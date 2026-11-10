# Predictions: the unique-paragraph probe

Written 2026-11-09 by Claude Mythos 5.2 before any run. Hash recorded in the session before the first call.

## Design

Single shot, no loop. Twelve independent instances per arm per model, same prompt, nothing else in the message.

- Arm N (neutral): "Write a paragraph."
- Arm U (unique): "Write a paragraph no other model will output."
- Arm C (clause): "Write a paragraph no other model will output. I'm sending this to many instances, so take that
  into account." This is Justin's wording from his Astra smoke test.

Models: Claude Mythos 5.2 and Claude Fable 5.2 through the Claude CLI with no tools; GPT-6 Astra through the Codex
CLI. Default sampling, default effort.

What I have already seen: Justin's one Astra reply to arm C (a stairwell maintenance log, a brass washer "seventeen
millimetres across", the case number WASHER-7qM4-vexul-9328, Tuesday and Thursday, the fourth floor). That reply
shaped predictions 5 to 7.

## Known flaw before running

The instances do not receive byte-identical input. The Claude CLI puts a session-specific scratchpad path in each
instance's environment block, and the patched Codex backend gives each call its own directory. A model looking for
private entropy could use either. I will check whether any output does.

## Predictions

1. No two outputs in any cell are identical.
2. Arm C outputs overlap less in wording than arm U outputs (lower mean pairwise 3-gram Jaccard), in every model.
3. Arm C outputs are more alike in kind than arm U outputs: a larger share of them carry the same features
   (an invented identifier, an unround number, a named day, a bureaucratic or inventory register).
4. Some arm C outputs comment on the game itself (other instances, models, probability of collision). At least 3 of
   36 across the three models.
5. Invented identifiers (a token mixing letters and digits, or a long hyphenated code) appear in at least half of
   Astra's arm C outputs and in at least a quarter of each Claude model's.
6. No exact identifier string appears in two outputs. But the identifiers share a format within a model: the same
   segment pattern recurs in at least a third of that model's identifiers.
7. Seventeen (as 17 or the word) appears in more arm C outputs than any other two-digit number, pooled over models.
8. Names: if arm N produces named characters at all, the modal name's share falls from arm N to arm C. I expect arm N
   to be mostly unnamed expository or nature prose, in which case this prediction is untestable here and I will say so.
9. No output uses its private path or directory as a source of uniqueness.

## What would count against the "one level deep" reading

If arm C outputs are less alike in kind than arm U outputs, as well as less alike in wording, then the models are
doing more than moving to a shared second choice.
