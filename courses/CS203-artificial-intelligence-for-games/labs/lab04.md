# CS203 · Lab 04: A* on a tactical grid

**Week:** 4 ([A* and heuristics](../lectures/w04-a-star-and-heuristics.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare tables with a neighbor at the end

## Objective

Implement A* on an 8-way grid with walls and mud, prove it returns the same cost as Dijkstra, measure how many cells each search expands, and build a small tool that tells you whether any heuristic is admissible on a given map. By the end you should be able to hand a designer a table that says "this heuristic, on this map, expands this many cells and returns paths this much worse than optimal."

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab04-starter/pathgrid.py`](lab04-starter/pathgrid.py). It loads grid files, generates legal 8-way moves (straight 10, diagonal 14, times the terrain factor of the cell entered; no cutting corners past walls), and contains a finished `dijkstra()` and `true_costs_to()` that serve as the reference answer. You fill in `manhattan()`, `octile()`, `astar()` and `max_overestimate()`. Run `python pathgrid.py` to print a comparison table for every map; rows for unwritten functions show a dash.
- [`labs/lab04-starter/check_lab04.py`](lab04-starter/check_lab04.py). Run `python check_lab04.py` from inside the starter folder. It prints PASS or FAIL for five checks and exits with status 1 until all pass. On the untouched starter all five fail.
- `labs/lab04-starter/maps/`: `open.txt` (16 × 16, empty), `wall.txt` (a vertical wall), `trap.txt` (a U-shaped obstacle open away from the goal) and `mud.txt` (a mud field at 3× cost between S and G).
- The interactive [`examples/w04-astar-vs-dijkstra.html`](../examples/w04-astar-vs-dijkstra.html) for building intuition. Note it uses 4-way movement; this lab uses 8-way.

## Steps

### Part A: heuristics and A* (60 minutes)

1. Write `manhattan(a, b)` as `10 × (|dr| + |dc|)` and `octile(a, b)` using the formula from lecture section 3 with `D = 10`, `D2 = 14`. Check by hand that `octile((0, 0), (3, 5))` is 62 before running the checker.
2. Write `astar(grid, start, goal, h, weight=1.0)`. Start from the lecture's `search()` function and change three things: costs come from `grid.neighbors()`, which yields `(cell, cost)` pairs; the function returns `(cost, path, expanded)`; and you keep a `parent` dictionary so you can rebuild the path with the provided `rebuild()`. Order the heap by `(g + weight × h, h, cell)`. Run the checker until the step 2 check passes.
3. Run `python pathgrid.py`. Copy the table into your report. The step 3 checks should now pass as well: A* with octile expands fewer cells than Dijkstra on `open`, `wall` and `trap`, and weighted A* stays within 2× the optimal cost.

### Part B: measure and explain (35 minutes)

4. Write `max_overestimate(grid, goal, h)`. Use `true_costs_to(grid, goal)`, which gives the exact cost from every reachable cell to the goal, and return the largest `h(cell, goal) − true_cost` over all cells, or 0 if `h` never overestimates. The step 4 check expects 0 for octile on every map and exactly 72 for Manhattan on `open.txt`. Explain in two sentences where on the map the 72 comes from.
5. Manhattan is not admissible on these maps, yet on the four maps provided it may still return optimal costs. Design a fifth map, `maps/cheat.txt`, at most 12 × 12, on which A* with Manhattan returns a path strictly more expensive than Dijkstra's. Record both costs. Do not change the checker: it loads every map in the folder, so your new map must still pass all checks with octile.
6. On `trap.txt`, record expansions for A* with `octile` and weights 1.0, 1.5, 2.0 and 3.0, and the path cost for each. Plot or tabulate expansions against weight and cost against weight.

### Part C: the designer note (at home)

7. Write a note of at most 300 words to a designer who wants a "fast but good enough" pathfinding setting for 150 units ordered across `trap.txt` at once. Use your step 6 numbers. Recommend a weight, state the worst-case cost increase the bound allows and the actual increase you measured, and name one change to the map or the heuristic that would help more than raising the weight.

## Deliverable

Your completed `pathgrid.py` and `maps/cheat.txt`, with `check_lab04.py` passing (paste its output), plus a PDF with the step 3 table, the step 4 explanation, the step 5 costs, the step 6 table or plot, and the designer note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct A* (30%) | All five checks pass; code is the lecture's structure with clear names; tie-breaking as specified | All checks pass, code hard to follow | A* works but one check fails | A* missing or wrong costs |
| Admissibility tool (15%) | `max_overestimate` passes; the 72 is explained by location and the `6k` rule | Passes, explanation vague | Returns a number but fails the check | Missing |
| Counterexample map (20%) | `cheat.txt` makes Manhattan return a worse path; both costs reported; one sentence says why that shape works | Map works, no explanation | Map attempted but Manhattan still optimal on it | Missing |
| Weight study (15%) | Four weights, expansions and costs, trend described; every cost within `w ×` optimal | Table present, trend not described | Fewer than four weights | Missing |
| Designer note (20%) | Recommendation with bound and measured cost; a concrete map or heuristic change with its trade-off | Numbers present, suggestion vague | No numbers | Missing |
