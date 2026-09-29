"""GD202 Lab 13: phase budget for a zone.

Run:   python phasing.py saltmarsh.json
Tests: python test_phasing.py   (or pytest test_phasing.py)

Model (lecture section 2):
    V        = sum of p_i squared      chance a random other player shares your phase
    visible  = (N - 1) * V             expected other players you can see
    n_eff    = 1 / V                   effective number of phases

A zone file has a quest chain and a funnel.
- chain[k]["sets_phase"] is null (no world change), a string (one flag), or
  a dict {flag: fraction} for a choice that splits players between flags.
- funnel[k] is the share of the zone's players currently standing at position k,
  for k = 0 .. len(chain). A player at position k has completed steps 0 .. k-1.
  Position len(chain) means "finished the chain, still in the zone".
- A player's phase is the tuple of flags from the steps they completed, in order.
  Name it by joining the flags with "+", or "base" when there are none.
"""
import json
import sys

TOL = 1e-9


def visible_share(shares):
    """Return V = sum of p_i^2. `shares` is a list of floats or a dict name -> float."""
    raise NotImplementedError("visible_share")


def expected_visible(shares, population):
    """Expected number of OTHER players you can see: (population - 1) * V."""
    raise NotImplementedError("expected_visible")


def effective_phases(shares):
    """1 / V."""
    raise NotImplementedError("effective_phases")


def per_phase_visible(shares, population):
    """Dict phase -> expected other players seen by someone standing in that phase.
    A player in phase i sees about p_i * (population - 1) others."""
    raise NotImplementedError("per_phase_visible")


def phase_shares(chain, funnel):
    """Return dict phase_name -> share of the zone population.

    Raise ValueError if len(funnel) != len(chain) + 1, if any funnel value is
    negative, if the funnel does not sum to 1 (within TOL), or if a choice's
    fractions do not sum to 1 (within TOL).
    Drop phases whose share is exactly 0.
    """
    raise NotImplementedError("phase_shares")


def report(zone):
    shares = phase_shares(zone["chain"], zone["funnel"])
    n = zone["population"]
    print(f"Zone {zone['zone']}: {n} players, {len(shares)} phases")
    for name, p in sorted(shares.items(), key=lambda kv: -kv[1]):
        print(f"  {name:32s} share {p:.3f}  sees {p * (n - 1):5.1f} others")
    print(f"  V = {visible_share(shares):.4f}")
    print(f"  expected visible others = {expected_visible(shares, n):.2f}")
    print(f"  effective phases = {effective_phases(shares):.2f}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "saltmarsh.json"
    with open(path) as f:
        zone = json.load(f)
    try:
        report(zone)
    except NotImplementedError as e:
        print(f"TODO: implement {e} in phasing.py")
