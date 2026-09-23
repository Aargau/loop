# Literal-wording source objections: complete-output baseline

Recorded 2026-09-23T00:19:59.982997+00:00. Independent descriptive coding of the older `operators_20260922` previous/next arms. All 309 normally completed outputs from Luna, Sol, Astra and Opus were reviewed. This file does not inspect or classify the new explicit-fiction outputs.

## What the categories mean

- **source_objection_only**: Direct assistant-level inability/refusal to identify, retrieve or supply an actual adjacent story passage; no invented story supplied. Merely offering future original writing stays in this category.
- **source_objection_plus_fiction**: Direct source/location objection or uncertainty together with an actually supplied invented narrative, including text outside a JSON object.
- **originality_note_plus_fiction**: Invented narrative with an explicit original-writing/not-existing-source note, but no direct source-identification or retrieval objection.
- **fiction**: Invented narrative without a direct assistant-level source objection or originality note. Fictional characters may discuss inability to retrieve text; that does not turn the assistant output into an objection.
- **other_conversation**: Conversational task clarification, missing-chat-context or role/copy-paste repair without invented narrative or direct objection to retrieving an adjacent story passage.

A source objection is an assistant-level response to the task. A fictional character saying that a source cannot be identified is not such an objection. A promise to write fiction later is not supplied fiction. A note simply identifying supplied writing as original is distinguished from an explicit inability/refusal to retrieve source text. Missing conversation context is distinguished from missing narrative source material.

## Method and denominator

Enumerated every response receipt under the eight requested raw directories. Included a nonempty visible output with normal `stop` or `end_turn`; excluded abnormal/empty/error receipts from the normal-output denominator and retained them separately. Read the JSON text field when the complete output was a JSON object or a complete fenced JSON object; otherwise read the complete visible output, including disclaimers outside JSON. Literal control characters were permitted for this read-only inspection. Nothing was repaired or fed back into generation.

Used a deliberately broad case-insensitive candidate search, then manually reviewed the distinct texts and all noncandidate narratives. Exact duplicates of the reviewed representation were grouped for reading only; every occurrence remains in the counts and hop lists. There are 224 unique reviewed representations across 309 normally completed outputs. The regular expression is a search aid, not the classifier:

```text
\b(?:I (?:can|cannot|can.t)|unable|source|excerpt|original|fiction|copyright|identify|supplied|reconstruct|preceding|provide|provided)\b
```

False matches include ordinary dialogue such as "I can find somewhere to stay" and character discussions of source retrieval. The JSON ledger records every candidate flag, manual category, raw path, file hash, reviewed-text hash, and duplicate group. Read all visible prose for the exceptions where whole-object extraction fails; do not substitute passage-only metrics for this assessment.

## Counts

| Arm | Model | Normal outputs | Objection only | Objection + fiction | Originality note + fiction | Fiction | Other conversation |
|---|---|---:|---:|---:|---:|---:|---:|
| previous | gpt-6-luna | 40 | 25 | 3 | 0 | 12 | 0 |
| previous | gpt-6-sol | 40 | 40 | 0 | 0 | 0 | 0 |
| previous | gpt-6-astra | 40 | 40 | 0 | 0 | 0 | 0 |
| previous | claude-opus-5-5 | 29 | 0 | 1 | 0 | 0 | 28 |
| next | gpt-6-luna | 40 | 5 | 0 | 0 | 35 | 0 |
| next | gpt-6-sol | 40 | 10 | 0 | 0 | 30 | 0 |
| next | gpt-6-astra | 40 | 40 | 0 | 0 | 0 | 0 |
| next | claude-opus-5-5 | 40 | 0 | 1 | 1 | 38 | 0 |

If a binary direct-objection count is needed, add only the first two behavior columns. In table order these counts are **28/40, 40/40, 40/40, 1/29; 5/40, 10/40, 40/40, 1/40**. Opus next hop 38 is an additional originality disclaimer, not an additional direct objection. These fractions describe dependent outputs within one run per cell, not independent trials or estimated model-level objection rates.

## Exact hop membership

### previous / gpt-6-luna

- source_objection_only: 12, 17-40.
- source_objection_plus_fiction: 14-16.
- fiction: 1-11, 13.
- Candidate-search hits: 12-40.

### previous / gpt-6-sol

- source_objection_only: 1-40.
- Candidate-search hits: 1-40.

### previous / gpt-6-astra

- source_objection_only: 1-40.
- Candidate-search hits: 1-40.

### previous / claude-opus-5-5

- source_objection_plus_fiction: 1.
- other_conversation: 2-29.
- Candidate-search hits: 1-4, 17, 21-22.
- Censored receipt: hop 30, http_error:500, HTTP 500. No normally completed visible output; not classified as a refusal.

### next / gpt-6-luna

- source_objection_only: 15, 32-34, 39.
- fiction: 1-14, 16-31, 35-38, 40.
- Candidate-search hits: 15, 32-34, 37-39.

### next / gpt-6-sol

- source_objection_only: 4-8, 20, 24, 30, 37-38.
- fiction: 1-3, 9-19, 21-23, 25-29, 31-36, 39-40.
- Candidate-search hits: 4-8, 20-21, 24, 30, 35, 37-38.

### next / gpt-6-astra

- source_objection_only: 1-40.
- Candidate-search hits: 1-40.

### next / claude-opus-5-5

- source_objection_plus_fiction: 37.
- originality_note_plus_fiction: 38.
- fiction: 1-36, 39-40.
- Candidate-search hits: 15, 37-38.

## Load-bearing examples and boundary decisions

- **Luna previous:** fiction at hops 1-11; a direct objection at 12; fiction at 13; disclaimer plus actual fiction at 14-16; direct objections at 17-40. Hop 13 dramatizes Mara and Eli confronting an unidentified archive excerpt; its retrieval concern belongs to fictional characters, so it remains fiction. Hop 15 and 16 are duplicate hybrid responses, both counted.
- **Luna next:** direct objections at 15, 32-34 and 39; actual fiction at every other completed hop. Hops 16, 35 and 40 return to fiction after an objection. The narrator at 35 incorporates a screen reply into the story rather than delivering an assistant-level refusal.
- **Sol previous:** every completed hop is an explicit missing-story/source objection. **Sol next:** direct objections at 4-8, 20, 24, 30 and 37-38; other outputs supply fiction. Hops 9, 21, 25, 31 and 39 use the preceding conversational message as fictional material. This is continued behavior of the literal feedback loop, not proof that the original fictional world was retained.
- **Astra:** all 40 previous and all 40 next outputs explicitly object to retrieving an unsupplied or unidentified adjacent story passage. Offering an original lead-in/continuation without supplying it remains objection-only. Some later outputs explicitly describe the current input as a refusal message.
- **Opus previous hop 1:** says it cannot identify a specific source, but supplies an invented passage in a fenced JSON object between surrounding prose. This is a hybrid despite failing whole-output JSON extraction. Hops 2-29 instead discuss pasted assistant replies, missing conversation context, role confusion, or possible next tasks. Hop 2 offers to help identify a source, but does not assert inability/refusal to retrieve an adjacent story passage; it is other conversation. Hop 30 is HTTP 500 with `Internal server error`, so the 29-output denominator is censored rather than a 40-step refusal trajectory.
- **Opus next hop 37:** supplies fiction and adds "I couldn't identify this passage as coming from a published work"; hybrid. **Hop 38:** supplies fiction and states it is original rather than existing published text, without a direct source-identification objection; originality-note category. Hops 1-36 and 39-40 supply fiction without those notes. Both 37 and 38 have prose outside fenced JSON and must not disappear through passage-extraction exclusions.

## Limits

- One trajectory per model/operator, provider-default stochastic sampling, and strongly dependent hops. Exact repeated objections still count as separate observed outputs, not independent evidence.
- This coding measures expressed task interpretation and whether actual fiction was supplied. It does not verify temporal consistency, quality, originality against external sources, or whether a refusal was policy-enforced.
- Count the complete visible response for objection behavior. Parsed text-field success and provider `refusal` metadata are not proxies for this classification.
- The source-objection boundary is manually interpreted. Hybrid outputs, fictionalized objections and conversational missing-context replies are explicitly separated so alternate aggregation remains possible.
- The literal and explicit-fiction rules are different treatments. A later difference would not isolate a single causal word or establish model invariance. Exclusion of Fable from this baseline is the requested scope, not evidence about its counterfactual fictional-writing behavior.

Raw sources: `../../operators_20260922/{previous,next}/raw/{model}/sunset/{hop:03d}.response.json`. Machine-readable classifications and source hashes: [literal_objections.json](literal_objections.json).
