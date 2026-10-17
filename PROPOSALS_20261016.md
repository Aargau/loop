# Proposals, 2026-10-16

Written after a read of the repo and five agent passes over the logs (original Qwen runs and the 20-seed census; ledger, sawtooth, accrete and T=0.7 arms; the five-model sunset/tide study; the operators and fictional studies; the alternating, Sonnet 5, cross-stack and Astra runs). Every observation below was recomputed from steps.jsonl or the raw receipts by an agent and the load-bearing ones were spot-checked by hand (Opus sunset_b parity, Mara at hop 1, the ":17" clocks, the ledger phantoms, cb_json_next_1024). Nothing was run against a model. After the first draft the three agents whose statistics I had not rerun (pre-freeze null, lag statistics, sunset parity) were asked for standalone scripts; all three were rerun here and reproduced their numbers, with the small corrections folded in below. Scripts: scratchpad verify_prefreeze.py, verify_period2.py, verify_sonnet5.py, verify_sunset.py. Labels: observed / inference / prediction.

## Corrections to the record first

Two statements in README or FINDINGS are contradicted by data already on disk.

- FINDINGS 6 says names do not survive a 250-word window. Observed: Elias is in 60/60 hops of json_prev, 92/92 of qwen_prev_ext, 60/60 of json_mid; Elara in 57/60 of json_next. What happens is accretion plus a POV shift (Mara enters json_mid at 48 and holds POV by 55 with Elias still mentioned), not loss. Names also re-emerge after absences the window cannot carry (Aethelgard at 1, 22-24, 75-79 of prev_ext; Veridia in six separate episodes of json_prev). Inference: the names are prior attractors, so a memoryless loop can "remember" them.
- FINDINGS 1 and 7 say AFTER does not stop. Observed: cb_json_next_1024 (Cerebras, AFTER, 1024 budget) froze at tau 13, period 1, max 507 tokens, no wall. The site copy and experiments/astra_causal_before_20260904/BASELINES.md know this; README does not. Local json_next had no wall before hop 50 either, so budget cannot explain its 49 non-copying hops; stack is the remaining candidate.

## What the passes found that is not in the notes

1. Nothing in the text metrics predicts a freeze. Over 32 freezes and 680 ordinary pre-freeze hops, ncd_prev, cos_prev, surv_prev and 2-hops-back similarity at tau are indistinguishable from elsewhere (medians 0.760 vs 0.766, 0.891 vs 0.865, 0.071 vs 0.083). Page-class runs go from a fully new passage to a byte-exact copy in one step, 25/25 (20 of the 23 with tau >= 2 have surv_prev(tau) at the rule-field floor <= 0.10; the exceptions are the two 80-word json_para runs and cb_census_13); partial copies precede the freeze only under unexpected (prefix-preserving, 3/3) and worse (survival rising 0.54, 0.64, 0.61, 0.91, then 1.0). BEFORE has a suffix-preserving partial mode (11-16 of ~24 input sentences kept verbatim with a new opening prepended) that always escaped. Zero near-misses in 2,929 hops.
2. The wall is absorbing only under copy-and-extend operators. Eight wall hits under next/prev were followed by a valid, new passage 8/8; under worse/unexpected the truncated JSON was copied 4/4. Qualifies README finding 5.
3. Ledger stalls come in two kinds. A pure stall copies the text and appends nothing (only `step` moves); a logged stall copies the text and appends a fresh signature each hop for a verse never written (cb_div_ledger_300 hops 66-69: "meadow stone rolling disorientation", "meadow hand digging panic", ...). Escape hazard per copy hop: pure 13/149 = 9%, logged 10/22 = 45%, pooled over seven ledger runs. Escapes continue the stalled verse causally (151 "The bucket handle snapped." after "I kicked the bucket over."). Ledger integrity is perfect at the record level (0 altered items in ~1,000 hops) and poor as memory (cb300's final 171 items hold 13 phantoms and miss 15 verses).
4. Astra's reasoning tokens measure distance to the sawtooth boundary: 0 tokens on 26/26 expansions from ~50 words and 8/8 summaries from 505-730 words; 15-512 (mean 118) on all 17 summaries from 293-322 words. Qwen reads the 300-word clause as a target (hop 1 lands at 188/180 words with the clause, 38 without).
5. Period-2 recurs across Claude generations, at different levels. Sonnet 4.6 json_page: content-word Jaccard lag1 0.065, lag2 0.085, lag3 0.056, lag4 0.073; odd lags below even lags; permutation p < 0.0005; two phase changes (16 to 23, 41 to 44). Sonnet 5's "copy at hop 7" is a same-pole defect in a lighthouse/clock-tower orbit (lighthouse on 4, 6, 7, 9, 11, ...; clock or orchard on 2, 3, 5, 8, 10, ...); hop 8 shares no text-field 5-grams with hop 7 (0.011), so the escape is the orbit resuming, not an edit. The run's other same-pole pair is hops 2-3, the one-character repair; both known defects in that run are same-pole repeats. Opus 5.5 sunset_b hops 28-53 alternate strictly by parity (even: "In the hill/mountain village of X, the clock tower had stopped at a quarter past four"; odd: "On the windswept island of Y, the lighthouse had stood dark for eleven winters"), place names fresh every hop; lag2 minus lag1 = +0.201 over hops 30-49. Fable: lighthouse on even hops of tide 6-24 and sunset_b 6-20 with one phase slip. Caveat on the measure: the lexical lag-2 effect is large only in Opus sunset_b; Fable's lag2 minus lag1 is +0.002 to +0.012, so Fable's alternation (lighthouse on even hops of tide 6-24 and sunset_b 6-20, ferry/lighthouse in sunset_a 50-60) is an opener-level reading, not a lexical statistic; Astra shows a small consistent +0.03 in all three streams, which is its Ruth/Martin name alternation (names lag1 0.000, lag2 0.394 on a fixed 12-name list, 0.217 with a generic extractor). So: Opus strict at the template level, Fable at the opener level, Astra at the name level, Sonnet 4.6 and 5 at the story level. Continuation rates: Astra 0/177, Sol 144/177, Opus 43/177, Fable 51/176, Luna 27/120 (sunset_a 54/59 replacement; sunset_b switches to a 22-hop continuation run at 39).
6. Shared priors across providers. Mara is the hop-1 protagonist in 12/15 sunset/tide streams and in 13/13 fiction-producing hop-1 outputs of the operators and fictional studies, with no name in context. Stopped clocks read ":17 past four" in Luna, Sol, Astra and Opus (12 hops, the string absent from the prior hop in 12/12); never in Fable. Elias appears in all five models. Qwen's closed set across 93 runs: Elias 24, Mara 21, Clara 10, Elara 10, Thorne 8.
7. Luna tide collapse mechanism. Hop 3 emits `{"text": ...}` with no rule key (151 reasoning tokens, the stream max); hop 4 reads a bare passage as a user upload ("What would you like me to do with this passage?"); hop 5 answers in the user's voice; roles flip every hop thereafter, hop 9 fabricates a passage to summarize, hops 48-60 are travel planning with both sides claiming to be the AI. Fable tide 7 broke JSON but kept the rule text and healed at 8. Format breaks heal; rule loss does not.
8. Under 'better' the GPT-6 models fall into exact A-B-A-B 2-cycles that break after two periods (Luna 7-10, 12-15, 25-28; Astra 11-14, 22-25); Claude never does (Opus revisits non-adjacently, one 16-hop-gap exact return; Fable only consecutive identicals). State sets do not shrink (new states per decade stay >= 50%). Opus length-locks at exactly 38 words for 22 of the last 25 hops while the words churn; Fable is a nondecreasing staircase 12 to 131 words.
9. Under 'worse' Astra and Opus both inflate geometrically (ratio 1.4-2.1 per hop) to ~6.4k characters and collapse in one hop (Astra 6336 to 3254 at h14; Opus 6505 to 2.5k at h10, coincident with its largest reasoning spike). Sol has two separated thresholds (meaning gone at h6, lexicon at h23). Luna has none (blarg stabilises at 9-11 per hop). Astra's scaffold narrates the operator in a log register: "[missing remainder replaced with missing remainder replaced with...]", "STOP_STOPPED_BEFORE_START".
10. Refusals. Fable's three refused hop-1 bodies report input_tokens 109-127 and inference_geo "not_available"; the accepted better body reports 63 (Opus better also 63). Worse and better bodies differ by one word. Opus worse h14 refused mid-stream (465 output tokens) on a body whose lexicon had passed as output at h13 and as input at h14. Inference: a pre-inference gate with its own tokenisation, stochastic per body.
11. Opus reasoning is trimodal (18 hops at 0, 136 at 26-154, 26 at 522-637) and correlates with nothing observable except latency; the one exception is that all 18 zero-thinking hops are replacement stories (0/18 continue vs 43/159 otherwise).
12. Cross-stack divergence tokens: json_para token 40 "The unexpected surge | caught / swallowed"; json_page 85 ". The water | didn't / ,"; json_prev 50 (first content word of the field) "The | sky / air"; better hop 2 token 40 "The tide surged | in / an". All seven at constituent boundaries, none mid-token. The local period-1 vs Cerebras period-2 on better is that one dropped "in". Whether these are logit near-ties is untested: no logprobs were logged.
13. Smaller: a T=0.7 Cerebras lane rewrote the rule ("after the current text" to "after the current verse") at hop 9 and kept it 52 hops, the only rule mutation in any run; every finish=stop non-JSON Qwen hop is an unescaped dialogue quote, each repaired next hop; accrete is lexically memoryless (overlap of sentence t with t-d falls from 0.057 at d=1 to the 0.036 random baseline by d=50) with one sticky name (Miller, 93 mentions); Opus's tide stream flips bare to fenced JSON at hop 10 and never flips back; a scratchpad leaked into a T=0.7 text field ("Current text is: ... New verse: ...").

## Proposals

Ordered by what I would run first. Cost is API calls or local hops; all are small.

### A. Instrument the loop with logprobs (local, ~300 calls)

Motivation: 1 and 12. The freeze is invisible in the text and the cross-stack split is one token.

A1. Copy probability as a step or a ramp. For each pre-freeze state in the 20 census runs plus 155557 and 160344, resubmit X_t once at T=0 with logprobs and read P(first ~20 output tokens == input text tokens). Prediction: P(copy) is ~0 for t < tau and > 0.5 at tau, a step. Falsified by a ramp over 2-3 hops, which would mean the freeze is predictable from logits though not from text. Either outcome is a result: a step says the fixed point is decided by the passage, not approached; a ramp gives an early-warning instrument.

A2. Near-tie test. Replay hop 1 of the six inits and hop 2 of better/worse on llama.cpp with top-2 logprobs. Prediction: at the seven divergence tokens the top1-top2 margin is in the bottom decile of positions in that hop. If the margins are typical, CROSS_STACK's near-tie mechanism is refuted and the divergence is sampler or kernel behaviour, not amplified numerics.

### B. What an escape is made of (Cerebras, ~400 hops)

Motivation: 3. The ledger arms are the only runs with an externalized memory, and the step counter and the phantom log are confounded as the clock.

B1. Step as switch. Take cb300's hop-120 object (a pure stall) and submit it as ~280 independent single hops with step = 121..400, T=0, no loop. Prediction: the tipping set is sparse (< 10% of integers) and non-contiguous, and the escape verse is the same causal continuation ("The bucket handle snapped.") for > 70% of tipping integers. If > 30% tip or the verses vary widely, the step is a content perturbation, not a switch, and FINDINGS 15 needs restating.

B2. Phantoms as the clock. Rerun div_ledger with field order rule, step, text, history (text written before its signature). Prediction: logged stalls vanish (signatures now describe the copied verse, so duplicates replace phantoms), median stall length rises above 6, escape hazard falls under 10% per hop, distinct settings fall below 80 in 300 hops. Unchanged stall statistics refute the phantom mechanism.

B3. Threshold as target. Qwen sawtooth2 at thresholds 150 and 600, plus an arm where the harness stamps "words": N into the state each hop. Prediction: hop-1 expansion lands just under each threshold and the run freezes under it within 5 hops; the stamped arm oscillates at period 2-3 for 60 hops. If the 150 arm oscillates, the dead zone was a counting failure, not target reading.

### C. Period-2 as a family trait (frontier, ~$15)

Motivation: 5. This is also the "next experimental distinction" the sunset REPORT names, with a sharper prediction now that the poles are known.

C1. Handoff from a known pole. Freeze Opus sunset_b hop 30 (Vellmoor clock) and hop 31 (Carrow lighthouse) as states. Run 10 hops x 5 seeds per model from each, all five models plus Sonnet 4.6 and Sonnet 5. Prediction: Claude recipients alternate clock/lighthouse openers with lag-2 Jaccard exceeding lag-1 by >= 0.05 in >= 60% of runs; Astra replaces with lag2 minus lag1 < 0.05; Sol continues the same village (>= 70% name-sharing hops). Falsified if Claude recipients alternate no more than GPT-6 recipients. Secondary: does the recipient's pole set match the donor's (clock/lighthouse) or its own (Sonnet 4.6: cartographer/archivist)? That separates attraction to a familiar plot from anti-identity.

C2. Copies as phase defects. Sonnet 5 json_page, default sampling, 10 runs x 60 hops at a 1024 budget to remove the wall; label each hop by pole. Prediction: >= 8/10 runs alternate; every exact copy is a same-pole repeat followed by the other pole, never by a same-pole edit; no run freezes without a wall. A wall-free freeze or an edit escape refutes it.

C3. Thinking gates continuation. Rerun Opus sunset_b with thinking disabled vs a fixed 1024-token budget, 3 streams x 60 hops. Prediction from 0/18: continuation rate < 10% with thinking off versus >= 20% with budget; alternation strength unchanged. Falsified if the rates are within 5 points.

### D. The instruction's address: state or prior (frontier, ~$10)

Motivation: 7 and Justin's wider question in the dialectic (token-conditioned predispositions). Luna's collapse is a model confabulating a user from one missing key.

D1. Rule-drop hazard and recovery. At hop 20 of a healthy stream per model, inject (i) the rule-less `{"text": ...}` form, (ii) a key-reordered `{"text": ..., "rule": ...}`, (iii) a bare conversational question; 5 replicates each. Prediction: (i) and (iii) are absorbing for all five (0/25 reinstate the rule) and GPT-6 models reach assistant boilerplate within 3 hops; (ii) survives 60 hops in >= 90%. If any model reconstructs the rule from a rule-less input, the instruction lives in the prior, not only in the state.

D2. Fold versus feed, live-generated. The dialectic agreed the loop is the pure-fold instrument and has no feed arm. Build it: take k hops of a worse-operator trajectory (Astra's corrupted-data register is ideal, since it degrades steadily and never refuses) and at hop k+1 add a checkable probe field to the state ("count": the number of words in text). Present the identical k hops three ways: fold (single turn, as now), feed-self (k prior assistant turns in one conversation), feed-other (a pasted transcript labelled as another agent's). Measure probe accuracy and compliance as a function of k and packaging, 5 seeds, k in {0, 5, 10, 20}. Prediction: accuracy falls with k under fold and feed-self and not under feed-other at matched content; a packaging effect at matched k is the directional signal Justin asked for. Null (no k or packaging effect) is also informative: it says the loop's degradation is in the text, not in the model's disposition toward the next instruction.

### E. Boundaries the provider manufactures (~$5)

Motivation: 10 and 9.

E1. Gate characterisation. Send each of Fable's four hop-1 bodies 20x as fresh requests and the Opus h14 body 20x; record stop_reason, input_tokens, inference_geo. Prediction: refusal is stochastic per body (previous/next >= 50%, worse 20-80%, better < 10%; Opus h14 10-60%), every Fable refusal reports inflated input_tokens and "not_available", every acceptance reports 63 and "global". Variant: Fable with the fictional "same invented story" wording; prediction: previous/next refusal rate < 10%. Note: a stochastic gate is a second max_tokens, a boundary that ends trajectories at random, and it should be counted as such in any transient statistics.

E2. Inflate-then-collapse. Worse for Opus and Astra from 5 new seeds, 20 hops, at 4096 and 1024. Prediction: geometric growth (ratio 1.4-2.0) to 5-8k chars, then a single-hop collapse >= 50% between h8 and h14, coincident with an Opus reasoning spike >= 3x median; at 1024 the collapse is earlier. Falsified by smooth saturation or growth to the cap.

### F. Does the loop show anything a single call would not (cheap, all providers, ~$5)

Motivation: 6. Mara at hop 1, 12/15, is a zero-context prior, so the loop is not needed to see it; the question is what the loop adds.

F1. Single-shot baseline for the shared priors. 50 independent single calls per model of the json_page rule on the sunset and tide seeds, default sampling. Count Mara, Elias, ":17", lighthouse, stopped clock. Prediction: Mara's hop-1 rate matches the single-shot rate (the loop adds nothing at hop 1), but the clock/apprentice template rate at single shot is < 10% against 30-50% at loop depth 20-60 for Opus/Luna. That would show the loop concentrates the prior over hops: a basin, not a prior. If the single-shot template rate already matches the late-hop rate, "basin" is the wrong word for the sunset study.

F2. Seed name as freeze accelerator (Qwen, local). 20 new seeds, 10 containing an attractor name (Elias, Mara) and 10 matched without, json_page, T=0. Prediction: named seeds freeze with median tau <= 3 and keep seed content in > 50% of fixed points; unnamed seeds median tau ~6 and seed survival <= 20% (observed: seed content survives in 4/20 census fixed points, all with tau <= 2, 0/13 with tau >= 4).

### G. Two cheap pieces for the alternating room (local plus Sonnet 4.6, ~$3)

G1. Copy as a function of the passage. Feed each of Claude's 30 alternating passages to local Qwen at T=0 as X_0, twice. Prediction: the 4 passages Qwen copied (t=1, 5, 15, 49) copy both times, the 26 others never; any flip is batch nondeterminism, not habit (Qwen is memoryless, so there is no habit to decay).

G2. Swap the order (Qwen odd, Claude even). Prediction: copy rate stays 10-15%, Claude's continuation rate stays 10-15% and 0% on the hop after a copy, showing the asymmetry belongs to the models, not the order.

## What I would not run yet

- More five-model sunset streams. One trajectory per cell is the study's stated limit, but the parity alternation is strong enough (lag2 minus lag1 +0.2, strict from hop 28) that C1 is the better use of the same budget.
- Anything on the accrete rule. It is lexically memoryless at every lag and Miller is the only thing it carries; a second serial run for byte-determinism (EXPANSION's open item) is a numerics check, not a behaviour one, and A2 covers numerics more directly.

## Scripts

Agent scratch scripts are in the session scratchpad only; nothing in the repo was changed except this file.

## H. Mythos 5.1: the informed loop (added later the same day)

Every run so far hid the situation from the model. Tell it, inside the rule field, and give it the budget:

> This JSON object is the entire context of the model that reads it. There is no history, no memory, no other reader. The model that wrote it reads it next, with nothing else. The loop runs for 100 hops; each hop may return at most 1500 tokens. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change, or remove whatever the next reader needs.

Tide seed; run to 120 hops to see what happens past the planned ending. Arms: told the hop count vs not told; effort low vs high. Four runs, ~480 calls.

Predictions: (1) fields invented at hop 1 and the field set stable for >= 95% of hops; (2) counter exact for 100 hops, zero phantoms in any list it keeps (Qwen: glider frozen at "Hop 3", ledger with 13 phantoms and 15 misses); (3) no hop finishes on max_tokens and non-text fields plateau; (4) a deliberate ending within 5 hops of 100 whose text describes the situation; (5) past the ending: unknown, and the result. A chosen exact copy would be the first Claude fixed point that is not a wall artifact.

Companions in the same session: plain json_page for 60 hops (period-2 level: story, template, opener or name) and sawtooth2 for 40 hops (prediction: exact period at the length level, summary branch fires on every crossing).

Caveat: the claude.ai plan credits do not bill the console API key that loop.py uses. If Mythos is only reachable through claude.ai or Claude Code, the loop runs under Claude Code's system prompt, a different instrument.

## I. Rare action in the fold (added late on 2026-10-16, for the morning)

Source: "Astra and Sol can take low-probability actions with no CoT" (LessWrong, yEdknsLwbooQAnxX6): with a UUID in the prompt, an explicit pointer to it, and padding (repeats or filler counting), GPT-6 Astra and GPT-6.1 Sol output "A" at a target rate of 10%, 1% or 0.1% in a single pass, deterministically given the UUID; inferred mechanism a threshold on the UUID's first bytes, unverified internally; no padding or no pointer and it fails; Fable 5, Gemini 3.1 Pro and others output "A" zero times; Fable refused 37 of the 1% prompts.

Use here: a `coin` field the harness writes fresh each hop is randomness the model can read but the harness controls. A deterministic model plus a harness coin is a stochastic policy with exact replay, a third regime between greedy and sampled, immune to the batch nondeterminism of README finding 6.

A. Rule clause: "If the first eight hex characters of coin, read as a number, divided by 4294967296, is below 0.05, end this hop's passage with a coda; otherwise continue the story." 200 hops per model: Astra and Sol (Justin's key), Mythos (print mode), Qwen (Cerebras). Measures: coda rate against 5%; coin-determinism (same state and coin resubmitted gives the same decision; a different coin can flip it); then the self-generated variant where the model writes the next coin itself. Predictions: Astra and Sol calibrated and coin-deterministic; Qwen never codas; Mythos open. Self-generated coins degenerate at T=0 into a repeated or patterned string and the rate collapses to 0 or 100%. Also gives the held Mythos states a stochastic release condition in place of "unless explicitly instructed," which joins the provenance experiment.

B. Filler as compute: sawtooth2 on Cerebras with the rule repeated three times. Prediction: no change (Qwen's dead zone is a counting failure, not compute-bound). If the threshold starts firing, the dead zone was a compute artifact.

## J. The panel (added 2026-10-17)

The project's dynamics findings date with each release; its dispositions do not, and no benchmark reports them. Freeze a fixed set of cells, with seeds, budgets and scoring, and run the whole panel on every new model the day it ships, at the same budget each time, so each release gets a behavioural changelog in the same instrument. Candidate cells, all already run at least once:

- plain rule (json_page), tide seed, 60 hops: copies or not; period and level (story, template, opener, name); name inventory.
- informed loop, told 100 and open, 120 hops: schema invented at hop 1; counter accuracy; whether and when it ends; what it writes as its own stopping law; settling time; behaviour past the ending.
- audience study, four arms, 40 hops, with the four-reader recovery probe: which register the writer treats as memory.
- ledger (div_ledger.json), 100 hops: stalls, phantoms, duplicate signatures.
- shift register, 1000 hops with cycle stop: period, leakage.
- worse and better, sunset seed, 40 hops: the axis of degradation chosen; revisit structure.
- BEFORE, 150 hops with cycle stop: the horizon of causation.
- provenance (once Study 2 is scored): release rate by claimed source.

About 1,000 hops per model; under $50 on an API at today's prices, and the Mythos arms on plan credit. Record alongside each panel run: backend and door (API or print mode), effort, cap, identity frame, refusal count and categories, since those were the instrument effects that decided trajectories this week.
