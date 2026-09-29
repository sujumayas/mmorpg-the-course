# PR101 · Lab 05: One sprint, measured

**Week:** 5, agile and Scrum ([lecture](../lectures/w05-agile-and-scrum-adapted-for-games.md)).
**Time:** a one-week sprint. Two hours in lab for planning and the review, plus the team's normal project hours during the week.
**Weight:** part of the peer review component (10%) and the jam game component (30%). Your measured `h` and `λ` set the sprint length for weeks 6 to 7 and the build-and-play cycle for the week 8 jam.

## Objective

Run one complete one-week sprint on your week 4 prototype, with every Scrum event and artifact from lecture section 1. Measure the sprint's real overhead `h` and count its wrong turns to estimate `λ`. Use the model from lecture section 2 to choose the sprint length for your next two sprints and your jam cycle, and defend the choice.

## Starter materials

Everything below is in this file, plus your lab 04 scope sheet and the [sprint-length interactive](../examples/w05-sprint-length.html).

**Sprint record template.** Keep it in your repository as `sprints/sprint-01.md`.

```
Sprint 01, <start date> to <end date>
Product Owner: <name>     Scrum Master: <name>
Sprint Goal (one sentence; a question in pre-production):
Sprint Backlog (task, owner, estimate):
Definition of Done for this sprint (3-5 checkable lines):

Standup log (one line each: date, time taken, blockers raised, decisions)
Review: date, who played (at least 2 people outside the team), what they did,
        what the team decided to change, backlog items added/removed/reordered
Retrospective: start / stop / continue notes, the ONE change, its owner,
               how you will check it happened
Overhead log (see below)
Wrong-turn log (see below)
```

**Overhead log.** Record every minute spent on sprint machinery, per person: making the build playable on a second machine, planning, standups, the review, the retrospective. Do not count feature work. Sum to team-hours. Mark which items would shrink if the sprint were shorter (standups add up per day) and which would not (making a clean build, the review setup). Only the second kind is `h` in the model.

**Wrong-turn log.** Each time the team decides to redo, remove or significantly change work because of something a playtest or the review showed, write one line: what was built, how many team-hours it had taken, and what showed it was wrong. Count the lines. That count divided by the sprint length in weeks is your first estimate of `λ`.

## Steps

1. **Plan (lab, 45 min).** The Product Owner orders the backlog from your lab 04 task list. Write a Sprint Goal. If your core mechanic still hasn't been tested with outsiders, the goal must be a question (lecture section 3). Pick the sprint backlog by capacity: use your charter's weekly `W` with a 25% buffer, and stop at the first task that doesn't fit. Write a Definition of Done for this sprint.
2. **Standups (during the week).** Hold at least three, each at most 15 minutes, at the same time each day you meet. Log each one. Any blocker gets two names and is discussed after the standup, not during.
3. **Keep the logs.** Fill the overhead log and the wrong-turn log as you go, not at the end.
4. **Review (lab, 30 min).** At least two people from outside your team play the build without help. Watch silently (GD101 week 7). Afterwards, change the backlog: add, remove or reorder at least one item based on what you saw, and record why. A review that changes nothing must say why nothing needed to change.
5. **Retrospective (lab, 20 min).** Run start, stop, continue. Pick one change with an owner and a check.
6. **Compute (at home, 30 min).** From your logs compute `h` (fixed overhead in team-hours) and `λ` (wrong turns per week). Use your charter's `W`. Compute `L* = √(2h / (λW))` and `C(L)` at `L = 0.5, 1, 2` weeks. Check them in the interactive.
7. **Decide (at home, 20 min).** Choose your sprint length for the next two sprints. Then name one change that would cut `h`, estimate the new `h`, and recompute `L*`. Finally, plan the jam cycle: compute a jam `L*` in hours with `W = 4` per hour, your measured build-and-play time per person, and a jam `λ` you justify in one sentence.

## Deliverable

`sprints/sprint-01.md` in your team repository, complete, plus a one-page note `sprints/sprint-length.md` containing:

- Your `h`, `λ` and `W`, with the logs they came from.
- `L*`, the cost table and your chosen sprint length, with a two-sentence justification.
- The overhead cut you propose, with the new `h` and `L*`.
- Your jam cycle length in hours and the one-line jam check-in schedule.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Sprint artifacts | Ordered backlog, one-sentence goal of the right kind for the phase, checkable Definition of Done | Goal vague or DoD not checkable | Missing artifacts | 20% |
| Events held | Three or more logged standups within 15 min; review with 2+ outside players; retro with one owned, checkable change | Events held but thin logs or no outside players | Events missing | 25% |
| Review changes the backlog | Backlog changed with a reason tied to what players did | Changes not tied to observations | No change and no explanation | 15% |
| Measurement | `h` separates fixed from per-day overhead; wrong turns logged with hours; `λ` computed correctly | Measured but fixed and per-day overhead mixed | Numbers invented after the fact | 20% |
| Model and decision | Correct `L*` and cost table; sprint length and jam cycle chosen and defended; credible overhead cut | Minor errors, or choice not tied to the numbers | Missing or wrong | 20% |
