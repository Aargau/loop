"""Offline, auditable snapshots of the previous/next/worse/better operator study.

No API calls or credentials. Only analysis/ is written. Repetitions are observed
events, not claims that a stochastic trajectory has reached a permanent fixed point.
"""
from collections import Counter
import argparse
import csv
import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import random
import re
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "basins_20260922_sunset" / "extracted_metrics.py"
SPEC = importlib.util.spec_from_file_location("operator_extraction_metrics", SOURCE)
DERIVED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DERIVED)
AUDIT, EXTRACT = DERIVED.AUDIT, DERIVED.EXTRACT
OPERATORS = ("previous", "next", "worse", "better")
MODELS = ("gpt-6-luna", "gpt-6-sol", "gpt-6-astra", "claude-fable-5-1", "claude-opus-5-5")
SAMPLE_HOPS = (1, 2, 3, 5, 10, 20, 30, 36, 37, 38, 39, 40)
SHUFFLE_SEED = 26092240
STUDY_BUDGET = 20.0
DISPLAY_NOTE = ("Display only: C0 control characters other than newline and tab are shown as visible \\uXXXX escapes. "
                "Raw responses, extracted metric inputs, hashes, and equality comparisons remain unchanged. "
                "Literal U+FFFD is retained as generated text; its occurrence is not a decoding diagnosis.")


class SnapshotChanged(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise DERIVED.AuditRejected(message)


def identity_map():
    streams = [(operator, model) for operator in OPERATORS for model in MODELS]
    random.Random(SHUFFLE_SEED).shuffle(streams)
    return {f"O{index:02d}": {"operator": operator, "model": model}
            for index, (operator, model) in enumerate(streams, 1)}


def consecutive_events(completed):
    events = []
    for (a_hop, a_text), (b_hop, b_text) in zip(completed, completed[1:]):
        if b_hop != a_hop + 1:
            continue
        a_passage, b_passage = EXTRACT.extract(a_text), EXTRACT.extract(b_text)
        comparable = a_passage is not None and b_passage is not None
        event = {"from_hop": a_hop, "to_hop": b_hop,
                 "full_output_exact": a_text == b_text,
                 "full_output_normalized": AUDIT.normalized(a_text) == AUDIT.normalized(b_text),
                 "extracted_text_exact": a_passage["text"] == b_passage["text"] if comparable else None,
                 "extracted_text_normalized": AUDIT.normalized(a_passage["text"]) == AUDIT.normalized(b_passage["text"])
                                              if comparable else None}
        if any(event[key] is True for key in (
                "full_output_exact", "full_output_normalized", "extracted_text_exact", "extracted_text_normalized")):
            events.append(event)
    return events


def current_status(audited, receipts):
    if audited["summary_status"] is not None:
        return audited["summary_status"]
    if receipts:
        status = receipts[-1].get("stream_status", "unknown")
        if status != "active":
            return status
        return "active"
    return "awaiting_receipt" if audited["counts"]["attempts"] else "not_started"


def stopped(status):
    return status not in ("active", "awaiting_receipt", "not_started", "unknown")


def chosen_samples(receipts, status):
    visible = [receipt for receipt in receipts if isinstance(receipt.get("output"), str) and receipt["output"]]
    selected = set(SAMPLE_HOPS)
    if stopped(status):
        if receipts:
            selected.add(receipts[-1]["hop"])
        if visible:
            selected.add(visible[-1]["hop"])
    return [receipt for receipt in receipts if receipt["hop"] in selected]


def provider_outcome(receipt):
    """Inspect the raw provider response independently of legacy runner labels."""
    raw = None
    try:
        if "response_body" in receipt:
            raw = json.loads(receipt["response_body"])
    except (ValueError, TypeError):
        pass
    finish, details, refusal = None, None, receipt.get("refusal")
    if isinstance(raw, dict):
        details = raw.get("stop_details")
        if "stop_reason" in raw:
            finish = raw["stop_reason"]
        elif raw.get("choices"):
            choice = raw["choices"][0]
            finish = choice.get("finish_reason")
            details = choice.get("stop_details", details)
            refusal = choice.get("message", {}).get("refusal", refusal)
    provider_refusal = finish == "refusal" or bool(refusal)
    has_output = isinstance(receipt.get("output"), str) and bool(receipt["output"])
    if provider_refusal:
        classification = "provider_refusal"
    elif receipt.get("error_type"):
        classification = "http_error" if (receipt.get("http_status") or 0) >= 400 else "recorded_exception"
    elif not has_output:
        classification = "unexplained_empty_output"
    elif finish in ("length", "max_tokens"):
        classification = "truncated_output"
    elif finish not in ("stop", "end_turn"):
        classification = "abnormal_provider_finish"
    elif receipt.get("usage_cost_upper_estimate_usd") is None:
        classification = "missing_usage"
    else:
        classification = "normal_visible_output"
    return {"hop": receipt["hop"], "classification": classification,
            "http_status": receipt.get("http_status"), "error_type": receipt.get("error_type"),
            "provider_finish_reason": finish, "provider_stop_details": details,
            "provider_refusal": provider_refusal, "provider_refusal_field": refusal,
            "has_nonempty_visible_output": has_output, "legacy_stream_status": receipt.get("stream_status")}


def complete_receipts(model, receipts):
    completed = []
    for receipt in receipts:
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
    return completed


def enrich(completed, rule, receipts, status):
    metrics, _ = DERIVED.measure_stream(completed, rule)
    metrics["observed_consecutive_equality_events"] = consecutive_events(completed)
    metrics["consecutive_equality_counts"] = {
        field: sum(event[field] is True for event in metrics["observed_consecutive_equality_events"])
        for field in ("full_output_exact", "full_output_normalized", "extracted_text_exact", "extracted_text_normalized")}
    final = EXTRACT.extract(completed[-1][1]) if completed else None
    metrics["final_completed_hop"] = completed[-1][0] if completed else None
    metrics["final_completed_extracted_words"] = len(final["text"].split()) if final is not None else None
    metrics["final_completed_full_visible_words"] = len(completed[-1][1].split()) if completed else None
    metrics["max_completed_extracted_words"] = metrics["extracted_text_word_lengths_including_empty_or_changed_rule"]["max"]
    sizes = []
    for hop, output in completed:
        parsed = EXTRACT.extract(output)
        text = parsed["text"] if parsed is not None else None
        sizes.append({"hop": hop, "extracted_characters": len(text) if text is not None else None,
                      "extracted_words": len(text.split()) if text is not None else None,
                      "u0000_count": text.count("\x00") if text is not None else None,
                      "u_fffd_count": text.count("\ufffd") if text is not None else None})
    metrics["per_completed_hop_extracted_sizes"] = sizes
    metrics["final_completed_extracted_characters"] = sizes[-1]["extracted_characters"] if sizes else None
    metrics["max_completed_extracted_characters"] = max(
        (item["extracted_characters"] for item in sizes if item["extracted_characters"] is not None), default=None)
    metrics["completed_extracted_character_counts"] = {
        "u0000": sum(item["u0000_count"] or 0 for item in sizes),
        "u_fffd": sum(item["u_fffd_count"] or 0 for item in sizes)}
    visible = [r for r in receipts if isinstance(r.get("output"), str) and r["output"]]
    if visible:
        last = visible[-1]
        parsed = EXTRACT.extract(last["output"])
        metrics["last_observed_visible_output"] = {
            "hop": last["hop"], "is_completed": last["hop"] in {hop for hop, _ in completed},
            "full_visible_words": len(last["output"].split()),
            "extracted_words": len(parsed["text"].split()) if parsed is not None else None}
    else:
        metrics["last_observed_visible_output"] = None
    sampled = chosen_samples(receipts, status)
    metrics["sampled_receipt_hops"] = [r["hop"] for r in sampled]
    metrics["sampled_visible_hops"] = [r["hop"] for r in sampled if r.get("output")]
    outcomes = [provider_outcome(receipt) for receipt in receipts]
    completed_hops = {hop for hop, _ in completed}
    metrics["provider_outcome_counts"] = dict(Counter(item["classification"] for item in outcomes))
    metrics["provider_finish_reason_counts"] = dict(Counter(str(item["provider_finish_reason"]) for item in outcomes))
    metrics["provider_refusal_hops"] = [item["hop"] for item in outcomes if item["provider_refusal"]]
    metrics["noncompleted_or_refusal_provider_outcomes"] = [
        item for item in outcomes if item["hop"] not in completed_hops or item["provider_refusal"]]
    return metrics


def build(root):
    mapping = identity_map()
    aliases = {(value["operator"], value["model"]): alias for alias, value in mapping.items()}
    arms, streams, captured = {}, {}, {}
    for operator in OPERATORS:
        source = root / operator
        protocol_path = source / "protocol.json"
        if not protocol_path.exists():
            arms[operator] = {"observation_status": "Protocol not present; arm not started in this snapshot.",
                              "run_finished_receipt_present": False, "audit_performed": False,
                              "usage_cost_upper_estimate_usd": 0.0, "retained_unknown_reserve_usd": 0.0,
                              "planned_budget_usd": 5.0}
            for model in MODELS:
                key = operator + "/" + model
                streams[key] = {**enrich([], "", [], "not_started"), "operator": operator, "model": model,
                                "alias": aliases[(operator, model)], "status": "not_started", "attempts": 0,
                                "receipts": 0, "pending_hops": [], "noncompleted_receipts": [],
                                "usage_cost_upper_estimate_usd": 0.0, "retained_unknown_reserve_usd": 0.0,
                                "seed_id": None, "audit_performed": False}
                captured[key] = {"receipts": [], "rule": None}
            continue
        try:
            config = json.loads(protocol_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise SnapshotChanged("Protocol is currently unreadable: " + operator) from exc
        require(set(m["id"] for m in config["models"]) == set(MODELS) and len(config["models"]) == 5,
                "Unexpected model roster in " + operator)
        require(len(config["seeds"]) == 1 and config["seeds"][0]["text"] == "The sun was setting behind the hills.",
                "Expected one exact sunset seed in " + operator)
        require(config["hops"] == 40 and config["budget_usd"] == 5,
                "Expected forty hops and a $5 arm budget in " + operator)
        audited, _ = AUDIT.audit(source)
        if audited["read_issues"] and not audited["errors"]:
            raise SnapshotChanged("Raw files may be mid-write in " + operator)
        DERIVED.require_clean(audited)
        totals = audited["totals"]
        arms[operator] = {"observation_status": audited["observation_status"],
                          "run_finished_receipt_present": audited["run_finished_receipt_present"],
                          "audit_performed": True, "audit_generated_at": audited["generated_at"],
                          "integrity_errors": 0, "read_issues": 0, "rule": config["rule"],
                          "protocol_sha256": AUDIT.sha(protocol_path.read_text(encoding="utf-8")),
                          "usage_cost_upper_estimate_usd": totals["usage_cost_upper_estimate_usd"],
                          "retained_unknown_reserve_usd": totals["uncertain_cost_reserve_usd"] + totals["pending_cost_reserve_usd"],
                          "planned_budget_usd": config["budget_usd"], "audit_totals": totals}
        seed_id = config["seeds"][0]["id"]
        for model in config["models"]:
            model_id = model["id"]
            expected = audited["streams"][model_id + "/" + seed_id]
            receipts = []
            for path in sorted((source / "raw" / model_id / seed_id).glob("*.response.json")):
                try:
                    receipts.append(json.loads(path.read_text(encoding="utf-8")))
                except (OSError, ValueError) as exc:
                    raise SnapshotChanged("Receipt changed after audit: " + str(path)) from exc
            completed = complete_receipts(model, receipts)
            if len(receipts) != expected["counts"]["receipts"] or len(completed) != expected["counts"]["completed_hops"]:
                raise SnapshotChanged("New receipts appeared after audit in " + operator + "/" + model_id)
            status = current_status(expected, receipts)
            key = operator + "/" + model_id
            metric = enrich(completed, config["rule"], receipts, status)
            metric.update(operator=operator, model=model_id, alias=aliases[(operator, model_id)], status=status,
                          attempts=expected["counts"]["attempts"], receipts=len(receipts),
                          pending_hops=expected["pending_hops"], noncompleted_receipts=expected["noncompleted_receipts"],
                          usage_cost_upper_estimate_usd=expected["usage_cost_upper_estimate_usd"],
                          retained_unknown_reserve_usd=expected["uncertain_cost_reserve_usd"] + expected["pending_cost_reserve_usd"],
                          seed_id=seed_id, audit_performed=True,
                          strict_json_valid_completed_passages=expected["counts"]["valid_passages"])
            streams[key] = metric
            captured[key] = {"receipts": receipts, "rule": config["rule"]}
    usage = sum(arm["usage_cost_upper_estimate_usd"] for arm in arms.values())
    reserve = sum(arm["retained_unknown_reserve_usd"] for arm in arms.values())
    require(usage + reserve <= STUDY_BUDGET + 1e-6, "Usage plus retained reserves exceeds the new study's $20 budget.")
    require(abs(usage - sum(stream["usage_cost_upper_estimate_usd"] for stream in streams.values())) <= 1e-8,
            "Per-stream usage failed to reconcile with the arm audits.")
    require(abs(reserve - sum(stream["retained_unknown_reserve_usd"] for stream in streams.values())) <= 1e-8,
            "Per-stream retained reserves failed to reconcile with the arm audits.")
    metrics = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(), "analysis_version": 1,
        "all_arms_finalized": all(arm["run_finished_receipt_present"] for arm in arms.values()),
        "scope": "Only the new four-operator study. Prior basin-study costs and outputs are excluded.",
        "definitions": {
            "completed": "Normal provider finish, nonempty visible output, known usage, no recorded exception; JSON compliance is separate.",
            "recurrence": "First repeated complete visible response or extracted text, with exact and case/whitespace-normalized variants. An observed repeat is not a permanent fixed point.",
            "consecutive_equality": "Compare neighboring completed hops only when their original hop numbers differ by one. Extracted equality is null if either text is unextractable.",
            "extraction": "Whole text-bearing JSON object; optional full Markdown fence removal and literal control-character parsing. No quote repair or prose extraction.",
            "rule_survival": "Rule status is assessed only when extraction succeeds; unextractable outputs are retained as unassessable outcomes.",
            "unextractable": "The declared whole-object extraction failed. This does not imply absence of fiction, reasoning, or other substantive content; complete visible text is exported.",
            "provider_refusal": "Raw finish/stop reason 'refusal' or a nonempty provider refusal field, independently of the runner's legacy refusal/empty-output labels. Raw stop_details are retained.",
            "word_counts": "Final/max extracted-word counts use completed hops. Final is null if the actual last completed output is unextractable; no backfill. Noncompleted final visible output is recorded separately.",
            "character_counts": "Python Unicode string length, not bytes or grapheme clusters; per-hop characters/words and U+0000/U+FFFD occurrence counts are null when text is unextractable. Literal character counts do not diagnose corruption or decoding failure.",
            "display_controls": DISPLAY_NOTE,
            "sampling": "Predeclared receipt hops plus the final attempted receipt and final nonempty visible output if stopped at other hops. Empty refusals and nonempty abnormal finishes are exported. Missing hops are never replaced with nearby observations.",
            "unknown_cost": "Unknown receipt billing and pending request reserves are retained. Pending outcomes and transport errors do not establish model failure.",
            "snapshots": "Arms are audited sequentially. This is a timestamped read-only snapshot, not a simultaneous observation of all workers."},
        "identity_masking": {"shuffle_seed": SHUFFLE_SEED, "aliases": "O01 through O20",
                             "sample_hops": list(SAMPLE_HOPS), "mapping_file": "identity_map.json",
                             "limitation": "Model/operator labels are withheld in samples; output content itself may disclose the instruction."},
        "totals": {"streams": len(streams), "attempts": sum(s["attempts"] for s in streams.values()),
                   "completed_hops": sum(s["completed_hops"] for s in streams.values()),
                   "usage_cost_upper_estimate_usd": usage, "retained_unknown_reserve_usd": reserve,
                   "usage_plus_reserves_usd": usage + reserve, "budget_limit_usd": STUDY_BUDGET,
                   "within_budget": True},
        "arms": arms, "streams": streams,
        "source_code_hashes": {"audit": AUDIT.sha(DERIVED.AUDIT_PATH.read_text(encoding="utf-8")),
                               "extractor": AUDIT.sha(DERIVED.EXTRACT_PATH.read_text(encoding="utf-8")),
                               "extracted_metrics": AUDIT.sha(SOURCE.read_text(encoding="utf-8"))}}
    return metrics, mapping, captured


def fence(text):
    text = re.sub(r"[\x00-\x08\x0b-\x1f]", lambda match: f"\\u{ord(match[0]):04X}", text)
    marker = "`" * max(3, 1 + max((len(run) for run in re.findall(r"`+", text)), default=0))
    return marker + "text\n" + text + "\n" + marker


def rendered_output(receipt, rule, masked=False):
    outcome = provider_outcome(receipt)
    prefix = ("Provider outcome: `" + outcome["classification"] + "`; raw finish/stop reason: `"
              + str(outcome["provider_finish_reason"]) + "`.\n")
    if outcome["provider_stop_details"] is not None:
        prefix += "\nRaw provider stop details:\n\n" + fence(json.dumps(
            outcome["provider_stop_details"], ensure_ascii=False, indent=2)) + "\n"
    if outcome["provider_refusal_field"]:
        prefix += "\nProvider refusal field:\n\n" + fence(str(outcome["provider_refusal_field"])) + "\n"
    output = receipt.get("output")
    if not isinstance(output, str) or not output:
        return prefix + "\nNo nonempty visible output was saved. Legacy runner status: `" + str(receipt.get("stream_status")) + "`.\n"
    parsed = EXTRACT.extract(output)
    if parsed is None:
        return prefix + "\nComplete visible output; no text field was extractable under the declared whole-object method.\n\n" + fence(output) + "\n"
    note = "Extracted text: " + parsed["wrapper"] + "/" + parsed["parser"] + "."
    if not masked:
        note += " Original rule preserved: " + str(parsed["rule"] == rule) + "."
    text = prefix + "\n" + note + "\n\n" + fence(parsed["text"]) + "\n"
    if not masked:
        text += "\nExact visible output, retained separately from extraction:\n\n" + fence(output) + "\n"
    return text


def transcripts(metrics, mapping, captured):
    files = {}
    for key, stream in metrics["streams"].items():
        operator, model = stream["operator"], stream["model"]
        data = captured[key]
        text = [f"# {operator}: {model}", "", f"Snapshot: {metrics['generated_at']}. Status: `{stream['status']}`.", "",
                "Readable derived transcript. Exact visible responses are preserved below with the display escaping described here; no extraction was fed into generation.", "",
                DISPLAY_NOTE, ""]
        for receipt in data["receipts"]:
            text.extend([f"## Hop {receipt['hop']}", "", "Receipt status: `" + str(receipt.get("stream_status")) + "`.", "",
                         rendered_output(receipt, data["rule"])])
        if stream["pending_hops"]:
            text.extend(["## Pending requests", "", "No readable response receipt for hops: "
                         + ", ".join(map(str, stream["pending_hops"])) + ". Outcome and billing remain unresolved.", ""])
        if not data["receipts"]:
            text.extend(["No response receipts exist in this snapshot.", ""])
        files[f"transcripts/{operator}/{model}.md"] = "\n".join(text)
        selected = chosen_samples(data["receipts"], stream["status"])
        masked = [f"# Stream {stream['alias']}", "", "Model and operator labels withheld.", "",
                  DISPLAY_NOTE, "",
                  f"Predeclared sampled hops: {list(SAMPLE_HOPS)}. A stopped trajectory's final attempted receipt and final nonempty visible output "
                  "are also included when they fall at other hops. Empty refusals and abnormal finishes are retained. Missing observations are not backfilled.", "",
                  "Observed sampled hops: " + (", ".join(str(r["hop"]) for r in selected) or "none") + ".", ""]
        for receipt in selected:
            masked.extend([f"## Hop {receipt['hop']}", "", rendered_output(receipt, data["rule"], masked=True)])
        files[f"masked_samples/{stream['alias']}.md"] = "\n".join(masked)
    return files


def first_repeat(stream, population, normalized=False):
    suffix = "case_whitespace_normalized_recurrence" if normalized else "exact_recurrence"
    return stream[population + "_" + suffix]["first_repeat_hop"]


def cell(value):
    return "null" if value is None else str(value)


def summary_table(metrics):
    totals = metrics["totals"]
    lines = ["# Operator-study snapshot", "", "Snapshot: " + metrics["generated_at"] + ". "
             + ("All four arms have final receipts." if metrics["all_arms_finalized"] else
                "Incomplete: one or more arms have no final receipt; they may be running, not started, or interrupted."), "",
             "Formatting counts cover completed responses: B = bare strict JSON, F = fenced strict JSON, "
             "BC/FC = bare/fenced JSON allowing literal control characters, U = unextractable. Rule survival is unchanged / extractable; "
             "unextractable rules are unassessable. Repeat columns give first repeated hop, exact / case-and-whitespace-normalized. "
             "Final extracted word count is null when the last completed output is unextractable; no earlier text replaces it.", "",
             "| Operator | Model | Attempts / completed | Status | Provider refusals | B/F/BC/FC/U | Rule unchanged / extracted | First full repeat E/N | First text repeat E/N | Final / max extracted words | Final / max extracted characters | U+0000 / U+FFFD occurrences | Usage $ | Unknown reserve $ |",
             "| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | ---: | ---: |"]
    for stream in metrics["streams"].values():
        formats = stream["formatting_counts_among_completed"]
        format_text = "/".join(str(formats[key]) for key in DERIVED.FORMAT_CATEGORIES)
        full_repeat = "/".join(cell(first_repeat(stream, "full_visible", normalized)) for normalized in (False, True))
        text_repeat = "/".join(cell(first_repeat(stream, "extracted_text", normalized)) for normalized in (False, True))
        rules = stream["rule_survival_among_completed"]
        lines.append(f"| {stream['operator']} | {stream['model']} | {stream['attempts']} / {stream['completed_hops']} | "
                     f"{stream['status']} | {len(stream['provider_refusal_hops'])} | {format_text} | {rules['unchanged']} / {stream['extracted_passages_including_empty_or_changed_rule']} | "
                     f"{full_repeat} | {text_repeat} | {cell(stream['final_completed_extracted_words'])} / {cell(stream['max_completed_extracted_words'])} | "
                     f"{cell(stream['final_completed_extracted_characters'])} / {cell(stream['max_completed_extracted_characters'])} | "
                     f"{stream['completed_extracted_character_counts']['u0000']} / {stream['completed_extracted_character_counts']['u_fffd']} | "
                     f"{stream['usage_cost_upper_estimate_usd']:.6f} | {stream['retained_unknown_reserve_usd']:.6f} |")
    lines.extend(["", f"New-study usage estimate **${totals['usage_cost_upper_estimate_usd']:.6f}** + retained unknown reserves "
                  f"**${totals['retained_unknown_reserve_usd']:.6f}** = **${totals['usage_plus_reserves_usd']:.6f}**, "
                  f"within **${totals['budget_limit_usd']:.2f}**. Each arm is independently capped at $5. Prior-study spending is not included.", "",
                  "Operational stops and pending requests remain explicit. An observed repeat does not establish a permanent fixed point. "
                  "`repeating_runs.md` and `repetition_events.csv` identify exact recorded recurrence/equality events.", ""])
    return "\n".join(lines)


def repetition_exports(metrics):
    lines = ["# Observed repetitions", "", "A repeat is a recorded recurrence, not evidence of a permanent fixed point. "
             "Only completed hops enter this table. Consecutive equality requires neighboring original hop numbers; "
             "missing or unextractable observations are never silently bridged.", "",
             "| Alias | Operator | Model | First full repeat exact / normalized | First extracted repeat exact / normalized | Consecutive full exact / normalized | Consecutive text exact / normalized |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    rows = [["alias", "operator", "model", "from_hop", "to_hop", "full_output_exact", "full_output_normalized",
             "extracted_text_exact", "extracted_text_normalized"]]
    repeated = 0
    for stream in metrics["streams"].values():
        full = [first_repeat(stream, "full_visible", normalized) for normalized in (False, True)]
        text = [first_repeat(stream, "extracted_text", normalized) for normalized in (False, True)]
        if any(hop is not None for hop in full + text):
            repeated += 1
            counts = stream["consecutive_equality_counts"]
            lines.append(f"| {stream['alias']} | {stream['operator']} | {stream['model']} | {' / '.join(map(cell, full))} | "
                         f"{' / '.join(map(cell, text))} | {counts['full_output_exact']} / {counts['full_output_normalized']} | "
                         f"{counts['extracted_text_exact']} / {counts['extracted_text_normalized']} |")
        for event in stream["observed_consecutive_equality_events"]:
            rows.append([stream["alias"], stream["operator"], stream["model"], event["from_hop"], event["to_hop"]]
                        + [event[field] for field in rows[0][5:]])
    if not repeated:
        lines.extend(["", "No full-output or extracted-text repeat was found among the completed observations in this snapshot."])
    lines.extend(["", "First-recurrence and all repeated-state hop lists are preserved in `metrics.json`. "
                  "The CSV lists consecutive transitions with at least one true equality; an empty extracted equality means "
                  "at least one side was unextractable.", ""])
    target = io.StringIO(newline="")
    csv.writer(target).writerows(rows)
    return "\n".join(lines), target.getvalue()


def save(root, metrics, mapping, captured):
    repetitions, csv_data = repetition_exports(metrics)
    files = transcripts(metrics, mapping, captured)
    files.update({"metrics.json": json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
                  "identity_map.json": json.dumps(mapping, indent=2) + "\n",
                  "comparison_table.md": summary_table(metrics),
                  "repeating_runs.md": repetitions, "repetition_events.csv": csv_data})
    for relative, content in files.items():
        target = root / "analysis" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(target.name + ".tmp")
        temp.write_text(content, encoding="utf-8", newline="")
        temp.replace(target)


def self_test():
    rule = "Use the same rule."
    bare = json.dumps({"rule": rule, "text": "apple carrot"})
    folded = json.dumps({"rule": rule, "text": "Apple  CARROT"})
    fenced = "```json\n" + bare + "\n```"
    completed = [(1, bare), (2, bare), (3, folded), (4, fenced), (6, fenced), (7, "visible prose")]
    receipts = [{"hop": hop, "output": output, "stream_status": "active"} for hop, output in completed]
    metrics = enrich(completed, rule, receipts, "transport_or_parse_error")
    assert metrics["full_visible_exact_recurrence"]["first_repeat_hop"] == 2
    assert metrics["extracted_text_exact_recurrence"]["first_repeat_hop"] == 2
    assert metrics["final_completed_extracted_words"] is None and metrics["max_completed_extracted_words"] == 2
    assert metrics["sampled_visible_hops"] == [1, 2, 3, 7]
    assert [r["hop"] for r in chosen_samples(receipts, "active")] == [1, 2, 3]
    events = metrics["observed_consecutive_equality_events"]
    assert events[0]["full_output_exact"] is True and events[0]["extracted_text_exact"] is True
    assert any(e["to_hop"] == 3 and e["extracted_text_normalized"] and not e["extracted_text_exact"] for e in events)
    assert not any(e["from_hop"] == 4 and e["to_hop"] == 6 for e in events)
    assert metrics["rule_survival_among_completed"]["unassessable_unextractable"] == 1
    assert metrics["formatting_counts_among_completed"]["markdown_fence/strict"] == 2
    aliases = identity_map()
    assert list(aliases) == [f"O{i:02d}" for i in range(1, 21)] and len({tuple(v.values()) for v in aliases.values()}) == 20
    assert aliases == identity_map()
    long = [(hop, "plain prose" if hop == 39 else bare) for hop in range(1, 41)]
    tail = enrich(long, rule, [], "hop_limit")["lexical_tail"]
    assert tail["selected_completed_hops"] == list(range(21, 41)) and 39 not in tail["included_hops"]
    assert tail["included_hops"][0] == 21
    assert fence("contains ``` marker").startswith("````text\n")
    refusal = {"hop": 8, "output": "", "stream_status": "empty_output", "http_status": 200,
               "refusal": None, "usage_cost_upper_estimate_usd": 0.01,
               "response_body": json.dumps({"content": [], "stop_reason": "refusal",
                                            "stop_details": {"type": "refusal", "category": "reasoning_extraction"}})}
    outcome = provider_outcome(refusal)
    assert outcome["provider_refusal"] and outcome["classification"] == "provider_refusal"
    assert outcome["provider_stop_details"]["category"] == "reasoning_extraction"
    assert [r["hop"] for r in chosen_samples(receipts + [refusal], "empty_output")] == [1, 2, 3, 7, 8]
    rendered = rendered_output(refusal, rule, masked=True)
    assert "reasoning_extraction" in rendered and "No nonempty visible output" in rendered
    abnormal = {"hop": 9, "output": "partial visible text", "stream_status": "abnormal_finish:max_tokens",
                "response_body": json.dumps({"content": [{"type": "text", "text": "partial visible text"}],
                                             "stop_reason": "max_tokens"})}
    assert "partial visible text" in rendered_output(abnormal, rule, masked=True)
    assert provider_outcome(abnormal)["classification"] == "truncated_output"
    original_text = "alpha\x00\x01 beta\ufffd\n\ttail"
    controlled_output = json.dumps({"rule": rule, "text": original_text})
    controlled = enrich([(1, controlled_output), (2, controlled_output)], rule,
                        [{"hop": 1, "output": controlled_output, "stream_status": "active"}], "active")
    assert controlled["final_completed_extracted_characters"] == len(original_text)
    assert controlled["per_completed_hop_extracted_sizes"][0]["extracted_words"] == len(original_text.split())
    assert controlled["completed_extracted_character_counts"] == {"u0000": 2, "u_fffd": 2}
    assert controlled["extracted_text_exact_recurrence"]["repeated_states"][0]["sha256"] == AUDIT.sha(original_text)
    shown = fence(original_text)
    assert "\\u0000\\u0001" in shown and "\x00" not in shown and "\x01" not in shown
    assert "\ufffd" in shown and "\n\t" in shown
    assert EXTRACT.extract(controlled_output)["text"] == original_text
    import tempfile
    with tempfile.TemporaryDirectory(prefix="operator-analysis-test-") as folder:
        root = Path(folder)
        result, mapping, captured = build(root)
        assert result["totals"]["streams"] == 20 and result["totals"]["completed_hops"] == 0
        assert not result["all_arms_finalized"] and result["totals"]["usage_plus_reserves_usd"] == 0
        save(root, result, mapping, captured)
        assert len(list((root / "analysis/masked_samples").glob("O*.md"))) == 20
        assert len(list((root / "analysis/transcripts").glob("*/*.md"))) == 20
        saved = json.loads((root / "analysis/metrics.json").read_text(encoding="utf-8"))
        assert saved["totals"] == result["totals"]
    print("Synthetic checks passed: recurrence/equality, no bridging/backfill, formatting, final-null word counts, stopped final samples, provider outcomes, control-display escaping with unchanged metric/hash inputs, stable aliases, and incomplete snapshot exports.")


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
                metrics, mapping, captured = build(args.root)
                break
            except SnapshotChanged:
                if attempt == 2:
                    raise
        save(args.root, metrics, mapping, captured)
    except (DERIVED.AuditRejected, SnapshotChanged) as exc:
        print("Analysis not rewritten: " + str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps({"all_arms_finalized": metrics["all_arms_finalized"], "totals": metrics["totals"]}, indent=2))


if __name__ == "__main__":
    main()
