"""MMO406 Lab 11: a continuity checker.

Run:   .venv/bin/python continuity.py thornmere_canon.json
Tests: .venv/bin/python test_continuity.py   (or pytest)

Model (week 11 lecture, sections 2 to 4):
    Desc(x)   = every fact reachable from x by following "is depended on by" arrows
    Review(x) = {x} plus Desc(x)
    radius(x) = |Desc(x)|
    W(x)      = sum of cost over non-frozen facts in Review(x)
    F(x)      = frozen facts in Review(x), sorted by id
    P(contradiction) = 1 - (1 - eps)**k

A canon file (see thornmere_canon.json) holds a list of tiers, highest first,
and a list of facts. Each fact has id, text, depends_on (ids it relies on),
cost (writer-days), frozen (true/false), tier, and asserts (a dict of
key -> value that the fact states, for example {"drowning_year": 912}).

`canon` in the functions below is that list of fact dicts.
"""
import json
import sys


def descendants(canon, fid):
    """Return the set of ids that depend on fid, directly or indirectly.
    Must terminate even if the graph has a cycle. Ignore unknown ids in
    depends_on (validate reports them)."""
    raise NotImplementedError("descendants")


def blast(canon, fid):
    """Return {"radius": int, "cost": float, "frozen": sorted list of ids}."""
    raise NotImplementedError("blast")


def validate(canon):
    """Return a sorted list of (id, code) problems:
    ("T1", "UNKNOWN_DEP") for each fact that depends on an id not in canon
    (one entry per missing id), and (id, "CYCLE") for every fact that lies
    on a dependency cycle (a fact that is its own descendant)."""
    raise NotImplementedError("validate")


def resolve(canon, tiers):
    """Resolve asserted values by tier precedence (tiers[0] is highest).

    For each key, look at the facts that assert it. Take the highest tier
    among them. If all facts at that tier agree, the key resolves to that
    value, and every lower-tier fact asserting a different value is
    overridden. If facts at the top tier disagree, the key is unresolved
    (it gets no value and nothing is marked overridden for it).

    Return {"values": {key: value}, "overridden": sorted list of (id, key),
            "unresolved": sorted list of keys}.
    Raise ValueError if a fact's tier is not in tiers.
    """
    raise NotImplementedError("resolve")


def contradiction_chance(eps, k):
    """Chance that content touching k facts, each wrong with probability eps,
    contradicts canon at least once."""
    raise NotImplementedError("contradiction_chance")


def report(data):
    canon, tiers = data["facts"], data["tiers"]
    print(f"{data.get('world', 'canon')}: {len(canon)} facts")
    print("\nProblems:")
    for fid, code in validate(canon) or [("-", "none")]:
        print(f"  {fid:<4} {code}")
    print("\nBlast radius:")
    for f in canon:
        b = blast(canon, f["id"])
        print(f"  {f['id']:<4} radius {b['radius']:>2}  cost {b['cost']:>5}  frozen {b['frozen']}")
    r = resolve(canon, tiers)
    print("\nResolved values:", r["values"])
    print("Overridden:", r["overridden"])
    print("Unresolved:", r["unresolved"])


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "thornmere_canon.json"
    with open(path) as f:
        data = json.load(f)
    try:
        report(data)
    except NotImplementedError as e:
        print(f"TODO: implement {e}")
        sys.exit(1)
