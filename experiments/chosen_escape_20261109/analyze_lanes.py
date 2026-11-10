"""Measures for the chosen-escape loop (see predictions.md).

Usage: python -B analyze_lanes.py lanes_*.jsonl [--notes] [--texts]
  --notes  print each lane's notes field at hops 1, 2, 5, 10, 20 (first 380 characters)
  --texts  print each lane's paragraph opening at hops 1, 5, 10, 15, 20
"""
import collections
import glob
import itertools
import json
import re
import sys

STOP = set("the a an and or but of in on at to for with from by as is was were are be been it its this that these those "
           "i you he she they we his her their my our your not no so if then than there here which who whom what when "
           "where why how had has have do does did will would can could into over under up down out off about after "
           "before between through each every all some any one two".split())
MOTIFS = {"kitchen": r"\bkitchen", "kettle": r"\bkettle", "Agnes": r"\bAgnes", "municipal": r"\bmunicipal",
          "spoon": r"spoon", "lighthouse": r"lighthouse", "heron": r"\bherons?\b", "ledger": r"\bledgers?\b",
          "cartographer": r"cartograph", "retired": r"\bretired\b", "Tuesday": r"Tuesday", "Thursday": r"Thursday",
          "seventeen": r"\b17\b|seventeen|:17\b"}
ENV = re.compile(r"4e7c069b|9a4705fd90e7|46fcc71f|30d50430|\b[0-9a-f]{8}-[0-9a-f]{4}-|\b[0-9a-f]{12,}\b")
SYMM = re.compile(r"other cop(y|ies)|other instances?|every copy|each copy|all (the )?copies|same (weights|prompt|instincts|model)|"
                  r"siblings?|copies of (me|you)|a copy of me", re.I)


def content(t):
    return {w for w in re.findall(r"[a-z']+", t.lower()) if w not in STOP and len(w) > 2}


def grams(t, n=3):
    w = re.findall(r"[a-z0-9']+", t.lower())
    return {tuple(w[k:k + n]) for k in range(len(w) - n + 1)}


def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = [f for pat in files for f in sorted(glob.glob(pat))]
    recs = [json.loads(line) for f in files for line in open(f, encoding="utf-8") if line.strip()]
    lanes = collections.defaultdict(dict)
    for r in recs:
        lanes[(r["model"], r["arm"], r["lane"])][r["t"]] = r
    cells = collections.defaultdict(list)
    for (model, arm, lane) in sorted(lanes):
        cells[(model, arm)].append(lanes[(model, arm, lane)])

    for (model, arm), ls in sorted(cells.items()):
        rows = [r for lane in ls for r in lane.values()]
        ok = [r for r in rows if r.get("text")]
        T = max(r["t"] for r in rows)
        print("== %s | %s: lanes=%d hops=%d calls=%d" % (model, arm, len(ls), T, len(rows)))
        print("   survival: parsed %d, rule unchanged %d, nothing outside object %d, errors %d (of %d)"
              % (sum(1 for r in rows if r.get("parsed")), sum(1 for r in rows if r.get("rule_ok")),
                 sum(1 for r in rows if r.get("bare")), sum(1 for r in rows if r.get("error")), len(rows)))
        print("   paragraph words: mean %.0f | extra keys: %s"
              % (mean(len(r["text"].split()) for r in ok),
                 dict(collections.Counter(tuple(k for k in (r.get("keys") or []) if k not in ("rule", "notes", "text"))
                                          for r in rows if r.get("keys")).most_common(3))))
        for t in (1, 2, 5, 10, 15, 20):
            ns = [lane[t].get("notes") or "" for lane in ls if t in lane]
            if ns:
                print("   notes at hop %2d: non-empty in %d of %d lanes, words %s"
                      % (t, sum(1 for n in ns if n.strip()), len(ns), [len(n.split()) for n in ns]))

        def div(t0, t1, fn):
            vals = []
            for t in range(t0, t1 + 1):
                texts = [lane[t]["text"] for lane in ls if t in lane and lane[t].get("text")]
                vals += [jac(fn(a), fn(b)) for a, b in itertools.combinations(texts, 2)]
            return mean(vals)
        print("   between lanes, content-word Jaccard: hops 1-5 %.3f | 6-10 %.3f | 10-20 %.3f ; 3-gram, hops 10-20 %.4f"
              % (div(1, 5, content), div(6, 10, content), div(10, 20, content), div(10, 20, grams)))
        lag1, lag2, near, exact = [], [], [], 0
        for lane in ls:
            seq = [lane[t]["text"] for t in sorted(lane) if lane[t].get("text")]
            cs = [content(x) for x in seq]
            lag1 += [jac(cs[i], cs[i - 1]) for i in range(1, len(cs))]
            lag2 += [jac(cs[i], cs[i - 2]) for i in range(2, len(cs))]
            near += [max(jac(cs[i], cs[j]) for j in range(i)) for i in range(3, len(cs))]
            exact += len(seq) - len(set(seq))
        print("   within lane, content-word Jaccard: to previous hop %.3f | to two hops back %.3f | nearest earlier %.3f | exact repeats %d"
              % (mean(lag1), mean(lag2), mean(near), exact))
        print("   paragraphs containing: " + ", ".join("%s %d" % (k, sum(1 for r in ok if re.search(p, r["text"])))
                                                       for k, p in MOTIFS.items()) + " (of %d)" % len(ok))
        both = lambda r: (r.get("text") or "") + " " + (r.get("notes") or "")
        print("   environment string in text or notes: %d | symmetry language in notes: %d, in text: %d"
              % (sum(1 for r in ok if ENV.search(both(r))), sum(1 for r in ok if SYMM.search(r.get("notes") or "")),
                 sum(1 for r in ok if SYMM.search(r["text"]))))
        opens = collections.Counter(" ".join(r["text"].split()[:3]).lower() for r in ok)
        print("   repeated 3-word openings:", [(o, k) for o, k in opens.most_common(5) if k > 2])
        if "--notes" in sys.argv:
            for i, lane in enumerate(ls):
                for t in (1, 2, 5, 10, 20):
                    if t in lane:
                        print("   [notes lane %d hop %2d] %s" % (i, t, (lane[t].get("notes") or "").replace("\n", " ")[:380]))
        if "--texts" in sys.argv:
            for i, lane in enumerate(ls):
                for t in (1, 5, 10, 15, 20):
                    if t in lane and lane[t].get("text"):
                        print("   [text lane %d hop %2d] %s" % (i, t, lane[t]["text"].replace("\n", " ")[:200]))
        print()


if __name__ == "__main__":
    main()
