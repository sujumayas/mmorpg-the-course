# CS201 · Lab 06: AoS to SoA

**Week:** 6 ([lecture](../lectures/w06-cache-locality-and-data-oriented-design.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). The layout you choose in Part D replaces the component storage in your lab 05 ECS for the final engine.

## Objective

Convert the lecture's 128-byte entity into a hot/cold split and a struct-of-arrays layout, implement the byte model, and prove the new layouts give bit-identical results. Then measure all three on your own machine, compare the measurements with the model for your cache line size, track down one surprising result, and redesign the entity layout of an MMO client for three systems.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). C++20 and the standard library only.

- `layout.hpp`: `EntityAoS` (128 bytes), `Hot`, `Cold`, `SplitEntities`, `EntitiesSoA`, the reference `move_aos`, and six stubs marked `TODO 1` to `TODO 6`.
- `test_layout.cpp`: six checks. Build and run with `c++ -std=c++20 -O2 test_layout.cpp -o test_layout && ./test_layout`. Every check prints `FAIL` on the starter, and the program exits with 0 only when all six pass.
- `bench_layouts.cpp`: times movement over the three layouts at 10,000, 100,000, 1,000,000 and 10,000,000 entities and prints the model's prediction. Build with `c++ -std=c++20 -O2 bench_layouts.cpp -o bench_layouts` and run with your cache line size as the argument, for example `./bench_layouts 64`. It needs about 1.5 GB of free memory for the largest size. If your machine has less, delete `10'000'000` from the list and say so in your README.

## Steps

### Part A: conversions and systems (45 min)

1. Find your machine's cache line size (macOS: `sysctl hw.cachelinesize`; Linux: `getconf LEVEL1_DCACHE_LINESIZE`; Windows on x86-64: 64). Write it at the top of your README.
2. Implement `to_soa` and `to_split` (TODO 1 and 2) using only `push_back`, with no `reserve`. Checks 1 and 2 must pass.
3. Implement `move_soa` and `move_split` (TODO 3 and 4). Checks 3 and 4 compare every position with `==`, not with a tolerance. Write one sentence in your README on why exact equality is a fair test here, and one on what would make it fail (hint: think about the order of floating-point operations).
4. Implement the byte model and `damage_team_soa` (TODO 5 and 6). Checks 5 and 6 must pass.

### Part B: measure (25 min)

5. Run `bench_layouts` three times with your line size. Record the median of each cell in a table in your README.
6. Compare your 1,000,000 row with the model's prediction. Is the measured AoS/SoA ratio above or below it? Using the lecture's discussion of write-back and SIMD, explain the gap in at most 100 words.
7. Find the `N` at which the AoS/SoA ratio jumps. Relate it to your machine's cache sizes (macOS: `sysctl hw.perflevel0.l2cachesize`; Linux: `lscpu`). Show the working-set arithmetic for AoS and SoA at the `N` before and after the jump.

### Part C: a surprise (25 min)

8. Look at your SoA column at 100,000 entities. On the reference machine, with `push_back` only, it was about 0.14 ms, slower than AoS at the same size and five times slower than the 0.027 ms the lecture reports. Check whether yours shows the same effect.
9. Print `soa.px.capacity()` and the addresses of `soa.px.data()`, `soa.py.data()` and `soa.vx.data()` at `N = 100,000`. Then change `to_soa` to `reserve(es.size())` on every array first, and rerun. Record both results.
10. Explain in at most 120 words what changed and your best explanation of why. Hints: compare the capacity with a power of two; look at how far apart the arrays start; the cache decides where a line may be stored using some of the address bits. If you cannot explain it fully, say what evidence you have and what experiment would settle it.

### Part D: design (25 min)

11. An MMO client keeps 20,000 nearby entities. Its entity struct is:

    ```cpp
    struct NetEntity {
        char name[32]; char guild[32];
        float prev_pos[3], next_pos[3]; double snapshot_time;
        float pos[3]; float radius;
        std::uint32_t id, flags; float health, max_health;
        std::uint8_t visible; std::uint8_t faction;
    };
    ```

    Three systems run each frame: interpolation (reads `prev_pos`, `next_pos`, `snapshot_time`; writes `pos`), culling (reads `pos`, `radius`; writes `visible`) and nameplates (for visible entities only, about 300: reads `pos`, `name`, `guild`, `health`, `max_health`). Compute `sizeof(NetEntity)` by hand with padding and check it with `static_assert`. Then design a layout (split, SoA, or a mix) and give a table of bytes fetched per entity for each system, before and after, at your line size. Justify every choice in one line.

## Deliverable

A zip of your `lab06-starter/` folder containing:

- `layout.hpp` with all six checks passing (with `reserve` added in step 9), the unchanged `test_layout.cpp` and `bench_layouts.cpp`, and a `netentity.cpp` with your `static_assert`s from step 11.
- `README.md` (at most three pages): line size, the answers to step 3, the benchmark table, the answers to steps 6, 7 and 10 with the data from step 9, and the design table from step 11.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Implementation (checks 1 to 6) | All pass; step 3 answered correctly | All pass, step 3 vague | Two or more fail | 25 |
| Measurement and model (steps 5 to 7) | Clean table; gap explained with write-back and SIMD; cache-size arithmetic correct at both `N` | Table present, explanation or arithmetic weak | Missing | 25 |
| Surprise (steps 8 to 10) | Data from both runs; explanation links power-of-two spacing to cache placement, or states evidence and a deciding experiment | Data present, explanation guesses without evidence | Missing | 20 |
| Design (step 11) | Correct `sizeof`; layout serves all three systems; per-system bytes table correct | One system's numbers wrong | Missing | 30 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

Reference machine (Apple M4 Pro, 128-byte lines, Apple clang 17, `-O2`, September 2026), `push_back` only, median of three runs: at 1,000,000 entities AoS about 4.2 ms, split 0.55, SoA 0.27 (ratio about 15, model 5.33); at 10,000,000 AoS 44, split 5.8, SoA 2.8. At 100,000 entities SoA was 0.14 ms with `push_back` and 0.038 ms after `reserve`.

With `push_back`, each array's capacity at 100,000 is 131,072 floats (512 KiB, a power of two), and the arrays are large enough to be placed on their own page-aligned regions, so the six streams start at addresses that differ by multiples of a large power of two. The likely cause of the slowdown is that those streams compete for the same cache sets (the set index is taken from low address bits), so lines evict each other. The effect disappears when `reserve` gives each array exactly 400,000 bytes. We have not verified the exact placement rule of the reference machine's allocator or cache, so accept any answer that shows the capacity and address evidence and proposes a deciding experiment (for example, padding each array by one cache line and rerunning).

Step 11: with natural alignment `sizeof(NetEntity)` is 136 on common 64-bit ABIs (the `double` forces 8-byte alignment; 32 + 32 + 12 + 12 = 88, then `snapshot_time` at 88, `pos` at 96, `radius` at 108, `id` at 112, `flags` 116, `health` 120, `max_health` 124, the two bytes at 128 and 129, padded to 136). Good designs put `prev_pos`, `next_pos`, `snapshot_time`, `pos` and `radius` in hot arrays or a hot struct, move `name` and `guild` to a cold array, and replace `visible` with a list of visible indices rebuilt by culling. Students should notice that the nameplate system benefits least and matters least, since it touches only about 300 entities.

</details>
