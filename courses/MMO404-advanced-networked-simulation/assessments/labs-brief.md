# MMO404 · Labs brief

**Weight:** 40% of the course grade.
**What counts:** all 14 labs, weighted as in the table below. There are no dropped labs, because each week's lab is the only assessed practice of that week's model.
**When:** each lab is assigned in its week's session and is due before the next lecture, unless the lab says otherwise. Lab 14's slides and handout are due before your group's presentation slot, and its peer questions at the end of week 14.

## What this component is for

Every lecture in this course ends in a model you can compute: a tick cost, a seam cost, a water level, a controller, a conflict rate, a bill. The labs make you implement each model, reproduce the lecture's numbers from your own code, push the model somewhere the lecture did not go, and then write a one-page plan that a lead engineer could act on. The course outcome "optimize replication for massive battles" is assessed mostly here, in labs 01 and 03 to 07. The outcome "design distributed simulation across many servers" is assessed here in labs 02 and 08 to 13, and again in the [final demo](final-demo-brief.md).

Two labs carry more weight because the final demo is built on them. Lab 02's handoff protocol is the core of the demo, and Lab 09's epoch fencing is what keeps the demo correct when a server pauses. Lab 14 carries more weight because it is the case study presentation, the only group work in the component, and it cannot be redone after the week.

## The labs and their weights

| Lab | Week | Title | Feeds the final demo | Points |
|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Zone capacity | "what breaks first" section of the report | 6 |
| [02](../labs/lab02.md) | 2 | Seams and handoff | handoff protocol, seam cost sweep | 12 |
| [03](../labs/lab03.md) | 3 | Partitioning a crowded world | border placement | 6 |
| [04](../labs/lab04.md) | 4 | Priority allocator | ghost priority near the seam | 6 |
| [05](../labs/lab05.md) | 5 | Dead reckoning and shaping | per-client shaper | 6 |
| [06](../labs/lab06.md) | 6 | Battle budget | seeded replay, checksums | 6 |
| [07](../labs/lab07.md) | 7 | A dilation controller | one clock domain for both servers | 6 |
| [08](../labs/lab08.md) | 8 | Lookahead on the border | border lookahead rule | 6 |
| [09](../labs/lab09.md) | 9 | A mesh for a crowd | epoch fencing, pause test | 10 |
| [10](../labs/lab10.md) | 10 | Conflicts and convergence | chest policy, boss damage counter | 6 |
| [11](../labs/lab11.md) | 11 | Physics budget | islands across the seam (optional feature) | 6 |
| [12](../labs/lab12.md) | 12 | AI budget | bot and monster scheduling | 6 |
| [13](../labs/lab13.md) | 13 | The player-hour bill | cost section of the report | 6 |
| [14](../labs/lab14.md) | 14 | Case study teardown (group) | presentation skills for the viva | 12 |
| | | | **Total** | **100** |

Your labs component is the sum of `points × lab mark / 100` over the 14 labs, multiplied by 0.40. A 6-point lab is worth 2.4% of the course grade, Lab 02 and Lab 14 are worth 4.8% each, and Lab 09 is worth 4%.

Labs 01 to 13 are individual. You may talk through ideas with anyone, but the code and the report you submit must be your own. Lab 14 is marked per group for the slides and handout and per person for your answers in the question period and your peer questions, as its rubric says.

## How each lab is marked

Every lab has its own rubric with five to seven criteria, each with a weight, and the weights in each lab total 100%. Each criterion is scored in bands from 0 to 4. A criterion earns `weight × band ÷ 4`, so a criterion weighted 20% and marked 3 earns 15 points of that lab's 100.

| Band | Label in the lab rubric | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the lecture or the check |
| 3 | Adequate, strong | 75% | Correct, one piece of evidence or explanation missing |
| 2 | Adequate, weak | 50% | Works in outline, explanations thin or a number off |
| 1 | Missing or wrong, partial | 25% | Attempted, but fails the check or reasons from the wrong model |
| 0 | Missing or wrong | 0% | Not submitted, or unrelated to the lab |

Across the 14 rubrics, the criteria fall into the same five families. Use this table to see where the marks usually are before you start a lab. The exact weights are in each lab's own rubric.

| Criterion family | What earns the top band | Typical share of a lab |
|---|---|---|
| Model code | The lab's `--check` or test file passes on a clean copy; hand calculations agree with the code | 15 to 30% |
| Reproducing and validating the lecture | The lecture's table reproduced from your code; where the model and a simulation differ, the gap explained with a named cause | 15 to 20% |
| Analysis past the lecture | A sweep, a new population or a broken-on-purpose run, reported with numbers and units and explained in a few sentences | 15 to 25% |
| Design or plan | A one-page plan in which every setting is backed by a number you computed and every choice names what players pay for it | 20 to 30% |
| Writing | Plain sentences, one idea per paragraph, units on every number | 5 to 10% |

### Automatic checks

Most labs have a `--check` mode or a test file (`zone_capacity.py --check`, `handoff.py --check`, `seam.py --check`, `partition.py --check`, `priority.py --check`, `lod.py --check`, `battle.py --check`, `lockstep.py --check`, `test_tidi_control.py`, `test_lookahead.py`, `test_mesh.py`, `consistency.py --check`, `physics_budget.py --check`, `ai_budget.py --check`, `cost_model.py --check` and `teardown.py --check`). Markers run it on a clean copy of your folder with the course interpreter, `.venv/bin/python`. The model-code criterion cannot score above band 1 if the check fails there. Code that only runs on your machine because of an absolute path or a missing file is treated as failing. Code that special-cases the test inputs earns band 0 for that criterion.

### Hand calculations first

Every lab's first step asks you to compute something by hand before you write code: a capacity, a water level, a controller target, a finish-time table, a bill. Put the working in your report with units at every step. A hand calculation written after the code ran, or changed to match it, earns the lowest band for the criterion that asks for it. A wrong hand calculation with honest working loses nothing, as long as you then explain the difference.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own code and numbers. Typical questions are "Your sweep put the best band at 12 m. What would it do if handoffs cost twice as much?" or "Point to the line in your `merge` that makes duplicated snapshots harmless, and say what happens if it used `+`."

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor, using this scale.

| Band | Share of the lab mark kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot trace a second function or answer a "what if this constant doubled" question |
| Weak | 40% | Recognizes the code and can run it, but cannot say what it does or where a number came from |
| None | 0% | Cannot explain the submitted work |

## Late work

A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and scores 0. Lab 14's presentation cannot be moved, so a group that misses its slot without a documented reason scores 0 for the delivery and answers criterion. Extensions for illness or other documented reasons follow the university policy. If Lab 02 or Lab 09 is at risk, talk to the instructor before the deadline, because the final demo needs that code whatever its mark.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("used the Python docs for `heapq`; asked an assistant why my union-find recursed too deep"). You may not submit code you cannot explain, and you may not copy another student's sweeps, seeds or plots. Every number in a report must come from runs you did yourself, with the seeds and settings recorded. In Lab 14, every real-game number carries its source and era, and quotes are limited to one short phrase per source. The spot checks are designed around these rules.
