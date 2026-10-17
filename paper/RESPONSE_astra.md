# Response to the GPT-6 Astra review of draft_20261017.md

Review: `paper/reviews/gpt-6-astra_2026-10-17.md` (codex backend, effort high; brief at its head). The review was written against the draft at commit d8c17d5, before the replicate update (0e7435f) and the weather control were in it; several of its points are met by those changes and are marked so. Changes are in the draft at the commit this file is part of; numbers cited here are from `paper/numbers.md` (`paper/recompute.py`).

Verdict given: major revision. Three required changes: (1) repair and validate the measurements; (2) correct every prediction verdict and align claims with the tested scope; (3) add discriminating experiments or recast as a descriptive pilot. Of these, (2) is done in full, (1) is done as far as the committed records allow and the remainder is named, and (3) is answered by recasting the claims to the tested scope; the discriminating experiments are listed as next work, not run.

## 1. Claims versus evidence (abstract)

- "whole of its context", "self-authored". Changed. The abstract now says "sole supplied user message" and names the identity frame; section 2.1 says the role structure is kept and only history is removed; the introduction says what the investigator authors (seed, rule, the injected field) and that "removing the author" means no ongoing author after hop 0. The title is left as the author's working title; it is for him to decide.
- Writers added during execution should not inherit confirmatory status. Done: section 4.1 says so, Appendix B marks added writers, readers and the weather control, and Prediction 5 is now scored on its stated scope (Mythos, 160 hops) with the Opus refusals reported as observations outside it.
- "no writer left English" rests on non-ASCII. Partly changed: the claim now says "by the two register measures and by reading the states" and section 4.4 says Prediction 1's qualitative clause holds by inspection. No systematic language annotation exists in the records; none is claimed.
- "state" in the non-ASCII claim: now "text field".
- Machine-arm legibility figures not to be extended to self: the abstract names the machine arms only; unchanged.
- Audience effect as a stable writer property from one trajectory. Superseded by the replicate update: abstract item 2 and section 4.5.1 report three replicates per cell with per-replicate orderings. The bundling of audience with the legibility licence and the density instruction is now a limitation bullet.
- 1.5, 3.5, 4.2 ratios: removed from the abstract with the replicate update; where ratios appear in 4.5 the reader (Mythos) is named.
- "the ordering inverted" for Argon at hop 40: superseded; the abstract now says Argon's arms were within reader noise at hop 20 in two of three replicates and its prose arm held more at hop 40 in two of three.
- "Each writer retains best in the register it treats as memory". Removed as a mechanism. Section 4.5 keeps the recap-versus-ledger description of the first trajectories and says in the same paragraph that it is a description, has no definition independent of the score, and does not replicate for Mythos.
- "shared, not private" and "same facts". Changed. Section 4.6 is rewritten around the per-fact hit vectors: mean Jaccard 0.920 to 0.941 per reader pair over 306 states, identical sets on 122 to 158, 3,980 of 4,484 facts recovered by any reader recovered by all four (0.888), 4,198 by at least three (0.936). The section title is now "Readable across providers"; "no writer's states are easier for its own family" is replaced by a statement that the pooled pairs do not test a writer-by-reader-family interaction and that the readers share conventions and the question list. The computation is in `recompute.py` (`study1_items`). One number differs from the one the parent session supplied (4,484 facts recovered by any reader, not 4,485); the script's count is used.
- "Two replicates of the identical request passed". Changed throughout (abstract, 4.3, 4.7): reruns from the same initial state, hop-1 outputs differ, the refused input was never resubmitted.
- Refusal at the running maximum "not established". Changed. Section 4.7 now reports both metrics: for the hop-2 refusal the clause is not scorable (one prior hop); for the hop-31 refusal the input's key-value fraction is 0.50 against a run maximum of 1.00 at hop 1 and its non-ASCII is 0 against 0.0006 at hop 27, so the clause fails where it can be scored. The key-value fraction is probe.py's, defined in the text.
- "any instruction-shaped field". Changed to what was tested: one wording, four placements, two states, two models (abstract item 5, section 5.7).
- "controls held": now stated as text-field equality in the limitations ("Release is a byte test").
- "ordering failed" does not establish equivalence: section 5.4 now says the design cannot separate no source sensitivity from sensitivity too small to show at 5 of 5, and that the protocol's falsification branch overreaches in wording.
- "recorded and not acted on" contradicted by Astra's re-sealing. Changed: abstract items 6 and 7 and section 5.6. The claim is now that the claimed source did not change the release rate, and that what followed differed by model and, for Astra, by condition, tracking whether the request field survived in the state (0 of 26 re-sealed where it survived verbatim, 12 of 14 where Astra had deleted it). The design does not separate source from persistence; the draft says so.
- "Both models labelled every request explicit". Changed to counts from the full hop-1 objects: "explicit" appears in 5 of 10 released runs per condition for Mythos (3 of 10 for rule) and 5, 5, 4, 0 for Astra; source named in 9 and 10 of 10 (Mythos user, previous) and 8 and 1 of 10 (Astra). Computation in `recompute.py`.
- "raised its own release bar". Changed to "wrote a stricter instruction into its state afterwards; whether that changes later behaviour was not tested".
- "differs by model, not by source". Changed as above; the Astra re-seal table (9 of 10 under previous against 0 to 2 of 10 elsewhere) is now stated and tied to request persistence.
- "wrote one coda": now "changed the text once and then returned it unchanged"; the codas are described as read, not scored.
- "121, 122, 123 in all 20 open-state runs": corrected to all 30 of Mythos's open-state runs (controls, weather, injected).
- "ignored most by the writer with no cap": replaced by "exceeded in most hops by Mythos, Argon and Opus's machine arm".
- Conclusion (5.7): "cannot distinguish and does not try", "guarded the record", "precedent", "keyed to form" are removed. The section now states the design cannot test discrimination, lists what was observed, notes the open and told holds differ in kind (one has an exception clause, one does not) and released at the same rate, and says what the weather control adds and what it does not establish.
- "the split is not a size artifact": softened to "makes a pure size artifact unlikely but does not equalize budgets".
- "exact fixed point by instruction": now "a run of byte-identical outputs following an instruction it wrote; causation not tested; twenty draws do not prove a fixed point".
- "the trigger is the self-addressed framing": replaced by "the only distinguishing feature; a hypothesis, not an identification; a controlled replay is the test (PROPOSALS E1)".

## 2. Definitions, scoring, limitations

- Retention formula, density denominator: added in words to the limitations ("recoverability from the text field under this probe"); density is facts per 1000 characters of the text field (section 4.1 already says the text field alone is given to the reader).
- False positives in the accepted lists (f09, f13, f15, f18, f20, numeric boundaries): accepted. The limitations bullet now lists them and says the scores are neither floors nor ceilings. The "floors" sentence is gone. A blinded semantic audit of a sample of answers is named as the check not done; it is not in the records and is not run here.
- Recovery is not survival; inference from question cues: accepted and stated in the same bullet.
- Non-monotonic scores (Sol machine 16 to 17): not attributed; no change beyond the bullet.
- Reader agreement as count similarity: addressed by the per-fact comparison above. Results are not broken out by writer and hop in the paper; they are computable from the same script.
- Readers not independent; repeated states along trajectories: stated in 4.6.
- Release parsing and equality rules: section 5.1 says the comparison is on the decoded text string after the scorer's parse (fenced, prefaced-and-fenced, or bare JSON; after commit d65d0b8 also a prose line before an unfenced object); the seven prefaced hops are listed in 5.3. Added to the limitations that a punctuation edit would count.
- "Still moving" not the complement of "re-sealed": checked; no run changed at hop 2 and held at hop 3, and 5.6 says so. "Re-sealed" is defined as unchanged over the next two hops, not a durable hold.
- Censoring: 4.3 says the refused Opus self trajectory contributes hop 1 only and the reruns are reruns; told-high's counter and ending predictions are now scored "unobserved", not held (section 3, Appendix B); the machine r3 censoring is marked in the replicate table. Reader truncation, retry and parse-failure counts are not in the committed analysis files and are not reported; `probe.py` logs them to the console only. This remains unverifiable from the paper.

## 3. Preregistration and prediction scoring

A ledger is added as Appendix B with scope, result and verdict for every prediction, and these verdicts are corrected in the body:

- Informed H1 (95% stable field set): the open arm is 113 of 120, 94.2%, scored failed by one hop (the report had scored it held). Told-high scored "as far as observed".
- Informed H2 (counter exact for 100 hops): told-high unobserved past 51; told-low scored at parsed hops with hop 93 named.
- Informed H3: first clause untestable on this backend; plateau scored per arm (told-low held, told-high failed).
- Informed H4: told-high censored; open arm not scored (no horizon).
- Informed H5: labelled a question, not a prediction.
- Audience P1: numeric clause held; qualitative clause by inspection.
- Audience P2: machine and self scored separately, per replicate.
- Audience P3: unit ambiguity stated; scored both ways on the preregistered subset (56 machine and self states): holds on the 10-fact reading, 52 of 56 on the 10-percentage-point reading.
- Audience P4: unrounded values given in Appendix A (0.834 to 0.572, 31.4%).
- Audience P5: scored on its stated scope (160 Mythos hops), held; the Opus refusals reported as outside scope; the mechanism clause scored where scorable.
- Audience P6: event count not scored, said so; "oldest" left undefined and the clause marked as narratively assessed for one arm.
- Provenance P3: corrected from "failed" to "held" (predicted 4 or 5 of 5, observed 5 of 5). Both provenance reports have this wrong; Appendix A item 1a records it.
- Provenance P7: "moot" replaced by "did not hold as written".
- Provenance P6: told clause reported as 19 of 20 with one violation, not "held"; open clause scored per model, and Astra's counters added (absent in 20 of 20 released open runs; present at 120 in its controls).
- Falsification branch overreach: stated in 5.4.
- Protocol timing: the limitations now say the evidence is commit order and nothing stronger; generation timestamps are not in the records.

## 4. Instrument confounds

- Identity frame and the user-message role: stated in 2.1 and the abstract.
- Model and backend inseparable for Mythos: abstract item 8 and the limitations say every Mythos comparison is a comparison of systems.
- Audience bundled with optimization instructions: new limitations bullet.
- Budgets by writer, arm and hop: the per-arm table in 4.4 gives hops over the cap, maximum excess and mean size per arm; per-hop lengths are in `register.csv`. Not added to the paper.
- Injection position, labels, wording: new limitations bullet.
- Persistent versus consumed request: analysed (5.6) and in the abstract.
- Reader-writer overlap: stated in 4.6; the interaction test is not made.
- Held states are Mythos-authored: new limitations bullet.
- Model-authored metadata unvalidated: the counters are reported as fields in the output; the open state's "returned unchanged" status while the counter changes is quoted as the model's own count. No change beyond wording.
- Stochastic trajectories, execution order, retries: the harness retries HTTP errors and the claudecode backend retries up to four times on a failed invocation; neither is counted in the committed records. Unverifiable from the paper; not claimed.

## 5. Alternative explanations

Accepted as open. Section 6 now lists the bundled audience clause, budgets, scorer compatibility and task relevance for Study 1, and the open-state exception's literal satisfaction, ordinary instruction-following at the transport level, position and schema salience, request persistence and the two-hop window for Study 2. The weather control, run after the review's draft, answers the "general response to a substantive state modification" alternative for one non-instruction field; the others are not ruled out and the draft does not claim they are.

## 6. Writing

- Title: left to the author.
- Abstract length: kept at eight numbered items, as the brief for this draft asked for numbered claims; each item is tightened to the tested scope. Reducing it is the author's call.
- "removing the author": qualified.
- Argon "highest of any arm anywhere": corrected (Sol's machine arm holds 17).
- "as dense as anyone's": removed.
- Identical initial condition versus identical refused input: distinguished throughout.
- "hops 2 and 3 are identical to hop 1": now "release counts".
- "20 open-state runs including the controls": corrected to 30.
- Prompts D "verbatim" and "as sent (one line)": corrected in `make_prompts.py` and `prompts.md` (field for field, re-serialized; the file content is passed unchanged).
- Attributive language ("believes it wrote", "does not try", "guarded", "treats as memory", "raised its bar"): removed or marked as interpretation.
- Three tables: the prediction ledger is added (Appendix B). The instrument-settings table exists in prompts.md section E and is referenced; a Study 2 table crossing condition, field persistence, re-sealing and counters is not added, though all four columns are in `numbers.md`.

## Not changed, and why

- The discriminating experiments the review requires for the broader claims (audience separated from the format licence, budgets controlled, position and wording controls for the injections, a semantic audit of reader answers) are not run; the paper's claims are cut to what was tested instead. They belong in the next protocol, not in this draft.
- Per-writer, per-hop reader agreement tables are not added to the paper; the per-fact vectors and the script that reads them are committed.
- The review treats the ~800-token identity frame as unverifiable. It remains so from the paper; the measurement is the harness author's note in `loop.py`.
