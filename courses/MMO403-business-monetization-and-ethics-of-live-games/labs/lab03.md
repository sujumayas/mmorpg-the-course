# MMO403 · Lab 03: Premium currency store audit

**Week:** 3, premium currencies ([lecture](../lectures/w03-premium-currencies.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** the store audit counts toward the Models strand (40%); the written check against the CPC principles is the first input to the ethics analysis (20%).

## Objective

Implement the cheapest-cover solver from lecture section 2 with dynamic programming, use it to audit a store's pack grid and item prices, and then audit one real game's store. You finish with a redesign that removes forced leftovers, and an honest estimate of what the redesign costs in revenue.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python 3.10 or later. All money is in integer cents.

- [`packs.py`](lab03-starter/packs.py), with the lecture's Emberfall pack grid, a CSV loader and four empty functions: `cheapest_cover`, `reference_cents`, `audit` and `sequence`.
- [`flat_store.csv`](lab03-starter/flat_store.csv), a flat-rate grid of 80 coins per dollar with the same pack sizes and prices as the Guild Wars 2 gem store in September 2026.
- [`test_packs.py`](lab03-starter/test_packs.py), the lecture's test values: the five-row Emberfall table, reference prices, the 300-coin starting balance case, the tie rule (same cash, prefer more currency), the purchase sequences from section 3, and the flat store. Every test fails on the starter.
- The interactive `examples/w03-currency-packs.html` for spot checks.

Run the tests from inside the folder with `python3 test_packs.py` (or `pytest`).

## Steps

1. **Solver.** Implement `cheapest_cover(packs, c, balance)`. Use a dynamic program: `best[x]` is the fewest cents that buy exactly `x` coins, for `x` from 0 to `c − balance + largest pack`. Then take the cheapest `x ≥ c − balance`, breaking ties by the larger `x`. Recover the pack counts by storing which pack reached each `x`.
2. **Reference price.** Implement `reference_cents(packs, c)` at the smallest pack's rate, rounded half up.
3. **Audit.** Implement `audit(packs, prices)` returning cash, leftover, reference and markup per item.
4. **Sequence.** Implement `sequence(packs, prices, balance)` for a player buying items one after another.
5. **Tests.** Run until all seven tests pass.
6. **Sawtooth.** Print the leftover for every item price from 100 to 3,000 in steps of 100 for both grids. Compute the mean leftover and mean markup for 100 to 2,000. Confirm Emberfall's 450 coins and 2.13.
7. **Real store.** Pick a game with a premium currency. Record its current pack grid (coins and local price) and the currency prices of at least ten items on sale, with the date and the source for each. Audit it. Report the item with the largest markup and the one with the largest leftover.
8. **Redesign.** Change the pack grid, the item prices or both so that no item's markup exceeds 1.10 from a zero balance. Keep at least one bulk bonus if the original had one. Estimate the revenue change for two players, one who buys a single mid-priced item and quits, and one who buys ten items over a year (use `sequence`).
9. **Principles check.** For the original store and your redesign, write one short paragraph each on CPC key principles 1, 2 and 3 (21 March 2025).

## Deliverable

Your completed `packs.py` with passing tests; the sawtooth output from step 6; the audit table, redesign and revenue estimates from steps 7 and 8; and a written check of at most 600 words (step 9). Cite every real price with its source and date.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Solver | Dynamic program, all tests pass, runs in under a second for 13,500-coin items | Tests pass by brute force only | Tests fail | 25% |
| Real-store audit | Ten or more items, every price sourced and dated, worst cases identified | Fewer items or some prices undated | Unsourced or incorrect | 20% |
| Redesign | Meets the 1.10 bound, keeps a bonus, revenue change estimated for both players | Meets the bound, revenue estimate thin | Bound not met | 25% |
| Principles check | Specific to the store, cites the principle's wording by paraphrase, balanced about the studio's reasons | Generic but correct | Missing or misreads the principles | 20% |
| Presentation | Tables readable, numbers reproducible from the code | Minor gaps | Hard to follow | 10% |
