# CS101 · Lab 07: A scene tree you can test

**Week:** 7, engine intro ([lecture](../lectures/w07-engine-intro-scenes-nodes-scripts.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%).

## Objective

Build a small Python model of how Godot calls your scripts, prove it with tests, then check it against the real engine. By the end you can predict any tree's `_ready` and `_process` order, and compute the follower gap an ordering bug produces before you run the game.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Standard-library Python 3.10 or later, no packages.

- [`scene_tree.py`](lab07-starter/scene_tree.py). Part A gives you a `Node` class (name, children, `priority`, `x`), a `Mover` that moves right at a set speed, and a `Follower` that copies its target's `x` every frame. Part B has six empty functions with docstrings: `pre_order`, `post_order`, `process_order`, `run_frames`, `lag_frames`, `predicted_gap`. Part C prints the lecture's two experiments once Part B works.
- [`test_lab07.py`](lab07-starter/test_lab07.py) has ten tests built from the lecture's tables and check-yourself answers. Run `python test_lab07.py` from inside the folder. On the starter it reports `0/10 tests passed`.
- Godot 4.x (standard build) for step 6.

## Steps

1. **Traversals.** Write `pre_order` and `post_order` as recursive functions that return lists. Test with the lecture's section 4 tree and the check-yourself tree. Before running the tests, write the expected orders on paper.
2. **Priority.** Write `process_order`. It sorts the pre-order list by `priority`, lower first. Python's `sorted` is *stable*, which means nodes with equal keys keep their existing order, exactly Godot's tie rule. Explain in one sentence why a non-stable sort would be a bug here.
3. **Frame runner.** Write `run_frames`. Run Part C. You should see a 5.0 px gap when the bar is listed first and 0.0 when the enemy is first.
4. **Predicting lag.** Write `lag_frames` and `predicted_gap`. `lag_frames` walks the chain from a follower to the thing it ultimately copies and counts the links where the copier runs first. Make `test_measured_matches_predicted` pass. It checks the formula against the simulation for a two-link chain at 450 px/s and 90 fps.
5. **Gap table.** Using your functions, print the gap for 1 and 2 frames of lag at 30, 60, 90 and 144 fps for speeds of 40, 300 and 1,200 px/s. Paste the table into your notes and mark every cell above 3 px (roughly where players start to notice a bar sliding).
6. **Check the engine.** In Godot, build the section 4 tree with a script on every node that prints `name` in `_enter_tree`, `_ready` and the first `_process` call (use a `var done := false` flag). Run once. Compare the three printed orders with your Python output. Then give `HealthBar` a `process_priority` of 10 and confirm your `process_order` still matches.
7. **Fix it three ways.** Using the in-class scene (enemy at 1,200 px/s with a bar above it), apply each fix from the lecture: reorder, `process_priority`, parenting. For each, record the gap you measured and one way a teammate could break the fix later.

## Deliverable

Your edited `scene_tree.py` with `python test_lab07.py` reporting `10/10 tests passed`, and a note of at most 300 words containing: the step 2 sentence, the step 5 table with marked cells, a screenshot or pasted log from step 6, and the three fixes from step 7 with their measured gaps and weaknesses.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 10/10 | 7-9 | 6 or fewer | 30% |
| Traversal code | Recursive, short, no special cases for depth; `process_order` uses a stable sort | Works but duplicates logic or hard-codes depth | Does not generalise to new trees | 15% |
| Gap table | All 24 cells correct and the 3 px cells marked | Minor arithmetic errors | Missing or formula misapplied | 15% |
| Engine comparison | Godot log matches Python for all three callbacks, including the priority case, with evidence | Matches for two callbacks | No engine evidence | 20% |
| Three fixes | Each measured and each weakness is specific (who breaks it and how) | Measured, weaknesses generic | Fewer than three fixes | 20% |
