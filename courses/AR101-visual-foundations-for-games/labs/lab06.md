# AR101 · Lab 06: A readable sprite

**Week:** 6, pixel art fundamentals ([lecture](../lectures/w06-pixel-art-fundamentals.md)).
**Time:** 2 hours in studio, plus up to 4 hours at home.
**Weight:** one of the weekly studies (50% of the course grade across all studies). You may reuse the sprite in later studies.

## Objective

Draw one small sprite that reads at 1×, uses only your lab 05 zone palette, has clean lines and consistent light, and survives export at an integer scale. A provided checker verifies the countable rules; your review sheet shows you can find and fix the rest.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). The checker is a finished tool (standard-library Python, run with `.venv/bin/python`).

- [`check_sprite.py`](lab06-starter/check_sprite.py): checks size, palette use, color count, orphan pixels and exact integer scaling. Exit code 0 means every rule passes.
- [`sample_potion.png`](lab06-starter/sample_potion.png), [`sample_potion_4x.png`](lab06-starter/sample_potion_4x.png), [`sample_potion_2_5x.png`](lab06-starter/sample_potion_2_5x.png) and [`sample.hex`](lab06-starter/sample.hex): an invented 16 × 16 potion with two deliberate faults and a badly scaled copy. Run the checker on them first so you know what its messages mean.
- [`test_check_sprite.py`](lab06-starter/test_check_sprite.py): self-tests for the checker. You only need them if you modify it.
- Your `zone.hex` from lab 05, and any pixel editor that exports PNG with nearest-neighbor scaling (Aseprite, LibreSprite, Pyxel Edit, Piskel, GIMP or Krita).
- The [interactive](../examples/w06-clean-pixel-lines.html) for checking run patterns.

Try the samples from the repository root:

```
P=courses/AR101-visual-foundations-for-games/labs/lab06-starter
.venv/bin/python $P/check_sprite.py $P/sample_potion.png --palette $P/sample.hex --scaled $P/sample_potion_4x.png
.venv/bin/python $P/check_sprite.py $P/sample_potion.png --scaled $P/sample_potion_2_5x.png
```

The first run reports one off-palette color (`c33a52`, a near-copy of the liquid color) and two orphan pixels at (4,9) and (7,11). The second reports that the enlargement is ×2.5, not a whole number.

## The brief

Draw a creature, character or item that belongs in the zone you invented in lab 05. It must be your own design; no existing game characters.

- **Canvas:** 16 × 16, 24 × 24 or 32 × 32, transparent background.
- **Colors:** only colors from your `zone.hex`, at most 8 opaque colors in the sprite.
- **Silhouette:** readable when filled with one color at 1× (week 3's test).
- **Light:** one light direction, stated in your review sheet, with no pillow shading.
- **Lines:** at least one straight edge at least 6 pixels long at a clean slope (1:1, 2:1, 3:1 or their steep versions), and no jaggies on any straight edge.
- **Outline:** your choice of black, colored or selective, with ΔV of at least 20 (week 1) between the outline and the zone's main ground color.
- **Orphans:** at most 4, each one justified.
- **Export:** the sprite at 1× and at 4× nearest-neighbor.

## Steps

1. **Thumbnails (15 min).** On a 64 × 64 canvas, block four silhouettes at your target size in one color. Pick the one that reads best at 1×.
2. **Base colors (15 min).** Fill the chosen silhouette with the middle step of each material's ramp. No shading yet.
3. **Light and shade (30 min).** Pick a light direction. Shade with your ramps away from the light. Check for banding and pillow shading.
4. **Lines and outline (20 min).** Clean every straight edge to a single run pattern. Add the outline and remove doubles.
5. **Clean-up (15 min).** Run the checker with `--palette`. Remove or justify every orphan it lists.
6. **Export and check.** Export `sprite.png` at 1× and `sprite_4x.png` at 4× with nearest-neighbor. Run:
   `.venv/bin/python .../check_sprite.py sprite.png --palette zone.hex --scaled sprite_4x.png`
   until it prints `PASS`.
7. **Review sheet.** Fill in the sheet described below.

## Deliverable

Submit a folder with:

- `sprite.png` and `sprite_4x.png` that pass the checker with your `zone.hex` (included in the folder).
- `on_ground.png`: the sprite at 4× on a 128 × 128 patch of your zone's main ground color, plus `silhouette.png`, the sprite filled with a single color.
- `review.md` (at most 400 words):
  - the light direction and the ramp steps used for lit, mid and shadow areas;
  - the clean edge: its width, height, run list and period, with the coordinates of its first pixel;
  - the outline's L*, the ground's L*, and the ΔV;
  - each orphan pixel with coordinates and why it stays;
  - one problem you found and fixed during steps 3-5 (jaggy, double, banding or pillow shading), with before and after coordinates.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Checker rules | Passes with no changes by the grader | Passes after one small fix | Fails | 20% |
| Readability | Silhouette and interior read at 1× on the zone ground; outline ΔV at least 20 | Reads at 4× but muddy at 1×, or ΔV between 10 and 20 | Does not read at 1× | 25% |
| Lines and pixel craft | Clean edge with correct run list; no jaggies, doubles or unjustified orphans | One or two minor faults | Many faults | 20% |
| Light and color | One consistent light direction; ramps used as ramps; no pillow shading or banding | Mostly consistent, one area off | Pillow shading or random shading | 20% |
| Review sheet | All five items complete, with numbers that match the files | Items present but numbers missing or wrong | Missing | 15% |
