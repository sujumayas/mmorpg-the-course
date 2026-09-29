# MMO407 · Lab 10: Recovery dashboard and plan

**Assigned:** week 10 ([lecture](../lectures/w10-recovery-strategies.md)). **Due:** start of week 11 class. **Feeds:** the recovery section of the week 13 launch plan and the final launch plan (50%).

## Objective

Build the numbers a recovery team should watch, then use them to choose a plan. You will compute all-time, recent-window, reset and exponentially weighted review scores from a daily review log, reproduce the lecture's months-to-target table, and compare three recovery plans for an invented MMO. By the end you should be able to say, for any plan, which of the three stocks (build, players, reputation) it moves and how many months the store page will lag behind the players.

## Starter materials

The folder [`lab10-starter/`](lab10-starter/) contains:

- [`review_memory.py`](lab10-starter/review_memory.py), your file. It has the lecture's section 2 constants, a deterministic `make_log()` that builds a 720-day review log (a 30-day launch rush at 35%, a quiet period at 30%, a fix on day 120 after which 85% of reviews are positive), the `lapsed_pool` and `net_returners` helpers, and four TODOs: `lifetime_share`, `reviews_needed`, `weight` and `score`.
- [`test_review_memory.py`](lab10-starter/test_review_memory.py), five tests. All five fail on the starter.

Standard library only. Run everything with the course Python from inside the starter folder:

```
cd labs/lab10-starter
../../../../.venv/bin/python -m unittest test_review_memory.py
../../../../.venv/bin/python review_memory.py
```

When the TODOs are done, the report's first lines match the lecture's tables (35.0%, 44.2%, 50.5% ... and 11.4, 26.7, 62.2, 240.0 months), and the log section prints one row per checkpoint day with the four scores.

## Steps

1. **The mixture (20 min).** Implement `lifetime_share` and `reviews_needed` (TODOs 1 and 2). Run the tests in `TestMixture`. Then, by hand, check one row of the lecture's 12-month table and one row of the target table, and paste your working into the report.
2. **Weights (30 min).** Implement `weight` and `score` (TODOs 3 and 4). All five tests should now pass. In the report, write the general form `Σ w × x / Σ w` and state `w` for each of the four modes in one line each.
3. **Read the log (20 min).** Run the script. Make a table of the four scores at days 29, 119, 149, 365 and 719. Answer: on day 149, why do the recent-window and reset scores agree while the lifetime score is still near 36%? Which score does a stranger on the store page read first, and which does a returning player care about?
4. **Half-life sweep (20 min).** Recompute the day-365 exponential score for half-lives of 30, 90, 180 and 365 days. Plot or tabulate it. Explain in two sentences where Steam's two scores sit on this sweep.
5. **Three plans (40 min).** Use this invented game. The launch window drew 60,000 reviews at 30%. Since the stabilisation patch, 2,000 reviews a month arrive at 80%. It sold 1,500,000 copies and has 110,000 monthly active players. Compare, over 24 months:
   - Plan A, fix and wait: `r` rises to 85% from month 4, volume unchanged.
   - Plan B, content update with a free weekend in month 6: one month with 25,000 extra reviews at 80%, and 6% of the lapsed pool reactivated, of whom 40% stay a month.
   - Plan C, relaunch on a new store page in month 12: the new page starts empty; assume 30,000 reviews in its first month at 82%, then 2,500 a month at 82%.
   For each plan, give the all-time share of the page a stranger sees at months 6, 12 and 24, the net returning players, and the stock each part of the plan moves. Write a helper for plans B and C; the tests do not cover it, so show your code.
6. **Choose (15 min).** Pick one plan (or a combination) and defend it in one paragraph, using at least two numbers from step 5. State one assumption that, if wrong, would change your choice, and what telemetry would tell you it is wrong.

## Deliverable

A zip or repository link containing:

- Your `review_memory.py` with all tests passing (paste the test output in the report), and the helper from step 5.
- `report.md`, 700 to 1,000 words: the step 1 hand check, the step 2 weights, the step 3 table and answers, the step 4 sweep, the step 5 comparison table, and the step 6 recommendation.
- Every number reproducible from a command you list.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Tests | All five pass | Three or four pass | Two or fewer | 20% |
| Model understanding | Hand checks correct; `w` stated correctly for all four modes; step 3 answer ties the gap to the launch pile | Minor slips in one part | Weights or hand checks wrong | 20% |
| Half-life sweep | Correct values and a clear placement of Steam's lifetime and 30-day scores at the ends of the sweep | Values correct, placement missing | Not done | 10% |
| Plan comparison | All three plans computed at 6, 12 and 24 months with returners; the stranger's page is identified correctly for plan C | Two plans computed, or plan C uses the wrong page | Fewer than two plans | 25% |
| Recommendation | Uses the numbers, names the stock each step moves, names a falsifying assumption and its telemetry | Uses the numbers but no assumption | Opinion without numbers | 15% |
| Reproducibility and clarity | Commands listed; tables match reruns | Minor gaps | Cannot be rerun | 10% |
