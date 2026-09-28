# MMO401 · Lab 05: Build a matching engine

**Week:** 5 ([lecture](../lectures/w05-market-microstructure-order-books-and-spreads.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** ABM labs (40% of the course grade). Lab 06 imports this engine.

## Objective

Run a price-time priority order book with fees, populate it with simple agents (impatient buyers, impatient sellers, gatherers and one market maker), and measure how the fee schedule changes the spread, the depth and the market maker's profit. You will see the week 5 break-even spread appear in a simulation that never uses the formula.

## Starter materials

- [`lab05-starter.py`](lab05-starter.py): Python 3, standard library only. It contains
  - a working `Book` class with `limit(side, price, qty, owner)`, `market(side, qty, owner)`, `best_bid()`, `best_ask()`, `spread()`, `depth(side, within)` and `cancel_all(owner)`. The resting order sets the trade price. Older orders at the same price fill first. A broker fee is charged on each placed limit order and a sales tax on each sale, and both go to `book.sink`;
  - `lecture_book()`, which loads the herb book from the lecture;
  - `check_lecture()`, which walks the book for the lecture's order sizes and prints "ok" against the lecture table;
  - three stubs to write: `break_even_ratio(b, t)`, the `MarketMaker` class and `run_day(...)`.
- The week 5 interactive, once built (`examples/w05-order-book-depth.html`), for spot checks.
- Any plotting tool.

Run the starter first. It must print "Lecture checks: ok" and "Agents: not written yet".

## Steps

### Part A: read the engine (20 min)

1. Read `Book._cross`. In two sentences, explain who gets the price improvement when a new buy order is priced above the best ask, and which Old School RuneScape rule from the lecture this copies.
2. Using the engine, walk the lecture book with a market sell of 370 units. Record proceeds and average price. Check it by hand against the bid side.

### Part B: agents (50 min)

3. Implement `break_even_ratio(b, t)`. The starter prints the EVE "both at V" value, which must read 1.0670.
4. Implement `MarketMaker.act(book)` following the docstring. Before the day starts, give the maker its starting stock and cash with `book.stock[name] = start_stock` and `book.cash[name] = start_cash`. The maker must cancel its old orders each tick before posting new ones.
5. Implement `run_day(...)` as described in its docstring. Use `random.Random(seed)` so runs repeat exactly. Return mean spread, mean ask depth within 5%, number of trades, the maker's end-of-day profit (cash change plus stock change valued at 10.0), and `book.sink`.

### Part C: experiments (40 min)

6. **Fee sweep.** With `half_spread = 0.03` (a 6% quoted spread), run 30 seeds each for broker fee and sales tax pairs `(0, 0)`, `(0, 0.02)`, `(0.015, 0.03375)`, `(0.03, 0.075)`. Tabulate mean profit, trades and sink.
7. **Spread sweep.** At the EVE "both at V" fees, sweep `half_spread` from 0.01 to 0.10 in steps of 0.005. Find the smallest quoted spread at which the mean profit over 30 seeds is positive. Compare it with the break-even spread from step 3.
8. **Depth test.** After a day at each fee level, send one 200-unit market buy and record its slippage. Does the fee level change slippage? Explain through what the fee does to how many units the maker is willing to post.

## Deliverable

Your completed `lab05-starter.py` (renamed `lab05.py`) and a report of at most two pages: the Part A answers, the step 6 table, a chart of mean maker profit against quoted spread for step 7 with the break-even spread marked, and a paragraph for step 8.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Engine reading | Price-improvement rule stated correctly, sell-370 numbers right and checked by hand | One of the two right | Neither | 15 |
| Agents | Maker and day loop follow the spec, seeded, maker never sells stock it lacks | Runs with one deviation from the spec | Does not run | 25 |
| Fee sweep | Table complete with 30 seeds per cell, sink and trades move in the expected directions and are explained | Table complete, no explanation | Incomplete | 20 |
| Break-even comparison | Simulated threshold within 1.5 points of the formula, any gap explained (inventory risk, unsold stock) | Threshold found, no comparison | Missing | 25 |
| Depth paragraph | Links fees to posted size and slippage with a number | Claim without numbers | Missing | 15 |

<details>
<summary>Instructor check values</summary>

- Sell 370 into the lecture book: `50 × 9.8 + 120 × 9.5 + 200 × 9.0 = 490 + 1,140 + 1,800 = 3,430`, average about 9.27.
- `break_even_ratio(0.015, 0.03375) = 1.0670`; `(0.03, 0.075)` gives 1.1508; `(0, 0.02)` gives 1.0204.
- The simulated threshold in step 7 usually lands a little above 6.7%, because the maker ends some days holding stock bought at the bid and valued at 10.0, and because gatherer asks sometimes undercut the maker. A result between 6.5% and 8% is correct.
- At `(0.03, 0.075)` and a 6% quoted spread the maker loses money on every seed. Students who see this have found the "skills create a profession" point from the lecture.

</details>
