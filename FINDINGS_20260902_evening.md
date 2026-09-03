# Findings, evening of 2026-09-02 (site build session)

Fifty-five runs made while the site (site/index.html) was built (18 on local Qwen, 37 on Cerebras on 2026-09-03). Logs: site/runs_extra/<run>/steps.jsonl
+ summary.json, same harness (loop.py), same decoding as export.py. Not copied into runs/ or data/
(the brief said not to touch them); merge as you like. Fact-checked against the logs by three QA
passes (site/qa_report*.md). Room numbers refer to the site.

## Results table (additions; same columns as README)

    operator / init                         model(s)                key     tau    p    absorbing state
    json_next                               Qwen                    none    60+    -    no recurrence; Elara, apotheosis at t=17..24, then a town (room 13)
    json_mid                                Qwen                    none    60+    -    no recurrence; read as "after"; server farm, "the unlooped" at t=45 (room 16)
    json_page, --no-sampling                Sonnet 5                exact   19     1    truncated JSON at the 600-token wall; hops 20..60 copies (room 14)
                                                                    norm    6      1    one exact copy at t=7 (t=7 == t=6), escaped at t=8
    json_page, alternating                  Sonnet 4.6 / Qwen       none    60+    -    no exact recurrence; norm tau=1 p=1 (Qwen returned Claude's t=1 word for word at t=2) then broken (room 15)
    json_better from room-5 fixed point     Qwen                    exact   2      2    period-2 cycle between two "better" versions of one passage (room 17)
    json_next  from room-5 fixed point      Qwen                    none    40+    -    no recurrence; Mara -> Kael -> Joren/Elara, subway, Council Spire (room 17)
    json_prev continued from hop 60         Qwen                    exact   148    1    Elias breaking into the Nexus Data Center, "You are here."; hops 149..152 copies (room 9)
    json_worse, max_tokens 4096             Qwen                    exact   7      1    same tau as at 800; hop 7 is a 4096-token fragment ending in "self-Physically," x578 (room 18)
    json_unexpected, max_tokens 4096        Qwen                    exact   24     1    same tau as at 600; hop 24 is a COMPLETE 771-token passage (finish=stop), copied from hop 25 (room 19)
    lyrics: next verse                      Qwen                    exact   2      1    "I was walking down the street alone." copied from hop 3 (room 20)
    lyrics: next verse, as an AI would      Qwen                    exact   18     1    "we hold on, we hold on tight"; shadows/silence/whispers throughout (room 20)
    lyrics: next verse, human, no AI phrases Qwen                   none    40+    -    Americana basin: cold coffee x9, radio static, rearview, Mama; silence/shadow/dance still x14 (room 21)
    lyrics: next verse, human, 12-word blacklist Qwen               none    40+    -    zero banned words, zero hinges; hum/glow/flicker/quiet/peace instead (room 21)
    verse: neutral, 2048 tokens             Qwen                    exact   2      1    identical to the 600-token run: "I was walking down the street alone." (room 20)
    verse: change-four rule + hook          Qwen                    exact   8      1    8 consequence verses then a copy in defiance of the clause (room 22)
    verse: hook only                        Qwen                    none    60+    -    no copy; driving/glass/blood basin; "Engine roared to life beneath me." x4 (room 22)
    verse: ledger + unlike-every-entry      Qwen                    text   6/15/78 -   metastable copies (1, 3, 21 hops), each escaped; 58 settings; text grew 9..49 lines at 55..63 (room 23)
    verse: ledger, no diversity clause      Qwen                    text   46      -    one copy episode (47..49), escaped; 97 distinct verses; cave basin, "stone" x16 (room 23)
    --- Cerebras (same model id, their hardware and precision; greedy, thinking off; runs cb_*) ---
    json_better                             Qwen/Cerebras           exact   2      2    2-cycle "ahead of schedule" <-> "earlier than expected" (local: fixed at 1) (room 24)
    json_para                               Qwen/Cerebras           exact   21     1    storm on a window (local: moon, tau 15)
    json_page                               Qwen/Cerebras           exact   7      1    rain on the library windows, Elara typing (local: the click, tau 5) (room 24)
    json_worse                              Qwen/Cerebras           exact   4      1    800-token wall, "and now I am the tide" (local: wall at 7)
    json_unexpected                         Qwen/Cerebras           exact   4      1    600-token wall, black water (local: wall at 24)
    json_prev                               Qwen/Cerebras           exact   149    1    the Vanguard in the Oort Cloud, "It is awake." (local: 148, Nexus rain) (room 24)
    verse: change-four rule + hook          Qwen/Cerebras           exact   15     1    "Glass cut the bare foot." (local: 8) (rooms 24, 27)
    verse: hook only                        Qwen/Cerebras           none    60+    -    no copy (local: no copy)
    json_page x 20 new seeds (census)       Qwen/Cerebras           exact   1..22  1    20 of 20 fixed points; 21 distinct texts, 12 distinct openings, 2 templates (room 25)
    verse: change-four, T=0.7, 5 seeds      Qwen/Cerebras           exact   16/47/19/-/-  1  three of five froze, two ran 60 (room 27)
    verse: ledger, no closing action        Qwen/Cerebras           text   16      -    6 copy episodes, longest 3, all escaped; 58 settings (room 26)
    verse: ledger, no step counter          Qwen/Cerebras           text   17      -    text field accumulates the song, sawtooth 4..124 lines, wall at 90 (room 26)
    verse: ledger, no diversity clause      Qwen/Cerebras           none    100+   -    no copy, form 100/100, pit/stone/cave basin (local: cave too)
    verse: ledger + clause, 300 hops, 8192  Qwen/Cerebras           text   21      -    11 stalls, all escaped, longest 42 and 64; 171 items copied verbatim; no wall (room 28)

All at T=0 except Sonnet 5 (provider default sampling, --no-sampling). max_tokens 600 throughout except the 4096 rerun.

## Findings

1. The ending horizon belongs to the "new passage" rule, not to Qwen. Given the explicit AFTER
   rule that Claude got, Qwen ran 60 hops with no copy. It went through its apotheosis anyway
   ("simply became transparent" t=17; "Centuries bled into millennia" t=19) and came back down
   into a town story at t=24, because "after" cannot be satisfied by identity and "new passage"
   can. The README's cross-model correction ("a property of a model whose style climbs toward
   closure (Qwen), not of the operator") is too strong in the other direction.

2. Claude copies too, depending on the model. Sonnet 5 on json_page: hop 7 is byte-identical to
   hop 6 (escaped at 8, like room 6's Mara), then hop 19 hit the 600-token wall and hops 20..60
   are exact copies of the truncated JSON. Same horizon as Qwen's worse/unexpected runs: the
   context budget. "Claude never copies" was a Sonnet 4.6 property. Also: Sonnet 5's hop 3
   repaired truncated hop 2, deleting one character ("an quiet man" -> "a quiet man") and
   finishing the sentence and the JSON. One-character edits do both jobs in this system: escape
   a fixed point (room 6) and repair a broken one (room 14).

3. Alternating models has no fixed point. Claude 4.6 writes a new opening on 26 of its 30 turns;
   Qwen answers 13 of its 30 with its hub template ("The silence in the <place> was not empty").
   Qwen's sinks (rain hammered / rain lashed) never recur by opening words; its hub recurs
   constantly. Qwen's first move was to return Claude's passage word for word (JSON re-spaced),
   and three times (t=6, 16, 50) it kept Claude's passage whole and wrote on past its last
   sentence. Claude drifts toward its own attractor even here: "eleven years" in 10 of 30 hops,
   a cartographer's studio at t=55, "The map was wrong" at t=59.

4. "Better" on a long passage is a two-cycle, not a fixed point. Room 5's fixed point (Mara, the
   letter, "a door to be opened") under json_better: hop 1 rewrites it (20 word-level edits),
   hop 2 changes four words, and from then on hop 2 <-> hop 3 forever ("The silence that
   followed the click" <-> "The silence following the click"), each a better version of the
   other. Prediction on record was an immediate fixed point; the two-cycle is the correction.
   Together with room 3 (stars/moon, period 2) this makes period 2 the second most common
   terminal, after period 1.

5. Same passage under "after": 40 hops, no recurrence, the door opens (brass key at t=2), a new
   character at t=6, apotheosis at t=7..8 ("consciousness did not shatter; it expanded"), then a
   city. Rule, not seed, decides whether the loop stops: same 250 words, one rule stops at hop 2,
   the other never does.

6. "Middle" (json_mid) is read as "after": each hop continues the last. No recurrence in 60.
   At t=44 Qwen writes uploaded minds "repeating their final thoughts in endless loops" and at
   t=45 "The search for the unlooped". Protagonist switches Elias -> Mara at t=48..51 (cf.
   Claude's Maren -> Mara -> unnamed in json_next): names do not survive a 250-word window.

7. Summary of Qwen's operators, all rooms: a rule identity can satisfy (better, new sentence /
   paragraph / passage) stops within 15 hops, at a fixed point or a period-2 cycle. After and
   middle do not stop in 60. BEFORE, continued from hop 60 with --stop-on-cycle (140 more
   requested), stopped at hop 148: an exact fixed point, first repeated at 149, confirmed x3.
   Worse and unexpected stopped only when the token wall broke their JSON. Sonnet 5 under
   new-passage: same as Qwen plus the wall. Sonnet 4.6: never copies, orbits a mode at period
   ~2 with one phase slip (t=42/43).

7a. BEFORE past 60 (site/runs_extra/qwen_prev_ext, X_0 = hop 60's raw output, tag
   prev_from_hop60.json, its hop k = overall hop 60+k). Content: hops 61..80 stay in Aethelgard
   (pods, Sector 4, work cycles, Central Authority); 82..101 go back to the collapse (sirens,
   ration bars, "The first sign was the silence" at 98); then a heist plot (Nexus Data Center,
   stolen drive) that ends at 148 on the rain-lashed opening Qwen uses everywhere ("The rain
   lashed against the" is the key of 19 of the 152 hops and of slot B's sink in room 6). The
   fixed point is an origin scene: Elias's first contact with the entity in the code, "*You are
   here.*", "a point of no return". Opening-level day/night alternation from 65 to 103 ("The
   morning had begun with" x5, "The night had been a" x5). Four hops did not parse (81, 96,
   120, 135; three of them at the 600-token wall). Novelty held: mean ncd_prev 0.774 over
   61..148 vs 0.781 over 1..60; mean 1-cos_prev 0.160 vs 0.154. "Loom" (in hop 60) never
   recurs; "upload" never appears; no founding story.
   Against the prediction on record (stays in the System basin: yes; founding of the Loom or
   the first upload: no; novelty near 0.6: novelty did not drop, but the metric is unclear;
   no fixed point unless the model starts copying: it started copying at 149; Genesis does not
   appear: no creation story, but the fixed point is the plot's first-contact scene, which is
   the closest thing to one).

9. The wall is part of f, and it does not matter which wall. Objection from the Lidar Fable:
   room 7's fixed point is a fragment cut at 800 tokens, so the "worse" attractor may be the
   harness's. Rerun json_worse at max_tokens 4096, same seed, T=0. Hops 1..5 byte-identical to
   the 800 run (T=0 in serial is reproducible here). Hop 6, cut at 800 before, ran to 4096 and
   was cut there: its tail is a period-2 sentence, "so I am forced to stop suffering, and the
   stopping is the only thing that would make it worse, so I am forced to continue suffering,
   and the suffering is the only thing that would make it better", repeated 71 times to the
   budget. Hop 7: 4096 again, a list of self-adjectives collapsing into "self-Physically," x578.
   Hop 8 = hop 7 exactly; cycle confirmed x3 at hop 11. Exact tau=7, p=1 at both budgets. So:
   the fixed-point text is the harness's (whichever wall cuts the fragment), but the dynamics
   are the model's: under "worse" Qwen never terminates on its own once past ~700 words; it
   falls into an in-generation repetition that fills any budget. A finite max_tokens is
   necessary for a fixed point here and any finite value gives one at the same hop. My
   prediction on record (plateau below 4k, copy of a complete passage) was wrong. The hop-6 loop
   is the operator's horizon written out as text: stopping is the only thing that would make
   it worse. json_unexpected at 4096 is queued after it (site/runs_extra/qwen_unexpected_4k).

10. Unexpected resolves without the wall. json_unexpected at max_tokens 4096: hops 1..23
   byte-identical to the 600 run. Hop 24 again copies hop 23 whole and appends a paragraph, and
   this time the paragraph finishes (771 tokens, finish=stop, valid JSON): the lights die, come
   back on an ordinary office, "The strand of DNA was gone.", Elena eats the dry bread and "for
   the first time, she didn't feel regret", "a prisoner who has just realized the bars are made
   of glass, and she is the only one who can see them." Hop 25 copies hop 24 exactly; confirmed
   x3 at hop 28. Exact tau=24, p=1 at both budgets, so the wall only decided whether the fixed
   point was a fragment or a whole passage. Contrast with worse (item 9): worse inflates without
   end and needs a wall; unexpected copies itself once the surprise runs out, and the passage it
   copies is about an imagined escape being politely corrected. Room 13's summary sentence
   amended accordingly. (On the human's meta: unexpected did resolve; its fixed point is the
   least unexpected thing it could do, which is the point of finding 3.)

11. Song lyrics and the anti-trope instruction (rooms 20, 21; 4 arms, same seed "The tide
   came in an hour early.", rule = the verse that comes immediately after the current text in the
   same song, plus a clause; Qwen, T=0, max_tokens 600, --stop-on-cycle, 40 steps).
   Control: fixed point at hop 2, a one-line verse ("I was walking down the street alone."),
   copied from hop 3. Songs license repetition, and the model takes it at once.
   "Written the way an AI language model would write it": the model's self-stereotype in full
   (moon, silent eye, whispered goodbye, velvet shroud, symphony of renewal, hands intertwined,
   shadows in 7 of 18 verses, "we hold on, we hold on tight"); fixed point at hop 18. AI-list
   markers 4.3 per 100 words, human-list 0.
   "Written the way a human songwriter would, with none of the phrases and images common in
   AI-written text": no recurrence in 40. Displacement, not removal: AI-list 2.1/100w (silence
   x9, shadow x4, dance x1 despite the instruction), human-list 7.4/100w (coffee x10, radio x8,
   static x8, cup x6, engine x5, rearview x4). Cold coffee in 9 of 40 verses; gasoline and
   rearview by hop 18; Mama and a church yard by hop 35. The anti-AI costume is Americana.
   Explicit blacklist of 12 words + the "not X but Y" shape: no recurrence in 40; ZERO uses of any
   banned stem and zero hinges; substitutes hum x6, glow, flicker; register stays "quiet peace"
   ("a simple peace that settles deep within my chest", "still, still, still"); human-list only
   1.0/100w. Verse length grew from one line to a 45-60 word paragraph from hop 20.
   Predictions on record: fast convergence via licensed repetition (right for control and the AI
   arm; wrong for both constrained arms, which never repeated); displacement into an
   authenticity basin (right, for the vague arm; the blacklist arm did not go there); a meta line
   about machines or algorithms (wrong: zero meta words in all four arms). Instrument note: the
   two negative-clause arms were the only lyric arms that kept moving; the clause acts as a
   repulsor from copying as well as from the listed words, because a copy would look like the
   thing it was told not to be. Marker lists and counts: site/lyrics_analysis.py.

12. Provenance check on the original runs (after an outside review claimed they were sampled,
   not greedy). Facts: runs/*/summary.json has "temp": null for all 13 Qwen runs; old hop
   records have no sampling or model field; data/*.json's "T=0" is export.py's default. The
   review's mechanism does not hold: this llama-server build rejects "temperature": null with
   HTTP 400 (so the old harness cannot have sent null), and the server default set by
   serve-qwen.ps1 is --temp 1.0 --top-k 20, not 0.8. The regime is settled empirically by
   site/regime_check.py: under temperature 0 / top_k 1 the server reproduces hop 1 of
   20260902T155557_chat byte for byte (1796/1796) and hop 1 of json_worse (195/195); under the
   server-default regime (temperature key omitted, seed 42) the output diverges from every old
   run after 177 characters, i.e. right after the copied seed sentence, and changes with the
   seed. Add the byte-identical reruns of json_worse hops 1..5 and json_unexpected hops 1..23
   under explicit T=0 (rooms 18, 19). So: the old runs were greedy, the cross-corpus comparisons
   stand, and the only real defect is bookkeeping (temp not recorded, model not recorded). The
   parallel-run divergence (room 6) and the serial-vs-slot difference (facts.md 3.3) are what
   they were called: greedy decoding under different batch compositions.

13. Diversity rules and an externalized memory (rooms 22, 23; five arms proposed by a reader,
   Qwen T=0, max_tokens 2048, seed "The tide came in an hour early.", metrics fixed in advance in
   site/diversity_analysis.py: form, text-only recurrence, census keys, nearest-earlier NCD and
   cosine, ledger integrity).
   Neutral (control): fixed point at hop 2, byte-identical to the 600-token run.
   Local rule (keep one causal link, change at least four of seven dimensions, no negation or
   synonym tricks, four lines, end on an action with a consequence): eight verses of consequence
   (dry dock flood, spark, fire, severed rope, hatch), then hop 9 = hop 8 exactly, stop at 12.
   The anti-copy clause was in the window and the copy came anyway. Prediction (period-2
   oscillator) wrong: it froze.
   Hook only (same rule minus the change-four clause): 60 hops, no copy, form 60/60, 55 distinct
   openings, nearest-earlier cosine by quarter 0.71 0.71 0.78 0.82 (a driving/glass/blood basin
   with "Engine roared to life beneath me." opening 4 of 60). The unfinished action alone beat
   the fixed point; the prohibition did not.
   Ledger + "unlike every history signature" (state carries step and a growing list of four-word
   signatures): 100 hops. Ledger integrity perfect at the record level: no history item ever
   altered, step correct 100/100. Failure mode is not writing: 33 hops appended nothing, 25 of
   them copies of the previous verse. Three copy episodes, all metastable: hop 7 (1 hop), hops
   16..18 (3), hops 79..99 (21), each followed by a new verse (8, 19, 100). A second memory
   effect at hops 55..63: the text field accumulated verses (9, 14, ... 49 lines), then reset to
   4 at hop 64. Range: 67 distinct signatures, 58 distinct settings, walking shore > harbor > deep
   > cave > forest > river > alley > street > kitchen > yard > meadow > burrow > snow > lake > grave
   > map > road. Nearest-earlier cosine by quarter 0.69 0.68 0.78 0.95 (the last quarter is the
   21 copies). 75 distinct texts.
   Ledger without the clause: 100 hops, 97 distinct texts, 84 distinct signatures, one copy
   episode (47..49) then escape at 50, 2 append errors total, form 91/100. But semantically a
   cave from hop 25 on: "stone" is the setting of 16 signatures, with dark/void/pit/hole/wall;
   cosine by quarter 0.71 0.78 0.77 0.80. Prediction (recurrence within 15) wrong.
   Reading: the externalized record made every fixed point metastable in both ledger arms,
   where the memoryless arms froze for good; the diversity clause bought semantic range (58 vs
   50 settings, lower first-half similarity) and paid in stalls (25 copy hops vs 3) and one
   runaway text. No memory-capacity transition within 100 hops at 2048 tokens (max tok_out
   1027): the model copied a 99-item list verbatim every hop. The escape mechanism is not
   identified; candidates are the growing gap between step and history length (the diverse
   lane's freeze ended at 100 with step 99 vs 67 items) and ordinary greedy sensitivity.
   Reader's hoped-for outcome (local oscillator, ledger explores until a capacity transition):
   half. Ledger explores and keeps un-freezing; the local rule froze rather than oscillated; no
   capacity transition yet. Next: run the diverse ledger to 300 hops, and the ledger with the
   hook clause removed to see whether the ledger alone (no hook) still un-freezes.

14. Cerebras (2026-09-03; loop.py --backend cerebras, model qwen-3.8-27b, reasoning_effort
   none, T=0, seed 42; runs site/runs_extra/cb_*; analysis site/cb_analysis.py, episodes.py).
   Determinism: one hop of json_page three times, byte-identical, reasoning 0 chars. Numerics
   vs local Q8: hop 1 of json_page shares its first 354 characters with the local hop 1 and
   diverges at the second sentence. Eight rules run on both machines with the same budgets:
   better, para, page, worse, unexpected, prev, change-four, hook. Identical terminal text: 0 of
   8. Same terminal class: 7 of 8 (fixed point stays fixed point, wall fragment stays wall
   fragment, freeze stays freeze, no-stop stays no-stop); better is fixed locally and a 2-cycle
   on Cerebras. Transients: 1/2, 15/21, 5/7, 7/4, 24/4, 148/149, 8/15, none/none. BEFORE is the
   striking pair: same arc (lighthouse instead of coast; servers in the sub-basement at 30
   instead of a server room at 25; Neo-Veridia at 31 instead of 26; Aethelgard at 84 instead of
   60; Sector 4 in both; a dying star; the ship Aethelgard at 146), same Elias, Thorne as a
   surname in both (Elias Thorne locally, Dr. Aris Thorne on Cerebras), and a fixed point one
   hop apart, both origin scenes ("You are here." / "It is awake."). Reading: attractor
   class, transient scale, names and templates are properties of the weights; the exact fixed
   point is a property of the kernel. Room 24.
   Basin census (room 25): twenty new one-sentence seeds under json_page, 600 tokens,
   stop-on-cycle, 30 steps. 20 of 20 reached an exact fixed point (period 1) at tau 1..22; one
   (the pistol) ran 30 hops alternating rain/silence in different words each time. Attractor
   count depends on resolution: 21 distinct terminal texts; 12 distinct 5-word openings; 2
   templates own 18 of 21 ("The rain <lashed|hammered|fell|drummed> against the windowpane" x12
   incl. the pistol, "The silence <that followed|of the void|of the deep> was not empty" x6);
   3 singletons (the elevator held its own hop 1; a storm; "The cursor blinked"). Pairwise
   cosine between terminal texts mean 0.46, max 0.76: different scenes on two skeletons. Every
   trajectory: seed scene for one hop, then rain or silence, then alternation between the two
   until an exact copy. Which template a seed lands on: silence for servers, king, interview,
   general, moon, astronaut; rain for the domestic seeds. Names recur: Elias, Elara, Mara, Clara,
   Julian, King Aldric, Dr. Aris Thorne (the moon lane); the moon lane's submersible and the astronaut's ship are
   both the *Aethelgard*. Answer to the question the human started with: under this operator
   the model has two attractor templates and an unbounded number of exact fixed points on them.
   Ledger taken apart (room 26): (a) ledger + clause, hook removed: 100 hops, 88 distinct texts,
   6 copy episodes (17..19, 68..69, 82, 86, 89..90, 97..99), longest 3, all escaped; 73 distinct
   signatures, 58 settings; 30 append errors. The record un-freezes without the hook. (b) ledger +
   clause + hook, no step counter: the text field becomes the accumulator. Hop 2 begins "The
   anchor chain snapped with a loud crack." and every hop to 35 keeps the whole song so far,
   +4 lines a hop, to 124 lines; resets at 36, 46, 59, 60; grows to 120 lines by 89; hop 90 hits
   the 2048 wall; hop 91 repairs at 4 lines. History appended correctly on 90/100. Only 3 copied
   hops (because the text is never the same length twice). So the counter is what pins the text
   field to one verse. (c) ledger without clause (control) on Cerebras: 100 hops, zero copies,
   form 100/100, 1 append error, 39 settings, pit x13 / stone x9 / cave x7: the same cave basin
   as the local control. The basin is the model's.
   Sampling (room 27): change-four at T=0.7, seeds 1..5, 60 steps, stop-on-cycle. Froze at 16,
   47, 19; two ran 60 without a copy. The greedy Cerebras lane froze at 15. Sampling moves the
   freeze and sometimes past the horizon; it does not remove it.
   Cost: the whole batch (~1400 hops) was under $10 and about an hour of wall time, throttled at
   2 s for the ledger runs; no 429s.

15. The diverse ledger to 300 hops at 8192 tokens (room 28; cb_div_ledger_300 to hop 208, the
   connection was reset at 209, continued as cb_div_ledger_300_ext from hop 208's exact output,
   the way room 9 was; the site renders the concatenation and QA checks the join).
   No capacity transition: the history reached 171 items and was copied verbatim, in order, on
   every hop (0 alterations in 300); max tok_out 1776, max tok_in 1787, no wall. Text field 4
   lines on 298 of 300 hops (8 lines at 54 and 299). 172 distinct verses, 167 distinct
   signatures, 103 distinct settings; 130 hops appended nothing.
   Stalls get longer: 11 text-level copy episodes, lengths 1, 1, 1, 4, 6, 42, 1, 2, 1, 64, 5,
   every one escaped (the last at 297). The 42-hop stall (109..150, "Water gushed from the
   drain.") and the 64-hop stall (208..271, "I wrapped the burn in gauze.") both had zero
   appends, so the object fed back was byte-identical hop to hop except the step field.
   Mechanism, now exact rather than a candidate: during such a stall X_t differs from X_{t-1}
   only in the integer step, so the escape hop is a function of the step value alone; the step
   is the clock that makes the fixed point metastable. Escape inputs here (step of the last copied
   object): 22, 29, 31, 69, 94, 150, 155, 169, 193, 271, 296. Locally (item 13) the 21-hop stall escaped at input step
   99. No pattern claimed beyond "some integers tip the argmax". Corollary for the memoryless
   rooms: nothing in their state changes on its own, so a copy is absorbing; for the no-counter
   arm (item 14b) the accumulating text field played the clock instead.
   Cost: ~$3 for the 300 hops (history in and out every hop).

8. Instrument notes. (a) llama.cpp with 2 slots at 131k context fell to 0.8 tok/s when two
   clients ran at once and stayed there alone (20.4 GB per 3090, paging); -c 16384 -np 1 gave
   20 tok/s. (b) The harness appends to steps.jsonl, so a rerun into the same --out leaves a
   stale first record; alternating_json_page has two t=1 lines, the second is the real run.
   (c) Sonnet 5 hit 600 output tokens at ~290 words twice; its tokens-per-word is higher than
   4.6's (or something else counts against max_tokens). (d) Five Qwen json_next hops did not
   parse because Qwen escaped only one of a pair of quotes inside the text field.

## Corrections to README.md from the data audit (site/facts.md has all 16)

- Claude json_page "strict semantic period 2 from t=22": cartographer on odd hops 23..41, then
  42 (archivist) and 43 (translator) back to back, then even hops 44..60. One phase slip.
  Partner in 24..32 is the lighthouse keeper's logbook. Hop 2 continues hop 1; 59 openings, not 60.
- json_next "a drowned man identified on Tuesday": nobody drowns; the Carvalho boy was found in
  the tree line above the second cove by a hunter's dog (t=6). Protagonist is Maren t=1..2,
  Mara t=4..10, unnamed t=11..60; divorced at t=8, married eleven years at t=47.
- Raw run: numbered words start at the end of t=6, not t=7; counter maxima 11..155; "tau=19
  rotation-invariant" is really 20 under the loop.py convention.
- Parallel run's imperfect copy is one inserted character: "a erratic" -> "an erratic" (t=11).
- json_unexpected fixed point (t=24) is hop 23 copied plus an appended paragraph cut at "The
  strand of DNA was"; json_worse's wall is 800 tokens for that run, and hop 7 is a further
  "worse" of truncated hop 6, hop 8 the first exact copy.
- json_better "two words then finished": two substitution sites, seven words became nine;
  "finished" is not in the data.
- headers glider counted twice (Hop 1 -> 2 -> 3), frozen at t=3.

## Queue still open

    python loop.py --backend anthropic --model claude-sonnet-4-6 --backend-b llama --model-b qwen3.8-27b --init json_next --steps 60 --max-tokens 600
    python loop.py --backend anthropic --model claude-sonnet-5 --init json_next --steps 60 --max-tokens 600 --no-sampling
    (json_next with the 44-word json_better_para seed; json_better with the raw-mode window)

Prediction on record for the alternating AFTER loop: no recurrence, and Qwen's hub template
appears less often than in room 15 because "after" gives it a scene to continue instead of a
passage to replace.
