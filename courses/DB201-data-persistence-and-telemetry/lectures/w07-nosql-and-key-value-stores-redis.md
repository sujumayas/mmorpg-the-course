# DB201 · Week 07 — NoSQL and Key-Value Stores (Redis)

**Why this matters:** Some questions a game asks thousands of times a second are awkward for a relational database. "What rank am I?" is the classic one. A key-value store such as Redis answers it in microseconds, but it keeps its data in memory and makes weaker promises about keeping it. You need to know which questions to move out of PostgreSQL, and what you give up when you do.

**You will be able to:**
- Compute the cost of a rank query in PostgreSQL and in a Redis sorted set for a leaderboard of N players, and predict which players pay the most.
- Design Redis keys and pick a data type (string, hash, sorted set, set, list) for five common game features.
- State what a Redis crash loses under each persistence setting (RDB snapshots, AOF with `everysec`, AOF with `always`).
- Decide, for a given feature, whether the source of truth belongs in PostgreSQL, in Redis, or in both, and justify it with a number.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 2, "Data Models and Query Languages", the sections on the relational versus document model. Redis documentation, "Redis sorted sets" (read the leaderboard example) and "Redis persistence" (the RDB and AOF sections).

**Prerequisites from earlier courses:** [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (what a hash map costs and why). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (O(log n) versus O(n) in practice). From this course, [week 4, indexes and query plans](w04-sql-ii-indexes-and-query-plans.md) (B-trees and covering indexes) and [week 5, transactions and ACID](w05-transactions-and-acid.md).

**Interactive:** [examples/w07-rank-query-cost.html](../examples/w07-rank-query-cost.html). Keep it open during section 2.

---

## 1. What "NoSQL" means, and what a key-value store is

"NoSQL" is a label, not a design. It covers any database that does not use the relational model you have used since week 2. Four families matter for games:

- **Key-value stores** (Redis, Memcached). You give a key, you get a value. The store knows nothing about what is inside the value unless the value has one of a few built-in types.
- **Document stores** (MongoDB, Google Cloud Datastore and Firestore). The value is a document, usually JSON-like, and the store can index fields inside it.
- **Wide-column stores** (Cassandra, ScyllaDB). Rows grouped by a partition key, tuned for very high write rates.
- **Graph databases** (Neo4j). Nodes and edges, tuned for "friends of friends" queries.

This week is about the first family, with a short look at the second. The other two turn up again in MMO302.

A **key-value store** is a hash map (CS102 week 5) that lives in another process, usually on another machine, reached over the network. That sentence gives you its whole cost model:

```
time per operation ≈ network round trip + work inside the store
```

Inside the store, a `GET` on a hash map is O(1) and takes well under a microsecond. The round trip over a datacenter network is about 200 microseconds, according to the Redis latency documentation for a 1 Gbit/s link. So the network dominates by a factor of a hundred or more. Two rules follow, and you should keep both in mind whenever you touch Redis:

1. **Count round trips, not operations.** Ten `GET`s sent one at a time cost about 2 ms. The same ten sent as one `MGET` or one pipeline cost about 0.2 ms.
2. **Watch for commands that are not O(1).** Redis runs every command on a single thread, one after another. A command that walks a million elements blocks every other client until it finishes. The documentation singles out `KEYS` as a common cause of production latency for exactly this reason.

### Redis in one page

Redis (the name comes from "remote dictionary server") stores keys whose values have a type. The types you will use in games:

| Type | What it is | Game use | Typical commands and cost |
|---|---|---|---|
| String | Bytes, or an integer you can increment | Session token, counter, cached JSON blob | `GET`, `SET`, `INCR`: O(1) |
| Hash | A small map of field to value | One player's live stats | `HGET`, `HSET`, `HINCRBY`: O(1) per field |
| List | A double-ended queue | Recent chat lines, a job queue | `LPUSH`, `RPOP`: O(1); `LRANGE`: O(k) |
| Set | Unordered unique members | Who is online in zone 7 | `SADD`, `SISMEMBER`: O(1) |
| Sorted set | Unique members, each with a numeric score, kept in score order | Leaderboards, matchmaking by rating | `ZADD`, `ZINCRBY`, `ZRANK`, `ZREVRANK`, `ZCOUNT`: O(log N) |

Every key can carry a **TTL** (time to live) set with `EXPIRE`, after which Redis deletes it. That makes Redis a natural home for data that should vanish on its own: login sessions, "this player is in a match" flags, rate-limit counters.

Keys are plain strings, so you invent the structure with a naming convention. The common one uses colons: `player:48213:stats`, `zone:7:online`, `lb:season12:arena`. Keep that convention in a document your whole team shares. A typo in a key name is not an error in Redis. It is a new, empty key.

### Atomic by construction

Because one thread runs all commands in order, each command is atomic. `INCR gold:48213` can never lose an update to a race, which is the bug you studied in week 6. `MULTI` and `EXEC` group several commands so that no other client's command runs in the middle of them.

That is less than a PostgreSQL transaction, and the difference matters for games. If a command inside `MULTI ... EXEC` fails at run time, the Redis documentation says the other commands still run, and Redis has no rollback. You get isolation (nobody interleaves) without all-or-nothing. A trade that must move gold and an item together, or not at all, belongs in PostgreSQL with the week 5 tools.

## 2. Worked example: "What rank am I?"

### The hook

Open any game with a global ranking of millions of players and look up your own position. The Redis documentation uses almost exactly this case to introduce sorted sets. It suggests them for "the highest scores in a massive online game", and it lists `ZRANK` and `ZREVRANK` at O(log N).

Here is the puzzle. You already know how to do this in SQL. The query is one line, the `score` column has a B-tree index (week 4), and the top of the leaderboard loads instantly. So why do so many game backends add a second database just to answer it? And why do the players who complain that "the leaderboard page is slow" tend to be the ones in the middle of the pack, not the ones at the top?

### The model

Take a leaderboard with `N` players. Your rank is `r`, the number of players with a higher score than yours, plus one.

**In PostgreSQL** you store `scores(player_id, score)` with an index on `score` and ask:

```sql
SELECT COUNT(*) + 1 AS rank
FROM scores
WHERE score > (SELECT score FROM scores WHERE player_id = $1);
```

The index lets the database jump straight to your score. It then has to count every index entry above it, one at a time, because a PostgreSQL B-tree does not store how many entries sit under each branch. So the work is:

```
SQL entries read   ≈ r − 1              (grows with how far down you are)
SQL time           ≈ (r − 1) × c
```

where `c` is the cost of reading one index entry. On a laptop, SQLite's covering-index count reads about 5 ns per entry with everything in memory (you will measure this in the lab). PostgreSQL's index-only scan does more work per entry, so treat 5 ns as a best case.

**In Redis** the sorted set is a skip list (a linked list with extra "express lane" pointers) plus a hash table, per the Redis documentation. Each express-lane pointer also records how many members it skips, its **span**. To find your rank, Redis walks down from the top lane and adds up the spans it passes. The work is:

```
skip list steps    ≈ a small multiple of log₂ N   (the same for every player)
```

That is the whole model. The SQL cost depends on **your rank**. The sorted-set cost depends only on **the size of the board**, and only logarithmically.

### Numbers you can check

Take `N = 2,000,000` players, `c = 5 ns` per index entry, and a skip list that visits about `2 × log₂ N ≈ 42` nodes.

| Your rank r | SQL entries read | SQL time at 5 ns/entry | Sorted-set steps |
|---|---|---|---|
| 10 | 9 | 0.05 µs | ≈ 42 |
| 1,000 | 999 | 5 µs | ≈ 42 |
| 100,000 | 99,999 | 0.5 ms | ≈ 42 |
| 1,000,000 (median) | 999,999 | 5 ms | ≈ 42 |
| 2,000,000 (last) | 1,999,999 | 10 ms | ≈ 42 |

Now scale it to a load. After each match, players open the results screen, which shows their new rank. Say 2,000 rank lookups a second at peak, spread evenly across the board. The average player sits at rank `N/2`, so the average SQL lookup reads a million entries:

```
CPU time per second = 2,000 lookups × 1,000,000 entries × 5 ns = 10 seconds
```

Ten seconds of CPU work every second means ten cores doing nothing but counting, and that is with the optimistic 5 ns. The same 2,000 lookups in Redis cost about 2,000 × 42 node visits, well under a millisecond of work, plus one network round trip each.

Notice who suffers. The top ten players get their rank in a fraction of a microsecond on either system. The player at rank 1,400,000 pays 7 ms in SQL, every time. The slow-leaderboard complaint comes from the middle and the bottom, which is where most of your players are.

### Move it

Open the interactive. The left view shows the leaderboard as one long bar, best at the left. Drag the "your rank" slider and the part of the bar that SQL has to count lights up. The right view plots work against rank on a log scale. The SQL line climbs steadily, and the sorted-set line stays flat. Raise `N` from 10,000 to 10,000,000 and watch the SQL line move up by three orders of magnitude while the sorted-set line moves by a few steps.

### The same idea in other games and systems

The principle is "pick the store by the question you ask most often." Here it is in three other places, each rewritten as "which access pattern, which store".

**Fortnite (Epic Games, February 2018).** In its postmortem of the outages at 3.4 million concurrent players, Epic described its game-profile service, which it calls MCP. It stored player profiles, statistics and items in MongoDB, a document store, spread over nine shards with user data spread across eight of them. At peak the service handled 124,000 client requests a second, which became 318,000 database reads and 132,000 writes a second. The dominant question there is "give me everything about player X", a lookup by key. A document keyed by player ID answers it in one read, with no joins. The trouble Epic reported came from the one shard that did not fit that pattern. Matchmaking sessions had to live in a single collection and queued writes up to 40 seconds and more at peak.

**Fortnite's account service (same postmortem).** Access-token checks were answered from Memcached, a pure key-value cache, in front of the main service, with Redis behind it. The question is "is token T valid?", asked tens of thousands of times a second, which is a textbook `GET`. Section 4 of [next week's lecture](w08-caching-and-write-behind.md) returns to what happened when that cache failed.

**Pokémon GO (Niantic on Google Cloud, launch in July 2016).** Google's reliability team wrote that Cloud Datastore, a document store, was the game's primary database for the game world. Traffic reached 50 times the launch target, ten times the worst case the teams had planned for. Again, the store was chosen for "look up and update this entity by key" at very high volume, not for ad hoc joins.

In every case you can rewrite the design as the same sentence you used for the leaderboard: *the hot question is X, and this store answers X in O(1) or O(log N) regardless of which player asks.* The leaderboard is the case where the relational answer is O(r), and r is large for most players.

### Eyes-open design judgment

A sorted set wins the rank question outright. It still is not free, and there are cheaper fixes in SQL that you should weigh first.

- **Rank snapshots in SQL.** Many games do not need a live rank. Recompute ranks for the whole board every five minutes with a window function, `RANK() OVER (ORDER BY score DESC)`, into a `rank_snapshot` table indexed by `player_id`. A lookup is then one index probe. The cost is staleness. A player who just won sees an old rank until the next run. For a weekly season board that is fine. For a live tournament it is not.
- **Score buckets.** If scores are integers in a known range (say an Elo-style rating from 0 to 5,000), keep a count per rating. Rank is then a sum over at most 5,000 buckets, or O(log 5,000) with a Fenwick tree (an array that stores running totals so any prefix sum takes log-many additions). This is exact and live, and needs no second database.
- **Memory.** A sorted set lives in RAM. Two million members at, say, 100 bytes each is about 200 MB, which is fine. One board per region, per mode, per season, per friend list multiplies quickly. Measure with `MEMORY USAGE` before you promise per-guild boards.
- **Durability.** If Redis restarts, the board is gone unless persistence brought it back (section 3). Keep scores in PostgreSQL as the source of truth, and write a rebuild script that reloads the sorted set from it. Test that script before launch.
- **Ties.** Redis orders members with equal scores by comparing the member strings byte by byte. So with equal scores, player `"10"` sorts before `"9"`. If your game says "earlier achiever wins ties", encode that in the score, for example `score × 10¹⁰ + (10¹⁰ − timestamp)`, and keep the result below 2⁵³, because scores are double-precision floats.

Decide two things on purpose. How fresh must the rank be, and how many players ask how often? Fresh and frequent points to a sorted set. Stale and rare points to a snapshot table.

### Check yourself on the worked example

1. A board has 500,000 players. Using `c = 5 ns`, what is the average SQL rank-lookup time across all players, and how many lookups per second can one core serve?
2. A designer proposes showing rank only to the top 1,000 players and "top X%" to everyone else. Which SQL query would compute "top X%" cheaply, and why is it cheaper than an exact rank?

<details>
<summary>Answers</summary>

1. The average rank is about 250,000, so about 250,000 entries at 5 ns, or 1.25 ms. One core serves about 1 / 0.00125 = 800 lookups a second.
2. Precompute the score thresholds at each percentile once (for example with `percentile_disc` in PostgreSQL, or by reading the score at position `N × X/100` from the index) every few minutes. Each player's lookup then compares their score against about 100 stored thresholds. The cost no longer depends on the player's rank.

</details>

## 3. What Redis keeps when it crashes

Redis holds everything in memory. What survives a crash depends on its persistence setting, and the Redis persistence documentation spells out the options:

| Setting | How it works | What a crash can lose |
|---|---|---|
| No persistence | Nothing written to disk | Everything |
| RDB snapshots | A forked child writes the whole dataset to `dump.rdb` on a schedule, for example `save 60 1000` (every 60 s if at least 1,000 keys changed) | Everything since the last snapshot, often minutes |
| AOF, `appendfsync no` | Every write command is appended to a log; the operating system decides when to flush | Up to about 30 s on a typical Linux setup |
| AOF, `appendfsync everysec` (the default for AOF) | The log is flushed to disk once a second in a background thread | About 1 s of writes |
| AOF, `appendfsync always` | Flush before replying to each batch of commands | Almost nothing; documented as very slow |

Put this next to the question from week 1: how much progress can a player lose? A leaderboard that can lose one second of score updates is fine, because the next match rewrites the score, and the source of truth is in PostgreSQL. A currency balance that can lose one second is a support ticket for every player who bought something in that second.

That gives you the default rule for this program's reference stack. **PostgreSQL holds anything a player would file a ticket about losing. Redis holds data that is derived, rebuildable or meant to expire.** Leaderboards, sessions, presence, rate limits and caches go in Redis. Inventories, wallets and trade history go in PostgreSQL.

You will break this rule in week 8, on purpose, when you let Redis hold recent changes for a few seconds before writing them to PostgreSQL. You will then have to count exactly what you lose.

## 4. Designing keys and picking types

Here are five features from an MMO, each with the key design and the reasoning.

**Login session.** `session:{token}` as a string holding the player ID, with `EXPIRE` set to 30 minutes and refreshed on activity. The only question is "who owns this token?", a pure `GET`. The TTL means logged-out players clean themselves up.

**Who is in zone 7.** `zone:7:online` as a set of player IDs. `SADD` on enter, `SREM` on leave, `SCARD` for the count shown on the map. Add a TTL-based heartbeat per player (`presence:{id}`, expires after 60 s), because a server crash never sends the `SREM`.

**Live combat stats for one character.** `char:{id}:live` as a hash with fields `hp`, `mana`, `x`, `y`. `HINCRBY char:77:live hp -35` is one atomic command. This is the data that changes many times a second. Next week you decide how often it gets written to PostgreSQL.

**Recent guild chat.** `guild:{id}:chat` as a list. `LPUSH` each message, then `LTRIM` to the latest 200 so the list never grows without bound. Permanent chat logs, if you keep them at all, go to the telemetry pipeline of week 11, not here.

**Arena ladder.** `lb:{season}:arena` as a sorted set. `ZINCRBY` after each match, `ZREVRANK` for "my rank", `ZREVRANGE 0 99 WITHSCORES` for the top 100, and `ZREVRANGE` around your own rank for "players near me".

A pattern to notice: the key name carries the part of the question that you know before you ask (which session, which zone, which season). The data type carries the operation you need (lookup, membership, order). If a feature needs you to scan many keys to find the one you want, the key design is wrong. Fix the key before you reach for `SCAN`.

### A short look at document stores

A document store keeps one JSON-like document per key and can index fields inside it. For a player profile that is read and written as a whole, like Fortnite's MCP profiles, that is convenient. One read returns everything, and adding a field needs no `ALTER TABLE`.

Kleppmann's chapter 2 calls this the **schema-on-read** approach. The database does not enforce a structure, so the code that reads the document has to handle every shape the document has ever had. The relational alternative is **schema-on-write**: the table enforces the structure, and changing it is an explicit migration. Week 9 is about doing that migration without taking the game down. Keep in mind that a document store does not remove the migration problem. It moves it into your reading code.

Document stores are weak where relational databases are strong. "Which players own at least one item of type 4471?" means scanning every profile unless you built an index for exactly that field in advance. For the economy analysis you will do in MMO304, that question comes up all the time.

## In-class activity (25 minutes)

Work in pairs. You are designing the online services for a small MMO with 200,000 players, 20,000 of them online at peak.

1. For each of these six features, write the Redis key pattern and type, or write "PostgreSQL" and one sentence why: friend list, currently-online friends, daily quest progress, guild bank contents, "last 50 players who killed this world boss", weekly dungeon-clear leaderboard.
2. For the leaderboard, estimate the SQL rank-lookup cost at `c = 5 ns` if each online player checks their rank once a minute. Is it worth a sorted set at this size?
3. For one feature you put in Redis, write down what happens to players if Redis restarts with RDB snapshots every 5 minutes. Is that acceptable?

Expected output: a six-row table, one cost estimate with the arithmetic shown, and a two-sentence crash analysis. Pairs swap tables and challenge one choice each.

## Common misconceptions

- **"NoSQL is faster than SQL."** Speed depends on the question. A primary-key lookup in PostgreSQL is also fast. The leaderboard gap comes from one specific operation, counting rows above a value, that the B-tree does not support in O(log N).
- **"Redis transactions are like database transactions."** `MULTI`/`EXEC` stops other clients from interleaving, but there is no rollback. If one command fails at run time, the rest still run.
- **"Redis is in memory, so it loses everything on restart."** That is true only with persistence off. With AOF and `everysec` it loses about a second. The right question is how much loss your feature can tolerate.
- **"A document store means I never need migrations."** You still change the shape of your data. The work moves from `ALTER TABLE` into every piece of code that reads old documents.

## Check yourself

1. A game server sends 12 separate `HGET` commands to load one character's live stats, with a 0.2 ms round trip each. How long does the load take? Rewrite it as one command and give the new time.
2. A board of 8,000,000 players uses SQL rank lookups at `c = 5 ns`. What is the lookup time for the player at rank 6,000,000? About how many steps does a skip list need for the same board?
3. Your team stores the in-game currency balance only in Redis, with AOF `everysec`. Describe the worst case a player could see after a crash, and propose a fix.
4. Scores are equal for players `"alice"` and `"Bob"` on a Redis board. Which appears first in `ZRANGE` (ascending), and why? Suggest a way to break ties by "who got the score first".

<details>
<summary>Answers</summary>

1. 12 × 0.2 ms = 2.4 ms. One `HGETALL char:{id}:live` (or `HMGET` with the 12 fields) takes one round trip, about 0.2 ms, so about 12 times faster.
2. About 6,000,000 × 5 ns = 30 ms. The skip list needs a small multiple of log₂ 8,000,000 ≈ 23, so roughly 46 steps.
3. A player buys an item, the purchase and the balance change are acknowledged, and Redis crashes before the next once-a-second flush. After restart the balance is back to its old value. If the item was granted somewhere else (for example in PostgreSQL), the player now has the item and the gold. That is a duplication. Fix it by keeping the balance in PostgreSQL and changing it in the same transaction as the item grant, as in week 5. Redis may cache the balance for display.
4. Equal scores are ordered by comparing the member strings byte by byte. `"B"` (byte 66) comes before `"a"` (byte 97), so `"Bob"` appears first. To break ties by time, fold the time into the score, for example `score × 10¹⁰ + (10¹⁰ − unix_seconds)`, so that an earlier timestamp gives a larger score. Check the result stays below 2⁵³.

</details>

## Lab / assignment hook

[Lab 07, ranks at scale](../labs/lab07.md). You load 200,000 players into SQLite, measure the SQL rank query at different ranks, finish a small skip list with spans so it answers `zrevrank` in O(log N), and compare both against a rank-snapshot table. Deliverable: a timing table, a plot of time against rank, and a 300-word recommendation for a 2-million-player board.

## Sources

- Redis documentation, "Redis sorted sets" (Redis 8.x docs, accessed September 2026). Sorted sets implemented as a skip list plus a hash table; leaderboard use case; equal scores ordered lexicographically; most operations O(log n). https://redis.io/docs/latest/develop/data-types/sorted-sets/
- Redis documentation, command pages for `ZRANK`, `ZREVRANK`, `ZADD`, `ZCOUNT` (time complexity O(log N)). https://redis.io/docs/latest/commands/zrank/
- Redis documentation, "Diagnosing latency issues". Mostly single-threaded command execution; slow commands block other clients; about 200 µs round trip on a 1 Gbit/s network; warning about `KEYS` in production. https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/
- Redis documentation, "Transactions". Commands in `MULTI`/`EXEC` run without interleaving; no rollback; other commands run if one fails after `EXEC`. https://redis.io/docs/latest/develop/using-commands/transactions/
- Redis documentation, "Redis persistence". RDB snapshots, AOF with `always`, `everysec` (default, about 1 s of loss) and `no` (Linux usually flushes every 30 s). https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
- Epic Games, "Postmortem of Service Outage at 3.4M CCU" (Fortnite news, 8 February 2018). MCP backed by 9 MongoDB shards; 124k client requests/s, 318k reads/s and 132k writes/s at peak; matchmaking shard write queueing past 40,000 ms; account-service token checks via Memcached with Redis behind it. Read via the Internet Archive copy of the epicgames.com post.
- Stone, L. (2016). "Bringing Pokémon GO to life on Google Cloud." Google Cloud blog, 29 September 2016. Cloud Datastore as the primary game-world database; traffic 50 times the target. https://cloud.google.com/blog/products/containers-kubernetes/bringing-pokemon-go-to-life-on-google-cloud
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 2 (document versus relational models, schema-on-read and schema-on-write).
- Timing of SQLite covering-index counts (about 5 ns per entry, 1,000,000 rows in memory, SQLite 3.53 on an Apple laptop) measured by the course team for this lecture; the lab reproduces it.

## Interactive spec: examples/w07-rank-query-cost.html

**The one insight:** the SQL rank query costs more the further down the board you are, while the sorted set costs the same for everyone. Most players are in the expensive part.

**Layout.** Two linked views side by side on desktop, stacked on mobile.

- **Left, "The board".** A horizontal bar representing all `N` players, rank 1 at the left. A marker shows "you" at rank `r`. The segment from rank 1 to `r − 1` is filled in the accent color and labelled "SQL counts these: {r − 1} entries". Under the bar, a thin strip shows a stylized skip list: 4-5 lanes of dots, with the path from the top-left down to "you" highlighted (about `2·log₂ N` highlighted hops, drawn schematically, not to scale). Label "Sorted set walks these: ≈ {steps} steps".
- **Right, "Work versus rank".** Log-log chart. x-axis rank from 1 to N. y-axis time in seconds from 1 ns to 1 s. Line A (SQL) `t = (r − 1) × c`, drawn from r = 2. Line B (sorted set) `t = steps × s`, flat. A vertical cursor at the current `r` with both values labelled. Shade the region between r = N/10 and r = N (90% of players) lightly and label it "90% of your players".

**Controls.**
- `N` players: log slider 10,000 to 10,000,000, default 2,000,000.
- Your rank `r`: log slider 1 to N, default 1,000,000. Keep `r ≤ N` when N changes.
- `c`, ns per index entry: slider 2 to 50, default 5.
- `s`, ns per skip-list step: slider 20 to 200, default 50.
- Lookups per second `L`: slider 100 to 20,000, default 2,000.
- Button "Median player" sets `r = N/2`. Button "Top 10" sets `r = 10`.

**Readouts (exact numbers, copyable).**
- SQL entries read `= r − 1`; SQL time `= (r − 1) × c`.
- Skip-list steps `= round(2 × log₂ N)`; sorted-set time `= steps × s`.
- Ratio SQL / sorted set.
- Load panel: SQL CPU-seconds per second at average rank `= L × (N/2) × c`, shown as "≈ K cores busy counting". Sorted-set CPU-seconds per second `= L × steps × s`.

**Test values (must match the lecture table).** With N = 2,000,000, c = 5 ns: r = 10 gives 9 entries and 45 ns (display "0.05 µs"); r = 1,000 gives 4.995 µs; r = 100,000 gives 0.5 ms; r = 1,000,000 gives 5.0 ms; r = 2,000,000 gives 10.0 ms. Steps = round(2 × log₂ 2,000,000) = round(41.9) = 42. Load at L = 2,000: 2,000 × 1,000,000 × 5 ns = 10.0 CPU-seconds per second.

**Accessibility and behavior.** All sliders keyboard operable with visible labels and current values. Line A and B distinguished by both color and dash pattern. No animation needed beyond the highlight moving; respect `prefers-reduced-motion`.
