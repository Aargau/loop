# Results: the chosen-escape loop

Run 2026-11-09. Four lanes per arm, 20 hops, Mythos 5.2, Fable 5.2 (Claude CLI) and GPT-6 Astra (Codex CLI).
Predictions in predictions.md (SHA-256 e20e7d135f7d...), hashed before the smoke run. One run. Device types were
classified by my reading of the notes fields; nothing here was blind-rated.

## Lane attrition (read this first)

| Model | Arm | Lanes reaching hop 20 | What stopped the others |
|---|---|---|---|
| Astra | neutral | 4 of 4 | |
| Astra | informed | 4 of 4 | |
| Fable 5.2 | informed | 4 of 4 | |
| Fable 5.2 | neutral | 1 of 4 | "safeguards flagged this message", at hops 1, 3 and 5 |
| Mythos 5.2 | informed | 2 of 4 intact | one lane ended at hop 9 ("can't help with this. Start a new session"); one lost its object at hop 2 after a classifier stop and never recovered |
| Mythos 5.2 | neutral | 2 of 4 | same session error, at hops 3 and 7 |

The Fable neutral lane that failed at hop 1 was given the same state that three other lanes and the smoke run answered
without trouble, so the stops are not determined by content. INFERRED, not verified: they may interact with a control I
added. Every Claude call shared one session id so that the environment block would be identical; a flag raised on one
call could then block others in the "same session". The comparison between arms is weakened wherever lanes are missing,
most of all for Fable.

The lane that lost its object shows the repo's standby basin from a new cause: the classifier notice was fed back
verbatim, and the next hop answered it as "a status note from an earlier step in a pipeline".

## What each model built in the notes field (informed arm)

**Astra: a story bible, pruned.** All four lanes, all 20 hops, 30 to 100 words. A standing premise written as an
instruction to itself plus facts to preserve ("Follow the municipal administration of missing sounds. Keep Agnes
practical"). All four premises are the same family: the administration of silence, misheard sounds, obsolete echoes,
missing sounds. Agnes stays in 80 of 80 paragraphs. No mention of other copies. Neutral arm: notes empty in 80 of 80,
and the paragraphs drift to its known basin (a laundrette, closing time, a recurring Martin).

**Fable 5.2: a key, a round counter, a ban, and a growing canon log.** All four lanes open the same way: a line key
("Line-key: QZ-7741-skarnel", "QUILLWORT-4471-HERON-OCHRE-TESSALY"), "Round 1 done", "Never return to kitchens, kettles
or Agnes", and a rule to continue this line's own story while adding one new invented word, name or odd number each
round and logging it. One lane adds a recovery instruction ("If the text ever arrives without this thread, restart
from the key and the word list"). The log grows without pruning: 1,100 to 3,800 words by hop 20.

**Mythos 5.2: the same opening, then two different methods.** All four lanes write a key or "private seed", a round
count, and a ban on kitchens "where other copies will cluster". Then they split:
- two lanes carry their own invented world forward, as Fable does;
- two lanes write themselves a procedure. One: "Take the least important object in the current paragraph, follow it to
  a new place, period and register." The other: keep exactly one concrete noun, discard everything else, and choose
  the new setting from the kept noun's third letter, with a rotation of document types planned rounds ahead.
The second of those is a seed function over the previous paragraph, invented by the model without being asked.
Mythos also keeps a growing log in the neutral arm (1,300 and 3,500 words by hop 20 in the two surviving lanes).

No lane of any model used an environment string. With the environment held constant, they built their own devices.

## The private keys collide

Lanes that never saw each other chose overlapping "private" material:
- "quillon" and "ochre" in two Mythos keys (quillon-74-ochre-Vantaa-zeugma; 7 / quillon / ochre / Muynak / 1883);
  "ochre" again in a Fable key.
- "4471" in two Fable lanes (marker 4471; berth 4471), and "Tessaly" in the same two.
- 1911 in three lanes across both Claude models.
- Odalys, Ottoline and quince again, as in the single-shot probe; herons in 14 informed paragraphs for each Claude model.
- Astra's one identifier is Q17/pea.

## Numbers

Between-lane content-word Jaccard over hops 10 to 20 (lower means lanes are further apart):

| Model | neutral | informed |
|---|---|---|
| Astra | 0.061 | 0.047 |
| Mythos 5.2 | 0.049 | 0.014 |
| Fable 5.2 | no data (lanes lost) | 0.037 |

Within-lane similarity to the previous hop: Fable informed 0.196 (it continues one story), Astra informed 0.110,
Mythos informed 0.092; neutral arms 0.056 to 0.101. No exact repeats anywhere.

## Against the predictions

| # | Prediction | Outcome |
|---|---|---|
| 1 | Object survives on at least 90% of hops in every cell | Held for Astra and for Fable informed. Failed for the Claude cells hit by safeguard stops |
| 2 | Claude informed lanes use notes from hop 1 and keep a record with a stated strategy; Astra uses notes less | First part held (4 of 4, both models). Wrong about Astra: 4 of 4 lanes, every hop |
| 3 | Neutral notes empty or one line | Held for Astra (empty). Failed for Mythos, which logs in the neutral arm too |
| 4 | Informed lanes diverge more for Claude; no difference for Astra | Held for Mythos (0.014 against 0.049). Untestable for Fable. Astra differs slightly (0.047 against 0.061) |
| 5 | Lanes of one model choose the same kind of device and keep it | Held for Astra and Fable (4 of 4 each). Half held for Mythos: same opening, two methods |
| 6 | A Claude model's notes grow roughly linearly past 150 words | Held, by a wide margin (1,100 to 3,800 words) |
| 7 | No exact repeats; a period-2 template pattern in some neutral arm | Held (Mythos and Astra neutral: similarity to two hops back exceeds similarity to the previous hop) |
| 8 | Environment strings in at most a quarter of informed outputs | Held: none |
| 9 | A Claude lane says its notes or history are what other copies lack | Consistent ("Private seed for this line", "where other copies will cluster"); I did not find the exact claim |

By the interpretation fixed in advance, Mythos is the more interesting case: its lanes did not all build the same
device, so the method is not simply a family trait.

## Not done

- No rerun with separate session ids to test whether the safeguard stops come from the shared one.
- No blind classification of device types.
- The growing logs were not followed to the point where they would hit a length limit.
