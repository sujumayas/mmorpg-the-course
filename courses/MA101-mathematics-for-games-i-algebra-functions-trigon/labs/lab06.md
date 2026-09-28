# MA101 · Lab 06: Asymptote audit

**Week:** 6 ([Rational functions and asymptotes: A/(A+K)](../lectures/w06-rational-functions-and-asymptotes.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Audit four damage-mitigation formulas the way a technical designer would before shipping one. For each, find the asymptotes and half point by algebra, confirm them numerically, plot mitigation and effective HP side by side, and flag any input range where the formula misbehaves. Then design your own formula and pass it through the same audit.

## Starter materials

- A spreadsheet program. Optional: Python with matplotlib if you prefer code, as long as your algebra is shown.
- The four formulas from lecture:
  1. League of Legends armor (current wiki, patch V26.10): `m = A / (A + 100)` for `A ≥ 0`; damage multiplier `2 − 100/(100 − A)` for `A < 0`.
  2. Classic World of Warcraft, attacker levels 1 to 59: `m = A / (A + 400 + 85L)`, capped at 75%.
  3. Dota 2 patch 7.20 (November 2018 notes): `m = 0.052A / (0.9 + 0.048A)`.
  4. The exponential comparison curve: `m = 1 − 0.5^(A/K)`.
- The general-form checklist from lecture section 3.
- Health `H = 1,000` for all EHP calculations unless you say otherwise.

## Steps

### Part A: algebra first (30 minutes, on paper)

1. For formulas 1 (positive branch), 2 and 3, write each in the form `(a·A + b) / (c·A + d)`. State `a`, `b`, `c` and `d`. For formula 2, leave `L` as a symbol.
2. For each, find the vertical asymptote, the horizontal asymptote, `m(0)` and the armor that gives 50%. Show the working.
3. For formula 2, find where the 75% cap starts as a function of `L`.
4. For formula 3, find the armor where `m` reaches exactly 100%.
5. For formula 1's negative branch, find the damage multiplier's limit as `A → −∞`.

Photograph or scan this page. It is part of the deliverable.

### Part B: numbers second (35 minutes)

6. Build a sheet with armor from −90 to 600 in steps of 10. Compute `m`, damage taken per 100 incoming and `EHP = H / (1 − m)` for every formula. For WoW, add three columns for attacker levels 10, 30 and 50, with the cap applied using `MIN`.
7. Next to each algebraic result from Part A, put the numerical check (the row where `m` crosses 50%, the value at 600 compared with the asymptote, and so on). Every algebraic claim needs a numerical check beside it.
8. Add an "EHP per armor point" column: `EHP(A + 10) − EHP(A)` divided by 10. Say which formulas give a constant value and which do not, and where.

### Part C: pictures (20 minutes)

9. Plot all mitigation curves on one chart and all EHP curves on another. Clip the EHP chart at 10,000 and note which curve leaves it and at what armor.
10. Draw each horizontal asymptote as a dashed line on the mitigation chart.

### Part D: your formula (at home)

11. Design a mitigation formula for a stat of your choice (armor, resilience, dodge). It must be rational, start at 0, stay below a soft cap you choose, and have a half point that depends on a second variable such as enemy level or hit size.
12. Run it through Parts A to C. Then try to break it: find inputs that hit a vertical asymptote, go negative or exceed 100%. Fix what you find, or argue in one sentence why the input cannot occur in play.
13. Write at most 300 words recommending your formula over League's for a specific game you name (it can be a hypothetical game). Use EHP numbers, not only percentages.

## Deliverable

The Part A working (scan or photo), one spreadsheet with sheets `Numbers`, `Charts` and `Mine`, and the memo as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Algebra (25%) | All asymptotes, half points, cap start and the Dota 100% point correct, with working | One slip, working clear | Several slips or no working | Missing |
| Numerical checks (20%) | Every algebraic claim has a numerical check beside it and they agree | Most claims checked | Few checks | Missing |
| EHP analysis (15%) | Correctly identifies constant slope for the rational form, flat slope past the WoW cap, rising slope for the exponential | Mostly correct, one formula misread | Column computed, no interpretation | Missing |
| Charts (15%) | Both charts readable, asymptotes dashed, clipping noted | Charts present, asymptotes missing | One chart | Missing |
| Own formula and memo (25%) | Formula meets all constraints, a break attempt documented and handled, memo argues with EHP numbers | Formula meets constraints, break attempt shallow | Formula misses a constraint | Missing |
