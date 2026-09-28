# GD102 · Lab 03: Snowball simulator

**Week:** 3 ([Positive feedback loops (snowballing)](../lectures/w03-positive-feedback-loops-snowballing.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Build the three loop models from lecture (independent, capped, zero-sum) in a spreadsheet, reproduce the lecture's tables, then add random income and measure how often an early lead wins. You should leave able to say, with a measured number, whether a snowball in a design comes from the loop gain, the noise or the coupling.

## Starter materials

- Any spreadsheet program (Google Sheets, LibreOffice Calc or Excel). Sheets and LibreOffice recalculate `RAND()` on every edit; that is expected.
- Parameter block (use cells, never type these into formulas):

```
A0 = 12   B0 = 10   r = 0.10   c = 0.10   Cap = 100   T = 30   s (noise) = 0.10
```

- Deterministic check values from lecture section 2:
  - Independent, no cap: turn 10 A = 31.1, B = 25.9, gap 5.2; turn 30 A = 209.4, B = 174.5, gap 34.9; ratio 1.20 throughout; `t_2 = 7.27`; time lead 1.91.
  - Independent, cap 100: turn 22 A = 97.7, B = 81.4; turn 25 both 100.
  - Zero-sum, `c = 0.10`: turn 10 A = 17.19, B = 4.81; turn 13 A = 21.70, B = 0.30; B reaches 0 during turn 14; `A + B = 22` every turn.
- Random check values (measured by the course team with 20,000 runs; your 200-run results should land within about 7 percentage points): share of runs where A is ahead at turn 30 with `A0 = 12`, `B0 = 10`:

| Model | s = 0.05 | s = 0.10 | s = 0.20 |
|---|---|---|---|
| Independent, r = 0.10 | 81% | 67% | 58% |
| Independent, r = 0.20 | 83% | 69% | 59% |
| Zero-sum, c = 0.10 | 93% | 76% | 64% |

## Steps

### Part A: deterministic models (35 minutes)

1. Sheet `Independent`: columns `Turn`, `A`, `B`, `Gap`, `Ratio`, `log10 A`, `log10 B`. `A[t+1] = A[t] × (1 + r)`. Match the check values.
2. Add a cap switch cell (0 or 1). When it is 1, wrap both updates in `MIN(Cap, ...)`. Match the capped check values.
3. Sheet `ZeroSum`: `A[t+1] = A[t] + c × A[t] − c × B[t]` and the mirror for B, both wrapped in `MAX(0, ...)`. Add a `Total` column and confirm it is constant until elimination.
4. Chart each sheet twice: A and B on an ordinary axis, and on a logarithmic axis. Put the four charts on one sheet `Charts` and write one sentence under each pair saying what stays constant and what does not.

### Part B: random income (45 minutes)

5. Sheet `MC_Independent`. Each row is one run, 200 rows. Columns are turns 0 to 30 for A, then 0 to 30 for B. In each A cell after turn 0: `= prev × (1 + r + s × (2 × RAND() − 1))`. Same for B with its own `RAND()`.
6. Add a column `A wins` = 1 if A at turn 30 is greater than B at turn 30. Compute the share of wins. Recalculate five times and record all five shares.
7. Repeat for `s` = 0.05 and 0.20 and for `r` = 0.20. Fill your own version of the check-value table. Mark any cell that falls outside the 7-point tolerance and recalculate before deciding it is wrong.
8. Sheet `MC_ZeroSum`: the same, using the zero-sum update with each player's own random rate (`c_A = c + s × (2 × RAND() − 1)`, and `c_B` likewise) and `MAX(0, ...)`. A wins if A is ahead at turn 30 or B reached 0 first. Record the share for the same three values of `s`.

### Part C: find the knob (20 minutes)

9. Look at your table. Write two sentences on which changes moved the win share a lot and which barely moved it. (Hint: compare the effect of doubling `r` with the effect of doubling `s`.)
10. A designer wants a 20% early lead to win between 60% and 70% of games in the zero-sum model. Find one value of `s` that does it, and one value of `c` with `s = 0.10` that does it. Record each with five recalculated shares.

### Part D: write it up (at home)

11. Write a memo of at most 400 words to a designer who says "our game snowballs, so we're lowering the income rate." Using at least three numbers from your sheets, explain what lowering the gain will and will not change about who wins, and recommend a different knob. Name one thing players would lose if your recommendation were adopted.

## Deliverable

One spreadsheet file with sheets `Independent`, `ZeroSum`, `Charts`, `MC_Independent`, `MC_ZeroSum` and `Results`, plus the memo as a PDF. All values must come from formulas tied to the parameter block.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Deterministic models (25%) | All check values match; cap switch and constant total work; four charts with correct sentences | Values match, one chart or sentence weak | One model off, cause identified | Models missing or wrong |
| Monte Carlo (25%) | 200 runs per case, five recalculations recorded, all cells within tolerance or explained | Within tolerance, recalculations incomplete | Several cells outside tolerance, unexplained | Not attempted |
| Knob analysis (20%) | Correctly identifies that gain barely moves the win share while noise and coupling do; both 60 to 70% settings found | Right conclusion, one setting missing | Conclusion unsupported by numbers | Missing |
| Spreadsheet craft (10%) | Parameter block drives everything; clear labels | One hard-coded number | Several hard-coded numbers | Pasted values |
| Memo (20%) | Direct answer, three or more numbers, a recommended knob and its cost to players | Answer with numbers, cost vague | Answer without numbers | Missing |
