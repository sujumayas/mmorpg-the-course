"""MMO403 Lab 12: the revenue waterfall.

Run:  python fees.py          # prints the channel table and the two publishing deals
      python check_lab12.py   # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.
All money in US$. forecast.csv is one invented year of an invented game.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def bracket_take(gross, brackets):
    """Store share under a bracket schedule. brackets: list of [start, rate] sorted by start;
    each rate applies to the part of gross between its start and the next start."""
    raise NotImplementedError


def status_take(gross, eligible, small, standard, threshold):
    """Apple-style status rule. If eligible (last year's proceeds <= threshold), the small rate
    applies up to threshold and the standard rate to revenue above it this year.
    If not eligible, the standard rate applies to all of gross."""
    raise NotImplementedError


def card_fees(revenue, purchases, pct, fixed):
    """Card processor fees: pct of revenue plus a fixed amount per purchase."""
    raise NotImplementedError


def tax_from_inclusive(spend, rate):
    """Tax contained in a tax-inclusive amount: spend * rate / (1 + rate)."""
    raise NotImplementedError


def channel_take(net, purchases, eligible, schedule):
    """Dispatch on schedule['kind']: 'bracket', 'status' or 'card'. Return the fee in US$."""
    raise NotImplementedError


def publisher_split(payout, studio_share, recoup, base):
    """Split a store payout between studio and publisher. Return (studio, publisher).
    base 'studio': studio's share = studio_share * payout, then recoup is taken from it
      (the studio receives max(0, share - recoup)).
    base 'all': recoup comes off the whole payout first (up to the payout), then the rest
      is split by studio_share.
    The publisher receives everything the studio does not."""
    raise NotImplementedError


def waterfall(spend, purchases, eligible, schedule, tax_rate, refund_rate):
    """Return a dict with keys spend, tax, refunds, net, fee, payout for one channel.
    tax = tax_from_inclusive(spend, tax_rate); refunds = refund_rate * (spend - tax);
    net = spend - tax - refunds; fee = channel_take(net, purchases, eligible, schedule);
    payout = net - fee."""
    raise NotImplementedError


def load():
    schedules = json.loads((HERE / "channels.json").read_text())
    with open(HERE / "forecast.csv") as f:
        rows = [{"channel": r["channel"], "spend": float(r["consumer_spend"]),
                 "purchases": int(r["purchases"]), "eligible": r["eligible_last_year"] == "1"}
                for r in csv.DictReader(f)]
    return schedules, rows


def main():
    try:
        schedules, rows = load()
        total = 0.0
        print("channel         spend        net        fee   avg fee     payout")
        for r in rows:
            w = waterfall(r["spend"], r["purchases"], r["eligible"], schedules[r["channel"]], 0.10, 0.04)
            total += w["payout"]
            print(f"{r['channel']:<11} {w['spend']:>10,.0f} {w['net']:>10,.0f} {w['fee']:>10,.0f} "
                  f"{w['fee'] / w['net']:>8.1%} {w['payout']:>10,.0f}")
        print(f"total payout {total:,.0f}")
        for base in ("studio", "all"):
            studio, pub = publisher_split(total, 0.5, 4_000_000, base)
            print(f"deal 50/50, recoup 4,000,000 from {base:<6}: studio {studio:,.0f}  publisher {pub:,.0f}")
    except NotImplementedError:
        print("TODO: finish the functions, then rerun")


if __name__ == "__main__":
    main()
