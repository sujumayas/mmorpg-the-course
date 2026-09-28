# CS102 · Lab 09: A world with a component index

**Week:** 9 ([lecture](../lectures/w09-pattern-component.md)) · **Time:** 2 hours in lab plus about 2 hours at home · **Work mode:** individual, pair discussion allowed · **Weight:** one of the weekly labs (labs are 40% of the course in total)

## Objective

Build the runtime side of the component pattern: a `World` that keeps a per-component index, queries that return entities in spawn order, systems that run over those queries, and deferred destruction. Then measure polling against indexing on your own machine and decide where the index is not worth it.

## Starter materials

- [`lab09-starter.py`](lab09-starter.py): Python 3.10+, standard library only. Run it from the repository root with `.venv/bin/python courses/CS102-programming-for-games-ii-structures-and-patterns/labs/lab09-starter.py`. Add `--time` to print the timing table once your queries work. It contains:
  - Components `Position`, `Render`, `Mover`, `Health` (with a TODO `damage`), `AI` and `Burning`.
  - `Entity` with `get` and `has`, and a `World` with `spawn` and `destroy` written and `add`, `remove`, `query_poll`, `query` and `flush` as TODOs.
  - A `BLUEPRINTS` dict of entity types as data (player, goblin, chest, tree) with two TODO entries, and a TODO `make`.
  - TODO systems `ai_system`, `move_system` and `burn_system`.
  - A timing harness `timing_table()` that builds worlds of 1,000, 10,000 and 100,000 entities (0.5% burning, fixed seed) and times `query_poll(Burning, Health)` against `query(Burning, Health)`.
  - Four tests. On the untouched starter all four report `TODO`.
- The lecture's measured table (Python 3.13, Apple M4 Pro) as a reference. Your times will differ. The ratio should land in the same range, roughly 100 to 200 times.

## Steps

### Part A: the world (40 min)

1. **Health.** Implement `Health.damage`, clamping at 0 and returning whether the entity is still alive.
2. **Index.** Implement `World.add` and `World.remove` so the component dict and the index always agree. Use a dict with `None` values as the ordered set.
3. **Queries.** Implement `query_poll` (scan every entity) and `query` (start from the smallest index set, return a new list). Implement `make` from the blueprints. Run until `test_components_and_index` passes. It checks that both queries return identical lists.

### Part B: systems and a frame (40 min)

4. **Systems.** Implement `ai_system`, `move_system` and `burn_system` using `world.query`. Run until `test_systems` passes. The goblin at `(30, 40)` chasing a player at the origin at speed 90 should reach `(3, 4)` after half a second.
5. **Deferred destruction.** Implement `flush`. Run until `test_deferred_destroy` passes. Then, as an experiment, change `burn_system` to remove dead entities from the index immediately while iterating the index dict directly (not a copy). Record the exact error Python raises, then undo the change.
6. **New types as data.** Add `turret` and `mimic` to `BLUEPRINTS` without writing a class. Run until `test_new_types` passes.
7. **Order.** Write a `frame(world, dt)` that runs the systems in a fixed order and then flushes. Add a tiny `render_system` that prints each rendered entity's glyph and hp. Run burn before render and show, with printed output, the one-frame "drawn at 0 hp" bug: an entity that burns to 0 hp is only doomed, so it stays in the render query until `flush()`. Then show two fixes: (a) make `render_system` skip entities at 0 hp, and (b) swap the order so render runs before burn. In one sentence each, say what the player sees under each fix (under (b) every frame's damage is drawn one frame late).

### Part C: measure and judge (40 min)

8. **Time it.** Run with `--time`. Copy the table into your report. Compute your per-check cost for polling, in microseconds, from the 100,000 row.
9. **Budget.** Using your per-check cost, how many polling systems over 100,000 entities fit in a 16.7 ms frame? How many over 10,000?
10. **Churn.** Write a benchmark where 2,000 entities in a 10,000-entity world gain and lose a `WasHit` component every frame, and one system queries it. Time 100 frames with the index and 100 frames with polling (no index updates for `WasHit`). Report which is cheaper and by how much.
11. **Judge.** In 150 words, name one component in a game you like where you would *not* index, and give the number from your measurements that supports it.

## Deliverable

- Your completed starter (renamed `lab09-<yourname>.py`) with all four tests passing, plus your `frame`, `render_system` and churn benchmark below the tests.
- A text file of up to 400 words with: the error from step 5, the before-and-after output from step 7, your timing table and per-check cost, the step 9 and 10 numbers, and the 150-word judgment from step 11.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| World and index (steps 1-3) | Tests pass; index and components always agree; `query` starts from the smallest set and returns a copy in spawn order | Tests pass but `query` scans a larger set than needed or returns the live index | Tests fail | 25% |
| Systems, destruction, data types (steps 4-6) | All tests pass; error from step 5 recorded; new types added purely as data | Tests pass, step 5 experiment missing | Tests fail | 25% |
| Frame order (step 7) | Output shows the one-frame bug and both fixes, each with a one-sentence explanation | Bug shown with only one fix, or fixes without the bug | Missing | 15% |
| Measurement (steps 8-10) | Table, per-check cost, budget counts and churn result all present and consistent | Most numbers present, one inconsistent | Missing | 25% |
| Judgment (step 11) | Specific component, specific number from the student's own data | Plausible component, no number | Missing | 10% |
