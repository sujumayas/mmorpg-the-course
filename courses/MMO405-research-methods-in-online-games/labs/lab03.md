# MMO405 · Lab 03: Sessionizing a log and auditing self-report

**Week:** 3 ([lecture](../lectures/w03-telemetry-as-research-data.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual code; the data management section may be drafted in pairs.
**Counts toward:** methods labs (30% of the course grade). The data management and consent section becomes part of your course proposal (20%).

## Objective

Turn a raw event log into hours played under several defensible rules, see how much the rule and the cleaning change the answer, measure how well players' own estimates track the log, and write the consent and data-handling plan a linked-telemetry study needs.

## Starter materials

- [`lab03-starter/telemetry.py`](lab03-starter/telemetry.py), Python 3.10 or later, standard library only. It loads both files and gives you `login_logout_hours` as a worked model. It has three stubs:
  - `sessionize` (TODO 1), the activity-gap rule from lecture section 3.
  - `hours_by_account` (TODO 2), hours per account, with zeros for accounts that never appear.
  - `corrected_r` (TODO 3), Spearman's correction from lecture section 2.
- [`lab03-starter/events.csv`](lab03-starter/events.csv), an invented week of events: `account_id`, `minute` (since Monday 00:00) and `type` (`login`, `activity`, `logout`). It has 54,274 rows, arriving out of order as real logs do. [`lab03-starter/survey.csv`](lab03-starter/survey.csv) has the same week's survey for 300 accounts: `reported_hours` and `satisfaction` (1 to 7). [`make_log.py`](lab03-starter/make_log.py) generated both. **Do not read it until step 8.**
- [`lab03-starter/test_telemetry.py`](lab03-starter/test_telemetry.py) has six tests. All fail on the starter and pass on a correct solution. Run them from inside `lab03-starter/` with `python -m unittest test_telemetry.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w03-self-report-vs-logs.html`](../examples/w03-self-report-vs-logs.html), once it is built.

## Steps

### Part A: from events to hours (45 min)

1. Before writing code, write down which construct you want ("time with the game running" or "time actively playing") for a study of play and satisfaction, and which rule that implies. One sentence each.
2. Implement TODOs 1 and 2. The lecture's evening must give 85 minutes under a 10-minute gap and 110 under a 30-minute gap. Run the tests.
3. Run `python telemetry.py` (TODO 3 is needed for the last column; stub it with `return 0.0` until Part B if you like). Report the mean hours for the 300 surveyed accounts under login-to-logout, a 10-minute gap and a 30-minute gap. Compute the ratio of the largest to the smallest mean and compare it with the lecture's 1.76 for one evening.
4. Find the five accounts whose hours change most between login-to-logout and the 10-minute rule. Look at their raw events and describe in two sentences what they have in common.

### Part B: cleaning (25 min)

5. Some accounts in `events.csv` are not in the survey. List them, their hours under your chosen rule, and give a one-line cleaning rule that would remove them from a study that did not have the survey to tell you. State which way the rule moves mean hours for all logged accounts.
6. Thirty surveyed accounts have no events at all. Should they count as zero hours, or be dropped? Compute the mean hours both ways under your rule and state which population each version describes.

### Part C: self-report audit (30 min)

7. Implement TODO 3 and run all six tests. For your chosen rule, report the mean of `reported_hours − logged hours`, the SD of that difference, and `r(said, logged)`. Then report `r(said, satisfaction)`, `r(logged, satisfaction)` and the corrected value, each with a 95% interval using Fisher's `z` from lab 02. Say whether the corrected estimate's interval contains the log-based one.
8. Now read `make_log.py`. Its "true hours" is a rough count of activity events, not any of your rules. Explain in three sentences how that affects your step 7 comparison, and which of your rules comes closest to it.

### Part D: data management and consent (20 min)

9. Write the data section of a proposal to run this study with a real studio. In at most one page, cover:
   - the unit of analysis and the sessionization rule, with a sensitivity check;
   - the consent text for linking survey answers to logs (two or three sentences a player would read);
   - how IDs are pseudonymized, who holds the mapping, and when it is deleted;
   - the GDPR points from lecture section 5 that apply (lawful basis named separately from ethical consent, Article 89(1) safeguards, a deletion date);
   - which ethics board reviews it and what you will do if the data show a player at risk.

## Deliverable

- `telemetry.py` passing all six tests, plus your code for steps 3 to 7.
- A results sheet (two pages at most) with the answers to steps 1 and 3 to 8.
- The one-page data section from step 9.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (steps 2 and 7) | All tests pass; report reproduced | Tests pass; report incomplete | Tests fail | 20 |
| Rules and units (steps 1, 3 and 4) | Construct chosen first; three means and ratio correct; pattern in the five accounts identified | Numbers right, reasoning thin | Missing or wrong | 20 |
| Cleaning (steps 5 and 6) | Bots found with a rule that does not need the survey; direction of bias stated; zero-vs-drop populations named | Found but rule or direction missing | Missing | 15 |
| Self-report audit (steps 7 and 8) | Bias, noise and attenuation separated; intervals computed; ground-truth caveat explained | Values right, interpretation weak | Missing | 20 |
| Data section (step 9) | Every bullet covered; legal basis and ethical consent kept separate; realistic deletion plan | One bullet missing or GDPR points vague | Missing | 20 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
