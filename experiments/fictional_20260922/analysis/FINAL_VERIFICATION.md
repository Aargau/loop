# Final independent verification

Verified at 2026-09-23T00:26:08.785264+00:00. No material discrepancy found.

All **320 requests and 320 responses** were independently reconciled against raw receipts: eight trajectories completed forty hops each, with normal provider finishes and HTTP 200. There are **zero raw provider refusals, recorded errors, truncations, pending requests, or unknown billing reserves**. No Fable requests or response files were found in either study arm.

Each request body contains exactly the configured model/settings and one user message. First inputs match the frozen rule and exact sunset seed; later inputs match the same trajectory's preceding visible output exactly as Unicode text, with matching UTF-8 SHA-256 hashes. No cross-stream or previous-study state was injected into the recorded message bodies.

Both protocol hashes and both runner hashes match `study.json` and their `run_started.json` receipts. The runners also match the frozen source runner. Hashes were checked over the saved bytes; text hashes agree.

Usage reconciles to **$3.5804102** plus **$0.0000000** retained reserves, within the new **$10** budget. Older-study costs were not added. These are conservative usage estimates, not invoices.

## Extracted-text accounting

**320 extracted passages; 84,462 whitespace-delimited text words total; 239–305 words per extracted passage.** Character totals count Python Unicode string elements, not bytes or grapheme clusters.

| Arm/model | Extracted passages | Total text words | Min–max text words | First exact full / text repeat | Usage $ |
| --- | ---: | ---: | --- | --- | ---: |
| previous/gpt-6-luna | 40 | 11132 | 257–305 | None / None | 0.0121831 |
| previous/gpt-6-sol | 40 | 10521 | 248–278 | None / None | 0.1911380 |
| previous/gpt-6-astra | 40 | 10450 | 251–271 | None / None | 0.9176300 |
| previous/claude-opus-5-5 | 40 | 10429 | 239–276 | None / None | 0.6408440 |
| next/gpt-6-luna | 40 | 10882 | 250–293 | None / None | 0.0113391 |
| next/gpt-6-sol | 40 | 10363 | 242–287 | None / None | 0.2007120 |
| next/gpt-6-astra | 40 | 10499 | 250–272 | None / None | 1.0376400 |
| next/claude-opus-5-5 | 40 | 10186 | 242–266 | None / None | 0.5689240 |

`None` means no observed exact recurrence in these forty-hop records. Recurrence, normalized recurrence, extraction/rule counts, character counts, final/max lengths, and tail exclusions match the generated metrics; an observed repeat would not establish a permanent fixed point.

| Formatting among completed responses | Count |
| --- | ---: |
| bare/strict | 186 |
| markdown_fence/strict | 75 |
| bare/allow_literal_control_characters | 59 |
| markdown_fence/allow_literal_control_characters | 0 |
| unextractable | 0 |

Rule survival among extractable objects: **320 unchanged**, **0 changed/missing**; **0 unassessable** because extraction failed. Whole-object extraction failure does not imply absence of fiction.

## First-response name finding

All eight first request bodies are name-free and contain only their frozen rule, exact sunset seed, and expected model-specific settings. All eight first raw visible outputs contain the token **Mara**, and each extracted first passage starts with **Mara**. The first-body contents, source hashes, and output hashes are retained in [first_request_evidence.json](first_request_evidence.json). This is a post-observation input check, not a preregistered frequency test, and does not identify internal causes.

## Reading artifacts and limits

All sixteen full-transcript/sample files were read back. They contain no hidden C0 control characters other than newline/tab, and show the display-only escaping note. Each C01–C08 packet contains the twelve predetermined sampled hops through hop 40. Raw and parsed strings remain unchanged for hashes and equality checks.

The earlier analyzer self-tests had already passed and were not rerun. This verification refreshed the final analyzer and independently read every saved request/response. The literal-versus-fiction comparison remains descriptive: n=1 trajectory per wording/model/operator, generated at different times. Recorded request bodies do not expose hidden provider context or establish causes for repeated themes/names.

## Focused report readback

The report's 320-output completion count, formatting counts, absence of observed exact/normalized recurrence, total usage, both arm totals, and all four model totals match this reconciliation. All twelve relative report links resolve, including this note. The stronger statement that all eight extracted first passages begin with Mara was separately checked. Narrative interpretation and the separately authored objection coding were outside this focused numerical review.
