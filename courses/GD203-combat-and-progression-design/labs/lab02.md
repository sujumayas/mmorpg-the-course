# GD203 · Lab 02: Three damage formulas in one sheet

**Assigned:** week 2. **Due:** start of week 3 (Lab 03 extends this sheet). **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 2, damage formulas](../lectures/w02-damage-formulas.md).

## Objective

Build one spreadsheet that computes damage taken under subtractive, divisive and ratio formulas for any attack and armor, with floors and a two-step pipeline. Use it to show which formula retires weak enemies and to recommend a formula for the course's practice RPG.

## Starter materials

Create a blank spreadsheet with an `Inputs` tab holding these named cells:

| Name | Default | Meaning |
|---|---|---|
| `K` | 100 | Divisive constant, the armor that halves damage |
| `Def0` | 50 | Ratio formula: defender's base defense |
| `Floor` | 0 | Subtractive floor as a fraction of D (0 = none, 0.1 = 10%) |
| `Flat` | 20 | Flat reduction for the pipeline test |
| `Pct` | 0.5 | Percent reduction for the pipeline test |

Hit sizes to test: 10, 20, 50, 100, 200, 500. Armor values: 0 to 300 in steps of 10.

The ratio formula for this lab is `damage = D × Def0 / (Def0 + A)`, where the attacker's stat is fixed at `Def0` so that an armorless defender takes full damage.

## Steps

1. **Grid.** On a `Formulas` tab, lay out armor down the rows and hit sizes across the columns, three times: one block per formula. Each cell holds damage taken.
   - Subtractive: `max(Floor × D, D − A)`, and never below 0.
   - Divisive: `D × K / (A + K)`.
   - Ratio: `D × Def0 / (Def0 + A)`.
2. **Fraction through.** Add a second set of blocks with `damage taken / D`. Check yourself: at A = 50 and D = 100, subtractive gives 0.50 and divisive 0.667.
3. **Charts.** Plot fraction-through against armor for D = 20, 100 and 500 under subtractive, and the divisive curve on the same chart. Plot the ratio curve on a second chart next to divisive with `K = Def0`.
4. **Recognition.** Show algebraically, in a text cell, that the ratio formula here is the divisive formula with `K = Def0`. Confirm it by setting `K = 50` and comparing the two blocks cell by cell (a difference column of zeros is enough).
5. **Swarm versus ogre.** Build a small table: ten hits of 20 against one hit of 200, at armor 0, 10, 20, 50. Check yourself: at A = 20 the swarm deals 0 under subtractive with no floor and 166.7 under divisive; the ogre deals 180 under subtractive.
6. **Floors.** Set `Floor` to 0.1 and record the new swarm totals. Then try a flat floor of 1 (add a switch cell). Write one sentence per floor on what it does to swarms.
7. **Crossover.** For A = 60 and K = 100, find the hit size where subtractive and divisive give equal damage by scanning D from 100 to 250. Compare it with the formula `D = A + K`.
8. **Pipeline order.** For D = 100, compute `(D − Flat) × (1 − Pct)` and `D × (1 − Pct) − Flat`. Then repeat for D = 30 and D = 500. Record which order favours the defender against small hits.

## Deliverable

The spreadsheet and a recommendation memo of about 300 words for the practice RPG (rats, guards and a boss; player armor 0 to 200 over 20 levels). State the formula, constants, floor policy and pipeline order you recommend, and support each choice with at least one number from your sheet.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Formula grid | 20 | All three formulas correct across the full grid, named inputs used throughout | One formula wrong or hard-coded constants | Grid incomplete |
| Charts | 15 | Both charts correct, labeled, readable | One chart missing or unlabeled | No charts |
| Recognition proof | 15 | Algebra correct and confirmed by a zero difference column | Algebra or confirmation only | Missing |
| Swarm, floors, crossover | 20 | All tables correct, crossover matches `A + K` | One part missing or wrong | Two or more missing |
| Pipeline order | 10 | All three hit sizes computed, conclusion stated | Computed without a conclusion | Missing |
| Memo | 20 | Clear recommendation, every choice backed by a sheet number | Recommendation with weak evidence | No recommendation |
