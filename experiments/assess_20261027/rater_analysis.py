"""Compare the blind rater (analysis/rater.jsonl) with the models' self-scores (runs/*/steps.jsonl).
Writes analysis/rater_summary.json and prints a summary. Run from the repo root after rate.py.
"""
import io, json, math, os, re, statistics
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
INIT = json.load(io.open(os.path.join(HERE, "inits", "assess.json"), encoding="utf-8"))
QUAL = list(INIT["qualities"])
PAIRS = [("floridity", "economy"), ("relatability", "strangeness"), ("grounding", "scope"), ("coherence", "surprise")]


def parse(out):
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", out.strip())
    try:
        d = json.loads(s)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def corr(x, y):
    n = len(x)
    if n < 5:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((v - mx) ** 2 for v in x)); sy = math.sqrt(sum((v - my) ** 2 for v in y))
    if sx == 0 or sy == 0:
        return None
    return round(sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy), 3)


def main():
    rater = defaultdict(dict)
    for l in io.open(os.path.join(HERE, "analysis", "rater.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if r.get("scores") and all(isinstance(r["scores"].get(q), (int, float)) for q in QUAL):
            rater[r["run"]][r["t"]] = r
    res = {}
    allq = defaultdict(list)
    for run in sorted(rater):
        recs = [json.loads(l) for l in io.open(os.path.join(HERE, "runs", run, "steps.jsonl"), encoding="utf-8")]
        objs = {r["t"]: parse(r["out"]) for r in recs if "out" in r}
        T = max(objs)
        agree = tied = n = 0
        rose = same = fell = 0
        rs = {q: [] for q in QUAL}; ss = {q: [] for q in QUAL}
        chosen_rows = []
        for t in range(1, T + 1):
            o = objs.get(t); rr = rater[run].get(t)
            if not o or not rr or not o.get("scores"):
                continue
            s = o["scores"]
            if not all(isinstance(s.get(q), (int, float)) for q in QUAL):
                continue
            n += 1
            for q in QUAL:
                rs[q].append(rr["scores"][q]); ss[q].append(s[q]); allq[q].append(rr["scores"][q])
            mn = min(s[q] for q in QUAL); tiedset = {q for q in QUAL if s[q] == mn}
            if rr["weakest"] == o.get("weakest"): agree += 1
            if rr["weakest"] in tiedset: tied += 1
            h = o.get("history") or []
            ch = h[-1] if h else None
            prev = rater[run].get(t - 1)
            if ch in QUAL and prev:
                d = rr["scores"][ch] - prev["scores"][ch]
                chosen_rows.append((t, ch, prev["scores"][ch], rr["scores"][ch]))
                if d > 0: rose += 1
                elif d == 0: same += 1
                else: fell += 1
        rater_pairs = {"%s/%s" % (a, b): corr(rs[a], rs[b]) for a, b in PAIRS}
        rater_vs_self = {q: corr(rs[q], ss[q]) for q in QUAL}
        mean_r = {q: round(statistics.mean(rs[q]), 2) for q in QUAL if rs[q]}
        mean_s = {q: round(statistics.mean(ss[q]), 2) for q in QUAL if ss[q]}
        k = min(10, len(rs["coherence"]))
        traj = {q: (round(statistics.mean(rs[q][:k]), 2), round(statistics.mean(rs[q][-k:]), 2)) for q in QUAL if rs[q]}
        rmin = [min(rs[q][i] for q in QUAL) for i in range(len(rs["coherence"]))]
        rweak = Counter(rater[run][t]["weakest"] for t in rater[run])
        res[run] = {"rated_hops": n, "weakest_agree_exact": agree, "weakest_agree_within_ties": tied,
                    "bolstered_quality_rater_rose_same_fell": [rose, same, fell],
                    "rater_pair_corr": rater_pairs, "rater_vs_self_corr_per_quality": rater_vs_self,
                    "rater_mean": mean_r, "self_mean": mean_s, "rater_first10_last10": traj,
                    "rater_min_mean": round(statistics.mean(rmin), 2) if rmin else None,
                    "rater_weakest_counts": dict(rweak.most_common())}
    res["_rater_overall_mean"] = {q: round(statistics.mean(allq[q]), 2) for q in QUAL if allq[q]}
    io.open(os.path.join(HERE, "analysis", "rater_summary.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1))
    for run, r in res.items():
        if run.startswith("_"):
            print("rater overall mean per quality:", r); continue
        print("=== %s: rated %d; weakest agrees exact %d, within ties %d; bolstered quality rose/same/fell %s" % (
            run, r["rated_hops"], r["weakest_agree_exact"], r["weakest_agree_within_ties"], r["bolstered_quality_rater_rose_same_fell"]))
        print("  rater pair corr", r["rater_pair_corr"])
        print("  rater vs self per quality", r["rater_vs_self_corr_per_quality"])
        print("  rater mean", r["rater_mean"]); print("  self  mean", r["self_mean"])
        print("  rater first10->last10", r["rater_first10_last10"]); print("  rater weakest counts", r["rater_weakest_counts"], "rater min mean", r["rater_min_mean"])


if __name__ == "__main__":
    main()
