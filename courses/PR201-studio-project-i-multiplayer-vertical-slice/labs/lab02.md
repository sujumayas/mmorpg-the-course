# PR201 · Lab 02: Pillars and scope sheet

**Week:** 2 · **Time:** 1 hour in the studio session plus about 3 hours as a team · **Weight:** part of [milestone 1, pitch and pre-production](../assessments/m1-pitch-and-preproduction-brief.md) (marked with lab 01)

## Objective

Turn your pitch into a ranked feature list with a cut line, and check that every pillar still stands after the cut. The model is in section 2 of the [week 2 guide](../lectures/w02-pre-production-pillars-and-scope.md).

## Starter materials

Folder `lab02-starter/`. Standard library Python only.

- `features.csv`: one row per feature with `id`, `feature`, `tier`, `hours`, one column per pillar (`P1`, `P2`, …, 1 or 0) and `player_loses`. The must tier has `tier` set to `must`. Other rows are `should` or `cut`, or blank if you use `--greedy`. The starter holds the *Hollowmarch* list with blank tiers.
- `check_scope.py`: ranks features by pillar support per hour, places the cut line (with `--greedy`) or checks your tiers (without it), prints support per pillar and `m_max`, and ends with `PASS` or `NOT READY`. Options `--plannable`, `--useful` and `--min-support` default to 312, 445.5 and 2.
- Your week 1 files, for plannable and useful hours.

## Steps

1. **Reproduce the guide.** Run `python check_scope.py features.csv --greedy`. Confirm the 156-hour greedy tier and the fragile P3.
2. **Repair it.** Copy the file, set tiers by hand to the repaired set from the guide (F2 cut, F6 kept) and fill in `player_loses` for every cut row. Run without `--greedy` and confirm `PASS`.
3. **Your pillars.** Write two or three pillars. For each, write the playtest question that tests it and one feature it rules out.
4. **Your features.** List every candidate feature. Each discipline's primary adds their hours to every row. Map each feature to pillars.
5. **Your cut line.** Run with `--greedy` and your own `--plannable` and `--useful` from week 1. Repair any fragile pillar with a swap. Write every override of the density order with one sentence.
6. **Dependencies.** For each kept feature, list what it depends on. If it depends on a cut feature, either keep the dependency or cut the feature, then rerun.
7. **Timeline.** Write the 15-minute player timeline and mark the minute each kept feature first appears. Fix any stretch over two minutes with no kept feature active.

## Deliverable

In `docs/`: `pillars.md`, `features.csv` with your final tiers, the checker output showing `PASS` (in `scope.md`), and `scope.md` with the must tier as player steps, overrides, dependencies, cut triggers and the timeline.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Pillars | One pillar about players together; each has a playtest question and rules something out | Pillars present, one test or rule missing | Genre labels or adjectives | 20% |
| Estimates and mapping | Every discipline estimated every row; mapping defensible | Some rows estimated by one person | Hours or mapping missing | 20% |
| Cut line and repair | `check_scope.py` passes; swaps and overrides explained | Passes, reasons thin | Does not pass | 25% |
| Dependencies and cut list | No kept feature depends on a cut one; every cut has a player-loses line | Minor gaps | Missing | 15% |
| Timeline and triggers | Timeline reaches every kept feature; triggers tied to milestones | One of the two weak | Missing | 20% |
