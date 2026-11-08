#!/usr/bin/env python
"""ring.py: a ring of N text cells updated synchronously, each seeing its own text and the last sentence of its two
neighbours. The 1-D cellular-automaton version of the memoryless loop (loop.py). Uses loop.py's backends.

  python ring.py --backend cerebras --model qwen-3.8-27b --cells 7 --steps 40 --temp 0 \
      --seed-file experiments/ring_20261017/seeds/plain.txt --disturb-file experiments/ring_20261017/seeds/disturb.txt \
      --rule-file experiments/ring_20261017/rule.txt --out experiments/ring_20261017/runs/cerebras_qwen_n7
  (several disturbed cells: --disturb 0=seeds/jug.txt,8=seeds/panic.txt; --disturb-file F is exactly --disturb 0=F)

Each hop t: for every cell i the harness builds {"rule", "left": last sentence of cell i-1, "text": cell i,
"right": last sentence of cell i+1} (indices mod N), calls the model once per cell with that object as the only user
message, and takes the returned object's text field as cell i's new text. All N calls read the state at hop t-1 and
all N results are written together, so call order does not matter. Returns that do not parse as JSON with a text
field keep the raw output as the cell's text (logged as parsed=false), as loop.py does.

Logs ring.jsonl: one record per hop with every cell's text, hash, word count, finish and parse flag; plus
summary.json. Models may be given per cell with --models m0,m1,... (one per cell; same backend) for a heterogeneous
ring. Keys from the environment as loop.py expects. Nothing is retried beyond loop.py's post_retry.
"""
import argparse, concurrent.futures, hashlib, io, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loop as L

FENCE = re.compile(r"^\s*```[a-zA-Z]*\s*\n(.*?)\n\s*```\s*$", re.S)
SENT = re.compile(r"(?<=[.!?])\s+(?=[\"'A-Z])")


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def last_sentence(text):
    parts = [p.strip() for p in SENT.split(text.strip()) if p.strip()]
    return parts[-1] if parts else text.strip()


def parse_text(out):
    s = out.strip()
    m = FENCE.match(s)
    if m:
        s = m.group(1)
    for cand in (s, s[s.find("{"):] if "{" in s else None):
        if not cand:
            continue
        try:
            o = json.loads(cand, strict=False)
            if isinstance(o, dict) and isinstance(o.get("text"), str):
                return o["text"], True
        except Exception:
            pass
    return out, False


def parse_disturb(spec, disturb_file, N):
    """--disturb 'POS=FILE[,POS=FILE...]' -> {pos mod N: path}; --disturb-file F is {0: F}. Both at once, a malformed
    item or a position named twice (after mod N) is an error."""
    if spec and disturb_file:
        raise SystemExit("ring: give --disturb or --disturb-file, not both (--disturb-file F equals --disturb 0=F)")
    if disturb_file:
        return {0: disturb_file}
    dmap = {}
    for item in (spec.split(",") if spec else []):
        pos, sep, path = item.strip().partition("=")
        try:
            p = int(pos)
        except ValueError:
            p = None
        if p is None or not sep or not path:
            raise SystemExit("ring: bad --disturb item %r (want POS=FILE, POS an integer)" % item)
        p %= N
        if p in dmap:
            raise SystemExit("ring: --disturb names cell %d twice (mod %d): %s and %s" % (p, N, dmap[p], path))
        dmap[p] = path
    return dmap


def place_cells(N, seed, disturb_map):
    """Initial ring: disturb_map {pos: text} in the named cells, seed everywhere else."""
    return [disturb_map.get(i, seed) for i in range(N)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", default="cerebras", choices=["llama", "anthropic", "openai", "cerebras", "claudecode", "gemini", "codex"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--models", default=None, help="comma list, one model per cell (heterogeneous ring; same backend)")
    ap.add_argument("--backends", default=None, help="comma list, one backend per cell (with --models)")
    ap.add_argument("--cells", type=int, default=7)
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--seed-file", required=True, help="text placed in every cell except the disturbed ones")
    ap.add_argument("--disturb-file", default=None, help="text placed in cell 0 (default: same as seed); same as --disturb 0=FILE")
    ap.add_argument("--disturb", default=None, help="POS=FILE[,POS=FILE...]: text placed in cell POS (0-based, mod N); not with --disturb-file")
    ap.add_argument("--rule-file", required=True)
    ap.add_argument("--max-tokens", type=int, default=600)
    ap.add_argument("--temp", type=float, default=0.0)
    ap.add_argument("--no-sampling", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--effort", default=None)
    ap.add_argument("--think", action="store_true")
    ap.add_argument("--system", default=None)
    ap.add_argument("--workers", type=int, default=4, help="parallel calls per hop")
    ap.add_argument("--min-interval", type=float, default=0.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    N = args.cells
    rule = io.open(args.rule_file, encoding="utf-8").read().strip()
    seed = io.open(args.seed_file, encoding="utf-8").read().strip()
    dmap = parse_disturb(args.disturb, args.disturb_file, N)
    dtext = {p: io.open(path, encoding="utf-8").read().strip() for p, path in dmap.items()}
    models = args.models.split(",") if args.models else [args.model or {"cerebras": "qwen-3.8-27b", "claudecode": "claude-mythos-5-1", "codex": "gpt-6-astra", "llama": "qwen3.8-27b"}.get(args.backend, args.model)] * N
    backends = args.backends.split(",") if args.backends else [args.backend] * N
    assert len(models) == N and len(backends) == N, "one model and backend per cell"
    steps = {}
    for b in set(backends):
        steps[b] = {"llama": L.step_llama_chat, "anthropic": L.step_anthropic, "openai": L.step_openai, "cerebras": L.step_cerebras,
                    "claudecode": L.step_claudecode, "gemini": L.step_gemini, "codex": L.step_codex}[b]
    os.makedirs(args.out, exist_ok=True)
    log = io.open(os.path.join(args.out, "ring.jsonl"), "a", encoding="utf-8")
    cells = place_cells(N, seed, dtext)
    rec0 = {"t": 0, "cells": [{"i": i, "text": c, "hash": h(c), "words": len(c.split()), "parsed": True, "finish": "seed", "model": models[i]} for i, c in enumerate(cells)]}
    if args.disturb:  # new flag only, so records from --disturb-file runs stay byte-identical
        for p, path in dmap.items():
            rec0["cells"][p]["disturb"] = os.path.basename(path)
    log.write(json.dumps(rec0, ensure_ascii=False) + "\n"); log.flush()
    print("ring N=%d backend=%s models=%s steps=%d out=%s" % (N, ",".join(sorted(set(backends))), ",".join(sorted(set(models))), args.steps, args.out), flush=True)

    def call(i, state_obj):
        s = json.dumps(state_obj, ensure_ascii=False)
        t0 = time.time()
        try:
            out, meta = steps[backends[i]](s, args, models[i])
            text, parsed = parse_text(out)
            return i, text, parsed, meta.get("finish"), meta.get("tok_out"), round(time.time() - t0, 2), None
        except Exception as ex:
            return i, cells[i], False, "error", None, round(time.time() - t0, 2), str(ex)[:300]

    for t in range(1, args.steps + 1):
        objs = []
        for i in range(N):
            objs.append({"rule": rule, "left": last_sentence(cells[(i - 1) % N]), "text": cells[i], "right": last_sentence(cells[(i + 1) % N])})
        results = [None] * N
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
            for i, text, parsed, finish, tok, lat, err in ex.map(lambda i: call(i, objs[i]), range(N)):
                results[i] = (text, parsed, finish, tok, lat, err)
        new = [r[0] for r in results]
        rec = {"t": t, "cells": []}
        for i in range(N):
            text, parsed, finish, tok, lat, err = results[i]
            rec["cells"].append({"i": i, "text": text, "hash": h(text), "words": len(text.split()), "parsed": parsed, "finish": finish,
                                 "tok_out": tok, "latency": lat, "same_as_prev": text == cells[i], "model": models[i], "error": err})
        log.write(json.dumps(rec, ensure_ascii=False) + "\n"); log.flush()
        frozen = sum(1 for c in rec["cells"] if c["same_as_prev"])
        print("t=%3d frozen=%d/%d words=%s finishes=%s" % (t, frozen, N, [c["words"] for c in rec["cells"]], sorted(set(c["finish"] for c in rec["cells"]))), flush=True)
        cells = new
    summary = {"args": vars(args), "cells": N, "steps": args.steps, "models": models, "backends": backends}
    if args.disturb:
        summary["disturb"] = {str(p): dmap[p] for p in sorted(dmap)}
    json.dump(summary, io.open(os.path.join(args.out, "summary.json"), "w", encoding="utf-8", newline="\n"), indent=2)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
