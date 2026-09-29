# MMO306 · Lab 10: The best-farm simulator

**Week:** 10 ([lecture](../lectures/w10-player-generated-content.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** encounter designs (40%). The reward and funnel rules you write here are required if your final dungeon includes a player-content layer.

## Objective

Implement the best-of-`N` model from the lecture, confirm it by simulation, find out how much the result depends on the shape of the overpay distribution, and use it to set reward and publication rules for a player-made dungeon system.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`ugc_rewards.py`](lab10-starter/ugc_rewards.py), a skeleton with seven functions to write: `harmonic`, `expected_best`, `sample_overpay`, `simulate_best`, `inflow_multiplier`, `funnel` and `largest_pool`. Each docstring states the formula and an example value.
- [`test_ugc_rewards.py`](lab10-starter/test_ugc_rewards.py), ten tests built from the lecture's numbers. All of them fail on the starter. Run them with `python -m unittest test_ugc_rewards.py` inside the folder.
- The [interactive](../examples/w10-best-farm.html) for spot checks.
- A spreadsheet is fine for Part C if you prefer, as long as Parts A and B pass the tests.

## Steps

### Part A: the model (30 min)

1. Implement `harmonic`, `expected_best` and `inflow_multiplier`. Run `python ugc_rewards.py`. Your table must match the lecture's to three decimals.
2. Implement `funnel` and `largest_pool`. Check `largest_pool(0.08, 1.3)` against the lecture's check-yourself question 3. Explain in one sentence why the exact answer (23) and the `ln N` estimate agree here.

### Part B: simulation and the shape of the tail (45 min)

3. Implement `sample_overpay` and `simulate_best`. Run all tests until they pass.
4. For `m = 0.10`, simulate the best rate for `N` = 10, 100, 1,000 and 10,000 with the exponential distribution and with the uniform distribution on `[0, 2m]`. Both have the same mean overpay. Put the eight results in one table beside the formula `1 + m H_N`.
5. Add a third distribution of your choice with the same mean `m` and a heavier tail than the exponential (for example a Pareto with shape 2.5, scaled to mean `m`). Simulate it at the same four values of `N`.
6. Write three sentences. Which distribution does a server-computed reward rule push the mission catalogue toward? Which does an author-configured rule allow? What does that mean for the cap you would need?

### Part C: set the rules (45 min)

7. Your game has 250,000 monthly players, 2% of whom publish one dungeon a month. After a year, how many paying dungeons exist if nothing is removed? Using `m = 0.10`, what is the expected best rate?
8. Choose a combination of levers (server-computed `m`, cap, curated pool, separate currency) that keeps the expected best at or under 1.25× after one year. Report the number for each lever you use, and one cost of each in a sentence.
9. Design a publication funnel with at least three gates that puts between 200 and 400 dungeons a month on the public list. Give each gate's pass rate and say how you would measure it after launch.
10. Assume `φ = 0.25` of play time goes to the best dungeon. Report the inflow multiplier before and after your levers.

## Deliverable

- The completed `ugc_rewards.py` with all tests passing, plus any script you used for Parts B and C.
- A report of at most 2 pages: the Part B table (three distributions, four values of `N`, plus the formula), your three sentences from step 6, and a one-page rules sheet for Part C with the numbers from steps 7 to 10.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model and tests (Part A, step 3) | All ten tests pass; lecture table reproduced | Most tests pass, one function wrong | Tests fail with no diagnosis | 25 |
| Distribution comparison (Part B) | Three distributions simulated at four `N`; table correct; sentences link tail shape to reward rules | Table present, interpretation vague | Missing | 25 |
| Lever design (steps 7-8, 10) | Target met with numbers shown; each lever's cost named and specific | Target met but costs generic, or numbers partly wrong | Target not met | 25 |
| Publication funnel (step 9) | Three or more gates, output in range, each rate measurable after launch | Funnel in range but rates not measurable | Missing | 15 |
| Code quality | Readable, parameters in one place, runs first time | Runs with minor fixes | Does not run | 10 |
| **Total** | | | | **100** |
