"""MMO403 Lab 05 checker. Run after gen_owners.py:  python check_lab05.py"""
import sys

import battlepass as b


def close(a, b_, tol=1e-6):
    return abs(a - b_) <= tol


def t_stats():
    r = b.stats_from_distribution(b.tier_distribution(40, 40, 0.7))
    f = b.stats_from_distribution(b.tier_distribution(40, 40, 0.7), placement="final")
    return (close(r["finish"], 0.5) and close(r["mean_tier"], 80.6633, 1e-3)
            and close(r["near_miss"], 0.059821, 1e-5)
            and close(r["tier_revenue"], 15014.56, 0.05)
            and close(r["rebate_back"], 1209.95, 0.05)
            and close(f["rebate_back"], 750.0, 1e-6))


TESTS = {
    "share_playing_at_least": lambda: close(b.share_playing_at_least(40, 40, 0.7), 0.5)
        and close(b.share_playing_at_least(60, 40, 0.7), 0.281215, 1e-5)
        and b.share_playing_at_least(0, 40, 0.7) == 1.0,
    "tier_reached": lambda: b.tier_reached(30, 50) == 60 and b.tier_reached(80, 50) == 100
        and b.tier_reached(49.9, 50) == 99,
    "tier_distribution": lambda: (lambda d: len(d) == 101 and close(sum(d), 1.0, 1e-9)
        and close(d[100], 0.5))(b.tier_distribution(40, 40, 0.7)),
    "stats_from_distribution": t_stats,
    "empirical_distribution": lambda: (lambda r: close(r["finish"], 0.3534, 1e-6)
        and close(r["mean_tier"], 69.0604, 1e-6) and close(r["tier_revenue"], 13050.0, 1e-3))(
        b.stats_from_distribution(b.empirical_distribution(b.load_hours(), 50))),
    "fit_lognormal": lambda: all(close(x, y, 1e-6) for x, y in
        zip(b.fit_lognormal(b.load_hours()), (34.906561, 0.916760))),
    "best_h_star": lambda: b.best_h_star(40, 0.7) == 43
        and b.best_h_star(34.906561, 0.916760) == 37,
}


def main():
    ok = True
    for name, test in TESTS.items():
        try:
            passed = bool(test())
        except NotImplementedError:
            print(f"TODO {name}")
            ok = False
            continue
        except Exception as ex:
            print(f"FAIL {name}: {type(ex).__name__}: {ex}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
