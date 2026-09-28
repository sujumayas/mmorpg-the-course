# DB201 · Lab 14: Disaster-recovery drill

**Week:** 14, [backups and disaster recovery](../lectures/w14-backups-and-disaster-recovery.md)
**Time:** 2 hours in the lab plus about 2 hours at home
**Work:** pairs

## Objective

Restore a game database from base backups and an archived log after two kinds of disaster, measure the RPO and RTO you actually get, and build the verification that would have caught GitLab's silent backup failure. You finish with a restore runbook for your final service.

## Starter materials

- `labs/lab14-starter/dr_drill.py`. Python 3.10+ and the standard library only. It simulates a game server with 500 characters doing loot, trades and vendor sales at 20 transactions per game second. It takes base backups with SQLite's online backup API and archives a logical transaction log in segments. The file header maps each piece to its PostgreSQL equivalent (`pg_basebackup`, `archive_command`, `archive_timeout`, `recovery_target_time`).
- Drill 1 deletes the live database mid-segment. Drill 2 runs a GM script that sets every character's gold to 0 at t = 700.
- Parts B, C and D are functions marked `TODO`. The simulation is deterministic, so everyone gets the same numbers.

Run it from the starter folder:

```
python dr_drill.py --check                 # tests for your TODO functions only
python dr_drill.py                         # base every 600 s, archive every 60 s
python dr_drill.py --base 1800 --archive 5 # another policy
```

A full run takes about 10 seconds on a 2025 laptop.

## Steps

**Part A. Read the server (15 min).** Read `Server.run`, `take_base_backup`, `archive_segment` and `disaster`. Answer in your notes: which records are lost in a disaster, and why does every transaction also write `last_txn` and `clock` into the `meta` table?

**Part B. Point-in-time restore (35 min).** Implement `restore_to(bases, archive_dir, target_t, out_path)` as described in its docstring. Pass `--check`, then run the default drill. Record the base used, records replayed, replay time and the RPO in seconds and transactions. Confirm that drill 2 restores the gold total exactly.

**Part C. Verify backups (20 min).** Implement `verify_base_backup(path)`. It must return an empty list for a good backup and at least one problem for an empty or truncated file. Then break the server on purpose: change `take_base_backup` so that every third backup writes an empty file, the way GitLab's job produced nothing. Show that your verifier catches it.

**Part D. The model (15 min).** Implement `model(...)` from the lecture. Use it to fill in the lecture's five-policy table, and add one row for your own policy.

**Part E. Four policies, measured (at home).** Run the drill with `--base/--archive` set to (600, 60), (1800, 60), (600, 5) and (150, 60). For each, record the RPO in seconds, records replayed and replay wall time. Plot replay time against the base interval and RPO against the archive interval. Say in two sentences which knob moves which number, and whether your data agrees with the lecture.

**Part F. The operator mistake (at home).** In drill 2, restoring to t = 699 throws away 200 seconds of legitimate play. Write `selective_repair(live_con, restored_con)` that copies only the `gold` column from the restored copy into the live database. Then find one transaction in the log after t = 700 that makes the repaired state questionable (hint: a trade where the buyer's gold was 0 or near 0). Describe what you would tell that player.

## Deliverable

1. `dr_drill.py` with Parts B, C, D and F completed and `--check` passing.
2. The Part E table and two plots.
3. A restore runbook for your final inventory service, at most two pages: the backup schedule with the RPO and RTO arithmetic, numbered restore steps (including re-applying week 13 erasures and verification), who is paged, and how you announce a rollback to players.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half) | Missing (zero) | Points |
|---|---|---|---|---|
| Restore correct (Part B) | `--check` passes; drill 2 matches history exactly | Restores but fingerprint differs or picks the wrong base | Does not restore | 25 |
| Verification (Part C) | Catches empty, truncated and sabotaged backups with clear messages | Catches some cases | Missing | 15 |
| Model (Part D) | Correct, table filled, own policy justified | Correct formulas, table incomplete | Missing | 10 |
| Measurements (Part E) | Four runs, two plots, conclusion supported by the data | Runs without plots or conclusion | Missing | 15 |
| Selective repair (Part F) | Working repair plus a specific questionable transaction and a player-facing answer | Repair only | Missing | 15 |
| Runbook | Arithmetic, steps a stranger could follow at 3 a.m., erasure step, verification, communication | Steps without arithmetic or missing erasure/verification | Missing | 20 |
| **Total** | | | | **100** |
