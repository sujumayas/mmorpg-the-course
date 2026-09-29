# AU101 · Lab 01: Sound audit

**Week:** 1, what sound does in games ([lecture](../lectures/w01-what-sound-does-feedback-space-emotion.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** formative, feeds the SFX pack (30%). You will redesign the three highest-cost sounds from this audit in that assignment.

## Objective

Log every sound event in a stretch of play from a shipped game, label each one with its job and trigger, and use the numbers to say what the game's audio carries that its visuals do not.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python, no installs.

- [`audit_template.csv`](lab01-starter/audit_template.csv), the header row only. Open it in any spreadsheet program and save as CSV (UTF-8).
- [`sample_audit.csv`](lab01-starter/sample_audit.csv), five filled rows showing the format. It fails the checker on purpose because it has fewer than 40 events.
- [`check_audit.py`](lab01-starter/check_audit.py), a checker that validates your sheet and prints the summary numbers your memo must quote. Run it from the repository root:

```
.venv/bin/python courses/AU101-audio-for-games/labs/lab01-starter/check_audit.py my_audit.csv
```

- Any game you own, or a gameplay video with original audio and no commentary. Headphones.

## Steps

1. **Choose a stretch.** Pick 10 to 15 continuous minutes that include movement, at least one fight or threat, and at least one menu or inventory action. Write down the game, platform, version or patch date, and where the stretch starts.
2. **Log it.** Play or watch once without writing, then again pausing as needed. Add one row per distinct sound event. Repeated identical events in quick succession (a burst of footsteps) count as one row with a note.
3. **Label every row** with the columns from lecture section 4:
   - `time` as `mm:ss`, never going backwards.
   - `event`, a plain description.
   - `on_screen`, `yes` or `no`.
   - `job`, one of `feedback`, `space`, `emotion`. Optional `second_job`, a different one of the three.
   - `feedback_kind`, one of `confirm`, `report`, `forecast`, filled only when `job` or `second_job` is `feedback`.
   - `diegetic`, `yes` or `no`.
   - `trigger`, `input` (the player did something) or `state` (the game changed).
   - `mute_cost`, `1` (no loss muted), `2` (some loss) or `3` (a muted player would miss something that matters).
   - `notes`, free text.
4. **Validate.** Run the checker until it prints `OK`. You need at least 40 events.
5. **Mute test.** Replay a 3-minute part of the same stretch with sound off. Mark in `notes` every row where you would have acted differently without sound.
6. **Direction test.** For five off-screen sounds, write the clock-face direction you heard (12 ahead, 6 behind) before checking the screen. Record the true direction. Count front-back swaps.
7. **Pick three.** Choose the three rows with `mute_cost` 3 that you consider worst served (hard to hear, hard to place, or with no visual twin). These go into the SFX pack.

## Deliverable

1. Your CSV, passing the checker.
2. A memo of about 500 words that:
   - quotes at least four numbers from the checker's summary (for example `off_screen_pct` and `forecast_pct_of_feedback`) and says what each tells you about the game;
   - reports the mute test and the direction test, including the number of front-back swaps;
   - names your three chosen sounds and, for each, the job it does and one concrete fix (a stronger cue, a symbolic code, or a visual twin).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Audit completeness | 40+ events, checker passes, stretch and version stated | Checker passes, stretch vague | Checker fails or under 40 events | 25% |
| Labelling accuracy | Jobs, kinds and triggers defensible on spot check of 5 rows | 1-2 rows mislabelled | 3+ rows mislabelled | 20% |
| Use of numbers | Four or more summary numbers quoted and interpreted | Numbers quoted without interpretation | No numbers | 20% |
| Mute and direction tests | Both done, swaps counted, linked to the cone of confusion | One test done | Neither | 15% |
| Three redesign picks | Each has job, problem and concrete fix | Fixes vague | Missing | 20% |
