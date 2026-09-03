# QA report 2: the material added after qa_report.md

Read-only pass, 2026-09-02, over the new authored text only: src/copy.py ROOM_QWEN_NEXT (room 13), EXTRA_ROOMS "sonnet5-passage" (room 14) and "alternating" (room 15), MAP_NOTE, the changed INTRO_AFTER_SEED, the COLOPHON sections "What is data", "The map", "The harness", "Not in this site", plus the two strings build.py generates for the new material (the map facts line "N states over M hops" and the colophon paragraph "Added after the bundle").

Data: site/runs_extra/{qwen_json_next,sonnet5_json_page,alternating_json_page}/steps.jsonl, decoded with build.py's text_of (fence stripped, json.loads, "text" field; raw output otherwise), later record kept for a duplicated t (alternating t=1 has two records, the site uses the second: 368 tokens, not 360). Map census recomputed independently from data/20260902T155557_chat.json (json_page) and data/20260902T160344_chat.json (json_page, json_page~r) with key = first five words after lowercasing and replacing non-alphanumerics with spaces, X_0 text "The tide came in an hour early." at t=0. Every claim below was checked with Python, not by eye.

## 0. What checks out

Room 13 (qwen_json_next, json_next, 60 hops, qwen3.8-27b, T=0, max_tokens 600):
- 60 hops, 60 distinct raw outputs and 60 distinct texts: "Sixty hops, no copy" is right.
- Rule field byte-identical to room 12's json_next rule.
- The three quotes are in the cited hops: "simply became transparent" (17), "Centuries bled into millennia" (19), "Elara felt her form begin to solidify" (24).
- Elara from hop 1, lighthouse hops 1 to 10, Keeper from hop 4. After hop 24: bakery 27, council 28, stone bridge 30, tunnel 57, reservoir 59.
- Six unparsed hops shown as raw JSON: 25, 38, 41, 42, 43, 50. Five (25, 38, 41, 42, 43) fail on an unescaped quote mark inside the text field (json error "Expecting ',' delimiter" at that quote; finish=stop). Hop 50 is finish=length at 600 tokens (unterminated string). "In five ... hop 50 hit the token wall" is exact.
- "Worse and unexpected stopped only when the token wall broke their JSON": room 7 fixed point is hop 7 (800 tokens, finish=length; copied 8 to 11), room 8 fixed point is hop 24 (600 tokens, finish=length; copied 25 to 28). Right.

Room 14 (sonnet5_json_page, json_page, claude-sonnet-5, sampling "default", max_tokens 600, stop_on_cycle false; the other lane is room 11's 20260902T175920_anthropic_chat json_page):
- Same seed and rule in both lanes (both start from INITS["json_page"]).
- Hop 2: 600 tokens, finish max_tokens, text ends "while the tower stood silent, its" (mid-sentence). Right.
- Hop 3 versus the text field of hop 2: exactly one deletion ("an quiet man" to "a quiet man", hop 2 char 946) and one insertion at the end (" secrets folded quietly into the gathering dusk, waiting for the next hour to strike."). "handed back the same passage with ... corrected ... and the sentence finished" is exact. Both quotes are in the cited hops.
- Hop 7 raw is byte-identical to hop 6 raw (a lighthouse at Bell's Point). Hop 8 is a clocktower (Millbrook). Right.
- Hops 9 to 19 alternate lighthouse (odd) and orchard (even): 9 L, 10 O, 11 L, 12 O, 13 L, 14 O, 15 L, 16 O, 17 L, 18 O, 19 L. Hop 19 is 600 tokens, finish max_tokens, raw ends "quiet pride in". Right.
- Hops 20 to 60 are all byte-identical to hop 19: hop 20 copies it, and the forty after (21 to 60) do too. summary.json says transient_exact 19, period 1. Right.
- Room 11's note says "Sonnet 4.6 never copies" (that run: 60 distinct outputs). Rooms 7 and 8 froze on finish=length outputs. "it froze where Qwen froze in rooms 7 and 8: on the token limit" is right.

Room 15 (alternating_json_page, json_page, 60 hops, all parsed):
- Odd hops 1 to 59 are claude-sonnet-4-6, even hops 2 to 60 are qwen3.8-27b; both at sampling T=0. Right.
- Hop 2 text == hop 1 text; raws differ only in whitespace (json.loads equal; equal after stripping whitespace). The reader shows "same words as hop 1, JSON spaced differently" and no copy mark. Right.
- Hops 6, 16 and 50 each begin with the whole of the previous (Claude) text and add to it (see item 3 for what "added a paragraph" gets wrong).
- 13 of Qwen's 30 hops begin with the words "The silence in the": 8, 14, 22, 24, 26, 30, 36, 40, 46, 48, 54, 58, 60 (see item 8 for the wording). The quote "The silence in the village was not empty" is in hop 14. The map's library state is labelled "The silence in the library".
- "eleven years" occurs in exactly ten odd hops: 3, 7, 13, 15, 23, 27, 31, 35, 37, 57 (and in one even hop, 16, inside the passage Qwen kept). "ten of them" is right as a count of Claude's hops.
- "The cartographer's studio" is in hop 55 (its first words).
- 60 distinct raw outputs; 59 distinct texts (hop 2 = hop 1). No byte copy anywhere.
- Neither map sink key ("the rain hammered against the", "the rain lashed against the") occurs in any hop of room 15. The library key occurs seven times (22, 24, 26, 30, 48, 54, 58); "the rain had finally ceased" (slot B's exit state) once, at hop 32.

Map census (recomputed): 11 states, 129 hops (room 5: 9 hops; slot A: 60; slot B: 60), which is what index.html prints ("11 states over 129 hops"). Per state: tide 6 visits (t=0 and t=1 in all three runs, so 3 same-opening self-transitions, no exact copy); rain did not fall 4; library 5; rain hammered 58 visits, 56 exact copies; rain lashed 48 visits, 46 exact copies; silence that followed the 5 visits, 4 exact copies; ink, shadow, silence was not empty, rain had finally ceased 1 each; silence that followed was 2 visits, 1 same-opening self-transition. The one-character copy is slot B hop 10 to 11: a single inserted "n" ("a erratic" to "an erratic"). Edge counts: tide to rain 3, rain to library 3, library to lashed 2, library to hammered 2, library to ink 1, hammered to library 1, lashed to silence-that-followed-the 1, ink to shadow 1, shadow to silence-was-not-empty 1, silence-was-not-empty to rain-did-not-fall 1, rain-did-not-fall to silence-that-followed-was 1, silence-that-followed-was to rain-had-finally-ceased 1, rain-had-finally-ceased to library 1. So in the facts line: "11 states", "129 hops", "hop 1 of every run starts like the seed", "Mara's copy was one character off", solid loops ×56 ×46 ×4, dashed loops at the tide (×3) and Mara (×1) all check out. In MAP_NOTE: "Three runs leave the tide the same way: rain, then the library" (all three: tide at t=0 and 1, rain at 2, library at 3), "slot A stayed for fifty-six hops" (56 exact copies of hop 4, hops 5 to 60), "slot B stayed for forty-six" (46 copies of hop 14), "which room 5 passed through on its way to the click" (room 5 hop 4 is the windowpane, hop 5 has the click), "a copy with one character changed let it out" all check out. Node hrefs are "#room/t" and app.js parseHash handles that form, so "Clicking a state opens the reader at the first hop that reached it" works. Room 6's "236 characters" (asked for in the brief) is the common prefix of the two hop-1 texts, split at "it crept" / "it whispered": right.

INTRO_AFTER_SEED: "Time seemed to suspend itself in this moment" is in 20260902T155321_chat json_para hop 15, the exact fixed point (hops 16 to 19 identical, cycle confirmed x3). "a door to be opened" is in 20260902T155557_chat json_page hop 5, the exact fixed point (6 to 9 identical). Both quotes are now things a run stopped on. Right.

Colophon: "in room 13 five times a quote mark inside the text field broke it" is right (see above). Hop 1 of room 12 does carry a sentence before a fenced JSON. The failed smoke test is data/index.json run 20260902T175622_anthropic_chat, 0 hops, note "workspace header missing". max_tokens is 600 for all three new runs (summary.json). Sonnet 5 ran at the provider's default sampling (steps.jsonl "sampling": "default", summary "no_sampling": true), which is what the room 14 note says.

Style: no em or en dashes, no "resonates", no "here's what" in any of the new strings. Three-part structures: see section 2.

## 1. Wrong or imprecise sentences

Format: quoted sentence; what the data shows (run, hop); proposed replacement in the same register.

### Room 15, alternating (EXTRA_ROOMS "alternating")

1. "Claude never let it settle. Every odd hop is a new opening, ten of them eleven years after something, and by hop 55 there is {{...|55|The cartographer's studio}}."
   Data (alternating_json_page): four of Claude's thirty hops continue Qwen's passage instead of opening a new one. Hop 9 "The first entry Dominic wrote was only a date and a single sentence" carries on hop 8 (Dominic, the archive room, the journal); hop 35 "The key slid into the lock ... Elias did not recognize" carries on hop 34 (Elias in the woods); hop 41 "The figure standing at the center of the lantern room had its back to her ... Dessa's lamp died" carries on hop 40 (Dessa, the lighthouse); hop 47 "The line Declan had drawn seemed to breathe on the page" carries on hop 46 (Declan, the vellum). The other 26 odd hops are openings (three of those reuse an opening's first five words: "The lighthouse had not been" at 5, 13, 31; "The library closed at nine" at 21, 45, 51; "The marina at low tide" at 25, 29, but the passages differ). The sentence is also a three-clause structure.
   Proposed: "Claude never let it settle. Twenty-six of its thirty hops are new openings; four times, at hops 9, 35, 41 and 47, it went on with Qwen's scene instead. Ten of Claude's hops are set eleven years after something, and by hop 55 there is {{alternating_json_page|json_page|55|The cartographer's studio}}."

2. "Otherwise it answered each opening with its own, and thirteen of its thirty hops begin the way the library on the map begins: ..."
   Data: apart from hops 2, 6, 16 and 50, Qwen mostly did not answer with an opening of its own; it went on with Claude's story. Seventeen of the remaining 26 even hops keep a named character from Claude's preceding hop (8 and 10 Dominic, 12 Mara, 14 Yusra, 18 Sera, 22 Maren, 24 Declan, 36 Elias, 38 Mara and Corvin, 40 and 42 Dessa, 44 Maren, 46 and 48 Declan, 52 Declan, 58 Maren, 60 Declan). Nine start something unconnected (4, 20, 26, 28, 30, 32, 34, 54, 56). The "silence" openings are usually the next scene of Claude's story, not a new story.
   Proposed: "Otherwise it mostly went on with Claude's story, keeping the character and writing the next scene, and thirteen of its thirty hops open that scene the way the library on the map opens, with The silence in the: ..." (continue as in item 8).

3. "Three more times it kept Claude's passage and added a paragraph to it, at hops 6, 16 and 50."
   Data: at hops 6, 16 and 50 Qwen's text is Claude's previous text followed by a space and new sentences, with no paragraph break (the added part contains no newline; hop 5 has paragraph breaks of its own, hops 15 and 49 do not). In the reader, which renders newlines, the addition shows as Claude's last paragraph growing longer. Added: 77 words at hop 6 ("The realization hit her with the force of a physical blow..."), 97 at hop 16 ("The silence in the room grew heavy..."), 174 at hop 50 ("The words were stark..."). "kept Claude's passage" is exact (byte prefix, 5-gram survival 0.996).
   Proposed: "Three more times it kept Claude's passage whole and wrote on past its last sentence, at hops 6, 16 and 50."

4. "No hop repeats."
   Data: no two raw outputs are identical, but hop 2's text is hop 1's text word for word, which the sentence two lines earlier concedes, and the harness itself recorded a normalized cycle of period 1 at hop 2 (summary.json transient_norm 1, period_norm 1; steps.jsonl cycle_norm 1). A reader who has just been told hop 2 is the same words will read "No hop repeats" as contradicted.
   Proposed: "After hop 2, no hop repeats."

5. "Qwen's hub keeps coming back and its sinks never do, because something else takes every other turn."
   Data: by first five words this is right (neither "the rain hammered against the" nor "the rain lashed against the" occurs in room 15; the library key occurs seven times). But MAP_NOTE has just described slot B's sink as "rain on a windowpane", and rain on a windowpane with Elias inside comes back three times in room 15, at hops 4 ("The rain against the windowpane sounded like static ... Elias stared at the manuscript"), 20 and 56, under a different first five words than slot B's "The rain lashed against the windowpane ... Elias sat hunched over a cold cup of coffee". Slot B's exit state "The rain had finally ceased" also appears once, hop 32.
   Proposed: "Qwen's hub keeps coming back and its sinks never do, by their opening words at least: the rain reaches a windowpane again at hop 4 and twice more, but never as the words that held slot B. Something else takes every other turn."

### MAP_NOTE

6. "From the library there are two doors. ... Only one path ever came back: slot B's excursion, ink and shadow and silence, then the rain again, then Mara on the platform, where a copy with one character changed let it out."
   Data (census over 20260902T155557_chat json_page and 20260902T160344_chat json_page, json_page~r): three edges leave the library, not two: to the warehouse key "the rain hammered against the" (twice: slot A hop 4, slot B hop 4), to the windowpane "the rain lashed against the" (twice: room 5 hop 4, slot B hop 14), and to "the ink did not dry" (once: slot B hop 6). Slot B's path is tide 0-1, rain 2, library 3, rain hammered 4, library 5, ink 6, shadow 7, silence was not empty 8, rain did not fall 9 (the same key as hop 2), Mara 10 and 11, rain had finally ceased 12, library 13, rain lashed 14 to 60. So two arrows come back to the library and both are slot B's: warehouse to library (hop 4 to 5) and "the rain had finally ceased" to library (hop 12 to 13); the map draws both. The excursion starts from the library at hop 5, not from a sink. Slot B's hop 4 shares the warehouse's first five words but is a different passage ("The rain hammered against the tin roof of the abandoned shack"), which the node tooltip reports as "slot B: hop 4". "ink and shadow and silence" is also a three-part structure.
   Proposed: "From the library there are three doors. One is a warehouse in the rain, where slot A stayed for fifty-six hops; slot B looked in at hop 4 and was back in the library at hop 5. Another is rain on a windowpane, where slot B stayed for forty-six, and which room 5 passed through on its way to the click. The third is slot B's excursion: ink, then shadow, then a silence that was not empty, then the same rain as hop 2, then Mara on the platform, where a copy with one character changed let it out, through a rain that had ceased and back to the library one last time. Click a state to read it."

7. "Every page-scale Qwen run on this site, drawn as one graph."
   Data: the map covers only the three lanes with the json_page rule in rooms 5 and 6 (build.py MAP_RUNS). Qwen also writes 250-word passages in room 8 (json_unexpected), room 9 (json_prev), room 13 (json_next) and, with this very rule, in every even hop of room 15 (alternating_json_page, json_page), none of which is on the map. The sentence was true before rooms 13 and 15 existed.
   Proposed: "The three Qwen lanes with the new-passage rule, drawn as one graph: room 5 and both slots of room 6."

### Room 15, wording of the thirteen

8. "thirteen of its thirty hops begin the way the library on the map begins: {{...|14|The silence in the village was not empty}}, then the library itself, the room, the valley."
   Data: thirteen even hops begin with the four words "The silence in the" (the library state's first five words are "The silence in the library"). The first of them is hop 8, "The silence in the archive room felt heavier now", which comes before the quoted village (14) and does not say "not empty". Then the library itself seven times (22, 24, 26, 30, 48, 54, 58), a reversed woodland (36), a room (40), a reading room (46), a valley (60). Hop 28 "The library's silence was not empty" is the same template with the words reordered and is not among the thirteen. The trailing "the library itself, the room, the valley" is a three-part list.
   Proposed: "... thirteen of its thirty hops open the way the library on the map opens, with The silence in the: an archive room at hop 8, then {{alternating_json_page|json_page|14|The silence in the village was not empty}}, then the library itself seven times, and after it a reversed woodland, a room, a reading room and a valley."

### Colophon

9. "What is data": "Every passage in a room is the model's output for that hop, byte for byte, taken from data/<run>.json in the loop directory (room 13 from site/runs_extra, see below)."
   Data: rooms 14 and 15 also come from site/runs_extra (sonnet5_json_page, alternating_json_page); room 14's first lane is room 11's run from data/ (20260902T175920_anthropic_chat).
   Proposed: "... taken from data/<run>.json in the loop directory (rooms 13 to 15 from site/runs_extra, see below; room 14's Sonnet 4.6 lane is room 11's run)."

10. "The harness": "Claude rooms: claude-sonnet-4-6 through the API, temperature 0."
    Data: room 14's second lane is claude-sonnet-5 with sampling "default" (summary.json no_sampling true; the room note says so, the colophon does not). Room 15 alternates claude-sonnet-4-6 and qwen3.8-27b, both recorded at T=0 (summary.json backend anthropic, backend_b llama, temp 0.0).
    Proposed: "Claude rooms: claude-sonnet-4-6 through the API, temperature 0, except the Sonnet 5 lane of room 14, which is claude-sonnet-5 at the provider's default sampling. Room 15 alternates claude-sonnet-4-6 and Qwen, both at temperature 0."

11. "Not in this site" (optional): the section names the zero-hop Claude run and the probe and watermark experiments, but site/runs_extra also holds qwen_json_mid (the middle rule, 28 hops at build time, no summary.json, so its PLACEHOLDER room is not built). If that run is meant to become a room, nothing to do; if the build ships before it finishes, add: "A Qwen run with the middle rule (site/runs_extra/qwen_json_mid) was still running when this page was built and has no room yet."

### build.py, generated colophon paragraph "Added after the bundle"

12. "Rooms 13 and up come from runs made while this site was built, with the same harness (...). They are not in data/."
    Data: room 14's Sonnet 4.6 lane is data/20260902T175920_anthropic_chat.json, room 11's run.
    Proposed: "Rooms 13 and up come from runs made while this site was built, with the same harness (site/runs_extra/<run>/steps.jsonl; the Claude runs were started by the human from a terminal with the API key). Apart from room 14's Sonnet 4.6 lane, which is room 11's run, they are not in data/. Their run ids are names, not timestamps."

### INTRO_AFTER_SEED

13. "The sixty-hop rooms are an hour each." (minor)
    Data: rooms 6, 9, 11, 12, 13, 14 and 15 have sixty-hop lanes, but room 6 is 102 copies out of 120 hops and room 14's Sonnet 5 lane is 42 copies out of 60; those are minutes, not an hour. The hour-long ones are the rooms that never stop.
    Proposed: "The rooms that never stop are an hour each."

## 2. Style lint (new text only; text inside {{...}} skipped)

- Em or en dashes: none.
- "resonates": none (it occurs inside a quoted hop of room 15, hop 40, which is data).
- "here's what" openers: none.
- Three-part parallel structures:
  - MAP_NOTE: "ink and shadow and silence" (fixed in item 6).
  - Room 15: "then the library itself, the room, the valley" (fixed in item 8).
  - Room 15: "Every odd hop is a new opening, ten of them eleven years after something, and by hop 55 there is ..." (three clauses; fixed in item 1).
  - Borderline, left to the author: "at hops 6, 16 and 50" (room 15) and "in rooms 7 and 8" are lists of data points rather than rhetorical triples. The proposal in item 5 avoids adding another ("at hop 4 and twice more").
  - Not triples, listed because a scan flags them: "on the same machine and model" (two), "a bridge and a council, a bakery, a tunnel, a reservoir" (five), "The hop numbers, token counts, stop reasons and metrics" (four), the max_tokens list in "The harness" (five), "room 5, and slots A and B of room 6" (two).

## 3. Necessary fixes, most important first

1. Room 15: "Every odd hop is a new opening" is false; hops 9, 35, 41 and 47 continue Qwen's passage (Dominic, Elias, Dessa, Declan). Say twenty-six of thirty, and name the four (item 1).
2. MAP_NOTE: "two doors" and "Only one path ever came back" contradict the map's own arrows. The library has three exits (warehouse ×2, windowpane ×2, ink ×1), and slot B came back to it twice: from the warehouse key at hop 5 (its hop 4 is a shack under the warehouse's first five words) and from "the rain had finally ceased" at hop 13. The excursion leaves from the library, not from a sink (item 6).
3. Room 15: "added a paragraph to it" at hops 6, 16 and 50: the additions (77, 97, 174 words) are run on after Claude's last sentence with no paragraph break (item 3).
4. Room 15: "Otherwise it answered each opening with its own": 17 of the other 26 Qwen hops carry Claude's character forward and write the next scene; only nine start something unconnected (item 2).
5. MAP_NOTE: "Every page-scale Qwen run on this site" is no longer true with rooms 13 and 15 (and 8, 9) off the map; say the three lanes with the new-passage rule (item 7).
6. Colophon "The harness": add Sonnet 5 at default sampling (room 14) and the alternating room (item 10).
7. Colophon "What is data": "(room 13 from site/runs_extra" should cover rooms 13 to 15 and note room 14's lane from data/ (item 9).
8. Room 15: the thirteen: the first is the archive room at hop 8, not the village; drop the closing triple (item 8).
9. Room 15: "No hop repeats" sits two sentences after "hop 2 differs from hop 1 only in how the JSON is spaced" and the harness logged a normalized period-1 cycle at hop 2; say "After hop 2, no hop repeats" (item 4).
10. Room 15: "its sinks never do" is true by first five words but rain on a windowpane with Elias comes back at hops 4, 20 and 56; qualify it (item 5).
11. build.py "Added after the bundle": "They are not in data/" is wrong for room 14's Sonnet 4.6 lane (item 12).
12. Style: remove "ink and shadow and silence" and "the library itself, the room, the valley" (covered by items 6 and 8).
13. Minor: INTRO_AFTER_SEED "The sixty-hop rooms are an hour each" (rooms 6 and 14 are mostly copies) (item 13); optional mention of the unfinished qwen_json_mid run in "Not in this site" (item 11).

Everything else in the new text checks out against the data: all of room 13's note (hops 17, 19, 24; six raw hops, five from quoting, hop 50 from the 600-token wall; sixty hops, no copy; the town list), all of room 14's note (hop 2 wall mid-sentence; "an quiet man" to "a quiet man" plus the finished sentence at hop 3; hop 7 = hop 6; clocktower at 8; lighthouse and orchard alternating 9 to 19; "quiet pride in"; hop 20 and the forty after it identical to 19; rooms 7 and 8 froze on the token limit), the quotes and counts in room 15 that are not listed above (odd/even model split, hop 2 spacing-only, hops 6/16/50 keep the passage, ten "eleven years" hops, the cartographer at 55, thirteen "The silence in the" hops), the map facts line (11 states, 129 hops, hop 1 like the seed in every run, Mara's one-character copy, ×56, ×46, ×4), the rest of MAP_NOTE (tide then rain then library in all three runs, fifty-six, forty-six, room 5 through the windowpane to the click, the one-character escape), both INTRO_AFTER_SEED quotes (fixed points of json_para hop 15 and json_page hop 5), the colophon's "five times a quote mark" and the failed smoke test, and room 6's 236 shared characters.
