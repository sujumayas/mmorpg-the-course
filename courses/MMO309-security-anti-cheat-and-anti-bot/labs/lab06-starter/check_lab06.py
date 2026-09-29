"""Checker for MMO309 Lab 06. Run:  python check_lab06.py

Part 1 checks the model against the week 6 lecture's numbers.
Part 2 checks your estimators on a tiny hand-made log and on bots.csv.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import farm as F  # noqa: E402

if not (HERE / "bots.csv").exists():
    import make_ledger
    make_ledger.main()

failures = 0
total = 0


def check(name, fn):
    global failures, total
    total += 1
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not implemented yet ({exc})"
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures += 1


def close(a, b, tol=1e-6):
    return a is not None and b is not None and abs(a - b) <= tol


TINY = [
    {"account": "a", "created_day": 0, "detected_day": 4, "banned_day": 7},
    {"account": "b", "created_day": 2, "detected_day": 3, "banned_day": 7},
    {"account": "c", "created_day": 5, "detected_day": None, "banned_day": None},
    {"account": "d", "created_day": 1, "detected_day": 9, "banned_day": None},
]


def reference_d(rows, end_day):
    det = sum(1 for r in rows if r["detected_day"] is not None)
    risk = sum((r["detected_day"] if r["detected_day"] is not None else end_day) - r["created_day"]
               for r in rows)
    return det / risk


checks = [
    ("margin with the lecture's card", lambda: (close(F.margin(20_000, 20, 1.50, 1.00), 5.0),
                                               f"{F.margin(20_000, 20, 1.50, 1.00)}")),
    ("profit d=0.1, W=0 is $15", lambda: (close(F.profit(0.1, 0), 15.0), f"{F.profit(0.1, 0)}")),
    ("profit d=1, W=14 is $5", lambda: (close(F.profit(1.0, 14), 5.0), f"{F.profit(1.0, 14)}")),
    ("profit with setup doubled is -$27.50", lambda: (close(F.profit(0.2, 7, setup=70.0), -27.5),
                                                     f"{F.profit(0.2, 7, setup=70.0)}")),
    ("break-even d at W=0 is 1/7", lambda: (close(F.breakeven_d(0), 1 / 7), f"{F.breakeven_d(0)}")),
    ("break-even d at W=7 is 1/3.5", lambda: (close(F.breakeven_d(7), 1 / 3.5), f"{F.breakeven_d(7)}")),
    ("no d is enough at W=14", lambda: (F.breakeven_d(14) is None, f"{F.breakeven_d(14)}")),
    ("negative margin: any d closes it", lambda: (F.breakeven_d(0, price=0.20) == 0.0,
                                                 f"{F.breakeven_d(0, price=0.20)}")),
    ("estimate_d on the tiny log is 3/18", lambda: (close(F.estimate_d(TINY, end_day=10), 3 / 18),
                                                   f"{F.estimate_d(TINY, end_day=10)}")),
    ("mean_wave_lag on the tiny log is 3.5", lambda: (close(F.mean_wave_lag(TINY), 3.5),
                                                     f"{F.mean_wave_lag(TINY)}")),
]


def csv_d():
    rows = F.load()
    got, want = F.estimate_d(rows), reference_d(rows, F.END_DAY)
    return close(got, want, 1e-9) and abs(got - 0.15) < 0.01, f"estimate {got:.4f} (data generated with 0.15)"


def csv_lag():
    rows = F.load()
    lag = F.mean_wave_lag(rows)
    return 3.7 < lag < 4.3, f"mean lag {lag:.3f} days (weekly waves, ban strictly after detection)"


if __name__ == "__main__":
    for name, fn in checks:
        check(name, fn)
    check("estimate_d on bots.csv", csv_d)
    check("mean_wave_lag on bots.csv", csv_lag)
    print(f"\n{total - failures} of {total} checks pass.")
    sys.exit(1 if failures else 0)
