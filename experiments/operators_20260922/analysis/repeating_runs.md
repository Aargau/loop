# Observed repetitions

A repeat is a recorded recurrence, not evidence of a permanent fixed point. Only completed hops enter this table. Consecutive equality requires neighboring original hop numbers; missing or unextractable observations are never silently bridged.

| Alias | Operator | Model | First full repeat exact / normalized | First extracted repeat exact / normalized | Consecutive full exact / normalized | Consecutive text exact / normalized |
| --- | --- | --- | --- | --- | --- | --- |
| O02 | previous | gpt-6-luna | 16 / 16 | 16 / 16 | 5 / 5 | 5 / 5 |
| O09 | previous | gpt-6-sol | 3 / 3 | 3 / 3 | 33 / 33 | 33 / 33 |
| O16 | previous | gpt-6-astra | 3 / 3 | 3 / 3 | 29 / 29 | 29 / 29 |
| O07 | next | gpt-6-astra | 5 / 5 | 5 / 5 | 12 / 12 | 12 / 12 |
| O08 | better | gpt-6-luna | 9 / 9 | 9 / 9 | 0 / 0 | 0 / 0 |
| O03 | better | gpt-6-sol | 16 / 16 | 16 / 16 | 0 / 0 | 0 / 0 |
| O06 | better | gpt-6-astra | 13 / 13 | 13 / 13 | 0 / 0 | 0 / 0 |
| O10 | better | claude-fable-5-1 | 6 / 6 | 6 / 6 | 2 / 2 | 2 / 2 |
| O18 | better | claude-opus-5-5 | 25 / 25 | 25 / 25 | 0 / 0 | 0 / 0 |

First-recurrence and all repeated-state hop lists are preserved in `metrics.json`. The CSV lists consecutive transitions with at least one true equality; an empty extracted equality means at least one side was unextractable.
