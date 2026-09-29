# MMO306 · Lab 01: Locust math on a player population

**Week:** 1 · **Time:** 2 hours in the lab plus about 1.5 hours at home · **Weight:** formative. The functions you write here feed the week 13 cadence plan and the final dungeon's content budget.

**Lecture:** [Week 01, the content treadmill](../lectures/w01-the-content-treadmill-production-vs-consumption.md). **Interactive:** [w01-content-locust.html](../examples/w01-content-locust.html), for checking bars and curves by eye.

## Objective

Implement the lecture's exhaustion time `T`, locust ratio `L` and drought, then run them on a sample of 2,000 players instead of five percentile rows. Use the sample to find the cheapest mix of content hours, replay and gate that keeps the median player busy until the next drop without letting the p99 player race too far ahead. Finish with a short memo that says which percentile your plan serves worst and why you accept it.

## Starter materials

- [`lab01-starter/locust.py`](lab01-starter/locust.py). Loader, a cost function and six functions to fill in: `exhaust_days`, `locust_ratio`, `drought_days`, `percentile`, `share_with_content` and `cheapest_plan`.
- [`lab01-starter/players.csv`](lab01-starter/players.csv). 2,000 invented players with their weekly hours (a lognormal sample with median about 6 hours, generated with a fixed seed).
- [`lab01-starter/test_locust.py`](lab01-starter/test_locust.py). Tests taken from the lecture's table and the sample. Do not edit it.

Run from inside `lab01-starter`:

```
../../../../.venv/bin/python test_locust.py
../../../../.venv/bin/python locust.py
```

On the starter every test fails with `NotImplementedError`. When you are done, all four print `PASS`.

## Steps

1. **Part A, the model (20 min).** Implement `exhaust_days`, `locust_ratio` and `drought_days`. Check them against the section 2 table of the lecture: design A gives the median player 23.3 days, design C gives every player above 12 hours exactly 70 days.
2. **Part B, the population (15 min).** Implement `percentile` with the nearest-rank rule in its docstring. Print the p50, p75, p90, p99 and p99.9 of the sample and compare them with the lecture's invented table (6, 10, 16, 34, 60). Note which rows differ and by how much.
3. **Part C, the curve (15 min).** Implement `share_with_content`. Plot it for day 0 to 175 for the lecture's designs A, B and C (spreadsheet or matplotlib, if you have it). Mark the day the share falls below 50% on each plot.
4. **Part D, the search (25 min).** Implement `cheapest_plan`. Run the test file until all four tests pass. Then run `locust.py` and record the cheapest plan it prints.
5. **Part E, your own rules (20 min).** Change one rule of the search to match a design goal you choose, for example "p90 must have `L ≤ 2`" or "no gate below 20 hours". Rerun it and record how the cheapest plan and its cost change.
6. **Part F, the cliff (at home, 30 min).** For your chosen plan, find the day on which the share of players with content falls fastest (the steepest drop between consecutive days). Explain in two sentences what causes it and what you could release on that day.
7. **Memo (at home, 1 hour).** One page. State your plan, its cost and the five percentile rows with `T` and `L`. Name the percentile it serves worst and argue for or against accepting that.

## Deliverable

Submit a zip with:
- Your completed `locust.py`, with the Part E rule change as a second function or a flag.
- The three plots from Part C and the plot for your chosen plan.
- The one-page memo, including the Part F cliff day and your answer.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Tests | All 4 pass | 2-3 pass | 0-1 pass | 25% |
| Population and curve | Percentiles compared with the lecture table, three plots with the 50% day marked | Plots present but unmarked, or comparison missing | Missing | 20% |
| Search and own rule | Cheapest plan recorded, rule change stated in advance and its effect on cost measured | Rule changed but effect not measured | No search result | 25% |
| Cliff analysis | Cliff day found from the data, cause named (a gate or a cluster of players), a concrete release proposed | Cliff found but cause vague | Missing | 15% |
| Memo | Worst-served percentile named with its `T` and `L`, argument uses the model | Plan described without a judgment | Missing or no numbers | 15% |
