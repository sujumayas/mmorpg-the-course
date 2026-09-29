# CS201 · Lab 01: A layer checker

**Week:** 1 ([lecture](../lectures/w01-engine-anatomy-and-runtime-layers.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs (one keyboard, swap every 20 minutes).
**Counts toward:** subsystem labs (50% of the course grade). You will run this checker on your own engine at the end of the semester, so write it to last.

## Objective

Build a small Python tool that reads a C++ source tree and reports, for any layer map you give it, every upward dependency, every file outside the platform layer that includes an OS header, the port share, and a start-up order. Then use it on Kiln, a 14-file mini engine, and fix Kiln's C++ until the tool reports zero problems while the engine still builds and runs.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Python 3.10 or later, standard library only. A C++20 compiler (`c++`, `clang++` or `g++`; on Windows use MSVC from a Developer prompt or MinGW).

- `layercheck.py`: the `CycleError` class, six functions to write (`parse_includes`, `layer_of`, `scan`, `upward`, `os_leaks`, `start_order`) and a finished `report()` that prints the summary once they work. Each docstring states exactly what the checks expect.
- `layers.json`: the layer number of each top-level folder, the name of the platform folder, and the list of OS header prefixes.
- `mini_engine/`: Kiln. Thirteen header files in six layer folders plus `main.cpp`. It builds and runs as shipped. It contains two upward includes and one OS leak, planted on purpose. Comments mark them, but your tool must find them without reading comments.
- `check_lab01.py`: seven checks. Run `python check_lab01.py` from inside the folder. Each check prints `TODO` until you write the function it needs, then `PASS` or `FAIL` with a reason. On the starter all seven print `TODO` and the script exits with code 1.

Build Kiln before you change anything, so you know what "still works" looks like:

```
cd mini_engine
c++ -std=c++20 -Wall -I. main.cpp -o kiln
./kiln
```

## Steps

### Part A: reading includes (30 min)

1. Implement `parse_includes`. Use a regular expression anchored at the start of the line. Checks 1 must pass. Look at the `SAMPLE` string in `check_lab01.py`: which of its five lines is the trap, and why does anchoring handle it?
2. Implement `layer_of` and `scan`. Checks 2 and 3 must pass. Paths in the result use forward slashes on every OS (`Path.as_posix()`).

### Part B: finding violations (35 min)

3. Implement `upward`. Only quoted includes of files that exist in the tree count. Check 4 must pass.
4. Implement `os_leaks`. An OS header matches by prefix, so `"sys/"` catches `<sys/stat.h>`. Check 5 must pass.
5. Run `python layercheck.py mini_engine layers.json` and copy the output into your README. Compute the port share by hand from the line counts and confirm the tool agrees.

### Part C: start-up order (25 min)

6. Implement `start_order` with the rule in its docstring: repeatedly take the alphabetically first module whose needs are all placed. Checks 6 and 7 must pass.
7. Write Kiln's subsystem dependencies as a dict (window, clock, files, memory, log, resources, renderer, audio, game) from what each header uses, and print the order your function gives. Put the dict and the order in your README.

### Part D: fix Kiln (30 min)

8. Remove both upward includes and the leak without changing what Kiln prints (the log prefix may change). Use the techniques from lecture sections 4 and 2:
   - `platform/window.h` must hand key presses to the game through a function-pointer slot the game fills at start-up.
   - `core/log.h` must not know the player exists.
   - `game/save.h` must ask the platform layer whether a file exists instead of calling `access()` itself.
9. Rebuild and rerun Kiln. Then run your checker on it. It must print `upward dependencies: 0` and `OS leaks: 0` and exit with code 0. Record the new port share. Explain in two sentences why it went down even though you added code to the platform layer.

### Part E: point it at real code (optional, up to 5 bonus points)

10. Clone `id-Software/DOOM` and write a `doom_layers.json` that maps prefixes to layers (you will need a small change to `layer_of`, since Doom uses prefixes, not folders). Report how many upward includes your map finds. There is no single right map; defend yours in three sentences.

## Deliverable

A zip of your `lab01-starter/` folder containing:

- `layercheck.py` with all seven checks passing.
- The fixed `mini_engine/`, which builds with the command above and passes your checker.
- `README.md` (one page at most): the checker output before and after Part D, the hand computation from step 5, the dependency dict and order from step 7, and your two-sentence answer from step 9.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Parsing and scanning (checks 1-3) | All pass; regex handles the trap line and trailing comments | Checks pass but code relies on the sample's exact spacing | Checks fail | 20 |
| Violations (checks 4-5, step 5) | Both pass; hand computation matches the tool | Checks pass, hand computation missing or wrong | Checks fail | 20 |
| Start-up order (checks 6-7, step 7) | Both pass; Kiln dict matches the headers | Checks pass; Kiln dict has one wrong edge | Checks fail | 20 |
| Kiln refactor (steps 8-9) | Zero violations, builds with `-Wall` without warnings, same behavior, callback used for input | Zero violations but behavior changed or warnings added | Violations remain or it does not build | 30 |
| README | Complete, outputs pasted, step 9 answer names the leaked file's lines | Incomplete | Missing | 10 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

The reference solution reports, on the shipped fixture, 14 files and 170 lines, two upward dependencies (`core/log.h -> game/player.h`, `platform/window.h -> game/game.h`), one leak (`game/save.h`) and a port size of 51 of 170 lines (30.0%). After the reference refactor the tree is 157 lines with a port size of 35 lines (22.3%); students' numbers will differ by a few lines. The share drops because `game/save.h` (10 lines) drops out of the port size entirely. In the reference refactor `platform/window.h` also shrinks from 13 to 7 lines, because it no longer carries the game include; a student version that adds wrapper code to `platform/file.h` will land a few lines higher. Common mistakes: matching `#include` anywhere in the line (catches the trap on line 5 of `SAMPLE`), counting system includes as upward dependencies, and a `start_order` that returns a valid but different order because it does not re-sort the ready set after each placement.

</details>
