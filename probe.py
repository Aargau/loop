"""probe.py -- send the same prompt N times to a backend and count distinct outputs.
Tells you whether "sampling" is real (many distinct outputs, early divergence) or deterministic
given context (one output, or a few differing only by batch noise). Uses loop.py's backends and
env-var keys.

  python probe.py --backend anthropic --model claude-sonnet-5 --no-sampling --n 10
  python probe.py --backend anthropic --model claude-sonnet-4-6 --temp 1.0 --n 10
  python probe.py --backend llama --model qwen3.8-27b --temp 1.0 --n 10
"""
import argparse, collections, hashlib, types, sys
import loop

ap = argparse.ArgumentParser()
ap.add_argument("--backend", choices=["llama", "anthropic", "openai"], default="anthropic")
ap.add_argument("--model", default="claude-sonnet-5")
ap.add_argument("--n", type=int, default=10)
ap.add_argument("--temp", type=float, default=1.0)
ap.add_argument("--no-sampling", action="store_true")
ap.add_argument("--max-tokens", type=int, default=120)
ap.add_argument("--prompt", default="Write one sentence about a tide that came in an hour early.")
a = ap.parse_args()
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

args = types.SimpleNamespace(temp=a.temp, no_sampling=a.no_sampling, max_tokens=a.max_tokens, seed=42,
                             system=None, think=False)
step = loop.make_step(a.backend, "chat", a.model)

outs = []
for i in range(a.n):
    args.seed = 42 + i
    text, meta = step(a.prompt, args)
    outs.append(text)
    print("[%2d %-8s] %s" % (i + 1, meta.get("sampling"), text[:110].replace("\n", "\\n")), flush=True)

distinct = collections.Counter(outs)
print("\ndistinct outputs: %d / %d" % (len(distinct), a.n))
ref = outs[0]
divs = []
for o in outs[1:]:
    w1, w2 = ref.split(), o.split()
    k = 0
    while k < min(len(w1), len(w2)) and w1[k] == w2[k]: k += 1
    divs.append(k if o != ref else None)
print("first divergent word vs run 1:", divs)
for o, c in distinct.most_common():
    print("  x%d  %s" % (c, hashlib.sha256(o.encode()).hexdigest()[:10]))
