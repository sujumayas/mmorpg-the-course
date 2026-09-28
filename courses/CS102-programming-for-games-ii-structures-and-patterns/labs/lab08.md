# CS102 · Lab 08: Dialogue linter

**Week:** 8 ([lecture](../lectures/w08-graphs-maps-and-dialogue.md)) · **Time:** 2 hours in lab plus about 2 hours at home · **Work mode:** individual, pair discussion allowed · **Weight:** one of the weekly labs (labs are 40% of the course in total)

## Objective

Build the tool a narrative team runs on every commit: load a dialogue file as a directed graph, search it with breadth-first search, and report unreachable lines, dead ends and broken links. Then point it at a conversation you wrote and judge where static checking stops being trustworthy.

## Starter materials

- [`lab08-starter.py`](lab08-starter.py): Python 3.10+, standard library only. Run it from the repository root with `.venv/bin/python courses/CS102-programming-for-games-ii-structures-and-patterns/labs/lab08-starter.py`, or add a path to lint another file. It contains:
  - `load(path)` and a `report(data)` function that prints the lint results once your functions work.
  - Stubs for `build_graph`, `bfs`, `unreachable`, `dead_ends`, `broken_links`, `path_to` and the stretch `cannot_finish`.
  - Two tests against the sample file. On the untouched starter both report `TODO`.
- [`lab08-dialogue.json`](lab08-dialogue.json): an invented 12-line blacksmith conversation with one typo in a choice target and a few planted problems. The format is documented at the top of the starter.
- The lecture's BFS trace tables, for checking your queue by hand.
- The interactive `examples/w08-bfs-reachability.html`, when it is built, for spot checks on the lecture's smaller blacksmith graph.

## Steps

### Part A: build and search (40 min)

1. **Adjacency list.** Implement `build_graph`: a dict from every node id to the list of its choices' targets, in file order, keeping targets that do not exist.
2. **Trace first.** Before you write `bfs`, trace it by hand on the sample file from `greet`. Keep the queue in a column. Write down `dist` for every node you reach.
3. **BFS.** Implement `bfs` with `collections.deque`, returning `dist` and `prev`. Skip targets that are not nodes. Compare its output with your hand trace. If they differ, find which of you is wrong, and write down why.
4. **Paths.** Implement `path_to`. Run until `test_graph_and_bfs` passes.

### Part B: lint (35 min)

5. **Three checks.** Implement `unreachable`, `dead_ends` and `broken_links`. Run until `test_lint` passes and the report prints.
6. **Read the report as a writer.** The sample has a single typo in one choice target. Explain in two sentences why that one typo shows up in *two* lint categories.
7. **Fix the data, not the linter.** Make a copy of the JSON, fix every problem the report found (link the unreachable lines from sensible places, give the dead end a way out), and run the linter on your copy until the report is clean.

### Part C: your own dialogue (45 min)

8. **Write one.** Write a conversation of 20 to 30 lines for an invented quest giver in the same JSON format. Include at least one loop back to an earlier line and at least two endings.
9. **Lint it.** Run the linter. Fix what it finds, keeping a list of each problem and its fix.
10. **Where it lies.** Add a `"requires"` field to two choices (for example `"requires": "has_key"`). The linter ignores it. Describe one line your linter now calls reachable that no player without the key can see (a false negative), and one way a scripted jump in code could make it report a false positive. Propose, in 100 words, how you would extend the linter to handle one flag.
11. **Stretch.** Implement `cannot_finish`: reachable lines from which no ending is reachable. Reverse every edge and run one BFS from all endings at once. On the sample file it should report `rumor_detail`.

## Deliverable

- Your completed starter (renamed `lab08-<yourname>.py`) with both tests passing.
- Your fixed copy of the sample JSON and your own dialogue JSON.
- A text file of up to 400 words with: your hand trace from step 2 (queue column and `dist`), the step 6 explanation, the list of problems found in your own dialogue with fixes, and the step 10 analysis.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Graph and BFS (steps 1-4) | Tests pass; BFS uses a deque, marks nodes when first seen, skips broken targets | Tests pass with a list queue or nodes marked when dequeued | Tests fail | 25% |
| Hand trace | Queue shown after every dequeue, `dist` matches the program, any disagreement explained | Trace present with small slips | Missing | 15% |
| Lint checks and fixed data (steps 5-7) | All three checks correct; typo explained; fixed file lints clean | Checks correct, fixed file still has one issue | Checks wrong | 20% |
| Own dialogue (steps 8-9) | 20-30 lines with a loop and two endings; problems and fixes listed | Meets size but no loop or no list of fixes | Missing | 20% |
| Limits of static checking (step 10) | Concrete false negative and false positive, a workable one-flag extension | Examples given without a proposed extension | Missing | 15% |
| Stretch (step 11) | `cannot_finish` correct using reversed edges and a multi-source BFS | Works by running BFS from every node | Not attempted (no penalty beyond this row) | 5% |
