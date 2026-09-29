"""Checks for Lab 10. Run from inside lab10-starter: python test_script_host.py"""
import math
import sys

from script_host import (BoundaryError, Engine, HandleTable, Host, bound, marshal,
                         move_batched, move_one, predict_frame_us, run_frame)

results = []


def check(name):
    def wrap(fn):
        try:
            fn()
            results.append((name, True, ""))
        except Exception as e:  # noqa: BLE001
            results.append((name, False, f"{type(e).__name__}: {e}"))
        return fn
    return wrap


@check("step 1a: bound functions refuse stale handles")
def _():
    t = HandleTable()
    goblin = t.create({"hp": 10})
    calls = []
    def apply_damage(obj, amount):
        calls.append(amount)
        obj["hp"] -= amount
        return obj["hp"]
    dmg = bound(t, apply_damage)
    assert dmg(goblin, 3) == 7
    t.destroy(goblin)
    arrow = t.create({"hp": 1})
    assert arrow == (0, 1), arrow
    assert dmg(goblin, 5) is None
    assert dmg("junk", 5) is None and dmg((9, 0), 5) is None
    assert calls == [3], calls
    assert t.get(arrow) == {"hp": 1}


@check("step 1b: bound functions pass extra arguments and exceptions through")
def _():
    t = HandleTable()
    h = t.create([1, 2])
    assert bound(t, lambda obj, a, b: obj + [a, b])(h, 3, 4) == [1, 2, 3, 4]
    def boom(obj):
        raise KeyError("no such stat")
    try:
        bound(t, boom)(h)
    except KeyError:
        return
    raise AssertionError("exception was swallowed")


@check("step 2: marshal copies allowed values and refuses the rest")
def _():
    src = [1, 2.5, "a", None, True, (3, 4), [5, [6]]]
    out = marshal(src)
    assert out == src and out is not src and out[6] is not src[6]
    for bad in ({"a": 1}, {1, 2}, (1, 2, 3), (1, "x"), object(), [1, {"k": 2}]):
        try:
            marshal(bad)
        except BoundaryError:
            continue
        raise AssertionError(f"marshal accepted {bad!r}")


@check("step 3: batched movement matches per-object and counts crossings")
def _():
    for n, batch in ((10, 1), (10, 3), (1000, 100), (1000, 1000), (7, 50)):
        e1, e2 = Engine(), Engine()
        h1 = [e1.spawn(i, -i, i % 3, 1.5) for i in range(n)]
        h2 = [e2.spawn(i, -i, i % 3, 1.5) for i in range(n)]
        e2.handles.destroy(h2[0])
        e1.handles.destroy(h1[0])
        host1, host2 = Host(e1), Host(e2)
        for h in h1:
            move_one(host1, h, 0.5, e1.pos[h[0]])
        move_batched(host2, h2, 0.5, batch)
        assert host2.crossings == 2 * math.ceil(n / batch), (n, batch, host2.crossings)
        for i in range(n):
            assert all(abs(a - b) < 1e-9 for a, b in zip(e1.pos[i], e2.pos[i])), i


@check("step 4: the crossing model reproduces the lecture table")
def _():
    expect = {1: 11000.0, 10: 2000.0, 100: 1100.0, 1000: 1010.0, 10000: 1001.0}
    for b, us in expect.items():
        assert abs(predict_frame_us(10000, b, 1.0, 0.1) - us) < 1e-6, b
    assert abs(predict_frame_us(4000, 40, 2.0, 0.5) - 2200.0) < 1e-6
    assert abs(predict_frame_us(7, 3, 1.0, 1.0) - 10.0) < 1e-6


@check("step 5a: budgeted scheduler matches the lecture trace")
def _():
    def patrol(name, steps):
        for i in range(steps):
            yield f"{name} step {i}"
    q = [patrol("guard", 3), patrol("merchant", 5)]
    frames, errs = [], []
    while q:
        frames.append(run_frame(q, 3, errs))
    assert frames == [["guard step 0", "merchant step 0", "guard step 1"],
                      ["merchant step 1", "guard step 2", "merchant step 2"],
                      ["merchant step 3", "merchant step 4"]], frames
    assert errs == []


@check("step 5b: a crashing script is removed and logged, others keep running")
def _():
    def bad():
        yield "bad 0"
        yield 1 / 0
    def good():
        for i in range(4):
            yield f"good {i}"
    q, errs = [bad(), good()], []
    out = []
    while q:
        out += run_frame(q, 2, errs)
    assert out == ["bad 0", "good 0", "good 1", "good 2", "good 3"], out
    assert len(errs) == 1 and errs[0].startswith("ZeroDivisionError"), errs


passed = 0
for name, ok, msg in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  ({msg})"))
    passed += ok
print(f"{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
