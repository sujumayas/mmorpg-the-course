# CS101 · Lab 10: Collision toolkit

**Week:** 10, collision basics ([lecture](../lectures/w10-collision-basics-aabb-and-circles.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). Your `collision.py` goes straight into mini-game 2.

## Objective

Write the box, circle and circle-against-box overlap tests from the lecture, add minimum push-out, and measure tunneling in a small bullet simulation. By the end you should be able to predict, before running anything, whether a bullet at a given speed and frame rate can pass through a wall.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python 3.10 or later, no packages.

- [`collision.py`](lab10-starter/collision.py) has helper functions `edges` and `clamp` (given), five empty functions (`aabb_overlap`, `circle_overlap`, `circle_box_overlap`, `overlap_depth`, `push_out`) with docstrings that state the exact rules, and `bullet_hits_wall`, a finished simulation loop with one TODO line.
- [`test_lab10.py`](lab10-starter/test_lab10.py) has eight tests built from the lecture's tables: the five boxes A to E, the plus-sign overlap, the coin, the bullet near the player's corner, push-out, and tunneling at 60 and 30 fps. Run it with `python test_lab10.py`. On the starter it reports `0/8 tests passed`.
- The week 10 interactive, `examples/w10-aabb-overlap.html`, once it is built, for checking single cases by eye.

## Steps

1. **Four comparisons.** Implement `aabb_overlap` with the strict rule, in the lecture's order. Run the tests. `test_lecture_table`, `test_symmetric` and `test_plus_sign` should pass.
2. **Break it on purpose.** Change comparison 2 to `>=` and rerun. Write down which test fails and which box causes it. Then change it back. This is the teammate bug from check-yourself question 4.
3. **Circles.** Implement `circle_overlap` and `circle_box_overlap` without `math.sqrt`. `test_circles` and `test_circle_box` should pass.
4. **Depth and push-out.** Implement `overlap_depth` and `push_out`. `push_out` must return a new dictionary and leave its input unchanged. Check by hand that pushing the player out of box A gives `x = 88`.
5. **Tunneling.** Fill in the TODO in `bullet_hits_wall`. Run `python collision.py`. It prints the hit time at 120, 60, 30 and 20 fps for a 4-pixel bullet at 900 px/s against a 16-pixel wall.
6. **How often does it tunnel?** At 30 fps the result depends on where the bullet starts. For each integer `start_x` from 0 to 29, record whether the bullet misses the wall. Count the misses. Before you run it, predict the count from the lecture's condition: a step of `v / f` pixels misses a window `t + s` pixels wide for roughly `(v / f − (t + s)) / (v / f)` of the start positions. Compare your prediction with the count and explain any difference of one or two (hint: strict comparisons).
7. **Fix it two ways.** Find the smallest `substeps` value that makes the 30 fps bullet hit for all 30 start positions. Then, with `substeps = 1`, find the smallest wall thickness that does the same. Report both.

## Deliverable

Your completed `collision.py` with `python test_lab10.py` reporting `8/8 tests passed`, plus a note of at most 250 words addressed to your mini-game team. It must give the miss count from step 6 with your prediction, both fixes from step 7, and your recommendation for a minimum wall thickness for your game's fastest projectile at 30 fps, with the arithmetic.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Overlap tests | 8/8 tests pass; no square roots; four comparisons in lecture order | 6-7 pass | 5 or fewer | 35% |
| Push-out | Correct axis and direction, input unchanged, result touches without overlapping | Correct axis, direction or copying wrong in one case | Missing or moves the wrong box | 15% |
| Tunneling measurement | Miss count reported with a prediction from the formula and a correct explanation of the gap | Count reported, prediction or explanation missing | Missing | 25% |
| Fixes and recommendation | Both minimum values found and a wall thickness justified with `v / f − s` | One value found or justification thin | Missing | 15% |
| Code quality | Clear names, docstrings kept, no global state | Minor issues | Hard to follow | 10% |
