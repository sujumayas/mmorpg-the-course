#!/usr/bin/env python3
"""MMO401 Lab 11 starter: a token market inside a small agent-based economy.

Standard library only. Run:  python3 lab11-starter.py

Two kinds of agent:
- Cash-rich players buy tokens from the studio store with real money and sell them for gold.
- Time-rich players earn gold by playing and spend part of their gold on tokens.

The market is a daily call auction (a "trading post" market): every seller hands in tokens,
every buyer hands in gold, and the price is total gold bid divided by tokens offered,
P = B / Q, as in week 11. Each buyer receives tokens in proportion to their gold.
Tokens received are redeemed for game time at once (a token sink).

Your tasks are in labs/lab11.md. Places to edit are marked TODO.
"""
import random

SEED = 11
DAYS = 360
N_CASH = 300                 # cash-rich players
N_TIME = 3000                # time-rich players
STORE_PRICE = 20.0           # dollars per token
BUY_CHANCE = 0.05            # chance a cash-rich player buys one token on a given day
GOLD_PER_HOUR = 20_000       # time-rich income per hour of play
HOURS_PER_DAY = 2.0
SPEND_SHARE = 0.03           # share of gold balance a time-rich player bids per day
FEE = 0.0                    # TODO (step 3): fee on the seller's proceeds, destroyed

# Events (day numbers). Set to None to switch off.
FAUCET_UP_DAY = 120          # from this day, GOLD_PER_HOUR rises by FAUCET_UP_FACTOR
FAUCET_UP_FACTOR = 1.25
SALE_DAY = 200               # on this day BUY_CHANCE is multiplied by SALE_FACTOR
SALE_FACTOR = 3.0
NEW_USE_DAY = 280            # from this day, SPEND_SHARE is multiplied by NEW_USE_FACTOR
NEW_USE_FACTOR = 1.5


def run(seed=SEED, fee=FEE, verbose=True):
    rng = random.Random(seed)
    time_gold = [rng.uniform(50_000, 500_000) for _ in range(N_TIME)]
    cash_gold = [0.0] * N_CASH
    history = []
    dollars = 0.0
    for day in range(1, DAYS + 1):
        wage = GOLD_PER_HOUR * (FAUCET_UP_FACTOR if FAUCET_UP_DAY and day >= FAUCET_UP_DAY else 1)
        share = SPEND_SHARE * (NEW_USE_FACTOR if NEW_USE_DAY and day >= NEW_USE_DAY else 1)
        chance = BUY_CHANCE * (SALE_FACTOR if SALE_DAY and day == SALE_DAY else 1)
        # faucet: time-rich players play
        for i in range(N_TIME):
            time_gold[i] += wage * HOURS_PER_DAY * rng.uniform(0.5, 1.5)
        # store: cash-rich players buy tokens with money and offer them
        sellers = [j for j in range(N_CASH) if rng.random() < chance]
        q = len(sellers)
        dollars += q * STORE_PRICE
        # bids: each time-rich player bids a share of gold
        bids = [share * g for g in time_gold]
        b = sum(bids)
        if q == 0:
            history.append((day, None, b, q))
            continue
        price = b / q
        for i in range(N_TIME):
            time_gold[i] -= bids[i]        # tokens received = bids[i] / price, redeemed at once
        for j in sellers:
            cash_gold[j] += price * (1 - fee)
        # TODO (step 3): count fee * price * q as destroyed gold in a ledger.
        # TODO (step 2): record money supply M = sum(time_gold) + sum(cash_gold).
        history.append((day, price, b, q))
    if verbose:
        for day, price, b, q in history[::30]:
            p = "   n/a" if price is None else f"{price:12,.0f}"
            print(f"day {day:3d}  tokens {q:3d}  gold bid {b:16,.0f}  price {p}")
        print(f"dollars to the studio: {dollars:,.0f}")
    return history


def monthly_average(history):
    """Average price per 30-day month, skipping days with no sellers."""
    out = []
    for m in range(0, len(history), 30):
        prices = [p for _, p, _, _ in history[m:m + 30] if p is not None]
        out.append(sum(prices) / len(prices) if prices else None)
    return out


if __name__ == "__main__":
    h = run()
    print("monthly average price:", [round(x) for x in monthly_average(h)])
    # TODO (step 4): implied gold per dollar e = P / STORE_PRICE, and implied wage
    # W = STORE_PRICE / (P / wage). Print both per month.
