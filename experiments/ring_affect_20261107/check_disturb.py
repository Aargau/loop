#!/usr/bin/env python
"""check_disturb.py: verifies ring.py's --disturb placement without calling any backend.

  python3 -I experiments/ring_affect_20261107/check_disturb.py     (from the project root)

(a) --disturb-file F places exactly as --disturb 0=F (N=7);
(b) --disturb 0=jug.txt,8=panic.txt (N=16) puts jug in 0, panic in 8, plain elsewhere, with the real seed files;
(c) the hop-0 record from the old flags is byte-identical to the one ring.py wrote before the change
    (first line of experiments/ring_20261017/runs/cerebras_qwen_n7/ring.jsonl);
plus the error cases (repeated position, both flags, malformed item).
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
import ring  # noqa: E402  (imports loop.py too; both stdlib-only, nothing is called)


def read(p):
    return io.open(p, encoding="utf-8").read().strip()


def texts(dmap):
    return {p: read(path) for p, path in dmap.items()}


def hop0(N, seed, dmap, models, disturb_flag):
    """Mirror of main()'s hop-0 construction (kept in step with ring.py by test (c))."""
    cells = ring.place_cells(N, seed, texts(dmap))
    rec0 = {"t": 0, "cells": [{"i": i, "text": c, "hash": ring.h(c), "words": len(c.split()), "parsed": True, "finish": "seed", "model": models[i]} for i, c in enumerate(cells)]}
    if disturb_flag:
        for p, path in dmap.items():
            rec0["cells"][p]["disturb"] = os.path.basename(path)
    return json.dumps(rec0, ensure_ascii=False) + "\n"


def expect_error(label, *a):
    try:
        ring.parse_disturb(*a)
    except SystemExit as ex:
        print("  ok  %-28s -> %s" % (label, ex))
        return
    raise AssertionError(label + ": no error raised")


def main():
    old = os.path.join(ROOT, "experiments", "ring_20261017", "seeds")
    new = os.path.join(ROOT, "experiments", "ring_affect_20261107", "seeds")
    plain_old, disturb_old = os.path.join(old, "plain.txt"), os.path.join(old, "disturb.txt")
    plain_new, jug, panic = os.path.join(new, "plain.txt"), os.path.join(new, "jug.txt"), os.path.join(new, "panic.txt")

    # (a) old flag == new flag, N=7
    N = 7
    m_old = ring.parse_disturb(None, disturb_old, N)
    m_new = ring.parse_disturb("0=" + disturb_old, None, N)
    assert m_old == m_new == {0: disturb_old}, (m_old, m_new)
    seed7 = read(plain_old)
    c_old = ring.place_cells(N, seed7, texts(m_old))
    c_new = ring.place_cells(N, seed7, texts(m_new))
    assert c_old == c_new and len(c_old) == N
    assert c_old[0] == read(disturb_old) and all(c == seed7 for c in c_old[1:])
    assert ring.place_cells(N, seed7, texts(ring.parse_disturb(None, None, N))) == [seed7] * N, "no flag: seed everywhere"
    print("(a) ok  --disturb-file F == --disturb 0=F, N=7: cell 0 disturb, cells 1-6 seed")

    # (b) two disturbances, N=16, real seed files
    N = 16
    m = ring.parse_disturb("0=%s,8=%s" % (jug, panic), None, N)
    assert m == {0: jug, 8: panic}, m
    seed16 = read(plain_new)
    cells = ring.place_cells(N, seed16, texts(m))
    assert len(cells) == N
    assert cells[0] == read(jug) and cells[8] == read(panic)
    assert all(cells[i] == seed16 for i in range(N) if i not in (0, 8))
    assert cells[0] != seed16 and cells[8] != seed16 and cells[0] != cells[8]
    rec = json.loads(hop0(N, seed16, m, ["qwen3.8-27b"] * N, "0=..,8=.."))
    assert [c.get("disturb") for c in rec["cells"]] == ["jug.txt"] + [None] * 7 + ["panic.txt"] + [None] * 7
    assert "disturb" not in rec["cells"][1], "undisturbed cells carry no disturb key"
    assert ring.parse_disturb("16=%s,-8=%s" % (jug, panic), None, N) == {0: jug, 8: panic}, "positions mod N"
    print("(b) ok  --disturb 0=jug.txt,8=panic.txt, N=16: jug@0 panic@8 plain@%s; hop-0 disturb tags jug.txt@0 panic.txt@8"
          % [i for i in range(N) if i not in (0, 8)])

    # (c) byte identity with the pre-change hop-0 record
    N = 7
    with io.open(os.path.join(ROOT, "experiments", "ring_20261017", "runs", "cerebras_qwen_n7", "ring.jsonl"), encoding="utf-8") as f:
        line0 = f.readline()
    want = json.loads(line0)
    assert want["t"] == 0 and len(want["cells"]) == N
    models = [c["model"] for c in want["cells"]]
    built = hop0(N, seed7, ring.parse_disturb(None, disturb_old, N), models, None)
    got = json.loads(built)
    for w, g in zip(want["cells"], got["cells"]):
        assert (w["text"], w["hash"], w["words"]) == (g["text"], g["hash"], g["words"]), ("cell %d differs" % w["i"])
    assert built == line0, "hop-0 line not byte-identical to the archived record"
    built_new_syntax = hop0(N, seed7, ring.parse_disturb("0=" + disturb_old, None, N), models, None)
    assert built_new_syntax == line0
    print("(c) ok  hop-0 record from --disturb-file is byte-identical to cerebras_qwen_n7/ring.jsonl line 1 (%d bytes, %d cells)"
          % (len(line0.encode("utf-8")), N))

    # error cases
    print("(d) error cases:")
    expect_error("repeated position", "0=%s,0=%s" % (jug, panic), None, 16)
    expect_error("repeated after mod N", "0=%s,16=%s" % (jug, panic), None, 16)
    expect_error("both flags", "0=" + jug, disturb_old, 16)
    expect_error("malformed item", "jug.txt", None, 16)
    expect_error("non-integer position", "a=%s" % jug, None, 16)
    print("all checks passed")


if __name__ == "__main__":
    main()
