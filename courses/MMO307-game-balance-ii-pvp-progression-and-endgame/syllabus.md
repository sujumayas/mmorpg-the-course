# MMO307 — Game Balance II: PvP, Progression and Endgame

Year 3, semester 6 · 4 credits · Prerequisites: MMO303

Long-term balance: rating systems, gear treadmills, power creep, catch-up mechanics and endgame design.

## Learning outcomes

- Implement and tune Elo/Glicko-style rating systems
- Design endgame progression that resists power creep
- Balance PvP separately from PvE where needed

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | The endgame problem | [lecture](lectures/w01-the-endgame-problem.md) | [upgrade-decay](examples/w01-upgrade-decay.html) |
| 2 | Vertical progression and power creep | [lecture](lectures/w02-vertical-progression-and-power-creep.md) | [power-creep](examples/w02-power-creep.html) |
| 3 | Horizontal progression | [lecture](lectures/w03-horizontal-progression.md) | [situation-weights](examples/w03-situation-weights.html) |
| 4 | Gear treadmills and item level | [lecture](lectures/w04-gear-treadmills-and-item-level.md) | [season-ladder](examples/w04-season-ladder.html) |
| 5 | Stat squish: when numbers get too big | [lecture](lectures/w05-stat-squish-when-numbers-get-too-big.md) | [squish-map](examples/w05-squish-map.html) |
| 6 | Catch-up mechanics | [lecture](lectures/w06-catch-up-mechanics.md) | [rolling-cap](examples/w06-rolling-cap.html) |
| 7 | PvP balance vs PvE balance: split tuning | [lecture](lectures/w07-pvp-vs-pve-split-tuning.md) | [split-tuning](examples/w07-split-tuning.html) |
| 8 | Elo and expected score | [lecture](lectures/w08-elo-and-expected-score.md) | [elo-expected-score](examples/w08-elo-expected-score.html) |
| 9 | Glicko and uncertainty; TrueSkill for teams | [lecture](lectures/w09-glicko-and-trueskill.md) | [rating-uncertainty](examples/w09-rating-uncertainty.html) |
| 10 | Matchmaking quality vs queue time | [lecture](lectures/w10-matchmaking-quality-vs-queue-time.md) | [queue-fairness-curve](examples/w10-queue-fairness-curve.html) |
| 11 | Seasonal structures and resets | [lecture](lectures/w11-seasonal-structures-and-resets.md) | [soft-reset](examples/w11-soft-reset.html) |
| 12 | Alternative advancement and account progression | [lecture](lectures/w12-alternative-advancement-and-account-progression.md) | [aa-gap](examples/w12-aa-gap.html) |
| 13 | Meta-game and patch cycles | [lecture](lectures/w13-meta-game-and-patch-cycles.md) | [patch-cadence](examples/w13-patch-cadence.html) |
| 14 | Measuring balance with win rates and pick rates | [lecture](lectures/w14-measuring-balance-with-win-rates-and-pick-rates.md) | [rating-absorbs-advantage](examples/w14-rating-absorbs-advantage.html) |
| 15 | Final: season design with rating simulation | [assessments](#assessment-materials) | — |

## Signature worked examples

- Elo expected score: 1/(1+10^(diff/400)) — slider from 0 to 800 rating gap
- Power creep chart: item level over expansions and the stat squish reset (verified: Warcraft Wiki stat squish, 8.0.1, 9.0.1, 12.0.0)
- Queue time vs match fairness trade-off curve

## Labs

- [MMO307 · Lab 01: Gear chase simulator](labs/lab01.md)
- [MMO307 · Lab 02: Power creep audit](labs/lab02.md)
- [MMO307 · Lab 03: Horizontal reward track](labs/lab03.md)
- [MMO307 · Lab 04: The season ladder](labs/lab04.md)
- [MMO307 · Lab 05: The squish planner](labs/lab05.md)
- [MMO307 · Lab 06: Catch-up simulator](labs/lab06.md)
- [MMO307 · Lab 07: Split register](labs/lab07.md)
- [MMO307 · Lab 08: Build and tune an Elo ladder](labs/lab08.md)
- [MMO307 · Lab 09: Glicko and TrueSkill side by side](labs/lab09.md)
- [MMO307 · Lab 10: Queue time vs match fairness](labs/lab10.md)
- [MMO307 · Lab 11: Simulating a season end](labs/lab11.md)
- [MMO307 · Lab 12: Designing an alternative advancement track](labs/lab12.md)
- [MMO307 · Lab 13: Settling time and patch cadence](labs/lab13.md)
- [MMO307 · Lab 14: Does the ladder hide an overpowered class?](labs/lab14.md)

## Assessment materials

- [MMO307 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [MMO307 · Final season design brief: a ranked season with rating simulation](assessments/final-season-design-brief.md)
- [MMO307 · Progression analysis brief](assessments/progression-analysis-brief.md)
- [MMO307 · Rating lab brief](assessments/rating-lab-brief.md)

## Readings

- Elo — The Rating of Chessplayers
- Glickman — The Glicko System
- Herbrich, Minka, Graepel (2006) — TrueSkill

## Assessment

Rating lab (30%), progression analysis (30%), final season design (40%)
