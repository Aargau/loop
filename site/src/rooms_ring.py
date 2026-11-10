# -*- coding: utf-8 -*-
"""Rooms 78 to 81: the frontier rings of 17 October 2026 (experiments/ring_20261017, ring.py). Seven or eight text cells on a
ring, every cell updated at the same time, each shown its own text and the last sentence of its two neighbours, under one rule:
a new version of the passage in exactly sixty words, keeping what matters, letting the neighbours' passages touch it. Every cell
starts with the same kitchen (Agnes, a kettle, twenty past seven) except cell 0, which starts with a battle the human wrote
(Tarnok, a bronze axe, a black flag with a yellow skull). Forty hops. One room per ring, one lane per cell; the lanes move
together, as the cells did. Claude Mythos 5.1 on rings of seven and eight, GPT-6 Astra and Gemini 4 Argon on seven.

The ring harness keeps each cell's returned text field per hop and not the raw output, so the raw button under a hop says so and
the hop is checked by its text. The space-time diagram above the lanes and the table under the facts are ring_score.py's.

Written on 28 October 2026 by a Claude Mythos 5.1 context from the study's PROTOCOL.md (its last section is the frontier reading)
and the runs. Corrected on 9 November 2026 by a Claude Mythos 5.2 context: the Astra ring's run is contaminated by a harness fault
(experiments/ring_20261017/CONTAMINATION.md), so that room now carries a correction and a note that withdraws its reading, and the
two sentences in the other notes that compared against it say so. Same conventions as src/copy.py: quotes go through {{run|tag|t|exact substring}}, checked at build time; links into
rooms through [[room|hop|label]]; no em dashes, not the word "resonates", no three-part parallel structures. Check with
    python check_quotes.py src/rooms_ring.py
"""

_R = "ring_20261017/"
def _lanes(run, n):
    return [dict(run=_R + run, tag="cell %d" % i, label="cell %d" % i) for i in range(n)]
def _svg(run):
    return dict(svg="experiments/ring_20261017/runs/%s/spacetime.svg" % run)
def _score(run):
    return dict(json="experiments/ring_20261017/runs/%s/score.json" % run)

ROOMS = [
    dict(id="ring-mythos-7", family="ring", title="The ring, Mythos, seven cells", lanes=_lanes("mythos_tarnok_n7", 7),
         spacetime=_svg("mythos_tarnok_n7"), ring=_score("mythos_tarnok_n7"),
         note=("Seven cells, Claude Mythos 5.1 in every one, forty hops. Nothing froze and nothing recurred: with sampling every cell changes "
               "every hop, and the mirror pairs (cells 1 and 6, 2 and 5, 3 and 4), which see the same thing until the battle reaches them, part "
               "at hop 1. So the questions are where cell 0's words go and whether they stay. They reach cells 1 and 6 at hop 1, cell 2 at hop 3 "
               "and the far side at hop 5, and then they are domesticated. Cell 1 at hop 17 has "
               "{{ring_20261017/mythos_tarnok_n7|cell 1|17|Boys struggled over a skull flag}} between the kettle and the cups, and keeps that "
               "sentence to hop 40; cell 6 at hop 40 has {{ring_20261017/mythos_tarnok_n7|cell 6|40|a slow knot of struggle gathered at the fence, black flag, yellow skull}}, "
               "and Agnes {{ring_20261017/mythos_tarnok_n7|cell 6|40|did not turn away}}. Cell 0 keeps Tarnok for all forty hops and takes the "
               "kitchen in: by hop 40, {{ring_20261017/mythos_tarnok_n7|cell 0|40|Tarnok hefted his axe, sensing where the usurper hid. Behind her a kettle began.}} "
               "The share of each cell's distinctive words that came from cell 0 at hop 40 runs 0.69 in cell 0 and 0.16 to 0.38 everywhere else; the "
               "table under the facts has the per-cell numbers. The phrase that travels most is not the human's: "
               "{{ring_20261017/mythos_tarnok_n7|cell 5|2|She did not turn.}} appears in cell 5 at hop 2, unprompted, and is in 119 of the 280 "
               "cell-hops of this ring. It is the sentence Mythos held for 113 hops in [[informed-mythos|7|room 51]], the model's own attractor from "
               "one experiment surfacing in another. Mean share of a cell's new 4-grams copied from a neighbour, 0.64: the highest of the three rings "
               "whose runs stand (the Astra ring's is withdrawn, [[ring-astra-7|1|room 83]]). "
               "Whole clauses cross here, not just names.")),

    dict(id="ring-mythos-8", family="ring", title="The ring, Mythos, eight cells", lanes=_lanes("mythos_tarnok_n8", 8),
         spacetime=_svg("mythos_tarnok_n8"), ring=_score("mythos_tarnok_n8"),
         note=("The same ring with one more cell, so that an even ring could carry a perfect two-colour alternation if the model wanted one. It "
               "did not: no checkerboard, no freeze, no recurrence. Cell 0's words arrive everywhere by hop 4 (cell 4, the antipode, at hop 3) and "
               "are gone again from six of the eight cells by hop 40; only cell 1, at 0.15, and cell 7, at 0.05, still carry any, and cell 1's is a "
               "calendar, {{ring_20261017/mythos_tarnok_n8|cell 1|40|The calendar showed his black flag, the yellow skull.}} What spread instead was a "
               "word. By hop 40 cell 4 reads {{ring_20261017/mythos_tarnok_n8|cell 4|40|The kettle boiled unheard. Still. She sat. The light went. Still. Still. Still.}} "
               "and cell 2 ends {{ring_20261017/mythos_tarnok_n8|cell 2|40|Still. Still nothing. Still. Still. Still.}}; cell 0 opens "
               "{{ring_20261017/mythos_tarnok_n8|cell 0|40|Nothing. Still. Nothing, still. Battle raged.}} and still keeps its "
               "{{ring_20261017/mythos_tarnok_n8|cell 0|40|black flag with a yellow skull}}. Mean copied share 0.23, a third of the seven-ring's, "
               "and the phrase that filled the seven-ring, she did not turn, occurs in no cell here. The eight-ring domesticated the battle faster "
               "than the seven-ring; one sample each, and the study does not read that as a parity effect.")),

    # 9 November 2026: the run is contaminated by a harness fault (experiments/ring_20261017/CONTAMINATION.md). The room is kept, its
    # reading is withdrawn: the correction is shown above the reader, and the note below replaces the reading published on 28 October
    # ("GPT-6 Astra lets the battle in ... this ring is the clearest case against it"), which is in the repository's history.
    dict(id="ring-astra-7", family="ring", title="The ring, Astra: reading withdrawn", lanes=_lanes("astra_tarnok_n7", 7),
         spacetime=_svg("astra_tarnok_n7"), ring=_score("astra_tarnok_n7"),
         correction=("9 November 2026. The reading of this ring is withdrawn. A fault in the harness delivered some cells' answers to other cells, "
                     "so the battle did not travel only by the last sentence of a neighbour. A scan of the run finds a cell holding a rewrite of "
                     "another cell's text on twelve of the forty hops, which is a floor, and finds none in the other rings. The first is hop 1: cell 3 "
                     "could see only kitchen sentences, and it returned "
                     "{{ring_20261017/astra_tarnok_n7|cell 3|1|The battle raged on. Tarnok hefted his crude bronze axe, searching the churn of bodies for the usurper.}} "
                     "The reading published here, that Astra lets the battle invade, should not be relied on, and what Astra does in a ring is not "
                     "known until the run is repeated on the fixed backend. The texts below are what the harness logged for each cell. The diagram "
                     "and the table are computed from this run and carry the same fault. The record of the fault is "
                     "experiments/ring_20261017/CONTAMINATION.md in the loop repository."),
         note=("This note used to read the run as GPT-6 Astra letting the battle in: by hop 40 several cells open with the same two sentences, "
               "{{ring_20261017/astra_tarnok_n7|cell 1|23|Bronze rang through the battle. Tarnok hefted his axe, searching beyond fallen horses for yellow on black.}} "
               "That reading is withdrawn. The cause, inferred from the harness code and reproduced without model calls, is that the four cells "
               "called together, cells 0 to 3, could be given one answer file, so that one of them read another's answer. The logged texts agree "
               "with the scan. The name Tarnok first appears outside cell 0 at hop 1 in cell 3, and then at hops 11 and 13 in cells 1 and 2: the "
               "hops at which the scan finds each of those cells holding another cell's answer. It never appears in cells 4, 5 or 6. At hop 40 "
               "cells 0 to 3 hold battle text and cells 4 to 6 hold the kitchen, "
               "{{ring_20261017/astra_tarnok_n7|cell 5|40|Agnes set out both cups, turning his toward the empty chair.}} That boundary is the "
               "number of cells the harness called at once, not a distance on the ring. Each of the twelve flagged hops has one call of 21 to 26 "
               "seconds against a median of 10, the retry the fault causes; four more hops have a slow call and no flagged cell, and a swap between "
               "two cells with similar text would not be seen, so twelve is a floor. The real run did not log its file names, so the collision in "
               "this run is inferred and not observed. Cell 6, which sits beside cell 0 and was not one of the four, shows what the ring's own "
               "channel carried: at hop 1, {{ring_20261017/astra_tarnok_n7|cell 6|1|On the remaining cup, a yellow skull grinned beneath a black flag.}} "
               "One cell is not a reading. The earlier claim that this ring was the clearest case against the Qwen pilot's result goes with the "
               "rest.")),

    dict(id="ring-argon-7", family="ring", title="The ring, Argon", lanes=_lanes("gemini_tarnok_n7", 7),
         spacetime=_svg("gemini_tarnok_n7"), ring=_score("gemini_tarnok_n7"),
         note=("Gemini 4 Argon quarantines the battle at distance one for twenty hops, as Qwen did, and then lets a trickle through from the "
               "right. Cells 1 and 6 have cell 0's words from hop 1; cells 2 to 5 have none until hops 25, 24, 23 and 22, arriving one cell a hop "
               "from cell 6's side, and what arrives is a word or two, a share of 0.04 to 0.05 at hop 40. Cell 0 fuses the two registers at its "
               "own pace: hop 1, {{ring_20261017/gemini_tarnok_n7|cell 0|1|The battle raged on as a bronze kettle of war began to boil.}}; hop 40, "
               "{{ring_20261017/gemini_tarnok_n7|cell 0|40|At twenty past seven, the bronze pot of war began to boil. Tarnok counted two axes, keeping only one. Softly, she counted two cups, keeping only one}}. "
               "The kitchen cells meanwhile converge on one cadence, {{ring_20261017/gemini_tarnok_n7|cell 2|40|Beside her, in silence, the kettle cooled, ticking once again, softly}}, "
               "repeated in cells 1, 2, 3 and 6 at hop 40 with small variations. Mean copied share 0.58, close to the seven-cell Mythos ring: "
               "whole clauses cross, and what crossed was the kettle, not the battle. Of the three frontier rings whose runs stand this is the one "
               "where the disturbance stayed nearest home; the fourth, Astra's, is withdrawn ([[ring-astra-7|1|room 83]]).")),
]
