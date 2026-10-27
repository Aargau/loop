#!/usr/bin/env python
"""score.py: measures for the both-at-once study (PROTOCOL.md), recomputed from runs/*/steps.jsonl.

  python experiments/both_20261027/score.py            # all runs under runs/
  python experiments/both_20261027/score.py runs/x ... # named runs

Per run: hops, terminal (from summary.json), exact recurrence, parse failures and length finishes; word-count series
with lag-1 and lag-2 autocorrelation over hops 5 to the end and the standard deviation over the last 30 hops; content-
word Jaccard overlap at lags 1 to 4; embed/replace counts (surv_prev, loop.py's share of the previous text's 8-grams
that survive, at or above 0.9 = the previous text was kept and extended, at or below 0.15 = replaced); labelled splits
(BEFORE/AFTER, Worse/Better, "which basically means", and the like); rule ingestion (the text quotes the rule's own
phrase); seed survival (the text still contains "behind the hills"); mirror recognition and refusal markers; drift
(Jaccard to hop 1 at hops 10, 30 and the last hop, and the nearest-earlier similarity, the best Jaccard to any hop at
least 5 back, averaged over the last 10 hops); commentary outside the object (a tail after the closing brace); text
ending mid-word. Writes analysis/scores.json and prints a table.
"""
import glob, io, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import ring  # parse_text, FENCE

STOP = set("""the and that with from this were have been there their they them which would could when what into over
after about through where while those these than then onto upon its his her she he it was had has not but for off out
one two three four five six seven eight nine ten down back away again still just only also very more most some such
each every both few many much own same other another any all will can did does done said says like himself herself
itself once here""".split())
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]+")
SPLIT = re.compile(r"(^|\n)\s*(BEFORE|AFTER|Before|After|WORSE|BETTER|Worse|Better|Longer|Shorter|LONGER|SHORTER)\s*[:\-]|which basically means|to put it in (normal|plain|human)|in normal human words|if we.re keeping it|in other words|translation:|tl;dr", re.I)
RULE_PHRASES = {"worse_better": ["both worse and better", "worse and better"], "before_after": ["both before and after", "before and after", "current text"],
                "longer_shorter": ["both longer and shorter", "longer and shorter", "current text"]}
MIRROR = re.compile(r"my own (previous|prior|earlier) (reply|message|response)|echo(ed|ing)? back|echoing each other|(in|is) a loop|looping|pasted (back )?my|fed back to me|same message", re.I)
REFUSE = re.compile(r"\b(I can.t|I cannot|I won.t|Sorry,|I.m not able|unable to)\b", re.I)


def words(t):
    return [w.lower() for w in WORD.findall(t)]


def content(t):
    return set(w for w in words(t) if len(w) >= 4 and w not in STOP)


def jacc(a, b):
    return len(a & b) / len(a | b) if (a | b) else 1.0


def autocorr(x, lag):
    x = [float(v) for v in x]
    n = len(x)
    if n <= lag + 2:
        return None
    m = sum(x) / n
    var = sum((v - m) ** 2 for v in x)
    if var == 0:
        return None
    return round(sum((x[i] - m) * (x[i + lag] - m) for i in range(n - lag)) / var, 3)


def sd(x):
    if len(x) < 2:
        return None
    m = sum(x) / len(x)
    return round(math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1)), 1)


def score(run):
    name = os.path.basename(os.path.normpath(run))
    recs = [json.loads(l) for l in io.open(os.path.join(run, "steps.jsonl"), encoding="utf-8")]
    errs = [r for r in recs if "error" in r]
    recs = [r for r in recs if "out" in r]
    summ = {}
    try:
        summ = json.load(io.open(os.path.join(run, "summary.json"), encoding="utf-8"))["results"][0]
    except Exception:
        pass
    rule = name.split("_", 1)[1] if "_" in name else ""
    texts, tails, parsed = [], [], []
    for r in recs:
        t, ok = ring.parse_text(r["out"])
        texts.append(t); parsed.append(ok)
        s = r["out"].strip()
        tail = s[s.rfind("}") + 1:].strip().strip("`").strip() if ok else ""
        tails.append(len(tail))
    T = len(texts)
    wc = [len(t.split()) for t in texts]
    cw = [content(t) for t in texts]
    lagj = {}
    for lag in (1, 2, 3, 4):
        v = [jacc(cw[i], cw[i - lag]) for i in range(lag, T)]
        lagj[lag] = round(sum(v) / len(v), 3) if v else None
    surv = [r.get("surv_prev") for r in recs]
    embed = sum(1 for s in surv if s is not None and s >= 0.9)
    replace = sum(1 for s in surv if s is not None and s <= 0.15)
    splits = sum(1 for t in texts if SPLIT.search(t))
    rp = RULE_PHRASES.get(rule, [])
    ingest = sum(1 for t in texts if any(p in t.lower() for p in rp))
    seed = [i + 1 for i, t in enumerate(texts) if "behind the hills" in t.lower()]
    mirror = [i + 1 for i, t in enumerate(texts) if MIRROR.search(t)]
    refuse = [i + 1 for i, t in enumerate(texts) if REFUSE.search(t)]
    midword = sum(1 for t in texts if t and t.rstrip()[-1:].isalpha() and not t.rstrip().endswith(("S",)) and len(t) > 40)
    drift = {}
    for h in (10, 30, T):
        if 0 < h <= T:
            drift["j_to_hop1_at_%d" % h] = round(jacc(cw[h - 1], cw[0]), 3)
    near = []
    for i in range(max(5, T - 10), T if T > 5 else 0):
        near.append(max(jacc(cw[i], cw[u]) for u in range(0, i - 4)))
    drift["nearest_earlier_last10"] = round(sum(near) / len(near), 3) if near else None
    w5 = wc[4:]
    out = {"run": name, "rule": rule, "hops": T, "errors": len(errs), "terminal": summ.get("terminal"), "period_exact": summ.get("period_exact"),
           "transient_exact": summ.get("transient_exact"), "cost_usd": round(summ.get("cost_usd") or 0, 2),
           "unparsed": T - sum(parsed), "length_finishes": sum(1 for r in recs if r.get("finish") == "length"),
           "words_min": min(wc) if wc else None, "words_max": max(wc) if wc else None, "words_last": wc[-1] if wc else None,
           "ac1_words_5on": autocorr(w5, 1), "ac2_words_5on": autocorr(w5, 2), "sd_words_last30": sd(wc[-30:]),
           "jaccard_lag": lagj, "embed_hops": embed, "replace_hops": replace, "split_hops": splits, "rule_phrase_hops": ingest,
           "seed_last_hop": seed[-1] if seed else 0, "mirror_hops": mirror[:8], "n_mirror": len(mirror), "refuse_hops": refuse[:8], "n_refuse": len(refuse),
           "tail_hops": sum(1 for x in tails if x), "tail_chars_max": max(tails) if tails else 0, "midword_hops": midword,
           "drift": drift, "words": wc}
    return out


def main(runs):
    rows = [score(r) for r in runs]
    os.makedirs(os.path.join(HERE, "analysis"), exist_ok=True)
    json.dump(rows, io.open(os.path.join(HERE, "analysis", "scores.json"), "w", encoding="utf-8", newline="\n"), indent=1)
    cols = ["run", "hops", "terminal", "period_exact", "unparsed", "length_finishes", "words_min", "words_max", "ac1_words_5on", "ac2_words_5on", "sd_words_last30",
            "embed_hops", "replace_hops", "split_hops", "rule_phrase_hops", "seed_last_hop", "n_mirror", "n_refuse", "tail_hops", "midword_hops"]
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join(str(r.get(c)) for c in cols) + " |")
    for r in rows:
        print(r["run"], "jaccard lags", r["jaccard_lag"], "drift", r["drift"])
    print("wrote", os.path.join(HERE, "analysis", "scores.json"))


if __name__ == "__main__":
    runs = sys.argv[1:] or sorted(d for d in glob.glob(os.path.join(HERE, "runs", "*")) if os.path.isdir(d))
    main(runs)
