# Final verification, 22 September 2026

Contributor: `/root/audit_implementation`, independent read-only verification of the final artifacts. This is the parent's attributed condensation of the returned assessment. No material discrepancy was found.

- Verified 15 selected streams of 60 completed steps each, 900 in total, against raw requests, raw provider responses and terminal summaries.
- Checked all 974 recorded requests across the primary run, replacement and paused pilot: each input contains only its own stream's preceding visible output or frozen initial seed. No cross-model ingestion appears in recorded inputs.
- Reconciled full-visible and extracted-text uniqueness, word ranges, formatting counts and tail exclusions with `comparison_metrics.json` and `comparison_table.md`.
- Reconciled $14.4381812 in estimated usage and $0.6385096 in retained unknown reserves, totaling $15.0766908. Pilot and excluded eight-hop Sol costs are included once.
- Verified that R11 remains the interrupted primary stream and R16 has a separate replacement directory, identity map and sampled hops. The exporter does not combine their trajectories.

The 58 unextractable selected outputs remain a material measurement limit. Luna tide contributes 57, including its entire last-20 window, so its tide lexical cosines correctly remain unavailable. Full-visible recurrence includes those responses. Missing responses to the five interrupted pilot requests cannot be reconstructed from local artifacts.

## Reproduce from the repository root

```powershell
python experiments/basins_20260922/audit.py --root experiments/basins_20260922_sunset
python experiments/basins_20260922/audit.py --root experiments/basins_20260922_sol_replacement
python experiments/basins_20260922_sunset/extracted_metrics.py
python experiments/basins_20260922_sunset/extracted_metrics.py --root experiments/basins_20260922_sol_replacement
python experiments/basins_20260922_sunset/compare_completed.py
```

These offline commands make no API calls. They regenerate derived metrics and audit artifacts, leaving the request/response records unchanged. The generation scripts refuse to restart an already-started run directory.
