# MMO303 · Lab 03: The EHP / eDPS calculator and a four-class TTK matrix

**Week:** 3 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the problem sets (30%); the calculator is reused in the simulator (week 13) and the final balance pass

## Objective

Build a reusable calculator that turns character sheets into effective HP, time to die and effective DPS, and then into a time-to-kill matrix. Use it to find the dominant class in a four-class roster and tune the roster until every class wins some duels and loses others, without breaking PvE.

This lab uses [week 3](../lectures/w03-effective-hp-and-effective-dps.md): mixed-damage EHP, healed time to die, the eDPS chain and the TTK matrix. The [resist split explorer](../examples/w03-resist-split.html) checks your optimal armor/MR splits in step 3.

## Starter materials

A fictional roster. All classes use `K = 100` for both armor and magic resistance (MR).

| Class | HP | Armor | MR | Sheet DPS | Hit chance | Crit chance | Crit multiplier | Uptime | Damage type |
|---|---|---|---|---|---|---|---|---|---|
| Blademaster | 1,200 | 60 | 20 | 100 | 95% | 20% | 2.0× | 90% | physical |
| Pyromancer | 800 | 20 | 50 | 90 | 100% | 10% | 1.5× | 100% | magic |
| Warden | 1,600 | 80 | 60 | 64 | 95% | 5% | 2.0× | 94% | physical |
| Stormcaller | 1,000 | 40 | 40 | 85 | 100% | 15% | 1.5× | 95% | magic |

Two PvE targets from week 3, section 5.

| Target | Armor | MR |
|---|---|---|
| Armored golem | 100 | 25 |
| Cloth caster | 20 | 50 |

A tank test: a boss dealing 400 raw DPS, 80% physical and 20% magic, against a class being healed at 150 HPS. Scale that class's HP by 8 (a raid-level tank) for this test only.

## Steps

1. **Inputs tab.** Enter the roster and targets as a table. Every later cell must refer to these inputs, so a single change updates the whole workbook.
2. **eDPS tab.** Compute each class's pre-defense eDPS with `sheet × hit × (1 + c(M − 1)) × uptime`, then eDPS against each PvE target.
3. **EHP tab.** Compute each class's EHP against physical, against magic, and against the boss's 80/20 mix. For the mix, also compute the best armor/MR split of that class's current total resist (week 3, section 2) and the EHP it would give.
4. **TTD tab.** For each class in the tank test, compute damage taken per second and time to die with and without the 150 HPS healer. Flag any class that never dies.
5. **TTK matrix.** Build the 4×4 matrix `TTK(i → j) = EHP_j vs i's type / eDPS_i`. Add a duel table listing the winner of each of the six pairs and a column counting each class's wins.
6. **Tune.** Change as few numbers as you can so that (a) no class wins all three of its duels, (b) no class loses all three, and (c) no class's eDPS against either PvE target changes by more than 15%. Log every change in a "Changes" tab with before and after values.
7. **Stress test.** Change the global crit multiplier for every class by +0.25 (as League did in reverse in patch 10.23). Record which duels flip. Write two sentences on what this means for how you would ship such a change.

## Deliverable

The workbook with the five tabs plus "Changes," and a one-page note that states the final duel structure (who beats whom), the number of changes made, the PvE impact of each, and the result of the stress test. Keep the workbook. The week 13 simulator work builds on it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Calculator structure | All outputs driven by the inputs tab; changing one input updates everything | Mostly formula-driven, some typed values | Typed values throughout | 15% |
| eDPS and EHP | All values correct, optimal split computed per class | One or two errors | Method wrong | 20% |
| TTD with healing | Correct with and without healer, never-dies cases flagged | Minor errors | Healing added before mitigation, or missing | 15% |
| TTK matrix and duels | Matrix and duel table correct, dominant class identified | Matrix correct, duel reading has an error | Matrix wrong | 20% |
| Tuning | All three conditions met with few, well-logged changes and PvE impact within 15% | Conditions met but many changes or PvE impact unchecked | Conditions not met | 20% |
| Stress test and note | Flipped duels identified, shipping implication argued | Flips identified, implication thin | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- Pre-defense eDPS: Blademaster 102.6, Pyromancer 94.5, Warden 60.0, Stormcaller 86.8.
- TTK matrix in seconds (row attacks column; order Blademaster, Pyromancer, Warden, Stormcaller):
  - Blademaster: 18.7, 9.4, 28.1, 13.6
  - Pyromancer: 15.2, 12.7, 27.1, 14.8
  - Warden: 32.0, 16.0, 48.0, 23.3
  - Stormcaller: 16.6, 13.8, 29.5, 16.1
- Duel wins: Blademaster 3, Warden 2, Stormcaller 1, Pyromancer 0. The Blademaster is dominant and the Pyromancer is not viable in duels.
- eDPS vs armored golem: 51.3, 75.6, 30.0, 69.4. vs cloth caster: 85.5, 63.0, 50.0, 57.9.

</details>
