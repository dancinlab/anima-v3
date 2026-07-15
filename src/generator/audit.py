"""Leak scan — the audit that decides whether a win is a measurement or an echo.

`rig-drift-deficit-asserted` and invariant 4: every rendered eval string must
occur ZERO times as an exact substring of either phase stream, and held-out stems
must never co-occur with a NEG-class affix. v1's precedent is not hypothetical —
its one apparent win (GATED 0.345 << base) was a CA-neighbour lookahead LEAK and
evaporated leak-free (`l6-leak`).

Deterministic, stdlib only.
"""

from __future__ import annotations

from lang import from_jamo, parse, to_jamo
from spec import neg_forms
from stream import POS_MARK, NEG_MARK, SENTINEL


def _iter_words(stream_iter):
    """Yield whole sentinel-delimited stream words (jamo, mark stripped)."""
    marks = (to_jamo(POS_MARK), to_jamo(NEG_MARK))
    carry = ""
    for chunk in stream_iter:
        buf = carry + chunk
        words = buf.split(SENTINEL)
        carry = words.pop() if words else ""
        for w in words:
            for mk in marks:
                if w.endswith(mk):
                    w = w[: -len(mk)]
                    break
            if w:
                yield w
    if carry:
        for mk in marks:
            if carry.endswith(mk):
                carry = carry[: -len(mk)]
                break
        if carry:
            yield carry


def leak_scan(stream_iter, spec: dict, forms: list) -> dict:
    """Count stream words that PARSE to exactly one of `forms`.

    The leak question is "was this composed form ever EMITTED", not "does its
    jamo appear as a substring somewhere". Two weaker tests both give false
    positives here and were rejected: raw jamo substring (a 3-jamo affix collides
    everywhere), and whole-word prefix (a held-out stem's jamo can prefix an
    unrelated word). The only correct test is to recompose each stream word to
    its surface form and compare to the target set exactly — a word IS a leak iff
    it renders to a form in the set.
    """
    target_surface = set(forms)
    hits = {f: 0 for f in forms}
    for wj in _iter_words(stream_iter):
        surface = from_jamo(wj)
        if surface in target_surface:
            hits[surface] += 1
    return {"hits": hits, "total": sum(hits.values()), "clean": sum(hits.values()) == 0}


def heldout_neg_cooccurrence(spec: dict, stream_iter) -> int:
    """Times a stream word PARSES to (held-out stem + a NEG affix).

    Must be 0 in both phases — the invariant that makes the eval measure
    RECOMBINATION rather than coverage. Parse-based, not substring or prefix: the
    stream only ever emits held-out stems with PLAIN affixes, so a word that
    genuinely decomposes to (held-out stem, NEG-affix) is a real break, and a
    coincidental jamo collision is not (it will not parse that way).
    """
    heldout = set(spec["heldout_stems"])
    negs = set(neg_forms(spec, 1)) | set(neg_forms(spec, 2))
    all_affixes = sorted({a["form"] for a in spec["affixes_p1"]} | {a["form"] for a in spec["affixes_p2"]})
    stems = spec["stems"]
    count = 0
    for wj in _iter_words(stream_iter):
        surface = from_jamo(wj)
        try:
            stem, chain = parse(surface, stems, all_affixes)
        except ValueError:
            continue
        if stem in heldout and any(c in negs for c in chain):
            count += 1
    return count


def heldout_neg_cooccurrence(spec: dict, stream_iter) -> int:
    """Times a WHOLE stream word parses as (held-out stem + a NEG affix).

    Must be 0 in both phases — the invariant that makes the eval measure
    RECOMBINATION rather than coverage. Word-granular, not substring: a held-out
    stem's jamo can appear as a coincidental substring of an unrelated word, and
    a short NEG affix's jamo can prefix any number of PLAIN affixes, so a raw
    substring scan reports collisions that were never emitted. The stream only
    ever emits held-out stems with PLAIN affixes, so a true parse to (held-out
    stem, NEG-affix) is a real invariant break.
    """
    heldout = set(spec["heldout_stems"])
    negs = set(to_jamo(a) for a in set(neg_forms(spec, 1)) | set(neg_forms(spec, 2)))
    heldout_jamo = {to_jamo(s): s for s in heldout}
    count, carry = 0, ""
    for chunk in stream_iter:
        buf = carry + chunk
        words = buf.split(SENTINEL)
        carry = words.pop() if words else ""
        for w in words:
            for hj in heldout_jamo:
                if w.startswith(hj):
                    tail = w[len(hj):]
                    if any(tail.startswith(n) for n in negs):
                        count += 1
                    break
    return count
