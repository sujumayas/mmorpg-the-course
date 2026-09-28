# DB201 · Week 09 — Schema Migrations in a Live Game

**Why this matters:** Every patch that adds a stat, a currency or an item property changes the database. In a single-player game you rewrite the save file when the player loads it. In an MMO you change one table with tens of millions of rows while players keep trading out of it. Do it carelessly and you either take the servers down for an hour or freeze every trade in the game while a migration runs.

**You will be able to:**
- Classify a schema change as metadata-only, scan, or rewrite in PostgreSQL, and estimate how long each takes on a table of known size.
- Compute the total time and the longest write stall of a batched backfill from its batch size, row rate, per-batch overhead and duty cycle.
- Design an expand, migrate and contract sequence that keeps old and new server code working throughout a rolling deploy.
- Write a versioned migration and a batched backfill in SQL, and say where PostgreSQL behaves differently from SQLite.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 2, the section on schema flexibility in the document model (schema-on-read versus schema-on-write). PostgreSQL documentation, `ALTER TABLE`, the Notes section (about two pages). Xu, J., "Online migrations at scale", Stripe engineering blog (February 2017), about 10 minutes.

**Prerequisites from earlier courses:** [DB201 week 7, key-value stores](w07-nosql-and-key-value-stores-redis.md) (schema-on-read in document stores). [DB201 week 8, caching and write-behind](w08-caching-and-write-behind.md) (version numbers and idempotent writes). From this course, [week 2, relational modeling](w02-relational-modeling-characters-inventories-items.md) (the item tables), [week 4, indexes and query plans](w04-sql-ii-indexes-and-query-plans.md) and [week 5, transactions and ACID](w05-transactions-and-acid.md) (transactions and locks). Versioned data files and validation, [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md).

**Interactive:** [Backfill batches](../examples/w09-backfill-batches.html). Keep it open during section 2.

---

## 1. Why a live game makes migrations hard

A **schema migration** is a change to the structure of the database: a new column, a new table, a changed type, a new constraint or index. The data usually has to change with it, for example filling the new column for rows that already exist. That second step is a **backfill**.

Three facts about MMOs make migrations harder than in a typical web app.

**The tables are big and hot.** An item table holds one row per item instance in the world. A few hundred thousand characters with a few hundred items each is tens of millions of rows. And unlike an archive table, it is written to constantly, every loot drop, trade, repair and sale.

**Downtime is scheduled, short and public.** Some games keep a regular maintenance window. EVE Online shuts its server every day from 11:00 UTC, nominally for 15 minutes, and deploys patches in that window. Old School RuneScape ships its weekly update on Wednesdays at about 11:30 UTC. A large update comes with an in-game countdown, usually 45 minutes, before players are logged out. Its smaller hotfixes go out without a restart or timer. Either way, a migration has a hard time budget, and players notice when it runs over.

**Old and new code run at the same time.** Unless every server stops at once, a deploy rolls through the fleet. For some minutes, version 41 and version 42 of the server both talk to the same database. The schema must work for both.

### Three kinds of change, three costs

PostgreSQL's `ALTER TABLE` documentation tells you, subform by subform, how much work a change does. You can sort almost every change into three bins:

| Kind | What the database does | Time on a 60M-row table | Examples (PostgreSQL 11 and later) |
|---|---|---|---|
| Metadata-only | Updates the catalog, touches no rows | Milliseconds | `ADD COLUMN` with no default or a constant default; `DROP COLUMN`; renames |
| Scan | Reads every row to check something, writes nothing | Proportional to table size, read speed | `SET NOT NULL`; `ADD CONSTRAINT ... CHECK`; `VALIDATE CONSTRAINT` |
| Rewrite | Writes a new copy of the table and all its indexes | Proportional to table plus index size, write speed | `ALTER COLUMN ... TYPE` in most cases; `ADD COLUMN` with a volatile default such as `clock_timestamp()` |

The first row has a history. Before PostgreSQL 11 (released October 2018), adding a column with any non-null default rewrote the whole table. PostgreSQL 11 added a fast path. A constant default is stored once in the catalog and returned for old rows when they are read. So "is this fast?" depends on the version, which is why every migration plan should name the database version it assumes.

**Locks.** Unless the documentation notes otherwise for a subform, `ALTER TABLE` takes an `ACCESS EXCLUSIVE` lock, which conflicts with everything, including plain `SELECT`. For a metadata-only change the lock is held for milliseconds, which is fine. But the `ALTER` must first *get* the lock, and it waits for every open transaction that has touched the table. A migration that waits behind a long report query is a risk you do not want. Set `lock_timeout` (for example `SET lock_timeout = '2s'`) so the migration gives up quickly, and retry it a moment later.

SQLite, which you use in the labs, has the same fast path for plain `ADD COLUMN`. Its documentation says the time is independent of the amount of data. It does not allow a non-constant default in `ADD COLUMN` at all, and it has no general `ALTER COLUMN ... TYPE`. Changing a type there means building a new table and copying. SQLite also locks the whole database for writers, not single rows, so a long write transaction in the lab blocks every other writer. PostgreSQL blocks only writers of the rows involved.

## 2. Worked example: backfilling 60 million items without freezing trades

### The hook

Your MMO's next patch adds item durability. Weapons and armor lose durability in combat and must be repaired. Every existing item needs a starting value, and that value depends on the item type. A starter sword has 40, and a raid helm has 120.

The expand step is easy: `ALTER TABLE item_instance ADD COLUMN durability smallint;` is metadata-only. The problem is filling it. The obvious statement is:

```sql
UPDATE item_instance i
SET durability = d.max_durability
FROM item_def d
WHERE d.id = i.def_id;
```

Your table has 60 million rows. Your staging tests show the database updates about 20,000 of these rows a second (you will measure your own number in the lab). One statement means 60,000,000 / 20,000 = 3,000 seconds, 50 minutes. Even EVE's daily window is 15 minutes. And during those 50 minutes, every row the statement has updated stays locked until it commits. Any trade, repair or sale that touches one of those items waits until the very end.

So you cannot do it in the window, and you cannot do it in one go while the game runs. You need to split it.

### The model

Split the backfill into batches of `b` rows, each in its own short transaction, and pause between batches so the game keeps most of the database's capacity. Name every quantity:

- `N`: rows to backfill (60,000,000).
- `r`: rows per second the database can update while running a batch (20,000).
- `o`: fixed overhead per batch in seconds (commit, round trip, finding the next range), here 0.005 s.
- `d`: **duty cycle**, the fraction of time the backfill is allowed to run. `d = 0.25` means it runs a quarter of the time and pauses the rest.
- `b`: batch size, the knob you pick.

Each batch runs for `b / r + o` seconds and is followed by a pause that keeps the duty cycle at `d`. Then:

```
batches                  = N / b
longest write stall      = b / r                     (a writer waits for the batch holding its row)
total time               = (N / b) × (b / r + o) / d
                         = N / (r × d)  +  N × o / (b × d)
```

Read the last line slowly. The first term, `N / (r × d)`, does not depend on `b` at all. It is the time to do the real work at the speed you allowed. The second term is the overhead, and it only matters when `b` is small. The stall, meanwhile, depends only on `b`.

So the two knobs have separate jobs. **Batch size sets how long a player can be blocked. Duty cycle sets how long the whole backfill takes.** Overhead is what stops you from making batches tiny.

### Numbers you can check

With `N = 60,000,000`, `r = 20,000`, `o = 0.005` s and `d = 0.25`:

| Batch size b | Batches | Longest stall b/r | Total time | Total in hours |
|---|---|---|---|---|
| 60,000,000 (one statement, no pauses) | 1 | 3,000 s | 3,000 s | 0.83 |
| 100,000 | 600 | 5 s | 12,012 s | 3.34 |
| 10,000 | 6,000 | 0.5 s | 12,120 s | 3.37 |
| 1,000 | 60,000 | 0.05 s | 13,200 s | 3.67 |
| 100 | 600,000 | 0.005 s | 24,000 s | 6.67 |
| 10 | 6,000,000 | 0.0005 s | 132,000 s | 36.7 |

Check the 1,000 row. Each batch runs `1,000 / 20,000 + 0.005 = 0.055` s. Sixty thousand batches is 3,300 s of running time, and at `d = 0.25` the pauses stretch that to 13,200 s.

Now read down the table. From 100,000 rows to 1,000 rows per batch, the worst stall falls by a factor of 100, from 5 s to 50 ms, and the total time rises by 10%. Below 1,000 the overhead takes over. At 10 rows per batch the backfill takes a day and a half to save a player half a millisecond.

The single statement is the fastest by far. It is also the only row in the table that stalls a trade for 50 minutes.

A sensible choice here: `b = 1,000`, a 50 ms worst stall, which is one server tick at 20 Hz, finishing in under four hours at a quarter of the database's write capacity. Run it the afternoon after the patch, while the new code (section 3) already treats missing durability as full.

### Move it

Open the interactive. The top view is a timeline. Blue blocks are backfill batches, gaps are pauses, and small markers are game writes arriving at random. A game write that lands on a row inside a running batch turns red and waits until the block ends. Drag the batch-size slider and watch the blocks shrink and multiply. The red waits shrink with them. Drag duty cycle and the gaps change, but the blocks stay the same width.

The bottom view plots total time against longest stall, one point per batch size, on log axes. The curve is an L: a long flat floor where shrinking the stall is nearly free, and a steep wall on the left where overhead takes over. Your current choice is the highlighted point. The lesson is to sit near the corner.

### The same idea in other systems

**Stripe (payments, 2017).** Stripe's engineering blog describes moving hundreds of millions of subscription records from being stored inside customer records to a separate table, with no downtime. The four steps are dual writing to both places, changing all reads to the new place, changing all writes to the new place, and removing the old data. That is expand, migrate and contract (section 3) at a very large scale, with a batched backfill in the middle step.

**GitHub's gh-ost (MySQL, public repository since March 2016).** GitHub's online schema-change tool for MySQL creates a "ghost" copy of the table with the new structure, copies rows into it in small chunks, and keeps it up to date by reading MySQL's replication log. At the end it swaps the two tables in a short **cut-over**, which the operator can postpone to a quiet moment. It is our model with a copy instead of an update. Chunk size sets the stall, the copy rate sets the total time, and the one moment that needs a lock is short and scheduled.

**PostgreSQL 11's fast default (October 2018).** Before version 11, adding a column with a default meant a full rewrite, the one-statement row of our table. PostgreSQL 11 changed `ADD COLUMN` with a constant default into a metadata-only change. So for a default that is the same for every row, the database now does what our batches do, only smarter. It skips the backfill and fills old rows in at read time. When the default depends on the row, as durability depends on item type, you still batch.

**EVE Online and Old School RuneScape (current practice).** A daily 15-minute window and a weekly update with hotfixes in between both set a budget in seconds. Anything that fits the budget can run in the window as one statement. Anything that doesn't must be split across the live game. To tell which is which, compare `N / r` with the window.

### Eyes-open design judgment

- **Measure `r` on a copy of production.** The rate depends on row width, indexes (each index on the table is updated too), the replication setup and the other load. A number from an empty laptop is off by an order of magnitude.
- **Pick `b` from the stall budget.** Decide the longest wait a player may see (one tick, 50 ms, is a good default for combat-relevant rows; 1 s may be fine for a cosmetic table), then `b = r × budget`.
- **Pick `d` from the time budget and the load.** If the backfill must finish before next week's patch, `d ≥ N / (r × deadline)`. If replicas fall behind or game latency rises, lower `d`. Make `d` a setting you can change while the job runs.
- **Batch by primary-key range, not by `LIMIT`.** `WHERE id BETWEEN 1000 AND 1999 AND durability IS NULL` finds its rows through the index every time. `WHERE durability IS NULL LIMIT 1000` rescans rows it already skipped and slows down as it goes.
- **Make each batch idempotent.** The `AND durability IS NULL` clause means a crashed or repeated batch does no harm. Record the last finished `id` in a small table so the job resumes where it stopped.
- **Watch the side effects in PostgreSQL.** Each updated row leaves an old row version behind for `VACUUM` to clean, and every change is written to the log and shipped to replicas. Sixty million updates make 60 million dead rows and several gigabytes of log. Pauses give autovacuum and replicas time to keep up, which is one more reason `d` is below 1.

## 3. Expand, migrate, contract

The backfill is one step in a longer sequence. The pattern is called **expand and contract** (or **parallel change**). Its rule is that at every moment the schema supports both the code that is running and the code about to run.

For durability:

1. **Expand.** `ALTER TABLE item_instance ADD COLUMN durability smallint;` Metadata-only, nullable, no default. Old code ignores the column, because it never names it. Ship this migration before any code that uses it.
2. **Deploy code that tolerates both.** Server v42 writes `durability` for every new item and every repair. When it reads an item with `durability IS NULL`, it treats it as the item type's maximum. v41 and v42 can now run side by side.
3. **Migrate (backfill).** Run the batched job from section 2 until no row has `durability IS NULL`.
4. **Enforce.** In PostgreSQL, add `CHECK (durability IS NOT NULL) NOT VALID`, which checks only new writes and takes effect immediately, then `VALIDATE CONSTRAINT`. Validation scans the table, but the documentation says it takes only a `SHARE UPDATE EXCLUSIVE` lock, so trades keep flowing. After that, `SET NOT NULL` can skip its own scan, because a valid `CHECK` constraint already proves no nulls exist.
5. **Contract.** Remove the "NULL means full" branch from the code in a later release.

A **rename** follows the same pattern and shows why you never rename a live column in place. Old code still names the old column and would break the instant it disappears. Instead: add the new column, write to both, backfill, switch reads, stop writing the old one, drop it. That is Stripe's four steps.

### Migration files

Every change is a numbered file kept in version control next to the server code, for example `migrations/0042_add_item_durability.sql`. A table in the database records which files have run:

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);
```

A small runner applies, in order, every file whose number is not in the table, each inside a transaction together with the insert into `schema_migrations`. PostgreSQL can run most DDL (data definition statements such as `ALTER TABLE`) inside a transaction, so a failed migration rolls back cleanly. `CREATE INDEX CONCURRENTLY` is the notable exception and must run outside one. Backfills do not belong in these files. They are long-running jobs with their own progress table, started after the expand migration has shipped.

### What about save data stored as JSON?

Some games keep part of a character as a JSON document in one column, for example the quest journal, because its shape changes every patch. That is schema-on-read, as in the document stores of week 7. The migration then moves into code. Store a `schema_version` inside the document, and write a chain of upgrade functions, `v3 → v4`, `v4 → v5`, applied when the document is loaded. Write the upgraded document back on the next save, so the data upgrades lazily as players log in. The validation habits of CS102 week 13 apply directly. Refuse to load a document whose version is newer than the code knows, and test every upgrade step against a real old document.

## In-class activity (25 minutes)

Pairs. The design team wants two changes for next week's patch on a PostgreSQL 16 database:

- A `bound_to_account` boolean on `item_instance` (60M rows), default `false` for all existing items.
- Changing `character.gold` from `integer` to `bigint` (400,000 rows, but with 3 indexes), because top players are near the 2.1 billion limit.

For each change:

1. Classify it as metadata-only, scan or rewrite, citing the rule from section 1.
2. If it needs a backfill or a rewrite, estimate its time with `r = 20,000` rows per second and decide whether it fits a 15-minute window.
3. Write the expand, migrate and contract steps, naming which server version ships at each step.

Expected output: two short plans, each with a classification, a time estimate and a numbered step list. One pair presents the `gold` plan; the class looks for a moment when old code would break.

## Common misconceptions

- **"Adding a column locks the table for as long as it takes to fill it."** In PostgreSQL 11 and later, adding a column with no default or a constant default touches no rows and holds its lock for milliseconds. The slow part is a backfill you write yourself, which you control.
- **"Smaller batches are always safer."** Below the point where per-batch overhead dominates, the total time explodes while the stall is already negligible. Size batches from a stall budget.
- **"We'll just do it in the maintenance window."** Compare `N / r` with the window first. 60 million rows at 20,000 per second is 50 minutes, over three times EVE's nominal daily downtime.
- **"A document store has no migrations."** It has lazy ones in code, which must handle every old shape forever unless you backfill those too.

## Check yourself

1. A `quest_progress` table has 12 million rows. You measure `r = 30,000` rows per second and `o = 0.004` s. With a 20 ms stall budget and `d = 0.5`, what batch size do you choose, and how long does the backfill take?
2. Under the same numbers, the team wants the backfill done in 30 minutes. What duty cycle does that need, and what might go wrong at that setting?
3. Classify each for PostgreSQL 16: (a) `ADD COLUMN created_at timestamptz DEFAULT now()`; (b) `ADD COLUMN created_at timestamptz DEFAULT clock_timestamp()`; (c) `ALTER COLUMN name TYPE varchar(40)` from `varchar(24)`. For (a) and (b), say what value old rows get.
4. Why does the batched backfill filter on `durability IS NULL` as well as on the `id` range?

<details>
<summary>Answers</summary>

1. `b = r × budget = 30,000 × 0.02 = 600` rows. Batches: 12,000,000 / 600 = 20,000. The longest stall is `b / r = 600 / 30,000 = 0.02` s, exactly the budget. Each batch runs `b / r + o = 0.02 + 0.004 = 0.024` s, since the overhead adds to the batch's running time but not to the stall. Running time `20,000 × 0.024 = 480` s; at `d = 0.5`, total 960 s, 16 minutes.
2. Running time is 480 s and the budget is 1,800 s, so `d = 480 / 1,800 ≈ 0.27` would do. At 30 minutes you already have room. If the target were 8 minutes you would need `d = 1`, meaning the backfill takes the database's whole write capacity with no pauses, and game writes, replicas and vacuum all fall behind.
3. (a) `now()` is stable within a statement, not volatile, so PostgreSQL evaluates it once at `ALTER` time and stores it as the default: metadata-only, and every old row reads the time the migration ran. (b) `clock_timestamp()` is volatile, so the table and its indexes are rewritten, and each old row gets the time it was rewritten. (c) Increasing a `varchar` length limit is binary coercible and does not require a rewrite. Shrinking it would, because every value must be checked and possibly rejected.
4. It makes each batch idempotent. If the job crashes and re-runs a range, rows already filled are skipped. It also avoids overwriting durability that v42 has already written for items created or repaired since the expand step.

</details>

## Lab / assignment hook

[Lab 09, a migration under load](../labs/lab09.md). You run the durability migration on a 1,000,000-row SQLite item table while a second thread plays the game, writing to random items and recording how long each write waits. You compare the one-statement backfill with batched versions, check your measured stalls against `b / r`, and fit `r` and `o` from your runs. Deliverable: the stall and total-time table, the fitted numbers, and a migration plan for the 60-million-row case.

## Sources

- PostgreSQL 18 documentation, `ALTER TABLE` (Notes and subform descriptions, accessed September 2026). Constant defaults stored in metadata; volatile defaults and most type changes rewrite the table and its indexes; `CHECK`/`NOT NULL` need a scan but no rewrite; `VALIDATE CONSTRAINT` takes `SHARE UPDATE EXCLUSIVE`; `SET NOT NULL` skips its scan when a valid `CHECK` constraint proves no nulls; `ACCESS EXCLUSIVE` unless noted. https://www.postgresql.org/docs/current/sql-altertable.html
- PostgreSQL 11 release notes (released 18 October 2018). `ALTER TABLE` can add a column with a non-null constant default without a table rewrite. https://www.postgresql.org/docs/11/release-11.html
- PostgreSQL 18 documentation, "Explicit Locking" (13.3). `ACCESS EXCLUSIVE` conflicts with all modes and is the only mode that blocks a plain `SELECT`. And "Client Connection Defaults", `lock_timeout` (default 0, disabled). https://www.postgresql.org/docs/current/explicit-locking.html
- SQLite documentation, "ALTER TABLE" (SQLite 3.53, 2026). `ADD COLUMN` runs in time independent of table size; restrictions on defaults; no general column type change. https://www.sqlite.org/lang_altertable.html
- EVE University Wiki, "Downtime" (current practice, accessed September 2026). Daily downtime 11:00 to nominally 11:15 UTC; patches and expansions deployed during downtime. https://wiki.eveuniversity.org/Downtime
- Old School RuneScape Wiki, "Updates" (current practice, accessed September 2026). Weekly updates on Wednesdays around 11:30 UTC; a countdown, regularly 45 minutes, before players are logged out; hotfixes deployed without an update timer. https://oldschool.runescape.wiki/w/Updates
- Xu, J. (2017). "Online migrations at scale." Stripe blog, 2 February 2017. Four-step dual-writing pattern for hundreds of millions of subscription records. https://stripe.com/blog/online-migrations
- GitHub, gh-ost README. Triggerless online schema migration for MySQL using a ghost table, the binary log and a postponable cut-over. Repository created 21 March 2016 (GitHub API). https://github.com/github/gh-ost
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 2 (schema-on-read and schema-on-write).

## Interactive spec: examples/w09-backfill-batches.html

**The one insight:** batch size sets the longest stall a player sees, duty cycle sets the total time, and per-batch overhead is the only thing that punishes small batches. Shrinking batches from 100,000 to 1,000 rows cuts the stall 100 times for about 10% more total time.

**Layout.** Two linked views stacked (both desktop and mobile), readout table beside or below.

- **Top, "Timeline" (a window of simulated time).** A horizontal time axis showing a window of `W_view` seconds (auto-chosen as about 8 batch cycles, minimum 1 s). Blue blocks for each batch's running time `b/r + o`, gaps for pauses of length `(b/r + o)(1/d − 1)`. Overlay game-write markers arriving as a Poisson process at rate `λ` per second (seeded, reproducible). A marker is red if it lands inside a block and the targeted row is in the batch's range (probability `b / N_remaining` is negligible for large N, so for the visual assume a write conflicts if it lands inside a block and a seeded coin with probability `p_hit` succeeds; default `p_hit = 1` to show the worst case). A red marker draws a short horizontal "wait" bar to the end of its block. Label the longest wait visible.
- **Bottom, "Total time against longest stall".** Log-log scatter-line of the points `(b/r, T_total(b))` for `b` in powers of 10 from 10 to N, plus the current `b` as a highlighted point. Horizontal reference line at the time budget (default 4 h). Vertical reference line at the stall budget (default 50 ms). Label the flat floor `N/(r·d)`.

**Controls.**
- `N` rows: log slider 100,000 to 500,000,000, default 60,000,000.
- `r` rows per second: log slider 1,000 to 200,000, default 20,000.
- `o` overhead per batch: slider 0 to 50 ms, default 5 ms.
- `d` duty cycle: slider 0.05 to 1.0, default 0.25.
- `b` batch size: log slider 10 to N, default 1,000. A "one statement" button sets `b = N` and `d = 1`.
- `λ` game writes per second (timeline only): slider 1 to 200, default 20.
- Stall budget and time budget inputs (default 50 ms, 4 h).

**Readouts (exact, copyable).** Batches `N/b`; longest stall `b/r`; running time `(N/b)(b/r + o)`; total time `(N/b)(b/r + o)/d` in seconds and hours; the floor `N/(r·d)`; overhead share `(N·o/b) / ((N/b)(b/r + o))`. Recommended `b = r × stall budget` and minimum `d = N / (r × time budget)`, with a warning if that `d` exceeds 1.

**Test values (must match the lecture table), N = 60,000,000, r = 20,000, o = 0.005, d = 0.25.** b = 100,000: 600 batches, stall 5 s, total 12,012 s (3.34 h). b = 10,000: 6,000, 0.5 s, 12,120 s. b = 1,000: 60,000, 0.05 s, 13,200 s (3.67 h). b = 100: 600,000, 0.005 s, 24,000 s. b = 10: 6,000,000, 0.0005 s, 132,000 s (36.7 h). One statement (b = N, d = 1): stall and total both 3,000 s (the overhead 0.005 s is negligible, display 3,000.0 s). Check-yourself: N = 12,000,000, r = 30,000, o = 0.004, d = 0.5, b = 600 gives 20,000 batches, longest stall 0.02 s, running time 0.024 s per batch (stall plus overhead), total 960 s.

**Behavior.** All sliders keyboard operable with visible values. Timeline uses a seeded random generator so the same settings give the same picture. Respect `prefers-reduced-motion`: no scrolling animation of the timeline, static redraw on change.
