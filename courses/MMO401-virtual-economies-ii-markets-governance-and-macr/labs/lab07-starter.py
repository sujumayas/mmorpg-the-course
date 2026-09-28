"""MMO401 Lab 07 starter: a daily order book with a sales tax and an untaxed bypass channel.

Standard library only. Run:  python3 lab07-starter.py
The baseline (no bypass) works and checks itself against the lecture table.
Your tasks are the functions marked TODO.
"""
import csv
import random

N_BUYERS = 100
N_SELLERS = 100


def make_day(rng=None):
    """Return (bids, asks) for one day.

    Deterministic mode (rng is None): bids are 100, 99, ..., 1 and asks are 1, 2, ..., 100,
    exactly the lecture's evenly spread book. Random mode: values uniform on [0, 100].
    """
    if rng is None:
        bids = [101 - k for k in range(1, N_BUYERS + 1)]
        asks = [k for k in range(1, N_SELLERS + 1)]
    else:
        bids = [rng.uniform(0, 100) for _ in range(N_BUYERS)]
        asks = [rng.uniform(0, 100) for _ in range(N_SELLERS)]
    return sorted(bids, reverse=True), sorted(asks)


def clear_book(bids, asks, t):
    """Match the k-th highest bid with the k-th lowest ask while bid >= ask / (1 - t).

    Returns a list of (bid, ask) pairs that trade. The trade price for a pair is the midpoint
    between the bid and the grossed-up ask; see trade_price().
    """
    trades = []
    for bid, ask in zip(bids, asks):
        if bid >= ask / (1 - t):
            trades.append((bid, ask))
        else:
            break
    return trades


def trade_price(bid, ask, t):
    """Buyer price for one matched pair: midpoint of the bid and the tax-grossed ask."""
    return (bid + ask / (1 - t)) / 2


def run_day(t, rng=None):
    """Baseline: every matched trade goes through the market and pays tax."""
    bids, asks = make_day(rng)
    trades = clear_book(bids, asks, t)
    sink = sum(t * trade_price(b, a, t) for b, a in trades)
    value = sum(b - a for b, a in trades)
    return {"t": t, "trades": len(trades), "on_market": len(trades), "sink": sink, "value": value}


# ---------------------------------------------------------------- TODO part B
def bypass_cost(rng, E):
    """TODO: draw one trader pair's bypass cost e, uniform on [0, E]."""
    raise NotImplementedError


def run_day_with_bypass(t, E, rng):
    """TODO: like run_day, but a matched pair trades off-market when
    t * trade_price(...) > bypass_cost(rng, E). Off-market trades pay no tax
    and cost the pair e (count e as destroyed value). Return the same keys as
    run_day plus 'off_market'.

    Part C asks you to go further: re-clear the book so that a pair whose surplus
    covers e (bid - ask >= e) can trade off-market even when it fails the tax test.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- checks
def check_baseline():
    expected = {0.0: 50, 0.05: 49, 0.10: 47, 0.20: 44, 0.50: 33}
    ok = True
    for t, k in expected.items():
        got = run_day(t)["trades"]
        flag = "ok" if got == k else "MISMATCH"
        ok &= got == k
        print(f"t={t:.2f}: trades {got} (lecture {k}) {flag}")
    return ok


def sweep(fn, rates, days=200, seed=401, **kw):
    """Average fn over `days` random days for each rate. Returns list of dicts."""
    rows = []
    for t in rates:
        rng = random.Random(seed)
        acc = {}
        for _ in range(days):
            r = fn(t, rng=rng, **kw)
            for key, v in r.items():
                acc[key] = acc.get(key, 0) + v
        rows.append({k: v / days for k, v in acc.items()})
    return rows


def write_csv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    print("Baseline check against the lecture's discrete book:")
    check_baseline()
    rates = [i / 100 for i in range(0, 81, 2)]
    write_csv(sweep(run_day, rates), "lab07-baseline.csv")
    print("Wrote lab07-baseline.csv (random books, no bypass).")
    try:
        rows = sweep(run_day_with_bypass, rates, E=20)
        write_csv(rows, "lab07-bypass-E20.csv")
        print("Wrote lab07-bypass-E20.csv")
    except NotImplementedError:
        print("Bypass: not run yet (implement bypass_cost and run_day_with_bypass).")
