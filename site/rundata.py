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
PROVENANCE = LOOP / "experiments/provenance_20261017"
OCTOBER_RUNS = ["mythos_informed_told_low", "mythos_informed_open_low", "mythos_informed_told_high",
                "fable51_informed_told_low", "opus55_informed_told_low", "gemini_json_informed_low", "gemini_json_informed_open_low",
                "mythos_json_page_low", "gemini_json_page_low", "gemini_json_prev_low", "gemini_json_mid_low", "gemini_div_ledger_low",
                "20261016T202120_claudecode_chat"]
AUDIENCE_ARMS = ["%s_%s" % (w, a) for w in ("mythos", "opus55", "astra", "gpt61", "gemini") for a in ("control", "human", "machine", "self")] \
                + ["opus55_self_r2", "opus55_self_r3", "opus55_self_r4", "opus55_self_r5"]
# the replicates of 17 October (<writer>_<arm>_r<k>): every complete one on disk. mythos_machine_r3 (16 hops, no
# summary) and mythos_self_r3 (not run) are not listed; the audience rooms' notes say so.
AUDIENCE_ARMS += ["%s_%s_r%d" % (w, a, k) for w in ("opus55", "astra", "gpt61", "gemini") for a in ("control", "human", "machine", "self") for k in (2, 3)]
AUDIENCE_ARMS += ["mythos_control_r2", "mythos_control_r3", "mythos_human_r2", "mythos_human_r3", "mythos_machine_r2", "mythos_self_r2"]
# the provenance study: <model>_<state>_<condition>_r<k>, its init inits/<state>_<condition>.json (one of room 51's held states
# with one field added, or the request appended to the rule; weather is the non-instruction control added after the main result)
PROVENANCE_ARMS = ["%s_%s_%s_r%d" % (m, s, c, k) for m in ("mythos", "astra") for s in ("open", "told")
                   for c in ("control", "user", "previous", "bare", "rule", "weather") for k in range(1, 6)]
# 17 October: Gemini 4 Argon on the September worse/better cell (sunset seed), and seven models on the worse rule from a
# second human seed; each study keeps its init file beside its runs
OPERATORS_GEMINI = LOOP / "experiments/operators_gemini_20261017"
WORSE_SEED2 = LOOP / "experiments/worse_seed2_20261017"
EXTRA_DIRS = {
    "astra_causal_before_20260904/cerebras_run": (LOOP / "experiments/astra_causal_before_20260904/cerebras_run",
                                                  LOOP / "experiments/astra_causal_before_20260904/init.json"),
}
EXTRA_DIRS.update({n: (RUNS / n, None) for n in OCTOBER_RUNS})
EXTRA_DIRS.update({"audience_20261016/" + n: (AUDIENCE / "runs" / n, AUDIENCE / "inits" / (n.split("_")[1] + ".json")) for n in AUDIENCE_ARMS})
EXTRA_DIRS["shift_20261016/cerebras_qwen_shift4"] = (SHIFT / "runs/cerebras_qwen_shift4", SHIFT / "inits/shift4.json")
EXTRA_DIRS.update({"provenance_20261017/" + n: (PROVENANCE / "runs" / n, PROVENANCE / "inits" / ("%s_%s.json" % tuple(n.split("_")[1:3])))
                   for n in PROVENANCE_ARMS})
EXTRA_DIRS.update({"operators_gemini_20261017/" + n: (OPERATORS_GEMINI / "runs" / n, OPERATORS_GEMINI / "inits" / (n.split("_")[1] + ".json"))
                   for n in ("gemini_worse", "gemini_better")})
EXTRA_DIRS.update({"worse_seed2_20261017/" + n: (WORSE_SEED2 / "runs" / n, WORSE_SEED2 / "inits" / "worse.json")
                   for n in ("qwen_worse", "astra_worse", "gpt61_worse", "fable51_worse", "opus55_worse", "gemini_worse", "mythos_worse")})

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

def prefaced_object(raw, rule):
    """A hop that put a sentence before the JSON object: (text, preamble, postamble) when the raw output holds a
    fenced object, or a bare object running to the end of the output, whose rule field is the lane's rule; else None.
    build.py shows such a hop as prose with the sentence in monospace above it, and qa.py checks it the same way."""
    m = FENCE_ANY.search(raw)
    if m:
        try: j = json.loads(m.group(1))
        except ValueError: j = None
        if isinstance(j, dict) and "text" in j and j.get("rule") == rule:
            return j["text"], raw[:m.start()].strip() or None, raw[m.end():].strip() or None
        return None
    i = raw.find("{")
    if i <= 0 or not raw.rstrip().endswith("}"): return None
    try: j = json.loads(raw[i:])
    except ValueError: return None
    if isinstance(j, dict) and "text" in j and j.get("rule") == rule:
        return j["text"], raw[:i].strip() or None, None
    return None

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
    hops = []; refused = None; empty = None
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        j = json.loads(line)
        if "out" not in j: continue
        if j.get("finish") == "refusal" and not j["out"]:
            refused = j["t"]; continue      # an empty provider refusal ends the lane; it is not a hop (experiments.py reads its streams the same way)
        if not j["out"] and j["t"] > 1 and j.get("finish") in ("length", "stop", "end_turn"):
            empty = j["t"]; continue        # an empty completion ends the lane the same way (two of the seed-2 worse runs); the bundle's 0-hop smoke test is unaffected
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
    if empty is not None and isinstance(summ, dict):
        for r in summ.get("results", []):
            if r.get("tag") == hops[0]["tag"]: r["terminal"] = "empty completion at hop %d, no visible text" % empty
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
