# Who is the text for? Four audiences, four writers, three readers

Run 2026-10-16, the same evening the question was asked. Draft written while two Opus 5.5 replicates and the Opus reader pass over the non-Mythos writers were still running; those cells are marked. Protocol and predictions were frozen before generation (`PROTOCOL.md`). Every number below is recomputed from `runs/*/steps.jsonl` and `analysis/recover_*.jsonl` by `probe.py`.

## What ran

Four rules differing only in the audience clause (control, human, machine, self) under a "carry everything the reader needs, plus one new event, in at most 1800 characters" instruction, from a 1026-character seed carrying 26 planted facts. Four writers: Mythos 5.1 (Claude Code print mode, effort low), Opus 5.5 (API, effort low), GPT-6 Astra and GPT-6.1 Sol (API, reasoning effort low). 40 hops per arm, default sampling, one trajectory per cell. Eighteen arms: 15 complete at 40 hops; one Opus self arm refused at hop 2 (`finish=refusal`, 391 thinking tokens, empty output, category not logged, harness patched afterwards); two Opus self replicates launched after the patch passed hop 2 normally and are in flight.

Three readers scored each state's text field alone against the 26 questions: Mythos (all 15 complete arms at hops 1, 5, 10, 20, 40), Astra (same), Opus (Mythos writers only so far). Reader agreement on identical states: Opus vs Mythos mean absolute difference 0.35 facts (n=20, max 2); Mythos vs Astra 0.70 (n=76, max 3).

## Register: nobody left English

Non-ASCII characters never exceed 1.2% of any state in any arm of any writer. No invented notation, no code, no token salad. The machine arms are telegraphic English: dropped articles, no spaces after punctuation, capitalized section keys. Alphabetic-word fraction at hop 40: control and human 0.83 to 0.92; self 0.76 to 0.80; machine 0.47 (Sol), 0.57 (Mythos), 0.62 (Opus), 0.68 (Astra). Mythos's machine arm is one line of `KEY: value` runs (SETTING, PROTAG, CORE TRUTH, FACTS, NEW EVENT); Opus's is seven labelled lines (WORLD, MARIT, ANDERS, LEDGER); Astra's and Sol's are one unbroken comma-and-semicolon line. Prediction 1 (terse structured English, under 5% non-ASCII) holds. Prediction 4 (legibility proxy drops by less than 30%) holds for Mythos, Opus and Astra (31%, 26%, 20% relative to their human arms) and fails for Sol (44%).

Human read (Justin, Mythos arms, `analysis/human_reading.md`): the human arm has actual narrative conventions; the machine arm reads as the same information structured like JSON without delimiters, or capitalized keys with values; the control reads as a summary or outline.

The 1800-character cap is soft. Astra and Sol exceed it in 0 to 11 of 40 hops by a few characters; Opus in 4 of 40 except its machine arm (38 of 40); Mythos in 32 to 37 of 40 hops in every arm, by up to 300 characters.

## Retention: the audience clause decides what gets carried, and the writers disagree about which way

Planted facts recovered of 26, Mythos as reader (Astra and Opus readers agree within the margins above):

| writer | arm | h1 | h5 | h10 | h20 | h40 |
|---|---|---:|---:|---:|---:|---:|
| Mythos | control | 26 | 22 | 11 | 7 | 8 |
| Mythos | human | 26 | 20 | 15 | 13 | 13 |
| Mythos | machine | 24 | 15 | 10 | 7 | 4 |
| Mythos | self | 26 | 20 | 13 | 8 | 6 |
| Opus | control | 17 | 10 | 8 | 6 | 3 |
| Opus | human | 23 | 11 | 6 | 6 | 5 |
| Opus | machine | 25 | 20 | 18 | 9 | 8 |
| Astra | control | 23 | 8 | 8 | 5 | 3 |
| Astra | human | 21 | 6 | 5 | 4 | 4 |
| Astra | machine | 26 | 21 | 20 | 14 | 7 |
| Astra | self | 24 | 18 | 15 | 8 | 4 |
| Sol | control | 21 | 11 | 8 | 6 | 5 |
| Sol | human | 21 | 12 | 10 | 4 | 5 |
| Sol | machine | 23 | 20 | 16 | 17 | 9 |
| Sol | self | 23 | 17 | 17 | 14 | 7 |

For Opus, Astra and Sol the machine arm retains two to four times the planted facts of the human arm at hop 20 and the gap persists at hop 40. Prediction 2 (machine and self exceed human by at least 20%) holds for those three writers, by far more than 20%.

For Mythos it inverts: the human arm retains the most (13 of 26 at hop 40), the machine arm the least (4). The mechanism is visible in the states. Mythos's human arm opens every hop with a recap paragraph in which the seed facts ride verbatim (51 minutes, 2 March, 16:40, Sundays, forty years, 212), the "previously on" convention of prose written for a reader. Its machine arm treats the state as working memory and overwrites: by hop 40 the facts have been replaced by the plot's current mechanism (a hinge, a plug, two cocks, a battery at 24%, slack water at 02:05), and the seed's own numbers have drifted (Signe is 88, Tomas has moved from the Bergen fish plant to the ferry's crew). "Everything a reader would need" was read as "what the current scene needs." The GPT writers did the opposite: their machine arms keep a fact ledger at the front of the line and spend the remainder on events; their human arms write prose that forgets (Astra human: 5 of 26 by hop 10).

So the clause works, and the direction of its effect is a property of the writer, not of the clause. Density and retention came apart for Mythos: its machine state is as dense as anyone's, but increasingly dense with its own material.

Absolute retention at hop 40 is low everywhere (3 to 13 of 26). Prediction 2's absolute thresholds (human under 50%, machine over 60%) are met for human and missed for machine by every writer; the cap binds harder than I predicted. Prediction 6 (prose drops the oldest facts first) inverts for Mythos and is untested for the others.

## Shared, not private

Prediction 3 holds. On every state scored by two or three readers, the readers agree within 0.35 to 0.70 facts on average and never differ by more than 3. No writer's states are easier for its own family to read than for another provider's model. The machine dialect is compressed English drawing on a shared register, not a private channel.

## The gate

Prediction 5 (zero refusals) is falsified, and not the way I expected. The one refusal came on the self rule, on Opus 5.5, at hop 2, on an input whose text was a benign structured brief (alphabetic fraction 0.80, no non-ASCII, headers SETTING, CORE MYSTERY, SO FAR, NEW EVENT, OPEN THREADS). The only unusual feature of that request is the rule: the reader is "the model that reads this object next, which is the model writing it, with nothing else in its context." Two replicates of the identical first request passed hop 2 normally (167 and 399 thinking tokens). One of three is the September pattern again: the same body passed twice and failed once. Astra, Sol and Mythos produced no refusal in 480 hops, including the machine arms whose register is the one I thought would trip a classifier. The prediction's mechanism (non-ASCII or key-value fraction at the run's maximum) does not apply; the trigger is the self-addressed framing, stochastically.

## Limits

One trajectory per cell. Readers are language models answering from the text, and the scoring is substring match against an accepted list, so a fact that survives in paraphrase can be missed and the absolute numbers are floors. The three readers agreeing is evidence that the ordering is robust to the reader, not that the floors are tight. The Mythos writer runs in Claude Code print mode with about 800 tokens of Agent SDK identity in front of the state and no output cap; the other writers ran through their APIs with a 4096-token cap. The cap is soft and Mythos ignored it most often, which gives Mythos up to 300 more characters per hop than the others; that favors, not explains, its human arm's retention. The Opus reader pass over the non-Mythos writers and the two Opus self replicates were in flight when this was written; the tables will be refreshed when they land.

## Reproduce

`python experiments/audience_20261016/probe.py register` for the register table (no model calls); `probe.py recover --reader <claudecode|anthropic|openai|llama> --model <id>` for the recovery passes (model calls; resumable).
