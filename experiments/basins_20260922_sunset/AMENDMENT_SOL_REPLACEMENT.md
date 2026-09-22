# Protocol amendment: one fresh Sol replacement

Written at 2026-09-22T20:42:29.031423+00:00, before any replacement generation. The decision was announced in the live task after the connection failure; this timestamp records the written amendment, not a reconstructed decision time.

The original `gpt-6-sol/sunset_b` stream saved eight complete responses. Its ninth request failed with `URLError` / Windows error 10054, a remote connection reset, with no response body saved. The run obeyed its no-automatic-retry policy and stopped that stream. All original requests, responses, error receipt, and the $0.04533 uncertain-billing reservation remain unchanged.

Amendment: after the primary run has finalized its cost accounting, permit exactly one additional, fresh Sol sunset trajectory of up to 60 hops. It begins from `The sun was setting behind the hills.` with the original rule and identical model, effort, sampling and token limit. It does not retry the failed request, resume from hop 8, inherit any prior generated text, or replace files. The sole selection reason is the recorded transport failure, not any qualitative or lexical property of the eight passages. No other content-selected trajectories are replaced.

The new stream is `sunset_replacement` in `../basins_20260922_sol_replacement/`. Allocate at most $3 from the original $20 total only after subtracting all primary/pilot reported usage and retained unknown-billing reserves. If it fails, preserve that outcome and do not automatically launch another replacement.

The intended equal-depth comparison comprises 14 complete primary streams and the fresh Sol replacement. Exclude the original eight-hop stream from that comparison while retaining it in attempts, costs and all-run evidence. This is an infrastructure-conditioned completed-stream comparison, not an unchanged original sample of exactly 15 attempts.

Qualitative identity: R11 always denotes the original interrupted Sol stream. Its frozen early coding remains attached only to that stream. Assign the fresh replacement R16 and separately inspect its own hops 1,2,3,10,20,30,40,50,56,57,58,59,60. Never attach R11's early observations to R16's later ones. Record whether identity is withheld from each reader.
