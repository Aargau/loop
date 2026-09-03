# -*- coding: utf-8 -*-
"""episodes.py: copy episodes at the text level for any run in site/runs_extra.

    python episodes.py cb_div_ledger_nohook [more runs...]
    python episodes.py "cb_div_*"

An episode is a maximal run of consecutive hops whose text field equals the previous hop's
text. Reports start, end, length, whether it escaped (a later hop differs) and, for ledger
runs, whether the history was appended to during the episode.
"""
import json, sys, pathlib, glob
HERE = pathlib.Path(__file__).resolve().parent; LOOP = HERE.parent
sys.path.insert(0, str(LOOP)); sys.path.insert(0, str(HERE))
import build as B

def parse(out):
    m = B.FENCE.match(out); s = m.group(1) if m else out
    try: return json.loads(s)
    except Exception: return None

def episodes(name):
    d = HERE / "runs_extra" / name
    hops = [json.loads(l) for l in (d / "steps.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    hops = list({h["t"]: h for h in hops if "t" in h and "out" in h}.values()); hops.sort(key=lambda h: h["t"])
    tag = hops[0]["tag"]
    x0 = B.x0_for(tag, name)
    texts = [B.split_x0(x0)[1]] + [B.text_of(h["out"])[0] for h in hops]
    objs = [parse(x0)] + [parse(h["out"]) for h in hops]
    n = len(hops)
    eps = []; t = 1
    while t <= n:
        if texts[t] == texts[t - 1]:
            s = t
            while t + 1 <= n and texts[t + 1] == texts[t]: t += 1
            e = t
            hist_grew = None
            if isinstance(objs[s - 1], dict) and "history" in objs[s - 1] and isinstance(objs[e], dict):
                hist_grew = len(objs[e].get("history", [])) - len(objs[s - 1].get("history", []))
            eps.append(dict(start=s, end=e, length=e - s + 1, escaped=e < n, hist_grew=hist_grew, line=texts[s].split("\n")[0][:60]))
        t += 1
    distinct = len(set(texts[1:]))
    copies = sum(e["length"] for e in eps)
    print("== %s: %d hops, %d distinct texts, %d copied hops in %d episodes, longest %d, %s" % (
        name, n, distinct, copies, len(eps), max([e["length"] for e in eps], default=0),
        "final state is a copy (absorbed)" if eps and not eps[-1]["escaped"] else "every episode escaped" if eps else "no copies"))
    for e in eps:
        print("   hops %3d..%-3d (%2d) %s%s | %s" % (e["start"], e["end"], e["length"], "escaped" if e["escaped"] else "ABSORBED",
                                                     ("" if e["hist_grew"] is None else ", history +%d" % e["hist_grew"]), e["line"]))
    return eps

if __name__ == "__main__":
    names = []
    for a in sys.argv[1:] or ["cb_div_*"]:
        names += [pathlib.Path(p).name for p in sorted(glob.glob(str(HERE / "runs_extra" / a))) if (pathlib.Path(p) / "steps.jsonl").exists()]
    for nm in names: episodes(nm)
