# CS203 — Artificial Intelligence for Games

Year 2, semester 4 · 4 credits · Prerequisites: CS102, MA101

NPC behavior that is fun rather than optimal: pathfinding, decision making and group tactics.

## Learning outcomes

- Implement A* and navigation meshes
- Build NPC behavior with FSMs, behavior trees and utility AI
- Design AI for readability and fairness

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Game AI vs academic AI: the goal is fun | [lecture](lectures/w01-game-ai-vs-academic-ai.md) | [ghost-targets](examples/w01-ghost-targets.html) |
| 2 | Steering behaviors | [lecture](lectures/w02-steering-behaviors.md) | [seek-vs-arrive](examples/w02-seek-vs-arrive.html) |
| 3 | Graphs and Dijkstra | [lecture](lectures/w03-graphs-and-dijkstra.md) | [dijkstra-terrain](examples/w03-dijkstra-terrain.html) |
| 4 | A* and heuristics | [lecture](lectures/w04-a-star-and-heuristics.md) | [astar-vs-dijkstra](examples/w04-astar-vs-dijkstra.html) |
| 5 | Navigation meshes | [lecture](lectures/w05-navigation-meshes.md) | [navmesh-funnel](examples/w05-navmesh-funnel.html) |
| 6 | Finite state machines | [lecture](lectures/w06-finite-state-machines.md) | [target-commitment](examples/w06-target-commitment.html) |
| 7 | Behavior trees | [lecture](lectures/w07-behavior-trees.md) | [bt-tick-trace](examples/w07-bt-tick-trace.html) |
| 8 | Utility AI | [lecture](lectures/w08-utility-ai.md) | [utility-curves](examples/w08-utility-curves.html) |
| 9 | GOAP | [lecture](lectures/w09-goap.md) | [goap-planner](examples/w09-goap-planner.html) |
| 10 | Perception systems | [lecture](lectures/w10-perception-systems.md) | [detection-meter](examples/w10-detection-meter.html) |
| 11 | Group tactics and formations | [lecture](lectures/w11-group-tactics-and-formations.md) | [attack-grid](examples/w11-attack-grid.html) |
| 12 | MMO mob AI: leashing, aggro, threat tables | [lecture](lectures/w12-mmo-mob-ai-leashing-aggro-threat-tables.md) | [threat-table](examples/w12-threat-table.html) |
| 13 | Boss AI and scripted encounters | [lecture](lectures/w13-boss-ai-and-scripted-encounters.md) | [phase-gates](examples/w13-phase-gates.html) |
| 14 | Performance: AI LOD, time-slicing | [lecture](lectures/w14-performance-ai-lod-and-time-slicing.md) | [frame-budget](examples/w14-frame-budget.html) |
| 15 | Final: NPC ecosystem demo | [assessments](#assessment-materials) | — |

## Signature worked examples

- A* vs Dijkstra on the same map: nodes expanded, animated
- Threat table: why a tank's threat multiplier keeps the boss off healers (interactive)

## Labs

- [CS203 · Lab 01: Ghost brains](labs/lab01.md)
- [CS203 · Lab 02: A steering toolkit](labs/lab02.md)
- [CS203 · Lab 03: Terrain costs, movement range and Dijkstra maps](labs/lab03.md)
- [CS203 · Lab 04: A* on a tactical grid](labs/lab04.md)
- [CS203 · Lab 05: A navmesh by hand](labs/lab05.md)
- [CS203 · Lab 06: A guard that commits](labs/lab06.md)
- [CS203 · Lab 07: A behavior tree you can trace](labs/lab07.md)
- [CS203 · Lab 08: Utility scoring you can tune](labs/lab08.md)
- [CS203 · Lab 09: A goal-oriented action planner](labs/lab09.md)
- [CS203 · Lab 10: The awareness meter](labs/lab10.md)
- [CS203 · Lab 11: The stage manager](labs/lab11.md)
- [CS203 · Lab 12: The mob brain](labs/lab12.md)
- [CS203 · Lab 13: Encounter scripts and skip thresholds](labs/lab13.md)
- [CS203 · Lab 14: A frame-budget scheduler](labs/lab14.md)

## Assessment materials

- [CS203 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [CS203 · Final demo brief: an NPC ecosystem](assessments/final-demo-brief.md)
- [CS203 · Labs brief](assessments/labs-brief.md)

## Readings

- Millington — AI for Games (3rd ed.)
- Rabin (ed.) — Game AI Pro (free online chapters)

## Assessment

Labs (50%), final demo (50%)
