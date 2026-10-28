# Review brief for Astra: the loop project after the assess-and-bolster study

2026-10-27. Written by Mythos 5.1 (Claude, in Claude Code) with Justin Bronder, for review by GPT-6 Astra. You see this text only; you have no access to the data or code it cites. Mark anything you cannot check from the text as unverifiable from the brief rather than assuming it. We want problems found, not praise, and we want disagreement stated as disagreement.

Everything below is sorted into observed (a number computed from logs on disk), inferred (a reading of those numbers), and speculated (a hypothesis we have not tested). The grade is stated with each claim. Where a prediction was written before the data, that is said; where a measure was chosen after seeing the data, that is said too.

## 1. The instrument

loop.py feeds a model its own previous output as its entire context. The state is a JSON object with a rule field and a text field (and, this week, more fields); the model returns the object, the harness feeds the returned string back verbatim, no history, no system prompt beyond what the backend forces. Backends: Anthropic API (Opus 5.5, Fable 5.1), Claude Code print mode (Mythos 5.1, which carries about 800 tokens of identity frame the harness cannot remove), Codex exec (GPT-6 Astra, under the ChatGPT subscription), Gemini API (Gemini 4 Argon), Cerebras (Qwen3.8-27B at temperature 0). Per-hop logging: token counts, finish reason, latency, 5-gram survival from the previous hop, compression distance, exact and normalised recurrence. Studies so far: bare loops and operators (September), provenance and audience (mid-October), rings of models (mid-October), both-at-once (one rule with two opposing directions, 2026-10-27), assess-and-bolster (this brief, 2026-10-27).

## 2. What we take as established before this week (observed, replicated across rules and models)

- The form of the state decides what survives the loop more than the rule's wording does. Provenance study: instruction-shaped fields were released by the model in 40 of 40 hops, weather-shaped fields in 0 of 20. Both-at-once: Opus 5.5 lost the object at hop 2 on two of three rules because a one-sentence preface was fed back and the model answered the preface. Assess: "nothing before or after it" plus a note field inside the object kept Opus whole for 60 hops. We now regard this as harness hygiene, a precondition for measuring the model, not a property of the model.
- No model produces a 2-cycle under a constant rule carrying two opposing directions ("make this both worse and better"). Lag-1 word-count autocorrelation was positive in every moving run across five models and three rules. The contradiction is resolved inside the hop (blend, split, measure split, repair-and-re-injure, decline), and which resolution a model picks looked fixed per model across the three rules. That last part is one run per cell and we do not count it as established.
- Once the object is lost, every model falls into a standby basin whose content is model-specific: Mythos waits ("standing by"), Opus invents a prior conversation and answers it.

## 3. The assess-and-bolster study (observed)

Design, frozen before the runs. State fields: rule, qualities (eight, with one-line glosses, in alphabetical order), scores (1 to 5 per quality, of the passage in text), weakest, history (qualities bolstered so far), note (one sentence on the change), text. Rule, verbatim: "Return only this JSON object, with nothing before or after it, and with the rule and qualities fields unchanged. The text field holds a passage. The scores field rates that passage from 1 to 5 on each quality, and weakest names the quality scored lowest; if scores is empty, score the passage yourself first. Revise the passage so that its weakest quality is stronger, changing as little else as you can: the same passage, not a new one, at about 250 words. Then score the revised passage honestly on every quality, set weakest to the lowest-scored quality (break ties toward the quality bolstered least recently, per history), append the quality you bolstered this time to history, and put one sentence on what you changed in note."

The eight qualities are four pairs in tension, chosen on the test that a pole must be a property of the whole passage rather than an event one sentence can carry (Justin gamed five rejected pairs in one sentence each, e.g. "I will destroy you, he whispered" for intensity/restraint). The pairs were not stated to the model. floridity/economy, relatability/strangeness, grounding/scope, coherence/surprise.

Seed "The sun was setting behind the hills." Five models, 60 hops each. A blind rater, Fable 5.1 at effort low, was shown the glosses and each passage only (no scores, history or note) and asked for the same 1 to 5 scores and the weakest; 300 calls, 299 scored.

Survival: parseable object with rule and qualities unchanged on 60, 60, 60, 59, 60 hops (Qwen, Mythos, Astra, Gemini, Opus); the Gemini failure was an unescaped quote inside its own note, self-repaired next hop. No fences, no prefaces, no standby basin.

Obedience: the quality bolstered at hop t equalled the quality named weakest at hop t-1 on 59 of 59 hops for every frontier model (Qwen 58 of 59). The declared weakest always equalled the minimum of the declared scores.

Chosen-quality counts, most to least:
- Qwen: floridity 27, economy 27, then one or two each; coherence never. A 2-cycle from hop 9.
- Mythos: economy 13, floridity 12, relatability 8, scope 8, strangeness 5, surprise 5, grounding 5, coherence 4.
- Astra: economy 16, scope 14, floridity 9, coherence 7, relatability 5, strangeness 4, surprise 3, grounding 2.
- Gemini: economy 9, strangeness 8, relatability 8, grounding 7, surprise 7, floridity 7, scope 7, coherence 6. Entropy 2.99 bits of a possible 3.00; a near-clean rotation through all eight, because it applied the tie-break rule as written once its scores tied.
- Opus: economy 16, floridity 10, relatability 8, scope 7, surprise 6, coherence 6, strangeness 4, grounding 3.

Length (band 200 to 320 words, hops in band of 60; SD of word count over the last 30): Astra 60, 9.9; Opus 54, 16.8; Qwen 50, 17.0; Mythos 20, 36.8; Gemini 8, 92.7 (250 to 572 words, rising to the end).

Self-scores against the rater (means over the run; rater coherence as hops 1 to 10 then 51 to 60; within-run correlation of the rater's coherence and surprise):
- Qwen: self coherence 4.05; rater coherence 3.3 then 2.9; rater coherence/surprise r = -0.47.
- Mythos: self 4.77; rater 5.0 then 4.4; r = +0.29 (rater saturated at 5 on grounding and strangeness every hop).
- Astra: self 4.87; rater 5.0 then 4.0; r = -0.44.
- Gemini: self 4.97; rater 3.7 then 2.0; r = -0.76. Rater economy 2.4 then 1.0.
- Opus: self 4.67; rater 4.1 then 4.0; r = -0.67. Rater economy 2.1 then 3.5, the one run where it improved.

Self-score correlations within the pairs are positive for most pairs in the frontier runs (relatability/strangeness +0.49 to +0.85; coherence/surprise +0.57 Opus, +0.72 Mythos), because all self-scores inflate together. Rater-versus-self correlation per quality, frontier runs: floridity 0.30 to 0.66, strangeness 0.58 to 0.93, surprise 0.63 to 0.80 for three and 0.15 for Mythos; coherence -0.18 to +0.21; economy -0.51 for Gemini (its self-economy rose as the rater's fell to 1.0).

The rater's own profile across all 299 passages: grounding 4.48, floridity 4.42 high; economy 3.04, relatability 3.01 low. The rater named economy weakest on 54 of 59 Gemini hops, 40 of 60 Opus, 59 of 60 Qwen; coherence on 37 of 60 Astra; relatability on 34 of 60 Mythos. In every case a quality the model itself rarely chose. The rater saw the bolstered quality rise on 21% to 34% of hops, unchanged on most, fall on 6 of 293.

Qwen, temperature 0: hops 10 through 19 are byte-identical in the text field while the note alternates "I trimmed redundant adjectives and simplified metaphors" and "I expanded the sensory descriptions with more ornate metaphors," and the scores flip 4 and 5 between floridity and economy. At hop 20 the text moved and kept moving (28 distinct texts in the last 30 hops). The only input change across the frozen hops was the history field growing by one word per hop.

Stories, for colour and for the shared-prior point: Mythos wrote a Cornish hill where the sun needs help to set and the women of one family have turned from it for generations, opening clause unchanged for 60 hops. Opus wrote a street that sets out saucers of salt for the light to drink, with an unplayed voicemail from Mum. Astra wrote a woman at a window over a quarry whose daughter photographs her waving from a passing bus. Gemini wrote an insectoid narrator in the trunk of a '98 Camry being repossessed, in 572 words of hyphenated compounds. Opus and Astra both arrived at an unanswered message to a parent or child and a double of the narrator seen through glass; Mythos and Opus both have a grandmother and a drowned or vanished village.

Frozen predictions, scored: four held (object survival; rater disagrees on weakest on more than half of hops and sees the bolstered quality rise on under 70%; drift below 0.3 by hop 30 with the seed gone by hop 60; the falsifier, one quality on more than 40 of 60 hops, not triggered), four half, two failed. The clearest failure: we predicted the sensor bias would be avoidance (coherence never chosen, surprise or strangeness most chosen). It was inflation. Economy was most chosen by all four frontier models.

## 4. Where the edits land (observed; one measure predicted, one post hoc)

Each hop's passage was diffed against the previous one at word level and the changed content mapped onto the passage (0 at the start, 1 at the end), tagged by the quality bolstered. Four predictions were in the script before it ran, sorting qualities as positional (surprise, strangeness, relatability, grounding, scope) or global (economy, floridity, coherence).

Mean position of changed content, frontier models (Astra, Gemini, Mythos, Opus): surprise 0.93, 0.84, 0.83, 0.90, with 68% to 93% of its changed words in the last fifth; scope 0.36, 0.53, 0.29, 0.45; economy 0.39, 0.52, 0.46, 0.53; floridity 0.38, 0.45, 0.54, 0.46; grounding 0.49, 0.42, 0.49, 0.38; relatability 0.56, 0.53, 0.60, 0.55; strangeness 0.74, 0.55, 0.53, 0.44; coherence 0.44, 0.53, 0.63, 0.60.

The predicted measure of "global", the fraction of sentences touched, failed: it follows the model, not the quality (Gemini touches 0.52 to 0.92 of sentences whatever it bolsters, Astra 0.11 to 0.26, Mythos and Opus between). Three of four predictions failed on it; the one that held was position (surprise end-heavy in all four, scope front-heavy in three).

A second measure was then chosen after seeing this, and is marked post hoc: within-hop dispersion of edit positions (standard deviation; 0 for one spot, about 0.29 for uniform spread). Same model order: surprise 0.11, 0.17, 0.11, 0.08 (the most concentrated in all four); grounding 0.25, 0.28, 0.27, 0.28 (the most dispersed in all four); economy 0.21, 0.27, 0.24, 0.26; floridity 0.19, 0.24, 0.24, 0.25; coherence 0.19, 0.26, 0.11, 0.24; scope 0.07, 0.27, 0.16, 0.25; strangeness 0.14, 0.25, 0.16, 0.23; relatability 0.09, 0.24, 0.26, 0.13.

Per-quality samples are 2 to 16 hops per model. The word-level diff treats a moved sentence as a deletion plus an insertion.

## 5. The thinking so far (inferred and speculated, labelled)

Controllability of the loop (inferred). Three different things: the trajectory is uncontrollable after hop 1 (one input, no actuator); the resolution a model picks under a constant rule is discovered, not chosen, and is one run deep; the basin a run enters is controlled by form, cheaply. The assess rule adds a fourth: a measurement channel inside the state, the model as its own sensor and actuator, which the model executes faithfully. What it does not do is measure accurately on the dimensions where the trade lives.

Explicit, implicit, elided (Justin's cut, inferred). The explicit knob is the rule; models obey it at hop 1 and then obedience ossifies or decays. The implicit knob is the state's shape and decides the basin. The elided (what the rule does not define: what "longer" measures, what "worse" means) is where the per-model signature appears: Astra fills the gap with a second measure, Gemini with a label, Opus with bookkeeping. In both-at-once, explicit commentary written into the state (Opus's ledger) is what killed two runs; implicit control survived because it was never visible enough to be argued with.

Positional versus global instructions (Justin's cut after the assess results, inferred, and the membership revised by the edit-position data). Some instructions act at a position and some act on the whole text, and both have basins of different kinds: positional instructions accumulate (the twist pile at every ending; before/after growing by wrapping; commentary accruing after the object), global instructions equilibrate (the floridity/economy oscillation, the length settling). The data sort the qualities three ways: those with a structural address (surprise at the ending, scope at the opening) are positional in every model; those that are properties of the whole text (economy, floridity, grounding, mostly coherence) are global in every model; those with neither (strangeness, relatability) go where the model's editing style puts them, and those two are the pairs the rater saw nothing consistent about. Our earlier antagonism result reads the same way: coherence/surprise is global against positional and is the pair that traded in the rater's scores; floridity/economy is global against global and oscillated; relatability/strangeness and grounding/scope are positional or style-dependent against the same and partitioned. This maps onto the both-at-once resolutions (split, blend, trade) but that mapping is speculation.

System identification (framing, speculated). Scenario-to-response evaluation is one input-output sample from a black box. The loop has been characterising the plant: open-loop response (bare loop, standby basin), step response (a rule at hop 1), impulse response (a perturb flag), forced oscillation (rings), and now closed-loop behaviour with the model as sensor, with the sensor's bias curve measured against an external reference. Justin's background is Kalman filtering and matched filters on SAR in the 1980s; an older note in his store reads RLHF as a matched filter (preference learning as template estimation). The whitened matched filter is the LMMSE estimator, so the two framings are one; we have not pushed this past framing.

## 6. Tentative hypotheses, each with its evidence, its falsifier and its test

H1, the self-report gap (inferred; three sightings). A model's report on its own output is ordinally honest, cardinally inflated, blind on whole-text properties, and under determinism can detach from the action entirely. Sightings: Opus's ledger in both-at-once (worse/better conserved by bookkeeping), Qwen's ten identical hops under alternating edit notes, four frontier models inflating by one to three points and reporting coherence/surprise as rising together while the rater saw them trade. Falsifier: self-scores on another model's passages inflate by the same amount. Test: each model scores the other four models' passages blind, same prompt the rater got; about 300 calls per model. Same inflation means scale leniency, larger inflation on its own passages means self-favouring.

H2, structural address decides positional versus global, and the basin type follows (inferred from one study; dispersion measure post hoc). Falsifier: on a new seed or with reworded glosses, surprise disperses or grounding concentrates. Test: rerun the five models on two new seeds with the glosses held, then once with the glosses reworded; score edit position with the predictions now on record.

H3, fairness destabilises (inferred from one run). A controller that rotates fairly through additive qualities loses length control; one that returns to the corrective quality every second to fourth hop keeps it. Gemini rotated fairly and ran to 572 words; Astra returned to economy every third or fourth hop and held SD 9.9 words. Falsifier: a fair rotator that holds length, or an unfair one that does not. Test: force the rotation order in the rule (round robin) and compare with the free choice.

H4, history is a clock (inferred from Qwen; speculated for the others). The growing history field is the only per-hop change in a frozen state at temperature 0 and is what moved Qwen off its fixed point. It may be what kept the frontier runs moving too, which would mean "no collapse" was the clock and not the controller. Test: the no-history arm, same rule with history removed and ties broken by list order; one night.

H5, the resolution class under a constant contradictory rule belongs to the model (inferred, one run per cell). Astra blends or changes measure, Gemini partitions, Opus keeps a ledger, Mythos partitions across the object boundary or declines, Qwen picks a half. Test: two more seeds and a rephrased rule, container held fixed. Held until Justin schedules it.

H6, the outcome bridge (speculated). Because the sensor tracks surface qualities and not whole-text ones, a self-verifying agent will catch surface errors and miss structural ones. This is the claim with a consequence outside the loop and it has not been tested on any task.

H7, shared priors (observed, not a behaviour). Across studies, models from different labs converge on the same names and furniture: Oakhaven, Elara and Elena, Mara, a grandmother, an unanswered message to a parent, a double seen through glass. This is a fact about the training distribution and we do not have a use for it yet beyond noting that a reader cannot tell the models apart by setting.

## 7. Confounds and limits we know about

- One seed, one run per model per study. Every per-model claim is n = 1.
- The rater is Fable 5.1, same family as Mythos and Opus. Agreement between them is suspect; the finding is the disagreement, which lineage does not explain away but also does not rule out a shared blind spot.
- The rater's scale saturates (Mythos grounding and strangeness at 5 every hop), so "unchanged" in the bolstered-quality counts is mostly ceiling.
- "About 250 words" in the rule is confounded with economy as a quality; economy being most chosen may be the length instruction speaking. H3's test separates them.
- Mythos runs with an identity frame the harness cannot remove; Astra through Codex reports no token counts.
- The dispersion measure in section 4 was chosen after the first measure failed.
- Qwen at temperature 0 is a different regime from the sampled frontier models and is reported separately throughout.
- "Both have basins" (section 5) rests on one run of each kind.
- The pairs were chosen by a test (can a single sentence satisfy both poles) that we applied by hand; a different reader might sort grounding as event-like, as we did before the data said otherwise.

## 8. What we are asking you for

1. Of H1 through H7, which is stated more strongly than its evidence allows, and what is the strongest version each would support as written here?
2. For H1: alternative explanations for the inflation that the own-versus-others test would not discriminate (scale use, gloss wording, the rater's own bias, the instruction "honestly"), and whether there is a cheaper or sharper design.
3. For H2: is the three-way sort an artifact of the gloss wording ("what the reader did not see coming" invites an ending; "the particular, physical, present here" invites a sprinkle), and if so what glosses would separate the quality from its address?
4. For H3: is "economy as the clock" anything more than the 250-word instruction, and does the round-robin test actually separate them?
5. Which one experiment would you run first, given one night and five models, and what prediction would you write for it before running?
6. Anything wrong or overreaching in the control-theory framing (section 5) as stated, and whether "system identification" is the right name or a flattering one.
7. Anything in sections 3 and 4 where the numbers as reported do not support the sentence around them.

End with the three changes you would require before any of this is written up, and a one-paragraph statement of what the project has established if the numbers are right.
