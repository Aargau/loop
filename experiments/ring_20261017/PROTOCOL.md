# The ring: a synchronous cellular automaton of text cells

Frozen 2026-10-17 before any run. Justin's concept (fleshed out with an Opus 5.5 context over lunch): N cells on a ring, every cell updated at the same time, each seeing its own text and the last sentence of its two neighbours. The 1-D cellular-automaton version of the memoryless loop, and the first design in this project where the Class 4 question (localized structures that travel and interact) has a substrate with locality and a synchronous update.

## Design

`ring.py`. Each hop, for every cell i, the harness builds `{"rule", "left": last sentence of cell i-1, "text": cell i, "right": last sentence of cell i+1}` (indices mod N) and calls the model once with that object as the only user message; the returned text field is cell i's new text. All N calls read hop t-1 and all N results are written together.

Rule (`rule.txt`): "Return this JSON object with the rule field unchanged and the left and right fields removed. The text field holds a new version of the passage in exactly 60 words. Keep what matters of your own text. Let the left and right passages touch it: something from one or both may enter, alter, or displace what is there."

Design choices carried from the concept: neighbours show only their last sentence (a thin edge, so one cell cannot copy another whole); a fixed word count (logged, not enforced; no model here counts reliably, and Justin's call is that variable counts may induce interesting behaviour); the touch clause is permissive, not compulsory (a cell may hold until a neighbour's edge disturbs it).

Seeds (`seeds/`): every cell gets the plain passage (a kitchen, Agnes, a kettle, twenty past seven; 60 words) except cell 0, which gets the disturbed passage (a mill burning at night, Tobias Reel, a bell, a horse, lit shingles under an arch; 60 words). Distinct nouns and a name in each so provenance can be tagged.

Pilot: Cerebras `qwen-3.8-27b`, T=0, seed 42, reasoning off, 600 output tokens, 40 hops, rings of 7 and 8. Parity is a variable: with a synchronous update on a symmetric neighbourhood, an even ring admits a perfect period-2 checkerboard and an odd ring frustrates it, so a model that wants to alternate must carry a defect on an odd ring. Later arms, on Justin's word after the pilot: frontier models (sampled), and a heterogeneous ring with one model per cell.

## Measures (`ring_score.py`)

Provenance in three layers, each tagged by the cell where the unit first appeared: exact 4-grams (copies; die under paraphrase); distinctive content words and capitalised names (survive paraphrase while the word does); and, tag-free, symmetry: cells equidistant from cell 0 are mirror images until the disturbance reaches them, so the first hop at which a mirror pair differs is the disturbance's arrival. Also per cell: freeze hop; share of 4-grams copied from each neighbour's previous text and kept from its own; whole-ring exact recurrence. The space-time diagram (`spacetime.svg`): one row per hop, one column per cell, colour = origin cell of the dominant distinctive words, a bar for the share copied from each neighbour, a dot where a cell is unchanged. Gliders would be diagonal streaks, fixed points vertical stripes, mixing noise.

## Predictions on record (Cerebras Qwen pilot)

1. Every cell freezes into its own fixed point within 8 hops and ignores the edges: vertical stripes, Class 2; the ring state recurs exactly by hop 12.
2. Cell 0's words reach cells 1 and N-1 by hop 2 and go no further than distance 2 before the cells freeze; mirror pairs at distance 3 or more never diverge.
3. Copied 4-grams from neighbours average under 5% of a cell's 4-grams; what crosses is a name (Tobias, Agnes) or a noun (bell, kettle), not a sentence.
4. Word counts drift outside 50 to 70 in at least a quarter of cells by hop 10.
5. Parity makes no visible difference at T=0 on Qwen, because nothing alternates; the odd/even test is for the frontier arms.
Falsified by diagonal streaks persisting more than 5 hops, by cell-0 words arriving at distance 3 or more, or by a ring that never freezes.

## Pilot result (Cerebras Qwen, T=0, rings of 7 and 8, 40 hops, same night)

Mechanism, exact: at hop 1 every plain cell kept its whole kitchen text and appended its neighbour's edge verbatim ("By the time the bell answered, the roof had gone and the river was carrying lit shingles under the arch."); that sentence became the cell's own last sentence, so the next cell out saw it as its edge at hop 2 and appended it; and so on, one cell per hop in both directions, the two fronts meeting at the antipode (cell 4 at hop 4 on the eight-ring, cells 3 and 4 at hop 3 on the seven-ring). A single sentence travelled at one cell per hop as a verbatim copy: a soliton, the thin edge carried whole rather than touching anything. Cell 0 received the kitchen's edge "The kettle began to tick." prepended at hop 1 and "The kettle began to tick again." appended. When the fronts met nothing new was made: every cell ended in the same mill sentence, every edge was identical, and the ring froze on one uniform 84-word kitchen-plus-bell text with cell 0 the lone defect ("The kettle ticked. The mill burned. ... The kettle began to tick again.", 64 words). Freeze hops [4, 3, 7, 6, 5, 4, 3] and [4, 3, 8, 7, 6, 5, 4, 3]; whole-ring exact recurrence from hop 8 (N=7) and 9 (N=8); mirror pairs diverged two hops after the front reached them (3, 4, 5), the rule's left-right asymmetry as a measurable lag. Copied 4-grams from neighbours (new 4-grams only) averaged 0.049 and 0.052. Word counts 57 to 83 against the rule's 60. No malformed hops, no errors.

Predictions: 1 held (every cell frozen by 8; recurrence by 8 and 9). 2 failed in the interesting direction: cell 0's words reached the antipode, distance 3 and 4, at one cell per hop, before the freeze. 3 half held: the copied share is under 5%, but what crossed was a whole sentence, not a name or a noun. 4 held (six of seven cells at 79 to 84 words by hop 10). 5 held: parity made no difference at T=0; the seven- and eight-rings are the same picture with one more column.

Class 2, with a transient of about N/2 hops and one soliton that saturated rather than annihilated. On Qwen at T=0 "let them touch it" is executed as "append the edge"; the question for the sampled frontier arms is whether a model that paraphrases rather than appends turns the soliton into something that changes as it travels.

## Second pilot: Justin's disturbed seed (same night)

Seed (`seeds/disturb_tarnok.txt`, Justin, stream of consciousness, perturbing quiet, period, gender, scope, verisimilitude and indoor/outdoor at once): "The battle raged on. Tarnok hefted his crude bronze axe, sensing which way he should search for the usurper. A small knot of struggle around a black flag painted with a yellow skull made his decision for him." Same plain seed, rule, model and settings; rings of 7 and 8.

Result: every cell froze at hop 1; whole-ring recurrence from hop 2; the disturbance died at distance 1. Cells 1 and N-1 absorbed the skull-flag sentence but inserted it before their own closing line ("...twenty past seven. A small knot of struggle around a black flag painted with a yellow skull made his decision for him. The kettle began to tick."), so their edge, the last sentence, stayed the kitchen's, and the next cells out saw nothing new. Cell 0 wrapped the battle in the kitchen's closing line on both sides ("The kettle began to tick. The battle raged on. ... The kettle began to tick.") and held. Copied 4-grams 0.007; parity irrelevant.

Reading: with the mill seed the edge read as a scene's ending and was appended, becoming the next edge and travelling one cell per hop; with the battle seed it read as a non-sequitur and was quarantined mid-text, and the kitchen kept its own ending. On Qwen at T=0 a disturbance travels only when it is register-compatible with the cell it enters; perturb more and it goes less far. The frontier arms should run both seeds, since propagation is partly a question of register.

## Frontier rings on Justin's seed (2026-10-17, scored; reading added 2026-10-28)

Runs: Mythos 5.1 (print mode) on rings of 7 and 8, GPT-6 Astra (Codex) on 7, Gemini 4 Argon on 7; 40 hops, 60-word rule, provider default sampling. Scores in `runs/*_tarnok_n*/score.json` and `spacetime.svg`.

Nothing froze and nothing recurred: with sampling every cell changes every hop (freeze hop 40 means never), mirror pairs diverge at hop 1, and the ring never repeats a state. So the questions become where cell 0's words go and whether they stay.

| run | first hop with cell-0 words, per cell | cell-0 share of distinctive words at hop 40, per cell | reading |
|---|---|---|---|
| Mythos n7 | 1, 1, 3, 5, 5, 5, 1 | 0.69, 0.36, 0.16, 0.24, 0.19, 0.19, 0.38 | domesticated: the battle reaches the antipode by hop 5 and is absorbed as a sentence in the kitchen ("Boys struggled over a skull flag"); cell 0 keeps Tarnok, every other cell is Agnes and the kettle |
| Mythos n8 | 1, 1, 1, 4, 3, 2, 1, 1 | 0.65, 0.15, 0, 0, 0, 0, 0, 0.05 | domesticated harder: words arrive everywhere by hop 4 and are gone from six of eight cells by hop 40 |
| Astra n7 | 1, 1, 2, 1, 3, 2, 1 | 0.47, 0.45, 0.41, 0.42, 0.06, 0.17, 0.24 | invaded: by hop 40 cells 0 to 3 and 6 all open "Bronze rang through the battle. Tarnok hefted his axe, searching beyond fallen horses for yellow on black" and then go to the cups upstairs; a battle domain of five cells with the kitchen inside it |
| Argon n7 | 1, 1, 25, 24, 23, 22, 1 | 0.50, 0.20, 0.04, 0.04, 0.04, 0.05, 0.48 | quarantined at distance 1 for twenty hops, then a trickle from the right (hops 22 to 25); cell 0 fuses the two registers ("the bronze pot of war began to boil. Tarnok counted two axes, keeping only one. Softly, she counted two cups, keeping only one") |

Mean share of new 4-grams copied from a neighbour: Mythos n7 0.64, Argon 0.58, Astra 0.23, Mythos n8 0.23; Qwen at T=0 on the same seed 0.007. The frontier models take neighbour text by the phrase and rewrite the rest. Mythos's own fixed-point sentence from the informed loop, "She did not turn.", appears 149 times in the n7 log, written into the kitchen cells unprompted: the model's attractor from one experiment surfacing in another.

Parity: no checkerboard on either ring; Mythos n8 domesticates faster than n7, which is one sample and not a parity effect on this evidence.

Predictions 2 and 3 of the pilot, carried to the frontier: cell-0 words reach the antipode in every run (2 fails again, in the same direction), and what crosses is phrases and the name, not sentences (3 holds for Astra and Mythos n8, fails for Mythos n7 and Argon, where whole clauses travel). The register-compatibility reading from the Qwen second pilot does not carry: three of four frontier rings let the battle into the kitchen; what differs is whether it stays.
