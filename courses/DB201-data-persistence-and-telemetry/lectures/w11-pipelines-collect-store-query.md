# DB201 · Week 11 — Pipelines: Collect, Store, Query

**Why this matters:** Last week you designed events. This week they arrive, millions a day, some twice, some a day late, all needing to become a number on a dashboard in under a second. The same question can take 90 seconds or a fraction of a millisecond depending on how you stored the data, and the difference is design, not hardware.

**You will be able to:**
- Draw the four stages of a telemetry pipeline (collect, transport, store, aggregate) and name what can go wrong at each.
- Compute rows touched and query time for a question under four storage layouts, and the CPU load of a dashboard that runs it repeatedly.
- Make ingestion idempotent so retried batches do not inflate counts, in SQLite and in PostgreSQL.
- Choose a policy for late-arriving events and compute how incomplete a daily rollup is when it is built too early.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 11, the sections on message brokers, logs and idempotence (you met the event log last week). Chapter 3's section on column-oriented storage. Reread your week 4 notes on query plans.

**Prerequisites from earlier courses:** [DB201 week 10, telemetry design](w10-telemetry-design-events-and-properties.md) (envelope, properties, the storage model and the 40,000-DAU reference game). [DB201 week 4, indexes and query plans](w04-sql-ii-indexes-and-query-plans.md) (why an index turns a scan into a search). [DB201 week 7, Redis](w07-nosql-and-key-value-stores-redis.md) (the data types used in section 5). [CS102 week 6, queues and stacks](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md) (a buffer between a producer and a consumer). [CS202 week 2, latency, jitter and loss](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w02-latency-jitter-loss-measure-your-own.md) (why sends fail and get retried).

**Interactive:** [Query cost ladder](../examples/w11-query-cost-ladder.html). Keep it open during section 2.

---

## 1. The four stages

A **pipeline** is the path an event takes from the moment the game creates it to the moment a person sees it as part of a number. Every telemetry pipeline, from a student project to a studio with a data team, has the same four stages.

1. **Collect.** Game code (client or server) creates events and sends them to a **collector**, an HTTP endpoint whose only job is to accept them quickly. Events travel in **batches**: a client does not send one request per event, it gathers 20 or 100 or a few seconds' worth and sends them together.
2. **Transport.** The collector writes each batch into a **buffer**, a durable queue that holds events until the storage stage is ready for them. The buffer decouples arrival rate from write rate. During a launch-day spike events pile up in the buffer instead of being dropped.
3. **Store.** A loader reads from the buffer and writes to the **raw event store**, an append-only table (or set of files) that keeps every event as it arrived. Raw is the source of truth. You never edit it, and everything downstream can be rebuilt from it.
4. **Aggregate and serve.** Jobs read raw events and write smaller tables, called **rollups** or aggregates, shaped for specific questions: deaths per zone per day, active players per day, gold created per hour. Dashboards query the rollups.

```
game --batch--> collector --> buffer --> loader --> raw events --> rollup jobs --> rollups --> dashboard
      (collect)            (transport)          (store)                      (aggregate and serve)
```

Why so many stages? Because each one absorbs a different kind of trouble. The collector absorbs bursts of network traffic. The buffer absorbs the gap between arrival and storage speed, and survives a loader crash. The raw store absorbs your mistakes, since any bug in a rollup can be fixed by rebuilding it. The rollups absorb query load, so the dashboard does not read a billion rows every time someone opens it.

You built the smallest possible version of this in CS102 when an event bus handed events to listeners. Here the listener is on another machine, the network is unreliable and the volume is a million times larger.

## 2. Worked example: the query that took 90 seconds

### The hook

The same AWS case study you met last week describes Supercell's pipeline around 2015, when it ran Hay Day, Clash of Clans and Boom Beach. Events flowed through Amazon Kinesis, a managed buffer, at 45 billion a day, and landed in Amazon S3 at up to 10 TB a day. Do two divisions. 45 billion events over 86,400 seconds is about 520,000 events every second, all day. And reading 10 TB at a brisk 1 GB/s takes 10,000 seconds, nearly three hours, for one day of data.

So no one at that scale answers "how many battles were fought yesterday?" by reading yesterday's events. The pipeline has to arrange the data so that the question touches a tiny fraction of it. That arrangement is this week's model.

### The model

For the queries a dashboard runs (filter, then count or sum), the cost is dominated by how many rows the database has to touch.

```
query time ≈ rows touched / scan rate
```

- **Rows touched** depends on the storage layout, not on the answer. A query whose answer is 134 may touch 134 rows or 1.8 billion.
- **Scan rate** is how many rows per second one CPU core can read and filter. For simple filters over narrow rows it is in the tens of millions. In Lab 11, SQLite on the author's laptop scanned 392,736 rows in 21 ms, about 19 million rows a second. We use **20 million rows per second** as the model value.

The model ignores disk speed (assume the data is cached), index lookup cost beyond rows touched, and parallelism. It is for comparing layouts, and on that job it is accurate to an order of magnitude, which is all you need when layouts differ by factors of a thousand.

### Numbers you can check

Take the reference game from week 10: 40,000 DAU. Now count every event, deaths included. Each player sends about 500 events a day (deaths, kills, loot, zone changes, quest steps), so the game produces 20,000,000 events a day, of which 1,000,000 (5%) are deaths. You keep raw events for 90 days, so the raw table holds 1.8 billion rows. There are 40 zones.

The designer's question: **how many players died in zone 7 yesterday?**

| Layout | What the database touches | Rows touched | Time at 20 M rows/s |
|---|---|---|---|
| L0, one raw table, no index | every row ever stored | 1,800,000,000 | 90 s |
| L1, raw table partitioned by day | yesterday's partition only | 20,000,000 | 1 s |
| L2, L1 plus an index on (event type, zone) | yesterday's zone-7 deaths only | 25,000 | 1.25 ms |
| L3, a rollup `daily_zone_deaths(day, zone, deaths)` | one row | 1 | 0.05 µs, effectively 0 |

Check two lines by hand. L1 is 40,000 × 500 = 20,000,000 rows, and 20,000,000 / 20,000,000 per second is 1 second. L2 touches only deaths in zone 7: 1,000,000 deaths / 40 zones = 25,000 rows, and 25,000 / 20,000,000 = 0.00125 s.

Each step is a **layout decision**, and each one throws away rows before the query starts.

- **Partitioning** (L1) splits one logical table into physical pieces by a key, here the day. A query that filters on the day skips every other piece without opening it.
- **Indexing** (L2) you know from week 4. It lets the database jump to the matching rows inside the piece.
- **Pre-aggregation** (L3) does the counting once, when the rollup is built, and stores the answer.

The lab reproduces the ladder at small scale. On 14 days of events for 400 players (392,736 rows after removing duplicates), the full scan took 21 ms, the same query with an index on (event name, day) took 0.58 ms, and the rollup lookup took 0.004 ms. Different machine, different scale, same shape. Each layout step cut the time by a factor of 30 to 150.

Now a dashboard. It has 20 tiles like this one, 10 people keep it open, and it refreshes every minute. That is 200 queries a minute.

| Layout | CPU-seconds per minute | Cores kept busy |
|---|---|---|
| L0 | 200 × 90 = 18,000 | 300 |
| L1 | 200 × 1 = 200 | 3.33 |
| L2 or L3 | under 1 | under 0.02 |

This is where the model earns its keep. L0 is not "slow". It is impossible: 300 cores to keep one dashboard live. L1 is affordable but wasteful. L3 is free at query time, because the cost moved to the rollup job, which scans one day's partition once (1 second) and writes 40 rows.

### The visual

Open `examples/w11-query-cost-ladder.html`. The left view is the ladder, four horizontal bars, one per layout, on a logarithmic axis of rows touched, with the query time printed beside each. Move the DAU slider from 40,000 to 1,000,000. The L0, L1 and L2 bars grow by the same factor of 25 (L3 stays at one row), and L0 goes from 90 seconds to over half an hour. Move the retention slider from 90 to 365 days. Only L0 moves. Partitioning made the query's cost independent of how much history you keep.

The right view is the price. It lists eight questions a designer might ask tomorrow ("deaths in zone 7 by hour", "deaths by mob", "median time between death and quitting", and so on). Click a layout, and each question is marked answerable or not. L0, L1 and L2 answer all eight, because they still hold every raw event. L3 answers exactly one, the question it was built for. Faster and narrower are the same move.

### Cross-game recognition

**Supercell (AWS case study, c. 2015).** Map its pipeline onto our four stages. Collection by the game servers. Transport through Kinesis. Raw storage in S3, with long-term archives in Amazon Glacier. Aggregation through Hadoop jobs on Amazon EMR feeding a data warehouse, and a second path from Kinesis into DynamoDB for data needed in real time. Two serving paths, one for dashboards and one for live features, both fed from the same buffer. That is the standard shape at scale.

**GameAnalytics (collection API documentation, 2025-2026).** The client side of the collect stage is documented openly. Events are sent as a batch in one POST whose body must stay under 1 MB (1 to 2 MB returns HTTP 413, above 2 MB the connection is closed), gzip compression is strongly recommended, and the client should resubmit only if it was offline or got a 413, never after a 400. On the serving side, as you saw last week, its aggregated metrics drop event ids that exceed the cardinality limits, while its raw data export keeps them. That is the L3 versus L0 trade-off, made by a vendor on your behalf: fast dashboards over pre-decided dimensions, raw data for everything else.

**World of Warcraft's combat log file (since patch 2.4.0, 2008).** A player-run pipeline. The `/combatlog` command makes the client append every combat event to a local file, `Logs\WoWCombatLog.txt`, in the envelope-plus-properties format from week 10. Patch 2.4.0 (March 2008) changed the file format to make it easier for programs to read. Players then upload the file to hosted parsers such as Warcraft Logs, which turn it into per-fight tables of damage, healing and deaths. Map it: the client collects, the file is the buffer, the upload is transport, and the parser's tables are rollups. The per-fight tables answer the common questions instantly, and anything unusual, such as "damage taken from one boss ability in the second phase", goes back to the raw log.

Across all three the pattern repeats. A buffer between sender and store, an append-only raw layer, and small pre-shaped tables for the questions that get asked every day. When you meet a new analytics setup, find the rollups first. They tell you which questions the team decided were worth answering fast.

### Design judgment

- **Keep raw, always.** Every rollup is a bet about which questions matter. When the bet is wrong, and it will be after the first patch, you rebuild from raw. If raw is gone, you cannot. Keep it for as long as privacy rules allow ([week 13](w13-privacy-gdpr-and-data-retention.md) sets that window).
- **Partition by the column every query filters on.** For telemetry that is almost always time. Partitioning by player or by event type helps a few queries and hurts the rest.
- **Build rollups for questions asked daily, not for questions asked once.** A one-off investigation can wait 1 second on L1. A dashboard tile cannot run 18,000 CPU-seconds a minute.
- **Name the rollup's grain.** "One row per day per zone" is the grain of `daily_zone_deaths`. Anything finer (hour, mob, player) cannot be recovered from it. Write the grain in the table's comment.
- **Do not over-optimize the cheap end.** Once a query takes a millisecond, the network round trip to the dashboard is larger than the query. Stop there.

## 3. Collecting: batches, retries and duplicates

### Batching

A client that sends each event in its own HTTP request pays the request overhead (headers, TLS, a round trip) every time. Batching amortizes it.

```
requests per second = events per second / batch size
events at risk      ≤ event rate per client × flush interval
```

The first line says why batches exist. At Supercell's 520,000 events a second, a batch size of 1 would mean 520,000 requests a second. A batch of 100 brings that to 5,200.

The second line is the cost. Events waiting in a client's batch are lost if the game crashes or the phone dies before the flush. A player generating one event every 15 seconds, flushed every 60 seconds, risks at most 4 events. Flushed every 10 minutes, 40. Most SDKs flush on a timer, on a batch-size limit, and when the game goes to the background, and write unsent batches to local storage so a crash loses nothing that was already on disk.

### At-least-once delivery

Here is the failure that bites every pipeline. The client sends a batch. The collector stores it and replies "OK". The reply is lost (the player walked into an elevator). The client never saw "OK", so it sends the batch again. The collector now has it twice.

The client cannot tell "the batch never arrived" from "the batch arrived but the reply did not". The only safe rule for the client is to retry until it sees an acknowledgement, which guarantees each event arrives **at least once** and sometimes more. The network alone cannot promise **exactly-once** delivery. Kleppmann's chapter 11 shows how systems get the same effect another way. Make the storage step **idempotent**, so that writing the same event twice has the same result as writing it once.

That is why the week 10 envelope starts with `event_id`. It is created by the sender, once, when the event happens, and it travels with every retry. Make it the primary key and tell the database to skip conflicts.

```sql
-- PostgreSQL (9.5 and later)
INSERT INTO raw_events (event_id, event_type, event_time, received_at, player_id, session_id, build_id, properties)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
ON CONFLICT (event_id) DO NOTHING;

-- SQLite (the lab)
INSERT OR IGNORE INTO raw_events (...) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
```

In Lab 11's landing file, 2% of batches were sent twice. That produced 8,182 duplicate lines out of 400,918, and without the key every count in the lab came out about 2% high. On the day you test a balance change that moves deaths by 2%, that error is the whole effect.

One PostgreSQL detail. On a partitioned table, a unique constraint must include the partition key. So the real key is `(event_time, event_id)`, which still works because a retried event carries the same `event_time`. SQLite has no partitioning, so the lab uses `event_id` alone.

## 4. Storing: time, lateness and layout

### Which day does an event belong to?

Every event carries two clocks. `event_time` is when it happened, by the sender's clock. `received_at` is when the collector got it, by your clock. They differ by seconds usually, and by hours or days when a client was offline.

A daily rollup has to pick. Almost always the right grain for design questions is `event_time` (a death on Tuesday belongs to Tuesday). But then Tuesday's numbers keep changing after Tuesday ends, as late events trickle in.

In the lab, 1% of batches arrived after midnight, some up to three hours late. That was 4,485 late events out of 392,736. If you build the rollup for 5 March at 00:05 on 6 March, it is missing 6 of that day's 848 deaths, 0.7%. Build it at 03:00 and it is complete.

Three policies, from simple to careful.

1. **Build once, late.** Build day d's rollup at a fixed time after midnight (say 04:00 UTC) and never touch it again. Anything later is lost from the rollup (still in raw). Simple and good enough for most dashboards.
2. **Rebuild a sliding window.** Every night, rebuild the last 3 days. Numbers for recent days can change a little, which you show on the dashboard ("last 3 days provisional").
3. **Watermark.** Track, per source, the oldest `event_time` still possibly in flight. A day is "closed" when every source's watermark has passed its end. Kleppmann's chapter 11 discusses these late "straggler" events and how a system decides a time window is complete.

Whichever you pick, the rollup job must be idempotent too. Delete the day's rows and insert fresh ones in one transaction (week 5), or use `INSERT ... ON CONFLICT (day, zone) DO UPDATE`. Running it twice must give the same table.

### Clocks you cannot trust

A client clock can be wrong by hours or years. A common defensive rule at load time. If `event_time` is more than 5 minutes after `received_at`, or more than 7 days before it, keep the event but flag it and use `received_at` for rollups. Server events have no such problem, which is one more reason (after week 10's trust argument) to send gameplay facts from the server.

### Layout in PostgreSQL

The reference stack does L1 and L2 with standard features.

```sql
CREATE TABLE raw_events (
  event_id    uuid        NOT NULL,
  event_type  smallint    NOT NULL,
  event_time  timestamptz NOT NULL,
  received_at timestamptz NOT NULL,
  player_id   bigint      NOT NULL,
  session_id  uuid        NOT NULL,
  build_id    int         NOT NULL,
  properties  jsonb       NOT NULL,
  PRIMARY KEY (event_time, event_id)
) PARTITION BY RANGE (event_time);

CREATE TABLE raw_events_2026_03_05 PARTITION OF raw_events
  FOR VALUES FROM ('2026-03-05') TO ('2026-03-06');

CREATE INDEX ON raw_events (event_type, ((properties->>'zone_id')::int));

-- retention: drop a whole day in one step instead of deleting 20 million rows
DROP TABLE raw_events_2026_01_01;
```

Declarative partitioning exists since PostgreSQL 10. `EXPLAIN` shows **partition pruning**: only the partitions matching the `WHERE` clause appear in the plan. The last line is the other gift of partitioning. Dropping a partition is instant and leaves no dead rows behind, where `DELETE` of 20 million rows would take minutes and leave the table bloated until vacuumed (week 13 shows why that matters for erasure).

SQLite, used in the lab, has no partitioning. An index on the day column gets you most of the L1 benefit at lab scale.

### Row stores and column stores

PostgreSQL is a **row store**: each row's columns sit together on disk. A query that reads 3 columns out of 15 still reads whole rows. **Column stores** (the design used by most analytics warehouses) keep each column separately, so the same query reads about 3/15 of the bytes, and similar values stored together compress very well. Kleppmann's chapter 3 explains the layout.

For this course the rule of thumb is simple. PostgreSQL with partitions and rollups is comfortable up to the tens of millions of events a day of our reference game. Well beyond that, studios move the raw layer to a column store and keep PostgreSQL for the game's own state.

## 5. Where Redis fits

Redis from [week 7](w07-nosql-and-key-value-stores-redis.md) has two jobs in a telemetry pipeline.

**The buffer.** A Redis stream is an append-only log inside Redis. The collector appends each batch with `XADD`. Loader processes read with `XREADGROUP` as a **consumer group**, so several loaders share the work, and each loader confirms a batch with `XACK` only after it has committed the rows to PostgreSQL. If a loader dies mid-batch, the batch stays pending and another loader claims it. Note that this is at-least-once again. The loader may have written the rows just before dying, and the next loader writes them again. The `ON CONFLICT DO NOTHING` from section 3 is what makes that harmless.

**Real-time counters.** Some numbers are needed within seconds, not after tonight's rollup: "deaths in the last minute" on a live-ops screen during a world event, for example. The loader can `INCR` a key such as `deaths:zone:7:2026-03-05T19:42` as it writes each death and set it to expire after an hour. The dashboard reads 60 keys for the last hour. This is a rollup maintained on write instead of computed on a schedule, with the same trade-off as L3. Fast, and only for the question it was built for.

Redis holds data in memory, and week 7 showed what it keeps after a crash. Treat Redis counters as a fast approximation. Raw events in PostgreSQL remain the record.

## In-class activity (25 minutes)

In groups of three. Your MMO has 150,000 DAU, 400 events per player per day, 60 zones, and a 180-day raw retention. Deaths are 4% of events. Use the model's 20 million rows a second.

1. Compute rows per day, the size of the raw table, and rows touched for "deaths in zone 12 yesterday" at L0, L1, L2 and L3. (8 minutes)
2. The live-ops team wants a wall screen with 12 tiles refreshed every 30 seconds, and 25 analysts each run about 40 ad hoc queries a day. Decide which layout serves each group. Estimate the CPU load of the wall screen for your choice. (8 minutes)
3. Pick a late-event policy (build once, sliding window, or watermark) for the wall screen and for a weekly report to the producer. Justify each in one sentence. (5 minutes)
4. Present to another group. They must name one question your rollups cannot answer. (4 minutes)

Expected output: a table like section 2's with your numbers (L0 is 150,000 × 400 × 180 = 10.8 billion rows, 540 s), a layout choice per audience, and two late-event policies.

## Common misconceptions

- **"A faster database fixes a slow dashboard."** A machine twice as fast turns L0's 90 seconds into 45. A rollup turns it into microseconds. Layout changes are worth factors of thousands. Hardware is worth factors of two.
- **"Retries are rare, so duplicates don't matter."** In the lab 2% of batches were retried, and counts came out 2% high. Balance changes are often judged on effects of a few percent. Deduplicate at load time, always.
- **"The rollup is the data."** The rollup is one answer computed from the data. Delete raw and you lose every question you did not think of. Rollups are disposable, raw is not.
- **"Group events by when they arrived, it's simpler."** Then a day of offline play lands on the day the player reconnected, and a server outage looks like a drop in deaths followed by a spike. Group by `event_time`, and choose a policy for lateness.

## Check yourself

1. A game produces 6 million events a day and keeps 30 days of raw data. How many rows does "count yesterday's quest completions" touch under L0 and L1, and how long does each take at 20 million rows a second?
2. A client emits one event every 12 seconds and flushes every 90 seconds. At most how many events are lost if the game crashes? What flush interval keeps the worst case at 3 events?
3. Your loader wrote a batch of 500 events to PostgreSQL and crashed before calling `XACK`. Another loader picks up the batch. Without `ON CONFLICT DO NOTHING`, what happens? With it?
4. In the lab data, the 5 March rollup built at 00:05 was missing 6 of 848 deaths. The live team compares 5 March with 4 March (built at 04:00, complete) and reports "deaths fell 0.7% after the hotfix". What is wrong with the comparison?
5. A dashboard runs 300 queries a minute, each at L1 on a table with 50 million rows a day. How many cores does it keep busy? What would you change?

<details>
<summary>Answers</summary>

1. L0 touches 6,000,000 × 30 = 180,000,000 rows, 9 s. L1 touches one day, 6,000,000 rows, 0.3 s.
2. A 90-second window holds 90 / 12 = 7.5 event intervals, so 7 or 8 events depending on where the crash falls. Plan for 8. For a worst case of 3 events, flush at least every 3 × 12 = 36 seconds.
3. Without it, if `event_id` is not a key, all 500 events are stored twice and every count that includes them is inflated. If `event_id` is a primary key without `ON CONFLICT`, the insert fails with a unique violation and the second loader keeps retrying a batch it can never write. With `ON CONFLICT DO NOTHING`, the second write skips all 500 rows and the loader acknowledges the batch. Same result as writing once.
4. The two days were built with different completeness. The 0.7% drop is exactly the late events the 00:05 build missed, so the "effect" may be entirely an artifact. Rebuild 5 March after its late events arrive (or compare two days built at the same lag) before reading anything into it.
5. Each query touches 50,000,000 rows, 2.5 s. 300 × 2.5 = 750 CPU-seconds per minute, 12.5 cores. Build rollups at the grain the tiles need, or add indexes so each tile is an L2 query.

</details>

## Lab / assignment hook

[Lab 11, a telemetry pipeline in SQLite](../labs/lab11.md). You load a landing file of 400,918 events with retries and late arrivals, make ingestion idempotent, build the `daily_zone_deaths` rollup, measure the ladder of section 2 on your own machine, and quantify the late-event gap. Deliverable: your `pipeline.py`, a results table and a 300-word recommendation.

## Sources

- Amazon Web Services, "Supercell Case Study" (version with these figures first archived by the Internet Archive in January 2016, when Supercell had three games). Amazon Kinesis carrying 45 billion events per day; up to 10 TB of game event data per day in Amazon S3; Amazon Glacier for archives; Amazon EMR feeding a data warehouse on EC2; Kinesis data also read into DynamoDB.
- GameAnalytics documentation, "API limitations" and "Event types" (collection API, accessed September 2026). 1 MB POST body limit and the 413 and connection-close behavior, gzip recommendation, resubmit only when offline or on 413, never on 400.
- Warcraft Wiki, "Combat Log" (accessed September 2026). The `/combatlog` command, the `Logs\WoWCombatLog.txt` file, the patch 2.4.0 (25 March 2008) format change for programs, and hosted parsers such as Warcraft Logs.
- PostgreSQL 17 documentation, "Table Partitioning" (declarative partitioning since version 10, partition pruning, unique constraints must include the partition key, dropping partitions for retention) and "INSERT" (`ON CONFLICT`, since version 9.5).
- SQLite documentation, "INSERT" and "The ON CONFLICT clause" (`INSERT OR IGNORE`).
- Redis documentation, "Redis Streams" (`XADD`, `XREADGROUP`, consumer groups, `XACK`, pending entries).
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 3 (column-oriented storage) and chapter 11 (log-based message brokers, idempotence, exactly-once semantics, straggler events and time windows).
- Lab 11 measurements: `labs/lab11-starter`, seed 1111, 400 players, 14 days, SQLite 3.53 on Python 3.13, Apple Silicon laptop, September 2026.

## Interactive spec: examples/w11-query-cost-ladder.html

**The one insight.** Storage layout, not hardware, decides query cost, by factors of thousands. The fastest layout is also the narrowest. A rollup answers only the question it was built for.

**Layout.** Two linked views, stacked on phones, side by side at 1,000 px and wider. Sliders above both.

**Controls.**
- DAU: 1,000 to 1,000,000, log scale, default 40,000.
- Events per player per day: 50 to 2,000, default 500.
- Share of events that are deaths: 1% to 20%, default 5%.
- Zones: 5 to 200, default 40.
- Raw retention in days: 7 to 365, default 90.
- Scan rate in million rows per second: 1 to 100, log scale, default 20.
- Dashboard load: queries per minute, 1 to 1,000, default 200.

**Left view, the ladder.** Four horizontal bars L0 to L3 on a log axis of rows touched from 1 to 10^12. Beside each bar: rows touched, query time (formatted in µs, ms, s, min or h), and dashboard cores busy.

**Formulas.**
- `rowsPerDay = DAU × eventsPerPlayer`
- `L0 = rowsPerDay × retentionDays`
- `L1 = rowsPerDay`
- `L2 = rowsPerDay × deathShare / zones`
- `L3 = 1`
- `time = rows / (scanRate × 1e6)` seconds
- `coresBusy = queriesPerMinute × time / 60`
- Also show, under L3, the rollup's build cost once per day (`L1 / scanRate` seconds) and its size (`zones × retentionDays` rows).

**Right view, what each layout can answer.** Clicking a bar selects that layout. A list of eight questions, each marked answerable or not for the selected layout. Questions: (1) deaths in zone 7 yesterday; (2) deaths in zone 7 yesterday by hour; (3) deaths by mob last week; (4) heat map of deaths in zone 7; (5) deaths per player for the top 100 players; (6) median minutes between a death and session end; (7) deaths before and after build 1406; (8) all item loot yesterday. L0, L1 and L2 answer all eight. L3 answers only (1), and (7) only if the build changed at midnight, which the card notes. Include a small note under L2 that questions not using the (event type, zone) index fall back to L1 speed.

**Test values (defaults).** Rows per day 20,000,000. L0 1,800,000,000 rows, 90 s, 300 cores. L1 20,000,000 rows, 1 s, 3.33 cores. L2 25,000 rows, 1.25 ms, 0.0042 cores. L3 1 row, 0.05 µs (the lecture table adds "effectively 0"). Rollup build 1 s per day, 3,600 rows. With DAU 1,000,000: L0 45,000,000,000 rows, 2,250 s (37.5 min). With retention 365 and DAU 40,000: L0 7,300,000,000 rows, 365 s, while L1 stays 1 s.

**Accessibility.** Bars are also a table for screen readers. Sliders keyboard-operable with visible values. Shared palette from `templates/interactive-tokens.css`. No game art.
