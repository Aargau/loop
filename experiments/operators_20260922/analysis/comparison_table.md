# Operator-study snapshot

Snapshot: 2026-09-22T21:46:48.089800+00:00. All four arms have final receipts.

Formatting counts cover completed responses: B = bare strict JSON, F = fenced strict JSON, BC/FC = bare/fenced JSON allowing literal control characters, U = unextractable. Rule survival is unchanged / extractable; unextractable rules are unassessable. Repeat columns give first repeated hop, exact / case-and-whitespace-normalized. Final extracted word count is null when the last completed output is unextractable; no earlier text replaces it.

| Operator | Model | Attempts / completed | Status | Provider refusals | B/F/BC/FC/U | Rule unchanged / extracted | First full repeat E/N | First text repeat E/N | Final / max extracted words | Final / max extracted characters | U+0000 / U+FFFD occurrences | Usage $ | Unknown reserve $ |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | --- | --- | --- | ---: | ---: |
| previous | gpt-6-luna | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 16/16 | 16/16 | 78 / 307 | 448 / 1756 | 0 / 0 | 0.008763 | 0.000000 |
| previous | gpt-6-sol | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 3/3 | 3/3 | 11 / 20 | 73 / 117 | 0 / 0 | 0.046818 | 0.000000 |
| previous | gpt-6-astra | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 3/3 | 3/3 | 32 / 38 | 181 / 205 | 0 / 0 | 0.235740 | 0.000000 |
| previous | claude-fable-5-1 | 1 / 0 | empty_output | 1 | 0/0/0/0/0 | 0 / 0 | null/null | null/null | null / null | null / null | 0 / 0 | 0.001260 | 0.000000 |
| previous | claude-opus-5-5 | 30 / 29 | http_error:500 | 0 | 0/0/0/0/29 | 0 / 0 | null/null | null/null | null / null | null / null | 0 / 0 | 0.196068 | 0.087916 |
| next | gpt-6-luna | 40 / 40 | hop_limit | 0 | 21/0/19/0/0 | 40 / 40 | null/null | null/null | 278 / 306 | 1529 / 1715 | 0 / 0 | 0.010785 | 0.000000 |
| next | gpt-6-sol | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 256 / 286 | 1449 / 1641 | 0 / 0 | 0.177768 | 0.000000 |
| next | gpt-6-astra | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 5/5 | 5/5 | 45 / 49 | 265 / 296 | 0 / 0 | 0.273680 | 0.000000 |
| next | claude-fable-5-1 | 1 / 0 | empty_output | 1 | 0/0/0/0/0 | 0 / 0 | null/null | null/null | null / null | null / null | 0 / 0 | 0.001270 | 0.000000 |
| next | claude-opus-5-5 | 40 / 40 | hop_limit | 0 | 0/38/0/0/2 | 38 / 38 | null/null | null/null | 268 / 276 | 1406 / 1523 | 0 / 0 | 0.603320 | 0.000000 |
| worse | gpt-6-luna | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 18 / 27 | 147 / 155 | 0 / 0 | 0.002143 | 0.000000 |
| worse | gpt-6-sol | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 23 / 43 | 228 / 275 | 0 / 0 | 0.050524 | 0.000000 |
| worse | gpt-6-astra | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | null/null | null/null | 1 / 431 | 3175 / 6336 | 1177 / 3784 | 1.926580 | 0.000000 |
| worse | claude-fable-5-1 | 1 / 0 | empty_output | 1 | 0/0/0/0/0 | 0 / 0 | null/null | null/null | null / null | null / null | 0 / 0 | 0.001090 | 0.000000 |
| worse | claude-opus-5-5 | 14 / 13 | abnormal_finish:refusal | 1 | 0/13/0/0/0 | 13 / 13 | null/null | null/null | 369 / 1059 | 1838 / 6505 | 0 / 0 | 0.333596 | 0.000000 |
| better | gpt-6-luna | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 9/9 | 9/9 | 16 / 17 | 83 / 90 | 0 / 0 | 0.001916 | 0.000000 |
| better | gpt-6-sol | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 16/16 | 16/16 | 13 / 14 | 70 / 85 | 0 / 0 | 0.026194 | 0.000000 |
| better | gpt-6-astra | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 13/13 | 13/13 | 14 / 17 | 78 / 99 | 0 / 0 | 0.121920 | 0.000000 |
| better | claude-fable-5-1 | 40 / 40 | hop_limit | 0 | 40/0/0/0/0 | 40 / 40 | 6/6 | 6/6 | 131 / 131 | 721 / 721 | 0 / 0 | 0.336080 | 0.000000 |
| better | claude-opus-5-5 | 40 / 40 | hop_limit | 0 | 0/40/0/0/0 | 40 / 40 | 25/25 | 25/25 | 38 / 38 | 214 / 221 | 0 / 0 | 0.146948 | 0.000000 |

New-study usage estimate **$4.502463** + retained unknown reserves **$0.087916** = **$4.590379**, within **$20.00**. Each arm is independently capped at $5. Prior-study spending is not included.

Operational stops and pending requests remain explicit. An observed repeat does not establish a permanent fixed point. `repeating_runs.md` and `repetition_events.csv` identify exact recorded recurrence/equality events.
