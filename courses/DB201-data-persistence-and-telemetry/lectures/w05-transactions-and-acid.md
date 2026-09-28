# DB201 · Week 05 — Transactions and ACID

**Why this matters:** A trade between two players is at least four writes: two gold balances, one item owner, one log row. Anything that can stop a program between two writes, such as a crash, a bug, a full disk or a deploy, can leave the world with half a trade. Half a trade is either a dupe or a theft. A transaction is the tool that makes "half" impossible, and this week you learn exactly what it promises, what it costs, and what it does not promise.

**You will be able to:**
- Define atomicity, consistency, isolation and durability in terms of a game trade, and name the failure each one prevents.
- Compute the probability that independent per-character saves leave a trade half-persisted, as a function of save interval and crash time.
- Write a trade as one transaction in Python's `sqlite3` and in PostgreSQL, including the rollback path.
- Estimate commit throughput from the flush time and the batch size, and choose where a game can relax durability without losing atomicity.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 7, from the start through "Single-Object and Multi-Object Operations". PostgreSQL 18 documentation, section 28.4 "Asynchronous Commit". Python documentation, `sqlite3` module, the "Transaction control" explanation.

**Prerequisites from earlier courses:** [DB201 week 1, why persistence is hard](w01-why-persistence-is-hard-in-games.md) (the save-interval model, `atomic_save`, and the warning that a trade saved in two pieces can dupe). [DB201 week 2, relational modeling](w02-relational-modeling-characters-inventories-items.md) (constraints as game rules, `CHECK (gold >= 0)`). [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) (multiplying probabilities of independent events). Looking ahead, [MMO304 week 4, money supply and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (year 3) shows why created gold hurts every player; this week needs only the idea that it does.

**Interactive:** [examples/w05-split-save.html](../examples/w05-split-save.html). Keep it open during section 2.

---

## 1. A trade is not one write

Here is the simplest trade a game has. Character 1 sells a sword to character 2 for 500 gold. In the row model of week 2, the server must do this:

```sql
UPDATE characters SET gold = gold - 500 WHERE character_id = 2;   -- buyer pays
UPDATE characters SET gold = gold + 500 WHERE character_id = 1;   -- seller is paid
UPDATE items SET owner_id = 2 WHERE item_id = 5001;               -- sword moves
INSERT INTO trade_log (seller, buyer, item_id, price) VALUES (1, 2, 5001, 500);
```

Four statements. Between any two of them the process can die. If it dies after the second, the buyer has paid, the seller has been paid, and the sword has not moved. The buyer is 500 gold poorer with nothing to show for it. If the order were different, the sword could move and nobody pay. In Lab 05 you do exactly this. A child process runs the first two statements and then calls `os._exit(1)`, the software equivalent of pulling the plug. In autocommit mode, where every statement commits on its own, the database after restart shows the seller with 500 gold, the buyer with 0, and the sword still with the seller.

### The transaction

A **transaction** groups statements so the database treats them as one unit:

```sql
BEGIN;
UPDATE characters SET gold = gold - 500 WHERE character_id = 2;
UPDATE characters SET gold = gold + 500 WHERE character_id = 1;
UPDATE items SET owner_id = 2 WHERE item_id = 5001;
INSERT INTO trade_log (seller, buyer, item_id, price) VALUES (1, 2, 5001, 500);
COMMIT;
```

Until `COMMIT` succeeds, none of the changes count. If the process dies before then, or the program calls `ROLLBACK`, or any statement fails, the database behaves as if the transaction never started. Run the same crash in Lab 05 with a `BEGIN` in front and the restarted database shows the original state: buyer 500, seller 0, sword with the seller. Nothing happened, which is correct, because the trade never finished.

### ACID, one letter at a time

The four guarantees a transaction offers are abbreviated ACID. Kleppmann points out that the acronym is fuzzy in practice and that databases differ in what each letter means. So here is each one in game terms, with the failure it prevents.

- **Atomicity.** All of the transaction's writes happen, or none do. It prevents half a trade after a crash or error. Kleppmann suggests "abortability" would be a better name. The key property is that a failed transaction can be thrown away completely.
- **Consistency.** The database moves from one valid state to another, where "valid" means your rules hold. Most of this letter is your job, not the database's. The database enforces the constraints you declared (week 2's `CHECK (gold >= 0)`, foreign keys, unique slots). If a statement would break one, the statement fails and the transaction can roll back. Rules you did not declare, like "total gold only changes through faucets and sinks," are invisible to it.
- **Isolation.** Concurrent transactions do not see each other's half-finished work. It prevents two trades that run at the same moment from interfering. It is also the letter with the most exceptions, because full isolation is expensive. Week 6 is entirely about this letter.
- **Durability.** Once `COMMIT` returns success, the data survives a crash or power loss. It prevents "the server said OK, then forgot." It costs a disk flush per commit, and section 3 puts a number on that.

The letters are independent. A system can be durable and not atomic (autocommit mode is durable per statement and loses half-trades). It can be atomic and not durable, which is what PostgreSQL's asynchronous commit gives you, and section 3 argues that is often the right trade for a game.

### A trade in Python

Python's `sqlite3` module has a history of surprising people about transactions. By default (the "legacy" transaction control, still the default in Python 3.14), the module silently opens a transaction before any `INSERT`, `UPDATE` or `DELETE`, and nothing is saved until you call `commit()`. The clearest pattern is the connection used as a context manager, which commits if the block finishes and rolls back if it raises:

```python
import sqlite3

def sell(con, item_id, seller, buyer, price):
    with con:  # BEGIN ... COMMIT, or ROLLBACK on any exception
        con.execute("UPDATE characters SET gold = gold - ? WHERE character_id = ?",
                    (price, buyer))           # fails the CHECK if the buyer is short
        con.execute("UPDATE characters SET gold = gold + ? WHERE character_id = ?",
                    (price, seller))
        moved = con.execute("UPDATE items SET owner_id = ? "
                            "WHERE item_id = ? AND owner_id = ?",
                            (buyer, item_id, seller)).rowcount
        if moved != 1:
            raise ValueError("seller no longer owns the item")  # rolls back the gold
        con.execute("INSERT INTO trade_log (seller, buyer, item_id, price) "
                    "VALUES (?, ?, ?, ?)", (seller, buyer, item_id, price))
```

Three things in that function matter. The buyer's overdraft is caught by the `CHECK` constraint from week 2, which raises `sqlite3.IntegrityError` and rolls the whole trade back. The item move checks that the seller still owns the item and raises if not, which also undoes the gold. And nothing about the order of statements matters for correctness any more, because either all four land or none do. Python 3.12 added an `autocommit` attribute that makes this behaviour explicit. Setting `autocommit=False` in `connect()` gives the PEP 249 behaviour, where a transaction is always open and `commit()` or `rollback()` ends it.

In PostgreSQL the SQL is the same. The drivers differ (`psycopg` also uses `with conn.transaction():`), and PostgreSQL gives you `SAVEPOINT` inside a transaction if you want to undo part of it, for example to retry one failed mail delivery without abandoning a whole batch.

## 2. Worked example: the split save

### The hook

Ultima Online private shards run on community-built server emulators. The best known, RunUO, saves the entire world every 5 minutes by default. When it does, it pauses every client connection, broadcasts "The world is saving, please wait.", writes every mobile, item and guild to disk, and then reports "World save complete" with how many seconds the whole process took. Players on large shards learned to stop mid-fight when the message appeared.

Freezing an entire shard every five minutes looks crude. It is also one of the safest save designs a game can have, and the reason is not obvious until you look at the alternative most people build first. That alternative is to save each character on its own timer, which spreads the write load evenly (week 1's model) and never freezes anyone. Here is what it does to trades.

### The model

Two characters, A (the giver) and B (the receiver), are each saved every `T` seconds. Their timers are independent, so each character's next save after any moment falls at a random time, uniform on `[0, T)`. A trade happens at time 0. In memory, the item leaves A and appears in B. The server then crashes `d` seconds later. After the restart, each character is loaded from its own last save.

A's save includes the trade if A was saved between the trade and the crash, which happens with probability:

```
p = min(d / T, 1)
```

B's save is independent of A's, with the same `p`. Four outcomes:

| A's save has the trade | B's save has the trade | Result after restart | Probability |
|---|---|---|---|
| yes | yes | trade happened, correct | `p²` |
| no | no | trade never happened, acceptable | `(1 − p)²` |
| no | yes | **dupe**: A still has the item, B has it too | `p (1 − p)` |
| yes | no | **loss**: A gave it away, B never got it | `p (1 − p)` |

So the chance a crash `d` seconds after a trade splits it is:

```
P(split) = 2 p (1 − p),   with P(dupe) = P(loss) = p (1 − p)
```

- `p` is the fraction of one save interval that passed between the trade and the crash.
- `T` is the per-character save interval.
- `d` is the time from the trade to the crash.

### Numbers you can check

| Crash delay `d / T` | `p` | `P(dupe)` | `P(loss)` | `P(split)` |
|---|---|---|---|---|
| 0.1 | 0.1 | 0.09 | 0.09 | 0.18 |
| 0.25 | 0.25 | 0.1875 | 0.1875 | 0.375 |
| 0.5 | 0.5 | 0.25 | 0.25 | **0.5** |
| 0.75 | 0.75 | 0.1875 | 0.1875 | 0.375 |
| 1.0 or more | 1 | 0 | 0 | 0 |

The worst moment for a crash is half an interval after the trade, when a coin flip decides whether the trade is split. The average over a crash anywhere in the interval after the trade, `d` uniform on `[0, T]`, is:

```
average P(split) = ∫₀¹ 2p(1 − p) dp = 2 × (1/2 − 1/3) = 1/3
```

One trade in three that happened in the last save interval before a crash comes back split. Half of those are dupes.

Put that on a server. Take 5,000 players online, `T = 300` seconds, and one cross-player transfer (trade, mail, auction purchase) per player every 10 minutes. That is `5,000 / 600 ≈ 8.3` transfers per second, so about 2,500 transfers happened in the 300 seconds before any crash. A third of them split, about 833. That is roughly 417 dupes and 417 losses per crash. Every loss is a support ticket. Every dupe is an item or a stack of gold created from nothing, and some players will learn to cause crashes on purpose to produce them.

Lab 05 checks the model by simulation, with 200,000 trials, `T = 300` and crashes uniform in `[0, 300)`. It found a dupe rate of 0.166 and a loss rate of 0.168, against the model's 1/6 ≈ 0.167 each.

### A visual you can move

Open the interactive. The top view is a timeline: two rows of save ticks for A and B with their phases, a trade marker at 0, and a crash marker you drag. Under it, a "restored from disk" panel shows what each character holds after restart and counts swords in the world: 0, 1 or 2. Drag the crash marker past A's tick but not B's and the world shows 0 swords. Past B's but not A's, 2 swords. The bottom view plots `P(dupe)` and `P(loss)` against `d / T`, the parabola `p(1 − p)`, with a dot at your current crash delay. Now switch "Save both characters in one transaction when they trade" on. The timeline gains a joint save at the trade, the parabola collapses to a flat line at zero, and the sword count never leaves 1.

### Cross-game recognition

The split save is one problem with one fix. Make the moment of persistence a single point for everything that must agree. Every working system you know does this somehow.

**RunUO (Ultima Online emulator).** The world save is a snapshot of every object at a single instant, taken while network traffic is paused. Deletions requested during the save are queued and applied afterwards. So every trade is either entirely before the snapshot or entirely after it. `P(split) = 0` for any crash, and the price is a pause that grows with the size of the world.

**A database transaction.** PostgreSQL writes each change to its write-ahead log (WAL) and marks a transaction committed with a single commit record. After a crash, recovery replays the log and treats every transaction without a commit record as never having happened. SQLite in rollback-journal mode does the same with the moment it deletes the journal, as week 1 described. The whole trade has one commit point, which is the database's version of RunUO's freeze, but for four rows instead of the whole world.

**Git.** A commit records the new state of every changed file under one hash. There is no moment when half your files are in the new commit and half in the old one. A crash during `git commit` leaves either the old commit as `HEAD` or the new one. If you have ever wished your game's save worked like version control, this is the property you wanted.

**Bank transfers.** Kleppmann's chapter 7 returns several times to money moving between two bank accounts, because it is the plainest case of two writes that must agree. Accounting solved the same problem centuries before computers, by recording every transfer as a single journal entry with a debit and a matching credit, never as two separate entries. Our trade log row is that journal entry.

Rewritten in the model's terms, each system makes A's save and B's save the same event, so the two outcomes "yes/no" and "no/yes" cannot occur.

### Eyes-open design judgment

- **Per-character saves are fine for per-character state.** XP, position and quest progress belong to one character. Losing the last `T/2` seconds of them on a crash is week 1's trade-off, and nothing dupes.
- **Anything that crosses characters must commit as one transaction.** Trades, mail, auction purchases, guild bank deposits and crafting orders all qualify. A common hybrid is periodic saves for personal state plus an immediate transaction that writes both sides of every transfer. That transaction also becomes the new last-saved state for the items and gold involved, so the next periodic save cannot overwrite it with stale values. Be sure your save code does not write back stale copies of rows the transaction just changed. That exact bug is the heart of week 6.
- **Stop-the-world is honest and does not scale.** RunUO's approach is correct and simple. It also pauses everyone for as long as the save takes, and that time grows with world size. Large games prefer transactions, which make the "freeze" as small as one trade.
- **If the two sides live in different databases, a local transaction cannot cover both.** This happens across shards, or between a game database and a billing service. Then you need a protocol that makes the outcome recoverable. One example is a durable transfer log written first and applied idempotently to both sides. Another is two-phase commit. [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) ("Item ownership and transactional integrity") covers these. Until then, if you must write two sides separately, take before you give. A crash then produces a loss, which a support agent can repair from the log, never a dupe, which spreads through the economy.

### Check yourself on the worked example

1. With `T = 120` s, a crash happens 30 s after a trade. What are `P(dupe)` and `P(split)`?
2. A designer proposes saving characters every 60 s instead of 300 s "to fix dupes." Using the fleet numbers above (8.3 transfers per second), how many split trades should you expect per crash now? Did the change fix the problem?
3. Why is `P(dupe)` exactly equal to `P(loss)` in this model? Describe a change to the save code that makes dupes impossible while keeping per-character saves for trades, at the cost of more losses.

<details>
<summary>Answers</summary>

1. `p = 30/120 = 0.25`. `P(dupe) = 0.25 × 0.75 = 0.1875`. `P(split) = 0.375`.
2. Transfers in the last 60 s: `8.3 × 60 ≈ 500`. A third split, about 167 per crash (83 dupes, 83 losses). Five times fewer, not zero. The average split fraction is still 1/3 for any `T`. A shorter interval only shrinks the number of trades exposed.
3. The model treats A and B symmetrically, with independent uniform phases. Save the giver immediately at the moment of the trade, and let the receiver wait for its timer. Then A's save always includes the trade (`p_A = 1`), so "no/yes" is impossible and the only failure is "yes/no," a loss, with probability `1 − p_B`. That is safer for the economy and worse for players. The real fix is one transaction for both.

</details>

## 3. What durability costs

Atomicity is almost free. Durability is not. For `COMMIT` to promise that data survives a power cut, the database must wait until the log record is on storage that survives power loss. That wait is a **flush** (the `fsync` family of system calls), and it takes about the same time whether it carries one transaction or a hundred.

### The flush model

Let `t_f` be the time for one flush, and let each flush carry `b` committed transactions:

```
commits per second  = b / t_f
latency per commit  ≈ t_f   (plus any time spent waiting to join a batch)
```

Lab 05 measures this in SQLite in WAL mode with `synchronous = FULL`, on the lecturer's laptop (Apple silicon SSD, macOS, with `PRAGMA fullfsync = ON` so that macOS really flushes the drive's cache):

| Setting | Trades per commit `b` | Time per commit | Trades per second |
|---|---|---|---|
| `synchronous = FULL` | 1 | 3.89 ms | 257 |
| `synchronous = FULL` | 10 | 3.86 ms | 2,591 |
| `synchronous = FULL` | 100 | 4.00 ms | 24,990 |
| `synchronous = OFF` | 1 | 0.006 ms | 158,874 |

The middle column barely moves. The flush costs about 4 ms regardless of how much it carries, so throughput is almost exactly proportional to `b`. Without `fullfsync`, macOS reports 0.036 ms per commit, because a plain `fsync` there hands data to the drive without forcing the drive's own cache to disk. That number is a measure of the operating system, not of durability. Check what "flushed" means on your platform before you trust a benchmark.

### Group commit

A game server does not batch 100 trades on purpose. It has many connections committing at once. PostgreSQL uses this. When one session flushes the WAL, the flush carries every commit record written so far, including other sessions' records, so several transactions share one flush. This is **group commit**. The `commit_delay` setting makes a committing session wait a few microseconds before flushing, so that more sessions can join, and it trades a little latency for throughput when load is high.

Put numbers on it. The 5,000-player server commits 8.3 transfers per second, trivial at 257 per second even with no batching. Now suppose you also commit every loot pickup and gold change as its own transaction, one per player every 2 seconds. That is 2,500 commits per second. One flush at a time handles 257. You need about 10 commits per flush on average, which group commit gives you only if enough sessions commit concurrently. Otherwise players feel commit latency queue up.

### Relaxing durability without losing atomicity

PostgreSQL's `synchronous_commit` can be turned off per transaction. With it off, `COMMIT` returns before the flush, and a background WAL writer flushes every `wal_writer_delay` (200 ms by default). A crash can lose the most recent transactions, up to three times `wal_writer_delay`, so at most 600 ms of commits. It cannot lose half of one. The documentation is explicit that this is not the same as `fsync = off`, which risks corrupting the database.

That distinction is the design lever for games:

- **Position, XP, kill counts:** commit asynchronously. Losing 600 ms of them is invisible next to week 1's 150-second average periodic-save loss.
- **Trades, purchases, anything involving real money or another player:** commit synchronously. Losing a trade that the UI already confirmed is a support ticket, and with real money involved it is a refund.
- **Never:** `fsync = off` in PostgreSQL, or `synchronous = OFF` in SQLite, on data you cannot regenerate. SQLite's documentation warns that with `OFF`, an operating-system crash or power loss can corrupt the database. That is worse than losing recent commits, and it breaks atomicity, not only durability. It is fine for building a database from scratch that you can rebuild.

SQLite's middle setting, `synchronous = NORMAL` in WAL mode, is similar to PostgreSQL's asynchronous commit. SQLite's documentation says that combination is always consistent but may roll back the last transactions after a power loss.

## 4. Consistency is mostly your job

Transactions make your rules stick, but only the rules you told the database about. Three kinds matter in games.

**Declared constraints** fail the statement, so the transaction can roll back:

```sql
CREATE TABLE characters (
  character_id INTEGER PRIMARY KEY,
  gold INTEGER NOT NULL CHECK (gold >= 0)      -- no overdrafts, ever
);
CREATE TABLE items (
  item_id  INTEGER PRIMARY KEY,                -- one row per instance: no two copies
  owner_id INTEGER NOT NULL REFERENCES characters(character_id),
  bag INTEGER NOT NULL, slot INTEGER NOT NULL,
  UNIQUE (owner_id, bag, slot)                 -- two items cannot share a slot
);
```

The `PRIMARY KEY` on `item_id` matters more than it looks. In the row model, a duplicated sword would need two rows with the same `item_id`, which the database refuses. A whole class of dupes becomes a failed insert instead of a corrupted economy. Week 6 builds on this.

**Invariants across rows** are rules like "total gold changes only through logged faucets and sinks" or "every trade log row matches two balance changes." No `CHECK` constraint can see across rows. You enforce them by making every change go through a transaction that also writes the log row, and you verify them with audit queries. MMO304's [economic telemetry](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) is that audit at world scale. Week 6 shows a studio catching a dupe this way within a day.

**Rules the database cannot know** are game design, like "soulbound items cannot be traded." Put them in the transaction's code, and where you can, also in a constraint, such as a `CHECK (NOT soulbound OR owner_id = original_owner)`. Two layers catch bugs that one misses.

### A first look at isolation

One more thing happens when many transactions run at once. PostgreSQL does not overwrite a row in place. An `UPDATE` writes a new version of the row and marks the old one obsolete, and each transaction reads the versions that were committed when its statement (or, at stricter levels, its transaction) began. This is **multi-version concurrency control** (MVCC). It is why readers never wait for writers. It is also why the week 4 index-only scan must check a visibility map. Some row versions in the index are not visible to your transaction.

PostgreSQL's default level is **Read Committed**. Each statement sees data committed before the statement began. That is enough for the trade in section 1, because every statement changes rows relative to their current value (`gold = gold - 500`) or checks a condition in the same statement (`WHERE owner_id = ?`). It is not enough for code that reads a value into the application, decides something, and writes it back later. That pattern is the duplication bug, and it is next week.

## In-class activity (25 minutes)

Work in groups of three. You receive a list of eight game actions: loot pickup, XP gain, player-to-player trade, mail with attachment, auction purchase, guild bank deposit, cosmetic purchase with real money, and character position.

1. For each action, decide: periodic save, asynchronous commit, or synchronous transaction. One sentence of justification each.
2. For the three cross-character actions, list the rows the transaction writes and the constraint or `WHERE` condition that makes it fail safely.
3. Using the flush model with `t_f = 4 ms`, estimate the commits per second your policy produces for 5,000 players (make and state your own per-action rates) and whether one flush at a time can keep up.
4. Pick one action where your group disagreed. Write both positions in two sentences each.

Expected output: an eight-row policy table, three transaction sketches, a commit-rate estimate, and the recorded disagreement.

## Common misconceptions

- **"A transaction makes my code run as if nobody else were running."** Only at the strictest isolation level, which is not the default. At Read Committed, two transactions can still interfere if the application reads a value and writes it back later (week 6).
- **"Saving more often fixes trade dupes."** It reduces how many trades a crash can split, but the fraction split stays at 1/3 of trades in the last interval for any `T`. Only one commit point for both sides removes it.
- **"Turning off synchronous commit risks corrupting the database."** In PostgreSQL, `synchronous_commit = off` risks losing the last few hundred milliseconds of commits, whole. `fsync = off` risks corruption. They are different settings.
- **"Consistency means the database keeps my data correct."** It keeps the constraints you declared. Every other invariant is enforced by your transaction code and checked by your audits.

## Check yourself

1. In autocommit mode, a server runs the four trade statements in the order item move, seller paid, buyer pays, log. It crashes after the first. Describe the world after restart and classify the failure (dupe, loss, or neither).
2. Per-character saves every 240 s, and a crash 180 s after a trade. Compute `P(dupe)`, `P(loss)` and `P(correct)`.
3. A server measures `t_f = 2 ms`. How many commits per second can it do with no batching? What average batch size does it need for 6,000 commits per second?
4. A game commits trades with `synchronous_commit = off`. A player completes a trade and the server crashes 300 ms later. List the possible outcomes. Which outcome of the split-save table is impossible here, and why?
5. Why does the `PRIMARY KEY` on `item_id` in the row model block a duplicated sword, while the blob model of week 2 does not?

<details>
<summary>Answers</summary>

1. The sword belongs to the buyer. No gold moved. No log row exists. The buyer received the item for free, and the seller lost it unpaid. It is a loss for the seller, and the item was not duplicated. Had the statements run in a different order, the result would differ, which is exactly why order should not matter. Use a transaction.
2. `p = 180/240 = 0.75`. `P(dupe) = P(loss) = 0.75 × 0.25 = 0.1875`. `P(correct) = p² + (1 − p)² = 0.5625 + 0.0625 = 0.625`.
3. `1 / 0.002 = 500` commits per second. For 6,000 per second you need `b = 6,000 × 0.002 = 12` commits per flush on average.
4. Either the trade's commit record reached disk before the crash (the trade happened) or it did not (the trade never happened). A split is impossible because the four writes share one commit record, so atomicity holds even though durability was relaxed. The player may see a confirmed trade undone, which is a support issue, not an economy issue.
5. In the row model the sword is one row with a unique key. A second copy would need a second row with the same `item_id`, which the constraint rejects. In the blob model the sword's id is a value inside two separate JSON documents, and no constraint looks inside them, so both can contain it.

</details>

## Lab / assignment hook

[Lab 05, split saves, real crashes and commit cost](../labs/lab05.md). You simulate the split save and derive its closed form, kill a process in the middle of a trade with and without a transaction and audit the result, and measure trades per second against batch size and `synchronous`. Deliverable: the completed `acid_lab.py`, your three tables, and a half-page persistence policy for the in-class activity's eight actions. This lab counts toward the SQL labs (40%).

## Sources

- RunUO, open-source Ultima Online server emulator (GitHub `runuo/runuo`, master branch, read September 2026). `Scripts/Misc/AutoSave.cs`: default save interval `TimeSpan.FromMinutes(5.0)`. `Server/World.cs`, `Save()`: pauses network state, broadcasts the saving message, queues deletions during the save, reports elapsed seconds on completion. https://github.com/runuo/runuo. RunUO is a community emulator, not the official Ultima Online server.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 7: "The Meaning of ACID" (atomicity as abortability; consistency as a property of the application), "Single-Object and Multi-Object Operations".
- PostgreSQL 18 documentation (September 2026): section 28.4 "Asynchronous Commit" (loss window up to three times `wal_writer_delay`; differs from `fsync = off`); section 19.5 "Write Ahead Log" (`wal_writer_delay` default 200 ms; `commit_delay` and group commit); section 13.2.1 "Read Committed Isolation Level" (the default level). https://www.postgresql.org/docs/current/
- SQLite, "Pragma statements", `synchronous` (OFF may corrupt on OS crash or power loss; WAL with NORMAL stays consistent but may lose recent commits after power loss) and `fullfsync` (macOS F_FULLFSYNC). https://www.sqlite.org/pragma.html
- Python 3.14 documentation, `sqlite3`, "Transaction control" (legacy implicit transactions; the `autocommit` attribute added in 3.12; the connection context manager). https://docs.python.org/3/library/sqlite3.html
- Lab 05 measurements: DB201 lecturer's machine, Apple silicon, macOS, Python 3.13.5, SQLite 3.53.3, WAL mode, `fullfsync = ON`, September 2026.

## Interactive spec: examples/w05-split-save.html

**The one insight.** When two characters are saved on independent timers, a crash after a trade can restore one side with the trade and the other without it. The chance is `2p(1 − p)` and peaks at 50% half an interval after the trade. A single joint commit makes it zero for every crash time.

**Layout.** Two linked views stacked vertically at every width (timeline on top), plus a readout strip.

- Top, "What the disk remembers". A horizontal timeline from `t = −0.2T` to `t = 1.5T`. Two rows labelled "Character A (giver)" and "Character B (receiver)". Each row shows save ticks every `T` seconds starting at its phase (`φ_A`, `φ_B` in `[0, T)`), drawn as short vertical bars. A trade marker (diamond) at `t = 0` spanning both rows. A draggable crash marker (vertical red line) at `t = d`. The first tick of each row after 0 and before `d` is highlighted "saved with trade". Under the timeline, a "Restored from disk" box with two cards: A's inventory and B's inventory (a generic sword icon drawn with CSS/SVG shapes, present or absent), and a large count "Swords in the world: N" coloured neutral for 1, warning for 2 ("DUPE"), and muted for 0 ("LOST").
- Bottom, "Across all phases". x-axis `d / T` from 0 to 1.5. y-axis probability 0 to 0.55. Curves: `P(dupe) = p(1 − p)` and `P(loss)` (same curve; draw one solid, one dashed offset by 1px so both are visible, and label both), and `P(split) = 2p(1 − p)` bold. A dot on the `P(split)` curve at the current `d / T`. A horizontal dotted line at the average 1/3 over `[0, 1]`, labelled "average over the interval: 1/3".
- Readout strip: `T`, `d`, `d / T`, `p`, `P(dupe)`, `P(loss)`, `P(split)` (3 decimals), and for the current phases the actual outcome (correct, nothing happened, DUPE, LOST).

**Controls.** All keyboard reachable; arrow keys move sliders and the crash marker (step 1% of T).
- Save interval `T`: 30 to 600 s, step 10, default 300.
- Crash delay `d`: 0 to `1.5T`, default `0.5T`. The crash marker is draggable and mirrors this slider.
- Phase of A `φ_A` and phase of B `φ_B`: 0 to `T`, step 1% of T, defaults 0.7T and 0.3T (so the default crash at 0.5T gives B saved, A not: a DUPE).
- Button "Random phases" (draws both uniformly).
- Toggle "Save both characters in one transaction when they trade" (default off). When on, draw a joint tick at `t = 0` on both rows, the restored box always shows the sword with B, the bottom curves are replaced by a flat line at 0 labelled "one commit point: no split possible", and the outcome reads "correct".
- Button "Simulate 10,000 crashes" (with the current `T` and `d` uniform in `[0, T]`): draws random phases each trial and prints observed dupe and loss fractions next to the model's 1/6.

**Formulas.**
- `p = min(d / T, 1)`
- Outcome for given phases: `A_saved = φ_A < d`, `B_saved = φ_B < d` (first tick after the trade is at the phase). DUPE if `B_saved && !A_saved`; LOST if `A_saved && !B_saved`; correct if both; nothing happened if neither.
- `P(dupe) = P(loss) = p(1 − p)`; `P(split) = 2p(1 − p)`; average over `d ∈ [0, T]` is 1/3.

**Test values (must match exactly).**

| T | d | φ_A | φ_B | p | P(dupe) | P(split) | Outcome shown |
|---|---|---|---|---|---|---|---|
| 300 | 150 | 210 | 90 | 0.500 | 0.250 | 0.500 | DUPE (2 swords) |
| 300 | 150 | 90 | 210 | 0.500 | 0.250 | 0.500 | LOST (0 swords) |
| 300 | 30 | 210 | 90 | 0.100 | 0.090 | 0.180 | nothing happened (1 sword, with A) |
| 120 | 30 | 10 | 20 | 0.250 | 0.188 | 0.375 | correct (1 sword, with B) |
| 240 | 180 | 200 | 100 | 0.750 | 0.188 | 0.375 | DUPE |
| 300 | 400 | any | any | 1.000 | 0.000 | 0.000 | correct |

With the transaction toggle on, every row shows "correct" and `P(split) = 0.000`. The 10,000-crash simulation with `T = 300` should print dupe and loss fractions within 0.01 of 0.167.

**Visual rules.** Use `templates/interactive-tokens.css` inline. No game art; the sword is a generic shape. Respect `prefers-reduced-motion` (no marker animation) and `prefers-color-scheme`. No horizontal overflow at 390px; on narrow screens the timeline may compress but labels must stay legible.
