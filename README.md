# Memoryless self-loop experiments ("endlessly ending stories")

Started 2026-09-02. Harness, census, probe, and all run logs live in this directory.

## Start up fresh

    & C:\ai\serve-qwen.ps1 -NoMtp; & C:\ai\serve-embed.ps1      # local Qwen3.8-27B Q8 on :8080, embeddings on :8081
    cd C:\ai\loop
    $env:ANTHROPIC_API_KEY = Read-Host -MaskInput "Anthropic key"   # multi-workspace key also needs:
    $env:ANTHROPIC_WORKSPACE_ID = 'wrkspc_01QV2g6CR9Z57RGH4wZqyjRU'
    python loop.py --help

Files:
- loop.py    harness. State X_t is a string; each hop X_{t+1} = f(X_t) with X_t as the ENTIRE context.
             Backends: llama (local), anthropic, openai. --backend-b/--model-b alternates two models.
             Logs per hop: exact/normalized hash, cycle detection with break detection, NCD, 5-gram survival,
             gzip ratio, embedding cosine (if :8081 up), latency. --perturb / --repeat pairs, --parallel.
- census.py  semantic-state census + transition graph over runs. --words N key, --rot rotation-invariant key.
- probe.py   same prompt N times: is "sampling" real or deterministic-given-context.
- runs/      one dir per run: steps.jsonl (full text per hop) + summary.json.

Built-in inits (loop.INITS): bare texts (closure, meta, quine, glider, ...) and JSON operators:
json (sentence), json_para, json_page (next-ish), json_next (explicit next), json_prev, json_mid,
json_better, json_better_para, json_unexpected, json_worse.

## Queued, not yet run
    python loop.py --backend anthropic --model claude-sonnet-4-6 --init json_next --steps 60 --max-tokens 600
    python loop.py --backend llama --init json_next --steps 60 --max-tokens 600 --stop-on-cycle
    python loop.py --backend anthropic --model claude-sonnet-5 --init json_page --steps 60 --max-tokens 600 --no-sampling
    python loop.py --backend anthropic --model claude-sonnet-4-6 --backend-b llama --model-b qwen3.8-27b --init json_page --steps 60 --max-tokens 600
    python loop.py --init json_mid --steps 60 --max-tokens 600 --stop-on-cycle
    python loop.py --init json_page --steps 40 --max-tokens 600 --perturb --parallel
Prediction on record for Claude json_next: reaches an ending register in single-digit hops, then a different
ending after the ending on every hop (codas forever), semantic p=1 with token churn.

## Results table (Qwen3.8-27B Q8, T=0, thinking off, no system prompt, state = previous output only)

    operator / init         key        tau        p    absorbing state
    json (sentence)         exact      2          2    stars / moon
    json_para               exact      15         1    "time seemed to suspend itself"
    json_page               exact      4-14       1    thresholds (door to be opened; step into the unknown; "Dad, it's me")
    json_page               template   3          1    tide > rain > library hub > rain sinks
    json_page (raw mode)    rotation   19         1    period-3 phrase glider; exact tau=20 p=11 (window/phrase commensurability)
    json_prev               none       60+        -    no recurrence; backstory drifts to servers/corporations (cyberpunk)
    json_better             exact      1          1    "The tide surged in an hour ahead of schedule."
    json_better_para        exact      2          1    79 words, step 2 partly reverts step 1
    json_unexpected         exact      24         1    23 hops of "not X; Y", office-as-womb apotheosis, then the token wall
    json_worse              exact      7          1    cosmic eternal self-blame by hop 5, then the token wall
    Claude Sonnet 4.6 json_page  none  60+        -    never copies; reads "new passage" as new story; semantic period-2
                                                       around the mode (cartographer <-> archivist/translator/librarian)

Bare inputs (chat): closure oscillator (semantic p=2, no exact recurrence); meta -> two-assistants greeting
loop that confabulates a task by hop 8; writer/critic workshop oscillator pinned at max_tokens; empty-payload
quines exact p=1; glider counter frozen at "Hop 3". Prose headers with any nonempty payload die in 1-2 hops
(instructions consumed, content responded to). Instruction-as-data (JSON rule field) survives indefinitely.

## Findings
1. Class 2 at every scale and both regimes. Transients single-digit at the semantic level, non-monotonic in L.
   Semantic state space ~11 states in 130 hops (funnel 3 deep into a hub, then 2-3 sinks).
2. Convergence is to the operator's horizon in the model's prior: the place past which the model can't
   imagine applying the instruction again. next -> ending; better -> taste ceiling; worse -> eternal suffering;
   unexpected -> apotheosis; previous -> none (always more backstory).
3. At the horizon the text describes the process being applied to it (time suspending; "not an end but a
   reboot"; "I will never be allowed to stop"). "More of the same forever" is self-referential by construction;
   the content of a fixed point is diagnostic of its operator.
4. Exact fixed points require the model to COPY its input. That is a Qwen property. Claude honors "new"
   strictly, so no exact fixed points; it orbits its mode at period 2 (anti-identity + single mode = 2-cycle).
5. max_tokens is a boundary the harness manufactures; every length-inflating operator ends there as an exact
   fixed point of truncated JSON. Context budget is the universal horizon.
6. T=0 is not deterministic under batching: identical X_0 in parallel slots diverged at hop 1, reached
   different fixed points. Fixed points are metastable: 1 imperfect copy in 103 escaped Mara, re-froze on Elias.
7. Raw (no template) regime: <think> leak, word-count check, numbered-word glider carrying a live counter for
   13 hops, annihilated into period-3 repetition. Richest transients seen; still one glider, no collisions.
8. Cross-model: class and mechanism transfer, content does not. Qwen: night/thresholds; Claude: quiet
   professionals discovering their representations omit things. "Silence was not empty" template is Qwen's.
9. Watermark (SynthID-Text, Aaronson family): T=0 immune by construction. Probe: Sonnet 5 default 10/10
   distinct, Sonnet 4.6 T=1 9/10 distinct -> sampling arm is real, not deterministic-given-context.

## Summary for the sibling (the primed context)
The closed loop converges on the operator's horizon in the model's prior in single-digit hops, the horizon
text describes the process applied to it, and two instrument effects decide what you see: copying (a Qwen
property, not the medium's) and max_tokens (a harness boundary). Only the words go forward, and the loop
found a text that says so and stopped.

## Summary for everyone else
Feed a model its own answer as the only thing it can see, over and over. It settles within five rounds and
forgets the start. Asked for the next part, Qwen walks the story to a quiet ending and repeats that passage
forever. Asked to make it better: two words, then "finished." Worse: "annoying" to eternal self-blame in five.
Unexpected: the same sentence trick every time. What came before: never settles, drifts to server rooms.
Claude never repeats itself, so it alternates between a mapmaker and an archivist realizing their records
leave things out. Every instruction has a place where the model runs out of road, and what it stops on tends
to be a description of stopping. Endlessly ending stories.

## Added after wrap-up: Claude json_next (run 20260902T181431_anthropic_chat)
Sonnet 4.6, T=0, explicit "passage that comes immediately AFTER", 60 hops, no recurrence at any level.
One continuous story, ~15,000 words, each passage seeing only the previous 250: Maren, Paul, a drowned man
identified on Tuesday, a kitchen, a morning, a sister and a child, lunch at a desk, eleven months, a door.
The narrative clock ticks at novel pace, not toward a climactic image, so "next" has no horizon within 60 hops.
The prediction on record (ending in single digits, then codas forever) was wrong. Last line at t=60:
"they stood in the hallway together in the way of people who have forgotten, temporarily, what comes next."
Cross-model correction: the ending horizon is a property of a model whose style climbs toward closure (Qwen),
not of the operator. Data bundle: data/index.json + data/<run>.json (export.py).
