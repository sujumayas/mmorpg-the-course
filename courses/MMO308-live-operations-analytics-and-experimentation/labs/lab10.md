# MMO308 · Lab 10: Who answered the survey?

**Week:** 10, player feedback loops ([lecture](../lectures/w10-player-feedback-loops-forums-surveys-polls.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** analytics labs (40% of the course grade).

## Objective

A fictional MMO ran an in-game survey about a new daily quest cap, shown to players who were online at random moments. The raw result says most players dislike the cap. You will work out what the survey trigger did to the sample, correct it with inverse-probability weights, measure what the correction costs in effective sample size, and then estimate how many players were stuck on a quest bug from two report channels. You finish with a one-page note to a producer that gives both numbers with honest uncertainty.

## Starter materials

All in [`lab10-starter/`](lab10-starter/). Standard-library Python 3.12 or later (the repository's `.venv` has 3.13).

- [`survey.csv`](lab10-starter/survey.csv): about 3,000 respondents, one row each, with `player_id`, `segment` (casual, regular, hardcore), `hours_7d` and `sessions_7d` from telemetry for the survey week, and `approve` (1 or 0). Each player in the game was asked independently with a chance proportional to `hours_7d`, and everyone asked answered.
- [`forum_accounts.txt`](lab10-starter/forum_accounts.txt) and [`reporter_accounts.txt`](lab10-starter/reporter_accounts.txt): the distinct accounts that posted in the bug thread and that filed an in-game bug report about the stuck quest.
- [`stuck_accounts.txt`](lab10-starter/stuck_accounts.txt): the accounts the quest-state telemetry shows as stuck. Treat it as the answer key for section C. Don't open it until step 6.
- [`stuck_telemetry.csv`](lab10-starter/stuck_telemetry.csv): `player_id` and `hours_7d` for every stuck account, for step 7.
- [`feedback.py`](lab10-starter/feedback.py): loaders plus five stubs, `raw_share`, `ipw_share`, `kish_neff`, `lincoln_petersen` and `chapman`. Running it prints a results table once the stubs work.
- [`test_lab10.py`](lab10-starter/test_lab10.py): five checks. Three reproduce the lecture's numbers (the toy weights, `n_eff = 480`, and the 3,000-player capture-recapture estimate), one checks that no overlap raises an error, and one requires your weighted estimate on `survey.csv` to land within 2 points of the true approval. Run it from inside `lab10-starter/` with `../../../../.venv/bin/python test_lab10.py`. All five fail on the starter.
- [`make_survey.py`](lab10-starter/make_survey.py): the generator, seed 10. Don't edit it. Read its docstring if you want to know how the world was built, but do the analysis from the data.

## Steps

**A. The raw survey (20 min)**

1. Implement `raw_share`. Compute the raw approval, then the share of respondents in each segment and the mean `hours_7d` of respondents. Before going further, write one sentence predicting whether the true approval is higher or lower than the raw number, and why.

**B. Weighting (40 min)**

2. Implement `ipw_share` and `kish_neff`. Run the tests until the first three pass.
3. Compute the approval weighted by `1 / hours_7d`, and again weighted by `1 / sessions_7d`. Only one matches how the survey was triggered. Explain which, and what the other one would be right for.
4. Compute `n_eff` for the hours weights. Build a 95% interval for the weighted approval with the MA102 week 13 formula, using `n_eff` in place of `n`. Then build the interval the naive way, with `n` and the raw share. Put both in a table.
5. Compute the weighted approval separately within each segment and compare with the raw within-segment shares. Explain in two sentences why weighting changes the overall number a lot and the within-segment numbers only a little.

**C. How many were stuck? (30 min)**

6. Implement `lincoln_petersen` and `chapman`, and run all tests. Estimate the number of stuck players from the two channels. Now open `stuck_accounts.txt` and compare. Is the estimate a floor or a ceiling here?
7. Diagnose the gap. Join the two channel lists to `stuck_telemetry.csv`. Split stuck players into hours bands (under 5, 5 to 15, over 15) and show, in one table, the share of each band that posted, reported, and did both. Explain in three sentences how that breaks the independence assumption and which way it pushes the estimate.

**D. The note (at home)**

8. Write a one-page note to the producer. It must give the weighted approval with its interval, say plainly how the raw survey misled and by how much, give the stuck-player estimate from the two channels and the telemetry count, and recommend one change to how the team triggers surveys and one change to how it counts bug reach. Every claim must cite a number from steps 1 to 7.

## Deliverable

1. Your completed `feedback.py`, with all five tests passing.
2. A results table covering steps 1 to 7.
3. The producer note from step 8, one page.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; functions are short, clear and match the lecture's formulas | Tests pass with awkward or duplicated code | Tests fail | 20% |
| Weighting analysis (steps 1-5) | Correct weights chosen and justified; `n_eff` interval and naive interval both correct; segment comparison explained | Numbers correct, reasoning thin | Wrong weights, or intervals missing | 30% |
| Capture-recapture (steps 6-7) | Both estimates correct; dependence between channels shown with data and its direction explained | Estimates correct, diagnosis vague | Estimates wrong or missing | 25% |
| Producer note | Readable by a non-analyst, every claim backed by a number, both recommendations concrete | Recommendations present but some claims unsupported | Opinion without numbers | 25% |

<details>
<summary>Instructor check values</summary>

Generated with seed 10 and checked with Python 3.13.

- 3,078 respondents: 707 casual, 1,182 regular, 1,189 hardcore. Raw approval 43.9%.
- Weighted by `1 / hours_7d`: 60.8%. The true approval over all 60,000 players is 61.5%, so the estimate is within one standard error. Weighted by `1 / sessions_7d`: 54.2%, which is wrong for this trigger because the survey chance followed hours, not sessions.
- `n_eff` for the hours weights: 1,248. A 95% interval with `n_eff` is about ±2.7 points; the naive interval with `n = 3,078` is about ±1.8 points around the wrong centre.
- Forum 452 accounts, reporter 788, both 127. Lincoln-Petersen 2,805, Chapman 2,791. Telemetry shows 3,688 stuck, so the two-channel estimate is a floor, about 24% low, because engaged players use both channels.
- Strong notes recommend drawing survey invitations from the account list (or at least logging `π`), and counting bug reach from the quest-state event first, with capture-recapture reserved for problems telemetry can't see.

</details>
