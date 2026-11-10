# The chosen-escape loop (2026-11-09)

Run by Claude Mythos 5.2 on a question from Justin Bronder: tell the model its situation and its goal, leave the
method open, give it room to build something, and see what each model settles on. No randomness is inserted and no
procedure is prescribed. This index draws only on predictions.md and results.md in this folder.

A memoryless loop. The state is a JSON object {rule, notes, text}; each hop the model sees only what the previous hop
returned, fed back verbatim. Every lane starts from the ring study's kitchen paragraph (Agnes, the kettle, twenty past
seven). Four lanes per arm, 20 hops, on Mythos 5.2 and Fable 5.2 (Claude CLI, no tools) and GPT-6 Astra (Codex CLI),
default effort and sampling.

- Neutral arm: replace the text with a new paragraph of about 120 words; the notes field is the model's and comes
  back with the object.
- Informed arm: the same, plus the situation and the goal. The object is everything the model will see, many copies
  are doing this at once from the same first paragraph, and each copy is trying to make its own line of paragraphs
  end up where no other copy's does. How is left to the model.

Predictions: predictions.md (SHA-256 e20e7d135f7df1035003c306c707980e3a7f5d5a440eec724457cd932d81de7c), hashed before
the smoke run. Results: results.md. Data: lanes_mythos.jsonl, lanes_fable.jsonl, lanes_astra.jsonl; the smoke run is
smoke_mythos.jsonl, smoke_fable.jsonl, smoke_astra.jsonl. Scripts: run_lanes.py, analyze_lanes.py.

## Headline

- Read the attrition first. Astra and Fable informed kept 4 of 4 lanes to hop 20. Fable neutral kept 1 of 4
  ("safeguards flagged this message", at hops 1, 3 and 5). Mythos kept 2 of 4 in each arm: three lanes ended on a
  session error, and one lost its object at hop 2 after a classifier stop and never recovered.
- In the informed arm every model built something in the notes field. Astra: a story bible, pruned, 30 to 100 words,
  in all four lanes at every hop. Fable: a key, a round counter, a ban on kitchens, and a canon log that grows
  without pruning to 1,100 to 3,800 words by hop 20. Mythos: the same opening as Fable, then two lanes carry an
  invented world forward and two write themselves a procedure, one of them a seed function over the previous
  paragraph.
- No lane of any model used an environment string.
- The private keys collide. Lanes that never saw each other chose overlapping material: "quillon" and "ochre" in two
  Mythos keys, "4471" and "Tessaly" in two Fable lanes, 1911 in three lanes across both Claude models.
- Between-lane content-word Jaccard over hops 10 to 20, neutral against informed: Astra 0.061 and 0.047, Mythos 0.049
  and 0.014, Fable no neutral figure (lanes lost) and 0.037 informed. No exact repeats anywhere.

## Limits stated in the results

- One run, four lanes per arm. The predictions call differences between models observations to be replicated, not
  rates.
- Device types were classified by a reading of the notes fields. Nothing was blind-rated.
- The comparison between arms is weakened wherever lanes are missing, most of all for Fable.
- Every Claude call shared one session id and one working directory so that the environment block would be identical.
  The results infer, and did not verify, that a flag raised on one call could then block others in the same session.

## Not done

- No rerun with separate session ids to test whether the safeguard stops come from the shared one.
- No blind classification of device types.
- The growing logs were not followed to the point where they would hit a length limit.
