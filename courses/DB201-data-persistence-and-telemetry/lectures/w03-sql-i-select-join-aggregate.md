# DB201 · Week 03 — SQL I: Select, Join, Aggregate

**Why this matters:** Once your game's state lives in tables, every question a designer, economist or support agent asks becomes a SQL query. "Which class is richest?" "How many Emberfang Swords exist?" "Who has never picked up an item?" A correct query answers in milliseconds. A query that looks correct and double counts will put a wrong number on a dashboard, and someone will nerf a class because of it.

**You will be able to:**
- Write `SELECT` queries that filter, sort, limit, join and group, and predict the result of each clause from the order in which SQL evaluates them.
- Compute how many rows a join produces from the match counts per key, and predict exactly how much a join inflates a `SUM` or `COUNT`.
- Fix a fan-out join by aggregating before joining, and find rows with no match using a left join or `NOT EXISTS`.
- State the grain of a table (what one row means) and choose between `COUNT(*)`, `COUNT(column)` and `SUM(quantity)` for a question.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 2, the section "Query Languages for Data" (declarative versus imperative queries). PostgreSQL documentation, Tutorial chapter "The SQL Language", sections "Querying a Table", "Joins Between Tables" and "Aggregate Functions".

**Prerequisites from earlier courses:** The schema for characters, item types, items and affixes, [DB201 week 2](w02-relational-modeling-characters-inventories-items.md). Loops and nested loops, and why a loop inside a loop multiplies work, [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). Sums, means and grouping from playtest data, [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md). Looking ahead, [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (year 3) puts these queries to work on an economy; you do not need it this week.

**Interactive:** [Join fan-out](../examples/w03-join-fan-out.html). Keep it open during section 2.

---

## 1. Reading a SELECT

All examples this week run on a four-character world you can build yourself. Paste this into the `sqlite3` shell or run it with Python's `sqlite3` module:

```sql
CREATE TABLE characters (character_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE,
  class TEXT NOT NULL, level INTEGER NOT NULL, gold INTEGER NOT NULL);
CREATE TABLE item_types (type_id INTEGER PRIMARY KEY, name TEXT NOT NULL,
  rarity TEXT NOT NULL, max_stack INTEGER NOT NULL, vendor_price INTEGER NOT NULL);
CREATE TABLE items (item_id INTEGER PRIMARY KEY, type_id INTEGER NOT NULL REFERENCES item_types,
  owner_id INTEGER NOT NULL REFERENCES characters, quantity INTEGER NOT NULL);
CREATE TABLE quest_completions (character_id INTEGER NOT NULL REFERENCES characters,
  quest_id INTEGER NOT NULL, PRIMARY KEY (character_id, quest_id));

INSERT INTO characters VALUES (1,'Aria','warrior',12,500), (2,'Bram','mage',9,300),
  (3,'Cyra','rogue',15,200), (4,'Dax','mage',4,0);
INSERT INTO item_types VALUES (1,'Minor Healing Potion','common',20,5),
  (2,'Emberfang Sword','rare',1,400), (3,'Copper Ore','common',50,1);
INSERT INTO items VALUES (101,1,1,12), (102,2,1,1), (103,3,1,30),
  (104,1,2,5), (105,3,2,50), (106,2,4,1);
INSERT INTO quest_completions VALUES (1,10), (1,11), (2,10), (2,11), (2,12), (2,13), (3,10);
```

In words: Aria has 3 item stacks and 2 quests, Bram has 2 stacks and 4 quests, Cyra has no items and 1 quest, Dax has 1 item (a sword) and no quests.

A query has up to seven clauses. You write them in one order and the database evaluates them in another. Learn the evaluation order and most SQL surprises disappear.

| Written order | Evaluated | What it does |
|---|---|---|
| `SELECT` | 5th | choose and compute output columns |
| `FROM` / `JOIN` | 1st | build the working set of rows |
| `WHERE` | 2nd | keep rows that pass a test, before grouping |
| `GROUP BY` | 3rd | collapse rows into groups |
| `HAVING` | 4th | keep groups that pass a test, after grouping |
| `ORDER BY` | 6th | sort the output |
| `LIMIT` | 7th | keep the first N output rows |

```sql
SELECT name, gold
FROM characters
WHERE level >= 9
ORDER BY gold DESC
LIMIT 2;
```

Read it in evaluation order: start from all four characters, keep the three at level 9 or above (Aria, Bram, Cyra), sort by gold descending, keep two. Result: Aria 500, Bram 300.

Two consequences of the order:

- `WHERE` cannot use an aggregate like `sum(gold)`, because grouping has not happened yet when `WHERE` runs. Use `HAVING` for tests on groups.
- An alias defined in `SELECT` is not visible in `WHERE`, because `SELECT` runs later. PostgreSQL rejects `WHERE total > 100` if `total` is a `SELECT` alias. SQLite is looser and often accepts it, so a query that works in the lab can fail on the server. Write the expression out in `WHERE`, or wrap the query in a subquery.

### NULL in a WHERE clause

`NULL` means "no value," and any comparison with it gives neither true nor false but unknown, which `WHERE` treats as false. So `WHERE durability = NULL` matches nothing, ever. Use `WHERE durability IS NULL`. And `WHERE durability < 50` silently skips every stackable item whose durability is NULL. That is usually what you want, and occasionally a bug.

## 2. Worked example: the double-counted gold

### The hook

Ask the official Guild Wars 2 API what is for sale on the Trading Post for one item, and you get a list of price levels. Each entry has a `unit_price`, a `quantity` and a field called `listings`. One entry can stand for many players' orders merged together: `listings` counts the orders at that price and `quantity` counts the items in them.

So "how many are for sale?" has three answers depending on what you add up. Counting entries gives the number of price levels. Summing `listings` gives the number of orders. Summing `quantity` gives the number of items. Each is correct for a different question. The skill this week is knowing, before you write `COUNT` or `SUM`, what one row of your working set means. That is called the **grain** of the table. Joins change the grain, and when they do it silently, you get the most common wrong number in game analytics.

### The model

A **join** combines rows from two tables where a condition holds, usually "this foreign key equals that primary key":

```sql
SELECT c.name, i.item_id
FROM characters c
JOIN items i ON i.owner_id = c.character_id;
```

For each character, the result has one row per matching item. If a character matches `m` items, the character's row appears `m` times. Join a third table and each of those rows is repeated again for every match there. Name it:

- `m₁(p)` is the number of rows in the first child table matching parent row `p`.
- `m₂(p)` is the number in the second child table.

Then for an inner join of the parent with both children:

```
rows produced for p          = m₁(p) × m₂(p)          (0 if either is 0)
SUM(parent.x) reported       = Σ  x(p) × m₁(p) × m₂(p)
COUNT(child1 rows) reported  = Σ  m₁(p) × m₂(p)
```

The parent's value `x` is counted once per joined row, so it is inflated by the product of the match counts. The first child's rows are counted once per match in the second child. **A join multiplies; an aggregate after it adds up the multiplied rows.** This is the SQL version of a nested loop from CS102 week 4: the inner body runs `m₁ × m₂` times.

### Numbers you can check

A designer wants one table: per class, total gold, number of item stacks, number of quests completed. The obvious query:

```sql
SELECT c.class, SUM(c.gold) AS total_gold,
       COUNT(i.item_id) AS item_rows, COUNT(q.quest_id) AS quest_rows
FROM characters c
JOIN items i             ON i.owner_id = c.character_id
JOIN quest_completions q ON q.character_id = c.character_id
GROUP BY c.class;
```

Compute each character's contribution with the model:

| Character | Class | gold | m₁ items | m₂ quests | Joined rows | Gold counted | Items counted | Quests counted |
|---|---|---|---|---|---|---|---|---|
| Aria | warrior | 500 | 3 | 2 | 6 | 3,000 | 6 | 6 |
| Bram | mage | 300 | 2 | 4 | 8 | 2,400 | 8 | 8 |
| Cyra | rogue | 200 | 0 | 1 | 0 | 0 | 0 | 0 |
| Dax | mage | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

The query returns warrior 3,000 gold, 6 items, 6 quests, and mage 2,400 gold, 8 items, 8 quests. The rogue class vanishes. The truth:

| Class | True gold | True item stacks | True quests | Query said |
|---|---|---|---|---|
| mage | 300 | 3 | 4 | 2,400 / 8 / 8 |
| rogue | 200 | 0 | 1 | (missing) |
| warrior | 500 | 3 | 2 | 3,000 / 6 / 6 |

Every number is wrong, and wrong in a way that looks plausible. World gold appears to be 5,400 instead of 1,000. Notice also that item and quest counts come out equal for each class, which is a telltale sign: both are counting the same joined rows.

Scale makes it worse. In Lab 03's generated world (1,200 characters, 27,684 item stacks, 7,863 quest completions), the same query produces 205,116 joined rows and reports 273,095,099 gold for warriors, whose true total is 1,135,335. That is 240 times too high. In a live MMO with 200,000 characters, 150 stacks and 40 quests each, the join builds `200,000 × 150 × 40 = 1.2 billion` rows to answer a question about 200,000 characters.

### The fix: aggregate, then join

Reduce each child table to one row per character first, then join those one-row-per-key results. Joining one row to one row cannot multiply anything.

```sql
SELECT c.class,
       SUM(c.gold)              AS total_gold,
       SUM(COALESCE(i.n, 0))    AS item_rows,
       SUM(COALESCE(q.n, 0))    AS quest_rows
FROM characters c
LEFT JOIN (SELECT owner_id, COUNT(*) AS n FROM items GROUP BY owner_id) i
       ON i.owner_id = c.character_id
LEFT JOIN (SELECT character_id, COUNT(*) AS n FROM quest_completions GROUP BY character_id) q
       ON q.character_id = c.character_id
GROUP BY c.class
ORDER BY c.class;
```

Result: mage 300, 3, 4; rogue 200, 0, 1; warrior 500, 3, 2. Correct.

Three changes did the work:

- The subqueries in parentheses (**derived tables**) have grain "one row per character," so every `m` is now 0 or 1.
- `LEFT JOIN` keeps characters with no match, filling the missing side with NULL. An inner join drops them, which is how the rogues disappeared.
- `COALESCE(x, 0)` turns those NULLs into zeros, so the sums are right for characters with no items or quests.

The join now touches `C` rows from each side, 1,200 in the lab instead of 205,116.

### Seeing it move

Open the interactive. The left view shows the four characters as rows, with their item and quest rows fanned out to the right. Next to each character, its joined rows are drawn as a grid, `m₁ × m₂` per character, with the gold value stamped into every copy. The right view is a bar chart per class: true gold as an outline, reported gold as a filled bar. Drag Bram's quest count from 4 to 10 and his joined block grows from 8 to 20 rows while mage gold climbs to 6,000. Set Cyra's item count to 1 and the rogue bar appears. Then toggle "aggregate first" and every block collapses to one row per character and the filled bars snap to the outlines.

### Cross-game recognition

The grain question appears in every game data format. Rewrite each as "rows × multiplier."

**Guild Wars 2 Trading Post (API v2, current).** Grain of `/v2/commerce/listings`: one row per price level per side (buy or sell). Items for sale `= SUM(quantity)`, orders `= SUM(listings)`, price levels `= COUNT(*)`. If you joined listings to the item's recipe ingredients (one row per ingredient) to value them, every listing would repeat once per ingredient, the same fan-out as above.

**EVE Online assets (ESI, 2025 schema).** Grain of the assets endpoint: one row per item stack or individual item, with `quantity` and `is_singleton`. "How many of type 587 do I own?" is `SUM(quantity) WHERE type_id = 587`. `COUNT(*)` gives the number of stacks, which is only the same when every copy is a singleton. And because an asset's `location_id` can point at another asset (a module in a ship), joining assets to their containers is a one-to-many join that repeats the container's values once per contained item.

**Minecraft inventories (Java Edition).** A slot holds up to 64 of most items. An inventory with 20 slots of cobblestone at 64 each holds 1,280 cobblestone. Counting slots answers "how much space is used," summing counts answers "how much do I have." Same data, two grains, two questions.

In all three, the fix is the same habit: say out loud what one row means before you aggregate, and after every join, ask whether that meaning changed.

### Eyes-open design judgment

- **Check the row count after every join.** Before running a big aggregate, run `SELECT COUNT(*)` on the `FROM ... JOIN ...` part alone. If it is bigger than the largest table you expected to aggregate over, you have fan-out.
- **Pre-aggregation is the default fix.** It is correct, and it is usually faster, because the joins run on small per-key summaries.
- **`COUNT(DISTINCT ...)` is a partial fix.** It rescues counts of child rows (count distinct `item_id`). It does not rescue sums of parent values. `SUM(DISTINCT gold)` treats two different characters who both have 300 gold as one, so it undercounts. In the four-character world, `SUM(DISTINCT c.gold)` over characters joined to items gives 800, which is wrong for a different reason (Cyra has no items and drops out of the inner join).
- **Inner or left is a question about missing data.** An inner join answers "among characters who have items." A left join answers "among all characters." Dashboards usually mean the second, and silently reporting the first hides exactly the players you care about, the ones with nothing.
- **When a total is needed every minute, store it.** A materialized summary table, refreshed on a schedule, is deliberate denormalization (week 2). Week 12 does this for dashboards.

### Check yourself on the worked example

1. Bram completes 3 more quests (7 total). What does the naive query now report for mage gold, and what is the truth?
2. Using the model, how many joined rows does the naive query produce if every one of 1,000 characters has 20 items and 10 quests? What inflation factor does it apply to gold?
3. Rewrite the naive query to use `COUNT(DISTINCT ...)` for items and quests. Which of its three output columns are now right, and which is still wrong?

<details>
<summary>Answers</summary>

1. Bram's joined rows become `2 × 7 = 14`, so mage gold is `300 × 14 = 4,200` (Dax still contributes nothing). The truth stays 300.
2. `1,000 × 20 × 10 = 200,000` joined rows. Each character's gold is counted `20 × 10 = 200` times.
3. `COUNT(DISTINCT i.item_id)` and `COUNT(DISTINCT q.quest_id)` give correct counts for characters who have both items and quests. Gold is still inflated by `m₁ × m₂`, and the inner joins still drop characters missing either side, so rogues are still missing and Dax's item is still uncounted. (Also note `COUNT(DISTINCT q.quest_id)` counts distinct quest ids across the whole class, so two mages who completed quest 10 count it once. Use `(character_id, quest_id)` pairs or pre-aggregate.)

</details>

## 3. Joins in detail

**Inner join** (`JOIN ... ON`) keeps pairs where the condition holds. Characters with no items disappear.

**Left join** (`LEFT JOIN ... ON`) keeps every row of the left table. Where no right row matches, the right columns are NULL.

```sql
SELECT c.name, COUNT(i.item_id) AS stacks
FROM characters c
LEFT JOIN items i ON i.owner_id = c.character_id
GROUP BY c.character_id, c.name;
```

Aria 3, Bram 2, Cyra 0, Dax 1. Note `COUNT(i.item_id)`, not `COUNT(*)`. For Cyra the left join produces one row with NULL item columns. `COUNT(*)` counts that row and says 1. `COUNT(i.item_id)` skips NULLs and says 0.

**Anti-join**: "rows with no match." Two equivalent forms:

```sql
SELECT c.name FROM characters c
LEFT JOIN items i ON i.owner_id = c.character_id
WHERE i.item_id IS NULL;

SELECT c.name FROM characters c
WHERE NOT EXISTS (SELECT 1 FROM items i WHERE i.owner_id = c.character_id);
```

Both return Cyra. Support teams run this kind of query constantly ("characters who logged in this week but hold no items" usually means a bug or a stripped account).

**Forgetting the ON clause.** `SELECT * FROM characters, items` with no condition pairs every character with every item: `4 × 6 = 24` rows. This is a **cross join**. It has legitimate uses (every class paired with every zone for a report skeleton), but written by accident on 200,000 characters and 30 million items it asks for 6 trillion rows.

**Self-join.** Week 2's `container_id` points from `items` back into `items`. Joining `items AS child` to `items AS bag ON child.container_id = bag.item_id` lists each item with its container. For containers inside containers to any depth, SQL has recursive queries (`WITH RECURSIVE`, described in the PostgreSQL documentation under "WITH Queries"). You will not need them in Lab 03.

## 4. Aggregates and groups

An **aggregate function** reduces many rows to one value. The five you will use weekly:

| Function | Returns | NULLs |
|---|---|---|
| `COUNT(*)` | number of rows | counts them |
| `COUNT(col)` | number of non-NULL values | skips them |
| `SUM(col)` | total | skips them; NULL if all are NULL |
| `AVG(col)` | mean | skips them |
| `MIN(col)`, `MAX(col)` | smallest, largest | skip them |

`GROUP BY` splits the working set into groups with equal values and runs the aggregates once per group:

```sql
SELECT t.rarity, SUM(i.quantity) AS total_qty
FROM items i JOIN item_types t ON t.type_id = i.type_id
GROUP BY t.rarity;
```

Common 97 (12 potions, 30 ore, 5 potions, 50 ore), rare 2 (two swords). Joining `items` to `item_types` does not fan out, because each item has exactly one type: `m = 1` for every item row. A join from the many side to the one side keeps the grain. The danger is joining from one parent to two or more "many" tables at once.

`HAVING` filters groups:

```sql
SELECT class, AVG(level) AS avg_level, COUNT(*) AS n
FROM characters
GROUP BY class
HAVING COUNT(*) >= 2;
```

Only mage has two characters: average level `(9 + 4) / 2 = 6.5`.

A computed aggregate combining two tables, the vendor value of each inventory:

```sql
SELECT c.name, SUM(i.quantity * t.vendor_price) AS value
FROM characters c
JOIN items i      ON i.owner_id = c.character_id
JOIN item_types t ON t.type_id = i.type_id
GROUP BY c.character_id, c.name
ORDER BY value DESC;
```

Aria `12 × 5 + 1 × 400 + 30 × 1 = 490`, Dax 400, Bram `5 × 5 + 50 × 1 = 75`. Economy designers run exactly this query, across the whole world, to see how much gold is locked in inventories and could flow to vendors (see MMO304 week 3 on sinks).

### Where SQLite and PostgreSQL differ

- **Bare columns.** SQLite accepts `SELECT class, name, MAX(gold) FROM characters GROUP BY class`, where `name` is neither grouped nor aggregated. With exactly one `MIN` or `MAX` it takes `name` from the row holding the maximum; otherwise from an arbitrary row in the group. PostgreSQL rejects the query unless the column is grouped, aggregated, or functionally dependent on a grouped primary key. So `GROUP BY c.character_id` lets you select `c.name` in PostgreSQL; `GROUP BY c.class` does not.
- **Integer division.** In both, `gold / level` with two integers truncates: `500 / 12 = 41`. Write `gold * 1.0 / level` or cast to get 41.67.
- **AVG type.** PostgreSQL returns an exact `numeric` for `AVG` of integers; SQLite returns a floating-point value. Round explicitly with `ROUND(AVG(level), 1)` when you compare results across the two.
- **String comparison.** PostgreSQL compares text case-sensitively by default, so `'Aria' = 'aria'` is false. SQLite's `=` is also case-sensitive, but its `LIKE` is case-insensitive for ASCII letters, while PostgreSQL's `LIKE` is case-sensitive (use `ILIKE`).

## In-class activity (25 minutes)

In pairs, with the four-character world loaded:

1. Each partner writes, on paper, the result of this query before running it: `SELECT c.name, COUNT(*) FROM characters c LEFT JOIN items i ON i.owner_id = c.character_id LEFT JOIN quest_completions q ON q.character_id = c.character_id GROUP BY c.character_id, c.name`. Use the model: for left joins, a zero match count behaves as 1. Compare predictions, then run it.
2. Write a query for "average gold per character, by class, counting characters with no items." Check it by hand.
3. Write the query a designer would need for "the three item types held by the most distinct characters." State the grain of your working set after each join.
4. Invent a fourth child table (for example `achievements`, 5 per character) and predict how the naive three-join query from section 2 would change if you added it. Then write the correct version.

Expected output: predicted and actual counts for step 1 (Aria 6, Bram 8, Cyra 1, Dax 1), two correct queries with hand checks, and the prediction for step 4 (every joined block multiplied by 5, so world gold reported as 27,000).

## Common misconceptions

- **"A join combines two tables side by side."** It combines matching rows, and the number of result rows is the sum of the products of match counts. It can be much larger or much smaller than either table.
- **"`COUNT(*)` and `COUNT(column)` are the same."** They differ exactly when the column can be NULL, which is always the case on the right side of a left join.
- **"`DISTINCT` fixes double counting."** It fixes counts of rows that have a unique id. It breaks sums of values that can legitimately repeat, like gold.
- **"`WHERE` and `HAVING` are interchangeable."** `WHERE` filters rows before grouping; `HAVING` filters groups after. `WHERE level > 10` and `HAVING AVG(level) > 10` answer different questions.

## Check yourself

1. Predict the output of `SELECT COUNT(*), COUNT(i.item_id), SUM(i.quantity) FROM characters c LEFT JOIN items i ON i.owner_id = c.character_id`.
2. A table `logins` has one row per login, with about 30 logins per character per month. An analyst joins `characters` to `logins` and to `items` (150 stacks each) and sums gold. By what factor is gold inflated for a typical character?
3. Write a query that lists each class with the name of its richest character. Why is the SQLite bare-column shortcut risky here, and what would you write for PostgreSQL?
4. In the Guild Wars 2 listings format, what is the grain, and which expression answers "total coins needed to buy every item currently for sale"?
5. Explain why joining `items` to `item_types` never inflates `SUM(i.quantity)`, while joining `characters` to `items` does inflate `SUM(c.gold)`.

<details>
<summary>Answers</summary>

1. The left join produces Aria 3, Bram 2, Cyra 1 (NULLs), Dax 1: `COUNT(*) = 7`, `COUNT(i.item_id) = 6`, `SUM(i.quantity) = 12 + 1 + 30 + 5 + 50 + 1 = 99`.
2. `30 × 150 = 4,500` times.
3. One portable form joins to a per-class maximum: `SELECT c.class, c.name, c.gold FROM characters c JOIN (SELECT class, MAX(gold) AS g FROM characters GROUP BY class) m ON m.class = c.class AND m.g = c.gold`. The SQLite shortcut `SELECT class, name, MAX(gold) ... GROUP BY class` works only because SQLite has a special rule for a single `MAX`, picks arbitrarily on ties, and fails outright in PostgreSQL. The portable form returns both characters on a tie, which is honest.
4. One row per price level per side. For sells, the total cost is `SUM(unit_price × quantity)` over the sell entries.
5. Each item row has exactly one type, so every item appears once in the join (`m = 1`) and the item's quantity is counted once. Each character can have many items, so the character's gold appears once per item (`m = number of stacks`).

</details>

## Lab / assignment hook

[Lab 03, eight questions about a generated world](../labs/lab03.md). Build a 1,200-character world with `build_db.py`, then write eight queries (filter, top-N, join and group, anti-join, the fan-out trap, vendor value, `HAVING`) that the checker compares against answers computed in plain Python. For q06, you first record what the naive join reports, then fix it. Deliverable: the eight `.sql` files and a short report with the naive and corrected q06 numbers.

## Sources

- Guild Wars 2 Wiki, "API:2/commerce/listings" (API v2, as of September 2026). Buy and sell arrays of price levels with `listings` (number of orders at that price), `unit_price` and `quantity`.
- EVE Online ESI OpenAPI specification, `GET /characters/{character_id}/assets` (compatibility date 2025-08-26). `quantity`, `is_singleton`, `location_id` and `location_type` including `item`.
- Minecraft Wiki, "Stack" (Java Edition, as of September 2026). Most items stack to 64.
- SQLite documentation, "SELECT", section "Bare columns in an aggregate query" (sqlite.org/lang_select.html). A bare column takes its value from an arbitrary input row, or from the row holding the single `min()` or `max()`.
- PostgreSQL 18 documentation, "SELECT" (the `GROUP BY` clause and functional dependency on a primary key) and Tutorial sections "Joins Between Tables" and "Aggregate Functions".
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 2.

## Interactive spec: examples/w03-join-fan-out.html

**The one insight:** a join repeats each parent row once per combination of matching child rows, so an aggregate after a two-child join counts the parent's gold `m₁ × m₂` times. Aggregating each child first collapses every block to one row and the totals snap to the truth.

**Layout (two linked views, stacked on mobile, side by side at ≥ 900px):**

- View A, "the joined rows": four character cards down the left (name, class, gold). To the right of each, a block of joined rows drawn as a grid of `m₁` columns by `m₂` rows of small cells, each cell stamped with the character's gold value. Zero-match characters show an empty, dashed outline labelled "dropped (inner join)" or, in left-join mode, a single cell with a NULL marker. A running counter at the top: "joined rows: N".
- View B, "what the dashboard says": grouped bar chart per class (mage, rogue, warrior). For each class, an outline bar at the true gold total and a filled bar at the reported total. A missing class is drawn as an empty slot labelled "missing". A second small chart shows item and quest counts, true against reported, in the same style. Print the numbers on every bar.

**Controls:**

- Per character, two steppers (0 to 12): items `m₁` and quests `m₂`. Defaults: Aria 3 and 2, Bram 2 and 4, Cyra 0 and 1, Dax 1 and 0.
- Per character, a gold input (0 to 2,000), defaults 500, 300, 200, 0.
- Join type toggle: inner (default) or left.
- Toggle "aggregate first" (default off). When on, view A redraws each block as a single row with columns `n_items`, `n_quests`, and view B's filled bars equal the outlines.
- Button "show the SQL" that reveals the query that corresponds to the current mode.

**Formulas (exact):**

```
inner, naive:   rows(p) = m1(p) × m2(p)
left, naive:    rows(p) = max(m1(p), 1) × max(m2(p), 1)
reported_gold(class) = Σ_{p in class} gold(p) × rows(p)
reported_items(class) = Σ count of non-NULL item cells = Σ m1(p) × (inner ? m2(p) : max(m2(p),1))
reported_quests(class) = Σ m2(p) × (inner ? m1(p) : max(m1(p),1))
aggregate first: rows(p) = 1; gold, items, quests are the true values; class present if it has any character (left join)
```

**Test values (must match):**

- Defaults, inner, naive: joined rows 14; warrior gold 3,000 / items 6 / quests 6; mage 2,400 / 8 / 8; rogue missing. World gold reported 5,400, true 1,000.
- Defaults, left, naive: joined rows Aria 6, Bram 8, Cyra 1, Dax 1 = 16; mage gold 2,400 + 0 = 2,400; rogue gold 200, items 0, quests 1; mage items `2 × 4 + 1 × 1 = 9`, mage quests `4 × 2 + 0 = 8`.
- Aggregate first: mage 300 / 3 / 4, rogue 200 / 0 / 1, warrior 500 / 3 / 2; joined rows 4.
- Bram quests set to 7, inner, naive: mage gold 4,200.
- Cyra items set to 1, inner, naive: rogue appears with gold 200, items 1, quests 1.

**First screen:** defaults, inner join, naive mode, with the filled warrior and mage bars towering over their outlines, the rogue slot labelled "missing", and a caption: "The query is correct SQL. The numbers are wrong. Count the cells."

**Accessibility:** steppers and toggles keyboard operable with visible focus; the numeric summary (joined rows and per-class reported vs true) in an `aria-live="polite"` region; respects `prefers-reduced-motion` (no cell animation, instant redraw) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline, with reported values in the damage red and true values in the survival ochre. No game art or logos.
