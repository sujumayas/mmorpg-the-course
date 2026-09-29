"""MMO307 Lab 14: does the ladder hide an overpowered class?

Standard-library Python only. Run the tests with:
    .venv/bin/python test_ladder.py        (or: pytest test_ladder.py)
Run an experiment with:
    .venv/bin/python ladder.py --delta 60 --f 1.0 --seed 1

Model (lecture week 14, section 2):
    E(d)        = 1 / (1 + 10 ** (-d / 400))      Elo expected score, d = own minus opponent
    rating      ~ skill + f * delta               where the rating settles
    win rate    = E((1 - f) * delta)              class win rate against equal-rated opponents
    top share   = 1 - Phi(z_top - f * delta / sigma)

Fill in the four functions marked TODO. `simulate_ladder` and the helpers below
them are complete and call your functions.
"""
import argparse
import random
from statistics import NormalDist

START_RATING = 1500.0


def expected_score(r_a, r_b):
    """Elo expected score of A against B: 1 / (1 + 10 ** ((r_b - r_a) / 400))."""
    # TODO: implement
    raise NotImplementedError


def elo_update(r_a, r_b, score_a, k=24.0):
    """Return (new_r_a, new_r_b) after one game. score_a is 1 for an A win, 0 for a loss."""
    # TODO: implement
    raise NotImplementedError


def class_win_rate(delta, f):
    """Closed-form win rate of a class with advantage `delta` (rating points)
    when a fraction `f` of the rating's games are played on it."""
    # TODO: implement
    raise NotImplementedError


def top_share(shift, sigma, top_fraction):
    """Share of a group whose ratings sit `shift` points above everyone else's
    that lands in the ladder's top `top_fraction` (e.g. 0.001 for the top 0.1%).
    Ratings of everyone else are normal with SD `sigma`. Use statistics.NormalDist."""
    # TODO: implement
    raise NotImplementedError


# ---------------------------------------------------------------- complete below


def simulate_ladder(n_players=1000, rounds=200, delta=60.0, class_share=0.2,
                    f=1.0, k=24.0, sigma=200.0, pair_noise=25.0, seed=1, start="patch"):
    """Ladder simulation.

    start="patch" (default): ratings already match skill, and a patch gives the
    strong class its advantage at round 0 (a mid-season buff).
    start="reset": every player starts at START_RATING (a season reset, week 11).

    A `class_share` of players main the strong class. Each game, a main plays the
    strong class with probability f, otherwise a neutral class. Everyone else always
    plays neutral. Each round the matchmaker sorts players by rating plus a little
    noise and pairs neighbours. Games where both sides play the strong class
    (mirrors) are not recorded in the class win rate (see MMO303 week 1).

    Returns a dict with:
      "wins", "games": lists, one entry per round, for strong-class non-mirror games
      "ratings", "is_main": final ratings and a flag per player
    """
    rng = random.Random(seed)
    skill = [rng.gauss(START_RATING, sigma) for _ in range(n_players)]
    is_main = [rng.random() < class_share for _ in range(n_players)]
    rating = list(skill) if start == "patch" else [START_RATING] * n_players
    wins, games = [], []
    for _ in range(rounds):
        order = sorted(range(n_players), key=lambda i: rating[i] + rng.gauss(0, pair_noise))
        w = g = 0
        for a, b in zip(order[0::2], order[1::2]):
            on_a = is_main[a] and rng.random() < f
            on_b = is_main[b] and rng.random() < f
            s_a = skill[a] + (delta if on_a else 0.0)
            s_b = skill[b] + (delta if on_b else 0.0)
            a_wins = rng.random() < expected_score(s_a, s_b)
            rating[a], rating[b] = elo_update(rating[a], rating[b], 1.0 if a_wins else 0.0, k)
            if on_a != on_b:
                g += 1
                w += 1 if (a_wins == on_a) else 0
        wins.append(w)
        games.append(g)
    return {"wins": wins, "games": games, "ratings": rating, "is_main": is_main}


def window_win_rate(result, start, end):
    """Strong-class win rate over rounds start..end-1."""
    w = sum(result["wins"][start:end])
    g = sum(result["games"][start:end])
    return w / g if g else float("nan")


def representation(result, top_fraction):
    """Strong-class share of the top `top_fraction` of final ratings,
    divided by its share of the whole ladder (1.0 means fair representation)."""
    n = len(result["ratings"])
    top_n = max(1, round(n * top_fraction))
    top = sorted(range(n), key=lambda i: result["ratings"][i], reverse=True)[:top_n]
    share_top = sum(result["is_main"][i] for i in top) / top_n
    share_all = sum(result["is_main"]) / n
    return share_top / share_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delta", type=float, default=60.0)
    ap.add_argument("--f", type=float, default=1.0)
    ap.add_argument("--players", type=int, default=1000)
    ap.add_argument("--rounds", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--start", choices=["patch", "reset"], default="patch")
    args = ap.parse_args()
    res = simulate_ladder(args.players, args.rounds, args.delta, f=args.f,
                          seed=args.seed, start=args.start)
    print(f"closed form win rate   {class_win_rate(args.delta, args.f):.4f}")
    print(f"win rate, rounds 0-9   {window_win_rate(res, 0, 10):.4f}")
    print(f"win rate, last 50      {window_win_rate(res, args.rounds - 50, args.rounds):.4f}")
    print(f"representation top 10% {representation(res, 0.10):.2f}x")
    print(f"closed form top 10%    {top_share(args.f * args.delta, 200, 0.10) / 0.10:.2f}x")


if __name__ == "__main__":
    main()
