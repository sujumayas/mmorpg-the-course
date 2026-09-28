# GD203 · Lab 09: Item budget audit

**Assigned:** week 9. **Due:** start of week 10. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 9, item budgets and stat weights](../lectures/w09-item-budgets-and-stat-weights.md).

## Objective

Audit a 12-item loot table with a budget sheet, find the items that are off budget (some of them hidden by cheap stats or unpriced procs), compute stat weights from a small DPS model by finite differences, and re-derive the price list. By the end you should be able to explain, with numbers, why a stat weight is a slope at one gear set and not a fixed property of the stat.

## Starter materials

Build these in any spreadsheet tool. All items and numbers are fictional.

**Price list and budgets.** Str 1.0, Sta 0.5, Crit 0.8, Haste 0.8 points per unit. Budget is 100 points at item level 50 and 110 at item level 55. Tolerance is ±5%.

**Loot table.**

| Item | ilvl | Str | Sta | Crit | Haste | Effect |
|---|---|---|---|---|---|---|
| Ironbark Helm | 50 | 45 | 60 | 32 | 0 | — |
| Gale Hood | 50 | 40 | 0 | 0 | 75 | — |
| Keen Visor | 50 | 50 | 0 | 50 | 25 | — |
| Warden Pauldrons | 50 | 30 | 100 | 0 | 25 | — |
| Duelist Mantle | 50 | 45 | 0 | 40 | 30 | — |
| Plain Gloves | 50 | 50 | 50 | 20 | 0 | — |
| Stormgrip | 55 | 50 | 0 | 45 | 30 | — |
| Oathbound Belt | 55 | 40 | 80 | 25 | 0 | — |
| Runner Boots | 55 | 46 | 0 | 0 | 80 | — |
| Emberband | 55 | 60 | 0 | 40 | 0 | 10% chance on hit to deal 200 damage |
| Tidewalker Legs | 55 | 50 | 50 | 0 | 50 | — |
| Lucky Charm | 55 | 40 | 40 | 0 | 0 | 20% chance on hit to deal 250 damage |

**DPS model for the reference build.** The build attacks once per second.

```
DPS = 100 × (1 + Str / 200) × (1 + Crit / 400) × (1 + Haste / 400)
```

Crit / 400 is crit chance, and a crit doubles damage, so `1 + Crit / 400` is the expected damage multiplier. Haste / 400 is the attack speed bonus.

## Steps

1. **Budget tab.** Enter the loot table. Add columns for raw stat total, budget cost (stats only), budget for the item level and percent of budget. Check yourself: Keen Visor costs 110 (110%), Oathbound Belt costs 100 against a budget of 110 (90.9%), Tidewalker Legs costs 115 (104.5%).
2. **Flag.** Mark each item on, over or under budget using the ±5% tolerance. Sort by raw total and by percent of budget side by side. Name the item whose ranking changes the most between the two sorts.
3. **Weights tab.** Compute DPS for a balanced gear set (Str 200, Crit 100, Haste 100). Then add 10 of one stat at a time and compute the weight as `ΔDPS / 10`. Check yourself: baseline 312.5 DPS; weights Str 0.781, Crit 0.625, Haste 0.625. Normalize to Str and confirm you get the lecture's prices, 0.8 for both Crit and Haste.
4. **Procs.** Price each proc by expected value. Expected proc DPS is `chance × damage × hits per second`. Convert to points by dividing by the Str weight from step 3. Add the result to each item's cost. Check yourself: Emberband's proc is 20 DPS, worth 25.6 points, and the item is now 106.9% of budget. Lucky Charm's proc is worth 64 points, which puts a 54.5% item at 112.7%.
5. **Weights move.** Repeat step 3 for a crit-heavy gear set (Str 200, Crit 200, Haste 50). Check yourself: baseline 337.5 DPS, normalized Crit 0.667 and Haste 0.889. In two sentences, explain why the stat this build already has the most of is now worth the least, using the form of the DPS formula.
6. **Re-derive prices.** Suppose 60% of players wear the balanced set and 40% the crit-heavy set. Compute share-weighted normalized prices for Crit and Haste. Recompute every item's percent of budget with the new prices. Which items change verdict?
7. **Fix list.** For each item outside tolerance under the original prices, propose the smallest stat change that brings it within ±5% while keeping its identity. For each proc item, decide whether to lower the proc or the stats.
8. **Ship one on purpose.** Choose one item you would leave overbudget and write its justification in one sentence (drawback, source, narrow use).

## Deliverable

The spreadsheet (or a share link) with budget, weights and fix-list tabs, and an audit memo of about 300 words for the design lead. It should list the problem items with their percent of budget, explain what hid each one, report how the weights changed between gear sets, and give your recommendations.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Budget sheet | 20 | All costs, budgets and flags correct, both sorts shown | One or two errors | Costs wrong or missing |
| Stat weights | 20 | Both gear sets computed by finite difference, normalized, match check values | One gear set correct | Weights asserted, not computed |
| Proc pricing | 15 | Both procs priced by expected value and added to cost | One proc priced | Procs ignored |
| Re-derived prices | 15 | Share-weighted prices computed and verdict changes listed | Prices computed, effect not traced | Missing |
| Fix list and justified exception | 15 | Minimal fixes that keep identity, one defended exception | Fixes change item identity or exception undefended | Missing |
| Audit memo | 15 | Clear, numbered findings with percentages and causes | Findings without causes | Restates the lab |
