# GD201 · Lab 08: Clue reliability from playtest data

**Week:** 8 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the analysis component (20% of the course).

**Lecture:** [Week 08, environmental storytelling](../lectures/w08-environmental-storytelling.md). **Interactive:** [w08-clue-reliability.html](../examples/w08-clue-reliability.html), for checking your numbers and seeing the correlated case.

## Objective

Implement the three reading rules and the general "at least k of n" calculation. Use them on a 24-tester playtest log of the lecture's watchtower to compare what the independence model predicts with what testers did. Build a planner that picks the fewest clue slots to hit a target understanding rate. Then put one story beat into your week 7 greybox and measure it.

## Starter materials

- [`lab08-starter/story_reliability.py`](lab08-starter/story_reliability.py). Seven functions to fill in: `p_all`, `p_any`, `p_at_least`, `load_log`, `estimate_p`, `observed_rate` and `plan_clues`. Also `CHAPEL_SLOTS`, eight candidate clue positions for a chapel level, each with a notice chance from the lecture's tier table.
- [`lab08-starter/watchtower_playtest.csv`](lab08-starter/watchtower_playtest.csv). One row per tester (24 rows). Columns `well`, `sickbay`, `order`, `bags` are 1 if the tester noticed and correctly read that clue. `said_beat` is 1 if, asked "what happened in the tower?", the tester stated the beat without a hint.
- [`lab08-starter/check_lab08.py`](lab08-starter/check_lab08.py). A checker with 10 checks. Do not edit it.
- For Part E: your week 7 greybox, three testers who haven't seen it, and a notebook.

Run from inside `lab08-starter` with the course Python:

```
python story_reliability.py
python check_lab08.py
```

The starter runs and says the functions are not implemented. The checker prints `0/10 checks pass` until you fill them in.

## Steps

1. **Part A, the rules (20 min).** Implement `p_all`, `p_any` and `p_at_least`. Use the dynamic program from the lecture for `p_at_least`, and handle `k = 0` and `k > n`. Reproduce the lecture's table for the four watchtower clues.
2. **Part B, the log (20 min).** Implement `load_log`, `estimate_p` and `observed_rate` with the `csv` module. Print `p̂` for every clue.
3. **Part C, the planner (20 min).** Implement `plan_clues` by brute force over subsets of increasing size (there are only 255 non-empty subsets of eight slots). Follow the tie rule in the docstring. Run the checker until it prints `10/10 checks pass`.
4. **Read the playtest (20 min).** Run `story_reliability.py`. Make a table of predicted and observed rates for `k = 1..4`. In your log, answer:
   - For which `k` is the prediction too optimistic, and for which too pessimistic? Explain the pattern with the idea of correlated noticing from section 2 of the lecture.
   - Count how many testers noticed at least one clue but did not say the beat, and how many said the beat having noticed only one clue. What `k` best describes how these testers actually read the tower?
   - With 24 testers, how confident can you be in `p̂` for the captain's order (7 of 24)? Give a rough range and say whether you would redesign that clue based on this test alone.
5. **Part D, plan the chapel (15 min).** Use `plan_clues` to find the smallest layouts for target 0.9 with `k = 1` and `k = 2`, and explain why `k = 3` has no solution. Then choose a beat for the chapel, write four clues for the `k = 2` layout, and explain which of them you would rewrite if the altar slot turned out to be only 0.5 in testing.
6. **Part E, dress your greybox (at home, 60 min).** Pick one beat for your week 7 vertical space and place three or four clues using the lecture's levers (stop points, framing, gates, sound). Write down your intended `k` and each clue's tier before testing. Run three testers. Record who noticed which clue and who said the beat, in the same CSV format. Compare with your prediction.
7. **Stretch (optional).** Write `simulate(ps, k, players, attentive_share, boost)` using the interactive's attentive-player model and find the correlation strength that best reproduces the watchtower log's observed rates.

## Deliverable

Submit a zip with:
- Your completed `story_reliability.py`.
- Your greybox playtest CSV and two screenshots of your beat's strongest and weakest clue.
- A log (about 600 words) with: the predicted-versus-observed table and your three answers from step 4; the chapel layouts and your clue text from step 5; your beat, intended `k`, tier table and test result from step 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 10/10 checks pass | 6-9 checks pass | 5 or fewer pass | 30% |
| Playtest reading | Direction of error explained by correlation for each `k`; reading rule inferred from `said_beat`; sample-size caution with a range | Correct table, explanation partial | Table missing or misread | 25% |
| Chapel plan | Both layouts, `k = 3` impossibility explained with numbers, clue text carries whole beats | Layouts correct, clue text weak | Missing | 15% |
| Greybox beat | Intended `k` and tiers written before testing, three testers, honest comparison and a specific fix | Tested but prediction written after | Not tested | 20% |
| Code readability | Clear names, no repeated logic between rules | Works but repetitive | Hard to follow | 10% |
