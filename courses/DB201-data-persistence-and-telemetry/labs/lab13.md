# DB201 · Lab 13: Retention and erasure

**Week:** 13, [privacy, GDPR and data retention](../lectures/w13-privacy-gdpr-and-data-retention.md)
**Time:** 2 hours in the lab plus about 2 hours at home
**Work:** individually

## Objective

Measure what an erasure request costs under three schemas, build the retention job and a subject access export, and see for yourself that `DELETE` leaves the bytes on disk. You finish with a retention schedule for your final project's inventory service.

## Starter materials

- `labs/lab13-starter/privacy_lab.py`. Python 3.10+ and the standard library only. It builds two telemetry stores in a temp folder:
  - a **naive** store, where every event carries `player_id` and `display_name`;
  - a **pseudonymous** store, where events carry a random `telemetry_id` and a single `pseudonyms` table links it to the account.
- Both stores keep one table per day (`events_d000`, `events_d001`, ...), which is how the lab fakes PostgreSQL partitioning in SQLite.
- Parts B (scan and index erasure) and F (forensic check) are written for you. Parts C, D and E are functions marked `TODO`.

Run it from the starter folder:

```
python privacy_lab.py --check      # tests for your TODO functions only
python privacy_lab.py              # tests, then every measurement
python privacy_lab.py --players 1000 --days 20   # smaller, for slow laptops
```

On a 2025 laptop the full run takes about 2 seconds.

## Steps

**Part A. Predict (15 min).** Before running anything, use the lecture's model to predict the number of event rows in each store for the defaults (2,000 players, 40% active per day, 40 events each, 30 days). Predict the rows examined per request for strategies A, B and C. Write the predictions down.

**Part B. Measure the given strategies (15 min).** Run the program. Record rows examined, rows deleted and milliseconds per request for A and B, and the file size before and after building the indexes. Compare with Part A. Explain any gap in one sentence.

**Part C. Erase through the pseudonym (20 min).** Implement `erase_pseudonymous`. It deletes the mapping row and the account row, and does not touch any event table. Run `--check` until Part C passes, then record its line in the table.

**Part D. The retention job (20 min).** Implement `enforce_retention(con, today, keep_days)` with `DROP TABLE`. Time it at `keep_days = 7`. Then write a version with `DELETE FROM ... WHERE ts < ?` on a single combined table (make one with `CREATE TABLE all_events AS SELECT * FROM events_d000 UNION ALL ...`) and time that too. Report both times.

**Part E. Subject access export (25 min).** Implement `export_subject(con, player_id)` so it works on both stores. Show the export for one player before and after erasure in the pseudonymous store. In two sentences, explain why the post-erasure export is empty even though the events still exist.

**Part F. Deleted bytes (10 min).** Read the Part F output. Then add `con.execute("PRAGMA secure_delete = ON")` right after the forensic database is built and run again. Record the counts in the three states for both runs.

**Part G. Scale it up (at home).** Use the lecture's formulas to scale your Part B measurements to the section 2 game (40,000 daily players, 1,500 events each, R = 395). Estimate monthly scan hours for 300 per-request scans and for weekly batches, and compare with the lecture's table.

## Deliverable

1. `privacy_lab.py` with Parts C, D and E completed and `--check` passing.
2. A results table covering predictions and measurements for Parts A to F.
3. A memo of at most 600 words:
   - which erasure strategy your final inventory service will use and why;
   - one thing strategy C does **not** protect against, with an example event from your own telemetry design;
   - a retention schedule with at least five rows (category, purpose, window, deletion mechanism, erasure strategy) for your final service.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half) | Missing (zero) | Points |
|---|---|---|---|---|
| Parts C, D, E correct | `--check` passes; code is short and uses `DROP TABLE` for retention | Passes with workarounds or uses `DELETE` for retention | Tests fail | 30 |
| Predictions vs measurements | All predictions shown, gaps explained with the model | Measurements without predictions or explanations | Missing | 15 |
| Retention timing comparison | Both timings, with the reason `DROP` is faster in one sentence | One timing | Missing | 10 |
| Forensic findings | Counts for DELETE, VACUUM and secure_delete, correctly interpreted | Counts without interpretation | Missing | 10 |
| Scale-up (Part G) | Correct arithmetic matching the lecture's model | Minor arithmetic errors | Missing | 10 |
| Memo and schedule | Justified choice, a concrete re-identification risk from own design, five complete schedule rows | Generic risk or incomplete schedule | Missing | 25 |
| **Total** | | | | **100** |
