# AR101 · Lab 14: Build an atlas packer and write your pipeline chapter

**Assigned:** week 14 ([lecture](../lectures/w14-pipeline-export-atlases-import-settings.md)). **Due:** one week after the week 14 class. **Feeds:** the technical chapter of your style bible (assessment, 20%) and the export of your final portfolio piece.

## Objective

Finish a small atlas packer and texture memory calculator, use it to find the power-of-two cliff in a real sprite list, fix the cliff by changing the art budget rather than the tool, and turn the results into the pipeline chapter of the style bible you started in [Lab 13](lab13.md). You don't need prior programming beyond what CS101 covers in its first weeks. Every function is under 20 lines.

## Starter materials

The folder [`lab14-starter/`](lab14-starter/) contains:

- [`atlas.py`](lab14-starter/atlas.py). Six functions with docstrings that say exactly what they return, namely `next_pow2`, `texture_bytes`, `safe_mip_level`, `pack_shelves`, `choose_atlas` and `uv_rect`. Each raises `NotImplementedError` until you write it. It also has a `main` that loads a sprite list and prints atlas size, fill and memory for gutters 0, 2 and 4.
- [`test_atlas.py`](lab14-starter/test_atlas.py). Six tests. All six fail on the starter and all six pass on a correct solution.
- [`sprites.json`](lab14-starter/sprites.json). Forty invented HUD sprites for an MMO (24 item icons at 32×32, 8 markers at 24×24, 4 portraits at 64×64, 2 banners at 128×32 and 2 buttons at 96×24).

Run from inside the folder:

```
../../../../.venv/bin/python atlas.py sprites.json
../../../../.venv/bin/python test_atlas.py
```

On the starter, `atlas.py` prints the sprite count and "not implemented yet" for each gutter, and `test_atlas.py` prints six `FAIL` lines and exits with status 1. The tests also run under `pytest` if you have it.

## Steps

1. **Memory (30 min).** Implement `next_pow2` and `texture_bytes`. For block formats, remember that a level smaller than 4×4 still pays for one whole block. Check yourself against the lecture's table for a 2048×2048 atlas before running the tests.
2. **Gutter rule (10 min).** Implement `safe_mip_level` from the lecture's model. Write one sentence in your report explaining why the answer for a 3-pixel gutter is the same as for 2.
3. **Shelf packing (60 min).** Implement `pack_shelves`. The docstring gives the exact algorithm (tallest first, ties by name, fill left to right, new shelf under the tallest cell, round positions up to `align`). Draw the five-sprite test case on paper first. Then implement `choose_atlas` (try square powers of two from the smallest that fits one cell) and `uv_rect`.
4. **Run the real list (15 min).** Run `atlas.py sprites.json`. Record the atlas side, fill and memory in RGBA8, BC7 and BC1 (with mipmaps) for gutters 0, 2 and 4.
5. **Find and fix the cliff (45 min).** You should see the atlas jump in size as soon as the gutter is greater than 0. Find two different fixes and measure both. Candidates include allowing non-square atlases (write a `choose_atlas_rect` that also tries `W × H` with `W = 2H`), drawing every square sprite 4 pixels smaller inside its old cell size, and moving the banners and buttons to a second atlas. Be warned that not every candidate works alone, and some only work combined. Measure before you claim. For each fix, report the new atlas size, memory and safe mip level, and say what it costs the artist.
6. **Pipeline chapter (45 min).** Add a pipeline chapter to your Lab 13 bible, using section 5 of the lecture as a checklist. It must include an import settings table for the asset types in your zone, the gutter and cell rule you chose in step 5, the transparent-pixel rule, the file naming pattern, and which files are sRGB and which are linear.
7. **Optional extension.** Use Pillow (installed in the course `.venv`) to write `atlas.png` from the placements, extruding each sprite's edge pixels into its gutter. Load it in the interactive or any viewer and zoom out to confirm there is no bleeding.

## Deliverable

- Your completed `atlas.py`, with `test_atlas.py` output showing six `PASS` lines pasted into the report.
- `report.md` (500 to 800 words) with the step 4 table, the step 5 comparison of two fixes (atlas size, memory, fill, safe mip level, artist cost), and the one-sentence answer from step 2.
- The pipeline chapter added to your style bible (one to two pages).

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Correctness | All six tests pass; no changes to the tests | Four or five tests pass | Three or fewer pass | 30% |
| Measurement | Step 4 table complete for three gutters and three formats, numbers match a rerun | Table present with gaps | No measurements | 15% |
| Cliff analysis | Two fixes measured, each with size, memory, fill and safe mip level; artist cost stated and compared | One fix measured, or two without artist cost | Cliff not identified | 25% |
| Pipeline chapter | Import settings table, gutter and cell rule, transparent-pixel rule, naming and color-space rules, each with a test a reviewer could run | Chapter present, rules missing tests or one area missing | No chapter | 25% |
| Report clarity | Step 2 answer uses the model (`floor(log2 g)`) correctly; figures reproducible from the commands given | Answer present, reasoning thin | Missing | 5% |
