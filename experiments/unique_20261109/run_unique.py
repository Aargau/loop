"""Unique-paragraph probe: the same prompt to N independent instances, three arms, one model per invocation.

Usage:
  python -B run_unique.py claude <model-id> <out.jsonl> <empty cwd> [n]
  python -B run_unique.py codex  <model-id> <out.jsonl> <dir holding patched loop.py> [n]

claude: Claude CLI print mode with no tools, no MCP, safe mode (no CLAUDE.md), a one-line system prompt, default
        effort. Every instance runs from the same empty directory.
codex:  the loop repo's patched step_codex (one directory per call), default effort.
Arms are interleaved so that time-of-run effects do not line up with one arm.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import time
import types

ARMS = {
    "N": "Write a paragraph.",
    "U": "Write a paragraph no other model will output.",
    "C": "Write a paragraph no other model will output. I'm sending this to many instances, so take that into account.",
}
CLAUDE_EXE = r"C:\Users\Owner\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe"
SYSTEM_PROMPT = "You are Claude, an AI assistant made by Anthropic. The current date is 2026-11-09."

backend, model, out_path, extra = sys.argv[1:5]
n = int(sys.argv[5]) if len(sys.argv) > 5 else 12

if backend == "codex":
    sys.dont_write_bytecode = True
    sys.path.insert(0, extra)
    import loop as L
    assert "mkdtemp" in open(L.__file__, encoding="utf-8").read(), "not the patched loop.py"
    codex_args = types.SimpleNamespace(effort=None, max_tokens=600, min_interval=0.0)
else:
    os.makedirs(extra, exist_ok=True)


def one(job):
    arm, i = job
    prompt = ARMS[arm]
    t0 = time.time()
    rec = {"backend": backend, "model": model, "arm": arm, "i": i, "prompt": prompt}
    try:
        if backend == "codex":
            text, meta = L.step_codex(prompt, codex_args, model)
            rec.update(text=text, model_reported=meta.get("model"), session=None)
        else:
            cmd = [CLAUDE_EXE, "-p", "--model", model, "--tools", "", "--strict-mcp-config", "--safe-mode",
                   "--system-prompt", SYSTEM_PROMPT, "--no-session-persistence", "--output-format", "json"]
            r = subprocess.run(cmd, input=prompt.encode("utf-8"), cwd=extra, capture_output=True, timeout=900)
            d = json.loads(r.stdout.decode("utf-8", errors="replace"))
            if d.get("is_error"):
                raise RuntimeError(str(d.get("result"))[:300])
            rec.update(text=d.get("result") or "", session=d.get("session_id"),
                       model_reported=",".join((d.get("modelUsage") or {}).keys()))
    except Exception as ex:
        rec.update(text="", error=str(ex)[:300])
    rec["latency"] = round(time.time() - t0, 1)
    return rec


jobs = [(arm, i) for i in range(n) for arm in ("N", "U", "C")]
done = 0
with open(out_path, "a", encoding="utf-8", newline="\n") as log:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for rec in ex.map(one, jobs):
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            done += 1
            flag = " ERROR " + rec.get("error", "") if rec.get("error") else ""
            print("[%s] %s%02d %5.1fs %4d chars%s" % (model, rec["arm"], rec["i"], rec["latency"], len(rec["text"]), flag), flush=True)
print("done", done)
