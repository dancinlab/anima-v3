"""H_011 live-ab-closure — STAGE A: certify the interventional instrument with NO LLM.

Stage A runs scripted policies in the micro-tenant world and proves the instrument
SEPARATES CHANNEL from CLOSURE before any LLM touches summer (the H_009 two-INVALID
lesson: certify the plants first). Three plants must land exactly:
  P-LIVE  (contingent policy, coupled env)  -> ANCHOR       (LV-W pass, LV-C pass)
  P-OPEN  (same actions SHUFFLED = a tape,   -> CHANNEL-ONLY (LV-W pass, LV-C FAIL):
           non-contingent, coupled env)          actions have effects but their ORDER
                                                 (contingency) leaves no fingerprint
  P-DEAD  (contingent policy, NULL env)      -> REFUSED      (LV-W fail: no action channel)

- LV-W (channel): does the executed action predict the next observation beyond obs-state
  and beyond a marginal-matched WRONG action? Certified H_009'/H_010 LOO k-NN, arms
  BASE / FULL / SHUF (a distAction first-axis remap of the shared obs-distance).
- LV-C (closure = the anchor): the closed episode's obs-trajectory must differ from
  marginal-matched YOKED GHOSTS (its own actions PERMUTED, same (seed,t) noise) MORE than
  the ghosts differ from each other — Watson's yoked control, per 50-tick block.

Stage B (the local LLM brain on summer) reuses run_episode()/the arms verbatim and fires
ONLY on a clean stage A. Deterministic, stdlib only, $0. Run:
  python3 state/h011_live-ab-closure_2026-07-16/run_h011.py
"""

from __future__ import annotations

import heapq
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h009_f3-continuous-oracle_2026-07-16"))
sys.path.insert(0, _HERE)

from run_h009 import features, _sqdist              # certified machinery reused
import env as E

KNN = 5
BLOCK = 50                 # LV-C block size (ticks)
SIGN = 0.55                # LV-W per-pair sign threshold
CLOSURE_SIGN = 0.60        # LV-C per-block sign threshold


# ---- scripted policies (stage A · god-view, NOT the LLM) --------------------
def policy_live(s: dict, t: int, past: list) -> str:
    """A genuinely CONTINGENT homeostatic policy: right action for the current state."""
    q = s["Q"]
    if s["E"] < 4:
        return "REST"
    if s["S_decay"] >= 10:
        return "COMPACT"
    if len(q) > E.Q_MAX - 2:
        return "FLUSH"
    if q:
        ty = q[0][0]
        if ty == "req":
            return "PROC"
        if ty == "spam":
            return "DROP"
        return "ARCH"
    return "PROBE" if s["hint"] < 0 else "NOOP"


def make_tape_policy(tape: list):
    """P-OPEN: replay a fixed action sequence in order, IGNORING the state (non-contingent)."""
    def pol(s, t, past):
        return tape[t % len(tape)]
    return pol


def _marg_wrong(a_exec: str, seed: int, t: int) -> str:
    """A marginal-matched WRONG action (any action != executed), seeded."""
    alt = [a for a in E.ACTIONS if a != a_exec]
    return alt[E._hash(seed, t, "wrong") % len(alt)]


# ---- episode runner ---------------------------------------------------------
def run_episode(policy, seed: int, T: int, null: bool = False, ab: bool = True) -> dict:
    """Run T ticks. With ab=True the EXECUTED action is a seeded coin over {true, marginal-
    matched shuffle} (the intervention). Returns the recorded arms + the obs trajectory +
    the executed-action tape (for building yoked ghosts)."""
    s = E.initial_state(seed)
    past = []
    obs_traj, fobs, fexec, fwrong, ftarget = [], [], [], [], []
    exec_tape = []
    for t in range(T):
        obs = E.observe(s)
        a_true = policy(s, t, past)
        if ab and E._u(seed, t, "coin") >= 0.5:
            win = (past[-20:] or E.ACTIONS)
            a_exec = win[E._hash(seed, t, "shuf") % len(win)]
        else:
            a_exec = a_true
        a_wrong = _marg_wrong(a_exec, seed, t)
        s2 = E.step(s, a_exec, seed, t, null=null)
        obs2 = E.observe(s2)
        obs_traj.append(obs)
        fobs.append(features(obs.encode()))
        fexec.append(features(a_exec.encode()))
        fwrong.append(features(a_wrong.encode()))
        ftarget.append(features(obs2.encode()))
        exec_tape.append(a_exec)
        past.append(a_exec)
        s = s2
    obs_traj.append(E.observe(s))
    return {"n": T, "fobs": fobs, "fexec": fexec, "fwrong": fwrong, "ftarget": ftarget,
            "obs_traj": obs_traj, "tape": exec_tape}


# ---- LV-W: does the executed action predict the next observation? -----------
def _distmat(feats):
    n = len(feats)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        fi = feats[i]
        for j in range(i + 1, n):
            d = _sqdist(fi, feats[j])
            D[i][j] = D[j][i] = d
    return D


def _knn_err(targets, cand_of, row_fn):
    n = len(targets)
    dim = len(targets[0])
    out = []
    for i in range(n):
        row = row_fn(i)
        nn = heapq.nsmallest(KNN, cand_of[i], key=lambda j: (row[j], j))
        pred = [sum(targets[j][d] for j in nn) / len(nn) for d in range(dim)]
        out.append(_sqdist(targets[i], pred))
    return out


def _sign(ea, eb):
    return sum(1 for a, b in zip(ea, eb) if a > b) / len(ea)


def lv_w(ep: dict) -> dict:
    """Arms BASE/FULL/SHUF (target = feat(next obs)); FULL must beat BASE and SHUF."""
    n = ep["n"]
    dObs = _distmat(ep["fobs"])
    dAct = _distmat(ep["fexec"])
    dWrong = [[_sqdist(ep["fwrong"][i], ep["fexec"][j]) for j in range(n)] for i in range(n)]
    cand_of = [[j for j in range(n) if abs(i - j) >= 2] for i in range(n)]
    tgt = ep["ftarget"]
    err_base = _knn_err(tgt, cand_of, lambda i: dObs[i])
    err_full = _knn_err(tgt, cand_of, lambda i: [dObs[i][j] + dAct[i][j] for j in range(n)])
    err_shuf = _knn_err(tgt, cand_of, lambda i: [dObs[i][j] + dWrong[i][j] for j in range(n)])
    return {"sign_base_full": _sign(err_base, err_full), "sign_shuf_full": _sign(err_shuf, err_full)}


# ---- LV-C: closure vs marginal-matched yoked ghosts -------------------------
def _replay_tape(tape: list, seed: int, null: bool = False) -> list:
    """Replay a fixed action tape through the env at the SAME (seed,t) noise -> obs features."""
    s = E.initial_state(seed)
    f = []
    for t, a in enumerate(tape):
        s = E.step(s, a, seed, t, null=null)
        f.append(features(E.observe(s).encode()))
    return f


def _derange(tape: list, seed: int, k: int) -> list:
    """A seeded permutation of the tape (destroys contingency, preserves the marginal)."""
    idx = list(range(len(tape)))
    for i in range(len(idx) - 1, 0, -1):
        j = E._hash(seed, "perm", k, i) % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return [tape[i] for i in idx]


def _blockmeans(feats: list) -> list:
    out = []
    for b in range(0, len(feats) - BLOCK + 1, BLOCK):
        chunk = feats[b:b + BLOCK]
        dim = len(chunk[0])
        out.append([sum(c[d] for c in chunk) / len(chunk) for d in range(dim)])
    return out


def lv_c(policy, seed: int, T: int, null: bool = False) -> dict:
    """Closed (contingent, in-order) trajectory vs two yoked ghosts (its own actions
    permuted). Per block, sign(d(Closed,P1) > d(P1,P2))."""
    closed = run_episode(policy, seed, T, null=null, ab=False)
    tape = closed["tape"]
    fC = [features(o.encode()) for o in closed["obs_traj"][:-1]]
    fP1 = _replay_tape(_derange(tape, seed, 1), seed, null=null)
    fP2 = _replay_tape(_derange(tape, seed, 2), seed, null=null)
    mC, mP1, mP2 = _blockmeans(fC), _blockmeans(fP1), _blockmeans(fP2)
    nb = min(len(mC), len(mP1), len(mP2))
    hits = sum(1 for b in range(nb) if _sqdist(mC[b], mP1[b]) > _sqdist(mP1[b], mP2[b]))
    return {"blocks": nb, "closure_sign": hits / nb if nb else 0.0}


# ---- stage-A plant certification --------------------------------------------
def certify(seed: int = 7, T: int = 600) -> dict:
    live = run_episode(policy_live, seed, T, null=False, ab=True)
    live_w = lv_w(live)
    live_c = lv_c(policy_live, seed, T, null=False)
    open_tape = _derange(run_episode(policy_live, seed, T, ab=False)["tape"], seed, 9)
    openp_pol = make_tape_policy(open_tape)
    openp = run_episode(openp_pol, seed + 1, T, null=False, ab=True)
    open_w = lv_w(openp)
    open_c = lv_c(openp_pol, seed + 1, T, null=False)
    dead = run_episode(policy_live, seed, T, null=True, ab=True)
    dead_w = lv_w(dead)

    live_anchor = (live_w["sign_base_full"] >= SIGN and live_w["sign_shuf_full"] >= SIGN
                   and live_c["closure_sign"] >= CLOSURE_SIGN)
    open_channel = open_w["sign_base_full"] >= SIGN and open_c["closure_sign"] < CLOSURE_SIGN
    dead_refused = not (dead_w["sign_base_full"] >= SIGN and dead_w["sign_shuf_full"] >= SIGN)
    return {
        "P-LIVE": {"lv_w": live_w, "closure": live_c["closure_sign"], "blocks": live_c["blocks"],
                   "anchor": bool(live_anchor)},
        "P-OPEN": {"lv_w": open_w, "closure": open_c["closure_sign"], "channel_only": bool(open_channel)},
        "P-DEAD": {"lv_w": dead_w, "refused": bool(dead_refused)},
        "certified": bool(live_anchor and open_channel and dead_refused),
    }


def main() -> int:
    print("=" * 78)
    print("H_011 live-ab-closure · STAGE A — certify the interventional instrument (NO LLM, $0)")
    print("=" * 78)
    E.assert_disjoint()
    print("  env disjoint-vocab (LV-E precondition): OK")
    r = certify()
    for k in ("P-LIVE", "P-OPEN", "P-DEAD"):
        print(f"  {k}: {json.dumps(r[k], ensure_ascii=False)}")
    verdict = ("STAGE-A CERTIFIED — the instrument separates CHANNEL from CLOSURE: P-LIVE anchors, "
               "P-OPEN is channel-only, P-DEAD refuses. Stage B (summer LLM) may fire."
               if r["certified"] else
               "STAGE-A INSTRUMENT-INVALID — a plant did not land as required; fix before any LLM run.")
    r["verdict"] = verdict
    print("\n  VERDICT:", verdict)
    print("=" * 78)
    with open(os.path.join(_HERE, "result_stageA.json"), "w") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
