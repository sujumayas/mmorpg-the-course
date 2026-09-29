# MA201 · Lab 04: A software camera

**Week:** 4, homogeneous coordinates and projection ([lecture](../lectures/w04-homogeneous-coordinates-and-projection.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (40%).

## Objective

Build the whole path from a world-space point to a pixel in about 60 lines of Python, with no graphics library. You will check every stage against the lecture's numbers, write the FOV converter a settings screen needs, and measure how the near plane controls depth precision. By the end you should be able to debug a wrong projection in any engine by printing four numbers.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Python 3.10 or later, standard library only.

- [`camera.py`](lab04-starter/camera.py). Column-vector 4×4 helpers are given (`identity`, `mat_mul`, `apply`, `rot_y`). You write eleven functions in four parts:
  - Part A: `translate`, `scale`, `point`, `direction`, `rigid_inverse`.
  - Part B: `perspective` and `project` (world point to pixel, or `None` if clipped).
  - Part C: `hfov_from_vfov`, `vfov_from_hfov`, `vfov_from_setting` for the conventions `"vertical"`, `"horizontal"` and `"horizontal43"`.
  - Part D: `z_ndc` and `depth_step`, the smallest depth difference a 24-bit depth buffer can resolve at a given distance.
- [`test_lab04.py`](lab04-starter/test_lab04.py): ten tests. Run `python test_lab04.py` from inside the folder. On the starter it reports `0/10 tests passed`, and every test says `TODO` until you fill in the function it needs.
- The week 4 interactive, [`examples/w04-fov-frustum.html`](../examples/w04-fov-frustum.html), to check conversions by eye.

## Steps

1. **Predict first.** Before coding, compute by hand: the result of `translate(3, 0, −2)` on the point and on the direction `(1, 1, 1)`, and the pixel position of `(2, 1, −10)` for vertical FOV 75° on a 1920 × 1080 screen. Write the numbers down. You will compare them with your code.
2. **Part A.** Implement the affine helpers. `rigid_inverse` must use the transpose rule from lecture section 2, not a general inverse. Make `test_translate_point_and_direction`, `test_order_matters`, `test_scale` and `test_rigid_inverse` pass.
3. **Part B.** Implement `perspective` and `project`. `project` must multiply `P · V`, apply it to the point with `w = 1`, reject the point if `w ≤ 0` or any of `x, y, z` lies outside `[−w, w]`, then divide and map to pixels with pixel `y` growing downward. Make the three projection tests pass.
4. **Walk the camera.** Place a camera at `(0, 1.6, 8)` turned 20° about y (`C = translate(0, 1.6, 8) · rot_y(20)`), and use `V = rigid_inverse(C)`. Project the eight corners of a 2 × 2 × 2 cube centered at `(0, 1, 0)` onto 1920 × 1080 with vertical FOV 70°. Record the eight pixel positions. Sketch the cube from them on paper, or plot them, and check that it looks like a cube seen from the front-right.
5. **Part C, the settings table.** Implement the conversions. Then produce a table for a settings screen: for the settings values 60, 75, 90 and 105 under each of the three conventions, give the vertical and horizontal angles on 4:3, 16:10, 16:9, 21:9 and 32:9. That is 12 rows. Mark every cell where the horizontal angle exceeds 130°.
6. **Part D, depth precision.** Implement `z_ndc` and `depth_step`. Using far = 4000, compute `depth_step` at 10, 100, 300 and 1,000 m for near = 0.05, 0.1, 0.3 and 1.0 m. You should find about 0.107 m at 300 m for the Godot default near of 0.05. Then repeat for near = 0.05 with far = 400 and far = 40,000. Write one sentence on which parameter matters.
7. **Z-fighting budget.** A castle wall in your game has a decal 2 cm in front of it, and players see the wall from up to 300 m away. Find the smallest near plane that keeps `depth_step(300)` below 2 cm. Explain what gameplay case (a camera close to a wall, a first-person weapon model) that near plane might break.

## Deliverable

Your `camera.py` with `python test_lab04.py` reporting `10/10 tests passed`, plus a PDF of at most two pages with:

- Your step 1 predictions next to the code's values.
- The eight cube corners from step 4 and your sketch or plot.
- The 12-row FOV table from step 5.
- The depth-step tables from step 6 and the sentence.
- A 300-word recommendation for a third-person MMO camera: the FOV convention, default and range for the slider, and the near and far planes, with the numbers from steps 5 to 7 as evidence.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 10/10 | 7-9 | 6 or fewer | 30% |
| Camera walk (step 4) | All eight corners correct to 0.5 px, sketch clearly a cube from the front-right | Corners correct, no check of the picture | Wrong or missing | 15% |
| FOV table (step 5) | All 12 rows correct to 0.01°, over-130° cells marked, conventions labelled | Minor errors in one convention | Missing or mostly wrong | 20% |
| Depth analysis (steps 6 and 7) | Tables correct, sentence names the near plane and cites the 2n rule or the numbers, near value found for step 7 with a named trade-off | Numbers right, reasoning thin | Missing | 20% |
| Recommendation | Under 300 words, every choice backed by a number from the lab, a designer could act on it | Choices made but some unsupported | Missing or generic | 15% |
