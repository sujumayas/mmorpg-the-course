#!/usr/bin/env python3
"""MMO401 Lab 10 starter: loss rules in a small agent-based economy.

Standard library only. Run:  python3 lab10-starter.py

Agents are pilots. Each day a pilot who owns a ship may fly it. A flying ship is lost with
probability H_OUTING. On a loss, the ship's hull is destroyed and each fitting survives (goes
to the killer's hangar) with probability R. Insurance pays INSURANCE gold from an NPC.
A crafter builds BUILD_PER_DAY ships and sells them at a posted price that adjusts toward
the price that clears the market. A sales tax TAX is destroyed on every ship sale.

Your tasks are in labs/lab10.md. Places to edit are marked TODO.
"""
import random

# ---- parameters (change these per policy) -------------------------------------------
SEED = 401
DAYS = 365
N_PILOTS = 2000
INCOME_PER_DAY = 50_000          # gold each pilot earns per day (faucet)
H_OUTING = 0.02                  # chance a flying ship is lost per day
R = 0.5                          # share of fittings that survive a loss (go to the killer)
FITTINGS_PER_SHIP = 4
INSURANCE = 0                    # gold paid per hull lost (NPC faucet)
TAX = 0.05                       # sales tax on each ship sale (sink)
BUILD_PER_DAY = 40               # ships the crafting sector builds per day
START_PRICE = 200_000
PRICE_STEP = 0.03                # price adjusts 3% a day toward clearing
RESERVE_SHARE = 0.25             # a pilot buys a ship only if price <= this share of their gold


class Pilot:
    def __init__(self, rng):
        self.gold = rng.randint(100_000, 1_000_000)
        self.has_ship = rng.random() < 0.5
        self.spare_fittings = 0


def run(seed=SEED, r=R, h=H_OUTING, insurance=INSURANCE, tax=TAX, verbose=True):
    rng = random.Random(seed)
    pilots = [Pilot(rng) for _ in range(N_PILOTS)]
    price = START_PRICE
    unsold = 0
    ledger = {"faucet_income": 0, "faucet_insurance": 0, "sink_tax": 0,
              "hulls_destroyed": 0, "fittings_destroyed": 0, "fittings_looted": 0,
              "ships_built": 0, "ships_sold": 0}
    history = []
    for day in range(1, DAYS + 1):
        # faucet: daily income
        for p in pilots:
            p.gold += INCOME_PER_DAY
            ledger["faucet_income"] += INCOME_PER_DAY
        # combat: each ship owner flies; losses apply the (h, r, insurance) rule
        owners = [p for p in pilots if p.has_ship]
        for p in owners:
            if rng.random() < h:
                p.has_ship = False
                ledger["hulls_destroyed"] += 1
                killer = rng.choice(pilots)
                for _ in range(FITTINGS_PER_SHIP):
                    if rng.random() < r:
                        killer.spare_fittings += 1
                        ledger["fittings_looted"] += 1
                    else:
                        ledger["fittings_destroyed"] += 1
                p.gold += insurance
                ledger["faucet_insurance"] += insurance
        # production
        unsold += BUILD_PER_DAY
        ledger["ships_built"] += BUILD_PER_DAY
        # market: shipless pilots who can afford it buy, richest first
        buyers = sorted((p for p in pilots if not p.has_ship
                         and price <= RESERVE_SHARE * p.gold),
                        key=lambda p: -p.gold)
        sold_today = 0
        for p in buyers:
            if unsold == 0:
                break
            p.gold -= price
            p.has_ship = True
            unsold -= 1
            sold_today += 1
            ledger["sink_tax"] += tax * price     # tax destroyed; crafter income not modelled
        ledger["ships_sold"] += sold_today
        # price adjustment: excess demand raises price, unsold stock lowers it
        waiting = len(buyers) - sold_today
        if waiting > 0:
            price *= 1 + PRICE_STEP
        elif unsold > BUILD_PER_DAY:
            price *= 1 - PRICE_STEP
        # TODO (step 3): record the money supply M = total pilot gold, and check the
        # identity M(end) = M(start) + faucets - sinks. Note: ship purchases move gold to
        # the crafter, which this starter does not model as an agent. Decide how to count it.
        ships = sum(p.has_ship for p in pilots) + unsold
        history.append((day, ships, round(price), sold_today))
    if verbose:
        for day, ships, pr, sold in history[::30] + [history[-1]]:
            print(f"day {day:3d}  ships {ships:5d}  price {pr:9,d}  sold {sold:3d}")
        print({k: round(v) for k, v in ledger.items()})
    return history, ledger


if __name__ == "__main__":
    run()
    # TODO (step 4): run the three policies from lab10.md with the same seed and compare.
