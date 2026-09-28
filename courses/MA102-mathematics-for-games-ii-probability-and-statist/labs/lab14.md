# MA102 · Lab 14: Analyze an A/B test, and design one

**Week:** 14 ([Intro to hypothesis testing (A/B)](../lectures/w14-intro-to-hypothesis-testing-ab.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** problem sets (35% of the course grade); the test plan in step 5 is reused in the final loot-system design
**Work:** in pairs; submit one folder per pair

## Objective

You will analyze a simulated A/B test of a game tutorial, confirm by simulation what a 5% false-positive rate looks like, and write a test plan that is sized to detect the effect you care about.

## Starter materials

The files are in [`lab14-starter/`](lab14-starter/README.md). Each item is described so you can rebuild it if needed.

- [`tutorial_test.csv`](lab14-starter/tutorial_test.csv). 4,800 rows, one per new player: `player_id`, `group` (A or B), `completed_tutorial` (0/1), `day1_return` (0/1), `sessions_day1` (integer), `platform` (pc or mobile). Assignment was random, 50/50.
- [`ab_template.py`](lab14-starter/ab_template.py). Functions to fill in for `k_A`, `n_A`, `k_B`, `n_B`, pooled rate, SE, `z`, p-value, the interval for the difference, the power formula and the A/A simulation. Spreadsheet users build the same cells, with the power formula on a second sheet.
- [`mulberry32.py`](lab14-starter/mulberry32.py). The seeded random generator (seed 14 for all simulations).
- The interactive [`examples/w14-ab-test-simulator.html`](../examples/w14-ab-test-simulator.html) for checking numbers.

## Steps

1. **Check the split (10 min).** Count players per group and per platform within each group. Is the split close to 50/50? Use a one-proportion interval from week 13 on the share of players in B. If it excludes 50%, stop and report the assignment problem before analyzing anything.
2. **Primary test (25 min).** The primary metric, fixed in advance, is `completed_tutorial`. Compute both rates, the pooled rate, SE, `z` and the p-value. State the verdict at α = 0.05. Compute the 95% confidence interval for the difference using the unpooled SE, `sqrt(p̂_A(1 − p̂_A)/n_A + p̂_B(1 − p̂_B)/n_B)`.
3. **The metric fishing trap (20 min).** Now test `day1_return`, then `completed_tutorial` separately on pc and on mobile, then `day1_return` on pc and on mobile. That is six tests in all, counting step 2. How many are significant at 0.05? Apply the Bonferroni threshold. Write two sentences on which results you would report to the producer and how.
4. **A/A simulation (25 min).** Simulate 1,000 A/A tests, each with 2,400 players per group and a true rate equal to group A's observed completion rate. Record the fraction with `|z| > 1.96`. Then repeat with "peeking": for each simulated test, compute `z` after every 200 players per group and stop at the first `|z| > 1.96`. Report both false-positive rates.
5. **Test plan (at home).** Pick one change to your loot-system design project, for example a pity timer or a changed drop rate. Write a one-page plan with: hypothesis, primary metric and its current baseline (estimate one if needed and say how), minimum effect worth detecting, `α`, power, `n` per group from the power formula, expected duration given an assumed daily player count, unit of randomization, and one threat specific to online games (interference, fairness or novelty) with your mitigation.

## Deliverable

One folder named `lab14-<name1>-<name2>` containing:

- The spreadsheet or script, reproducible with seed 14.
- `results.md` with the answers to steps 1 to 4, each number next to the formula that produced it.
- `test-plan.pdf`, one page, from step 5.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Split check (step 1) | Counts and interval correct, conclusion stated | Counts correct, no interval | Missing | 2 |
| Primary test (step 2) | `z`, p-value, verdict and interval for the difference all correct and interpreted in plain words | Correct numbers, weak interpretation, or interval missing | Wrong test or wrong arithmetic | 5 |
| Multiple comparisons (step 3) | Six tests done, Bonferroni applied, reporting advice is honest about which result is primary | Tests done, correction missing or misapplied | Missing | 4 |
| A/A and peeking (step 4) | Both rates reported, A/A near 5%, peeking rate clearly higher, explanation correct | One of the two simulations missing or unexplained | Missing | 4 |
| Test plan (step 5) | All nine elements present, sample size and duration computed correctly, online-game threat is specific and the mitigation is realistic | Plan complete but sizing wrong or threat generic | Missing or not sized | 5 |
