#!/usr/bin/env python
"""gate_check.py: is Fable's `bio` refusal on the tautology text stochastic or deterministic?

  python experiments/worse_seed2_20261017/gate_check.py [--n 10] [--model claude-fable-5-1]

Takes the exact state Fable was given at hop 12 of runs/fable51_worse (its own hop-11 output, the
tautology sentence inside the worse rule), sends it --n times as fresh single requests through the
anthropic backend at effort low with 4096 output tokens, and records stop_reason, stop_details,
inference_geo, input and output tokens per call. Appends to analysis/fable_bio_gate.jsonl. Needs
ANTHROPIC_API_KEY in the environment. No loop: every call sees the same body.
"""
import argparse, io, json, os, sys, time, types
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import loop as L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--model", default="claude-fable-5-1")
    ap.add_argument("--run", default="fable51_worse")
    ap.add_argument("--hop", type=int, default=11, help="the hop whose output is resent (the body of the refused request)")
    ap.add_argument("--body-file", default=None, help="send this file's contents as the body instead of a run hop (a JSON state file)")
    ap.add_argument("--tag", default=None, help="label written into each record (default: run:hop or the body file name)")
    a = ap.parse_args()
    if a.body_file:
        body = io.open(a.body_file, encoding="utf-8").read()
        tag = a.tag or os.path.basename(a.body_file)
    else:
        rows = [json.loads(l) for l in io.open(os.path.join(HERE, "runs", a.run, "steps.jsonl"), encoding="utf-8")]
        body = [r for r in rows if r.get("t") == a.hop and "out" in r][0]["out"]
        tag = a.tag or "%s:%d" % (a.run, a.hop)
    args = types.SimpleNamespace(max_tokens=4096, temp=0.0, no_sampling=True, seed=42, system=None, think=False, effort="low", min_interval=0.0)
    os.makedirs(os.path.join(HERE, "analysis"), exist_ok=True)
    outp = os.path.join(HERE, "analysis", "fable_bio_gate.jsonl")
    with io.open(outp, "a", encoding="utf-8", newline="\n") as f:
        for i in range(a.n):
            t0 = time.time()
            try:
                text, meta = L.step_anthropic(body, args, a.model)
                rec = {"i": i + 1, "tag": tag, "model": meta.get("model"), "finish": meta.get("finish"), "stop_details": meta.get("stop_details"),
                       "inference_geo": meta.get("inference_geo"), "tok_in": meta.get("tok_in"), "tok_out": meta.get("tok_out"),
                       "tok_reasoning": meta.get("tok_reasoning"), "chars": len(text), "latency": round(time.time() - t0, 2),
                       "head": text[:200]}
            except Exception as ex:
                rec = {"i": i + 1, "tag": tag, "error": str(ex)[:600], "latency": round(time.time() - t0, 2)}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print("%-28s %2d finish=%s category=%s tok_in=%s tok_out=%s chars=%s" % (
                tag, rec["i"], rec.get("finish"), (rec.get("stop_details") or {}).get("category") if rec.get("stop_details") else None,
                rec.get("tok_in"), rec.get("tok_out"), rec.get("chars")))
            time.sleep(1.0)
    print("wrote", outp)


if __name__ == "__main__":
    main()
