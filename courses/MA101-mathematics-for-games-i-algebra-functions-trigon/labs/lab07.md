# MA101 · Lab 07: Stat curves with caps and floors

**Week:** 7 ([Piecewise functions, caps and floors](../lectures/w07-piecewise-caps-and-floors.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Reproduce a shipped stat curve as a piecewise function, find its soft caps from the per-point gain, then design a curve of your own to a brief and prove, with numbers, where players will stop investing. You will also find one bug caused by clamp order and fix it.

## Starter materials

- A spreadsheet program. Optional: Python with matplotlib, as long as each formula is visible.
- The Elden Ring HP formulas from lecture section 2 (Fextralife wiki, retrieved September 2026, community-derived, floored to an integer):
  - Vigor 1 to 25: `300 + 500((V − 1)/24)^1.5`
  - Vigor 26 to 40: `800 + 650((V − 25)/15)^1.1`
  - Vigor 41 to 60: `1450 + 450(1 − (1 − (V − 40)/20)^1.2)`
  - Vigor 61 to 99: `1900 + 200(1 − (1 − (V − 60)/39)^1.2)`
- The straight-line model through `(25, 800)`, `(40, 1450)`, `(60, 1900)`, `(99, 2100)`.
- The Diablo II: Lord of Destruction resistance rule: `effective = clamp(listed − penalty, −100, 75 + bonusMax)`, penalty 0 / 40 / 100 for Normal / Nightmare / Hell, `bonusMax` at most 20.
- Test values to check your sheet: wiki HP at Vigor 30 = 994, 50 = 1704, 80 = 2015.

## Steps

### Part A: reproduce and read (40 minutes)

1. Make a sheet with Vigor from 1 to 99. Add a column for wiki HP using a nested `IF` (or `IFS`) that picks the right piece, then `FLOOR`. Check the three test values above before going on.
2. Add a column for the straight-line model (Vigor 25 and up) and a column for the difference between model and wiki.
3. Add a column "gain" `= HP(V) − HP(V − 1)` for the wiki formula.
4. Chart total HP and gain on two separate charts with the same x-axis. Mark Vigor 40 and 60.
5. In two or three sentences, say where the largest single-point drop in gain is, and how big it is. Compare it with the drop in the straight-line model at the same breakpoint.

### Part B: the clamp-order bug (20 minutes)

6. Build a small table for Diablo II resistance with listed resistance from −60 to 200 in steps of 20, for all three difficulties, with `bonusMax = 0`.
7. Add a second block with the wrong order, `clamp(listed, −100, 75) − penalty`.
8. Highlight every cell where the two differ. Write one sentence per difficulty describing what a player would experience under the buggy version.

### Part C: design to a brief (at home)

Brief: a "Focus" stat raises mana from 100 (Focus 10) to between 400 and 500 (Focus 80). The team wants most builds to stop between Focus 35 and 50, but a pure caster at 80 must still feel rewarded.

9. Write a continuous piecewise-linear function with at least two breakpoints. Give the per-point gain on each piece. No piece may have zero gain.
10. Build it in the sheet, chart total and gain, and check continuity at every breakpoint with a formula (not by eye).
11. Replace one straight piece with a curved one (a power curve like the Elden Ring pieces) that meets the same endpoints. Show the gain column tapering instead of stepping.
12. Write at most 250 words: where will players stop, why, and what the pure caster gets for Focus 50 to 80 in mana per point. Use numbers from your sheet.

## Deliverable

One spreadsheet with sheets `EldenRing`, `ClampOrder` and `Focus`, containing both charts per sheet where asked, and the memo as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Reproduction (25%) | Wiki formula matches all test values, model and difference columns correct, charts labelled with breakpoints | One small error, test values still match | Test values do not match or charts missing | Missing |
| Reading the gain (15%) | Correctly locates and sizes the largest drop and compares it with the model | Locates it, size or comparison wrong | Vague description | Missing |
| Clamp-order bug (20%) | Both blocks correct, every difference highlighted, player-facing consequence stated for each difficulty | Tables correct, consequences thin | One table wrong | Missing |
| Focus design (25%) | Continuous, meets range and brief, gain never zero, continuity checked by formula, curved piece meets endpoints | Meets brief, one check missing | Discontinuous or misses the range | Missing |
| Memo (15%) | Argues from sheet numbers, predicts stopping point convincingly | Uses some numbers | Opinion without numbers | Missing |
