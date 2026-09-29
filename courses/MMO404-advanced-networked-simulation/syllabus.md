# MMO404 — Advanced Networked Simulation

Year 4, semester 7 · 4 credits · Prerequisites: MMO302

Large battles, seamless worlds and distributed simulation: the frontier of MMO engineering.

## Learning outcomes

- Design distributed simulation across many servers
- Optimize replication for massive battles

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Limits of the zone model | [lecture](lectures/w01-limits-of-the-zone-model.md) | [zone-hotspot](examples/w01-zone-hotspot.html) |
| 2 | Seamless worlds and boundary handoff | [lecture](lectures/w02-seamless-worlds-and-boundary-handoff.md) | [seam-hysteresis](examples/w02-seam-hysteresis.html) |
| 3 | Spatial partitioning at scale | [lecture](lectures/w03-spatial-partitioning-at-scale.md) | [crowd-split](examples/w03-crowd-split.html) |
| 4 | Replication prioritization and relevancy | [lecture](lectures/w04-replication-prioritization-and-relevancy.md) | [replication-priority](examples/w04-replication-priority.html) |
| 5 | Bandwidth shaping and LOD for networking | [lecture](lectures/w05-bandwidth-shaping-and-lod-for-networking.md) | [network-lod](examples/w05-network-lod.html) |
| 6 | Massive battles | [lecture](lectures/w06-massive-battles.md) | [massive-battle](examples/w06-massive-battle.html) |
| 7 | Time dilation revisited | [lecture](lectures/w07-time-dilation-revisited.md) | [tidi-controller](examples/w07-tidi-controller.html) |
| 8 | Distributed simulation research | [lecture](lectures/w08-distributed-simulation-research.md) | [lookahead-timeline](examples/w08-lookahead-timeline.html) |
| 9 | Server meshing concepts | [lecture](lectures/w09-server-meshing-concepts.md) | [mesh-crowd](examples/w09-mesh-crowd.html) |
| 10 | Consistency models | [lecture](lectures/w10-consistency-models.md) | [optimistic-conflicts](examples/w10-optimistic-conflicts.html) |
| 11 | Physics in MMOs | [lecture](lectures/w11-physics-in-mmos.md) | [sleeping-bodies](examples/w11-sleeping-bodies.html) |
| 12 | AI at scale | [lecture](lectures/w12-ai-at-scale.md) | [ai-lod](examples/w12-ai-lod.html) |
| 13 | Cost engineering | [lecture](lectures/w13-cost-engineering.md) | [player-hour-cost](examples/w13-player-hour-cost.html) |
| 14 | Case study presentations | [lecture](lectures/w14-case-study-presentations.md) | [implied-cost-ladder](examples/w14-implied-cost-ladder.html) |
| 15 | Final: seamless 2-server handoff demo | [assessments](#assessment-materials) | — |

## Signature worked examples

- Replication priority: bandwidth budget allocated by distance and relevance (interactive)

## Labs

- [MMO404 · Lab 01: Zone capacity](labs/lab01.md)
- [MMO404 · Lab 02: Seams and handoff](labs/lab02.md)
- [MMO404 · Lab 03: Partitioning a crowded world](labs/lab03.md)
- [MMO404 · Lab 04: Priority allocator](labs/lab04.md)
- [MMO404 · Lab 05: Dead reckoning and shaping](labs/lab05.md)
- [MMO404 · Lab 06: Battle budget](labs/lab06.md)
- [MMO404 · Lab 07: A dilation controller](labs/lab07.md)
- [MMO404 · Lab 08: Lookahead on the border](labs/lab08.md)
- [MMO404 · Lab 09: A mesh for a crowd](labs/lab09.md)
- [MMO404 · Lab 10: Conflicts and convergence](labs/lab10.md)
- [MMO404 · Lab 11: Physics budget](labs/lab11.md)
- [MMO404 · Lab 12: AI budget](labs/lab12.md)
- [MMO404 · Lab 13: The player-hour bill](labs/lab13.md)
- [MMO404 · Lab 14: Case study teardown](labs/lab14.md)

## Assessment materials

- [MMO404 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [MMO404 · Final demo brief: a seamless two-server handoff](assessments/final-demo-brief.md)
- [MMO404 · Labs brief](assessments/labs-brief.md)

## Readings

- Selected GDC talks and papers (instructor list)

## Assessment

Labs (40%), final demo (60%)
