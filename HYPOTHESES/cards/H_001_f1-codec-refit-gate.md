---
id: H_001
slug: f1-codec-refit-gate
title: The F1 twin rig (frozen vs adaptive codec, 10M params, drill scale) has the power, the instruments, and a specified metric to make a null attributable to the mechanism — or it does not, and must be refused before any GPU is rented.
domain: write-lever axis (F1 codec-is-the-self) — ARCHITECTURE.json `components.f1-codec-is-the-self`
status: pre-register-frozen
exploration_method: divergence (8 families) -> Fable 5 design pass (D1-D7) -> single-family selection on belief-killed-per-dollar
verification_method: deterministic closed-form harness (tool/anima_v3.py) + 5 pre-registered falsifiers
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_001 — does the F1 twin rig deserve to exist?

## Hypothesis

This card does **not** test whether F1 is true. It tests whether the cheap rig proposed
for F1 (`H_002`) can produce an **attributable** verdict. The claim, operationally:

> At drill scale (~10M params, synthetic agglutinative stream, matched byte budget),
> a null result on the frozen-vs-adaptive codec twin would be attributable to the
> **mechanism** (codec refit during training buys nothing), not to under-scale,
> under-power, blind instruments, or an unspecified metric.

Verdict is binary and is about the RIG, not about F1: **LICENSED** (H_002 may be run as
pre-registered) or **REFUSED** (H_002 must not be run until the named defect is repaired).

A card that cannot refuse its own successor is not a gate. `break-walls` classifies
under-invest as a *wall*, not a verdict — this card exists so that a drill-scale null
cannot be dismissed later with "maybe it emerges at 300M", and so that it cannot be
*accepted* while the rig was in fact blind.

## Why

- **Family selection (D1).** F1 alone. The campaign bet "F1 substrate + F3 objective"
  must be bought as two sequential cards, not one: composing them is confounded twice —
  (a) two levers move at once, so a null cannot be attributed and a win cannot assign
  credit (un-confounding needs the 2×2 factorial = two cards' cost wearing one card's
  name); (b) F3's diary `m` lives in token space, so an F1 refit changes the diary's
  alphabet underneath it, making the diary-swap control and scramble floor
  non-stationary — F3 would inherit F1's L6 comparability trap squared.
- **Why F1 first, not F3.** Belief-killed-per-dollar. An F1 null kills F1, kills F6's
  variation axis (F6 presupposes codec mutation is a live lever), and bounds
  `salvage.l4-write-side-crack` (b) — the campaign's **only** green causal measurement —
  down from "the codec is architecture" to "one-time static codec choice matters",
  leaving F4 as the write-lever axis's sole survivor. Roughly half the campaign's prior
  mass, for ≤$25. An F3 null at cheap scale kills much less because it is not
  attributable: it cannot separate "the diary carries no load" from "this corpus has no
  cross-day mutual information to carry", and the generic mechanism question (do forced
  bottleneck summaries carry load?) is already answered in the literature. F3 is the
  right SECOND card.
- **Axis (fake-diversity audit).** This buys information on the **write-lever axis
  (F1/F4)** — correct to buy first because it is the only axis with measured green
  causality (hence the only axis where a cheap rig has *known* power), and two other
  axes lean on it. The prediction-error-action axis's cheap questions are
  literature-answered and its campaign questions are wall-clock-bound.
- **Campaign rule (실측전 research).** `CLAUDE.md` mandates a research pass before
  renting compute. Done (see Cross-Links). The exact twin — from-scratch continual
  training through periodic codec refits on a drifting stream vs a frozen codec, matched
  byte budget, held-out recombination — **has not been run**. Adjacent work raises the
  prior (refit-to-domain reliably helps compression/downstream) but measures one-shot
  adapt-then-finetune, never a refit *organ*, and never recombination. One adjacent
  result sharpens this card's own gate: gist/bottleneck studies document steep
  singular-value decay — **near-rank-1 redundancy on the write side** — so the L1 gate
  below is not paranoia.

## Predictions

- **P1**: The synthetic drift schedule moves the codec: boundary-shift rate on frozen
  probes ≥ 5% of byte positions between the phase-1 and phase-2 refits. `?`
- **P2**: Closed-form power for δ=+0.15 at α=0.01, power=0.99 around p≈0.62/0.77 requires
  **N ≥ ~400** non-overlapping held-out recombination items; the generator can emit them.
- **P3**: Every estimator reproduces its closed-form fixture (PR = 1.0 ± 0.1 on a rank-1
  boundary-delta matrix; PR = k ± 20% on rank-k fixtures; bpb to 1e-9).
- **P4**: MORPH-ATOM's control score 0.617 sits **outside** the 99% binomial chance band
  for the drill format — i.e. `salvage.L4` (b) was genuinely above floor.
- **P5**: The held-out recombination protocol can be restated unambiguously and in full.

## Variables

Inputs (pre-registered values, frozen before any run):

- `delta_min` = **+0.15** recombination F-score — half of MORPH-ATOM's measured +0.291.
  Source: `salvage.L4` (b). Halved because that measurement is **1 seed, synthetic**.
- `p_control` ≈ **0.617**, `p_treat` ≈ **0.77** — MORPH-ATOM control/treatment. Source:
  `salvage.L4`. Marked `?` until G-5 recovers the protocol that produced them.
- `alpha` = **0.01**, `power` = **0.99** — pre-registered, not adjustable post-hoc.
- `pr_floor` = **2.0** — the hard L1 floor. Derivation: an exactly rank-1 boundary-delta
  matrix has PR = 1 by construction (all drift from one merge family = the F1 analogue of
  v1's one-bit seam). 2.0 = "at least two orthogonal change-directions of comparable
  energy" = the minimum that is *strictly more* than v1's death mode.
- `pr_null_draws` = **1000**, single-pattern-drift null, fixed documented seed → `null_99`.
  Binding L1 threshold = **max(2.0, null_99)** (noise inflates PR above 1 even when the
  truth is rank-1, so the floor alone is not enough).
- `theta_L2` = **max(5·σ_seed, 0.004 bpb)**. Derivation of the absolute term: v1's OMEGA
  decoration signature 0.0009 nats/token ≈ 0.0013 bits/token ÷ ~3.5 bytes/token `?`
  ≈ 0.0004 bpb; ×10 = one order of magnitude above the measured signature of decoration.
  `σ_seed` = std of post-drift bpb across the 5 frozen-arm seeds, **measured and frozen in
  code before any adaptive arm runs**.
- `drift_floor` = **5%** of byte positions `?` — calibrate against MORPH-ATOM's
  jamo-vs-BPE segmentation distance if recoverable.
- `chance_p0`, `n_items` for the drill format — **`?`, blocked on G-5**.

Outputs (measured by this card):

- `n_required` (closed-form power), `chance_band_99` (binomial), fixture residuals,
  boundary-shift rate, protocol-reconstruction status → `rig: LICENSED | REFUSED`.

## Run Protocol

- **harness**: `tool/anima_v3.py` — `participation_ratio`, `effective_rank`,
  `stable_rank`, `singular_values`, `gram_matrix`, `bits_per_byte`, `ablation_delta`,
  `ablation_fraction`, `Falsifier`, `evaluate`
- **fixtures**: `tool/test_anima_v3.py` (wired into `sidecar ci` as `estimator-fixtures`)
- **run script**: `state/h001_f1-codec-refit-gate_2026-07-16/run_h001.py`
- **deterministic**: stdlib only, no randomness beyond a fixed documented seed, no
  network, $0 local
- **run cmd**: `python3 state/h001_f1-codec-refit-gate_2026-07-16/run_h001.py`
- **artifacts**: `state/h001_f1-codec-refit-gate_2026-07-16/result.json`

## Criteria

- **C1 power**: G-2 yields a finite `n_required` the generator can actually emit.
- **C2 instruments**: every fixture in G-3 passes.
- **C3 lever**: G-1's boundary-shift rate ≥ `drift_floor`.
- **C4 salvage**: G-4's chance band excludes 0.617.
- **C5 metric**: G-5's protocol is fully restated in this card.
- **verdict_rule**: `rig = LICENSED` iff **no** falsifier triggers. Any trigger →
  `rig = REFUSED`, and H_002 is blocked until the named defect is repaired.
  A REFUSED verdict is a **result**, not a delay (`honesty`).

## Falsifiers (pre-registered, measurable)

- **G-1 drift existence** (negative control on the lever): refit the BPE-jamo codec on
  phase-1 vs phase-2 generator output; if the boundary-shift rate on frozen probes
  < `drift_floor` (5% of positions `?`), the stream cannot move the codec at all and the
  twin compares two frozen codecs under different names → **REFUSE**.
- **G-2 closed-form power**: two-proportion test, α=0.01, power=0.99, δ=`delta_min`
  around p≈0.62/0.77 → `n_required`. If the generator cannot emit `n_required`
  **non-overlapping** held-out recombination items → the rig is underpowered by
  construction; a null would be meaningless → **REFUSE**.
- **G-3 estimator fixtures** (positive control on the instruments): `participation_ratio`
  must return 1.0 ± 0.1 on a constructed rank-1 boundary-delta matrix and k ± 20% on
  rank-k fixtures; bpb accounting must reproduce its closed-form reference to 1e-9. Any
  failure → the instrument is blind, nothing downstream is interpretable → **REFUSE**.
- **G-4 salvage bounds check** (this card's own kill-power): compute the closed-form 99%
  binomial chance band for the drill format. **If MORPH-ATOM's control score 0.617 lies
  inside it, `salvage.L4` (b) was never above floor** — the campaign's only green causal
  measurement was noise, the whole write-lever axis is demoted, and this card has
  retroactively indicted the evidence that selected its own family. → **REFUSE**, and
  escalate to a campaign-level re-ranking.
- **G-5 protocol reconstruction**: the "H_9288 held-out recombination protocol" is cited
  in the SSOT but **specified nowhere in this repo** — v1 is discarded and `state/` holds
  only the divergence seed. The metric must be restated here in full (item construction,
  scoring, chance rate, split rule). If it cannot be reconstructed unambiguously →
  **REFUSE** rather than eyeball it (a metric reconstructed *after* seeing results is not
  a pre-registration).

## Honest Limits

- **L1**: A drill win establishes **mechanism, not identity**. "Idiolect = self" remains
  unbought until the full ~300M natural-stream rig (~$300–1000 `?`). This card only
  decides whether that rig deserves to exist.
- **L2**: The power calc is anchored on the **weakest green in salvage** — MORPH-ATOM is
  1 seed, synthetic. If +0.291 was luck, `delta_min` = 0.15 is miscalibrated. Hedges:
  halved effect size, 3 seeds/arm in H_002, and G-4 catches the worst case.
- **L3**: **Scale transfer is unknown in both directions.** Swap cost at 10M (where the
  embedding mass fraction is far higher than at 300M) may overstate H_002's F-6; codec
  effects could also shrink with scale. The pre-commitment "drill-scale null = F1 family
  dead" is a campaign **choice**, stated now so it cannot be relitigated after results.
- **L4**: **Designer degrees of freedom in the drift schedule** — the generator is built
  by the same party that wants F1 to live. Freezing generator params here, before any
  training exists, bounds but does not eliminate this.
- **L5**: `σ_seed` from 5 seeds is a rough null-spread estimate (~±35% error on σ itself);
  the 5× multiplier and the 0.004 bpb absolute floor backstop it.
- **L6**: Representative-not-measured numbers, all marked `?`, none load-bearing for the
  verdict logic: MPS wall-clock, `drift_floor` 5%, ~3.5 bytes/token.
- **L7**: The fixtures in `tool/test_anima_v3.py` were authored while building the
  harness, i.e. the instrument and its positive control share an author. They are
  closed-form (PR of a rank-1 matrix is 1 by algebra, not by convention), but a fixture
  suite cannot certify the *choice* of estimator, only its arithmetic.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `components.f1-codec-is-the-self`,
  `verification-inherited-gates`, `salvage.l4-write-side-crack`,
  `salvage.l1-one-bit-seam`, `salvage.l6-measurement-is-the-grave`
- **design seed**: `state/h001_f1-codec-refit-gate_2026-07-16/DESIGN_fable.md` (verbatim
  Fable 5 design, D1–D7 — seed of record, not the SSOT)
- **divergence seed**: `state/diverge_aliveness_2026-07-16/RESULT_8-families.md`
- **successor**: `H_002` — the 11-run twin (frozen / adaptive / scramble-refit × 3 seeds
  + 2 extra frozen seeds), 10M params, matched ~300M byte budget, ≤$25, GPU-hours.
  Pre-registered behind this card with thresholds frozen from its outputs.
- **harness**: `tool/anima_v3.py` · **fixtures**: `tool/test_anima_v3.py`
- **prior work (research pass, 2026-07)**: AdaptBPE (arXiv:2410.03258) · Teaching Old
  Tokenizers New Words (arXiv:2512.03989) · Getting the most out of your tokenizer
  (arXiv:2402.01035) · Zero-Shot Tokenizer Transfer (arXiv:2405.07883) · Byte Latent
  Transformer (arXiv:2412.09871) · gist-token compression study (arXiv:2412.17483)

## Verdict

_None yet — pre-register-frozen, still-to-run._

<!-- After running, paste the VERBATIM stdout in a fenced block + link result.json. -->
