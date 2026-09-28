# MA101 · Lab 05: The "how many until" calculator

**Week:** 5 ([Logarithms: "how many levels until…"](../lectures/w05-logarithms-how-many-levels-until.md))
**Time:** one 2-hour lab session plus up to 1.5 hours at home
**Work:** pairs

## Objective

Build a spreadsheet calculator that answers player questions about exponential systems with logarithms, and prove every answer correct by brute-force counting. You will invert three curves: an XP table, a building price and a decaying rank score.

The skill you are practicing is the one a balance designer uses daily: turn a player's "how many more?" into a one-cell formula, then check it before trusting it.

## Starter materials

- Any spreadsheet program. Sheets and Excel both provide `LN`, `LOG` (with a base argument), `LOG10`, `FLOOR` and `CEILING`.
- Your Lab 04 spreadsheet (the RuneScape `Rebuild` sheet), or rebuild the XP column from the lecture formula.
- The Cookie Clicker price model: next price `p · 1.15^M`, where `M` is the number owned. Base costs: Cursor 15, Grandma 100, Farm 1,100, Mine 12,000.
- A rank-decay rule for a fictional arena game: a player loses 3% of their rank points for each day they do not play.
- Formulas from lecture: `N(C) = floor( ln( 1.15^M + 0.15·C/p ) / ln(1.15) ) − M`, `L ≈ 7 · log_2((xp + 796)/720.5)` and `n = ln(T/a) / ln(b)`.

## Steps

### Part A: the building calculator (35 minutes)

1. Make input cells for budget `C`, base cost `p`, growth rate `r` and owned `M`.
2. In one cell, compute `N(C)` with the logarithm formula, generalized to growth rate `r`.
3. Brute-force check: build a column that lists the price of each next building and a running total, then count how many rows fit in the budget with `COUNTIF`. Compare with step 2 for at least 10 input combinations, including `M > 0` and a budget exactly equal to a running total. Log any case where they disagree and explain it (floating-point rounding at an exact boundary is the usual culprit).
4. Add a "doubling table": `C` = 1,000, 2,000, 4,000, … up to about 10⁹. Next to it, `N(C)` and the difference from the row above. Confirm the difference settles at `ln 2 / ln(1 + r)` rounded up or down.

### Part B: the level calculator (25 minutes)

5. Given an XP value, find the exact RuneScape level with a lookup against your XP column (`MATCH` with approximate match, or `VLOOKUP`).
6. In the next cell, estimate the level with `7 · log_2((xp + 796)/720.5)`. Tabulate exact versus estimated for XP = 1,000, 10,000, 100,000, 1,000,000, 5,000,000 and 13,034,431.
7. Answer, with a formula that uses logarithms only: a player has 2,500,000 XP and gains 90,000 XP per hour. How many hours until level 99? Check against the exact table.

### Part C: the decay calculator (20 minutes)

8. With starting points `S`, decay rate `q` per day and threshold `T`, compute the first whole day on which the score falls below `T`: `ceiling( ln(T/S) / ln(1 − q) )`, with care at exact boundaries.
9. Check it by building a day-by-day column. Test `S = 2,000`, `q = 3%`, `T = 1,000` (answer: day 23) plus three cases of your own.
10. Compute the half-life for `q` = 1%, 3%, 5% and 10%. Compare with the rule of 70 and note where it drifts.

### Part D: player-facing answers (at home)

11. Write five questions a player might ask in chat ("How many Farms can I get with 3 million cookies if I already have 12?"), each answered by your calculator. For each, give the formula cell and the brute-force check cell side by side.
12. Write at most 250 words on one place in a game you play where showing players the logarithm (a level, a rank) hides a large difference in the underlying quantity. Use a number from your calculator to make the point.

## Deliverable

One spreadsheet with sheets `Buildings`, `Levels`, `Decay` and `Questions`, plus the short write-up as a PDF. Both partners' names on both files.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Building calculator (25%) | Log formula and brute force agree on 10+ cases including `M > 0`; every disagreement explained | Agree on most cases, one unexplained mismatch | Formula works only for `M = 0` | Missing or wrong |
| Doubling table (15%) | Differences settle at `ln 2 / ln(1+r)` and the student says why | Table correct, explanation missing | Table incomplete | Missing |
| Level calculator (20%) | Exact and estimated levels tabulated, hours-to-99 answered with logs and checked | Table correct, hours answer unchecked | Only exact lookup works | Missing |
| Decay calculator (15%) | Correct first day for all cases, boundary handled, half-life table compared with rule of 70 | Correct, rule of 70 comparison missing | Off-by-one on the day | Missing |
| Player questions and write-up (25%) | Five varied questions with formula and check side by side; write-up uses a computed number to make a clear point | Five questions, write-up general | Fewer than five questions | Missing |
