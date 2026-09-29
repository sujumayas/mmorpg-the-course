"""MMO406 Lab 12: transmedia reach calculator (complete tool, no code to write).

Run:       .venv/bin/python transmedia.py thornmere_transmedia.json
Self-test: .venv/bin/python transmedia.py --selftest

Model (week 12 lecture, section 2), for media with reach s_i:
    C = product of s_i over media the story REQUIRES     (AND)
    X = 1 - product of (1 - s_i) over OPTIONAL media     (OR)
    n = sum of s_i                                        (pieces per player)
    Frechet bounds, whatever the overlap between audiences:
        max(0, sum(s) - (k - 1)) <= C <= min(s)
        max(s) <= X <= min(1, sum(s))

A medium is REQUIRED when at least one beat comes from it and has no retell
line in the game ("retell": null). Otherwise it is optional.
"""
import json
import sys
from math import prod


def shares(reaches_required, reaches_optional):
    req, opt = list(reaches_required), list(reaches_optional)
    C = prod(req) if req else 1.0
    X = 1 - prod(1 - s for s in opt) if opt else 0.0
    C_lo = max(0.0, sum(req) - (len(req) - 1)) if req else 1.0
    C_hi = min(req) if req else 1.0
    X_lo = max(opt) if opt else 0.0
    X_hi = min(1.0, sum(opt)) if opt else 0.0
    return {"C": C, "X": X, "n": sum(req) + sum(opt),
            "C_bounds": (C_lo, C_hi), "X_bounds": (X_lo, X_hi)}


def audit(plan):
    media = {m["id"]: m for m in plan["media"]}
    for m in plan["media"]:
        if not 0 <= m["reach"] <= 1:
            raise ValueError(f"reach of {m['id']} must be between 0 and 1")
    required, missing = set(), []
    for b in plan["beats"]:
        if b["source"] not in media:
            raise ValueError(f"beat '{b['beat']}' cites unknown medium {b['source']}")
        if not b.get("retell"):
            required.add(b["source"])
            missing.append(b)
    req = [media[i]["reach"] for i in sorted(required)]
    opt = [m["reach"] for m in plan["media"] if m["id"] not in required]
    return required, missing, shares(req, opt)


def report(plan):
    required, missing, r = audit(plan)
    print(f"{plan.get('world', 'plan')}: {plan.get('release', '')}")
    print(f"{'medium':<8} {'reach':>6}  role      tier     timing")
    for m in plan["media"]:
        role = "REQUIRED" if m["id"] in required else "optional"
        print(f"{m['id']:<8} {m['reach']:>6.0%}  {role:<8}  {m.get('tier', '?'):<7}  {m.get('timing', '?')}")
    print("\nBeats with no retell line (they make their medium required):")
    for b in missing or [{"beat": "none", "source": "-"}]:
        print(f"  - {b['beat']}  [{b['source']}]")
    lo, hi = r["C_bounds"]
    elo, ehi = r["X_bounds"]
    print(f"\nPieces per player n       = {r['n']:.2f}")
    print(f"Can follow the story C    = {r['C']:.1%}   (any overlap: {lo:.1%} to {hi:.1%})")
    print(f"Got something extra X     = {r['X']:.1%}   (any overlap: {elo:.1%} to {ehi:.1%})")
    print("\nTarget: C = 100% (every required beat retold in the game).")


def selftest():
    close = lambda a, b: abs(a - b) < 1e-9
    r = shares([], [0.60, 0.30, 0.15])
    assert close(r["X"], 0.762) and close(r["n"], 1.05) and r["C"] == 1.0
    r = shares([0.60, 0.30, 0.15], [])
    assert close(r["C"], 0.027) and close(r["C_bounds"][1], 0.15) and r["C_bounds"][0] == 0
    r = shares([], [0.60, 0.30, 0.15, 0.35])
    assert close(r["X"], 1 - 0.40 * 0.70 * 0.85 * 0.65)
    r = shares([0.12, 0.25, 0.70], [0.55])
    assert close(r["C"], 0.021) and close(r["X"], 0.55) and close(r["n"], 1.62)
    print("Self-test passed: lecture values reproduced.")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    path = sys.argv[1] if len(sys.argv) > 1 else "thornmere_transmedia.json"
    with open(path) as f:
        report(json.load(f))
