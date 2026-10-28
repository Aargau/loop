"""Where does each bolstering edit land? For every hop t >= 2 of the assess runs, diff the passage against the
previous one, find the sentences touched and where they sit, and tag the hop with the quality bolstered.
Writes analysis/edit_position.json and prints per-model, per-quality tables. Run from the repo root.

Predictions on record (2026-10-27, before this script was first run), Justin's cut: some instructions act at a
position, others act globally. Sorted by how the notes described the edits: positional = surprise, strangeness,
relatability, grounding, scope; global = economy, floridity, coherence.
P1. For each of the four frontier models, the mean fraction of sentences touched is under 0.40 for every positional
    quality and over 0.60 for every global one.
P2. Surprise edits are end-heavy: mean position of changed content above 0.65 in every frontier model. Scope edits are
    front-heavy: mean position below 0.50 in at least three of four.
P3. Economy and floridity are the two qualities that touch the most sentences in every frontier model.
P4. The ordering of the eight qualities by sentences touched is the same across the frontier models: Spearman rank
    correlation above 0.7 for every pair of models.
Qwen is reported but excluded from P1 to P4 (ten identical hops and a 2-cycle on two qualities).
"""
import difflib, io, json, math, os, re, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
INIT = json.load(io.open(os.path.join(HERE, "inits", "assess.json"), encoding="utf-8"))
QUAL = list(INIT["qualities"])
POSITIONAL = ["surprise", "strangeness", "relatability", "grounding", "scope"]
GLOBAL = ["economy", "floridity", "coherence"]
FRONTIER = ["astra", "gemini", "mythos", "opus55"]


def parse(out):
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", out.strip())
    try:
        d = json.loads(s)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def sentences(t):
    t = re.sub(r"\s+", " ", t.strip())
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'“‘(]?[A-Z0-9])", t)
    return [p for p in parts if p]


def words(t):
    return re.findall(r"\S+", t)


def hop_edit(prev, cur):
    """Diff prev -> cur at word level; map changed cur spans (and deletion points) onto cur's sentences."""
    pw, cw = words(prev), words(cur)
    if not cw:
        return None
    sents = sentences(cur)
    # word index -> sentence index in cur
    sidx, k = [], 0
    for i, s in enumerate(sents):
        for _ in words(s):
            sidx.append(i)
    n = len(cw)
    sidx = (sidx + [len(sents) - 1] * n)[:n]
    sm = difflib.SequenceMatcher(None, pw, cw, autojunk=False)
    changed = 0; touched = set(); pos_w = []; spans = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        spans += 1
        if j2 > j1:
            for j in range(j1, j2):
                touched.add(sidx[j]); pos_w.append((j + 0.5) / n)
            changed += j2 - j1
        else:  # pure deletion: a point in cur
            j = min(j1, n - 1); touched.add(sidx[j])
            w = i2 - i1; changed += w; pos_w.extend([(j + 0.5) / n] * w)
    frac_sent = len(touched) / len(sents) if sents else None
    frac_words = min(1.0, changed / n)
    mean_pos = statistics.mean(pos_w) if pos_w else None
    # within-hop dispersion of edit positions: 0 = one spot, ~0.29 = spread uniformly over the passage.
    # Added after the first run (post hoc): the sentences-touched measure turned out to follow the model's editing
    # style rather than the quality, so this is the second operationalisation of "positional versus global".
    pos_sd = statistics.pstdev(pos_w) if len(pos_w) > 1 else (0.0 if pos_w else None)
    last5 = sum(1 for p in pos_w if p >= 0.8) / len(pos_w) if pos_w else None
    first5 = sum(1 for p in pos_w if p < 0.2) / len(pos_w) if pos_w else None
    return {"frac_sentences": round(frac_sent, 3), "frac_words": round(frac_words, 3), "mean_pos": round(mean_pos, 3) if mean_pos is not None else None,
            "pos_sd": round(pos_sd, 3) if pos_sd is not None else None,
            "share_last20": round(last5, 3) if last5 is not None else None, "share_first20": round(first5, 3) if first5 is not None else None,
            "spans": spans, "n_sentences": len(sents), "identical": (pw == cw)}


def spearman(a, b):
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i]); r = [0] * len(x)
        for rank, i in enumerate(order): r[i] = rank
        return r
    ra, rb = ranks(a), ranks(b); n = len(a)
    d2 = sum((x - y) ** 2 for x, y in zip(ra, rb))
    return round(1 - 6 * d2 / (n * (n * n - 1)), 3)


def main():
    per = {}
    for run in sorted(os.listdir(RUNS)):
        p = os.path.join(RUNS, run, "steps.jsonl")
        if not os.path.exists(p):
            continue
        recs = [json.loads(l) for l in io.open(p, encoding="utf-8")]
        objs = [parse(r["out"]) for r in recs if "out" in r]
        hops = []
        for t in range(1, len(objs)):
            a, b = objs[t - 1], objs[t]
            if not a or not b or not a.get("text") or not b.get("text"):
                continue
            h = b.get("history") or []
            q = h[-1] if h else None
            e = hop_edit(a["text"], b["text"])
            if e:
                e["t"] = t + 1; e["quality"] = q; hops.append(e)
        byq = defaultdict(list)
        for e in hops:
            if e["quality"] in QUAL and not e["identical"]:
                byq[e["quality"]].append(e)
        summ = {}
        for q in QUAL:
            es = byq.get(q, [])
            if not es:
                summ[q] = {"n": 0}; continue
            summ[q] = {"n": len(es),
                       "frac_sentences": round(statistics.mean(e["frac_sentences"] for e in es), 3),
                       "frac_words": round(statistics.mean(e["frac_words"] for e in es), 3),
                       "mean_pos": round(statistics.mean(e["mean_pos"] for e in es), 3),
                       "pos_sd": round(statistics.mean(e["pos_sd"] for e in es), 3),
                       "share_last20": round(statistics.mean(e["share_last20"] for e in es), 3),
                       "share_first20": round(statistics.mean(e["share_first20"] for e in es), 3),
                       "spans": round(statistics.mean(e["spans"] for e in es), 1)}
        per[run] = {"hops": hops, "by_quality": summ, "identical_hops": sum(1 for e in hops if e["identical"])}
    # predictions
    pred = {}
    p1 = {}
    for run in FRONTIER:
        s = per[run]["by_quality"]
        p1[run] = {"positional_max": max(s[q]["frac_sentences"] for q in POSITIONAL if s[q]["n"]),
                   "global_min": min(s[q]["frac_sentences"] for q in GLOBAL if s[q]["n"])}
    pred["P1"] = p1
    pred["P2"] = {run: {"surprise_pos": per[run]["by_quality"]["surprise"].get("mean_pos"), "scope_pos": per[run]["by_quality"]["scope"].get("mean_pos")} for run in FRONTIER}
    pred["P3"] = {run: sorted(QUAL, key=lambda q: -(per[run]["by_quality"][q].get("frac_sentences") or 0))[:2] for run in FRONTIER}
    rho = {}
    for i, a in enumerate(FRONTIER):
        for b in FRONTIER[i + 1:]:
            va = [per[a]["by_quality"][q].get("frac_sentences") or 0 for q in QUAL]
            vb = [per[b]["by_quality"][q].get("frac_sentences") or 0 for q in QUAL]
            rho["%s/%s" % (a, b)] = spearman(va, vb)
    pred["P4"] = rho
    out = {"per_run": {r: {"by_quality": per[r]["by_quality"], "identical_hops": per[r]["identical_hops"]} for r in per},
           "hops": {r: per[r]["hops"] for r in per}, "predictions": pred}
    io.open(os.path.join(HERE, "analysis", "edit_position.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1))
    for run in per:
        print("=== %s (identical hops: %d)" % (run, per[run]["identical_hops"]))
        print("  %-12s %3s %6s %6s %6s %6s %6s %6s %5s" % ("quality", "n", "sent", "words", "pos", "possd", "last20", "first20", "spans"))
        for q in sorted(QUAL, key=lambda q: -(per[run]["by_quality"][q].get("pos_sd") or 0)):
            s = per[run]["by_quality"][q]
            if not s["n"]:
                print("  %-12s %3d" % (q, 0)); continue
            print("  %-12s %3d %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f %5.1f" % (q, s["n"], s["frac_sentences"], s["frac_words"], s["mean_pos"], s["pos_sd"], s["share_last20"], s["share_first20"], s["spans"]))
    print("P1", json.dumps(pred["P1"])); print("P2", json.dumps(pred["P2"])); print("P3", json.dumps(pred["P3"])); print("P4", json.dumps(pred["P4"]))


if __name__ == "__main__":
    main()
