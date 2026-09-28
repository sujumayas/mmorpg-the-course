# GD102 · Lab 02: Stock-and-flow spreadsheet

**Week:** 2 ([Stocks and flows](../lectures/w02-stocks-and-flows.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Turn two stock-and-flow diagrams into working spreadsheet simulations, prove they are right with the bathtub check, then design a capped energy system for a named target player and defend its time to fill with numbers from your own sheet.

## Starter materials

- Any spreadsheet program (Google Sheets, LibreOffice Calc or Excel). No code needed.
- Model A, the rested pool, from lecture section 3. One row per day, days 0 to 60. Inflow `i = 15%` of a level per day (rest area), cap 150%. The player logs in every `N` days and earns base experience `X = 30%` of a level per hour for `H` hours; the bonus used is `min(R, X × H)`.
- Model B, the town, from lecture section 4. One row per day, days 0 to 60. `S[t+1] = S[t] + I − r × S[t]` with `I = 100`, `r = 0.05`, `S[0] = 0`.
- Check values. Model A with `N = 14`, `H = 5`: pool at day 10 = 150%, wasted inflow by day 14 = 60%, wasted share over one complete cycle = 28.6%. Model B: day 1 = 100, day 3 = 285.25, day 14 ≈ 1,024.7, day 30 ≈ 1,570.7, equilibrium 2,000.
- A parameter block you must use (so nothing is typed into formulas directly). Put these in cells at the top of each sheet with labels:

```
Model A:  i (per day) = 15%   Cap = 150%   N (days) = 14   H (hours) = 5   X (per hour) = 30%
Model B:  I (per day) = 100   r (per day) = 0.05   S0 = 0
```

## Steps

### Part A: the rested pool (40 minutes)

1. Columns: `Day`, `Login?` (1 if `Day > 0` and `MOD(Day, N) = 0`), `R start`, `Inflow`, `Stored` = `MIN(Inflow, Cap − R start)`, `Wasted` = `Inflow − Stored`, `Bonus used` = `Login? × MIN(R start + Stored, X × H)`, `R end` = `R start + Stored − Bonus used`. The next row's `R start` is this row's `R end`.
2. Check your sheet against the check values. Then add a column `Bathtub check` = `R end − R start − (Stored − Bonus used)`. It must be 0 in every row. Fix anything that is not.
3. Chart `R end` as a line and `Stored`, `Wasted` and `−Bonus used` as stacked bars on a second chart with the same day axis.
4. Build a small table of wasted share over days 0 to 60 for `N` = 3, 7, 10, 14, 20 and 30. Compare each with the formula `W(N) = max(0, 1 − Cap/(i × N))`. Explain in two sentences any row where your simulated share over 60 days differs from `W(N)` (hint: incomplete cycles at the end of the window).

### Part B: the town (25 minutes)

5. Columns: `Day`, `S`, `Inflow` = `I`, `Outflow` = `r × S`, `Net` = `Inflow − Outflow`, next `S` = `S + Net`. Add the same bathtub check.
6. Chart `S` and a horizontal line at `I / r`. Find the first day `S` passes 50% and 90% of equilibrium. Compare with the formula `t = ln(1 − p) / ln(1 − r)` for fraction `p`.
7. Change `S0` to 4,000. Describe what happens and why, using the words "outflow" and "equilibrium."
8. Double `I` and separately double `r`. Record the new equilibrium and the day `S` passes 90% of it in each case. Which change moves the equilibrium, and which changes the speed?

### Part C: design an energy system (35 minutes)

9. Pick one target player and write them down in one line, for example "plays on the bus twice a day, 8:00 and 18:00" or "plays one long session every Saturday."
10. Copy Model A to a new sheet `Energy`. Change units to energy points and steps to hours. Choose an inflow per hour, a cap and an energy cost per play session so that your target player wastes at most 10% of their inflow, and a player who checks in half as often wastes at least 30%.
11. Record `T_fill`, the wasted share for your target player, and the wasted share for the half-as-often player, all computed by the sheet.

### Part D: write it up (at home)

12. Write a memo of at most 400 words to a producer who asked "why not just remove the cap?" Use at least three numbers from your `Energy` sheet. Explain what the cap asks your target player to do, what removing it would change about how often they return, and one player type your design treats badly.

## Deliverable

One spreadsheet file with sheets `Rested`, `Town` and `Energy`, plus the memo as a PDF. All values must come from formulas tied to the parameter block; a changed parameter must update every chart.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Rested model (25%) | All check values match; bathtub check is 0 in every row; both charts correct; waste table explained | Values match, one chart or explanation weak | One check value off, cause identified | Values wrong or model missing |
| Town model (20%) | Equilibrium, 50% and 90% days match formulas; S0 and parameter experiments explained correctly | Numbers right, explanations thin | Equilibrium right, experiments missing | Missing |
| Energy design (25%) | Both waste constraints met and shown by the sheet; parameters justified for the named player | Constraints met, justification vague | One constraint missed | Missing |
| Spreadsheet craft (10%) | Parameter block drives everything; labeled columns and axes | One hard-coded number | Several hard-coded numbers | Pasted values |
| Memo (20%) | Direct answer to the producer, three or more numbers, a named player type treated badly | Answer with numbers, weak on trade-offs | Answer without numbers | Missing |
