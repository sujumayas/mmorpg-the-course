# PR101 · Lab 13: Release checker and a dry-run release

**Week:** 13, builds and release checklists ([lecture](../lectures/w13-builds-and-release-checklists.md)).
**Time:** 2 hours in lab, plus up to 2 hours with your team before week 14.
**Weight:** part of the final team game (40%). The checklist and the checker script are graded as part of your week 15 release.

## Objective

Finish a small script that automates the yes-or-no lines of a release checklist, then use it together with a written checklist to do a full dry-run release of your final game to a private itch.io page. By the end you can show, with your own team's list, which failure items you automated, which you deleted, and which still need a human, and what that did to the model's `P(clean)`.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Standard-library Python 3.10 or later, no packages. From the repository root the course uses `.venv/bin/python`.

- [`release_check.py`](lab13-starter/release_check.py). Five check functions and `release_risk`, each a stub that returns "pass". The runner `run_checks` and `main` are complete. Run `python release_check.py sample_build`. On the starter it reports `5/5 checks passed` on a build that is broken in four ways. That is the point. A checklist that checks nothing always passes.
- [`sample_build/`](lab13-starter/sample_build/). A fake build folder with `version.txt` (`1.0`, not valid SemVer), `last_release.txt` (`0.9.2`), a `CHANGELOG.md` with no entry for the new version, a `settings.cfg` with `show_fps=true`, and a `manifest.txt` that lists `assets/music/boss.ogg`, which isn't there.
- [`test_lab13.py`](lab13-starter/test_lab13.py). Nine tests. Run `python test_lab13.py`. On the starter it reports `1/9 tests passed`.

## Steps

1. **Run everything first.** Run the checker on `sample_build` and the tests. Write down the four problems you can see by opening the files yourself. Compare with the checker's all-green output.
2. **SemVer.** Implement `parse_version` from the docstring (lecture section 3). Test it by hand on `1.0.0-rc.10+a3f9c21`, `1.02.0` and `v1.0.0` before running the tests.
3. **Precedence.** Implement `is_newer`. The traps are that `1.0.0-rc.1` is older than `1.0.0`, that `rc.10` is newer than `rc.2`, and that equal versions are not newer.
4. **Changelog, debug flags, manifest.** Implement `changelog_has`, `debug_flags_on` and `missing_files`. Run `python release_check.py sample_build` and confirm it now reports `0/5 checks passed`, exits with code 1, and names `show_fps` and `assets/music/boss.ogg`.
5. **The model.** Implement `release_risk`. Run the tests until you see `9/9 tests passed`.
6. **Your team's failure list.** Take the list your team wrote in the in-class activity (at least 20 items). For each item, record a rough `p`, and mark it "automated", "deleted" or "human check" with a pass condition. Compute `P(clean)` with `release_risk` three times: no checks; your plan with automated items at `c = 0.99` and human checks at your honest guess; your plan after deleting items. Put all three in a table.
7. **Adapt the script to your game.** Copy `release_check.py` into your project's `tools/` folder. Point it at your real files: your version in the Godot project settings (`application/config/version`) or a `version.txt` your export script writes, your real debug settings, your real asset manifest. Add at least one check specific to your game (for example, "every scene listed in the level-select menu exists"). Make your export script run the checker and stop if it fails.
8. **Dry-run release.** Tag `v1.0.0-rc.1`. Clone the repository into a fresh folder, export from the command line with your script, run the checker, and upload with butler to a **restricted** (not public) itch.io page. Download it on a different machine and run your smoke test. Record how long each stage took and every problem you found.
9. **Fix and repeat.** Fix what the dry run found, tag `rc.2`, and run the whole sequence again. Record the times again.

## Deliverable

- Your edited `release_check.py` with `python test_lab13.py` reporting `9/9 tests passed` (individual).
- Team: `RELEASE_CHECKLIST.md` committed in your repository, with stage, check, owner, pass condition and "automated?" for every line (lecture section 4 format), and your game-specific checker in `tools/`.
- Team: a note of at most 400 words with the step 6 table, the step 8 and 9 timings, every problem the dry run caught, and the one item you think is still most likely to escape.
- A link to the restricted itch.io page with `rc.2` on it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 9/9 | 7-8 | 6 or fewer | 20% |
| Failure list and model (step 6) | 20+ items covering every system; three `P(clean)` values computed and explained; deleted items named | List present, model partly applied | Short list or no numbers | 20% |
| Checklist quality | Every line has an owner and a pass condition another person could verify; stages separated; lives in Git | Most lines verifiable | Vague lines ("check audio") | 20% |
| Game-specific automation | Checker adapted to the real project, one new game-specific check, export script stops on failure | Checker runs on the project but not wired into the export | Not adapted | 20% |
| Dry-run release | Two full clean-checkout runs with timings, problems found and fixed, rc.2 downloadable on a second machine | One run, or no second-machine test | No upload | 20% |
