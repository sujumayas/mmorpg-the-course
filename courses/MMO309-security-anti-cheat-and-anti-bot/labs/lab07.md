# MMO309 · Lab 07: Behavioral features for bot detection

Assigned in week 7 ([lecture](../lectures/w07-bot-detection-behavioral-features.md)). Due at the start of week 8. Part of the labs component (30% of the course).

## Objective

Turn raw server telemetry into the three features from the week 7 lecture (slack CV, active hours per day and self-similarity), combine them into a detection rule that meets a precision and recall target without accusing honest players, and rank your features by what it would cost a bot operator to fake them.

## Starter materials

- [`lab07-starter/make_logs.py`](lab07-starter/make_logs.py). Generates the dataset with seed 309: 150 synthetic accounts, 7 days each. It writes `intervals.csv` (200 action intervals per account, with the cooldown that gated each action), `hours.csv` (one row per active hour with six action counts: kills, loots, moves, chats, trades, crafts) and `labels.csv` (bot or human, and the account's kind). The population includes casual players, rotation players on a 1.5 s global cooldown, heavy grinders, a few honest players who fish for hours, and four kinds of bot. All data is invented; nothing comes from a real game.
- [`lab07-starter/features.py`](lab07-starter/features.py). The file you edit. Five functions marked TODO: `slack_cv`, `active_hours_per_day`, `cosine`, `self_similarity` and `flag`. The starter's `flag` uses raw timing only, the rule the lecture warns against.
- [`lab07-starter/check_lab07.py`](lab07-starter/check_lab07.py). Tests each feature on hand-computable inputs, then runs your features and your rule over all 150 accounts and prints how many of each kind you flagged. Run it from inside `lab07-starter/` with `../../../../.venv/bin/python check_lab07.py` (it builds the CSV files if they are missing). Every check fails on the starter and passes on a correct solution.
- The week 7 interactive, `examples/w07-click-timing.html`, for checking your intuition about each feature.

## Steps

1. **Look before you code (15 minutes).** Run `make_logs.py`. Open `labels.csv` and count accounts of each kind. Pick one rotation human and one rotation bot and compute, in a spreadsheet or by hand, the mean and standard deviation of their first 10 gaps and of their first 10 slacks. Write one sentence on why the raw numbers mislead.
2. **Implement the features.** Fill in `slack_cv`, `active_hours_per_day`, `cosine` and `self_similarity`, following the docstrings. Run the checker until its first four checks pass.
3. **Profile the population.** Write a short script (or use a notebook) that computes all four features for every account and prints the minimum and maximum of each feature for each kind. Put the result in a table. Mark every cell where an honest kind overlaps a bot kind.
4. **Try the naive rules.** Test each single-feature rule on its own: `raw_cv < 0.35`, `slack_cv < 0.35`, `hours_per_day > 18`, `self_similarity > 0.97`. For each, record precision, recall and which honest kinds it flags.
5. **Write your rule.** Replace `flag` with a rule that reaches precision ≥ 0.95 and recall ≥ 0.90 and flags no rotation humans. The checker enforces all three. Keep the rule to at most three clauses, and justify each threshold with a number from your step 3 table. The lecture's section 5 rule already meets the targets on this data, so copying it earns nothing for the detection-rule criterion. Derive your thresholds from your own table, and if they land where the lecture's do, show the margin each one leaves on both sides. Step 7 then shows why a rule that only just fits one dataset is fragile.
6. **Attack your own rule.** For each clause, describe in one or two sentences the cheapest change a bot author could make to escape it, and estimate what it would cost them in output. Use the Lineage break-even figure from the lecture (at least 120 hours a month) for the hours clause.
7. **Stress test.** Change one generator parameter to make the part-time mimic bots play 4 to 6 hours a day instead of 7 to 10, regenerate, and rerun the checker. Report what broke and propose one feature from the lecture's section 4 catalog that would catch them. You do not need to implement it.

## Deliverable

Your completed `features.py` with the checker printing `ALL PASS` on the original data, and a report of at most 600 words plus tables containing the step 3 feature table, the step 4 comparison, your rule with its justification, the step 6 cost-to-fake analysis and the step 7 stress-test finding.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correct features | All four feature checks pass; code is readable and handles edge cases named in the docstrings | Passes with minor style or edge-case issues | Checks failing | 25% |
| Detection rule | End-to-end check passes; every threshold justified from the step 3 table; no clause without a reason | Passes, justification thin for one clause | Fails the targets or thresholds are unexplained | 20% |
| Error analysis | Step 4 table complete; the honest kinds each naive rule flags are named and explained by the game's design | Table complete, explanations generic | Missing or wrong | 20% |
| Cost-to-fake reasoning | Each clause has a specific evasion and a numeric cost estimate tied to the lecture's economics | Evasions named, costs vague | Missing | 20% |
| Stress test | Clear report of what broke, with a proposed feature that would plausibly catch it and its likely false positives | Report present, proposal weak | Missing | 15% |
