# MMO308 · Lab 11: The poll archive

**Week:** 11, community-voted design ([lecture](../lectures/w11-community-voted-design-old-school-runescape-polls.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

Work with thirteen years of real votes. You will implement the lecture's pass and blocking rules, measure how many Old School RuneScape decisions depend on where the threshold sits, test two ballot-design effects (skips and conditional questions) in the data, and then write a voting rule for a game of your own with numbers to back each choice.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Standard-library Python 3.12 or later (the repository's `.venv` has 3.13). Use a spreadsheet for charts if you prefer.

- [`osrs_polls.csv`](lab11-starter/osrs_polls.csv): 3,304 rows, one per yes/no question from OSRS polls between 14 March 2013 and 21 September 2026, with `opened` (ISO date), `poll`, `yes`, `no`, `skip` and `question` (trimmed to 160 characters). Vote counts were tallied for this course from the Old School RuneScape Wiki's poll pages in September 2026. The wiki's text is licensed CC BY-NC-SA 3.0, and this file is shared under the same licence, so credit it if you publish anything built on this file. See [`DATA-LICENSE.md`](lab11-starter/DATA-LICENSE.md). The file includes a few survey-style questions and doesn't record which questions had extra voting restrictions.
- [`polls.py`](lab11-starter/polls.py): a loader, a date filter and five stubs, `yes_share`, `passes`, `no_votes_to_block`, `pass_count` and `flipped`. Thresholds are whole percentages and pass or fail must use integer arithmetic.
- [`test_lab11.py`](lab11-starter/test_lab11.py): five checks built from the lecture's numbers (Sailing and Warding shares, the 48,419 and 37,659 blocking counts, the archive pass counts, and the 177 and 21 flipped questions). Run it from inside `lab11-starter/` with `../../../../.venv/bin/python test_lab11.py`. All five fail on the starter.

## Steps

**A. The rule (30 min)**

1. Implement the five stubs and run the tests until all pass. Explain in one sentence why `passes` must not compare floats.
2. For Sailing (112,976 Yes, 44,153 No), compute the blocking "No" count at every threshold from 50% to 90% in steps of 5. Then do the same for Warding (82,633 Yes, 41,726 No). Mark the lowest threshold at which each fails.

**B. The archive (45 min)**

3. Plot the pass rate against the threshold, from 50% to 95% in steps of 1, for the whole archive. Mark 70% and 75%. Describe the shape of the curve in two sentences. Where is it steep and why?
4. Plot a histogram of yes shares in 1-point bins, once for questions before 27 October 2022 and once after. Compute the median of each. The lecture claims the rise in pass rate after 2022 came more from what was polled than from the threshold. Test that claim. Compute the pass rate after the change *at 75%* and compare it with the pass rate before the change at 75%.
5. Compute the pass rate by calendar year, judged at the threshold in force on each question's date. Pick the two years that stand out and look up, in the list of polls, one reason each could differ.

**C. Ballot design in the data (30 min)**

6. **Skips.** For questions since 11 February 2016, compute the skip share `skip / (yes + no + skip)`. Compare the median skip share of questions that fail at 75% with those that pass. Then recompute every yes share as if skips counted as "No", and report how many questions that passed at the rule in force would have failed.
7. **Conditional questions.** Flag questions whose text starts with "If" or "Subject to". Compare their median yes share with the rest. Find the Warding poll (opened 2019-07-19) and list its first question and all its follow-ups with their shares. Explain in three sentences why the follow-ups can outpoll the main question.

**D. Your rule (at home)**

8. Write a one-page voting rule for a mid-sized MMO of your own design, with 120,000 monthly active players and an expected 8% turnout. It must state the threshold, the eligibility rules, how skips count, whether results are visible during the vote, the categories you will not poll, and whether polls are greenlight or lock-in. Justify the threshold with its blocking group `τ × (1 − T)` and with one number from steps 3 to 7.

## Deliverable

1. Your completed `polls.py`, with all five tests passing.
2. The charts from steps 3 and 4 and a table covering steps 2, 5, 6 and 7.
3. The one-page voting rule from step 8.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; integer pass rule explained correctly | Tests pass, explanation missing or vague | Tests fail | 20% |
| Archive analysis (steps 3-5) | Both charts correct; the screening claim tested with the 75%-after comparison; year outliers explained with evidence from the poll list | Charts correct, claim tested loosely | Charts wrong or claim not tested | 30% |
| Ballot design (steps 6-7) | Skip and conditional effects measured; counterfactual skip count correct; Warding explained through who votes on follow-ups | Numbers correct, explanation thin | Missing or wrong | 25% |
| Voting rule | Every choice justified, threshold backed by the blocking-group formula and archive evidence, trade-offs named | Rule complete, some choices unsupported | Rule incomplete or unsupported | 25% |

<details>
<summary>Instructor check values</summary>

Checked with Python 3.13 on the shipped `osrs_polls.csv`.

- Pass counts over all 3,304 questions: 3,204 at 50%, 3,121 at 60%, 2,975 at two thirds, 2,879 at 70%, 2,681 at 75%, 2,404 at 80%, 1,065 at 90%. The curve is flat below about 70% and steep between 80% and 95%, because the median question gets about 87% "Yes".
- Before 27 October 2022: 2,647 questions, median 86.1%, pass rate at 75% 78.2%. From that date: 657 questions, median 89.7%, pass rate at 70% 96.3% and at 75% 93.2%. Most of the rise survives at 75%, which supports the screening explanation.
- Pass rate by year at the rule in force: 2013 53.3%, 2014 69.4%, 2019 68.4% are the low years; 2020 onward mostly above 93%, with 2022 at 80.1%. 2019 includes the Warding poll and its fifteen follow-ups.
- Skips since 11 February 2016: median skip share 8.2% for questions that fail at 75%, 6.4% for those that pass.
- Conditional questions: 455, median yes share 84.7%, against 87.2% for the other 2,849. Warding: main question 66.4%; eleven of fifteen follow-ups between 70% and 74%, highest 73.8% (Warding Guild).
- Skips counted as "No": of the 2,702 questions that passed at the rule in force on their date, 382 would have failed. Questions before February 2016 have no skips, so they are unaffected. Accept a different count only if the student states a different method clearly.

</details>
