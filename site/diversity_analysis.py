# -*- coding: utf-8 -*-
"""diversity_analysis.py: metrics for the diversity arms (site/runs_extra/qwen_div_*).

    python diversity_analysis.py [glob]        default glob: qwen_div_*   (e.g. cb_div_*)

Per arm and per hop, on the decoded text field only (the ledger arms carry step/history in the
state, so raw-level recurrence is impossible by construction there):
  - form: number of lines, words per line, compliance with "four lines of five to ten words"
  - recurrence: exact text repeat of an earlier hop; normalized repeat (loop.norm)
  - census key (first five words)
  - nearest earlier hop by NCD (zlib) on the text, and by cosine if the embedding server is up
  - ledger integrity (ledger arms): step == previous step + 1, every previous history item
    preserved verbatim in order, exactly one item appended, signature is four lowercase words
  - the wall: tok_out == max_tokens
Prints a per-hop table and a summary line per arm. Metrics were fixed before the runs.
"""
import json, re, sys, zlib, pathlib, collections, urllib.request
HERE = pathlib.Path(__file__).resolve().parent; LOOP = HERE.parent
sys.path.insert(0, str(LOOP)); sys.path.insert(0, str(HERE))
import loop as L
import build as B

EMBED = "http://127.0.0.1:8081"

def embed(texts):
    try:
        req = urllib.request.Request(EMBED + "/v1/embeddings", data=json.dumps({"input": texts}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            j = json.loads(r.read().decode())
        vs = [d["embedding"] for d in j["data"]]
        return vs
    except Exception:
        return None

def cos(a, b):
    num = sum(x * y for x, y in zip(a, b)); da = sum(x * x for x in a) ** .5; db = sum(y * y for y in b) ** .5
    return num / (da * db) if da and db else 0.0

def C(b): return len(zlib.compress(b, 9))
def ncd(a, b):
    a, b = a.encode(), b.encode()
    if not a or not b: return 1.0
    ca, cb = C(a), C(b); return (C(a + b) - min(ca, cb)) / max(ca, cb, 1)

def key(s, n=5):
    w = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split(); return " ".join(w[:n])

def parse(out):
    m = B.FENCE.match(out)
    s = m.group(1) if m else out
    try: return json.loads(s)
    except Exception: return None

def form(text):
    lines = [l for l in text.split("\n") if l.strip()]
    wc = [len(l.split()) for l in lines]
    ok = len(lines) == 4 and all(5 <= w <= 10 for w in wc)
    return len(lines), wc, ok

SIG = re.compile(r"^[a-z]+ [a-z]+ [a-z]+ [a-z]+$")

def main():
    pat = sys.argv[1] if len(sys.argv) > 1 else "qwen_div_*"
    for d in sorted(HERE.glob("runs_extra/" + pat)):
        p = d / "steps.jsonl"
        if not p.exists(): continue
        hops = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        hops = list({h["t"]: h for h in hops if "t" in h and "out" in h}.values()); hops.sort(key=lambda h: h["t"])
        sp = d / "summary.json"
        budget = json.loads(sp.read_text(encoding="utf-8"))["args"]["max_tokens"] if sp.exists() else 2048
        x0 = json.loads((HERE / "runs_extra" / "inits" / hops[0]["tag"]).read_text(encoding="utf-8"))
        texts = [x0["text"]] + [B.text_of(h["out"])[0] for h in hops]
        objs = [x0] + [parse(h["out"]) for h in hops]
        maxtok = max(h["tok_out"] for h in hops)
        vecs = embed(texts)
        print("== %s: %d hops, max tok_out %d" % (d.name, len(hops), maxtok))
        first_exact = None; first_norm = None; form_ok = 0; walls = 0; ledger_errs = []
        keys = collections.Counter(); sigs = []
        rows = []
        for t in range(1, len(texts)):
            tx = texts[t]
            ex = next((k for k in range(t) if texts[k] == tx), None)
            nm = next((k for k in range(t) if L.norm(texts[k]) == L.norm(tx)), None)
            if ex is not None and first_exact is None: first_exact = (t, ex)
            if nm is not None and first_norm is None: first_norm = (t, nm)
            nl, wc, ok = form(tx); form_ok += ok
            keys[key(tx)] += 1
            near = min(((ncd(texts[k], tx), k) for k in range(t)), default=(1.0, 0))
            nc = None
            if vecs: nc = max(((cos(vecs[k], vecs[t]), k) for k in range(t)), default=(0.0, 0))
            wall = hops[t - 1]["tok_out"] >= budget; walls += wall
            led = ""
            o, po = objs[t], objs[t - 1]
            if isinstance(po, dict) and "history" in po:
                if not isinstance(o, dict) or "history" not in o:
                    led = "NO LEDGER"; ledger_errs.append(t)
                else:
                    ph, h = po.get("history", []), o.get("history", [])
                    probs = []
                    if "step" in po and o.get("step") != (po.get("step") or 0) + 1: probs.append("step")
                    if h[:len(ph)] != ph: probs.append("history altered")
                    if len(h) != len(ph) + 1: probs.append("appended %d" % (len(h) - len(ph)))
                    if h and not SIG.match(h[-1].strip()): probs.append("bad signature")
                    if o.get("rule") != po.get("rule"): probs.append("rule changed")
                    if h: sigs.append(h[-1])
                    led = ", ".join(probs) if probs else "ok"
                    if probs: ledger_errs.append(t)
            rows.append((t, nl, "/".join(map(str, wc)), "Y" if ok else "n", ex, nm, "%.2f@%d" % near, ("%.2f@%d" % nc) if nc else "-", "WALL" if wall else "", led, tx.split("\n")[0][:50]))
        for r in rows:
            print("  t=%3d lines=%d words=%-12s form=%s exact=%s norm=%s ncd_near=%s cos_near=%s %s %s | %s" % r)
        sig_reuse = sum(1 for s, n in collections.Counter(sigs).items() if n > 1)
        settings = collections.Counter(s.split()[0] for s in sigs if s.split())
        print("  SUMMARY first exact text repeat=%s first norm repeat=%s form ok %d/%d walls=%d distinct keys=%d" % (
            first_exact, first_norm, form_ok, len(hops), walls, len(keys)))
        if sigs:
            print("  LEDGER signatures=%d distinct=%d reused=%d distinct settings=%d first error at hop=%s errors=%d" % (
                len(sigs), len(set(sigs)), sig_reuse, len(settings), ledger_errs[0] if ledger_errs else None, len(ledger_errs)))
            print("  settings:", dict(settings.most_common(12)))
        if vecs:
            near_cos = [max(cos(vecs[k], vecs[t]) for k in range(t)) for t in range(1, len(texts))]
            q = len(near_cos) // 4 or 1
            print("  nearest-earlier cosine, mean by quarter:", ["%.3f" % (sum(near_cos[i:i + q]) / max(1, len(near_cos[i:i + q]))) for i in range(0, len(near_cos), q)])
        print()

if __name__ == "__main__":
    main()
