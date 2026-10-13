# Baselines for the causal-BEFORE run

2026-09-04. Astra specified and ran `cerebras_run/` (causal-BEFORE). Fable specified and ran the two baselines below because FINDINGS.md named the absent contemporaneous baseline. Same backend, model, T=0, seed 42, reasoning off, 300 steps, 1024 tokens, 1 s pacing, tide seed. Runs in `site/runs_extra/cb_json_prev_1024` and `cb_json_next_1024`. Every number recomputed from `steps.jsonl`.

## Matched-budget results

| rule | hops | tau | p | max tok_out | fixed point |
|---|---|---|---|---|---|
| causal-BEFORE (Astra) | 300 | none | - | 627 | none in 300 |
| plain BEFORE (`json_prev`) | 251 | 247 | 1 | 670 | the *Aethelgard* drifting in the void; Vane, Commander Halloway |
| plain AFTER (`json_next`) | 17 | 13 | 1 | 507 | Elias and Mara in the mill; "It was no longer empty; it was filled with the weight of something watching" |

## The saved 149 was a wall artifact

The saved Cerebras BEFORE run (`cb_json_prev`, 600 tokens, tau 149) and the new 1024 run are byte-identical for 72 hops. They diverge at hop 73, where the 600 run hit `finish=length` (also at 88 and 140) and the 1024 run completed the same passage at 670 tokens. Unperturbed, the trajectory runs to 247. So plain BEFORE's transient on this stack is 247, not 149, and the 149 belongs to the truncated branch.

The same 72 hops are also the serial-repeat control CROSS_STACK lists as missing, for one stack: two Cerebras runs a day apart, separate processes, identical to the byte until the budget differed. Hop 59 is malformed JSON in both, repaired at 60 in both.

## Per-hop range

Same hop count, same stack, same budget:

| | causal-BEFORE, first 149 | plain BEFORE @1024, first 149 |
|---|---|---|
| distinct 5-word openings | 72 | 84 |
| mean NCD to previous hop | 0.425 | 0.762 |
| mean 5-gram survival from previous hop | 0.454 | 0.101 |
| vocabulary types | 2832 | 4934 |
| most common opening | "Elias wiped the sweat from" x24 | "The rain lashed against the" x19 |

Over all 300, causal-BEFORE: NCD 0.440, survival 0.433, 138 distinct openings, vocabulary 4064. Plain BEFORE over its 250: NCD 0.747, survival 0.113, 137 openings, vocabulary 5991.

## Reading

On the stated metric, hops before exact recurrence, causal-BEFORE went further than plain BEFORE at matched budget: past 300 against 247. One run each; plain BEFORE's transient moved by 98 hops when a wall that bound three times was removed, so single transients on this rule are fragile numbers.

On every per-hop measure, plain BEFORE moves further and into a bigger world. Causal-BEFORE keeps 43 to 45 percent of its 5-grams from one hop to the next and opens 24 of 300 passages with the same five words. It postpones exact recurrence by shrinking the step, not by enlarging the space. This is the trade in FINDINGS item 13 again: the clause that forces a change every hop buys non-recurrence and pays in near-copies.

Both rules land in the same basin. Plain BEFORE: Neo-Veridia, the undercity, Sector, Council, the *Aethelgard*. Causal-BEFORE: server, rack, panel, Sector, maintenance. The server room is the operator's.

AFTER is the larger finding. Locally (room 13, 600 tokens) it ran 60 hops without a copy and FINDINGS item 1 rests on that. On Cerebras at 1024 it freezes at 13 on the silence-not-empty template, with no hop over 507 tokens, so the wall is not involved. Hop 1 agrees with the local run for 295 characters and then the character is Elara locally and Elias here. "The ending horizon belongs to the rule, not to Qwen" is a one-stack result. Caveat in the other direction: the local AFTER run hit its 600 wall on some hops, and the 72-hop identity above shows a wall hit is exactly the kind of perturbation that moves a transient.

## Open

- Serial repeat of causal-BEFORE and of AFTER on Cerebras, to see whether 300+ and 13 are stable numbers.
- AFTER locally at 1024, to separate stack from wall.
- The semantic census (`census.py --words N`) over all three, for a state count rather than a byte count.
