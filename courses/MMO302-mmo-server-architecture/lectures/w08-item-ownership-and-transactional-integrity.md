# MMO302 · Week 08 — Item ownership and transactional integrity

**Why this matters:** Every duplication exploit in MMO history comes down to a moment when an item or a pile of gold was in two places at once, or in one place twice. On a shard doing two million item moves a day, a failure that happens once in ten thousand operations is 200 incidents a day. This week you learn to count them before launch and to design moves that cannot produce them, even when servers crash and clients retry.

**You will be able to:**
- Compute the expected daily dupes, losses and double-applied operations for a given transfer design, from the operation count and two failure rates.
- Design item storage so every item has exactly one owner at every moment, and write a transfer that is atomic and idempotent in SQL.
- Write a conservation audit (supply equals minted minus destroyed, over every container) and compute how fast it detects a dupe exploit.
- Critique a cross-server item flow (mail, auction house, cross-realm trade) by finding the step where a crash or retry breaks conservation.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 7, "Transactions", the sections on atomicity and "Preventing Lost Updates". Stripe API reference, "Idempotent requests" (docs.stripe.com, one page). Reread your notes on DB201 weeks 5 and 6.

**Prerequisites from earlier courses:** [DB201 week 5, transactions and ACID](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md), and [DB201 week 6, race conditions and the duplication bug](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md), whose worked example steps through the interleavings of two concurrent trades on one database. This lecture does not repeat that trace. It takes the fleet's view instead: how many dupes a day a shard makes from its operation volume and failure rates when servers crash between writes and clients retry, and how idempotency keys and a supply audit catch them. It assumes you can write `BEGIN ... COMMIT` and explain atomicity. [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (the client asks, the server decides). [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) and [MMO304 week 4, money supply](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (what extra gold does to prices). [MMO302 week 7](w07-persistence-strategies-write-through-periodic-event-sourcing.md) (the event log and per-state persistence policy).

**Interactive:** [examples/w08-ledger-drift.html](../examples/w08-ledger-drift.html). Keep it open during section 2.

---

## 1. One item, one owner

Start with the rule this whole lecture defends.

**At every moment, every item has exactly one owner, and every unit of currency is counted in exactly one container.**

An **owner** or **container** is anything that can hold an item: a character's bag slot, a bank, a guild vault, a mail waiting to be opened, an auction listing, a trade window, the ground under a dead monster. Currency is the same idea for things that stack: 500 gold is held by one wallet, one mail or one escrow account, never by two.

A **dupe** breaks the rule upward: an item exists in two containers, or a container's gold went up without any other container going down. A **loss** breaks it downward: the item left one container and never arrived in another. Players report losses loudly and dupes quietly, because the person who gets a free item rarely files a ticket.

### Model items as rows with one owner column

The storage model decides how easy the rule is to keep. Compare two designs for a unique item such as a sword.

- **Copy between inventories.** Each character has an inventory table and the sword is a row in Ayla's. A trade inserts a copy into Bren's inventory and deletes the row from Ayla's. The rule holds only if both statements take effect together, and any crash between them breaks it.
- **One row, one owner.** The sword is one row in an `item` table with a globally unique `item_id` and an `owner_container_id` column. A trade is `UPDATE item SET owner_container_id = :bren_bag WHERE item_id = :sword`. There is only ever one row, so there can only ever be one sword. Setting the owner a second time to the same value changes nothing.

The second design makes the most common dupe impossible by construction, because you cannot copy a row you only ever update. It also makes the move **idempotent**, meaning that doing it twice has the same effect as doing it once. That property will matter a great deal once retries enter the picture.

Stackable items and currency are harder, because they are counters. `gold = gold - 300` done twice takes 600. Counters need the transaction and idempotency tools of section 3.

### Where item IDs come from

A unique `item_id` must be unique across every server that can create items, forever. Three common schemes:

- A database sequence (`BIGSERIAL` in PostgreSQL). Simple, and every creation needs a database round trip, which is fine for rare drops and awkward for a crafting system that makes 10,000 arrows a minute.
- **Block allocation.** Each world server reserves a block of IDs (say 100,000 at a time) from the database and hands them out from memory. A crash wastes the rest of the block, which costs nothing because IDs are cheap.
- 64-bit IDs built from a server number, a timestamp and a counter, so servers never coordinate. Collisions are impossible as long as server numbers are unique and clocks do not run backwards.

Never reuse an ID. An audit that finds item 88,213 in two places must be able to say "this is a dupe" with certainty, not "maybe one of them is a recycled number".

## 2. Worked example: counting dupes before they happen

### The hook

In August 2005 a group of EverQuest II players found a duplication bug and used it to create platinum, the game's currency. According to Sony Online Entertainment's public relations director, the amount of money in the game rose by about a fifth in roughly 24 hours. The exploiters tried to sell the platinum through Station Exchange, the official real-money marketplace SOE had launched the month before. SOE said it had "a lot of alarms" for this kind of thing, that they all went off, and that the economy was brought back to its pre-exploit state.

Two facts in that story are worth your attention as a server engineer. First, the dupe existed at all, on a shipped game from an experienced studio. Second, SOE caught it within about a day because it had alarms on the money supply. This worked example builds both halves: a model that predicts how many dupes a design produces, and the audit that catches the ones you missed.

### The model

Picture a shard that performs `M` value-moving operations per day. Trades, mail claims, auction-house sales, bank deposits and quest rewards all count. Each operation is two writes: take from a source, give to a destination. Two things go wrong, at small rates.

- `f`, the probability that the operation stops **between** its two writes. The zone server crashes, the process is killed during a deploy, a timeout aborts the handler halfway.
- `a`, the probability that the operation **completes**, but the reply never reaches whoever asked (the client, or another service). The caller cannot tell success from failure, so it retries.

Four designs, from worst to best.

1. **Two separate writes, give first.** Credit Bren, then debit Ayla. A stop in between leaves both holding the value: a **dupe**.
2. **Two separate writes, take first.** Debit Ayla, then credit Bren. A stop in between leaves neither holding it: a **loss**.
3. **One transaction.** Both writes commit together or not at all. A stop in between rolls back cleanly. But a retry after a lost reply runs the whole operation again.
4. **One transaction plus idempotency.** The operation carries a unique ID, and the transaction records it. A retry with the same ID finds it already applied and returns the original answer without doing anything.

Expected incidents per day:

```
half-done operations         = M × f       → dupes (design 1) or losses (design 2), 0 in designs 3 and 4
retried completed operations = M × a       → applied twice in designs 1, 2 and 3, 0 in design 4
```

"Applied twice" means different things for different operations. If the source is another player, gold is conserved but the sender paid twice, which is a support ticket. If the source is a mail, a reward table or an escrow that should empty after one use, and nothing marks it used, the second application creates value from nothing. That is a dupe.

### Numbers you can check

Take `M = 2,000,000` operations per day, `f = 1` in 10,000 and `a = 1` in 5,000. These are invented, but a real shard with tens of thousands of daily players and a bad deploy week can exceed them.

| Design | Half-done per day | Outcome | Retried per day | Outcome |
|---|---|---|---|---|
| 1. Separate writes, give first | 200 | 200 dupes | 400 | 400 applied twice |
| 2. Separate writes, take first | 200 | 200 losses | 400 | 400 applied twice |
| 3. One transaction | 0 | none | 400 | 400 applied twice |
| 4. Transaction + idempotency | 0 | none | 400 | none (replayed answer) |

Check the arithmetic: `2,000,000 / 10,000 = 200` and `2,000,000 / 5,000 = 400`.

Notice the order of writes in designs 1 and 2. Changing the order does not fix anything. It only picks the direction of the error: dupes that quietly inflate the economy, or losses that fill the support queue. Many teams pick "take first" for exactly that reason, since a loss is visible and refundable while a dupe spreads. Only atomicity removes half-done operations, and only idempotency removes double application.

### The accidental rate is not the real rate

200 dupes a day at an average of 250 gold is 50,000 gold. On a shard with 400 million gold in circulation that is 0.0125% a day, far too small to notice in the price of anything. So why did EverQuest II's supply jump 20% in a day?

Because players do not wait for accidents. Once someone learns how to cause the failure on purpose (disconnecting at the right moment, crashing a zone with a known bug, sending a request twice), `f` for that player is no longer 1 in 10,000. It is close to 1. Suppose 10 exploiters each trigger one dupe every 30 seconds, duplicating a stack worth 10,000 gold each time.

```
10 players × 120 dupes per hour × 10,000 gold = 12,000,000 gold per hour
12,000,000 / 400,000,000 = 3% of the money supply per hour
```

Left alone for 24 hours, that is 288 million gold, a 72% increase. The design question is never "how rare is the failure?" It is "can a player make it happen?" If yes, the rare-failure numbers are irrelevant. Design 3 stops the half-done dupe, but a player who can force a retry against a one-time source (a mail, a reward) still gets it applied twice. Only design 4 is safe.

### The audit: supply equals minted minus destroyed

Designs fail and exploits get found. The second line of defence is a **conservation audit**. Every faucet (monster loot, quest rewards, vendor sales) and every sink (repair costs, vendor purchases, auction fees) writes a ledger row when it creates or destroys currency. Then, at any time:

```
expected supply(t) = supply(0) + minted(0..t) − destroyed(0..t)
actual supply(t)   = Σ over every container of the gold it holds
drift(t)           = actual supply(t) − expected supply(t)
```

In a correct system, drift is exactly zero, not "about zero". Positive drift means value was created without a faucet, which is a dupe. Negative drift means value vanished without a sink, which is a loss. The words "every container" carry the weight. If mail in transit, auction escrow and open trade windows are left out of the sum, drift wobbles with every trade in flight, you have to add a tolerance, and a small dupe hides inside it.

With an hourly audit and an alarm at any nonzero drift, the exploit above trips the alarm at the first audit, with 12 million gold of drift. The accidental 200-a-day dupes of design 1 trip it too, with `50,000 / 24 = 2,083` gold of drift in the first hour. That figure assumes every retried operation moves gold between two players, so a double application only shifts gold between wallets. If half the retries instead draw from a one-time source such as mail or a quest reward (the interactive's default share of 50%), the 400 retries add 200 more dupes a day and the first-hour drift is `100,000 / 24 = 4,167` gold. Even a small, exact audit catches a slow leak.

Star Wars Galaxies found a currency dupe this way. Its designers compared the money created with the money destroyed and saw that more was leaving the system than entering. Yet the world had no shortage of money. The only explanation was money arriving from somewhere the ledger did not know about.

### Seeing it move

Open the interactive. The left view is three players' wallets as they trade, each bar moving up and down. Every individual wallet looks fine; nothing on this side reveals anything wrong. The right view plots two lines over a simulated day: expected supply (from the ledger) and actual supply (the sum of every container). Choose design 1 and raise `f`. The lines separate. Switch to design 4 and they stay welded together. Now turn on "exploiter" and watch actual supply climb away from the ledger while each wallet on the left still looks normal. That is the point of the audit. No single player's view shows a dupe, and only the global sum does.

### Cross-game recognition

**EverQuest II (August 2005).** A dupe raised the money supply by about 20% in a day. SOE detected it with automated alarms on the total money in the game and restored the economy. This is the audit of this section, run continuously.

**Star Wars Galaxies (2004, as described by its creative director Raph Koster).** The designers found a dupe by comparing money created and money destroyed. The ledger said the economy was shrinking while players had plenty of cash. This is the `drift` line, computed by hand.

**TrinityCore (World of Warcraft 3.3.5 server emulator).** Taking gold from a mail changes two containers, the player's wallet and the mail. The handler saves both inside one database transaction, with a source comment saying it does so to prevent cheating. A completed trade saves both players' inventories and gold in one transaction too. That is design 3 applied to exactly the operations players try to exploit. It is worth reading one detail closely: the handler updates the in-memory state and sends the success reply first, and commits afterwards. A crash in between rolls back both the wallet and the mail together. The player loses the claim, but the gold cannot exist twice.

**Stripe (payments API, current).** A payment API faces the same retry problem with real money. Stripe lets the client send an `Idempotency-Key` header. The server saves the status code and body of the first request made with that key and returns the saved response for any retry with the same key, even if the first attempt failed. It also rejects a retry whose parameters differ from the original. That is design 4, and Stripe keeps keys for at least 24 hours before pruning them.

Four systems, two tools. Atomicity keeps an operation from being half done. Idempotency keeps it from being done twice. The audit catches whatever the first two missed.

### Eyes-open design judgment

- **Make the dangerous operations impossible, not unlikely.** A 1-in-10,000 race is a certainty for someone who can trigger it. Put every value move in one transaction, and give every retryable request an ID.
- **Prefer storage where the natural operation is idempotent.** "Set owner to Bren" can be repeated safely. "Add 300 gold" cannot. Where you must use counters, add a guard: a conditional update (`WHERE claimed = 0`) or an operation-ID table.
- **Pick the failure direction on purpose.** Where atomicity is truly impossible (a flow across two systems you do not control), order the steps so a stop causes a loss you can see and refund, never a dupe you cannot see.
- **Count every container in the audit.** Mail, escrow, trade windows, guild banks, the ground. A tolerance hides a slow dupe. An exact audit catches it.
- **Plan the response before you need it.** Rollback of the whole shard, targeted removal of duped items, or bans. Each has costs to honest players, and MMO309 treats the choice in depth. An event log from week 7 makes the targeted options possible, because you can trace every duped item back to its origin.

### Check this example

1. A shard does 5 million operations a day with `f` = 1 in 50,000 and `a` = 1 in 20,000, using design 3. How many operations are applied twice per day?
2. An exploit duplicates 2,000 gold every 10 seconds for one player. The shard has 150 million gold. How long until drift passes 0.5% of supply?
3. A developer "fixes" design 1 by swapping to design 2. What happens to the drift line on the audit, and who notices first?

<details>
<summary>Answers</summary>

1. Half-done: `5,000,000 / 50,000 = 100`, all rolled back, so zero incidents. Retried: `5,000,000 / 20,000 = 250` applied twice.
2. The exploit adds `2,000 × 360 = 720,000` gold per hour. 0.5% of 150 million is 750,000, so about 1.04 hours, just over an hour.
3. Drift turns negative instead of positive, at the same rate. The players whose items vanished notice first, and they file tickets. The audit sees it at the same moment it would have seen the dupes.

</details>

## 3. Atomic and idempotent in SQL

Here is the mail-claim case from the TrinityCore example, written twice against SQLite so you can run it. The naive version gives the gold and then marks the mail claimed, as two separate commits. The atomic version does both in one transaction, and it marks the mail claimed with a conditional update, which makes the claim naturally idempotent. Each version is run with a crash injected between its two writes, followed by the client's retry and a second, impatient retry.

```python
import sqlite3

class Crash(Exception):
    pass

def fresh():
    db = sqlite3.connect(":memory:", isolation_level=None)  # we control transactions
    db.executescript("""
        CREATE TABLE wallet (player TEXT PRIMARY KEY, gold INTEGER NOT NULL);
        CREATE TABLE mail (id INTEGER PRIMARY KEY, player TEXT, gold INTEGER, claimed INTEGER);
        INSERT INTO wallet VALUES ('ayla', 100);
        INSERT INTO mail VALUES (7, 'ayla', 500, 0);
    """)
    return db

def supply(db):  # every container that can hold gold, mail included
    w = db.execute("SELECT SUM(gold) FROM wallet").fetchone()[0]
    m = db.execute("SELECT SUM(gold) FROM mail WHERE claimed = 0").fetchone()[0] or 0
    return w + m

def claim_naive(db, mail_id, crash=False):
    player, gold, claimed = db.execute(
        "SELECT player, gold, claimed FROM mail WHERE id = ?", (mail_id,)).fetchone()
    if claimed:
        return "already claimed"
    db.execute("UPDATE wallet SET gold = gold + ? WHERE player = ?", (gold, player))
    if crash:
        raise Crash()           # the process dies between the two writes
    db.execute("UPDATE mail SET claimed = 1 WHERE id = ?", (mail_id,))
    return "ok"

def claim_atomic(db, mail_id, crash=False):
    db.execute("BEGIN")
    try:
        cur = db.execute("UPDATE mail SET claimed = 1 WHERE id = ? AND claimed = 0", (mail_id,))
        if cur.rowcount == 0:
            db.execute("ROLLBACK")
            return "already claimed"
        player, gold = db.execute("SELECT player, gold FROM mail WHERE id = ?", (mail_id,)).fetchone()
        db.execute("UPDATE wallet SET gold = gold + ? WHERE player = ?", (gold, player))
        if crash:
            raise Crash()
        db.execute("COMMIT")
        return "ok"
    except Crash:
        db.execute("ROLLBACK")  # what recovery does to an uncommitted transaction
        raise

for name, claim in [("naive", claim_naive), ("atomic", claim_atomic)]:
    db = fresh()
    before = supply(db)
    try:
        claim(db, 7, crash=True)
    except Crash:
        pass
    retry = claim(db, 7)        # the client never got an answer, so it asks again
    again = claim(db, 7)        # and a second, impatient retry
    gold = db.execute("SELECT gold FROM wallet WHERE player = 'ayla'").fetchone()[0]
    print(f"{name:6}  retry: {retry:15}  again: {again:15}  wallet: {gold}  supply {before} -> {supply(db)}")
```

It prints:

```
naive   retry: ok               again: already claimed  wallet: 1100  supply 600 -> 1100
atomic  retry: ok               again: already claimed  wallet: 600  supply 600 -> 600
```

Read the naive line. Ayla started with 100 gold and a 500-gold mail, so 600 in total. After the crash and one retry she has 1,100, and the supply audit shows 500 gold that no faucet created. That is design 1, and the audit line is the drift. The atomic line ends at 600, as it should. Note one detail: the conditional `UPDATE ... WHERE claimed = 0` does the "already used?" check and the "mark used" step in one statement, so two retries racing each other cannot both see `claimed = 0`. Checking with a `SELECT` first and updating second, as the naive version does, leaves a gap between the check and the write, and two concurrent requests can both pass the check. [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) steps through that race frame by frame.

### When the operation is not naturally idempotent

A player-to-player gold transfer has no "claimed" flag to flip. For those, record the operation ID in the same transaction as the effect. A primary key on the ID turns a duplicate into an error you can catch.

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)
db.executescript("""
    CREATE TABLE wallet (player TEXT PRIMARY KEY, gold INTEGER NOT NULL CHECK (gold >= 0));
    CREATE TABLE applied_op (op_id TEXT PRIMARY KEY, result TEXT NOT NULL);
    INSERT INTO wallet VALUES ('ayla', 1000), ('bren', 0);
""")

def transfer(op_id, src, dst, amount):
    db.execute("BEGIN")
    try:
        db.execute("INSERT INTO applied_op VALUES (?, 'ok')", (op_id,))
    except sqlite3.IntegrityError:   # this op_id already ran: replay its answer
        db.execute("ROLLBACK")
        return db.execute("SELECT result FROM applied_op WHERE op_id = ?", (op_id,)).fetchone()[0] + " (replayed)"
    try:
        db.execute("UPDATE wallet SET gold = gold - ? WHERE player = ?", (amount, src))
        db.execute("UPDATE wallet SET gold = gold + ? WHERE player = ?", (amount, dst))
    except sqlite3.IntegrityError:   # CHECK refused an overdraft
        db.execute("ROLLBACK")       # never leave the transaction open
        db.execute("INSERT INTO applied_op VALUES (?, 'insufficient')", (op_id,))
        return "insufficient"
    db.execute("COMMIT")
    return "ok"

print(transfer("trade-8841", "ayla", "bren", 300))  # commits, but say the reply is lost
print(transfer("trade-8841", "ayla", "bren", 300))  # client retries with the same key
print(transfer("trade-8842", "ayla", "bren", 900))  # more than ayla holds
print(transfer("trade-8842", "ayla", "bren", 900))  # retry replays the refusal
print(dict(db.execute("SELECT player, gold FROM wallet")))
```

It prints:

```
ok
ok (replayed)
insufficient
insufficient (replayed)
{'ayla': 700, 'bren': 300}
```

Three details make this correct. The ID row and the gold moves commit together, so there is no state where the gold moved but the ID was not recorded, or the reverse. The `CHECK (gold >= 0)` constraint makes the database refuse an overdraft even if the game server's own check has a bug, and the `except` branch rolls back so the refused transfer never leaves a transaction open on the connection. It then records the refusal under the ID, so a retry replays "insufficient" instead of trying again. And the ID comes from the caller, generated once per player intent (one click on "accept trade"), not once per network attempt. If the client generates a fresh ID on each retry, the table cannot tell a retry from a new trade.

In PostgreSQL the same pattern is `INSERT ... ON CONFLICT (op_id) DO NOTHING RETURNING op_id`: if nothing is returned, the operation already ran. Keep the `applied_op` table small by deleting rows older than your longest retry window, which is what Stripe's 24-hour pruning does.

## 4. When the item crosses servers

Everything so far assumed one database transaction could cover the whole operation. In an MMO that is often false. The mail system, the auction house and cross-realm trading may be separate services, and week 4's zone servers each own their own players in memory. A transaction cannot span two services' memory.

### Escrow in steps

The standard answer is to break the flow into steps, each of which is one local transaction, with an intermediate container that owns the item in between. That container is called **escrow**. An auction-house sale runs like this:

1. **List.** One transaction on the world database moves the sword from Ayla's bag to the container `auction:5512` and records operation `list-5512`.
2. **Buy.** One transaction moves Bren's 900 gold into `auction:5512`'s escrow and marks the auction sold, conditional on it being unsold. Operation `buy-5512`.
3. **Settle.** One transaction moves the sword to Bren's mail and the gold, minus the house fee (a sink, logged in the ledger), to Ayla's mail. Operation `settle-5512`.

Each step is atomic and idempotent. A crash between steps leaves the sword and the gold in a real container, `auction:5512`, which the audit counts. A settlement job that restarts simply finds sold-but-unsettled auctions and runs step 3 again, and the operation ID makes that safe. Nothing is ever in two places, and nothing is ever nowhere.

A multi-step flow in which each step is its own transaction, and a failed later step is answered by a compensating step (for example "cancel: return the gold from escrow"), is called a **saga**. The alternative is **two-phase commit** (2PC), in which a coordinator asks every participant to prepare and then tells all of them to commit. 2PC gives you one atomic step across systems. It also blocks every participant while the coordinator is unreachable, which is why game servers rarely use it on the hot path. Escrow plus idempotent steps is the usual choice.

### Lost updates between two writers

A different failure appears when two servers hold the same character in memory. During a zone handoff (week 4) the old and new zone servers may both believe they own Ayla for a moment. If both save her whole record, the second save silently overwrites the first. That is a **lost update**: nothing is duplicated, but a change vanishes.

Two defences:

- **One owner at a time.** A lease in Redis or a row in PostgreSQL names the zone server that owns each character. A server may write a character only while it holds the lease. The handoff protocol transfers the lease as one step.
- **Optimistic concurrency.** Each character row carries a `version` number. A save runs `UPDATE character SET ..., version = version + 1 WHERE id = :id AND version = :v_loaded`. If it updates zero rows, another writer got there first, and this save must reload and merge instead of overwriting.

Use both. The lease prevents the common case and the version check catches the rare case where the lease logic has a bug.

## In-class activity (25 minutes)

In pairs. Here is a guild bank withdrawal flow written by a junior engineer:

1. Client sends "withdraw item 88213 from guild bank to my bag".
2. World server checks the player's guild rank allows it.
3. World server adds item 88213 to the player's in-memory bag and sends "ok" to the client.
4. World server sends "remove item 88213" to the guild service over the network.
5. Guild service deletes the item from the guild bank table.
6. The player's bag is saved by the periodic save, up to 90 seconds later.

Your tasks:

1. Mark every point where a crash or a lost message breaks conservation, and say whether each produces a dupe or a loss.
2. Two officers click "withdraw" on the same item in the same second from different zone servers. What happens?
3. Redesign the flow with an owner column, one transaction per step, and an operation ID. Write the SQL for the step that moves the item.
4. Estimate daily incidents for the old flow on a shard doing 40,000 withdrawals a day, with `f` = 1 in 2,000 between steps 3 and 5.

Expected output: an annotated flow (a lost step 4 message, or a guild-service crash before step 5, is a dupe once step 6 saves the bag; a world-server crash after step 5 but before step 6 is a loss), the race answer (both officers get the item), the redesigned flow with one `UPDATE item SET owner_container_id = ... WHERE item_id = 88213 AND owner_container_id = :guild_bank` in one transaction, and `40,000 / 2,000 = 20` dupes a day before any exploiter finds it.

## Common misconceptions

- **"We use a database with transactions, so we can't have dupes."** Transactions only protect what is inside one of them. Two separate commits, a reply lost after commit, or a flow across two services each leave a gap.
- **"Retries are safe because the operation checks first."** A check followed by a separate write is a race between concurrent retries. Put the check inside the write (`WHERE claimed = 0`) or behind a unique key.
- **"Rare failures don't matter at our scale."** At two million operations a day, one in ten thousand is 200 a day. And once a player can cause the failure, its rate is whatever the player wants.
- **"The audit only needs to be roughly right."** A tolerance hides dupes smaller than the tolerance. Count every container and demand exactly zero drift.

## Check yourself

1. Explain why `UPDATE item SET owner_container_id = 42 WHERE item_id = 7` is idempotent and `UPDATE wallet SET gold = gold + 50 WHERE player = 'bren'` is not. What would you add to the second to make a retried request safe?
2. A shard's ledger says 1.2 billion gold were minted and 1.05 billion destroyed since launch, with a starting supply of 0. The sum of all wallets and banks is 162 million. Mail and auction escrow were not counted. What can you conclude, and what must you do before raising an alarm?
3. In the escrow flow of section 4, the settlement job crashes after moving the sword to Bren's mail and before moving the gold to Ayla's, and both moves were separate transactions. What is the state of the audit? How would you change step 3?
4. A client generates a new idempotency key each time it retries. Give a sequence of events that produces a double transfer.
5. Using the section 2 numbers, how many applied-twice operations per day does design 3 produce if `a` doubles during a bad network week? Does design 4 change?

<details>
<summary>Answers</summary>

1. Setting a column to a fixed value leaves the same result however many times it runs. Adding 50 adds 50 each time. Record an operation ID in the same transaction (with a primary key on the ID), or turn the counter update into a conditional one tied to a one-time source such as a mail's `claimed` flag.
2. Expected supply is `1.2 − 1.05 = 0.15` billion, 150 million. Actual counted is 162 million, so drift is at least +12 million, but the count is incomplete. Uncounted containers can only add to the actual supply, so the true drift is 12 million or more. That points to a dupe, not away from one. Before alarming, count mail and escrow so the size of the drift is exact.
3. The sword left escrow and the gold did not, so the audit is still balanced (the gold sits in `auction:5512`), but Ayla has not been paid and the auction looks half-settled. Make step 3 one transaction that moves both, conditional on the auction being unsettled, with an operation ID.
4. The client sends transfer (key k1). The server commits. The reply is lost. The client retries with key k2. The server has never seen k2, so it transfers again. Bren receives twice and Ayla pays twice.
5. `a` becomes 1 in 2,500, so `2,000,000 / 2,500 = 800` per day. Design 4 still produces zero, because every retry carries the original key.

</details>

## Lab / assignment hook

[Lab 08, a dupe-proof item service](../labs/lab08.md). You start from an inventory service with a known dupe, reproduce it with an injected crash, then rewrite the transfer to be atomic and idempotent and add a conservation audit that must report zero drift after 10,000 randomized operations with crashes and retries. Deliverable: the completed `item_service.py` passing the tests, the audit output, and a 250-word incident report for the original bug.

## Sources

- Terdiman, D. (2005, August 11). "Cheaters slam 'Everquest II' economy". ZDNet (archived copy, web.archive.org). SOE's Chris Kramer: the amount of money in the game rose by about a fifth in about 24 hours, alarms went off, the dupers tried to sell on Station Exchange, and the economy was restored.
- Koster, R. (2004, April 30), "Economy Stats", Star Wars Galaxies live server report (Internet Archive copy of the simbaspaws.org mirror, re-read September 2026). Also summarized in Wikipedia, "Duping (video games)". Star Wars Galaxies designers saw more currency leaving than entering with no shortage of money, concluded there was a dupe bug, found it and removed trillions of credits.
- TrinityCore, `src/server/game/Handlers/MailHandler.cpp` and `src/server/game/Handlers/TradeHandler.cpp` (branch 3.3.5, the World of Warcraft 3.3.5a client era, read September 2026). `HandleMailTakeMoney` saves gold and mail in one `CharacterDatabaseTransaction`, after sending the success result, with the comment "save money and mail to prevent cheating"; completed trades save both players in one transaction. https://github.com/TrinityCore/TrinityCore
- Stripe API reference, "Idempotent requests" (docs.stripe.com, read September 2026). The server saves the status code and body of the first request for a key and returns them for retries; keys can be pruned after at least 24 hours; mismatched parameters cause an error.
- PostgreSQL 18 documentation, "INSERT", the `ON CONFLICT` clause.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 7 (atomicity, lost updates) and chapter 9 (two-phase commit).
- Operation counts, failure rates, supply sizes and exploit rates in section 2 are invented teaching values.

## Interactive spec: examples/w08-ledger-drift.html

**The one insight:** every player's own wallet looks normal during a dupe. Only the global sum of every container, compared with the ledger of minted and destroyed currency, shows it. Atomicity and idempotency keep the two lines welded together; anything less lets them drift apart.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "what players see": three wallet bars (players A, B, C) plus one "mail and escrow" bar, updated as the simulation runs. Each operation briefly draws an arrow from source to destination. Half-done operations flash the arrow in the alert color; double-applied ones draw a second arrow. No totals are shown in this view.
- View B, "what the audit sees": a line chart over one simulated day (x from 0 to 24 h). Line 1, expected supply from the ledger. Line 2, actual supply (sum of all containers). The gap between them is shaded (alert color above, a second color below) and the current drift is printed at the right edge. Vertical ticks mark audit times; the first audit where drift is nonzero gets a label "alarm at h:mm, drift X".

**Controls:**

- Design selector: 1 (separate writes, give first), 2 (separate writes, take first), 3 (one transaction), 4 (transaction and idempotency key). Default 1.
- `M` operations per day, 100,000 to 10,000,000, log slider (default 2,000,000).
- `f` failure between writes, 0 to 1 in 1,000, log slider (default 1 in 10,000). `a` lost reply, 0 to 1 in 1,000, log slider (default 1 in 5,000).
- Share of retried operations whose source is a one-time container (mail, reward, escrow) rather than another player, 0 to 100% (default 50%). Double application from a one-time source counts as a dupe; from a player it moves gold between wallets and does not change supply.
- Average value per operation, 10 to 100,000 gold (default 250).
- Starting supply, 10 million to 10 billion (default 400 million). Faucet and sink rates are equal so expected supply is flat unless the user sets "net faucet per day" (default 0).
- Exploiter toggle, with number of exploiters (default 10), seconds between dupes (default 30) and gold per dupe (default 10,000). Exploit dupes apply only in designs 1 and 3 (a half-done give-first operation or an unguarded retry), and never in design 4. In design 2 an exploiter can only cause losses.
- Audit interval: 5 min, 15 min, 1 h, 6 h, 24 h (default 1 h). Alarm threshold: 0 or a tolerance as a percentage of supply (default 0).
- Play, pause and step buttons (step = one audit interval), and a speed control.

**Readout (always visible, `aria-live="polite"`):** half-done per day `M·f`, retried per day `M·a`, dupes per day, losses per day, double charges per day, drift per day in gold and as a percentage of supply, time of first alarm.

**Formulas (expected values, which the simulation should approach; show both):**

```
half_done   = M × f
retried     = M × a
design 1: dupes = half_done + retried × one_time_share     losses = 0
design 2: dupes = retried × one_time_share                 losses = half_done
design 3: dupes = retried × one_time_share                 losses = 0
design 4: dupes = 0                                        losses = 0
double charges (all designs 1-3) = retried × (1 − one_time_share)
drift per day = (dupes − losses) × value + exploit_rate
exploit_rate  = exploiters × 3600/interval × gold × 24   (designs 1 and 3 only)
```

**Test values (must match):**

- Defaults with one-time share set to 0: design 1 gives 200 dupes, 0 losses, 400 double charges; design 2 gives 0 dupes, 200 losses; design 3 gives 0 and 0 with 400 double charges; design 4 gives all zero.
- Defaults (one-time share 50%): design 1 dupes `200 + 200 = 400` per day, drift 100,000 gold per day (0.025% of supply).
- Exploiter on, defaults, design 1: exploit adds 12,000,000 gold per hour; first hourly audit alarms with drift about 12,004,167 (12,000,000 plus `100,000/24` from accidents).
- Exploiter on, design 4: drift 0, no alarm.
- `M = 5,000,000`, `f` = 1 in 50,000, `a` = 1 in 20,000, design 3, one-time share 0: 0 dupes, 250 double charges.

**First screen:** defaults with the exploiter on, design 1, paused at the first audit alarm (1:00). Caption: "Every wallet on the left looks normal. The audit on the right does not."

**Accessibility:** all controls keyboard operable with visible focus; readout in an `aria-live="polite"` region; respects `prefers-reduced-motion` (no arrow animation, instant updates) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes and labels only, no game art or logos.
