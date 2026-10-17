# -*- coding: utf-8 -*-
"""rundata.py: every run the site can show, loaded one way.

Three sources, one shape (meta + hops, each hop with t, tag, model, text, raw and the metrics):
  data/<run>.json                 the original bundle (export.py)
  site/runs_extra/<run>/          loop.py runs made after the bundle (steps.jsonl + summary.json),
                                  plus loop.py runs kept elsewhere (EXTRA_DIRS)
  experiments/*_20260922*/        the 22 September studies' raw receipts (experiments.py)

Reads only. build.py, qa.py and check_quotes.py all load through load_all().
"""
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent          # site/
LOOP = HERE.parent                                        # loop/
DATA = LOOP / "data"
sys.path.insert(0, str(LOOP))
import loop as L                                          # for INITS
import experiments as E

FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)
FENCE_ANY = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)

# loop.py runs that live outside site/runs_extra: run id -> (directory, init file for its X_0, or None when the
# seed is one of loop.INITS or site/runs_extra/inits)
RUNS = LOOP / "runs"                                      # runs made from the loop directory itself (16 and 17 October 2026)
AUDIENCE = LOOP / "experiments/audience_20261016"
SHIFT = LOOP / "experiments/shift_20261016"
OCTOBER_RUNS = ["mythos_informed_told_low", "mythos_informed_open_low", "mythos_informed_told_high",
                "fable51_informed_told_low", "opus55_informed_told_low", "gemini_json_informed_low", "gemini_json_informed_open_low",
                "mythos_json_page_low", "gemini_json_page_low", "gemini_json_prev_low", "gemini_json_mid_low", "gemini_div_ledger_low",
                "20261016T202120_claudecode_chat"]
AUDIENCE_ARMS = ["%s_%s" % (w, a) for w in ("mythos", "opus55", "astra", "gpt61", "gemini") for a in ("control", "human", "machine", "self")] \
                + ["opus55_self_r2", "opus55_self_r3"]
EXTRA_DIRS = {
    "astra_causal_before_20260904/cerebras_run": (LOOP / "experiments/astra_causal_before_20260904/cerebras_run",
                                                  LOOP / "experiments/astra_causal_before_20260904/init.json"),
}
EXTRA_DIRS.update({n: (RUNS / n, None) for n in OCTOBER_RUNS})
EXTRA_DIRS.update({"audience_20261016/" + n: (AUDIENCE / "runs" / n, AUDIENCE / "inits" / (n.split("_")[1] + ".json")) for n in AUDIENCE_ARMS})
EXTRA_DIRS["shift_20261016/cerebras_qwen_shift4"] = (SHIFT / "runs/cerebras_qwen_shift4", SHIFT / "inits/shift4.json")

X0 = {}   # run id -> X_0 for runs whose seed is not in loop.INITS or runs_extra/inits (filled by load_all)

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

def load_steps(name, d):
    """One loop.py run directory (steps.jsonl + summary.json), decoded like export.py. None if it has no hops."""
    p = d / "steps.jsonl"
    if not p.exists(): return None
    hops = []; refused = None
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        j = json.loads(line)
        if "out" not in j: continue
        if j.get("finish") == "refusal" and not j["out"]:
            refused = j["t"]; continue      # an empty provider refusal ends the lane; it is not a hop (experiments.py reads its streams the same way)
        text, parsed = text_of(j["out"])
        hops.append({"t": j["t"], "tag": j["tag"], "model": j.get("model", "qwen3.8-27b"), "sampling": j.get("sampling", "T=0"),
                     "text": text, "text_is_json_field": parsed, "raw": j["out"], "tok_out": j.get("tok_out"), "finish": j.get("finish"),
                     "cos_prev": j.get("cos_prev"), "cos_x0": j.get("cos_x0"), "ncd_prev": j.get("ncd_prev"), "ncd_x0": j.get("ncd_x0"),
                     "surv_prev": j.get("surv_prev"), "surv_x0": j.get("surv_x0"), "gzip_ratio": j.get("gzip_ratio"), "latency": j.get("latency"),
                     "tok_reasoning": j.get("tok_reasoning"),
                     "cycle_exact": j.get("cycle_exact"), "cycle_norm": j.get("cycle_norm"), "cycle_broken": j.get("cycle_broken")})
    if not hops: return None
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
    if refused is not None and isinstance(summ, dict):
        for r in summ.get("results", []):
            if r.get("tag") == hops[0]["tag"]: r["terminal"] = "provider refusal at hop %d, no visible text" % refused
    return {"meta": {"run": name, "model": "qwen", "mode": "chat", "hops": len(hops), "tags": sorted({h["tag"] for h in hops}),
                     "summary": summ, "superseded": dup, "source": str(d.relative_to(LOOP)).replace("\\", "/")}, "hops": hops}

def load_extra():
    """Runs made after the bundle: site/runs_extra/<name>/ and EXTRA_DIRS."""
    out = {}
    for d in sorted((HERE / "runs_extra").glob("*")):
        r = load_steps(d.name, d)
        if r: out[d.name] = r
    for name, (d, init) in EXTRA_DIRS.items():
        r = load_steps(name, d)
        if r:
            out[name] = r
            if init: X0[name] = init.read_text(encoding="utf-8")
    return out

def load_all():
    """(runs, index, extra, experiments): every run by id, the bundle's index, and the two later sets."""
    runs, index = load_bundle()
    extra = load_extra()
    exp = E.load_experiments(text_of)
    for rid, r in exp.items(): X0[rid] = r["meta"]["x0"]
    runs.update(extra); runs.update(exp)
    return runs, index, extra, exp

def x0_for(tag, run):
    """Full X_0 string for a lane (loop.INITS has the untruncated text; --init-file runs carry the file name as tag)."""
    if run in X0: return X0[run]
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
