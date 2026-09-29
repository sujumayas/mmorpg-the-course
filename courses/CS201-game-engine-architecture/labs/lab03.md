# CS201 · Lab 03: Three allocators

**Week:** 3 ([lecture](../lectures/w03-memory-allocators-stack-pool-and-frame.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). These allocators are the memory system of your final engine: the frame allocator is reset in week 4's end-of-frame step, and week 5's component storage sits on the pool.

## Objective

Implement a stack allocator with markers, a double-ended stack that reports its largest free run, and a pool allocator with an embedded free list. Each takes one block from the OS at construction and never touches the global heap again. Then measure where a pool beats `new` and `delete`, and where the gap is smaller than you'd expect.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). A C++20 compiler and Python 3.10+.

- `allocators.h`: the three classes with constructors, destructors and accessors written, and every allocation function marked TODO. The starter compiles cleanly, returns `nullptr` or 0, and is safe to run.
- `test_lab03.cpp`: twelve tests. A1-A4 stack, B1-B3 double-ended stack, C1-C4 pool, and G1, which replaces the global `operator new` with a counter and fails if any allocator uses it after construction. Test A1 uses the five requests from lecture section 3, so its expected offsets are the table you checked by hand.
- `run_tests.py`: builds with UndefinedBehaviorSanitizer (misaligned pointers are undefined behavior, so UBSan catches alignment bugs) and runs the tests. `--asan` adds AddressSanitizer. On the starter, 12 tests fail and it exits with code 1.
- `bench.cpp`: the Part D benchmark. Case 1 is the lecture's particle measurement. Case 2 uses five sizes (16 to 256 bytes) freed in random order, with a fixed random seed so every run does the same work. The pool half of case 2 is yours to write. On the starter it prints that the pool is not implemented and exits with code 1.

## Steps

### Part A: stack allocator (30 min)

1. Implement `StackAllocator::alloc`, `free_to` and `reset`. Align the *address*, not the offset: the base is 16-byte aligned, but test A2 asks for alignments up to 256. A failed request must leave `top` unchanged. Tests A1-A4 must pass.
2. In your README, show the arithmetic for one allocation from A2 with alignment 64: the address before, the rounded address, and the padding.

### Part B: double-ended stack (35 min)

3. Implement `alloc_low` the same way as the stack.
4. Implement `alloc_high`. It grows down, so compute the start as `end − bytes` and round the start *down* to the alignment. Fail, changing nothing, if the block would reach below the low end. `high_used()` counts bytes from the top of the block. Test B1 must pass. In your README, explain why rounding down is correct at the high end and rounding up is correct at the low end.
5. Implement the two `free_to` functions and `largest_free()`. Tests B2 and B3 must pass.
6. Write a 20-line program that replays the lecture's "two ends" load from section 2 on a `DoubleEndedStack` of 100 MiB, with assets high and read buffers low (use `free_to_low` after each file). Print `largest_free()` after the load. It must print 51,380,224 bytes (49 MiB). Put the output in your README.

### Part C: pool allocator (30 min)

7. Implement the pool constructor: compute the block size (the rule is in the header comment), take one block with `std::malloc`, and thread every slot onto the free list so that block 0 comes out first. Test C1 must pass.
8. Implement `alloc` and `free`. Keep `free_count_` correct. Tests C2-C4 and G1 must pass.
9. In your README, compute the internal fragmentation for pools of `Particle` (20 bytes), a 44-byte `Projectile` and a 64-byte `NetMessage`. Which one would you give a different rounding rule, and what does that cost?

### Part D: measure (25 min)

10. Finish case 2 in `bench.cpp`: one `PoolAllocator` per size class (16, 32, 64, 128, 256 bytes), 5,000 blocks each, and the same allocate, shuffle and free sequence as the heap half. Build with `c++ -std=c++20 -O2 bench.cpp -o bench`.
11. Run it five times and record the median of each of the four numbers, with your machine, OS and compiler. Compare the pool-versus-heap ratio in case 1 and case 2.
12. Write one paragraph for your README that answers: did the gap grow or shrink in case 2, and why? Then name one property of the pools that this benchmark does not measure at all but that lecture section 2 says matters more.

## Deliverable

A zip of your `lab03-starter/` folder containing:

- `allocators.h` with all twelve tests passing under `python run_tests.py`.
- `bench.cpp` with case 2 complete, and the Part B replay program (`replay.cpp`).
- `README.md` (one page at most): answers to steps 2, 4, 9 and 12, the replay output, and the Part D table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Stack allocator (A1-A4) | All pass; alignment on the address; failed calls change nothing | All pass but alignment computed on the offset (works only because the base is aligned) | Any fails | 20 |
| Double-ended stack (B1-B3, step 6) | All pass; replay prints 51,380,224 | Tests pass, replay wrong or missing | Any test fails | 20 |
| Pool allocator (C1-C4, G1) | All pass; free list embedded; no extra containers | All pass but uses an extra array for the free list (G1 still passes) | Any fails | 25 |
| Measurements (steps 10-11) | Case 2 pools correct; five-run medians with machine details | Numbers present, single run or missing details | Missing | 15 |
| README answers (steps 2, 4, 9, 12) | Correct, specific, step 12 names largest free run or predictability | Mostly correct but vague | Missing | 20 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

A reference solution passes all twelve tests under UBSan. On an Apple M4 Pro with clang 17 at `-O2`, case 1 gives about 0.07 ms for `new`/`delete` and 0.006 ms for the pool, and case 2 gives about 0.15 ms for the heap; students' case 2 pool numbers should be in the same range as case 1's pool plus the shuffle, which the timed region includes in both halves. Expect the heap-versus-pool ratio to vary a lot by OS: glibc, the macOS allocator and the Windows heap behave differently with random free order, which is a good discussion point. Step 6: 100 MiB is 104,857,600 bytes; the assets use 51 MiB (53,477,376 bytes), leaving 51,380,224. Step 9: 32, 48 and 64-byte blocks, so 37.5%, 8.3% and 0%. Common mistakes: rounding the high end up instead of down (B1 fails with an overlap), forgetting to decrement `free_count_`, and building the free list in ascending order so block `count − 1` comes out first (C2 fails).

</details>
