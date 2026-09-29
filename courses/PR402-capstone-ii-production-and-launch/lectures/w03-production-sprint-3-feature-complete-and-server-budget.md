# PR402 · Week 03 — Production sprint 3: feature complete and the server budget

**Why this matters:** Next week your game stops living on laptops. Alpha needs every system in and a server that outsiders can reach, and from then until the showcase that server costs money every hour it runs. Most student teams guess the bill from player numbers. The numbers below show that, at your scale, the bill is set mostly by which machines you leave switched on.

**You will be able to:**
- Write alpha exit criteria that define "feature complete" for your game in checkable terms.
- Forecast average, evening-peak and launch-day concurrent players from sign-ups, conversion and session length.
- Size your zone server fleet from a load-test knee and a target utilization.
- Build a semester hosting budget by environment and schedule, and cut it below a fixed cap.

**Before class:** Bring your load-test results from PR401's technical design or your latest bot run (players per zone server at the knee). Bring your cloud provider's price page for the machine types you use, printed or saved. Read [MMO302 week 13, sections 1 and 2](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) on capacity per server and headroom (about 25 minutes).

**Prerequisites from earlier courses:** [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (finding the knee). [MMO302 week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md). [MMO407 week 2, capacity planning and login queues](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md). [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md). [MMO308 week 2, DAU and MAU](../../MMO308-live-operations-analytics-and-experimentation/lectures/w02-kpis-dau-mau-stickiness-arpdau.md). [PR402 week 1](w01-production-sprint-1-the-ops-tax.md) (the feature budget).

---

## 1. What "feature complete" means

Alpha is a gate, and a gate needs criteria someone can check. "Feature complete" is the usual name for the alpha gate, and it means different things in different studios. In this course it means four things.

1. **Every system is in and connected.** Each feature kept in your lab 01 backlog exists in the build and works end to end with the others. Trading works with the inventory, parties work with quest credit, the guild chat survives a zone change.
2. **No placeholder logic.** Placeholder art and text are fine. Placeholder rules are not. If the crafting recipe table is a hard-coded list of three items, crafting is not in.
3. **Server authority holds.** Every value path (gold, items, experience) is decided on the server, as required since [PR201](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md). Alpha is the last cheap moment to find a client that decides its own loot.
4. **It runs where testers will run it.** A build from the release pipeline, deployed to the production environment, joinable from a machine outside the team.

Write your version as a checklist of 10 to 20 lines, each one a test a stranger could run. "Two players in a party both receive quest credit for a kill by either" is a criterion. "Parties work" is not. The instructor uses your list at the week 4 alpha review, so write it for someone who has never seen your game.

Anything not on the list after sprint 3 is either cut or goes on the trigger list from lab 01. It does not quietly continue into week 4. Features that land during alpha week meet testers without ever having been tested together.

## 2. Three environments

From week 4 you need at least three places where the game runs:

- **Dev.** Each person's machine, or a shared dev server. Broken often, and that is fine.
- **Staging.** A copy of production where each build is tried before release. It uses the same machine types, configuration and database schema as production, with test data.
- **Production.** What testers and players connect to. Only builds that passed staging and the release checklist ([PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md)) reach it.

Each environment is a set of machines, and each machine costs money per hour while it runs, whether anyone plays or not. That fact drives the budget below.

## 3. From sign-ups to concurrent players

You size servers by **concurrent users** (CCU), the number of players connected at one moment. Start from what you can estimate:

```
average CCU     = DAU × session hours / 24
evening peak    = average CCU × peak ratio
launch peak     = evening peak × launch spike
```

- **DAU** is daily active users, the number of distinct players on a day ([MMO308 week 2](../../MMO308-live-operations-analytics-and-experimentation/lectures/w02-kpis-dau-mau-stickiness-arpdau.md)). For launch, estimate it as sign-ups times the share you expect to play on launch day.
- **Session hours** is the average hours one player plays per day. Your PR401 and alpha playtests give a first value.
- **Peak ratio** is peak CCU divided by average CCU. A global audience spread over time zones has a low ratio, near 1.5. A student audience in one time zone, playing in the evening, has a high one, around 3.
- **Launch spike** is how much busier the first day is than a normal day. Use 2 unless you have evidence.

Then, as in [MMO302 week 13](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md), size the fleet with headroom:

```
usable per server = knee × u
servers           = ceil(peak CCU / usable per server)
```

`knee` is the player count per zone server where your load test showed latency starting to climb steeply ([MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md)). `u` is the target utilization, the share of the knee you plan to fill, usually 0.6 to 0.8.

## 4. Worked example: the bill is the switch, not the players

### The hook

Palworld entered early access on 19 January 2024. It sold two million copies in its first 24 hours and eight million by its sixth day. On 27 January it recorded 2,101,867 concurrent players on Steam, and the player count caused server problems. It was the first game since PUBG: Battlegrounds to pass two million concurrent players on Steam, and Pocketpair had built a game, not a server plan for that.

You will not have Palworld's problem. At capstone scale the surprise runs the other way. Teams worry about a flood of players and budget for it. Then the money goes on servers that nobody switched off. This example shows both sides with one team's numbers.

### The model

```
avg CCU    = DAU × s / 24
peak CCU   = avg CCU × k × spike
servers    = ceil(peak CCU / (knee × u))
cost       = Σ over machines ($ per hour × hours switched on)
           + egress $ per GB × player-hours × GB per player-hour
```

- `s` is session hours per day, `k` the peak ratio, `spike` the launch-day factor.
- **Egress** is data sent from your servers to players, which most cloud providers bill per gigabyte. Data coming in is usually free.
- Every machine is billed for the hours it is switched on, not the hours it is used.

### Numbers you can check

Emberfall expects 1,200 sign-ups by launch and 25% of them to play on launch day, so `DAU = 300`. Alpha playtests gave `s = 1.5` hours. The audience is mostly students in one time zone, so `k = 3`, and `spike = 2`.

| Quantity | Calculation | Value |
|---|---|---|
| Average CCU | 300 × 1.5 / 24 | 18.8 |
| Evening peak | 18.8 × 3 | 56.2 |
| Launch-day peak | 56.2 × 2 | 112.5 |
| Usable per zone server | knee 80 × `u` 0.7 | 56 |
| Zone servers, normal evening | ceil(56.2 / 56) | 2 |
| Zone servers, launch evening | ceil(112.5 / 56) | 3 |

Check the evening row: 56.25 players need slightly more than one server's 56 usable slots, so two servers. The evening peak is close to the launch target of 60 CCU in Emberfall's PR401 technical design.

This sizes zone servers one at a time. The zone servers in a shard also share one login service and one database, and those set a second limit. [Week 8](w08-open-beta.md) load-tests the whole shard to find it, and week 9 decides what to do when the launch peak is above it. The budget below assumes the week 9 answer. The third zone server for launch evening runs as a second shard with its own gateway and database, not as a third zone server in the first shard.

Now the costs. The prices below are invented round numbers for teaching. Replace them with your provider's prices in the lab. One production or staging stack is one zone server ($0.08 per hour), one small gateway and login machine ($0.02) and a managed database ($0.05), so $0.15 per hour. An extra zone server is $0.08 per hour. Egress is $0.09 per GB, and the load test measured 20 KB per second per player, which is 72 MB per player-hour. The semester runs from week 4 (alpha) to week 15 (showcase), 12 weeks. The department grant is $500.

**Naive plan.** Production and staging both run all the time from alpha on. An extra zone server runs four hours every evening from open beta (week 8) on. In launch week a second shard stack runs for 120 hours, from launch until the merge that week 9 plans for about day 5.

| Line | Calculation | Cost ($) |
|---|---|---|
| Production stack, always on | 0.15 × 168 h × 12 weeks | 302.40 |
| Staging stack, always on | 0.15 × 168 × 12 | 302.40 |
| Extra zone server at peak | 0.08 × 28 h × 8 weeks | 17.92 |
| Second shard stack, launch week | 0.15 × 120 h | 18.00 |
| Egress | beta, launch week and six later weeks of play | 97.98 |
| Load tests | 3 runs × 20 bot machines × 2 h × $0.04 | 4.80 |
| **Total** | | **743.50** |

The plan is $243.50 over the grant. Look at where the money goes. The three lines that depend on players, the peak zone server, the second shard and egress, add up to $134, about 18% of the total. The two stacks left switched on are $605, 81%.

**Fixed plan.** Nothing about the players changes. Only the schedules do.

| Line | Change | Cost ($) |
|---|---|---|
| Production, weeks 4-7 | Scheduled for 60 hours a week of alpha and closed beta sessions | 36.00 |
| Production, weeks 8-15 | Always on from open beta | 201.60 |
| Staging | Scheduled for 40 hours a week of team work time | 72.00 |
| Extra zone server at peak | Same | 17.92 |
| Second shard stack, launch week | Same | 18.00 |
| Egress | Same | 97.98 |
| Load tests | Same | 4.80 |
| **Total** | | **448.30** |

$51.70 under the grant, and that margin is the launch spike reserve. It also keeps the total under the lab 03 limit of the grant less 10%, $450. One more line belongs in the risk register: a load-test fleet of 20 bot machines forgotten over a weekend runs about 60 hours and costs $48. That is almost all of the reserve, lost to one missing shutdown command. Set a budget alert at 50% and 80% of the grant with your provider, and add "bot fleet destroyed" to the load-test checklist.

The egress line uses 60 testers a day in beta weeks 5 to 8, 300 a day in launch week and 150 a day for the six weeks after. For example, launch week is `300 × 1.5 × 7 = 3,150` player-hours, `3,150 × 72 MB = 227 GB` and `227 × 0.09 = $20.41`.

This program reproduces both tables:

```python
import math

# Demand at launch (week 9)
dau, session_h, peak_ratio, spike = 300, 1.5, 3, 2
avg_ccu = dau * session_h / 24
peak = avg_ccu * peak_ratio
launch_peak = peak * spike
knee, u = 80, 0.7                       # load-test knee per zone server, target utilization
per_server = knee * u
print(f"avg CCU {avg_ccu:.1f}, evening peak {peak:.1f}, launch-day peak {launch_peak:.1f}")
print(f"zone servers: normal {math.ceil(peak / per_server)}, launch {math.ceil(launch_peak / per_server)}")

# Costs in dollars (invented list prices)
stack = 0.08 + 0.02 + 0.05              # zone server + gateway + database, per hour
zone, egress_gb, mb_per_ph = 0.08, 0.09, 72


def egress(player_hours):
    return player_hours * mb_per_ph / 1000 * egress_gb


peaks = 8 * 28 * zone                  # one extra zone server 4 h/evening, weeks 8-15
shard2 = stack * 120                    # second shard stack in launch week, until the merge
traffic = egress(60 * 1.5 * 7) * 4 + egress(300 * 1.5 * 7) + egress(150 * 1.5 * 7) * 6
loadtests = 3 * 20 * 2 * 0.04
naive = stack * 168 * 12 * 2 + peaks + shard2 + traffic + loadtests
fixed = stack * 60 * 4 + stack * 168 * 8 + stack * 40 * 12 + peaks + shard2 + traffic + loadtests
print(f"naive {naive:.2f}  fixed {fixed:.2f}  player-driven {peaks + shard2 + traffic:.2f}")
```

It prints:

```
avg CCU 18.8, evening peak 56.2, launch-day peak 112.5
zone servers: normal 2, launch 3
naive 743.50  fixed 448.30  player-driven 133.90
```

### Cross-game recognition

- **Pokémon GO, July 2016.** [MMO302 week 13](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) tells how traffic reached about 50 times the planned baseline. At that scale, player-driven cost is everything and the answer is automatic scaling. The model is the same as yours with `spike` far outside its planned range.
- **New World, 28 September 2021.** Amazon's MMO recorded over 700,000 concurrent players on Steam on launch day, and its servers had trouble handling them. Players waited in login queues ([MMO407 week 2](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md) models them). Even a studio with its own cloud provider budgets for a peak and accepts queues above it.
- **Palworld, January 2024.** Eight million copies in six days is `spike` in its most extreme form, and it shows why no small team budgets for the true worst case. You plan a queue and a player cap for it instead.

The shared lesson is the split into two kinds of cost. One kind follows players, and one follows the clock. A large live game is dominated by the first. A capstone is dominated by the second.

### Eyes-open judgment

Scheduling environments saves money and costs convenience. A closed beta tester who logs in at 2 am to a switched-off server may not come back. That is why the fixed plan schedules production only before open beta, when you control when testers play (week 5 builds on this). From open beta on, production stays up.

A spike reserve is not a plan for a spike. If a streamer brings ten times your forecast, $51.70 buys about 650 extra zone-server hours, but only if someone is awake to start them. Decide now what happens above your fleet's capacity: a login queue, a hard player cap with a friendly message, or both. [MMO407 week 2](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md) gives the queue arithmetic.

Do not cut the budget by dropping staging. A team without staging tests releases on its players, and the ops tax from week 1 rises to pay for it.

## 5. Sprint 3 itself

Sprint 3 has one goal: pass the alpha gate. Plan it against the exit criteria, not the backlog.

- **Order by criterion.** For each line of the alpha checklist that fails today, name the story that makes it pass. Those stories are the sprint. Anything else goes below the line.
- **Integration days.** Merge and deploy to staging at least twice during the sprint, not only at the end. The first full staging deploy always finds configuration problems.
- **Freeze on the last day.** The build that goes to alpha review is tagged on the last working day of week 3. No merges after the tag without instructor approval.

## Studio session plan

Week 3 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Sprint 2 review: done points, measured tax, lab 01 and lab 02 reruns | Updated sheets |
| 0:15-0:35 | Briefing: sections 1 to 3 | |
| 0:35-1:10 | Write the alpha exit criteria; mark each pass or fail on today's build | `alpha-criteria.md` |
| 1:10-1:20 | Break | |
| 1:20-2:00 | Demand and fleet sizing, then the budget by environment (lab 03) | `demand.csv`, `budget.csv` |
| 2:00-2:15 | Run `check_budget.py`; set budget alerts with the provider | `PASS` output, alert screenshot |
| 2:15-2:40 | Instructor round, 5 minutes per team: two alpha criteria and the budget's largest line | Notes on the board |
| 2:40-3:00 | Sprint 3 planning, ordered by failing criteria | Sprint 3 board live |

## Deliverables

Due at the end of the week 3 meeting:

1. **Alpha exit criteria**, 10 to 20 checkable lines, each marked pass or fail on the current build.
2. **Hosting budget** in the lab 03 format ([`labs/lab03.md`](../labs/lab03.md)). The instructor reruns `check_budget.py`. It must print `PASS`.
3. **Capacity plan for spikes**, a short paragraph: player cap per zone server, what players see above it, and who can add a server during launch week.
4. **Budget alerts** set at 50% and 80% of the grant, shown with a screenshot.

Due at the start of week 4: the alpha build tagged, deployed to production from the release pipeline, and joinable from outside the team.

## Common failure modes

- **"Feature complete" with no list.** Every team member has a different idea of done, and the alpha review becomes an argument. Write the criteria this week.
- **Placeholder rules called placeholder art.** A hard-coded drop table is missing logic, not missing polish. It fails the gate.
- **Budgeting for players and forgetting the clock.** The biggest lines are machines left on. Schedule everything that does not need to be up.
- **No staging.** Releases go straight to testers, and every bad build becomes an ops evening.
- **Forgotten bot fleets and test databases.** One weekend of a forgotten load test costs most of the reserve. Make teardown a checklist line.
- **Sizing from the maximum, not the knee.** A server that "held 150 bots" at five-second latency holds 80 players you would want to keep.

## Review checklist

The instructor checks at the end of week 3 and at the start of week 4:

- [ ] Alpha exit criteria are 10 to 20 lines, each checkable by a stranger, covering every feature kept in lab 01.
- [ ] Demand forecast shows DAU, session hours, peak ratio and spike with sources for each.
- [ ] Fleet size uses a measured knee and a stated utilization.
- [ ] Budget lists every environment with its schedule; checker `PASS` against the grant, with a stated reserve.
- [ ] Staging exists and matches production's configuration.
- [ ] Budget alerts are set.
- [ ] A player cap and the over-capacity behavior are written down.
- [ ] At the start of week 4: tagged alpha build on production, joinable from outside.

## Sources

- Wikipedia, "Palworld" (read September 2026). Early access on 19 January 2024; one million copies in eight hours, two million in 24 hours, eight million by day 6; over two million concurrent players on Steam on 24 January and 2,101,867 on 27 January 2024; server issues from the player count.
- Wikipedia, "New World (video game)" (read September 2026; "New World: Aeternum" redirects there). PC release on 28 September 2021; over 700,000 concurrent players on Steam that day; servers had difficulty handling the load.
- Beyer, B. et al. (eds.) (2016). *Site Reliability Engineering*. O'Reilly. Background on capacity planning and headroom; the Pokémon GO figures are taken from MMO302 week 13 and its sources.
- The Emberfall sign-ups, conversion, session length, knee, machine prices, egress price and grant are invented for teaching. Real cloud prices vary by provider, region and date; the lab requires your provider's current prices.
