# AR101 · Lab 01: The value checker

**Week:** 1, value before color ([lecture](../lectures/w01-seeing-like-an-artist-value-before-color.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home for the studies.
**Weight:** one of the weekly studies (50% of the course grade in total).

## Objective

Build a small tool that measures value (CIE L*) and flags figure and ground pairs that are too close, then use it on your own work. By the end you should be able to plan a game scene in three values, paint it in color, and prove with numbers that every gameplay-critical element separates from its ground.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python, no packages needed.

- [`value_check.py`](lab01-starter/value_check.py), a skeleton with four empty functions (`srgb_to_linear`, `lightness`, `band`, `check_scene`) and a finished loader and report. The docstrings give the exact formulas from lecture section 2.
- [`palette.csv`](lab01-starter/palette.csv), the lecture's dungeon palette (floors, potions, a coin, a player cloak, a moss-green enemy) as `name,r,g,b`.
- [`pairs.csv`](lab01-starter/pairs.csv), seven figure and ground pairs to check, as `figure,ground`.
- [`test_value_check.py`](lab01-starter/test_value_check.py) with the lecture's test values: pure red L* 53.24, middle gray (128) L* 53.59, pure green 87.74, pure blue 32.30, the low branch of the gamma curve, band boundaries, and the red potion failing on the stone floor with a gap of about 0.35.
- The [interactive](../examples/w01-value-view.html) for spot checks.

Run the tests from inside the folder with `python3 test_value_check.py`. On the starter they report 5 tests not passing. When all pass, run `python3 value_check.py palette.csv pairs.csv --min-gap 20`.

## Steps

1. **Implement.** Fill in the four functions until every test passes. Do not change the tests.
2. **Check the dungeon.** Run the report on the supplied palette. You should find four failing pairs. For each, write one line saying whether you would fix the figure or the ground, and why.
3. **Fix the dungeon.** Edit `palette.csv` so that all seven pairs pass at a gap of 20, changing as few colors as possible. Keep the potion recognizably red. Record the before and after RGB values.
4. **Three-value studies.** On paper or in any paint program, make three thumbnails (about 8 × 5 cm each) of three different game scenes of your choice: one interior, one exterior by day, one exterior by night. Use exactly three flat values. Mark the player, one enemy, one pickup and one goal in each.
5. **Color the best study.** Take one thumbnail and paint it in full color at a small game resolution (for example 320 × 180). Keep each element in the value group you planned.
6. **Prove it.** Sample the color of each marked element and the ground right next to it. Put them in your own `my_palette.csv` and `my_pairs.csv` (at least eight pairs) and run the checker. Iterate until every pair has a gap of at least 20, and the pickup and enemy have at least 30.
7. **The band test.** Run the report and look at the "band of 4" column. List any figure that shares a band with its ground even though its gap passes. Explain in two sentences why this can happen and whether it matters for your scene.

## Deliverable

A folder containing: `value_check.py` with all tests passing; the fixed `palette.csv`; the three thumbnails; the colored scene as a PNG; a grayscale (L*) version of it; `my_palette.csv`, `my_pairs.csv` and the checker's output; and a note of at most 400 words covering steps 2, 3 and 7.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Checker correctness | All tests pass; report runs on the student's own files | Tests pass, own files not run | Tests fail | 25% |
| Dungeon fix | All seven pairs pass with three or fewer color changes, reasoning given per pair | All pass with more changes or thin reasoning | Pairs still failing | 15% |
| Three-value studies | Three clear value plans, focal point placed deliberately in each, gameplay elements in a different group from their ground | Plans present, one merges a key element | Values muddled or more than three | 25% |
| Colored scene | Color version keeps the value plan; grayscale matches the thumbnail; every pair measured and passing | Minor drift from the plan, most pairs pass | Plan lost in color | 25% |
| Band analysis and note | Correct explanation of gap versus band edges with a judgment for this scene | Explanation present, no judgment | Missing | 10% |
