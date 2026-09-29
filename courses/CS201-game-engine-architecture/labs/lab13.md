# CS201 · Lab 13: A frame profiler

**Week:** 13 ([lecture](../lectures/w13-profiling-cpu-gpu-frame-budgets.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish Part C at home.
**Work mode:** pairs for Parts A and B; Part C in your own final-project engine.
**Counts toward:** subsystem labs (50% of the course grade). Part C's profiler and budget report are reused in the final engine demo.

## Objective

Build the analysis half of an instrumenting profiler and check it against the lecture's numbers: self time from nested scopes, overhead correction, how long a sampling capture must run, the bottleneck, percentiles, and export to a trace viewer. Then put a real scoped timer into your C++ engine, measure its own cost per scope, and write a budget report for your demo scene that a teammate could act on.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Python 3.10 or later, standard library only (in this repository, `.venv/bin/python`).

- [`frameprof.py`](lab13-starter/frameprof.py). Provided: `FakeClock`, a `Profiler` with a `scope()` context manager that records `(name, tid, depth, start_us, end_us)`, `simulated_frame()` (the lecture's frame on a main thread and a render thread, with nested child scopes), and `capture()` (120 frames of per-thread totals from a level that streams a chunk every 40 frames). You write six functions marked `TODO 1` to `TODO 6`; each docstring states exactly what the checks expect. Run `python frameprof.py` to print a short report; parts you have not written show a dash.
- [`test_frameprof.py`](lab13-starter/test_frameprof.py). Run `python test_frameprof.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w13-two-profilers.html`](../examples/w13-two-profilers.html), to predict results before you compute them.
- For Part C: your engine from earlier labs, the `ScopedTimer` from lecture section 3, and your `shown_ms` and `bottleneck` functions from [lab 04](lab04.md).

## Steps

### Part A: the analysis functions (60 min)

1. Write `self_times(events)` (TODO 1). A scope's self time is its inclusive time minus the inclusive time of its direct children on the same thread. Sum over repeated names. Both step 1 checks must pass. In your notes, explain in one sentence why the check only subtracts children on the same `tid`.
2. Write `correct_overhead(measured_ns, calls, overhead_ns)` (TODO 2) from `measured = true + n × o`, never returning a negative time. The step 2 check includes a function whose measured time is less than its call count times the overhead. Write down what that tells you about the value of `o` someone used.
3. Write `frames_needed(t_ns, rate_hz, error_pct)` (TODO 3) with integer arithmetic only. You need `k = 1 / e²` samples in the function, and each frame gives `rate × t` of them. The step 3 check includes the lecture's `vec_normalize` (32 frames for ±10% at 8 kHz) and check-yourself question 3 (134 frames). If you get 51 instead of 50 on one case, you used floats; rewrite the ceiling as integer division.
4. Write `bottleneck(threads)` (TODO 4), week 4's `max` over threads and GPU, returning the name and the time.
5. Write `percentile(values, p)` (TODO 5) using the nearest-rank rule from lecture section 5. The check includes p98 and p99 of the lecture's 120-frame capture; one lands on a normal frame and one on a hitch. Say which and why.
6. Write `to_trace(events)` (TODO 6), producing Chrome JSON `B` and `E` events. The step 6 check replays your events and fails if any `E` does not close the innermost open scope on its thread. Read the docstring's tie-breaking rules before you start: a parent and its first child begin at the same microsecond.

### Part B: look at it (20 min)

7. Run `python frameprof.py`. It writes `frame_trace.json`. Open [ui.perfetto.dev](https://ui.perfetto.dev), choose "Open trace file", and load it. Take a screenshot showing both threads with the nested scopes expanded. Check by eye that `physics` has a 0.6 ms gap before `broadphase` starts.
8. From the printed report, record the median and p99 game-thread time of the capture, and the worst frame. Using week 4's model at 60 Hz with vsync, how many refreshes does the worst frame occupy? How many hitches per second does the level have, and what subsystem from lecture section 5 would you suspect first?

### Part C: your engine (at home)

9. Add a `ScopedTimer` to your C++ engine that appends `(name, thread id, depth, start, end)` to a per-thread buffer instead of printing. Put scopes around each subsystem in your frame (about 10 to 30 scopes, not per entity). Write the buffer once per frame and flush it to a Chrome JSON trace file on a key press.
10. Measure your own `o`. Time a loop of 1,000,000 empty scopes, subtract the time of the same loop without scopes, and divide. Report `o` in nanoseconds for a debug and an optimized build.
11. Capture 600 frames of your demo scene's scripted camera path. Report median and p99 for the whole frame and for each thread, plus the GPU if your renderer has timestamp queries (if it does not, say so and report the frame time from `present` to `present` instead). Use your lab 04 `shown_ms` to report what the player sees at 60 Hz.
12. Instrument one function that runs at least 1,000 times per frame, measure it, then remove the scope and measure its caller. Using your `o` from step 10 and `correct_overhead`, check whether the difference matches `n × o` to within 20%.

## Deliverable

- Your completed `frameprof.py` with `test_frameprof.py` output pasted into a `README.md` (all seven checks passing).
- In the README: the notes from steps 1, 2 and 5; the Perfetto screenshot and the answers to step 8.
- From Part C: the engine code diff for the timer and trace export, your measured `o` in both builds, one exported trace file, and a one-page budget report. The report states the target frame rate, a per-subsystem budget that keeps at least 10% of the frame in reserve, the measured median and p99 per subsystem, the bottleneck, and the step 12 overhead check.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Analysis functions (30%) | All seven checks pass; integer arithmetic where required; the step 1, 2 and 5 notes are correct and short | All checks pass, notes vague or missing one | Four to six checks pass | Three or fewer |
| Trace and reading (15%) | Perfetto screenshot shows both threads nested; step 8 answers computed from the model with the refresh count and a named suspect | Screenshot and answers present, one step unexplained | Screenshot only | Missing |
| Engine instrumentation (25%) | Per-thread buffer, no printing in the frame, trace opens in Perfetto; `o` measured in both builds with method shown | Works, `o` measured in one build | Timer prints per scope, or trace does not open | Missing |
| Budget report (30%) | Median and p99 per subsystem and thread, bottleneck named, reserve of at least 10%, what the player sees at 60 Hz, overhead check within 20% or the gap explained | Numbers present, one element missing | Averages only, no percentiles | Missing |
