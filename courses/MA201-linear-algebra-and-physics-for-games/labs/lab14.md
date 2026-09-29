# MA201 · Lab 14: Precision budget and a determinism harness

**Week:** 14, determinism and floating point ([lecture](../lectures/w14-determinism-and-floating-point.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Weight:** part of the problem sets (40%). The precision budget goes into your physics sandbox design document.

## Objective

Turn the lecture's two warnings into tools you can run on any project. First, a precision calculator that tells you where movement and clocks break for a given speed, tick rate and representation. Second, a per-tick state hash that finds the exact tick where two builds of the same simulation stop agreeing. You finish with a one-page precision budget for your own sandbox world.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Python 3.13 or later (the arena uses `math.fma`), standard library only.

- [`precision.py`](lab14-starter/precision.py). Given: `f32`, which rounds a double to the nearest float32, the lecture's section 5 arena as `arena_run(ticks, fused)` returning every tick's state, and a command-line runner. You write `gap32`, `walk_speed` (float32, double and integer millimetres), `freeze_distance`, `float_clock`, `state_hash` and `first_divergence`. As shipped they return 0 or `None`, so the file runs and prints a table of zeros.
- [`test_lab14.py`](lab14-starter/test_lab14.py): nine tests. Run `python test_lab14.py` from inside the folder. On the starter it reports `0/9 tests passed`.
- The week 14 interactive, [`examples/w14-far-from-origin.html`](../examples/w14-far-from-origin.html), for checking walker speeds by eye.

## Steps

### Part A: the precision calculator (40 min)

1. **Predict.** Before coding, compute by hand `gap32` at 5,000 m and at 200,000 m, and the float32 walking speed at 200 km for 1.4 m/s at 60 Hz. The lecture's section 2 shows the method.
2. **Implement** `gap32`, `walk_speed`, `freeze_distance` and `float_clock`. In `walk_speed`, round the step to float32 once with `f32(v * dt)` and round after every addition with `f32(x + step)`. For `"mm"`, keep integers throughout.
3. **Run** `python precision.py`. The walker table must match the lecture's to every digit shown, and the freeze distance must read 524,288 m. Then run `python precision.py --speed 0.5 --hz 30` and check it against the lecture's Check this example, question 1.

### Part B: find the desync (40 min)

4. **Implement** `state_hash` (pack the tuple as little-endian doubles and take `zlib.crc32`) and `first_divergence`. Explain in one sentence why the test that hashes `0.0` and `-0.0` must give different results, and why that is what a lockstep checksum wants.
5. Run all tests. `test_arena_fma_diverges_at_first_bounce` expects the first differing tick to be 191, the first pillar bounce.
6. **Map the divergence.** Write a short script that lists every run of consecutive ticks where the two builds differ over 60 s (7,200 ticks). You should find the difference at tick 191 disappear and a lasting one begin later. Report both ranges, and explain in three sentences how a difference can vanish. Hint: print both states on the tick where they become equal again, and on the tick before.
7. Repeat step 6 hashing positions only (`s[:2]`). Report the first differing tick and how many seconds later it is than the full-state answer. State the rule for what a checksum must include.

### Part C: precision budget for your sandbox (40 min)

8. For the [physics sandbox](../assessments/sandbox-brief.md) you are building (weeks 10 to 15, showcased in week 15), write down its world size, tick rate, slowest mover and its speed, the longest session you expect, and whether any part is replayed or networked.
9. Use your calculator to fill a table with the gap at the world edge, the slowest step per tick, their ratio, the freeze distance, and the float32 clock error after the longest session. Rate each as safe (ratio at least 20), visible (2 to 20) or broken (under 2).
10. Choose a representation for positions and for time, and justify it in at most 200 words. If you choose float32, say where the origin is and whether you will shift it. If anything is replayed, list the determinism rules from lecture section 4 you will follow.

## Deliverable

- The completed `precision.py` passing all nine tests, plus your step 6 script.
- A PDF of at most 3 pages containing the Part A hand predictions, the Part B divergence ranges and explanations, and the Part C budget table and justification.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Implementation (Parts A and B) | All nine tests pass; walker table matches the lecture; hand predictions correct | Seven or eight tests pass | Six or fewer pass | 35 |
| Divergence analysis (Part B) | Both ranges found; vanishing difference explained from the printed states; positions-only delay measured and checksum rule stated | Ranges found, explanation vague | Missing | 30 |
| Precision budget (Part C) | Complete table from the pair's own world; ratings consistent with the numbers; choice justified with a named cost | Table complete, justification generic | Missing | 25 |
| Clarity | Plain writing, units on every number, figures labelled | Minor unit or labelling gaps | Hard to follow | 10 |
| **Total** | | | | **100** |
