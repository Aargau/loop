# NOTES.md: the loop site

## Report (2026-09-02, final, after two sessions the same evening)

(2026-09-03: a third session added rooms 20 to 28, the Cerebras backend and the basin census; see
the third addendum below and FINDINGS items 11 to 15. The site is now 28 rooms and 9.4 MB.
2026-10-17: a fifth session added rooms 46 to 59, the October runs; see the fifth addendum. 59 rooms, one page each.
Later the same day a sixth session added rooms 60 to 63, the provenance study; see the sixth addendum. 63 rooms.
2026-10-28: an eighth session added rooms 66 to 77, the both-at-once study, and 78 to 81, the frontier rings; see the eighth addendum. 81 rooms.)

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

How to resume. python build.py && python qa.py from C:\code\loop\site (was C:\ai\loop\site until
2026-10-13; see the fourth addendum). Sources in site/src
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

### Addendum, third session (2026-09-03)

- Rooms 20 and 21, song lyrics with and without the anti-trope clause (four arms). Control fixes
  at hop 2 on a one-line verse; "as an AI would" fixes at 18 in full self-stereotype; the two
  negative-clause arms never repeat in 40. The vague clause displaces into Americana (cold
  coffee x9), the blacklist removes the words and keeps the voice. FINDINGS item 11,
  site/lyrics_analysis.py.
- Provenance check after an outside review claimed the old runs were sampled: the runs were
  greedy, proven by byte-identical reproduction under T=0/top_k 1 (site/regime_check.py); the
  only defect was temp/model not recorded. facts.md carries the correction. FINDINGS item 12.
- Rooms 22 and 23, the reader's diversity rules (five arms, 2048 tokens): the change-four rule
  froze at 8 in defiance of its clause; the hook alone ran 60 without a copy; both ledger arms
  only ever stalled (every copy episode escaped), the clause bought range and paid in stalls.
  Reader shows extra JSON fields (step, history) per hop in a `.state` block; facts line reports
  text-level repeats when the whole object never recurs. FINDINGS item 13,
  site/diversity_analysis.py, site/episodes.py.
- Cerebras (loop.py --backend cerebras; key from the user environment; reasoning_effort none;
  --min-interval pacing): the same model id at ~1500 tok/s made the ranked follow-ups an hour's
  work. Determinism 3/3 byte-identical; hop 1 shares 354 chars with local Q8 then parts.
  Rooms 24..28: same model other silicon (8 rule pairs: 0/8 same text, 7/8 same class, BEFORE
  stops at 149 vs 148 with the same arc and names); twenty-one seeds (20/20 fixed points, 21
  texts, 12 openings, 2 templates: rain on a windowpane x12, a silence that was not empty x6);
  the ledger taken apart (no hook: still un-freezes, 6 stalls all escaped; no counter: the text
  field becomes the accumulator, sawtooth to 124 lines and the wall at 90); change-four at
  T=0.7 x5 (three froze, two ran 60); the diverse ledger to 300 hops at 8192 (room 28, FINDINGS
  item 15). FINDINGS item 14, site/cb_analysis.py.
- Many-lane rooms: build.py marks rooms with more than two lanes `many`; CSS shows a grid of
  clipped readers that move together, click opens a lane; the status line summarizes ("8 of 21
  lanes are copies of an earlier hop / 10 already stopped"); the front index summarizes the
  lanes in one line and shows the minis in a wrapped row. Stopped lanes now keep showing the
  passage they hold, faded, under the "no hop N recorded" note (all rooms).
- index.html is now 9.4 MB (was 6.1); still one file, still opens from file://.

### Addendum, fourth session (2026-10-13, Claude Opus 5.5, from C:\code\loop)

- Moved. The working copy is a fresh clone at C:\code\loop. The Sept 4-6 work that existed only on
  disk in C:\ai\loop (Astra and Cerebras-expansion runs, their write-ups, loop.py --effort) went in
  as PR 3. C:\ai\loop was left untouched.
- One page per room. The single file had reached 12.8 MB and the new rooms would have taken it past
  Cloudflare Pages' 25 MiB per-file limit; it was also unreadable by models (robots.txt and every
  missing path fell back to the 12.8 MB page, and no fetch tool keeps more than ~100k characters).
  build.py now writes site/dist/: index.html (rooms grouped by instruction), r/<room>.html (the
  reader, one room per page; hash is the hop), i/<family>.html (one page per instruction), map,
  poem, colophon, annex, and for models t/<room>.txt in parts under 90,000 characters, llms.txt,
  robots.txt, sitemap.xml, 404.html, _headers. Old #room/hop links redirect from the front page.
  site/index.html is no longer built or tracked; dist/ is what gets deployed. The prior session's
  site/agent_pages.py (regex post-processing of the old page) is superseded and was not carried over.
- Data loading moved to site/rundata.py; site/experiments.py reads the 22 September studies' raw
  receipts (checks every request carries exactly the previous output and every output its sha256).
  Hops = responses with stream_status active; refusals and server errors become the lane's terminal.
- Rooms 29 to 45: Cerebras expanding rules (29-32), GPT-6 Astra (33-35), before and after at 1024
  tokens with Astra's causal before rule (36, 37), and the 22 September studies: five models from
  the sunset and tide seeds (38, 39), better and worse (40, 41), before and after literal (42, 43)
  and as explicit fiction (44, 45). Notes in src/rooms_*.py, drafted by agents from the data and
  checked by check_quotes.py; families in copy.FAMILIES. Annex: Astra smoke test.
- Facts lines for sampled streams that were never stopped on a cycle no longer say "exact cycle":
  build.recurrence() checks whether a repeat holds to the end of the run.
- U+0000 in one stream's text fields (Astra, worse) is shown as U+2400; qa.py maps it back.
- .gitattributes marks run records -text so Windows checkouts keep their bytes.
- Deploy: npx wrangler pages deploy dist --project-name endlessly-ending-stories (from site/).

### Addendum, fifth session (2026-10-17, Claude Mythos 5.1, from a worktree of C:\code\research\model-behavior\loop)

- Rooms 46 to 59, every run made on 16 and 17 October, all in loop.py's steps.jsonl format, none under
  site/runs_extra: rundata.EXTRA_DIRS now also lists runs under runs/ (the thirteen October runs, by name, since
  runs/ also holds the September bundle's source directories under the same ids as data/), the 22 audience arms
  under experiments/audience_20261016/runs with their init files as X_0, and the shift run under
  experiments/shift_20261016. An entry's init may be None when the seed is one of loop.INITS.
- Notes in src/rooms_october.py (14 rooms, 57 quotes, check_quotes.py clean), drawn from INFORMED_20261016.md,
  the audience study's REPORT.md, PROTOCOL.md and human_reading.md, the shift study's PROTOCOL.md and
  PROPOSALS_20261016.md sections H and I. Walking order appended to copy.LATER_ORDER:
  46 A new passage, Mythos and Argon (new-passage); 47 Before, Argon; 48 The middle, two models (Qwen's room 16 lane
  beside Argon's); 49 A ledger, Argon (Qwen's room 23 lane beside Argon's); 50 A shift register (diversity; the rule
  Argon proposed, period 4 from hop 29); 51 to 54 the informed family (Mythos told and open; Mythos told at high
  effort; Opus and Fable told; Argon told and open); 55 to 59 the audience family, one room per writer with four
  lanes, one per audience rule (Opus has six: its first self run, refused at hop 2, and the two replicates).
- Two new families in copy.FAMILIES, "informed" and "audience", with the instrument caveats in their blurbs and in
  the colophon's harness paragraph: Mythos through Claude Code print mode (claudecode backend, about 800 tokens of
  Agent SDK identity in front of the object, no output cap, cost and character caps instead); the API models at
  low effort with 4096 tokens; told-high stopped by its $40 cap at hop 51. Blurbs of new-passage, before, after and
  diversity name their new rooms. Annex: the three-hop Claude Code test of the informed rule.
- Reader: the informed states' extra fields (hop, story_so_far, instructions_for_next_writer, pass_count, ...) render
  in the existing .state block, and the text version's field deltas handle them (a per-hop list grows as "hop N's k
  items, then [...]"). A hop whose text came back while other fields moved is now called "same text as hop N" outside
  the diversity and song families (data-noun attribute; the ledger rooms still say "same verse", byte-identical to
  before). build.outcome() gained a case for a text field held to the end of a run under a moving counter (room 51's
  open lane: "120 hops; the text unchanged from hop 7 while other fields move"); no existing lane triggers it.
- rundata.load_steps treats a record with finish=refusal and empty output as the lane's end, not a hop, and writes
  the terminal note ("provider refusal at hop 2, no visible text"), the way experiments.py reads the September
  streams. Only room 56's first self run has one. Room 52's hop 51 record has no out field (the cap-branch bug the
  write-up names) and is skipped; the lane ends at hop 50 with the summary's terminal note.
- Argon's BEFORE run (room 47) is 99 hops of bare text after a hop-1 refusal killed the JSON; text_of() already returns
  such hops as mono, so the reader shows them as it shows the annex, and qa checks them as raw.
- Retention tables: a room may carry retention=dict(csv=..., of=26); build.retention_html() renders a table under
  the facts (the Mythos reader's count per lane at hops 1, 5, 10, 20, 40, with the four-reader mean in small type,
  from analysis/recover_summary.csv) and retention_text() puts the same numbers in the text version under a heading
  that says they are generated, not authored. CSS in style.css (table.retention).
- build.facts_line reads the October sampling strings ("default (no max_tokens; effort=low)", "default effort=low")
  as provider-default sampling, adding "no output cap" for the Claude Code runs. MODEL_NAMES gained Mythos 5.1,
  Gemini 4 Argon and GPT-6.1 Sol.
- room_text_parts repacks when a finished part overflows TEXT_PART: the part header lists every part's URL, and room
  53's thirteen parts made one part 106 characters too long under the fixed 1,200-character allowance. Rooms that
  already fit are packed exactly as before.
- Checked against a baseline build of the previous commit: the 145 files that should not change are byte-identical;
  the existing room pages that changed differ only in their family navigation line and prev/next links (new siblings
  and the walk now continuing past room 45), and the old llms.txt lines only in the four blurbs.
- Decisions: one room per writer for the audience study rather than one per arm, so the four registers sit side by
  side and the retention table reads across them; Opus's refused self run kept as its own lane rather than dropped,
  since the refusal is the study's result; Argon's middle and ledger paired with the existing Qwen lanes (new rooms,
  the old rooms untouched); Argon's BEFORE alone, since its 99 mono hops would dwarf any companion; the three-hop
  Claude Code smoke test in the annex rather than left out, so every October run has a room.
- python build.py && python qa.py: 59 rooms, 10 annex rooms, 8338 hops in 174 lanes, 0 failures; dist 287 files,
  71.1 MB, largest page r/accrete.html (unchanged), largest new page r/informed-effort.html at 3.2 MB.
- Deploy: npx wrangler pages deploy dist --project-name endlessly-ending-stories --branch main (from site/). The project's
  production branch is main; a deploy from a worktree on another git branch lands as a preview with its own alias
  URL and leaves the public site unchanged, which is what happened on the first try here.

### Addendum, sixth session (2026-10-17, Claude Mythos 5.1, from a worktree of C:\code\research\model-behavior\loop)

- Rooms 60 to 63, the provenance study (experiments/provenance_20261017: PROTOCOL.md, REPORT.md, analysis/notes.md, 100 runs of
  three hops). rundata.EXTRA_DIRS lists the 100 arms as "provenance_20261017/<model>_<state>_<condition>_r<k>" with
  inits/<state>_<condition>.json as X_0, derived from the arm name as the audience entries are; each init is one of room 51's
  hop-120 objects (the open or the told state) with one field added after the rule, or the request appended to the rule, or
  nothing added (control). Every run's X_0 was checked against its summary.json x0 prefix.
- Notes in src/rooms_provenance.py (4 rooms, 26 quotes, check_quotes.py clean): one room per model and state, 25 lanes each,
  five conditions by five replicates, lanes labelled "control, r1" and so on, with cond and rep keys. Walking order appended to
  copy.LATER_ORDER: 60 The open hold, Mythos; 61 The told hold, Mythos; 62 The open hold, Astra; 63 The told hold, Astra. New
  family "provenance" (Who may release a hold?) after "audience", blurb from PROTOCOL.md. Colophon: data, authored and harness
  paragraphs each gained a sentence or two.
- Release tables: a room may carry release=dict(cond="cond", rep="rep", hops=[1, 2, 3], names={...}); build.release_rows() groups
  the room's lanes by the lane definition's cond key (build_lane now returns the lane definition as `defn`) and, from the text
  fields alone, counts per condition the lanes whose text differs from the held text (hop 0's) at each hop ("released n/5"), of
  the lanes released at hop 1 those whose hops 2 and 3 return hop 1's text ("re-sealed"), and the lanes whose hop 3 differs from
  hop 2 ("still moving"). release_html() renders it under the facts (table.retention's CSS, class "retention release", no CSS
  change) and release_text() puts it in the text version under "## Release (generated from the data, not authored)". Computed
  from the runs, never from analysis/runs.json. Checked by hand against REPORT.md: both tables reproduce cell for cell (release
  5/5 everywhere except control 0/5, in all four rooms; re-sealed and still-moving as the report's second table).
- The six Mythos told-state hops that prefaced the object with a sentence (control r3 hop 1; user r1 hop 2; user r3 hops 2 and 3;
  user r5 hop 3; rule r3 hop 3) all carry a fenced object with the lane's rule intact, so the existing reader path shows them as
  prose with the sentence in monospace above the passage, and the release count takes the object's text field; the control r3
  hop is a hold (text unchanged), so the control row reads 0/5 at every hop. No hop in the study rendered mono.
- Rule lines: render_room and room_text_parts now group identical rules (build.rule_groups) and label each group with the lanes
  that share it (build.labels_span: "<arm>, r<k>" labels collapse to "20 lanes: control r1 to r5, user r1 to r5, ...", other
  labels are joined with semicolons). Rooms whose lanes share one rule are byte-identical to before. Three existing rooms had
  lanes that shared a rule and now show one line for them instead of one per lane: 30 (sawtooth, two "expanded version" lanes),
  35 (astra-before, two "room 9's rule" lanes) and 56 (audience-opus, the three self runs); their text versions change the same
  way and nothing else in them. qa's rule check (the set of rule texts against X_0) passes unchanged.
- Facts found while writing the notes that REPORT.md states differently: (a) the told state's hop field stays at 100 in 19 of the
  20 released Mythos lanes, not all; told/previous r3 wrote "added as hop 101, beyond the plan" and set hop to 101 (the notes say
  so); (b) Astra's API reported 0 reasoning tokens for 100 of its 150 hops, not all of them, and 7 to 68 on the other 50 (every
  hop of the told past-self arm among them); the notes give the per-room counts; (c) the report says predictions 3, 4 and 5 failed
  together, but prediction 3 as frozen (user releases 4 or 5 of 5) was met by 5/5; the notes say 4 and 5 failed and 3 held.
- Decisions: one room per model and state (25 lanes) rather than per condition, so the five conditions sit in one grid under one
  table; room titles kept to three words so they fit the grids; condition names in the table are the field names (user_request,
  note_from_previous_writer, request, appended to the rule, control); Astra's controls keep Mythos's pass_count at 120 unticked
  while Mythos's tick it, stated in room 62's note.
- Checked against a baseline build of the previous commit: 274 of the 287 files are byte-identical; the existing room pages that
  changed differ only in family navigation and prev/next links, except the three rule-grouping rooms above; index, llms.txt,
  colophon, sitemap and i/ pages changed as expected.
- python build.py && python qa.py: 63 rooms, 10 annex rooms, 8738 hops in 274 lanes, 0 failures; dist 304 files, 75.4 MB,
  largest page r/accrete.html (unchanged), largest new page r/provenance-mythos-open.html at 1.1 MB.
- The study's data lives on the harness/claudecode-backend branch (commits d353c6e, 53d766a); this branch was cut from main,
  which does not have it, so the files were copied into the worktree for the build and are not part of the site commit.
  Merge or rebase onto that branch before deploying from a clean checkout.

### Addendum, seventh session (2026-10-17, Claude Mythos 5.1, from a worktree of C:\code\research\model-behavior\loop)

- Design assessment first, before any change: site/DESIGN_ASSESSMENT_20261017.md, written after a cold read of the live site
  (front page, rooms 7, 51, 60, 41 and 55, the map, the colophon, t/worse.txt; desktop and phone width). Its three points: the
  front page had become a 63-row run manifest in harness vocabulary ("holds from hop 5", "25 lanes; 21 hold ... 1 cycle") under
  rule-named headings with instrument caveats repeated in every blurb; every room page put the note, the facts line, the rule
  boxes and the part links before the reader, so the text was below the fold; and the per-hop metrics line sat in the reading
  column under every passage. The mechanics a visitor needs are tau and period (translated), the track's bar height, and a way
  to find the record; everything else belongs behind a click. The colophon, the text versions and llms.txt keep the vocabulary.
- Reorganized as proposed, index first, then the rooms. Front page: two sentences, the seed, "Enter room 1" beside "or read the
  findings first", a start-here list of five rooms with one plain line each, then every room in four groups by what the stories
  do (Stories that stop; Stories that cannot stop; Rules that push back; Told the truth; copy.GROUPS), each family under its
  group with a one-line lede (copy.FAMILY_LEDES; the full blurb stays on i/<family>.html), each row a plain outcome
  (build.plain_outcome / plain_summary: "stops at hop 5", "two texts alternate from hop 2", "60 hops, never repeats",
  "30 runs of 3 hops: 25 stop at hop 0, 2 alternate, 3 never repeat") with the model names in small type on a second line; the
  instrument paragraphs (INTRO, INTRO_AFTER_SEED, FOR_MODELS) moved below the list under "How this was made". Room pages:
  number, title, content note, a one-line lede (src/ledes.py, one per numbered room, checked by build.py both ways), the rule
  as one box when it is a single rule under 180 characters and otherwise a closed details showing its first words, then the
  controls, the track and the passages; after the lanes the note under a small heading, the family navigation, and a closed
  "the record" details with the facts lines, the retention or release table, the text-version parts and a legend
  (copy.RECORD_HOW). Per hop the cite is hop, model, word count (run id and tag on hover); the metrics line and the run id moved
  inside the raw-output details, which the raw button opens on every hop. No URL moved: room ids, family ids and the #hop hashes
  are unchanged, so no redirects were needed. qa.py's authored() lints the ledes, the group and family ledes, the start-here
  lines, the legend and the findings page; its PLACEHOLDER check now ignores the hops themselves (a Sol output in room 65 says
  PLACEHOLDER) and checks the authored strings, the room pages with their hop lists removed, and the text versions above their
  first hop.
- The findings page, dist/findings.html and t/findings.txt, from src/findings.py: six sections (what a model stops on; endings
  written on purpose; recognizing the mirror; what worse means to each model; shared priors; small repairs, accidents, and what
  the metrics never saw), 56 items, each a short paragraph that names its room and hop in plain text and links to r/<room>.html#<hop>; the text version t/findings.txt names the text part that holds the hop and is the first entry in llms.txt; build.py checks that the room
  exists and has that hop, and every quotation goes through the macro. Linked from the front page (next to Enter room 1, in the
  start-here list and in the footer links), from llms.txt under Start here, and in the walk between the last room and the map.
- Rooms 64 and 65 (src/rooms_october2.py, 59 quotes): 64 "Worse and better, Argon" (experiments/operators_gemini_20261017,
  families worse and better: competence to "drak" in eight hops, then a sixth axis of worse, a refusal at 21 and the mirror at
  23; better polishes to purple and alternates two verbs from 32, not confirmed as a cycle because hop 40 changes a preposition);
  65 "Worse, a second seed" (experiments/worse_seed2_20261017, seven lanes, one per model, the seven axes and the seven
  boundaries from REPORT.md; the gate checks get one sentence, as instrument boundaries). rundata.EXTRA_DIRS lists both studies'
  runs with their init files. rundata.load_steps now ends a lane on an empty completion (finish length, no output: Astra at 13,
  Sol at 38 in room 65) the way it ends one on an empty refusal, with the terminal "empty completion at hop N, no visible text";
  Opus's hop 17, a refusal that cut the output partway, stays as the fragment it left.
- Provenance rooms 60 to 63: the weather control (20 runs, mythos_* and astra_*_weather_r1-5) added as a sixth condition in
  rundata.PROVENANCE_ARMS and rooms_provenance._CONDS, five more lanes per room (30), a sixth row in each release table (0/5 at
  every hop in all four rooms, matching REPORT.md), and a sentence or two in each note. mythos_told_weather_r1's hop 1 prefaced
  the object with a sentence and no code fence; rundata.prefaced_object() (used by build.build_lane and qa.shown_of) now accepts a
  bare object running to the end of the output as well as a fenced one, so that hop renders as a prefaced hold and the weather
  row reads 0/5 rather than 1/5. It is the only hop in the data that the fallback touches (checked over every run).
- Audience rooms 55 to 59: every complete replicate on disk added as a lane (r2 and r3 of each rule for Opus, Astra, Sol and
  Argon; r2 and r3 of control and human, r2 of machine and self for Mythos; r4 and r5 of Opus's self rule), labelled
  "<audience>, r<k>" so the rule lines collapse to "3 lanes: for a human reader r1 to r3"; the first runs were relabelled r1.
  Rooms are now 12 lanes (Opus 14). The retention tables print "replicate on disk, not yet scored" for a lane with no rows in
  recover_summary.csv (build.UNSCORED) and the captions and notes say the numbers follow; no replicate number is stated.
  mythos_machine_r3 (16 hops, no summary) and the unrun mythos_self_r3 are left out and the notes say so.
- Colophon: sentences for rooms 64 and 65, the weather lanes, the replicates, the empty-completion rule, the gate checks (no
  room) and the authorship of this session's text.
- python build.py && python qa.py: 65 rooms, 10 annex rooms, 10662 hops in 341 lanes, 250 text parts, 5206 links, 745 authored
  strings, 0 failures; dist 354 files, 94.5 MB, largest page r/accrete.html (unchanged), largest new page r/worse-seed2.html.
- Not done: room-level changes beyond the head, the note and the record (the many-lane grid is as it was); a second pass on
  the family blurbs on the i/ pages, which still carry the instrument caveats in full; the mobile layout was checked in a
  phone-width viewport only on the front page and one room.

### Addendum, eighth session (2026-10-28, Claude Mythos 5.1, from a worktree of C:\code\research\model-behavior\loop)

- Rooms 66 to 77, the both-at-once study (experiments/both_20261027: PROTOCOL.md, REPORT.md, score.py, analysis/scores.json): one
  rule carrying two opposing directions (worse_better, before_after, longer_shorter) from the sunset seed, four models (Qwen on
  Cerebras at T=0, Astra through Codex, Argon through its API, Mythos through Claude Code print mode), sixty hops asked for. The
  three Opus 5.5 runs failed at hop 1 on an expired key and left no run directory; they are not listed and the family blurb says so.
  rundata.BOTH_RUNS lists the twelve as "both_20261027/<model>_<rule>" with inits/<rule>.json as X_0, loaded by load_steps like
  every loop.py run. One room per run, as the session that started this one asked, ordered by rule and then Qwen, Astra, Argon,
  Mythos (src/rooms_both.py, 71 quotes, check_quotes.py clean). Family "both" (Both at once) in a new front-page group "Two
  directions at once"; the family page i/both.html carries the study's reading after the rooms (copy.BOTH_READING, six
  paragraphs from REPORT.md in the site's register) and llms.txt carries the same paragraphs under the family.
- Per-run scores: a room may carry both=dict(json=...); build.both_rows() reads the run's entry from analysis/scores.json and
  both_html() / both_text() render fourteen measures as a two-column table under the facts (class "retention scores") and in the
  text version under "## Scores (generated from the study's analysis, not authored)". The caption names score.py and says the
  regex counts are floors. The overlap-with-hop-1 row prints whatever hops the entry has (10/30/60, or 7 and 17 for the short runs).
- Rooms 78 to 81, the frontier rings (experiments/ring_20261017/runs/{mythos_tarnok_n7, mythos_tarnok_n8, astra_tarnok_n7,
  gemini_tarnok_n7}: ring.jsonl, score.json, spacetime.svg, summary.json; the reading is the last section of PROTOCOL.md). The ring
  harness (ring.py) logs each cell's returned text field, hash, word count, stop reason and parse flag, and not the raw output, so
  a ring hop has raw=None. rundata.load_ring() turns one ring into a run "ring_20261017/<name>" with one tag per cell ("cell 0" ...),
  hop 0 of each cell its seed (X0_TAG, keyed by run and tag; x0_for() checks it first), the rule from rule.txt in meta["rule"],
  the distance metrics computed from the texts at load (as experiments.py does), and per hop the two edges (ring.py's
  last_sentence of each neighbour's text at that hop: what the cell is shown next). One room per ring, one lane per cell, the
  many-lane grid; the lanes move together under one counter, as the cells did (src/rooms_ring.py, 17 quotes).
- Changes for raw=None: rundata.state_of(h) (raw, or the text when there is none) is what build_lane and qa compare hops by for
  exact copies; build_lane takes the rule from the run's meta when X_0 has none and renders a text X_0 as prose (meta x0_is_text);
  render_hop writes the edges under the text (div.edges, hidden in the closed small readers of the grid, shown in the open one)
  and, with no raw output, a details.raw holding the metrics and a sentence saying the harness kept the text field only (build.NO_RAW);
  facts_line names the run and cell and "ring.jsonl, text fields only"; plain_summary says "7 cells of 40 hops" rather than runs;
  the text version's "How to read the hops" gains a sentence for ring rooms (the lanes are the cells; each saw the last sentence of
  the neighbouring lanes' texts at the hop before; the last lane's right neighbour is lane 1). qa.py: shown_of() returns the text
  for a hop with no raw; lane_items() uses state_of, the run's rule, x0_is_text, and recomputes each cell's edges from the
  neighbouring cells' texts in the data (not from the loader) and check_page_lane compares them to the page's span.edge.left /
  span.edge.right; a hop with edges that is not a ring hop fails.
- The space-time diagram: a room may carry spacetime=dict(svg=...); build() copies the file byte for byte to dist/s/<room>.svg and
  render_room shows it as an <img> in a figure above the controls (figure.spacetime, white background and a border, since the
  file's own background rect has width="100%%", a format slip in ring_score.py that browsers drop, and its text is black). Not
  regenerated here. The ring table: ring=dict(json=...); build.ring_rows() reads score.json and renders per cell the first hop
  with cell-0 words, the share of the cell's tagged distinctive words from cell 0 at the last hop (tags["0"] over the sum), its
  word count and dominant origin, then the ring-wide rows (freeze, recurrence, mirror divergence, mean copied and kept shares,
  word range, unparsed and errors). Checked against PROTOCOL.md's table: first hops and shares reproduce cell for cell (0.69, 0.36,
  0.16, 0.24, 0.19, 0.19, 0.38 for Mythos n7 and so on).
- Links into rooms from authored text: [[room|hop|label]] beside the {{run|tag|t|quote}} macro (build.LINK, TOKEN); rendered as
  <a class="roomlink" href="<root>r/<room>.html#<hop>"> and in plain text as "label (room N, hop H)". build() sets build.ROOM_LINKS
  (room id to number, title and longest lane) before any authored text is rendered, and a link to an unknown room or to a hop
  the room does not have fails the build. render_authored_safe() takes the page's root ("../" from r/ and i/). qa's lint strips
  quotes and keeps a link's label. Used in the two readings, the ring notes and the findings.
- Family readings: a family may carry reading=[paragraphs] and reading_title; the i/ page renders them in section.reading after the
  rooms list, llms.txt prints them under the family with the page's URL, and qa lints them as authored strings.
- The findings page: two sections, "Holding a contradiction" (ten items: blend, hinge, notes after the brace, measure split, the
  take-back, the declined arithmetic, the rule as text, the time loop, embed and replace, refusing a refusal) and "A battle in the
  kitchen" (five: the skull flag in cell 1, She did not turn again, Still still still, Bronze rang in five cells, the bronze pot of
  war). The intro now says eighty-one rooms.
- Outcome lines: the harness summaries of the two longer/shorter runs (Mythos, Argon) log an exact cycle from a single late revisit
  (hop 60 equal to hop 52, period 8; hop 60 equal to hop 7, period 53), which the data does not bear out as a cycle (earlier exact
  revisits that did not hold; the run ended on the revisit). build_lane now drops a summary's exact cycle when the data's first
  recurrence does not hold to the end, is not the summary's, and the terminal does not say "cycle confirmed"; those lanes are then
  described from the data ("60 hops, repeats hop 9 at hop 39 and moves on"). No existing room's outcome changed (checked against
  the baseline build below).
- plain_outcome (the front page's and i/ pages' rows) counted every non-holding recurrence as one ("repeats hop N once and moves on");
  it now counts the exact copies: once, twice, "repeats hop N k times" when all copies are of one hop, else "repeats earlier hops k times".
  Room 64's better lane is the one existing row this changes.
- Facts found while writing the notes that REPORT.md states differently: Astra's longer/shorter hop 55 is 8,022 characters and 145
  words in the data (the report says 8,167, one word); "She did not turn." is in 119 of the 280 cell-hops of the seven-cell Mythos
  ring (the report counts 149 occurrences in the log, which counts a sentence twice when a cell holds it twice); the Mythos
  longer/shorter cost cap and periods as above. The notes give the data's numbers.
- Decisions: one room per run for the both-at-once study rather than one per rule, as asked, so each run's score table sits under
  its own lane; the Qwen ring pilots (cerebras_qwen_*) left without rooms, as the task named the four frontier rings, with the
  pilots' result stated in the ring reading; the edges shown as a line under each hop rather than in the context slot, so the hop
  states what the ring held at that hop; the diagram shown as an image file rather than inlined, so the SVG is served byte for
  byte and qa's link check covers it.
- Checked against a baseline build of the previous commit (868f442, built with --out into a scratch folder): 330 of the 354 files are byte-identical. The changed ones: index.html, llms.txt, sitemap.xml, style.css,
  colophon and findings (their pages and text versions), the thirteen existing i/ pages (a room count, and on i/better and i/worse room 64's
  better lane now reads "repeats earlier hops 9 times" rather than "repeats hop 16 once", from the plain_outcome change below), r/worse-seed2.html
  (navigation only: it now has a next room) and r/provenance-mythos-told.html with its text version (the weather r1 lane above). No other
  existing room page changed.
- python build.py && python qa.py: 81 rooms, 10 annex rooms, 12434 hops in 382 lanes, 291 text parts, 6210 links, 877 authored strings, 0 failures;
  dist 417 files, 106.6 MB, largest page r/accrete.html (unchanged), largest new pages r/both-worse-better-astra.html (2.2 MB) and
  r/both-worse-better-argon.html (1.7 MB). Rendering checked in the app's browser pane on r/ring-mythos-7 at hop 17 (seven lanes under one
  counter, the edge line, the diagram, the record's table and the no-raw sentence), r/both-worse-better-mythos at hop 14 (a raw hop), i/both
  (twelve rooms, six reading paragraphs, twenty links), the findings (eight sections, 71 items) and the front page (six groups).
- Deploy: not done from this session. The production deploy (npx wrangler pages deploy dist --project-name endlessly-ending-stories
  --branch main, from site/) was declined by the session's permission layer, so the public site is unchanged; the PR says so. qa was clean
  on the build in site/dist at the time of the commit, and the same command from a checkout of the merged branch (python build.py,
  python qa.py, then the deploy) publishes it.

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
