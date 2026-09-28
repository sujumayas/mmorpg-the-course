# DB201 · Week 04 — SQL II: Indexes and Query Plans

**Why this matters:** Every login, bag open and bank visit runs a query like `SELECT * FROM items WHERE owner_id = ?`. On a test server with 50 characters it returns instantly no matter how you wrote it. On a live realm with a hundred million item rows, the same query either reads a few hundred pages or a few million, and the only difference is whether an index exists that the database decides to use. This week you learn to predict which one you will get, and to prove it with a query plan.

**You will be able to:**
- Compute the pages a full table scan and a B-tree index lookup read for a given table size, row size and result size.
- Read a query plan in SQLite (`EXPLAIN QUERY PLAN`) and PostgreSQL (`EXPLAIN`, `EXPLAIN ANALYZE`) and say which access path was chosen and why.
- Derive the selectivity at which an index stops paying off, and explain why the planner sometimes ignores your index on purpose.
- Design a composite index for a game query and state what it costs on every insert.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 3, the sections "Data Structures That Power Your Database" through "B-Trees" (read for the B-tree, skim the log-structured part). PostgreSQL 18 documentation, section 14.1 "Using EXPLAIN", up to "EXPLAIN ANALYZE". Rerun your Lab 03 queries and keep the output.

**Prerequisites from earlier courses:** [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (O(n) against O(log n), and counting work instead of timing it). [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (why a hash map finds a key without looking at the others). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (what `log_f N` counts). From this course, the item schema and the blob-or-rows trade-off of [DB201 week 2](w02-relational-modeling-characters-inventories-items.md), and the joins and aggregates of [DB201 week 3](w03-sql-i-select-join-aggregate.md).

**Interactive:** [Index or scan](../examples/w04-index-vs-scan.html). Keep it open during section 2.

---

## 1. Where the rows live

Your Lab 03 queries ran on 1,200 characters and about 30,000 item rows. Every query came back in a few milliseconds, including the badly written ones. That is the trap. Small tables hide every mistake, because a computer can read 30,000 rows faster than you can blink. The mistakes appear when the table grows by a factor of a thousand, which is what a live game does to it.

To see why, you need a picture of how a database stores a table.

### Pages

A database does not read rows one at a time from disk. It reads **pages**, fixed-size blocks that each hold many rows. PostgreSQL stores every table and every index as an array of pages that are usually 8 kB each. SQLite has used 4,096-byte pages by default since version 3.12.0 (2016). A page is the unit of work. Reading one row costs the same as reading every row on its page.

So the first number to know about a table is how many rows fit on a page. Call it `R`:

```
R = page size / row size        (rows per page, rounded down)
P = N / R                       (pages in a table of N rows, rounded up)
```

An item row with an id, a type, an owner, a bag, a slot, a quantity, a durability and some per-row overhead is about 100 bytes. With 8 kB pages and some room for page headers, `R ≈ 80`. In SQLite with 4 kB pages and slightly smaller rows, Lab 04 measures about 49 rows per page.

### The heap and the order of rows

The table itself is called the **heap**. Rows go into it roughly in the order they were inserted. In a game, rows are inserted when items are created: when a monster drops them, when a player crafts them, when a vendor sells them. A character's 120 items were created over weeks of play, one here, three there, interleaved with the items of every other player online at the same time. So a character's items are **scattered** across the heap, a few per page at most, usually one.

Keep that fact in mind. It decides half of this lecture.

### The full table scan

Without any extra structure, the only way to answer `WHERE owner_id = 4417` is to read every page and check every row. This is a **sequential scan** (PostgreSQL calls it `Seq Scan`, SQLite prints `SCAN items`). Its cost is `P` page reads plus `N` row checks, and it does not depend on how many rows match. Finding one row costs the same as finding a million.

## 2. Worked example: opening the bank

### The hook

Open your bank in World of Warcraft today and you see six tabs of 98 slots each. That is the Character Bank since patch 11.2.0. Your account also has a five-tab Warband Bank of 490 slots shared across characters, plus a 16-slot backpack and the bags you carry. A character with a full bank, a full Warband Bank and full bags is looking at more than a thousand item slots, and the window fills with no visible wait.

Blizzard does not publish how it stores items, so we will not guess at its schema. The observable fact is the requirement. A server must find one player's few hundred items among every item owned by every character on the realm, fast enough that the UI never waits. Any game with persistent inventories faces the same demand. How much work that takes is not a matter of taste. It follows from two numbers.

### The model

Let:

- `N` be the number of rows in the items table.
- `R` be rows per heap page (80 in this example).
- `k` be the number of rows the query returns (a character's items).
- `f` be the **fanout** of the index, the number of entries that fit on one index page.

**Full scan:** reads every heap page.

```
pages_scan = ⌈N / R⌉
```

**B-tree index lookup:** a **B-tree** is a sorted tree of pages. The root page holds `f` keys that split the key space into `f` ranges, each pointing to a child page, which splits its range `f` ways again, down to the **leaf** pages. The leaves hold every key in sorted order with a pointer to the row's location in the heap. To find a key you read one page per level. With `f` entries per page, `h` levels cover `f^h` keys, so the height is:

```
h = ⌈log_f N⌉
```

After reaching the leaf, the database follows one pointer per matching row into the heap. If the rows are scattered, each is on a different page:

```
pages_index (scattered)  = h + k
pages_index (clustered)  = h + ⌈k / R⌉
```

An index entry for an 8-byte `owner_id` key is roughly 16 to 20 bytes including the row pointer and overhead, so an 8 kB page holds a few hundred. We use `f = 400`. The exact value barely matters, as you are about to see.

### Numbers you can check

Take `k = 120` items per character, `R = 80`, `f = 400`, and grow the realm:

| Characters | Item rows `N` | Scan pages `⌈N/80⌉` | `h = ⌈log₄₀₀ N⌉` | Index pages, scattered `h + 120` | Index pages, clustered `h + 2` |
|---|---|---|---|---|---|
| 1,000 | 120,000 | 1,500 | 2 | 122 | 4 |
| 10,000 | 1,200,000 | 15,000 | 3 | 123 | 5 |
| 100,000 | 12,000,000 | 150,000 | 3 | 123 | 5 |
| 1,000,000 | 120,000,000 | 1,500,000 | 4 | 124 | 6 |

Check one row by hand. For 12 million rows, `log₄₀₀(12,000,000) = ln(12,000,000) / ln(400) = 16.30 / 5.99 = 2.72`, so `h = 3`. Three index pages, then 120 heap pages, 123 in all. The scan reads 150,000.

Read the table down each column. The scan column grows a thousandfold. The index column grows by two pages. That is the whole reason indexes exist, and it is CS102's O(n) against O(log n) with real page counts attached. A B-tree is so flat that a fourth level covers 400⁴ = 25.6 billion keys. You will never build a game table that needs a fifth.

Now read across the last two columns. When a character's rows sit together on disk, the lookup reads 5 pages instead of 123. The index finds the rows equally fast either way. The difference is the trip into the heap afterwards. Most of the cost of a scattered lookup is the heap, not the tree.

### The same numbers, measured

Lab 04 builds the 10,000-character row of that table in SQLite: 1.2 million item rows, 24,554 pages of 4 kB, 48.9 rows per page. On the lecturer's laptop (Apple silicon, Python 3.13, SQLite 3.53, the whole file cached in memory):

| Query `WHERE owner_id = ?` | Plan printed by `EXPLAIN QUERY PLAN` | Time per query |
|---|---|---|
| No index | `SCAN items` | 32.9 ms |
| After `CREATE INDEX idx_items_owner ON items(owner_id)`, rows scattered | `SEARCH items USING INDEX idx_items_owner (owner_id=?)` | 0.148 ms |
| Same index, rows inserted per character (clustered) | same | 0.065 ms |

The index made the lookup 222 times faster on scattered rows. Clustering made it faster again by a factor of 2.3. The index cost 3,226 extra pages (13% of the table) and took 0.22 seconds to build. Your timings will differ. The ratios should not move much.

One warning about that 32.9 ms. It is fast only because the whole file sat in memory. On a production server where the table is 100 times larger than RAM, a scan reads from disk, and 150,000 pages at even 1 GB/s is over a second per query. Multiply by 2,000 logins a minute after a server restart and the database falls over.

### A visual you can move

Open the interactive. The left panel plots pages read against table size on logarithmic axes. The scan is a straight diagonal line. The index is a nearly flat line that steps up by one page each time `N` crosses a power of `f`. Drag the rows-per-character slider and watch the index line lift while the scan line does not move. Then toggle "clustered" and watch the index line drop to almost nothing.

The right panel is where the surprise lives. We will need it in section 3.

### Cross-game recognition

The same idea, a small structure that tells you where to look so you do not read everything, shows up wherever games store things.

**Minecraft region files (Java Edition, Beta 1.3 onward, still used by the Anvil format).** The world is saved in files that each hold a 32×32 grid of chunks. Each file starts with a 4 KiB table of 1,024 four-byte entries. Entry `i = x + 32z` gives the offset of chunk `(x, z)` in 4 KiB sectors, plus its length. Loading one chunk is one header read and one seek, whether the file holds 10 chunks or all 1,024. That is an index with fanout 1,024 and height 1, possible because chunk coordinates are small integers that can be used directly as positions. A database cannot do this for arbitrary keys, which is why it uses a tree.

**Quake (id Software, 1996; source released 1999).** Game assets are packed into `.pak` files with a directory of up to 2,048 entries. To find a file, the engine loops through the directory comparing names with `strcmp`, one by one. That is a full scan, and it is the right choice. The directory is read into memory once, it has at most 2,048 entries, and a scan of 2,048 short strings takes microseconds. An index is a tool for large `N`. When `N` is small and fixed, the scan is simpler and fast enough.

**A book's index**, for completeness, is a B-tree of height 1 with page numbers as row pointers. It is fast for "where is *armor* mentioned?" and useless for "which pages mention a weapon?", which you answer by reading the book. Hold on to that distinction.

Rewrite each case in the lecture's terms. Minecraft: `h = 1`, `k = 1`, one heap read. Quake: `h = 0`, a scan of `N ≤ 2,048` in memory. The bank: `h = 3`, `k` up to a thousand.

### Eyes-open design judgment

An index is a trade. You pay on every write and in storage so that some reads get cheaper. Decide it deliberately.

- **Index the lookups that run on every player action.** Owner lookups, character-by-name at login, auction listings by item type and price. These run thousands of times a minute and must stay flat as the realm grows.
- **Do not index for the report that runs once a night.** A nightly economy job that reads every item anyway gains nothing from an index and pays for it on every loot drop all day.
- **Think about the heap, not only the tree.** For `k = 120`, most of the cost is 120 random heap reads. If you can store a character's items together (a clustered layout, a covering index as in section 4, or the blob model of [week 2](w02-relational-modeling-characters-inventories-items.md)), the lookup gets another order of magnitude cheaper.
- **Measure with the plan, not the stopwatch on your laptop.** Your laptop caches everything. The plan tells you the access path, which is what changes when the table grows.

### Check yourself on the worked example

1. A realm has 3 million characters with 200 items each and `f = 400`, `R = 80`. How many pages does a scattered owner lookup read? A scan?
2. Your items are clustered by owner. How many pages does the same lookup read?
3. A designer doubles bag space so `k` goes from 120 to 240. By what factor does the scattered lookup cost change? The scan?

<details>
<summary>Answers</summary>

1. `N = 600,000,000`. `log₄₀₀(6 × 10⁸) = 20.21 / 5.99 = 3.37`, so `h = 4`. Scattered lookup reads `4 + 200 = 204` pages. Scan reads `6 × 10⁸ / 80 = 7,500,000` pages.
2. `4 + ⌈200 / 80⌉ = 4 + 3 = 7` pages.
3. The lookup goes from `h + 120` to `h + 240`, roughly doubling (123 to 243 pages at `h = 3`). The scan does not change for a fixed `N`, but `N` doubles too if everyone fills the new space, so the scan doubles as well. Both double, yet the index is still about a thousand times cheaper.

</details>

## 3. When the index loses

Here is a query Lab 04 runs: find every health potion in the game.

```sql
SELECT * FROM items WHERE type_id = 7;   -- potions are 8% of all rows
```

You add `CREATE INDEX idx_items_type ON items(type_id)` and expect a speed-up. On a disk-bound PostgreSQL server you often get none, because the planner ignores the index. That is not a bug. Look at the numbers.

### Selectivity

The **selectivity** `s` of a condition is the fraction of rows it matches, `s = k / N`. An owner lookup in the 1.2-million-row table has `s = 120 / 1,200,000 = 0.01%`. The potion query has `s = 8%`.

A scan reads each page once, in order. Disks and operating systems are good at that, because they read ahead. An index lookup on scattered rows reads one heap page per row, in random order. PostgreSQL's planner models this with two settings whose defaults are `seq_page_cost = 1.0` and `random_page_cost = 4.0`. A random read is assumed to cost four sequential ones.

Set the two costs equal, ignoring the few tree pages:

```
scan cost   = (N / R) × 1
index cost  = (s × N) × 4
equal when  s* = 1 / (4R)
```

With `R = 80`, `s* = 1/320 ≈ 0.31%`. Below a third of a percent, the index wins. Above it, the scan wins. The potion query at 8% is 25 times past the crossover. The index would read about 96,000 random pages to fetch 96,000 potions from a 15,000-page table. That means reading many pages several times over.

The right panel of the interactive plots both costs against selectivity on a log axis. The scan is a flat line. The index is a rising line. They cross at `s*`. Drag `R` or `random_page_cost` and watch the crossing move.

### The cache moves the line

Lab 04 measures the potion query both ways. It takes 78 ms through the index and 92 ms by forced scan. The index won, narrowly. The model said it should lose by a factor of 25. What happened?

The whole database was cached in RAM, so a "random" page read cost about the same as a sequential one. With `random_page_cost = 1`, the crossover moves to `s* = 1/80 = 1.25%`, and at that point the remaining gap is CPU work. The PostgreSQL documentation gives the same advice. If your data is mostly cached, lower `random_page_cost`. The model did not fail. It told you which number to change. That is what a model is for.

### Reading a PostgreSQL plan

Run `EXPLAIN` in PostgreSQL and you get the planner's estimate in abstract cost units. The documentation's own example is a 10,000-row table on 345 pages:

```
EXPLAIN SELECT * FROM tenk1;
 Seq Scan on tenk1  (cost=0.00..445.00 rows=10000 width=244)
```

The 445 is `345 pages × seq_page_cost 1.0 + 10,000 rows × cpu_tuple_cost 0.01`. Add a `WHERE` clause and each row also pays `cpu_operator_cost` (0.0025) to evaluate the condition. So in our 12-million-row table, the planner prices the owner scan at about `150,000 + 120,000 + 30,000 = 300,000` units and the index lookup at about `123 × 4 ≈ 500`. It picks the index.

`EXPLAIN ANALYZE` runs the query and prints real times and real row counts next to the estimates. When estimate and reality disagree by a factor of ten or more, the table's statistics are stale. Run `ANALYZE items` and look again. SQLite's `EXPLAIN QUERY PLAN` gives no costs, only the chosen path: `SCAN` for a full scan, `SEARCH ... USING INDEX` when only a subset of rows is visited.

### Conditions that cannot use an index

A B-tree is sorted by the raw column value. Any condition that does not ask about a range of that sorted order forces a scan:

- `WHERE lower(name) = 'aria'` sorts by `lower(name)`, which is not what the index on `name` holds. Build an index on the expression itself (both PostgreSQL and SQLite support expression indexes) or store names already lowercased.
- `WHERE name LIKE '%sword%'` asks for a substring anywhere. The sorted order cannot help. `LIKE 'Ember%'` is a prefix, so it can use the index in PostgreSQL when the column uses the C collation or an index with the `text_pattern_ops` operator class. Auction-house search boxes that match anywhere in a name need a different structure, for example PostgreSQL's trigram indexes. That is outside this course.
- `WHERE owner_id + 0 = 4417` hides the column inside arithmetic. Write `owner_id = 4417`.

## 4. Composite and covering indexes

### Column order is the whole design

Most game queries filter on more than one column. The bag UI asks for one character's items in one bag, in slot order:

```sql
SELECT * FROM items WHERE owner_id = ? AND bag = ? ORDER BY slot;
```

A **composite index** on `(owner_id, bag, slot)` sorts entries by owner first, then by bag within each owner, then by slot within each bag. Think of a phone book sorted by surname, then first name. It serves:

- `owner_id = ?` (all of one owner's entries are contiguous),
- `owner_id = ? AND bag = ?`,
- `owner_id = ? AND bag = ? ORDER BY slot` (the entries are already in slot order, so no sort step),

but not `bag = ?` alone, just as a phone book cannot list everyone named Maria. This is the **leftmost-prefix rule**. An index helps a query only through a prefix of its columns, starting from the first.

Here is a detail from your Lab 02 schema that is easy to miss. `UNIQUE (owner_id, bag, slot)` does not only enforce that two items cannot share a slot. Both PostgreSQL and SQLite enforce a unique constraint by building exactly this composite index. Your schema already had the owner lookup covered before you wrote a single `CREATE INDEX`. Lab 04 deliberately starts from a table without that constraint so you can see the difference.

### Covering indexes

If every column a query needs is in the index, the database never visits the heap. PostgreSQL calls this an **index-only scan**. SQLite reports `USING COVERING INDEX`. Take the stack-count query that a crafting UI runs:

```sql
SELECT type_id, SUM(quantity) FROM items WHERE owner_id = ? GROUP BY type_id;
```

An index on `(owner_id, type_id, quantity)` answers it from the leaf pages alone. Our scattered 123-page lookup becomes `h` plus the one or two leaf pages holding that owner's 120 entries. It is the clustered case without reorganising the table. PostgreSQL also offers `INCLUDE (quantity)` to carry a column in the leaves without sorting by it. PostgreSQL has one caveat. An index-only scan still checks a per-page "visibility map" to confirm that rows are visible to your transaction, so it works best on tables that `VACUUM` keeps current. Week 5 explains why rows can be invisible to you.

### What every index costs

Every index is a second copy of some columns, kept sorted. Every `INSERT` into the table also inserts into every index. Every `DELETE` removes from each. Every `UPDATE` to an indexed column moves an entry. A rough write model:

```
page writes per inserted row ≈ 1 (heap) + number of indexes × (1 leaf, plus occasional splits)
```

Appending to the heap is cheap because new rows go at the end. Inserting into an index on `owner_id` is not, because the new key lands in the middle of the sorted order, on whichever leaf page holds that owner. Lab 04 measures this in SQLite. Inserting 20,000 items in one transaction ran at 2.3 million rows per second with no secondary index and 165,000 rows per second with two, a factor of 14.

Is that a problem? Put it in game terms. Say 20,000 players are online and each loots one item a minute. That is 333 inserts per second, far below either rate. The index cost is irrelevant here. Now say you add a telemetry table that logs every combat event, 50 per player per minute, a million events a minute, or 16,700 per second. Suddenly each index on that table is a real cost, and indexing it like the items table would be a mistake. [DB201 week 11](w11-pipelines-collect-store-query.md) returns to that table. For now, the rule is simple. Index tables in proportion to how often they are read by key, not by habit.

## In-class activity (25 minutes)

Work in pairs. You are the database engineer for a game launching with an expected 400,000 characters, each owning about 150 items, and an auction house holding 2 million listings. The listings table has columns `listing_id, item_type_id, seller_id, price_each, quantity, expires_at`.

1. Using `R = 80`, `f = 400`, compute the scan and scattered-index page counts for an owner lookup on the items table.
2. The auction UI runs three queries. Query A lists the cheapest listings of one item type, sorted by price. Query B lists everything one seller has listed. Query C, a nightly job, deletes expired listings. Write the index or indexes you would create for each, in column order, or write "none" and justify it.
3. For query A, estimate its selectivity if there are 5,000 item types, and state whether the index will be used.
4. Swap with another pair. Find one query their index set serves badly, and one index they created that costs writes and serves nothing.

Expected output: the two page counts from step 1, three `CREATE INDEX` statements (or justified "none"), the selectivity from step 3, and the critique from step 4.

## Common misconceptions

- **"An index makes every query on that column faster."** Only selective ones. Above the crossover selectivity, the planner uses a scan because it is cheaper, and it is right to.
- **"More indexes is safer."** Each index is paid for on every insert, delete and indexed update. A write-heavy table with five indexes can spend most of its write time maintaining them.
- **"`EXPLAIN` on my laptop shows the index is fast, so production will be fine."** Your laptop caches the whole table. Production may not. Check the plan's access path and row estimates, not the milliseconds.
- **"A composite index on (a, b) also serves queries on b."** Only through its leftmost prefix. A query on `b` alone cannot use it efficiently.

## Check yourself

1. A table has 40 million rows of 200 bytes on 8 kB pages. Estimate `R`, the number of pages, and the B-tree height for `f = 300`.
2. With `random_page_cost = 4` and `R = 40`, what is the crossover selectivity? A query matches 0.5% of rows. Which access path should the planner choose?
3. A query `WHERE bag = 0 AND owner_id = ?` exists alongside an index on `(owner_id, bag, slot)`. Can the index serve it? Why?
4. PostgreSQL prints `Seq Scan on items (cost=0.00..300000.00 rows=120 ...)` for an owner lookup. What is missing, and what one statement would you run first?
5. A telemetry table receives 20,000 inserts per second. A designer wants indexes on `player_id`, `event_type` and `zone_id` "in case someone needs them". What do you tell them, with numbers?

<details>
<summary>Answers</summary>

1. `R = 8,192 / 200 ≈ 40` (fewer after headers). `P = 40,000,000 / 40 = 1,000,000` pages. `log₃₀₀(4 × 10⁷) = 17.50 / 5.70 = 3.07`, so `h = 4`.
2. `s* = 1 / (4 × 40) = 1/160 = 0.625%`. At 0.5% the index is slightly cheaper by the model, so the planner should pick it, although the margin is small and the real choice will depend on caching and correlation.
3. Yes. Both `owner_id` and `bag` form a leftmost prefix of the index, and the order in which you write the conditions in `WHERE` does not matter. The planner matches conditions to index columns, not text order.
4. There is no usable index on `owner_id` (or its statistics are wrong). Run `EXPLAIN` again after `CREATE INDEX ... ON items(owner_id)`, and if an index already exists, run `ANALYZE items` and check the estimate. The expected result is an Index Scan with cost in the hundreds.
5. Each index adds at least one random leaf write per insert, so with three indexes each insert modifies about four pages instead of one, roughly 80,000 page modifications per second instead of 20,000. Lab 04 measured a 14× slowdown from two indexes on bulk inserts. Index only what a real, frequent query needs, and run occasional analysis queries on a copy or a columnar store (DB201 week 11).

</details>

## Lab / assignment hook

[Lab 04, scans, indexes and plans](../labs/lab04.md). You build a 1.2-million-row items table in SQLite, read its plans, measure the owner lookup with and without an index, find where the potion query crosses over, and measure what two indexes cost on inserts. Deliverable: your modified `index_lab.py`, a results table, and a one-page index recommendation for the in-class auction house. This lab counts toward the SQL labs (40%).

## Sources

- Warcraft Wiki, "Bank", "Backpack" and "Bag" (retail World of Warcraft, patch 11.2.0 and later, read September 2026). Character Bank of six 98-slot tabs since 11.2.0 (previously 28 slots plus 7 bag slots); Warband Bank of five 98-slot tabs (490 slots); backpack of 16 slots by default. https://warcraft.wiki.gg/wiki/Bank
- Minecraft Wiki, "Region file format" (Java Edition, Beta 1.3 onward; Anvil keeps the same container). 32×32 chunks per file, 4 KiB sectors, a 1,024-entry location table indexed by `x + 32z`. https://minecraft.wiki/w/Region_file_format
- id Software, Quake source code (1996 game, GPL source release 1999), `WinQuake/common.c`. `MAX_FILES_IN_PACK 2048`; `COM_FindFile` compares names with `strcmp` in a loop over the pack directory. https://github.com/id-Software/Quake
- PostgreSQL Global Development Group, *PostgreSQL 18 Documentation*: section 14.1 "Using EXPLAIN" (the `tenk1` example, 345 pages, cost 445); section 19.7.2 "Planner Cost Constants" (`seq_page_cost` 1.0, `random_page_cost` 4.0, `cpu_tuple_cost` 0.01, `cpu_index_tuple_cost` 0.005, `cpu_operator_cost` 0.0025, and the advice to lower `random_page_cost` for cached data); section 66.6 "Database Page Layout" (pages usually 8 kB). https://www.postgresql.org/docs/current/
- SQLite, "Pragma statements", `page_size` (default 4,096 since 3.12.0, 2016-03-29), and "EXPLAIN QUERY PLAN" (`SCAN` against `SEARCH`, covering indexes). https://www.sqlite.org/pragma.html and https://www.sqlite.org/eqp.html
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 3 (B-trees, branching factor, a four-level tree of 4 KB pages with branching factor 500 storing up to 256 TB).
- Lab 04 measurements: DB201 lecturer's machine, Apple silicon, macOS, Python 3.13.5, SQLite 3.53.3, September 2026.

## Interactive spec: examples/w04-index-vs-scan.html

**The one insight.** As the table grows a thousandfold, the scan's cost grows a thousandfold and the index's cost barely moves. But the index is only cheaper for selective queries, and the crossover selectivity is `1 / (random_page_cost × R)`. Two linked views, one about table size, one about selectivity.

**Layout.** Two panels side by side above 900px, stacked below (size panel first). A readout strip under both.

- Left panel, "Pages read as the realm grows". Log-log line chart. x-axis: item rows `N` from 10³ to 10⁹ (label ticks 1K, 1M, 1B). y-axis: pages read from 1 to 10⁸. Series: "Full scan" `⌈N/R⌉` (straight diagonal); "Index, scattered" `h(N) + k`; "Index, clustered" `h(N) + ⌈k/R⌉`. The index lines are step functions (h jumps by 1 at each power of f); draw them as steps. A vertical marker at the current `N`, with the three values labelled beside it.
- Right panel, "Cost as the query gets less selective". x-axis: selectivity `s` from 0.001% to 100% on a log scale. y-axis: modelled cost in sequential-page units, log scale. Series: "Full scan" `N/R` (flat horizontal line); "Index" `h + s × N × c_r` where `c_r` = random_page_cost (use the scattered model; if "clustered" is on, use `h + ⌈s × N / R⌉ × c_r`). Shade the region where the index wins. A vertical dashed line at `s* = 1 / (c_r × R)` (scattered) labelled "crossover s* = X.XX%". Two preset markers on the x-axis: "owner lookup" at `s = k / N` and "all potions" at `s = 8%`.
- Readout strip: `N`, `R`, `f`, `h`, `k`, scan pages, index pages (scattered and clustered), ratio scan/index (scattered, 0 decimals), `s*` (2 decimals, %), and a sentence "Planner picks: INDEX" or "SCAN" for the potion query and for the owner lookup, by comparing the two costs.

**Controls.** All keyboard reachable; sliders respond to arrow keys; numbers are selectable text.
- Table size `N`: log slider 10³ to 10⁹, default 1.2 × 10⁶, snapping to 1, 1.2, 2, 5 × powers of 10, plus a number box for an exact `N` (1,000 to 10⁹) so values such as 600,000,000 can be entered.
- Rows per heap page `R`: 10 to 200, step 1, default 80.
- Index fanout `f`: 50 to 1,000, step 10, default 400.
- Rows per character `k`: 10 to 1,000, step 10, default 120.
- `random_page_cost` `c_r`: 1.0 to 10.0, step 0.1, default 4.0. Label "1.0 = everything cached (SSD/RAM)".
- Toggle "Items clustered by owner" (default off). Affects the right panel's index curve and highlights the clustered line on the left.
- Preset buttons: "Lab 04 laptop" (N = 1.2M, R = 49, f = 400, k = 120, c_r = 1.0), "Lecture model" (defaults), "Huge realm" (N = 1.2 × 10⁸).

**Formulas.**
- `h = max(1, ⌈ln N / ln f⌉)`
- `scan = ⌈N / R⌉`; `idx_scattered = h + k`; `idx_clustered = h + ⌈k / R⌉` (left panel, page counts; no cost weighting)
- Right panel: `cost_scan = N / R`; `cost_idx(s) = h + s × N × c_r` (scattered) or `h + ⌈s × N / R⌉ × c_r` (clustered)
- `s* = 1 / (c_r × R)` (scattered); show the numerically found crossing for the clustered case, which is where `⌈s N / R⌉ × c_r = N / R − h`, and note "clustered index wins up to s ≈ 1/c_r".

**Test values (must match exactly).**

| N | R | f | k | h | Scan pages | Index scattered | Index clustered |
|---|---|---|---|---|---|---|---|
| 120,000 | 80 | 400 | 120 | 2 | 1,500 | 122 | 4 |
| 1,200,000 | 80 | 400 | 120 | 3 | 15,000 | 123 | 5 |
| 12,000,000 | 80 | 400 | 120 | 3 | 150,000 | 123 | 5 |
| 120,000,000 | 80 | 400 | 120 | 4 | 1,500,000 | 124 | 6 |
| 600,000,000 | 80 | 400 | 200 | 4 | 7,500,000 | 204 | 7 |

Crossover: `R = 80, c_r = 4` gives `s* = 0.3125%` (display 0.31%). `R = 80, c_r = 1` gives 1.25%. `R = 40, c_r = 4` gives 0.625% (display 0.63%). With defaults, the potion query (8%) shows "Planner picks: SCAN" and the owner lookup (`s = 0.01%`) shows "INDEX".

**Visual rules.** Use `templates/interactive-tokens.css` inline. No game art or logos; label series in text. Respect `prefers-reduced-motion` (no animated transitions when set) and `prefers-color-scheme`. Must not overflow horizontally at 390px.
