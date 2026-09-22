"""Bounded, raw-recording memoryless API loops. Standard library only.

Each model has one worker; its three independent streams are interleaved by hop.
No response or model identity is transferred between streams. Keys are never logged.
"""
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "protocol.json").read_text(encoding="utf-8"))
PRINT_LOCK = threading.Lock()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())


def emit(data):
    with PRINT_LOCK:
        print(json.dumps(data, ensure_ascii=True), flush=True)


class Budget:
    def __init__(self, limit):
        self.limit = limit
        self.used = 0.0
        self.reserved = 0.0
        self.uncertain = 0.0
        self.lock = threading.Lock()

    def reserve(self, amount):
        with self.lock:
            if self.used + self.reserved + self.uncertain + amount > self.limit:
                return False
            self.reserved += amount
            return True

    def settle(self, reserved, cost):
        with self.lock:
            self.reserved -= reserved
            if cost is None:
                self.uncertain += reserved
            else:
                self.used += cost
            return self.snapshot_unlocked()

    def snapshot_unlocked(self):
        return dict(usage_cost_upper_estimate_usd=round(self.used, 8),
                    uncertain_cost_reserve_usd=round(self.uncertain, 8),
                    in_flight_reserve_usd=round(self.reserved, 8),
                    limit_usd=self.limit)

    def snapshot(self):
        with self.lock:
            return self.snapshot_unlocked()


def request_body(model, state):
    body = {"model": model["id"], "messages": [{"role": "user", "content": state}]}
    if model["provider"] == "openai":
        body.update(max_completion_tokens=CONFIG["max_output_tokens"], reasoning_effort="low")
    else:
        body.update(max_tokens=CONFIG["max_output_tokens"], output_config={"effort": "low"})
    return body


def unpack(model, response):
    if model["provider"] == "openai":
        choice = response["choices"][0]
        content = choice["message"].get("content") or ""
        return content, choice["finish_reason"], choice["message"].get("refusal")
    content = "".join(b["text"] for b in response["content"] if b["type"] == "text")
    return content, response["stop_reason"], None


def usage_cost(model, response):
    usage = response.get("usage", {})
    if model["provider"] == "openai":
        if "prompt_tokens" not in usage or "completion_tokens" not in usage:
            return None
        inp, out = usage["prompt_tokens"], usage["completion_tokens"]
    else:
        if "input_tokens" not in usage or "output_tokens" not in usage:
            return None
        # Conservative: charge cache reads at full input price, writes at 2x.
        inp = (usage["input_tokens"] + usage.get("cache_read_input_tokens", 0)
               + 2 * usage.get("cache_creation_input_tokens", 0))
        out = usage["output_tokens"]
    return (inp * model["input_usd_per_million"] + out * model["output_usd_per_million"]) / 1e6


def analyze_output(text):
    try:
        obj = json.loads(text)
        if not isinstance(obj, dict):
            return {"json_object": False, "rule_unchanged": False}
        passage = obj.get("text")
        return {"json_object": True, "rule_unchanged": obj.get("rule") == CONFIG["rule"],
                "passage_is_string": isinstance(passage, str),
                "passage_sha256": digest(passage) if isinstance(passage, str) else None,
                "passage_words": len(passage.split()) if isinstance(passage, str) else None}
    except (ValueError, TypeError):
        return {"json_object": False, "rule_unchanged": False}


def model_worker(model, budget):
    provider = model["provider"]
    if provider == "openai":
        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
    else:
        endpoint = "https://api.anthropic.com/v1/messages"
        headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                   "anthropic-workspace-id": os.environ.get("ANTHROPIC_WORKSPACE_ID") or CONFIG["anthropic_workspace_id"]}
    headers["Content-Type"] = "application/json"
    streams = {s["id"]: {"state": json.dumps({"rule": CONFIG["rule"], "text": s["text"]}),
                            "completed_hops": 0, "status": "active", "cost_usd": 0.0}
               for s in CONFIG["seeds"]}
    for hop in range(1, CONFIG["hops"] + 1):
        if all(s["status"] != "active" for s in streams.values()):
            break
        for seed_id, stream in streams.items():
            if stream["status"] != "active":
                continue
            if (ROOT / "PAUSE").exists():
                stream["status"] = "paused_before_request"
                continue
            state = stream["state"]
            body = request_body(model, state)
            # Bytes provide a conservative input-token allowance; overhead allows framing.
            reserve = ((len(state.encode("utf-8")) + 512) * model["input_usd_per_million"]
                       + CONFIG["max_output_tokens"] * model["output_usd_per_million"]) / 1e6
            if not budget.reserve(reserve):
                stream["status"] = "budget_stop"
                emit({"model": model["id"], "seed": seed_id, "status": "budget_stop", "hop": hop})
                continue
            stem = ROOT / "raw" / model["id"] / seed_id / f"{hop:03d}"
            request = {"started_at": now(), "model": model["id"], "seed": seed_id, "hop": hop,
                       "endpoint": endpoint, "body": body, "state_sha256": digest(state),
                       "reserved_cost_usd": reserve}
            save(stem.with_suffix(".request.json"), request)
            start = time.monotonic()
            record = {"model": model["id"], "seed": seed_id, "hop": hop}
            cost = None
            output = ""
            try:
                req = urllib.request.Request(endpoint, data=json.dumps(body).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=CONFIG["request_timeout_seconds"]) as reply:
                    raw = reply.read().decode("utf-8")
                    record.update(http_status=reply.status, response_body=raw,
                                  response_headers={k: v for k, v in reply.headers.items()
                                                    if k.lower() in {"request-id", "x-request-id", "date", "openai-processing-ms"}})
                response = json.loads(raw)
                cost = usage_cost(model, response)
                output, finish, refusal = unpack(model, response)
                record.update(output=output, output_sha256=digest(output), finish_reason=finish,
                              refusal=refusal, returned_model=response.get("model"), usage=response.get("usage"),
                              format=analyze_output(output))
                if cost is None:
                    stream["status"] = "missing_usage"
                elif not output:
                    stream["status"] = "empty_output"
                elif finish not in ("stop", "end_turn"):
                    stream["status"] = "abnormal_finish:" + str(finish)
                else:
                    stream["state"] = output
                    stream["completed_hops"] += 1
                    # Malformed JSON / changed rules are outcomes: feed exact text onward.
            except urllib.error.HTTPError as error:
                record.update(http_status=error.code, error_body=error.read().decode("utf-8", errors="replace"),
                              error_type=type(error).__name__)
                stream["status"] = "http_error:" + str(error.code)
            except Exception as error:
                record.update(error_type=type(error).__name__, error_message=str(error))
                stream["status"] = "transport_or_parse_error"
            record.update(finished_at=now(), latency_seconds=round(time.monotonic() - start, 4),
                          usage_cost_upper_estimate_usd=cost, stream_status=stream["status"],
                          budget=budget.settle(reserve, cost))
            if cost is not None:
                stream["cost_usd"] += cost
            save(stem.with_suffix(".response.json"), record)
            if hop == 1 or hop % 5 == 0 or stream["status"] != "active":
                emit({"model": model["id"], "seed": seed_id, "hop": hop,
                      "status": stream["status"], "latency_s": record["latency_seconds"],
                      "words": record.get("format", {}).get("passage_words"), "budget": budget.snapshot()})
    summary = {"model": model["id"], "finished_at": now(),
               "streams": {k: {a: b for a, b in v.items() if a != "state"} for k, v in streams.items()}}
    for s in summary["streams"].values():
        if s["status"] == "active":
            s["status"] = "hop_limit"
    save(ROOT / "raw" / model["id"] / "summary.json", summary)
    return summary


def main():
    # Never overwrite or silently resume an interrupted trajectory.
    if (ROOT / "run_started.json").exists():
        raise SystemExit("Run already started; inspect raw evidence before an explicit recovery.")
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if not os.environ.get(key):
            raise SystemExit("Missing environment key: " + key)
    save(ROOT / "run_started.json", {"started_at": now(), "protocol_sha256": digest((ROOT / "protocol.json").read_text()),
                                    "runner_sha256": digest(Path(__file__).read_text()),
                                    "concurrency": "one model, one fresh independent sunset stream"})
    budget = Budget(CONFIG["budget_usd"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(model_worker, m, budget) for m in CONFIG["models"]]
        results = [f.result() for f in futures]
    result = {"finished_at": now(), "budget": budget.snapshot(), "models": results}
    save(ROOT / "run_finished.json", result)
    emit({"finished": True, "budget": budget.snapshot()})


if __name__ == "__main__":
    main()
