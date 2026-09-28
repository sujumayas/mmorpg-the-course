# DB201 · Week 02 — Relational Modeling: Characters, Inventories, Items

**Why this matters:** The shape you give your data on day one decides which questions you can ask cheaply for the life of the game. Store every inventory as one opaque blob and "how many of this sword exist?" becomes a job that reads every character in the world. Store it as rows and that question takes milliseconds, but loading one character gets harder. This week you learn to choose on purpose.

**You will be able to:**
- Split game items into item types and item instances, and decide which attributes belong to which.
- Design a relational schema for characters, inventories, items and item affixes with primary keys, foreign keys and constraints that enforce game rules.
- Estimate row counts, bytes per row and storage for a schema, and compare the cost of common operations for a blob design and a row design.
- Recognize the type/instance split in three shipped games' data formats and rewrite each into the same tables.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 2, the section "Relational Model Versus Document Model" (through "Which data model leads to simpler application code?"). PostgreSQL documentation, chapter "Data Definition", section "Constraints" (read primary keys, foreign keys, unique and check constraints).

**Prerequisites from earlier courses:** Classes, objects and their fields, [CS102 week 1](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w01-classes-objects-encapsulation.md). Hash maps keyed by id, [CS102 week 5](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md). Type objects and item tables in CSV, [CS102 week 13](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md). From this course, the four kinds of game data and the cost of a save, [DB201 week 1](w01-why-persistence-is-hard-in-games.md).

**Interactive:** [Blob or rows?](../examples/w02-blob-vs-rows.html). Keep it open during section 2.

---

## 1. Tables, rows and keys

A **relational database** stores data in tables. A **table** has named, typed columns, and each **row** is one record. The **schema** is the set of table definitions: names, columns, types and rules. Here is a first table for characters, in SQL that runs in both SQLite and PostgreSQL:

```sql
CREATE TABLE characters (
  character_id INTEGER PRIMARY KEY,
  name         TEXT    NOT NULL UNIQUE,
  class        TEXT    NOT NULL,
  level        INTEGER NOT NULL DEFAULT 1,
  gold         INTEGER NOT NULL DEFAULT 0 CHECK (gold >= 0)
);
```

Each line after the column name is a promise the database keeps for you.

- A **primary key** is the column (or columns) that identifies a row. No two rows share it and it is never empty. `character_id` is the character's permanent identity, even if the player renames the character.
- `NOT NULL` means the column must have a value. `NULL` is SQL's marker for "no value" (not zero, not an empty string).
- `UNIQUE` means no two rows may share the value. Two characters on one server cannot both be named Aria.
- `CHECK` states a rule the row must satisfy. Gold may not go negative. A bug that tries to set it to -50 fails loudly instead of quietly creating debt.
- `DEFAULT` fills a value when the insert leaves the column out.

A **foreign key** is a column that refers to another table's primary key. It is how tables point at each other:

```sql
CREATE TABLE items (
  item_id  INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL REFERENCES characters(character_id),
  ...
);
```

With the foreign key in place, the database rejects an item whose owner does not exist, and refuses to delete a character who still owns items (unless you tell it what to do with them). Think of these constraints as the game's rules written where no code path can skip them. Your server code has bugs. The constraints still hold.

In CS102 you kept a dictionary from item id to item object. A table with a primary key is that dictionary, stored on disk, shared by every server process, and guarded by rules.

## 2. Worked example: blob or rows?

### The hook

In Minecraft (Java Edition), 64 blocks of dirt fit in one inventory slot. Ender pearls stop at 16. But two iron swords never share a slot, even when both are brand new. The rule is on the wiki: items with durability do not stack.

Players learn that as a quirk. It is a data-modeling rule. Sixty-four dirt blocks are indistinguishable, so the game stores "dirt, 64" and is done. A sword carries its own state (how worn it is), so each sword is a separate thing with its own record. Every inventory system you will build faces the same split, and the choice of how to store it has consequences measured in gigabytes.

### The model, part 1: types and instances

Split every item into two tables.

- `item_types` has **one row per kind of item**: its name, rarity, how many fit in a stack, what a vendor pays. Designers change these. A game might have 8,000 of them. This is the content data of week 1, and it is the same "type object" you loaded from CSV in CS102 week 13.
- `items` has **one row per stack or per individual item a player holds**: which type it is, who owns it, where it sits, how many are in the stack, and any state that belongs to this copy alone, such as durability.

```sql
CREATE TABLE item_types (
  type_id      INTEGER PRIMARY KEY,
  name         TEXT    NOT NULL UNIQUE,
  rarity       TEXT    NOT NULL,
  max_stack    INTEGER NOT NULL CHECK (max_stack >= 1),
  vendor_price INTEGER NOT NULL CHECK (vendor_price >= 0)
);

CREATE TABLE items (
  item_id    INTEGER PRIMARY KEY,
  type_id    INTEGER NOT NULL REFERENCES item_types(type_id),
  owner_id   INTEGER NOT NULL REFERENCES characters(character_id),
  bag        INTEGER NOT NULL,          -- 0 = backpack, 1-4 = bags, 100 = bank
  slot       INTEGER NOT NULL,
  quantity   INTEGER NOT NULL CHECK (quantity >= 1),
  durability INTEGER,                   -- NULL for things that do not wear
  UNIQUE (owner_id, bag, slot)          -- one stack per slot
);
```

The stacking rule falls out of the split. **Two copies can share a row (stack) only if every instance column other than `quantity` would be identical.** Dirt has no instance columns, so it stacks. A sword has durability, so each sword needs its own row. When a later patch adds a per-copy attribute (an enchantment, a "crafted by" name), items with that attribute stop stacking, whether the designer meant it or not.

### The model, part 2: where to put the inventory

Now the question in the title. There are two ways to store a character's inventory.

- **Blob:** one column on the character row holding the whole inventory as a JSON document, like a save file. Loading is one read. The database sees a single opaque value.
- **Rows:** the `items` table above, one row per stack, linked to the character by `owner_id`.

Name the quantities:

- `C` is the number of characters.
- `I` is the average number of item rows (stacks) per character.
- `j` is the JSON size of one item in the blob, in bytes.
- `r` is the stored size of one item row, in bytes.
- `K` is the number of item types.

Then, for the operations a game server and its designers actually run:

```
storage, blob          = C × I × j
storage, rows          = C × I × r              (plus indexes)
load one character     blob: 1 row, I × j bytes      rows: I rows, maybe I different pages
move one item          blob: rewrite 2 blobs, 2 × I × j bytes    rows: update 1 row, ~r bytes
count one type, world  blob: read and parse all C × I × j bytes  rows + index: ~C × I / K rows
```

The pattern is the one to remember. **A blob is cheap to read whole and expensive to read across or change in part. Rows are cheap to read across and change in part, and cost more to reassemble.**

### Numbers you can check

Take an invented MMO with `C = 200,000` characters, `I = 150` stacks each, `K = 8,000` item types, and a JSON item of `j = 70` bytes (five fields such as `{"item_id":1234567,"type_id":4521,"bag":2,"slot":17,"qty":20}` is about 60 characters, plus commas and brackets).

**Row size in PostgreSQL.** The data columns are two 8-byte ids (`bigint` in PostgreSQL), two 4-byte integers and two 2-byte small integers: 28 bytes. (`durability` is NULL for most stacks, and a NULL costs only one bit in the row header.) Every row also carries a header of 23 bytes, padded to 24. Rows are padded to a multiple of 8, so 52 bytes becomes 56. Each row also needs a 4-byte pointer in its page. Total `r = 60` bytes.

**Rows per page.** PostgreSQL stores tables in 8,192-byte pages with a 24-byte page header, leaving 8,168 bytes. `8,168 / 60 = 136` rows per page.

| Quantity | Blob design | Row design |
|---|---|---|
| Item records | 200,000 blobs holding 30,000,000 items | 30,000,000 rows |
| Size per character | `150 × 70 = 10,500` bytes | `150 × 60 = 9,000` bytes |
| Table size | `200,000 × 10,500 = 2.1 GB` (before compression) | `30,000,000 / 136 = 220,589` pages `× 8,192 = 1.81 GB` |
| Load one character | 1 lookup, 10.5 kB | 150 rows; up to 150 page reads if scattered |
| Move one item between characters | rewrite 2 blobs, 21,000 bytes | update 1 row, about 60 bytes |
| "How many of type X exist?" | read and parse 2.1 GB | about `30,000,000 / 8,000 = 3,750` rows via an index, at most 3,750 pages (30.7 MB) |

Verify one line by hand: the move costs `2 × 150 × 70 = 21,000` bytes for the blob and about 60 for the row. That is a factor of 350, and it grows with inventory size. A character with 600 stacks makes every trade rewrite 84 kB.

Notice also where the blob wins. Loading a character at login is one lookup. The row design must gather 150 rows, and if those items were picked up over months they may sit on 150 different pages. An index on `owner_id` finds them quickly, but reading 150 pages costs more than reading one blob. [Week 4](w04-sql-ii-indexes-and-query-plans.md) shows how to measure that and what to do about it.

One PostgreSQL detail changes the blob numbers in your favor and one against. Values larger than about 2 kB (the `TOAST_TUPLE_THRESHOLD`) are compressed and moved out of the main row into a side table. The 10.5 kB blob is stored compressed, which shrinks storage. But any change to one item still rewrites the whole value.

In Lab 02 you build both designs in SQLite with 2,000 characters and 150 items each. On the lecture's machine, counting one type across the world took 0.35 ms with an index on `type_id` and 114 ms by parsing blobs with `json_each`, a factor of about 330. The blob file was also larger (24.5 MB against 14.8 MB for rows plus index), because every JSON item repeats its key names.

### Seeing it move

Open the interactive. The left view shows storage: a grid of pages, with blobs drawn as long bars and rows as small cells packed 136 to a page. The right view is a bar chart of bytes touched per operation, blob against rows, on a log scale. Pick an operation and the pages it touches light up on the left. Drag `I` from 20 to 600 and watch "move one item" for the blob climb in step with inventory size while the row bar stays flat. Then switch to "load one character". The data bars are close, 10,500 bytes of blob against 9,000 bytes of rows, but a third bar shows the worst case for rows: 150 scattered page reads, 1.23 MB. That page count, not the byte count, is why the blob wins at login.

### Cross-game recognition

Three shipped games, three formats, one model. Rewrite each into `item_types` plus `items`.

**Minecraft (Java Edition).** Most items stack to 64, many projectiles to 16, and items with durability to 1. In our tables: `max_stack` on the type is 64, 16 or 1, and durability is an instance column. Recent Java versions also let a data component raise a stack limit up to 99. That is `max_stack` changed per instance, which our schema would need a new instance column to express.

**Guild Wars 2 (official API v2, current).** The character inventory endpoint returns a list of bags. Each bag has an item id and a size, and an array of slots. Each slot is either `null` (empty) or an object with the item `id`, a `count` from 1 to 250, and optional per-copy fields: `upgrades`, `infusions`, `skin`, `stats`, `binding` and `bound_to`. In our tables: `id` is `type_id`, `count` is `quantity`, and the optional fields are instance state. `upgrades` and `infusions` are lists, so they become a child table (next section). An empty slot is simply no row. Bags being items themselves is a hint for the container design in section 3.

**EVE Online (ESI, the official web API, 2025 schema).** The character assets endpoint returns one record per asset with `item_id`, `type_id`, `quantity`, `is_singleton`, `location_id`, `location_type` and `location_flag`. That is our `items` table almost column for column. `type_id` points to the static type data. `is_singleton` sits next to `quantity` and, as its name says, separates one-of-a-kind items from stacks. And `location_type` can be `item`, which means the asset sits inside another asset: a module inside a ship inside a station hangar. Location is a foreign key that can point back into the same table.

The same two tables fit all three. Game data formats differ in names and nesting, and underneath sits the same split between what kind of thing and this particular thing.

### Eyes-open design judgment

- **Rows are the default for anything with value.** Items, currency and anything players trade need cross-player queries (economy dashboards, dupe investigations) and small atomic changes (trades, week 5). The blob design makes both expensive.
- **Blobs are fine for state nobody queries across players.** UI layout, keybindings, chat channel settings and the last camera angle are read at login, written rarely, and never summed across the world. A JSON column is simpler and faster for those. PostgreSQL's `jsonb` type sits between the two: it stores a parsed document and can index keys inside it, which rescues some queries but not the cost of rewriting the document on every change.
- **Every instance column is a stacking decision.** Adding "crafted by" to items means crafted potions stop stacking. Decide that with the designers before the migration, not after the bug reports.
- **Row count is the bill.** `C × I` grows with both player count and inventory size. Generous bank space is a design gift with a storage and index cost you can now compute.
- **Measure the blob's one advantage before giving it up.** If login time matters more than anything else, you can keep rows as the truth and cache an assembled character in Redis (week 8).

### Check yourself on the worked example

1. With the numbers above, a patch doubles bank space and average stacks per character rise from 150 to 250. What are the new row count and approximate table size for the row design?
2. For the blob design, how many bytes does one trade of a single item rewrite after that patch?
3. A designer asks for "top 10 most common item types in the world" every morning. Which operation in the table is this closest to, and which design suits it?

<details>
<summary>Answers</summary>

1. `200,000 × 250 = 50,000,000` rows. `50,000,000 / 136 = 367,648` pages, `× 8,192 ≈ 3.01 GB`.
2. `2 × 250 × 70 = 35,000` bytes.
3. It is a world-wide count, grouped by type. Rows answer it with one pass over the `items` table (or its `type_id` index); blobs must parse every inventory.

</details>

## 3. Relationships

Tables relate to each other in three patterns. Each has one standard shape.

**One-to-many.** One character owns many items; each item has one owner. Put a foreign key on the "many" side: `items.owner_id`. Never put a list of item ids on the character row.

**Many-to-many.** A character can belong to several guilds over time and a guild has many members. Characters earn many achievements and each achievement is earned by many characters. Neither side can hold one foreign key, so add a **join table** whose rows are the pairs:

```sql
CREATE TABLE guild_members (
  guild_id     INTEGER NOT NULL REFERENCES guilds(guild_id),
  character_id INTEGER NOT NULL REFERENCES characters(character_id),
  rank         TEXT    NOT NULL DEFAULT 'member',
  joined_at    TEXT    NOT NULL,
  PRIMARY KEY (guild_id, character_id)
);
```

The join table also gives facts about the pair a home. `rank` and `joined_at` belong neither to the guild nor to the character. They belong to the membership.

**One-to-one.** A character has exactly one appearance record (hair, face, colors). You can keep those columns on `characters` or move them into a separate table keyed by `character_id`. Split them off when they are large or rarely read, so the common character row stays small.

**Self-reference.** EVE's "asset inside an asset" and Guild Wars 2's bags that are also items both call for an item that contains other items. Give `items` a nullable `container_id` that references `items(item_id)`. A backpack item has children; a potion in it has the backpack as its container. This is a tree stored in a table ([CS102 week 7](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w07-trees-scene-graphs-and-skill-trees.md)), and SQL can walk it with a recursive query (`WITH RECURSIVE`), which [week 3](w03-sql-i-select-join-aggregate.md) points you to but does not need in its lab.

### Lists become child tables

Guild Wars 2 slots carry `upgrades` and `infusions`, which are lists. A first attempt stores them as a comma-separated string in one column: `'24615,24615,49432'`. Now answer "which items carry upgrade 49432?" You must search inside strings, and nothing stops a typo like `'24615,,4943'`.

The relational answer is a child table with one row per element:

```sql
CREATE TABLE item_affixes (
  item_id INTEGER NOT NULL REFERENCES items(item_id),
  stat    TEXT    NOT NULL,
  value   INTEGER NOT NULL,
  PRIMARY KEY (item_id, stat)
);
```

A Diablo-style sword with "+14 fire damage" and "+6% attack speed" has one `items` row and two `item_affixes` rows. The primary key `(item_id, stat)` forbids the same stat twice on one item, which is a game rule enforced by the database.

## 4. Normalization: one fact in one place

**Normalization** is the practice of storing each fact exactly once. The rule of thumb: if you can say "this column depends on something other than this row's key," it probably belongs in another table.

Suppose you put the item's name and vendor price on every `items` row, to save a lookup. Each of 30 million rows now carries about 40 more bytes. At 100 bytes per row, a page holds 81 rows instead of 136, and the table grows from 1.81 GB to about 3.03 GB. That is the smaller problem. The bigger problems are three **anomalies**:

- **Update anomaly.** A designer renames "Emberfang Sword." If 250,000 copies exist, that is 250,000 row updates, and a crash halfway leaves two names in the world. In the normalized design it is one row in `item_types`.
- **Insert anomaly.** You cannot record a new item type's price until someone holds a copy, because the price only lives on held copies.
- **Delete anomaly.** When the last copy of a rare item is destroyed, its name and price vanish with it.

Denormalization, copying a fact on purpose, is sometimes right. A leaderboard table that copies each character's name and class can be read without joins, thousands of times a minute. The rule is that you choose it deliberately, you name the one table that holds the truth, and you know how the copies get refreshed.

## 5. Constraints are game rules

Here is the whole schema from this lecture as game rules:

| Game rule | Constraint |
|---|---|
| Every character has a unique name | `UNIQUE (name)` on `characters` |
| Gold never goes negative | `CHECK (gold >= 0)` |
| An item must be a real type | `type_id REFERENCES item_types` |
| An item must have a real owner | `owner_id REFERENCES characters` |
| No empty stacks | `CHECK (quantity >= 1)` |
| One stack per slot | `UNIQUE (owner_id, bag, slot)` |
| No stat twice on one item | `PRIMARY KEY (item_id, stat)` on `item_affixes` |
| A type in use cannot be deleted | the foreign key from `items` blocks the delete |
| A stack never exceeds its type's max | not expressible as a `CHECK`, since it spans two tables; use a trigger or enforce it in code |

The last row matters. A `CHECK` can only see the row it is checking. Rules that compare two tables need a **trigger** (a small procedure the database runs before an insert or update) or application code. Lab 02 has a stretch goal to write that trigger in SQLite.

### Where SQLite and PostgreSQL differ

The labs use SQLite. Four differences will bite you if you forget them.

- **Foreign keys are off by default in SQLite**, for backwards compatibility, and must be turned on per connection with `PRAGMA foreign_keys = ON`. Forget it and every `REFERENCES` in your schema is decoration. PostgreSQL always enforces them.
- **SQLite types are flexible.** In an ordinary SQLite table, inserting `'xyz'` into an `INTEGER` column stores the string. Since SQLite 3.37.0 (2021) you can declare a table `STRICT` to reject that. PostgreSQL rejects it always.
- **NULLs are not equal in UNIQUE constraints**, in both systems. If `bag` were nullable, two items with `bag = NULL` in the same slot would both be accepted, because `NULL` is not equal to `NULL`. That is why our `bag` is `NOT NULL` with 0 for the backpack. PostgreSQL 15 and later let you write `UNIQUE NULLS NOT DISTINCT` to treat NULLs as equal; SQLite has no such option.
- **Foreign keys are not indexed automatically.** PostgreSQL does not create an index on `items.owner_id` just because it references `characters`. Without one, loading a character's items scans the whole table. Add `CREATE INDEX ON items(owner_id)` and, for world-wide counts, `CREATE INDEX ON items(type_id)`. [Week 4](w04-sql-ii-indexes-and-query-plans.md) covers why.

For ids in PostgreSQL, use `bigint GENERATED ALWAYS AS IDENTITY` rather than `INTEGER`. A busy MMO can create more than 2.1 billion item rows over its lifetime (the limit of a 32-bit integer), and changing a primary key type on a live table is a week 9 problem you want to avoid.

## In-class activity (25 minutes)

In pairs, design the schema for a mail system in an invented MMO. A player can send a letter with a text body, up to 5 attached item stacks, and optional gold, to any character. Letters expire after 30 days, and unopened letters return their attachments to the sender.

1. Draw the tables with columns, primary keys and foreign keys. Decide where attached items live while in the mail. (Hint: can an item be in a bag and in a letter at once?)
2. List every game rule from the paragraph above and mark which constraint enforces it, or say "code" if none can.
3. Estimate row counts: 200,000 characters each send 3 letters a day with 1.5 attachments on average, and letters live 30 days. How many letter rows and attachment rows exist at steady state?
4. Swap with another pair and find one way to lose or duplicate an item in their design.

Expected output: a table diagram, a rule-to-constraint list, `200,000 × 3 × 30 = 18,000,000` letter rows and 27,000,000 attachment rows, and one flaw in your neighbors' design.

## Common misconceptions

- **"JSON columns are modern; tables are old-fashioned."** They answer different questions. A JSON blob is a good fit for data read and written whole by one owner. Anything summed, searched or partly changed across players wants rows. Most real schemas use both.
- **"Normalization makes queries slow because of joins."** A join on an indexed key is cheap, and normalized rows are smaller, so more fit in memory. Denormalize only when a measured, frequent read needs it, and keep one source of truth.
- **"The foreign key protects me in SQLite."** Only on connections that ran `PRAGMA foreign_keys = ON`. A maintenance script that forgets the pragma can insert orphans.
- **"Stacking is a UI feature."** It is a data rule. Two copies stack only if they have no instance state that differs.

## Check yourself

1. A game adds a "soulbound to" column on items, filled when a player equips an item. Explain what happens to stacking for potions and for swords, and whether that is a problem.
2. Using `r = 60` bytes and 136 rows per page, how many pages does a table of 1,000,000 item rows need, and how many megabytes is that?
3. A designer wants to store "list of characters who have killed this boss" on the boss row. Propose the correct table instead and its primary key.
4. Rewrite this EVE ESI record into rows for `item_types`, `items` and the location relationship: `{"item_id": 5001, "type_id": 587, "quantity": 1, "is_singleton": true, "location_id": 5000, "location_type": "item", "location_flag": "HiSlot0"}`.
5. Why does `UNIQUE (owner_id, bag, slot)` fail to stop two items in one slot if `bag` allows NULL? Give two fixes, one for each database.

<details>
<summary>Answers</summary>

1. Potions are not equipped, so the column stays NULL on all of them and they still stack. Swords already do not stack (durability), so nothing changes for them. It would become a problem for any stackable item that can be equipped or bound, such as ammunition: bound and unbound copies could no longer share a stack, so the code must treat binding as instance state.
2. `1,000,000 / 136 = 7,353` pages (rounding up), `× 8,192 = 60.2 MB`.
3. A join table `boss_kills (boss_id, character_id, first_killed_at)` with primary key `(boss_id, character_id)`, both foreign keys. Facts about the kill, like the date, live on the pair.
4. `items` row: `item_id 5001, type_id 587, quantity 1, container_id 5000`, plus a text column such as `location_flag = 'HiSlot0'` (our `slot` is an integer), and a flag or rule that it is a singleton. `type_id 587` refers to a row in `item_types`. Item 5000 is itself a row in `items` (the ship), so `container_id` is a self-referencing foreign key.
5. `NULL` is not equal to `NULL`, so the constraint sees two different keys. Fix in either database: make `bag NOT NULL` with a sentinel such as 0. In PostgreSQL 15+, you can also write `UNIQUE NULLS NOT DISTINCT (owner_id, bag, slot)`.

</details>

## Lab / assignment hook

[Lab 02, an inventory schema that enforces the rules](../labs/lab02.md). Write `schema.sql` for characters, item types, items and affixes so that 12 constraint tests pass (and a stretch trigger for stack limits), then measure the blob and row designs on a 300,000-item world. Deliverable: `schema.sql`, the measurement table, and a 300-word recommendation on which parts of a character to keep as rows and which as JSON.

## Sources

- Minecraft Wiki, "Stack" (Java and Bedrock Editions, as of September 2026). Stack sizes of 64, 16 (many projectiles) and 1 (items with durability); stacks up to 99 in Java Edition through data components.
- Guild Wars 2 Wiki, "API:2/characters/:id/inventory" (API v2, as of September 2026). Bags with id, size and inventory; slots null when empty; `count` 1 to 250; optional `upgrades`, `infusions`, `skin`, `stats`, `binding`, `bound_to`.
- EVE Online ESI OpenAPI specification, `GET /characters/{character_id}/assets` (compatibility date 2025-08-26, fetched September 2026 from esi.evetech.net/meta/openapi.json). Required fields `item_id`, `type_id`, `quantity`, `is_singleton`, `location_id`, `location_type` (`station`, `solar_system`, `item`, `other`) and `location_flag`.
- PostgreSQL 18 documentation, "Database Page Layout". 8 kB pages, 24-byte page header, 4-byte item identifiers, 23-byte row header.
- PostgreSQL 18 documentation, "TOAST". Out-of-line and compressed storage for rows wider than about 2 kB.
- PostgreSQL 18 documentation, "Constraints". NULLs are distinct in unique constraints unless `NULLS NOT DISTINCT` is given; foreign keys do not create an index on the referencing columns.
- SQLite documentation, "SQLite Foreign Key Support" (foreign keys off by default, per connection) and "STRICT Tables" (added in 3.37.0, 2021-11-27; non-strict tables store text in integer columns when conversion fails).
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 2.

## Interactive spec: examples/w02-blob-vs-rows.html

**The one insight:** a blob is cheap to load whole and expensive to change in part or search across; rows are the reverse. Changing one slider (inventory size `I`) makes the blob's cost for "move one item" grow in a straight line while the row cost stays flat.

**Layout (two linked views, stacked on mobile, side by side at ≥ 900px):**

- View A, "what is stored": a schematic of storage for 12 sample characters. Blob design on top: each character is one horizontal bar whose length is proportional to `I × j`. Row design below: a grid of pages (rectangles), each holding up to `floor(8168 / r)` small cells, with each character's rows given a consistent hue (use 12 muted tones derived from the token palette, not the semantic red). Rows for one character are scattered across pages using a seeded shuffle, to show fragmentation. When an operation is selected, the bytes it touches light up: whole bars (blob) or individual cells and their pages (rows).
- View B, "bytes touched": horizontal bar chart on a log scale (10 B to 10 GB), two bars per operation (blob, rows) for the four operations: load one character, move one item, count one type world-wide, rename one item type (with denormalized names as a third, optional bar). The selected operation is highlighted. Numbers are printed at the end of each bar.

**Controls:**

- `C` characters: slider 1,000 to 1,000,000 on a log scale (default 200,000).
- `I` stacks per character: slider 20 to 600 (default 150).
- `j` JSON bytes per item: slider 30 to 200 (default 70).
- `K` item types: slider 100 to 50,000 on a log scale (default 8,000).
- Operation selector (radio buttons): load one character, move one item, count one type, rename one type.
- Toggle "denormalize name into rows" (adds 40 bytes to `r` and enables the rename bar).

**Formulas (exact):**

```
r            = 60 (normalized) or 100 (denormalized)
rows_per_pg  = floor(8168 / r)
rows         = C × I
pages        = ceil(rows / rows_per_pg)
rows_bytes   = pages × 8192
blob_bytes   = C × I × j
load_blob    = I × j
load_rows    = I × r             (data) ; pages_touched_max = min(I, pages)
move_blob    = 2 × I × j
move_rows    = r
count_blob   = C × I × j
count_rows   = min(ceil(C × I / K), pages) × 8192   (worst case, one page per match)
rename_rows  = 1 row (normalized) ; ceil(C × I / K) rows × r (denormalized)
rename_blob  = ceil(C × I / K) blobs rewritten if names are copied into blobs, shown as that × I × j
```

**Test values (must match at defaults, normalized):**

- `rows = 30,000,000`, `rows_per_pg = 136`, `pages = 220,589`, `rows_bytes = 1.81 GB`, `blob_bytes = 2.10 GB`.
- load: blob 10,500 B, rows 9,000 B, pages touched up to 150, drawn as a third "pages, worst" bar of `150 × 8,192 = 1,228,800` B (1.23 MB).
- move: blob 21,000 B, rows 60 B.
- count: blob 2.10 GB, rows 3,750 matches, worst case 30.7 MB.
- Denormalized: `rows_per_pg = 81`, `pages = 370,371`, `rows_bytes = 3.03 GB`, rename touches 3,750 rows.
- `I = 250`: rows 50,000,000, pages 367,648, 3.01 GB; move blob 35,000 B.

**First screen:** defaults, operation "move one item" selected, so two whole blob bars light up in view A while a single cell lights up in the page grid, and view B shows 21,000 B against 60 B with the ratio "350×" printed between them.

**Accessibility:** controls keyboard operable with visible focus; a text summary of the selected operation's numbers in an `aria-live="polite"` region; respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. No game art, icons or logos.
