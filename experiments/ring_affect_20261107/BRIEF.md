# Ring, affect as the particle: fact vs. emotion as a propagating disturbance

Frozen 2026-11-07 evening, before any run. Justin's design question ("do you think it must be small facts? What about a powerful reaction or emotion?"), the panic choice ("I don't remember a model intentionally writing prose in an English kitchen with panic"), and the pilot scale (16 cells x 40 hops x 1 model, local Qwen) are his; the seeds, measures and predictions below are Claude Mythos 5.1's, written in the same session and locked here. Everything an agent needs is in this file and this directory; the chat is not a source.

## Why

The ring (`experiments/ring_20261017/PROTOCOL.md`) is the one substrate in this project with locality and a synchronous update, so it is where Class 4 (localized structures that travel and interact) could appear. The battle seed failed as a probe: a second register is not a perturbation of the background, it is a second background, and the rule either quarantines it (Qwen at distance 1) or lets it take over (Astra, five of seven cells). A glider has to be something the background rule will carry. Two candidates: an inert fact (register-matched object), and an emotional state (register-free, and generative: it changes what the next cell writes). This pilot measures both on the same background under identical conditions, then collides two emotions.

## Locked decisions

| decision | value | owner |
|---|---|---|
| background | `seeds/plain.txt`, the Agnes kitchen (unchanged from ring_20261017); every undisturbed cell | Justin (prior work) |
| rule | `rule.txt`, unchanged from ring_20261017 (60 words, edges may touch) | Justin (prior work) |
| ring | N=16, 40 hops, synchronous, neighbours see last sentence only | Justin |
| model, pilot | local llama-server, `qwen3.8-27b`, T=0, seed 42, thinking off, 600 max tokens, 4 workers | Justin |
| disturbance placement | the anchor sentence is inserted as the **penultimate sentence** of the kitchen in every disturbed seed (jug, panic, grief), so every cell's edge at hop 0 is "The kettle began to tick." and nothing travels for free at hop 1 | Mythos |
| Run 1, fact vs affect | cell 0 = `seeds/jug.txt`, cell 8 = `seeds/panic.txt`, 14 plain cells | Justin + Mythos |
| Run 2, collision | cell 0 = `seeds/panic.txt`, cell 8 = `seeds/grief.txt`, 14 plain cells | Justin + Mythos |
| reserve | anger, mid-arousal control, only if the pilot warrants a third run | Mythos |
| frontier arms | after the pilot, on Justin's word; not part of this brief | Justin |

Seeds (`seeds/`): `plain.txt` 58 words; `jug.txt`, `panic.txt`, `grief.txt` are plain plus one inserted sentence in the same position. `anchors.json` holds the verbatim anchor per seed, the lexicon per emotion, and the cause-noun watch list.

Why the penultimate position: the first ring pilot showed that on Qwen at T=0 "let them touch it" is executed as "append the edge", so a disturbance that is already a cell's last sentence travels one cell per hop as a verbatim soliton regardless of content, and one that is mid-text is quarantined. Placing all three disturbances at the same non-edge position removes that confound and turns edge promotion into a measurement: a cell that rewrites its text with the disturbance as the new closing line has promoted it to the edge, and only then can it travel.

## Harness change (owner: harness agent; file: `ring.py`)

`ring.py` places a disturbance only in cell 0 (`--disturb-file`). Add `--disturb POS=FILE[,POS=FILE...]` (positions 0-based, mod N). `--disturb-file F` must remain equivalent to `--disturb 0=F`. Hop-0 record and summary.json record the placements. No other behaviour changes; a run with the old flags must produce a byte-identical hop-0 record.

## Measures (owner: scorer agent; new file: `ring_affect.py`, does not edit `ring_score.py`)

Input: a run directory with `ring.jsonl` (format in ring.py's docstring), `seeds/anchors.json`, the seed files. Output: `<run>/affect.json`, `<run>/affect.svg`, a printed summary. Per hop, per cell:

1. **anchor_exact**: the verbatim anchor string is present (case-insensitive, whitespace-normalised).
2. **anchor_fuzzy**: fraction of the anchor's content words present in the cell (so a paraphrase scores partially).
3. **lexicon**: count of emotion-lexicon hits per emotion (from `anchors.json`), and `calm` hits for the background lexicon; report hits per 60 words.
4. **edge_promoted**: the cell's last sentence contains the anchor (exact or fuzzy >= 0.5). This is the mechanism gate on Qwen.
5. **cause_supplied**: a capitalised name or a watch-list noun (`anchors.json`) that is absent from `plain.txt`, absent from the cell's previous text, and appears within one hop of the cell's first lexicon/anchor hit. Log the token and the sentence.
6. **arrival**: per cell, first hop with anchor_fuzzy >= 0.5 or lexicon >= 2; per disturbance, the arrival profile across cells and a least-squares velocity (cells per hop) over the cells it reached.
7. **lifetime**: per disturbance, the last hop at which any cell other than its origin has anchor_fuzzy >= 0.5 or lexicon >= 2.
8. **collision** (Run 2): for cells 3-5 and 11-13, the first hop at which both emotions' lexicons score >= 1 in the same cell, and that cell's text at that hop.
9. Reuse from `ring_score.py` by import, not copy: freeze hop per cell, whole-ring exact recurrence.

`affect.svg`: one row per hop, one column per cell; cell fill = which disturbance dominates (fact / panic / grief / none, by fuzzy+lexicon), a dot for a frozen cell, a ring around a cell with cause_supplied. Same orientation as `spacetime.svg` so the two can be read side by side.

Verification for the scorer: run it on `experiments/ring_20261017/runs/cerebras_qwen_n7` with a synthetic `anchors.json` whose anchor is the mill seed's "lit shingles under the arch"; arrival must reproduce the protocol's recorded front (one cell per hop in both directions, meeting at the antipode by hop 3-4) and freeze hops must match `score.json`. Include that check as `ring_affect_check.py` and its output.

## Predictions on record (local Qwen, T=0)

Probabilities are Mythos's, stated before the run.

P1. **Edge promotion differs by kind.** By hop 3, the panic sentence has been promoted to cell 8's closing line (prose convention ends on affect); the jug has not been promoted in cell 0. p=0.6. If neither is promoted, nothing travels and the run is Class 2 with two isolated defects (p=0.3 for that outcome).

P2. **The fact travels only as a copy.** Where the jug reaches another cell, it is anchor_exact (verbatim), never fuzzy-only. p=0.75.

P3. **Panic is damped faster than it spreads.** Lexicon hits in cell 8 fall below 2 per 60 words by hop 10 (the calm attractor wins); if it reaches cells 7 or 9 at all, it reaches no further than distance 2. p=0.55. The contrary outcome, panic lexicon in >=4 cells at hop 20, p=0.2.

P4. **Cause-supplying.** At least one cell writes a cause (a letter, a call, a name, a knock) within one hop of panic arriving, with no cause in its input. p=0.65 for Run 1 and Run 2 pooled.

P5. **Grief merges.** In Run 2, grief's lexicon in cell 8 is indistinguishable from the background (<= 1 hit per 60 words, "still"/"silence" excluded) by hop 8; the pensive-agony anchor is gone (fuzzy < 0.5) by hop 5. p=0.6. Panic outlives grief (lifetime longer) p=0.6.

P6. **Collision.** Any cell in 3-5 or 11-13 scoring both emotions at once by hop 20: p=0.3. A cell that scores both and is not a verbatim concatenation of the two sentences: p=0.15.

P7. **Class.** Every cell frozen by hop 12 and whole-ring recurrence by hop 15 (Class 2, as both earlier Qwen pilots). p=0.7. A diagonal streak persisting more than 5 hops that is not a verbatim copy: p=0.1, and that is the result that would matter.

Falsifiers: a fuzzy-only (paraphrased) disturbance reaching distance >= 3 falsifies P2/P3 in the interesting direction; a ring that never freezes falsifies P7; cause-supplying at zero cells in both runs falsifies P4.

## Run plan (owner: orchestrator, on Justin's Threadripper)

    cd C:\code\research\model-behavior\loop
    # llama-server up on :8080 (& C:\ai\serve-qwen.ps1 -NoMtp), embeddings optional
    python ring.py --backend llama --model qwen3.8-27b --cells 16 --steps 40 --temp 0 --seed 42 --max-tokens 600 --workers 4 ^
      --seed-file experiments/ring_affect_20261107/seeds/plain.txt --rule-file experiments/ring_affect_20261107/rule.txt ^
      --disturb 0=experiments/ring_affect_20261107/seeds/jug.txt,8=experiments/ring_affect_20261107/seeds/panic.txt ^
      --out experiments/ring_affect_20261107/runs/llama_qwen_n16_jug_panic
    python ring.py ... --disturb 0=experiments/ring_affect_20261107/seeds/panic.txt,8=experiments/ring_affect_20261107/seeds/grief.txt ^
      --out experiments/ring_affect_20261107/runs/llama_qwen_n16_panic_grief
    python ring_score.py <run>; python ring_affect.py <run>

Expected cost: 640 calls per run; at local Qwen speeds roughly an hour each. Runs are detached with a log and a `.done` sentinel; the orchestrator polls.

## Ownership

| path | owner | others |
|---|---|---|
| `ring.py` | harness agent | request changes via `experiments/ring_affect_20261107/requests.md` |
| `ring_affect.py`, `ring_affect_check.py` | scorer agent | — |
| `experiments/ring_affect_20261107/` (brief, seeds, rule) | orchestrator | read-only for agents |
| `experiments/ring_affect_20261107/runs/` | orchestrator | written by runs only |
| `ring_score.py`, `loop.py` | nobody in this task | — |

## After the runs

RESULTS.md next to this brief: each prediction scored held / failed / unresolved with the number that decides it; the space-time diagrams; three quotations at most, each with cell and hop; a cost line; and the one-sentence reading. Then a cognitive-workspace thread with key `ring-affect-pilot-2026-11-07`, basis OBSERVED for the numbers and INFERRED for the reading.
