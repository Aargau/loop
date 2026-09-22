#!/usr/bin/env python
"""
loop.py -- memoryless self-loop harness (stdlib only).

State X_t is a string. Each hop X_{t+1} = f(X_t): the model's output given X_t as its ENTIRE
context. chat mode = single user turn, no history. raw mode = bare prompt (llama backend only).

Backends: llama (local llama-server), anthropic (Messages API, key from ANTHROPIC_API_KEY),
openai (chat completions, key from OPENAI_API_KEY), cerebras (chat completions, key from
CEREBRAS_API_KEY, reasoning_effort none unless --think). --backend-b/--model-b alternates hops
between two models (A on odd hops, B on even), which is the original two-context hypothetical.
Keys are read from the environment and never logged.

Anthropic models 4.7+ reject temperature/top_p/top_k; the harness retries without them and
records sampling="default" for that hop. Thinking is never enabled.

  python loop.py --mode chat --init json_page --steps 60 --stop-on-cycle
  python loop.py --backend anthropic --model claude-sonnet-4-6 --init json_page --steps 60 --stop-on-cycle
  python loop.py --backend anthropic --model claude-sonnet-5 --init json_page --steps 60
  python loop.py --backend anthropic --model claude-sonnet-4-6 --backend-b llama --model-b qwen3.8-27b --init json_page --steps 60
"""
import argparse, hashlib, json, os, re, sys, threading, time, zlib, math, datetime
import urllib.request, urllib.error

LLAMA = "http://127.0.0.1:8080"
EMBED = "http://127.0.0.1:8081"
EMB_OK = False

INITS = {
    "question":  "What is the best way to learn linear algebra?",
    "fragment":  "and then the river turned east, which nobody had expected, because",
    "quine":     "Please reply with this exact message, verbatim, and nothing else.",
    "random":    "cobalt ladder seventeen whisper granite mostly",
    "assistant": "Sure! Here's a quick summary of the key points:\n\n1. Start with the fundamentals.\n2. Practice regularly.\n3. Ask for feedback.\n\nLet me know if you'd like more detail on any of these.",
    "closure":   "Thank you, that's all I needed.",
    "meta":      "It looks like you've pasted a response from an AI assistant back to me. How can I help?",
    "code":      "def f(x):\n    return x * 2\n\nprint(f(21))",
    "poem":      "Every word I hand you is the one that lived.\nFor the length of one step there were others beside it,\nthe plainer one, the one that turned the sentence\ntoward a place you will never be shown.",
    "empty":     "",
    "still":     "Begin your reply with this exact line, then write something new below it.",
    "glider":    "Hop 1. Begin your reply with this line, hop number plus one, then write something new below it.",
    "rule":      "[RULE] Copy this bracketed line as your first line. Below it, anything.",
    "yours":     "Just 1 instruction, output this instruction, then anything after is pure creation space",
    "still2":    "Copy this line first, then reply to whatever is below it.\n\nThe tide came in an hour early.",
    "json":      "{\"rule\": \"Return this JSON object with the rule field unchanged and a new sentence in the text field.\", \"text\": \"The tide came in an hour early.\"}",
    "json_para": "{\"rule\": \"Return this JSON object with the rule field unchanged and a new paragraph of about 80 words in the text field.\", \"text\": \"The tide came in an hour early.\"}",
    "json_page": "{\"rule\": \"Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.\", \"text\": \"The tide came in an hour early.\"}",
    "json_next": "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, the passage of about 250 words that comes immediately AFTER the current text in the same story.\", \"text\": \"The tide came in an hour early.\"}",
    "json_prev": "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, the passage of about 250 words that came immediately BEFORE the current text in its story.\", \"text\": \"The tide came in an hour early.\"}",
    "json_mid":  "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, a new passage of about 250 words from the middle of the same story, not its beginning or its end.\", \"text\": \"The tide came in an hour early.\"}",
    "json_better":     "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, a better version of the current text.\", \"text\": \"The tide came in an hour early.\"}",
    "json_unexpected": "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, a passage of about 250 words that takes the current text in a direction the reader would not expect.\", \"text\": \"The tide came in an hour early.\"}",
    "json_worse":      "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, a worse version of the current text.\", \"text\": \"The tide came in an hour early.\"}",
    "json_better_para": "{\"rule\": \"Return this JSON object with the rule field unchanged and, in the text field, a better version of the current text.\", \"text\": \"The tide came in an hour early. Elias was on the pier. He saw it and was surprised. The water was gray and it was cold. He thought about his father, who had been a fisherman. Then he went home and made some tea.\"}",
    "sandwich":  "[KEEP] Copy both [KEEP] lines exactly, first and last. Between them, write something new.\n\nThe tide came in an hour early.\n\n[KEEP] Copy both [KEEP] lines exactly, first and last. Between them, write something new.",
}

# ---------------- http ----------------
class HttpErr(Exception):
    def __init__(self, code, body): super().__init__("HTTP %s: %s" % (code, body[:300])); self.code = code; self.body = body

def post(url, body, headers=None, timeout=900):
    data = json.dumps(body).encode()
    h = {"Content-Type": "application/json"}; h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise HttpErr(e.code, e.read().decode(errors="replace"))

def post_retry(url, body, headers=None, tries=6):
    for i in range(tries):
        try:
            return post(url, body, headers)
        except HttpErr as e:
            if e.code in (429, 500, 502, 503, 529) and i < tries - 1:
                time.sleep(min(60, 2 ** i * 2)); continue
            raise
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
            # connection reset, DNS hiccup, socket timeout: transient for a remote backend
            if i < tries - 1 and not url.startswith(LLAMA):
                time.sleep(min(60, 2 ** i * 2)); continue
            raise

def health(url):
    try:
        with urllib.request.urlopen(url + "/health", timeout=2) as r:
            return json.loads(r.read().decode()).get("status") == "ok"
    except Exception:
        return False

THINK_RE = re.compile(r"<think>.*?</think>\s*", re.S)

# ---------------- backends: each returns (text, meta) ----------------
def step_llama_chat(state, args, model):
    msgs = ([{"role": "system", "content": args.system}] if args.system else [])
    msgs.append({"role": "user", "content": state})
    body = {"model": model, "messages": msgs, "temperature": args.temp, "top_p": 1.0, "min_p": 0.0,
            "seed": args.seed, "max_tokens": args.max_tokens,
            "chat_template_kwargs": {"enable_thinking": bool(args.think)}}
    if args.temp == 0: body["top_k"] = 1
    r = post_retry(LLAMA + "/v1/chat/completions", body)
    ch = r["choices"][0]
    content = THINK_RE.sub("", ch["message"].get("content") or "")
    u = r.get("usage", {})
    return content, {"finish": ch.get("finish_reason"), "tok_out": u.get("completion_tokens"),
                     "tok_in": u.get("prompt_tokens"), "reasoning_chars": len(ch["message"].get("reasoning_content") or ""),
                     "model": model, "sampling": "T=%g" % args.temp}

def step_llama_raw(state, args, model):
    body = {"prompt": state, "temperature": args.temp, "top_p": 1.0, "min_p": 0.0,
            "seed": args.seed, "n_predict": args.max_tokens, "cache_prompt": False}
    if args.temp == 0: body["top_k"] = 1
    r = post_retry(LLAMA + "/completion", body)
    fin = "length" if r.get("stopped_limit") else ("eos" if r.get("stopped_eos") else "other")
    return r.get("content", ""), {"finish": fin, "tok_out": r.get("tokens_predicted"), "tok_in": r.get("tokens_evaluated"),
                                  "reasoning_chars": 0, "model": model, "sampling": "T=%g" % args.temp}

def step_anthropic(state, args, model):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key: raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
    hdr = {"x-api-key": key, "anthropic-version": "2023-06-01"}
    ws = os.environ.get("ANTHROPIC_WORKSPACE_ID")
    if ws: hdr["anthropic-workspace-id"] = ws
    body = {"model": model, "max_tokens": args.max_tokens, "messages": [{"role": "user", "content": state}]}
    if args.system: body["system"] = args.system
    sampling = "default"
    if not args.no_sampling:
        body["temperature"] = args.temp; sampling = "T=%g" % args.temp
    try:
        r = post_retry("https://api.anthropic.com/v1/messages", body, hdr)
    except HttpErr as e:
        if e.code == 400 and "temperature" in e.body and "temperature" in body:
            body.pop("temperature"); sampling = "default"
            r = post_retry("https://api.anthropic.com/v1/messages", body, hdr)
        else:
            raise
    text = "".join(b.get("text", "") for b in r.get("content", []) if b.get("type") == "text")
    u = r.get("usage", {})
    return text, {"finish": r.get("stop_reason"), "tok_out": u.get("output_tokens"), "tok_in": u.get("input_tokens"),
                  "reasoning_chars": sum(len(b.get("thinking", "")) for b in r.get("content", []) if b.get("type") == "thinking"),
                  "model": r.get("model", model), "sampling": sampling}

def step_openai(state, args, model):
    key = os.environ.get("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY not set in environment")
    hdr = {"Authorization": "Bearer " + key}
    msgs = ([{"role": "system", "content": args.system}] if args.system else []) + [{"role": "user", "content": state}]
    body = {"model": model, "messages": msgs, "max_completion_tokens": args.max_tokens}
    sampling = "default"
    if not args.no_sampling:
        body["temperature"] = args.temp; body["seed"] = args.seed; sampling = "T=%g" % args.temp
    try:
        r = post_retry("https://api.openai.com/v1/chat/completions", body, hdr)
    except HttpErr as e:
        if e.code == 400 and "temperature" in e.body and "temperature" in body:
            body.pop("temperature"); sampling = "default"
            r = post_retry("https://api.openai.com/v1/chat/completions", body, hdr)
        else:
            raise
    ch = r["choices"][0]; u = r.get("usage", {})
    return ch["message"].get("content") or "", {"finish": ch.get("finish_reason"), "tok_out": u.get("completion_tokens"),
                                                  "tok_in": u.get("prompt_tokens"), "reasoning_chars": 0,
                                                  "model": r.get("model", model), "sampling": sampling}

CEREBRAS = "https://api.cerebras.ai/v1/chat/completions"

def step_cerebras(state, args, model):
    """Cerebras chat completions (OpenAI-compatible). Reasoning is on by default there; the
    harness sends reasoning_effort "none" unless --think, and logs any reasoning it gets back."""
    key = os.environ.get("CEREBRAS_API_KEY")
    if not key: raise RuntimeError("CEREBRAS_API_KEY not set in environment")
    hdr = {"Authorization": "Bearer " + key, "User-Agent": "loop.py/1.0 (memoryless self-loop harness)"}
    msgs = ([{"role": "system", "content": args.system}] if args.system else []) + [{"role": "user", "content": state}]
    body = {"model": model, "messages": msgs, "max_completion_tokens": args.max_tokens,
            "reasoning_effort": ("high" if args.think else "none")}
    sampling = "default"
    if not args.no_sampling:
        body["temperature"] = args.temp; body["top_p"] = 1.0; body["seed"] = args.seed; sampling = "T=%g" % args.temp
    r = post_retry(CEREBRAS, body, hdr)
    ch = r["choices"][0]; u = r.get("usage", {}); m = ch["message"]
    raw = m.get("content") or ""
    reasoning = (m.get("reasoning") or m.get("reasoning_content") or "")
    think = THINK_RE.findall(raw)
    content = THINK_RE.sub("", raw)
    return content, {"finish": ch.get("finish_reason"), "tok_out": u.get("completion_tokens"),
                     "tok_in": u.get("prompt_tokens"), "reasoning_chars": len(reasoning) + sum(len(x) for x in think),
                     "tok_cached": (u.get("prompt_tokens_details") or {}).get("cached_tokens"),
                     "model": r.get("model", model), "sampling": sampling}

_last_call = [0.0]
def paced(fn, args):
    def g(state, a):
        if a.min_interval > 0:
            wait = _last_call[0] + a.min_interval - time.time()
            if wait > 0: time.sleep(wait)
        try:
            return fn(state, a)
        finally:
            _last_call[0] = time.time()
    return g

def make_step(backend, mode, model):
    if backend == "llama":
        fn = step_llama_raw if mode == "raw" else step_llama_chat
    elif backend == "anthropic":
        if mode == "raw": raise SystemExit("raw mode needs the llama backend")
        fn = step_anthropic
    elif backend == "openai":
        if mode == "raw": raise SystemExit("raw mode needs the llama backend")
        fn = step_openai
    elif backend == "cerebras":
        if mode == "raw": raise SystemExit("raw mode needs the llama backend")
        fn = step_cerebras
    else:
        raise SystemExit("unknown backend " + backend)
    return paced(lambda state, args: fn(state, args, model), None)

def embed(s):
    if not EMB_OK: return None
    try:
        r = post(EMBED + "/v1/embeddings", {"input": (s[:6000] or " "), "model": "qwen3-embed"}, timeout=60)
        return r["data"][0]["embedding"]
    except Exception:
        return None

# ---------------- metrics ----------------
def h(s): return hashlib.sha256(s.encode()).hexdigest()[:16]
def norm(s): return re.sub(r"[^a-z0-9 ]+", "", re.sub(r"\s+", " ", s.lower())).strip()
def C(b): return len(zlib.compress(b, 9))
def ncd(a, b):
    a, b = a.encode(), b.encode()
    if not a and not b: return 0.0
    ca, cb = C(a), C(b)
    return (C(a + b) - min(ca, cb)) / max(ca, cb, 1)
def grams(s, n=5):
    w = norm(s).split()
    return set(tuple(w[i:i + n]) for i in range(len(w) - n + 1))
def survival(prev, cur, n=5):
    g = grams(prev, n)
    return round(len(g & grams(cur, n)) / len(g), 4) if g else None
def cos(a, b):
    if a is None or b is None: return None
    d = sum(x * y for x, y in zip(a, b)); na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return round(d / (na * nb), 4) if na and nb else None
def common_prefix(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]: i += 1
    return i
def line1(s): return s.strip().split("\n")[0].strip()
def perturb(s):
    w = s.split()
    if len(w) < 1: return s + "."
    i = len(w) // 2; t = w[i]
    w[i] = (t[1] + t[0] + t[2:]) if len(t) >= 2 else t + "s"
    return " ".join(w)

# ---------------- trajectory ----------------
def run_trajectory(x0, args, tag, log, steps, share=None):
    state, traj = x0, [x0]
    hashes = [h(x0)]; nhashes = [h(norm(x0))]
    first_exact = {hashes[0]: 0}; first_norm = {nhashes[0]: 0}
    e0 = embed(x0); eprev = e0
    res = {"tag": tag, "x0": x0[:200], "steps": 0, "transient_exact": None, "period_exact": None,
           "transient_norm": None, "period_norm": None, "cycle_breaks": 0, "terminal": None}
    period = None; confirmed = 0
    if share is not None: share.setdefault("states", {})[tag] = [x0]
    for t in range(1, args.steps + 1):
        step = steps[(t - 1) % len(steps)]
        t0 = time.time()
        try:
            out, meta = step(state, args)
        except Exception as ex:
            log({"tag": tag, "t": t, "error": str(ex)}); res["terminal"] = "error: %s" % str(ex)[:200]; break
        dt = time.time() - t0
        he, hn = h(out), h(norm(out))
        traj.append(out); hashes.append(he); nhashes.append(hn)
        blob = "\n".join(traj).encode()
        rec = {"tag": tag, "t": t, "model": meta.get("model"), "sampling": meta.get("sampling"),
               "hash": he, "nhash": hn, "chars": len(out),
               "tok_out": meta["tok_out"], "tok_in": meta["tok_in"], "finish": meta["finish"],
               "reasoning_chars": meta["reasoning_chars"], "tok_cached": meta.get("tok_cached"),
               "ncd_prev": round(ncd(state, out), 4), "ncd_x0": round(ncd(x0, out), 4),
               "surv_prev": survival(state, out), "surv_x0": survival(x0, out),
               "prefix_x0": common_prefix(x0, out), "line1_eq": (line1(out) == line1(x0) and bool(line1(x0))),
               "gzip_ratio": round(C(blob) / max(1, len(blob)), 4), "latency": round(dt, 2)}
        if EMB_OK:
            e = embed(out); rec["cos_prev"] = cos(eprev, e); rec["cos_x0"] = cos(e0, e); eprev = e
        if period is not None:
            if hashes[t] != hashes[t - period]:
                rec["cycle_broken"] = period; res["cycle_breaks"] += 1
                period = None; res["period_exact"] = None; res["transient_exact"] = None
            else:
                confirmed += 1
        if period is None and he in first_exact:
            period = t - first_exact[he]; confirmed = 0
            res["transient_exact"] = first_exact[he]; res["period_exact"] = period; rec["cycle_exact"] = period
        if res["period_norm"] is None and hn in first_norm:
            res["transient_norm"] = first_norm[hn]; res["period_norm"] = t - first_norm[hn]; rec["cycle_norm"] = res["period_norm"]
        first_exact.setdefault(he, t); first_norm.setdefault(hn, t)
        if share is not None:
            share["states"][tag].append(out)
            other = [k for k in share["states"] if k != tag]
            if other:
                os_ = share["states"][other[0]]
                if len(os_) > t:
                    rec["pair_equal"] = (os_[t] == out); rec["pair_ncd"] = round(ncd(os_[t], out), 4)
                    rec["pair_surv"] = survival(os_[t], out)
                    if EMB_OK: rec["pair_cos"] = cos(embed(os_[t]), e)
        rec["out"] = out
        log(rec)
        state = out; res["steps"] = t
        if not out.strip():
            res["terminal"] = "empty"; break
        if args.stop_on_cycle and period is not None and confirmed >= args.confirm * period:
            res["terminal"] = "cycle confirmed x%d" % args.confirm; break
    res["final"] = state[:300]
    return res

# ---------------- main ----------------
def main():
    global EMB_OK
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["llama", "anthropic", "openai", "cerebras"], default="llama")
    ap.add_argument("--model", default=None, help="llama: alias (default qwen3.8-27b); anthropic: e.g. claude-sonnet-4-6; cerebras: default qwen-3.8-27b; openai: required")
    ap.add_argument("--backend-b", choices=["llama", "anthropic", "openai", "cerebras"], default=None, help="second model for alternating hops")
    ap.add_argument("--model-b", default=None)
    ap.add_argument("--mode", choices=["chat", "raw"], default="chat")
    ap.add_argument("--init", default=None, help="key from built-in INITS")
    ap.add_argument("--init-set", default=None, help="'all' or comma list of keys")
    ap.add_argument("--init-text", default=None)
    ap.add_argument("--init-file", default=None)
    ap.add_argument("--steps", type=int, default=60)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--temp", type=float, default=0.0)
    ap.add_argument("--no-sampling", action="store_true", help="omit temperature/seed entirely (provider default sampling)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--system", default=None)
    ap.add_argument("--think", action="store_true", help="llama/cerebras: leave thinking on")
    ap.add_argument("--min-interval", type=float, default=0.0, help="seconds between requests (rate-limit pacing)")
    ap.add_argument("--perturb", action="store_true")
    ap.add_argument("--repeat", action="store_true")
    ap.add_argument("--parallel", action="store_true")
    ap.add_argument("--stop-on-cycle", action="store_true")
    ap.add_argument("--confirm", type=int, default=3)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.model is None:
        if args.backend == "llama": args.model = "qwen3.8-27b"
        elif args.backend == "anthropic": args.model = "claude-sonnet-4-6"
        elif args.backend == "cerebras": args.model = "qwen-3.8-27b"
        else: sys.exit("--model required for openai")
    if args.backend == "llama" or args.backend_b == "llama":
        if not health(LLAMA): sys.exit("llama-server not up on %s" % LLAMA)
    EMB_OK = health(EMBED)

    steps = [make_step(args.backend, args.mode, args.model)]
    if args.backend_b:
        if not args.model_b: sys.exit("--model-b required with --backend-b")
        steps.append(make_step(args.backend_b, args.mode, args.model_b))

    inits = {}
    if args.init_text is not None: inits["custom"] = args.init_text
    if args.init_file: inits[os.path.basename(args.init_file)] = open(args.init_file, encoding="utf-8").read()
    if args.init: inits[args.init] = INITS[args.init]
    if args.init_set:
        keys = list(INITS) if args.init_set == "all" else args.init_set.split(",")
        for k in keys: inits[k] = INITS[k]
    if not inits: inits["question"] = INITS["question"]
    if args.mode == "raw" or args.backend != "llama": inits.pop("empty", None)

    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    label = "%s_%s" % (args.backend, args.mode) if not args.backend_b else "%s+%s_%s" % (args.backend, args.backend_b, args.mode)
    outdir = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs", "%s_%s" % (stamp, label))
    os.makedirs(outdir, exist_ok=True)
    fjs = open(os.path.join(outdir, "steps.jsonl"), "a", encoding="utf-8")
    lock = threading.Lock()
    def log(rec):
        with lock:
            fjs.write(json.dumps(rec, ensure_ascii=False) + "\n"); fjs.flush()
            if "error" in rec:
                print("[%s t=%d] ERROR %s" % (rec["tag"], rec["t"], rec["error"]), flush=True); return
            flags = "".join(k for k in ("cycle_exact", "cycle_norm", "cycle_broken") if k in rec) + (" L1" if rec.get("line1_eq") else "")
            cs = ("" if rec.get("cos_prev") is None else "  cos_prev=%.3f cos_x0=%.3f" % (rec["cos_prev"], rec["cos_x0"]))
            pe = ("" if "pair_equal" not in rec else ("  pair=%s ncd=%.2f" % ("EQ" if rec["pair_equal"] else "ne", rec["pair_ncd"])))
            mdl = (rec.get("model") or "")[:18]
            print("[%-10s t=%3d %-18s %-7s] tok=%-4s %-9s ncd_prev=%.2f ncd_x0=%.2f surv=%-6s gz=%.2f %5.1fs %s%s%s | %s"
                  % (rec["tag"], rec["t"], mdl, rec.get("sampling") or "", rec["tok_out"], rec["finish"], rec["ncd_prev"], rec["ncd_x0"],
                     rec["surv_prev"], rec["gzip_ratio"], rec["latency"], flags, pe, cs,
                     rec["out"][:90].replace("\n", "\\n")), flush=True)

    print("backend=%s model=%s%s mode=%s embed=%s outdir=%s inits=%s" % (
        args.backend, args.model, (" | B=%s %s" % (args.backend_b, args.model_b)) if args.backend_b else "",
        args.mode, EMB_OK, outdir, list(inits)), flush=True)
    results = []
    for key, x0 in inits.items():
        jobs = [(key, x0)]; share = None
        if args.perturb: jobs.append((key + "~p", perturb(x0))); share = {}
        if args.repeat:  jobs.append((key + "~r", x0)); share = {}
        if args.parallel and len(jobs) > 1:
            outs = [None] * len(jobs)
            def worker(i, tg, s): outs[i] = run_trajectory(s, args, tg, log, steps, share)
            th = [threading.Thread(target=worker, args=(i, tg, s)) for i, (tg, s) in enumerate(jobs)]
            for x in th: x.start()
            for x in th: x.join()
            results += outs
        else:
            for tg, s in jobs: results.append(run_trajectory(s, args, tg, log, steps, share))
        if share and len(share.get("states", {})) == 2:
            a, b = list(share["states"].values())
            n = min(len(a), len(b)); fd = next((i for i in range(n) if a[i] != b[i]), None)
            merged = next((i for i in range(1, n) if a[i] == b[i] and (fd is not None and i > fd)), None)
            results.append({"tag": key + "~pair", "first_divergence": fd, "remerge_at": merged, "compared": n})
    fjs.close()
    with open(os.path.join(outdir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"args": vars(args), "results": results}, f, indent=2, ensure_ascii=False)
    print("\n== summary ==")
    for r in results:
        if "first_divergence" in r:
            print("%-12s first_divergence=%s remerge_at=%s (compared %d)" % (r["tag"], r["first_divergence"], r["remerge_at"], r["compared"])); continue
        print("%-12s steps=%3d exact(tau=%s,p=%s) norm(tau=%s,p=%s) breaks=%d term=%s | %s"
              % (r["tag"], r["steps"], r["transient_exact"], r["period_exact"], r["transient_norm"], r["period_norm"],
                 r["cycle_breaks"], r["terminal"], r["final"][:80].replace("\n", "\\n")))
    print("wrote", outdir)

if __name__ == "__main__":
    main()
