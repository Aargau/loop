"""export.py -- flatten every run in runs/ into data/ for downstream use (site, art, analysis).
Writes data/index.json (one entry per run with metadata + my annotation) and data/<run>.json
(list of hops: t, tag, model, sampling, text (decoded from the JSON rule/text wrapper, fences
stripped), raw, metrics, cycle flags). Nothing is invented: text is exactly what the model returned.
"""
import json, os, re, glob, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)

NOTES = {
    "smoke":  ("quine", "qwen", "Bare instruction quine, 4 hops: refused at hop 1, then the meta loop."),
    "headers": ("yours,still,rule,glider", "qwen", "Four header designs, 10 hops each. yours/rule: exact fixed point with empty payload. still: header lost at hop 2, writer/critic workshop loop. glider: counter incremented once, rule dropped, frozen at Hop 3."),
    "headers2": ("still2,sandwich", "qwen", "Two more header designs. still2: copied the payload line, then greeting loop, confabulated a task. sandwich: kept the form, swapped the content, then critic mode."),
    "headers3": ("json", "qwen", "Instruction as data. Rule field survives; text field: sun -> stars -> moon -> stars, exact period 2 from hop 4."),
    "20260902T155321_chat": ("json_para", "qwen", "Paragraph scale. 15 hops of a continuous sea story (storm, dawn, meal, dusk, stars, moon), then exact fixed point on a paragraph about time suspending itself."),
    "20260902T155557_chat": ("json_page", "qwen", "Page scale. tau=5, p=1. Fixed point: Mara's letter in the greenhouse, 'a door to be opened'."),
    "20260902T160344_chat": ("json_page (+repeat, parallel)", "qwen", "Determinism test: identical X_0 in two slots diverged at hop 1. json_page froze at tau=4 (warehouse, 'into the unknown'); json_page~r visited Mara at t=10, copied imperfectly at t=11, escaped, froze at tau=14 (Elias phones his father). 102 exact copies out of 103."),
    "20260902T162514_raw": ("json_page (raw mode)", "qwen", "No chat template. <think> leak at t=2, word-count check at t=6, numbered-word glider carrying a live counter t=7..19, annihilated at t=20 into a period-3 phrase loop ('the last time she would ever...'). Rotation-invariant fixed point tau=19; exact tau=20, p=11."),
    "20260902T165324_chat": ("json_prev", "qwen", "Backward operator. 60 hops, no recurrence at any level. Backstory drifts from coastal mystery to Chicago offices to Neo-Veridia server rooms. Forward sinks (rain lashed, silence not empty) are transit states here."),
    "20260902T172519_chat": ("json_better", "qwen", "Improve operator, sentence seed. tau=1: 'The tide surged in an hour ahead of schedule.' then unchanged forever."),
    "20260902T172547_chat": ("json_unexpected", "qwen", "Surprise operator. 23 hops of 'not X; Y' subversion (digital, cosmic, then the anti-twist: break room, spreadsheet, dry bread), office becomes a womb, 'The void was not empty. It was full of her.' Then copied, overflowed 600 tokens, truncated JSON became the exact fixed point at tau=24."),
    "20260902T174258_chat": ("json_worse", "qwen", "Degrade operator. 'which was annoying' -> flooded basement -> liquefied foundation -> before the universe formed, a sentient malevolent void -> eternal self-blame ('I will never be allowed to stop'). Hit the 800-token wall at t=6, exact fixed point on truncated JSON at tau=7."),
    "20260902T174854_chat": ("json_better_para", "qwen", "Improve operator, flat 44-word seed. tau=2: one expansion to 82 words, one small revision (partly reverting hop 1), then fixed."),
    "20260902T175622_anthropic_chat": ("json", "claude-sonnet-4-6", "Failed smoke test (workspace header missing). No hops."),
    "20260902T175821_anthropic_chat": ("json", "claude-sonnet-4-6", "Smoke test, 3 hops. Sonnet wraps the JSON in a code fence from hop 2."),
    "20260902T181431_anthropic_chat": ("json_next", "claude-sonnet-4-6", "Claude with an explicit NEXT operator, T=0, 60 hops, no recurrence. One continuous story (Maren, Paul, a drowned man identified on Tuesday, a kitchen, a sister and a child, eleven months, a door) written 250 words at a time with only the previous passage visible. No ending reached: quiet realism always has another ordinary moment. Last line at t=60: people who have forgotten, temporarily, what comes next. Prediction on record (codas forever in single digits) was wrong."),
    "20260902T175920_anthropic_chat": ("json_page", "claude-sonnet-4-6", "Claude at T=0, 60 hops, no exact recurrence: it never copies. Reads 'new passage' as a new story; all 60 are openings. Converges on a theme (cartographer, archivist, translator, librarian discovering their records leave things out) with strict semantic period 2 from t=22: the cartographer on every other hop."),
}

def text_of(out):
    m = FENCE.match(out)
    if m: out = m.group(1)
    try:
        j = json.loads(out)
        if isinstance(j, dict) and "text" in j: return j["text"], True
    except Exception:
        pass
    return out, False

os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
index = []
for d in sorted(glob.glob(os.path.join(ROOT, "runs", "*"))):
    name = os.path.basename(d)
    p = os.path.join(d, "steps.jsonl")
    if not os.path.exists(p): continue
    hops = []
    for line in open(p, encoding="utf-8"):
        j = json.loads(line)
        if "out" not in j:
            hops.append({"t": j["t"], "tag": j["tag"], "error": j.get("error")}); continue
        text, parsed = text_of(j["out"])
        hops.append({
            "t": j["t"], "tag": j["tag"], "model": j.get("model", "qwen3.8-27b"), "sampling": j.get("sampling", "T=0"),
            "text": text, "text_is_json_field": parsed, "raw": j["out"],
            "tok_out": j.get("tok_out"), "finish": j.get("finish"),
            "cos_prev": j.get("cos_prev"), "cos_x0": j.get("cos_x0"), "ncd_prev": j.get("ncd_prev"), "ncd_x0": j.get("ncd_x0"),
            "surv_prev": j.get("surv_prev"), "surv_x0": j.get("surv_x0"), "gzip_ratio": j.get("gzip_ratio"),
            "latency": j.get("latency"), "cycle_exact": j.get("cycle_exact"), "cycle_norm": j.get("cycle_norm"),
            "cycle_broken": j.get("cycle_broken"), "pair_equal": j.get("pair_equal"), "pair_ncd": j.get("pair_ncd"),
        })
    summ = {}
    sp = os.path.join(d, "summary.json")
    if os.path.exists(sp):
        s = json.load(open(sp, encoding="utf-8")); summ = {"args": s.get("args"), "results": s.get("results")}
    init, model, note = NOTES.get(name, ("?", "?", ""))
    x0 = None
    if summ.get("args"):
        import importlib.util
        spec = importlib.util.spec_from_file_location("loop", os.path.join(ROOT, "loop.py")); loop = importlib.util.module_from_spec(spec); spec.loader.exec_module(loop)
        k = summ["args"].get("init") or (summ["args"].get("init_set") or "").split(",")[0]
        x0 = loop.INITS.get(k)
    entry = {"run": name, "init": init, "model": model, "mode": (summ.get("args") or {}).get("mode", "chat"),
             "hops": len([h for h in hops if "text" in h]), "tags": sorted(set(h["tag"] for h in hops)),
             "x0": x0, "note": note, "results": summ.get("results")}
    index.append(entry)
    json.dump({"meta": entry, "hops": hops}, open(os.path.join(ROOT, "data", name + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("%-32s %3d hops  %s" % (name, entry["hops"], init))
json.dump(index, open(os.path.join(ROOT, "data", "index.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote data/index.json with %d runs" % len(index))
