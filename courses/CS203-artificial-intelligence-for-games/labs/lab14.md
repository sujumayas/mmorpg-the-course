# CS203 · Lab 14: A frame-budget scheduler

**Week:** 14 ([Performance: AI LOD and time-slicing](../lectures/w14-performance-ai-lod-and-time-slicing.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare your step 6 plots with a neighbor at the end

## Objective

Build the scheduler from the lecture. It has a budgeted round robin with a near tier, it handles agents whose thinks cost different amounts, and it can time-slice a long A* search. Then measure it and use the numbers to pick a budget for a scene. By the end you should be able to tell a designer "with this many agents and this budget, the player's nearest enemies react within X ms and the rest within Y ms", and show the formula and the measurement agree. This scheduler is a good base for the final NPC ecosystem demo.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`lab14-starter/scheduler.py`](lab14-starter/scheduler.py). It contains `Agent`, a `fortress()` builder for the lecture's 600 guards, a finished `simulate()` that measures worst frame, average frame and each agent's longest wait, an `all_at_once()` reference policy, three small grid maps and a finished one-frame `astar()` from week 4. You write `staggered()`, `BudgetScheduler.__call__()`, `predicted_wait()` and `sliced_astar()`. Run `python scheduler.py` to print the lecture's comparison table; rows for unwritten parts show a dash.
- [`lab14-starter/test_scheduler.py`](lab14-starter/test_scheduler.py). Run `python test_scheduler.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w14-frame-budget.html`](../examples/w14-frame-budget.html), to predict results before you run them.

## Steps

### Part A: the scheduler (65 minutes)

1. Write `staggered(agents, period)`. It returns a policy function in which agent `a` thinks when `(frame + a.id) % period == 0`. Run the tests until step 1 passes. The step 1 check expects a flat 4,000 µs per frame and a longest wait of 6 frames for the fortress.
2. Write `BudgetScheduler.__call__(frame)`. Follow the docstring exactly. Near agents come first. Far agents are served in round-robin order from a cursor that persists between frames, and the scheduler stops at the first far agent that does not fit, without skipping ahead. The one exception keeps the queue moving: if no far agent has been served this frame, serve the next one anyway. The three step 2 checks test the plain budget (every frame exactly 2,000 µs, wait 12), the order of service on a 10-agent example, and the near tier (near wait 1, far wait 20).
3. Write `predicted_wait(n_near, n_far, cost, budget)` from the lecture's formulas. The step 3 check compares your formula with the simulation on six configurations, including one where the near tier uses the whole budget. Write down what happens in that case and why the "at least 1" rule matters.
4. Run the step 4 check. It gives agents three different think costs plus one agent whose think costs more than the whole budget. If it fails, your scheduler is either skipping ahead (the 3,000 µs agent starves) or letting ordinary frames go over budget. Explain in two sentences why "no skipping ahead" is the rule that prevents starvation.
5. Write `sliced_astar(grid, start, goal, steps_per_frame)`, starting from the provided `astar()` and the lecture's section 3. The step 5 check runs it on three maps with 1, 7 and 50 expansions per frame and expects the same `(cost, expanded)` as `astar()`, on frame `ceil(expanded / steps_per_frame)`. It also tests an unreachable goal.

### Part B: measure (30 minutes)

6. Using `simulate()` and `BudgetScheduler`, sweep the fortress size `N` from 100 to 2,000 in steps of 100 with a 2,000 µs budget, a 40 µs think and a near tier of 20. For each `N`, record the worst frame, the near wait and the far wait. Plot worst frame and far wait against `N` on two axes. On the same plot, draw `predicted_wait()`'s far wait as a line. Then answer:
   - At what `N` does the far wait first exceed 500 ms?
   - What budget would keep the far wait at or under 500 ms for `N = 2,000`? Check it with the simulation.
7. Give every tenth guard a 400 µs think (a guard running a costly perception query) and repeat the `N = 600` measurement. Report the worst frame, how often a frame goes over budget, and the new far wait. Suggest one change to the scheduler that would reduce the over-budget frames, and say what it costs.

### Part C: the budget note (at home)

8. Your team's stealth level has 450 guards, at most 30 on screen at once, and a measured think cost of 55 µs. On-screen guards must react within 50 ms and off-screen guards within 750 ms. Using your formula, find the smallest budget that meets both targets, then confirm it with `simulate()`. Also time-slice a path request on the `maze` map with the smallest `steps_per_frame` that still answers within 3 frames.
9. Write a note of at most 300 words to the lead programmer. State the budget you recommend and the share of a 16.7 ms frame it takes, the near and far waits you measured, what happens to both if the level designer adds 150 guards, and one LOD change from lecture section 4 that would let you lower the budget without the player noticing.

## Deliverable

Your completed `scheduler.py`, with `test_scheduler.py` passing (paste its output). Also a PDF with the answers to steps 3 and 4, the step 6 plot and answers, the step 7 measurements and suggestion, the step 8 calculations and simulation output, and the budget note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct scheduler (30%) | All seven checks pass; code follows the docstring rules with clear names; the starvation and "at least 1" answers are correct and short | All checks pass, explanations vague | Plain budget works, near tier or variable costs fail | Scheduler missing or wrong |
| Time-sliced search (15%) | Step 5 passes; the frame count is explained from `ceil(expanded / steps)`; maze choice in step 8 justified | Passes, no explanation | Returns the right path but wrong frame count | Missing |
| Measurement (25%) | Sweep plotted with formula line; both step 6 answers checked by simulation; step 7 reports over-budget rate and a costed suggestion | Plot and answers present, one not checked | Sweep partial | Missing |
| Budget note (30%) | Recommendation with share of frame, measured waits, the +150 guards case and a concrete LOD change with its visible risk | Numbers present, LOD change vague | Few numbers | Missing |
