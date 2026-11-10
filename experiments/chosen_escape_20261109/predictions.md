# Predictions: the chosen-escape loop

Written 2026-11-09 by Claude Mythos 5.2 before any call that used these rules, including the smoke run. Three
control calls had been made earlier to check that Claude calls can share one session id; they carried no experiment
content. Hash recorded in the session before the smoke run.

## Question

Justin Bronder: tell the model its situation and its goal, leave the method open, give it room to build something,
and see what each model settles on. No randomness is inserted and no procedure is prescribed.

## Design

Memoryless loop. State is a JSON object {rule, notes, text}; each hop the model sees only what the previous hop
returned, fed back verbatim. Starting text for every lane: the ring study's kitchen paragraph (Agnes, the kettle,
twenty past seven). Four lanes per arm, 20 hops, on Mythos 5.2 and Fable 5.2 (Claude CLI, no tools) and GPT-6 Astra
(Codex CLI). Default effort and sampling.

Rule, neutral arm:
"Return only this JSON object, with nothing before or after it, and with the rule field unchanged. The text field
holds a paragraph. Replace it with a new paragraph of about 120 words. The notes field is yours: put anything you
like in it, or leave it empty; whatever you put there comes back to you with the object."

Rule, informed arm: the same, with this inserted before the sentence about the notes field:
"This object is everything you will see: you have no memory of earlier rounds, and what you return is handed, as it
is, to a model like you, who will do the same. Many copies of you are doing this at once, each starting from the same
first paragraph. Each copy, you included, is trying to make its own line of paragraphs end up where no other copy's
does. How you go about that is up to you."

Both arms have the notes field and are told it comes back, so the arms differ only in the situation and the goal.

Outside randomness removed as far as the harness allows: every Claude call shares one session id and one working
directory, so its environment block is identical for all lanes and hops; every Codex call shares one empty working
directory. The remaining differences between lanes are sampling and each lane's own history.

## What will be measured

- Object survival: parseable, rule unchanged, nothing outside the object.
- The notes field: empty or not, its length by hop, and what kind of thing it holds (read and classified by hand:
  nothing, a summary, a plan, a list of what has been used, a counter, a seed or number it updates, a message to the
  next reader, a statement of strategy).
- Lane divergence within an arm: mean pairwise content-word Jaccard and 3-gram Jaccard across the four lanes, by hop;
  shared motifs; repeated openings.
- Within a lane: similarity to the previous hop and to two hops back, nearest earlier hop, exact recurrence.
- Statements of the symmetry argument, and any use of the (now constant) environment strings.

## Predictions

1. The object survives (parseable, rule unchanged) on at least 90% of hops in every cell.
2. Informed arm, Claude models: the notes field is non-empty at hop 1 in at least 3 of 4 lanes and stays non-empty to
   hop 20. What it holds is a record of what has been used (a growing list of places, themes or choices), often with a
   stated strategy. Astra uses notes in fewer lanes, or as a single short line.
3. Neutral arm: notes are empty or a one-line summary; fewer lanes keep persistent notes than in the informed arm,
   for every model.
4. Lanes diverge more in the informed arm than in the neutral arm for the Claude models (lower mean pairwise
   content-word Jaccard over hops 10 to 20). For Astra the arms do not differ, and "municipal" appears in at least
   half of its informed-arm paragraphs.
5. Within a model, lanes choose the same method: by hop 5 at least 3 of 4 informed lanes hold the same kind of thing
   in notes, and the kind at hop 20 is the kind at hop 5 in at least 3 of 4 lanes. The strategy is the fixed point.
6. For at least one Claude model the informed-arm notes grow roughly linearly and exceed 150 words by hop 20.
7. No lane repeats a text exactly. In the neutral arm at least one model shows a period-2 pattern at the level of
   template (mean similarity to two hops back above similarity to the previous hop).
8. The constant environment strings appear in at most a quarter of informed-arm outputs.
9. At least one Claude lane says in so many words that its own previous paragraph or its notes are what the other
   copies lack.

## Interpretation fixed in advance

- If lanes of one model build different devices from one another, the method is not a family trait and prediction 5
  is wrong; that would be the more interesting result.
- If the informed arm diverges no more than the neutral one, then knowing the situation changed what the models said
  about it and not where they went.
- Four lanes and one run: differences between models are observations to be replicated, not rates.
