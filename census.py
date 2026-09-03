"""census.py -- semantic-state census and transition graph over loop runs.
Key = normalized first N words of the text field (or raw output). With --rot, key = hash of the
sorted set of 5-grams occurring >=2 times (rotation-invariant: catches periodic content
translating through the window, which the exact hash can't see). Prints state census,
transition counts, and per-run walks as key sequences.
  python census.py runs\20260902T155557_chat runs\20260902T160344_chat --words 5
  python census.py runs\20260902T162514_raw --rot
"""
import sys, json, re, os, collections, argparse, hashlib

ap = argparse.ArgumentParser()
ap.add_argument("runs", nargs="+")
ap.add_argument("--words", type=int, default=5)
ap.add_argument("--tag", default=None, help="only this tag prefix")
ap.add_argument("--rot", action="store_true", help="rotation-invariant key (sorted repeated 5-gram set)")
ap.add_argument("--min", type=int, default=2, help="min count for a 5-gram to enter the --rot key")
a = ap.parse_args()

FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)
def text_of(out):
    m = FENCE.match(out)
    if m: out = m.group(1)
    try:
        return json.loads(out).get("text", out)
    except Exception:
        return out

def key(s):
    w = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()
    if a.rot:
        c = collections.Counter(tuple(w[i:i + 5]) for i in range(len(w) - 4))
        core = sorted(g for g, n in c.items() if n >= a.min)
        if not core:
            return "norep | " + (" ".join(w[:a.words]) or "<empty>")
        return "bag:%s reps=%d | %s" % (hashlib.sha1(repr(core).encode()).hexdigest()[:8], len(core), " ".join(core[0]))
    return " ".join(w[:a.words]) or "<empty>"

walks = collections.OrderedDict()
for r in a.runs:
    p = os.path.join(r, "steps.jsonl")
    for line in open(p, encoding="utf-8"):
        j = json.loads(line)
        if "out" not in j: continue
        if a.tag and not j["tag"].startswith(a.tag): continue
        walks.setdefault((os.path.basename(r), j["tag"]), []).append((j["t"], key(text_of(j["out"]))))

states = collections.Counter(); trans = collections.Counter(); fixed = collections.Counter()
for (run, tag), seq in walks.items():
    seq.sort()
    ks = [k for _, k in seq]
    for k in ks: states[k] += 1
    for x, y in zip(ks, ks[1:]):
        trans[(x, y)] += 1
        if x == y: fixed[x] += 1

ids = {k: i for i, (k, _) in enumerate(states.most_common())}
print("== states (id, visits, self-loops)")
for k, n in states.most_common():
    print("  S%-2d %4d %4d  %s" % (ids[k], n, fixed.get(k, 0), k))
print("\n== transitions (excluding self-loops)")
for (x, y), n in sorted(trans.items(), key=lambda kv: -kv[1]):
    if x != y: print("  S%-2d -> S%-2d  x%d" % (ids[x], ids[y], n))
print("\n== walks")
for (run, tag), seq in walks.items():
    seq.sort()
    path = []
    for _, k in seq:
        s = "S%d" % ids[k]
        if path and path[-1].split("x")[0] == s:
            base, _, cnt = path[-1].partition("x"); path[-1] = "%sx%d" % (base, int(cnt or 1) + 1)
        else:
            path.append(s)
    print("  %-26s %-12s %s" % (run, tag, " > ".join(path)))
