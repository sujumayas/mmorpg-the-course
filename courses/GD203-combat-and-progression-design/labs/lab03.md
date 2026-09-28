# GD203 · Lab 03: Effective HP and the defensive budget

**Assigned:** week 3. **Due:** start of week 4. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 3, mitigation curves and effective HP](../lectures/w03-mitigation-curves-and-effective-hp.md).

## Objective

Extend your Lab 02 sheet with effective HP. Compare four mitigation models in the percent view and the EHP view, compute EHP against mixed damage types, and find the health-armor split that maximizes EHP for three different price settings. Use the results to recommend a mitigation model for the practice RPG.

## Starter materials

Your completed Lab 02 spreadsheet. If you did not finish it, start a new sheet with an `Inputs` tab holding `K = 100`, `HP = 1000` and `Hit = 250`, and armor values from 0 to 400 in steps of 10.

Four models, all written as the fraction that gets through `f(A)`:

| Model | `f(A)` |
|---|---|
| Divisive | `K / (A + K)` |
| Linear, cap 75% | `max(0.25, 1 − A/100)` |
| Exponential | `0.99^A` |
| Divisive, cap 75% | `max(0.25, K / (A + K))` |

## Steps

1. **EHP tab.** For each model and armor value compute mitigation `1 − f`, EHP `HP / f`, and hits to die `ceil(EHP / Hit)`. Check yourself: divisive at A = 300 gives 75.0%, 4,000 EHP and 16 hits; exponential at A = 100 gives 63.4% and 2,732 EHP.
2. **Marginal value.** Add a column per model for "EHP from the last 10 armor." Describe in one sentence each whether that column is constant, rising, falling or zero, and over which range.
3. **Two charts.** Chart mitigation against armor for all four models, and EHP against armor for all four. Put them side by side. Clamp the EHP axis at 20,000 so the exponential curve does not flatten the others.
4. **Mixed damage.** Build a calculator with inputs HP, armor, fire resistance (both divisive with `K = 100`) and physical share `s`. Compute `f_total = s × f_phys + (1 − s) × f_fire` and `EHP = HP / f_total`. Check yourself: 1,000 HP, 120 armor, 0 fire resistance and `s = 0.7` give about 1,618 EHP. Adding 50 fire resistance gives about 1,930. Adding 50 armor instead gives about 1,788.
5. **Budget optimizer.** A character starts with 500 HP and 0 armor and has 100 budget points. For each price setting below, list `x` (points into health) from 0 to 100, compute HP, armor and EHP, and find the best `x`.

   | Setting | One point buys | Check value |
   |---|---|---|
   | A | 50 HP or 5 armor | best x = 55, EHP 10,562.5 |
   | B | 50 HP or 10 armor | best x = 50, EHP 18,000 |
   | C | 100 HP or 5 armor | best x = 57 or 58 (tie), EHP 19,530 |

6. **Verify the rule.** For each setting, check that at the best split `HP / h ≈ (A + K) / a`, where `h` and `a` are HP and armor per point.
7. **Cap test.** Repeat setting A with the capped divisive model. Does the best split change? Explain why or why not in one sentence.

## Deliverable

The spreadsheet and a memo of about 400 words recommending a mitigation model for the practice RPG. Say what return the next point of defense should give at level 20, which model produces it in EHP, what prices for health and armor you would set, and what tank build those prices lead to. Support each claim with a number from your sheet.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| EHP tab and marginal values | 20 | All four models correct, marginal column described correctly | One model wrong or descriptions missing | Tab incomplete |
| Paired charts | 15 | Both charts correct, same axis range, clearly labeled | One chart missing or unreadable | No charts |
| Mixed-damage calculator | 15 | Correct, check values match, inputs are live | Correct but hard-coded | Missing or wrong |
| Budget optimizer and rule check | 25 | All three settings correct, rule verified, cap test explained | One setting wrong or rule not checked | Two or more settings missing |
| Memo | 25 | Recommendation tied to EHP evidence and a stated build target | Recommendation with little evidence | No recommendation |
