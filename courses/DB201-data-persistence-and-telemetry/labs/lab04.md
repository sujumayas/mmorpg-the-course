# DB201 · Lab 04: Scans, indexes and query plans

**Week:** 4 ([SQL II: indexes and query plans](../lectures/w04-sql-ii-indexes-and-query-plans.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare numbers with a neighbour at the end

## Objective

Build a 1.2-million-row items table, read the plan SQLite chooses for an owner lookup before and after an index, and check the lecture's page model against what the file actually contains. Then find a query where the index does not pay off, and measure what indexes cost on every insert. By the end you should be able to recommend an index set for a game table with numbers, not habit.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- `labs/lab04-starter/index_lab.py`, which contains:
  - `build(path, n_chars, clustered)`: complete. Creates `items` without any secondary index and inserts 120 items per character. By default the rows are shuffled so each character's items are scattered, as they are after months of play. `--clustered` keeps each character's items together.
  - `pages(con)`, `plan(con, sql, args)`, `time_queries(con, sql, arg_list)`: complete helpers for `PRAGMA page_count`, `EXPLAIN QUERY PLAN` and best-of-N timing.
  - `btree_height(n_rows, fanout)` and `model_pages(n_rows, k, rows_per_page, fanout, scattered)`: complete. The lecture's model.
  - `selectivity(con, where_sql, args)`: you write it (Part C).
  - `insert_rate(con, n_rows)`: you write it (Part D).
- Run `python index_lab.py` (about 4 seconds on a recent laptop), `python index_lab.py --clustered`, or `python index_lab.py --chars 2000` on a slow machine.
- Reference output from the lecturer's machine (Apple silicon, Python 3.13, SQLite 3.53): 24,554 pages of 4,096 bytes, 48.9 rows per page; owner lookup 32.9 ms with `SCAN items`, 0.148 ms with `SEARCH items USING INDEX`; clustered 0.065 ms. Your times will differ. The plans and ratios should not differ much.

## Steps

### Part A: the table without an index (20 minutes)

1. Run the script once without changes. Record the rows, pages, page size, rows per page, the plan and the time for the owner lookup.
2. From your page size and rows per page, estimate the average bytes per row including overhead. Compare it with the lecture's 100-byte assumption.
3. Using the lecture's model with your measured `R`, compute the pages a full scan reads for 10,000 characters and for 1,000,000 characters (120 items each).

### Part B: the owner index (25 minutes)

4. Record the index build time, the new page count, and the plan and time after `CREATE INDEX idx_items_owner`. Compute the speed-up and the index's size as a percentage of the table.
5. Run `--clustered` and record the same numbers. Explain in two sentences why the index lookup got faster while the scan did not, using the terms heap page and `k`.
6. Run with `--chars 1000`, `--chars 5000` and `--chars 20000` (scattered). Tabulate scan time and index time against the row count. Which one grows in proportion to `N`? Fit your table to the lecture's model in one sentence.

### Part C: when the index loses (30 minutes)

7. Implement `selectivity`. Report the selectivity of an owner lookup and of the potion query (`type_id = 7`).
8. Record the potion query's time through `idx_items_type` and with `NOT INDEXED` (forced scan). Compute the crossover selectivity `s* = 1 / (c_r × R)` for `c_r = 4` and for `c_r = 1`. Which value of `c_r` explains your measurement, and why?
9. Add a query of your own with a selectivity between the owner lookup and the potion query, for example `type_id BETWEEN 1 AND 10`. Time it both ways, and say whether it lands on the side of the crossover your chosen `c_r` predicts.
10. Write three `WHERE` clauses on `items` that cannot use `idx_items_owner` even though they mention `owner_id`. Confirm each with `plan()`.

### Part D: what indexes cost (25 minutes)

11. Implement `insert_rate`. Insert 20,000 rows in one transaction, measure rows per second, and roll back so the table size does not drift.
12. Record the rates with two secondary indexes and with none. Then add a third index on `(owner_id, bag, slot)` and measure again.
13. A telemetry table receives 16,700 inserts per second at peak (the lecture's combat-event estimate). Using your rates, how many indexes can it carry before inserts take more than half of one core? State your assumptions.

### Part E: the recommendation (at home)

14. Write a one-page index recommendation for the in-class auction house (2 million listings; queries A, B and C from the lecture's activity). For each index, give its columns in order, the query it serves, that query's estimated selectivity, and its insert cost from your Part D numbers. Name one index you chose not to create and why.

## Deliverable

Your modified `index_lab.py`, a results file (text, spreadsheet or notebook) with the tables from steps 1, 4 to 6, 8, 9 and 12, the three `WHERE` clauses from step 10 with their plans, and the recommendation as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Model against measurement (25%) | Page counts, `R` and bytes per row computed from your own output; scaling table in step 6 matched to the model with a stated growth rate | Numbers right, the link to the model thin | Some numbers copied from the reference output | Not attempted |
| Plans (20%) | Every timing paired with its plan; three non-sargable `WHERE` clauses shown with plans and a reason each | Plans present, one reason missing | Timings without plans | Missing |
| Selectivity and crossover (25%) | `selectivity` correct; `s*` for both `c_r`; the measurement explained by caching; own query placed correctly | Crossover computed, caching explanation vague | Crossover missing or wrong | Missing |
| Write cost (15%) | Three insert rates; the step 13 answer uses them with stated assumptions | Rates present, step 13 hand-waved | One rate only | Missing |
| Recommendation (15%) | Every index justified with query, selectivity and cost; one rejected index argued | Indexes listed with partial justification | Indexes listed only | Missing |
