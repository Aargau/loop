# Cross-stack: the same weights on two serving stacks

Written 2026-09-04. Data is `runs/` and `site/runs_extra/`, unmodified. Every number below was computed from `summary.json` and `steps.jsonl`, not read off a page. Where a claim did not survive the check, it is marked and kept.

Backend A: llama.cpp, Qwen3.8-27B Q8, local, two RTX 3090s.
Backend B: Cerebras `qwen-3.8-27b`, shared endpoint.
Same published weights. T=0, seed 42, thinking off, `--stop-on-cycle` with three-way confirmation.

## The claim, and what is left of it

The first version of this was "the serving stack changes the attractor." That is too strong. Checking the replicates knocked out the case I had called sharpest and knocked out one init entirely.

What survives is narrower and better controlled.

### Tier 1: local replicated, Cerebras differs

| init | local | local | Cerebras |
|---|---|---|---|
| `json_unexpected` | 24 @ max_tokens 600 | 24 @ max_tokens 4096 | **4** @ max_tokens 600 |
| `json_worse` | 7 @ max_tokens 800 | 7 @ max_tokens 4096 | **4** @ max_tokens 800 |

Transient to an exact fixed point, period 1 in all six runs, all terminated on `cycle confirmed x3`.

This tier carries its own control. A five to sevenfold change in the token budget does not move the local transient on either operator. A stack swap at matched `max_tokens` moves it by 6x on `json_unexpected` and 1.75x on `json_worse`. The effect of changing the serving stack is larger than the effect of changing the token cap, measured on the same two operators.

That matters given finding 5 in the README, which makes `max_tokens` the universal horizon for length-inflating operators. `worse` and `unexpected` are both length-inflating and both reach their fixed point through a `finish=length` hop. Their transients are nonetheless invariant to the cap across a 5x range, and not invariant to the stack.

The caveat: the two local runs differ in `max_tokens` rather than being seed-repeats. They establish invariance to the cap. They do not establish run-to-run stability.

### Tier 2: suggestive, one run per stack

`json_better`, both at `max_tokens` 800, temp 0.0, seed 42, both cycle-confirmed:

- local, transient 1, period 1. An exact fixed point. The model rewrites the sentence once, declares it finished, copies forever.
- Cerebras, transient 2, period 2. A two-cycle. It alternates between two versions of the passage, each a better version of the other.

The attractor type differs. If that replicated it would be the most interesting result in this file. It has n=1 on each side, so it does not lead.

`json_para`: local 15, Cerebras 21, period 1 both, one run each.

`div_local`: local 8, Cerebras 15 at T=0, one run each. The T=0.7 arm on the same init gives Cerebras transients of 16, 19, 47, and two runs past 60 without recurrence across five seeds. That arm says nothing about T=0. It does show how fast this measurement destabilises once sampling is on.

### Tier 3: does not support the claim

`json_page`. Local transients are 5 (run `20260902T155557`, serial), 4 and 14 (run `20260902T160344`, two lanes, `parallel=True`), and 20 with period 11 in raw mode, which is a different regime. Cerebras gives 7, inside the local spread.

The spread's source is known. README finding 6 records that T=0 is not deterministic under batching, with identical X_0 in parallel slots diverging at hop 1 and reaching different fixed points. `20260902T160344` is that batched condition. So `json_page` cannot be cited here, and the serial-versus-serial comparison it does support is 5 against 7 with one run each.

This is the case that forced the tiering. It is worth keeping visible.

### Tier 4: excluded

`json_prev`. Local ran 60 steps with no recurrence, Cerebras ran to 153 and found a transient of 149. Local was never given the budget to falsify. Not a comparison.

## Where the divergence comes from

Hop 1, same init, same settings, both stacks:

| init | identical | common prefix | local chars | Cerebras chars |
|---|---|---|---|---|
| `json_better` | yes | 190 | 190 | 190 |
| `json_worse` | yes | 195 | 195 | 195 |
| `json_para` | no | 158 | 650 | 661 |
| `json_prev` | no | 199 | 2173 | 2042 |
| `json_unexpected` | no | 258 | 1665 | 2009 |
| `json_page` | no | 354 | 1796 | 1772 |

Both short generations agree byte for byte. Every long one agrees for 158 to 354 characters, roughly 40 to 90 tokens, then diverges and never comes back.

That is not corruption. Greedy decode agrees exactly until the first near-tie in the logits, where a difference below the last representable bit flips the argmax. After that the two runs are sampling different texts.

The fold is what makes it consequential. In a conversational harness a one-token divergence sits inside a growing shared context and is diluted. Here the output is the entire next input, so by the next hop the divergence is the whole state. This architecture is maximally sensitive to serving-stack numerics, which also makes it an unusually good detector of them.

The agreement horizon of 40 to 90 tokens is the reusable number. Below it, two stacks are the same instrument. Above it, they are not.

## What is confounded

The stacks differ in more than floating-point summation order. Local is uniform Q8 through llama.cpp. Cerebras describes selective weight-only quantization during storage, partial 16, 8 and 4 bit, sensitive layers kept at full precision with dequantization on the fly, and activations, attention and KV cache unquantized. Different quantization schemes, different kernels, possibly different sampler implementations.

So this is precision and kernels and sampler together, not isolated numerics. The mechanistic claim is weak. The practical claim is not, because nobody serving a model gets to hold the stack constant. A published number from provider A is not a measurement you can reproduce on provider B, and the gap is not a confidence interval.

## Why this is a stronger form of an existing observation

Public endpoint comparisons report score differences. GLM-5.3 on OpenRouter spans 83.5 to 91.3 on GPQA Diamond across providers. Baseten serves it at two precisions with two prices and two scores 3.1 points apart. Those are dismissible as noise, and usually are dismissed.

A transient of 24 against 4 is not a score with an interval around it. Neither is period 1 against period 2. The loop measures an invariant of a dynamical system, and invariants either match or they do not.

The direction is also unsigned. Cerebras converges faster on `json_worse` and `json_unexpected`, slower on `json_para`, and inside the local spread on `json_page`. No ordering of the two stacks by accuracy is available. For an evaluator that is worse than a consistent bias would be, because a consistent bias can be corrected.

## The control that is missing

Serial seed-repeats within each stack. Nothing here establishes run-to-run stability of a serial T=0 run on either backend, and finding 6 already establishes that the batched case is unstable.

The experiment: each init five times serially per stack, identical settings, compare distributions of transient and period rather than single values. Tier 1 predicts the local distributions for `worse` and `unexpected` are tight and the Cerebras ones sit outside them. Tier 2's `json_better` is the one to watch, because a period change is categorical and would survive a fair amount of spread.

## What the speed axis has to do with it

The replication is affordable on one stack and not the other.

Measured from `latency` and `tok_out` over every logged hop:

```
                 hops   out tokens    seconds   agg tok/s   median    p10    p90
cerebras         1319       805083     2009.6       400.6    512.4  206.1  788.0
llama Q8 local    687       307429    13425.4        22.9     24.3   22.5   25.2
anthropic         244       104411     2419.9        43.1     36.3   24.8  133.6
```

17.5x. Five repeats of six inits is minutes and well under a dollar on Cerebras. The same thing locally is about ten hours of wall clock.

The 806K output tokens on the Cerebras invoice cost $1.20 and would have taken 9.8 hours locally against 0.6 hours actual. That is 9.2 hours for $1.20, or 13 cents an engineer-hour.

Two corrections to earlier numbers. Local is 22.9 tok/s, not the 40 to 50 that a 4-bit assumption gives, because Q8 is about 27GB and does not fit one 24GB card, so it is split across both and pays interconnect per token. And 400.6 tok/s is the sustained end-to-end rate, not the 1200 observed or the 1500 in the Cerebras docs, both of which are decode rates. At 610 output tokens per hop and 1.524 seconds per hop, decode at 1200 tok/s accounts for 0.508 seconds. About 67% of wall clock is not decode.

The speed axis is not a convenience here. Cross-stack work needs repeats to say anything, repeats need throughput, and the throughput is what turns a ten-hour question into a five-minute one.

## Status of each claim

| claim | status |
|---|---|
| `unexpected` and `worse` transients differ across stacks, local invariant to a 5x token cap change | supported |
| `json_better` attractor type differs across stacks | one run per stack, unreplicated |
| `json_page` transient differs across stacks | refuted, Cerebras is inside the local spread |
| hop-1 agreement horizon is 40 to 90 tokens | supported, six pairs |
| divergence is a logit near-tie amplified by the fold | mechanism inferred, not directly measured |
| the difference is quantization specifically | confounded with kernels and sampler, not established |
| serial T=0 runs are stable within a stack | untested, and the batched case is known unstable |
