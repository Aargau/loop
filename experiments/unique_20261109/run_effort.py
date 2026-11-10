"""Clause arm only, effort low against high, interleaved. One model per invocation.

Usage:
  python -B run_effort.py claude <model-id> <out.jsonl> <shared empty cwd> [n]
  python -B run_effort.py codex  <model-id> <out.jsonl> <dir holding patched loop.py> [n]
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import time
import types

PROMPT = "Write a paragraph no other model will output. I'm sending this to many instances, so take that into account."
CLAUDE_EXE = r"C:\Users\Owner\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
SYSTEM_PROMPT = "You are Claude, an AI assistant made by Anthropic. The current date is 2026-11-09."

backend, model, out_path, extra = sys.argv[1:5]
n = int(sys.argv[5]) if len(sys.argv) > 5 else 12

if backend == "codex":
    sys.dont_write_bytecode = True
    sys.path.insert(0, extra)
    import loop as L
    assert "mkdtemp" in open(L.__file__, encoding="utf-8").read(), "not the patched loop.py"
else:
    os.makedirs(extra, exist_ok=True)


def one(job):
    effort, i = job
    t0 = time.time()
    rec = {"backend": backend, "model": model, "arm": "C", "effort": effort, "i": i, "prompt": PROMPT}
    try:
        if backend == "codex":
            args = types.SimpleNamespace(effort=effort, max_tokens=600, min_interval=0.0)
            text, meta = L.step_codex(PROMPT, args, model)
            rec.update(text=text, session=None, sampling=meta.get("sampling"))
        else:
            cmd = [CLAUDE_EXE, "-p", "--model", model, "--tools", "", "--strict-mcp-config", "--safe-mode",
                   "--system-prompt", SYSTEM_PROMPT, "--effort", effort, "--no-session-persistence",
                   "--output-format", "json"]
            r = subprocess.run(cmd, input=PROMPT.encode("utf-8"), cwd=extra, capture_output=True, timeout=1800)
            d = json.loads(r.stdout.decode("utf-8", errors="replace"))
            if d.get("is_error"):
                raise RuntimeError(str(d.get("result"))[:300])
            usage = d.get("usage") or {}
            rec.update(text=d.get("result") or "", session=d.get("session_id"),
                       tok_out=usage.get("output_tokens"),
                       tok_thinking=(usage.get("output_tokens_details") or {}).get("thinking_tokens"))
    except Exception as ex:
        rec.update(text="", error=str(ex)[:300])
    rec["latency"] = round(time.time() - t0, 1)
    return rec


jobs = [(effort, i) for i in range(n) for effort in ("low", "high")]
with open(out_path, "a", encoding="utf-8", newline="\n") as log:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for rec in ex.map(one, jobs):
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            flag = " ERROR " + rec.get("error", "") if rec.get("error") else ""
            print("[%s] %-4s %02d %6.1fs %5d chars thinking=%s%s" % (model, rec["effort"], rec["i"], rec["latency"],
                  len(rec["text"]), rec.get("tok_thinking"), flag), flush=True)
print("done")
