# UX201 · Lab 14: Findings triage and research report

Assigned in week 14 ([lecture](../lectures/w14-ux-research-reporting.md)). Due one week later. Groups of three; each group submits one report and one tracker. This lab is the dry run for the week 15 final, a UX study of a shipped game, so use the same structure there.

## Objective

Turn a raw observation log into a report a team can act on. You will cluster notes into findings, rate severity independently, compute Wilson intervals and impact tiers with the starter script, write each finding in the five-part form, and assemble a report with a one-page summary and a findings tracker. The skill being graded is honest prioritization. Your report should put the right problems first and say how sure you are about each.

## Starter materials

**1. Observation log.** [`lab14-starter/observation_log.csv`](lab14-starter/observation_log.csv) holds 36 timestamped notes from five invented testers (P1 to P5) playing the first 30 minutes of a fictional co-op dungeon game. Columns: `tester`, `time` (mm:ss into the session), `task` (T1 create character, T2 leave town, T3 first quest, T4 first dungeon, T5 loot and talents, plus post-session remarks), `observation`, `quote` (verbatim, may be empty) and `tag` (`S` stuck or error, `Q` question, `B` gave up or visible annoyance, empty for neutral or success). Some notes record things that worked. The facilitator was silent except where a note says otherwise.

**2. Triage script.** [`lab14-starter/triage.py`](lab14-starter/triage.py), standard-library Python 3. It reads a findings CSV and prints, per finding, the rounded mean severity, the Wilson interval, `P`, `L`, `U`, tier and fix cost, sorted by tier and then by `U`, followed by the plain frequency order for comparison. It flags findings whose three severity ratings differ by 2 or more. Options: `--n` (testers, default 5), `--weights` (default `1,3,10,30`), `--bar` (default 1), `--z` (default 1.96).

**3. Findings CSV.** [`lab14-starter/findings_template.csv`](lab14-starter/findings_template.csv) has the header row `id, title, testers_hit, r1, r2, r3, fix_cost` and one placeholder line. [`lab14-starter/findings_example.csv`](lab14-starter/findings_example.csv) holds the six findings from the lecture's worked example, so you can check that the script reproduces the lecture table before you start: `python3 triage.py findings_example.csv`.

**4. Severity scale (use exactly).** 1 cosmetic: noticed, no cost. 2 minor: costs seconds or mild annoyance. 3 major: costs minutes, causes a wrong decision or strong frustration. 4 blocker: the player can't continue, loses progress, or gives up on content.

**5. Fix-cost estimates.** Your lab instructor plays the owner. Ask for a cost (S, M or L) for each finding once your list is final. Record the answer in the CSV.

**6. Report skeleton.** Use the five sections from lecture section 4 as headings: summary, findings by tier, what worked, method and limits, appendix.

## Steps

1. **Agree the policy first (10 min).** Before reading the log in detail, write down your weights and bar. Use the lecture defaults unless you can justify a change in two sentences. Commit this to your report's method section now. You may not change it later.
2. **Cluster (30 min).** Group the 36 notes into findings. Title each one with the problem, not the feature. Count **testers**, not notes, for `testers_hit`. P1 opening the map four times is one tester. Put successes into a separate list.
3. **Rate independently (10 min).** Each group member rates every finding's severity alone, without discussion, and enters it as `r1`, `r2` or `r3`.
4. **Get fix costs** from the instructor and fill `fix_cost`.
5. **Run the script** with your policy. Save the output. Then run it once with `--weights 1,2,4,8` and once with `--z 1.645`, and note which findings change tier.
6. **Discuss the split ratings.** For each finding the script flags, write two sentences on why the ratings differed. Don't change the ratings to agree. Report the split.
7. **Write the findings** in the five-part form (observation, evidence, interpretation, impact, recommendation), with the severity, count, interval and tier on the title line. Every quote must come from the `quote` column, word for word, with tester and timestamp.
8. **Give every investigate finding a next step.** Name the test, how many testers, or which telemetry event would decide it.
9. **Write the one-page summary last.** Study goal, build and testers, the fix-now findings in one line each, what worked, and the single most important limit of the study.
10. **Build the tracker.** One row per finding: ID, title, severity, tier, cost, owner (write "design", "UI" or "QA"), status "open", and a column for retest results in the form "x of n after fix (interval)". Add one invented retest row for your top fix-now finding, 0 of 6, and fill its interval.

## Deliverable

- The report, at most four pages plus appendix, in the section order above.
- The tracker as a table (spreadsheet or Markdown).
- Appendix: your findings CSV, both script outputs from step 5, and the split-rating notes.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Findings and counts | Problem-first titles; testers counted, not notes; successes kept; no finding merges two different problems | Minor counting or clustering slips | Findings are features or opinions; notes counted as testers | 20% |
| Triage | Policy fixed before analysis; script run correctly; tiers reported with intervals; sensitivity runs interpreted; split ratings reported honestly | Tiers correct, sensitivity or splits thin | Findings ordered by frequency or by gut | 25% |
| Writing each finding | Five parts kept separate; verbatim quotes with codes and times; recommendations as directions with a retest | Parts present but blurred | Interpretation presented as observation, or invented quotes | 25% |
| Summary and structure | A reader of page one alone would schedule the right fixes; limits stated plainly | Summary present but buries the blocker or overclaims | No summary, or percentages with no counts | 20% |
| Tracker | All fields filled; retest row reports the interval and a close-or-keep decision | Tracker present with gaps | Missing | 10% |
