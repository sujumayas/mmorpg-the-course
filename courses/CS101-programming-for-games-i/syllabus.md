# CS101 — Programming for Games I

Year 1, semester 1 · 4 credits · Prerequisites: none

First programming course, taught entirely through small games: variables to game loops to a complete arcade game.

## Learning outcomes

- Write, run and debug programs using variables, conditionals, loops and functions
- Explain and implement a fixed-timestep game loop
- Handle input, draw sprites, detect collisions
- Ship a complete small arcade game

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Programs, variables, types — a text adventure's state | [lecture](lectures/w01-programs-variables-and-types.md) | [byte-counter](examples/w01-byte-counter.html) |
| 2 | Conditionals — room transitions and win/lose | [lecture](lectures/w02-conditionals-room-transitions-and-win-lose.md) | [win-lose-order](examples/w02-win-lose-order.html) |
| 3 | Loops — the game loop concept | [lecture](lectures/w03-loops-and-the-game-loop.md) | [invaders-loop](examples/w03-invaders-loop.html) |
| 4 | Functions and decomposition | [lecture](lectures/w04-functions-and-decomposition.md) | [one-function-many-callers](examples/w04-one-function-many-callers.html) |
| 5 | Arrays and lists — inventories | [lecture](lectures/w05-arrays-and-lists-inventories.md) | [inventory-stacking](examples/w05-inventory-stacking.html) |
| 6 | Dictionaries/maps — item databases | [lecture](lectures/w06-dictionaries-item-databases.md) | [ids-vs-keys](examples/w06-ids-vs-keys.html) |
| 7 | Engine intro: scenes, nodes, scripts (Godot) | [lecture](lectures/w07-engine-intro-scenes-nodes-scripts.md) | [update-order](examples/w07-update-order.html) |
| 8 | Input handling and movement | [lecture](lectures/w08-input-handling-and-movement.md) | [jump-forgiveness](examples/w08-jump-forgiveness.html) |
| 9 | Delta time and frame-rate independence | [lecture](lectures/w09-delta-time-and-frame-rate-independence.md) | [fixed-timestep-accumulator](examples/w09-fixed-timestep-accumulator.html) · [refresh-rate-race](examples/w09-refresh-rate-race.html) |
| 10 | Collision basics: AABB and circles | [lecture](lectures/w10-collision-basics-aabb-and-circles.md) | [aabb-overlap](examples/w10-aabb-overlap.html) |
| 11 | Game state machines (menu, play, pause, game over) | [lecture](lectures/w11-game-state-machines.md) | [ghost-mode-machine](examples/w11-ghost-mode-machine.html) |
| 12 | Debugging: breakpoints, logging, rubber-ducking | [lecture](lectures/w12-debugging-breakpoints-logging-rubber-ducking.md) | [level-256-debugger](examples/w12-level-256-debugger.html) |
| 13 | Randomness: spawning and procedural variety | [lecture](lectures/w13-randomness-spawning-and-procedural-variety.md) | [randomizer-droughts](examples/w13-randomizer-droughts.html) |
| 14 | Polish pass: sound, particles, screen shake | [lecture](lectures/w14-polish-pass-sound-particles-screen-shake.md) | [trauma-shake](examples/w14-trauma-shake.html) |
| 15 | Final: arcade game release | [assessments](#assessment-materials) | — |

## Signature worked examples

- Why movement speed doubles on a 120 Hz monitor without delta time — side-by-side interactive
- Fixed vs variable timestep: the 'Fix Your Timestep' accumulator visualized
- AABB overlap test shown as four comparisons on a live drag-and-drop canvas

## Labs

- [CS101 · Lab 01: The state of a text adventure](labs/lab01.md)
- [CS101 · Lab 02: A cave with a way out](labs/lab02.md)
- [CS101 · Lab 03: Loop it](labs/lab03.md)
- [CS101 · Lab 04: Refactoring the combat turn](labs/lab04.md)
- [CS101 · Lab 05: A stacking inventory](labs/lab05.md)
- [CS101 · Lab 06: The item database](labs/lab06.md)
- [CS101 · Lab 07: A scene tree you can test](labs/lab07.md)
- [CS101 · Lab 08: Input you can trust](labs/lab08.md)
- [CS101 · Lab 09: One game, every frame rate](labs/lab09.md)
- [CS101 · Lab 10: Collision toolkit](labs/lab10.md)
- [CS101 · Lab 11: The game-flow machine](labs/lab11.md)
- [CS101 · Lab 12: Bug hunt](labs/lab12.md)
- [CS101 · Lab 13: Seeded randomizers and a fair spawner](labs/lab13.md)
- [CS101 · Lab 14: Headless juice](labs/lab14.md)

## Assessment materials

- [CS101 · Exam bank](assessments/exam-bank.md)
- [CS101 · Final arcade game brief](assessments/final-arcade-game-brief.md)
- [CS101 · Mini-games brief](assessments/mini-games-brief.md)
- [CS101 · Weekly exercises brief](assessments/weekly-exercises-brief.md)

## Readings

- Nystrom — Game Programming Patterns: Game Loop, Update Method
- Fiedler — Fix Your Timestep! (gafferongames.com)

## Assessment

Weekly exercises (40%), 2 mini-games (30%), final arcade game (30%)
