"""MMO402 Lab 13 starter: stranded value of a shutdown.

Usage:
  python3 lab13-starter.py lab13-purchases.csv [--notice N] [--cost C] [--balance B]

Purchase file: CSV with header `age_months,category,spend_usd`. Each row is the
real money spent on one category in one month, dated by its age at the moment the
shutdown is announced (0.5 = the month just before the announcement).

Model (week 13, section 2). A purchase of price P and useful life L months keeps
a straight-line share of its value. If it was bought `a` months before the
announcement and the servers close N months after it, the value it loses is

    stranded = P * max(0, 1 - (a + N) / L)

Real-money sales stop on the day of the announcement. Unspent premium currency
(the balance B) is stranded in full unless the operator refunds or converts it.
The operator pays C per month to keep the world running during the notice period.

Pure standard library. Python 3.8+.
"""
import csv
import sys

# Useful life in months for each category. These are the lab's assumptions,
# not facts about any real game. Change them only in step 4.
LIFETIME = {
    "cosmetic": 12.0,
    "season_pass": 3.0,
    "expansion": 24.0,
}


def load(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append((float(r["age_months"]), r["category"], float(r["spend_usd"])))
    return rows


def stranded(rows, notice, lifetime=LIFETIME):
    """Total value purchases lose when servers close `notice` months after the announcement."""
    total = 0.0
    for age, cat, spend in rows:
        L = lifetime[cat]
        total += spend * max(0.0, 1.0 - (age + notice) / L)
    return total


def stranded_by_category(rows, notice, lifetime=LIFETIME):
    out = {}
    for age, cat, spend in rows:
        L = lifetime[cat]
        out[cat] = out.get(cat, 0.0) + spend * max(0.0, 1.0 - (age + notice) / L)
    return out


def total_cost(rows, notice, monthly_cost, balance=0.0):
    """Operator's running cost during notice plus everything players lose."""
    return monthly_cost * notice + stranded(rows, notice) + balance


def best_notice(rows, monthly_cost, max_months=24, step=0.25, balance=0.0):
    """TODO (step 2): return the notice period N in [0, max_months], searched in
    steps of `step`, that minimises total_cost. On ties, return the shorter N."""
    raise NotImplementedError


def refund_window(rows, window, notice):
    """TODO (step 3): a policy refunds the full price of every purchase younger
    than `window` months at the announcement (age < window). Return a pair
    (refund_paid, stranded_left): the cash refunded, and the value still
    stranded at shutdown on the purchases that were NOT refunded."""
    raise NotImplementedError


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    rows = load(args[0])
    def opt(name, default):
        return float(args[args.index(name) + 1]) if name in args else default
    notice = opt("--notice", 0.0)
    cost = opt("--cost", 150000.0)
    balance = opt("--balance", 0.0)
    spent_12 = sum(s for a, _, s in rows if a < 12)
    print(f"Spent in the 12 months before the announcement: ${spent_12:,.0f}")
    for n in (0, 1, 3, 6, 9, 12):
        mark = "  <-- chosen" if n == notice else ""
        print(f"notice {n:>2} months: stranded ${stranded(rows, n):>11,.0f}"
              f"   running cost ${cost * n:>11,.0f}"
              f"   total ${total_cost(rows, n, cost, balance):>11,.0f}{mark}")
    print("By category at the chosen notice:")
    for cat, v in stranded_by_category(rows, notice).items():
        print(f"  {cat:<12} ${v:,.0f}")
    try:
        n = best_notice(rows, cost, balance=balance)
        print(f"Best notice at ${cost:,.0f}/month: {n} months, total ${total_cost(rows, n, cost, balance):,.0f}")
    except NotImplementedError:
        print("best_notice() not implemented yet (step 2).")


if __name__ == "__main__":
    main()
