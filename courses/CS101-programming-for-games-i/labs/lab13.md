# CS101 · Lab 13: Seeded randomizers and a fair spawner

**Week:** 13, randomness ([lecture](../lectures/w13-randomness-spawning-and-procedural-variety.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). The spawner and the run seed go straight into your final arcade game (week 15).

## Objective

Implement two piece randomizers and a rejection-sampling spawner in plain Python, check them against numbers you computed by hand, then port the seeded bag and the spawner to your Godot game. By the end you can explain, with your own output, why a bag caps droughts and a no-repeat rule does not, and why gameplay needs its own generator.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard-library Python 3.10 or later, no packages.

- [`randomizers.py`](lab13-starter/randomizers.py). `pure_random` is done. `nes_style`, `seven_bag` and `gaps_between` have docstrings that state the rule and a fallback line so the file runs. `report()` prints the table from lecture section 2.
- [`spawner.py`](lab13-starter/spawner.py). An 800 × 600 arena, a 150 px safe radius and a weighted spawn table. `spawn_position` is a stub that ignores the safe radius. `demo()` prints a text map of 40 spawns with `@` for the player and `*` for enemies, plus a count of spawns that landed too close.
- [`test_lab13.py`](lab13-starter/test_lab13.py). Nine tests. Run `python test_lab13.py`. On the starter it reports `2/9 tests passed`.

## Steps

1. **Run everything first.** Run `python randomizers.py`, `python spawner.py` and `python test_lab13.py`. Note that all three randomizer rows are identical (they all fall back to pure random) and that some spawns land within the safe radius.
2. **NES style.** Implement the rule from lecture section 2: roll 0 to 7, reroll 0 to 6 on the dummy value or a repeat, deal the second roll unconditionally. Before running the tests, write down the repeat rate you expect, as a fraction and as a percentage.
3. **7-bag.** Implement the bag with `rng.shuffle`. Use the generator you were given, never the module-level `random` functions.
4. **Droughts.** Implement `gaps_between`. Run `python randomizers.py` and copy the table into your notes. Compare each row with the lecture table (seed 13) and with the hand values `1/7`, `1/28`, `1/49` and `(6/7)^20`.
5. **Break reproducibility on purpose.** In `report()`, make the NES generator share one `random.Random(13)` with the pure generator (create it once, pass it to both). Rerun. Write two sentences on what changed and why. Then undo the change.
6. **Safe spawns.** Implement `spawn_position` with rejection sampling, the squared-distance test and the attempt cap. Run `python spawner.py`; the "too close" count must be 0 and the mean tries close to 1.17. Run the tests until you see `9/9 tests passed`.
7. **Measure the collapse.** Call `spawn_position` 10,000 times with `safe=350` and then `safe=450`, player centered. Record the mean tries and the share of calls that returned `None`. Compare with the table in lecture section 3.
8. **Port to Godot.** In your arcade game, create `var spawn_rng := RandomNumberGenerator.new()` and set its seed at the start of each run from `Time.get_ticks_usec()` or a fixed debug seed. Port `spawn_position` and use the lecture's `shuffle_with` for any bag you need (enemy types per wave work well). Show the seed on the game-over screen. Effects must not use `spawn_rng`.
9. **Replay test.** Play two runs with the same fixed seed, making the same moves for the first 20 seconds. Screenshot the first three spawns of each run.

## Deliverable

- Your edited `randomizers.py` and `spawner.py`, with `python test_lab13.py` reporting `9/9 tests passed`.
- A note of at most 300 words with: the table from step 4 beside your hand values, the two sentences from step 5, the step 7 measurements, and the step 9 screenshots.
- A commit of your Godot project where the run seed shows on the game-over screen.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 9/9 | 7-8 | 6 or fewer | 25% |
| Hand values vs simulation | All four hand values computed and matched to the table, with a sentence on the one that only simulation can give | Values present, comparison thin | Missing or wrong | 20% |
| Reproducibility explanation (step 5) | Names the shared generator, which rows changed, and the link to cosmetic effects moving spawns | Describes the change without the cause | Missing | 15% |
| Spawner measurements (step 7) | Both radii measured, compared with the lecture table, with a proposed sampler for the 450 px case | Measured but not compared | Missing | 15% |
| Godot port | Seeded spawner, separate effects generator, seed on screen, replay screenshots match | Port works but shares a generator or lacks the seed display | Not ported | 25% |
