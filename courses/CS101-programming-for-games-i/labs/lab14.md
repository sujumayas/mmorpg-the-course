# CS101 · Lab 14: Headless juice

**Week:** 14, polish pass ([lecture](../lectures/w14-polish-pass-sound-particles-screen-shake.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the weekly exercises (40%). The shake camera, emitter settings and polish table go into your final arcade game release (week 15).

## Objective

Fix the logic of a trauma-based screen shake and a particle emitter in plain Python until they behave the same at 30, 60 and 144 frames per second, then port both to your Godot game with a shake-scale setting. You test feel with numbers first, so that the Godot version is only a translation.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard-library Python 3.10 or later, no packages.

- [`juice.py`](lab14-starter/juice.py). A `Trauma` class with two bugs marked TODO (no upper clamp, and decay per frame instead of per second), a working `value_noise` and `shake_offset`, and an `Emitter` class with two TODOs (no accumulator, no removal of dead particles). `python juice.py` prints a shake timeline for one 0.5 hit and a particle count after 5 seconds.
- [`test_lab14.py`](lab14-starter/test_lab14.py). Eight tests, including frame-rate checks at 30, 60 and 144 Hz. Run `python test_lab14.py`. On the starter it reports `2/8 tests passed`.

## Steps

1. **Read the failing output.** Run `python juice.py` and `python test_lab14.py`. The particle line says 300 alive where the model says 90. Write one sentence per failing test on what you think is wrong before you change any code.
2. **Clamp.** Fix `Trauma.add` so trauma never exceeds 1.
3. **Decay in seconds.** Fix `Trauma.update` to use `dt` and clamp at 0. Check that `test_decay_is_frame_rate_independent` passes, and record how long a 0.5 hit shakes at each frame rate before and after your fix.
4. **Check the table.** Run `python juice.py` and compare the trauma and shake columns with the table in lecture section 2. They must match to three decimals.
5. **Accumulator.** Fix `Emitter.update` to emit `rate × dt` particles per frame, carrying the fraction in `self.to_emit`.
6. **Removal.** Remove particles whose age reaches the lifetime by building a new list. Run the tests until you see `8/8 tests passed`, and check that `python juice.py` now prints 90 alive.
7. **Port to Godot.** Put the lecture's `Camera2D` script in your game. Add a "Shake" slider (0% to 100%) to your options menu that sets `user_scale`, and a HUD on a `CanvasLayer`. Replace any existing shake code. For particles, set each `GPUParticles2D` node's `amount` from your budget, using `alive = rate × lifetime`.
8. **Polish table.** Fill the section 5 table from the lecture for your game: five frequent events and one rare event, each with a trauma amount, a burst size and lifetime, and a sound with a pitch range in semitones. Store it as a dictionary in one script, and have every event handler read from it.
9. **Zero test.** Set shake, particles and effects volume to 0 and play one full run. Nothing in the rules may change. Then measure particle count and frame time in your busiest wave with Godot's debugger Monitors tab.

## Deliverable

- Your edited `juice.py`, with `python test_lab14.py` reporting `8/8 tests passed`.
- A note of at most 300 words with: the before and after durations from step 3, your polish table from step 8, and the measured particle count against your predicted budget from step 9.
- A 20-second screen recording of your game showing one frequent event and the rare event, once at 100% shake and once at 0%.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 8/8 | 6-7 | 5 or fewer | 25% |
| Frame-rate reasoning (steps 1 and 3) | Predictions written before fixing; durations at 30/60/144 Hz recorded and explained with `d × dt` | Durations recorded, explanation thin | Missing | 15% |
| Polish table and budget | Frequent events small, rare event largest; budget computed with `rate × lifetime` and within 20% of the measured count | Table complete, budget not checked | Table missing or effects all the same size | 25% |
| Godot port | Shake through one offset line with a working scale setting, still HUD, particles sized from the budget | Works but UI shakes or scale missing | Not ported | 25% |
| Zero test | Recording shows identical gameplay with effects at 0 | Mentioned, not shown | Missing | 10% |
