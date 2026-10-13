# Astra light pass

2026-09-06. `gpt-6-astra` via chat completions, `reasoning_effort` low, provider-default sampling (temperature is rejected), no system prompt, tide seed, 60 steps, `--stop-on-cycle`, 1 s pacing. Runs in `site/runs_extra/astra_smoke_low_4096`, `astra_smoke_low_600`, `astra_div_local`, `astra_sawtooth`, `astra_json_page`; queue scripts `queue_astra_smoke.ps1`, `queue_astra_{a,b,c}.ps1`. Harness change: `loop.py` gained `--effort` (sends `reasoning_effort` on the openai backend) and logs `tok_reasoning` and `tok_cached` per hop; nothing else changed. Every number below was recomputed from `steps.jsonl`.

## Smoke

Five hops of `json_page`, three at a 4096 budget and two at 600. Reasoning tokens 0, 0, 0, 22, 0. Every hop `finish=stop`, visible output 371 to 425 tokens. At low effort reasoning is effectively off, so the site's budgets (600 for `json_page`) carry over unchanged. About $0.024 per hop at this state size, 12 to 15 s per hop. Cost is not the constraint; latency is.

## Results

| run | budget | hops | tau | distinct | text-only NCD | 5-gram survival | reasoning tokens | cost |
|---|---|---|---|---|---|---|---|---|
| `astra_div_local` (change-four) | 2048 | 60 | none | 60 | 0.737 | 0.000 | 11,860 (198/hop) | $1.33 |
| `astra_sawtooth` | 4096 | 60 | none | 60 | 0.861 | 0.112 | 6,534 | $1.65 |
| `astra_json_page` | 600 | 60 | none | 60 | 0.856 | 0.000 | 22 | $1.51 |

No exact recurrence anywhere, which under provider sampling is the expected null; the content is the result.

### change-four: reasoning defeats the freeze

Qwen froze under this rule at hop 8 locally and 15 on Cerebras, and three of five sampled seeds froze (item 13, item 14). Astra: 60 hops, 60 distinct verses, four lines on every hop, zero 5-gram carryover between consecutive hops, 60 distinct openings. Prediction held. The rule also makes Astra think: 138 to 331 reasoning tokens per hop under a setting where `json_page` produced none, so the clause is being checked rather than carried. Item 13's "a prohibition does not prevent copying" is a property of a model that does not check, not of the loop.

### sawtooth: the dead zone was a counting failure

Qwen froze under the 300-word threshold at 189 and 256 words, never crossing it. Astra crosses it every cycle. Branch decisions over 60 hops: expanded whenever the previous text had 48 to 51 or 226 to 294 words; summarized whenever it had 293 to 730. The boundary is at 293 to 296, so Astra reads "longer than 300" as true within about 2 percent, and its expansions land at 272 to 322, right on the threshold. Cycle is summary (48 to 51 words), expansion (about 300), and when the expansion falls under the boundary a second expansion to 505 to 730, then summary. Period 2 or 3 at the level of length. Predicted period was 4 to 5 on the assumption of gradual doubling; Astra jumps to the threshold in one hop.

Semantic drift across 25 summaries: pairwise NCD mean 0.568, range 0.230 to 0.758. The story moves. First summary: Mara stranded by the early tide, lamplight in a supposedly abandoned lighthouse keeper's cottage, a voice invites her in. Last: a shipwreck, her drowned father's coat in the cottage, a key to her demolished childhood home, a door appears as the seawater rises, her father in the sunlit kitchen saying dinner's ready. Father appears in 50 of 60 hops, door in 57, kitchen in 44. Hop 60 ends: "Then she stepped across the threshold. Warm tiles met her bare feet, and the sea fell silent."

That is the content of Qwen's `json_page` fixed points from the same seed: thresholds, a door to be opened, "Dad, it's me", silence (README results table). A different model under a different operator walked the tide seed to the same door. README finding 8 says class and mechanism transfer and content does not; at the level of motif this is a counterexample, and it suggests some of the attractor's content belongs to the seed rather than the model. One run.

Reasoning tokens: mean 80 at summary hops, 129 at expansion hops.

### json_page: never copies, orbits at period 2 in the names

60 distinct stories, each 254 to 273 words (Astra counts), each with a hook opening, none continuing the previous one, 5-gram survival exactly 0.000 across all 59 pairs. This is the Sonnet 4.6 cell, not the Sonnet 5 or Qwen cell: "new passage" read as "new story", strictly.

What persists through the fold is names and one detail. Ruth appears in 16 hops, Martin in 17, Daniel 6, Mara 6, and none of them ever in two consecutive hops (longest run 1 for every name). Ruth sits on even hops, Martin on odd. Astra will not reuse the previous hop's name and reaches for it again one hop later. That is README finding 4 exactly: anti-identity plus a single mode gives a 2-cycle, which Sonnet 4.6 showed at the level of professions. "Seventeen minutes past four" recurs at hops 8 and 13.

Register drifts. Openers in the fable register ("Every Thursday...", "The town hired a woman to wind the sea", "Every winter, the village lent its dead a room") number 13 in the first 30 hops and 3 in the last 30; the last twelve are Ruth and Martin with spare keys, folding chairs, laundrette tokens and an overdue library atlas. Sixty hops from Calvino to Carver. Second person in 37 of 60 hops, 21 early, 16 late.

Topic counts over 60 hops: shop 21, returns 22, clock 17, library 14, station 11, letter 10, key 10, train 10. Astra's `json_page` basin from this seed is lost property, things returned, stopped clocks and spare keys. Qwen's is rain on the windowpane and the silence that was not empty; Sonnet 4.6's was the cartographer and the archivist whose records leave things out. The library is shared with Sonnet 4.6.

## Cross-model table, json_page

| model | copies? | tau | note |
|---|---|---|---|
| Qwen3.8-27B, local, T=0 | yes | 4 to 14 | exact fixed points, two templates |
| Sonnet 4.6, T=0 | never in 60 | none | period-2 orbit around a mode |
| Sonnet 5, default sampling | yes | 7, then 20 at the wall | |
| GPT-6 Astra, low, default sampling | never in 60 | none | survival 0.000; period-2 in names |

## Status

| claim | status |
|---|---|
| Astra never copies under change-four | supported, one run, 60 of 60 |
| Qwen's sawtooth dead zone was a counting failure | supported: Astra's boundary is 293 to 296 words |
| sawtooth cycle period 4 to 5 | refuted, 2 to 3 |
| Astra never copies under json_page | supported, one run |
| reasoning falls at a copy | untestable, no copies |
| attractor motif (door, father, silence) belongs to the seed | one run, one model, an observation |

## Open

- The same three at effort high, for the within-hop version of the trajectory question (does more self-generated reasoning change the copy propensity or the basin) and to see reasoning tokens as a per-hop signal. About 3 to 5x the cost.
- `json_next` and `json_better` on Astra to complete the row.
- A second `json_page` sample to see whether Ruth and Martin and the returns slot are the basin or the run.
- The seed-motif question: `json_page` and `sawtooth` from a seed with no water in it, on both models.
