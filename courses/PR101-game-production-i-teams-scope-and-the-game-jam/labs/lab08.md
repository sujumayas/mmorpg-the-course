# PR101 · Lab 08: The jam

**Week:** 8 ([The 48-hour game jam](../lectures/w08-48-hour-game-jam.md))
**Time:** 48 hours, in the lab, from 17:00 on the first day of jam week
**Work:** in your jam teams

## Objective

Make and ship a game in 48 hours, and keep the production evidence that lets you learn from it. The game is assessed as the course's jam game assignment (30%). This lab grades the evidence: a tagged build that runs on a machine it wasn't made on, a complete jam log, the board at each checkpoint, and a record of your freeze decision. Lab 09 analyses the log.

## Starter materials

- Your lab 07 outputs at the `jam-plan` tag: `tasks.csv`, `dod.md` and the seeded `jam_log.csv`. Re-run lab 07's script after the theme is announced, because your cards will change.
- [`lab08-starter/check_log.py`](lab08-starter/check_log.py): checks the jam log format. It rejects a wrong header, hours that aren't checkpoints (0, 6, ..., 48), a first row with time already spent, spent hours that go down, rows after a `done` or `cut` row, unknown statuses, and a `done` row with remaining hours.
- [`lab08-starter/jam_log_template.csv`](lab08-starter/jam_log_template.csv): a three-task example log that passes. Task T01 is the one the week 9 lecture works through by hand.
- The interactive [`examples/w08-feature-freeze.html`](../examples/w08-feature-freeze.html), for the freeze decision.

From the `lab08-starter` folder:

```
python check_log.py jam_log_template.csv
python check_log.py ../../<your repo>/jam_log.csv
```

## Steps

### Hour 0 to 2: plan

1. Theme announced. Write the one-pager with an MVP sentence (week 4).
2. Replace your lab 07 card list with cards for the jam game. Rerun lab 07's `check_board.py` with `--seed` to rewrite `jam_log.csv`. Put the cards on the board.
3. Name the build owner. Write your freeze hour and content-lock hour on the board (from the week 8 in-class activity).
4. Tag the empty project `jam-start`.

### Every six hours: log

5. At hours 6, 12, 18, 24, 30, 36, 42 and 48, the producer collects `spent` and `remaining_est` from each owner for every open card and adds one row per card. Add a `done` or `cut` row for any card that reached Done or was cut since the last checkpoint. New cards get a first row at the checkpoint where they were created.
6. Run `check_log.py` at hour 24 and again before submission. Fix any problem it reports on the spot.
7. At hours 12, 24, 36 and 42, photograph or screenshot the board.

### Checkpoints: decide

8. Apply week 4's cut triggers at hours 12 and 24, and write down each decision in one line (what was cut, or "no cut, because ...").
9. From your freeze hour on, tag every build that works (`jam-good-1`, `jam-good-2`, ...) after someone has played it for two minutes. Record every change made after the freeze: what, who approved it, and whether the build still ran.

### Hour 44 to 48: ship

10. At hour 44, tag `v0.1.0-rc.1`, build from a fresh clone of that tag, and play the build on a machine that isn't the build owner's. If it fails, fix, tag `rc.2`, repeat.
11. Tag the submitted commit `v0.1.0`. Zip the build with the version in the file name.
12. Submit before hour 46. The hard close is hour 48.

## Deliverable

Submitted through the course page by hour 48:

- The zipped build (`<team>-v0.1.0.zip`), which runs on a lab machine or in a browser without the engine installed, and has a credits screen listing every person and every third-party asset with its licence.
- The repository link with tags `jam-start`, any `jam-good-*`, `v0.1.0-rc.*` and `v0.1.0`.
- `jam_log.csv`, passing `check_log.py`, with a row for every card at every checkpoint while it was open.
- Board images at hours 12, 24, 36 and 42.
- The one-pager.
- A freeze record, one paragraph: when you froze, what the cut-trigger decisions were, every post-freeze change with its reason, and whether you would move the freeze next time and why, using the week 8 model.

## Rubric

This rubric covers the production evidence. The game itself is graded under the jam game assessment.

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Build ships (30%) | `v0.1.0` tag builds the submitted zip; runs on a clean machine first time; credits complete | Runs after a minor fix by the marker (a missing runtime noted in the readme) | Runs only in the editor or needs team help | Not submitted or does not run |
| Jam log (30%) | Passes the checker; every open card has a row at every checkpoint; no 0-remaining rows on unfinished cards, or each one explained | Passes; a few checkpoints missing for some cards | Fails the checker, or many gaps | Missing |
| Checkpoint evidence (20%) | Four board images; every cut-trigger decision written with its reason | Images present; decisions brief | Some images or decisions missing | Missing |
| Freeze record (20%) | Every post-freeze change listed with outcome; the freeze reflection uses `F` and `q` from the team's own jam | Changes listed; reflection general | Record incomplete | Missing |

The log is graded on completeness, never on estimate accuracy. A task that took four times its estimate, honestly logged, earns full marks.
