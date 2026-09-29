# MMO404 · Week 04 — Replication prioritization and relevancy

**Why this matters:** In a busy MMO scene, the server knows about far more than it can send. Some entities will be stale on the client every tick, and the only question is which ones. This week you learn to answer that question on purpose, with a priority function you can write down, test and tune, instead of letting the order of a hash map decide who teleports.

**You will be able to:**
- Separate relevancy (who may receive an entity at all) from priority (what share of the budget it gets), and compute the cost of each per tick.
- Compute each entity's update interval from a priority function and a byte budget with the fair-share (water-filling) rule, and check it against a priority accumulator.
- Derive why an inverse-distance falloff gives every entity of a class the same on-screen error, and predict what a new crowd does to everyone else's error.
- Design and critique a priority function for a given MMO scene, including class weights, a starvation floor and relevancy hysteresis.

**Before class:** Mark Frohnmayer and Tim Gift, "The TRIBES Engine Networking Model" (Dynamix, an undated paper written while Tribes II was in development), the sections on the Stream and Ghost managers and on the Simulation layer. Glenn Fiedler, "State Synchronization" (Gaffer on Games, January 2015), the section on priority accumulators. Epic Games, "Actor Relevancy" and "Actor Priority" (Unreal Engine 5.8 documentation).

**Prerequisites from earlier courses:** [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (the per-client byte budget and the priority accumulator in its section 4; this lecture starts where that section stops). [CS202 week 7, snapshots and delta compression](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w07-snapshots-and-delta-compression.md) (why an entity's first update costs more than later ones). [CS202 week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) (what the client draws between updates). [MMO302 week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (grids, radius and hysteresis). [MMO404 week 3, spatial partitioning at scale](w03-spatial-partitioning-at-scale.md).

**Interactive:** [examples/w04-replication-priority.html](../examples/w04-replication-priority.html). Keep it open during section 2.

---

## 1. Two questions, not one

When the server builds a packet for one client, it answers two different questions, and a lot of bad netcode comes from mixing them up.

**Relevancy** asks whether this client may know about this entity at all. The answer is yes or no. An entity that is relevant has a *ghost* (a client-side copy, the word comes from Tribes) or an open channel (Unreal's term) on that client. An entity that is not relevant does not exist for that client. Relevancy is where you apply the area of interest from MMO302 week 3, plus rules that have nothing to do with distance: a stealthed rogue is not relevant to enemies, a quest NPC is relevant only to players on the quest, and your own inventory is relevant only to you.

**Priority** asks what share of this client's byte budget an entity gets, given that it is relevant. The answer is a number. It decides how often the entity is updated, and so how stale the client's copy is.

The two questions have different costs and different failure modes.

| | Relevancy | Priority |
|---|---|---|
| Output | A set per client | A number per (client, entity) pair |
| Typical clock | Slow, about once a second | Every packet |
| Cost to change the answer | High, since opening a ghost sends the full state and closing it deletes the copy | Low, since the next packet just orders things differently |
| Failure if wrong | Entities pop in or out, or information leaks (wallhacks) | Entities stutter or lag behind |
| Needs hysteresis | Yes, or entities flicker at the boundary | No |

That third row explains why relevancy runs on a slow clock. From CS202 week 7, an entity that a client has never seen must be sent in full, because there is no baseline to delta against. If a new ghost costs 120 bytes and an ongoing delta costs 20, opening and closing a ghost every second at a boundary costs six deltas each time. Unreal's documentation (UE 5.8) states the same idea in its own terms. The server re-checks relevancy per connection about once a second, and it closes an actor's channel only after the actor has been irrelevant for 5 seconds.

Priority, on the other hand, changes every packet, because it depends on time. An entity that was just sent has nothing new to say. An entity that has waited ten ticks has a lot.

### The budget is the hard part

Suppose relevancy has done its job and left 249 entities in view of one client. That is a normal number for a raid, a city hub or a siege. The client's budget from CS202 week 13 is 20 entity updates per tick at 20 ticks per second, 20 bytes per update. That is `20 × 20 + 28 = 428` bytes per packet, or 68.5 kbit/s with the header. To send all 249 every tick would take 12.5 times that.

So on any given tick, 229 of the 249 entities are not updated. That is the design problem, and priority is the tool.

## 2. Worked example: a budget shared by distance and relevance

### The hook

*Starsiege: Tribes* shipped in December 1998 with up to 128 players in one game, human or AI. Its networking paper describes a client on a 28.8 kbit/s modem that asks the server for 10 packets a second of 200 bytes each, about 2 KB of data per second. Now imagine a battle with 60 players in view and a few hundred projectiles, vehicles and items. Even at a thrifty 10 bytes per update and 10 updates per second, 60 players alone would be 6 KB/s, three times the pipe. Yet the game was playable on those modems. The paper's answer is two sentences long. Only objects in *scope* are sent, and each object in scope gets a priority from its distance, its size on screen, its speed relative to the player and how interesting its type is. Your job this week is to turn those sentences into a model you can compute.

### The model

Each relevant entity `i` gets a priority

```
p_i = w_i × f(d_i)
f(d) = d0 / max(d, d0)
```

- `w_i` is the **class weight**: how much this kind of entity matters to this client. Your current target might be 4, other players 2, NPCs 1, loot on the floor 0.5.
- `d_i` is its distance from the client's avatar, in metres.
- `f(d)` is the **distance falloff**. This one is inverse distance, flat inside `d0` so it never divides by zero. With `d0 = 10` m, `f` is 1 at 10 m, 0.5 at 20 m, 0.25 at 40 m and 0.125 at 80 m.

The client can take `B` entity updates per tick. We want each entity's **update rate** `ρ_i`, the fraction of ticks on which it is sent. An entity cannot be sent more than once per tick, so `ρ_i ≤ 1`. The rates must use the whole budget, `Σ ρ_i = B`. The **fair-share rule** says that below the cap, rate is proportional to priority:

```
ρ_i = min(1, λ × p_i)        choose λ so that Σ ρ_i = B
update interval  = 1 / ρ_i   ticks
```

This is called water-filling. Picture a tank with a bumpy floor made of `1 / p_i`. Pour in `B` units of water and each entity gets as much as fits above it, up to a ceiling of one. The number `λ` is the water level. Everything below the cap gets a share of the budget in exact proportion to its priority. That is the meaning of Unreal's line that only the ratio between priorities matters.

To find `λ`, start by assuming no entity is capped, so `λ = B / Σ p`. If any entity then has `λ p_i ≥ 1`, fix its rate at 1, take it out, reduce `B` by one, and recompute from the rest. Repeat until nothing new is capped.

### Numbers you can check

Take one client in an open-world fight. It is a healer in a party of eight, targeting an enemy at 10 m. Budget `B = 20` updates per tick, tick rate 20 Hz, so one tick is 50 ms.

| Group | Count | Class weight `w` | Distance | `f(d)` | Priority `p` | Group total `Σp` |
|---|---|---|---|---|---|---|
| Your target | 1 | 4 | 10 m | 1 | 4 | 4 |
| Party members | 8 | 2 | 10 m | 1 | 2 | 16 |
| Enemy players | 16 | 2 | 20 m | 0.5 | 1 | 16 |
| NPCs | 32 | 1 | 40 m | 0.25 | 0.25 | 8 |
| Far players | 64 | 2 | 80 m | 0.125 | 0.25 | 16 |
| Far NPCs and loot | 128 | 0.5 | 80 m | 0.125 | 0.0625 | 8 |
| **All** | **249** | | | | | **68** |

First guess, `λ = 20 / 68 = 0.294`. The target has `4 × 0.294 = 1.18 ≥ 1`, so it is capped at one update per tick. Take it out. The rest have total priority `68 − 4 = 64` and share the 19 remaining slots, so `λ = 19 / 64 = 0.297`. Now no one else reaches the cap (party members get `2 × 0.297 = 0.59`), so we are done.

| Group | Rate `ρ` | Interval | Interval at 20 Hz | Slots per tick used by the group |
|---|---|---|---|---|
| Your target | 1 | 1 tick | 50 ms | 1 |
| Party members | 0.594 | 1.68 ticks | 84 ms | 4.75 |
| Enemy players | 0.297 | 3.37 ticks | 168 ms | 4.75 |
| NPCs | 0.074 | 13.5 ticks | 674 ms | 2.375 |
| Far players | 0.074 | 13.5 ticks | 674 ms | 4.75 |
| Far NPCs and loot | 0.019 | 53.9 ticks | 2.7 s | 2.375 |

Check the last column adds to 20. It does: `1 + 4.75 + 4.75 + 2.375 + 4.75 + 2.375 = 20`. Also notice that each uncapped group's slots are its share of the uncapped priority. Party members hold 16 of the 64, so they get 16/64 of the 19 slots, which is 4.75.

Here is the rule as code. It prints the rows above.

```python
def fair_rates(prios, budget):
    """Water-filling: rate = min(1, lam * p), rates sum to budget."""
    capped = set()
    while True:
        rest = [i for i in range(len(prios)) if i not in capped]
        lam = (budget - len(capped)) / sum(prios[i] for i in rest)
        new = {i for i in rest if lam * prios[i] >= 1}
        if not new:
            break
        capped |= new
    return [1.0 if i in capped else lam * p for i, p in enumerate(prios)], lam

groups = [("target", 1, 4, 10), ("party", 8, 2, 10), ("enemies", 16, 2, 20),
          ("npcs", 32, 1, 40), ("far players", 64, 2, 80), ("far npcs", 128, 0.5, 80)]
prios, start = [], {}
for name, count, w, d in groups:
    start[name] = len(prios)
    prios += [w * 10 / max(d, 10)] * count
rates, lam = fair_rates(prios, 20)
print(f"lambda {lam:.4f}")
for name, count, w, d in groups:
    r = rates[start[name]]
    print(f"{name:12s} every {1 / r:5.2f} ticks = {50 / r:6.0f} ms")
```

```
lambda 0.2969
target       every  1.00 ticks =     50 ms
party        every  1.68 ticks =     84 ms
enemies      every  3.37 ticks =    168 ms
npcs         every 13.47 ticks =    674 ms
far players  every 13.47 ticks =    674 ms
far npcs     every 53.89 ticks =   2695 ms
```

### What the fair share looks like on screen

An update interval is abstract. What the player sees is how far an entity moves between updates. If an entity runs at speed `v`, it covers `v × interval` metres before the client hears about it again. That displacement is the **drift**. Take a run speed of 7 m/s, an invented but typical figure.

| Group | Interval | Drift at 7 m/s | Angle at the camera, `drift / d` |
|---|---|---|---|
| Party members, 10 m | 84 ms | 0.59 m | 3.4° |
| Enemy players, 20 m | 168 ms | 1.18 m | 3.4° |
| Far players, 80 m | 674 ms | 4.72 m | 3.4° |
| NPCs, 40 m | 674 ms | 4.72 m | 6.8° |
| Far NPCs, 80 m | 2.7 s | 18.9 m | 13.5° |

The three player groups show exactly the same angle. It is the most useful fact in this lecture. Under the fair share, an uncapped entity's interval is `1 / (λ w f(d))`. With inverse-distance falloff, `f(d) = d0 / d`, so the interval grows in proportion to `d`, and so does the drift. Divide by `d` to get the angle and the distance cancels:

```
angle = v × tick / (λ × w × d0)          (radians, uncapped entities, d ≥ d0)
```

The angle depends on speed, class weight and the water level, and not on distance. Distant objects look small, so they can afford to be proportionally wrong. Inverse-distance falloff spends the budget so that every entity of the same class looks equally wrong on screen. Class weight then tilts the result. NPCs have half the players' weight and twice their angular error. Change the falloff and you change the rule. Inverse-square falloff makes far entities much worse than near ones on screen. A flat falloff makes near ones worse.

### Move it yourself

Open `examples/w04-replication-priority.html`. The left view is a top-down map with your avatar in the middle and the 249 entities of the table, each coloured by its update interval. The right view plots each group's angular error in degrees against distance, with the water level `λ` printed above it. Start with the table's settings and the three player groups sit on one flat line. Then press "add crowd" to drop 100 NPCs at 40 m, and watch every line in the right view rise together while nothing on the left moved closer. Switch the falloff from inverse distance to inverse square and the flat line tilts.

### Same idea elsewhere

**Starsiege: Tribes (Dynamix, December 1998; paper written for Tribes II).** The Ghost manager keeps an update list per client, orders it by status change and then by priority, and writes objects into the packet until the packet is full. Each object sets its own priority from distance, projected radius in the client's view, relative velocity, animation state and type modifiers. The paper's example is that projectiles moving toward the client beat vehicles, which beat items. Rewrite it in our form. The type modifiers are `w`. Projected radius is object size divided by distance, which is our `f(d) = d0 / d` with `d0` set by the object's size. The packet budget is `B`, fixed by the client's 10 packets of 200 bytes. Relative velocity is a term we have not used yet, and it is the right instinct, since drift is `v × interval`, so fast objects need a shorter interval for the same error. Section 3 adds it.

**Unreal Engine (Epic Games, UE 5.8 documentation).** Every actor has a `NetPriority`. The defaults are 1.0 for an actor and 3.0 for pawns and player controllers, so a player is a class weight of 3 against a crate's 1. The engine's `GetNetPriority` scales that base by the time since the actor was last replicated and by its distance to the viewer. The time factor is an accumulator by another name. A waiting actor's effective priority grows until it wins a slot. Actors are sorted by that value per connection, and the ones that do not fit when the connection saturates wait for the next update. The relevancy side is a separate function, `IsNetRelevantFor`, that runs through ownership, instigator and visibility rules and then a squared distance test (`NetCullDistanceSquared`). In our terms, that last test is the cut to the set before `f(d)` is applied.

**Fiedler's cube demo (Gaffer on Games, January 2015).** Fiedler's 901 cubes are sent at 60 packets per second within 256 kbit/s, with at most 64 cube states per packet. He sets the player's cube to priority 1,000,000, cubes being pushed around to 100, and cubes at rest to 1. In our form, `B = 64`, and the player's cube is capped at every packet. Say 30 cubes are in motion. The first guess is `λ = 63 / (3,000 + 870) = 0.0163`, which gives the moving cubes `1.63 ≥ 1`, so they are capped too. The remaining 33 slots go to the 870 resting cubes, each sent every `870 / 33 = 26.4` packets, about 0.44 s. Weights 100 times apart mean "always" and "when there is room". Resting cubes do not move, so their drift is zero and their long interval costs nothing on screen.

Three engines from 1998 to today, one rule. A per-client budget is split in proportion to a class weight times a distance term, and waiting entities eventually win.

### Design judgment

- **Choose the falloff by the error you care about.** Inverse distance equalises on-screen error within a class, which suits anything the player looks at. Melee combat, where 2 m of error at 3 m range decides whether a swing lands, may want a steeper curve near the player or a fixed high weight for anything within weapon reach.
- **Put gameplay into the weights, not the distances.** A healer's party at 40 m matters more to that healer than an enemy at 20 m. Weights per client role are cheap to compute and they say what your game is about.
- **Budget the crowd you will actually get.** The water level `λ` is set by the total priority in view. A world boss that pulls 300 players into one spot drops `λ` for everyone there, so test at that density, not at the average.
- **Do not route rare, critical state through priority.** A death, a loot roll or a quest completion must arrive once and for certain. Send those as reliable events ([CS202 week 6](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w06-reliability-over-udp.md)) alongside the prioritised state stream.
- **Watch the lowest priorities.** Water-filling never starves anyone, since every positive priority gets a positive rate. But a 2.7 s interval is effectively a frozen NPC. Section 4 adds a floor.

### Check this example

1. In the table, the 64 far players are removed by a relevancy cut at 60 m, and so are the 128 far NPCs. Recompute `λ` and the party members' update interval.
2. Starting from the original table, 100 extra NPCs arrive at 40 m. By what factor does every uncapped entity's interval grow?
3. A designer changes the enemy players' class weight from 2 to 4, because in PvP enemies matter more than friends. Which groups lose update rate, and does the target stay capped?

<details>
<summary>Answers</summary>

1. Remaining priority `4 + 16 + 16 + 8 = 44`. First guess `λ = 20 / 44 = 0.455` caps the target (`1.82`). Then `λ = 19 / 40 = 0.475`. Party members get `2 × 0.475 = 0.95`, below the cap, so their interval is `1 / 0.95 = 1.05` ticks, about 53 ms. Cutting 192 entities halved the party's interval.
2. The NPCs add `100 × 0.25 = 25` priority, so the total is 93. The first guess is `λ = 20 / 93 = 0.215`, and the target now gets `4 × 0.215 = 0.86`, below the cap. So nothing is capped and `λ` goes from `19 / 64 = 0.297` to `20 / 93 = 0.215`. Every interval that was uncapped grows by `0.297 / 0.215 = 1.38`, and the party's goes from 84 ms to 116 ms. Every player group's angular error rises from 3.4° to 4.7°, although the crowd is 40 m away. The target also loses its cap and now updates on 86% of ticks.
3. Each enemy's priority goes from 1 to 2, so the group total goes from 16 to 32 and the grand total from 68 to 84. The first guess is `λ = 20 / 84 = 0.238`. The target gets `4 × 0.238 = 0.95`, below the cap, so nothing is capped and `λ = 0.238` stands. Enemies now get `2 × 0.238 = 0.48` each, 60% more than before. Every other group loses 20% of its rate (`0.238 / 0.297 = 0.80`), and that includes the target, which now updates on only 95% of ticks. Give the target a larger weight or a hard "always send" flag.

</details>

## 3. Beyond distance: what makes an entity relevant

Distance is the easy term, since you already have positions. The other terms are where your game's design shows.

### Speed and error-driven priority

The drift table shows that the thing to equalise is error, and error is `v × interval`. So speed belongs in the priority. A parked cart and a galloping horse at the same distance should not get the same rate. A simple fix multiplies by speed relative to the viewer:

```
p_i = w_i × f(d_i) × (1 + |v_i − v_viewer| / v0)
```

where `v0` is a reference speed such as walking pace. Tribes names relative velocity for exactly this reason. Stopped entities still get the base priority, so they are refreshed now and then. Next week takes this idea to its end with error-driven updates, which send an entity only when the client's guess of its position is wrong by more than a threshold.

### Gameplay relevance

Some modifiers have nothing to do with geometry.

- **Target and attackers.** The entity you have selected and the entities attacking you should be near the cap whatever their distance. Unreal's relevancy rules put owner and instigator checks before the distance test for this reason.
- **Team and role.** A healer needs party members' health more than enemies' animation. A tank needs every NPC's target.
- **Direction of travel.** An entity moving toward you, especially a projectile, needs attention sooner than one moving away. That is the first of Tribes' interest modifiers.

Keep the modifiers multiplicative and few. Every modifier you add is a knob someone must tune, and two modifiers that both say "enemy nearby" count the same fact twice.

### Relevancy hysteresis

A relevancy test like `d < 60 m` flickers. An entity walking along the circle at 59.9 to 60.1 m is opened and closed every few ticks, and each opening sends its full state. The fix is the hysteresis you met in MMO302 week 3: open at `d < 60` m, close at `d > 70` m. Unreal adds time hysteresis on top. It checks each second and closes an actor's channel only after five seconds of irrelevance. With a 120-byte opening cost and a 20-byte delta, one flicker per second on a boundary costs as much as six extra updates per second. A hundred players milling at the edge of a town can eat the whole budget this way.

### Staleness as an input

The accumulator of CS202 week 13 reaches roughly the fair share without computing `λ`. Each tick every relevant entity adds its priority to a running total, the top `B` totals are sent and reset to zero, and the rest carry over. Here it is on this lecture's table.

```python
def accumulate(prios, budget, ticks):
    acc = [0.0] * len(prios)
    sends = [0] * len(prios)
    for _ in range(ticks):
        acc = [a + p for a, p in zip(acc, prios)]
        for i in sorted(range(len(acc)), key=lambda i: -acc[i])[:budget]:
            acc[i] = 0.0
            sends[i] += 1
    return [ticks / s for s in sends]

groups = [("target", 1, 4.0), ("party", 8, 2.0), ("enemies", 16, 1.0),
          ("npcs", 32, 0.25), ("far players", 64, 0.25), ("far npcs", 128, 0.0625)]
prios, start = [], {}
for name, count, p in groups:
    start[name] = len(prios)
    prios += [p] * count
gaps = accumulate(prios, 20, 10_000)
for name, count, p in groups:
    g = gaps[start[name]:start[name] + count]
    print(f"{name:12s} every {sum(g) / count:5.2f} ticks")
```

```
target       every  1.00 ticks
party        every  2.00 ticks
enemies      every  3.35 ticks
npcs         every 12.36 ticks
far players  every 12.74 ticks
far npcs     every 49.16 ticks
```

Compare with the fair share. The far groups land within 10%. The party members are the interesting miss, at 2.00 ticks instead of 1.68. An entity is sent on whole ticks, so its interval under the accumulator tends to snap to whole numbers. A party member with priority 2 reaches the top after two ticks, and there is not enough spare room to send it after one. The slack goes to the far groups, which come out a little faster than their fair share. NPCs and far players have the same priority, yet they differ by 3% because ties are broken by list order. If you need the exact fair share, compute `λ` and send each entity when its own `ρ_i` says it is due. If you want simplicity and self-correction, the accumulator is close enough.

## 4. The costs you do not see in the packet

### Floors against starvation

Water-filling gives every positive priority a positive rate, but it can be tiny. In the table, far NPCs wait 2.7 s. Add another crowd and they wait 5. Past some interval the client's interpolation (CS202 week 10) gives up and the entity freezes, then jumps. Two fixes are common.

- **A maximum interval.** Promise that every relevant entity is sent at least once every `T_max` ticks. That reserves `N / T_max` slots per tick for `N` relevant entities. With 249 entities and a 2-second floor at 20 Hz (40 ticks), the floor costs `249 / 40 = 6.2` slots of your 20. That is expensive, which tells you something. A floor is a promise about the size of the relevant set.
- **Shrink the set instead.** If the floor costs too much, the relevancy radius is too big for this density. Pull it in, or move distant entities to a cheaper form of update (next week's aggregate and low-detail updates).

### The CPU side

Every term in the priority is computed per client per entity. With `n` clients and `k` relevant entities each, that is `n × k` priorities plus `n` sorts of `k` items every packet. A town of 300 players who each see 250 entities is 75,000 priority evaluations per tick, 1.5 million per second at 20 Hz, before any bytes are written.

Unreal's documentation gives the number that made Epic build a new system. Fortnite has 100 connected players and about 50,000 replicated actors. The default path asks each actor about each connection, which is `100 × 50,000 = 5` million checks per net update, and the documentation says that path bottlenecks the server CPU. The Replication Graph answers by grouping actors in advance. A spatial grid lets each connection look only at nearby cells, and separate lists for dormant and frequently updating actors keep trees and placed props out of the per-tick checks. That is this course's week 3 grid put to work on relevancy, and the same lesson as the bandwidth wall of CS202 week 13. The shape of the work matters more than the constant.

A cheaper trick is to recompute priorities every fourth tick, since distances and weights change slowly, and keep adding them to the accumulator every tick. That cuts the priority work by four.

### Leaks

Relevancy is also a security boundary. Anything you send, a cheater can read. If the server sends an invisible player's position because the stealth check lives on the client, the wallhack writes itself ([MMO302 week 6, simulation authority and anti-cheat](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md)). Priority can be approximate. Relevancy for hidden information must be exact and must run on the server.

## In-class activity (25 minutes)

Groups of three. Each group gets one scene card: a 40-player raid on one boss, a 200-player capital city at peak, or an open-world PvP skirmish of 30 against 30 with siege weapons.

1. List the entity classes in the scene (at least five) with a count and a typical distance for each.
2. Choose class weights and a falloff. Write one sentence per weight saying which player need it serves.
3. With `B = 20` updates per tick at 20 Hz, compute `λ` and the update interval of each class by hand with the water-filling rule. Use the interactive's custom mode to check.
4. Find the class with the worst angular error at 7 m/s. Is that acceptable for your scene? If not, change one weight and show the cost to the other classes.

Expected output: a one-page table (class, count, distance, weight, priority, interval, angular error), the one change you made in step 4, and what it cost. Groups with the same card compare weights and argue.

## Common misconceptions

- **"Relevancy and priority are the same thing with different thresholds."** Relevancy is a set with an expensive entry and exit. Priority is a share with no entry cost. Using priority to hide an entity (giving it zero) still leaves its ghost open. Using relevancy to throttle an entity makes it pop in and out.
- **"Doubling an entity's priority doubles its update rate."** Only while its rate is below the cap and only if the others stay the same. Doubling one priority also lowers `λ` for everyone else, so part of the gain comes out of other entities' rates.
- **"Far away entities are cheap, so a big relevancy radius is free."** Each far entity has a small priority, but a ring of radius `R` holds a number of entities that grows with `R²` at uniform density. Inverse-distance priority summed over that ring grows with `R`, so the far field keeps pulling `λ` down as the radius grows.
- **"The accumulator gives exactly the fair share."** It approximates it. Intervals snap to whole ticks, and ties are broken by order, as the section 3 run shows.

## Check yourself

1. A client with `B = 12` sees 4 entities at priority 3 and 40 entities at priority 0.5. Compute `λ` and both update intervals.
2. With inverse-distance falloff and `λ = 0.2`, `d0 = 10` m, a 20 Hz tick and class weight 1, what angular error does an NPC running at 5 m/s have? Does it depend on the NPC's distance beyond 10 m?
3. A designer proposes a 2-second maximum interval for every relevant entity in a 200-player city where each client sees 300 entities, at 20 Hz with `B = 25`. What fraction of the budget does the floor use? What would you change?
4. Explain in two sentences why Unreal closes an actor channel only after five seconds of irrelevance, using the cost of opening a ghost.

<details>
<summary>Answers</summary>

1. Total priority `12 + 20 = 32`. `λ = 12 / 32 = 0.375`. Priority-3 entities get `1.125`, so they are capped at 1. Then `λ = (12 − 4) / 20 = 0.4`, and the others get `0.2`. The intervals are 1 tick and 5 ticks, or 50 ms and 250 ms at 20 Hz.
2. `angle = v × tick / (λ × w × d0) = 5 × 0.05 / (0.2 × 1 × 10) = 0.125` rad, about 7.2°. It does not depend on distance beyond 10 m, which is the point of inverse-distance falloff.
3. The floor needs `300 / 40 = 7.5` slots per tick, 30% of 25. That leaves 17.5 slots for everything the priorities want. Better options: cut relevancy so each client sees fewer entities in the city, or send the far crowd as cheap aggregate updates (week 5) and apply the floor only to what remains.
4. Opening a ghost sends the entity's full state because there is no baseline to delta from, which costs several ordinary updates. A delay before closing stops an entity that wanders back and forth across the boundary from being opened and closed repeatedly, which would waste that cost each time.

</details>

## Lab / assignment hook

[Lab 04, priority allocator](../labs/lab04.md). You implement the priority function, the fair-share rule and the accumulator, check them against this lecture's tables, then run a seeded 400-entity scene with moving crowds and measure each class's interval and angular error. Deliverable: your `priority.py`, a CSV of per-class intervals under three falloffs, and a one-page priority design for a scene from the in-class activity.

## Sources

- Frohnmayer, M. and Gift, T. "The TRIBES Engine Networking Model, or How to Make the Internet Rock for Multi-player Games" (Dynamix, undated; the abstract says the model is being developed for Tribes II and was first used in Starsiege: Tribes. Copy at https://www.gamedevs.org/uploads/tribes-networking-model.pdf). Starsiege: Tribes shipped December 1998 with up to 128 players; a 28.8 modem client example of 10 packets per second of 200 bytes, about 2 KB/s; scoping and priority from distance, projected radius, relative velocity, animation state and interest modifiers (projectiles moving toward the client over vehicles over items); update list ordered by status change and then priority.
- Epic Games, "Actor Priority" (Unreal Engine 5.8 documentation). Default `NetPriority` 1.0 for actors and 3.0 for pawns and player controllers; only the ratio matters; `GetNetPriority` uses the base priority, distance to the viewer and time since last replicated.
- Epic Games, "Actor Relevancy" (Unreal Engine 5.8 documentation). Order of checks in `IsNetRelevantFor`, ending with the `NetCullDistanceSquared` distance test.
- Epic Games, "Detailed Actor Replication Flow" (Unreal Engine 5.8 documentation). Relevancy checked per connection about once a second; channels closed after 5 seconds of irrelevance; actors sorted by priority per connection.
- Epic Games, "Replication Graph" (Unreal Engine 5.8 documentation). Fortnite with 100 players and about 50,000 replicated actors; the per-actor, per-connection path bottlenecks server CPU; grouping by spatial grid and by dormancy.
- Fiedler, G. "State Synchronization" (Gaffer on Games, 5 January 2015). Priority accumulator; 901 cubes; 60 packets per second; 256 kbit/s; at most 64 state updates per packet; priorities 1,000,000 for the player cube, 100 for interacting cubes, 1 for cubes at rest.

## Interactive spec: examples/w04-replication-priority.html

**Insight the visual must make obvious:** priority is a share of a fixed budget. With inverse-distance falloff, every uncapped entity of one class shows the same on-screen error, whatever its distance. Adding entities anywhere lowers the water level `λ` and raises everyone's error together.

**Layout.** Two linked views and a number panel. Desktop: map on the left, error chart on the right, panel below. Under 700 px: stacked, map first.

**Scene data (default, must match section 2).** Avatar at the origin. Six groups, placed on rings at their distance with evenly spaced angles (group index offsets the start angle by 15° so dots do not overlap).

| Group | Count | Weight | Distance (m) | Colour role |
|---|---|---|---|---|
| target | 1 | 4 | 10 | accent |
| party | 8 | 2 | 10 | series 1 |
| enemies | 16 | 2 | 20 | series 2 |
| npcs | 32 | 1 | 40 | series 3 |
| far players | 64 | 2 | 80 | series 4 |
| far npcs | 128 | 0.5 | 80 | series 5 |

**Model.**
- `f(d)`: inverse (`d0 / max(d, d0)`, default), inverse square (`(d0 / max(d, d0))²`) or flat (`1`). `d0 = 10` m.
- `p = w × f(d)`. Relevancy cut: entities with `d > R` are removed before the allocation. `R` default 100 m.
- Fair share by water-filling (section 2 algorithm): repeat `λ = (B − capped) / Σ p(uncapped)`, cap any with `λ p ≥ 1`, until no new caps.
- Interval in ticks `1 / ρ`; in ms `50 / ρ` at 20 Hz. Drift `v × interval_seconds`. Angle `degrees(drift / d)`.

**Left view (map).** Top-down, 100 m radius, rings at 10, 20, 40, 80 m labelled. Dots coloured on a sequential scale by interval (50 ms to 3,000 ms, log scale), with legend. Culled entities drawn as hollow grey dots. The relevancy radius drawn as a dashed circle.

**Right view (error chart).** x axis distance 0 to 100 m, y axis angular error in degrees (0 to 20). One marker per group at its distance, with a horizontal guide line through all groups that share the target's weight class. Water level `λ` printed at top: "λ = 0.2969".

**Controls (all keyboard accessible).**
- Budget `B`: slider 5 to 60, default 20.
- Falloff: segmented control inverse / inverse square / flat.
- Relevancy radius `R`: slider 20 to 100 m, default 100.
- Speed `v`: slider 1 to 15 m/s, default 7.
- "Add crowd" button: adds 100 NPCs (weight 1) at 40 m; pressing again removes it. Label toggles "Remove crowd".
- Custom mode: an editable table of the six groups (count, weight, distance) for the in-class activity.

**Number panel.** One row per group: priority, rate, interval ticks, interval ms, drift m, angle degrees, slots per tick. Totals row: slots sum (must equal `B` when not everything is capped).

**Test values (default settings).** `λ = 0.2969`. Target rate 1, 50 ms. Party 84 ms, 3.38°. Enemies 168 ms, 3.38°. NPCs 674 ms, 6.75°. Far players 674 ms, 3.38°. Far NPCs 2,695 ms, 13.51°. Slot sum 20.000.
- With crowd added: `λ = 0.2151` (the target is no longer capped, rate 0.860), party 116 ms, party angle 4.66°.
- With `R = 60`: `λ = 0.4750`, party 53 ms (1.05 ticks).
- Inverse square, default otherwise: `λ = 0.8462`, party capped at 50 ms (2.01°), enemies 118 ms (2.37°), far players 1,891 ms (9.48°). The player groups no longer share an angle, and the far players' error is four times the enemies'.

**First screen.** Default settings, with the three player groups' markers on one horizontal line in the right view and a caption "Same class, same on-screen error".
