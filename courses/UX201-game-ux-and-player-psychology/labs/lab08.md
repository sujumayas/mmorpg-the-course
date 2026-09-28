# UX201 · Lab 08: RITE usability test of an onboarding sequence

Assigned in week 8 ([lecture](../lectures/w08-usability-testing-methods.md)). Due at the start of week 10. Groups of three or four; each group submits one report. This lab is the practice run for the graded usability test assignment (30%).

## Objective

Plan and run a usability test of a short onboarding sequence using the RITE method. Fix the build between testers when the cause and the fix are clear, log errors and failures per tester, and report what you found, what you fixed, how confident you are that each fix worked, and what is still open. The point is to see reach at work. Your error count may rise after a good fix, and you should be able to explain why.

## Starter materials

**1. Test plan template.** Copy the eight headings from lecture section 3, "A test plan in one page": question, players, tasks (each with a success criterion and time limit), zero-tolerance items, measures, script, change policy, report. Your plan must fit on one page.

**2. Observation log.** [`lab08-starter/observations.csv`](lab08-starter/observations.csv), with invented data from the lecture's Harbor tutorial so you can run the script before your sessions. Columns: `tester, build, minute, task, issue_id, kind, note`. `kind` is `error` or `failure`, using the week 8 definitions (a failure stops the tester continuing without help). Log an issue once per tester. Write `ASSIST` in the note whenever the moderator stepped in.

**3. Change log.** [`lab08-starter/changes.csv`](lab08-starter/changes.csv). Columns: `after_tester, issue_id, change, refix_of`. One row per change to the build. For a re-fix, repeat the `issue_id` and put the earlier change's `after_tester` in `refix_of`.

**4. Report script.** [`lab08-starter/rite_report.py`](lab08-starter/rite_report.py), standard-library Python 3. Run `python3 rite_report.py observations.csv changes.csv`. It prints errors and failures per tester with build boundaries, each issue's sightings and fix status, fixes contradicted by later sightings, verification confidence `1 − (1 − p)^m` at `p = 0.1` and `0.3`, and the impact and re-fix ratios.

**5. What to test.** You need a sequence of 10 to 20 minutes that you can change between testers in under 30 minutes. Choose one:

- your own onboarding prototype from lab 07 or GD101/GD102 work (a paper prototype counts, with a "computer" played by a team member);
- a level or tutorial built in a game with a level editor or modding tools that your group can change quickly;
- a paper or clickable mock-up of a game menu flow (inventory, crafting or group finder), with the screens printed or in a prototyping tool.

Get the choice approved in the week 8 lab session.

**6. Script (read it word for word, then add your task cards).**

> Thanks for helping. We're testing the game, not you. If something is confusing, that is the game's fault and exactly what we need to find. Please think aloud as you play: say what you're looking at, what you're trying to do and what you expect to happen. In fast moments you can go quiet, and we'll ask you afterwards. I can't answer questions about how to play during the tasks, but I'll answer everything at the end.

**7. SUS questionnaire.** Use the ten standard SUS items from Brooke (1986) with the word "system" replaced by the name of the part you tested. Score with the formula from lecture section 1.

## Steps

1. **Plan.** Write the one-page plan. Agree the zero-tolerance list and the change policy as a group before recruiting. Name who decides on changes during the test.
2. **Pilot** with one classmate. Fix the setup, not the game, after the pilot.
3. **Recruit six to eight testers** who match your player definition and have not seen your sequence.
4. **Run the sessions.** Roles: moderator, observer (fills the CSV), and builder (makes changes). After each tester, spend five minutes sorting issues into the four RITE categories (obvious and quick, obvious and slow, unclear cause, might be the test). Fix category 1 issues before the next tester. Log every change in `changes.csv`.
5. **Rescue rule.** If a tester is stuck at a failure for three minutes, rescue them, log `ASSIST`, and let them continue so later sections still get tested.
6. **SUS** after each session.
7. **Run the script.** Save the output.
8. **Explain the curve.** Mark every build change on the errors-per-tester chart. For any rise after a change, say whether it came from reach (testers got further) or from a fix that broke something, with evidence from the notes.
9. **Verify.** For each fix, report `m` and the confidence at `p = 0.1` and `0.3`. Name the fixes you would not yet trust.

## Deliverable

A report of at most three pages plus appendices.

- The one-page test plan (counts toward the three pages).
- The errors-per-tester chart with build changes marked, and your explanation of its shape.
- A problem table: id, description, heuristic or cause, first seen, times seen, status (fixed after tester k, re-fixed, open), verification confidence.
- Impact ratio and re-fix ratio, with one sentence on what each says about your test.
- SUS per tester and the mean, with a sentence on why you shouldn't compare it with other groups' numbers.
- The three most important open problems, each with a proposed fix.
- Appendices: `observations.csv`, `changes.csv`, script output, handwritten notes.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Test plan | Precise question, player criteria, tasks with success criteria, agreed zero-tolerance list and change policy, one page | Most parts present, some vague | Missing tasks or success criteria | 20% |
| Session method | Script verbatim, think-aloud kept up, assists logged, rescue rule followed | Minor slips, documented | Coaching, or no log of assists | 20% |
| RITE decisions | Changes made between testers, each categorised, logged and verified by later testers | Some changes, weak logging | No changes during the test, or changes without logging | 20% |
| Analysis | Error curve explained with reach and evidence, verification confidence computed and read correctly, both ratios reported | Numbers right, explanation thin | Error counts treated as a quality score | 25% |
| Recommendations | Open problems ranked, each with a fix and its cost | Generic recommendations | Missing | 15% |
