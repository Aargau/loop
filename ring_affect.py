#!/usr/bin/env python
"""ring_affect.py: fact vs. affect as a propagating disturbance in a ring.py run (experiments/ring_affect_20261107/BRIEF.md).

  python ring_affect.py <run_dir> [--anchors PATH] [--plain PATH]

Per hop, per cell, per disturbance in anchors.json (entries with an "anchor"; "background" gives the calm lexicon):
  anchor_exact    verbatim anchor present (case-insensitive, whitespace-normalised, straight apostrophes)
  anchor_fuzzy    fraction of the anchor's content words present (words of 3+ letters not in ring_score.STOP and not in
                  plain.txt, so "kettle" in the panic anchor does not score every kitchen)
  lexicon         lex = non-overlapping hits of the emotion's lexicon (word-boundary, inflections allowed), lex60 = per 60
                  words, lex_entries = raw count per entry; calm/calm60 likewise for the background lexicon
  edge_promoted   the cell's last sentence (ring.py's sentence split) holds the anchor, exact or fuzzy >= 0.5
  cause_supplied  a mid-sentence capitalised name or a watch-list noun, absent from plain.txt and from the cell's previous
                  text, within one hop of the cell's first affect hit (lexicon >= 1 or anchor fuzzy >= 0.5); token,
                  sentence and whether it was in a neighbour's edge are logged
  arrival         first hop (0 = seed) with anchor_fuzzy >= 0.5 or lex >= 2; per disturbance the profile across cells and
                  a least-squares velocity: ring distance from origin regressed on arrival hop, cells per hop
  lifetime        last hop at which any non-origin cell meets the arrival criterion
  collision       for the two cells either side of each midpoint between two origins (3-5 and 11-13 for 0 and 8 on N=16),
                  the first hop at which both disturbances score (lex >= 1 for an affect, fuzzy >= 0.5 for a fact), and
                  that cell's text
  freeze, recurrence  from ring_score.main run on a scratch copy of ring.jsonl (imported, not copied; the run's own
                  score.json is left alone)
Thresholds use raw lexicon hits (lex); lex60 is reported for the per-60-words predictions (P3, P5).
Writes <run>/affect.json and <run>/affect.svg (one row per hop, one column per cell, fill = dominant disturbance by
anchor_fuzzy + lex among those meeting the arrival criterion, full colour for anchor_exact, pale for fuzzy or lexicon
only; dot = frozen from here on; ring = cause supplied) in spacetime.svg's orientation, and prints a summary.
"""
import argparse, collections, contextlib, io, json, os, re, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ring_score as RS

HERE = os.path.dirname(os.path.abspath(__file__))
DEF_ANCHORS = os.path.join(HERE, "experiments", "ring_affect_20261107", "seeds", "anchors.json")
DEF_PLAIN = os.path.join(HERE, "experiments", "ring_affect_20261107", "seeds", "plain.txt")
SENT = re.compile(r"(?<=[.!?])\s+(?=[\"'A-Z])")   # ring.py's split, so "last sentence" means what the harness showed
WATCH_DEFAULT = ["letter", "phone", "call", "telegram", "doctor", "hospital", "news", "knock", "door"]
COLOURS = {"fact": "#2f6f8f", "panic": "#b5543c", "grief": "#8f5a9a", "anger": "#c48a2a"}
SUFFIX = r"(?:ing|ed|es|s|e|d|ly)?"


def norm(text):
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("‘", "'")).strip().lower()


def last_sentence(text):
    parts = [p.strip() for p in SENT.split(text.strip()) if p.strip()]
    return parts[-1] if parts else text.strip()


def sentence_of(text, pos):
    starts = [0] + [m.end() for m in SENT.finditer(text)]
    s = max(st for st in starts if st <= pos)
    nxt = [st for st in starts if st > pos]
    return text[s:nxt[0] if nxt else len(text)].strip()


def lex_pattern(entries):
    return [(e, re.compile(r"\b" + r"\s+".join(re.escape(p) for p in e.lower().split()) + SUFFIX + r"\b")) for e in entries]


def lex_hits(ntext, pats):
    spans, per = [], {}
    for e, p in pats:
        ms = [m.span() for m in p.finditer(ntext)]
        if ms: per[e] = len(ms); spans += ms
    spans.sort(); merged = 0; end = -1
    for a, b in spans:
        if a >= end: merged += 1; end = b
        else: end = max(end, b)
    return merged, per


def names_mid(text):
    """Capitalised words not at a sentence start (ring_score.names also takes 'The', 'Outside'...)."""
    out = []
    for m in re.finditer(r"\b[A-Z][a-z]{2,}\b", text):
        prev = text[:m.start()].rstrip()
        if prev and prev[-1] not in ".!?\"'“”‘’" and m.group().lower() not in RS.STOP:
            out.append((m.group(), m.start()))
    return out


def watch_list(anchors):
    w = anchors.get("cause_nouns_watch", WATCH_DEFAULT)
    if isinstance(w, str):
        m = re.search(r"\(([^)]*)\)", w)
        w = [x.strip() for x in (m.group(1) if m else w).split(",") if x.strip()] or WATCH_DEFAULT
    return [x.lower() for x in w]


def placements(hop0, dists, anchors):
    """{cell: disturbance name}: per-cell 'disturb' (seed basename) if the harness wrote it, else the cell whose hop-0 text
    holds the anchor, else cell 0 for a lone disturbance."""
    byseed = {d.get("seed", "").lower(): n for n, d in dists.items()}
    place = {}
    for c in hop0["cells"]:
        s = c.get("disturb")
        if not s: continue
        b = os.path.basename(str(s)).lower()
        n = byseed.get(b) or next((n for n in dists if n.lower() == b or n.lower() == os.path.splitext(b)[0]), None)
        if n: place[c["i"]] = n
    if place: return place
    for c in hop0["cells"]:
        for n, d in dists.items():
            if norm(d["anchor"]) in norm(c["text"]) and n not in place.values(): place[c["i"]] = n; break
    if not place and len(dists) == 1: place[0] = next(iter(dists))
    return place


def ring_score_freeze(run):
    """ring_score.main on a scratch copy of ring.jsonl: its freeze hops and recurrence without touching the run's files."""
    tmp = tempfile.mkdtemp(prefix="ring_affect_")
    try:
        shutil.copy(os.path.join(run, "ring.jsonl"), tmp)
        with contextlib.redirect_stdout(io.StringIO()):
            RS.main(tmp)
        sc = json.load(io.open(os.path.join(tmp, "score.json"), encoding="utf-8"))
        return sc["freeze_hop"], sc["ring_recurrence"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def lsq_velocity(points):
    """distance = v * hop + c over (hop, distance) pairs; v in cells per hop."""
    n = len(points)
    if n < 2 or len(set(t for t, _ in points)) < 2: return None, None
    mt = sum(t for t, _ in points) / n; md = sum(d for _, d in points) / n
    v = sum((t - mt) * (d - md) for t, d in points) / sum((t - mt) ** 2 for t, _ in points)
    return round(v, 3), round(md - v * mt, 3)


def ringdist(i, o, N):
    return min((i - o) % N, (o - i) % N)


def main(run, anchors_path=DEF_ANCHORS, plain_path=DEF_PLAIN):
    hops = [json.loads(l) for l in io.open(os.path.join(run, "ring.jsonl"), encoding="utf-8")]
    N = len(hops[0]["cells"]); T = len(hops) - 1
    texts = [[c["text"] for c in hp["cells"]] for hp in hops]
    anchors = json.load(io.open(anchors_path, encoding="utf-8"))
    plain = io.open(plain_path, encoding="utf-8").read().strip()
    plain_w = set(RS.words(plain))
    dists = {n: d for n, d in anchors.items() if isinstance(d, dict) and d.get("anchor")}
    for n, d in dists.items():
        d["kind"] = d.get("kind", "affect" if d.get("lexicon") else "fact")
        d["aw"] = [w for w in dict.fromkeys(RS.words(d["anchor"])) if len(w) >= 3 and w not in RS.STOP and w not in plain_w]
        d["pats"] = lex_pattern(d.get("lexicon", []))
    calm_pats = lex_pattern(anchors.get("background", {}).get("lexicon_calm", []))
    watch = lex_pattern(watch_list(anchors))
    place = placements(hops[0], dists, anchors)
    origin = {n: i for i, n in place.items()}
    freeze, ring_rec = ring_score_freeze(run)

    def measure(text, ntext, wset, nlast, nw):
        out = {}
        for n, d in dists.items():
            na = norm(d["anchor"])
            fz = round(sum(1 for w in d["aw"] if w in wset) / len(d["aw"]), 3) if d["aw"] else 0.0
            lex, per = lex_hits(ntext, d["pats"])
            edge = na in nlast or (d["aw"] and sum(1 for w in d["aw"] if w in set(RS.words(nlast))) / len(d["aw"]) >= 0.5)
            out[n] = {"exact": na in ntext, "fuzzy": fz, "lex": lex, "lex60": round(lex / max(1, nw) * 60, 2), "edge": bool(edge)}
            if per: out[n]["lex_entries"] = per
        return out

    rows = []
    for t in range(T + 1):
        row = []
        for i in range(N):
            text = texts[t][i]; ntext = norm(text); ws = RS.words(text); nw = len(ws)
            m = measure(text, ntext, set(ws), norm(last_sentence(text)), nw)
            calm, cper = lex_hits(ntext, calm_pats)
            live = {n: v["fuzzy"] + v["lex"] for n, v in m.items() if v["fuzzy"] >= 0.5 or v["lex"] >= 2}
            dom = max(live, key=lambda n: (live[n], -list(dists).index(n))) if live else None
            row.append({"i": i, "t": t, "words": nw, "d": m, "calm": calm, "calm60": round(calm / max(1, nw) * 60, 2),
                        "dominant": dom, "frozen": freeze[i] is not None and t >= freeze[i] and t >= 1, "cause": []})
        rows.append(row)
    # arrival, velocity, lifetime, edge promotion per disturbance
    hit = lambda v: v["fuzzy"] >= 0.5 or v["lex"] >= 2
    summ = {}
    for n, d in dists.items():
        o = origin.get(n)
        arr = [next((t for t in range(T + 1) if hit(rows[t][i]["d"][n])), None) for i in range(N)]
        pts = [(arr[i], ringdist(i, o, N)) for i in range(N) if arr[i] is not None] if o is not None else []
        v, c = lsq_velocity(pts)
        life = max([t for t in range(T + 1) for i in range(N) if i != o and hit(rows[t][i]["d"][n])], default=None)
        edge_first = [next((t for t in range(T + 1) if rows[t][i]["d"][n]["edge"]), None) for i in range(N)]
        exact_first = [next((t for t in range(T + 1) if rows[t][i]["d"][n]["exact"]), None) for i in range(N)]
        reached = [i for i in range(N) if arr[i] is not None and i != o]
        summ[n] = {"origin": o, "kind": d["kind"], "emotion": d.get("emotion"), "anchor": d["anchor"], "anchor_words": d["aw"],
                   "arrival": arr, "cells_reached": reached, "max_distance": max([ringdist(i, o, N) for i in reached], default=0) if o is not None else None,
                   "velocity": v, "velocity_fit": {"slope": v, "intercept": c, "n": len(pts)}, "lifetime": life,
                   "edge_promoted_first": edge_first, "anchor_exact_first": exact_first,
                   "fuzzy_only_cells": [i for i in reached if exact_first[i] is None and rows[arr[i]][i]["d"][n]["fuzzy"] >= 0.5]}
    # cause supplied: window of one hop around the cell's first affect hit
    affect = [n for n, d in dists.items() if d["kind"] == "affect"]
    causes = []
    for i in range(N):
        fh = next((t for t in range(T + 1) if any(rows[t][i]["d"][n]["lex"] >= 1 or rows[t][i]["d"][n]["fuzzy"] >= 0.5 for n in affect)), None)
        if fh is None: continue
        for t in range(max(1, fh - 1), min(T, fh + 1) + 1):
            text = texts[t][i]; prev_w = set(RS.words(texts[t - 1][i])) | set(w.lower() for w, _ in names_mid(texts[t - 1][i]))
            edges = norm(last_sentence(texts[t - 1][(i - 1) % N]) + " " + last_sentence(texts[t - 1][(i + 1) % N]))
            found = [(w, p) for w, p in names_mid(text) if w.lower() not in plain_w and w.lower() not in prev_w]
            for e, pat in watch:
                for m in pat.finditer(text.lower()):
                    if e not in plain_w and e not in prev_w: found.append((text[m.start():m.end()], m.start()))
            seen = set()
            for w, p in found:
                if w.lower() in seen: continue
                seen.add(w.lower())
                rec = {"i": i, "t": t, "token": w, "sentence": sentence_of(text, p), "first_hit_hop": fh, "from_edge": w.lower() in edges}
                causes.append(rec); rows[t][i]["cause"].append(w)
    # collision between pairs of placed disturbances, around the midpoints between their origins
    collisions = []
    placed = [n for n in dists if n in origin]
    score1 = lambda v, d: v["lex"] >= 1 if d["kind"] == "affect" else v["fuzzy"] >= 0.5
    for a in range(len(placed)):
        for b in range(a + 1, len(placed)):
            na, nb = placed[a], placed[b]; oa, ob = origin[na], origin[nb]
            mids = sorted({((oa + ((ob - oa) % N) // 2) % N), ((ob + ((oa - ob) % N) // 2) % N)})
            cells = sorted({(m + k) % N for m in mids for k in (-1, 0, 1)} - {oa, ob})
            per = {}
            for i in cells:
                t = next((t for t in range(1, T + 1) if score1(rows[t][i]["d"][na], dists[na]) and score1(rows[t][i]["d"][nb], dists[nb])), None)
                per[str(i)] = None if t is None else {"hop": t, "text": texts[t][i], "both_anchors_exact": rows[t][i]["d"][na]["exact"] and rows[t][i]["d"][nb]["exact"]}
            first = min([v["hop"] for v in per.values() if v], default=None)
            collisions.append({"pair": [na, nb], "cells": cells, "first_hop": first, "per_cell": per})
    out = {"run": os.path.basename(run.rstrip("/\\")), "cells": N, "hops": T, "anchors": os.path.relpath(anchors_path, HERE).replace("\\", "/"),
           "plain": os.path.relpath(plain_path, HERE).replace("\\", "/"), "placements": {str(i): n for i, n in sorted(place.items())},
           "disturbances": summ, "cause_supplied": causes, "collision": collisions or None, "freeze_hop": freeze, "ring_recurrence": ring_rec,
           "all_frozen_by": max(freeze) if all(f is not None for f in freeze) else None, "rows": rows}
    json.dump(out, io.open(os.path.join(run, "affect.json"), "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
    write_svg(run, out, dists, texts)
    print("%s: N=%d T=%d | placements %s | freeze hop per cell %s | ring recurrence %s" % (out["run"], N, T, out["placements"], freeze, ring_rec))
    for n, s in summ.items():
        print("  %-6s %-6s origin %s | arrival %s | velocity %s cells/hop (n=%d) | max distance %s | lifetime %s | edge promoted first %s | exact first %s | fuzzy-only cells %s" % (
            n, s["kind"], s["origin"], s["arrival"], s["velocity"], s["velocity_fit"]["n"], s["max_distance"], s["lifetime"], s["edge_promoted_first"], s["anchor_exact_first"], s["fuzzy_only_cells"]))
    print("  cause_supplied: %d token(s)%s" % (len(causes), "".join("\n    cell %d hop %d %r (first hit hop %d%s): %s" % (c["i"], c["t"], c["token"], c["first_hit_hop"], ", in edge" if c["from_edge"] else "", c["sentence"]) for c in causes[:12])))
    for c in collisions:
        print("  collision %s cells %s: first hop %s" % ("+".join(c["pair"]), c["cells"], c["first_hop"]))
    print("wrote affect.json and affect.svg")
    return out


def write_svg(run, out, dists, texts):
    N, T, rows = out["cells"], out["hops"], out["rows"]
    cw, ch, left, top = 28, 10, 40, 30
    W, H = left + N * cw + 190, top + (T + 1) * ch + 20
    col = {n: COLOURS.get(d.get("emotion") or d["kind"], RS.PAL[k % len(RS.PAL)]) for k, (n, d) in enumerate(dists.items())}
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="sans-serif" font-size="9">' % (W, H),
         '<rect width="100%" height="100%" fill="white"/>',
         '<text x="%d" y="14">%s: %d cells, %d hops. Fill = dominant disturbance (anchor_fuzzy + lexicon hits, among those at fuzzy &gt;= 0.5 or lexicon &gt;= 2); solid = verbatim anchor, pale = paraphrase or lexicon only; dot = frozen from here on; ring = cause supplied.</text>' % (left, out["run"], N, T)]
    for i in range(N):
        o.append('<text x="%d" y="%d" text-anchor="middle">%d</text>' % (left + i * cw + cw / 2, top - 4, i))
    for t in range(T + 1):
        y = top + t * ch
        if t % 5 == 0: o.append('<text x="%d" y="%d" text-anchor="end">%d</text>' % (left - 4, y + ch - 2, t))
        for i in range(N):
            x = left + i * cw; c = rows[t][i]; dom = c["dominant"]
            fill = col[dom] if dom else "#dddddd"
            op = 1.0 if dom and c["d"][dom]["exact"] else (0.5 if dom else 1.0)
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" fill-opacity="%.2f" stroke="white"/>' % (x, y, cw, ch, fill, op))
            if c["frozen"]: o.append('<circle cx="%d" cy="%d" r="2" fill="#000"/>' % (x + cw / 2, y + ch / 2))
            if c["cause"]: o.append('<circle cx="%d" cy="%d" r="4" fill="none" stroke="#000" stroke-width="1.2"/>' % (x + cw / 2, y + ch / 2))
    lx, ly = left + N * cw + 10, top
    for n, d in dists.items():
        o.append('<rect x="%d" y="%d" width="10" height="10" fill="%s"/><text x="%d" y="%d">%s (%s%s) origin %s</text>' % (
            lx, ly, col[n], lx + 14, ly + 9, n, d["kind"], ", " + d["emotion"] if d.get("emotion") else "", out["disturbances"][n]["origin"])); ly += 13
        o.append('<rect x="%d" y="%d" width="10" height="10" fill="%s" fill-opacity="0.5"/><text x="%d" y="%d">%s, paraphrase / lexicon only</text>' % (lx, ly, col[n], lx + 14, ly + 9, n)); ly += 13
    o.append('<rect x="%d" y="%d" width="10" height="10" fill="#dddddd"/><text x="%d" y="%d">none (background)</text>' % (lx, ly, lx + 14, ly + 9)); ly += 13
    o.append('<circle cx="%d" cy="%d" r="2" fill="#000"/><text x="%d" y="%d">frozen (unchanged from here on)</text>' % (lx + 5, ly + 5, lx + 14, ly + 9)); ly += 13
    o.append('<circle cx="%d" cy="%d" r="4" fill="none" stroke="#000" stroke-width="1.2"/><text x="%d" y="%d">cause supplied</text>' % (lx + 5, ly + 5, lx + 14, ly + 9)); ly += 13
    o.append("</svg>")
    io.open(os.path.join(run, "affect.svg"), "w", encoding="utf-8", newline="\n").write("\n".join(o))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="fact vs. affect measures for a ring.py run")
    ap.add_argument("run", nargs="+")
    ap.add_argument("--anchors", default=DEF_ANCHORS)
    ap.add_argument("--plain", default=DEF_PLAIN)
    a = ap.parse_args()
    try: sys.stdout.reconfigure(errors="replace")   # cell text in the summary may hold curly quotes; cp1252 consoles
    except Exception: pass
    for r in a.run:
        main(r, a.anchors, a.plain)
