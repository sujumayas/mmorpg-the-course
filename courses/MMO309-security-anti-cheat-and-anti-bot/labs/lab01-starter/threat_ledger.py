"""MMO309 Lab 01: the threat ledger.

    python threat_ledger.py --check                    # test your functions against the lecture
    python threat_ledger.py --table                    # print both rankings and the control table
    python threat_ledger.py --table --threats my_threats.csv --controls my_controls.csv

The model is the week 1 lecture, section 2. Standard library only.

    ALE = f * I                      expected annual loss of one threat
    net = r * ALE - B - P            first-year net value of one control

threats.csv columns:  id, name, stride, f, I, I_low, I_high
controls.csv columns: id, name, threat, r, B, P
"""
import argparse
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_csv(path):
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        for key, value in row.items():
            try:
                row[key] = float(value)
            except (TypeError, ValueError):
                pass
    return rows


# ------------------------------------------------------------------ your code

def ale(threat, cost_key="I"):
    """Expected annual loss of one threat row: f times the cost in column cost_key.
    cost_key is "I" normally, or "I_low" / "I_high" for the range estimates. TODO."""
    raise NotImplementedError


def rank(threats, key):
    """Return the threat IDs sorted from largest to smallest by key(threat).
    Break ties by ID in ascending order, so the result never depends on input order.
    Example: rank(threats, lambda t: t["f"]) is the ticket-queue order. TODO."""
    raise NotImplementedError


def net_value(control, threats_by_id):
    """First-year net value of one control: r * ALE(its threat) - B - P. TODO."""
    raise NotImplementedError


def stable_top(threats, n):
    """The IDs that are in the top n by ALE under the low cost estimate AND under the
    high cost estimate, returned as a sorted list. These are the threats you can stop
    arguing about. TODO."""
    raise NotImplementedError


# ------------------------------------------------------------------ checks and report

def check():
    threats = load_csv(HERE / "threats.csv")
    controls = load_csv(HERE / "controls.csv")
    by_id = {t["id"]: t for t in threats}
    tests = [
        ("ALE of T7", lambda: round(ale(by_id["T7"])), 80_000),
        ("total ALE", lambda: round(sum(ale(t) for t in threats)), 792_000),
        ("ticket-queue order", lambda: rank(threats, lambda t: t["f"]),
         ["T5", "T4", "T3", "T8", "T1", "T6", "T2", "T7"]),
        ("loss-ledger order", lambda: rank(threats, ale),
         ["T2", "T5", "T6", "T7", "T1", "T4", "T8", "T3"]),
        ("net of each control", lambda: [round(net_value(c, by_id)) for c in controls],
         [210_000, -24_080, -394_000, 4_000, 40_000]),
        ("tie broken by ID", lambda: rank([{"id": "T9", "v": 1}, {"id": "T2", "v": 1}], lambda t: t["v"]),
         ["T2", "T9"]),
        ("stable top 3", lambda: stable_top(threats, 3), ["T2", "T5"]),
    ]
    failed = 0
    for name, fn, expected in tests:
        try:
            got = fn()
        except NotImplementedError:
            got = "not implemented yet"
        if got != expected:
            failed += 1
            print(f"FAIL {name}: expected {expected}, got {got}")
        else:
            print(f"ok   {name}")
    print("all checks passed" if not failed else f"{failed} check(s) failed")
    return failed == 0


def table(threat_path, control_path):
    threats = load_csv(threat_path)
    controls = load_csv(control_path)
    by_id = {t["id"]: t for t in threats}
    print("Ticket queue:", " ".join(rank(threats, lambda t: t["f"])))
    print("Loss ledger: ", " ".join(rank(threats, ale)))
    for t in sorted(threats, key=lambda t: -ale(t)):
        print(f"  {t['id']:4} {t['name']:46} ALE {ale(t):>11,.0f}"
              f"  (range {ale(t, 'I_low'):,.0f} to {ale(t, 'I_high'):,.0f})")
    print(f"  total {sum(ale(t) for t in threats):,.0f}")
    for c in controls:
        print(f"  {c['id']:4} {c['name']:46} net year 1 {net_value(c, by_id):>+11,.0f}")
    print("Stable top 3:", " ".join(stable_top(threats, 3)) or "none")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--threats", default=str(HERE / "threats.csv"))
    ap.add_argument("--controls", default=str(HERE / "controls.csv"))
    args = ap.parse_args()
    if args.table:
        table(args.threats, args.controls)
    else:
        raise SystemExit(0 if check() else 1)
