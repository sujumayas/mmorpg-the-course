# AR101 · Lab 07: Autotiler and seamless tile

**Week:** 7, tilesets and seamless tiling ([lecture](../lectures/w07-tilesets-and-seamless-tiling.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home for the art.
**Weight:** one of the weekly studies (50% of the course grade across all studies).

## Objective

Write the two neighbour-index rules from the lecture and prove they give 16 and 47 tiles. Then draw a seamless fill tile and a 16-tile edge set for a stone path, and test both with your own code.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Python standard library, plus Pillow for the image script (already in the course `.venv`).

- [`autotile.py`](lab07-starter/autotile.py) holds the bit tables, a `filled()` helper, a finished `tiles_used()` helper, and four empty functions: `edge_index`, `corner_rule`, `blob_index` and `seam_ratio`.
- [`test_autotile.py`](lab07-starter/test_autotile.py) holds the lecture's test values. They cover the plaza map (edge and blob index of all 8 path cells), the lone cell, plus sign and 3 by 3 block, the corner rule on four patterns, the count of 47, the diagonal-touch case from the interactive, and the seam ratio of the two 4 by 4 tiles from section 1 (1.0 and 3.0). All 8 tests fail on the starter.
- [`seam_check.py`](lab07-starter/seam_check.py) loads a square PNG, converts each pixel to CIE L* (0-100, as in week 1), runs your `seam_ratio`, prints PASS if the ratio is 1.5 or lower, and saves a 3 by 3 repeat of the tile at 4× zoom for you to inspect.
- The [interactive](../examples/w07-autotile.html) for spot checks.
- Any pixel editor you like. Aseprite, LibreSprite, Piskel (free, in the browser) and Krita all work.

Run the tests from the repository root:

```
.venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab07-starter/test_autotile.py
```

## Steps

1. **Edge index.** Implement `edge_index`. Run the tests. `test_edge_plaza` should pass.
2. **Corner rule and blob index.** Implement `corner_rule`, then `blob_index` on top of it. `test_forty_seven` must pass. In a comment, explain in one sentence why the diagonal-touch test expects no change.
3. **Seam ratio.** Implement `seam_ratio` exactly as the docstring defines it. All 8 tests should now pass.
4. **Fill tile.** Draw a 16 by 16 stone-path fill tile with at most 6 colors (week 6's palette limit). Run `seam_check.py` on it. Keep editing until it prints PASS, then open the 3 by 3 repeat and fix any single detail that forms an obvious grid, even if the number passes. Save each attempt's ratio.
5. **Edge set.** Draw the 16 edge tiles of the path on grass, laid out in index order 0 to 15 on a 4 by 4 sheet (64 by 64 pixels). Light comes from the top left. Reuse your fill tile as the interior of every piece.
6. **Test map.** Paint a 12 by 10 test map in the interactive or on paper that uses every one of the 16 edge indices at least once. Build it from your sheet (in Tiled, Godot, GameMaker or by pasting in the pixel editor) and take a screenshot at 2× scale.
7. **Blob gap.** Run `tiles_used(your_map, "blob")` on the same map. List the blob tiles your map would need that the edge set can't draw, and describe what each would look like.

## Deliverable

Submit one folder with:

- `autotile.py` with all tests passing.
- `fill.png` (16 by 16) and the seam ratios of your attempts, in order.
- `edge_set.png` (64 by 64, tiles in index order).
- `test_map.png` and the 0/1 grid of the map as a text file.
- `note.md`, at most 250 words, answering step 7 and saying whether you'd draw the full 47 for this game, and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All 8 tests pass; the diagonal-touch comment is correct | 6-7 tests pass | 5 or fewer pass | 25% |
| Seamless fill | Ratio at most 1.5 and no visible grid in the 3 by 3 repeat | Ratio passes but one detail forms a grid | Ratio above 1.5 | 20% |
| Edge set | All 16 pieces present, consistent border width and light direction | One or two pieces inconsistent | Pieces missing or wrong index order | 30% |
| Test map | Uses all 16 indices, correctly placed at 2× | Uses 12 or more, or one misplaced tile | Fewer than 12, or several misplaced | 10% |
| Blob-gap note | Names each missing blob tile by index and appearance, with a costed decision | Lists the tiles without a decision | Missing or wrong | 15% |
