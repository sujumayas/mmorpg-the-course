"""MMO403 Lab 08 starter: the friction-for-sale model and asymmetric friction.

Standard library only. Fill in every function marked TODO, then run
    .venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab08-starter/test_friction.py
from the repository root. Formulas are the week 8 lecture's, sections 2 and 3.

Parameters travel in a dict with keys A0, n, s, m, a, r0, d, b (see DEFAULTS).
Waits w are in hours; lifetimes in months; money in dollars.
"""

DEFAULTS = {"A0": 0.50, "n": 20, "s": 1.00, "m": 0.10, "a": 2.0,
            "r0": 0.90, "d": 0.20, "b": 8.0}


def pay(w, p=DEFAULTS):
    """Share of wall encounters where the player pays: m * w / (w + a). TODO"""
    raise NotImplementedError


def retention(w, p=DEFAULTS):
    """Monthly retention: r0 - d * w / (w + b). TODO"""
    raise NotImplementedError


def arpu(w, p=DEFAULTS):
    """Monthly ARPU: A0 + n * s * pay(w). TODO"""
    raise NotImplementedError


def lifetime(w, p=DEFAULTS):
    """Expected lifetime in months: 1 / (1 - retention(w)). TODO"""
    raise NotImplementedError


def ltv(w, p=DEFAULTS):
    """Lifetime value: arpu(w) * lifetime(w). TODO"""
    raise NotImplementedError


def best_wait(p=DEFAULTS, step=0.01, wmax=48.0):
    """Return (w_star, ltv_star) maximizing ltv on the grid 0, step, 2*step, ..., wmax.
    Use integer grid indices, not repeated float addition. TODO"""
    raise NotImplementedError


def lifetime_lost(p=DEFAULTS):
    """Share of lifetime lost at the LTV peak: 1 - lifetime(w_star) / lifetime(0). TODO"""
    raise NotImplementedError


def completion(c, k):
    """Share finishing a k-step flow when each step keeps a share c: c ** k. TODO"""
    raise NotImplementedError


def asymmetry(c, k_buy, k_undo):
    """Buy completion divided by undo completion. TODO"""
    raise NotImplementedError


def accidental(visits, error_rate, catch_rate):
    """Expected accidental purchases: visits * error_rate * (1 - catch_rate).
    With no confirmation step, catch_rate is 0. TODO"""
    raise NotImplementedError


def sweep(name, values, p=DEFAULTS):
    """For each value of parameter `name`, return (value, w_star, ltv_star,
    lifetime at w_star). Provided once best_wait and lifetime work."""
    rows = []
    for v in values:
        q = dict(p)
        q[name] = v
        w, best = best_wait(q)
        rows.append((v, w, best, lifetime(w, q)))
    return rows


if __name__ == "__main__":
    for w in [0, 1, 2, 3.5, 6, 12, 24]:
        print(w, round(ltv(w), 2), round(lifetime(w), 2))
    print(best_wait())
