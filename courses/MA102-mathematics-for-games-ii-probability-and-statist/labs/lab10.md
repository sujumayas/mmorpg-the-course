# MA102 · Lab 10: Design a bad-luck protection rule

Assigned in week 10 ([lecture](../lectures/w10-pseudo-random-distribution-and-pity-timers.md)). Due at the start of week 11. Counts toward the problem-set grade. Your code is reused in the week 11 Monte Carlo lab.

## Objective

Implement independent rolls, pseudo-random distribution (PRD) and pity counters for the same nominal rate, compute their gap distributions exactly, and choose a rule for a real design brief with numbers to back the choice.

## Starter materials

- [`starter/lab10_starter.py`](starter/lab10_starter.py). A Python 3 script (paste it into a notebook if you prefer) with numpy and matplotlib imported and these empty functions:
  - `prd_gap_dist(C)` returns a list whose entry `n − 1` is `P(first proc on attempt n)` under `p_n = min(1, C × n)`.
  - `pity_gap_dist(base, soft_start, step, hard)` returns the same list for a soft-and-hard pity rule. Setting `step = 0` gives hard pity only.
  - `mean_sd(dist)` returns the mean and standard deviation of a gap distribution.
  - `solve_C(p)` finds `C` by bisection.
- A spreadsheet version, which you build yourself from this layout, with one row per attempt and columns for the per-attempt chance, survival and landing probability. Bisection is done by hand with a goal-seek cell.
- The week 10 interactives, [`examples/w10-prd-streaks.html`](../examples/w10-prd-streaks.html) and [`examples/w10-gacha-pity.html`](../examples/w10-gacha-pity.html), to check your values.

## Steps

1. **Exact PRD distribution.** Implement `prd_gap_dist(C)`. With `C = 0.084744`, confirm the mean gap is 4.00, the SD is 1.90, and the longest possible gap is 12.
2. **Solve C.** Implement `solve_C(p)` by bisection on `[0, p]` using the mean gap. Reproduce the published constants for 10%, 20%, 30% and 50% to four significant figures. Report how many bisection steps you needed for six-digit accuracy.
3. **Compare shapes.** For `p = 0.2`, plot the independent (geometric) and PRD gap distributions on one chart. Report P(gap ≥ 10) and P(back-to-back success) for both.
4. **Pity rules.** Implement `pity_gap_dist`. Reproduce the week 10 table: 69.70 expected pulls for hard pity only at 90 with base 0.6%, and 62.30 for the community soft-pity model. Report the median in each case.
5. **Seeded sanity check.** Simulate 10,000 gaps for PRD at 25% with `np.random.default_rng(1010)`. Compare the simulated mean and SD with step 1. They should agree to within about 0.05.
6. **Design brief.** A dungeon boss drops a crafting reagent at 4% per kill. Players need one to progress their main quest line. The producer wants "no player stuck for more than 60 kills, and the average should still feel like 1 in 25". Propose two rules (for example, hard pity at 60, and a soft ramp starting at kill 30). For each, compute the expected kills, median, 95th percentile and the share of players who reach the cap. Recommend one.

## Deliverable

One notebook or spreadsheet plus a memo of at most 400 words to the lead designer. The memo must contain:

- The C values from step 2 and the comparison numbers from step 3.
- A table of your two proposed rules from step 6 with all four statistics.
- Your recommendation and one sentence on what the rule costs (for example, a lower effective rarity or the state you now store per player).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Exact distributions | PRD and pity distributions correct, week 10 values reproduced to stated precision | Minor numerical errors, or one function incorrect | Distributions wrong or missing | 30% |
| Solving C | Bisection correct and reproduces published constants, step count reported | Constants close but method unclear | Constants copied, not computed | 15% |
| Comparison and simulation check | Plot and tail numbers correct, simulation agrees with exact values and the agreement is explained | Numbers present with one error or no explanation | Missing or wrong | 20% |
| Design brief | Two defensible rules, all four statistics correct, recommendation tied to the producer's targets | Rules reasonable but a statistic missing or wrong | Rule arbitrary or unsupported | 25% |
| Memo clarity | Under 400 words, numbers first, a designer could act on it | Understandable but padded or missing a number | Hard to follow | 10% |
