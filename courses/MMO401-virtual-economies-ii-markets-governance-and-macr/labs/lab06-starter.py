"""MMO401 Lab 06 starter: corners and cartels.

Standard library only. Run:  python3 lab06-starter.py
Part A (closed-form corner model) works and checks itself against the week 6 tables.
Parts B and C are yours; they are marked TODO. Part B imports your lab 05 engine.
"""
import importlib.util
import pathlib
import random

HERE = pathlib.Path(__file__).parent

# ---- Part A: the lecture's corner model (works as shipped) -------------------------
LECTURE_LADDER = [(9.0 + 0.5 * i, 100) for i in range(10)]


def ladder_cost(ladder):
    return sum(p * q for p, q in ladder), sum(q for _, q in ladder)


def corner_profit(P, L, ladder=LECTURE_LADDER, a=250, b=10, p_after=10.0, s=0, cap=None):
    """Profit of buying the whole ladder and holding price P for L days (week 6, section 2)."""
    if cap is not None and P > cap:
        return None
    C, F = ladder_cost(ladder)
    per_day = max(0.0, a - b * P - s)
    sold = min(F, per_day * L)
    return P * sold + p_after * (F - sold) - C


def best_corner(L, step=0.01, **kw):
    a, b = kw.get("a", 250), kw.get("b", 10)
    hi = kw.get("cap") or a / b
    best = None
    P = kw.get("p_after", 10.0)
    while P <= hi + 1e-9:
        v = corner_profit(round(P, 2), L, **kw)
        if v is not None and (best is None or v > best[1]):
            best = (round(P, 2), v)
        P += step
    return best


def break_even_lag(**kw):
    L = 0.0
    while L <= 60:
        if best_corner(L, **kw)[1] >= 0:
            return round(L, 2)
        L += 0.01
    return None


def check_part_a():
    rows = [(1, -687.5), (2, -125.0), (3, 437.5), (5, 1562.5), (7, 2687.5)]
    ok = True
    for L, want in rows:
        got = best_corner(L)[1]
        ok &= abs(got - want) < 1.0
        print(f"L={L:>2}: best profit {got:9.1f} (lecture {want})")
    for label, kw, want in [("baseline", {}, 2.22), ("vendor 12", {"cap": 12}, 4.81),
                            ("after 8", {"p_after": 8.0}, 4.5), ("s=50", {"s": 50}, 5.0)]:
        got = break_even_lag(**kw)
        ok &= got is not None and abs(got - want) < 0.02
        print(f"L* {label:>9}: {got} (lecture {want})")
    return ok


# ---- Part B: a cornering agent on the lab 05 engine --------------------------------
def load_engine():
    spec = importlib.util.spec_from_file_location("lab05", HERE / "lab05-starter.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def simulate_corner(engine, hold_price, lag_days, rng, a=250, b=10, ticks_per_day=50):
    """TODO B1: agent-based version of the corner.

    1. Build a Book with the lecture ladder as asks (owner "sellers", charge_fee=False).
    2. The cornerer market-buys the whole ask side and posts one limit ask of everything
       at hold_price.
    3. Each day, read the best ask P and let round(max(0, a - b*P)) buyers arrive, spread
       evenly over ticks_per_day ticks. Each sends a market buy for one unit.
       (Re-read P each tick: once gatherers undercut, demand rises again.)
    4. From day lag_days on, gatherers post 200 units per day at p_after - 0.01.
    5. Stop after lag_days + 5 days. Mark the cornerer's leftover stock at 10.0.
    Return the cornerer's profit. Average over 50 seeds and compare with corner_profit().
    """
    raise NotImplementedError


# ---- Part C: a repeated Cournot cartel ---------------------------------------------
def cournot_profit(qs, A=100, B=1, c=10):
    P = max(0.0, A - B * sum(qs))
    return [(P - c) * q for q in qs]


def run_cartel(n, delta, rounds, strategy, rng):
    """TODO C1: play `rounds` rounds with n producers.

    `strategy(i, history, rng)` returns producer i's output this round; history is the list
    of past output vectors. Provide at least: quota keeper (always (A-c)/(2B)/n), grim
    trigger (keep quota until anyone exceeds it, then play Cournot (A-c)/((n+1)B) forever),
    and an opportunist who cheats with the best response to everyone else's quota with
    probability 1 - delta each round. Return total discounted profit per producer using
    weight delta**t.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("Part A checks:", "ok" if check_part_a() else "FAILED")
    print("Cournot n=2 cartel:", cournot_profit([22.5, 22.5]), "(expect 1012.5 each)")
    try:
        eng = load_engine()
        print("Part B:", simulate_corner(eng, 17.5, 3, random.Random(1)))
    except NotImplementedError:
        print("Part B: not written yet")
