"""MMO407 lab 05: redesign break-even. Standard-library Python 3.10+.

Model from the week 5 lecture.

  D        = sum(w_i * d_i)                    departure share
  L        = S0 * D                            immediate loss
  t*       = L / (a * r - g_new + g_old)       break-even month (inf if denominator <= 0)
  remaining after changes = (1 - D1) * (1 - D2) * ...
  second round = h * (hub players lost / S0) * (non-hub players left)

Fill in every function marked TODO, then run:  python -m unittest test_redesign.py
"""
import math
import random

# The lecture's invented game: segment -> (share w, departure share d).
S0 = 200_000
SEGMENTS = {
    "crafters and traders": (0.25, 0.45),
    "entertainers":         (0.10, 0.60),
    "combat players":       (0.45, 0.15),
    "Jedi grinders":        (0.20, 0.25),
}
HUBS = {"crafters and traders", "entertainers"}
A, G_NEW, G_OLD = 20_000, 3_000, 4_000


def departure_share(segments):
    """TODO 1. D = sum of w * d over segments."""
    raise NotImplementedError("departure_share")


def break_even(loss, a, r, g_new, g_old):
    """TODO 2. Months until the redesign passes the no-change path.
    Return math.inf when the gap never closes."""
    raise NotImplementedError("break_even")


def compound(departures):
    """TODO 3. Share of the original players left after changes with these D values, in order."""
    raise NotImplementedError("compound")


def second_round(s0, segments, hubs, h):
    """TODO 4. Extra departures among non-hub players caused by the hubs' departure."""
    raise NotImplementedError("second_round")


def chance_by_month(month, n, seed, r_range, g_old_range, d_spread):
    """TODO 5. Monte Carlo. In each of n trials draw
         r     uniformly from r_range,
         g_old uniformly from g_old_range,
         each segment's d uniformly from [d - d_spread, d + d_spread], clipped to [0, 1],
    using random.Random(seed). Compute L = S0 * D with the drawn d values and
    t* = break_even(L, A, r, G_NEW, g_old). Return the share of trials with t* <= month."""
    raise NotImplementedError("chance_by_month")


def print_lecture_tables():
    D = departure_share(SEGMENTS)
    loss = S0 * D
    print(f"departure share D = {D:.4f}, players lost = {loss:,.0f}")
    for r in (0.35, 0.25, 0.15, 0.10, 0.05):
        print(f"retain {r:.0%}: break-even month {break_even(loss, A, r, G_NEW, G_OLD):5.1f}")


if __name__ == "__main__":
    print_lecture_tables()
