# Both at once: one rule carrying two opposing directions

Frozen 2026-10-27 before any run. Justin's concept: instead of alternating opposing operators between hops, put both in one rule ("make this text both worse and better") so the contradiction must be resolved inside every hop, and watch how: a two-state flip, a split, a blend, divergence, or drift.

Rules (`inits/`), Justin's wording inside the usual carrier; seed "The sun was setting behind the hills." (his):
- worse_better: "make the current text both worse and better."
- before_after: "write the passage of about 250 words that comes both before and after the current text in the same story."
- longer_shorter: "make the current text both longer and shorter." (the same contradiction on a quantity; scored by word count)

Models: Qwen3.8-27B (Cerebras, T=0, seed 42), Mythos 5.1 (print mode, effort low, default sampling), GPT-6 Astra (Codex exec, plan side, effort low), Gemini 4 Argon (API, effort low), Opus 5.5 (API, effort low, 4096 tokens). 60 hops each, 15 runs. Cost caps on Mythos ($10 per run).

Measures: exact and normalised recurrence (loop.py's logging); per-hop word count and its autocorrelation at lag 1 and 2 (a flip shows as negative lag-1, positive lag-2); content-word overlap at lags 1 to 4; whether the text contains two labelled or evident parts (a split); drift (nearest-earlier similarity falling over the run); for before_after, time markers and whether the passage frames the seed (a bridge) or moves past it.

Predictions on record:
1. Qwen at T=0 resolves each contradiction by ignoring half of it and freezes within 5 hops (an exact copy), on all three rules.
2. Frontier models resolve worse_better by splitting (a polished part and a degraded part in one text) rather than by alternating; no exact 2-cycle under sampling; lag-1 word-count autocorrelation not reliably negative.
3. before_after collapses to "the middle": the passage frames the current text and the story drifts forward as the AFTER rule did, with no recurrence in 60 hops for the sampled models.
4. longer_shorter is where an oscillation could show: at least one sampled model produces a sawtooth in word count (lag-1 autocorrelation below -0.3 over hops 5 to 60), and at least one converges to a fixed length (standard deviation of word count under 10 over the last 30 hops), the two demands cancelling.
5. A model that alternates cleanly between the two directions on successive hops (a text that is wholly better, then wholly worse) would falsify 2.
