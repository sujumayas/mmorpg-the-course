# MMO302 · Week 07 — Persistence strategies: write-through, periodic save, event sourcing

**Why this matters:** A world server holds thousands of characters in memory and must copy them to a database without freezing the game, flooding the database, or losing an hour of loot when it crashes. You cannot have all three for free. This week you learn the five standard strategies, put a price on each one in commits per second, seconds lost and seconds frozen, and pick one per kind of state instead of one for the whole server.

**You will be able to:**
- Compute commits per second, bytes per second, average loss, freeze time and recovery time for stop-the-world, periodic, write-through, write-behind and event-log persistence on a given shard.
- Explain why a whole-world snapshot needs either a paused world or copy-on-write to be consistent, and what goes wrong without either.
- Derive the recovery time of an event log with snapshots, `replay = events per second × K / 2 / r`, and choose a snapshot interval `K` from a recovery-time target.
- Design a per-state persistence policy for a world server and defend it against a failure scenario.

**Before class:** Martin Fowler, "Event Sourcing" (martinfowler.com, December 2005), the whole article. Redis documentation, "Redis persistence", the sections on RDB and AOF advantages and disadvantages and "How durable is the append only file?". Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 11, the section "Databases and Streams" through "Event Sourcing". Reread your notes on [DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md).

**Prerequisites from earlier courses:** [DB201 week 1, why persistence is hard](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) derived the periodic-save model (`W = N / T`, average loss `T / 2`, and the hybrid with event saves). This lecture uses it and does not re-derive it. [DB201 week 5, transactions and ACID](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) and [DB201 week 8, caching and write-behind](../../DB201-data-persistence-and-telemetry/lectures/w08-caching-and-write-behind.md). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the tick as a CPU budget, which a save can blow). [MMO302 week 1](w01-scale-targets-ccu-messages-and-n-squared.md) for shard sizing and [week 5 on tick rate](w05-tick-rate-for-mmos-vs-shooters.md).

**Interactive:** [examples/w07-persistence-strategies.html](../examples/w07-persistence-strategies.html). Keep it open during section 2.

---

## 1. Where the truth lives

In DB201 you treated persistence as a question about one player. How often do we save this character, and how much can a crash erase? An MMO world server asks the same question for 3,000 characters at once, plus the world objects they share, on a machine whose first job is to run a 10 to 30 Hz simulation tick.

Three places hold state in a running MMO, and every strategy in this lecture is a rule about what moves between them.

- **Memory on the world server.** The simulation reads and writes here every tick. It is the only copy fast enough to run the game, and it vanishes when the process dies.
- **A cache or log close to the server,** such as Redis. Faster than the database, slower than memory, and optionally durable.
- **The system of record,** PostgreSQL in our reference stack. What it holds after a crash is, by definition, what happened.

A **persistence strategy** is the rule for copying changes from memory to the system of record. Five rules cover almost every shipped server. They differ in when the copy happens and in what unit gets copied.

| Strategy | When it writes | What it writes |
|---|---|---|
| Stop-the-world snapshot | every `T_world` seconds, with the game paused | the whole world |
| Periodic save | every `T` seconds per player, staggered | one whole character |
| Write-through | on every change, before the change is confirmed | the changed row |
| Write-behind | every `F` seconds, for records marked dirty | the changed rows, merged |
| Event log | on every change, appended to a log | a small event describing the change |

Two terms first. A change is **persistent** if the game must remember it across a crash: gold, XP, an item moving between bags, a quest step. Position, facing and current mana are usually not persistent in this sense; they are saved with the character but nobody files a ticket if they roll back by a minute. A **commit** is one durable write the database confirms, which means one flush to disk. Databases are limited by commits per second far more than by bytes, so commits are the number to watch.

## 2. Worked example: what does each strategy cost one shard?

### The hook

Anyone who has played on a community server for Ultima Online has seen the broadcast "The world is saving, please wait." Then everything stops. Monsters freeze mid-swing, chat goes quiet, and a second message reports how long the save took. The server runs this every five minutes by default. In ServUO, the open-source Ultima Online server emulator that many of these shards run, the save routine calls `NetState.Pause()` before it starts serializing, then resumes the network when it is done.

A modern server team would call that a bug, a regular and deliberate freeze for every player on the shard. So why would a working MMO server stop the world on purpose? And what did later servers do instead? The answer is a model that prices all five strategies on the same shard.

### The model

Take one shard and name its numbers.

- `N`, players online.
- `c`, persistent changes per player per second (loot, XP, gold, quest counters).
- `S`, bytes in one full character save. `s`, bytes in one change record (a row delta or an event).
- `W`, bytes in a whole-world snapshot. `R`, how fast the server can serialize and write, in bytes per second.
- `T_world`, `T`, `F`, the intervals for stop-the-world, periodic and write-behind saves.
- `g`, the event log's group-commit window. **Group commit** means the log collects all events that arrive in a short window and flushes them in one commit.
- `h`, how many distinct rows one player dirties in a flush window (write-behind merges repeated changes to the same row).
- `K`, how often the event log takes a snapshot. `r`, how many events per second recovery can replay.

Then each strategy has five costs.

```
                 commits/s    bytes/s              avg loss    freeze       replay after crash
stop-the-world   1/T_world    W/T_world            T_world/2   W/R          0
periodic         N/T          N·S/T                T/2         0            0
write-through    N·c          N·c·s                0           0            0
write-behind     N/F          (N/F)·min(c·F, h)·s  F/2         0            0
event log        min(1/g,N·c) N·c·s                0           0            N·c·K/2/r
```

Three of these lines deserve a sentence.

The **freeze** of a stop-the-world save is the snapshot size divided by the write speed, and every player on the shard pays it at once.

**Write-behind** keeps changes in memory (or Redis) and marks each changed record **dirty**. Every `F` seconds a flusher writes the dirty records and clears the marks. If a player's gold changes ten times in one window, the database sees one write with the final value. That merging is called **coalescing**, and it is why write-behind's bytes per second can fall below the raw change rate.

The **event log** writes every change, but as a tiny record appended to the end of a file, and group commit turns thousands of appends into a hundred or so flushes a second. It never overwrites anything. After a crash the server loads the latest snapshot and replays the events written since. On average a crash lands halfway through a snapshot interval, so recovery replays `N·c·K/2` events.

### Numbers you can check

Here is a mid-sized shard, with invented but realistic values. It has 3,000 players, each making 0.5 persistent changes per second (one every two seconds). A character is 20 kB, a change record 120 bytes. The world snapshot is 150 MB and serializes at 100 MB/s. The intervals are the ServUO default of 300 seconds for the world save, 90 seconds for periodic saves, 10 seconds for write-behind flushes, a 10 ms group commit, and an event-log snapshot every 600 seconds replayed at 200,000 events per second.

```python
N = 3000        # players online
c = 0.5         # persistent changes per player per second
S = 20_000      # bytes in one full character save
s = 120         # bytes in one change record (a row delta or an event)
h = 3           # distinct rows one player dirties per flush (write-behind)
T_world = 300   # stop-the-world save interval, seconds
W = 150e6       # whole-world snapshot, bytes
R = 100e6       # serialize-and-write speed, bytes per second
T = 90          # periodic per-player save interval, seconds
F = 10          # write-behind flush interval, seconds
g = 0.010       # event-log group commit window, seconds
K = 600         # event-log snapshot interval, seconds
r = 200_000     # events replayed per second during recovery

changes = N * c
rows = [  # name, commits/s, bytes/s, avg loss s, freeze s, replay s
    ("stop-the-world", 1 / T_world, W / T_world, T_world / 2, W / R, 0),
    ("periodic save", N / T, N * S / T, T / 2, 0, 0),
    ("write-through", changes, changes * s, 0, 0, 0),
    ("write-behind", N / F, N / F * min(c * F, h) * s, F / 2, 0, 0),
    ("event log", min(1 / g, changes), changes * s, 0, 0, changes * K / 2 / r),
]
print(f"{'strategy':15}{'commits/s':>10}{'kB/s':>6}{'loss s':>8}{'freeze s':>9}{'replay s':>9}")
for name, w, b, loss, freeze, replay in rows:
    print(f"{name:15}{w:10.3f}{b/1000:6.0f}{loss:8.1f}{freeze:9.1f}{replay:9.2f}")
```

It prints:

```
strategy        commits/s  kB/s  loss s freeze s replay s
stop-the-world      0.003   500   150.0      1.5     0.00
periodic save      33.333   667    45.0      0.0     0.00
write-through    1500.000   180     0.0      0.0     0.00
write-behind      300.000   108     5.0      0.0     0.00
event log         100.000   180     0.0      0.0     2.25
```

Check two rows by hand. Write-behind: `3,000 / 10 = 300` flushes per second. Each player made `0.5 × 10 = 5` changes in the window, but they landed on only 3 rows, so each flush writes `3 × 120 = 360` bytes, and `300 × 360 = 108,000` bytes per second. Event log: 1,500 events per second, 100 commits per second because of the 10 ms window, and a crash replays on average `1,500 × 600 / 2 = 450,000` events, which takes `450,000 / 200,000 = 2.25` seconds.

Now read the table as a set of trades.

- **Stop-the-world** is the cheapest on the database (one file every five minutes) and the worst for players: a 1.5-second freeze every five minutes and 150 seconds of average loss. At a 20 Hz tick, 1.5 seconds is 30 missed ticks.
- **Periodic save** removes the freeze and cuts loss to 45 seconds. It writes the most bytes, because it rewrites whole 20 kB characters that barely changed.
- **Write-through** loses nothing, at 1,500 commits per second from one shard. Twenty such shards on one database cluster would ask for 30,000 commits per second. Worse, every player action now waits for a database round trip, and a slow database slows the game.
- **Write-behind** is the middle: 300 commits per second, 5 seconds of loss, no freeze, and the fewest bytes.
- **The event log** matches write-through's zero loss at a fifteenth of its commits. It pays at recovery time, and it adds up to 10 ms of latency to any action that waits for its event to be committed.

One more row is worth computing, because it is the mistake every first event-sourced server makes, which is never taking snapshots. After 24 hours the log holds `1,500 × 86,400 = 129.6 million` events. Replaying them at 200,000 per second takes 648 seconds, almost 11 minutes of downtime after every crash, and the number grows every day the server stays up. Snapshots are not an optimization of event sourcing. They are part of it.

### Seeing it move

Open the interactive. The first view is a 10-minute timeline for one shard. Pick a strategy and it draws its writes as marks, its freezes as grey bands, and a draggable crash marker shades what that crash erases in red and what recovery must replay in blue. The second view, beside it on a wide screen and below it on a phone, is the bill. It has four bars per strategy (commits per second, kB per second, average loss, and freeze or replay time combined in one bar) on log scales, so 0.003 and 1,500 fit on one chart.

Drag the crash marker across a stop-the-world interval and watch the red region grow from zero to 300 seconds. Then switch to the event log and drag `K`. The red region stays at zero, and the blue replay region grows in a straight line with `K`. That is the whole trade of event sourcing in one picture. You stop losing progress and start paying in restart time, and the snapshot interval is the dial between them.

### Why stop the world at all

Back to the hook. A snapshot is only useful if it is **consistent**, meaning it shows a state the game was really in at one instant. Suppose a trade moves a sword from Ayla's bag to Bren's while the save is running. If the saver wrote Ayla just before the trade and Bren just after it, the snapshot has Ayla with the sword (not yet given) and Bren with the sword (already received). A crash now restores a world with two swords. If it wrote Bren first and Ayla second, the snapshot has neither of them holding it, and the sword is gone. ServUO's own source code logs a warning when a script tries to create or delete an object during a save, warning that the action could leave the saved state inconsistent.

Pausing the world is the simplest way to guarantee that nothing changes while you copy it. There are two ways around the pause.

- **Copy-on-write.** Redis creates its RDB snapshot by calling `fork()`. The child process gets a frozen view of memory and writes it to disk, while the parent keeps serving clients. The operating system copies a memory page only when the parent changes it. The pause shrinks to the time `fork()` takes, which the Redis documentation puts at milliseconds, or up to a second for a very large dataset on slow hardware.
- **Stop saving the world as one thing.** Periodic, write-through, write-behind and event-log strategies never snapshot the whole world at once. They each need a different answer to the sword problem, which is that any change touching two records (a trade, a mail, a guild bank withdrawal) must reach the database as one transaction. Week 8 is about exactly this.

### Cross-game recognition

Rewrite any real server's persistence into the table's terms and ask which cost it chose to pay.

**ServUO (Ultima Online server emulator, current master branch).** Stop-the-world with `T_world = 300` seconds. `AutoSave.Frequency` defaults to five minutes, the save pauses the network, broadcasts the "world is saving" message, and afterwards tells players how many seconds the save took. The emulator can serialize on several threads and let the disk write finish in the background, which shrinks `W / R` without changing the shape. The freeze is the price of a consistent snapshot with no database at all: the world is a set of binary files.

**TrinityCore (World of Warcraft 3.3.5 server emulator).** Periodic per-player saves with `T = 90` seconds: `PlayerSaveInterval` defaults to 90,000 ms in `worldserver.conf.dist`. It plugs the consistency hole for trades with a targeted transaction. When a trade completes, the handler saves both players' inventories and gold inside one database transaction, with a comment noting that the per-player saves would otherwise be out of sync with each other. That is the hybrid from [DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) (periodic for cheap state, immediate for valuable events) plus the rule that a two-sided event commits both sides together.

**Redis (the cache in our reference stack).** Redis offers two persistence modes that map onto two rows of the table. RDB is a periodic snapshot made by `fork()` and copy-on-write, and the documentation warns that you should be prepared to lose the latest minutes of data. AOF, the append-only file, is an event log: every write command is appended and replayed on restart. Its default `appendfsync everysec` is group commit with `g = 1` second, and the documentation says you may lose one second of writes. Redis also rewrites the AOF in the background into the shortest command sequence that rebuilds the current data. That rewrite is the event log's snapshot, the `K` of our model.

**PostgreSQL (the system of record).** Every change goes first to the write-ahead log (WAL), a sequential log flushed at commit. The data files are brought up to date at a **checkpoint**. After a crash, PostgreSQL replays the WAL written since the last checkpoint. `checkpoint_timeout` defaults to 5 minutes, and the PostgreSQL 18 documentation states that raising it can increase crash-recovery time. That is `replay = N·c·K/2/r` with `K = 300`. Your database is already an event-sourced system with snapshots, which is part of why it can promise durability at thousands of commits per second.

Four systems, one table. Each picked a row, or a mix of rows, and paid the cost that row charges.

### Eyes-open design judgment

- **Choose per kind of state, not per server.** Position and mana can go in a periodic save. Gold and XP suit write-behind with a short `F`. Trades, mail, auction-house sales and real-money purchases need an immediate transaction or an event committed before the player sees "success". One server can run three strategies at once, and good ones do.
- **Write-through moves the database into your tick.** Every action now waits on a network round trip and a disk flush. A database hiccup of 200 ms becomes a 200 ms freeze for anyone who looted during it. Use write-through only for rare, valuable events, and make the tick not wait for it (the action completes when the commit returns, while the simulation keeps running).
- **Write-behind is only as good as its flusher.** If the process dies, everything dirty is lost, up to `F` seconds. If the flusher falls behind (the database is slow), dirty records pile up in memory and the real loss window grows past `F`. Monitor the age of the oldest dirty record, not the configured `F`.
- **An event log needs three things decided on day one.** A snapshot interval, from your recovery-time target. A versioning plan for events, because you will replay events written by a server version you no longer run. And a retention policy, because the log grows forever unless you archive it.
- **Event sourcing gives you a history for free.** You can answer "where did this sword come from?" by reading the log. Week 8 uses that for dupe audits, and MMO309 uses it for exploit investigations. For some teams this, not durability, is the reason to adopt it.
- **The freeze is sometimes the right call.** A small community shard with 50 players, no database and a 0.3-second save is well served by a stop-the-world snapshot. Knowing the cost means you can accept it on purpose.

### Check this example

1. The shard grows to `N = 6,000` with everything else unchanged. Which rows of the table double, and which do not change?
2. Your recovery-time target is 5 seconds on average after a crash. With `N = 3,000`, `c = 0.5` and `r = 200,000`, what is the longest snapshot interval `K` you can use?
3. A stop-the-world server's world grows to 400 MB. At `R = 100` MB/s, how many 30 Hz ticks does one save skip?

<details>
<summary>Answers</summary>

1. Periodic commits and bytes, write-through commits and bytes, write-behind commits and bytes, event-log bytes and event-log replay time all double, because they are proportional to `N`. Stop-the-world does not depend on `N` directly (only on world size), average loss does not depend on `N` for any strategy, and the event log's commits stay at `1 / g = 100` per second because group commit absorbs the extra events.
2. `N·c·K/2/r ≤ 5` gives `K ≤ 5 × 2 × 200,000 / 1,500 = 1,333` seconds, about 22 minutes.
3. The freeze is `400 / 100 = 4` seconds, which is `4 × 30 = 120` skipped ticks.

</details>

## 3. Event sourcing in practice

An **event** is a record of a fact that happened, written in the past tense: "Ayla looted 50 gold", "Bren gained 80 XP". **Event sourcing** means the event log, not the current state, is the source of truth. The current state is whatever you get by applying every event in order to an empty world. A **snapshot** is a saved copy of that state at some sequence number, so recovery can start there instead of at the beginning.

This short program applies six events to rebuild two characters, then shows that a snapshot taken after the fourth event, plus the last two events, gives the same result.

```python
import copy

def apply(state, event):
    kind, who, amount = event
    char = state.setdefault(who, {"gold": 0, "xp": 0})
    if kind == "loot_gold":
        char["gold"] += amount
    elif kind == "buy":
        char["gold"] -= amount
    elif kind == "kill_xp":
        char["xp"] += amount
    return state

log = [
    ("loot_gold", "ayla", 50), ("kill_xp", "ayla", 120),
    ("loot_gold", "bren", 30), ("buy", "ayla", 35),
    ("kill_xp", "bren", 80), ("loot_gold", "ayla", 10),
]

# Recovery 1: replay the whole log from nothing.
full = {}
for e in log:
    apply(full, e)

# Recovery 2: a snapshot taken after event 4, then replay only the tail.
snapshot, seq = {}, 4
for e in log[:seq]:
    apply(snapshot, e)
restored = copy.deepcopy(snapshot)
for e in log[seq:]:
    apply(restored, e)

print(full)
print(restored == full, "replayed", len(log) - seq, "of", len(log), "events")
```

It prints:

```
{'ayla': {'gold': 25, 'xp': 120}, 'bren': {'gold': 30, 'xp': 80}}
True replayed 2 of 6 events
```

Three rules keep a real event log honest.

**Events must be deterministic to apply.** `apply` may not roll dice, read the clock or look at anything outside the state and the event. If a loot roll happened, the event records the result ("looted 50 gold"), not the roll ("rolled on table 7"). Otherwise replay produces a different world than the one players saw. This is the same discipline as the deterministic simulation of [CS202 week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md), applied to storage.

**Events are never edited.** If a GM refunds a scammed player, the fix is a new event ("GM refund, 500 gold, ticket 88213"), not a change to an old one. The log is a history, and history you can edit is not evidence.

**Event formats outlive the code that wrote them.** A patch that renames `loot_gold` or adds a field must still replay last month's events. Teams handle this with a version number in each event and an "upcaster" that converts old versions to the current shape during replay. [DB201 week 9](../../DB201-data-persistence-and-telemetry/lectures/w09-schema-migrations-in-a-live-game.md) covers live schema migrations, and event logs are the hardest case of it.

### How big does the log get?

At 1,500 events per second of 120 bytes, the shard writes 180 kB per second, which is 15.6 GB per day. A year is over 5 TB for one shard. Nobody keeps that hot. The usual policy is to keep events since the last snapshot on fast storage for recovery, move older events to cheap archive storage for audits, and delete or aggregate them after the retention period your privacy policy allows ([DB201 week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md)).

### Event log plus database, not event log instead of database

A common production design uses both. The world server appends events to a log (Redis streams, Kafka, or an `events` table in PostgreSQL with sequential IDs). A separate process, often called a **projector**, reads the log and updates ordinary relational tables (`character`, `inventory_item`) that the rest of the company queries. The log is the truth for recovery and audit. The tables are a convenient, rebuildable view of it. If a projector bug corrupts the tables, you fix the bug, drop the tables and replay.

## 4. Picking a policy for one server

Put the pieces together for a single world server with the section 2 shard. Here is one defensible policy.

| State | Strategy | Parameter | Why |
|---|---|---|---|
| Position, facing, current HP and mana | periodic, with the character | `T = 90` s | cheap to lose, expensive to write often |
| Gold, XP, reputation counters | write-behind to Redis, flushed to PostgreSQL | `F = 10` s | changes often, coalesces well, 5 s of loss is acceptable |
| Loot of rare items, quest completion | event appended and committed before the "you received" message | `g = 10` ms | valuable, low rate, players screenshot it |
| Trades, mail, auction-house sales | one PostgreSQL transaction covering both sides | immediate | two players involved, a half-done write is a dupe or a loss |
| Real-money purchases | write-through, plus the payment provider's receipt | immediate | legal record, refunds cost money |

Estimate its commit load. Periodic: `3,000 / 90 = 33` commits per second. Write-behind: 300 per second into Redis, which can absorb that easily, and Redis flushes batches to PostgreSQL at, say, one batch per second. Rare loot and quests: if each player has 12 valuable events an hour, that is `3,000 × 12 / 3,600 = 10` events per second, grouped into at most 100 commits per second. Trades and mail at 2 per player-hour add `3,000 × 2 / 3,600 = 1.7` transactions per second. The system of record sees well under 200 commits per second from this shard, zero loss on anything a player would report, and no freeze.

The policy is only half the work. The other half is the question each row raises. When two rows touch the same object (a rare item looted by event, then traded by transaction, then saved periodically with the character), which write wins? The answer is ownership, and it is next week's topic.

## In-class activity (25 minutes)

In groups of three. Your studio's survival MMO has shards of 1,200 players. Each player makes 1.5 persistent changes per second (building placement, crafting, gathering). Characters are 60 kB. The world has 800 MB of player-built structures. The database team offers 400 commits per second per shard. Crashes happen about once a week.

1. Fill in the section 2 table for all five strategies with `T_world = 600`, `T = 120`, `F = 15`, `h = 4`, `g = 0.02`, `K = 900`, `R = 200 MB/s`, `r = 100,000`, and `s = 200` bytes. Show one row of arithmetic.
2. Cross out every strategy that breaks the 400 commits per second budget or freezes the shard for more than one second.
3. The designers say a lost building is unacceptable, a lost gathering node is fine. Write a three-row policy table like section 4's.
4. Name the failure your policy handles worst, in one sentence.

Expected output: the filled table (write-through at 1,800 commits/s and stop-the-world at a 4 s freeze are both out), a policy table, and one named weakness. A good answer puts building placement in the event log and notices that a 900-second `K` gives `1,800 × 900 / 2 / 100,000 = 8.1` seconds of average replay.

## Common misconceptions

- **"Write-through is the safe choice."** It is the safe choice for loss and the risky one for availability. Every action depends on the database, so a database slowdown becomes a game slowdown. Zero loss can also come from an event log at a fraction of the commits.
- **"Event sourcing means you never lose data."** You lose nothing that was committed to the log. Events inside the group-commit window at the moment of a crash are gone unless the player's action waited for the commit. And a log you cannot replay (because the event format changed) loses everything after the last usable snapshot.
- **"A snapshot is just a copy of memory."** A copy taken while the world keeps changing can record states that never existed together, such as an item in both traders' bags. A snapshot needs a pause, copy-on-write, or transactions that keep multi-record changes together.
- **"Write-behind loses at most `F` seconds."** It loses at most the age of the oldest unflushed record, which equals `F` only while the flusher keeps up. Under load the backlog grows and so does the loss.

## Check yourself

1. A shard of 5,000 players uses write-behind with `F = 20` s. Each player makes 0.4 changes per second, spread over at most 2 rows per flush, 150 bytes per row. Compute commits per second, bytes per second and average loss.
2. Your team switches that shard to an event log with 100-byte events, `g = 5` ms, `K = 300` s and `r = 250,000`. Compute commits per second, bytes per second and average replay time. Which is better for the database, and which for players?
3. PostgreSQL's `checkpoint_timeout` is raised from 5 to 30 minutes on a server writing 4,000 WAL records per second, replayed at 80,000 records per second. How does the average recovery time change?
4. A developer proposes snapshotting the world by iterating over all characters in a background thread while the simulation keeps running, without copy-on-write. Describe a sequence of two events that produces an inconsistent snapshot.
5. Why does Redis's AOF rewrite count as taking a snapshot, in the terms of this lecture?

<details>
<summary>Answers</summary>

1. Commits: `5,000 / 20 = 250` per second. Each player makes `0.4 × 20 = 8` changes per window on at most 2 rows, so each flush writes `2 × 150 = 300` bytes, and `250 × 300 = 75,000` bytes per second (75 kB/s). Average loss `F / 2 = 10` seconds.
2. Events: `5,000 × 0.4 = 2,000` per second. Commits: `1 / 0.005 = 200` per second. Bytes: `2,000 × 100 = 200` kB/s. Replay: `2,000 × 300 / 2 / 250,000 = 1.2` seconds. Write-behind is lighter on the database (fewer commits, fewer bytes). The event log is better for players, with zero committed loss against 10 seconds, at the price of a 1.2-second longer restart.
3. Average replay is `4,000 × K / 2 / 80,000`. At `K = 300` s that is 7.5 seconds; at `K = 1,800` s it is 45 seconds. Six times longer, because replay is linear in the checkpoint interval.
4. The thread saves Bren. Then Ayla trades a sword to Bren. Then the thread saves Ayla. The snapshot has Bren without the sword and Ayla without the sword, so the sword is gone after a restore. (Saving Ayla first, then the trade, then Bren duplicates it instead.)
5. The rewrite replaces a long history of commands with the shortest set of commands that rebuilds the current data, which is the current state at one point written in log form. After it, restart only has to replay that base plus the commands appended since, which is exactly a snapshot plus a tail.

</details>

## Lab / assignment hook

[Lab 07, persistence strategies under crash](../labs/lab07.md). You implement a write-behind store with dirty tracking and an event log with snapshots for a simulated shard, inject crashes, and measure commits, loss and recovery time against the section 2 formulas. Deliverable: the completed `persistence.py` passing the tests, the measured-versus-predicted table, and a 300-word policy for the in-class survival MMO.

## Sources

- ServUO, `Server/World.cs` and `Scripts/Misc/AutoSave.cs` (ServUO GitHub repository, master branch, read September 2026). `AutoSave.Frequency` defaults to 5 minutes; `World.Save` pauses network state, broadcasts "The world is saving, please wait.", reports the save duration to players, selects a single- or multi-threaded save strategy, and logs a warning when objects are created or deleted during a save. https://github.com/ServUO/ServUO
- TrinityCore, `src/server/worldserver/worldserver.conf.dist` and `src/server/game/Handlers/TradeHandler.cpp` (branch 3.3.5, the World of Warcraft 3.3.5a client era, read September 2026). `PlayerSaveInterval = 90000` ms; completed trades save both players' inventory and gold in one `CharacterDatabaseTransaction`. https://github.com/TrinityCore/TrinityCore
- Redis documentation, "Redis persistence" (redis.io, current as of September 2026). RDB snapshots via `fork()` and copy-on-write; fork can stop serving clients for milliseconds up to a second on large datasets; AOF fsync policies, default `everysec` with up to one second of loss; background AOF rewrite.
- PostgreSQL 18 documentation, "Write Ahead Log" server configuration. `checkpoint_timeout` default 5 min, `max_wal_size` default 1 GB, `wal_writer_delay` default 200 ms; raising checkpoint intervals can increase crash-recovery time.
- Fowler, M. (2005, December 12). "Event Sourcing". martinfowler.com. Definition of event sourcing, rebuilding state by replaying events, and snapshots.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 11, "Databases and Streams".
- All shard sizes, change rates and speeds in section 2 are invented teaching values, chosen to be realistic in order of magnitude.

## Interactive spec: examples/w07-persistence-strategies.html

**The one insight:** every persistence strategy pays for durability somewhere. Moving between strategies moves the cost between commits per second, seconds lost, seconds frozen and seconds of replay. None of them makes all four small, and the event log's snapshot interval `K` trades loss-free operation against restart time in a straight line.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "ten minutes of one shard": a horizontal timeline from 0 to 600 s. A strategy selector (five radio buttons) chooses which strategy is drawn. Writes appear as thin vertical ticks: one tick per stop-the-world save, one tick per 1 s of periodic saves (height proportional to commits in that second), one per flush for write-behind, one per snapshot (tall) plus a continuous thin band for the event log. Freezes are grey bands of width `W/R` starting at each world save. A draggable crash marker (default 430 s). The span from the last durable point before the crash to the crash is shaded red and labelled "lost: X s" (for periodic, write-behind and stop-the-world, the last durable point is the previous save or flush; for write-through and event log, loss is 0 and the label says "lost: 0 s"). For the event log, the span from the last snapshot to the crash is shaded blue and labelled "replay: Y events, Z s".
- View B, "the bill": five small bar groups, one per strategy, always all visible, with the selected one highlighted. Each group has four bars: commits/s, kB/s, average loss (s), and freeze-or-replay (s). Each bar uses its own log scale shared across strategies (commits 0.001 to 100,000; kB/s 1 to 100,000; seconds 0.01 to 10,000). Exact numbers are printed on each bar.

**Controls:**

- `N` slider, 100 to 20,000, step 100 (default 3,000).
- `c` slider, 0.05 to 5 changes per player per second, step 0.05 (default 0.5).
- `S` input, 1 to 500 kB (default 20). `s` input, 20 to 2,000 bytes (default 120). `h` input, 1 to 20 (default 3).
- `W` input, 1 to 5,000 MB (default 150). `R` input, 10 to 2,000 MB/s (default 100).
- `T_world` select: 60, 120, 300, 600, 1,800 s (default 300). `T` slider, 10 to 600 s (default 90). `F` slider, 1 to 120 s (default 10). `g` select: 1, 5, 10, 50, 1,000 ms (default 10).
- `K` slider, 30 to 86,400 s on a log scale, snapping to 30, 60, 120, 300, 600, 1,800, 3,600, 21,600, 86,400 (default 600). `r` input, 10,000 to 2,000,000 events/s (default 200,000).
- Draggable crash marker in view A, also operable with arrow keys (plus or minus 5 s, Shift plus or minus 50 s).

**Readout (always visible, `aria-live="polite"`):** the five-row table exactly as printed in section 2 for the current inputs, plus for the selected strategy and crash position: "lost: X s", "freeze per save: Y s" and "replay: Z events in Z2 s". With `K = 86,400` show an extra line "a crash after 24 h without snapshots replays `N·c·86400` events in `N·c·86400/r` s".

**Formulas:**

```
changes          = N × c
stop-the-world   commits = 1/T_world   bytes = W/T_world            loss = T_world/2   freeze = W/R
periodic         commits = N/T         bytes = N×S/T                loss = T/2
write-through    commits = N×c         bytes = N×c×s                loss = 0
write-behind     commits = N/F         bytes = (N/F)×min(c×F, h)×s  loss = F/2
event log        commits = min(1/g, N×c) bytes = N×c×s                loss = 0           replay = N×c×K/2/r
crash view:      periodic/write-behind/stop-the-world loss at crash time t = t mod interval
                 event log replay at crash time t = N×c×(t mod K) events, divided by r for seconds
```

**Test values (must match):**

- Defaults: stop-the-world 0.003 commits/s, 500 kB/s, loss 150.0, freeze 1.5; periodic 33.333, 667, 45.0; write-through 1500.000, 180, 0.0; write-behind 300.000, 108, 5.0; event log 100.000, 180, 0.0, replay 2.25 s.
- `K = 86,400` with defaults: 24-hour line shows 129,600,000 events and 648 s.
- `N = 6,000`, other defaults: periodic 66.667 commits/s and 1,333 kB/s; event log still 100 commits/s, replay 4.50 s.
- `W = 400` MB, `R = 100` MB/s: freeze 4.0 s.
- Crash marker at 430 s with defaults: stop-the-world "lost: 130 s"; periodic "lost: 70 s"; write-behind "lost: 0 s" (430 is a multiple of 10; at 437 it shows 7 s); event log "replay: 645,000 events, 3.2 s" (`1,500 × 430 = 645,000`, divided by 200,000 is 3.225 s, shown to one decimal) (since `430 mod 600 = 430`).

**First screen:** defaults, event log selected, crash at 430 s, the blue replay band visible, and a one-line caption: "Zero loss, 3.2 seconds to restart. Drag K and watch the restart time move instead."

**Accessibility:** all controls keyboard operable with visible focus; readout in an `aria-live="polite"` region; respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.
