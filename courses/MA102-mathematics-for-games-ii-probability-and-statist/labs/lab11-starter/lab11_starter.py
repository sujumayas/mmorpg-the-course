"""MA102 lab 11 starter: Monte Carlo simulation of raid loot with pity.

Run it as a script (python lab11_starter.py) or paste the cells into a
notebook. It uses only the Python standard library, and the same
random.Random(seed) generator as the week 11 lecture, so seeds reproduce.

What is done for you:
    load_config(path)            read raid_config.json or validation_config.json
    simulate(trial, n, seed)     run n trials, return the list of results
    estimate(trial, n, seed)     mean of n trials and its 95% margin
    percentile(values, q)        inclusive percentile (the week 12 rule)

What you write:
    trial_raid(rng, config)      one full raid, kill by kill, until every
                                 player has their item

Rules of one kill (read with raid_config.json):
    1. Every player still missing their item adds 1 to their pity counter.
    2. Roll `drops_per_kill` items, each one independently from the
       weighted table (the same item can drop twice).
    3. For each dropped item, the eligible players are those still missing
       that item. If there are any, one of them, chosen uniformly at random,
       gets it. If there are none, the item is wasted.
    4. After the drops, any player still missing their item whose counter
       has reached `pity_kills` gets it from pity. `pity_kills: null` means
       no pity.
The raid ends on the kill where the last player gets their item.
"""
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).parent


def load_config(name):
    with open(HERE / name) as f:
        return json.load(f)


def simulate(trial, n, seed):
    """Run `trial(rng)` n times with one seeded generator. Returns a list."""
    rng = random.Random(seed)
    return [trial(rng) for _ in range(n)]


def estimate(trial, n, seed):
    """Mean of n trials and its 95% margin (1.96 standard errors).

    If every result is 0 or 1 the mean is a probability p-hat and the
    margin uses sqrt(p(1 - p) / n), as in the lecture. Otherwise it uses
    the sample SD, 1.96 * s / sqrt(n).
    """
    xs = simulate(trial, n, seed)
    mean = sum(xs) / n
    if all(x in (0, 1) for x in xs):
        se = math.sqrt(mean * (1 - mean) / n)
    else:
        s = math.sqrt(sum((x - mean) ** 2 for x in xs) / (n - 1))
        se = s / math.sqrt(n)
    return mean, 1.96 * se


def percentile(values, q):
    """Inclusive percentile, q in [0, 100]. Matches PERCENTILE.INC."""
    v = sorted(values)
    pos = (len(v) - 1) * q / 100
    lo = math.floor(pos)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (pos - lo) * (v[hi] - v[lo])


def trial_raid(rng, config):
    """Play one raid until every player has their item.

    Return a dict: {"kills": total kills, "pity_awards": items given by pity}.
    Use rng.random() or rng.choices(...) for every random draw, never the
    global random module, so that seeds reproduce.
    """
    raise NotImplementedError("Write trial_raid, then run step 1 before anything else.")


if __name__ == "__main__":
    val = load_config("validation_config.json")

    # Step 1: P(item within 10 kills). Exact: 1 - 0.95**10 = 0.4013.
    def got_within_10(rng):
        return 1 if trial_raid(rng, val)["kills"] <= 10 else 0

    exact = 1 - 0.95 ** 10
    print(f"Exact {exact:.4f}")
    for n in (1_000, 10_000, 100_000):
        p, m = estimate(got_within_10, n, seed=1111)
        covers = "covers" if abs(p - exact) <= m else "MISSES"
        print(f"n = {n:>7,}  p-hat = {p:.4f} ± {m:.4f}  {covers} the exact value")
