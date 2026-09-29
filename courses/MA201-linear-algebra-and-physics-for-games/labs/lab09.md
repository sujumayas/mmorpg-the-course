# MA201 · Lab 09: A narrow phase with contacts

**Week:** 9, collision detection ([lecture](../lectures/w09-collision-detection-spheres-aabb-sat.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Weight:** part of the problem sets (40%). Your contact functions are the input to week 10's impulse lab and to the physics sandbox.

## Objective

Write the narrow phase of a small physics engine: sphere, AABB and oriented-box tests that return a contact normal and depth, not just yes or no. Verify each against the lecture's tables, then measure how often an AABB-only test lies about rotated boxes, and turn that measurement into a shape recommendation.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Python 3.10 or later, standard library only.

- [`narrow.py`](lab09-starter/narrow.py). Given: `dot`, `make_box` (center, half-extents, angle in degrees, with its two axes in world space), `aabb_of`, and a `false_hit_rate` experiment. You write six functions:
  - Part A (3D): `sphere_sphere`, `aabb_aabb`, `aabb_sphere`.
  - Part B (2D): `projection_radius`, `sat_obb`.
  - Every test returns `None` or `(normal, depth)`, with the normal pointing from the first shape to the second.
- [`test_lab09.py`](lab09-starter/test_lab09.py): ten tests using the lecture's numbers. Run `python test_lab09.py` inside the folder. On the starter it reports `0/10 tests passed`.
- The week 9 interactive, [`examples/w09-sat-projections.html`](../examples/w09-sat-projections.html), for checking any SAT case by eye.

## Steps

### Part A: 3D spheres and boxes (30 min)

1. **Predict.** By hand, find the normal and depth for the sphere pair `(0, 0, 0)`, radius 1 and `(1.2, 0.9, 0.8)`, radius 0.8, and for the boxes centered at `(0, 0, 0)` and `(1.5, 0.2, −1.8)`, both with half-extents `(1, 1, 1)`. Write the numbers down before coding.
2. **Implement** `sphere_sphere`, `aabb_aabb` and `aabb_sphere`. Handle coincident sphere centers with the normal `(0, 1, 0)`. Take the square root only on a hit.
3. **Pass** the four Part A tests.

### Part B: SAT for oriented rectangles (40 min)

4. **Implement** `projection_radius` and check it against the lecture's radius table before going further (`test_projection_radius`).
5. **Implement** `sat_obb`. Test A's two axes first, then B's, stop at the first gap, and otherwise return the smallest-overlap axis signed so that `d · n > 0`.
6. **Pass** the remaining tests. `test_resolving_by_mtv_leaves_zero_overlap` moves B by the MTV and checks that it now just touches A. If it fails while the case tests pass, your sign is wrong.
7. Add a counter to `sat_obb` for how many axes it tests before returning. Over 10,000 random placements of the lecture's boxes A and B (B at a random angle), report the mean number of axes tested for separated pairs. Then try reordering the axes (B's first) and report again.

### Part C: how often does an AABB lie? (30 min)

8. Run `python narrow.py`. It prints, for B rotated by 0° to 90°, the fraction of AABB "hits" that SAT rejects. With a correct `sat_obb` you should see 0 at 0° and 90° and a peak close to 0.20 at 45°. Plot the curve at 5° steps.
9. Change the experiment so both boxes are squares (half-extents 1, 1) and repeat. Then make B a long thin plank (half-extents 2, 0.2). Put all three curves on one plot.
10. Write three sentences explaining why the plank's curve looks the way it does, using the projection radius formula.

### Part D: recommendation (20 min)

11. Choose one: a tumbling barrel in a physics puzzle, a player's sword swing in an action game, a pile of 200 crates in a warehouse level. Write a 250-word recommendation for its collision shape (sphere, capsule, AABB, oriented box, or a set of spheres). Use your Part C numbers and your Part B axis counts as evidence, and name what the choice costs.

## Deliverable

- The completed `narrow.py` passing all ten tests, with the axis counter from step 7.
- A PDF of at most 3 pages: the hand predictions from step 1 next to your code's output, the axis-count results from step 7, the three-curve plot and explanation from Part C, and the Part D recommendation.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Implementation | All ten tests pass; square root only on hits; coincident centers handled | Eight or nine tests pass | Seven or fewer pass | 35 |
| Early-exit study (step 7) | Mean axes counted for both orders, difference explained | Counted for one order only | Missing | 15 |
| False-hit study (Part C) | Three curves plotted at 5° steps, plank shape explained with the radius formula | Curves plotted, explanation vague | Missing | 25 |
| Recommendation (Part D) | Shape chosen and justified with the pair's own numbers, cost named | Plausible, not backed by numbers | Missing | 25 |
| **Total** | | | | **100** |
