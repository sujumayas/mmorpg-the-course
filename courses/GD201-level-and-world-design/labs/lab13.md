# GD201 · Lab 13: Metrics gym and jump audit

**Week:** 13 · **Time:** 2 hours in the lab plus about 3 hours at home · **Weight:** part of the blockouts component (40% of the course). The metrics sheet you produce goes into the final zone's design document.

**Lecture:** [Week 13, metrics: player speed, jump, scale](../lectures/w13-metrics-player-speed-jump-scale.md). **Interactive:** [w13-jump-reach.html](../examples/w13-jump-reach.html), for checking your numbers.

## Objective

Implement the lecture's reach envelope and a jump audit in Python, then build a metrics gym for your own character controller, measure its real limits, correct the model against them, and audit the critical path of your Lab 02 blockout.

## Starter materials

- [`lab13-starter/metrics.py`](lab13-starter/metrics.py). The Quake metrics sheet, a sample route of eight jumps and five functions to fill in: `jump_height`, `time_to_apex`, `max_gap`, `classify` and `audit`. The docstrings define each one.
- [`lab13-starter/check_lab13.py`](lab13-starter/check_lab13.py). A checker with 13 checks. Do not edit it.
- Your engine of choice (Unity, Unreal, Godot or TrenchBroom for Quake-style maps) with the character controller you used in Lab 02, a world-aligned grid texture, and a stopwatch or an in-game timer.

Run from inside `lab13-starter` with the course Python:

```
python metrics.py
python check_lab13.py
```

The starter runs and reports that the functions are not implemented. The checker prints `0/13 checks pass` until you fill them in.

## Steps

1. **Part A, the envelope (20 min).** Implement `jump_height`, `time_to_apex` and `max_gap`. Check against the lecture's table: `G(0) = 248.0`, `G(h) = 140.0`, `G(−h) = 292.7` for Quake at a run.
2. **Part B, the audit (20 min).** Implement `classify` and `audit`. Run the checker until it prints `13/13 checks pass`. Read the audit of the sample route and write one sentence on why "high ledge" is a skill jump even though its gap is only 62.5% of the widest.
3. **Part C, build the gym (45 min).** In your engine, build a gym level with the pieces listed in section 4 of the lecture: a step ramp, a jump wall, a gap ladder at three height differences (flat, half a jump up, one jump down), a drop tower, corridors and doorways at 1, 1.5, 2, 3 and 4 box widths, and a timed straight run. Label every piece with its size in world units.
4. **Part D, measure (30 min).** Measure step height, jump height (plain and with every other climbing verb your controller has), run speed, and the widest gap at each of the three heights. For each gap, record the widest you clear 10 times out of 10 and the widest you clear at all. Use at least two testers besides yourself for the gap ladder.
5. **Part E, correct the model (20 min).** Read `v0`, `g`, `v` and `w` from your controller's settings and enter them as a new metrics sheet in `metrics.py`. Compare `max_gap` with your measured maxima. Compute the percentage error at each height. If any is above 5%, find the cause (air control, acceleration, a speed cap in the air, frame stepping, edge forgiveness) and write it down.
6. **Part F, audit your blockout (25 min).** List every jump and every blocking wall on the critical path of your Lab 02 blockout as a route in `metrics.py`, using your corrected sheet. Run the audit. Fix every "impossible" or "skill" jump on the critical path that you did not intend, and every blocking wall lower than your jump plus margin. Replay the fixed route once and record the critical-path time.
7. **Stretch (optional).** Add a `blocks(wall_height, m)` function that returns True only when a wall is taller than every climbing verb plus your margin, and use it in the audit.

## Deliverable

Submit a zip with:
- Your completed `metrics.py`, including your controller's metrics sheet and your blockout's route.
- Screenshots of the gym (at least the gap ladder and the jump wall, with labels readable).
- A one-page metrics sheet: every metric, its measured value, the model value where there is one, the error, the margin you chose and the date measured.
- A half-page audit report: the audit output before and after your fixes, the changes you made, and the new critical-path time.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 13/13 checks pass | 8-12 pass | 0-7 pass | 20% |
| Gym | Every listed piece built, labelled, grid-textured and usable | Most pieces built, some unlabelled | Missing pieces or unreadable sizes | 20% |
| Measurements | Two testers plus author, 10-of-10 and maximum recorded at three heights, run speed timed | Measurements present but from one tester or one height | Values guessed or copied from settings | 20% |
| Model correction | Error computed at each height, any error over 5% explained with a specific controller cause | Errors computed, causes vague | No comparison | 20% |
| Audit and fixes | Critical path audited, every unintended skill or impossible jump fixed, new time recorded | Audit run, some issues left without comment | No audit of the blockout | 20% |
