# MMO302 · Week 13 — Cloud deployment and autoscaling

**Why this matters:** Renting servers by the minute sounds like the end of launch-day queues. It isn't. A new zone server takes minutes to become useful, players arrive by the thousand per minute, and the gap between those two numbers decides whether your launch evening has a queue. This week you learn to size that gap, pay for it deliberately, and shrink the fleet again without kicking anyone out.

**You will be able to:**
- Compute the headroom an autoscaler must hold from the demand ramp rate and the provisioning lag, and the target utilization that follows from it.
- Simulate a target-tracking autoscaler minute by minute and predict the peak login queue for a given ramp, lag and utilization target.
- Explain why scaling in a stateful zone-server fleet is slower and riskier than scaling out, and compute the natural drain time from the session-length distribution.
- Design a capacity plan that mixes committed and on-demand servers for a daily player cycle, and justify the commitment level with numbers.

**Before class:** Kubernetes documentation, "Horizontal Pod Autoscaling", the sections "How does a HorizontalPodAutoscaler work?" and "Algorithm details" (kubernetes.io). Agones documentation, "Fleet Autoscaler Specification", the Buffer policy (agones.dev). Luke Stone, "Bringing Pokémon GO to life on Google Cloud" (Google Cloud blog, September 2016).

**Prerequisites from earlier courses:** [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (how many players one process can simulate inside its tick budget; that number is the capacity `c` in this lecture). [CS202 week 3, topologies](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) (the dedicated server). [DB201 week 1, why persistence is hard](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) (a server you shut down must have saved its players first). From this course, the CCU targets of [week 1](w01-scale-targets-ccu-messages-and-n-squared.md), hysteresis from [week 3](w03-area-of-interest-grids-radius-hysteresis.md), zone handoff from [week 4](w04-zone-servers-and-handoff.md) and the load-test bots from [week 11](w11-load-testing-with-bots.md). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) is used once, in section 3.

**Interactive:** [Autoscaling headroom](../examples/w13-autoscaling-headroom.html). Keep it open during section 2.

---

## 1. What the cloud changes, and what it doesn't

For most of MMO history, a studio bought its servers. Capacity was a purchase order, a shipping date and a rack in a data center. If a launch sold twice the expected copies, the extra machines arrived weeks later. Cloud providers changed the unit of purchase. You now rent a virtual machine (a VM, a slice of a physical server that behaves like its own computer) by the second, start it with an API call and hand it back when you are done.

Three terms come up all week.

- **Image.** A frozen copy of everything a server needs to run: the operating system, the .NET runtime, your world-server build, its configuration. In the reference stack this is a container image, a smaller package that shares the host's operating system kernel. You build it once per release and start identical copies from it.
- **Orchestrator.** The program that decides where copies run, restarts them when they crash and adds or removes them. Kubernetes is the common one. Agones is an open-source layer on top of Kubernetes built for game servers.
- **Fleet.** The set of running copies of one server type. You will have a zone-server fleet, a gateway fleet, a chat fleet, and so on.

An MMO backend has two kinds of fleet, and the cloud treats them very differently.

**Stateless services** hold nothing that matters between requests. The login gateway of week 9 checks a token against the database and forwards the player. Chat relays in week 10 move messages between players. If one copy dies, the next request goes to another copy and nobody notices. These fleets autoscale like any web service. Add copies when CPU is high, remove them when it is low.

**Stateful services** hold live game state in memory. A zone server owns every monster, every player position and every buff in its area, twenty times a second (the 20 Hz tick this lecture assumes). You cannot delete a zone server with 400 players inside the way you delete a web server. They would be disconnected, and anything not yet saved to PostgreSQL would be lost ([DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) put a number on that loss). Adding zone servers is easy. Removing them is the hard direction, and section 3 is about it.

### Capacity per server is a measured number

Every autoscaling calculation starts from one number, `c`: how many players one server process holds while staying inside its tick budget. You do not guess `c`. You measure it with the load-test bots of week 11, raising the bot count until the 95th-percentile tick time reaches the budget, then backing off.

Riot's write-up of the Valorant server work (August 2020) is a clean public example of how hard studios work on this number. The team set a target of 3 matches per CPU core on 36-core hosts, which is 108 matches or about 1,080 players per physical machine. At 128 ticks per second that left a budget of 2.34 ms per server frame. Their first measurements were at 50 ms, so they spent months cutting frame time before capacity planning made sense. Valorant is a match-based shooter, so its "server" holds one 10-player match. The principle carries over. `c` is the output of optimization and measurement, and every cost number in this lecture scales with `1 / c`.

In this lecture, one zone-server instance holds **`c = 500` players**. It runs on one 4-vCPU VM at 20 Hz.

## 2. Worked example: headroom must cover the lag

### The hook: 50 times the plan

In July 2016 Niantic launched Pokémon GO on Google Cloud. Google's reliability team later wrote that the launch had planned for a baseline of player traffic and a worst case of about 5 times that. Actual traffic reached about 50 times the baseline, ten times the worst case. The game ran on Google Container Engine (Google's managed Kubernetes), one of the largest Kubernetes deployments of its time, and Google's reliability engineers still had to help add capacity and swap in a different load balancer while the game was live.

Here is the puzzle. A cloud provider has far more machines than any one game needs. The autoscaler can ask for a thousand VMs in one API call. So why does any cloud-hosted game still show a queue on launch night? Because capacity you ask for now arrives later, and players do not wait for it.

### The model

Name the quantities.

- `D` is demand: players who want to be in the world right now (concurrent users, CCU).
- `r` is the ramp rate: how fast `D` grows, in players per minute.
- `c` is capacity per server, in players (500 here).
- `L` is the provisioning lag: minutes from the moment the autoscaler decides to add a server until that server accepts players.
- `u` is the target utilization: the fraction of capacity the autoscaler tries to fill. The autoscaler keeps `N = ⌈D / (u × c)⌉` servers.

With target utilization `u`, the fleet holds `D / u` player slots, so it has `D × (1/u − 1)` spare slots. Call that the **headroom**. During the lag, `r × L` new players arrive before any new server can help them. Nobody waits if the headroom already covers them:

```
headroom ≥ arrivals during the lag
D × (1/u − 1) ≥ r × L

which rearranges to

u ≤ D / (D + r × L)        and        N = (D + r × L) / c
```

The second form says the same thing in plain words. **Provision now for the demand you will have `L` minutes from now.** Target utilization is not a tuning preference. It is forced by the ramp and the lag.

### Where the lag comes from

`L` is the sum of every step between "we need more" and "a player is standing in the zone". A realistic breakdown for our zone server:

| Step | Minutes |
|---|---|
| Metric window (the autoscaler averages CPU or player count over 60 s so it does not chase noise) | 1.0 |
| Autoscaler sync interval (it checks every 30 s, so on average you wait half of that, rounded up here) | 0.5 |
| VM boot | 2.5 |
| Pull the container image (the world-server build plus navigation meshes and data) | 1.0 |
| Load the zone: spawn tables, NPCs, a warm cache from PostgreSQL and Redis, pass a health check | 3.0 |
| **Total `L`** | **8.0** |

These are planning numbers, not measurements from a particular game. Your own numbers come from timing each step in your deployment. Notice that most of the lag is yours, not the cloud provider's. The zone load step is game code.

### Numbers you can check

Start from `D = 20,000` players online, `c = 500`, `L = 8` minutes. Vary the ramp:

| Ramp `r` (players/min) | Arrivals during lag `r × L` | Max target utilization `u` | Servers needed `N` |
|---|---|---|---|
| 100 (a quiet evening) | 800 | 96.2% | 42 |
| 500 (a busy evening) | 4,000 | 83.3% | 48 |
| 1,000 (patch day, servers just back up) | 8,000 | 71.4% | 56 |
| 3,000 (expansion launch) | 24,000 | 45.5% | 88 |
| 10,000 (a Pokémon GO-sized surprise) | 80,000 | 20.0% | 200 |

Check the third row by hand. `r × L = 1,000 × 8 = 8,000`. `u ≤ 20,000 / 28,000 = 0.714`. `N = 28,000 / 500 = 56`. At the quiet-evening ramp you can run servers almost full. At launch you must run them less than half full, and the bill for the same 20,000 players more than doubles. This short script prints the table:

```python
import math

CAP = 500      # players one zone-server instance holds within its tick budget
LAG = 8        # minutes from "scale out" decision to a server taking players
D0 = 20_000    # players online when the ramp starts

print(" ramp/min  arrive in lag  max util  servers")
for ramp in [100, 500, 1_000, 3_000, 10_000]:
    arrive = ramp * LAG
    u_max = D0 / (D0 + arrive)
    servers = math.ceil((D0 + arrive) / CAP)
    print(f"{ramp:9,} {arrive:14,} {u_max:9.1%} {servers:8}")
```

Output:

```
 ramp/min  arrive in lag  max util  servers
      100            800     96.2%       42
      500          4,000     83.3%       48
    1,000          8,000     71.4%       56
    3,000         24,000     45.5%       88
   10,000         80,000     20.0%      200
```

### Watching it fail: a minute-by-minute simulation

The inequality tells you where the line is. A simulation shows what happens when you cross it. The autoscaler below checks demand every minute, computes `⌈D / (u × c)⌉`, and launches whatever is missing. Launched servers take `L` minutes to become ready. Players who find no free slot wait in the login queue. You pay for a server from the minute you launch it, because the cloud provider bills booting machines too.

```python
import math

def simulate(demand, cap=500, util=0.8, lag=8):
    """Minute-by-minute target-tracking autoscaler with a boot lag.
    Returns (peak players waiting, server-minutes paid)."""
    ready = math.ceil(demand[0] / (util * cap))
    booting = []                       # minute each launched server is ready
    peak_wait, paid = 0, 0
    for t, d in enumerate(demand):
        ready += booting.count(t)
        booting = [m for m in booting if m > t]
        want = math.ceil(d / (util * cap))
        short = want - ready - len(booting)
        if short > 0:
            booting += [t + lag] * short
        peak_wait = max(peak_wait, d - ready * cap)
        paid += ready + len(booting)
    return peak_wait, paid

# Launch evening: 20,000 online, then +3,000 players per minute for 20 minutes.
launch = [20_000 + 3_000 * min(t, 20) for t in range(60)]

print("util  lag  peak waiting  server-hours")
for lag in [8, 1]:
    for util in [0.9, 0.7, 0.45]:
        wait, paid = simulate(launch, util=util, lag=lag)
        print(f"{util:4.0%} {lag:4} {max(wait, 0):13,} {paid / 60:13.1f}")
```

Output:

```
util  lag  peak waiting  server-hours
 90%    8        21,500         154.8
 70%    8        15,000         199.0
 45%    8             0         309.3
 90%    1           500         154.8
 70%    1             0         199.0
 45%    1             0         309.3
```

Read the rows against the model. With an 8-minute lag, the rule said `u ≤ 45.5%`, and indeed only the 45% row has no queue. At 90% the queue peaks at 21,500 players, larger than the whole starting population. With a 1-minute lag, `r × L = 3,000` and the rule allows `u ≤ 20,000 / 23,000 = 87%`. The 90% row is just over that line, and the queue is a small 500. The bill for the hour depends only on utilization. Running at 45% costs 309 server-hours against 155 at 90%. So the two levers are clear. You can buy headroom (pay double) or cut the lag (make the queue vanish at the same price).

Open the interactive. The top view plots demand and ready capacity over time. Capacity climbs in steps that trail demand by `L`, and the gap between them is shaded as the queue. The bottom view plots every utilization setting as a point: server-hours on one axis, peak queue on the other. Drag the lag slider from 8 down to 1 and watch the whole curve in the bottom view slide toward the zero-queue axis. The shortest lag buys more than any utilization setting does.

### Cross-game recognition

Every cloud game-hosting tool you will meet is a version of `N = (D + r × L) / c`. What changes is which term it lets you set.

**Kubernetes Horizontal Pod Autoscaler (current documentation).** It computes `desiredReplicas = ⌈currentReplicas × currentMetric / desiredMetric⌉`. Put player count in as the metric and a per-server target of `u × c` as the desired value. That is exactly `⌈D / (u × c)⌉`. The HPA has no idea of `r` or `L`. You encode both by choosing the target `u`, which is the first row of our derivation. It also ignores changes within 10% of the target by default, and waits for a 5-minute stabilization window before scaling down. Both are defences against flapping, which section 3 comes back to.

**Agones Fleet Autoscaler, Buffer policy (current documentation).** Agones counts game servers as Ready (started and waiting), Allocated (hosting players) or Reserved. The Buffer policy keeps a fixed number or percentage of Ready servers on top of the Allocated ones, checking every 30 seconds by default. That buffer is our headroom written in servers instead of players. There is one difference that matters. A Ready server has already booted and loaded, so allocating it takes seconds. A buffer of Ready servers turns `L` from 8 minutes into the time to refill the buffer, and the player never sees the long part. The Agones autoscaler also never removes an Allocated server, which is the scale-in rule of section 3 built into the tool.

**Amazon GameLift target-based autoscaling (current documentation).** GameLift tracks a metric called `PercentAvailableGameSessions`, the share of the fleet's session slots that are free, and adds or removes instances to hold it at the target you set. That target is `1 − u`, the headroom fraction, stated directly. The documentation says openly that starting new instances and server processes can take minutes, and that a larger buffer means shorter waits but a bigger bill. That is our trade-off in the vendor's own words.

**EVE Online (Tranquility, time dilation since 2011).** EVE runs its whole universe as one shard, and each solar system lives on one server node. When thousands of players jump into one system, no autoscaler can split that system across new machines in time, because the lag for re-homing a live system is effectively infinite during the fight. CCP's answer, time dilation, slows the game clock in that system down to as little as 10% of normal speed. In our model, when `L` is unbounded and headroom is exhausted, the only variable left is the rate at which demand is served. Week 12 covers time dilation in detail.

Four products, one inequality. Kubernetes asks you for `u`. Agones asks for the headroom in servers and hides most of `L`. GameLift asks for `1 − u` directly. EVE, which cannot add capacity mid-fight, slows time instead.

### Design judgment

- **Headroom costs money every hour, not only on launch night.** If your ramp on an ordinary Tuesday is 100 players per minute, a 96% target is safe. Setting 45% all year because of launch night doubles your bill 364 days a year. Use a schedule. Raise headroom for known events (patch day, expansion launch, a streamer event) and lower it afterwards.
- **Cut `L` before buying headroom.** Most of the 8 minutes is your code: image size, world loading, cache warming. A pre-warmed pool of Ready servers, a smaller image, or a zone that loads its static data from a local snapshot instead of the database each shorten `L`, and shortening `L` shrinks the required headroom proportionally.
- **Measure the ramp you design for.** Your own login telemetry from previous events ([DB201 week 11, pipelines](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md)) gives `r`. Pokémon GO planned for 5× and got 50×, so assume your estimate is low and keep a fallback.
- **Plan the queue on purpose.** A login queue is not a failure if it is fair, visible and bounded. It protects the servers that are running. MMO407 week 2 (see the [MMO407 week 2 lecture](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md)) models queue length from arrival and admission rates. The autoscaler and the queue are two halves of one plan.
- **Know your ceiling.** Cloud accounts have quotas on how many VMs of a type you may run in a region. Raising a quota takes a support ticket and days. Check it before launch, not during.

## 3. Scaling in: the hard direction

Scaling out adds empty servers. Nobody is affected until players arrive. Scaling in removes a server, and on a stateful fleet every server you remove has players on it. A web autoscaler kills the least-useful copy. A game autoscaler must first make the server empty.

### Draining

The standard sequence is called draining.

1. Mark the server as not accepting new players. The gateway (week 9) stops routing logins and zone transfers to it.
2. Wait for it to empty, or actively move players out.
3. When it holds zero players and has saved everything to the database, shut it down.

How long does step 2 take if you just wait? Players log out on their own. If session lengths are roughly exponential with mean `S` minutes (a reasonable first model, which your telemetry can confirm or reject), the fraction still online after `t` minutes is `e^(−t/S)`. With `S = 90` minutes:

| Minutes after drain starts | Fraction still on the server |
|---|---|
| 30 | 71.7% |
| 90 | 36.8% |
| 180 | 13.5% |
| 270 | 5.0% |

Waiting for the last 5% takes `90 × ln 20 ≈ 270` minutes, four and a half hours. A daily player cycle has maybe six hours of decline from peak to trough. So passive draining barely finishes before demand rises again. That is why real fleets combine it with active moves.

- **Handoff.** Week 4's zone handoff moves a player to another server copy of the same zone. It is visible to the player (a short loading screen or a "server transfer" message) but costs seconds, not hours.
- **Pack new logins onto the fullest servers.** If the gateway sends new players to the least-loaded server, every server stays half-full and none can drain. If it sends them to the fullest server that still has room, the emptiest servers drain on their own. This is bin packing. Agones makes the same choice by default. Its Packed scheduling strategy allocates game servers on the nodes that are already busiest, so the quiet nodes empty and can be removed.
- **Drain at maintenance.** Many MMOs run a regular maintenance window in which every server restarts. That is also a free moment to change the fleet size.

### Hysteresis stops flapping

If the rule is "remove a server when utilization falls below the target", then demand that wobbles around the target makes the fleet add and remove the same server over and over. This is called flapping, and on a stateful fleet each flap is a drain that bothers players. The fix is the hysteresis you met for area-of-interest boundaries in week 3: two thresholds and a wait.

- Scale out when utilization is above `u` for 1 minute.
- Scale in only when it is below a lower threshold, say `u − 0.15`, for 15 minutes.

Kubernetes ships the same idea as defaults. It ignores changes within 10% of the target, and it will not scale down until the lower recommendation has held for a 5-minute window. For a stateful zone fleet you usually want a longer window than that, because an unnecessary drain costs more than an extra server-hour.

### The probability that a drain hits someone

Suppose you instead kill a server outright once it holds "almost nobody", say 5 players. Each of those players has some chance `p` of being in the middle of something that loses progress: a trade window, a crafting action, a boss pull. The complement rule from MA102 week 3 gives the chance that at least one of the `k` players is hit, `1 − (1 − p)^k`. With `p = 0.1` and `k = 5` that is 41%. Do this twice a day for a year and the forums will know. Drain to zero, or hand off.

## 4. Paying for the daily cycle

MMO demand follows the sun. Here is an invented but typical weekday for one region, in thousands of players online by hour (00:00 to 23:00 local):

```
22 17 14 12 12 12 13 15 17 19 21 22 23 24 25 27 30 34 38 40 39 35 30 26
```

Peak is 40,000 at 19:00, trough 12,000 in the early morning, average 23,625. Take `c = 500` and a day-to-day target `u = 0.8`, so each server carries 400 players.

- **Fixed fleet sized for peak:** `40,000 / 400 = 100` servers, 24 hours, 2,400 server-hours.
- **Autoscaled, hour by hour:** sum of `⌈D / 400⌉` over the 24 hours, which is 1,423 server-hours, 41% less.

The saving is close to `1 − average / peak = 1 − 23,625 / 40,000 = 41%`. The flatter your daily curve, the less autoscaling saves.

Cloud providers also sell capacity in more than one way, and real numbers vary by provider, region and year. Use round invented prices to see the structure:

- **On-demand:** $0.40 per server-hour, pay only for hours used.
- **Committed:** $0.24 per server-hour (a 40% discount), but you pay for all 24 hours whether or not you use the server.
- **Spot** (spare capacity sold cheaply that the provider can take back at short notice): fine for load-test bots, analytics jobs and build machines. Never for a zone server with players inside, because an interruption is an unplanned kill.

When should a server be committed? Commit the `k`-th server if it runs for at least `0.24 / 0.40 = 60%` of the day, that is 14.4 hours or more. In this curve the 53rd server is needed in 15 hours and the 54th in only 14, so the best commitment is 53 servers.

| Plan | Daily cost |
|---|---|
| Fixed 100 servers, all on-demand | $960.00 |
| Fixed 100 servers, all committed | $576.00 |
| Autoscaled, all on-demand | $569.20 |
| 30 committed (the trough) + on-demand above | $454.00 |
| 53 committed + on-demand above | $424.48 |

Recompute one row. The 53-server plan pays `53 × 24 × 0.24 = $305.28` for committed servers. On-demand server-hours are those above 53 in each hour, which total 298, so `298 × 0.40 = $119.20`. The sum is $424.48. The surprise is the middle rows. Autoscaling at full on-demand price saves almost nothing over simply committing to a peak-sized fleet. Autoscaling pays off only when you combine it with a committed base.

## In-class activity (25 minutes)

Work in pairs. You run a region with the daily curve from section 4 and are planning an expansion launch at 18:00. Marketing predicts a ramp of 2,000 players per minute for the first 15 minutes.

1. Time the lag. Using the breakdown table in section 2, decide which step you can shorten before launch and by how much. Write down your new `L`.
2. Compute the target utilization you need at 18:00 (demand 34,000) with the old and new `L`. How many servers does each need?
3. Marketing is wrong by 3×. With your new `L` and your chosen `u`, what is the peak queue? Use the interactive or the simulation code.
4. Write a two-line scaling schedule: the target `u` from 17:30 to 19:00 and the scale-in rule afterwards.

Expected output: two values of `L`, two server counts, the peak queue under the 3× error, and your schedule. Two pairs then compare schedules and pick the cheaper one that still meets a queue limit of 10,000.

## Common misconceptions

- **"In the cloud, capacity is instant."** API calls are instant. A zone server that can take players is not. Everything in this lecture follows from `L > 0`.
- **"Higher utilization is always more efficient."** Only when demand is flat. With a ramp, `u` above `D / (D + r × L)` buys a queue, and the saved servers cost less than the players who give up waiting.
- **"Autoscaling saves money by itself."** At on-demand prices it barely beat a committed peak fleet in section 4. The saving comes from committing to the base and autoscaling the rest.
- **"Scaling in is scaling out backwards."** Scaling out affects nobody. Scaling in removes a server that has players on it, so it needs draining, handoff and a longer stabilization window.

## Check yourself

1. A shard has 30,000 players online, a ramp of 1,500 players per minute, and a 6-minute lag. What is the highest safe target utilization, and how many 500-player servers must be running?
2. Your team cuts the zone load time from 3 minutes to 30 seconds. Every other step of the lag table stays the same. By how much does the required headroom shrink at a ramp of 1,000 players per minute?
3. In the simulation, the 70% utilization, 8-minute lag row has a peak queue of 15,000. Explain, without running code, why the 70% row with a 1-minute lag has none.
4. Session lengths are exponential with a mean of 60 minutes. How long does passive draining take to reach 10% of the starting population?
5. Committed capacity costs 70% of the on-demand price instead of 60%. Using the daily curve in section 4, which server is now the last one worth committing?

<details>
<summary>Answers</summary>

1. `r × L = 1,500 × 6 = 9,000`. `u ≤ 30,000 / 39,000 = 76.9%`. `N = 39,000 / 500 = 78` servers.
2. `L` falls from 8 to 5.5 minutes. Headroom `r × L` falls from 8,000 to 5,500 players, a drop of 2,500 players, or 5 fewer servers.
3. With `L = 1`, `r × L = 3,000`. The rule allows `u ≤ 20,000 / 23,000 = 87%`, and 70% is below that, so the headroom already covers the players who arrive during one minute of lag.
4. `e^(−t/60) = 0.1` gives `t = 60 × ln 10 ≈ 138` minutes.
5. The break-even is now 70% of 24 hours, 16.8 hours. Counting hours from the daily curve, the fleet needs at least 43 servers in 18 of the 24 hours but at least 44 in only 16. So the 43rd server is the last one worth committing. Commit 43 and run the rest on demand.

</details>

## Lab / assignment hook

[Lab 13, an autoscaler for a zone-server fleet](../labs/lab13.md). You get a Python fleet simulator with launch, evening and daily demand traces. You write the scaling policy: target tracking with headroom, a drain rule for scale-in and a placement rule for new logins. The tests check that your launch queue and server-hours stay under targets and that you never terminate a server with players on it.

## Sources

- Stone, L. "Bringing Pokémon GO to life on Google Cloud." Google Cloud blog, 29 September 2016. Launch-era figures: planned baseline, a worst case of about 5×, actual traffic about 50× (ten times the worst case); Google Container Engine and Cloud Datastore; one of the largest Kubernetes deployments of its time.
- Randall, B. "VALORANT's 128-Tick Servers." Riot Games technology blog, 31 August 2020. Target of 3 matches per core on 36-core hosts, a 2.34 ms frame budget, a starting point of 50 ms.
- Kubernetes documentation, "Horizontal Pod Autoscaling" (current as of 2026). The `desiredReplicas` formula, the default 10% tolerance and the default 5-minute scale-down stabilization window.
- Agones documentation, "Fleet Autoscaler Specification" (current as of 2026). Buffer policy with absolute or percentage `bufferSize`, required `maxReplicas`, 30-second default sync; Allocated game servers are not scaled down.
- Amazon GameLift Servers Developer Guide, "Target-based auto scaling" (current as of 2026). The `PercentAvailableGameSessions` metric, the buffer trade-off between wait time and cost, and the note that starting instances can take minutes.
- Agones documentation, "Scheduling and Autoscaling" (current as of 2026). Packed is the default strategy and allocates onto the most-used nodes first.
- EVE University Wiki, "Time dilation" (maintained wiki, current), and CCP Games, "Introducing Time Dilation (TiDi)" dev blog, 22 April 2011. Time dilation applies per server node and slows the clock down to a floor of 10%.
- Prices, lag breakdown, daily curve and capacity `c = 500` in this lecture are invented planning numbers for teaching, not figures from any provider or game.

## Interactive spec: examples/w13-autoscaling-headroom.html

**The one insight:** capacity you ask for arrives `L` minutes late, so the headroom you hold now must cover `r × L` players, and cutting `L` beats buying headroom.

**Layout.** Two linked views. On wide screens they sit side by side; at 390 px they stack, top view first.

**Top view: "Launch night, minute by minute".** X axis minutes 0 to 60. Y axis players (auto-scale to the max of demand and capacity). Draw:
- Demand `D(t)` as a solid line.
- Ready capacity `ready(t) × c` as a stepped line.
- Booting capacity (servers launched but not ready) as a lighter stacked band above ready capacity.
- The queue `max(0, D(t) − ready(t) × c)` as a shaded area between the two lines, in the palette's warning colour.
- A small readout under the chart: peak queue, minute of peak, server-hours for the 60 minutes.

**Bottom view: "What each utilization target costs".** X axis server-hours for the hour, Y axis peak queue (players). For the current `r`, `L`, `D0` and warm pool, plot one point for every `u` from 0.30 to 0.95 in steps of 0.05, joined by a line. Highlight the current `u` as a larger point. Draw a vertical dashed marker at the `u_max = D0 / (D0 + r × L)` point, labelled with its value.

**Controls** (all update both views immediately, keyboard-operable range inputs with visible numeric values):
- Target utilization `u`: 0.30 to 0.95, step 0.05, default 0.90.
- Lag `L`: 1 to 15 minutes, step 1, default 8.
- Ramp `r`: 0 to 10,000 players/min, step 100, default 3,000.
- Starting demand `D0`: 5,000 to 50,000, step 1,000, default 20,000.
- Ramp duration: 5 to 40 minutes, step 1, default 20.
- Warm pool `W`: 0 to 40 servers, step 1, default 0. Ready-but-empty servers available instantly; see the formulas.
- A preset row of buttons: "Quiet evening" (`r = 100`), "Patch day" (`r = 1,000`), "Launch" (`r = 3,000`), "Surprise hit" (`r = 10,000`).

**Formulas** (integer minutes, integers for players and servers, `c = 500` fixed and shown):
- Demand: `D(t) = D0 + r × min(t, ramp_duration)` for `t = 0 … 59`.
- Initial ready servers: `ready = ⌈D0 / (u × c)⌉ + W`.
- Each minute, in this order: servers whose ready minute equals `t` join `ready`; `want = ⌈D(t) / (u × c)⌉ + W`; `short = want − ready − booting`; if `short > 0`, launch `short` servers ready at minute `t + L`; `queue(t) = max(0, D(t) − ready × c)`; add `ready + booting` to paid server-minutes.
- Server-hours = paid server-minutes / 60.
- `u_max = D0 / (D0 + r × L)`.

**Test values** (`c = 500`, `D0 = 20,000`, `r = 3,000`, ramp 20 minutes, `W = 0`; these match the lecture):
- `u = 0.90, L = 8`: peak queue 21,500; server-hours 154.8.
- `u = 0.70, L = 8`: peak queue 15,000; server-hours 199.0.
- `u = 0.45, L = 8`: peak queue 0; server-hours 309.3.
- `u = 0.90, L = 1`: peak queue 500; server-hours 154.8.
- `u = 0.70, L = 1`: peak queue 0.
- `u_max` readout at `r = 3,000, L = 8`: 45.5%. At `r = 1,000, L = 8`: 71.4%.

**Accessibility and style:** shared palette from `templates/interactive-tokens.css`, light and dark mode, reduced motion (no animated transitions when `prefers-reduced-motion` is set), a text table under the charts listing minute, demand, ready, booting and queue every 5 minutes so the numbers can be copied. No game names or art in the visual.
