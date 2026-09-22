"""Export R16 separately from the interrupted R11; never alter generation data."""
import json
from pathlib import Path

from extract_passages import SAMPLE_HOPS, extract


def main():
    primary = Path(__file__).resolve().parent
    root = primary.parent / "basins_20260922_sol_replacement"
    if not (root / "run_finished.json").is_file():
        raise SystemExit("Replacement is not finished.")
    config = json.loads((root / "protocol.json").read_text(encoding="utf-8"))
    model, seed, alias = "gpt-6-sol", "sunset_replacement", "R16"
    receipts = [json.loads(p.read_text(encoding="utf-8")) for p in
                sorted((root / "raw" / model / seed).glob("*.response.json"))]
    if [r["hop"] for r in receipts] != list(range(1, 61)) or any(
            "error_type" in r or "output" not in r for r in receipts):
        raise SystemExit("Expected exactly 60 successful replacement receipts.")
    sampled, transcript = [], []
    for receipt in receipts:
        parsed = extract(receipt["output"])
        text = parsed["text"] if parsed else receipt["output"]
        note = (f'Extraction: {parsed["wrapper"]}/{parsed["parser"]}; '
                f'original rule preserved: {parsed["rule"] == config["rule"]}.'
                if parsed else "Complete visible output; no JSON text field extracted.")
        transcript.append(f'## Hop {receipt["hop"]}\n\n{note}\n\n{text}\n')
        if receipt["hop"] in SAMPLE_HOPS:
            sampled.append(f'## Hop {receipt["hop"]}\n\n{text}\n')
    target = primary / "analysis" / "masked_replacement"
    target.mkdir(parents=True, exist_ok=True)
    (target / "R16.md").write_text(
        f"# Stream R16\n\nModel identity and seed label withheld. "
        f"Deterministic sampled hops: {SAMPLE_HOPS}. This is its own complete trajectory.\n\n"
        + "\n".join(sampled), encoding="utf-8")
    destination = root / "analysis" / "transcripts" / model
    destination.mkdir(parents=True, exist_ok=True)
    (destination / f"{seed}.md").write_text(
        f"# {model}: {seed}\n\nReadable derived transcript. Original request/response receipts "
        "remain in raw/. No cleaned text was fed into generation.\n\n"
        + "\n".join(transcript), encoding="utf-8")
    (primary / "analysis" / "replacement_identity_map.json").write_text(
        json.dumps({alias: {"root": root.name, "model": model, "seed": seed}}, indent=2)
        + "\n", encoding="utf-8")
    print(json.dumps({"alias": alias, "completed_hops": len(receipts), "sampled_hops": SAMPLE_HOPS}))


if __name__ == "__main__":
    main()
