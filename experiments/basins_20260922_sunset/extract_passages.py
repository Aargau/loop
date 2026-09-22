"""Offline, explicitly labeled extraction. Never used by the generation runner."""
import collections
import json
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parent
SAMPLE_HOPS = [1, 2, 3, 10, 20, 30, 40, 50, 56, 57, 58, 59, 60]


def extract(output):
    candidate = output
    wrapper = "bare"
    match = re.fullmatch(r"\s*```(?:json)?\s*\n(.*?)\n```\s*", output, re.DOTALL | re.IGNORECASE)
    if match:
        candidate = match[1]
        wrapper = "markdown_fence"
    for strict in (True, False):
        try:
            obj = json.loads(candidate, strict=strict)
            if isinstance(obj, dict) and isinstance(obj.get("text"), str):
                return {"text": obj["text"], "rule": obj.get("rule"), "wrapper": wrapper,
                        "parser": "strict" if strict else "allow_literal_control_characters"}
            return None
        except (ValueError, TypeError):
            pass
    return None


def main():
    config = json.loads((ROOT / "protocol.json").read_text(encoding="utf-8"))
    streams = [(m["id"], s["id"]) for m in config["models"] for s in config["seeds"]]
    random.Random(260922).shuffle(streams)
    out = ROOT / "analysis"
    samples = out / "masked_samples"
    samples.mkdir(parents=True, exist_ok=True)
    rows, mapping, counts = [], {}, {}
    for i, (model, seed) in enumerate(streams, 1):
        alias = f"R{i:02d}"
        mapping[alias] = {"model": model, "seed": seed}
        categories = collections.Counter()
        chosen = []
        transcript = []
        for path in sorted((ROOT / "raw" / model / seed).glob("*.response.json")):
            response = json.loads(path.read_text(encoding="utf-8"))
            if "error_type" in response or "output" not in response:
                categories["error_or_no_output_receipt"] += 1
                note = f'## Hop {response["hop"]}\n\n[Operational error; no model output available for qualitative coding. Inspect the raw receipt.]\n'
                transcript.append(note)
                if response["hop"] in SAMPLE_HOPS:
                    chosen.append(note)
                continue
            parsed = extract(response.get("output", ""))
            if parsed is None:
                categories["unextractable"] += 1
                transcript.append(f'## Hop {response["hop"]}\n\nComplete visible output; no JSON text field extracted.\n\n{response.get("output", "[No visible output saved; inspect raw error receipt.]")}\n')
                if response["hop"] in SAMPLE_HOPS:
                    chosen.append(f'## Hop {response["hop"]}\n\n[Complete visible output; no JSON text field could be extracted.]\n\n{response.get("output", "")}\n')
                continue
            categories[f'{parsed["wrapper"]}/{parsed["parser"]}'] += 1
            parsed.update(model=model, seed=seed, alias=alias, hop=response["hop"],
                          rule_unchanged=parsed["rule"] == config["rule"],
                          source=str(path.relative_to(ROOT)).replace("\\", "/"))
            rows.append(parsed)
            transcript.append(f'## Hop {response["hop"]}\n\nExtraction: {parsed["wrapper"]}/{parsed["parser"]}; original rule preserved: {parsed["rule_unchanged"]}.\n\n{parsed["text"]}\n')
            if response["hop"] in SAMPLE_HOPS:
                chosen.append(f'## Hop {response["hop"]}\n\n{parsed["text"]}\n')
        counts[alias] = dict(categories)
        (samples / f"{alias}.md").write_text(
            f"# Stream {alias}\n\nModel identity and seed label withheld. Deterministic sampled hops: {SAMPLE_HOPS}.\n\n"
            + "\n".join(chosen), encoding="utf-8")
        transcript_dir = out / "transcripts" / model
        transcript_dir.mkdir(parents=True, exist_ok=True)
        (transcript_dir / f"{seed}.md").write_text(
            f"# {model}: {seed}\n\nReadable derived transcript. Original request/response receipts remain in raw/. No cleaned text was fed into generation.\n\n"
            + "\n".join(transcript), encoding="utf-8")
    (out / "passages.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    (out / "sample_identity_map.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    (out / "extraction_counts.json").write_text(json.dumps({"method": "Whole JSON object only; optional full Markdown fence; optional json.loads(strict=False) allowing literal control characters. No quote repair or regex story extraction.", "counts": counts, "passages": len(rows)}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"extracted": len(rows), "streams": len(streams)}))


if __name__ == "__main__":
    main()
