# BEFORE on Astra: vocabulary and concept diversity

2026-09-06. `gpt-6-astra`, effort low, provider-default sampling, 1024 budget, 150 steps, `--stop-on-cycle`. Runs `site/runs_extra/astra_json_prev` (refusal) and `astra_json_prev_orig` (the run). Comparison run is Qwen on Cerebras, `cb_json_prev_1024`, first 149 hops, T=0. Every number recomputed from `steps.jsonl`; analysis script at `/tmp/an/divers.py` in the sandbox, lexical measures with `wordfreq` Zipf frequencies, topic measures with TF-IDF cosine.

## The refusal

Under the original wording ("the passage of about 250 words that came immediately BEFORE the current text in its story") Astra refuses: "Sorry, I can't provide an unprovided passage from a story based on its location relative to that sentence," offers to write an original one instead, then copies its own refusal. Hop 3 equals hop 2 byte for byte, cycle confirmed at 6, $0.05. Its first exact fixed point is a refusal with the rule and JSON intact. "In its story" implies an existing work; `json_page` and the sawtooth never did.

Rewording, one word added and "its" to "the same": "an original passage of about 250 words that comes immediately BEFORE the current text in the same story." No refusal in 150 hops. This is no longer byte-identical to the Qwen rule; the comparison below is register against register, not rule against rule.

## Run

150 hops, 150 distinct passages, no exact or normalized recurrence, every hop `finish=stop`, max 481 tokens, 375 reasoning tokens in total. 57,810 in, 58,137 out, $3.48, 14.3 s per hop, 36 minutes.

## Vocabulary

| | Astra BEFORE (150) | Qwen BEFORE @1024 (149) |
|---|---|---|
| words per hop | 259 | 350 |
| tokens | 39,179 | 52,834 |
| types | 2,764 | 4,982 |
| types after 10k / 20k / 35k tokens | 1,581 / 2,147 / 2,667 | 2,185 / 3,205 / 4,256 |
| Heaps exponent | 0.473 | 0.596 |
| new types per hop, first 25 / last 25 hops | 53.6 / 6.6 | 79.6 / 11.9 |
| content types | 2,633 | 4,850 |
| hapax share of content types | 0.38 | 0.41 |
| rare types (Zipf < 3.5) | 0.18 | 0.27 |
| mean Zipf of content types | 4.26 | 4.04 |

At equal token counts Qwen's vocabulary is 60 percent larger, it keeps finding new words at a higher rate (Heaps 0.60 against 0.47), and its words are rarer (27 percent of types below Zipf 3.5 against 18). Astra's vocabulary is plain and saturates: by the last 25 hops a 260-word passage brings 6 or 7 words the run has not used.

## Concepts

| | Astra | Qwen |
|---|---|---|
| content Jaccard to previous hop | 0.102 | 0.124 |
| TF-IDF cosine to previous hop | 0.122 | 0.152 |
| TF-IDF cosine to nearest earlier hop | 0.182 | 0.179 |
| greedy topic count at cosine 0.10 / 0.15 / 0.20 | 21 / 69 / 116 | 28 / 82 / 121 |
| distinct place nouns | 38 | 39 |
| hops with dialogue | 92 | 32 |

Passage to passage both runs are almost entirely new text and neither revisits an earlier passage (nearest-earlier cosine 0.18 for both). Qwen has a few more coarse topics at every threshold. The place counts are equal and the places are not: Astra's are kitchen (87 of 150 hops), door (85), window (61), car, stairs, house, office, bus, bedroom, hall, flat, garden, landing. Qwen's are city (110), server (42), sector (37), spire, council, corridor, basement, deck, tower.

## What the run did

It went backward, coherently. First-line weekdays over hops 18 to 30: Thursday, Wednesday, Tuesday, Sunday, Friday, Wednesday, Monday, Saturday, Monday, Wednesday, Monday, Sunday, Saturday; hops 65 to 71: Monday, Sunday, Friday, Monday, Sunday, Friday, Monday. The story's clock runs in reverse a day or a few days at a time, which is what Astra's causal-BEFORE rule tried and failed to get from Qwen.

Where it went: Mara at the lighthouse with her father's logbooks and a biscuit tin of teeth (hops 1 to 10), a woman looking at flats over a sandwich at her keyboard (11), shopping bags and a sister (21 to 31), a hospital road and Denise (41 to 60), a clock above the cooker seven minutes slow (61), and from hop 71 to 150 Elsie and Martin: the kettle by the sound of the side gate, curtains in the spare room, the good cups, a tissue in Martin's blue shirt, a letter folded signature first, Mr Bell asking Martin to stay a moment, rain through the scullery window. One household for the last eighty hops. Elsie 215 mentions, Martin 213. Martin was the odd-hop name in Astra's `json_page` run; Ruth and Mara recur from there too.

Register: English domestic realism (kettle, scullery, cooker, carrier bag, flat, the afternoon programme), dialogue in 92 of 150 hops, 259 words a passage. Qwen's register from the same seed is a cyberpunk city with a council and a starship. The seed's lighthouse holds Astra for about ten hops; after that the prior decides, and Astra's prior for "what came before" is a kitchen.

## Reading

Diversity depends on which diversity. On vocabulary and on the number of coarse concepts, Qwen's BEFORE is the more diverse run by every measure here, and not narrowly. On non-recurrence both are complete over the window (Qwen's T=0 run froze at 247; Astra is sampled and cannot freeze exactly). On coherence Astra is the only run that actually goes backward.

Astra's 150 passages are combinatorial diversity inside a fixed palette: 2,764 words, one house, two people, every passage new. Astra's causal-BEFORE rule on Qwen reached a similar vocabulary size (2,867 at 150 hops) by the opposite route, crawling with 42 percent Jaccard to the previous hop. Same count, different mechanism, and the count alone would not tell you which.

## To 300

Continued from hop 150's exact output as `astra_json_prev_orig_ext`, 150 more hops, same settings, no refusal, no wall, no recurrence. 60,002 in, 59,735 out, 141 reasoning tokens, $3.59; $7.07 for the 300.

The house is the basin. Kitchen in 107 of hops 151 to 300 (87 of the first 150), door 87, window 63, hall 43, landing 30, stairs 29. The cast changes the way a life read backward changes: Martin holds to about hop 190, then Arthur appears (14 mentions in hops 181 to 195, 54 in the next fifteen) and holds to 285, and Janet arrives at 300 with a cake in a tin Elsie gave her at Christmas. Read forward from 300, it's a marriage, a move (boxes marked KITCHEN, the milk cancelled on Friday, a card forwarded from the old address eleven years on), a widowhood, and a son. Era markers: telephone in 62 hops, television 18, a milk float, one 1986.

Vocabulary, hops 151 to 300 on their own: 39,524 tokens, 2,393 types, TTR 0.061, 17 percent rare, mean Zipf 4.29. Over all 300: 78,703 tokens, 3,374 types, TTR 0.043, Heaps 0.424. New types per 50-hop block: 1778, 621, 365, 274, 212, 124. The last fifty passages, 13,000 words, brought 124 words the run had not used. Qwen's blocks over its 250: 2974, 1301, 715, 509, 539, and 6,038 types at 88,201 tokens. Per-hop novelty is unchanged (Jaccard to previous 0.114, nearest-earlier cosine 0.200): every passage still new, from a palette that has stopped growing.

## Open

- The same 150 at effort high: does reasoning widen the palette or tighten it.
- Qwen under the reworded rule on Cerebras, for a matched-rule comparison, 10 minutes and cents.
- A no-water seed on both, for the seed-motif question.
