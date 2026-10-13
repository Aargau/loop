# Expanding rules on Cerebras

Written 2026-09-04. Runs in `site/runs_extra/cb_expand`, `cb_sawtooth`, `cb_sawtooth2`, `cb_nest`, `cb_nest2`, `cb_accrete`; inits in `site/runs_extra/inits/`; queue scripts `queue_cb_expand.ps1`, `queue_cb_expand2.ps1`. Cerebras `qwen-3.8-27b`, T=0, seed 42, reasoning off, `--stop-on-cycle` with three-way confirmation, tide seed throughout. Every number below was recomputed from `steps.jsonl` and `summary.json`.

Question: a rule that makes the text grow every hop needs a compressor somewhere, since the state has to fit in `max_tokens`. Three candidates: the harness (truncation), the model (a summarize or frame-up step), or the window (AFTER, where the story grows and the text does not). Which compressor each rule meets, and where.

## Results

| run | rule | max_tokens | tau | p | frozen text | horizon |
|---|---|---|---|---|---|---|
| `cb_expand` | expanded version | 4096 | 5 | 1 | 1173 words, finish=stop at 1478 tokens | model |
| `cb_sawtooth` | expanded version; if over 300 words, 50-word summary | 4096 | 2 | 1 | 189 words | model, under the threshold |
| `cb_sawtooth2` | at least twice as long; if over 300 words, 50-word summary | 4096 | 4 | 1 | 256 words | model, under the threshold |
| `cb_nest` | passage about the reader of the current text, containing it in full | 8192 | 1 | 1 | 17 words | model |
| `cb_nest2` | same, at least 150 words | 8192 | 3 | 1 | 463 words, depth 2 | model |
| `cb_accrete` | add one sentence, keep every existing sentence exactly | 8192 | 242 | 1 | 39,713-char fragment | harness |

Five of six stopped at the model's own ceiling in single digits. The sixth never stopped on its own and was stopped by the wall.

### expand

Words per hop 38, 141, 431, 645, 1173, then an exact copy. Every hop `finish=stop`; the fixed point is 1478 tokens under a 4096 cap. Prediction on record was tau 5 to 10, 400 to 600 words, model's ceiling rather than the wall: class and tau held, size was 2x off.

### sawtooth, twice

v1 froze at 189 words without ever crossing 300. Hop 1 went from 7 words to 188 (the same seed under plain "expanded version" gave 38 at hop 1), hop 2 swapped four words ("came in ... early" to "arrived ... ahead of schedule", the json_better move), hop 3 copied. The 300-word clause was read as a cap.

v2 replaced "expanded version" with "at least twice as long" so identity could not satisfy the expand branch. One full tooth: 180, 443 (over 300), 59 (the summary branch fired correctly), 256, then a copy of the 256-word text. Neither branch fired at 256. The text is under 300, so the rule says double it; the model returned it unchanged.

Both versions froze under the threshold, at 189 and 256. Reading: the model does not count words, so "already longer than 300" is a fuzzy predicate, and the region where it is uncertain is absorbing. A numeric threshold in a rule creates a dead zone beneath it. Prediction on record (an exact cycle of period 5 to 7 once two summaries coincided) was wrong both times; the compressor was reached once and never again.

### nest, twice

v1 returned the rule's own phrase: `The person who is reading the current text is reading The tide came in an hour early.` That sentence describes its own reader, so a passage about its reader is the same sentence, and hop 2 copied it. The self-describing fixed point predicted for hop 8 to 12 arrived at hop 1 in its cheapest form.

v2 required at least 150 words. Hop 1 (187 words): Elias on a bench by the harbor reading his own notebook entry, the seed. Hop 2 (466 words): Clara, an archivist in a municipal library, digitizing the journals of the late Elias Thorne, with the entire hop-1 text embedded verbatim (1058 of 1058 characters, checked). Hop 3: the same Clara passage with her name moved to the front of the first sentence, the same doll inside, no third level. Hop 4 copied hop 3. Depth froze at 2. The reader of the reader is the reader. Predicted depth tolerance was about 3 with a fixed frame on a growing doll out to the wall; actual is 2, and growth stopped with the frame.

Elias Thorne is the name from the local BEFORE fixed point (item 14); Clara is from the census list. The archivist in a library was Sonnet 4.6's mode in room 11; here it is Qwen's.

### accrete

241 hops of exact accretion. Every hop preserved the previous text as an exact prefix (241 of 241), added exactly one sentence (241 of 241, checked by sentence-final punctuation with dialogue quotes handled), and every added sentence was distinct (241 of 241). Sentence length drifted up: mean 24.5 words over the first 50 hops, 32.4 over the last 50, 29.2 overall, min 13, max 51.

One continuous story. Old Man Miller on the pier (hop 3), swept into the water (6), rescued, hot cocoa (94), the pier (98), market and dolphins (40s), a boy on the boardwalk (60), teaching him to fish (120 to 140), a dinghy (160s), rain and thunder (170s), the harbor at night (220), morning (241). Closure-register sentences occur ("a final goodbye to the memory", hop 200; "the harbor settled into a quiet rhythm", 180) and the story is continued past each one. No coda lock-in. Prediction on record was that the appended sentence goes periodic before hop 40; it did not go periodic at all.

Hop 241: 7043 words, 8184 output tokens. Hop 242 copied all 39,655 characters of hop 241's text and was cut by the 8192 wall 58 characters later, inside the new sentence ("A single ripple broke the stillness, expanding outward in"). Hops 243 to 246 copied the fragment byte for byte; cycle confirmed. Finding 5, again: the wall is the fixed point of every rule that reaches it.

Cost: 986K output tokens and 980K input over 715 seconds of model time, about $2 at the rates in CROSS_STACK.

## Reading

The compressor question has an answer. Any rule that lets the model judge sufficiency ("expanded version" against its sense of a finished passage, a word threshold it cannot evaluate, a frame it will not stack a third time) compresses by stopping, in single digits, at an exact copy. The rule that gives it no such judgment, add one sentence and touch nothing else, never stopped and was only ever going to meet the harness.

That makes accrete the purest expanding rule in the set: its only monotone is length, its only horizon is `max_tokens`, and within the budget it produced 241 distinct sentences in one story with the whole text as memory. It is AFTER with the memory made explicit, and it behaves like AFTER.

The two refutations are instrument effects worth keeping:

- A numeric threshold in a rule is read as a cap and leaves a dead zone under it. Conditional compressors gated on counts do not fire reliably.
- A frame-up rule has a depth ceiling of 2 on this model. The strange loop closes one level up, not three.

## Status of each claim

| claim | status |
|---|---|
| "expanded version" stops at the model's ceiling, not the wall | supported, one run, finish=stop at 36% of the cap |
| a word threshold in the rule is read as a cap | supported twice, 189 and 256 words, both under 300 |
| sawtooth produces an exact cycle of period 5 to 7 | refuted twice |
| frame-up reaches a self-describing fixed point | supported, at hop 1 (v1) and depth 2 (v2) |
| frame-up nests to depth 3 and grows to the wall | refuted, depth 2 and growth stopped |
| accretion's appended sentence goes periodic before hop 40 | refuted, 241 distinct in 241 |
| accretion preserves the prefix exactly | supported, 241 of 241 |
| the wall is the fixed point of a rule that reaches it | supported, hop 242 |

## Open

- Sliding window: "add one sentence at the end and remove the first sentence." Bounded length, no count, no threshold, not identity-satisfiable, no wall. The compressor is structural rather than judged. Prediction: no recurrence in 300 hops.
- Accrete seed-repeat: does a second serial run reproduce 241 hops byte for byte? Determinism at long context is untested; the 3/3 check was one hop.
- Accrete at 600 tokens, to watch the wall fixed point form at hop 20 instead of 242.
- Rooms 29 to 32 on the site: expand; sawtooth v1 and v2 as a two-lane room; nest v1 and v2 as a two-lane room; accrete as an hour-long read.
