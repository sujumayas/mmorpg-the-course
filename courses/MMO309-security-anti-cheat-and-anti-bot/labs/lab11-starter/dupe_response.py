"""MMO309 Lab 11: dupe response, rollback versus trace versus ban.

The model is the week 11 lecture's. A dupe creates D items worth p gold each on a server with
money supply M. Each hour a share k of the items still held by the ring leaves it. After T hours
the share that has left is m = 1 - exp(-k T). Of those, a share b were bought by honest players
(the item still exists and carries its serial) and 1 - b are gone (vendored or crafted).
P honest players are online on average; w is the hours of play needed to earn one item's price;
lam is the player-hours the team trades to avoid 1 point of inflation.

Policies and outputs (hours = honest player-hours lost, inflation in % of M, keeps in gold):
    rollback      hours = P T              inflation = 0                      keeps = 0
    trace         hours = w b m D          inflation = 100 (1-b) m D p / M    keeps = m D p
    ring_only     hours = 0                inflation = 100 m D p / M          keeps = m D p
    trace_refund  like trace, but the team debits up to `wallet` gold from the ring and refunds
                  buyers: debit = min(wallet, m D p); hours = w max(0, b m D - debit / p);
                  keeps = m D p - debit
    harm = hours + lam * inflation
    ring net after a ban of accounts worth A = keeps - A

Fill in every function marked TODO. Run `python dupe_response.py` for a summary.
"""
import random
from math import exp

PARAMS = dict(D=50_000, p=1_000, M=500_000_000, k=0.2, b=0.6, P=4_000, w=0.5, lam=20_000)
POLICIES = ("rollback", "trace", "ring_only", "trace_refund")


def respond(policy, T, P=PARAMS, wallet=0.0):
    """Return dict(hours, inflation, harm, keeps) for one policy at detection delay T hours."""
    raise NotImplementedError("TODO")


def ring_net(policy, T, A, P=PARAMS, wallet=0.0):
    """Gold the ring is ahead after the response and a ban of accounts worth A in total."""
    raise NotImplementedError("TODO")


def crossover(P=PARAMS, step=0.01, T_max=200.0):
    """First T on the grid step, 2*step, ... T_max at which the rollback's harm is greater than the
    trace's harm. None if there is none."""
    raise NotImplementedError("TODO")


def simulate(rng, T, P=PARAMS):
    """Item-by-item version of the model. For each of the D items draw its leave time with
    rng.expovariate(P["k"]); if it left before T, it was bought with probability P["b"] (use
    rng.random()), otherwise it is gone. Return dict(held, bought, gone) as counts."""
    raise NotImplementedError("TODO")


def estimate(rows, T_obs):
    """Estimate (k, b) from an incident log (see make_log.py) observed T_obs hours after the
    exploit began. Items still held were watched for T_obs hours without leaving, so
    k = (number that left) / (total hours all items were watched while still held)."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    for T in (1 / 3, 1, 3, 6, 12, 24, 48):
        print(f"T = {T:5.2f}", {pol: {k: round(v, 2) for k, v in respond(pol, T).items()} for pol in POLICIES[:3]})
    print("crossover:", crossover())
    print("simulated counts at T = 6:", simulate(random.Random(1), 6))
    from make_log import T_OBS, incident_log
    print("estimated (k, b):", estimate(incident_log(), T_OBS))
