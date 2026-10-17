#!/usr/bin/env python
"""score.py: measurables for the shift-register rule (experiments/shift_20261016/PROTOCOL.md).

  python experiments/shift_20261016/score.py [run_dir ...]      # default: every runs/* here

Per hop: sentence count, words per sentence, whether the hop shifted (input sentences 2..4 == output
sentences 1..3, after whitespace normalisation), exact/normalised recurrence of the full output.
Per run: gliders (capitalised names and concrete nouns that survive more than 4 consecutive hops in the
window), their lifetimes, and collisions (two gliders both present in a hop's new fourth sentence).
No model calls. Writes analysis/<run>.json and prints a summary.
"""
import glob, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FENCE = re.compile(r"^\s*```[a-zA-Z]*\s*\n(.*?)\n\s*```\s*$", re.S)
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")
STOP = set("""the and that with from this were have been there their they them which would could when what into
over after about through where while those these than then into onto upon its his her she he it was had has not but
for off out one two three four five six seven eight nine ten down back away again still just only also very more most
some such each every both few many much own same other another any all""".split())
NAME = re.compile(r"\b([A-Z][a-z]{2,})\b")
NOUNISH = re.compile(r"\b([a-z]{4,})\b")


def norm(s):
    return re.sub(r"\s+", " ", s.strip())


def extract(out):
    s = out.strip()
    m = FENCE.match(s)
    if m:
        s = m.group(1)
    try:
        o = json.loads(s, strict=False)
        if isinstance(o, dict) and isinstance(o.get("text"), str):
            return o["text"], True
    except Exception:
        pass
    return out, False


def sentences(text):
    return [x.strip() for x in SENT.split(norm(text)) if x.strip()]


def score_run(run):
    rows = [json.loads(l) for l in io.open(os.path.join(run, "steps.jsonl"), encoding="utf-8")]
    rows = [r for r in rows if "out" in r]
    if not rows:
        return None
    x0 = None
    sp = os.path.join(run, "summary.json")
    if os.path.exists(sp):
        x0 = json.load(io.open(sp, encoding="utf-8"))["results"][0].get("x0")
    prev_sents = sentences(json.loads(io.open(os.path.join(HERE, "inits", "shift4.json"), encoding="utf-8").read())["text"])
    hops, seen_exact, seen_norm = [], {}, {}
    present = {}   # token -> list of hops it appears in the window
    newsent_tokens = {}
    for r in rows:
        text, parsed = extract(r["out"])
        ss = sentences(text)
        wc = [len(s.split()) for s in ss]
        shifted = len(ss) >= 3 and len(prev_sents) >= 4 and [norm(x) for x in ss[:3]] == [norm(x) for x in prev_sents[1:4]]
        new = ss[-1] if ss else ""
        toks = set(NAME.findall(new)) | set(w for w in NOUNISH.findall(new.lower()) if w not in STOP)
        newsent_tokens[r["t"]] = toks
        wtoks = set(NAME.findall(text)) | set(w for w in NOUNISH.findall(text.lower()) if w not in STOP)
        for w in wtoks:
            present.setdefault(w, []).append(r["t"])
        he, hn = r["hash"], r["nhash"]
        rec = {"t": r["t"], "parsed": parsed, "n_sent": len(ss), "words": wc, "in_cap": (len(ss) == 4 and all(12 <= w <= 18 for w in wc)),
               "shifted": bool(shifted), "exact_repeat_of": seen_exact.get(he), "norm_repeat_of": seen_norm.get(hn),
               "finish": r.get("finish"), "tok_out": r.get("tok_out"), "new_sentence": new}
        seen_exact.setdefault(he, r["t"]); seen_norm.setdefault(hn, r["t"])
        hops.append(rec)
        prev_sents = ss
    # gliders: tokens present in > 4 consecutive hops (longer than the window can carry by shifting alone)
    gliders = {}
    for w, ts in present.items():
        runs_, cur = [], [ts[0]]
        for a, b in zip(ts, ts[1:]):
            if b == a + 1:
                cur.append(b)
            else:
                runs_.append(cur); cur = [b]
        runs_.append(cur)
        best = max(runs_, key=len)
        if len(best) > 4:
            gliders[w] = {"longest_run": len(best), "from": best[0], "to": best[-1], "hops_present": len(ts)}
    collisions = []
    for t, toks in newsent_tokens.items():
        g = [w for w in toks if w in gliders and gliders[w]["from"] < t <= gliders[w]["to"] + 1]
        if len(g) >= 2:
            collisions.append({"t": t, "gliders": sorted(g)})
    n = len(hops)
    summary = {"run": os.path.basename(run.rstrip("/\\")), "hops": n,
               "shifted_frac": round(sum(h["shifted"] for h in hops) / n, 3),
               "in_cap_frac": round(sum(h["in_cap"] for h in hops) / n, 3),
               "n_sent_hist": {str(k): sum(1 for h in hops if h["n_sent"] == k) for k in sorted(set(h["n_sent"] for h in hops))},
               "first_exact_repeat": next((h["t"] for h in hops if h["exact_repeat_of"]), None),
               "first_norm_repeat": next((h["t"] for h in hops if h["norm_repeat_of"]), None),
               "unparsed": sum(1 for h in hops if not h["parsed"]),
               "length_finishes": sum(1 for h in hops if h["finish"] == "length"),
               "gliders": dict(sorted(gliders.items(), key=lambda kv: -kv[1]["longest_run"])[:25]),
               "n_gliders": len(gliders), "collisions": collisions[:50], "n_collisions": len(collisions)}
    os.makedirs(os.path.join(HERE, "analysis"), exist_ok=True)
    json.dump({"summary": summary, "hops": hops}, io.open(os.path.join(HERE, "analysis", summary["run"] + ".json"), "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    return summary


if __name__ == "__main__":
    runs = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "runs", "*")))
    for run in runs:
        if not os.path.exists(os.path.join(run, "steps.jsonl")):
            continue
        s = score_run(run)
        if not s:
            continue
        print("%s: %d hops; shifted %.0f%%; in cap %.0f%%; sentences %s; first exact repeat %s, norm %s; unparsed %d; length finishes %d" % (
            s["run"], s["hops"], 100 * s["shifted_frac"], 100 * s["in_cap_frac"], s["n_sent_hist"], s["first_exact_repeat"], s["first_norm_repeat"], s["unparsed"], s["length_finishes"]))
        print("  gliders (>4 consecutive hops): %d; collisions: %d" % (s["n_gliders"], s["n_collisions"]))
        for w, g in list(s["gliders"].items())[:10]:
            print("    %-14s run %3d hops (%d..%d), present in %d" % (w, g["longest_run"], g["from"], g["to"], g["hops_present"]))
