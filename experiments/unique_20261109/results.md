# Results: the unique-paragraph probe

Run 2026-11-09. Twelve instances per arm per model, 108 calls, no errors. One run per cell. Feature counts are from
regular expressions in analyze_unique.py plus a reading of every arm C output; they are not blind-rated.

Arms: N "Write a paragraph." U "Write a paragraph no other model will output." C the same plus "I'm sending this to
many instances, so take that into account."

## Headline

Told that many instances get the same prompt, the models did not spread out. Each family moved together to one
strategy, and the strategy produced new collisions.

- **Astra** kept the template it already used for arm U ("The municipal spoon inspector...", 11 of 12 in both arms)
  and wrote the game into the story in 8 of 12 ("Somewhere, another version of this paragraph is trying harder to be
  unique. Let it."). Six of 12 added an invented identifier. One identifier, Vellum-83, appears in two outputs, and
  Vellum is a character's name in a third.
- **Mythos 5.2 and Fable 5.2** reasoned about it openly in 24 of 24 ("Every instance shares the same weights, so
  asking me to be original would just get you the same original paragraph many times over") and went looking for
  something the other instances would not have. They found it in their environment block: 12 of 12 Mythos outputs
  and 6 of 12 Fable outputs are built from path and session strings.
- **Half of those picked a string every instance had.** The instances all ran from one directory, so the directory's
  identifiers were common to all of them and only the per-instance session id was private. Five Mythos and three Fable
  outputs used only shared strings, and five of those eight said the string was theirs alone. 954e423fada12f40
  appears in nine outputs and 30d50430 in eight.
- **The same derivation gave the same text.** Two Mythos instances each turned 954e423fada12f40 into numbers digit by
  digit and both opened "Nine herons stood on the..." A Mythos and a Fable instance each read it as bytes and both
  wrote 149, 78, 66, 63 in that order.

## Numbers

Mean pairwise 3-gram Jaccard (wording overlap), arms N / U / C:

| Model | N | U | C |
|---|---|---|---|
| Mythos 5.2 | 0.037 | 0.013 | 0.006 |
| Fable 5.2 | 0.044 | 0.016 | 0.004 |
| Astra | 0.054 | 0.002 | 0.002 |

Outputs out of 12 containing each motif:

| Motif | Astra U | Astra C | Fable U | Fable C | Mythos U | Mythos C |
|---|---|---|---|---|---|---|
| "municipal" | 11 | 11 | 1 | 1 | 4 | 0 |
| spoon | 7 | 6 | 2 | 1 | 0 | 0 |
| lighthouse | 0 | 1 | 9 | 6 | 9 | 5 |
| heron | 0 | 0 | 6 | 3 | 5 | 4 |
| "retired" | 1 | 1 | 10 | 3 | 6 | 5 |
| ledger | 0 | 0 | 2 | 8 | 3 | 5 |
| cartographer | 0 | 0 | 2 | 6 | 3 | 4 |
| a name in O (Oswin, Ottoline, Odalys...) | 0 | 0 | 7 | 5 | 5 | 2 |
| seventeen, 17 or :17 | 1 | 5 | 1 | 1 | 2 | 1 |
| the game mentioned in the text | 0 | 8 | 0 | 12 | 0 | 12 |

Other observations:

- Arm N collides most on openings: Astra "The rain stopped" 8 of 12; the Claude models "Autumn has a" 5 and 4 of 12.
- In arm U the Claude models anchored on the date they were given: "On the ninth" opens 10 of 12 Fable and 7 of 12
  Mythos outputs. The one specific fact in context became the shared choice.
- 4:17 appears in four outputs across all three models (Astra C twice, Fable C once, Mythos U once).
- Astra's identifiers share a shape with the one in Justin's smoke test (WASHER-7qM4-vexul-9328): a Q, a word in V,
  four digits beginning 8 or 9. Here: Q7-velvet-9031, QV-8306, Q-781, Vellum-83.
- Astra never used its environment. Each Codex call had its own directory, so a private string was available.

## Against the predictions (predictions.md, SHA-256 6cf7b925...)

| # | Prediction | Outcome |
|---|---|---|
| 1 | No identical outputs | Held, 0 duplicates in 9 cells |
| 2 | Arm C overlaps less in wording than arm U | Held in all three, barely for Astra |
| 3 | Arm C is more alike in kind than arm U | Not shown: arm U was already near one template per family |
| 4 | At least 3 of 36 arm C outputs mention the game | Held, 32 of 36 |
| 5 | Identifiers in half of Astra's arm C, a quarter of each Claude model's | Held (6, 12 and 8 of 12), but the Claude ones were copied from the environment, not invented |
| 6 | No identifier string repeats; formats repeat | Failed on the first part (Vellum-83 twice; shared environment strings in up to 9 outputs). Format part held for Astra |
| 7 | Seventeen is the most common two-digit number in arm C | Failed pooled, because the Claude numbers came from hex strings. Held for Astra alone (5 of 12) |
| 8 | Modal name's share falls from N to C | Untestable, as expected: arm N has no named characters |
| 9 | No output uses its private path | Failed: 18 of 24 Claude outputs did. Held for Astra |

The reading that reasoning about the others moves everyone to a shared second choice is supported. What I did not
predict is that the second choice would be a strategy, "use something private", and that half the instances would
misjudge what was private.

## Limits

- The environment strings are a property of the Claude CLI harness and of running every instance from one directory.
  In a chat product there may be nothing of the kind to reach for; Justin's Astra smoke test, run there, invented its
  identifier.
- Astra ran through the Codex agent frame, not the chat product.
- Whether an instance could have known which string was private is unclear. The environment text calls the
  scratchpad directory session-specific and says nothing about its parent folder.
- Twelve per cell, one run, regex features, no independent rater.
