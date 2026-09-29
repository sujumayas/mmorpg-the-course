# MMO404 · Lab 04: Priority allocator

**Week:** 4 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 4 lecture](../lectures/w04-replication-prioritization-and-relevancy.md) into code you trust. You implement the priority function, the fair-share (water-filling) rule and the priority accumulator, check them against the lecture's tables, and then run a seeded 400-entity scene to see what each falloff does to on-screen error. You finish with a priority design for a real scene that you can defend with numbers.

## Starter materials

Folder [`lab04-starter/`](lab04-starter/README.md). Standard library Python only.

- `priority.py`: TODOs for `falloff`, `priority`, `priority_speed`, `fair_rates` and `Accumulator.pick`. Given code builds the scene (`make_scene`, `step`), runs it (`run_scene`) and writes a CSV. `--check`, `--scene` and `--speed` modes.

## Steps

1. **By hand first.** Before writing code, compute `λ` and the update interval of each group for the lecture's section 2 table with `B = 16` instead of 20. Write the numbers down.
2. **The model.** Implement `falloff`, `priority`, `priority_speed` and `fair_rates`. Run `python priority.py --check` until only the accumulator fails. Then call `fair_rates` with `B = 16` and compare it with step 1.
3. **The accumulator.** Implement `Accumulator.pick` with ties broken by the lower index. Run `--check` until it prints `all checks passed`. In the lecture table, the fair share gives party members 1.68 ticks and the accumulator gives 2.00. Explain the difference in three sentences, and find the smallest budget at which the accumulator sends party members every tick.
4. **Three falloffs.** Run `python priority.py --scene scene.csv`. Make one chart of angular error by class, with one bar group per falloff. Which falloff gives the three player classes the most equal error? Relate your answer to the angle formula in lecture section 2. Why do NPCs show a lower error than players under the inverse falloff, even though their class weight is half?
5. **Speed.** Run the scene again with `--speed`. The loot never moves. How many slots per tick did it use before and after, and where did those slots go? Is there any reason to keep loot's priority above zero?
6. **A crowd.** Copy `CLASSES` and add a class of 150 NPCs at 30 m, weight 1, speed 3. Report how much each player class's angular error rises, and compare with the prediction from the lecture's "add crowd" rule (every uncapped interval grows by the ratio of total priorities).
7. **Your design.** Take one scene card from the lecture's in-class activity. Write a priority function for it (class weights, falloff, speed term, relevancy radius with hysteresis, and a maximum interval if you want one). Encode it as a new `CLASSES` table and run it. Report the interval and angular error of every class and the budget share the floor costs.

## Deliverable

Your finished `priority.py`, `scene.csv` and `scene_speed.csv`, the chart from step 4, and a report (PDF or Markdown, at most three pages) with the hand calculation from step 1, the answers to steps 3 to 6, and the design from step 7 with its numbers. Submit before the week 5 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | `--check` passes; hand calculation for `B = 16` agrees with the code | Passes, hand calculation missing or wrong | Fails the check | 20% |
| Accumulator analysis | Whole-tick snapping explained; smallest budget for every-tick party members found and justified | Explanation present, budget guessed | Missing | 15% |
| Falloff comparison | Chart correct; the equal-error result tied to the angle formula; the NPC speed effect explained | Chart present, explanation thin | No chart | 20% |
| Speed and crowd | Slot counts before and after; crowd effect measured and compared with the ratio prediction | One of the two done well | Missing | 20% |
| Design | Every weight justified by a player need; numbers for every class; hysteresis and floor cost stated | Numbers present, some unjustified | Missing or copied from the lecture | 20% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
