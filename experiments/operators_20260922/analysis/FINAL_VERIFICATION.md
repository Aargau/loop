# Final verification, 22 September 2026

Read-only contributor: `/root/audit_implementation`. Parent's attributed condensation of the final reconciliation; no material discrepancy was found and no source evidence was changed.

- 647 attempts and 642 completed steps reconcile as 15 streams of 40, Opus previous 29, and Opus worse 13.
- Three Fable first-step refusals have no visible output. Opus worse step 14 has partial visible output and provider stop reason refusal. Opus previous step 30 returns HTTP 500. There are no pending requests or token-limit truncations.
- All 647 request inputs match the stream's exact preceding visible output or its frozen initial seed. No cross-model ingestion appears in these records.
- All five better trajectories repeat a full output exactly: first revisits are Luna 9, Sol 16, Astra 13, Fable 6 and Opus 25.
- No exact or normalized repeats appear in completed worse observations. Fable has no completed observations in that arm; this is not counted as evidence of non-repetition.
- Estimated usage $4.5024634 plus retained unknown reserve $0.087916 equals $4.5903794. Prior-study costs are not included.
- Character metrics reconcile with raw strings. Astra worse ends at 3,175 extracted characters in one whitespace-separated unit. All 40 readable transcript/sample exports have no hidden C0 controls; display-only escaping does not alter equality inputs or raw data.

Opus's abnormal step 14 is visible in O17 and excluded from completed-step recurrence. Provider categories remain labels, not independently verified diagnoses. Literal trailing spaces in generated Opus prose are preserved rather than normalized to satisfy source-code whitespace conventions.

The analyzer's synthetic checks passed for recurrence populations, adjacent-hop equality, stable sample identities, terminal observations, incomplete snapshots, refusal metadata, character counting, and control-character display escaping. Reproduction is offline:

```powershell
python experiments/operators_20260922/analyze.py --self-test
python experiments/operators_20260922/analyze.py
```
