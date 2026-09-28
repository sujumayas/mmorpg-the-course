"""MMO401 Lab 05 starter: a price-time priority order book with fees, plus agent stubs.

Standard library only. Run:  python3 lab05-starter.py
The engine and the lecture checks work as shipped. Your tasks are marked TODO.
Lab 06 imports this file, so keep the engine's function names unchanged.
"""
import itertools
import random

_seq = itertools.count()  # arrival order for time priority


class Order:
    def __init__(self, side, price, qty, owner):
        self.side = side      # "bid" or "ask"
        self.price = price
        self.qty = qty
        self.owner = owner
        self.seq = next(_seq)


class Book:
    """Two-sided book. Resting order sets the trade price (as in the OSRS Grand Exchange).

    broker_fee: share of order value charged when a limit order is placed (both sides).
    sales_tax:  share of the sale value charged to the seller on every fill.
    Fees are removed from the economy and counted in self.sink.
    """

    def __init__(self, broker_fee=0.0, sales_tax=0.0):
        self.bids, self.asks = [], []
        self.broker_fee, self.sales_tax = broker_fee, sales_tax
        self.cash, self.stock = {}, {}
        self.sink = 0.0
        self.trades = []  # (price, qty, buyer, seller)

    # ---- helpers -------------------------------------------------------------
    def _sort(self):
        self.bids.sort(key=lambda o: (-o.price, o.seq))
        self.asks.sort(key=lambda o: (o.price, o.seq))

    def _pay(self, who, amount):
        self.cash[who] = self.cash.get(who, 0.0) + amount

    def _give(self, who, qty):
        self.stock[who] = self.stock.get(who, 0) + qty

    def best_bid(self):
        return self.bids[0].price if self.bids else None

    def best_ask(self):
        return self.asks[0].price if self.asks else None

    def spread(self):
        if not self.bids or not self.asks:
            return None
        return self.best_ask() - self.best_bid()

    def depth(self, side, within):
        """Units on one side within `within` (a share, e.g. 0.05) of that side's best price."""
        if side == "ask" and self.asks:
            limit = self.best_ask() * (1 + within)
            return sum(o.qty for o in self.asks if o.price <= limit)
        if side == "bid" and self.bids:
            limit = self.best_bid() * (1 - within)
            return sum(o.qty for o in self.bids if o.price >= limit)
        return 0

    # ---- order entry ---------------------------------------------------------
    def limit(self, side, price, qty, owner, charge_fee=True):
        """Place a limit order. Crosses the book first; any remainder rests."""
        if charge_fee:
            fee = self.broker_fee * price * qty
            self._pay(owner, -fee)
            self.sink += fee
        remaining = self._cross(side, qty, owner, price_limit=price)
        if remaining > 0:
            book = self.bids if side == "bid" else self.asks
            book.append(Order(side, price, remaining, owner))
            self._sort()
        return qty - remaining

    def market(self, side, qty, owner):
        """Market order. side="bid" buys from asks, side="ask" sells into bids.
        Returns (filled_qty, total_value)."""
        before = len(self.trades)
        remaining = self._cross(side, qty, owner, price_limit=None)
        value = sum(p * q for p, q, _, _ in self.trades[before:])
        return qty - remaining, value

    def _cross(self, side, qty, owner, price_limit):
        other = self.asks if side == "bid" else self.bids
        while qty > 0 and other:
            top = other[0]
            if price_limit is not None:
                if side == "bid" and top.price > price_limit:
                    break
                if side == "ask" and top.price < price_limit:
                    break
            q = min(qty, top.qty)
            buyer, seller = (owner, top.owner) if side == "bid" else (top.owner, owner)
            value = top.price * q
            tax = self.sales_tax * value
            self._pay(buyer, -value)
            self._pay(seller, value - tax)
            self.sink += tax
            self._give(buyer, q)
            self._give(seller, -q)
            self.trades.append((top.price, q, buyer, seller))
            top.qty -= q
            qty -= q
            if top.qty == 0:
                other.pop(0)
        return qty

    def cancel_all(self, owner):
        self.bids = [o for o in self.bids if o.owner != owner]
        self.asks = [o for o in self.asks if o.owner != owner]


# ---- the lecture's herb book ----------------------------------------------------
LECTURE_BIDS = [(9.8, 50), (9.5, 120), (9.0, 200), (8.0, 300)]
LECTURE_ASKS = [(10.0, 40), (10.2, 60), (10.5, 100), (11.0, 150), (12.0, 200), (14.0, 300)]


def lecture_book(broker_fee=0.0, sales_tax=0.0):
    b = Book(broker_fee, sales_tax)
    for p, q in LECTURE_BIDS:
        b.limit("bid", p, q, "npc_bidder", charge_fee=False)
    for p, q in LECTURE_ASKS:
        b.limit("ask", p, q, "npc_seller", charge_fee=False)
    return b


def check_lecture():
    """Walk the book for the lecture's order sizes and compare with its table."""
    expected = {40: 400, 100: 1012, 200: 2062, 250: 2612, 350: 3712, 550: 6112, 850: 10312}
    ok = True
    for q, cost in expected.items():
        b = lecture_book()
        filled, value = b.market("bid", q, "tester")
        good = filled == q and abs(value - cost) < 1e-6
        ok &= good
        print(f"buy {q:4d}: cost {value:8.1f} avg {value / q:6.3f}  {'ok' if good else 'MISMATCH'}")
    b = lecture_book()
    filled, value = b.market("ask", 200, "tester")
    good = abs(value - 1900) < 1e-6
    ok &= good
    print(f"sell 200: proceeds {value:.1f}  {'ok' if good else 'MISMATCH'}")
    print("spread", round(lecture_book().spread(), 3), "(expect 0.2)")
    return ok


# ---- agents (your work) -----------------------------------------------------------
def break_even_ratio(b, t):
    """TODO 1: return A/B = (1 + b) / (1 - b - t) from lecture section 3."""
    raise NotImplementedError


class MarketMaker:
    """TODO 2: each tick, cancel old orders and post one bid and one ask around the mid.

    Suggested rule: mid = (best_bid + best_ask) / 2 of the book *without* your own orders
    (fall back to a reference price of 10.0 if a side is empty); post the bid at
    mid * (1 - half_spread) and the ask at mid * (1 + half_spread), size `size` each,
    but never post an ask for more units than you hold.
    """

    def __init__(self, name, half_spread, size, start_stock=200, start_cash=5000.0):
        self.name, self.half_spread, self.size = name, half_spread, size
        self.start_stock, self.start_cash = start_stock, start_cash

    def act(self, book):
        raise NotImplementedError


def run_day(book, maker, rng, ticks=200, p_buy=0.3, p_sell=0.3, max_q=30):
    """TODO 3: simulate one day.

    Each tick: the maker acts; then with probability p_buy an impatient buyer sends a
    market buy for randint(1, max_q) units, and with probability p_sell an impatient
    seller sends a market sell for randint(1, max_q) units. NPC gatherers refill the
    ask side: every 20 ticks add a limit ask of 50 units at 10.0 + rng.uniform(0, 1.0)
    (charge_fee=False), and every 20 ticks add a limit bid of 50 units at
    9.5 - rng.uniform(0, 1.0) (charge_fee=False).
    Record the spread and ask depth within 5% after every tick; return a dict of means.
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("Lecture checks:", "ok" if check_lecture() else "FAILED")
    try:
        print("break-even EVE both V:", round(break_even_ratio(0.015, 0.03375), 4), "(expect 1.0670)")
    except NotImplementedError:
        print("Agents: not written yet")
