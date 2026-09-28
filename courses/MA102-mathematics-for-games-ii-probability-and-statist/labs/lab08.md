# MA102 · Lab 08: Dice by design

Assigned in week 8 ([lecture](../lectures/w08-dice-sums-and-the-normal-curve.md)). Due at the start of week 9. Counts toward the problem-set grade.

## Objective

Build a small tool that computes the exact distribution of any dice expression, then use it to design and defend a skill-check rule for a tabletop-style RPG.

## Starter materials

- `lab08_starter.ipynb` (on the course page): a Python 3 notebook with numpy and matplotlib, and three empty functions:
  - `die(F)` returns an array of length F filled with `1/F`.
  - `dice_sum(N, F, bonus)` returns `(values, probs)` for NdF + bonus using `np.convolve` N times.
  - `success_curve(values, probs, mode)` returns `P(roll ≥ t)` or `P(roll ≤ t)` for every target t.
- `lab08_starter.xlsx` for spreadsheet users: a 2d6 table of all 36 outcomes, an empty sheet for 3d6 by repeated convolution (one column per die), and a chart template.
- The week 8 interactive, `examples/w08-dice-shapes.html`, for checking values.

## Steps

1. **Build the tool.** Implement the three functions. Test them against the week 8 values: 2d6 gives `P(= 7) = 6/36`, 3d6 gives `P(≤ 10) = 0.5`, 8d6 has mean 28 and SD 4.83.
2. **Check the formulas.** For 1d20, 3d6, 4d8 and 10d4, compare the mean and SD from your arrays to `N(F + 1)/2` and `√(N(F² − 1)/12)`. They must agree to 4 decimal places.
3. **Check the normal approximation.** For 3d6, 8d6 and 20d6, compute `P(sum ≥ μ + 2σ)` exactly and with the normal approximation plus continuity correction. Put the results in a table. At what number of dice does the approximation get within 0.5 percentage points?
4. **Design a check rule.** Characters in your RPG have a skill from 0 to 6. You must meet all four goals:
   - Skill 0 against a standard target succeeds between 25% and 35% of the time.
   - Skill 6 against a standard target succeeds at least 95% of the time.
   - Going from skill 2 to 3 adds more success chance than going from 5 to 6.
   - A "heroic" target exists that skill 6 succeeds at between 40% and 60% of the time.
   Choose the dice expression, the standard target and the heroic target. Plot the success chance against skill for both targets.
5. **Compare with a flat alternative.** Try to meet the same four goals with a single die (1dF + skill). Show which goal a flat rule cannot meet, with numbers.
6. **One damage choice.** A basic attack must average 12. Give two expressions with mean 12, one with SD under 2 and one with SD over 5. For each, compute the chance of dealing 18 or more.

## Deliverable

The notebook or spreadsheet, plus a one-page PDF memo (at most 350 words) to your lead designer that states your check rule, shows the skill-versus-success table for both targets, explains in plain words why a bell curve (or not) fits the game, and names one player experience your rule gives up.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Distribution tool | Convolution correct for any N, F, bonus; tests from step 1 pass | Works for the tested cases only | Wrong or missing | 25% |
| Formula and approximation checks | Tables for steps 2 and 3 complete and correct, clear answer on when the normal curve is good enough | Tables partly complete | Missing | 20% |
| Check rule design | All four goals met and shown numerically, both targets plotted | Three goals met, or numbers unclear | Fewer than three goals met | 30% |
| Flat comparison and damage choice | Correctly shows which goal a flat rule fails; both damage expressions correct with tail chances | One part correct | Missing | 15% |
| Memo | Plain, numbers first, states the trade-off honestly | Understandable but vague on trade-offs | Hard to follow | 10% |
