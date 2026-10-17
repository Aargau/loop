#!/usr/bin/env python
"""review.py: have another model referee a document, for cross-model review of research-grade write-ups.

  python review.py paper/draft_20261017.md --backend openai --model gpt-6-astra [--effort high] [--extra paper/prompts.md ...]

Sends the document (plus any --extra files, each labelled) to the model through loop.py's backends with a
referee brief, and writes the review to <doc dir>/reviews/<model>_<date>.md with the exact brief at the top.
Keys from the environment as loop.py expects. The reviewer sees the documents only; it has no file access, so
the brief asks it to flag anything it cannot verify from the text rather than assume it.
"""
import argparse, datetime, io, os, sys, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loop as L

BRIEF = """You are refereeing a draft research paper for a careful author who wants problems found, not praise. You see only the text below; you have no access to the data or code it cites. Review it as a referee for a venue in machine-learning evaluation would, with these priorities, in this order:

1. Claims versus evidence: list every claim in the abstract and conclusions, and for each say whether the body supports it with the stated numbers, supports a weaker version, or does not support it. Quote the claim.
2. Definitions and measurement: are the defined quantities (retention, release, re-seal, reader agreement) defined precisely enough to recompute, and are the scoring choices (substring matching, model readers, censoring) handled honestly in the limitations?
3. Preregistration: where predictions are reported as failed or held, check that the scoring follows the stated prediction rather than a convenient reading.
4. Instrument confounds the author may have missed: the print-mode identity frame, soft caps, the rule-ordering of injected fields, reader-writer family overlap, anything else.
5. Alternative explanations for the two main results that the paper does not rule out.
6. Writing: where it is unclear, overlong, or where a table would replace prose.

For each point give the section or quoted sentence it refers to. Mark anything you cannot verify from the text as "unverifiable from the draft" rather than assuming. End with the three changes you would require before accepting, and a one-paragraph summary of what the paper establishes if its numbers are right."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--backend", default="openai", choices=["openai", "anthropic", "gemini", "claudecode", "cerebras", "llama"])
    ap.add_argument("--model", default="gpt-6-astra")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--extra", nargs="*", default=[])
    a = ap.parse_args()
    parts = [BRIEF, "\n\n===== DOCUMENT: %s =====\n\n" % os.path.basename(a.doc), io.open(a.doc, encoding="utf-8").read()]
    for x in a.extra:
        parts += ["\n\n===== SUPPORTING FILE: %s =====\n\n" % os.path.basename(x), io.open(x, encoding="utf-8").read()]
    prompt = "".join(parts)
    args = types.SimpleNamespace(max_tokens=a.max_tokens, temp=0.0, no_sampling=True, seed=42, system=None, think=False, effort=a.effort, min_interval=0.0)
    step = {"openai": L.step_openai, "anthropic": L.step_anthropic, "gemini": L.step_gemini, "claudecode": L.step_claudecode,
            "cerebras": L.step_cerebras, "llama": L.step_llama_chat}[a.backend]
    text, meta = step(prompt, args, a.model)
    outdir = os.path.join(os.path.dirname(os.path.abspath(a.doc)), "reviews")
    os.makedirs(outdir, exist_ok=True)
    stamp = datetime.date.today().isoformat()
    outp = os.path.join(outdir, "%s_%s.md" % (a.model.replace("/", "_"), stamp))
    with io.open(outp, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Review of %s by %s (%s)\n\n" % (os.path.basename(a.doc), meta.get("model", a.model), stamp))
        f.write("Backend %s, effort %s, max_tokens %d, finish %s, tokens in/out %s/%s, reasoning %s. Supporting files: %s.\n\n" % (
            a.backend, a.effort, a.max_tokens, meta.get("finish"), meta.get("tok_in"), meta.get("tok_out"), meta.get("tok_reasoning"),
            ", ".join(os.path.basename(x) for x in a.extra) or "none"))
        f.write("## Brief given to the reviewer\n\n" + BRIEF + "\n\n## Review\n\n" + text + "\n")
    print("wrote", outp, "| finish", meta.get("finish"), "| tokens", meta.get("tok_in"), meta.get("tok_out"))


if __name__ == "__main__":
    main()
