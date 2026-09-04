# Causal BEFORE exploratory run, 2026-09-04

Astra proposed the operator; Justin authorized a Cerebras exploratory run while collaborating with Fable 5.1. No other run or shared harness was edited.

Question: does shifting causal focus extend BEFORE beyond the saved approximately 149-hop Cerebras transient? Prediction before launch: more character/setting movement, with repair/handoff templates a possible attractor.

## Observed result

300 generated passages, 300 distinct text fields and raw outputs, no exact or normalized recurrence reported by the harness. All 300 JSON objects parse and preserve the seed rule exactly. Every finish reason is stop; maximum output 627 tokens against a 1024-token limit. 135,761 output tokens, 138,709 input tokens. Summed request latency 510.43 seconds, approximately 266 output tokens per request-second; the configured one-second pacing is additional. Stop was the 300-hop budget, not convergence.

Backend cerebras; requested and returned model qwen-3.8-27b; T=0, top_p=1, seed=42, reasoning_effort=none, no system prompt, no embeddings. Initial text: The tide came in an hour early. Exact rule: init.json. Harness snapshot SHA256: 8711CB2F71D024207F721300854414320BEBCEE8066B413A8AB1EC1082D42F9F (copied during the run; shared harness was not modified by Astra).

## Interpretation from inspected passages

This extends observed non-repetition beyond the saved BEFORE result, but is not a controlled estimate of improvement: one seed/run, different output budget, and no contemporaneous baseline. Finite observed non-repetition does not establish an infinite trajectory or deterministic implementation.

Early passages alternate Elias and Mara and repeat maintenance situations. A rusted fire extinguisher appears in every passage from 24 through 67, often ignored at the end rather than selected for the next causal transition. Later passages move into office/HVAC, server maintenance, and warehouse logistics, with recurrent mugs, plants, paperwork, tools, and urgent practical problems. These observations come from selected passages and a substring check, not a complete semantic annotation.

At 215 the closet/lock account is spatially confused. At 300 the passage slips among network diagnosis, an electrical outlet, a conveyor belt, and a lobby. Thus text-level non-repetition coexists with strong template recurrence and inconsistent causal/spatial detail. The intended backward chain is not reliably maintained.

Candidate next test, unrun: require the final incidental object to become the next passage's focal object, and move to its previous owner or earlier use elsewhere. Current rule merely includes a detail and allows selection of any supporting detail, leaving a loophole for decorative repetition. This is a hypothesis, not a proven fix.

## Artifacts and access seam

cerebras_run/steps.jsonl is the complete successful raw trajectory; summary.json records arguments and terminal status. analyze.py independently checks text recurrence and JSON; analysis.json is the final result.

The first sandbox attempt in run/ failed before any model output with WinError 10013 (socket forbidden). The network-enabled attempt used a separate output directory and completed. Preserve the failed attempt as access evidence, not model behavior. No credentials are stored here.
