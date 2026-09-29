# GD201 · Final zone brief: greybox zone and design document

**Weight:** 40% of the course grade.
**Assigned:** week 9. **Milestone 1:** end of week 10. **Milestone 2:** end of week 13. **Final submission:** start of week 15, followed by a 20-minute crit and viva in week 15.
**Work mode:** individual.
**Lectures:** all fourteen, most directly [week 3, pacing](../lectures/w03-flow-pacing-and-intensity-graphs.md), [week 4, landmarks](../lectures/w04-guiding-the-player-landmarks-light-weenies.md), [week 9, POI density](../lectures/w09-open-world-structure-poi-density.md), [week 10, hubs and gating](../lectures/w10-hubs-spokes-and-gating.md), [week 11, shared spaces](../lectures/w11-shared-spaces-designing-for-many-players.md), [week 12, spawns and contested resources](../lectures/w12-spawn-design-and-contested-resources.md), [week 13, metrics](../lectures/w13-metrics-player-speed-jump-scale.md) and [week 14, heatmaps](../lectures/w14-playtesting-levels-with-heatmaps.md).

## What this component is for

The labs test one idea at a time. A real zone has to satisfy all of them at once, for players who arrive at different skill levels, in groups and alone, on launch day and a year later. This component asks you to build one. You make a playable greybox of a shared outdoor zone for an online RPG, and write the design document that explains, with numbers, why it is laid out the way it is.

It assesses all three course outcomes. The teaching path, beat chart and intensity graph assess "plan levels with pacing graphs and critical paths". The landmark plan, signpost language and spawn sightlines assess "use landmarks, sightlines and affordances to guide players". The POI density, hub connections, population plan and contested camps assess "design zones for shared, persistent use by many players".

Two numbers carry the course's signature examples, and markers look for both. The first is **walking-speed math**: the seconds between points of interest, predicted from your controller's speed and your POI spacing, then measured in the greybox. The second is **spawn camping as geometry**: the sightline exposure `E` and camp positions `K` of every respawn point in the zone.

## What you build

A playable greybox of one zone in an engine from the labs (Unity, Unreal, Godot or TrenchBroom), with the default character controller whose metrics you measured in [Lab 13](../labs/lab13.md). Grey materials, grid textures and labelled placeholder boxes only. No art is marked, and you must not use purchased or ripped assets, copyrighted characters, logos or maps.

### Size and speed

- A playable area of at least 400 m × 400 m and at most 1 km × 1 km, built at true scale.
- A **design speed** stated in m/s, taken from your controller's measured run speed or a mount speed you implement. Every travel time in the document uses it.
- A **design gap** between points of interest, between 20 and 60 seconds at the design speed, chosen and justified with week 3's idea of rest between peaks.

### Required contents

1. **An entry point and a teaching path.** Where a new character arrives, and the first five beats it meets, written as a lesson matrix (week 1). At least one verb or mechanic is introduced, practised and tested along it.
2. **A hub and at least six destinations.** A quest hub (a town, a camp, an outpost) and at least six points of interest the zone's quests or objectives point at. The connections form a topology you chose on purpose (week 10), with at least one loop-back shortcut or a stated reason for having none.
3. **A landmark plan.** One global landmark (the weenie) legible from every start and respawn point, and at least two district landmarks (week 4). Sizes come from `d_max` at the widest field of view you allow.
4. **A signpost language.** The signals your zone uses, what each means, and where the loud ones sit on the critical route (week 5).
5. **A combat space.** A contested site with at least one chokepoint and a flank or second lane, with cover whose value you state (week 6).
6. **Height.** At least one area with three height levels, a one-way drop and a shortcut unlocked from the far side (week 7).
7. **One environmental story beat.** At least three clues, their tiers and the reading rule `k` you intend (week 8).
8. **At least one gate.** A key, count or level gate, with its slack (week 10).
9. **Camps.** At least four camps, each labelled competitive or cooperative, and at least one competitive camp whose spawns you checked against `P*` (weeks 11 and 12).
10. **Respawn points.** At least one graveyard or respawn point, with its exits, `E` and `K` computed on a grid sketch of its surroundings (week 12).
11. **Telemetry.** Logging of position once per second, deaths or other failure events, and progress events, in Lab 14's CSV format with anonymous tester IDs.

## The design document

3,000 to 5,000 words plus tables and figures, as `DESIGN.md` or a PDF. Every number carries its unit and says whether it is a model value or a measurement. Use these sections.

1. **The zone in one page.** Its purpose in the game, the player level range, the design speed and gap, a top-down map you drew with every place named, and the critical route from entry to hub marked.
2. **Metrics sheet.** From Lab 13, corrected against your gym: box size, eye height, step, jump (every climbing verb), run speed, safe drop, and the margins you chose. List every jump and blocking wall on the critical route with its audit band.
3. **Teaching and pacing.** The lesson matrix for the teaching path. A beat chart for the critical route, and its intensity curve with the four measurements from week 3. Where the valleys are, and what fills them.
4. **Guidance.** The landmark legibility matrix for every start and respawn point (Lab 04's tool). Contrast ratios for the landmarks at the worst time of day. The signpost language and the predicted find rate for the critical route under a stated scanner and tunneler population (Lab 05's model).
5. **Structure and walking-speed math.** POI spacing and density from the design gap and speed. The travel gap for every leg of a nearest-neighbour tour (Lab 09's tool), the longest leg and the largest empty circle. The visible count `N_visible` at your landmark distance. Then measure the same table in the greybox. Time each leg between at least five neighbouring POI pairs three times and report the median, next to the model's gap. Explain each difference over 15%.
6. **Connections and gates.** The zone as a graph with measured link lengths, its mean errand cost `E` in metres and seconds, the pairwise mean, the shortcut you built and what it saved. The slack at every gate. Any errand a key gate adds.
7. **Combat and height.** The chokepoint cost for your expected attacker and defender counts, with cover and area damage stated. Rotation time against lane fall time. Out times, back times and return ratios for the vertical area before and after its shortcut.
8. **Shared use.** The population plan from Lab 11: `H`, `f`, `A`, `r`, the band for competitive and cooperative camps, `P_min` and `P_max`, and `N_camp` and `N_open` at launch, at 20% and at 3% of launch, with and without copies. For each competitive camp, `P*` and the quest time at the expected camp population. The credit rules you chose.
9. **Spawns.** An exposure heatmap of each respawn point's surroundings on a grid, `E` at the spawn and at each exit, `K`, and the walk-back time to the nearest objective. If `K` is above 5, say why that is acceptable here.
10. **The story beat.** Clues, tiers, `k`, the predicted understanding rate, and what testers actually said.
11. **Playtest evidence.** See below.
12. **What you would change next.** The two problems you know about and have not fixed, with the model's prediction for a fix and the test that would confirm it.

## Playtest evidence

The zone must be played by people who did not build it, and changed because of what they did.

- **At least three rounds**, one of them at Milestone 2, with at least three fresh testers each. At least eight testers in total. Classmates are fine. Record the build number with every result.
- **Telemetry from every round**, loaded with your Lab 14 `heatmap.py`. Show the death (or failure) count map and the shrunk-rate map with the `k` and cell size you chose before looking, plus one position map at a fixed time into the first session (the Jungle method from week 14). Report `v` next to every rate.
- **Observation notes** for the hottest cell on the shrunk-rate map, covering at least two failures there, written as behaviour.
- **A revision log**, one row per round: date, build, testers, critical-route time, problems observed, the change made for each, and the round that checked it.
- **The two signature checks, measured.** The measured travel gaps from section 5 of the document, and a run where one tester stands on the best camp position of your main respawn point while another respawns, with what happened.

Follow the playtest rules in the [blockouts brief](blockouts-brief.md#playtest-evidence-in-every-lab): fresh testers, no coaching, stopwatch times, consent and anonymous IDs.

## Milestone 1: zone plan (end of week 10, 10 points)

A two-page plan before most of the greybox exists. It covers the zone's purpose in three sentences, the design speed and gap, the POI count those imply for your area, a hand-drawn top-down map with the hub, destinations, landmarks and respawn points, the connection graph with its `E`, and each landmark's height from its `d_max`. Feedback comes back within a week. Numbers may change later, but the design document must say what changed and why.

## Milestone 2: playable greybox (end of week 13, 15 points)

A short demo in the week 13 lab session, 5 minutes per student. The zone runs from entry to hub to at least four destinations with your measured controller. Bring the corrected metrics sheet from Lab 13, the telemetry CSV from a first round with three testers (in the CSV format Lab 14 uses: player, run, time, kind, x, y), and a one-page note comparing three measured POI gaps with the model's gap. You analyse this first round with Lab 14's tools in week 14.

## Crit and viva (week 15, 20 minutes)

You run your submission from a clean copy on a lab machine while two examiners watch. Every student follows the same steps.

1. **Arrival (3 min).** The examiner starts a new character at the entry point and plays the first beats of the teaching path while you stay silent.
2. **Landmarks (2 min).** The examiner picks a start or respawn point. You show the weenie from it and read its screen fraction from your legibility matrix.
3. **Walking-speed math (3 min).** The examiner picks two neighbouring POIs. You predict the travel time from your document, then walk it while the examiner times you.
4. **Spawn (3 min).** You stand on the best camp position of your main respawn point and show which exits it covers. The examiner asks what one change would bring `K` down.
5. **Evidence (3 min).** Your shrunk-rate heatmap, the hottest cell, what testers did there, and the change you made.
6. **Questions (6 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your zone's numbers. At least one is a compute question, such as "your launch estimate doubles; how many copies now, and what happens to `N_camp`?"

## Deliverables

- The engine project, or an exported build for Windows or macOS, that runs from a clean copy on the lab machines, with a `README.md` saying how to start it and where the telemetry file is written.
- `DESIGN.md` (or a PDF) with the twelve sections above.
- Every CSV behind every table: telemetry, timings, signpost and clue logs.
- Your Python tools from the labs as used for the document, runnable with `.venv/bin/python`.
- Screenshots: the zone from above, the weenie from every start point, the vertical area's overlook, and the main respawn point's exits.

## Rubric

### Milestones (25 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: plan numbers | 5 to 6: speed, gap, POI count, `E` and landmark heights each computed correctly from the lecture models | 3 to 4: one number wrong or unjustified | 1 to 2: numbers guessed | 0 | 6 |
| M1: map and topology | 4: hub, destinations, landmarks and respawns placed; the topology choice is stated with its reason | 3: map complete, reason missing | 1 to 2: sketch without structure | 0 | 4 |
| M2: playable greybox | 7 to 8: entry, hub and four destinations playable at true scale with the measured controller; checklist from week 2 met | 5 to 6: playable with scale or checklist gaps | 2 to 4: partly playable | 0 to 1 | 8 |
| M2: first evidence | 7: metrics sheet corrected against the gym; three-tester telemetry logged per second and per failure with anonymous IDs; three measured gaps compared with the model | 5 to 6: one of the three thin | 2 to 4: two missing | 0 to 1 | 7 |

### Final submission, crit and viva (75 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Greybox build and scale | 9 to 10: every required content item present and playable; true scale; metrics audit clean on the critical route; readable without art | 7 to 8: one item thin | 4 to 6: two items missing or scale errors | 0 to 3: not playable end to end | 10 |
| Teaching and pacing | 7 to 8: lesson matrix follows the week 1 rules; beat chart durations measured; intensity curve with valleys that testers used as intended | 5 to 6: one element unmeasured | 3 to 4: chart and curve not matched to the build | 0 to 2: missing | 8 |
| Guidance | 7 to 8: every start point sees the weenie at the widest allowed field of view; contrast checked at the worst hour; signpost find rate predicted and compared with testers | 5 to 6: one start point or one check missing | 3 to 4: matrix present without comparison | 0 to 2: missing | 8 |
| Walking-speed math and structure | 11 to 12: model gaps and measured gaps side by side for five or more legs, differences over 15% explained; tour, empty circle and `N_visible` reported; `E`, pairwise mean, shortcut saving and gate slack correct | 8 to 10: one analysis thin or one difference unexplained | 4 to 7: model only, no measured gaps | 0 to 3: missing | 12 |
| Combat, height and spawns | 9 to 10: chokepoint cost, rotation race and return ratios correct; heatmap, `E` and `K` for every respawn point; `P*` for every competitive camp; the camp-position run reported | 7 to 8: one of these thin | 4 to 6: two missing | 0 to 3: most missing | 10 |
| Shared use | 6 to 7: population band, copies at three populations, competitive and cooperative camps and credit rules argued from the numbers | 4 to 5: numbers present, rules not argued | 2 to 3: one population only | 0 to 1: missing | 7 |
| Playtest evidence | 9 to 10: three or more rounds and eight or more fresh testers; telemetry every round; count, shrunk-rate and position maps with `k`, cell size and `v`; observation notes for the hottest cell; every change tied to an observation and rechecked | 7 to 8: one round or one map missing | 4 to 6: fewer testers, or maps without `v` | 0 to 3: little or no evidence | 10 |
| Crit and viva | 9 to 10: all six steps work from a clean copy; predictions made before the walk; answers use your own numbers | 7 to 8: one step needs help | 4 to 6: two steps fail, or answers vague | 0 to 3: cannot run or explain | 10 |
| **Total** | | | | | **75** |

The final zone mark is the milestones plus the final, out of 100, multiplied by 0.40.

## Rules and advice

- **Your labs are the parts.** Most of the document is Lab 04's legibility matrix, Lab 05's find rate, Lab 06's chokepoint numbers, Lab 07's return ratios, Lab 09's density audit, Lab 10's connection plan, Lab 11's population plan, Lab 12's spawn analysis, Lab 13's metrics sheet and Lab 14's heatmaps, run on one zone. The new work is making them agree with each other.
- **Measure early.** Add the telemetry logging in week 13, before the zone is finished. A logger added the night before submission has no rounds behind it.
- **Predict, then measure.** Every section rewards a model number written before the test and an honest account of the gap. A document where every prediction matches every measurement to the second gets checked closely.
- **Keep it small.** Meet the minimums well before you add more. Extra destinations earn nothing, and each one is another leg to time and another camp to check.
- **Late submission.** Up to 48 hours late, the final is marked out of 60 instead of 75, and the crit is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** The rules in the [blockouts brief](blockouts-brief.md#rules) apply. Measurements and playtest logs must come from your own sessions, with build numbers recorded. In the viva you must be able to explain every number in the document.
