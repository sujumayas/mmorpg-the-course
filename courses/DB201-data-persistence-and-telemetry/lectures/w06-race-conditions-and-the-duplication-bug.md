# DB201 · Week 06 — Race Conditions and the Duplication Bug

**Why this matters:** Last week's transactions stop a crash from splitting a trade. They do not, by themselves, stop two trades that run at the same moment from both succeeding with the same sword. That bug creates items and gold from nothing. It passes every test you write alone at your desk, and players who find it can repeat it on demand. This week you trace it step by step, measure how easy it is to trigger, and learn the four standard ways to make it impossible.

**You will be able to:**
- Trace an interleaving of two concurrent handlers against a shared database and predict the final state.
- Count the interleavings of two multi-step handlers and the fraction that duplicate, and compute an attacker's chance of success from the race window and the request jitter.
- Fix a read-modify-write race with a conditional update, a row lock, a version check or serializable isolation, and state what each fix costs.
- Explain why acquiring locks in a fixed order prevents deadlock, and design that order for a two-player trade.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 7, "Weak Isolation Levels" through "Preventing Lost Updates", and skim "Write Skew and Phantoms". PostgreSQL 18 documentation, section 13.2 "Transaction Isolation" (the table of phenomena) and section 13.3.2 "Row-Level Locks" (`FOR UPDATE`).

**Prerequisites from earlier courses:** [DB201 week 5, transactions and ACID](w05-transactions-and-acid.md) (atomicity, Read Committed, the split save). [DB201 week 2, relational modeling](w02-relational-modeling-characters-inventories-items.md) (the blob model and the row model of an inventory). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) and [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (the chance of at least one success, and the expected number of tries). [CS202 week 2, latency and jitter](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w02-latency-jitter-loss-measure-your-own.md) (why two packets sent together arrive apart). Looking ahead, [MMO304 week 4, money supply and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (year 3) shows what duped gold does to prices.

**Interactive:** [examples/w06-trade-dupe-stepper.html](../examples/w06-trade-dupe-stepper.html). This is the course's signature example. Keep it open for all of section 2.

---

## 1. Why a server runs two things at once

A game server handles many requests at the same time. A zone server may process each player's messages on a pool of worker threads. An async server interleaves thousands of requests on one thread, switching whenever one waits for the database. Several zone servers, a mail service and an auction house service may all write to the same PostgreSQL database. In every case, two requests that arrive close together can be in progress at once, each paused in the middle while the other runs a step.

That is only a problem when both touch the same data. For a trade, the shared data is the giver's inventory. And the pattern that breaks is so common that it has a name. A **read-modify-write** cycle reads a value into the application, changes it in memory, and writes it back. Between the read and the write, the value in memory can go stale. If someone else changed the database in that gap, the write-back erases their change. Kleppmann calls this a **lost update**. When the value is an inventory, a lost update can be a dupe.

A **race condition** is any bug whose outcome depends on the timing of concurrent operations. It is the hardest kind of bug to find by testing, for a reason section 2 makes precise. When you test alone, you never send two requests close enough together.

## 2. Worked example: the trade dupe

### The hook

At the start of November 2021 (reported on 2 November), about five weeks after launch, Amazon Games disabled every way to move wealth between players in New World. That meant sending currency, the guild treasury, the trading post and player-to-player trading, all at once, while the team worked on a fix for a gold duplication exploit. The community team said players who had used the exploit would be banned. Amazon did not publish the technical cause, and neither will we. The response itself is the lesson. The studio shut off *every* path that moves value between two players, because each of those paths is a write to two sides that has to be correct under concurrency, and at that moment they could not be sure which ones were.

This is not new. In August 2005, Sony Online Entertainment reported that a group of players used a duplication bug in EverQuest II to create so much platinum that the game's total money supply rose by a fifth in about 24 hours. SOE's director of public relations said that "a lot of alarms" went off. The dupers had tried to sell the currency through Station Exchange, SOE's own real-money auction service, and the studio returned the economy to its pre-attack state.

Here is a bug that produces exactly that kind of event, small enough to trace by hand.

### The model

Use the blob model of week 2. Each character's inventory is one JSON list in one row, and the server edits it with read-modify-write. The giver (character 1) owns one sword, instance 5001. A trade handler has three steps:

```python
def naive_trade(con, receiver):
    inv = load(con, GIVER)                  # step R: read the giver's inventory
    if SWORD not in inv:
        return "rejected"
    got = load(con, receiver)               # step G: give (read-modify-write receiver)
    save(con, receiver, got + [SWORD])
    inv.remove(SWORD)                       # step T: take (write back the list from step R)
    save(con, GIVER, inv)
    return "done"
```

Each step is individually correct. Each `save` is a single `UPDATE` that commits atomically. Now two trades run concurrently, trade 1 giving the sword to character 2 and trade 2 giving it to character 3. The duplicate can come from a double-click, a script, or two clients on one account. Write their steps as `R1 G1 T1` and `R2 G2 T2`.

**The dupe condition.** Trade 2 duplicates the sword if its read `R2` happens before trade 1's take `T1`. At that moment the giver still has the sword, so the check passes, and trade 2 goes on to give a sword that is already on its way to someone else. Symmetrically, trade 1 duplicates it if `R1` happens before `T2`. The world ends with two swords when both reads come before the other trade's take:

```
dupe  ⇔  R2 before T1  and  R1 before T2
```

Only one bug is at work here. `T` writes back a copy of the giver's inventory that was read at `R`, without checking whether it is still current.

### Numbers you can check: the interleavings

A scheduler can run the six steps in any order that keeps each trade's own steps in order. The number of such interleavings is the number of ways to choose which three of the six time slots belong to trade 1:

```
C(6, 3) = 6! / (3! × 3!) = 20
```

Write an interleaving as a string of 1s and 2s, such as `112122`, meaning `R1 G1 R2 T1 G2 T2`. Apply the dupe condition to each:

| Interleavings | Count | Result |
|---|---|---|
| `111222`, `222111` (one trade entirely before the other) | 2 | one sword; the second trade is rejected |
| every other interleaving | 18 | **two swords** |

**18 of 20.** Unless one trade finishes completely before the other starts, the sword duplicates. Here is `112122` traced step by step. This is the output of `python dupe_lab.py --order 112122` in Lab 06:

| Step | What runs | Giver | Char 2 | Char 3 | Trade 2's copy in memory |
|---|---|---|---|---|---|
| 1 | `R1` reads giver | [5001] | [] | [] | — |
| 2 | `G1` gives to char 2 | [5001] | [5001] | [] | — |
| 3 | `R2` reads giver: sword still there, check passes | [5001] | [5001] | [] | [5001] |
| 4 | `T1` writes giver = [] | [] | [5001] | [] | [5001] (stale) |
| 5 | `G2` gives to char 3 | [] | [5001] | [5001] | [5001] (stale) |
| 6 | `T2` writes giver = [] from its stale copy | [] | [5001] | [5001] | — |

Two swords, and nothing in the database looks wrong. Every row is a valid inventory. The dupe is visible only if you count sword 5001 across all inventories.

Does it help to take before giving (`R T G`)? Try it on paper. The dupe condition is unchanged, but `T` is now each trade's second step. So it holds exactly when both trades read before either takes, meaning the order starts `12` or `21`: 6 + 6 = 12 of 20 interleavings dupe. Orders such as `112122`, where one trade reads and takes before the other reads, are now safe. Reordering shrinks the window without closing it. It helps against crashes, as week 5 showed, not against races.

### Numbers you can check: how often it fires

Interleavings are not equally likely in real time, so "18 of 20" is not a probability. For that, model time. Let:

- `w` be the **race window**, the time from a handler's read `R` to its take `T`. It includes the receiver's database round trip, so on a real server it is typically a few milliseconds.
- `J` be the **jitter**, the spread in when each request reaches the handler. Each of two requests sent "at the same time" starts after an independent random delay, uniform on `[0, J]`, from network jitter (CS202 week 2) and server queueing.

The trades overlap badly when their start times differ by less than `w`. For two independent uniform delays on `[0, J]` with `w ≤ J`:

```
P(dupe per attempt) = 1 − (1 − w/J)²
expected attempts to first dupe = 1 / P                  (geometric, MA102 week 7)
P(at least one dupe in n attempts) = 1 − (1 − P)ⁿ        (complement rule, MA102 week 3)
```

| `w / J` | `P` per attempt | Expected attempts | `P` of at least one in 20 attempts |
|---|---|---|---|
| 0.01 | 0.020 | 50.3 | 0.331 |
| 0.05 | 0.098 | 10.3 | 0.872 |
| 0.1 | 0.190 | 5.3 | 0.985 |
| 0.2 | 0.360 | 2.8 | 0.9999 |
| 1/3 | 0.556 | 1.8 | ≈ 1 |

Check the third row by hand. `1 − 0.9² = 0.19`, `1 / 0.19 = 5.3`, `1 − 0.81²⁰ = 1 − 0.0148 = 0.985`.

Now compare the honest player with the attacker. An honest player sends one trade request per trade, so there is no second request to race with, and the rate is effectively zero. Your QA testers also never send two, so they never see it. An attacker sends two on purpose, and even with a race window only 5% of the jitter they succeed within 20 attempts 87% of the time. **A race that never fires under honest load can be a reliable exploit.** Lab 06's threaded stress test fires both trades within 3 ms of each other, with 0.5 ms of simulated work per step. On the lecturer's laptop the naive handler duplicated the sword in 60% to 68% of attempts across runs. The model with `w ≈ 1.2 ms` (two steps of work plus scheduling overhead) and `J = 3 ms` gives `1 − 0.6² = 0.64`.

### The step-through animation

Open the interactive. The top view has two lanes, trade 1 and trade 2, each with three step cards (`R`, `G`, `T`), and a middle panel showing the database: three inventories with the sword drawn where it currently is. Each trade also shows its "copy in memory," which turns amber when it no longer matches the database. Press "Trade 1 step" or "Trade 2 step" to advance either one, or pick an interleaving from the grid below and press play. The sword counter reads 1 until the second give, then 2.

The bottom view is a grid of all 20 interleavings, coloured red for dupe and grey for correct, with the current one outlined. Change the handler selector from "naive" to any fix in section 3, and the grid turns grey, all 20 cells. Replay `112122` under "row lock" and watch trade 2's first step turn into a "waiting for lock" card until trade 1 commits. A third panel has the `w` and `J` sliders and the probability table above.

### Cross-game recognition

The same three steps (read a balance or inventory, credit the other side, write back the stale value) show up far outside games.

**Starbucks gift cards (2015).** Security researcher Egor Homakov found that transferring money between two Starbucks gift cards on the website used a two-step process, set up the transfer and then confirm. By preparing the same $5 transfer in two browser sessions and sending both confirmations at once, he made a $5 card send $5 twice, turning $15 into $20 across his cards. It worked on the sixth attempt. Rewrite it in our model. `R` checks the source balance, `G` credits the target, `T` debits the source from the value read at `R`. Two concurrent confirmations both pass `R`. He also notes the usual failed defenses (rate limits, random delays, transactions used the wrong way) and names a pessimistic lock with `FOR UPDATE` as the correct fix. That is fix 2 below.

**Flexcoin (March 2014).** A small Bitcoin bank shut down after an attacker used its internal transfer feature. By sending thousands of simultaneous transfer requests, the attacker moved coins between accounts before balances updated, overdrew the sending accounts, repeated this across accounts to grow the sum, and withdrew 896 BTC. Same race, higher stakes, and no rollback available, because the coins had left the system.

**RuneScape Classic (7 November 2003), for contrast.** The most famous dupe in RuneScape history was not a race. A player using a third-party client found that the server accepted trade offers of items the player did not own. The client showed a quantity of 0 on the offering side, while the receiving player saw 1. Players spawned party hats and gave them away in Varrock. Jagex offered a lifetime membership to whoever explained the bug, fixed it within a day, and chose not to roll back. Prices of rare items took 11 months to settle, and the purple party hat (players call it pink) went from the most expensive to one of the cheapest. The root cause was trusting the client ([CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md), "Server authority: never trust the client"). No database isolation level would have stopped it.

So dupes have at least three root causes, and you should classify every dupe report before you fix it:

| Root cause | Example | Fix lives in |
|---|---|---|
| Concurrent read-modify-write (a race) | this week's model; Starbucks; Flexcoin | the database access pattern (section 3) |
| Two sides persisted separately, then a crash | week 5's split save | one transaction per transfer |
| The server trusts the client's claim | RuneScape Classic, 2003 | server-side validation |

### Eyes-open design judgment

- **Assume every value-moving path will be raced on purpose.** Test it with two simultaneous requests, not one. Lab 06's stress harness is 40 lines, and any studio can afford one like it.
- **Prefer designs where the race cannot be expressed.** The row model plus a single conditional `UPDATE` has no window at all. Locks and retries are for cases that truly need several steps.
- **Keep a kill switch per path.** New World could disable trading, mail, the trading post and the guild treasury independently. That let the game stay online while the fix was built. Design value-moving features so each can be turned off at runtime.
- **Detect, because prevention will fail somewhere.** EverQuest II caught its 2005 dupe through alarms on the total money supply, within a day. Count total gold and unique-item copies on a schedule and alert on jumps. [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) builds that dashboard, and DB201 weeks 10 to 12 build the pipeline under it.
- **Decide rollback against ban before you need to.** Jagex refused to roll back in 2003. SOE restored the EQ2 economy in 2005. A rollback punishes every innocent player's last hours. Not rolling back leaves duped goods in circulation forever. [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) ("Exploit response: rollback vs ban") treats this choice in depth.
- **Two later courses take other angles on the same bug.** This week counts interleavings. [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) counts expected dupes per day from operation volume and failure rates, and adds idempotent retries and a supply audit. [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) takes the attacker's side, forcing failures at chosen moments.

### Check yourself on the worked example

1. The handler becomes four steps, `R V G T`, where `V` is a slow validation call made after the read. How many interleavings are there, and in how many does the sword duplicate?
2. A race window is 8 ms and requests arrive with 40 ms of jitter. What is the chance per attempt, and how many attempts does an attacker expect to need?
3. A teammate says "our trades are wrapped in `BEGIN ... COMMIT`, so this can't happen." What do you need to know about the isolation level and the code to decide whether they are right?

<details>
<summary>Answers</summary>

1. `C(8, 4) = 70` interleavings. The dupe condition is still "each read before the other's take." A trade's read is its first step and its take is its last, so the only safe interleavings are the two serial ones. `70 − 2 = 68` dupe. A longer handler widens the window in time too.
2. `w / J = 0.2`, so `P = 1 − 0.8² = 0.36` and the expected attempts are `1 / 0.36 ≈ 2.8`.
3. You need the isolation level, and whether the handler reads a value into the application and writes a value computed from it back later. At PostgreSQL's default Read Committed, a `SELECT` followed later by an `UPDATE ... SET items = <value from the SELECT>` still loses updates, so the transaction does not help. At Repeatable Read or Serializable, PostgreSQL aborts the second writer with a serialization error, which is safe only if the code retries properly. With `SELECT ... FOR UPDATE`, or a single conditional `UPDATE`, it is safe at any level.

</details>

## 3. Four ways to make the dupe impossible

Every fix removes the gap between "check" and "act," either by making them one operation or by making sure nobody else can act in the gap. All four fixes make every one of the 20 interleavings correct in Lab 06, and all four drop the stress-test dupe rate to 0%.

### Fix 1: one conditional statement (row model)

Move the sword with a single `UPDATE` whose `WHERE` clause is the check:

```sql
UPDATE items SET owner_id = :receiver
WHERE item_id = 5001 AND owner_id = :giver;
```

The database runs the check and the write as one atomic operation on one row. Whichever trade runs second finds `owner_id` no longer equal to the giver and updates zero rows. The code reads the affected-row count (`cursor.rowcount` in Python) and reports "rejected". Gold works the same way:

```sql
UPDATE characters SET gold = gold - 500
WHERE character_id = :buyer AND gold >= 500;
```

**Cost:** almost none. It needs the row model, where each item is a row, which is one more reason week 2 recommended rows for anything with value. In PostgreSQL, when two such statements hit the same row at once, the second waits for the first to commit and then re-checks its `WHERE` against the new row version. That is why this is safe even at Read Committed. For a full trade (gold both ways, item, log), put the conditional statements in one transaction and roll back if any affects zero rows, as in the week 5 `sell` function.

### Fix 2: lock the row you are about to change (pessimistic)

Keep the multi-step handler but take a lock at the read:

```sql
BEGIN;
SELECT items FROM inventories WHERE character_id = :giver FOR UPDATE;  -- locks the row
-- ... application logic, give to receiver ...
UPDATE inventories SET items = :new_items WHERE character_id = :giver;
COMMIT;                                                                  -- releases the lock
```

`FOR UPDATE` locks the selected rows until the transaction ends. A second trade's `SELECT ... FOR UPDATE` on the same giver waits. When it proceeds, it reads the committed inventory without the sword and rejects. SQLite has no row locks. `BEGIN IMMEDIATE` takes the database's single write lock at the start of the transaction, which has the same effect for this example at the cost of blocking every other writer.

**Cost:** waiting, and deadlocks (section 4). Hold locks for as short a time as possible. Never hold one across a network call to a client.

### Fix 3: check the version when you write (optimistic)

Add a `version` column. Read it with the inventory. Make the write conditional on it being unchanged:

```sql
UPDATE inventories SET items = :new_items, version = version + 1
WHERE character_id = :giver AND version = :version_read;
```

If another trade wrote first, the version moved, zero rows update, and this trade reports a conflict and gives nothing. Order matters here. Do the conditional take *before* the give, or inside the same transaction as the give, so a failed take cannot leave a gift already delivered. Lab 06's `versioned_trade` rejects trade 2 in every interleaving.

**Cost:** retries under contention. With little contention, as with most trades, it is cheaper than locking because nobody waits. When many requests hit one row at once, for example a guild bank during a raid payout, many of them fail and retry, and a lock is better.

### Fix 4: serializable isolation, with retries

PostgreSQL's `SERIALIZABLE` level promises that concurrent transactions produce the same result as some serial order. It tracks read and write dependencies and aborts a transaction that would break that promise, with SQLSTATE `40001` ("serialization failure"). At `REPEATABLE READ`, PostgreSQL already aborts our naive handler's second `T` with "could not serialize access due to concurrent update", because it tries to modify a row that another transaction changed after its snapshot.

**Cost:** you must catch `40001` and rerun the *whole* transaction, including the reads, and every code path must do this correctly. The PostgreSQL documentation calls this a generalized way of handling serialization failures, and in return the application needs no explicit locks. It is the strongest option and the one whose failure mode, forgetting a retry, is easiest to miss in review.

### Safety nets that catch what slips through

- **Unique keys.** In the row model, `item_id` is the primary key, so a second copy of sword 5001 cannot exist as a second row. That turns some dupes into an error. The row model does not catch a stackable dupe, where one row's quantity goes from 5 to 10.
- **Audit queries.** Run `SELECT SUM(gold) FROM characters` and per-type item counts on a schedule. Compare them with the logged faucets and sinks. Alert on unexplained jumps.
- **Trade logs.** Week 5's `trade_log` row, written in the same transaction, is what lets you trace every copy of an item back to its source after the fact.

## 4. Deadlocks and lock ordering

Locks create a new failure. Two players trade with each other, A giving a sword to B and B giving gold to A. The handler locks "my side first":

```
Trade X (started by A):  lock A ... then lock B      (waits for Y)
Trade Y (started by B):  lock B ... then lock A      (waits for X)
```

Each holds one lock and waits for the other's. Neither can move. That is a **deadlock**. PostgreSQL detects it after waiting `deadlock_timeout` (1 second by default) and aborts one transaction with an error, so nothing corrupts. But a player waited a second and then saw a failed trade.

The fix is to acquire locks in a single global order. Lock the lower `character_id` first, always:

```sql
SELECT character_id FROM characters
WHERE character_id IN (:a, :b)
ORDER BY character_id
FOR UPDATE;
```

Now both trades try to lock the lower id first. One gets it, the other waits at the first lock while holding nothing, and no cycle can form. The PostgreSQL documentation gives the same advice. It calls a consistent lock order the best defense against deadlocks. The same idea shows up in CS courses as resource ordering for the dining philosophers. For multi-party actions, such as a five-player loot split, sort all participants by id and lock in that order.

## 5. Isolation levels, summarized for this bug

| Level | PostgreSQL | Naive read-modify-write in one transaction | Where it is the default |
|---|---|---|---|
| Read Committed | each statement sees data committed before it began | **dupes**: the stale write-back succeeds | PostgreSQL |
| Repeatable Read | one snapshot for the whole transaction | second writer aborted ("could not serialize access"), retry needed | — |
| Serializable | as if run one at a time; aborts with `40001` | second transaction aborted, retry needed | — |
| SQLite, inside `BEGIN ... COMMIT` | one writer at a time | safe, but writers queue behind each other | SQLite (serializable by design) |
| SQLite, autocommit per statement | each statement is its own transaction | **dupes** (Lab 06's naive handler) | Python's `sqlite3` if you never open a transaction |

Read the last row carefully. SQLite is serializable only within a transaction. Lab 06's naive handler dupes on SQLite because each `load` and `save` commits separately, so there is no transaction for the isolation to apply to.

## In-class activity (25 minutes)

Work in pairs with the printed step cards (or the interactive in "manual" mode).

1. Play three interleavings of the naive trade, `121212`, `211122` and `111222`, by moving the sword token between three inventory cards and keeping each trade's stale copy on a sticky note. Record the final sword count for each.
2. A guild bank handler withdraws gold with `bal = SELECT gold ...; if bal >= amt: UPDATE ... SET gold = bal - amt; give amt to member`. The bank holds 1,000 gold and two members each withdraw 1,000 at once. Write the interleaving that lets both succeed and state how much gold the world gained.
3. Rewrite the guild bank handler with fix 1 and with fix 2. For each, say what the second member sees.
4. A raid of 25 players all withdraw from the guild bank within the same second after a boss kill. Which of fixes 2 and 3 do you choose, and why?

Expected output: three sword counts, the guild bank interleaving with the gold created (1,000), two rewritten handlers, and a one-paragraph choice for step 4.

## Common misconceptions

- **"Wrapping the handler in a transaction fixes it."** Not at Read Committed, PostgreSQL's default, when the application reads a value and writes it back later. Use a conditional update, `FOR UPDATE`, or a stricter level with retries.
- **"It is too rare to matter; we never saw it in testing."** Testers send one request at a time. An attacker sends two on purpose, and at `w / J = 0.05` succeeds within 20 tries 87% of the time.
- **"Take before give fixes the race."** It changes a crash's failure from dupe to loss (week 5). It shortens the race window, from 18 dupes in 20 interleavings to 12, but never closes it.
- **"Rate limits or random delays will stop it."** They change `J` and the number of attempts, not whether a dupe is possible. Homakov lists both among the poor protections he routinely got past.

## Check yourself

1. Trace `212121` for the naive handler. List the giver's inventory after each step and the final sword count.
2. Two requests have a race window of 2 ms and jitter of 100 ms. What is the chance per attempt, and the chance of at least one dupe in 100 attempts?
3. Write the single SQL statement that sells a potion stack of quantity 5 from character 10 to character 11 in the row model, failing safely if character 10 no longer owns it. What does the application check afterwards?
4. Trade X locks characters 7 then 3. Trade Y locks 3 then 7. Can they deadlock? Rewrite the rule so they cannot.
5. A dupe report says "players who log out during a trade window keep their item and the buyer gets one too." Classify the root cause with the section 2 table, and name the fix.

<details>
<summary>Answers</summary>

1. `R2` reads [5001]. `R1` reads [5001]. `G2` gives to char 3, giver still [5001]. `G1` gives to char 2, giver still [5001]. `T2` writes giver = []. `T1` writes giver = [] from its stale copy. Final: char 2 and char 3 each hold 5001, two swords.
2. `w / J = 0.02`, `P = 1 − 0.98² = 0.0396`. At least one in 100 attempts is `1 − (1 − 0.0396)¹⁰⁰ = 1 − 0.0176 ≈ 0.98`.
3. `UPDATE items SET owner_id = 11 WHERE item_id = :potion_id AND owner_id = 10 AND quantity = 5;` The application checks that `rowcount == 1`. If it is 0, the item moved or its quantity changed, and the trade is rejected.
4. Yes. X holds 7 and waits for 3, while Y holds 3 and waits for 7. Rule: always lock the lower id first, so both lock 3 then 7.
5. Logging out mid-trade suggests the two sides were saved at different moments (the logout save writes the giver's stale state, or the receiver's side was already saved). That is the week 5 split save, a crash-like persistence split rather than a pure race. Fix it by committing both sides of the trade in one transaction when the trade completes, and by making sure the logout save cannot overwrite rows the trade transaction changed (fix 3's version check does that).

</details>

## Lab / assignment hook

[Lab 06, reproduce the dupe, then make it impossible](../labs/lab06.md). You run all 20 interleavings of the naive trade against SQLite, trace one step by step, stress it with real threads, and implement three fixes (conditional update, lock, version check) that must pass all 20 interleavings and the stress test with zero dupes. Deliverable: the completed `dupe_lab.py`, your interleaving table, and a one-page incident note classifying a dupe report. This lab counts toward the SQL labs (40%) and is the core of the final inventory service.

## Sources

- NWDB, "All Forms of Trading Disabled Due to Coin Duplication Exploits" (2 November 2021), quoting the New World community manager's forum post; NME, "'New World' disables 'all forms' of wealth transfers to combat gold exploit" (2 November 2021). New World at launch (released 28 September 2021): sending currency, guild treasury, trading post and player-to-player trading disabled; bans announced. Neither source describes the exploit's mechanism. https://nwdb.info/news/all-forms-of-trading-disabled-due-to-coin-duplication-exploits
- Wikipedia, "New World (video game)" (read September 2026). Worldwide release on 28 September 2021.
- Terdiman, D., "Cheaters slam 'Everquest II' economy", CNET News.com via ZDNet, 11 August 2005 (Internet Archive copy). A duplication bug raised EQ2's money supply by about 20% in 24 hours; alarms; attempted sales on Station Exchange; economy restored. https://web.archive.org/web/2006/http://news.zdnet.com/2100-1040_22-5829403.html
- Homakov, E., "Hacking Starbucks for unlimited coffee", Sakurity blog, 21 May 2015. The two-session race on gift-card transfers, success on the sixth attempt, and `FOR UPDATE` named as the fix. https://sakurity.com/blog/2015/05/21/starbucks.html
- Flexcoin shutdown notice, 3 and 4 March 2014 (Internet Archive copy of flexcoin.com). 896 BTC taken; simultaneous transfer requests overdrew accounts before balances updated. https://web.archive.org/web/2014/http://www.flexcoin.com/
- RuneScape Wiki, "Partyhat duplication glitch" and "Purple partyhat" (RuneScape Classic, 7 November 2003). Item spawning through a third-party client in trades, the membership reward, no rollback, 11 months for prices to settle. https://runescape.wiki/w/Partyhat_duplication_glitch
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 7, "Preventing Lost Updates" (atomic writes, explicit locking, compare-and-set), "Write Skew and Phantoms".
- PostgreSQL 18 documentation (September 2026): section 13.2 "Transaction Isolation" (Read Committed default; Repeatable Read's "could not serialize access due to concurrent update"; Serializable and SQLSTATE 40001); section 13.3 "Explicit Locking" (`FOR UPDATE`; acquiring locks in a consistent order); section 19.12 "Lock Management" (`deadlock_timeout` default 1 s). https://www.postgresql.org/docs/current/
- SQLite, "Transaction" (`BEGIN IMMEDIATE`). https://www.sqlite.org/lang_transaction.html
- Lab 06 measurements: DB201 lecturer's machine, Apple silicon, macOS, Python 3.13.5, SQLite 3.53.3, September 2026. Stress-test dupe rate varies between runs (60% to 68% observed).

## Interactive spec: examples/w06-trade-dupe-stepper.html

**The one insight.** Two trades that are each correct on their own duplicate the sword in 18 of the 20 ways their steps can interleave, because each writes back a stale copy of the giver's inventory. Every fix removes the gap between check and write, and the whole grid turns safe. The step-through must make the stale copy visible, because it is the bug.

**Layout.** Three stacked sections (stacked at all widths; on screens ≥ 1100px the step view and the grid sit side by side, with the timing panel full width below).

- **Step view, "Two trades, one sword."** Two lanes, "Trade 1 → Bram" and "Trade 2 → Cyra", each with three cards `R` (read giver), `G` (give), `T` (take). Card states are pending, current, done, waiting-for-lock (fix 2 only) and rejected. Between the lanes, a "Database" panel with three inventory cards (Giver, Bram, Cyra), each showing a generic sword shape if it holds item 5001. Under each lane, "Trade N's copy of the giver's inventory," which is empty until its `R` runs. It shows the list read at `R` and turns amber with the label "stale" whenever it differs from the Giver card. A large counter "Swords in the world: N" (N = 1 neutral, 2 alert labelled "DUPE"). A text log lists each executed step in words, for example "T2: write giver = [] (from stale copy)".
- **Grid, "All 20 interleavings."** A 4 × 5 grid of buttons labelled with the order string (`111222` ... `222111`, lexicographic order). Each is coloured by the outcome under the selected handler: red "dupe", grey "ok (one rejected)" or "ok". The current order is outlined. Clicking a cell loads it into the step view, reset to step 0. A summary line reads "Dupes: 18 of 20" for the naive handler (12 of 20 for `R T G`, 0 of 20 for the fixes).
- **Timing panel, "How often does it fire?"** Sliders for the race window `w` (0.1 to 50 ms, step 0.1, default 5) and the jitter `J` (1 to 200 ms, step 1, default 50), plus attempts `n` (1 to 100, default 20). Readouts: `w/J`, `P` per attempt, expected attempts `1/P`, and `P(at least one in n)`. A small bar chart of `P(at least one in k)` for `k = 1..n`. If `w > J`, clamp `P` to 1 and show the note "window longer than jitter: every attempt overlaps."

**Controls.** All keyboard reachable; visible focus.
- Buttons "Trade 1 step" and "Trade 2 step" (disabled when that trade is finished; under fix 2, pressing a step for a trade blocked on the lock shows the waiting card and advances nothing).
- Buttons "Play" / "Pause" (auto-steps the loaded order, one step per 900 ms; with reduced motion, step instantly per press only), "Reset".
- Handler selector (radio group): "Naive (read, give, take)", "Naive, take before give (R T G)", "Fix 1: conditional UPDATE (row model)", "Fix 2: row lock (FOR UPDATE)", "Fix 3: version check", "Fix 4: serializable with retry".
- Keyboard: `1` and `2` step the trades; arrow keys move within the grid.

**Semantics per handler (must match Lab 06).**
- Naive `R G T`: `R` copies the Giver list into the trade's copy; if 5001 is absent, the trade is rejected at `R` and its remaining cards grey out. `G` appends 5001 to the receiver. `T` sets Giver to the copy minus 5001.
- Naive `R T G`: same operations, with `T` before `G`. The grid shows 12 of 20 dupes; the safe orders are the serial two plus the six where one trade reads and takes before the other reads.
- Fix 1: a single card `M` (move) per lane replaces `R G T`. It succeeds if Giver holds 5001 (the card moves it to the receiver) and is rejected otherwise. Map the order string to steps by skipping turns of a finished trade.
- Fix 2: at `R`, the trade takes the lock if free; otherwise its card shows "waiting for lock" and the turn passes to the other trade (the step does not advance). The lock is released after `T`. The second trade then reads the committed Giver list (without the sword) and is rejected.
- Fix 3: `R` also reads a version number (shown on the Giver card, starting at 0). The order is `R T G`, and `T` succeeds only if the version is unchanged (then version + 1). Otherwise it is marked "conflict" and `G` never runs.
- Fix 4: behaves like Naive until the second trade's `T`, which is shown aborting with "40001, retry". The retry replays from `R`, reads the committed Giver list, and is rejected.

**Test values (must match exactly).**
- Naive `R G T`: dupes in 18 of 20. The safe orders are exactly `111222` and `222111`.
- Trace of `112122` (naive): after each step Giver/Bram/Cyra are `[5001]/[]/[]`, `[5001]/[5001]/[]`, `[5001]/[5001]/[]` (trade 2's copy = [5001]), `[]/[5001]/[]` (trade 2's copy now stale), `[]/[5001]/[5001]`, `[]/[5001]/[5001]`. Final count 2.
- Trace of `212121` (naive): final Giver `[]`, Bram `[5001]`, Cyra `[5001]`, count 2.
- Naive `R T G`: 12 of 20. Dupes are exactly the orders starting `12` or `21`; `112122` is safe.
- Fixes 1 to 4: 0 of 20. Under fix 3, `121122` shows trade 2 "conflict".
- Timing: `w = 5, J = 50` gives `w/J = 0.100`, `P = 0.190`, `1/P = 5.3`, `P(≥1 in 20) = 0.985`. `w = 2, J = 100, n = 100` gives `P = 0.0396`, `P(≥1 in 100) = 0.982`. `w = 8, J = 40` gives `P = 0.360`, `1/P = 2.8`.

**Visual rules.** Use `templates/interactive-tokens.css` inline. Generic shapes only (a simple sword silhouette drawn in SVG); no game art or logos. Respect `prefers-reduced-motion` (no card slide animations; instant state changes) and `prefers-color-scheme`. Do not rely on colour alone: dupe cells also carry a "×2" label and stale copies the word "stale". No horizontal overflow at 390px; the 4 × 5 grid may become 4 columns of smaller buttons.
