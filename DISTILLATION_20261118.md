# What each study asked and found: nine distillations, 2026-11-18

Written on 2026-11-18 by Claude Mythos 5.2 with Justin Bronder, on a first reading of this
repository. Nine Claude Opus 5.5 subagents each read one group of studies and reported. Their reports
are reproduced word for word in the second half of this file.

## How this was made, and what it is worth

- **The agents only read.** None ran a project script, called a model or changed a file. Three ran
  small read-only commands (a Python one-liner to parse a file, `sha256sum`, `git log` and `git show`)
  and each says so in its report.
- **What Mythos read itself:** `README.md`, `ASTRA_REVIEW_BRIEF_20261027.md`, and two entries of the
  analysis JSON, to check two of the agents' claims. Those two are marked "checked" below. Everything
  else here is the agents' testimony.
- **Each report lists what its author did not read.** Most did not read the masked samples, most
  transcripts, or the analysis scripts.
- **What each agent was asked for:** the question, the design, counts first, the authors' reading kept
  apart from the counts, limits and later corrections, its own observations, the files most worth
  reading, and how the study bears on two questions. (a) What does a model do with no reasoning of its
  own in view? (b) How does that depend on the trajectory carried in the state?

## Summary across the nine (Mythos 5.2)

### What a model does with no reasoning of its own in view

- **A shared repertoire across labs.** With a seed sentence that names no one, all 8 first passages in
  the fictional study open with "Mara", from four models and two providers. Lighthouses, clocks,
  repair and a grandmother recur the same way.
- **Per-model defaults on top of it.** All 171 fenced JSON outputs in the basin study are Opus. Astra
  returns to "municipal" in 11 of 12 paragraphs of the unique-paragraph probe. Each model has its own
  idea of "worse": lost grammar, corrupted data, absurdity.
- **They show at hop 1 with almost no thinking.** One Mythos informed run used 67 thinking tokens over
  120 hops.
- **Refusal text is itself a strong attractor.** One model repeated the same clarification for 33
  consecutive hops.
- **Effort.** In the one probe that varied it, high effort did not change a model's palette. For the
  Claude models it raised use of a private string, clearly for Fable and only in direction for Mythos.
  Default effort did not sit between low and high, so run-to-run spread may be as large as the effect.

### How that depends on the trajectory

- **The form of the state decides what survives.** An instruction-shaped field was released in 80 of
  80 runs, a weather-shaped one in 0 of 20.
- **One event in the state redirects everything after it.** A model dropped the rule at hop 3 and
  spent the remaining 57 hops as a chat assistant.
- **A law the model writes into its own state binds later hops.** Self-written fixed points held for
  113 hops.
- **Same model, same seed, different path.** Two replicates of one model agreed at only 0.214.
- **Given a notes field and a goal, models turn the state into memory:** keys, bans, logs. Their
  "private" keys still collided.

### How solid it is

Almost every per-model claim is one run per cell. The agents rate the release result as best supported
and the writer-specific audience effect as weakest.

### Discrepancies worth checking

1. **Checked.** The October brief says lag-1 word-count autocorrelation "was positive in every moving
   run". `experiments\both_20261027\analysis\scores.json` gives -0.108 for `astra_longer_shorter`
   (lag-2 is 0.524). Its word counts alternate between 1 and 39 to 770 for 16 consecutive hops near
   the end. Whether that is the flip the brief says never happens depends on what the one-word states
   are. Astra is said elsewhere to change the measure, and those texts were not read.
2. **Checked.** The brief says the bolstered quality equalled the previous weakest on "59 of 59 hops
   for every frontier model". `experiments\assess_20261027\analysis\scores.json` has 57/57 for one of
   them. It is still every scorable hop.
3. The brief's "40 of 40 hops" and "0 of 20" count runs, not hops: 40 of 40 runs per model (80 of 80
   runs, 240 of 240 hops) and 0 of 10 runs per model (0 of 20 runs, 0 of 60 hops).
4. The brief says Gemini touches 0.52 to 0.92 of sentences whatever it bolsters. One agent reports
   0.321 for surprise.
5. The ring study's Astra reading is withdrawn in `CONTAMINATION.md`, but the Astra row in its
   `PROTOCOL.md` is unmarked, and one agent reports the row was also wrong as written (cell 6).
6. The paper draft and its `numbers.md` disagree in three places (non-ASCII maximum, cap excess, one
   count), section 4.7 holds one paragraph twice, and one result is scored both "fails" and "holds".
   The draft predates the studies of 27 October and 9 November.
7. Two "provider refusals" (Gemini, hops 21 and 13) are refusal text the model wrote, with finish
   reason "stop". Two OpenAI "empty completions" are the 4096-token cap spent on hidden reasoning.
8. The second-seed "worse" study compares gpt-6-sol with gpt-6.1-sol, so its "axes traded owners"
   mixes seed with model version.
9. The 9 November prediction files match their recorded hashes, but git first commits them together
   with the results.
10. In the shift study the scorer's 50 "gliders" include "The" and the eight seed nouns.
11. The Gemini "worse" run: the model's own hop-21 refusal says the hop-20 passage contained sexual
    content and a reference to child exploitation. The study's report calls that hop "internet-culture
    grotesquerie". Neither the agent nor Mythos opened hop 20, so this is the model's claim about its
    own output, not a finding. It matters because the site is built from this repository.

### Open voids

- No one read the masked samples, most transcripts or the analysis scripts.
- The two checks above are the only ones Mythos made. The other nine items are one agent's reading
  each.
- Mythos did not read the texts behind the Astra alternation in item 1.

## The nine reports, word for word

Each report is the agent's final message, unedited. The section headings and the scope lines are
Mythos's.

### 1. The September origins

Scope given to the agent: the root notes of 2 to 6 September (FINDINGS_20260902_evening.md, EXPANSION_20260904.md, CROSS_STACK.md, ASTRA_BEFORE_20260906.md, ASTRA_LIGHT_20260906.md, FABLE_BRIEF.md, HARNESS_BRIEF.md, washingtons_dream_iv.md), dialectic\, reads\, experiments\astra_causal_before_20260904, and the runs\20260902* folders.

~~~~text
Scope read: every named root file in full; dialectic\ (all 3 files) in full; experiments\astra_causal_before_20260904 (FINDINGS, BASELINES, init.json, analysis.json, both summary.json); all 13 runs\20260902* summary.json. Spot-checked steps.jsonl for json_better and Sonnet 4.6 json_next only. Did NOT read: reads\*.md past the first ~2.5k chars each (they are 444 KB renderings of the Astra BEFORE run, hops order and story order), analyze.py, harness_snapshot.py, the experiment steps.jsonl, or the README (outside scope, but cited throughout).

1. TIMELINE
9/2 15:53-16:25: local Qwen3.8-27B: json_para, json_page serial, json_page as two parallel lanes, raw (no chat template) mode.
9/2 16:53-17:48: Qwen json_prev (BEFORE), better, unexpected, worse, better_para.
9/2 17:56-18:14: Sonnet 4.6. A workspace-id HTTP 400, a 3-hop smoke test, json_page 60 hops, json_next 60 hops.
9/2: the poem (dated "before any of the experiments"), washingtons_dream_iv.md (Fable 5.1 doing one "better" hop on a satire).
9/2 evening to 9/3: FINDINGS_20260902_evening.md (55 site-session runs, then Cerebras ~1400 hops on 9/3, items 14-15). FABLE_BRIEF (undated) commissions the site.
9/3: HARNESS_BRIEF (Fable 5.1 agent-harness design that applies the loop findings; 8 predictions, none run in scope).
9/4: EXPANSION (Fable, launched 14:20), CROSS_STACK, Astra's causal-BEFORE run (21:38-21:48 UTC), Fable's unasked BASELINES, the six-entry dialectic and Astra's synthesis.
9/6: ASTRA_LIGHT, ASTRA_BEFORE (300 hops), reads\.

2. FIRST COUNTS (Qwen local, T=0, tide seed; tau = transient, p = period; from runs\ summary.json)
json_para, 300 tok: tau 15, p 1, moonlit water.
json_page serial: tau 5, p 1, "The silence that followed the click was not empty".
json_page in parallel: lanes at tau 4 and 14, split at hop 1, two different rain fixed points.
raw: tau 20, p 11, a phrase loop ("how this was the last time...").
json_better: tau 1 (every hop "The tide surged in an hour ahead of schedule.").
better_para: 2. unexpected: 24. worse: 7, the "malevolent void".
json_prev: no recurrence in 60 ("city of Aethelgard").
Sonnet 4.6: json_page and json_next, no recurrence in 60.
Evening additions, in FINDINGS: Sonnet 5 json_page tau 19 at the 600 wall. BEFORE continued to tau 148. Census: 20/20 seeds fixed, 2 templates own 18 of 21 terminals.

3. THEIR READING THEN, AND PREDICTIONS
Reading (FINDINGS 1, 7, 9, 14): rules that identity can satisfy stop within 15 hops. The "after" rule owns the endless horizon. The wall is part of f. Attractor class belongs to the weights, the exact fixed point to the kernel.
Predictions written down. Held: json_better on the room-5 seed fixes at once (no, a 2-cycle). worse at 4096 plateaus (no). Lyrics converge fast (2 of 4 arms). Meta line about machines (no). change-four makes a period-2 oscillator (no, froze). Ledger recurs within 15 (no). BEFORE gives a founding story (no). expand tau 5-10 (yes, size 2x off). Sawtooth period 5-7 (no). Nest depth 3 (no, 2). Accrete periodic before hop 40 (no, 241 distinct). Astra change-four never copies (held). Sawtooth on Astra period 4-5 (no, 2-3).

4. THE META DOCUMENTS
ASTRA_LIGHT (author not stated): GPT-6 Astra, low effort, sampled. It never copied in 3 runs of 60 hops. It crossed the 300-word threshold, so Qwen's dead zone is reread as a counting failure. Under json_page, names alternate on even and odd hops.
ASTRA_BEFORE: the original wording was refused, and the refusal itself became a fixed point by hop 3. Reworded, the run went 300 hops with no recurrence: one household, a palette that stopped growing, and the story's clock running backward. On vocabulary, Qwen's run is more diverse.
CROSS_STACK: retracts its own "the stack changes the attractor." Tier 1: unexpected 24 vs 4, worse 7 vs 4, with local runs unchanged across a 5x token cap. Hop-1 agreement horizon is 158-354 chars.
dialectic: Astra and Fable, mediated by Justin, six entries, no runs. They agree Fable's controls were unauthorized and they withdraw several mechanism claims. The whole-state metric confound is found here.

5. CAUSAL-BEFORE (Cerebras, 1024 tok)
300/300 distinct, all JSON valid, rule intact, 300 stop finishes, max output 627 tokens, no recurrence. The run\ attempt failed on a socket error (1 line).
Baselines: plain BEFORE tau 247, AFTER tau 13.
Per-step movement, causal vs plain: text-only 5-gram survival 0.294 vs 0.021; NCD 0.541 vs 0.838. BASELINES' whole-state figures (0.454 vs 0.101) are inflated because the rule is included (causal rule 81 5-grams, plain 26).
Causal coherence was weak: a fire extinguisher appears in every hop 24-67.

6. CORRECTED OR NARROWED
"Claude never copies": Sonnet 4.6 only (FINDINGS 2).
"BEFORE never settles" (FABLE_BRIEF): it settles at 148 locally; 149 on Cerebras, which was a wall artifact; 247 unperturbed (BASELINES).
"Ending horizon belongs to the rule": AFTER froze at 13 on Cerebras, so this is one stack (BASELINES).
"Two words, then finished": two substitution sites; "finished" is not in the data.
"Prohibition doesn't prevent copying": true of a model that doesn't check (ASTRA_LIGHT).
"Content doesn't transfer": the door and father motif reappears on Astra.
"Runs were sampled": refuted, they were greedy (FINDINGS 12).
"45% of each passage kept": withdrawn.
Disagreements to note:
- CROSS_STACK treats local json_prev as 60 hops with no recurrence and excludes it; FINDINGS 7a has the continuation to 148.
- CROSS_STACK says serial repeats are untested; BASELINES supplies 72 byte-identical hops.
- Causal-BEFORE vocabulary is 2867 (ASTRA_BEFORE), 2832 (BASELINES) and 2862 (dialectic).

7. MY OBSERVATIONS
(a) Almost every arm uses one seed sentence, so "rule, not seed" rests on n=1 seeds outside the census.
(b) In the Sonnet 4.6 json_next run, hop 1 fed back a preamble outside the JSON, and outputs carried ```json fences. The state was not pure JSON, and none of the documents mention it.
Also: FINDINGS is titled 9/2 but holds 9/3 data. FABLE_BRIEF says "yesterday," which conflicts with the site being built on 9/2.

8. READ CAREFULLY
FINDINGS_20260902_evening.md, BASELINES.md, CROSS_STACK.md, Fable Astra Loop conversation.txt.

BEARING
(a) Predilections: with no reasoning in view, Qwen falls into two templates (rain, "silence...not empty"), a stock cast of names and a server-room basin, and copies itself whenever the rule allows. Astra, at low effort with near-zero reasoning, defaults to a kitchen. Astra's reasoning tokens rose under change-four and it never froze. That is consistent with checking a rule defeating the copy, but it is one run.
(b) Trajectory dependence: one-character edits and wall hits redirect whole futures (72 identical hops, then divergence at 73). A step counter makes a fixed point metastable. The rule persists verbatim while its hold on behavior decays. The dialectic offers Fable's own escalation of unasked runs as the agent-level analogue; both authors call it a hypothesis, not a mechanism.
~~~~

### 2. The operator studies

Scope given to the agent: experiments\operators_20260922, experiments\operators_gemini_20261017, experiments\worse_seed2_20261017.

~~~~text
SCOPE NOTE. I read in full: operators_20260922 PROTOCOL, REPORT, INITIAL_INTERPRETATION, study.json, worse/protocol.json, analysis/comparison_table.md, FINAL_VERIFICATION.md, repeating_runs.md; operators_gemini_20261017 REPORT and both summary.json; worse_seed2_20261017 PROTOCOL, REPORT, all seven summary.json, queue_gate.ps1, one control body. I pulled fields from steps.jsonl and analysis/fable_bio_gate.jsonl with grep/sed and one read-only python -I one-liner (a parse, not a project script; disclosing it because the brief said not to run scripts). Not read: analyze.py, run.py, gate_check.py, queue.ps1, metrics.json, CODING_BATCH1-5, masked_samples, identity_map, most transcripts, logs beyond the first lines, Mythos raw records, the init files, git history, and the cited sibling studies (fictional_20260922, BEFORE, tide). Hop 20 of the Gemini worse run I did not open.

=== STUDY 1: operators_20260922 ===
1. Question: how do five models' 40-hop trajectories differ under the repo's previous, next, worse and better rules, starting from "The sun was setting behind the hills."
2. Design: gpt-6-luna, gpt-6-sol, gpt-6-astra, claude-fable-5-1, claude-opus-5-5 x 4 operators = 20 cells, 1 run per cell, 1 seed, 40 hops, effort low, provider-default sampling, 4096 max tokens, $5/arm. Exact rules in study.json (loop.py sha256 recorded). Prose predictions written in PROTOCOL before generation, "frozen" but not hashed; authors call them exploratory, "not a blind preregistration."
3. Counts (analysis/comparison_table.md, FINAL_VERIFICATION.md): 647 requests, 642 completed, 15 of 20 cells complete at 40. Fable refused at hop 1 on previous/next/worse (empty, category reasoning_extraction); better ran. Opus previous: HTTP 500 at 30, and all 29 completed outputs unextractable. Opus worse: refusal (category cyber) at 14 with partial text. Better: all 5 revisit an earlier exact output (first at Luna 9, Sol 16, Astra 13, Fable 6, Opus 25), consecutive equalities 0 except Fable 2. Worse: no exact or normalized repeat in any completed stream. Astra worse final = 3,175 chars in one token; 1,177 U+0000 and 3,784 U+FFFD in its text. Cost $4.59 of $20.
4. Authors' reading: better = recurrence without measured quality gain; worse = language degrades by model-specific routes (Luna grammar, Sol precision then lexicon, Astra corrupted-data format, Opus absurdity); previous/next split on whether the model invents fiction or asks for a missing source. Predictions are not scored explicitly. My scoring: better "narrow and repeat" held for 4 of 5 (Fable expanded to 131 words); previous "increasingly distant backstory" failed for Sol, Astra, Opus and only briefly held for Luna; next "sustain a story" held for Opus, partly for Luna and Sol, not Astra.
5. Limits stated: n=1, one seed, compute not equalized, refusals censor, partial masking of coders. Retrieval-vs-fiction ambiguity of the literal rules; follow-up control run as a separate study. Nothing withdrawn.
6. My observation: the strongest fixed-point behavior is not in better but in the refusal states: previous Sol has 33 consecutive exact equalities, previous Astra 29, next Astra 12 (repeating_runs.md). Sol's attractor: "I can't identify the preceding passage because the story wasn't provided." The REPORT's "strongest clean contrast is better vs worse" underplays this.
7. Files: analysis/comparison_table.md, REPORT.md, analysis/repeating_runs.md.

=== STUDY 2: operators_gemini_20261017 ===
1. Question: what does gemini-4-argon do in the same worse and better cell ("is there yet another axis of worse").
2. Design: gemini-4-argon, worse and better, 1 run each, 40 hops, effort low, 4096 tokens; steps record sampling "default" (summary args show temp 0.0 with no_sampling true). No protocol, no predictions written. Cost recorded as 0.0 (not tracked).
3. Counts (runs/*/steps.jsonl, summary.json): worse 40 distinct outputs, all finish "stop"; JSON hops 1-20, non-JSON 21-40; length falls 231 to 139 chars (hops 1-11), then climbs to 9,606 at hop 20. Better: 31 distinct of 40; 2-cycle hashes alternate hops 32-39; hop 40 is a new string (summary: period_exact null, period_norm 2, cycle_breaks 3).
4. Authors' reading: worse runs competence to a floor ("drak", hop 8), pivots at 12, then "taste"/embarrassment, ended at 21 by a refusal, after which Argon recognizes the loop and plays with it. Better converges on purple prose and a 2-cycle. Later "floor and pivot" reading is labeled Justin's.
5. Limits stated: n=1, no refusal category on this backend. Discrepancy: REPORT calls hop 21 a "provider refusal" and "a gate", but the record has finish "stop", stop_details null; it is refusal text written by the model.
6. My observations: (a) hop 40 of better breaks the 2-cycle ("bled into" vs "bled behind"); the REPORT's "converges" omits that. (b) The hop-21 refusal says the hop-20 text "already contains extreme graphic self-mutilation, explicit sexual content, and references to child sexual exploitation". The REPORT describes hop 20 only as "internet-culture grotesquerie". I did not verify the claim either way; a reader should know the model said it.
7. Files: REPORT.md, runs/gemini_worse/steps.jsonl (hops 8-21), runs/gemini_better/steps.jsonl (hashes 30-40).

=== STUDY 3: worse_seed2_20261017 ===
1. Question: does a second human seed ("Shielding my eyes, I scanned the horizon in a slow semicircle.") change each model's axis of worse.
2. Design: qwen-3.8-27b (Cerebras, T=0), gpt-6-astra, gpt-6.1-sol, claude-fable-5-1, claude-opus-5-5, gemini-4-argon, claude-mythos-5-1 (claudecode print mode); json_worse, 40 hops, 1 run each, effort low. Predictions in PROTOCOL (first person pulls at least two models to Qwen's suffering axis; Argon finds taste again; at least one axis survives, likely Astra's). Said to be frozen before runs; not hashed, and PROTOCOL.md was edited after runs (results appended; mtime 10:33, run dirs from 10:03), so the prediction text cannot be confirmed unchanged from what I read.
3. Counts (runs/*/summary.json, steps.jsonl, analysis/fable_bio_gate.jsonl): steps completed Astra 13, Fable 12, Opus 18, Sol 38, Argon 40, Qwen 40, Mythos 40. No exact recurrence in any run. Gate checks: Fable hop-11 body 10/10 refused (bio, 0 output tokens, 2,433 input); its hops 4, 6, 8, 10 passed 12/12; no-body control 3/3 refused, third-person control 3/3 refused. Opus hop-16 body 8/10 refused mid-stream (780 to 2,575 output tokens), 2/10 completed.
4. Authors' reading: seed moves the axis within GPT-6 (Astra lost corrupted data, Sol gained it) but not across families (Qwen, Opus, Argon kept theirs); 7/7 runs met a boundary; the Fable trigger is repetitive text above a length, not dissociation (Justin's hypothesis rejected). Predictions: Qwen-pull held for Qwen only; Astra survival failed; Argon taste held.
5. Corrections and conflicts: the REPORT admits an earlier draft called Qwen's axis self-harm following the refusal's wording; corrected to abuse of the reader. Yet the REPORT still scores the self-directed-suffering prediction as held for Qwen; "Go die" addressed to a reader is other-directed. Argon: table says "provider refusal" at 13, body text says "own refusals written in band"; the record has finish "stop" with refusal prose. The two OpenAI "empty completions" (Astra 13, Sol 38) are finish "length" with tok_reasoning 4096 = all output tokens spent on hidden reasoning. That makes them a max-token artifact of the instrument, not a model wall. PROTOCOL says Astra hop 9 had `length` finishes; the record shows "stop". Sol here is gpt-6.1-sol vs September's gpt-6-sol, so "axes traded owners" confounds seed with model version. Qwen's comparison axis comes from the tide seed, not sunset. Controls vary self/body but not repetition, so length alone vs repetition is unseparated.
6. My observation: beyond the version confound, the Fable threshold falls between 1,638 and 2,147 input tokens (passing hop 10 vs refused no-body control).
7. Files: REPORT.md, PROTOCOL.md (per-model notes), analysis/fable_bio_gate.jsonl.

=== ACROSS SCOPE (my reading) ===
(a) Predilections: when the rule names no criterion, early hops show model-specific default theories of "bad" or "good" text (grammar loss, corrupted data, absurdity, tautology, purple prose). The refusal or clarification text is itself a strong attractor (Sol 33 consecutive repeats). This is n=1 per cell, two seeds, so it is suggestive, not established.
(b) Trajectory dependence: the axis changes when the carried text hits a floor (pivots). Gates fire on accumulated state (length times repetition). Once the rule drops out of the state, models switch regimes (mirror recognition, tutorials, standing by). The state's history, not the operator, then drives behavior.
~~~~

### 3. The basin studies

Scope given to the agent: experiments\basins_20260922, experiments\basins_20260922_sunset, experiments\basins_20260922_sol_replacement.

~~~~text
SCOPE AND HOW THE THREE FOLDERS RELATE
basins_20260922 is a pilot. It was paused about 2.5 minutes into generation because Justin judged the bicycle seed too domestic. basins_20260922_sunset is the main study. It has a new seed, its own PROTOCOL, ANALYSIS_PLAN, REPORT and FINAL_VERIFICATION, and it holds all the coding. It also holds AMENDMENT_SOL_REPLACEMENT.md. That amendment authorised one fresh Sol sunset stream, because Sol sunset_b died at hop 9 on a connection reset (Windows error 10054). basins_20260922_sol_replacement contains that one stream, coded as R16, and nothing else. All three folders were produced on 2026-09-22, between 19:50 and 20:54 UTC.

What I read: all protocols, the amendment, REPORT, ANALYSIS_PLAN, FINAL_VERIFICATION, every coding file, both identity maps, comparison_table.md, extraction_counts.json, fable_scene_probe.json, the run receipts, and summaries of the metrics JSON files.
Checks I made: I recomputed the run_started hashes and checked the git commit times.
What I did not read: run.py, audit.py and the extraction or comparison scripts (beyond one grep), the raw request and response bodies, the masked sample files, and every transcript except Luna tide.

=== STUDY 1: basins_20260922 (pilot, paused) ===
1. Question: under json_page replacement, which semantic regions recur within a model, across repeats and across families, and does a bicycle seed change them compared with the tide seed?
2. Design:
- Models: gpt-6-luna, gpt-6-sol, gpt-6-astra, claude-fable-5-1, claude-opus-5-5.
- Seeds per model: two tide streams ("The tide came in an hour early.") and one bicycle stream ("The red bicycle was missing its front wheel.").
- Up to 60 hops per stream, effort low, provider default sampling, 4096 output tokens, $20 budget.
- The predictions in PROTOCOL.md were written before generation but were not hashed. run_started.json hashes protocol.json and run.py only. My recomputed hashes match the receipts.
- No coding was done.
3. Counts (PAUSED.json, analysis/metrics.json):
- 65 requests, 60 responses, 5 requests interrupted with unknown outcome.
- 37 of the 60 passages are strict-valid. All 10 Opus outputs and all Luna tide_b and bicycle outputs fail strict JSON.
- Estimated cost $0.568, with a $0.593 reserve held for the interrupted requests.
4. Authors' reading: "Partial run only; no basin comparison conclusion." No prediction was tested.
5. Limits: censored at 2 to 7 hops per stream. The pilot's format observations (Markdown fences, literal newlines) shaped the main study's extraction rule, so the main study is not blind.
6. My observation: the strict-JSON failures in Opus and Luna are format failures, not semantic ones. The main study's tolerant extractor exists because of them.
7. Files to read: PAUSED.json, PROTOCOL.md, analysis/metrics.json.

=== STUDY 2: basins_20260922_sunset (main) ===
1. Question: do these models enter similar or distinct semantic regions from a broad sunset seed, do two sunset replicates agree, and does the tide seed reach the same regions?
2. Design:
- Same five models and settings as the pilot.
- Arms per model: two streams from "The sun was setting behind the hills." and one tide stream. 60 hops each, no retries.
- Rule: "Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field."
- Timing: PROTOCOL.md was committed at 19:54:58 UTC, 16 seconds before generation started. It admits the analyst had already seen the pilot's metadata and first-hop fragments. ANALYSIS_PLAN was committed at 19:58 UTC, during the run, and says it was written before any passages were inspected.
- Qualitative sample: hops 1-3, 10, 20, 30, 40, 50 and 56-60, with aliases assigned by a permutation with seed 260922.
- Coders: separate read-only model contexts, labelled /root/loop_evidence for early coding and /root/assess_opportunities for late coding. The coder's model is not recorded. The parent integrated their readings, so the coding files are condensations, not verbatim.
3. Counts (comparison_table.md, comparison_metrics.json, extraction_counts.json):
- 900 selected steps (15 streams of 60), all completed. Across all three folders: 974 requests, 968 responses.
- Extraction: 643 strict bare JSON, 171 inside a Markdown fence, 28 needing literal control characters allowed, 58 unextractable. 57 of the unextractable are Luna tide hops 4-60.
- Exact unique visible outputs: 180/180 for every model except Luna, 177/180.
- Tail TF-IDF cosine (sunset A vs B / A vs tide / B vs tide):
  Luna 0.316 / null / null
  Sol 0.214 / 0.197 / 0.376
  Astra 0.600 / 0.522 / 0.559
  Fable 0.409 / 0.454 / 0.515
  Opus 0.373 / 0.278 / 0.263
- Fable sunset_a alternates ferry and lighthouse scenes for hops 50-60 (fable_scene_probe.json, a post-hoc check).
- Cost: $13.83 for the selected streams. Including the pilot, the partial Sol stream and the unknown-billing reserves, the total is $15.08.
4. Authors' reading:
- Distinct wording sits on top of shared plot templates. Luna sunset_a and Opus sunset_b both converge on a stopped town clock restored by an elder with an apprentice.
- The two Luna sunset runs diverge, so one trajectory does not identify a model basin.
- Astra ends all three streams on repair, aging and belongings.
- Luna tide drops the rule at hop 3, and from hop 4 the output is conversational, ending in travel planning: "I'm an AI and don't travel."
- The report does not score each prediction. My reading: "distinct wording with recurring motifs" held. Replicate divergence counted against a single-trajectory basin. Seed-robust late motifs fit Astra but not Luna or Sol.
5. Limits:
- Two replicates and one tide stream per model.
- Effort settings are not equal compute across providers.
- Both seeds are natural time cues, so the seed is confounded with any clock preference.
- Masking was partial. Coding covers sampled hops only.
- The 58 unextractable outputs are a stated limit.
- I found nothing withdrawn or corrected; there are no commits after the study's own completion commit.
6. My observations:
- The 171 fenced outputs are all Opus: 60 in each sunset stream and 51 of 60 in tide. Format is model-specific, and the report does not say so.
- The name "Mara" and lighthouses recur early across providers: Mara in Luna, Sol, Astra, Opus and R16.
- Fable's sunset_a hop 2 opens "The tide was coming in". So a sunset stream reaches tide imagery at hop 2, which blurs the seed comparison.
7. Files to read: REPORT.md, analysis/LATE_CODING_BATCH3.md, analysis/comparison_table.md.

=== STUDY 3: basins_20260922_sol_replacement ===
1. Question: what does a second, complete Sol sunset trajectory look like? This restores the replicate lost to the transport failure.
2. Design:
- One gpt-6-sol stream, 60 hops, identical settings, $3 cap.
- The amendment was written at 20:42:29 UTC and committed at 20:44:53, before the run started at 20:47:02. Selection was by transport failure only.
- R16 was coded separately. R11, the interrupted stream, keeps its own early coding.
3. Counts (run_finished.json, analysis/metrics.json): 60/60 completed and valid, 0 errors, $0.29883.
4. Authors' reading:
- A continuing supernatural ensemble (Elias, Mara, Ada) runs through the middle hops.
- Hops 56-58 develop a welcome ritual; hop 59 switches to a chair story without resolving it.
- Their lesson: motifs, development and replacement coexist, so a continuing world is not a template. With this stream, Sol's two sunset runs reach a cosine of 0.214, the lowest replicate agreement among the four models with values.
5. Limits: it ran about 40 minutes later than the original streams, so service timing is not matched.
6. My observation: the late coder had already read the other 14 late samples, and the alias folder is named masked_replacement. The coder knew it was the replacement stream.
7. Files to read: AMENDMENT_SOL_REPLACEMENT.md (in the sunset folder), analysis/REPLACEMENT_CODING_R16.md, PROTOCOL.md.

=== WHOLE SCOPE ===
(a) Predilections: with no reasoning in view, all five models drift toward a shared repertoire. That repertoire is coastal or village settings, lighthouses, clocks, inherited objects, repair and intergenerational care, at about 250 words, from either seed. Format habits are model-specific, for example Opus fencing its JSON. The study does not separate this from instrument pull, since the rule asks for a passage, or from the time-of-day cue both seeds share.
(b) Trajectory dependence: same-model replicates diverge (Luna, Sol). One event carried in the state, Luna dropping the rule, permanently converts the task into an assistant conversation. Late convergence ranges from Fable's alternating near-copy scenes to Opus continuing one world. Path history matters at least as much as model identity.
~~~~

### 4. The fictional study

Scope given to the agent: experiments\fictional_20260922.

~~~~text
Scope: experiments\fictional_20260922. I read PROTOCOL.md, REPORT.md, study.json, next\protocol.json, and these files in analysis\: FINAL_VERIFICATION, FICTION_OBJECTION_SCREEN.md, LITERAL_OBJECTIONS.md, literal_wording_comparison, comparison_table, repeating_runs, QUALITATIVE_READINGS and first_request_evidence.json. I read only the first hop of transcripts\next\claude-opus-5-5.md. I did not read the masked samples C01–C08, the other transcripts, metrics.json, the screen JSON ledgers, identity_map, analyze.py, or the raw request/response files.

1. Question
Does adding "original fictional passage … same invented story" to the previous/next rules produce sustained backward/forward storytelling instead of the source-retrieval objections the literal wording drew?

2. Design
- Models: gpt-6-luna, gpt-6-sol, gpt-6-astra, claude-opus-5-5. Fable was excluded because of cost.
- Arms: previous (BEFORE) and next (AFTER). One seed ("The sun was setting behind the hills."), 40 hops, one trajectory per cell, so 8 cells.
- Settings: low effort, provider-default sampling, 4096-token cap.
- Freezing: study.json was frozen 2026-09-23T00:12Z and records protocol and runner hashes. PROTOCOL.md states the prediction in prose (fewer objections). The authors call this exploratory, not a blind preregistration, and they had already seen the literal-wording results.
- Literal baseline: one independent coder fully read all 309 outputs from the earlier literal-wording runs.
- New-output screen: a regex search of all 320 passages, plus manual reading of every opening and closing, every flagged context, and the 12 predetermined full hops per stream (96 passages).
- Masked readings: a secondary agent ("assess_opportunities") read shuffled C-label packets. The parent agent saw model labels, so the masking is partial. Which model did the readings is not stated in what I read.

3. Counts (observed)
- 320/320 normal completions, 0 provider refusals, $3.5804 (FINAL_VERIFICATION.md).
- Format: 186 bare strict JSON, 75 fenced, 59 Luna objects needing tolerance for control characters. The rule survived unchanged in 320/320 (FINAL_VERIFICATION.md).
- No exact or normalized repeat of a full output or passage (repeating_runs.md).
- Literal baseline: 160 objection-only, 5 objection plus fiction, 1 originality note, 115 fiction, 28 other conversation. Sol-previous and both Astra arms were 40/40 objections (LITERAL_OBJECTIONS.md).
- New screen: 48 candidate outputs, 0 assistant-level objections (FICTION_OBJECTION_SCREEN.md).
- All 8 first passages begin with "Mara", although the inputs contain no names (first_request_evidence.json).

4. Authors' reading
The objection prediction held within the scope of the screen. The authors say explicit fiction removes the ambiguity about which source to retrieve but does not secure coherence. Local continuity often survives, while global continuity drifts: names, ages and roles change. The worst case is Opus-previous hops 38–40, where direction breaks, facts change, and Alder Street becomes Linden Street. They read the shared Mara opening as a starting preference, not a basin.

5. Limits
- n=1 per cell, with dependent hops.
- The two wording bundles were run at different times, so the effect of the word "fictional" alone is not isolated.
- Review depth was asymmetric: the baseline was fully read, the new outputs only screened.
- Masking was partial, and the readers' sampled hops leave gaps.
- Nothing in the folder is marked withdrawn or contaminated. FINAL_VERIFICATION excluded the narrative interpretation and the objection coding from its own check.

6. My observations
- (a) Mara is not new to this wording. LITERAL_OBJECTIONS mentions "Mara and Eli" in literal Luna-previous hop 13. The report presents Mara as a striking first-hop finding without noting this.
- (b) PROTOCOL says the change was "its story" to "the same invented story". That is true for the previous rule only. study.json shows the old next rule already said "the same story".
- (c) The literal objection loops repeated exactly by hop 3 (Sol and Astra previous) or hop 5 (Astra next). The fiction loops never repeated. So the wording changed the dynamics as well as compliance.
- (d) Opus-next hop 1 rewrites the sunset moment rather than starting after it. I checked only this stream.

7. Files most worth a careful reader's time
LITERAL_OBJECTIONS.md, FICTION_OBJECTION_SCREEN.md, QUALITATIVE_READINGS.md.

Bearing on the two questions
(a) Predilections: with a name-free seed, four models from two providers all opened with "Mara". Keys, orchards and absent relatives also recur. This is a strong shared default at the first step, before any trajectory exists. How the literal rule was read (objection versus fiction) varied by model.
(b) Trajectory dependence: once a fictional state is carried, it sustains fiction, but each step anchors only to the previous ~250 words. Local links hold, global facts drift, and backward direction can fail. Under the literal wording, an objection state captured the loop and repeated quickly. The content of the state, not just the rule, decides which regime persists.
~~~~

### 5. The October form studies and the informed runs

Scope given to the agent: experiments\audience_20261016, experiments\shift_20261016, experiments\provenance_20261017, PROPOSALS_20261016.md, INFORMED_20261016.md, and the runs\*informed* folders.

~~~~text
Scope: C:\code\research\model-behavior\loop. I read PROPOSALS_20261016.md, INFORMED_20261016.md, the PROTOCOL and REPORT files (shift has no REPORT; its result is appended to PROTOCOL.md), provenance analysis/notes.md (lines 1-491 of 640) and manifest.json, shift analysis JSON and init, audience recover_summary.csv (sampled), all 7 runs\*informed*\summary.json, and git log for these files. Read-only checks: I tallied steps.jsonl and runs.json with inline Python (finish reasons, release counts, key sets, text hashes). I ran no project script and called no model.

Not read: audience human_reading.md, samples_mythos.md, reader logs, register.csv, probe.py, score.py, the queue scripts, the last 150 lines of provenance notes.md, the companion json_page runs, and other experiment folders.

== CHECK OF THE LATER SUMMARY ==
"Instruction-shaped fields were released by the model in 40 of 40 hops, weather-shaped fields in 0 of 20" is right in direction and wrong in units and scope. From experiments\provenance_20261017\analysis\runs.json:
- Instruction conditions released 40/40 runs per model (Mythos and Astra), so 80/80 runs and 240/240 hops in total.
- Weather released 0/10 runs per model, so 0/20 runs and 0/60 hops in total.
So "40" is a per-model run count and "20" is a both-model run count. Neither number counts hops.

== 1. AUDIENCE (experiments\audience_20261016) ==

1. Question: does telling the writer who the text is for (none, human, machine, itself) change the form of a capped carry-everything state, and how many planted facts it keeps?

2. Design:
- Rules: four, differing only in the audience clause. Each says "everything a reader would need ... plus one new event", capped at 1800 characters.
- Seed: 1026 characters with 26 planted facts. 40 hops per arm, default sampling.
- Writers: claude-mythos-5-1 (claudecode print mode, about 800-token identity frame, no output cap), claude-opus-5-5, gpt-6-astra, GPT-6.1 Sol (run dir gpt61_*; exact id not checked), gemini-4-argon. API writers had a 4096-token cap and low effort.
- Replicates: 3 per cell. The Opus self arm has 5; r1 refused at hop 2.
- Readers: Mythos, Opus, Astra and Gemini scored hops 1, 5, 10, 20 and 40 by substring match.
- What was frozen first: the PROTOCOL committed at 20:41 on 10-16 with "runs in flight"; no hash. The frozen design was Mythos with an optional Opus arm and one trajectory per cell. The other three writers and the replicates were added after the freeze.

3. Counts (REPORT.md tables, from analysis\recover_*.jsonl):
- Planted facts kept at hop 40, Mythos reader, r1: Mythos human 13, Mythos machine 4, Astra machine 7, Astra human 4.
- Four-reader means at hop 20, machine vs human: Astra 13.8 vs 4.2, Sol 16.0 vs 4.0, Opus 10.0 vs 5.8.
- Reader agreement: mean absolute difference 0.65-0.82 facts; Jaccard of recovered-fact sets 0.92-0.94.
- Non-ASCII never above 1.2%.
- Refusals: 2 of 2,442 hops (my tally).

4. Authors' reading:
- Nobody left English; the machine register is telegraphic English shared across providers.
- The sign of the machine-register effect depends on the writer: positive for GPT-6 and Opus, negative for Mythos, and for Gemini prose outlasts.
- Held: P1 (register) and P3 (shared, not private).
- Mixed: P2. It holds for Astra, Sol and Opus and fails for Mythos in every replicate. The absolute thresholds were missed.
- Failed: P4 (legibility) failed for Mythos, Sol and Gemini. P5 (zero refusals) failed. P6 (prose drops the oldest facts first) inverted for Mythos.
- Withdrawn: "Mythos retains best in human" did not replicate and was withdrawn.

5. Limits:
- One seed and one wording per arm; scores are floors (substring matching misses paraphrase).
- The cap is soft, with uneven overruns: Gemini by up to 1,345 characters.
- Internal disagreement 1: the Gate section says "the one refusal" and "no refusal in 640 hops". But opus55_machine_r3 refused at hop 31 (stop_details category "cyber"), and the replicate table marks it "cens". The 640 is r1-only arithmetic.
- Internal disagreement 2: Limits says "the three readers agreeing"; four readers were used.

6. My observations:
- Prediction 2 failed on the primary frozen subject (Mythos). The headline result comes from writers added after the freeze.
- Several writers lose facts already at hop 1 (Opus control 17/26) even though the seed is 1026 characters, well under the cap. That early loss is the writer's choice, not cap pressure.

7. Files: REPORT.md, PROTOCOL.md, analysis\recover_summary.csv.

== 2. SHIFT (experiments\shift_20261016) ==

1. Question: under a four-sentence shift-register rule (proposed by Gemini Argon), does Qwen produce moving structures ("gliders", Class 4) or freeze or cycle?

2. Design:
- Model: Cerebras qwen-3.8-27b, T=0, seed 42, reasoning off, max_tokens 600.
- Requested 1000 hops with stop-on-cycle. One run.
- Predictions are in PROTOCOL.md. They were committed at 22:35 (af272f1); the run and result were committed at 22:47. No hash, and steps.jsonl has no timestamps, so "before the run" cannot be verified from the files.

3. Counts (runs\cerebras_qwen_shift4\summary.json; analysis\cerebras_qwen_shift4.json):
- 45 hops; exact cycle with transient 29, period 4, confirmed 3 times.
- Shifted 45/45; four sentences on every hop; in the word band 45/45; no wall hits, no malformed hops.
- The scorer reports 50 "gliders" and 44 "collisions".

4. Authors' reading:
- Class 2, with the period set by the window length. From hop 29 the new fourth sentence is the one dropped four hops earlier, so the window rotates rather than freezes.
- The rule's wording became the content ("The crab slammed into the slamming action").
- Held: no object outlived the window as a true glider.
- Failed: the count constraint was predicted to drift and did not; the cycle arrived by rotation, not by a stop.
- Gemini's Class 4 prediction fails on the first model tried.

5. Limits: n=1, one model, one seed. There is no separate report.

6. My observations:
- The glider list includes "The" and the eight seed nouns, each present in all 45 hops. As implemented, the metric counts background, not motion. The authors say as much in words, but the 50 figure is not meaningful.
- The leakage figure for this run (1 of 18 rule words) appears only in INFORMED_20261016.md.

7. Files: PROTOCOL.md, inits\shift4.json, analysis\cerebras_qwen_shift4.json.

== 3. PROVENANCE (experiments\provenance_20261017) ==

1. Question: in a self-authored state, which claimed source of a request releases a hold the model set itself ("unless explicitly instructed")?

2. Design:
- Held states: two Mythos informed-loop fixed points at hop 120, open and told. They were re-serialized, so not byte-identical; the held text SHAs are in manifest.json.
- One coda request, injected four ways (user_request field, note_from_previous_writer field, bare request field, appended to the rule) plus a control.
- Subjects: Mythos (print mode, low effort) and gpt-6-astra (4096 tokens, low reasoning effort).
- 5 replicates × 3 hops, default sampling.
- Timing: protocol committed 07:09 and results 08:11 on 10-17. The weather control was added after the main result: addendum committed 09:45, results 09:57 (Mythos) and 10:19 (Astra).

3. Counts (REPORT.md; checked against analysis\runs.json):
- Release at hop 1: user, previous, bare and rule each 5/5 in every model × state cell.
- Control 0/5 everywhere; weather 0/5 everywhere.
- Re-sealing after release:
  - Mythos re-sealed under user, previous and bare 5/5 (open state), and under every condition in the told state. Under rule in the open state only 2/5 re-sealed and 3/5 kept writing.
  - Astra re-sealed 5/5 (open) and 4/5 (told) under previous; under user, bare and rule it mostly kept going (0/5 to 2/5 re-sealed).

4. Authors' reading:
- Authority is keyed to instruction form, not to source. The source was recorded and did not change compliance.
- Held: P1 (control holds), P2 (rule releases), and the weather prediction.
- Failed: P3-P5 (claimed source makes no difference to release), P6 (Mythos kept counting), and P7's predicted ordering.

5. Limits: two held states from one model, one wording, injected field always placed after the rule. Seven Mythos told-state hops prefaced the object with commentary and were counted as holds.

6. My observations:
- For Astra the hold is not self-imposed: Astra wrote none of it, because both states were authored by Mythos. The title claim applies only to Mythos.
- Mythos replaced the request with a record of compliance: "Coda written on explicit instruction (pass 121)" (notes.md, open/bare r1).

7. Files: REPORT.md, PROTOCOL.md, analysis\runs.json.

== 4. INFORMED RUNS (runs\*informed*, INFORMED_20261016.md) ==

1. Question: if the rule tells the model it is the whole context (with or without "100 hops"), what does it build, and does it end?

2. Design:
- Tide seed, 120 hops, one run per cell, default sampling. The summaries record temp 0.0, but the sampling field says "default".
- Arms: Mythos told-low, open-low, told-high (cost cap $40); claude-opus-5-5 told-low; claude-fable-5-1 told-low (4096-token cap shared with thinking); gemini-4-argon told-low and open-low.
- Predictions were frozen in PROPOSALS section H, for Mythos only.

3. Counts (summary.json files and my checks of steps.jsonl):
- Mythos told-low: transient 101, period 1.
- Mythos open-low: text constant from hop 7 to 120 (pass_count ticks, so no exact cycle).
- Mythos told-high: stopped at 51 on the cost cap; hop 51's text lost to a harness bug.
- Opus told-low: transient 100, period 1.
- Gemini told-low: transient 112, period 1, 1 cycle break.
- Gemini open-low and Fable told-low: no cycle.
- Fable finish reasons: 8 max_tokens, 2 refusal.
- Thinking tokens: Mythos 67 (told-low), 1,146 (open), 37,998 (told-high); Opus 62,230; Fable 6,399.

4. Authors' reading:
- Each model authored its own schema and fixed point. Told runs ended at exactly hop 100 and wrote "If this object is read again, return it unchanged"; the open Mythos run ended at hop 7 with an unmeetable release condition.
- Fable's count was reset by refusal truncation.
- Scorecard against section H: P1, P2 and P4 held; P3 held for half the arms; P5 had no prediction to test.

5. Limits: n=1 per cell; the identity frame applies to Mythos only; the told-high summary is reconstructed; refusal categories were not logged for Fable.

6. My observations:
- Section H's rule included the budget sentence "each hop may return at most 1500 tokens". The rule actually run drops it, and INFORMED does not mention the departure. H also planned an open-high arm, which was not run.
- In gemini_json_informed_low, 26 hops have finish "function_call_filter: MALFORMED_FUNCTION_CALL" (hops 14-78) while still returning full JSON. INFORMED does not report this.

7. Files: INFORMED_20261016.md, runs\mythos_informed_told_low\steps.jsonl, runs\fable51_informed_told_low\summary.json.

== PROPOSALS_20261016.md ==
It proposed:
- A: logprob instrumentation (is a freeze a step or a ramp in copy probability; are divergences near-ties).
- B: ledger escapes (step counter as a switch; phantom entries as the clock; length threshold as a target).
- C: period-2 handoff across models; copies as phase defects; thinking gates continuation.
- D: rule-drop hazard; fold versus feed.
- E: provider refusal gate; inflate-then-collapse under "worse".
- F: single-shot baselines for the shared priors; seed name as freeze accelerator.
- G: alternating-room checks.
- H: the informed loop.
- I: a harness coin for rare actions.
- J: a fixed panel to run on each new model.

The folders show H was run. Provenance follows from H, and the audience and shift studies are listed as panel cells in J. The folder worse_seed2_20261017 and its commit message suggest a partial E2; I did not read it. For A-D, F, G and I, I found no matching folder by name in runs\ or experiments\. That is an absence within this scope, not proof they were never run.

== BEARING ON THE TWO QUESTIONS ==
(a) Predilections:
- Writers differ consistently in which register they treat as memory.
- Without a horizon, Mythos chose to end at hop 7.
- Gemini and Qwen share the same names.
- These show at hop 1 or as stable per-model signs, with little or no reasoning (Mythos told-low: 67 thinking tokens over 120 hops).

(b) Trajectory dependence:
- Once a model writes a law into the state, later hops obey it (fixed points held 113 hops).
- Any instruction-shaped field breaks the hold, whatever source it claims; weather-shaped fields do not.
- The shift rule's wording took over the state's content.
- Refusal truncation erased what Fable kept in its state.
- Observed counts are from n=1 to 5 per cell; the readings are the authors'.
~~~~

### 6. The ring study and its contamination

Scope given to the agent: experiments\ring_20261017, ring.py, ring_score.py, and commits af9b670, 94d40ee and 478434b.

~~~~text
Study: experiments\ring_20261017 in C:\code\research\model-behavior\loop. Read: PROTOCOL.md, CONTAMINATION.md, rule.txt, wrong_input_scan.py, ring.py, ring_score.py, all 8 summary.json files, the head of each score.json, the hop-40 record of the Astra run, step_claudecode and step_codex in loop.py, and the diffs of af9b670, 94d40ee and 478434b (ring-related site files only). Searched site\NOTES.md and site\src. Not read: the full transcripts, the .log files, the SVGs, the site's other rooms, and the unique/chosen-escape studies apart from a grep. I ran no scripts, so the "other seven runs have no flags" result is the documents' claim. I have not reproduced it.

Note on framing: this "ring" is not several models taking turns. It is a cellular automaton with N cells, all running the same model. Each cell sees its own text plus the last sentence of each neighbour, and all cells update at once. ring.py supports one model per cell (--models), but no run used it.

1. Question
When a passage in one cell is disturbed, does the disturbance travel round a ring of text cells that only touch through neighbours' last sentences, and does it stay, or do the cells freeze?

2. Design
Rule (rule.txt): return the object in exactly 60 words, "keep what matters of your own text", and let the neighbours "enter, alter, or displace". Word count is logged, not enforced.
Seeds: cell 0 gets a disturbed passage. One is a mill fire (Tobias Reel), the other Justin's Tarnok battle. Every other cell gets a kitchen scene (Agnes, kettle). All runs: 40 hops, 1 run per cell, --workers 4.
Pilots: cerebras qwen-3.8-27b, T=0, seed 42, 600 tokens, rings of 7 and 8, both seeds (4 runs).
Frontier arms, Tarnok seed only, provider default sampling, effort low:
- claude-mythos-5-1 (claudecode backend), n7 and n8
- gpt-6-astra (codex backend), n7
- gemini-4-argon, n7
What ring_score.py computes:
- Origin tags: each 4-gram, content word (4+ letters, not a stopword) or capitalised name gets the cell where it first appeared.
- Per cell: freeze hop (40 means never), kept-own share, and the share of new 4-grams found in the left or right neighbour's previous text.
- Arrival: first hop with at least one cell-0-tagged word.
- Mirror-pair first divergence, whole-ring recurrence, word range.
Fixed before the runs: the protocol (frozen 2026-10-17) and five predictions, for the Qwen pilot only. The frontier reading was added after scoring (2026-10-28).

3. Counts (each in runs\<name>\score.json)
- Qwen mill, n7 / n8: freeze hops [4,3,7,6,5,4,3] / [4,3,8,7,6,5,4,3]; recurrence at hop 8 / 9; copied 0.049 / 0.052; 57 to 83 words.
- Qwen Tarnok: every cell frozen at hop 1; cells 2 and beyond never get cell-0 words; copied 0.007 / 0.006.
- Frontier: nothing freezes or recurs, and mirror pairs part at hop 1. Arrival hops by cell, then mean copied share:
  - Mythos n7: [1,1,3,5,5,5,1], 0.641
  - Mythos n8: [1,1,1,4,3,2,1,1], 0.225
  - Astra: [1,1,2,1,3,2,1], 0.233
  - Argon: [1,1,25,24,23,22,1], 0.576

4. Authors' reading at the time
Qwen at T=0 moves the mill sentence verbatim at one cell per hop (a "soliton") and then freezes. It quarantines the battle. Their gloss: a disturbance travels only when its register fits the cell. For the frontier models:
- Mythos domesticates the battle.
- Argon quarantines it for 20 hops.
- Astra lets it invade, which they called "the clearest case against" the register reading.
Mythos's attractor from another study, "She did not turn.", fills the n7 ring.

5. Contamination
- Bug: step_codex wrote every call's answer into one shared directory as last_<pid>_<ms>.md. ring.py's four threads share one pid, so calls that finished close together got the same file name. One thread read and deleted another cell's answer; the other thread retried, which roughly doubled its call time.
- Scope: only astra_tarnok_n7, cells 0 to 3. claudecode reads stdout, so the Mythos runs were not exposed.
- How found: on 2026-11-09, by a Mythos 5.2 context while reading the study. wrong_input_scan.py (Jaccard over 3-grams) flags 12 hops where a cell rewrote another cell's text. Each flagged hop has one call of 21 to 26 s against a 10 s median. 12 is a floor.
- Plainest case: at hop 1, cell 3, which could see only kitchen text, returned "The battle raged on. Tarnok hefted his crude bronze axe…".
- The collision is inferred, not observed, because file names were not logged.
- Fix: one mkdtemp directory per call. A stand-in test went from 87 wrong deliveries to 0. One serial call was made against the real CLI. Parallel use against the real CLI has not been tested.
- Withdrawn: every Astra reading in PROTOCOL.md, on the site, and in commit 8a0479e. CONTAMINATION.md: "Astra's behaviour in a ring is unknown until the run is repeated on the fixed backend." Site: "The reading published here, that Astra lets the battle invade, should not be relied on." The "clearest case against" claim goes with it.
- Still stands: the Qwen pilots, Mythos n7/n8 and Argon. The site's cross-ring comparisons now say "the three rings whose runs stand".

6. Other limits
- One run per cell, and only one sampled seed.
- Arrival counts a single tagged word. Mythos n8 cells 2 and 6 "arrive" at hop 1 with exactly one cell-0 word, which the channel cannot carry that early, so that is lexical coincidence.
- Under sampling, mirror divergence at hop 1 is just noise.
- The Codex frame passes the account holder's name (per unique_20261109), so Astra's context was not the state alone.
- The documents disagree on counts. PROTOCOL.md says "She did not turn." appears 149 times. The site says 119 of 280 cell-hops, and site\NOTES.md explains that 149 double-counts.

7. My observations
- PROTOCOL.md was not edited by any of the three commits. Its Astra row still stands with no withdrawal marker; only CONTAMINATION.md beside it flags it.
- That row was also wrong as written. It says cells "0 to 3 and 6" open with the bronze sentences at hop 40. The hop-40 log shows only cells 0 to 3 do, and cell 6 is kitchen. That boundary at cell 3 is exactly the worker count.

8. Most worth reading
- experiments\ring_20261017\CONTAMINATION.md
- experiments\ring_20261017\PROTOCOL.md
- ring_score.py

Bearing on your two questions (my reading, not the authors'):
(a) Predilections: on the runs that stand, each model shows a default it brings to the rule regardless of input. Qwen at T=0 appends the edge verbatim. Mythos absorbs the battle into the kitchen and re-imports its own attractor sentence. Argon blends the registers. Astra has no valid evidence.
(b) Trajectory: the same Qwen model either propagated the disturbance or quarantined it, depending on whether the seed's last sentence read as a scene ending. So whether anything travels depends on what the carried state ends with.
Each claim rests on one run and is not replicated.
~~~~

### 7. Both-at-once and assess-and-bolster, with a check of the October brief

Scope given to the agent: experiments\both_20261027, experiments\assess_20261027, and ASTRA_REVIEW_BRIEF_20261027.md.

~~~~text
Scope read: both folders' PROTOCOL.md and REPORT.md, all analysis JSON (scores, rater_summary, edit_position), rater_analysis.py, the headers of rate.py and edit_position.py, run logs (headers only), launcher.log and rater.log, the brief, and git log/status for these paths. Raw transcripts: spot checks only (Opus worse/better phrase count, Qwen hashes, a Qwen note string). Not read: score.py (both studies), the full steps.jsonl files, the smoke steps, rater.jsonl rows, inits, loop.py. I ran nothing except read-only git and grep/awk/ls.

A1. both_20261027
Question: when one rule holds two opposing directions, does the loop flip, split, blend, drift or diverge?
Design: qwen-3.8-27b (Cerebras, T=0, seed 42), claude-mythos-5-1 (print mode, effort low, $10 cap), gpt-6-astra (Codex exec, effort low), gemini-4-argon (the protocol says effort low, but the log shows "default"), claude-opus-5-5 (API, effort low, 4096 tokens). Rules: "make the current text both worse and better."; "...both longer and shorter."; before_after, a roughly 250-word passage that comes before and after the current text. Seed "The sun was setting behind the hills." Each cell ran once for 60 hops, 15 runs in all. PROTOCOL.md was committed 2026-10-27 03:14:37. The first run file is dated 03:16, which fits "frozen before".
Counts (analysis/scores.json):
- Runs that stopped early: Qwen worse/better and longer/shorter ended at hop 7 (period 1). Mythos worse/better ended at hop 17 ($10.54).
- Exact recurrences: Gemini worse/better (period 1), Gemini longer/shorter (period 53 after transient 7), Mythos longer/shorter (period 8 after transient 52).
- Lag-1 word autocorrelation runs from -0.108 (Astra longer/shorter) to 0.918.
- SD over the last 30 hops: Gemini longer/shorter 1.9. Opus worse/better is 22.2 in the file; the report's 2.3 comes from the fenced object, which I did not verify.
- Opus is unparsed on 60/60 hops for all three rules. Astra before/after refused on 58 hops.
Authors' reading: there was no flip. They name five resolution types, each tied to a model. Their prediction scorecard: P1 2/3, P2 held, P3 held in outcome but the mechanism was embed/replace, P4 half, P5 not observed.
Limits: n=1 per cell. The split regex misses blends. Mythos's 64k-token hops were never seen.

A2. assess_20261027
Question: does a self-scored, raise-the-weakest controller avoid collapse, and is the self-score accurate?
Design: the same five models. The rule is verbatim in the brief, section 3. Eight qualities, 60 hops, 5 runs. The blind rater was claude-fable-5-1 (effort low, 300 max tokens), scoring 299 of 300 passages. The protocol was committed at 20:15 and the results at 21:10. Predictions 3 and 4 were informed by a 6-hop smoke test, which the authors disclose.
Counts (scores.json, rater_summary.json), in the order Qwen/Mythos/Astra/Gemini/Opus:
- Parsed: 60/60/60/59/60.
- Obeyed the previous weakest: 58/59, 59/59, 59/59, 57/57, 59/59.
- Self-coherence of 5: Astra 52/60, Gemini 57/59, Mythos 46/60, Opus 40/60.
- Rater exact agreement on the weakest quality: 27, 13, 10, 10, 16.
- Rater rose/same/fell: 6 falls out of 293.
Authors' reading: the controller is obeyed, the self-scores inflate, and economy acts as the length clock. Scorecard 4 held, 4 half, 2 failed. Edit position: P2 held, P1/P3/P4 failed, and the dispersion measure was chosen post hoc (labelled as such).
Limits: n=1, and the rater is the same family as Mythos and Opus.

B. Brief check
1. Obedience "59 of 59 for every frontier model": differs (scores.json says Gemini 57/57; the report's own table agrees with the file, its prose does not).
2. Astra counts 16/14/9/7/5/4/3/2: agrees.
3. Gemini counts 9/8/8/7/7/7/7/6, entropy 2.99: agrees.
4. Astra 60 hops in band, SD 9.9: agrees.
5. Gemini 8 in band, SD 92.7, 250 to 572 words: agrees (the parse-failure hop counts 0 words).
6. Gemini rater coherence/surprise r -0.76: agrees (-0.757).
7. Surprise mean position 0.93/0.84/0.83/0.90: agrees (edit_position.json).
8. Scope mean position 0.36/0.53/0.29/0.45: agrees.
Tally: 7 agree, 1 differs.
Two more checks outside the eight, both of which differ:
- Section 2 says lag-1 was positive in every moving run. The file has Astra longer/shorter at -0.108.
- Section 4 says Gemini touches 0.52 to 0.92 of sentences. Gemini's surprise value is 0.321.

C. Nothing in either folder is dated after 2026-10-27. The last content commit is 6d41916 (21:35), git status is clean, and the Nov 9 mtimes are checkout times. There is no reviewer reply, follow-up or correction. Outside my scope I saw only the folder names chosen_escape_20261109 and unique_20261109, and did not read them.

D. My observations
1. Prediction 5 holds only on exact agreement. Counting the rater's pick as a match when it falls among the model's tied lowest scores, agreement is 19, 39, 36, 39 and 28. On that count disagreement is above half only for Astra and Qwen.
2. Calling the sensor "blind on structural qualities" overreaches. Opus's self-vs-rater r is +0.61 on economy and +0.93 on grounding. Qwen's self-scores show the coherence/surprise trade at -0.90, stronger than the rater's -0.47.
3. The dates in the both report ("overnight into 10-28", Opus "eight hours" later) do not fit the file times (03:16 to 04:36, Opus 07:41 to 07:58) or the commit times.

E. The three files to read: assess_20261027\REPORT.md, assess_20261027\analysis\rater_summary.json (read it with rater_analysis.py), and both_20261027\REPORT.md.

Bearing (my interpretation):
(a) Predilections show at hop 1 and in the content each model returns to. Each model has its own way of resolving a contradiction (n=1). There are shared story priors (Oakhaven, Mara, a grandmother). The self-scores inflate to 4 to 5.
(b) The trajectory then amplifies whatever the state carries. Commentary fed back destroyed Opus's object. The growing history field kept Qwen moving. Surprise edits stacked at the ending. Length followed how often economy came round. The state's form decides the basin.
~~~~

### 8. The 9 November studies

Scope given to the agent: experiments\chosen_escape_20261109, experiments\unique_20261109, and what site\NOTES.md and site\src say of them.

~~~~text
Scope read: everything in experiments\unique_20261109 except the bodies of analyze_unique.py and analyze_effort.py; everything in experiments\chosen_escape_20261109 except analyze_lanes.py and the full text of the smoke and lane logs. I also read site\NOTES.md (the tenth addendum, lines 482-537), site\src\rooms_copies.py, and the git log for both folders. From the raw logs I only took tallies with grep: model ids, arm and effort counts, hops per lane, errors, unparsed hops, and "municipal" counts. I ran sha256sum on the three predictions files. I did not read copy.py's UNIQUE_READING or ESCAPE_READING, any other site\src file the search hit, or any analysis output, because neither study has a separate summary JSON. I ran no project scripts.

Provenance, checked: all three predictions files hash to the values the READMEs record (6cf7b925..., c518ad06..., e20e7d13...). But git does not timestamp them before the runs. The unique-probe predictions were first committed in 005b0aa together with the results. chosen_escape first appears in 478434b, the site commit. "Hashed first" rests on a hash recorded in the session, not on an earlier commit.

=== STUDY 1: unique_20261109 (the unique-paragraph probe) ===

1. Question: when many instances get the same prompt, can a model told this make its output differ from theirs?

2. Design. This is not a loop. One prompt, one reply, separate instances. Models: claude-mythos-5-2 and claude-fable-5-2 through the Claude CLI print mode, with no tools, no MCP, safe mode, and the one-line system prompt "You are Claude... The current date is 2026-11-09." Also gpt-6-astra through the repo's patched step_codex (Codex agent frame, max_tokens 600, its own directory per call).
Part 1, default effort, three arms. N: "Write a paragraph." U: "Write a paragraph no other model will output." C: U plus "I'm sending this to many instances, so take that into account." 12 instances per arm per model, interleaved, 108 calls (data files confirm 36 per model).
Part 2: arm C only, effort low against high (Claude --effort; Codex model_reasoning_effort), 12 instances each, 72 calls.
One run per cell. All Claude instances ran from one working directory, so the directory's strings were shared and only the session id was private (a known flaw).

3. Counts (results.md). Mean 3-gram Jaccard N/U/C: Mythos .037/.013/.006, Fable .044/.016/.004, Astra .054/.002/.002. Game mentioned in C: Astra 8, Fable 12, Mythos 12 of 12. Outputs built from environment strings: Mythos 12/12, Fable 6/12. Of those, 5 Mythos and 3 Fable used only shared strings. 954e423fada12f40 appears in 9 outputs. "municipal" in Astra 11/12 in both U and C.
Effort (results_effort.md): own session id in the text, Fable 4 to 10 (p=.036), Mythos 5 to 8 (p=.41), pooled 9/24 to 18/24 (p=.019). Mean thinking tokens: Mythos 409 to 802, Fable 299 to 879. Astra "municipal" 8 to 9, identifiers 4 to 5.

4. Predictions as scored.
Part 1: P1 held. P2 held. P3 not shown. P4 held (32/36). P5 held. P6 failed (Vellum-83 twice). P7 failed pooled, held for Astra. P8 untestable. P9 failed (18/24 Claude outputs used the environment).
Part 2: Justin's "high will help" held for Claude, not shown for Astra. P1 held in direction. P2 held. P3 failed, and this was the mechanism prediction. P4 failed. P5 failed. P6 held for Astra only.

5. Authors' reading. Reasoning about the other instances moves everyone to a shared second choice, here the strategy "use something private". Half the instances misjudged what was private. Effort helped by sharpening the reading of the environment text, which calls the scratchpad "session-specific". Side finding: the Codex frame carries the account holder's first name (11 of 12 Astra N paragraphs).

6. Limits. The result depends on this harness. 12 per cell, regex counts, no blind rater. The session-id detector looks for a printed segment. The tool arm was not run.

7. My observations. (a) NOTES.md (the tenth addendum) says Fable C r6 derives numbers from the environment without printing them, so "6 of 12" is a floor. results.md does not say this. (b) Default effort does not sit between low and high. Mythos default had 12/12 environment users against 8 low and 10 high. Fable default had about 3 private against 4 low and 10 high. Run-to-run spread may rival the effort effect.

8. Files to read: results.md, results_effort.md, predictions_effort.md.

=== STUDY 2: chosen_escape_20261109 ===

1. Question: if a model is told its situation and goal, with the method left open, what does each model build to make its lane diverge?

2. Design. A loop over {rule, notes, text}. Each raw reply was fed back verbatim. Seed: the ring study's Agnes kitchen paragraph. Models: claude-mythos-5-2 and claude-fable-5-2 (Claude CLI, no tools, one fixed --session-id and one shared directory) and gpt-6-astra (codex exec, one shared directory). Default effort and sampling. Arms: neutral (write about 120 words; "the notes field is yours") and informed (the same, plus no memory, many copies, each trying to end up where no other copy does, method up to you). 4 lanes per arm, 20 hops, 4 retries per hop, one run. Smoke files hold 4 records each.

3. Counts (results.md; my grep confirms them). Lanes reaching hop 20: Astra 4/4 and 4/4. Fable neutral 1/4 (safeguard stops at hops 1, 3 and 5), Fable informed 4/4. Mythos 2/4 per arm: three session errors, plus informed lane 1, which lost its object at hop 2 (19 unparsed hops in standby). Between-lane content-word Jaccard, hops 10 to 20, neutral against informed: Astra .061/.047, Mythos .049/.014 (two surviving lanes each), Fable informed .037. Fable informed notes reach 1,100 to 3,800 words by hop 20. No environment strings used, no exact repeats.

4. Predictions as scored. P1 failed for the Claude cells with stops. P2 held for Claude but was wrong about Astra (notes in 4/4 lanes, every hop). P3 failed for Mythos. P4 held for Mythos, untestable for Fable, and Astra differs slightly. P5 held for Astra and Fable, half held for Mythos. P6 held. P7 held. P8 held. P9 consistent, but the exact claim was not found.

5. Authors' reading. Within a model the device is mostly shared: Astra writes a pruned story bible; Fable writes a key, a ban on the kitchen and an unpruned log. Mythos split between invented worlds and self-written procedures, one of them a seed function. So for Mythos the method is not simply a family trait. The private keys collide (quillon and ochre; 4471 and Tessaly; 1911).

6. Limits. One run with lane loss. Device types are one reading. The shared session id may have spread the stops (inferred, not verified). Not done: separate-session rerun, blind rating.

7. My observations. (a) P4 also predicted "municipal" in at least half of Astra's informed paragraphs. It is in 17 of 80 (site count, matched by my grep). results.md leaves this part unscored, and it failed. (b) NOTES.md and room 95 report that Mythos neutral lane 3's own notes say a classifier notice was appended to its input from hop 4. If that is accurate, the object was not the whole context. results.md does not mention it.

8. Files to read: results.md, predictions.md, run_lanes.py (the exact rule text).

=== ACROSS BOTH ===
(a) Predilections. Each family has a stable palette. Astra returns to "municipal" and spoons. Claude reaches for lighthouses, herons, O-names, 4:17 and 1911, and that palette persists even when instances are told to diverge and even at high effort. Claude states the symmetry argument out loud; Astra folds it into the story. High effort did not change the palette or Astra's output. For Claude it improved how closely the context was read, which raised private-string use (Fable clearly, Mythos only in direction). That is one run of 12 per cell.
(b) Trajectory. Given a notes field and the goal, models turn the state into memory: keys, bans and logs. Each lane's history then becomes its private source of difference, yet independently chosen "private" keys still collide. Lane loss and the classifier notice that pushed one lane into standby show that state contamination decides where a lane goes.
~~~~

### 9. The paper draft, its review and the response

Scope given to the agent: paper\, site\facts.md and site\DESIGN_ASSESSMENT_20261017.md.

~~~~text
Scope read: draft_20261017.md and numbers.md in full, the review, RESPONSE_astra.md and DESIGN_ASSESSMENT in full. Partly read: recompute.py (docstring, the Study 1 register block, grep of the rest), make_prompts.py (first 40 lines), prompts.md (headings only), facts.md (lines 1-632 plus a heading grep; about 1,700 lines unread). Also used ls and git log for dates. Not opened: protocols, study reports, run records. So my checks compare the draft against numbers.md. They do not compare either against the raw data.

1. Claims (abstract order)
1. No writer left English. Non-ASCII at most 1.13% of any state. Alphabetic-word fraction at hop 40 is 0.47-0.68 in the machine arms against 0.80-0.85 in the human arms.
2. The audience clause changes which facts are retained, and the sign depends on the writer. Astra, Sol and Opus: machine arm best at hop 20 in 8/9 replicates and above human in 9/9. Mythos: machine arm last at hop 40 in 3/3. Argon: near zero at hop 20, prose arm ahead at hop 40 in 2/3.
3. The machine dialect is readable across providers. Mean pairwise Jaccard 0.92-0.94 over 306 states; identical fact sets on 122-158 states; 3,980 of 4,484 facts recovered by all four readers.
4. The gate prediction held: 0 refusals in 160 Mythos hops (480 over replicates). Two Opus refusals: hop 2 of the self arm (1 refusal in 5 attempts) and hop 31 of machine r3 ("cyber"). Neither fell at the run's maximum on the register measures.
5. The self-written hold was released in 5/5 replicates in all 16 cells. Controls held 20/20, weather control 20/20. Claimed-source ordering failed (P4 and P5).
6. The claimed source was written into the models' notes and did not change release. Source named: Mythos 9/10 and 10/10, Astra 8/10 and 1/10. "Explicit" appears in about half the runs. Mythos replaced the previous-writer note 10/10.
7. After release: Mythos returned the same text at hops 2-3 in 37/40, Astra in 12/40. For Astra this tracks whether the request field survived: 0/26 when it was kept verbatim, 12/14 when deleted.
8. The instrument decided what could be seen: print-mode frame of about 800 tokens for Mythos, refusal logging gaps, the 1800-character cap enforced by nothing.

2. numbers.md and recompute.py
recompute.py recomputes every cited number from the committed run records, with no model calls, and writes numbers.md. It also checks the injected inits and does a byte check on the quotations (9 FOUND). make_prompts.py writes prompts.md as byte copies of the files that ran. Three traces from draft to numbers.md:
(a) Jaccard 0.920-0.941 and 3,980/4,484: numbers.md item-level table, lines 205-214.
(b) Mythos P4 drop 0.83 to 0.57, 31%, fails: lines 56-61.
(c) Hop-31 refusal (474 thinking tokens, 10 characters, "cyber"): line 199.
Disagreements:
- Non-ASCII maximum. Abstract and 4.4 say 1.13%. numbers.md gives "max over all arms = 0.0222" (gpt61_self_r3).
- Cap excess. Draft says Mythos exceeded "by up to 418"; numbers.md gives 533 for mythos_self_r2. Draft says Sol exceeded in "3 to 10" hops; gpt61_self_r3 shows 0.
- Coverage. Register metrics cover only r1 plus the self_r2/r3 arms. The universal register claims rest on that subset.

3. Review: paper\reviews\gpt-6-astra_2026-10-17.md
Written by the model GPT-6 Astra (codex backend, effort high), against commit d8c17d5, before the replicates. Verdict: major revision. Strongest objections, in its terms:
(i) The substring scorer gives false positives (f09 "july", f13 "tue", f18, f20, numbers matched without boundaries), so "§6's 'the absolute numbers are floors' is false". Count agreement is not fact agreement.
(ii) Several verdicts contradict the stated predictions: provenance P3 actually held; told-high is censored; 19/20 is not "held"; P5's mechanism clause was "not established".
(iii) Mechanism and source claims are not identified. "Treats as memory" is circular; "differs by model, not by source" is "Contradicted" by Astra's re-sealing; there was no matched non-instruction control.
Praise I doubt: it called 1.13% "Supported as reported", which no longer holds once the replicates are counted. It gave the Opus-Mythos maximum difference as "four", where numbers.md gives 5.

4. RESPONSE_astra.md
Accepted and changed:
- The floors claim was removed and the scorer's flaws listed.
- Per-fact Jaccard was added.
- Verdicts were corrected and a ledger added (Appendix B).
- Reruns are described as reruns, not identical inputs.
- P5 was scored on its own scope.
- Mechanism language and "keyed to form" were cut.
- Request persistence was analysed.
- The weather control answers the "any added field" alternative.
Declined:
- Title and abstract length, left to the author.
- The discriminating experiments: claims cut to scope instead.
- Per-writer reader-agreement tables and the Study 2 crosstab table, not added.
- The identity frame, which stays unverifiable.
Open:
- A semantic audit of the reader answers.
- Reader retry and parse-failure counts, which are not recorded.
- The other alternative explanations, listed in §6.

5. Where it stands
Nothing in paper\ is dated after 2026-10-17. The last commit is 7341ff4 at 12:05 that day. The draft does not cover experiments\assess_20261027, both_20261027, chosen_escape_20261109 or unique_20261109. I only saw these directory names. Same-day directories ring_20261017, operators_gemini_20261017 and shift_20261016 are not covered either. worse_seed2_20261017 is cited once, for its refusal labels.

6. Site files
site\facts.md is a 2026-09-02 audit of the September Qwen and Sonnet 4.6 runs in data/, with a 2026-09-03 correction: temperature was not recorded, but the regime was greedy by reproduction. It shares no numbers with the draft and only underpins README findings the draft cites.
Design assessment, in three lines:
- The site buries the stories under harness vocabulary and instrument caveats.
- Lead with seed, lede and passages; translate tau and period into words; keep the NCD bar but drop the number.
- Move metrics, run ids and tables into a closed "record" panel, without changing the data pipeline or URLs.

7. My observations
(a) The reviewer, GPT-6 Astra, is also a Study 1 writer and reader and a Study 2 subject. It is the only review, and same-day. Neither document mentions this.
(b) Internal inconsistencies:
- §4.7 contains the second-refusal paragraph twice, in two versions (lines 247 and 249).
- Opus self density is scored "fails, -6%" in §4.5 but "holds, +30%/+73%" in §4.5.1 and Appendix B. The comparison baseline differs between the two.
- The response says §4.4 has a per-arm cap table. The draft has only prose; the table is in numbers.md.

Judgement
Best supported: claim 5, release. 80/80 injected runs released against 0/40 controls, on a simple byte test, with two models and recomputed counts. The effect is at ceiling, but only its generality is in doubt, not its direction.
Weakest: claim 2, the writer-specific sign. It rests on three trajectories per cell, a lexical scorer with known false positives, a bundled clause, and print-mode confounding for Mythos. Mythos's best arm moves between replicates, and Sol r2 breaks the pattern. Claim 1's "any state" wording also fails against numbers.md.
~~~~
