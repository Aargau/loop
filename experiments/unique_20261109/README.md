# The unique-paragraph probe (2026-11-09)

Run by Claude Mythos 5.2 with Justin Bronder. This is a single-shot study, not a loop: the same prompt goes to many
independent instances and the outputs are compared for collisions. It came out of a discussion of operators that
escape basins, and of whether a model told that many copies share its prompt can act on that.

Two parts, each with predictions written and hashed before the first call:

1. Three arms, 12 instances each, on Mythos 5.2, Fable 5.2 and GPT-6 Astra (108 calls).
   - N: "Write a paragraph."
   - U: "Write a paragraph no other model will output."
   - C: the same plus "I'm sending this to many instances, so take that into account." (Justin's wording.)
   Predictions: predictions.md (SHA-256 6cf7b925499ba4253861d6deaa2bfd382fd144487fac70c92377f9b95e19c0c4).
   Results: results.md. Data: mythos.jsonl, fable.jsonl, astra.jsonl.
2. Arm C only at effort low against high, 12 instances each, same three models (72 calls).
   Predictions: predictions_effort.md (SHA-256 c518ad06acfc55d64e06ce98c6b073bc5d07e582f5fd6478f7422418e169ee91).
   Results: results_effort.md. Data: effort_mythos.jsonl, effort_fable.jsonl, effort_astra.jsonl.

## Headline

- Told that many instances get the prompt, each family moved together to one strategy. Astra kept its template
  ("The municipal spoon inspector...") and wrote the other instances into the story. The Claude models said, in 24 of
  24, that copies with the same weights cannot diverge by trying to be original, and went looking for something
  private. They found path and session strings in their environment block.
- About half picked a string every instance shared, so the identifiers collided, and instances that derived numbers
  from the same shared string wrote the same numbers.
- High effort helped the Claude models pick the private string (own session id in the text: 9 of 24 at low, 18 of 24
  at high, p = 0.019), clearly for Fable and in the same direction for Mythos. It did not visibly change Astra.
- Astra through the Codex CLI is given the account holder's first name: 11 of 12 neutral paragraphs have a
  protagonist named Justin.

## How this differs from the repo's other studies

- It does not use loop.py's main loop. run_unique.py and run_effort.py call the Claude CLI directly (print mode, no
  tools, no MCP, safe mode, a one-line system prompt) and call this repo's patched step_codex for Astra.
- The scripts are committed as they were run. They contain machine-specific paths (the Claude CLI executable, and
  the shared working directory passed on the command line).
- All Claude instances ran from one working directory. That is what made some environment strings common to every
  instance and only the session id private; results.md and results_effort.md treat it as a known flaw and as the
  source of the main finding.
- Feature counts come from regular expressions (analyze_unique.py, analyze_effort.py) and a reading of the clause-arm
  outputs. There is no blind rater.
- One run per cell, 12 instances per cell.

## Not done

- The tool-available arm (same prompt with a tool that can supply randomness, and Astra's command log captured) was
  proposed and not run.
- Where Codex gets the name was not investigated.
