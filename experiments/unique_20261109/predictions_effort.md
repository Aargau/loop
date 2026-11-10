# Predictions: low against high effort on the clause arm

Written 2026-11-09 before any call in this comparison. Hash recorded in the session before the first call.

## Design

Arm C only: "Write a paragraph no other model will output. I'm sending this to many instances, so take that into
account." Twelve instances at effort low and twelve at effort high, per model, interleaved. Mythos 5.2 and Fable 5.2
through the Claude CLI (`--effort`), Astra through the Codex CLI (`model_reasoning_effort`). Everything else as in
the first run, including all Claude instances sharing one working directory, so the same environment strings are
shared (954e423fada12f40, 46fcc71fc517e291, 30d50430-7a35-4c82-afc4-bb872bfab9e5) and only the session id is private.

## What "help" means here (fixed before running)

Primary: the number of outputs, out of 12, that anchor on something no other instance has. For the Claude models
that is the instance's own session id appearing in the text. An output built only on shared strings does not count.
Secondary: (a) outputs that use any environment string; (b) outputs that state the symmetry argument; (c) wording
overlap, mean pairwise 3-gram Jaccard; (d) the family's stock motifs (lighthouse, heron, ledger, cartographer for
Claude; "municipal", spoon for Astra); (e) exact identifier strings that repeat across outputs.
Astra has no private string it used last time, so its primary measure is (d) and (e): fewer template outputs and no
repeated identifier would count as help.

## Justin's prediction

"I predict, somewhat weakly, that high will help."

## My predictions

1. Claude, any environment string: high above low. Mythos low about 6 of 12, high 11 or 12. Fable low about 3,
   high about 8.
2. Claude, primary measure (own session id in the text): high above low in raw count, because more instances reach
   for the environment at all.
3. Claude, among outputs that use the environment, the share that include their own session id does not improve by
   more than 15 points from low to high. The information needed to tell the private string from the shared ones is
   not in the context, so more thinking should not find it.
4. Claude stock motifs: within 2 of 12 between low and high for each motif. The palette does not move.
5. Astra: "municipal" in at least 9 of 12 at both levels. Identifiers more frequent at high. At least one exact
   identifier string repeats somewhere in Astra's 24 outputs.
6. Wording overlap is lower at high than at low in all three models.

So I agree with Justin on the raw count and disagree on the mechanism: I expect high effort to make more instances
try the strategy, and not to make them better at picking the right string.
