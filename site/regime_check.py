# -*- coding: utf-8 -*-
"""regime_check.py: which sampling regime reproduces the original runs/ hop-1 outputs?

Sends the json_page X_0 to the local llama-server three ways and compares the full output with
the recorded hop 1 of runs 20260902T155557_chat, 20260902T160344_chat (both slots), and the
json_worse hop 1 of 20260902T174258_chat:
  A. temperature 0, top_k 1, seed 42            (what the current harness sends)
  B. no temperature key, seed 42                (server defaults: serve-qwen.ps1 sets --temp 1.0 --top-k 20)
  C. no temperature key, seed 7
  D. temperature 1.0, top_k 20, seed 42         (explicit server defaults)
Run on the Windows side: python C:\\ai\\loop\\site\\regime_check.py
"""
import json, urllib.request, sys, os
LOOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LOOP)
import loop as L

def ask(x0, body_extra, max_tokens):
    body = {"model": "qwen3.8-27b", "messages": [{"role": "user", "content": x0}], "top_p": 1.0, "min_p": 0.0,
            "max_tokens": max_tokens, "chat_template_kwargs": {"enable_thinking": False}}
    body.update(body_extra)
    req = urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        j = json.loads(r.read().decode())
    return j["choices"][0]["message"]["content"]

def rec(run, tag, t):
    for line in open(os.path.join(LOOP, "runs", run, "steps.jsonl"), encoding="utf-8"):
        j = json.loads(line)
        if j.get("tag") == tag and j.get("t") == t and "out" in j: return j["out"]

def common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y: break
        n += 1
    return n

def main():
    cases = [("json_page", 600, [("20260902T155557_chat", "json_page"), ("20260902T160344_chat", "json_page"), ("20260902T160344_chat", "json_page~r")]),
             ("json_worse", 800, [("20260902T174258_chat", "json_worse")])]
    regimes = [("A: T=0 top_k=1 seed 42", {"temperature": 0.0, "top_k": 1, "seed": 42}),
               ("B: no temp key, seed 42", {"seed": 42}),
               ("C: no temp key, seed 7", {"seed": 7}),
               ("D: T=1.0 top_k=20 seed 42", {"temperature": 1.0, "top_k": 20, "seed": 42})]
    for init, mt, targets in cases:
        x0 = L.INITS[init]
        recs = [(r + "/" + tg, rec(r, tg, 1)) for r, tg in targets]
        print("== %s (max_tokens %d)" % (init, mt))
        outs = {}
        for name, extra in regimes:
            out = ask(x0, extra, mt); outs[name] = out
            for label, old in recs:
                print("   %-28s vs %-36s identical=%s common prefix=%d/%d" % (name, label, out == old, common_prefix(out, old), len(old)))
        print("   B == C (does seed matter without temp key): %s" % (outs["B: no temp key, seed 42"] == outs["C: no temp key, seed 7"]))
        print("   A == B: %s   A == D: %s" % (outs["A: T=0 top_k=1 seed 42"] == outs["B: no temp key, seed 42"], outs["A: T=0 top_k=1 seed 42"] == outs["D: T=1.0 top_k=20 seed 42"]))

if __name__ == "__main__":
    main()
