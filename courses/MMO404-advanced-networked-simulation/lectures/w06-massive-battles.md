# MMO404 · Week 06 — Massive battles

**Why this matters:** Every technique in weeks 3 to 5 assumes that most of the world is far from most players. A massive battle breaks that assumption on purpose. When a thousand players stand in one place and everyone can see everyone, interest management stops helping, and the costs you tamed return in their `n²` form. MMO302 showed how time dilation keeps the server's CPU in budget. This week is about the other two bills a battle runs up, the stream of combat events each player must receive, and the price of the one design that avoids sending state at all.

**You will be able to:**
- Compute a battle's combat-event fan-out per client and for the server, with and without MMO302's time-dilation factor.
- Explain why dilation shrinks each client's event stream once the pair term dominates, and where that stops.
- Compare full fan-out, per-observer aggregation and deterministic lockstep for a large battle, with numbers for each.
- Model how fast a determinism error grows, demonstrate it in code, and critique lockstep as a design for an MMO battle.

**Before class:** Reread [MMO302 week 12](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md), section 2, on the dilation model, and [CS202 week 12](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md), section 3, on the sources of non-determinism. Phil Savage, "Planetside 2 breaks world record for most players in an FPS battle" (PC Gamer, 26 January 2015), a short news item. Epic Games, "Replication Graph" (Unreal Engine 4.27 documentation), the overview.

**Prerequisites from earlier courses:** [MMO302 week 12, single-shard architectures and time dilation](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md) (the cost model `W(n) = a n + b n²`, the dilation factor `f = clamp(C / W(n), f_min, 1)` and its thresholds; this lecture uses them without deriving them again). [CS202 week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) (commands instead of state, the four sources of non-determinism, per-turn checksums). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (per-client bandwidth budgets). [MMO404 week 4](w04-replication-prioritization-and-relevancy.md) (fair share and the water level `λ`) and [week 5](w05-bandwidth-shaping-and-lod-for-networking.md) (aggregation and shaping).

**Interactive:** [w06-massive-battle.html](../examples/w06-massive-battle.html). Keep it open during sections 2 and 3.

---

## 1. What changes when everyone is in range

Interest management works because relevance is sparse. In an ordinary zone, a player sees a few dozen of the thousands of entities on the server, so each client's stream grows with local density, not with the server's population. A battle is local density taken to its limit. Every participant is within weapon range of many others, every participant cares about the fight's state, and the design wants all of them there.

Three costs return in that situation.

1. **Per-tick CPU.** MMO302 week 12 wrote the cost of simulating one game-second as `W(n) = a n + b n²`. The `b n²` term covers pair work: range checks, targeting, collision, and writing each participant into each observer's view. Spatial partitioning (week 3) keeps pair work low when participants are spread out. In a battle they are not, so the pairs are real. MMO302 showed how time dilation keeps this cost inside the node's capacity.
2. **Event fan-out.** A battle is full of discrete events: an ability fires, damage lands, a heal lands, a ship explodes. Each event has one source and potentially `n` observers. If `n` participants each cause `r` events per second and every event goes to everyone, the server sends `n × r × n` event copies per second.
3. **The state stream.** Week 4's water level `λ` falls as the total priority in view rises. With `n` participants all near, `λ` falls about as `1 / n`, so every entity gets staler as the fight grows.

A shooter with 100 players faces these costs too, but at 100 they fit. The question for an MMO is what happens at 1,000 or 3,000, and the answer is that something the players can feel has to give. This lecture is about the second cost and about lockstep, the design that claims to avoid it.

## 2. Worked example: every shot to every witness

### The hook

On 24 January 2015, 1,158 PlanetSide 2 players fought in one battle on the game's Jaeger event server. Guinness World Records recognised it as the most players in an online FPS battle, beating the 999 of Man vs. Machine. The organisers' battle report counted 53,729 kills, 3,822 of them team kills, and 31 base captures.

Every one of those kills had one killer and, in a crowd that dense, hundreds of witnesses whose screens had to show it. A shooter cannot slow its clock the way EVE does, because its players feel every hundred milliseconds. So how many bytes does one player's connection have to carry when a thousand people are shooting within sight of each other? And what, other than a faster connection, could make that number smaller?

### The model

Each participant causes `r` combat events per game-second, each `k` bytes on the wire. If every event goes to every participant, one client receives

```
full stream per client = n × r × k          bytes per game-second
server total           = n² × r × k
```

We use `r = 2` events per second and `k = 12` bytes, both invented but modest.

Dilation changes the denominator. From MMO302 week 12, a node whose work `W(n)` exceeds its capacity `C` runs the game at speed `f = clamp(C / W(n), f_min, 1)`. Everything that happens per game-second then happens `f` times per real second, and that includes the events. So the stream a client actually receives is

```
dilated stream per client = f × n × r × k    bytes per real second
```

We do not derive `f` again. We take MMO302's teaching node as it is: `a = 0.3` ms, `b = 1` µs, `C = 1`, `f_min = 0.1`. With those constants dilation starts at 861 pilots and reaches the floor at about 3,016.

The third line is **aggregation**. Each client receives its own **circle** in full (itself, its target, its squad, whoever is shooting it, `circle = 20` entities), and everything else as one summary per squad of 10 per real second, 8 bytes each (squad health, position, count).

```
aggregated stream = f × circle × r × k + (n / squad) × summary
```

### Numbers you can check

```python
A, B, C, FLOOR = 0.0003, 0.000001, 1.0, 0.1   # MMO302 week 12's node

def work(n):
    """CPU-seconds to simulate one game-second with n pilots."""
    return A * n + B * n * n

def speed(n):
    """MMO302's time-dilation factor f: game-seconds per real second."""
    return max(FLOOR, min(1.0, C / work(n)))

def stream_Bps(n, f, r=2.0, k=12, circle=None, squad=10, summary=8):
    """Combat-event bytes per real second that one client receives."""
    if circle is None:                     # every event to everyone
        return f * n * r * k
    full = f * circle * r * k              # own circle in full, at game speed
    reports = (n / squad) * summary        # one summary per squad per real second
    return full + reports

kb = lambda Bps: Bps * 8 / 1000
print(f"{'pilots':>6} {'speed':>6} {'all events':>11} {'dilated':>9} {'aggregated':>11}")
for n in [100, 500, 1000, 2000, 3000, 4000]:
    f = speed(n)
    print(f"{n:6d} {f:6.1%} {kb(stream_Bps(n, 1.0)):8.0f} kb {kb(stream_Bps(n, f)):6.0f} kb "
          f"{kb(stream_Bps(n, f, circle=20)):8.1f} kb")
```

```
pilots  speed  all events   dilated  aggregated
   100 100.0%       19 kb     19 kb      4.5 kb
   500 100.0%       96 kb     96 kb      7.0 kb
  1000  76.9%      192 kb    148 kb      9.4 kb
  2000  21.7%      384 kb     83 kb     13.6 kb
  3000  10.1%      576 kb     58 kb     19.6 kb
  4000  10.0%      768 kb     77 kb     26.0 kb
```

The columns are kbit/s per client. Check two rows by hand.

- **1,000 pilots.** Events per client at full speed are `1,000 × 2 × 12 = 24,000` B/s, which is 192 kbit/s. The server sends `1,000 × 24,000 = 24` MB/s, 192 Mbit/s, of events alone. MMO302's node runs at `f = 1 / 1.3 = 76.9%`, so the client actually receives `0.769 × 192 = 148` kbit/s.
- **3,000 pilots.** Full fan-out would need 576 kbit/s per client. The node runs at `1 / 9.9 = 10.1%`, so the dilated stream is `0.101 × 576 = 58` kbit/s. Aggregated, the circle costs `0.101 × 20 × 2 × 12 = 48.5` B/s and the summaries `300 × 8 = 2,400` B/s, 19.6 kbit/s in all.

Three things stand out.

**Full fan-out grows with `n` per client and with `n²` at the server.** Every pilot you add is one more source for every client and one more client for every source. A thousand pilots already cost 192 Mbit/s of events at the server before a single position update.

**Dilation shrinks each client's stream.** Look at the "dilated" column. It rises until dilation starts at 861 pilots, where it peaks at `861 × 24 = 20,664` B/s, about 165 kbit/s. Then it *falls*: 148, 83, 58. Once the pair term dominates, `f ≈ C / (b n²)`, so the stream `f × n × r × k ≈ C r k / (b n)` falls as `1 / n`. A bigger battle sends each player fewer events per real second, because each event takes longer to happen. MMO302 introduced dilation to protect the CPU. As a side effect it protects every client's connection.

**Past the floor, the stream climbs again.** At 4,000 pilots `f` is stuck at 10%, so the stream grows with `n` once more, 58 to 77 kbit/s, and MMO302's backlog grows with it. The floor is where both protections end together.

### What the players pay

The dilated stream is cheap because the game is slow. At `f = 0.101`, a module that cycles every 5 game-seconds cycles every 50 real seconds. Nothing is lost and nothing is out of order, but the game is ten times less responsive. A shooter has no such trade available. PlanetSide 2's 1,158 players had to receive their fight at full speed, so the only levers left were what to send (aggregation and relevance) and how many players to admit.

### The other lever: send less per event

Aggregation turns the per-client stream from "everyone's events" into "my circle's events plus a report on the rest". It still grows with `n`, through the summaries, but with a slope of 0.8 bytes per pilot per real second instead of 24 bytes per pilot per game-second. At 3,000 pilots the circle is 48.5 B/s and the summaries are 2,400 B/s: nearly all of the aggregated stream is the report on the rest, so the squad size is the setting that matters.

Aggregation and dilation solve different problems. Aggregation fixes the network. It does nothing for the CPU, because the server still simulates every pair. Dilation fixes the CPU, and as a side effect it limits the network. A large battle in a slow game needs both. A large battle in a fast game gets only aggregation.

### Move it yourself

Open `examples/w06-massive-battle.html`. The left chart plots each client's event stream against pilots in three lines: full fan-out, full fan-out with MMO302's dilation, and aggregated with dilation. A gauge above it shows the dilation percentage. Start at 500 pilots and drag to 5,000. Watch the dilated line peak at 861, bend down while the full fan-out line keeps climbing, then turn up again past the floor at 3,016. Switch dilation off, as a shooter must, and the middle line lies on the top one. Then change the squad size and watch only the aggregated line move. The right panel belongs to section 3.

### Same idea elsewhere

**EVE Online (CCP, time dilation since 2011, current rules).** The EVE University wiki describes dilation down to a floor of 10% speed on an overloaded node, and notes that server load grows as `O(n²)` in players on grid. In our model, every event stream on that node is multiplied by `f`. EVE's players receive a thousand-pilot fight through an ordinary connection because the fight itself runs slowly.

**Age of Empires (Ensemble Studios, 1997; postmortem 2001).** [CS202 week 12](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) worked through how Age of Empires sent commands instead of unit state. Rewrite it in this lecture's form. The stream per client is `(players − 1) × commands per second × bytes per command`, and the unit count `n` does not appear at all. That is the extreme form of "send less per event". Section 3 is about its price at MMO scale.

**Fortnite and Unreal's Replication Graph (Epic Games, Unreal Engine 4.27 documentation).** Epic's documentation gives Fortnite Battle Royale as the motivating case: 100 connected players and about 50,000 replicated actors per match. The Replication Graph groups actors into nodes so the server builds each client's list from shared buckets instead of testing every actor against every connection. In our form, that attacks the server-side cost of deciding who sees what, the `n²` of the fan-out, and it feeds week 4's priority allocator. It does not change `r` or `k`.

**PlanetSide 2 (the hook).** A shooter with `f` fixed at 1. Its record crowd of 1,158 is well above the 861 pilots at which our teaching node would start to dilate, and it had to be served at full speed.

Four games, one model with a few knobs. EVE turns `f`. PlanetSide 2 and battle royales cap `n`. Age of Empires changes what an event is. Fortnite makes the choice of recipients cheaper. Each studio chose the knob its players would tolerate.

### Design judgment

- **Pick the currency your players will pay in.** Strategy players accept slow time (EVE) and input delay of a few hundred milliseconds (Age of Empires, as CS202 week 12 showed). Shooter players accept neither, so they must accept caps and aggregation. Ask which one your genre forgives before you pick a technique. [Week 7](w07-time-dilation-revisited.md) takes the dilation controller further.
- **Aggregate what the player cannot act on.** A pilot needs its circle in full detail. It needs the other 3,000 as a situation report. Decide the circle's membership with gameplay rules (week 4's weights) and make it explicit, since players notice when an ally they are healing drops out of it.
- **Size summaries, not events.** Past a few hundred pilots, summaries are almost all of the aggregated stream. The squad size and the summary rate are your real budget settings.
- **Attack the pair term, not the per-pilot term.** Halving `b` moves MMO302's floor from 3,016 to 4,182 pilots, about `√2` further. Halving `a` moves it only to 3,088.
- **Design battles to spread.** Several objectives, spaced out, turn one `n²` into several smaller ones and give week 3's partition something to split. That is a map design decision, not a netcode one, and it is often the cheapest fix.

### Check this example

1. At what pilot count does the dilated full fan-out stream peak on MMO302's node, and how large is it in kbit/s? Explain why the peak is there.
2. For 2,500 pilots, compute `f`, the full fan-out stream and the dilated stream, in kbit/s.
3. At 3,000 pilots, what squad size keeps the aggregated stream under 12 kbit/s, with 8-byte summaries once per real second?

<details>
<summary>Answers</summary>

1. At 861 pilots, where dilation starts. Below it `f = 1` and the stream grows with `n`. Above it `f × n = C n / (a n + b n²) = C / (a + b n)`, which falls as `n` grows. The peak is `861 × 2 × 12 = 20,664` B/s, about 165 kbit/s.
2. `W(2,500) = 0.75 + 6.25 = 7.0`, so `f = 1 / 7 = 14.3%`. Full fan-out is `2,500 × 2 × 12 = 60,000` B/s, 480 kbit/s. Dilated, `480 / 7 = 68.6` kbit/s.
3. 12 kbit/s is 1,500 B/s. The circle takes `0.101 × 20 × 24 = 48.5` B/s, leaving 1,451.5 B/s for summaries. Summaries cost `(3,000 / squad) × 8` B/s, so `squad ≥ 24,000 / 1,451.5 = 16.5`. Squads of 17 or more.

</details>

## 3. Lockstep and determinism error

Age of Empires shows that a battle's network cost need not depend on its size at all. So why do MMOs not use lockstep for their battles? CS202 week 12 taught how lockstep works and where non-determinism leaks in. This section asks what those leaks cost at MMO scale.

### What lockstep demands

In lockstep, each machine runs the whole simulation from the same starting state and the same ordered list of commands. For an MMO battle, four demands follow.

1. **Every machine simulates everything.** In an RTS with 8 players, each PC runs all the units. In an MMO battle with 3,000 players, each client would run 3,000 pilots, including their full pair work. The server's CPU problem, the one MMO302 solved with dilation, becomes every client's problem, on hardware you do not control.
2. **Everyone waits for the slowest.** A turn cannot run until every command for it has arrived. With 8 players that is tolerable. With 3,000, one player on a bad connection stalls everybody.
3. **Every machine sees everything.** Each client holds the full state, so hidden information (stealth, fog of war, an enemy fleet's composition) is readable by anyone who inspects memory. In an MMO, where the server is the only trusted party ([MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md)), that is a cheat waiting to happen.
4. **The simulation must be bit-for-bit deterministic on every machine.** CS202 listed the leaks: floating-point order, random number generators, iteration order and local-only state. With 8 PCs you can pin one build per platform. With 3,000 clients on every operating system and CPU a player might own, every leak is live.

### Determinism error, in code

Floating-point addition is not associative, as CS202 showed. Here is what that does to a battle when two machines add the same hits in a different order.

```python
import hashlib, struct

print((0.1 + 0.2) + 0.3, 0.1 + (0.2 + 0.3))

def add_all(values):
    total = 0.0
    for v in values:          # plain left-to-right adds, as a C++ loop would do
        total += v
    return total

def battle(order, ticks):
    """1,000 units trade damage; each machine adds up incoming hits in its own order."""
    hp = [100.0] * 1000
    for t in range(ticks):
        new = []
        for i in range(1000):
            hits = [0.1 * ((i * 7 + k * 13 + t) % 10 + 1) for k in range(5)]
            dmg = add_all(hits if order == "forward" else reversed(hits))
            new.append(hp[i] - dmg * hp[(i + 1) % 1000] / 100.0)
        hp = new
    return hp

def checksum(hp):
    return hashlib.sha1(struct.pack(f"{len(hp)}d", *hp)).hexdigest()[:8]

for ticks in (1, 10, 40):
    a, b = battle("forward", ticks), battle("reverse", ticks)
    gap = max(abs(x - y) for x, y in zip(a, b))
    print(f"tick {ticks:2d}  checksums {checksum(a)} {checksum(b)}  largest gap {gap:.1e} hp")
```

```
0.6000000000000001 0.6
tick  1  checksums 4e11cb83 4e11cb83  largest gap 0.0e+00 hp
tick 10  checksums 4d13d47f 9e20d09d  largest gap 1.4e-14 hp
tick 40  checksums 9bb895fd 4b8a1ba1  largest gap 2.1e-14 hp
```

After one tick the two machines agree. By tick 10 they differ by `1.4 × 10⁻¹⁴` hit points, which no player could see, and their checksums no longer match. In a lockstep game that is already a desync. The gap stays tiny here because this toy battle is gentle: nothing in it amplifies a difference. Real simulations have thresholds (a unit dies at 0 hp, a projectile hits or misses, a pathfinder picks the left or right route) and chaotic interactions that grow a small difference fast.

### How fast an error grows

Here is a model you can use. In a chaotic update, a small gap between two machines grows by roughly a constant factor `g` per tick. A gap that starts at `ε` reaches a visible size `v` after

```
ticks to visible = ln(v / ε) / ln(g)
```

The next block measures `g` for a simple chaotic update, starting from a gap of `10⁻¹⁵`, about the size of one rounding difference.

```python
import math

x, y = 0.4, 0.4 + 1e-15             # two machines, one bit apart
visible = None
for step in range(1, 61):
    x, y = 3.9 * x * (1 - x), 3.9 * y * (1 - y)
    if visible is None and abs(x - y) > 0.01:
        visible = step
    if step % 15 == 0:
        print(f"step {step:2d}  gap {abs(x - y):.1e}")

g = (abs(x - y) / 1e-15) ** (1 / 60)    # average growth per step
print(f"growth {g:.2f} per step; model says {math.log(0.01 / 1e-15) / math.log(g):.0f} steps "
      f"to a 0.01 gap; the run crossed it at step {visible}")
```

```
step 15  gap 2.0e-12
step 30  gap 4.1e-08
step 45  gap 9.0e-05
step 60  gap 3.7e-01
growth 1.75 per step; model says 54 steps to a 0.01 gap; the run crossed it at step 52
```

The gap grows by about 1.75 per step, and the model's 54 steps is within two of the measured 52. The logarithm is the point. Making the first error a thousand times smaller buys only `ln(1,000) / ln(1.75) ≈ 12` more ticks. At 20 ticks per second, 54 ticks is under three seconds. Flocking, collision response and physics stacks behave like this. A single bit of disagreement becomes a unit in a different place within seconds, and no amount of "almost deterministic" code changes the order of magnitude.

This also tells you why a checksum has to fire at the first differing bit rather than at a visible difference. By the time players can see a desync, the two worlds have been diverging for dozens of ticks, and CS202's hunt for the first bad turn starts that much further from the cause.

One more lesson hides in the battle code. It uses an explicit loop instead of Python's built-in `sum`. Since Python 3.12, `sum` of floats uses compensated (Neumaier) summation, which makes the result less sensitive to order. A program that summed damage with `sum` would give different bits on Python 3.11 and 3.12. A library update changed floating-point results. In a lockstep game with 3,000 clients, that is a desync between players on different versions, and it is why lockstep games pin compilers, flags and math libraries, or use fixed-point integer arithmetic for everything that affects game state.

### Where lockstep belongs in an MMO

Lockstep is wrong for the whole battle and right for parts of it. Things that are deterministic, visible to everyone and cheap to simulate can be sent as seeds and commands instead of state: a volley of cosmetic projectiles from a seed, a debris field from a seed and a time, an NPC formation from its orders. If one of those diverges after 54 ticks, nobody loses a ship. The server stays authoritative for everything that decides outcomes, and uses lockstep-style "send the cause, not the result" for everything that only needs to look right.

## 4. Other levers for the largest fights

Section 2 covered fan-out and aggregation, and MMO302 covered dilation. Studios use a few more, usually in combination.

- **Caps and queues.** Limit the number of players in one space and queue the rest. Honest and cheap, but players hate being locked out of the fight they came for. Pair it with in-world reasons (a limited number of docking slots, a gate that holds so many ships).
- **Splitting the battle across processes.** Assign parts of the battlefield to different processes or machines and hand work across boundaries ([week 2's handoff](w02-seamless-worlds-and-boundary-handoff.md), and week 9's meshing). This splits the `a n` term well. It splits the `b n²` term only for pairs that straddle no boundary, which in a dense fight is few, so it helps less than it seems.
- **Coarser pair work.** Replace exact range checks with range bands, recompute targeting every few ticks, and cap the number of targets any one attacker can engage. Each cuts `b`, which moves the ceiling by roughly the square root of the saving.
- **Scheduled capacity.** When a studio knows a fight is coming, it can move the battle onto a dedicated, faster node ahead of time, which raises `C`. Week 7 works through what that buys and why it depends on knowing in advance.
- **Designing the fight's shape.** Multiple objectives, structures with timers that spread engagements, and rewards for small-group play all reduce the peak `n` in any one place. The best netcode for a 3,000-player fight is sometimes a design that makes it three fights of 1,000.

## In-class activity (25 minutes)

Groups of three. Each group gets one design brief: a fantasy siege for 800 players with catapults and spell effects, a space battle for 3,000 pilots with fleets and target locks, or a shooter-style frontline for 1,500 soldiers.

1. Choose `r`, `k`, and whether dilation is allowed at all. If it is, use MMO302's node or your own `a`, `b` and `C`. Justify each choice in one sentence using your genre.
2. With the interactive's custom mode, find the per-client full fan-out stream at your target size, with and without dilation. If dilation is not allowed, find the largest `n` that fits a 256 kbit/s event budget.
3. Choose an aggregation scheme (who is in the circle, what a summary contains, how often) and compute the per-client stream at your target size.
4. Name one thing in your brief that could run as lockstep-style "send the cause", and one that must never. For the first, estimate how many ticks a one-bit error takes to become visible, using `g = 1.75`.

Expected output: a half-page sheet with the numbers from steps 2 and 3, the circle definition, and the two items from step 4. Groups with different briefs compare which knob each had to turn.

## Common misconceptions

- **"Interest management solves large battles."** It solves large worlds. In a battle everyone is relevant to everyone, so the relevant set is the whole battle and the `n²` returns.
- **"Dilation only helps the CPU."** Every event per game-second arrives `f` times per real second, so dilation also shrinks each client's event stream, until the floor.
- **"Lockstep scales to any number of units, so it should scale to any number of players."** Its bandwidth is independent of units, but it depends on players (commands), waits for the slowest player, trusts every client with every secret and needs bit-exact determinism on every machine.
- **"A smaller floating-point error buys a lot of time."** Error in a chaotic update grows geometrically, so a thousand times smaller error buys only about a dozen ticks. Determinism is all or nothing.

## Check yourself

1. A shooter cannot dilate. At PlanetSide 2's record of 1,158 players, if each player causes 3 events per second of 16 bytes and every event goes to everyone, what does each client receive in kbit/s, and what does the server send in total, in Mbit/s?
2. Under full fan-out with dilation, the per-client stream is `f × n × r × k`. Show that once the pair term dominates and `f` is above its floor, doubling `n` roughly halves the per-client stream.
3. A lockstep simulation's worst subsystem grows a gap by 1.5 per tick. A one-bit error starts at `10⁻¹⁶`, and players notice a gap of `10⁻³`. How many ticks until players notice, and how many seconds at 20 ticks per second?
4. Give two independent reasons, each enough on its own, why a 3,000-player MMO battle should not run as pure lockstep.

<details>
<summary>Answers</summary>

1. Per client `1,158 × 3 × 16 = 55,584` B/s, about 445 kbit/s. The server sends that to 1,158 clients, `64,366,272` B/s, about 515 Mbit/s of events alone.
2. With pair work dominant, `W(n) ≈ b n²`, so `f ≈ C / (b n²)`. Then `f × n × r × k ≈ C r k / (b n)`, which is proportional to `1 / n`. Doubling `n` halves it.
3. `ln(10⁻³ / 10⁻¹⁶) / ln(1.5) = ln(10¹³) / ln(1.5) = 29.9 / 0.405 ≈ 74` ticks, about 3.7 seconds at 20 ticks per second.
4. Any two of: every client would have to simulate all 3,000 pilots including the pair work; every turn would wait for the slowest of 3,000 connections; every client would hold hidden information and could read it; every client would have to be bit-exact with every other on hardware and software the studio does not control, and any error becomes visible within seconds.

</details>

## Lab / assignment hook

[Lab 06, battle budget](../labs/lab06.md). You implement MMO302's work and speed functions and this week's event-stream model, check them against this lecture's table, then run seeded battles where you count the pairs really in weapon range and measure speed and per-client bytes under full fan-out and under your own aggregation scheme. A second part asks you to find and fix a determinism bug in a small lockstep simulation using checksums. Deliverable: your `battle.py` and `lockstep.py`, a CSV of the battle run, and a one-page battle plan.

## Sources

- Savage, P. "Planetside 2 breaks world record for most players in an FPS battle" (PC Gamer, 26 January 2015). 1,158 players in one battle on 24 January 2015, beating Man vs. Machine's 999; organised by the community site PlanetSide Battles; 53,729 kills, 3,822 team kills and 31 base captures in the battle report.
- Wikipedia, "PlanetSide 2" (accessed September 2026). The Guinness World Record for most players in an online FPS battle, 24 January 2015, on the Jaeger server, citing Guinness World Records news of 23 January 2015 and GameSpot.
- EVE University Wiki, "Time dilation" (accessed September 2026, current mechanics). Dilation to a floor of 10% speed on an overloaded node; server load `O(n²)` in players on grid.
- MMO302 week 12 (this program). The cost model `W(n) = a n + b n²` with `a = 0.3` ms, `b = 1` µs, `C = 1`, floor 0.1, and its thresholds of 861 and 3,016 pilots.
- Bettner, P. and Terrano, M. "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond" (Gamasutra, 22 March 2001; now on gamedeveloper.com), as worked through in CS202 week 12. Commands instead of unit state.
- Epic Games, "Replication Graph" (Unreal Engine 4.27 documentation). Fortnite Battle Royale with 100 connected players and about 50,000 replicated actors; actors grouped into nodes to build each connection's replication list.
- Python Software Foundation, "What's New In Python 3.12" (Python documentation). `sum()` uses Neumaier summation for floats.

## Interactive spec: examples/w06-massive-battle.html

**Insight the visual must make obvious:** full fan-out grows with every pilot; MMO302's time dilation makes each client's event stream peak where dilation starts and shrink as the battle grows, until the floor; and in lockstep, a one-bit disagreement grows geometrically until it is visible, so determinism is all or nothing.

**Layout.** Two panels. Left, "Fan-out": a gauge and the event-stream chart. Right, "Determinism": the error-growth chart. Desktop: side by side, left panel wider (about 60%). Under 700 px: stacked, fan-out first. A number panel sits under each chart.

**Fan-out model (must match section 2).**
- `W(n) = a n + b n²` CPU-seconds per game-second; defaults `a = 0.3` ms, `b = 1` µs, `C = 1`, floor `f_min = 0.1` (MMO302 week 12).
- `f = clamp(C / W(n), f_min, 1)`; dilation off means `f = 1`.
- Full stream per client `n r k` B/s; dilated `f n r k`; aggregated `f × circle × r × k + (n / squad) × summary`. Defaults `r = 2`, `k = 12`, `circle = 20`, `squad = 10`, `summary = 8`.
- kbit/s `= B/s × 8 / 1,000`. Server total for full fan-out `n × n r k` (with `f` when dilated), shown in Mbit/s.
- When `f` is at the floor and `f_min × W(n) > C`, show a badge "past the floor: backlog grows" (MMO302's backlog growth, `f_min W − C` CPU-s per second, shown in the badge).

**Fan-out chart.** x axis pilots, log scale 100 to 10,000. y axis kbit/s per client, linear 0 to 800 (clip higher values at the top edge with a marker). Three lines: full fan-out, full with dilation, aggregated with dilation. A cursor at the current `n`. Mark the dilation start `n₁` (where `W = C`) with a dot on the dilated line and the floor `n₂` (where `W = C / f_min`) with a vertical dashed line labelled "floor".

**Gauge.** Dilation percentage `f` as a large number with a horizontal bar, and "1 game second = X real seconds" (`1 / f`).

**Determinism model (must match section 3).** Two machines start from `x = 0.4` and `y = 0.4 + ε`, and each step applies `x ← R x (1 − x)` to both. Defaults `R = 3.9`, `ε = 10⁻¹⁵`, visible gap `v = 0.01`, 60 steps. Plot `log10 |x − y|` against step (y axis from −16 to 0), with a horizontal line at `log10 v`. Show the measured growth `g = (gap at the last step / ε)^(1 / steps)`, the model's `ln(v / ε) / ln(g)` steps to visible, the first step where the measured gap exceeds `v`, and the time to visible at the chosen tick rate. A "fixed-point" toggle computes both machines in integer arithmetic from the same start (gap 0 throughout) and shows the line flat at the bottom with the label "identical bits".

**Controls (keyboard accessible, each with a live value label).**
- Pilots `n`: slider 100 to 10,000 (log), default 3,000. Chip buttons 500, 861, 1,000, 3,000, 4,000.
- Dilation on/off, default on.
- `b` (pair cost, µs): slider 0.25 to 4, default 1. Buttons "halve b" and "halve a".
- `r`, `k`, `circle`, `squad`: number inputs.
- Determinism: `ε` as a power of ten, slider −16 to −6, default −15. `R`: slider 3.6 to 4.0, step 0.01, default 3.9. Tick rate: 1, 10, 20 or 60 Hz, default 20. Fixed-point toggle.

**Number panels.** Fan-out: `W(n)`, `f`, per-client kbit/s for each line, server total Mbit/s, `n₁` and `n₂`. Determinism: `g`, predicted and measured steps to visible, seconds to visible.

**Test values (defaults).**

| n | f | full kbit/s | dilated | aggregated |
|---|---|---|---|---|
| 100 | 100% | 19.2 | 19.2 | 4.5 |
| 1,000 | 76.9% | 192 | 148 | 9.4 |
| 2,000 | 21.7% | 384 | 83 | 13.6 |
| 3,000 | 10.1% | 576 | 58 | 19.6 |
| 4,000 | 10.0% | 768 | 77 | 26.0 |

Dilation starts at `n₁ ≈ 861` (dilated stream 165 kbit/s there); floor at `n₂ ≈ 3,016`; with `b` halved, `n₂ ≈ 4,182`; with `a` halved, `n₂ ≈ 3,088`. Server total at 1,000 pilots without dilation 192 Mbit/s. Past-the-floor badge at 4,000: growth 0.72 CPU-s per second. Determinism defaults: gap 2.0e-12, 4.1e-08, 9.0e-05, 3.7e-01 at steps 15, 30, 45, 60; `g = 1.75`; model 54 steps, measured 52; 2.7 s at 20 Hz.

**First screen.** Defaults at `n = 3,000`, gauge showing 10.1%, caption "3,000 pilots: full fan-out needs 576 kbit/s per client; dilation delivers 58." The determinism chart already drawn with its default run.

**Accessibility.** All controls keyboard reachable; number panels `aria-live="polite"`; charts have text alternatives through the number panels; respects `prefers-reduced-motion` and `prefers-color-scheme`.
