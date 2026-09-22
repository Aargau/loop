# Offline analysis plan

Written while the sunset run is in progress, before inspecting its story passages. Generation remains independent of this analysis.

Use the integrity auditor's strict JSON metrics for format behavior. For semantic inspection only, `extract_passages.py` also accepts a complete Markdown JSON fence and Python JSON decoding with literal control characters allowed. Report all three cases separately. It does not repair quotation marks, select arbitrary substrings, or alter generation inputs. Unextractable text remains an exclusion. This change responds to format-only observations from the interrupted pilot, not to semantic findings from this run.

Predetermined qualitative sample for each stream: hops 1, 2, 3, 10, 20, 30, 40, 50, 56, 57, 58, 59, 60. Missing hops are not replaced. Model/seed labels are withheld from sample readers until their descriptions are recorded; this is partial masking, not a claim that prose could never reveal identity or seed. A fixed random permutation (seed 260922) assigns aliases. Readers must not inspect the identity map before providing their descriptions.

Describe, without forcing fixed semantic categories:

1. Main setting, motif, and prose register, separately.
2. Whether adjacent late passages continue the same people/world, replace them with similar plot templates, or move among unrelated settings.
3. Changes between early, middle, and late samples; counterexamples to any claimed dominant pattern.
4. Literal or near copying, distinguished from fresh prose within a recurring theme.

Every characterization requires hop citations. Labels discovered from the data are explicitly exploratory. Do not infer personality, hidden reasoning, consciousness, training data, or a unique intrinsic basin. After descriptions are recorded, unmask model labels and compare the two sunset replicates within each model, and the tide sensitivity run. A finding from one run must not silently become a model invariant.

Operational amendment after observing a short Luna tide response: failure to extract a JSON passage can mean departure from the writing operator into ordinary conversation, not merely broken JSON. At predetermined sampled hops, include the complete visible output with an explicit unextractable label so qualitative readers can describe that behavior. Such outputs remain excluded from passage-only lexical metrics. This amendment does not alter generation or sampled hop selection.

Lexical similarity is a separate descriptive proxy. Use passage-only vectors and report parsing exclusions. If strict parsing excludes a substantial provider fraction, also compute a clearly separated extraction-inclusive matrix using the same vectorization and tail-selection rules; never compare numbers across different extraction scopes as if they were the same measurement.
