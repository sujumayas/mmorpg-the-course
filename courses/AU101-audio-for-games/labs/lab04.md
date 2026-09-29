# AU101 · Lab 04: The variation engine

**Week:** 4, layering and variation ([lecture](../lectures/w04-layering-and-variation.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home for Part 2.
**Weight:** formative, feeds the SFX pack (30%). The layered sound from Part 2 becomes the first entry in that pack.

## Objective

Turn the repeat-chance model from lecture section 2 into working code, hear the machine-gun effect you just measured, then design one layered sound of your own with a variation plan you can defend with numbers.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python 3.10 or later, no packages. Any audio player that opens WAV files.

- [`variation.py`](lab04-starter/variation.py) has three parts. Part A holds four empty model functions (`semitones_to_ratio`, `db_to_gain`, `repeat_chance`, `burst_repeat_probability`). Part B holds a `NoRepeatPicker` class and `plan_burst`, which decides the variant, pitch and gain of every shot in a burst. Part C is provided. It synthesizes three layers of four variants each (transient, body, tail) from seeded noise and sine sweeps, pitch-shifts by resampling, and mixes a burst into a 16-bit WAV.
- [`test_lab04.py`](lab04-starter/test_lab04.py) has seven tests. Run it with `python test_lab04.py`. On the starter it reports `0/7 tests passed`.

## Steps

### Part 1: the engine (in lab)

1. **Model functions.** Fill in Part A. Each docstring states the formula. Run the tests after each function. `test_repeat_chance` includes Doom's 32 uniform offsets, Heretic's triangular 15, and the weighted footstep from the lecture's check-yourself question.
2. **No-repeat picker.** Implement `NoRepeatPicker.pick`. Draw with `rng.randrange(self.n)` and reroll while the result equals the last pick, but only when `no_repeat` is on and `n >= 2`. Do not call `random` directly; all randomness must come from the `rng` argument so tests can reproduce it.
3. **Burst planner.** Implement `plan_burst`. Follow the draw order in the docstring exactly (every layer's variant, then pitch with `rng.uniform`, then gain with `rng.uniform`), or the reproducibility test fails.
4. **Listen.** Run `python variation.py`. It writes `same_x10.wav` (one body variant, no pitch, no volume change) and `layered.wav` (3 layers × 4, ±1 semitone, 0 to −2 dB, no-repeat on). Both play 10 shots at Doom's chaingun rate, 8.75 per second. Listen on headphones and write two sentences on what you hear in each.
5. **Measure.** Write a short script (or use the Python prompt) that calls `plan_burst([4, 4, 4], 10, 0, 0, rng, no_repeat=False)` 2,000 times with one seeded `rng`, counts exact neighbouring repeats, and prints the average per burst. Compare with the model's `9 × R`. Repeat with `no_repeat=True`. Paste both numbers in your notes.
6. **Break it on purpose.** Change the pitch range in `main()` to ±5 semitones and render again. Then change the body layer so all four variants use the same `f0` (edit `make_layers`). Describe what each change does to the sound's identity in one sentence each.

### Part 2: your layered sound (at home)

7. **Design.** Pick one frequent game action (footstep on one surface, sword hit, spell cast, pickaxe strike). Plan three layers with a clear job each (transient, body, tail) and 3 or 4 variants per layer. You may record, synthesize (week 3 tools) or combine. No copyrighted samples; libraries are allowed only under a licence that permits redistribution in coursework (CC0 or CC-BY with credit).
8. **Plan the numbers.** Fill in the variation table below and compute `R` and `P(at least one repeat)` for a realistic burst length (for example, 8 footsteps or a 5-hit combo). Use half-semitone groups for pitch.
9. **Render.** Load your layers into `make_layers` (read your WAVs with the `wave` module, or replace the synthesis) and render a burst with your settings.

| Layer | Job | Variants | Pick rule | Pitch range | Volume range |
|---|---|---|---|---|---|
| Transient | | | | | |
| Body | | | | | |
| Tail | | | | | |

## Deliverable

1. Your edited `variation.py` with `python test_lab04.py` reporting `7/7 tests passed`.
2. `same_x10.wav`, `layered.wav`, and `my_sound_burst.wav` from Part 2, plus the individual layer files.
3. A note of at most 400 words with: the two listening sentences from step 4, the measured versus predicted numbers from step 5, the two sentences from step 6, and the completed variation table from step 8 with your `R` calculation shown.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 7/7 | 5-6 | 4 or fewer | 25% |
| Measurement (step 5) | Measured averages within 0.05 of `9R` for both settings, and the no-repeat result explained with the model | Numbers present, explanation thin | Missing or wrong by a wide margin | 15% |
| Layer design | Each layer has one clear job in time and frequency; layers sum without phase problems; the sound reads as the chosen action | Layers work but two overlap in job or band | One layer does everything, or layers cancel | 25% |
| Variation plan | Table complete, `R` computed correctly for the chosen burst, ranges justified by the sound's role (signal or texture) | Table complete, justification thin | Table missing or `R` wrong | 20% |
| Listening notes | Specific (names what repeats, where identity breaks) | General impressions | Missing | 15% |
