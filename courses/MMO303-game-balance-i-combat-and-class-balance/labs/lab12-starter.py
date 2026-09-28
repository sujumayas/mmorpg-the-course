"""MMO303 Lab 12 starter: stat weights from a noisy simulator.

Run it as-is to see the exact (formula) weights and a polite failure for the
parts you write. Standard library only; numpy is optional.

    python3 lab12-starter.py
"""
import math
import random
from dataclasses import dataclass, replace

RATING_PER_PCT = 40      # 40 rating = 1 percentage point
BASE_CRIT = 0.05
FIGHT_SECONDS = 300


@dataclass
class Char:
    power: float = 1000
    crit_rating: float = 1000
    haste_rating: float = 200
    m: float = 2.0            # crit damage multiplier
    crit_cap: float = None    # e.g. 0.30 for Part C step 8

    @property
    def c(self):
        c = BASE_CRIT + self.crit_rating / (RATING_PER_PCT * 100)
        return min(c, self.crit_cap) if self.crit_cap is not None else c

    @property
    def h(self):
        return self.haste_rating / (RATING_PER_PCT * 100)


def expected_dps(ch):
    """The lecture's closed form: P x (1 + (m-1)c) x (1 + h)."""
    return ch.power * (1 + (ch.m - 1) * ch.c) * (1 + ch.h)


def fight(ch, seconds, rng):
    """TODO Part A. Attack once every 1/(1+h) seconds for `seconds`.
    Each attack deals `power`, times m if rng.random() < c.
    Return total damage / seconds."""
    raise NotImplementedError("fight() is yours to write")


def mean_se(xs):
    """Mean and standard error of a list of numbers."""
    n = len(xs)
    mu = sum(xs) / n
    var = sum((x - mu) ** 2 for x in xs) / (n - 1)
    return mu, math.sqrt(var / n)


def run(ch, n_fights, seed):
    """n_fights independent fights from one seed. Reuse the seed across
    runs to get common random numbers (Part B step 3)."""
    rng = random.Random(seed)
    return mean_se([fight(ch, FIGHT_SECONDS, rng) for _ in range(n_fights)])


if __name__ == "__main__":
    base = Char()
    print(f"Closed-form DPS at 1,000 power / 1,000 crit / 200 haste: {expected_dps(base):.1f}")
    d = 100
    gp = expected_dps(replace(base, power=base.power + d)) - expected_dps(base)
    gc = expected_dps(replace(base, crit_rating=base.crit_rating + d)) - expected_dps(base)
    gh = expected_dps(replace(base, haste_rating=base.haste_rating + d)) - expected_dps(base)
    print(f"Exact normalized weights: crit {gc / gp:.3f}, haste {gh / gp:.3f} (lecture: 0.192, 0.238)")
    try:
        mu, se = run(base, 1000, seed=1)
        print(f"Simulated DPS: {mu:.1f} +/- {se:.1f}")
    except NotImplementedError as e:
        print(f"Simulated DPS: not run yet ({e})")
