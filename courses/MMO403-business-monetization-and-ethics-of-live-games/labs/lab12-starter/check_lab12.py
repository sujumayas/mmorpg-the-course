"""MMO403 Lab 12 checker:  python check_lab12.py

Prints PASS, FAIL or TODO for each function. Values are checked to 1e-9 (relative).
"""
import sys

import fees as f

TOL = 1e-9
STEAM = [[0, 0.30], [10_000_000, 0.25], [50_000_000, 0.20]]


def close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(b))


def waterfall_ok():
    schedules, rows = f.load()
    s = rows[0]
    w = f.waterfall(s["spend"], s["purchases"], s["eligible"], schedules["steam"], 0.10, 0.04)
    a = rows[2]
    wa = f.waterfall(a["spend"], a["purchases"], a["eligible"], schedules["apple_sbp"], 0.10, 0.04)
    return (close(w["tax"], 1_200_000) and close(w["refunds"], 480_000) and close(w["net"], 11_520_000)
            and close(w["fee"], 3_380_000) and close(w["payout"], 8_140_000)
            and close(wa["fee"], 282_000))


TESTS = {
    "bracket_take": lambda: close(f.bracket_take(30_000_000, STEAM), 8_000_000)
        and close(f.bracket_take(100_000_000, STEAM), 23_000_000)
        and close(f.bracket_take(5_000_000, [[0, 0.0], [1_000_000, 0.12]]), 480_000)
        and f.bracket_take(0, STEAM) == 0,
    "status_take": lambda: close(f.status_take(3_000_000, True, 0.15, 0.30, 1_000_000), 750_000)
        and close(f.status_take(3_000_000, False, 0.15, 0.30, 1_000_000), 900_000)
        and close(f.status_take(800_000, True, 0.15, 0.30, 1_000_000), 120_000),
    "card_fees": lambda: close(f.card_fees(19.99, 1, 0.029, 0.30), 0.87971)
        and close(f.card_fees(960_000, 55_000, 0.029, 0.30), 44_340),
    "tax_from_inclusive": lambda: close(f.tax_from_inclusive(24.0, 0.20), 4.0),
    "channel_take": lambda: close(f.channel_take(2_304_000, 0, False, {"kind": "bracket",
        "brackets": [[0, 0.0], [1_000_000, 0.12]]}), 156_480)
        and close(f.channel_take(100.0, 10, False, {"kind": "card", "pct": 0.029, "fixed": 0.30}), 5.9),
    "publisher_split": lambda: all(close(x, y) for x, y in zip(
        f.publisher_split(6_720_000, 0.5, 3_000_000, "studio"), (360_000, 6_360_000)))
        and all(close(x, y) for x, y in zip(
        f.publisher_split(6_720_000, 0.5, 3_000_000, "all"), (1_860_000, 4_860_000)))
        and f.publisher_split(1_000_000, 0.5, 3_000_000, "studio")[0] == 0,
    "waterfall": waterfall_ok,
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
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
