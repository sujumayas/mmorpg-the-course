# MA101 · Lab 04: Build and tune an XP curve

**Week:** 4 ([Exponentials: growth and the XP curve](../lectures/w04-exponentials-and-the-xp-curve.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually, discussing with a neighbor is fine

## Objective

Rebuild a published exponential XP table from its formula, confirm the "halfway level" rule with your own numbers, then design two XP curves of your own (one exponential, one polynomial) for the same skill and compare how long each level feels to a player.

By the end you should be able to defend a doubling interval with a table, not a hunch.

## Starter materials

- Any spreadsheet program (Google Sheets, LibreOffice Calc or Excel). No code needed.
- The RuneScape XP formula from lecture section 2:
  `xp(L) = floor( (1/4) · Σ_{n=1}^{L−1} floor( n + 300 · 2^(n/7) ) )`
- The approximation `xp(L) ≈ 720.5 · 2^(L/7) − 796`.
- The Pokémon Medium Fast formula `xp(L) = L³` (Generation III and IV games).
- A playtest assumption sheet for the crafting skill from the in-class activity: level cap 40, about 2,000 XP per hour at level 1 and 20,000 XP per hour at level 40.
- Check values: `xp(2) = 83`, `xp(50) = 101,333`, `xp(92) = 6,517,253`, `xp(99) = 13,034,431`.

## Steps

### Part A: rebuild the table (35 minutes)

1. Column A: levels 1 to 99. Column B: the per-level term `floor(n + 300 · 2^(n/7))` for `n` = the level in column A. In Sheets this is `=FLOOR(A2 + 300*POWER(2, A2/7))`.
2. Column C: running total of column B, shifted so that row `L` holds the sum for `n = 1` to `L − 1`. Level 1 is 0.
3. Column D: `xp(L) = FLOOR(C/4)`. Check your four check values. If any is off, fix it before going on. Off-by-one errors in the shift are the usual cause.
4. Column E: the approximation `720.5 · 2^(L/7) − 796`. Column F: the percentage error between D and E. Note the level above which the error stays below 1%.
5. Column G: the ratio `xp(L) / xp(L − 7)`. Plot it against level. Describe in one sentence what it converges to and from which level.

### Part B: see the shape (20 minutes)

6. Make two charts of column D against level: one with an ordinary vertical axis, one with a logarithmic vertical axis. Put them next to each other.
7. Add a horizontal line at `xp(99) / 2` to both charts. Mark the halfway level.
8. Add the Pokémon curve `L³`, scaled so that level 99 matches RuneScape's `xp(99)`, to both charts. Mark its halfway level too.

### Part C: design your own (45 minutes)

9. Build an exponential XP curve for the 40-level crafting skill: `xp(L) = a · (2^((L−1)/d) − 1)`, which gives 0 at level 1. Choose `d` and `a` so that level 2 costs about 100 XP. Record why you picked `d`.
10. Build a polynomial curve for the same skill: `xp(L) = c · (L − 1)^p` with `p` = 2 or 3. Choose `c` so that level 40 needs the same total XP as your exponential.
11. Model XP per hour as exponential between the two playtest points (2,000 at level 1, 20,000 at level 40). Compute the growth factor with the two-point method from lecture section 4.
12. For both curves, compute hours per level: `(xp(L+1) − xp(L)) / rate(L)`. Plot both on one chart.
13. Compute, for each curve, the ratio of hours at level 39 to hours at level 5.

### Part D: write it up (at home)

14. Write a memo of at most 400 words to a lead designer. Recommend one of your two curves for a crafting skill in a game where most players will play for about 60 hours in total. Use at least three numbers from your sheet. Name one player type your recommended curve serves badly and what you would change for them.

## Deliverable

Submit one spreadsheet file with sheets named `Rebuild`, `Charts` and `Design`, plus the memo as a PDF. The spreadsheet must calculate from formulas; pasted values lose marks in the first rubric row.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Table rebuilt from the formula (25%) | All four check values match; formulas, not pasted numbers | Check values match, one formula is hard-coded | One check value off, cause identified | Values wrong or pasted |
| Shape analysis (20%) | Both charts, halfway levels marked, ratio column explained with the level where it settles | Charts and halfway levels correct, ratio explanation vague | Charts present, halfway levels missing or wrong | No charts |
| Curve design (25%) | Both curves hit their constraints; `d`, `a`, `c` and `p` justified; hours-per-level computed correctly | Curves correct, justification thin | One curve misses a constraint | Curves missing |
| Pacing comparison (15%) | Hours chart plus the level-39 to level-5 ratio for both curves, interpreted correctly | Chart and ratios present, interpretation weak | Chart only | Missing |
| Memo (15%) | Clear recommendation, three or more numbers used as evidence, a named player type and a concrete fix | Recommendation with evidence, fix vague | Recommendation without numbers | Missing |
