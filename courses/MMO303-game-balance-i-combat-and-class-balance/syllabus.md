# MMO303 — Game Balance I: Combat and Class Balance

Year 3, semester 5 · 4 credits · Prerequisites: GD203, MA102

Balancing many classes, roles and encounters at once: mitigation math, the holy trinity, intransitivity, and simulation.

## Learning outcomes

- Derive and choose mitigation formulas with eyes open
- Balance roles (tank, healer, DPS) around encounter demands
- Use intransitive design and game theory to avoid dominant builds
- Build a combat simulator to test class balance

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | What 'balanced' means: fairness, viability, diversity | [lecture](lectures/w01-what-balanced-means.md) | [effective-classes](examples/w01-effective-classes.html) |
| 2 | Armor and damage mitigation: A/(A+K) | [lecture](lectures/w02-armor-and-damage-mitigation.md) | [armor-curve](examples/w02-armor-curve.html) |
| 3 | Effective HP and effective DPS | [lecture](lectures/w03-effective-hp-and-effective-dps.md) | [resist-split](examples/w03-resist-split.html) |
| 4 | Stacking mitigation: multiplicative layers | [lecture](lectures/w04-stacking-mitigation-multiplicative-layers.md) | [mitigation-layers](examples/w04-mitigation-layers.html) |
| 5 | The holy trinity: tank, healer, DPS | [lecture](lectures/w05-the-holy-trinity-tank-healer-dps.md) | [role-composition](examples/w05-role-composition.html) |
| 6 | Threat, aggro and control | [lecture](lectures/w06-threat-aggro-and-control.md) | [threat-race](examples/w06-threat-race.html) |
| 7 | Healing throughput and mana economy | [lecture](lectures/w07-healing-throughput-and-mana-economy.md) | [mana-budget](examples/w07-mana-budget.html) |
| 8 | Crowd control and diminishing returns | [lecture](lectures/w08-crowd-control-and-diminishing-returns.md) | [cc-diminishing-returns](examples/w08-cc-diminishing-returns.html) |
| 9 | Intransitivity and counters | [lecture](lectures/w09-intransitivity-and-counters.md) | [counter-triangle](examples/w09-counter-triangle.html) |
| 10 | Game theory: payoff matrices and Nash equilibria | [lecture](lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) | [world-boss-game](examples/w10-world-boss-game.html) |
| 11 | Lanchester's laws and group combat | [lecture](lectures/w11-lanchesters-laws-and-group-combat.md) | [lanchester-battle](examples/w11-lanchester-battle.html) |
| 12 | Stat weights and theorycrafting | [lecture](lectures/w12-stat-weights-and-theorycrafting.md) | [stat-weights](examples/w12-stat-weights.html) |
| 13 | Combat simulators | [lecture](lectures/w13-combat-simulators.md) | [monte-carlo-dps](examples/w13-monte-carlo-dps.html) |
| 14 | Communicating balance changes (patch notes) | [lecture](lectures/w14-communicating-balance-changes.md) | [patch-line-translator](examples/w14-patch-line-translator.html) |
| 15 | Final: 4-class balance pass with simulation evidence | [assessments](#assessment-materials) | — |

## Signature worked examples

- Armor / (Armor + K) across League of Legends, Diablo II and WoW — the anchor lesson (built: w02)
- Lanchester's square law: why 10 players beat 8 by far more than 25% (interactive battle)
- CC diminishing returns: 100% -> 50% -> 25% -> immune (WoW-style) and chain-stun math

## Labs

- [MMO303 · Lab 01: Reading a balance dashboard](labs/lab01.md)
- [MMO303 · Lab 02: Mitigation spreadsheet](labs/lab02.md)
- [MMO303 · Lab 03: The EHP / eDPS calculator and a four-class TTK matrix](labs/lab03.md)
- [MMO303 · Lab 04: Mitigation stack audit](labs/lab04.md)
- [MMO303 · Lab 05: Composition solver](labs/lab05.md)
- [MMO303 · Lab 06: Threat budget simulator](labs/lab06.md)
- [MMO303 · Lab 07: Healer mana budget](labs/lab07.md)
- [MMO303 · Lab 08: Chain CC planner](labs/lab08.md)
- [MMO303 · Lab 09: Patch the triangle](labs/lab09.md)
- [MMO303 · Lab 10: Solving a class meta](labs/lab10.md)
- [MMO303 · Lab 11: Battle simulator and the exponent of your game](labs/lab11.md)
- [MMO303 · Lab 12: Measuring stat weights with a noisy simulator](labs/lab12.md)
- [MMO303 · Lab 13: Build a combat simulator](labs/lab13.md)
- [MMO303 · Lab 14: Patch notes from simulation evidence](labs/lab14.md)

## Assessment materials

- [MMO303 · Question bank](assessments/exam-bank.md)
- [MMO303 · Final balance pass brief](assessments/final-balance-pass-brief.md)
- [MMO303 · Problem sets brief](assessments/problem-sets-brief.md)
- [MMO303 · Combat simulator brief](assessments/simulator-brief.md)

## Readings

- Schreiber & Romero — Game Balance (2021)
- Sirlin — Balancing Multiplayer Competitive Games (GDC 2009)
- Elias, Garfield & Gutschera — Characteristics of Games

## Assessment

Problem sets (30%), simulator (30%), final balance pass (40%)
