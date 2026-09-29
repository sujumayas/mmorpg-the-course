# GD201 · Blockouts brief

**Weight:** 40% of the course grade.
**What counts:** ten blockout labs (70 points) and the week 8 blockout crit (30 points).
**When:** each lab is due before the next week's lecture unless the lab says otherwise. The crit runs in the week 8 lab session. The response to the crit is due before the week 9 lecture.
**Work mode:** individual. You may playtest each other's levels, and you should.

## What this component is for

A level exists to be played, so this component grades levels you can play, not drawings of them. Every lab here ends in something built at true scale in an engine or on a grid, measured with a stopwatch or a script, and changed because a tester did something you did not expect.

It assesses two of the course outcomes most directly. "Plan levels with pacing graphs and critical paths" is assessed in Labs 01 to 03 and in the crit, where your level has to hold the lesson plan, the critical-path timings and the intensity curve you designed. "Use landmarks, sightlines and affordances to guide players" is assessed in Labs 04, 05, 06, 07 and 12, where you size landmarks, place signposts, and measure what a position can see.

The component also builds the parts of your [final zone](final-zone-brief.md). Lab 04's landmark tool, Lab 10's connection plan, Lab 12's spawn analysis and Lab 13's metrics sheet all go into its design document.

## The labs

| Lab | Week | Title | What you build | Can be dropped? |
|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Checkpoint placement and a one-verb lesson | Paper level, measured `p̂`, checkpoint placement | yes |
| [02](../labs/lab02.md) | 2 | Blockout and critical path | Your first playable blockout, three test rounds | **no** |
| [03](../labs/lab03.md) | 3 | Intensity graph for your blockout | Beat chart and revised encounters in the Lab 02 blockout | yes |
| [04](../labs/lab04.md) | 4 | Landmark legibility audit | Fixed sample zone, engine check of landmark sizes | yes |
| [05](../labs/lab05.md) | 5 | Signpost playtest and model | Greybox route with a signpost playtest | yes |
| [06](../labs/lab06.md) | 6 | Chokepoint simulator and three-lane arena | 6-versus-6 arena tuned by geometry | **no** |
| [07](../labs/lab07.md) | 7 | Return ratios in a vertical level | Vertical greybox with a one-way drop and a shortcut | yes |
| [10](../labs/lab10.md) | 10 | Errand costs, shortcuts and gate slack | Connection plan for your final zone | yes |
| [12](../labs/lab12.md) | 12 | Sightline heatmaps and spawn redesign | Redesigned spawn meeting exposure targets | yes |
| [13](../labs/lab13.md) | 13 | Metrics gym and jump audit | Metrics gym and an audited critical path | **no** |

Your best eight of the ten count. Labs 02, 06 and 13 always count. Lab 02 is the first blockout the crit is built on, Lab 06 is the only combat space you build, and Lab 13's metrics sheet is required by the final zone. Dropping a lab removes its mark, not the work. If the final zone needs a tool you skipped (Lab 10's `errand_cost`, for example), you still have to write it.

Labs 08, 09, 11 and 14 belong to the [analysis component](teardown-brief.md).

## How each lab is marked

Every lab has its own rubric with four to six criteria, each with a weight and four bands. A criterion earns `weight × band ÷ 4`, so a criterion weighted 25% and marked 3 earns 18.75 points. The lab's mark is the sum, out of 100.

| Band | Label in the lab rubric | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the lecture or the checker |
| 3 | Adequate, strong | 75% | Correct, with one piece of evidence or explanation missing |
| 2 | Adequate, weak | 50% | Works in outline, explanation thin or one number off |
| 1 | Missing or wrong, partial | 25% | Attempted, but the checker fails or the reasoning uses the wrong model |
| 0 | Missing or wrong | 0% | Not submitted, or unrelated to the lab |

The labs part of this component is the mean of your eight counted lab marks, multiplied by 0.70. A single lab is worth about 3.5% of the course.

### Checkers and code

Every lab has a checker script (`check_lab01.py` and so on). Markers run it on a clean copy of your folder with the course interpreter, `.venv/bin/python`. The checker criterion scores its band from the pass count in the lab's rubric. Code that only runs on your machine, because of an absolute path or a missing file, counts as failing. Do not edit the checkers.

### Playtest evidence in every lab

A lab that asks for a playtest is marked on what testers did, not on what you think they would do. Every playtest you submit follows the same rules.

- **Fresh testers.** Each round uses testers who have not played that version of the level. Classmates are fine. You are never your own tester.
- **Observe, don't coach.** Follow GD101 week 7. Write down behaviour ("walked past the ladder twice, then opened the map"), not interpretation ("didn't understand the ladder"). If you had to intervene, say so and mark that run.
- **Record the build.** Every log row carries the date and a build name or number. A result from last week's layout is not evidence about this week's.
- **Time it.** Critical-path times, valley lengths and walk-backs are measured with a stopwatch or a timer script, not estimated.
- **Consent and privacy.** Tell testers what you record. Use an anonymous tester ID in every CSV. Delete raw recordings when the course ends.

### Predictions before results

Several labs compare a model's number with a measurement: Lab 02's critical-path time, Lab 04's landmark pixel heights, Lab 06's fall and rotation times and Lab 13's gap limits. Compute and date the model's number before you measure. A prediction written after the measurement, or changed to match it, earns the lowest band for that criterion. A wrong prediction with honest working loses nothing, as long as you then explain the difference.

## The week 8 blockout crit (30 points)

A crit is a design review. You show your work, the room plays it and asks questions, and you defend or change your choices. It is the midpoint check that your blockouts add up to levels, not a pile of lab exercises.

### What you bring

- **Blockout A, your teaching level.** The Lab 02 blockout, as revised by Lab 03's pacing, with at least one landmark sized with Lab 04's tool and a signpost language from Lab 05. It must be playable from start to finish.
- **Blockout B, a combat or vertical space.** Your Lab 06 arena or your Lab 07 vertical space, your choice.
- **A one-page evidence sheet.** For Blockout A: the lesson matrix, the critical-path time from the tool next to the stopwatch time for each round, the intensity curve with its four measurements, and the landmark legibility from the start point. For Blockout B: the fall times and rotation times (arena) or the return ratios before and after the shortcut (vertical space).
- **The revision log** for Blockout A, covering every round since Lab 02. At least four rounds by week 8, each with fresh testers.

### How the session runs (15 minutes per student)

1. **Cold play (5 min).** A classmate who has not seen Blockout A plays it while you stay silent. The marker times the critical path and notes where the player hesitates.
2. **Your case (4 min).** Walk through the evidence sheet. Compare the cold play with your predictions.
3. **Questions (6 min).** The marker and the room ask questions in the style of the [exam bank](exam-bank.md), using your own numbers. Typical ones are "Your checkpoint before the gear room gives `r = 20` s. What penalty ratio does that give a learner at `p = 0.3`?" or "From which start point is your weenie closest to its `d_max`, and what happens to it at the widest field of view you allow?"

### Response to the crit (due before the week 9 lecture)

Pick the most important problem the crit exposed. Change the level to fix it, run one more round with two fresh testers, and submit a half-page note: the problem as observed, the change, the prediction for the new version and the result.

### Crit criteria

**Playable blockout at true scale (8 points).**
- 7 to 8: both blockouts run from start to finish with the default controller; grid floor, scale figure and labelled placeholders present; sizes are whole multiples of one base unit; doorways and walls follow the week 2 checklist.
- 4 to 6: playable, with one or two scale or checklist gaps.
- 1 to 3: runs only in parts, or dressed with art instead of measured.
- 0: missing.

**Playtest evidence (8 points).**
- 7 to 8: four or more rounds with fresh testers; behaviour recorded separately from interpretation; every change in the log tied to an observation; stopwatch times every round.
- 4 to 6: enough rounds, but some changes are not tied to observations or some times are missing.
- 1 to 3: fewer than three rounds, or notes written from memory.
- 0: none.

**Numbers from the models (8 points).**
- 7 to 8: the evidence sheet's predictions match the lecture models; the cold play is compared with them; every large gap is explained by a named place in the level.
- 4 to 6: numbers present and mostly right, comparison thin.
- 1 to 3: numbers asserted without working, or from the wrong model.
- 0: none.

**Response to the crit (6 points).**
- 5 to 6: the change targets the crit's most important problem, the prediction was written first, and the retest result is reported honestly, including if it failed.
- 3 to 4: a sensible change and a retest, but the prediction or the link to the crit is missing.
- 1 to 2: cosmetic change, or no retest.
- 0: not submitted.

## Rubric

| Part | Criterion | Points |
|---|---|---|
| Labs | Mean of the eight counted lab marks × 0.70 | 70 |
| Crit | Playable blockout at true scale | 8 |
| Crit | Playtest evidence | 8 |
| Crit | Numbers from the models | 8 |
| Crit | Response to the crit | 6 |
| **Total** | | **100** |

The component mark out of 100 is multiplied by 0.40 for the course grade.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, taken from the [exam bank](exam-bank.md) and rewritten with the student's own level. A spot check never lowers a mark for a slip. It confirms the work is yours. If you cannot explain your own code or your own numbers at all, the lab is re-marked after a 10-minute conversation with the instructor.

| Band | Points kept from the lab mark | What the student shows |
|---|---|---|
| Full | 100 | Explains each function they wrote, reproduces the lab's key number by hand, and says what a tester did that changed the level |
| Partial | 70 | Explains the main function and the key number, but cannot answer a "what if the run speed rose 20%" change |
| Weak | 40 | Can run the code and open the level, but cannot say where a number came from |
| None | 0 | Cannot explain the submitted work |

## Rules

- **Engines and assets.** Use any engine from the labs (Unity, Unreal, Godot or TrenchBroom) with its default controller, and write the controller's run speed and jump on your metrics sheet from Lab 13 onward. Grey materials, grid textures and labelled boxes only. No final art, no purchased or ripped assets, and no copyrighted characters, logos or maps.
- **Late work.** A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two dropped labs. Labs 02, 06 and 13 cannot be dropped, so talk to the instructor before the deadline if one is at risk. A missed crit slot can be rescheduled once within week 8 for a documented reason. Extensions for illness or other documented reasons follow university policy and do not use up a drop.
- **Academic integrity.** You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an engine feature, and you must say so in one line in the lab report. You may not submit code you cannot explain, and you may not copy another student's measurements or playtest logs. Testers' results must come from sessions you ran.
