"""anima_v3 — shared runnable harness for HYPOTHESES hypothesis cards.

Deterministic, dependency-free (stdlib only) primitives for the anima-v3 problem.
HYPOTHESES cards reference these functions from their per-hypothesis run scripts
under `state/<hX>/` (shared machinery lives in repo-root `tool/`, per-hypothesis
runs live in `state/`).

Every function is a closed-form public relation — no fitting, no hidden constants
beyond documented defaults. All inputs are explicit so a card's falsifiers can be
evaluated against the returned numbers.

Scope note: this module owns the ESTIMATORS, not the experiment. A card's run
script extracts raw quantities (seam activations, CE values, byte counts) from
whatever rig produced them and passes them here; the estimator that turns those
into a gate verdict is pre-registered, deterministic, and identical across runs.
That separation is what makes two runs comparable at all.

The two gates below are non-negotiable for every family
(`ARCHITECTURE.json` -> `verification.inherited-gates`) — they are the exact
measurements whose absence killed v1:

  * L1 effective-rank check — does the mechanism's seam carry more than one bit?
    (v1's emit-seam measured rank-1: it visited 2 of 4 codes and the only bit it
    ever learned was the gate's own existence.)
  * L2 ablation check — cut the channel; does CE actually move? (v1's OMEGA moved
    0.0009 nats = decoration.)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

LN2 = math.log(2.0)


# --- linear algebra (stdlib-only, deterministic) -------------------------------

def gram_matrix(vectors: list, center: bool = True) -> list:
    """Gram matrix G = X^T X of a seam activation set.

    `vectors` is a list of observations, each a list of floats of equal width
    (rows = observations, columns = seam channels). With `center=True` each
    column has its mean removed first, so G is the (unnormalized) covariance and
    the estimator measures how many directions the seam actually VARIES along —
    a seam pinned to one constant vector is rank-0 variation, not rank-1.
    """
    if not vectors:
        raise ValueError("vectors must be non-empty")
    width = len(vectors[0])
    if width == 0:
        raise ValueError("vectors must have non-zero width")
    for v in vectors:
        if len(v) != width:
            raise ValueError(f"ragged vectors: expected width {width}, got {len(v)}")

    x = [list(map(float, v)) for v in vectors]
    if center:
        n = len(x)
        means = [sum(row[j] for row in x) / n for j in range(width)]
        x = [[row[j] - means[j] for j in range(width)] for row in x]

    return [
        [sum(row[i] * row[j] for row in x) for j in range(width)]
        for i in range(width)
    ]


def _jacobi_eigenvalues(matrix: list, tol: float = 1e-12, max_sweeps: int = 100) -> list:
    """Eigenvalues of a real SYMMETRIC matrix via the cyclic Jacobi method.

    Deterministic and stdlib-only (no numpy). Returns eigenvalues sorted
    descending. Jacobi is O(n^3) per sweep and is chosen over anything faster
    because a seam is narrow (a handful of channels) and reproducibility across
    runs matters more than speed here.
    """
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise ValueError("matrix must be square")
    a = [list(map(float, row)) for row in matrix]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(a[i][j] - a[j][i]) > 1e-9 * max(1.0, abs(a[i][j])):
                raise ValueError("matrix must be symmetric")

    for _ in range(max_sweeps):
        off = sum(a[p][q] ** 2 for p in range(n) for q in range(n) if p != q)
        if off <= tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) <= 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                sign = 1.0 if theta >= 0.0 else -1.0
                t = sign / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk

    return sorted((a[i][i] for i in range(n)), reverse=True)


def singular_values(vectors: list, center: bool = True) -> list:
    """Singular values of the seam activation set (rows = observations).

    Computed as sqrt of the eigenvalues of the Gram matrix. Negative eigenvalues
    from floating-point noise are clamped to 0 (the Gram matrix is PSD by
    construction, so a negative value is numerical, not physical).
    """
    eigenvalues = _jacobi_eigenvalues(gram_matrix(vectors, center=center))
    return [math.sqrt(max(0.0, ev)) for ev in eigenvalues]


# --- L1 gate: effective rank of the seam ---------------------------------------

def participation_ratio(sv: list, eps: float = 1e-12) -> float:
    """Participation ratio PR = (sum sv^2)^2 / sum sv^4 — the PRE-REGISTERED L1
    estimator for this campaign (`ARCHITECTURE.json` -> `gates.L1`).

    Reads as "how many directions carry comparable ENERGY" (it weights by sv^2,
    i.e. variance, where `effective_rank` weights by sv). An exactly rank-1 seam
    returns 1.0; k directions of equal energy return k.

    Preferred over `effective_rank` for the gate because the threshold is
    calibrated against a rank-1 null whose PR is exactly 1 by construction,
    which makes "how far above rank-1 is this" a statement about energy rather
    than about the shape of a long noise tail.
    """
    if not sv:
        return 0.0
    sum_sq = sum(s * s for s in sv)
    sum_quad = sum(s ** 4 for s in sv)
    if sum_quad <= eps:
        return 0.0
    return (sum_sq * sum_sq) / sum_quad


def effective_rank(sv: list, eps: float = 1e-12) -> float:
    """Entropy-based effective rank (Roy & Vetterli): exp(H(p)), where
    p_i = sv_i / sum(sv) and H is Shannon entropy in nats.

    Reads as "how many directions does this seam effectively use". A seam that
    lives on one direction returns ~1.0; a seam spreading energy evenly over k
    directions returns ~k. This is the continuous generalization of v1's
    code-counting verdict (2 of 4 codes visited), and it is continuous ON
    PURPOSE: a discrete count cannot distinguish a seam that genuinely uses a
    second direction from one that twitches along it.

    Pre-register the threshold on THIS quantity, not on a code count.
    """
    total = sum(sv)
    if total <= eps:
        return 0.0
    entropy = 0.0
    for s in sv:
        p = s / total
        if p > eps:
            entropy -= p * math.log(p)
    return math.exp(entropy)


def stable_rank(sv: list, eps: float = 1e-12) -> float:
    """Stable rank: sum(sv^2) / max(sv)^2 — a second, independent rank estimator.

    Reported alongside `effective_rank` as a cross-check: the two disagree when
    the spectrum has a heavy tail of near-zero directions, and a gate verdict
    that flips depending on which estimator you chose is not a verdict.
    """
    if not sv:
        return 0.0
    top = max(sv)
    if top <= eps:
        return 0.0
    return sum(s * s for s in sv) / (top * top)


# --- L2 gate: ablation delta ----------------------------------------------------

def ablation_delta(ce_ablated: float, ce_full: float) -> float:
    """Load-bearingness of a channel in nats: CE(ablated) - CE(intact).

    Positive means cutting the channel HURT prediction — the channel was
    carrying something. Zero-ish means the channel was decoration: the rest of
    the model was already predicting whatever it supplied.

    v1's reference number for "decoration": 0.0009 nats.
    """
    return ce_ablated - ce_full


def ablation_fraction(ce_ablated: float, ce_full: float, ce_floor: float) -> float:
    """Ablation delta as a fraction of the headroom above a measured floor:
    (ce_ablated - ce_full) / (ce_floor - ce_full).

    Raw nats are not comparable across rigs — 0.01 nats is huge on a task whose
    total headroom is 0.02 and noise on a task whose headroom is 3.0. `ce_floor`
    is the pre-measured CE of the scrambled/no-information control, so this
    returns "what share of the channel's MAXIMUM possible contribution did
    ablation actually cost", which is comparable across rigs and is the quantity
    a threshold should be pre-registered on.
    """
    headroom = ce_floor - ce_full
    if headroom <= 0.0:
        raise ValueError(
            f"ce_floor ({ce_floor}) must exceed ce_full ({ce_full}) — "
            "a floor at or below the intact CE means the control is broken"
        )
    return (ce_ablated - ce_full) / headroom


# --- codec-invariant measurement (L6: measurement is the grave) -----------------

def bits_per_byte(ce_nats_per_token: float, n_tokens: int, n_bytes: int) -> float:
    """Cross-entropy converted to bits per BYTE of the underlying text.

    When the codec changes, per-token CE is not comparable between runs — a
    coarser vocabulary lowers token count and per-token CE at once while
    predicting exactly as well. Bits-per-byte divides by a quantity the codec
    cannot move (the raw bytes), which is the only reason a fixed-codec vs
    adaptive-codec comparison means anything.

    This is v1's single inherited measurement discipline. Any comparison that
    crosses a codec boundary MUST be expressed in this unit.
    """
    if n_bytes <= 0:
        raise ValueError(f"n_bytes must be > 0: {n_bytes}")
    if n_tokens <= 0:
        raise ValueError(f"n_tokens must be > 0: {n_tokens}")
    return (ce_nats_per_token * n_tokens) / (LN2 * n_bytes)


# --- closed-form power + chance bands (G-2 / G-4) ------------------------------

def binom_pmf(k: int, n: int, p: float) -> float:
    """Exact binomial probability mass P(X = k) for n trials at rate p."""
    if not (0 <= k <= n):
        raise ValueError(f"k must be in [0, n]: k={k}, n={n}")
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"p must be in [0,1]: {p}")
    return math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))


def binom_sf(k: int, n: int, p: float) -> float:
    """Exact upper tail P(X >= k). Summed directly — no normal approximation.

    The approximation is what makes a razor-thin verdict unfalsifiable: near the
    band edge the normal and exact answers straddle the threshold, and then the
    verdict is a property of the estimator rather than of the data.
    """
    return sum(binom_pmf(i, n, p) for i in range(k, n + 1))


def binom_cdf(k: int, n: int, p: float) -> float:
    """Exact lower tail P(X <= k)."""
    return sum(binom_pmf(i, n, p) for i in range(0, k + 1))


def binom_two_sided_p(k: int, n: int, p: float) -> float:
    """Two-sided exact binomial p-value for observing k successes under rate p.

    Doubles the smaller tail (clipped at 1.0) — the standard convention for a
    symmetric null (p = 0.5), which is the only case this campaign uses it for.
    """
    tail = min(binom_cdf(k, n, p), binom_sf(k, n, p))
    return min(1.0, 2.0 * tail)


def chance_band(n: int, p0: float = 0.5, conf: float = 0.99) -> tuple:
    """Exact binomial chance band as a (low_rate, high_rate) pair of RATES.

    Returns the widest interval of observed rates that a pure-chance process at
    p0 produces with probability >= conf. A score inside this band is not
    distinguishable from chance at that confidence — which is the whole question
    G-4 asks of a control arm.
    """
    if n <= 0:
        raise ValueError(f"n must be > 0: {n}")
    if not (0.0 < conf < 1.0):
        raise ValueError(f"conf must be in (0,1): {conf}")
    alpha = 1.0 - conf
    lo = 0
    while lo <= n and binom_cdf(lo, n, p0) < alpha / 2.0:
        lo += 1
    hi = n
    while hi >= 0 and binom_sf(hi, n, p0) < alpha / 2.0:
        hi -= 1
    return (lo / n, hi / n)


def two_proportion_n(p1: float, p2: float, alpha: float = 0.01, power: float = 0.99) -> int:
    """Per-arm N for a two-proportion test to detect p1 vs p2 (normal approx).

    n = (z_{alpha/2} + z_{beta})^2 * [p1(1-p1) + p2(1-p2)] / (p1-p2)^2

    Normal approximation is appropriate HERE (unlike the chance band): this sizes
    a study before it exists, so the answer only needs to be right to the nearest
    handful of items, and the operating point is far from 0 or 1.
    """
    if p1 == p2:
        raise ValueError("p1 and p2 must differ — a zero effect needs infinite N")
    for name, p in (("p1", p1), ("p2", p2)):
        if not (0.0 < p < 1.0):
            raise ValueError(f"{name} must be in (0,1): {p}")
    z_a = normal_quantile(1.0 - alpha / 2.0)
    z_b = normal_quantile(power)
    var = p1 * (1.0 - p1) + p2 * (1.0 - p2)
    n = ((z_a + z_b) ** 2) * var / ((p1 - p2) ** 2)
    return math.ceil(n)


def normal_quantile(p: float) -> float:
    """Standard-normal inverse CDF via Acklam's rational approximation
    (|error| < 1.15e-9 over the open interval) — stdlib-only, deterministic."""
    if not (0.0 < p < 1.0):
        raise ValueError(f"p must be in (0,1): {p}")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    dd = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
          3.754408661907416e+00]
    p_low, p_high = 0.02425, 1.0 - 0.02425
    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((dd[0]*q+dd[1])*q+dd[2])*q+dd[3])*q+1.0)
    if p > p_high:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((dd[0]*q+dd[1])*q+dd[2])*q+dd[3])*q+1.0)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1.0)


# --- falsifier harness --------------------------------------------------------

@dataclass
class Falsifier:
    """One pre-registered, measurable falsifier. `predicate(metrics) -> bool`
    returns True when the falsifier is TRIGGERED (hypothesis component refuted)."""

    name: str
    predicate: object  # callable(dict) -> bool
    desc: str = ""


def evaluate(metrics: dict, falsifiers: list) -> dict:
    """Run each falsifier against the measured metrics. A falsifier PASSes when
    it is NOT triggered. Returns a verdict ledger (all-stdlib, JSON-safe)."""
    results = []
    for f in falsifiers:
        triggered = bool(f.predicate(metrics))
        results.append(
            {"name": f.name, "triggered": triggered, "status": "FAIL" if triggered else "PASS"}
        )
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    return {
        "metrics": metrics,
        "falsifiers": results,
        "n_pass": n_pass,
        "n_total": len(results),
        "all_pass": n_pass == len(results),
    }
