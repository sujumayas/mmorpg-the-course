# MMO303 · Lab 06: Threat budget simulator

**Week:** 6, threat, aggro and control ([lecture](../lectures/w06-threat-aggro-and-control.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the problem sets (30%). The simulator becomes a module of the week 13 combat simulator.

## Objective

Build a tick-based threat simulator for one or more enemies and a 5-player group, confirm it against the closed-form pull time from the lecture, and use it to set a threat rule that makes DPS players hold back a little, but not a lot.

## Starter materials

- `threat_sim.py` skeleton with a 0.1-second tick loop, a `Combatant` class (damage per second, threat modifier, melee or ranged, healing per second) and an empty `ThreatTable` class.
- `test_threat.py` with the lecture's test values: `τT = 500`, `L = 1,500`, melee 700 pulls at 11.0 s, ranged 700 at 39.0 s, melee 550 never; taunt at first pull gives a second pull at 16.13 s.
- The [interactive](../examples/w06-threat-race.html) for spot checks.

## Steps

1. **Threat table.** Implement per-enemy threat. Damage adds `damage × modifier`. Healing adds `0.5 × healing / number of enemies in combat` to every enemy.
2. **Target switching.** An enemy switches when a melee player exceeds 110% of the current target's threat, or a ranged player exceeds 130%. Record every switch with its time.
3. **Closed-form check.** Run the test cases. Your tick-based pull times must match the formula `k L / (τD − k τT)` within one tick.
4. **Taunt.** Add a tank taunt: on use, the tank's threat becomes equal to the highest on the table and the enemy targets the tank. Add a 10-second cooldown. Report pull times over a 60-second fight for the melee 700 case with the tank taunting whenever it can.
5. **Threat drop.** Add a DPS ability that removes 50% of that player's threat, 30-second cooldown. Find the best time to use it in the melee 700 case (the one that delays the first pull the most).
6. **Multi-enemy pull.** Four enemies. The tank has a single-target TPS of 700 on its main target and an area ability giving 150 TPS to all four. A healer heals 800 HPS. Report which enemies end up on the healer, and when.
7. **Tune.** Using the lecture's week 5 encounter (`H = 600,000`, `T = 180 s`, group 1-1-3, DPS at 1,000 raw each), pick a tank threat modifier so that DPS players must hold back to between 90% and 100% of their raw damage, and the group still passes the damage check. Show the numbers.

## Deliverable

The simulator with passing tests, a plot of threat over time for steps 4 and 6, and a report of at most 500 words with your tuned modifier and a one-paragraph argument for why that amount of holding back is fun, or why it is not.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Simulator correctness | Tests pass; matches closed form within one tick | Small timing drift explained | Tests fail | 30% |
| Taunt and threat drop | Both implemented, results reported and interpreted with the slope argument | Implemented, not interpreted | Missing | 20% |
| Multi-enemy pull | Healer threat split correct, switch times reported | Split correct, analysis thin | Missing or wrong split | 20% |
| Tuning | Modifier found, damage check verified, hold-back percent stated | Modifier found without full verification | Missing | 20% |
| Plots and writing | Clear plots, numeric argument | Plots unlabeled or argument vague | Missing | 10% |
