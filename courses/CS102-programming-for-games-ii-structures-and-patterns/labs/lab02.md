# CS102 · Lab 02: Breaking up the blob

**Week:** 2 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** one of the weekly labs (labs are 40% of the course)

**Lecture:** [Week 02, inheritance vs composition](../lectures/w02-inheritance-vs-composition.md)

## Objective

Refactor a working god class into a `GameObject` that holds components, one feature at a time, without changing behaviour. Then add two entity types the old class could only express by growing new flags, and measure the unused data before and after.

## Starter materials

All in [`lab02/`](lab02/):

- `god_entity.py`: a 120-line `Entity` class with six flag-controlled features (render, collide, move, health, AI, explode) and a small `World` that steps entities and keeps an event log.
- `entities.py`: a factory, `make(kind, x, y)`, that builds seven entity kinds (bush, trigger, crate, rock, grenade, barrel, goblin) from `Entity`. The tests only ever build objects through `make`.
- `test_behaviour.py`: six `unittest` tests that pin down current behaviour, including a grenade fuse, a goblin chase and a two-barrel chain explosion with an exact event log.
- `test_mine.py`: one test that fails on the starter. It builds a `"mine"` with `make` (which raises `ValueError` today), puts a goblin on the same spot, steps once and expects the mine to have exploded and the goblin to be at 0 HP. It passes once you finish step 6.

You need Python 3.11 or later and Git. From the `lab02` folder run `python -m unittest -v`. On the starter code the six behaviour tests pass and `test_mine` errors with `ValueError: unknown kind 'mine'`. The six must stay green after every step below. `test_mine` goes green in step 6 and stays green after that.

## Steps

1. **Commit the baseline (5 min).** `git init`, add the three files, commit. Every later step ends with a green test run and a commit.
2. **Measure the blob (15 min).** List every attribute `Entity.__init__` creates that belongs to one feature (for example `sprite`, `radius`, `vx`, `blast_damage`). For each of the seven kinds in `entities.py`, count how many of those attributes it never uses. Record the total unused count and the total slot count in `NOTES.md`, as in the lecture's god-class row.
3. **Extract Health (20 min).** Create `components.py` with a `Component` base class and a `Health` component that owns `hp`, `max_hp` and `take_damage`. Make `Entity` hold an optional `Health` and forward `hp` and `take_damage` to it. Run the tests. Commit.
4. **Extract the rest (45 min).** Repeat step 3 for `Render`, `Collide`, `Mover`, `AI` and `Explode`, one per commit. Components that need another component (AI steers the `Mover`; `Explode` checks `Health`) must look it up through the owner, not through a flag.
5. **Replace Entity (20 min).** When `Entity` only forwards, write `GameObject(name, x, y, *components)` and change `entities.make` to build from components. Delete the flags. Run the tests. If `test_goblin_chases` fails, check the order your `GameObject` updates components in, and write down the order rule you chose.
6. **Two new kinds (at home).** Add both to `make` and write at least two tests for each:
   - `"mine"`, named `"Mine"`: invisible, collides, and explodes (radius 2, damage 30) on the first step in which any other collidable object overlaps it. The shipped `test_mine.py` checks this case.
   - `"totem"`: renders, has 15 HP, and heals every entity with a `Health` component within radius 3 by 5 HP per whole second of game time, never above that entity's max.
   Each should need exactly one new component class and no edits to existing components, except where you can justify one in `NOTES.md`.
7. **Re-measure (at home).** Recount unused slots for all nine kinds under your component design and under the original `Entity` extended with whatever flags the mine and totem would have needed.

## Deliverable

A repository link or zip with:

- The Git history: at least seven commits, one per extracted feature, each with passing tests. Paste `git log --oneline` into `NOTES.md`.
- `components.py` and the updated `entities.py`. The original `god_entity.py` may be deleted.
- `test_behaviour.py` with the original six tests unchanged and your new tests for the mine and totem, plus `test_mine.py` unchanged, all passing.
- `NOTES.md`, at most 500 words: the before and after unused-slot table from steps 2 and 7; your component update-order rule and why it's needed; one place where a component had to know about another, and how you kept that dependency visible.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Behaviour preserved | All six original tests pass at every commit, unchanged | Pass at the end but some commits were red, or a test was edited with a reason | Original tests fail or were weakened | 25% |
| Refactor quality | No feature flags remain; each component owns its data; `GameObject` knows no specific feature | One flag or a feature-specific branch left in `GameObject` | Still a god class with renamed parts | 25% |
| New kinds | Mine and totem each added as one new component with tests, including an edge case (overlap on the first frame; healing capped at max) | Both work, tests thin or one needs edits to other components | One or both missing | 20% |
| Measurement | Correct before and after unused-slot counts with the method shown | Counts present, method unclear or small errors | Missing | 15% |
| Notes and history | Clear update-order rule, a named inter-component dependency, commit-per-step history | Two of the three | Generic or missing | 15% |
