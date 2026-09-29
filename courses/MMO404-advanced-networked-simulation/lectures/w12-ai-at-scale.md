# MMO404 · Week 12 — AI at scale

**Why this matters:** An MMO server runs thousands of monsters, and players only ever look at a few dozen of them. If every monster thinks at full rate all the time, the AI alone needs several cores per zone. This week you learn to spend AI time where players can see it, to predict the cost from where players stand, and to keep the savings from turning into sleepy monsters that ignore a player running at them.

**You will be able to:**
- Compute a zone's AI cost from mob density, player positions and a tiered think-rate policy, and explain why spread-out players cost far more than a raid in one spot.
- Design tier radii and rates that fit a CPU budget, and compute the reaction delay each tier adds.
- Schedule AI updates so that the busiest tick costs the same as the average one.
- Choose between per-agent pathfinding, precomputed tables and shared flow fields for a given crowd, and justify the choice with a cost estimate.

**Before class:** Gravot, Yokoyama and Miyake, "Precomputed Pathfinding for Large and Detailed Worlds on MMO Servers", chapter 20 of *Game AI Pro* (2013), sections 20.1, 20.2 and 20.9 (free online at gameaipro.com). Emerson, "Crowd Pathfinding and Steering Using Flow Field Tiles", chapter 23 of the same book, sections 23.1 to 23.7 and 23.15.

**Prerequisites from earlier courses:** [MMO404 week 1](w01-limits-of-the-zone-model.md) (tick budget, cost that follows density), [week 4](w04-replication-prioritization-and-relevancy.md) (priority under a budget, the accumulator) and [week 10](w10-consistency-models.md) (the visibility window). [CS203 week 4, A* and heuristics](../../CS203-artificial-intelligence-for-games/lectures/w04-a-star-and-heuristics.md), and CS203 weeks 12 and 14 on MMO mob AI (leashing, aggro, threat) and AI LOD with time-slicing ([CS203 week 12](../../CS203-artificial-intelligence-for-games/lectures/w12-mmo-mob-ai-leashing-aggro-threat-tables.md), [CS203 week 14](../../CS203-artificial-intelligence-for-games/lectures/w14-performance-ai-lod-and-time-slicing.md)). [MMO302 week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (the spatial grid you use to find the nearest player). [MMO404 week 8](w08-distributed-simulation-research.md) and [week 9](w09-server-meshing-concepts.md) on splitting a simulation across processes.

**Interactive:** [w12-ai-lod.html](../examples/w12-ai-lod.html). Keep it open during section 2.

---

## 1. What a monster costs

In CS203 you built monsters that perceive, decide and move. On a server, each of those steps is a cost paid per monster, per update.

- **Perception** asks what the monster can sense: players in aggro range, allies calling for help, line of sight to a target. It uses spatial queries on the grid from MMO302 week 3.
- **Decision** runs the behaviour tree, state machine or utility scores: attack, flee, return home, call for help.
- **Movement** follows a path, which may need a new path search, and steers around others.

Call one pass of all three a **think**, and its CPU cost `c_t`. A monster that thinks 10 times a second costs `10 × c_t` per second whether anyone is watching or not. The rest of this lecture is about not paying for thinks nobody would miss.

Three terms first. **AI level of detail (AI LOD)** means giving a monster less CPU when it matters less, by thinking less often, using a cheaper behaviour, or both. A **dormant** monster does not think at all. It keeps its state and wakes when a player comes near. **Time-slicing** means spreading the monsters' thinks across ticks so that each tick does a fair share, instead of all monsters thinking on the same tick.

## 2. Worked example: 10,000 mobs and who is watching

### The hook

Final Fantasy XIV: A Realm Reborn (Square Enix) runs all its navigation on the servers. Its developers described maps of up to 4 km² holding several thousand NPCs and players, with one server simulating several maps, and said that A* was not an option because the servers had so few CPU cycles for each request. They precomputed every path into lookup tables instead, and a query took about 4 microseconds.

Minecraft makes a harsher cut. In Java Edition since 1.18 (2021), entities outside a player's **simulation distance** are not updated at all, and hostile mobs more than 128 blocks from every player despawn outright.

Both games say the same thing. The server cannot afford to think for every creature every tick. Here is a zone with 10,000 monsters and 200 players online. If every monster thinks 10 times a second at 20 µs a think, the AI alone needs 2,000 ms of CPU every second, two full cores. Yet on the same night, with the same 200 players, the AI might cost 9 ms per second or 400. What decides which?

### The model

Give each monster a think rate from its distance `d` to the **nearest** player, in tiers.

| Tier | Distance to nearest player | Think rate `f` | Added reaction delay, average `1 / (2f)` |
|---|---|---|---|
| Near | under 50 m | 10 per s | 50 ms |
| Mid | 50 to 150 m | 2 per s | 250 ms |
| Far | 150 to 400 m | 0.2 per s | 2.5 s |
| Dormant | 400 m or more | 0 | wakes on promotion |

The zone's AI cost per second is the sum of every monster's rate times the cost of a think:

```
C = c_t × Σ f(d_i)
```

We use `c_t = 20 µs`. The zone is 4 km × 4 km (`A = 16 km²`) with `N = 10,000` monsters spread evenly, 625 per km². The AI budget is 250 ms of CPU per second, a quarter of one core.

Now, how many monsters fall in each tier? That depends on how much of the zone lies within each radius of some player. If `n` players stand at random over the zone, the share of the zone within distance `r` of at least one of them is

```
covered(r) = 1 − e^(−n π r² / A)
```

because each player's disc covers `π r² / A` of the zone and random discs overlap. The number of monsters within `r` of a player is `N × covered(r)`. Subtract the tiers inside to get each ring.

### Numbers you can check

For one player, overlap does not matter, and each tier is close to density times ring area. The near disc has area `π × 50² = 7,854 m²`, so it holds `0.000625 × 7,854 = 4.9` monsters. The mid ring holds `0.000625 × π × (150² − 50²) = 39.3`, and the far ring `0.000625 × π × (400² − 150²) = 270`. The cost is `20 µs × (4.9 × 10 + 39.3 × 2 + 270 × 0.2) = 20 µs × 181.6 = 3.6 ms` per second. The coverage formula, which the table and the code use, gives 4.9, 39.2 and 265 instead, because `1 − e^(−x)` is a little smaller than `x`. For the 400 m disc, `x = π × 400² / 16,000,000 = 0.0314`, and the gap is already 1.6%. The cost rounds to 3.6 ms per second either way.

For 200 players spread over the zone, use the coverage formula. `covered(50) = 1 − e^(−200 × 7,854 / 16,000,000) = 1 − e^(−0.098) = 0.094`, so 935 monsters are near. Doing the same at 150 m and 400 m gives the rest of the row below.

| Player layout | Near | Mid | Far | Dormant | AI cost `C` | Share of 250 ms/s budget |
|---|---|---|---|---|---|---|
| Every mob at 10 Hz (no LOD) | 10,000 | — | — | — | 2,000 ms/s | 800% |
| 1 player (model) | 5 | 39 | 265 | 9,691 | 3.6 ms/s | 1.5% |
| 200 spread out (model) | 935 | 4,932 | 4,114 | 19 | 400.8 ms/s | 160% |
| 200 spread out (simulated) | 939 | 5,000 | 4,001 | 60 | 403.8 ms/s | 162% |
| 200 in 10 groups (simulated) | 189 | 612 | 2,450 | 6,749 | 72.1 ms/s | 29% |
| 200 in one raid (simulated) | 24 | 63 | 350 | 9,563 | 8.7 ms/s | 3.5% |

Three things stand out.

- **AI cost follows the ground players cover, not the number of players or monsters.** The same 200 players cost 403.8 ms/s spread out and 8.7 ms/s in one raid, a factor of 46. Only the dormant column changes between the rows, because the monsters never moved.
- **This is week 1 turned upside down.** A crowd in one place was the worst case for replication, because pairs grow with density. For AI, the crowd is the best case, because 200 players in one spot wake the monsters of one spot. Spread-out players, questing alone across the whole map, are the expensive night for AI.
- **Even with LOD, a busy evening can blow the budget.** The spread-out row is 60% over. LOD turned an 8× problem into a 1.6× problem. Sections 3 and 4 close the rest of the gap.

The group rows have no model value because the coverage formula assumes players stand at random. A group of 20 players spread over about 60 m behaves roughly like one player with slightly larger discs. Counting each group as one player gives 34 ms/s for ten groups, half the simulated 72.1, because the discs of a real group are wider than one player's. That is a useful lower bound.

Here is the model and the simulation. It is the core of Lab 12.

```python
import math, random

WORLD = 4000.0                                   # metres per side, 16 km²
N_MOBS = 10_000
TIERS = ((50, 10.0), (150, 2.0), (400, 0.2))     # (radius in m, thinks per second); beyond: dormant
C_T = 20e-6                                      # CPU seconds per think

def model_cost(n_players):
    """Players spread at random: the share of the world within r of someone is 1 - e^(-n pi r^2 / A)."""
    within = [N_MOBS * (1 - math.exp(-n_players * math.pi * r * r / WORLD**2)) for r, _ in TIERS]
    counts = [within[0], within[1] - within[0], within[2] - within[1]]
    return 1000 * C_T * sum(c * hz for c, (_, hz) in zip(counts, TIERS))

def measured_cost(n_players, groups=None, seed=12):
    rng = random.Random(seed)
    mobs = [(rng.uniform(0, WORLD), rng.uniform(0, WORLD)) for _ in range(N_MOBS)]
    if groups is None:                           # spread over the whole world
        players = [(rng.uniform(0, WORLD), rng.uniform(0, WORLD)) for _ in range(n_players)]
    else:                                        # gathered in `groups` clusters, 30 m spread
        centres = [(rng.uniform(500, 3500), rng.uniform(500, 3500)) for _ in range(groups)]
        players = [(cx + rng.gauss(0, 30), cy + rng.gauss(0, 30))
                   for cx, cy in (centres[i % groups] for i in range(n_players))]
    total = 0.0
    for m in mobs:
        d = min(math.dist(m, p) for p in players)
        total += next((hz for r, hz in TIERS if d < r), 0.0)
    return 1000 * C_T * total

print(f"every mob at 10 Hz: {1000 * C_T * 10 * N_MOBS:,.0f} ms/s")
for label, n, g in (("1 player", 1, None), ("200 spread", 200, None),
                    ("200 in 10 groups", 200, 10), ("200 in one raid", 200, 1)):
    model = f"{model_cost(n):6.1f}" if g is None else "     -"
    print(f"{label:17} model {model} ms/s   measured {measured_cost(n, g):6.1f} ms/s")
```

It prints `every mob at 10 Hz: 2,000 ms/s`, then the model and measured costs from the table: 3.6 and 3.3 for one player, 400.8 and 403.8 for 200 spread out, and the measured 72.1 and 8.7 for the groups and the raid. The single-player simulation reads 3.3 rather than 3.6 because one random player out of 10,000 random monsters is a small sample.

The simulation finds the nearest player by checking all of them, which is fine for a lecture and far too slow for a server. On a server you use the grid from MMO302 week 3. Lab 12 asks you to do that and time the difference.

### Move it yourself

Open `examples/w12-ai-lod.html`. The left view is the zone from above with 10,000 monsters as small dots, coloured by tier, and the players as larger markers. The right view is a stacked bar of AI cost by tier against the 250 ms/s budget line. Start with 200 players spread out. The map is a quilt of overlapping rings and almost every dot is lit. Now drag the "grouping" slider toward one raid. The players slide together, the lit area shrinks to one patch, and the bar collapses to a sliver. Nothing about the monsters changed. Then set the far-tier radius from 400 m to 250 m with the players spread, and watch how much of the bar was far-tier monsters thinking once every five seconds.

### Same idea elsewhere

Each technique below cuts one factor of `C = c_t × Σ f(d_i)`. Some cut `f` for distant monsters, some cut `c_t`, some share one think among many monsters.

**Minecraft (Java Edition 1.18 and later).** Simulation distance sets `f = 0` beyond a radius measured in chunks around each player (12 chunks by default in single player). Nothing outside it moves. Despawning goes further and deletes hostile mobs more than 128 blocks from every player, with a chance of despawning each tick beyond 32 blocks. In our form, simulation distance is the dormant radius, and despawning removes monsters from `N` rather than setting them to sleep. That works in Minecraft because a despawned zombie can be replaced by a new one without anyone noticing. In an MMO, a named rare spawn or a monster mid-fight with a player cannot be deleted, so MMOs use dormancy instead.

**Final Fantasy XIV: A Realm Reborn (Gravot, Yokoyama and Miyake, *Game AI Pro*, 2013).** FFXIV cuts `c_t` for the most expensive part of a think, the path search. It precomputes the next step between polygons into hierarchical lookup tables, so a path query takes about 4 µs, and the heaviest remaining work is finding the nearest navigation polygon. The price is memory and flexibility. The biggest table in their tests was about 4 MB for a 1.5 km² forest, and any change to the world needs new tables, though doors can still open and close at run time. In our form, that chapter shows how to make the path part of `c_t` small enough to afford full-rate thinking near players.

**Supreme Commander 2 (Gas Powered Games, 2010; Emerson, *Game AI Pro*, 2013).** Supreme Commander 2 shares one think among many agents. Instead of one A* path per unit, it builds flow fields over 10 × 10 m sectors, where each grid square stores the direction to move toward the goal, and caches them so that any unit passing through the same sector toward the same exit reuses the same field. It also caps how many tiles it builds per tick to keep the CPU cost bounded. In our form, the path part of `c_t` is paid once per sector and goal instead of once per unit, and the per-tick cap is a budget like week 4's.

**The LOD Trader (Sunshine-Hill, *Game AI Pro*, 2013).** Fixed distance tiers have a flaw that the chapter names directly. When monsters cluster near a player, no distance threshold both respects the budget and gives the visible monsters the detail you want. The LOD Trader treats every monster's detail level as a choice to make each frame and picks the set that gives the most value without going over the CPU budget, in tens of microseconds. That is week 4's priority allocation applied to AI. Our tiers are the simple version, and section 3 adds the budget.

Four games, one sum. When you study a new game's AI performance, ask which factor it cuts: the number of monsters thinking, how often they think, what one think costs, or how many monsters share one think.

### Design judgment

- **Put tier boundaries outside what players can notice.** A monster in the mid tier reacts on average 250 ms late. That is fine at 100 m, where a player cannot tell. It is not fine inside aggro range. Make the near radius comfortably larger than the largest aggro radius in the zone.
- **Recompute tiers every tick, even for monsters that think slowly.** A player running at 7 m/s covers 35 m in the 5 seconds between a far-tier monster's thinks. If the tier is only updated when the monster thinks, a player can reach a far-tier monster before it notices. Finding the nearest player on a grid is cheap. Promote monsters the moment a player crosses a boundary, and keep the expensive think on its own schedule.
- **Plan for the spread-out night, not the raid.** Your content decides how players spread. A zone full of solo quests with kill targets scattered everywhere is the expensive case for AI. A world event that pulls everyone to one boss is the cheap case, even though it is the expensive case for replication.
- **Decide what dormant means for monsters in a fight.** A monster fighting a player who walks 400 m away should leash home (CS203 week 12), not freeze in place. Dormancy must never stop a monster halfway through something a player can see.

### Check this example

1. With the lecture's tiers and `c_t = 20 µs`, what does one isolated player cost if monster density doubles to 1,250 per km²?
2. Use the coverage formula to find the model cost for 50 players spread over the zone. Does it fit the budget?
3. A designer shrinks the far tier from 400 m to 250 m. For one isolated player, how many monsters leave the far tier, and how much CPU per second does that save?

<details>
<summary>Answers</summary>

1. Every tier count doubles, so the cost doubles to about 7.3 ms/s.
2. `covered(50) = 1 − e^(−50 × 7,854 / 16×10⁶) = 0.0243`, so 242 near. `covered(150) = 1 − e^(−0.2209) = 0.198`, so 1,982 within 150 m and 1,740 mid. `covered(400) = 1 − e^(−1.571) = 0.792`, so 7,921 within 400 m and 5,939 far. `C = 20 µs × (242 × 10 + 1,740 × 2 + 5,939 × 0.2) = 20 µs × 7,088 ≈ 141.8 ms/s`. It fits, at 57% of the budget.
3. The far ring shrinks from `π × (400² − 150²)` to `π × (250² − 150²)`, from 431,969 m² to 125,664 m². At 0.000625 per m², that is 270 − 78.5 ≈ 191 monsters becoming dormant. Each thought 0.2 times a second, so the saving is `191 × 0.2 × 20 µs ≈ 0.77 ms` per second per isolated player.

</details>

## 3. The busiest tick, not the average one

Section 2 priced AI per second. The server lives per tick. At 10 Hz, the 200-players-spread night costs 403.8 ms per second, 40.4 ms per 100 ms tick on average. Whether it fits a tick depends on how the thinks are spread.

Suppose every monster in a tier thinks on the same ticks: all mid-tier monsters on ticks 0, 5, 10 and so on, and all far-tier monsters on ticks 0, 50, 100. On tick 0, every monster that is not dormant thinks at once: `939 + 5,000 + 4,001 = 9,940` thinks, costing `9,940 × 20 µs = 198.8 ms`. That tick is twice the length of a whole tick interval. The average is fine and the server still hitches every 5 seconds, and the players notice the hitch, not the average.

**Time-slicing** fixes this with a phase per monster. A mid-tier monster that thinks every 5 ticks does so when `(tick + id) mod 5 = 0`. With ids spread evenly, one fifth of the mid tier thinks on each tick. Now every tick costs about `939 + 5,000/5 + 4,001/50 = 2,019` thinks, or 40.4 ms, the same as the average.

| Schedule | Thinks on the worst tick | Worst tick | Average tick |
|---|---|---|---|
| Every tier in step | 9,940 | 198.8 ms | 40.4 ms |
| Phased by id | about 2,019 | about 40.4 ms | 40.4 ms |

Phasing by id fixes the steady state. It does not fix a sudden change, such as a raid teleporting into a dormant area and promoting 500 monsters to the near tier on one tick. For that, give the AI a per-tick **budget** and a queue, exactly as you gave replication a byte budget in week 4. Each tick, run thinks in priority order until the budget is spent, and let the rest wait. Use an accumulator so that a monster that waited gains priority and thinks next tick. A monster in combat with a player gets a large weight. A far-tier monster gets a small one. When the budget is short, the first thing that suffers is the reaction time of monsters nobody is looking at, which is exactly the cost you want to pay.

The accumulator also gives you a measurable promise. If a tier's monsters are guaranteed at least their share, then the worst reaction delay for a tier with rate `f` is `1 / f` plus the time spent waiting in the queue, and the queue wait is what your load test (MMO302 week 11) should report.

## 4. Pathfinding when everyone wants to move

Paths are usually the largest part of `c_t`. A monster that thinks 10 times a second does not search for a new path every think, but a monster chasing a moving player needs a new one often. Take a raid of 40 players pulling 300 monsters that all chase them across a 500 m area. Three ways to pay for it:

- **One A* search per monster per replan.** Suppose a search costs 0.5 ms on this terrain and each monster replans twice a second. That is `300 × 2 × 0.5 ms = 300 ms` per second, more than the whole AI budget, spent on one pull.
- **Precomputed tables, as in FFXIV.** A table lookup per step costs microseconds. At the chapter's 4 µs per query, `300 × 2 × 4 µs = 2.4 ms` per second. The cost has moved to memory and to a build step, and the world must be mostly static.
- **Shared flow fields, as in Supreme Commander 2.** All 300 monsters want to reach the raid. Build one field toward the raid's position and let every monster read its direction from the field under its feet. Suppose a field over the 500 m area costs 5 ms to build and is rebuilt twice a second: 10 ms per second, whatever the number of monsters, plus a cheap lookup for each one.

These constants are illustrative, but the shape of the result is not. Per-monster search scales with the number of monsters. Shared fields scale with the number of goals. In an MMO, the goal is often the same few players, which is why shared structures pay off. The trade is that a flow field toward one goal does not help a monster heading somewhere else, and splits in the raid mean more fields.

Whatever method you choose, put path requests in a queue with a per-tick budget, like the thinks in section 3. A monster whose path request is waiting can keep steering straight at its target for a tick or two. Players will not notice a monster that takes 200 ms to find a way around a rock. They will notice a server that stops for 300 ms.

### Moving AI to its own process

Weeks 8 and 9 split a simulation across processes. AI is often the first thing moved. An **AI server** reads the world through replication, like a client, and sends monster commands back to the zone server, like a player's inputs. The zone server stays the owner and checks every command.

The price is week 10's visibility window. The AI server sees the world `W` late and its commands arrive `d` later still. With a 10 Hz zone and a 1 ms link, a monster's reaction gains about 100 ms, the same as dropping it one tier. For far and mid tiers that is invisible. For a boss in the middle of a fight, it may not be, which is why some designs keep near-tier and boss AI on the zone server and move only the rest.

## In-class activity (25 minutes)

In groups of three, you are the AI team for a new open-world zone of 3 km × 3 km with 6,000 monsters spread evenly and a budget of 150 ms of AI CPU per second at `c_t = 20 µs`.

1. Using the lecture's tiers and the coverage formula, compute the AI cost for 100 players spread out. Does it fit? (8 min)
2. Choose new tier radii or rates so that 150 spread-out players fit the budget. The near radius must stay at least 40 m, the largest aggro radius in the zone. (10 min)
3. State the average and worst reaction delay of each tier in your design, and the distance a player running at 7 m/s covers in one think interval of each tier. Name the tier whose delay players might notice. (7 min)

Expected output: the cost for step 1 (about 222 ms/s, over budget), a tier table that fits 150 players, and a delay table with one sentence on which tier is riskiest.

## Common misconceptions

- **"More monsters means more AI cost."** More monsters near players does. With dormancy, 10,000 monsters with one player online cost 3.6 ms/s. What you pay for is the ground players cover.
- **"A raid is the worst case."** For replication and combat, yes (week 1). For AI, a raid is cheap, because 200 players in one spot wake the monsters of one spot. Players spread across the map are the expensive case.
- **"Time-slicing reduces AI cost."** It does not change the average at all. It removes the spikes, so the worst tick matches the average one. Lower rates and dormancy reduce the cost.
- **"Slow tiers make monsters slow to notice players."** Only if tiers are updated when the monster thinks. Update tiers every tick from a cheap grid query, and a monster is promoted the moment a player comes near.

## Check yourself

1. A zone has 8,000 monsters in 16 km², all at 10 Hz, with `c_t = 25 µs`. What is the AI cost? What fraction of that does one isolated player cost under the lecture's tiers?
2. With phasing by id, a tier of 3,000 monsters thinks at 2 Hz on a 20 Hz server. How many thinks does it add to each tick?
3. A raid of 40 pulls 200 monsters. Per-monster A* costs 0.8 ms per search with 3 replans per second. A flow field costs 6 ms to build and is rebuilt 3 times a second. Compare the two in ms per second. At how many chasing monsters are they equal?
4. An AI server runs on a separate machine with a 2 ms link to a 20 Hz zone server. Estimate the extra reaction delay it adds, and say which tier of monster you would keep on the zone server.

<details>
<summary>Answers</summary>

1. `8,000 × 10 × 25 µs = 2,000 ms/s`. One player, with density 500 per km²: near 3.9, mid 31.4, far 216. `C = 25 µs × (39 + 62.8 + 43.2) ≈ 3.6 ms/s`, about 0.18% of the full-rate cost.
2. At 20 Hz, a 2 Hz monster thinks every 10 ticks, so each tick has `3,000 / 10 = 300` of them.
3. A*: `200 × 3 × 0.8 = 480 ms/s`. Flow field: `3 × 6 = 18 ms/s`, plus lookups. They are equal when `n × 3 × 0.8 = 18`, so at 7.5 monsters. Above eight chasing monsters, the shared field wins.
4. At 20 Hz, `W ≈ T + d = 50 + 2 = 52 ms`, and the command takes another 2 ms back, so about 54 ms. Keep bosses and near-tier monsters in combat on the zone server, where a 54 ms lag could change who gets hit.

</details>

## Lab / assignment hook

[Lab 12, AI budget](../labs/lab12.md). You implement tier assignment with a spatial grid, reproduce the lecture's cost table and time the grid against brute force, build a time-sliced scheduler with a per-tick budget and measure its worst tick, and write an AI budget for a zone whose players spread out on quest nights and gather for a weekly world boss.

## Sources

- Gravot, F., Yokoyama, T. & Miyake, Y. (2013). "Precomputed Pathfinding for Large and Detailed Worlds on MMO Servers." In S. Rabin (ed.), *Game AI Pro*, chapter 20. CRC Press. Final Fantasy XIV: A Realm Reborn; all navigation on servers; maps of about 4 km² with several thousand NPCs and players; A* ruled out for server CPU; hierarchical lookup tables; about 4 µs per query; largest table about 4 MB for a 1.5 km² forest; doors handled at run time.
- Emerson, E. (2013). "Crowd Pathfinding and Steering Using Flow Field Tiles." *Game AI Pro*, chapter 23. Built for Supreme Commander 2 (Gas Powered Games, published by Square Enix, March 2010); 10 × 10 m sectors of 1 m squares; flow field cache shared across path requests; capping tiles built per tick.
- Sunshine-Hill, B. (2013). "Phenomenal AI Level-of-Detail Control with the LOD Trader." *Game AI Pro*, chapter 14. Distance thresholds cannot both respect a budget and serve clustered characters; LOD chosen per frame to maximize value within the CPU budget, in tens of microseconds.
- Minecraft Wiki, "Simulation distance" (Java Edition 1.18, snapshot 21w38a, 2021; accessed September 2026). Entities beyond simulation distance are not ticked; default 12 chunks in single player.
- Minecraft Wiki, "Mob spawning", despawning section (Java Edition, current). Hostile mobs beyond 128 blocks of every player despawn instantly; beyond 32 blocks they may despawn at random.
- Rabin, S. (ed.) (2013). *Game AI Pro: Collected Wisdom of Game AI Professionals*. CRC Press. Free chapters at gameaipro.com.

## Interactive spec: examples/w12-ai-lod.html

**The one insight:** AI cost follows the ground players cover, not how many monsters or players there are. The same 200 players cost about 400 ms/s spread out and under 10 ms/s gathered in one raid, and the map shows it as the lit area shrinking while the monster dots stay put.

**Layout.** Two linked views and a numbers panel. Desktop: map on the left (55%), bars on the right. Under 700 px: map, bars, panel.

- **Left, the zone map.** A 4 km × 4 km square. 10,000 monsters as 1-2 px dots, coloured by tier: near, mid, far, dormant (dormant faint grey). Players as larger markers. Positions come from a JavaScript port of Python's Mersenne Twister (`random.Random(12)`, including `random.gauss`), drawn in the same order as the lecture's code, so the page reproduces the simulated rows exactly: monsters first, then up to 1,000 spread players. The grouped layout for `k` groups restarts the stream at seed 12, skips the monster draws, then draws `k` centres uniform in [500, 3500] m and a Gaussian offset of 30 m per player, assigned round-robin. Player positions are interpolated between the spread layout and the grouped layout by the grouping slider `g` from 0 (spread) to 1 (grouped): `pos = (1 − g) × spread + g × grouped`. Tier rings may be drawn faintly around players when "show rings" is on. Use a uniform grid with 400 m cells to find each monster's nearest player within 400 m; recompute tiers on every control change.
- **Right top, stacked bar** of AI cost in ms/s split by tier (near, mid, far), against a vertical budget line (default 250 ms/s). Axis to max(300, 1.1 × C). A ghost bar behind it shows the no-LOD cost (2,000 ms/s) when "compare with no LOD" is on, with a break in the axis.
- **Right bottom, per-tick chart.** 50 ticks (5 seconds at 10 Hz) as small vertical bars of thinks per tick, for the current layout, with a toggle "phase by id" (on by default). Off: every tier thinks on ticks where `tick mod (10 / f) = 0`. On: monster `i` thinks when `(tick + i) mod (10 / f) = 0`. Draw the 100 ms tick line converted to thinks (`0.1 / c_t = 5,000` thinks).
- **Numbers panel.** Monsters per tier, dormant count, `C` in ms/s, share of budget, model cost from the coverage formula when `g = 0`, worst tick and average tick in ms, and the average and worst reaction delay for each tier.

**Controls.**
- Players `n`: slider 1 to 1,000, default 200.
- Grouping `g`: slider 0 to 1, step 0.01, default 0.
- Groups `k`: stepper 1 to 20, default 1.
- Tier radii: near 20 to 100 m (default 50), mid 60 to 300 m (default 150), far 150 to 800 m (default 400), each forced to stay above the previous.
- Tier rates: near 1 to 20 Hz (default 10), mid 0.5 to 5 Hz (default 2), far 0.05 to 1 Hz (default 0.2).
- Think cost `c_t`: 5 to 50 µs, default 20.
- Toggles: "phase by id", "show rings", "compare with no LOD". Reset.

**Formulas.** `f(d)` by the tier table (strict `d < r`). `C = 1000 × c_t × Σ f(d_i)` ms/s. Model: `within(r) = N × (1 − exp(−n π r² / 16e6))`, tiers by differences. Reaction delay average `1 / (2f)`, worst `1 / f`.

**Test values** (defaults). Model: 1 player 3.6 ms/s with tiers 4.9 / 39.2 / 265.2 and 9,691 dormant; 50 spread 141.8 ms/s; 200 spread 400.8 ms/s with tiers 935 / 4,932 / 4,114. Seeded simulation, identical to the lecture's: 200 spread 403.8 ms/s with tiers 939 / 5,000 / 4,001; 200 in 10 groups 72.1 ms/s; 200 in one group 8.7 ms/s. No LOD: 2,000 ms/s. Per tick with 939 / 5,000 / 4,001 monsters per tier: in step, worst tick 9,940 thinks = 198.8 ms; phased, about 2,019 thinks = 40.4 ms.

**First screen.** 200 players spread out (`g = 0`), with the caption "Same 200 players. Drag them together and watch the AI bill."

**Accessibility.** All controls keyboard operable with visible focus. Announce `C` and share of budget in an `aria-live="polite"` region when a control changes. With `prefers-reduced-motion`, jump players to new positions without animating. Palette from `templates/interactive-tokens.css`, light and dark. Tiers must differ by dot size or shape as well as colour.
