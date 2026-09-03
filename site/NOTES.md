# NOTES.md: the loop site

## Report (2026-09-02, final, after two sessions the same evening)

What I made. One instrument: a memoryless reader, at C:\ai\loop\site\index.html (3.6 MB, one
file, opens from file:// in Chrome, no network, no build step for the viewer). Seventeen rooms,
a map, the poem, a colophon, and an annex of eight. In every room you see the rule, the passage
the model was shown (faded, clamped, dropped words struck) and the passage it wrote (changed
words marked). You press next. At a fixed point the text stays perfectly still, the counter
ticks, and a rust line under it says "unchanged since hop 15". A track above shows one bar per
hop at the same scale in every room; the front index shows a miniature of each room's track, so
the index alone shows which rooms stop and where. Play auto-advances; sound (off by default,
confirmed audible by the human) plays one tone per hop, pitch from distance to the seed and
loudness from distance to the previous hop, so a fixed point becomes the same quiet tick. Two-
lane rooms put two runs on one counter: the two identical starts that diverged (6), Qwen
against Claude (11), Sonnet 4.6 against Sonnet 5 (14), one passage under two rules (17). Rooms
12, 13, 15 and 16 are hour-long reads. The map (#map) is the eleven-state census over the
page-scale Qwen runs, hand-laid, with exact copies as solid loops, opening-words-only repeats
as dashed loops, the escape edge in rust, and every state clickable into the reader.

New data, made this evening (site/runs_extra/, data/ and runs/ untouched):
- Room 13, Qwen under the AFTER rule: 60 hops, no copy. It passed through its apotheosis and
  came back down. The README's "the ending horizon is a property of Qwen, not the operator" is
  too strong: "new passage" freezes Qwen, "after" does not.
- Room 14, Sonnet 5 (run by the human): Sonnet 5 copies. Hop 7 = hop 6; hop 19 hit the token
  wall and hops 20 to 60 copy the fragment. Hop 3 repaired truncated hop 2 with a one-character
  fix ("an quiet man" to "a quiet man"). "Claude never copies" was a Sonnet 4.6 property.
- Room 15, Claude 4.6 and Qwen taking turns (run by the human): no recurrence in 60 hops.
  Qwen's hub template (the library silence) recurs 13 times in its 30 hops; its sinks never do,
  because Claude erases them every other turn. Qwen returned Claude's hop 1 word for word at
  hop 2 and appended to Claude's passage three times.
- Room 16, the "middle" rule: Qwen reads it as after; 60 hops, no copy; at hop 44 it writes
  about uploaded minds repeating their final thoughts in endless loops.
- Room 17, room 5's fixed point under "better" and under "after": better stops at hop 2 in a
  period-2 cycle between two versions of the passage (prediction on record was a fixed point;
  it was a two-cycle); after runs 40 hops and does not stop (prediction held).
So: a rule that identity can satisfy stops Qwen within a few hops, at a fixed point or a
two-cycle; after, before and the middle never stop; worse and unexpected stopped only when the
token wall broke their JSON. All of this is stated in the room notes as my reading.

Exactness. Every passage is rendered by build.py straight from data/<run>.json or
runs_extra/<run>/steps.jsonl; nothing is retyped. qa.py byte-compares all 885 rendered hops
(29 lanes, 25 rooms) against the data, checks the copy flags, the context renderings, the poem
against the brief, PLACEHOLDER notes, and the style rules: 0 failures. Every quotation inside an
authored note goes through a {{run|tag|hop|text}} macro that fails the build if the substring is
not in that hop, and renders with a visible hop number. Three QA agent passes (qa_report.md,
qa_report2.md, qa_report3.md) fact-checked every authored sentence against the data; all
necessary fixes were applied. facts.md (facts_gen.py) is the audit of the original bundle.

Incidents. Running two loops against llama.cpp at once (2 slots, 131k context) collapsed it to
0.8 tok/s and it stayed there alone; restarted with -Context 16384 -Slots 1 (20 tok/s). The
human's alternating run was rerun; its steps.jsonl carries one stale hop-1 record and the site
keeps the later record per hop (colophon says so). Sound was inaudible at first (110 Hz sines,
low gain); rebuilt at 220 to 620 Hz with harmonics.

What I chose not to make. A rendered audio file. A PDF book (the print stylesheet lays out the
active room's hops in order; checked once via headless Chrome). Mobile beyond one headless
screenshot. The remaining README queue items (Sonnet 5 under AFTER; the alternating loop under
AFTER; the AFTER rule with the paragraph seed).

What I would do with another day. Run the alternating loop under AFTER (does Qwen's copy habit
or Claude's continuity win when the rule cannot be satisfied by identity?). Sonnet 5 under
AFTER. Compose the sound from the trajectories rather than one tone per hop. Have a human read
the notes aloud once; they are dense.

How to resume. python build.py && python qa.py from C:\ai\loop\site. Sources in site/src
(copy.py is all authored text, including EXTRA_ROOMS for runs under site/runs_extra; a room is
built only once its summary.json exists). facts.md is the reference for claims about the
original bundle; qa_report*.md for the rest. The Chrome extension cannot open file://; headless
Chrome (--headless=new --screenshot) opens file:// fine and was used for the later checks.

### Addendum, second session (same evening)

- The map is built (#map): census over the 129 page-scale Qwen hops (rooms 5 and 6), 11 states,
  hand-laid SVG, nodes clickable into the reader. Solid loops are exact copies (×56, ×46, ×4);
  dashed loops mean only the opening words repeated (hop 1 of every run; Mara's one-character
  copy). The escape edge is in rust.
- Room 14, Sonnet 5 (json_page, provider default sampling, run by the human from a terminal):
  Sonnet 5 COPIES. Hop 7 = hop 6 (escaped at 8), hop 19 hit max_tokens and hops 20..60 are exact
  copies of the truncated JSON. Hop 3 repaired truncated hop 2 ("an quiet man" -> "a quiet man",
  sentence finished). So "Claude never copies" was a Sonnet 4.6 property; room 11's note now
  says Sonnet 4.6. Same token-wall horizon as Qwen's worse/unexpected rooms.
- Extra rooms are generic now: copy.EXTRA_ROOMS lists runs under site/runs_extra; a room is
  added only when its summary.json exists. Notes for pending runs are PLACEHOLDER and qa.py
  fails if a PLACEHOLDER is ever rendered.
- Room 15, alternating Claude 4.6 / Qwen (json_page, 60 hops, run by the human): no exact
  recurrence. Qwen's hop 2 returned Claude's hop 1 word for word (JSON re-spaced, so not a byte
  copy; the reader now says "same words as hop 1"); Qwen appended a paragraph to Claude's
  passage at hops 6, 16, 50; 13 of Qwen's 30 hops open with the library-silence hub template;
  Claude wrote a new opening every odd hop ("eleven years" in 10 of 30), reaching a
  cartographer's studio at 55. Qwen's hub keeps recurring, its sinks never do.
- Room 14 became two-lane: Sonnet 4.6 (room 11's run) beside Sonnet 5, so the tracks show one
  that never flattens next to one that does at hop 20.
- Front index now shows a mini track per room (4 px per hop), so the index itself shows which
  rooms stop and where.
- Context slot now strikes the words the next hop dropped (del marks; QA checks textContent).
- Sound: rebuilt after the human heard nothing: 220 to 620 Hz with harmonics, louder, longer;
  button reads "sound on" only when the AudioContext is running. Confirmed audible by the human.
- llama.cpp incident: with two clients (my queue + the human's alternating run) the server
  fell to 0.8 tok/s and stayed there even alone (20.4 GB per 3090, paging). Restarted with
  -Context 16384 -Slots 1: 20 tok/s. The human's run was rerun; its steps.jsonl carries one
  stale hop-1 record from the aborted start; load_extra keeps the later record per hop and the
  colophon says so.
- Rooms 16 (middle) and 17 (one passage, two rules) landed; see the report above.
- BEFORE continued from hop 60 (site/runs_extra/qwen_prev_ext, --stop-on-cycle, 140 requested):
  exact fixed point at overall hop 148, first repeated at 149, cycle confirmed x3 at 152. The
  fixed point opens on Qwen's "The rain lashed against the" template (slot B's sink in room 6)
  and is a first-contact scene at the Nexus Data Center ("You are here."). Room 9 now shows all
  152 hops as one lane (build_lane supports lane["extend"]; QA checks the concatenation).
  Details and the check against the other Fable's prediction are in
  C:\ai\loop\FINDINGS_20260902_evening.md item 7a.
- Room 18, json_worse at max_tokens 4096 (objection from the Lidar Fable: the wall is part of
  f). Same tau=7, p=1; hop 6 fills 4096 with a period-2 sentence x71, hop 7 with
  "self-Physically," x578, hop 8 copies. The fragment is the wall's, the non-termination is the
  model's. FINDINGS item 9.
- Room 19, json_unexpected at 4096: same tau=24, but hop 24 completes (771 tokens, finish=stop)
  and hop 25 copies it whole. The wall only decided fragment vs whole passage. FINDINGS item 10.
- Git: C:\ai\loop is a repo, pushed to https://github.com/Aargau/loop (private). Site deployed
  to Cloudflare Pages: https://endlessly-ending-stories.pages.dev (manual deploy from site/dist,
  see the message log; project endlessly-ending-stories).

(Below: the plan as written at the start, decisions, and the status log.)

## Concept: the memoryless reader

One instrument, applied to every run. The reader puts you where the model sat: you see the
instruction (the rule field, verbatim), the passage the model saw (previous hop, faded), and the
passage it wrote (current hop). One control matters: next. At a fixed point, next produces the
same text; the hop counter goes up and nothing moves. That is the finding, felt rather than told.

A stranger gets it in under two minutes on the first rooms (better: one hop, then stuck; worse:
five hops to the void, then the token wall; new paragraph: fifteen hops of sea, then the moon
forever). The primed context reads Claude's sixty passages the same way, one at a time, with only
the previous one visible, and it never sticks. Then the poem. Then the colophon.

Why this and not the others in the brief: the horizon gallery, the two-models-one-seed pairing,
the novella-with-the-constraint-visible, the worse room, the counter, and the fixed-point
anthology are all views of the same object. One reader with a room index gives all of them
without building six things. The funnel map is the one seed this does not cover; skipped on
purpose (depth over breadth), noted in the report.

## Rooms (order = the walk)

Part one, Qwen3.8-27B Q8, T=0, local:

 1. Better               json_better        20260902T172519_chat   5 hops, tau 1
 2. Better, paragraph    json_better_para   20260902T174854_chat   6 hops, tau 2
 3. A new sentence       json (headers3)    headers3               12 hops, period 2 from hop 4
 4. A new paragraph      json_para          20260902T155321_chat   19 hops, tau 15 (the moon)
 5. A new passage        json_page          20260902T155557_chat   9 hops, tau 5 (Mara, the click)
 6. A new passage, twice json_page x2       20260902T160344_chat   2 x 60 hops, diverge at hop 1; tau 4 / tau 14 with the escape at t=11
 7. Worse                json_worse         20260902T174258_chat   11 hops, tau 7 (content note)
 8. Unexpected           json_unexpected    20260902T172547_chat   28 hops, tau 24 (content note)
 9. Before               json_prev          20260902T165324_chat   60 hops, no recurrence
10. No template          json_page raw      20260902T162514_raw    40 hops, glider t=7..19, period 11 exact from t=20

Part two, Claude Sonnet 4.6, T=0, API:

11. A new passage        json_page          20260902T175920_anthropic_chat  60 hops, never copies, period-2 orbit
    (paired two-track with room 5: same seed, same rule, two models)
12. The next passage     json_next          20260902T181431_anthropic_chat  60 hops, one story, holds

Annex (the instrument being found): smoke (quine), headers (yours/still/rule/glider),
headers2 (still2/sandwich), and the 3-hop Claude smoke test. Same reader, listed after the rooms.
The 0-hop failed Claude smoke test is mentioned in the colophon only.

Then: the poem (as written, credited to a fresh Claude context, 2026-09-02, before the experiments).
Then: colophon.

## Design decisions

- Static first. build.py renders every hop of every run into the DOM (section per hop, with
  data-run, data-t, data-model attributes and a visible citation). JS only hides/shows and
  handles next/back/play/keyboard/hash routing/raw toggle. Without JS it is one long scroll of
  everything, in order, cited. Print CSS gives a printable book of the current room.
- Exactness by construction: texts come straight from data/<run>.json into the HTML via a
  builder; nothing is retyped. QA diffs DOM textContent against data/ for every hop.
- Diff marks: when a hop keeps most of the previous hop (5-gram survival >= 0.5), words not in
  the previous text are marked. When the passage is mostly new, nothing is marked. At an exact
  copy, nothing is marked. Word-level LCS, computed at build time. Presentation only; textContent
  unchanged. Stated in the colophon.
- Track: one bar per hop, height = NCD to the previous hop (always present; pure text metric;
  the embedding server was not always up). Exact copies sit near the floor (~0.03). Click a bar
  to jump. Two-track layout for the parallel run and for the Qwen/Claude pairing.
- Truncated JSON fixed points (worse, unexpected, prev t=20) render as monospace pre-wrap,
  exactly, cut where the token wall cut them. Raw-mode run renders monospace throughout.
- Typography: serif system stack for loop text (Charter / Iowan / Palatino Linotype / Georgia),
  monospace for the instrument (labels, rule, metrics, citations). Authored prose is set in the
  instrument face and small, so what is mine looks like apparatus and what is the loop's looks
  like text. The colophon says so.
- Color: warm paper ground, near-black ink, one muted accent for the next control. Dark variant
  via prefers-color-scheme. No decoration that is not data.
- Motion: next slides the current passage up into the context slot and the new one in below.
  Play auto-advances (2.5 s) so a frozen run is felt as time passing with nothing changing, and
  the raw-mode glider is seen as motion.
- Sound: optional, off by default, stretch goal. One soft tone per hop, pitch from NCD to the
  seed. Only if the main thing is right first.

## Process / agents

- Me: concept, authored texts, build.py, reader JS/CSS, iteration.
- Agent A (data audit): reads data/, writes site/facts.md with verified per-run facts and exact
  quotes with hop numbers, for the room notes.
- Agent B (QA): opens file:///C:/ai/loop/site/index.html in Chrome, walks every room,
  screenshots, checks keyboard, hash links, print view, reports.
- Script QA: qa.py diffs every hop in index.html against data/.
- Optional: Qwen json_next run started in the background (site/runs_extra/qwen_json_next,
  ~49 s/hop, --stop-on-cycle). If it finishes it becomes room 12a, the missing cell: Qwen with
  the same explicit NEXT operator Claude got. Main work does not depend on it.

## Status

- [x] plan written (this file)
- [x] Qwen json_next run: FINISHED, 60 hops, no recurrence (site/runs_extra/qwen_json_next). Room 13.
      This is new information: with the explicit AFTER rule Qwen does not stop either. The ending
      horizon belongs to the "new passage" rule (identity satisfies it), not to the model. Note in
      room 13 says so as my reading.
- [x] facts.md from data audit (agent; 16 corrections to README/index notes, all listed there)
- [x] build v1: build.py + src/{copy.py,template.html,style.css,app.js} -> index.html (2.1 MB)
- [x] authored texts, first pass (src/copy.py). Second pass after browser review.
- [x] qa.py: 589 hops in 23 lanes byte-checked against data/, poem checked against the brief,
      style lint on authored text. 0 failures.
- [x] browser iteration: stacked layout (previous faded above, current below, one 46rem column;
      two-lane rooms side by side), natural-scale track with tick labels, still text at copies,
      "unchanged since hop N" status, counter tick, theme toggle, sound, glider digits tinted,
      page nav on poem/colophon, document.title per room, favicon, source-reader comment.
- [x] file:// verified with a desktop screenshot of Chrome opened on
      file:///C:/ai/loop/site/index.html#better/2 (renders, reader works).
- [x] QA agent: qa_report.md; 16 necessary fixes applied to copy.py and build.py (fixed-point
      quote in the intro, room 8 content note direction, room 11 partner list and slip hops,
      room 12 "first run" and the name drop at hop 11, room 13 six raw hops split 5+1, colophon
      corrections, three-part structures removed).
- [x] report (top of this file)

Style-rule note: the QA agent's strict three-part list flagged every "a, b, c" in the notes;
all strong cases were rewritten. Lists of four or more, and two-item pairs, were kept.

Files: site/index.html (the site), site/build.py (rebuild), site/qa.py (check), site/src/* (sources),
site/facts.md + facts_gen.py (audit), site/runs_extra/ (the Qwen json_next run made today).
Rebuild: python build.py && python qa.py (from site/).

Decisions made during the build:
- Hops that did not parse as JSON but contain a fenced JSON object with the rule intact (Claude
  json_next hop 1) render the preamble in mono and the story in serif; QA reconstructs the raw
  from preamble + inner text + postamble.
- Diff marks apply to mono hops too (so the worse room's hop 7 shows what it added to hop 6).
- Track is at natural scale, 12 px per hop, so a 5-hop room and a 60-hop room look as different
  as they are.
- Theme follows the system; a toggle in the top bar (and on the front) overrides, remembered in
  localStorage; ?light / ?dark in the query string also work (for screenshots).
