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
