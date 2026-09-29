# MMO403 · Lab 07: A loot box rules engine

**Week:** 7, regulation ([lecture](../lectures/w07-regulation-belgium-netherlands-china-others.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish the memo.
**Work mode:** pairs for the code, individual memo.
**Counts toward:** ethics analysis (20% of the course grade), one of its five lab pieces with labs 03, 04, 06 and 08 (see the [ethics analysis brief](../assessments/ethics-analysis-brief.md)).

## Objective

Turn the week 7 rule table into code you can run against any monetization design, use it to find the smallest design changes that clear a set of markets, and then apply it to one real game in a compliance memo. The model is a teaching tool with a stated date (28 September 2026). It is not legal advice, and your memo must say so.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Standard-library Python.

- [`lootlaw.py`](lab07-starter/lootlaw.py): a `Design` record with the lecture's five facts plus two compliance facts (`odds_shown`, `parental_gate`), the six lecture presets A to F, a provided `candidate_changes`, and stubs for `assess`, `assess_all`, `must_remove`, `compliance`, `fixes` and `switch_off_cost`.
- [`test_lootlaw.py`](lab07-starter/test_lootlaw.py): seven tests built from the lecture's table, its cost example and its check-yourself answers. All seven fail on the starter. Run them from the repository root:

```
.venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab07-starter/test_lootlaw.py
```

- The interactive `examples/w07-loot-box-law-map.html`, for checking single designs by hand.

## Steps

1. **Rules.** Implement `assess` for all eight markets exactly as the lecture's rule table states, then `assess_all` and `must_remove`. Run the tests. The first four should pass.
2. **Compliance.** Implement `compliance`. A market that only asks for odds is a "breach" if odds are hidden. The UK guidance is a "gap", not a breach, because it is voluntary. Ratings are "ok": they are not violations, though they may still hurt your audience.
3. **Fixes.** Implement `fixes`, a breadth-first search over sets of changes. Return every smallest set that clears the markets you pass in. Check it against the lecture: for preset A across all markets, the only one-change fixes are "paid off" and "chance off".
4. **Costs.** Implement `switch_off_cost`. The tests use the lecture's $50 million example ($180,000 regional against $7.5 million global) and check-yourself question 3 ($72,000).
5. **A real game.** Choose one live game with paid random rewards that you can inspect (the store, the rating and the trading rules must be publicly documented). Encode it as a `Design`. Cite where each fact comes from. Where `S` or `M` is arguable, run both values and report both.
6. **Sensitivity.** Using `fixes`, find the smallest change that clears (a) Belgium only, (b) the Netherlands and the UK, (c) all eight markets. For each, say in one sentence what that change would do to the player's experience.
7. **Check the date.** Pick two rows of the rule table and check whether anything has changed since 28 September 2026. Record what you checked and where.

## Deliverable

Your completed `lootlaw.py` with all tests passing, and an individual memo of at most 400 words addressed to the game's producer. The memo must state the encoded facts with sources, the outcome in each market, the recommended option (regional switch-off, redesign, or both) with its cost estimate and assumptions (`s_m`, `b`, `k`), one design change that reduces exposure next year, and a one-line disclaimer that this is a model, not legal advice.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All seven tests pass; `fixes` is a real search, not hard-coded; readable | Tests pass with special cases | Tests fail | 30% |
| Encoding the real game | Every fact sourced; arguable facts run both ways and discussed | Facts stated with some sources | Facts guessed or unsourced | 20% |
| Analysis | Correct outcomes, fixes and costs; sensitivity tied to player experience | Outcomes correct, thin sensitivity | Outcomes wrong or missing | 25% |
| Currency of the law | Two rows re-checked with dated primary sources; changes noted | Checked with secondary sources | Not checked | 10% |
| Memo | Plain, numeric, balanced, within 400 words, disclaimer present | Correct but long or vague | Hard to act on | 15% |
