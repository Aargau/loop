#!/usr/bin/env python
"""ring_affect_check.py: ring_affect.py must reproduce the first ring pilot (experiments/ring_20261017/PROTOCOL.md).

  python ring_affect_check.py

Scores experiments/ring_20261017/runs/cerebras_qwen_n7 with a synthetic anchors file (one disturbance, "mill", anchor
"lit shingles under the arch", kind fact) and asserts: (1) arrival is one cell per hop in both directions from cell 0,
the fronts meeting at the antipode (cells 3 and 4) by hop 3-4, i.e. arrival[i] == ring distance from cell 0 and the
velocity is 1.0; (2) per-cell freeze hops equal the run's score.json; plus the recurrence and the mechanism (every cell
the anchor reached holds it verbatim as its last sentence). Prints PASS/FAIL per assertion with the numbers; exit 1 on
any FAIL. Writes experiments/ring_affect_20261107/check_anchors_mill.json and the run's affect.json/affect.svg.
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ring_affect

RUN = os.path.join(HERE, "experiments", "ring_20261017", "runs", "cerebras_qwen_n7")
ANCH = os.path.join(HERE, "experiments", "ring_affect_20261107", "check_anchors_mill.json")
PLAIN = os.path.join(HERE, "experiments", "ring_20261017", "seeds", "plain.txt")
SYN = {"mill": {"anchor": "lit shingles under the arch", "kind": "fact", "seed": "disturb.txt"},
       "background": {"seed": "plain.txt", "lexicon_calm": ["warm", "quiet", "waited", "wiped", "counted", "tick", "ticked", "ticking", "good cups", "twenty past seven"]},
       "cause_nouns_watch": "any capitalised name or concrete noun (letter, phone, call, telegram, doctor, hospital, news, knock, door)"}


def main():
    json.dump(SYN, io.open(ANCH, "w", encoding="utf-8", newline="\n"), indent=1)
    if not os.path.exists(PLAIN): PLAIN_ = ring_affect.DEF_PLAIN
    else: PLAIN_ = PLAIN
    out = ring_affect.main(RUN, ANCH, PLAIN_)
    N = out["cells"]; m = out["disturbances"]["mill"]; fails = 0

    def check(name, ok, detail):
        nonlocal fails
        fails += 0 if ok else 1
        print("%s  %s: %s" % ("PASS" if ok else "FAIL", name, detail))

    expect = [ring_affect.ringdist(i, 0, N) for i in range(N)]
    check("placement", out["placements"] == {"0": "mill"}, "placements %s (want {'0': 'mill'})" % out["placements"])
    check("arrival front (one cell per hop both ways)", m["arrival"] == expect, "arrival %s, ring distance %s" % (m["arrival"], expect))
    anti = [i for i in range(N) if expect[i] == max(expect)]
    check("fronts meet at antipode by hop 3-4", all(m["arrival"][i] is not None and 3 <= m["arrival"][i] <= 4 for i in anti), "antipode cells %s arrive at %s" % (anti, [m["arrival"][i] for i in anti]))
    check("velocity 1.0 cells/hop", m["velocity"] == 1.0, "velocity %s intercept %s n=%d" % (m["velocity"], m["velocity_fit"]["intercept"], m["velocity_fit"]["n"]))
    score = json.load(io.open(os.path.join(RUN, "score.json"), encoding="utf-8"))
    check("freeze hops equal score.json", out["freeze_hop"] == score["freeze_hop"], "affect %s score %s" % (out["freeze_hop"], score["freeze_hop"]))
    check("ring recurrence equals score.json", list(out["ring_recurrence"] or []) == list(score["ring_recurrence"] or []), "affect %s score %s" % (out["ring_recurrence"], score["ring_recurrence"]))
    check("soliton is verbatim and edge-promoted on arrival", all(m["anchor_exact_first"][i] == m["arrival"][i] and m["edge_promoted_first"][i] == m["arrival"][i] for i in range(1, N)),
          "exact first %s, edge promoted first %s, fuzzy-only cells %s" % (m["anchor_exact_first"], m["edge_promoted_first"], m["fuzzy_only_cells"]))
    check("lifetime is the last hop", m["lifetime"] == out["hops"], "lifetime %s of %d hops" % (m["lifetime"], out["hops"]))
    print("%d FAIL" % fails if fails else "ALL PASS")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
