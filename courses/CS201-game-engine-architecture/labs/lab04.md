# CS201 · Lab 04: Frame pacer

**Week:** 4 ([lecture](../lectures/w04-the-frame-update-render-present.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). The functions you write here become the budget and pacing readout in your engine's profiler overlay in week 13.

## Objective

Implement the lecture's two models in C++. The budget model turns a frame's stage times into CPU time, GPU time, the work interval `W` and the bottleneck. The queue model's three rules turn a sequence of work intervals into start, ready and shown times for a queue depth `Q` and swap interval `S`. Check both against the lecture's tables. Then replay a recorded 600-frame stage log, find what causes its long frames, and choose settings for two different games.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). C++20 and the standard library only. Any recent Clang, GCC or MSVC works.

- `frame.hpp`: the `Stages`, `Frame` and `Summary` structs, `refresh_ms`, and nine stubs. Part A is `TODO A1` to `A3` (budget), Part B is `TODO B1` to `B6` (queue). Each comment states what the checks expect.
- `test_frame.cpp`: eleven checks built from the lecture's tables and traces. Build and run with `c++ -std=c++20 -O2 test_frame.cpp -o test_frame && ./test_frame`. Every check prints `FAIL` on the starter, and the program exits with 0 only when all eleven pass.
- `analyze.cpp`: reads a stage log, reports the bottleneck of every frame over budget, then replays the frames for `Q` from 1 to 3 and `S` of 1 and 2. It prints empty results until `frame.hpp` is complete.
- `frame_log.csv`: 600 frames (about 10 seconds at 60 Hz) with columns `frame,input,gameplay,physics,animation,render_prep,gpu` in milliseconds.

## Steps

### Part A: the budget (30 min)

1. Implement `cpu_ms`, `work_ms` and `bottleneck` (TODO A1 to A3). Checks A1 to A3 must pass. They use the lecture's city, raid and raid-with-effects frames.
2. Write one sentence in your README on why `bottleneck` returns "gpu" only when `G > C`, and one on what it should mean for a serial frame, where both processors add up.

### Part B: the queue (45 min)

3. Before writing code, trace `W = 25` ms, 60 Hz, `Q = 2`, `S = 1` for frames 0 to 4 by hand, as in the lecture's trace table. Put the table in your README.
4. Implement `next_vblank` (TODO B1). Check B1 must pass. It feeds exact multiples of `1000.0 / 60.0`. If it fails, reread the lecture's note on the `1e-9` tolerance.
5. Implement `simulate` (TODO B2). Checks B2, B2b and B2c must pass. Print your step 3 trace with it and correct your hand trace if they differ. Say in one sentence where you went wrong, if you did.
6. Implement `on_screen_ms`, `latency_ms`, `long_frames` and `summarize` (TODO B3 to B6). Checks B3 to B6 must pass.
7. Write a short `sweep.cpp` that runs 121 frames of constant `W` from 4 ms to 40 ms in steps of 2 ms at 60 Hz with `Q = 2`, `S = 1`, and prints `W`, fps, long frames and max latency. Paste the table into your README. Latency is 33.33 ms for every `W` up to 16 ms and then changes with `W`. Explain in two sentences what sets the latency below 16.67 ms and what sets it above, and why long frames appear only in the second range.

### Part C: the recorded log (35 min)

8. Build and run `analyze.cpp`. Copy the output into your README.
9. Plot `W` (pipelined) for the 600 frames with any tool and mark the two kinds of trouble in the log. Describe each in one sentence with its frame numbers, its size and the stage responsible.
10. Explain, using the three rules, why `Q = 1, S = 1` has by far the most long frames and why `Q = 2` has so few. Refer to one specific frame range in each explanation.
11. Your studio is making two games on this engine: a fast action game where players parry attacks, and a slow city builder. Choose `Q` and `S` for each from the six rows. Defend each choice in at most 80 words using the numbers.

### Part D: a better option (10 min)

12. Propose one change to the engine or the content (not to `Q` or `S`) that would let the action game use `Q = 1, S = 1` with fewer than 20 long frames on this log. Edit a copy of the log to reflect your change, rerun `analyze`, and show that it works.

## Deliverable

A zip of your `lab04-starter/` folder containing:

- `frame.hpp` with all eleven checks passing, `sweep.cpp`, your edited log copy from step 12, and the unchanged `test_frame.cpp`, `analyze.cpp` and `frame_log.csv`.
- `README.md` (at most two pages): build commands, the answers to step 2, the hand trace, the sweep table and explanation, the `analyze` output, the plot, and the answers to steps 9 to 12.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Budget (checks A1 to A3, step 2) | All pass; both sentences correct | Pass, sentences vague | Two or more fail | 15 |
| Queue rules (checks B1 to B2c) | All pass; code follows the three rules directly with no special cases for 60 Hz | Pass, but with hard-coded 16.67 or special cases | Two or more fail | 20 |
| Measurement (checks B3 to B6) | All pass | One fails | Two or more fail | 10 |
| Hand trace and sweep (steps 3 and 7) | Correct trace; sweep correct; `Q × T` below 16.67 ms and `W` plus the vblank wait above it | One error, or explanation vague | Missing | 20 |
| Log diagnosis (steps 9 and 10) | Both problems found with frame ranges and stage; both explanations use the rules and name frames | One of the two | Neither | 20 |
| Choices and change (steps 11 and 12) | Two defended choices with numbers; change demonstrated with a rerun | Choices without numbers, or change not demonstrated | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

A reference solution's `analyze` output (60 Hz, 600 frames, pipelined): over budget with bottleneck gpu 78 frames and physics 13 frames. Then:

| Q | S | fps | long frames | max latency | mean latency |
|---|---|---|---|---|---|
| 1 | 1 | 52.1 | 91 | 33.33 | 19.19 |
| 2 | 1 | 59.1 | 9 | 38.38 | 32.31 |
| 3 | 1 | 59.2 | 8 | 50.00 | 46.56 |
| 1 | 2 | 30.0 | 0 | 33.33 | 33.31 |
| 2 | 2 | 30.0 | 0 | 66.67 | 66.52 |
| 3 | 2 | 30.0 | 0 | 100.00 | 99.64 |

The log has two problems. Every 45th frame (44, 89, ..., 584) physics jumps from 2.5 to 12.5 ms, five fixed steps after a stall, and `C` reaches about 22 ms. Frames 380 to 459 are a boss fight where the GPU runs 17.9 to 19.1 ms, just over `T`. Two hitch frames (404 and 449) fall inside the boss fight and count under physics, which is why the GPU count is 78 and not 80. With `Q = 1` every boss-fight frame starts on a vblank, finishes after the next one, and waits for the one after, so all 80 show for 33.33 ms. With `Q = 2` the engine free-runs, a frame drifts past a vblank only about `(18.5 − 16.67) / 16.67 ≈ 11%` of the time, and the queued frame absorbs most hitches. The cost is latency: the mean rises from 19 to 32 ms.

Good step 11 answers: the action game takes `Q = 1` or `2` with `S = 1` and argues latency against smoothness with the 19 versus 32 ms means; the city builder takes `Q = 2` or `3` with `S = 1`, or `S = 2` for perfectly even frames at 30 fps. Step 12: bringing the boss-fight GPU time under 16.67 ms (fewer particles, lower-resolution effects) removes about 78 long frames at `Q = 1`; capping fixed steps per frame or spreading the streaming work removes the rest.

Sweep answers (`Q = 2`, `S = 1`): for `W` from 4 to 16 ms, 60 fps, 0 long frames and latency exactly 33.33 ms, which is `Q × T`, because the engine fills the queue and waits. From 18 ms up the engine is slower than the display, the queue never fills, and latency is `W` plus the wait for the next vblank (34.00 at 18 ms, 40.00 at 24 ms, 53.33 at 40 ms). Long frames appear only there: 9 at 18 ms, 53 at 24 ms, and all 120 from 34 ms.

</details>
