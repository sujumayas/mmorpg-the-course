# DB201 · Week 12 — Dashboards and KPIs

**Why this matters:** "DAU is down 8%" can end a feature, start a crisis meeting or move a launch date. But DAU is not a fact you read off the database. It is a definition someone wrote in SQL, and two reasonable definitions can disagree by more than the change everyone is worried about. This week you learn to write KPI queries whose definitions are explicit, and dashboards that show people what the number means.

**You will be able to:**
- Compute DAU, WAU or MAU, stickiness, and D1 and D7 retention from a session log, by hand and in SQL.
- Show how the activity threshold, the day boundary and the counting unit change DAU, and quantify the change on a given log.
- Explain why distinct counts cannot be summed across days, and choose between a user-day table and HyperLogLog for rolling MAU, with storage and error figures.
- Critique a dashboard tile for missing definitions, missing denominators and unfair comparisons.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 3, the section on data warehousing and "aggregation: data cubes and materialized views". Skim the "Special Note Regarding Operating Metrics" at the start of Roblox's most recent annual report on Form 10-K (SEC EDGAR, free). Reread MA102 week 12 on choosing a summary statistic.

**Prerequisites from earlier courses:** [DB201 week 11, pipelines](w11-pipelines-collect-store-query.md) (raw events, rollups, late-arriving events). [DB201 week 3, select, join, aggregate](w03-sql-i-select-join-aggregate.md) (`GROUP BY`, `COUNT(DISTINCT ...)`). [DB201 week 7, Redis](w07-nosql-and-key-value-stores-redis.md) (keys and data types). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean versus median, fair comparisons). Looking ahead, [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (year 3) applies the same denominator problem to an economy. Retention curves, cohorts and A/B tests get a full treatment later in [MMO308 weeks 2 to 6](../../MMO308-live-operations-analytics-and-experimentation/syllabus.md). This week is the data side.

**Interactive:** [w12-dau-definitions.html](../examples/w12-dau-definitions.html). Keep it open during section 2.

---

## 1. KPIs are definitions

A **KPI** (key performance indicator) is a number a team agrees to watch because it summarizes something they care about. For a live game the common ones are:

- **DAU**, daily active users: how many distinct players were active on a day.
- **WAU** and **MAU**, weekly and monthly active users: distinct players active at least once in a 7-day or 30-day window.
- **Stickiness**: mean DAU over a window divided by the active users of that window, usually DAU/MAU. It answers "on a typical day, what share of this month's players show up?"
- **Dn retention**: of the players who installed on a given day (a **cohort**), the share active exactly n days later. D1, D7 and D30 are the usual checkpoints.
- **CCU** and **PCU**, concurrent and peak concurrent users: how many are logged in at one instant, and the highest such value in a period. MMOs care about these because server capacity is sized by them.
- **Session length**: minutes per session, usually reported as a median because a few marathon sessions pull the mean.
- **ARPDAU**, average revenue per daily active user: revenue divided by DAU. [GS101 week 11](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) used the monthly version to compare business models.

Every item on that list contains the word "active", "distinct", "day" or "player". Each word hides a decision.

- **Active** means what? Logged in? Played at least 5 minutes? Did anything besides open the menu?
- **Day** by which clock? UTC midnight is simple for the database, but a player in California who plays from 19:00 to 23:00 local time crosses UTC midnight every evening.
- **Player** means what? An account, a character, or a person? One person with two accounts is two "users" in almost every database.

A KPI is the SQL query plus those decisions. Change a decision and the number changes, even though no player did anything differently.

## 2. Worked example: three DAUs from one log

### The hook

Roblox reports DAU to its investors every quarter, and its annual report defines the number in unusual detail. The 2025 annual report (filed February 2026) says a DAU is a user who logged in and visited on a unique registered account on a given calendar day. It adds a special rule. If a logged-in user visits more than once within a 24-hour period that spans two calendar days, they count only for the first day. It says that DAU for a period, such as a month, is the average of the daily values. And it warns that because DAU measures account activity, and one person may play on several accounts, DAU is not a count of unique people. It adds that undetected bot accounts can overstate it.

Read that again as a database designer. A company reporting 127 million average DAUs for 2025 spends a paragraph on midnight, averaging, alternate accounts and bots. Each of those is a clause in a `WHERE` or a `COUNT(DISTINCT ...)`. If the definition did not matter, nobody would write it down.

### The model

Let `active(u, d)` be 1 if user `u` has at least one qualifying session on day `d`, and 0 otherwise. Then:

```
DAU(d)        = Σ_u active(u, d)
WAU           = number of users with Σ_d active(u, d) ≥ 1   over the 7 days
stickiness    = mean DAU / WAU
              = (Σ_u Σ_d active(u, d)) / (7 × WAU)
              = (mean active days per weekly user) / 7
```

The last line is worth remembering. Stickiness is just the average number of days a weekly (or monthly) player shows up, divided by the window length. A DAU/MAU of 0.20 means the typical monthly player is active about 6 days out of 30.

Three decisions define `active(u, d)`:

1. **Threshold `T`**: a session qualifies if it lasts at least `T` minutes.
2. **Day boundary**: a session belongs to the UTC day of its start, or to the player's local day.
3. **Unit**: `u` is an account, or a person (grouping alternate accounts).

### Numbers you can check

Here is one week (Monday to Sunday) of sessions for six accounts. Cells show minutes played, placed on the UTC day the session started.

| Account (person) | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Note |
|---|---|---|---|---|---|---|---|---|
| A1 (P1) | 45 | 30 | — | 60 | — | 90 | 40 | Regular |
| A2 (P1) | 3 | — | 20 | — | — | 15 | — | P1's alt, used for crafting |
| A3 (P2) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | Logs in for the daily reward, leaves |
| A4 (P3) | — | 50 | 50 | — | 70 | 80 | — | Lives in UTC−8, plays at 19:00 local (03:00 UTC next day) |
| A5 (P4) | — | — | — | — | — | 120 | 150 | Weekend player |
| A6 (P5) | — | — | 25 | — | — | — | — | Tried it once |

A4 also has a 60-minute session at 03:00 UTC on the following Monday, outside this week in UTC.

**Definition D1, any session, UTC day, accounts.** Count non-empty cells per column.

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Sum | Mean DAU | WAU | Stickiness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | 3 | 3 | 4 | 2 | 2 | 5 | 3 | 22 | 3.14 | 6 | 0.52 |

Check stickiness both ways. 3.14 / 6 = 0.52. Or 22 active account-days over 6 accounts is 3.67 days each, and 3.67 / 7 = 0.52.

**Definition D2, sessions of 5 minutes or more.** A3 disappears entirely (every session is 2 minutes), and A2's Monday login goes too.

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Sum | Mean DAU | WAU | Stickiness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | 1 | 2 | 3 | 1 | 1 | 4 | 2 | 14 | 2.00 | 5 | 0.40 |

**Definition D3, any session, player's local day.** Only A4 changes. Each of A4's sessions moves back one day: Tuesday UTC becomes Monday local, and the following Monday's session becomes this Sunday.

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Sum | Mean DAU | WAU | Stickiness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3 | 4 | 3 | 3 | 3 | 2 | 4 | 4 | 23 | 3.29 | 6 | 0.55 |

**Definition D4, any session, UTC day, people.** A1 and A2 merge into P1. Monday and Saturday each lose one, because both of P1's accounts played.

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Sum | Mean DAU | WAU | Stickiness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D4 | 2 | 3 | 4 | 2 | 2 | 4 | 3 | 20 | 2.86 | 5 | 0.57 |

Line the summaries up.

| Definition | Mean DAU | WAU | Stickiness | Busiest day |
|---|---|---|---|---|
| D1, any, UTC, accounts | 3.14 | 6 | 0.52 | Saturday (5) |
| D2, 5 min or more | 2.00 | 5 | 0.40 | Saturday (4) |
| D3, local day | 3.29 | 6 | 0.55 | Mon, Sat, Sun tie (4) |
| D4, people | 2.86 | 5 | 0.57 | Wed, Sat tie (4) |

Same players, same sessions. Mean DAU ranges from 2.00 to 3.29, a spread of 64%. Stickiness goes **down** under D2 and **up** under D4, so even the direction of a "change" depends on which definition you compare. The busiest day moves when you change the clock.

Toy data exaggerates, so check at scale. In Lab 12's generated data (3,000 accounts, 60 days), DAU on 1 April 2026 is 653 by D1, 593 by D2 (−9%), 674 by D3 (+3%) and 644 by D4 (−1%). A 9% gap between two reasonable definitions is larger than most week-to-week changes a live team reacts to.

### The visual

Open `examples/w12-dau-definitions.html`. The top view is the grid above. Each cell lights up when it counts under the current definition. The bottom view is a bar chart of DAU for each day, with mean DAU, WAU and stickiness printed beside it.

Drag the threshold slider from 1 to 30 minutes. Watch A3's row go dark at 3 minutes and A2's Saturday at 16, while the bars shrink unevenly. Toggle the day boundary to "local". A4's row slides one cell to the left, and the tallest bar moves. Toggle the unit to "people". A1 and A2 merge into one row. The picture to take away is this: the log never changes, only the lens. A dashboard that shows "DAU" without saying which lens is showing you a number you cannot interpret.

### Cross-game recognition

**Roblox (annual report on Form 10-K for 2025).** Covered in the hook. Its choices in our vocabulary: threshold, any logged-in visit; day boundary, calendar day with a special rule for visits within 24 hours that span midnight; unit, accounts, with an explicit warning that accounts are not people. The filing does not spell out every edge case of the midnight rule, which is itself the lesson. Even a carefully written definition leaves decisions to whoever writes the SQL.

**EVE Online (5 May 2013).** EVE reported a record of 65,303 accounts logged in at once. That is a PCU, a different kind of "active" measured at an instant rather than over a day. It shares D1's unit problem. It counts concurrent **accounts**, so one player flying two ships on two accounts counts twice. For a single-shard MMO, where every player shares one server cluster, PCU is the number that sizes hardware, so counting accounts is the right choice there. The load on the server is per account, not per person.

**MMO304 week 12, money supply per active player (year 3).** In the economics course you will see a team compute "gold per active player" and reach opposite conclusions with different denominators, because players who left kept their gold and alternate characters multiplied "players". It is the same decision about the unit and the activity rule, made on the bottom of a ratio instead of on its own.

Three contexts: a platform's investor report, an MMO's server record, an economy dashboard. One idea. "Active user" is a definition with at least three parameters, and every number built on it inherits them.

### Design judgment

- **Pick the definition that matches the decision.** Capacity planning wants accounts and instants (PCU). Business reporting usually wants accounts per calendar day, because that is what the industry reports. Design questions ("do players come back?") are better served by people and a minimum-play threshold, because a 2-minute reward login is not engagement with your content.
- **Fix the definition before the data arrives, and write it on the dashboard.** The failure mode is not choosing the "wrong" definition. It is changing the definition silently and comparing across the change.
- **Report more than one when they disagree.** If D1 and D2 diverge over time, that is information. A growing gap means more players are logging in for rewards and leaving, which is a design signal a single DAU line would hide.
- **Local days for design, UTC days for the pipeline.** Store everything in UTC (week 11), and compute local days in the query when the question is about player behavior ("do people play more on weekends?").
- **Bots and alts are part of the definition.** Decide whether flagged bots are excluded and say so. [MMO309 week 7](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w07-bot-detection-behavioral-features.md) covers detection. Your job here is to leave room in the schema for an `is_flagged` join.

## 3. Writing KPIs in SQL

The lab's schema is two tables, `accounts(account_id, person_id, install_day, utc_offset_hours)` and `sessions(account_id, start_utc, minutes)`. In PostgreSQL, with `start_utc` as `timestamptz`:

```sql
-- D1: DAU by UTC day
SELECT (start_utc AT TIME ZONE 'UTC')::date AS day,
       COUNT(DISTINCT account_id)           AS dau
FROM sessions
GROUP BY day
ORDER BY day;

-- D3: DAU by the player's local day
SELECT ((s.start_utc AT TIME ZONE 'UTC') + make_interval(hours => a.utc_offset_hours))::date AS day,
       COUNT(DISTINCT s.account_id) AS dau
FROM sessions s JOIN accounts a USING (account_id)
GROUP BY day;

-- D7 retention per install cohort (exact-day definition)
SELECT a.install_day,
       COUNT(*) AS cohort,
       AVG((EXISTS (SELECT 1 FROM sessions s
                    WHERE s.account_id = a.account_id
                      AND (s.start_utc AT TIME ZONE 'UTC')::date = a.install_day + 7))::int) AS d7
FROM accounts a
WHERE a.install_day + 7 <= DATE '2026-04-29'
GROUP BY a.install_day
ORDER BY a.install_day;
```

In SQLite, used in the lab, the date arithmetic is `date(start_utc)`, `date(start_utc, utc_offset_hours || ' hours')` and `date(install_day, '+7 days')`. Everything else is the same.

Two details in the retention query deserve attention.

- **Exact-day versus rolling retention.** The query counts a player as D7-retained if they played **on** day 7. Some tools count anyone who played on day 7 **or later**. Rolling retention is always higher, since it can only add players. Neither is wrong, but a D7 of 40% under one and 55% under the other are not comparable.
- **Only complete cohorts.** The `WHERE` clause drops cohorts whose day 7 has not happened yet. Leave it out and the newest cohorts show D7 of zero, which looks like a catastrophe on the chart.

In Lab 12's data, the 1 March cohort has 216 accounts, D1 of 65.7% and D7 of 42.6%.

## 4. Distinct counts do not add up

Here is the error that breaks the most dashboards. In the worked example, the seven D1 DAU values sum to 22. WAU is 6. Summing daily active users counts a player once for every day they played, so the sum measures **user-days**, not users. At scale, Lab 12's last 30 days have a mean DAU of 564.1, so the 30 DAU values sum to 16,922, while MAU is 2,945.

This matters for pipelines because week 11 taught you to pre-aggregate. You can store `daily_zone_deaths` and sum it over a month, because counts add. You cannot store `daily_dau` and get MAU by summing it, because distinct counts do not add. A rolling 30-day MAU needs to know **which** users were active each day. How many is not enough.

Two practical answers.

**A user-day table.** One row per active user per day: `user_day(day, account_id)`, filled by a nightly job from raw sessions. DAU is `COUNT(*)` for a day. MAU for any window is `COUNT(DISTINCT account_id)` over 30 days of it. For the reference game's 40,000 DAU, that is 40,000 rows a day, about 40 bytes each with overhead (28 + 8 + 4), so 1.6 MB a day and 584 MB a year. Exact, cheap, and it answers WAU, MAU, stickiness and retention from one table. For most games this is the right answer.

**HyperLogLog.** When the user-day table is too large (hundreds of millions of users) or the number is needed in real time, use a **HyperLogLog**, a data structure that estimates the number of distinct items in a set using a fixed, small amount of memory. Redis has it built in. `PFADD dau:2026-03-05 <account_id>` as each session starts; `PFCOUNT dau:2026-03-05` for DAU; `PFCOUNT` over 30 keys at once (or `PFMERGE` them into one) for a rolling MAU. Redis documents a maximum of 12 KB per key and a standard error of 0.81%. A year of daily keys is 365 × 12 KB, about 4.4 MB. The price is precision. On an MAU of 150,000, one standard error is about 1,215 users, so a day-over-day change of 0.5% in an HLL-based MAU is noise.

| Approach | Storage per year (40,000 DAU) | MAU for any window | Error |
|---|---|---|---|
| Sum of daily DAU | 365 numbers | no, gives user-days | wrong by design |
| User-day table | about 584 MB | yes, `COUNT(DISTINCT)` | exact |
| Redis HyperLogLog per day | about 4.4 MB | yes, `PFCOUNT` over 30 keys | 0.81% standard error |

In PostgreSQL, a user-day table built by a nightly job can be a **materialized view**, a stored query result refreshed on demand with `REFRESH MATERIALIZED VIEW`. Adding `CONCURRENTLY` lets dashboards keep reading during the refresh, and requires a unique index on the view. SQLite has no materialized views, so the lab creates an ordinary table.

## 5. Designing the dashboard

A **dashboard** is a page of tiles, each showing one number or chart, refreshed on a schedule. Most bad dashboards fail in a few recurring ways. Here is a checklist you can apply to any tile, including the ones you build in Lab 12.

1. **One question per tile.** "Are players coming back?" is a question. "Engagement" is not. Write the question as the tile's title.
2. **Definition in the tile.** A footnote with the threshold, day boundary and unit: "DAU, accounts with a session of 5 min or more, UTC day". If you cannot write the footnote, you do not know what the number means.
3. **Show the denominator.** "Deaths in zone 7: 25,000" says nothing without "players in zone 7: 4,100". The same denominator lesson applies to every ratio, and MMO304 week 12 will apply it to gold per player.
4. **Compare like with like.** Player activity has a weekly rhythm (in the worked example, Saturday is the busiest day). Compare Saturday with last Saturday, not with Friday. A "10% drop" from Saturday to Sunday may be every week's normal.
5. **Mark provisional data.** Week 11's late events mean the most recent day or two are incomplete. Grey them out or label them. Otherwise every dashboard shows a "drop" on the right edge, every morning.
6. **Show the noise.** A daily number moves even when nothing changes. Show the last 8 weeks of the same weekday so a reader can see the normal range. [MA102 week 13](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) gives you the tools to put an interval on it.
7. **Few tiles.** A dashboard with 40 tiles gets skimmed. One with 6 gets read. Every tile that nobody acted on in a month is a candidate to delete.

The query side follows from week 11. Every tile reads a rollup or the user-day table, never the raw events, and the refresh interval matches how fast the underlying number can meaningfully change. A DAU tile refreshed every minute shows a partial day that rises from zero each midnight. Refresh it daily, or show "today so far" beside the same hour yesterday.

## In-class activity (25 minutes)

Pairs, then groups of four.

1. **Write the definitions (8 min).** For your team's PR201 project (or an invented game), write the definition of DAU, MAU and D7 retention in one sentence each, naming threshold, day boundary and unit. Justify each choice in one sentence by the decision it supports.
2. **Break them (7 min).** Swap with another pair. Invent one player whose behavior makes their definition give a misleading answer (for example, a player in UTC+9 who plays at 08:00 local, or a player with four alts). Compute what their DAU counts for that player over a week.
3. **Design the tiles (10 min).** As a group of four, sketch a six-tile dashboard for a live producer who meets every Monday. For each tile: question, definition footnote, comparison baseline, refresh schedule, and which table it reads (rollup, user-day table or HLL).

Expected output: three definitions per pair, one counterexample from the other pair, and a six-tile sketch with footnotes.

## Common misconceptions

- **"DAU is a fact."** It is a query. In Lab 12's data the same day has DAU of 593 or 674 depending on reasonable choices. Always ask for the definition before reacting to a change.
- **"MAU is the sum of DAUs, or DAU times 30."** Distinct counts do not add. The 30 DAUs sum to 16,922 user-days, while MAU is 2,945. You need user-level data (a user-day table or an HLL) for any distinct count over a window.
- **"High stickiness means the game is healthy."** Stickiness rises when casual players leave, because the remaining monthly players are the daily ones. A shrinking game can have rising stickiness. Read it next to MAU, never alone.
- **"D7 retention of 0% for yesterday's cohort means disaster."** Yesterday's cohort has not reached day 7. Only complete cohorts belong on the chart.

## Check yourself

1. In the worked example, set the threshold to 30 minutes (UTC day, accounts). Compute the DAU for each day, mean DAU, WAU and stickiness.
2. A game has MAU 90,000 and stickiness 0.18. What is its mean DAU? On average, how many days a month does a monthly player play?
3. A tile shows "WAU = 41,300" computed as the sum of the last seven daily rollup values of DAU. What does the number actually measure? What would you need to compute real WAU?
4. You keep one Redis HyperLogLog per day. Your MAU estimate for March is 240,000. What is one standard error in users? The next day's estimate is 241,500. Should the live team announce growth?
5. A cohort of 500 players installed on 2 March. 190 played on 9 March, and 260 played at least once between 9 March and 1 April. What is exact-day D7 retention, and what might a tool that reports rolling D7 show?

<details>
<summary>Answers</summary>

1. Sessions of at least 30 minutes: A1 on Mon 45, Tue 30, Thu 60, Sat 90, Sun 40; A4 on Tue 50, Wed 50, Fri 70, Sat 80; A5 on Sat 120 and Sun 150. A2, A3 and A6 never reach 30. DAU Mon to Sun is 1, 2, 1, 1, 1, 3, 2, sum 11, mean 1.57. WAU is 3 (A1, A4, A5). Stickiness 11 / (7 × 3) = 0.52.
2. Mean DAU = 0.18 × 90,000 = 16,200. Days per month = 0.18 × 30 = 5.4.
3. It measures user-days, how many (account, day) pairs were active, so a player active all seven days counts seven times. Real WAU needs user-level data over the seven days: `COUNT(DISTINCT account_id)` over a user-day table, or `PFCOUNT` over the seven daily HyperLogLog keys.
4. 0.81% of 240,000 is about 1,944 users. A change of 1,500 is smaller than one standard error, so it is indistinguishable from estimation noise. Do not announce it.
5. Exact-day D7 = 190 / 500 = 38%. A rolling D7 counts anyone active on day 7 or later, so it would be at least 260 / 500 = 52%. The two are not comparable, and the dashboard footnote must say which is shown.

</details>

## Lab / assignment hook

[Lab 12, KPIs in SQL](../labs/lab12.md). You compute DAU under four definitions, 30-day MAU, stickiness and D1 and D7 retention from 45,123 sessions, check each against a reference, and design a one-page dashboard whose every tile carries its definition. Deliverable: your `kpis.py`, the CSV outputs, a dashboard specification and a 300-word memo on which DAU definition the team should adopt.

## Sources

- Roblox Corporation, Annual Report on Form 10-K for the fiscal year ended 31 December 2025, filed 11 February 2026 (SEC EDGAR, accession 0001315098-26-000024), "Special Note Regarding Operating Metrics" and Item 1. Definition of a DAU, the rule for visits within 24 hours that span two calendar days, period DAU as the average of daily DAUs, the statement that DAUs are not a measure of unique individuals, the note that bot accounts can overstate DAU, and 127 million average DAUs in 2025.
- Wikipedia, "Eve Online" (accessed September 2026). Record of 65,303 concurrent accounts logged in on 5 May 2013.
- Redis documentation, "HyperLogLog" (accessed September 2026). Up to 12 KB per key and a standard error of 0.81%; `PFADD`, `PFCOUNT`, `PFMERGE`.
- PostgreSQL 17 documentation, "CREATE MATERIALIZED VIEW" and "REFRESH MATERIALIZED VIEW" (the `CONCURRENTLY` option and its unique index requirement), and "Date/Time Functions and Operators" (`AT TIME ZONE`, `make_interval`).
- SQLite documentation, "Date And Time Functions" (modifiers such as `'+7 days'` and `'-8 hours'`).
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 3 (data warehousing, materialized views and data cubes).
- Lab 12 figures: `labs/lab12-starter`, seed 1212, 3,000 accounts, 60 days, computed with SQLite 3.53 in September 2026.

## Interactive spec: examples/w12-dau-definitions.html

**The one insight.** The session log never changes. Only the definition of "active" changes, and it moves DAU, WAU and stickiness by more than most real-world changes a team reacts to, sometimes in opposite directions.

**Layout.** Two linked views, stacked on all widths (grid above, chart below), with the controls in a bar between them that stays visible on scroll.

**Data (hard-code exactly).** Days are Mon to Sun (index 0 to 6), plus index 7 for the following Monday, drawn as a greyed extra column labelled "next Mon".

| Account | Person | UTC offset for local mode | Sessions as (UTC day index, minutes) |
|---|---|---|---|
| A1 | P1 | 0 | (0,45) (1,30) (3,60) (5,90) (6,40) |
| A2 | P1 | 0 | (0,3) (2,20) (5,15) |
| A3 | P2 | 0 | (0,2) (1,2) (2,2) (3,2) (4,2) (5,2) (6,2) |
| A4 | P3 | −1 day shift (UTC−8, sessions at 03:00 UTC) | (1,50) (2,50) (4,70) (5,80) (7,60) |
| A5 | P4 | 0 | (5,120) (6,150) |
| A6 | P5 | 0 | (2,25) |

**Controls.**
- Threshold slider, 1 to 30 minutes, default 1. A session counts if `minutes ≥ threshold`.
- Day boundary toggle, "UTC day" (default) or "local day". In local mode, A4's sessions move to `dayIndex − 1`. Sessions landing outside 0 to 6 do not count.
- Unit toggle, "accounts" (default) or "people". In people mode, rows with the same person merge into one row that is active on a day if any of its accounts is.
- Presets D1, D2 (threshold 5), D3 (local), D4 (people).

**Top view, the grid.** One row per account (or person), one column per day. Each cell shows its minutes. A counted cell is filled with the accent color; an uncounted session is outlined only; an empty cell is blank. In local mode, animate A4's cells sliding one column left (no animation under `prefers-reduced-motion`).

**Bottom view, the chart.** Seven bars of DAU per day with the value on each bar. Beside the chart: sum of DAU (labelled "user-days"), mean DAU, WAU, stickiness, and the busiest day or days. A faint ghost of the D1 bars stays behind the current bars so the change is visible.

**Formulas.** `DAU[d] = count of units with at least one counted session on d` for d in 0 to 6; `WAU = count of units with any counted session in 0 to 6`; `meanDAU = sum(DAU) / 7`; `stickiness = sum(DAU) / (7 × WAU)`.

**Test values.**
- D1 (threshold 1, UTC, accounts): DAU 3,3,4,2,2,5,3; sum 22; mean 3.14; WAU 6; stickiness 0.524.
- D2 (threshold 5): 1,2,3,1,1,4,2; sum 14; mean 2.00; WAU 5; stickiness 0.400.
- D3 (local): 4,3,3,3,2,4,4; sum 23; mean 3.29; WAU 6; stickiness 0.548.
- D4 (people): 2,3,4,2,2,4,3; sum 20; mean 2.86; WAU 5; stickiness 0.571.
- Threshold 30, UTC, accounts: 1,2,1,1,1,3,2; sum 11; mean 1.57; WAU 3; stickiness 0.524.
- Threshold 5, local, people: 2,2,2,2,1,2,3; sum 14; mean 2.00; WAU 4; stickiness 0.500.

**Secondary panel, "why you can't add DAUs".** A small readout that always shows "sum of DAU = N user-days, WAU = M users" in the current mode, with one sentence: a player active on k days is counted k times in the sum and once in WAU.

**Accessibility.** Grid is a real table with cell states announced ("A4, Tuesday, 50 minutes, counted"). Controls keyboard-operable. Shared palette from `templates/interactive-tokens.css`. No game art.
