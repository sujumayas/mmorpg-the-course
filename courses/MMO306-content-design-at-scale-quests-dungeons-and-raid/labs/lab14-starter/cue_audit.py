"""MMO306 Lab 14 starter: a cue-table accessibility audit. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_cue_audit.py

Notation follows the week 14 lecture.
    fight     {mechanic name: {"channels": set of channels, "essential": bool}}
    profiles  {profile name: {"share": w, "reads": set of channels}}
    E         share of players shut out of at least one (essential) mechanic
    G         share of random N-player groups with at least one shut-out member
"""
import itertools
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNELS = ("colour", "shape", "icon", "text", "sound")
SENSE = {"colour": "vision", "shape": "vision", "icon": "vision", "text": "vision",
         "sound": "hearing", "haptic": "touch"}


def load(path=os.path.join(HERE, "encounters.json")):
    """Return (profiles, costs, bosses) with channel lists turned into sets."""
    with open(path) as f:
        data = json.load(f)
    profiles = {k: {"share": v["share"], "reads": set(v["reads"])}
                for k, v in data["profiles"].items()}
    bosses = {b: {m: {"channels": set(v["channels"]), "essential": v["essential"]}
                  for m, v in mechs.items()}
              for b, mechs in data["bosses"].items()}
    return profiles, data["channel_cost_days"], bosses


def shut_out_of(channels, profiles):
    """TODO step 1. Set of profile names that can read none of `channels`."""
    raise NotImplementedError("shut_out_of() is yours to write")


def fight_shut_out(fight, profiles, essential_only=True):
    """TODO step 1. E: the summed share of profiles shut out of at least one mechanic.
    With essential_only, ignore mechanics whose "essential" flag is False."""
    raise NotImplementedError("fight_shut_out() is yours to write")


def blocked_groups(E, N):
    """TODO step 1. G = 1 - (1 - E) ** N."""
    raise NotImplementedError("blocked_groups() is yours to write")


def spans_two_senses(channels):
    """TODO step 2. True if the channels cover at least two senses, where touch
    (haptic) does not count toward the two (XAG 103: haptics never the only extra)."""
    raise NotImplementedError("spans_two_senses() is yours to write")


def cheapest_fix(channels, profiles, costs, require_two_senses=False):
    """TODO step 3. The cheapest set of channels to ADD to one mechanic so that no
    profile is shut out (and, if required, the result spans two senses).
    Search every subset of the CHANNELS not already present. Among subsets that
    work, pick the lowest total cost, then the fewest channels, then the
    alphabetically first sorted tuple. Return (cost, sorted tuple of added channels).
    A mechanic that already passes returns (0, ())."""
    raise NotImplementedError("cheapest_fix() is yours to write")


def audit(fight, profiles, costs, require_two_senses=False):
    """TODO step 4. Fix every essential mechanic with cheapest_fix.
    Return (total cost, {mechanic: added tuple}) listing only mechanics that needed a fix."""
    raise NotImplementedError("audit() is yours to write")


if __name__ == "__main__":
    profiles, costs, bosses = load()
    for boss, fight in bosses.items():
        E = fight_shut_out(fight, profiles)
        print(f"{boss:13s} E={E:5.1%}  G(5)={blocked_groups(E, 5):5.1%}  "
              f"G(20)={blocked_groups(E, 20):5.1%}")
        print("   cheapest fix:", audit(fight, profiles, costs))
        print("   two senses:  ", audit(fight, profiles, costs, require_two_senses=True))
