# CS202 · Week 13 — Tick rate and bandwidth budgets

**Why this matters:** Every multiplayer game ships with two numbers someone chose on purpose: how many times per second the server simulates, and how many bytes it may send each player. Choose them by feel and you find out at launch, when the server bill arrives or the 60-player match stutters. This week you learn to write both numbers down as a budget before you build, and to see which design changes move the budget by a constant and which change its shape.

**You will be able to:**
- Compute a snapshot's size in bytes and packets, a client's download and a server's upload from player count, send rate, bytes per entity, header size and MTU.
- Derive why server upload grows as `n²` without interest management and as `n` with it, and find the player count where a given link hits its limit.
- Compute the CPU time per tick and the latency each tick rate adds, and defend a tick rate for a given game with those numbers.
- Rank the levers (send rate, bytes per entity, entities per snapshot, priority) by how much each one saves, and design a per-client budget.

**Before class:** Glenn Fiedler, "Snapshot Compression" (Gaffer on Games, January 2015), the introduction and the section on the bandwidth target. Respawn, "What Makes Apex Tick: A Developer Deep Dive into Servers and Netcode" (Apex Legends news, April 2021), the section on tick rate. Riot Games, "VALORANT's 128-Tick Servers" (August 2020), the first half.

**Prerequisites from earlier courses:** [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (you will watch `O(n²)` hit a wall in megabits per second). [CS101 week 9, delta time and the fixed timestep](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (a server tick is a fixed timestep). [CS202 week 1](w01-networks-for-game-devs-tcp-vs-udp.md) (28-byte UDP/IPv4 header, the 1,280-byte packet rule), [week 2](w02-latency-jitter-loss-measure-your-own.md) (the latency table and the interpolation delay of two intervals) and [week 3](w03-topologies-peer-to-peer-client-server-relay.md) (the dedicated server upload formula this lecture extends). Quantization comes from [CS202 week 5](w05-serialization-and-bit-packing.md), delta compression from [week 7](w07-snapshots-and-delta-compression.md), and entity interpolation from [week 10](w10-entity-interpolation.md).

**Interactive:** [examples/w13-bandwidth-budget.html](../examples/w13-bandwidth-budget.html). Keep it open during section 2.

---

## 1. Three clocks, not one

Players say "tick rate" for everything the server does per second. A netcode programmer separates three rates, because each one costs something different.

- The **tick rate** `T` is how many times per second the server advances the simulation. One tick reads the queued inputs, moves everything, resolves hits and applies game rules. It is the fixed timestep from CS101 week 9, run on a machine nobody watches. The time between ticks is `1000 / T` ms.
- The **snapshot rate** `r` (also called the send rate or update rate) is how many times per second the server sends each client a picture of the world. It can equal the tick rate or be lower. It can never be higher, because the server has nothing new to say between ticks.
- The **command rate** is how many times per second the client sends its inputs. Several ticks' worth of input can share one packet.

The Source engine shows all three as separate settings. Valve's documentation (archived 2023) lists a tick rate of 66 for *Counter-Strike: Source* and *Team Fortress 2*, 64 by default for *Counter-Strike: Global Offensive*, 60 for the GoldSrc *Counter-Strike*, and 30 for *Left 4 Dead*. The client asks for 20 snapshots per second by default (`cl_updaterate`) and sends about 30 command packets per second (`cl_cmdrate`). The server never sends more snapshots than it simulates ticks.

Each rate has a price.

| Rate goes up | You pay in | Because |
|---|---|---|
| Tick rate `T` | Server CPU | Every tick runs the whole simulation. Twice the ticks, twice the work |
| Snapshot rate `r` | Bandwidth, both ends | Every snapshot is a packet to every client |
| Command rate | Client upload, server receive work | Every command packet carries headers |

And each rate buys latency. From week 2, an event waits on average half an interval for the next tick, and another player sees it through an interpolation buffer of two snapshot intervals. With the tick rate equal to the snapshot rate:

| Rate (Hz) | Interval (ms) | Average wait for a tick | Interpolation (2 intervals) | Total from the rate |
|---|---|---|---|---|
| 10 | 100 | 50 | 200 | 250 |
| 20 | 50 | 25 | 100 | 125 |
| 30 | 33.3 | 16.7 | 66.7 | 83.3 |
| 60 | 16.7 | 8.3 | 33.3 | 41.7 |
| 128 | 7.8 | 3.9 | 15.6 | 19.5 |

Going from 20 to 60 Hz removes 83 ms from what one player sees of another. Going from 60 to 128 removes 22 ms more. The gains shrink as the rate climbs, because they follow `1 / r`. The costs grow in a straight line. Keep that asymmetry in mind for the rest of the lecture.

## 2. Worked example: the n-squared wall at 100 players

### The hook

*Valorant* puts 10 players in a match and runs its servers at 128 ticks per second. *Apex Legends* puts 60 players in a match and runs at 20. Respawn's netcode team wrote in 2021 that the game uses roughly 60 kB/s at the start of a match, and that moving to 60 Hz would triple that to about 180 kB/s. Both studios are competent, and both games are shooters. So why does the bigger game run six times slower? The answer comes from one formula, and it has `n` in it twice.

### The model

A dedicated server has `n` connected players. Every snapshot interval it sends each client a snapshot describing `k` entities.

- `r` is the snapshot rate, in snapshots per second.
- `b` is the bytes per entity in a snapshot: position, rotation, velocity, animation state, health. Quantization (week 5) and delta compression (week 7) shrink it.
- `k` is the number of entities each client hears about. Without **interest management** (sending each client only what is near or relevant to it), `k = n`. With a cap of `K` entities per client, `k = min(n, K)`.
- `h` is the header bytes per packet, 28 for UDP over IPv4.
- `M` is the largest packet you send, 1,280 bytes including headers, from week 1. So one packet carries at most `M − h = 1,252` bytes of entities.

```
packets per snapshot   p = ceil(k × b / (M − h))
snapshot size          S = k × b + h × p                 (bytes)
client download        D = r × S                          (bytes per second)
server upload          U = n × D = n × r × (k × b + h × p)
```

Now look at `U` with no interest management, so `k = n`:

```
U ≈ r × b × n²
```

That is week 3's dedicated-server formula, extended with packet splitting. The `n²` comes from two independent facts. There are `n` clients, and each snapshot describes `n` players. Doubling the match size doubles both.

With a cap `K`, once `n > K`:

```
U ≈ r × b × K × n
```

The exponent drops from 2 to 1. The other three levers, `r`, `b` and `h`, only multiply the curve by a constant.

To convert bytes per second into bits per second, multiply by 8. Divide by 1,000 for kbit/s or by 1,000,000 for Mbit/s.

### Numbers you can check

Take the curriculum's signature case. One hundred players, `r = 20` Hz, `b = 40` bytes per entity (roughly a position, rotation and a few state fields at full precision), `h = 28`, `M = 1,280`.

- Entity bytes per snapshot `100 × 40 = 4,000`. That needs `p = ceil(4,000 / 1,252) = 4` packets.
- Snapshot size `S = 4,000 + 4 × 28 = 4,112` bytes.
- Client download `D = 20 × 4,112 = 82,240` bytes/s, which is 657.9 kbit/s.
- Server upload `U = 100 × 82,240 = 8,224,000` bytes/s, which is 65.8 Mbit/s.
- Over one hour, the server sends `8,224,000 × 3,600 = 29.6` GB for one match.

Now grow the match with everything else fixed. The right-hand columns add an interest cap of `K = 32` entities per client.

| Players `n` | Packets per snapshot | Client download, no cap | Server upload, no cap | Client download, `K = 32` | Server upload, `K = 32` |
|---|---|---|---|---|---|
| 10 | 1 | 68.5 kbit/s | 0.68 Mbit/s | 68.5 kbit/s | 0.68 Mbit/s |
| 25 | 1 | 164.5 | 4.11 | 164.5 | 4.11 |
| 50 | 2 | 329.0 | 16.45 | 213.8 | 10.69 |
| 100 | 4 | 657.9 | 65.79 | 213.8 | 21.38 |
| 200 | 7 | 1,311 | 262.3 | 213.8 | 42.75 |
| 500 | 16 | 3,272 | 1,636 | 213.8 | 106.9 |
| 1,000 | 32 | 6,543 | 6,543 | 213.8 | 213.8 |

Check one cell by hand. At `n = 50` with the cap, each client hears 32 entities, `32 × 40 = 1,280` bytes, which is 2 packets, so `S = 1,280 + 56 = 1,336` bytes. Then `D = 20 × 1,336 = 26,720` bytes/s = 213.8 kbit/s, and `U = 50 × 26,720` bytes/s = 10.69 Mbit/s.

Three things stand out.

- **Without a cap, each doubling of players quadruples the server's upload.** From 100 to 200 players, 65.8 becomes 262.3 Mbit/s. From 500 to 1,000, 1.6 becomes 6.5 Gbit/s. A server with a 1 Gbit/s network card fits 390 players and no more.
- **The client hits a wall too.** Without a cap, each client's download grows as `n`. Past 152 players, every client needs more than 1 Mbit/s just for snapshots. Players on a weak mobile connection drop out of the match long before the server does.
- **With a cap, the client's download stops growing at all.** Past `n = 32`, every client costs the server the same 213.8 kbit/s, and the server's total becomes a straight line. A 1,000-player world costs 213.8 Mbit/s instead of 6.5 Gbit/s, a factor of about 31, and the factor keeps growing with `n`.

The server's CPU sees the same wall. Without a cap, it writes `n × n` entity records into snapshots every interval. At 100 players and 20 Hz that is 200,000 records per second. At 1,000 players it is 20 million.

### Levers, one at a time

Start from the 100-player baseline and apply one change at a time, keeping the earlier ones.

| Step | `r` | `b` | `k` | Snapshot `S` | Client download | Server upload | Saved vs baseline |
|---|---|---|---|---|---|---|---|
| A. Baseline | 20 | 40 | 100 | 4,112 B | 657.9 kbit/s | 65.8 Mbit/s | — |
| B. Quantize fields (week 5) | 20 | 16 | 100 | 1,656 B | 265.0 | 26.5 | 60% |
| C. Interest cap `K = 32` | 20 | 16 | 32 | 540 B | 86.4 | 8.64 | 87% |
| D. Halve the rate | 10 | 16 | 32 | 540 B | 43.2 | 4.32 | 93% |
| (A at 60 Hz, for comparison) | 60 | 40 | 100 | 4,112 B | 1,974 | 197.4 | −200% |

Every row is a factor. B saves 60% because 16 bytes is 40% of 40, and headers shrink from 4 packets to 2. C saves another 67% at 100 players, but that factor is `K / n`, so it grows with the match. D halves everything and adds 50 ms of interpolation delay (from the table in section 1). The 60 Hz row triples the baseline, which is the Apex arithmetic.

Here is the model as code. It fits on one screen and it is the core of this week's lab.

```python
import math

def budget(n, r, b, K=None, h=28, mtu=1280):
    """Bytes per second for one client and for the server, per section 2."""
    k = n if K is None else min(n, K)
    p = max(1, math.ceil(k * b / (mtu - h)))
    snapshot = k * b + h * p
    client = r * snapshot
    return {"k": k, "packets": p, "snapshot": snapshot,
            "client_Bps": client, "server_Bps": n * client}

print(budget(100, 20, 40))          # snapshot 4112, client 82240, server 8224000
print(budget(100, 20, 16, K=32))    # snapshot 540, client 10800, server 1080000
```

### Move it yourself

Open `examples/w13-bandwidth-budget.html`. The left view plots server upload against player count from 2 to 1,000, with the no-cap curve and the capped line drawn together, and a horizontal line for the server's link (1 Gbit/s by default). The right view shows one client's download as a bar, against lines for a 1 Mbit/s mobile connection and a 10 Mbit/s home connection. Start at 100 players. Drag bytes per entity from 40 down to 10 and watch both curves in the left view drop by the same proportion without changing shape. Then drag the interest cap from "off" to 32 and watch the curve straighten. Compression moves the curve. Interest management bends it.

### Same idea elsewhere

**Apex Legends (Respawn, April 2021).** Respawn describes a 20 Hz server that sends snapshots of the world, uses roughly 60 kB/s at the start of a match, and would use about 180 kB/s at 60 Hz. Rewrite it in our form. `D = r × S`, so `S = 60,000 / 20 = 3,000` bytes per snapshot on average, and tripling `r` triples `D` with `S` unchanged. That division is ours, not Respawn's, and it is an average over whatever each snapshot happens to contain. Respawn also argues that 60 Hz would save only about two frames of input delay in the best case, for three times the bandwidth and CPU. The `1 / r` column of section 1 against the linear cost column is the same argument in numbers.

**Fiedler's cube demo (Gaffer on Games, 2015).** Fiedler's physics demo has 901 cubes and sends 60 snapshots per second. Uncompressed, each cube costs 40.125 bytes, which gives 17.37 Mbit/s. His target is 256 kbit/s. In our form, `k = 901` and `r = 60` are fixed, so the only lever left is `b`. The target needs `256,000 / 8 / 60 / 901 = 0.59` bytes per cube on average. No field-level packing gets a moving cube under one byte. Fiedler gets there by quantizing each cube to about 10 bytes and then sending deltas, so cubes at rest cost almost nothing. When `n` and `r` are fixed by the design, `b` is where the whole budget is won.

**Source engine (Valve documentation, archived 2023).** Source makes the per-client budget explicit. The client sets `rate`, its incoming limit in bytes per second, and server operators bound it with `sv_minrate` and `sv_maxrate`. The server never exceeds the client's rate. The documentation suggests 10,000 bytes/s for DSL and faster, and warns that modem players can receive only 5 to 7 KB/s. In our form it is a constraint, `r × S ≤ rate`. At the default 20 snapshots per second and `rate = 10,000`, a snapshot can average at most 500 bytes. If the world does not fit, something else has to give, which is section 4's topic.

**Valorant (Riot Games, August 2020).** Riot turned the tick rate into a CPU budget. At 128 ticks per second one tick lasts 7.8125 ms. To fit three games on each CPU core, and so 108 games and 1,080 players on a 36-core server, each game's tick had to finish in about 2.34 ms after overhead. The server started at about 50 ms per tick. Ten players make a small `n`, so Riot could spend the budget on a high `T`. A 60-player game with the same per-player cost could not.

**EVE Online (CCP, current mechanics).** EVE runs the opposite extreme. Its server aims for one tick per second, and thousands of pilots can share one star system. When a node is overloaded, EVE slows game time itself, down to 10% speed, which CCP announced as Time Dilation in a dev blog on 22 April 2011. The EVE University wiki notes that server load grows as `O(n²)` with players on grid. With `n` in the thousands, the only levers left are `r` and time. MMO302 takes this case apart in its weeks on tick rate for MMOs and on single-shard worlds ([MMO302 week 5](../../MMO302-mmo-server-architecture/lectures/w05-tick-rate-for-mmos-vs-shooters.md) and [week 12](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md)).

Five games, one formula. Before you pick a tick rate, write `U = n × r × (k × b + h × p)` with your own numbers and ask which letter you can afford to move.

### Design judgment

- **Choose the shape before the constants.** If your game has more than a few dozen players in one space, you need interest management, and no amount of compression will replace it. Compression buys a constant factor once. The cap buys a factor that grows with every player you add.
- **Budget per client first, then multiply.** The client's link is the one you do not control. Pick a ceiling (Fiedler's 256 kbit/s is a sensible starting point for action games) and design snapshots to fit it at your worst crowd density. The server total follows.
- **High tick rate is a luxury of small matches.** Ten players at 128 Hz and 60 players at 20 Hz can cost similar amounts. Spend rate where players can feel it, which is small, competitive matches with hitscan weapons.
- **Separate tick rate from snapshot rate when CPU is cheap and bandwidth is not.** Simulating at 60 Hz and sending at 20 Hz gives accurate physics and hit detection with a third of the bandwidth. The cost is a longer interpolation delay.
- **Budget the worst case, not the average.** Apex's 60 kB/s figure is for the start of a match. A late-game fight in a small circle packs more entities into view. Your cap `K` and your priority rules must hold at the densest moment your design allows.

### Check this example

1. A 64-player game sends 30 snapshots per second with 24 bytes per entity and no interest cap. Compute the packets per snapshot, the client download in kbit/s and the server upload in Mbit/s.
2. For the same game, what interest cap `K` keeps every client under 128 kbit/s?
3. The baseline 100-player server (65.8 Mbit/s) goes to 150 players. Estimate the new upload from the `n²` rule, then compute it exactly. Why do they differ?

<details>
<summary>Answers</summary>

1. Entity bytes `64 × 24 = 1,536`, so `p = ceil(1,536 / 1,252) = 2`, and `S = 1,536 + 56 = 1,592` bytes. `D = 30 × 1,592 = 47,760` B/s = 382.1 kbit/s. `U = 64 × 47,760 = 3,056,640` B/s = 24.45 Mbit/s.
2. `128,000 / 8 / 30 = 533.3` bytes per snapshot. With one packet, `24K + 28 ≤ 533.3`, so `K ≤ 21.05`. The cap is 21 entities (`S = 532` bytes, 127.7 kbit/s).
3. The rule gives `65.8 × (150/100)² = 148.0` Mbit/s. Exactly, `150 × 40 = 6,000` bytes needs 5 packets, `S = 6,140`, `D = 122,800` B/s, `U = 150 × 122,800 = 18,420,000` B/s = 147.4 Mbit/s. The small difference comes from headers, which grow with packet count, not with `n²`.

</details>

## 3. Tick rate is a CPU budget

Bandwidth is only half the bill. The server must also finish each tick before the next one starts.

```
tick interval   t = 1000 / T        (ms)
games per core  G = floor(t / c)     where c is the CPU time one game's tick takes
```

If a tick takes longer than `t`, the server falls behind. It can skip ticks, which makes the game jerk, or slow down, which is what EVE does on purpose. Neither is acceptable in a shooter, so shooters buy more hardware or cut work.

The cost of one tick is rarely one number. Split it by how it grows with `n`.

```
c(n) = a + d × n + e × n²
```

- `a` is fixed work per game (timers, game rules).
- `d × n` is per-player work: running each player's inputs, moving them, animating them.
- `e × n²` is per-pair work: checking who can see whom, who collides with whom, and writing each player into each snapshot.

Take invented costs for illustration: `a = 0.2` ms, `d = 0.1` ms and `e = 0.002` ms. Ten players cost `0.2 + 1.0 + 0.2 = 1.4` ms per tick, which fits five times into Valorant's 7.8 ms tick. Sixty players cost `0.2 + 6 + 7.2 = 13.4` ms. That misses a 7.8 ms tick badly but fits easily into a 50 ms tick at 20 Hz. The same code, the same per-player cost, and the larger game is forced to a lower tick rate by its own `n²` term.

Riot's post shows the other half of the job, which is cutting `a`, `d` and `e`. Animating characters on every fourth frame instead of every frame cut animation cost by 75%. Turning off animation during the buy phase cut a further third. Each is a per-player cost, so each saving scales with `n`.

## 4. When the snapshot does not fit

A budget is a promise, and sometimes the world breaks it. Twenty players pile into one room and `k × b` exceeds your per-client ceiling. You have four choices.

1. **Send it anyway.** The client's link queues or drops the excess. You get the lag spikes of week 2 at the worst possible moment.
2. **Lower the rate for this client.** Source does this. The server will not exceed the client's `rate`, so a full world is sent less often. Everything is equally stale.
3. **Drop the least important entities.** A pure interest cap. Distant players vanish until they come closer.
4. **Spread the entities over several snapshots by priority.** Every entity gets updated eventually, important ones more often.

Option 4 is what most modern netcode does, and Fiedler's "State Synchronization" article (2015) gives the simplest version, the **priority accumulator**. Every entity keeps a running number. Each tick, you add the entity's priority to it (high for the player you are aiming at, low for a crate across the map). You sort by the running number, fill the packet from the top until the byte budget runs out, and reset the running number of every entity you sent to zero. Entities that did not fit keep their total and climb the list, so even the lowest priority object is sent sooner or later.

```python
def fill_packet(entities, budget_bytes, bytes_per_entity):
    for e in entities:
        e.acc += e.priority
    entities.sort(key=lambda e: e.acc, reverse=True)
    chosen = entities[: budget_bytes // bytes_per_entity]
    for e in chosen:
        e.acc = 0.0
    return chosen
```

Take two classes of entity. Eight near entities have priority 1.0 and 24 far entities have priority 0.25, with room for 12 per packet. If every entity were sent at the rate its priority suggests, near ones every tick and far ones every 4 ticks, you would need `8 + 24 / 4 = 14` slots per tick. You have 12, so both classes slip. Run the code for 12,000 ticks and each near entity is sent every 1.11 ticks on average and each far entity every 5 ticks. Check the total, `8 / 1.11 + 24 / 5 = 7.2 + 4.8 = 12` slots. Nobody starves, and the shortfall is shared in proportion to priority. The accumulator lets you state the budget as bytes and the policy as priorities, and it works out the rates itself.

## In-class activity (25 minutes)

Pairs. Each pair gets one game card: a 2v2 arena brawler, a 40-player survival sandbox, a 100-player battle royale, or a city hub in an MMO with 300 players visible at peak.

1. Pick `r`, `b` and `K` (or no cap) and justify each in one sentence. Use `b = 40` unless you name the week 5 or week 7 technique that lowers it.
2. Compute the client download and the server upload at your card's peak player count. Show the packets per snapshot.
3. State your per-client ceiling. Does your design fit it at peak? If not, choose one of the four options from section 4.
4. Compute the latency your chosen `r` adds (section 1 table) and say whether players of that genre will feel it.

Expected output: one index card with the five numbers (`r`, `b`, `K`, client kbit/s, server Mbit/s), the ceiling, the fix, and a one-line defense. Two pairs with the same card compare and argue.

## Common misconceptions

- **"Higher tick rate is always better."** It lowers latency by a shrinking amount (`1 / r`) and costs CPU and bandwidth in a straight line. A 60-player game at 128 Hz may cost more than it is worth.
- **"Tick rate and send rate are the same number."** They are two settings. Many games simulate faster than they send, and the server can never send faster than it ticks.
- **"Compression solves the bandwidth problem."** It divides the curve by a constant. Without interest management, the `n²` catches up with any constant as the player count grows.
- **"Bandwidth is the server's problem."** The client's download grows as `n` without a cap, and the client's link is the one you cannot upgrade.

## Check yourself

1. A game ticks at 64 Hz. How long is one tick? If a game's tick costs 4.5 ms, how many games fit on one core?
2. Using the section 2 model with `n = 12`, `r = 64`, `b = 40`, no cap, compute the client download in kbit/s. Compare it with the Source `rate` setting of 10,000 bytes/s. Does it fit?
3. A designer wants 300 players in one city hub at `r = 20` and `b = 16`. What server upload does the hub need without a cap, and with `K = 48`?
4. Moving from 30 Hz to 60 Hz, how many milliseconds of the "total from the rate" do players save, and by what factor does bandwidth grow?
5. In section 4's accumulator example, the budget rises to 16 entities per packet. About how often is each far entity sent now?

<details>
<summary>Answers</summary>

1. `1000 / 64 = 15.625` ms. `floor(15.625 / 4.5) = 3` games per core.
2. `12 × 40 = 480` bytes, 1 packet, `S = 508` bytes. `D = 64 × 508 = 32,512` B/s = 260.1 kbit/s. That exceeds 10,000 B/s by a factor of 3.25, so a Source-style server would not send all 64 snapshots per second to that client.
3. Without a cap, `300 × 16 = 4,800` bytes needs 4 packets, `S = 4,912`, `D = 98,240` B/s, `U = 300 × 98,240 = 29,472,000` B/s = 235.8 Mbit/s. With `K = 48`, `48 × 16 = 768` bytes, 1 packet, `S = 796`, `D = 15,920` B/s, `U = 4,776,000` B/s = 38.2 Mbit/s.
4. `83.3 − 41.7 = 41.7` ms saved. Bandwidth doubles.
5. 16 slots exceed the 14 the priorities ask for, so near entities go every tick and take 8 slots. The other 8 slots serve 24 far entities, so each is sent every `24 / 8 = 3` ticks, more often than its priority alone would ask. (The simulation in section 4 gives exactly 1.0 and 3.0.)

</details>

## Lab / assignment hook

[Lab 13, bandwidth budget](../labs/lab13.md). You implement the section 2 model, check it against the tables in this lecture, add a grid-based interest cap to a 500-player scatter of positions, and then measure real snapshot sizes from a small `struct`-based encoder at two precisions. Deliverable: the finished `budget.py`, a CSV sweep, a plot of server upload against `n`, and a one-page budget for a game of your choice.

## Sources

- Valve Developer Community, "Source Multiplayer Networking" (archived copy, December 2023). Tick rates 66 (*Counter-Strike: Source*, *Day of Defeat: Source*, *Team Fortress 2*), 64 default (*CS:GO*), 60 (*Counter-Strike*, GoldSrc) and 30 (*Left 4 Dead*, *Left 4 Dead 2*). `cl_updaterate` default 20, command packets usually 30 per second, no more snapshots than ticks. Client `rate` in bytes per second, `sv_minrate` and `sv_maxrate`, 10,000 suggested for DSL and above, modem players limited to 5 to 7 KB/s.
- Respawn Entertainment, "What Makes Apex Tick: A Developer Deep Dive into Servers and Netcode" (Apex Legends news, ea.com, 28 April 2021). 20 Hz server, about 60 kB/s at the start of a match, about 180 kB/s at 60 Hz, the "two frames" argument about triple bandwidth and CPU.
- Electronic Arts, "About Apex Legends" (ea.com, accessed September 2026). "Play in classic 60-person Battle Royale matches."
- Randall, B. "VALORANT's 128-Tick Servers" (Riot Games, 31 August 2020). 7.8125 ms per tick, 2.34 ms target per game, three games per core, 108 games and 1,080 players on a 36-core host, a starting cost of 50 ms, the animation savings.
- Fiedler, G. "Snapshot Compression" (Gaffer on Games, 4 January 2015). 901 cubes, 60 Hz, 40.125 bytes per cube, 17.37 Mbit/s uncompressed, 256 kbit/s target.
- Fiedler, G. "State Synchronization" (Gaffer on Games, 5 January 2015). The priority accumulator and the 256 kbit/s budget.
- EVE University Wiki, "Server tick" and "Time dilation" (accessed September 2026). One tick per second, time dilation down to 10% speed, server load `O(n²)` in players on grid. CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), read directly: load in large fights is mostly tied to the game clock, so slowing time lowers it. The 10% floor comes from the wiki, not the blog.

## Interactive spec: examples/w13-bandwidth-budget.html

**Insight the visual must make obvious:** shrinking bytes per entity, headers or send rate moves the server's bandwidth curve down by a constant factor without changing its shape, while an interest cap changes the curve from a parabola into a straight line. At large player counts only the cap matters.

**Layout.** Two linked views and a number panel. Desktop: the two views side by side, panel beneath. Under 700 px: stacked, left view first.

1. **Server view (left).** x axis: players `n`, 2 to 1,000 (linear, with a toggle for log-log). y axis: server upload in Mbit/s. Two curves: "no cap" (`k = n`) and "cap K" (`k = min(n, K)`), both computed with the current `r`, `b`, `h`, `M`. When the cap is off, draw only the first curve. A horizontal dashed line for the server link (selector: 100 Mbit/s, 1 Gbit/s default, 10 Gbit/s). Mark the crossing point with a label, "wall at n = 390". A vertical cursor at the current `n`, with dots on both curves. On the log-log toggle, label the slopes "slope 2" and "slope 1" so students read the exponent.
2. **Client view (right).** One bar for the client download at the current `n`, and a ghost bar for the other mode (cap on or off). Horizontal lines at 1 Mbit/s ("mobile") and 10 Mbit/s ("home"), plus a user-set ceiling line (default 256 kbit/s). The bar is red when above the ceiling.
3. **Number panel.** `k`, packets per snapshot `p`, snapshot bytes `S`, client download in B/s and kbit/s, server upload in B/s and Mbit/s, GB per match-hour, entity records per second (`n × k × r`), and the "total from the rate" latency `500 / r + 2000 / r` ms.

**Controls.**
- Slider `n`, 2 to 1,000, step 1, default 100.
- Slider `r`, 1 to 128 Hz, default 20. Preset buttons 10, 20, 30, 60, 128.
- Slider `b`, 1 to 64 bytes, default 40.
- Interest cap: toggle (default off) and slider `K`, 4 to 128, default 32.
- Header `h`, number field, default 28. MTU `M`, number field, default 1,280.
- Button "Apply levers A to D" steps through the lecture's lever table (A: r 20, b 40, cap off; B: b 16; C: cap 32; D: r 10), updating everything and showing the "saved vs baseline" percentage.
- All sliders keyboard accessible (arrows ±1, Page Up/Down ±10).

**Formulas.** `k = cap ? min(n, K) : n`. `p = max(1, ceil(k·b / (M − h)))`. `S = k·b + h·p`. `D = r·S`. `U = n·D`. kbit/s `= 8·x / 1000`, Mbit/s `= 8·x / 1e6`. GB per hour `= U·3600 / 1e9`. Wall: smallest `n` where `U(n)` in Mbit/s exceeds the link, reported as that `n` minus 1.

**Test values** (assert on load, `r = 20`, `b = 40`, `h = 28`, `M = 1,280`).
- `n = 100`, no cap: `p = 4`, `S = 4,112`, `D = 82,240` B/s (657.9 kbit/s), `U = 8,224,000` B/s (65.79 Mbit/s), 29.61 GB/h, 200,000 records/s.
- `n = 50`, `K = 32`: `S = 1,336`, `D` 213.8 kbit/s, `U` 10.69 Mbit/s.
- `n = 1,000`, no cap: `p = 32`, `U` 6,543.4 Mbit/s. With `K = 32`: 213.76 Mbit/s.
- Wall with a 1 Gbit/s link and no cap: `n = 390`. Client over 1 Mbit/s with no cap from `n = 153`.
- Levers at `n = 100`: A 65.79, B 26.50, C 8.64, D 4.32 Mbit/s. `r = 60`, `b = 40`, no cap: 197.38 Mbit/s.

**First screen:** `n = 100`, cap off, with the cap curve drawn faintly as a preview, and a caption: "100 players at 20 Hz: 65.8 Mbit/s. Double the players and it quadruples. Turn on the interest cap to see the curve straighten."
