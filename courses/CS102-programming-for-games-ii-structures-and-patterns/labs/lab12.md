# CS102 · Lab 12: Record, replay and find the desync

**Week:** 12 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** one of the weekly labs (labs are 40% of the course in total); the recorder is reused in the pattern project

## Objective

Record 30 seconds of a small arena game as a stream of one-byte commands, replay it in a fresh Python process, and make the replay match the recording checksum for checksum. You find three planted sources of nondeterminism by bisecting with per-second checksums, then add undo and redo to the game's tile editor. This lab is the course's signature worked example from [week 12](../lectures/w12-command-pattern-input-replay-undo.md), done by hand.

## Starter materials

- `lab12-starter.py`: Python 3.10+, standard library only. Run it from this folder.
  - `python lab12-starter.py record run.rep` plays a scripted 30 seconds at 60 ticks per second and writes a recording.
  - `python lab12-starter.py replay run.rep` replays a recording and reports the first second whose checksum differs.
  - `python lab12-starter.py check` records, then replays in a **new** Python process, which is what a player loading a replay file does.
  - `python lab12-starter.py --test` runs the self-checks. Three fail on the untouched starter, and two more undo checks appear once `History` exists.
- The recording format is documented at the top of the file: an 11-byte header (magic, version, seed, tick count), one command byte per tick, then a 4-byte checksum for every full second.
- The simulation has three planted determinism bugs. Lines that deserve a look are tagged `# suspicious?`, and so are some harmless lines. Part of the job is telling them apart.
- Enemy names and all numbers are invented for teaching.

## Steps

1. **Baseline.** Run `check` three times. Record the recording size, the first bad second and the kills each time. Explain why the kill count changes between runs of the *recording*, which should not happen if the recording is a faithful description of play.
2. **Size model.** Before looking at the file, predict its size from the format description. Then predict the size of the same 30 seconds as snapshots (6 objects: the player with x, y and 5 enemies with x, y, hp, respawn timer, all as 8-byte values). State the ratio.
3. **Bug hunt.** Fix one bug at a time. After each fix, run `check` and `--test` and record which checks pass. For each bug, write: the line, which part of the state it corrupts (position, randomness or order), and the mechanism in one sentence. Use the section 3 checklist from the lecture.
4. **Why the new process matters.** One of the three bugs is invisible to the same-process test and only shows up in `check`. Which one, and why? Name a way to make it visible in a single process (hint: look up `PYTHONHASHSEED`).
5. **Bisecting a desync.** Change the checksum interval from 60 ticks to 1 tick and add a debug mode to `replay` that prints both states side by side at the first bad tick. Reintroduce any one bug and show the output your tool gives. Store this tool; the pattern project needs it.
6. **Undo and redo.** Implement `PaintTile` as in lecture section 4 and a `History` with `run`, `undo` and `redo` as in [week 6](../lectures/w06-queues-and-stacks-undo-and-command-buffers.md), so the undo tests pass. Then add `FillRect(x0, y0, x1, y1, tile)` that stores only the tiles it changed. Measure, for 500 random edits on a 256 × 256 level, the bytes your history holds (use `sys.getsizeof` recursively or count stored integers × 8) against 500 full copies of the level.
7. **Change-only encoding.** Add a second recording format that stores `(tick: uint16, buttons: uint8)` only when the command changes. Compare its size with the one-byte-per-tick format for the scripted player, then for a player you write who holds each direction for 2 seconds and fires in bursts.

## Deliverable

Your `lab12.py` passing all seven self-checks plus your own tests for `FillRect` and the change-only format, a recording file `run.rep` that matches in `check`, and a report (600 to 800 words) with: the size predictions and measurements (steps 2 and 7), the bug table (step 3), the answer to step 4, the output of your bisect tool (step 5), and the memory comparison (step 6).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Deterministic replay | `check` matches every run; all self-checks pass | Matches in the same process only | Still desyncs | 30% |
| Bug analysis | All three bugs with line, corrupted state and mechanism; step 4 explained with the hashing cause | Bugs fixed, explanations partial | Bugs not identified | 20% |
| Size models | Predictions made before measuring and match to the byte; ratio stated; change-only format compared for both players | Measurements without predictions | Missing | 15% |
| Bisect tool | Per-tick checksums and a side-by-side state print at the first bad tick | Per-tick checksums only | Missing | 15% |
| Undo, redo and FillRect | All work, redo cleared on new command, FillRect stores only changed tiles, memory measured | Undo works, FillRect or measurement missing | Undo fails | 20% |

<details>
<summary>Instructor check values</summary>

- Recording size: 11 + 1,800 + 30 × 4 = **1,931 bytes**. Snapshots as described: 1,800 ticks × (2 + 5 × 4) values × 8 bytes = 316,800 bytes, about 164 times larger.
- The three bugs: (1) `measured_dt()` in the step loop, a wall-clock timestep that corrupts position; (2) `random.random()` from the unseeded global generator for the hit roll, which corrupts kills and hp; (3) `self.alive` is a `set` of strings and the target is `next(iter(self.alive))`, so the chosen target depends on per-process string hashing. Harmless tagged lines: the `dx` computation, `self.rng.randrange(4)` (seeded, same process and version) and the `for n in NAMES` loop in `checksum` (a list, fixed order).
- With only the timestep and global-RNG bugs fixed, the same-process test passes and `check` still fails at second 1. That is bug 3, visible in one process with `PYTHONHASHSEED` set to different values for record and replay.
- Fully fixed with `alive` as an insertion-ordered dict or list: every run gives 1,931 bytes, 53 kills, final position (180.000, −300.000), and `MATCH` on all 30 checksums. A student who instead picks the target from `sorted(self.alive)` also gets a deterministic replay, but with a different kill count; accept it if every run agrees.
- Extra credit if a student notes that `randrange` is not covered by Python's cross-version reproducibility guarantee (only `random()` is), so a replay file from another Python version could desync; the version byte should then include the Python version.

</details>
