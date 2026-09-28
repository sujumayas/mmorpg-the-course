"""MMO303 Lab 08 starter: diminishing-returns engine and chain planner.
Standard library only. Fill in the TODOs, then run `python3 test_cc_planner.py`
(or pytest).

A chain is a list of casts, each a dict:
    {"time": 0.0, "ability": "Shield Bash", "category": "stun", "base": 5.0}
A rule is a dict:
    {"m": (1, 0.5, 0.25, 0), "R": 18}   # rule A, the WoW era from the lecture
    {"m": (1, 0.5, 0), "R": 16}         # rule B
    {"m": None, "R": None}              # rule C, no DR
"""

RULE_A = {"m": (1, 0.5, 0.25, 0), "R": 18}
RULE_B = {"m": (1, 0.5, 0), "R": 16}
RULE_C = {"m": None, "R": None}

ABILITIES = {
    # name: (owner, category, base duration s, cooldown s). Invented for this lab.
    "Shield Bash": ("Warden", "stun", 5, 30),
    "Hamstring Net": ("Warden", "root", 6, 20),
    "Hex": ("Oracle", "incapacitate", 8, 45),
    "Thunderclap": ("Oracle", "stun", 3, 20),
    "Hush": ("Oracle", "silence", 4, 25),
}


def simulate(chain, rule):
    """TODO step 1. Apply DR to a chain and return a list of applied effects,
    one per cast, in time order:
        {"ability", "category", "start", "end", "multiplier"}
    Each category keeps its own step counter. The counter resets to step 1
    when a cast lands more than R seconds after the previous effect in that
    category ended. Past the end of the multiplier list the multiplier is 0
    (immune). An effect starts at its cast time.
    """
    raise NotImplementedError("simulate is yours to write")


def total_control(effects, categories=None):
    """Seconds of control in the applied effects, optionally only some categories.
    Overlapping effects are not merged here; plan chains so they do not overlap."""
    return sum(e["end"] - e["start"] for e in effects
               if categories is None or e["category"] in categories)


def back_to_back(bases, category="stun", start=0.0, gap=0.0, rule=RULE_A):
    """Build a chain where each cast lands `gap` seconds after the previous
    effect ends. Useful for the lecture checks. Needs a working simulate()."""
    chain, t = [], start
    for i, d in enumerate(bases):
        chain.append({"time": t, "ability": f"cast{i + 1}", "category": category, "base": d})
        applied = simulate(chain, rule)[-1]
        t = applied["end"] + gap
    return chain


def uptime_ceiling(d, rule):
    """TODO step 4. The lecture's ceiling for one category: sum(m) x d / (sum(m) x d + R)."""
    raise NotImplementedError("uptime_ceiling is yours to write")
