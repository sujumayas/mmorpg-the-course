"""MMO403 Lab 07 starter: a loot box rules engine.

Standard library only. Fill in every function marked TODO, then run
    .venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab07-starter/test_lootlaw.py
from the repository root. The rules are the week 7 lecture's table, status as of
28 September 2026. They are a teaching model, not legal advice.

A Design holds the five facts from the lecture plus two compliance facts:
    paid      real money, or a currency sold for money, can buy a draw
    chance    contents are random at purchase
    transfer  "none", "trade" or "cashout"
    skill     the draw feeds a mode that is mainly a game of skill
    minors    the game is aimed at, or likely played by, under-18s
    odds_shown       odds are published before purchase
    parental_gate    under-18 purchases need a parent to enable them

Outcome codes returned by assess():
    "remove"     licence needed or prohibited (BE, NL, UK law, BR)
    "rating_M"   Australian minimum rating M
    "rating_16"  PEGI default 16
    "odds"       odds must be published by law (CN, KR)
    "voluntary"  UK industry guidance applies
    "none"       no specific rule
"""
from dataclasses import dataclass, replace
from itertools import combinations

MARKETS = ["BE", "NL", "UK", "CN", "KR", "BR", "AU", "PEGI"]
TRANSFER_LEVELS = ("none", "trade", "cashout")


@dataclass(frozen=True)
class Design:
    paid: bool
    chance: bool
    transfer: str = "none"
    skill: bool = False
    minors: bool = False
    odds_shown: bool = False
    parental_gate: bool = False


# The lecture's presets. Provided.
PRESETS = {
    "A": Design(True, True, "none", False, True),
    "B": Design(True, True, "trade", True, True),
    "C": Design(True, True, "cashout", False, False),
    "D": Design(True, True, "trade", False, True),
    "E": Design(False, True, "none", False, True),
    "F": Design(True, False, "none", False, True),
}


def assess(design, market):
    """Return the outcome code for one market (see module docstring). TODO"""
    raise NotImplementedError


def assess_all(design):
    """Return {market: outcome} for every market in MARKETS. TODO"""
    raise NotImplementedError


def must_remove(design, markets=MARKETS):
    """Sorted list (in MARKETS order) of markets in `markets` whose outcome is "remove". TODO"""
    raise NotImplementedError


def compliance(design, market):
    """Return "remove", "breach", "gap" or "ok".
    - "remove" if assess() says remove.
    - "breach" if the market legally requires odds ("odds") and odds_shown is False.
    - "gap" if the UK guidance applies ("voluntary") and either odds_shown or
      parental_gate is False.
    - "ok" otherwise (ratings count as ok: they are not a breach). TODO"""
    raise NotImplementedError


def candidate_changes(design):
    """All single-fact changes as (field, new_value) pairs, excluding no-ops.
    Fields: paid, chance, skill, minors (flip) and transfer (each other level).
    Provided."""
    out = []
    for f in ("paid", "chance", "skill", "minors"):
        out.append((f, not getattr(design, f)))
    for level in TRANSFER_LEVELS:
        if level != design.transfer:
            out.append(("transfer", level))
    return out


def fixes(design, markets=MARKETS, max_changes=2):
    """Return the smallest sets of changes that make must_remove(new, markets) empty.
    Search sets of size 0, 1, ..., max_changes and stop at the first size with any
    solution. Never combine two changes to the same field. Return a list of
    frozensets of (field, value) pairs, sorted by sorted(tuple(s)). If none work,
    return []. TODO"""
    raise NotImplementedError


def switch_off_cost(R, b, k, shares, design):
    """Return (regional, global) yearly revenue lost.
    regional = R * sum(shares[m] for m in must_remove(design)) * b * (1 - k)
    global   = R * b * (1 - k)
    `shares` maps market -> share of revenue; missing markets count as 0. TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    for name, d in PRESETS.items():
        print(name, assess_all(d))
