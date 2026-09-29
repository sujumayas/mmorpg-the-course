# GD202 · Lab 03: Branch explosion analyzer

**Week:** 3, branching structures and the combinatorial explosion ([lecture](../lectures/w03-branching-structures-and-the-combinatorial-explosion.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** dialogue exercises (40% of the course, shared across the exercise labs). The analyzer is reused to check the word budget of the final quest chain (60%).

## Objective

Turn the week 3 model into a tool. First, code the closed-form counts for the fold-back structure. Then write a graph analyzer that reports nodes, endings, distinct paths and the average length of a playthrough for any branching dialogue, including graphs that no formula describes. Finally, use it to bring a branching quest plan of your own under a word budget.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python, run with the program's `.venv/bin/python`.

- [`branching.py`](lab03-starter/branching.py), with a finished `build_structure(b, d, k)` that generates the lecture's fold-back graph, a JSON loader, a `report` function, and five empty functions: `formula`, `reachable`, `endings`, `count_paths` and `mean_path_nodes`.
- [`ferry.json`](lab03-starter/ferry.json), a 17-node sample dialogue graph (a night ferry crossing) that mixes an early three-way choice, a fold at the deck, a dead end and a late branch. No formula fits it, which is the point.
- [`test_branching.py`](lab03-starter/test_branching.py), tests built from the lecture's tables: the five fold values for `b = 3, d = 5`; 88,573 nodes and 59,049 endings for the depth-10 tree; agreement between your formula and the generated graph for every `k` of three `(b, d)` pairs; a 20-choice branch-and-bottleneck graph with `3^20` paths that must finish in well under a second; and the ferry graph's 4 endings, 20 paths and average playthrough of 7.2 nodes. The tests fail on the starter and pass once your functions are correct.
- The [calculator](../examples/w03-branch-explosion.html), for spot checks.

Run the tests from inside the starter folder:

```
cd courses/GD202-narrative-and-quest-design/labs/lab03-starter
../../../../.venv/bin/python test_branching.py
```

## Steps

1. **Formula (20 min).** Implement `formula(b, d, k)` from the lecture's segment formulas without building a graph. `test_formula_matches_lecture` and `test_formula_depth_table` should pass.
2. **Reachability and endings (15 min).** Implement `reachable` (any search from CS102 week 8 works) and `endings`. Unreachable nodes must be ignored.
3. **Count paths (25 min).** Implement `count_paths`. Enumerating paths one at a time will pass the small tests and time out on the `3^20` graph. Use the rule "paths from a node = sum of paths from its children, and 1 at an ending," and store each node's answer so it is computed once.
4. **Average playthrough (20 min).** Implement `mean_path_nodes`. Hint: for each node keep two numbers, the paths below it and the total nodes across those paths. Check your answer on the ferry graph by hand for the `sneak` branch.
5. **Run the sample.** Run `branching.py` with no arguments. Write down nodes, endings, paths, the mean playthrough and the share seen. In two sentences, explain which structure from Ashwell's catalog the ferry graph most resembles.
6. **Your quest plan (at home).** Write a JSON graph for a branching quest of your own: at least 4 choices on the main path and at least 12 nodes. Label nodes with short scene names.
7. **Budget it (at home).** Give each node a word estimate. Set a budget of 5,000 words. If the plan is over budget, restructure it (fold earlier, cut a branch, move a branch later) and rerun until it fits. Keep every version.
8. **Explain the trade (at home).** Compare your first and final versions: nodes, paths, share seen, and the one thing a player can no longer experience in the final version.

## Deliverable

- Your completed `branching.py` with all six tests passing.
- The ferry report with your two-sentence classification.
- Your quest graphs (first and final JSON) and a report of at most 600 words: the budget table for each version, the restructuring moves you made, and the trade-off paragraph from step 8.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All six tests pass, including the `3^20` graph | Five pass; the big graph times out | Fewer than five pass | 30% |
| Code quality | Memoized, readable, no hard-coded test values | Works but duplicated or hard to follow | Hard-coded or unreadable | 10% |
| Ferry analysis | Numbers correct; classification names the pattern and cites structure evidence | Numbers correct, classification vague | Numbers wrong | 15% |
| Quest plan and budget | Plan meets the size rules; final version fits 5,000 words; every version measured | Fits budget but versions not compared | Over budget or not measured | 25% |
| Trade-off reasoning | Names what a player loses in concrete terms and why it was the right cut | Lists changes without judging them | Missing | 20% |
