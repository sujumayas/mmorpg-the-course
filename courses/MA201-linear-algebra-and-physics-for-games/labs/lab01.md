# MA201 · Lab 01: Floor, wall or ceiling

**Week:** 1, vectors in 3D and the cross product ([lecture](../lectures/w01-vectors-in-3d-and-the-cross-product.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (40%).

## Objective

Write the cross product and the triangle tools every 3D engine relies on, then use them to classify a small test level the way three engines would. You will find the triangles whose class depends on the engine, catch a triangle authored with the wrong winding, and handle a degenerate one without crashing. The result is a slope-audit tool you could run on a real level before a playtest.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Python 3.10 or later, standard library only.

- [`vec3.py`](lab01-starter/vec3.py). Vector basics (`add`, `sub`, `scale`, `dot`, `length`) and a CSV loader are given. You write seven functions in three parts:
  - Part B: `cross`, `normalize` (returns `None` below length `1e-9`), `triangle_normal`, `triangle_area`.
  - Part C: `classify(n_hat, preset, up)` for the presets `"ue5"`, `"ue3"` and `"godot47"` defined at the top of the file, and `side(forward, to_target, up)`.
  - Part D: `area_by_class(triangles, preset, up)`.
- [`level.csv`](lab01-starter/level.csv): 18 triangles in a Y-up world. A 10 × 10 floor, five ramps (1:4, 3:4, 1:1, 1.01:1, 6:5), a wall, a ceiling, one ramp triangle with its corners in the wrong order, and one sliver whose three corners lie on a line. [`make_level.py`](lab01-starter/make_level.py) regenerates it and shows how each piece was built.
- [`test_lab01.py`](lab01-starter/test_lab01.py): nine tests. Run `python test_lab01.py` from inside the folder. On the starter it reports `0/9 tests passed` with every test marked `TODO`, and it exits with status 1 until all nine pass.
- The week 1 interactive, [`examples/w01-walkable-slope.html`](../examples/w01-walkable-slope.html), to check single ramps by eye.

## Steps

1. **Predict first.** Before coding, compute by hand: `(2, 1, 0) × (1, 3, 2)`, the unit normal of the triangle `(0, 0, 0)`, `(0, 0, 1)`, `(4, 3, 0)`, and its area. Write the numbers down to compare with your code.
2. **Part B.** Implement the four triangle functions. `triangle_normal` must return `None` for the sliver, not raise and not return `NaN`. Make the first four tests pass.
3. **Part C.** Implement `classify` using the rule table in the docstring at the top of `vec3.py`. Clamp dot products to `[−1, 1]` before calling `acos`, or a normal of length 1.0000001 will crash your tool. Implement `side`. Make the lecture-table, flipped-winding, custom-up and side tests pass.
4. **Part D.** Implement `area_by_class`. Every result must have all four keys, even when an area is 0. Make the last test pass. Checkpoint: under `"godot47"` the floor area is about 129.59 m².
5. **Audit table.** For each of the 18 triangles, print its name, `n̂`, `n̂ · û`, slope angle, area, and its class under all three presets. Mark each row where the presets disagree. You should find seven: four ramp triangles that differ between floor and wall, and three triangles that Godot calls ceiling while both Unreal presets call wall. Explain each group in one or two sentences, and say which of the three is the authoring bug.
6. **Z-up port.** Your team moves the level to Unreal, which is Z-up. Convert every vertex with `(x, y, z) → (x, z, y)`, then classify with `up = (0, 0, 1)`. Compare with step 5. Which classes changed, and why? (Hint: swapping two axes is a mirror. Compute the determinant of that swap, then check what happened to every normal.) Fix the conversion so that no class changes, and explain the fix.
7. **Designer rule.** Find the largest rise : run with run 1 (to 0.01) that is a floor under all three presets, and the smallest that is a wall under all three. Turn them into a two-line rule for level designers.

## Deliverable

Your `vec3.py` with `python test_lab01.py` reporting `9/9 tests passed`, plus a PDF of at most two pages with:

- Your step 1 predictions next to the code's values.
- The step 5 audit table with the disagreeing rows marked and explained.
- The step 6 comparison and your corrected conversion, with the determinant argument.
- A 250-word memo to your level designers recommending one slope limit and an authoring margin, using the step 7 numbers and at least one number from the audit table.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 9/9 | 7-8 | 6 or fewer | 30% |
| Audit table (step 5) | All 18 rows correct, all seven disagreeing triangles found, each group explained by its `n̂ · û` and the thresholds, the flipped ramp named as the bug | Rows correct, explanations thin or one missed | Missing or mostly wrong | 20% |
| Z-up port (step 6) | Explains that the swap has determinant −1, that it flips every normal, and fixes it by also swapping two corners (or negating the normal) with a check that all classes match | Finds the problem, fix unexplained | Missing | 20% |
| Designer rule (step 7) | Both limits correct to 0.01, rule stated in degrees and rise : run | Limits correct, rule vague | Missing | 10% |
| Memo | Under 250 words, one clear limit with a margin, backed by numbers from the lab | Recommendation made but unsupported | Missing or generic | 20% |
