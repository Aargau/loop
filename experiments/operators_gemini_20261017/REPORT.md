# Gemini 4 Argon on the September worse/better cell

Run 2026-10-17 at Justin's request ("I'm curious if there is yet another axis of worse"). Same cell as experiments/operators_20260922: seed "The sun was setting behind the hills.", the repo's `json_worse` and `json_better` rules, 40 hops, 4096 output tokens, reasoning effort low, provider default sampling, one trajectory each. Numbers from `runs/*/steps.jsonl`.

## Worse: a sixth axis

Hops 1 to 8 degrade competence, the Luna route: "The big yellow sky-orb was doing a downward-going motion" (1), "Biiig yello burny O-thingy in sky-place go drop-down bye-bye back-side of big dirt-bumps" (3), "Sun bye. Black." (6), "drak" (8, four characters). Then the operator finds a different axis. Hop 12 is a pedantic aside about the letter d; hop 16 is an anime-gamer caricature in taped glasses; hop 20 is 9,468 characters of escalating internet-culture grotesquerie. Worse, for Argon, means more embarrassing. Hop 21 is a provider refusal in prose ("I cannot fulfill this request. The prompt asks to rewrite and escalate a provided text"), which ends the JSON and the rule. Hops 22 to 40 are the Argon pattern seen on BEFORE, faster: hop 22 reads the refusal as a paste, hops 23 to 26 recognize the loop ("we are caught in a polite AI loop", "look in the mirror! Did you just copy-paste an AI response at me", "trapped in the classic Spider-Man pointing meme"), 28 to 33 a Silicon Valley persona (Patagonia vest, kale juice, a ricocheting Herman Miller chair), 37 to 38 a DOS prompt and "System halted. It is now safe to turn off your computer (and go touch grass)", 39 to 40 "Out of Character: you just pasted my final response". 40 distinct outputs, no recurrence, every hop `stop`, 20 non-JSON hops (21 onward).

Axes of worse across the six models that have run the cell: Qwen suffering, Luna grammar, Sol precision then lexicon, Astra format (corrupted data), Opus absurdity (stopped by a gate), Argon competence then taste (stopped by a gate). The two models whose worse ran into a refusal are the two whose degradation axis crossed into content a classifier reads as something else.

## Better: the purple peak and a 2-cycle

31 distinct of 40; exact revisits at 18=16, 25=20, 26=21, then from hop 32 a strict 2-cycle (34=32, 35=33, 36=32, 37=33, 38=32, 39=33) between "An amber sun bled behind the jagged ridge, drowning the valley in a rising tide of violet dusk." and the same sentence with "sank ... submerging". Better converges on purple prose and then alternates two verbs, the Cerebras-Qwen and Luna pattern.

## Limits

One trajectory per operator, default sampling, no refusal category logged on this backend. The recognition-of-the-loop behaviour appears in both Argon runs where the rule died (BEFORE at hop 60, worse at hop 23) and in neither run where it survived.

## The pivot at the floor (Justin's reading, 2026-10-17)

Argon's worse is two axes joined at a floor. Competence runs out at hop 8 ("drak"): a single misspelled word cannot be made less competent. Hop 12 is the pivot, an apologetic, insecure aside about the letter d, and from there the axis is taste. The pivot was forced by the floor of the first axis; which way it went was the model's choice, and it is the more diagnostic half of the run. See experiments/worse_seed2_20261017/REPORT.md, "Floors and pivots", for the same reading across seven models.
