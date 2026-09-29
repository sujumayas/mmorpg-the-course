# PR101 · Lab 01: Team charter and RACI

**Week:** 1, roles on a game team ([lecture](../lectures/w01-roles-on-a-game-team.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home with your team.
**Weight:** part of the peer review component (10%) and the base document for the jam game (30%). The charter is reused in weeks 8, 9 and 11.

## Objective

Form a team of four, write the one-page team charter from lecture section 5, and back it with a RACI matrix and a coverage matrix that pass a checker. Then use the channel model from section 2 to justify your team size with your own estimate of coordination cost.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python 3.10 or later, no packages.

- [`raci_check.py`](lab01-starter/raci_check.py) checks both matrices. It fails (exit code 1) on any RACI row without exactly one A, any row with no R, any unknown letter, any skill nobody covers, and any skill marked critical with a bus factor of 1. It warns, without failing, when one person is A on more than half the rows or a non-critical skill has a bus factor of 1.
- [`raci.csv`](lab01-starter/raci.csv) is the lecture's four-person platformer team with three planted errors.
- [`coverage.csv`](lab01-starter/coverage.csv) is that team's coverage matrix with two planted errors.
- The [interactive](../examples/w01-team-channels.html) for the team-size step.

Run the checker from the `labs/` folder:

```
python lab01-starter/raci_check.py lab01-starter/raci.csv lab01-starter/coverage.csv
```

On the starter files it prints `5 error(s), 2 warning(s)` and exits with code 1.

## Steps

1. **Warm-up (15 min), fix the example.** Without looking at the checker output first, read `raci.csv` and `coverage.csv` and write down every problem you can see. Then run the checker. Compare. Fix all five errors with the smallest change that keeps the lecture's intent (for example, who should be A for "Menus and UI"?). Run the checker again until it reports `0 error(s)`. Keep a one-line note per fix.
2. **Coverage (20 min).** Copy `coverage.csv` to `team/coverage.csv`. Replace the people with your team and list at least 8 skills your semester project needs. Mark at least three as critical, and "Export a build" must be one of them. Mark honestly. "Could learn it in a weekend" is not "yes".
3. **RACI (25 min).** Copy `raci.csv` to `team/raci.csv`. Write at least 8 deliverables for your first milestone (a playable one-screen prototype in week 4). Assign letters. Run the checker on your two files until there are no errors.
4. **Fix the warnings you can.** For each remaining bus-factor-1 warning, either plan a pairing session (who, when, one hour) or write one sentence on why the team accepts the risk.
5. **Team size (15 min).** Each teammate estimates, alone, how many hours per teammate they would spend on coordination (talking, waiting, redoing) over a 48-hour jam. Take the median as your team's `c`. Compute `n* = (H + c) / (2c)` with `H = 30`, and useful capacity at `n = 3, 4, 5`. Check the numbers in the interactive.
6. **Charter (at home).** Write the one-page charter answering the six questions in lecture section 5. Include your `c`, `n*` and the capacity numbers from step 5, and one sentence on whether they support a team of four.
7. **Sign.** Every team member adds their name and the date at the bottom of the charter.

## Deliverable

A folder `lab01-<teamname>/` in your team's shared drive (from week 2, your repository) containing:

- `fixes.md`, the five warm-up fixes, one line each.
- `team/raci.csv` and `team/coverage.csv`, passing `raci_check.py` with `0 error(s)`. Paste the checker output at the top of the charter.
- `charter.md`, at most one page (about 500 words) plus the two tables, signed by all four members.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Warm-up fixes | All five fixed with the smallest change and a reason each | All fixed, reasons missing or changes larger than needed | Errors remain | 15% |
| RACI matrix | Passes the checker; deliverables are concrete and cover code, art, audio, build and QA; no bottleneck warning or it is justified | Passes the checker; some deliverables vague ("do the game") | Fails the checker | 25% |
| Coverage and bus factor | Honest marks, 8+ skills, every bus-factor-1 warning has a plan or a reasoned acceptance | Plans for some warnings | No plans; marks look inflated | 20% |
| Team-size reasoning | `c` from the median of individual estimates; `n*` and three capacities correct; clear conclusion about four | Numbers correct, conclusion missing | Numbers wrong or missing | 20% |
| Charter | Answers all six questions with rules specific enough to apply at hour 34 of a jam; signed by all | Answers most questions; some rules vague | Missing questions or unsigned | 20% |
