"""Checks for CS203 Lab 10. Run: python check_lab10.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys

import perception as p

results = []

WALL_MAP = p.load_grid("""
.......
.......
...#...
...#...
...#...
""")


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def close(a, b, tol=1e-6):
    return a is not None and b is not None and abs(a - b) <= tol


def fill_times():
    got = [p.detect_time(d) for d in (0, 5, 10, 20, 35)] + [p.detect_time(10, 0.5)]
    want = [1.0, 1.75, 2.5, 4.0, 4.0, 5.0]
    ok = all(close(g, w) for g, w in zip(got, want)) and p.detect_time(5, 0) == float("inf")
    return ok, f"got {got}, want {want} and inf at light 0"


def breakeven():
    got = (p.break_even(10), p.break_even(20), p.break_even(10, 1.0, 40.0))
    want = (2.5 / 8.5, 0.4, 2.5 / 42.5)
    return all(close(g, w) for g, w in zip(got, want)), f"got {got}, want {want}"


def meter_fill_and_drain():
    npc = p.Awareness(forget=6.0)
    for _ in range(10):                      # 1 s in view at 10 m
        npc.update(True, 10)
    if not close(npc.meter, 0.4) or npc.state != "unaware":
        return False, f"after 1 s at 10 m: meter {npc.meter:.3f} {npc.state}, want 0.400 unaware"
    for _ in range(30):                      # 3 s hidden
        npc.update(False, 10)
    if not close(npc.meter, 0.0):
        return False, f"after hiding 3 s: meter {npc.meter:.3f}, want 0 (floored)"
    for _ in range(40):                      # 4 s in view at 0 m
        npc.update(True, 0)
    return close(npc.meter, 1.0) and npc.state == "alert", \
        f"after 4 s at 0 m: meter {npc.meter:.3f} {npc.state}, want capped 1.000 alert"


def hysteresis():
    npc = p.Awareness(forget=6.0)
    for _ in range(13):                      # 1.3 s at 10 m -> 0.52
        npc.update(True, 10)
    if npc.state != "suspicious":
        return False, f"meter {npc.meter:.3f} should be suspicious, got {npc.state}"
    for _ in range(10):                      # drain 1 s -> 0.353, still >= 0.3
        npc.update(False, 10)
    if npc.state != "suspicious":
        return False, f"meter {npc.meter:.3f} dropped below 0.5 but is above 0.3; want suspicious, got {npc.state}"
    for _ in range(4):                       # -> 0.287 < 0.3
        npc.update(False, 10)
    if npc.state != "unaware":
        return False, f"meter {npc.meter:.3f} below 0.3; want unaware, got {npc.state}"
    for _ in range(25):                      # 2.5 s at 10 m -> alert
        npc.update(True, 10)
    for _ in range(59):                      # 5.9 s hidden: not yet drained
        npc.update(False, 10)
    if npc.state != "alert":
        return False, f"alert NPC must stay alert until the meter is 0 (meter {npc.meter:.3f}, {npc.state})"
    npc.update(False, 10)
    return npc.state == "unaware", f"after draining fully want unaware, got {npc.state}"


def peeking():
    peek = [(1.5, True, 10, 1.0), (2.0, False, 10, 1.0)] * 5
    t, _ = p.simulate(peek)
    safe = [(1.0, True, 10, 1.0), (3.0, False, 10, 1.0)] * 10
    s, _ = p.simulate(safe)
    return t == 8.2 and s is None, f"peek 1.5/2: {t} (want 8.2); peek 1/3: {s} (want None)"


def paths():
    got = (p.path_distance(WALL_MAP, (3, 1), (3, 5)),
           p.path_distance(WALL_MAP, (0, 0), (0, 6)),
           p.path_distance([".#."], (0, 0), (0, 2)))
    want = (8, 6, None)
    return got == want, f"got {got}, want {want}"


def hearing():
    d = p.path_distance(WALL_MAP, (3, 1), (3, 5))
    got = (p.heard(6, 4), p.heard(6, d), p.heard(10, d), p.heard(10, d, offscreen_far=True),
           p.heard(20, None))
    want = (True, False, True, False, False)
    return got == want, f"got {got}, want {want}"


check("step 1: detect_time matches the table, capped at range, inf in the dark", fill_times)
check("step 1: break_even is T / (T + F)", breakeven)
check("step 2: meter fills, drains, floors at 0 and caps at 1", meter_fill_and_drain)
check("step 3: suspicious on at 0.5, off below 0.3; alert sticks until drained", hysteresis)
check("step 3: peeking run matches the lecture (8.2 s and never)", peeking)
check("step 4: BFS path distance around a wall", paths)
check("step 4: heard() uses path distance and the off-screen half radius", hearing)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
