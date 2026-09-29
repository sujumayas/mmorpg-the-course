"""MMO404 Lab 12: what does a zone's AI cost, and when?

    python ai_budget.py --check          # tests your functions against the week 12 lecture
    python ai_budget.py --measure        # model vs simulated cost for spread and grouped players
    python ai_budget.py --sweep out.csv  # model cost for 1 to 1,000 spread players

Implement every function marked TODO. The model is in the week 12 lecture, sections 2 and 3.
Standard library only.
"""
import csv
import math
import random
import sys
import time

WORLD = 4000.0                                   # metres per side
N_MOBS = 10_000
TIERS = ((50, 10.0), (150, 2.0), (400, 0.2))     # (radius m, thinks per second); beyond: dormant
C_T = 20e-6                                      # CPU seconds per think
TICK_HZ = 10


# ---------------------------------------------------------------- part A: the cost model

def tier_rate(d, tiers=TIERS):
    """Think rate for a monster whose nearest player is d metres away (strict d < radius);
    0.0 beyond the last tier. TODO."""
    raise NotImplementedError


def model_tier_counts(n_players, n_mobs=N_MOBS, area=WORLD * WORLD, tiers=TIERS):
    """Expected monsters per tier for n_players spread at random, from
    covered(r) = 1 - exp(-n * pi * r^2 / area). Returns a list, one count per tier. TODO."""
    raise NotImplementedError


def cost_ms_per_s(tier_counts, tiers=TIERS, c_t=C_T):
    """AI CPU in ms per second: 1000 * c_t * sum(count * rate). TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- part B: finding the nearest player

def nearest_grid(mobs, players, max_r=TIERS[-1][0]):
    """For each monster, the distance to its nearest player if it is below max_r, else math.inf.
    Use a uniform grid of players with cells of side max_r and check only the 3 x 3 block
    of cells around each monster. Must agree with nearest_brute. TODO."""
    raise NotImplementedError


def nearest_brute(mobs, players, max_r=TIERS[-1][0]):
    """Reference answer for nearest_grid. Given. O(monsters x players)."""
    out = []
    for m in mobs:
        d = min(math.dist(m, p) for p in players)
        out.append(d if d < max_r else math.inf)
    return out


# ---------------------------------------------------------------- part C: scheduling

def thinks_per_tick(periods, n_ticks, phased):
    """periods[i] is how many ticks monster i waits between thinks (0 means dormant).
    In step: monster i thinks when tick % period == 0. Phased: when (tick + i) % period == 0.
    Return a list with the number of thinks on each of ticks 0 .. n_ticks - 1. TODO."""
    raise NotImplementedError


def budgeted_tick(acc, weights, budget):
    """One tick of a priority accumulator (week 4). Add each monster's weight to its
    accumulator, pick the `budget` monsters with the largest accumulators (ties to the lower
    index), reset their accumulators to 0, and return their indices sorted. Modifies acc. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- the world (given)

def make_world(n_players, groups=None, seed=12):
    """Monsters uniform over the zone; players uniform (groups=None) or round-robin in
    `groups` clusters with a 30 m Gaussian spread. Same layout as the lecture."""
    rng = random.Random(seed)
    mobs = [(rng.uniform(0, WORLD), rng.uniform(0, WORLD)) for _ in range(N_MOBS)]
    if groups is None:
        players = [(rng.uniform(0, WORLD), rng.uniform(0, WORLD)) for _ in range(n_players)]
    else:
        centres = [(rng.uniform(500, 3500), rng.uniform(500, 3500)) for _ in range(groups)]
        players = [(cx + rng.gauss(0, 30), cy + rng.gauss(0, 30))
                   for cx, cy in (centres[i % groups] for i in range(n_players))]
    return mobs, players


def simulated_counts(n_players, groups=None, finder=None):
    mobs, players = make_world(n_players, groups)
    dists = (finder or nearest_grid)(mobs, players)
    counts = [0] * len(TIERS)
    for d in dists:
        for k, (r, _) in enumerate(TIERS):
            if d < r:
                counts[k] += 1
                break
    return counts


# ---------------------------------------------------------------- tests and tools

def check():
    assert tier_rate(49.9) == 10.0 and tier_rate(50) == 2.0
    assert tier_rate(399.9) == 0.2 and tier_rate(400) == 0.0
    one = model_tier_counts(1)
    assert [round(c, 1) for c in one] == [4.9, 39.2, 265.2], one
    assert abs(cost_ms_per_s(one) - 3.61) < 0.01, cost_ms_per_s(one)
    assert [round(c) for c in model_tier_counts(200)] == [935, 4932, 4114]
    assert abs(cost_ms_per_s(model_tier_counts(200)) - 400.8) < 0.05
    assert abs(cost_ms_per_s(model_tier_counts(50)) - 141.8) < 0.05

    rng = random.Random(5)
    mobs = [(rng.uniform(0, 2000), rng.uniform(0, 2000)) for _ in range(1500)]
    players = [(rng.uniform(0, 2000), rng.uniform(0, 2000)) for _ in range(40)]
    g, b = nearest_grid(mobs, players), nearest_brute(mobs, players)
    assert all((x == y) or abs(x - y) < 1e-9 for x, y in zip(g, b)), "nearest_grid disagrees"
    assert simulated_counts(200) == [939, 5000, 4001], simulated_counts(200)

    periods = [1] * 939 + [5] * 5000 + [50] * 4001 + [0] * 60
    step = thinks_per_tick(periods, 50, phased=False)
    phase = thinks_per_tick(periods, 50, phased=True)
    assert step[0] == 9940 and sum(step) == sum(phase), (step[0], sum(step), sum(phase))
    assert max(phase) <= 939 + 1000 + 81, max(phase)

    acc = [0.0] * 3
    counts = [0, 0, 0]
    for _ in range(500):
        for i in budgeted_tick(acc, [3.0, 1.0, 1.0], 1):
            counts[i] += 1
    assert sum(counts) == 500, "exactly `budget` thinks per tick"
    assert counts[0] > 1.5 * counts[1] and min(counts) >= 100, f"weights ignored or starvation: {counts}"
    acc = [0.0] * 4
    assert budgeted_tick(acc, [1.0, 1.0, 1.0, 1.0], 2) == [0, 1], "ties go to the lower index"
    assert budgeted_tick(acc, [1.0, 1.0, 1.0, 1.0], 2) == [2, 3], "waiting raises priority"
    print("all checks passed")


def measure():
    print("layout              near  mid   far    model ms/s  simulated ms/s")
    for label, n, g in (("1 player", 1, None), ("200 spread", 200, None),
                        ("200 in 10 groups", 200, 10), ("200 in one raid", 200, 1)):
        sim = simulated_counts(n, g)
        model = f"{cost_ms_per_s(model_tier_counts(n)):10.1f}" if g is None else "         -"
        print(f"{label:18} {sim[0]:5} {sim[1]:5} {sim[2]:5}  {model}  {cost_ms_per_s(sim):14.1f}")
    for finder in (nearest_brute, nearest_grid):
        t0 = time.perf_counter()
        simulated_counts(200, finder=finder)
        print(f"{finder.__name__}: {time.perf_counter() - t0:.2f} s for 200 players")


def sweep(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["players", "near", "mid", "far", "cost_ms_per_s"])
        for n in (1, 2, 5, 10, 20, 50, 100, 200, 300, 500, 700, 1000):
            c = model_tier_counts(n)
            w.writerow([n] + [round(x, 1) for x in c] + [round(cost_ms_per_s(c), 2)])
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
