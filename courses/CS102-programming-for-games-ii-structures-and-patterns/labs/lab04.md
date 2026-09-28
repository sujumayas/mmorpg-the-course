# CS102 · Lab 04: The proximity budget

**Week:** 4 ([Big-O intuition for game developers](../lectures/w04-big-o-intuition-for-game-developers.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare numbers with a neighbor at the end

## Objective

Measure what one proximity check costs on your machine, use the count `n(n − 1)/2` to predict the cost of the all-pairs check at any size, and find the largest battle that fits a frame budget with the naive check and with a uniform grid. By the end you should be able to tell a designer, with numbers, how many units the current code supports and what doubling that would take.

## Starter materials

- Python 3.10 or later. No packages needed. (In this repository, `.venv/bin/python`.)
- `labs/lab04-starter/proximity.py`. It contains `make_units`, `naive_pairs`, `grid_pairs` and a `main` that prints checks and times for several sizes. Run it as `python proximity.py` and `python proximity.py --clustered`. `python proximity.py --check` asserts that `naive_pairs` and `grid_pairs` find the same number of hits on uniform and clustered layouts at two radii, and on your mixed-cluster layouts from step 9. It exits with status 1 on the starter, because `cluster_fraction_units` does not exist yet, and with status 0 once step 9 is done.
- Reference values from the lecture's machine (CPython 3.13, Apple silicon): `c_pair ≈ 50 ns`, `c_unit ≈ 1 µs`, naive `n_max = 566` at 8 ms. Yours will differ. The shapes should not.
- Formulas from the lecture:

```
pairs(n)         = n (n − 1) / 2
T_naive(n)       = pairs(n) × c_pair
n_max_naive      = floor((1 + sqrt(1 + 8B / c_pair)) / 2)
checks_grid(n)   ≈ 4.5 n² / C        (units spread evenly, C cells)
T_grid(n)        ≈ n × c_unit + checks_grid(n) × c_pair
```

## Steps

### Part A: measure your constants (30 minutes)

1. Run `proximity.py` three times. For each `n`, keep the smallest naive time (the others include noise from the operating system).
2. Compute `c_pair = naive ms / naive checks` for `n = 1000`, `2000` and `4000`. They should agree within about 15%. Use their average.
3. Estimate `c_unit` from the grid column: `c_unit ≈ (grid ms − grid checks × c_pair) / n` at `n = 4000`.
4. Add a function `doubling_ratio(times)` that, given the naive times for `n` and `2n`, returns their ratio. Print it for 500→1000, 1000→2000 and 2000→4000. Explain in one sentence why it's close to 4.

### Part B: predict before you measure (30 minutes)

5. Using only your constants, predict the naive and grid times for `n = 3000` and `n = 6000`. Write the predictions down.
6. Add 3000 and 6000 to `sizes` and run. Record actual times and the percentage error of each prediction.
7. Compute `n_max_naive` and `n_max_grid` for budgets of 4 ms and 8 ms on your machine. For the grid, search `n` upward in steps of 10 until `T_grid(n)` exceeds the budget.

### Part C: break the grid (25 minutes)

8. Run `--clustered`. Compute the ratio `grid checks / naive checks` for each size. Explain why it stays roughly constant rather than falling.
9. Write a function `cluster_fraction_units(n, frac, seed=1)` that places `round(frac × n)` of the units in the 30 × 30 corner at the origin and the rest spread over the world. Run `python proximity.py --check` until every line passes. A timing is only worth reporting if both methods find the same pairs. Time the grid at `n = 2000` for `frac = 0, 0.1, 0.25, 0.5`. Plot or tabulate grid ms against `frac`.
10. From step 9, state the largest cluster fraction at which the grid still fits 8 ms at `n = 2000` on your machine.

### Part D: the designer note (at home)

11. Write a note of at most 300 words to a designer who wants a 1,500-unit siege and a world boss that 400 players stack on. State, with your numbers, whether each fits 8 ms, what each would cost with the naive and the grid method, and one design or technical change you would propose for the world boss case.

## Deliverable

Your modified `proximity.py`, passing `--check`, a text file or notebook with the tables from steps 2, 6, 7 and 9, and the designer note as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Measured constants (20%) | `c_pair` from three sizes agreeing within 15%; `c_unit` derived correctly; doubling ratios explained | Constants correct, explanation thin | One constant wrong or taken from a single noisy run | Not attempted |
| Predictions (25%) | Predictions written before running; errors computed; errors under 20% or explained | Predictions and errors present, one missing | Predictions made after measuring, or no error analysis | Missing |
| Budget limits (20%) | Both `n_max` values at both budgets, method shown | Values right, method unclear | Only the naive limit | Missing |
| Clustering (20%) | Mixed-cluster function works and `--check` passes; table or plot for four fractions; threshold stated and justified | Table present, threshold vague | Only the `--clustered` run discussed | Missing |
| Designer note (15%) | Both scenarios answered with numbers; a concrete proposal with its trade-off | Numbers present, proposal vague | No numbers | Missing |
