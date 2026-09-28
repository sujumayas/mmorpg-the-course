# MA101 · Lab 01: Build a stat machine

**Week:** 1 ([Functions as machines: input stat, output effect](../lectures/w01-functions-as-machines.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually, discussing with a neighbor is fine

## Objective

Rebuild two real stat pipelines in a spreadsheet, one step per cell, so you can see every intermediate value. Measure how much each input is worth and show that the answer depends on the other inputs. Write inverse formulas that answer a designer's "how much do I need?" questions, and check them against your tables.

By the end you should be able to take any game formula, split it into boxes, and say which box makes an input cheap or expensive.

## Starter materials

- Any spreadsheet program (Google Sheets, LibreOffice Calc or Excel). No code needed.
- The Pokémon stat formula (Generation III onward) from lecture section 2:
  `Stat = floor( ( floor( (2·B + I + floor(E/4)) · L / 100 ) + 5 ) · N )`
  `HP = floor( (2·B + I + floor(E/4)) · L / 100 ) + L + 10`
- The classic-era World of Warcraft warrior pipeline from lecture section 5: `AP = 2 · Str`, `DPS = weaponDPS + AP / 14`, damage per swing `= DPS × weapon speed`.
- Check values:
  - B 100, IV 31, EV 0, neutral, L 50 → 120. Same at L 100 → 236.
  - B 80, IV 31, EV 252, boosting, L 50 → 145.
  - B 130, IV 20, EV 100, lowering, L 50 → 141.
  - HP: B 250, IV 31, EV 252, L 100 → 704.
  - Warrior with a 50 DPS weapon and 210 Strength → 80.00 DPS.

## Steps

### Part A: the stat pipeline (35 minutes)

1. Make input cells for B, IV, EV, L and N. Use data validation so each input stays in its domain (B 1 to 255, IV 0 to 31, EV 0 to 252, L 1 to 100, N one of 0.9, 1.0, 1.1).
2. Build four cells for the four pipeline steps (combine, scale by level, add 5, nature). Then the final stat. Match all four non-HP check values. In Sheets, `FLOOR(x)` rounds down. When you multiply by 1.1, add `0.000001` before flooring to avoid floating-point errors such as `120 × 1.1 = 131.9999`.
3. Build a second block for HP and match its check value.
4. Make a table with levels 1 to 100 down the rows and the stat in one column for IV 31 and in the next for IV 0. Add a third column for the gap. Chart the two stat columns against level.

### Part B: what is an input worth? (25 minutes)

5. At level 50 and at level 100, record how much the stat changes when you raise B by 10, IV by 10, EV by 40, and switch nature from neutral to boosting. Put the eight results in a 4 × 2 table.
6. Write two sentences explaining the pattern. Use the words "parameter" and "multiplier."
7. Find a level at which raising IV by 1 does **not** change the stat. Explain why using the floor step.

### Part C: composition and inverses (30 minutes)

8. Build the warrior pipeline on a new sheet: Strength, AP, DPS, damage per swing. Inputs: Strength, weapon DPS, weapon speed. Match the check value.
9. Write the composed function `DPS(Str)` as one formula. Write its inverse `Str(DPS)`. Use the inverse to find the Strength needed for 90 DPS with a 50 DPS weapon, and confirm it in the pipeline.
10. For the Pokémon stat with B 100, IV 31, EV 0, neutral nature, write the inverse without the floor steps: `L ≈ 100 · (target − 5) / raw`. Use it to estimate the level that first reaches 150, 200 and 230. Check each estimate against your level table and correct it.

### Part D: redesign and write up (at home)

11. Change the stat formula so that IVs add the same number of points at every level. Build it next to the original. Pick your own way of doing this and write the formula down.
12. Compare the original and your version at levels 5, 50 and 100 for IV 0 and IV 31.
13. Write a memo of at most 300 words to a lead designer. Recommend the original or your version for a game where most battles happen at levels 5 to 30. Use at least three numbers from your sheet. Name one player who is hurt by your recommendation.

## Deliverable

Submit one spreadsheet file with sheets named `Stat`, `Warrior` and `Redesign`, plus the memo as a PDF. The spreadsheet must calculate from formulas; pasted values lose marks in the first rubric row.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Pipelines rebuilt (25%) | All check values match; one cell per step; inputs validated to their domains | Check values match, steps merged into one formula | One check value off, cause identified | Values wrong or pasted |
| Input worth analysis (20%) | 4 × 2 table correct; explanation uses parameter and multiplier correctly; floor case found and explained | Table correct, explanation vague | Table has one or two errors | Missing |
| Composition and inverses (25%) | Composed formula and inverse correct; all three level estimates checked and corrected in the table | Formulas correct, one estimate not checked | Inverse wrong but table check done | Missing |
| Redesign (15%) | Working formula, compared at the three levels, behaves as intended | Formula works, comparison thin | Formula has an unintended effect not noticed | Missing |
| Memo (15%) | Clear recommendation, three or more numbers, a named player who loses out | Recommendation with evidence, loser vague | Recommendation without numbers | Missing |
