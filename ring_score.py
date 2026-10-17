#!/usr/bin/env python
"""ring_score.py: provenance tags, symmetry breaking and a space-time diagram (SVG) for a ring.py run.

  python ring_score.py experiments/ring_20261017/runs/cerebras_qwen_n7

Three provenance layers, each tagged by the cell where the unit first appeared (hop 0 tags are the seeds: cell 0 is
the disturbed seed, every other cell the plain seed, so plain-seed units are tagged "plain" and only units born in a
cell after hop 0, or in the disturbed seed, carry a cell tag):
  1. exact 4-grams (copies; die under paraphrase)
  2. distinctive content words and capitalised names (survive paraphrase while the word does)
  3. symmetry: cells equidistant from cell 0 are compared hop by hop; the first hop at which a mirror pair differs
     is the disturbance's arrival, tag-free.
Per cell: freeze hop (first hop from which the text never changes again), exact recurrence of the whole ring state.
Writes <run>/score.json, <run>/spacetime.svg (one row per hop, one column per cell, cell colour = dominant origin
tag of its distinctive words, with a bar for the share of its 4-grams copied from each neighbour) and prints a summary.
"""
import collections, io, json, os, re, sys
STOP = set("""the and that with from this were have been there their they them which would could when what into over
after about through where while those these than then into onto upon its his her she he it was had has not but for
off out one two three four five six seven eight nine ten down back away again still just only also very more most
some such each every both few many much own same other another any all will can did does done said says like
himself herself itself then once here where""".split())
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]+")
PAL = ["#b5543c", "#2f6f8f", "#5a8f3c", "#8f5a9a", "#c48a2a", "#3c8f8a", "#8f3c5a", "#5a5a8f", "#8f7a3c", "#3c5a8f"]


def words(text):
    return [w.lower() for w in WORD.findall(text)]


def content(text):
    return [w for w in words(text) if len(w) >= 4 and w not in STOP]


def names(text):
    return [w for w in re.findall(r"\b[A-Z][a-z]{2,}\b", text) if w.lower() not in STOP]


def grams(text, n=4):
    w = words(text)
    return [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]


def main(run):
    hops = [json.loads(l) for l in io.open(os.path.join(run, "ring.jsonl"), encoding="utf-8")]
    N = len(hops[0]["cells"]); T = len(hops) - 1
    texts = [[c["text"] for c in hp["cells"]] for hp in hops]
    # origin tags
    origin_w, origin_g = {}, {}
    plain = set(content(texts[0][1])) | set(w.lower() for w in names(texts[0][1])) if N > 1 else set()
    for w in plain: origin_w[w] = "plain"
    for g in grams(texts[0][1]): origin_g[g] = "plain"
    for w in set(content(texts[0][0])) | set(w.lower() for w in names(texts[0][0])):
        origin_w.setdefault(w, 0)
    for g in grams(texts[0][0]): origin_g.setdefault(g, 0)
    cellrows = []
    for t in range(1, T + 1):
        row = []
        for i in range(N):
            cw = set(content(texts[t][i])) | set(w.lower() for w in names(texts[t][i])); cg = set(grams(texts[t][i]))
            for w in cw: origin_w.setdefault(w, i)
            for g in cg: origin_g.setdefault(g, i)
            tags = collections.Counter(origin_w[w] for w in cw)
            gtags = collections.Counter(origin_g[g] for g in cg)
            # copied from neighbours: 4-grams present in the neighbour's previous text
            L, R = texts[t - 1][(i - 1) % N], texts[t - 1][(i + 1) % N]
            gl, gr = set(grams(L)), set(grams(R))
            own_prev = set(grams(texts[t - 1][i]))
            newg = cg - own_prev                       # 4-grams this hop that were not already the cell's own
            own = len(cg & own_prev) / max(1, len(cg))
            from_left = len(newg & gl) / max(1, len(newg)) if newg else 0.0
            from_right = len(newg & gr) / max(1, len(newg)) if newg else 0.0
            dom = max(tags.items(), key=lambda kv: (kv[1], str(kv[0])))[0] if tags else "plain"
            row.append({"i": i, "t": t, "words": len(words(texts[t][i])), "tags": {str(k): v for k, v in tags.items()}, "dominant": str(dom),
                        "gram_tags": {str(k): v for k, v in gtags.items()}, "copied_from_left": round(from_left, 3), "copied_from_right": round(from_right, 3),
                        "kept_own_grams": round(own, 3), "same_as_prev": texts[t][i] == texts[t - 1][i], "names": names(texts[t][i])})
        cellrows.append(row)
    # freeze hops
    freeze = []
    for i in range(N):
        f = None
        for t in range(1, T + 1):
            if all(texts[u][i] == texts[t][i] for u in range(t, T + 1)):
                f = t; break
        freeze.append(f)
    # whole-ring recurrence
    seen = {}; ring_rec = None
    for t in range(0, T + 1):
        k = tuple(c["hash"] for c in hops[t]["cells"])
        if k in seen: ring_rec = (t, seen[k]); break
        seen[k] = t
    # symmetry: mirror pairs (i, N-i)
    mirror = {}
    for i in range(1, (N - 1) // 2 + 1):
        j = (N - i) % N
        if j == i: continue
        first = next((t for t in range(1, T + 1) if texts[t][i] != texts[t][j]), None)
        mirror["%d|%d" % (i, j)] = first
    # travel: first hop each cell contains a cell-0-origin word (distance from the seed)
    arrival = []
    for i in range(N):
        a = next((t for t in range(1, T + 1) if cellrows[t - 1][i]["tags"].get("0", 0) > 0), None)
        arrival.append(a)
    score = {"run": os.path.basename(run.rstrip("/\\")), "cells": N, "hops": T, "freeze_hop": freeze, "ring_recurrence": ring_rec,
             "mirror_first_divergence": mirror, "first_hop_with_cell0_words": arrival,
             "mean_copied_from_neighbours": round(sum(c["copied_from_left"] + c["copied_from_right"] for r in cellrows for c in r) / max(1, N * T), 3),
             "mean_kept_own_grams": round(sum(c["kept_own_grams"] for r in cellrows for c in r) / max(1, N * T), 3),
             "words_range": [min(c["words"] for r in cellrows for c in r), max(c["words"] for r in cellrows for c in r)],
             "unparsed_hops": sum(1 for hp in hops[1:] for c in hp["cells"] if not c.get("parsed", True)),
             "errors": sum(1 for hp in hops[1:] for c in hp["cells"] if c.get("error")), "rows": cellrows}
    json.dump(score, io.open(os.path.join(run, "score.json"), "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    # svg
    cw, ch, left, top = 28, 10, 40, 30
    W, H = left + N * cw + 160, top + (T + 1) * ch + 20
    def col(tag):
        if tag == "plain": return "#dddddd"
        try: return PAL[int(tag) % len(PAL)]
        except Exception: return "#999999"
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="sans-serif" font-size="9">' % (W, H),
           '<rect width="100%%" height="100%%" fill="white"/>',
           '<text x="%d" y="14">%s: %d cells, %d hops. Colour = origin cell of the dominant distinctive words (grey = plain seed); inner bar = share of the new 4-grams (not in the cell itself at the previous hop) that were in the previous text of the left (dark) or right (light) neighbour; black dot = unchanged from previous hop.</text>' % (left, score["run"], N, T)]
    for i in range(N):
        out.append('<text x="%d" y="%d" text-anchor="middle">%d</text>' % (left + i * cw + cw / 2, top - 4, i))
    for t in range(0, T + 1):
        y = top + t * ch
        if t % 5 == 0: out.append('<text x="%d" y="%d" text-anchor="end">%d</text>' % (left - 4, y + ch - 2, t))
        for i in range(N):
            x = left + i * cw
            if t == 0:
                out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="white"/>' % (x, y, cw, ch, col("0" if i == 0 else "plain")))
                continue
            c = cellrows[t - 1][i]
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="white"/>' % (x, y, cw, ch, col(c["dominant"])))
            bl = int(cw * 0.9 * c["copied_from_left"]); br = int(cw * 0.9 * c["copied_from_right"])
            if bl: out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#000" opacity="0.55"/>' % (x + 1, y + ch - 4, bl, 3))
            if br: out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#fff" opacity="0.8"/>' % (x + cw - 1 - br, y + 1, br, 3))
            if c["same_as_prev"]: out.append('<circle cx="%d" cy="%d" r="2" fill="#000"/>' % (x + cw / 2, y + ch / 2))
    ly = top
    for k, lab in [("0", "cell 0 (disturbed seed)"), ("plain", "plain seed")] + [(str(i), "born in cell %d" % i) for i in range(1, N)]:
        out.append('<rect x="%d" y="%d" width="10" height="10" fill="%s"/><text x="%d" y="%d">%s</text>' % (left + N * cw + 10, ly, col(k), left + N * cw + 24, ly + 9, lab)); ly += 13
    out.append("</svg>")
    io.open(os.path.join(run, "spacetime.svg"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("%s: N=%d T=%d | freeze hop per cell %s | ring recurrence %s | mirror divergence %s | cell-0 words first seen per cell %s | copied from neighbours %.3f | kept own 4-grams %.3f | words %s | unparsed %d errors %d" % (
        score["run"], N, T, freeze, ring_rec, mirror, arrival, score["mean_copied_from_neighbours"], score["mean_kept_own_grams"], score["words_range"], score["unparsed_hops"], score["errors"]))
    print("wrote score.json and spacetime.svg")


if __name__ == "__main__":
    for r in sys.argv[1:]:
        main(r)
