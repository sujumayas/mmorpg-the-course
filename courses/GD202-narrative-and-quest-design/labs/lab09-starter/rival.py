"""GD202 Lab 09 starter: when does a stranger become a rival? Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_rival.py

Notation follows the week 9 lecture. A cast of R named characters can meet
the player. Each encounter draws one of them at random. Every character has
weight 1, except a remembered character (the rival), who has weight w >= 1.
"""
import random


def p_meet(R, w):
    """TODO step 1. Chance that one encounter is with the rival: w / (R - 1 + w).
    Raise ValueError unless R >= 1 and w > 0."""
    raise NotImplementedError("p_meet() is yours to write")


def p_rematch_within(k, R, w):
    """TODO step 1. Chance of at least one rematch in the next k encounters:
    1 - (1 - P)^k with P = p_meet(R, w). Return 0.0 when k == 0."""
    raise NotImplementedError("p_rematch_within() is yours to write")


def expected_wait(R, w):
    """TODO step 1. Mean number of encounters until the rematch: 1 / P."""
    raise NotImplementedError("expected_wait() is yours to write")


def weight_for(R, k, target):
    """TODO step 2. Smallest whole w >= 1 with p_rematch_within(k, R, w) >= target.
    Compare with a tolerance of 1e-12."""
    raise NotImplementedError("weight_for() is yours to write")


def simulate(R, w, k, trials, seed=7):
    """TODO step 3. Monte Carlo check. For each trial, draw k encounters with
    random.Random(seed).choices using weights [w, 1, 1, ...] (character 0 is
    the rival) and count the trial if character 0 appears at least once.
    Return the fraction of trials counted. Use ONE Random object for all trials."""
    raise NotImplementedError("simulate() is yours to write")


def campaign(R, w, encounters, p_player_wins, seed=7):
    """TODO step 4. A tiny nemesis system. All R characters start at rank 1 with
    weight 1 and no memory. For each encounter:

      1. draw a character with rng.choices using the current weights;
      2. the player wins with probability p_player_wins (one rng.random() call);
      3. if the player loses, that character's rank goes up by 1, its weight
         becomes w, and it is marked as remembering the player;
      4. append a dict to the log:
         {"n": i, "who": index, "player_won": bool, "rematch": bool}
         where rematch is True when the drawn character already remembered
         the player before this encounter.

    Use one rng = random.Random(seed), and call rng.choices before rng.random
    in every encounter. Return (log, ranks)."""
    raise NotImplementedError("campaign() is yours to write")


if __name__ == "__main__":
    for R, w in [(20, 1), (20, 10), (3, 1), (200, 1), (200, 50)]:
        print(f"R={R:4d} w={w:3d}  P={p_meet(R, w):.4f}  "
              f"within 5 = {p_rematch_within(5, R, w):.4f}  wait = {expected_wait(R, w):.1f}")
    log, ranks = campaign(20, 10, 40, 0.7)
    print("rematches in a 40-encounter campaign:", sum(e["rematch"] for e in log))
