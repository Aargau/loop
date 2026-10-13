# -*- coding: utf-8 -*-
"""experiments.py: load the 22 September studies (experiments/*_20260922*) as site runs.

Those studies used their own recording runner, not loop.py: one directory per stream,
NNN.request.json + NNN.response.json per hop. This module turns each stream into a run with
the same shape build.load_extra() returns, so the reader renders it like any other lane.

A hop is a response with stream_status "active": the model's visible output, which the runner
forwarded unchanged as the whole next input. Anything else (a provider refusal, an HTTP error,
a dropped connection) ends the stream and is reported as the lane's terminal note, not as a hop.
The chain is checked on load: every request after the first must carry exactly the previous
response's output, and every output must match its recorded sha256.

Run ids are the stream's path under experiments/, e.g. "operators_20260922/worse/gpt-6-astra".
"""
import hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
LOOP = HERE.parent
EXP = LOOP / "experiments"
sys.path.insert(0, str(LOOP))
import loop as L

# (run id, stream directory, tag) for every stream the site shows. The 22 September pilot
# (experiments/basins_20260922) is left out, as its own report leaves it out; so is Sol's sunset_b,
# which lost its connection after eight hops and was replaced by a fresh stream (AMENDMENT_SOL_REPLACEMENT.md).
MODELS = ["gpt-6-luna", "gpt-6-sol", "gpt-6-astra", "claude-fable-5-1", "claude-opus-5-5"]

def streams():
    out = []
    for m in MODELS:
        for s in ("sunset_a", "sunset_b", "tide"):
            if m == "gpt-6-sol" and s == "sunset_b":
                out.append(("basins_20260922_sol_replacement/gpt-6-sol", EXP / "basins_20260922_sol_replacement/raw/gpt-6-sol/sunset_replacement", "sunset_replacement"))
            else:
                out.append(("basins_20260922_sunset/%s/%s" % (m, s), EXP / "basins_20260922_sunset/raw" / m / s, s))
    for op in ("better", "worse", "previous", "next"):
        for m in MODELS:
            out.append(("operators_20260922/%s/%s" % (op, m), EXP / "operators_20260922" / op / "raw" / m / "sunset", op))
    for d in ("previous", "next"):
        for m in MODELS:
            if m == "claude-fable-5-1": continue   # excluded from the explicit-fiction study at Justin's request
            out.append(("fictional_20260922/%s/%s" % (d, m), EXP / "fictional_20260922" / d / "raw" / m / "sunset", "fiction_" + d))
    return out

def _sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()

def _user_content(req):
    msgs = req["body"]["messages"]
    c = msgs[-1]["content"]
    if isinstance(c, list): c = "".join(b.get("text", "") for b in c if b.get("type") == "text")
    return c

def _tok_out(u):
    if not u: return None
    return u.get("completion_tokens", u.get("output_tokens"))

def _terminal(resp, hop):
    st = resp.get("stream_status") or ""
    if st == "empty_output" and resp.get("finish_reason") == "refusal":
        return "provider refusal at hop %d, no visible text" % hop
    if st.startswith("abnormal_finish:refusal"):
        return "provider refusal at hop %d after partial text" % hop
    if st.startswith("http_error"):
        return "HTTP %s at hop %d" % (resp.get("http_status"), hop)
    return "%s at hop %d" % (st.replace("_", " "), hop)

def load_stream(run_id, d, tag, text_of):
    reqs = sorted(d.glob("*.request.json"))
    if not reqs: raise SystemExit("no requests in %s" % d)
    x0 = _user_content(json.loads(reqs[0].read_text(encoding="utf-8")))
    hops = []; prev = x0; terminal = None; model = None; refusal_detail = None
    for rq in reqs:
        n = int(rq.name.split(".")[0])
        req = json.loads(rq.read_text(encoding="utf-8"))
        model = req.get("model") or model
        sent = _user_content(req)
        if sent != prev: raise SystemExit("%s hop %d: request does not carry the previous output" % (run_id, n))
        rp = rq.with_name(rq.name.replace(".request.", ".response."))
        if not rp.exists():
            terminal = "no response recorded at hop %d" % n; break
        resp = json.loads(rp.read_text(encoding="utf-8"))
        if resp.get("stream_status") != "active":
            terminal = _terminal(resp, n)
            try:
                body = json.loads(resp.get("response_body") or "{}")
                det = body.get("stop_details") or {}
                if det: refusal_detail = det
            except Exception:
                pass
            break
        out = resp["output"]
        if resp.get("output_sha256") and _sha(out) != resp["output_sha256"]:
            raise SystemExit("%s hop %d: output does not match its recorded sha256" % (run_id, n))
        text, parsed = text_of(out)
        hops.append({"t": n, "tag": tag, "model": resp.get("returned_model") or model, "sampling": "default",
                     "text": text, "text_is_json_field": parsed, "raw": out,
                     "tok_out": _tok_out(resp.get("usage")), "finish": resp.get("finish_reason"),
                     "cos_prev": None, "cos_x0": None,
                     "ncd_prev": round(L.ncd(prev, out), 4), "ncd_x0": round(L.ncd(x0, out), 4),
                     "surv_prev": L.survival(prev, out), "surv_x0": L.survival(x0, out),
                     "gzip_ratio": None, "latency": resp.get("latency_seconds"),
                     "cycle_exact": None, "cycle_norm": None, "cycle_broken": None})
        prev = out
    for i, h in enumerate(hops):
        if h["t"] != i + 1: raise SystemExit("%s: hop numbering has a gap at %d" % (run_id, h["t"]))
    # first exact revisit of a whole visible output. Not "transient_exact": these streams were sampled and
    # never stopped on a cycle, so a revisit need not hold; build.py decides that from the hops themselves.
    first = {x0: 0}; summ = {}
    for h in hops:
        if h["raw"] in first and not summ:
            summ = {"first_revisit_of": first[h["raw"]], "first_revisit_at": h["t"]}
        first.setdefault(h["raw"], h["t"])
    result = dict(tag=tag, terminal=terminal, **summ)
    if refusal_detail: result["refusal_detail"] = refusal_detail
    return {"meta": {"run": run_id, "model": model, "mode": "chat", "hops": len(hops), "tags": [tag],
                     "summary": {"results": [result]}, "superseded": 0, "x0": x0, "source": str(d.relative_to(LOOP)).replace("\\", "/"),
                     "settings": "low effort, provider-default sampling, 4096-token budget"},
            "hops": hops}

def load_experiments(text_of):
    """text_of is build.text_of, so these runs are decoded exactly like every other run."""
    return {rid: load_stream(rid, d, tag, text_of) for rid, d, tag in streams()}

if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    import build as B
    runs = load_experiments(B.text_of)
    tot = 0
    for rid, r in runs.items():
        res = r["meta"]["summary"]["results"][0]
        tot += r["meta"]["hops"]
        print("%-52s %3d hops  %s" % (rid, r["meta"]["hops"], {k: v for k, v in res.items() if k != "tag" and v is not None}))
    print("%d streams, %d hops" % (len(runs), tot))
