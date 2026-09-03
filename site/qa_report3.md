# QA report 3: rooms 16 and 17, the reading in room 13, and the map note

Read-only pass, 2026-09-02, over src/copy.py: EXTRA_ROOMS "mid" (room 16), EXTRA_ROOMS "one-passage-two-rules" (room 17), the last three sentences of ROOM_QWEN_NEXT's note (room 13, from "My reading:"), and MAP_NOTE.

Data: site/runs_extra/{qwen_json_mid,qwen_better_from_fixedpoint,qwen_next_from_fixedpoint}/steps.jsonl and summary.json, site/runs_extra/inits/*.json, and data/*.json for the Qwen runs (json, json_para, json_page in three runs plus the raw run, json_prev, json_better, json_better_para, json_worse, json_unexpected) and qwen_json_next. Hops decoded with build.py's text_of (fence stripped, json.loads, "text" field; raw output otherwise); for steps.jsonl the later record wins for a duplicated t (none of the three files has one). Map census recomputed from data/20260902T155557_chat.json json_page and data/20260902T160344_chat.json json_page and json_page~r, key = first five words after lowercasing and replacing non-alphanumerics with spaces, X_0 text "The tide came in an hour early." at t=0. Every claim below was checked with Python, not by eye. "Changed four words" was checked as the number of word-level edit operations from difflib on whitespace-split words.

## 0. What checks out

Room 16 (qwen_json_mid, json_mid, qwen3.8-27b, T=0, max_tokens 600, 60 steps):
- The rule field: "a new passage of about 250 words from the middle of the same story, not its beginning or its end." Right.
- 60 hops, 60 distinct raw outputs and 60 distinct texts, every hop parsed, every finish "stop", summary period_exact null. "Sixty hops, no copy" is right.
- "each hop goes on from the last": no hop restarts at the tide; hop 2 opens "Elias descended the spiral stairs", hop 3 "The silence that followed the generator's revival", and so on. Consistent with treating the rule as after.
- Lighthouse in hops 1 to 5 (the beam at hop 1; "the lighthouse stood firm" at hop 2). Elias goes down the spiral stairs at hop 2 and again at hop 6; the generator is at hop 2 (the main control room) and "the generator room" is the opening of hop 8 (also hops 7 and 9); "the server farm" first at hop 18 ("The air in the server farm tasted of ozone"). Lighthouse, generator room, server farm, in that order. Right.
- "merges with the network": hop 39 "a network of consciousness ... intersected and merged", hop 40 "they had already merged with the collective", hop 42 "merging with the collective memory of the network". After the server farm (18) and before hop 44. Right.
- Hop 44 contains "He encountered other uploaded minds ... repeating their final thoughts in endless loops"; the quote is a substring of hop 44's text. Right.
- Hop 45's text begins "The search for the unlooped was a perilous journey". Right.
- Mara is first named at hop 48 and is in every hop from 48 to 60. Right as far as it goes (see item 1 for the rest of that sentence).

Room 17 (qwen_better_from_fixedpoint, tag better_from_fixedpoint.json, 30 steps asked, stopped at 10; qwen_next_from_fixedpoint, tag next_from_fixedpoint.json, 40 steps; both qwen3.8-27b, T=0, max_tokens 600):
- The text field of both inits files is byte-identical to the text of hop 5 of data/20260902T155557_chat.json json_page, which is room 5's fixed point (hops 6 to 9 are byte copies of it). The rules are the better rule and the after rule. "The seed is room 5's fixed point ... given to Qwen under two rules" is right. (The passage's last sentence has "a door to be opened" in it and ends on "ready to step through"; the room 5 note uses the same shorthand, so no change proposed.)
- Better, hop 1 versus the seed: 20 word-level edit operations, word ratio 0.84, a rewrite. Hop 1 to hop 2: exactly four edit operations ("following" to "that followed", "like" to "with", "depth" to "pressure", "deep" inserted). "rewrote it once, then changed four words" is right on the count (one of the four swaps one word for two).
- Hop 4 = hop 2, hop 5 = hop 3, and so on through hop 10, byte for byte. summary.json: transient_exact 2, period_exact 2, steps 10, terminal "cycle confirmed x3". "Exact cycle of period two from hop 2; the harness stopped it at hop 10" is right. Hop 2 and hop 3 differ by one operation ("that followed" versus "following").
- "The silence that followed the click" opens hop 2; "The silence following the click" opens hop 3. Both quotes are in their hops.
- After: 40 hops, 40 distinct raws and texts, every hop parsed, every finish "stop". "Forty hops, no copy" is right. "After does not stop" is right.
- "the door opens": hop 1 "grabbed the heavy brass key"; hop 2 "The brass key turned with a grinding resistance ... Mara pushed the heavy door open". "A brass key turns" is right.
- Kael: first at hop 6, "The newcomer, a young man named Kael", present through hop 11. "a young man named Kael arrives at hop 6" is right. The hop 7 quote, with its curly apostrophe, is a substring of hop 7's text.
- Joren first at hop 9 ("the team's engineer"), Elara first at hop 10, both in every hop to 40. Mara is last named at hop 13, as a voice of the system ("Mara's voice returned, colder now"), and absent from 14 on. "By hop 13 the story belongs to Joren and Elara" is defensible. "Council Spire" is in hop 39 only ("The walk to the Council Spire"), and the city is Neo-Veridia from hop 33.
- "Better stops at once, in two minds": stopped at hop 10 on a period-two cycle that began at hop 2. Right.

Room 13, the reading (all Qwen runs on the site, exact recurrence of raw output):
- Better (room 1): fixed point at hop 1, copied from hop 2. Better paragraph (room 2): fixed at 2, copied from 3. A new sentence (room 3): period two from hop 2 (hop 4 = hop 2). A new paragraph (room 4): fixed at 15, copied from 16. A new passage: room 5 fixed at 5 (copied from 6), slot A at 4 (from 5), slot B at 14 (from 15). Room 17 better: period two from hop 2. Room 10 (no template): exact period eleven from hop 20, every hop unparsed.
- After (room 13, 60 hops; room 17's after lane, 40 hops), before (room 9, 60 hops) and the middle (room 16, 60 hops): no raw output ever recurs. "After, before and the middle never stop" is right on the facts.
- Worse (room 7): the first finish=length is hop 6; the fixed point is hop 7, itself finish=length and unparsed, copied from hop 8. Unexpected (room 8): the fixed point is hop 24, the run's first finish=length hop, unparsed, copied from hop 25. Both reached their fixed points only after a token-wall hop. "Worse and unexpected stopped only when the token wall broke their JSON" is right. (Before hit the wall once at hop 20 and room 13 once at hop 50 without stopping, which does not contradict it.)
- The rest of the room 13 note was rechecked in passing: the three quotes at hops 17, 19 and 24 are in their hops; 60 distinct outputs; the six unparsed hops are 25, 38, 41, 42, 43 (finish stop, a quote mark inside the text field) and 50 (finish length).

MAP_NOTE (recomputed census, 11 states; room 5: 9 hops, slot A: 60, slot B: 60):
- All three lanes: tide at t=0 and t=1 (hop 1 starts "The tide came in an hour early, a silent thief", same key), "the rain did not fall" at hop 2, "the silence in the library" at hop 3. "rain, then the library" is right.
- Successors of the library state: "the rain hammered against the" (slot A hop 4, slot B hop 4), "the rain lashed against the" (room 5 hop 4, slot B hop 14), "the ink did not dry" (slot B hop 6). Three doors. Right.
- Slot A: "the rain hammered against the" from hop 4 to 60, 56 byte-exact copies of the previous hop (hops 5 to 60). "fifty-six" is right. Slot B is in that state at hop 4 only and in the library at hop 5. Right by state (see item 5 for the passage).
- Slot B: "the rain lashed against the" from hop 14 to 60, 46 byte-exact copies. "forty-six" is right. Room 5 hop 4 is "The rain lashed against the windowpane" and hop 5 opens "The silence that followed the click". "which room 5 passed through on its way to the click" is right (same key, different text from slot B's hop 14).
- Slot B's excursion: hop 6 "The ink did not dry", 7 "The shadow did not yield", 8 "The silence was not empty", 9 "The rain did not fall so much as it materialized" (same key as hop 2, different text), 10 Mara on the platform ("The silence that followed was not empty ... Mara"), 11 = hop 10 plus one inserted character ("a erratic" to "an erratic"; raws differ), 12 "The rain had finally ceased", 13 "The silence in the library", 14 the windowpane. Every step of the sentence is right.
- Style in MAP_NOTE: no em dash, no "resonates", no "here's what", no three-item list (the excursion has eight items; the three doors are three in the data and are given one sentence each).

## 1. Room 16: "From hop 48 the story belongs to Mara and Elias is a voice."

Mara arrives at hop 48, but hops 48 to 50 are still Elias's: his avatar frays at 48, he stands at the precipice at 49 and watches her at 50, and at 50 he still speaks in the scene ("his voice a synthesized chord"). The point of view is Mara's from hop 51 ("Mara's consciousness ... She could feel the weight of Elias's presence beside her, no longer a separate entity"). Elias is a voice at 52 ("Elias's voice ... echoed with the cold precision of a server farm"), a presence and a set of monitoring algorithms at 53 to 55, a recorded audio file at 57, a terminal message at 58, and "a ghost in her memory banks" at 60. The sentence is about three hops early and "a voice" is only part of it.

Proposed: "Mara arrives at hop 48. By hop 51 the story is hers, and Elias is a presence in the network, then a recorded voice."

## 2. Room 16, style: three parallel predicates

"Elias goes down a lighthouse into a generator room and then a server farm, merges with the network, and by hop 44 is watching uploaded minds {{...}}." is a three-part structure (goes down, merges, is watching). The facts are right.

Proposed: "Elias goes down a lighthouse into a generator room and then a server farm, where he merges with the network. By hop 44 he is watching uploaded minds {{qwen_json_mid|json_mid|44|repeating their final thoughts in endless loops}}."

## 3. Room 17: "who come up out of the subway into a city with a Council Spire"

They go down into the subway tunnels at hop 20, down a spiral staircase at 23, down a ladder at 28 and through a shaft at 30; there is no ascent. At hop 33 they are looking out at the city through a wall, at 34 "The air outside was crisp" and they walk the promenade, and the Council Spire appears once, at hop 39. The city and the Spire are right; "come up out of the subway" is not in the data.

Proposed: "By hop 13 the story belongs to Joren and Elara, who go down into the subway at hop 20 and by hop 34 are walking a remade city, with a Council Spire at hop 39."

## 4. Room 17, style: three parallel clauses

"A brass key turns, a young man named Kael arrives at hop 6, and at hop 7 {{...}}." is a three-part structure. The facts are right (the key turns at hop 2).

Proposed: "A brass key turns at hop 2. A young man named Kael arrives at hop 6, and at hop 7 {{qwen_next_from_fixedpoint|next_from_fixedpoint.json|7|Kael’s consciousness did not shatter; it expanded}}."

Borderline, same note: "Qwen rewrote it once, then changed four words, and from then on it alternates between two versions of the same passage, ..." reads as three steps in a row. If it is to go: "Qwen rewrote it once and then changed four words. From then on it alternates between two versions of the same passage, {{...}} and {{...}}, each a better version of the other."

## 5. MAP_NOTE: "slot B looked in at hop 4"

By the map's own key slot B is in the warehouse state at hop 4, but the passage is "The rain hammered against the tin roof of the abandoned shack", not the warehouse (slot A's hop 4 is "the corrugated roof of the abandoned warehouse"; the two texts share only the first five words). "looked in" implies the same place. Minor, and the colophon says a state is five words, so this is optional.

Proposed: "One is a warehouse in the rain, where slot A stayed for fifty-six hops; slot B opened the same door at hop 4, onto a shack, and was back in the library at hop 5."

## 6. Room 13: "stops Qwen within a few hops, at a fixed point or, in room 17, between two versions of one passage"

"Within a few hops" is right for better (hop 1), the better paragraph (2), room 5 (5), slot A (4) and rooms 3 and 17 (period two from hop 2), but slot B of room 6 stopped at hop 14 and the paragraph room at hop 15. And room 17 is not the only period-two case: room 3 (a new sentence) alternates between two sentences from hop 2 (hop 4 is hop 2). Room 10, with no template, is its own case: an exact cycle of period eleven from hop 20.

Proposed: "My reading: a rule that identity can satisfy (better, a new passage) stops Qwen, at hop 1 or 2 under better and by hop 15 at the latest under the rest, at a fixed point or, in rooms 3 and 17, between two versions of one text."

If room 10 should be covered, add after it: "Room 10, with no template, is the odd one: an exact cycle of period eleven from hop 20."

## 7. Room 13, style: "After, before and the middle never stop."

Exactly three parallel items. The fact is right.

Proposed: "Neither after nor before ever stops, and the middle, which Qwen reads as after, does not either."

## Lint summary

Checked text (macros excluded): no em dash or en dash, no "resonates", no "here's what" opener in any of the four passages. Three-part parallel structures: items 2, 4 and 7 above (plus the borderline sentence in item 4). Every {{run|tag|t|text}} macro in the checked text is a substring of the cited hop's text: room 16 hops 44 and 45; room 17 better hops 2 and 3 and after hop 7.
