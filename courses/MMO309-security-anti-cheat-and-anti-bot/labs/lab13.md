# MMO309 · Lab 13: Pricing a bounty table

Assigned in week 13 ([lecture](../lectures/w13-bug-bounty-and-disclosure.md)). Due at the start of week 14. Part of the labs component (30% of the course).

## Objective

Turn the week 13 finder model into a working pricing tool. Price a bounty table for five classes of exploit, show how the table changes with your team's detection speed, and recommend a payout scale and a detection target to your producer.

## Starter materials

- [`lab13-starter/bounty.py`](lab13-starter/bounty.py). A module with the model's formulas in its docstring, a CSV loader, a `round_up` helper and six stub functions marked TODO: `exploit_value`, `bounty_needed`, `studio_cost`, `double_dip_value`, `price_table` and `longest_affordable_detection`. Running it as a script prints the priced table once the stubs are filled.
- [`lab13-starter/exploit_classes.csv`](lab13-starter/exploit_classes.csv). Five invented exploit classes for a fictional MMO, from a currency dupe down to an out-of-bounds teleport. Each row gives `v`, `q`, `L`, `a`, `d` and `R` as defined in the lecture. The numbers are assumptions for practice, not data from any real game.
- [`lab13-starter/test_bounty.py`](lab13-starter/test_bounty.py). Checks against the lecture's worked numbers and the CSV. Run it from inside `lab13-starter/` with `../../../../.venv/bin/python test_bounty.py`. Every check fails on the starter and passes on a correct solution.

## Steps

1. **Implement the model.** Fill in `exploit_value`, `bounty_needed`, `studio_cost` and `double_dip_value`. Run the tests until the "model" and "double dip" groups pass. Then reproduce the lecture's five-row table (mean detection 50, 20, 10, 4 and 2 days) in your own output and confirm it matches.
2. **Price the table.** Implement `price_table`. With a mean detection time of 10 days and a $100 floor, print `B*`, the payout, the studio's expected cost and the payout as a share of that cost for each class.
3. **Find the affordable detection time.** Implement `longest_affordable_detection`. Your producer caps any single bounty at $5,000. What is the slowest mean detection time at which every class still has `B* ≤ $5,000`? Which class sets the limit? Repeat for caps of $2,000 and $10,000 and put the three answers in a table.
4. **Sensitivity.** For the currency dupe only, change one input at a time by ±50% (`v`, `q`, `L`, `a`) and record how `B*` moves at 10-day detection. Rank the four inputs by how much they move the bounty. Say which one the studio controls most directly.
5. **Double dip.** For the currency dupe at the payout you chose in step 2, find the log-audit probability `p` above which using the bug for 3 days before reporting is worse than reporting at once. Say what logging you would need to reach that `p`.
6. **Policy.** Write the payout scale you would publish. You may round, add tiers or merge classes, but each published number must be at or above the class's `B*` at the detection time you commit to, or you must explain why not.

## Deliverable

Your completed `bounty.py` (tests passing), and a memo to your producer of at most 300 words plus tables. The memo gives the payout scale, the detection time it assumes, the cap analysis from step 3, and the single investment you would fund first (detection, triage speed, audit logging or higher bounties), backed by a number from your analysis.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All tests pass; lecture table reproduced exactly | Most tests pass, small error in one function | Tests fail or functions missing | 30% |
| Detection analysis | Step 3 table for three caps, binding class named and explained with the formula | Table present but binding class not explained | Missing | 20% |
| Sensitivity and double dip | Inputs ranked with numbers; break-even `p` computed and tied to a concrete logging need | Ranking or break-even present, not both | Missing | 20% |
| Recommendation | Payout scale consistent with `B*`, first investment justified by a computed number | Scale given, justification qualitative | No recommendation | 20% |
| Memo clarity | Under 300 words, tables first, plain language a producer can act on | Clear but long | Hard to follow | 10% |
