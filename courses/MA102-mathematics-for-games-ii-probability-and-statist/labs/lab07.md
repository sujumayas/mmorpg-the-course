# MA102 · Lab 07: Dry streaks at scale

Assigned in week 7 ([lecture](../lectures/w07-geometric-distribution-kills-until-the-drop.md)). Due at the start of week 8. Counts toward the problem-set grade.

## Objective

Simulate a population of players farming a rare drop, confirm that the simulated dry curve matches `(1 − p)^n`, and use the result to recommend where a pity cap should go for an item players need to progress.

By the end you will have working simulation code that you will reuse in the week 11 Monte Carlo lab.

## Starter materials

- [`starter/lab07_starter.py`](starter/lab07_starter.py). It is a Python 3 script (paste it into a notebook if you prefer) with numpy and matplotlib imported, a seeded random generator (`rng = np.random.default_rng(102)`), and three empty functions:
  - `simulate_first_success(p, players, rng)` returns an array with the kill number of each player's first drop.
  - `dry_curve(samples, n_max)` returns the share of players still dry after each n from 0 to n_max.
  - `percentile_wait(samples, q)` returns the kill count by which a share q of players have the drop.
- A spreadsheet version for students who prefer it. Build the sheet yourself from this layout. It has one row per kill, a column for `(1 − p)^n`, and an empty sheet for 1,000 simulated players using `RAND()`.
- The week 7 interactive, [`examples/w07-kills-until-drop.html`](../examples/w07-kills-until-drop.html), to check your exact values.

You may use either the notebook or the spreadsheet. The notebook scales to 10,000 players easily; the spreadsheet should use 1,000.

## Steps

1. **Simulate one player.** Write a loop that draws a uniform random number per kill and stops when it is below `p`. Return the kill number. Run it 10 times at `p = 0.01` and write down the results. Note how different they are.
2. **Simulate the population.** Run it for 10,000 players (1,000 in the spreadsheet) at `p = 0.01`. A faster alternative is `rng.geometric(p, size=players)`. Use both once and confirm they agree to within simulation noise.
3. **Compare to the formula.** Plot the simulated dry share against `(1 − p)^n` for n = 0 to 500 on the same axes. Report the simulated and exact dry share at n = 69, 100 and 299 in a table.
4. **Percentiles.** Compute the simulated median, mean, 95th and 99th percentile. Compare each to the exact values (69, 100, 299, 459). Explain in two sentences why the simulated 99th percentile is noisier than the median.
5. **Two-player groups.** Pair players up. Model two loot rules. Rule A: each player rolls their own 1% chance each kill. Rule B: the boss rolls once at 1%, and if it drops, a random member of the pair gets it. For each rule, find how many kills until 95% of *individual* players have the item. Which rule is kinder to the unlucky player, and by how much?
6. **Required-item recommendation.** A raid weapon drops at 5% per weekly clear. Compute the 95th and 99th percentile wait in weeks. Propose a pity cap (a clear number after which the item is guaranteed). Simulate the capped system, and report the new mean wait and the share of players whose wait was shortened by the cap.

## Deliverable

Submit one notebook or spreadsheet plus a PDF memo of at most 400 words addressed to a lead designer. The memo must contain:

- The table from step 3 and the percentile comparison from step 4.
- Your answer to step 5 with the numbers.
- Your pity cap from step 6, the new mean and the share of players affected, and one sentence on what the cap costs the design (for example, rarity or economy value).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Simulation correctness | Code or sheet runs, seeded, results within noise of the exact values | Runs with minor errors or unseeded | Does not run or gives wrong distribution | 25% |
| Formula comparison | Plot and table clearly overlay simulation and `(1 − p)^n`, differences explained | Plot or table present, weak explanation | Missing or wrong | 20% |
| Group loot analysis | Both rules modelled, correct 95th percentiles, clear comparison | One rule correct or comparison unclear | Missing | 20% |
| Pity cap design | Cap justified with percentiles, new mean and affected share computed by simulation | Cap given with partial justification | Cap arbitrary or missing | 25% |
| Memo clarity | Under 400 words, numbers first, plain language, a designer could act on it | Understandable but padded or missing a number | Hard to follow | 10% |
