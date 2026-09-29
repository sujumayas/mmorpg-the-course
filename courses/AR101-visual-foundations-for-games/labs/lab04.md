# AR101 · Lab 04: The palette swapper

**Week:** 4, hue, saturation and value ([lecture](../lectures/w04-color-theory-hue-saturation-value.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** one of the weekly studies (50% of the course grade across all studies). The conversions are reused in lab 05.

## Objective

Build a tool that recolors a palette to a new hue while keeping every color's value (L*), then use it to make two variants of a creature you draw. You will see, in numbers and on the sprite, where the ceiling rule forces a variant to give up saturation.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python, run with the repository's `.venv/bin/python`.

- [`color_tools.py`](lab04-starter/color_tools.py): week 1's `lightness` (finished), file helpers, a command line, and six empty functions: `hex_to_rgb`, `rgb_to_hsv`, `hsv_to_rgb`, `match_value`, `swap` and `nearest_value`.
- [`test_color_tools.py`](lab04-starter/test_color_tools.py): tests built from the lecture's tables. On the starter every test prints `TODO` and the script exits with code 1.
- [`slime.hex`](lab04-starter/slime.hex): the lecture's green slime ramp. [`pico8.hex`](lab04-starter/pico8.hex): the 16 PICO-8 colors. Both use the Lospec `.hex` format, one color per line, and the loader skips lines starting with `;`.
- The [interactive](../examples/w04-palette-swap-value.html) for spot checks.

## Steps

1. **Conversions.** Write `hex_to_rgb`, `rgb_to_hsv` and `hsv_to_rgb` from lecture section 2. Wrap hue with `% 360` so rotations past 360° or below 0° work. Round channels with `int(x * 255 + 0.5)`.
2. **Matching.** Write `match_value(target, h, s)` with the two-step search from the lecture: bisect V first, and if V = 100% is not enough, bisect S instead.
3. **Swapping.** Write `swap(hexes, rotation, keep_value)`. Grays stay unchanged.
4. **Fixed palettes.** Write `nearest_value(target_hex, palette)`, the manual PICO-8 method.
5. **Test.** From the repository root run
   `.venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab04-starter/test_color_tools.py`
   until it prints `all tests pass`.
6. **Try it.** `.venv/bin/python .../color_tools.py .../slime.hex 120` and again with `naive` as a third argument. Compare the L* columns with the lecture's tables.
7. **Draw.** In any pixel editor, draw an invented creature on a 32 × 32 canvas with one ramp of four or five steps, a black outline and a transparent background. Export its ramp as `creature.hex`.
8. **Make variants.** Choose a rotation that turns your creature into a clearly different "element" (for example fire to ice). Produce `variant_naive.hex` and `variant_kept.hex`, recolor two copies of the sprite with them, and place all three on the same mid-gray background.
9. **Measure.** For both variants, list each step's L*, the ΔV to its neighbors and to the outline, and flag any ΔV under 10.

## Deliverable

Submit a folder with:

- `color_tools.py` with passing tests (the grader runs the provided test file, unchanged).
- `creature.hex`, `variant_naive.hex`, `variant_kept.hex`.
- `lineup.png`: the three creatures side by side at 4× nearest-neighbor scale on mid-gray `(128, 128, 128)`, plus a grayscale copy `lineup_gray.png` made with a lightness-based conversion (week 1).
- `note.md`, at most 300 words: which steps changed value in the naive swap and by how much, which steps in the kept variant had to give up saturation and why (use the ceiling rule), and whether the kept variant still reads as "the same creature, different element."

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tool correctness | All provided tests pass, including hue wrap, grays and the ceiling branch | Tests pass after small fixes by the grader | Tests fail | 35% |
| Creature and ramp | Invented design, clear four- or five-step ramp, clean outline | Ramp present but steps uneven or muddy | No ramp or borrowed character | 15% |
| Variants | Naive and kept variants correct; kept variant within 1 L* per step | One variant has errors | Variants missing | 20% |
| Measurement | ΔV table complete, merges flagged, matches the PNGs | Table partly complete | Missing | 15% |
| Explanation | Uses the ceiling rule to explain every saturation loss, with numbers | Explains in general terms | Missing or incorrect | 15% |
