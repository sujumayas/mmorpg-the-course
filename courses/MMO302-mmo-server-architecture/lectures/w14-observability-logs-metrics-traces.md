# MMO302 · Week 14 — Observability: logs, metrics, traces

**Why this matters:** Players tell you the server is lagging while your dashboard says the average tick takes 20 ms of a 50 ms budget. Both are telling the truth. This week you learn which numbers to record so that the dashboard agrees with the players, how much each kind of record costs to keep, and why the system that watches your servers must not depend on them.

**You will be able to:**
- Compute stalls per minute and the share of seconds that contain a stall from a tick-time distribution, and pick the percentile an alert must watch for a given stall tolerance.
- Explain why averages and averaged percentiles hide bad zones, and compute fleet percentiles correctly from merged histogram buckets.
- Estimate the storage cost of logs, the series count of metrics, and the number of error traces kept under head and tail sampling.
- Design an alert and a dashboard for a zone-server fleet, and critique a monitoring setup that shares failure modes with the system it watches.

**Before class:** Beyer, Jones, Petoff and Murphy (eds.), *Site Reliability Engineering* (O'Reilly, 2016), chapter 6, "Monitoring Distributed Systems", free at sre.google. Dean and Barroso, "The Tail at Scale", *Communications of the ACM* 56(2), 2013, pages 74 to 76. The Prometheus documentation page "Histograms and summaries" (prometheus.io).

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one stall is `1 − (1 − p)^n`). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean, median and percentiles). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the tick budget `1000 / f` ms). DB201 weeks 10 to 12 on telemetry [events](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md), [pipelines](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md) and [dashboards](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md); this lecture is about operational data for engineers, while DB201 covered gameplay telemetry for designers. From this course, MMO302 [week 5, tick rate](w05-tick-rate-for-mmos-vs-shooters.md), [week 9, the gateway](w09-login-character-select-gateway-services.md), [week 11, load-test bots](w11-load-testing-with-bots.md) and [week 13, the autoscaler](w13-cloud-deployment-and-autoscaling.md).

**Interactive:** [Tick tail](../examples/w14-tick-tail.html). Keep it open during section 2.

---

## 1. Three signals, three questions

Observability is your ability to answer a question about a running system from the data it already emits, without shipping new code first. Three kinds of data do most of the work. The OpenTelemetry project, which defines a common format for them, calls them signals.

- **Metrics** are numbers measured at runtime and aggregated over time: ticks per second, players online, CPU. They answer "is something wrong, and since when?" They are cheap because a counter costs the same whether it counted 10 events or 10 million.
- **Logs** are records of single events: "player 81223 traded item 5541 to player 90017 at 19:02:11.304". They answer "what exactly happened to this player, this item, this server?" They cost storage per event.
- **Traces** follow one request as it passes through several services. A login goes from the gateway to the auth service to PostgreSQL to Redis to a zone server. Each step is a span with a start time and a duration. The trace answers "where did the time go on this request?"

A useful order of work follows from what each signal costs. Metrics tell you that something is wrong. Traces tell you where. Logs tell you what, for one specific case.

### What to measure first

Google's SRE book proposes four golden signals for any user-facing service. Rewritten for a zone server:

| Golden signal | Zone-server metric |
|---|---|
| Latency | Tick duration, as a histogram (not an average) |
| Traffic | Players in zone, messages in and out per second |
| Errors | Disconnects per minute, failed zone transfers, exceptions per tick |
| Saturation | Fraction of the tick budget used, send-queue depth, garbage-collection pause time |

The first row is where most teams go wrong, and it is the subject of the worked example.

## 2. Worked example: the average tick that hides the stalls

### The hook: EVE would rather be slow than spiky

In a large EVE Online battle, thousands of players in one solar system send commands to one server node. Commands arrive in bursts, so without intervention the node would process some ticks quickly and others very late. Players would see normal speed broken by freezes, and some commands would miss their window entirely. Since 2011 CCP's answer has been time dilation. The server slows the clock for the whole system, down to a floor of 10% of normal speed, so that everything happens in slow motion but at a steady pace. The client even shows an icon with the current dilation percentage.

Think about what that choice implies. CCP chose to make every second ten times slower rather than let a few seconds freeze. Players accept a uniform slowdown more readily than random stalls. So the number that describes what players feel is not the average tick time. It is how often a tick runs late.

### The model

Name the quantities for one zone server.

- `f` is the tick rate in hertz (ticks per second). Our zone runs at 20 Hz.
- `B = 1000 / f` is the tick budget in milliseconds. At 20 Hz, `B = 50 ms`.
- A **stall** is a tick that takes longer than `B`. The server falls behind and every player in the zone sees it as a hitch or a rubber-band.
- `p` is the fraction of ticks that stall, the overrun rate.
- The **q-th percentile** of tick time is the value that a fraction `q` of ticks are at or below. The median is the 50th percentile, p50.

Two results follow.

```
stalls per minute                     = 60 × f × p
chance a given second has a stall     = 1 − (1 − p)^f

and the link between p and percentiles:

   p_q ≤ B   exactly when   p ≤ 1 − q
```

The last line says a percentile is an overrun rate in disguise. "p99 is under budget" means "at most 1% of ticks stall". So you choose the percentile from the stall rate you can tolerate. To allow at most `k` stalls per minute, you need `p ≤ k / (60 × f)`, so you must watch the percentile `q = 1 − k / (60 × f)`.

The second formula is the complement rule from MA102 week 3. It assumes stalls are independent from tick to tick. Real stalls often cluster (a garbage-collection pause can hit several ticks in a row), so treat it as an estimate and measure the real number from your data.

### Numbers you can check

Here are 1,000 ticks from one zone server. Most ticks do normal work and take 12 to 24 ms. Twenty ticks include an autosave batch and take 45 ms. Ten ticks hit a garbage-collection pause and take 140 ms.

```python
import math

BUDGET = 50  # ms per tick at 20 Hz

# 1,000 ticks from one zone server: normal work, autosave batches, GC pauses.
ticks = [12 + (i * 7) % 13 for i in range(970)] + [45] * 20 + [140] * 10

def pct(values, q):
    """Nearest-rank percentile: the smallest value with at least q of the data at or below it."""
    s = sorted(values)
    return s[math.ceil(q * len(s)) - 1]

mean = sum(ticks) / len(ticks)
over = sum(t > BUDGET for t in ticks) / len(ticks)
print(f"mean {mean:.1f} ms  p50 {pct(ticks, 0.50)}  p95 {pct(ticks, 0.95)}  "
      f"p99 {pct(ticks, 0.99)}  p99.9 {pct(ticks, 0.999)}  max {max(ticks)}")
print(f"ticks over budget: {over:.1%}")
print(f"stalls per minute at 20 Hz: {over * 20 * 60:.0f}")
print(f"seconds containing a stall: {1 - (1 - over) ** 20:.1%}")
```

Output:

```
mean 19.8 ms  p50 18  p95 24  p99 45  p99.9 140  max 140
ticks over budget: 1.0%
stalls per minute at 20 Hz: 12
seconds containing a stall: 18.2%
```

Read the first line the way a dashboard would. The mean is 19.8 ms, 40% of budget. The median is 18. Even p99 is 45 ms, under the 50 ms budget. Every summary a team usually puts on a dashboard is green. The second line says 1% of ticks stall. At 20 ticks per second that is 12 stalls every minute, and almost one second in five contains one. That matches what the players are reporting.

Check the arithmetic by hand. Ten ticks out of 1,000 exceed 50 ms, so `p = 0.01`. `60 × 20 × 0.01 = 12`. `0.99^20 ≈ 0.818`, so `1 − 0.818 = 18.2%`. And p99 at 45 ms is consistent with the rule, since `p ≤ 1 − 0.99` holds with equality. p99 sits right on the edge, which is why it looks fine and the players do not.

Here is the same calculation across overrun rates:

| Overrun rate `p` | Stalls per minute at 20 Hz | Seconds with a stall | Percentile that must stay under 50 ms |
|---|---|---|---|
| 0.1% | 1.2 | 2.0% | p99.9 |
| 0.5% | 6 | 9.5% | p99.5 |
| 1% | 12 | 18.2% | p99 |
| 2% | 24 | 33.2% | p98 |
| 5% | 60 | 64.2% | p95 |

Suppose your design goal is "a player sees at most one stall per minute". Then `p ≤ 1 / 1200 ≈ 0.083%`, and the percentile you must watch is p99.92. A dashboard that shows p95 is watching a number that stays green while every player stalls once a second.

Open the interactive. The left view is a strip of 600 ticks (30 seconds at 20 Hz), one bar per tick, with a line at the budget and a line at the mean. The right view is the same ticks sorted from fastest to slowest, with markers at p50, p95, p99 and p99.9. Raise the spike probability slider from 0 to 2%. The mean line barely moves. The strip fills with red bars above the budget line. The stalls-per-minute readout, measured from the ticks on the strip, climbs from 0 into the high 20s (28 with the default seed 1). A 600-tick strip at 2% holds only about 12 spikes, so the measured count moves by several stalls from seed to seed. The note under the strip gives the formula value at 2%, exactly `60 × 20 × 0.02 = 24`.

### Cross-game recognition

**Web services at Google (Dean and Barroso, 2013).** "The Tail at Scale" uses the same formula with servers in place of ticks. If one server answers 1 request in 100 slowly (1 second or more), and a user request must wait for 100 servers, the chance the user waits is `1 − 0.99^100 ≈ 63%`. Rewrite that in our form: `f = 100` samples, `p = 0.01`. A tick loop is a fan-out in time. A web request is a fan-out in space. In both, a tail that is rare per sample becomes common per user.

**Google's SRE book (2016).** The monitoring chapter gives the web version of our dashboard trap. A service can average 100 ms at 1,000 requests per second while 1% of requests take 5 seconds. The book recommends counting requests in latency buckets instead of averaging, with bucket edges spaced roughly by a factor of 3. That is the histogram of section 3.

**Valorant (Riot Games, August 2020).** Riot gave Valorant's 128-tick servers a budget of 2.34 ms per frame, so that three matches fit on one CPU core. Their engineers built a subsystem telemetry system that charged each frame's time to named subsystems such as replication, animation, networking, movement and physics, and compared those numbers across builds to catch regressions. Knowing that a frame is late is the metric. Knowing which subsystem made it late is the attribution a trace gives you. Riot reported that this measurement let them predict launch hardware needs to within about 1%.

**EVE Online (since 2011).** Time dilation is the same principle turned into a design fix. When `p` would be high, CCP stretches the budget `B` itself by slowing game time, so no tick is late relative to the dilated clock. The dilation percentage becomes a health metric that players see directly.

### Design judgment

- **Record distributions, not averages.** Emit tick time as a histogram. You can compute any percentile afterwards from a histogram. You cannot recover the tail from a mean.
- **Put a bucket edge exactly at the budget.** With an edge at 50 ms, the count of ticks above 50 ms is exact, and it is the overrun rate `p` that the formulas need. Percentiles estimated between edges are approximations (section 3 shows how rough).
- **Alert on stalls per minute, per zone.** It is a number players understand and designers can set a goal for. Derive the percentile from it, not the other way round.
- **Averages are still useful for capacity.** Mean tick time times tick rate is CPU use, which is what the autoscaler of week 13 needs. Use the mean for cost, the tail for experience.
- **Know when to change the design.** If the tail comes from a big fight that the server cannot handle, no alert fixes it. That is when you look at interest management (week 3), splitting zones (week 4) or EVE's route of slowing time (week 12).

## 3. Metrics at fleet scale

### Histograms aggregate, percentiles don't

A metrics system such as Prometheus stores a histogram as a set of counters, one per bucket, each counting observations less than or equal to its upper edge (Prometheus calls the edge `le`). Every zone server increments its own counters. To get a fleet view you add the counters bucket by bucket, then estimate a percentile from the sums. Prometheus's documentation is blunt about the alternative. Averaging percentiles that servers computed on their own rarely makes sense.

Here is why, with ten zone servers: the busy one from section 2 and nine quiet ones whose ticks take 8 to 13 ms.

```python
BOUNDS = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 250]  # bucket upper edges, ms

def histogram(values):
    """Cumulative counts: how many values are <= each bound, plus the total."""
    return [sum(v <= b for v in values) for b in BOUNDS] + [len(values)]

def quantile(q, counts):
    """Estimate a quantile from cumulative buckets by linear interpolation."""
    rank = q * counts[-1]
    lower_bound, lower_count = 0, 0
    for bound, count in zip(BOUNDS, counts):
        if count >= rank:
            return lower_bound + (bound - lower_bound) * (rank - lower_count) / (count - lower_count)
        lower_bound, lower_count = bound, count
    return BOUNDS[-1]

busy = [12 + (i * 7) % 13 for i in range(970)] + [45] * 20 + [140] * 10
quiet = [8 + i % 6 for i in range(1000)]
servers = [busy] + [quiet] * 9

per_server = [quantile(0.99, histogram(s)) for s in servers]
merged = [sum(col) for col in zip(*(histogram(s) for s in servers))]
print("p99 per server:", [round(p, 1) for p in per_server[:2]], "...")
print(f"average of the p99s: {sum(per_server) / len(per_server):.1f} ms")
print(f"p99 of merged buckets: {quantile(0.99, merged):.1f} ms")
print(f"fleet ticks over 50 ms: {merged[-1] - merged[BOUNDS.index(50)]} of {merged[-1]}")
```

Output:

```
p99 per server: [50.0, 14.9] ...
average of the p99s: 18.4 ms
p99 of merged buckets: 23.8 ms
fleet ticks over 50 ms: 10 of 10000
```

Three lessons sit in those four lines.

1. **The estimate is only as good as the buckets.** The busy server's true p99 is 45 ms. The histogram says 50.0, because all it knows is that the 990th tick lies somewhere between the 40 and 50 ms edges, and linear interpolation lands on the top edge. The quiet servers' true p99 is 13 ms; the estimate says 14.9.
2. **The average of p99s is not a percentile of anything.** 18.4 ms is neither the fleet's p99 (23.8) nor any server's. Never put it on a dashboard.
3. **Fleet-wide numbers hide the bad zone.** Both fleet numbers look healthy. The bad zone shows up only in a per-zone view, and the exact count "10 ticks over 50 ms" comes straight from the bucket edge at 50. This is the argument for labelling tick metrics by zone and alerting per zone.

### Labels and the cardinality bill

A label is a key-value pair attached to a metric, like `zone="harbor-02"`. Prometheus's naming guide points out that every unique combination of label values is a separate time series, and warns against labels with unbounded values such as user IDs. Count the series:

| Metric | Labels | Series |
|---|---|---|
| Tick-time histogram (12 bucket edges + the `+Inf` bucket + sum + count = 15 series per zone) | zone (200) | 3,000 |
| Messages per second | zone (200) × message type (40) | 8,000 |
| Same, plus `player_id` | × up to 20,000 players | up to 160,000,000 |

A metrics store that handles ten thousand series comfortably will fall over at a hundred million. The rule is simple. Labels have small, fixed sets of values: zone, server role, region, build version, message type. Anything that identifies a single player, item or session goes into logs or traces, which are built for that.

## 4. Logs: the record of what happened

When a player writes in to say a sword disappeared during a trade, no metric will answer them. You need the log of that trade.

### Structured logs and correlation IDs

Write logs as structured records (JSON lines or a similar key-value format), not as free text. Every record carries a timestamp, a level, the service, and the IDs a support engineer will search by: player, character, item, zone, and a correlation ID. The correlation ID is created once when a request enters the system (at the gateway, in week 9's design) and passed along to every service that handles it. Searching one correlation ID then returns every log line for that request, across every server.

Week 8's item transactions deserve the strongest logging you have. Every item creation, transfer and destruction gets a record with the item's unique ID, both owners and the transaction ID. That audit trail is how you find a duplication exploit after the fact, and it is also a data set DB201's pipelines can query.

### The volume budget

Logs cost storage and ingestion per byte. Estimate before you ship. Suppose each online player causes, on average, one log line per second across all services (combat events, loot, chat moderation, trades, zone transfers; movement is never logged per packet), and each line is 250 bytes.

```
20,000 players × 1 line/s × 250 bytes = 5,000,000 bytes/s = 5 MB/s
5 MB/s × 86,400 s/day                 = 432,000 MB = 432 GB per day
```

At that rate a 30-day retention holds about 13 TB. Three habits keep it in check.

- **Levels.** Debug output is off in production and turned on for one zone at a time when needed.
- **Sampling for routine events.** Keep 1 in 100 "monster killed" lines. Keep every trade, every item change and every error.
- **Retention by type.** Item audit logs may need to be kept for months. Routine combat logs can go after a week.

Logs are also where privacy rules bite. Do not log passwords, session tokens or payment data, and check what personal data you keep against the retention rules covered in [DB201 week 13, privacy, GDPR and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md).

## 5. Traces: where did the time go?

A player reports that logging in took 8 seconds. The gateway's latency histogram confirms that p99 login time jumped from 1.2 to 7 seconds at 20:00. The metric says when. A trace says where.

A trace of one login might look like this (each line is a span, indented under the span that called it):

```
login                               gateway          2,410 ms
  verify token                      auth service        35 ms
  load character                    character svc    2,050 ms
    SELECT character + inventory    PostgreSQL       1,980 ms   (waiting on a row lock)
  write session                     Redis                4 ms
  place in zone                     zone server        290 ms
```

The critical path is the character load, and inside it a query waiting on a lock. That is a [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) problem, and without the trace you would have started by profiling the zone server.

### Sampling: which traces do you keep?

Recording every span of every request costs more than logs. So you sample. The OpenTelemetry documentation describes two approaches.

- **Head sampling** decides at the start of the request, before anything is known about it. Keep 1% at random. Simple and cheap, but it cannot guarantee that the traces with errors are the ones kept.
- **Tail sampling** buffers the spans until the request finishes, then decides. Keep every trace that errored or was slow, plus a small random share of the rest. It keeps what you need, at the price of running a stateful collection service.

Put numbers on it. The gateway handles 50 logins per second at the evening peak, and 0.2% of them fail.

```
failing logins        = 50 × 0.002          = 0.1 per second  = 360 per hour
head sampling at 1%   = 360 × 0.01          = 3.6 failed-login traces per hour
tail sampling         = all 360 failures + 1% of successes (49.9 × 0.01 × 3,600 ≈ 1,800) per hour
```

With head sampling you would have fewer than four examples an hour of the thing you are investigating. With tail sampling you have all of them, plus a baseline of normal logins to compare against.

## 6. Alerts, and the monitor that shares your fate

### Alert on symptoms players feel

An alert wakes a person up, so every alert must be about something a player would notice and something a person can act on. The SRE book's advice is to page on symptoms (players stalling, logins failing) and use causes (a CPU at 90%, a disk filling) for dashboards and tickets. For a zone fleet, two alerts cover most of it.

- **Stalls:** any zone above 2 stalls per minute for 5 minutes. From section 2, that is an overrun rate above `2 / 1200 ≈ 0.17%`, measured from the bucket at 50 ms.
- **Logins:** more than 1% of logins failing, or p99 login time above 5 seconds, for 5 minutes.

The 5-minute window is hysteresis again. It stops one bad tick from paging anyone.

### Roblox, October 2021

Roblox was down for 73 hours from 28 to 31 October 2021. The cause was inside Consul, the service-discovery system Roblox's services used to find each other. A newly enabled streaming feature caused contention under heavy load, and a pathological behaviour in Consul's storage layer made each write enormously larger than it should have been. Roblox's own post-mortem adds the part that matters for this week. The monitoring systems that would have shown the problem faster depended on Consul themselves, so the outage also blinded the team that was trying to diagnose it. Removing that dependency was on Roblox's list of follow-up work.

The principle generalises. Your observability stack must not share a failure mode with the thing it watches. In the reference stack that means:

- Metrics and logs do not go through the same Redis or PostgreSQL that the game uses.
- The metrics system runs in a different failure domain (another cluster, and for the most important alerts another region or provider) from the zone servers.
- There is at least one outside probe, a small bot that logs in from outside your network every minute and reports whether it succeeded, so that "everything is down" still produces an alert.

MMO308 week 13 on incident response (see the [MMO308 syllabus](../../MMO308-live-operations-analytics-and-experimentation/syllabus.md)) picks up from the moment the alert fires.

## In-class activity (25 minutes)

Work in groups of three. Your world server from the labs runs 40 zones at 20 Hz. Design its monitoring on one page.

1. List the metrics for each golden signal, with their labels. Compute the total series count and check it stays under 20,000.
2. Choose tick-histogram bucket edges. Justify each edge near the budget.
3. Write the two alerts with exact thresholds and windows, derived from a stated stall goal.
4. Name one failure your design cannot see, and one component your monitoring depends on that could fail with the game.

Expected output: a metrics table with series counts, a bucket list, two alert rules and the two named weaknesses. Swap sheets with another group and find one label that could explode in cardinality.

## Common misconceptions

- **"Mean tick time under budget means the server keeps up."** The mean says how busy the CPU is. Players feel the tail. A mean at 40% of budget can come with 12 stalls per minute.
- **"p99 is the tail, so watching p99 is safe."** p99 under budget still allows 1% of ticks to stall, which is 12 per minute at 20 Hz. Choose the percentile from the stall goal.
- **"You can average each server's p99 to get the fleet's p99."** You cannot. Merge the histogram buckets, then estimate.
- **"Log everything, sort it out later."** At 5 MB/s you pay for 432 GB a day. Decide what each event type is for and set its sampling and retention.

## Check yourself

1. A zone runs at 30 Hz with an overrun rate of 0.5%. How many stalls per minute does a player see, and what share of seconds contain one?
2. Your stall goal is at most 3 stalls per minute at 20 Hz. Which percentile must stay under the 50 ms budget?
3. A histogram has edges at 25 and 50 ms. Of 1,000 ticks, 900 are at or below 25 ms and 1,000 at or below 50 ms. What p95 does linear interpolation estimate? Can the true p95 be 26 ms?
4. A team adds a `client_version` label (6 live versions) to a counter already labelled by zone (200) and message type (40). How many series now, and is this a reasonable label?
5. The gateway handles 80 logins per second and 0.5% fail. How many failed-login traces per hour do you keep under 2% head sampling? Under tail sampling that keeps all failures?

<details>
<summary>Answers</summary>

1. Stalls per minute `= 60 × 30 × 0.005 = 9`. Share of seconds with a stall `= 1 − 0.995^30 ≈ 14.0%`.
2. `p ≤ 3 / 1200 = 0.25%`, so p99.75 must stay under 50 ms.
3. Rank `0.95 × 1000 = 950` lies in the 25 to 50 ms bucket. Estimate `25 + 25 × (950 − 900) / (1000 − 900) = 37.5 ms`. Yes, the true p95 could be 26 ms, or anything in that bucket. The histogram only knows the bucket.
4. `200 × 40 × 6 = 48,000` series, six times the old 8,000. The label has a small, bounded set of values, so it is acceptable if you need it. Drop it if no alert or dashboard uses it.
5. Failures `= 80 × 0.005 = 0.4` per second `= 1,440` per hour. Head sampling at 2% keeps about 29. Tail sampling keeps all 1,440.

</details>

## Lab / assignment hook

[Lab 14, tick telemetry and a stall alert](../labs/lab14.md). You implement a mergeable tick-time histogram, a nearest-rank percentile and a per-zone stall alert, then run them over an hour of recorded ticks from 12 zones. The tests check your percentiles, that merged histograms equal the histogram of the combined data, and that your alert finds the one zone with a clustered garbage-collection problem. The lab's histogram is the one your week 15 load test reports.

## Sources

- EVE University Wiki, "Time dilation" (maintained wiki, current), and CCP Games, "Introducing Time Dilation (TiDi)" dev blog, 22 April 2011. Per-node slowdown to a floor of 10% speed, the client icon showing the dilation percentage, the purpose of keeping a steady pace in large fights.
- Dean, J. and Barroso, L. A. "The Tail at Scale." *Communications of the ACM* 56(2), 2013, pp. 74-80. The 1-in-100 slow server, fan-out to 100 servers, about 63% of requests affected.
- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.) *Site Reliability Engineering*. O'Reilly, 2016, chapter 6, "Monitoring Distributed Systems". The four golden signals; the 100 ms average with 1% of requests at 5 seconds; latency buckets spaced by about a factor of 3; paging on symptoms.
- Randall, B. "VALORANT's 128-Tick Servers." Riot Games technology blog, 31 August 2020. 2.34 ms frame budget, three matches per core, per-subsystem frame-time telemetry, hardware prediction to within about 1%.
- Prometheus documentation, "Histograms and summaries" and "Metric and label naming" (current as of 2026). Aggregating summary quantiles rarely makes sense; histogram quantiles are estimated by interpolation within buckets; each label combination is a new series; avoid user IDs as labels.
- OpenTelemetry documentation, "Signals" and "Sampling" (current as of 2026). Definitions of traces, metrics and logs; head versus tail sampling and their trade-offs.
- Roblox, "Roblox Return to Service 10/28-10/31/2021." Roblox newsroom, January 2022. 73-hour outage; Consul streaming contention and a storage-layer pathology; monitoring that depended on Consul slowed diagnosis and was later decoupled.
- Tick distributions, player counts, log rates and sampling rates in this lecture are invented teaching numbers, not measurements from any game.

## Interactive spec: examples/w14-tick-tail.html

**The one insight:** the mean tick time can sit far below budget while players stall many times a minute; the overrun rate (a percentile chosen from the stall goal) is what players feel.

**Layout.** Two linked views. Side by side on wide screens, stacked at 390 px with the strip first. A readout row above both views.

**Readout row:** mean, p50, p95, p99, p99.9 (nearest rank), overrun rate `p`, stalls per minute `60 × f × p`, seconds containing a stall `1 − (1 − p)^f`. Each value colored by whether it is under budget (neutral) or over (warning), except stalls per minute, which turns warning above the stall-goal control.

**Left view: "Tick strip".** 600 consecutive ticks as vertical bars (x = tick index, y = ms, y axis 0 to max(160, max tick)). A horizontal line at the budget `B = 1000 / f`, labelled. A dashed horizontal line at the mean, labelled. Bars over budget in the warning colour.

**Right view: "Sorted ticks".** The same 600 ticks sorted ascending (x = rank as percent, 0 to 100; y = ms). Vertical markers at p50, p95, p99, p99.9 with their values. The budget line again. The region where sorted ticks exceed the budget is shaded; its width on the x axis is `p`, so the student sees the percentile/overrun link directly.

**Controls** (range inputs with numeric values, keyboard operable, all update immediately):
- Tick rate `f`: 10, 20, 30, 60 Hz (segmented buttons), default 20.
- Base tick time: 5 to 45 ms, default 18. Normal ticks are `base − 6 + ((i × 7) mod 13)` ms, clamped at a minimum of 1 ms.
- Spike probability: 0% to 5%, step 0.1%, default 1.0%.
- Spike size: 30 to 200 ms, default 140.
- Clustered spikes toggle, default off. When on, spikes come in runs of 3 consecutive ticks and the run start probability is spike probability / 3, so the mean overrun rate is unchanged.
- Stall goal: 0.5 to 10 stalls per minute, default 1. Shows the derived percentile `q = 1 − k / (60 × f)` beside it and draws that percentile as an extra marker in the right view.
- A "Reseed" button.

**Generation.** Use a seeded PRNG (mulberry32, seed shown and editable, default 1) so screenshots are reproducible. A tick is a spike if `rand() < spike probability` (or run logic when clustered). Spike ticks take the spike size exactly.

**Formulas.** `B = 1000 / f`. Nearest-rank percentile: sort ascending, take index `ceil(q × n) − 1`. `p = (ticks > B) / n`. Stalls per minute `= 60 × f × p`. Seconds with a stall `= 1 − (1 − p)^f`. When clustered is on, also show the measured share of 1-second windows (blocks of `f` ticks) containing a stall, next to the formula value, labelled "measured".

**Test values** (these match the lecture): with the deterministic lecture data set, available as a "Lecture data" button that replaces the random ticks with the 1,000 ticks `[12 + (i × 7) mod 13 for i < 970] + 20 × [45] + 10 × [140]` in that order at 20 Hz, the readout must show mean 19.8, p50 18, p95 24, p99 45, p99.9 140, overrun 1.0%, 12 stalls per minute, 18.2% of seconds. For the table in section 2 (formula values, `f = 20`): `p = 0.1%` gives 1.2 and 2.0%; `p = 2%` gives 24 and 33.2%; `p = 5%` gives 60 and 64.2%. Stall goal 1 at 20 Hz shows `q = 99.92%`.

**Accessibility and style:** shared palette from `templates/interactive-tokens.css`, light and dark mode, `prefers-reduced-motion` respected, a collapsible text table of the sorted-tick percentiles for copying. No game names or art in the visual.
