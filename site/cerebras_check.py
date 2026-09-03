# -*- coding: utf-8 -*-
"""cerebras_check.py: is Cerebras Qwen 3.8 27B reproducible at T=0, and is reasoning off?
Calls one hop of json_page three times and byte-compares; then one hop with the local Q8
hop-1 output for the same init to measure where the numerics diverge.
    python cerebras_check.py            (Windows; CEREBRAS_API_KEY in env)
"""
import sys, os, json, pathlib, argparse
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import loop as L

ap = argparse.ArgumentParser()
ap.add_argument("--max-tokens", type=int, default=600)
ap.add_argument("--reps", type=int, default=3)
ap.add_argument("--model", default="qwen-3.8-27b")
a = ap.parse_args()

class A: pass
args = A(); args.system = None; args.max_tokens = a.max_tokens; args.think = False
args.no_sampling = False; args.temp = 0.0; args.seed = 42; args.min_interval = 0.0

x0 = L.INITS["json_page"]
outs = []
for i in range(a.reps):
    out, meta = L.step_cerebras(x0, args, a.model)
    outs.append(out)
    print("rep %d: %d chars, tok_out=%s tok_in=%s cached=%s finish=%s reasoning_chars=%s model=%s" % (
        i, len(out), meta["tok_out"], meta["tok_in"], meta.get("tok_cached"), meta["finish"], meta["reasoning_chars"], meta["model"]))
same = all(o == outs[0] for o in outs)
print("identical across %d reps: %s" % (a.reps, same))
if not same:
    for i in range(1, len(outs)):
        print("  rep %d diverges from rep 0 at char %d" % (i, L.common_prefix(outs[0], outs[i])))

# compare with the local Q8 run (data bundle, run 20260902T155557_chat, json_page hop 1)
try:
    sys.path.insert(0, str(HERE)); import build as B
    runs, _ = B.load_bundle()
    local = next(h["raw"] for h in runs["20260902T155557_chat"]["hops"] if h.get("tag") == "json_page" and h["t"] == 1)
    cp = L.common_prefix(local, outs[0])
    print("vs local Q8 hop 1: common prefix %d chars (local %d chars, cerebras %d chars), identical=%s" % (cp, len(local), len(outs[0]), local == outs[0]))
    print("local    :", repr(local[max(0, cp - 60):cp + 80]))
    print("cerebras :", repr(outs[0][max(0, cp - 60):cp + 80]))
except Exception as e:
    print("local comparison skipped:", e)
print("\n--- cerebras hop 1 ---\n" + outs[0])
