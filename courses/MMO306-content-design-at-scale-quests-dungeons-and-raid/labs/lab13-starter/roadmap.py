"""MMO306 Lab 13 starter: a roadmap simulator. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_roadmap.py

Notation follows the week 13 lecture.
    a, m, b   optimistic, most likely and pessimistic build times (days)
    mu, sigma PERT mean and spread of the build time
    n         number of staggered teams
    P         cadence, days between drops
    T         a player's exhaustion time for one drop (week 1)
"""
import random
from statistics import NormalDist

PHI = NormalDist()   # PHI.cdf(z), PHI.pdf(z), PHI.inv_cdf(q)


def pert(a, m, b):
    """TODO step 1. Return (mu, sigma) with mu = (a + 4m + b) / 6 and sigma = (b - a) / 6."""
    raise NotImplementedError("pert() is yours to write")


def on_time_chance(n, P, mu, sigma):
    """TODO step 1. q = PHI.cdf((n * P - mu) / sigma)."""
    raise NotImplementedError("on_time_chance() is yours to write")


def mean_days_late(n, P, mu, sigma):
    """TODO step 1. sigma * (pdf(z) - z * (1 - cdf(z))) with z = (n * P - mu) / sigma."""
    raise NotImplementedError("mean_days_late() is yours to write")


def teams_needed(P, mu, sigma, target):
    """TODO step 2. Smallest whole n with on_time_chance(n, P, mu, sigma) >= target."""
    raise NotImplementedError("teams_needed() is yours to write")


def fastest_cadence(n, mu, sigma, target):
    """TODO step 2. P_min = (mu + z* x sigma) / n, with z* = PHI.inv_cdf(target)."""
    raise NotImplementedError("fastest_cadence() is yours to write")


def release_days(build_times, n, P):
    """TODO step 3. Release day of every drop, given each drop's actual build time.

    Drops are numbered k = 1, 2, ... and build_times[k - 1] is drop k's build time.
    Drop k is built by team (k - 1) % n and is due on day k * P. The rules:
      start_k   = (k - n) * P                          for k <= n (pre-launch work)
      start_k   = max((k - n) * P, finish_(k - n))     for k > n (the team must be free)
      finish_k  = start_k + build_times[k - 1]
      release_k = max(k * P, finish_k, release_(k - 1))   (never early, always in order)
    with release_0 = 0. Return the list [release_1, release_2, ...]."""
    raise NotImplementedError("release_days() is yours to write")


def drought_days(releases, T):
    """TODO step 4. Total drought for a player whose T is the same for every drop.
    The launch drop is out on day 0. Each cycle runs from one release to the next,
    and its drought is max(0, gap - T). Sum over all cycles in `releases`."""
    raise NotImplementedError("drought_days() is yours to write")


def simulate(n, P, mu, sigma, drops=12, trials=2000, seed=13):
    """TODO step 5. Monte Carlo over whole roadmaps.

    For each trial draw `drops` build times with rng.gauss(mu, sigma), floored at 1 day,
    using rng = random.Random(seed) created once. Run release_days on them.
    Return (on_time_share, mean_late): the share of all drops released exactly on
    their due day k * P, and the mean of (release_k - k * P) over all drops."""
    raise NotImplementedError("simulate() is yours to write")


if __name__ == "__main__":
    mu, sigma = pert(240, 300, 480)
    print(f"mu = {mu:.0f}, sigma = {sigma:.0f}")
    for n, P in ((2, 160), (2, 175), (3, 133), (3, 124)):
        share, late = simulate(n, P, mu, sigma)
        print(f"n={n} P={P}: one drop {on_time_chance(n, P, mu, sigma):6.1%} on time, "
              f"roadmap {share:6.1%} on time, mean {late:5.1f} d late")
    print("teams for 90% at P=133:", teams_needed(133, mu, sigma, 0.9))
    print("fastest 90% cadence with 3 teams:", round(fastest_cadence(3, mu, sigma, 0.9), 1))
