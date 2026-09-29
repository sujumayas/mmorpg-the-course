"""MMO308 Lab 13 starter: measuring an incident and choosing revert or fix.

Run it with:
    .venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab13-starter.py

Every function marked TODO raises NotImplementedError. The tests at the bottom
print PASS or FAIL for each part and the script exits with status 1 while any
test fails. Do not change the tests or the data generator. Standard library only.
"""
import math
import random
import sys

# ---------------------------------------------------------------------------
# Data: a synthetic Saturday evening, sampled every 15 minutes (do not edit)
# ---------------------------------------------------------------------------

SAMPLE_HOURS = 0.25          # 15-minute samples
START = "18:00"              # first sample
PATCH_INDEX = 5              # the patch went live just before sample 5 (19:15)


def make_evening(seed=13):
    """Return (last_week, today) concurrent-user series, 24 samples from 18:00.

    Today is about 2% busier than last week before the incident. The patch at
    19:15 breaks logins for most players until about 21:00, then players rebound.
    """
    rng = random.Random(seed)
    base = [40_000 + 16_000 * math.sin(math.pi * (i + 2) / 26) for i in range(24)]
    last_week = [round(b * (1 + rng.uniform(-0.01, 0.01))) for b in base]
    today = []
    for i, b in enumerate(base):
        x = b * 1.02 * (1 + rng.uniform(-0.01, 0.01))
        if 5 <= i <= 7:
            x *= 0.40 - 0.05 * (i - 5)      # logins failing, players dropping
        elif 8 <= i <= 11:
            x *= 0.30                       # most players out
        elif i == 12:
            x *= 0.85                       # fix live, players returning
        elif 13 <= i <= 15:
            x *= 1.06                       # rebound
        today.append(round(x))
    return last_week, today


# ---------------------------------------------------------------------------
# Part A. Measuring the damage (lecture section 3)
# ---------------------------------------------------------------------------

def scaled_baseline(last_week, today, pre_start, pre_end):
    """Scale last week's series by sum(today[pre_start:pre_end]) / sum(last_week[pre_start:pre_end]).

    Return a list of floats, one per sample.
    """
    raise NotImplementedError("A1: scaled baseline")


def lost_player_hours(baseline, observed, start, sample_hours=SAMPLE_HOURS):
    """From sample `start` to the end, return (gross, rebound, net) in player-hours.

    gross   = sum of positive gaps (baseline - observed) x sample_hours
    rebound = sum of the negative gaps as a positive number x sample_hours
    net     = gross - rebound
    """
    raise NotImplementedError("A2: lost player-hours")


# ---------------------------------------------------------------------------
# Part B. Revert first or fix forward (lecture section 2)
# ---------------------------------------------------------------------------

def expected_fix_forward(r, p, F):
    """Expected outage in minutes: r/p + F."""
    raise NotImplementedError("B1: expected fix-forward outage")


def expected_revert_first(R, q, r, p, F):
    """Expected outage in minutes: R + (1 - q) (r/p + F)."""
    raise NotImplementedError("B2: expected revert-first outage")


def q_star(R, r, p, F):
    """Break-even belief R / (r/p + F)."""
    raise NotImplementedError("B3: break-even belief")


def still_down(t, strategy, R, q, r, p, F):
    """Chance the game is still down t minutes after the page.

    strategy is "fix" or "revert". Use the lecture's step formulas:
      fix:    1 if t < F + r, else (1 - p) ** floor((t - F) / r)
      revert: 1 if t < R,     else (1 - q) * fix-curve(t - R)
    """
    raise NotImplementedError("B4: survival curve")


# ---------------------------------------------------------------------------
# Part C. Check the model by simulation
# ---------------------------------------------------------------------------

def simulate(strategy, R, q, r, p, F, n, seed):
    """Simulate n incidents and return a list of outage lengths in minutes.

    Use rng = random.Random(seed). Fix forward: count rounds until one succeeds
    (rng.random() < p means success), outage = rounds x r + F. Revert first:
    draw rng.random() < q for "revert worked" (outage R); otherwise R plus a
    fix-forward outage drawn the same way.
    """
    raise NotImplementedError("C1: simulation")


# ---------------------------------------------------------------------------
# Part D. Rank postmortem action items
# ---------------------------------------------------------------------------

def rank_actions(actions):
    """actions: list of (name, player_hours_saved_per_year, engineer_days).

    Return the names sorted by player-hours saved per engineer-day, best first.
    Ties keep their input order.
    """
    raise NotImplementedError("D1: rank action items")


# ---------------------------------------------------------------------------
# Tests (do not edit)
# ---------------------------------------------------------------------------

def _close(a, b, tol):
    return abs(a - b) <= tol


def run_tests():
    results = []

    def check(name, fn):
        try:
            ok = fn()
        except NotImplementedError as e:
            ok, name = False, f"{name} (not written yet: {e})"
        except Exception as e:  # show the error but keep going
            ok, name = False, f"{name} ({type(e).__name__}: {e})"
        results.append(ok)
        print(("PASS  " if ok else "FAIL  ") + name)

    # Part A, on the lecture's 30-minute table
    lw = [52_000, 54_000, 55_000, 55_500, 55_000, 53_000, 50_000]
    td = [51_500, 21_000, 14_000, 15_000, 49_000, 55_500, 51_000]
    check("A1 scaled baseline matches the lecture table",
          lambda: [round(x) for x in scaled_baseline(lw, td, 0, 1)]
          == [51_500, 53_481, 54_471, 54_966, 54_471, 52_490, 49_519])

    def a2():
        g, rb, n = lost_player_hours(scaled_baseline(lw, td, 0, 1), td, 1, 0.5)
        return _close(g, 59_194.5, 1) and _close(rb, 2_245.5, 1) and _close(n, 56_949, 1)
    check("A2 gross, rebound and net match the lecture", a2)

    def a3():
        last_week, today = make_evening()
        base = scaled_baseline(last_week, today, 0, PATCH_INDEX)
        g, rb, n = lost_player_hours(base, today, PATCH_INDEX)
        return 40_000 < g < 80_000 and rb > 0 and n < g
    check("A3 the synthetic evening gives a plausible loss", a3)

    # Part B
    check("B1 fix forward = 165", lambda: _close(expected_fix_forward(30, 0.25, 45), 165, 1e-9))
    check("B2 revert first = 86", lambda: _close(expected_revert_first(20, 0.6, 30, 0.25, 45), 86, 1e-9))
    check("B3 q* = 0.121", lambda: _close(q_star(20, 30, 0.25, 45), 20 / 165, 1e-9))
    params = dict(R=20, q=0.6, r=30, p=0.25, F=45)
    expected = {60: (1.000, 0.400), 120: (0.562, 0.300), 240: (0.178, 0.095),
                360: (0.056, 0.030), 480: (0.018, 0.010)}
    check("B4 survival table matches the lecture",
          lambda: all(_close(still_down(t, "fix", **params), a, 0.0006)
                      and _close(still_down(t, "revert", **params), b, 0.0006)
                      for t, (a, b) in expected.items()))

    # Part C
    def c1():
        fx = simulate("fix", n=20_000, seed=1, **params)
        rv = simulate("revert", n=20_000, seed=2, **params)
        m_fx, m_rv = sum(fx) / len(fx), sum(rv) / len(rv)
        tail = sum(1 for x in fx if x > 240) / len(fx)
        return _close(m_fx, 165, 3) and _close(m_rv, 86, 3) and _close(tail, 0.178, 0.015)
    check("C1 simulation agrees with the formulas", c1)

    # Part D
    acts = [("be more careful", 0, 1), ("kill switch on trades", 30_000, 5),
            ("revert without restart", 50_000, 20), ("runbook", 6_000, 1)]
    check("D1 ranking by player-hours per engineer-day",
          lambda: rank_actions(acts) == ["kill switch on trades", "runbook",
                                         "revert without restart", "be more careful"])

    passed = sum(results)
    print(f"\n{passed}/{len(results)} tests passed")
    return passed == len(results)


if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
