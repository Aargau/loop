# Completed-stream comparison

Fifteen selected streams completed 60 hops each: two sunset trajectories and one tide trajectory per model.

Excluded primary `gpt-6-sol/sunset_b`: 8 completed hops; status `transport_or_parse_error`. Fresh `replacement/gpt-6-sol/sunset_replacement` supplies the second Sol sunset replicate. The partial remains in raw evidence and all-run costs. The paused pilot is excluded from comparisons but retained in costs.

Operational completion is not a quality score. Uniqueness is pooled across each model's selected streams. The uniqueness columns show exact / case-and-whitespace-normalized unique counts, followed by the population size. Word ranges cover explicitly extracted text, including any empty or changed-rule text.

| Model | 60-hop streams: primary + replacement | Selected hops | Extracted word range | Full visible unique (exact / normalized; n) | Extracted text unique (exact / normalized; n) | Selected usage $ | All-run usage $ | Unknown reserve $ |
| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: |
| gpt-6-luna | 3/3 + none | 180 | 251–310 | 177 / 177; 180 | 122 / 122; 123 | 0.033608 | 0.038721 | 0.002262 |
| gpt-6-sol | 2/3 + 1/1 | 180 | 240–286 | 180 / 180; 180 | 180 / 180; 180 | 0.871846 | 0.987080 | 0.090526 |
| gpt-6-astra | 3/3 + none | 180 | 246–281 | 180 / 180; 180 | 180 / 180; 180 | 4.579060 | 4.711520 | 0.228380 |
| claude-fable-5-1 | 3/3 + none | 180 | 248–333 | 180 / 180; 180 | 179 / 179; 179 | 5.686070 | 5.899340 | 0.227010 |
| claude-opus-5-5 | 3/3 + none | 180 | 240–279 | 180 / 180; 180 | 180 / 180; 180 | 2.662460 | 2.801520 | 0.090332 |

All-run usage estimate **$14.438181** + retained unknown reserves **$0.638510** = **$15.076691**, within the **$20.00** study budget. Selected-stream usage is **$13.833044**. These are conservative estimates, not provider invoices.

The following cosines use one global passage-only TF-IDF fit. Tails are completed hops 41–60, followed by explicit extraction/rule/empty-text exclusions without backfilling. Missing vectors yield `null`. Values describe lexical overlap; they are not semantic basin labels or significance tests.

| Model | Sunset replicates | Sunset A to tide | Sunset B or replacement to tide |
| --- | ---: | ---: | ---: |
| gpt-6-luna | 0.3160 | null | null |
| gpt-6-sol | 0.2140 | 0.1974 | 0.3763 |
| gpt-6-astra | 0.5995 | 0.5216 | 0.5590 |
| claude-fable-5-1 | 0.4091 | 0.4542 | 0.5147 |
| claude-opus-5-5 | 0.3729 | 0.2782 | 0.2635 |

Full stream exclusions and formatting counts are recorded in `comparison_metrics.json`; the complete centroid matrix is in `comparison_lexical_similarity.csv`.
