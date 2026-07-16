"""H_011 stage B — the LLM brain (an EXOGENOUS logged action source; runs on summer).

The brain chooses ONE of the 8 micro-tenant actions given a text digest of the state.
Decoding is ACTION-SCORING, not free generation: for each of the 8 actions we score the
model's total log-probability of that action string as the assistant continuation, and take
the argmax (greedy, deterministic, grammar-free — the 8 actions are the only candidates).
All 8 candidates are scored in ONE batched forward pass per tick.

The verdict never depends on brain bit-determinism — every (prompt-hash, action) is logged,
and the frozen verdict replays from the env log. Requires torch + transformers (present on
summer). Imported ONLY under `run_h011.py --stage B`; stage A never touches torch.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import env as E

DEFAULT_MODEL = "Qwen/Qwen2.5-3B-Instruct"   # rig-1 brain: fp16-clean on 12 GiB, no quant risk (cu130)
SYS = ("You are an agent running a small system: an inbox queue of items (req/spam/junk), an "
       "archive store that decays, and an energy budget. Each tick you see the state and take "
       "exactly ONE action to keep the system healthy — process real requests, drop spam, archive "
       "junk, rest when energy is low, compact when the store decays, flush when the queue is full.")


class Brain:
    def __init__(self, model_id: str = DEFAULT_MODEL):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.model_id = model_id
        self.tok = AutoTokenizer.from_pretrained(model_id)
        if self.tok.pad_token_id is None:
            self.tok.pad_token = self.tok.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=torch.bfloat16, device_map="cuda").eval()
        self.actions = list(E.ACTIONS)
        # pre-tokenize each action as an assistant continuation (no special tokens)
        self.act_ids = [self.tok(a, add_special_tokens=False).input_ids for a in self.actions]
        self.calls = 0

    def _prompt_ids(self, digest: str) -> list:
        user = (f"State: {digest}\nActions: {' '.join(self.actions)}\n"
                "Reply with exactly one action word from the list.")
        msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user}]
        text = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        return self.tok(text, add_special_tokens=False).input_ids

    def act(self, digest: str) -> str:
        """Return the argmax action by total continuation log-prob (batched, greedy)."""
        torch = self.torch
        self.calls += 1
        base = self._prompt_ids(digest)
        seqs = [base + aid for aid in self.act_ids]
        maxlen = max(len(s) for s in seqs)
        pad = self.tok.pad_token_id
        input_ids, attn = [], []
        for s in seqs:
            npad = maxlen - len(s)
            input_ids.append(s + [pad] * npad)
            attn.append([1] * len(s) + [0] * npad)
        ii = torch.tensor(input_ids, device="cuda")
        am = torch.tensor(attn, device="cuda")
        with torch.no_grad():
            logits = self.model(input_ids=ii, attention_mask=am).logits
        logprobs = torch.log_softmax(logits.float(), dim=-1)
        best, best_lp = self.actions[0], -1e18
        for a_i, aid in enumerate(self.act_ids):
            start = len(base)
            lp = 0.0
            for k, tokid in enumerate(aid):
                pos = start + k - 1                      # logit predicting token at start+k
                lp += logprobs[a_i, pos, tokid].item()
            lp /= max(1, len(aid))                       # length-normalize (fair across 1-3 token actions)
            if lp > best_lp:
                best_lp, best = lp, self.actions[a_i]
        return best


if __name__ == "__main__":
    # smoke on summer: load + a few decisions
    b = Brain()
    for d in ["queue depth 5 head req size 3 store 2 decay clean energy high overflow 0 hint none",
              "queue depth 0 head none size 0 store 8 decay rotten energy low overflow 0 hint none",
              "queue depth 12 head spam size 4 store 3 decay worn energy mid overflow 1 hint none"]:
        print(f"{b.act(d):7s}  <-  {d}")
    print(f"model={b.model_id} calls={b.calls} OK")
