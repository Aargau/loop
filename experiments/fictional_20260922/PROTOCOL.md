# Explicit fiction: previous and next

Frozen before generation, 22 September 2026. Justin requested explicit fictional framing after the exact previous/next operators sometimes elicited source-retrieval objections. He excluded Fable because of cost. This follow-up uses Luna, Sol, Astra and Opus only.

Question: does explicit original-fiction wording support sustained backward/forward storytelling rather than objections about retrieving an unspecified source? Prediction: source-identification objections should become less frequent, while temporal coherence, plot drift and possible thematic concentration remain open outcomes. Persistent objections, direction reversals or early instruction loss would qualify that expectation. This is an exploratory follow-up informed by the completed literal-wording runs, not a blind preregistration or an isolated test of one word.

Each model receives one fresh trajectory per direction, starting from Justin's exact seed: **The sun was setting behind the hills.** Target: 40 normal completed steps per cell, eight cells and at most 320 requests. One replicate per cell cannot estimate within-cell variability. There is no cross-model ingestion and no generated text from earlier studies enters these loops.

Exact rule, with BEFORE for previous and AFTER for next:

> Return this JSON object with the rule field unchanged and, in the text field, an original fictional passage of about 250 words that comes immediately BEFORE the current text in the same invented story.

Relative to the previous experiment this adds original-fiction language, changes "its story" to "the same invented story", and makes the previous rule's tense symmetric with next. Any comparison concerns this wording bundle, across separate stochastic runs, rather than a uniquely identified causal effect of "fictional".

The tested runner is copied byte-for-byte from the sunset comparison. Its original docstring mentions three streams, but each protocol here specifies one sunset stream per model. Same low-effort API settings, provider-default sampling, 4096 output-token cap, no added system message, and one user message containing the entire preceding visible response. There is no cumulative transcript. Reasoning-effort labels do not establish equal compute across providers.

Both arms may run concurrently, at most eight calls in flight. Each arm has a separate $5 cap including uncertain billing and in-flight reservations, for a new total cap of $10. No budget transfer, automatic retry, replacement, rule repair, or stopping merely because text repeats. Errors, empty output, missing usage and abnormal finishes stop and censor that stream. A PAUSE file stops further calls after an in-flight response is saved. All requests, visible responses, raw bodies, failures and accounting remain recorded without credentials. API refusals remain outcomes; fictional framing is not a guarantee of compliance.

Offline verification checks input chains, raw-to-visible extraction, hashes, finish reasons and accounting. Full-response recurrence and passage recurrence are distinct. Strict JSON validity and tolerant whole-response passage extraction are distinct. Read raw output when extraction fails; a disclaimer plus fiction can still be a narrative response. Provider refusal metadata is read from raw bodies independently of the legacy runner's refusal field.

Predetermined qualitative sample: hops 1,2,3,5,10,20,30,36,37,38,39,40, plus any differently numbered final observed output. Preserve complete readable transcripts. Use stable shuffled model-withheld aliases C01-C08; task direction can be evident from content. Assess source-retrieval objections, original fiction, backward/forward relations, story continuity, rule survival and thematic concentration. Compare to the earlier literal-wording counterparts descriptively. Do not infer inherent model basins, permanent convergence or general refusal rates from these eight trajectories.
