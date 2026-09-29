# DB201 · Week 08 — Caching and Write-Behind

**Why this matters:** A busy MMO changes character state far faster than any database can record it. You cannot write every step to PostgreSQL, and you cannot write nothing. A cache sits between the game and the database and decides, per kind of data, how much work the database sees and how much a crash erases. This week you learn to set that dial with numbers instead of by feel.

**You will be able to:**
- Compute the database write rate for write-through and write-behind persistence, given the number of players, their update rate and the flush interval.
- Compute the expected and worst-case progress lost in a crash for a given flush interval, and find the interval where extra buffering stops paying off.
- Compute database load and average latency for a read cache from its hit ratio, and explain why the last few percent of hit ratio matter most.
- Decide which game data may be write-behind and which must be written through in a transaction, and defend the split.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 7, "Transactions", the opening section on what ACID durability promises. Nishtala et al., "Scaling Memcache at Facebook" (NSDI 2013), sections 1 and 3.2.1 (look-aside caching and leases), about 4 pages.

**Prerequisites from earlier courses:** [DB201 week 7, key-value stores](w07-nosql-and-key-value-stores-redis.md) (Redis types and persistence settings). From this course, [week 1, why persistence is hard](w01-why-persistence-is-hard-in-games.md) (save intervals and crash loss), [week 5, transactions and ACID](w05-transactions-and-acid.md) and [week 6, the duplication bug](w06-race-conditions-and-the-duplication-bug.md) (the trade dupe). The hash maps behind every cache, [CS102 week 5](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md). MA102's exponential and Poisson material helps in section 2 but is not required.

**Interactive:** [examples/w08-write-behind-tradeoff.html](../examples/w08-write-behind-tradeoff.html). Keep it open during section 2.

---

## 1. A cache has two jobs

A **cache** is a faster, smaller, less durable copy of data whose real home is somewhere else. In this course the real home, the **source of truth**, is PostgreSQL. The cache is usually Redis, or plain memory inside the game server process.

A cache can help with reads, with writes, or with both, and the patterns have names you will see in every backend codebase.

**For reads:**

- **Cache-aside** (Facebook's paper calls it look-aside). The game asks the cache first. On a **miss** it reads from the database and puts the result in the cache for next time. On a write it updates the database and then deletes the cached copy, so the next read fetches fresh data. The cache never talks to the database itself. Your code does.
- **Read-through.** The same idea, but a library or proxy does the database read for you on a miss.

**For writes:**

- **Write-through.** Every change goes to the database immediately, and the cache is updated too. Nothing is lost in a crash, and the database sees every write.
- **Write-behind** (also called write-back). Changes go to the cache and are marked **dirty**. A background job **flushes** dirty entries to the database later, in batches. The database sees far fewer writes. Anything not yet flushed is lost if the cache dies.

Week 1 looked at the simplest form of write-behind: save every player's whole state every T seconds. This week adds the part that makes it a cache. You flush only the entries that changed, and several changes to the same entry collapse into one write. That collapse, called **coalescing**, is where all the savings come from.

## 2. Worked example: 20 changes a second, one write every five minutes

### The hook

Minecraft Java Edition runs its world at 20 ticks a second. Blocks, mobs and furnaces change state on every tick. Yet the Minecraft Wiki documents that the game autosaves every 6,000 ticks, which is five minutes, plus whenever a single-player opens the pause menu.

That is a coalescing ratio of 6,000 to 1 for a chunk that changes every tick. A furnace smelting iron might change state thousands of times between saves, and the disk sees one write. The price shows up when the game or the server process crashes. Everything since the last autosave is gone, up to five minutes of building and mining.

Why five minutes and not five seconds, or one hour? And would the same answer suit an MMO with 5,000 players online? You can answer both with one formula.

### The model

Take:

- `N`, the number of online players (or chunks, or any unit you save as one row).
- `u`, how many times per second each one changes, on average.
- `T`, the flush interval in seconds.

**Write-through** writes every change:

```
W_through = N × u        writes per second
```

**Write-behind** writes each entry at most once per flush, and only if it changed since the last flush. If changes arrive at random at rate `u` (a Poisson process, from MA102), the chance an entry changed at least once in `T` seconds is `1 − e^(−uT)`. So:

```
W_behind = N × (1 − e^(−uT)) / T     writes per second
```

Look at the two ends. When `uT` is tiny (flush far more often than changes happen), `1 − e^(−uT) ≈ uT` and `W_behind ≈ N × u`, the same as write-through. There is nothing to coalesce. When `uT` is large (many changes per interval), `1 − e^(−uT) ≈ 1` and `W_behind ≈ N / T`. Every entry is dirty at every flush, and the write rate falls as one over `T`.

**What a crash loses.** A crash lands at a random moment in the flush cycle. The last flush happened, on average, `T/2` seconds earlier, and at most `T` seconds earlier:

```
expected loss  = T / 2   seconds of progress
worst case     = T       seconds
changes lost   ≈ u × T / 2   per entry, on average
```

So the two quantities you care about move in opposite directions. Writes fall like `1/T`. Loss grows like `T`.

### Numbers you can check

Take an MMO shard with `N = 5,000` players online and `u = 2` changes per player per second (position, health, experience and cooldowns, rolled together).

| Flush interval T | DB writes per second | Cut versus write-through | Expected loss | Worst-case loss |
|---|---|---|---|---|
| write-through | 10,000 | — | 0 s | 0 s |
| 1 s | 4,323 | 57% | 0.5 s | 1 s |
| 5 s | 1,000 | 90% | 2.5 s | 5 s |
| 30 s | 167 | 98.3% | 15 s | 30 s |
| 300 s | 17 | 99.8% | 150 s | 300 s |

Check the 1-second row by hand. `uT = 2`, `e^(−2) ≈ 0.135`, so `W = 5,000 × 0.865 / 1 ≈ 4,323`. At 5 seconds, `e^(−10)` is about 0.00005, so nearly every player is dirty and `W ≈ 5,000 / 5 = 1,000`.

Now read the table as a trade. Going from 1 s to 5 s saves 3,323 writes per second and adds 2 seconds of expected loss. That is about 1,660 writes saved per second of extra risk. Going from 30 s to 300 s saves 150 writes per second and adds 135 seconds of expected loss, about 1.1 writes saved per second of risk. The first move is 1,500 times better value than the second.

This is the key idea of the week. **Nearly all the savings arrive in the first few multiples of `1/u`.** After that, each extra second of buffering buys almost nothing and costs you a full second of player progress.

### Move it

Open the interactive. The left view plots database writes per second against `T` on a log axis, with the write-through level drawn as a flat line on top. The right view plots expected loss against `T` on the same axis. Drag the `T` slider and watch the left curve drop off a cliff between `T = 0.1` and `T = 3`, then flatten, while the right line keeps climbing at the same steady rate. Toggle "savings per second of loss" to see the ratio from the paragraph above as a third curve falling away.

Then change `u`. A slow-changing entity (`u = 0.01`, a house that changes when the owner redecorates) needs `T` in the hundreds of seconds before coalescing does anything. A fast one (`u = 20`, a Minecraft chunk on every tick) gets most of the benefit at `T = 0.2` s. The knee sits at about `T ≈ 1/u` to `3/u`. Minecraft's five minutes is far past the knee for a busy chunk. The model cannot tell you why Minecraft's developers chose that number. It can tell you that things outside the model, such as the cost of writing a large world file and the fact that the game also saves on pause, must have carried the decision, because the write savings stopped growing long before five minutes.

### The same trade in other systems

Write-behind is not a game trick. The databases in this program's stack make the same trade, and they document the loss window just as you did.

**Redis AOF (current Redis 8.x documentation).** With `appendfsync everysec`, the default, Redis appends each write to its log in memory and flushes the log to disk once a second. The documentation says you may lose one second of data in a disaster. That is write-behind with `T = 1` s, applied to the log instead of to rows. With `always` it becomes write-through and the docs call it very slow.

**PostgreSQL asynchronous commit (PostgreSQL 18 documentation).** With `synchronous_commit = off`, PostgreSQL reports a commit as done before its log record reaches disk. A background process, the WAL writer, flushes every `wal_writer_delay`, which defaults to 200 ms. The documentation gives the risk window as up to three times that, 600 ms. It also notes a property your game should copy. Transactions are replayed in commit order, so a crash can lose the newest commits but never keeps a later one while losing an earlier one it depended on.

**Fortnite (Epic Games, February 2018).** The postmortem of the 3.4 million concurrent-player outages reports the profile service handling 132,000 database writes a second at peak, with the matchmaking shard queuing writes until single updates took 40 seconds or more. Among Epic's listed fixes were cutting unnecessary calls to the backend and batching calls that could be done in bulk, which are the two levers of this model. Lower `u`, and coalesce.

Written in the same form, every one of these is `W = N × (1 − e^(−uT)) / T` with a stated `T`: 300 s for a Minecraft autosave, 1 s for Redis AOF, at most 0.6 s for PostgreSQL async commit. Once you see the formula you can read any "how often do we flush?" setting as a point on the curve.

### Eyes-open design judgment

- **Pick `T` from the knee, then check the loss.** Compute `W` at `T = 1/u`, `3/u` and `10/u`. Usually `3/u` gets most of the savings. Then ask whether `T` seconds of loss is acceptable for this data. If not, the data does not belong in write-behind at any `T`.
- **Split by data, not by server.** Position and health can lose 5 seconds; nobody files a ticket. A rare drop, a purchase or a trade cannot lose anything. So run two paths: write-behind for high-rate, low-value state, and write-through in a transaction for events that create or move value.
- **Flush on the moments that matter.** Always flush a player on logout, zone transfer and before any write-through transaction that reads their state. Minecraft does the equivalent when you open the pause menu.
- **Crash is not the only failure.** If the flusher falls behind (the database is slow, as in Fortnite's matchmaking shard), dirty entries pile up in memory and the real `T` grows without anyone changing the setting. Alert on the age of the oldest dirty entry, not just on errors.

## 3. Write-behind that does not corrupt anything

A careless flusher can do worse than lose data. It can write it in the wrong order or twice. Three rules keep it safe.

**Flush a batch in one transaction.** Collect all dirty entries, write them with one multi-row upsert, commit once. PostgreSQL and SQLite (3.24 and later) both accept `INSERT ... ON CONFLICT (id) DO UPDATE`.

```python
def flush(cache, conn):
    dirty = cache.take_dirty()          # swap out the dirty set atomically
    if not dirty:
        return 0
    rows = [(pid, s.x, s.y, s.hp, s.xp, s.version) for pid, s in dirty.items()]
    with conn:                           # one transaction per batch
        conn.executemany(
            """INSERT INTO char_state(id, x, y, hp, xp, version)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 x=excluded.x, y=excluded.y, hp=excluded.hp,
                 xp=excluded.xp, version=excluded.version
               WHERE excluded.version > char_state.version""",
            rows)
    return len(rows)
```

PostgreSQL uses `$1` placeholders instead of `?` through most drivers. In PostgreSQL you would also send the batch as one statement with `unnest` arrays or `COPY` into a staging table, because `executemany` in some drivers still makes one round trip per row.

**Carry a version number.** Every change increments `version` in the cache. The `WHERE excluded.version > char_state.version` clause refuses to overwrite newer data with older data. That matters when a flush is retried after a timeout, or when two server processes briefly both think they own a character during a zone handoff. A retried flush becomes harmless. The term for "safe to run twice" is **idempotent**.

**Take the dirty set, don't read it.** `take_dirty()` swaps the dirty map for an empty one in one step. Changes that arrive during the flush go into the new map and are written next time. If you iterate the live map instead, a change that lands mid-flush can be marked clean without being written.

### Where write-behind meets the trade dupe

In week 6 you watched two concurrent trades duplicate an item because neither ran in a transaction. Write-behind creates a slower version of the same bug. Suppose player A's inventory is cached with write-behind and player B's is written through. A gives B a sword. B's side is committed at once. The server crashes before A's next flush. After restart, B has the sword, and A's stored inventory still contains it too.

The rule that prevents this: **any operation that moves value between two owners runs as one database transaction over the rows of both owners, after flushing both.** The cache may speed up everything around a trade. The trade itself is write-through.

## 4. Read caching: the hit ratio does the work

Now the read side. Let:

- `R` be read requests per second.
- `h` be the **hit ratio**, the fraction of reads the cache answers.
- `t_c` and `t_db` be the time for a cache hit and for a database read.

```
DB reads per second = R × (1 − h)
average latency     = h × t_c + (1 − h) × (t_c + t_db)
```

The second line counts the cache check on a miss too, because cache-aside asks the cache first. Take `R = 20,000`, `t_c = 0.3` ms and `t_db = 3` ms:

| Hit ratio h | DB reads per second | Average latency |
|---|---|---|
| 0.80 | 4,000 | 0.90 ms |
| 0.90 | 2,000 | 0.60 ms |
| 0.95 | 1,000 | 0.45 ms |
| 0.99 | 200 | 0.33 ms |

The database load depends on `1 − h`, the miss ratio. Going from 95% to 99% looks like four points. It cuts database reads by a factor of five. Whenever someone reports a hit ratio, convert it to a miss ratio before you judge it.

### Invalidation

A cache is only useful if its copy is correct or close enough. Three tools, in order of preference:

1. **Delete on write.** When the game changes a row in PostgreSQL, it deletes the cached key. Facebook's paper explains why it deletes instead of updating the cache. A delete is idempotent, and the next read fills the cache with whatever the database now says.
2. **TTL.** Give every cached key an expiry (`EXPIRE`, week 7). Even if a delete is missed, the stale copy dies within the TTL. Pick the TTL as the longest staleness you would accept for that data: 60 s for a guild's member list, 5 s for an auction house price, never for a wallet balance you plan to act on.
3. **Versioned keys.** Put a version in the key (`item_def:v37:4471`). A content patch bumps the version, and old keys are simply never read again and expire on their own.

### The stampede

When a popular key expires, every server that wanted it misses at the same moment and all of them query the database for the same row. This is a **stampede** (Facebook calls it a thundering herd). The Facebook paper describes a fix called **leases**: on a miss, the cache gives one client a token that entitles it to refill the key, and tells the others to wait a moment and retry. Facebook configured memcached to hand out a token at most once every 10 seconds per key. For a set of keys prone to herds, measured over a week, the peak database query rate fell from 17,000 per second without leases to 1,300 per second with them.

For your game, the equivalent is a short lock in Redis (`SET lock:item_def:4471 me NX PX 2000`) held by the one server that refills the key, plus a small random spread on TTLs so that thousands of keys set at server start do not all expire in the same second. The Redis latency documentation warns about exactly that pattern, many keys expiring at once, as a cause of stalls inside Redis itself.

### When the cache is the outage

The Fortnite postmortem has a case every backend programmer should know. Epic's account service verified access tokens through an Nginx proxy that checked Memcached first. On 4 February 2018, Memcached began failing under network and connection load. Each check now waited for a 100 ms timeout before falling through. Nginx ran out of worker threads waiting on those timeouts, stopped answering health checks, and the load balancer removed every node. Sign-ins were mostly blocked for almost two hours.

Run it through the model. A healthy cache with `h` near 1 hides the database. A failing cache is worse than none: every read now costs `t_c`, which has become the full timeout, plus `t_db`. Two design rules follow. Set cache timeouts far below your request budget (a few milliseconds, not 100). And when the cache errors, skip it for a while rather than asking it again on every request, a pattern called a **circuit breaker**.

## In-class activity (25 minutes)

Groups of three. You run a shard with 3,000 players online. For each data type below you are given `u`, the change rate per player per second:

| Data | u |
|---|---|
| Position and facing | 5 |
| Health and mana | 1 |
| Experience points | 0.2 |
| Gold from loot | 0.05 |
| Crafted item created | 0.002 |

1. For each row, compute `W` for write-through and for write-behind at `T = 1/u`, `3/u` and 60 s.
2. Choose a policy for each row: write-behind with a stated `T`, or write-through in a transaction. Write one sentence per row naming the crash outcome you accept.
3. Add up the total write rate for your policy. Compare it with writing everything through.

Expected output: the filled table, a policy column, and the total with the ratio. One group presents and the others challenge the gold row.

## Common misconceptions

- **"Write-behind halves the writes if you flush half as often."** Only once `uT` is well above 1. Below the knee, doubling `T` barely changes `W`, because most flushes still find each entry dirty only once.
- **"A 95% hit ratio is nearly as good as 99%."** Database load follows the miss ratio. 5% misses is five times the load of 1% misses.
- **"A cache can only make things faster."** A cache that times out slowly makes every request slower than going straight to the database, and can take the service down, as in Fortnite's February 2018 incident.
- **"If I flush on a timer, loss is bounded by the timer."** Only while the flusher keeps up. If the database slows down, the real age of dirty data grows past `T`. Monitor the oldest dirty entry.

## Check yourself

1. A shard has 8,000 players with `u = 4` changes per second. Compute the write rate for write-through and for write-behind at `T = 0.25` s, `T = 1` s and `T = 10` s. Where is the knee?
2. Your designer wants at most 3 seconds of expected loss for position. What is the largest `T` you can use, and what write rate does it give for the shard in question 1?
3. A cache serves 50,000 reads per second at a 97% hit ratio. A patch changes key names and the hit ratio drops to 85% for an hour. By what factor does database read load rise?
4. Explain, with the trade example from section 3, why the flush of both players must happen before a trade's transaction, not after.

<details>
<summary>Answers</summary>

1. Write-through: 8,000 × 4 = 32,000 per second. At `T = 0.25`, `uT = 1`, so `W = 8,000 × (1 − e^(−1)) / 0.25 = 8,000 × 0.632 / 0.25 ≈ 20,228`. At `T = 1`, `uT = 4`, `W = 8,000 × 0.982 / 1 ≈ 7,853`. At `T = 10`, `W ≈ 800`. The knee is around `T = 1/u` to `3/u`, so 0.25 s to 0.75 s. By 1 s you already cut 75% of writes.
2. Expected loss is `T/2`, so `T ≤ 6` s. At `T = 6`, `uT = 24`, so `W ≈ 8,000 / 6 ≈ 1,333` writes per second.
3. Misses go from 3% to 15% of 50,000, from 1,500 to 7,500 database reads per second. That is five times the load.
4. The trade transaction reads both inventories from PostgreSQL. If A's latest changes are still dirty in the cache, the transaction works from old data and may, for example, let A trade a sword they already sold. And if the trade commits while A's older cached state is still waiting to be flushed, that later flush can write the sword back into A's row unless version numbers stop it. Flushing both players first makes PostgreSQL the single up-to-date copy while the transaction runs.

</details>

## Lab / assignment hook

[Lab 08, the write-behind flusher](../labs/lab08.md). You finish a write-behind cache over SQLite with a dirty set, versioned upserts and a crash switch. You then run it at several flush intervals, compare the measured write rates with `N × (1 − e^(−uT)) / T`, and measure the loss after simulated crashes. Deliverable: a results table, one plot, and a policy memo for the five data types from the in-class activity.

## Sources

- Minecraft Wiki, "Autosave" (Java Edition, current as of 1.21.x, accessed September 2026). Autosave every 6,000 ticks (5 minutes) and when a single-player opens the pause menu. https://minecraft.wiki/w/Autosave
- Minecraft Wiki, "Tick" (Java Edition). The game normally runs at 20 ticks per second. https://minecraft.wiki/w/Tick
- Redis documentation, "Redis persistence" (Redis 8.x docs, accessed September 2026). `appendfsync everysec` is the default and may lose one second of data; `always` is very slow. https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- Redis documentation, "Diagnosing latency issues". Many keys expiring in the same second can block Redis. https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/
- PostgreSQL 18 documentation, "Asynchronous Commit" (section 28.4) and "Write Ahead Log" settings. `wal_writer_delay` default 200 ms; risk window up to three times that; replay in commit order. https://www.postgresql.org/docs/current/wal-async-commit.html
- Epic Games, "Postmortem of Service Outage at 3.4M CCU" (Fortnite news, 8 February 2018). 132k database writes per second at peak; matchmaking shard write queueing past 40,000 ms; Memcached failure with 100 ms timeouts saturating Nginx on 4 February 2018, 18:30 to 20:20 UTC; planned fixes including removing unnecessary backend calls and batching. Posted by "The Epic Team" and dated 2.8.2018 on the page. Re-read in full via the Internet Archive copy of the epicgames.com post in September 2026; every figure here matches it.
- Nishtala, R. et al. (2013). "Scaling Memcache at Facebook." 10th USENIX Symposium on Networked Systems Design and Implementation (NSDI '13). Demand-filled look-aside cache with delete on write; leases issued at most once per 10 s per key; herd-prone keys fell from 17K to 1.3K peak database queries per second. https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 7 (durability and what a commit promises).

## Interactive spec: examples/w08-write-behind-tradeoff.html

**The one insight:** database writes fall off a cliff in the first few multiples of `1/u` and then flatten, while crash loss keeps rising in a straight line. Past the knee, buffering longer buys almost nothing.

**Layout.** Two linked charts side by side on desktop, stacked on mobile, sharing the same log-scale x-axis (flush interval `T` from 0.01 s to 1,000 s). A readout table below.

- **Left, "Database writes per second".** Curve `W(T) = N × (1 − e^(−uT)) / T`. Horizontal dashed line at `N × u` labelled "write-through". Vertical cursor at the current `T`. Shade the band `1/u ≤ T ≤ 3/u` and label it "knee". y-axis log scale from 0.1 to `2 × N × u`.
- **Right, "Expected progress lost per crash".** Line `T/2` (solid) and `T` (dashed, "worst case"), on the same x-axis, y-axis log scale seconds. Same cursor.
- **Optional third series (toggle "savings per second of loss")**, drawn on the left chart's secondary axis or as a small third chart: `S(T) = −dW/dT ÷ 0.5`, the writes saved per extra second of expected loss. Compute numerically by central difference on the log grid.

**Controls.**
- `N` players or entities: slider 1 to 50,000, default 5,000 (the minimum is 1 so the "Minecraft chunk" preset fits).
- `u` changes per player per second: log slider 0.001 to 50, default 2.
- `T` flush interval: log slider 0.01 s to 1,000 s, default 5 s.
- Preset buttons: "MMO shard" (N 5,000, u 2, T 5), "Minecraft chunk" (N 1, u 20, T 300), "Redis AOF everysec" (T 1), "PostgreSQL async commit worst case" (T 0.6).

**Readouts (exact, copyable).**
- `W_through = N × u`
- `W_behind` to one decimal, and the percentage cut `1 − W_behind / W_through`.
- Expected loss `T/2` and worst case `T`; changes lost per entry `u × T / 2`.
- Writes saved per second of extra expected loss at the current `T`.

**Test values (must match the lecture table), N = 5,000, u = 2.** T = 1 gives 4,323.3 (57% cut), loss 0.5 s. T = 5 gives 1,000.0 (90% cut), loss 2.5 s. T = 30 gives 166.7 (98.3%), loss 15 s. T = 300 gives 16.7 (99.8%), loss 150 s. Write-through 10,000. Check-yourself values, N = 8,000, u = 4: T = 0.25 gives 20,227.9; T = 1 gives 7,853.5; T = 10 gives 800.0.

**Behavior.** Moving any slider redraws both charts immediately. Keyboard operable sliders with visible values. Colors from the shared palette, with the write-through line distinguished by dash pattern as well as color. Respect `prefers-reduced-motion` (no animated transitions when set).
