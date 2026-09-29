# PR401 Lab 01: Pitch sheet, content budget and claims

**Week:** 1 (Pitch development). **Guide:** [week 1](../lectures/w01-pitch-development.md). **Team lab**, submitted once per team.

## Objective

Turn your chosen pitch into numbers a greenlight panel can check. You will compute how many one-pass content hours your team can author before the PR402 launch, how long each type of player takes to run out of content during the four-week live period, and which replay multiplier the pitch depends on. You will then write the pitch's claims, tag each with its evidence level, and mark the ones the pitch cannot survive without.

## Starter materials

In [`labs/lab01-starter/`](lab01-starter/):

- `check_pitch.py`. Standard library only. Run it with `.venv/bin/python check_pitch.py pitch.csv claims.csv`. It prints plannable hours, one-pass content `C`, and `T`, `L` and `r_needed` for four player types. It ends with `PASS` or `NOT READY` and exits with code 1 when anything fails.
- `pitch.csv`. The *Emberfall* pitch from section 2 of the guide, as key, value, note rows.
- `claims.csv`. Six example claims for *Emberfall*. One has no owner and the sheet is too short, so the starter prints `NOT READY` on purpose.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. Confirm the *Emberfall* column of the guide's table. Change `content_share` to 0.40 and `replay` to 1.5 and confirm the *Lanternfall* column and the `FAIL: median L = 1.62` line. Change them back.
2. **Your capacity.** Set `team_size` to your team. Keep `hours_per_week = 12` and `weeks = 8` unless your charter agrees different PR402 hours. Record any change in the note column.
3. **Your content share.** List the pitch's work in three buckets: authored content, systems, and everything else (tools, networking, UI, polish). Set `content_share` to the authored bucket's share of the team's estimated hours.
4. **Your `k` and `r`.** Keep `authoring_ratio = 20` unless you have your own PR301 measurement. Set `replay` to what the pitch claims, and write in the note column why you believe it.
5. **Player types.** Keep the course percentiles, or replace them with play-time data from your PR301 playtest if you logged it. Say which in the note column.
6. **Run both pitches.** Save the output for your chosen pitch as `check-output.txt` and for the rejected one as `check-output-rejected.txt`.
7. **Claims.** Replace the starter claims with 8 to 15 of your own. Merge in the claims another team heard during the two-pitch round. Every claim has an evidence level (`assumed`, `estimated`, `tested`), a load-bearing flag (`yes`, `no`) and an owner.
8. **The replay claim.** Make sure one claim states the `r_needed` value for your median player as a threshold, as C1 does in the starter. It becomes risk R1 in lab 04.

If your median `L` is above 1 and you choose to keep the pitch anyway, write the reason in `median_L_accepted`. The checker then passes, and the reviewer reads the reason.

## Deliverable

In `preproduction/week01/` in the team repository:

- `pitch.csv`, `check-output.txt` and `check-output-rejected.txt`.

In `docs/`, because later weeks keep updating them:

- `claims.csv`.
- `pitch.md`, the pitch draft (two pages plus the numbers appendix) described in the guide's Deliverables section.

**Checkable output:** the instructor reruns `check_pitch.py pitch.csv claims.csv`. It must print `PASS` and exit with code 0, and its output must match `check-output.txt`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; saved output matches |
| Capacity inputs | 3 | Team size and hours match the charter; every changed default has a note |
| Content share | 3 | The three-bucket split is shown and adds up to the team's estimate |
| Replay claim | 4 | `r` has a stated source; the `r_needed` threshold appears as a load-bearing claim with an owner |
| Claims sheet | 4 | 8 to 15 real claims (not tasks); evidence levels are honest; claims from the outside team are included |
| Rejected pitch | 2 | Its output is saved and the reason it lost is one clear sentence |
