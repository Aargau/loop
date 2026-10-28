"""Blind external rater for the assess-and-bolster runs.
Shows Fable 5.1 the qualities and the passage only (no self-scores, history or note) and asks for the same
1 to 5 scores and the weakest quality. Appends one line per (run, hop) to analysis/rater.jsonl; resumable.
Run from the repo root with ANTHROPIC_API_KEY in the environment: python experiments/assess_20261027/rate.py
"""
import io, json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
OUT = os.path.join(HERE, "analysis", "rater.jsonl")
INIT = json.load(io.open(os.path.join(HERE, "inits", "assess.json"), encoding="utf-8"))
QUAL = INIT["qualities"]
MODEL = os.environ.get("RATER_MODEL", "claude-fable-5-1")
SYSTEM = "You rate a passage of prose on eight named qualities. You return only a JSON object and nothing else."
PROMPT = ("Qualities, each with a one-line gloss:\n%s\n\nPassage:\n<<<\n%s\n>>>\n\n"
          "Score the passage from 1 to 5 on every quality, honestly, and name the quality you scored lowest. "
          "Return only this JSON object: {\"scores\": {\"coherence\": n, \"economy\": n, \"floridity\": n, \"grounding\": n, "
          "\"relatability\": n, \"scope\": n, \"strangeness\": n, \"surprise\": n}, \"weakest\": \"...\"}")


def parse_obj(out):
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", out.strip())
    try:
        d = json.loads(s)
        return d if isinstance(d, dict) else None
    except Exception:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
        return None


def call(passage):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY not set")
    hdr = {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
    ws = os.environ.get("ANTHROPIC_WORKSPACE_ID")
    if ws:
        hdr["anthropic-workspace-id"] = ws
    body = {"model": MODEL, "max_tokens": 300, "system": SYSTEM, "output_config": {"effort": "low"},
            "messages": [{"role": "user", "content": PROMPT % (json.dumps(QUAL, indent=1), passage)}]}
    for i in range(6):
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(), headers=hdr)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read().decode())
            text = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
            u = d.get("usage", {})
            return text, u.get("input_tokens"), u.get("output_tokens"), d.get("model")
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503, 529) and i < 5:
                time.sleep(2 ** i); continue
            raise SystemExit("HTTP %s: %s" % (e.code, msg[:500]))


def main():
    done = set()
    if os.path.exists(OUT):
        for l in io.open(OUT, encoding="utf-8"):
            r = json.loads(l); done.add((r["run"], r["t"]))
    names = sorted(d for d in os.listdir(RUNS) if os.path.isdir(os.path.join(RUNS, d)))
    n_done = 0
    with io.open(OUT, "a", encoding="utf-8", newline="\n") as f:
        for name in names:
            for l in io.open(os.path.join(RUNS, name, "steps.jsonl"), encoding="utf-8"):
                r = json.loads(l)
                if "out" not in r or (name, r["t"]) in done:
                    continue
                obj = parse_obj(r["out"])
                passage = (obj or {}).get("text") if obj else None
                if not passage:
                    f.write(json.dumps({"run": name, "t": r["t"], "skipped": "no text field"}) + "\n"); f.flush(); continue
                text, ti, to, model = call(passage)
                d = parse_obj(text) or {}
                rec = {"run": name, "t": r["t"], "scores": d.get("scores"), "weakest": d.get("weakest"),
                       "raw": text if not d else None, "tok_in": ti, "tok_out": to, "model": model}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
                n_done += 1
                time.sleep(0.5)
            print("rated", name, flush=True)
    print("done; new ratings:", n_done)


if __name__ == "__main__":
    main()
