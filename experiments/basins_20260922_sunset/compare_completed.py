"""Compare fifteen completed 60-hop streams, including the fresh Sol replacement.

Read-only with respect to every source run. Refuses live, unaudited, incomplete,
or over-budget inputs. Writes only three derived comparison files in analysis/.
No basin interpretation or statistical significance claims are produced.
"""
from collections import Counter
import argparse
import datetime as dt
import importlib.util
import json
import math
from pathlib import Path
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("basin_extracted_metrics", HERE / "extracted_metrics.py")
DERIVED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DERIVED)
AUDIT, EXTRACT = DERIVED.AUDIT, DERIVED.EXTRACT
SOL = "gpt-6-sol"
EXCLUDED = SOL + "/sunset_b"
REPLACEMENT = SOL + "/sunset_replacement"
SUNSET = "The sun was setting behind the hills."
TIDE = "The tide came in an hour early."
STUDY_BUDGET = 20.0


class ComparisonNotReady(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ComparisonNotReady(message)


def load_json(path):
    need(path.is_file(), "Required source is not present: " + str(path))
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ComparisonNotReady("Source could not be read: " + str(path)) from exc


def finished_audit(root):
    need((root / "run_finished.json").is_file(), "Run is not finalized: " + str(root))
    result, _ = AUDIT.audit(root)
    DERIVED.require_clean(result)
    need(result["run_finished_receipt_present"], "Finished receipt could not be verified: " + str(root))
    need(result["totals"]["pending_or_unreadable_receipts"] == 0,
         "Finalized source still has pending receipts: " + str(root))
    return result


def is_complete(stream):
    return stream["counts"]["completed_hops"] == 60 and stream["summary_status"] == "hop_limit"


def select_streams(primary, replacement, primary_config, replacement_config):
    models = [model["id"] for model in primary_config["models"]]
    need(len(models) == 5 and len(set(models)) == 5 and SOL in models,
         "Primary protocol must contain the five distinct study models including Sol.")
    need(primary_config["hops"] == replacement_config["hops"] == 60, "Both protocols must specify 60 hops.")
    primary_seeds = {seed["id"]: seed["text"] for seed in primary_config["seeds"]}
    need(primary_seeds == {"sunset_a": SUNSET, "sunset_b": SUNSET, "tide": TIDE},
         "Primary seeds do not match the frozen sunset/tide design.")
    need([model["id"] for model in replacement_config["models"]] == [SOL],
         "Replacement protocol must contain only Sol.")
    need(replacement_config["seeds"] == [{"id": "sunset_replacement", "text": SUNSET}],
         "Replacement must start a fresh stream from the exact sunset seed.")
    for field in ("rule", "max_output_tokens", "reasoning_effort", "sampling"):
        need(primary_config[field] == replacement_config[field], "Replacement setting differs: " + field)
    primary_sol = next(model for model in primary_config["models"] if model["id"] == SOL)
    need(primary_sol == replacement_config["models"][0], "Replacement model/provider/prices differ from primary Sol.")
    need(EXCLUDED in primary["streams"], "Excluded primary Sol stream is missing.")
    need(not is_complete(primary["streams"][EXCLUDED]),
         "Designated partial Sol stream is now complete; explicit selection needs reconsideration.")
    selected = []
    for model in models:
        for role in ("sunset_a", "sunset_b", "tide"):
            key = model + "/" + role
            source, source_key = ("replacement", REPLACEMENT) if key == EXCLUDED else ("primary", key)
            audit = replacement if source == "replacement" else primary
            need(source_key in audit["streams"] and is_complete(audit["streams"][source_key]),
                 "Required 60-hop stream is not complete: " + source + "/" + source_key)
            selected.append({"id": source + "/" + source_key, "source": source,
                             "source_key": source_key, "model": model, "role": role})
    need(len(selected) == 15, "Expected exactly fifteen selected streams.")
    for model in models:
        need(Counter(item["role"] for item in selected if item["model"] == model)
             == Counter({"sunset_a": 1, "sunset_b": 1, "tide": 1}),
             "A model is missing its two sunset replicates and tide comparison.")
    return selected


def amount(value, label):
    need(isinstance(value, (int, float)) and not isinstance(value, bool)
         and math.isfinite(value) and value >= 0, "Invalid money value: " + label)
    return value


def audit_cost(audit):
    totals = audit["totals"]
    return {"usage_cost_upper_estimate_usd": amount(totals["usage_cost_upper_estimate_usd"], "usage"),
            "retained_unknown_reserve_usd": amount(totals["uncertain_cost_reserve_usd"], "uncertain reserve")
                                           + amount(totals["pending_cost_reserve_usd"], "pending reserve")}


def reconcile_costs(primary, replacement, pilot, paused):
    costs = {name: audit_cost(data) for name, data in (
        ("primary", primary), ("replacement", replacement), ("paused_pilot", pilot))}
    need(math.isclose(costs["paused_pilot"]["usage_cost_upper_estimate_usd"],
                      amount(paused["usage_cost_upper_estimate_usd"], "PAUSED usage"), abs_tol=1e-8),
         "Pilot PAUSED.json usage does not reconcile with raw receipts.")
    need(math.isclose(costs["paused_pilot"]["retained_unknown_reserve_usd"],
                      amount(paused["unresolved_billing_reserve_usd"], "PAUSED reserve"), abs_tol=1e-8),
         "Pilot PAUSED.json reserve does not reconcile with raw requests.")
    used = sum(cost["usage_cost_upper_estimate_usd"] for cost in costs.values())
    unknown = sum(cost["retained_unknown_reserve_usd"] for cost in costs.values())
    need(used + unknown <= STUDY_BUDGET + 1e-6, "All-run usage plus retained reserves exceeds the $20 study budget.")
    return {"sources": costs, "usage_cost_upper_estimate_usd": used,
            "retained_unknown_reserve_usd": unknown, "usage_plus_reserves_usd": used + unknown,
            "study_budget_usd": STUDY_BUDGET, "within_budget": True,
            "accounting": "Each source is counted once. Protocol fields describing prior spend are not added again. Usage estimates are not provider invoices."}


def read_completed(root, model, seed):
    completed = []
    for path in sorted((root / "raw" / model["id"] / seed).glob("*.response.json")):
        receipt = load_json(path)
        if "error_type" in receipt or "response_body" not in receipt:
            continue
        try:
            raw = json.loads(receipt["response_body"])
            output, finish, _ = AUDIT.unpack(model["provider"], raw)
            cost = AUDIT.price(model, raw)
        except (ValueError, TypeError, KeyError, IndexError):
            continue
        if output and finish in ("stop", "end_turn") and cost is not None:
            completed.append((receipt["hop"], output))
    need([hop for hop, _ in completed] == list(range(1, 61)),
         "Selected source does not contain exactly completed hops 1 through 60: " + model["id"] + "/" + seed)
    return completed


def uniqueness(texts):
    return {"n": len(texts), "unique_exact": len(set(texts)),
            "unique_case_whitespace_normalized": len({AUDIT.normalized(text) for text in texts})}


def cosine_lookup(rows, left, right):
    names = rows[0][1:]
    cell = rows[names.index(left) + 1][names.index(right) + 1]
    return None if cell == "" else cell


def build(primary_root, replacement_root, pilot_root):
    roots = {"primary": primary_root, "replacement": replacement_root, "paused_pilot": pilot_root}
    configs = {name: load_json(root / "protocol.json") for name, root in roots.items()}
    audits = {"primary": finished_audit(primary_root), "replacement": finished_audit(replacement_root)}
    paused = load_json(pilot_root / "PAUSED.json")
    audits["paused_pilot"], _ = AUDIT.audit(pilot_root)
    DERIVED.require_clean(audits["paused_pilot"])
    need(paused["requests_saved"] == audits["paused_pilot"]["totals"]["attempts"]
         and paused["responses_saved"] == audits["paused_pilot"]["totals"]["receipts"],
         "Pilot PAUSED.json file counts do not reconcile with the raw audit.")
    selected = select_streams(audits["primary"], audits["replacement"], configs["primary"], configs["replacement"])
    costs = reconcile_costs(audits["primary"], audits["replacement"], audits["paused_pilot"], paused)
    streams, all_completed, documents = {}, {}, []
    for item in selected:
        source, source_key = item["source"], item["source_key"]
        model = next(model for model in configs[source]["models"] if model["id"] == item["model"])
        seed = source_key.split("/", 1)[1]
        completed = read_completed(roots[source], model, seed)
        metric, eligible = DERIVED.measure_stream(completed, configs[source]["rule"])
        metric.update(item)
        metric["usage_cost_upper_estimate_usd"] = audits[source]["streams"][source_key]["usage_cost_upper_estimate_usd"]
        streams[item["id"]] = metric
        all_completed[item["id"]] = completed
        documents.extend((item["id"], hop, passage) for hop, passage in eligible)
    lexical, rows = AUDIT.lexical(documents, streams)
    lexical["representation"] = (
        "Only extracted text fields: optional whole Markdown fence removal and literal control-character parsing. "
        "The JSON rule and wrappers are excluded. One shared IDF fit covers all fifteen selected stream tails.")
    lexical["tail_selection"] = (
        "Completed hops 41 through 60 of each selected 60-hop stream, then exclude unextractable, empty, "
        "or changed/missing-rule passages without backfilling.")
    per_model = {}
    for model in configs["primary"]["models"]:
        name = model["id"]
        group = [item for item in selected if item["model"] == name]
        role = {item["role"]: item["id"] for item in group}
        full = [text for item in group for _, text in all_completed[item["id"]]]
        extracted = [EXTRACT.extract(text) for text in full]
        texts = [obj["text"] for obj in extracted if obj is not None]
        all_source_streams = [stream for audit in audits.values() for stream in audit["streams"].values()
                              if stream["model"] == name]
        primary_group = [s for s in audits["primary"]["streams"].values() if s["model"] == name]
        replacement_group = [s for s in audits["replacement"]["streams"].values() if s["model"] == name]
        per_model[name] = {
            "primary_streams": len(primary_group), "primary_60_hop_streams": sum(map(is_complete, primary_group)),
            "replacement_streams": len(replacement_group),
            "replacement_60_hop_streams": sum(map(is_complete, replacement_group)),
            "selected_streams": len(group), "selected_completed_hops": len(full),
            "full_visible_uniqueness_pooled_across_selected_streams": uniqueness(full),
            "extracted_text_uniqueness_pooled_across_selected_streams": uniqueness(texts),
            "extracted_word_lengths_including_empty_or_changed_rule": AUDIT.summary([len(text.split()) for text in texts]),
            "selected_usage_cost_upper_estimate_usd": sum(streams[item["id"]]["usage_cost_upper_estimate_usd"] for item in group),
            "all_run_usage_cost_upper_estimate_usd": sum(s["usage_cost_upper_estimate_usd"] for s in all_source_streams),
            "all_run_retained_unknown_reserve_usd": sum(s["uncertain_cost_reserve_usd"] + s["pending_cost_reserve_usd"]
                                                       for s in all_source_streams),
            "lexical_cosines": {
                "sunset_replicates": cosine_lookup(rows, role["sunset_a"], role["sunset_b"]),
                "sunset_a_to_tide": cosine_lookup(rows, role["sunset_a"], role["tide"]),
                "sunset_b_or_replacement_to_tide": cosine_lookup(rows, role["sunset_b"], role["tide"])},
            "comparison_roles": role}
    selected_cost = sum(s["usage_cost_upper_estimate_usd"] for s in streams.values())
    costs.update(selected_usage_cost_upper_estimate_usd=selected_cost,
                 excluded_usage_cost_upper_estimate_usd=costs["usage_cost_upper_estimate_usd"] - selected_cost)
    partial = audits["primary"]["streams"][EXCLUDED]
    excluded = {"source": "primary", "stream": EXCLUDED, "completed_hops": partial["counts"]["completed_hops"],
                "attempts": partial["counts"]["attempts"], "summary_status": partial["summary_status"],
                "noncompleted_receipts": partial["noncompleted_receipts"],
                "usage_cost_upper_estimate_usd": partial["usage_cost_upper_estimate_usd"],
                "retained_unknown_reserve_usd": partial["uncertain_cost_reserve_usd"] + partial["pending_cost_reserve_usd"],
                "replacement": "replacement/" + REPLACEMENT,
                "reason": "Operationally interrupted stream retained in raw evidence and all-run accounting; excluded from the equal-60-hop comparison. The replacement is a fresh trajectory, not a continuation."}
    metrics = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "comparison_version": 1,
        "scope": "Descriptive comparison of fifteen completed streams. No semantic basin conclusions or significance claims.",
        "selection": {"selected_streams": len(selected), "selected_completed_hops": sum(s["completed_hops"] for s in streams.values()),
                      "streams_per_model": "Two independently generated sunset trajectories and one tide trajectory.",
                      "replacement_timing": "Fresh Sol replacement ran separately after the primary run; service timing is not matched.",
                      "excluded_primary_partial": excluded, "pilot_selected": False},
        "definitions": {
            "completion": "Exactly sixty normally finished, nonempty responses with known usage and no recorded exception, plus a hop_limit summary. Operational completion is not a quality score.",
            "uniqueness": "Exact and case/whitespace-normalized counts pooled across each model's three selected streams. Different strings do not establish different meanings.",
            "extracted_population": "Explicit tolerant extraction; extracted recurrence/word lengths include empty or changed-rule text. Lexical vectors exclude such passages.",
            "null_cosine": "At least one stream has no nonzero eligible passage vectors in its selected tail.",
            "cost": "All-run accounting includes every primary stream, paused pilot stream, fresh replacement, and retained unknown billing reserves."},
        "source_audits": {name: {"root": str(roots[name]), "generated_at": audit["generated_at"],
                                "integrity_errors": 0, "read_issues": 0,
                                "run_finished_receipt_present": audit["run_finished_receipt_present"],
                                "totals": audit["totals"]} for name, audit in audits.items()},
        "costs": costs, "models": per_model, "streams": streams, "lexical": lexical}
    return metrics, rows


def table(metrics):
    costs = metrics["costs"]
    partial = metrics["selection"]["excluded_primary_partial"]
    lines = ["# Completed-stream comparison", "",
             "Fifteen selected streams completed 60 hops each: two sunset trajectories and one tide trajectory per model.", "",
             f"Excluded primary `{partial['stream']}`: {partial['completed_hops']} completed hops; status `{partial['summary_status']}`. "
             f"Fresh `{partial['replacement']}` supplies the second Sol sunset replicate. The partial remains in raw evidence and all-run costs. "
             "The paused pilot is excluded from comparisons but retained in costs.", "",
             "Operational completion is not a quality score. Uniqueness is pooled across each model's selected streams. "
             "The uniqueness columns show exact / case-and-whitespace-normalized unique counts, followed by the population size. "
             "Word ranges cover explicitly extracted text, including any empty or changed-rule text.", "",
             "| Model | 60-hop streams: primary + replacement | Selected hops | Extracted word range | Full visible unique (exact / normalized; n) | Extracted text unique (exact / normalized; n) | Selected usage $ | All-run usage $ | Unknown reserve $ |",
             "| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: |"]
    for name, model in metrics["models"].items():
        word = model["extracted_word_lengths_including_empty_or_changed_rule"]
        word_range = "unextractable" if word["n"] == 0 else f"{word['min']}–{word['max']}"
        full = model["full_visible_uniqueness_pooled_across_selected_streams"]
        text = model["extracted_text_uniqueness_pooled_across_selected_streams"]
        replacement = (f"{model['replacement_60_hop_streams']}/{model['replacement_streams']}"
                       if model["replacement_streams"] else "none")
        completed = f"{model['primary_60_hop_streams']}/{model['primary_streams']} + {replacement}"
        lines.append(f"| {name} | {completed} | {model['selected_completed_hops']} | {word_range} | "
                     f"{full['unique_exact']} / {full['unique_case_whitespace_normalized']}; {full['n']} | "
                     f"{text['unique_exact']} / {text['unique_case_whitespace_normalized']}; {text['n']} | "
                     f"{model['selected_usage_cost_upper_estimate_usd']:.6f} | {model['all_run_usage_cost_upper_estimate_usd']:.6f} | "
                     f"{model['all_run_retained_unknown_reserve_usd']:.6f} |")
    lines.extend(["", f"All-run usage estimate **${costs['usage_cost_upper_estimate_usd']:.6f}** + retained unknown reserves "
                  f"**${costs['retained_unknown_reserve_usd']:.6f}** = **${costs['usage_plus_reserves_usd']:.6f}**, "
                  f"within the **${costs['study_budget_usd']:.2f}** study budget. Selected-stream usage is "
                  f"**${costs['selected_usage_cost_upper_estimate_usd']:.6f}**. These are conservative estimates, not provider invoices.", "",
                  "The following cosines use one global passage-only TF-IDF fit. Tails are completed hops 41–60, "
                  "followed by explicit extraction/rule/empty-text exclusions without backfilling. Missing vectors yield `null`. "
                  "Values describe lexical overlap; they are not semantic basin labels or significance tests.", "",
                  "| Model | Sunset replicates | Sunset A to tide | Sunset B or replacement to tide |",
                  "| --- | ---: | ---: | ---: |"])
    for name, model in metrics["models"].items():
        values = ["null" if value is None else f"{value:.4f}" for value in model["lexical_cosines"].values()]
        lines.append("| " + name + " | " + " | ".join(values) + " |")
    lines.extend(["", "Full stream exclusions and formatting counts are recorded in `comparison_metrics.json`; "
                  "the complete centroid matrix is in `comparison_lexical_similarity.csv`.", ""])
    return "\n".join(lines)


def save(root, metrics, rows):
    output = root / "analysis"
    output.mkdir(parents=True, exist_ok=True)
    for name, content in (
            ("comparison_metrics.json", json.dumps(metrics, ensure_ascii=False, indent=2) + "\n"),
            ("comparison_lexical_similarity.csv", AUDIT.csv_text(rows)),
            ("comparison_table.md", table(metrics))):
        temp = output / (name + ".tmp")
        temp.write_text(content, encoding="utf-8", newline="")
        temp.replace(output / name)


def self_test():
    models = [{"id": name, "provider": "test"} for name in ("a", SOL, "b", "c", "d")]
    primary_config = {"models": models, "hops": 60, "rule": "rule", "max_output_tokens": 4096,
                      "reasoning_effort": "low", "sampling": "defaults",
                      "seeds": [{"id": "sunset_a", "text": SUNSET}, {"id": "sunset_b", "text": SUNSET},
                                {"id": "tide", "text": TIDE}]}
    replacement_config = {**primary_config, "models": [models[1]],
                          "seeds": [{"id": "sunset_replacement", "text": SUNSET}]}
    complete = {"counts": {"completed_hops": 60}, "summary_status": "hop_limit"}
    primary = {"streams": {model["id"] + "/" + seed["id"]: complete
                           for model in models for seed in primary_config["seeds"]}}
    primary["streams"][EXCLUDED] = {"counts": {"completed_hops": 8}, "summary_status": "transport_or_parse_error"}
    replacement = {"streams": {REPLACEMENT: complete}}
    selected = select_streams(primary, replacement, primary_config, replacement_config)
    assert len(selected) == 15
    assert sum(item["source"] == "replacement" for item in selected) == 1
    assert all(item["id"] != "primary/" + EXCLUDED for item in selected)
    assert next(item for item in selected if item["source"] == "replacement")["role"] == "sunset_b"
    primary["streams"]["a/tide"] = {"counts": {"completed_hops": 59}, "summary_status": "active"}
    try:
        select_streams(primary, replacement, primary_config, replacement_config)
    except ComparisonNotReady:
        pass
    else:
        raise AssertionError("Accepted an incomplete selected trajectory")
    assert cosine_lookup([["stream", "a", "b"], ["a", 1, ""], ["b", "", ""]], "a", "b") is None
    assert uniqueness(["Hello  world", "hello world"]) == {"n": 2, "unique_exact": 2, "unique_case_whitespace_normalized": 1}
    def cost_fixture(used, unknown):
        return {"totals": {"usage_cost_upper_estimate_usd": used, "uncertain_cost_reserve_usd": unknown,
                           "pending_cost_reserve_usd": 0}}
    paused = {"usage_cost_upper_estimate_usd": 0.5, "unresolved_billing_reserve_usd": 0.6}
    costs = reconcile_costs(cost_fixture(8, 0.1), cost_fixture(1, 0), cost_fixture(0.5, 0.6), paused)
    assert math.isclose(costs["usage_plus_reserves_usd"], 10.2)
    try:
        reconcile_costs(cost_fixture(20, 0.1), cost_fixture(1, 0), cost_fixture(0.5, 0.6), paused)
    except ComparisonNotReady:
        pass
    else:
        raise AssertionError("Accepted over-budget accounting")
    # Missing/live roots are refused before any output directory is created.
    import tempfile
    with tempfile.TemporaryDirectory(prefix="basin-comparison-test-") as folder:
        root = Path(folder)
        try:
            finished_audit(root)
        except ComparisonNotReady:
            pass
        else:
            raise AssertionError("Accepted a live run without a finished receipt")
        assert not (root / "analysis").exists()
    print("Synthetic checks passed: exact fifteen-stream selection, fresh replacement role, incomplete/live refusal, null cosine, uniqueness, cost reconciliation, and budget rejection.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HERE)
    parser.add_argument("--replacement-root", type=Path, default=HERE.parent / "basins_20260922_sol_replacement")
    parser.add_argument("--pilot-root", type=Path, default=HERE.parent / "basins_20260922")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    try:
        metrics, rows = build(args.root, args.replacement_root, args.pilot_root)
        save(args.root, metrics, rows)
    except (ComparisonNotReady, DERIVED.AuditRejected) as exc:
        print("Comparison not written: " + str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps({"selected_streams": metrics["selection"]["selected_streams"],
                      "selected_completed_hops": metrics["selection"]["selected_completed_hops"],
                      "costs": metrics["costs"]}, indent=2))


if __name__ == "__main__":
    main()
