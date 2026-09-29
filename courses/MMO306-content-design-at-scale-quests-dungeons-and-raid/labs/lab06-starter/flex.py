"""MMO306 Lab 06: a flexible tier ladder.

Finish every function marked TODO, then run `python test_flex.py`.
Standard-library Python only. Model and notation follow the week 6 lecture:
    tanks t(N), healers h(N) = N // 5, damage dealers d(N) = N - t(N) - h(N)
    per-dealer requirement r(N) = H(N) / (T * u * d(N))
"""
import math


def roster(N, tanks=2, extra_tank_at=None):
    """Return (tanks, healers, dealers) for a raid of N players.
    If extra_tank_at is set and N >= extra_tank_at, the raid brings one more tank."""
    raise NotImplementedError("roster")


def health_linear(N, H20):
    """Linear rule: the same health per player at every size, H20 * N / 20."""
    raise NotImplementedError("health_linear")


def per_dealer(H, N, T, u, **roster_kw):
    """Effective DPS each damage dealer must bring: H / (T * u * d(N))."""
    raise NotImplementedError("per_dealer")


def health_neutral(N, H20, T, u, **roster_kw):
    """Health that gives every N the same per-dealer requirement as N = 20."""
    raise NotImplementedError("health_neutral")


def clean_raidwide(p, N, k):
    """Clean-pull chance for a mechanic that targets all N players k times."""
    raise NotImplementedError("clean_raidwide")


def clean_targeted(p, N, k):
    """Clean-pull chance for a mechanic that targets N // 5 players k times."""
    raise NotImplementedError("clean_targeted")


def clean_fixed(p, m, k):
    """Clean-pull chance for a mechanic that targets exactly m players k times."""
    raise NotImplementedError("clean_fixed")


def wipes_to_clear(fraction, step=0.05, max_stacks=10):
    """A group has `fraction` of the effective DPS it needs. Each wipe adds `step`
    to its damage multiplier (additive), up to max_stacks. Return the number of wipes
    before it can clear (0 if it already can), or None if it never can."""
    raise NotImplementedError("wipes_to_clear")


if __name__ == "__main__":
    for N in (10, 15, 20, 25, 30):
        H = health_linear(N, 5_040_000)
        print(N, roster(N), H, round(per_dealer(H, N, 300, 0.8), 1),
              round(health_neutral(N, 5_040_000, 300, 0.8)))
