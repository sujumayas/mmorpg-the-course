# PR101 · Lab 03: Asset pipeline and LFS

**Week:** 3, asset workflows and large files ([lecture](../lectures/w03-asset-workflows-and-large-files-lfs.md)).
**Time:** 2 hours in lab, plus up to 1.5 hours at home.
**Weight:** part of the jam game component (30%). The asset setup you finish here is the one your team jams with.

## Objective

Implement the lecture's clone-size model and check it against real Git measurements. Then repair a repository where three weeks of art and audio were committed without LFS, and apply a correct asset setup to your team repository before anyone commits art to it.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python 3.10 or later, Git 2.28 or later, and git-lfs 3.x (`git lfs version` should print a version).

Part A:

- [`repo_model.py`](lab03-starter/repo_model.py) has six empty functions: `pointer_size`, `is_lfs`, `history_bytes`, `lfs_server_bytes`, `clone_bytes` and `clone_minutes`. The docstrings define each one.
- [`test_repo_model.py`](lab03-starter/test_repo_model.py) has six tests built from the lecture's numbers (the 132-byte pointer, the 200-asset semester project at week 8, the jam weekend at 10 Mbps, and a project that forgot to track `*.ogg`). On the starter it prints `0/6 tests passed`.
- [`measure_history.py`](lab03-starter/measure_history.py) commits several versions of one binary file into a throwaway repository, packs it, and prints the packed size, once with fully re-randomized versions and once with 10-byte edits.

Part B:

- [`setup_lab03.py`](lab03-starter/setup_lab03.py) builds `lab03-repo/`, three weekly commits of a small game with 8 PNGs, 2 WAVs and a PSD, all committed without LFS. About 23 MiB of Git objects.
- [`check_lab03.py`](lab03-starter/check_lab03.py) runs 11 checks. On a fresh `lab03-repo` it prints `2/11 checks passed`.

Run everything from inside `lab03-starter/` (so `import repo_model` works), for example `python test_repo_model.py`.

## Steps

### Part A, model and measurement (50 min)

1. **Implement the model.** Fill in `repo_model.py` until `python test_repo_model.py` prints `6/6 tests passed`. Build the pointer text from `POINTER_TEMPLATE` rather than hard-coding 132. Then run `python repo_model.py` and check the output against the lecture's table for week 8.
2. **Measure.** Run `python measure_history.py`, then `python measure_history.py 12` and `python measure_history.py 6 8000000`. Record the six packed sizes in a table.
3. **Compare.** For each run, compute the model's prediction for the resave case (`versions × size`, in KiB) and the percentage error of the measurement. Then explain in two or three sentences why the patch case doesn't match the model and what kind of real asset edit behaves like it.

### Part B, repair a repository (40 min)

4. **Build and inspect.** Run `python setup_lab03.py` and `python check_lab03.py lab03-repo`. In `lab03-repo`, run `git count-objects -vH` and record the size. Set your name and email there with `git config user.name` and `git config user.email`.
5. **Predict first.** Use your `repo_model.py` to predict the Git history size of this repository before and after moving the four binary patterns to LFS. The assets are listed in the docstring of `setup_lab03.py`. Write the numbers down before you run anything.
6. **Migrate history.** Run `git lfs install --local`, then `git lfs migrate import --yes --everything --include="*.png,*.wav,*.ogg,*.psd"`. This rewrites every commit so that binaries become pointers, and writes a `.gitattributes`. Run `git show HEAD:art/sprites/enemy_0.png` and confirm you see a pointer.
7. **Make source files lockable, then clean up.** Run `git lfs track --lockable "*.psd"` and commit the changed `.gitattributes` with a good message. The old binary objects are still on disk, kept alive by the reflog. Remove them with `git reflog expire --expire=now --all` and then `git gc --prune=now`. Run `git count-objects -vH` again and `du -sh .git/lfs` (or check the folder size in your file manager).
8. **Check.** Run `python check_lab03.py lab03-repo` until it prints `11/11 checks passed`.
9. **Explain the two numbers.** The Git object store dropped from about 23 MiB to a few KiB, but `.git/lfs` holds about 23 MiB. Which quantity in the lecture's model does each number correspond to? What would a fresh clone from a server download?

### Part C, your team repository (30 min, with your team)

10. **Before any art is committed**, add LFS tracking to your team repository for every binary type in your in-class list, with source formats marked lockable. Commit `.gitattributes` on its own with a clear message.
11. **Test locking.** One teammate locks a lockable file with `git lfs lock <path>`, another runs `git lfs locks` and tries to push a change to it. Record what happens. If your host doesn't support LFS locking, record the error and write the manual rule your team will use instead.
12. **README.** Add a "Setup" section with `git lfs install` and a "Assets" section with your folder layout, naming rule, export settings and the lock rule ("lock before you open, unlock after you push, the RACI owner may break a stale lock after messaging the holder").

## Deliverable

- `repo_model.py` passing `6/6` tests, and a short report of at most 400 words with the part A measurement table, errors against the model and the step 3 explanation.
- The step 5 predictions next to the measured sizes from steps 4 and 7, the `11/11` checker output, and the step 9 answer.
- A link to your team repository showing the `.gitattributes` commit made before the first binary commit, the README sections from step 12, and one sentence on the locking test from step 11.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model code | 6/6 tests pass; pointer size computed from the template; readable | 6/6 pass with hard-coded constants | Fewer than 6 pass | 25% |
| Measurement and comparison | Six measurements, errors computed, patch case explained by what changes inside the file | Measurements and errors, explanation vague | Measurements missing | 20% |
| Repository repair | 11/11 checks; predictions made before measuring and compared; step 9 names the model terms correctly | 11/11 checks, predictions or step 9 weak | Checker fails | 25% |
| Team setup | `.gitattributes` committed before any binary; lockable source formats; locking tested or a manual rule written | Tracking set up after some binaries, or locking untested | No LFS in the team repository | 20% |
| README conventions | Folder layout, naming, export settings and lock rule concrete enough for a new teammate to follow | Some sections vague | Missing | 10% |
