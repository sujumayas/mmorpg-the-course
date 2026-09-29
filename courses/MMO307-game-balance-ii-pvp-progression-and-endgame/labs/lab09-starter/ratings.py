"""MMO307 Lab 09 starter: Glicko-1 and two-team TrueSkill.
Standard library only. Fill in the TODOs, then run
    ../../../../.venv/bin/python test_ratings.py      (from this folder)
or pytest.

Formulas are in the week 9 lecture, sections 2 and 4.
"""
import math
import random
from statistics import NormalDist

N = NormalDist()

# ------------------------------------------------------------------ Glicko-1
Q = math.log(10) / 400
NEW_R, NEW_RD, MAX_RD = 1500.0, 350.0, 350.0


def g(rd):
    """TODO step 1. Glickman's g(RD)."""
    raise NotImplementedError("g is yours to write")


def glicko_expected(r, rj, rdj):
    """TODO step 1. Expected score against opponent j."""
    raise NotImplementedError("glicko_expected is yours to write")


def glicko_update(r, rd, games):
    """TODO step 1. games is a list of (r_j, RD_j, s_j) in one rating period.
    Return (r', RD'). With an empty list, return (r, rd) unchanged."""
    raise NotImplementedError("glicko_update is yours to write")


def rd_after_idle(rd, c, periods):
    """TODO step 2. RD after `periods` rating periods, capped at MAX_RD."""
    raise NotImplementedError("rd_after_idle is yours to write")


def c_for_reset(typical_rd, periods):
    """TODO step 2. The c that takes typical_rd back to MAX_RD in `periods`."""
    raise NotImplementedError("c_for_reset is yours to write")


# ---------------------------------------------------------------- TrueSkill
MU, SIGMA = 25.0, 25 / 3
BETA, TAU = SIGMA / 2, SIGMA / 100


def win_probability(team_a, team_b):
    """TODO step 3. P(team A beats team B), teams as lists of (mu, sigma).
    Use c^2 = n beta^2 + sum of sigma^2 (no tau, no draw margin)."""
    raise NotImplementedError("win_probability is yours to write")


def trueskill_rate(winners, losers, draw_probability=0.0):
    """TODO step 3. Two-team update after a win by `winners`. Add TAU to every
    sigma first (sigma -> sqrt(sigma^2 + TAU^2)). Draw margin
    eps = Phi^-1((draw_probability + 1) / 2) * sqrt(n) * BETA.
    Return (new winners, new losers)."""
    raise NotImplementedError("trueskill_rate is yours to write")


# ---------------------------------------------------------------- provided

def elo_expected(a, b):
    return 1 / (1 + 10 ** ((b - a) / 400))


def career(system, seed, true_before=1800, true_after=2000, jump_at=150,
           games=300, k=32, c=0.0, rd_floor=30.0, opponent_rd=50.0):
    """One player, one game per period, always against an accurately rated
    opponent at the player's current rating. Returns the rating after each game.
    system is "elo" or "glicko"."""
    rng = random.Random(seed)
    r, rd, out = NEW_R, NEW_RD, []
    for i in range(games):
        true = true_before if i < jump_at else true_after
        s = 1 if rng.random() < elo_expected(true, r) else 0
        if system == "elo":
            r += k * (s - 0.5)
        else:
            rd = rd_after_idle(rd, c, 1)
            r, rd = glicko_update(r, rd, [(r, opponent_rd, s)])
            rd = max(rd, rd_floor)
        out.append(r)
    return out


if __name__ == "__main__":
    try:
        print(glicko_update(1500, 200, [(1400, 30, 1), (1550, 100, 0), (1700, 300, 0)]))
        print(trueskill_rate([(MU, SIGMA)], [(MU, SIGMA)], 0.10))
    except NotImplementedError as e:
        print("TODO:", e)
