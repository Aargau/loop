# -*- coding: utf-8 -*-
"""prev_analysis.py: recurrence analysis of the BEFORE (json_prev) trajectory, base run + extension.

    python prev_analysis.py

Sequence: data/20260902T165324_chat.json hops 1..60, then site/runs_extra/qwen_prev_ext hops as 61..N.
Reports, per level: exact (raw bytes), normalized (loop.norm), census key (first five words),
and for each hop the earlier hop with the smallest NCD (zlib), so a loose recurrence is visible.
"""
import json, re, sys, zlib, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent; LOOP = HERE.parent
sys.path.insert(0, str(LOOP)); sys.path.insert(0, str(HERE))
import loop as L
import build as B

def key(s, n=5):
    w = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split(); return " ".join(w[:n])

def main():
    base = json.loads((LOOP / "data" / "20260902T165324_chat.json").read_text(encoding="utf-8"))
    seq = [(h["t"], h["raw"], h["text"]) for h in sorted(base["hops"], key=lambda h: h["t"])]
    p = HERE / "runs_extra" / "qwen_prev_ext" / "steps.jsonl"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            j = json.loads(line)
            if "out" not in j: continue
            t, _ = B.text_of(j["out"])
            seq.append((j["t"] + 60, j["out"], t))
    n = len(seq)
    print("hops:", n)
    raws = [r for _, r, _ in seq]; texts = [x for _, _, x in seq]
    # exact / normalized
    for name, f in (("exact", lambda s: s), ("norm", L.norm)):
        seen = {}
        hits = []
        for i, r in enumerate(raws):
            k = f(r)
            if k in seen: hits.append((i + 1, seen[k] + 1))
            else: seen[k] = i
        print("%s recurrences: %s" % (name, hits[:20] if hits else "none"))
    # census keys
    keys = collections.OrderedDict()
    for i, x in enumerate(texts): keys.setdefault(key(x), []).append(i + 1)
    print("distinct 5-word keys:", len(keys))
    for k, ts in keys.items():
        if len(ts) > 2: print("  %-40s %s" % (k, ts))
    # nearest earlier hop by NCD (raw), for the extension hops
    def C(b): return len(zlib.compress(b, 9))
    comp = [C(r.encode()) for r in raws]
    print("\nnearest earlier hop by NCD (hop: nearest, ncd), extension hops only")
    for i in range(60, n):
        best = None
        for j in range(i):
            a, b = raws[j].encode(), raws[i].encode()
            d = (C(a + b) - min(comp[j], comp[i])) / max(comp[j], comp[i], 1)
            if best is None or d < best[1]: best = (j + 1, d)
        flag = "  <-- close" if best[1] < 0.5 else ""
        print("  %3d: %3d  %.3f%s   %s" % (i + 1, best[0], best[1], flag, texts[i][:60].replace("\n", " ")))

if __name__ == "__main__":
    main()
