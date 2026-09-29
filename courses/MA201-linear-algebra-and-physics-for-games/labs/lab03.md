# MA201 · Lab 03: Local and world space

**Week:** 3, transform hierarchies ([lecture](../lectures/w03-transform-hierarchies-local-and-world-space.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (40%).

## Objective

Write a 2D transform type with a basis and an origin, load a small scene tree from a file, and compute every node's world transform. Use the inverse to answer gameplay questions in a node's own space ("is the player ahead of the guard, and on which side?"). Then audit the scene for shear caused by non-uniformly scaled parents, measure what the rotation-only shortcut gets wrong, and propose a fix for every flagged node.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Python 3.10 or later, standard library only.

- [`xform.py`](lab03-starter/xform.py). The `Xform` class has `trs`, `columns`, `det` and the rotation-only `transpose_inverse` given. The `Scene` loader is given. You write ten methods in three parts:
  - Part A: `Xform.point`, `vector`, `__mul__` (compose) and `inverse` (raises `ValueError` for a singular basis).
  - Part B: `Xform.normal` (inverse transpose, then normalize) and `corner_angle`.
  - Part C: `Scene.world`, `to_local`, `describe` and `audit`.
- [`scene.csv`](lab03-starter/scene.csv): twelve nodes in five trees. The ship, crane and hook and the guard from the lecture; the bench and sign from the worked example, with a lamp on the sign; a tall tower with a flag; and the cart, crate and lantern from the in-class activity. Each row gives a local position, angle in degrees, and scale `(sx, sy)`.
- [`test_lab03.py`](lab03-starter/test_lab03.py): nine tests. Run `python test_lab03.py` from inside the folder. On the starter it reports `0/9 tests passed` and exits with status 1.
- The week 3 interactive, [`examples/w03-parent-scale-shear.html`](../examples/w03-parent-scale-shear.html), to check corner angles by eye.

## Steps

1. **Predict first.** By hand: the world origin of `Crane` and of `Hook`, the guard-local position of the player at (14, 9), and the corner angle of `Sign`. Write the numbers down.
2. **Part A.** Implement the four `Xform` methods. Make the point, compose, inverse, guard and hook tests pass. In your report, show one numeric example of `A * B ≠ B * A` from this scene.
3. **Part B.** Implement `normal` and `corner_angle`. Clamp the cosine to `[−1, 1]` before `acos`. Make the shear-table and normal tests pass.
4. **Part C.** Implement `world`, `to_local`, `describe` and `audit`. Make the remaining tests pass.
5. **World table.** For all twelve nodes print the world origin, world corner angle, world determinant and the two column lengths. Mark every node whose column lengths differ from its own local scale. Explain in one sentence why `Hook` has determinant 4 although its own scale is 1.
6. **Gameplay queries.** A monster walks the straight path from (−30, 10) to (30, 10), sampled at 13 points 5 m apart. For each point, report `describe("Guard", p)` and `describe("Lantern", p)`. Find where the monster crosses from the guard's left to its right, and check it against the x where the guard's facing line meets y = 10.
7. **The shortcut's error.** For each audited node, compute `to_local` of the point (3, 2) with the full inverse and with `transpose_inverse`. Report the distance between the two answers. Then do the same for `Hook` and explain why the shortcut is wrong there too, even though `Hook` has no shear. (Look at its determinant.)
8. **Three engines.** For `Sign` and `Flag`, compute the Unreal-style world basis `R(θ_total) · S_total`, where `θ_total` is the sum of angles on the path and `S_total` multiplies scales component by component (lecture section 3). Report its corner angle and determinant next to the matrix-product version. Say what each engine (Unity, Unreal, Godot) would draw.
9. **Fix the scene.** Apply the lecture's rule, "non-uniform scale only on leaves", by editing a copy of `scene.csv`. You may add unscaled parent nodes and move scale to a new leaf node that holds only the mesh. Rerun `audit()` and show it returns an empty list, while every mesh keeps its original world size along its own axes.

## Deliverable

Your `xform.py` with `python test_lab03.py` reporting `9/9 tests passed`, your fixed `scene_fixed.csv`, and a PDF of at most two pages with:

- Your step 1 predictions next to the code's values.
- The step 5 world table and the `Hook` sentence.
- The step 6 table of 13 points with the crossing marked.
- The step 7 and step 8 comparison tables.
- An audit table with one row per flagged node: its corner angle, the error of the shortcut inverse, and your fix from step 9 in one line.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 9/9 | 7-8 | 6 or fewer | 30% |
| World table and queries (steps 5-6) | All values correct; `Hook` determinant explained by the ship's scale; crossing found and checked against the facing line (x = 18.66) | Values correct, explanations thin | Missing or wrong | 20% |
| Shortcut error (step 7) | Distances correct; explains that the transpose inverts only rotations, so both shear and uniform scale break it | Distances correct, `Hook` unexplained | Missing | 15% |
| Engine comparison (step 8) | Both versions computed; equal determinants and different corner angles noted; each engine's display stated correctly | One node done, or engines unclear | Missing | 15% |
| Scene fix (step 9) | `audit()` empty; world sizes preserved and demonstrated with numbers | Audit empty but sizes changed | Missing | 20% |
