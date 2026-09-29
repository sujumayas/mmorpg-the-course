# AR101 · Lab 12: The color-blind audit

**Week:** 12 ([lecture](../lectures/w12-accessibility-color-blindness-and-contrast.md))
**Time:** 2 hours in the studio, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** weekly studies (50% of the course grade, shared across the weekly labs). The audit table you produce here goes into your style bible (week 13).

## Objective

Build a small color-blind simulator and auditor, prove the red-and-green raid telegraph from the lecture fails, and design a telegraph set for an invented boss that passes for all four viewers on two different floors without any special mode.

## Starter materials

- [`lab12-starter/cvd_check.py`](lab12-starter/cvd_check.py): a Python 3 skeleton (standard library only). The Machado et al. (2009) severity 1.0 matrices and the week 1 color functions are provided. You write `simulate`, `contrast_ratio` and `audit`.
- [`lab12-starter/test_cvd_check.py`](lab12-starter/test_cvd_check.py): six tests built from the lecture's tables. All fail on the starter.
- [`lab12-starter/raid_palette.csv`](lab12-starter/raid_palette.csv) and [`lab12-starter/raid_pairs.csv`](lab12-starter/raid_pairs.csv): the lecture's red-and-green design (floor, danger, safe) and its three critical pairs.
- [`lab12-starter/render_sheet.py`](lab12-starter/render_sheet.py): draws a simple arena (boss marker, danger zone, safe zone) through all four viewers as one PNG. It uses your `simulate`, so it only works once the tests pass. Needs Pillow, which the course `.venv` has. Optional palette rows: `rim` for a dark ring around the danger zone, `safe_ring` to draw the safe zone as a dashed ring with chevrons.
- The [color-blind telegraph interactive](../examples/w12-colorblind-telegraph.html) for quick checks.
- A paint or layout tool for the final mockups.

Run the tests first from inside `lab12-starter/`, with the course Python:

```
python test_cvd_check.py
```

## Steps

### Part A: the tool (40 min)

1. Implement `simulate`, `contrast_ratio` and `audit` following their docstrings. Run the tests until all six pass.
2. Run `python cvd_check.py raid_palette.csv raid_pairs.csv`. You should see 1 of 12 pair-mode checks pass. The only pass is danger against safe for protanopia, where the red darkens enough to open a gap of 27. The values match the lecture's tables to within 0.1 or 0.2, because the tool rounds simulated colors to whole sRGB numbers.
3. Run `python render_sheet.py raid_palette.csv` and look at `raid_palette_fourup.png`. Write one sentence per viewer describing what they see.

### Part B: design a telegraph set (50 min)

4. Invent a boss attack with at least four gameplay-critical visuals: a danger zone, a safe zone, and two more of your choice (a "stack here" marker, a "spread out" marker, a debuff icon, an add's highlight, a targeting beam).
5. The fight happens on two floors: the mossy stone from the lecture, `#607048`, and a pale sand floor of your choice with L* between 70 and 85.
6. Write a palette CSV and a pairs CSV. The pairs must include every critical element against both floors, and every pair of critical elements that mean different things.
7. Iterate until every pair passes ΔV ≥ 20 in all four modes. Where two elements are meant to be told apart by shape rather than value, you may leave their ΔV under 20, but only if you list the shape difference in your rationale (step 10).
8. Render four-up sheets for both floors (make one palette file per floor if you like).

### Part C: check and record (30 min)

9. Paint a mockup of the attack at game scale on each floor, then run it through the lecture's routine from section 4: grayscale, then simulation (render sheets or the interactive), then the pair table. Note anything the table missed.
10. Write the rationale and the style bible entry: for each critical element, its colors, its value band, its shape or pattern, and the minimum ΔV it must keep.

## Deliverable

- The four-up renders of the lecture's design (from step 3) and of your final design on both floors.
- The audit report before and after (paste the tool's output).
- Your two mockups, in color and grayscale.
- A PDF of at most 3 pages: the attack brief, the step 3 sentences, a 250 to 350 word rationale naming which channel (value, shape, pattern, motion) carries each distinction, and the style bible entry from step 10.
- Your finished `cvd_check.py` and CSV files.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Tool correctness | All six tests pass; step 2 output matches; step 3 observations correct | Tests pass but outputs misread | Tests fail | 20 |
| Audit coverage | Pairs cover every critical element on both floors and every pair with different meanings | One floor or a few pairs missing | Pairs chosen arbitrarily | 15 |
| Accessible result | Every value-based pair passes ΔV ≥ 20 in all four modes on both floors; shape-coded exceptions listed and convincing | One or two failures with a plan to fix them | Many failures, or the design relies on hue alone | 30 |
| Craft | Mockups read in grayscale at game scale; the set looks like one encounter | Readable but inconsistent | Unreadable in grayscale | 20 |
| Rationale and bible entry | Names the carrying channel for each distinction; entry has numbers another artist could check | Correct but vague | Missing | 15 |
| **Total** | | | | **100** |
