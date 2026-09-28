# MMO303 · Lab 11: Battle simulator and the exponent of your game

**Week:** 11 ([lecture](../lectures/w11-lanchesters-laws-and-group-combat.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** the simulator assignment (30% of the course grade). This lab's code is the starting point for the week 13 simulator.

## Objective

Build a discrete group-combat simulator, confirm it against Lanchester's square law, then use it to measure how strongly your own rules reward numbers and where healers stall a fight.

## Starter materials

- `lab11-starter.py` (provided on the course site): a 60-line Python skeleton with a `Unit` class (HP, DPS, HPS, role), a `simulate(side_a, side_b, rules)` function stub and a CSV writer. A spreadsheet version, `lab11-starter.xlsx`, is available for students who prefer it; it runs the simulation row by row at `dt = 0.1` s.
- The reference results from the lecture tables (10 against 8, targeting modes, healers).
- Python 3 with `matplotlib`, or any spreadsheet with charts.

## Steps

### Part A: build and verify (45 min)

1. Implement `simulate` with these rules from the lecture: time step 0.01 s; each side's damage per step is the sum of its living damage dealers' DPS × `dt`; "focus" puts all of it on the first living enemy in list order; "spread" divides it equally among living enemies; overkill is lost; deaths are simultaneous within a step; the fight ends when a side is empty or at 300 s.
2. Run the four targeting combinations for 10 against 8 (1,000 HP, 100 DPS). Your survivors must match the lecture table exactly and your times must be within 0.2 s.
3. Add the continuous square-law prediction `sqrt(A₀² − B₀²)` as a column and compare it with your focus/focus survivors for `A₀` from 9 to 20 against `B₀ = 8`. Plot both.

### Part B: measure the exponent (40 min)

4. Add an "area fire, target cap k" rule: each attacker's damage per step is applied in full to up to `k` living enemies. Use area DPS equal to 10% of normal DPS so fights last a few seconds.
5. For `k = 1`, `k = 5` and `k = 1000` (effectively uncapped), run `A₀` from 9 to 20 against `B₀ = 8` and record survivors.
6. For each `k`, find the exponent `e` that best fits `survivors ≈ (A₀^e − B₀^e)^(1/e)`. Try `e` from 1.0 to 2.0 in steps of 0.1 and pick the one with the smallest squared error. Report `e` for each cap.
7. Write two sentences on what your results mean for a designer choosing an area-damage target cap.

### Part C: find the healing threshold (35 min)

8. Give side B 6 damage dealers and 2 healers (healing the lowest-health living ally). Side A has 10 damage dealers.
9. With side A attacking damage dealers first, sweep healing per healer from 0 to 400 HP/s in steps of 10. Record winner, survivors and fight length. Find the threshold where the winner flips. It should fall between 200 and 250 HP/s.
10. Repeat with side A killing healers first. Find the new threshold.
11. Plot fight length against healing for both targeting orders on one chart. Mark the thresholds.

## Deliverable

- Code or spreadsheet, runnable, with a README of up to 10 lines saying how to run it.
- A PDF report of up to 3 pages: the Part A verification table and plot, the Part B exponent table and your two sentences, the Part C chart with both thresholds, and a 200-word design recommendation for a 10-versus-10 battleground in which the designer wants an outnumbered side (8 players) to have a real chance. Name the rule you would change and cite your own simulation numbers.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Simulator correctness (Part A) | All four targeting results match the lecture; square-law comparison plotted and discussed | Most results match, or plot missing | Results do not match and no diagnosis | 30 |
| Exponent measurement (Part B) | Three caps simulated, exponent fitted for each, interpretation correct and specific | Fits done with errors, or interpretation vague | Missing | 25 |
| Healing threshold (Part C) | Both thresholds found, chart clear, stalemate region visible and explained | One threshold found, or chart unclear | Missing | 20 |
| Design recommendation | Uses the pair's own numbers, names a rule, states a cost | Recommendation plausible but not backed by the simulation | Missing | 15 |
| Code quality and README | Readable, runs first time, parameters in one place | Runs with minor fixes | Does not run | 10 |
| **Total** | | | | **100** |
