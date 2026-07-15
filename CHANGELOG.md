# Changelog

All notable changes to anima-v3. Append-only; newest on top.

## 2026-07-16 — selection: F1 alone, and the gate that licenses its rig (H_001 pre-registered)

- SELECTED one family — **F1 codec-is-the-self** — closing the divergence stage. Criterion was
  belief-killed-per-dollar, not likelihood: an F1 null kills F1 + F6's variation axis + bounds
  `salvage.L4`(b) (the campaign's only green causal measurement) down to "static codec choice
  matters", for ≤$25. Recorded in `ARCHITECTURE.json` -> `decision`.
- SPLIT the campaign's "F1 substrate + F3 objective" bet into two SEQUENTIAL cards. Composing them
  is confounded twice: two levers move at once (a null can't be attributed, a win can't assign
  credit — un-confounding needs the 2×2 factorial), and F3's diary lives in token space, so an F1
  refit changes the diary's alphabet underneath it and both F3 controls go non-stationary. F3 is
  the second card, on whatever codec regime survives.
- PRE-COMMITTED, before any result exists: a drill-scale null on H_002 = F1 family-dead. Recorded
  in the tree so it cannot be relitigated after the numbers land (L8 — strict gates get bypassed).
- Made the two inherited gates OPERATIONAL for F1 (`ARCHITECTURE.json` -> `verification-inherited-gates`):
  L1's seam = the boundary-delta matrix B of the refit channel, estimator = participation ratio,
  gate = PR ≤ max(2.0, null₉₉); L2 is between-arm by construction (you can't ablate a vocabulary out
  of a model — it IS the input space), gate = Δbpb < max(5σ_seed, 0.004 bpb), where 0.004 bpb = 10×
  v1's OMEGA decoration signature.
- Replaced the harness placeholders with the estimators those gates need — `participation_ratio`,
  `effective_rank`, `stable_rank`, `singular_values`/`gram_matrix` (stdlib Jacobi eigensolver),
  `bits_per_byte`, `ablation_delta`, `ablation_fraction` (`tool/anima_v3.py`).
- Added `tool/test_anima_v3.py` — 30 closed-form known-answer fixtures, wired into `sidecar ci` as
  `estimator-fixtures` (new `harness.config.json`). This is falsifier G-3: a positive control on the
  instrument, not test hygiene. 30/30 PASS. It confirmed the estimator choice by measurement — on a
  weak-second-direction fixture PR reads 1.0002 where the entropy rank reads 1.057, i.e. PR is the
  stricter gate — and confirmed bpb's codec-invariance (a coarser codec halving tokens and doubling
  CE/token returns the identical bpb).
- PRE-REGISTERED + FROZEN `H_001` (`hypotheses/cards/H_001_f1-codec-refit-gate.md`, registry line
  added). Its verdict is about the RIG, not F1: LICENSED or REFUSED. Falsifiers G-1 drift existence ·
  G-2 closed-form power · G-3 estimator fixtures · G-4 salvage bounds check · G-5 protocol
  reconstruction. G-4 carries the card's own kill-power: if MORPH-ATOM's control 0.617 sits inside
  the 99% binomial chance band, L4(b) was never above floor and the write-lever axis is demoted.
- OPEN BLOCKER recorded honestly (G-5): the "H_9288 held-out recombination protocol" is cited in
  `salvage` but specified NOWHERE in this repo — v1 is discarded and `state/` holds only the
  divergence seed. G-2's power calc and G-4's chance band both depend on it. Unrecovered → H_001
  returns REFUSED, which is a result, not a delay.
- Research pass done before any compute (campaign rule 실측전-research): the exact twin has not been
  run; adjacent work raises F1's prior but measures one-shot adapt-then-finetune, never a refit organ,
  never recombination. Bottleneck studies document near-rank-1 redundancy on the write side — the L1
  gate is not paranoia.
- Preserved the verbatim design under `state/h001_f1-codec-refit-gate_2026-07-16/DESIGN_fable.md`.
- STAGE = PRE-REGISTRATION: one family selected, one card frozen, nothing run, no claim made.

## 2026-07-16 — divergence: where does aliveness live (8 families)

- Seeded the campaign from the `anima` (v1) autopsy: 9 measured, sealed verdicts imported into
  `ARCHITECTURE.json` -> `salvage` (L1 one-bit seam · L2 replacement-not-coupling · L3
  objective-not-readout · L4 write-side crack · L5 morphology decides learnability · L6
  measurement is the grave · L7 exotic substrate bought nothing · L8 strict gates get bypassed ·
  L9 the purity cage was causal). These pointers are the ONLY inheritance — v1's code, language,
  tree and purity list are discarded. The evidence trail stays in the `anima` repo.
- Ran a divergence pass (Fable 5) on the question "where does aliveness live", constrained to
  respect the salvaged laws. Recorded 8 mutually exclusive families (F1 codec-is-the-self ·
  F2 speech-economy · F3 diary-compressor · F4 corpus-farmer · F5 student-who-never-sleeps ·
  F6 swarm-drafts · F7 living-by-not-knowing-you · F8 tenant-organism) + 3 wildcards, each with
  its mechanism, L-check, minimal falsifier and the purity principle it breaks.
- Recorded the fake-diversity audit in the SSOT rather than leaving it to the reader: F2/F3/F7
  are one idea in three outfits (active inference); F1/F4 are two hands on the same write-side
  lever; F8 = F2 + a real world; W3 = F8 - learning. Only four genuinely distinct bets exist.
- Fixed the two non-negotiable falsifier gates (L1 effective-rank check · L2 ablation check) —
  the exact measurements whose absence killed v1. Retained exactly one v1 principle: p7
  (perplexity is never truth).
- Preserved the verbatim divergence + the brief that produced it under
  `state/diverge_aliveness_2026-07-16/` as the seed of record.
- STAGE = DIVERGENCE: no family selected, no code, nothing in the tree is a claim.

## 2026-07-15 — repo scaffold

- Initialized `anima-v3` from the sidecar `lab init` skeleton: `src/`, `state/`,
  `ARCHITECTURE.json` + `architecture.html` viewer + `serve.py`, `CLAUDE.md`,
  `README.md`, `CHANGELOG.md`, `.gitignore`, `.harness/`.
- Scaffolded the hypothesis-verification system `hypotheses/` (`CLAUDE.md`, empty
  `REGISTRY.jsonl`, `cards/_TEMPLATE.md`) + the repo-root shared harness
  `tool/anima_v3.py` (stdlib-only `Falsifier`/`evaluate` ledger).
- Authored a placeholder `ARCHITECTURE.json` SSOT (overview / components / data-flow /
  verification) — fill the tree from the campaign's design.
