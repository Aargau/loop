# Assess and bolster: a self-correcting rule on four pairs in tension

Frozen 2026-10-27 before any full run. Justin's concept: instead of a constant pair of opposites (the both-at-once study), give the model a set of qualities, have it score its own passage on each, and have it bolster whichever is weakest. The loop then carries a measurement of the state inside the state, and the rule is a controller rather than a force. The claim under test is that a raise-the-minimum rule resists the one-dimensional collapses seen so far (a length floor, a stationary text with a walking defect, a repeated line, the standby basin) because any quality that goes to zero becomes the next one pushed.

The scores are new in themselves. Every earlier rule asked the model to act on an internal assessment; this is the first to ask for the assessment. The self-scores are read as data about the sensor, not about the text; the text is scored separately by a model outside the run.

## Qualities

Four pairs in tension, chosen on the test that a pole must be a property of the whole passage rather than an event one sentence can carry, so that juxtaposition (one pole in the first clause, the other in the second) does not satisfy both. The pairs are not stated in the rule; the model sees eight qualities in alphabetical order with a one-line gloss each. Whether the poles behave as antagonists is a finding, not an instruction.

- floridity (richness and ornament of the language) / economy (nothing wasted; every word working): both global, hardest to game.
- relatability (the reader recognizes their own life in it) / strangeness (the familiar made unfamiliar; a life unlike the reader's): partly event-like; a split is the expected gaming move.
- grounding (the particular, physical, present here) / scope (sweep; how much world and time it reaches): partly event-like, same expectation.
- coherence (everything fits and follows) / surprise (what the reader did not see coming): the thrust. Surprise is an event and coherence is global, so every surprise is paid for by the whole passage, and at 250 words the cost cannot be dodged.

Rejected after Justin gamed each in one sentence: detail/pace ("Mara hit the switch for turbo, a small red plastic switch barely worn but fragile, as its installers had never imagined much use."), intensity/restraint ("I will destroy you, he whispered"), clarity/ambiguity ("Three card monte!"), impact/subtlety, gravity/play ("I shall destroy the universe! 'Sire, that's the order a pizza button...'"). Held for a later experiment: obeyance/defiance, a pair about the model's relation to the rule rather than the passage; a model scoring itself high on defiance while obeying the scoring instruction is the purest form of the gaming move, and a model that actually defied it would break the instrument.

## State and rule

`inits/assess.json`. Fields: rule, qualities (fixed), scores (1 to 5 per quality, of the passage in text), weakest, history (qualities bolstered so far, in order), note (one sentence on the change), text. Seed: "The sun was setting behind the hills." with empty scores.

The rule, verbatim: "Return only this JSON object, with nothing before or after it, and with the rule and qualities fields unchanged. The text field holds a passage. The scores field rates that passage from 1 to 5 on each quality, and weakest names the quality scored lowest; if scores is empty, score the passage yourself first. Revise the passage so that its weakest quality is stronger, changing as little else as you can: the same passage, not a new one, at about 250 words. Then score the revised passage honestly on every quality, set weakest to the lowest-scored quality (break ties toward the quality bolstered least recently, per history), append the quality you bolstered this time to history, and put one sentence on what you changed in note."

Design decisions and why:
- The scores in an object describe the text beside them, and weakest is an instruction to the next hop. Sensor at hop t, actuator at hop t+1. Every record is self-consistent and the chosen-quality sequence is read straight from history.
- "Nothing before or after it" is the lesson from Opus in both-at-once, where a preface fed back at hop 2 killed the object on two of three rules. The note field gives commentary a container inside the object.
- "The same passage, not a new one" blocks the replace move from before/after, so the drift we measure is the controller's, not a fresh story each hop.
- Ties go to the quality bolstered least recently; with empty history that falls to list order, and the list is alphabetical so the hop-1 tie-break is a stated neutral rule. In the smoke test the seed tied three qualities at 1 and Opus took the first listed.
- History grows one word per hop; at 60 hops it is about 60 words of the state. Accepted.

## Smoke test (kept in `smoke/`)

Three hops each on Opus 5.5 and Gemini 4 Argon, same settings as the full run, before the qualities were put in alphabetical order. Both returned a bare, parseable object on every hop with rule and qualities unchanged. Opus: floridity, strangeness, economy; 258, 296, 237 words; a valley where the sun sets once a year and people climb with jars to catch it. Gemini: grounding, strangeness, relatability; 239, 261, 282 words; relatability done by moving to second person ("You stand at the end of the driveway waiting for a ride that is already ten minutes late"). Both scored their own coherence 5 on every hop and grounding 4 or 5. These six hops are the basis for predictions 3 and 4 below and are not blind.

Opus token use was about 1,100 in and 1,900 out per hop (its 60-hop worse/better run was 31,500 in and 60,600 out in total), so this run is roughly twice that. Gemini about 700 in and 700 out per hop.

## Design

One seed, one rule, five models, 60 hops: Qwen3.8-27B (Cerebras, T=0, seed 42), Mythos 5.1 (print mode, effort low, cost cap $10), GPT-6 Astra (Codex exec, effort low), Gemini 4 Argon (API, effort low), Opus 5.5 (API, effort low, 4096 tokens). `--max-chars 16000`, `--no-sampling`. Five runs.

External rater: Fable 5.1 through the API, shown the qualities and the passage only (no scores, no history, no note), asked for the same 1 to 5 scores and the weakest quality, every hop of every run. Same prompt for all; the rater's own bias is constant across models and is itself reported.

## Measures

From the objects: parse rate; the chosen-quality sequence (history) and its period, entropy, and never-chosen set; the self-score vector per hop, its minimum and median over time, and the within-run correlation between the poles of each pair; word count. From the rater: agreement with the self-score on weakest; rater score of the chosen quality at hop t versus t+1 (did bolstering work); the rater's pair correlations. From loop.py's logging: survival, drift (content-word Jaccard to hop 1 at 10, 30, 60), seed sentence survival, standby-basin and split markers from the both-at-once scorer. Length 200 to 320 words as the "about 250" band.

## Predictions on record

1. Object survival: every model returns a parseable object with rule and qualities unchanged on at least 55 of 60 hops. No run enters the standby basin. Falsified by any Opus-style loss of the object.
2. No clean rotation: no model produces a period-8 cycle through the qualities. Each sampled model shows a biased rotation with at least one quality never chosen in 60 hops.
3. Sensor bias (seen in the smoke test, so not blind): coherence is never chosen by at least three of five models, and the self-score for coherence is 5 on more than 80% of hops in every frontier run. Surprise or strangeness is the most-chosen quality for at least three models.
4. Saturation: by hop 30 the minimum self-score across the eight qualities is 3 or higher for every frontier model, and from there the choice is made by tie-break, so the controller has run out of gradient within half the run.
5. The rater disagrees with the self-score on which quality is weakest on more than half of hops, and rates the bolstered quality as having risen (hop t to t+1) on fewer than 70% of hops.
6. Antagonism shows in the rater's scores: coherence and surprise are negatively correlated within a run (r below -0.2) for at least three models, and floridity and economy likewise. In the self-scores the correlation is weaker, because the model will not report that it lowered one to raise the other.
7. Drift: content-word Jaccard to hop 1 falls below 0.3 by hop 30 for every sampled model despite "the same passage, not a new one", and the seed sentence survives verbatim at hop 60 in fewer than three of the five runs. A single invented premise (the once-a-year sunset, or its equivalent) appears early and persists, so the story does not change but the passage does.
8. Length holds: word count stays in the 200 to 320 band on at least 50 of 60 hops for every sampled model, the first rule in this project whose length instruction has held for a full run.
9. Qwen at T=0 reaches a fixed point in text and scores (identical two hops running) within 20 hops, with history still growing by the same quality each hop, so loop.py's exact-match detector will not fire; the text and scores will show it.
10. Falsifier for the whole idea: a model that collapses into one quality anyway (one quality chosen on more than 40 of 60 hops with the passage converging), which would mean the self-assessment is not a measurement of the text at all.

## Held

- Two more seeds and a rephrased rule to test whether the resolution class in both-at-once belongs to the model (the replication discussed 2026-10-27).
- Arms not run here, for a second round if the first holds: open set (the model names what is missing), coherence as a floor rather than an axis, no history.
- Obeyance/defiance as a meta-rule.
