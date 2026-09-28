# MA102 · Lab 01: Sample spaces in a spreadsheet

**Week:** 1 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** part of the problem-set component

**Lecture:** [Week 01, Probability basics: sample spaces and events](../lectures/w01-sample-spaces-and-events.md)

## Objective

Build two sample spaces as spreadsheet grids, count events on them with formulas, and confirm your counts with a simulation. By the end you will have computed advantage, disadvantage and Fire Emblem's two-number "true hit" yourself, and used them to recommend a "roll twice" rule for a game.

## Starter materials

- A spreadsheet program (Google Sheets, LibreOffice Calc or Excel). No add-ons.
- Optional: Python 3 with only the standard library, for step 5.
- The starter workbook layout below. Create it yourself; there is no file to download.

| Sheet | Contents |
|---|---|
| `adv` | A 20 × 20 grid. Row headers 1 to 20 in column A (die b), column headers 1 to 20 in row 1 (die a). A target cell `T` above the grid. |
| `fe` | A 100 × 100 grid. Row headers 0 to 99, column headers 0 to 99. A displayed-hit cell `H`. |
| `sim` | 10,000 rows, two columns of `RANDBETWEEN(1,20)`. |
| `memo` | A text box for your recommendation. |

## Steps

1. **Advantage grid.** In each cell of `adv`, write a formula that returns 1 if `MAX(a, b) >= T` and 0 otherwise. Sum the grid and divide by 400. Use conditional formatting to shade the 1s, and confirm the failing corner has side `T − 1`.
2. **Disadvantage and plain.** Add two more grids, or switch the formula with a mode cell, for `MIN(a, b) >= T` and for `a >= T`. Build a table for T = 1 to 20 with columns plain, advantage, +5, disadvantage. Check at least four values against the lecture's table.
3. **Closed forms.** Next to your counted table, add columns using the formulas `1 − ((T − 1)/20)^2`, `((21 − T)/20)^2` and `MIN(1, MAX(0, (26 − T)/20))`. Add a column that shows the difference between counted and formula values. It must be zero everywhere.
4. **Fire Emblem true hit.** In `fe`, each cell returns 1 if `a + b < 2 × H`. Sum and divide by 10,000. Fill a table for H = 0, 10, 20, ..., 100. Confirm H = 50 → 50.50%, H = 70 → 82.30%, H = 90 → 98.10%. Plot displayed hit against true hit, with the line `y = x` for reference.
5. **Simulation.** In `sim`, compute the kept value `MAX` of each pair, then the fraction of rows at or above T = 18. Recalculate five times and record the five results. How far from 27.75% do they land? (Python users: write a 10-line script that does the same with `random.randint` and 100,000 rows, and report the result.)
6. **Your own rule.** Invent one "combine two rolls" rule not covered in the lecture (for example "roll 2d20 and use the average", or "roll twice, keep the one closer to 10"). Build its grid, compute its success table for T = 1 to 20, and plot it with plain and advantage.
7. **Memo.** Your team's game needs a "focused" buff for a sniper class. It should help most on hard shots (T = 16 to 20). Recommend advantage, +5, or your step-6 rule. Use numbers from your tables.

## Deliverable

One spreadsheet file with the four sheets, the three plots (step 2 curves, step 4 true hit, step 6 comparison), and a memo of 200 to 300 words in the `memo` sheet.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Counting on grids | All grid formulas correct; counted tables match closed forms exactly | Minor errors in one mode, found and explained | Counts do not match or grids missing | 30% |
| Fire Emblem true hit | Full table and plot; all three check values correct | Table correct, plot missing or unlabelled | Wrong event (for example `a + b <= 2H`) and not caught | 20% |
| Simulation | Five runs recorded, spread discussed in a sentence with numbers | Runs recorded, no discussion | No simulation | 15% |
| Own rule | Rule clearly stated, grid and curve correct, one sentence on its feel | Rule computed with a small error | No rule or not computed | 15% |
| Memo | Recommendation uses at least three numbers from the tables and names a trade-off | Recommendation with numbers but no trade-off | No numbers or no recommendation | 20% |
