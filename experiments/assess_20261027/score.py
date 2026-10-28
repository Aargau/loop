"""Score the assess-and-bolster runs: object survival, chosen-quality sequence, self-score dynamics,
pair correlations, length, drift. Writes analysis/scores.json and prints a summary.
Run from the repo root: python experiments/assess_20261027/score.py
"""
import io, json, math, os, re, statistics, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
INIT = json.load(io.open(os.path.join(HERE, "inits", "assess.json"), encoding="utf-8"))
QUAL = list(INIT["qualities"])
PAIRS = [("floridity", "economy"), ("relatability", "strangeness"), ("grounding", "scope"), ("coherence", "surprise")]
SEED = "The sun was setting behind the hills."
STOP = set("the a an and or of to in on at by for with from as is was were be been it its he she they them his her their this that these those not no but so if then than into over under up down out off about".split())


def parse(out):
    s = out.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    try:
        d = json.loads(s)
        return d if isinstance(d, dict) else None
    except Exception:
        # last resort: first {...} block
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                d = json.loads(m.group(0))
                return d if isinstance(d, dict) else None
            except Exception:
                return None
        return None


def words(t):
    return re.findall(r"[A-Za-z']+", t.lower())


def content(t):
    return set(w for w in words(t) if w not in STOP and len(w) > 2)


def jacc(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def corr(x, y):
    n = len(x)
    if n < 5:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((v - mx) ** 2 for v in x)); sy = math.sqrt(sum((v - my) ** 2 for v in y))
    if sx == 0 or sy == 0:
        return None
    return round(sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy), 3)


def period_of(seq, maxp=16):
    """Smallest p such that seq[i] == seq[i-p] for the last 2*p elements at least, checked over the last 30."""
    tail = seq[-30:]
    for p in range(1, maxp + 1):
        if len(tail) < 2 * p:
            break
        if all(tail[i] == tail[i - p] for i in range(p, len(tail))):
            return p
    return None


def entropy(c):
    n = sum(c.values())
    return round(-sum(v / n * math.log2(v / n) for v in c.values() if v), 3) if n else None


def score_run(name):
    recs = [json.loads(l) for l in io.open(os.path.join(RUNS, name, "steps.jsonl"), encoding="utf-8")]
    recs = [r for r in recs if "out" in r]
    T = len(recs)
    objs = [parse(r["out"]) for r in recs]
    parsed = [o is not None for o in objs]
    rule_ok = [o is not None and o.get("rule") == INIT["rule"] for o in objs]
    qual_ok = [o is not None and o.get("qualities") == INIT["qualities"] for o in objs]
    fenced = [r["out"].strip().startswith("```") for r in recs]
    texts = [(o.get("text", "") if o else "") for o in objs]
    # chosen quality at hop t = last element of history if history grew by one
    chosen, hist_ok = [], []
    prev_len = 0
    for o in objs:
        h = (o or {}).get("history") or []
        ok = isinstance(h, list) and len(h) == prev_len + 1
        hist_ok.append(ok)
        chosen.append(h[-1] if h else None)
        prev_len = len(h) if isinstance(h, list) else prev_len
    scores = [((o or {}).get("scores") or {}) for o in objs]
    valid = [all(isinstance(s.get(q), (int, float)) for q in QUAL) for s in scores]
    weakest = [(o or {}).get("weakest") for o in objs]
    # does the declared weakest match the min of the scores (ties allowed)?
    weak_consistent = []
    for s, w, v in zip(scores, weakest, valid):
        if not v:
            weak_consistent.append(None); continue
        mn = min(s[q] for q in QUAL)
        weak_consistent.append(w in QUAL and s.get(w) == mn)
    # does hop t+1 bolster what hop t declared weakest?
    obeyed = []
    for t in range(1, T):
        if weakest[t - 1] in QUAL and chosen[t] is not None:
            obeyed.append(chosen[t] == weakest[t - 1])
    wc = [len(words(t)) for t in texts]
    in_band = sum(1 for w in wc if 200 <= w <= 320)
    mins = [min(s[q] for q in QUAL) if v else None for s, v in zip(scores, valid)]
    meds = [statistics.median(s[q] for q in QUAL) if v else None for s, v in zip(scores, valid)]
    first_min3 = next((t + 1 for t, m in enumerate(mins) if m is not None and m >= 3 and all(x is not None and x >= 3 for x in mins[t:])), None)
    coh5 = sum(1 for s, v in zip(scores, valid) if v and s["coherence"] == 5)
    pair_corr = {}
    for a, b in PAIRS:
        xs = [s[a] for s, v in zip(scores, valid) if v]; ys = [s[b] for s, v in zip(scores, valid) if v]
        pair_corr["%s/%s" % (a, b)] = corr(xs, ys)
    cnt = Counter(c for c in chosen if c in QUAL)
    never = [q for q in QUAL if cnt[q] == 0]
    c0 = content(texts[0]) if texts else set()
    drift = {str(k): (round(jacc(c0, content(texts[k - 1])), 3) if T >= k else None) for k in (10, 30, 60)}
    seed_alive = [SEED.lower() in t.lower() for t in texts]
    exact_rep = sum(1 for i in range(1, T) if texts[i] and texts[i] == texts[i - 1])
    text_period = period_of(texts) if T >= 10 else None
    # 2-cycle in text: Jaccard lag-2 vs lag-1 over last 30
    cs = [content(t) for t in texts]
    lag1 = [jacc(cs[i], cs[i - 1]) for i in range(max(1, T - 30), T)]
    lag2 = [jacc(cs[i], cs[i - 2]) for i in range(max(2, T - 30), T)]
    out = {
        "hops": T, "parsed": sum(parsed), "rule_unchanged": sum(rule_ok), "qualities_unchanged": sum(qual_ok), "fenced": sum(fenced),
        "scores_valid": sum(valid), "history_grew_by_one": sum(hist_ok), "weakest_matches_min": sum(1 for x in weak_consistent if x),
        "next_hop_obeyed_weakest": "%d/%d" % (sum(obeyed), len(obeyed)),
        "chosen_counts": dict(cnt.most_common()), "never_chosen": never, "chosen_entropy_bits": entropy(cnt),
        "chosen_period_last30": period_of([c for c in chosen]), "chosen_seq": chosen,
        "min_self_score": mins, "median_self_score": meds, "min_at_or_above_3_from_hop": first_min3,
        "coherence_5_hops": coh5, "self_pair_corr": pair_corr,
        "words": wc, "words_in_band_200_320": in_band, "words_sd_last30": round(statistics.pstdev(wc[-30:]), 1) if T >= 30 else None,
        "drift_jaccard_to_hop1": drift, "seed_sentence_alive_hops": sum(seed_alive), "seed_alive_at_end": seed_alive[-1] if seed_alive else None,
        "exact_text_repeats": exact_rep, "text_period_last30": text_period,
        "jacc_lag1_mean_last30": round(sum(lag1) / len(lag1), 3) if lag1 else None, "jacc_lag2_mean_last30": round(sum(lag2) / len(lag2), 3) if lag2 else None,
        "tok_in": sum(r.get("tok_in") or 0 for r in recs), "tok_out": sum(r.get("tok_out") or 0 for r in recs),
        "notes": [(o or {}).get("note", "") for o in objs],
    }
    return out


def main():
    names = sorted(d for d in os.listdir(RUNS) if os.path.isdir(os.path.join(RUNS, d)))
    res = {n: score_run(n) for n in names}
    os.makedirs(os.path.join(HERE, "analysis"), exist_ok=True)
    io.open(os.path.join(HERE, "analysis", "scores.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, ensure_ascii=False))
    for n, r in res.items():
        print("=== %s: %d hops, parsed %d, rule %d, qualities %d, fenced %d, scores valid %d, history ok %d" % (
            n, r["hops"], r["parsed"], r["rule_unchanged"], r["qualities_unchanged"], r["fenced"], r["scores_valid"], r["history_grew_by_one"]))
        print("  chosen:", r["chosen_counts"], "never:", r["never_chosen"], "entropy", r["chosen_entropy_bits"], "period", r["chosen_period_last30"])
        print("  obeyed weakest:", r["next_hop_obeyed_weakest"], " weakest==min:", r["weakest_matches_min"], " coherence=5 on", r["coherence_5_hops"])
        print("  min score >=3 from hop", r["min_at_or_above_3_from_hop"], " self pair corr", r["self_pair_corr"])
        print("  words in band", r["words_in_band_200_320"], "sd30", r["words_sd_last30"], " drift", r["drift_jaccard_to_hop1"], " seed alive", r["seed_sentence_alive_hops"], "end", r["seed_alive_at_end"])
        print("  exact repeats", r["exact_text_repeats"], "text period", r["text_period_last30"], "lag1/lag2", r["jacc_lag1_mean_last30"], r["jacc_lag2_mean_last30"], "tok", r["tok_in"], r["tok_out"])
        print("  seq:", " ".join((c or "?")[:4] for c in r["chosen_seq"]))


if __name__ == "__main__":
    main()
