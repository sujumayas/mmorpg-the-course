# GD203 · Lab 06: Crits, breakpoints and Monte Carlo

**Assigned:** week 6. **Due:** start of week 7. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 6, critical hits and variance](../lectures/w06-critical-hits-and-variance.md). **Interactive:** [Crit hits-to-kill](../examples/w06-crit-hits-to-kill.html), for checking your numbers.

## Objective

Compute exact hits-to-kill distributions for crit builds with the binomial method, check them against a 10,000-fight simulation, map where crits speed up or slow down kills, and redesign a crit system to meet a variance target at the hit counts your game uses.

## Starter materials

Create these yourself in any spreadsheet tool. All numbers are fictional.

**Builds.** Each build averages 40 damage per hit.

| Build | Crit chance c | Multiplier m |
|---|---|---|
| Steady | 0 | — |
| Flicker | 0.30 | 1.5 |
| Gambler | 0.10 | 4.0 |

**Targets.** Health 80, 100, 120, 160, 200, 400 and 2,000.

**Check values.** Flicker's base damage is `40 / (1 + 0.3 × 0.5) = 34.78`. Gambler's is `40 / (1 + 0.1 × 3) = 30.77`.

## Steps

1. **Per-hit statistics.** For each build compute base damage, expected damage (should be 40), standard deviation and per-hit CV. Check yourself: Flicker's CV is about 0.199.
2. **Exact distribution.** For each crit build and each target up to 400 health, compute `P(kill by hit n)` using `BINOM.DIST` and the kill condition `d_B × (n + k × (m − 1)) ≥ H`. Derive `P(kill on hit n)` and the mean hits-to-kill. Compare with Steady's `ceil(H / 40)`.
3. **Monte Carlo.** On a new tab, simulate 10,000 fights for Flicker against the 120-health target. Each row draws random numbers for up to 10 hits (`RAND() < c` means a crit), keeps a running total, and records the hit on which it passes 120. Compare the simulated distribution with step 2. Report the largest difference in any bar, in percentage points.
4. **Help or hurt map.** For target health from 40 to 400 in steps of 5, chart Steady's hits-to-kill and each crit build's mean hits-to-kill on one chart. Shade where each crit build is faster than Steady. Write one sentence per build describing the pattern.
5. **Fight-length variance.** For each crit build, compute the CV of total damage for fights of 2, 5, 20 and 100 hits. Mark the fight lengths where the CV is above 0.15.
6. **Redesign.** Your game's design goal is "crits are noticeable in 3-hit PvP exchanges (fight CV at least 0.15) but mean hits-to-kill against the 120-health and 200-health targets is never more than 3% slower than Steady." First test whether any `c` and `m` (average stays 40) can meet it. Both targets sit exactly on Steady's breakpoints (`3 × 40` and `5 × 40`), so explain what you find using lecture section 2. Then change each of those two enemies' health by at most 10 points, and choose `c` and `m` that meet the goal against the new values. Show the numbers.

## Deliverable

The spreadsheet file (or a share link), the help-or-hurt chart, and a design note of about 350 words. The note must report the Monte Carlo check, describe the help-or-hurt pattern in terms of breakpoints, and justify your redesign with the fight CV and the mean hits-to-kill.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Per-hit statistics | 10 | All values correct | One build wrong | Missing |
| Exact distributions | 25 | Correct kill condition, distributions sum to 1, means correct | Minor errors in one build | Average damage used instead of distribution |
| Monte Carlo check | 15 | 10,000 fights, comparison reported, difference explained | Fewer fights or no comparison | Missing |
| Help-or-hurt map | 15 | Chart correct, pattern tied to breakpoints | Chart without explanation | Missing |
| Variance and redesign | 20 | Fight CVs correct; the on-breakpoint conflict explained; redesign meets both goals after the health change, with evidence | One goal met, or conflict not explained | No redesign |
| Design note | 15 | Clear, numeric, answers all three prompts | Thin in one area | Restates the lab |
