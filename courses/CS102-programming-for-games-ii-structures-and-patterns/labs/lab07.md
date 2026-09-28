# CS102 · Lab 07: Scene graph and skill tree

**Week:** 7 ([lecture](../lectures/w07-trees-scene-graphs-and-skill-trees.md)) · **Time:** 2 hours in lab plus about 2 hours at home · **Work mode:** individual, pair discussion allowed · **Weight:** one of the weekly labs (labs are 40% of the course in total)

## Objective

Write the core tree operations twice, once for a 2D scene graph and once for a skill tree, and see that they are the same operations with a different payload. Then break the one-parent rule on purpose and extend the skill tree into a DAG, the structure Diablo II's cold skills actually use.

## Starter materials

- [`lab07-starter.py`](lab07-starter.py): Python 3.10+, standard library only. Run it from the repository root with `.venv/bin/python courses/CS102-programming-for-games-ii-structures-and-patterns/labs/lab07-starter.py`. It contains:
  - A `Node` class with local `x`, `y` and `angle`, and `add_child`. The method `world()` is a TODO.
  - Stubs for `preorder`, `postorder` and `subtree_size`.
  - A `Skill` class with `cost`, `learned` and one `parent`, and stubs for `can_learn`, `path_cost` and `refund`.
  - Three tests using the tank from the lecture (turret at local `(10, 0)`, barrel `(30, 0)`, muzzle `(20, 0)`, two tracks at `(0, ±12)`) and a five-skill frost tree. On the untouched starter every test reports `TODO`.
- The lecture's tables are the reference values. The tests check the muzzle at `(160, 100)`, `(153.3, 125.0)`, `(100, 160)` and `(75.0, 153.3)` for the four tank and turret angles in the table.
- The interactive `examples/w07-scene-graph-transforms.html`, when it is built, for spot checks.

## Steps

### Part A: scene graph (45 min)

1. **World transform.** Implement `Node.world()` from the lecture's model. The parent's world angle rotates this node's offset. This node's own angle is added to the result but does not move this node. Run the file until `test_world` passes.
2. **Walks.** Implement `preorder` and `postorder` recursively, and `subtree_size`. Run until `test_walks` passes.
3. **One pass.** Add a function `update_all(root)` that stores `wx`, `wy`, `wa` on every node in a single pre-order pass, as in section 3 of the lecture. Count how many times `math.cos` is called for the tank tree using `update_all`, and how many times calling `world()` on every node calls it. Record both numbers.
4. **The detached barrel.** Write a short script that copies every node's world position into a plain dict, then changes the turret angle to 30° and updates *only* the turret's stored entry. Print the distance between the stored barrel position and the true one from `world()`. This is the "direct storage" bug from the interactive, in numbers.

### Part B: skill tree (35 min)

5. **Prerequisites and cost.** Implement `can_learn` and `path_cost`. Check by hand that `path_cost` gives 4 for Shatter and 5 for Deep Freeze.
6. **Refund.** Implement `refund` as a post-order walk that unlearns the subtree and returns the points. Run until `test_skills` passes.
7. **Refund policy.** Add a parameter `rate` (default 1.0) so a refund returns `floor(cost × rate)` per skill. Compute, by program, what refunding the whole learned frost tree returns at `rate = 0.5`, rounding per skill, and compare it with rounding the total once. Write one sentence on which a player would prefer and which a designer should choose.

### Part C: from tree to DAG (40 min)

8. **Several parents.** Make a copy of `Skill` called `DagSkill` with a list `parents` instead of one `parent`. Rewrite `can_learn` (all parents learned) and `path_cost` (the cost of the *set* of all ancestors plus this skill, each counted once).
9. **Diablo II's cold skills.** Build Ice Bolt → Ice Blast → Glacial Spike → Blizzard → Frozen Orb, plus Frost Nova → Blizzard, each with cost 1. Show that `path_cost(Frozen Orb)` is 6. Now add an invented skill, Ice Storm (cost 1), that requires both Blizzard and Glacial Spike. Your set-based `path_cost(Ice Storm)` should be 6. A naive version that adds up `path_cost` of each parent gives `1 + 5 + 3 = 9`. Explain which skills it counted twice and why the Frozen Orb case did not expose the bug.
10. **Refund in a DAG.** When a player unlearns Frost Nova, which skills must also go? Implement `dag_refund` and test it on step 9's graph.

## Deliverable

- Your completed `lab07-starter.py` (renamed `lab07-<yourname>.py`) with all three tests passing and your Part A step 3-4 and Part C code below the tests.
- A text file of up to 300 words with: the two `math.cos` counts from step 3, the detached-barrel distance from step 4, the refund comparison from step 7, and a 200-word note on the DAG extension (why `path_cost` needs a set, and what `dag_refund` removes).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Scene graph (steps 1-2) | `test_world` and `test_walks` pass; code follows the lecture's model directly | Tests pass with workarounds or hard-coded cases | Tests fail | 25% |
| Cost and bug evidence (steps 3-4) | Both `cos` counts correct and explained; barrel distance computed and linked to the interactive | Numbers present, explanation thin | Missing | 15% |
| Skill tree (steps 5-7) | `test_skills` passes; refund policy compared with numbers and a clear recommendation | Tests pass, policy comparison missing numbers | Tests fail | 25% |
| DAG extension (steps 8-10) | Correct `path_cost` of 6 for both skills, the naive 9 explained; `dag_refund` removes exactly the dependent skills | Works on the example but double counts or misses a case | Missing | 25% |
| Code quality | Readable names, no duplicated walk logic, runs first time | Runs with minor fixes | Does not run | 10% |
