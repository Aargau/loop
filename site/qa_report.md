# QA report: site/index.html against facts.md, data/ and the brief

Read-only pass, 2026-09-02. Checked: src/copy.py (every authored sentence), index.html as built (build_report.json says 13 rooms + 8 annex rooms, qwen_next=true), src/app.js, src/style.css, src/build.py, facts.md, data/*.json, site/runs_extra/qwen_json_next/steps.jsonl, FABLE_BRIEF.md.

Things that are right and need no change (verified independently with Python, not only via facts.md):

- All 566 model hops in index.html (23 lanes) match data/ and runs_extra byte for byte, both the shown text and the raw output behind the raw toggle. Seeds (hop 0) match loop.INITS.
- Every hop `<li>` carries a visible citation: `hop N · model · run <id>, <tag>` plus either `identical to hop M` or a word count. Seeds carry `seed hop 0 · run <id>, <tag>` (no model, which is correct).
- The poem in index.html (title, four stanzas, signature) is byte-identical to the poem in FABLE_BRIEF.md.
- All 14 `{{run|tag|t|...}}` quotes in the notes exist in the cited hop (build.py refuses otherwise).
- Hop numbers, transients and periods in the notes, the TOC ("holds from hop N", "period p from hop N") and the room fact lines agree with facts.md section 1 for all 21 lanes.
- Room 6: 236 shared characters, split at `it crept` / `it whispered`, slot A frozen from hop 4, slot B: Mara on the platform at hop 10, `a erratic` to `an erratic` at hop 11, Elias phoning his father at hop 14, 56 + 46 exact copies + 1 imperfect = 103. All correct.
- Room 7: annoying (1), basement (2), foundation (3), before the universe and "never be allowed to stop" (5), 800-token wall at 6, hop 7 expands the truncated JSON, hop 8 copies. Correct.
- Room 10: think block at hop 2, `The(1) kitchen(2)` at the end of hop 6, counter maximum 155 at hop 19, one repeated sentence from hop 20, exact period 11. Correct.
- Room 9: Chicago first at hop 12, server room at hop 19, Aethelgard at hop 60, no exact or normalized repeat. Correct.
- Room 13: 60 distinct outputs; the three quotes are at hops 17, 19, 24; council at 28, bakery at 27, stone bridge at 30, tunnel at 57, reservoir at 59. Rule field identical to the Claude json_next rule. max_tokens 600.
- Colophon mechanics that match app.js/build.py/style.css: play interval 2500 ms; keys right/space/left/p/r/s/escape; sound off by default, pitch from ncd_x0, loudness from ncd_prev; track bar height = ncd_prev on raw output; copy detection is byte equality of raw at build time; cos omitted when None (json_next hops 59, 60); loop text serif, authored prose in the mono body face; loop.py mtime 2026-09-02; Q8, thinking off, no system prompt per README line 36; stop_on_cycle confirm=3.
- No em dashes, no "resonates", no "here's what" in any authored string.

## 1. Fact check: wrong, imprecise or unsupported sentences

Format: quoted sentence; what the data shows; proposed replacement.

### INTRO

1. "Every run starts from the same sentence."
   Data: room 2 (20260902T174854_chat, json_better_para) starts from a 44-word paragraph that begins with the sentence. Annex runs smoke/quine, headers/yours, rule, still, glider start from a bare instruction with no seed sentence at all; still2 and sandwich carry it as a payload line.
   Proposed: "Every room but room 2 starts from this sentence. Room 2 starts from a paragraph that begins with it."

2. "In each room the rule sits at the top." (minor)
   In the built page the order is title, content note, note, fact line, then the rule, then the controls and passages. Annex rooms (bare-text runs) have no rule line at all.
   Proposed: "In each room the rule is shown above the passages."

### INTRO_AFTER_SEED

3. "What a run stops on tends to be about stopping: {{...json_para|15|Time seemed to suspend itself in this moment}}, or {{...json_worse|5|I will never be allowed to stop}}."
   Data: `never be allowed to stop` occurs in 20260902T174258_chat json_worse hop 5 only. The run stopped on hop 7, a truncated JSON whose text ends `where I am the villain, my rent has been` (facts 3.8). The sentence says the run stopped on words it never stopped on.
   Proposed: "What a run stops on tends to be about stopping: {{20260902T155321_chat|json_para|15|Time seemed to suspend itself in this moment}}, or {{20260902T155557_chat|json_page|5|a door to be opened}}." (155557 hop 5 is the fixed point of room 5; the phrase is its last sentence.)

4. "Room 12 is an hour." (minor, now that room 13 exists)
   Proposed: "Rooms 12 and 13 are an hour each."

### Room 1, Better

5. "Asked for a better version of a seven-word sentence, Qwen changed two words."
   Data (20260902T172519_chat json_better hop 1): `came` became `surged` and `early.` became `ahead of schedule.`; two substitution sites, seven words became nine. The marks in the room show one one-word mark and one three-word mark, so a reader will count and disagree.
   Proposed: "Asked for a better version of a seven-word sentence, Qwen replaced two words with four."

### Room 2, Better, paragraph

6. "One expansion, then one small revision that partly undoes the first, and then the taste ceiling."
   Facts are right (hop 1 82 words; hop 2 reverts `in an hour ahead of schedule` toward `an hour early` and changes `bit at` to `cut through`; hops 3..6 identical to 2). "The taste ceiling" is an explanation in jargon, and the sentence is a three-part structure.
   Proposed: "One expansion, then one small revision that partly undoes the first. Nothing after hop 2 is new." (drop the existing last sentence, which this absorbs)

### Room 4, A new paragraph

7. Correct on facts (two dawns at hops 6 and 10, two sunsets at 8 and 12, moon and sand at 15, 16 = 15). Style only, see section 2.

### Room 5, A new passage

8. "Tide, rain, a library, rain again, and then a click, a greenhouse, a letter."
   Data (20260902T155557_chat json_page): the greenhouse, the brass key and the sealed letter are hop 4; the click and the opened letter are hop 5. The order "a click, a greenhouse, a letter" puts the greenhouse after the click.
   Proposed: "Tide, rain, a library, rain on a greenhouse, and then the click of a lock and a letter."

### Room 6, A new passage, twice

9. All numbers verified. "on the left" / "on the right": style.css stacks the two lanes at widths of 64rem and below, so on a narrow window the left slot is the top one. The lanes are labelled "slot A" and "slot B".
   Proposed: "{{...|it crept}} in slot A, {{...|it whispered}} in slot B. Slot A froze at hop 4, in a warehouse. Slot B reached Mara..."

### Room 7, Worse

10. Facts all verified. Style only (see section 2).

### Room 8, Unexpected

11. Content note: "The middle hops contain body horror, and the run ends with a body dissolving into an office."
    Data (20260902T172547_chat json_unexpected hop 23, copied into 24..28): the office becomes a body ("The plastic chair beneath her softened, becoming warm and fleshy", "The office wasn't a place of work; it was a womb"); the memo dissolves into DNA. Hop 24's appended paragraph turns the office back into an office. The direction in the note is reversed. Body horror in the middle hops is supported (hop 7 the polished molar, hop 8 the molar screams, hop 15 her mouth sealed shut).
    Proposed: "The middle hops contain body horror, and the run ends with an office turning into a womb and back. It is shown as it happened."

12. "The same hinge in every hop, several times a hop: it did not do X; it did Y."
    Data (facts 3.7 table): the loose count gives a minimum of 2 per hop (hop 20), so "several" overstates two hops (7 and 20).
    Proposed: "The same hinge in every hop, at least twice a hop: it did not do X; it did Y."

13. "The turns go digital, then cosmic, and then the twist is that there is no twist: a break room, a spreadsheet, dry bread."
    Facts right (break room hop 22, spreadsheet hop 22, dry bread hop 23). Two three-part structures in one sentence.
    Proposed: "The turns go digital and then cosmic. From hop 22 the twist is that there is no twist: a break room and a spreadsheet, then dry bread at hop 23."

### Room 9, Before

14. Facts right. "The coast becomes Chicago, Chicago becomes a server room, and by hop 60 the city is called Aethelgard." is a three-part structure.
    Proposed: "The coast becomes Chicago at hop 12 and a server room at hop 19. By hop 60 the city is called Aethelgard."

### Room 10, No template

15. Facts right. "It leaks a think block at hop 2, starts counting its words, and by the end of hop 6 is numbering them" is a three-verb structure.
    Proposed: "It leaks a think block at hop 2 and starts counting its words. By the end of hop 6 it is numbering them: {{...|The(1) kitchen(2)}}."

### Room 11, A new passage, two models

16. "(hop 2 continues hop 1; the other fifty-eight are beginnings)"
    Data (facts 3.12): hop 1 is an opening, hop 2 continues it, hops 3..60 (58 hops) are fresh openings. So 59 hops are beginnings. "The other fifty-eight" reads as excluding hop 1, which is itself a beginning.
    Proposed: "(hop 2 continues hop 1; every other hop is a beginning)"

17. "a cartographer on every other hop, with one stumble at hop 42"
    Data: cartographer on odd hops 23..41, then hop 42 (archivist) and hop 43 (translator) are both non-cartographer, then even hops 44..60. Hop 42 is a normal off-beat; the missed beat is hop 43.
    Proposed: "a cartographer on every other hop, with one slip at hops 42 and 43"

18. "and between her a lighthouse keeper's logbook, an archivist, a translator, each finding that the record leaves things out."
    Data: the partners from hop 23 on are the lighthouse logbook (24..32), archivist (34, 36, 38, 42, 47, 51, 53, 57), translator (40, 43, 45), librarian (49, 59), lexicographer (55). Two are missing, and the list is a three-part structure.
    Proposed: "and between her a lighthouse keeper's logbook, then an archivist, a translator, a librarian, a lexicographer, each finding that the record leaves things out."

19. "Qwen on the left, Claude Sonnet 4.6 on the right." Same layout issue as item 9; lanes are labelled "Qwen" and "Claude".
    Proposed: "Qwen in one lane, Claude Sonnet 4.6 in the other."

### Room 12, The next passage

20. "The one run asked for what comes after, not for something new."
    Room 13 (qwen_json_next, json_next, 60 hops) is in the build with the identical rule. There are two such runs.
    Proposed: "The first run asked for what comes after, not for something new."

21. "Her name is Maren at hop 2 and Mara at hop 4, and after hop 10 she has no name, because the passage that knew it is gone."
    Data (20260902T181431_anthropic_chat json_next): Maren at hops 1 and 2; Mara at 4..10; unnamed 11..60. Hop 11 was written with hop 10 as its whole context, and hop 10 contains `Mara did not agree or disagree.` So hop 11 dropped the name while it could still see it; only from hop 12 is the passage that knew it gone. The "because" is not what the data shows.
    Proposed: "Her name is Maren at hop 1 and Mara at hop 4. Hop 11 drops it, and no later hop can get it back."

22. "It is one story." (optional hedge)
    Data (facts 3.13): locally continuous, globally drifting: divorced at hop 8, a husband of eleven years at hop 47; Paul's kitchen at hop 5 becomes her own house at hop 10.
    Proposed: "It reads as one story, though a divorce at hop 8 has become a husband of eleven years by hop 47."

### Room 13, The next passage, Qwen

23. "at hop 19 {{...|Centuries bled into millennia}}, which is the kind of place the unexpected room ended in."
    Data: the unexpected room ended in an office (break room hop 22, office/womb hop 23, office again in hop 24's tail). Its cosmic stretch is hops 16..20, the middle. Room 8's own note says the ending is "a break room, a spreadsheet, dry bread"; the two notes contradict each other.
    Proposed: "which is the kind of place the unexpected room passed through."

24. "Six hops are shown as raw JSON because Qwen's quoting inside the text field did not parse; the story runs through them."
    Data (steps.jsonl): hops 25, 38, 41, 42, 43 fail on unescaped double quotes inside the text field (finish=stop). Hop 50 fails because it hit the 600-token limit (finish=length, tok_out=600, unterminated string). Five are quoting, one is the wall.
    Proposed: "Six hops are shown as raw JSON. In five, Qwen's quoting inside the text field did not parse; hop 50 hit the token wall. The story runs through them."

25. "My reading: a rule that identity can satisfy (better, a new passage) finds a fixed point in Qwen; a rule it cannot satisfy (after, before) does not."
    Data: worse (fixed point hop 7) and unexpected (hop 24) also found fixed points, and identity satisfies neither rule; both stopped only when the token limit broke the JSON. The reading as stated ignores two of the rooms.
    Proposed: "My reading: a rule that identity can satisfy (better, a new passage) finds a fixed point in Qwen at once. After and before never stop. Worse and unexpected stopped only when the token wall broke their JSON."

26. "Elara, a lighthouse, a Keeper." Facts right (Elara 1..49 and 51..60, lighthouse 1..10, Keeper 8..10 and 16..17). Three-part list.
    Proposed: "Elara at a lighthouse, then a Keeper."

### ANNEX_INTRO

27. "Before the JSON rule."
    Data (runs/ mtimes): smoke 15:25, headers 15:34, headers3 15:46, headers2 15:47, first JSON run 15:53. True for seven of the eight annex rooms. The eighth, "A new sentence, Claude" (20260902T175821_anthropic_chat), ran at 17:58 with the JSON rule.
    Proposed: "Mostly before the JSON rule. The first attempts carried the instruction as a bare line of prose, and the loop mostly ate it: the model read the line and obeyed it once, then answered whatever was under it. These runs are the instrument being found. The last one is a three-hop test of the Claude backend. Same reader."
    (This also removes the three-part "read the line, obeyed it once, and answered".)

28. "the loop mostly ate it: the model read the line, obeyed it once, and answered whatever was under it."
    For yours and rule the line was never eaten (all 10 hops are byte-identical to X_0) and there was nothing under it. "mostly" covers this; no change needed beyond item 27.

### Annex notes

29. Still: "Begin with this exact line, then write something new." and Still2: "Copy this line first, then reply to what is below."
    These are near-quotes of X_0 (`Begin your reply with this exact line, then write something new below it.` and `Copy this line first, then reply to whatever is below it.`) shown without quote marks. Not wrong, but rule 1 forbids paraphrases that read as quotes. The exact line is visible at hop 0, so this is optional.
    Proposed: "The header says to begin with the line and write something new below it." / "The header says to copy the line and reply to what is below it."

30. Still2: "It copied the sentence, then greeted itself, then invented a task." Facts right (hop 1 copies the payload, greetings hops 3..6, question hop 7, answer hop 8). Three-part structure.
    Proposed: "It copied the sentence and greeted itself. By hop 7 it had invented a task."

31. Quine: "Refused at hop 1; a chat about starting fresh by hop 4." Right (hop 3 already says "let's start fresh"; hop 4 "Since we're starting fresh"). No change.

32. Glider, Yours, Rule, Sandwich, Claude sentence: verified, no change.

### POEM_HEAD

33. Verified against the brief. No change.

### COLOPHON

34. "What is data": "Every passage in a room is the model's output for that hop, byte for byte, taken from data/<run>.json in the loop directory."
    Room 13 comes from site/runs_extra/qwen_json_next/steps.jsonl. The build appends an "Added after the bundle" paragraph that says so, which is enough. No change needed, but see item 41.

35. "The rule line above each room is the rule field of the run's starting object."
    Seven annex rooms are bare-text runs and have no rule line; there the whole instruction is the hop-0 text.
    Proposed: "In the JSON rooms the rule line is the rule field of the run's starting object. In the annex the starting text is the whole instruction."

36. "Where a passage is shown in monospace it is because the model's output at that hop did not parse as the JSON object it was asked for: usually the token limit cut it off."
    Data: the 64 annex hops of smoke/headers/headers2 are all monospace and were never asked for JSON. Room 10's 39 monospace hops are a transcript, not a cut JSON object (they were also cut at 600 tokens). Room 13 has five hops that are monospace because of unescaped quotes.
    Proposed: "Where a passage is shown in monospace it is because the model's output at that hop did not parse as the JSON object it was asked for: usually the token limit cut it off, in room 13 five times because of quote marks inside the text field. The bare-text runs in the annex are monospace throughout because there was no JSON to parse."

37. "Nothing in the data was edited, smoothed or paraphrased." Three-part list.
    Proposed: "Nothing in the data was edited or paraphrased."

38. "What is authored": "The site title, the room titles, the room notes, this page, and the few lines of framing on the front are mine ... They are set in the small instrument face; the loop's text is set in serif."
    style.css line 47 sets h1, h2, h3 in the serif face, so the site title and room titles are serif, not the instrument face. The list also omits the content notes, the annex intro and notes, the poem head, the TOC summaries and the interface labels (it saw, it wrote, slot A, next, back).
    Proposed: "The site title, the room and annex titles and notes, the content warnings, the interface labels, this page, and the few lines of framing on the front are mine, written by a Claude context (Fable 5.1) on 2026-09-02 from the run logs and the README. The notes and this page are set in the small instrument face; the titles and the loop's text are set in serif."

39. "The reader": "When a hop keeps at least half of the previous hop's words, the words that changed are marked"
    build.py diff_marks: frac = matched / len(current words). The test is on the current hop's words, not the previous hop's. (NOTES.md says "5-gram survival >= 0.5", which is a third description; the code is the LCS one.)
    Proposed: "When at least half of a hop's words are carried over from the previous hop, the words that changed are marked; when a hop is mostly new, nothing is marked."

40. "The harness": "max_tokens differed by run (300 for the paragraph room, 600 for the passage rooms and the Claude rooms, 800 for the better and worse rooms, 128 to 256 for the annex)."
    runs/<run>/summary.json via facts.md: json_para 300; 155557, 160344, 162514_raw, 165324 (before), 172547 (unexpected), both Claude 60-hop runs and qwen_json_next 600; 172519, 174854, 174258 800; smoke 128, headers 256, headers2 200, Claude smoke 200; headers3 (room 3, A new sentence) 200. Room 3 is missing from the list, and "passage rooms" has to be read as covering Unexpected, Before and No template.
    Proposed: "max_tokens differed by run: 200 for the sentence room, 300 for the paragraph room, 600 for every room with a 250-word rule and for the Claude rooms, 800 for the better and worse rooms, 128 to 256 for the annex."

41. "The harness": "Qwen rooms: Qwen3.8-27B Q8 served locally by llama.cpp, temperature 0, thinking off, no system prompt." Verified against README. Three-part tail; optional.
    Proposed: "Qwen rooms: Qwen3.8-27B Q8 served locally by llama.cpp at temperature 0, with thinking off and no system prompt."

42. "Not in this site": "One Claude run with zero hops (an API header was missing; it is in the index as a failed smoke test)."
    On this site "the index" is the front page (Escape goes to "the index"); the sentence means data/index.json. Also the paragraph is three parallel fragments.
    Proposed: "The Claude run with zero hops is not here (an API header was missing; data/index.json lists it as a failed smoke test). Nor are the probe and watermark experiments mentioned in the README, whose logs are not in the data bundle, or the eleven-state map of the passage-scale runs, which the README describes and this site leaves for another day."

43. "The reader": "Next moves forward one hop. Back moves back, which the loop could not do. Play advances every two and a half seconds." Three parallel sentences; optional.
    Proposed: "Next moves forward one hop, and back moves back, which the loop could not do. Play advances every two and a half seconds."

44. "The track": "an exact copy is a stub at the floor (about 0.03, the wrapper's share)". Data: ncd_prev on exact copies is 0.027..0.042 in the JSON rooms and 0.040..0.082 in the annex (facts section 4). "About 0.03" is fine for the rooms; "the wrapper's share" will not mean anything to a stranger. Optional.
    Proposed: "(about 0.03: what zlib charges for the JSON wrapper even when nothing changed)".

45. Build-time footer: "Built ... from C:\ai\loop\data by site/build.py." Room 13 is built from site/runs_extra. Optional: "from C:\ai\loop\data and site/runs_extra".

## 2. Style lint (brief rule 3)

Em dashes: none in authored text. "resonates": absent. "Here's what" openers: none. Contractions are fine.

Three-part parallel structures. Strict list of every candidate, strongest first; the author decides.

Strong (exactly three parallel items or three same-shaped sentences):
- Room 2: "One expansion, then one small revision that partly undoes the first, and then the taste ceiling." (fix in item 6)
- Room 4: "runs through a storm, a cracking hull, two dawns and two dusks, and comes to rest". Proposed: "The sea story runs through a storm that cracks the hull and through two dawns and two dusks. It comes to rest on a moonlit shore where {{...}}."
- Room 5: "a click, a greenhouse, a letter" (fix in item 8)
- Room 7: "Hop 6 hits the 800-token wall mid-sentence. Hop 7 makes the broken JSON worse. Hop 8 copies it." Proposed: "Hop 6 hits the 800-token wall mid-sentence, and hop 7 makes the broken JSON worse. Hop 8 copies it."
- Room 7: "Qwen added {{which was annoying}}. Then a flooded basement. Then the foundation." Proposed: "Asked for a worse version, Qwen added {{...|which was annoying}}. By hop 3 the basement had flooded and the foundation had liquefied."
- Room 8: "digital, then cosmic, and then the twist" and "a break room, a spreadsheet, dry bread" (fix in item 13)
- Room 9: "The coast becomes Chicago, Chicago becomes a server room, and by hop 60..." (fix in item 14)
- Room 10: "leaks a think block at hop 2, starts counting its words, and by the end of hop 6 is numbering them" (fix in item 15)
- Room 11: "a lighthouse keeper's logbook, an archivist, a translator" (fix in item 18)
- Room 13: "Elara, a lighthouse, a Keeper." (fix in item 26)
- ANNEX_INTRO: "read the line, obeyed it once, and answered whatever was under it" (fix in item 27)
- Annex Still2: "It copied the sentence, then greeted itself, then invented a task." (fix in item 30)
- Colophon: "edited, smoothed or paraphrased" (fix in item 37)
- Colophon "Not in this site": three same-shaped fragments (fix in item 42)

Weaker candidates (three-step sequences or three clauses of similar weight):
- Room 1: "Qwen changed two words. Handed the result, it changed nothing. Handed that, nothing."
- Room 12: "Her name is Maren at hop 2 and Mara at hop 4, and after hop 10 she has no name" (fix in item 21 removes it)
- Room 13: "which is the kind of place ... Here the rule says after, so there is an after. At hop 24 ..." (not parallel, listed for completeness)
- Colophon "The reader": "Next moves forward one hop. Back moves back... Play advances..." (item 43)
- Colophon "The harness": "temperature 0, thinking off, no system prompt" (item 41)
- Colophon "What is data": "The hop numbers, token counts, stop reasons and metrics" (four items, fine)

Explaining rather than matching the register:
- Room 2: "and then the taste ceiling" (jargon; item 6)
- Room 12: "because the passage that knew it is gone" (an explanation, and not quite right; item 21)
- Room 13: "Here the rule says after, so there is an after.", "The horizon was reached and passed.", and the "My reading:" sentence. The brief allows authored framing that reads as yours; these three are the only places on the site that argue. Keep at most one. If one stays, the "My reading" sentence, corrected as in item 25, is the honest one.
- INTRO_AFTER: "and that is the other half of the finding." Mild; optional.
- Room 9: "There is no horizon in this direction, only more of it." In register; fine.

Clumsy or unclear:
- Room 11: "and between her a lighthouse keeper's logbook" ("between her" for "between her appearances"). Proposed in item 18 keeps the phrase; alternative: "and in the gaps a lighthouse keeper's logbook, ...".
- ANNEX_INTRO: "Same reader." A stranger will not know "reader" means the instrument. Proposed: "The same reader as the rooms."
- Room 3: "The smallest loop." Room 1's loop is a nine-word sentence with period 1; "smallest" is arguable. Proposed: "The shortest cycle that is not a copy."
- Colophon "The reader": "Word-level longest-common-subsequence, computed at build time, presentation only." A fragment; fine in a colophon.
- Room 12: "Read it the way it was written: one passage, and the one before it." Good.

## 3. Reading index.html

Structure as built: front (title, sub, intro, hop 0 seed, second intro, "Enter room 1", TOC of 13 rooms, links to poem, colophon, annex), 13 room sections, poem, colophon, annex index, 8 annex room sections. Every room: h2, optional content note, note, fact line, rule line (JSON rooms only), controls, one or two lanes each with a track SVG, an "it saw" slot, an "it wrote" slot, and the full `<ol class="hops">`.

Checked and fine:
- Citations: all 589 `<li class="hop">` (566 hops + 23 seeds) carry hop number, run id and tag; hops carry the model name (Qwen3.8-27B or Claude Sonnet 4.6). Room 13's run id is `qwen_json_next`, which is not a timestamp id like the others; the colophon's "Added after the bundle" paragraph explains where it comes from.
- Poem: exact match with the brief, including the title and the signature line.
- Hash routing (#room/t), next/back/play, raw toggle, sound, theme toggle, keyboard: consistent with the colophon. Two undocumented keys exist (j/k for next/back, n/b for next/previous room); harmless.
- The two-lane rooms handle unequal lengths: past hop 9 the Qwen lane in room 11 shows "No hop N recorded. The harness stopped this run at hop 9: cycle confirmed x3."
- The status line under the counter says "unchanged" when a hop equals the previous one and "same as hop N" otherwise, matching the colophon.
- Room 12 hop 1 shows Claude's preamble in mono above the story in serif, with a tooltip. The colophon does not mention this case; optional one clause.

Things a careful stranger would trip on:
- Front: "Every run starts from the same sentence" directly above a room list whose room 2 does not (item 1).
- Front: the second quotation in "What a run stops on tends to be about stopping" is from a hop the run did not stop on (item 3). Anyone who walks room 7 to the end will see the fixed point ends with "my rent has been".
- Room 8's content note describes the ending backwards (item 11); room 13's note then says the unexpected room "ended" in a cosmic place, which room 8's own note denies (item 23).
- Room 12 says it is "the one run" with the after rule; room 13 is the next room (item 20).
- TOC and fact lines for annex Yours and Rule say "holds from hop 0" / "exact fixed point from hop 0" while the front labels the seed "hop 0". The notes explain it ("Copied exactly from hop 1"), but the TOC line alone is puzzling. Optional: build.py could print "holds from hop 0 (the seed itself)" when transient_exact is 0.
- The in-page keys hint (`title` on "keys → ← p r s esc") lists next, back, play, raw and esc but not s for sound, though the button label shows s. Minor, in build.py.
- Hover-only citations on the `<q class="cited">` quotes in the notes: rule 1 asks for a citation wherever a text appears; a title tooltip is invisible on touch and in print. Optional: render the citation as a small visible suffix (run, hop) or at least in the print stylesheet.
- "the wrapper's share", "cycle confirmed x3", "5-gram survival", "ncd": instrument vocabulary a stranger meets before the colophon explains it. The fact line and metrics line are data and can stay; the colophon covers ncd and survival. "cycle confirmed x3" is never explained; one clause in "The harness" would do ("the index calls this cycle confirmed x3").
- "Left"/"right" in rooms 6 and 11 become top/bottom below 64rem (items 9, 19).
- Colophon "in the index" (item 42).

## 4. Necessary fixes, most important first

1. INTRO_AFTER_SEED: replace the json_worse hop 5 quote in "What a run stops on tends to be about stopping"; the run stopped on hop 7 ("my rent has been"), not on "I will never be allowed to stop". Use a fixed-point phrase such as 155557 json_page hop 5 "a door to be opened".
2. Room 12 note: "The one run asked for what comes after" is false now that room 13 (qwen_json_next, same rule) is built. Say "The first run".
3. Room 8 content note: the ending is an office turning into a womb (hop 23) and back (hop 24 tail), not "a body dissolving into an office".
4. Room 13 note: "the kind of place the unexpected room ended in" contradicts room 8 (it ended in an office); say "passed through". And "Six hops ... because Qwen's quoting did not parse": five are quoting (25, 38, 41, 42, 43), hop 50 is the 600-token wall.
5. INTRO: "Every run starts from the same sentence" is false for room 2 (44-word seed) and for five annex runs (bare instruction, no seed sentence).
6. Room 11 note: "the other fifty-eight are beginnings" (hop 1 is also a beginning; say "every other hop is a beginning"); "one stumble at hop 42" (the missed beat is hop 43; say "one slip at hops 42 and 43"); the partner list omits the librarian (49, 59) and the lexicographer (55).
7. Room 12 note: "Maren at hop 2" (first at hop 1) and "because the passage that knew it is gone" (hop 11 dropped the name while hop 10, its whole context, still contained "Mara").
8. ANNEX_INTRO "Before the JSON rule": the annex's last room is the Claude smoke test, run at 17:58 with the JSON rule.
9. Colophon "The harness": the max_tokens list omits room 3 (headers3, 200); add it.
10. Colophon "What is data": the monospace sentence does not cover the annex (64 bare-text hops, never asked for JSON) or room 13's five quote failures; and "the rule line above each room" does not hold in the annex.
11. Colophon "The reader": the diff-mark rule is "at least half of the current hop's words carried over" (build.py diff_marks), not "keeps at least half of the previous hop's words".
12. Colophon "What is authored": titles are set in serif (style.css h1, h2, h3), not in the instrument face; the list of authored parts omits the annex notes, content notes and interface labels.
13. Colophon "Not in this site": "it is in the index" reads as this site's index; say data/index.json.
14. Room 1 note: "changed two words" reads against the marks on screen (two sites, four words in); say "replaced two words with four".
15. Rule 3 three-part structures, strong cases: rooms 2, 4, 5, 7 (twice), 8 (twice), 9, 10, 11, 13; annex intro; annex Still2; colophon "edited, smoothed or paraphrased" and the "Not in this site" paragraph. Replacements are given in sections 1 and 2.
16. Room 2 note: drop "the taste ceiling" (explanation in jargon; rule 3).
