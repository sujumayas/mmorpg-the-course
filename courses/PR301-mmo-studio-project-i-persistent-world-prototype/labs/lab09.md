# PR301 Lab 09: Alpha weekend ops sheet

**Week:** 9 (Alpha: the first persistent weekend). **Guide:** [week 9](../lectures/w09-alpha-first-persistent-weekend.md). **Team lab**, submitted once per team by the Thursday freeze.

## Objective

Get the world and the team ready to run for 48 hours without a lecturer in the room. You size the sign-up target from stated rates, cover every hour of the weekend with an on-call person and a backup, and write a runbook that someone other than its author can follow at 3 am.

## Starter materials

In [`labs/lab09-starter/`](lab09-starter/):

- `check_weekend.py`. Standard library only. Run it with `.venv/bin/python check_weekend.py sizing.txt rota.csv runbook.md`. It applies the guide's hand model to your rates, prints the sign-ups needed and the humans expected at the event, checks that the rota covers all 48 hours with no shift over six hours, and checks that the runbook has a heading for each required action. Then it prints `PASS` or `NOT READY` (exit code 1).
- `sizing.txt`. The guide's rates, with the sign-up figure left blank.
- `rota.csv`. A sample rota with one shift that is too long and a six-hour gap on Sunday night.
- `runbook.md`. A runbook skeleton missing two required sections.

## Steps

### Part A: sign-ups (30 minutes)

1. Run the checker on the starter files and read its complaints. Fill `signups_claimed` with the guide's figure (55) and check that the model agrees.
2. Replace the rates with your team's. Use the class playtest in week 8 for session length if you have nothing better, and mark every rate in `ops/alpha-weekend.md` as measured or guessed.
3. At the board, agree your event hour with the other teams so that no two events share an hour. Record the agreed schedule.
4. If `signups_planned` is below the model's figure, say in the ops plan how bots or a higher attendance cover the gap. Either way, say how many bots you will run to reach your week 2 load-test crowd at the event.

### Part B: rota

5. Fix the starter rota, then write your own. Every hour from Friday 18:00 to Sunday 18:00 has a primary and a different backup. No shift is longer than six hours. Night shifts say "alarm wakes me" in the ops plan if that is the arrangement.
6. Trigger one real alarm (stop the server's health endpoint for 60 seconds) and record who received it and when.

### Part C: runbook and consent

7. Complete the runbook with sections for start, stop, restart, restore, kill switches, hotfix deploy, hotfix roll back and contacts. Every step is a command. Have the teammate who knows the server least run the restart and restore sections on Tuesday, and fix whatever they got stuck on.
8. Write the tester consent notice: what data you collect, why, who can see it, and the deletion date. Show it before first login.
9. Run the checker until it prints `PASS`.

## Deliverable

In `production/week09/` and `ops/` in the team repository:

- `sizing.txt`, `rota.csv` and `runbook.md` that pass `check_weekend.py`, with its output saved as `check-output.txt`.
- `ops/alpha-weekend.md`: rates marked measured or guessed, the agreed event schedule, the bot plan, the alarm test record, the dashboard link and the incident log template.
- The consent notice text and deletion date.

**Checkable output:** the instructor reruns `check_weekend.py` on your three files. It must print `PASS` and exit with code 0. During the weekend, the instructor may message the on-call channel at a random hour and expects a reply within 15 minutes.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 3 | `PASS` on rerun, output file matches |
| Sign-up sizing | 4 | Rates stated and marked measured or guessed; gap to target covered by a stated plan; event hour coordinated |
| Rota | 3 | Full coverage, backups, alarm test recorded |
| Runbook | 5 | Every section is copyable commands; restart and restore run by a non-author, with fixes made |
| Consent and data | 3 | Notice shown before login; data, purpose, access and deletion date named; no personal data in shared files |
| Weekend conduct | 2 | Incident log has an entry every shift; spot-check message answered within 15 minutes |
