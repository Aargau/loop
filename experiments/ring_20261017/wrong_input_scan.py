#!/usr/bin/env python
"""wrong_input_scan.py: does any cell's output at hop t look like a rewrite of ANOTHER cell's text at hop t-1?

  python experiments/ring_20261017/wrong_input_scan.py experiments/ring_20261017/runs

A cell's output should be closest to its own previous text. A cell that was handed another cell's answer is instead
closest to that other cell's previous text. Similarity is Jaccard over word 3-grams. A cell is flagged when another
cell's previous text matches its output more than twice as well as its own does (and above 0.08), and the two
previous texts are not identical. Calls slower than 1.8 times the run's median latency are listed beside each flag,
because a retry after a missing output file roughly doubles a call's latency.

The test cannot see a swap between two cells whose previous texts are alike (two untouched kitchen cells), so the
count is a floor. Written 2026-11-09 to check the ring runs after the Codex output-file collision was found; see
CONTAMINATION.md in this directory.
"""
import json
import os
import re
import statistics
import sys


def grams(text, n=3):
    words = re.findall(r"[a-z']+", text.lower())
    return {tuple(words[k:k + n]) for k in range(len(words) - n + 1)}


def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def scan(path):
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    n = len(rows[0]["cells"])
    lats = [c.get("latency") for r in rows[1:] for c in r["cells"] if c.get("latency") is not None]
    med = statistics.median(lats) if lats else None
    flags = []
    slow_hops = {}
    for r in rows[1:]:
        for c in r["cells"]:
            if med and c.get("latency") and c["latency"] > 1.8 * med:
                slow_hops.setdefault(r["t"], []).append((c["i"], c["latency"]))
    for t in range(1, len(rows)):
        prev = [grams(c["text"]) for c in rows[t - 1]["cells"]]
        for i, c in enumerate(rows[t]["cells"]):
            out = grams(c["text"])
            sims = [jac(out, p) for p in prev]
            best = max(range(n), key=lambda j: sims[j])
            if best != i and sims[best] > 0.08 and sims[best] > 2.0 * sims[i] and prev[best] != prev[i]:
                flags.append((t, i, best, round(sims[i], 3), round(sims[best], 3)))
    return n, len(rows) - 1, med, flags, slow_hops


def main():
    root = sys.argv[1]
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name, "ring.jsonl")
        if not os.path.exists(path):
            continue
        n, hops, med, flags, slow = scan(path)
        nslow = sum(len(v) for v in slow.values())
        print("== %s  cells=%d hops=%d median_latency=%s slow_calls=%d flagged=%d" % (name, n, hops, med, nslow, len(flags)))
        for t, i, best, own, other in flags:
            print("   t=%2d cell %d looks like a rewrite of cell %d's previous text (own %.3f, other %.3f); slow calls this hop: %s"
                  % (t, i, best, own, other, slow.get(t, [])))
        unexplained = sorted(t for t in slow if t not in {f[0] for f in flags})
        if unexplained:
            print("   slow-call hops with no flagged cell:", unexplained)


if __name__ == "__main__":
    main()
