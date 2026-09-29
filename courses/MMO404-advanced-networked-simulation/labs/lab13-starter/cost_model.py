"""MMO404 Lab 13: what does one player-hour cost, and which lever moves it?

    python cost_model.py --check            # tests your functions against the week 13 lecture
    python cost_model.py --levers           # the lecture's lever table for the baseline
    python cost_model.py --sweep out.csv    # cost and shares for tick rates 5 to 128 Hz

Implement every function marked TODO. The model is in the week 13 lecture, sections 2 and 4.
Standard library only. All prices are invented round numbers from the lecture.
"""
import csv
import math
import sys

# Week 1 tick model, at 10 Hz with half the tick kept free.
C_P = 20e-6      # CPU seconds per player per tick
C_I = 2e-6       # CPU seconds per interacting ordered pair per tick
F = math.pi * 100 ** 2 / 2000 ** 2   # AOI fraction of a 2 km zone with R = 100 m

BASELINE = dict(h=0.1, speedup=1.0, fill=0.5, zones=8, server_price=0.40,
                bytes_per_s=6000, egress_per_gb=0.08, services=0.25, tick_hz=10)


def zone_capacity(h, speedup=1.0, tick_hz=10):
    """Week 1 capacity: largest n with c_p n + c_i n^2 g <= B, where B = 0.5 / tick_hz s
    and a speed-up s divides both constants. Given."""
    budget = 0.5 / tick_hz
    g = h * h + (1 - h * h) * F
    a, b = C_I / speedup * g, C_P / speedup
    return (-b + math.sqrt(b * b + 4 * a * budget)) / (2 * a)


def cost_terms(h=0.1, speedup=1.0, fill=0.5, zones=8, server_price=0.40,
               bytes_per_s=6000, egress_per_gb=0.08, services=0.25, tick_hz=10):
    """Dollars per 1,000 player-hours as a tuple (compute, network, services).
    compute = 1000 * P_s / (Z * N * u); network = 1000 * b * 3600 / 1e9 * P_e. TODO."""
    raise NotImplementedError


def shares(terms):
    """Each term divided by the total, as a tuple in the same order. TODO."""
    raise NotImplementedError


def lever_saving(baseline_kwargs, change):
    """Fractional saving (0.276 means 27.6%) when the keyword arguments in `change`
    replace those in `baseline_kwargs`. TODO."""
    raise NotImplementedError


def ceiling(share, factor):
    """Share rule: the saving when a term with this share gets `factor` times cheaper. TODO."""
    raise NotImplementedError


def spot_fill_limit(spot_share, reclaim_share):
    """Highest fill u at which a worst-case reclaim can still be seated: 1 - q x. TODO."""
    raise NotImplementedError


def blended_price(price, spot_share, discount=0.7):
    """Average server-hour price when a share of the fleet runs at a discount. TODO."""
    raise NotImplementedError


def check():
    t = cost_terms()
    assert abs(t[0] - 0.10667) < 1e-4, f"compute {t[0]}"
    assert abs(t[1] - 1.728) < 1e-9, f"network {t[1]}"
    assert t[2] == 0.25
    s = shares(t)
    assert abs(sum(s) - 1) < 1e-12 and abs(s[1] - 0.8288) < 1e-3, s
    table = {"speedup": (3.0, 0.024), "fill": (0.7, 0.015),
             "bytes_per_s": (4000, 0.276), "egress_per_gb": (0.06, 0.207)}
    for key, (value, want) in table.items():
        got = lever_saving(BASELINE, {key: value})
        assert abs(got - want) < 0.0015, f"{key}={value}: saving {got:.4f}, lecture says {want}"
    assert abs(ceiling(s[1], 1.5) - lever_saving(BASELINE, {"bytes_per_s": 4000})) < 1e-9, \
        "the share rule must match the direct computation for a network lever"
    crowd = cost_terms(h=0.25, bytes_per_s=12000)
    assert abs(sum(crowd) - 3.894) < 0.001, f"crowd total {sum(crowd)}"
    assert abs(spot_fill_limit(0.6, 0.25) - 0.85) < 1e-12
    assert abs(blended_price(0.40, 0.6) - 0.232) < 1e-12
    spot = cost_terms(server_price=blended_price(0.40, 0.6))
    assert abs(sum(spot) - 2.040) < 0.001, f"spot total {sum(spot)}"
    print("all checks passed")


def levers():
    base = sum(cost_terms())
    print(f"baseline total {base:.3f} $ per 1,000 player-hours")
    for key, value in (("speedup", 3.0), ("fill", 0.7), ("bytes_per_s", 4000),
                       ("egress_per_gb", 0.06)):
        print(f"{key:14s} -> {value:<7}  saves {100 * lever_saving(BASELINE, {key: value}):5.1f}%")


def sweep(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["tick_hz", "capacity", "compute", "network", "services", "compute_share"])
        for hz in (5, 10, 20, 30, 45, 60, 90, 128):
            t = cost_terms(tick_hz=hz)
            w.writerow([hz, round(zone_capacity(0.1, 1.0, hz), 1)] +
                       [round(x, 4) for x in t] + [round(shares(t)[0], 4)])
    print("wrote", path)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--levers" in sys.argv:
        levers()
    elif "--sweep" in sys.argv:
        sweep(sys.argv[sys.argv.index("--sweep") + 1])
    else:
        print(__doc__)
