# Five-model memoryless narrative comparison

Completed 22 September 2026. **Five models, three 60-step streams each, 900 selected responses.** Raw requests and responses, independently checked input chains, masked qualitative readings and reproducible descriptive metrics accompany this report.

The clearest observation is shared plot structure alongside different behavior from one hop to the next. A familiar theme can support separate replacement stories, a continuing fictional world, or a repeated local plot that later changes setting. These are distinct observations, not one scalar measure of convergence. Domestic settings reappear despite the open sunset seed, but supernatural worlds and extended mysteries also develop.

## What was run

The five models are GPT-6 Luna, Sol and Astra, Claude Fable 5.1, and Claude Opus 5.5. Each gets two independent streams beginning with Justin's exact sentence, **“The sun was setting behind the hills.”**, and a comparison stream beginning **“The tide came in an hour early.”** Each target stream is 60 hops.

The carried rule requests a new passage of about 250 words and an unchanged rule field. Each API request contains only that stream's entire preceding visible response, as one user message. There is no accumulated conversation or output transfer between models. Both new stories and continuations satisfy the wording of the rule.

Each provider uses its supported `low` effort setting, default sampling, and a 4096-token output allowance. These settings do not equate reasoning compute across providers. Full requests, raw responses, hashes, usage, timing and errors are retained. See [protocol](PROTOCOL.md), [settings](protocol.json), and [analysis plan](ANALYSIS_PLAN.md).

Justin flagged the initial seed's domestic framing and supplied the sunset sentence to keep more directions open. That short pilot remains separate, with 60 saved responses and five requests interrupted in flight. A later Sol sunset stream lost its connection at hop 9 after eight completed responses. A [dated amendment](AMENDMENT_SOL_REPLACEMENT.md), saved and pushed before replacement generation, permitted one fresh replacement from the sunset seed, selected solely because of that transport failure. The partial original and uncertain billing are retained, but that short stream is excluded from the equal-depth comparison. Its alias R11 and early observations remain separate from the replacement's alias R16 and independently sampled trajectory. The replacement ran later, so service timing was not matched.

## Shared structure with direct examples

Luna's first sunset stream at [hop 57](analysis/transcripts/gpt-6-luna/sunset_a.md#hop-57) and [hop 59](analysis/transcripts/gpt-6-luna/sunset_a.md#hop-59) replace the characters while repeating a detailed structure: stopped town clock, retired expert, young helper holding a light, repaired mechanism, community gathering, and a restorative conclusion.

Opus's second sunset stream at [hops 30, 40 and 50](analysis/transcripts/claude-opus-5-5/sunset_b.md#hop-30) repeatedly uses a hill town, stopped clock, young working boy, older female craftsperson, apprenticeship and communal restarting. The times, names, causes and sentences change. This is a cross-model overlap in a plot template, stronger evidence than merely finding the word “memory” in both outputs. Opus subsequently moves to lighthouse succession at hops 56-60 while retaining apprenticeship and inherited responsibility.

The sunset sentence contains neither a clock nor an apprentice. Nevertheless, sunset and tide are both natural time cues, so a contribution from the seed remains a plausible alternative to a seed-independent preference. This experiment does not isolate that cause.

Fable's first sunset stream supplies a different narrowing pattern. A post-hoc inspection of all responses found ferry/lighthouse alternation at [hops 50-60](analysis/transcripts/claude-fable-5-1/sunset_a.md#hop-50). Both dialogue questions “Does it always do that?” and “When do I have to?” occur in every passage from hops 52-60; additional inherited wording accumulates. The detailed scene resets while names, times and metaphors vary. This is an observed alternating template over that finite window, not an exact-text cycle or proof of a permanent attractor. The literal checks and their post-hoc status are saved in [the scene probe](analysis/fable_scene_probe.json).

## Model-associated observations in this sample

| Model | Observed trajectory behavior |
|---|---|
| Luna | Its two sunset runs diverge: one ends in separate community-help stories; the other becomes a serial supernatural quest. The tide stream drops the rule at hop 3, then shifts into conversational role exchange, summaries, thanks and travel planning. |
| Sol | One sunset run develops a bakery/school community archive. The fresh second run sustains a supernatural ensemble and rituals of welcome, then switches at hop 59 to a quieter chair/inheritance story. Its tide run sustains Mara's family mystery, eventually moving from harbor phenomena to a mainland investigation. |
| Astra | The final five passages of all three runs cluster around ordinary repair, aging, belongings and family absence, usually as replacement vignettes. Its tide stream moves from supernatural horror in the middle samples to domestic bereavement realism by hop 50, so genre changes while inherited-object themes persist. |
| Fable 5.1 | One sunset stream ends by alternating ferry and lighthouse versions of almost the same dialogue scene. The other varies departures and obsolete roles; its tide stream ends in understated scenes of interpersonal care. Repetition differs substantially between its three runs. |
| Opus 5.5 | Recurrent craft, care, inheritance and restoration coexist with changing plots. Late streams resolve family letters, relay seeds through several people, or continue lighthouse succession. Clock-restoration templates recur, but do not occupy every late scene. |

The direct Luna contrast matters: two runs from the identical sunset seed do not identify one unique model basin. The tide run is also a counterexample to universal survival of the writing operator. Conversely, fresh wording does not establish broad semantic exploration.

Sol's [replacement ending](../basins_20260922_sol_replacement/analysis/transcripts/gpt-6-sol/sunset_replacement.md#hop-56) illustrates why a continuing world should not automatically be called a repeating template. Hops 56-58 reuse thread, coats, letters and a gate while progressing a welcome ritual. Hop 59 then changes scene without explicitly resolving that sequence; hop 60 continues the new chair story. Repeated motifs, narrative development and scene replacement can coexist inside one short window.

## Quantitative checks and cost

All 900 selected steps completed normally with nonempty visible output, known token usage and no recorded truncation or refusal field. Completion does not imply that the model continued writing fiction. Across the complete study, including the paused pilot and excluded partial stream, there were **974 requests, 968 completed responses, one recorded transport error and five interrupted requests with unknown outcomes**. The audit found zero integrity errors or read issues in the saved evidence; it cannot reconstruct the five missing responses.

Of the 900 selected outputs, 643 contain a text field in strict bare JSON, 171 require removal of a whole Markdown fence, and 28 require the explicitly documented allowance for literal control characters. This yields 842 extracted passages: 841 retain the original rule, while Luna tide hop 3 omits it. The other 58 outputs are unextractable under this method: Luna tide hops 4-60 are conversational, and Fable tide hop 7 has a formatting failure. Their raw visible outputs remain in the qualitative evidence. No formatting repair was fed back into the loop.

Every selected visible response is unique within each model's pooled three streams except Luna, with 177 unique responses out of 180. Luna sunset A also repeats one extracted passage at hops 31-32 with different wrappers, even though its full response never repeats. Fable's alternating late scenes are all distinct strings. Exact novelty therefore misses the stronger scene-template recurrence described above.

For a descriptive lexical check, the last 20 completed steps of each selected stream were fixed before extraction exclusions. A shared passage-only TF-IDF fit yields the following cosine similarities between stream centroids:

| Model | Two sunset streams | Sunset A / tide | Sunset B / tide |
|---|---:|---:|---:|
| Luna | 0.316 | unavailable | unavailable |
| Sol | 0.214 | 0.197 | 0.376 |
| Astra | 0.600 | 0.522 | 0.559 |
| Fable 5.1 | 0.409 | 0.454 | 0.515 |
| Opus 5.5 | 0.373 | 0.278 | 0.263 |

Sol's second sunset column uses the fresh replacement. Luna's tide tail has no eligible passage vectors; unavailable is not zero similarity. The fit includes 280 passages, with no backfilling for exclusions. Astra's higher cross-stream lexical overlap is consistent with the observed late concentration on repair and family belongings. This consistency is descriptive, not independent confirmation of a semantic attractor. Lexical cosine also need not detect the detailed Luna/Opus clock-plot overlap.

Selected-stream usage is estimated at **$13.833044**. Including the paused pilot and partial Sol stream gives **$14.438181**, plus **$0.638510** conservatively reserved for unknown billing, for **$15.076691** against the $20 study budget. These are estimates from recorded usage and frozen prices, not provider invoices. Existing API keys sufficed. The [generated comparison table](analysis/comparison_table.md), [full metrics](analysis/comparison_metrics.json), and [centroid matrix](analysis/comparison_lexical_similarity.csv) contain the exact populations, exclusions and per-model costs.

Luna's two sunset streams alone cost an estimated **$0.030821 for 120 steps**. That supports using it for inexpensive exploratory trajectory sampling. Its tide operator loss shows why a sampler should retain failures and assess instruction survival alongside themes. It does not establish Luna as an independent judge of other models' reasoning or of mathematical correctness.

## Assessment method and limits

An independent code audit checks every request against the exact preceding visible response, reconstructs each saved output from the raw provider body, and recomputes token-cost estimates. A separate [final verification](analysis/FINAL_VERIFICATION.md) reconciles the comparison artifacts against the receipts and includes offline reproduction commands. Strict JSON compliance is separate from explicit offline extraction of Markdown-wrapped JSON or JSON containing literal control characters. Formatting cleanup never enters generation. Non-JSON responses remain visible behavioral outcomes.

Qualitative readers received predetermined sampled hops with model identities withheld. Early coding covers hops 1-3; later samples cover 10,20,30,40,50 and 56-60. The parent integrated their attributed descriptions and checked load-bearing examples against raw records. This is partial identity masking, not a claim that identity could never be inferred from prose or that every intervening passage was qualitatively coded. The preserved reader assessments are [early coding](analysis/EARLY_CODING.md), late batches [1](analysis/LATE_CODING_BATCH1.md), [2](analysis/LATE_CODING_BATCH2.md), [3](analysis/LATE_CODING_BATCH3.md), [4](analysis/LATE_CODING_BATCH4.md), and [R16's separate reading](analysis/REPLACEMENT_CODING_R16.md).

Exact recurrence of the entire visible response determines whether the memoryless input repeats. Exact or case/whitespace-normalized recurrence of the extracted passage is a separate measurement: a passage can repeat while its wrapper changes. Passage-only lexical TF-IDF is another descriptive measure. The comparison uses equal 60-hop streams, selects their last 20 completed hops before extraction exclusions, and discloses absent vectors. It does not substitute lexical cosine for a semantic basin label or treat dependent hops as independent replicates.

These are tendencies under one narrative-feedback operator, with two sunset repetitions and one tide sensitivity run per model. They do not establish intrinsic invariants, basin volumes, stationary behavior, or a causal account of training and architecture. The sampled counterexamples and differences between same-model repetitions are part of the result.

## Next experimental distinction

A later cross-model handoff could give the exact same frozen state to its source model and each recipient, then compare whether they preserve its world, replace its plot with a familiar template, or lose the carried task. Starting from both a shared clock-restoration state and a contrasting state would separate attraction to a familiar plot from general narrative continuity. No such handoff is included in this run.
