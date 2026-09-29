"""MMO307 Lab 08 starter: an Elo ladder you can tune.
Standard library only. Fill in the TODOs, then run
    ../../../../.venv/bin/python test_elo.py      (from this folder)
or pytest.

Notation from the week 8 lecture:
    E_A = 1 / (1 + 10^((R_B - R_A) / 400))
    R_A' = R_A + K_A (S_A - E_A)
    g = ln(10) / 1600, tau = 1 / (K g), sigma = sqrt(K / (8 g))
"""
import math
import random

G = math.log(10) / 1600
START = 1500


def expected(r_a, r_b, scale=400):
    """TODO step 1. A's expected score against B."""
    raise NotImplementedError("expected is yours to write")


def update(r_a, r_b, score_a, k_a=32, k_b=None):
    """TODO step 1. Return (new r_a, new r_b). k_b defaults to k_a.
    Each player uses their own K on their own surprise."""
    raise NotImplementedError("update is yours to write")


def time_constant(k):
    """TODO step 2. Games to close about 63% of a rating gap."""
    raise NotImplementedError("time_constant is yours to write")


def settled_sd(k):
    """TODO step 2. Predicted rating standard deviation once settled."""
    raise NotImplementedError("settled_sd is yours to write")


def calibration(records, edges=(0.5, 0.6, 0.7, 0.8, 0.9, 1.0)):
    """TODO step 4. records is a list of (E_favourite, favourite_won) pairs with
    E >= 0.5. Return a list of (low, high, n, mean_E, win_rate), one per bucket
    [low, high), with the last bucket including 1.0. Skip empty buckets."""
    raise NotImplementedError("calibration is yours to write")


# ---------------------------------------------------------------- provided

def make_players(n=500, seed=1, mean=1500, sd=200):
    """Hidden true strengths, all starting at the same rating."""
    rng = random.Random(seed)
    return [{"true": rng.gauss(mean, sd), "rating": float(START), "games": 0}
            for _ in range(n)]


def k_rule_flat(k):
    return lambda player: k


def play_round(players, k_rule, rng, window=None, records=None):
    """Pair every player once (sorted by rating when window is None,
    so neighbours meet), decide results from true strength, update ratings.
    Appends (E_favourite, favourite_won) to records if given."""
    order = sorted(range(len(players)), key=lambda i: players[i]["rating"])
    for a, b in zip(order[0::2], order[1::2]):
        pa, pb = players[a], players[b]
        p_true = expected(pa["true"], pb["true"])
        s_a = 1 if rng.random() < p_true else 0
        e_a = expected(pa["rating"], pb["rating"])
        if records is not None:
            fav_won = s_a if e_a >= 0.5 else 1 - s_a
            records.append((max(e_a, 1 - e_a), fav_won))
        pa["rating"], pb["rating"] = update(pa["rating"], pb["rating"], s_a,
                                            k_rule(pa), k_rule(pb))
        pa["games"] += 1
        pb["games"] += 1


def rating_error(players):
    """Root-mean-square gap between rating and truth, after removing the
    average offset (only gaps matter)."""
    off = sum(p["rating"] - p["true"] for p in players) / len(players)
    return math.sqrt(sum((p["rating"] - p["true"] - off) ** 2 for p in players) / len(players))


if __name__ == "__main__":
    try:
        rng = random.Random(2)
        players = make_players()
        for r in range(1, 201):
            play_round(players, k_rule_flat(32), rng)
            if r in (10, 50, 100, 200):
                print(f"round {r:3}: rating error {rating_error(players):6.1f}")
    except NotImplementedError as e:
        print("TODO:", e)
