# -*- coding: utf-8 -*-
"""cb_analysis.py: the Cerebras runs (site/runs_extra/cb_*).

    python cb_analysis.py numerics     local Q8 vs Cerebras: same init, same rule, where do they part, do the attractors match
    python cb_analysis.py census       twenty seeds under json_page: how many attractors
    python cb_analysis.py sampling     change-four at T=0.7, five seeds

Metrics fixed before the runs:
  numerics: first divergence character at hop 1; terminal (tau, period) on each side; census key
            (first five normalized words) of the terminal text on each side; cosine between the
            two terminal texts when the embedding server is up.
  census:   per seed: tau, period, terminal text's key, its setting nouns; attractors counted three
            ways: identical terminal text, identical key, cosine >= 0.90 single-link clusters.
  sampling: per seed: tau, period, hops without copy; whether hop 8/9 froze as at T=0.
"""
import json, re, sys, pathlib, collections, urllib.request
HERE = pathlib.Path(__file__).resolve().parent; LOOP = HERE.parent
sys.path.insert(0, str(LOOP)); sys.path.insert(0, str(HERE))
import loop as L
import build as B

EMBED = "http://127.0.0.1:8081"

def embed(texts):
    try:
        req = urllib.request.Request(EMBED + "/v1/embeddings", data=json.dumps({"input": [t[:6000] or " " for t in texts]}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return [d["embedding"] for d in json.loads(r.read().decode())["data"]]
    except Exception:
        return None

def cos(a, b):
    num = sum(x * y for x, y in zip(a, b)); da = sum(x * x for x in a) ** .5; db = sum(y * y for y in b) ** .5
    return num / (da * db) if da and db else 0.0

def key(s, n=5):
    w = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split(); return " ".join(w[:n])

def load(name):
    d = HERE / "runs_extra" / name
    p = d / "steps.jsonl"
    if not p.exists(): return None
    hops = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    hops = list({h["t"]: h for h in hops if "t" in h and "out" in h}.values()); hops.sort(key=lambda h: h["t"])
    sp = d / "summary.json"
    summ = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else None
    return dict(name=name, hops=hops, summary=summ, done=summ is not None)

def terminal(hops):
    """(tau, period) from exact raw recurrence, computed here rather than trusted from summary."""
    raws = [h["out"] for h in hops]
    first = {}
    for t, r in enumerate(raws, 1):
        if r in first: return first[r], t - first[r]
        first[r] = t
    return None, None

def text_at(hops, t):
    return B.text_of(hops[t - 1]["out"])[0]

def numerics():
    runs, _ = B.load_bundle()
    pairs = [("20260902T172519_chat", "json_better", "cb_json_better"),
             ("20260902T155321_chat", "json_para", "cb_json_para"),
             ("20260902T155557_chat", "json_page", "cb_json_page"),
             ("20260902T174258_chat", "json_worse", "cb_json_worse"),
             ("20260902T172547_chat", "json_unexpected", "cb_json_unexpected"),
             ("20260902T165324_chat", "json_prev", "cb_json_prev"),
             ("qwen_div_local", "div_local.json", "cb_div_local"),
             ("qwen_div_hook", "div_hook.json", "cb_div_hook")]
    extra = B.load_extra()
    for lrun, tag, cname in pairs:
        cb = load(cname)
        if cb is None: print("%-18s not run yet" % cname); continue
        lhops = [h for h in (runs.get(lrun) or extra.get(lrun))["hops"] if h.get("tag") == tag and "text" in h]
        lraws = [h["raw"] for h in lhops]; craws = [h["out"] for h in cb["hops"]]
        div = L.common_prefix(lraws[0], craws[0])
        same_hops = sum(1 for a, b in zip(lraws, craws) if a == b)
        lt = terminal_from_raws(lraws); ct = terminal(cb["hops"])
        ltext = B.text_of(lraws[lt[0] if lt[0] else len(lraws) - 1])[0] if lraws else ""
        ctext = text_at(cb["hops"], ct[0] if ct[0] else len(craws))
        v = embed([ltext, ctext]); c = cos(v[0], v[1]) if v else None
        print("== %s vs local %s/%s%s" % (cname, lrun, tag, "" if cb["done"] else "  (still running)"))
        print("   hop 1 shares %d chars; identical hops %d/%d" % (div, same_hops, min(len(lraws), len(craws))))
        print("   local    tau=%s p=%s  key=%r" % (lt[0], lt[1], key(ltext)))
        print("   cerebras tau=%s p=%s  key=%r" % (ct[0], ct[1], key(ctext)))
        print("   terminal cosine=%s  same key=%s  same text=%s" % ("%.3f" % c if c is not None else "-", key(ltext) == key(ctext), ltext == ctext))
        print("   local    terminal: %s" % ltext[:160].replace("\n", " | "))
        print("   cerebras terminal: %s" % ctext[:160].replace("\n", " | "))
        print()

def terminal_from_raws(raws):
    first = {}
    for t, r in enumerate(raws, 1):
        if r in first: return first[r], t - first[r]
        first[r] = t
    return None, None

SETTING_WORDS = ["tide", "rain", "sea", "shore", "pier", "harbor", "beach", "city", "street", "kitchen", "house", "room", "forest", "mountain", "desert",
                 "train", "station", "ship", "moon", "space", "server", "office", "church", "cemetery", "school", "hospital", "library", "garden",
                 "lab", "bridge", "cellar", "door", "window", "river", "lake", "storm", "fog", "snow", "field", "village", "town", "road"]

def census():
    rows = []; texts = []; names = []
    inits = HERE / "runs_extra" / "inits"
    for i in range(0, 21):
        cname = "cb_json_page" if i == 0 else "cb_census_%02d" % i
        cb = load(cname)
        if cb is None: print("%-14s not run yet" % cname); continue
        if i == 0: seed = json.loads(L.INITS["json_page"])["text"]
        else: seed = json.loads((inits / ("census_%02d.json" % i)).read_text(encoding="utf-8"))["text"]
        tau, p = terminal(cb["hops"])
        tt = text_at(cb["hops"], tau if tau else len(cb["hops"]))
        words = collections.Counter(re.findall(r"[a-z]+", tt.lower()))
        sett = [w for w in SETTING_WORDS if words.get(w)]
        rows.append((cname, seed, tau, p, len(cb["hops"]), cb["done"], key(tt), sett[:5], tt))
        texts.append(tt); names.append(cname)
    print("%-14s %-6s %-3s %-4s %-5s %-34s %s" % ("run", "tau", "p", "hops", "done", "terminal key", "settings"))
    for r in rows:
        print("%-14s %-6s %-3s %-4d %-5s %-34s %s" % (r[0], r[2], r[3], r[4], "y" if r[5] else "RUN", r[6][:34], ",".join(r[7])))
        print("      seed: %s" % r[1])
        print("      end : %s" % r[8][:150].replace("\n", " "))
    n = len(rows)
    if n < 2: return
    print("\nattractors among %d seeds:" % n)
    print("  by identical terminal text: %d" % len(set(texts)))
    print("  by terminal key           : %d" % len(set(r[6] for r in rows)))
    v = embed(texts)
    if v:
        # single-link clusters at cosine >= 0.90
        parent = list(range(n))
        def find(a):
            while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
            return a
        pairs = []
        for a in range(n):
            for b in range(a + 1, n):
                c = cos(v[a], v[b]); pairs.append((c, a, b))
                if c >= 0.90: parent[find(a)] = find(b)
        cl = collections.defaultdict(list)
        for a in range(n): cl[find(a)].append(names[a])
        print("  by cosine >= 0.90 (single link): %d clusters" % len(cl))
        for k, mem in sorted(cl.items(), key=lambda kv: -len(kv[1])):
            if len(mem) > 1: print("     ", mem)
        pairs.sort(reverse=True)
        print("  closest terminal pairs:", ["%s~%s %.3f" % (names[a], names[b], c) for c, a, b in pairs[:6]])
        print("  mean pairwise cosine: %.3f  (min %.3f, max %.3f)" % (sum(c for c, _, _ in pairs) / len(pairs), pairs[-1][0], pairs[0][0]))
    # distribution of tau and period
    print("  tau distribution:", dict(collections.Counter(r[2] for r in rows)))
    print("  period distribution:", dict(collections.Counter(r[3] for r in rows)))
    ended_on = collections.Counter()
    for r in rows:
        last = re.split(r"(?<=[.!?])\s+", r[8].strip())[-1][:80]
        ended_on[last] += 1
    print("  terminal last sentences:")
    for s, c in ended_on.most_common(): print("     %d  %s" % (c, s))

def sampling():
    base = load("cb_div_local")
    if base: print("T=0: tau=%s p=%s" % terminal(base["hops"]))
    for s in range(1, 6):
        cb = load("cb_div_local_T07_s%d" % s)
        if cb is None: print("seed %d not run yet" % s); continue
        tau, p = terminal(cb["hops"])
        texts = [text_at(cb["hops"], t) for t in range(1, len(cb["hops"]) + 1)]
        tcopy = next((t for t in range(1, len(texts)) if texts[t] in texts[:t]), None)
        print("seed %d: %d hops, exact tau=%s p=%s, first text-level copy at hop %s, %s" % (
            s, len(cb["hops"]), tau, p, (tcopy + 1) if tcopy is not None else None, "done" if cb["done"] else "running"))
        print("   hop 1: %s" % texts[0].split("\n")[0][:70])
        print("   last : %s" % texts[-1].split("\n")[0][:70])

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "numerics"
    {"numerics": numerics, "census": census, "sampling": sampling}[what]()
