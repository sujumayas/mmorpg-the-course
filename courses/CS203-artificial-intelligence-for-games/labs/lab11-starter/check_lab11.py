"""Checks for CS203 Lab 11. Run: python check_lab11.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys

import stage as s

results = []
SLOTS = [(-3.0, 10.0), (-1.0, 10.0), (1.0, 10.0), (3.0, 10.0)]
UNITS = [(2, 2), (-1, 1), (-1, 4), (-4, 3)]


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def admission():
    st = s.StageManager(12, 10)
    got = [st.request_slot("A", 4), st.request_slot("T", 8), st.request_slot("B", 4),
           st.request_slot("A", 4)]
    return got == [True, True, False, True] and st.grid_used == 12, \
        f"got {got}, grid_used {st.grid_used}; want [True, True, False, True], 12"


def attacks():
    st = s.StageManager(12, 10)
    st.request_slot("A", 4)
    st.request_slot("T", 8)
    t = st.choose_attack("T", s.CREATURES["troll"][1])
    a = st.choose_attack("A", s.CREATURES["soldier"][1])
    again = st.choose_attack("A", s.CREATURES["soldier"][1])
    outsider = st.choose_attack("B", s.CREATURES["soldier"][1])
    got = (t and t[0], a and a[0], again, outsider, st.attack_used)
    return got == ("charge", "swing", None, None, 9), \
        f"got {got}, want ('charge', 'swing', None, None, 9)"


def releasing():
    st = s.StageManager(12, 10)
    st.request_slot("A", 4)
    st.request_slot("T", 8)
    st.choose_attack("T", s.CREATURES["troll"][1])
    st.release("T")
    st.release("nobody")
    ok = st.grid_used == 4 and st.attack_used == 0 and st.request_slot("B", 4) \
        and "T" not in st.on_grid
    return ok, f"after releasing T: grid_used {st.grid_used}, attack_used {st.attack_used}"


def rotation():
    pack = [(f"S{i}", "soldier") for i in range(6)]
    per_round, count = s.run_rounds(pack, 12, 20, 8)
    fair = all(c == 4 for c in count.values())
    return fair and per_round == [42] * 8, \
        f"per round {per_round} (want [42]*8), attacks {count} (want 4 each)"


def damage():
    got = (s.damage_taken(8, None), s.damage_taken(8, 3), s.damage_taken(8, 4),
           s.damage_taken(10, 3), s.damage_taken(2, 3), s.damage_taken(5, 1, dps=20, kill_time=2))
    want = (1800, 1050, 1300, 1350, 150, 200)
    return got == want, f"got {got}, want {want}"


def assignment():
    g = s.assign_greedy(UNITS, SLOTS)
    b = s.assign_best(UNITS, SLOTS)
    ok = g == (2, 1, 0, 3) and b == (3, 2, 1, 0) and \
        abs(s.total_distance(UNITS, SLOTS, b) - 30.35) < 0.01
    return ok, f"greedy {g} (want (2, 1, 0, 3)), best {b} (want (3, 2, 1, 0))"


def best_never_worse():
    import random
    rng = random.Random(11)
    for _ in range(200):
        units = [(rng.uniform(-5, 5), rng.uniform(0, 5)) for _ in range(5)]
        slots = [(rng.uniform(-5, 5), rng.uniform(8, 12)) for _ in range(5)]
        gb = s.total_distance(units, slots, s.assign_best(units, slots))
        gg = s.total_distance(units, slots, s.assign_greedy(units, slots))
        if gb > gg + 1e-9 or sorted(s.assign_best(units, slots)) != list(range(5)):
            return False, f"best {gb:.2f} worse than greedy {gg:.2f}, or not a permutation"
    return True, ""


check("step 1: request_slot admits by grid weight (Dawe's example)", admission)
check("step 1: choose_attack takes the strongest affordable attack, once", attacks)
check("step 2: release frees grid and attack capacity", releasing)
check("step 2: six soldiers, capacity 12: fair rotation, 4 attacks each in 8 rounds", rotation)
check("step 3: damage_taken matches the lecture table", damage)
check("step 4: greedy and best assignment on the lecture's four units", assignment)
check("step 4: best assignment is never longer than greedy (200 random cases)", best_never_worse)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
