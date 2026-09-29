# PR201 Lab 14: Release candidate fix log and go/no-go

**Week:** 14 (Release candidate). **Guide:** [week 14](../lectures/w14-release-candidate.md). **Team lab**, submitted once per team.

## Objective

Decide, bug by bug, what enters your release candidates and what ships as a known issue, using regression rates measured from your own tracker. The output is a fix log that a script checks against the course's RC rules, a known issues list written for players, and a go/no-go record naming the build you will submit.

## Starter materials

In [`labs/lab14-starter/`](lab14-starter/):

- `check_rc.py`. Standard library only. Run `.venv/bin/python check_rc.py rates.csv fixes.csv`. It computes `r` for each change type, groups your fixes by RC, prints `P(no regression)`, expected new defects and expected escapes per RC (catch rate 0.7 by default, change with `--catch`), and checks the rules below. It prints `PASS` or `NOT READY` and exits with code 1 on `NOT READY`.
- `rates.csv`. One row per change type (netcode, gameplay, ui, art, audio, data, config) with `fixes` and `regressions` empty. `config` is the rate used when you remove or switch off a feature.
- `fixes.csv`. Hollowmarch's nine bugs from the guide with the decisions empty.

Rules the script enforces:

- Every bug has a change type with a rate and a decision: `fix`, `remove` or `known`.
- No P1 ships as `known`.
- Every `fix` or `remove` names its RC, an author and a reviewer who is not the author.
- An RC holds at most one high-risk change (`r ≥ 0.3` by default, change with `--high`).

## Steps

### Part A: measure `r` (30 minutes)

1. **Warm-up.** Fill `rates.csv` so each type gives the guide's rate (for example netcode 7 regressions in 18 fixes gives 0.39), then make decisions in `fixes.csv` that reproduce the guide's suggested plan: F1, F2 and the four low-risk fixes in `rc.2`, F3 alone in `rc.3`, F5 and F7 as known issues. Run the script until it passes. `rc.2` should show about 42% `P(no regression)`.
2. **Your rates.** Replace `rates.csv` with counts from your tracker for sprints 3 and 4. A regression is a fix that was reopened or that a later ticket names as its cause. Put the query in `source`. If a type has no fixes, use `default_r` (0.2 for code, 0.4 for anything touching network timing, 0.02 for text, data or config) and say why in `source`.

### Part B: decide (30 minutes)

3. **Classify.** List every open bug in `fixes.csv` with priority and change type. When a bug could be fixed two ways (for example code fix or switching the feature off), pick the one you will do and note the other in `rc-decisions.md`.
4. **Decide.** Set each decision. Take P1s first. Then add low-risk changes. Treat every remaining high-risk change as its own decision, and write one sentence per high-risk change in `rc-decisions.md` saying why you took it or left it.
5. **Assign.** For every change, name the author (ideally the person who wrote the original code) and a reviewer.
6. **Run the script** until it prints `PASS`. Save the output as `rc-output.txt`.

### Part C: ship (rest of the week)

7. **Known issues.** Write `KNOWN_ISSUES.md` for players: what they will see, how to avoid it, ticket number. One line per `known` bug and per removed feature.
8. **Build each RC** from a clean checkout of its tag and run the RC checklist from PR101 week 13 on it. Record any regression you find as a new ticket, and add it to `fixes.csv`.
9. **Go/no-go.** Write the rule before the meeting in `go-no-go.md`. Record the meeting: date, who attended, each checklist owner's answer, the decision, and the tag of the RC that passed.
10. **Post-mortem data.** Commit the exports listed in guide section 5 to `production/postmortem-data/`.

## Deliverable

In `production/week14/`: `rates.csv`, `fixes.csv`, `rc-output.txt`, `rc-decisions.md`, `KNOWN_ISSUES.md` (also copied into the build), `go-no-go.md`. In `production/postmortem-data/`: the exports.

**Checkable output:** the instructor reruns `check_rc.py` on your two CSV files. It must print `PASS` and exit with code 0. The tag in `go-no-go.md` must exist and match the submitted build's version string.

## Rubric (25 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Measured rates | 5 | Rates come from tracker counts with queries; defaults labelled and justified |
| Decisions | 6 | P1s fixed or removed; low-risk fixes taken; each high-risk change argued in one sentence; removal considered where it is safer |
| Known issues list | 3 | Written for players, matches the tracker, includes removed features |
| Go/no-go | 4 | Rule written before the meeting; record complete; RC tag matches the submitted build |
| Post-mortem data | 3 | Tracker export, sprint boards, review sheets, soak log and RC decisions committed |
