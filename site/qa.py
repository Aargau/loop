# -*- coding: utf-8 -*-
"""qa.py: check that every passage in index.html is byte-identical to the data it cites.

    python qa.py

For each <li class="hop"> in index.html: read data-t and the enclosing lane's data-run/data-tag,
then compare
  - the textContent of .text (plus .preamble/.postamble when present) against the hop's text
    (the JSON text field, or the raw output when the output did not parse), and
  - the textContent of details.raw pre against the raw output,
  - hop 0 against loop.INITS[tag] (seed text / rule).
Also lints authored text (src/copy.py) for the style rules: no em dashes, not "resonates",
no "here's what's happening" openers. Exits non-zero on any failure.
"""
import json, re, sys, pathlib, html
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
LOOP = HERE.parent
sys.path.insert(0, str(LOOP)); sys.path.insert(0, str(HERE / "src"))
import loop as L
import build as B

class Extract(HTMLParser):
    """Collect, per lane, per hop li: text of .text/.preamble/.postamble/.rule and details pre."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # (tag, classes, id)
        self.lanes = []      # dict(run, tag, hops: {t: {...}})
        self.cur_lane = None
        self.cur_hop = None
        self.capture = None  # key being captured
        self.buf = []
        self.rooms = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        self.stack.append((tag, cls, a))
        if tag == "section" and "room" in cls:
            self.rooms.append(a.get("id"))
        if tag == "div" and "lane" in cls:
            self.cur_lane = dict(run=a.get("data-run"), tag=a.get("data-tag"), n=int(a.get("data-n")), hops={},
                                 ext_run=a.get("data-extend-run"), ext_tag=a.get("data-extend-tag"))
            self.lanes.append(self.cur_lane)
        if tag == "li" and "hop" in cls and self.cur_lane is not None:
            self.cur_hop = dict(t=int(a.get("data-t")), text="", preamble="", postamble="", raw="", ctx=None, mono=("mono" in cls), copy=("copy" in cls))
            self.cur_lane["hops"][self.cur_hop["t"]] = self.cur_hop
        if self.cur_hop is not None:
            if tag == "div" and "as-context" in cls: self.capture = "ctx"; self.buf = []
            elif tag == "div" and "text" in cls: self.capture = "text"; self.buf = []
            elif tag == "div" and "preamble" in cls:
                self.capture = "postamble" if self.cur_hop["text"] else "preamble"; self.buf = []
            elif tag == "pre" and self.capture is None: self.capture = "raw"; self.buf = []
    def handle_endtag(self, tag):
        if self.capture and self.stack and self.stack[-1][0] == tag and (
            (tag == "div" and self.capture in ("text", "preamble", "postamble", "ctx")) or (tag == "pre" and self.capture == "raw")):
            self.cur_hop[self.capture] = "".join(self.buf); self.capture = None; self.buf = []
        if tag == "li" and self.cur_hop is not None and self.stack and self.stack[-1][0] == "li":
            self.cur_hop = None
        if self.stack: self.stack.pop()
    def handle_data(self, data):
        if self.capture: self.buf.append(data)

def main():
    page = (HERE / "index.html").read_text(encoding="utf-8")
    ex = Extract(); ex.feed(page)
    runs, index = B.load_bundle(); runs.update(B.load_extra())
    fails = []; checked = 0
    for lane in ex.lanes:
        run = runs.get(lane["run"])
        if run is None: fails.append("unknown run %s" % lane["run"]); continue
        hops = {h["t"]: h for h in run["hops"] if h.get("tag") == lane["tag"] and "text" in h}
        if lane.get("ext_run"):
            base_n = len(hops)
            erun = runs.get(lane["ext_run"])
            if erun is None: fails.append("unknown extension run %s" % lane["ext_run"])
            else:
                for h in erun["hops"]:
                    if h.get("tag") == lane["ext_tag"] and "text" in h: hops[h["t"] + base_n] = h
        if len(hops) != lane["n"]: fails.append("%s/%s: lane n=%d but data has %d hops" % (lane["run"], lane["tag"], lane["n"], len(hops)))
        x0 = B.x0_for(lane["tag"], lane["run"])
        rule, seed, _ = B.split_x0(x0)
        for t, got in sorted(lane["hops"].items()):
            checked += 1
            if t == 0:
                if got["text"] != seed: fails.append("%s/%s hop 0 seed mismatch" % (lane["run"], lane["tag"]))
                if got["raw"] != x0: fails.append("%s/%s hop 0 raw mismatch" % (lane["run"], lane["tag"]))
                continue
            h = hops.get(t)
            if h is None: fails.append("%s/%s hop %d not in data" % (lane["run"], lane["tag"], t)); continue
            if got["raw"] != h["raw"]:
                fails.append("%s/%s hop %d raw differs" % (lane["run"], lane["tag"], t))
            if got["ctx"] is not None and got["ctx"] != got["text"]:
                fails.append("%s/%s hop %d context rendering differs from text" % (lane["run"], lane["tag"], t))
            if h["text_is_json_field"]:
                if got["text"] != h["text"]:
                    fails.append("%s/%s hop %d text differs" % (lane["run"], lane["tag"], t))
                if got["preamble"] or got["postamble"]:
                    fails.append("%s/%s hop %d has a preamble but parsed as JSON" % (lane["run"], lane["tag"], t))
            else:
                # either shown raw verbatim (mono), or preamble + inner text + postamble reconstructs the raw
                if got["mono"]:
                    if got["text"] != h["raw"]: fails.append("%s/%s hop %d mono text != raw" % (lane["run"], lane["tag"], t))
                else:
                    m = B.FENCE_ANY.search(h["raw"])
                    ok = False
                    if m:
                        try:
                            j = json.loads(m.group(1))
                            inner = j.get("text")
                            pre = h["raw"][:m.start()].strip(); post = h["raw"][m.end():].strip()
                            ok = (got["text"] == inner and got["preamble"] == pre and got["postamble"] == post)
                        except Exception: ok = False
                    if not ok: fails.append("%s/%s hop %d prose-from-fence mismatch" % (lane["run"], lane["tag"], t))
            # copy flag agrees with byte equality against earlier states
            states = [x0] + [hops[k]["raw"] for k in sorted(hops)]
            is_copy = any(states[t] == states[k] for k in range(t))
            if is_copy != got["copy"]: fails.append("%s/%s hop %d copy flag wrong" % (lane["run"], lane["tag"], t))
        # every data hop rendered?
        for t in hops:
            if t not in lane["hops"]: fails.append("%s/%s hop %d missing from page" % (lane["run"], lane["tag"], t))
    # the poem, verbatim against the brief
    brief = (LOOP / "FABLE_BRIEF.md").read_text(encoding="utf-8")
    import copy as CP
    if CP.POEM not in brief: fails.append("poem text differs from FABLE_BRIEF.md")
    if CP.POEM_TITLE not in brief or CP.POEM_SIGN not in brief: fails.append("poem title/sign differ from the brief")
    # style lint on authored text
    authored = []
    authored += CP.INTRO + CP.INTRO_AFTER_SEED + [CP.SITE_SUB, CP.SITE_TITLE, CP.ANNEX_INTRO, CP.POEM_HEAD]
    for r in CP.ROOMS + [CP.ROOM_QWEN_NEXT] + CP.ANNEX + CP.EXTRA_ROOMS:
        authored += [r["title"], r["note"], r.get("content_note") or ""]
    authored += [CP.MAP_NOTE]
    if "PLACEHOLDER" in page: fails.append("a rendered room still has a PLACEHOLDER note")
    for h, b in CP.COLOPHON: authored += [h, b]
    for s in authored:
        s2 = re.sub(r"\{\{[^}]*\}\}", "", s)  # quotes from the data are not authored
        if "—" in s2: fails.append("em dash in authored text: %r" % s2[:80])
        if "resonat" in s2.lower(): fails.append("'resonates' in authored text: %r" % s2[:80])
        if re.search(r"here'?s what", s2.lower()): fails.append("banned opener: %r" % s2[:80])
    print("checked %d hops in %d lanes across %d rooms; %d failures" % (checked, len(ex.lanes), len(ex.rooms), len(fails)))
    for f in fails: print("  FAIL", f)
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
