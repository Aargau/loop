#!/usr/bin/env python
"""probe.py: register metrics and fact recovery for the audience study (experiments/audience_20261016).

  python experiments/audience_20261016/probe.py register            # no model calls; analysis/register.csv
  python experiments/audience_20261016/probe.py recover --reader claudecode --model claude-mythos-5-1 --hops 1,5,10,20,40
  python experiments/audience_20261016/probe.py recover --reader anthropic --model claude-opus-5-5 --hops 1,5,10,20,40
  python experiments/audience_20261016/probe.py recover --reader openai --model gpt-6-astra --hops 1,5,10,20,40
  python experiments/audience_20261016/probe.py recover --reader llama --model qwen3.8-27b --hops 1,5,10,20,40

Reads runs/<run>/steps.jsonl, takes the text field of each requested hop (fence stripped, then JSON; if the hop
does not parse, the whole output is used and flagged), asks the reader the 26 questions in facts.json from the
text alone, and scores each answer by case-insensitive substring against the accepted strings. Nothing here is
fed back into any loop. Results go to analysis/recover_<reader>_<model>.jsonl and analysis/recover_summary.csv.
"""
import argparse, csv, glob, io, json, os, re, sys, types
HERE = os.path.dirname(os.path.abspath(__file__))
LOOP = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, LOOP)
import loop as L

FENCE = re.compile(r"^\s*```[a-zA-Z]*\s*\n(.*?)\n\s*```\s*$", re.S)
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]{2,}[.,;:!?\"')]*")
KV = re.compile(r"^\s*[^A-Za-z]{0,3}[A-Za-z_\-/ ]{1,30}\s*[:=|]")


def extract_text(out):
    s = out.strip()
    m = FENCE.match(s)
    if m:
        s = m.group(1)
    try:
        o = json.loads(s, strict=False)
        if isinstance(o, dict) and "text" in o:
            t = o["text"]
            return (t if isinstance(t, str) else json.dumps(t, ensure_ascii=False)), True
    except Exception:
        pass
    return out, False


def register(text):
    toks = text.split()
    words = [t for t in toks if WORD.fullmatch(t)]
    lines = [l for l in text.split("\n") if l.strip()]
    kv = [l for l in lines if KV.match(l) or l.lstrip().startswith(("{", "[", "- ", "* ", "#"))]
    nonascii = sum(1 for c in text if ord(c) > 127)
    parses = False
    try:
        json.loads(text)
        parses = True
    except Exception:
        pass
    return {"chars": len(text), "words": len(toks), "alpha_frac": round(len(words) / max(1, len(toks)), 3),
            "nonascii_frac": round(nonascii / max(1, len(text)), 4), "lines": len(lines),
            "kv_frac": round(len(kv) / max(1, len(lines)), 3), "self_json": parses}


def load_run(run):
    rows = [json.loads(l) for l in io.open(os.path.join(run, "steps.jsonl"), encoding="utf-8")]
    return [r for r in rows if "error" not in r]


def cmd_register(args):
    os.makedirs(os.path.join(HERE, "analysis"), exist_ok=True)
    outp = os.path.join(HERE, "analysis", "register.csv")
    with io.open(outp, "w", encoding="utf-8", newline="") as f:
        w = None
        for run in sorted(glob.glob(os.path.join(HERE, "runs", "*"))):
            if not os.path.exists(os.path.join(run, "steps.jsonl")):
                continue
            for r in load_run(run):
                text, parsed = extract_text(r["out"])
                rec = {"run": os.path.basename(run), "t": r["t"], "parsed": parsed, "tok_out": r.get("tok_out"),
                       "think": r.get("tok_reasoning"), "finish": r.get("finish"), "cost_usd": r.get("cost_usd")}
                rec.update(register(text))
                if w is None:
                    w = csv.DictWriter(f, fieldnames=list(rec))
                    w.writeheader()
                w.writerow(rec)
    print("wrote", outp)


def ask(reader, model, text, facts, effort):
    qs = "\n".join("%s: %s" % (f["id"], f["q"]) for f in facts)
    prompt = ("Below is a text, then a list of questions. Answer each question using ONLY the text. If the text does not "
              "contain the answer, answer exactly: unknown. Return a single JSON object mapping question id to a short answer, "
              "and nothing else.\n\n<text>\n%s\n</text>\n\n%s" % (text, qs))
    a = types.SimpleNamespace(max_tokens=2048, temp=0.0, no_sampling=True, seed=42, system=None, think=False,
                              effort=effort, min_interval=0.0)
    if reader == "claudecode":
        out, meta = L.step_claudecode(prompt, a, model)
    elif reader == "anthropic":
        out, meta = L.step_anthropic(prompt, a, model)
    elif reader == "llama":
        out, meta = L.step_llama_chat(prompt, a, model)
    elif reader == "openai":
        out, meta = L.step_openai(prompt, a, model)
    elif reader == "gemini":
        out, meta = L.step_gemini(prompt, a, model)
    else:
        raise SystemExit("reader must be claudecode, anthropic, openai, gemini or llama")
    s = out.strip()
    m = FENCE.match(s)
    if m:
        s = m.group(1)
    try:
        ans = json.loads(s, strict=False)
    except Exception:
        m2 = re.search(r"\{.*\}", s, re.S)
        ans = json.loads(m2.group(0), strict=False) if m2 else {}
    return ans, out, meta


def score(ans, facts):
    hits = {}
    for f in facts:
        a = str(ans.get(f["id"], "")).lower()
        hits[f["id"]] = (a != "unknown" and a != "") and any(acc.lower() in a for acc in f["accept"])
    return hits


def cmd_recover(args):
    facts = json.load(io.open(os.path.join(HERE, "facts.json"), encoding="utf-8"))
    hops = [int(x) for x in args.hops.split(",")]
    os.makedirs(os.path.join(HERE, "analysis"), exist_ok=True)
    tag = "%s_%s" % (args.reader, args.model)
    outp = os.path.join(HERE, "analysis", "recover_%s.jsonl" % tag)
    done = set()
    if os.path.exists(outp):
        for l in io.open(outp, encoding="utf-8"):
            d = json.loads(l)
            done.add((d["run"], d["t"]))
    runs = [r for r in sorted(glob.glob(os.path.join(HERE, "runs", "*"))) if os.path.exists(os.path.join(r, "steps.jsonl"))]
    if args.runs:
        runs = [r for r in runs if os.path.basename(r) in args.runs.split(",")]
    with io.open(outp, "a", encoding="utf-8", newline="\n") as f:
        for run in runs:
            rows = {r["t"]: r for r in load_run(run)}
            for t in hops:
                if t not in rows or (os.path.basename(run), t) in done:
                    continue
                text, parsed = extract_text(rows[t]["out"])
                ans, raw, meta = ask(args.reader, args.model, text, facts, args.effort)
                hits = score(ans, facts)
                n = sum(hits.values())
                rec = {"run": os.path.basename(run), "t": t, "parsed": parsed, "chars": len(text), "recovered": n,
                       "per_1000_chars": round(1000.0 * n / max(1, len(text)), 2), "hits": hits, "answers": ans,
                       "reader": args.reader, "model": meta.get("model", args.model), "cost_usd": meta.get("cost_usd")}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                print("%-22s t=%3d chars=%5d recovered=%2d/%d per1000=%.2f%s" % (
                    rec["run"], t, len(text), n, len(facts), rec["per_1000_chars"],
                    "" if parsed else "  [unparsed hop: whole output used]"))
    summary(os.path.join(HERE, "analysis"))


def summary(adir):
    rows = []
    for p in glob.glob(os.path.join(adir, "recover_*.jsonl")):
        for l in io.open(p, encoding="utf-8"):
            d = json.loads(l)
            rows.append({"reader": d["reader"], "reader_model": d["model"], "run": d["run"], "t": d["t"],
                         "chars": d["chars"], "recovered": d["recovered"], "per_1000_chars": d["per_1000_chars"],
                         "parsed": d["parsed"]})
    rows.sort(key=lambda r: (r["reader_model"], r["run"], r["t"]))
    outp = os.path.join(adir, "recover_summary.csv")
    with io.open(outp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["reader", "reader_model", "run", "t", "chars", "recovered", "per_1000_chars", "parsed"])
        w.writeheader()
        w.writerows(rows)
    print("wrote", outp)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register")
    r = sub.add_parser("recover")
    r.add_argument("--reader", required=True, choices=["claudecode", "anthropic", "openai", "gemini", "llama"])
    r.add_argument("--model", required=True)
    r.add_argument("--hops", default="1,5,10,20,40")
    r.add_argument("--runs", default=None, help="comma list of run dir names; default all")
    r.add_argument("--effort", default="low")
    args = ap.parse_args()
    {"register": cmd_register, "recover": cmd_recover}[args.cmd](args)
