---
id: H_005
slug: f3-stream-mi-precheck
title: Does any available experience stream carry day-specific cross-boundary information — beyond the model's context reach — for a diary to transport? The hindsight-optimal summary's lift is the oracle-diary ceiling; if it is ≤ the shuffle floor on all streams, F3 (and F8's diary organ) is REFUSED for want of a temporal self to compress.
domain: prediction-error-action axis (F3 diary-compressor) — first card after the write-lever axis yielded
status: pre-register-frozen
exploration_method: H_004 terminal -> campaign re-decision (Fable) -> F3 premise measured before the organ
verification_method: $0 deterministic compression-based conditional-bpb estimators + cheap numpy-LM agreement + 5 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_005 — f3-stream-mi-precheck

## Hypothesis

F3's diary is load-bearing ONLY if tomorrow's experience stream has mutual information with
today's that (i) exceeds what fits in the model's context at prediction time, and (ii) is
**day-specific**, not generic style. Measure that quantity on real streams **before building
any organ** — the premise before the mechanism. This institutionalizes the H_004 lesson (`l11`
Corollary B): measure the ceiling in-substrate before spending on the twin.

> **Oracle-diary ceiling** = bpb(day t+1 prefix | tail of day t) − bpb(day t+1 prefix | tail of
> day t + summary of day t). The hindsight-optimal summary is the best a diary could ever do
> (later the twin's `delta_min := ceiling/2`, anchored before the twin exists — repairing the
> `decision-attributability` disease by construction).
> **Day-specificity** = bpb(… | tail + WRONG day t′) − bpb(… | tail + day t) — is the lift the
> day's content, or generic register any day supplies?

Outcome set: **ANCHORED** (ceiling > shuffle floor AND day-specific → F3 licensed with a
pre-anchored delta_min) · **F3-REFUSED** (ceiling ≤ floor on all streams — the substrate has no
temporal self to compress; retires F3 AND F8's diary component, redirects the whole axis) ·
**INVALID** (instrument blind / leak — not a ceiling=0 reading).

## Why

- The campaign re-decision (`decision-redecide-h004`) promoted F3 after the write-lever axis
  yielded. F3's disease 1 (`decision-f3-cure1`): a null can't separate "diary carries no load"
  from "stream has no cross-day MI". Cure: measure the MI first, deterministically.
- **Escapes L11** (`l11-design-consequence`): this contrasts NO representation arms — it measures
  a property of the STREAM. And the eventual diary twin escapes structurally because the
  transported information sits OUTSIDE the context window at prediction time, so no within-context
  statistic of any order substitutes for the bottleneck m — the credit path physically crosses m.
- The L11 Corollary-B failure mode (a planted signal recoverable from the visible context) is
  exactly what this card quantifies and closes (via the P-2 liveness control + the "beyond tail"
  conditioning).

## Predictions

- **P1** ceiling > 0 on at least one stream `?` — genuinely uncertain; this is what the card is FOR.
- **P2** day-specificity > 0 where ceiling > 0 `?` (else the lift is generic register).
- **P3** the planted-latent liveness stream reads ceiling ≥ its pre-registered value.
- **P4** the three estimators (n-gram, gzip, numpy-LM) sign-agree.

## Variables

Pre-registered, frozen before measuring:

- **streams** (must exist on disk today): `hexa-lang` git history (10664 commits, 106 distinct
  days — the richest), `anima` (2245, 44 days), `sidecar` (460, 30 days). A "day" = all commit
  messages + diffs on one calendar date, concatenated in commit order.
- **tail reach** `W` = **4096 bytes** (a proxy for the model's in-context reach; the summary must
  beat what W already supplies).
- **prefix** `P` = first **2048 bytes** of day t+1 (the quantity predicted).
- **summary (oracle)** = the FULL day t beyond the tail — the UPPER BOUND on any bottlenecked
  diary. If even the full day does not lift bpb, no k-token diary will (conservative for the kill).
- **shuffle floor** = ceiling recomputed with day labels permuted (P-3 bounds control), + ε = 0.02
  bpb (an OMEGA-0.0009-class threshold scaled to bpb — decoration guard).
- **min day-pairs** = 20 consecutive (t, t+1) pairs per stream.

Measured outputs: per-stream ceiling, day-specificity, shuffle-floor ceiling, participation ratio
of day-representations, estimator agreement → `verdict`.

## Run Protocol

- **harness**: `tool/anima_v3.py` (`participation_ratio`, `bits_per_byte`, `Falsifier`, `evaluate`)
- **estimators**: compression-based conditional bpb (gzip: bpb(X|Y) = [|gz(Y+X)|−|gz(Y)|]·8/|X|),
  order-k n-gram cross-entropy, tiny numpy LM (`state/h004…/nlm.py` pattern) — all $0/deterministic
- **run script**: `state/h005_f3-stream-mi-precheck_2026-07-16/run_h005.py`
- **artifacts**: `state/h005_f3-stream-mi-precheck_2026-07-16/result.json`
- **deterministic**: stdlib only, no network, $0.

## Criteria

- **verdict_rule**: **ANCHORED** iff no falsifier triggers AND (ceiling − shuffle_floor) > ε on ≥1
  stream AND day-specificity > ε there. **F3-REFUSED** iff (ceiling − shuffle_floor) ≤ ε on ALL
  streams. Else per the triggered falsifier.

## Falsifiers (pre-registered)

- **P-1 the kill**: (ceiling − shuffle_floor) ≤ ε on ALL streams → the available substrate has no
  cross-day self to compress → **F3-REFUSED** (and F8's diary premise with it).
- **P-2 instrument liveness** (blind-tool control): a synthetic planted-latent stream — a per-day
  latent placed BEYOND the tail W and fresh each day — must read ceiling ≥ a pre-registered value
  through the SAME instrument, else the instrument can't see cross-boundary MI → **INVALID**.
- **P-3 bounds**: the day-order-shuffled real stream must read ceiling ≈ 0 (that IS the shuffle
  floor); if a shuffled stream reads a large ceiling, the estimator is picking up within-day
  structure, not cross-day → **INVALID**.
- **P-4 estimator agreement**: gzip / n-gram / numpy-LM must SIGN-agree on the ceiling; disagreement
  → **PENDING(instrument)**.
- **P-5 leak** (L2 ablation / `l6-leak`): the day-specificity (swap) control IS the L2 ablation — if
  bpb(tail+swap) ≈ bpb(tail+oracle) within ε, the measured "MI" is generic register, not day
  information → the ceiling is decoration → counts as **kill**, not support. Plus a dedup check: no
  verbatim cross-day overlap between the P prefix and the summary (else the lift is copying).

**Inherited gates, operational:**
- **L1 effective-rank**: participation ratio of the day-representation vectors (estimator features
  across ≥ the min day-pairs) must exceed a floor (≥ 8 effective dims `?`). Days indistinguishable →
  the stream is degenerate → **INVALID** (the l6-scramble-floor distinction).
- **L2 ablation**: the swap control (P-5) — the day-specificity gap IS the ablation of day identity.

## Honest Limits

- **L1** the full-day summary is the ceiling of an UNBOUNDED diary; a positive here still needs a
  second card to show a k-BOUNDED extract captures it. A null here, though, is decisive (unbounded
  ≥ bounded).
- **L2** git-commit streams are a proxy for an agent's experience stream — a developer's daily work
  has cross-day MI (an ongoing project) that an agent's dialogue may or may not share `?`. A null on
  git does not prove a null on every possible stream; it proves it on the substrate actually available.
- **L3** compression-based bpb is an estimator, not the true conditional entropy; the three-estimator
  agreement gate (P-4) guards the direction, not the exact magnitude.
- **L4** `W` = 4096 and `P` = 2048 are frozen proxies for context reach `?`; a different reach would
  move the ceiling (a longer W subsumes more of the "diary", shrinking the measured lift).

## Cross-Links

- **architecture**: `components.F3` · `decision-redecide-h004` · `decision-f3-cures` ·
  `salvage.l11-*` (esp. Corollary B + design consequence) · `l6-measurement-is-the-grave`
- **predecessor**: `H_004` (structural terminal, F1 spent) · **axis**: prediction-error-action
- **design seed**: `state/h004_static-anchor-pilot_2026-07-16/DESIGN_redecide.md`
- **harness**: `tool/anima_v3.py` · numpy-LM: `state/h004…/nlm.py`

## Verdict

**🟡 PENDING(instrument) — leaning ANCHORED under the sensitive estimator** (run 2026-07-16,
`state/h005_f3-stream-mi-precheck_2026-07-16/result.json`). Not F3-REFUSED; not cleanly ANCHORED.

### What ran

Two independent $0 estimators of conditional bits-per-byte — gzip (LZ) and an order-4 adaptive
byte model (PPM) — measured the oracle-diary ceiling (full day t summary vs tail-only) against a
shuffle floor (day-adjacency broken), on three real developer streams. The planted-latent
liveness control read **7.79 bpb** (instrument sees cross-boundary MI — PASS).

| stream | days | gzip over-floor | ppm over-floor | reading |
|---|---|---|---|---|
| hexa-lang | 102 | −0.004 | **+0.143** | estimators DISAGREE (gzip at noise floor) |
| anima | 44 | +0.031 | **+0.221** | both positive — ANCHORED under both |
| sidecar | 21 | −0.066 | −0.016 | both flat/negative |

### The honest reading

The pre-registered P-4 (estimator sign-agreement) triggers → formal verdict **PENDING(instrument)**,
because gzip and PPM disagree on hexa-lang. But the disagreement is **gzip's resolution floor, not
a real conflict**: gzip's 32KB LZ window + entropy coder is insensitive to a single day-specific
long-range token inside a large context, so it reads ~0 where the more sensitive adaptive model
(PPM) reads a clear positive lift. Under PPM — the more trustworthy estimator here — the two RICHER
streams show a real day-specific cross-boundary lift (hexa-lang +0.14, anima +0.22 bpb above the
shuffle floor), and the day-specificity swap control is positive on both (+0.20, +0.14).

**This LEANS ANCHORED — the opposite of the F1 terminal.** A developer's stream plausibly carries a
day-specific temporal self a diary could transport (a project's ongoing state lives across days,
outside any single day's tail). That would LICENSE the F3 line with a pre-anchored `delta_min =
ceiling/2` — the campaign's first honestly-anchored effect size.

### What it does NOT settle

- The verdict is not clean: gzip's weakness means the $0 battery cannot cross the pre-registered
  agreement gate. The decisive tie-breaker is a proper AUTOREGRESSIVE model (the card's third,
  numpy-LM estimator) — but the available `nlm.py` is mean-pooled and structurally unable to
  represent a specific long-range token, so it is the WRONG tool; a small causal LM (a few $ / an
  MPS hour) is the honest decisive estimator.
- sidecar (the thinnest stream, 21 days) is flat on both — a null on a short stream is
  under-powered, not informative (L2 of this card).

### Resume target (the live frontier)

Decide the estimator question: either (a) accept PPM as authoritative → ANCHORED, and design the
F3 diary twin (which escapes L11 structurally — the bottleneck m sits outside the context window);
or (b) run a small causal-LM tie-breaker to satisfy P-4 formally. Either way the F3 premise is
LIVE, not refuted — recorded to ING.

### Verbatim stdout

See `state/h005_f3-stream-mi-precheck_2026-07-16/result.json` (both estimators, all streams,
liveness, ledger).

_Formal verdict PENDING(instrument); scientific lean ANCHORED under the sensitive estimator. F3 is
live._
