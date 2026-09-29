"""MMO407 lab 03: beta exposure planner.

Bug rates are written as "fires once per N player-hours" (N = 1 / rate).
Exposure is in player-hours. Standard library only. Run the tests from inside
lab03-starter/ with:  python -m unittest test_beta_exposure.py
"""
import math

APPLE_PHASES = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00]   # share of users, days 1 to 7


def exposure(players, hours_each):
    """Player-hours."""
    return players * hours_each


def p_seen(once_per, exposure_hours):
    """Chance a bug that fires once per `once_per` player-hours fires at least
    once in `exposure_hours`: 1 - exp(-exposure / once_per)."""
    # TODO 1: use math.exp
    raise NotImplementedError("TODO 1")


def expected_firings(once_per, exposure_hours):
    """Average number of firings in `exposure_hours`."""
    return exposure_hours / once_per


def rule_of_three(exposure_hours):
    """After zero firings, the 95% bound on the rate, as 'once per N hours'.
    The rate is below 3 / exposure, so N = exposure / 3."""
    # TODO 2
    raise NotImplementedError("TODO 2")


def hours_needed(once_per, confidence=0.95):
    """Player-hours needed to see the bug at least once with `confidence`.
    Solve 1 - exp(-E / once_per) = confidence for E."""
    # TODO 3: use math.log
    raise NotImplementedError("TODO 3")


def path_exposure(total_hours, shares):
    """Split exposure across content paths. `shares` maps path -> share of play
    (they need not sum to 1; normalise them). Returns path -> player-hours."""
    # TODO 4
    raise NotImplementedError("TODO 4")


def phased_ladder(launch_week_hours, once_per, fractions=APPLE_PHASES):
    """Chance the bug has been seen by the end of each day of a phased launch.

    Launch-week hours are spread evenly over len(fractions) days at full
    rollout; on day d only fractions[d] of players have the build, so that
    day's exposure is launch_week_hours / days * fractions[d]. Returns a list
    of cumulative probabilities, one per day.
    """
    # TODO 5: accumulate each day's exposure and call p_seen
    raise NotImplementedError("TODO 5")


def print_lecture_table():
    beta, launch = exposure(5_000, 20), exposure(200_000, 15)
    for n in [10_000, 50_000, 200_000, 1_000_000, 5_000_000]:
        print(f"{n:>11,} h  seen {p_seen(n, beta):6.1%}  launch {expected_firings(n, launch):7.1f}")
    print(f"clean beta bound: once per {rule_of_three(beta):,.0f} h")


if __name__ == "__main__":
    try:
        print_lecture_table()
    except NotImplementedError as e:
        print(f"{e} is not done yet. Run the tests to see what is missing.")
