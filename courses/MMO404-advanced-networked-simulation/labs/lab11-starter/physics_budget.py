"""MMO404 Lab 11: how much physics does a zone really run?

    python physics_budget.py --check          # tests your functions against the week 11 lecture
    python physics_budget.py --measure        # awake bodies in a live world vs Little's law
    python physics_budget.py --sweep out.csv  # awake count and CPU for kick rates 10 to 1,000 per s

Implement every function marked TODO. The model is in the week 11 lecture, sections 2 and 4.
Standard library only.
"""
import csv
import math
import random
import sys

F = 30            # physics steps per second
C_B = 4e-6        # CPU seconds per awake body per step
LIN_TOL = 0.01    # m/s: a body faster than this cannot sleep (Box2D v2.4.1 value)
T_SLEEP = 0.5     # s a body (or island) must stay slow before it sleeps (Box2D v2.4.1 value)
DAMPING = 2.0     # 1/s: linear damping, speed falls as v0 * exp(-DAMPING * t)
BUDGET_MS = 200.0 # physics budget in ms of CPU per second


# ---------------------------------------------------------------- part A: the sleep rule

def update_sleep_time(speed, sleep_time, dt, lin_tol=LIN_TOL):
    """Return the body's new sleep time after one step: reset to 0 if speed > lin_tol,
    otherwise increase by dt. TODO."""
    raise NotImplementedError


def island_should_sleep(sleep_times, t_sleep=T_SLEEP):
    """An island sleeps only when every body in it has been slow for at least t_sleep. TODO."""
    raise NotImplementedError


def t_move_for(v0, damping=DAMPING, lin_tol=LIN_TOL):
    """Seconds until a body kicked to speed v0 slows to lin_tol under exponential damping.
    Return 0 if v0 <= lin_tol. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- part B: the budget model

def awake_little(delta, tau, n):
    """Little's law: min(n, delta * tau). TODO."""
    raise NotImplementedError


def awake_exact(delta, tau, n):
    """Random pushes on n bodies: n * (1 - exp(-delta * tau / n)). TODO."""
    raise NotImplementedError


def cpu_ms_per_s(n_awake, f=F, c_b=C_B):
    """Physics CPU in ms per second: 1000 * f * c_b * n_awake. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- part C: islands on a seam

def islands(bodies, contacts):
    """Connected components of the contact graph, as a sorted list of sorted lists.
    Use union-find with path halving. TODO."""
    raise NotImplementedError


def island_owner(group, owner):
    """The server that owns most bodies in the group. Ties go to the server whose name
    sorts first, so both sides agree without talking. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- the world (given)

class Body:
    __slots__ = ("vx", "vy", "awake", "sleep_time")

    def __init__(self):
        self.vx = self.vy = 0.0
        self.awake, self.sleep_time = False, 0.0


def run_world(n, delta, v0, seconds=120.0, seed=11, warmup=20.0):
    """n bodies spread thinly enough that they never touch (each is its own island).
    Kicks arrive as a Poisson process at rate delta; a kick wakes a random body and gives it
    speed v0 in a random direction. Every step, awake bodies are damped, their sleep time is
    updated with your update_sleep_time, and your island_should_sleep decides if they sleep.
    Returns the average number of awake bodies after the warm-up."""
    rng = random.Random(seed)
    bodies = [Body() for _ in range(n)]
    dt = 1.0 / F
    decay = math.exp(-DAMPING * dt)
    next_kick = rng.expovariate(delta)
    t, total, samples = 0.0, 0, 0
    awake = set()
    while t < seconds:
        t += dt
        while next_kick <= t:
            i = rng.randrange(n)
            a = rng.uniform(0, 2 * math.pi)
            b = bodies[i]
            b.vx, b.vy = v0 * math.cos(a), v0 * math.sin(a)
            b.awake, b.sleep_time = True, 0.0
            awake.add(i)
            next_kick += rng.expovariate(delta)
        for i in list(awake):
            b = bodies[i]
            b.vx *= decay
            b.vy *= decay
            b.sleep_time = update_sleep_time(math.hypot(b.vx, b.vy), b.sleep_time, dt)
            if island_should_sleep([b.sleep_time]):
                b.awake, b.vx, b.vy = False, 0.0, 0.0
                awake.discard(i)
        if t > warmup:
            total += len(awake)
            samples += 1
    return total / samples


# ---------------------------------------------------------------- tests and tools

def check():
    assert update_sleep_time(0.5, 0.3, 1 / 30) == 0.0, "a fast body resets its sleep time"
    assert abs(update_sleep_time(0.005, 0.3, 0.1) - 0.4) < 1e-12
    assert island_should_sleep([0.6, 0.5, 0.9]) is True
    assert island_should_sleep([0.6, 0.49, 0.9]) is False, "one restless body keeps the island awake"
    assert abs(t_move_for(2.0) - math.log(200) / 2) < 1e-9
    assert t_move_for(0.005) == 0

    assert awake_little(430, 3.5, 20_000) == 1505
    assert awake_little(430, 3.5, 1_000) == 1_000
    assert round(awake_exact(430, 3.5, 20_000)) == 1450
    assert round(awake_exact(430, 3.5, 2_000)) == 1058
    assert abs(cpu_ms_per_s(1505) - 180.6) < 1e-9
    assert abs(cpu_ms_per_s(300) - 36.0) < 1e-9

    owner = {"c1": "A", "c2": "A", "c3": "B", "c4": "B", "c5": "B", "c6": "A"}
    contacts = [("c1", "c2"), ("c2", "c3"), ("c4", "c5")]
    assert islands(owner, contacts) == [["c1", "c2", "c3"], ["c4", "c5"], ["c6"]]
    assert island_owner(["c1", "c2", "c3"], owner) == "A"
    assert island_owner(["c4", "c5"], owner) == "B"
    assert island_owner(["c3", "c6"], owner) == "A", "ties go to the name that sorts first"
    chain = [(f"b{i}", f"b{i + 1}") for i in range(999)]
    assert len(islands([f"b{i}" for i in range(1000)], chain)) == 1, "long chains must work"

    tau = t_move_for(2.0) + T_SLEEP
    got = run_world(2_000, 50, 2.0, seconds=80)
    want = awake_exact(50, tau, 2_000)
    assert abs(got - want) / want < 0.06, f"live world {got:.0f} awake, model {want:.0f}"
    print("all checks passed")


def measure():
    tau = t_move_for(2.0) + T_SLEEP
    print(f"kick speed 2 m/s: t_move = {t_move_for(2.0):.3f} s, tau = {tau:.3f} s")
    print(" delta   Little   exact   measured")
    for delta in (10, 50, 200, 800):
        print(f"{delta:6}  {awake_little(delta, tau, 2_000):7.0f}  {awake_exact(delta, tau, 2_000):6.0f}"
              f"  {run_world(2_000, delta, 2.0):9.0f}")


def sweep(path):
    tau = t_move_for(2.0) + T_SLEEP
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["delta", "awake_little", "awake_exact", "cpu_ms_per_s", "share_of_budget"])
        for k in range(10, 31):
            delta = round(10 ** (k / 10))
            a = awake_exact(delta, tau, 20_000)
            w.writerow([delta, round(awake_little(delta, tau, 20_000), 1), round(a, 1),
                        round(cpu_ms_per_s(a), 2), round(cpu_ms_per_s(a) / BUDGET_MS, 3)])
    print("wrote", path)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--measure" in sys.argv:
        measure()
    elif "--sweep" in sys.argv:
        sweep(sys.argv[sys.argv.index("--sweep") + 1])
    else:
        print(__doc__)
