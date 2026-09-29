"""MMO403 Lab 04: what a purchased edge is worth.

Run:  python edge.py          # prints the lecture's table once your functions work
      python ladder_sim.py    # runs a full Elo ladder with buyers (uses win_prob and rating_gap)
      python check_lab04.py   # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
The formulas are in lecture 04, section 2.
"""
from math import erf, sqrt


def phi(x):
    """Standard normal CDF. Given, do not change."""
    return 0.5 * (1 + erf(x / sqrt(2)))


def win_prob(b, sigma):
    """Chance that a player with a +b damage edge (b = 0.10 for +10%) beats an
    equal-skill opponent, when each player's log kill time has noise sigma.
    p = phi( ln(1 + b) / (sigma * sqrt(2)) )."""
    raise NotImplementedError


def rating_gap(p):
    """Elo rating difference that gives expected score p: 400 * log10(p / (1 - p))."""
    raise NotImplementedError


def top_cutoff(delta, f, sd=200.0, top=0.10):
    """Rating t above which a share `top` of all players sits, when a share f of
    players are rated N(delta, sd) and the rest N(0, sd). Solve by bisection on
    [-3000, 3000] with 100 iterations. Return t."""
    raise NotImplementedError


def payer_share_on_top(delta, f, sd=200.0, top=0.10):
    """Share of the top `top` of the ladder held by payers:
    f * (1 - phi((t - delta) / sd)) / top, with t from top_cutoff."""
    raise NotImplementedError


def unranked_win_rates(p, f):
    """Random opponents, no matchmaking. Payers meet payers with chance f.
    Return (payer_win_rate, non_payer_win_rate) where
    payer = f * 0.5 + (1 - f) * p and non-payer = (1 - f) * 0.5 + f * (1 - p)."""
    raise NotImplementedError


def main():
    print(" edge   win     Elo   top10%  top1%")
    for b in (0.0, 0.02, 0.05, 0.10, 0.20):
        p = win_prob(b, 0.25)
        d = rating_gap(p)
        print(f"{b:5.0%}  {p:6.1%}  {d:6.1f}  {payer_share_on_top(d, 0.2):6.1%}"
              f"  {payer_share_on_top(d, 0.2, top=0.01):6.1%}")


if __name__ == "__main__":
    main()
