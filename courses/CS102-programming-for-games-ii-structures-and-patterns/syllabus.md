# CS102 — Programming for Games II: Structures and Patterns

Year 1, semester 2 · 4 credits · Prerequisites: CS101

Object-oriented and data-oriented thinking, core data structures and the patterns that hold game code together.

## Learning outcomes

- Use classes, interfaces and composition appropriately
- Pick data structures by access pattern and cost
- Apply common game programming patterns
- Write testable gameplay code

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Classes, objects, encapsulation | [lecture](lectures/w01-classes-objects-encapsulation.md) | [stat-stage-gate](examples/w01-stat-stage-gate.html) |
| 2 | Inheritance vs composition (the 'god class' trap) | [lecture](lectures/w02-inheritance-vs-composition.md) | [hierarchy-vs-components](examples/w02-hierarchy-vs-components.html) |
| 3 | Interfaces and polymorphism | [lecture](lectures/w03-interfaces-and-polymorphism.md) | [reaction-grid](examples/w03-reaction-grid.html) |
| 4 | Big-O intuition for game developers | [lecture](lectures/w04-big-o-intuition-for-game-developers.md) | [pair-checks-budget](examples/w04-pair-checks-budget.html) |
| 5 | Arrays vs linked lists vs hash maps | [lecture](lectures/w05-arrays-linked-lists-and-hash-maps.md) | [list-vs-dict-timing](examples/w05-list-vs-dict-timing.html) |
| 6 | Queues and stacks: undo, command buffers | [lecture](lectures/w06-queues-and-stacks-undo-and-command-buffers.md) | [undo-stacks-and-input-queue](examples/w06-undo-stacks-and-input-queue.html) |
| 7 | Trees: scene graphs and skill trees | [lecture](lectures/w07-trees-scene-graphs-and-skill-trees.md) | [scene-graph-transforms](examples/w07-scene-graph-transforms.html) |
| 8 | Graphs: maps and dialogue | [lecture](lectures/w08-graphs-maps-and-dialogue.md) | [bfs-reachability](examples/w08-bfs-reachability.html) |
| 9 | Pattern: Component | [lecture](lectures/w09-pattern-component.md) | [component-queries](examples/w09-component-queries.html) |
| 10 | Pattern: Observer / events | [lecture](lectures/w10-observer-and-events.md) | [poll-vs-push](examples/w10-poll-vs-push.html) |
| 11 | Pattern: State and State Machine | [lecture](lectures/w11-state-and-state-machines.md) | [triple-jump-window](examples/w11-triple-jump-window.html) · [ghost-modes](examples/w11-ghost-modes.html) |
| 12 | Pattern: Command (input, replay, undo) | [lecture](lectures/w12-command-pattern-input-replay-undo.md) | [record-and-replay](examples/w12-record-and-replay.html) |
| 13 | Data-driven design: stats in JSON/CSV | [lecture](lectures/w13-data-driven-design-stats-in-json-and-csv.md) | [edit-the-table](examples/w13-edit-the-table.html) |
| 14 | Unit testing gameplay rules | [lecture](lectures/w14-unit-testing-gameplay-rules.md) | [property-sweep](examples/w14-property-sweep.html) |
| 15 | Final: data-driven RPG combat module | [assessments](#assessment-materials) | — |

## Signature worked examples

- Command pattern replay: record 30 s of inputs and replay them deterministically
- Why a List lookup of 10,000 items stalls a frame vs a Dictionary — live timing chart

## Labs

- [CS102 · Lab 01: Gated stats](labs/lab01.md)
- [CS102 · Lab 02: Breaking up the blob](labs/lab02.md)
- [CS102 · Lab 03: The chemistry engine](labs/lab03.md)
- [CS102 · Lab 04: The proximity budget](labs/lab04.md)
- [CS102 · Lab 05: The item database](labs/lab05.md)
- [CS102 · Lab 06: Undo and the input buffer](labs/lab06.md)
- [CS102 · Lab 07: Scene graph and skill tree](labs/lab07.md)
- [CS102 · Lab 08: Dialogue linter](labs/lab08.md)
- [CS102 · Lab 09: A world with a component index](labs/lab09.md)
- [CS102 · Lab 10: Build and instrument an event bus](labs/lab10.md)
- [CS102 · Lab 11: Table-driven state machines](labs/lab11.md)
- [CS102 · Lab 12: Record, replay and find the desync](labs/lab12.md)
- [CS102 · Lab 13: A validated data loader](labs/lab13.md)
- [CS102 · Lab 14: A test suite for the combat module](labs/lab14.md)

## Assessment materials

- [CS102 · Exam bank: practice, quiz and code-review questions](assessments/exam-bank.md)
- [CS102 · Final module brief: a data-driven RPG combat module](assessments/final-module-brief.md)
- [CS102 · Labs brief](assessments/labs-brief.md)
- [CS102 · Pattern project brief: Skirmish](assessments/pattern-project-brief.md)

## Readings

- Nystrom — Game Programming Patterns (Command, Observer, State, Component)

## Assessment

Labs (40%), pattern project (25%), final module (35%)
