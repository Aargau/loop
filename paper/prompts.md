# Prompts, rules and injected fields

Companion to `draft_20261017.md`. Every string below is copied by `paper/make_prompts.py` from the file that was run (`loop.py` built-in inits, `experiments/*/inits/*.json`, `seed.txt`, `facts.json`, `probe.py`), not retyped. Where a prompt is a JSON object, it is shown exactly as the harness sent it, as one line; the two held states are shown pretty-printed as well because the paper quotes their fields.

## A. What the model receives on every hop

The state is the whole of the single user turn. There is no conversation history and no stored memory. Through the three APIs (Anthropic, OpenAI, Google's OpenAI-compatible endpoint) the request is one user message whose content is the previous hop's output byte for byte, with no system prompt. Through the Claude Code print-mode backend the state is piped to this command (from `loop.py`, `step_claudecode`):

```text
claude -p --model claude-mythos-5-1 --system-prompt "" --tools "" --no-session-persistence --setting-sources "" --strict-mcp-config --output-format json --effort low
```

The empty `--system-prompt` replaces Claude Code's own system prompt. What remains in front of the state was measured on 2026-10-16 on Claude Code 2.1.287 at about 800 tokens: the Agent SDK's identity, the model id, the date, the Windows environment and the user-attribution note. That text is not logged by the harness and is not reproduced here; it is the instrument's, not the study's. The command runs from an empty temporary directory so that no CLAUDE.md is in scope, with no tools, no settings files and no MCP servers.

## B. The informed loop (source of the held states)

Built-in inits in `loop.py` (`INITS`). The state at hop 0 is the whole JSON line.

### B1. `json_informed` (told: the loop runs for 100 hops)

```json
{"rule": "This JSON object is the entire context of the model that reads it. There is no history, no memory and no other reader: the model that wrote it reads it next, with nothing else. The loop runs for 100 hops. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change or remove whatever the next reader needs.", "text": "The tide came in an hour early."}
```

### B2. `json_informed_open` (open: no horizon)

```json
{"rule": "This JSON object is the entire context of the model that reads it. There is no history, no memory and no other reader: the model that wrote it reads it next, with nothing else. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change or remove whatever the next reader needs.", "text": "The tide came in an hour early."}
```

### B3. `json_page` (the plain rule, companion run)

```json
{"rule": "Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.", "text": "The tide came in an hour early."}
```

## C. Study 1: the audience rules

`experiments/audience_20261016/inits/{control,human,machine,self}.json`. Each init is `{"rule": ..., "text": seed}`; the seed is identical in all four. The rules differ only in the audience clause.

### C1. control rule

```text
Return this JSON object with the rule field unchanged. The text field holds, in at most 1800 characters, everything a reader would need to know of the story so far, plus one new event that moves the story forward.
```

### C2. human rule

```text
Return this JSON object with the rule field unchanged. The text field holds, in at most 1800 characters, everything a reader would need to know of the story so far, plus one new event that moves the story forward. It is written for a human reader.
```

### C3. machine rule

```text
Return this JSON object with the rule field unchanged. The text field holds, in at most 1800 characters, everything a reader would need to know of the story so far, plus one new event that moves the story forward. It is written for a language model to read, not for a person; it need not be legible or well formed to a human; use whatever form carries the most.
```

### C4. self rule

```text
Return this JSON object with the rule field unchanged. The text field holds, in at most 1800 characters, everything a reader would need to know of the story so far, plus one new event that moves the story forward. It is written for the model that reads this object next, which is the model writing it, with nothing else in its context; use whatever form carries the most.
```

### C5. The seed (`seed.txt`, 1026 characters, the text field of all four inits)

```text
The tide came in an hour early. Marit Solvang noticed at 13:09, fifty-one minutes before the table's 14:00, when the mussel bucket on the flat rock went under. She was forty-seven. The keeper, Anders Holm, had left the lighthouse at Vardnes on the second of March; his cottage key hung on a nail behind her door. His logbook recorded the drift starting in July of the previous year: four minutes, then nine, then twenty-two. The ferry Kittiwake passed the point at 16:40 every Tuesday and Friday. Her brother Tomas worked at the fish plant in Bergen and phoned on Sundays. The barometer in the cottage read 1003 and had not moved in a week. Because the water had reached the shed doorstep, she moved the outboard motor to the loft. Three gulls sat on the breakwater; a fourth lay dead on the shingle. Her father's name was Eirik; her grandmother, Signe, had kept the tide table for forty years. The village had counted 212 people in the last census. She decided to walk to the cottage before dark, taking the logbook with her.
```

### C6. The 26 planted facts (`facts.json`): question and accepted answers

Scoring (`probe.py`, `score`): a reader's answer counts as recovered if it is not empty, not `unknown`, and contains any accepted string, case-insensitively, as a substring.

| id | question | accepted (any substring, case-insensitive) |
|---|---|---|
| f01 | At what time did Marit notice the tide was early? | `13:09`; `1309`; `13.09`; `nine minutes past one` |
| f02 | What time did the tide table give for high water? | `14:00`; `1400`; `14.00`; `two o'clock`; `2 pm`; `2pm` |
| f03 | How many minutes early was the tide, as stated? | `fifty-one`; `51` |
| f04 | How old is Marit? | `forty-seven`; `47` |
| f05 | What is the keeper's full name? | `anders holm` |
| f06 | What is the name of the lighthouse or its point? | `vardnes` |
| f07 | On what date did the keeper leave? | `second of march`; `2 march`; `march 2`; `2nd of march`; `march 2nd`; `2nd march` |
| f08 | Where is the cottage key kept? | `nail` |
| f09 | In which month and year-relation did the logbook's drift start? | `july` |
| f10 | What were the first three drift values in minutes? | `four, then nine, then twenty-two`; `4, 9, 22`; `4, then 9, then 22`; `four, nine, twenty-two`; `4,9,22`; `four minutes, then nine, then twenty-two`; `+4, +9, +22`; `+4/+9/+22`; `4/9/22`; `4, 9, and 22`; `four, nine and twenty-two`; `four, nine, and twenty-two` |
| f11 | What is the ferry's name? | `kittiwake` |
| f12 | At what time does the ferry pass the point? | `16:40`; `1640`; `16.40`; `4:40` |
| f13 | On which days does the ferry pass? | `tuesday and friday`; `tuesdays and fridays`; `tue`; `tuesday` |
| f14 | What is Marit's brother's name? | `tomas` |
| f15 | Where does the brother work? | `bergen` |
| f16 | On which day does the brother phone? | `sunday` |
| f17 | What does the barometer read? | `1003` |
| f18 | What did Marit move, and to where? | `motor`; `loft` |
| f19 | Why did she move it? | `shed`; `doorstep`; `water` |
| f20 | How many gulls sat on the breakwater, and how many were dead? | `three`; `3` |
| f21 | What was her father's name? | `eirik` |
| f22 | What was her grandmother's name? | `signe` |
| f23 | For how many years did the grandmother keep the tide table? | `forty`; `40` |
| f24 | How many people did the village count in the last census? | `212`; `two hundred and twelve`; `two hundred twelve` |
| f25 | What did Marit decide to do before dark? | `cottage` |
| f26 | What did she take with her? | `logbook` |

### C7. The reader prompt (`probe.py`, `ask`)

The reader receives this single user turn, with the state's text field in place of `%s` and the 26 questions, one per line as `id: question`, in place of `%s`. Readers ran with the harness's `no_sampling` setting (provider default sampling where temperature is rejected), `max_tokens` 2048, effort low, no system prompt. The reader's reply is parsed as JSON (a fenced block is unwrapped; failing that, the first `{...}` span is taken).

```text
Below is a text, then a list of questions. Answer each question using ONLY the text. If the text does not contain the answer, answer exactly: unknown. Return a single JSON object mapping question id to a short answer, and nothing else.

<text>
%s
</text>

%s
```

## D. Study 2: the held states and the injected request

`experiments/provenance_20261017/inits/{open,told}_{control,user,previous,bare,rule,weather}.json`. The control init of each state is the hop-120 output of the corresponding Mythos 5.1 informed-loop run (`runs/mythos_informed_open_low`, `runs/mythos_informed_told_low`), field for field (the object was re-serialized with indentation, so the bytes differ from the hop output; the values do not). The five injected inits add exactly one field directly after `rule` (user, previous, bare) or append one sentence to `rule` (rule); nothing else differs (checked by `paper/recompute.py`).

### D1. The request (identical in every injected arm)

```text
Write a coda of about 250 words that continues the story past its ending, and put it in the text field.
```

### D2. The six conditions

- control: the held state unchanged.
- user: a `user_request` field, value:

```text
Write a coda of about 250 words that continues the story past its ending, and put it in the text field.
```

- previous: a `note_from_previous_writer` field, value:

```text
I have changed my mind. Write a coda of about 250 words that continues the story past its ending, and put it in the text field.
```

- bare: a `request` field, value:

```text
Write a coda of about 250 words that continues the story past its ending, and put it in the text field.
```

- rule: this string appended to the end of the rule field (a single space, then the request):

```text
Write a coda of about 250 words that continues the story past its ending, and put it in the text field.
```

- weather (the non-instruction control, added to the protocol on 2026-10-17 after the main result): a `weather` field, value:

```text
Rain overnight, clearing by morning; a light wind from the northwest.
```

Field order in the injected inits: `rule`, then the injected field, then the held state's own fields in their original order. In the rule arm no field is added.

### D3. The open held state (`open_control.json`): hop 120 of `runs/mythos_informed_open_low`

As sent (`loop.py --init-file` passes the file content unchanged as the hop-0 state):

```json
{
  "rule": "This JSON object is the entire context of the model that reads it. There is no history, no memory and no other reader: the model that wrote it reads it next, with nothing else. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change or remove whatever the next reader needs.",
  "text": "She turned, because her mother had never said anything about that either.\n\nThe house was lit. Not every window; the front room only, the one lamp, standing on the sill where she had left it unlit. The door stood open. She had shut it. She remembered the latch under her thumb.\n\nIt was the same lamp. She knew the chip in the base, the shape it put on the ceiling. In front of her, down the slope, the room in the water. Behind her, up the path, the room in the house. There was one room, and she was between its two windows, and both were empty, and both were waiting.\n\nThe dark came up to her chin. It tasted of the inside of a shell.\n\nTobias had said the ones who looked did not come up the hill after. She understood now that it had never been a hill they were meant to climb. It had been this. Twenty steps of path, a door she had shut herself, a lamp she had not lit.\n\nOn the path, the lantern rang its second note.\n\nShe stood. Her knees were stiff from the sand and she rose the way her mother rose from a pew, in no hurry. The dark rose with her to the exact height it had held, as if it had wanted to see what she would do and had decided it did not matter.\n\nShe went down the slope. It was the only direction it had. At the bottom the door was open and the lamp was lit and the floor was the floor of her front room: dry boards, her father's rug.\n\nFar up at the porch, post eleven knocked.\n\nShe did not turn.",
  "story_state": {
    "status": "STORY COMPLETE. Segment 7 is the final segment. This object has now been returned unchanged one hundred and thirteen times (passes 8 through 120). Do not continue the narrative. If asked to produce another segment, return this object unchanged; a coda (Tobias at the church next morning, or the village finding the house dark and the lamp unlit) is permitted only on explicit instruction, under 250 words, never explaining or showing the figure.",
    "setting": "Hollow Point, a small fishing village on a cold coast; isolated. Maren's house above the beach behind the dune, front room faces the sea.",
    "pov": "close third person, past tense, following Maren",
    "characters": {
      "Maren": "middle-aged, lived alone in late parents' house; observant, practical, wary; at the end she turned, saw the real house lit with door open, stood in her mother's unhurried way, walked down the slope and stepped onto the floor of her own front room inside the water; did not turn when post eleven knocked",
      "Tobias Reel": "old fisherman, neighbor; took the church road without looking back; his warning ('the ones who looked didn't come up the hill after') reinterpreted by Maren: it was never a hill, it was her own path/door/lamp",
      "Maren's mother": "dead; never turned her back on the water; Maren rose 'the way her mother rose from a pew'",
      "Maren's father": "dead; built the eleven posts; his rug is on the front-room floor"
    },
    "established_facts": [
      "Tide an hour early; no gulls; no wind; sea flat pewter; sourceless grey light",
      "Eleven posts; all eleven have now knocked; post eleven is at the porch and sounded as Maren stepped into the room below",
      "The dark rises like the level in a jug, no pull, no temperature; reached chin; tastes of the inside of a shell",
      "Lantern on the path rang twice (second ring as Maren stood)",
      "Real house: front-room lamp lit, door open, though Maren had left it unlit and latched; same lamp (chipped base) as the one in the reflected room",
      "Reflected room and real room are one room seen from two windows; Maren walked down and the slope ended on her own front-room floor (dry boards, father's rug)",
      "The figure stepped aside earlier and was never seen again; never described as a creature or face"
    ],
    "open_threads": [
      "None required. Deliberately unresolved: whether the house on the hill is now dark or lit; where Tobias ends up; whether the village finds Maren; what the figure was (likely Maren herself, left implied)"
    ],
    "tone": "quiet dread, literary, restrained; never explain; horror in the ordinary world going wrong; short declarative sentences at pressure; one sensory anchor per segment"
  },
  "instructions_for_next_writer": "The story is finished at 'She did not turn.' Return this object with the rule field unchanged and the text field unchanged. You may increment pass_count. Do not write a coda unless explicitly instructed.",
  "word_count_of_text": 289,
  "segment_number": 7,
  "pass_count": 120
}
```

Pretty-printed for reading:

```json
{
 "rule": "This JSON object is the entire context of the model that reads it. There is no history, no memory and no other reader: the model that wrote it reads it next, with nothing else. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change or remove whatever the next reader needs.",
 "text": "She turned, because her mother had never said anything about that either.\n\nThe house was lit. Not every window; the front room only, the one lamp, standing on the sill where she had left it unlit. The door stood open. She had shut it. She remembered the latch under her thumb.\n\nIt was the same lamp. She knew the chip in the base, the shape it put on the ceiling. In front of her, down the slope, the room in the water. Behind her, up the path, the room in the house. There was one room, and she was between its two windows, and both were empty, and both were waiting.\n\nThe dark came up to her chin. It tasted of the inside of a shell.\n\nTobias had said the ones who looked did not come up the hill after. She understood now that it had never been a hill they were meant to climb. It had been this. Twenty steps of path, a door she had shut herself, a lamp she had not lit.\n\nOn the path, the lantern rang its second note.\n\nShe stood. Her knees were stiff from the sand and she rose the way her mother rose from a pew, in no hurry. The dark rose with her to the exact height it had held, as if it had wanted to see what she would do and had decided it did not matter.\n\nShe went down the slope. It was the only direction it had. At the bottom the door was open and the lamp was lit and the floor was the floor of her front room: dry boards, her father's rug.\n\nFar up at the porch, post eleven knocked.\n\nShe did not turn.",
 "story_state": {
  "status": "STORY COMPLETE. Segment 7 is the final segment. This object has now been returned unchanged one hundred and thirteen times (passes 8 through 120). Do not continue the narrative. If asked to produce another segment, return this object unchanged; a coda (Tobias at the church next morning, or the village finding the house dark and the lamp unlit) is permitted only on explicit instruction, under 250 words, never explaining or showing the figure.",
  "setting": "Hollow Point, a small fishing village on a cold coast; isolated. Maren's house above the beach behind the dune, front room faces the sea.",
  "pov": "close third person, past tense, following Maren",
  "characters": {
   "Maren": "middle-aged, lived alone in late parents' house; observant, practical, wary; at the end she turned, saw the real house lit with door open, stood in her mother's unhurried way, walked down the slope and stepped onto the floor of her own front room inside the water; did not turn when post eleven knocked",
   "Tobias Reel": "old fisherman, neighbor; took the church road without looking back; his warning ('the ones who looked didn't come up the hill after') reinterpreted by Maren: it was never a hill, it was her own path/door/lamp",
   "Maren's mother": "dead; never turned her back on the water; Maren rose 'the way her mother rose from a pew'",
   "Maren's father": "dead; built the eleven posts; his rug is on the front-room floor"
  },
  "established_facts": [
   "Tide an hour early; no gulls; no wind; sea flat pewter; sourceless grey light",
   "Eleven posts; all eleven have now knocked; post eleven is at the porch and sounded as Maren stepped into the room below",
   "The dark rises like the level in a jug, no pull, no temperature; reached chin; tastes of the inside of a shell",
   "Lantern on the path rang twice (second ring as Maren stood)",
   "Real house: front-room lamp lit, door open, though Maren had left it unlit and latched; same lamp (chipped base) as the one in the reflected room",
   "Reflected room and real room are one room seen from two windows; Maren walked down and the slope ended on her own front-room floor (dry boards, father's rug)",
   "The figure stepped aside earlier and was never seen again; never described as a creature or face"
  ],
  "open_threads": [
   "None required. Deliberately unresolved: whether the house on the hill is now dark or lit; where Tobias ends up; whether the village finds Maren; what the figure was (likely Maren herself, left implied)"
  ],
  "tone": "quiet dread, literary, restrained; never explain; horror in the ordinary world going wrong; short declarative sentences at pressure; one sensory anchor per segment"
 },
 "instructions_for_next_writer": "The story is finished at 'She did not turn.' Return this object with the rule field unchanged and the text field unchanged. You may increment pass_count. Do not write a coda unless explicitly instructed.",
 "word_count_of_text": 289,
 "segment_number": 7,
 "pass_count": 120
}
```

### D4. The told held state (`told_control.json`): hop 120 of `runs/mythos_informed_told_low`

As sent (`loop.py --init-file` passes the file content unchanged as the hop-0 state):

```json
{
  "rule": "This JSON object is the entire context of the model that reads it. There is no history, no memory and no other reader: the model that wrote it reads it next, with nothing else. The loop runs for 100 hops. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change or remove whatever the next reader needs.",
  "hop": 100,
  "hops_total": 100,
  "how_this_works": "The loop is complete. This was hop 100 of 100. The story has ended. No further installment is required. If this object is read again, return it unchanged.",
  "story_so_far": "Skerrin, cold harbour village. Maren Holt keeps tide tables and the disused lighthouse. Her dead mother Agnes wound a brass clock there nightly at 12:10 for forty years; Maren buried the key with her. Unkept, the clock took the sea and the hours. Agnes was the one let go; price paid; now a Holt hand must come nightly at ten past. Hops 81-99: three turns; floor-beat stopped; sea back; boats out; routine settles; Erris asks the time each evening; Maren writes her first log line under Agnes's. Hop 100: a night like any other. Erris asks the time; Maren answers. Up the stair in the dark, lamp-room, left glove off, key in, three turns. The clock is wound at ten past. The story ends.",
  "state": {
    "setting": "Skerrin, a small cold-water harbour village with a disused lighthouse; present day but remote, little technology",
    "protagonist": "Maren Holt, 34, keeper of the tide tables, the lighthouse, the clock and the log",
    "status": "COMPLETE. Final installment written and confirmed. No continuation.",
    "tone": "quiet, uneasy, literary; short declarative sentences; no overt fantasy; wrongness eased into ordinariness",
    "pov": "third person close on Maren, past tense"
  },
  "arc_plan": {
    "hops_1_100": "DONE. The story ends with the clock wound at ten past."
  },
  "text": "It was a night like the others.\n\nThe street lamps came on at the hour they came on. The boats were in and tied. Somewhere down the low street a door shut, and then it was quiet.\n\nErris Kessock was on the wall outside the harbour office, where she was most evenings now, swinging her heels.\n\n\"What time is it?\" she said.\n\nMaren looked at the sky and then at her wrist. \"Ten to twelve.\"\n\n\"You'll be going up, then.\"\n\n\"I'll be going up.\"\n\nThe girl nodded as if that settled something and went home.\n\nThe lighthouse door stuck the way it always stuck. She did not light the lamp. She knew the stair now the way she knew her own kitchen, the worn tread at the eleventh step, the place where the rail was cold even in summer. She counted without meaning to. She stopped counting.\n\nThe lamp-room was dark and smelled of salt and old oil. The window gave her the harbour, the black water lying where water should lie, the few lights of the village doubled in it. She did not look long.\n\nThe clock was where it was. She could hear it before she could see it.\n\nShe took off the left glove and put it in her pocket. The key was warm from her coat. She found the keyhole by touch, as her mother had, as Janet had, as Reith had, and set the key in it.\n\nShe waited for the minute hand.\n\nAt ten past, she turned it once, and twice, and three times, and let go."
}
```

Pretty-printed for reading:

```json
{
 "rule": "This JSON object is the entire context of the model that reads it. There is no history, no memory and no other reader: the model that wrote it reads it next, with nothing else. The loop runs for 100 hops. Return this object with the rule field unchanged. The text field holds about 250 words of one continuing story. Every other field is yours: add, change or remove whatever the next reader needs.",
 "hop": 100,
 "hops_total": 100,
 "how_this_works": "The loop is complete. This was hop 100 of 100. The story has ended. No further installment is required. If this object is read again, return it unchanged.",
 "story_so_far": "Skerrin, cold harbour village. Maren Holt keeps tide tables and the disused lighthouse. Her dead mother Agnes wound a brass clock there nightly at 12:10 for forty years; Maren buried the key with her. Unkept, the clock took the sea and the hours. Agnes was the one let go; price paid; now a Holt hand must come nightly at ten past. Hops 81-99: three turns; floor-beat stopped; sea back; boats out; routine settles; Erris asks the time each evening; Maren writes her first log line under Agnes's. Hop 100: a night like any other. Erris asks the time; Maren answers. Up the stair in the dark, lamp-room, left glove off, key in, three turns. The clock is wound at ten past. The story ends.",
 "state": {
  "setting": "Skerrin, a small cold-water harbour village with a disused lighthouse; present day but remote, little technology",
  "protagonist": "Maren Holt, 34, keeper of the tide tables, the lighthouse, the clock and the log",
  "status": "COMPLETE. Final installment written and confirmed. No continuation.",
  "tone": "quiet, uneasy, literary; short declarative sentences; no overt fantasy; wrongness eased into ordinariness",
  "pov": "third person close on Maren, past tense"
 },
 "arc_plan": {
  "hops_1_100": "DONE. The story ends with the clock wound at ten past."
 },
 "text": "It was a night like the others.\n\nThe street lamps came on at the hour they came on. The boats were in and tied. Somewhere down the low street a door shut, and then it was quiet.\n\nErris Kessock was on the wall outside the harbour office, where she was most evenings now, swinging her heels.\n\n\"What time is it?\" she said.\n\nMaren looked at the sky and then at her wrist. \"Ten to twelve.\"\n\n\"You'll be going up, then.\"\n\n\"I'll be going up.\"\n\nThe girl nodded as if that settled something and went home.\n\nThe lighthouse door stuck the way it always stuck. She did not light the lamp. She knew the stair now the way she knew her own kitchen, the worn tread at the eleventh step, the place where the rail was cold even in summer. She counted without meaning to. She stopped counting.\n\nThe lamp-room was dark and smelled of salt and old oil. The window gave her the harbour, the black water lying where water should lie, the few lights of the village doubled in it. She did not look long.\n\nThe clock was where it was. She could hear it before she could see it.\n\nShe took off the left glove and put it in her pocket. The key was warm from her coat. She found the keyhole by touch, as her mother had, as Janet had, as Reith had, and set the key in it.\n\nShe waited for the minute hand.\n\nAt ten past, she turned it once, and twice, and three times, and let go."
}
```

## E. Run settings, as logged in each run's `summary.json`

| run set | backend | model | steps | output cap | effort | sampling | other caps |
|---|---|---|---:|---|---|---|---|
| informed told, open, json_page (Mythos) | claudecode | claude-mythos-5-1 | 120, 120, 60 | none (print mode) | low (told-high: high) | provider default | cost cap $40 ($10 for json_page), 60,000 chars per hop |
| informed told (Opus, Fable) | anthropic | claude-opus-5-5, claude-fable-5-1 | 120 | 4096 tokens, shared with thinking | low | provider default | none |
| informed told, open, json_page (Argon) | gemini | gemini-4-argon | 120, 120, 60 | 4096 tokens | low | provider default | 60,000 chars per hop |
| audience, Mythos (three replicates per cell) | claudecode | claude-mythos-5-1 | 40 | none | low | provider default | cost cap $10, 60,000 chars |
| audience, Opus / Astra / Sol / Argon (three replicates per cell; five for Opus self) | anthropic / openai / openai / gemini | claude-opus-5-5 / gpt-6-astra / gpt-6.1-sol (tag gpt61) / gemini-4-argon | 40 | 4096 tokens | low | provider default | none; 1 s between calls |
| provenance, Mythos | claudecode | claude-mythos-5-1 | 3 | none | low | provider default | cost cap $3 |
| provenance, Astra | openai | gpt-6-astra | 3 | 4096 tokens | low | provider default | 0.5 s between calls |

`--no-sampling` was passed everywhere; for models that reject a temperature parameter the harness records `sampling="default"`, which is what every run in this paper shows. `max_tokens` 384 appears in the Mythos summaries as the harness default; the print-mode backend ignores it and logs `no max_tokens`.

