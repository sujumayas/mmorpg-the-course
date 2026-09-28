# DB201 · Week 13 — Privacy, GDPR and Data Retention

**Why this matters:** Every telemetry event you designed in weeks 10 to 12 carries a player ID, and that makes it personal data. Somewhere a player will ask you to delete everything you hold about them, and the law gives you about a month. Whether that request costs two row deletions or a full scan of five terabytes was decided months earlier, when someone picked the schema and the retention window.

**You will be able to:**
- Compute the storage and erasure cost of a telemetry store from daily active users, events per player, bytes per event and retention days.
- Compare three erasure strategies (scan, index, pseudonym table) by rows examined per request, and say what each one costs at write time.
- Design a retention schedule for a game's data categories, with a purpose, a window and a deletion mechanism for each.
- Explain why `DELETE` does not remove bytes from disk in SQLite or PostgreSQL, and list the other copies an erasure must reach.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 2, the section on relational versus document models (you will reason about where one player's data lives). GDPR Articles 4(5), 5, 12, 15 and 17 and Recital 26 (gdpr-info.eu has a readable copy, about 20 minutes). Riot Games Privacy Notice, section III "How long we retain personal info" (5 minutes).

**Prerequisites from earlier courses:** [DB201 week 1, why persistence is hard](w01-why-persistence-is-hard-in-games.md) (bytes per second and the save-interval model). [DB201 week 2, relational modeling](w02-relational-modeling-characters-inventories-items.md) (primary and foreign keys). [DB201 week 4, indexes and query plans](w04-sql-ii-indexes-and-query-plans.md). [DB201 week 10, telemetry design](w10-telemetry-design-events-and-properties.md) (the events you are about to retain and erase). [DB201 week 11, pipelines](w11-pipelines-collect-store-query.md). Dashboards are [DB201 week 12, dashboards and KPIs](w12-dashboards-and-kpis.md). [CS102 week 5, hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (why hashing is fast, which matters in section 4). Children's privacy law (COPPA and the UK code) is covered later, in year 4, in [MMO402 week 11, minors in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w11-minors-in-online-worlds.md). This lecture does not repeat it.

**Interactive:** [w13-retention-and-erasure.html](../examples/w13-retention-and-erasure.html). Keep it open during section 2.

---

## 1. Personal data in a game

A game collects more personal data than most students expect. The account table is the obvious part: email, password hash, date of birth, country, payment tokens. The less obvious part is everything that carries an identifier. A telemetry event with `player_id = 81234` is personal data, because the studio can join it back to the account table. So is an IP address in a connection log, a character name in a chat log, a voice recording kept for abuse reports, and a device ID in a crash report.

The EU's General Data Protection Regulation (GDPR, in force since May 2018) is the law most studios design for, because it applies to the data of people in the EU wherever the studio sits. The UK has a near-copy called UK GDPR. You do not need to become a lawyer. You need five ideas from the text, because each one turns into a database requirement.

- **Data minimisation, Article 5(1)(c).** Personal data must be limited to what is necessary for the purpose you collected it for. In schema terms, every column needs a reason.
- **Storage limitation, Article 5(1)(e).** Data that identifies a person must be kept no longer than necessary for its purpose. In schema terms, every table needs a retention window and a job that enforces it.
- **Right of access, Article 15, and right to erasure, Article 17.** A person can ask for a copy of their data, and in many situations can ask you to erase it "without undue delay". In schema terms, you must be able to find every row about one person, and delete or unlink it.
- **The deadline, Article 12(3).** You must act on such a request within one month of receiving it. You can extend by two further months for complex cases, but you must tell the person within the first month. In schema terms, erasure has a service level of 30 days, and it will arrive at a steady rate forever.
- **Pseudonymisation, Article 4(5) and Recital 26.** Pseudonymised data is data that can no longer be tied to a person without extra information kept separately. Recital 26 says such data still counts as personal data, because the link exists. Truly anonymous data, where the person is no longer identifiable by any means reasonably likely to be used, falls outside the regulation.

The penalties are large enough that engineers get pulled into the discussion. Article 83(5) sets fines for breaking the principles or the data subject rights at up to 20 million euros or 4% of worldwide annual turnover, whichever is higher. A separate rule, Article 33, requires a studio to notify the regulator of a personal data breach within 72 hours of becoming aware of it where feasible. Every extra year of data you keep is data that can leak.

A note on scope. This lecture teaches the engineering, not legal advice. Real retention periods and erasure policies are set with a privacy lawyer, and they differ by country and by data category. Your job as the engineer is to make any reasonable policy cheap to carry out.

## 2. Worked example: the erasure bill

### The hook

Riot Games' privacy notice (last modified April 2026) says something most players never read. Voice chat from your match is kept for 24 hours so that other players can report it. If someone reports you and no action is taken, the recording is kept for 7 days. If action is taken, it can be kept for up to 2 years. Yesterday's voice chat from a clean match is already gone.

Notice what that sentence is. It is a database design. There is one kind of row, a voice recording, and three retention windows chosen by what happened to the row. The short default window means Riot does not have to find and erase most recordings when a player asks. They expire on their own. Keep that in mind while we build the same reasoning for the much larger telemetry store.

### The model

Take a mid-size MMO and its gameplay telemetry, meaning kills, loot, quests, trades, crafting and deaths. Name the quantities.

- `D`, daily active players. We use 40,000.
- `e`, events per active player per day. We use 1,500 (about 12 a minute over a two-hour session, no movement samples).
- `b`, stored bytes per event, including table overhead. We use 200.
- `R`, the retention window in days. This is the design choice.

The store holds the last `R` days, so:

```
rows stored   N_rows = D × e × R
storage       S      = D × e × b × R
```

With our numbers `D × e = 60,000,000` events a day and `D × e × b = 12 GB` a day. Storage is `12 GB × R`. Nothing surprising yet. Storage is a straight line in `R`, like week 1's save traffic was a straight line in the number of players.

Now add erasure requests. Let `q` be the number of erasure requests per month. We use 300, an invented figure for a game with about 150,000 monthly players. For each request you must remove or unlink every event about that player. There are three ways to do it.

**Strategy A, scan.** Events carry `player_id`, and there is no index on it. The table is partitioned by day (one partition per day, so old days can be dropped). Deleting one player's events reads every row in every partition:

```
rows examined per request (A) = D × e × R
```

**Strategy B, index.** Same events, plus an index on `player_id` in each daily partition. The database visits only that player's rows. If the player was active on `a` of the last `R` days:

```
rows examined per request (B) ≈ e × a      (a ≤ R)
```

The price is paid at write time. Every one of the 60 million daily inserts also updates an index, and the index takes space, which we estimate at about 24 extra bytes per row (a 12% storage increase over 200 bytes).

**Strategy C, pseudonym table.** Events never carry `player_id`. They carry a `telemetry_id`, a random value stored in exactly one place, a table that maps `player_id` to `telemetry_id`. Erasure deletes the account row and the mapping row:

```
rows examined per request (C) = 2
```

The events stay, but nothing links them to a person any more. Section 4 examines whether that is enough.

### Numbers you can check

Assume the store can scan 1 GB per second (an invented but realistic figure for one well-provisioned database server). One full scan then takes `12 GB × R / (1 GB/s) = 12 s × R`. Three hundred of them a month take `300 × 12 s × R = 3,600 s × R`. That is exactly **one hour of full-disk scanning per month for every day of retention**. The numbers were picked so that falls out cleanly, and it makes the table easy to verify.

| Retention R | Rows stored | Storage | One scan (A) | 300 scans a month (A) |
|---|---|---|---|---|
| 7 days | 420 million | 84 GB | 1.4 min | 7 h |
| 30 days | 1.8 billion | 360 GB | 6 min | 30 h |
| 90 days | 5.4 billion | 1.08 TB | 18 min | 90 h |
| 395 days (13 months) | 23.7 billion | 4.74 TB | 79 min | 395 h |
| 1,095 days (3 years) | 65.7 billion | 13.1 TB | 3.65 h | 1,095 h |

A month has 720 hours. At three years of retention, strategy A needs more scan time than the month contains. At 13 months it takes more than half of the month, on a server that also has to ingest 60 million new events a day.

Now compare the strategies per request, for a player who was active on 20 days inside the window:

| Strategy | Rows examined per request (R = 395) | Extra cost paid elsewhere |
|---|---|---|
| A, scan | 23.7 billion | none at write time; unusable at this scale |
| B, index | about 30,000 (1,500 × 20) | 60 million index updates a day; about 570 GB of index at R = 395 |
| C, pseudonym | 2 | events must never contain identifiers (section 4) |

Two changes to strategy A are worth computing, because teams reach for them first.

*Batch the requests.* Collect a week of requests and delete them all in one scan with `WHERE player_id IN (...)`. Four scans a month at R = 395 cost `4 × 79 min ≈ 5.3 h`, not 395 h. Batching fits comfortably inside the one-month deadline, and it is the cheapest fix if you already have strategy A in production.

*Shorten the window.* At R = 30, all of a player's raw events leave the store within 30 days even if you do nothing. The retention job itself becomes the erasure mechanism. This is the Riot voice chat design applied to telemetry.

The lab starter reproduces this at laptop scale. With 2,000 players, 40% active each day, 40 events each and 30 days, the store holds about 960,000 rows. On a 2025 laptop, strategy A examined 965,480 rows to delete 488 (about 20 ms per request), strategy B examined 464 rows (1 ms), and strategy C touched 2 rows (0.2 ms). The ratios are the same as the table's, only smaller.

### Seeing it move

Open the interactive. The left panel plots storage against `R` as a straight line, with the one-month deadline marked at R = 30. The right panel plots monthly erasure work for the three strategies on a log scale. Drag `R` from 7 to 1,095. The storage line climbs steadily and looks harmless. Strategy A's monthly work climbs just as steadily, until it crosses the "hours in a month" ceiling and turns red. Strategy C stays flat at the bottom at every `R`. Tick "batch weekly" and watch A drop by a factor of 75 (300 requests become 4 scans).

The one idea to take from it: **retention and schema are one decision.** The window sets how much you store and how much you must search. The schema sets whether searching is needed at all.

### Cross-game recognition

The same model, `S = volume per day × R`, with `R` chosen per category and per event, runs through every published game privacy policy. The rewriting skill is to find `R` and what it depends on.

**Riot Games voice chat (privacy notice, April 2026).** Let `h` be the stored voice per day. Rows get one of three windows: 1 day by default, 7 days if reported without action, up to 730 days if action is taken. Expected storage is `h × (1 + p₁ × 6 + p₂ × 729)`, where `p₁` and `p₂` are the shares of recordings in the two reported tiers. With invented shares of 5% and 1%, that is `h × (1 + 0.3 + 7.29) = 8.59 h`. The 1% of actioned recordings holds 85% of all stored voice. A tiered window is dominated by its longest tier, so the rule that decides which rows reach that tier matters most. The same notice says that when an account is deleted, Riot keeps some account-related data, such as match history, for purposes like security and fraud detection. That is a second store with its own purpose and its own `R`.

**Blizzard Entertainment (privacy policy, last updated June 2025).** Photo ID sent to customer support for identity checks is normally deleted once the check is complete, or after 30 days if the case is not handled by then. Speech-to-text transcripts of voice chat are kept only until any toxicity action is taken, then deleted. Both are the same model with `R` tied to an event ("the check is done") plus a hard cap. For the engineer this means the deletion job has two triggers, a status change and a timer. The timer is the one that saves you when the status change never arrives.

**PostgreSQL partitioning (documentation, version 18).** The database documentation says that dropping a whole partition with `DROP TABLE`, or detaching it, is far faster than a bulk `DELETE`, and avoids the `VACUUM` work a bulk delete creates. That is why every design above partitions by day. The retention job becomes one `DROP TABLE` a day, a metadata change that finishes in milliseconds, instead of deleting 60 million rows one by one.

Three sources, one shape: a volume per day multiplied by a window, where the window is set by purpose. When you read any game's privacy policy, look for the `R` for each category and ask what event, if any, shortens or extends it.

### Eyes-open design judgment

- **Choose `R` per category, from the purpose.** Raw combat events for balance analysis are usually most useful in the first weeks after a patch. Payment records may have legal retention periods measured in years. One global window is always wrong for some category.
- **Short raw windows plus aggregates cover most analytics.** After 30 days, roll raw events into daily counts per event type, region and level band, with no player key. Most dashboards (week 12) only ever read aggregates. The aggregates cost megabytes, not terabytes. Watch small groups, though. A row that says "one level-60 player in region PE crafted item 912 today" may still point at a person.
- **Strategy B is fine at small scale.** For a store of a few million rows, an index on `player_id` and a nightly erasure job is simple and correct. It stops being fine when the index maintenance on every insert becomes the bottleneck of your ingest pipeline (week 11).
- **Strategy C moves the problem into the event schema.** It only works if nothing in the event body identifies the player. The next section is about that condition.
- **Decide deliberately.** Picking `R = forever` because "storage is cheap" makes storage the smallest of your costs. Every search, export, erasure, backup and breach grows with it.

### Check yourself on the worked example

1. A game has 10,000 daily players, 3,000 events each per day, 150 bytes per event, and keeps 180 days. How large is the store, and how long does one full scan take at 1 GB/s?
2. In the section 2 game, the studio switches from 300 per-request scans to one batched scan every week at R = 90. How many scan hours a month does that save?
3. Riot-style voice retention with shares `p₁ = 10%` and `p₂ = 0.5%`. What is the average stored lifetime of a recording in days?

<details>
<summary>Answers</summary>

1. `10,000 × 3,000 × 150 × 180 = 810 GB`. One scan takes 810 s, 13.5 minutes.
2. Per-request scans cost 90 h (one hour per retention day). Weekly batches cost `4 × 18 min = 72 min`. The saving is about 88.8 hours a month.
3. `1 + 0.10 × 6 + 0.005 × 729 = 1 + 0.6 + 3.645 = 5.245` days.

</details>

## 3. Why `DELETE` does not delete

Suppose you run strategy B and the query `DELETE FROM events WHERE player_id = 81234` returns "30,000 rows affected". The player's data is still on your disks, in at least four places.

**Inside the database file.** In PostgreSQL, an `UPDATE` or `DELETE` does not immediately remove the old row version. This is how multiversion concurrency control (MVCC, week 5) lets other transactions keep reading the old version. The dead row stays in the table file until `VACUUM` marks its space reusable, and even then the bytes stay until something overwrites them. SQLite behaves similarly. Deleted rows go to free pages that keep their old content. The SQLite documentation says that running `VACUUM` removes these traces, so that deleted content cannot be recovered by forensic analysis, and that `PRAGMA secure_delete` is the alternative that overwrites content at delete time.

You can see it yourself. Part F of the lab builds a small store, erases one player, and counts how many times their email and display name appear in the raw file bytes:

```
before erasure : email x4, name x82
after DELETE   : email x4, name x82
after VACUUM   : email x0, name x0
```

The `DELETE` changed nothing in the file bytes. Only the rewrite removed them. In PostgreSQL the equivalent is `VACUUM FULL`, which rewrites the whole table and takes an exclusive lock, or dropping the partition.

**In replicas and caches.** A read replica applies the same delete, with its own dead rows. A Redis cache (week 8) may hold the player's profile until its key expires. Give every cached copy of personal data a time-to-live shorter than your erasure deadline, or delete the keys explicitly.

**In backups.** Last night's backup still holds the player. The UK regulator (ICO) guidance on the right to erasure accepts that data may stay in backups until they are overwritten on a set schedule, provided the backup data is put "beyond use". That means you do not restore it into live systems or read it for any other purpose. It also means you need a rule for what happens after a restore. Next week you will restore a backup, and if you do, you must re-apply every erasure that happened after that backup was taken. Keep the list of erased player IDs (a list of IDs that were erased, with nothing else) for as long as your oldest backup, exactly for this.

**Downstream.** Exports to a data warehouse, CSV files on an analyst's laptop, crash reports at a third-party service, the ad network. A written data map (every store, what personal data it holds, its `R`, and who deletes from it) is the only reliable way to find these. Studios that skip it discover the copies during their first audit.

## 4. Pseudonyms that stay pseudonyms

Strategy C rests on one claim. Once the mapping row is gone, nobody can tie the events to the player. Three common mistakes break that claim.

**Mistake 1, hashing the player ID.** A tempting shortcut is `telemetry_id = sha256(player_id)`. No mapping table is needed. But player IDs are small integers. There are perhaps 10 million of them. Computing SHA-256 of every integer up to 10 million took about 3 seconds in plain Python on a 2025 laptop, and then you have a lookup table that reverses every pseudonym. Hashing is fast by design (CS102 week 5), which is exactly the wrong property here. The fix is a random `telemetry_id` stored in a mapping table, or a keyed hash (an HMAC) whose secret key lives in a separate system. With the keyed hash, deleting the key unlinks every event at once. Deleting one player's link needs the mapping table.

**Mistake 2, identifiers in the event body.** The pseudonym is useless if the event also stores `display_name`, the raw IP address, an email in a support-ticket event, or free chat text. Design events so that identifiers are replaced at the edge of the pipeline, before the event is written. Coarsen what you need for analytics. Store the country rather than the IP, the level band rather than the exact level if rare combinations would single someone out.

**Mistake 3, the rare player.** Even without names, a trail of events can be unique. "The only player on server EU-3 who reached level 60 on launch day and owns a guild" is one person to anyone who reads the forums. Recital 26 asks whether identification is reasonably likely given the means available. Unique trails of events are the usual reason pseudonymised data does not become anonymous. Short raw retention (section 2) limits how long such a trail exists. Aggregates with minimum group sizes limit what survives after that.

Here is the schema for strategy C in PostgreSQL. It is the same design the lab builds in SQLite.

```sql
CREATE TABLE accounts (
  player_id    bigint PRIMARY KEY,
  email        text NOT NULL UNIQUE,
  display_name text NOT NULL,
  country      char(2) NOT NULL
);

-- The only link from telemetry back to a person.
CREATE TABLE pseudonyms (
  player_id    bigint PRIMARY KEY REFERENCES accounts ON DELETE CASCADE,
  telemetry_id uuid NOT NULL UNIQUE DEFAULT gen_random_uuid()
);

-- One partition per day. No player_id, no names, no IPs.
CREATE TABLE events (
  ts           timestamptz NOT NULL,
  telemetry_id uuid NOT NULL,
  type         text NOT NULL,
  country      char(2),
  level_band   smallint,
  value        integer
) PARTITION BY RANGE (ts);

CREATE TABLE events_2026_09_28 PARTITION OF events
  FOR VALUES FROM ('2026-09-28') TO ('2026-09-29');

-- Erasure: the cascade removes the pseudonym row too.
DELETE FROM accounts WHERE player_id = 81234;

-- Retention job, once a day: drop the partition that just left the window.
DROP TABLE events_2026_08_29;
```

In SQLite there is no `PARTITION BY`. The lab creates one table per day (`events_d000`, `events_d001`, ...) and drops tables by name, which is the same idea done by hand. SQLite also has no `uuid` type or `gen_random_uuid()`. The lab generates a random hex string in Python with `secrets.token_hex`.

Serving an access request (Article 15) runs the same path in reverse: look up the `telemetry_id` from `player_id`, then collect that player's events from the partitions still in the window. After erasure that lookup fails, which is the whole point. Lab Part E asks you to write this export for both stores.

## 5. A retention schedule

Put sections 2 to 4 together and a game's privacy design becomes a table that engineers and lawyers fill in together. Here is a starting schedule for a small MMO. The windows are examples for teaching, not recommendations for any real game.

| Data category | Purpose | Window R | Deletion mechanism | Erasure strategy |
|---|---|---|---|---|
| Account (email, country, birth year) | Run the account | Life of account + 30 days | Delete row on closure | Delete row |
| Raw gameplay events | Balance, bug hunting | 30 days | Drop daily partition | C (pseudonym) |
| Daily aggregates | Dashboards, KPIs | 3 years | Drop yearly partition | None needed if groups ≥ 20 players |
| Connection logs with IP | Security, fraud | 90 days | Drop partition | B (index on account) |
| Chat logs | Moderation reports | 7 days; 1 year if actioned | Timer plus status flag | B |
| Payment records | Tax and refunds | As tax law requires | Yearly job | Keep, exempt from erasure while legally required |
| Backups | Disaster recovery (week 14) | 35 days | Rotation | Beyond use; re-apply erasures after a restore |

Every row answers four questions. Why do we have this? For how long? What removes it? What happens when one player asks? If you cannot fill in a cell, you have found a design problem.

## In-class activity (25 minutes)

Work in groups of three. You are the data team for a new MMO launching in the EU with 25,000 expected daily players.

1. Write down every place player data will live in your PR201 or PR301 project (or an imagined one): tables, logs, caches, analytics tools, backups, third-party services. Aim for at least eight entries.
2. For the telemetry store, pick `e`, `b` and `R`. Compute storage and the monthly scan hours for strategy A at 200 erasure requests a month and 1 GB/s.
3. Fill in the retention schedule table for four of your categories.
4. Pick one event from your telemetry spec (week 10) and rewrite it so it contains no direct identifier and no field that would single out a rare player.

Expected output: the data map list, one computed line with storage and scan hours, four schedule rows, and a before/after event definition.

## Common misconceptions

- **"Telemetry is anonymous because it only has IDs."** An ID that you can join to an account table is personal data. Even a random pseudonym is personal data while the mapping exists (Recital 26).
- **"Hashing the player ID anonymises it."** Hashing a small ID space is reversible by trying every ID. Use a random mapping or a keyed hash with the key held elsewhere.
- **"`DELETE` erased it."** The bytes remain in the database file until a rewrite, and in replicas, caches, backups and exports. Erasure is a process across every store in your data map.
- **"Keeping everything is the safe default."** Storage cost is linear in `R`, but so are scan time, export size and the damage of a breach. The safe default is the shortest window that serves the purpose.

## Check yourself

1. Your store keeps 60 days of events at 8 GB a day and scans at 0.5 GB/s. You receive 150 erasure requests a month. How many scan hours a month does strategy A cost per request? With weekly batching?
2. A designer proposes `telemetry_id = md5(player_id)` to "remove personal data from analytics". Your game has 3 million accounts. Explain in two sentences why this fails, and propose a fix.
3. A player's erasure request is completed on 3 October. On 10 October you restore the database from a backup taken on 1 October. Is the player's data back? What should your restore procedure do?
4. With Riot-style tiers (1, 7 and 730 days) and 2% of recordings in the actioned tier, what share of stored voice sits in that tier? Ignore the 7-day tier.

<details>
<summary>Answers</summary>

1. One scan reads `8 × 60 = 480 GB` at 0.5 GB/s, 960 s or 16 minutes. 150 per month cost 2,400 minutes, 40 hours. Four weekly batches cost 64 minutes.
2. Anyone with access can compute the MD5 of all 3 million IDs in seconds and reverse every pseudonym, so the data is still linked to accounts. Use a random `telemetry_id` in a separate mapping table (delete the row on erasure), or a keyed HMAC with the key stored in a different system.
3. Yes. The 1 October backup predates the erasure. Your restore procedure must re-apply every erasure made after the backup's timestamp, using the retained list of erased player IDs, before the restored database goes live.
4. Stored amount is proportional to share × days. Actioned: `0.02 × 730 = 14.6`. Default: `0.98 × 1 = 0.98`. Share in actioned tier `= 14.6 / 15.58 ≈ 94%`.

</details>

## Lab / assignment hook

[Lab 13, retention and erasure](../labs/lab13.md). You build a naive and a pseudonymous telemetry store, measure rows examined per erasure for three strategies, write the retention job and a subject access export, and watch deleted bytes survive a `DELETE`. Deliverable: code plus a one-page retention schedule for your final project's inventory service. The final service (week 15) must implement the erasure path you choose here.

## Sources

- Regulation (EU) 2016/679 (GDPR), text via gdpr-info.eu, accessed September 2026. Article 4(5) definition of pseudonymisation; Article 5(1)(c) data minimisation and 5(1)(e) storage limitation; Article 12(3) one month to act, extendable by two further months; Article 17 erasure "without undue delay"; Article 33 breach notification within 72 hours where feasible; Article 83(5) fines up to 20 million euros or 4% of worldwide annual turnover; Recital 26 on pseudonymised and anonymous data.
- UK Information Commissioner's Office, "Right to erasure" guidance, accessed September 2026. Erasure from backups, and putting backup data beyond use until it is overwritten on schedule.
- Riot Games, Privacy Notice, last modified 28 April 2026, section III. Voice chat retained 24 hours; 7 days if reported without action; up to 2 years if action is taken; some account data such as match history kept after account deletion for security and fraud detection.
- Blizzard Entertainment, Online Privacy Policy, last updated 27 June 2025. Identification photos normally deleted after verification or after 30 days; speech-to-text transcripts deleted after any toxicity action.
- PostgreSQL 18 documentation, "Routine Vacuuming" (24.1.2) and "Table Partitioning" (5.12). `DELETE` does not immediately remove old row versions; `VACUUM` reclaims space; dropping or detaching a partition is far faster than bulk `DELETE` and avoids its `VACUUM` overhead.
- SQLite documentation, "VACUUM" (sqlite.org/lang_vacuum.html). Deleted content can remain recoverable by forensic analysis; `VACUUM` removes the traces; `PRAGMA secure_delete` as the alternative.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly, chapter 2.
- All game-scale figures in the worked example (`D`, `e`, `b`, request rate, scan throughput, report shares) are invented for teaching. The lab timings were measured with the lab13 starter on a 2025 laptop with SQLite 3.53.

## Interactive spec: examples/w13-retention-and-erasure.html

**The one insight.** Storage grows as a harmless-looking straight line in the retention window `R`, but the monthly work of honoring erasure requests by scanning grows with it and hits the ceiling of hours in a month. A pseudonym table makes erasure cost flat at every `R`. Retention and schema are one decision.

**Layout.** Controls on top. Two linked panels side by side at 1280px, stacked at 390px (storage first). A results table under both. First screen, before any interaction, shows `R = 395` so strategy A's bar is already near the ceiling.

**Controls (all keyboard operable, with numeric readouts).**
- Retention `R` in days: log slider 7 to 1,095, default 395. Snap buttons: 7, 30, 90, 395, 1,095.
- Daily players `D`: 1,000 to 500,000 (log), default 40,000.
- Events per player per day `e`: 100 to 5,000, default 1,500.
- Bytes per event `b`: 50 to 1,000, default 200.
- Erasure requests per month `q`: 10 to 5,000 (log), default 300.
- Scan throughput `T` in GB/s: 0.1 to 10 (log), default 1.
- Active days of the erasing player `a`: 1 to 365, default 20 (clamped to `R`).
- Checkbox "Batch weekly" (default off).

**Formulas.**
- `rows_per_day = D × e`; `bytes_per_day = D × e × b`.
- `rows = D × e × R`; `storage_bytes = D × e × b × R`; `index_bytes = 24 × rows` (strategy B only).
- `scan_seconds = storage_bytes / (T × 1e9)`.
- Monthly work, A: `scans = batch ? 4 : q`; `hours_A = scans × scan_seconds / 3600`; rows examined per month `= scans × rows`.
- Monthly rows examined, B: `q × e × min(a, R)`. C: `q × 2`.
- Ceiling: 720 hours per month.
- Deadline marker: R = 30 days.

**Left panel, storage.** x axis `R` (log, 7 to 1,095 days), y axis storage in TB (linear). A line for events only and a dashed line for events plus index (strategy B). A vertical marker at the current `R` with the storage printed. A vertical dotted line at R = 30 labeled "one-month response deadline".

**Right panel, monthly erasure work.** x axis `R` (same scale), y axis rows examined per month, log scale from 1 to 1e14. Three lines, A (solid), B (dashed), C (dotted), labeled at the right end. A horizontal band marking the rows that correspond to 720 hours of scanning at the current `T` (compute `720 × 3600 × T × 1e9 / b` rows) labeled "a month of full-time scanning". The part of line A above that band is drawn in the warning color. A marker at the current `R` on each line.

**Results table.** Rows: A scan, A batched, B index, C pseudonym. Columns: rows examined per request, rows examined per month, scan hours per month (A only), extra storage (B only). Values update live.

**Test values (defaults, batch off).** `rows_per_day = 60,000,000`; at R = 395: rows `= 23,700,000,000`, storage `= 4.74 TB`, one scan `= 4,740 s = 79 min`, A monthly `= 395 h` (not over the ceiling), B per request `= 30,000`, C per request `= 2`. At R = 1,095: storage 13.14 TB, A monthly 1,095 h (over the ceiling, red). Batch on at R = 395: A monthly `= 4 × 79 min ≈ 5.27 h`. At R = 30: storage 0.36 TB, A monthly 30 h.

**Accessibility and style.** Lines distinguished by dash pattern as well as color. Shared tokens from `templates/interactive-tokens.css`. Respect `prefers-reduced-motion`. No game art or logos.
