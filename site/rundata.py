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
# 27 and 28 October: one rule carrying two opposing directions (worse and better; before and after; longer and shorter), five models,
# init inits/<rule>.json (the Opus 5.5 runs were relaunched on a fresh key the next morning after a first launch failed at hop 1).
BOTH = LOOP / "experiments/both_20261027"
BOTH_RUNS = ["%s_%s" % (m, r) for r in ("worse_better", "before_after", "longer_shorter") for m in ("qwen", "astra", "gemini", "mythos", "opus55")]
EXTRA_DIRS.update({"both_20261027/" + n: (BOTH / "runs" / n, BOTH / "inits" / (n.split("_", 1)[1] + ".json")) for n in BOTH_RUNS})
# 27 October: assess and bolster. One rule, one seed, five models, sixty hops: the model scores its own passage from 1 to 5 on eight
# qualities (four pairs in tension, not stated as pairs), bolsters the one it scored lowest, rescores, and carries the choice in a
# history field; a blind Fable 5.1 rater scored every passage afterward (analysis/rater_summary.json). One init for all five runs.
ASSESS = LOOP / "experiments/assess_20261027"
ASSESS_RUNS = ["qwen", "mythos", "astra", "gemini", "opus55"]
EXTRA_DIRS.update({"assess_20261027/" + n: (ASSESS / "runs" / n, ASSESS / "inits" / "assess.json") for n in ASSESS_RUNS})

# The ring (experiments/ring_20261017, ring.py): N cells updated at once, each shown its own text and the last sentence of its
# two neighbours. ring.jsonl keeps each cell's returned text field per hop and not the raw output, so a ring lane's hops carry
# raw=None ("not recorded"); the site renders and checks them by their text. One run per ring, one tag per cell ("cell 0" ...).
RING = LOOP / "experiments/ring_20261017"
RING_RUNS = ["mythos_tarnok_n7", "mythos_tarnok_n8", "astra_tarnok_n7", "gemini_tarnok_n7"]
RING_SETTINGS = {"claudecode": "Claude Code print mode, reasoning effort low, provider-default sampling, no output cap",
                 "codex": "Codex exec, reasoning effort low, provider-default sampling, 1024-token budget",
                 "gemini": "API, reasoning effort low, provider-default sampling, 1024-token budget"}

# 9 November 2026: two studies whose scripts keep their own jsonl logs (one record per call), not loop.py's steps.jsonl.
# The chosen-escape loop (experiments/chosen_escape_20261109, run_lanes.py): a memoryless loop over the object {rule, notes, text},
# four lanes per arm (neutral, informed), twenty hops asked for, one log per model. One run per model, one tag per lane ("informed 2").
ESCAPE = LOOP / "experiments/chosen_escape_20261109"
ESCAPE_RUNS = ["mythos", "fable", "astra"]
ESCAPE_ARMS = ["neutral", "informed"]
ESCAPE_SETTINGS = {"claude": "Claude CLI print mode, no tools, a one-line system prompt, one session id and one working directory shared by every call, default effort and sampling",
                   "codex": "Codex exec, one empty working directory shared by every call, default effort and sampling"}
# The unique-paragraph probe (experiments/unique_20261109, run_unique.py and run_effort.py): not a loop. One prompt, twelve independent
# instances per cell, one reply each. One run per cell the site shows, one tag per instance ("r0" to "r11", the log's own index).
# The site reads the two arms that ask for a paragraph no other model will output (U, and C which adds that many instances get the
# prompt), and for the two Claude models the clause arm at low and at high effort. It does not read the neutral arm or Astra's effort
# cells: their numbers are reported from the study's results files, and some of those replies carry a personal name (the repository's
# README for the study says how), which the site leaves out.
UNIQUE = LOOP / "experiments/unique_20261109"
UNIQUE_CELLS = [("%s_%s" % (m, a), m + ".jsonl", "arm", a) for m in ("mythos", "fable", "astra") for a in ("U", "C")] \
               + [("effort_%s_%s" % (m, e), "effort_%s.jsonl" % m, "effort", e) for m in ("mythos", "fable") for e in ("low", "high")]
UNIQUE_SETTINGS = {"claude": "Claude CLI print mode, no tools, a one-line system prompt, every instance from one working directory, provider-default sampling",
                   "codex": "Codex exec, one directory per call, provider-default sampling"}
UNIQUE_NO_RAW = ("This study is not a loop and asks for no JSON object: its log keeps each instance's whole reply as one string, "
                 "and the text above is that string, byte for byte. There is no separate raw output.")

X0 = {}   # run id -> X_0 for runs whose seed is not in loop.INITS or runs_extra/inits (filled by load_all)
X0_TAG = {}   # (run id, tag) -> X_0 when the lanes of one run start from different texts (the ring's cells)

def state_of(h):
    """The string a hop is compared by: its raw output, or its text when the harness kept only the text field (the ring)."""
    return h["raw"] if h.get("raw") is not None else h["text"]

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

RING_SENT = re.compile(r"(?<=[.!?])\s+(?=[\"'A-Z])")     # ring.py's sentence split, for the edges a cell was shown
def last_sentence(text):
    parts = [p.strip() for p in RING_SENT.split(text.strip()) if p.strip()]
    return parts[-1] if parts else text.strip()

def load_ring(name, d):
    """One ring run (ring.jsonl + summary.json) as a run with one lane per cell, tag "cell <i>". Hop 0 of each cell is its
    seed (the disturbed passage in cell 0, the plain passage elsewhere), kept in X0_TAG; the rule is the run's, in meta["rule"].
    The distance metrics are computed here from the texts (as experiments.py does for the September streams), since the ring
    harness logs none. Each hop carries `edges`, the last sentence of each neighbour's text at that hop, which is what the
    cell is shown next (ring.py's last_sentence). None if the run is not on disk."""
    p = d / "ring.jsonl"
    if not p.exists(): return None
    recs = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not recs or recs[0]["t"] != 0: return None
    by_t = {}
    for r in recs: by_t[r["t"]] = r          # a later record for the same t wins, as in load_steps
    ts = sorted(by_t)
    if ts != list(range(len(ts))): raise SystemExit("%s: hops are not numbered 0..n" % name)
    N = len(by_t[0]["cells"])
    rule = (RING / "rule.txt").read_text(encoding="utf-8").strip()
    summ = json.loads((d / "summary.json").read_text(encoding="utf-8")) if (d / "summary.json").exists() else {}
    hops = []; models = set(); edges0 = {}
    for t in ts:
        cells = by_t[t]["cells"]
        if len(cells) != N or [c["i"] for c in cells] != list(range(N)): raise SystemExit("%s hop %d: cells are not 0..%d" % (name, t, N - 1))
        prev = by_t[t - 1]["cells"] if t else None
        for c in cells:
            i = c["i"]; tag = "cell %d" % i
            edges = (last_sentence(cells[(i - 1) % N]["text"]), last_sentence(cells[(i + 1) % N]["text"]))
            if t == 0:
                X0_TAG[(name, tag)] = c["text"]; edges0[tag] = edges; continue
            x0 = X0_TAG[(name, tag)]; pt = prev[i]["text"]
            models.add(c.get("model"))
            hops.append({"t": t, "tag": tag, "cell": i, "model": c.get("model"), "sampling": "default",
                         "text": c["text"], "text_is_json_field": bool(c.get("parsed")), "raw": None, "tok_out": c.get("tok_out"), "finish": c.get("finish"),
                         "cos_prev": None, "cos_x0": None, "ncd_prev": round(L.ncd(pt, c["text"]), 4), "ncd_x0": round(L.ncd(x0, c["text"]), 4),
                         "surv_prev": L.survival(pt, c["text"]), "surv_x0": L.survival(x0, c["text"]), "gzip_ratio": None, "latency": c.get("latency"),
                         "error": c.get("error"), "edges": edges, "cycle_exact": None, "cycle_norm": None, "cycle_broken": None})
    backend = (summ.get("args") or {}).get("backend") or (summ.get("backends") or ["?"])[0]
    return {"meta": {"run": name, "model": " / ".join(sorted(models)), "mode": "ring", "hops": len(hops), "tags": ["cell %d" % i for i in range(N)],
                     "summary": summ, "superseded": 0, "source": str(d.relative_to(LOOP)).replace("\\", "/"), "rule": rule, "cells": N, "x0_is_text": True, "edges0": edges0,
                     "settings": "a ring of %d cells updated together, %d hops; %s" % (N, len(ts) - 1, RING_SETTINGS.get(backend, backend))},
            "hops": hops}

def script_constants(path, names):
    """Module-level constants of a study's script, read from its source without running it (the scripts act on import).
    Only literals: a string, or a dict of strings. A name that is missing or not a literal stops the build."""
    import ast
    out = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names:
            out[node.targets[0].id] = ast.literal_eval(node.value)
    missing = [n for n in names if n not in out]
    if missing: raise SystemExit("%s: no literal %s" % (path, ", ".join(missing)))
    return out

SAFEGUARD = re.compile(r"^failed after (\d+) tries: API Error: (.*?)(?: \(https?://|\. |\n|$)", re.S)
def _call_failed(err, t):
    """A lane's end, from the error its log recorded in place of a reply: the CLI's own first sentence, quoted. The Claude CLI
    reports a safeguard stop as an API error that points at the usage policy; anything else is called a failed call."""
    m = SAFEGUARD.match(err)
    if m and ("safeguards" in err or "/legal/aup" in err):
        return "safeguard stop at hop %d, no reply in %s tries (the CLI's message: %s)" % (t, m.group(1), m.group(2).strip())
    return "the call failed at hop %d, no reply (%s)" % (t, err.split("\n")[0][:160])

def load_escape(name, path):
    """One model's log of the chosen-escape loop as a run with one lane per (arm, lane), tag "<arm> <lane>". Each lane's X_0 is
    built as run_lanes.py builds it, from that script's own strings (the rule for the arm, an empty notes field, the seed
    paragraph), and kept in X0_TAG. A record with an error and no reply ends its lane and is not a hop. The log does not record
    what was sent, so the chain cannot be checked as experiments.py checks its streams; what is checked is that every hop the
    study marked rule_ok carries the arm's rule byte for byte, and that each lane's hops are numbered 1..n with any error last.
    (run_lanes.py sent each hop the previous reply stripped of surrounding whitespace.) Distances are computed here from the
    raw outputs, as experiments.py does. None if the log is not on disk."""
    if not path.exists(): return None
    k = script_constants(ESCAPE / "run_lanes.py", ["SEED_TEXT", "HEAD", "TAIL", "SITUATION"])
    rules = {"neutral": k["HEAD"] + k["TAIL"], "informed": k["HEAD"] + k["SITUATION"] + k["TAIL"]}
    recs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    lanes = {}
    for r in recs: lanes.setdefault((r["arm"], r["lane"]), []).append(r)
    hops = []; results = []; tags = []; model = None; backend = None
    for arm in ESCAPE_ARMS:
        for lane in sorted(l for a, l in lanes if a == arm):
            tag = "%s %d" % (arm, lane)
            rs = sorted(lanes[(arm, lane)], key=lambda r: r["t"])
            if [r["t"] for r in rs] != list(range(1, len(rs) + 1)): raise SystemExit("%s, %s: hops are not numbered 1..n" % (name, tag))
            if any("error" in r for r in rs[:-1]): raise SystemExit("%s, %s: an error record that is not the lane's last" % (name, tag))
            x0 = json.dumps({"rule": rules[arm], "notes": "", "text": k["SEED_TEXT"]}, ensure_ascii=False)
            X0_TAG[(name, tag)] = x0; tags.append(tag)
            prev = x0; terminal = None
            for r in rs:
                model = r["model"]; backend = r["backend"]
                if "error" in r:
                    terminal = _call_failed(r["error"], r["t"]); break
                raw = r["raw"]
                text, parsed = text_of(raw)
                if r.get("rule_ok") and not (parsed and json.loads(FENCE.match(raw).group(1) if FENCE.match(raw) else raw).get("rule") == rules[arm]):
                    raise SystemExit("%s, %s hop %d: marked rule_ok, but the rule is not run_lanes.py's rule for the arm" % (name, tag, r["t"]))
                hops.append({"t": r["t"], "tag": tag, "model": r["model"], "sampling": "default", "text": text, "text_is_json_field": parsed, "raw": raw,
                             "tok_out": None, "finish": None, "cos_prev": None, "cos_x0": None,
                             "ncd_prev": round(L.ncd(prev, raw), 4), "ncd_x0": round(L.ncd(x0, raw), 4),
                             "surv_prev": L.survival(prev, raw), "surv_x0": L.survival(x0, raw), "gzip_ratio": None, "latency": r.get("latency"),
                             "cycle_exact": None, "cycle_norm": None, "cycle_broken": None})
                prev = raw
            results.append(dict(tag=tag, terminal=terminal))
    return {"meta": {"run": name, "model": model, "mode": "chat", "hops": len(hops), "tags": tags, "summary": {"results": results}, "superseded": 0,
                     "source": str(path.relative_to(LOOP)).replace("\\", "/"),
                     "settings": "20 hops asked for; %s" % ESCAPE_SETTINGS.get(backend, backend)},
            "hops": hops}

def load_unique(name, path, key, value):
    """One cell of the unique-paragraph probe (the records of one log whose `key` field is `value`: an arm, or an effort level)
    as a run with one lane per instance, tag "r<i>", each lane a single hop: hop 0 is the prompt the instance was sent, hop 1 its
    whole reply. The reply is the passage (`plain`: shown as prose, not as an object that failed to parse) and there is no raw
    output beside it (raw None; meta no_raw says why). Checked on load: every record's prompt is the one the study's script holds
    for the cell, no record carries an error or an empty reply, and the instances are numbered 0..n-1. The prompt is also the
    run's rule. None if the log is not on disk."""
    if not path.exists(): return None
    recs = [r for r in (json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()) if r.get(key) == value]
    recs.sort(key=lambda r: r["i"])
    if not recs or [r["i"] for r in recs] != list(range(len(recs))): raise SystemExit("%s: instances are not numbered 0..n-1" % name)
    if key == "arm": prompt = script_constants(UNIQUE / "run_unique.py", ["ARMS"])["ARMS"][value]
    else: prompt = script_constants(UNIQUE / "run_effort.py", ["PROMPT"])["PROMPT"]
    hops = []
    for r in recs:
        if r.get("error") or not r["text"]: raise SystemExit("%s, instance %d: an error or an empty reply in the log" % (name, r["i"]))
        if r["prompt"] != prompt: raise SystemExit("%s, instance %d: the logged prompt is not the script's" % (name, r["i"]))
        d = round(L.ncd(prompt, r["text"]), 4)
        hops.append({"t": 1, "tag": "r%d" % r["i"], "model": r["model"], "sampling": "default", "text": r["text"], "text_is_json_field": False, "plain": True,
                     "raw": None, "tok_out": r.get("tok_out"), "finish": None, "cos_prev": None, "cos_x0": None, "ncd_prev": d, "ncd_x0": d,
                     "surv_prev": None, "surv_x0": None, "gzip_ratio": None, "latency": r.get("latency"),
                     "cycle_exact": None, "cycle_norm": None, "cycle_broken": None})
    X0[name] = prompt
    backend = recs[0]["backend"]
    effort = ("reasoning effort %s" % value) if key == "effort" else "default effort"
    return {"meta": {"run": name, "model": recs[0]["model"], "mode": "single", "hops": len(hops), "tags": [h["tag"] for h in hops],
                     "summary": {"results": [dict(tag=h["tag"], terminal=None) for h in hops]}, "superseded": 0,
                     "source": str(path.relative_to(LOOP)).replace("\\", "/"), "rule": prompt, "x0_is_text": True, "no_raw": UNIQUE_NO_RAW,
                     "settings": "%s, %s" % (UNIQUE_SETTINGS.get(backend, backend), effort)},
            "hops": hops}

def load_extra():
    """Runs made after the bundle: site/runs_extra/<name>/ and EXTRA_DIRS, the ring runs, and the two studies of 9 November 2026."""
    out = {}
    for d in sorted((HERE / "runs_extra").glob("*")):
        r = load_steps(d.name, d)
        if r: out[d.name] = r
    for name, (d, init) in EXTRA_DIRS.items():
        r = load_steps(name, d)
        if r:
            out[name] = r
            if init: X0[name] = init.read_text(encoding="utf-8")
    for n in RING_RUNS:
        name = "ring_20261017/" + n
        r = load_ring(name, RING / "runs" / n)
        if r: out[name] = r
    for n in ESCAPE_RUNS:
        name = "chosen_escape_20261109/" + n
        r = load_escape(name, ESCAPE / ("lanes_%s.jsonl" % n))
        if r: out[name] = r
    for n, fname, key, value in UNIQUE_CELLS:
        name = "unique_20261109/" + n
        r = load_unique(name, UNIQUE / fname, key, value)
        if r: out[name] = r
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
    """Full X_0 string for a lane (loop.INITS has the untruncated text; --init-file runs carry the file name as tag; a ring's
    cells each have their own)."""
    if (run, tag) in X0_TAG: return X0_TAG[(run, tag)]
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
