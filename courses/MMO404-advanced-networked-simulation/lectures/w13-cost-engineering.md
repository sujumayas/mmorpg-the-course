# MMO404 · Week 13 — Cost engineering

**Why this matters:** Every technique in this course costs money to run, and the bill arrives every month for as long as the game lives. Teams routinely spend weeks making the server faster and then find the bill barely moved, because the money was going somewhere else. This week you learn to price one player-hour, split it into the terms that make it up, and pick the lever that moves the biggest term.

**You will be able to:**
- Compute the cost of 1,000 player-hours from server price, zone capacity, fill, bytes per client and egress price, and state each term's share.
- Predict the most a lever can save from its term's share, and explain why a 3× faster server saves only a few percent in a bandwidth-heavy MMO.
- Compute the fill limit that cheap interruptible capacity imposes, `u ≤ 1 − q x`, and decide whether it pays.
- Critique a cost-reduction proposal by naming which term it attacks and what players pay for it.

**Before class:** Brent Randall, "VALORANT's 128-Tick Servers" (Riot Games technology blog, 31 August 2020), the whole post. Roblox, "Roblox Return to Service 10/28-10/31 2021" (Roblox newsroom, January 2022), the introduction and the section on why Roblox runs its own infrastructure. Amazon Web Services, "Spot Instance interruption notices" (Amazon EC2 User Guide, current).

**Prerequisites from earlier courses:** [MMO302 week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (on-demand and committed prices, headroom, why the fleet runs below full; this lecture does not repeat them). [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (the metrics you need to meter the bill). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md). In this course, [week 1](w01-limits-of-the-zone-model.md) (the tick-cost model and zone capacity), [week 2](w02-seamless-worlds-and-boundary-handoff.md) (handoff), [week 4](w04-replication-prioritization-and-relevancy.md) and [week 5](w05-bandwidth-shaping-and-lod-for-networking.md) (bytes per client and the shaper).

**Interactive:** [w13-player-hour-cost.html](../examples/w13-player-hour-cost.html). Keep it open during section 2.

---

## 1. The unit you pay for

A studio does not pay per player. It pays per server-hour, per gigabyte leaving the data centre, per database operation and per stored byte. Players arrive, stay a while and leave. To connect the two, you need one unit that both sides understand.

The unit in this lecture is the **player-hour**: one player connected for one hour. A game that averages 20,000 players online (20,000 **CCU**, concurrent users) for a whole day uses 480,000 player-hours. One CCU held for a month is about 730 player-hours. Every cost below is expressed in dollars per 1,000 player-hours, because the numbers are then small enough to read without scientific notation.

The bill for a player-hour has three parts.

- **Compute.** The servers that run the simulation. You rent them by the hour whether they are full or not. So the compute cost of one player-hour is the server price divided by the number of players the server actually holds.
- **Network egress.** Bytes sent from your servers to players' machines. Cloud providers charge for data leaving their network by the gigabyte, and they usually charge little or nothing for data arriving. In an MMO nearly all your traffic is outbound, because the server tells each client about many entities and each client sends back only its own inputs.
- **Shared services.** The login gateway, the database, chat, guilds, the market, logs and metrics (MMO302 weeks 7 to 10 and 14). They scale roughly with the number of players, not with where the players stand. We fold them into one number per player-hour.

Two terms from earlier weeks do most of the work. **Zone capacity** `N` is the number of players one zone process can hold inside its tick budget. Week 1 computed it from the tick-cost model: 938 players when a tenth of them crowd together. **Fill** `u` is the average share of that capacity actually in use across the fleet. MMO302 week 13 showed why fill must stay well below 100%. New servers take minutes to start, so you hold headroom for the ramp, and a fleet that autoscales still spends much of the day half empty.

## 2. Worked example: where a player-hour's money goes

### The hook

In 2020, Riot Games launched VALORANT, a 5-versus-5 shooter, with 128-tick servers. The first build of the server took about 50 ms to simulate one frame. At 128 ticks per second, a frame lasts only 7.8125 ms. Riot's engineers set themselves a target of three games per CPU core, which left 2.6 ms per frame, and after keeping 10% for the operating system they aimed for 2.34 ms. They got the frame time below 2 ms with code optimization, hardware changes and operating-system tuning. On a 36-core host, that meant 108 games or 1,080 players.

Riot's reason is stated plainly in the post. One full core per game would have made hosting at scale too expensive to offer 128-tick servers to every player for free. So the whole optimization project was cost engineering. It changed how many players one core holds.

Here is the puzzle for you. Suppose you run an MMO and your lead engineer proposes the same project: make the zone server three times faster. Will the bill fall by two thirds, as it would have for Riot at one game per core? For the MMO in this lecture, it falls by 2.4%. The model below shows why, and what to do instead.

### The model

The cost of 1,000 player-hours, in dollars, is the sum of three terms:

```
K = K_cpu + K_net + K_svc

K_cpu = 1000 × P_s / (Z × N × u)
K_net = 1000 × b × 3600 / 10⁹ × P_e
K_svc = a fixed number per 1,000 player-hours
```

- `P_s` is the price of one server-hour. We use $0.40, the invented on-demand price from MMO302 week 13.
- `Z` is the number of zone processes one server runs. Our server has 8 cores and runs one zone per core, so `Z = 8`.
- `N` is one zone's capacity from week 1, at the density you plan for. At a hot-spot share `h = 0.1`, `N = 938`.
- `u` is the average fill. We use 0.5, a fleet that autoscales but keeps headroom.
- `b` is the bytes per second sent to each client. We use 6,000 B/s (48 kbit/s), close to the error-driven stream of week 5's quiet hub.
- `P_e` is the egress price per gigabyte. We use $0.08.
- `K_svc` covers the shared services. We use $0.25 per 1,000 player-hours.

All prices here are invented round numbers. Real prices vary by provider, region, volume discount and year, and you should always use your own. For scale, Amazon's published list price for data sent from its us-east-1 region to the internet in September 2026 was $0.09 per GB for the first 10 TB a month, falling in steps to $0.05 per GB above 150 TB, before any negotiated discount. Our $0.08 sits inside that range. What carries over is the structure of the formula.

Look at what each term depends on. `K_cpu` falls as `N` and `u` rise, so it rewards density and packing. `K_net` does not depend on `N` or `u` at all. Every player you add brings their own bytes. No amount of packing players onto fewer servers makes a byte cheaper.

One more rule turns the model into a decision tool. If a lever makes term `i` cheaper by a factor `s`, the total falls by

```
saving = share_i × (1 − 1/s)
```

where `share_i = K_i / K`. The share is a hard ceiling. A term that is 5% of the bill can never save more than 5%, even if you make it free. This is Amdahl's law from parallel computing, applied to money.

### Numbers you can check

The baseline comes out to about $2.09 per 1,000 player-hours. The three terms are far from equal:

| Term | How it is computed | $ per 1,000 player-hours | Share |
|---|---|---|---|
| Compute | `1000 × 0.40 / (8 × 937.5 × 0.5)` | 0.107 | 5.1% |
| Network | `1000 × 6000 × 3600 / 10⁹ × 0.08` | 1.728 | 82.9% |
| Services | invented | 0.250 | 12.0% |
| Total | | 2.085 | 100% |

Check the network row by hand. One player receives 6,000 bytes per second, so in an hour they receive 21.6 million bytes, which is 0.0216 GB. At $0.08 per GB that is $0.001728 per player-hour, or $1.728 per 1,000. One CCU for a month costs about `2.085 × 730 / 1000 = $1.52`.

Now try four levers, one at a time:

| Lever | What changes | New total | Saving |
|---|---|---|---|
| Server code 3× faster | `N` rises from 938 to 1,792 | 2.034 | 2.4% |
| Better packing | `u` rises from 0.5 to 0.7 | 2.054 | 1.5% |
| Network LOD | `b` falls from 6,000 to 4,000 B/s | 1.509 | 27.6% |
| Negotiated egress | `P_e` falls from $0.08 to $0.06 | 1.653 | 20.7% |

Three things stand out.

- **The famous lever barely moves the bill.** Making the code three times faster does not even triple capacity, because of week 1's square-root law. At `h = 0.1` a 3× faster server holds 1.91 times the players. The compute term drops from $0.107 to $0.056, and the total drops by 2.4%. The share rule predicted this before any code was written. Compute is 5.1% of the bill, so even free compute saves at most 5.1%.
- **A third fewer bytes saves more than a quarter.** Network LOD from week 5 attacks the 83% term. Removing a third of it saves `0.829 × 1/3 = 27.6%`, exactly as the share rule says.
- **The procurement meeting beats the packing project.** A 25% cut in the egress price is a contract negotiation, not an engineering project, and it saves 20.7%. Better packing, which takes real work in the autoscaler and the matchmaker, saves 1.5%.

Here is the model as code. It is the core of Lab 13.

```python
import math

C_P, C_I, BUDGET = 20e-6, 2e-6, 0.050      # week 1 tick model
F = math.pi * 100**2 / 2000**2

def zone_capacity(h, speedup=1.0):
    a, b = C_I / speedup * (h * h + (1 - h * h) * F), C_P / speedup
    return (-b + math.sqrt(b * b + 4 * a * BUDGET)) / (2 * a)

def cost_per_1000(h=0.1, speedup=1.0, fill=0.5, zones=8, server_price=0.40,
                  bytes_per_s=6000, egress_per_gb=0.08, services=0.25):
    """Dollars per 1,000 player-hours: (compute, network, services)."""
    players = zones * zone_capacity(h, speedup) * fill
    compute = 1000 * server_price / players
    network = 1000 * bytes_per_s * 3600 / 1e9 * egress_per_gb
    return compute, network, services

base = cost_per_1000()
total = sum(base)
print(f"baseline  compute {base[0]:.3f}  network {base[1]:.3f}  services {base[2]:.3f}"
      f"  total {total:.3f}")
levers = {
    "code 3x faster":        dict(speedup=3.0),
    "fill 50% -> 70%":       dict(fill=0.7),
    "bytes 6,000 -> 4,000":  dict(bytes_per_s=4000),
    "egress price -25%":     dict(egress_per_gb=0.06),
}
for name, kw in levers.items():
    new = sum(cost_per_1000(**kw))
    print(f"{name:22s} total {new:.3f}  saves {100 * (1 - new / total):4.1f}%")
```

It prints:

```
baseline  compute 0.107  network 1.728  services 0.250  total 2.085
code 3x faster         total 2.034  saves  2.4%
fill 50% -> 70%        total 2.054  saves  1.5%
bytes 6,000 -> 4,000   total 1.509  saves 27.6%
egress price -25%      total 1.653  saves 20.7%
```

### Why Riot's lever was worth pulling

The same model explains why Riot's project paid off. Put VALORANT's published density into our form, with an invented host price of $1.80 per hour for 36 cores ($0.05 per core-hour, the same rate as our 8-core $0.40 server). At three games per core, 1,080 players share the host, and compute costs `1000 × 1.80 / 1080 = $1.67` per 1,000 player-hours. At one game per core, 360 players share it, and compute costs $5.00.

We do not know VALORANT's bytes per client, so assume, only to compare, the same 6,000 B/s as our MMO. Then at one game per core, compute is `5.00 / (5.00 + 1.73) = 74%` of the bill, and tripling the density saves about half of the whole bill. The difference from our MMO is the tick rate. At 128 ticks per second, every player costs about 13 times as many simulation steps per hour as at 10 per second, so compute is the big term. At 10 ticks per second, with many entities to tell each client about, bytes are.

Neither game is wrong. The lesson is that the same engineering project can be worth half the bill in one game and 2% in another. You find out which by computing the shares first.

### Move it yourself

Open `examples/w13-player-hour-cost.html`. The left view is one stacked bar for the cost of 1,000 player-hours, split into compute, network and services. The right view shows a row of lever bars: for each lever, the saving it achieves right now, drawn on top of a faint bar for its ceiling (the share of its term). Start at the baseline. Drag "server code speed-up" from 1× to 10×. The compute slice shrinks to almost nothing, and the lever bar crawls toward its 5.1% ceiling and stops there. Now drag "bytes per client" from 6,000 to 3,000. The whole left bar shrinks by 41%. Then reset and raise the tick rate slider from 10 to 128 Hz. Zone capacity falls from 938 to 154, and the compute slice grows from 5% to a quarter of the bill. Now drag bytes per client down to 1,500 B/s, a lean shooter-like stream, and compute becomes the largest term. The ranking of the levers flips. The left view shows what you pay. The right view shows what you can still win, and it is rarely where the engineering effort wants to go.

### Same idea elsewhere

Each of these organizations pulled a lever on one term of `K`. Naming the term is the skill.

**VALORANT (Riot Games, August 2020).** Riot's games per core is `Z × N` in our compute term, with `Z = 36` cores and `N = 30` players per core. Riot attacked `N` with engineering because, at 128 ticks per second, compute was the term that mattered, as the previous subsection showed.

**Roblox (on-premises infrastructure, described in the January 2022 postmortem of the October 2021 outage).** Roblox writes that it builds and manages its own infrastructure, over 18,000 servers at the time, because at its scale that is the best way to support the business. It gives two reasons, cost and control over latency, and says the savings affect how much it can pay creators. It uses public cloud for burst capacity, DevOps and most analytics. In our model, owning hardware lowers `P_s` for the base of the fleet, and the cloud covers the peak. That is MMO302 week 13's committed base plus on-demand peak, with the committed part replaced by hardware Roblox owns. The price is that Roblox must run its own data centres and absorb the risk of a long outage itself, as the 73-hour outage of October 2021 showed.

**Amazon EC2 Spot Instances (current documentation, 2026).** A cloud provider sells spare capacity at up to a 90% discount against on-demand, on the condition that it can take the machine back. The interruption notice arrives two minutes before the machine stops. In our model, spot lowers `P_s` for part of the fleet. Section 4 shows the price. You must be able to move every player off a machine in under two minutes, and the rest of the fleet must have seats for them.

**EVE Online (time dilation, since 2011).** Time dilation slows the game clock on an overloaded node, down to 10% speed, instead of refusing players or buying a bigger machine (week 1). In our model it raises the effective budget of a node for the few hours a battle lasts, so `N` rises without any change to `P_s`. It is a cost decision as much as a design one. CCP does not have to provision every node for the largest fight the players might ever start. The players pay in time instead.

Four organizations, one bill. When you meet a new cost story, ask which term it changed: the price of an hour, the players per hour of hardware, the bytes per player, or the shared services.

### Design judgment

- **Compute the shares before you start a cost project.** The share of a term is the most you can win by attacking it. A two-week estimate on a lever with a 5% ceiling should be compared with the same two weeks spent on a lever with an 80% ceiling.
- **Tick rate decides which term is big.** High-rate games (shooters, fighting games) pay mostly for compute. Low-rate, entity-heavy games (most MMOs) pay mostly for bytes. When a design change raises the tick rate or widens the area of interest, reprice the bill.
- **Some levers are contracts, not code.** Egress price, committed discounts and owning hardware are business decisions. Put them in front of producers with the same share arithmetic you use for engineering levers.
- **Every lever has a player price.** Fewer bytes mean coarser far entities (week 5). Higher fill means less headroom for a sudden crowd (MMO302 week 13). Spot capacity means evacuations. Name the player price next to the dollar saving, or someone else will name it after launch.

## 3. The crowd changes the bill

The baseline assumed a planning density of `h = 0.1`. A crowd changes two terms at once.

First, capacity falls. Week 1 showed that a zone holds 938 players at `h = 0.1` and 531 at `h = 0.25`. If fill stays the same, the compute term rises by the same factor, from $0.107 to $0.188.

Second, bytes rise. More entities are in each client's area of interest, and they move more. Week 5 showed an error-driven stream growing by a factor of 20 between a quiet crowd and a panic. Without a limit, the network term follows it.

This is where week 5's shaper becomes a cost tool. A token bucket with rate `ρ` caps each client's average at `ρ` bytes per second, whatever the crowd does. With `ρ = 12,000` B/s, the rate week 5 used, the worst crowded player-hour costs:

| Case | Compute | Network | Services | Total |
|---|---|---|---|---|
| Planning density, `h = 0.1`, 6,000 B/s | 0.107 | 1.728 | 0.250 | 2.085 |
| Crowd, `h = 0.25`, same bytes | 0.188 | 1.728 | 0.250 | 2.166 |
| Crowd, `h = 0.25`, bytes at the shaper cap 12,000 B/s | 0.188 | 3.456 | 0.250 | 3.894 |

The crowd's CPU cost barely shows on the bill. Its bytes nearly double it. Without the shaper, there is no upper row at all, because nothing bounds `b`. A shaper therefore does two jobs. It protects the player's link from bursts, which is why week 5 introduced it, and it puts a ceiling on the cost of the worst hour, which is what the finance team will ask you for.

Crowds are also short. If a world boss draws a crowd for one hour a day in one zone out of forty, it adds very little to the monthly bill. Price the typical hour for the budget and the worst hour for the ceiling, and keep the two numbers apart. A team that prices every hour at the worst case buys hardware it does not need. A team that prices only the average has no answer when the event runs every evening for a month.

## 4. Cheap capacity you can lose

Interruptible capacity such as EC2 Spot is the largest discount on compute that a cloud offers. Section 2 already tells you the most it can save in our MMO. Compute is 5.1% of the bill, so even a 70% discount on the whole fleet saves at most `0.051 × 0.7 = 3.6%`. For a shooter where compute is 74% of the bill, the same discount is worth half the bill. So first decide whether the lever is worth having. If it is, this section tells you what it costs to hold.

### Evacuation in two minutes

When the provider reclaims a spot server, every player on it must move to another server before it stops. You get a two-minute notice, and AWS recommends checking for it every 5 seconds, so plan on about 115 seconds of usable time.

Moving a player between servers is week 2's handoff. Between servers in one data centre, one handoff is a message each way and a few milliseconds of processing. One of our servers holds `8 × 938 × 0.5 = 3,750` players. At 5 ms of processing per handoff on the receiving side, and 8 zones evacuating in parallel, the evacuation takes `3,750 / 8 × 5 ms = 2.3 s`. Time is not the problem, provided your handoff really is the exactly-once protocol of week 2 and you have tested it under load. A handoff with a one-in-a-million duplication bug, run 3,750 times per evacuation, will duplicate something every few hundred evacuations.

### Seats for the evacuees

The real limit is room. Spot interruptions tend to come in groups, because the provider reclaims capacity from a pool, not from one machine at random. Suppose a share `x` of your fleet runs on spot, and in the worst case the provider reclaims a share `q` of those servers at once. After the reclaim, the fleet has `(1 − q x)` of its servers left, and they must hold every player. So the fill must satisfy

```
u ≤ 1 − q x
```

With `x = 0.6` and `q = 0.25`, the fill limit is 85%. Our fleet already runs at 50% fill for autoscaling headroom, so spot costs nothing extra in seats. A team that had pushed fill to 90% to save money would find spot forces it back down to 85%. The two cheap levers compete for the same headroom.

Put numbers on it. With 60% of the fleet on spot at a 70% discount, the average price of a server-hour falls to `0.40 × (1 − 0.6 × 0.7) = $0.232`. At 50% fill, the compute term falls from $0.107 to $0.062, and the total from $2.085 to $2.040, a 2.2% saving. At 85% fill without spot, compute would cost $0.063. Spot and packing buy about the same saving here, and neither is large, because compute is a small share. That is the share rule again.

### Where spot fits an MMO

Not every server is equally easy to move. Stateless or nearly stateless processes, such as login front ends, chat relays, AI workers from [week 12](w12-ai-at-scale.md), or bot load generators from [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md), can be reclaimed with almost no player effect. A zone server in the middle of a raid boss fight is the worst candidate. The evacuation interrupts the fight for every player at once, even if nobody is disconnected. A sensible plan puts spot under the processes that are cheap to move, keeps the zone servers on committed or owned hardware, and measures whether the saving is worth the engineering.

## 5. Metering the bill

The model in section 2 used invented constants. In a live game you measure them, and the measurement is most of the work.

**Compute per player-hour.** Every zone process already reports its tick time (MMO302 week 14). Add its player count to the same metric, and you can compute CPU-seconds per player-hour for each zone, each hour. Zones with a high number are either crowded, which week 1 predicts, or running an expensive feature. Group the metric by zone type and by event, and the expensive feature shows up.

**Bytes per player-hour.** Count bytes per client at the send path, broken down by entity class and by message type. Week 4's priority classes are the natural labels. The breakdown tells you which class to put on a diet. In many MMOs, a few chatty classes (other players' movement, combat log messages, cosmetic effects) carry most of the bytes.

**Services per player-hour.** Database writes per player-hour, login calls per session and log volume per player-hour. MMO302 week 14 warned that logs and metrics have their own bill. Watch that the metering you just added does not become a large new term itself.

**Cost per feature.** Once you have the three meters, you can price a feature. A new area-of-effect spell that makes every cast replicate 40 particles to 200 clients adds a known number of bytes per cast. Multiply by casts per hour and by `P_e`, and the design discussion gets a dollar figure, not a vague worry.

Metering has one trap. The cheapest hour to measure is the average, and the average hides the crowd, as week 1 warned. Store the distribution per zone and per hour, not one fleet total.

## In-class activity (25 minutes)

In groups of three, you are the server team for a new free-to-play MMO. Your producer has one engineer for six weeks and three proposals on the table.

- A. Rewrite the combat system to make the zone server 2× faster.
- B. Add distance-based field LOD so far entities send only position, cutting bytes per client from 7,000 to 5,000 B/s.
- C. Move the login, chat and AI worker processes to spot capacity. Today they are 40% of the services cost.

Use the model with `P_s = $0.40`, `Z = 8`, `h = 0.1`, `u = 0.5`, `P_e = $0.07`, `K_svc = $0.30`, and assume spot gives a 70% discount.

1. Compute the baseline cost per 1,000 player-hours and each term's share. (8 min)
2. Compute the saving of each proposal. For A, use `zone_capacity(0.1, 2.0)` from the code above. (10 min)
3. Rank the proposals and write, for the top one, two sentences a producer would accept: the dollar saving per 100,000 CCU-months and the player-facing price. (7 min)

Expected output: a baseline of about $2.17 with network near 81%, savings of roughly 1.7% for A, 23.2% for B and 3.9% for C, and a recommendation for B that names coarser far entities as the price.

## Common misconceptions

- **"A faster server cuts the hosting bill in proportion."** Only if compute is most of the bill, and only up to week 1's square-root law. In the lecture's MMO a 3× faster server saves 2.4%.
- **"Packing players tighter saves on everything."** Fill only divides the compute term. Bytes and services are paid per player, however tightly you pack them.
- **"Cost engineering is about the average."** The average sets the monthly budget, but the worst hour sets the ceiling, and a crowd can double the cost of an hour through bytes alone. Cap it with a shaper and price both numbers.
- **"Spot capacity is free money."** Its discount only applies to the compute share, and it costs seats (`u ≤ 1 − q x`) and evacuations. For a bandwidth-heavy MMO it saves a few percent.

## Check yourself

1. With the lecture's baseline, the egress price rises to $0.12 per GB. What is the new cost per 1,000 player-hours, and what share is network?
2. A team makes the server 2× faster (zone capacity 938 → 1,419 at `h = 0.1`). How much does the total fall, in dollars per 1,000 player-hours and in percent? What is the most any compute project could save?
3. A shooter runs at one game per core on the $1.80, 36-core host from section 2, 10 players per game, 6,000 B/s per client, $0.08 per GB, and no shared services. What share of its bill is compute? What does moving to three games per core save?
4. A fleet runs 80% of its servers on spot, and the provider can reclaim up to half of the spot servers at once. What is the highest safe fill? The fleet currently runs at 70%. Is it safe?

<details>
<summary>Answers</summary>

1. Network is `21.6 × 0.12 / 1000 × 1000 = $2.592`. The total is `0.107 + 2.592 + 0.250 = $2.949`, and network is 87.9% of it.
2. Compute becomes `1000 × 0.40 / (8 × 1,419.3 × 0.5) = $0.0705`, down from $0.1067. The total falls by $0.036, about 1.7%. The most any compute project could save is the compute share, 5.1%.
3. At one game per core, 360 players share the host: compute `1000 × 1.80 / 360 = $5.00`, network $1.728, so compute is `5.00 / 6.728 = 74%`. At three games per core, compute is $1.667 and the total is $3.395, a saving of 49.5%.
4. `u ≤ 1 − 0.5 × 0.8 = 0.6`. At 70% fill, a worst-case reclaim leaves 60% of the servers to hold 70% of full-fleet load, so players would be refused or crammed into overloaded zones. Either lower the fill to 60%, move fewer servers to spot, or accept that a bad reclaim causes a queue.

</details>

## Lab / assignment hook

[Lab 13, the player-hour bill](../labs/lab13.md). You implement the cost model on top of week 1's capacity function, compute the shares and the lever table, add the spot fill limit, and write a one-page cost plan that ranks three proposals for a given game by dollars saved and names what each costs players.

## Sources

- Randall, B. "VALORANT's 128-Tick Servers" (Riot Games technology blog, 31 August 2020). First build at about 50 ms per frame, 7.8125 ms frame at 128 ticks, target of three games per core, 2.6 ms and then 2.34 ms per frame after keeping 10% for the operating system, final frame time below 2 ms, 36-core hosts with 108 games or 1,080 players, and one core per game described as too expensive to host at scale. Paraphrased.
- Roblox. "Roblox Return to Service 10/28-10/31 2021" (Roblox newsroom, January 2022). Outage of 73 hours, over 18,000 servers and 170,000 containers, on-premises infrastructure chosen for cost and latency control with savings tied to creator payouts, public cloud used for burst capacity, DevOps workflows and most analytics.
- Amazon Web Services. AWS Price List API, AWSDataTransfer offer for us-east-1 (published 16 September 2026). Data transfer out to the internet: $0.09 per GB for the first 10 TB per month, $0.085 for the next 40 TB, $0.07 for the next 100 TB, $0.05 above 150 TB.
- Amazon Web Services. "Amazon EC2 Spot Instances" product page (current, 2026). Spot capacity at up to a 90% discount compared with on-demand.
- Amazon Web Services. "Spot Instance interruption notices" (Amazon EC2 User Guide, current, 2026). Notice issued two minutes before interruption; checking every 5 seconds recommended; notices are best effort.
- EVE University Wiki, "Time dilation" (current mechanics). Game clock slowed per node under load, floor of 10% speed.
- Amdahl, G. M. (1967). Validity of the single processor approach to achieving large scale computing capabilities. *AFIPS Spring Joint Computer Conference*. The ceiling on the speed-up from improving one part of a job, used here for cost.

## Interactive spec: examples/w13-player-hour-cost.html

**The one insight:** the most a lever can save is the share of the term it attacks. In a bandwidth-heavy MMO, a big CPU speed-up hardly moves the bill, while a modest cut in bytes moves it a lot. Raising the tick rate and lowering the bytes flips which term dominates.

**Layout.** Two linked views side by side on desktop, stacked on mobile (bill first).

- **Left, the bill.** One vertical stacked bar for the cost of 1,000 player-hours, three segments: compute (steel), network (blood), services (ochre). Each segment labelled with dollars (3 decimals) and share (1 decimal %). A faint outline shows the baseline total so the student sees how far the bar has moved. Above the bar: total $ per 1,000 player-hours and $ per CCU-month (`total × 730 / 1000`).
- **Right, the levers.** Four horizontal bars, one per lever: "server speed-up", "fill", "bytes per client", "egress price". Each bar shows the saving of that lever alone from the baseline to its current slider value, as a percent of the baseline total (moss). Behind it, a faint bar for the ceiling, the baseline share of the lever's term (compute share for speed-up and fill, network share for bytes and egress price). A text line under the bars: "Largest possible saving from compute: X%. From network: Y%."
- **Numbers panel** below: `N` (zone capacity, 1 decimal), players per server `Z × N × u`, `K_cpu`, `K_net`, `K_svc`, total, each share.

**Controls.**
- Server code speed-up: slider 1 to 10, step 0.1, default 1.
- Fill `u`: slider 0.2 to 0.95, step 0.05, default 0.5.
- Bytes per client `b`: slider 1,000 to 20,000 B/s, step 500, default 6,000.
- Egress price `P_e`: slider $0.00 to $0.15, step 0.005, default 0.08.
- Tick rate: slider 5 to 128 Hz, step 1, default 10. The tick rate scales the week 1 constants: budget per tick `B = 0.5 / rate` s, and zone capacity is recomputed with it (so higher rates hold fewer players).
- Hot-spot share `h`: slider 0 to 1, step 0.05, default 0.1.
- Spot share `x`: slider 0 to 1, step 0.1, default 0, with discount fixed at 70% and reclaim share `q` slider 0 to 1, step 0.05, default 0.25. When `u > 1 − q x`, show a warning "fill above spot limit: a worst-case reclaim cannot be seated" in blood colour and the limit value.
- Reset button.

**Formulas.** `F = π × 100² / 2000²`. `g = h² + (1 − h²) F`. `B = 0.5 / rate`. `N = (−c_p/s + √((c_p/s)² + 4 (c_i/s) g B)) / (2 (c_i/s) g)` with `c_p = 20e-6`, `c_i = 2e-6`, speed-up `s`. `P_s_eff = 0.40 × (1 − 0.7 x)`. `K_cpu = 1000 × P_s_eff / (8 × N × u)`. `K_net = 1000 × b × 3600 / 1e9 × P_e`. `K_svc = 0.25`. Lever savings are computed each with only its own control moved from the baseline (speed-up 1, fill 0.5, bytes 6,000, egress 0.08) and all other controls at their current values.

**Test values** (rate 10, h 0.1, x 0 unless stated). Baseline: `N = 937.5`, `K_cpu = 0.107`, `K_net = 1.728`, total 2.085, shares 5.1 / 82.9 / 12.0%, CCU-month $1.52. Speed-up 3: `N = 1,792.0`, total 2.034, saving 2.4%. Speed-up 2: `N = 1,419.3`. Fill 0.7: total 2.054, 1.5%. Bytes 4,000: total 1.509, 27.6%. Egress 0.06: total 1.653, 20.7%. `h = 0.25`: `N = 530.9`, `K_cpu = 0.188`. `h = 0.25` and bytes 12,000: total 3.894. `x = 0.6`: `P_s_eff = 0.232`, `K_cpu = 0.062`, total 2.040; with `q = 0.25` the limit is 0.85. Rate 128: `N = 153.5`, `K_cpu = 0.652`, compute share 25%; rate 128 with bytes 1,500: network 0.432, compute share 49%.

**Accessibility.** Keyboard-operable sliders with visible focus and value labels. An `aria-live="polite"` region announces the total and the largest share when they change. Respect `prefers-reduced-motion` (no bar tweening). Palette from `templates/interactive-tokens.css`, light and dark.
