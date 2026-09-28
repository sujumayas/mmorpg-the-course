# MMO401 · Lab 07: Tuning a transaction tax on an order-book simulation

**Week:** 7 ([lecture](../lectures/w07-taxes-and-fees-as-policy.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** ABM labs (40% of the course grade). The final project reuses this market module.

## Objective

Turn the lecture's first-order bypass model into an agent-based simulation, find the tax rate that maximizes the sink for three bypass costs, and recommend a rate and a bypass rule for a stated policy goal.

## Starter materials

- [`lab07-starter.py`](lab07-starter.py): Python 3, standard library only. It contains
  - `make_day(rng)`, which builds 100 bids and 100 asks, either the lecture's evenly spread book (no `rng`) or random values on 0 to 100;
  - `clear_book(bids, asks, t)`, which matches the k-th highest bid with the k-th lowest ask while `bid ≥ ask / (1 − t)`;
  - `trade_price`, the midpoint of the bid and the tax-grossed ask;
  - a working `run_day(t)` with no bypass;
  - a `check_baseline()` that compares trade counts at 0%, 5%, 10%, 20% and 50% with the lecture table (50, 49, 47, 44, 33);
  - a `sweep()` helper that averages 200 random days per rate and a CSV writer;
  - two stubs to write, `bypass_cost` and `run_day_with_bypass`.
- The interactive spec at the end of the lecture and, once built, `examples/w07-tax-order-book.html` for spot checks.
- Any plotting tool (matplotlib or a spreadsheet chart).
- Optional: your lab 05 matching engine. If you prefer, port `run_day_with_bypass` into it instead of the starter's simple call market; report which you used.

Run the starter first. It must print "ok" for all five baseline rows and "Bypass: not run yet".

## Steps

### Part A: baseline (20 min)

1. Run the starter and confirm the baseline check.
2. Open `lab07-baseline.csv`. Plot sink and trades against the tax rate. Your random-book sink at 10% should be within 5% of the lecture's 249 (sampling noise and the midpoint price rule explain the gap). Write one sentence explaining why the random book gives slightly different numbers from the evenly spread one.

### Part B: add the bypass channel (45 min)

3. Implement `bypass_cost(rng, E)` as a uniform draw on `[0, E]`.
4. Implement `run_day_with_bypass(t, E, rng)`. For each matched pair, draw `e`. If `t × price > e`, the pair trades off-market, pays no tax and loses `e` of value. Otherwise it trades on the market and pays the tax.
5. Sweep `t` from 0% to 60% in steps of 0.5% for `E` = 10, 20 and 40. Find the revenue-maximizing rate for each. Expect peaks near 9%, 18% and 31%, each within 3 points of the lecture's first-order values (9.3%, 17.3%, 29.9%).
6. Plot, on one chart, sink against rate for the three `E` values. On a second chart plot on-market trades against rate.

### Part C: relax the first-order assumption (35 min)

7. The lecture kept total trades fixed and only moved them between channels. Change the clearing rule so that a pair whose surplus covers its bypass cost (`bid − ask ≥ e`) trades off-market even when it fails the tax test. Pairs that fail both tests don't trade.
8. Rerun the `E = 20` sweep. Report the new peak rate, the total trades at 20%, and the destroyed value (lost surplus plus bypass costs paid) at 20%.
9. In two sentences, say whether the first-order model overstated or understated the damage of a high tax, and why.

### Part D: recommendation (20 min)

10. Your live team wants at least 150 gold a day of sink from this market and wants at least 70% of trades to stay on the market (for price data and scam protection). Using your Part C model, find every `(t, E)` pair on a grid (`t` in 1% steps up to 30%, `E` in {10, 20, 30, 40, 60}) that meets both targets.
11. Pick one and name the in-game rule that would give you that `E` (for example a mail fee, a trade-window cooldown, or binding on trade).

## Deliverable

- Your completed script, runnable with `python3`, plus the CSVs it writes.
- A report of up to 2 pages: the Part A sentence, the Part B table of peaks and both charts, the Part C numbers and sentences, and a 250-word recommendation from Part D that cites your own numbers and names who pays for the rule you chose.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Baseline and bypass implementation (Parts A, B) | Baseline passes; bypass matches the spec; peaks within 3 points of expected | Runs, with one rule wrong or peaks off by more than 3 points | Does not run | 30 |
| Charts and peak table | Both charts labelled, peaks marked, three `E` values | Charts present but unlabelled or one `E` missing | Missing | 15 |
| Relaxed model (Part C) | Clearing rule correct, three numbers reported, explanation correct | Numbers reported, explanation vague | Missing | 20 |
| Recommendation (Part D) | Feasible set found, choice justified with own numbers, rule and its cost named | Choice made without the feasible set, or cost not named | Missing | 25 |
| Code quality | Parameters in one place, readable, runs first time | Runs with minor fixes | Does not run | 10 |
| **Total** | | | | **100** |
