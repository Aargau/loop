"""Offline receipt/chain audit and descriptive passage-only lexical metrics.

No network access or imports from the generation runner. Safe to rerun during a
live run; unfinished receipts are reported, and only analysis/ is overwritten.
Use --self-test for synthetic chain, accounting, and contamination checks.
"""
from collections import Counter, defaultdict
import argparse
import csv
import datetime as dt
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import re
import statistics
import tempfile


STOPWORDS = frozenset("""a an and are as at be been being but by can could did do
does doing for from had has have having he her here hers herself him himself his
how i if in into is it its itself me more most my myself no nor not of on once
only or other our ours ourselves out over own same she should so some such than
that the their theirs them themselves then there these they this those through
to too under until up very was we were what when where which while who whom why
will with would you your yours yourself yourselves""".split())
TOKEN_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")
TAIL_SIZE = 20


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized(text):
    return " ".join(text.casefold().split())


def summary(values):
    if not values:
        return {"n": 0, "min": None, "mean": None, "median": None, "max": None}
    return {"n": len(values), "min": min(values), "mean": statistics.mean(values),
            "median": statistics.median(values), "max": max(values)}


def passage_info(output, rule):
    try:
        obj = json.loads(output)
    except (ValueError, TypeError):
        return None, {"json_object": False, "rule_unchanged": False}, ["invalid_json"]
    if not isinstance(obj, dict):
        return None, {"json_object": False, "rule_unchanged": False}, ["not_json_object"]
    passage = obj.get("text")
    is_string = isinstance(passage, str)
    unchanged = obj.get("rule") == rule
    info = {"json_object": True, "rule_unchanged": unchanged,
            "passage_is_string": is_string,
            "passage_sha256": sha(passage) if is_string else None,
            "passage_words": len(passage.split()) if is_string else None}
    reasons = []
    if not unchanged:
        reasons.append("changed_or_missing_rule")
    if not is_string:
        reasons.append("non_string_or_missing_text")
    elif not passage.strip():
        reasons.append("empty_passage")
    return passage if is_string else None, info, reasons


def unpack(provider, response):
    if provider == "openai":
        choice = response["choices"][0]
        message = choice["message"]
        return message.get("content") or "", choice["finish_reason"], message.get("refusal")
    return ("".join(b["text"] for b in response["content"] if b["type"] == "text"),
            response["stop_reason"], None)


def price(model, response):
    usage = response.get("usage", {})
    if model["provider"] == "openai":
        if "prompt_tokens" not in usage or "completion_tokens" not in usage:
            return None
        inp, out = usage["prompt_tokens"], usage["completion_tokens"]
    else:
        if "input_tokens" not in usage or "output_tokens" not in usage:
            return None
        inp = (usage["input_tokens"] + usage.get("cache_read_input_tokens", 0)
               + 2 * usage.get("cache_creation_input_tokens", 0))
        out = usage["output_tokens"]
    return (inp * model["input_usd_per_million"] + out * model["output_usd_per_million"]) / 1e6


def expected_body(config, model, state):
    body = {"model": model["id"], "messages": [{"role": "user", "content": state}]}
    if model["provider"] == "openai":
        body.update(max_completion_tokens=config["max_output_tokens"],
                    reasoning_effort=config["reasoning_effort"])
    else:
        body.update(max_tokens=config["max_output_tokens"],
                    output_config={"effort": config["reasoning_effort"]})
    return body


def recurrence(items, transform):
    seen = defaultdict(list)
    for hop, passage in items:
        seen[sha(transform(passage))].append(hop)
    repeats = [{"sha256": key, "hops": hops} for key, hops in seen.items() if len(hops) > 1]
    return {"passages": len(items), "unique": len(seen),
            "repeated_occurrences_after_first": len(items) - len(seen),
            "first_repeat_hop": min((r["hops"][1] for r in repeats), default=None),
            "repeated_states": repeats}


def dot(left, right):
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(term, 0) for term, value in left.items())


def unit(values):
    norm = math.sqrt(sum(v * v for v in values.values()))
    return {k: v / norm for k, v in values.items()} if norm else {}


def lexical(documents, stream_metrics):
    """Fit a single vocabulary/IDF to eligible passages in preselected tails."""
    counts = [Counter(t for t in TOKEN_RE.findall(d[2].lower())
                      if len(t) >= 2 and t not in STOPWORDS) for d in documents]
    df = Counter(term for count in counts for term in count)
    n = len(counts)
    idf = {term: math.log((1 + n) / (1 + frequency)) + 1 for term, frequency in df.items()}
    vectors = [unit({term: frequency * idf[term] for term, frequency in count.items()})
               for count in counts]
    grouped = defaultdict(list)
    zero_documents = []
    for (stream, hop, _), vector in zip(documents, vectors):
        if vector:
            grouped[stream].append((hop, vector))
        else:
            zero_documents.append({"stream": stream, "hop": hop})
    centroids = {}
    for stream, metrics in stream_metrics.items():
        group = grouped[stream]
        aggregate = Counter()
        for _, vector in group:
            aggregate.update(vector)
        centroids[stream] = unit(aggregate)
        metrics["lexical_tail"].update(
            nonzero_vectors=len(group),
            zero_token_hops=[d["hop"] for d in zero_documents if d["stream"] == stream],
            within_pairwise_cosine=summary([dot(a[1], b[1]) for a, b in itertools.combinations(group, 2)]),
            consecutive_hop_cosine=summary([dot(a[1], b[1]) for a, b in zip(group, group[1:])
                                           if b[0] == a[0] + 1]))
    names = list(stream_metrics)
    rows = [["stream"] + names]
    for left in names:
        rows.append([left] + [round(dot(centroids[left], centroids[right]), 8)
                              if centroids[left] and centroids[right] else ""
                              for right in names])
    return {"description": "Descriptive lexical similarity; not semantic basin identification or an inferential test.",
            "tail_selection": "Last 20 completed hops per stream, then exclude invalid/unverified passages; never backfill.",
            "representation": "Only parsed text fields; the rule and other JSON fields are excluded.",
            "tokenization": "ASCII [a-z]+(?:'[a-z]+)?, lowercased, minimum length 2; no stemming.",
            "stopwords": sorted(STOPWORDS),
            "weighting": "Raw term count times log((1+N)/(1+df))+1; L2-normalized per passage.",
            "centroid": "L2-normalized sum of nonzero passage vectors per stream; cosine matrix in CSV.",
            "corpus_passages_including_zero_vectors": n,
            "vocabulary_size": len(df), "zero_token_documents": zero_documents,
            "empty_centroid_policy": "CSV cell blank if either stream has no nonzero passage vectors."}, rows


def audit(root):
    root = Path(root)
    config = json.loads((root / "protocol.json").read_text(encoding="utf-8"))
    errors, read_issues, warnings = [], [], []

    def issue(code, path, **details):
        errors.append({"code": code, "path": str(Path(path).relative_to(root)), **details})

    def read(path):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            read_issues.append({"path": str(path.relative_to(root)), "type": type(exc).__name__,
                                "note": "Could be an in-progress write during a live run; rerun after completion."})
            return None

    def same(actual, expected, code, path):
        if actual != expected:
            issue(code, path)

    def money(actual, expected, code, path):
        if actual is None or expected is None:
            same(actual, expected, code, path)
        elif not isinstance(actual, (int, float)) or abs(actual - expected) > 1e-8:
            issue(code, path, actual=actual, expected=expected)

    started_path = root / "run_started.json"
    started = read(started_path) if started_path.exists() else None
    if started:
        same(started.get("protocol_sha256"), sha((root / "protocol.json").read_text(encoding="utf-8")),
             "protocol_hash_mismatch", started_path)
        if (root / "run.py").exists():
            same(started.get("runner_sha256"), sha((root / "run.py").read_text(encoding="utf-8")),
                 "runner_hash_mismatch", started_path)
    models = {m["id"]: m for m in config["models"]}
    seeds = {s["id"]: s for s in config["seeds"]}
    files = list((root / "raw").glob("*/*/*.request.json"))
    files += list((root / "raw").glob("*/*/*.response.json"))
    indexed = defaultdict(dict)
    for path in files:
        model_id, seed_id = path.parent.parent.name, path.parent.name
        match = re.fullmatch(r"(\d+)\.(request|response)\.json", path.name)
        if model_id not in models or seed_id not in seeds or not match:
            issue("unexpected_record_path", path)
            continue
        hop, kind = int(match[1]), match[2]
        if path.name != f"{hop:03d}.{kind}.json" or not 1 <= hop <= config["hops"]:
            issue("invalid_hop_filename", path)
        indexed[(model_id, seed_id)].setdefault(hop, {})[kind] = path

    streams, documents = {}, []
    totals = Counter()
    for model_id, model in models.items():
        model_summary_path = root / "raw" / model_id / "summary.json"
        model_summary = read(model_summary_path) if model_summary_path.exists() else None
        if model_summary:
            same(model_summary.get("model"), model_id, "model_summary_id_mismatch", model_summary_path)
        for seed_id, seed in seeds.items():
            key = model_id + "/" + seed_id
            state = json.dumps({"rule": config["rule"], "text": seed["text"]})
            expected_hop, terminated = 1, False
            completed, eligible, invalid, pending, receipt_errors = [], [], [], [], []
            latency, costs, returned_models, statuses = [], [], set(), Counter()
            count = Counter()
            uncertain, pending_reserve = 0.0, 0.0
            for hop, paths in sorted(indexed[(model_id, seed_id)].items()):
                # A counterpart may have appeared between directory snapshots.
                base = root / "raw" / model_id / seed_id / f"{hop:03d}"
                for kind in ("request", "response"):
                    counterpart = base.with_suffix(f".{kind}.json")
                    if kind not in paths and counterpart.exists():
                        paths[kind] = counterpart
                req_path, res_path = paths.get("request"), paths.get("response")
                before = len(errors)
                req = read(req_path) if req_path else None
                res = read(res_path) if res_path else None
                if req_path:
                    count["attempts"] += 1
                if res_path:
                    count["response_files"] += 1
                if not req_path:
                    issue("response_without_request", res_path)
                if req:
                    for name, expected in (("model", model_id), ("seed", seed_id), ("hop", hop)):
                        same(req.get(name), expected, "request_" + name + "_mismatch", req_path)
                    if hop != expected_hop:
                        issue("nonconsecutive_request_hop", req_path, expected=expected_hop, actual=hop)
                    if terminated:
                        issue("request_after_stream_stopped", req_path)
                    body = req.get("body", {})
                    messages = body.get("messages", [])
                    actual_state = messages[0].get("content") if messages and isinstance(messages[0], dict) else None
                    same(actual_state, state, "chain_state_mismatch", req_path)
                    same(body, expected_body(config, model, state), "request_body_or_settings_mismatch", req_path)
                    if isinstance(actual_state, str):
                        same(req.get("state_sha256"), sha(actual_state), "request_state_hash_mismatch", req_path)
                        reserve = ((len(actual_state.encode("utf-8")) + 512) * model["input_usd_per_million"]
                                   + config["max_output_tokens"] * model["output_usd_per_million"]) / 1e6
                        money(req.get("reserved_cost_usd"), reserve, "request_reserve_mismatch", req_path)
                    endpoint = ("https://api.openai.com/v1/chat/completions" if model["provider"] == "openai"
                                else "https://api.anthropic.com/v1/messages")
                    same(req.get("endpoint"), endpoint, "request_endpoint_mismatch", req_path)
                if res is None:
                    pending.append(hop)
                    count["pending_or_unreadable_receipts"] += 1
                    pending_reserve += (req or {}).get("reserved_cost_usd", 0) or 0
                    expected_hop = hop + 1
                    continue
                for name, expected in (("model", model_id), ("seed", seed_id), ("hop", hop)):
                    same(res.get(name), expected, "response_" + name + "_mismatch", res_path)
                count["receipts"] += 1
                status = res.get("stream_status")
                statuses[str(status)] += 1
                seconds = res.get("latency_seconds")
                if isinstance(seconds, (int, float)) and seconds >= 0:
                    latency.append(seconds)
                else:
                    issue("invalid_latency", res_path)
                reported_cost = res.get("usage_cost_upper_estimate_usd")
                if isinstance(reported_cost, (int, float)) and reported_cost >= 0:
                    costs.append(reported_cost)
                elif reported_cost is None:
                    uncertain += (req or {}).get("reserved_cost_usd", 0) or 0
                else:
                    issue("invalid_reported_cost", res_path)
                raw, output, finish, refusal, computed_cost = None, None, None, None, None
                unpack_error = None
                if "response_body" in res:
                    try:
                        raw = json.loads(res["response_body"])
                        computed_cost = price(model, raw)
                        output, finish, refusal = unpack(model["provider"], raw)
                        if not isinstance(output, str):
                            raise TypeError("visible output is not a string")
                    except (ValueError, TypeError, KeyError, IndexError) as exc:
                        unpack_error = type(exc).__name__
                if raw is not None:
                    money(reported_cost, computed_cost, "usage_cost_mismatch", res_path)
                if output is not None:
                    same(res.get("output"), output, "receipt_output_mismatch", res_path)
                    same(res.get("output_sha256"), sha(output), "receipt_output_hash_mismatch", res_path)
                    same(res.get("finish_reason"), finish, "receipt_finish_mismatch", res_path)
                    same(res.get("refusal"), refusal, "receipt_refusal_mismatch", res_path)
                    same(res.get("returned_model"), raw.get("model"), "receipt_returned_model_mismatch", res_path)
                    same(res.get("usage"), raw.get("usage"), "receipt_usage_mismatch", res_path)
                    returned_models.add(str(raw.get("model")))
                    passage, info, reasons = passage_info(output, config["rule"])
                    same(res.get("format"), info, "receipt_format_mismatch", res_path)
                    inferred_status = ("missing_usage" if computed_cost is None else "empty_output" if not output
                                       else "abnormal_finish:" + str(finish) if finish not in ("stop", "end_turn")
                                       else "active")
                    if "error_type" not in res:
                        same(status, inferred_status, "receipt_status_mismatch", res_path)
                elif "error_type" not in res:
                    issue("receipt_without_output_or_error", res_path)
                completed_ok = (output is not None and bool(output) and computed_cost is not None
                                and finish in ("stop", "end_turn") and "error_type" not in res)
                if completed_ok:
                    count["completed_hops"] += 1
                    completed.append({"hop": hop, "passage": passage, "exclusions": list(reasons)})
                    if passage is not None:
                        count["completed_string_passages"] += 1
                    if not reasons:
                        count["valid_passages"] += 1
                    if req is None or len(errors) != before:
                        completed[-1]["exclusions"].append("integrity_error_or_unreadable_request")
                    else:
                        count["verified_completed_hops"] += 1
                    if not completed[-1]["exclusions"]:
                        eligible.append((hop, passage))
                        count["verified_valid_passages"] += 1
                    else:
                        invalid.append({"hop": hop, "reasons": completed[-1]["exclusions"]})
                    state = output
                else:
                    terminated = True
                    count["noncompleted_receipts"] += 1
                    failure = {"hop": hop, "status": status, "error_type": res.get("error_type"),
                               "http_status": res.get("http_status"), "finish_reason": finish,
                               "raw_unpack_error": unpack_error}
                    receipt_errors.append(failure)
                if finish in ("length", "max_tokens"):
                    count["truncations"] += 1
                if refusal:
                    count["refusals"] += 1
                if res.get("error_type"):
                    count["errors"] += 1
                if computed_cost is None:
                    count["receipts_without_known_usage_cost"] += 1
                expected_hop = hop + 1
            tail = completed[-TAIL_SIZE:]
            included = [item for item in tail if not item["exclusions"]]
            documents.extend((key, item["hop"], item["passage"]) for item in included)
            terminal_summary = (model_summary or {}).get("streams", {}).get(seed_id)
            if terminal_summary:
                same(terminal_summary.get("completed_hops"), count["completed_hops"],
                     "summary_completed_hops_mismatch", model_summary_path)
                money(terminal_summary.get("cost_usd"), sum(costs), "summary_cost_mismatch", model_summary_path)
                if terminal_summary.get("status") == "hop_limit" and count["completed_hops"] != config["hops"]:
                    issue("premature_hop_limit_summary", model_summary_path, seed=seed_id)
            for counter in ("attempts", "receipts", "response_files", "completed_hops", "verified_completed_hops",
                            "valid_passages", "verified_valid_passages", "completed_string_passages", "errors",
                            "truncations", "refusals", "pending_or_unreadable_receipts", "noncompleted_receipts",
                            "receipts_without_known_usage_cost"):
                count[counter] += 0
            streams[key] = {"model": model_id, "seed": seed_id, "counts": dict(count),
                            "summary_status": terminal_summary.get("status") if terminal_summary else None,
                            "receipt_status_counts": dict(statuses), "returned_models": sorted(returned_models),
                            "pending_hops": pending, "noncompleted_receipts": receipt_errors,
                            "excluded_completed_passages": invalid,
                            "passage_metric_population": "Verified completed passages with an unchanged rule and nonempty string text.",
                            "exact_recurrence": recurrence(eligible, lambda s: s),
                            "case_whitespace_normalized_recurrence": recurrence(eligible, normalized),
                            "passage_word_lengths": summary([len(s.split()) for _, s in eligible]),
                            "latency_seconds_all_receipts": summary(latency),
                            "usage_cost_upper_estimate_usd": sum(costs),
                            "uncertain_cost_reserve_usd": uncertain,
                            "pending_cost_reserve_usd": pending_reserve,
                            "lexical_tail": {"selected_completed_hops": [item["hop"] for item in tail],
                                             "included_hops": [item["hop"] for item in included],
                                             "excluded_hops": [{"hop": item["hop"], "reasons": item["exclusions"]}
                                                               for item in tail if item["exclusions"]]}}
            totals.update(count)
    lexical_metrics, rows = lexical(documents, streams)
    cost_total = sum(s["usage_cost_upper_estimate_usd"] for s in streams.values())
    uncertain_total = sum(s["uncertain_cost_reserve_usd"] for s in streams.values())
    pending_total = sum(s["pending_cost_reserve_usd"] for s in streams.values())
    finished_path = root / "run_finished.json"
    finished = read(finished_path) if finished_path.exists() else None
    if finished:
        budget = finished.get("budget", {})
        money(budget.get("usage_cost_upper_estimate_usd"), cost_total, "final_cost_mismatch", finished_path)
        money(budget.get("uncertain_cost_reserve_usd"), uncertain_total, "final_uncertain_reserve_mismatch", finished_path)
        money(budget.get("in_flight_reserve_usd"), pending_total, "final_in_flight_reserve_mismatch", finished_path)
        money(budget.get("limit_usd"), config["budget_usd"], "final_budget_limit_mismatch", finished_path)
        if totals["pending_or_unreadable_receipts"]:
            issue("finished_run_has_pending_receipts", finished_path)
    if cost_total + uncertain_total + pending_total > config["budget_usd"] + 1e-6:
        issue("accounted_budget_exceeds_limit", root / "protocol.json")
    if not finished:
        warnings.append("Live or interrupted snapshot: absence of run_finished.json does not establish a failure.")
    if read_issues:
        warnings.append("Unreadable files prevent a clean audit; rerun after generation finishes.")
    metrics = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
               "audit_version": 1, "run_finished_receipt_present": finished is not None,
               "observation_status": ("Finalized run receipt present." if finished else
                                      "Unfinished/censored snapshot: generation may be live or interrupted."),
               "audit_clean_for_readable_snapshot": not errors and not read_issues,
               "errors": errors, "read_issues": read_issues, "warnings": warnings,
               "definitions": {"attempts": "Request files, including pending or unreadable requests.",
                               "completed_hops": "Nonempty visible output, normal finish, known usage cost, no recorded exception; format may be invalid.",
                               "valid_passages": "Completed hops whose parsed JSON has the original rule and nonempty string text.",
                               "verified": "No per-request or receipt integrity error and request is readable.",
                               "pending": "Request without a readable response receipt: outcome and billing unresolved; not classified as an API failure.",
                               "latency": "All readable response receipts, including failures; excludes pending requests.",
                               "cost": "Runner's conservative usage estimate, independently recomputed; not a provider invoice."},
               "totals": {**dict(totals), "usage_cost_upper_estimate_usd": cost_total,
                          "uncertain_cost_reserve_usd": uncertain_total, "pending_cost_reserve_usd": pending_total,
                          "budget_limit_usd": config["budget_usd"]},
               "streams": streams, "lexical": lexical_metrics}
    return metrics, rows


def write_analysis(root, metrics, rows):
    output = Path(root) / "analysis"
    output.mkdir(parents=True, exist_ok=True)
    for name, content in (("metrics.json", json.dumps(metrics, ensure_ascii=False, indent=2) + "\n"),
                          ("lexical_similarity.csv", csv_text(rows))):
        temp = output / (name + ".tmp")
        temp.write_text(content, encoding="utf-8", newline="")
        temp.replace(output / name)


def csv_text(rows):
    target = io.StringIO(newline="")
    csv.writer(target).writerows(rows)
    return target.getvalue()


def self_test():
    """Temporary synthetic fixtures only; no real passages or API calls."""
    def put(path, obj):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj), encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="basin-audit-test-") as directory:
        root = Path(directory)
        config = {"rule": "Shared rule tokens must never inflate passage similarity.",
                  "seeds": [{"id": "a", "text": "start"}, {"id": "b", "text": "start"}],
                  "models": [{"id": "test", "provider": "openai", "input_usd_per_million": 2,
                              "output_usd_per_million": 10}], "hops": 30, "max_output_tokens": 100,
                  "reasoning_effort": "low", "budget_usd": 20}
        model = config["models"][0]
        put(root / "protocol.json", config)

        def fixture(seed, hop, state, output=None, failure=False):
            base = root / "raw" / "test" / seed / f"{hop:03d}"
            reserve = ((len(state.encode()) + 512) * 2 + 100 * 10) / 1e6
            req = {"model": "test", "seed": seed, "hop": hop,
                   "body": expected_body(config, model, state), "state_sha256": sha(state),
                   "reserved_cost_usd": reserve, "endpoint": "https://api.openai.com/v1/chat/completions"}
            put(base.with_suffix(".request.json"), req)
            if output is None and not failure:
                return
            res = {"model": "test", "seed": seed, "hop": hop, "latency_seconds": 1.0}
            if failure:
                res.update(error_type="HTTPError", http_status=429, stream_status="http_error:429",
                           usage_cost_upper_estimate_usd=None)
            else:
                raw = {"model": "test", "choices": [{"message": {"content": output}, "finish_reason": "stop"}],
                       "usage": {"prompt_tokens": 10, "completion_tokens": 20}}
                res.update(response_body=json.dumps(raw), output=output, output_sha256=sha(output),
                           finish_reason="stop", refusal=None, returned_model="test", usage=raw["usage"],
                           format=passage_info(output, config["rule"])[1], stream_status="active",
                           usage_cost_upper_estimate_usd=price(model, raw))
            put(base.with_suffix(".response.json"), res)

        initial = json.dumps({"rule": config["rule"], "text": "start"})
        apple = json.dumps({"rule": config["rule"], "text": "apple carrot"})
        quartz = json.dumps({"rule": config["rule"], "text": "quartz zircon"})
        fixture("a", 1, initial, apple)
        fixture("b", 1, initial, quartz)
        metrics, rows = audit(root)
        assert metrics["audit_clean_for_readable_snapshot"], metrics["errors"]
        assert rows[1][2] == 0, "Repeated JSON rule contaminated the lexical vectors"
        assert metrics["lexical"]["vocabulary_size"] == 4
        fixture("a", 2, initial, apple)
        metrics, _ = audit(root)
        assert any(e["code"] == "chain_state_mismatch" for e in metrics["errors"])
        fixture("a", 2, apple, apple)
        fixture("a", 3, apple, failure=True)
        fixture("b", 2, quartz)
        metrics, _ = audit(root)
        assert metrics["audit_clean_for_readable_snapshot"], metrics["errors"]
        assert metrics["totals"]["attempts"] == 5
        assert metrics["totals"]["receipts"] == 4
        assert metrics["totals"]["completed_hops"] == 3
        assert metrics["totals"]["valid_passages"] == 3
        assert metrics["totals"]["errors"] == 1
        assert metrics["totals"]["pending_or_unreadable_receipts"] == 1
        assert math.isclose(metrics["totals"]["usage_cost_upper_estimate_usd"], 3 * 0.00022)
        assert metrics["totals"]["uncertain_cost_reserve_usd"] > 0
        assert metrics["totals"]["pending_cost_reserve_usd"] > 0
        assert metrics["streams"]["test/a"]["exact_recurrence"]["repeated_occurrences_after_first"] == 1
        # Replace pending b2, then add 20 completed hops including one invalid
        # JSON output. Selection must remain the final 20, with no backfill.
        state = quartz
        for hop in range(2, 23):
            output = "malformed" if hop == 4 else quartz
            fixture("b", hop, state, output)
            state = output
        metrics, rows = audit(root)
        tail = metrics["streams"]["test/b"]["lexical_tail"]
        assert metrics["audit_clean_for_readable_snapshot"], metrics["errors"]
        assert tail["selected_completed_hops"] == list(range(3, 23))
        assert tail["included_hops"] == [h for h in range(3, 23) if h != 4]
        assert tail["excluded_hops"] == [{"hop": 4, "reasons": ["invalid_json"]}]
        assert metrics["totals"]["completed_hops"] == metrics["totals"]["valid_passages"] + 1
        assert normalized("Apple  CARROT\n") == normalized("apple carrot")
        assert passage_info("```json\n" + quartz + "\n```", config["rule"])[2] == ["invalid_json"]
        assert passage_info('{"rule": "x", "text": "literal\nnewline"}', config["rule"])[2] == ["invalid_json"]
        anthropic_model = {"provider": "anthropic", "input_usd_per_million": 4,
                           "output_usd_per_million": 20}
        anthropic_raw = {"content": [{"type": "thinking", "thinking": "not visible"},
                                     {"type": "text", "text": "first"},
                                     {"type": "text", "text": "second"}],
                         "stop_reason": "end_turn",
                         "usage": {"input_tokens": 10, "output_tokens": 20,
                                   "cache_read_input_tokens": 5, "cache_creation_input_tokens": 3}}
        assert unpack("anthropic", anthropic_raw) == ("firstsecond", "end_turn", None)
        assert math.isclose(price(anthropic_model, anthropic_raw), 0.000484)
        # Receipt/body corruption must be caught independently of the stored hash.
        path = root / "raw" / "test" / "b" / "022.response.json"
        receipt = json.loads(path.read_text())
        receipt["output"] = "different"
        receipt["output_sha256"] = sha("different")
        put(path, receipt)
        metrics, rows = audit(root)
        assert any(e["code"] == "receipt_output_mismatch" for e in metrics["errors"])
        write_analysis(root, metrics, rows)
        assert json.loads((root / "analysis" / "metrics.json").read_text())["errors"]
    print("Synthetic tests passed: clean chain, chain mismatch, rule-only exclusion, receipts, accounting, recurrence, tail selection, output corruption, strict formatting, Anthropic text and cache accounting.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    metrics, rows = audit(args.root)
    write_analysis(args.root, metrics, rows)
    print(json.dumps({"audit_clean_for_readable_snapshot": metrics["audit_clean_for_readable_snapshot"],
                      "run_finished_receipt_present": metrics["run_finished_receipt_present"],
                      "integrity_errors": len(metrics["errors"]), "read_issues": len(metrics["read_issues"]),
                      "totals": metrics["totals"]}, indent=2))


if __name__ == "__main__":
    main()
