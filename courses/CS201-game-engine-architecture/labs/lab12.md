# CS201 · Lab 12: A save system that survives patches

**Week:** 12 ([Serialization and save files](../lectures/w12-serialization-and-save-files.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; in Part C you swap save files with a neighbor

## Objective

Build the engine's save pipeline and then try to break it with patches. You will write the migration chain from the lecture, a header that detects truncation and corruption, a two-pass loader that restores references by persistent ID, and a write that never leaves a half-written file behind. Then you will ship three format changes of your own, add a golden file for each, and prove that a save from every version still loads. By the end you should be able to show a producer, with a test run, that no player's save from any past patch is lost.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`lab12-starter/save_system.py`](lab12-starter/save_system.py). The two shipped migrations (`v1_to_v2` renames `hp`, `v2_to_v3` converts tiles to pixels), the `Entity` class and the header layout are finished. You write `upgrade()`, `pack()`, `unpack()`, `to_save()`, `from_save()`, `write_save()` and `read_save()`. Each docstring is the specification.
- [`lab12-starter/golden/`](lab12-starter/golden/v1.json). One real save per shipped version (`v1.json`, `v2.json`, `v3.json`). They include a reference cycle, a forward reference and a target that no longer exists. Do not edit them. That is the point of golden files.
- [`lab12-starter/test_save_system.py`](lab12-starter/test_save_system.py). Run `python test_save_system.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w12-save-migration-chain.html`](../examples/w12-save-migration-chain.html).

## Steps

### Part A: the pipeline (70 minutes)

1. Write `upgrade()`. It must not mutate its input, must set `version` after each step, and must refuse both a save newer than `CURRENT` and a chain with a missing link, naming the version in the message. Checks 1a and 1b load all three golden files.
2. Write `pack()` and `unpack()`. Check 2 flips a byte, truncates the file, replaces the magic number and passes a blob shorter than the header. Then explain in two sentences why the version sits in the header as a fixed-width field and not only inside the JSON payload. Think about a future patch that changes the payload encoding.
3. Write `to_save()` and `from_save()` with the lecture's two passes. Checks 3a and 3b cover a cycle, a backward reference (the merchant in `v2.json` targets the player listed before it), a forward reference (the player in `v3.json` targets the wolf listed after it) and a dangling target (uid 999).
4. Write `write_save()` and `read_save()`. The write goes to a `.tmp` file with `fsync`, moves any existing save to `.bak`, then renames with `os.replace`. The read falls back to `.bak` when the main file fails to unpack. Checks 4a and 4b simulate a crash that truncates the main file.

### Part B: measure the cost of age (20 minutes)

5. Make 10 identity migrations `v3 → v4` through `v12 → v13` (each only bumps the version) in a local copy of `MIGRATIONS`, and time `upgrade()` on a v1 save with 10,000 entities (repeat `v1.json`'s entities with new uids). Report the time per migration step and per entity. Using the lecture's model, how long would a save 40 versions old take to load? Would you write the upgraded save back immediately after loading, or at the next normal save? Give one reason for each choice.

### Part C: ship three patches (at home)

6. Ship version 4. Items become stacks: `"items": ["bread", "bread"]` becomes `"items": [{"template": "bread", "count": 2}]`, in order of first appearance. Write `v3_to_v4`, bump `CURRENT`, update `to_save` and `from_save`, and add `golden/v4.json` written by your own game.
7. Ship version 5. Health becomes a fraction of a new `max_health`, which is 50 for players and 20 for everything else in old saves.
8. Ship version 6. The kinds `"merchant"` and `"trader"` merge into `"vendor"`. Any entity whose target was a merged entity keeps its target.
9. Add a test to `test_save_system.py` that loads every file in `golden/` and checks that each upgrades to `CURRENT` and round-trips through `pack`, `unpack`, `from_save` and `to_save` unchanged. Then swap your `golden/v6.json` with a neighbor's and load theirs with your code. Report what happened and why.
10. For each of your three patches, say in one sentence whether Protocol Buffers-style tagged fields could have handled it without a migration.

## Deliverable

Your completed `save_system.py` at version 6, the `golden/` folder with six files, and `test_save_system.py` with your added test, all passing (paste the output). Also a PDF with the step 2 answer, the step 5 measurements and write-back decision, the step 9 swap report and the step 10 sentences.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Pipeline correct (35%) | All seven checks pass; clear code that follows the docstrings; step 2 answer explains why the version belongs in the header | All checks pass, step 2 answer vague | Chain and header work, references or safe write fail | Missing or broken |
| Patches (30%) | Three migrations correct and frozen; six golden files; the all-goldens test passes; merged kinds keep their references | Three migrations, one edge case wrong (order of stacks, max_health by kind, or references) | One or two patches | Missing |
| Measurement (15%) | Per-step and per-entity times, 40-version estimate from the model, write-back choice argued both ways | Numbers and estimate, one-sided argument | Numbers only | Missing |
| Swap and judgment (20%) | Swap result explained (version refused, or loaded, and why); tagged-field sentences correct for all three patches | Swap reported, one sentence wrong | Swap not explained | Missing |
