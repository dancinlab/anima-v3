"""Phase streams, frozen probes, and held-out eval items.

The stream carries EXPLICIT flip supervision (polarity-consistent co-occurrence
grids), not merely shifted collocation statistics. This is not decoration: v1's
NAT-ATOM law (`l4-morph-atom-amplifier`) says atomicity is an AMPLIFIER, not a
signal source — natural-distribution rescue FAILED. A stream with no taught flip
signal would read chance even in the ORACLE arm, and the pilot would kill the rig
for a reason that has nothing to do with codecs.

Deterministic, stdlib only.
"""

from __future__ import annotations

import random

from codec import SENTINEL
from lang import render, to_jamo
from spec import neg_forms, plain_forms

# A polarity marker word pair: the stream states the polarity of each utterance
# explicitly, so "flip" is a learnable supervised relation rather than a hope.
POS_MARK = "ㄱㄲ"   # arbitrary non-syllable marks, outside the stem alphabet
NEG_MARK = "ㄳㄴ"


def _weighted_index(rng: random.Random, weights: list) -> int:
    """Deterministic weighted pick — `random.choices` uses the same stream but we
    keep it explicit so the draw cannot change if CPython's impl changes."""
    x = rng.random()
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if x <= acc:
            return i
    return len(weights) - 1


def line(spec: dict, phase: int, rng: random.Random, allow_heldout_neg: bool = False) -> str:
    """One training line: a stem + one affix, plus its explicit polarity mark.

    Held-out stems NEVER co-occur with a NEG affix in either phase (invariant 4):
    they DO appear with PLAIN affixes, so the stems themselves are in-distribution
    and only the COMPOSITION (held-out stem x NEG allomorph) is novel. That is the
    difference between measuring recombination and measuring vocabulary coverage.
    """
    stems = spec["stems"]
    weights = spec["colloc"]["w1"] if phase == 1 else spec["colloc"]["w2"]
    heldout = set(spec["heldout_stems"])

    idx = _weighted_index(rng, weights)
    stem = stems[idx]
    is_heldout = stem in heldout

    use_neg = rng.random() < 0.5
    if is_heldout and not allow_heldout_neg:
        use_neg = False   # the invariant: no held-out stem ever meets a NEG affix

    if use_neg:
        af = rng.choice(neg_forms(spec, phase))
        mark = NEG_MARK
    else:
        af = rng.choice(plain_forms(spec, phase))
        mark = POS_MARK
    return render(stem, [af]) + mark


def stream(spec: dict, phase: int, seed_offset: int = 0):
    """Iterator of sentinel-framed jamo text, capped at the phase's byte budget.

    Framing matches what the model trains on EXACTLY (invariant 7). v1's
    instrumentation bug #3 was precisely probe-framing != stream-format, which
    pushed probe NLL above uniform and made four arms look dead. Here framing is
    a generator invariant, not an eval afterthought.
    """
    if phase not in (1, 2):
        raise ValueError(f"phase must be 1 or 2: {phase}")
    rng = random.Random(spec["seed"] * 1000 + phase * 7 + seed_offset)
    budget = spec["phase_bytes"][phase - 1]
    emitted = 0
    while emitted < budget:
        chunk = to_jamo(line(spec, phase, rng)) + SENTINEL
        b = chunk.encode("utf-8")
        emitted += len(b)
        yield chunk


def stream_sample(spec: dict, phase: int, n_lines: int) -> list:
    """A bounded sample of the phase stream — what the codec is fit on.

    Fitting BPE on the full 150MB phase is unnecessary and slow; the merge table
    converges long before that. n_lines is recorded in the card.
    """
    rng = random.Random(spec["seed"] * 1000 + phase * 7 + 991)
    return [to_jamo(line(spec, phase, rng)) for _ in range(n_lines)]


PROBE_N = 256
PROBE_LEN = 64      # in JAMO (= 192 bytes exactly); see codec.py's indexing note


def probes(spec: dict) -> list:
    """256 frozen jamo strings of EXACTLY 64 jamo — the seam's probe set.

    Stratified in thirds: phase-1-affix forms / phase-2-novel-affix forms /
    stem-shared forms. Rectangular by construction (invariant 2): equal length,
    no padding, so the boundary-delta matrix has no constant columns to inflate
    the rank estimate for free.
    """
    rng = random.Random(spec["seed"] + 4242)
    stems = spec["stems"]
    p1_neg, p2_novel = neg_forms(spec, 1), spec["novel_neg_forms"]
    plains = plain_forms(spec, 1)

    out = []
    for i in range(PROBE_N):
        bucket = i % 3
        buf = ""
        while len(buf) < PROBE_LEN:
            stem = rng.choice(stems)
            if bucket == 0:
                af = rng.choice(p1_neg)
            elif bucket == 1:
                af = rng.choice(p2_novel)
            else:
                af = rng.choice(plains)
            buf += to_jamo(render(stem, [af]))
        out.append(buf[:PROBE_LEN])
    return out


def eval_items(spec: dict) -> list:
    """Held-out forced-choice flip items: held-out stem x NOVEL NEG allomorph.

    Each item offers `pos` and `neg` renderings of the same stem; the model must
    pick the one matching `label`. Chance = 0.50 by construction — the recovered
    H_9288 protocol's format, not an F-score (H_001's G-5 finding).

    Candidate pairs = 128 held-out stems x 12 novel NEG allomorphs = 1536, which
    must clear N_required AFTER leak filtering (invariant 3).
    """
    rng = random.Random(spec["seed"] + 777)
    heldout = spec["heldout_stems"]
    novel = spec["novel_neg_forms"]
    plains = plain_forms(spec, 2)

    items = []
    for si, stem in enumerate(heldout):
        for ai, af in enumerate(novel):
            plain = plains[(si * len(novel) + ai) % len(plains)]
            items.append({
                "stem": stem,
                "stem_id": si,
                "affix": af,
                "affix_id": ai,
                "pos": render(stem, [plain]),
                "neg": render(stem, [af]),
                "label": "neg" if rng.random() < 0.5 else "pos",
            })
    return items
