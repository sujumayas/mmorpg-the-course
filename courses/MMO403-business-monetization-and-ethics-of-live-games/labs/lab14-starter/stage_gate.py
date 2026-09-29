"""MMO403 Lab 14 starter: staged funding, the go/no-go gate and dilution.
Standard-library Python 3.10 or later.

Fill in every function marked TODO, then run the tests from this folder:

    python3 test_stage_gate.py        (or: pytest test_stage_gate.py)

The model is the one from the week 14 lecture, section 2. Money is in $ millions.

    p  = probability the game is a hit (worth V); otherwise it is worth 0
    C1 = stage-1 cost (prototype, vertical slice or soft launch)
    C2 = stage-2 cost (full production and launch), paid only after a "go"
    s  = P(go | hit), f = P(go | miss)

    EV_all  = p V - C1 - C2
    EV_gate = -C1 + max(0, p s (V - C2) - (1 - p) f C2)
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_options(path=os.path.join(HERE, "stage1_options.csv")):
    """Return a list of dicts: {"design": str, "c1": float, "s": float, "f": float}."""
    with open(path, newline="") as fh:
        return [{"design": r["design"], "c1": float(r["c1"]), "s": float(r["s"]),
                 "f": float(r["f"])} for r in csv.DictReader(fh)]


# ---------------------------------------------------------------- TODO

def ev_all_in(p, V, C1, C2):
    """Expected value of funding both stages up front."""
    raise NotImplementedError("ev_all_in")


def ev_gated(p, V, C1, C2, s, f):
    """Expected value with a gate after stage 1. Never continue at a loss."""
    raise NotImplementedError("ev_gated")


def kill_rate(p, s, f):
    """Share of projects stopped after stage 1: 1 - (p s + (1 - p) f)."""
    raise NotImplementedError("kill_rate")


def posterior_hit(p, s, f):
    """P(hit | go) by Bayes' rule. Return None if a 'go' is impossible."""
    raise NotImplementedError("posterior_hit")


def breakeven_f(p, V, C1, C2, s):
    """Largest false-go rate at which the gated plan is still worth >= 0:
    f* = (p s (V - C2) - C1) / ((1 - p) C2), clamped to [0, 1]."""
    raise NotImplementedError("breakeven_f")


def best_stage1(options, p, V, C2):
    """Return (design, ev) of the stage-1 option with the highest gated EV."""
    raise NotImplementedError("best_stage1")


def post_money(investment, share):
    """Post-money valuation when `investment` buys `share` of the company."""
    raise NotImplementedError("post_money")


def pre_money(investment, share):
    """Pre-money valuation: post-money minus the investment."""
    raise NotImplementedError("pre_money")


def founder_share(shares_sold):
    """Founders' ownership after rounds that each sell the given share of the
    company as it stands (for example [0.25, 0.25] -> 0.5625)."""
    raise NotImplementedError("founder_share")


if __name__ == "__main__":
    print("all in:", ev_all_in(0.25, 60, 2, 18))
    print("gated: ", ev_gated(0.25, 60, 2, 18, 0.8, 0.2))
