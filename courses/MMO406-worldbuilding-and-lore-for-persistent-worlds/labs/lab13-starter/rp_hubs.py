"""MMO406 Lab 13: roleplay hubs.

Run:   .venv/bin/python rp_hubs.py dikeholm_rp.json
Tests: .venv/bin/python test_rp_hubs.py   (or pytest)

Model (week 13 lecture, section 2):
    lam      = Lam / H                       mean crowd at one hub
    P_k(lam) = 1 - sum_{j<k} e^-lam lam^j / j!   chance a hub has at least k
    V        = H * P_k(lam)                  expected live hubs
    S        = P_{k-1}(lam)                  share of roleplayers in a live hub

A day file (see dikeholm_rp.json) holds "hourly": 24 counts of roleplayers
looking for a scene (hour 0 = midnight), "k": the minimum cast, and
"target_share": the smallest acceptable day-wide share in a scene.
"""
import json
import math
import sys


def p_at_least(lam, k):
    """Chance that a Poisson count with mean lam is at least k (1.0 if k <= 0)."""
    raise NotImplementedError("p_at_least")


def viable_hubs(Lam, H, k):
    """Expected number of live hubs, V = H * P_k(Lam / H)."""
    raise NotImplementedError("viable_hubs")


def scene_share(Lam, H, k):
    """Share of roleplayers standing in a live hub, S = P_{k-1}(Lam / H)."""
    raise NotImplementedError("scene_share")


def best_hubs(Lam, k, h_max=60):
    """The H in 1..h_max with the largest V (ties go to the smaller H)."""
    raise NotImplementedError("best_hubs")


def day_plan(hourly, k, H, fallback_below=None):
    """Evaluate a plan that opens H hubs every hour, except that in hours
    with fewer than fallback_below roleplayers everyone uses one hub.

    Return {"live_hub_hours": sum over hours of V,
            "share": roleplayer-weighted mean of S over the day,
            "worst_hour": (hour, S) for the hour with the lowest S
                          among hours with at least one roleplayer,
                          earliest hour on ties}.
    Hours with zero roleplayers add nothing and are skipped.
    """
    raise NotImplementedError("day_plan")


def choose_plan(hourly, k, target_share, h_max=12, fallback_below=None):
    """Among H in 1..h_max, return the H whose day_plan has the most
    live_hub_hours while its share is at least target_share. Ties go to the
    smaller H. Return None if no H meets the target."""
    raise NotImplementedError("choose_plan")


def report(data):
    hourly, k, target = data["hourly"], data["k"], data["target_share"]
    peak = max(hourly)
    print(f"{data.get('city', 'city')}: k = {k}, peak {peak} roleplayers, target share {target:.0%}")
    print(f"Best hubs at peak: {best_hubs(peak, k)}")
    for fb in (None, data.get("fallback_below")):
        label = "no fallback" if fb is None else f"one hub below {fb}"
        print(f"\nPlans ({label}):")
        for H in range(1, 9):
            p = day_plan(hourly, k, H, fb)
            print(f"  H={H}  live hub-hours {p['live_hub_hours']:6.2f}  share {p['share']:6.1%}"
                  f"  worst hour {p['worst_hour'][0]:02d}:00 at {p['worst_hour'][1]:.1%}")
        print(f"  chosen: H = {choose_plan(hourly, k, target, fallback_below=fb)}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "dikeholm_rp.json"
    with open(path) as f:
        data = json.load(f)
    try:
        report(data)
    except NotImplementedError as e:
        print(f"TODO: implement {e}")
        sys.exit(1)
