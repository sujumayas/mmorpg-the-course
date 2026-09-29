# GD201 · Lab 07: Return ratios in a vertical level

**Week:** 7 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the blockouts component (40% of the course).

**Lecture:** [Week 07, verticality and navigation](../lectures/w07-verticality-and-navigation.md). **Interactive:** [w07-drop-and-climb.html](../examples/w07-drop-and-climb.html), for checking the Cliff Ruin numbers.

## Objective

Turn a level with height into a directed graph with timed edges, compute out and back times with a shortest-path search, find the places that strand the player, and choose shortcuts that fix them. Then greybox a small vertical space of your own and measure its return ratios in your engine.

## Starter materials

- [`lab07-starter/vertical_nav.py`](lab07-starter/vertical_nav.py). The speed constants from the lecture and eight functions to fill in: `drop_time`, `climb_time`, `edge_times`, `build_graph`, `shortest_time`, `return_ratio`, `stranded` and `best_shortcut`. The docstrings define each one.
- [`lab07-starter/levels.py`](lab07-starter/levels.py). Two levels in one format: the lecture's Cliff Ruin, and the Quarry (eight places between 0 and 20 m, with one unsafe drop). Also four shortcut candidates for the Quarry. Do not edit it.
- [`lab07-starter/check_lab07.py`](lab07-starter/check_lab07.py). A checker with 10 checks. Do not edit it.
- For Part E: the engine you used for the week 2 blockout (Unity, Unreal or Godot), with its default character controller.

Run from inside `lab07-starter` with the course Python:

```
python vertical_nav.py
python check_lab07.py
```

The starter runs and says the functions are not implemented. The checker prints `0/10 checks pass` until you fill them in.

## Steps

1. **Part A, edges (20 min).** Implement `drop_time`, `climb_time` and `edge_times`. An unsafe drop returns an empty list, not an edge with infinite time. A ladder goes both ways, up at `V_CLIMB` and down at `V_LADDER_DOWN`. A slope is uphill in whichever direction the heights say.
2. **Part B, search (25 min).** Implement `build_graph`, `shortest_time` (Dijkstra, as in the lecture) and `return_ratio`. Reproduce the lecture's Cliff Ruin numbers: 6.55 s out (printed as 6.5), 47.5 s back, ratio 7.25.
3. **Part C, diagnosis (15 min).** Implement `stranded` and `best_shortcut`. Run the checker until it prints `10/10 checks pass`.
4. **Read the Quarry (15 min).** Print out time, back time and return ratio from the Hub to every place. Draw the Quarry as a side section by hand, using the heights, and mark every one-way edge. Answer in your log: why does the Shelf have a ratio of 3.14 when its back trip is only 15 s? Is it really a problem? Propose a rule that combines the ratio with the absolute back time.
5. **Part D, fix the Quarry (20 min).** `best_shortcut` picks one candidate, and no single candidate gets every ratio under 2. Design a fix with at most two new edges of your own (any kind, any places, realistic heights and lengths) that brings every place with a back time over 20 s under a ratio of 2. Lifts are allowed. Add a `("timed", a, b, seconds)` kind to your copy of `edge_times` and give each lift a speed between 2 and 4 m/s. Add them to a copy of `QUARRY` and show the numbers. Say where each shortcut is unlocked from and why.
6. **Part E, greybox (at home, 60 min).** Build a small vertical space in your engine with at least three height levels, one one-way drop and one shortcut. Measure the real times with a stopwatch or a timer script (three runs each, take the median) for every edge. Enter your measured times into a new level in `levels.py` format, using the `timed` kind from step 5 for every edge. Report the return ratios before and after the shortcut is unlocked.
7. **Stretch (optional).** Minecraft prices a drop in health instead of forbidding it (`floor(h − 3)` of 20). Add an optional `hp_cost` to drops over `h_safe` and change `shortest_time` so that a player with a given health budget can take unsafe drops while they can afford them. What happens to the Quarry's Pit when the player has 20 health and each metre over 8 costs 2?

## Deliverable

Submit a zip with:
- Your completed `vertical_nav.py` and your copy of `levels.py` with the fixed Quarry and your greybox level.
- A log (about 500 words) with: the Quarry table from step 4 and your answer about the Shelf; your two-edge fix and its table from step 5; your greybox's measured edge times and return ratios from step 6.
- Three screenshots of your greybox: the overlook before the drop, the view up from the bottom, and the shortcut.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 10/10 checks pass | 6-9 checks pass | 5 or fewer pass | 30% |
| Quarry reading | Side section correct with every one-way edge; Shelf question answered with a rule that uses both ratio and back time | Section drawn, rule vague | Missing | 15% |
| Quarry fix | Two edges or fewer, realistic, every place over 20 s back is under ratio 2, unlock side justified | Target met but edges unrealistic or unjustified | Target not met | 20% |
| Greybox measurement | Three height levels, medians of three runs, ratios before and after the shortcut, screenshots show the preview from the overlook | Measured but only one run, or one screenshot missing | Formula values instead of measurements | 25% |
| Code readability | Edge kinds handled in one clear place, no copied search code | Works but repetitive | Hard to follow | 10% |
