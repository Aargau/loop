# Sunset-seeded model basin comparison, 22 September 2026

Frozen before this run's generation. Supersedes the interrupted bicycle pilot as the primary comparison. Justin identified the bicycle seed as domestic and supplied the exact broader seed: **The sun was setting behind the hills.** His rationale was to keep world building, domestic, and fantastical possibilities open. We accepted that correction rather than treating an ordinary object as a neutral starting condition.

Question: do newer models enter similar or distinct semantic regions when repeatedly applying the same memoryless replacement rule to a broadly specified setting? Do repeated sunset streams agree with one another, and does the original tide seed reach similar regions?

Prediction: distinct wording may coexist with recurring narrative motifs and registers. Strong differences between sunset replicates would count against treating a single trajectory as a model-specific basin. Shared late motifs across independent seeds would be suggestive of seed-robust tendencies under this operator; sustained seed-dependent divergence would be disconfirming. These predictions precede this run, but the analyst has seen format, word-count and cost metadata plus short first-hop fragments from the earlier pilot. This is not a fully blind preregistration.

Interpretation: exploratory behavioral trajectories under one prose-generation operator. The sentence is broader than the bicycle seed but still contains a familiar narrative setting, time of day, and landscape. The carried instruction asks for a passage, so the instrument itself can favor narrative prose. We do not estimate basin volumes, identify internal activations, prove inherent attractors, or isolate architecture/training effects.

## Design and changes from pilot

- Five models: `gpt-6-luna`, `gpt-6-sol`, `gpt-6-astra`, `claude-fable-5-1`, `claude-opus-5-5`.
- Two independent streams begin with `The sun was setting behind the hills.` One comparison stream begins with `The tide came in an hour early.` All are fresh streams; no pilot output or output from another model is ingested.
- Each stream runs up to 60 hops. Each request is a single user message containing the entire preceding visible response. There is no accumulated transcript or extra system prompt. Rule: `Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.`
- `reasoning_effort: low` for OpenAI, `output_config.effort: low` and default adaptive thinking for Anthropic. These are provider-specific controls, not equal-compute settings. Sampling parameters omitted. Output allowance 4096 tokens including provider-counted reasoning. No forced JSON schema, retries, cycle stops, or evaluator interventions.
- One worker per model, interleaving its streams in fixed order. Malformed JSON/changed rule is retained and fed onward unchanged. Empty output, missing usage, non-normal finish (including truncation), or API error stops that stream. Such stops censor the trajectory.
- New convenience control: creating a file named `PAUSE` in this directory stops new requests once each in-flight request completes and is saved. No automatic restart. This avoids losing responses during another user-requested pause.
- The shared initial $20 budget is retained. The pilot saved 60 responses costing an estimated $0.5680635 at uncached standard rates; five interrupted requests have unknown remote outcomes and a conservative $0.5931796 billing reservation. This fresh run therefore has an $18.83 limit, leaving the overall reserved total below $20. Price assumptions are in `protocol.json` and sources in the pilot protocol. Budget censoring can produce unequal depths; compare common horizons.

## Evidence and analysis

The runner retains exact request bodies, complete raw response bodies, visible output, hashes, returned model identifiers, provider request IDs where available, token usage, latency, and errors. No keys or authorization headers are logged. The prior source-loop snapshot and protocol are in `../basins_20260922/`; raw pilot data and `PAUSED.json` remain separate.

Audit exact chains before interpretation. Analyze story text separately from the repeating rule. Report strict JSON/unchanged-rule rates independently from semantic extraction. Pilot format observation: some models wrap JSON in Markdown fences or emit literal newlines inside strings. Any tolerant offline extraction must be explicitly labeled, preserve the original response, and never feed repaired text into generation. Invalid or uncertain extraction remains an exclusion, not a semantic finding.

Measure exact/normalized passage recurrence, passage lengths, lexical overlap, failures, and representative semantic motifs/registers across early/middle/late windows. Use block or trajectory comparisons, not hops as independent replicates. Qualitative labels are fallible observations and require exact passage citations and counterexamples. No causal or statistical-significance claims from this small sample.
