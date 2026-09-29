"""MMO403 Lab 11: what a subscription token does to revenue.

Run:  python gen_players.py      # once, writes players.csv
      python tokens.py           # prints the scenarios
      python check_lab11.py      # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
Money is in US$ per 30 days of game time. Gold is per month.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def token_gain(T, c, s, k, sigma):
    """Monthly revenue change from adding a token (lecture section 2):
    T * (c * (1 - sigma) - k * s).
    T: game-time months paid with tokens; c: token price; s: subscription price;
    k: share of token-time players who would have paid cash without the token;
    sigma: share of token dollars that would otherwise have been spent in your store."""
    raise NotImplementedError


def breakeven_sigma(c, s, k):
    """The sigma at which token_gain is zero: 1 - k * s / c."""
    raise NotImplementedError


def blended_rate(n_cash, s, T, c):
    """Average dollars the studio receives per month of game time played:
    (n_cash * s + T * c) / (n_cash + T). Return 0.0 if nobody plays."""
    raise NotImplementedError


def classify(wtp, gold, s, gold_price, gold_share, token_on):
    """Return 'token', 'cash' or 'churn' for one player.
    With the token on: 'token' if gold_share * gold >= gold_price; otherwise 'cash' if
    wtp >= s; otherwise 'churn'. With the token off: 'cash' if wtp >= s, else 'churn'.
    (Players prefer paying with gold when they can afford it.)"""
    raise NotImplementedError


def simulate(players, s, c, gold_price, gold_share=0.5, sigma=0.0):
    """players: list of (wtp_usd, gold_per_month).
    Return a dict with keys:
      cash, token, churn         counts with the token on
      cash_off, churn_off        counts with the token off
      k                          share of token players whose wtp >= s (0.0 if no token players)
      revenue_on                 cash * s + token * c * (1 - sigma)
      revenue_off                cash_off * s
      gain                       revenue_on - revenue_off
    Token supply is assumed to clear at gold_price: cash-rich buyers outside this file
    buy one token for every token player."""
    raise NotImplementedError


def load_players():
    with open(HERE / "players.csv") as f:
        return [(float(r["wtp_usd"]), int(r["gold_per_month"])) for r in csv.DictReader(f)]


def main():
    try:
        players = load_players()
        s, c = 15.0, 20.0
        print("gold price  token   cash  churn  churn_off     k    gain ($/month)  blended $")
        for gp in (50_000, 100_000, 150_000, 250_000):
            r = simulate(players, s, c, gp)
            print(f"{gp:>10,} {r['token']:>6} {r['cash']:>6} {r['churn']:>6} {r['churn_off']:>10} "
                  f"{r['k']:5.2f} {r['gain']:>15,.0f}  {blended_rate(r['cash'], s, r['token'], c):9.2f}")
        r = simulate(players, s, c, 100_000)
        print(f"break-even sigma at gold price 100,000: {breakeven_sigma(c, s, r['k']):.2f}")
    except NotImplementedError:
        print("TODO: finish the functions, then rerun")


if __name__ == "__main__":
    main()
