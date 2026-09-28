# GD203 · Lab 12: Duel simulator

**Assigned:** week 12. **Due:** start of week 13. **Weight:** first part of the simulation assessment (20% of the course).
**Lecture:** [Week 12, simulation-driven balance](../lectures/w12-simulation-driven-balance.md). Uses your [lab 11](lab11.md) sheet as the source of stats.

## Objective

Build a seeded Monte Carlo duel simulator, prove it correct against exact results, and use it to map where one of your lab 11 matchups is balanced. By the end you should be able to state a win rate with a confidence interval and show which parameters move it.

## Starter materials

- Python 3 (standard library only; `matplotlib` optional for charts) or a spreadsheet with `RAND()` and enough rows for 10,000 fights. Python is recommended. A spreadsheet sim of 10,000 fights recalculates slowly.
- The `hits_to_kill` function from lecture section 2, as a starting point.
- The [duel simulator](../examples/w12-duel-simulator.html) interactive, to compare your results against for the crit-sword and underdog cases.
- Three validation targets from the lecture:
  1. Crit sword (10 damage, 25% crit for ×2) vs 50 health, enemy kills hero with its 4th attack: hero-first win 68.4%, enemy-first 15.6%.
  2. Underdog: A steady 10 vs B with 0-or-18 at 50%, both 50 health. B wins 31.25% with A first, 50% with B first.
  3. Crit chance 0: hero wins 0% in both orders.
- Your lab 11 sheet, level 15 row, for the soldier's stats and the player's weapon.

## Steps

1. **Structure.** Write separate functions for state setup, one attack (rules), the duel loop, and a runner that plays `N` duels and returns wins, fight lengths and the hits-to-kill distribution. Create the random generator with a seed passed in as an argument.
2. **Validate.** Run each validation target with `N = 10,000`. For each, report the simulated win rate, its 95% interval, and whether the exact value falls inside. Fix your code until all three pass.
3. **Real-time loop.** Extend the duel to real time with an event queue: each side has an attack interval (take them from your lab 11 soldier and player weapon), and the next attack is scheduled at `now + interval`. Check that when both intervals are equal the result matches the turn-based version with the same first-swinger.
4. **Your matchup.** Simulate the level 15 player against the level 15 soldier with a crit chance you choose. Report win rate, mean fight length and the hits-to-kill distribution. Compare with your lab 11 sheet's prediction and explain any gap.
5. **Precision.** Rerun step 4 with `N` = 100, 1,000 and 10,000, each with 5 different seeds. Tabulate the spread of results and compare it with the formula `1.96 × sqrt(p(1 − p)/N)`.
6. **Sweep.** Sweep two parameters over a grid of at least 8 × 8 (for example player crit chance 0-50% and soldier health ±30% around its lab 11 value), 2,000 fights per cell, using common random numbers. Produce a heatmap or a colored table of win rate.
7. **Frontier.** Mark the cells between 45% and 55%. Describe the shape of that frontier and point out any cliff (a jump of more than 15 points between neighbouring cells). Link each cliff to a breakpoint.

## Deliverable

- Source code (or spreadsheet) that runs from a clean start and prints the three validation results.
- A results document with the validation table, the step 4 comparison, the precision table and the heatmap.
- A 400-word analysis: Where is your matchup balanced, how fragile is it (steepness around the frontier), and which one parameter would you change to move the level 15 soldier fight into a 75-85% player win band? Support every claim with a number from your results.

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Code structure and reproducibility (15%) | Clear separation of rules, loop and runner; seeded; reruns give identical output | Seeded but tangled | Unseeded or not rerunnable | Does not run |
| Validation (25%) | All three targets pass with intervals reported | Two pass | One passes, or intervals missing | No validation |
| Real-time extension (15%) | Event queue correct, equal-interval check passes | Works, check missing | Fixed-tick approximation with errors | Missing |
| Precision study (15%) | Spread across seeds matches the SE formula, with discussion | Table present, discussion thin | Single seed only | Missing |
| Sweep and frontier (20%) | 8 × 8 or larger, common random numbers, frontier and cliffs identified and explained | Grid smaller or no common random numbers | Heatmap without interpretation | Missing |
| Analysis (10%) | Every claim backed by a number, a clear recommendation | Mostly supported | Vague | Missing |
