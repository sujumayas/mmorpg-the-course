"""MMO407 lab 10: how long a bad launch stays on the store page.

Standard library only. Run from inside lab10-starter/:
    python review_memory.py              # prints the report (fails until the TODOs are done)
    python -m unittest test_review_memory.py
"""
import math

# The lecture's section 2 game. Invented teaching values.
LAUNCH_REVIEWS, LAUNCH_SHARE = 40_000, 0.35
NEW_SHARE, PER_MONTH = 0.85, 1_500


def lifetime_share(n0, s0, n1, r):
    """All-time positive share: n0 old reviews at share s0 plus n1 new ones at share r."""
    # TODO 1: the weighted average (n0*s0 + n1*r) / (n0 + n1)
    raise NotImplementedError("TODO 1")


def reviews_needed(n0, s0, r, target):
    """New reviews at share r that lift the all-time share from s0 to `target`.

    Return 0 if the target is already met (target <= s0).
    Return math.inf if it can never be met (target >= r).
    """
    # TODO 2: n0 * (target - s0) / (r - target), with the two edge cases above
    raise NotImplementedError("TODO 2")


def months_to_target(n0, s0, r, per_month, target):
    """Months of steady reviews at `per_month` to reach `target` (math.inf if never)."""
    return reviews_needed(n0, s0, r, target) / per_month


def make_log(launch_days=30, launch_per_day=1_000, launch_share=0.35,
             fix_day=120, per_day=50, share_after=0.85, quiet_share=0.30,
             days=720):
    """A deterministic daily review log: list of (day, positive, total).

    Days 0..launch_days-1: the launch rush. Then `per_day` reviews a day at
    `quiet_share` until the fix on `fix_day`, then at `share_after`.
    Counts are whole numbers (positive is rounded down).
    """
    log = []
    for day in range(days):
        if day < launch_days:
            total, share = launch_per_day, launch_share
        else:
            total, share = per_day, (share_after if day >= fix_day else quiet_share)
        log.append((day, math.floor(total * share), total))
    return log


def weight(age_days, mode, half_life_days=None, day=None, reset_day=None):
    """Weight of one day's reviews in a score.

    mode "lifetime": 1 for every day.
    mode "recent30": 1 if age_days < 30, else 0 (the 30 days ending today).
    mode "reset":    1 if the review's `day` >= reset_day, else 0.
    mode "exponential": 0.5 ** (age_days / half_life_days).
    """
    # TODO 3: return the weight for each mode; raise ValueError for an unknown mode
    raise NotImplementedError("TODO 3")


def score(log, today, mode, **kw):
    """Weighted positive share of all log entries with day <= today.

    Return None if the total weight is zero.
    """
    # TODO 4: sum weight * positive and weight * total over days <= today
    raise NotImplementedError("TODO 4")


def lapsed_pool(sold, active):
    """Players who bought the game and are not active this month."""
    return max(0, sold - active)


def net_returners(sold, active, reactivation, stay_rate):
    """Players a recovery update adds after one month: pool x reactivation x stay_rate."""
    return lapsed_pool(sold, active) * reactivation * stay_rate


if __name__ == "__main__":
    for months in (0, 6, 12, 24, 36, 60):
        s = lifetime_share(LAUNCH_REVIEWS, LAUNCH_SHARE, PER_MONTH * months, NEW_SHARE)
        print(f"month {months:2}  all-time {s:5.1%}")
    for target in (0.50, 0.60, 0.70, 0.80):
        m = months_to_target(LAUNCH_REVIEWS, LAUNCH_SHARE, NEW_SHARE, PER_MONTH, target)
        print(f"reach {target:.0%}: {m:5.1f} months")
    log = make_log()
    for today in (29, 119, 149, 365, 719):
        parts = []
        for mode in ("lifetime", "recent30", "reset", "exponential"):
            s = score(log, today, mode, half_life_days=90, reset_day=120)
            parts.append(f"{mode} " + ("  n/a" if s is None else f"{s:5.1%}"))
        print(f"day {today:3}  " + "  ".join(parts))
