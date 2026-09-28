# DB201 · Lab 02: An inventory schema that enforces the rules

**Week:** 2 ([Relational modeling: characters, inventories, items](../lectures/w02-relational-modeling-characters-inventories-items.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually

## Objective

Write a relational schema for characters, item types, items and affixes in which the database itself rejects impossible game states, then measure the blob and row designs on a generated world of 300,000 items.

## Starter materials

- Python 3.10 or later with its built-in `sqlite3` module (SQLite 3.38 or later, for JSON functions). In this repository use `.venv/bin/python`.
- `labs/lab02-starter/schema.sql`: empty except for comments. You write it.
- `labs/lab02-starter/check_schema.py`: the checker. It runs your schema on a fresh database with `PRAGMA foreign_keys = ON`, loads a three-item base world, and runs 12 required tests, each on a fresh copy, plus one stretch test. If all 12 pass it builds a 2,000-character world with 150 items each in two designs (your row schema, and a JSON blob per character) and prints sizes and timings.
- Run `python check_schema.py`, or `python check_schema.py --tests-only` while you iterate.

## Steps

### Part A: the tables (40 minutes)

1. Write four tables in `schema.sql` with exactly these names and columns (types and constraints are your job):
   - `item_types (type_id, name, rarity, max_stack, vendor_price)`
   - `characters (character_id, name, class, level, gold)`
   - `items (item_id, type_id, owner_id, bag, slot, quantity, durability)`
   - `item_affixes (item_id, stat, value)`
2. Run the checker. For each failing test, find the game rule it describes and add the constraint that enforces it. Do not edit the checker.
3. When 12/12 pass, write down for each test which constraint made it pass. Three tests are passed by foreign keys; for each, say which table is being protected from what.

### Part B: the NULL trap and the stretch trigger (25 minutes)

4. Temporarily make `bag` nullable and change the base-data insert in a scratch copy of the checker so both items have `bag = NULL` and the same slot. Does your `UNIQUE` constraint reject the second one? Explain the result in one sentence, then restore `bag NOT NULL`.
5. Stretch: write a `BEFORE INSERT` trigger on `items` that aborts when `quantity` exceeds the type's `max_stack`. The stretch line of the checker changes from `no` to `OK`. Explain why a `CHECK` constraint cannot do this.

### Part C: measure the two designs (30 minutes)

6. Run the full checker without any `CREATE INDEX` in your schema and copy the measurement block into your report.
7. Add `CREATE INDEX ... ON items(type_id)` and run it again. Record the new query plan line and the time for "how many of type 42 exist?"
8. Compare with the lecture's model. Using the average blob size the checker prints, compute the bytes rewritten by one item move in the blob design and the ratio to one row. Explain why `blob.db` is larger than `rows.db` even though the lecture's model predicted similar sizes.

### Part D: recommendation (at home)

9. In at most 300 words, recommend which parts of a character in an MMO of your choice belong in rows and which in a JSON column. Use at least three of your measured numbers. Name one operation where the blob design wins and say whether it matters for your game.

## Deliverable

`schema.sql`, the checker output from steps 6 and 7, and a report with the answers to steps 3, 4, 5 (if attempted) and 8, plus the recommendation.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Schema correctness (30%) | 12/12 tests pass; types sensible; each test mapped to its constraint | 12/12, mapping incomplete | 9-11 pass | Fewer than 9 |
| Rules and traps (20%) | NULL trap explained correctly; trigger works and the `CHECK` limitation is explained | NULL trap explained, no trigger | Explanation vague | Missing |
| Measurement (25%) | Both runs recorded; index effect shown with the plan line; move-cost ratio computed; size difference explained by repeated JSON keys | Runs recorded, one analysis missing | Numbers without analysis | Missing |
| Recommendation (20%) | Clear split with reasons, three or more own numbers, the blob's winning case named and weighed | Split with numbers, weak on the blob case | Split without numbers | Missing |
| Presentation (5%) | Schema readable, commented where a rule is not obvious | Minor issues | Hard to read | Missing |
