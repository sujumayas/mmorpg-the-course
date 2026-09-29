# CS203 · Lab 03: Terrain costs, movement range and Dijkstra maps

**Week:** 3, graphs and Dijkstra ([lecture](../lectures/w03-graphs-and-dijkstra.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the labs (50% of the course). Keep your expansion counts from step 5; week 4 compares A* against Dijkstra.

## Objective

Implement Dijkstra's algorithm on a tile grid with terrain costs, use it for movement ranges and for Brogue-style Dijkstra maps, and tune a cost table until NPC routes match a designer's written intent.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python 3, no packages.

- [`paths.py`](lab03-starter/paths.py) has the lecture's cost table (open 1, woods 2, hills 2, wooded hills 3, mountains and walls impassable), a map loader, `find`, `neighbours` (N, E, S, W order, paying the cost of the cell entered), a `show` printer, the lecture's 6 × 5 map and two tuning maps with their designer intents. Four functions are empty: `dijkstra`, `path_to`, `movement_range` and `flee_map`.
- [`test_paths.py`](lab03-starter/test_paths.py) checks the lecture's cost grid cell by cell, the 9-tile route and its exact cells, an empty path when the goal is out of budget, movement ranges of 12, 10 and 1 cells for budgets 4, 3 and 0, a two-source corridor, and the values of a flee map on a 10-cell corridor.
- The [interactive](../examples/w03-dijkstra-terrain.html), for spot checks.

Run the tests from the starter folder with `python3 test_paths.py` (or the course's `.venv/bin/python`). On the starter every test prints `TODO` and the script exits with status 1.

## Steps

1. **Dijkstra and paths.** Write `dijkstra` with `heapq`, `(cost, cell)` tuples and lazy deletion, and `path_to`. It takes a *list* of start cells, all at cost 0. With one start it is the lecture's algorithm. Keep the strict `<` when updating, or the route test will pick a different tie.
2. **Movement range.** Write `movement_range` as Dijkstra with a budget. Print the range for budgets 2 to 6 on the lecture map and check the counts against the interactive.
3. **Multi-source.** Run `dijkstra` with every cell of the goal set as a start. On the six-cell corridor with starts at both ends, confirm `0 1 2 2 1 0`. This is a Dijkstra map in Walker's sense. Any agent can walk to the nearest goal by stepping to its lowest neighbour.
4. **Flee map.** Write `flee_map` following Walker's recipe in the docstring (map from the threats, multiply by −1.2, rescan until nothing changes). Pass the corridor test. Then build a 12 × 7 room of your own with a pillar in the middle and one door. Place the threat near the door and a monster in a corner. Print the map and trace the monster's downhill steps. Repeat with factors −1.05, −1.2 and −2. Describe how the factor changes when the monster makes a break past the threat.
5. **Cost of the search.** Add a counter for expanded cells. For the lecture map and your room, report expanded cells before the goal and in total. Keep these numbers for week 4.
6. **Tune `forest_or_open`.** With the default costs, report the route's cost and length. The intent says the patrol must walk around the woods. Find the lowest woods cost that makes it do so, to one decimal place. Derive the threshold by hand as well (hint: compare `3w + 3` with the detour's cost) and check that the two agree.
7. **Tune `hill_or_around`.** With the default costs, the two routes tie. Report which one your code returns and why (tie order). Then find the smallest change to the wooded-hill cost that satisfies the intent, and explain why relying on a tie is a bug waiting to happen.
8. **Per-unit costs.** Civilization VI's Ranger promotion lets a unit ignore woods penalties. Make a `scout` cost table with woods at 1 and run `forest_or_open` for the scout and the patrol with your step 6 costs. Report both routes. Write one sentence on what a player would read into the difference.

## Deliverable

- `paths.py` with all tests passing and the expansion counter.
- A short report (at most 500 words, plus printed grids) with: the step 2 range counts, your room's flee maps for three factors with the monster's path marked, the step 5 expansion counts, and the tuning results for steps 6 to 8 with the hand derivation.
- A 300-word cost-table rationale. What does a cost of 1 mean in your game, why each terrain cost is what it is, and one route in your maps that a player might find odd, with your decision to keep or fix it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All tests pass; expansion counts reported | Tests pass, counts missing | Tests fail | 30% |
| Flee map experiment | Three factors compared on a room with a loop; the break-past behavior explained from the numbers | Maps printed, explanation thin | Missing | 20% |
| Tuning (steps 6 and 7) | Thresholds found numerically and derived by hand, tie behavior explained | Thresholds found, no derivation | Wrong or missing | 25% |
| Per-unit costs and rationale | Routes differ as predicted; rationale defines the cost unit and defends one odd route | Routes reported, rationale generic | Missing | 15% |
| Code quality | One Dijkstra used for paths, ranges and maps; no copy-pasted variants | Works with some duplication | Hard to follow | 10% |
