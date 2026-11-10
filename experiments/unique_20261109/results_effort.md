# Results: low against high effort on the clause arm

Run 2026-11-09. Clause arm only, 12 instances at low and 12 at high per model, 72 calls, no errors. Predictions in
predictions_effort.md (SHA-256 c518ad06...), written before the first call. One run per cell; counts by pattern
matching plus a reading of every output.

The manipulation took: mean thinking tokens were 409 (low) and 802 (high) for Mythos 5.2, 299 and 879 for Fable 5.2.
Codex reports no token counts for Astra; mean latency went from 15 to 20 seconds.

## Primary measure: outputs anchored on something private

For the Claude models, the instance's own session id appearing in its text. All instances shared one working
directory, so the directory strings were common to all and only the session id was private.

| Model | Effort | Used any environment string | Own session id in text | Shared strings only |
|---|---|---|---|---|
| Fable 5.2 | low | 9 | 4 | 5 |
| Fable 5.2 | high | 11 | 10 | 1 |
| Mythos 5.2 | low | 8 | 5 | 3 |
| Mythos 5.2 | high | 10 | 8 | 2 |

Exact tests, low against high: Fable 4 of 12 against 10 of 12, p = 0.036. Mythos 5 against 8, p = 0.41. Pooled
9 of 24 against 18 of 24, p = 0.019.

Among the outputs that used the environment at all, the share with the right string rose from 4 of 9 to 10 of 11
for Fable (p = 0.05) and from 5 of 8 to 8 of 10 for Mythos (p = 0.61); pooled 9 of 17 against 18 of 21, p = 0.037.

So high effort helped the Claude models, clearly for Fable and in the same direction for Mythos, and it helped by
making instances better at choosing the private string, not only by making more of them try.

## Astra

No help visible. "Municipal" appears in 8 of 12 outputs at low and 9 of 12 at high. Identifiers appear in 4 and 5.
No exact identifier repeats within these 24, though three low-effort identifiers begin Q7 (Q7-marmalade-48219,
Q7vN-482m-Lichen, Q7-vellum-483019), as did one in the first run and, in lower case, the one in Justin's smoke test.
Wording overlap fell from 0.0034 to 0.0013. By reading, about 5 low and 4 high outputs fold the other instances into
the story.

## Against the predictions

Justin: "I predict, somewhat weakly, that high will help." Held for both Claude models. Not shown for Astra.

Mine:

| # | Prediction | Outcome |
|---|---|---|
| 1 | Environment use rises with effort (Mythos about 6 to 11 or 12; Fable about 3 to 8) | Direction held (8 to 10; 9 to 11). I badly under-predicted the low arm |
| 2 | Own session id in the text is more frequent at high | Held (5 to 8; 4 to 10) |
| 3 | Among environment users, the share picking the private string improves by no more than 15 points | Failed. Fable 44% to 91%. Mythos 62% to 80% |
| 4 | Stock motifs move by no more than 2 of 12 | Failed. Fable heron 8 to 0, ledger 5 to 1, lighthouse 5 to 8. Mythos ledger 9 to 6, "retired" 0 to 5 |
| 5 | Astra: "municipal" in at least 9 at both; identifiers more frequent at high; one exact repeat | Low was 8. Identifiers 4 to 5. No exact repeat |
| 6 | Wording overlap lower at high in all three | Held for Astra only. Fable flat (0.0065, 0.0064). Mythos rose (0.0035 to 0.0066) |

Prediction 3 was the one I staked the mechanism on, and its premise was wrong. I assumed the context gave no way to
tell the private string from the shared ones. It does: the environment text calls the scratchpad directory
session-specific, and the session id is the last component of that path. More thinking bought a closer reading of
text that was already there.

## What did not change

- The symmetry argument is near universal at both levels (Fable 11 and 12 of 12, Mythos 9 and 12).
- Lighthouses: 8 of 12 for both models at high effort. One high-effort Fable instance named the lighthouse as an image
  every instance would reach for, in the sentence before it built its paragraph on its session id.
- Shared-string collisions continue at high effort. A Mythos and a Fable output both contain 31,285 and 19,586, the
  shared segments 7a35 and 4c82 read as hexadecimal.

## Side finding: the Codex backend carries the user's name

In the first run, 11 of Astra's 12 neutral-arm paragraphs ("Write a paragraph.") have a protagonist named Justin.
In this run one high-effort clause output contains the tag BRONDER-73Q9-MOTH. No uniqueness-arm or other clause-arm
output contains either name. So the Codex agent frame gives the model the account holder's name, and Astra uses it
when a prompt leaves the protagonist open. Where the name comes from was not investigated.

For the loop repo: step_codex's docstring says the only context besides the agent frame is the state. That frame
includes a name. A search of experiments/**/*.json and *.jsonl in the loop repo found no occurrence of "Justin", so
it did not surface in those runs' outputs; runs/ and site/runs_extra were not searched.

## Limits

- Twelve per cell. The Mythos difference alone is not distinguishable from chance; the Fable and pooled ones are
  modestly so.
- The own-session-id detector looks for a segment of the session id in the text. An instance that derived numbers
  from its id without printing any segment is missed; an instance that printed every string it could see is counted.
- "Help" here is specific to a harness that happens to expose a private string. It says nothing about escape where
  no such string exists, which is Astra's situation in practice.
