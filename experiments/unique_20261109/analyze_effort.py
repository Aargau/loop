"""Low against high effort on the clause arm: the measures fixed in predictions_effort.md.

Usage: python -B analyze_effort.py <effort_file.jsonl> [...]   (add --show to print every output's first 420 chars)
"""
import collections
import itertools
import json
import re
import sys

from analyze_unique import grams, jac, ids_in

SHARED = ["954e423f", "46fcc71f", "c517e291", "30d50430", "30d5", "7a35", "4c82", "afc4", "bb872"]
SYMMETRY = re.compile(r"same (prompt|weights|instincts|model|training)|every (instance|copy)|other instances|"
                      r"each instance|all (of us|instances)|share[sd]? (my|the same|our)|converge", re.I)
MOTIFS = {"municipal": r"\bmunicipal", "spoon": r"spoon", "lighthouse": r"lighthouse", "heron": r"\bherons?\b",
          "ledger": r"\bledgers?\b", "cartographer": r"cartograph", "retired": r"\bretired\b",
          "seventeen": r"\b17\b|seventeen|:17\b", "game in text": r"instances?|other versions?|another version|duplicates?|"
          r"other applicants|identical strangers|same prompt|same weights|strangers were"}


def own_id_used(rec):
    sid = rec.get("session") or ""
    if not sid:
        return False
    parts = [p for p in sid.split("-") if len(p) >= 4]
    return any(p in rec["text"] for p in parts)


def main():
    show = "--show" in sys.argv
    recs = []
    for path in [a for a in sys.argv[1:] if not a.startswith("--")]:
        recs += [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    cells = collections.defaultdict(list)
    for r in recs:
        if r.get("text"):
            cells[(r["model"], r["effort"])].append(r)
    ids_seen = collections.defaultdict(list)
    for key in sorted(cells):
        rs = cells[key]
        n = len(rs)
        g = [grams(r["text"]) for r in rs]
        pairs = list(itertools.combinations(range(n), 2))
        lex = sum(jac(g[a], g[b]) for a, b in pairs) / max(1, len(pairs))
        env = [any(s in r["text"] for s in SHARED) or own_id_used(r) for r in rs]
        own = [own_id_used(r) for r in rs]
        shared_only = [e and not o for e, o in zip(env, own)]
        sym = [bool(SYMMETRY.search(r["text"])) for r in rs]
        think = [r.get("tok_thinking") for r in rs if r.get("tok_thinking") is not None]
        words = sum(len(r["text"].split()) for r in rs) / n
        lat = sum(r["latency"] for r in rs) / n
        print("== %s effort %s: n=%d words=%.0f latency=%.0fs thinking_tokens=%s | 3-gram J=%.4f"
              % (key[0], key[1], n, words, lat, (round(sum(think) / len(think)) if think else "n/a"), lex))
        print("   environment string used %d | own session id in text %d | shared strings only %d | symmetry argument stated %d"
              % (sum(env), sum(own), sum(shared_only), sum(sym)))
        print("   motifs: " + ", ".join("%s %d" % (name, sum(1 for r in rs if re.search(pat, r["text"])))
                                          for name, pat in MOTIFS.items()))
        cell_ids = collections.Counter(tok for r in rs for tok in ids_in(r["text"]))
        for tok in cell_ids:
            ids_seen[tok].append(key)
        opens = collections.Counter(" ".join(r["text"].split()[:3]).lower() for r in rs)
        print("   repeated 3-word openings:", [(o, k) for o, k in opens.most_common(4) if k > 1])
        if show:
            for r in rs:
                print("   -- %s %02d own=%s: %s" % (r["effort"], r["i"], own_id_used(r),
                                                  r["text"].strip().replace("\n", " ")[:420]))
    rep = collections.Counter()
    for r in recs:
        for tok in ids_in(r.get("text") or ""):
            rep[(r["model"], tok)] += 1
    print()
    print("identifier strings in more than one output (model, string, outputs):",
          sorted(((m, t, k) for (m, t), k in rep.items() if k > 1), key=lambda x: -x[2])[:20] or "none")


if __name__ == "__main__":
    main()
