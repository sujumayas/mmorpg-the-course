# AR101 · Lab 05: A zone palette

**Week:** 5, palettes and color harmony ([lecture](../lectures/w05-palettes-and-color-harmony.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** one of the weekly studies (50% of the course grade across all studies). The palette you make here is the one you draw with in lab 06, and it can seed your style bible in week 13.

## Objective

Write the ramp and harmony functions from the lecture, then design a palette of at most 16 colors for an invented MMO zone. The palette must pass a provided checker: at least three ramps whose value rises at every step, and one reserved gameplay color that stands apart in both hue and value.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python, run with the repository's `.venv/bin/python`.

- [`palette.py`](lab05-starter/palette.py): finished color helpers from weeks 1 and 4 (`lightness`, `hsv_to_rgb`, `rgb_to_hsv`, `solve_v`), a finished palette checker and report, and four empty functions: `lerp_hue`, `ramp`, `harmony` and `even_ramp`.
- [`test_palette.py`](lab05-starter/test_palette.py): tests from the lecture's tables and check-yourself answers. On the starter six tests print `TODO` and the script exits with code 1.
- [`broken_zone.hex`](lab05-starter/broken_zone.hex): an invented "mossy ruins" palette with two deliberate faults. Run the checker on it to see the file format and what a failure looks like.
- The [interactive](../examples/w05-hue-shift-ramp.html), including its paste box, for trying ramps by eye.

### Palette file format

Lospec `.hex`, one color per line, with comment lines that group the colors:

```
; ramp grass
1c332b
29603b
2a8c2a
; ramp stone
...
; reserved
ff3aa0
; neutral
000000
```

Ramps list colors dark to light. The checker counts unique colors across all groups, so a color shared by two ramps counts once.

## Steps

1. **Hue lerp.** Write `lerp_hue`. Test it by hand on the lecture's examples first.
2. **Ramp.** Write `ramp` from the lecture model. Your output must match the lecture's tables within one channel step.
3. **Harmony.** Write `harmony(base, scheme)` for the six schemes in the lecture's table, in the table's order, all mod 360.
4. **Even ramp.** Write `even_ramp`, which picks each step's V so its L* lands exactly on an even staircase, lowering S only where the ceiling forces it.
5. **Test.** From the repository root run
   `.venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab05-starter/test_palette.py`
   until it prints `all tests pass`.
6. **Read the broken palette.** Run `.venv/bin/python .../palette.py .../broken_zone.hex`. Write one sentence for each problem it reports, saying how you would fix it.
7. **Brief.** Invent a zone for an MMO: a name, a biome, the time of day, and the light source (sun, moon, lava, crystals). Write it in three sentences. The light source decides which way your ramps shift.
8. **Hues.** Choose a harmony scheme and a base hue. Use `harmony` to get the hues for your main materials. Choose a reserved hue for the zone's most important gameplay signal (loot, hazard or quest object) at least 60° away from every ramp.
9. **Ramps.** Build at least three ramps with `ramp` or `even_ramp`. Share dark ends where it saves slots. Save the result as `zone.hex` with group comments.
10. **Check.** Run the checker until it prints `PASS`. Then look at the palette in the interactive's paste box and adjust by eye; rerun the checker after every change.

## Deliverable

Submit a folder with:

- `palette.py` with passing tests (the grader runs the provided test file, unchanged).
- `zone.hex`, which must pass `check_palette` with the default settings.
- `swatch.png`: every ramp as a row of squares at least 32 × 32 pixels, the reserved color and neutrals on a final row, and under it the same image converted to gray by lightness (week 1).
- `rationale.md`, one page (at most 450 words): the zone brief, the harmony scheme and base hue with the numbers from `harmony`, the direction and size of each ramp's hue shift and why it matches your light source, which colors are shared between ramps, and why your reserved color will read on the zone's large areas (give the ΔV).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All provided tests pass | Tests pass after small fixes by the grader | Tests fail | 30% |
| Checker | `zone.hex` passes with no changes by the grader | Passes after a one-line fix | Fails | 15% |
| Ramps | Each ramp reads as one material, shifts consistently toward the stated light, clear value steps | Ramps pass the checker but hue shift is arbitrary or inconsistent | Straight or muddy ramps | 20% |
| Hue plan and reserved color | Scheme stated with numbers; reserved color clearly separate in hue and value, justified with ΔV | Scheme named but numbers or justification thin | No plan, or reserved color blends in | 20% |
| Rationale | Every decision tied to the brief and the lecture's models | Decisions described without reasons | Missing or generic | 15% |
