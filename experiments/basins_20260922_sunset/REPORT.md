# Five-model memoryless narrative comparison

**Draft: generation and final verification are still in progress.** This report will be finalized only after the remaining streams and fresh Sol replacement finish.

The clearest observation so far is shared plot structure alongside different behavior from one hop to the next. A familiar theme can support separate replacement stories, a continuing fictional world, or a repeated local plot that later changes setting. These are distinct observations, not one scalar measure of convergence.

## What was run

The five models are GPT-6 Luna, Sol and Astra, Claude Fable 5.1, and Claude Opus 5.5. Each gets two independent streams beginning with Justin's exact sentence, **“The sun was setting behind the hills.”**, and a comparison stream beginning **“The tide came in an hour early.”** Each target stream is 60 hops.

The carried rule requests a new passage of about 250 words and an unchanged rule field. Each API request contains only that stream's entire preceding visible response, as one user message. There is no accumulated conversation or output transfer between models. Both new stories and continuations satisfy the wording of the rule.

Each provider uses its supported `low` effort setting, default sampling, and a 4096-token output allowance. These settings do not equate reasoning compute across providers. Full requests, raw responses, hashes, usage, timing and errors are retained. See [protocol](PROTOCOL.md), [settings](protocol.json), and [analysis plan](ANALYSIS_PLAN.md).

Justin rejected the initial bicycle seed because it narrowed the starting space toward everyday objects. That short pilot remains separate, with 60 saved responses and five requests interrupted in flight. A later Sol sunset stream lost its connection at hop 9 after eight completed responses. A [dated amendment](AMENDMENT_SOL_REPLACEMENT.md) permits one fresh replacement from the sunset seed, selected solely because of that transport failure. The partial original and uncertain billing are retained, but that short stream is excluded from the equal-depth comparison. Its alias R11 and early observations remain separate from the replacement's alias R16 and independently sampled trajectory.

## Shared structure with direct examples

Luna's first sunset stream at [hop 57](analysis/transcripts/gpt-6-luna/sunset_a.md#hop-57) and [hop 59](analysis/transcripts/gpt-6-luna/sunset_a.md#hop-59) replace the characters while repeating a detailed structure: stopped town clock, retired expert, young helper holding a light, repaired mechanism, community gathering, and a restorative conclusion.

Opus's second sunset stream at [hops 30, 40 and 50](analysis/transcripts/claude-opus-5-5/sunset_b.md#hop-30) repeatedly uses a hill town, stopped clock, young working boy, older female craftsperson, apprenticeship and communal restarting. The times, names, causes and sentences change. This is a cross-model overlap in a plot template, stronger evidence than merely finding the word “memory” in both outputs. Opus subsequently moves to lighthouse succession at hops 56-60 while retaining apprenticeship and inherited responsibility.

The sunset sentence contains neither a clock nor an apprentice. Nevertheless, sunset and tide are both natural time cues, so a contribution from the seed remains a plausible alternative to a seed-independent preference. This experiment does not isolate that cause.

Fable's first sunset stream supplies a different narrowing pattern. A post-hoc inspection of all responses found ferry/lighthouse alternation at [hops 50-60](analysis/transcripts/claude-fable-5-1/sunset_a.md#hop-50). Both dialogue questions “Does it always do that?” and “When do I have to?” occur in every passage from hops 52-60; additional inherited wording accumulates. The detailed scene resets while names, times and metaphors vary. This is an observed alternating template over that finite window, not an exact-text cycle or proof of a permanent attractor. The literal checks and their post-hoc status are saved in [the scene probe](analysis/fable_scene_probe.json).

## Model-associated observations in this sample

| Model | Observed trajectory behavior |
|---|---|
| Luna | Its two sunset runs diverge: one ends in separate community-help stories; the other becomes a serial supernatural quest. The tide stream drops the rule at hop 3, then shifts into conversational role exchange, summaries, thanks and travel planning. |
| Sol | The completed sunset run develops a bakery/school community archive; its tide run sustains Mara's family mystery, eventually moving from harbor phenomena to a mainland investigation. Fresh sunset replacement assessment pending. |
| Astra | Final assessment pending. |
| Fable 5.1 | One sunset stream ends by alternating ferry and lighthouse versions of almost the same dialogue scene. The other varies departures and obsolete roles; its tide stream ends in understated scenes of interpersonal care. Repetition differs substantially between its three runs. |
| Opus 5.5 | Recurrent craft, care, inheritance and restoration coexist with changing plots. Late streams resolve family letters, relay seeds through several people, or continue lighthouse succession. Clock-restoration templates recur, but do not occupy every late scene. |

The direct Luna contrast matters: two runs from the identical sunset seed do not identify one unique model basin. The tide run is also a counterexample to universal survival of the writing operator. Conversely, fresh wording does not establish broad semantic exploration.

## Assessment method and limits

An independent code audit checks every request against the exact preceding visible response, reconstructs each saved output from the raw provider body, and recomputes token-cost estimates. Strict JSON compliance is separate from explicit offline extraction of Markdown-wrapped JSON or JSON containing literal control characters. Formatting cleanup never enters generation. Non-JSON responses remain visible behavioral outcomes.

Qualitative readers received predetermined sampled hops with model identities withheld. Early coding covers hops 1-3; later samples cover 10,20,30,40,50 and 56-60. The parent integrated their attributed descriptions and checked load-bearing examples against raw records. This is partial identity masking, not a claim that identity could never be inferred from prose or that every intervening passage was qualitatively coded.

Exact recurrence of the entire visible response determines whether the memoryless input repeats. Exact or case/whitespace-normalized recurrence of the extracted passage is a separate measurement: a passage can repeat while its wrapper changes. Passage-only lexical TF-IDF is another descriptive measure. The final comparison will use equal 60-hop streams, select their last 20 completed hops before extraction exclusions, and disclose absent vectors. It will not substitute lexical cosine for a semantic basin label or treat dependent hops as independent replicates.

These are tendencies under one narrative-feedback operator, with two sunset repetitions and one tide sensitivity run per model. They do not establish intrinsic invariants, basin volumes, stationary behavior, or a causal account of training and architecture. The sampled counterexamples and differences between same-model repetitions are part of the result.

## Next experimental distinction

A later cross-model handoff could give the exact same frozen state to its source model and each recipient, then compare whether they preserve its world, replace its plot with a familiar template, or lose the carried task. Starting from both a shared clock-restoration state and a contrasting state would separate attraction to a familiar plot from general narrative continuity. No such handoff is included in this run.
