# GD201 · Analysis component brief: labs and level teardown

**Weight:** 20% of the course grade (the "analysis" line of the course assessment).
**What counts:** four analysis labs (60 points) and one level teardown of a shipped game (40 points).
**When:** each lab is due before the next week's lecture. The teardown is assigned in week 9 and due before the week 13 lecture.
**Work mode:** individual.

## What this component is for

The blockouts component asks whether you can build a level. This one asks whether you can read one, your own or someone else's, and say with numbers what it does to players. That is most of a level designer's working week: reading playtest data, auditing a zone someone else laid out, and explaining why a map that looks fine plays badly.

It assesses the outcome "design zones for shared, persistent use by many players" most directly, through Labs 09 and 11 and the teardown's open-world and shared-space models. It also assesses the reading side of the other two outcomes. Lab 08 reads a story playtest, Lab 14 reads a death heatmap, and the teardown reads a shipped level's pacing and guidance.

## The labs

| Lab | Week | Title | What you study |
|---|---|---|---|
| [08](../labs/lab08.md) | 8 | Clue reliability from playtest data | A 24-tester story playtest, then a beat in your own greybox |
| [09](../labs/lab09.md) | 9 | POI density audit | A 60-POI zone with a hidden dead zone and cluster, fixed for walkers and riders |
| [11](../labs/lab11.md) | 11 | Zone population planner | A Monte Carlo test of the neighbour model, and your final zone's population plan |
| [14](../labs/lab14.md) | 14 | Death heatmaps that don't lie | A simulated playtest, then telemetry from your own blockout |

All four count. None can be dropped. Each is marked with its own rubric, using the same bands as the [blockouts brief](blockouts-brief.md#how-each-lab-is-marked). A criterion earns `weight × band ÷ 4`, and the lab's mark is the sum out of 100. The labs part of this component is the mean of the four lab marks, multiplied by 0.60. Checkers, playtest rules, spot checks and late work follow the blockouts brief.

Three of these labs feed the [final zone](final-zone-brief.md). Lab 09's fixed layout is a starting point for its POI plan, Lab 11's population plan is a section of its design document, and Lab 14's instrumented blockout gives you the telemetry code for its playtests.

## The level teardown (40 points)

A **teardown** takes a shipped level apart into the decisions its designers made and puts a number on each. You pick the level. You measure it yourself. You explain what the numbers do to a player, and you propose one change.

### Choosing a level

Pick one of these, from any game you can play for at least three hours:

- a single-player level or chapter of at least 10 minutes;
- a competitive multiplayer map;
- an MMO or open-world area of at least 1 km², or a quest hub with the camps it sends players to.

State the game, the platform, the version or patch you played and the date. Levels change between patches, and your numbers belong to one version. Clear the choice with the instructor by the end of week 10. Two students may not tear down the same level unless their model sets differ.

### What you measure

Apply at least **three** models from different weeks of the course, and at least one of them from weeks 9 to 12 (POI density, hubs and gating, shared spaces, spawns and contested resources). For every model, measure its inputs yourself. The models and the measurements they usually need:

| Week | Model | Typical measurements |
|---|---|---|
| 1 | Retry cost `E[T]` and penalty ratio | Attempt time, respawn delay and walk-back, timed; your `p̂` over several attempts |
| 3 | Intensity curve | A threat log every 10 s over a recorded run, on a scale you state |
| 4 | Landmark legibility | Screenshot heights against an object of known size, the field of view and aspect ratio you played at |
| 5 | Signpost find rate | Signposts counted on a route; notice data from at least three players you watched |
| 6 | Chokepoint law and lanes | Choke widths in characters abreast, time-to-kill, rotation routes timed |
| 7 | Return ratio | Out and back times on the fastest routes, one-way edges mapped |
| 8 | Clue reliability | Clues for one beat, with what three players noticed and said |
| 9 | Travel gap and density | Run and mount speeds timed over a known distance, POI positions from a hand-drawn map |
| 10 | Errand cost and gate slack | Hub-to-destination walks timed, gate thresholds and available content |
| 11 | Neighbours and capacity | Camp and player counts at several times of day, view radius estimated |
| 12 | Exposure and `P*` | Spawn exits and camp positions on a gridded sketch; spawn counts and respawn times timed |
| 13 | Reach envelope | Jump heights and gaps measured in the game against objects of known size |

Every measured value carries its method, its unit and how many times you repeated it (at least three repeats for timings, reporting the median). If you use a published figure instead of your own measurement, cite it with its source and version as the lectures do, and say why you could not measure it.

### What you write

A report of 1,500 to 2,000 words plus tables and figures, with these sections.

1. **The level.** What it is, where it sits in the game, the version played, and a map you drew yourself with the places you refer to. Do not paste maps from wikis or guides.
2. **Measurements.** One table per model with its inputs, method and repeats.
3. **What the numbers say.** For each model, the result and what it means for a player at a stated skill level. Link the models where you can. A long walk-back (week 1) on a supply-limited camp (week 12) is worse than either alone.
4. **Where the model and the game disagree.** At least one place where your measurement and the model's prediction differ, with your best explanation. A model that fits perfectly is suspicious.
5. **One change.** A single layout or rule change, the model's prediction for it, and what it would cost the players or the team. Say what a playtest would have to show to confirm it.
6. **Sources.** Any facts you did not measure, with version or era.

Screenshots you took yourself may appear in the report as measurement evidence. Diagrams must be your own.

### Teardown criteria

**Choice and scope (4 points).**
- 4: level, version and date stated; scope small enough to measure properly; the chosen models fit what the level is for.
- 2 to 3: scope too broad, or one model a poor fit.
- 0 to 1: version missing, or models chosen with no link to the level.

**Measurements (10 points).**
- 9 to 10: every model input measured by you with method, unit and repeats; medians reported; screenshots and timings reproducible.
- 6 to 8: most inputs measured, one or two estimated without saying so.
- 3 to 5: measurements thin, or single runs.
- 0 to 2: numbers invented or copied without sources.

**Models applied correctly (10 points).**
- 9 to 10: three or more models from different weeks, one from weeks 9 to 12, every formula used as in the lecture, every result checkable from the tables.
- 6 to 8: one arithmetic slip, or one model stretched past its assumptions without comment.
- 3 to 5: models named but results not computed, or only two models.
- 0 to 2: wrong models or no computation.

**Disagreement and uncertainty (6 points).**
- 5 to 6: a real model-versus-game difference explained with a named mechanism (frame stepping, path detours, correlated noticing, uneven camps); uncertainty from small samples stated as a range.
- 3 to 4: a difference noted, explanation vague.
- 0 to 2: none, or "the model is wrong" with no reason.

**Design judgment (7 points).**
- 6 to 7: one change with a predicted effect from the model, a named cost, and a test that could confirm or refute it.
- 3 to 5: a sensible change without a prediction or without a cost.
- 0 to 2: a wish list, or a change unrelated to the numbers.

**Writing and sources (3 points).**
- 3: plain, well organised, within the word range, every unmeasured fact cited with version.
- 1 to 2: hard to follow in places, or a citation missing.
- 0: over length by more than 20%, or uncited facts throughout.

## Rubric

| Part | Criterion | Points |
|---|---|---|
| Labs | Mean of the four analysis lab marks × 0.60 | 60 |
| Teardown | Choice and scope | 4 |
| Teardown | Measurements | 10 |
| Teardown | Models applied correctly | 10 |
| Teardown | Disagreement and uncertainty | 6 |
| Teardown | Design judgment | 7 |
| Teardown | Writing and sources | 3 |
| **Total** | | **100** |

The component mark out of 100 is multiplied by 0.20 for the course grade.

## Rules

- **Late work.** Labs follow the [blockouts brief](blockouts-brief.md#rules). A teardown up to 48 hours late is marked out of 32 instead of 40. After that it is marked for feedback only.
- **Playing and recording.** Measure in single-player modes, private sessions or quiet times, where your stopwatch runs do not get in other players' way. Do not record other players' names or chat. If you watch friends play for signpost or clue data, the playtest consent rule in the blockouts brief applies.
- **Academic integrity.** Your measurements must come from your own play. You may read guides and wikis for facts, cited with version, but you may not copy their maps, tables or conclusions. AI assistants may help you check arithmetic or phrasing, and you must say so in one line. You may not submit work you cannot explain at a spot check.
