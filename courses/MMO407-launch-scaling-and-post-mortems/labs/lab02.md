# MMO407 · Lab 02: Launch queue planner

**Week:** 2 ([lecture](../lectures/w02-capacity-planning-and-login-queues.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** the launch plan (50% of the course grade). The capacity memo is the capacity section of your final launch plan.

## Objective

Build a launch-queue simulator for a fresh launch, check it against the lecture's hour-3 numbers, measure how much the session-ending assumption moves the answer, and choose a capacity plan (worlds, layers, head start) that meets a launch-night wait target and a day-30 population target.

## Starter materials

- [`lab02-starter/launch_queue.py`](lab02-starter/launch_queue.py), Python 3, standard library only. It provides the lecture's demand schedule, `demand_at`, `queue_at`, `peak` and `wait_at_back`, and three stubs:
  - `simulate` (TODO 1), the minute-by-minute fresh-launch model with three session models: `"full"`, `"first"` and `"fixed"`.
  - `alive_on_day30` (TODO 2).
  - `smallest_worlds` (TODO 3), the fewest worlds that meet a wait target at a given hour.
- [`lab02-starter/test_launch_queue.py`](lab02-starter/test_launch_queue.py) has six tests. All fail on the starter and pass on a correct solution. Run them from inside `lab02-starter/` with `python -m unittest test_launch_queue.py`.
- `python launch_queue.py` prints the lecture's 10, 15 and 20-world lines once TODO 1 is done.
- The interactive `examples/w02-launch-queue-hour-three.html`, once it is built.

## Steps

### Part A: the model (45 min)

1. Implement `simulate` (TODO 1) with all three session models. Run the tests. `test_ten_worlds` must reproduce the lecture's table: 2,700 at hour 1, 4,500 at hour 3, peak at minute 180, empty at minute 630.
2. Write a function that returns the cumulative curves `A(t)` and `D(t)` for one world alongside the queue, and check that `A(t) − D(t)` equals the queue at every minute. Plot both curves for 10 worlds and mark hour 3.
3. For 10 worlds, find the minute at which the per-world arrival rate first falls below the admission rate. Confirm it is the minute of the peak, then change the schedule so the shoulder lasts until minute 240 and confirm the peak moves with it.

### Part B: how sure are you? (35 min)

4. Run all three session models for 10 and 15 worlds and report the queue at hour 3 and the peak for each. Present the six numbers as a range per world count.
5. Sweep the entry rate from 50 to 500 per minute for 10 worlds and plot the hour-3 queue. Write two sentences on when entry speed matters and when it does not.
6. Sweep `session_min` from 90 to 240 in steps of 30 for 10 worlds. Which parameter moves the hour-3 queue more per 10% change, `session_min` or the entry rate? Show the numbers.

### Part C: the capacity plan (40 min)

7. Implement `alive_on_day30` and `smallest_worlds` (TODOs 2 and 3) and run all tests.
8. Plan this launch. Arrivals across the game are 2,000 per minute for the first 45 minutes, 500 per minute until minute 240, then 180 per minute. Worlds have `C = 5,000`, entry rate 120 per minute and a launch-night session of 180 minutes. The day-30 peak forecast is 36,000 and a world needs 3,000 at peak. The target is a back-of-queue wait of at most 45 minutes at every hour from 1 to 6.
   - Find the smallest fixed world count that meets the wait target, and check it against day 30.
   - Design a layered plan (a layer factor applies to both `C` and the entry rate for launch week) that meets both targets with fewer permanent worlds. Report the layer factor and the number of worlds.
   - Model a 48-hour head start for 20% of players by removing 20% of the first 45 minutes of arrivals. How much does it change your plan?
9. Rerun your chosen plan under the `"fixed"` session model. Does it still meet the target? If not, what would you add?

## Deliverable

- `launch_queue.py` passing all six tests, plus your code for steps 2 to 9.
- Plots from steps 2, 5 and 6.
- A one-page capacity memo for the step 8 launch. State the plan (worlds, layers, head start, when each layer closes), the expected queue and wait at hours 1 to 6 as a range across session models, the day-30 population per world, and the one assumption that would most change your plan if it were wrong.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Simulator (steps 1 to 3) | Tests for the lecture launch pass; cumulative curves correct; peak explained as the λ = μ crossing | Tests pass; curves or explanation incomplete | Tests fail | 25 |
| Sensitivity (steps 4 to 6) | Ranges reported for both world counts; entry-rate and session-length effects compared with numbers | Numbers reported without comparison | Missing | 20 |
| Planning functions (step 7) | All tests pass | Minor numeric drift | Tests fail | 10 |
| Capacity plan (steps 8 and 9) | Fixed, layered and head-start plans all computed; plan meets both targets or explains why it cannot; fixed-session check done | Plan meets targets under one model only, or head start missing | Missing | 30 |
| Memo | Every number traced to a run; ranges, not single values; the key assumption named | Clear but partly unsupported | Missing | 10 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
