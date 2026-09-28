# DB201 · Exam bank: quiz, practice and viva questions

DB201 has no written exam. The grade comes from the SQL labs (40%, see [sql-labs-brief.md](sql-labs-brief.md)) and the final persistence and telemetry service (60%, see [final-service-brief.md](final-service-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers or runs a query, and one asks you to explain or critique.
- **Viva.** The lab spot checks and the week 15 service viva ask questions in this style, rewritten with your own schema, your own measurements and your own code.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model (save interval, page counts, split saves, write-behind, backfill batches, storage, RPO and RTO) to values you have not seen.
- **query**: write a SQL query, or predict what one returns.
- **code**: trace what a piece of Python prints or does.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a schema, policy or setting for a stated situation and justify it.
- **critique**: find what is wrong with a query, a piece of code or a proposal, and fix it.

All numbers are invented unless a question names a game or a product. Every real-world fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 and SQLite 3.53 (`.venv/bin/python`), and every number was recomputed in Python from the lectures' own models. Write your answer before you open the solution.

---

## Week 1: Why persistence is hard in games

Lecture: [w01](../lectures/w01-why-persistence-is-hard-in-games.md).

1. *Week 1 · compute.* A shard has 12,000 players online, each with an 18 kB saved state (`S = 18,000` bytes), saved every 180 seconds. Give the saves per second `W`, the write volume `B`, the average loss per player, and the player-hours lost in one crash.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `W = 66.7` saves/s, `B = 1.2 MB/s`, average loss 90 s, 300 player-hours per crash.

`W = N / T = 12,000 / 180 = 66.7`. `B = N × S / T = 12,000 × 18,000 / 180 = 1,200,000` bytes per second. A crash lands uniformly inside the interval, so the average loss is `T / 2 = 90` s. Summed over everyone online, `N × T / 2 = 12,000 × 90 = 1,080,000` player-seconds, which is 300 player-hours.

Check the constant from the lecture. `W × T / 2 = 66.7 × 90 = 6,000 = N / 2`.
</details>

2. *Week 1 · compute.* A 3,000-player shard saves a 30 kB state every 120 s and also writes a 1.5 kB event save for each valuable event, at `e = 18` events per player-hour.
   (a) Give the hybrid writes per second and bytes per second.
   (b) A producer asks for purely periodic saves at the same write rate instead. What `T` is that, and what is its average loss for valuable state?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40 writes/s and 772.5 kB/s. (b) `T = 75` s, with 37.5 s average loss on everything, valuable state included.

(a) Periodic writes `3,000 / 120 = 25` per second. Event writes `3,000 × 18 / 3,600 = 15` per second. Total 40. Bytes: `3,000 × 30,000 / 120 = 750,000` plus `15 × 1,500 = 22,500`, so 772,500 bytes per second.

(b) Periodic saves at 40 per second need `T = N / W = 3,000 / 40 = 75` s. That policy halves cheap-state loss (37.5 s against 60 s) but loses 37.5 s of valuable state on average, where the hybrid loses none. The hybrid spends the same write budget where players feel it.
</details>

3. *Week 1 · code.* A teammate writes a helper for the save-policy spreadsheet. What does the last line print, what should it print, and what is the bug?

```python
def hybrid_writes(n, T, e):
    return n / T + n * e / 60

print(round(hybrid_writes(4000, 300, 12), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `813.3`. It should print `26.7`. The event rate `e` is per player-hour, so the event term must divide by 3,600, not 60.

`4,000 / 300 = 13.3`. The buggy event term is `4,000 × 12 / 60 = 800`, so the total is 813.3. The correct term is `4,000 × 12 / 3,600 = 13.3`, total 26.7, which matches the lecture's hybrid row. The bug overstates event writes 60 times and would make the hybrid look far worse than a 10-second periodic save (400 writes/s). Put the unit in the parameter name (`events_per_hour`) and test the function against a row you checked by hand.
</details>

4. *Week 1 · critique.* This save routine is meant to survive crashes. Which crash does it survive, which does it not, and what two lines are missing?

```python
import json, os

def save(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(json.dumps(state))
    os.replace(tmp, path)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It survives a crash of the game process at any point, because the real file is replaced in one atomic rename and the old version stays intact until then. It does not reliably survive a power cut or an operating-system crash. The missing lines are `f.flush()` and `os.fsync(f.fileno())` before the file closes.

Without `fsync`, the new bytes may still sit in the operating system's memory when `os.replace` runs. After a power cut the rename can be on disk while the file contents are not, which leaves an empty or partial save under the real name. Lab 01 step 7 makes the same point. Its simulated crash is a process crash, so the test passes without `fsync` even though the code is not durable.
</details>

---

## Week 2: Relational modeling

Lecture: [w02](../lectures/w02-relational-modeling-characters-inventories-items.md).

5. *Week 2 · compute.* Use the lecture's PostgreSQL row model (data bytes plus a 24-byte padded header, rounded up to a multiple of 8, plus a 4-byte line pointer, and 8,168 usable bytes per 8,192-byte page). The `items` row gains `crafted_by bigint` and `durability int` on top of the lecture's 28 data bytes. What is `r`, how many rows fit on a page, and how large is a table of 50 million rows?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `r = 68` bytes, 120 rows per page, 416,667 pages, about 3.41 GB.

Data bytes `28 + 8 + 4 = 40`. With the header, `40 + 24 = 64`, already a multiple of 8. Add the 4-byte pointer, `r = 68`. Rows per page `⌊8,168 / 68⌋ = 120`. Pages `⌈50,000,000 / 120⌉ = 416,667`, and `416,667 × 8,192 = 3.41 GB`.

The lecture's 60-byte row gave 136 rows per page. Two extra columns cost 12% more pages, and every scan and cache pays that.
</details>

6. *Week 2 · compute.* An invented MMO has `C = 500,000` characters, `I = 80` stacks each, `K = 4,000` item types, and a JSON item of `j = 90` bytes. For the blob design, give the table size and the bytes rewritten by one item trade. For the row design with `r = 60`, give the bytes changed by the same trade, the ratio, and the rows an indexed "how many of type X exist?" visits.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Blob table 3.6 GB. A trade rewrites 14,400 bytes in the blob design and about 60 in the row design, a ratio of 240. The count visits about 10,000 rows.

Blob storage `C × I × j = 500,000 × 80 × 90 = 3.6 × 10⁹` bytes. A trade rewrites both inventories, `2 × I × j = 2 × 80 × 90 = 14,400` bytes. The row design updates one row, about 60 bytes, and `14,400 / 60 = 240`. The world count through an index on `type_id` visits `C × I / K = 40,000,000 / 4,000 = 10,000` rows, against parsing all 3.6 GB of blobs.
</details>

7. *Week 2 · code.* The script below runs seven statements against a fresh SQLite database. Without running it, say for each line whether it prints `ok` or `rejected`, and name the constraint. Then name the two results a PostgreSQL server with the same schema would change.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE characters (character_id INTEGER PRIMARY KEY,
  gold INTEGER NOT NULL CHECK (gold >= 0));
CREATE TABLE items (item_id INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL REFERENCES characters(character_id),
  bag INTEGER, slot INTEGER NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity >= 1),
  UNIQUE (owner_id, bag, slot));
INSERT INTO characters VALUES (1, 100);
""")
tests = [
    "INSERT INTO items VALUES (10, 1, 0, 3, 5)",
    "INSERT INTO items VALUES (11, 1, 0, 3, 2)",
    "INSERT INTO items VALUES (12, 1, NULL, 4, 1)",
    "INSERT INTO items VALUES (13, 1, NULL, 4, 1)",
    "INSERT INTO items VALUES (14, 99, 0, 5, 1)",
    "INSERT INTO items VALUES (15, 1, 0, 6, 0)",
    "UPDATE characters SET gold = gold - 150 WHERE character_id = 1",
]
for n, sql in enumerate(tests, 1):
    try:
        con.execute(sql)
        print(n, "ok")
    except sqlite3.IntegrityError as e:
        print(n, "rejected:", e)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
1 ok
2 rejected: UNIQUE constraint failed: items.owner_id, items.bag, items.slot
3 ok
4 ok
5 ok
6 rejected: CHECK constraint failed: quantity >= 1
7 rejected: CHECK constraint failed: gold >= 0
```

Line 2 puts a second stack in bag 0, slot 3. Lines 3 and 4 both use `bag = NULL` in slot 4, and `NULL` is not equal to `NULL`, so the unique constraint sees two different keys and accepts both. Line 5 references character 99, who does not exist, and SQLite accepts it because foreign keys are off until the connection runs `PRAGMA foreign_keys = ON`. Lines 6 and 7 break the two `CHECK` rules.

PostgreSQL always enforces foreign keys, so line 5 would be rejected. Line 4 would still be accepted, because PostgreSQL also treats NULLs as distinct in a unique constraint unless you write `UNIQUE NULLS NOT DISTINCT` (PostgreSQL 15 and later). The fix that works in both is `bag INTEGER NOT NULL` with 0 for the backpack.
</details>

8. *Week 2 · design.* A Guild Wars 2 inventory slot from the official API looks like `{"id": 24615, "count": 3, "upgrades": [24615, 49432], "binding": "Character"}`. Rewrite it into rows of the lecture's schema, name the child table the list needs and its primary key, and say whether this item can stack with a copy that has no upgrades.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One `items` row with `type_id = 24615` and `quantity = 3`, plus a binding column (or flag), and two rows in a child table such as `item_upgrades (item_id, position, upgrade_type_id)` with primary key `(item_id, position)`. It cannot stack with an unupgraded copy.

`id` is the type, `count` is the quantity, and `binding` is instance state. `upgrades` is a list, so it becomes one row per element instead of a comma-separated string, which lets you ask "which items carry upgrade 49432?" with an index. The key uses a position because the same upgrade can appear twice in the list, so `(item_id, upgrade_type_id)` alone would reject a legal item. Two copies share a row only if every instance column except `quantity` is identical, and this copy carries upgrades and a binding the other lacks.
</details>

---

## Week 3: SQL I, select, join, aggregate

Lecture: [w03](../lectures/w03-sql-i-select-join-aggregate.md). Questions 9 to 13 use the lecture's four-character world (Aria, Bram, Cyra and Dax, section 1).

9. *Week 3 · query.* Predict the output of this query, row by row, then say which number a designer would misread and why.

```sql
SELECT c.class, COUNT(*) AS n, SUM(i.quantity) AS qty
FROM characters c LEFT JOIN items i ON i.owner_id = c.character_id
GROUP BY c.class ORDER BY c.class;
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `mage 3 56`, `rogue 1 NULL`, `warrior 3 43`.

The left join produces Bram's 2 item rows, Dax's 1 and Aria's 3, and one all-NULL row for Cyra. Mage `n = 2 + 1 = 3`, quantity `5 + 50 + 1 = 56`. Warrior `n = 3`, quantity `12 + 1 + 30 = 43`. Rogue has one row with NULL item columns, so `COUNT(*) = 1` and `SUM` of only NULLs is NULL.

The misleading number is rogue `n = 1`. It reads as "one item stack" but counts Cyra's padding row. Use `COUNT(i.item_id)` for stacks, and `COALESCE(SUM(i.quantity), 0)` if the dashboard should show 0.
</details>

10. *Week 3 · compute.* A new world has three characters. X has 800 gold, 4 item stacks and 5 quests. Y has 200 gold, no items and 3 quests. Z has 500 gold, 2 items and 1 quest. The naive query joins `characters` to `items` and to `quest_completions` and sums gold.
   (a) With inner joins, how many joined rows are there and what total gold is reported?
   (b) The same with both joins changed to `LEFT JOIN`.
   (c) What is the true total?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 22 rows, 17,000 gold. (b) 25 rows, 17,600 gold. (c) 1,500 gold.

(a) Inner join rows per character are `m₁ × m₂`. X gives `4 × 5 = 20`, Y gives `0 × 3 = 0`, Z gives `2 × 1 = 2`, 22 in all. Gold is counted once per row, `800 × 20 + 500 × 2 = 17,000`.

(b) In a left join a zero match count behaves as 1. X 20, Y `1 × 3 = 3`, Z 2, 25 rows. Gold `16,000 + 200 × 3 + 1,000 = 17,600`. Left joins bring Y back but still inflate everyone.

(c) `800 + 200 + 500 = 1,500`. The naive inner join is 11.3 times too high. Aggregate each child table per character first, then join.
</details>

11. *Week 3 · query.* Write a query for "characters who completed quest 10 but hold no rare item", sorted by name, and give its result on the four-character world.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Bram and Cyra.

```sql
SELECT c.name FROM characters c
WHERE EXISTS (SELECT 1 FROM quest_completions q
              WHERE q.character_id = c.character_id AND q.quest_id = 10)
  AND NOT EXISTS (SELECT 1 FROM items i JOIN item_types t ON t.type_id = i.type_id
                  WHERE i.owner_id = c.character_id AND t.rarity = 'rare')
ORDER BY c.name;
```

Aria, Bram and Cyra completed quest 10. Aria holds an Emberfang Sword, which is rare, so she drops out. Dax holds a sword but never did quest 10. `EXISTS` and `NOT EXISTS` test for matches without joining the rows in, so nothing can fan out.
</details>

12. *Week 3 · query.* A designer asks: "Among characters of level 5 or more, which classes have an average gold above 200?" Write the query, give the result, and give the result of the same query with the `WHERE` clause deleted.

<details>
<summary>Answer and worked solution</summary>

**Answer:** With the filter: mage 300, warrior 500. Without it: warrior 500 only.

```sql
SELECT class, AVG(gold) AS avg_gold, COUNT(*) AS n
FROM characters WHERE level >= 5
GROUP BY class HAVING AVG(gold) > 200 ORDER BY class;
```

`WHERE` removes Dax (level 4) before grouping. The groups are then warrior {500}, mage {300} and rogue {200}. `HAVING` keeps groups whose average exceeds 200, so rogue (exactly 200) goes. Without the `WHERE`, mage averages `(300 + 0) / 2 = 150` and fails the `HAVING`. The row filter and the group filter answer different questions, which is why they are different clauses.
</details>

13. *Week 3 · critique.* This query is meant to list quests completed per character. What does it return on the four-character world, which row is wrong, and what one change fixes it?

```sql
SELECT c.name, COUNT(*) AS quests
FROM characters c LEFT JOIN quest_completions q ON q.character_id = c.character_id
GROUP BY c.character_id, c.name ORDER BY c.character_id;
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** Aria 2, Bram 4, Cyra 1, Dax 1. Dax is wrong. He completed no quests. Change `COUNT(*)` to `COUNT(q.quest_id)` and Dax becomes 0.

The left join keeps Dax with one row of NULL quest columns. `COUNT(*)` counts rows, including that one. `COUNT(q.quest_id)` counts non-NULL values and skips it. The two counts differ exactly on the right side of a left join.
</details>

---

## Week 4: SQL II, indexes and query plans

Lecture: [w04](../lectures/w04-sql-ii-indexes-and-query-plans.md).

14. *Week 4 · compute.* An items table holds 48 million rows with `R = 80` rows per heap page and index fanout `f = 400`. A character owns `k = 150` items. Give the pages read by a full scan, the B-tree height, and the pages read by an owner lookup when items are scattered and when they are clustered.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Scan 600,000 pages. `h = 3`. Scattered lookup 153 pages, clustered 5 pages.

Scan `⌈48,000,000 / 80⌉ = 600,000`. Height `⌈log₄₀₀ 48,000,000⌉`. `ln(4.8 × 10⁷) / ln 400 = 17.69 / 5.99 = 2.95`, so `h = 3`. Scattered `h + k = 3 + 150 = 153`. Clustered `h + ⌈k / R⌉ = 3 + ⌈150 / 80⌉ = 3 + 2 = 5`. The scattered lookup spends 150 of its 153 pages in the heap, not the tree.
</details>

15. *Week 4 · compute.* A table has `R = 60` rows per page. With `random_page_cost = 4`, what is the crossover selectivity `s*`? Which access path should the planner choose for a query matching 0.2% of rows, and for one matching 1%? Repeat both with `random_page_cost = 1.5`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** At `c_r = 4`, `s* = 0.42%`, so 0.2% uses the index and 1% scans. At `c_r = 1.5`, `s* = 1.11%`, so both use the index.

`s* = 1 / (c_r × R)`. `1 / (4 × 60) = 1/240 = 0.417%`. `1 / (1.5 × 60) = 1/90 = 1.11%`. Lowering `random_page_cost`, which the PostgreSQL documentation advises when data is mostly cached, moves the crossover to the right, so the planner keeps choosing the index for less selective queries.
</details>

16. *Week 4 · compute.* Using the PostgreSQL cost constants from the lecture (`seq_page_cost 1.0`, `cpu_tuple_cost 0.01`, `cpu_operator_cost 0.0025`), what total cost does `EXPLAIN` print for a sequential scan of a 2,000,000-row table on 25,000 pages, without a `WHERE` clause and with `WHERE owner_id = 42`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 45,000 without the filter, 50,000 with it.

Without a filter, `25,000 × 1.0 + 2,000,000 × 0.01 = 25,000 + 20,000 = 45,000`. The `WHERE` clause adds one operator evaluation per row, `2,000,000 × 0.0025 = 5,000`, for 50,000. This is the same arithmetic as the documentation's `tenk1` example, `345 + 10,000 × 0.01 = 445`. An index lookup returning 150 scattered rows costs a few hundred units, so the planner picks it.
</details>

17. *Week 4 · code.* The table below has one composite index. Predict the `EXPLAIN QUERY PLAN` detail line SQLite prints for each of the five queries, and explain the last one.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("""CREATE TABLE items (item_id INTEGER PRIMARY KEY, owner_id INTEGER,
  type_id INTEGER, bag INTEGER, slot INTEGER, quantity INTEGER)""")
con.execute("CREATE INDEX ix_osb ON items(owner_id, bag, slot)")
queries = [
    "SELECT * FROM items WHERE bag = 0",
    "SELECT * FROM items WHERE owner_id = 7 AND slot = 3",
    "SELECT * FROM items WHERE owner_id = 7 ORDER BY bag, slot",
    "SELECT bag, slot FROM items WHERE owner_id = 7",
    "SELECT * FROM items WHERE owner_id + 0 = 7",
]
for q in queries:
    detail = [row[3] for row in con.execute("EXPLAIN QUERY PLAN " + q)]
    print(" | ".join(detail))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
SCAN items
SEARCH items USING INDEX ix_osb (owner_id=?)
SEARCH items USING INDEX ix_osb (owner_id=?)
SEARCH items USING COVERING INDEX ix_osb (owner_id=?)
SCAN items
```

`bag` alone is not a leftmost prefix, so the first query scans. The second uses only the `owner_id` prefix, because `slot` is not next to `owner_id` in the index; `slot = 3` is checked on the rows found. The third needs no sort step, because the entries for one owner are already in `(bag, slot)` order. The fourth reads only indexed columns, so it never visits the table. The last hides `owner_id` inside arithmetic. The index is sorted by the raw value, not by `owner_id + 0`, so SQLite must scan. Write `owner_id = 7`.
</details>

---

## Week 5: Transactions and ACID

Lecture: [w05](../lectures/w05-transactions-and-acid.md).

18. *Week 5 · compute.* Two characters are saved on independent timers every `T = 200` s. A crash happens 50 s after they trade. Give `p`, `P(dupe)`, `P(loss)`, `P(split)` and `P(correct)` (both saves have the trade).

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = 0.25`, `P(dupe) = P(loss) = 0.1875`, `P(split) = 0.375`, `P(correct) = 0.0625`.

`p = d / T = 50 / 200 = 0.25`. `P(dupe) = p(1 − p) = 0.25 × 0.75 = 0.1875`, and `P(loss)` is the same. `P(split) = 2p(1 − p) = 0.375`. Both saves include the trade with probability `p² = 0.0625`, and neither does with probability `(1 − p)² = 0.5625`. The four outcomes sum to 1. Note that "neither saved it" is the most likely outcome here and is harmless, because the trade simply never happened.
</details>

19. *Week 5 · compute.* A shard has 12,000 players online. Each makes one cross-player transfer every 15 minutes. Characters are saved on independent timers every 180 s and nothing else. How many transfers are exposed to a crash, and how many dupes should you expect per crash?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 2,400 transfers exposed, 800 split, 400 of them dupes.

Transfers per second `12,000 / 900 = 13.3`. In the 180 s before a crash, `13.3 × 180 = 2,400` transfers happened. Averaged over a crash anywhere in the interval, one third split, 800, and half of those are dupes, 400 per crash. Shortening `T` shrinks the 2,400 but not the one third. Only a joint commit makes the split impossible.
</details>

20. *Week 5 · compute.* A server's flush takes `t_f = 5 ms`. How many commits per second can it do with one transaction per flush? What average batch size does it need for 3,000 commits per second, and roughly what commit latency does each player see?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 200 commits per second unbatched. It needs 15 commits per flush for 3,000 per second. Latency stays about 5 ms, plus any wait to join a batch.

`b / t_f` with `b = 1` gives `1 / 0.005 = 200`. For 3,000 per second, `b = 3,000 × 0.005 = 15`. The flush costs about the same whether it carries 1 or 100 commits, so throughput grows with `b` while each commit still waits roughly one flush. Group commit only reaches `b = 15` if enough sessions commit at the same moment.
</details>

21. *Week 5 · code.* Both calls run the same three statements against a fresh world where the seller (character 1) has 0 gold and the buyer (character 2) has 300. The connection is in autocommit mode. What does the last line print, and which ACID letter explains the difference?

```python
import sqlite3

def world():
    con = sqlite3.connect(":memory:", isolation_level=None)   # autocommit
    con.executescript("""
    CREATE TABLE characters (character_id INTEGER PRIMARY KEY,
                             gold INTEGER NOT NULL CHECK (gold >= 0));
    CREATE TABLE items (item_id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL);
    INSERT INTO characters VALUES (1, 0), (2, 300);
    INSERT INTO items VALUES (5001, 1);""")
    return con

def sell(con, use_txn):
    try:
        if use_txn:
            con.execute("BEGIN")
        con.execute("UPDATE characters SET gold = gold + 500 WHERE character_id = 1")
        con.execute("UPDATE characters SET gold = gold - 500 WHERE character_id = 2")
        con.execute("UPDATE items SET owner_id = 2 WHERE item_id = 5001")
        if use_txn:
            con.execute("COMMIT")
    except sqlite3.IntegrityError:
        if use_txn:
            con.execute("ROLLBACK")
    gold = con.execute("SELECT SUM(gold) FROM characters").fetchone()[0]
    owner = con.execute("SELECT owner_id FROM items").fetchone()[0]
    return gold, owner

print(sell(world(), False), sell(world(), True))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `(800, 1) (300, 1)`. Atomicity.

Without a transaction, each statement commits alone. The seller is paid 500, then the buyer's debit fails the `CHECK (gold >= 0)` because 300 − 500 is negative, and the item never moves. The seller's 500 stays, so world gold rose from 300 to 800. That is gold created from nothing by a trade that failed. With `BEGIN`, the failed `CHECK` leads to `ROLLBACK`, which undoes the seller's credit, and the world is back to 300 gold with the sword still with the seller. The constraint (consistency) caught the overdraft, but only atomicity made the earlier statement disappear too.
</details>

22. *Week 5 · explain.* A game commits trades with PostgreSQL's `synchronous_commit = off`. The server loses power 400 ms after a player sees "trade complete". List the possible outcomes and say which letters of ACID still hold.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Either the whole trade survived or none of it did. Atomicity and consistency hold. Durability was relaxed, so a confirmed trade can vanish. A half trade is impossible.

The loss window is up to three times `wal_writer_delay`, 600 ms by default, so a commit 400 ms old may not have reached disk. All four writes share one commit record, so recovery replays them all or none. The player may see a confirmed trade undone, which is a support ticket. The economy is not damaged, because no item or gold was created. That is why the lecture keeps trades synchronous and uses asynchronous commit for position and XP.
</details>

---

## Week 6: Race conditions and the duplication bug

Lecture: [w06](../lectures/w06-race-conditions-and-the-duplication-bug.md).

23. *Week 6 · compute.* Two concurrent trade handlers each have five steps. Each reads the giver's inventory at its first step and writes back its stale copy at its last step. How many interleavings are there, and in how many does the item duplicate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 252 interleavings, 250 dupes.

The number of interleavings is `C(10, 5) = 252`, the ways to choose which 5 of 10 time slots belong to trade 1. The dupe condition is "each trade's read comes before the other trade's take". With the read first and the take last, it fails only when one trade finishes before the other starts, which happens in 2 orders. So `252 − 2 = 250`. Longer handlers widen the race, both in orders and in milliseconds.
</details>

24. *Week 6 · compute.* An attacker fires two trade requests at once. The race window is `w = 3 ms` and the arrival jitter is `J = 60 ms`. Give the chance of a dupe per attempt, the expected attempts to the first dupe, and the chance of at least one dupe in 50 attempts. Then give the per-attempt chance if a slow validation call stretches the window to 12 ms and jitter falls to 50 ms.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `P = 0.0975` per attempt, about 10.3 attempts expected, 0.994 within 50 attempts. With `w = 12`, `J = 50`, `P = 0.42`, about 2.4 attempts.

`w / J = 0.05`. `P = 1 − (1 − 0.05)² = 1 − 0.9025 = 0.0975`. Expected attempts `1 / 0.0975 = 10.3`. At least one in 50 is `1 − 0.9025⁵⁰ = 1 − 0.0059 = 0.994`. With `w / J = 0.24`, `P = 1 − 0.76² = 1 − 0.5776 = 0.4224`, and `1 / P = 2.37`. An attacker who can trigger the slow path gets a reliable exploit.
</details>

25. *Week 6 · code.* The function below simulates the naive handler with its steps reordered to read, take, give (`R T G`). With `checked=True` it becomes the lecture's version check (fix 3). What does the last line print? A teammate claims `R T G` dupes in the same 18 of 20 interleavings as `R G T`, because the dupe condition does not mention `G`. Is that right?

```python
from itertools import combinations

def run(order, checked):
    giver, recv = {5001}, {1: set(), 2: set()}
    version = 0
    seen = {}             # what each trade read at R: (copy, version)
    step = {1: 0, 2: 0}   # next step per trade: 0 = R, 1 = T, 2 = G, 3 = finished
    for ch in order:
        t = int(ch)
        if step[t] == 3:
            continue
        if step[t] == 0:                     # R: read the giver
            if 5001 not in giver:
                step[t] = 3                  # rejected
                continue
            seen[t] = (set(giver), version)
        elif step[t] == 1:                   # T: write back the copy minus the sword
            copy, v = seen[t]
            if checked and v != version:
                step[t] = 3                  # conflict: give nothing
                continue
            giver = copy - {5001}
            version += 1
        else:                                # G: give to this trade's receiver
            recv[t].add(5001)
        step[t] += 1
    return (5001 in giver) + len(recv[1]) + len(recv[2])

orders = ["".join("1" if i in c else "2" for i in range(6))
          for c in combinations(range(6), 3)]
print(len(orders),
      sum(run(o, False) == 2 for o in orders),
      sum(run(o, True) == 2 for o in orders))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `20 12 0`. The teammate is wrong. Taking before giving still dupes, but in 12 of 20 interleavings, as the week 6 lecture shows.

The dupe condition is "R2 before T1 and R1 before T2". It does not mention `G`, but it does depend on where `T` sits. With `R G T`, each take is the trade's last step, so the condition fails only for the two serial orders, 18 dupes. With `R T G`, each take is the second step. Now the condition also fails when a trade reads and takes before the other trade reads, for example `112122` and `112212`. Counting gives 12 dupes, and the Lab 06 scheduler gives the same 12 when run with a take-before-give handler.

The lesson holds. Reordering shortens the window but never closes it, and 12 of 20 is still a reliable exploit. The version check closes it completely, 0 of 20, because a stale take fails and gives nothing.
</details>

26. *Week 6 · code.* A guild bank holds 1,000 gold. Two officers withdraw 600 each, and the server runs the same conditional statement for both. What does the script print?

```python
import sqlite3
con = sqlite3.connect(":memory:", isolation_level=None)
con.execute("CREATE TABLE guild_bank (guild_id INTEGER PRIMARY KEY, gold INTEGER NOT NULL)")
con.execute("INSERT INTO guild_bank VALUES (7, 1000)")
withdraw = "UPDATE guild_bank SET gold = gold - ? WHERE guild_id = 7 AND gold >= ?"
a = con.execute(withdraw, (600, 600)).rowcount
b = con.execute(withdraw, (600, 600)).rowcount
print(a, b, con.execute("SELECT gold FROM guild_bank").fetchone()[0])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `1 0 400`.

The first update finds 1,000 ≥ 600 and changes one row. The second finds 400, fails the `WHERE`, and changes none. The server hands gold to an officer only when `rowcount == 1`. The read-modify-write version (`SELECT gold`, check in Python, `UPDATE ... SET gold = <value read>`) could let both succeed and create 600 gold. In PostgreSQL the same statement is safe at Read Committed, because the second writer waits for the first to commit and then re-checks its `WHERE` against the new row.
</details>

27. *Week 6 · design.* A five-player loot split locks the characters involved. Trade A involves characters 12, 40 and 7, and trade B involves 40, 7 and 91. Each handler currently locks in the order the players joined the group. Show how they can deadlock, give the rule that prevents it, and write the PostgreSQL statement for trade A.

<details>
<summary>Answer and worked solution</summary>

**Answer:** If A holds 40 and waits for 7 while B holds 7 and waits for 40, neither can move. Always lock in ascending `character_id`. Then A locks 7, 12, 40 and B locks 7, 40, 91, and whichever gets 7 first proceeds while the other waits holding nothing.

```sql
SELECT character_id FROM characters
WHERE character_id IN (12, 40, 7)
ORDER BY character_id
FOR UPDATE;
```

PostgreSQL would detect the deadlock after `deadlock_timeout` (1 s by default) and abort one transaction, so nothing corrupts, but a player waits a second and sees a failed split. A single global lock order removes the cycle.
</details>

---

## Week 7: NoSQL and key-value stores (Redis)

Lecture: [w07](../lectures/w07-nosql-and-key-value-stores-redis.md).

28. *Week 7 · compute.* A leaderboard has 5,000,000 players. Use `c = 5 ns` per index entry for the SQL rank query and `2 × log₂ N` steps for the skip list.
   (a) What does a SQL rank lookup cost for the median player?
   (b) At 1,500 lookups per second spread evenly over the board, how many cores does SQL keep busy?
   (c) How many skip-list steps does `ZREVRANK` take?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12.5 ms. (b) 18.75 cores. (c) About 45 steps, for every player.

(a) The median rank is 2,500,000, so SQL reads `r − 1 ≈ 2,500,000` entries, `2.5 × 10⁶ × 5 ns = 12.5 ms`.

(b) The average lookup reads `N / 2` entries. `1,500 × 2,500,000 × 5 ns = 18.75` CPU-seconds per second.

(c) `log₂ 5,000,000 = 22.25`, so `2 × 22.25 = 44.5`, about 45 steps. The SQL cost depends on your rank. The sorted-set cost depends only on the size of the board.
</details>

29. *Week 7 · compute.* A game server loads 30 separate keys for one character at login with individual `GET` commands, over a 0.25 ms round trip. What does the load cost, and what does one `MGET` (or a pipeline) cost? After a restart, 2,000 players log in within a minute. How much round-trip time does each version spend per second of that minute?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 7.5 ms against 0.25 ms per login. During the login rush, about 250 ms of waiting per second against about 8 ms.

`30 × 0.25 = 7.5` ms. One `MGET` is one round trip, 0.25 ms. 2,000 logins a minute is 33.3 per second, so `33.3 × 7.5 = 250` ms against `33.3 × 0.25 = 8.3` ms of round trips per second. The work inside Redis is the same either way. Count round trips, not operations.
</details>

30. *Week 7 · compute.* To break ties by "who got the score first", a team stores `score × 10¹⁰ + (10¹⁰ − t)` in a Redis sorted set, where `t` is a Unix time in seconds. Scores are doubles, so the value must stay below 2⁵³ to be exact. What is the largest integer score that stays exact for every `t` from 0 to 10¹⁰?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 900,718.

The largest stored value is `score × 10¹⁰ + 10¹⁰`. It must stay at or below `2⁵³ = 9,007,199,254,740,992`. So `score ≤ (2⁵³ − 10¹⁰) / 10¹⁰ = 900,718.9`, which rounds down to 900,718. An arena rating of 0 to 5,000 fits easily. A cumulative score in the millions does not, and must use a smaller multiplier or a separate tie-break.
</details>

31. *Week 7 · code.* Five members of a Redis sorted set all have the same score. Redis orders equal scores by comparing member strings byte by byte, as Python does. What do these two lines print, and which member does `ZRANGE lb 0 0` return?

```python
members = ["alice", "Bob", "10", "9", "_zed"]
print(sorted(members))
print(sorted(members, reverse=True))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
['10', '9', 'Bob', '_zed', 'alice']
['alice', '_zed', 'Bob', '9', '10']
```

`ZRANGE lb 0 0` returns `"10"`.

Digits (bytes 48 to 57) come before uppercase letters (65 to 90), then `_` (95), then lowercase (97 to 122). So `"10"` sorts before `"9"` because `'1' < '9'`, whatever the numbers mean. A tie-break that depends on player ids stored as strings is arbitrary. Encode the rule you want into the score.
</details>

32. *Week 7 · design.* For each feature, give a Redis key pattern and type, or say "PostgreSQL" and why: (a) the players currently in dungeon instance 4412; (b) a player's premium currency balance; (c) the weekly raid-clear leaderboard; (d) a login session token.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) `instance:4412:players`, a set, with a per-player heartbeat key carrying a TTL, because a crashed server never sends `SREM`.
- (b) PostgreSQL. A balance players pay real money for is something they would file a ticket about losing, and it must change in the same transaction as the item it buys. AOF `everysec` can lose about a second of writes.
- (c) `lb:raid:2026w39`, a sorted set, rebuilt from PostgreSQL if Redis restarts.
- (d) `session:{token}`, a string holding the player id, with `EXPIRE` refreshed on activity.

The lecture's rule is that PostgreSQL holds anything a player would file a ticket about losing, and Redis holds data that is derived, rebuildable or meant to expire.
</details>

---

## Week 8: Caching and write-behind

Lecture: [w08](../lectures/w08-caching-and-write-behind.md).

33. *Week 8 · compute.* A shard has 6,000 players whose state changes at `u = 0.5` times per second. Give the write-through rate, then the write-behind rate and percentage cut at `T = 2` s, 10 s and 60 s, with the expected loss at each. Where is the knee?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Write-through 3,000 writes/s. `T = 2`: 1,896 (37% cut), loss 1 s. `T = 10`: 596 (80% cut), loss 5 s. `T = 60`: 100 (96.7% cut), loss 30 s. The knee is between `1/u = 2` s and `3/u = 6` s.

`W = N × (1 − e^(−uT)) / T`. At `T = 2`, `uT = 1`, `1 − e^(−1) = 0.632`, `6,000 × 0.632 / 2 = 1,896`. At `T = 10`, `uT = 5`, `1 − e^(−5) = 0.993`, `6,000 × 0.993 / 10 = 596`. At `T = 60`, nearly every player is dirty at each flush, `6,000 / 60 = 100`. Expected loss is `T / 2`. Going from 10 s to 60 s saves 496 writes per second for 25 s more expected loss, about 20 writes per second of risk. Going from 2 s to 10 s saves 1,300 for 4 s more, about 325. The savings are front-loaded.
</details>

34. *Week 8 · compute.* A cache serves `R = 40,000` reads per second with `t_c = 0.4 ms` and `t_db = 4 ms`. Compare a 92% and a 98% hit ratio on database reads per second and average latency.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 92%: 3,200 DB reads/s, 0.72 ms. 98%: 800 DB reads/s, 0.48 ms. Six points of hit ratio cut database load by a factor of 4.

DB reads `R × (1 − h)`, so `40,000 × 0.08 = 3,200` and `40,000 × 0.02 = 800`. Average latency `h × t_c + (1 − h) × (t_c + t_db) = t_c + (1 − h) × t_db`. That is `0.4 + 0.08 × 4 = 0.72` ms and `0.4 + 0.02 × 4 = 0.48` ms. Convert hit ratios to miss ratios before comparing them.
</details>

35. *Week 8 · code.* Three flush batches reach the database, the third one a retried, older flush. What does the script print?

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE char_state (id INTEGER PRIMARY KEY, hp INTEGER, version INTEGER)")
UPSERT = """INSERT INTO char_state (id, hp, version) VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET hp = excluded.hp, version = excluded.version
            WHERE excluded.version > char_state.version"""
batches = [
    [(1, 90, 1), (2, 70, 1)],
    [(1, 50, 3)],
    [(1, 80, 2), (2, 65, 2)],   # a retried, older flush for player 1
]
for batch in batches:
    with con:
        con.executemany(UPSERT, batch)
print(con.execute("SELECT id, hp, version FROM char_state ORDER BY id").fetchall())
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `[(1, 50, 3), (2, 65, 2)]`.

Player 1 reaches version 3 with 50 hp in the second batch. The retried row `(1, 80, 2)` carries version 2, which is not greater than 3, so the `WHERE` skips it and the newer 50 hp survives. Player 2's version 2 is newer than its stored version 1, so it applies. Without the version check the retry would have written 80 hp back over 50, which is how a flush retry or a zone handoff resurrects old state. With it, running a batch twice is harmless (idempotent).
</details>

36. *Week 8 · compute.* A healthy cache answers 95% of reads with `t_c = 0.3 ms` over a database at `t_db = 3 ms`. Then the cache starts failing and every request waits for a 100 ms timeout before going to the database. Compare the average latency healthy, failing, and with no cache at all, and name the two design rules this motivates.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Healthy 0.45 ms. Failing 103 ms. No cache 3 ms. A failing cache is 34 times slower than having no cache.

Healthy, `0.3 + 0.05 × 3 = 0.45` ms. Failing, every read pays the full timeout and then the database, `100 + 3 = 103` ms. Without a cache, 3 ms. Worker threads blocked on the timeout run out, as in Fortnite's February 2018 account-service outage described in the lecture. Set cache timeouts far below your request budget (a few milliseconds), and add a circuit breaker that skips the cache for a while after errors.
</details>

---

## Week 9: Schema migrations in a live game

Lecture: [w09](../lectures/w09-schema-migrations-in-a-live-game.md).

37. *Week 9 · compute.* A backfill must fill 24 million rows. The database updates `r = 15,000` rows per second, each batch costs `o = 8 ms` of overhead, and the stall budget is 40 ms. At duty cycle `d = 0.4`, give the batch size, the number of batches, the time per batch, the running time, the total time, the floor `N / (r × d)` and the overhead share.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `b = 600`, 40,000 batches, 0.048 s each, 1,920 s running, 4,800 s total (1.33 h), floor 4,000 s, overhead share 16.7%.

`b = r × budget = 15,000 × 0.04 = 600`. Batches `24,000,000 / 600 = 40,000`. Each runs `600 / 15,000 + 0.008 = 0.048` s. Running time `40,000 × 0.048 = 1,920` s. Total `1,920 / 0.4 = 4,800` s. The floor is `24,000,000 / (15,000 × 0.4) = 4,000` s, and the other 800 s are overhead, `0.008 / 0.048 = 16.7%` of every batch.
</details>

38. *Week 9 · compute.* Same backfill as question 37. (a) What minimum duty cycle finishes it within 2 hours? (b) The producer now wants it done in 30 minutes. Is that possible with `b = 600`? If not, what is the smallest batch size that makes it possible at `d = 1`, and what stall does that cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `d ≥ 0.27`. (b) No. It needs `b ≥ 960`, which raises the worst stall to 64 ms, over budget.

(a) Running time is 1,920 s and the deadline is 7,200 s, so `d ≥ 1,920 / 7,200 = 0.267`.

(b) At `b = 600` the running time alone is 1,920 s, more than 1,800 s, even with no pauses. Total time at `d = 1` is `N / r + N × o / b = 1,600 + 192,000 / b`. Setting that to at most 1,800 gives `b ≥ 960`. The stall becomes `960 / 15,000 = 0.064` s. The two knobs have separate jobs. To meet this deadline you must either accept a longer stall, raise `r`, or move the deadline, and `d = 1` also starves game writes, replicas and vacuum.
</details>

39. *Week 9 · design.* Classify each change for PostgreSQL 16 as metadata-only, scan or rewrite, following the lecture's table: (a) `ADD COLUMN bound boolean DEFAULT false`; (b) `ADD COLUMN seed double precision DEFAULT random()`; (c) `ALTER COLUMN gold TYPE bigint` from `integer`; (d) `ALTER COLUMN durability SET NOT NULL` with no `CHECK` constraint in place; (e) `DROP COLUMN legacy_flags`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) metadata-only. (b) rewrite. (c) rewrite. (d) scan. (e) metadata-only.

(a) A constant default is stored once in the catalog since PostgreSQL 11 and returned for old rows. (b) `random()` is volatile, so each row needs its own value and the table and its indexes are rewritten. (c) Changing `integer` to `bigint` changes the stored width, which rewrites the table and its indexes under an `ACCESS EXCLUSIVE` lock for the whole rewrite. (d) `SET NOT NULL` must read every row to prove there are no NULLs. Adding `CHECK (durability IS NOT NULL) NOT VALID` and then `VALIDATE CONSTRAINT` first lets `SET NOT NULL` skip that scan. (e) Dropping a column only marks it dropped in the catalog.
</details>

40. *Week 9 · code.* Ten items exist. Odd ids are type 2 (max durability 120) and even ids are type 1 (max durability 40). New server code has already written durability 7 on items 3 and 6. What does the script print, and why is the second list all zeros?

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE item_def (id INTEGER PRIMARY KEY, max_durability INTEGER);
CREATE TABLE item_instance (id INTEGER PRIMARY KEY, def_id INTEGER, durability INTEGER);
INSERT INTO item_def VALUES (1, 40), (2, 120);
""")
con.executemany("INSERT INTO item_instance VALUES (?, ?, NULL)",
                [(i, 1 + i % 2) for i in range(1, 11)])
con.execute("UPDATE item_instance SET durability = 7 WHERE id IN (3, 6)")  # written by new code

def backfill(b):
    counts = []
    for lo in range(1, 11, b):
        with con:
            n = con.execute("""UPDATE item_instance SET durability =
                   (SELECT max_durability FROM item_def WHERE item_def.id = item_instance.def_id)
                 WHERE id BETWEEN ? AND ? AND durability IS NULL""", (lo, lo + b - 1)).rowcount
        counts.append(n)
    return counts

print(backfill(4), backfill(4))
print(con.execute("SELECT SUM(durability) FROM item_instance").fetchone()[0])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[3, 3, 2] [0, 0, 0]
654
```

The batches cover ids 1 to 4, 5 to 8 and 9 to 10. In the first, item 3 already has a value, so 3 rows change. In the second, item 6 is skipped, 3 rows. The last has 2. The second run finds no NULLs and changes nothing, which is what makes the job safe to rerun after a crash. The total is four odd items at 120, four even items at 40, and the two 7s written by new code, `480 + 160 + 14 = 654`. The `durability IS NULL` filter is also what stops the backfill from overwriting values the new code wrote.
</details>

---

## Week 10: Telemetry design, events and properties

Lecture: [w10](../lectures/w10-telemetry-design-events-and-properties.md).

41. *Week 10 · compute.* A `quest_step_completed` event carries the lecture's 54-byte envelope plus `quest_id` (int), `step` (smallint), `zone_id` (int) and `duration_s` (int). The game has 75,000 DAU and 30 quest steps per player per day. Using 28 bytes of row overhead, give bytes per row, rows per day, MB per day and GB per year.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 96 bytes per row, 2,250,000 rows per day, 216 MB per day, 78.8 GB per year.

Properties `4 + 2 + 4 + 4 = 14` bytes. Row `28 + 54 + 14 = 96`. Rows `75,000 × 30 = 2,250,000`. Bytes `96 × 2,250,000 = 216,000,000` a day, and `216 × 365 = 78,840` MB a year. The envelope and overhead are 82 of the 96 bytes, which is why adding a property or two barely moves the bill.
</details>

42. *Week 10 · compute.* Your analytics tool allows 15,000 unique combinations per day. You want a death heat map across 25 zones of 1,000 m by 1,000 m. What is the smallest square cell size, in whole multiples of 10 m, that fits? Where should the bucketing happen?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 50 m, bucketed in the query, not in the event.

Cells per zone must be at most `15,000 / 25 = 600`, so at most 24 × 24 = 576 per zone (25 × 25 = 625 is too many). The cell must be at least `1,000 / 24 = 41.7` m. At 40 m the grid is 25 × 25, 625 per zone, 15,625 in total, over the limit. At 50 m it is 20 × 20, 400 per zone, 10,000 in total, which fits. Store raw `x` and `y` in the event and compute `floor(x / 50)` where you aggregate, so a finer map around one arena is still possible later.
</details>

43. *Week 10 · critique.* A tracking plan contains these three events. Find at least one problem with each and rewrite it: (a) `LevelUp_Warrior`, `LevelUp_Mage` and so on, one per class, sent by the client; (b) `player_level_up` with properties `player_name` and `new_level`; (c) `gold_earned` sent by the client with property `amount`.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- (a) A value (the class) is baked into the name, the naming is not `object_action` in lower snake case, and level-ups feed progression decisions, so they should come from the server. Rewrite as one server event `character_leveled_up` with `class_id` and `new_level`.
- (b) `player_name` is a direct identifier in the event body, which breaks pseudonymisation (week 13) and duplicates what the envelope's id already gives. Drop it. Keep `new_level`, and name the event in the past tense, `character_leveled_up`.
- (c) Gold feeds the economy and could feed bans or rewards, so a client-sent amount is untrustworthy. Send `gold_changed` from the server with `amount`, `source_kind` and the new balance.

The fixes follow the lecture's rules. No values in names. Identify players only through the envelope. Anything that could feed an economic decision, a ban or a reward comes from the server.
</details>

44. *Week 10 · explain.* The live team asks "which zone is the deadliest?" and a dashboard shows zone 7 with the most deaths. Why might that answer be wrong, and what event must the tracking plan add to fix it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Zone 7 may simply hold the most player-hours. Deaths need a denominator, an exposure event such as `zone_entered` and `zone_left` (or a periodic heartbeat), so the question becomes deaths per hour played in each zone.

Suppose zone 7 has 25,000 deaths in 12,500 player-hours and zone 3 has 6,000 in 1,500. Zone 7 has four times the deaths but 2 deaths per hour against zone 3's 4. Numerators come free with the event. Denominators have to be designed before launch, because history recorded without them cannot be recovered.
</details>

---

## Week 11: Pipelines, collect, store, query

Lecture: [w11](../lectures/w11-pipelines-collect-store-query.md).

45. *Week 11 · compute.* A game has 90,000 DAU, 300 events per player per day, 6% of events are deaths, 50 zones and 60 days of raw retention. At 20 million rows per second, give rows touched and time for "deaths in zone 12 yesterday" under L0, L1, L2 and L3. A wall screen runs 120 such queries a minute. How many cores does it keep busy at L0 and at L1?

<details>
<summary>Answer and worked solution</summary>

**Answer:** L0 1.62 billion rows, 81 s. L1 27 million rows, 1.35 s. L2 32,400 rows, 1.62 ms. L3 one row. The wall screen needs 162 cores at L0 and 2.7 at L1.

Rows per day `90,000 × 300 = 27,000,000`. L0 reads 60 days, `1.62 × 10⁹` rows, `/ 2 × 10⁷ = 81` s. L1 reads one day, 1.35 s. L2 reads that day's deaths in one zone, `27,000,000 × 0.06 / 50 = 32,400` rows, 1.62 ms. L3 reads the rollup row. Cores busy are `queries per minute × time / 60`, so `120 × 81 / 60 = 162` and `120 × 1.35 / 60 = 2.7`. Build a rollup or index for any tile that refreshes.
</details>

46. *Week 11 · code.* A loader stores four batches, one of them a retry whose acknowledgement was lost. What does the script print, and which line is the one a dashboard should trust?

```python
import sqlite3
batches = [
    [("e1", "death", 7), ("e2", "death", 7), ("e3", "loot", 7)],
    [("e4", "death", 3), ("e5", "death", 7)],
    [("e4", "death", 3), ("e5", "death", 7)],   # retry: the ack was lost
    [("e6", "death", 7)],
]
for keyed in (False, True):
    con = sqlite3.connect(":memory:")
    pk = "PRIMARY KEY" if keyed else ""
    con.execute(f"CREATE TABLE raw (event_id TEXT {pk}, type TEXT, zone INTEGER)")
    for batch in batches:
        con.executemany("INSERT OR IGNORE INTO raw VALUES (?, ?, ?)", batch)
    print(con.execute("SELECT COUNT(*), SUM(type = 'death' AND zone = 7) FROM raw").fetchone())
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
(8, 5)
(6, 4)
```

Trust the second line. Without a key, `INSERT OR IGNORE` has nothing to conflict on, so the retried batch lands twice and zone-7 deaths read 5 (e1, e2, e5, e5, e6). With `event_id` as the primary key, the retry is skipped and the count is the true 4. Delivery is at-least-once, so idempotent storage is what makes the count exactly-once. In PostgreSQL the same idea is `ON CONFLICT (event_time, event_id) DO NOTHING` on a table partitioned by time.
</details>

47. *Week 11 · compute.* A mobile client emits an event every 8 seconds and flushes its batch every 45 seconds. At most how many events can a crash lose? What flush interval keeps the worst case at 4 events? The collector receives 300,000 events per second. How many HTTP requests per second is that at a batch size of 50?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 5 or 6 events, so plan for 6. Flush every 32 s or less for at most 4. 6,000 requests per second.

A 45 s window holds `45 / 8 = 5.6` event intervals, so 5 or 6 events depending on where the crash falls. For at most 4, flush at least every `4 × 8 = 32` s. Requests are `events per second / batch size = 300,000 / 50 = 6,000`. Writing unsent batches to local storage before the flush removes most of the crash risk without shrinking batches.
</details>

48. *Week 11 · explain.* The daily rollup for Tuesday was built at 00:05 Wednesday. Monday's was built at 04:00 Tuesday. A report says "deaths fell 1.1% on Tuesday after the hotfix". What should you check before believing it, and which lateness policy would have prevented the comparison?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Check how many of Tuesday's events arrived after 00:05. The two days were built at different lags, so Tuesday is missing its late events and Monday is not. A sliding-window rebuild (rebuild the last 3 days each night, marked provisional) or a fixed late build time for every day removes the artifact.

Late client events belong to the day of their `event_time` but arrive after midnight. In Lab 11's data a build at 00:05 missed 0.7% of one day's deaths, the same order as the claimed effect. Compare days built at the same lag, or rebuild Tuesday after its stragglers arrive, before reading anything into a 1% change.
</details>

---

## Week 12: Dashboards and KPIs

Lecture: [w12](../lectures/w12-dashboards-and-kpis.md). Questions 49 and 50 use the lecture's six-account week (A1 to A6, section 2).

49. *Week 12 · compute.* Using the six-account week, compute daily DAU (Monday to Sunday), sum, mean DAU, WAU and stickiness for (a) a 16-minute threshold, UTC day, accounts; (b) any session, local day, people.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) DAU 1, 2, 3, 1, 1, 3, 2, sum 13, mean 1.86, WAU 5, stickiness 0.371. (b) DAU 3, 3, 3, 3, 2, 3, 4, sum 21, mean 3.00, WAU 5, stickiness 0.600.

(a) A3 (2-minute sessions) drops out, and so do A2's 3-minute Monday and 15-minute Saturday. A2 keeps Wednesday (20). A6 keeps Wednesday (25). Monday A1; Tuesday A1, A4; Wednesday A2, A4, A6; Thursday A1; Friday A4; Saturday A1, A4, A5; Sunday A1, A5. WAU counts A1, A2, A4, A5, A6. Stickiness `13 / (7 × 5) = 0.371`.

(b) A4's sessions move one day earlier, including next Monday's onto this Sunday. A1 and A2 merge into P1. Monday P1, P2, P3; Tuesday P1, P2, P3; Wednesday P1, P2, P5; Thursday P1, P2, P3; Friday P2, P3; Saturday P1, P2, P4; Sunday P1, P2, P3, P4. Five people. Stickiness `21 / 35 = 0.600`. Against D1 (0.524), both lenses move the number, one down and one up.
</details>

50. *Week 12 · query.* The tables below hold five accounts and eleven sessions. Write a query that returns, per install day, the cohort size and exact-day D1 and D7 retention (UTC), and give its result. Then give the DAU per day, the sum of DAU, and the number of distinct accounts active over the whole period.

```sql
CREATE TABLE accounts (account_id INTEGER PRIMARY KEY, install_day TEXT);
CREATE TABLE sessions (account_id INTEGER, start_utc TEXT, minutes INTEGER);
INSERT INTO accounts VALUES (1,'2026-03-01'), (2,'2026-03-01'), (3,'2026-03-01'),
                            (4,'2026-03-02'), (5,'2026-03-02');
INSERT INTO sessions VALUES
 (1,'2026-03-01 18:00',40), (1,'2026-03-02 19:00',30), (1,'2026-03-08 20:00',25),
 (2,'2026-03-01 09:00',12), (2,'2026-03-09 21:00',50),
 (3,'2026-03-01 23:30',90), (3,'2026-03-02 00:10',15),
 (4,'2026-03-02 12:00',20), (4,'2026-03-03 12:00',20), (4,'2026-03-09 12:00',20),
 (5,'2026-03-02 17:00',5);
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1 March cohort, 3 accounts, D1 0.667, D7 0.333. 2 March cohort, 2 accounts, D1 0.5, D7 0.5. DAU 3, 4, 1, 1, 2 on 1, 2, 3, 8 and 9 March, summing to 11 user-days. Distinct accounts active: 5.

```sql
SELECT a.install_day,
       COUNT(*) AS cohort,
       AVG(EXISTS (SELECT 1 FROM sessions s WHERE s.account_id = a.account_id
                   AND date(s.start_utc) = date(a.install_day, '+1 day'))) AS d1,
       AVG(EXISTS (SELECT 1 FROM sessions s WHERE s.account_id = a.account_id
                   AND date(s.start_utc) = date(a.install_day, '+7 days'))) AS d7
FROM accounts a
GROUP BY a.install_day
ORDER BY a.install_day;
```

For 1 March, accounts 1 and 3 played on 2 March (account 3's 00:10 session counts even though it continues a late-night one), so D1 is 2/3. Only account 1 played on 8 March, so D7 is 1/3. Account 2 played on 9 March, day 8, which exact-day D7 ignores and rolling D7 (2/3) would count. For 2 March, account 4 played on 3 and 9 March, account 5 never returned. The five days' DAU sum to 11, while only 5 accounts exist, because summing DAU counts user-days.
</details>

51. *Week 12 · compute.* A game reports MAU 400,000 and DAU/MAU 0.22. What is its mean DAU, and how many days a month does the typical monthly player play? The MAU comes from one Redis HyperLogLog per day. What is one standard error, and how much memory do the 30 daily keys use at most?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Mean DAU 88,000. About 6.6 days a month. One standard error is about 3,240 users. At most 360 KB.

`0.22 × 400,000 = 88,000`. Stickiness is mean active days divided by the window, so `0.22 × 30 = 6.6` days. Redis documents a standard error of 0.81%, `0.0081 × 400,000 = 3,240`. Each key is at most 12 KB, so 30 keys are at most 360 KB. A day-over-day MAU change of 2,000 is inside one standard error and should not be announced.
</details>

52. *Week 12 · compute.* A game with 250,000 DAU keeps an exact `user_day(day, account_id)` table at about 40 bytes per row. How much does it grow per day and per year? Compare it with summing a stored `daily_dau` column over 30 days for MAU.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 10 MB per day, about 3.65 GB per year. The sum of 30 DAU values measures user-days, not users, so it overstates MAU by the average number of active days per monthly player.

`250,000 × 40 = 10,000,000` bytes a day, `× 365 = 3.65 × 10⁹` bytes. `COUNT(DISTINCT account_id)` over 30 days of `user_day` gives the exact MAU. At the stickiness of question 51, the sum of DAUs would be about 6.6 times the MAU. Counts add across days. Distinct counts do not.
</details>

---

## Week 13: Privacy, GDPR and data retention

Lecture: [w13](../lectures/w13-privacy-gdpr-and-data-retention.md).

53. *Week 13 · compute.* A telemetry store has `D = 25,000` daily players, `e = 2,000` events each, `b = 180` bytes per event and `R = 120` days. It scans at 1.5 GB/s and receives 200 erasure requests a month. Give daily volume, storage, one full scan, monthly scan hours for per-request scans (strategy A) and for weekly batches, rows examined per request with an index (strategy B) for a player active on 15 days, and the index size at 24 bytes per row.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 50 million events and 9 GB a day, 1.08 TB stored, 12 minutes per scan, 40 hours a month per-request or 48 minutes with weekly batches, 30,000 rows per indexed request, a 144 GB index.

`25,000 × 2,000 = 50,000,000` events a day, `× 180 = 9 GB`. Storage `9 GB × 120 = 1,080 GB`. One scan `1,080 / 1.5 = 720` s. Per request, `200 × 720 = 144,000` s, 40 h. Weekly batches, `4 × 12 = 48` min. Strategy B visits `e × a = 2,000 × 15 = 30,000` rows. The index holds `24 × 50,000,000 × 120 = 144 GB`. Strategy C, a pseudonym table, touches 2 rows per request at any `R`.
</details>

54. *Week 13 · compute.* A studio keeps chat logs 2 days by default, 14 days if reported without action, and 365 days if action is taken. 8% of logs are reported without action and 0.5% are actioned. What is the average stored lifetime of a log, and what share of stored logs sits in the actioned tier?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 4.78 days on average. The 0.5% actioned tier holds 38% of storage.

Average lifetime `2 + 0.08 × (14 − 2) + 0.005 × (365 − 2) = 2 + 0.96 + 1.815 = 4.775` days. Stored amount is proportional to share times days. Default `0.915 × 2 = 1.83`, reported `0.08 × 14 = 1.12`, actioned `0.005 × 365 = 1.825`. They sum to 4.775, and the actioned tier is `1.825 / 4.775 = 38.2%`. A tiered window is dominated by its long tier, so the rule that sends rows there matters most.
</details>

55. *Week 13 · code.* A designer pseudonymises telemetry with a truncated SHA-256 of the player id. What does the script print, and what does it show? Why does the third line differ?

```python
import hashlib, hmac
def pseudo(pid):
    return hashlib.sha256(str(pid).encode()).hexdigest()[:16]
leaked = pseudo(81234)
table = {pseudo(pid): pid for pid in range(1, 200_001)}
print(leaked, table.get(leaked))
key = b"kept-in-another-system"
keyed = hmac.new(key, b"81234", hashlib.sha256).hexdigest()[:16]
print(table.get(keyed))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `3c19414715d57283 81234`, then `None`.

Anyone who sees the pseudonym can hash every plausible id (here 200,000 of them, in well under a second) and look it up, so the "pseudonym" reverses to player 81234. Hashing is fast by design, which is the wrong property here. The keyed hash (HMAC) cannot be reversed from the table without the key. Keep the key in a separate system, or use a random `telemetry_id` in a mapping table and delete the mapping row on erasure.
</details>

56. *Week 13 · code.* What do the three `print` lines show, and what does the result mean for an erasure request?

```python
import sqlite3, tempfile, os
path = os.path.join(tempfile.mkdtemp(), "t.db")
con = sqlite3.connect(path)
con.execute("PRAGMA secure_delete = OFF")
con.execute("CREATE TABLE accounts (player_id INTEGER PRIMARY KEY, email TEXT)")
con.executemany("INSERT INTO accounts VALUES (?, ?)",
                [(i, f"player{i}@example.com") for i in range(1, 21)])
con.commit()
def hits():
    return open(path, "rb").read().count(b"player7@example.com")
print("before", hits())
con.execute("DELETE FROM accounts WHERE player_id = 7"); con.commit()
print("after DELETE", hits(), con.execute("SELECT COUNT(*) FROM accounts WHERE player_id = 7").fetchone()[0])
con.execute("VACUUM")
print("after VACUUM", hits())
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
before 1
after DELETE 1 0
after VACUUM 0
```

After the `DELETE`, SQL can no longer see the row (count 0), but the email's bytes are still in the file. Only `VACUUM`, which rewrites the file, removes them. `PRAGMA secure_delete = ON` would overwrite the content at delete time instead. In PostgreSQL the dead row version stays until vacuum and is only guaranteed gone after `VACUUM FULL` or a dropped partition. Erasure must also reach replicas, caches, backups (put beyond use, and erasures re-applied after a restore) and exports.
</details>

57. *Week 13 · design.* Write a retention schedule row (purpose, window, deletion mechanism, erasure strategy) for (a) raw gameplay events, (b) IP connection logs and (c) nightly database backups, for a small EU MMO. Justify each window in one sentence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One reasonable schedule, in the lecture's form:

| Category | Purpose | Window | Deletion mechanism | Erasure strategy |
|---|---|---|---|---|
| Raw gameplay events | Balance and bug hunting | 30 days | Drop the daily partition | C, pseudonym table |
| IP connection logs | Security and fraud | 90 days | Drop partition | B, index on account |
| Nightly backups | Disaster recovery | 35 days | Rotation | Beyond use, re-apply erasures after any restore |

Raw events are most useful in the weeks after a patch, and a 30-day window means the retention job itself completes most erasures within the one-month deadline. Fraud investigations reach back a few months, so IPs need longer, and an index lets you find one account's rows. Backups need to reach past the longest silent corruption you expect, and GDPR guidance accepts that they hold erased data until rotation if they are not used for anything else. The windows are teaching examples. Real ones are set with a privacy lawyer.
</details>

---

## Week 14: Backups and disaster recovery

Lecture: [w14](../lectures/w14-backups-and-disaster-recovery.md).

58. *Week 14 · compute.* An 800 GB database restores at 320 MB/s, writes 15 GB of WAL an hour and replays 120 GB/h. Base backups run every 12 hours with WAL archived every 30 s. Detection takes 20 minutes and verification 10. Give the worst-case RPO, average RPO and worst-case RTO.

<details>
<summary>Answer and worked solution</summary>

**Answer:** RPO worst 30 s, average 15 s. RTO worst about 2.69 h.

With WAL archiving, `RPO_worst ≈ I_arch = 30` s and the average is half. The copy term is `800,000 MB / 320 MB/s = 2,500` s, 0.694 h. Worst-case replay is `w × I_base / r = 15 × 12 / 120 = 1.5` h. RTO worst `0.333 + 0.694 + 1.5 + 0.167 = 2.69` h. The base interval does not appear in the RPO, and the archive interval does not appear in the RTO.
</details>

59. *Week 14 · compute.* Same database as question 58. The producer wants worst-case RTO under 2 hours. What is the longest base backup interval that achieves it, and what RTO does a 6-hour interval give?

<details>
<summary>Answer and worked solution</summary>

**Answer:** At most about 6.4 hours. A 6-hour interval gives about 1.94 h.

The fixed part is `0.5 + 0.694 = 1.194` h (detect, verify, copy), leaving `2 − 1.194 = 0.806` h for replay. `15 × I_base / 120 ≤ 0.806` gives `I_base ≤ 6.44` h. At 6 h, replay is `15 × 6 / 120 = 0.75` h, and RTO is `1.194 + 0.75 = 1.94` h. Changing `I_arch` would not have helped at all.
</details>

60. *Week 14 · compute.* A server sets `archive_timeout = 20 s` with 16 MB WAL segments. How much archive does one idle day produce? How does that compare with the documentation's suggested value of about a minute?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 4,320 segments, about 69 GB a day of archive for a server that did nothing, three times the 23 GB a day at 60 s.

`86,400 / 20 = 4,320` segments, `× 16 MB = 69,120` MB. An early-archived segment is still full length, so a short timeout buys a smaller RPO with a steady stream of mostly empty files. At 60 s it is `1,440 × 16 MB = 23` GB.
</details>

61. *Week 14 · code.* A lab-style restore replays a logical log onto a base backup. The GM script at t = 700 wrongly subtracted gold from both players. What do the two lines print? Then give the gold after a selective repair that keeps every legitimate change and removes only the script's.

```python
base = {"t": 600, "gold": {"ana": 120, "bo": 80}}          # base backup at t = 600
log = [                                                     # archived logical log
    (610, "ana", +30), (655, "bo", -20), (700, "ana", -150),  # t = 700: the GM script
    (700, "bo", -60), (720, "bo", +15), (760, "ana", +5),
]
def restore(target_t):
    gold = dict(base["gold"])
    replayed = 0
    for t, who, delta in log:
        if base["t"] < t <= target_t:
            gold[who] += delta
            replayed += 1
    return gold, replayed
print(restore(699))
print(restore(800))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
({'ana': 150, 'bo': 60}, 2)
({'ana': 5, 'bo': 15}, 6)
```

Selective repair gives ana 155 and bo 75.

`restore(699)` replays only the two records after the base and before the target. `restore(800)` replays all six, including the script. Skipping the two t = 700 records and replaying the rest gives ana `150 + 5 = 155` and bo `60 + 15 = 75`. That only works because this log is logical and the later changes do not depend on the bad ones. PostgreSQL's WAL is physical, so it cannot skip one transaction, which is why studios keep their own logical log of economy changes.
</details>

62. *Week 14 · compute.* A studio keeps 28 days of backups, with a 250 GB base every day and about 90 GB of WAL a day. How much storage is that? How much if it keeps daily bases only for the last 7 days and weekly bases for the other three weeks, with all WAL kept?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 9,520 GB with daily bases throughout. 5,020 GB with the weekly scheme.

Daily: `28 × (250 + 90) = 9,520` GB. Weekly scheme: `7 × 250 + 3 × 250 + 28 × 90 = 1,750 + 750 + 2,520 = 5,020` GB. The saving costs replay time for old restore points, up to a week of WAL (`7 × 90 = 630` GB) for a point in the third week. The window itself should come from the longest silent corruption you can imagine, and it also caps how long erased data survives.
</details>

---

## Across the course: viva questions for the final service

These questions ask about your own service. Model answers describe what a strong answer contains.

63. *Weeks 5, 6 and 8 · design.* Your inventory service caches character state with write-behind. Walk through a trade between two players, from request to commit, naming every step that stops a dupe and every step that stops a lost update.

<details>
<summary>What a strong answer contains</summary>

The service flushes both characters' dirty state before the trade, so PostgreSQL (or SQLite) holds the only current copy. It opens one transaction and locks both characters in ascending id order, or uses conditional updates only. It moves the item with `UPDATE items SET owner_id = :to WHERE item_id = :id AND owner_id = :from`, checks `rowcount == 1`, moves gold with `gold = gold - :p WHERE gold >= :p`, writes the trade log row, and commits synchronously. It bumps each character's version so a late write-behind flush of old state is refused by the `excluded.version > version` clause. A strong answer cites its own stress-test numbers, for example 0 dupes in 2,000 concurrent attempts, and names which week each guard comes from.
</details>

64. *Weeks 10 to 13 · design.* Show the path of one `item_traded` telemetry event in your service, from the moment the trade commits to a dashboard tile, and say what happens to it when the seller asks for erasure.

<details>
<summary>What a strong answer contains</summary>

The event is created by the server inside or right after the trade transaction, with the envelope (`event_id`, type, `event_time`, a pseudonymous `telemetry_id`, session, build) and properties such as item type, price and zone, and no names. It is loaded with `INSERT ... ON CONFLICT DO NOTHING` (or `INSERT OR IGNORE`) into a table partitioned or indexed by day. A nightly idempotent rollup builds the tile's table at a stated grain, and the tile footnotes its definition and marks provisional days. On erasure the mapping row and account row are deleted, so the raw event can no longer be linked to the seller, and the retention job drops the raw partition after the window. Aggregates contain no player key and keep minimum group sizes.
</details>

65. *Weeks 9 and 14 · design.* Your service ships a migration that adds `soulbound` to items while players trade. Then an operator runs it twice by mistake. What happens, and how would you restore if the second run had been destructive?

<details>
<summary>What a strong answer contains</summary>

The migration is numbered and recorded in `schema_migrations` inside the same transaction, so the runner skips it the second time. The backfill is batched by primary-key range, filters on `soulbound IS NULL`, records progress, and changes nothing on a rerun. If a destructive statement had run, the answer uses the service's backup script, the verification check and the runbook. Restore the newest base before the mistake, replay the log to just before it, re-apply erasures made after the backup, verify, then choose between rollback and selective repair with the numbers from the drill (measured RPO and RTO).
</details>
