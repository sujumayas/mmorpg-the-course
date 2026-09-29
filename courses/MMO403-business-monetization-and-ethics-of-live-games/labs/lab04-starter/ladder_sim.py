"""MMO403 Lab 04: an Elo ladder in which some players buy an edge.

Given code. It uses your win_prob and rating_gap from edge.py.

    python ladder_sim.py [edge] [payer_share] [sigma] [seed]
    python ladder_sim.py 0.10 0.2 0.25 404

Each player has a true skill drawn from N(0, 200). Buyers add the rating
value of their edge to their true strength. Everyone starts rated 0.
Matchmaking pairs each chosen player with the closest-rated of 16 random
candidates. Results follow the Elo expected-score curve on TRUE strength,
and ratings update with K = 16. The script reports, over the second half of
the run, win rates of buyers and non-buyers, and the buyer share of the top
10% and top 1% of the final ladder.
"""
import random
import sys

from edge import rating_gap, win_prob

PLAYERS = 4000
MATCHES = 1_000_000
K = 16
CANDIDATES = 16


def expected(diff):
    return 1 / (1 + 10 ** (-diff / 400))


def run(edge=0.10, f=0.2, sigma=0.25, seed=404):
    rng = random.Random(seed)
    delta = rating_gap(win_prob(edge, sigma)) if edge > 0 else 0.0
    skill = [rng.gauss(0, 200) for _ in range(PLAYERS)]
    payer = [rng.random() < f for _ in range(PLAYERS)]
    strength = [s + (delta if b else 0.0) for s, b in zip(skill, payer)]
    rating = [0.0] * PLAYERS
    wins = {True: 0, False: 0}
    games = {True: 0, False: 0}
    for m in range(MATCHES):
        a = rng.randrange(PLAYERS)
        pool = [rng.randrange(PLAYERS) for _ in range(CANDIDATES)]
        pool = [c for c in pool if c != a] or [(a + 1) % PLAYERS]
        o = min(pool, key=lambda c: abs(rating[c] - rating[a]))
        a_wins = rng.random() < expected(strength[a] - strength[o])
        e = expected(rating[a] - rating[o])
        change = K * ((1 if a_wins else 0) - e)
        rating[a] += change
        rating[o] -= change
        if m >= MATCHES // 2:
            for who, won in ((a, a_wins), (o, not a_wins)):
                games[payer[who]] += 1
                wins[payer[who]] += won
    order = sorted(range(PLAYERS), key=lambda i: rating[i], reverse=True)
    top10 = order[: PLAYERS // 10]
    top1 = order[: PLAYERS // 100]
    return {
        "delta": delta,
        "payer_win_rate": wins[True] / max(1, games[True]),
        "non_payer_win_rate": wins[False] / max(1, games[False]),
        "payers_overall": sum(payer) / PLAYERS,
        "payers_top10": sum(payer[i] for i in top10) / len(top10),
        "payers_top1": sum(payer[i] for i in top1) / len(top1),
    }


if __name__ == "__main__":
    args = [float(x) for x in sys.argv[1:4]]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 404
    r = run(*args, seed=seed)
    for k, v in r.items():
        print(f"{k:20} {v:.3f}")
