"""MMO307 Lab 12: alternative advancement schedules.

A design is a cost schedule (hours for each point) plus a value rule (power
from n points). `evaluate` plays a light and a heavy player through three
years and reports the numbers the lab's targets are written in.

    python3 aa_schedules.py            # evaluates the three lecture designs
    python3 test_aa_schedules.py

Standard library only.
"""
import math

WEEKS = 156            # three years
LIGHT, HEAVY = 5, 20   # post-cap hours per week


def cost_of_point(n, schedule, p):
    """Hours needed to earn point number n (n = 1, 2, ...).

    schedule "flat":      p["cost"]
    schedule "linear":    p["step"] * n
    schedule "geometric": p["first"] * p["ratio"] ** (n - 1)
    """
    # TODO: implement (see lab sheet).
    raise NotImplementedError("cost_of_point")


def points_after(hours, schedule, p):
    """Largest n such that points 1..n together cost at most `hours`."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("points_after")


def power(n, value, p):
    """Power multiplier from n points.

    value "constant": 1 + p["v"] * n
    value "decaying": 1 + p["v0"] * (1 - p["d"] ** n) / (1 - p["d"])
                      (point k is worth v0 * d ** (k - 1))
    value "capped":   1 + p["v"] * min(n, p["cap"])
    """
    # TODO: implement (see lab sheet).
    raise NotImplementedError("power")


def evaluate(design, light=LIGHT, heavy=HEAVY, weeks=WEEKS):
    """design = {"schedule": ..., "cost": {...}, "value": ..., "power": {...}}.
    Returns the metrics used by the lab's targets."""
    s, cp, v, vp = design["schedule"], design["cost"], design["value"], design["power"]
    ratios, heavy_pts = [], []
    for w in range(1, weeks + 1):
        nl = points_after(light * w, s, cp)
        nh = points_after(heavy * w, s, cp)
        heavy_pts.append(nh)
        ratios.append(power(nh, v, vp) / power(nl, v, vp))
    gained = heavy_pts[weeks - 1] - heavy_pts[weeks - 53]
    return {
        "ratio_final": ratios[-1],
        "ratio_max": max(ratios),
        "light_points_week10": points_after(light * 10, s, cp),
        "heavy_weeks_per_point_year3": 52 / gained if gained else math.inf,
    }


LECTURE_DESIGNS = {
    "flat": {"schedule": "flat", "cost": {"cost": 10},
             "value": "constant", "power": {"v": 0.01}},
    "linear": {"schedule": "linear", "cost": {"step": 2},
               "value": "constant", "power": {"v": 0.01}},
    "geometric": {"schedule": "geometric", "cost": {"first": 2, "ratio": 1.05},
                  "value": "constant", "power": {"v": 0.01}},
}


def main():
    print("design      final G   max G   light pts wk10   heavy weeks/point yr3")
    for name, d in LECTURE_DESIGNS.items():
        try:
            m = evaluate(d)
        except NotImplementedError as e:
            print("TODO:", e)
            return
        print(f"{name:10} {m['ratio_final']:7.3f} {m['ratio_max']:7.3f} "
              f"{m['light_points_week10']:13d} {m['heavy_weeks_per_point_year3']:17.2f}")


if __name__ == "__main__":
    main()
