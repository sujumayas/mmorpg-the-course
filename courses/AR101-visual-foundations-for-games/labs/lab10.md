# AR101 · Lab 10: The chaos plate test

**Week:** 10 ([lecture](../lectures/w10-readability-in-chaos-vfx-and-telegraphing.md))
**Time:** 2 hours in the studio, plus up to 3 hours to finish.
**Work mode:** individual.
**Counts toward:** weekly studies (50% of the course grade, shared across the weekly labs).

## Objective

Design a ground telegraph for an invented boss attack that stays readable on an empty floor and under a pile of glowing player effects. Prove it with numbers, not with "it looks fine on my screen".

## Starter materials

- [`lab10-starter/chaos_plates.py`](lab10-starter/chaos_plates.py) writes four identical 512 × 512 "chaos plates": a stone floor at value 30 with 0, 2, 4 and 8 stacked additive effects over the telegraph area (each adds 10 value points, capped at 100, as in the lecture). A dashed guide circle marks where the telegraph goes: center (256, 300), radius 110. With `--demo` it also writes the lecture's fill-only and two-tone telegraphs on every plate.
- [`lab10-starter/contrast_probe.py`](lab10-starter/contrast_probe.py) measures a finished plate. It reports the median value (CIE L*) inside the circle, on its edge and just outside, the contrast of the fill and of the edge, and a verdict at the week 1 gap of 20.
- Any paint program with layers (Krita, GIMP, Aseprite, Photoshop or similar). Work on copies of the plates.
- The [telegraph headroom interactive](../examples/w10-telegraph-headroom.html) for quick what-if checks.

Run the starter first from inside `lab10-starter/`, using the course Python (`.venv/bin/python` from the repository root, which has Pillow):

```
python chaos_plates.py --demo
python contrast_probe.py demo_fill_n*.png demo_tone_n*.png
```

You should see the lecture's result in measured form. The fill-only telegraph reads about 42, 42, 31 and 0 contrast on the four plates and is "LOST" on the 8-effect plate. The two-tone telegraph never drops below 42.

## Steps

### Part A: brief and thumbnails (30 min)

1. Invent a boss attack that uses a ground telegraph (a slam, a cone breath, a line charge, a ring of spikes). Write two sentences: what the player must do, and how long the windup lasts.
2. Thumbnail six telegraph designs in grayscale, each about 5 cm across. Vary the value structure, not only the color: light fill, dark fill, light fill with dark rim, dark fill with light rim, patterned fill, hard-edged segments.
3. Circle the two you think will survive the 8-effect plate. Write one line of reasoning for each, using the headroom idea from the lecture.

### Part B: paint and measure (60 min)

4. Paint your best design on copies of all four plates. Keep the circle's size and position so the probe can find it (if your attack is a cone or line, keep a circular edge where the guide circle is, or pass your own `--cx --cy --r`). Use any colors and blending you like, but paint the same design on every plate. Do not repaint per plate.
5. Run `contrast_probe.py` on your four plates. Record the table.
6. If any plate reads "LOST", change the design (not the plate) and repeat. Keep the failed version and its numbers. You will hand both in.
7. Make a grayscale copy of each final plate and look at all eight images side by side at 25% zoom. Note anything the probe did not catch (for example a rim that reads but a fill that is too noisy).

### Part C: rationale (30 min)

8. Using the lecture's model, predict the fill and rim contrast of your final design on a floor of value 60 with 3 effects of 10 points each. Then paint that case (fill a copy of `plate_n0.png` to value 60 first, then add the effects by hand or by editing the script's `V_FLOOR`) and measure it. Report prediction and measurement side by side.
9. Write your rationale: which part of the telegraph carries the signal on each plate, and why.

## Deliverable

- One PNG contact sheet: the four final plates in color on the top row, the same four in grayscale below, plus the failed version's worst plate.
- The probe output for the failed and final versions (paste the text).
- A one-page PDF rationale: the attack brief (step 1), the prediction-versus-measurement table (step 8), and 200 to 300 words on why your design works, naming headroom and the two-tone rule where they apply.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Readability result | Final design reads 20 or more on all four plates and on the step 8 case | Fails on one plate, with a correct diagnosis | Fails on two or more plates, or not measured | 30 |
| Iteration evidence | Failed version, its numbers and the specific change that fixed it | Failed version shown but the change is vague | No iteration shown | 15 |
| Model use | Step 8 prediction within 8 points of the measurement, differences explained | Prediction made but not compared, or large unexplained gap | No prediction | 20 |
| Craft and design | Telegraph fits the attack brief, uses shape language deliberately, reads at 25% zoom | Readable but generic, or the shape does not match the attack | Unreadable at 25% zoom | 20 |
| Rationale writing | Names which part carries the signal on each plate, uses the lecture's terms correctly, 200-300 words | Correct but thin, or over length | Missing | 15 |
| **Total** | | | | **100** |
