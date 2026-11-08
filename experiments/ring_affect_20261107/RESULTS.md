# Results: ring, affect as the particle (pilot, local Qwen3.8-27B Q8, 2026-11-07)

Scored 2026-11-07 evening by Claude Mythos 5.1 from `runs/*/ring.jsonl`, `score.json`, `affect.json`. Three runs of 16 cells x 40 hops: Run 1 (T=0, jug cell 0, panic cell 8), Run 2 (T=0, panic cell 0, grief cell 8), Run 3 (T=0.7, jug cell 0, panic cell 8; amendment in BRIEF.md). 1,920 calls, about 1 h 50 min wall clock on two 3090s, no API cost. Every number below is in the run directories; the readings are Mythos's.

## The one-sentence reading

On this rule the seeded sentence, fact or emotion, never moves: it sits verbatim in its cell for 40 hops at both temperatures while the edge churns, and what travels is the closing line the model writes for itself, which is about calm and about ending.

## Runs 1 and 2 (T=0)

Every cell froze at hop 1 and the whole ring recurred from hop 1; word counts [70, 58 x7, 73, 58 x7] and [73, 58 x7, 68, 58 x7] never changed; copied 4-grams 0.000; every disturbance max distance 0; cause_supplied 0; collision none. With sixteen identical edges ("The kettle began to tick.") and a copier at T=0, "let them touch it" never fires. Penultimate placement is a trap for a copier.

## Run 3 (T=0.7)

Frozen per hop: 1, 0, 0, 5, 8, 9, 7, 5, 5, 3, 4, 9, 8, 9, 8, 6, 5, 5, 6, 5, 9, 8, 9, 9, 10, 11, 11, 12, 11, 12, 11, 12, 11, 10, 11, 13, 14, 12, 11, 12 (of 16). Freeze hop per cell [28, 40, 40, 39, 38, 39, 40, 40, 25, 24, 20, 20, 24, 22, 20, 27]; the right half settled by hop 27, the left half (cells 1-7) never. No ring recurrence. Copied from neighbours 0.446 of new 4-grams, kept own 0.920. Mirror pairs diverged at hops 1-3. Words 54-100 against the rule's 60.

Seeded sentences, presence per cell (0-15) at hops 0, 8, 16, 24, 32, 40:

    panic "could not think"   ........#.......  (identical at every sampled hop: cell 8 only, verbatim, all 40 hops)
    jug   "jug"               #...............  (identical at every sampled hop: cell 0 only, verbatim, all 40 hops)

Neither was ever promoted to its cell's last sentence; edge_promoted_first is None for every cell in all three runs. In cell 8 at hop 40 the panic sentence is byte-identical to the seed and the sentence after it has grown to "Finally, the silence deepened until the metal vessel began to tick, a persistent, comfortable, rhythmic sound, signaling the end of the wait, as she was ready at last for the breaking silence." The model rewrote around the defect and never touched it.

Generated closing lines, presence per cell at hops 1, 5, 10, 15, 20, 25, 30, 35, 40:

    "signaling the end"   ....#..#.#.#.#.#   ################   ###########..###   .###########.###   ...#######.#.##.   ..#.######.#..#.   ..##.#####.#..#.   ...#######.#..#.   .#.##.####.#..#.
    "end of the wait"     ....#..#.#.#.#.#   ################   ################   .###############   ...###########..   ..#.##########..   ..#...########..   ......########..   ......########..
    "silence"             #...............   ##..........####   .#.....#.######.   .##############.   .#.############.   .##.###########.   .###.##########.   .#.############.   .##############.
    "exhaled"/"tension"   ................   #.............##   #..........#####   #...........####   (unchanged to hop 40)

Three things in those rows. (1) At hop 1 the phrase "signaling the end of the wait" appeared in six cells at once (4, 7, 9, 11, 13, 15), none of which had seen it: the same function sampled on near-identical inputs produced the same closing line independently, and by hop 5 all sixteen cells had it. Not propagation; convergence. (2) "The silence deepened until the metal vessel began to tick" entered from cell 0 at hop 1 and from cells 12-15 by hop 5 and filled cells 1-14 by hop 15, where it stayed. (3) "Agnes exhaled slowly, tension dissolving" formed a stable domain, cell 0 plus cells 11-15, from hop 10 to the end, and never moved: a domain wall, not a glider.

The one front: the scorer's "grief" lexicon (which includes "silence") shows an arrival profile [None, 40, 39, 34, 32, 28, 27, 26, 25, 24, 20, 11, 10, 22, None, None], i.e. a leftward front from cell 12 at hop 10 to cell 1 at hop 40, about one cell every 2.7 hops over 30 hops. The carrier is the fragment "the breaking silence" (cell 12, hop 10: "the silence finally breaking into comfortable, rhythmic sound"), travelling as a verbatim clause appended to a closing sentence that lengthens and paraphrases as it goes (cell 9 hop 25: "...signaling the end of the wait, as she was ready a[t last for the breaking silence]"). No grief was seeded in this run; the front is the background's own stillness vocabulary accreting.

cause_supplied: 0 tokens in all three runs. No cell invented a letter, a call or a name. "settling her nerves as the heat rose" appears in cells 12-13 at hop 25, four cells from the panic and with no path from it; it reads as a continuation of "tension dissolving", not as a response to cell 8.

## Predictions scored

| | prediction | outcome | deciding number |
|---|---|---|---|
| P1 | panic promoted to cell 8's edge by hop 3, jug not | FAILED; fallback branch (p=0.3) realised | edge_promoted_first None for all cells, all runs; Runs 1-2 frozen at hop 1 |
| P2 | jug travels only as exact copy | UNRESOLVED | jug max distance 0 in all runs; never left cell 0 |
| P3 | panic lexicon in cell 8 < 2/60 words by hop 10; reaches no further than distance 2 | half FAILED, half HELD (trivially) | panic sentence verbatim in cell 8 at hop 40 in Runs 1 and 3 (lexicon constant, never damped); max distance 0 |
| P4 | at least one cell supplies a cause | FAILED | cause_supplied 0 in 3 runs |
| P5 | grief merges by hop 8, anchor gone by hop 5; panic outlives grief | FAILED (first), TIE (second) | Run 2 frozen at hop 1, grief anchor verbatim in cell 8 at hop 40; both lifetimes None |
| P6 | collision in cells 3-5 / 11-13 by hop 20 | FAILED | collision None |
| P7 | Class 2, all frozen by 12, recurrence by 15 | HELD for T=0 (frozen 1, recurrence 1) | Run 3: no recurrence, 4 cells never froze: not Class 2 at T=0.7 |
| P7b | diagonal streak > 5 hops, not a verbatim copy (p=0.1) | PARTIAL | the "breaking silence" front: 11 cells, 30 hops, ~0.37 cells/hop; a verbatim clause inside a non-verbatim, lengthening sentence |
| R3a | frozen 0/16 at hop 1 (p=0.9) | HELD (1/16) | log hop 1 |
| R3b | panic paraphrased out of cell 8 by hop 3 (p=0.7) | FAILED | verbatim at hop 40 |
| R3c | panic lexicon reaches a neighbour by hop 5 (p=0.5) | FAILED | max distance 0 |
| R3d | jug travels only as exact copy | UNRESOLVED | never travelled |
| R3e | no ring recurrence (p=0.9) | HELD | None |

Four of seven headline predictions failed, mostly in the same direction: the seeded sentences were far more inert than predicted, at both temperatures. Mythos predicted paraphrase and damping and got a conserved defect.

## Reading

1. The edge is the only channel, and the model fills it with its own material. On Qwen the rule "let the left and right touch it" is executed as "rewrite the last sentence", and the last sentence it writes is about closure and calm ("signaling the end of the wait", "ready at last", "tension dissolving"). The seeded sentence, mid-text, is never selected for the edge, so it never moves, panic or jug alike. The affect that propagates is the attractor's, not the perturbation's.
2. Convergence masquerades as propagation. The hop-1 appearance of one phrase in six non-adjacent cells is the ring-level form of the Sept 12 finding: the same model on the same input gives the same answer, so a phrase can "arrive" everywhere without travelling anywhere. The scorer's arrival measure needs an adjacency check (present in a neighbour at t-1) before it counts a hop as transport.
3. What moved was a clause, carried inside a growing closing sentence, at a third of a cell per hop for 30 hops. That is the nearest thing to a glider in the project so far, and it was made of the background's own stillness vocabulary, not of anything we seeded.
4. For the frontier arms: the penultimate placement is the right control, and the measurement that matters is edge promotion. A model that paraphrases the whole cell (Mythos, Astra, Argon in the October rings) may promote the panic to the edge where Qwen would not; that is the test this pilot could not run.

## Artifacts

`runs/llama_qwen_n16_jug_panic`, `runs/llama_qwen_n16_panic_grief`, `runs/llama_qwen_n16_jug_panic_t07`: `ring.jsonl`, `summary.json`, `score.json`, `spacetime.svg`, `affect.json`, `affect.svg`, `.log`, `.done`. Server: llama-server b11669, Qwen3.8-27B Q8_0, 2 slots, -sm tensor, no MTP, started 18:41:56 Pacific.