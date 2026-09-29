# CS201 · Lab 07: A resource manager with handles and hot reload

**Week:** 7 ([lecture](../lectures/w07-resource-management-and-hot-reload.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). This resource manager is the one your final engine loads textures and materials through, and lab 8's render queue sorts by the handles it returns.

## Objective

Build the runtime half of a resource system: a cache that loads each file once, hands out generational handles, counts references and frees at zero, and reloads files in place without breaking a single handle. Add dependency-ordered rebuilds that are correct on graphs where the lecture's breadth-first order is not. Use the load-time model to justify a packing decision with numbers.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Python 3.10 or later, standard library only. The logic is the same you would write in C++; the lecture's `Pool<T>` shows the C++ shape, and the optional Part E ports your manager to it.

- `resources.py`: the `Handle` dataclass, a provided `parse_texture` loader for a tiny fake texture format (`"64x32 red"`), and nine stubs marked `TODO A1` to `TODO C2`. Each docstring states exactly what the checker expects.
- `check_lab07.py`: ten checks. Run `python check_lab07.py` inside the folder. Every check prints `TODO` on the starter, then `PASS` or `FAIL` with a reason. The script exits with 0 only when all ten pass.
- `watch_demo.py`: a hot-reload loop that polls `assets/` once a second and reloads changed files at the start of the next "frame". It works once Parts B and C pass.
- `assets/`: three texture files (`rock.tex`, `goblin.tex`, `water.tex`).

## Steps

### Part A: the load-time model (20 min)

1. Implement `load_time`, `knee_mb` and `pack_or_loose`. Checks A1 to A3 must pass.
2. In your README, use `pack_or_loose` to answer: a UI screen loads 250 icons of 24 KB each. On the laptop hard drive (`t_a = 15 ms`, `R = 100 MB/s`) and on the SSD (`t_a = 0.1 ms`, `R = 5,500 MB/s`), what is the speedup from packing? Should you pack for the SSD build? Give one reason beyond load time.

### Part B: handles and reference counts (45 min)

3. Implement `acquire`, `get`, `release` and `refs`. Start with `acquire` and `get`; B1 must pass before the others make sense. Then B2 to B4.
4. B2 checks that a freed slot is reused with a new generation. Write two sentences in your README: what would the stale handle `a1` return if you had left out the generation, and what would that look like on screen in a real game?
5. B4 loads a broken file. Explain why a failed load must not take a slot or a reference, and what bug you would get later if it did.

### Part C: hot reload and dependency order (40 min)

6. Implement `reload`. C1 must pass. It checks that all 300 handles see a new rock texture, and that a half-typed save keeps the last good data.
7. Run `python watch_demo.py`. While it runs, edit `assets/rock.tex` in a text editor three times: a valid change (`128x128 mossy`), a typo (`128x12 mossy`), and the fix. Paste the terminal output into your README and point to the frame where the swap happened.
8. Implement `rebuild_order` as a topological sort (C2, C3). Before you do, run the lecture's breadth-first `rebuild_order` on the `diamond` graph in check C2 and write down its output. In one sentence, say what a player would see if the engine rebuilt in that order.

### Part D: layout memo (15 min)

9. Your team's MMO zone has 8 subzones of 120 MB unique data each, plus 500 shared prop files averaging 0.16 MB, of which each subzone uses 300. Compute the subzone load time on the laptop hard drive for "store once, loose" and for "duplicate the used props into each subzone", and the disk cost of each. Recommend a layout for a hard-drive platform and for an SSD platform in at most 150 words.

### Part E (optional, +5 bonus): port to C++

10. Port `ResourceManager` to C++ on top of the lecture's `Pool<T>` with `T = Texture { int w, h; std::string color; }`. Add an RAII `TextureRef` class whose constructor calls `acquire` and whose destructor calls `release`, with a move constructor and deleted copy (week 2). Show in a 20-line `main` that leaving a scope drops the count.

## Deliverable

A zip of your `lab07-starter/` folder containing:

- `resources.py` with all ten checks passing.
- `README.md` (at most two pages): how to run the checks, answers to steps 2, 4, 5 and 8, the `watch_demo.py` session from step 7, and the Part D memo with its numbers.
- Optional: `pool.cpp` for Part E, with the build command in the README.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Load-time model (A1-A3, step 2) | Checks pass; speedups correct for both drives; a non-time reason given (open cost, patching, file count limits) | Checks pass, reasoning thin | Checks fail | 15 |
| Handles and counts (B1-B4, steps 4-5) | All four pass; explanations name the wrong-texture symptom and the leaked slot | Checks pass, explanations vague | Two or more checks fail | 30 |
| Hot reload (C1, step 7) | C1 passes; session shows reload, kept data on the typo, and recovery at a frame boundary | C1 passes, session incomplete | C1 fails | 20 |
| Dependency order (C2, C3, step 8) | Both pass; BFS output recorded and the visible symptom explained | Checks pass, step 8 missing | Checks fail | 20 |
| Layout memo (Part D) | Numbers correct, recommendation differs by platform with a reason | Numbers correct, recommendation generic | Missing or wrong numbers | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

Step 2: 250 × 0.024 = 6 MB. HDD loose 3.81 s, packed 0.075 s, about 51×. SSD loose 0.0261 s, packed 0.0012 s, about 22×, but the absolute saving is 25 ms. Good non-time reasons: per-file open cost in the OS, one checksum per pack for patching, fewer file handles, console file-count limits if the student can cite one.

Step 8: the lecture's BFS returns `['a/model', 'z/mat']`, so `a/model` is rebuilt from the old `z/mat` and shows the old material until the next reload.

Part D: shared used per subzone = 300 × 0.16 = 48 MB, so B = 168 MB. Store once: S = 1 + 300 = 301, T = 4.515 + 1.68 = 6.195 s, disk = 8 × 120 + 500 × 0.16 = 1,040 MB. Duplicate: S = 1, T = 1.695 s, disk = 8 × 168 = 1,344 MB (plus the 200 unused props if they are still shipped once: 1,376 MB). Accept either disk figure if the assumption is stated. On the SSD the loose layout costs 0.0301 + 0.0305 = 0.061 s, so duplication saves about 30 ms.

Common Part B bug: incrementing the generation on every `release` instead of only at zero, which makes other holders' handles stale. Check B2 catches it because `a2` must stay valid after `a1` is released.

</details>
