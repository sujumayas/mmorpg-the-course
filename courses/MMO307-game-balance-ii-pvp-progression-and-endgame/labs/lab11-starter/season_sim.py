"""MMO307 Lab 11: a season end, simulated.

A population of players with fixed true skills plays rated games matched by
shown rating. After a warm-up so ratings settle, the season ends with a reset,
and we track how fast the matchmaker recovers.

    python3 season_sim.py --alpha 0.5 --k 32 --seed 1
    python3 test_season_sim.py

Standard library only.
"""
import argparse
import random

MU, SIGMA = 1500.0, 200.0


def expected(r_a, r_b):
    """Elo expected score of A against B (week 8)."""
    return 1.0 / (1.0 + 10.0 ** ((r_b - r_a) / 400.0))


def elo_update(r_a, r_b, score_a, k):
    """Return the two new ratings after one game. score_a is 1, 0.5 or 0."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("elo_update")


def soft_reset(ratings, alpha, mu=MU):
    """Pull every rating a share (1 - alpha) of the way to mu. Returns a new list."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("soft_reset")


def play_round(true, shown, k, rng, jitter=150.0):
    """Everyone plays one game. Pair neighbours in shown-rating order.

    Add a random jitter, uniform in [-jitter, jitter], to each shown rating
    and sort players by that jittered value. The jitter stands in for a
    matchmaker's search window, so opponents vary from game to game. Pair
    sorted positions (0, 1), (2, 3), ... Draw the winner from the TRUE
    skills with expected(). Update `shown` in place with elo_update, using
    the shown ratings. Return the list of (a, b) index pairs.
    """
    # TODO: implement (see lab sheet).
    raise NotImplementedError("play_round")


def mean_abs_error(true, shown):
    """Average of |true - shown| over all players."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("mean_abs_error")


def lopsided_share(pairs, true, gap=200.0):
    """Share of games whose TRUE skill gap is larger than `gap`."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("lopsided_share")


def run_season(alpha=0.5, k=32, players=1000, warmup=300, rounds=100, seed=1,
               jitter=150.0):
    """Warm up, reset with `alpha`, then play `rounds` rounds.
    Returns a list of (round, mean_abs_error, lopsided_share); round 0 is
    measured right after the reset, before any game."""
    rng = random.Random(seed)
    true = [rng.gauss(MU, SIGMA) for _ in range(players)]
    shown = [MU] * players
    for _ in range(warmup):
        play_round(true, shown, k, rng, jitter)
    shown = soft_reset(shown, alpha)
    out = [(0, mean_abs_error(true, shown), None)]
    for n in range(1, rounds + 1):
        pairs = play_round(true, shown, k, rng, jitter)
        out.append((n, mean_abs_error(true, shown), lopsided_share(pairs, true)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--k", type=float, default=32)
    ap.add_argument("--players", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--jitter", type=float, default=150.0)
    a = ap.parse_args()
    try:
        rows = run_season(a.alpha, a.k, a.players, seed=a.seed, jitter=a.jitter)
    except NotImplementedError as e:
        print("TODO:", e)
        return
    print("round  mean|error|  lopsided share")
    for n, err, lop in rows:
        if n in (0, 1, 5, 10, 20, 40, 60, 100):
            print(f"{n:5d}  {err:11.1f}  {'-' if lop is None else f'{lop:.3f}'}")


if __name__ == "__main__":
    main()
