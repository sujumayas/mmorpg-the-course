# CS203 · Final demo brief: an NPC ecosystem

**Weight:** 50% of the course grade.
**Assigned:** week 7. **Milestone 1:** end of week 9. **Milestone 2:** end of week 12. **Final submission:** start of week 15, followed by a 20-minute demo and viva in week 15.
**Work mode:** individual, or a pair with a contribution statement. In a pair, each partner answers the viva questions alone, and the pair must meet the stretch requirements marked below.
**Lectures:** all fourteen, most directly [week 1, the five tests](../lectures/w01-game-ai-vs-academic-ai.md), [week 2, steering](../lectures/w02-steering-behaviors.md), [week 4, A*](../lectures/w04-a-star-and-heuristics.md), [weeks 6 to 9, decision making](../lectures/w06-finite-state-machines.md), [week 10, perception](../lectures/w10-perception-systems.md), [week 11, group tactics](../lectures/w11-group-tactics-and-formations.md), [week 12, threat tables](../lectures/w12-mmo-mob-ai-leashing-aggro-threat-tables.md) and [week 14, frame budgets](../lectures/w14-performance-ai-lod-and-time-slicing.md).

## What this component is for

Each lab tests one technique in isolation, on a scripted trace. This assessment asks you to put several of them into one small world where NPCs of different kinds share space, notice each other and the player, and make decisions that affect one another. Then it asks you to defend that world with numbers. An ecosystem that "looks lively" earns little here. One that states its switch points, its break-even exposure, its budget and the reaction delay each NPC pays, and shows a player can read and beat it, earns a lot.

It assesses all three course outcomes. Your pathfinding assesses "implement A* and navigation meshes". Your NPC types assess "build NPC behavior with FSMs, behavior trees and utility AI". Your design document and the viva assess "design AI for readability and fairness", which carries the most marks, because it is the point of the course.

## What you build

A top-down 2D world, about 40 × 40 m or a grid of similar size, with at least three kinds of NPC and one player. The player can be controlled by keyboard in the visual mode and by a scripted route in the headless mode. Pick a setting that gives your NPCs reasons to interact. Some examples follow.

- **A village at night.** Villagers go about a schedule, wolves hunt livestock at the edge of the woods, guards patrol and respond to noise, and the player sneaks through.
- **A dungeon floor.** Goblins in packs share an attack grid around the player, a shaman heals them, rats flee from everything, and a mini-boss runs a short script.
- **A market.** Merchants, thieves and watchmen, with the player as a pickpocket or as the watch captain.

Keep the art plain. Circles, squares and text labels are enough, and nothing about the visuals is marked. Do not use copyrighted characters, sprites or logos.

### Technical rules

- **Language.** Python 3.10 or later. The simulation uses the standard library only. You may draw with pygame, tkinter or a text renderer, or write a self-contained HTML page that replays your event log. Another language needs the instructor's written approval, under the same rules.
- **Headless mode.** `python ecosystem.py --headless --seed N --seconds S` runs the world with the scripted player, prints a summary and writes an event log to CSV. It must run with the course interpreter, `.venv/bin/python`, from a clean copy of your submission, without importing any drawing library. Markers use this mode for every measurement.
- **Determinism.** The same seed gives the same event log, line for line. Every random choice draws from one seeded `random.Random`.
- **A debug overlay.** In visual mode, each NPC shows its current state or action, and its awareness meter where it has one. A key toggles the overlay. In headless mode, the same information goes to the event log.

### Required features

Each item names the lab that gives you a starting point. You may reuse your own lab code freely.

1. **Movement (Lab 02).** NPCs move with steering. Destinations where an NPC must stop use arrive, with the slowing radius derived from `b = v² / (2a)` for that NPC's body. At least one group uses separation.
2. **Pathfinding (Lab 04 or Lab 05).** A* on a grid with terrain costs, or a navmesh with the funnel algorithm. State your heuristic and show with Lab 04's `max_overestimate` tool, or an argument, that it is admissible on your map.
3. **Two decision methods (Labs 06 to 09).** At least two NPC types use different methods from FSM, behavior tree, utility and planner. Each choice is justified in `DESIGN.md` with the week 9 comparison table in mind. Pairs use three.
4. **Commitment.** At least one decision uses a time lock, a margin, a hysteresis band or a commitment bonus (weeks 6 and 8), with the number chosen from a measured switch cost or noise level.
5. **Perception (Lab 10).** At least one NPC type has a fill-and-drain awareness meter with a suspicious state and hysteresis. Hearing uses path distance, not straight-line distance.
6. **A group rule (Lab 11 or Lab 12).** One group interaction is governed by tokens, roles, an attack grid or a threat table. Its capacity or multiplier is chosen from the lecture model.
7. **A frame budget (Lab 14).** All thinks run through a budgeted scheduler with a near tier. Measure each NPC type's real think cost with `time.perf_counter_ns` over at least 1,000 thinks, and use those costs as `c` in the scheduler. The headless summary prints worst frame, average frame, and near and far wait in milliseconds.
8. **A scripted moment (Lab 13, pairs only).** One timed or HP-gated event, such as a boss phase, a curfew bell or a reinforcement wave, written as data.

## The design document

`DESIGN.md`, 1,500 to 2,500 words, with these sections.

1. **The experience.** In three sentences, what the player should feel and do. Name the week 1 experience goal.
2. **The cast.** One table row per NPC type with its decision method, perception, movement body (`max_speed`, `max_accel`, `b`, slowing radius) and think cost.
3. **The five tests.** One table per NPC type scoring readable, beatable, varied, cheap and authorable, with a mechanism and a number for each, not an opinion.
4. **The numbers.** Every tuning value with the formula it came from. At least the slowing radius, one commitment value, one switch point (utility) or one priority order (tree) with its reaction delay, `f*` at two distances, the group capacity or threat margin `S`, and the scheduler budget with `k`, near wait and far wait.
5. **What the player can exploit.** At least two exploits you found in your own world, and for each whether you kept it (as a deliberate player win, like Days Gone's flanks) or fixed it, and how.
6. **What you would change at ten times the NPC count.** Using your scheduler numbers, which wait breaks first and what LOD change you would make.

## The evidence report

`EVIDENCE.md` holds three experiments. Each one has a question, a prediction written before the run and dated, the headless commands with seeds, a table of results over at least 5 seeds, and a paragraph comparing the prediction with the result.

1. **Commitment on and off.** Run your world with the commitment rule from feature 4 removed and then restored. Report switches per minute and the share of time the NPC spends on its main action.
2. **Perception tuning.** Run the scripted player along a careful route and a careless route at two forget times. Report first-alert times and compare with `f* = T / (T + F)`.
3. **Budget against population.** Run with your normal NPC count, then double and quadruple it. Report worst frame, near wait and far wait, and compare each with the week 14 formulas.

## Deliverables

- A repository or zip with the simulation, the headless mode, the visual mode or replay page, and any map files.
- `README.md` with the commands to run the visual mode, run headless, reproduce each experiment, and replay one seed. They must work from a clean copy on the lab machines.
- `DESIGN.md` and `EVIDENCE.md` as above.
- The CSV event logs behind every table in `EVIDENCE.md`.
- A 90-second screen recording of the visual mode with the debug overlay on, showing each NPC type making at least one decision.
- Pairs only: `CONTRIBUTIONS.md`, one paragraph each, naming the files each partner wrote.

## Milestone 1: design proposal (end of week 9, 10 points)

Two pages, before most of the code exists. The setting and experience goal in three sentences, the cast table from `DESIGN.md` section 2 with planned decision methods, a sketch of the map, the five tests for your most important NPC type, and the formulas you will use to set four tuning values. Feedback comes back within a week. Plans may change later, but `DESIGN.md` must say what changed and why.

## Milestone 2: running skeleton (end of week 12, 15 points)

A 5-minute demo in the lab session. The world runs headless from a seed and prints a summary. At least two NPC types move with steering and pathfinding, one of them decides with its chosen method, and all thinks go through your scheduler. Bring a one-page note with your measured think costs, the scheduler's worst frame and waits at your planned NPC count, and one bug you found by reading the event log.

## Demo and viva (week 15, 20 minutes)

You run your submission from a clean copy on a lab machine while two examiners watch. Every student follows the same steps.

1. **Start (2 min).** Visual mode from the README commands, debug overlay on.
2. **Tour (4 min).** Walk the examiners through one decision of each NPC type as it happens, naming the state, branch, score or plan on the overlay.
3. **Play (4 min).** An examiner takes the controls and tries to beat or exploit one NPC. You explain what the NPC perceives and why it reacts as it does, with a number from your design document.
4. **Headless (3 min).** The examiner picks a seed and an NPC count. You run headless and read out the worst frame and waits, and compare them with your formula.
5. **Questions (7 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your own numbers and code. At least one is a compute question and one is a trace through your own decision code.

## Rubric

### Milestones (25 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: cast and method choices | 5: every NPC type has a method justified against the week 9 table and a named experience goal | 3 to 4: one choice unjustified | 1 to 2: methods listed with no reasons | 0 | 5 |
| M1: five tests and formulas | 5: five tests with mechanisms for the key NPC; four formulas with the inputs they need | 3 to 4: one test or formula vague | 1 to 2: opinions instead of mechanisms | 0 | 5 |
| M2: skeleton demo | 10: seeded headless run; two NPC types with steering and paths; one decision method; scheduler in the loop | 6 to 9: runs, one element missing | 2 to 5: visual only, or no scheduler | 0 to 1 | 10 |
| M2: first measurements | 5: measured think costs, scheduler numbers compared with the week 14 formula, one log-found bug | 3 to 4: measured but not compared | 1 to 2: estimates only | 0 | 5 |

### Final submission, demo and viva (75 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Movement and pathfinding | 9 to 10: arrive radii from `b`; separation in a group; admissible heuristic shown; no visible stalls or wall scraping in the recording | 7 to 8: one of those missing | 4 to 6: paths work, tuning not derived | 0 to 3: straight-line movement or broken paths | 10 |
| Decision making | 13 to 15: two (pairs three) methods, each suited to its NPC; commitment value chosen from a measured cost; priorities or switch points stated with reaction delays | 10 to 12: methods work, one choice or number weak | 6 to 9: one method only, or visible dithering | 0 to 5: hard-coded behavior | 15 |
| Perception | 9 to 10: fill-and-drain meter with hysteresis; path-based hearing; `f*` computed and matched by experiment 2 | 7 to 8: meter works, experiment thin | 4 to 6: instant cone or straight-line hearing | 0 to 3: NPCs read the player's position directly | 10 |
| Group rule | 9 to 10: tokens, grid or threat table with capacity or `S` from the model; waiting members stay busy | 7 to 8: works, number not derived | 4 to 6: rule present, visible idling or pile-ups | 0 to 3: missing | 10 |
| Budget and scheduler | 9 to 10: measured think costs; near tier; experiment 3 matches the formulas at three populations; one LOD change argued | 7 to 8: one population off or unexplained | 4 to 6: scheduler present, no measurements | 0 to 3: all agents think every frame | 10 |
| Readability and fairness (`DESIGN.md`) | 9 to 10: five tests with mechanisms and numbers for every NPC type; two exploits found and decided; the ten-times section uses the formulas | 7 to 8: one section thin | 4 to 6: tests scored by opinion | 0 to 3: missing | 10 |
| Demo and viva | 9 to 10: all five steps from a clean copy; each decision explained with a number; answers use your own code and data | 7 to 8: one step needs help | 4 to 6: two steps fail, or answers vague | 0 to 3: cannot run or explain | 10 |
| **Total** | | | | | **75** |

The final demo mark is the milestones plus the final, out of 100, multiplied by 0.50.

## Rules and advice

- **Your labs are the parts.** Most of the ecosystem is Lab 02's steering, Lab 04's A*, one or two of Labs 06 to 09, Lab 10's meter, Lab 11's or 12's group rule and Lab 14's scheduler. The new work is making them share one world and one clock, and measuring the result.
- **Log from day one.** Write the event log in week 10, before the world is interesting. Most bugs in a multi-agent world are found by reading a log, not by watching.
- **Predict, then measure.** Every experiment rewards a dated prediction and an honest account of the gap.
- **Small beats big.** Three NPC types with numbers behind every choice beat eight types with none. Every extra type is another row in every table you must fill in.
- **Late submission.** Up to 48 hours late, the final is marked out of 60 instead of 75, and the demo is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** The rules in the [labs brief](labs-brief.md#academic-integrity) apply. Every measurement must come from your own runs, with seeds recorded. In the viva you must be able to explain every file you submit.
