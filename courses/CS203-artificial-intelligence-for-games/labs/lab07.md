# CS203 · Lab 07: A behavior tree you can trace

**Week:** 7 ([Behavior trees](../lectures/w07-behavior-trees.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare traces with a neighbor at the end

## Objective

Write the two composites that every behavior tree rests on, make one tree run under three tick rules (reactive, memory, hybrid), and reproduce the lecture's trace table and visit counts exactly. Then extend the guard with a new behavior and prove with a trace that you placed it correctly. By the end you should be able to predict, before running anything, which tick a tree will react on and how many nodes it will visit.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab07-starter/bt.py`](lab07-starter/bt.py). It provides `Condition`, `Action` (with a tick counter and `halt()`), the `Composite` base class with `finish()` (which aborts the previously running child and records the running index), a global visit counter, the lecture's `guard(mode)` tree, its 12-tick `TIMELINE`, and `run()`, which ticks a tree and returns `(action, visits)` per tick. You write `Selector.tick`, `Sequence.tick` and `Inverter.tick`.
- [`labs/lab07-starter/test_bt.py`](lab07-starter/test_bt.py). Run `python test_bt.py` from inside the starter folder. It prints PASS, FAIL or TODO for nine tests and exits with status 1 until all pass. On the untouched starter all nine report TODO.
- The interactive [`examples/w07-bt-tick-trace.html`](../examples/w07-bt-tick-trace.html) for checking your traces by eye.

## Steps

### Part A: the composites (60 minutes)

1. Write `Selector.tick`. Call `visit()` once, then tick children in order and return the first status that is not FAILURE, always through `self.finish(i, status)`. In memory mode only, start at `self.running` when it is set. Run the tests. `test_selector_returns_first_non_failure` should pass.
2. Write `Sequence.tick`, the mirror image: return the first status that is not SUCCESS. Reactive mode starts at child 0. Memory mode skips every child before `self.running`. Hybrid mode also skips them, except `Condition` children, which it ticks again. Get the three `test_lecture_trace_*` tests and `test_lecture_visit_counts` passing.
3. Write `Inverter.tick`. Swap SUCCESS and FAILURE, pass RUNNING through, and count one visit.
4. Run `python bt.py`. Copy its output into your report. Mark by hand, on the printout, the stutter tick of the reactive guard, the two late ticks of the memory guard and the three ticks on which the memory guard should have fled.

### Part B: extend the guard (40 minutes)

5. The designer asks: "When the guard first sees the player, it shouts for help, once, then fights. It must not shout again for 10 seconds." Add a `Cooldown(child, ticks)` decorator to `bt.py`. It returns FAILURE without ticking its child if the child last *succeeded* fewer than `ticks` ticks ago, and otherwise ticks the child. You will need a tick clock. Pass the current tick in the blackboard as `bb["t"]` by editing `run()`.
6. Add `Action("CallForHelp", 1)` to the tree wherever you think it belongs, wrapped in your cooldown at 5 Hz. Write a 20-tick timeline in which the player is seen twice, at ticks 3 to 6 and again at ticks 12 to 16. Show with a trace under the hybrid rule that the guard calls for help at tick 3 only, and fights on every other "sees" tick.
7. Write two sentences on why you put the new branch where you did, and what a player would see if you had put it one level higher or lower.

### Part C: the designer note (at home)

8. A designer on your team says the memory rule is "the fast one" and wants it for all 300 guards in a town. Write a note of at most 300 words. Use your Part A output to give the visit saving as a percentage, name the two visible bugs it causes with the tick numbers, and propose a cheaper fix that keeps reactive priorities (behavior tags, events, or ticking far-away guards less often). Say what your fix costs.

## Deliverable

Your completed `bt.py` with `test_bt.py` passing (paste its output), plus a PDF with the Part A trace printout and markings, the Part B tree diagram and 20-tick trace, the two sentences from step 7, and the designer note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Composites (35%) | All nine tests pass; code follows the lecture's structure, uses `finish()` for every return, no special cases for the guard | All pass, code hard to follow | Selector and sequence work in one or two modes only | Tests mostly fail |
| Trace reading (15%) | Stutter, late reaction and missed flee all marked on the right ticks, each with a one-line cause | Marked, causes vague | One or two of the three found | Missing |
| Cooldown and extension (25%) | Cooldown correct; the 20-tick trace shows exactly one call for help; placement argued with a concrete alternative | Works, weak argument | Calls for help more than once or blocks fighting | Missing |
| Designer note (25%) | Saving as a percentage, both bugs with tick numbers, a concrete cheaper fix with its cost | Numbers present, fix vague | No numbers | Missing |
