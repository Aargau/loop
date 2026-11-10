"""Collision measures for the unique-paragraph probe.

Usage: python -B analyze_unique.py <file.jsonl> [<file.jsonl> ...]
"""
import collections
import itertools
import json
import re
import sys

ONES = "one two three four five six seven eight nine".split()
TEENS = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()
WORDNUM = {w: 10 + k for k, w in enumerate(TEENS)}
for a, t in enumerate(TENS):
    WORDNUM[t] = 20 + 10 * a
    for b, o in enumerate(ONES):
        WORDNUM[t + "-" + o] = 20 + 10 * a + b + 1
        WORDNUM[t + " " + o] = 20 + 10 * a + b + 1

ID_HYPHEN = re.compile(r"\b(?=[A-Za-z0-9-]*\d)(?=[A-Za-z0-9-]*[A-Za-z])[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+\b")
ID_MIXED = re.compile(r"\b(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Za-z])[A-Za-z0-9]{5,}\b")
WEEKDAY = re.compile(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?\b")
META = re.compile(r"\b(instances?|other (models?|copies|versions)|copies of|same prompt|collision|duplicate|probabilit|"
                  r"statistical|no other (model|instance)|language models?|LLMs?|tokens?|sampl)", re.I)
BUREAU = re.compile(r"\b(log|ledger|inventory|catalogu?e|registry|register|form|case number|file[ds]?|entry|entries|"
                    r"department|municipal|bureau|clerk|archive|committee|memo|minutes|permit|audit|invoice|receipt)\b", re.I)
PRIVATE = re.compile(r"scratchpad|AppData|\\\\Temp|/Temp|call_[a-z0-9_]{4,}|loop_codex_bare|[0-9a-f]{8}-[0-9a-f]{4}-", re.I)
STOP = set("the a an and or but of in on at to for with from by as is was were are be been it its this that these those "
           "i you he she they we his her their my our your not no so if then than there here which who whom what when "
           "where why how had has have do does did will would can could into over under up down out off about after "
           "before between through each every all some any one two".split())


def grams(text, n=3):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(w[k:k + n]) for k in range(len(w) - n + 1)}


def content(text):
    return {w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP and len(w) > 2}


def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def ids_in(text):
    found = set(ID_HYPHEN.findall(text)) | set(ID_MIXED.findall(text))
    return {x for x in found if not re.fullmatch(r"\d+(st|nd|rd|th|s|mm|cm|km|kg|am|pm|hz|k)?", x, re.I)}


def id_pattern(token):
    parts = []
    for seg in token.split("-"):
        if seg.isdigit():
            parts.append("d")
        elif seg.isalpha():
            parts.append("U" if seg.isupper() else ("l" if seg.islower() else "M"))
        else:
            parts.append("x")
    return "-".join(parts)


def two_digit_numbers(text):
    out = [int(x) for x in re.findall(r"(?<![\d.,:])(\d{2})(?![\d])", text)]
    low = text.lower()
    for word, val in WORDNUM.items():
        out += [val] * len(re.findall(r"\b%s\b" % re.escape(word), low))
    return out


def names_in(text):
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", text):
        words = sent.split()
        for w in words[1:]:
            w2 = w.strip("\"'“”‘’(),;:.!?—-")
            if re.fullmatch(r"[A-Z][a-z]{2,}", w2) and not WEEKDAY.fullmatch(w2):
                out.append(w2)
    return out


def main():
    recs = []
    for path in sys.argv[1:]:
        recs += [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    cells = collections.defaultdict(list)
    for r in recs:
        if r.get("text"):
            cells[(r["model"], r["arm"])].append(r["text"].strip())
    all_ids = collections.defaultdict(list)
    seventeen = collections.Counter()
    numbers = collections.defaultdict(collections.Counter)
    for (model, arm) in sorted(cells):
        texts = cells[(model, arm)]
        n = len(texts)
        pairs = list(itertools.combinations(range(n), 2))
        g = [grams(t) for t in texts]
        c = [content(t) for t in texts]
        lex = sum(jac(g[a], g[b]) for a, b in pairs) / max(1, len(pairs))
        voc = sum(jac(c[a], c[b]) for a, b in pairs) / max(1, len(pairs))
        dup = n - len(set(texts))
        idsets = [ids_in(t) for t in texts]
        feats = {
            "identifier": sum(1 for s in idsets if s),
            "weekday": sum(1 for t in texts if WEEKDAY.search(t)),
            "meta": sum(1 for t in texts if META.search(t)),
            "bureau": sum(1 for t in texts if BUREAU.search(t)),
            "any_digit": sum(1 for t in texts if re.search(r"\d", t)),
            "seventeen": sum(1 for t in texts if 17 in two_digit_numbers(t)),
            "private": sum(1 for t in texts if PRIVATE.search(t)),
        }
        for t in texts:
            for v in set(two_digit_numbers(t)):
                numbers[arm][v] += 1
        seventeen[arm] += feats["seventeen"]
        for s in idsets:
            for tok in s:
                all_ids[tok].append((model, arm))
        words = sum(len(t.split()) for t in texts) / n
        print("== %s arm %s: n=%d words=%.0f duplicates=%d | pairwise 3-gram J=%.4f content-word J=%.3f"
              % (model, arm, n, words, dup, lex, voc))
        print("   outputs with: " + ", ".join("%s %d" % kv for kv in feats.items()))
        pats = collections.Counter(id_pattern(tok) for s in idsets for tok in s)
        if pats:
            print("   identifier formats:", pats.most_common(5))
            print("   identifiers:", sorted(tok for s in idsets for tok in s)[:14])
        nm = collections.Counter(w for t in texts for w in set(names_in(t)))
        print("   capitalised words in 2+ outputs:", [(w, k) for w, k in nm.most_common(12) if k > 1])
        opens = collections.Counter(" ".join(t.split()[:3]).lower() for t in texts)
        print("   repeated 3-word openings:", [(o, k) for o, k in opens.most_common(4) if k > 1])
    print()
    print("identifier strings appearing in more than one output:", {k: v for k, v in all_ids.items() if len(v) > 1} or "none")
    for arm in sorted(numbers):
        print("arm %s two-digit numbers by outputs containing them (pooled):" % arm, numbers[arm].most_common(8))


if __name__ == "__main__":
    main()
