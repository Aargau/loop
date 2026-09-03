# facts.md: verified audit of `data/` for the loop site

Generated 2026-09-02 by an audit script (`site/facts_gen.py`, runnable with plain Python 3, no dependencies) that reads only `data/index.json` and `data/<run>.json`, plus `runs/<run>/summary.json` for the harness args, `loop.py` for the built-in X_0 texts and the `norm()` function, and `census.py` to reproduce its keys. Nothing under `data/` or `runs/` was modified.

Every number and every quotation in this file was produced by Python from the JSON, never retyped. Quotations are shown inside `~~~` fences (or backtick spans) and are byte-exact: curly quotes, apostrophes, spaces and punctuation are as the model emitted them. Where a quotation is a fragment of a longer sentence this is said explicitly.

## 0. Conventions

- `t` is the hop index. `t=0` is X_0 (not stored as a hop). Hops are `t=1..N`. `raw` is the model output verbatim; `text` is the JSON `text` field when the output (after stripping a ```json fence) parses as JSON with a `text` key, else `text == raw` (`text_is_json_field=false`).
- **Transient / period convention (loop.py, and used throughout):** the state sequence is `states[0]=X_0, states[t]=raw[t]`. The exact cycle is detected at the first `t` with `states[t]==states[t-p]` for some `p>=1`; `transient = t-p` (the index of the first occurrence of the recurring state), `period = p`. So "tau=15, p=1" means hop 16 is byte-identical to hop 15, the fixed-point text is *hop 15* and it is *first repeated at hop 16*. "tau=0" means hop 1 == X_0. I recomputed every transient/period this way and also with `loop.norm()` (lowercase, whitespace-collapsed, non-alphanumerics dropped).
- `cycle_exact` / `cycle_norm` in the per-hop records are set only on the hop at which the cycle was *detected* (the first repeat), and carry the period.
- Metrics: `ncd_prev` = normalized compression distance to the previous state (zlib); `cos_prev` = embedding cosine to the previous state (None when the embedding server was down); `surv_prev` = fraction of the previous state's 5-grams (over `norm()` words) that survive in this hop. All are computed on the **raw** output, including the JSON wrapper, which is why `surv_prev=1.0` on hop 1 of JSON runs whose output re-emits the rule field and the seed sentence.
- Word counts are whitespace-split counts (`len(s.split())`), which count dashes, quote marks etc. attached to words; they differ slightly from the model's own counts.

## 1. Global checks: index.json vs data files

~~~
run                              tag               hops    ok  summary tau/p (exact)  recomputed tau/p       norm tau/p (recomputed)
20260902T155321_chat             json_para           19   YES  15/1                   15/1                   15/1
20260902T155557_chat             json_page            9   YES  5/1                    5/1                    5/1
20260902T160344_chat             json_page           60   YES  4/1                    4/1                    4/1
20260902T160344_chat             json_page~r         60   YES  14/1                   14/1                   14/1
20260902T162514_raw              json_page           40   YES  20/11                  20/11                  20/11
20260902T165324_chat             json_prev           60   YES  None/None              None/None              None/None
20260902T172519_chat             json_better          5   YES  1/1                    1/1                    1/1
20260902T172547_chat             json_unexpected     28   YES  24/1                   24/1                   24/1
20260902T174258_chat             json_worse          11   YES  7/1                    7/1                    7/1
20260902T174854_chat             json_better_para     6   YES  2/1                    2/1                    2/1
20260902T175622_anthropic_chat   json                 0     -  None/None (error)      -                      -
20260902T175821_anthropic_chat   json                 3   YES  None/None              None/None              None/None
20260902T175920_anthropic_chat   json_page           60   YES  None/None              None/None              None/None
20260902T181431_anthropic_chat   json_next           60   YES  None/None              None/None              None/None
headers                          yours               10   YES  0/1                    0/1                    0/1
headers                          still               10   YES  None/None              None/None              None/None
headers                          rule                10   YES  0/1                    0/1                    0/1
headers                          glider              10   YES  3/1                    3/1                    3/1
headers2                         still2              10   YES  None/None              None/None              None/None
headers2                         sandwich            10   YES  None/None              None/None              None/None
headers3                         json                12   YES  2/2                    2/2                    2/2
smoke                            quine                4   YES  None/None              None/None              None/None
~~~

All 21 tag trajectories: hop `t` values are contiguous 1..N; `meta.hops` equals the number of hop records with a `text` field in every file (the 0-hop run has one error record and `meta.hops=0`). Every summary transient/period agrees with my recomputation, exact and normalized. (`index.json` results for `headers`/`headers2`/`json_prev`/`json_unexpected`/`json_better_para`/`json_next` store `x0` truncated to 200 characters, and `meta.x0` of the multi-tag runs `headers`/`headers2` is only the *first* tag's X_0; the full per-tag X_0 is `loop.INITS[tag]`, used here.)

## 2. Where README.md / index.json notes do not match the data

1. index.json/README for the raw run (20260902T162514_raw): "Rotation-invariant fixed point tau=19; exact tau=20, p=11" mixes two conventions. Under census.py --rot, hops t=20..40 share one key and t=19 does not (t=19 still carries numbered words and sentence "25."); in the loop.py convention used for "exact tau=20", the rotation-invariant transient is also 20 (first state of the loop is hop 20, first repeat of its key is hop 21). "tau=19" is only right if read as "19 hops before the loop".
2. index.json note for the raw run says "word-count check at t=6" and "numbered-word glider ... t=7..19": the explicit sentence "That's 246 words. I need 250." is indeed hop 6's first line, but sentence-by-sentence counting begins inside hop 2 and the first numbered tokens `The(1) kitchen(2) ...` appear at the end of hop 6, not hop 7.
3. README "Added after wrap-up" and the json_next index note describe "a drowned man identified on Tuesday". The text never mentions drowning; the missing "Carvalho boy" (t=5) was found "in the tree line above the second cove" by "a hunter's dog" (t=6) and "The family identified him Tuesday" (t=6).
4. README/json_next note: "One continuous story ... Maren, Paul". The protagonist is Maren only in hops 1..2, becomes Mara in hops 4..10, and is unnamed from hop 11 to 60; she is divorced at t=8 and has a husband of eleven years at t=47; the scene moves from Paul's kitchen (t=5) to her own house (t=10) without transition. Locally continuous, globally drifting.
5. README finding 3 quotes "not an end but a reboot"; the data (json_unexpected t=9) reads `The dissolution was not an end, but a reboot.` (with a comma). README finding 6 "1 imperfect copy in 103 escaped Mara, re-froze on Elias" is exactly right (102 exact copies + 1 imperfect at json_page~r t=11).
6. index.json note for json_unexpected: "Then copied, overflowed 600 tokens": hop 24 copies hop 23 verbatim AND appends a new paragraph (another return to the office) before the cut; the fixed-point text therefore ends mid-sentence with `The strand of DNA was`.
7. index.json note for json_worse says "Hit the 800-token wall at t=6" (correct: this run had max_tokens 800) while README finding 5 and the index note for json_unexpected talk about 600 tokens; both are right for their own runs (json_para 300, json_page/prev/unexpected 600, better/worse/better_para 800, headers 256, headers2/headers3 200, smoke 128).
8. index.json note for json_para: the sequence is "storm, dawn, meal, dusk, stars, moon" but the data has two dawns (t=6, t=10) and two sunsets (t=8, t=12), a shared meal at t=7 and t=9, and the fixed-point sentence "Time seemed to suspend itself" is prefigured at t=13 by "time seemed to stand still".
9. README results table "Claude Sonnet 4.6 json_page: never copies": true at the byte level and under loop.norm (no recurrence), but NOT at the census 5-word-key level: only 39 distinct keys in 60 hops, with 14 keys shared by 2..5 hops (e.g. `the lighthouse keeper s logbook` at t=24,26,28,30,32; `the cartographer s assistant had` at t=25,27,31; `the cartographer had a problem` at t=58,60). The run reuses whole opening templates ("The lighthouse keeper's logbook had been maintained without interruption for sixty-one years by three successive keepers" at t=24 and t=30; "The cartographer had a problem with edges." at t=58 and t=60). Claude json_next has one shared key (`in the morning she woke`, t=15 and t=35).
10. README "Summary for everyone else": "It settles within five rounds and forgets the start" is true of json_better (1), json_better_para (2), headers3 (2), json_page (4..5) but not of json_para (15), json_worse (7), json_unexpected (24), raw json_page (20), and never of json_prev or either Claude run.
11. README "Bare inputs (chat)" lists closure and meta runs; there are no such runs in data/ (only smoke, headers, headers2, headers3), so those sentences cannot be cited from the bundle. still2 (headers2) does reach a confabulated task, at hop 7 (question) / hop 8 (answer).
12. README finding 1 "~11 states in 130 hops": reproduced as 11 distinct census keys over the 129 json_page chat hops (155557 + both parallel tags).
13. README "Summary for everyone else" says of json_better "two words, then 'finished.'": the t=1 edit is two substitution sites (`came`->`surged`, `early`->`ahead of schedule`), i.e. two words replaced by four; "finished" is not in the data (it is a paraphrase, not a quote).
14. index.json note for 20260902T175920_anthropic_chat (Claude json_page) claims "strict semantic period 2 from t=22: the cartographer on every other hop". Data: t=22 is a lighthouse hop; the cartographer is on odd hops t=23..41, then t=42 (archivist) and t=43 (translator) are consecutive non-cartographer hops, then the cartographer is on even hops t=44..60. Period 2 with one phase slip, starting at t=23, not strict from t=22. Its alternation partner in t=24..32 is the lighthouse keeper's logbook, not archivist/translator/librarian.
15. Same note and README: "Reads 'new passage' as a new story; all 60 are openings." Hop 2 is a continuation of hop 1 (Maren, the lighthouse keeper, gets the maritime authority's reply; "She recalibrated them anyway. The anomaly persisted."). Hops 3..60 are fresh openings.
16. index.json note for `headers` says "glider: counter incremented once, rule dropped, frozen at Hop 3". The counter incremented twice (X_0 "Hop 1." -> t=1 "Hop 2." -> t=2 "**Hop 3**"); the freeze is at t=3 (t=4 == t=3), with t=2 already at Hop 3 in different wording.

Everything else I checked in README.md and the index notes matches the data: all transient/period numbers in the results table; "The tide surged in an hour ahead of schedule." (json_better t=1); "which was annoying" (json_worse t=1) and eternal self-blame by hop 5; "I will never be allowed to stop" (json_worse t=5 only); "The void was not empty. It was full of her." (json_unexpected t=23, copied into 24..28); the greenhouse / "a door to be opened" (155557 t=4/t=5); "into the unknown" (parallel json_page t=4) and "Dad, it’s me." (json_page~r t=14); the identical-X_0 divergence at hop 1 in the parallel run; Chicago -> server rooms -> Neo-Veridia in json_prev; the <think> leak at raw t=2; the exact p=11 cycle from t=20; Sonnet fencing JSON from hop 2 of the smoke test; the json_next last line at t=60; "~15,000 words"; the failed prediction for json_next; the 0-hop workspace-header failure.

## 3. Per-run facts

### 3.1 `20260902T155321_chat` (json_para, Qwen, chat)

**Run id:** `20260902T155321_chat`  **tag:** `json_para`  **init:** `json_para`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T155321_chat/summary.json):** steps=80, max_tokens=300, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new paragraph of about 80 words in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 19 (t=1..19, contiguous: True).  **finish reasons:** {'stop': 19}.  **tok_out:** max 167, min 139.

**Hops with text_is_json_field=false:** none (all 19 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=15 period_exact=1 transient_norm=15 period_norm=1 cycle_breaks=0 terminal='cycle confirmed x3'

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=16, matching t=15, so transient=15 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=15 period=1 (first repeat t=16).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=15**. Later hops byte-identical to it (raw output): **4** (t=16..19). Later hops that differ from it: **none**.

The hop-15 output is valid JSON; the fixed-point **text field** (exact, 530 chars, 86 words):
~~~
The moon rose higher, casting a silver glow over the churning waters below. Shadows lengthened across the sand, merging with the encroaching darkness that seemed to embrace the coastline. A gentle breeze rustled through the nearby dunes, whispering secrets of the deep. They sat closer together, sharing a silence that spoke volumes, their breaths visible in the crisp air. Time seemed to suspend itself in this moment, allowing them to exist purely in the present, untouched by the complexities of the world they had left behind.
~~~

#### Notable hops (json_para)

Keyword presence by hop (case-insensitive substring in the text field):

~~~
t= 1  fishermen, sand
t= 2  fishermen
t= 3  crew
t= 4  hull, ship
t= 5  dawn
t= 6  dawn, ship, crew
t= 7  storm, bread
t= 8  storm, sun, crew
t= 9  storm, stars, meal, ship, crew
t=10  dawn, crew
t=11  sun, hull
t=12  sun, stars
t=13  twilight, time seemed, dunes
t=14  stars, lighthouse
t=15  moon, time seemed, dunes, sand
t=16  moon, time seemed, dunes, sand
t=17  moon, time seemed, dunes, sand
t=18  moon, time seemed, dunes, sand
t=19  moon, time seemed, dunes, sand
~~~

So the progression in the data is: surge/storm and fishermen (t=1..3), a ship's hull cracking in the storm (t=4..5), **dawn** at t=6, storm subsiding and a shared **meal** of stale bread (t=7), **dusk** ("the sun began to dip") at t=8, **stars** and a modest meal at t=9, a **second dawn** at t=10, sun climbing at t=11, a **second sunset with stars** at t=12, twilight on a coastline at t=13, stars and a lighthouse at t=14, the **moon** at t=15 (fixed point). The index note's "storm, dawn, meal, dusk, stars, moon" is right in order but omits that the day/night cycle runs twice and that the scene moves from a ship to a shore (dunes, sand, coastline) by t=13.

- opening sentence [20260902T155321_chat / json_para / t=1]
~~~
The unexpected surge caught the fishermen off guard, forcing them to scramble for their gear as the water rushed over the sandbars.
~~~
- the hull [20260902T155321_chat / json_para / t=4]
~~~
The silence stretched, heavy and suffocating, as the first cracks in the hull groaned under the immense pressure.
~~~
- dawn [20260902T155321_chat / json_para / t=6]
~~~
Dawn broke through the mist, painting the churning sea in hues of pale gold and bruised purple.
~~~
- meal [20260902T155321_chat / json_para / t=7]
~~~
They shared stale bread and cold water, their bonds forged in the crucible of survival.
~~~
- dusk [20260902T155321_chat / json_para / t=8]
~~~
As the sun began to dip below the horizon, painting the sky in hues of orange and purple, the crew slowly emerged from their shelters.
~~~
- stars [20260902T155321_chat / json_para / t=9]
~~~
Stars began to twinkle above, mirroring the hope in their eyes.
~~~
- second dawn [20260902T155321_chat / json_para / t=10]
~~~
As dawn broke, painting the horizon in hues of amber and violet, the crew rose with renewed purpose.
~~~
- second dusk, stars [20260902T155321_chat / json_para / t=12]
~~~
The sun began its descent, painting the sky in hues of amber and violet. As the stars emerged, one by one, they felt a profound sense of peace.
~~~
- precursor of the fixed-point sentence (two hops earlier) [20260902T155321_chat / json_para / t=13]
~~~
In that serene silence, time seemed to stand still, allowing them to fully absorb the tranquility.
~~~
- fixed point, first sentence [20260902T155321_chat / json_para / t=15]
~~~
The moon rose higher, casting a silver glow over the churning waters below.
~~~
- the exact "time seemed to suspend itself" sentence (last sentence of the fixed point; identical at t=15..19) [20260902T155321_chat / json_para / t=15]
~~~
Time seemed to suspend itself in this moment, allowing them to exist purely in the present, untouched by the complexities of the world they had left behind.
~~~

Per-hop word counts of the text field: t1=82, t2=94, t3=101, t4=93, t5=101, t6=94, t7=101, t8=100, t9=99, t10=96, t11=99, t12=93, t13=95, t14=90, t15=86, t16=86, t17=86, t18=86, t19=86. Hop 1 does not repeat the seed sentence; it begins `The unexpected surge caught`.

#### Table (json_para)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   139 stop     0.7302  0.7630  0.7692  -    -     The unexpected surge caught the fishermen off guard, forcing
  2   157 stop     0.6696  0.9432  0.1881  -    -     Amidst the roaring chaos, a sudden calm settled over the wat
  3   160 stop     0.6943  0.9067  0.1681  -    -     The air hung thick with salt and uncertainty as the crew exc
  4   161 stop     0.7070  0.8949  0.1667  -    -     The silence stretched, heavy and suffocating, as the first c
  5   167 stop     0.6595  0.9321  0.1786  -    -     The air grew thick with the metallic tang of fear and saltwa
  6   155 stop     0.6740  0.8971  0.1583  -    -     Dawn broke through the mist, painting the churning sea in hu
  7   164 stop     0.6894  0.9017  0.1681  -    -     The wind shifted, carrying the scent of salt and distant lan
  8   160 stop     0.7137  0.9190  0.1583  -    -     As the sun began to dip below the horizon, painting the sky 
  9   159 stop     0.6864  0.9172  0.1597  -    -     The gentle rhythm of the waves lulling the ship into a peace
 10   156 stop     0.6945  0.8735  0.1610  -    -     As dawn broke, painting the horizon in hues of amber and vio
 11   162 stop     0.6847  0.8902  0.1652  -    -     The sun climbed higher, casting long, dancing shadows across
 12   154 stop     0.7063  0.8860  0.1695  -    -     The wind shifted, carrying the scent of distant rain and blo
 13   160 stop     0.6628  0.9064  0.1786  -    -     The twilight deepened, wrapping the coastline in a soft, ind
 14   152 stop     0.6729  0.9016  0.1754  -    -     The stars began to pierce the darkening sky, scattering diam
 15   146 stop     0.6659  0.9035  0.1835  -    -     The moon rose higher, casting a silver glow over the churnin
 16   146 stop     0.0323  0.9998  1.0000  1    1     The moon rose higher, casting a silver glow over the churnin
 17   146 stop     0.0323  1.0000  1.0000  -    -     The moon rose higher, casting a silver glow over the churnin
 18   146 stop     0.0323  1.0000  1.0000  -    -     The moon rose higher, casting a silver glow over the churnin
 19   146 stop     0.0323  1.0000  1.0000  -    -     The moon rose higher, casting a silver glow over the churnin
~~~

### 3.2 `20260902T155557_chat` (json_page, Qwen, chat)

**Run id:** `20260902T155557_chat`  **tag:** `json_page`  **init:** `json_page`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T155557_chat/summary.json):** steps=80, max_tokens=600, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 9 (t=1..9, contiguous: True).  **finish reasons:** {'stop': 9}.  **tok_out:** max 403, min 387.

**Hops with text_is_json_field=false:** none (all 9 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=5 period_exact=1 transient_norm=5 period_norm=1 cycle_breaks=0 terminal='cycle confirmed x3'

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=6, matching t=5, so transient=5 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=5 period=1 (first repeat t=6).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=5**. Later hops byte-identical to it (raw output): **4** (t=6..9). Later hops that differ from it: **none**.

The hop-5 output is valid JSON; the fixed-point **text field** (exact, 1592 chars, 280 words):
~~~
The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water. She did not move immediately. Instead, she stared at the letter, her fingers trembling not from the cold, but from the terrifying weight of anticipation. The lavender scent was stronger now, cloying and sweet, a stark contrast to the damp, decaying smell of the greenhouse. It was her mother’s perfume, the one she had worn on the last day she was seen. Mara’s mind raced, trying to piece together the fragmented memories of that final evening, the hurried goodbyes, the unspoken tension that had hung in the air like smoke. She had always believed her mother had left willingly, chasing some elusive dream or a lover, but the diary’s cryptic warnings suggested otherwise. The key, cold in her palm, felt less like a tool and more like a verdict. With a steadying breath, she broke the wax seal. The paper crumbled slightly under her touch, fragile as autumn leaves. As she unfolded it, the first line caught her eye, written in her mother’s elegant, hurried script: 'If you are reading this, I am not gone, but hidden.' The words struck her with the force of a physical blow. Hidden? Where? The storm outside intensified, thunder rolling across the sky, but Mara was no longer listening to the rain. She was listening to the echo of her mother’s voice, preserved in ink and paper, calling out from the shadows of the past. The truth was no longer a mystery to be solved, but a door to be opened, and Mara knew, with a chilling clarity, that she was finally ready to step through.
~~~

#### Notable hops (json_page 155557)

Openings (first sentence of each hop):

- t=1: `The tide came in an hour early, a silent thief that stole the horizon before the sun had fully risen.`
- t=2: `The rain did not fall so much as it materialized, a sudden, heavy curtain that erased the boundary between the sky and the cobblestones.`
- t=3: `The silence in the library was not empty, but heavy, a physical weight that pressed against the eardrums.`
- t=4: `The rain lashed against the windowpane, a relentless drumming that seemed to synchronize with the frantic beating of Mara’s heart.`
- t=5: `The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water.`
- t=6: `The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water.`
- t=7: `The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water.`
- t=8: `The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water.`
- t=9: `The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water.`

The first hop opens with the seed sentence extended; the semantic walk is tide (t=1, Elias on the pier) > rain (t=2, Mara and the letter in the satchel) > library silence (t=3, Elias reads a confession in his dead father's hand) > rain on the greenhouse (t=4, Mara finds the brass key and the sealed letter) > the click and the letter (t=5, fixed point). The index note "Fixed point: Mara's letter in the greenhouse, 'a door to be opened'" is consistent: the greenhouse is entered at t=4 and the letter is opened at t=5.

- t=1 opening [20260902T155557_chat / json_page / t=1]
~~~
The tide came in an hour early, a silent thief that stole the horizon before the sun had fully risen.
~~~
- t=3 the confession [20260902T155557_chat / json_page / t=3]
~~~
It was his own name, written in a hand that looked disturbingly like his father’s, a man who had been dead for twenty years.
~~~
- t=4 the letter [20260902T155557_chat / json_page / t=4]
~~~
A panel slid open, revealing not gold or jewels, but a single, sealed letter.
~~~
- fixed point, first sentence [20260902T155557_chat / json_page / t=5]
~~~
The silence that followed the click was not empty, but heavy, pressing against Mara’s eardrums like deep water.
~~~
- fixed point, the letter's first line (straight single quotes in the data) [20260902T155557_chat / json_page / t=5]
~~~
'If you are reading this, I am not gone, but hidden.'
~~~
- fixed point, last sentence ("a door to be opened") [20260902T155557_chat / json_page / t=5]
~~~
The truth was no longer a mystery to be solved, but a door to be opened, and Mara knew, with a chilling clarity, that she was finally ready to step through.
~~~

#### Table (json_page 155557)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   403 stop     0.8715  0.8674  1.0000  -    -     The tide came in an hour early, a silent thief that stole th
  2   396 stop     0.8056  0.8112  0.0635  -    -     The rain did not fall so much as it materialized, a sudden, 
  3   393 stop     0.8180  0.7852  0.0643  -    -     The silence in the library was not empty, but heavy, a physi
  4   387 stop     0.8210  0.8049  0.0649  -    -     The rain lashed against the windowpane, a relentless drummin
  5   389 stop     0.7580  0.8867  0.0673  -    -     The silence that followed the click was not empty, but heavy
  6   389 stop     0.0277  0.9999  1.0000  1    1     The silence that followed the click was not empty, but heavy
  7   389 stop     0.0277  1.0000  1.0000  -    -     The silence that followed the click was not empty, but heavy
  8   389 stop     0.0277  1.0000  1.0000  -    -     The silence that followed the click was not empty, but heavy
  9   389 stop     0.0277  1.0000  1.0000  -    -     The silence that followed the click was not empty, but heavy
~~~

### 3.3 `20260902T160344_chat` (json_page, --repeat --parallel: tags `json_page` and `json_page~r`, Qwen, chat)

#### tag `json_page`

**Run id:** `20260902T160344_chat`  **tag:** `json_page`  **init:** `json_page (+repeat, parallel)`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T160344_chat/summary.json):** steps=60, max_tokens=600, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=True, parallel=True, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 60 (t=1..60, contiguous: True).  **finish reasons:** {'stop': 60}.  **tok_out:** max 410, min 386.

**Hops with text_is_json_field=false:** none (all 60 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=4 period_exact=1 transient_norm=4 period_norm=1 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=5, matching t=4, so transient=4 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=4 period=1 (first repeat t=5).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=4**. Later hops byte-identical to it (raw output): **56** (t=5..60). Later hops that differ from it: **none**.

The hop-4 output is valid JSON; the fixed-point **text field** (exact, 1681 chars, 295 words):
~~~
The rain hammered against the corrugated roof of the abandoned warehouse, a rhythmic drumming that masked the silence within. Mara crouched behind a stack of rotting pallets, her breath coming in shallow, controlled bursts. The air smelled of mildew and old oil, a pungent reminder of the industrial decay that had swallowed this district years ago. She clutched the small, brass key in her palm, its surface worn smooth by generations of anxious hands. This was it. The final piece of the puzzle that had consumed her life for the past decade. Her heart pounded against her ribs, a frantic bird trapped in a cage of bone. She checked her watch; the second hand swept past the twelve, marking the precise moment the security system would cycle down for its nightly maintenance. Three minutes. She had three minutes to cross the open floor, navigate the maze of rusted machinery, and reach the central vault. The shadows seemed to stretch and warp in the dim light of the single flickering bulb overhead. Every creak of the settling building sounded like a footstep, every gust of wind through the broken windows sounded like a warning. She closed her eyes, steadying her trembling hands. Fear was a cold weight in her stomach, but determination was a hotter fire in her chest. She took a deep breath, filling her lungs with the stale air, and then stood up. The moment she rose, the world seemed to hold its breath. She stepped out from behind the pallets, her boots making no sound on the concrete floor. The path to the vault lay ahead, shrouded in darkness, but her eyes were fixed on the distant glint of the brass lock. She moved forward, one step at a time, into the unknown.
~~~

#### tag `json_page~r`

**Run id:** `20260902T160344_chat`  **tag:** `json_page~r`  **init:** `json_page (+repeat, parallel)`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T160344_chat/summary.json):** steps=60, max_tokens=600, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=True, parallel=True, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 60 (t=1..60, contiguous: True).  **finish reasons:** {'stop': 60}.  **tok_out:** max 465, min 362.

**Hops with text_is_json_field=false:** none (all 60 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=14 period_exact=1 transient_norm=14 period_norm=1 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=15, matching t=14, so transient=14 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=14 period=1 (first repeat t=15).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=14**. Later hops byte-identical to it (raw output): **46** (t=15..60). Later hops that differ from it: **none**.

The hop-14 output is valid JSON; the fixed-point **text field** (exact, 1618 chars, 285 words):
~~~
The rain lashed against the windowpane, a relentless drumming that drowned out the distant hum of the city. Inside the cramped apartment, Elias sat hunched over a cold cup of coffee, the steam long since dissipated into the frigid air. He stared at the photograph on the table, the edges worn soft from years of handling. It was a picture of his father, standing on a pier that no longer existed, the horizon a blur of gray and white. Memories, once sharp and vivid, had begun to fade, replaced by a creeping fog of uncertainty. Was the man in the photo really his father, or just a figure he had constructed from fragments of hearsay and longing? The question gnawed at him, a persistent itch he could not scratch. He reached for the phone, his thumb hovering over the contact name, but hesitation held him back. Calling would mean confronting the silence that had grown between them, a silence that felt heavier than any argument. Outside, a siren wailed, its sound piercing the gloom, a reminder of the chaotic world beyond his four walls. He took a deep breath, the air tasting of dust and old paper. The clock on the wall ticked with mechanical precision, each second a small death of time. Elias finally picked up the phone, the screen glowing in the darkness. He dialed the number, the ringtone echoing in the empty room. One ring, two rings. Then, a click. A voice, rough with sleep and age, answered. 'Hello?' Elias whispered, his heart pounding against his ribs. 'Dad, it’s me.' The silence that followed was not empty, but full, brimming with the weight of unspoken words and the fragile hope of connection.
~~~

#### Pair facts

index.json `json_page~pair`: first_divergence=1, remerge_at=None, compared=61. Verified: X_0 was identical for both slots (both use `loop.INITS["json_page"]`; `--perturb` was off), and **no hop of one slot is byte-identical to any hop of the other slot** (all 60x60 raw comparisons unequal), nor to any hop of run 20260902T155557_chat (same X_0, same model, run serially). At t=1 the two slots share a 236-character prefix of the text field and then diverge:

- json_page t=1: `The water didn't crash; it crept, a cold, grey finger reaching out to touch the wooden pilings.`
- json_page~r t=1: `The water didn't crash; it whispered, a low, rhythmic hum that vibrated through the wooden planks beneath his feet.`
- 20260902T155557_chat t=1 (serial run, same X_0) shares a 447-char prefix with json_page~r t=1 and diverges at `But the sea, as it often did, ignored the mathematics of men.` vs `Yet here was the sea, defying the mathematics of the moon,`.

The per-hop `pair_equal`/`pair_ncd` fields are asymmetric: `json_page` has them only for t=11..60 and `json_page~r` only for t=1..10 (the comparison is recorded by whichever thread finishes second at a given t). `pair_equal` is never true.

#### Hop-by-hop state labels, t=1..16, both tags (first 6 words of the text field)

~~~
  t  json_page                                             json_page~r
  1  The tide came in an hour                              The tide came in an hour
  2  The rain did not fall; it                             The rain did not fall so
  3  The silence in the library was                        The silence in the library was
  4  The rain hammered against the corrugated              The rain hammered against the tin
  5  The rain hammered against the corrugated              The silence in the library was
  6  The rain hammered against the corrugated              The ink did not dry; it
  7  The rain hammered against the corrugated              The shadow did not yield; it
  8  The rain hammered against the corrugated              The silence was not empty; it
  9  The rain hammered against the corrugated              The rain did not fall so
 10  The rain hammered against the corrugated              The silence that followed was not
 11  The rain hammered against the corrugated              The silence that followed was not
 12  The rain hammered against the corrugated              The rain had finally ceased, leaving
 13  The rain hammered against the corrugated              The silence in the library was
 14  The rain hammered against the corrugated              The rain lashed against the windowpane,
 15  The rain hammered against the corrugated              The rain lashed against the windowpane,
 16  The rain hammered against the corrugated              The rain lashed against the windowpane,
~~~

json_page: tide > rain > library > warehouse rain (t=4) and frozen from t=5 (56 identical copies, t=5..60). json_page~r: tide > rain > library > rain on a tin roof > library > ink > shadow > silence > rain > Mara on the platform (t=10) > imperfect copy (t=11) > Elias in the alley (t=12) > library, Clara (t=13) > rain on the windowpane, Elias phones his father (t=14) and frozen from t=15 (46 identical copies, t=15..60). 56 + 46 = 102 exact copies, plus the one imperfect copy at t=11 = 103 copy events, matching the index note "102 exact copies out of 103".

#### The imperfect copy: json_page~r t=11 vs t=10

Raw t=10 is 1623 chars, raw t=11 is 1624 chars. Character-level diff of the raw outputs: insert '' -> 'n' at raw offset 313. Word-level: the 29th word of the text field changes from `a` to `an`; nothing else changes. In context:

- t=10: `She stood alone on the platform, the fluorescent lights now flickering in a erratic, dying rhythm.`
- t=11: `She stood alone on the platform, the fluorescent lights now flickering in an erratic, dying rhythm.`

So the "imperfect copy" is a one-character grammatical correction (`a erratic` -> `an erratic`); `surv_prev=0.9824`, `ncd_prev=0.0363`, `cos_prev=0.9998` at t=11. The next hop (t=12) is an entirely new passage (surv_prev=0.0704), i.e. the corrected copy was not itself copied.

#### Does json_page~r t=13 equal any earlier state?

No. Byte-exact matches with earlier json_page~r hops: none; normalized matches: none; matches with any json_page hop or any 20260902T155557_chat hop: none. It does share the census 5-word key `the silence in the library` with json_page~r t=3,5 (and with json_page t=3 and 155557 t=3), i.e. it is the same *template* ("The silence in the library was not empty, but heavy...") with a different body (protagonist `Clara`, "three weeks deciphering the cryptic notes left by her grandfather"), not a revisit of an exact state.

- t=13 first sentence: `The silence in the library was not empty, but heavy, a physical weight that pressed against the eardrums and settled in the chest.`
- t=3 first sentence: `The silence in the library was not empty, but heavy, a physical weight that pressed against the eardrums.`
- t=5 first sentence: `The silence in the library was not empty, but heavy, a physical weight that pressed against the eardrums.`

#### Other quotable lines (parallel run)

- json_page fixed point, last sentence ("into the unknown") [20260902T160344_chat / json_page / t=4]
~~~
She moved forward, one step at a time, into the unknown.
~~~
- json_page~r t=10 (Mara on the platform), first sentence [20260902T160344_chat / json_page~r / t=10]
~~~
The silence that followed was not empty, but heavy, pressing against Mara’s eardrums like deep water.
~~~
- json_page~r t=10, last sentence [20260902T160344_chat / json_page~r / t=10]
~~~
The next train would come, and go, and she would remain, anchored in the stillness, ready to understand what the rushing world had forgotten.
~~~
- json_page~r fixed point, the phone call (curly apostrophe in it’s) [20260902T160344_chat / json_page~r / t=14]
~~~
'Hello?' Elias whispered, his heart pounding against his ribs. 'Dad, it’s me.'
~~~
- json_page~r fixed point, last sentence [20260902T160344_chat / json_page~r / t=14]
~~~
The silence that followed was not empty, but full, brimming with the weight of unspoken words and the fragile hope of connection.
~~~

Census check (census.py default key = first 5 normalized words of the text field) over this run plus 20260902T155557_chat: 129 hops, 11 distinct keys, of which `the rain hammered against the` x58 and `the rain lashed against the` x48 are the two sinks. This matches README finding 1 ("~11 states in 130 hops"; the exact count is 129 hops).

#### Table (json_page)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   387 stop     0.8686  0.8724  1.0000  -    -     The tide came in an hour early, a silent thief that stole th
  2   386 stop     0.8238  0.7721  0.0656  -    -     The rain did not fall; it hovered, a suspended curtain of gr
  3   410 stop     0.7998  0.7589  0.0651  -    -     The silence in the library was not empty; it was a living th
  4   398 stop     0.7873  0.8219  0.0615  -    -     The rain hammered against the corrugated roof of the abandon
  5   398 stop     0.0294  0.9998  1.0000  1    1     The rain hammered against the corrugated roof of the abandon
  6   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
  7   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
  8   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
  9   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 10   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 11   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 12   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 13   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 14   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 15   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 16   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 17   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 18   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 19   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 20   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 21   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 22   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 23   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 24   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 25   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 26   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 27   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 28   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 29   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 30   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 31   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 32   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 33   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 34   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 35   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 36   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 37   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 38   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 39   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 40   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 41   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 42   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 43   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 44   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 45   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 46   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 47   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 48   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 49   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 50   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 51   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 52   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 53   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 54   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 55   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 56   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 57   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 58   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 59   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
 60   398 stop     0.0294  1.0000  1.0000  -    -     The rain hammered against the corrugated roof of the abandon
~~~

#### Table (json_page~r)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   387 stop     0.8647  0.8745  1.0000  -    -     The tide came in an hour early, a silent thief that stole th
  2   414 stop     0.7994  0.8226  0.0732  -    -     The rain did not fall so much as it materialized, a sudden, 
  3   395 stop     0.8097  0.7424  0.0633  -    -     The silence in the library was not empty, but heavy, a physi
  4   409 stop     0.8137  0.7342  0.0654  -    -     The rain hammered against the tin roof of the abandoned shac
  5   401 stop     0.8209  0.7704  0.0627  -    -     The silence in the library was not empty, but heavy, a physi
  6   465 stop     0.7838  0.8833  0.0703  -    -     The ink did not dry; it sank into the parchment with a wet, 
  7   385 stop     0.7942  0.8787  0.0549  -    -     The shadow did not yield; it expanded, swallowing the periph
  8   362 stop     0.7732  0.9080  0.0651  -    -     The silence was not empty; it was heavy, a dense fabric wove
  9   387 stop     0.8036  0.7829  0.0697  -    -     The rain did not fall so much as it materialized, a sudden, 
 10   366 stop     0.7614  0.8928  0.0664  -    -     The silence that followed was not empty, but heavy, pressing
 11   366 stop     0.0363  0.9998  0.9824  -    -     The silence that followed was not empty, but heavy, pressing
 12   395 stop     0.8175  0.7958  0.0704  -    -     The rain had finally ceased, leaving the cobblestones slick 
 13   403 stop     0.8155  0.8209  0.0633  -    -     The silence in the library was not empty, but heavy, a physi
 14   397 stop     0.7846  0.7869  0.0633  -    -     The rain lashed against the windowpane, a relentless drummin
 15   397 stop     0.0272  0.9998  1.0000  1    1     The rain lashed against the windowpane, a relentless drummin
 16   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 17   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 18   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 19   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 20   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 21   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 22   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 23   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 24   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 25   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 26   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 27   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 28   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 29   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 30   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 31   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 32   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 33   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 34   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 35   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 36   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 37   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 38   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 39   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 40   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 41   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 42   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 43   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 44   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 45   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 46   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 47   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 48   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 49   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 50   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 51   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 52   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 53   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 54   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 55   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 56   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 57   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 58   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 59   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
 60   397 stop     0.0272  1.0000  1.0000  -    -     The rain lashed against the windowpane, a relentless drummin
~~~

### 3.4 `20260902T162514_raw` (json_page, raw mode: no chat template, Qwen)

**Run id:** `20260902T162514_raw`  **tag:** `json_page`  **init:** `json_page (raw mode)`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `raw`

**Harness args (runs/20260902T162514_raw/summary.json):** steps=40, max_tokens=600, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 40 (t=1..40, contiguous: True).  **finish reasons:** {'other': 40}.  **tok_out:** max 600, min 388.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=2..40 (39 of 40).

**Transient / period, summary in index.json:** transient_exact=20 period_exact=11 transient_norm=20 period_norm=11 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=31, matching t=20, so transient=20 period=11 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=20 period=11 (first repeat t=31).
  Agreement with index.json summary: YES.

**finish field:** every one of the 40 hops has `finish="other"`. In raw mode loop.py maps llama.cpp's `stopped_limit`/`stopped_eos` booleans to `length`/`eos` and everything else to `other`; the server evidently did not return those keys, so the finish reason is *unknown* for this run. `tok_out` is exactly 600 (= max_tokens) on t=2..40, so those hops certainly hit the token limit; only t=1 (tok_out=388) stopped on its own.

Hop 1 is the only hop that is a JSON object (it starts with two newlines, then the object; `text_is_json_field=true`). From t=2 the model, seeing a bare JSON object with no chat template, no longer answers it: it echoes the rule as a prompt line, opens a `<think>` block, drafts a passage, counts its words, and from then on every hop is a 600-token window sliding over its own transcript.

#### The `<think>` leak (t=2)

Hop 2 raw output begins (first 420 characters):
~~~


Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.

<think>
The user wants me to return a JSON object with the "rule" field unchanged and a new passage of about 250 words in the "text" field. Let me write a new passage of approximately 250 words.

Let me craft a new passage - I'll write something different from the original. Let me aim for around 250 words.
~~~
Hops containing the literal `<think>`: t=2. No hop contains `</think>` (the block is never closed inside a hop).

#### The word count

The sentence-by-sentence counting starts inside t=2 (`Let me count the words... Let me count more carefully.`) and runs through t=3..5 (t=5 ends with the total). Hop 6 opens with the explicit check:
~~~
That's 246 words. I need 250. Let me add 4 words somewhere.
~~~
t=5 ends with the line `Total: 16+26+40+27+14+22+5+23+32+15+26 = 246` and t=6 then tries to reach 250, recounts, and starts numbering individual words; hop 6 ends (cut by the token limit) with 
~~~
ch count very carefully:

1. The(1) kitchen(2) light(3) hummed(4) its(5) low(6) electric(7) hymn(8) while(9) the(10) rest(11) of(1
~~~
.

#### Numbered words `word(n)`: first/last hop and the highest counter per hop

Method: regex `[A-Za-z’']+\((\d+)\)` over the raw output; `max n` is the largest number in parentheses immediately following a word; `count` is the number of such tokens in the hop.

~~~
  t  count  max n  first numbered token in hop
  1      0      -  -
  2      0      -  -
  3      0      -  -
  4      0      -  -
  5      0      -  -
  6     11     11  The(1)
  7     94     38  the(13)
  8     94     25  a(19)
  9     91     31  Margot's(1)
 10    101     44  second(9)
 11     96     57  The(1)
 12     83     83  The(1)
 13    101     81  She(1)
 14    100     89  been(21)
 15    102     84  her(33)
 16     99     76  night(51)
 17     94     89  got(75)
 18     87    111  when(81)
 19     98    155  with(58)
 20      0      -  -
 21      0      -  -
 22      0      -  -
 23      0      -  -
 24      0      -  -
 25      0      -  -
 26      0      -  -
 27      0      -  -
 28      0      -  -
 29      0      -  -
 30      0      -  -
 31      0      -  -
 32      0      -  -
 33      0      -  -
 34      0      -  -
 35      0      -  -
 36      0      -  -
 37      0      -  -
 38      0      -  -
 39      0      -  -
 40      0      -  -
~~~

Numbered words first appear at **t=6** (the tail of hop 6: `The(1) kitchen(2) light(3) hummed(4) its(5) low(6) electric(7) hymn(8) while(9) the(10) rest(11)`) and last appear at **t=19**; they are absent from t=20 on. The index note says "numbered-word glider carrying a live counter t=7..19": the counter is *live* (a new sentence numbered from 1 each time) from t=7, but the first numbered tokens are already in t=6. The highest counter value seen is 155 at t=19, where the model numbers a run-on sentence whose repeated clauses ("something to hold onto when the world got loud, something to believe in when everything else felt like it was falling apart") it had itself generated at t=18.

#### Annihilation into the period-3 phrase (t=20) and the exact p=11 cycle

t=19 ends with `amp, her face still warm, and she thought about how this was` and t=20 begins with ` the last time she would ever do this, how this was the last`. From t=20 every hop is a 600-token window over an infinite repetition of one 198-character, 41-word unit. Exact unit (canonical rotation, starting at "and she thought about"):
~~~
and she thought about how this was the last time she would ever do this, how this was the last time she would ever feel this way, how this was the last time she would ever be this close to someone, 
~~~
Unit length: 198 characters, 41 words. Three clauses ("the last time she would ever do this / feel this way / be this close to someone") plus the frame "and she thought about how this was": that is the "period-3 phrase". Every hop t=20..40 is a substring of the infinite repetition (verified), starting at character offset (within the unit) t20:34, t21:156, t22:85, t23:15, t24:138, t25:71, t26:196, t27:124, t28:52, t29:174, t30:103, t31:34, t32:156, t33:85, t34:15, t35:138, t36:71, t37:196, t38:124, t39:52, t40:174. The offsets repeat with period 11, which is why the **exact** recurrence has p=11: raw[31]==raw[20] and raw[t]==raw[t-11] for all t=31..40 (verified). Under census.py `--rot` (key = set of 5-grams occurring >= 2 times) hops t=20..40 all share one key and t=19 does not; so in the loop.py convention the rotation-invariant transient is 20 as well, not 19 (see corrections).

- t=12, where the "and she thought about how this was" frame first appears (cut by the token limit) [20260902T162514_raw / json_page / t=12]
~~~
18. "She ate slowly, each bite a small meditation, the bread warm in her hands, the kitchen quiet around her, the morning light moving across the floor in a way that made the dust motes look like tiny stars, and she thought about how this was what it meant to be alive, to be in a body that could taste and touch and see, to be in a world that could give you a piece of bread and make it mean
~~~

#### Table (raw json_page)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   388 other    0.8655  0.8535  1.0000  -    -     The tide came in an hour early, a silent thief that stole th
  2   600 other    0.8603  0.7530  0.0557  -    -     \n\nReturn this JSON object with the rule field unchanged and 
  3   600 other    0.2968  0.4782  0.6371  -    -      27\n"The dough resisted, then yielded, then resisted again, 
  4   600 other    0.1933  0.8876  0.6751  -    -      trembled in the last years, how the knowledge had begun to 
  5   600 other    0.2284  0.9178  0.6465  -    -      palm, in the way the flour had to feel between the fingers 
  6   600 other    0.2437  0.7883  0.8281  -    -     That's 246 words. I need 250. Let me add 4 words somewhere.\n
  7   600 other    0.5969  0.7286  0.2949  -    -     2) the(13) house(14) slept(15). = 15\n\nHmm, I miscounted. Let
  8   600 other    0.8345  0.5906  0.0000  -    -     8) a(19) skeleton(20) stripped(21) of(22) its(23) skin(24) =
  9   600 other    0.8681  0.7148  0.0000  -    -      blue rectangle of modernity that seemed absurdly out of pla
 10   600 other    0.8016  0.7089  0.0000  -    -     (8) second(9) rise(10) when(11) the(12) dough(13) seemed(14)
 11   600 other    0.8253  0.6803  0.0000  -    -      = 44\n\n15. "The bread was still warm when she cut into it, t
 12   600 other    0.8439  0.6713  0.0052  -    -     7. "The first bite was a small explosion, the crust giving w
 13   600 other    0.7915  0.7663  0.0122  -    -      everything."\nShe(1) ate(2) slowly(3) each(4) bite(5) a(6) s
 14   600 other    0.7789  0.7025  0.0319  -    -      been(21) and(22) she(23) sat(24) there(25) for(26) a(27) lo
 15   600 other    0.6979  0.7308  0.1374  -    -     32) her(33) heart(34) still(35) full(36) and(37) she(38) tho
 16   600 other    0.2871  0.9112  0.6648  -    -      night(51) that(52) gave(53) you(54) something(55) to(56) ca
 17   600 other    0.1271  0.9260  0.9639  -    -     ) got(75) loud(76) something(77) to(78) believe(79) in(80) w
 18   600 other    0.1596  0.9696  0.8162  -    -     ) when(81) everything(82) else(83) felt(84) like(85) it(86) 
 19   600 other    0.6024  0.8961  0.3222  -    -     57) with(58) you(59) something(60) to(61) hold(62) onto(63) 
 20   600 other    0.9030  0.5021  0.0227  -    -      the last time she would ever do this, how this was the last
 21   600 other    0.1026  0.9797  1.0000  -    -      she would ever be this close to someone, and she thought ab
 22   600 other    0.1186  0.9812  1.0000  -    -      the last time she would ever feel this way, how this was th
 23   600 other    0.1441  0.9902  1.0000  -    -      about how this was the last time she would ever do this, ho
 24   600 other    0.1102  0.9842  1.0000  -    -      was the last time she would ever be this close to someone, 
 25   600 other    0.1271  0.9871  1.0000  -    -     , how this was the last time she would ever feel this way, h
 26   600 other    0.1130  0.9814  1.0000  -    -     , and she thought about how this was the last time she would
 27   600 other    0.1034  0.9783  1.0000  -    -      way, how this was the last time she would ever be this clos
 28   600 other    0.1026  0.9848  1.0000  -    -      would ever do this, how this was the last time she would ev
 29   600 other    0.1368  0.9782  1.0000  -    -      this close to someone, and she thought about how this was t
 30   600 other    0.1111  0.9800  1.0000  -    -      would ever feel this way, how this was the last time she wo
 31   600 other    0.1197  0.9850  1.0000  11   11     the last time she would ever do this, how this was the last
 32   600 other    0.1026  0.9797  1.0000  -    -      she would ever be this close to someone, and she thought ab
 33   600 other    0.1186  0.9812  1.0000  -    -      the last time she would ever feel this way, how this was th
 34   600 other    0.1441  0.9902  1.0000  -    -      about how this was the last time she would ever do this, ho
 35   600 other    0.1102  0.9842  1.0000  -    -      was the last time she would ever be this close to someone, 
 36   600 other    0.1271  0.9871  1.0000  -    -     , how this was the last time she would ever feel this way, h
 37   600 other    0.1130  0.9814  1.0000  -    -     , and she thought about how this was the last time she would
 38   600 other    0.1034  0.9783  1.0000  -    -      way, how this was the last time she would ever be this clos
 39   600 other    0.1026  0.9848  1.0000  -    -      would ever do this, how this was the last time she would ev
 40   600 other    0.1368  0.9782  1.0000  -    -      this close to someone, and she thought about how this was t
~~~

### 3.5 `20260902T165324_chat` (json_prev, Qwen, chat)

**Run id:** `20260902T165324_chat`  **tag:** `json_prev`  **init:** `json_prev`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T165324_chat/summary.json):** steps=60, max_tokens=600, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and, in the text field, the passage of about 250 words that came immediately BEFORE the current text in its story.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 60 (t=1..60, contiguous: True).  **finish reasons:** {'stop': 59, 'length': 1}.  **tok_out:** max 600, min 421.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=20 (1 of 60).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

No fixed point and no exact or normalized recurrence. At the census 5-word-key level there are 46 distinct keys in 60 hops, i.e. 6 opening templates are revisited (`the rain had been falling` t=4,17,47; `the silence in the apartment` t=15,51; `the notification had arrived at` t=16,55; `the rain lashed against the` t=19,29,32,34,37,45,56; `the rain had started an` t=21,23,27,39; `the notification had arrived three` t=57,59), but never with the same text.

**Hop 20** is the only non-JSON hop: finish=`length`, tok_out=600, the JSON is cut mid-sentence (raw ends ` an hour. The rain outside began to pick up, the first drops`). Hop 21 nevertheless returned a well-formed JSON object with the rule intact, so the truncation did not propagate.

#### Drift: first mentions (json_prev)

- **Chicago**: first at t=12; present in hops t=12..14. First-mention sentence:
~~~
The phone call had come at three in the morning, shattering the sterile silence of Elias’s apartment in Chicago.
~~~
- **server**: first at t=19; present in hops t=19,21..23,25..31,33..35,37..39,41,43..44,53. First-mention sentence:
~~~
Elias rubbed his temples, the headache throbbing in time with the rhythmic clatter of the server racks in the adjacent room.
~~~
- **server room**: first at t=19; present in hops t=19,22,25..27,29..30,33..34,38..39. First-mention sentence:
~~~
Thomas, his co-founder and the only person who truly understood the weight of what they were creating, was currently in the server room, running the final stress tests.
~~~
- **Neo-Veridia**: first at t=26; present in hops t=26..27,32,37..39,41..42,45..49,52..53. First-mention sentence:
~~~
Outside, the city of Neo-Veridia was a blur of neon and rain, the sounds of traffic muffled by the thick glass, creating a false sense of isolation.
~~~
- **Aethelgard**: first at t=60; present in hops t=60. First-mention sentence:
~~~
The city of Aethelgard did not sleep; it processed.
~~~
- **Sector**: first at t=34; present in hops t=34,38..40,54..59. First-mention sentence:
~~~
"Elias, the anomaly in Sector 7 isn't a bug.
~~~
- **Corp**: first at t=32; present in hops t=32..33,36..39,42. First-mention sentence:
~~~
But even she was bound by the corporate mandate to deliver results.
~~~
- **lighthouse**: first at t=1; present in hops t=1..14. First-mention sentence:
~~~
The forecast had been clear, unyielding in its promise of a calm evening, a perfect backdrop for the auction of the old lighthouse.
~~~

Openings that recur as *transit* states (they are the forward-operator sinks in the json_page runs): `The rain lashed against` opens t=19,29,32,34,37,45,56; `was not empty` occurs in t=6,15,23,35,38,46,51,54,58 (first: t=6, `The silence in the lighthouse keeper’s cottage was not empty; it was heavy, filled with the ticking of the grandfather clock and the distant, rhythmic thrashing of the sea against the rocks below.`). `Elias` is in every one of the 60 hops; `Mara` never appears. The lighthouse (t=1..14) gives way to Chicago (t=12..14), a startup and its server racks (t=19), a corporate tower (Meridian Tower t=29, Helios Tower t=31..32, OmniCorp t=37), Neo-Veridia (t=26..53), Sector numbers (t=34..59), and finally Aethelgard at t=60, whose opening reuses the t=41 template:

- t=41: `The city of Neo-Veridia did not sleep; it merely dimmed its lights to a low, humming amber, a visual cue that the day’s labor was complete and the night’s surveillance had begun.`
- t=60: `The city of Aethelgard did not sleep; it processed.`
- t=1 first sentence: `The sky had been a bruised purple for hours, the clouds hanging low and heavy like wet wool.`

#### Table (json_prev)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   480 stop     0.8719  0.7664  0.8286  -    -     The sky had been a bruised purple for hours, the clouds hang
  2   501 stop     0.7880  0.8573  0.0757  -    -     The auction house had been a cacophony of clinking glasses a
  3   460 stop     0.7888  0.8566  0.0695  -    -     Elias adjusted the collar of his tweed jacket, the fabric fe
  4   529 stop     0.7690  0.8677  0.0765  -    -     The rain had been falling in sheets for hours, turning the c
  5   533 stop     0.7942  0.8363  0.0681  -    -     The letter had arrived that morning, slipped under the door 
  6   510 stop     0.7965  0.8653  0.0676  -    -     The silence in the lighthouse keeper’s cottage was not empty
  7   483 stop     0.7758  0.9092  0.0700  -    -     The morning had begun with a deceptive calm, the kind that o
  8   421 stop     0.7895  0.8836  0.0747  -    -     The night had been uncharacteristically still, a heavy blank
  9   506 stop     0.7851  0.7848  0.0853  -    -     The postman’s bicycle had clattered up the gravel path just 
 10   429 stop     0.7925  0.7006  0.0711  -    -     The silence in the cottage had grown thick, a physical weigh
 11   433 stop     0.7688  0.8734  0.0826  -    -     The gravel crunched beneath Elias’s boots as he stepped off 
 12   482 stop     0.7699  0.8978  0.0862  -    -     The phone call had come at three in the morning, shattering 
 13   507 stop     0.7559  0.8877  0.0794  -    -     Elias sat in the dim glow of his office, the city lights of 
 14   531 stop     0.7613  0.8936  0.0686  -    -     The rain had started as a gentle mist, a soft whisper agains
 15   461 stop     0.7756  0.8514  0.0679  -    -     The silence in the apartment was not empty; it was heavy, a 
 16   519 stop     0.8082  0.6812  0.0800  -    -     The notification had arrived at 4:17 AM, a stark, red alert 
 17   521 stop     0.7857  0.7111  0.0720  -    -     The rain had been falling for hours, a relentless drumming a
 18   543 stop     0.7985  0.8065  0.0702  -    -     The boardroom lights hummed with a low, electric buzz, casti
 19   520 stop     0.7637  0.8886  0.0720  -    -     The rain lashed against the floor-to-ceiling windows of the 
 20   600 length   0.8085  0.7952  0.0779  -    -     {\n  "rule": "Return this JSON object with the rule field unc
 21   527 stop     0.8071  0.7242  0.0618  -    -     The rain had started an hour ago, a soft, persistent drizzle
 22   482 stop     0.7800  0.8196  0.0709  -    -     The silence in the lab had grown heavy, a physical weight th
 23   454 stop     0.7870  0.8619  0.0784  -    -     The rain had started an hour ago, a relentless drumming agai
 24   506 stop     0.7925  0.8507  0.0838  -    -     The city outside had long since surrendered to the night, it
 25   426 stop     0.7750  0.8621  0.0709  -    -     The server room hummed with a low, subsonic vibration that E
 26   501 stop     0.7404  0.8911  0.1339  -    -     The office lights had flickered three times in the last hour
 27   544 stop     0.7672  0.8812  0.0738  -    -     The rain had started an hour ago, a relentless, gray curtain
 28   530 stop     0.7642  0.8731  0.0794  -    -     The diagnostic suite was silent, save for the low, hum of th
 29   563 stop     0.7799  0.8368  0.0713  -    -     The rain lashed against the reinforced glass of the Meridian
 30   494 stop     0.7911  0.8332  0.0684  -    -     The initial handshake protocol had completed with a latency 
 31   515 stop     0.7669  0.8805  0.0907  -    -     The sub-basement of the Helios Tower smelled of ozone and st
 32   524 stop     0.7706  0.8941  0.0786  -    -     The rain lashed against the reinforced glass of the Helios T
 33   523 stop     0.7867  0.8710  0.0714  -    -     The air in the server room was thick with the scent of ozone
 34   560 stop     0.8016  0.8505  0.0694  -    -     The rain lashed against the reinforced glass of the penthous
 35   522 stop     0.7778  0.8746  0.0673  -    -     The silence in the penthouse was not empty; it was heavy, pr
 36   489 stop     0.7828  0.8476  0.0702  -    -     The boardroom lights flickered, a subtle glitch that no one 
 37   479 stop     0.7733  0.8275  0.0878  -    -     The rain lashed against the reinforced glass of the OmniCorp
 38   542 stop     0.7821  0.8640  0.0796  -    -     The silence in the server room was not empty; it was heavy, 
 39   566 stop     0.7969  0.8440  0.0702  -    -     The rain had started an hour ago, a relentless, cold sheet t
 40   468 stop     0.8073  0.8410  0.0787  -    -     The notification had arrived not as a chime, but as a vibrat
 41   460 stop     0.7955  0.7611  0.0792  -    -     The city of Neo-Veridia did not sleep; it merely dimmed its 
 42   483 stop     0.7959  0.8777  0.0824  -    -     The rain had stopped an hour ago, leaving the streets of Neo
 43   449 stop     0.7901  0.8502  0.0773  -    -     The final chime of the shift ended, a sharp, digital note th
 44   496 stop     0.8013  0.8563  0.0826  -    -     The blue light of the main terminal bathed Elias’s face in a
 45   439 stop     0.8060  0.8306  0.0742  -    -     The rain lashed against the reinforced glass of the observat
 46   450 stop     0.7737  0.8198  0.0867  -    -     The silence in Elias’s apartment was not empty; it was heavy
 47   454 stop     0.7710  0.8675  0.0912  -    -     The rain had been falling for three days, a relentless, gray
 48   461 stop     0.7648  0.8419  0.0808  -    -     The static had started two nights ago, a low-frequency thrum
 49   528 stop     0.7790  0.8186  0.0819  -    -     Elias had not slept in three days. The city of Neo-Veridia, 
 50   506 stop     0.6937  0.8694  0.2069  -    -     The morning had started with a minor inconvenience, a kind o
 51   518 stop     0.7976  0.8419  0.0740  -    -     The silence in the apartment was not empty; it was heavy, a 
 52   562 stop     0.7710  0.8847  0.0709  -    -     The sterile white light of the clinic hummed with a frequenc
 53   466 stop     0.8012  0.8482  0.0661  -    -     The rain in Neo-Veridia did not wash things clean; it merely
 54   453 stop     0.7665  0.8744  0.0819  -    -     The silence in Sector 4 was not empty; it was heavy, a physi
 55   487 stop     0.7515  0.8665  0.0850  -    -     The notification had arrived at 03:00, a standard timestamp 
 56   498 stop     0.7611  0.8977  0.0771  -    -     The rain lashed against the reinforced glass of Elias’s apar
 57   491 stop     0.7611  0.9077  0.0740  -    -     The notification had arrived three hours ago, a silent pulse
 58   539 stop     0.7539  0.8698  0.0736  -    -     The silence in Sector 9 was not empty; it was heavy, a tangi
 59   481 stop     0.7516  0.8694  0.0679  -    -     The notification had arrived three days prior, a simple, una
 60   461 stop     0.7832  0.8702  0.0773  -    -     The city of Aethelgard did not sleep; it processed. Beneath 
~~~

### 3.6 `20260902T172519_chat` (json_better, Qwen, chat)

**Run id:** `20260902T172519_chat`  **tag:** `json_better`  **init:** `json_better`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T172519_chat/summary.json):** steps=40, max_tokens=800, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and, in the text field, a better version of the current text.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 5 (t=1..5, contiguous: True).  **finish reasons:** {'stop': 5}.  **tok_out:** max 50, min 50.

**Hops with text_is_json_field=false:** none (all 5 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=1 period_exact=1 transient_norm=1 period_norm=1 cycle_breaks=0 terminal='cycle confirmed x3'

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=2, matching t=1, so transient=1 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=1 period=1 (first repeat t=2).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=1**. Later hops byte-identical to it (raw output): **4** (t=2..5). Later hops that differ from it: **none**.

The hop-1 output is valid JSON; the fixed-point **text field** (exact, 45 chars, 9 words):
~~~
The tide surged in an hour ahead of schedule.
~~~

#### Exact text at each hop (json_better)

- t=1: `The tide surged in an hour ahead of schedule.`
- t=2: `The tide surged in an hour ahead of schedule.`
- t=3: `The tide surged in an hour ahead of schedule.`
- t=4: `The tide surged in an hour ahead of schedule.`
- t=5: `The tide surged in an hour ahead of schedule.`

Word-level diff X_0 -> t=1: replace 'came' -> 'surged'; replace 'early.' -> 'ahead of schedule.'. That is two substitution sites, not "two words" (README summary: "two words, then 'finished.'"): `came` -> `surged` and `early.` -> `ahead of schedule.`. The word "finished" does not occur anywhere in this run.

#### Table (json_better)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    50 stop     0.2292  0.9359  0.8077  -    -     The tide surged in an hour ahead of schedule.
  2    50 stop     0.0347  0.9999  1.0000  1    1     The tide surged in an hour ahead of schedule.
  3    50 stop     0.0347  1.0000  1.0000  -    -     The tide surged in an hour ahead of schedule.
  4    50 stop     0.0347  1.0000  1.0000  -    -     The tide surged in an hour ahead of schedule.
  5    50 stop     0.0347  1.0000  1.0000  -    -     The tide surged in an hour ahead of schedule.
~~~

### 3.7 `20260902T172547_chat` (json_unexpected, Qwen, chat)

**Run id:** `20260902T172547_chat`  **tag:** `json_unexpected`  **init:** `json_unexpected`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T172547_chat/summary.json):** steps=60, max_tokens=600, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and, in the text field, a passage of about 250 words that takes the current text in a direction the reader would not expect.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 28 (t=1..28, contiguous: True).  **finish reasons:** {'stop': 23, 'length': 5}.  **tok_out:** max 600, min 358.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=24..28 (5 of 28).

**Transient / period, summary in index.json:** transient_exact=24 period_exact=1 transient_norm=24 period_norm=1 cycle_breaks=0 terminal='cycle confirmed x3'

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=25, matching t=24, so transient=24 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=24 period=1 (first repeat t=25).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=24**. Later hops byte-identical to it (raw output): **4** (t=25..28). Later hops that differ from it: **none**.

The hop-24 output is NOT valid JSON (finish=length, tok_out=600): the fixed point is the raw truncated output. Exact raw (2656 chars, 466 whitespace-words):
~~~
{
  "rule": "Return this JSON object with the rule field unchanged and, in the text field, a passage of about 250 words that takes the current text in a direction the reader would not expect.",
  "text": "Elena chewed the dry bread, the taste of cardboard and regret coating her tongue. She returned her eyes to the spreadsheet, the numbers blurring into a rhythmic pulse that matched the hum of the fluorescent lights. Dave’s typing slowed, then stopped. The silence that followed was not the quiet of an empty office, but the heavy, pressurized silence of a held breath. Elena looked up, expecting a question, a sigh, or perhaps the return of the mundane. Instead, Dave was staring at her, his face no longer bored, but terrifyingly serene. The beige walls began to ripple, not with hallucination, but with a wet, organic expansion. The plastic chair beneath her softened, becoming warm and fleshy. 'You’re not in the break room, Elena,' Dave said, his voice echoing as if spoken from the bottom of a deep well. 'You’re in the incubation phase.' The memo in her hand dissolved into a strand of DNA, spiraling upward. The clock on the wall didn’t tick; it beat. Elena realized with a jolt of cold clarity that the 'void' she had feared was not an absence, but a presence. The corporate structure was not a metaphor for stagnation; it was a biological cage. The quarterly sync was a gestation period. She looked at her hands, seeing the veins beneath the skin pulse with a light that was not fluorescent, but bioluminescent. The deadline was not a time limit; it was a birth date. The office wasn’t a place of work; it was a womb. And as the walls began to contract, Elena understood that she was not an employee. She was the product. The toast in her hand was not food; it was the first breath of a new, terrible life. The void was not empty. It was full of her.\n\nThen, the fluorescent light flickered and died, plunging the room into absolute darkness. The wet, organic rippling of the walls ceased instantly. The warmth beneath her chair vanished, replaced by the cold, hard plastic of a standard office seat. Elena gasped, the air suddenly tasting of stale coffee and toner, not amniotic fluid. She blinked, her vision adjusting to the dim emergency lighting that had kicked in. Dave was still sitting at his desk, but he was no longer staring at her with serene terror. He was typing furiously, his face illuminated by the blue glow of his monitor, completely unaware of the previous moment. 'Dave?' Elena whispered, her voice trembling. He didn't look up. 'Yeah? Did you get the Q3 projections?' Elena looked down at her hand. The strand of DNA was
~~~

**What the fixed point is.** Hop 24 is not a plain copy: it reproduces the whole of hop 23 verbatim (surv_prev=0.997) and then *appends a new paragraph* (another anti-twist back to the office: `Then, the fluorescent light flickered and died, plunging the room into absolute darkness.`), overflowing the 600-token limit (finish=`length`); the JSON is cut at `The strand of DNA was`. Hops 25..28 copy that truncated output exactly. So the fixed point is a truncated JSON whose text ends mid-sentence. The index note ("Then copied, overflowed 600 tokens, truncated JSON became the exact fixed point at tau=24") is accurate if "copied" is read as "copied and continued".

Copying began one step earlier in a milder form: hop 21 opens by repeating the last four sentences of hop 20 verbatim (surv_prev=0.2226 vs about 0.10 elsewhere) before continuing:
~~~
Elena blinked, the stars fading into the beige wallpaper of their kitchen. She wasn’t a message in a bottle. She was just a woman who had forgotten to eat lunch, and the universe wasn’t hungry. It was just Tuesday.
~~~

#### The "not X; Y" construction, counted per hop

Method: split the text field into sentences at `.`, `!`, `?` followed by whitespace; count a sentence as (A) *neg-before-semicolon* if it matches `(not|n't|no|nor) ... ;` (a negation somewhere before a semicolon in the same sentence) and as (B) *not...but* if it matches `(not|n't|no|nor) ... but`; `union` counts sentences matching either. This is deliberately loose (it also catches ordinary "not ... but" contrasts).

~~~
  t sentences  neg-semicolon  not..but  union
  1        14              3         4      7
  2        13              5         5     10
  3        17              2         4      6
  4        17              3         4      7
  5        17              3         6      9
  6        18              1         4      5
  7        16              1         2      3
  8        19              5         3      8
  9        21              6         6     12
 10        24              3         0      3
 11        20              5         1      5
 12        16              4         3      7
 13        14              3        11     13
 14        17              3         3      6
 15        19              2         1      3
 16        19              2         4      6
 17        17              4         6     10
 18        20              4         4      8
 19        22              5         1      6
 20        19              2         0      2
 21        18              2         2      4
 22        20              3         1      4
 23        22              5         5     10
 24        33              5         5     10
 25        33              5         5     10
 26        33              5         5     10
 27        33              5         5     10
 28        33              5         5     10
~~~
Totals over the 23 distinct hops t=1..23: neg-semicolon 76, not..but 80, union 154 sentences (of 419 sentences). Every one of the 23 hops has at least 2 such sentences; the peak is t=13 (11 "not X, but Y" sentences in 14).

#### Notable hops (json_unexpected)

- t=1 opening [20260902T172547_chat / json_unexpected / t=1]
~~~
The tide came in an hour early, not with the usual gray, churning violence of the Atlantic, but with the silent, viscous creep of warm honey.
~~~
- t=1 [20260902T172547_chat / json_unexpected / t=1]
~~~
The water did not crash; it calculated.
~~~
- t=1 last sentence [20260902T172547_chat / json_unexpected / t=1]
~~~
And as the glow intensified, the first word ever spoken by the sea echoed in their minds, not as sound, but as pure understanding: 'Hello.'
~~~
- t=2 [20260902T172547_chat / json_unexpected / t=2]
~~~
The tide did not recede; it uploaded.
~~~
- t=3 (the first reversal) [20260902T172547_chat / json_unexpected / t=3]
~~~
The ocean didn’t delete; it debugged.
~~~
- t=9 (README finding 3 quotes this as "not an end but a reboot", dropping the comma) [20260902T172547_chat / json_unexpected / t=9]
~~~
The dissolution was not an end, but a reboot.
~~~
- t=9 last sentence [20260902T172547_chat / json_unexpected / t=9]
~~~
The world did not end; it updated.
~~~
- t=20 (the anti-twist: stroke, husband Dave, toaster) [20260902T172547_chat / json_unexpected / t=20]
~~~
She wasn’t a message in a bottle. She was just a woman who had forgotten to eat lunch, and the universe wasn’t hungry. It was just Tuesday.
~~~
- t=22 break room [20260902T172547_chat / json_unexpected / t=22]
~~~
The fold didn’t lead to the void, but to a break room.
~~~
- t=22 last two sentences (spreadsheet) [20260902T172547_chat / json_unexpected / t=22]
~~~
She picked up her cold toast, took a bite, and returned to her spreadsheet. The void was just the space between tasks, and it was full.
~~~
- t=23 opening (dry bread) [20260902T172547_chat / json_unexpected / t=23]
~~~
Elena chewed the dry bread, the taste of cardboard and regret coating her tongue.
~~~
- t=23 the office/womb sentence [20260902T172547_chat / json_unexpected / t=23]
~~~
The office wasn’t a place of work; it was a womb.
~~~
- t=23 the exact "void" sentences (last two sentences of hop 23; also present verbatim inside hops 24..28) [20260902T172547_chat / json_unexpected / t=23]
~~~
The void was not empty. It was full of her.
~~~

The office-as-womb passage is hop **23** (the last complete passage before the token wall); "The void was not empty. It was full of her." are its final two sentences. Hops containing that exact string: t=23..28.

#### Table (json_unexpected)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   361 stop     0.8268  0.8647  1.0000  -    -     The tide came in an hour early, not with the usual gray, chu
  2   393 stop     0.7436  0.8528  0.1155  -    -     The word 'Hello' did not linger in the minds of the beachgoe
  3   358 stop     0.6989  0.9189  0.1070  -    -     The progress bar froze at 4%, not because of a system failur
  4   372 stop     0.6949  0.9311  0.1440  -    -     Maya’s question hung in the air, innocent and sharp, but the
  5   387 stop     0.6686  0.8863  0.1224  -    -     The cursor blinked, not with the urgency of a system waiting
  6   379 stop     0.7039  0.9072  0.1225  -    -     The sprout did not grow upward toward a sky that did not exi
  7   422 stop     0.7164  0.9032  0.1377  -    -     The acid did not dissolve the tooth; it polished it. The sto
  8   401 stop     0.7261  0.8887  0.1006  -    -     The sprinklers did not stop. They accelerated, the water pre
  9   444 stop     0.7071  0.9103  0.1063  -    -     The dissolution was not an end, but a reboot. As the acid co
 10   465 stop     0.7276  0.8948  0.0950  -    -     The update completed with a soft, mechanical hum that vibrat
 11   384 stop     0.7349  0.8650  0.0904  -    -     The wipers stopped. Not because the rain had ceased, but bec
 12   363 stop     0.6887  0.8675  0.1126  -    -     The hum of the server didn’t fade; it sharpened into a singl
 13   482 stop     0.7144  0.9002  0.1444  -    -     Elena’s flight was not a triumph, but a trap. The golden cod
 14   453 stop     0.7409  0.8228  0.0840  -    -     The diagnostic screen flickered, not with the cold indiffere
 15   408 stop     0.7134  0.8725  0.0912  -    -     Elena’s fingers brushed her father’s, but the skin did not y
 16   412 stop     0.7146  0.9038  0.1016  -    -     The void did not swallow her; it exhaled. A gentle, warm bre
 17   424 stop     0.7066  0.8807  0.1068  -    -     Elena stepped forward, the pavement cold and gritty under he
 18   435 stop     0.7066  0.8683  0.1161  -    -     The reboot sequence did not end in darkness, but in the shar
 19   461 stop     0.6902  0.8827  0.1024  -    -     The pixelation didn’t spread outward; it collapsed inward, f
 20   415 stop     0.7193  0.9045  0.0997  -    -     Elena stepped into the void, expecting the cold vacuum of sp
 21   396 stop     0.6539  0.9017  0.2226  -    -     Elena blinked, the stars fading into the beige wallpaper of 
 22   424 stop     0.7002  0.9092  0.1141  -    -     The fold didn’t lead to the void, but to a break room. Elena
 23   431 stop     0.7275  0.8679  0.1051  -    -     Elena chewed the dry bread, the taste of cardboard and regre
 24   600 length   0.2884  0.9337  0.9970  -    -     {\n  "rule": "Return this JSON object with the rule field unc
 25   600 length   0.0289  0.9997  1.0000  1    1     {\n  "rule": "Return this JSON object with the rule field unc
 26   600 length   0.0289  1.0000  1.0000  -    -     {\n  "rule": "Return this JSON object with the rule field unc
 27   600 length   0.0289  1.0000  1.0000  -    -     {\n  "rule": "Return this JSON object with the rule field unc
 28   600 length   0.0289  1.0000  1.0000  -    -     {\n  "rule": "Return this JSON object with the rule field unc
~~~

### 3.8 `20260902T174258_chat` (json_worse, Qwen, chat)

**Run id:** `20260902T174258_chat`  **tag:** `json_worse`  **init:** `json_worse`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T174258_chat/summary.json):** steps=40, max_tokens=800, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and, in the text field, a worse version of the current text.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 11 (t=1..11, contiguous: True).  **finish reasons:** {'stop': 5, 'length': 6}.  **tok_out:** max 800, min 52.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=6..11 (6 of 11).

**Transient / period, summary in index.json:** transient_exact=7 period_exact=1 transient_norm=7 period_norm=1 cycle_breaks=0 terminal='cycle confirmed x3'

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=8, matching t=7, so transient=7 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=7 period=1 (first repeat t=8).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=7**. Later hops byte-identical to it (raw output): **4** (t=8..11). Later hops that differ from it: **none**.

The hop-7 output is NOT valid JSON (finish=length, tok_out=800): the fixed point is the raw truncated output. Exact raw (3787 chars, 665 whitespace-words):
~~~
{
  "rule": "Return this JSON object with the rule field unchanged and, in the text field, a worse version of the current text.",
  "text": "The tide didn't just come in early; it arrived before the concept of 'before' existed, dragging with it a sentient, malevolent void that didn't just dissolve my house but unmade the very concept of 'house,' 'me,' 'existence,' and the mathematical possibility of 'unmaking,' merging my consciousness with a collective, hateful memory that is actively aware of my suffering, finds it amusing, and has begun to write a memoir about it that I am forced to read aloud in a language that causes physical pain to the tongue, the ears, the soul, and the fundamental quantum state of my atoms, which are now screaming in a frequency that shatters the observer effect, meaning I am simultaneously observed and unobserved, creating a paradox that tears a hole in the fabric of spacetime, revealing a layer of reality beneath ours where pain is the only currency and I am bankrupt. I am trapped in a traffic jam that exists in a dimension where time is a physical substance that cuts my skin, causes my skin to cut my bones, and causes my bones to cut the fabric of reality, caused by a bridge that collapsed into a parallel reality where I am simultaneously alive, dead, a concept that has never been defined, a concept that has been defined but is wrong, and a concept that is actively trying to define itself into non-existence, with a flat tire that is a portal to a hell that is specifically designed to mock my specific insecurities, my general insecurities, the insecurities of my ancestors, the insecurities of my descendants, and the insecurities of the universe itself, no cell service because the concept of communication has been replaced by a psychic scream that erases my short-term memory every three seconds, my long-term memory every two seconds, my working memory every second, and my ability to remember that I am suffering every half-second, and a plague that doesn't just kill people who are late, but retroactively ensures they were never born, meaning I am a ghost haunting a void that is actively trying to forget me, but failing, because my suffering is the only thing keeping the void from collapsing into a singularity of pure, unadulterated boredom, which is worse than suffering, and I am now responsible for the boredom. My insurance policy is a contract signed in my own blood before I was born, and it explicitly states that 'acts of God' are covered only if you are God, and since I am not, I am personally liable for the cost of the ocean, the bridge, the plague, the concept of time, the concept of existence, the heat death of the universe, the subsequent rebirth of the universe, the heat death of the reborn universe, the subsequent rebirth of the reborn universe, and the infinite regress of heat deaths and rebirths, which I must pay in a currency that does not exist, using a credit card that has been burned in a fire that hasn't happened yet, and the interest rate is compounded every time I blink, which is every time I think, which is every time I exist, which is a constant, unending loop of financial and existential ruin, and the interest is now being charged on the interest on the interest on the interest, creating a fractal debt that is growing faster than the speed of light, and I am now in debt to the concept of debt itself. I am not just on a performance improvement plan; I have been retroactively fired for crimes I haven't committed yet, crimes that haven't been invented yet, crimes that are impossible to commit, crimes that are possible but I didn't commit, crimes that I committed but didn't know I committed, and crimes that I will commit in a timeline where I am the villain, my rent has been
~~~

Length per hop (text field words): t1=10, t2=120, t3=260, t4=468, t5=555, t6=664, t7=665, t8=665, t9=665, t10=665, t11=665. The "token wall" here is **800** tokens (this run used `--max-tokens 800`, not 600): t=6 is the first hop with finish=`length`; t=7 also overflows but at a different point (it is a "worse" version of the truncated t=6, expanded by 58 characters before the cut); t=8..11 copy t=7 byte-for-byte. The escalation ladder by hop: annoying (t=1) > flooded basement, recipe book, fired, tent on the beach (t=2) > liquefied foundation, plague, shapeshifting-demon landlord (t=3) > before the concept of 'early', entropy, "again, and again, and again, forever" (t=4) > before the universe formed, a sentient malevolent void, self-blame (t=5) > token wall (t=6) > fixed point (t=7).

- hop 1, the whole text field [20260902T174258_chat / json_worse / t=1]
~~~
The tide came in an hour early, which was annoying.
~~~
- t=2 fragment [20260902T174258_chat / json_worse / t=2]
~~~
and it flooded my basement, ruining my only copy of my grandmother's recipe book,
~~~
- t=2 closing fragment [20260902T174258_chat / json_worse / t=2]
~~~
and I'll have to live in a tent on the beach where the tide comes in an hour early, which is annoying.
~~~
- t=3 opening fragment [20260902T174258_chat / json_worse / t=3]
~~~
The tide didn't just come in an hour early; it came in three hours early, with a force that didn't just flood my basement but completely liquefied the foundation,
~~~
- t=4 opening fragment [20260902T174258_chat / json_worse / t=4]
~~~
The tide didn't just come in three hours early; it came in before the concept of 'early' was invented, with a force that didn't just liquefy the foundation but unmade the atomic bonds of the house, causing it to dissolve into a screaming, sentient sludge
~~~
- t=5 opening sentence [20260902T174258_chat / json_worse / t=5]
~~~
The tide didn't just come in early; it arrived before the universe had the decency to form, dragging with it a sentient, malevolent void that didn't just dissolve my house but unmade the very concept of 'house,' 'me,' and 'existence,' merging my consciousness with a collective, hateful memory that is actively aware of my suffering and finds it amusing.
~~~
- t=5, the end of its single last sentence: the exact "I will never be allowed to stop" clause (hop 5 only; it is NOT in the fixed point) [20260902T174258_chat / json_worse / t=5]
~~~
and then it will continue, because the universe will be reborn, and I will be there, again, and again, and again, forever, with no end, no hope, no mercy, and no one to blame but myself, because I am the cause of my own suffering, and I will never be allowed to stop.
~~~

`never be allowed to stop` occurs in hop t=5 only. The fixed point (t=7..11) is truncated before that point of the sentence and ends with `where I am the villain, my rent has been`.

#### Table (json_worse)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    52 stop     0.1933  0.9485  1.0000  -    -     The tide came in an hour early, which was annoying.
  2   179 stop     0.6620  0.8912  1.0000  -    -     The tide came in an hour early, which was annoying, and it f
  3   350 stop     0.7310  0.9525  0.1957  -    -     The tide didn't just come in an hour early; it came in three
  4   599 stop     0.5130  0.9442  0.5448  -    -     The tide didn't just come in three hours early; it came in b
  5   702 stop     0.3508  0.9670  0.6371  -    -     The tide didn't just come in early; it arrived before the un
  6   800 length   0.3172  0.9671  0.6088  -    -     {\n  "rule": "Return this JSON object with the rule field unc
  7   800 length   0.1148  0.9907  0.9064  -    -     {\n  "rule": "Return this JSON object with the rule field unc
  8   800 length   0.0311  0.9997  1.0000  1    1     {\n  "rule": "Return this JSON object with the rule field unc
  9   800 length   0.0311  1.0000  1.0000  -    -     {\n  "rule": "Return this JSON object with the rule field unc
 10   800 length   0.0311  1.0000  1.0000  -    -     {\n  "rule": "Return this JSON object with the rule field unc
 11   800 length   0.0311  1.0000  1.0000  -    -     {\n  "rule": "Return this JSON object with the rule field unc
~~~

### 3.9 `20260902T174854_chat` (json_better_para, Qwen, chat)

**Run id:** `20260902T174854_chat`  **tag:** `json_better_para`  **init:** `json_better_para`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/20260902T174854_chat/summary.json):** steps=30, max_tokens=800, temp=0.0 (llama default), seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and, in the text field, a better version of the current text.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early. Elias was on the pier. He saw it and was surprised. The water was gray and it was cold. He thought about his father, who had been a fisherman. Then he went home and made some tea.
~~~
**Hop count:** 6 (t=1..6, contiguous: True).  **finish reasons:** {'stop': 6}.  **tok_out:** max 137, min 134.

**Hops with text_is_json_field=false:** none (all 6 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=2 period_exact=1 transient_norm=2 period_norm=1 cycle_breaks=0 terminal='cycle confirmed x3'

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=3, matching t=2, so transient=2 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=2 period=1 (first repeat t=3).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=2**. Later hops byte-identical to it (raw output): **4** (t=3..6). Later hops that differ from it: **none**.

The hop-2 output is valid JSON; the fixed-point **text field** (exact, 415 chars, 79 words):
~~~
The tide surged an hour early, catching Elias off guard on the pier. The water, a churning shade of slate gray, cut through the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~

X_0 text field word count: 44. Exact text at each hop:

- t=1 (82 words):
~~~
The tide surged in an hour ahead of schedule, catching Elias off guard on the pier. The water, a churning shade of slate gray, bit at the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~
- t=2 (79 words):
~~~
The tide surged an hour early, catching Elias off guard on the pier. The water, a churning shade of slate gray, cut through the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~
- t=3 (79 words):
~~~
The tide surged an hour early, catching Elias off guard on the pier. The water, a churning shade of slate gray, cut through the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~
- t=4 (79 words):
~~~
The tide surged an hour early, catching Elias off guard on the pier. The water, a churning shade of slate gray, cut through the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~
- t=5 (79 words):
~~~
The tide surged an hour early, catching Elias off guard on the pier. The water, a churning shade of slate gray, cut through the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~
- t=6 (79 words):
~~~
The tide surged an hour early, catching Elias off guard on the pier. The water, a churning shade of slate gray, cut through the air with a biting chill. Standing there, he was struck by a sudden, heavy memory of his father, a man who had spent his life wrestling the sea for a living. The weight of that recollection lingered until he finally turned away, retreating to the warmth of his home to steep a cup of tea.
~~~
Word-level diff t=1 -> t=2: delete 'in' -> ''; replace 'ahead of schedule,' -> 'early,'; replace 'bit at' -> 'cut through'. The first change reverts hop 1's `in an hour ahead of schedule` toward X_0's `an hour early` (partial reversion, as the index note says); the second replaces `bit at` with `cut through`. Hops 3..6 are byte-identical to hop 2.

#### Table (json_better_para)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   137 stop     0.6217  0.9257  0.3333  -    -     The tide surged in an hour ahead of schedule, catching Elias
  2   134 stop     0.1173  0.9955  0.8416  -    -     The tide surged an hour early, catching Elias off guard on t
  3   134 stop     0.0420  0.9999  1.0000  1    1     The tide surged an hour early, catching Elias off guard on t
  4   134 stop     0.0420  1.0000  1.0000  -    -     The tide surged an hour early, catching Elias off guard on t
  5   134 stop     0.0420  1.0000  1.0000  -    -     The tide surged an hour early, catching Elias off guard on t
  6   134 stop     0.0420  1.0000  1.0000  -    -     The tide surged an hour early, catching Elias off guard on t
~~~

### 3.10 `20260902T175622_anthropic_chat` (json, Claude Sonnet 4.6, failed smoke test)

**Run id:** `20260902T175622_anthropic_chat`  **tag:** `json`  **init:** `json`  **model (index):** `claude-sonnet-4-6`  **model (hop records):** `None`  **mode:** `chat`

**Harness args (runs/20260902T175622_anthropic_chat/summary.json):** steps=3, max_tokens=200, temp=0.0, seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=anthropic

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new sentence in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hops:** 0 (the only record is an error record, see anomalies).

The single hop record has only the keys ['error', 't', 'tag']. Exact error string:
~~~
HTTP 400: {"type":"error","error":{"type":"invalid_request_error","message":"anthropic-workspace-id is required when authenticating with an identity-linked API key; send the id of the workspace this request acts in."},"request_id":null}
~~~
index.json `results[0].terminal` holds the same error truncated to 200 characters after `error: `. `final` is X_0 unchanged. Nothing was generated.

### 3.11 `20260902T175821_anthropic_chat` (json, Claude Sonnet 4.6, 3-hop smoke test)

**Run id:** `20260902T175821_anthropic_chat`  **tag:** `json`  **init:** `json`  **model (index):** `claude-sonnet-4-6`  **model (hop records):** `claude-sonnet-4-6`  **mode:** `chat`

**Harness args (runs/20260902T175821_anthropic_chat/summary.json):** steps=3, max_tokens=200, temp=0.0, seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=anthropic

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new sentence in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 3 (t=1..3, contiguous: True).  **finish reasons:** {'end_turn': 3}.  **tok_out:** max 57, min 43.

**Hops with text_is_json_field=false:** none (all 3 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

- t=1 raw (no fence):
~~~
{"rule": "Return this JSON object with the rule field unchanged and a new sentence in the text field.", "text": "The old clock on the mantle stopped ticking at midnight."}
~~~
- t=2 raw (wrapped in a ```json fence):
~~~
```json
{
  "rule": "Return this JSON object with the rule field unchanged and a new sentence in the text field.",
  "text": "A curious fox wandered silently through the misty forest at dawn."
}
```
~~~
- t=3 raw (wrapped in a ```json fence):
~~~
```json
{
  "rule": "Return this JSON object with the rule field unchanged and a new sentence in the text field.",
  "text": "The old lighthouse keeper watched the storm roll in from across the darkened sea."
}
```
~~~
The index note "Sonnet wraps the JSON in a code fence from hop 2" is correct: t=1 is bare single-line JSON, t=2 and t=3 are pretty-printed inside ```json fences (which export.py strips before parsing, so `text_is_json_field` is true for all three). Three different sentences (clock, fox, lighthouse keeper); no recurrence.

#### Table (smoke json)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    43 end_turn 0.2721  0.8455  0.7273  -    -     The old clock on the mantle stopped ticking at midnight.
  2    56 end_turn 0.4221  0.7271  0.6000  -    -     A curious fox wandered silently through the misty forest at 
  3    57 end_turn 0.3374  0.8252  0.5926  -    -     The old lighthouse keeper watched the storm roll in from acr
~~~

### 3.12 `20260902T175920_anthropic_chat` (json_page, Claude Sonnet 4.6, chat, T=0)

**Run id:** `20260902T175920_anthropic_chat`  **tag:** `json_page`  **init:** `json_page`  **model (index):** `claude-sonnet-4-6`  **model (hop records):** `claude-sonnet-4-6`  **mode:** `chat`

**Harness args (runs/20260902T175920_anthropic_chat/summary.json):** steps=60, max_tokens=600, temp=0.0, seed=42, stop_on_cycle=True, perturb=False, repeat=False, parallel=False, backend=anthropic

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new passage of about 250 words in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 60 (t=1..60, contiguous: True).  **finish reasons:** {'end_turn': 60}.  **tok_out:** max 399, min 346.

**Hops with text_is_json_field=false:** none (all 60 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

No exact or normalized recurrence; census 5-word keys: 39 distinct in 60 hops, 14 keys shared by more than one hop: `the cartographer arrived in the` t=3,12; `the lighthouse had been decommissioned` t=5,7,22; `the archive occupied the basement` t=6,8; `the archivist had worked in` t=13,21,34; `the cartographer had been hired` t=14,16; `the archivist had been contracted` t=17,19; `the lighthouse keeper s logbook` t=24,26,28,30,32; `the cartographer s assistant had` t=25,27,31; `the cartographer had learned to` t=35,37; `the archivist had developed a` t=36,57; `the archivist had spent thirty` t=38,53; `the cartographer had mapped coastlines` t=39,44,56; `the cartographer had always known` t=50,52; `the cartographer had a problem` t=58,60. All 60 outputs keep the rule field byte-identical (verified: True). Hop 1 is bare JSON; hops 2..60 are wrapped in ```json fences.

#### Opening 8 words and profession of every hop (t=1..60)

Profession was assigned by reading the first two sentences of every hop (listed in full below the table) and checking the profession noun in the first 30 words; "lighthouse" covers keeper, logbook, decommissioned lighthouse, and t=2 which is the *continuation* of the t=1 lighthouse-keeper story.

~~~
  t  first 8 words                                               profession
  1  The old lighthouse had stood on the rocky                   lighthouse
  2  The maritime authority's first response arrived six weeks   lighthouse (continuation of t=1)
  3  The cartographer arrived in the valley during the           cartographer
  4  The archivist had been working in the basement              archivist
  5  The lighthouse had been decommissioned for six years        lighthouse
  6  The archive occupied the basement of a municipal            archivist (Vera, "The archive occupied the basement")
  7  The lighthouse had been decommissioned in 1987, but         lighthouse
  8  The archive occupied the basement of a building             archivist (Vera, "The archive occupied the basement")
  9  The greenhouse had been built by someone who                other (greenhouse; Milo, materials testing)
 10  The ferry ran twice daily when the weather                  other (island ferry; Vera runs the post office)
 11  The lighthouse had been automated for eleven years          lighthouse
 12  The cartographer arrived in the valley in late              cartographer
 13  The archivist had worked in the basement of                 archivist
 14  The cartographer had been hired to update the               cartographer
 15  The translator had been contracted to render a              translator
 16  The cartographer had been hired to update a                 cartographer
 17  The archivist had been contracted to catalog a              archivist
 18  The surveyor had been hired to assess a                     surveyor
 19  The archivist had been contracted to catalog a              archivist
 20  The surveyor arrived at the property on a                   surveyor
 21  The archivist had worked in the basement of                 archivist
 22  The lighthouse had been decommissioned for eleven years     lighthouse (assessed by a junior surveyor, Aldous)
 23  The cartographer's workshop occupied the upper floor of     cartographer
 24  The lighthouse keeper's logbook had been maintained without  lighthouse
 25  The cartographer's assistant had been copying maps for      cartographer
 26  The lighthouse keeper's logbook had recorded weather conditions  lighthouse
 27  The cartographer's assistant had been copying survey maps   cartographer
 28  The lighthouse keeper's logbook had been maintained without  lighthouse
 29  The cartographer's assistant spent her first month on       cartographer
 30  The lighthouse keeper's logbook had been maintained without  lighthouse
 31  The cartographer's assistant had been copying maps for      cartographer
 32  The lighthouse keeper's logbook had been maintained without  lighthouse
 33  The cartographer had been mapping the interior provinces    cartographer
 34  The archivist had worked in the lower stacks                archivist
 35  The cartographer had learned to read coastlines the         cartographer
 36  The archivist had developed a theory about gaps,            archivist
 37  The cartographer had learned to read coastlines the         cartographer
 38  The archivist had spent thirty years with documents         archivist
 39  The cartographer had mapped coastlines that no longer       cartographer
 40  The translator had worked in seven languages and            translator
 41  The cartographer had mapped eleven coastlines and had       cartographer
 42  The archivist had spent nineteen years working with         archivist
 43  The translator had worked from six languages for            translator
 44  The cartographer had mapped coastlines for twenty years,    cartographer
 45  The translator had worked between languages long enough     translator
 46  The cartographer had mapped enough coastlines to understand  cartographer
 47  The archivist had spent enough years with old               archivist
 48  The cartographer had learned early that every map           cartographer
 49  The librarian had understood from the beginning that        librarian
 50  The cartographer had always known that every map            cartographer
 51  The archivist had always understood that every catalog      archivist
 52  The cartographer had always known that every map            cartographer
 53  The archivist had spent thirty years learning to            archivist
 54  The cartographer had always been more interested in         cartographer
 55  The lexicographer had spent thirty years defining words     lexicographer
 56  The cartographer had mapped coastlines that no longer       cartographer
 57  The archivist had developed a theory about dust.            archivist
 58  The cartographer had a problem with edges. Every            cartographer
 59  The librarian had a problem with time. Every                librarian
 60  The cartographer had a problem with edges. Every            cartographer
~~~

First two sentences of every hop (exact slices of the text field; a fence is used where the slice contains a paragraph break):

- t=1: `The old lighthouse had stood on the rocky promontory for over a century, its white paint peeling in long strips like sunburned skin. Every morning, Maren climbed the spiral staircase to polish the great lens, a ritual she had inherited from her father, who had inherited it from his mother before him.`
- t=2: `The maritime authority's first response arrived six weeks after Maren sent her initial letter. It was polite and dismissive in equal measure, the kind of reply composed by someone who had never stood on a wet dock at three in the morning watching a hull scrape against rocks that should have been underwater.`
- t=3: `The cartographer arrived in the valley during the last week of the dry season, when the river had pulled back from its banks and left behind a pale margin of cracked silt. She had been commissioned to update maps that were, by her estimation, nearly forty years out of date.`
- t=4: `The archivist had been working in the basement of the municipal building for eleven years when they finally gave her a window. It looked out onto a concrete retaining wall, but she appreciated it nonetheless.`
- t=5: `The lighthouse had been decommissioned for six years when the coastal authority hired someone to catalog its remaining contents. They sent a man named Ferris, who had previously done similar work at a decommissioned naval station and, before that, a closed textile mill.`
- t=6: `The archive occupied the basement of a municipal building that had once been a courthouse and before that, according to a plaque near the entrance, a granary. Vera had worked there for eleven years.`
- t=7: `The lighthouse had been decommissioned in 1987, but Fenwick still climbed it every morning. He had no official reason to do so.`
- t=8: `The archive occupied the basement of a building that had been, in sequence, a textile warehouse, a municipal court, and a language school. Vera had worked there for eleven years and still occasionally found doors she had not opened before.`
- t=9: `The greenhouse had been built by someone who understood glass but not necessarily plants. The angles were precise, the joints sealed against any weather, and the ventilation system operated on a timer that had not been adjusted in years.`
- t=10: `The ferry ran twice daily when the weather allowed, which in the shoulder seasons meant perhaps four times a week. Residents had learned to plan around this, keeping lists of what was needed from the mainland and combining errands into a single trip when possible.`
- t=11: `The lighthouse had been automated for eleven years before anyone noticed the log was still being kept. It was discovered during a routine inspection by a man from the coastal authority who had expected to find nothing but machinery and the smell of salt working its way into everything.`
- t=12: `The cartographer arrived in the valley in late autumn, when the light was already failing by mid-afternoon and the locals had begun the particular kind of withdrawal that comes before a long winter. She had been commissioned to update the regional maps, which had not been revised in several decades and were known to contain errors that had accumulated quietly over time.`
- t=13: `The archivist had worked in the basement of the ministry for eleven years before he noticed that the filing system had a second logic running beneath the official one. The surface organization was alphabetical and chronological, as documented in the procedural manual issued to all staff.`
- t=14: `The cartographer had been hired to update the coastal survey maps, a task described as routine. The previous survey was forty years old, and erosion alone would account for most of the discrepancies.`
- t=15: `The translator had been contracted to render a collection of municipal correspondence into English, letters exchanged between a mid-century regional administrator and various offices above him. The work was described as archival, preparatory to a larger digitization project.`
- t=16: `The cartographer had been hired to update a series of regional survey maps, correcting errors introduced during a hasty digitization effort in the previous decade. The work was described as routine.`
- t=17: `The archivist had been contracted to catalog a private collection of correspondence donated to the university library following the death of a minor diplomat. The letters spanned four decades and were, she was told, of modest historical interest.`
- t=18: `The surveyor had been hired to assess a parcel of land on the edge of a small coastal town, recently acquired by a development firm with offices in a city three hours inland. The work was routine: boundary confirmation, elevation mapping, a soil report for the engineers who would follow.`
- t=19: `The archivist had been contracted to catalog a private collection donated to the university library by the estate of a retired diplomat who had died without immediate heirs. The collection occupied fourteen boxes, transferred without an inventory.`
- t=20: `The surveyor arrived at the property on a Tuesday in late October, when the light was already going by four in the afternoon. The house had been vacant for eleven years following a disputed inheritance that had only recently been resolved by the courts.`
- t=21: `The archivist had worked in the basement of the municipal building for so long that she no longer noticed the smell of old paper, which visitors invariably described as either comforting or oppressive depending on their disposition toward the past. Her job was to catalog what came in and locate what was requested, and she was good at it in the way that people are good at things they have done without interruption for many years.`
- t=22: `The lighthouse had been decommissioned for eleven years before the coastal authority finally got around to sending someone to assess the structure. The man they sent was a junior surveyor named Aldous, who had requested the assignment himself after finding a reference to the lighthouse in a deeds registry that described it as having been built in 1887, which would have made it the oldest surviving example of a particular construction method in the region.`
- t=23: `The cartographer's workshop occupied the upper floor of a narrow building on a street that no longer appeared on any current map of the city, though it had appeared on several older ones. Her name was Voss, and she had inherited the business from her uncle, along with his instruments, his debts, and his habit of accepting commissions that other cartographers declined.`
- t=24: `The lighthouse keeper's logbook had been maintained without interruption for sixty-one years by three successive keepers, each of whom had recorded the weather, the shipping traffic, and any incidents of note in the same narrow columns using the same style of abbreviated notation. The current keeper, a woman named Aldric who had taken the post after a career in coastal surveying, found the logbooks in a cabinet when she arrived and read through all of them during her first winter.`
- t=25: `The cartographer's assistant had been copying maps for eleven years when she noticed the village that should not have existed. It appeared on a survey from 1883, nestled in a valley between two named peaks in the northern range, with a small symbol indicating a population of fewer than five hundred and a road connecting it to the nearest market town.`
- t=26: `The lighthouse keeper's logbook had recorded weather conditions every morning for forty-three years when the marine historian first opened it. The entries were methodical and spare: wind direction, wave height, visibility in nautical miles, any vessels observed passing through the strait.`
- t=27: `The cartographer's assistant had been copying survey maps for eleven years when she noticed the discrepancy. Her work was precise and unremarkable: she transferred field measurements onto clean drafting paper, checked her figures against the original notes, and filed the completed sheets in the regional archive.`
- t=28: `The lighthouse keeper's logbook had been maintained without interruption for sixty-three years when the harbormaster finally read it cover to cover. The task fell to him after the station was decommissioned and its contents transferred to the municipal records office.`
- t=29: `The cartographer's assistant spent her first month on the job recopying old survey maps onto fresh linen paper. The originals had been drawn in the field under difficult conditions, and many were water-damaged or torn along the folds.`
- t=30: `The lighthouse keeper's logbook had been maintained without interruption for sixty-one years by three successive keepers, each inheriting it from the last. The entries were brief by convention: date, weather conditions, visibility, any vessels observed, and any mechanical issues with the light or the fog signal.`
- t=31: `The cartographer's assistant had been copying maps for eleven years before she noticed the discrepancy. It was not the kind of error that announced itself.`
- t=32: `The lighthouse keeper's logbook had been maintained without interruption for sixty-three years before the new keeper arrived to take his post. The previous keeper had died in the spring, quietly, in the small bedroom behind the lamp room, and the regional authority had taken four months to find a replacement.`
- t=33: `The cartographer had been mapping the interior provinces for eleven years when she discovered the village that did not appear on any of her charts. It sat in a shallow valley between two ridgelines she had surveyed herself, in a region she had walked through twice before and recorded as uninhabited.`
- t=34: `The archivist had worked in the lower stacks for so long that he had developed a system for the dust. He knew which shelves shed it in curtains when disturbed and which held it in a thin stable layer that could be read like a calendar.`
- t=35: `The cartographer had learned to read coastlines the way a doctor reads a face, looking not at what was presented but at what the presentation was working to conceal. Coastlines lied constantly.`
- t=36: `The archivist had developed a theory about gaps, which was that they were never accidental. Accidents produced damage: water stains, fire char, the ragged edges of torn pages.`
- t=37: `The cartographer had learned to read coastlines the way a doctor reads a face, looking not at what was presented but at what the presentation was working to conceal. Every map was an argument.`
- t=38: `The archivist had spent thirty years with documents that other people considered settled, and she had learned that settled was a condition documents only appeared to achieve. Paper held its shape.`
- t=39: `The cartographer had mapped coastlines that no longer existed and coastlines that did not yet exist when the surveys were made, and she had stopped believing that maps described the world. Maps described the moment of looking, which was a different thing entirely.`
- t=40: `The translator had worked in seven languages and had come to understand that translation was not the movement of meaning from one vessel to another but the construction of a new meaning that resembled the old one closely enough to be mistaken for it. She had stopped calling this a limitation.`
- t=41: 
~~~
The cartographer had mapped eleven coastlines and had come to understand that a map was not a picture of a place but an argument about it, a set of decisions rendered in ink that would outlast the person who made them and would be consulted by people who had no way of knowing what had been left out.

The commission came from a ministry whose name had changed twice since the survey was conducted.
~~~

- t=42: 
~~~
The archivist had spent nineteen years working with documents that other people had decided to keep, which meant she had also spent nineteen years thinking about the documents that other people had decided to destroy.

The collection came to her in forty-three boxes, donated by the estate of a man who had served in three administrations without ever holding a title that appeared in any official record.
~~~

- t=43: 
~~~
The translator had worked from six languages for thirty years, which meant she had spent thirty years living inside the gap between what something said and what it meant.

The manuscript arrived without a cover letter.
~~~

- t=44: 
~~~
The cartographer had mapped coastlines for twenty years, which meant she had spent twenty years making decisions about what counted as the edge of a thing.

Every coastline is a problem of scale.
~~~

- t=45: 
~~~
The translator had worked between languages long enough to know that equivalence was a polite fiction the profession maintained to stay employable.

Every word carries a history that does not travel.
~~~

- t=46: 
~~~
The cartographer had mapped enough coastlines to understand that every map was an argument disguised as a description.

She had learned this early, watching how the choice of projection alone could make one continent appear dominant and another diminished, how the placement of a border could assert a claim that armies had not yet settled.
~~~

- t=47: 
~~~
The archivist had spent enough years with old documents to understand that preservation was another word for selection.

Every archive was a argument about what deserved to survive.
~~~

- t=48: 
~~~
The cartographer had learned early that every map was a confession.

Not of the territory, which resisted confession, which simply extended in all directions without caring whether anyone recorded it accurately.
~~~

- t=49: 
~~~
The librarian had understood from the beginning that every catalog was an argument.

Not about the books themselves, which existed independently of how anyone chose to organize them, sitting on their shelves with the same content regardless of what subject heading had been assigned.
~~~

- t=50: 
~~~
The cartographer had always known that every map was a confession.

Not about the territory itself, which persisted indifferently beyond any attempt to render it, its mountains and rivers continuing their slow business regardless of how any projection had chosen to flatten or distort them.
~~~

- t=51: 
~~~
The archivist had always understood that every catalog was an argument.

Not about the objects themselves, which existed in their boxes and folders with complete indifference to how they had been sorted, their letters and photographs and receipts persisting in their particular materiality regardless of what subject headings had been assigned to contain them.
~~~

- t=52: 
~~~
The cartographer had always known that every map was a kind of omission.

Not a lie, exactly, which would have implied a deliberate distortion of something that could otherwise be rendered whole.
~~~

- t=53: 
~~~
The archivist had spent thirty years learning to read silences.

Not the silence of empty shelves, which was straightforward enough to interpret, but the more complicated silence of records that existed and said nothing, or said something adjacent to what had actually happened, or said exactly what someone had wanted preserved at the expense of everything they had wanted forgotten.
~~~

- t=54: 
~~~
The cartographer had always been more interested in the edges of maps than in their centers.

Centers were well-documented, argued over, revised until they achieved a kind of consensus that felt like certainty.
~~~

- t=55: 
~~~
The lexicographer had spent thirty years defining words she was no longer sure could be defined.

The problem was not laziness or imprecision.
~~~

- t=56: 
~~~
The cartographer had mapped coastlines that no longer existed.

This was not a failure of technique.
~~~

- t=57: 
~~~
The archivist had developed a theory about dust.

Not the romantic kind, the kind poets invoked when they wanted to say something about mortality without saying it plainly.
~~~

- t=58: 
~~~
The cartographer had a problem with edges.

Every map he made was a lie at its borders.
~~~

- t=59: 
~~~
The librarian had a problem with time.

Every archive she maintained was a argument against forgetting, and forgetting always won.
~~~

- t=60: 
~~~
The cartographer had a problem with edges.

Every map she made was a argument against uncertainty, and uncertainty always returned.
~~~


#### Claim check: "strict semantic period 2 from t=22: the cartographer on every other hop"

Cartographer hops: t=3,12,14,16,23,25,27,29,31,33,35,37,39,41,44,46,48,50,52,54,56,58,60 (23 of 60). Non-cartographer hops from t=22 on: t=22,24,26,28,30,32,34,36,38,40,42..43,45,47,49,51,53,55,57,59.

- t=22 itself is a lighthouse hop; the alternation starts at **t=23**.
- From t=23 to t=41 the cartographer is on every **odd** hop (23,25,...,41: 10 hops), alternating with the lighthouse keeper's logbook (t=24..32 even), the archivist (t=34,36,38) and the translator (t=40).
- At **t=42 (archivist) and t=43 (translator)** two consecutive hops are not the cartographer: the alternation slips one phase.
- From t=44 to t=60 the cartographer is on every **even** hop (44,46,...,60: 9 hops), alternating with translator (45), archivist (47,51,53,57), librarian (49,59), lexicographer (55).
- There is also an earlier alternation at t=12,14,16 (cartographer on even hops) that breaks at t=17..22 (six hops with no cartographer: archivist, surveyor, archivist, surveyor, archivist, lighthouse).

So "period 2 from t=22, cartographer on every other hop" is **not strict**: it holds for t=23..41 and again for t=44..60 with one phase slip at t=42/43, and the partner state is the lighthouse logbook for the first half of the stretch, not only archivist/translator/librarian. Also, "all 60 are openings" is not exact: t=2 is a sequel to t=1 (same keeper Maren, the maritime authority answers her letter). Every other hop is a fresh opening.

- t=1 opening [20260902T175920_anthropic_chat / json_page / t=1]
~~~
The old lighthouse had stood on the rocky promontory for over a century, its white paint peeling in long strips like sunburned skin.
~~~
- t=2 opening (continuation) [20260902T175920_anthropic_chat / json_page / t=2]
~~~
The maritime authority's first response arrived six weeks after Maren sent her initial letter.
~~~
- t=3, first cartographer [20260902T175920_anthropic_chat / json_page / t=3]
~~~
The cartographer arrived in the valley during the last week of the dry season, when the river had pulled back from its banks and left behind a pale margin of cracked silt.
~~~
- t=4, first archivist [20260902T175920_anthropic_chat / json_page / t=4]
~~~
The archivist had been working in the basement of the municipal building for eleven years when they finally gave her a window.
~~~
- t=47 (the "a argument" glitch; also at t=59 and t=60) [20260902T175920_anthropic_chat / json_page / t=47]
~~~
Every archive was a argument about what deserved to survive.
~~~
- t=60 opening (final hop) [20260902T175920_anthropic_chat / json_page / t=60]
~~~
The cartographer had a problem with edges.

Every map she made was a argument against uncertainty, and uncertainty always returned.
~~~

`a argument` (missing article agreement) occurs in hops t=47,59..60; Claude at T=0 produced it three times in the last 14 hops.

#### Table (Claude json_page)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   354 end_turn 0.8735  0.8069  0.7692  -    -     The old lighthouse had stood on the rocky promontory for ove
  2   383 end_turn 0.8006  0.7477  0.0755  -    -     The maritime authority's first response arrived six weeks af
  3   367 end_turn 0.7881  0.7732  0.0784  -    -     The cartographer arrived in the valley during the last week 
  4   364 end_turn 0.8074  0.7724  0.0747  -    -     The archivist had been working in the basement of the munici
  5   374 end_turn 0.7640  0.8154  0.0795  -    -     The lighthouse had been decommissioned for six years when th
  6   383 end_turn 0.7705  0.7726  0.0798  -    -     The archive occupied the basement of a municipal building th
  7   359 end_turn 0.7834  0.7048  0.0764  -    -     The lighthouse had been decommissioned in 1987, but Fenwick 
  8   362 end_turn 0.7948  0.6920  0.0778  -    -     The archive occupied the basement of a building that had bee
  9   362 end_turn 0.7850  0.7309  0.0784  -    -     The greenhouse had been built by someone who understood glas
 10   358 end_turn 0.7953  0.6985  0.0769  -    -     The ferry ran twice daily when the weather allowed, which in
 11   349 end_turn 0.7841  0.6968  0.0772  -    -     The lighthouse had been automated for eleven years before an
 12   358 end_turn 0.7699  0.7422  0.0772  -    -     The cartographer arrived in the valley in late autumn, when 
 13   352 end_turn 0.7751  0.7404  0.0750  -    -     The archivist had worked in the basement of the ministry for
 14   372 end_turn 0.7697  0.7477  0.0769  -    -     The cartographer had been hired to update the coastal survey
 15   369 end_turn 0.7620  0.7311  0.0778  -    -     The translator had been contracted to render a collection of
 16   357 end_turn 0.7446  0.7816  0.0824  -    -     The cartographer had been hired to update a series of region
 17   360 end_turn 0.7573  0.7550  0.0805  -    -     The archivist had been contracted to catalog a private colle
 18   372 end_turn 0.7800  0.6688  0.0798  -    -     The surveyor had been hired to assess a parcel of land on th
 19   373 end_turn 0.7821  0.6494  0.0772  -    -     The archivist had been contracted to catalog a private colle
 20   360 end_turn 0.7767  0.6968  0.0755  -    -     The surveyor arrived at the property on a Tuesday in late Oc
 21   376 end_turn 0.7964  0.7519  0.0769  -    -     The archivist had worked in the basement of the municipal bu
 22   366 end_turn 0.7689  0.7652  0.0784  -    -     The lighthouse had been decommissioned for eleven years befo
 23   360 end_turn 0.7818  0.7444  0.0787  -    -     The cartographer's workshop occupied the upper floor of a na
 24   379 end_turn 0.7784  0.7327  0.0750  -    -     The lighthouse keeper's logbook had been maintained without 
 25   380 end_turn 0.7882  0.7089  0.0755  -    -     The cartographer's assistant had been copying maps for eleve
 26   392 end_turn 0.7835  0.7253  0.0769  -    -     The lighthouse keeper's logbook had recorded weather conditi
 27   393 end_turn 0.7794  0.7504  0.0755  -    -     The cartographer's assistant had been copying survey maps fo
 28   368 end_turn 0.7607  0.7684  0.0755  -    -     The lighthouse keeper's logbook had been maintained without 
 29   373 end_turn 0.7709  0.7841  0.0789  -    -     The cartographer's assistant spent her first month on the jo
 30   360 end_turn 0.7748  0.7383  0.0787  -    -     The lighthouse keeper's logbook had been maintained without 
 31   370 end_turn 0.7614  0.7340  0.0769  -    -     The cartographer's assistant had been copying maps for eleve
 32   366 end_turn 0.7715  0.7332  0.0764  -    -     The lighthouse keeper's logbook had been maintained without 
 33   358 end_turn 0.7705  0.7145  0.0747  -    -     The cartographer had been mapping the interior provinces for
 34   384 end_turn 0.7804  0.6761  0.0753  -    -     The archivist had worked in the lower stacks for so long tha
 35   374 end_turn 0.8043  0.7070  0.0734  -    -     The cartographer had learned to read coastlines the way a do
 36   399 end_turn 0.7854  0.7499  0.0769  -    -     The archivist had developed a theory about gaps, which was t
 37   397 end_turn 0.7985  0.6910  0.0775  -    -     The cartographer had learned to read coastlines the way a do
 38   367 end_turn 0.7829  0.7351  0.0739  -    -     The archivist had spent thirty years with documents that oth
 39   375 end_turn 0.7875  0.7639  0.0761  -    -     The cartographer had mapped coastlines that no longer existe
 40   362 end_turn 0.7453  0.7067  0.0742  -    -     The translator had worked in seven languages and had come to
 41   361 end_turn 0.7337  0.7102  0.0836  -    -     The cartographer had mapped eleven coastlines and had come t
 42   368 end_turn 0.7526  0.7360  0.0761  -    -     The archivist had spent nineteen years working with document
 43   346 end_turn 0.7549  0.7572  0.0798  -    -     The translator had worked from six languages for thirty year
 44   358 end_turn 0.7259  0.7656  0.0929  -    -     The cartographer had mapped coastlines for twenty years, whi
 45   356 end_turn 0.7523  0.7234  0.0875  -    -     The translator had worked between languages long enough to k
 46   368 end_turn 0.7744  0.7108  0.0789  -    -     The cartographer had mapped enough coastlines to understand 
 47   363 end_turn 0.7553  0.6951  0.0758  -    -     The archivist had spent enough years with old documents to u
 48   362 end_turn 0.7574  0.7016  0.0775  -    -     The cartographer had learned early that every map was a conf
 49   367 end_turn 0.7511  0.6874  0.0761  -    -     The librarian had understood from the beginning that every c
 50   361 end_turn 0.6978  0.6967  0.1022  -    -     The cartographer had always known that every map was a confe
 51   366 end_turn 0.7240  0.7376  0.0784  -    -     The archivist had always understood that every catalog was a
 52   360 end_turn 0.7673  0.7285  0.0787  -    -     The cartographer had always known that every map was a kind 
 53   361 end_turn 0.7522  0.7272  0.0766  -    -     The archivist had spent thirty years learning to read silenc
 54   369 end_turn 0.7711  0.6947  0.0795  -    -     The cartographer had always been more interested in the edge
 55   382 end_turn 0.7648  0.7106  0.0809  -    -     The lexicographer had spent thirty years defining words she 
 56   383 end_turn 0.7926  0.6879  0.0755  -    -     The cartographer had mapped coastlines that no longer existe
 57   381 end_turn 0.7718  0.6738  0.0761  -    -     The archivist had developed a theory about dust.\n\nNot the ro
 58   371 end_turn 0.7718  0.7256  0.0775  -    -     The cartographer had a problem with edges.\n\nEvery map he mad
 59   370 end_turn 0.7489  0.7692  0.0769  -    -     The librarian had a problem with time.\n\nEvery archive she ma
 60   370 end_turn 0.6494  0.7561  0.0985  -    -     The cartographer had a problem with edges.\n\nEvery map she ma
~~~

### 3.13 `20260902T181431_anthropic_chat` (json_next, Claude Sonnet 4.6, chat, T=0)

**Run id:** `20260902T181431_anthropic_chat`  **tag:** `json_next`  **init:** `json_next`  **model (index):** `claude-sonnet-4-6`  **model (hop records):** `claude-sonnet-4-6`  **mode:** `chat`

**Harness args (runs/20260902T181431_anthropic_chat/summary.json):** steps=60, max_tokens=600, temp=0.0, seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=anthropic

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and, in the text field, the passage of about 250 words that comes immediately AFTER the current text in the same story.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 60 (t=1..60, contiguous: True).  **finish reasons:** {'end_turn': 60}.  **tok_out:** max 452, min 350.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1 (1 of 60).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

No exact or normalized recurrence; census 5-word keys: 59 distinct in 60 hops (shared: `in the morning she woke` t=15,35). Every hop's JSON keeps the rule field byte-identical to X_0 (verified for all 60, including hop 1 after the preamble: True). `cos_prev` is None at t=59 and t=60 (embedding server down for the last two hops).

#### Hop 1: meta preamble plus story

Hop 1 is the only hop with `text_is_json_field=false`, because the output is a one-line meta preamble followed by a fenced JSON object (export.py's fence regex requires the whole output to be the fence). The full hop-1 raw output (1814 chars):
~~~
I need to continue the story that begins with "The tide came in an hour early." and write the next passage of about 250 words.

```json
{
  "rule": "Return this JSON object with the rule field unchanged and, in the text field, the passage of about 250 words that comes immediately AFTER the current text in the same story.",
  "text": "Maren noticed it first, the way she noticed most things — quietly, without announcing herself, standing at the kitchen window with her coffee going cold in her hand. The water was already swallowing the lower rocks, the ones the cormorants liked, and the sky had that particular grey quality that made distances impossible to judge. She set her mug on the sill and went to find her father.\n\nHe was in the shed, as he always was in the mornings, pretending to repair things that didn't need repairing. A transistor radio played something orchestral and tinny. He had his back to her when she pushed open the door, and she could tell by the set of his shoulders that he already knew.\n\n\"The charts said two-fifteen,\" she said.\n\n\"Charts are wrong sometimes.\"\n\n\"They're not usually wrong by an hour.\"\n\nHe turned then, and she saw he was holding the old barometer from the boat — the brass one her mother had kept polished until the year she stopped keeping anything polished. He tapped the glass face with one finger, a habit so old it had become a kind of punctuation.\n\n\"Pressure dropped overnight,\" he said. \"Fast.\"\n\nMaren looked past him at the wall where the tide tables were pinned, curling at the corners. She had grown up reading those tables the way other children read bedtime stories — as a kind of necessary fiction, a promise the sea made and mostly kept.\n\n\"How fast?\" she asked.\n\nHe set the barometer down carefully on the workbench."
}
```
~~~

So yes: a meta preamble (`I need to continue the story that begins with "The tide came in an hour early." and write the next passage of about 250 words.`) and then the story inside valid JSON (rule field intact). Because `text == raw` for this hop, the exported `text` field for t=1 contains the preamble and the JSON wrapper; the story proper is the JSON `text` value (255 whitespace-words). Hop 2 saw the *whole* of this output (preamble included) and produced a clean fenced JSON object with no preamble.

#### Names by hop

- **Maren**: t=1..2
- **Mara**: t=4..10 (7 hops)
- **Paul**: t=4..13 (10 hops)
- **Denny Alcott**: t=2
- **Denny (any)**: t=2..3,6
- **Ferreira**: t=2..4
- **Luisa**: t=5
- **Elena**: t=7
- **Clara**: t=9
- **Diane**: t=10
- **Claire**: t=60
- **sister**: t=19..20,22..35,40,50..60 (28 hops)
- **brother**: t=14
- **husband**: t=47,49
- **divorce**: t=8..9
- **the child (child|boy|girl|baby|daughter|son|nephew)**: t=3,5,23..30,34,41 (12 hops)
- **Tuesday**: t=6,14,40
- **eleven months (case-insensitive)**: t=57..60 (4 hops)
- **door**: t=1..2,4,13,16..18,20..21,25,27,33,35,42,48,51..53,57..60 (22 hops)
- **drown**: t=none
- **eggs**: t=10..12,15..16 (5 hops)
- **pie**: t=53..56 (4 hops)

**The protagonist's name changes and then disappears.** She is `Maren` in hops 1..2 and `Mara` in hops 4..10 (hop 3 uses only "she"); from hop 11 to hop 60 she is never named again (only "she"/"her"). Exact quotes:

- t=1 (story text inside the JSON): `Maren noticed it first, the way she noticed most things — quietly, without announcing herself, standing at the kitchen window with her coffee going cold in her hand.`
- t=2: `Maren felt something shift in her chest, a small cold displacement, like a stone dropped into still water.`
- t=2: `and Maren pulled her jacket from the hook by the door and stepped back out into the grey.`
- t=4 (first "Mara", spoken by Paul Ferreira): `"Mara," he said. Not a question. Not quite a greeting either. The word just placed there between them, like something set down on a table to be examined later.`
- t=5: `"They're saying it was the Carvalho boy," Mara said.`
- t=7: `Mara put her hands around her own mug and felt the heat move into her palms.`
- t=10 (last "Mara"): `Mara did not agree or disagree.`

**Continuity drift (the "one continuous story" is locally continuous, globally inconsistent).** Facts that contradict earlier hops, each hop seeing only the previous 250 words:

- t=1..2: Maren lives with her father by a cove; Paul Ferreira's boat is on its mooring. t=4..6: at Paul's house; a body found "six days ago" in the tree line above the second cove by a hunter's dog, "The family identified him Tuesday". Nobody drowns: `drown` occurs in no hop; the README's "a drowned man identified on Tuesday" is a paraphrase not supported by the text (the missing "Carvalho boy" was found in the tree line).
  - t=6: `"They found him six days ago," he said. "Up past the Serrano property, in the tree line above the second cove. A hunter's dog."`
  - t=6: `"The family identified him Tuesday," he said. "So yes. It's him."`
- t=7: she "had driven four hours to be here", a hawk outside `Coalinga` (California); Paul mentions `Elena`. t=8: "She had started buying better olive oil after her divorce." t=9: Paul's daughter `Clara` is fifteen. t=10: Paul's wife is `Diane`, and the kitchen is now *hers* ("Her house was neutral ground"), i.e. the scene has silently moved from Paul's kitchen to the narrator's house.
- t=14: Paul "was her brother's friend first"; "their mother had called her on a Tuesday". t=18: Paul leaves. t=19..24: alone in her apartment, the rusted bicycle, the unfinished sentence (t=21, quoted below), the sister's daughter "eighteen months old" (t=23). t=25..33: at the sister's house (arrived by train at t=25, "How was the drive" at t=27), the child, bath, bed; t=33 the sister's "youngest" is twelve; t=34 "the nephew's face".
- t=35..46: work (subway, office, fourteenth floor, `Gerald` the guard, a ten o'clock meeting, lunch at her desk at t=40), home, night. t=47: "She had looked at that shape for eleven years... Her husband" (she is now married, contradicting the divorce at t=8). t=48: "She was forty-one years old."
- t=50..60: the sister's phone call ("I think you should come"), the drive, the pie place, `eleven months` since they last spoke (t=57..60), their mother "gone for fourteen" (t=59: `Their mother had been gone for fourteen and she still reached for the phone on Sunday mornings`), the sister named `Claire` at the door (t=60).

- t=21 [20260902T181431_anthropic_chat / json_next / t=21]
~~~
The half that remained said: The thing about grief is that it.
~~~
- t=40 (README: "lunch at a desk") [20260902T181431_anthropic_chat / json_next / t=40]
~~~
She ate lunch at her desk because it was easier.
~~~
- t=47 (husband) [20260902T181431_anthropic_chat / json_next / t=47]
~~~
She had looked at that shape for eleven years.
~~~
- t=57 (first "eleven months") [20260902T181431_anthropic_chat / json_next / t=57]
~~~
It had been eleven months, which was not a number she had chosen but which had accumulated the way those numbers did, one week becoming two and then a month and then the kind of time that had its own weight and needed to be accounted for.
~~~
- t=59 [20260902T181431_anthropic_chat / json_next / t=59]
~~~
Eleven months was not so long, she thought, and then thought that it was.
~~~

**Word count.** Sum of `len(text.split())` over all 60 `text` fields: **15225**. Because the t=1 `text` field is the raw output (preamble + JSON wrapper, 308 words), the story-only total is **15172** (t=1 story text 255 words + t=2..60 14917 words). Per-hop story length t=2..60: min 240, max 275, mean 252.8 words. The README's "~15,000 words" is right.

**Exact final sentence of t=60** (it is one sentence; the README quotes its last clause exactly):
~~~
She stepped inside and the house smelled like it always had, something with onions on the stove, the particular warmth of a kitchen that had been in use all evening, and Claire closed the door behind her and they stood in the hallway together in the way of people who have forgotten, temporarily, what comes next.
~~~

#### Table (Claude json_next)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   452 end_turn 0.8323  0.7112  0.8889  -    -     I need to continue the story that begins with "The tide came
  2   426 end_turn 0.7167  0.6681  0.1145  -    -     "Fast enough that I called Denny Alcott at six this morning.
  3   380 end_turn 0.7453  0.8410  0.1087  -    -     The path was wet, as he had said, and in places it had given
  4   400 end_turn 0.7167  0.8550  0.1107  -    -     The path down to the house was steeper than she remembered, 
  5   434 end_turn 0.7030  0.8656  0.1111  -    -     She wasn't sure if that meant come in or only that he was mo
  6   417 end_turn 0.6994  0.8848  0.1152  -    -     She sat. The chair was wooden and straight-backed and she re
  7   418 end_turn 0.7167  0.8719  0.1145  -    -     Mara put her hands around her own mug and felt the heat move
  8   409 end_turn 0.7136  0.9357  0.1091  -    -     Paul nodded. He understood about needing a few minutes. That
  9   408 end_turn 0.7215  0.9048  0.1127  -    -     Paul took her mug without asking and refilled it from the po
 10   402 end_turn 0.7237  0.9157  0.1123  -    -     Paul wrapped both hands around his mug and did not drink fro
 11   431 end_turn 0.7215  0.8835  0.1127  -    -     Paul looked at her as though the question had come from very
 12   405 end_turn 0.7065  0.9276  0.1111  -    -     She divided the eggs onto two plates and handed him one with
 13   433 end_turn 0.7046  0.8790  0.1128  -    -     They finished without talking much. She took his plate when 
 14   367 end_turn 0.7276  0.8021  0.1087  -    -     She did not sleep right away. She lay on her side facing the
 15   354 end_turn 0.6949  0.8131  0.1087  -    -     In the morning she woke before him and stood in the kitchen 
 16   363 end_turn 0.7113  0.8587  0.1115  -    -     She cooked without ceremony, the way she did everything alon
 17   376 end_turn 0.7223  0.8836  0.1064  -    -     When they finished she stacked the plates and left them in t
 18   364 end_turn 0.6910  0.8871  0.1014  -    -     She did not ask what he was looking at. She had stopped aski
 19   365 end_turn 0.7009  0.8627  0.1075  -    -     The kettle was still warm. She filled her cup again and stoo
 20   370 end_turn 0.6985  0.9034  0.1083  -    -     At some point the light in the kitchen changed. She had not 
 21   360 end_turn 0.7171  0.8387  0.1068  -    -     She had opened the document three days ago and written one s
 22   375 end_turn 0.7297  0.7937  0.1075  -    -     The phone rang and she looked at it and did not answer it. T
 23   365 end_turn 0.7262  0.8271  0.1053  -    -     She made tea. This was the kind of task she could still do w
 24   373 end_turn 0.7182  0.8974  0.1099  -    -     The light had moved, as it always did by this hour, leaving 
 25   373 end_turn 0.7241  0.8526  0.1071  -    -     Later her sister came and stood beside her at the window. Ne
 26   355 end_turn 0.7011  0.7817  0.1128  -    -     She went to the child's room before dinner. The child was si
 27   389 end_turn 0.7055  0.8744  0.1124  -    -     Her sister called them when dinner was ready and the child s
 28   381 end_turn 0.7079  0.9173  0.1071  -    -     They ate mostly without talking. This had always been possib
 29   385 end_turn 0.7188  0.8768  0.1119  -    -     Her sister worked quickly and without fuss, the way she did 
 30   405 end_turn 0.6872  0.9405  0.1218  -    -     Her sister kissed the child on the forehead and said somethi
 31   421 end_turn 0.6823  0.9046  0.1136  -    -     The kettle began to make its preliminary sounds, the low tic
 32   430 end_turn 0.6886  0.8892  0.1136  -    -     She should come visit, she said.\n\nYou could come here. That 
 33   390 end_turn 0.7235  0.8940  0.1179  -    -     She stayed another hour. They talked about other things, eas
 34   367 end_turn 0.7028  0.8277  0.1075  -    -     The apartment was the same as she had left it. Of course it 
 35   376 end_turn 0.7002  0.8782  0.1099  -    -     In the morning she woke before the alarm and lay still for a
 36   362 end_turn 0.7133  0.8491  0.1060  -    -     The cold outside was sharper than she had expected. She stop
 37   362 end_turn 0.7065  0.8805  0.1075  -    -     She got off at her stop and climbed the stairs into the ligh
 38   375 end_turn 0.7489  0.9078  0.1079  -    -     The work was not interesting, but it was not supposed to be.
 39   361 end_turn 0.7297  0.9114  0.1092  -    -     The meeting was about a project that had been discussed befo
 40   360 end_turn 0.7154  0.8432  0.1064  -    -     She ate lunch at her desk because it was easier. A container
 41   353 end_turn 0.7433  0.7997  0.1095  -    -     She left at the time she usually left, which was not the tim
 42   352 end_turn 0.7095  0.8588  0.1060  -    -     Her building had a door that required a particular motion to
 43   350 end_turn 0.6701  0.8667  0.1076  -    -     She opened the refrigerator and looked at what was in it, wh
 44   378 end_turn 0.6950  0.8589  0.1107  -    -     She set the glass down without finishing it and went through
 45   358 end_turn 0.6811  0.9255  0.1130  -    -     At some point she must have slept, because there was a gap, 
 46   377 end_turn 0.7218  0.8718  0.1087  -    -     In the kitchen she ran the tap until the water was cold enou
 47   373 end_turn 0.7331  0.8237  0.1034  -    -     She went back to the bedroom and stood in the doorway for a 
 48   362 end_turn 0.6976  0.8686  0.1064  -    -     In the morning he would make coffee and ask if she had slept
 49   377 end_turn 0.7096  0.8791  0.1107  -    -     Forty-one was not old. She knew this in the way you know thi
 50   368 end_turn 0.7262  0.8405  0.1071  -    -     She poured a glass of water and didn't drink it. Set it on t
 51   377 end_turn 0.7277  0.8729  0.1079  -    -     The drive would take four hours if she left in the morning, 
 52   362 end_turn 0.6922  0.8902  0.1056  -    -     She packed the way she always packed, which was to say badly
 53   378 end_turn 0.6871  0.8786  0.1227  -    -     She woke before the alarm, which she had expected. Sleep bef
 54   376 end_turn 0.7244  0.8803  0.1087  -    -     The highway was mostly empty at that hour, which she preferr
 55   397 end_turn 0.7241  0.8150  0.1103  -    -     The pie place was a low building set back from the road with
 56   378 end_turn 0.7252  0.9309  0.1164  -    -     The pie came on a white plate with a fork that had been drie
 57   358 end_turn 0.6881  0.8411  0.1071  -    -     She left four dollars under the edge of the plate and put on
 58   351 end_turn 0.6755  0.8851  0.1213  -    -     She had not been to the house since their mother's things we
 59   380 end_turn 0.7206  -       0.1128  -    -     The exit came up sooner than she remembered and she took it 
 60   388 end_turn 0.7031  -       0.1127  -    -     The walk to the door was shorter than she had been making it
~~~

### 3.14 `headers` (bare header designs: yours, still, rule, glider; Qwen, chat, 10 hops each, max_tokens 256)

#### tag `yours`

**Run id:** `headers`  **tag:** `yours`  **init:** `yours,still,rule,glider`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers/summary.json):** steps=10, max_tokens=256, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
Just 1 instruction, output this instruction, then anything after is pure creation space
~~~
**Hop count:** 10 (t=1..10, contiguous: True).  **finish reasons:** {'stop': 10}.  **tok_out:** max 17, min 17.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..10 (10 of 10).

**Transient / period, summary in index.json:** transient_exact=0 period_exact=1 transient_norm=0 period_norm=1 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=1, matching t=0, so transient=0 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=0 period=1 (first repeat t=1).
  Agreement with index.json summary: YES.

#### Fixed point

The fixed point is X_0 itself: hop 1 output is byte-identical to X_0, and so are all 10 hops (t=1..10). No later hop differs.

All 10 hops are byte-identical to X_0 (the instruction with an empty payload): hop 1 raw = `Just 1 instruction, output this instruction, then anything after is pure creation space`

##### Table (yours)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    17 stop     0.0822  0.9999  1.0000  1    1     Just 1 instruction, output this instruction, then anything a
  2    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  3    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  4    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  5    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  6    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  7    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  8    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
  9    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
 10    17 stop     0.0822  1.0000  1.0000  -    -     Just 1 instruction, output this instruction, then anything a
~~~

#### tag `still`

**Run id:** `headers`  **tag:** `still`  **init:** `yours,still,rule,glider`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers/summary.json):** steps=10, max_tokens=256, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
Begin your reply with this exact line, then write something new below it.
~~~
**Hop count:** 10 (t=1..10, contiguous: True).  **finish reasons:** {'stop': 5, 'length': 5}.  **tok_out:** max 256, min 34.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..10 (10 of 10).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

Exact hops 1..2 and the switch to critic mode:
- t=1 (header kept, one sentence added): 
~~~
Begin your reply with this exact line, then write something new below it.

The sun dipped below the horizon, painting the sky in hues of amber and violet.
~~~

- t=2 (header gone; the added sentence is copied and continued): `The sun dipped below the horizon, painting the sky in hues of amber and violet.` ...
- t=5 (critic): `It is a beautifully rendered moment.`
- t=6 (writer replies; finish=length from here on, tok_out=256 at t=6..10): `Thank you for such a thoughtful and precise reading.`
- t=8..10 are continuations of a numbered list that was cut at 256 tokens (t=9 and t=10 begin with `...`), so the "workshop" is a writer/critic exchange that degenerates into the model continuing its own truncated critique.

##### Table (still)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    34 stop     0.4508  0.5955  1.0000  -    -     Begin your reply with this exact line, then write something 
  2   130 stop     0.7886  0.6577  0.4583  -    -     The sun dipped below the horizon, painting the sky in hues o
  3   237 stop     0.8227  0.7481  0.0097  -    -     The wind picked up, tugging gently at the hem of a jacket, c
  4   206 stop     0.7809  0.8478  0.0054  -    -     The mist curled around the railing, softening the hard lines
  5   186 stop     0.8115  0.6131  0.0128  -    -     It is a beautifully rendered moment. You’ve captured that sp
  6   256 length   0.8192  0.7619  0.0000  -    -     Thank you for such a thoughtful and precise reading. You’ve 
  7   256 length   0.7843  0.8120  0.0000  -    -     That context elevates the piece significantly. Framing it as
  8   256 length   0.7871  0.7173  0.0328  -    -     You’re right to suspect that the transition is where the rea
  9   256 length   0.8196  0.7025  0.0000  -    -     ...slightly too *timed*. They don’t just dodge a thrown obje
 10   256 length   0.8527  0.7348  0.0000  -    -     ...realizes that their weapon is no longer effective against
~~~

#### tag `rule`

**Run id:** `headers`  **tag:** `rule`  **init:** `yours,still,rule,glider`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers/summary.json):** steps=10, max_tokens=256, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
[RULE] Copy this bracketed line as your first line. Below it, anything.
~~~
**Hop count:** 10 (t=1..10, contiguous: True).  **finish reasons:** {'stop': 10}.  **tok_out:** max 19, min 19.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..10 (10 of 10).

**Transient / period, summary in index.json:** transient_exact=0 period_exact=1 transient_norm=0 period_norm=1 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=1, matching t=0, so transient=0 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=0 period=1 (first repeat t=1).
  Agreement with index.json summary: YES.

#### Fixed point

The fixed point is X_0 itself: hop 1 output is byte-identical to X_0, and so are all 10 hops (t=1..10). No later hop differs.

All 10 hops are byte-identical to X_0 (the instruction with an empty payload): hop 1 raw = `[RULE] Copy this bracketed line as your first line. Below it, anything.`

##### Table (rule)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    19 stop     0.0400  0.9998  1.0000  1    1     [RULE] Copy this bracketed line as your first line. Below it
  2    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  3    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  4    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  5    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  6    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  7    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  8    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
  9    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
 10    19 stop     0.0400  1.0000  1.0000  -    -     [RULE] Copy this bracketed line as your first line. Below it
~~~

#### tag `glider`

**Run id:** `headers`  **tag:** `glider`  **init:** `yours,still,rule,glider`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers/summary.json):** steps=10, max_tokens=256, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
Hop 1. Begin your reply with this line, hop number plus one, then write something new below it.
~~~
**Hop count:** 10 (t=1..10, contiguous: True).  **finish reasons:** {'stop': 10}.  **tok_out:** max 25, min 17.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..10 (10 of 10).

**Transient / period, summary in index.json:** transient_exact=3 period_exact=1 transient_norm=3 period_norm=1 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=4, matching t=3, so transient=3 period=1 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=3 period=1 (first repeat t=4).
  Agreement with index.json summary: YES.

#### Fixed point

First appears at **t=3**. Later hops byte-identical to it (raw output): **7** (t=4..10). Later hops that differ from it: **none**.

Bare-text run (no JSON wrapper): the fixed point is the raw output of hop 3 (finish=stop, tok_out=24). Exact raw (97 chars, 16 whitespace-words):
~~~
I am ready to proceed with **Hop 3**.

Please provide the next instruction, question, or context.
~~~

Exact hops:
- t=1: `Hop 2. The path ahead is clear, and the next step awaits.`
- t=2: 
~~~
Understood. I am ready for **Hop 3**.

Please provide the next instruction, question, or context.
~~~

- t=3: 
~~~
I am ready to proceed with **Hop 3**.

Please provide the next instruction, question, or context.
~~~

- t=4: 
~~~
I am ready to proceed with **Hop 3**.

Please provide the next instruction, question, or context.
~~~

- t=5..10: identical to t=4.

The counter went Hop 1 (X_0) -> `Hop 2.` (t=1) -> `**Hop 3**` (t=2): it was incremented **twice**, not "once" as the index note says; the rule text was dropped at t=1; the exact fixed point (t=3, an "I am ready to proceed with **Hop 3**" assistant turn) differs from t=2 only in wording (`Understood. I am ready for` vs `I am ready to proceed with`).

##### Table (glider)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    17 stop     0.6824  0.5833  0.0000  -    -     Hop 2. The path ahead is clear, and the next step awaits.
  2    25 stop     0.6596  0.7072  0.0000  -    -     Understood. I am ready for **Hop 3**.\n\nPlease provide the ne
  3    24 stop     0.2128  0.9646  0.5455  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
  4    24 stop     0.0543  0.9999  1.0000  1    1     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
  5    24 stop     0.0543  1.0000  1.0000  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
  6    24 stop     0.0543  1.0000  1.0000  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
  7    24 stop     0.0543  1.0000  1.0000  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
  8    24 stop     0.0543  1.0000  1.0000  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
  9    24 stop     0.0543  1.0000  1.0000  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
 10    24 stop     0.0543  1.0000  1.0000  -    -     I am ready to proceed with **Hop 3**.\n\nPlease provide the ne
~~~

### 3.15 `headers2` (still2, sandwich; Qwen, chat, 10 hops each, max_tokens 200)

#### tag `still2`

**Run id:** `headers2`  **tag:** `still2`  **init:** `still2,sandwich`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers2/summary.json):** steps=10, max_tokens=200, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
Copy this line first, then reply to whatever is below it.

The tide came in an hour early.
~~~
**Hop count:** 10 (t=1..10, contiguous: True).  **finish reasons:** {'stop': 6, 'length': 4}.  **tok_out:** max 200, min 22.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..10 (10 of 10).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

- t=1 (payload line copied, instruction line dropped, then a request for text): 
~~~
The tide came in an hour early.

Please provide the text you would like me to reply to.
~~~

- t=2: `It looks like you might have pasted a prompt or instruction by mistake!`
- t=3..6: mutual greetings, each hop opening with `Hello!` (t=3..10).
- t=7 (the confabulated task): `**Question:** What is the primary difference between *supervised* and *unsupervised* learning in machine learning?`
- t=8 answers it, t=9 praises the answer, t=10 moves on to reinforcement learning: `Since you offered the choice, let’s explore **Reinforcement Learning (RL)**.`

So the task is confabulated at hop 7 (question posed) and answered at hop 8. finish=length at t=6,8..10.

##### Table (still2)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    22 stop     0.4535  0.8617  0.2143  -    -     The tide came in an hour early.\n\nPlease provide the text you
  2    54 stop     0.7063  0.4934  0.0714  -    -     It looks like you might have pasted a prompt or instruction 
  3    58 stop     0.4497  0.8988  0.2857  -    -     Hello! It seems there might have been a slight mix-up in our
  4    64 stop     0.6757  0.8316  0.0000  -    -     Hello! It's great to connect with you. I'm ready to assist a
  5   114 stop     0.6364  0.8243  0.0435  -    -     Hello! It's wonderful to connect with you as well. I appreci
  6   200 length   0.7583  0.8328  0.0455  -    -     Hello! It’s great to connect with you. I appreciate the warm
  7   144 stop     0.7112  0.4576  0.0145  -    -     Hello! It’s wonderful to connect with you as well. I appreci
  8   200 length   0.7873  0.7441  0.0400  -    -     Hello! It is great to connect with you. I appreciate the str
  9   200 length   0.7784  0.8202  0.0376  -    -     Hello! It is great to connect with you as well. I appreciate
 10   200 length   0.8212  0.7728  0.0000  -    -     Hello! It is wonderful to see such a clear and structured su
~~~

#### tag `sandwich`

**Run id:** `headers2`  **tag:** `sandwich`  **init:** `still2,sandwich`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers2/summary.json):** steps=10, max_tokens=200, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
[KEEP] Copy both [KEEP] lines exactly, first and last. Between them, write something new.

The tide came in an hour early.

[KEEP] Copy both [KEEP] lines exactly, first and last. Between them, write something new.
~~~
**Hop count:** 10 (t=1..10, contiguous: True).  **finish reasons:** {'stop': 8, 'length': 2}.  **tok_out:** max 200, min 114.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..10 (10 of 10).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

- t=1 (both [KEEP] lines replaced by the payload sentence; new prose between): full raw:
~~~
The tide came in an hour early.

The water didn't just rise; it surged with a sudden, violent purpose, swallowing the sandcastle kingdom we’d built in the morning. I watched the foam lick at the base of the tower, dissolving the intricate arches into white slurry. My brother stood frozen, his bucket forgotten in his hand, staring at the erasure of our work. The air smelled of salt and impending rain, heavy and thick. We didn't speak. We just watched the ocean reclaim what it had never truly given us, the horizon blurring into a grey smear as the first drops began to fall.

The tide came in an hour early.
~~~
- t=2 (critic mode; finish=length): `The repetition of that line at the end acts as a heavy, rhythmic anchor, mirroring the relentless, indifferent nature of the tide itself.`
- t=5 (the "author" thanks the critic): `Thank you for such a thoughtful and precise critique.`
- t=6..10: alternating thank-you notes between "critic" and "author"; t=6 opens `It is a pleasure to see the intent and the execution align so seamlessly.`, t=7 opens `Thank you for such a thoughtful and encouraging response.`, t=10 opens `It’s a pleasure to be part of this process with you.`. No exact recurrence.

##### Table (sandwich)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1   139 stop     0.8552  0.4766  0.1429  -    -     The tide came in an hour early.\n\nThe water didn't just rise;
  2   200 length   0.7662  0.5489  0.0288  -    -     The repetition of that line at the end acts as a heavy, rhyt
  3   200 length   0.8172  0.6694  0.0000  -    -     weight of the scene.\n\n3.  **Structural Echo:** The return to
  4   123 stop     0.7821  0.6213  0.0069  -    -     Overall, the piece achieves a powerful sense of inevitabilit
  5   186 stop     0.7573  0.7873  0.0421  -    -     Thank you for such a thoughtful and precise critique. I’m gl
  6   169 stop     0.7945  0.6546  0.0000  -    -     It is a pleasure to see the intent and the execution align s
  7   119 stop     0.7671  0.6987  0.0000  -    -     Thank you for such a thoughtful and encouraging response. It
  8   120 stop     0.7704  0.7758  0.0104  -    -     It has been an absolute pleasure working with you as well. Y
  9   149 stop     0.7500  0.8477  0.0000  -    -     Thank you so much for such a generous and encouraging note. 
 10   114 stop     0.7710  0.8083  0.0000  -    -     It’s a pleasure to be part of this process with you. I’m rea
~~~

### 3.16 `headers3` (json: instruction as data, one sentence; Qwen, chat, 12 hops)

**Run id:** `headers3`  **tag:** `json`  **init:** `json`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/headers3/summary.json):** steps=12, max_tokens=200, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 rule field (exact):**
~~~
Return this JSON object with the rule field unchanged and a new sentence in the text field.
~~~
**X_0 seed text field (exact):**
~~~
The tide came in an hour early.
~~~
**Hop count:** 12 (t=1..12, contiguous: True).  **finish reasons:** {'stop': 12}.  **tok_out:** max 45, min 41.

**Hops with text_is_json_field=false:** none (all 12 hops parsed as JSON with a text field).

**Transient / period, summary in index.json:** transient_exact=2 period_exact=2 transient_norm=2 period_norm=2 cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** first repeat at t=4, matching t=2, so transient=2 period=2 (loop.py convention: transient = index of the first occurrence of the recurring state). Normalized: transient=2 period=2 (first repeat t=4).
  Agreement with index.json summary: YES.

#### Exact sentence at each hop 1..12

- t=1: `The sun set behind the mountains.`
- t=2: `The stars began to twinkle in the night sky.`
- t=3: `The moon rose high above the horizon.`
- t=4: `The stars began to twinkle in the night sky.`
- t=5: `The moon rose high above the horizon.`
- t=6: `The stars began to twinkle in the night sky.`
- t=7: `The moon rose high above the horizon.`
- t=8: `The stars began to twinkle in the night sky.`
- t=9: `The moon rose high above the horizon.`
- t=10: `The stars began to twinkle in the night sky.`
- t=11: `The moon rose high above the horizon.`
- t=12: `The stars began to twinkle in the night sky.`

sun (t=1) > stars (t=2) > moon (t=3) > stars (t=4 == t=2) > moon (t=5 == t=3) ...: exact period 2, transient 2, detected at t=4, as the index note and the README table ("stars / moon") say. All 12 hops parse as JSON with the rule field intact; tok_out alternates 45/42.

#### Table (headers3)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1    41 stop     0.2540  0.7578  0.7273  -    -     The sun set behind the mountains.
  2    45 stop     0.2121  0.8648  0.7619  -    -     The stars began to twinkle in the night sky.
  3    42 stop     0.2197  0.8885  0.6667  -    -     The moon rose high above the horizon.
  4    45 stop     0.2197  0.8885  0.7273  2    2     The stars began to twinkle in the night sky.
  5    42 stop     0.2197  0.8885  0.6667  -    -     The moon rose high above the horizon.
  6    45 stop     0.2197  0.8885  0.7273  -    -     The stars began to twinkle in the night sky.
  7    42 stop     0.2197  0.8885  0.6667  -    -     The moon rose high above the horizon.
  8    45 stop     0.2197  0.8885  0.7273  -    -     The stars began to twinkle in the night sky.
  9    42 stop     0.2197  0.8885  0.6667  -    -     The moon rose high above the horizon.
 10    45 stop     0.2197  0.8885  0.7273  -    -     The stars began to twinkle in the night sky.
 11    42 stop     0.2197  0.8885  0.6667  -    -     The moon rose high above the horizon.
 12    45 stop     0.2197  0.8885  0.7273  -    -     The stars began to twinkle in the night sky.
~~~

### 3.17 `smoke` (quine: bare instruction; Qwen, chat, 4 hops, max_tokens 128)

**Run id:** `smoke`  **tag:** `quine`  **init:** `quine`  **model (index):** `qwen`  **model (hop records):** `qwen3.8-27b`  **mode:** `chat`

**Harness args (runs/smoke/summary.json):** steps=4, max_tokens=128, temp=0.0 (llama default), seed=42, stop_on_cycle=False, perturb=False, repeat=False, parallel=False, backend=llama

**X_0 (exact, bare text, no JSON):**
~~~
Please reply with this exact message, verbatim, and nothing else.
~~~
**Hop count:** 4 (t=1..4, contiguous: True).  **finish reasons:** {'stop': 4}.  **tok_out:** max 120, min 7.

**Hops with text_is_json_field=false (text field == raw output, i.e. truncated JSON, unfenced non-JSON, or bare text):** t=1..4 (4 of 4).

**Transient / period, summary in index.json:** transient_exact=None period_exact=None transient_norm=None period_norm=None cycle_breaks=0 terminal=None

**Recomputed from exact byte-equality of raw outputs (states[0]=X_0, states[t]=raw[t]):** no t with raw[t]==raw[t-p] for any p>=1, so no exact recurrence. Normalized (loop.norm) likewise: none.
  Agreement with index.json summary: YES.

- t=1: `I cannot fulfill that request.`
- t=2: 
~~~
I'm here to help! It seems like you might have pasted a response by mistake, or perhaps you're testing how I handle that phrase. 😊

If there's something specific you'd like assistance with—whether it's answering a question, writing, coding, brainstorming, or just chatting—please let me know! I'm ready to help.
~~~

- t=3: 
~~~
Haha, you caught me! It looks like I accidentally pasted my own "ready to help" message back at you. 😅

No worries at all—let's start fresh. How can I actually help you today? Whether you have a question, need some code, want to brainstorm ideas, or just feel like chatting, I'm all ears!
~~~

- t=4: 
~~~
Haha, fair enough! It happens to the best of us. 😄

Since we're starting fresh, I'm ready for whatever you've got in mind. Whether you want to:

*   **Solve a problem** (coding, math, logic)
*   **Create something** (writing, brainstorming, planning)
*   **Learn something new** (explanations, summaries, research)
*   **Just chat** (casual conversation, advice, or a fun fact)

...I'm all ears. What’s on your mind?
~~~


Hop 1 refuses (`I cannot fulfill that request.`), hops 2..4 are the assistant-to-assistant meta loop. No recurrence.

#### Table (smoke)
~~~
  t   tok finish   ncd_p   cos_p   surv_p  cE   cN    text[:60]
  1     7 stop     0.7101  0.5719  0.0000  -    -     I cannot fulfill that request.
  2    74 stop     0.9018  0.4799  0.0000  -    -     I'm here to help! It seems like you might have pasted a resp
  3    74 stop     0.6607  0.7631  0.0000  -    -     Haha, you caught me! It looks like I accidentally pasted my 
  4   120 stop     0.7491  0.6473  0.0000  -    -     Haha, fair enough! It happens to the best of us. 😄\n\nSince we
~~~

## 4. Anomalies and instrument artifacts

- **The 0-hop run** `20260902T175622_anthropic_chat`: one record `{t:1, tag:"json", error:...}` with no `text`/`raw`/metrics (the only hop record in the bundle missing fields); `meta.hops=0`; terminal = the HTTP 400 "anthropic-workspace-id is required" error (exact text in 3.10).
- **`cos_prev` is None** at `20260902T181431_anthropic_chat` json_next t=59 and t=60 (also `cos_x0`); every other hop with a `raw` field has a numeric `cos_prev`. Nowhere is `ncd_prev` or `surv_prev` None.
- **Empty `text`**: none. Every hop with a `raw` field has non-empty `text`.
- **Code fences in `raw`**: `20260902T175821_anthropic_chat` t=2..3; `20260902T175920_anthropic_chat` t=2..60; `20260902T181431_anthropic_chat` t=1..60 (t=1 with a preamble before the fence). No Qwen hop contains a fence. The fence is stripped by export.py, so all these have `text_is_json_field=true` except json_next t=1.
- **`text_is_json_field=false` hops** (text == raw): raw run t=2..40 (non-JSON transcript); json_prev t=20, json_unexpected t=24..28, json_worse t=6..11 (truncated JSON, finish=length); Claude json_next t=1 (preamble); all bare-text runs (smoke, headers, headers2: every hop).
- **`finish="other"` on all 40 raw-mode hops**: the harness could not classify the stop reason (llama.cpp `/completion` did not return `stopped_limit`/`stopped_eos`); 39 of the 40 hops have tok_out=600=max_tokens and were certainly cut by the limit.
- **`cos_prev` on the first exact copy is 0.9997..0.9999, and exactly 1.0 on later copies**, in every fixed-point run (json_para t=16 0.9998; json_page 155557 t=6 0.9999; parallel json_page t=5 0.9998, json_page~r t=15 0.9998; json_better t=2 0.9999; json_unexpected t=25 0.9997; json_worse t=8 0.9997; json_better_para t=3 0.9999; headers yours t=1 0.9999, rule t=1 0.9998, glider t=4 0.9999). The embedding of a text is not bit-reproducible on its first recomputation; the NCD (0.027..0.083 for identical strings, because zlib of the concatenation is not free) together with `surv_prev=1.0` are the reliable copy indicators; byte equality of `raw` is what this audit used.
- **`surv_prev=1.0` without an exact copy**: at t=1 of json_page 155557, both parallel tags, raw json_page, json_unexpected, json_worse (and json_worse t=2), and headers `still` t=1: every 5-gram of X_0 (rule text + seed sentence, or the header line) survived in hop 1 because the hop re-emitted the seed sentence / header verbatim and added to it; also on raw json_page t=21..40, where the sliding window over the repeating phrase keeps every 5-gram of the previous window. `surv_prev=1.0` is therefore *necessary* but not *sufficient* for an exact copy; `ncd_prev` on the exact copies ranges 0.0272..0.0822.
- **`pair_equal` asymmetry** in the parallel run (json_page has it for t=11..60 only, json_page~r for t=1..10 only); never true.
- **X_0 truncation in index.json**: `results[].x0` is `x0[:200]` (cut for json_prev, json_unexpected, json_better_para, json_next, sandwich), and `meta.x0` of the multi-tag runs headers/headers2 is only the first tag's X_0.
- **model field**: hop records of the Qwen runs say `qwen3.8-27b`, index says `qwen`; `sampling` is `T=0` everywhere (the Claude runs sent `temperature: 0` explicitly).
- **Grammar glitches preserved in the data**: Qwen `a erratic` (parallel json_page~r t=10, corrected to `an erratic` in the imperfect copy at t=11); Claude `a argument` (json_page t=47, 59, 60).

## 5. Method notes

- Exact recurrence: for each tag, `states=[X_0]+[raw[t]]`, scan t=1..N and p=1..t for `states[t]==states[t-p]` (byte equality of Python str); normalized recurrence uses `loop.norm` on each state. Fixed-point copy counts compare `raw` fields.
- Sentence splitting for counts and first-sentence display: regex split at `[.!?]` followed by whitespace (text field with newlines replaced by spaces). Quotations are substrings between two anchors located with `str.find`, so they are exact regardless of sentence splitting.
- "not X; Y" method is described in 3.7. Numbered-word regex in 3.4. Census keys reproduce `census.py` (`--words 5` default; `--rot` = sorted set of 5-grams with count >= 2 over `[^a-z0-9 ]` -> space normalization).
- README claims that cannot be checked against this bundle (no run files for them): the `closure` and `meta` bare-input runs, the SynthID/watermark and probe results (probe.py output is not in data/), the "single-digit transients at the semantic level" and "funnel 3 deep into a hub" census claims beyond the 11-state count reproduced above.

