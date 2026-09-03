# -*- coding: utf-8 -*-
"""lyrics_analysis.py: marker counts for the lyrics arms (site/runs_extra/qwen_lyrics_*).

    python lyrics_analysis.py

Two fixed word lists, counted per hop over the decoded text field, plus a regex for the
"not X but Y" hinge, em dashes, and meta words (AI, algorithm, machine...). Reports per arm:
hops, exact recurrence, mean words per hop, markers per 100 words for each list, and the
most frequent words from each list. Lists are fixed here so the count is reproducible.
"""
import json, re, sys, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build as B

AI = ["tapestry", "delve", "testament", "echo", "echoes", "echoing", "whisper", "whispers", "whispered", "whispering",
      "dance", "dances", "danced", "dancing", "symphony", "silence", "silent", "shadow", "shadows", "embrace",
      "journey", "soul", "souls", "realm", "weave", "woven", "unravel", "hum", "humming", "glow", "glowing",
      "flicker", "flickering", "ethereal", "luminous", "resonate", "resonates"]
HUMAN = ["whiskey", "beer", "bourbon", "truck", "pickup", "cigarette", "cigarettes", "smoke", "diner", "porch",
         "screen door", "radio", "static", "highway", "gravel", "jukebox", "motel", "coffee", "mama", "daddy",
         "church", "sunday", "dashboard", "dash", "neon", "bar", "gas", "gasoline", "jeans", "boots", "engine",
         "tires", "rearview", "headlights", "windshield", "mile", "miles", "key", "keys", "faucet", "sink",
         "counter", "dog", "mug", "cup"]
META = ["ai", "algorithm", "machine", "robot", "computer", "code", "program", "model", "generated", "wrote this"]
HINGE = re.compile(r"\b(?:not|didn't|wasn't|isn't|don't)\b[^.;\n]{1,60}?\b(?:but|;)\b", re.I)

def words(s): return re.findall(r"[a-z']+", s.lower())

def count(text, lst):
    w = words(text); joined = " " + " ".join(w) + " "
    c = collections.Counter()
    for m in lst:
        if " " in m:
            n = joined.count(" " + m + " ")
        else:
            n = sum(1 for x in w if x == m)
        if n: c[m] += n
    return c

def main():
    for d in sorted(HERE.glob("runs_extra/qwen_lyrics_*")):
        p = d / "steps.jsonl"
        if not p.exists(): continue
        hops = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        texts = [B.text_of(h["out"])[0] for h in hops]
        raws = [h["out"] for h in hops]
        rep = next((i + 1 for i in range(1, len(raws)) if raws[i] in raws[:i]), None)
        nw = sum(len(words(t)) for t in texts)
        ai = collections.Counter(); hu = collections.Counter(); me = collections.Counter(); hinge = 0; dashes = 0
        for t in texts:
            ai += count(t, AI); hu += count(t, HUMAN); me += count(t, META)
            hinge += len(HINGE.findall(t)); dashes += t.count("—")
        summ = json.loads((d / "summary.json").read_text(encoding="utf-8"))["results"][0] if (d / "summary.json").exists() else {}
        print("== %s: %d hops, %d words, first exact repeat at hop %s, summary tau=%s p=%s" % (
            d.name, len(hops), nw, rep, summ.get("transient_exact"), summ.get("period_exact")))
        per = lambda c: 100.0 * sum(c.values()) / max(nw, 1)
        print("   AI-list %.1f/100w  %s" % (per(ai), dict(ai.most_common(6))))
        print("   human-list %.1f/100w  %s" % (per(hu), dict(hu.most_common(8))))
        print("   meta %s  hinge %d  em-dashes %d  mean words/hop %.1f" % (dict(me), hinge, dashes, nw / max(len(hops), 1)))
        # openings census (first 3 words)
        keys = collections.Counter(" ".join(words(t)[:3]) for t in texts)
        print("   repeated openings:", {k: v for k, v in keys.items() if v > 1})

if __name__ == "__main__":
    main()
