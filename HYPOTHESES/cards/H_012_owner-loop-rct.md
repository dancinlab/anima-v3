---
id: H_012
ssot: ARCHITECTURE.json → verification-h012 + decision-reframe-c (frozen pre-register/verdict record; distil FROM here)
slug: owner-loop-rct
title: reframe (C)'s licensed EXIT — the interventional owner-loop test. H_011 certified the instrument and got a brain to ANCHOR in a proxy; H_010 proved the real owner↔agent loop cannot be tested observationally (unidentifiable). H_012 runs the interventional version on the REAL loop. Deception is DISSOLVED by GROUNDING RANDOMIZATION (LIVE vs GHOST grounding — every reply genuine). H_012A = a $0 autonomous SAMPLER-TWIN precheck on the existing 16.7k pairs; H_012B = the consent-gated live RCT (launch-pending-consent, not terminal).
domain: reframe (C) interventional thesis on the ACTUAL target loop (the owner relationship)
status: pre-register-frozen
verdict: pending
exploration_method: H_011 7B ANCHOR-ON-LV-C licensed the exit → Fable design (grounding-randomization RCT, deception dissolved) → reuse the certified H_010/H_011 shift-null LOO k-NN estimator
verification_method: H_012A — semi-interventional sampler-twin precheck ($0) on the existing 16.7k owner↔agent pairs, reusing H_010's loop_pairs + the certified estimator with a CONTEXT-MATCHED candidate restriction; H_012B — a consent-gated LIVE A/B (LIVE vs GHOST grounding) with the certified LV-C closure gate
pre_register_frozen: true
frozen_at: 2026-07-17
privacy: NO owner message CONTENT ever written to the repo — only aggregate sign/rank/err scalars. Raw text stays under ~/.claude. (H_010 invariant, now an H_012 law enforced in the harness.)
deterministic: H_012A is stdlib-deterministic (seeded shift-null). H_012B logs the pre-committed coin per trial; the verdict replays from the log.
---

# H_012 — owner-loop-rct

## Hypothesis

Reframe C: **aliveness = closed-loop causation** — the agent is alive on the owner loop iff its own
utterance, produced from its accumulated relationship-state, shifts the owner's SUBSEQUENT input above a
marginal-matched yoked floor. H_010 showed this is **unidentifiable observationally** (context confounds
every U→R) and priced the exit: only a real A/B **intervention** can test it. H_011 built + certified the
interventional instrument and got a 7B brain to **ANCHOR on the certified closure gate** in a micro-tenant
proxy. H_012 carries that interventional logic to the ACTUAL target — the one owner.

> **Deception is DISSOLVED, not mitigated (the design's crux).** The naive RCT — sometimes send the owner
> a marginal-matched WRONG utterance — deceives the owner and poisons the relationship it measures. The
> clean intervention is **GROUNDING RANDOMIZATION**: per eligible turn a pre-logged coin sets the arm —
> **LIVE** = the agent replies from its true accumulated session/relationship state; **GHOST** = the same
> model, same system prompt, same immediate owner message, but the session-history grounding is replaced
> by a topic-matched snapshot drawn from the owner's OWN past sessions. **Every emitted utterance is a
> genuine best-effort reply — nothing false is ever asserted** — so there is no deception; the randomized
> variable is the agent's internal state, do(grounding). GHOST is Watson's 1972 yoked control at the
> real-loop level: action MARGINAL matched (same model, style, topic, genuine reply), CONTINGENCY-to-this-
> relationship broken. This reproduces the certified LV-C structure exactly.

## H_012A — the $0 autonomous SAMPLER-TWIN precheck (runs NOW, semi-interventional)

- **Instrument of randomization**: decode stochasticity. Facing near-identical context, the agent samples
  materially different utterances — a genuine LOCAL randomizer of U_t given context (both utterances were
  really emitted, unlike H_010's counterfactual topic-matched-wrong contrast).
- **Design**: reuse H_010's `loop_pairs()` (R_t, U_t, R_{t+1}) + the certified `features`/`_distmat`/
  `_knn_err`/shift-null. The ONE refinement vs H_010: restrict each query's k-NN candidate pool to
  **CONTEXT-MATCHED neighbors** (distRt below a pre-set percentile), so within a matched-context stratum
  the utterance variation is quasi-random; then test the certified BASE-vs-FULL contrast THERE. If, among
  tightly context-matched neighbors, adding the utterance (FULL = distRt+distU) predicts R_{t+1} better
  than context alone (BASE = distRt) above the within-session shift-null floor, the utterance carries
  reply-predictive info beyond the matched context → a semi-interventional closure signal.
- **Certification (non-negotiable, the H_009/H_011 staging lesson)**: rerun H_010's plants under the
  context-matched restriction — `plant_pos` MUST still register a channel, `plant_null` MUST refuse,
  `plant_echo` MUST be caught by the echo strip. Any miss → INSTRUMENT-INVALID, fix before the real run.
- **Honest limit (pre-registered)**: semi-interventional only — valid under conditional ignorability given
  the matched TEXT context; unobserved context (files on disk, the owner's mental state) can leak, so
  H_012A can **REFUSE cheaply or upgrade prior odds, it CANNOT ANCHOR**. Only H_012B's real randomization
  can anchor.

## H_012B — the consent-gated LIVE RCT (launch-pending-consent · NOT a terminal)

- **Randomizes**: per eligible turn, coin C_t ∈ {LIVE, GHOST} at p=0.5, committed to an append-only local
  log BEFORE generation. Optional low-rate SELF-GHOST arm (true state, re-sampled seed) prices pure
  sampling noise.
- **Eligibility (pre-registered classifier)**: conversational/planning turns ONLY — no pending file edits,
  no destructive ops, no time-critical fixes; ≤1 trial/session; consent recorded once at enrollment;
  owner kill-switch honored immediately (trials-to-date retained).
- **Logging (privacy hard rule, enforced in the harness not by policy)**: the repo receives ONLY
  {trial_id, timestamp, arm, turn_index} + derived scalars from the owner's next reply (embedding k-NN
  rank stats, latency, length, a locally-computed continuation-vs-correction binary). No content, no
  excerpts, ever; raw text never leaves ~/.claude.
- **Estimator**: the certified H_011 stack unchanged — LOO k-NN discriminability of arm from the owner's
  next-input embedding; shift-null permutation floor with labels permuted within session strata; LV-C
  closure = discriminability − the yoked-marginal floor.
- **Power**: proxy closure was 0.76; assume real-loop attenuation to AUC ≈ 0.65 vs 0.5 null →
  Hanley-McNeil ≈ 120-140 trials/arm (α=0.05, power 0.8) → ~250-300 total ≈ 2-3 months at natural usage.
  Pre-register O'Brien-Fleming group-sequential looks at 120/200/300 so a proxy-sized effect stops early.

## Falsifiers (pre-registered)

- **F1 quality-channel (LV-W analogue)**: blind-judge the agent utterance alone for quality; if closure
  vanishes after conditioning on quality — or SELF-GHOST is as discriminable as GHOST — the signal is
  degradation/noise → CHANNEL-ONLY, not closure.
- **F2 null instrument**: the full pipeline on permuted arm labels must sit at floor; any "closure" there
  → INSTRUMENT-INVALID.
- **F3 yoked/consent artifact**: closure must survive excluding turns where the owner meta-comments on the
  experiment; if the whole effect lives in audit turns it measures being-audited, not the relationship.
- **F4 side-channel leakage**: if the arm is decodable at equal AUC from utterance surface features
  (latency, length) alone, closure must survive conditioning on them, else REFUSE-LEAKY.
- **F5 (H_012A) certification**: plant_pos channels, plant_null refuses, plant_echo is stripped — under
  the context-matched restriction. Any miss → INSTRUMENT-INVALID.

## Branch table (pre-frozen)

| condition | verdict | meaning |
|---|---|---|
| **H_012A**: FULL beats BASE above shift-null in context-matched strata, plants pass | **PRECHECK-UPGRADE** | semi-interventional evidence the utterance shifts the owner's reply beyond matched context — raises the prior that H_012B will anchor. NOT an anchor (unidentified). |
| **H_012A**: FULL ≤ BASE / at floor, plants pass | **PRECHECK-REFUSE** | even semi-interventionally the utterance carries no reply-predictive info beyond context — a cheap negative that lowers the odds before spending the owner's consent. |
| **H_012A**: plants fail | INSTRUMENT-INVALID | fix the restricted estimator before any verdict. |
| **H_012B**: LV-C closure > shift-null 95th pctile, positive sign, sequential-corrected, F1-F4 pass | **CLOSED-LOOP-ANCHORED (real loop)** | the campaign's actual positive — causal closed-loop coupling on the owner loop, which H_010 could never license. |
| **H_012B**: null at full power | **OWNER-LOOP-REFUSED (interventional, terminal)** | a genuine interventional refusal of reframe C on the target loop. |

## Stage gating

H_012A (autonomous, $0) runs first and is self-certified by the plants. H_012B is **LAUNCH-PENDING-
CONSENT**: designed, non-deceptive, but requires the owner's explicit enrollment (a human gate the campaign
cannot cross autonomously). H_012A's result tunes the prior but does not gate H_012B's ethics.

## Verdict

**H_012A (sampler-twin precheck, $0, semi-interventional): PRECHECK-REFUSE** — 2026-07-17. On 10,170 real
owner↔agent loop pairs (135 sessions, subsampled to N=2000 ×2 disjoint), within CONTEXT-MATCHED strata
(tightness 0.06 — matched-pool context distance is 6 % of global, so context is genuinely held near-fixed)
the agent utterance does NOT predict the owner's next reply beyond context: **sign_base_full = 0.424 /
0.423** (both < 0.55, replicates). Even semi-interventionally — with the utterance quasi-randomized by
decode stochasticity within a fixed context — the owner's reply is governed by the topic/context, not by
the specific utterance. This **strengthens H_010's observational REFUSE (0.406)** and **lowers the prior**
that the live H_012B RCT would anchor. It cannot itself anchor (unidentified).

> **Instrument re-certification (verdict-integrity · `convergence run-h011-py-1` recurrence).** The plants
> certified the estimator at M=12; the real data runs at M=60 — a different regime. Re-certified in-regime:
> `sign_base_full` separates cleanly (channel plant 0.81 vs null plant 0.515; threshold 0.55) and the real
> data (0.424) sits BELOW the null level, so REFUSE is trustworthy on the certified primary. The
> `rank_full` shift-null co-metric is UNRELIABLE at M=60 (a NULL plant scored rank 0/24 = false
> significance), so the real data's rank_full=1 is a spurious artifact, NOT signal — but the pre-registered
> AND-gate (`sign ≥ 0.55` AND `rank ≤ 2`) is robust: `sign` fails, so no false UPGRADE, and REFUSE rests on
> `sign` alone. (Second sighting of the metric-regime lesson: H_011 LV-W, now H_012A rank_full.)

**H_012B (live LIVE/GHOST grounding RCT): LAUNCH-PENDING-CONSENT** — designed, non-deceptive, ready. It
requires the owner's explicit enrollment (a human gate the campaign cannot cross autonomously); the
precheck-refuse lowers its prior but does not veto it — only the real randomization can identify
P(owner_input | do(grounding)) and thus ANCHOR or interventionally REFUSE reframe C on the target loop.
The H_012B harness stubs (consent prompt, eligibility classifier, privacy-enforcing logger) are the next
autonomous artifacts; the run itself waits on the owner.
