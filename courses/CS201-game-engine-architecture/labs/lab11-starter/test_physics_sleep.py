"""Checks for Lab 11. Run from inside lab11-starter: python test_physics_sleep.py"""
import math
import sys

from physics_sleep import (HZ, SleepSystem, World, build_islands, process_contacts,
                           settle, sleep_time_alone)

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


@check("step 1: islands from contacts, static bodies excluded")
def _():
    assert build_islands(4, []) == [[0], [1], [2], [3]]
    assert build_islands(5, [(0, 1), (3, 4), (1, 2)]) == [[0, 1, 2], [3, 4]]
    # body 9 is a floor touched by everything: it must not merge the islands
    pairs = [(0, 9), (1, 9), (2, 9), (1, 2)]
    assert build_islands(10, pairs, static={9}) == [[0], [1, 2], [3], [4], [5], [6], [7], [8]]
    big = [(i, i + 1) for i in range(999)]
    assert build_islands(1000, big) == [list(range(1000))]


@check("step 2: sleep time of a single body")
def _():
    expect = {4.0: 2.691, 2.0: 2.344, 1.0: 1.998, 0.5: 1.651, 0.25: 1.305}
    for v0, t in expect.items():
        assert abs(sleep_time_alone(v0, 2.0, 0.05, 0.5) - t) < 0.001, (v0, sleep_time_alone(v0, 2.0, 0.05, 0.5))
    assert sleep_time_alone(0.01, 2.0, 0.05, 0.5) == 0.5


@check("step 3a: the lecture's stack sleeps as one island at 2.683 s")
def _():
    counts = settle([4.0, 2.0, 1.0, 0.5, 0.25], [0] * 5)
    assert counts[160 - 1] == 5 and counts[161 - 1] == 0, (counts[159], counts[160])
    assert set(counts[:160]) == {5}
    counts = settle([4.0, 2.0, 1.0, 0.5, 0.25], [0] * 5, stacks=200)
    assert counts[round(2.5 * HZ) - 1] == 1000 and counts[round(3.0 * HZ) - 1] == 0


@check("step 3b: one jittery body keeps its island awake")
def _():
    floors = [0, 0, 0.06, 0, 0]
    assert settle([4.0, 2.0, 1.0, 0.5, 0.25], floors)[-1] == 5
    counts = settle([4.0, 2.0, 1.0, 0.5, 0.25], floors, v_sleep=0.10)
    assert counts[139 - 1] == 5 and counts[140 - 1] == 0, (counts[138], counts[139])


@check("step 3c: touching a sleeping island wakes all of it")
def _():
    s = SleepSystem(4, v_sleep=0.05, t_sleep=0.5)
    pile = [(0, 1), (1, 2)]
    for _ in range(30):
        awake = s.tick([0, 0, 0, 1.0], pile)
    assert awake == 1 and s.asleep[:3] == [True] * 3 and not s.asleep[3]
    awake = s.tick([0, 0, 0, 1.0], pile + [(2, 3)])
    assert awake == 4 and s.timers[:3] == [1, 1, 1], (awake, s.timers)


@check("step 4a: buffered contact processing destroys each body once")
def _():
    w = World({1: 30, 2: 10, 3: 10, 4: 50})
    w.step([(1, 2), (2, 3), (1, 3), (4, 1)])
    assert process_contacts(w, 10) == [1, 2, 3]
    assert w.health == {4: 40}, w.health


@check("step 4b: the unsafe callback style fails, the buffered style does not")
def _():
    w = World({1: 10, 2: 10})
    try:
        w.step([(1, 2)], on_contact=lambda world, a, b: world.destroy(a))
    except RuntimeError:
        pass
    else:
        raise AssertionError("destroy during step should raise")
    assert not w.locked
    w.step([(1, 2), (2, 1)])
    assert process_contacts(w, 5) == [1, 2] and w.health == {}


passed = 0
for name, ok, msg in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  ({msg})"))
    passed += ok
print(f"{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
