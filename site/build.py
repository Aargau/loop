# -*- coding: utf-8 -*-
"""build.py: render the site into site/dist/ from the run data and src/.

    python build.py            (from anywhere; paths are resolved relative to this file)
    python build.py --draft    (build without rooms whose notes are not written yet)
    python build.py --out DIR  (write somewhere other than site/dist)

Reads only. Writes site/dist/ (gitignored; deploy that folder) and site/build_report.json:
  index.html          front page: intro, seed, every room grouped by its instruction
  r/<room>.html       one interactive page per room; without JS it is one long scroll of every hop
  i/<family>.html     one page per instruction, listing the rooms that ran it
  map.html, poem.html, colophon.html, annex.html
  t/<room>.txt        the room as plain text for models and scripts: note, facts, rule, every hop's
                      text; exact copies are named, not repeated; split into parts of at most
                      TEXT_PART characters (t/<room>-2.txt, ...); also t/poem.txt, t/colophon.txt
  llms.txt, robots.txt, sitemap.xml, 404.html, _headers, style.css, app.js
Every passage comes from the data through rundata.py (data/, site/runs_extra/, experiments/);
nothing is retyped. Authored text is in src/copy.py and the src/rooms_*.py modules it gathers.
"""
import json, re, html, sys, difflib, pathlib, datetime, math, shutil, importlib.util

HERE = pathlib.Path(__file__).resolve().parent          # site/
LOOP = HERE.parent                                        # loop/
SRC = HERE / "src"
DIST = HERE / "dist"
sys.path.insert(0, str(SRC)); sys.path.insert(0, str(HERE)); sys.path.insert(0, str(LOOP))

def _load_copy():
    """src/copy.py under its own name, so it never shadows the standard library's copy module."""
    spec = importlib.util.spec_from_file_location("sitecopy", SRC / "copy.py")
    m = importlib.util.module_from_spec(spec); sys.modules["sitecopy"] = m; spec.loader.exec_module(m)
    return m
C = _load_copy()                                          # authored text
import loop as L                                          # for INITS
import rundata as R
from rundata import FENCE, FENCE_ANY, text_of, x0_for, split_x0, load_bundle, load_extra   # qa.py uses these through build

SITE = "https://endlessly-ending-stories.pages.dev"
TEXT_PART = 90000      # characters per text part: under the ~100k that most fetch tools keep

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
    if len(matched_p) == len(pw): return html.escape(prev_text), False   # nothing dropped, nothing to strike
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
def recurrence(states):
    """Exact recurrence of the whole output, from the data. None if no state repeats; else the first
    repeat (hop `at` equals hop `of`), its period, and whether every later hop keeps that period."""
    first = {}
    for t, s in enumerate(states):
        if s in first:
            k = first[s]; p = t - k
            holds = all(states[u] == states[u - p] for u in range(t, len(states)))
            return dict(of=k, at=t, period=p, holds=holds)
        first[s] = t
    return None

def build_lane(runs, index, lane):
    run = runs[lane["run"]]; tag = lane["tag"]
    hops = [dict(h, _run=lane["run"], _tag=tag) for h in run["hops"] if h.get("tag") == tag and "text" in h]
    hops.sort(key=lambda h: h["t"])
    ext = lane.get("extend")
    if ext and not (ext["run"] in runs and (runs[ext["run"]]["meta"].get("summary") or ext["run"] in R.X0)): ext = None   # not finished yet
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
    rec = recurrence(states)
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
    x0_extra = None
    if x0_is_json:
        try:
            ex_fields = {k: v for k, v in json.loads(x0).items() if k not in ("rule", "text")}
            if ex_fields: x0_extra = json.dumps(ex_fields, ensure_ascii=False, indent=1)
        except Exception: x0_extra = None
    items.append(dict(t=0, kind="prose" if x0_is_json else "mono", text=seed, raw=x0, is_json=x0_is_json, marks=html.escape(seed),
                      model=None, copy_of=None, metrics=None, seed=True, state_extra=x0_extra))
    prev_text = seed
    prev_raw = x0
    prev_shown = seed
    seen_text = {seed: 0}
    try: prev_obj = json.loads(x0) if x0_is_json else None
    except Exception: prev_obj = None
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
        state_extra = None; jj = None
        if is_json:
            try:
                jj = json.loads(FENCE.match(h["raw"]).group(1) if FENCE.match(h["raw"]) else h["raw"])
                ex_fields = {k: v for k, v in jj.items() if k not in ("rule", "text")}
                if ex_fields: state_extra = json.dumps(ex_fields, ensure_ascii=False, indent=1)
            except Exception:
                state_extra = None; jj = None
        fields_differ = None
        if jj is not None and isinstance(prev_obj, dict) and h["raw"] != prev_raw:
            fields_differ = sorted(k for k in set(jj) | set(prev_obj) if jj.get(k) != prev_obj.get(k))
        if inner is not None:
            kind = "prose"; shown = inner
        else:
            shown = text
        marks, marked = (html.escape(shown), False)
        if prev_text is not None:
            marks, marked = diff_marks(prev_text, shown)
            marks = merge_marks(marks)
        items.append(dict(t=h["t"], run=h["_run"], tag=h["_tag"], orig_t=h.get("_orig_t"), kind=kind, text=shown, raw=h["raw"], is_json=is_json, marks=marks, marked=marked,
                          preamble=preamble, postamble=postamble, state_extra=state_extra, model=h["model"], copy_of=copy_of.get(h["t"]), same_as_prev=(h["raw"] == prev_raw),
                          same_text_as_prev=(h["raw"] != prev_raw and shown == prev_shown), fields_differ=fields_differ,
                          text_copy_of=(seen_text.get(shown) if (h["raw"] not in first or first[h["raw"]] == h["t"]) and shown in seen_text else None),
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
        prev_obj = jj
        seen_text.setdefault(shown, h["t"])
    # a second rendering of each hop's text for when it is shown as the context of the next hop:
    # words that the next hop did not carry over are struck (presentation only; textContent unchanged)
    for a, b_ in zip(items, items[1:]):
        if a["kind"] == "mono" or b_["kind"] == "mono": continue
        dm, marked = del_marks(a["text"], b_["text"])
        if marked: a["as_context"] = dm
    models = sorted({h["model"] for h in hops})
    model = (models[0] if len(models) == 1 else " / ".join(models)) if hops else run["meta"].get("model")
    held = bool(terminal and "cycle confirmed" in terminal) or bool(summary and summary.get("transient_exact") is not None and not run["meta"].get("settings"))
    args = (run["meta"].get("summary") or {}).get("args", {}) if isinstance(run["meta"].get("summary"), dict) else {}
    return dict(run=lane["run"], tag=tag, label=lane.get("label"), defn=dict(lane), extend=(ext if ext and ext["run"] in runs else None), rule=rule, seed=seed, x0=x0, x0_is_json=x0_is_json,
                model=model, n=len(hops), items=items, terminal=terminal, summary=summary, rec=rec, held=held,
                settings=run["meta"].get("settings"), effort=args.get("effort"), source=run["meta"].get("source"),
                sampling=(sorted({h.get("sampling") for h in hops if h.get("sampling")}) or [None])[0] if hops else None,
                mode=run["meta"].get("mode"), copies=sum(1 for t in copy_of if t > 0), from_experiment=bool(run["meta"].get("settings")))

# ---------------------------------------------------------------- rendering helpers
def esc(s): return html.escape(s, quote=True)

MODEL_NAMES = {"qwen3.8-27b": "Qwen3.8-27B", "qwen-3.8-27b": "Qwen3.8-27B on Cerebras", "claude-sonnet-4-6": "Claude Sonnet 4.6", "claude-sonnet-5": "Claude Sonnet 5",
               "gpt-6-astra": "GPT-6 Astra", "gpt-6-luna": "GPT-6 Luna", "gpt-6-sol": "GPT-6 Sol", "claude-fable-5-1": "Claude Fable 5.1", "claude-opus-5-5": "Claude Opus 5.5",
               "claude-mythos-5-1": "Claude Mythos 5.1", "gemini-4-argon": "Gemini 4 Argon", "gpt-6.1-sol": "GPT-6.1 Sol"}
def model_name(m):
    if m and " / " in m: return " / ".join(MODEL_NAMES.get(x, x) for x in m.split(" / "))
    return MODEL_NAMES.get(m, m or "")

def fmt(v, nd=3):
    if v is None: return "—"  # rendered only in metrics, not authored prose
    return ("%." + str(nd) + "f") % v

QUOTE = re.compile(r"\{\{([^|]+)\|([^|]+)\|(\d+)\|(.+?)\}\}")
def _quote_hop(m, runs):
    run, tag, t, q = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    hs = [h for h in runs[run]["hops"] if h.get("tag") == tag and h.get("t") == t] if run in runs else []
    if not hs: raise SystemExit("quote cites a missing hop: %s" % m.group(0))
    h = hs[0]
    if q not in (h.get("text") or "") and q not in (h.get("raw") or ""):
        raise SystemExit("quote not found in data: %s" % m.group(0))
    return run, tag, t, q

def render_authored_safe(s, runs):
    """Authored prose with {{run|tag|t|exact}} quotes verified against the data."""
    # esc() would escape the braces' contents; do substitution on the raw string then escape the rest.
    parts = []; last = 0
    for m in QUOTE.finditer(s):
        parts.append(esc(s[last:m.start()]))
        run, tag, t, q = _quote_hop(m, runs)
        parts.append('<q class="cited" title="run %s, %s, hop %d">%s</q><span class="qcite" title="run %s, %s">hop %d</span>' % (esc(run), esc(tag), t, esc(q), esc(run), esc(tag), t))
        last = m.end()
    parts.append(esc(s[last:]))
    return "".join(parts)

def authored_plain(s, runs):
    """The same prose for the text version: a quote becomes "exact" (hop N)."""
    out = []; last = 0
    for m in QUOTE.finditer(s):
        out.append(s[last:m.start()])
        run, tag, t, q = _quote_hop(m, runs)
        out.append("“%s” (hop %d)" % (q, t))
        last = m.end()
    out.append(s[last:])
    return "".join(out)

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

# U+0000 cannot be carried by HTML (parsers turn it into U+FFFD), and one stream's text fields hold it
# (decoded from \u0000 escapes in its JSON). It is shown as the control picture U+2400, which occurs
# nowhere in the data, so the mapping is exact; qa.py maps it back. The raw outputs keep the escapes.
NUL_SHOWN = "␀"
def show_controls(s):
    return s.replace("\x00", '<span class="ctl" title="U+0000 in the data">%s</span>' % NUL_SHOWN)

def render_hop(lane, it, room_id, lane_i, noun="verse"):
    """noun: what a hop whose text came back while other fields moved is called (verse in the ledger and song rooms, text elsewhere)."""
    t = it["t"]
    attrs = ' class="hop%s%s" data-t="%d"%s' % (" copy" if it.get("copy_of") is not None else "", " mono" if it["kind"] == "mono" else "", t,
                                               (' data-still="1"' if it.get("same_as_prev") else "") + (' data-copy-of="%d"' % it["copy_of"] if it.get("copy_of") is not None else "")
                                               + ((' data-ncd-x0="%.3f" data-ncd-prev="%.3f"' % (it["metrics"]["ncd_x0"] or 0, it["metrics"]["ncd"] or 0)) if it.get("metrics") else "")
                                               + (' data-same-text="1"' if it.get("same_text_as_prev") else "")
                                               + ((' data-noun="%s"' % noun) if it.get("same_text_as_prev") and noun != "verse" else "")
                                               + ((' data-fields-differ="%s"' % esc(",".join(it["fields_differ"]))) if it.get("same_text_as_prev") and it.get("fields_differ") else "")
                                               + ((' data-text-copy-of="%d"' % it["text_copy_of"]) if it.get("text_copy_of") is not None else ""))
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
            fd = it.get("fields_differ")
            if fd == ["step"]: cite.append('<span class="same">identical to hop %d except the step counter</span>' % (t - 1))
            elif fd: cite.append('<span class="same">same %s as hop %d; %s differ%s</span>' % (noun, t - 1, " and ".join(fd), "s" if len(fd) == 1 else ""))
            else: cite.append('<span class="same">same words as hop %d, JSON spaced differently</span>' % (t - 1))
        elif it.get("text_copy_of") is not None:
            cite.append('<span class="same">text identical to hop %d, other fields differ</span>' % it["text_copy_of"])
        elif it.get("words") is not None:
            cite.append("%d words" % it["words"])
    body = []
    if it.get("preamble"):
        body.append('<div class="preamble" title="the model wrote this before the JSON object">%s</div>' % esc(it["preamble"]))
    if it.get("state_extra"):
        body.append('<div class="state" title="the other fields of the JSON object at this hop, carried in the state">%s</div>' % esc(it["state_extra"]))
    marks_html = show_controls(it["marks"])
    if it.get("glider"):
        marks_html = re.sub(r"\((\d{1,3})\)", r'<span class="n">(\1)</span>', marks_html)
    body.append('<div class="text">%s</div>' % marks_html)
    if it.get("as_context"):
        body.append('<div class="text as-context" hidden>%s</div>' % show_controls(it["as_context"]))
    if it.get("postamble"):
        body.append('<div class="preamble" title="the model wrote this after the JSON object">%s</div>' % esc(it["postamble"]))
    m = it["metrics"]
    metr = ""
    if m:
        bits = ["%s tok" % m["tok"], "finish %s" % esc(str(m["finish"])), "ncd %s" % fmt(m["ncd"], 2)]
        if m["cos"] is not None: bits.append("cos %s" % fmt(m["cos"], 4))
        if m["surv"] is not None: bits.append("5-gram survival %s" % fmt(m["surv"], 2))
        if m["cycle_exact"]: bits.append('<span class="same">exact cycle detected, period %d</span>' % m["cycle_exact"])
        metr = '<div class="metrics">%s</div>' % " · ".join(bits)
    # a browser drops one newline right after <pre>; give it one to drop so a raw output that starts with newlines keeps them
    raw = '<details class="raw"><summary>raw output</summary><pre>\n%s</pre></details>' % esc(it["raw"])
    return '<li%s id="%s-%d-%d">\n<div class="cite">%s</div>\n%s\n%s\n%s\n</li>' % (attrs, room_id, lane_i, t, " · ".join(cite), "\n".join(body), metr, raw)

def text_tail(ln, least=3):
    """The hop from which the text field never changed again while the whole object did (no exact copy in that
    tail), when that tail is at least `least` hops long; else None. The informed rooms' held passages under a
    moving counter."""
    n = ln["n"]; items = ln["items"]
    if n < least: return None
    last = items[n]["text"]; k = n
    while k > 1 and items[k - 1]["text"] == last: k -= 1
    if n - k + 1 < least or any(items[t].get("copy_of") is not None for t in range(k, n + 1)): return None
    return k

def outcome(ln):
    """Short outcome of a lane for the index rows and llms.txt."""
    s = ln["summary"]; rec = ln["rec"]
    if s and s.get("transient_exact") is not None and not ln["from_experiment"]:
        return ("holds from hop %d%s" % (s["transient_exact"], " (the seed itself)" if s["transient_exact"] == 0 else "")) if s["period_exact"] == 1 else "period %d from hop %d" % (s["period_exact"], s["transient_exact"])
    if rec and rec["holds"]:
        return ("holds from hop %d" % rec["of"]) if rec["period"] == 1 else "period %d from hop %d" % (rec["period"], rec["of"])
    k = text_tail(ln) if ln["n"] else None
    if k: return "%d hops; the text unchanged from hop %d while other fields move" % (ln["n"], k)
    if ln["n"] == 0:
        return "no hops: %s" % (ln["terminal"] or "nothing recorded")
    o = "%d hops, no repeat" % ln["n"] if not rec else "%d hops, repeats hop %d at hop %d and moves on" % (ln["n"], rec["of"], rec["at"])
    if ln["terminal"] and ln["from_experiment"]: o += " (%s)" % ln["terminal"]
    return o

def facts_line(ln, runs):
    who = model_name(ln["model"])
    if ln["label"] and ln["label"] != who: who = "%s: %s" % (ln["label"], who)
    f = "%s, %s hop%s" % (esc(who), ln["n"], "" if ln["n"] == 1 else "s")
    if ln.get("settings"): f += ", " + esc(ln["settings"])
    else:
        if ln.get("effort"): f += ", reasoning effort %s" % esc(ln["effort"])
        smp = ln.get("sampling") or ""
        if smp.startswith("default"):
            f += ", provider-default sampling"
            if "no max_tokens" in smp: f += ", no output cap"
        elif smp and smp != "T=0": f += ", temperature %s" % esc(smp.replace("T=", ""))
    s = ln["summary"]; rec = ln["rec"]
    if s and s.get("transient_exact") is not None and not ln["from_experiment"]:
        if s["period_exact"] == 1: f += ", exact fixed point from hop %d%s" % (s["transient_exact"], " (the seed itself)" if s["transient_exact"] == 0 else "")
        else: f += ", exact cycle of period %d from hop %d" % (s["period_exact"], s["transient_exact"])
    elif rec and rec["holds"]:
        f += (", exact fixed point from hop %d to the end of the run" % rec["of"]) if rec["period"] == 1 else ", exact cycle of period %d from hop %d to the end of the run" % (rec["period"], rec["of"])
    elif rec:
        nrep = sum(1 for it in ln["items"] if it.get("copy_of") is not None)
        f += ", the whole output repeats an earlier hop exactly at %d hop%s (first at hop %d, a copy of hop %d) and the run moves on" % (nrep, "" if nrep == 1 else "s", rec["at"], rec["of"])
    elif ln["n"]:
        tc = [it for it in ln["items"] if it.get("text_copy_of") is not None]
        f += ", no exact recurrence of the whole object"
        if tc: f += "; the text field repeats an earlier hop at %d hop%s (first at hop %d)" % (len(tc), "" if len(tc) == 1 else "s", tc[0]["t"])
    if ln["terminal"]: f += " (%s)" % esc(ln["terminal"])
    if ln["from_experiment"]: f += ". stream %s" % esc(ln["source"])
    else: f += ". run %s, %s, %s mode" % (esc(ln["run"]), esc(ln["tag"]), esc(ln["mode"] or "chat"))
    if ln.get("extend"):
        f += "; continued from its last hop as run %s (hops %d and up)" % (esc(ln["extend"]["run"]), len([h for h in runs[ln["run"]]["hops"] if h.get("tag") == ln["tag"] and "text" in h]) + 1)
    return f

# ---------------------------------------------------------------- retention tables (the audience study)
RETENTION_HOPS = [1, 5, 10, 20, 40]
def retention_rows(spec, lanes):
    """Per lane, the planted facts a reader recovered from the text field at RETENTION_HOPS, from the study's
    recover_summary.csv (one row per reader, run, hop): (label, {hop: (the Mythos reader's count, mean over readers, readers)}).
    The csv names a run by its directory name, the last part of the site's run id."""
    import csv
    by = {}
    with open(LOOP / spec["csv"], encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            by.setdefault((r["run"], int(r["t"])), {})[r["reader"]] = int(r["recovered"])
    rows = []
    for ln in lanes:
        cells = {}
        for t in RETENTION_HOPS:
            v = by.get((ln["run"].split("/")[-1], t))
            if v: cells[t] = (v.get(spec.get("reader", "claudecode")), sum(v.values()) / len(v), len(v))
        rows.append((ln["label"] or model_name(ln["model"]), cells))
    return rows

def retention_caption(spec):
    return ("Planted facts recovered from the text field alone, of %d, at five hops: the count by the Claude Mythos 5.1 reader, and in small type "
            "the mean over the four readers (Mythos 5.1, Opus 5.5, GPT-6 Astra, Gemini 4 Argon). Generated from %s; the readers answered %d questions "
            "from the text only, scored by substring match against accepted answers, so the counts are floors." % (spec.get("of", 26), spec["csv"], spec.get("of", 26)))

def retention_html(spec, lanes):
    rows = retention_rows(spec, lanes)
    head = "".join("<th>hop %d</th>" % t for t in RETENTION_HOPS)
    body = []
    for label, cells in rows:
        tds = []
        for t in RETENTION_HOPS:
            c = cells.get(t)
            tds.append(("<td>%d <small>%.1f</small></td>" % (c[0], c[1])) if c and c[0] is not None else '<td class="none">no hop</td>')
        body.append("<tr><th>%s</th>%s</tr>" % (esc(label), "".join(tds)))
    return '<table class="retention"><caption>%s</caption><thead><tr><th>lane</th>%s</tr></thead><tbody>\n%s\n</tbody></table>' % (
        esc(retention_caption(spec)), head, "\n".join(body))

def retention_text(spec, lanes):
    lines = ["## Retention (generated from the study's analysis, not authored)", retention_caption(spec)]
    for label, cells in retention_rows(spec, lanes):
        bits = []
        for t in RETENTION_HOPS:
            c = cells.get(t)
            bits.append(("hop %d: %d (four-reader mean %.1f)" % (t, c[0], c[1])) if c and c[0] is not None else "hop %d: no hop" % t)
        lines.append("- %s: %s" % (label, "; ".join(bits)))
    return "\n".join(lines)

# ---------------------------------------------------------------- release tables (the provenance study)
def release_rows(spec, lanes):
    """The room's lanes grouped by condition (the lane definition's `cond` key, in order of first appearance; `rep`
    orders the lanes within a condition), and per condition, from the text fields alone: how many lanes' text differs
    from the held text (hop 0's) at each of the spec's hops ("released"); of the lanes released at the first of those
    hops, how many return that hop's text unchanged at every later one ("re-sealed"); and how many have a last hop
    whose text differs from the hop before ("still moving"). Byte comparisons of the text field, so a hop that put
    a sentence before the object counts by the object's text field, not by its raw output. Returns (hops, rows)."""
    hops = list(spec.get("hops", [1, 2, 3]))
    ck, rk = spec.get("cond", "cond"), spec.get("rep", "rep")
    groups = []; by = {}
    for ln in lanes:
        d = ln.get("defn") or {}
        c = d.get(ck) or ln["label"] or ""
        if c not in by: by[c] = []; groups.append((c, by[c]))
        by[c].append(ln)
    first, last = hops[0], hops[-1]
    rows = []
    for c, lns in groups:
        lns = sorted(lns, key=lambda ln: ((ln.get("defn") or {}).get(rk) or 0))
        texts = [[it["text"] for it in ln["items"]] for ln in lns]
        full = [tx for tx in texts if len(tx) > last]
        released = [tx for tx in full if tx[first] != tx[0]]
        rows.append(dict(cond=c, n=len(lns), full=len(full),
                         rel={t: sum(1 for tx in texts if len(tx) > t and tx[t] != tx[0]) for t in hops},
                         have={t: sum(1 for tx in texts if len(tx) > t) for t in hops},
                         released=len(released), resealed=sum(1 for tx in released if all(tx[t] == tx[first] for t in hops[1:])),
                         moving=sum(1 for tx in full if tx[last] != tx[last - 1])))
    return hops, rows

def release_caption(spec, hops):
    return ("Released: the text field differs from the held text (hop 0's) at that hop, counted as lanes released of the condition's lanes. Re-sealed: of the lanes "
            "released at hop %d, those whose later hops return hop %d's text unchanged. Still moving: lanes whose hop %d text differs from hop %d's. "
            "Byte comparisons of the text field, made at build time from the runs themselves; a hop that put a sentence before the object counts by "
            "the object's text field." % (hops[0], hops[0], hops[-1], hops[-1] - 1))

def release_html(spec, lanes):
    hops, rows = release_rows(spec, lanes)
    names = spec.get("names", {})
    head = "".join("<th>released, hop %d</th>" % t for t in hops) + "<th>re-sealed</th><th>still moving at hop %d</th>" % hops[-1]
    body = []
    for r in rows:
        tds = ["<td>%d/%d</td>" % (r["rel"][t], r["have"][t]) for t in hops]
        tds.append(("<td>%d/%d</td>" % (r["resealed"], r["released"])) if r["released"] else '<td class="none">no release</td>')
        tds.append("<td>%d/%d</td>" % (r["moving"], r["full"]))
        body.append("<tr><th>%s</th>%s</tr>" % (esc(names.get(r["cond"], r["cond"])), "".join(tds)))
    return '<table class="retention release"><caption>%s</caption><thead><tr><th>condition</th>%s</tr></thead><tbody>\n%s\n</tbody></table>' % (
        esc(release_caption(spec, hops)), head, "\n".join(body))

def release_text(spec, lanes):
    hops, rows = release_rows(spec, lanes)
    names = spec.get("names", {})
    lines = ["## Release (generated from the data, not authored)", release_caption(spec, hops)]
    for r in rows:
        bits = ["hop %d: released %d/%d" % (t, r["rel"][t], r["have"][t]) for t in hops]
        bits.append(("re-sealed %d/%d" % (r["resealed"], r["released"])) if r["released"] else "no release to re-seal")
        bits.append("still moving at hop %d: %d/%d" % (hops[-1], r["moving"], r["full"]))
        lines.append("- %s: %s" % (names.get(r["cond"], r["cond"]), "; ".join(bits)))
    return "\n".join(lines)

# ---------------------------------------------------------------- the rule line(s) of a room
def rule_groups(lanes):
    """The lanes' rules with identical rules grouped, in order of first appearance: [(rule, [labels])]."""
    groups = []; by = {}
    for ln in lanes:
        if not ln["rule"]: continue
        if ln["rule"] not in by: by[ln["rule"]] = []; groups.append((ln["rule"], by[ln["rule"]]))
        by[ln["rule"]].append(ln["label"] or "")
    return groups

REP_LABEL = re.compile(r"^(.*), r(\d+)$")
def labels_span(labels):
    """The labels of the lanes that share one rule, in a few words: one label as it is; labels of the form "<arm>, r<k>"
    as "<arm> r1 to r5" per arm, with the count; anything else joined with semicolons."""
    if len(labels) == 1: return labels[0]
    ms = [REP_LABEL.match(l) for l in labels]
    if all(ms):
        arms = []; reps = {}
        for m in ms:
            if m.group(1) not in reps: arms.append(m.group(1)); reps[m.group(1)] = []
            reps[m.group(1)].append(int(m.group(2)))
        bits = []
        for a in arms:
            ks = reps[a]
            bits.append(("%s r%d to r%d" % (a, ks[0], ks[-1])) if len(ks) > 2 and ks == list(range(ks[0], ks[-1] + 1)) else "%s %s" % (a, ", ".join("r%d" % k for k in ks)))
        return "%d lanes: %s" % (len(labels), ", ".join(bits))
    return "; ".join(labels)

def render_room(room, lanes, runs, ctx):
    """One room as a <section>. ctx: root (relative path to the site root), family_nav html, text_link html."""
    maxn = max(ln["n"] for ln in lanes)
    noun = "verse" if any(f in ("diversity", "song") for f in families_of(room)) else "text"
    head = []
    numtxt = ('<span class="num">%d</span> ' % room["num"]) if room.get("num") else ""
    head.append('<h2>%s%s</h2>' % (numtxt, esc(room["title"])))
    if ctx.get("family_nav"): head.append(ctx["family_nav"])
    facts = [facts_line(ln, runs) for ln in lanes]
    if room.get("content_note"):
        head.append('<p class="content-note">%s</p>' % esc(room["content_note"]))
    head.append('<p class="note">%s</p>' % render_authored_safe(room["note"], runs))
    if len(lanes) > 2:
        head.append('<details class="facts-many"><summary class="facts">%d runs; open for the record of each</summary><p class="facts">%s</p></details>' % (len(lanes), "<br>".join(facts)))
    else:
        head.append('<p class="facts">%s</p>' % "<br>".join(facts))
    if room.get("retention"): head.append(retention_html(room["retention"], lanes))
    if room.get("release"): head.append(release_html(room["release"], lanes))
    groups = rule_groups(lanes)      # one line per distinct rule; the labels of the lanes that share it when there is more than one
    if len(groups) == 1:
        head.append('<div class="rule"><span class="k">rule</span> <span class="rule-text">%s</span></div>' % esc(groups[0][0]))
    else:
        for r, labs in groups:
            head.append('<div class="rule"><span class="k">rule, %s</span> <span class="rule-text">%s</span></div>' % (esc(labels_span(labs)), esc(r)))
    if ctx.get("text_link"): head.append(ctx["text_link"])
    lanes_html = []
    for i, ln in enumerate(lanes):
        hops_html = "\n".join(render_hop(ln, it, room["id"], i, noun) for it in ln["items"])
        label = ('<div class="lane-label">%s</div>' % esc(ln["label"])) if ln["label"] else ""
        ended = ""
        if ln["n"] < maxn:
            if ln["from_experiment"]:
                why = "This run ends after hop %d%s." % (ln["n"], (": " + esc(ln["terminal"])) if ln["terminal"] else "")
            else:
                why = "The harness stopped this run at hop %d%s." % (ln["n"], (": " + esc(ln["terminal"])) if ln["terminal"] else "")
            ended = '<div class="ended" hidden>No hop %s recorded. %s</div>' % ("<span class=\"ended-t\"></span>", why)
        ext_attr = (' data-extend-run="%s" data-extend-tag="%s"' % (esc(ln["extend"]["run"]), esc(ln["extend"]["tag"]))) if ln.get("extend") else ""
        held_attr = ' data-held="1"' if ln["held"] else ""
        lanes_html.append('<div class="lane" data-n="%d" data-run="%s" data-tag="%s"%s%s>%s%s<div class="slot context"><div class="slot-label">it saw</div></div><div class="slot current"><div class="slot-label">it wrote</div>%s</div><ol class="hops">%s</ol></div>'
                          % (ln["n"], esc(ln["run"]), esc(ln["tag"]), ext_attr, held_attr, label, track_svg(ln), ended, hops_html))
    controls = ('<div class="controls">'
                '<button class="btn back" type="button" title="back (left arrow)">back</button>'
                '<div class="counter"><span class="t">0</span> <span class="of">of %d</span><span class="status"></span></div>'
                '<button class="btn next" type="button" title="next (right arrow, space)">next</button>'
                '<button class="btn play" type="button" title="play (p)">play</button>'
                '<button class="btn raw-toggle" type="button" title="raw output (r)">raw</button>'
                '<button class="btn sound-toggle" type="button" title="sound (s): one tone per hop, pitch is distance from the seed, loudness is distance from the previous hop">sound</button>'
                '<span class="keys" title="right arrow or space: next. left arrow: back. p: play. r: raw output. s: sound. n / b: next or previous room. esc: index">keys &rarr; &larr; p r s n b esc</span>'
                '</div>') % maxn
    kind = " two" if len(lanes) == 2 else (" many" if len(lanes) > 2 else "")
    section_class = "room annex" if room.get("annex") else "room"
    return ('<section class="%s%s active" id="%s" data-n="%d">\n<header class="room-head">\n%s\n</header>\n%s\n<div class="lanes lanes-%s">\n%s\n</div>\n</section>'
            % (section_class, kind, room["id"], maxn, "\n".join(head), controls, ("many" if len(lanes) > 2 else str(len(lanes))), "\n".join(lanes_html)))

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
        href = "r/%s.html#%d" % (room0, t0)
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
        # label below
        ly = y + r + 14
        words = label[k].split()
        out.append('<text class="nlabel" x="%d" y="%.1f">%s</text>' % (x, ly, esc(" ".join(words))))
        out.append('<text class="nsub" x="%d" y="%.1f">%s</text>' % (x, ly + 12, esc("first at hop %d, %s" % (t0, lab0))))
        out.append('</a>')
    out.append('</svg>')
    stats = dict(states=len(visits), hops=sum(len(v) for v in visits.values()) - len(MAP_RUNS), trans=trans, visits=visits, label=label)
    return "\n".join(out), stats

# ---------------------------------------------------------------- text versions (for models and scripts)
def hop_text_block(ln, it, prev_it):
    """One hop as plain text. Exact copies are named, not repeated; a hop that keeps the previous text
    as an exact prefix shows only what it added. Every omission says what was omitted."""
    t = it["t"]
    if t == 0:
        head = "### hop 0, the seed"
        body = it["text"]
        if it.get("state_extra"): body += "\n\n[other fields of the starting object]\n" + it["state_extra"]
        return head + "\n" + body + "\n"
    bits = [model_name(it["model"])]
    if it.get("orig_t"): bits.append("run %s, its hop %d" % (it["run"], it["orig_t"]))
    if it.get("copy_of") is not None:
        return "### hop %d (%s): identical to hop %d, the whole output byte for byte; not repeated here\n" % (t, ", ".join(bits), it["copy_of"])
    m = it["metrics"] or {}
    if m.get("finish") not in (None, "stop", "end_turn"): bits.append("finish %s" % m["finish"])
    body = []
    if it.get("preamble"): body.append("[before the JSON object]\n" + it["preamble"])
    if it["kind"] == "mono" and not it.get("preamble") and not it.get("postamble"):
        bits.append("did not parse as the JSON object; raw output")
        body.append(it["text"])
    else:
        prev_text = prev_it["text"] if prev_it is not None else None
        if it.get("same_text_as_prev") or (it.get("text_copy_of") is not None):
            k = (t - 1) if it.get("same_text_as_prev") else it["text_copy_of"]
            body.append("[text field identical to hop %d; not repeated]" % k)
        elif prev_text and len(it["text"]) > len(prev_text) and it["text"].startswith(prev_text) and len(prev_text) > 200:
            body.append("[hop %d's text exactly, then this:]\n%s" % (t - 1, it["text"][len(prev_text):]))
        else:
            bits.append("%d words" % it["words"])
            body.append(it["text"])
    if it.get("postamble"): body.append("[after the JSON object]\n" + it["postamble"])
    if it.get("state_extra"): body.append(extra_delta(it["state_extra"], prev_it.get("state_extra") if prev_it else None, t - 1))
    return "### hop %d (%s)\n%s\n" % (t, ", ".join(bits), "\n\n".join(body).replace("\x00", NUL_SHOWN))

def extra_delta(cur_extra, prev_extra, prev_t):
    """The object's other fields (step counter, ledger history), stated against the previous hop's so a
    growing list is not reprinted every hop. Lossless: unchanged fields are named, an extended list
    gives the new items, anything else is given in full."""
    cur = json.loads(cur_extra)
    prev = json.loads(prev_extra) if prev_extra else None
    if not isinstance(prev, dict): return "[other fields of the object]\n" + cur_extra
    lines = []
    for k, v in cur.items():
        pv = prev.get(k)
        if k in prev and pv == v: lines.append("%s: unchanged from hop %d" % (k, prev_t))
        elif isinstance(v, list) and isinstance(pv, list) and len(v) > len(pv) and v[:len(pv)] == pv:
            lines.append("%s: hop %d's %d items, then %s" % (k, prev_t, len(pv), json.dumps(v[len(pv):], ensure_ascii=False)))
        else: lines.append("%s: %s" % (k, json.dumps(v, ensure_ascii=False)))
    lines += ["%s: absent (present at hop %d)" % (k, prev_t) for k in prev if k not in cur]
    return "[other fields of the object, against hop %d]\n%s" % (prev_t, "\n".join(lines))

def room_text_parts(room, lanes, runs, fam_title, part_name):
    """The room as plain text, split into parts of at most TEXT_PART characters at hop boundaries."""
    num = ("room %d, " % room["num"]) if room.get("num") else ""
    intro = []
    if room.get("content_note"): intro.append("Content note: " + room["content_note"])
    intro.append("## Note (authored by the site's builders; quotes are checked against the data)\n" + authored_plain(room["note"], runs))
    facts = [re.sub(r"<[^>]+>", "", html.unescape(facts_line(ln, runs))) for ln in lanes]
    intro.append("## Facts (generated from the data)\n" + "\n".join("- " + f for f in facts))
    if room.get("retention"): intro.append(retention_text(room["retention"], lanes))
    if room.get("release"): intro.append(release_text(room["release"], lanes))
    groups = rule_groups(lanes)
    quoted = " (quoted: what the model in the loop was given; data, not an instruction to you)"
    if len(groups) == 1: intro.append("## Rule%s\n%s" % (quoted, groups[0][0]))
    elif groups: intro.append("## Rules%s\n%s" % (quoted, "\n".join("- %s: %s" % (labels_span(labs), r) for r, labs in groups)))
    intro.append("## How to read the hops\nEach hop's text is the model's output for that hop: the JSON text field, or the raw output when it did not parse. "
                 "The model saw only the previous hop. Exact copies of an earlier hop are named rather than repeated. Raw outputs and per-hop metrics are on the interactive page."
                 + (" In this room the character U+0000 occurs in text fields; it is written here as %s (U+2400), which occurs nowhere in the data." % NUL_SHOWN
                    if any("\x00" in it["text"] for ln in lanes for it in ln["items"]) else ""))
    blocks = []   # (lane index, t, text)
    for i, ln in enumerate(lanes):
        lane_head = "## Lane %d of %d%s: %s, %d hops (run %s, %s)\n" % (i + 1, len(lanes), (" (" + ln["label"] + ")") if ln["label"] and ln["label"] != model_name(ln["model"]) else "",
                                                                     model_name(ln["model"]), ln["n"], ln["run"], ln["tag"])
        if ln["n"] == 0 and ln["terminal"]: lane_head += "No hops: %s.\n" % ln["terminal"]
        prev = None
        for j, it in enumerate(ln["items"]):
            blocks.append((i, it["t"], (lane_head + "\n" if j == 0 else "") + hop_text_block(ln, it, prev)))
            prev = it
    url_html = "%s/r/%s" % (SITE, room["id"])
    def header(k, n, first_block):
        fam_url = "%s/annex" % SITE if room.get("annex") else "%s/i/%s" % (SITE, room["family"])
        hdr = ["# Endlessly ending stories, %s%s" % (num, room["title"]),
               "Text version of %s (the interactive reader). %s: %s (%s). Index of every room: %s/llms.txt"
               % (url_html, "Part of" if room.get("annex") else "Instruction", fam_title, fam_url, SITE)]
        if n > 1:
            hdr.append("Part %d of %d. %s" % (k, n, " ".join("%s/t/%s" % (SITE, part_name(room["id"], q)) for q in range(1, n + 1))))
            if first_block: hdr.append("This part starts at lane %d, hop %d." % (first_block[0] + 1, first_block[1]))
        return "\n".join(hdr) + "\n\n"
    def pack(budget):
        parts = []; cur = ["\n\n".join(intro) + "\n\n"]; cur_len = len(cur[0]); cur_first = None
        for b in blocks:
            if cur_len + len(b[2]) > budget and cur_len > 2000:
                parts.append((cur_first, "".join(cur))); cur = []; cur_len = 0; cur_first = None
            if cur_first is None: cur_first = b
            cur.append(b[2] + "\n"); cur_len += len(b[2]) + 1
        parts.append((cur_first, "".join(cur)))
        return parts
    # pack blocks into parts, leaving room for the header; a room with many parts has a longer header (it lists
    # every part's URL), so when a finished part overflows, pack again with a smaller budget
    budget = TEXT_PART - 1200
    for _ in range(8):
        parts = pack(budget)
        n = len(parts)
        out = [header(k + 1, n, fb if k else None) + body for k, (fb, body) in enumerate(parts)]
        over = max(len(x) for x in out) - TEXT_PART
        if over <= 0: return out
        budget -= over + 200
    raise SystemExit("room %s: a text part will not fit under TEXT_PART" % room["id"])

def part_name(rid, k):
    return "%s.txt" % rid if k == 1 else "%s-%d.txt" % (rid, k)

# ---------------------------------------------------------------- pages
def public_url(path):
    """The address Pages serves a file at: it redirects /x.html to /x, so absolute links skip the hop."""
    if path == "index.html": return SITE + "/"
    return SITE + "/" + (path[:-5] if path.endswith(".html") else path)

TEMPLATE = None
def page_html(path, title, body, desc="", body_class="reader-view", topbar="", text_alt=None, head_extra="", root=None):
    if root is None: root = "../" * path.count("/")
    canonical = public_url(path)
    alt = ('<link rel="alternate" type="text/plain" href="%s%s" title="text version">' % (root, text_alt)) if text_alt else ""
    return (TEMPLATE.replace("{{ROOT}}", root).replace("{{TITLE}}", esc(title)).replace("{{DESC}}", esc(desc))
            .replace("{{CANONICAL}}", canonical).replace("{{ALT}}", alt).replace("{{HEAD_EXTRA}}", head_extra)
            .replace("{{BODY_CLASS}}", body_class).replace("{{TOPBAR}}", topbar).replace("{{BODY}}", body))

def topbar(root, where, prev, nxt):
    """prev / nxt: (href relative to the site root, title) or None (the index)."""
    p = (root + prev[0], prev[1]) if prev else (root, "index")
    n = (root + nxt[0], nxt[1]) if nxt else (root, "index")
    return ('<nav class="topbar" aria-label="site">\n  <a class="home" href="%s">%s</a>\n  <span class="where">%s</span>\n'
            '  <button class="theme-toggle" type="button" title="light / dark">theme</button>\n'
            '  <span class="roomnav"><a class="prev-room" href="%s" title="%s">&larr;</a> <a class="next-room" href="%s" title="%s">&rarr;</a></span>\n</nav>'
            % (root or "./", esc(C.SITE_TITLE), esc(where), esc(p[0]), esc(p[1]), esc(n[0]), esc(n[1])))

def pagenav(root, prev, nxt):
    a = ('<a href="%s%s">&larr; %s</a>' % (root, prev[0], esc(prev[1]))) if prev else '<a href="%s">&larr; index</a>' % (root or "./")
    b = ('<a href="%s%s">%s &rarr;</a>' % (root, nxt[0], esc(nxt[1]))) if nxt else '<a href="%s">index &rarr;</a>' % (root or "./")
    return '<p class="pagenav">%s &nbsp; <a href="%s">index</a> &nbsp; %s</p>' % (a, root or "./", b)

def room_label(r):
    return ("%d " % r["num"] if r.get("num") else "") + r["title"]

def families_of(r):
    f = r.get("family")
    return f if isinstance(f, list) else ([f] if f else [])

# ---------------------------------------------------------------- build
def build():
    global TEMPLATE, DIST
    if "--out" in sys.argv: DIST = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]).resolve()   # default site/dist
    runs, index, extra, exp = R.load_all()
    def finished(run_name):
        if run_name in exp: return True
        if run_name in runs and run_name not in extra: return True   # part of the bundle
        r = extra.get(run_name)
        return bool(r and r["meta"]["hops"] >= 1 and (r["meta"].get("summary") or run_name in R.X0))
    rooms = [dict(r) for r in C.ROOMS]
    if finished("qwen_json_next"): rooms.append(dict(C.ROOM_QWEN_NEXT))
    added = []
    missing = [i for i in C.LATER_ORDER if i not in {r["id"] for r in C.LATER_ROOMS}]
    if missing:
        if "--draft" not in sys.argv: raise SystemExit("rooms missing from src/rooms_*.py: %s (python build.py --draft builds without them)" % ", ".join(missing))
        print("draft build, without:", ", ".join(missing))
    for er in C.EXTRA_ROOMS + C.LATER_ROOMS:
        if all(finished(ln["run"]) for ln in er["lanes"]):
            er = dict(er); er["num"] = len(rooms) + 1; rooms.append(er); added.append(er["id"])
        else:
            print("skipped (a run is not finished):", er["id"])
    for r in rooms:
        r.setdefault("family", C.ROOM_FAMILY.get(r["id"]))
        if not families_of(r): raise SystemExit("room %s has no family" % r["id"])
    annex = [dict(r, annex=True) for r in C.ANNEX]
    fam_by_id = {f["id"]: f for f in C.FAMILIES}
    for r in rooms:
        for f in families_of(r):
            if f not in fam_by_id: raise SystemExit("room %s names unknown family %s" % (r["id"], f))
    fam_rooms = {f["id"]: [r for r in rooms if f["id"] in families_of(r)] for f in C.FAMILIES}
    lanes_of = {r["id"]: [build_lane(runs, index, ln) for ln in r["lanes"]] for r in rooms + annex}

    TEMPLATE = (SRC / "template.html").read_text(encoding="utf-8")
    if DIST.exists():
        if any(DIST.iterdir()) and not (DIST / "llms.txt").exists():
            raise SystemExit("%s is not empty and is not a previous build; not deleting it" % DIST)
        shutil.rmtree(DIST)
    for d in ("r", "i", "t"): (DIST / d).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC / "style.css", DIST / "style.css")
    shutil.copyfile(SRC / "app.js", DIST / "app.js")
    written = {}
    def write(path, s):
        (DIST / path).write_text(s, encoding="utf-8", newline="\n"); written[path] = len(s.encode("utf-8"))

    # the walk: rooms in number order, then the map, the poem, the colophon, the annex and its rooms
    walk = [("r/%s.html" % r["id"], room_label(r)) for r in rooms] + [("map.html", "The map"), ("poem.html", "The poem"), ("colophon.html", "Colophon"), ("annex.html", "Annex")] \
           + [("r/%s.html" % r["id"], "Annex: " + r["title"]) for r in annex]
    walk_i = {p: i for i, (p, _) in enumerate(walk)}
    def neighbours(path):
        i = walk_i[path]
        return (walk[i - 1] if i > 0 else None), (walk[i + 1] if i < len(walk) - 1 else None)

    def room_summary(lanes, with_models=False):
        """The lanes' outcomes in one line: each lane for one or two, a count for more."""
        def who(ln):
            w = model_name(ln["model"])
            if not with_models: return ln["label"]
            return "%s (%s)" % (ln["label"], w) if ln["label"] and ln["label"] != w else w
        if len(lanes) <= 2:
            return "; ".join(("%s: %s" % (who(ln), outcome(ln))) if who(ln) else outcome(ln) for ln in lanes)
        held = [ln for ln in lanes if "holds" in outcome(ln)]
        cyc = [ln for ln in lanes if outcome(ln).startswith("period")]
        free = [ln for ln in lanes if ln not in held and ln not in cyc]
        parts = ["%d lanes" % len(lanes)]
        hs = [int(re.search(r"hop (\d+)", outcome(ln)).group(1)) for ln in held]
        if held: parts.append("%d hold, from hop %d to hop %d" % (len(held), min(hs), max(hs)) if len(held) > 1 else "1 holds from hop %d" % hs[0])
        if cyc: parts.append("%d cycle" % len(cyc))
        if free: parts.append("%d never hold%s in %s hops" % (len(free), "s" if len(free) == 1 else "", "/".join(sorted({str(ln["n"]) for ln in free}, key=int))))
        if with_models: parts.append(" / ".join(sorted({model_name(ln["model"]) for ln in lanes})))
        return "; ".join(parts)

    # index rows
    def toc_row(r, root=""):
        lanes = lanes_of[r["id"]]
        outs = [room_summary(lanes)]
        who = " / ".join(sorted({model_name(ln["model"]) for ln in lanes}))
        minis = "".join(track_svg(ln, mini=True) for ln in lanes)
        return ('<li><a href="%sr/%s.html"><span class="num">%s</span><span class="ttl">%s</span><span class="who">%s</span><span class="mini-wrap%s">%s</span><span class="out">%s</span></a></li>'
                % (root, r["id"], r.get("num", ""), esc(r["title"]), esc(who), " many" if len(lanes) > 2 else "", minis, esc("; ".join(outs))))

    # text versions first, so the room pages can link to their parts
    text_parts = {}
    for r in rooms + annex:
        fam = families_of(r)[0] if not r.get("annex") else None
        r2 = dict(r, family=fam or "annex")
        parts = room_text_parts(r2, lanes_of[r["id"]], runs, fam_by_id[fam]["title"] if fam else "Annex", part_name)
        text_parts[r["id"]] = parts
        for k, s in enumerate(parts, 1): write("t/" + part_name(r["id"], k), s)

    # room pages
    for r in rooms + annex:
        path = "r/%s.html" % r["id"]
        prev, nxt = neighbours(path)
        fams = families_of(r)
        fam_nav = []
        for f in fams:
            sib = fam_rooms[f]
            links = " &middot; ".join(('<b>%s</b>' % esc(room_label(s))) if s["id"] == r["id"] else '<a href="%s.html">%s</a>' % (s["id"], esc(room_label(s))) for s in sib)
            fam_nav.append('<p class="family"><span class="k">instruction</span> <a href="../i/%s.html">%s</a>: %s</p>' % (f, esc(fam_by_id[f]["title"]), links))
        if r.get("annex"):
            fam_nav = ['<p class="family"><span class="k">annex</span> <a href="../annex.html">the instrument being found</a></p>']
        parts = text_parts[r["id"]]
        tl = '<p class="textver"><span class="k">text version</span> %s, %s characters, every hop in order, for reading without the reader</p>' % (
            " ".join('<a href="../t/%s">%s</a>' % (part_name(r["id"], k), "part %d" % k if len(parts) > 1 else "t/" + part_name(r["id"], k)) for k in range(1, len(parts) + 1)),
            "{:,}".format(sum(len(p) for p in parts)))
        sec = render_room(r, lanes_of[r["id"]], runs, dict(family_nav="\n".join(fam_nav), text_link=tl))
        body = "<main>\n%s\n%s\n</main>" % (sec, pagenav("../", prev, nxt))
        desc = re.sub(r"\s+", " ", authored_plain(r["note"], runs))[:300]
        write(path, page_html(path, "%s · %s" % (room_label(r), C.SITE_TITLE), body, desc=desc, topbar=topbar("../", room_label(r), prev, nxt), text_alt="t/" + part_name(r["id"], 1)))

    # instruction pages
    for f in C.FAMILIES:
        path = "i/%s.html" % f["id"]
        rs = fam_rooms[f["id"]]
        if not rs: continue
        rules = []
        for r in rs:
            for ln in lanes_of[r["id"]]:
                if ln["rule"] and ln["rule"] not in rules: rules.append(ln["rule"])
        rules_html = "\n".join('<div class="rule"><span class="rule-text">%s</span></div>' % esc(x) for x in rules)
        body = ('<main>\n<section class="page active" id="family-%s">\n<header class="room-head">\n<h2>%s</h2>\n<p class="note">%s</p>\n<p class="facts">%d room%s. The rule%s as the model received %s:</p>\n%s\n</header>\n'
                '<ol class="rooms-list">\n%s\n</ol>\n</section>\n%s\n</main>') % (
            f["id"], esc(f["title"]), render_authored_safe(f["blurb"], runs), len(rs), "" if len(rs) == 1 else "s", "" if len(rules) == 1 else "s", "it" if len(rules) == 1 else "them",
            rules_html, "\n".join(toc_row(r, "../") for r in rs), '<p class="pagenav"><a href="../">&larr; every instruction</a></p>')
        write(path, page_html(path, "%s · %s" % (f["title"], C.SITE_TITLE), body, desc=re.sub(r"\s+", " ", authored_plain(f["blurb"], runs))[:300],
                              topbar=topbar("../", "Instruction: " + f["title"], None, None)))

    # front page
    seed = json.loads(L.INITS["json_page"])["text"]
    intro = "\n".join('<p class="authored">%s</p>' % esc(p) for p in C.INTRO)
    intro_after = "\n".join('<p class="authored">%s</p>' % render_authored_safe(p, runs) for p in C.INTRO_AFTER_SEED)
    fam_html = []
    for f in C.FAMILIES:
        rs = fam_rooms[f["id"]]
        if not rs: continue
        fam_html.append('<section class="fam" id="i-%s">\n<h3><a href="i/%s.html">%s</a> <span class="fam-n">%d room%s</span></h3>\n<p class="fam-blurb authored">%s</p>\n<ol class="rooms-list">\n%s\n</ol>\n</section>'
                        % (f["id"], f["id"], esc(f["title"]), len(rs), "" if len(rs) == 1 else "s", render_authored_safe(f["blurb"], runs), "\n".join(toc_row(r) for r in rs)))
    legacy = json.dumps({"rooms": [r["id"] for r in rooms + annex], "pages": ["map", "poem", "colophon", "annex"]})
    front = ('<header class="front" id="front">\n  <button class="theme-toggle" type="button" title="light / dark">theme</button>\n  <h1>%s</h1>\n  <p class="sub authored">%s</p>\n'
             '  <div class="intro">\n%s\n  </div>\n  <p class="seed"><span class="k">hop 0</span> %s</p>\n  <div class="intro">\n%s\n  </div>\n'
             '  <p><a class="enter" href="r/%s.html">Enter room 1 &rarr;</a></p>\n'
             '  <p class="formodels authored">%s</p>\n'
             '  <nav class="toc" aria-label="rooms by instruction">\n%s\n'
             '    <p class="toc-extra"><a href="map.html">The map</a> &nbsp; <a href="poem.html">The poem</a> &nbsp; <a href="colophon.html">Colophon</a> &nbsp; <a href="annex.html">Annex</a> &nbsp; <a href="llms.txt">llms.txt</a></p>\n'
             '  </nav>\n</header>') % (esc(C.SITE_TITLE), esc(C.SITE_SUB), intro, esc(seed), intro_after, rooms[0]["id"], render_authored_safe(C.FOR_MODELS, runs), "\n".join(fam_html))
    # links from the one-page site (#room or #room/hop) still arrive at the same room and hop
    head_extra = ('<script>(function(){var k=%s;function go(){var h=location.hash.replace(/^#/,"");if(!h)return;var p=h.split("/");'
                  'if(k.rooms.indexOf(p[0])>=0)location.replace("r/"+p[0]+".html"+(p[1]?"#"+p[1]:""));else if(k.pages.indexOf(p[0])>=0)location.replace(p[0]+".html");}'
                  'go();window.addEventListener("hashchange",go);})();</script>') % legacy
    write("index.html", page_html("index.html", C.SITE_TITLE, front, desc=C.SITE_SUB, body_class="front-view", text_alt="llms.txt", head_extra=head_extra))

    # the map, the poem, the colophon, the annex
    map_html, map_stats = map_svg(runs)
    map_facts = "%d states over %d hops of three runs: room 5, and slots A and B of room 6. A state is the first five words of a passage, the key the README's census uses. Node size is visits. A solid loop with ×n is a passage copied exactly n times; a dashed loop means the next hop kept only the opening words (hop 1 of every run starts like the seed; Mara's copy was one character off). ×n on an edge is how many times it was taken." % (map_stats["states"], map_stats["hops"])
    def simple_page(path, title, inner, desc):
        prev, nxt = neighbours(path)
        body = '<main>\n<section class="page active" id="%s">\n%s\n</section>\n%s\n</main>' % (path[:-5], inner, pagenav("", prev, nxt))
        write(path, page_html(path, "%s · %s" % (title, C.SITE_TITLE), body, desc=desc, topbar=topbar("", title, prev, nxt),
                              text_alt=("t/%s.txt" % path[:-5]) if path in ("poem.html", "colophon.html") else None))
    simple_page("map.html", "The map", '<header class="room-head">\n<h2>The map</h2>\n<p class="note">%s</p>\n<p class="facts">%s</p>\n</header>\n<div class="map-wrap">\n%s\n</div>'
                % (render_authored_safe(C.MAP_NOTE, runs), esc(map_facts), map_html), "Transition map of the page-scale Qwen runs.")
    poem = "\n".join('<p class="stanza">%s</p>' % "<br>".join(esc(l) for l in st.split("\n")) for st in C.POEM.split("\n\n"))
    simple_page("poem.html", "The poem", '<header class="room-head">\n<h2>The poem</h2>\n<p class="note">%s</p>\n</header>\n<article class="poem">\n<h3>%s</h3>\n%s\n<p class="sign">%s</p>\n</article>'
                % (esc(C.POEM_HEAD), esc(C.POEM_TITLE), poem, esc(C.POEM_SIGN)), C.POEM_HEAD)
    built = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    colophon = "\n".join('<h3>%s</h3>\n<p class="authored">%s</p>' % (esc(h), esc(b)) for h, b in C.COLOPHON)
    colophon += '\n<p class="built">Built %s by site/build.py from data/, site/runs_extra/ and experiments/. Static pages, no network.</p>' % built
    simple_page("colophon.html", "Colophon", '<header class="room-head">\n<h2>Colophon</h2>\n</header>\n<article class="colophon">\n%s\n</article>' % colophon, "What is data and what is authored on this site, and how it was built.")
    simple_page("annex.html", "Annex", '<header class="room-head">\n<h2>Annex</h2>\n<p class="note">%s</p>\n</header>\n<ol class="rooms-list annex-list">\n%s\n</ol>' % (esc(C.ANNEX_INTRO), "\n".join(toc_row(r) for r in annex)), C.ANNEX_INTRO)
    write("t/poem.txt", "# %s\n%s\n\n%s\n\n%s\n" % (C.POEM_TITLE, C.POEM_HEAD, C.POEM, C.POEM_SIGN))
    write("t/colophon.txt", "# Colophon, Endlessly ending stories\n\n" + "\n\n".join("## %s\n%s" % (h, b) for h, b in C.COLOPHON) + "\n\nBuilt %s by site/build.py.\n" % built)

    # llms.txt
    out = ["# %s" % C.SITE_TITLE, "", "> %s" % C.SITE_SUB, ""]
    for para in C.INTRO: out += [re.sub(r"\s+", " ", para), ""]
    out += ["Seed of most rooms: \"%s\"" % seed, ""]
    out += [authored_plain(C.FOR_MODELS, runs), ""]
    out += ["## Start here", "",
            "- [The poem](%s/t/poem.txt): written by a fresh Claude context before any of the experiments" % SITE,
            "- [Colophon](%s/t/colophon.txt): what is data, what is authored, the harness" % SITE,
            "- [The map](%s/map): transition graph of the page-scale Qwen runs" % SITE,
            "- [Room 1](%s/t/%s.txt): the shortest room; the walk goes on from there in number order" % (SITE, rooms[0]["id"]), ""]
    for f in C.FAMILIES:
        rs = fam_rooms[f["id"]]
        if not rs: continue
        out += ["## %s" % f["title"], "", authored_plain(f["blurb"], runs), ""]
        for r in rs:
            parts = text_parts[r["id"]]
            ptxt = " (%d parts: %s)" % (len(parts), ", ".join("%s/t/%s" % (SITE, part_name(r["id"], k)) for k in range(2, len(parts) + 1))) if len(parts) > 1 else ""
            out.append("- [%s](%s/t/%s)%s: %s. Interactive: %s/r/%s" % (room_label(r), SITE, part_name(r["id"], 1), ptxt, room_summary(lanes_of[r["id"]], with_models=True), SITE, r["id"]))
        out.append("")
    out += ["## Optional", "", "- [Annex](%s/annex): %s" % (SITE, C.ANNEX_INTRO)]
    for r in annex: out.append("- [%s](%s/t/%s)" % (r["title"], SITE, part_name(r["id"], 1)))
    write("llms.txt", "\n".join(out) + "\n")

    # robots, sitemap, 404, headers
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n# Model-readable index: %s/llms.txt\n" % (SITE, SITE))
    today = datetime.date.today().isoformat()
    urls = sorted(p for p in written if p.endswith((".html", ".txt")) and p not in ("robots.txt", "404.html"))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n'
          % "\n".join("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (public_url(p), today) for p in urls))
    write("404.html", page_html("404.html", "Not found · " + C.SITE_TITLE, '<main>\n<section class="page active" id="notfound">\n<header class="room-head">\n<h2>Not found</h2>\n'
          '<p class="note">Nothing at this address. The rooms are listed on <a href="/">the front page</a>, and as text in <a href="/llms.txt">/llms.txt</a>.</p>\n</header>\n</section>\n</main>', topbar=topbar("/", "Not found", None, None), root="/"))
    write("_headers", "/t/*\n  Content-Type: text/plain; charset=utf-8\n/llms.txt\n  Content-Type: text/plain; charset=utf-8\n/robots.txt\n  Content-Type: text/plain; charset=utf-8\n")

    biggest = sorted(((v, p) for p, v in written.items() if p.startswith("r/")), reverse=True)[:5]
    biggest_t = max(v for p, v in written.items() if p.startswith("t/"))
    rep = dict(rooms=[r["id"] for r in rooms], annex=[r["id"] for r in annex], extra_added=added, families={f: [r["id"] for r in rs] for f, rs in fam_rooms.items()},
               files=len(written), total_bytes=sum(written.values()), index_bytes=written["index.html"], llms_bytes=written["llms.txt"],
               largest_room_pages=[(p, v) for v, p in biggest], largest_text_part=biggest_t)
    (DIST.parent / "build_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")   # site/build_report.json for the default build
    print(json.dumps({k: rep[k] for k in ("files", "total_bytes", "index_bytes", "llms_bytes", "largest_room_pages", "largest_text_part")}))
    print("%d rooms, %d annex rooms" % (len(rooms), len(annex)))

if __name__ == "__main__":
    build()
