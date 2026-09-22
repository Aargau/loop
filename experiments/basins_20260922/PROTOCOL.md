# New-model basin comparison, 22 September 2026

Written before generation. Authorized by Justin Bronder to compare newer model basins before cross-model ingestion. All model streams remain independent.

Question: under the original `json_page` memoryless replacement operator, which semantic regions recur within a model, across independent repetitions, and across model families? Does replacing the tide seed with a bicycle seed change those regions?

Prediction: distinct wording will persist more often than exact copying; recurring narrative motifs and registers will remain narrower than their surface wording suggests. Tide may induce coastal settings initially. Late cross-seed overlap would support a seed-robust behavioral tendency under this operator; sustained divergence would count against that hypothesis.

Interpretation: this is an exploratory sample of trajectories, not an estimate of basin volumes, proof of internal attractors, or a model ranking. Similar `low` effort labels do not match reasoning compute. Shared training, alignment, decoding, and the replacement instruction remain possible causes. One bicycle stream per model is a sensitivity probe; two tide streams are the primary replicate comparison.

## Frozen design

Exact model IDs, seeds, rule, price assumptions, limits, and settings are in `protocol.json`. Each of five models gets two independent tide-seed streams and one bicycle-seed stream, each up to 60 hops. No extra system instruction, transcript, other-model output, evaluator feedback, or embeddings enter generation. Each next request contains only the preceding complete visible response as one user message. Provider-returned reasoning blocks stay in raw evidence and are not carried forward.

There is one worker per model, interleaving its three seeds in fixed order by hop. Sampling parameters are omitted. OpenAI receives `reasoning_effort: low`; Anthropic receives `output_config.effort: low`, with its default adaptive thinking. The 4096-token output allowance includes provider-counted reasoning. JSON formatting is requested by the carried rule, not forced through an API schema. No automatic retries or early cycle stop. A malformed response or altered rule is recorded and fed onward unchanged. Empty output, non-normal finish, missing usage, or an API error stops only its stream. No hidden recovery or restart is permitted.

The shared $20 stopping budget conservatively charges reported input/output tokens at uncached standard rates. Reservations cover each pending maximum output and an input allowance based on UTF-8 bytes plus framing. Unknown billing following an error retains the entire reservation. This is a usage-based local stopping mechanism, not a provider billing guarantee. A budget stop can leave unequal model depths; comparisons must use common windows and disclose censoring. The run refuses to overwrite previous evidence.

## Evidence and assessment

Save each exact request body before sending and each complete raw response body afterward, along with returned model ID, request ID where available, usage, latency, stop reason, hashes, and errors. Authentication headers are excluded. Capture the existing locally modified `C:\ai\loop\loop.py` as a source snapshot; the new runner preserves its replacement semantics while adding full raw responses, explicit Anthropic effort, and bounded cost accounting. Source checkout commit: `b9f5a12d572951eecefac6779e4eedd22d7339d5`. Existing uncommitted work remains in that checkout.

Offline assessment must analyze the `text` passage separately from the repeated rule. Report exact and whitespace/case-normalized recurrence; rule and format survival; output-limit hits and other failures; word counts and timing; passage-only lexical similarity; and human/model qualitative coding with exact hop citations. Inspect first, middle, and late windows plus disconfirming passages. Distinguish same-world story continuation, plot templates, shared motifs, and generic prose register. Lexical overlap and model-generated labels are proxies, not ground truth for semantic basins. No inferential p-values from 15 dependent trajectories.

## Access and pricing sources

Read-only model catalog calls confirmed all five IDs using existing keys. The first sandboxed catalog calls hit Windows socket error 10013; authorized network calls succeeded. Anthropic requires the existing project's workspace header. No generation had occurred when this protocol was written.

- https://openai.com/index/introducing-gpt-6-sol-and-luna/
- https://developers.openai.com/api/docs/models/gpt-6-sol
- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://platform.claude.com/docs/en/models/fable-5-1/overview
- https://platform.claude.com/docs/en/models/opus-5-5/overview
- https://platform.claude.com/docs/en/build-with-claude/effort

Prices are assumptions verified from official documentation on the run date. Final estimated cost is not an invoice, and discounts can reduce it.
