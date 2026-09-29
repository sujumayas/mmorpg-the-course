"""MMO404 Lab 14: turn a public headline into the constraint it implies.

    python teardown.py --check                  # tests your functions against the week 14 lecture
    python teardown.py --cases                  # the lecture's table of implied pair costs
    python teardown.py --sweep FWST-8 out.csv   # sensitivity of one case to each assumption

Implement every function marked TODO. The model is in the week 14 lecture, section 2.
Standard library only. Add your own group's case to CASES before you run --sweep on it.
"""
import csv
import sys

# name: (players n, tick rate f_t in Hz, game speed d). Sources are in the week 14 lecture.
CASES = {
    "B-R5RB": (2670, 1, 0.1),
    "FWST-8": (6557, 1, 0.1),
    "Second Life region": (100, 45, 1.0),
    "Week 1 zone": (153, 10, 1.0),
}

# Default assumptions and the ranges the sensitivity sweep moves them across.
DEFAULTS = {"usable": 1.0, "pair_share": 1.0, "speed": None}   # None: use the case's own d
RANGES = {"usable": (0.3, 1.0), "pair_share": (0.1, 1.0), "speed": (0.1, 1.0)}

REFERENCE_NS = {"typical instruction": 1, "mutex lock/unlock": 25, "main-memory fetch": 100}


def implied_pair_ns(n, tick_hz, speed=1.0, usable=1.0, pair_share=1.0):
    """Upper bound on CPU ns per interacting ordered pair per tick:
    1e9 * usable / (tick_hz * speed) / (n * (n - 1) * pair_share). TODO."""
    raise NotImplementedError


def implied_player_us(n, tick_hz, speed=1.0, usable=1.0, games_per_core=1):
    """Upper bound on CPU microseconds per player per tick when the per-player term
    dominates and `games_per_core` games share one core. TODO."""
    raise NotImplementedError


def speedup_needed(current_ms, target_ms):
    """How many times faster the frame must get to meet the target. TODO."""
    raise NotImplementedError


def nearest_reference(ns):
    """Name of the REFERENCE_NS entry closest to `ns` on a log scale (compare ratios,
    not differences). TODO."""
    raise NotImplementedError


def sensitivity(case):
    """For each assumption in RANGES, the bound at the low and the high end of its range,
    with the other assumptions at DEFAULTS. Returns {name: (bound_at_low, bound_at_high)}.
    For 'speed', DEFAULTS uses the case's own d when the other two are varied. TODO."""
    raise NotImplementedError


def dominant_assumption(case):
    """The assumption whose range moves the bound by the largest factor (high/low). TODO."""
    raise NotImplementedError


def check():
    close = lambda a, b, tol: abs(a - b) <= tol
    assert close(implied_pair_ns(6557, 1, 0.1), 232.6, 0.1), implied_pair_ns(6557, 1, 0.1)
    assert close(implied_pair_ns(2670, 1, 0.1), 1403.3, 0.1)
    assert close(implied_pair_ns(6557, 1, 1.0), 23.3, 0.1)
    assert close(implied_pair_ns(100, 45, 1.0), 2244.7, 0.1)
    assert close(implied_pair_ns(6557, 1, 0.1, pair_share=0.25), 930.5, 0.1)
    assert close(implied_pair_ns(6557, 1, 0.1, usable=0.5), 116.3, 0.1)
    assert close(implied_pair_ns(1000, 20), 50.05, 0.01), "check yourself, question 1"
    assert close(implied_player_us(10, 128, usable=0.9, games_per_core=3), 234.4, 0.1), \
        "VALORANT: 7.8125 ms / 3 games, 10% kept for the OS, 10 players"
    assert close(implied_player_us(12, 64, games_per_core=4), 325.5, 0.1), "question 3"
    assert close(speedup_needed(50, 2.34), 21.37, 0.01)
    assert nearest_reference(233) == "main-memory fetch"
    assert nearest_reference(23) == "mutex lock/unlock"
    assert nearest_reference(3) == "typical instruction"
    s = sensitivity("FWST-8")
    assert set(s) == set(RANGES), s
    assert close(s["pair_share"][0], 2326.2, 0.1) and close(s["pair_share"][1], 232.6, 0.1)
    assert close(s["speed"][0], 232.6, 0.1) and close(s["speed"][1], 23.3, 0.1)
    assert close(s["usable"][0], 69.8, 0.1)
    assert dominant_assumption("FWST-8") in ("pair_share", "speed")
    assert dominant_assumption("Second Life region") in ("pair_share", "speed")
    print("all checks passed")


def cases():
    for name, (n, hz, d) in CASES.items():
        ns = implied_pair_ns(n, hz, d)
        print(f"{name:20s} n={n:5d}  <= {ns:8.1f} ns per pair per tick  (nearest: {nearest_reference(ns)})")


def sweep(name, path):
    n, hz, d = CASES[name]
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["assumption", "value", "bound_ns"])
        for key, (lo, hi) in RANGES.items():
            for k in range(11):
                v = lo + (hi - lo) * k / 10
                kw = {"speed": d, "usable": 1.0, "pair_share": 1.0}
                kw[key] = v
                w.writerow([key, round(v, 3), round(implied_pair_ns(n, hz, **kw), 2)])
    print("wrote", path, "- dominant assumption:", dominant_assumption(name))


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--cases" in sys.argv:
        cases()
    elif "--sweep" in sys.argv:
        i = sys.argv.index("--sweep")
        sweep(sys.argv[i + 1], sys.argv[i + 2])
    else:
        print(__doc__)
