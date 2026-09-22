"""Prepare one fresh replacement only after primary billing reservations settle.

Preparation does not make API calls. Generation is a separate explicit command.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST = ROOT.parent / "basins_20260922_sol_replacement"


def main():
    finish = ROOT / "run_finished.json"
    if not finish.exists():
        raise SystemExit("Primary run is still active; replacement not prepared.")
    primary = json.loads(finish.read_text(encoding="utf-8"))
    pilot = json.loads((ROOT.parent / "basins_20260922" / "PAUSED.json").read_text(encoding="utf-8"))
    failure = json.loads((ROOT / "raw/gpt-6-sol/sunset_b/009.response.json").read_text(encoding="utf-8"))
    if failure.get("error_type") != "URLError" or "10054" not in failure.get("error_message", ""):
        raise SystemExit("Expected infrastructure failure not confirmed; no replacement prepared.")
    prior = (primary["budget"]["usage_cost_upper_estimate_usd"]
             + primary["budget"]["uncertain_cost_reserve_usd"]
             + max(0, primary["budget"]["in_flight_reserve_usd"])
             + pilot["usage_cost_upper_estimate_usd"] + pilot["unresolved_billing_reserve_usd"])
    allowance = int(min(3.0, 20 - prior) * 100) / 100
    if allowance < 0.1:
        raise SystemExit("Insufficient remaining global budget; no replacement prepared.")
    config = json.loads((ROOT / "protocol.json").read_text(encoding="utf-8"))
    config["models"] = [m for m in config["models"] if m["id"] == "gpt-6-sol"]
    config["seeds"] = [{"id": "sunset_replacement", "text": "The sun was setting behind the hills."}]
    config["budget_usd"] = allowance
    config["prior_run"] = "../basins_20260922_sunset"
    config["all_prior_usage_and_uncertain_reserves_usd"] = prior
    config["replacement_for"] = "gpt-6-sol/sunset_b; remote connection reset at hop 9"
    DEST.mkdir(exist_ok=False)
    (DEST / "protocol.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    code = (ROOT / "run.py").read_text(encoding="utf-8")
    code = code.replace('"one worker per model; interleaved seeds; 5 workers"',
                        '"one model, one fresh independent sunset stream"')
    (DEST / "run.py").write_text(code, encoding="utf-8")
    (DEST / "PROTOCOL.md").write_text(
        "# Fresh Sol replacement after a connection reset\n\n"
        "One independent 60-hop stream from Justin's exact sunset seed, with the same model, rule, effort, "
        "sampling and token limit as the main study. This replaces the missing complete replicate after "
        "sunset_b lost its connection at hop 9. It does not continue from an earlier response or overwrite "
        "the eight completed passages and failure receipt. The missing response's billing reserve remains charged. "
        "This infrastructure-based replacement decision was announced before generation. No semantic output "
        "was used to select a replacement. The primary run has finished before this extra allowance is allocated.\n\n"
        f"All prior usage plus uncertainty reserves: ${prior:.8f}. Replacement allowance: ${allowance:.2f}. "
        "The combined reserved total remains within $20. Full settings are in protocol.json; see "
        "../basins_20260922_sunset/PROTOCOL.md for the primary design and limitations. No automatic retries.\n",
        encoding="utf-8")
    print(json.dumps({"prepared": str(DEST), "prior_accounted_usd": prior, "replacement_budget_usd": allowance}))


if __name__ == "__main__":
    main()
