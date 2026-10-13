# -*- coding: utf-8 -*-
"""check_quotes.py: check a module of room definitions before it goes into the site.

    python check_quotes.py src/rooms_growing.py [more modules...]

A module defines ROOMS, a list of dicts like the ones in src/copy.py (id, family, title,
lanes, note, optional content_note). For each room this checks that every lane's (run, tag)
has hops, that every {{run|tag|t|exact substring}} quote occurs in that hop's text or raw
output, and the house style (no em dashes, not "resonates", no "here's what" openers).
Exits non-zero on any failure. Nothing is written.
"""
import importlib.util, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rundata as R

QUOTE = re.compile(r"\{\{([^|]+)\|([^|]+)\|(\d+)\|(.+?)\}\}")

def check(mod_path, runs):
    spec = importlib.util.spec_from_file_location(pathlib.Path(mod_path).stem, mod_path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    fails = []; n_quotes = 0
    for room in m.ROOMS:
        rid = room.get("id", "?")
        for k in ("id", "family", "title", "lanes", "note"):
            if k not in room: fails.append("%s: missing %s" % (rid, k))
        for ln in room.get("lanes", []):
            run = runs.get(ln["run"])
            if run is None: fails.append("%s: unknown run %s" % (rid, ln["run"])); continue
            if not any(h.get("tag") == ln["tag"] for h in run["hops"]) and run["meta"]["hops"]:
                fails.append("%s: run %s has no hops with tag %s" % (rid, ln["run"], ln["tag"]))
        for field in ("title", "note", "content_note"):
            s = room.get(field) or ""
            for q in QUOTE.finditer(s):
                n_quotes += 1
                run, tag, t, text = q.group(1), q.group(2), int(q.group(3)), q.group(4)
                if run not in runs: fails.append("%s: quote cites unknown run %s" % (rid, run)); continue
                hs = [h for h in runs[run]["hops"] if h.get("tag") == tag and h.get("t") == t]
                if not hs: fails.append("%s: quote cites a missing hop: %s" % (rid, q.group(0)[:120])); continue
                if text not in (hs[0].get("text") or "") and text not in (hs[0].get("raw") or ""):
                    fails.append("%s: quote not found in data: %s" % (rid, q.group(0)[:160]))
            plain = QUOTE.sub("", s)
            if "—" in plain: fails.append("%s %s: em dash in authored text" % (rid, field))
            if "resonat" in plain.lower(): fails.append("%s %s: 'resonates'" % (rid, field))
            if re.search(r"here'?s what", plain.lower()): fails.append("%s %s: banned opener" % (rid, field))
    return len(m.ROOMS), n_quotes, fails

def main():
    runs, _, _, _ = R.load_all()
    bad = 0
    for p in sys.argv[1:]:
        n, nq, fails = check(p, runs)
        print("%s: %d rooms, %d quotes, %d failures" % (p, n, nq, len(fails)))
        for f in fails: print("  FAIL", f)
        bad += len(fails)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
