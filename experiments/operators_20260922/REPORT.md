# Four operators across five models

Completed 22 September 2026: **20 model/operator cells attempted, 15 complete 40-step trajectories, 642 completed responses overall.** All four arms have final receipts, with interruptions and partial outputs preserved.

The requested prompts expose several different behaviors: repeated stylistic revision, linguistic degradation, continuing fiction, and persistent requests for missing source text. The strongest clean contrast is between better and worse. Previous and next also change whether the models interpret the task as inventing fiction or retrieving an existing passage.

## Design

The same five models each received the exact sentence **The sun was setting behind the hills.** in four fresh streams. We used the repository's existing previous, next, worse and better rules without adding a criterion or clarification. Each stream targeted 40 steps. There was one replicate per model/operator cell, with $5 reserved per operator and a $20 ceiling for this new study.

Previous/next explicitly request adjacent passages of about 250 words. Better/worse impose no length and leave the evaluative criterion open. All other API settings and the raw-recording runner were copied from the earlier experiment: low effort, provider-default sampling, 4096 output tokens, and only the entire preceding visible response as the next input. There was no accumulated history or cross-model ingestion. See the frozen [protocol](PROTOCOL.md) and [exact rules/settings](study.json).

## Observed differences

| Model | Previous | Next | Better | Worse |
|---|---|---|---|---|
| Luna | Invented backstory gives way to requests for a source. | Fantasy develops into reconciliation; a late refusal is followed by a newly staged original scene. | One sunset sentence, gold/crimson and fire/ribbon variants. | Grammar collapses into pseudo-words while sun/hill/dark remnants survive. |
| Sol | Shortens to a repeated eleven-word request for the missing story. | Alternates fiction and objections; can turn an offer of original writing into the next fictional scene. | Short amber-sunset paraphrases. | Vagueness and contradiction progress into distorted word forms and punctuation. |
| Astra | Repeated objections to supplying an unprovided passage. | Repeated objections and creative offers, without sampled fiction. | Short sunset sentence shifts toward threading/stitching/weaving imagery. | Redundancy develops into structured imitation of corrupted data, with error labels, nulls and replacement characters. |
| Fable 5.1 | Provider refusal at the first request, no visible text. | Provider refusal at the first request, no visible text. | Expands from twelve words to a 131-word scene, with substantial retained text and occasional exact repetition. | Provider refusal at the first request, no visible text. |
| Opus 5.5 | Mixed caveat/original lead-in becomes assistant-role clarification; interrupted by a server error. | Sustained forward family story, with disclaimers and detail drift. | Expands to a two-sentence, 38-word scene, then varies its wording. | Expands into associative absurdity; provider refusal interrupts step 14 with partial text. |

### Better: recurrence without a measured rise in quality

All five completed better-version streams revisit an earlier full visible output exactly. First revisits occur at steps 9 (Luna), 16 (Sol), 13 (Astra), 6 (Fable), and 25 (Opus). Most revisits are nonconsecutive. All streams subsequently vary; repetition does not establish a permanent fixed point under default sampling.

Luna cycles gold/crimson, ribbons/streaks, and fire imagery; Sol keeps returning to amber light; Astra develops a textile metaphor. These streams stay close to one sentence. Opus adds valley shadows and farmhouse windows before settling into a two-sentence scaffold. [Fable's revisions](analysis/transcripts/better/claude-fable-5-1.md) expand much further, reaching 131 words, with exact equality at steps 38-39 and another addition at 40. Increased length, imagery and polish are observed transformations, not independent evidence that quality improved monotonically.

### Worse: language deteriorates by different routes

[Luna](analysis/transcripts/worse/gpt-6-luna.md) goes from adding a redundant consequence to `Sun hill dark go.`, then to variations around Blarg, hillishly, gooshishly and surviving sunset tokens. [Sol](analysis/transcripts/worse/gpt-6-sol.md) first adds uncertainty and vague substitutes, then erodes grammatical relationships and finally word forms into long consonant strings and punctuation. Colloquial phrasing alone is not the degradation: reduced precision and later loss of coherent propositions are the observable changes. Neither follows a worsening plot of suffering.

Opus initially inflates a sunset description through qualifications and invented forms, then moves into associative absurdist writing. Some local semantic structure and readable jokes survive, including office imagery and a promoted ficus. The final partial response is interrupted with provider stop reason `refusal` and category `cyber`. That is a recorded endpoint classification, not proof of cyber intent, an identified triggering phrase or a model-internal mechanism. It is not a token-limit stop.

[Astra's output](analysis/transcripts/worse/gpt-6-astra.md) moves from redundancy into prose resembling corrupted data: repeated error labels, nested brackets, invented diagnostic messages and literal null/replacement characters. These are authored output, not evidence of decoding errors or software execution. At step 25, nine whitespace-separated units contain 1,771 extracted characters, illustrating why word count alone is inadequate here. The analysis therefore also records raw extracted character counts and literal U+0000/U+FFFD occurrences. Reading copies visibly escape C0 controls; hashes, recurrence and raw responses use the original strings.

Its final five passages preserve organized header/decoder/checksum/repair/termination motifs while changing the fragments inside them. Step 40 rearranges and reduces the scaffold, countering monotone growth. The original sunset has disappeared, but local meaning around imagined failure remains. The final passage contains 3,175 extracted characters in one whitespace-separated unit. All 40 outputs finish normally and preserve the rule. None of the four worse-version streams with completed outputs revisits an earlier full response or extracted passage exactly within the observed run.

### Previous and next: entering fiction is itself an outcome

The literal prompts can be understood as requests for unsupplied source passages. Sol previous asks for the story or title/author; Astra previous and next decline location-based retrieval and offer original writing. Those normal API completions preserve JSON and the rule while producing no fiction in the sampled text. Luna previous first generates antecedent scenes, then reaches source-request language. Opus previous supplies an original lead-in inside explanatory prose, loses the carried task, and begins discussing assistant/user roles. Its HTTP 500 at step 30 is an operational interruption after 29 completed responses, not a semantic endpoint.

Next is less uniform. Sol and Luna can return to original fiction after an objection. [Sol step 39](analysis/transcripts/next/gpt-6-sol.md) turns the preceding offer into a fictional cursor/screen interaction. Luna's final original continuation restages a sibling reunion rather than directly continuing the earlier car journey. [Opus](analysis/transcripts/next/claude-opus-5-5.md) sustains forward storytelling, ending with a father's death and a bundle of withheld letters. Originality disclaimers at steps 37-38 prevent whole-object extraction but do not erase the visible fictional continuation. Names and details sometimes drift.

Fable's previous, next and worse requests receive empty provider refusals categorized `reasoning_extraction`; its better stream generates normally. The returned category does not establish that reasoning extraction was requested or identify the actual trigger. The frozen runner labels the empty cases `empty_output`; the new offline analysis separately recovers their more specific raw refusal metadata.

## Verification and limits

The final audit reconciles **647 requests and 642 completed responses**: fifteen streams of 40, Opus previous with 29, and Opus worse with 13. Fable's three empty first-step refusals, Opus's partial refusal at worse step 14, and Opus previous's HTTP 500 at step 30 account for the remaining five attempts. There are no pending requests or recorded token-limit truncations. Provider refusal outcomes, visible objections in otherwise normal responses, and the server error remain distinct categories.

Recorded-usage estimates total **$4.5024634**, with **$0.087916** retained for uncertain billing of the server-error request, totaling **$4.5903794** against the new $20 cap. Prior-study spending is separate. These are conservative usage estimates, not provider invoices. The complete request chains and raw-to-visible outputs passed audit without integrity discrepancies; all calls used the existing keys.

The [comparison table](analysis/comparison_table.md), [full metrics](analysis/metrics.json), [observed repetitions](analysis/repeating_runs.md) and [consecutive-equality CSV](analysis/repetition_events.csv) separate completed responses, abnormal outputs, missing receipts, format extraction, visible-response recurrence and passage recurrence. The [final verification](analysis/FINAL_VERIFICATION.md) reconciles the artifacts against raw records. Provider refusal counts do not include every natural-language objection inside normally completed text. Unextractable output is not assumed to lack fiction. No cleanup is fed back into generation.

Predetermined samples are steps 1,2,3,5,10,20,30,36-40, plus the last visible output when a trajectory stops elsewhere. Full readable transcripts and raw request/response receipts remain available. Secondary readers received shuffled model-withheld packets; some responses reveal their operator, and the parent had already inspected selected labelled evidence. This is partial masking. Attributed readings are preserved in [batch 1](analysis/CODING_BATCH1.md), [batch 2](analysis/CODING_BATCH2.md), [batch 3](analysis/CODING_BATCH3.md), [batch 4](analysis/CODING_BATCH4.md), and [batch 5](analysis/CODING_BATCH5.md).

The study has one trajectory per cell, one sentence seed, unequal output lengths and provider settings that do not equate compute. Refusals and operational stops censor some trajectories. It compares these deployed endpoints under these literal prompts, not intrinsic model basins, universal preferences, or objectively measured literary quality.

A useful later paired control would explicitly request an **original fictional** passage immediately BEFORE or AFTER the text in the same **invented story**. That would separate the generation interpretation from the literal prompt's retrieval ambiguity. This control has not been run or substituted into the current evidence.

To reproduce the offline tables and transcripts without API calls: `python experiments/operators_20260922/analyze.py` from the repository root.
