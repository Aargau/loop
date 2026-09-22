"""Explicitly tolerant, derived metrics; never changes generation or raw receipts.

Full visible response recurrence includes non-JSON outcomes. Extracted text is a
separate population. Lexical metrics admit only nonempty extracted text with the
original rule, after selecting the final 20 completed hops without backfilling.
An independent strict audit must pass before these derived files can be written.
"""
from collections import Counter
import argparse
import datetime as dt
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT_PATH = HERE.parent / "basins_20260922" / "audit.py"
EXTRACT_PATH = HERE / "extract_passages.py"
AUDIT = load_module("basin_receipt_audit", AUDIT_PATH)
EXTRACT = load_module("basin_passage_extractor", EXTRACT_PATH)
FORMAT_CATEGORIES = (
    "bare/strict", "markdown_fence/strict",
    "bare/allow_literal_control_characters",
    "markdown_fence/allow_literal_control_characters", "unextractable")


class AuditRejected(RuntimeError):
    pass


class SnapshotChanged(RuntimeError):
    pass


def require_clean(upstream):
    if upstream["errors"] or upstream["read_issues"]:
        raise AuditRejected(
            "Independent audit rejected this snapshot: "
            f'{len(upstream["errors"])} integrity errors, '
            f'{len(upstream["read_issues"])} unreadable files. '
            "Existing derived outputs were not rewritten.")


def measure_stream(completed, rule):
    """completed contains (hop, exact visible output), already receipt-verified."""
    full = [(hop, output) for hop, output in completed]
    extracted, classified = [], []
    formats = Counter({category: 0 for category in FORMAT_CATEGORIES})
    rules = Counter(unchanged=0, changed_or_missing=0, unassessable_unextractable=0)
    empty_hops, changed_rule_hops, unextractable_hops = [], [], []
    for hop, output in completed:
        parsed = EXTRACT.extract(output)
        exclusions = []
        if parsed is None:
            formats["unextractable"] += 1
            rules["unassessable_unextractable"] += 1
            unextractable_hops.append(hop)
            exclusions.append("unextractable")
        else:
            formats[parsed["wrapper"] + "/" + parsed["parser"]] += 1
            extracted.append((hop, parsed["text"]))
            if parsed["rule"] == rule:
                rules["unchanged"] += 1
            else:
                rules["changed_or_missing"] += 1
                changed_rule_hops.append(hop)
                exclusions.append("changed_or_missing_rule")
            if not parsed["text"].strip():
                empty_hops.append(hop)
                exclusions.append("empty_passage")
        classified.append({"hop": hop, "parsed": parsed, "exclusions": exclusions})
    tail = classified[-AUDIT.TAIL_SIZE:]
    included = [item for item in tail if not item["exclusions"]]
    metric = {
        "completed_hops": len(completed),
        "completed_hop_numbers": [hop for hop, _ in completed],
        "formatting_counts_among_completed": dict(formats),
        "extracted_passages_including_empty_or_changed_rule": len(extracted),
        "rule_survival_among_completed": dict(rules),
        "empty_extracted_passage_hops": empty_hops,
        "changed_or_missing_rule_hops": changed_rule_hops,
        "unextractable_completed_hops": unextractable_hops,
        "full_visible_exact_recurrence": AUDIT.recurrence(full, lambda text: text),
        "full_visible_case_whitespace_normalized_recurrence": AUDIT.recurrence(full, AUDIT.normalized),
        "extracted_text_exact_recurrence": AUDIT.recurrence(extracted, lambda text: text),
        "extracted_text_case_whitespace_normalized_recurrence": AUDIT.recurrence(extracted, AUDIT.normalized),
        "extracted_text_word_lengths_including_empty_or_changed_rule": AUDIT.summary(
            [len(text.split()) for _, text in extracted]),
        "lexical_tail": {
            "selected_completed_hops": [item["hop"] for item in tail],
            "included_hops": [item["hop"] for item in included],
            "excluded_hops": [{"hop": item["hop"], "reasons": item["exclusions"]}
                              for item in tail if item["exclusions"]]},
    }
    return metric, [(item["hop"], item["parsed"]["text"]) for item in included]


def build(root):
    root = Path(root)
    config = json.loads((root / "protocol.json").read_text(encoding="utf-8"))
    upstream, _ = AUDIT.audit(root)  # Pure audit call: no rewriting strict outputs.
    require_clean(upstream)
    stream_metrics, documents = {}, []
    for model in config["models"]:
        for seed in config["seeds"]:
            key = model["id"] + "/" + seed["id"]
            expected = upstream["streams"][key]
            completed, receipts = [], 0
            for path in sorted((root / "raw" / model["id"] / seed["id"]).glob("*.response.json")):
                try:
                    receipt = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, ValueError) as exc:
                    raise SnapshotChanged("Response file changed or is being written after the audit.") from exc
                receipts += 1
                if "error_type" in receipt or "response_body" not in receipt:
                    continue
                try:
                    raw = json.loads(receipt["response_body"])
                    output, finish, _ = AUDIT.unpack(model["provider"], raw)
                    cost = AUDIT.price(model, raw)
                except (ValueError, TypeError, KeyError, IndexError):
                    continue  # Accounted as a noncompleted receipt by strict audit.
                if output and finish in ("stop", "end_turn") and cost is not None:
                    completed.append((receipt["hop"], output))
            if receipts != expected["counts"]["receipts"] or len(completed) != expected["counts"]["completed_hops"]:
                raise SnapshotChanged("New receipts appeared between the audit and extraction; retry the snapshot.")
            metric, eligible = measure_stream(completed, config["rule"])
            metric.update(model=model["id"], seed=seed["id"],
                          attempts=expected["counts"]["attempts"], receipts=receipts,
                          pending_hops=expected["pending_hops"],
                          noncompleted_receipts=expected["noncompleted_receipts"],
                          summary_status=expected["summary_status"],
                          usage_cost_upper_estimate_usd=expected["usage_cost_upper_estimate_usd"])
            stream_metrics[key] = metric
            documents.extend((key, hop, passage) for hop, passage in eligible)
    lexical, rows = AUDIT.lexical(documents, stream_metrics)
    lexical["representation"] = (
        "Only explicitly extracted text fields; optional full Markdown fence removal and "
        "json.loads(strict=False) allow literal control characters. Rule and other fields are excluded.")
    lexical["tail_selection"] = (
        "Last 20 completed hops per stream first; then exclude unextractable, empty, or changed/missing-rule "
        "passages. Never backfill. Every source receipt passed the independent integrity audit.")
    formatting = Counter({category: 0 for category in FORMAT_CATEGORIES})
    rules = Counter(unchanged=0, changed_or_missing=0, unassessable_unextractable=0)
    for metric in stream_metrics.values():
        formatting.update(metric["formatting_counts_among_completed"])
        rules.update(metric["rule_survival_among_completed"])
    metrics = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "derived_analysis_version": 1,
        "scope": "Explicit tolerant extraction, separate from strict JSON compliance. Descriptive lexical metrics are not basin identification.",
        "extraction_method": (
            "Reuse extract_passages.extract(): a whole JSON object, optionally enclosed in one full Markdown fence; "
            "try strict JSON first, then allow literal control characters. No quote repair or free-text story extraction."),
        "definitions": {
            "completed_hops": "Normal provider finish, nonempty visible output, known usage estimate, no recorded exception.",
            "full_visible_recurrence": "Every completed response in full, including JSON wrappers, rule text, and non-JSON outcomes.",
            "extracted_text_recurrence": "Every extracted string text, including empty strings or changed/missing rules; wrappers and rule fields excluded.",
            "rule_survival": "Measured only when the extractor returns a text-bearing object; otherwise unassessable, not assumed absent.",
            "normalized_recurrence": "Unicode casefold and whitespace collapsing; punctuation retained.",
            "pending": "Request-only outcomes/billing remain unresolved and are not API or model failures.",
            "noncompleted": "Receipt outcome categories retained from the audit; operational errors are not evidence of model behavior."},
        "upstream_audit": {
            "generated_at": upstream["generated_at"],
            "integrity_errors": 0, "read_issues": 0,
            "observation_status": upstream["observation_status"],
            "run_finished_receipt_present": upstream["run_finished_receipt_present"],
            "totals": upstream["totals"],
            "audit_source_sha256": AUDIT.sha(AUDIT_PATH.read_text(encoding="utf-8")),
            "extractor_source_sha256": AUDIT.sha(EXTRACT_PATH.read_text(encoding="utf-8"))},
        "totals": {
            "completed_hops": sum(s["completed_hops"] for s in stream_metrics.values()),
            "extracted_passages_including_empty_or_changed_rule": sum(
                s["extracted_passages_including_empty_or_changed_rule"] for s in stream_metrics.values()),
            "formatting_counts_among_completed": dict(formatting),
            "rule_survival_among_completed": dict(rules),
            "empty_extracted_passages": sum(len(s["empty_extracted_passage_hops"]) for s in stream_metrics.values()),
            "lexical_tail_included_passages": len(documents)},
        "streams": stream_metrics,
        "lexical": lexical,
    }
    return metrics, rows


def save(root, metrics, rows):
    output = Path(root) / "analysis"
    output.mkdir(parents=True, exist_ok=True)
    for name, content in (
            ("extracted_metrics.json", json.dumps(metrics, ensure_ascii=False, indent=2) + "\n"),
            ("extracted_lexical_similarity.csv", AUDIT.csv_text(rows))):
        temp = output / (name + ".tmp")
        temp.write_text(content, encoding="utf-8", newline="")
        temp.replace(output / name)


def self_test():
    rule = "Shared rule words must not inflate passage similarity."
    bare = json.dumps({"rule": rule, "text": "apple carrot"})
    quartz = json.dumps({"rule": rule, "text": "quartz zircon"})
    literal = '{"rule": ' + json.dumps(rule) + ', "text": "apple\ncarrot"}'
    completed = [(hop, bare) for hop in range(1, 23)]
    completed[3] = (4, "```json\n" + bare + "\n```")
    completed[4] = (5, literal)
    completed[5] = (6, "An unstructured visible response")
    completed[6] = (7, json.dumps({"rule": "different", "text": "apple carrot"}))
    completed[7] = (8, json.dumps({"rule": rule, "text": ""}))
    completed[8] = (9, "```json\n" + literal + "\n```")
    metric, selected = measure_stream(completed, rule)
    assert metric["completed_hops"] == 22
    assert metric["full_visible_exact_recurrence"]["passages"] == 22
    assert metric["extracted_text_exact_recurrence"]["passages"] == 21
    assert metric["formatting_counts_among_completed"] == {
        "bare/strict": 18, "markdown_fence/strict": 1,
        "bare/allow_literal_control_characters": 1,
        "markdown_fence/allow_literal_control_characters": 1, "unextractable": 1}
    assert metric["rule_survival_among_completed"] == {
        "unchanged": 20, "changed_or_missing": 1, "unassessable_unextractable": 1}
    assert metric["empty_extracted_passage_hops"] == [8]
    assert metric["lexical_tail"]["selected_completed_hops"] == list(range(3, 23))
    assert [hop for hop, _ in selected] == [hop for hop in range(3, 23) if hop not in (6, 7, 8)]
    assert metric["extracted_text_case_whitespace_normalized_recurrence"]["unique"] == 2
    other, other_selected = measure_stream([(1, quartz)], rule)
    lexical, rows = AUDIT.lexical(
        [("a", hop, text) for hop, text in selected] + [("b", hop, text) for hop, text in other_selected],
        {"a": metric, "b": other})
    assert lexical["vocabulary_size"] == 4
    assert rows[1][2] == 0.0, "Repeated rule contaminated the extracted passage vectors"
    require_clean({"errors": [], "read_issues": []})
    for invalid in ({"errors": [{"code": "test"}], "read_issues": []},
                    {"errors": [], "read_issues": [{"path": "test"}]}):
        try:
            require_clean(invalid)
        except AuditRejected:
            pass
        else:
            raise AssertionError("Upstream integrity failure was accepted")
    print("Synthetic checks passed: distinct recurrence populations, all five format categories, rule/empty/unextractable counts, tail selection without backfill, rule-only exclusion, and upstream rejection.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=HERE)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    try:
        for attempt in range(3):
            try:
                metrics, rows = build(args.root)
                break
            except SnapshotChanged:
                if attempt == 2:
                    raise
        save(args.root, metrics, rows)
    except (AuditRejected, SnapshotChanged) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps({"observation_status": metrics["upstream_audit"]["observation_status"],
                      "totals": metrics["totals"]}, indent=2))


if __name__ == "__main__":
    main()
