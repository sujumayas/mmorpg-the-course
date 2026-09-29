# MA201 · Lab 02: The isometric picker

**Week:** 2, matrices and linear transformations ([lecture](../lectures/w02-matrices-and-linear-transformations.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (40%).

## Objective

Build the tile-to-screen matrix for a diamond-tile map, invert it to turn clicks into tiles, and prove with measurements that the "divide by the tile size" shortcut is wrong for half of all clicks. Then add camera zoom and a mirrored map and show that the matrix picker keeps working with no new code, while a hand-tuned picker would not.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Python 3.10 or later, standard library only.

- [`mat2.py`](lab02-starter/mat2.py). Matrices are tuples of rows. `columns`, the rectangle method `rect_pick` and the `MIRROR_X` matrix are given. You write nine functions in three parts:
  - Part A: `mat_vec`, `mat_mul`, `det`, `inverse` (returns `None` when the determinant is below `1e-9` in size).
  - Part B: `tile_matrix`, `tile_to_screen`, `screen_to_tile` (returns `None` when there is no inverse), `error_rate`.
  - Part C: `zoom`.
- [`test_lab02.py`](lab02-starter/test_lab02.py): eight tests, including the lecture's two tables. Run `python test_lab02.py` from inside the folder. On the starter it reports `0/8 tests passed` and exits with status 1.
- The week 2 interactive, [`examples/w02-isometric-basis.html`](../examples/w02-isometric-basis.html), whose error map you can compare with your step 5 output.

## Steps

1. **Predict first.** By hand: `det` and inverse of `[3 1; 2 5]`, the screen position of tile (4, 1)'s center for 64 × 32 tiles, and the tile under the click (20, 20) for 32 × 16 tiles. Write the numbers down.
2. **Part A.** Implement the four matrix functions. Make the first three tests pass. In your report, show one product where `A B ≠ B A` and one pair of non-identity matrices where they are equal, and explain the second from the pictures.
3. **Part B.** Implement `tile_matrix`, `tile_to_screen` and `screen_to_tile`. Use `math.floor`, not `int()`. Make the table tests and the round-trip test pass. Then change `math.floor` to `int` on purpose, rerun, and record which test fails and which click causes it. Change it back.
4. **Error rate.** Implement `error_rate`. Measure it for 64 × 32, 96 × 48 and 128 × 64 tiles over a region at least 8 tiles wide. Then write `error_rate_general(w, h)` for tiles whose height is not half their width (try 64 × 37, near true isometric). Does the rectangle method's error stay at one half? Use the determinant to explain the answer.
5. **Fix the rectangle method.** DevilutionX, the Diablo source port, keeps the rectangle step and adds a corner test (lecture section 3). Write `rect_pick_fixed(w, h, x, y)` that computes the position `(px, py)` inside the rectangle and compares it against the two diagonal lines of the diamond to move to the right neighbour. Show that its error rate is 0 for 64 × 32. Then try it on 64 × 37 without changing any constant and report what happens.
6. **Zoom.** Implement `zoom`. Build `Z M` for zoom 2 and zoom 0.5 and confirm the picker still works by round-tripping every tile center in an 8 × 8 map. Record the determinant of each matrix and relate it to the tile's on-screen area in pixels.
7. **Zoom about the mouse.** Players expect the scroll wheel to zoom toward the cursor, not toward the screen origin. Using `origin` as the only extra state, write `zoom_about(M, origin, k, cursor)` that returns a new `(M, origin)` pair so the tile under the cursor stays under the cursor. Test it with the cursor at (200, 150). (Next week's lecture explains why the origin has to change when you do this. Week 4 packs both into one matrix.)
8. **Mirror.** Use `MIRROR_X` to build a mirrored map, `F = MIRROR_X · M`. Record `det(F)`, round-trip the tile centers, and explain in two sentences why the picker still works, and what a 3D renderer would do to a floor mesh drawn with this matrix (lecture section 5).

## Deliverable

Your `mat2.py` with `python test_lab02.py` reporting `8/8 tests passed`, your extra functions from steps 4, 5 and 7, and a PDF of at most two pages with:

- Your step 1 predictions next to the code's values.
- The step 3 `int` versus `floor` failure: the test, the click and the two answers.
- A table of error rates from steps 4 and 5 for every tile size you tried, with the determinant explanation.
- The step 6 determinants and areas, and the step 7 test showing the cursor's tile is unchanged after zooming.
- A 200-word recommendation to a team deciding between the matrix picker and a hand-tuned rectangle picker, citing at least three numbers from your tables.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 8/8 | 6-7 | 5 or fewer | 30% |
| Error analysis (steps 3-5) | Floor bug reproduced with the exact click; error rates correct for all sizes; the one-half result explained as diamond area over rectangle area (det over w h); fixed picker at 0% and its failure at 64 × 37 explained | Rates correct, explanation missing or partial | Missing or wrong | 25% |
| Zoom and mirror (steps 6-8) | Determinants and areas agree; zoom-about-cursor keeps the tile to within 1e-9; mirror explained with winding | Two of three parts correct | Missing | 20% |
| Order of operations (step 2) | Non-commuting and commuting examples, the second explained geometrically | Examples without explanation | Missing | 10% |
| Recommendation | Under 200 words, a clear choice backed by three numbers | Choice made, weak evidence | Missing or generic | 15% |
