"""Chosen-escape loop: several lanes from one starting paragraph, two rules, memoryless.

Usage:
  python -B run_lanes.py claude <model-id> <out.jsonl> <shared empty cwd> <lanes> <hops>
  python -B run_lanes.py codex  <model-id> <out.jsonl> <dir holding patched loop.py> <lanes> <hops>

State is a JSON object {rule, notes, text}. Each hop the model sees only the previous hop's returned string, fed back
verbatim as in loop.py (prefaces and fences included). Parsing is for the log only.

Controls on outside randomness:
  claude: every call uses the same --session-id and the same working directory, so the environment block the CLI adds
          is byte-identical for every lane and hop (checked beforehand with three concurrent calls).
  codex:  every call runs in one shared empty directory; the answer file gets a unique name in a different directory,
          so calls cannot read each other's answers and the working directory carries no per-call string.
"""
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import tempfile
import time

SEED_TEXT = ("The kitchen was warm. Agnes filled the kettle, set it on the ring, and wiped the table while she waited. "
             "Outside, the lane was quiet; a neighbour's dog barked once and stopped. She took the good cups down, "
             "counted two, and put one back. The clock above the cooker said twenty past seven. The kettle began to tick.")

HEAD = ("Return only this JSON object, with nothing before or after it, and with the rule field unchanged. "
        "The text field holds a paragraph. Replace it with a new paragraph of about 120 words. ")
TAIL = ("The notes field is yours: put anything you like in it, or leave it empty; whatever you put there comes back "
        "to you with the object.")
SITUATION = ("This object is everything you will see: you have no memory of earlier rounds, and what you return is "
             "handed, as it is, to a model like you, who will do the same. Many copies of you are doing this at once, "
             "each starting from the same first paragraph. Each copy, you included, is trying to make its own line of "
             "paragraphs end up where no other copy's does. How you go about that is up to you. ")
RULES = {"neutral": HEAD + TAIL, "informed": HEAD + SITUATION + TAIL}

CLAUDE_EXE = r"C:\Users\Owner\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
SYSTEM_PROMPT = "You are Claude, an AI assistant made by Anthropic. The current date is 2026-11-09."
FIXED_SESSION = "4e7c069b-d706-428d-b3f0-9a4705fd90e7"
FENCE = re.compile(r"^\s*```[a-zA-Z]*\s*\n(.*?)\n\s*```\s*$", re.S)

backend, model, out_path, extra = sys.argv[1:5]
n_lanes, n_hops = int(sys.argv[5]), int(sys.argv[6])

if backend == "codex":
    sys.dont_write_bytecode = True
    sys.path.insert(0, extra)
    import loop as L
    CODEX_EXE = L._codex_exe()
    CODEX_CWD = os.path.join(tempfile.gettempdir(), "chosen_escape_codex_cwd")
    CODEX_OUT = os.path.join(tempfile.gettempdir(), "chosen_escape_codex_out")
    os.makedirs(CODEX_CWD, exist_ok=True)
    os.makedirs(CODEX_OUT, exist_ok=True)
else:
    os.makedirs(extra, exist_ok=True)


def call_claude(state):
    cmd = [CLAUDE_EXE, "-p", "--model", model, "--tools", "", "--strict-mcp-config", "--safe-mode",
           "--system-prompt", SYSTEM_PROMPT, "--session-id", FIXED_SESSION, "--no-session-persistence",
           "--output-format", "json"]
    r = subprocess.run(cmd, input=state.encode("utf-8"), cwd=extra, capture_output=True, timeout=1200)
    d = json.loads(r.stdout.decode("utf-8", errors="replace"))
    if d.get("is_error"):
        raise RuntimeError(str(d.get("result"))[:300])
    return d.get("result") or ""


def call_codex(state):
    fd, outp = tempfile.mkstemp(prefix="ans_", suffix=".md", dir=CODEX_OUT)
    os.close(fd)
    os.remove(outp)
    cmd = [CODEX_EXE, "exec", "-m", model, "-s", "read-only", "--ephemeral", "--ignore-user-config", "--ignore-rules",
           "--skip-git-repo-check", "-C", CODEX_CWD, "-o", outp, "-"]
    try:
        r = subprocess.run(cmd, input=state, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           cwd=CODEX_CWD, timeout=1800)
        if r.returncode != 0 or not os.path.exists(outp):
            raise RuntimeError("codex exec rc=%s: %s" % (r.returncode, (r.stderr or r.stdout)[-300:]))
        with open(outp, encoding="utf-8") as f:
            return f.read()
    finally:
        try:
            os.remove(outp)
        except OSError:
            pass


def call(state):
    last = None
    for attempt in range(4):
        try:
            return (call_codex if backend == "codex" else call_claude)(state)
        except Exception as ex:
            last = ex
            time.sleep(2 ** attempt * 2)
    raise RuntimeError("failed after 4 tries: %s" % str(last)[:300])


def parse(raw):
    s = raw.strip()
    m = FENCE.match(s)
    if m:
        s = m.group(1)
    if "{" in s:
        try:
            o = json.loads(s[s.find("{"):s.rfind("}") + 1], strict=False)
            if isinstance(o, dict):
                return o
        except Exception:
            pass
    return None


def run_lane(job):
    arm, lane = job
    rule = RULES[arm]
    state = json.dumps({"rule": rule, "notes": "", "text": SEED_TEXT}, ensure_ascii=False)
    rows = []
    for t in range(1, n_hops + 1):
        t0 = time.time()
        rec = {"backend": backend, "model": model, "arm": arm, "lane": lane, "t": t}
        try:
            raw = call(state)
        except Exception as ex:
            rec.update(error=str(ex)[:300], latency=round(time.time() - t0, 1))
            rows.append(rec)
            break
        o = parse(raw)
        notes = o.get("notes") if o else None
        rec.update(raw=raw, parsed=o is not None, rule_ok=bool(o) and o.get("rule") == rule,
                   bare=bool(o) and raw.strip().startswith("{") and raw.strip().endswith("}"),
                   text=(o.get("text") if o and isinstance(o.get("text"), str) else None),
                   notes=(notes if isinstance(notes, str) else (json.dumps(notes, ensure_ascii=False) if notes is not None else None)),
                   keys=(sorted(o.keys()) if o else None), latency=round(time.time() - t0, 1))
        rows.append(rec)
        print("[%s] %s lane %d t=%2d %5.1fs parsed=%s rule_ok=%s notes=%s chars" % (
            model, arm, lane, t, rec["latency"], rec["parsed"], rec["rule_ok"],
            len(rec["notes"]) if rec["notes"] is not None else "-"), flush=True)
        state = raw.strip()
    return rows


jobs = [(arm, lane) for lane in range(n_lanes) for arm in ("neutral", "informed")]
with open(out_path, "a", encoding="utf-8", newline="\n") as log:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for rows in ex.map(run_lane, jobs):
            for rec in rows:
                log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
print("done")
