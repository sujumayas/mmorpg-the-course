# DB201 · Lab 03: Eight questions about a generated world

**Week:** 3 ([SQL I: select, join, aggregate](../lectures/w03-sql-i-select-join-aggregate.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** in pairs (pair programming, swap the keyboard every query)

## Objective

Answer eight designer questions with SQL against a 1,200-character world, prove each answer against values computed without SQL, and measure the fan-out trap from lecture on real data before fixing it.

## Starter materials

- Python 3.10 or later with its built-in `sqlite3` module. In this repository use `.venv/bin/python`.
- `labs/lab03-starter/build_db.py`: builds `game.db` with seed 303. Tables `item_types` (300 rows), `characters` (1,200), `items` (27,684), `quest_completions` (7,863). The schema matches the Lab 02 reference, plus `quest_completions (character_id, quest_id, completed_day)`.
- `labs/lab03-starter/queries/q01.sql` to `q08.sql`: each holds the question, the required columns and the required order as comments. You write the query below the comments.
- `labs/lab03-starter/run_queries.py`: runs each query and compares the result with answers computed in plain Python from the same generator. Run `python run_queries.py` for all, or `python run_queries.py 6` for one. It builds `game.db` if it is missing.
- Optional: the `sqlite3` command-line shell, or any SQLite browser, for exploring (`.schema`, `.mode box`).

## Steps

### Part A: warm-up (30 minutes)

1. Run `python build_db.py`. Open `game.db` and run `SELECT COUNT(*)` on each table. Record the four counts and the grain of each table in one sentence ("one row per ...").
2. Write q01 (characters per class), q02 (five richest) and q05 (gold per class). Run the checker after each.

### Part B: joins (40 minutes)

3. Write q03 (total quantity per rarity). Before running it, state why joining `items` to `item_types` cannot inflate the sum.
4. Write q04 (characters with no items) twice, once with `LEFT JOIN ... IS NULL` and once with `NOT EXISTS`. Keep the one you find clearer in the file and the other in your report.
5. Write q07 (five most valuable inventories at vendor prices). Note which column you grouped by and why PostgreSQL would accept selecting `name` with that grouping.

### Part C: the fan-out trap (30 minutes)

6. For q06, first write the naive query: `characters` inner joined to `items` and to `quest_completions`, grouped by class, with `SUM(gold)`, `COUNT(item_id)` and `COUNT(quest_id)`. Run it directly (not through the checker) and record its output and the row count of the join alone (`SELECT COUNT(*) FROM ... JOIN ... JOIN ...`).
7. For the warrior class, compute the inflation factor on gold (naive divided by true). Explain in two sentences, using `m₁ × m₂` from lecture, why it is so large.
8. Fix q06 by aggregating each child table first and joining with `LEFT JOIN` and `COALESCE`. The checker must say `OK`.

### Part D: groups and report (at home)

9. Write q08 (average level for classes with more than 250 characters). Explain why the filter belongs in `HAVING` and not in `WHERE`.
10. Write one more query of your own that a designer would plausibly ask (for example, "average quests completed per character, by level band of 10"). Give the question, the query, the grain of the working set after each join, and a hand check on a small slice of the data.

## Deliverable

The eight query files (all `OK` in the checker), plus a report with the table counts and grains (step 1), the alternative q04, the naive q06 output with its join row count and inflation factor, the `HAVING` explanation, and your own query from step 10.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct queries (40%) | 8/8 `OK` | 7/8 | 5-6 | Fewer than 5 |
| Fan-out analysis (25%) | Naive output, join row count and warrior inflation factor recorded; explanation uses match counts per character | Numbers recorded, explanation generic | Fix without the naive measurement | Missing |
| Reasoning about grain (15%) | Grains stated for all tables and for step 10's joins; q03 and q08 explanations correct | Minor gaps | Grain mentioned but not used | Missing |
| Own query (15%) | A realistic designer question, correct query, hand check that would catch a double count | Correct query, weak hand check | Query runs but answers a different question | Missing |
| Style (5%) | Consistent aliases, one clause per line, comments where the intent is not obvious | Minor issues | Hard to read | Missing |
