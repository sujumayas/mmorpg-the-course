# GD203 · Lab 11: The level-sweep balance sheet

**Assigned:** week 11. **Due:** start of week 12. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 11, spreadsheet balancing workshop](../lectures/w11-spreadsheet-balancing-workshop.md). Builds on [lab 10](lab10.md).

## Objective

Turn your lab 10 roster sheet into a balance sheet that checks itself. Every constant lives on one tab, hits-to-kill and encounter cost are checked against target bands at every level from 1 to 30, and a sensitivity table tells you which inputs your balance really depends on.

## Starter materials

- Your lab 10 spreadsheet. If yours is incomplete, use the instructor's [lab 10 reference sheet](lab10-reference.md), released at the start of week 11; using it costs nothing on this lab's rubric.
- The damage model from the lecture's section 2 homebrew example, as a second player weapon to test against:
  - `W(L) = 10 + 2L`, `S(L) = 10 + 2L`, `Def(L) = 10 + 2L`
  - Multiplied model: `damage = W × S / 12`
  - Ratio model: `damage = W × S / Def`
- Target bands (put these on `Inputs`): soldier hits-to-kill 4-7; elite hits-to-kill 15-30; single enemy hit at most 25% of player health; room cost inside its lab 10 budget.

## Steps

1. **Four-tab layout.** Reorganize into `Inputs`, `Levels`, `Checks`, `Scenarios`. Name every input. Color input cells pale yellow. Search your formulas for typed numbers other than 0 and 1 and move each to `Inputs`.
2. **Two damage models.** On `Levels`, add columns for the player's damage per hit under the multiplied model and under the ratio model, plus a switch cell on `Inputs` that selects which one the rest of the sheet uses.
3. **Feel columns.** Add soldier and elite hits-to-kill at every level, using the selected model and the enemy health from lab 10. Round up, as in week 4, since the game deals whole hits.
4. **Checks tab.** One row per level. Columns: soldier hits in band, elite hits in band, max enemy hit under 25% of `H`, and each lab 10 room cost under budget at its level. Conditional formatting green, amber (within 10% of an edge) and red. Add a summary cell that counts red cells.
5. **Charts.** Chart soldier hits-to-kill against level with the target band shaded, once for each damage model. Chart the log of player damage against the log of level and report the slope between levels 10 and 30 (this is `b`). Do the same for enemy health (`a`).
6. **Sensitivity table.** Choose six inputs (for example soldier TTK, soldier cost share, player DPS growth, player health growth, AoE fraction `a`, Strength growth). For each, change it by −10% and +10% and record the change in two outputs: the red-cell count and room D's best-order cost as a share of `H`. Sort by the size of the effect.
7. **Goal seek.** Use goal seek (or a helper column) to find the Strength growth at which the multiplied model's soldier hits-to-kill drops below 4 at level 30. Record the value.
8. **Export.** Write the level-15 row of every role to a CSV tab formatted as a game data file would be (one row per enemy, columns `role, level, hp, dps, hit, interval`).

## Deliverable

- The spreadsheet, with the four tabs, the CSV tab, both charts and the sensitivity table.
- A 400-word robustness report. Answer: Which damage model do you recommend, and what are its measured exponents `a` and `b`? Which two inputs dominate the sensitivity table, and what does that mean for future patches? What Strength growth did goal seek find, and what would you do if a designer asked for more than that?

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Layout and naming (15%) | Four tabs, named inputs, no typed constants, colors consistent | One or two typed constants | Inputs scattered across tabs | No clear structure |
| Models and feel columns (20%) | Both damage models correct, switch works, hits rounded correctly | Minor rounding error | One model wrong | Missing |
| Checks (20%) | All four check columns correct, three-color rule, red-count summary | Checks correct, formatting partial | Checks hardcoded to one level or model | Missing |
| Charts and exponents (15%) | Band shaded, log-log slopes computed and match the lecture's reasoning | Charts present, slopes missing | Raw-stat charts only | Missing |
| Sensitivity and goal seek (20%) | Six inputs, both directions, sorted, goal seek value correct | Five inputs or one direction only | Fewer than four inputs | Missing |
| Report (10%) | Every question answered with numbers from the sheet | Mostly supported | Vague | Missing |
