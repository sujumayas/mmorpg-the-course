# CS203 · Lab 09: A goal-oriented action planner

**Week:** 9 ([Goal-oriented action planning](../lectures/w09-goap.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; trade characters with a neighbor in Part B

## Objective

Turn week 4's A* into a planner that searches world states instead of tiles, reproduce the lecture's eight-world table, Orkin's pizza example and the door replan, and then use the planner as a designer would: build a second character from a different action set, and protect your costs with a regression table so that one careless number cannot quietly change what every soldier does.

## Starter materials

- Python 3.10 or later, no packages. In this repository, `.venv/bin/python`.
- [`labs/lab09-starter/goap.py`](lab09-starter/goap.py). It provides the soldier's `ACTIONS` and `GOAL`, the door's `DOOR_ACTIONS`, `key()` (a state's identity is its set of true facts), `world()` for building the eight starting worlds, and `execute()`, which plans, runs the plan, learns a fact when an action fails, and replans. You write `satisfied`, `apply`, `unmet` and `plan`. Running `python goap.py` prints the eight-world table once `plan` works.
- [`labs/lab09-starter/test_goap.py`](lab09-starter/test_goap.py). Run `python test_goap.py` from inside the starter folder. It prints PASS, FAIL or TODO for eight tests and exits with status 1 until all pass. On the untouched starter all eight report TODO.
- The interactive [`examples/w09-goap-planner.html`](../examples/w09-goap-planner.html) for checking plans and expansion counts by eye.

## Steps

### Part A: the planner (55 minutes)

1. Write `satisfied(state, facts)` and `apply(state, effects)`. A fact missing from `state` counts as false. `apply` must return a new dictionary and leave `state` alone; the test checks this.
2. Write `unmet(state, goal)`, the heuristic.
3. Write `plan(start, goal, actions)`. Start from the lecture's code block and follow the docstring exactly: order the heap by `(f, tiebreak)`, close a state when you pop it, count one expansion for every closed state that is not the goal, and return `(cost, steps, expanded)`. Run the tests until `test_lecture_open_world` and `test_all_eight_worlds` pass, then the rest.
4. Run `python goap.py` and copy the table into your report. Next to each row, write one sentence that a designer would understand ("no cover, so it fires in the open").

### Part B: a second character and a regression table (50 minutes)

5. Build a `GRENADIER` action list for the same goal, `enemy_dead`. Keep GoToCover, Reload and FetchAmmo, drop Melee and Charge, and add at least two actions of your own that use a new fact `has_grenade` (for example ThrowGrenade, and PickUpGrenade from a crate). Choose costs so that a grenadier with a grenade and cover throws from cover, and one without a grenade still has a plan in every one of the eight starting worlds with `has_grenade` added as false.
6. Write `regression.py`. It imports your planner, runs both the soldier and the grenadier over every starting world (8 for the soldier, 16 for the grenadier), and compares each plan to a table you have saved and checked by hand. It prints `OK` or lists every world whose plan or cost changed.
7. Now play the careless designer. Change one cost in the soldier's list by 1 in either direction. Run `regression.py`. Record which worlds changed and whether each change is one you would accept. Find the smallest single cost change that makes the soldier stop using cover in the loaded, ammo, cover world.
8. Trade grenadiers with a neighbor. Find a starting world where their grenadier's plan would look stupid to a player, and write down the world, the plan and the costs that caused it.

### Part C: the design note (at home)

9. Using `execute()` and `DOOR_ACTIONS`, run the door with both failures, then change DiveThroughWindow's cost from 5 to 2 and run it again with no failures. Write a note of at most 300 words to a level designer. Explain what the soldier now does at every door with a window beside it, why, and propose one fix in the action data (not in the planner) that restores door use while keeping the window as a fallback. Use your regression table's approach to say how you would catch this kind of change before it ships.

## Deliverable

Your completed `goap.py` with `test_goap.py` passing (paste its output), your `GRENADIER` list and `regression.py`, plus a PDF with the annotated eight-world table, the regression output from step 7 with your judgments, your neighbor's stupid-plan finding, and the design note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Planner (30%) | All eight tests pass; code mirrors week 4's A* with clear names; expansion counts match the lecture | All pass, code hard to follow | Plans correct but expansion counts or the no-plan case wrong | Tests mostly fail |
| Second character (20%) | Grenadier meets both requirements in step 5; costs explained as behavior | Meets one requirement | Runs but has worlds with no plan | Missing |
| Regression table (20%) | Covers all 24 worlds; step 7 changes listed and judged; smallest cover-breaking change found and explained | Table works, judgments thin | Covers only some worlds | Missing |
| Peer finding (10%) | Concrete world, plan and the costs responsible | World and plan, no cause | Vague | Missing |
| Design note (20%) | Explains the window behavior from costs, proposes a data fix, and ties it to regression testing | Correct explanation, fix vague | Describes the behavior only | Missing |
