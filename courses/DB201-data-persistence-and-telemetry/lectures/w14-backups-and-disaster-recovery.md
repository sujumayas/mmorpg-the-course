# DB201 · Week 14 — Backups and Disaster Recovery

**Why this matters:** Week 1 asked how much progress a server crash can erase. This week asks the bigger question. What if the database itself is gone, or a bad script has corrupted it? The answer is two numbers you choose in advance, how much data you may lose and how long you may be down. Studios that never chose them learn them from an outage.

**You will be able to:**
- Compute the recovery point objective (RPO) and recovery time objective (RTO) of a backup policy from database size, restore throughput, log volume and backup intervals.
- Explain why the log archive interval sets data loss while the base backup interval sets downtime, and tune each one separately.
- Perform a point-in-time restore to undo an operator mistake, and state what that restore throws away.
- Design a restore drill that proves a backup works, and name the failure modes that make untested backups worthless.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 7, reread the "Durability" part of "The Meaning of ACID". PostgreSQL 18 documentation, section 25.3 "Continuous Archiving and Point-in-Time Recovery", subsections 25.3.1, 25.3.2 and 25.3.5 (about 30 minutes). GitLab, "Postmortem of database outage of January 31" (2017), about 20 minutes.

**Prerequisites from earlier courses:** [DB201 week 1, why persistence is hard](w01-why-persistence-is-hard-in-games.md) (the `T / 2` expected-loss model and write-ahead logs). [DB201 week 13, privacy and retention](w13-privacy-gdpr-and-data-retention.md) (backups hold erased data; re-apply erasures after a restore). [DB201 week 5, transactions and ACID](w05-transactions-and-acid.md). [DB201 week 6, the duplication bug](w06-race-conditions-and-the-duplication-bug.md). [DB201 week 7, Redis](w07-nosql-and-key-value-stores-redis.md) and [week 8, caching and write-behind](w08-caching-and-write-behind.md) (Redis persistence and what a cache loses). [CS102 week 12, command pattern](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) (replaying a log of commands rebuilds state, which is what log replay does). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (the average of a uniform quantity).

**Interactive:** [w14-rpo-rto-timeline.html](../examples/w14-rpo-rto-timeline.html). Keep it open during section 2.

---

## 1. Three disasters, three different backups

A crash of the game server process is not a disaster. The database survives it, and week 1 showed how to bound what the players lose. A disaster is when the database cannot come back by itself. Three kinds cover almost every real incident.

- **Loss of the machine or disk.** Hardware dies, a cloud volume is deleted, a data centre floods. The data is simply gone.
- **An operator mistake.** Someone runs a script against production instead of staging, or an `UPDATE` without a `WHERE`. The database is healthy and wrong.
- **Corruption or bad software.** A bug in a new game patch writes nonsense to thousands of inventories over three hours before anyone notices.

The first kind is the one people picture, and it is the one a replica handles. A replica is a second database server that applies every change the primary makes, a fraction of a second later. If the primary's disk dies, you promote the replica. But a replica copies the second and third kinds of disaster just as faithfully. An `UPDATE characters SET gold = 0` reaches the replica within a second. For those you need a copy of the past, and a way to go back to a chosen moment. That is what a backup is.

Three kinds of backup exist in PostgreSQL, and SQLite has simpler versions of each.

**Logical dump.** `pg_dump` writes the database out as SQL statements or an archive of table data. The documentation notes that its output can be loaded into newer PostgreSQL versions and onto different machine architectures, and that a dump is internally consistent, a snapshot as of the moment `pg_dump` started, taken without blocking normal reads and writes. Restoring means re-inserting every row and rebuilding every index, which is slow for large databases. SQLite's equivalent is `.dump` or `VACUUM INTO`.

**Physical base backup.** `pg_basebackup` copies the database's data files as they are on disk. It is fast to restore, since you copy files back, but it only works with the same major version of PostgreSQL. PostgreSQL 17 added incremental base backups, which copy only the blocks changed since an earlier backup. In SQLite, the online backup API (`Connection.backup` in Python's `sqlite3` module) copies a live database page by page into a consistent file.

**Continuous log archiving.** PostgreSQL writes every change to its write-ahead log (WAL, week 1) before touching the data files. The WAL is stored as a series of segment files, normally 16 MB each. If you configure an `archive_command`, the server copies each finished segment to safe storage. A base backup plus every WAL segment since it lets you replay history forward to any moment you choose. That is called point-in-time recovery (PITR). SQLite has no built-in equivalent. The lab builds one with a logical log, the same way CS102's command pattern rebuilds a game state by replaying commands.

## 2. Worked example: how much do the players lose, and for how long?

### The hook

In February 2013 Jagex asked RuneScape players whether it should open a separate version of the game as it had been in 2007. The poll passed, and on 22 February 2013 Old School RuneScape launched. It was built from a backup of the game dated August 2007 that Jagex found in its archives. The game has been maintained separately ever since.

Think about what that backup had to be. Five and a half years old, still readable, and complete enough to rebuild a working game. Most studios cannot restore last night's backup on the first try. This lecture is about the two numbers that say whether you can.

### The model

Two numbers define any backup policy. Both come from the moment of failure, `t_f`.

**Recovery point objective (RPO)**, how much committed data you lose. It is the gap between `t_f` and the newest moment you can restore to.

**Recovery time objective (RTO)**, how long the game is down. It is the time from `t_f` until players can log in to a correct database.

Now name the quantities for one game database.

- `S`, database size. We use 400 GB.
- `B`, restore throughput for copying a base backup back. We use 250 MB/s.
- `w`, WAL generated per hour at peak. We use 10 GB/h.
- `r`, WAL replay rate during recovery. We use 100 GB/h.
- `I_base`, time between base backups.
- `I_arch`, the longest a WAL segment can wait before it is archived. In PostgreSQL that is the `archive_timeout` setting. We use 60 s.
- `t_detect` and `t_verify`, time to notice the failure and time to check the restored data. We use 15 minutes each.

**RPO with snapshots only.** If you take a full backup every `I_base` and nothing else, the newest restorable point is the last backup. A failure lands at a random moment inside the interval, so, exactly as in week 1:

```
RPO_worst = I_base          RPO_avg = I_base / 2
```

**RPO with log archiving.** Every committed change is in the WAL. The only changes you lose are those in the segment that was not yet archived:

```
RPO_worst ≈ I_arch          RPO_avg ≈ I_arch / 2
```

The base backup interval has disappeared from the RPO. That is the first half of the lesson.

**RTO.** Restoring means copying the newest base backup back, then replaying every WAL segment written since that backup:

```
RTO = t_detect + S / B + (w × Δ) / r + t_verify
```

where `Δ` is the time between the last base backup and the failure. In the worst case `Δ = I_base`, so the replay term is `w × I_base / r`. On average it is half that.

The archive interval has disappeared from the RTO. The base backup interval has come back. That is the second half. **The archive interval sets how much you lose. The base backup interval sets how long you are down.** They are two separate knobs, and teams that treat backups as one setting end up turning the wrong one.

### Numbers you can check

The copy term is the same in every row: `400 GB / 250 MB/s = 1,600 s ≈ 0.44 h`. Detection plus verification adds 0.5 h. Replay worst case is `10 GB/h × I_base / 100 GB/h = 0.1 × I_base`.

| Policy | RPO worst | RPO avg | Replay worst | RTO worst |
|---|---|---|---|---|
| Nightly full backup only | 24 h | 12 h | 0 | 0.94 h |
| Hourly snapshot only | 1 h | 30 min | 0 | 0.94 h |
| Weekly base + WAL archive (60 s) | 60 s | 30 s | 16.8 h | 17.7 h |
| Daily base + WAL archive (60 s) | 60 s | 30 s | 2.4 h | 3.3 h |
| 6-hourly base + WAL archive (60 s) | 60 s | 30 s | 0.6 h | 1.5 h |

Translate RPO into what players feel. Say 8,000 players are online on average. A failure under the nightly-only policy erases on average `8,000 × 12 h = 96,000` player-hours of progress, every quest, drop and trade since the last backup. Under any WAL policy it erases `8,000 × 30 s ≈ 67` player-hours. That is the difference between "we are rolling back to last night" and "some of you lost your last fight".

Now look at RTO. The weekly-base policy has the best RPO in the table and the worst downtime. The replay rate is the reason. Recovery replays a week of WAL, 1,680 GB of it, at 100 GB/h. Adding base backups every six hours costs more backup storage and I/O, and cuts the worst-case downtime from 17.7 hours to 1.5.

Both knobs cost something. The PostgreSQL documentation points out that a segment archived early because of `archive_timeout` is still a full-size file. At 60 s a quiet server still produces up to `1,440 segments × 16 MB ≈ 23 GB` of archive a day. At 5 s that becomes about 276 GB a day, which is why the documentation calls very short timeouts unwise and suggests about a minute. More frequent base backups cost a full copy of `S` each time, unless you use incremental backups.

The lab runs the same model at toy scale. With a base backup every 600 game seconds and the log archived every 60, a disaster at t = 1,537 lost 37 seconds of transactions (the segment in progress) and replayed about 6,000 transactions onto the base from t = 1,200. Switch to a base every 1,800 s and an archive every 5 s, and the loss drops to 2 seconds, but replay grows to about 30,700 transactions and takes four to five times as long. The two knobs trade exactly as the table says.

### Seeing it move

Open the interactive. The top panel is a timeline of one day. Base backups appear as tall ticks, archived WAL segments as short ticks. Drag the red failure marker anywhere. A shaded block shows the data lost (from the last archived tick to the failure). A failure that lands exactly on an archive tick loses the whole interval, because that segment had not shipped yet, so the default marker, which sits on a tick, shows 60 s lost. A second block shows the recovery (copy plus replay since the last base tick). Move the failure just before a base backup and the recovery block is at its longest. Move it just after and it shrinks to the copy time.

The bottom panel plots worst-case RPO and RTO against the two intervals. Drag `I_arch` and only the RPO curve moves. Drag `I_base` and only the RTO curve moves. The picture makes the separation obvious in a way the formulas do not.

### Cross-game recognition

**GitLab.com, 31 January 2017.** Not a game, but the most detailed public account of a PostgreSQL recovery, and the one every operations team reads. While trying to repair broken replication, an engineer removed the data directory on the primary instead of the secondary. About 300 GB was gone before they stopped the command. The team then found that none of its backup methods worked. The nightly `pg_dump` job had been failing silently, because it used `pg_dump` from PostgreSQL 9.2 against a 9.6 server, and the failure emails were rejected by the receiving mail server. The storage bucket was empty. Replication had been set up for failover, not recovery. Disk snapshots were not enabled for the database servers. What saved them was a snapshot an engineer had taken by hand about six hours earlier to refresh staging.

Put it into the model. The realized RPO was the gap from that manual snapshot at about 17:20 UTC to midnight, about 6 hours 40 minutes, which cost roughly 5,000 projects, 5,000 comments and 700 new user accounts. The realized RTO was about 18 hours, and the copy term dominated. The staging disks were throttled to about 60 Mbps, so `S / B` was huge. The postmortem also notes that the site was not using WAL archiving. With it, the RPO would have been about a minute. A policy that exists on paper has an RPO of infinity until someone restores it.

**Redis persistence (Redis Open Source documentation).** Your game's Redis (weeks 7 and 8) has the same two mechanisms under different names. An RDB file is a point-in-time snapshot, typically every five minutes or more, so the documentation warns you may lose the latest minutes of data. That is snapshot-only, `RPO_worst = I_base`. The append-only file (AOF) logs every write. With `appendfsync everysec`, the default policy, you may lose one second of writes. That is `RPO_worst = I_arch` with `I_arch = 1 s`. On restart Redis loads the snapshot and replays the AOF, which is the RTO formula with `S` and `w` in memory rather than on disk. The documentation recommends using both if you want data safety comparable to PostgreSQL.

**Old School RuneScape again.** The 2007 backup is an extreme case of backup retention, the `R` from last week applied to backups. Most studios keep backups for weeks, because every retained backup costs storage, holds personal data players may have asked to erase, and must stay restorable on current software. Jagex's archive shows the upside of keeping one old backup readable. GitLab's shows the downside of never testing the recent ones.

Three contexts, one model. Every backup system is a snapshot plus, optionally, a log. The snapshot interval decides how much log you must replay. The log's flush interval decides how much you lose.

### Eyes-open design judgment

- **Choose RPO per kind of data.** Losing 60 seconds of combat is acceptable. Losing 60 seconds of real-money purchases is not, because the payment provider still has the charge. For purchase records, commit synchronously and replicate synchronously to a second site, and reconcile with the provider after any restore.
- **Choose RTO from what downtime costs.** A four-hour outage on launch weekend costs more than the extra base backups that prevent it. Work out the cost of an hour down, then buy the backup frequency that keeps the worst case below what you can afford.
- **Restore every store to the same moment.** If character inventories live in PostgreSQL with 60 s RPO and the trade escrow lives in Redis with a five-minute RDB, restoring both "to their latest" puts them at different moments. An item that moved between them in those minutes is now in both places, or neither. That is the week 6 duplication bug, created by your backup policy. Either restore everything to one common timestamp, or keep all authoritative economy state in one transactional database.
- **Replicas are for availability, backups are for history.** You need both. A replica gives you minutes of RTO for hardware loss. Only a backup plus log undoes an operator mistake.
- **Decide deliberately.** "Nightly backups" is a habit, not a design. The table above shows it can be both the fastest restore and the worst data loss in the list.

### Check yourself on the worked example

1. A 1.2 TB database restores at 400 MB/s, writes 20 GB of WAL an hour and replays 150 GB/h. Base backups run every 12 hours. What is the worst-case RTO, ignoring detection and verification?
2. Same database. The team wants worst-case RTO under 1.5 hours. What is the longest base backup interval that achieves it?
3. A server sets `archive_timeout = 10 s` and is idle overnight for 8 hours. How much archive storage does the idle night produce, with 16 MB segments?

<details>
<summary>Answers</summary>

1. Copy: `1,200,000 MB / 400 MB/s = 3,000 s ≈ 0.83 h`. Replay: `20 × 12 / 150 = 1.6 h`. RTO worst ≈ 2.43 h.
2. Replay budget is `1.5 − 0.83 = 0.67 h`. `20 × I_base / 150 ≤ 0.67` gives `I_base ≤ 5 h`.
3. `8 h × 360 segments/h = 2,880` segments, `2,880 × 16 MB ≈ 46 GB`, for a server that did nothing.

</details>

## 3. Undoing an operator mistake

Hardware loss is a restore to "as late as possible". An operator mistake is a restore to "just before the mistake". Here is the lab's scenario. At game time t = 700 a GM script meant to reset one test character runs as `UPDATE characters SET gold = 0`. It is noticed at t = 900.

In PostgreSQL you restore the newest base backup from before t = 700 into a new data directory, set a `restore_command` that fetches archived WAL segments, set `recovery_target_time` to a moment just before the script, and start the server. It replays the log and stops at the target. The lab does the same with its logical log, and the restored gold total matches the history exactly:

```
gold now: 4,257 (before the script: 515,468)
PITR to t=699: gold 515,468, matches history: True
```

Now the hard part. The restored copy is correct as of t = 699, but everything players did from t = 700 to t = 900 is missing, including loot and trades that had nothing to do with gold. You have three options, and none is free.

1. **Roll everyone back to t = 699.** Simplest and fully consistent. Players lose 200 seconds, or in a real incident several hours. Announce it and compensate.
2. **Repair selectively.** Keep the live database. Restore the old copy next to it, read the correct `gold` values from it, and write only those back into the live table. You keep all the legitimate work, but you must reason about every transaction that read or changed gold after t = 700. A trade at t = 750 where a player paid 40 gold they "did not have" is now a question.
3. **Replay around the mistake.** Restore to t = 699, then replay the log from t = 700 while skipping the bad transaction. This works only when later transactions did not depend on the bad one's result. The lab's log is logical, so it can skip one record. PostgreSQL's WAL is physical (page changes), so it cannot. Studios that want this option keep their own logical event log of economy transactions, which the week 11 pipeline may already give you.

Whichever you pick, run the week 13 step before the restored database goes live. Re-apply every erasure request completed after the backup's timestamp.

## 4. A backup is a restore you have tested

GitLab's backups did not fail during the incident. They had failed for weeks, and nobody knew. Four rules come straight from that postmortem and from the model.

**Verify every backup automatically.** After each base backup, open it somewhere else and check it. For SQLite that means `PRAGMA integrity_check`, the expected tables, and plausible row counts. For PostgreSQL, restore it into a scratch server and run a handful of queries. Lab Part C asks you to write this check so that an empty or truncated file fails loudly.

**Alert on absence, not only on error.** GitLab's error emails were being rejected. A monitor that says "no new backup has appeared in 26 hours" catches that, and a failed job, and a deleted cron entry.

**Drill the whole restore on a schedule.** Once a quarter, restore production into a fresh environment from scratch, time it, and compare the time with your RTO. The drill finds the missing password, the undocumented step, and the 60 Mbps disk. GDPR's Article 32 lists the ability to restore personal data in a timely manner after an incident, and a process for regularly testing it, among the security measures a studio should consider. The drill is also your evidence.

**Keep copies apart.** A backup on the same disk, account or region as the database dies with it. A common rule of thumb is three copies, on two kinds of storage, with one off-site. For cloud databases, keep at least one copy in an account that the production credentials cannot delete.

Here is a minimal nightly job for a SQLite game database, the kind you would run for a small server or a PR201 prototype. It makes a consistent copy of the live file, then proves the copy opens.

```python
import sqlite3, datetime, pathlib

def nightly_backup(live_path, backup_dir):
    stamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    dest = pathlib.Path(backup_dir) / f"game_{stamp}.db"
    src = sqlite3.connect(live_path)
    dst = sqlite3.connect(dest)
    src.backup(dst)                 # consistent even while the game keeps writing
    dst.close(); src.close()
    check = sqlite3.connect(f"file:{dest}?mode=ro", uri=True)
    assert check.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert check.execute("SELECT COUNT(*) FROM characters").fetchone()[0] > 0
    check.close()
    return dest
```

In PostgreSQL the same job is `pg_basebackup` to a dated folder, plus continuous WAL archiving configured once, plus a restore into a scratch instance for the check. Use `pg_dump` as a second, version-independent copy, and make sure the `pg_dump` binary matches the server's major version, which is exactly what failed at GitLab.

## 5. Backup retention

Backups need a retention window too, and last week's model applies. With a daily 400 GB base and 10 GB of WAL an hour at peak (say 150 GB a day on average), keeping 35 days costs about `35 × 400 + 35 × 150 = 19,250 GB`, roughly 19 TB. That is more than the database itself, many times over. Incremental base backups cut the first term. Keeping only weekly bases beyond the first week cuts it further, at the cost of longer replay for old restore points.

Your retention window for backups also caps how long erased data survives (week 13), and how far back you can reach to recover from slow corruption. If a bad patch corrupts inventories quietly for three weeks and your oldest backup is two weeks old, there is no clean copy left. Pick the window from the longest silent failure you can imagine, then check what that costs.

## In-class activity (25 minutes)

Work in groups of three on the database for the PR201 vertical slice or an imagined small MMO.

1. Estimate `S`, `w` and peak concurrent players for launch month.
2. The producer says the game may lose at most 5 minutes of progress and be down at most 2 hours. Choose `I_arch` and `I_base`, using `B = 200 MB/s` and `r = 80 GB/h`. Show the RPO and RTO arithmetic.
3. Write the restore runbook as numbered steps, including the week 13 erasure step and the check that says the restored data is correct.
4. Swap runbooks with another group. Find one step that would fail at 3 a.m. with the most senior engineer asleep.

Expected output: the two intervals with arithmetic, a runbook of 8 to 15 steps, and the weakness your partners found.

## Common misconceptions

- **"We have a replica, so we have backups."** A replica copies mistakes within a second. It covers hardware loss only.
- **"More frequent backups mean less downtime."** Frequent log archiving cuts data loss, not downtime. Downtime depends on database size and on how much log you must replay since the last base backup.
- **"The backup job runs every night, so we are safe."** A job that runs is not a backup that restores. Only a tested restore tells you the RPO and RTO you really have.
- **"Restore to the latest possible point."** After an operator mistake, the latest point contains the mistake. After a multi-store failure, "latest" differs per store and can duplicate items.

## Check yourself

1. Snapshot-only policy with backups every 4 hours and 12,000 players online on average. How many player-hours does an average failure erase? What is the figure with WAL archived every 30 s?
2. Your database is 2 TB and restores at 500 MB/s. Why can no base backup schedule bring the worst-case RTO under one hour, and what would you change instead?
3. Redis holds trade escrow with RDB every 10 minutes and no AOF. PostgreSQL holds inventories with 60 s RPO. Describe one sequence of events where restoring both to their latest point duplicates an item.
4. After an operator mistake at 14:00, you restore to 13:59 and roll everyone back. Name two things you must do before opening the servers.

<details>
<summary>Answers</summary>

1. Average loss is half the interval, 2 h, so `12,000 × 2 = 24,000` player-hours. With 30 s archiving the average is 15 s, `12,000 × 15 / 3,600 = 50` player-hours.
2. The copy alone takes `2,000,000 MB / 500 MB/s = 4,000 s ≈ 1.1 h`, before any replay. Change the copy term: faster restore storage, a smaller database (move old telemetry out, week 13), or a standby replica that is promoted instead of restored.
3. At 11:58 a seller puts an item into escrow (Redis) and PostgreSQL records it as removed from their bag. Redis snapshots at 12:00 with the item in escrow. At 12:05 the trade completes, Redis clears the escrow, and PostgreSQL puts the item in the buyer's bag. Disaster at 12:08. PostgreSQL restores to 12:07, so the buyer has the item. Redis restores its 12:00 snapshot, where the item is still in escrow and the trade is still open. When that escrow resolves, it hands the item out a second time (to the buyer again or back to the seller). One item, two copies.
4. Re-apply every erasure request completed after the backup's timestamp (week 13). Run the verification checks on the restored database. Also announce the rollback and reconcile real-money purchases made after 13:59 with the payment provider.

</details>

## Lab / assignment hook

[Lab 14, disaster-recovery drill](../labs/lab14.md). You write point-in-time restore for a simulated game database with base backups and an archived log, verify backups so that bad ones fail loudly, fill in the RPO/RTO table for four policies, and write the incident plan for an operator mistake. The final service (week 15) must ship with a backup script, a verification check and a one-page restore runbook.

## Sources

- Wikipedia, "Old School RuneScape" and "RuneScape" (accessed September 2026). February 2013 poll; release on 22 February 2013; based on an August 2007 backup found in Jagex's archives; maintained separately since.
- GitLab, "Postmortem of database outage of January 31" (published 10 February 2017). Primary data directory removed by mistake, about 300 GB; `pg_dump` 9.2 against PostgreSQL 9.6 failing silently; failure emails rejected; no WAL archiving; replication for failover only; restore from a manual LVM snapshot taken about 6 hours earlier; data lost from 17:20 to 00:00 UTC, about 5,000 projects, 5,000 comments and 700 user accounts; restore copy took about 18 hours on disks throttled to about 60 Mbps.
- PostgreSQL 18 documentation, "SQL Dump" (25.1), "Continuous Archiving and Point-in-Time Recovery" (25.3), "archive_timeout" (19.5) and "WAL Internals" (28.6). `pg_dump` output loads into newer versions and is internally consistent; physical backups and WAL are version-specific; early-archived segments are full length; a minute or so is a reasonable `archive_timeout`; WAL segments normally 16 MB.
- PostgreSQL 17 release notes (2024). `pg_basebackup` supports incremental backup.
- Redis Open Source documentation, "Redis persistence" (accessed September 2026). RDB snapshots every five minutes or more can lose minutes of data; AOF with `appendfsync everysec` can lose one second; recommendation to use both for PostgreSQL-like safety.
- Python 3 documentation, `sqlite3.Connection.backup`. Online backup that works while the database is in use. SQLite documentation, "VACUUM" (`VACUUM INTO` as an alternative backup method).
- Regulation (EU) 2016/679 (GDPR), Article 32(1)(c) and (d), via gdpr-info.eu. Ability to restore availability and access to personal data in a timely manner, and regular testing of measures.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly, chapter 7.
- All database sizes, rates, player counts and costs in the worked example are invented for teaching. Lab outputs were measured with the lab14 starter and SQLite 3.53.

## Interactive spec: examples/w14-rpo-rto-timeline.html

**The one insight.** The log archive interval sets how much data a failure loses (RPO). The base backup interval sets how long recovery takes (RTO). Moving one knob moves only its own number.

**Layout.** Controls on top. Top panel: a 24-hour timeline. Bottom panel: two small line charts side by side at 1280px, stacked at 390px. A results table under everything. First screen shows the "Daily base + WAL" preset with the failure marker placed 23 hours after the base backup, so the long recovery block is visible immediately.

**Controls (keyboard operable, numeric readouts).**
- Database size `S`: 10 GB to 10 TB (log slider), default 400 GB.
- Restore throughput `B`: 25 to 2,000 MB/s (log), default 250.
- WAL rate `w`: 0.5 to 100 GB/h (log), default 10.
- Replay rate `r`: 10 to 1,000 GB/h (log), default 100.
- Base interval `I_base`: 1 h to 168 h (log), default 24 h.
- Archive: checkbox "WAL archiving on" (default on) and `I_arch` 1 s to 3,600 s (log), default 60 s.
- Detection and verification, each 0 to 120 min, default 15.
- Failure time: a draggable marker on the timeline (arrow keys move it by 15 minutes; Shift+arrow by 1 minute).
- Players online `P`: 100 to 100,000 (log), default 8,000.
- Presets: "Nightly full only", "Hourly snapshot only", "Weekly base + WAL", "Daily base + WAL", "6-hourly base + WAL".

**Formulas.**
- `t_copy_h = S_GB × 1000 / B / 3600`.
- Snapshot only (archiving off): `RPO_worst = I_base`, `RPO_avg = I_base / 2`, replay `= 0`.
- With archiving: `RPO_worst = I_arch`, `RPO_avg = I_arch / 2`, `replay_worst_h = w × I_base / r`, `replay_avg_h = replay_worst_h / 2`.
- At the marker: `Δ = t_f − last_base_before(t_f)`; `loss = archiving ? (t_f − last_archive_tick_before(t_f)) : Δ`, where "before" is strict: a failure exactly on a tick has not archived that tick, so it loses a full `I_arch` (60 s at the default marker); `replay_h = archiving ? w × Δ / r : 0`; `RTO_here = t_detect + t_copy_h + replay_h + t_verify`.
- `player_hours_lost = P × loss_hours`.
- Archive storage per idle day `= (86,400 / I_arch) × 16 MB`, shown as a note next to the `I_arch` slider.

**Top panel, timeline.** 24 hours (or 7 days when `I_base` exceeds 24 h, with a toggle). Tall ticks at each base backup, short ticks at each archive point (thin out visually when denser than 2 px, but compute exactly). The failure marker in the warning color. A hatched block from the last restorable point to the marker labeled with the data lost. To the right of the marker, a bar with stacked segments for detect, copy, replay, verify, each labeled with minutes.

**Bottom panels.** Left: `RPO_worst` against `I_arch` (log x, 1 s to 1 h), with a flat reference line showing that `I_base` has no effect when archiving is on. Right: `RTO_worst` against `I_base` (log x, 1 h to 168 h). A dot marks the current setting on each chart. Dragging `I_arch` visibly moves only the left dot; dragging `I_base` moves only the right dot.

**Results table.** Columns: RPO worst, RPO average, RTO worst, RTO at marker, player-hours lost at marker, archive storage per idle day.

**Test values (defaults).** `t_copy_h = 400 × 1000 / 250 / 3600 = 0.444 h`. `replay_worst_h = 10 × 24 / 100 = 2.4`. `RTO_worst = 0.25 + 0.444 + 2.4 + 0.25 = 3.34 h`. `RPO_worst = 60 s`. Weekly base: replay 16.8 h, RTO worst 17.74 h. 6-hourly: replay 0.6 h, RTO 1.54 h. Nightly full only (archiving off, `I_base` 24 h): RPO worst 24 h, RPO avg 12 h, RTO 0.94 h, player-hours lost on average `8,000 × 12 = 96,000`. Archive storage per idle day at 60 s: 1,440 × 16 MB = 23.04 GB; at 5 s: 276.5 GB.

**Accessibility and style.** Segment types distinguished by pattern as well as color. Shared tokens from `templates/interactive-tokens.css`. Respect `prefers-reduced-motion` (no animated marker transitions). No game art or logos.
