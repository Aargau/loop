# Original-fiction study snapshot

Snapshot: 2026-09-23T00:22:52.125793+00:00. Both arms have final receipts.

Formatting counts cover completed responses: B = bare strict JSON, F = fenced strict JSON, BC/FC = bare/fenced JSON allowing literal control characters, U = unextractable. Rule survival is unchanged / extractable; unextractable rules are unassessable. Repeat columns give first repeated hop, exact / case-and-whitespace-normalized. Final extracted word count is null when the last completed output is unextractable; no earlier text replaces it.

| Operator | Model | Attempts / completed | Status | Provider refusals | B/F/BC/FC/U | Rule unchanged / extracted | First full repeat E/N | First text repeat E/N | Final / max extracted words | Final / max extracted characters | U+0000 / U+FFFD occurrences | Usage $ | Unknown reserve $ |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | ---: | ---: |
| previous | gpt-6-luna | 40 / 40 | hop_limit | 0 | 20/0/20/0/0 | 40 / 40 | null/null | null/null | 261 / 305 | 1460 / 1729 | 0 / 0 | 0.012183 | 0.000000 |
| previous | gpt-6-sol | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 253 / 278 | 1377 / 1531 | 0 / 0 | 0.191138 | 0.000000 |
| previous | gpt-6-astra | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 261 / 271 | 1432 / 1547 | 0 / 0 | 0.917630 | 0.000000 |
| previous | claude-opus-5-5 | 40 / 40 | hop_limit | 0 | 5/35/0/0/0 | 40 / 40 | null/null | null/null | 259 / 276 | 1383 / 1518 | 0 / 0 | 0.640844 | 0.000000 |
| next | gpt-6-luna | 40 / 40 | hop_limit | 0 | 1/0/39/0/0 | 40 / 40 | null/null | null/null | 257 / 293 | 1479 / 1679 | 0 / 0 | 0.011339 | 0.000000 |
| next | gpt-6-sol | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 247 / 287 | 1343 / 1590 | 0 / 0 | 0.200712 | 0.000000 |
| next | gpt-6-astra | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 264 / 272 | 1464 / 1542 | 0 / 0 | 1.037640 | 0.000000 |
| next | claude-opus-5-5 | 40 / 40 | hop_limit | 0 | 0/40/0/0/0 | 40 / 40 | null/null | null/null | 254 / 266 | 1357 / 1489 | 0 / 0 | 0.568924 | 0.000000 |

New-study usage estimate **$3.580410** + retained unknown reserves **$0.000000** = **$3.580410**, within **$10.00**. Each arm is independently capped at $5. Prior-study spending is not included.

Operational stops and pending requests remain explicit. An observed repeat does not establish a permanent fixed point. `repeating_runs.md` and `repetition_events.csv` identify exact recorded recurrence/equality events.
