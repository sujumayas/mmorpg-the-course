# MMO302 · Lab 05: Tick budget profiler

**Week:** 5 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Measure what one tick of a small world server costs on your own machine, fit the [week 5 lecture](../lectures/w05-tick-rate-for-mmos-vs-shooters.md)'s model `c = a + d·n + e·n·k` to your measurements, and use it to choose a tick rate, a multi-rate schedule and an overrun policy for a crowded zone. You finish with a tick-rate recommendation backed by numbers from your own hardware.

## Starter materials

Folder [`lab05-starter/`](lab05-starter/README.md). Standard library Python only.

- `tick_profiler.py`: stubs for `tick_cost`, `utilization`, `t_max`, `timer_length`, `same_tick_probability`, `multirate_cpu_per_second`, `fit_costs` (least squares without numpy) and `schedule` (the stretch and skip overrun policies). Provided: a toy `World` with grid AOI whose `tick()` does real per-entity and per-neighbour work, a `measure` helper, and a command line.
- `test_tick_profiler.py`: the lecture's numbers, an exact-recovery test for the fit, and the overrun test (102 ms ticks at 10 Hz drift 20 ms in 10 ticks under stretch and skip 3 of 200 ticks under skip).

## Steps

1. **The model.** Implement the five small functions. Run `python tick_profiler.py --lecture` and check both of the lecture's tables and the 244 ms multi-rate figure.
2. **The fit.** Implement `fit_costs` by building the 3×3 normal equations and solving them by Gaussian elimination. The test gives it noiseless data and expects the exact constants back.
3. **The schedule.** Implement `schedule` for both policies. Run the tests until they print `all lab 05 tests passed`.
4. **Measure.** Run `python tick_profiler.py --measure m.csv`. It times the toy world at 12 combinations of `n` and crowd size, and records the average `k`. Close other programs first and run it twice; report how much the two runs differ.
5. **Fit your machine.** Run `python tick_profiler.py --fit m.csv`. Report `a`, `d` and `e`. Your `a` may come out small or even negative. Explain why, by reading `World.tick()`: the per-neighbour loop scans every entity in the 3×3 cells, not only those within the radius, so the work is proportional to the candidates, not to `k`. Add a column for candidates per entity to `measure`, refit with it in place of `k`, and compare the fit error (sum of squared residuals) of the two models.
6. **Choose a rate.** With your better fit, compute `T_max` at `u_max = 0.6` for the lecture's zone (`n = 3,000`, `k = 50`) and for the siege (800 entities at `k = 400`). Then pick one of the in-class games (A, B or C) and choose its tick rate, checking the wait, timer and same-tick columns against the game's fastest decision.
7. **Multi-rate and overrun.** For your chosen game, design a multi-rate schedule for one system and compute its saving. Generate a list of tick costs for a 60-second event where the crowd grows from 0 to its peak and back (you choose the curve), run it through `schedule` with both policies, and plot the lateness of each tick. State which policy you would ship and what players would see.

## Deliverable

Your finished `tick_profiler.py` with passing tests, both measurement CSVs, the fitted constants for both models with their residuals, and a recommendation of at most 600 words with the tick rate, multi-rate schedule and overrun policy for your chosen game, including the lateness plot.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | All tests pass; fit written from the normal equations | Tests pass, fit copied from a library or hard-coded | Tests fail | 25% |
| Measurement and fit | Two runs compared; both models fitted; negative or small `a` explained from the code; residuals compared | One model fitted, explanation missing | No measurement | 25% |
| Tick-rate choice | `T_max` for zone and siege; choice checked against the game's fastest decision in all three feel columns | Choice made with only utilization | Missing | 20% |
| Multi-rate and overrun | Saving computed; lateness plot for both policies; shipped policy defended with what players see | One policy only | Missing | 20% |
| Writing | Numbers traced to code; plain, short, no filler | Some numbers unexplained | Hard to follow | 10% |
