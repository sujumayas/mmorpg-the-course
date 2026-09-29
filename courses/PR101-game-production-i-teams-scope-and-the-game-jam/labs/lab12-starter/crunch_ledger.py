"""PR101 lab 12: the crunch ledger from the week 12 lecture.

Usage (from inside this folder):

    python crunch_ledger.py                      # lecture defaults
    python crunch_ledger.py --hours 55 --weeks 3 --deadline 3 --horizon 8
    python crunch_ledger.py --schedule 50,40,50,40,40,40

--schedule gives your own hours for each week and overrides --hours/--weeks.
Output is per person, in fresh hours (hours x efficiency).
"""
import argparse
from itertools import accumulate


def ledger(schedule, f=0.005, g=0.10, e_min=0.3):
    """Return (efficiency, output) per week for a list of weekly hours."""
    e, rows = 1.0, []
    for h in schedule:
        rows.append((e, h * e))
        e = max(e_min, e - f * (h - 40)) if h > 40 else min(1.0, e + g)
        e = round(e, 6)
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--hours", type=float, default=60)
    p.add_argument("--weeks", type=int, default=4, help="crunch length")
    p.add_argument("--horizon", type=int, default=12)
    p.add_argument("--deadline", type=int, default=None)
    p.add_argument("--schedule", type=str, default=None)
    p.add_argument("--f", type=float, default=0.005, help="fatigue rate")
    p.add_argument("--g", type=float, default=0.10, help="recovery rate")
    p.add_argument("--emin", type=float, default=0.3, help="efficiency floor")
    a = p.parse_args()

    if a.schedule:
        schedule = [float(x) for x in a.schedule.split(",")]
        schedule += [40.0] * max(0, a.horizon - len(schedule))
    else:
        schedule = [a.hours if w < a.weeks else 40.0 for w in range(a.horizon)]
    deadline = a.deadline or max(1, a.weeks)

    rows = ledger(schedule, a.f, a.g, a.emin)
    cum = list(accumulate(out for _, out in rows))
    print("week  hours  eff   output  cum   cum40  lead")
    for w, (h, (e, out), c) in enumerate(zip(schedule, rows, cum), start=1):
        mark = "  <- deadline" if w == deadline else ""
        print(f"{w:>4}  {h:>5.0f}  {e:.2f}  {out:>6.1f}  {c:>5.1f}  {40 * w:>5}  "
              f"{c - 40 * w:>+6.1f}{mark}")
    extra = sum(max(0.0, h - 40) for h in schedule)
    lead_end = cum[-1] - 40 * len(schedule)
    print(f"lead at deadline (week {deadline}): {cum[deadline - 1] - 40 * deadline:+.1f}")
    print(f"lead at week {len(schedule)}: {lead_end:+.1f}")
    if extra:
        print(f"extra hours worked: {extra:.0f}, return per extra hour: {lead_end / extra:.2f}")


if __name__ == "__main__":
    main()
