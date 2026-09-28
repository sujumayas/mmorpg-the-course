# MMO302 · Week 01 — Scale targets: CCU, messages per second, the n-squared problem

**Why this matters:** Every MMO pitch promises "thousands of players in one world." The server team has to turn that sentence into numbers a machine can meet: how many players are online at the peak, how many messages the server must deliver each second, and how many milliseconds one tick may take. This week you learn which of those numbers grows in a straight line and which one grows as a square, and why the square one decides your architecture.

**You will be able to:**
- Compute average and peak concurrent users (CCU and PCU) from daily users, session length and a peak factor, and turn a PCU target into a server count with headroom.
- Compute the message deliveries per second for any split of players into groups with `D = u × Σ g(g − 1)`, and show why the same CCU can cost 5 or 30 times more depending on where players stand.
- Derive the largest crowd one server core can serve, `c_max ≈ √(B / u)`, and explain why doubling the hardware raises it by only 41%.
- Critique a scale target ("10,000 players per realm") by naming the density assumption hidden inside it.

**Before class:** Read CCP Logibro, "Battle for 6VDT-H: summary and numbers" (EVE Online news, 30 July 2013), the whole post. Read CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), from the start through the section on throttling load. Skim the introduction of Epic Games, "Replication Graph" (Unreal Engine documentation). Reread your notes on CS202 week 13.

**Prerequisites from earlier courses:** [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) derived the `n²` bandwidth wall for one match and the tick CPU budget `c(n) = a + d × n + e × n²`. This lecture reuses both and does not re-derive them. [CS202 week 3, topologies](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) (why an MMO is always client-server). [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (reading `O(n)` and `O(n²)` off a loop). [DB201 week 1, why persistence is hard](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) (the save-rate model that also scales with CCU).

**Interactive:** [examples/w01-crowd-cost.html](../examples/w01-crowd-cost.html). Keep it open during section 2.

---

## 1. Four numbers that size a world

A marketing team counts players one way. A server team counts them another way. Get the conversion wrong and you buy ten times too much hardware, or ten times too little.

- **Registered accounts** is everyone who ever made a character. It says nothing about load.
- **Daily active users (DAU)** is how many different accounts log in on one day. Monthly active users (MAU) is the same count over a month.
- **Concurrent users (CCU)** is how many are connected at one instant. This is the number a server feels.
- **Peak concurrent users (PCU)** is the highest CCU in a period, usually a day or a launch week. Servers are sized for the peak, never the average.

Two more numbers turn DAU into CCU. The **average session length** `h` is how many hours an active player spends connected per day. The **peak factor** `k` is PCU divided by average CCU, and it comes from the daily curve. Players log in after work and school, so the evening peak can be well above the daily average.

```
average CCU = DAU × h / 24
PCU         = k × DAU × h / 24
```

Take an invented game with 75,000 DAU, 2 hours of play per active player per day, and a peak factor of 1.6. Average CCU is `75,000 × 2 / 24 = 6,250`. PCU is `1.6 × 6,250 = 10,000`. That 10,000 is the number the rest of this lecture uses.

Real games publish few of these figures, but EVE Online gives two you can compare. CCP set a concurrency record of 63,170 players on its main server, Tranquility, on 23 January 2011. In July 2011 it described Tranquility as hosting over 350,000 subscribers. So at its busiest moment of that year, about `63,170 / 350,000 = 18%` of the paying player base was online at once. On 5 May 2013 the record rose to 65,303. Keep the ratio in mind as a sanity check. If someone plans servers for every registered account, they have bought five or more times too much.

CCU is a count of people. It is not a count of work. Two worlds with the same 10,000 CCU can need very different servers, and the next section shows why.

## 2. Worked example: same crowd size, different bill

### The hook

On 30 July 2013 CCP published the numbers for the battle for the system 6VDT-H. At its height 4,070 pilots were in one star system, a new record. For most of the fight the game ran at one tenth of normal speed, and CCP counted 19,070 seconds of simulation lost to slowdown, about five hours and 18 minutes. Less than three months earlier, on 5 May, the same server cluster had held 65,303 players online at once.

So 65,303 players were fine, and 4,070 players brought one machine to a crawl. The 4,070 were only 6% of the record. The difference is where they stood. The 65,303 were spread over thousands of star systems. The 4,070 were in one.

### The model

Split the players into **groups**. A group is a set of players who all need to hear about each other: a zone, a room, a star system, a crowd around a boss. Group `j` has `g_j` players, and the groups add up to the whole population, `Σ g_j = N`.

- `u` is the number of **state updates** each player produces per second: moves, casts, emotes, equipment changes.
- Each update must be **delivered** to every other player in the same group, which is `g − 1` players.
- A **delivery** is one message written for one recipient. The server serializes it, maybe encrypts it, and queues it for that client's connection.

The deliveries per second for the whole world are:

```
D = u × Σ_j g_j × (g_j − 1)
```

Each player in group `j` produces `u` updates, and each update goes to `g_j − 1` others, so group `j` contributes `u × g_j × (g_j − 1)`.

Two special cases show the shape.

- **Everyone in one group** (`g = N`): `D = u × N × (N − 1)`, which grows as `N²`.
- **Players spread evenly in groups of fixed size `g`**: there are `N / g` groups, so `D = u × N × (g − 1)`, which grows as `N`.

The same formula is linear or quadratic depending on one thing, whether the group sizes stay fixed as the population grows. Total CCU does not decide your load. The size of the biggest group does.

A note on messages and packets. The server usually bundles all the deliveries for one client into one packet per tick. So packets per second grow with `N`, not `N²`. The bytes inside those packets and the CPU work to build them still grow with `Σ g(g − 1)`. CS202 week 13 costed the bytes. This week counts deliveries, because each one costs CPU on the server whatever the packet count.

### Numbers you can check

Build a world to test the formula. It has `N = 10,000` players (the PCU from section 1), `u = 5` updates per second, and 400 zones hosted on 20 servers. Zone `i` lives on server `i mod 20`, so each server hosts 20 zones. At the baseline every zone holds 25 players, so every server holds 500.

Now a crowd forms. A world boss spawns in zone 0 and `c` players gather there. The other `10,000 − c` players spread evenly over the remaining 399 zones. When the division is not exact, the lowest-numbered zones get one extra player each. Server 0 hosts the crowd's zone plus 19 ordinary zones.

Check the baseline by hand. One zone gives `25 × 24 = 600`, and 400 zones give 240,000. Times `u = 5`, the world delivers 1,200,000 messages per second, and each server 60,000.

| Crowd `c` in zone 0 | Players on server 0 | Players on server 1 | Deliveries/s, server 0 | Deliveries/s, server 1 | Deliveries/s, whole world | World vs baseline |
|---|---|---|---|---|---|---|
| 25 (baseline) | 500 | 500 | 60,000 | 60,000 | 1,200,000 | 1.00× |
| 250 | 714 | 489 | 365,610 | 57,360 | 1,454,250 | 1.21× |
| 500 | 953 | 477 | 1,299,250 | 54,510 | 2,331,260 | 1.94× |
| 1,000 | 1,429 | 452 | 5,041,310 | 48,840 | 5,965,530 | 4.97× |
| 2,670 | 3,019 | 368 | 35,661,480 | 32,040 | 36,268,260 | 30.22× |

The crowd's own zone is the easy cell to check. At `c = 1,000`, zone 0 alone delivers `5 × 1,000 × 999 = 4,995,000` messages per second. The other 19 zones on server 0 add about 46,000 more.

Read across the `c = 1,000` row.

- **The world's CCU did not change.** It is 10,000 in every row.
- **Server 0 has about 3 times as many players as server 1** (1,429 against 452).
- **Server 0 does about 103 times as much delivery work as server 1** (5,041,310 against 48,840).

Players are a straight-line cost. Deliveries are a square. That gap is the whole of the n-squared problem, and it is why an MMO server team talks about density far more than about CCU.

### How big a crowd fits on one core?

Suppose one core can do `B` deliveries per second after everything else. For this example assume `B = 1,000,000`, which means one microsecond per delivery. That is an invented round number. Measure your own in the lab. A single crowd of size `c` needs `u × c × (c − 1)` deliveries per second. Set it equal to `B` and solve. For large `c`, `c − 1 ≈ c`, so:

```
c_max ≈ √(B / u)
```

| Budget `B` (deliveries/s) | Updates per player `u` | Largest crowd `c_max` |
|---|---|---|
| 1,000,000 | 5 | 447 |
| 2,000,000 | 5 | 632 |
| 1,000,000 | 1 | 1,000 |
| 1,000,000 | 0.1 | 3,162 |

Doubling the hardware (row 2) raises the crowd limit from 447 to 632, only 41% more, because `√2 = 1.41`. Cutting the update rate by 5 (row 3) raises it by `√5 = 2.24`. Cutting it by 50 (row 4) raises it by `√50 ≈ 7.1`. Under a square law, no amount of money buys a big crowd. You have to change the square.

### The tick view

Servers do their work in ticks. CS202 week 13 split a tick's CPU cost into a fixed part, a per-player part and a per-pair part. Here the per-pair part is the deliveries. Say the zone servers tick at `T = 10` Hz, so a tick may take 100 ms. Use invented costs of 2 ms fixed per tick, 0.05 ms per player per tick, and 0.001 ms (1 µs) per delivery. Deliveries per tick are `D / T`.

```
tick time = 2 + 0.05 × players + 0.001 × deliveries per tick      (ms)
```

- Baseline server: `2 + 0.05 × 500 + 0.001 × 6,000 = 33.0` ms. A third of the budget.
- Server 0 with a crowd of 250: `2 + 0.05 × 714 + 0.001 × 36,561 = 74.3` ms. Tight, but it fits.
- Server 0 with a crowd of 1,000: `2 + 0.05 × 1,429 + 0.001 × 504,131 = 577.6` ms. Almost six ticks' worth of work in every tick.

With these costs, a crowd of 327 still fits in 100 ms and a crowd of 328 does not. At 25 players per zone the per-player cost dominates. In a crowd the per-pair cost swamps everything else.

### Move it yourself

Open `examples/w01-crowd-cost.html`. The top view shows 20 bars, the players on each server. The bottom view shows 20 more bars, the deliveries per second on each server, drawn against a line for one core's budget. Start with the crowd slider at 25. Both views are flat. Drag the crowd to 250 and then to 1,000. In the top view, server 0 grows to about three times its neighbours. In the bottom view, it grows past the top of the chart and you have to switch to the log scale to see the others at all. Then drop the update rate from 5 to 0.5 and watch how much larger a crowd the budget line allows. Same players, two views, one of them a square.

### The same idea in other games

**EVE Online, time dilation (CCP, 2011 to today).** The EVE University wiki says outright that server load grows as `O(n²)` in players on the same grid. CCP's 2011 dev blog explains the fix in our terms. Most of the load in a big fight is tied to the game clock: module cycles, movement, travel, warp-outs. If you slow the clock to 10%, each player produces a tenth as many updates per real second. In our model that is `u → u / 10`, and the crowd one node can carry grows by `√10 ≈ 3.2`. CCP also notes that simply running the physics less often would save only 5 to 10% of the load, because the physics is not where the square lives. Time dilation does not remove the square. It trades game speed for crowd size, which is the only lever left once the hardware is maxed. MMO302 week 12 takes this apart in full.

**Fortnite and Unreal's Replication Graph (Epic Games, current documentation).** Epic's documentation says a Fortnite Battle Royale match starts with 100 connected players and about 50,000 replicated actors. Unreal's default replication asks each replicated actor whether it should update each connected client. Rewrite that in our form. The work per frame is actors × connections, `50,000 × 100 = 5,000,000` relevance checks, before any message is sent. Epic's fix is the Replication Graph, which groups actors by location (grid cells, rooms or zones) so a client is handed the list for its cell. That is exactly "make the groups small and fixed," and week 3 builds it.

**CS202 week 13, the bandwidth wall.** In one 100-player match with no interest cap, server upload is `U ≈ r × b × n²`. That is `D` from this lecture with `u = r`, one group of size `n`, and each delivery costing `b` bytes. The same square, measured in megabits instead of microseconds.

**World of Warcraft Classic, layering (Blizzard, 2019).** When WoW Classic launched on 26 August 2019, Blizzard ran several copies, called layers, of each crowded realm's outdoor world. Players see only players in their own layer. In our model a layer divides one huge group of size `g` into `L` groups of size `g / L`. Deliveries drop from `u × g²` to `u × g² / L`. Week 2 is about that trade and what it costs socially.

Four systems, one expression. Whenever you meet a scaling fix in an MMO, ask which part of `u × Σ g(g − 1)` it attacks. Time dilation cuts `u`. Interest management and layering cut `g`. Faster hardware only raises `B`, and that buys a square root.

### Design judgment

- **Size for the densest moment your design invites, not for CCU.** A world boss, a capital city, a launch-day starting zone and a siege are all design decisions. Each one sets a `g`. If your design says "the whole server fights over one castle," you have chosen `g = N` and signed up for the square.
- **Know which lever you are pulling.** Faster hardware buys `√2` per doubling. Halving `u` buys `√2` too, for free, if players will not notice. Splitting crowds by space (interest management, week 3) or by copies (layers, week 2) changes the exponent. That is the only lever that scales.
- **Density limits are design rules as much as server rules.** A hard cap on players per zone is the bluntest fix, and players feel it as a queue or a wall. A soft fix, such as slowing time or thinning updates for distant players, keeps everyone in but degrades their experience. Choose which failure you prefer before launch, because under load you will get one of them.
- **Budget from the tick, backwards.** Write down the tick length, subtract the fixed and per-player costs at your planned zone population, and what is left is `B` for the crowd. If the remainder is small, your world cannot host big events, and your design team should know that now.

### Check this example

1. In the model world, a crowd of 600 forms in zone 0 and the other 9,400 players stay spread over 399 zones. Estimate zone 0's deliveries per second. Is it more or less than one core's budget of 1,000,000?
2. A designer wants a 2,000-player siege on one server core. With `B = 1,000,000`, what update rate `u` would that require? Is it playable?
3. Two worlds each have 10,000 CCU. World A has 100 zones of 100 players. World B has 400 zones of 25 players. Compute `D` for each with `u = 5`. What is the ratio?

<details>
<summary>Answers</summary>

1. `5 × 600 × 599 = 1,797,000` deliveries per second, about 1.8 times one core's budget. The crowd needs a fix even before the other zones on the server are counted.
2. `u = B / (c × (c − 1)) = 1,000,000 / (2,000 × 1,999) ≈ 0.25` updates per second, one update every 4 seconds per player. That is one twentieth of the model's `u = 5`, the same as running the clock at 5% speed, which is slower than EVE's 10% time-dilation floor. It may be tolerable for slow fleet warfare and not for action combat.
3. A: `5 × 100 × (100 × 99) = 4,950,000`. B: `5 × 400 × (25 × 24) = 1,200,000`. A costs 4.125 times as much for the same CCU, which is `99 / 24`. With fixed group sizes, `D` is linear in `N` and proportional to `g − 1`.

</details>

## 3. From a PCU target to a machine count

Section 2 showed that density drives load. You still have to buy machines for the ordinary case. The usual planning chain has four links.

1. **PCU** from section 1: 10,000.
2. **Cost per player at normal density.** With the tick costs above and 25 players per zone, each player adds 0.05 ms of simulation plus `24 × 5 / 10 = 12` deliveries per tick at 0.001 ms each. That is 0.062 ms per player per tick.
3. **Target utilization** `U`, the fraction of the tick you allow ordinary play to use. The rest is headroom for crowds, spikes and slow machines.
4. **Players per server** is `P = (U × 100 − 2) / 0.062`, and the server count is `ceil(PCU / P)` plus spares.

| Target utilization | Players per server | Servers for 10,000 PCU | Spare for one failure | Total |
|---|---|---|---|---|
| 80% | 1,258 | 8 | 1 | 9 |
| 50% | 774 | 13 | 1 | 14 |
| 33% | 500 | 20 | 1 | 21 |

The model world in section 2 runs at 33% utilization, 500 players per server. That looks wasteful until you remember that a crowd of 327 fills a whole tick. The headroom is there for the crowd, not for the average. A team that plans at 80% utilization gets 9 servers and a world where any gathering over about 150 players overruns the tick.

The spare column is the simplest failure plan. If one machine in 20 dies, its zones must move somewhere, and the survivors must have room for them. With `S` servers each at utilization `U`, losing one server raises each survivor to `U × S / (S − 1)`. At 20 servers and 33%, the survivors go to 34.7%, which is harmless. At 8 servers and 80%, they go to 91%, and any crowd tips them over. Week 4 covers moving zones between servers, and week 13 covers adding servers automatically.

A third number to plan for is the **login storm**. After maintenance, most of the PCU tries to log in within a few minutes. If 10,000 players reconnect over 5 minutes, that is 33 logins per second. Each login loads a character from the database ([DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) sizes those reads). Login is linear in `N`, but it is a spike, and week 9 builds the queue that absorbs it.

## 4. Where else the square hides

Position updates are the obvious `g²`. Any feature that tells everyone in a group about everyone else has the same shape. Look for it in:

- **Chat channels.** One message in a channel of `g` members costs `g − 1` deliveries. If every member talks at rate `u`, the channel costs `u × g × (g − 1)`. A 5,000-member global trade channel where each player posts once every 10 minutes (`u = 1/600`) costs `5,000 × 4,999 / 600 ≈ 41,658` deliveries per second, from one text box. Week 10 designs chat services around this.
- **Guild and friends presence.** When a player logs in, every online guildmate is told. A guild of 500 whose members log in and out a few times an evening generates a burst of deliveries each time.
- **Area effects.** A spell that hits every enemy in range and reports each hit to every onlooker costs targets × onlookers. In a 200-versus-200 fight a single area spell can create tens of thousands of combat-log deliveries.
- **Collision and targeting checks.** Checking every pair for "can A see B" or "does A collide with B" is `g²` CPU even when nothing is sent. Week 3's grid removes most of those checks.

For each one, ask the same question as in section 2. What is `g`, and does it stay fixed as the game grows?

## In-class activity (25 minutes)

Groups of three. Each group gets a design card with a scale target.

- Card A: "A fantasy MMO with 8,000 PCU per realm, a capital city, and weekly world bosses."
- Card B: "A survival MMO with 2,000 PCU per server, where every guild fights over one castle on Saturdays."
- Card C: "A space MMO with 20,000 PCU on one shard, with player-run trade hubs."

1. Name the three densest places or moments your card's design creates, and estimate `g` for each.
2. With `u = 5` and `B = 1,000,000`, compute the deliveries per second for your densest group and how many cores it needs.
3. Choose one lever for each dense spot (lower `u`, split `g` in space, split `g` by copies, cap `g`) and say what the player will notice.
4. Present your worst group and your fix in one minute. The other groups challenge the estimate of `g`.

Expected output: a table with three rows (place, `g`, deliveries per second, cores, fix, what players notice) and one sentence naming the fix you are least happy with.

## Common misconceptions

- **"CCU is the load."** CCU is a count of people. Load depends on `Σ g(g − 1)`, which depends on how people cluster. Two worlds with the same CCU can differ by a factor of 30.
- **"Buy a bigger server and the crowd fits."** Under a square law, doubling capacity raises the crowd limit by 41%. The only scalable fixes change `g` or `u`.
- **"Packets per second is what grows as `n²`."** With one bundled packet per client per tick, packets grow as `n`. The deliveries inside those packets, their bytes and the CPU that builds them grow as the square.
- **"Headroom is waste."** Headroom is capacity reserved for crowds and failures. A server at 80% average utilization overruns its tick at the first gathering.

## Check yourself

1. A game has 200,000 DAU, players average 1.5 hours a day, and the peak factor is 1.8. What is the PCU?
2. A zone holds 60 players who each send 4 updates per second. How many deliveries per second does the zone need? What if the zone doubles to 120 players?
3. At `B = 1,000,000` deliveries per second and `u = 2`, what is the largest crowd one core can serve? How large a budget would a 1,500-player crowd need?
4. Using the tick model of section 2 (2 ms fixed, 0.05 ms per player, 0.001 ms per delivery, 10 Hz), what is the tick time for a server of 400 players spread in zones of 20 with `u = 5`?
5. Why does time dilation at 10% speed let EVE serve a crowd about 3.2 times larger, rather than 10 times larger?

<details>
<summary>Answers</summary>

1. Average CCU `= 200,000 × 1.5 / 24 = 12,500`. PCU `= 1.8 × 12,500 = 22,500`.
2. `4 × 60 × 59 = 14,160` deliveries per second. At 120 players, `4 × 120 × 119 = 57,120`, about 4.03 times as much for twice the players.
3. `c_max ≈ √(1,000,000 / 2) ≈ 707`. A 1,500-player crowd needs `2 × 1,500 × 1,499 = 4,497,000` deliveries per second, about 4.5 cores' worth.
4. Each zone gives `20 × 19 = 380`, and there are 20 zones, so `D = 5 × 20 × 380 = 38,000` per second, which is 3,800 per tick. Tick time `= 2 + 0.05 × 400 + 0.001 × 3,800 = 25.8` ms.
5. Time dilation divides `u` by 10. The crowd limit is `√(B / u)`, so it grows by `√10 ≈ 3.16`, not by 10.

</details>

## Lab / assignment hook

[Lab 01, the crowd cost model](../labs/lab01.md). You implement `D = u × Σ g(g − 1)` and the zone-and-server layout from section 2 in Python, reproduce the table, measure your own machine's cost per delivery, and find the crowd that breaks a 100 ms tick on your hardware. Deliverable: the finished `crowd_cost.py`, a CSV sweep of crowd size, one plot, and a half-page capacity plan for one of the in-class cards.

## Sources

- CCP Logibro, "Battle for 6VDT-H: summary and numbers" (EVE Online news, 30 July 2013), eveonline.com/article/battle-for-6vdt-h. Peak of 4,070 players in one system, time at 1/10 speed for most of the battle, 19,070 seconds of simulation lost, previous record of 3,615 in P-2TTL (2010).
- CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), eveonline.com/news/view/introducing-time-dilation-tidi. Most fight load tied to the game clock, slowing the clock lowers load in proportion, physics at a lower rate would save only 5 to 10%.
- Wikipedia, "Eve Online" (accessed September 2026), citing CCP forum and press posts. Concurrency record of 65,303 on 5 May 2013, previous record 63,170 on 23 January 2011, Tranquility described in July 2011 as hosting over 350,000 subscribers.
- EVE University Wiki, "Time dilation" and "Server tick" (accessed September 2026). Server load `O(n²)` in players on grid, time dilation down to 10% speed, one server tick per second.
- Epic Games, "Replication Graph" (Unreal Engine documentation, current as of September 2026), dev.epicgames.com. Fortnite Battle Royale starts with 100 players and about 50,000 replicated actors, the per-actor-per-connection cost of default replication, grid cells and rooms as the fix.
- Warcraft Wiki, "Layering" (accessed September 2026), and Wikipedia, "World of Warcraft Classic" (accessed September 2026). WoW Classic released 26 August 2019; each layer is a copy of the outdoor world and players see only their own layer.
- Alexander, T. (ed.) (2003). *Massively Multiplayer Game Development*. Charles River Media. Course reading for the server architecture weeks.

## Interactive spec: examples/w01-crowd-cost.html

**The one insight.** The same 10,000 players cost a flat, even load when spread out, and one server's load explodes as a square when they crowd into one zone. The player-count view stays tame (server 0 about 3 times its neighbours at `c = 1,000`) while the delivery view goes off the chart (about 103 times).

**Model (exact).**
- Inputs: `N` total players (default 10,000, range 1,000 to 20,000, step 500), `c` crowd in zone 0 (default 25, range 0 to 4,100, step 1, clamp to `N`, so the 4,070 preset fits), `u` updates per player per second (default 5, options 0.1, 0.5, 1, 2, 5, 10), `B` core budget in deliveries per second (default 1,000,000, options 500,000, 1,000,000, 2,000,000, 4,000,000).
- Fixed: `Z = 400` zones, `S = 20` servers, zone `i` on server `i mod 20`.
- Populations: `pop[0] = c`. Let `rest = N − c`, `q = floor(rest / 399)`, `r = rest mod 399`. For `i = 1 … 399`, `pop[i] = q + (1 if i − 1 < r else 0)`.
- Per zone deliveries: `d[i] = u × pop[i] × (pop[i] − 1)`.
- Per server: `players[s] = Σ pop[i]` over `i mod 20 = s`; `deliveries[s] = Σ d[i]` likewise.
- World total `D = Σ d[i]`. Baseline `D0` is the same computation with `c = N / 400` (i.e. even spread), used for the "world vs baseline" readout.
- Cores needed on server 0: `deliveries[0] / B`.
- Largest crowd one core can serve: `c_max = floor((1 + √(1 + 4B/u)) / 2)`.

**Layout.** Two stacked bar charts sharing the x-axis (servers 0 to 19). Top: players per server, linear axis. Bottom: deliveries per second per server with a horizontal dashed line at `B`, labelled "one core". The bottom chart has a linear/log toggle; in linear mode the axis is fixed at 2 × B so server 0 visibly clips past the top with an arrow and its value printed. Server 0's bars use the accent colour, the other 19 a neutral. Below the charts, a readout row: world CCU (always `N`), world deliveries/s, ratio to baseline, server 0 players ÷ server 1 players, server 0 deliveries ÷ server 1 deliveries, cores needed on server 0, `c_max`.

**Controls.** Sliders for `N` and `c` with number inputs beside them; segmented buttons for `u` and `B`; preset buttons "Spread (25)", "World boss (250)", "Big event (1,000)", "6VDT-H scale (4,070)". All keyboard operable; values update on input.

**First screen.** Load with `c = 1,000` (not the baseline), linear scale, so the clipped server 0 bar and the "×103" ratio are the first thing seen.

**Test values** (N = 10,000, u = 5):
- `c = 25`: server 0 players 500, deliveries 60,000; server 1 players 500, deliveries 60,000; world 1,200,000.
- `c = 250`: server 0 714 / 365,610; server 1 489 / 57,360; world 1,454,250 (1.21×).
- `c = 500`: server 0 953 / 1,299,250; server 1 477 / 54,510; world 2,331,260 (1.94×).
- `c = 1,000`: server 0 1,429 / 5,041,310; server 1 452 / 48,840; world 5,965,530 (4.97×); ratios 3.2× players, 103.2× deliveries.
- `c = 2,670`: server 0 3,019 / 35,661,480; server 1 368 / 32,040; world 36,268,260 (30.22×).
- `c_max`: B = 1,000,000 and u = 5 gives 447; u = 1 gives 1,000; u = 0.1 gives 3,162; B = 2,000,000 and u = 5 gives 632.

**Accessibility and style.** Use the shared tokens from `templates/interactive-tokens.css`. Bars get `aria-label`s with exact values; the readout row is an `aria-live="polite"` region. No game art; label the preset "6VDT-H scale" in text only.
