# GD201 · Lab 12: Sightline heatmaps and spawn redesign

**Week:** 12 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the blockouts component (40% of the course). The spawn and camp analysis you produce here goes into your final zone's design document.

**Lecture:** [Week 12, spawn design and contested resources](../lectures/w12-spawn-design-and-contested-resources.md). **Interactive:** [w12-spawn-sightlines.html](../examples/w12-spawn-sightlines.html), for checking maps by eye.

## Objective

Implement the lecture's line-of-sight test, exposure, heatmap and camp positions on a grid map, reproduce the lecture's spawn table, then redesign a badly placed spawn until it meets exposure and camp-position targets. Finish by checking a quest camp against its supply limit `P*`.

## Starter materials

- [`lab12-starter/spawns.py`](lab12-starter/spawns.py). The teaching map from the lecture, an open arena, a lab map whose team spawn stands in the open, and helpers `walls`, `open_cells`, `print_heatmap` and `spawn_report`. You fill in six functions: `los`, `exposure`, `heatmap`, `camp_positions`, `p_star` and `quest_time`. The docstrings give the exact rules, including the quarter-cell sampling for line of sight. It also has a design checker (`python spawns.py --design`) for Part D.
- [`lab12-starter/check_lab12.py`](lab12-starter/check_lab12.py). A checker with 10 checks. Do not edit it.
- Squared paper for sketching redesigns before you type them.

Run from inside `lab12-starter` with the course Python:

```
python spawns.py
python check_lab12.py
python spawns.py --design
```

The starter runs and reports that the functions are not implemented. The checker prints `0/10 checks pass` until you fill them in. The design check fails on the unchanged lab map.

## Steps

1. **Part A, line of sight (20 min).** Implement `los` exactly as the docstring says. Test by hand: two corners of the open arena see each other; A and C on the teaching map don't. Then check symmetry on ten random pairs of cells. Is your `los` always symmetric? If you find a pair where it isn't, keep it for your write-up and explain why sampling can cause it.
2. **Part A, exposure and heatmap (20 min).** Implement `exposure` and `heatmap`. Reproduce `E = 48` for the arena at `R = 4`, and 90 and 2 for A and C. Print the teaching map's heatmap with `print_heatmap` and compare it with the lecture's interactive.
3. **Part B, camp positions (20 min).** Implement `camp_positions`. Reproduce the lecture's `K = 2` for B, with camp cells (1, 7) and (5, 11), and `K = 28` with the north gap walled up. Run the checker until it prints `10/10 checks pass`.
4. **Part B, range (10 min).** For A, B and C, record `E` at the spawn and `K` for `R` = 4, 8 and 16. Plot `K` against `R` for the three spawns on one chart. Write two sentences on which spawn gets worse fastest as weapons reach further and why.
5. **Part C, the quest camp (15 min).** Implement `p_star` and `quest_time`. On the lab map, the capture point `X` is also where a quest sends players to kill 12 monsters. There are 5 spawns, `T = 45` s and `t_k = 15` s. Compute `P*` and the quest time for 1, 4 and 10 players. Then choose new `M` and `T` so that 10 players finish in under 4 minutes, and place the extra spawn cells on the lab map where `E ≤ 15` (use your heatmap).
6. **Part D, redesign the spawn (40 min).** Copy the lab map into `MY_MAP` and redesign the west side so that the team spawn meets every target in `DESIGN_TARGETS`: `E` at the spawn at most 20, at least two exits, every exit at most 45, and at most 5 camp positions (`R = 8`). Update `MY_SPAWN`, `MY_EXITS` and `MY_ROOM` to match. Keep the capture point and the map's outer size. Iterate with `python spawns.py --design` until all four targets pass.
7. **Part D, walk-back cost (10 min).** Count the shortest walk in cells from your new spawn to `X` and from the original spawn to `X`. At 6 m/s with 2-metre cells, how many seconds did your safer spawn add to every return trip? Use week 1's recovery time to say whether that is acceptable for a capture map with 10-second respawn waves.
8. **Stretch (optional).** Add a "camp value" to each camp position: the number of exit cells it sees divided by its own exposure. A camp position that sees every exit but is itself highly exposed is a weak camp. Report the best camp position on your redesigned map by this measure.

## Deliverable

Submit a zip with:
- Your completed `spawns.py`, including `MY_MAP` and the new spawn data.
- A write-up of up to two pages with: your symmetry finding from step 1; the heatmap of the teaching map (printed output or a screenshot); the table and chart from step 4 with your two sentences; the Part C numbers and your chosen `M`, `T` and spawn cells; your redesigned map (printed) with its `spawn_report` output and the design check result; the walk-back numbers and your judgment from step 7.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 10/10 checks pass | 6-9 pass | 0-5 pass | 25% |
| Range analysis | `E` and `K` at three ranges for three spawns, chart clear, explanation names the geometric reason | Table complete, explanation vague | Missing | 15% |
| Quest camp | `P*` and times correct, new `M` and `T` meet the target, extra spawns placed in low-exposure cells | Numbers correct, spawn placement not checked | Missing or wrong | 15% |
| Spawn redesign | All four design targets pass, capture point unchanged, layout still readable as a level | Three of four targets pass | Fewer than three | 30% |
| Walk-back judgment | Seconds computed, trade-off against safety argued with the recovery-time model | Seconds computed without a judgment | Missing | 15% |
