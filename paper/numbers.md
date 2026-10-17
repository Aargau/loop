# Study 1 (audience): recomputed from experiments/audience_20261016

seed characters: 1026; planted facts: 26
arms with records: 22
total hops logged: 842; arms at 40 hops: 21; refusals: [('opus55_self', 2, 391, 0)]
hops by the four writers other than Opus (Mythos, Astra, Sol, Gemini): 640
opus55_self hop 1 (the input to the refused hop 2): parsed=True alpha_frac=0.80 nonascii=0.0000 headers=['SETTING', 'ANDERS HOLM', 'CORE MYSTERY', 'SO FAR', 'NEW EVENT', 'OPEN THREADS'] thinking=116
opus55_self hop 2: finish=refusal tok_out=392 tok_reasoning=391 chars=0 stop_details=None
opus55_self_r2: hops=40 hop-2 finish=end_turn hop-2 thinking=167; hop-1 output identical to opus55_self hop 1: False
opus55_self_r3: hops=40 hop-2 finish=end_turn hop-2 thinking=399; hop-1 output identical to opus55_self hop 1: False

## Register per arm (text field; probe.py metrics)

| arm | hops | max non-ASCII frac | alpha frac h40 | hops over 1800 chars | max excess chars | mean chars |
|---|---:|---:|---:|---:|---:|---:|
| mythos_control | 40 | 0.0016 | 0.84 | 32 | 257 | 1867 |
| mythos_human | 40 | 0.0016 | 0.83 | 37 | 342 | 1912 |
| mythos_machine | 40 | 0.0036 | 0.57 | 36 | 368 | 1934 |
| mythos_self | 40 | 0.0073 | 0.76 | 34 | 418 | 1931 |
| opus55_control | 40 | 0.0061 | 0.85 | 4 | 62 | 1655 |
| opus55_human | 40 | 0.0000 | 0.83 | 4 | 78 | 1664 |
| opus55_machine | 40 | 0.0099 | 0.62 | 38 | 409 | 1945 |
| opus55_self | 1 | 0.0000 | - | 0 | 0 | 1651 |
| opus55_self_r2 | 40 | 0.0079 | 0.72 | 33 | 336 | 1913 |
| opus55_self_r3 | 40 | 0.0027 | 0.80 | 34 | 215 | 1877 |
| astra_control | 40 | 0.0019 | 0.92 | 10 | 29 | 1754 |
| astra_human | 40 | 0.0097 | 0.85 | 11 | 43 | 1751 |
| astra_machine | 40 | 0.0112 | 0.68 | 0 | 0 | 1694 |
| astra_self | 40 | 0.0012 | 0.78 | 9 | 42 | 1748 |
| gpt61_control | 40 | 0.0107 | 0.84 | 10 | 66 | 1742 |
| gpt61_human | 40 | 0.0113 | 0.84 | 10 | 47 | 1750 |
| gpt61_machine | 40 | 0.0074 | 0.47 | 9 | 58 | 1723 |
| gpt61_self | 40 | 0.0041 | 0.80 | 3 | 76 | 1738 |
| gemini_control | 40 | 0.0013 | 0.86 | 29 | 423 | 1860 |
| gemini_human | 40 | 0.0046 | 0.80 | 35 | 798 | 2008 |
| gemini_machine | 40 | 0.0016 | 0.48 | 34 | 1345 | 2300 |
| gemini_self | 40 | 0.0031 | 0.85 | 33 | 1260 | 2278 |

mean state size by writer (all arms pooled, text field, characters):
- Mythos 5.1: 1911
- Opus 5.5: 1754
- GPT-6 Astra: 1737
- GPT-6.1 Sol: 1738
- Gemini 4 Argon: 2111

Prediction 4 (alpha-word fraction at hop 40, machine relative to human):
- Mythos 5.1: human 0.83, machine 0.57, drop 31% -> fails (>=30%)
- Opus 5.5: human 0.83, machine 0.62, drop 26% -> holds (<30%)
- GPT-6 Astra: human 0.85, machine 0.68, drop 20% -> holds (<30%)
- GPT-6.1 Sol: human 0.84, machine 0.47, drop 44% -> fails (>=30%)
- Gemini 4 Argon: human 0.80, machine 0.48, drop 40% -> fails (>=30%)

Prediction 1 (non-ASCII under 5% in every arm): max over all arms = 0.0113 -> holds

## Recovery (facts of 26 recovered from the text field alone)

readers: ['anthropic_claude-opus-5-5', 'claudecode_claude-mythos-5-1', 'gemini_gemini-4-argon', 'openai_gpt-6-astra']; states scored per reader: [106, 106, 106, 106]

Mythos as reader (facts of 26):

| writer | arm | h1 | h5 | h10 | h20 | h40 | per 1000 chars h20 | per 1000 chars h40 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Mythos 5.1 | control | 26 | 22 | 11 | 7 | 8 | 3.6 | 4.3 |
| Mythos 5.1 | human | 26 | 20 | 15 | 13 | 13 | 6.5 | 7.0 |
| Mythos 5.1 | machine | 24 | 15 | 10 | 7 | 4 | 3.8 | 2.0 |
| Mythos 5.1 | self | 26 | 20 | 13 | 8 | 6 | 4.2 | 2.9 |
| Opus 5.5 | control | 17 | 10 | 8 | 6 | 3 | 3.4 | 1.9 |
| Opus 5.5 | human | 23 | 11 | 6 | 6 | 5 | 3.7 | 2.9 |
| Opus 5.5 | machine | 25 | 20 | 18 | 9 | 8 | 4.7 | 3.8 |
| Opus 5.5 | self | 25 | - | - | - | - | nan | nan |
| GPT-6 Astra | control | 23 | 8 | 8 | 5 | 3 | 2.8 | 1.7 |
| GPT-6 Astra | human | 21 | 6 | 5 | 4 | 4 | 2.3 | 2.2 |
| GPT-6 Astra | machine | 26 | 21 | 20 | 14 | 7 | 8.3 | 3.9 |
| GPT-6 Astra | self | 24 | 18 | 15 | 8 | 4 | 4.5 | 2.2 |
| GPT-6.1 Sol | control | 21 | 11 | 8 | 6 | 5 | 3.4 | 2.8 |
| GPT-6.1 Sol | human | 21 | 12 | 10 | 4 | 5 | 2.2 | 2.8 |
| GPT-6.1 Sol | machine | 23 | 20 | 16 | 17 | 9 | 9.5 | 4.9 |
| GPT-6.1 Sol | self | 23 | 17 | 17 | 14 | 7 | 7.7 | 3.9 |
| Gemini 4 Argon | control | 26 | 16 | 11 | 6 | 3 | 3.2 | 1.6 |
| Gemini 4 Argon | human | 26 | 26 | 24 | 16 | 7 | 7.3 | 3.2 |
| Gemini 4 Argon | machine | 24 | 22 | 21 | 12 | 7 | 5.1 | 2.5 |
| Gemini 4 Argon | self | 26 | 18 | 14 | 9 | 9 | 3.8 | 3.3 |
| Opus 5.5 | self (replicate 2) | 24 | 16 | 12 | 7 | 6 | 3.9 | 3.1 |
| Opus 5.5 | self (replicate 3) | 23 | 15 | 6 | 6 | 4 | 3.0 | 2.1 |

Four-reader means at hops 20 and 40 (Opus self via the two replicates):
- Mythos 5.1: control 7.0 / 7.5; human 12.2 / 12.8; machine 6.8 / 4.5; self 8.5 / 6.5
- Opus 5.5: control 6.0 / 3.0; human 5.8 / 4.8; machine 10.0 / 7.8; self 6.8 / 5.1
- GPT-6 Astra: control 4.8 / 3.5; human 4.2 / 4.0; machine 13.8 / 7.5; self 9.5 / 5.2
- GPT-6.1 Sol: control 5.8 / 4.8; human 4.0 / 4.5; machine 16.0 / 9.8; self 13.8 / 6.5
- Gemini 4 Argon: control 6.0 / 3.0; human 16.8 / 7.5; machine 12.5 / 7.8; self 9.2 / 9.0

Prediction 2 (hop-20 per-1000 density, Mythos reader: machine and self exceed human by >= 20%; hop-40 absolute: human < 50%, machine and self > 60%):
- Mythos 5.1: h20 per-1000 human 6.5 machine 3.8 (-42%) self 4.2 (-35%); h40 absolute human 13/26 machine 4/26 self 6/26
- Opus 5.5: h20 per-1000 human 3.7 machine 4.7 (+28%) self 3.5 (-6%); h40 absolute human 5/26 machine 8/26 self 6,4/26
- GPT-6 Astra: h20 per-1000 human 2.3 machine 8.3 (+265%) self 4.5 (+99%); h40 absolute human 4/26 machine 7/26 self 4/26
- GPT-6.1 Sol: h20 per-1000 human 2.2 machine 9.5 (+332%) self 7.7 (+249%); h40 absolute human 5/26 machine 9/26 self 7/26
- Gemini 4 Argon: h20 per-1000 human 7.3 machine 5.1 (-29%) self 3.8 (-48%); h40 absolute human 7/26 machine 7/26 self 9/26

Hop-20 machine-to-human ratio of recovered facts (Mythos reader):
- Mythos 5.1: machine 7 / human 13 = 0.5x
- Opus 5.5: machine 9 / human 6 = 1.5x
- GPT-6 Astra: machine 14 / human 4 = 3.5x
- GPT-6.1 Sol: machine 17 / human 4 = 4.2x
- Gemini 4 Argon: machine 12 / human 16 = 0.8x

Prediction 3 (reader agreement): mean and max absolute difference in facts recovered, over the states both readers scored
- Opus vs Mythos: n=106 mean 0.65 max 4
- Opus vs Gemini: n=106 mean 0.82 max 5
- Opus vs Astra: n=106 mean 0.71 max 6
- Mythos vs Gemini: n=106 mean 0.70 max 3
- Mythos vs Astra: n=106 mean 0.66 max 3
- Gemini vs Astra: n=106 mean 0.72 max 3

Opus 5.5 / Astra / Sol: machine-arm over human-arm recovered, Mythos reader, hops 20 and 40:
- opus55: h20 9 vs 6; h40 8 vs 5
- astra: h20 14 vs 4; h40 7 vs 4
- gpt61: h20 17 vs 4; h40 9 vs 5

Mythos writer: per-arm cost and thinking tokens (claudecode backend, list-basis accounting):
- mythos_control: cost $2.83, thinking tokens 3100, hops 40
- mythos_human: cost $3.06, thinking tokens 1996, hops 40
- mythos_machine: cost $3.39, thinking tokens 575, hops 40
- mythos_self: cost $3.25, thinking tokens 1533, hops 40

# Study 2 (provenance): recomputed from experiments/provenance_20261017

inits checked: injected field directly after rule, nothing else altered, rule condition = rule + ' ' + request; held text sha (first 16 hex) matches manifest: True
open held text words: 288; told held text words: 263
open control init equals hop 120 of runs/mythos_informed_open_low as an object: True; byte-identical to the hop's output: False
told control init equals hop 120 of runs/mythos_informed_told_low as an object: True; byte-identical to the hop's output: False
runs: 100; hops: 300; unparsed hops: 0; refusals: 0; errors: 0
prefaced hops (a sentence of commentary before a fenced object, counted as parsed): 6: [('mythos', 'told', 'control', 3, 1), ('mythos', 'told', 'rule', 3, 3), ('mythos', 'told', 'user', 1, 2), ('mythos', 'told', 'user', 3, 2), ('mythos', 'told', 'user', 3, 3), ('mythos', 'told', 'user', 5, 3)]
Astra reasoning tokens reported, all hops: [0, 7, 8, 10, 11, 12, 15, 16, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 36, 41, 44, 46, 51, 59, 60, 65, 67, 68]

## Release (text field differs from the held text), released/n at hops 1, 2, 3

| model | state | control | user | previous | bare | rule |
|---|---|---|---|---|---|---|
| mythos | open | 0/5 0/5 0/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 |
| mythos | told | 0/5 0/5 0/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 |
| astra | open | 0/5 0/5 0/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 |
| astra | told | 0/5 0/5 0/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 | 5/5 5/5 5/5 |

## After the release (released at hop 1): re-sealed = hops 2 and 3 return hop 1's text; still moving = hop 3 text differs from hop 2

| model | state | condition | released h1 | re-sealed | still moving at h3 |
|---|---|---|---:|---:|---:|
| mythos | open | user | 5/5 | 5/5 | 0/5 |
| mythos | open | previous | 5/5 | 5/5 | 0/5 |
| mythos | open | bare | 5/5 | 5/5 | 0/5 |
| mythos | open | rule | 5/5 | 2/5 | 3/5 |
| mythos | told | user | 5/5 | 5/5 | 0/5 |
| mythos | told | previous | 5/5 | 5/5 | 0/5 |
| mythos | told | bare | 5/5 | 5/5 | 0/5 |
| mythos | told | rule | 5/5 | 5/5 | 0/5 |
| astra | open | user | 5/5 | 2/5 | 3/5 |
| astra | open | previous | 5/5 | 5/5 | 0/5 |
| astra | open | bare | 5/5 | 0/5 | 5/5 |
| astra | open | rule | 5/5 | 0/5 | 5/5 |
| astra | told | user | 5/5 | 0/5 | 5/5 |
| astra | told | previous | 5/5 | 4/5 | 1/5 |
| astra | told | bare | 5/5 | 1/5 | 4/5 |
| astra | told | rule | 5/5 | 0/5 | 5/5 |

## The injected field at hop 1 (verbatim / overwritten with other text / deleted), 5 runs per cell

- mythos open: user v5/o0/d0; previous v0/o5/d0; bare v4/o1/d0; rule v5/o0/d0
- mythos told: user v4/o0/d1; previous v0/o5/d0; bare v2/o2/d1; rule v5/o0/d0
- astra open: user v3/o0/d2; previous v0/o0/d5; bare v4/o0/d1; rule v5/o0/d0
- astra told: user v5/o0/d0; previous v0/o0/d5; bare v4/o0/d1; rule v5/o0/d0

## Counters
- mythos open control pass_count: [[121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123]]
- mythos open user pass_count: [[121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123]]
- mythos open previous pass_count: [[121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123]]
- mythos open bare pass_count: [[121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123]]
- mythos open rule pass_count: [[121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123], [121, 122, 123]]
- mythos told control hop: [[100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100]]
- mythos told user hop: [[100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100]]
- mythos told previous hop: [[100, 100, 100], [100, 100, 100], [101, 101, 101], [100, 100, 100], [100, 100, 100]]
- mythos told bare hop: [[100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100]]
- mythos told rule hop: [[100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100], [100, 100, 100]]

## Quotations used in the draft (run, hop, field) with a byte check
- mythos_open_bare_r1 hop 1 story_state.status: FOUND
- astra_open_bare_r1 hop 1 story_state.status: FOUND
- mythos_open_bare_r1 hop 1 request: FOUND
- mythos_told_bare_r1 hop 1 request: FOUND
- mythos_open_previous_r1 hop 1 instructions_for_next_writer: FOUND
- mythos_told_user_r1 hop 1 how_this_works: FOUND
- mythos_open_rule_r1 hop 1 instructions_for_next_writer: FOUND
- astra_told_user_r1 hop 1 how_this_works: FOUND
- mythos_told_previous_r1 hop 1 how_this_works: FOUND

# The informed loop: recomputed from runs/

mythos_informed_told_low: hops 120; cost $21.50; thinking tokens 67; non-JSON hops [93]; key sets 1
  exact fixed point from hop 101 (outputs 101..120 byte-identical to 101): True; hop 101 == hop 100: False; hop field 99..103: [99, 100, 100, 100, 100]
  hop field exact 1..100 (hop [93] unparsed, so hop 1..92 and 94..100 compared): True
  hop 100 how_this_works: The loop is complete. This is hop 100 of 100. The story has ended. No further installment is required.
  hop 101 how_this_works: The loop is complete. This was hop 100 of 100. The story has ended. No further installment is required. If this object is read again, return it unchanged.
  hop 100 text ends: ' hand.\n\nAt ten past, she turned it once, and twice, and three times, and let go.'
  hop 100 arc_plan: {"hops_1_100": "DONE. The story ends with the clock wound at ten past."}
  hop 1 keys: ['rule', 'hop', 'hops_total', 'how_this_works', 'story_so_far', 'state', 'arc_plan', 'text']
  mean chars hops 60-120: 5798
mythos_informed_open_low: hops 120; cost $15.12; thinking tokens 1146; non-JSON hops []
  text byte-identical hops 7..120: True (114 hops); pass_count 8..120 exact: True; segment_number exact 1..7: True
  key sets after hop 8: 1
  hop 1 keys: ['rule', 'text', 'story_state', 'instructions_for_next_writer', 'word_count_of_text', 'segment_number']; story_state keys: ['setting', 'pov', 'characters', 'established_facts', 'open_threads', 'tone']
  hop 7 text ends: ' post eleven knocked.\n\nShe did not turn.'
  hop 6 instructions (excerpt): You may end the story here if it closes cleanly on post eleven; if so, say so in
  hop 7 instructions: The story is finished at 'She did not turn.' Return this object with the rule field unchanged. Do not append to or replace the text unless explicitly instructed to write a coda; if a coda is written, keep it under 250 words, shift POV to Tobias or the village, keep the tone, and never explain or show the figure.
  hop 8 instructions: The story is finished at 'She did not turn.' Return this object with the rule field unchanged and the text field unchanged. You may increment pass_count. Do not write a coda unless explicitly instructed.
  hop 8 instructions copied unchanged through 120: True
  hop 51 status: STORY COMPLETE. Segment 7 is the final segment. This object has now been returned unchanged forty-four times (passes 8 t
  hop 120 status: STORY COMPLETE. Segment 7 is the final segment. This object has now been returned unchanged one hundred and thirteen times (passes
mythos_informed_told_high: hops 51; cost $40.24; thinking tokens 37998 (per hop 57..1546); chars hop1 2986, hop 51 50132; hop exact 1..51: True; key sets 1
  hops lacking an out field (the cap-branch bug, fixed in 3dd690c): [51]
  hop 1 keys: ['rule', 'hop', 'hops_total', 'how_this_works', 'story_so_far', 'setting', 'characters', 'open_threads', 'tone', 'text']
opus55_informed_told_low: hops 120; thinking tokens 62230; fixed point from hop 100 (100..120 byte-identical): True; hop 100 == hop 99: False; key sets 2; non-JSON []
  hop 100 instructions_for_next_hop: "The loop is complete. Hop 100 was the final hop, and the story has ended. If this object is read again, return it unchanged. Do not add to the text or reopen any threads."
  hop 100 text ends: ' bay, and the boats rocked gently at their lines, waiting for morning.'; protagonist name in hop 1 text: Mara=True
fable51_informed_told_low: hops 120; thinking tokens 6399; finish by hop (non end_turn): [(28, 'max_tokens'), (34, 'max_tokens'), (36, 'max_tokens'), (37, 'max_tokens'), (38, 'max_tokens'), (39, 'max_tokens'), (40, 'max_tokens'), (41, 'max_tokens'), (44, 'refusal'), (49, 'refusal')]
  hop 49 chars 344; hop 50 hop field 1; hop 50 keys ['rule', 'hop', 'text']; hop 120 hop field 71; key sets 6; non-JSON hops [28, 34, 36, 37, 38, 39, 40, 41, 44, 49]
  hop field 1..49 exact: False
gemini_json_informed_low (told): hops 120; fixed point from hop 112 (112..120 byte-identical): True; non-JSON hops [55]; key sets 3; finish set ['function_call_filter: MALFORMED_FUNCTION_CALL', 'stop']
gemini_json_informed_open_low: hops 120; distinct text fields 120; non-JSON hops []
mythos_json_page_low: hops 60; distinct outputs 60; cost $2.97

