# MA201 · Lab 12: A grid raycaster and a hitscan check

**Week:** 12 ([Raycasting](../lectures/w12-raycasting.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; trade exploit maps with a neighbor in Part C
**Counts toward:** problem sets (40%). `grid_walk` and `ray_aabb` are reused in the final physics sandbox.

## Objective

Write the raycasts a game uses most: a grid walk, a raycast renderer with and without the fisheye correction, and exact tests against spheres and boxes. Then use the grid walk to close a line-of-sight exploit on a server map, where the old check sampled the segment and let players see through the corners of pillars.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`labs/lab12-starter/raycast.py`](lab12-starter/raycast.py). It has three maps as lists of strings (the lecture's 8 × 8 room, a 16 × 16 maze, and a 12 × 9 arena with three single-cell pillars), a text renderer that draws columns in the terminal with shade characters, and the old server check `sampled_can_see()`. You write `grid_walk()`, `column_heights()`, `ray_sphere()`, `ray_aabb()` and `can_see()`. `python raycast.py` renders the lecture room with the correction off and on, then the maze.
- [`labs/lab12-starter/check_lab12.py`](lab12-starter/check_lab12.py). Run `python check_lab12.py` inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w12-grid-raycaster.html`](../examples/w12-grid-raycaster.html). Its trace panel prints the same steps your `grid_walk` should take.

## Steps

### Part A: the renderer (60 minutes)

1. Write `grid_walk()`. It must return the distance, the wall cell, and which kind of grid line the ray crossed to enter it, and it must stop with `None` past `t_max`. Before running the checker, trace the lecture's 20° ray on paper and confirm your code's `t` values match all five rows of the lecture's trace. The tie check uses a direction with two identical components, so the tie is exact and must go to y.
2. Write `column_heights()`. The check compares your seven columns with the lecture's table, with and without the correction. Run `python raycast.py` and look at both renders of the lecture room. Describe the difference in one sentence.
3. Render the maze from three positions of your choice with `perp=False` and `perp=True`. Keep the one where the fisheye is most obvious and explain, with the geometry of that view, why it is worst there.

### Part B: shapes (30 minutes)

4. Write `ray_sphere()` and `ray_aabb()`. The checks include a sphere behind the ray, an origin inside a sphere and inside a box, and a ray parallel to a slab that starts outside it. For the parallel case, explain in your report what would happen if you divided by `d[axis] = 0.0` in Python, and what would happen in C# or GLSL, where the division gives infinity.
5. Write `can_see()` using your grid walk over the segment, with the rule that a segment through the exact shared corner of two diagonal wall cells is blocked. The check tests an open line, a line through a pillar, and that corner case.

### Part C: the exploit (at home)

6. The step 5 check fires one known exploit: from `(1.5, 1.5)` to `(4.2, 4.0)` in the arena, the old sampled check says "visible" and your walk says "blocked". Find the pillar and the cell the samples step over. Then write a short script that scans the arena for every pair of points on a 0.5-cell lattice where the two checks disagree. Report how many pairs the old check got wrong and draw the worst pillar's exposure as a small ASCII map.
7. Measure cost. Time 100,000 random segments with each check. The sampled check does about `4 × length` samples; the walk visits about `|Δx| + |Δy|` cells. Compare your measured ratio with that prediction.
8. Design a 12 × 9 arena of your own, with at least four pillars, where the old check is wrong on as many lattice pairs as you can manage. Swap arenas with a neighbor and confirm each other's counts with your step 6 script. Then write a note of at most 250 words to the server programmer: the numbers from steps 6 and 7, whether the exact check fits a budget of 2,000 line-of-sight tests per tick at 20 ticks per second, and the one situation (such as a diagonal gap) where the design team must decide the rule rather than the code.

## Deliverable

Your completed `raycast.py` with `check_lab12.py` passing (paste the output), the step 2 and 3 renders with their explanations, the step 4 answer, the step 6 count and ASCII map, the step 7 timing table, your step 8 arena file, your neighbor's confirmed count, and the note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Raycasts correct (35%) | All seven checks pass; grid walk has no special cases beyond the zero-direction guard; hand trace matches | All pass, with extra cases or duplicated walk code | Grid walk passes, shape tests fail | Fewer than three checks pass |
| Fisheye explanation (15%) | Renders shown; the worst view is explained with the angle between rays and the view direction | Renders shown, explanation vague | One render | Missing |
| Exploit analysis (30%) | Count and map for the given arena, a scan script that runs, a custom arena confirmed by a neighbor | Count and map, custom arena unconfirmed | Only the given exploit explained | Missing |
| Cost and note (20%) | Measured ratio compared with the prediction; budget answered with numbers; a rule decision named | Numbers present, budget answer weak | No numbers | Missing |
