# CS203 · Labs brief

**Weight:** 50% of the course grade.
**What counts:** all 14 labs, one per lecture week. Each lab is marked out of 100 with its own rubric, then scaled to the points in the table below.
**When:** each lab is assigned in its week's session and is due before the next lecture. Lab 14 is due at the end of week 14, because the [final demo](final-demo-brief.md) runs on its scheduler.
**Work mode:** individual unless the lab says otherwise. Labs 05 and 11 allow pairs for their first two parts; the written note is always individual.

## What this component is for

A lecture gives you a model, such as `b = v² / (2a)` for braking, `f* = T / (T + F)` for peeking or `m* = B / (2.6 d N)` for the tank multiplier. The lab makes you implement it, reproduce the lecture's numbers and then use it the way a designer would, by tuning one number until an NPC does what a written brief asks. Two of the course outcomes are assessed mostly here, "implement A* and navigation meshes" and "build NPC behavior with FSMs, behavior trees and utility AI", because both can only be shown by code that passes checks. The third, "design AI for readability and fairness", runs through every lab's design note.

The labs are also the parts of your final demo. The ecosystem you build in weeks 13 to 15 reuses your steering, pathfinding, decision, perception, group and scheduling code, so a lab you skip is work you will still have to do later.

## The labs

| Lab | Week | Title | Checker | Feeds the final demo |
|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Ghost brains | `test_ghosts.py` | the five tests in `DESIGN.md` |
| [02](../labs/lab02.md) | 2 | A steering toolkit | `test_steering.py` | movement (required) |
| [03](../labs/lab03.md) | 3 | Terrain costs, movement range and Dijkstra maps | `test_paths.py` | cost tables, flee maps |
| [04](../labs/lab04.md) | 4 | A* on a tactical grid | `check_lab04.py` | grid pathfinding option |
| [05](../labs/lab05.md) | 5 | A navmesh by hand | `check_lab05.py` | navmesh pathfinding option |
| [06](../labs/lab06.md) | 6 | A guard that commits | `check_lab06.py` | decision method option |
| [07](../labs/lab07.md) | 7 | A behavior tree you can trace | `test_bt.py` | decision method option |
| [08](../labs/lab08.md) | 8 | Utility scoring you can tune | `test_utility.py` | decision method option |
| [09](../labs/lab09.md) | 9 | A goal-oriented action planner | `test_goap.py` | decision method option |
| [10](../labs/lab10.md) | 10 | The awareness meter | `check_lab10.py` | perception (required) |
| [11](../labs/lab11.md) | 11 | The stage manager | `check_lab11.py` | group rule option |
| [12](../labs/lab12.md) | 12 | The mob brain | `check_lab12.py` | group rule option |
| [13](../labs/lab13.md) | 13 | Encounter scripts and skip thresholds | `test_encounter.py` | scripted events |
| [14](../labs/lab14.md) | 14 | A frame-budget scheduler | `test_scheduler.py` | scheduler (required) |

## Rubric

The labs component is out of 100 points. Each lab's mark (out of 100, from its own rubric) is scaled to the points below. Lab 14 carries two extra points because the final demo depends on it.

| Lab | Topic | Points |
|---|---|---|
| 01 | Ghost brains | 7 |
| 02 | Steering toolkit | 7 |
| 03 | Dijkstra and movement range | 7 |
| 04 | A* on a tactical grid | 7 |
| 05 | Navmesh and funnel | 7 |
| 06 | State machine with commitment | 7 |
| 07 | Behavior tree tick rules | 7 |
| 08 | Utility scoring | 7 |
| 09 | Goal-oriented planner | 7 |
| 10 | Awareness meter | 7 |
| 11 | Stage manager | 7 |
| 12 | Threat table and leash | 7 |
| 13 | Encounter runner | 7 |
| 14 | Frame-budget scheduler | 9 |
| **Total** | | **100** |

Your labs component is the points total multiplied by 0.50. A lab marked 80 out of 100 contributes `0.80 × 7 = 5.6` points, which is 2.8% of the course grade.

## How each lab is marked

Every lab rubric has four to six criteria with weights that add up to 100%. Each criterion is scored in bands from 0 to 4 and earns `weight × band ÷ 4`. A criterion weighted 30% and marked 3 earns 22.5 points.

| Band | Label in the lab rubrics | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the lecture or the checker |
| 3 | Good, or Adequate (upper) | 75% | Correct work with one explanation or measurement missing |
| 2 | Partial, or Adequate (lower) | 50% | Works in outline; a number is off or the reasoning is thin |
| 1 | Weak or Missing (partial) | 25% | Attempted, but fails the checker or reasons from the wrong model |
| 0 | Missing | 0% | Not submitted, or unrelated to the lab |

Labs 01 to 03 label the middle column "Adequate (2-3)". Labs 04 to 14 split it into "Good (3)" and "Partial (2)". The arithmetic is the same.

### Automatic checks

Every lab ships a checker that fails on the untouched starter and passes on a correct solution. Markers run it from a clean copy of your lab folder with the course interpreter, `.venv/bin/python`. Two rules follow.

- **The correctness criterion is capped by the checker.** The first criterion in every rubric (Correctness, Correct A*, Engine, Composites, Toolkit, Planner and so on) cannot score above band 1 if the checker does not pass on the marker's machine.
- **"Works on my machine" is a fail.** Absolute paths, files outside the lab folder, packages outside the standard library and edited checkers all count as a failing check.

### Numbers before claims

Most labs end with a note of at most 300 words to a designer, a lead programmer or a raid team. The note is marked on its numbers. "The guard feels better now" earns band 1. "The strafe trace went from 127 transitions to 2 and the attack share from 42% to 99%" earns band 4. Where a lab asks you to work something out by hand before you run it (Lab 04 step 1, Lab 05 step 1, Lab 08 steps 1 and 2, Lab 10 step 1, Lab 11 step 1, Lab 12 step 1, Lab 13 step 1), write the prediction in your report first. A prediction changed after the run to match it earns band 0 for that criterion. A wrong prediction with honest working loses nothing if you explain the difference.

## Spot checks

From week 2 on, each lab session opens with a 10-minute ungraded quiz of two or three questions from the [exam bank](exam-bank.md). In the same session a marker picks three or four students and asks two short questions about their previous lab, rewritten with that student's own code and numbers. Typical questions:

- "Your ogre's slowing radius is 4 m. What is its braking distance, and does it overshoot?"
- "Point to the line in your `Sequence.tick` that makes the hybrid rule re-check conditions. What does the memory guard do on tick 5 if you delete it?"
- "Your threat table kept the boss on the tank at `m = 1.2`. What margin `S` is that for a boss hitting for 600?"

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own submission, the lab is re-marked after a 10-minute conversation with the instructor, with the correctness criterion scaled as follows.

| Spot-check result | Correctness criterion kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function they wrote, traces one input through it, and says why the key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot trace a second function |
| Weak | 40% | Can run the code but cannot say where a number came from |
| None | 0% | Cannot explain the submitted work |

## Late work

A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and scores 0. Extensions for illness or other documented reasons follow the university policy. If Lab 14 is at risk, talk to the instructor before the deadline, because the final demo cannot run without a scheduler.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("asked an assistant why `heapq` compared my dictionaries"). You may not submit code you cannot explain, and you may not copy measurements, traces or tuning tables. Every number in a report must come from a run you did yourself, with the settings recorded. In pair parts (Labs 05 and 11), both partners must be able to explain all of the pair's code.
