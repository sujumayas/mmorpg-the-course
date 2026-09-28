# GD203 · Lab 04: The breakpoint table

**Assigned:** week 4. **Due:** start of week 5. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 4, time-to-kill and time-to-die](../lectures/w04-time-to-kill-and-time-to-die.md). **Interactive:** [Breakpoint staircase](../examples/w04-breakpoint-staircase.html), for checking your numbers.

## Objective

Build a hits-to-kill and time-to-kill matrix for a weapon set against an enemy roster. Find every matchup that sits within 5% of a breakpoint, retune enemy health so key matchups sit in the middle of their step, and compute the safety ratio for each fight. By the end you should be able to change one weapon's damage and see at a glance which matchups changed and which did not.

## Starter materials

Create these yourself in any spreadsheet tool. All numbers are fictional and belong to the course's practice RPG.

**Weapons (player).**

| Weapon | Damage per hit | Interval (s) |
|---|---|---|
| Shortsword | 12 | 0.8 |
| Spear | 18 | 1.2 |
| Warhammer | 45 | 2.5 |
| Dagger | 7 | 0.45 |
| Longbow | 30 | 1.6 |

**Enemies.**

| Enemy | Health | Armor mitigation | Damage per hit | Interval (s) |
|---|---|---|---|---|
| Rat | 24 | 0% | 3 | 1.0 |
| Goblin | 60 | 0% | 8 | 1.2 |
| Bandit | 90 | 10% | 12 | 1.0 |
| Orc | 180 | 20% | 20 | 1.5 |
| Troll | 400 | 0% | 30 | 2.0 |
| Knight | 144 | 25% | 16 | 1.2 |

**Player.** 200 health, 15% mitigation.

**Design goals (from the lead designer).** A goblin should die in about 4 seconds to the shortsword. An orc should take between 7 and 11 seconds for every weapon. No weapon should kill a knight more than 40% faster than the shortsword does.

## Steps

1. **Inputs tab.** Enter both tables, the player values and the design goals. Name every constant. No formulas on this tab.
2. **Effective damage.** For each weapon-enemy pair, compute damage per hit after the enemy's mitigation. Check yourself: the spear against the bandit deals `18 × 0.9 = 16.2`.
3. **Hits-to-kill matrix.** Compute `ceil(H / d_eff)` for all 30 pairs. Guard against floating-point error by subtracting a small value (for example `CEILING(H / d − 1E-9, 1)`). Check yourself: shortsword against goblin is 5 hits.
4. **TTK matrix.** Compute `(hits − 1) × interval`. Next to it, compute the smooth estimate `H × interval / d_eff` and the percentage gap. Use conditional formatting to shade gaps above 25%.
5. **Breakpoint margins.** For each pair compute two numbers. The damage increase needed to remove one hit, `H / (hits − 1) / d_eff − 1`. The damage decrease that would add one hit, `1 − H / hits / d_eff`. Flag any pair where either is under 5%. List the flagged pairs.
6. **Time-to-die and safety ratio.** Compute the player's TTD against each enemy using the player's health and mitigation, and the safety ratio `R = TTD / TTK` for each weapon-enemy pair. Shade `R < 1` red and `R > 8` grey.
7. **Retune.** Change enemy health (and only health) to meet the three design goals. Center each health value in its breakpoint step for the shortsword, using the method in lecture section 4. Record old and new health, and old and new margins.
8. **Patch test.** Apply a hypothetical patch of +10% damage to the warhammer. Record every pair whose TTK changes and by how much. Repeat for −10%.

## Deliverable

The spreadsheet file (or a share link) and a design note of about 400 words. The note must list the flagged pairs from step 5 before and after your retune, state which design goal was hardest to meet and why, and explain the warhammer patch result in terms of breakpoints.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Sheet structure | 15 | Inputs, matrices and analysis on separate tabs; no typed numbers in formulas | Tabs present, some hard-coded values | Single tab, numbers typed into formulas |
| Hits and TTK | 20 | All 30 pairs correct including the off-by-one and ceil guard | Off-by-one or a few pair errors | TTK computed as `H / DPS` only |
| Breakpoint margins | 20 | Both margins for every pair; flagged list correct | Margins computed one way only | No margins |
| Safety ratios | 15 | TTD and `R` correct with mitigation applied; shading used | Minor errors | Missing |
| Retune and patch test | 15 | Goals met with centered health values; patch results listed for both signs | Goals partly met, or patch tested one way | No retune |
| Design note | 15 | Decisions backed by numbers; patch explained with breakpoints | Some numbers, weak explanation | Restates the lab |
