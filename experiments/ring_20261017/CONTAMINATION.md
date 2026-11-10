# The Astra ring run is contaminated by the harness

Found 2026-11-09 by Claude Mythos 5.2 with Justin Bronder, while reading the ring study for a new design. This note
records what was observed, what is inferred, and what was not checked. The run data is left as it was.

## What is wrong

In `runs/astra_tarnok_n7`, cells received each other's answers. The ring's only channel between cells is the last
sentence of each neighbour, so content that crosses any other way breaks the experiment. The reading that "Astra lets
the battle invade" rests on that leak.

## Cause

`step_codex` in `loop.py` ran every Codex call in one shared directory and named the answer file
`last_<pid>_<millisecond>.md`. `ring.py` starts four cells at once in threads of one process, so those four calls
often computed the same file name. When two of them finished close together, both Codex processes wrote the same
file and the later write won. The first thread to return read that file (the other cell's answer) and deleted it.
The other thread found no file, raised, waited two seconds and retried, so its call took about twice as long.

The backend is fixed in the same commit as this note: each call now gets its own directory and file.

## Evidence in the run (observed)

`wrong_input_scan.py` in this directory compares each cell's output with every cell's previous text.

- Twelve hops have a cell whose output is a rewrite of another cell's previous text. The other seven ring runs
  (four Qwen, two Mythos, one Gemini) have none.
- Each of those hops has one call of 21 to 26 seconds against a median of 10.0 seconds.
- Every source and every receiving cell is among cells 0 to 3, the four that start together with `--workers 4`.

| hop | cell that got the wrong answer | answer was for | slow call that hop |
|---|---|---|---|
| 1 | 3 | 0 | cell 0, 24.5 s |
| 8 | 3 | 1 | cell 1, 22.1 s |
| 11 | 1 | 0 | cell 0, 23.6 s |
| 13 | 2 | 0 or 1 | cell 0, 23.0 s |
| 15 | 3 | 0 or 1 | cell 1, 22.1 s |
| 19 | 0 | 2 | cell 2, 21.3 s |
| 27 | 0 | 3 | cell 3, 22.5 s |
| 29 | 2 | 1 | cell 1, 21.6 s |
| 30 | 0 | 2 | cell 2, 26.3 s |
| 32 | 3 | 0 | cell 0, 22.6 s |
| 36 | 3 | 2 | cell 2, 22.1 s |
| 38 | 3 | 0 | cell 0, 23.2 s |

At hops 13 and 15 the texts of cells 0 and 1 were already about 0.75 alike (cell 1 had received cell 0's answer at
hop 11), so the scan cannot tell which of the two was the source. In the other ten the slow cell is the source.

The first event is the plainest. At hop 1 cell 3 could see only kitchen sentences, and it returned "The battle raged
on. Tarnok hefted his crude bronze axe, searching the churn of bodies for the usurper."

At hop 40 cells 0 to 3 hold battle text and cells 4 to 6 hold kitchen text. That boundary is the worker count.

## Reproduction without model calls (observed)

The unpatched `step_codex` was imported unchanged and its executable replaced by a stand-in that reads the state,
waits, and writes a labelled answer to the `-o` path. Seven cells were driven as `ring.py` drives them. In 40 hops,
cells 0 to 3 shared an output file name in most hops, 87 answers reached the wrong cell, and 66 calls retried. With
the patched function the same test gave 280 distinct files, no wrong deliveries and no retries. The stand-in's timing
is much tighter than real Codex calls, so 87 says nothing about the real rate.

## What is inferred, and what was not checked

- The real run did not log its file names, so the collision in that run is inferred from the code, the latency
  signature and the reproduction.
- Twelve is a floor. Hops 6, 7, 9 and 22 also have slow calls and no flagged cell; a swap between two cells with
  similar text would not be seen by the scan.
- The patched backend has not been run against the real Codex CLI. The stand-in test covers the Python side only.
- No other study was checked. Any code that calls the Codex backend from several threads of one process was exposed,
  including `loop.py --parallel`. Separate processes were safe because the pid differs.

## What should not be relied on

- Every reading of the Astra ring run in `PROTOCOL.md`, on the site (the frontier ring rooms), and in the commit
  message of 8a0479e ("Astra lets the battle invade").
- Astra's behaviour in a ring is unknown until the run is repeated on the fixed backend.
