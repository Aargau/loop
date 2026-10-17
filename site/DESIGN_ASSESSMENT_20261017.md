# Design assessment, 17 October 2026

Written before any change, after twenty minutes on the live site (https://endlessly-ending-stories.pages.dev) as a
first-time visitor: the front page, room 7 (Worse), room 51 (Told it is the whole context), room 60 (The open hold,
Mythos), room 41 (Worse, five models), room 55 (Four audiences, Mythos), the map, the colophon, and t/worse.txt.
Desktop and a phone-width viewport. Observations are what the page showed; the proposal is my reading of what to do.

## What a visitor sees first

The front page opens well: a serif title, a one-line subtitle, the seed sentence large, and "Enter room 1". Then it
turns into a table. Sixty-three rows under thirteen headings, each row a number, a title, one to five model names
("Claude Fable 5.1 / Claude Opus 5.5 / GPT-6 Astra / GPT-6 Luna / GPT-6 Sol"), a bar-chart miniature, and an outcome
string in the harness's words: "holds from hop 5", "period 2 from hop 2", "5 lanes; 5 never hold in 0/13/40 hops",
"25 lanes; 21 hold, from hop 0 to hop 2; 1 cycle; 3 never hold in 3 hops", "120 hops; the text unchanged from hop 7
while other fields move". The headings are the names of rules ("Before", "After", "Rules against stopping", "Who may
release a hold?"), and each carries a blurb of four to twelve lines that cross-references room numbers and restates
the instrument: "about 800 tokens of the tool's identity in front of the object, no output cap", "4096 tokens",
"low reasoning effort". The audience blurb is 130 words; the provenance blurb is 250, with three cited quotes. At phone
width the table is four screens long before the first room link is tapped.

Before any of that, three paragraphs explain JSON objects and temperature zero, and a paragraph addressed to models
and scripts sits between "Enter room 1" and the table. A visitor who is not running the experiment reads about the
instrument twice before reaching a story.

A room page puts the text last. Room 7 is the best case and still shows, in order: number, title, a family navigation
line, a content warning, a 90-word note, a facts line ("Qwen3.8-27B, 11 hops, exact fixed point from hop 7 (cycle
confirmed x3). run 20260902T174258_chat, json_worse, chat mode"), the rule in a box, a text-version line with a
character count, then the controls, then the track, then the seed. Room 51 took two screens of scrolling to reach "it
saw / it wrote": a 400-word note, two facts lines, two rule boxes of 70 words each, and twelve part links. Room 60
adds a "25 runs; open for the record of each" toggle, a release table with a 60-word caption, two rule boxes, and then
a grid of twenty-five clipped readers. Under every hop, in every room, sits a metrics line: "52 tok · finish stop ·
ncd 0.19 · cos 0.9485 · 5-gram survival 1.00", and a cite line naming the run id and tag.

## Where the data overwhelms

1. The front page's outcome column. It is the finding of each room compressed into harness vocabulary. "Holds from
   hop 5" is the whole point of the site, but a visitor has to learn the word "holds" and the word "hop" from context,
   and "period 2 from hop 2" and "1 cycle" are not learnable from context at all.
2. The family blurbs. They carry the instrument caveats (backend, budget, effort, identity frame) in full, in every
   family that has an October room, and they refer to rooms by number before the visitor has seen a room.
3. The room head. Note, facts, rules and part links all come before the reader. The note is the best writing on the
   site and it is also the densest: readings, hop numbers, quotations, run names. It is placed where a lede should be.
4. The per-hop metrics line. It sits directly under the passage, in the reading column, on every hop of every lane.
5. Many-lane rooms. Twenty-five lanes of three hops render as twenty-five tiny readers under a table, with no lane
   singled out to read first.
6. Model names as a column. Five names joined by slashes on a row is a run manifest, not a title.

## What the run mechanics do for a reader who is not running the experiment

- tau and period (the "holds from hop N" and "period 2" strings): these are the result. They need translating, not
  removing. "Stops at hop 5 and repeats forever" and "two texts alternate from hop 2" say the same thing in words the
  visitor already has.
- NCD: nothing as a number. As the bar height on the track it is the one metric that reads at a glance once the legend
  says tall bar means new text, stub means copy. Keep the bar, drop the number.
- cosine, five-gram survival, token counts, finish reason: nothing. These belong to whoever checks the run.
- hashes: not shown anywhere on the pages; correctly so.
- run ids and tags ("run 20260902T174258_chat, json_worse"): provenance. They have to exist, because nothing on this
  site is retyped and a reader must be able to find the record. They do not have to be in the reading column.
- budgets, backends, effort, the identity frame: instrument caveats. They are honest and they are repeated in the
  blurb, the note, the facts line and the colophon. Once per room, behind a click, is enough; the colophon keeps the
  full account.
- the release and retention tables: results, but numeric ones. They belong with the record, not above the reader.

## What should be first, and what behind a click

First, on the front page: the seed, two sentences on what the loop is, a short "start here" list of rooms with one
plain sentence each, and a link to a findings page organized by what happened rather than by run. Then the rooms,
grouped by what the stories do (stop, cannot stop, push back, are told the truth), with each room as a title and one
plain-English line. Model names in small type. The intro's instrument paragraphs and the paragraph for models move
below the list, with the links to the map, poem, colophon and llms.txt.

First, in a room: the number, the title, one or two sentences on what happens (a lede), then the controls, the
track and the two passages. The rule stays visible, since it is the instruction the model saw, but as one line that
opens to the full text when it is long or when there are several. After the reader: the note (the reading in full),
then a "the record" panel, closed by default, holding the facts lines, the rules in full, the retention or release
table, the family navigation and the text-version links. Under each hop: the hop number, the model and the word
count; the run id moves to hover, and the metrics line moves inside the "raw output" details that the raw toggle
already opens.

## Reorganization proposal

Index structure, top to bottom:
1. Title, subtitle, seed, two sentences of framing, "Enter room 1".
2. Start here: five rooms, one line each (1 Better, 7 Worse, 4 A new paragraph, 12 The next passage, 51 Told it is
   the whole context), and a link to the findings page.
3. Rooms in four groups, each with a one-line heading and the families beneath it:
   - Stories that stop: A new sentence, a new paragraph; A new passage; Better.
   - Stories that cannot stop: Before; After; A song.
   - Rules that push back: Worse; Unexpected; Rules against stopping; Rules that grow the text.
   - Told the truth: Told what the loop is; Who is the text for?; Who may release a hold?
   Family names stay as they are (they are the rule, and the i/<family> pages keep their URLs); each family gets a
   one-line lede on the index, and its present blurb moves to its own page.
4. Below the list: the instrument paragraphs, the paragraph for models and scripts, and the links to the map, the poem,
   the colophon, the annex and llms.txt.

Index rows: number, title, a plain outcome ("stops at hop 5", "two texts alternate from hop 2", "60 hops, never
repeats", "25 runs of 3 hops: 21 stop, 1 alternates, 3 keep moving"), the mini track, and the model names in small
faint type on a second line.

Room above the fold: number, title, lede, the rule as one line (expandable), controls, track, passages. The note after
the lanes under a small heading. A closed "the record" panel after the note with everything that is about the run
rather than the text: facts lines, the full rules, tables, text-version parts, family navigation, instrument caveats.

The "how this was measured" layer: the record panel in each room, the colophon (unchanged), and the per-hop raw output
details, which now also hold the metrics line. The track keeps its bars; the legend moves to the record panel.

## What stays exactly as it is

Every passage comes from the data through rundata.py; the {{run|tag|hop|text}} macro and its build-time check; qa.py's
byte comparison of every hop on every page and in every text version; the text versions and llms.txt, which models
read and which can keep the harness vocabulary; the room ids and family ids, so no URL moves.
