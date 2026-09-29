# CS201 · Lab 08: A sorted render queue

**Week:** 8 ([lecture](../lectures/w08-rendering-pipeline-overview.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). The queue you write here is the one your final engine submits through, and week 13's profiler reads its switch counter.

## Objective

Implement the lecture's 64-bit sort key and a state-switch counter in C++. Run them on a recorded 1,800-draw scene and measure how much each ordering costs under the section 2 model. Then design a variant key that trades exact back-to-front order for fewer translucent switches, measure both sides of the trade, and decide whether it is worth it.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). C++17 and the standard library only. Any recent Clang, GCC or MSVC works.

- `render_queue.hpp`: the `Pass` enum, the `Draw` struct, `load_scene`, and five stubs marked `TODO 1` to `TODO 5` (`quantize_depth`, `make_key`, `sort_by_key`, `count_switches`, `submit_us`). Each comment states exactly what the checks expect.
- `test_render_queue.cpp`: fifteen checks. Build and run with `c++ -std=c++17 -O2 test_render_queue.cpp -o test_render_queue && ./test_render_queue`. Most checks print `FAIL` on the starter. The program exits with 0 only when all fifteen pass.
- `analyze.cpp`: prints the switch count and simulated submit time of `scene.csv` in file order, sorted by material only, and sorted by your key. Build with `c++ -std=c++17 -O2 analyze.cpp -o analyze`. Optional arguments set `c_draw` and `c_switch` in microseconds (defaults 2 and 10).
- `scene.csv`: 1,800 draws from an MMO town scene: 1,400 opaque over 36 materials, 320 translucent over 14 materials, 80 UI over 3 materials. Columns `id,pass,material,depth`, depth in metres.

## Steps

### Part A: the key (40 min)

1. Implement `quantize_depth` and `make_key` (TODO 1 and 2). Checks 1 to 2d must pass. Check 2d is the lecture's check-yourself question 2.
2. In your README, answer: with `kNear = 0.1` and `kFar = 500`, how many metres is one depth step? Two opaque rocks with the same material are 1 mm apart. Can the key order them?

### Part B: sort and count (30 min)

3. Implement `sort_by_key`, `count_switches` and `submit_us` (TODO 3 to 5). All fifteen checks must pass.
4. Build and run `analyze`. Copy its output into your README.
5. Compare the three rows against the lecture's model. Use `N(1 − 1/M)` with `M = 53` for file order and `(M_o − 1) + 1 + N_t(1 − 1/M_t) + 1` for the keyed order (the last `+ 1` is the move to the UI pass). The opaque materials in this scene are not used equally. Does that make the model's file-order estimate too high or too low, and why?
6. The "material only" row has the fewest switches. Explain in two sentences why the engine must not ship it, naming both passes it breaks.

### Part C: a cheaper translucent key (40 min)

7. Almost all remaining switches are inside the translucent pass. Write `make_key_slabbed` in a new file `slab.hpp`: for translucent draws, split the depth range into `K` slabs, sort slabs far to near, then by material inside a slab, then far to near inside a material. Keep opaque and UI as before.
8. Add to `analyze.cpp` a report for `K = 1, 2, 4, 8, 16`: translucent switches, and the number of **inverted pairs** (pairs of translucent draws where the nearer one is drawn first). Inverted pairs are the draws that may blend wrongly if they overlap on screen.
9. Look at the depths of the translucent draws in `scene.csv`. Change where your slabs start and end so they cover only that range, and rerun. Put both tables in your README.
10. Write a memo of at most 200 words: which `K` would you ship for this town, what would a player see if you picked it wrong, and which kinds of translucent effect could safely use a large `K` (think particles far apart versus overlapping glass panes).

### Part D (optional, +5 bonus): measure the real cost

11. Time `sort_by_key` on the scene with `std::chrono::steady_clock` over 1,000 runs and report the mean in microseconds. Compare it with the submit-time saving from sorting at the default costs. Does sorting pay for itself?

## Deliverable

A zip of your `lab08-starter/` folder containing:

- `render_queue.hpp` with all fifteen checks passing, `slab.hpp`, and your extended `analyze.cpp`.
- `README.md` (at most two pages): build commands, answers to steps 2, 5 and 6, the `analyze` outputs from steps 4, 8 and 9, the memo from step 10, and Part D if attempted.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Key and quantization (checks 1-2d, step 2) | All pass; depth step computed and the 1 mm question answered with the tie rule | Checks pass, step 2 wrong or vague | Checks fail | 20 |
| Sorting and counting (checks 3-6d) | All pass | One check fails with a sensible diagnosis in the README | Two or more fail | 25 |
| Model comparison (steps 5-6) | Estimates computed; direction of the uneven-materials error explained; both broken passes named | Estimates computed, explanation thin | Missing | 20 |
| Slab key and measurements (steps 7-9) | Both tables present; re-ranged slabs show a clear improvement and the student says why | Tables present, re-ranging missing | Missing or wrong counts | 20 |
| Memo (step 10) | Chooses a `K`, names the visible artifact, distinguishes safe and unsafe effects | Choice made without the artifact or the distinction | Missing | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

Reference output with default costs: file order 1,764 switches (21,240 µs), material only 52 switches (4,120 µs), sort key 336 switches (6,960 µs), of which 297 are inside the translucent pass.

Step 2: `499.9 / 16,777,215 ≈ 0.03 mm` per step, so 1 mm is about 34 steps and the key orders the rocks. Students who answer with float precision concerns deserve credit if they note that `float` depth near 500 m has a resolution of about 0.03 mm too.

Step 5: file-order formula `1,800 × (1 − 1/53) ≈ 1,766`, measured 1,764. Keyed formula `35 + 1 + 320 × (1 − 1/14) + 1 ≈ 334`, measured 336. Uneven material use makes neighbors more likely to match, so the uniform formula is slightly too high for file order; in this scene the effect is small because the weights only range from 1 to 6.

Step 6: material-only interleaves passes (translucent before opaque at the same material id breaks blending, UI may be drawn under the world) and ignores depth inside the translucent pass.

Steps 8 and 9: with slabs spanning the full 0.1 to 500 m range, all translucent draws (1 to 120 m) fall into the first slab or two, so `K = 1, 2, 4` give 13 switches and about 23,700 inverted pairs, `K = 8` gives 27 and about 11,500, `K = 16` gives 55 and about 5,800. Re-ranging to 1 to 120 m makes each slab count. The point to reward is noticing that slabs must fit the data.

</details>
