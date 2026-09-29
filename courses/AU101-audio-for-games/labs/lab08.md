# AU101 · Lab 08: A layered score from an intensity curve

**Week:** 8 ([Adaptive music: vertical layering](../lectures/w08-adaptive-music-vertical-layering.md))
**Time:** one 2-hour lab session plus about 2 hours at home
**Work:** individually

## Objective

Build the vertical layering model from the lecture in code, hear it, and tune it. You implement the stem ramp, the mix level and the asymmetric smoother. A complete synthesizer in the starter then renders 32 seconds of layered music to a WAV file from a scripted fight. Finally, you retune thresholds and rates for a different encounter and defend your choices with numbers.

## Starter materials

- Python 3.10 or later, standard library only (`math`, `random`, `struct`, `wave`). In this repository use `.venv/bin/python`. Any audio player can open the WAV files.
- [`lab08-starter/layers.py`](lab08-starter/layers.py), which contains:
  - `STEMS`: the four stems from the lecture as `(name, threshold, width)` rows. The pad is the bed (`None`).
  - `stem_gain(x, a, w)`, `level_db(gains)` and `smooth(current, target, up_rate, down_rate, dt)`: you write them.
  - `equal_power(r)`: complete, used in Part C.
  - `render(intensity_at, seconds, path, ...)`: complete. It synthesizes a pad, drums, bass and lead from sine waves and noise at 120 BPM in a 4-bar loop, smooths the intensity sample by sample, mixes the stems by their gains, applies a fixed −6 dB master trim and writes a mono 16-bit WAV.
  - `demo_intensity(t)`: a scripted fight (calm, spotted, peak, over).
- [`lab08-starter/test_layers.py`](lab08-starter/test_layers.py): 12 unit tests. Do not edit it. On the starter, 11 fail.
- From the `lab08-starter` folder: `python layers.py` prints the gain table, `python layers.py render fight.wav` renders the demo, and `python -m unittest test_layers -v` runs the tests. Rendering 32 seconds takes a few seconds in pure Python.

## Steps

### Part A: the model (30 minutes)

1. Run the tests and note which fail.
2. Implement `stem_gain`. Check your printed table against the lecture's table in section 2.
3. By hand, compute the gains and level at `x = 0.55`. Then check with the code.
4. Implement `level_db`. It returns `-inf` when every gain is 0.
5. Explain in two sentences why `level_db` squares the gains before adding them, and when that assumption would be wrong.

### Part B: smoothing and rendering (40 minutes)

6. Implement `smooth`. It must never overshoot the target in either direction.
7. Run `python layers.py render fight.wav` and listen with headphones. Write down the times (to 0.5 s) when you first hear the drums, the bass and the lead, and when each disappears.
8. Compute those times from the model: `demo_intensity` plus `up_rate = 0.5` and `down_rate = 0.1`. Compare with what you heard. Explain any difference of more than 1 s (hint: a stem at gain 0.1 is −20 dB and may be masked by the others).
9. Change `render` to call `stem_gain` with `equal_power` applied to the ramp (`equal_power(stem_gain(...))`). Render again as `fight_ep.wav`. Describe the difference in how the entries sound.

### Part C: retune for a new encounter (40 minutes)

10. Write a new function `ambush_intensity(t)` for this encounter: 6 s of calm exploring (0.05), a sudden ambush that jumps to 0.9 for 5 s, a lull at 0.5 for 6 s while the player hides, a second wave at 1.0 for 5 s, then 0 until 34 s.
11. Choose new thresholds, fade width and rates so that all of these hold, and verify each with a short script that steps `smooth` at `dt = 0.01`:
    - the drums are at full gain within 0.5 s of the ambush;
    - the lead is silent within 2 s of the lull starting, and the drums stay at full gain through the whole lull;
    - after the second wave ends, the drums stay audible (gain above 0.1) for at least 5 s.
12. Render `ambush.wav` with your settings and listen. Note one thing the numbers did not predict.

### Part D: at home

13. Write a half-page design note: your final thresholds, width and rates, the three checks from step 11 with the computed times, and one paragraph on whether the +6 dB growth at full intensity helps or hurts this encounter. If you would compensate, say by how many dB.
14. Optional, for students with FMOD Studio installed: rebuild the four-stem mixer in FMOD Studio with a 0 to 1 parameter, volume automation curves and a seek modulator, using stems exported from `render` (edit `STEMS` to solo one stem at a time). Report how the seek speed setting maps to your `up_rate`.

## Deliverable

A zip with your `layers.py` (all 12 tests passing, `ambush_intensity` included), the three WAV files (`fight.wav`, `fight_ep.wav`, `ambush.wav`), and a PDF with the answers to steps 3, 5, 7, 8, 9 and 12 plus the design note from step 13.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Code and tests (25%) | All 12 tests pass; `smooth` never overshoots; `ambush_intensity` matches the brief | All tests pass, minor style issues | Some tests fail | Most tests fail |
| Listening versus model (25%) | Heard and computed times tabled side by side; differences over 1 s explained with masking or fade shape | Table complete, explanations thin | Only heard or only computed times | Missing |
| Retuning (30%) | All three step-11 checks met and shown by script output; the settings are musically sensible when rendered | Checks met, script output missing for one | One check failed | Missing |
| Design note (20%) | Loudness decision argued with a dB figure and tied to the encounter | Decision stated, reasoning generic | Note present, no numbers | Missing |
