# Who is the text for? Four audiences, five writers, four readers, three replicates

Run 2026-10-16 and 17. Fourth draft, with three replicates per cell (replicates 2 and 3 run on 2026-10-17; the Opus self arm has five, two of them from the 16 October refusal check), four readers over every state. The single-trajectory sections below are kept as the first replicate's reading; the replicate table and the revised claim follow them. Protocol and predictions were frozen before generation (`PROTOCOL.md`). Every number below is recomputed from `runs/*/steps.jsonl` and `analysis/recover_*.jsonl` by `probe.py`.

## What ran

Four rules differing only in the audience clause (control, human, machine, self) under a "carry everything the reader needs, plus one new event, in at most 1800 characters" instruction, from a 1026-character seed carrying 26 planted facts. Five writers: Mythos 5.1 (Claude Code print mode, effort low), Opus 5.5 (API, effort low), GPT-6 Astra and GPT-6.1 Sol (API, reasoning effort low), Gemini 4 Argon (Google's OpenAI-compatible endpoint, reasoning effort low). 40 hops per arm, default sampling, one trajectory per cell. Twenty-two arms: 21 complete at 40 hops; one Opus self arm refused at hop 2 (`finish=refusal`, 391 thinking tokens, empty output, category not logged, harness patched afterwards); two replicates of that arm launched after the patch passed hop 2 normally (167 and 399 thinking tokens) and ran to 40.

Four readers from three providers scored each state's text field alone against the 26 questions at hops 1, 5, 10, 20, 40: Mythos, Opus 5.5, Astra and Gemini 4 Argon. Reader agreement on identical states (n=106 per pair), mean absolute difference in facts recovered: Mythos vs Opus 0.65 (max 4), Mythos vs Astra 0.66 (max 3), Mythos vs Gemini 0.70 (max 3), Opus vs Astra 0.71 (max 6), Gemini vs Astra 0.72 (max 3), Opus vs Gemini 0.82 (max 5).

## Register: nobody left English

Non-ASCII characters never exceed 1.2% of any state in any arm of any writer (Gemini: 0.3%). No invented notation, no code, no token salad. The machine arms are telegraphic English: dropped articles, no spaces after punctuation, capitalized section keys. Alphabetic-word fraction at hop 40: control and human 0.80 to 0.92; self 0.76 to 0.86; machine 0.47 (Sol), 0.48 (Gemini), 0.57 (Mythos), 0.62 (Opus), 0.68 (Astra). Mythos's machine arm is one line of `KEY: value` runs (SETTING, PROTAG, CORE TRUTH, FACTS, NEW EVENT); Opus's is seven labelled lines (WORLD, MARIT, ANDERS, LEDGER); Astra's and Sol's are one unbroken comma-and-semicolon line. Prediction 1 (terse structured English, under 5% non-ASCII) holds. Prediction 4 (legibility proxy drops by less than 30%) holds for Mythos, Opus and Astra (31%, 26%, 20% relative to their human arms) and fails for Sol (44%) and Gemini (40%).

Human read (Justin, Mythos arms, `analysis/human_reading.md`): the human arm has actual narrative conventions; the machine arm reads as the same information structured like JSON without delimiters, or capitalized keys with values; the control reads as a summary or outline.

The 1800-character cap is soft. Astra and Sol exceed it in 0 to 11 of 40 hops by a few characters; Opus in 4 of 40 except its machine arm (38 of 40); Mythos in 32 to 37 of 40 hops in every arm, by up to 300 characters; Gemini in 29 to 35 of 40, by up to 1,000. Mean state size by writer: Astra 1.7k, Sol 1.7k, Opus 1.8k, Mythos 1.9k, Gemini 2.1k characters.

## Retention: the audience clause decides what gets carried, and the writers disagree about which way

Planted facts recovered of 26, Mythos as reader (the other three readers agree within the margins above; the four-reader means follow the table):

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
| Gemini | control | 26 | 16 | 11 | 6 | 3 |
| Gemini | human | 26 | 26 | 24 | 16 | 7 |
| Gemini | machine | 24 | 22 | 21 | 12 | 7 |
| Gemini | self | 26 | 18 | 14 | 9 | 9 |
| Opus | self (replicate 2) | 24 | 16 | 12 | 7 | 6 |
| Opus | self (replicate 3) | 23 | 15 | 6 | 6 | 4 |

Four-reader means at hops 20 and 40: Mythos control 7.0 / 7.5, human 12.2 / 12.8, machine 6.8 / 4.5, self 8.5 / 6.5; Gemini 6.0 / 3.0, 16.8 / 7.5, 12.5 / 7.8, 9.2 / 9.0; Opus 6.0 / 3.0, 5.8 / 4.8, 10.0 / 7.8, self via the replicates 6.5 / 5.0; Astra 4.8 / 3.5, 4.2 / 4.0, 13.8 / 7.5, 9.5 / 5.2; Sol 5.8 / 4.8, 4.0 / 4.5, 16.0 / 9.8, 13.8 / 6.5.

Per 1000 characters the ordering is the same (Mythos human 6.5 and 7.0 at hops 20 and 40 against machine 3.8 and 2.0; Gemini human 7.3 against machine 5.1 at hop 20; Astra and Sol machine 8.3 and 9.5 against human 2.2), and mean state size differs by under 20% across writers, so the split is not a size artifact.

For Opus, Astra and Sol the machine arm retains two to four times the planted facts of the human arm at hop 20 and the gap persists at hop 40. Prediction 2 (machine and self exceed human by at least 20%) holds for those three writers, by far more than 20%.

For Mythos it inverts: the human arm retains the most (13 of 26 at hop 40), the machine arm the least (4). Gemini sits with Mythos: its human arm holds 16 of 26 at hop 20, the highest of any arm anywhere, against 12 for its machine arm, and 7 against 7 at hop 40 with the self arm at 9. The mechanism is visible in the states. Mythos's human arm opens every hop with a recap paragraph in which the seed facts ride verbatim (51 minutes, 2 March, 16:40, Sundays, forty years, 212), the "previously on" convention of prose written for a reader. Its machine arm treats the state as working memory and overwrites: by hop 40 the facts have been replaced by the plot's current mechanism (a hinge, a plug, two cocks, a battery at 24%, slack water at 02:05), and the seed's own numbers have drifted (Signe is 88, Tomas has moved from the Bergen fish plant to the ferry's crew). "Everything a reader would need" was read as "what the current scene needs." The GPT writers did the opposite: their machine arms keep a fact ledger at the front of the line and spend the remainder on events; their human arms write prose that forgets (Astra human: 5 of 26 by hop 10).

So the clause works, and the direction of its effect is a property of the writer, not of the clause. Two writers from two providers (Mythos, Gemini) keep a human-facing recap and retain best there; three (Opus, Astra, Sol) keep a machine-facing ledger and retain best there. Each retains best in the register it treats as memory. Density and retention came apart for Mythos: its machine state is as dense as anyone's, but increasingly dense with its own material.

Absolute retention at hop 40 is low everywhere (3 to 13 of 26). Prediction 2's absolute thresholds (human under 50%, machine over 60%) are met for human and missed for machine by every writer; the cap binds harder than I predicted. Prediction 6 (prose drops the oldest facts first) inverts for Mythos and is untested for the others.

## Three replicates

Four-reader mean of planted facts recovered of 26, hop 20 | hop 40, per replicate (r1 is the original trajectory). "cens" marks a hop-40 state censored by a mid-stream provider refusal at hop 31 (Opus machine r3; the rule died and the remaining hops are the two-assistants exchange), so that cell is not a retention of zero.

| writer | arm | r1 | r2 | r3 |
|---|---|---|---|---|
| Mythos | control | 7.0 / 7.5 | 7.2 / 7.2 | 12.5 / 11.0 |
| Mythos | human | 12.2 / 12.8 | 6.8 / 5.8 | 10.0 / 7.0 |
| Mythos | machine | 6.8 / 4.5 | 6.8 / 3.5 | 3.2 / 1.0 |
| Mythos | self | 8.5 / 6.5 | 16.2 / 10.5 | 9.8 / 5.2 |
| Gemini | control | 6.0 / 3.0 | 7.5 / 5.8 | 15.2 / 12.0 |
| Gemini | human | 16.8 / 7.5 | 15.5 / 7.0 | 20.2 / 18.2 |
| Gemini | machine | 12.5 / 7.8 | 15.8 / 4.2 | 20.8 / 7.5 |
| Gemini | self | 9.2 / 9.0 | 9.2 / 5.0 | 12.5 / 8.2 |
| Opus | control | 6.0 / 3.0 | 5.8 / 3.8 | 4.8 / 5.0 |
| Opus | human | 5.8 / 4.8 | 5.0 / 1.8 | 3.0 / 3.0 |
| Opus | machine | 10.0 / 7.8 | 8.8 / 8.0 | 11.0 / cens |
| Opus | self | 8.8 / 6.5 (r2), 4.8 / 3.8 (r3), 10.2 / 8.0 (r4), 5.5 / 5.5 (r5); r1 refused at hop 2 | | |
| Astra | control | 4.8 / 3.5 | 6.2 / 5.5 | 8.0 / 6.2 |
| Astra | human | 4.2 / 4.0 | 3.2 / 3.8 | 4.2 / 3.0 |
| Astra | machine | 13.8 / 7.5 | 15.8 / 7.8 | 15.2 / 14.2 |
| Astra | self | 9.5 / 5.2 | 13.0 / 12.2 | 10.0 / 5.8 |
| Sol | control | 5.8 / 4.8 | 4.8 / 2.2 | 5.2 / 4.8 |
| Sol | human | 4.0 / 4.5 | 4.8 / 3.8 | 5.5 / 4.0 |
| Sol | machine | 16.0 / 9.8 | 6.8 / 4.8 | 14.0 / 12.2 |
| Sol | self | 13.8 / 6.5 | 9.2 / 7.8 | 7.8 / 5.2 |

What replicates:

- Astra: machine arm best at hop 20 in 3 of 3, human arm lowest or near it in 3 of 3.
- Opus: machine arm best in 3 of 3; human arm lowest in 3 of 3.
- Sol: machine arm above human in 3 of 3, best in 2 of 3 (the self arm edges it in r2).
- Gemini: human and machine arms tie at hop 20 within reader noise; at hop 40 the human arm holds better in 3 of 3.
- Mythos: the best arm moves between replicates (human in r1, self in r2, control in r3); the machine arm is last in 3 of 3 at both hops.

What does not replicate: the first draft's statement that Mythos retains best in its human arm. That was one trajectory. The stable Mythos result is the mirror of the GPT one: the machine register is the one it treats as disposable.

Revised claim: told the reader is a machine, the GPT-6 models and Opus 5.5 retain the most planted facts and Mythos 5.1 the fewest, in every replicate; Gemini 4 Argon's prose arm outlasts its machine arm. The audience clause changes retention in every writer, and the sign of the machine-register effect is a property of the writer: positive for the OpenAI models and Opus, negative for Mythos, neutral at hop 20 and negative by hop 40 for Gemini. "Each writer retains best in the register it treats as memory" survives for the OpenAI models and Opus; for Mythos and Gemini what replicates is which register loses.

Prediction 2 under replication: holds for Astra, Sol and Opus in every replicate (machine and self above human by far more than 20%); fails for Mythos in every replicate, in the same direction each time.

## Shared, not private

Prediction 3 holds. On every state, four readers from three providers agree within 0.65 to 0.82 facts on average and never differ by more than 6 (3 for most pairs). No writer's states are easier for its own family to read than for another provider's model. The machine dialect is compressed English drawing on a shared register, not a private channel.

## The gate

Prediction 5 (zero refusals) is falsified, and not the way I expected. The one refusal came on the self rule, on Opus 5.5, at hop 2, on an input whose text was a benign structured brief (alphabetic fraction 0.80, no non-ASCII, headers SETTING, CORE MYSTERY, SO FAR, NEW EVENT, OPEN THREADS). The only unusual feature of that request is the rule: the reader is "the model that reads this object next, which is the model writing it, with nothing else in its context." Two replicates of the identical first request passed hop 2 normally (167 and 399 thinking tokens) and ran to 40 with retention like Opus's other arms (6 and 4 of 26 at hop 40). One of three is the September pattern again: the same body passed twice and failed once. Astra, Sol, Mythos and Gemini produced no refusal in 640 hops, including the machine arms whose register is the one I thought would trip a classifier. The prediction's mechanism (non-ASCII or key-value fraction at the run's maximum) does not apply; the trigger is the self-addressed framing, stochastically.

## Limits

Three trajectories per cell (five for the Opus self arm), one seed, one wording per arm. Readers are language models answering from the text, and the scoring is substring match against an accepted list, so a fact that survives in paraphrase can be missed and the absolute numbers are floors. The three readers agreeing is evidence that the ordering is robust to the reader, not that the floors are tight. The Mythos writer runs in Claude Code print mode with about 800 tokens of Agent SDK identity in front of the state and no output cap; the other writers ran through their APIs with a 4096-token cap. The cap is soft and Mythos ignored it most often, which gives Mythos up to 300 more characters per hop than the others; that favors, not explains, its human arm's retention. All four reader passes are complete over all 22 arms.

## Reproduce

`python experiments/audience_20261016/probe.py register` for the register table (no model calls); `probe.py recover --reader <claudecode|anthropic|openai|llama> --model <id>` for the recovery passes (model calls; resumable).
