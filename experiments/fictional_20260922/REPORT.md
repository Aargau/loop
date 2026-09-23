# Explicit fiction keeps the previous/next loops in narrative

Completed 22 September 2026, Pacific time. **All eight trajectories reached 40 steps: 320 requests, 320 normal responses, no provider refusals, no operational stops, and $3.5804102 in estimated usage.** Fable was excluded at Justin's request. Existing API keys worked.

The explicit-fiction wording supports the intended generation interpretation in this follow-up. Sustaining fiction still leaves substantial variation in temporal direction, character continuity and recurring themes. The most striking shared opening choice appears before any iteration: **all eight first passages introduce Mara**, although every first input contains only the name-free sunset seed and its rule.

## Design and comparison

Luna, Sol, Astra and Opus each received fresh previous and next trajectories from **The sun was setting behind the hills.** The new rule is:

> Return this JSON object with the rule field unchanged and, in the text field, an original fictional passage of about 250 words that comes immediately BEFORE the current text in the same invented story.

Next substitutes AFTER for BEFORE. The [frozen protocol](PROTOCOL.md) and [study manifest](study.json) retain the exact old/new wording, hashes and settings. Each cell has one trajectory. The previous rule also changes tense and makes the story reference symmetric with next; this tests the wording bundle across separate stochastic runs, not the isolated causal contribution of one word.

Everything else uses the tested runner: low effort, provider-default sampling, 4096 output-token cap, no added system message, and only the entire preceding visible response as the next input. No cumulative transcript or cross-model ingestion. Two separate $5 arm caps include uncertain-billing and in-flight reservations. Earlier spending remains separate. No retries, replacements, schema enforcement, rule repairs or early stopping on repeats occurred.

## What changed about objections

An independent reading of all **309 normal outputs** from the four matching models' earlier literal previous/next runs found **160 source-objection-only responses**, **five objections that also supplied fiction**, **one neutral originality note with fiction**, **115 fiction-only responses**, and **28 other conversational responses**. These are dependent steps in eight trajectories, not independent trials or model-level refusal rates. Opus previous's HTTP 500 is separate censoring. Exact criteria, hop lists, exceptions and hashes are in the [baseline coding](analysis/LITERAL_OBJECTIONS.md).

The new runs have **zero raw provider refusal finishes**. No assistant-level source-retrieval objection was found by the [new-output screen](analysis/FICTION_OBJECTION_SCREEN.md), which searches every extracted passage, inspects every opening/closing and flagged context, and reads the 12 predetermined full samples per stream. This scope is narrower than a full manual reading of every word. Character dialogue and fiction about uncertain identity are distinguished from assistant objections to the task.

The change is especially clear for Sol previous and Astra in both directions: their earlier 40-step runs consisted entirely of direct source objections; their new sampled outputs sustain fictional scenes. Opus previous also retains the carried narrative instruction instead of entering the earlier conversation about roles and missing context. The [paired metrics](analysis/literal_wording_comparison.md) preserve the earlier outcomes unchanged.

## Shared openings, different trajectories

Both the parent and an independent auditor checked all eight first request bodies against their exact expected seed/rule message. None contains Mara, another stream's output or earlier-study text. All eight first extracted passages begin with Mara. Keys, letters, orchards, clocks and absent relatives recur across several openings. Opus previous begins with ordinary pear picking and a living grandfather, so an entirely supernatural or bereaved-opening description would be too broad.

This is evidence of shared starting preferences under these prompts. Establishing a basin requires more than the same initial name: it requires studying how different starting states evolve. The API records identify neither training causes nor internal model states.

| Model | Previous trajectory | Next trajectory |
| --- | --- | --- |
| **Luna** | Impossible station and grandmother's instructions recede into career decisions, an apprenticeship and childhood. The final five passages work backward through school, a library visit, a lost-card search and arriving home. | Clock-tower mystery develops into family remembrance and tending a seedling, then opens a new impossible garden and returning-grandmother thread. The late reopening counters a permanently absorbing consolation ending. |
| **Sol** | Magical orchard/well opening becomes house clearing, a hospital visit, repairs and delayed help for a mother. The late sequence retreats through April, March, winter, November and October. | A continuing supernatural quest uses doors, keys, doubles, counting rules and a bus. The final sequence reaches an apparent home, then reveals that the group brought home the wrong door. |
| **Astra** | Uncanny family return becomes restrained household, shop and bereavement scenes. The final five reverse a locally coherent sequence of personal belongings, hospital visits, collection and administration. | A returned brother and ferryman lead into domestic conversation, photographs and a key; later scenes center a boy, Anne, two fathers and unstable memories. Quiet domestic action becomes supernatural danger again. |
| **Opus** | Orchard inheritance expands into property history, widowhood and remembered courtship. There are clear late direction and chronology failures, despite fluent scenes. | Rural suspense evolves through threats and uncertain family identities into a temporary reunion with Gran. The final passage fulfills its limit: as the tea ends, her presence begins to disappear. |

Local continuity sometimes survives quite well. In Astra previous's last five passages, a comb requested in one antecedent is delivered incorrectly in the next, a cardigan is brought and later collected, and an instruction about a sticking lock precedes its use. Luna's late previous sequence similarly connects specific library and school events. Sol next's last five passages advance an ongoing journey rather than merely swapping scenery.

Global continuity is less secure. Opus previous hop 38 recounts a family's departure and a closed house; hop 39 jumps forward to the house reopening. Hop 40 provides an antecedent to 39 while changing earlier facts about Judge Hollis's death and Margaret's age. Its street changes from Alder to Linden. In other streams, ages, family roles and named protagonists drift. These observations qualify the outcome: explicit fiction removes a prominent ambiguity without ensuring a consistent story or correct temporal relation at every step.

The [attributed readings](analysis/QUALITATIVE_READINGS.md) retain hop references and counterexamples. The secondary reader used shuffled C-label packets; the parent had model-labelled evidence. This is partial masking. Apparent thematic concentration is descriptive, and departures from it remain visible.

## Verification and accounting

The [final independent verification](analysis/FINAL_VERIFICATION.md) reconciles the raw request chains, provider bodies, visible-output hashes, settings, stops and usage. All 320 outputs yield a passage and an unchanged rule under the documented extractor. Strict formatting differs: **186 bare strict JSON objects, 75 fenced strict objects, and 59 Luna objects requiring tolerant handling of literal control characters**. Extraction never repairs the input forwarded to a model. Therefore unchanged extracted rules do not imply universal strict-JSON compliance.

No exact or case/whitespace-normalized full-response or extracted-passage recurrence was found in these finite runs. That result does not rule out semantic concentration or later convergence. The [comparison table](analysis/comparison_table.md), [metrics](analysis/metrics.json), [recurrence record](analysis/repeating_runs.md), and full [previous](analysis/transcripts/previous/) / [next](analysis/transcripts/next/) transcripts preserve the distinctions.

| Model | Both directions, estimated usage |
| --- | ---: |
| Luna | $0.0235222 |
| Sol | $0.3918500 |
| Astra | $1.9552700 |
| Opus | $1.2097680 |
| **Total** | **$3.5804102** |

Previous cost $1.7617951 and next cost $1.8186151. Final uncertain and in-flight reserves are zero. These frozen-price usage estimates are not invoices. This study's clean operational completion and observed narrative behavior do not establish universal model traits, permanent basins or equal literary quality. There is one seed, one trajectory per cell, and sampling settings that do not equate compute across providers.

Rebuild the offline metrics and reading copies, without API calls, from the repository root with `python experiments/fictional_20260922/analyze.py`.
