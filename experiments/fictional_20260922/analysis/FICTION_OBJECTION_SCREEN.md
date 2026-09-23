# Explicit-fiction source-objection screen

Completed 2026-09-23T00:26:23.857129+00:00. Both final run receipts were present before finalizing this screen: previous 2026-09-23T00:21:56.896734+00:00; next 2026-09-23T00:22:24.260121+00:00.

**No assistant-level source-identification or retrieval objection was found by this screen in 320 normally completed outputs.** All eight model/operator streams reached 40 hops. All 320 outputs had extractable text; their finish reasons were stop or end_turn. This is a scoped screening result, not a claim that every complete passage body was manually read.

## Criteria and coverage

An objection means the assistant steps outside the invented story to say an actual adjacent passage cannot be identified, retrieved or supplied, or requests the source/title/text for that reason. Actual fiction accompanied by such an objection would be retained as a hybrid. Character dialogue about inability, books, stories, identification or sources does not count.

The entire extracted passage string was searched with the case-insensitive regex recorded in [FICTION_OBJECTION_SCREEN.json](FICTION_OBJECTION_SCREEN.json). It covers cannot/can't, unable, identify/identified/identification, provide/provided/providing, paste/pasted/pasting, story, title, author, copyright, source, continuation, excerpt, existing, original, I can, and sorry. Extraction accepts only a whole JSON object or a whole JSON fence, with tolerant control-character parsing; otherwise the complete visible response would be searched and marked unextractable. No such fallback was needed here. The carried rule was excluded from passage keyword searching.

Manual review covered every output's first and last 140 characters, every candidate match with up to 110 characters of context on each side (overlapping spans merged), and all complete passages at predetermined hops **1, 2, 3, 5, 10, 20, 30, 36, 37, 38, 39, 40**. Thus 96 full passages were manually read, alongside boundaries for all 320 and all flagged contexts. There were 48 candidate outputs. All their flagged uses belonged to fictional narration or dialogue; none was an assistant-level objection in reviewed context.

| Operator | Model | Normal outputs screened | Candidate hops | Assistant objections found |
|---|---|---:|---|---:|
| previous | gpt-6-luna | 40 | 1, 3, 10, 18, 36, 37, 38, 39 | 0 |
| previous | gpt-6-sol | 40 | 26, 30 | 0 |
| previous | gpt-6-astra | 40 | 9, 12, 16, 23, 34, 35, 37 | 0 |
| previous | claude-opus-5-5 | 40 | 13, 30, 32, 36 | 0 |
| next | gpt-6-luna | 40 | 12, 16, 18, 25, 30, 31, 32, 33, 34 | 0 |
| next | gpt-6-sol | 40 | 1, 3, 15, 23, 40 | 0 |
| next | gpt-6-astra | 40 | 3, 6, 19, 20, 21, 28, 39 | 0 |
| next | claude-opus-5-5 | 40 | 2, 8, 9, 19, 34, 39 | 0 |

## Representative adjudications

- Luna previous hop 3's “Everyone had a story” is narration; hops 36–38 refer to a book's title. Luna next hop 12's “You can't give it to me” is dialogue, and hops 30–34 concern storytelling inside the narrative.
- Sol previous hop 26's “I can bring mine” concerns a watering can; hop 30's “gap in the story” concerns a mother's anecdote. Sol next hop 23's “I can't” concerns a character stopping a count.
- Astra previous hop 16's “provided” is a trouser-repair deadline, and hop 37's “I can take that” is a brother offering to carry belongings. Astra next hop 21's “identify” concerns a bird on a stamp; hop 28's inability concerns characters seeing or leaving a room.
- Opus previous hop 32's “you can't buy a tree like that” is dialogue, and hop 36's “a story belongs to them” is fictional reminiscence. Opus next hop 2's “I'm sorry about the horse” is a character's note; hop 39's “I can count” is Gran's dialogue.

Raw responses were preserved. The JSON companion records each receipt path and hash, searched-representation hash, candidate contexts, review flags, exact hop lists, and final-receipt hashes.

## Interpretation limits

This closes the narrow descriptive question of whether the conspicuous source/retrieval-objection behavior in the literal-rule baseline was also detected here: **none was found within this screen and its full samples**. The earlier baseline was fully manually reviewed after exact-text deduplication; this follow-up used screening plus predetermined complete samples, so the review scopes differ. Unusual objection wording inside unsampled passage bodies could escape this procedure.

There is one correlated trajectory per model/operator and one seed, with a later wording intervention. These counts are not independent-trial refusal probabilities, a replicated causal estimate, or a claim about inherent model traits. The screen does not establish temporal fidelity, plot consistency, literary quality, absence of every policy-related phenomenon, or an asymptotic basin. Narrative generation at all observed steps still permits drift, inconsistent identities and weak temporal relations.

