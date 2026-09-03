# Findings, evening of 2026-09-02 (site build session)

Nine runs made while the site (site/index.html) was built. Logs: site/runs_extra/<run>/steps.jsonl
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
