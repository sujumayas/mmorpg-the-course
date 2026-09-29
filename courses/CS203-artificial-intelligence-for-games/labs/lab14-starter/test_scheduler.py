"""Checks for CS203 Lab 14. Run from this folder: python test_scheduler.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import math
import sys

import scheduler as s

results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"TODO: {exc} not written yet"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def stagger():
    guards = s.fortress()
    r = s.simulate(s.staggered(guards, 6), guards)
    if (r["worst"], r["average"]) != (4_000, 4_000):
        return False, f"worst/average: got {r['worst']}/{r['average']}, want 4000/4000"
    return max(r["wait"].values()) == 6, f"longest wait {max(r['wait'].values())}, want 6"


def budget_plain():
    guards = s.fortress(near=0)
    r = s.simulate(s.BudgetScheduler(guards, 2_000), guards)
    if r["worst"] != 2_000 or min(r["costs"]) != 2_000:
        return False, f"every frame should cost exactly 2000 us, got {min(r['costs'])}..{r['worst']}"
    return max(r["wait"].values()) == 12, f"longest wait {max(r['wait'].values())}, want 12"


def budget_order():
    guards = s.fortress(n=10, near=2, cost=100)
    sched = s.BudgetScheduler(guards, 500)
    got = [sched(1), sched(2), sched(3)]
    want = [[0, 1, 2, 3, 4], [0, 1, 5, 6, 7], [0, 1, 8, 9, 2]]
    return got == want, f"first three frames: got {got}, want {want}"


def budget_lod():
    guards = s.fortress()
    r = s.simulate(s.BudgetScheduler(guards, 2_000), guards)
    near = max(r["wait"][i] for i in range(20))
    far = max(r["wait"][i] for i in range(20, 600))
    ok = (r["worst"], near, far) == (2_000, 1, 20)
    return ok, f"worst {r['worst']}, near wait {near}, far wait {far}; want 2000, 1, 20"


def formulas():
    cases = [(0, 600, 40, 2_000), (20, 580, 40, 2_000), (0, 900, 25, 1_500),
             (30, 870, 25, 1_500), (20, 1_180, 40, 2_000), (50, 100, 40, 2_000)]
    for n_near, n_far, cost, budget in cases:
        want = s.predicted_wait(n_near, n_far, cost, budget)
        guards = s.fortress(n=n_near + n_far, near=n_near, cost=cost)
        r = s.simulate(s.BudgetScheduler(guards, budget), guards, frames=400)
        near = max((r["wait"][i] for i in range(n_near)), default=0)
        far = max(r["wait"][i] for i in range(n_near, n_near + n_far))
        if (near, far) != want:
            return False, f"{(n_near, n_far, cost, budget)}: simulated {(near, far)}, formula {want}"
    if s.predicted_wait(30, 870, 25, 1_500) != (1, 29):
        return False, "check-yourself 2 should give (1, 29)"
    return True, ""


def variable_costs():
    agents = [s.Agent(i, (20, 40, 120)[i % 3], False) for i in range(60)]
    agents.append(s.Agent(60, 3_000, False))            # one think bigger than the budget
    sched = s.BudgetScheduler(agents, 1_000)
    r = s.simulate(sched, agents, frames=200)
    if r["wait"][60] > 200:
        return False, "the 3000 us agent never thinks: the queue must always advance"
    over = [c for c in r["costs"] if c > 1_000]
    if any(c != 3_000 for c in over):
        return False, f"only the solo 3000 us think may exceed the budget, saw frame costs {sorted(set(over))}"
    return max(r["wait"].values()) <= 6, f"longest wait {max(r['wait'].values())} frames, want at most 6"


def sliced():
    for name, grid in s.MAPS.items():
        S, G = s.find(grid, "S"), s.find(grid, "G")
        cost, expanded = s.astar(grid, S, G)
        for steps in (1, 7, 50):
            frames, result = s.frames_to_answer(s.sliced_astar(grid, S, G, steps))
            if result != (cost, expanded):
                return False, f"{name}, {steps}/frame: got {result}, want {(cost, expanded)}"
            if frames != math.ceil(expanded / steps):
                return False, f"{name}, {steps}/frame: answer on frame {frames}, want ceil({expanded}/{steps})"
    blocked = ["S.#", "..#", "##G"]
    frames, result = s.frames_to_answer(s.sliced_astar(blocked, (0, 0), (2, 2), 2))
    return result == (None, 4), f"unreachable goal: got {result}, want (None, 4)"


check("step 1: staggered policy flattens the spike", stagger)
check("step 2: budgeted round robin, 600 guards", budget_plain)
check("step 2: near tier first, far cursor persists", budget_order)
check("step 2: near tier thinks every frame", budget_lod)
check("step 3: formulas match the simulation", formulas)
check("step 4: variable costs never starve an agent", variable_costs)
check("step 5: time-sliced A* gives the same answer", sliced)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
