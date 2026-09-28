# DB201 · Final service brief: a persistent inventory service with telemetry

**Weight:** 60% of the course grade.
**Assigned:** week 6, after Lab 06. **Milestone 1:** end of week 8. **Milestone 2:** end of week 12. **Final submission:** start of week 15, followed by a 20-minute demo and viva in week 15.
**Work mode:** individual, or a pair with a signed contribution statement. In a pair, each partner answers the viva questions alone.
**Lectures:** all fourteen, most directly [week 2, relational modeling](../lectures/w02-relational-modeling-characters-inventories-items.md), [week 5, transactions](../lectures/w05-transactions-and-acid.md), [week 6, the duplication bug](../lectures/w06-race-conditions-and-the-duplication-bug.md), [week 8, write-behind](../lectures/w08-caching-and-write-behind.md), [week 9, migrations](../lectures/w09-schema-migrations-in-a-live-game.md), [week 11, pipelines](../lectures/w11-pipelines-collect-store-query.md), [week 13, privacy](../lectures/w13-privacy-gdpr-and-data-retention.md) and [week 14, backups](../lectures/w14-backups-and-disaster-recovery.md).

## What this component is for

Each lab tests one technique on its own. This assessment asks you to put them together into the back end a small MMO would run. The service owns characters and items, never duplicates or loses either under concurrent load, records what players do as telemetry, forgets a player when asked, and comes back after a disaster. A service that "works when I click it" earns little here. A service that states its dupe rate under 2,000 concurrent attempts, its worst migration stall, its KPI definitions, its rows examined per erasure and its measured RPO and RTO earns a lot.

It assesses all three course outcomes. The schema, queries and indexes assess "model game entities relationally and query them with SQL". The trade path and its stress test assess "use transactions to prevent item duplication". The tracking plan, pipeline and dashboard assess "instrument a game with telemetry events and build dashboards".

## What you build

A Python service (a module with a small command-line interface is enough; an HTTP API is optional) over SQLite, built from your own lab code. There is no starter. Your Lab 02 schema, Lab 06 handlers, Lab 08 flusher, Lab 09 backfill, Lab 11 loader, Lab 12 queries, Lab 13 erasure and Lab 14 backup code are the parts, and this brief says how they must fit.

### Technical rules

- Python 3.10 or later with the standard library only. It must run with `.venv/bin/python` on a clean copy of your repository.
- SQLite is the system of record. You may also target PostgreSQL, but the marked run uses SQLite. Where your design depends on a PostgreSQL feature (row locks, partitions, `synchronous_commit`), write the PostgreSQL version in a comment next to the SQLite one.
- The cache may be an in-process dictionary or Redis. If you use Redis, the service must still start and pass its checks with the cache disabled.
- Every random process takes a seed, and every measurement in your report names the seed and the command that produced it.
- One command, `python -m service check` (or an equivalent you name in the README), runs every automatic check below and prints PASS or FAIL per line.

### Required features

1. **Schema.** Characters, item types, items in the row model, a trade log and a `schema_migrations` table, with the Lab 02 rules enforced by constraints: unique names, non-negative gold, real owners and types, no empty stacks, one stack per slot, and the stack-limit trigger. Foreign keys are on for every connection.
2. **Operations.** At least `create_character`, `grant_item` (loot), `move_item` (bag and slot), `trade` (items and gold both ways between two characters), `sell_to_vendor` and `destroy_item`. Every operation that creates, moves or destroys value runs as one transaction and writes one log row in that transaction.
3. **Concurrency.** The trade path uses conditional updates, ordered locks or a version check (week 6), and returns `rejected` or `conflict` instead of partly succeeding. A stress harness fires 2,000 pairs of conflicting trades from threads, with jitter, and reports dupes and losses. An audit query checks that total gold equals the logged faucets minus the logged sinks, and that no item id appears twice.
4. **Indexes.** The three hottest queries (load a character's items, one bag in slot order, and one other you choose) each have an index you justify, with its `EXPLAIN QUERY PLAN` line before and after, measured on a world of at least 2,000 characters with 150 items each.
5. **Write-behind state.** Position and health live in a cache and reach the database through a flusher with a dirty set, one transaction per batch and a versioned upsert (week 8). The service flushes a character before any trade that involves them, on logout and before a backup.
6. **One live migration.** Add a column the design needs (durability, soulbound or another of your choice) with the expand, backfill, enforce and contract steps of week 9. The backfill is batched by primary-key range, idempotent and resumable, and it runs while a load generator keeps trading. Report the worst stall a game write saw next to `b / r`.
7. **Telemetry.** A tracking plan of at least five events, each tied to a question it answers. Value events (`item_created`, `item_traded`, `gold_changed`, `item_destroyed`) come from the server, inside or right after the transaction that caused them. Events carry the week 10 envelope with a pseudonymous `telemetry_id` instead of `player_id`. An idempotent loader, daily rollups built with a stated lateness policy, and at least four KPI queries: DAU under a stated definition, D1 retention, items created and destroyed per day, and gold faucets and sinks per day.
8. **Privacy.** A pseudonym table, an erasure command that removes a player's link to every event in a small, stated number of rows, a subject access export, and a retention job that drops whole day tables. A retention schedule for every store your service keeps.
9. **Backups.** A backup command using SQLite's online backup API, a verification that fails loudly on an empty or truncated file, a log or change feed you can replay to a chosen moment, and a restore drill whose measured RPO and RTO appear in your report. The restore procedure re-applies erasures made after the backup.

## The design report

At most 2,500 words plus tables, as `REPORT.md`. It has six sections, and each one leads with numbers.

1. **Persistence policy.** A table of every kind of state your service holds, with its path (write-through transaction, write-behind with `T`, or telemetry only), the loss a crash can cause, and why that loss is acceptable.
2. **Concurrency evidence.** The stress results for your trade path and for a deliberately naive version, the audit query and its output, and one interleaving traced step by step.
3. **Queries and indexes.** The three hot queries with plans, timings and page counts, and one index you chose not to create, with its write cost.
4. **Migration.** The step list with the server version shipped at each step, your fitted `r` and `o`, the stall table, and the plan scaled to 60 million rows.
5. **Telemetry and dashboard.** The tracking plan, storage per day at your load and at 40,000 DAU, the rollups with their grain, and a dashboard specification of four to six tiles, each with a question, a definition footnote, a baseline and a refresh schedule.
6. **Privacy and recovery.** Rows examined per erasure, the retention schedule, the backup schedule with RPO and RTO arithmetic, measured drill numbers, and the restore runbook (two pages at most, as an appendix).

## Deliverables

- A repository link or zip with the service, `schema.sql`, the `migrations/` folder, the tracking plan, the stress harness, the load generator, the backup and restore scripts, and a README with the exact commands to reproduce every number in the report.
- `REPORT.md` and the runbook appendix.
- A contribution statement if you work in a pair.

## Milestone 1: schema and trade path (end of week 8, 10 points)

Submit `schema.sql`, the six operations, the trade path with its stress harness, and the persistence policy table. Show the stress output for your trade path and for a naive trade (it should dupe), and the audit query's output after the run. Feedback within a week tells you whether the design will survive the later features.

## Milestone 2: cache, migration and telemetry (end of week 12, 10 points)

Submit the write-behind flusher with a measured write rate next to `N × (1 − e^(−uT)) / T` for one setting, the migration run with its stall table, the tracking plan, and the loader passing an idempotence test (load the same file twice, same row count). One KPI query with its output is enough at this stage.

## Demo and viva (week 15, 20 minutes)

The marker clones your repository and follows your README. In order:

1. `check` runs every automatic check, and all pass.
2. The stress harness runs 2,000 conflicting trade pairs. Dupes and losses are both 0, and the audit query passes.
3. The migration runs under load, and the worst stall is printed next to `b / r`.
4. A player is erased. The export for that player is empty afterwards, and the rows examined are printed.
5. The live database is deleted. The restore drill brings it back, prints the RPO and RTO, and the audit query passes on the restored copy.

Then 10 minutes of questions in the style of the [exam bank](exam-bank.md) (questions 63 to 65 especially), asked about your own code and numbers. For example, "Your flusher runs every 5 s. What does a crash lose on average, and why can it not dupe an item?" or "Your erasure examines 3 rows. What in your event schema could still identify that player?"

## Rubric

### Milestones (20 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: schema and constraints | 5: every Lab 02 rule enforced by a constraint or trigger; foreign keys on; each rule mapped to its constraint | 3 to 4: one rule left to code without a reason | 1 to 2: several rules unenforced | 0 | 5 |
| M1: trade path | 5: one transaction per trade; 0 dupes in 2,000 stress pairs; naive version shown duping; audit passes | 3 to 4: correct, stress run smaller or audit missing | 1 to 2: transactional but dupes under stress | 0 | 5 |
| M2: cache and migration | 5: measured write rate within 10% of the model; migration batched, idempotent, with a stall table beside `b / r` | 3 to 4: one of the two without measurements | 1 to 2: cache or migration missing | 0 | 5 |
| M2: telemetry start | 5: plan ties every event to a question; server-sourced value events; loader passes the idempotence test; one KPI | 3 to 4: plan or loader incomplete | 1 to 2: events without a plan | 0 | 5 |

### Final submission, demo and viva (80 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Schema, queries and indexes | 9 to 10: constraints enforce every rule; three hot queries with plans before and after, timings and page counts on a 300,000-item world; one rejected index argued with its write cost | 7 to 8: plans present, one justification thin | 4 to 6: indexes added without plans or measurements | 0 to 3: blob inventory for items, or constraints missing | 10 |
| Trades and concurrency | 15 to 16: every value-moving operation is one transaction with a log row; 0 dupes and 0 losses in 2,000 stress pairs; lock order or conditional updates explained; audit query passes after the run; one interleaving traced | 11 to 14: correct, one piece of evidence missing | 6 to 10: correct alone, untested under concurrency | 0 to 5: any dupe under stress, or a trade that can half-commit | 16 |
| Caching and migration | 9 to 10: flusher swaps the dirty set, batches in one transaction, refuses stale versions, flushes before trades and logout; migration follows expand, backfill, enforce, contract with the stall table and a 60-million-row plan | 7 to 8: both work, one measurement or step missing | 4 to 6: one of the two missing or unsafe to rerun | 0 to 3: neither | 10 |
| Telemetry pipeline and KPIs | 11 to 12: plan with questions and a denominator event; envelope with `telemetry_id`; idempotent loader; rollups with stated grain and lateness policy; four KPI queries with definitions; dashboard spec with footnotes and baselines | 8 to 10: one element thin | 4 to 7: events recorded but KPIs undefined or rollups not rerunnable | 0 to 3: counters only, or client-sourced value events | 12 |
| Privacy and retention | 7 to 8: erasure through the pseudonym table in a stated number of rows; access export empty after erasure; retention by dropping day tables; schedule covers every store including backups and cache | 5 to 6: works, schedule incomplete | 3 to 4: erasure by scan only, or identifiers left in events | 0 to 2: missing | 8 |
| Backups and recovery | 9 to 10: verified backups that fail loudly when broken; restore to a chosen moment; measured RPO and RTO next to the model's; erasures re-applied; runbook a stranger could follow at 3 a.m. | 7 to 8: restore works, verification or runbook thin | 4 to 6: backup without a tested restore | 0 to 3: missing | 10 |
| Design report | 6: every section leads with numbers from your own runs, and each design choice names its cost | 4 to 5: one section without numbers | 2 to 3: descriptive, few numbers | 0 to 1: missing | 6 |
| Demo and viva | 7 to 8: all five demo steps work from a clean clone; answers use your own code and numbers | 5 to 6: one step needs help | 3 to 4: two steps fail, or answers vague | 0 to 2: cannot run or explain the service | 8 |
| **Total** | | | | | **80** |

Milestones and final together total **100**. The component mark is that total multiplied by 0.60.

Two hard limits apply whatever the rest of the work looks like. A single dupe in the marked stress run caps "Trades and concurrency" at 5 points. A restore that has never been run caps "Backups and recovery" at 3 points, because an untested backup has an unknown RPO.

## Rules and advice

- **Build on the compulsory labs.** Labs 05, 06, 13 and 14 are compulsory in the [SQL labs](sql-labs-brief.md) because this service needs them. Start the service in week 6 from your Lab 06 handlers, not in week 14.
- **Measure before you claim.** Every number in the report comes from a command in your README. A number from the lectures may appear as a prediction next to yours, never instead of yours.
- **Keep the data invented.** Generate characters and sessions from a seed. No real player data, no scraped data, no names of real people.
- **Late submission.** The final submission loses 5 points per day late, for up to 3 days. After that it is not accepted without an extension under the university policy. Demo slots are fixed, so a late submission is demonstrated in its original slot from whatever the repository holds.
- **Integrity.** You may reuse any lecture or starter code and your own lab code. You may use documentation, forums and AI assistants to understand errors and APIs, and you must say so in one line per use in the README. You may not submit code you cannot explain in the viva, and you may not copy another student's measurements.
