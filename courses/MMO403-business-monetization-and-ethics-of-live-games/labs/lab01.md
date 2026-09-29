# MMO403 · Lab 01: Business model race

**Week:** 1, business models ([lecture](../lectures/w01-business-models-box-subscription-f2p-hybrid.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the Models strand (40%). The model is extended in lab 02.

## Objective

Implement the four-parameter business model from lecture section 2, reproduce its tables, and use it to argue which model fits one real MMO. By the end you should be able to say, with a number, how much one point of monthly retention is worth to that game and at what retention its current model stops beating the alternatives.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python 3.10 or later.

- [`business_models.py`](lab01-starter/business_models.py), with a `Model` dataclass, a CSV loader and four empty functions: `months_active`, `contribution`, `crossover_month` and `retention_value`.
- [`models.csv`](lab01-starter/models.csv), the lecture's four rows (box, subscription, free-to-play, hybrid).
- [`test_business_models.py`](lab01-starter/test_business_models.py), the lecture's test values. It checks the `r = 0.80` table to the cent in millions, that the best model is the box at `r = 0.70` and the subscription at `r = 0.90`, that the subscription passes the box in month 7 at `r = 0.90` and never within 36 months at `r = 0.80`, and the value of one point of retention. Every test fails on the starter.
- The interactive `examples/w01-business-model-race.html` for spot checks.

Run the tests from inside the folder with `python3 test_business_models.py` (or `pytest`).

## Steps

1. **Active months.** Implement `months_active(r, T)`. Check `S(3) = 2.44` at `r = 0.8` by hand first.
2. **Contribution.** Implement `contribution(model, r, T, cost, audience)` as `A × d × (U + (m − c) × S(T))`.
3. **Crossover.** Implement `crossover_month(a, b, r)`. Derive the break-even `S*` for subscription against box on paper and confirm your code agrees with it.
4. **Retention value.** Implement `retention_value(model, r)`. Explain why the box's value is negative.
5. **Tests.** Run until all seven tests pass.
6. **Sensitivity sweep.** For `r` from 0.60 to 0.95 in steps of 0.05 and `c` in {0.25, 0.50, 1.00, 2.00}, record which model wins at 36 months. Present it as a grid (rows `r`, columns `c`, cell = winner).
7. **Fit a real game.** Pick one MMO. From public sources only (store pages, price lists, published player counts, press), estimate `d`, `U`, `m` and `r` as ranges, and cite each source with its date. Where no source exists, say so and give your reasoning.
8. **Argue.** Run your game's current model and one alternative across your ranges. State which model wins in the pessimistic, middle and optimistic cases.

## Deliverable

Your completed `business_models.py` with passing tests, the grid from step 6, and a memo of at most 700 words covering steps 7 and 8. The memo must name which players gain and which lose under your recommended model.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; break-even `S*` derived and matches code | Tests pass, derivation missing | Tests fail | 30% |
| Sensitivity grid | Complete, correct, with one sentence on the pattern | Complete but unexplained | Missing or wrong | 15% |
| Parameter fit | Every parameter sourced and dated, ranges justified | Some parameters unsourced | Guesses presented as facts | 25% |
| Recommendation | Holds across the ranges or says clearly where it fails | Based on the middle case only | No clear recommendation | 20% |
| Who gains, who loses | Specific player groups, tied to `d`, `U` or `m` | Generic statement | Missing | 10% |
