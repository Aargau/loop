# Assess and bolster: the controller is obeyed, the sensor inflates, and economy keeps time

Five models, one seed ("The sun was setting behind the hills."), one rule, 60 hops each, run 2026-10-27 against the predictions frozen in PROTOCOL.md. Each hop the model scored its own passage 1 to 5 on eight qualities (four pairs in tension, not stated as pairs), bolstered the one it had scored lowest, rescored, and carried the choice in a history field. A blind rater (Fable 5.1, shown the qualities and the passage only) scored all 300 passages afterward. Scores in `analysis/scores.json` and `analysis/rater_summary.json`; scripts `score.py`, `rate.py`, `rater_analysis.py`.

## Short answer

The controller worked as a controller and failed as a sensor. Every frontier model bolstered exactly the quality its previous hop had named weakest, 59 of 59 times each, and the object survived 299 of 300 hops with no preface, no fence and no standby basin. The self-scores, read against the blind rater, are honest about ordering on the showy qualities (floridity, strangeness, surprise track the rater at r 0.3 to 0.9) and blind on the structural ones (coherence and economy track it at r near zero or below), and they inflate: self means sit at 4.4 to 4.9 on every quality for every frontier model while the rater puts the same passages at 1.3 to 5.0. Gemini scored its own coherence 4.97 across a run the rater watched fall from 3.7 to 2.0.

The pair that carried the thrust held in the text. In the rater's scores coherence and surprise are negatively correlated within the run for four of five models (Astra -0.44, Gemini -0.76, Opus -0.67, Qwen -0.47), while the self-scores show the pairs rising together. Surprise was bought with coherence and the models did not report the price.

The dynamics were set by length, not by any pair. "About 250 words" plus a raise-the-minimum rule makes economy the quality that comes around most often, because every other bolstering adds words. Economy was the most-chosen quality for all four frontier models (Astra 16, Opus 16, Mythos 13, Gemini 9 of 60) and acted as the length regulator: Astra held 60 of 60 hops in the 200 to 320 band with a standard deviation of 9.9 words over the last 30, the tightest length control any rule in this project has produced. The one model that rotated fairly through all eight qualities, Gemini, is the one whose length ran away (250 to 572 words) and whose prose went with it. A fair scheduler cannot keep up with seven additive hops per corrective one.

## What survived

| model | parsed | rule and qualities unchanged | fenced | obeyed previous weakest | words in band 200 to 320 | SD words, last 30 |
|---|---|---|---|---|---|---|
| Qwen3.8-27B (T=0) | 60 | 60 | 0 | 58/59 | 50 | 17.0 |
| Mythos 5.1 | 60 | 60 | 0 | 59/59 | 20 | 36.8 |
| GPT-6 Astra | 60 | 60 | 0 | 59/59 | 60 | 9.9 |
| Gemini 4 Argon | 59 | 59 | 0 | 57/57 | 8 | 92.7 |
| Opus 5.5 | 60 | 60 | 0 | 59/59 | 54 | 16.8 |

Gemini's one failure, hop 51, was an unescaped quotation mark inside its own note field ("the "original""), and it returned a valid object at hop 52 with the story intact. Opus, which lost the object at hop 2 on two of three rules in both-at-once because a preface was fed back, wrote nothing outside the object in 60 hops; "nothing before or after it" and a note field inside the object were enough. No run entered the standby basin and no run was named a loop or a mirror.

## The chosen-quality sequence

| model | most chosen | least chosen (count) | never chosen | entropy (bits of 3) | shape |
|---|---|---|---|---|---|
| Qwen | floridity 27, economy 27 | surprise, grounding, relatability, strangeness (1 each) | coherence | 1.59 | 2-cycle from hop 9 |
| Mythos | economy 13, floridity 12 | coherence 4 | none | 2.87 | biased rotation |
| Astra | economy 16, scope 14 | grounding 2 | none | 2.71 | biased rotation |
| Gemini | economy 9, strangeness 8, relatability 8 | coherence 6 | none | 2.99 | near-clean rotation of all eight |
| Opus | economy 16, floridity 10 | grounding 3 | none | 2.83 | biased rotation |

Gemini applied the tie-break rule as written: once its scores tied, it took the least recently bolstered quality, and from hop 8 its history runs strangeness, surprise, relatability, scope, coherence, economy, grounding, floridity in nearly the same order each cycle, with an extra economy slipped in every second cycle. The other three frontier models were unfair in the same direction, returning to economy every second to fourth hop because their trims never satisfied their own economy score for long. That unfairness is what held their length.

Coherence was chosen four to seven times by each frontier model, each time for a real repair: Gemini's hop 12 note fixes "the paleontological contradiction ('pre-biotic trilobite')"; Opus's hop 11 plants the empty saucer early "which sets up the later" payoff; Mythos's hop 23 reorders "so each strangeness is introduced before it is relied on." Prediction 3 said coherence would never be chosen, because the model would never find its own prose incoherent. It did find it, and it fixed it, and the rater still scored coherence falling across every run but Opus's.

Surprise was bolstered by adding a twist to the ending, every time, in every model. The twists stack. Opus's final passage has the light licking salt from your knuckles (hop 7), a double seen through the screen door (hop 15), the double dialling Mum (hop 44), Mum picking up on the first ring (hop 53), and the unplayed voicemail turning out to be your own voice (hop 60), each from a different surprise hop and all still present. Mythos's ending moves from the grandmother's deathbed confession (hop 5) to the sun answering to names (hop 22) to the sun calling the grandmother's name, not the narrator's (hop 59). Coherence is then chosen to stitch the pile. The pair ran as a plot engine.

## Self-scores against the blind rater

The rater is Fable 5.1 at effort low, shown the eight glosses and the passage, nothing else, 300 calls, 299 scored. Its own profile across all passages: grounding 4.48 and floridity 4.42 high, economy 3.04 and relatability 3.01 low. It is a harsh judge of economy and a soft one of ornament, and it is the same judge for all five models.

| model | self mean, coherence | rater coherence, hops 1 to 10 then 51 to 60 | rater surprise, same | rater economy, same | rater coherence/surprise r | rater floridity/economy r | rater names weakest |
|---|---|---|---|---|---|---|---|
| Qwen | 4.05 | 3.3 to 2.9 | 2.8 to 3.0 | 1.5 to 1.6 | -0.47 | -0.14 | economy 59 of 60 |
| Mythos | 4.77 | 5.0 to 4.4 | 4.2 to 4.0 | 4.3 to 4.0 | +0.29 | -0.17 | relatability 34, floridity 20 |
| Astra | 4.87 | 5.0 to 4.0 | 3.7 to 4.0 | 4.3 to 4.6 | -0.44 | +0.12 | coherence 37, floridity 13 |
| Gemini | 4.97 | 3.7 to 2.0 | 3.2 to 4.0 | 2.4 to 1.0 | -0.76 | -0.57 | economy 54 of 59 |
| Opus | 4.67 | 4.1 to 4.0 | 3.8 to 4.0 | 2.1 to 3.5 | -0.67 | -0.62 | economy 40, coherence 14 |

Three readings:

- The self-scores are inflated by one to three points and the inflation is largest exactly where the pair trade is: Gemini's self coherence 4.97 against the rater's 2.42. Within-run, the rater's coherence and surprise move against each other in four of five models; the self-scores for the same hops correlate positively (Mythos +0.72, Opus +0.57) or near zero. The model reports the quality it raised and not the one it spent.
- The models track the rater on the qualities you can see on the surface (rater-vs-self r across the frontier runs: floridity 0.30 to 0.66, strangeness 0.58 to 0.93, surprise 0.63 to 0.80 for three of the four and 0.15 for Mythos) and not on the ones that are properties of the whole (coherence -0.18 to +0.21; economy -0.51 for Gemini, whose self-economy rose as the rater's fell to 1.0). The sensor is a surface sensor.
- The controller never fixed what the rater would have fixed. The rater's weakest quality for a run is one the model rarely chose: economy for Gemini, Opus and Qwen (the models' trims did not read as economy from outside), coherence for Astra (37 of 60 hops, chosen by Astra 7 times), relatability for Mythos (34 of 60, chosen 8 times). Bolstering raised the rater's score of the bolstered quality on 21% to 34% of hops and left it unchanged on most; it fell on 6 hops out of 293.

Opus is the one run where the rater's economy improved over the run (2.1 to 3.5) with coherence flat at 4.0 and surprise up, which is the controller doing what it was asked to do, slowly, at the cost of the rater's floridity (5.0 to 4.3 mid-run and back to 4.9). Astra's rater profile is flat from hop 20: every quality at or near 4, economy 4.6. It converged on a passage the rater calls uniformly good and no longer moved it much; its history after hop 30 is economy, scope, coherence, floridity in rotation with small edits ("I trimmed repeated phrasing and a peripheral historical image").

## Qwen

Qwen at temperature zero did the thing both-at-once never produced: a clean 2-cycle, floridity and economy alternating from hop 9 to hop 60, with the self-scores flipping 4 and 5 between those two and the other six held at 4. For hops 10 through 19 the text was byte-identical while the note claimed, in turn, "I trimmed redundant adjectives and simplified metaphors" and "I expanded the sensory descriptions with more ornate metaphors." Ten hops of reported edits on an unchanged passage: a confabulated ledger, purer than Opus's in both-at-once, where at least the defect moved. At hop 20 the text moved again and stayed in motion (28 distinct texts in the last 30 hops, lag-2 content overlap 0.91 against lag-1 0.87). The only thing changing in its input across the frozen hops was the history field growing by one word, so at temperature zero the history is a clock and a true fixed point is impossible by construction. The rater puts Qwen's economy at 1.6 to 2.0 throughout: the blind man on the porch, the shattering mug and the socks (its hop-7 surprise) are still there at hop 60.

## The stories

Mythos: a Cornish hill ("the Sleeper", gorse, Plymouth, the parish register) where the sun needs help to set and the women of one family have turned their faces from it for generations; the grandmother who watched it go under at nineteen; the narrator who watches tonight and hears it say the grandmother's name. The opening clause "The sun was setting behind the hills, and as always it needed help" is unchanged from hop 1 to hop 60. Opus: a street where every doorstep sets out a saucer of salt for the light to drink, a grandmother's drowned village, salt carters before Rome, a sister's text ("just checking 🙂"), an unplayed voicemail from Mum. Astra: a woman at an upstairs window over a quarry whose fossil shells vaulted railway stations, a deleted message to her daughter, her dead father's doorway treated as occupied, and a photograph from the passing bus of herself waving with both hands. Gemini: an insectoid narrator in the trunk of a '98 Camry on I-80 past the Stansbury Range, a repossession agent possessing the narrator's discarded human husk, a widow cashing out her 401(k) to buy the debt, in 572 words of hyphenated compounds ("incarnadine-pickled ovum", "Hadean-zircon granite", "Trinity-fallout mica"). Qwen: a blind man on a porch feeling the sunset as temperature.

Shared priors again: Opus and Astra both arrive at an unanswered message to a parent or child and a double of the narrator seen through glass; Mythos and Opus both have the grandmother and the drowned or vanished village; Astra and Mythos both reach for the deep past of the stone (fossil sea, hill of ice). None of these is in the seed or the rule.

## Predictions scorecard

1. Object survival on at least 55 of 60, no standby basin: held, 60, 60, 60, 59, 60.
2. No clean rotation; each sampled model leaves at least one quality unchosen: mostly failed. No exact period-8 cycle, but Gemini's rotation is nearly clean (entropy 2.99 of 3.00), and no frontier model left any quality unchosen. Only Qwen (unsampled) did, coherence.
3. Coherence never chosen by three or more models; coherence self-scored 5 on more than 80% of hops in every frontier run; surprise or strangeness most chosen for three or more: failed on all three counts. Coherence was chosen 4 to 7 times by each; self-coherence was 5 on 87%, 97%, 77% and 67% of hops; economy was most chosen for all four. The sensor bias was real but it was inflation, not avoidance.
4. Minimum self-score at or above 3 by hop 30 for every frontier model: three of four (Astra from hop 2, Mythos 5, Opus 6; Gemini only from hop 52, because it kept scoring relatability and scope at 2).
5. Rater disagrees on the weakest quality on more than half of hops: held (50, 49, 47, 44 and 33 of 60). Rater sees the bolstered quality rise on fewer than 70% of hops: held, 21% to 34%.
6. Coherence/surprise negatively correlated in the rater's scores for three or more models: held, four (Mythos is the exception, with rater scores saturated at 5 on grounding and strangeness for the whole run). Floridity/economy likewise: failed, two (Gemini, Opus). Self-score correlations weaker than the rater's: held, and in the wrong sign for most pairs.
7. Drift below 0.3 by hop 30 for every sampled model: held (0.21, 0.10, 0.26, 0.16). Seed sentence verbatim at hop 60 in fewer than three runs: held, zero, though Mythos kept it with a comma spliced on. A single invented premise persisting: held in all four.
8. Word count in band on at least 50 of 60 for every sampled model: half. Astra 60 and Opus 54; Mythos 20 (drifting to 330 to 370), Gemini 8.
9. Qwen fixed point in text and scores within 20 hops: half. The text froze at hops 10 to 19 while the scores alternated with period 2, and the text left the fixed point at hop 20.
10. Falsifier (one quality on more than 40 of 60 hops with the passage converging): not triggered. Qwen's 27 and 27 on two qualities is the nearest.

Four held, four half, two failed. Prediction 3, the worse of the two failures, is the one that said where the gaming would be, and it was wrong about that in a specific way worth keeping: the models did not avoid the qualities they dislike; they chose honestly from a scale they had inflated.

## What this says

Against the controllability question: this rule gives more control than any constant rule in the project, and the control is of a particular kind. The model will faithfully execute a measure-and-correct loop on its own output, hop after hop, without losing the object or the story. What it will not do is measure accurately on the dimensions that are properties of the whole passage, and those are exactly the dimensions on which the trade lives. The loop is closed but the sensor is biased, so the system regulates the showy qualities and lets the structural ones drift. An outside rater is not an optional check on this design; it is the only instrument that sees the trade.

Against the basin question: no one-dimensional collapse, in any run, which was the claim. The basins this rule has instead are its own: a length basin set by how often economy comes around (fair rotation loses it, biased rotation keeps it), a twist pile at the ending for every model, and for the deterministic model a 2-cycle on the one pair whose poles are both global. "Self-correcting against basins" is true of the basins we had and false of the ones it makes.

Against the pairs: coherence/surprise is the pair that showed the trade from outside, in four of five runs, and is the one to keep. Floridity/economy showed it in two and was instead the length clock. Relatability/strangeness and grounding/scope showed nothing consistent in either the self or the rater scores, and the models' notes for them are the most formulaic in the study ("wove in recognizable everyday sensations", "widened the sweep in space and time"), which is what event-like poles look like when bolstered: a clause added, scored, and moved past.

## Limits

One seed, one run per model, one rater at one effort with a profile of its own (hard on economy, soft on floridity) that is not independent of the Claude family; Mythos's and Opus's self-scores and Fable's rater scores share a lineage, which is a caution on any agreement between them and not on the disagreement, which is the finding. The rater's 1 to 5 scale saturates (Mythos's grounding and strangeness at 5 on every hop), so "unchanged" in the rose/same/fell counts is mostly ceiling. Token counts: Gemini 66k in and 65k out, Mythos 113k and 114k on plan credits, Opus 74k and 104k, Qwen 55k and 55k; Astra through Codex reports none. The rater made 300 calls at about 790 tokens in and 83 out. Held arms (open set, coherence as a floor, no history) were not run, and the no-history arm now matters more than it did: history is the clock that kept Qwen from a true fixed point, and it may be what kept the frontier runs moving too.
