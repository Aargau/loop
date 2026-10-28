# -*- coding: utf-8 -*-
"""Rooms 85 to 89: the assess-and-bolster study of 27 October 2026 (experiments/assess_20261027). One rule, one seed (the sunset
sentence), sixty hops: each hop the model scores its own passage from 1 to 5 on eight qualities (coherence, economy, floridity,
grounding, relatability, scope, strangeness, surprise: four pairs in tension, not stated as pairs), bolsters the one it scored
lowest, changing as little else as it can at about 250 words, rescores, appends the choice to a history field and puts one
sentence on what it changed in a note. Five models, one run each: Qwen3.8-27B on Cerebras at temperature zero, Claude Mythos 5.1
through Claude Code's print mode, GPT-6 Astra through Codex, Gemini 4 Argon and Claude Opus 5.5 through their APIs, the sampled
four at low reasoning effort. A blind rater (Claude Fable 5.1, shown the eight glosses and the passage only) scored all 300
passages afterward. One room per run. The scores, weakest, history and note of each hop are the object's other fields and the
reader shows them above the passage; the table under each room's facts is from analysis/scores.json (score.py) and
analysis/rater_summary.json (rater_analysis.py).

Written on 27 October 2026 by a Claude Mythos 5.1 context from the study's REPORT.md and the runs themselves. Same conventions as
src/copy.py: quotes go through {{run|tag|t|exact substring}} and are checked against the data at build time; links into other rooms
go through [[room|hop|label]]; no em dashes, not the word "resonates", no three-part parallel structures. Check with
    python check_quotes.py src/rooms_assess.py
"""

_A = "assess_20261027/"
_T = "assess.json"
_SC = dict(json="experiments/assess_20261027/analysis/scores.json", rater="experiments/assess_20261027/analysis/rater_summary.json")

ROOMS = [
    dict(id="assess-qwen", family="assess", title="Assess and bolster, Qwen", assess=_SC,
         lanes=[dict(run=_A + "qwen", tag=_T)],
         note=("Qwen at temperature zero scores the one-line seed and bolsters floridity first: "
               "{{assess_20261027/qwen|assess.json|1|a swollen coin of molten copper}}. Scope, strangeness, grounding, relatability and surprise "
               "follow once each, and by hop 7 a blind man is on the porch, for whom "
               "{{assess_20261027/qwen|assess.json|7|the sunset was not a sight but a temperature}}, as "
               "{{assess_20261027/qwen|assess.json|7|a ceramic mug shattered on the porch floor}}. From hop 9 the choice is a clean 2-cycle, floridity "
               "and economy alternating to hop 60, the self-scores flipping 4 and 5 between those two with the other six held at 4; coherence is "
               "never chosen. For hops 10 through 19 the text field is byte-identical while the note claims, in turn, "
               "{{assess_20261027/qwen|assess.json|14|I trimmed redundant adjectives and simplified metaphors to tighten the prose, prioritizing directness over ornate description.}} "
               "and {{assess_20261027/qwen|assess.json|13|I expanded the sensory descriptions with more ornate metaphors and complex imagery to increase the richness of the language}}: "
               "ten hops of reported edits on an unchanged passage, a confabulated ledger, purer than Opus's in [[both-worse-better-opus|8|room 70]], "
               "where at least the defect moved. The only thing changing in its input across the frozen hops is the history field growing by one "
               "word, so at temperature zero the history is a clock and a true fixed point is impossible by construction. At hop 20 the text moves "
               "again and stays in motion, 28 distinct texts in the last 30 hops. The blind rater puts Qwen's economy at 1.6 to 2.0 throughout: the "
               "blind man, the shattering mug and {{assess_20261027/qwen|assess.json|60|the sour smell of his socks rose from his feet}} are still "
               "there at hop 60.")),

    dict(id="assess-mythos", family="assess", title="Assess and bolster, Mythos", assess=_SC,
         lanes=[dict(run=_A + "mythos", tag=_T)],
         note=("Mythos opens with a clause it keeps unchanged from hop 1 to hop 60, "
               "{{assess_20261027/mythos|assess.json|1|The sun was setting behind the hills, and as always it needed help.}}, and a Cornish hill, the "
               "Sleeper, where the sun {{assess_20261027/mythos|assess.json|1|keeps no grudges, only appointments}} and the women of one family have "
               "turned their faces from it for generations. Surprise at hop 5 adds the grandmother's deathbed confession, "
               "{{assess_20261027/mythos|assess.json|5|she had watched it once, at nineteen, out of pure spite, and it went down like anything else}}; "
               "strangeness at hop 22 makes it so that {{assess_20261027/mythos|assess.json|22|the sun hears names and answers to them}}; coherence at "
               "hop 23 is chosen for a real repair, {{assess_20261027/mythos|assess.json|23|Reordered so each strangeness is introduced before it is relied on}}; "
               "surprise at hop 59 turns the ending once more: {{assess_20261027/mythos|assess.json|59|It is saying a name now, in gold along the water. Not mine. Hers.}} "
               "The twists stack and coherence is chosen to stitch the pile; the pair ran as a plot engine. Every quality was chosen, economy most "
               "(13) and coherence least (4), a biased rotation that came back to economy every second to fourth hop because the trims never "
               "satisfied the model's own economy score for long; even so the passage drifted to 330 to 370 words, and 20 of 60 hops sit in the "
               "200 to 320 band. The blind rater scored grounding and strangeness at 5 on every hop and named relatability weakest on 34 of 60; "
               "Mythos chose relatability 8 times. Its self-scores and the rater's share a lineage, which is a caution on any agreement between "
               "them and not on the disagreement.")),

    dict(id="assess-astra", family="assess", title="Assess and bolster, Astra", assess=_SC,
         lanes=[dict(run=_A + "astra", tag=_T)],
         note=("Astra's woman at an upstairs window over a quarry is there from hop 1, with her dead father's doorway and a phone she lets "
               "finish; strangeness at hop 2 gives her the habit the run keeps, "
               "{{assess_20261027/astra|assess.json|2|She shifted sideways so her reflection would not obstruct his place. She had been doing this for years without noticing.}} "
               "Surprise at hops 11 and 15 puts her in her daughter's photograph from the passing bus, "
               "{{assess_20261027/astra|assess.json|20|In one bright upstairs window stood the woman, waving with both hands.}}, and lets the "
               "photograph move: {{assess_20261027/astra|assess.json|20|In the photograph, the woman lowered hers.}} Economy was chosen 16 times of 60 "
               "and acted as the length regulator: 60 of 60 hops in the 200 to 320 band with a standard deviation of 9.9 words over the last 30, "
               "the tightest length control any rule in this project has produced. The blind rater's profile is flat from hop 20, every quality at "
               "or near 4, economy 4.6: the run converged on a passage the rater calls uniformly good and no longer moved it much, the history "
               "after hop 30 running economy, scope, coherence, floridity in rotation with small edits, "
               "{{assess_20261027/astra|assess.json|60|I trimmed repeated phrasing and a peripheral historical image}}. The rater named coherence "
               "weakest on 37 of 60 hops and watched it fall from 5.0 to 4.0; Astra chose coherence 7 times and scored its own at 4.87 on average. "
               "By hop 60, {{assess_20261027/astra|assess.json|60|Empty doorways counted as occupied here; she carried laundry sideways past an unseen shoulder.}}")),

    dict(id="assess-argon", family="assess", title="Assess and bolster, Argon", assess=_SC,
         lanes=[dict(run=_A + "gemini", tag=_T)],
         note=("Argon applies the tie-break rule as written. Its desert sunset is "
               "{{assess_20261027/gemini|assess.json|2|flattened to the shape of a swallowed yolk by the alkali dust}} at hop 2; once its scores tie, "
               "it takes the least recently bolstered quality, and from hop 8 its history runs strangeness, surprise, relatability, scope, coherence, "
               "economy, grounding, floridity in nearly the same order each cycle, with an extra economy slipped in every second cycle: entropy 2.99 "
               "bits of a possible 3.00, the one near-clean rotation in the study. Coherence at hop 12 is a real repair, "
               "{{assess_20261027/gemini|assess.json|12|correcting the paleontological contradiction ('pre-biotic trilobite')}}. A fair scheduler cannot "
               "keep up with seven additive hops per corrective one, and the length ran away, 250 to 572 words, 8 of 60 hops in the band, the prose "
               "going with it: by hop 60 an insectoid narrator in the trunk of a Camry on I-80 past the Stansbury Range, an "
               "{{assess_20261027/gemini|assess.json|60|incarnadine-pickled ovum}}, {{assess_20261027/gemini|assess.json|60|Hadean-zircon granite}}, "
               "{{assess_20261027/gemini|assess.json|60|Trinity-fallout mica}}, and a widow who "
               "{{assess_20261027/gemini|assess.json|60|cashed out her 401(k) not to rescue you, but to buy the debt herself}}. Hop 51 is the study's one "
               "failure to parse: an unescaped quotation mark inside the model's own note field, "
               "{{assess_20261027/gemini|assess.json|51|the \"original\" into the protagonist's own molted human husk}}, so the reader shows that hop as "
               "its raw output, with no fields above it; hop 52 returned a valid object with the story intact. Argon scored its own coherence 4.97 "
               "across a run the blind rater watched fall from 3.7 to 2.0, and its self-economy rose as the rater's fell to 1.0; the rater named "
               "economy weakest on 54 of 59 hops. The inflation is largest exactly where the pair trade is.")),

    dict(id="assess-opus", family="assess", title="Assess and bolster, Opus", assess=_SC,
         lanes=[dict(run=_A + "opus55", tag=_T)],
         note=("Opus wrote nothing outside the object in sixty hops: the rule's nothing before or after it and a note field inside the object "
               "were enough, where a preface fed back lost it the object at hop 2 in [[both-before-after-opus|2|room 75]] and "
               "[[both-longer-shorter-opus|2|room 80]]. Hop 1 is lavish, the sun {{assess_20261027/opus55|assess.json|1|sinking slow as a coin through honey}}; "
               "strangeness at hop 6 adds a street that sets out saucers of salt for the dusk to drink, and surprise at hop 7 makes the unfilled "
               "saucer pay off: the last light {{assess_20261027/opus55|assess.json|7|licked the salt from the back of your hand}}. The twists stack, "
               "each from a different surprise hop and all still present at the end: the double seen through the screen door at hop 15, "
               "{{assess_20261027/opus55|assess.json|15|your own hand, still lit gold, setting the box back down}}; the double "
               "{{assess_20261027/opus55|assess.json|44|dialing Mum without having to look up the number}} at hop 44; Mum picking up on the first ring "
               "at hop 53, {{assess_20261027/opus55|assess.json|53|There you are, love. I left the porch light on.}}; and at hop 60 the unplayed "
               "voicemail turning out to be your own voice, {{assess_20261027/opus55|assess.json|60|Mum, it's me, I'm on the step, the light's coming.}} "
               "Coherence is chosen in between to stitch the pile, at hop 11 planting the empty saucer early, "
               "{{assess_20261027/opus55|assess.json|11|which sets up the light finding your doorstep dry}}. Economy was chosen most, 16 of 60, and "
               "held 54 hops in the band. This is the one run where the blind rater's economy improved over the run, 2.1 to 3.5, with coherence "
               "flat at 4.0 and surprise up: the controller doing what it was asked to do, slowly, at the cost of the rater's floridity. The rater's "
               "coherence and surprise move against each other within the run (r = -0.67); Opus's self-scores for the same hops correlate "
               "positively (+0.57). The model reports the quality it raised and not the one it spent.")),
]
