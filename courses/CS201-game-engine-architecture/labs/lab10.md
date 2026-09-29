# CS201 · Lab 10: A script host

**Week:** 10 ([Scripting layer integration](../lectures/w10-scripting-layer-integration.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare your step 7 fit with a neighbor at the end

## Objective

Build the engine side of a scripting layer and measure it. You will write the four parts the lecture argued for: a binding wrapper that checks every handle, a marshalling rule that refuses anything unsafe, a batched API whose crossing count you can predict, and a budgeted coroutine scheduler that survives a crashing script. Then you will time your own host, fit `c_cross` and `c_work` from the measurements, and decide whether batching is worth it on this boundary. The host is written in Python so you can finish it in one session. Every rule carries over to a C++ engine embedding Lua, which is what your final engine will do.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`lab10-starter/script_host.py`](lab10-starter/script_host.py). It contains week 5's generational `HandleTable` (finished), a finished `Engine` (positions and velocities per handle), a finished `Host` whose `call()` counts crossings and marshals every argument and result, the per-object script `move_one()`, and a timing helper `measure()`. You write `bound()`, `marshal()`, `move_batched()`, `predict_frame_us()` and `run_frame()`. Each has a docstring that is the specification.
- [`lab10-starter/test_script_host.py`](lab10-starter/test_script_host.py). Run `python test_script_host.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w10-boundary-crossings.html`](../examples/w10-boundary-crossings.html), for predicting before you measure.

## Steps

### Part A: the host (70 minutes)

1. Write `bound(table, fn)`, the lecture's section 3 wrapper. The returned function looks up its first argument in the handle table, returns `None` without calling `fn` if the handle is stale or malformed, and otherwise calls `fn(obj, *args)`. Exceptions from `fn` must pass through, because `run_frame` handles them in step 5. Checks 1a and 1b cover both. Write one sentence on what a quest script would do wrong if `bound` called `fn` on whatever object now sits in the slot.
2. Write `marshal()`. Allowed values are `None`, `bool`, `int`, `float`, `str`, handles (a tuple of exactly two ints) and lists of allowed values, copied recursively. Everything else raises `BoundaryError`. Check 2 tries dicts, sets, other tuples and plain objects.
3. Write `move_batched()`. For each chunk of `batch` handles, make one `get_velocities` call and one `add_to_positions` call. Check 3 compares your result with `move_one()` on five sizes, including a destroyed entity and a batch larger than the list, and counts crossings. It expects exactly `2 × ceil(N / B)`.
4. Write `predict_frame_us()` from the lecture's model. Check 4 uses the lecture's table.
5. Write `run_frame()`. It is the lecture's scheduler plus one rule. A script that raises an exception is removed and logged, and the frame continues. Checks 5a and 5b test the lecture's trace and a script that divides by zero.

### Part B: measure your boundary (35 minutes)

6. Run `python script_host.py` to time 20,000 movers per-object and in one batch. Then write a short loop that times `move_batched()` at `B` = 1, 10, 100, 1,000 and 20,000 (best of 3 runs each) and records the host's `crossings`.
7. Fit the lecture's model to your five points. Total time is linear in the crossing count `X`, so fit `T = X × c_cross + N × c_work` with a straight line of `T` against `X` (a least-squares fit or two well-separated points both work). Report `c_cross` and `c_work` in microseconds and your `B* = c_cross / c_work`.
8. Explain your `B*`. In this host `marshal()` copies every value that crosses, so per-entity marshalling lands in `c_work`, not `c_cross`. Is batching worth much here? Now add a per-crossing check to `Host.call()` that costs something real (for example, verify every handle argument against the handle table, or append the call name to a log list), re-measure, and refit. How does `B*` move?

### Part C: the design note (at home)

9. Your team's MMO client has 400 nameplates and 60 buff icons scripted in Lua. A profile shows each crossing costs 1.8 µs and each nameplate's work costs 0.6 µs. Using your `predict_frame_us()`, compare per-object `OnUpdate` at 144 fps, one batched call per frame, and one batched call at 20 Hz. Report milliseconds per second for each.
10. Write a note of at most 300 words to the UI lead. Recommend a call style for nameplates and for buff icons, give the numbers, name the handle rule that stops a nameplate script from touching a despawned mob, and name one function you would *not* bind for addon authors and why.

## Deliverable

Your completed `script_host.py`, with `test_script_host.py` passing (paste its output). Also a PDF with the step 1 sentence, the step 6 table, the step 7 fit (plot of `T` against `X` with the fitted line), the step 8 before-and-after `B*` with your explanation, the step 9 numbers, and the design note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct host (35%) | All seven checks pass; code follows the docstrings with clear names; step 1 sentence names a concrete wrong-object bug | All checks pass, sentence vague | Wrapper and marshal work, batching or scheduler fails | Host missing or broken |
| Measurement and fit (30%) | Five timed points, fitted line drawn, `c_cross`, `c_work` and `B*` reported with units; step 8 re-measure shows how the added check moves `B*` and explains why | Fit present, step 8 explanation thin | Timings present, no fit | Missing |
| Model use (15%) | Step 9 numbers correct for all three styles, per second, with working shown | One style wrong | Numbers without working | Missing |
| Design note (20%) | Clear recommendation per object kind, numbers quoted, handle rule and an unbound function each justified by a named threat | Recommendation and numbers, weak justification | Recommendation only | Missing |
