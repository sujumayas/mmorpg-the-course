# GD203 · Lab 01: Stat sheet in a spreadsheet

**Assigned:** week 1. **Due:** start of week 2. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 1, stats as design language](../lectures/w01-stats-as-design-language.md).

## Objective

Build a three-tab spreadsheet (inputs, derived, outcomes) for a small three-class RPG. Compute the exchange rate of every primary stat into damage per second and health for every class, flag the dead stats, and chart how additive and multiplicative damage bonuses stack. By the end you should be able to change one exchange rate on the inputs tab and see every class's outcomes update.

## Starter materials

Create these yourself from the tables below in any spreadsheet tool (Google Sheets, Excel, LibreOffice Calc). All numbers are fictional and belong to the course's practice RPG.

**Classes and base values.**

| Class | Base HP | Base weapon DPS | Base spell DPS |
|---|---|---|---|
| Guardian | 200 | 20 | 0 |
| Ranger | 150 | 18 | 0 |
| Mystic | 120 | 6 | 24 |

**Exchange rates (per point of primary stat).**

| Primary stat | Derived stat | Guardian | Ranger | Mystic |
|---|---|---|---|---|
| Might | attack power | 2 | 1 | 0.5 |
| Agility | attack power | 0 | 2 | 0 |
| Vitality | max HP | 12 | 8 | 6 |
| Spirit | spell power | 0 | 0 | 2 |

**Named constants.** 10 attack power adds 1 weapon DPS. 10 spell power adds 1 spell DPS. A character's DPS is weapon DPS plus spell DPS.

**Starting allocation (level 1).** Each class has 20 points: Guardian 8 Might, 0 Agility, 10 Vitality, 2 Spirit. Ranger 4 Might, 10 Agility, 6 Vitality, 0 Spirit. Mystic 2 Might, 0 Agility, 6 Vitality, 12 Spirit.

## Steps

1. **Inputs tab.** Enter the three tables above. Put each named constant in its own labeled cell. No formulas on this tab.
2. **Derived tab.** For each class compute attack power, spell power and max HP from the inputs. Every formula must reference the inputs tab; type no numbers into formulas.
3. **Outcomes tab.** Compute DPS and HP for each class. Check yourself: the level-1 Guardian has 16 AP, 1.6 bonus weapon DPS, 21.6 DPS and 320 HP.
4. **Exchange-rate table.** On the outcomes tab, build a 4 × 3 table: for each primary stat and class, how much DPS and how much HP one point adds. Mark a stat as **dead** for a class when it adds nothing to either DPS or HP. List the dead stats.
5. **Stat graph.** Draw (by hand or in a drawing tool) the graph from primary stats to derived stats to outcomes, with the rates on the arrows, one graph for all classes with per-class rates written on each arrow.
6. **Modifier stacking.** On a new tab, list `n` from 0 to 20. Compute the additive total `1 + 0.1n`, the multiplicative total `1.1^n`, and the gain from the n-th modifier for each. Chart both totals on one line chart and both gains on a second. Check yourself: at n = 10 the additive total is 2.00 with a gain of 5.3%, and the multiplicative total is 2.594.
7. **Dilution test.** Suppose every level adds +5% to an additive damage pool, so at level L the pool is `1 + 0.05 × (L − 1)`. A ring gives +10% to the same pool. Compute the ring's real DPS gain for a Mystic at level 1 and level 20. Then compute the gain if the ring were a +10% multiplier instead.
8. **Redesign.** Change exactly one exchange rate to remove one dead stat you do not want. Record the old and new outcomes.

## Deliverable

The spreadsheet file (or a share link), the stat graph as an image, and a design note of about 300 words that answers: which dead stats did you keep and why, what the dilution test showed, and what your one redesign changed.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Sheet structure | 20 | Three tabs, all constants named, no typed numbers in formulas | Tabs present but some hard-coded numbers | One tab, numbers typed into formulas |
| Correct outcomes | 20 | All check values match; every class computed | Minor errors in one class | Check values do not match |
| Exchange rates and dead stats | 20 | Complete 4 × 3 table, dead stats correctly listed | Table incomplete or one dead stat missed | No exchange-rate table |
| Stacking and dilution | 20 | Both charts correct, dilution test computed for both levels and both modifier types | One chart or one case missing | No stacking analysis |
| Design note | 20 | Clear decisions backed by numbers from the sheet | Decisions stated with few numbers | Restates the lab without decisions |
