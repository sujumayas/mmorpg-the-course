# CS201 · Lab 05: A sparse-set ECS

**Week:** 5 ([lecture](../lectures/w05-entity-component-system-design.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). The `ecs.hpp` you finish here is the entity layer of your final engine. Week 6 changes how its component data is laid out, so keep the interface clean.

## Objective

Implement generational entity handles, a checked sparse-set component pool with swap-and-pop removal, and a two-component view in C++. Measure the two storage layouts from the lecture on your own machine, compute your own break-even rate of component changes, and recommend a storage strategy for five components of your demo game.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). C++20 and the standard library only.

- `ecs.hpp`: `Entity`, `EntityPool`, `Pool<T>` and `each2`, with seven stubs marked `TODO 1` to `TODO 7`. The comments state what the checks expect, including the error cases the lecture's minimal version skipped (stale destroy, duplicate add, removing a missing component).
- `test_ecs.cpp`: nine checks, including the lecture's trace. Build and run with `c++ -std=c++20 -O2 test_ecs.cpp -o test_ecs && ./test_ecs`. Every check prints `FAIL` on the starter, and the program exits with 0 only when all nine pass.
- `bench_storage.cpp`: the lecture's benchmark. It is self-contained and does not use your `ecs.hpp`, so it runs now. Build with `c++ -std=c++20 -O2 bench_storage.cpp -o bench_storage`.

## Steps

### Part A: handles (25 min)

1. Implement `EntityPool::create`, `destroy` and `alive` (TODO 1 to 3). Checks 1 to 3 must pass.
2. Add a comment above `destroy` that explains in two sentences why destroying a stale handle must be refused, with the bug that would follow if it were not. (Hint: what happens to the free list?)

### Part B: pools and views (50 min)

3. Implement `Pool::has`, `add` and `remove` (TODO 4 to 6). Checks 4 to 6b must pass. Check 5 and 6 are the lecture's trace table.
4. Implement `each2` (TODO 7). Check 7 must pass. It requires walking the smaller pool, so the order of visits is part of the test.
5. Write `demo.cpp` (about 40 lines). Create 1,000 entities with `Pos` and `Vel`, stun a random 100 of them each frame for 10 frames (add `Stunned` to 50 unstunned ones and remove it from 50 stunned ones), and run a movement system with `each2` that skips stunned entities. Destroy 10 entities per frame through a command list applied at the end of the frame, as in lecture section 3. After the run, print the live count, the size of each pool, and the result of `alive` on one handle you destroyed on frame 1. Paste the output into your README.

### Part C: your break-even (30 min)

6. Run `bench_storage` five times. Record the range of each of the four numbers.
7. Using the lecture's method, compute your machine's break-even rate of toggles per frame for one join system and for eight join systems. Show the arithmetic.
8. Change `Other` in `bench_storage.cpp` so a unit's components total about 400 bytes instead of 112 (for example, `char ai[352]`). Rerun, recompute the break-even for one system, and explain the change in one sentence using the lecture's cost model.

### Part D: recommendation (15 min)

9. Pick five components for the demo game you will build on your engine (at least two that change often). For each, recommend archetype column, sparse set, or enable flag, and justify it in one line with an estimated "changes per second" and "systems that join it", using your numbers from Part C.

## Deliverable

A zip of your `lab05-starter/` folder containing:

- `ecs.hpp` with all nine checks passing, `demo.cpp`, your modified `bench_storage.cpp` from step 8 (named `bench_storage_400.cpp`), and the unchanged `test_ecs.cpp` and `bench_storage.cpp`.
- `README.md` (at most two pages): build commands, the `demo` output, the benchmark ranges, both break-even calculations, the step 8 explanation and the five-row recommendation table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Handles (checks 1 to 3, step 2) | All pass; comment names the double free-list entry and the aliasing it causes | Pass, comment vague | Two or more fail | 15 |
| Pools and view (checks 4 to 7) | All pass; no extra lookups in the walked pool | Pass with an extra `get` on the walked pool | Two or more fail | 30 |
| Demo (step 5) | Deferred destruction, stunned entities skipped, correct counts, stale handle reported dead | Runs, one of these missing | Does not run | 20 |
| Break-even (steps 6 to 8) | Ranges recorded; both calculations correct; 400-byte result explained with `2S` | One calculation wrong or explanation missing | Missing | 20 |
| Recommendation (step 9) | Five components, each justified with the two numbers | Justifications without numbers | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

On the reference machine (Apple M4 Pro, Apple clang 17, `-O2`, September 2026), `bench_storage` printed toggles of 34 to 49 ns (archetype) and 6.4 to 8.8 ns (sparse set), and movement of 0.022 to 0.026 ms (archetype) and 0.133 to 0.157 ms (sparse set). With typical values the one-system break-even is about 3,400 toggles per frame and the eight-system break-even about 27,000.

Step 2: if `destroy` accepted a stale handle, it would bump the generation again and push the index onto the free list a second time. Two later `create` calls would then return the same index, and two live entities would share one set of components.

Step 8: with `S` near 400 bytes the archetype toggle copies about `2 × 400` bytes, so its cost rises several-fold and the break-even falls. The sparse-set toggle does not change, because it never touches the other components. The movement numbers change little for the archetype (it reads only the Position and Velocity columns).

Common mistakes: `has` reading `sparse[e]` without checking `e < sparse.size()`; `remove` forgetting to update `sparse` for the moved element when the removed element was not last; `each2` calling `get` on the pool it walks instead of using `data[i]`.

</details>
