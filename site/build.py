# -*- coding: utf-8 -*-
"""build.py: render C:/ai/loop/site/index.html from data/ and src/.

    python build.py            (from anywhere; paths are resolved relative to this file)

Reads only. Writes site/index.html and site/build_report.json.
Every passage in the output comes from data/<run>.json (or site/runs_extra/*/steps.jsonl for
runs made after the bundle) via this script; nothing is retyped. Authored text is in src/copy.py.
"""
import json, re, html, sys, difflib, pathlib, datetime

HERE = pathlib.Path(__file__).resolve().parent          # site/
LOOP = HERE.parent                                        # loop/
DATA = LOOP / "data"
SRC = HERE / "src"
sys.path.insert(0, str(SRC)); sys.path.insert(0, str(LOOP))
import copy as C                                          # authored text (src/copy.py)
import loop as L                                          # for INITS and norm()

FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)
FENCE_ANY = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)

# ---------------------------------------------------------------- data loading
def text_of(out):
    """Same decoding as export.py."""
    m = FENCE.match(out)
    if m: out = m.group(1)
    try:
        j = json.loads(out)
        if isinstance(j, dict) and "text" in j: return j["text"], True
    except Exception:
        pass
    return out, False

def load_bundle():
    runs = {}
    for p in sorted(DATA.glob("*.json")):
        if p.name == "index.json": continue
        d = json.loads(p.read_text(encoding="utf-8"))
        runs[d["meta"]["run"]] = d
    index = {e["run"]: e for e in json.loads((DATA / "index.json").read_text(encoding="utf-8"))}
    return runs, index

def load_extra():
    """Runs made after the bundle (site/runs_extra/<name>/steps.jsonl). Decoded like export.py."""
    out = {}
    for d in sorted((HERE / "runs_extra").glob("*")):
        p = d / "steps.jsonl"
        if not p.exists(): continue
        hops = []
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            j = json.loads(line)
            if "out" not in j: continue
            text, parsed = text_of(j["out"])
            hops.append({"t": j["t"], "tag": j["tag"], "model": j.get("model", "qwen3.8-27b"), "sampling": j.get("sampling", "T=0"),
                         "text": text, "text_is_json_field": parsed, "raw": j["out"], "tok_out": j.get("tok_out"), "finish": j.get("finish"),
                         "cos_prev": j.get("cos_prev"), "cos_x0": j.get("cos_x0"), "ncd_prev": j.get("ncd_prev"), "ncd_x0": j.get("ncd_x0"),
                         "surv_prev": j.get("surv_prev"), "surv_x0": j.get("surv_x0"), "gzip_ratio": j.get("gzip_ratio"), "latency": j.get("latency"),
                         "cycle_exact": j.get("cycle_exact"), "cycle_norm": j.get("cycle_norm"), "cycle_broken": j.get("cycle_broken")})
        if not hops: continue
        # a steps.jsonl can carry a hop from an aborted start (the harness appends); the later record for a t wins
        seen = {}
        for h in hops: seen[(h["tag"], h["t"])] = h
        dup = len(hops) - len(seen)
        hops = sorted(seen.values(), key=lambda h: (h["tag"], h["t"]))
        summ = {}
        sp = d / "summary.json"
        if sp.exists():
            try: summ = json.loads(sp.read_text(encoding="utf-8"))
            except Exception: summ = {}
        out[d.name] = {"meta": {"run": d.name, "model": "qwen", "mode": "chat", "hops": len(hops), "tags": sorted({h["tag"] for h in hops}), "summary": summ, "superseded": dup}, "hops": hops}
    return out

def x0_for(tag, run):
    """Full X_0 string for a tag (loop.INITS has the untruncated text; --init-file runs carry the file name as tag)."""
    base = tag.replace("~r", "")
    if base in L.INITS: return L.INITS[base]
    p = HERE / "runs_extra" / "inits" / base
    if p.exists(): return p.read_text(encoding="utf-8")
    raise KeyError(tag)

def split_x0(x0):
    try:
        j = json.loads(x0)
        if isinstance(j, dict) and "text" in j: return j.get("rule"), j["text"], True
    except Exception:
        pass
    return None, x0, False

# ---------------------------------------------------------------- diff marks
WORD = re.compile(r"(\s+)")
def diff_marks(prev_text, cur_text, threshold=0.5):
    """Return (html, marked) for cur_text with words not carried over from prev_text wrapped in <mark>.
    Only when at least `threshold` of the current words are matched by a word-level LCS; else plain."""
    if prev_text is None: return html.escape(cur_text), False
    ptoks = WORD.split(prev_text); ctoks = WORD.split(cur_text)
    pw = [w for w in ptoks if w and not w.isspace()]
    cw_idx = [i for i, w in enumerate(ctoks) if w and not w.isspace()]
    cw = [ctoks[i] for i in cw_idx]
    if not cw: return html.escape(cur_text), False
    sm = difflib.SequenceMatcher(a=pw, b=cw, autojunk=False)
    matched = set()
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): matched.add(blk.b + k)
    frac = len(matched) / len(cw)
    if frac < threshold or frac == 1.0 and len(cw) == len(pw):
        return html.escape(cur_text), False
    out = []; j = 0
    for i, tok in enumerate(ctoks):
        if not tok: continue
        if tok.isspace(): out.append(tok); continue
        if j in matched: out.append(html.escape(tok))
        else: out.append("<mark>" + html.escape(tok) + "</mark>")
        j += 1
    return "".join(out), True

def del_marks(prev_text, cur_text, threshold=0.5):
    """Return (html, marked) for prev_text with words not carried into cur_text wrapped in <del>.
    Same LCS and the same threshold as diff_marks (on the current hop's words)."""
    ptoks = WORD.split(prev_text); ctoks = WORD.split(cur_text)
    pw = [w for w in ptoks if w and not w.isspace()]
    cw = [w for w in ctoks if w and not w.isspace()]
    if not cw or not pw: return html.escape(prev_text), False
    sm = difflib.SequenceMatcher(a=pw, b=cw, autojunk=False)
    matched_c = set(); matched_p = set()
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): matched_c.add(blk.b + k); matched_p.add(blk.a + k)
    frac = len(matched_c) / len(cw)
    if frac < threshold or (frac == 1.0 and len(cw) == len(pw)):
        return html.escape(prev_text), False
    out = []; j = 0
    for tok in ptoks:
        if not tok: continue
        if tok.isspace(): out.append(tok); continue
        if j in matched_p: out.append(html.escape(tok))
        else: out.append("<del>" + html.escape(tok) + "</del>")
        j += 1
    return re.sub(r"</del>(\s+)<del>", r"\1", "".join(out)), True

def merge_marks(s):
    """<mark>a</mark> <mark>b</mark> -> <mark>a b</mark> (whitespace-only gaps)."""
    return re.sub(r"</mark>(\s+)<mark>", r"\1", s)

# ---------------------------------------------------------------- lane building
def build_lane(runs, index, lane):
    run = runs[lane["run"]]; tag = lane["tag"]
    hops = [dict(h, _run=lane["run"], _tag=tag) for h in run["hops"] if h.get("tag") == tag and "text" in h]
    hops.sort(key=lambda h: h["t"])
    ext = lane.get("extend")
    if ext and not (HERE / "runs_extra" / ext["run"] / "summary.json").exists(): ext = None   # not finished yet
    if ext and ext["run"] in runs:
        base_n = len(hops)
        ehops = sorted([h for h in runs[ext["run"]]["hops"] if h.get("tag") == ext["tag"] and "text" in h], key=lambda h: h["t"])
        ex0 = x0_for(ext["tag"], ext["run"])
        assert hops and ex0 == hops[-1]["raw"], "extension must start from the base run's last raw output"
        for h in ehops:
            hops.append(dict(h, t=h["t"] + base_n, _run=ext["run"], _tag=ext["tag"], _orig_t=h["t"]))
    x0 = x0_for(tag, lane["run"])
    rule, seed, x0_is_json = split_x0(x0)
    states = [x0] + [h["raw"] for h in hops]
    # copy_of: first earlier state byte-identical to this one
    first = {}
    copy_of = {}
    for t, s in enumerate(states):
        if s in first: copy_of[t] = first[s]
        else: first[s] = t
    # summary/terminal
    terminal = None; summary = None
    ie = index.get(lane["run"])
    if ie:
        for r in ie.get("results", []):
            if r["tag"] == tag: summary = r; terminal = r.get("terminal")
    elif run["meta"].get("summary"):
        for r in run["meta"]["summary"].get("results", []) if isinstance(run["meta"]["summary"], dict) else []:
            if r.get("tag") == tag: summary = r; terminal = r.get("terminal")
    if ext and ext["run"] in runs:
        # the base summary covers only the base hops; recompute the exact transient/period over the whole sequence
        first_rep = next((t for t in sorted(copy_of) if t > 0), None)
        esum = runs[ext["run"]]["meta"].get("summary") or {}
        eres = next((r for r in esum.get("results", []) if r.get("tag") == ext["tag"]), {}) if isinstance(esum, dict) else {}
        summary = dict(transient_exact=copy_of[first_rep] if first_rep else None, period_exact=(first_rep - copy_of[first_rep]) if first_rep else None)
        terminal = eres.get("terminal")
    items = []
    items.append(dict(t=0, kind="prose" if x0_is_json else "mono", text=seed, raw=x0, is_json=x0_is_json, marks=html.escape(seed),
                      model=None, copy_of=None, metrics=None, seed=True))
    prev_text = seed
    prev_raw = x0
    prev_shown = seed
    for h in hops:
        is_json = h["text_is_json_field"]
        text = h["text"]
        kind = "prose" if is_json else "mono"
        preamble = None; postamble = None; inner = None
        if not is_json:
            m = FENCE_ANY.search(h["raw"])
            if m:
                try:
                    j = json.loads(m.group(1))
                    if isinstance(j, dict) and "text" in j and j.get("rule") == rule:
                        inner = j["text"]
                        preamble = h["raw"][:m.start()].strip() or None
                        postamble = h["raw"][m.end():].strip() or None
                except Exception:
                    inner = None
        if inner is not None:
            kind = "prose"; shown = inner
        else:
            shown = text
        marks, marked = (html.escape(shown), False)
        if prev_text is not None:
            marks, marked = diff_marks(prev_text, shown)
            marks = merge_marks(marks)
        items.append(dict(t=h["t"], run=h["_run"], tag=h["_tag"], orig_t=h.get("_orig_t"), kind=kind, text=shown, raw=h["raw"], is_json=is_json, marks=marks, marked=marked,
                          preamble=preamble, postamble=postamble, model=h["model"], copy_of=copy_of.get(h["t"]), same_as_prev=(h["raw"] == prev_raw),
                          same_text_as_prev=(h["raw"] != prev_raw and shown == prev_shown),
                          metrics=dict(tok=h["tok_out"], finish=h["finish"], ncd=h["ncd_prev"], ncd_x0=h.get("ncd_x0"), cos=h["cos_prev"], surv=h["surv_prev"],
                                       cycle_exact=h["cycle_exact"], cycle_norm=h["cycle_norm"]),
                          words=len(shown.split()), glider=(run["meta"].get("mode") == "raw")))
        # for diff marks on the next hop: when this hop is raw JSON (truncated or unparsed), compare against
        # its text value as far as it goes, so the marks show edits to the passage rather than to the wrapper
        prev_text = shown
        if kind == "mono":
            mt = re.search(r'"text":\s*"(.*)$', shown, re.S)
            if mt: prev_text = mt.group(1).rstrip().rstrip('`').rstrip().rstrip('}').rstrip().rstrip('"')
        prev_raw = h["raw"]
        prev_shown = shown
    # a second rendering of each hop's text for when it is shown as the context of the next hop:
    # words that the next hop did not carry over are struck (presentation only; textContent unchanged)
    for a, b_ in zip(items, items[1:]):
        if a["kind"] == "mono" or b_["kind"] == "mono": continue
        dm, marked = del_marks(a["text"], b_["text"])
        if marked: a["as_context"] = dm
    return dict(run=lane["run"], tag=tag, label=lane.get("label"), extend=(ext if ext and ext["run"] in runs else None), rule=rule, seed=seed, x0=x0, x0_is_json=x0_is_json,
                model=(hops[0]["model"] if len({h["model"] for h in hops}) == 1 else " / ".join(sorted({h["model"] for h in hops}))) if hops else None,
                n=len(hops), items=items, terminal=terminal, summary=summary,
                mode=run["meta"].get("mode"), copies=sum(1 for t in copy_of if t > 0))

# ---------------------------------------------------------------- rendering helpers
def esc(s): return html.escape(s, quote=True)

def model_name(m):
    names = {"qwen3.8-27b": "Qwen3.8-27B", "claude-sonnet-4-6": "Claude Sonnet 4.6", "claude-sonnet-5": "Claude Sonnet 5"}
    if m and " / " in m: return " / ".join(names.get(x, x) for x in m.split(" / "))
    return names.get(m, m or "")

def fmt(v, nd=3):
    if v is None: return "\u2014"  # rendered only in metrics, not authored prose
    return ("%." + str(nd) + "f") % v

QUOTE = re.compile(r"\{\{([^|]+)\|([^|]+)\|(\d+)\|(.+?)\}\}")
def render_authored_safe(s, runs):
    """Authored prose with {{run|tag|t|exact}} quotes verified against the data."""
    # esc() would escape the braces' contents; do substitution on the raw string then escape the rest.
    parts = []; last = 0
    for m in QUOTE.finditer(s):
        parts.append(esc(s[last:m.start()]))
        run, tag, t, q = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        hs = [h for h in runs[run]["hops"] if h.get("tag") == tag and h.get("t") == t]
        if not hs: raise SystemExit("quote cites a missing hop: %s" % m.group(0))
        h = hs[0]
        if q not in (h.get("text") or "") and q not in (h.get("raw") or ""):
            raise SystemExit("quote not found in data: %s" % m.group(0))
        parts.append('<q class="cited" title="run %s, %s, hop %d">%s</q><span class="qcite" title="run %s, %s">hop %d</span>' % (esc(run), esc(tag), t, esc(q), esc(run), esc(tag), t))
        last = m.end()
    parts.append(esc(s[last:]))
    return "".join(parts)

def track_svg(lane, mini=False):
    n = lane["n"]
    step = 11; bw = 7; h = 40; lab = 14
    if mini: step = 4; bw = 3; h = 16; lab = 0
    w = step * (n + 1) + 4
    bars = []
    for it in lane["items"]:
        t = it["t"]
        x = 2 + t * step
        if t == 0:
            bars.append('<rect class="bar seed" data-t="0" x="%d" y="%d" width="%d" height="%d"><title>hop 0, the seed</title></rect>' % (x, h - 4, bw, 3))
            continue
        v = it["metrics"]["ncd"] if it["metrics"]["ncd"] is not None else 0
        bh = max(1.5, v * (h - 4))
        cls = "bar copy" if it["copy_of"] is not None else "bar"
        tip = "hop %d, ncd %s" % (t, fmt(v, 2)) + (", identical to hop %d" % it["copy_of"] if it["copy_of"] is not None else "")
        bars.append('<rect class="%s" data-t="%d" x="%d" y="%.1f" width="%d" height="%.1f"><title>%s</title></rect>' % (cls, t, x, h - bh, bw, bh, tip))
    labels = []
    if not mini:
        for t in range(0, n + 1, 10):
            labels.append('<text class="tick" x="%d" y="%d">%d</text>' % (2 + t * step + bw / 2, h + lab - 3, t))
    if mini:
        return ('<svg class="track mini" viewBox="0 0 %d %d" width="%d" height="%d" aria-hidden="true">'
                '<line class="floor" x1="0" y1="%d" x2="%d" y2="%d"/>%s</svg>') % (w, h, w, h, h - 1, w, h - 1, "".join(bars))
    return ('<svg class="track" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="hop track: one bar per hop, height is distance from the previous hop">'
            '<line class="floor" x1="0" y1="%d" x2="%d" y2="%d"/>%s%s<rect class="cursor" x="1" y="0" width="%d" height="%d"/></svg>') % (
            w, h + lab, w, h + lab, h - 1, w, h - 1, "".join(bars), "".join(labels), bw + 2, h)

def render_hop(lane, it, room_id, lane_i):
    t = it["t"]
    attrs = ' class="hop%s%s" data-t="%d"%s' % (" copy" if it.get("copy_of") is not None else "", " mono" if it["kind"] == "mono" else "", t,
                                               (' data-still="1"' if it.get("same_as_prev") else "") + (' data-copy-of="%d"' % it["copy_of"] if it.get("copy_of") is not None else "")
                                               + ((' data-ncd-x0="%.3f" data-ncd-prev="%.3f"' % (it["metrics"]["ncd_x0"] or 0, it["metrics"]["ncd"] or 0)) if it.get("metrics") else "")
                                               + (' data-same-text="1"' if it.get("same_text_as_prev") else ""))
    cite = []
    if t == 0:
        cite.append('<span class="k">seed</span> hop 0')
        cite.append("run %s, %s" % (esc(lane["run"]), esc(lane["tag"])))
    else:
        cite.append('<span class="k">hop %d</span>' % t)
        cite.append(esc(model_name(it["model"])))
        cite.append("run %s, %s%s" % (esc(it.get("run") or lane["run"]), esc(it.get("tag") or lane["tag"]), (", its hop %d" % it["orig_t"]) if it.get("orig_t") else ""))
        if it["copy_of"] is not None:
            cite.append('<span class="same">identical to hop %d</span>' % it["copy_of"])
        elif it.get("same_text_as_prev"):
            cite.append('<span class="same">same words as hop %d, JSON spaced differently</span>' % (t - 1))
        elif it.get("words") is not None:
            cite.append("%d words" % it["words"])
    body = []
    if it.get("preamble"):
        body.append('<div class="preamble" title="the model wrote this before the JSON object">%s</div>' % esc(it["preamble"]))
    marks_html = it["marks"]
    if it.get("glider"):
        marks_html = re.sub(r"\((\d{1,3})\)", r'<span class="n">(\1)</span>', marks_html)
    body.append('<div class="text">%s</div>' % marks_html)
    if it.get("as_context"):
        body.append('<div class="text as-context" hidden>%s</div>' % it["as_context"])
    if it.get("postamble"):
        body.append('<div class="preamble" title="the model wrote this after the JSON object">%s</div>' % esc(it["postamble"]))
    m = it["metrics"]
    metr = ""
    if m:
        bits = ["%s tok" % m["tok"], "finish %s" % esc(str(m["finish"])), "ncd %s" % fmt(m["ncd"], 2)]
        if m["cos"] is not None: bits.append("cos %s" % fmt(m["cos"], 4))
        if m["surv"] is not None: bits.append("5-gram survival %s" % fmt(m["surv"], 2))
        if m["cycle_exact"]: bits.append('<span class="same">exact cycle detected, period %d</span>' % m["cycle_exact"])
        metr = '<div class="metrics">%s</div>' % " \u00b7 ".join(bits)
    raw = '<details class="raw"><summary>raw output</summary><pre>%s</pre></details>' % esc(it["raw"])
    return '<li%s id="%s-%d-%d">\n<div class="cite">%s</div>\n%s\n%s\n%s\n</li>' % (attrs, room_id, lane_i, t, " \u00b7 ".join(cite), "\n".join(body), metr, raw)

def render_room(room, runs, index, section_class="room"):
    lanes = [build_lane(runs, index, ln) for ln in room["lanes"]]
    maxn = max(ln["n"] for ln in lanes)
    rule = lanes[0]["rule"]
    head = []
    numtxt = ('<span class="num">%d</span> ' % room["num"]) if room.get("num") else ""
    head.append('<h2>%s%s</h2>' % (numtxt, esc(room["title"])))
    facts = []
    for ln in lanes:
        f = "%s%s, %s hops" % ((esc(ln["label"]) + ": ") if ln["label"] else "", esc(model_name(ln["model"])), ln["n"])
        s = ln["summary"]
        if s and s.get("transient_exact") is not None:
            if s["period_exact"] == 1: f += ", exact fixed point from hop %d%s" % (s["transient_exact"], " (the seed itself)" if s["transient_exact"] == 0 else "")
            else: f += ", exact cycle of period %d from hop %d" % (s["period_exact"], s["transient_exact"])
        elif ln["n"]:
            f += ", no exact recurrence"
        if ln["terminal"]: f += " (%s)" % esc(ln["terminal"])
        f += ". run %s, %s, %s mode" % (esc(ln["run"]), esc(ln["tag"]), esc(ln["mode"] or "chat"))
        if ln.get("extend"):
            f += "; continued from its last hop as run %s (hops %d and up)" % (esc(ln["extend"]["run"]), len([h for h in runs[ln["run"]]["hops"] if h.get("tag") == ln["tag"] and "text" in h]) + 1)
        facts.append(f)
    if room.get("content_note"):
        head.append('<p class="content-note">%s</p>' % esc(room["content_note"]))
    head.append('<p class="note">%s</p>' % render_authored_safe(room["note"], runs))
    head.append('<p class="facts">%s</p>' % "<br>".join(facts))
    rules = [(ln["label"], ln["rule"]) for ln in lanes if ln["rule"]]
    if rules and len({r for _, r in rules}) == 1:
        head.append('<div class="rule"><span class="k">rule</span> <span class="rule-text">%s</span></div>' % esc(rules[0][1]))
    else:
        for lab, r in rules:
            head.append('<div class="rule"><span class="k">rule, %s</span> <span class="rule-text">%s</span></div>' % (esc(lab or ""), esc(r)))
    lanes_html = []
    for i, ln in enumerate(lanes):
        hops_html = "\n".join(render_hop(ln, it, room["id"], i) for it in ln["items"])
        label = ('<div class="lane-label">%s</div>' % esc(ln["label"])) if ln["label"] else ""
        ended = ""
        if ln["n"] < maxn:
            ended = '<div class="ended" hidden>No hop %s recorded. The harness stopped this run at hop %d%s.</div>' % ("<span class=\"ended-t\"></span>", ln["n"], (": " + esc(ln["terminal"])) if ln["terminal"] else "")
        ext_attr = (' data-extend-run="%s" data-extend-tag="%s"' % (esc(ln["extend"]["run"]), esc(ln["extend"]["tag"]))) if ln.get("extend") else ""
        lanes_html.append('<div class="lane" data-n="%d" data-run="%s" data-tag="%s"%s>%s%s<div class="slot context"><div class="slot-label">it saw</div></div><div class="slot current"><div class="slot-label">it wrote</div>%s</div><ol class="hops">%s</ol></div>'
                          % (ln["n"], esc(ln["run"]), esc(ln["tag"]), ext_attr, label, track_svg(ln), ended, hops_html))
    controls = ('<div class="controls">'
                '<button class="btn back" type="button" title="back (left arrow)">back</button>'
                '<div class="counter"><span class="t">0</span> <span class="of">of %d</span><span class="status"></span></div>'
                '<button class="btn next" type="button" title="next (right arrow, space)">next</button>'
                '<button class="btn play" type="button" title="play (p)">play</button>'
                '<button class="btn raw-toggle" type="button" title="raw output (r)">raw</button>'
                '<button class="btn sound-toggle" type="button" title="sound (s): one tone per hop, pitch is distance from the seed, loudness is distance from the previous hop">sound</button>'
                '<span class="keys" title="right arrow or space: next. left arrow: back. p: play. r: raw output. s: sound. esc: index">keys &rarr; &larr; p r s esc</span>'
                '</div>') % maxn
    return ('<section class="%s%s" id="%s" data-n="%d">\n<header class="room-head">\n%s\n</header>\n%s\n<div class="lanes lanes-%d">\n%s\n</div>\n</section>'
            % (section_class, " two" if len(lanes) == 2 else "", room["id"], maxn, "\n".join(head), controls, len(lanes), "\n".join(lanes_html)))


# ---------------------------------------------------------------- the map (census over the page-scale Qwen runs)
MAP_RUNS = [("20260902T155557_chat", "json_page", "passage", "room 5"),
            ("20260902T160344_chat", "json_page", "twice", "slot A"),
            ("20260902T160344_chat", "json_page~r", "twice", "slot B")]
# hand layout, keyed by census key (first five normalized words); x, y on an 860 x 420 canvas
MAP_POS = {
    "the tide came in an":            (70, 200),
    "the rain did not fall":          (230, 200),
    "the silence in the library":     (400, 200),
    "the rain hammered against the":  (590, 110),
    "the rain lashed against the":    (590, 290),
    "the silence that followed the":  (770, 290),
    "the ink did not dry":            (330, 340),
    "the shadow did not yield":       (230, 380),
    "the silence was not empty":      (120, 330),
    "the silence that followed was":  (150, 70),
    "the rain had finally ceased":    (330, 60),
}
def census_key(s, n=5):
    w = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()
    return " ".join(w[:n]) or "<empty>"

def map_svg(runs):
    seed = json.loads(L.INITS["json_page"])["text"]
    visits = {}      # key -> list of (room, lane label, t)
    trans = {}       # (a,b) -> count
    label = {}       # key -> exact first five words from the first passage that had it
    order_first = {} # key -> (t, room, t)
    exact_self = {}  # key -> number of hops that were byte-identical to the previous hop
    for run, tag, room, lab in MAP_RUNS:
        hops = sorted([h for h in runs[run]["hops"] if h.get("tag") == tag], key=lambda h: h["t"])
        seq = [(0, seed, L.INITS["json_page"])] + [(h["t"], h["text"], h["raw"]) for h in hops]
        keys = []; raws = []
        for t, text, raw in seq:
            k = census_key(text); keys.append(k); raws.append(raw)
            visits.setdefault(k, []).append((room, lab, t))
            if k not in label:
                label[k] = " ".join(text.split()[:5])
            if k not in order_first or t < order_first[k][0]: order_first[k] = (t, room, lab)
        for i, (a, b) in enumerate(zip(keys, keys[1:])):
            trans[(a, b)] = trans.get((a, b), 0) + 1
            if a == b and raws[i] == raws[i + 1]:
                exact_self[a] = exact_self.get(a, 0) + 1
    W, H = 860, 430
    out = ['<svg class="map" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="transition map of the page-scale Qwen runs">' % (W, H, W, H)]
    out.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>')
    import math
    def radius(k): return 10 + 3.2 * math.log(len(visits[k]))
    # edges
    for (a, b), n in sorted(trans.items(), key=lambda kv: kv[1]):
        if a == b: continue
        (x1, y1), (x2, y2) = MAP_POS[a], MAP_POS[b]
        dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy) or 1
        ra, rb = radius(a), radius(b)
        sx, sy = x1 + dx / d * (ra + 2), y1 + dy / d * (ra + 2)
        ex, ey = x2 - dx / d * (rb + 4), y2 - dy / d * (rb + 4)
        # curve back edges (pointing left) and the excursion so they do not overlap the main path
        back = x2 < x1 - 20
        bend = 0.22 if back else 0.0
        if (a, b) in {("the silence that followed was", "the rain had finally ceased"), ("the rain had finally ceased", "the silence in the library")}: bend = -0.12
        cx, cy = (sx + ex) / 2 - dy * bend, (sy + ey) / 2 + dx * bend
        cls = "edge" + (" escape" if a == "the silence that followed was" and b == "the rain had finally ceased" else "")
        out.append('<path class="%s" d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" style="stroke-width:%.1f" marker-end="url(#arr)"><title>%s → %s, %d time%s</title></path>'
                   % (cls, sx, sy, cx, cy, ex, ey, 1 + 0.9 * math.log(n) * 1.4, esc(label[a]), esc(label[b]), n, "" if n == 1 else "s"))
        if n > 1:
            lx, ly = (sx + 2 * cx + ex) / 4, (sy + 2 * cy + ey) / 4
            out.append('<text class="ecount" x="%.1f" y="%.1f">×%d</text>' % (lx, ly - 4, n))
    # nodes
    for k, (x, y) in MAP_POS.items():
        if k not in visits: continue
        r = radius(k); selfn = trans.get((k, k), 0); exn = exact_self.get(k, 0)
        t0, room0, lab0 = order_first[k]
        href = "#%s/%d" % (room0, t0)
        who = {}
        for room, lab, t in visits[k]: who.setdefault(lab, []).append(t)
        def span(ts):
            ts = sorted(ts)
            if len(ts) > 2 and ts[-1] - ts[0] == len(ts) - 1: return "hops %d to %d" % (ts[0], ts[-1])
            return "hop" + ("s " if len(ts) > 1 else " ") + ", ".join(str(t) for t in ts)
        tip = "; ".join("%s: %s" % (lab, span(ts)) for lab, ts in who.items())
        sink = exn >= 3
        held = (", copied exactly %d time%s" % (exn, "" if exn == 1 else "s")) if exn else ""
        same = (", %d hop%s with the same first five words but different text" % (selfn - exn, "" if selfn - exn == 1 else "s")) if selfn - exn else ""
        out.append('<a href="%s" class="node%s"><circle cx="%d" cy="%d" r="%.1f"/><title>%s. %s. %d visit%s%s%s. Click to read hop %d.</title>' % (
            href, " sink" if sink else "", x, y, r, esc(label[k]), esc(tip), len(visits[k]), "" if len(visits[k]) == 1 else "s", held, same, t0))
        if selfn:
            # self-loop drawn as a small arc above the node: solid for exact copies, dashed when only the opening words repeat
            dashed = exn == 0
            out.append('<path class="loop%s" d="M%.1f,%.1f a%.1f,%.1f 0 1,1 %.1f,0" marker-end="url(#arr)"/>' % (" same-opening" if dashed else "", x - r * 0.5, y - r * 0.85, r * 0.6, r * 0.6, r * 1.0))
            if exn: out.append('<text class="lcount" x="%d" y="%.1f">×%d</text>' % (x, y - r - 22, exn))
            else: out.append('<text class="lcount faint" x="%d" y="%.1f">×%d same opening</text>' % (x, y - r - 22, selfn))
        # label below (or above for the top row)
        ly = y + r + 14 if y > 90 else y + r + 14
        words = label[k].split()
        out.append('<text class="nlabel" x="%d" y="%.1f">%s</text>' % (x, ly, esc(" ".join(words))))
        out.append('<text class="nsub" x="%d" y="%.1f">%s</text>' % (x, ly + 12, esc("first at hop %d, %s" % (t0, lab0))))
        out.append('</a>')
    out.append('</svg>')
    stats = dict(states=len(visits), hops=sum(len(v) for v in visits.values()) - len(MAP_RUNS), trans=trans, visits=visits, label=label)
    return "\n".join(out), stats

# ---------------------------------------------------------------- page
def build():
    runs, index = load_bundle()
    extra = load_extra()
    runs.update(extra)
    rooms = list(C.ROOMS)
    def finished(run_name):
        if run_name in runs and run_name not in extra: return True   # part of the bundle
        r = extra.get(run_name)
        return bool(r and r["meta"]["hops"] >= 5 and (HERE / "runs_extra" / run_name / "summary.json").exists())
    have_qwen_next = finished("qwen_json_next")
    if have_qwen_next:
        rooms.append(C.ROOM_QWEN_NEXT)
    added = []
    for er in C.EXTRA_ROOMS:
        if all(finished(ln["run"]) for ln in er["lanes"]):
            er = dict(er); er["num"] = len(rooms) + 1; rooms.append(er); added.append(er["id"])
    # summary for the extra run: compute a terminal note from the copy structure
    room_html = [render_room(r, runs, index) for r in rooms]
    annex_html = [render_room(r, runs, index, section_class="room annex") for r in C.ANNEX]

    # index (table of contents)
    def toc_row(r):
        lanes = [build_lane(runs, index, ln) for ln in r["lanes"]]
        outs = []
        for ln in lanes:
            s = ln["summary"]
            if s and s.get("transient_exact") is not None:
                o = ("holds from hop %d%s" % (s["transient_exact"], " (the seed itself)" if s["transient_exact"] == 0 else "")) if s["period_exact"] == 1 else "period %d from hop %d" % (s["period_exact"], s["transient_exact"])
            else:
                o = "%d hops, no repeat" % ln["n"]
            if ln["label"]: o = "%s: %s" % (ln["label"], o)
            outs.append(o)
        who = " / ".join(sorted({model_name(ln["model"]) for ln in lanes}))
        minis = "".join(track_svg(ln, mini=True) for ln in lanes)
        return ('<li><a href="#%s"><span class="num">%s</span><span class="ttl">%s</span><span class="who">%s</span><span class="mini-wrap">%s</span><span class="out">%s</span></a></li>'
                % (r["id"], r.get("num", ""), esc(r["title"]), esc(who), minis, esc("; ".join(outs))))
    toc = "\n".join(toc_row(r) for r in rooms)
    toc_annex = "\n".join(toc_row(r) for r in C.ANNEX)

    seed = json.loads(L.INITS["json_page"])["text"]
    intro = "\n".join('<p class="authored">%s</p>' % esc(p) for p in C.INTRO)
    intro_after = "\n".join('<p class="authored">%s</p>' % render_authored_safe(p, runs) for p in C.INTRO_AFTER_SEED)
    poem = "\n".join('<p class="stanza">%s</p>' % "<br>".join(esc(l) for l in st.split("\n")) for st in C.POEM.split("\n\n"))
    colophon = "\n".join('<h3>%s</h3>\n<p class="authored">%s</p>' % (esc(h), esc(b)) for h, b in C.COLOPHON)
    if have_qwen_next or added:
        colophon += '\n<h3>Added after the bundle</h3>\n<p class="authored">%s</p>' % esc(
            "Rooms 13 and up come from runs made while this site was built, with the same harness (site/runs_extra/<run>/steps.jsonl; the Claude runs were started by the human from a terminal with the API key). Apart from room 14's Sonnet 4.6 lane, which is room 11's run, they are not in data/. Their run ids are names, not timestamps."
            + "".join(" The steps file of %s also holds %d record%s from a start that was aborted and rerun; the site uses the later record for that hop." % (name, r["meta"]["superseded"], "" if r["meta"]["superseded"] == 1 else "s")
                      for name, r in sorted(extra.items()) if r["meta"].get("superseded")))

    map_html, map_stats = map_svg(runs)
    map_note = render_authored_safe(C.MAP_NOTE, runs)
    tpl = (SRC / "template.html").read_text(encoding="utf-8")
    css = (SRC / "style.css").read_text(encoding="utf-8")
    js = (SRC / "app.js").read_text(encoding="utf-8")
    page = (tpl.replace("{{CSS}}", css).replace("{{JS}}", js)
            .replace("{{TITLE}}", esc(C.SITE_TITLE)).replace("{{SUB}}", esc(C.SITE_SUB))
            .replace("{{INTRO}}", intro).replace("{{INTRO_AFTER}}", intro_after).replace("{{SEED}}", esc(seed))
            .replace("{{TOC}}", toc).replace("{{TOC_ANNEX}}", toc_annex).replace("{{ANNEX_INTRO}}", esc(C.ANNEX_INTRO))
            .replace("{{ROOMS}}", "\n".join(room_html)).replace("{{ANNEX}}", "\n".join(annex_html))
            .replace("{{POEM_HEAD}}", esc(C.POEM_HEAD)).replace("{{POEM_TITLE}}", esc(C.POEM_TITLE)).replace("{{POEM}}", poem).replace("{{POEM_SIGN}}", esc(C.POEM_SIGN))
            .replace("{{COLOPHON}}", colophon).replace("{{MAP}}", map_html).replace("{{MAP_NOTE}}", map_note)
            .replace("{{MAP_FACTS}}", esc("%d states over %d hops of three runs: room 5, and slots A and B of room 6. A state is the first five words of a passage, the key the README's census uses. Node size is visits. A solid loop with ×n is a passage copied exactly n times; a dashed loop means the next hop kept only the opening words (hop 1 of every run starts like the seed; Mara's copy was one character off). ×n on an edge is how many times it was taken." % (map_stats["states"], map_stats["hops"]))).replace("{{BUILT}}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    (HERE / "index.html").write_text(page, encoding="utf-8")
    rep = dict(rooms=[r["id"] for r in rooms], annex=[r["id"] for r in C.ANNEX], qwen_next=have_qwen_next, extra_added=added,
               bytes=len(page.encode("utf-8")))
    (HERE / "build_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
    print(json.dumps(rep))

if __name__ == "__main__":
    build()
