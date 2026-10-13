# -*- coding: utf-8 -*-
"""qa.py: check the built site (site/dist/) against the data it cites.

    python build.py         (or python build.py --draft)
    python qa.py            (python qa.py --dist DIR checks a build made with --out DIR)

1. Room pages r/<room>.html, read as a browser reads them (a newline right after <pre> dropped, CR
   normalized): for every hop li, the text of .text (U+2400 mapped back to U+0000), .preamble,
   .postamble and .state against the data, details.raw pre against the raw output, hop 0 against the
   lane's X_0, the copy flag and data-copy-of against byte equality of states, the context rendering
   against the text, the lane's data-n against its hop count (extensions included), every data hop
   rendered once and in order, the rule against X_0. One room section per page, its lanes those of the
   room's definition, and the rooms are build_report.json's rooms + annex.
2. Text versions t/<room>.txt, t/<room>-2.txt ...: the parts are joined, each hop block is parsed and
   the hop's text and other JSON fields are rebuilt from the data's earlier hops (named copies, prefix
   continuations, repeated text fields, field deltas); every hop of every lane once, in order; part
   headers agree with where the parts start; no part over build.TEXT_PART characters.
3. Links: every relative or root-absolute href/src in every page names a file in dist; every site URL
   (canonical tags, llms.txt, sitemap.xml, robots.txt, text versions) maps to a file, extension-less
   for pages (Pages redirects /x.html to /x); robots.txt allows all and names the sitemap; 404.html
   uses root-absolute paths; the sitemap lists every page and llms.txt every room.
4. Authored text (src/copy.py, loaded as build.py loads it, and the src/rooms_*.py rooms it gathers):
   no em dash outside {{...}} quotes, no "resonat", no "here's what"; no PLACEHOLDER anywhere in dist.
5. The poem against FABLE_BRIEF.md.
6. Sizes: the largest room page, the largest text part, the total; no file over 25 MiB.
Prints a summary line, the sizes, and each FAIL. Exits non-zero on any failure.
"""
import json, re, sys, pathlib, posixpath, urllib.parse
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
LOOP = HERE.parent
sys.path.insert(0, str(HERE))
import build as B          # loads src/copy.py under the name "sitecopy" (it would shadow the standard library's copy)
import rundata as R
C = B.C

DIST = pathlib.Path(sys.argv[sys.argv.index("--dist") + 1]).resolve() if "--dist" in sys.argv else HERE / "dist"
SITE = B.SITE
MAX_FILE = 25 * 1024 * 1024        # Cloudflare Pages' limit for one file
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
fails = []
def fail(s): fails.append(s)

# ---------------------------------------------------------------- pages
class Page(HTMLParser):
    """One page: room sections, lanes, hop lis and the text of their parts, rule texts, every href/src."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0; self.rooms = []; self.lanes = []; self.rules = []; self.links = []
        self.lane = self.hop = self.cap = None
        self.lane_depth = self.hop_depth = self.cap_depth = None
        self.buf = []
    def start(self, key):
        self.cap = key; self.cap_depth = self.depth; self.buf = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get("class") or "").split()
        for k in ("href", "src"):
            if a.get(k) is not None: self.links.append((tag, a.get("rel"), a[k]))
        if tag in VOID: return
        self.depth += 1
        if self.cap: return
        if tag == "section" and "room" in cls:
            self.rooms.append(dict(id=a.get("id"), annex="annex" in cls))
        elif tag == "div" and "lane" in cls:
            self.lane = dict(run=a.get("data-run"), tag=a.get("data-tag"), n=int(a.get("data-n") or -1),
                             ext_run=a.get("data-extend-run"), ext_tag=a.get("data-extend-tag"), hops={}, order=[])
            self.lanes.append(self.lane); self.lane_depth = self.depth
        elif tag == "li" and "hop" in cls and self.lane is not None:
            self.hop = dict(t=int(a["data-t"]), text=None, preamble=None, postamble=None, raw=None, ctx=None, state=None,
                            mono="mono" in cls, copy="copy" in cls, copy_of=int(a["data-copy-of"]) if a.get("data-copy-of") else None)
            self.lane["hops"].setdefault(self.hop["t"], self.hop); self.lane["order"].append(self.hop["t"]); self.hop_depth = self.depth
        elif tag == "span" and "rule-text" in cls: self.start("rule")
        elif self.hop is not None:
            if tag == "div" and "as-context" in cls: self.start("ctx")
            elif tag == "div" and "text" in cls: self.start("text")
            elif tag == "div" and "preamble" in cls: self.start("preamble" if self.hop["text"] is None else "postamble")
            elif tag == "div" and "state" in cls: self.start("state")
            elif tag == "pre": self.start("raw")
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.cap and self.depth == self.cap_depth:
            s = "".join(self.buf)
            if self.cap == "raw" and s.startswith("\n"): s = s[1:]      # a browser drops a newline right after <pre>
            if self.cap == "rule": self.rules.append(s)
            else: self.hop[self.cap] = s
            self.cap = None
        if self.hop is not None and self.depth == self.hop_depth: self.hop = None
        if self.lane is not None and self.depth == self.lane_depth: self.lane = None
        self.depth -= 1
    def handle_data(self, data):
        if self.cap: self.buf.append(data)

def read_page(path):
    """Parse a page after the input-stream preprocessing a browser applies (CRLF and CR to LF; U+0000 is
    not carried, so it stands as U+FFFD and fails any comparison)."""
    s = path.read_text(encoding="utf-8")
    p = Page(); p.feed(s.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "�")); p.close()
    return s, p

# ---------------------------------------------------------------- the data, lane by lane
def shown_of(h, rule):
    """What the site shows as a hop's text: (text, preamble, postamble, mono). Mono is the raw output
    of a hop that did not parse; a fenced object with the lane's rule is shown as its text field."""
    if h["text_is_json_field"]: return h["text"], None, None, False
    m = R.FENCE_ANY.search(h["raw"])
    if m:
        try: j = json.loads(m.group(1))
        except ValueError: j = None
        if isinstance(j, dict) and "text" in j and j.get("rule") == rule:
            return j["text"], h["raw"][:m.start()].strip() or None, h["raw"][m.end():].strip() or None, False
    return h["raw"], None, None, True

def fields_of(s):
    """The object's fields other than rule and text, as the site prints them (None when there are none)."""
    m = R.FENCE.match(s)
    f = {k: v for k, v in json.loads(m.group(1) if m else s).items() if k not in ("rule", "text")}
    return json.dumps(f, ensure_ascii=False, indent=1) if f else None

def def_lanes(room):
    """A room definition's lanes as (run, tag, extension run, extension tag)."""
    return [(ln["run"], ln["tag"], (ln.get("extend") or {}).get("run"), (ln.get("extend") or {}).get("tag")) for ln in room["lanes"]]

LANES = {}
def lane_items(runs, run, tag, ext_run=None, ext_tag=None):
    """The lane as the data has it: hop 0 (X_0), then every hop, extension included, each with what the
    site must show. Returns (lane, None) or (None, why)."""
    key = (run, tag, ext_run, ext_tag)
    if key in LANES: return LANES[key]
    def hops_of(r, tg):
        if r not in runs: raise LookupError("unknown run %s" % r)
        hs = sorted((h for h in runs[r]["hops"] if h.get("tag") == tg and "text" in h), key=lambda h: h["t"])
        if [h["t"] for h in hs] != list(range(1, len(hs) + 1)): raise LookupError("run %s, %s: hops are not numbered 1..n" % (r, tg))
        return hs
    try:
        hops = [dict(h, _run=run, _t=h["t"]) for h in hops_of(run, tag)]
        if ext_run:
            if not hops or R.x0_for(ext_tag, ext_run) != hops[-1]["raw"]: raise LookupError("extension %s does not start from the last raw output" % ext_run)
            hops += [dict(h, t=h["t"] + len(hops), _run=ext_run, _t=h["t"]) for h in hops_of(ext_run, ext_tag)]
        x0 = R.x0_for(tag, run)
    except (LookupError, KeyError) as e:
        LANES[key] = (None, str(e)); return LANES[key]
    rule, seed, x0_json = R.split_x0(x0)
    items = [dict(t=0, raw=x0, text=seed, pre=None, post=None, mono=not x0_json, extra=fields_of(x0) if x0_json else None, copy_of=None)]
    first = {x0: 0}
    for h in hops:
        text, pre, post, mono = shown_of(h, rule)
        items.append(dict(t=h["t"], raw=h["raw"], text=text, pre=pre, post=post, mono=mono, copy_of=first.get(h["raw"]),
                          extra=fields_of(h["raw"]) if h["text_is_json_field"] else None, model=h["model"], finish=h.get("finish"),
                          ext=(h["_run"], h["_t"]) if h["_run"] != run else None))
        first.setdefault(h["raw"], h["t"])
    LANES[key] = (dict(rule=rule, n=len(hops), items=items), None)
    return LANES[key]

def check_page_lane(where, lane, exp):
    """Every hop li of one lane against the data."""
    if lane["n"] != exp["n"]: fail("%s: lane data-n=%d but the data has %d hops" % (where, lane["n"], exp["n"]))
    if lane["order"] != sorted(set(lane["order"])): fail("%s: hops repeated or out of order" % where)
    want = {it["t"] for it in exp["items"]}
    for t in sorted(want - set(lane["hops"])): fail("%s hop %d: in the data, missing from the page" % (where, t))
    for t in sorted(set(lane["hops"]) - want): fail("%s hop %d: on the page, not in the data" % (where, t))
    for it in exp["items"]:
        got = lane["hops"].get(it["t"])
        if got is None: continue
        w = "%s hop %d" % (where, it["t"])
        if "␀" in it["text"]: fail("%s: U+2400 occurs in the data, so it no longer stands for U+0000 unambiguously" % w)
        text = got["text"] and got["text"].replace(B.NUL_SHOWN, "\x00")
        if text != it["text"]: fail("%s: text differs from the data" % w)
        if got["raw"] != it["raw"]: fail("%s: raw output differs from the data" % w)
        if (got["preamble"], got["postamble"]) != (it["pre"], it["post"]): fail("%s: text before/after the JSON object differs" % w)
        if got["state"] != it["extra"]: fail("%s: other fields of the object differ" % w)
        if got["mono"] != it["mono"]: fail("%s: shown %s but the output %s" % (w, "raw" if got["mono"] else "as prose", "did not parse" if it["mono"] else "parsed"))
        if got["ctx"] is not None and got["ctx"].replace(B.NUL_SHOWN, "\x00") != it["text"]: fail("%s: context rendering differs from the text" % w)
        if got["copy"] != (it["copy_of"] is not None) or got["copy_of"] != it["copy_of"]:
            fail("%s: copy class %s, data-copy-of %s; the data says %s" % (w, "set" if got["copy"] else "not set", got["copy_of"],
                                                                         "a copy of hop %d" % it["copy_of"] if it["copy_of"] is not None else "not a copy"))

# ---------------------------------------------------------------- text versions
COPY_HEAD = re.compile(r"### hop (\d+) \((.*)\): identical to hop (\d+), the whole output byte for byte; not repeated here")
HOP_HEAD = re.compile(r"### hop (\d+) \((.*)\)")
SAME_TEXT = re.compile(r"\[text field identical to hop (\d+); not repeated\]")
PREFIX = re.compile(r"\[hop (\d+)'s text exactly, then this:\]\n")
FIELDS_FULL = "[other fields of the object]\n"
FIELDS_DELTA = re.compile(r"\[other fields of the object, against hop (\d+)\]\n")
SEED_FIELDS = "\n\n[other fields of the starting object]\n"

def rebuild_fields(sec, it, items):
    """A hop's other JSON fields from its text-version lines and the data's earlier hops; True if exact."""
    if sec.startswith(FIELDS_FULL): return sec[len(FIELDS_FULL):] == it["extra"]
    m = FIELDS_DELTA.match(sec)
    if not m: return False
    k = int(m.group(1))
    if k >= it["t"] or not items[k]["extra"]: return False
    prev = json.loads(items[k]["extra"]); f = {}; absent = set()
    for line in sec[m.end():].split("\n"):
        key, sep, rest = line.partition(": ")
        if not sep: return False
        grown = re.fullmatch(r"hop %d's (\d+) items, then (.*)" % k, rest, re.S)
        try:
            if rest == "unchanged from hop %d" % k: f[key] = prev[key]
            elif rest == "absent (present at hop %d)" % k:
                if key not in prev: return False
                absent.add(key)
            elif grown:
                if not isinstance(prev[key], list) or len(prev[key]) != int(grown.group(1)): return False
                f[key] = prev[key] + json.loads(grown.group(2))
            else: f[key] = json.loads(rest)
        except (KeyError, ValueError): return False
    return absent == set(prev) - set(f) and json.dumps(f, ensure_ascii=False, indent=1) == it["extra"]

def check_block(block, it, items, w):
    """One hop block of a text version against the data (items: the lane, indexed by t)."""
    line, _, body = block.partition("\n")
    t = it["t"]
    if t == 0:
        body = body[:-1]
        if line != "### hop 0, the seed": fail("%s: heading %r" % (w, line[:80]))
        if it["extra"]:
            k = body.rfind(SEED_FIELDS)
            if k < 0 or body[k + len(SEED_FIELDS):] != it["extra"]: fail("%s: the starting object's other fields differ" % w)
            if k >= 0: body = body[:k]
        if body != it["text"]: fail("%s: seed differs from X_0" % w)
        return
    mc = COPY_HEAD.fullmatch(line)
    mh = mc or HOP_HEAD.fullmatch(line)
    if not mh or int(mh.group(1)) != t: fail("%s: heading %r" % (w, line[:80])); return
    bits = mh.group(2)
    if not bits.startswith(B.model_name(it["model"])): fail("%s: heading names %r, the data %r" % (w, bits[:40], it["model"]))
    if it["ext"] and ("run %s, its hop %d" % it["ext"]) not in bits: fail("%s: does not cite the extension run and its hop" % w)
    if mc:
        k = int(mc.group(3))
        if body or k >= t or items[k]["raw"] != it["raw"]: fail("%s: named a copy of hop %d, but the raw outputs differ" % (w, k))
        return
    if it["copy_of"] is not None: fail("%s: an exact copy of hop %d, printed instead of named" % (w, it["copy_of"]))
    if it["finish"] not in (None, "stop", "end_turn") and ("finish %s" % it["finish"]) not in bits: fail("%s: does not say it finished with %s" % (w, it["finish"]))
    body = body[:-1].replace(B.NUL_SHOWN, "\x00")
    if it["pre"] is not None:
        need = "[before the JSON object]\n" + it["pre"] + "\n\n"
        if not body.startswith(need): fail("%s: text before the JSON object differs" % w); return
        body = body[len(need):]
    if it["extra"] is not None:
        k = body.rfind("\n\n[other fields of the object")
        if k < 0: fail("%s: other fields of the object missing" % w)
        else:
            if not rebuild_fields(body[k + 2:], it, items): fail("%s: other fields of the object do not rebuild from the data" % w)
            body = body[:k]
    if it["post"] is not None:
        need = "\n\n[after the JSON object]\n" + it["post"]
        if not body.endswith(need): fail("%s: text after the JSON object differs" % w); return
        body = body[:-len(need)]
    if it["mono"]:
        if body != it["raw"] or not bits.endswith(", did not parse as the JSON object; raw output"): fail("%s: raw output (did not parse) differs" % w)
        return
    ms, mp = SAME_TEXT.fullmatch(body), PREFIX.match(body)
    if ms:
        k = int(ms.group(1))
        if not (k < t and items[k]["text"] == it["text"]): fail("%s: text named identical to hop %d, but it differs" % (w, k))
    elif mp:
        k = int(mp.group(1)); rest = body[mp.end():]
        if not (k < t and rest and items[k]["text"] + rest == it["text"]): fail("%s: hop %d's text plus the addition is not this hop's text" % (w, k))
    elif body != it["text"]: fail("%s: text differs from the data" % w)
    elif not bits.endswith(", %d words" % len(it["text"].split())): fail("%s: word count in the heading is wrong" % w)

def check_text(rid, lanes, rules, part_sizes):
    """Join a room's parts and rebuild every hop of every lane from them, in order. Returns hop blocks read."""
    read = lambda k: (DIST / "t" / B.part_name(rid, k)).read_text(encoding="utf-8") if (DIST / "t" / B.part_name(rid, k)).is_file() else None
    parts = [read(1)]
    if parts[0] is None: fail("t/%s missing" % B.part_name(rid, 1)); return 0
    m = re.search(r"^Part 1 of (\d+)\. ", parts[0].partition("\n\n")[0], re.M)
    n = int(m.group(1)) if m else 1
    for k in range(2, n + 1):
        parts.append(read(k))
        if parts[-1] is None: fail("t/%s missing (part %d of %d)" % (B.part_name(rid, k), k, n)); return 0
    bodies = []; starts = {}; off = 0
    for k, s in enumerate(parts, 1):
        name = "t/" + B.part_name(rid, k)
        part_sizes.append((len(s), name))
        if len(s) > B.TEXT_PART: fail("%s: %d characters, over TEXT_PART (%d)" % (name, len(s), B.TEXT_PART))
        head, _, body = s.partition("\n\n")
        hl = head.split("\n")
        if not hl[0].startswith("# Endlessly ending stories, "): fail("%s: no title line" % name)
        if (n > 1) != any(l.startswith("Part %d of %d. " % (k, n)) for l in hl): fail("%s: part line wrong (part %d of %d)" % (name, k, n))
        if k > 1:
            ms = re.fullmatch(r"This part starts at lane (\d+), hop (\d+)\.", hl[-1])
            if not ms: fail("%s: does not say where it starts" % name)
            else: starts[off] = (name, int(ms.group(1)), int(ms.group(2)))
        bodies.append(body); off += len(body)
    stream = "".join(bodies)
    N = len(lanes)
    pos = stream.find("## Lane 1 of %d" % N)
    if pos < 0: fail("t/%s: no heading for lane 1 of %d" % (B.part_name(rid, 1), N)); return 0
    for r in rules:
        if r not in stream[:pos]: fail("t/%s: the rule %r is not given" % (B.part_name(rid, 1), r[:60]))
    block_at = {}; nblocks = 0
    for i, ((run, tag, _, _), exp) in enumerate(lanes):
        w0 = "t/%s lane %d (%s, %s)" % (rid, i + 1, run, tag)
        head_at = pos; eol = stream.find("\n", pos); line = stream[pos:eol]
        if not (line.startswith("## Lane %d of %d" % (i + 1, N)) and line.endswith(", %d hops (run %s, %s)" % (exp["n"], run, tag))):
            fail("%s: lane heading %r" % (w0, line[:120])); return nblocks
        pos = eol + 1
        if stream.startswith("No hops: ", pos): pos = stream.find("\n", pos) + 1
        if stream[pos:pos + 1] != "\n": fail("%s: no blank line after the lane heading" % w0); return nblocks
        pos += 1
        items = exp["items"]
        for j, it in enumerate(items):
            block_at[head_at if j == 0 else pos] = (i + 1, it["t"])
            if j + 1 < len(items): nxt = "\n\n### hop %d (" % items[j + 1]["t"]
            elif i + 1 < N: nxt = "\n\n## Lane %d of %d" % (i + 2, N)
            else: nxt = None
            end = stream.find(nxt, pos) if nxt else (len(stream) - 2 if stream.endswith("\n\n") else -1)
            if end < 0 or not stream.startswith("### hop %d" % it["t"], pos):
                fail("%s hop %d: block not found where expected (hops missing or out of order)" % (w0, it["t"])); return nblocks
            check_block(stream[pos:end + 1], it, items, "%s hop %d" % (w0, it["t"])); nblocks += 1
            pos = end + 2
    if pos != len(stream): fail("t/%s: text after the last hop" % rid)
    for o, (name, ln, t) in starts.items():
        if block_at.get(o) != (ln, t): fail("%s: says it starts at lane %d, hop %d; it starts at %s" % (name, ln, t, block_at.get(o, "no hop boundary")))
    return nblocks

# ---------------------------------------------------------------- links
def site_file(url):
    """The dist file a site URL is served from: / -> index.html, /r/x -> r/x.html, /t/x.txt -> t/x.txt."""
    p = urllib.parse.unquote(urllib.parse.urlsplit(url).path).lstrip("/")
    if p == "" or p.endswith("/"): return p + "index.html"
    return p + ".html" if "." not in p.rsplit("/", 1)[-1] else p

def check_site_url(where, url, files):
    if url.split("#")[0].split("?")[0].endswith(".html"): fail("%s: %s redirects (Pages serves /x.html at /x)" % (where, url))
    elif site_file(url) not in files: fail("%s: %s maps to no file in dist" % (where, url))

SITE_URL = re.compile(re.escape(SITE) + r"[^\s<>\"'()\[\]]*")
def site_urls(s): return [u.rstrip(".,;:") for u in SITE_URL.findall(s)]

def check_links(rel, links, files):
    """Every href/src of one page; returns how many were checked."""
    n = 0
    for tag, rel_attr, url in links:
        if url == "" or url.startswith(("#", "data:")): continue
        n += 1
        if url == SITE or url.startswith(SITE + "/"):
            check_site_url(rel, url, files)
            if rel_attr == "canonical" and site_file(url) != rel: fail("%s: canonical %s is another page" % (rel, url))
            continue
        sp = urllib.parse.urlsplit(url)
        if sp.scheme in ("http", "https"): continue
        if sp.scheme or sp.netloc: fail("%s: unexpected link %s" % (rel, url)); continue
        p = urllib.parse.unquote(sp.path)
        if not p: continue
        if rel == "404.html" and not p.startswith("/"): fail("404.html: %s is not root-absolute" % url)
        target = posixpath.normpath(p.lstrip("/") if p.startswith("/") else posixpath.join(posixpath.dirname(rel), p))
        if p.endswith("/") or target in (".", ".."): target = posixpath.normpath(posixpath.join(target, "index.html"))
        if target.startswith(".."): fail("%s: %s leaves the site" % (rel, url))
        elif target not in files: fail("%s: %s -> %s, no such file" % (rel, url, target))
    return n

# ---------------------------------------------------------------- authored text
def authored():
    """(where, text) for every string the site's builders wrote."""
    out = [("SITE_TITLE", C.SITE_TITLE), ("SITE_SUB", C.SITE_SUB), ("ANNEX_INTRO", C.ANNEX_INTRO), ("POEM_HEAD", C.POEM_HEAD),
           ("MAP_NOTE", C.MAP_NOTE), ("FOR_MODELS", C.FOR_MODELS)]
    out += [("INTRO", s) for s in C.INTRO] + [("INTRO_AFTER_SEED", s) for s in C.INTRO_AFTER_SEED]
    for r in C.ROOMS + [C.ROOM_QWEN_NEXT] + C.EXTRA_ROOMS + C.LATER_ROOMS + C.ANNEX:
        out += [("room %s %s" % (r["id"], k), r[k]) for k in ("title", "note", "content_note") if r.get(k)]
        out += [("room %s lane label" % r["id"], ln["label"]) for ln in r["lanes"] if ln.get("label")]
    for f in C.FAMILIES: out += [("family %s title" % f["id"], f["title"]), ("family %s blurb" % f["id"], f["blurb"])]
    for h, b in C.COLOPHON: out += [("COLOPHON", h), ("COLOPHON " + h, b)]
    return out

def lint(where, s):
    plain = B.QUOTE.sub("", s)    # quotes from the data are not authored
    if "—" in plain: fail("em dash in authored text (%s): %r" % (where, plain[max(0, plain.index("—") - 40):][:80]))
    if "resonat" in plain.lower(): fail("'resonates' in authored text (%s)" % where)
    if re.search(r"here['’]?s what", plain.lower()): fail("banned opener in authored text (%s)" % where)

# ---------------------------------------------------------------- main
def main():
    if not (DIST / "llms.txt").is_file(): sys.exit("no build in %s (python build.py first)" % DIST)
    runs, index, extra, exp = R.load_all()
    rep = json.loads((DIST.parent / "build_report.json").read_text(encoding="utf-8"))   # build.py writes it beside the build
    files = {p.relative_to(DIST).as_posix(): p.stat().st_size for p in DIST.rglob("*") if p.is_file()}
    defs = {r["id"]: r for r in C.ROOMS + [C.ROOM_QWEN_NEXT] + C.EXTRA_ROOMS + C.LATER_ROOMS + C.ANNEX}
    room_ids = rep["rooms"] + rep["annex"]
    pages = {p[2:-5] for p in files if p.startswith("r/") and p.endswith(".html")}
    for rid in sorted(set(room_ids) - pages): fail("r/%s.html missing (build_report.json lists the room)" % rid)
    for rid in sorted(pages - set(room_ids)): fail("r/%s.html is not a room in build_report.json" % rid)

    # 1. every page: links; room pages: every hop
    n_hops = n_lanes = n_links = 0; room_lanes = {}; texts = {}
    for rel in sorted(p for p in files if p.endswith(".html")):
        s, pg = read_page(DIST / rel)
        texts[rel] = s
        n_links += check_links(rel, pg.links, files)
        if not rel.startswith("r/"):
            if pg.rooms: fail("%s: has a room section" % rel)
            continue
        rid = rel[2:-5]
        if len(pg.rooms) != 1: fail("%s: %d room sections" % (rel, len(pg.rooms))); continue
        if pg.rooms[0]["id"] != rid: fail("%s: section id %s" % (rel, pg.rooms[0]["id"]))
        if pg.rooms[0]["annex"] != (rid in rep["annex"]): fail("%s: annex class does not match build_report.json" % rel)
        d = defs.get(rid)
        if d is None: fail("%s: no room definition in copy.py or src/rooms_*.py" % rel)
        else:
            want = def_lanes(d)
            got = [(ln["run"], ln["tag"], ln["ext_run"], ln["ext_tag"]) for ln in pg.lanes]
            if want != got: fail("%s: lanes %s, the room definition has %s" % (rel, got, want))
        lanes = []
        for ln in pg.lanes:
            n_lanes += 1
            key = (ln["run"], ln["tag"], ln["ext_run"], ln["ext_tag"])
            e, why = lane_items(runs, *key)
            if e is None: fail("%s %s/%s: %s" % (rel, ln["run"], ln["tag"], why)); continue
            n_hops += len(ln["hops"])
            check_page_lane("%s %s/%s" % (rel, ln["run"], ln["tag"]), ln, e)
            lanes.append((key, e))
        rules = sorted({e["rule"] for _, e in lanes if e["rule"]})
        if sorted(set(pg.rules)) != rules: fail("%s: rule text differs from X_0" % rel)
        if len(lanes) == len(pg.lanes): room_lanes[rid] = (lanes, rules)

    # 2. every text version (lanes as on the room page; from the room's definition when the page is missing)
    part_sizes = []; n_blocks = 0
    for rid in room_ids:
        if rid not in room_lanes and rid not in pages and rid in defs:
            lanes = [(k, lane_items(runs, *k)[0]) for k in def_lanes(defs[rid])]
            if all(e for _, e in lanes): room_lanes[rid] = (lanes, sorted({e["rule"] for _, e in lanes if e["rule"]}))
        if rid in room_lanes: n_blocks += check_text(rid, *room_lanes[rid], part_sizes)
        else: fail("t/%s not checked: its lanes could not be read" % B.part_name(rid, 1))
    known = {n for _, n in part_sizes} | {"t/poem.txt", "t/colophon.txt"}
    for p in sorted(p for p in files if p.startswith("t/") and p not in known): fail("%s: not a part of any room" % p)

    # 3. site URLs, robots, sitemap, llms
    for p in sorted(p for p in files if p.endswith((".txt", ".xml"))):
        s = (DIST / p).read_text(encoding="utf-8"); texts[p] = s
        for u in site_urls(s): n_links += 1; check_site_url(p, u, files)
    robots = texts.get("robots.txt", "").splitlines()
    if "User-agent: *" not in robots or "Allow: /" not in robots or any(l.startswith("Disallow:") and l[9:].strip() for l in robots):
        fail("robots.txt does not allow everything")
    if "Sitemap: %s/sitemap.xml" % SITE not in robots: fail("robots.txt does not name the sitemap")
    locs = re.findall(r"<loc>(.*?)</loc>", texts.get("sitemap.xml", ""))
    for u in locs:
        if not u.startswith(SITE + "/"): fail("sitemap.xml: %s is not a site URL" % u)
    listed = {site_file(u) for u in locs}
    for p in sorted(p for p in files if p.endswith((".html", ".txt")) and p not in ("404.html", "robots.txt") and p not in listed):
        fail("sitemap.xml does not list %s" % p)
    llms = texts.get("llms.txt", "")
    for rid in room_ids:
        if "%s/t/%s" % (SITE, B.part_name(rid, 1)) not in llms: fail("llms.txt does not list room %s" % rid)

    # 4. authored text
    strings = authored()
    for where, s in strings: lint(where, s)
    for p, s in sorted(texts.items()):
        if "PLACEHOLDER" in s: fail("%s: PLACEHOLDER rendered" % p)

    # 5. the poem, verbatim against the brief
    brief = (LOOP / "FABLE_BRIEF.md").read_text(encoding="utf-8")
    if C.POEM not in brief: fail("poem text differs from FABLE_BRIEF.md")
    if C.POEM_TITLE not in brief or C.POEM_SIGN not in brief: fail("poem title/sign differ from the brief")
    if C.POEM not in texts.get("t/poem.txt", ""): fail("t/poem.txt does not hold the poem verbatim")

    # 6. sizes
    for p, v in sorted(files.items()):
        if v > MAX_FILE: fail("%s: %d bytes, over Cloudflare Pages' 25 MiB per file" % (p, v))
    big_room = max(((v, p) for p, v in files.items() if p.startswith("r/")), default=(0, "-"))
    big_part = max(part_sizes, default=(0, "-"))

    print("checked %d hops in %d lanes on %d room pages, %d hop blocks in %d text parts, %d links, %d authored strings; %d failures"
          % (n_hops, n_lanes, len(pages), n_blocks, len(part_sizes), n_links, len(strings), len(fails)))
    print("sizes: largest room page %s %s bytes; largest text part %s %s characters (limit %s); dist %d files, %s bytes"
          % (big_room[1], "{:,}".format(big_room[0]), big_part[1], "{:,}".format(big_part[0]), "{:,}".format(B.TEXT_PART), len(files), "{:,}".format(sum(files.values()))))
    for f in fails: print("  FAIL", f)
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
