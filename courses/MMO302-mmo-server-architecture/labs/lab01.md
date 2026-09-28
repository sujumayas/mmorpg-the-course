# MMO302 · Lab 01: The crowd cost model

**Week:** 1 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 1 lecture](../lectures/w01-scale-targets-ccu-messages-and-n-squared.md)'s model into code, reproduce its table exactly, and then replace the lecture's invented cost per delivery with one you measured. You finish with a capacity plan that states how large a crowd your design can host and what happens when it grows past that.

## Starter materials

Folder [`lab01-starter/`](lab01-starter/README.md). Standard library Python only.

- `crowd_cost.py`: stubs for `deliveries`, `layout`, `per_server`, `c_max` and `tick_ms`, plus a provided table printer, CSV sweep, timing probe (`--measure`) and tick search (`--break-tick`).
- `test_crowd_cost.py`: the lecture's numbers as tests.

## Steps

1. **The formula.** Implement `deliveries(groups, u)` as `u × Σ g(g − 1)`. Check by hand that 400 zones of 25 players at `u = 5` give 1,200,000.
2. **The world.** Implement `layout` and `per_server` following their docstrings (zone `i` on server `i mod 20`, remainder players to the lowest-numbered zones). Run `python test_crowd_cost.py` until it passes, then `python crowd_cost.py --table`. Paste the output. It must match the lecture's table row for row.
3. **The ceiling.** Implement `c_max(budget, u)` so it returns the exact largest integer, not the square-root estimate. Explain in two sentences why a loop or a correction step is needed after the closed form.
4. **The tick.** Implement `tick_ms`. Run `--break-tick` and confirm that 327 fits a 100 ms tick and 328 does not. Change the tick rate to 20 Hz (edit the default or add a flag) and find the new breaking crowd. Explain why halving the tick length does not halve the crowd.
5. **Measure.** Run `--measure`. It times the cheapest possible delivery, packing 16 bytes and appending them to a buffer. Your number will be far below the lecture's 1 µs. Extend `measure` so each delivery also does one piece of per-client work a real server does, for example an `hmac.new(key, msg, 'sha256').digest()` per recipient to stand in for per-connection encryption or authentication. Report both numbers and the budget `B = 1 / cost` each implies.
6. **Replan.** Using your measured `B` from step 5, recompute `c_max` for `u = 5` and `u = 1`, and rerun `--break-tick` with `per_delivery` set to your measured cost in ms. Run `--sweep sweep.csv` and plot server 0's tick time against crowd size, with a horizontal line at 100 ms. Mark the breaking crowd.
7. **Capacity plan.** Pick one of the three in-class design cards. In half a page, state its PCU, your target utilization and servers needed (section 3 of the lecture), its densest planned moment and its `g`, whether that fits one core with your measured `B`, and which lever you would pull if it does not. Name what players will notice.

## Deliverable

Your finished `crowd_cost.py`, the output of steps 2 and 4, the two measurements from step 5, the plot from step 6, and the capacity plan from step 7, in one Markdown or PDF file plus the code. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | All tests pass; `c_max` exact; code follows the docstrings | Tests pass with one function hard-coded or inexact | Tests fail | 25% |
| Tick analysis | 327/328 reproduced; 20 Hz result correct and explained with the square law | Result correct, explanation vague | Missing or wrong | 20% |
| Measurement | Both costs reported; the realistic one justified; `B` derived from each | One measurement only, or `B` not derived | No measurement | 20% |
| Plot | Tick time against crowd with the 100 ms line and the breaking crowd marked; axes labelled | Plot present but unmarked | No plot | 10% |
| Capacity plan | Every number traced to the model; densest moment and lever named; player-facing cost stated | Numbers present, lever or player cost missing | Opinion without numbers | 25% |
