# GD203 — Combat and Progression Design

Year 2, semester 4 · 4 credits · Prerequisites: GD102, MA102

The numbers behind RPGs: stats, damage formulas, time-to-kill, XP and power curves, built in spreadsheets.

## Learning outcomes

- Design stat systems and damage formulas with predictable properties
- Tune time-to-kill and encounter length
- Build XP and power curves that pace a 40-hour game
- Prototype balance in spreadsheets and simulation

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Stats as design language | [lecture](lectures/w01-stats-as-design-language.md) | [modifier-stacking](examples/w01-modifier-stacking.html) |
| 2 | Damage formulas: subtractive vs divisive vs multiplicative | [lecture](lectures/w02-damage-formulas.md) | [damage-models](examples/w02-damage-models.html) |
| 3 | Mitigation curves and effective HP | [lecture](lectures/w03-mitigation-curves-and-effective-hp.md) | [effective-hp](examples/w03-effective-hp.html) |
| 4 | Time-to-kill (TTK) and time-to-die | [lecture](lectures/w04-time-to-kill-and-time-to-die.md) | [breakpoint-staircase](examples/w04-breakpoint-staircase.html) |
| 5 | DPS, burst and sustain | [lecture](lectures/w05-dps-burst-and-sustain.md) | [burst-vs-sustain](examples/w05-burst-vs-sustain.html) |
| 6 | Critical hits and variance | [lecture](lectures/w06-critical-hits-and-variance.md) | [crit-hits-to-kill](examples/w06-crit-hits-to-kill.html) |
| 7 | XP curves: linear, polynomial, exponential | [lecture](lectures/w07-xp-curves.md) | [xp-curve-shapes](examples/w07-xp-curve-shapes.html) |
| 8 | Power curves and level scaling | [lecture](lectures/w08-power-curves-and-level-scaling.md) | [level-gap](examples/w08-level-gap.html) |
| 9 | Item budgets and stat weights | [lecture](lectures/w09-item-budgets-and-stat-weights.md) | [item-budget](examples/w09-item-budget.html) |
| 10 | Enemy design by the numbers | [lecture](lectures/w10-enemy-design-by-the-numbers.md) | [encounter-cost](examples/w10-encounter-cost.html) |
| 11 | Spreadsheet balancing workshop | [lecture](lectures/w11-spreadsheet-balancing-workshop.md) | [level-sweep](examples/w11-level-sweep.html) |
| 12 | Simulation-driven balance | [lecture](lectures/w12-simulation-driven-balance.md) | [duel-simulator](examples/w12-duel-simulator.html) |
| 13 | Difficulty modes and scaling | [lecture](lectures/w13-difficulty-modes-and-scaling.md) | [difficulty-ladder](examples/w13-difficulty-ladder.html) |
| 14 | Horizontal vs vertical progression | [lecture](lectures/w14-horizontal-vs-vertical-progression.md) | [power-gap](examples/w14-power-gap.html) |
| 15 | Final: combat system spec + balance spreadsheet | [assessments](#assessment-materials) | — |

## Signature worked examples

- Subtractive armor (damage - armor) makes weak attacks useless; divisive A/(A+K) never does — interactive comparison
- Effective HP is linear in armor: every point is worth the same, the 'diminishing returns' is an illusion of the percent view
- Item budget: price every stat in 'points' and see which item is secretly overbudget

## Labs

- [GD203 · Lab 01: Stat sheet in a spreadsheet](labs/lab01.md)
- [GD203 · Lab 02: Three damage formulas in one sheet](labs/lab02.md)
- [GD203 · Lab 03: Effective HP and the defensive budget](labs/lab03.md)
- [GD203 · Lab 04: The breakpoint table](labs/lab04.md)
- [GD203 · Lab 05: Burst, sustain and the crossover](labs/lab05.md)
- [GD203 · Lab 06: Crits, breakpoints and Monte Carlo](labs/lab06.md)
- [GD203 · Lab 07: XP curve and 40-hour pacing sheet](labs/lab07.md)
- [GD203 · Lab 08: Power curves and scaling bands](labs/lab08.md)
- [GD203 · Lab 09: Item budget audit](labs/lab09.md)
- [GD203 · Lab 10 reference sheet](labs/lab10-reference.md)
- [GD203 · Lab 10: Enemy roster from player units](labs/lab10.md)
- [GD203 · Lab 11: The level-sweep balance sheet](labs/lab11.md)
- [GD203 · Lab 12: Duel simulator](labs/lab12.md)
- [GD203 · Lab 13: Difficulty ladder](labs/lab13.md)
- [GD203 · Lab 14: Progression audit](labs/lab14.md)

## Assessment materials

- [GD203 · Exam bank: practice, quiz and viva questions](assessments/exam-bank.md)
- [GD203 · Final spec brief: combat system spec and balance workbook](assessments/final-spec-brief.md)
- [GD203 · Simulation brief](assessments/simulation-brief.md)
- [GD203 · Spreadsheet labs brief](assessments/spreadsheet-labs-brief.md)

## Readings

- Schreiber & Romero — Game Balance (2021)
- Schreiber — Game Balance Concepts, levels 1-3, 6

## Assessment

Spreadsheet labs (40%), simulation (20%), final spec (40%)
