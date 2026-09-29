# MMO404 · Week 05 — Bandwidth shaping and LOD for networking

**Why this matters:** Last week you split a fixed budget and let the error float. This week you turn it around. You fix the error a player may see and let the bytes float, which is far cheaper on average and far more dangerous at the worst moment. Knowing both, and how a shaper joins them, is how you keep a city hub at 50 kbit/s on a quiet evening and still playable when a world boss spawns in the middle of it.

**You will be able to:**
- Compute the bandwidth of a crowd under three sending policies: a flat rate, distance tiers and error-driven (dead-reckoning) updates.
- Derive the send interval of an error-driven entity from its acceleration and threshold, `T = √(2ε / a)`, and scale the threshold with distance.
- Choose field-level LOD (which fields, at what precision) from an error target, using quantization from CS202.
- Size a token-bucket shaper (rate and depth) for a given burst and compute how long the backlog takes to clear.

**Before class:** Jesse Aronson, "Dead Reckoning: Latency Hiding for Networked Games" (Gamasutra, September 1997), the whole article. Frohnmayer and Gift, "The TRIBES Engine Networking Model", the sections on the Stream manager and the Ghost manager's state mask. Epic Games, "Actor Network Dormancy" (Unreal Engine 5.8 documentation).

**Prerequisites from earlier courses:** [MMO404 week 4, replication prioritization and relevancy](w04-replication-prioritization-and-relevancy.md) (fair share, the angle formula, the accumulator). [CS202 week 5, serialization and bit packing](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w05-serialization-and-bit-packing.md) (bits of precision per field). [CS202 week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) and [week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) (what the client does between updates). [CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (per-client budgets and the four options when a snapshot does not fit).

**Interactive:** [w05-network-lod.html](../examples/w05-network-lod.html). Keep it open during section 2.

---

## 1. Fix the bytes or fix the error

Every replication system makes one of two promises, even if nobody wrote it down.

- **A byte promise.** "This client receives at most `B` updates per tick." Week 4's fair share keeps this promise exactly. The cost is that error floats. When the scene gets busier, every entity gets staler.
- **An error promise.** "No entity on this client's screen is wrong by more than `ε`." The server sends an entity only when the client's guess of it has drifted past `ε`. Error is capped by construction. The cost is that bytes float. When the scene gets busier or more chaotic, the stream grows.

**Network LOD** (level of detail) is the family of techniques that spend fewer bytes on entities where the player would not notice. It comes in three forms.

1. **Rate LOD.** Send far or unimportant entities less often. Distance tiers are the simple version. Error-driven updates are the precise version.
2. **Field LOD.** Send fewer fields, or the same fields at lower precision. A player at 100 m does not need its weapon's attachment slots or centimetre-precise position.
3. **Representation LOD.** Replace many entities with one summary. A crowd of 80 at the far end of a plaza becomes "about 80 people around here, moving north".

**Bandwidth shaping** is what keeps the byte promise when the error promise would break it. A shaper limits the rate at which bytes leave the server for one client and queues the rest. The queue is then drained in priority order, which is week 4 again.

The model for this week has all three parts: what each policy costs, what error it allows, and what the shaper does with a burst.

## 2. Worked example: three policies for a 300-entity city hub

### The hook

In a military simulation that follows the DIS standard (Distributed Interactive Simulation, IEEE 1278, the protocol that grew out of DARPA's SIMNET project), a tank parked in a field reports its state about once every five seconds. That is the heartbeat, and it exists so other simulators know the tank is still there. A tank driving in a straight line at a steady speed may report no more often than the parked one. A tank that swerves reports within a fraction of a second. Every simulator runs the same prediction for every remote vehicle, and a vehicle's own simulator sends an update only when the shared prediction has drifted past an agreed threshold. How often you hear about an entity depends on how *unpredictable* it is, not how close or important. Aronson described the scheme to game developers in 1997, and it still beats most distance-tier systems on bytes. The question is what it costs you when things get chaotic.

### The model

A client in a city hub sees 300 entities. Group them into distance bands.

| Band | Count | Typical distance `d` |
|---|---|---|
| Near | 30 | 10 m |
| Mid | 90 | 40 m |
| Far | 180 | 100 m |

At a quiet moment, half the entities in each band stand still (at a bank, a vendor, a mailbox) and half walk around. Walkers turn gently, with a lateral acceleration `a = 2 m/s²`, and change input suddenly (start, stop, sharp turn) about once a second. All three numbers are invented but typical of a hub.

Each policy's cost is a sum over entities of rate times bytes:

```
bandwidth = Σ  rate_i × bytes_i
```

**Policy A, flat.** Everyone at the tick rate, 20 Hz, with a full 20-byte update.

**Policy B, three tiers.** Near at 20 Hz with 20 bytes, mid at 5 Hz with 12 bytes (position and heading only), far at 1 Hz with 6 bytes (coarse position only).

**Policy C, error-driven.** The client extrapolates each entity from its last position and velocity (dead reckoning). The server runs the same extrapolation and sends a 20-byte update when the true position differs from the client's guess by more than `ε`.

For an entity with lateral acceleration `a`, the gap between a straight-line guess and a curving path after time `t` is `a t² / 2`. It reaches `ε` after

```
T = √(2ε / a)          seconds between updates for smooth motion
```

We want the same *angular* error at every distance, as in week 4, so set the threshold to an angle `θ` at the camera, `ε = θ × d`. Then add one update per sudden input change (rate `c`), a heartbeat floor `r_min`, and the tick rate as a ceiling `r_max`:

```
rate(d) = min(r_max, max(r_min, √(a / (2 θ d)) + c))     for moving entities
rate    = r_min                                            for idle entities
```

Use `θ = 1°`, `c = 1` per second, `r_min = 0.2` Hz (one update every 5 seconds, the DIS heartbeat) and `r_max = 20` Hz.

### Numbers you can check

First the thresholds and rates for a moving entity under Policy C.

| Band | `ε = θd` | Smooth interval `√(2ε/a)` | Smooth rate | Plus `c = 1` | Rate |
|---|---|---|---|---|---|
| Near, 10 m | 0.175 m | 0.418 s | 2.39 Hz | +1 | 3.39 Hz |
| Mid, 40 m | 0.698 m | 0.836 s | 1.20 Hz | +1 | 2.20 Hz |
| Far, 100 m | 1.745 m | 1.321 s | 0.76 Hz | +1 | 1.76 Hz |

Check the near row. `ε = 0.01745 × 10 = 0.1745` m. `T = √(2 × 0.1745 / 2) = √0.1745 = 0.418` s. Its inverse is 2.39 Hz.

Now the three policies for the whole hub.

| Policy | Near (30) | Mid (90) | Far (180) | Total | kbit/s |
|---|---|---|---|---|---|
| A. Flat 20 Hz × 20 B | 12,000 | 36,000 | 72,000 | 120,000 B/s | 960.0 |
| B. Tiers | 12,000 | 5,400 | 1,080 | 18,480 B/s | 147.8 |
| C. Error-driven, θ = 1° | 1,078 | 2,157 | 3,522 | 6,758 B/s | 54.1 |

Check two cells. Tiers, mid band: `90 × 5 Hz × 12 B = 5,400` B/s. Error-driven, near band: 15 walkers at 3.39 Hz plus 15 idle at 0.2 Hz is `50.9 + 3 = 53.9` updates per second, times 20 bytes, 1,078 B/s.

The code below prints the totals.

```python
import math

BANDS = [("near", 30, 10), ("mid", 90, 40), ("far", 180, 100)]  # name, count, distance m
TIERS = {"near": (20, 20), "mid": (5, 12), "far": (1, 6)}       # Hz, bytes per update

def error_rate(d, moving, theta_deg=1.0, a=2.0, changes=1.0, r_max=20, r_min=0.2):
    """Updates per second for one entity under a threshold of theta_deg at distance d."""
    if not moving:
        return r_min
    eps = math.radians(theta_deg) * d
    return min(r_max, max(r_min, math.sqrt(a / (2 * eps)) + changes))

flat = sum(n * 20 * 20 for _, n, _ in BANDS)
tiered = sum(n * TIERS[b][0] * TIERS[b][1] for b, n, _ in BANDS)
errd = sum(20 * (n / 2 * error_rate(d, True) + n / 2 * error_rate(d, False))
           for _, n, d in BANDS)
for name, bps in [("flat 20 Hz", flat), ("three tiers", tiered), ("error-driven", errd)]:
    print(f"{name:13s} {bps:8.0f} B/s  {bps * 8 / 1000:6.1f} kbit/s")
```

```
flat 20 Hz      120000 B/s   960.0 kbit/s
three tiers      18480 B/s   147.8 kbit/s
error-driven      6758 B/s    54.1 kbit/s
```

### What the tiers buy with their extra bytes

The tiers cost almost three times as much as the error-driven stream. Look at what the extra bytes buy. Assume the client extrapolates under both policies, so a smoothly turning walker is off by `a T² / 2` just before its next update.

| Band | Tier interval | Smooth error before update | As an angle | Error-driven angle |
|---|---|---|---|---|
| Near | 0.05 s | 0.0025 m | 0.01° | 1° |
| Mid | 0.2 s | 0.04 m | 0.06° | 1° |
| Far | 1 s | 1.0 m | 0.57° | 1° |

In the near and mid bands, the tiers keep smooth motion 17 to 70 times more accurate than the 1° anyone would notice, and they pay 20 Hz for the 15 near players standing still at the bank. Now take a sudden stop. A player running at 3.5 m/s stops dead, and the client's guess keeps going at 3.5 m/s until the next update.

| Band | Tier interval | Error from a stop | As an angle | Error-driven |
|---|---|---|---|---|
| Near | 0.05 s | 0.175 m | 1.0° | Sent next tick, 1° at most |
| Mid | 0.2 s | 0.70 m | 1.0° | Sent within 0.2 s, 1° at most |
| Far | 1 s | 3.5 m | 2.0° | Sent within 0.5 s, 1° at most |

The tiers were sized for the worst case, which is sudden changes. They pay for that worst case every tick, for everyone, including the idle. Error-driven updates pay only when an entity actually does something unpredictable. That is where the factor of three comes from.

### The catch: error-driven bytes float

Now the world boss spawns in the plaza. Every one of the 300 entities starts running and dodging, with three sudden changes a second instead of one.

| Crowd behaviour | Tiers | Error-driven, θ = 1° |
|---|---|---|
| Everyone idle | 147.8 kbit/s | 9.6 kbit/s |
| Half walking, `c = 1` (the quiet hub) | 147.8 | 54.1 |
| Everyone walking, `c = 1` | 147.8 | 98.5 |
| Half walking, `c = 3` | 147.8 | 102.1 |
| Everyone running and dodging, `c = 3` | 147.8 | 194.5 |

The tiers cost the same whatever the crowd does. The error-driven stream swings by a factor of 20, and in a panic it costs more than the tiers. That is the price of the error promise. The bytes follow the chaos, and chaos arrives exactly when the player is paying attention. Section 4 caps it.

### Move it yourself

Open `examples/w05-network-lod.html`. The top view shows one walker's true path and the client's guess for the selected band, with the error drawn as a line between them, under tiers and under error-driven updates side by side. The bottom view is a stacked bar of the hub's bytes per second under each policy, with a horizontal line for a 96 kbit/s client budget. Start in "quiet hub". Then drag the crowd behaviour slider from "idle" to "panic" and watch the tiers' bar stay put while the error-driven bar grows past it and past the budget line. Drag θ from 1° to 2° and the error-driven bar shrinks by about a seventh.

### Same idea elsewhere

**DIS and SIMNET (IEEE 1278, military simulation, 1980s to today).** Aronson's article describes it plainly. Every node runs an agreed dead-reckoning model for every remote entity, the owning node compares the model with its true state, and a new Entity State PDU goes out when the two differ by more than the agreed threshold. Entity State PDUs also go out at least once every five seconds. In our form, that is Policy C with a fixed threshold `ε` in metres and `r_min = 0.2` Hz. The only change we made was to scale `ε` with distance, because a game has one camera per client and a military simulator may not.

**Starsiege: Tribes (Dynamix, 1998).** Tribes does field LOD with its state mask. Each object splits its state into groups (position and velocity as one, rotation as another, animation as a third), with upwards of 20 flags in a typical object, and marks a flag dirty only when that group changes. The packet carries only dirty groups. It also shapes. A client connecting over a 28.8 modem asks the server for, say, 10 packets per second of at most 200 bytes, and the server enforces its own per-client maximum on top. In our form, the state mask sets `bytes_i` per update from what changed, and the requested rate and size are the shaper's `ρ`.

**Unreal Engine (Epic Games, UE 5.8 documentation).** Net dormancy is the idle case turned into an engine feature. An actor marked dormant (`DORM_Initial` or `DORM_DormantAll`) is dropped from the list the net driver scans each update, until the game wakes it. The documentation says this can save several milliseconds of server CPU per frame in projects with many rarely changing actors. In our form, dormancy sets an idle entity's rate to zero with no heartbeat, which is safe for a placed door or chest and wrong for a player who might be hiding.

**Fiedler's cube demo (Gaffer on Games, 2015).** Resting cubes get priority 1 against 100 for interacting cubes, and delta compression against acked baselines ([CS202 week 7](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w07-snapshots-and-delta-compression.md)) makes an unchanged cube nearly free. That is an error-driven policy expressed in week 4's language. A cube whose state has not changed has nothing to say and costs almost nothing. The byte budget of 256 kbit/s stays fixed, so the demo keeps the byte promise and lets the error of resting cubes float, which is safe because they are not moving.

Four systems, one decision. Every one of them sends less when the receiver's guess is still right, and each has to decide separately what happens when many guesses go wrong at once.

### Design judgment

- **Choose the promise first.** A competitive arena should keep the error promise near the player, since a 2° error on an enemy at 10 m decides fights. A social hub can keep the byte promise, since nobody loses anything if a dancer at 80 m is a little late.
- **Use the heartbeat for presence, not for accuracy.** A 5-second heartbeat tells the client the entity still exists. It does not keep a moving entity accurate. If your game can hide an idle player behind dormancy, make sure "idle" cannot be used to stay invisible.
- **Scale the threshold with the camera, not the map.** An angular threshold spends bytes where the player can see the difference. A metre threshold overspends on far entities and underspends near the camera.
- **Budget the panic, not the evening.** An error-driven hub that averages 54 kbit/s and peaks at 195 kbit/s needs a shaper sized for the peak or a priority rule for what to drop. Test with a spawn event, not an idle crowd.
- **Tiers are fine when behaviour is uniform.** Projectiles, vehicles on rails and AI patrols move predictably. For them, a fixed rate per tier is simpler to test and to reason about, and error-driven updates save little.

### Check this example

1. Under Policy C, what is the smooth-motion interval for a walker at 25 m with `a = 2 m/s²` and `θ = 1°`? What is its rate with `c = 1`?
2. The hub doubles its far band to 360 entities. How many bytes per second does each policy add?
3. A designer loosens θ from 1° to 2°. By what factor does the smooth part of the rate change? Why is the saving on the whole stream smaller than that?

<details>
<summary>Answers</summary>

1. `ε = 0.01745 × 25 = 0.436` m. `T = √(2 × 0.436 / 2) = √0.436 = 0.661` s, so the smooth rate is 1.51 Hz. Adding `c = 1` gives 2.51 Hz.
2. Flat adds `180 × 20 × 20 = 72,000` B/s. Tiers add `180 × 1 × 6 = 1,080` B/s. Error-driven adds `20 × (90 × 1.757 + 90 × 0.2) = 3,522` B/s. The error-driven far band is more expensive than the tiered far band, because tiers only promise about 2° there.
3. The smooth rate goes as `1 / √θ`, so doubling θ divides it by `√2 = 1.41`. The sudden-change term `c` and the idle heartbeat do not depend on θ, so they stay. The quiet hub falls from 6,758 B/s to 5,833 B/s, a saving of 14%.

</details>

## 3. Field LOD: fewer bits for far entities

Rate is one axis of LOD. Size is the other. From CS202 week 5, a coordinate quantized over a range `L` with step `s` needs `⌈log₂(L / s)⌉` bits. If the error you can accept at distance `d` is `θd`, you can quantize with a step of about `2θd` (half a step each side), so the bits you need fall as the entity gets farther away.

| Distance | Allowed error `θd` at 1° | Step `2θd` | Bits per axis over a 1,024 m region |
|---|---|---|---|
| 10 m | 0.17 m | 0.35 m | 12 |
| 40 m | 0.70 m | 1.40 m | 10 |
| 100 m | 1.75 m | 3.49 m | 9 |

Check one row. At 40 m the step is `2 × 0.01745 × 40 = 1.40` m, and `1,024 / 1.40 = 733`, which needs 10 bits since `2¹⁰ = 1,024`. Three axes save 9 bits per update between near and far. That is modest. Coarse quantization has a bigger payoff when you send positions *relative* to a reference the client already has, such as the centre of the client's grid cell ([week 3](w03-spatial-partitioning-at-scale.md)), because the range `L` shrinks too.

The larger savings come from dropping fields. A far entity does not need its equipment, its buff list, its casting bar or its exact animation frame. A practical scheme defines a field set per tier, the way Tribes defines state groups. The near set has everything, the mid set has position, heading, movement mode and a coarse animation state, and the far set has position and a team colour. The client must handle an entity changing sets as it approaches, which means sending the missing fields when it crosses into a richer tier. That is the same "first update costs more" effect as opening a ghost in week 4, and it wants the same hysteresis.

### Representation LOD: crowds as one entity

At some density, individuals stop mattering. The far band of our hub has 180 entities, and from 100 m away they are a crowd. Replace each 20 m by 20 m grid cell of far entities with one summary: count, centroid, mean velocity. Say that is 8 bytes, sent once a second. If the 180 far entities fill 12 cells, the far band costs `12 × 8 = 96` B/s instead of 3,522 B/s under Policy C. The client draws plausible people within the cell from the summary. The cost is that you cannot target, inspect or whisper someone the client has only as a statistic. The moment a far player matters (they are your friend, they attack you) week 4's gameplay weights must promote them out of the crowd into a real ghost.

## 4. Shaping: keeping the byte promise under an error policy

### The token bucket

A **token bucket** has two parameters. Tokens (bytes you are allowed to send) arrive at rate `ρ` bytes per second, and the bucket holds at most `σ` bytes of them, its depth. Each send spends tokens. If there are not enough, the data waits in a queue. Over any window of `t` seconds, the bucket lets out at most `σ + ρ t` bytes, so `ρ` bounds the average and `σ` bounds the burst.

Two numbers describe what happens to a burst. If a client's steady stream uses `s` bytes per second and a burst of `X` bytes arrives, the part that does not fit in the bucket, about `X − σ`, becomes a backlog. It drains at the spare rate `ρ − s`:

```
drain time ≈ (X − σ) / (ρ − s)
```

Take the quiet hub under error-driven updates, about 6,800 B/s. Suddenly the client runs through the town gate and 150 new ghosts must be opened at 60 bytes each, a burst of 9,000 bytes. The simulation below ticks at 20 Hz.

```python
def bucket(demand, rate, depth, tick=0.05):
    """demand: bytes wanted per tick. Returns the backlog after each tick."""
    tokens, backlog, out = depth, 0.0, []
    for want in demand:
        tokens = min(depth, tokens + rate * tick)
        backlog += want
        sent = min(tokens, backlog)
        tokens -= sent
        backlog -= sent
        out.append(backlog)
    return out

steady = 6_800 * 0.05                       # 340 bytes per tick
demand = [steady] * 100
demand[20] += 9_000                         # 150 new ghosts at 60 bytes each
for rate, depth in [(12_000, 2_000), (12_000, 8_000), (24_000, 2_000)]:
    q = bucket(demand, rate, depth)
    clear = next(i for i in range(20, 100) if q[i] < 1) - 20
    print(f"rate {rate:6d} B/s depth {depth:5d} B  peak backlog {max(q):6.0f} B  "
          f"clear after {clear * 50:5d} ms")
```

```
rate  12000 B/s depth  2000 B  peak backlog   7340 B  clear after  1450 ms
rate  12000 B/s depth  8000 B  peak backlog   1340 B  clear after   300 ms
rate  24000 B/s depth  2000 B  peak backlog   7340 B  clear after   450 ms
```

Check the first line with the formula. `(9,340 − 2,000) / (12,000 − 6,800) = 7,340 / 5,200 = 1.41` s, which the 50 ms ticks round up to 1.45 s. A deeper bucket absorbs the burst almost at once, which is kind to the player and hard on the link. Sending 8 KB in one tick is 1.3 Mbit/s for 50 ms, and a weak mobile link will queue or drop it ([CS202 week 2](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w02-latency-jitter-loss-measure-your-own.md)). A faster rate clears the backlog in a third of the time but raises the average you promise to carry. Choose `σ` from what the client's link can absorb in one burst and `ρ` from what it can carry on average.

### What waits in the queue

A queue drained in arrival order is the wrong queue. The backlog should drain in week 4's priority order. The client's target and party go first, new ghosts near the camera next, and far crowd summaries last. Two rules keep the queue healthy.

- **Replace, do not append.** If an entity already has an update waiting and a newer one arrives, overwrite the old one. A stale position is worth nothing once a fresher one exists. With this rule the backlog is bounded by the number of entities, not by time.
- **Shed by LOD before you shed by priority.** When the backlog grows, first demote entities one LOD level (fewer fields, a crowd summary), then loosen θ for low-priority classes, and only then drop updates. That order keeps every entity present and trades detail for coverage.

### Who sets the rate

Tribes lets the client ask for its packet rate and size and change them as the line quality changes, while the server caps each client with its own maximum. That is the right split. The client knows its link. The server knows its total upload. In a modern game you can go further and adapt `ρ` from measured loss and round-trip time, cutting it quickly when loss rises and raising it slowly when the link is clean. That is the same instinct as TCP's congestion control, applied to your own UDP stream ([CS202 week 6](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w06-reliability-over-udp.md)).

## In-class activity (25 minutes)

Pairs. Each pair gets one scene: a 60-player raid on one boss (all near, all chaotic), a 400-player capital city at peak (mostly far, mostly idle), or a 100-player open-world race (mid distance, fast and predictable).

1. Choose Policy B (tiers) or Policy C (error-driven) for each entity class in your scene, and one sentence of justification per class.
2. Using the interactive's custom mode, set counts, distances, moving share, `a` and `c` for your scene. Record the quiet and panic bandwidth of your mixed policy.
3. Size a token bucket (`ρ`, `σ`) for a 96 kbit/s client link. Compute the drain time for the biggest burst your scene can produce.
4. Name the first thing your shaper sheds when the backlog grows.

Expected output: a short table (class, policy, quiet B/s, panic B/s), your `ρ` and `σ`, the drain time, and the shedding order. Pairs with the same scene compare.

## Common misconceptions

- **"Dead reckoning is a client prediction trick."** It is also a sending rule. The server runs the client's prediction so it knows when the client is wrong. Without that shared model, you cannot decide when to send.
- **"Error-driven updates are always cheaper than tiers."** They are cheaper on average for mixed crowds, and more expensive when everyone moves unpredictably. The quiet hub is 54 kbit/s, and the panic is 195 kbit/s against the tiers' 148.
- **"A token bucket smooths traffic, so it cannot hurt."** It adds queueing delay to everything behind a burst. With a FIFO queue, your target's update waits behind 150 new ghosts. Drain by priority.
- **"Far entities need the same precision, just less often."** The error you can accept grows with distance, so precision can fall too. Field LOD and rate LOD save on different axes and multiply.

## Check yourself

1. An NPC patrols in a circle of radius 8 m at 4 m/s. Under a fixed threshold of 0.2 m, how often does an error-driven server send it? Compare with a 5 Hz tier.
2. For the quiet hub, you replace the far band's individual updates (Policy C) with crowd summaries in 12 cells at 8 bytes per second each. What is the new total, and what fraction of the stream was the far band before?
3. A client's link carries 64 kbit/s on average and can absorb a 4 KB burst. Its steady stream is 5,000 B/s. How long does a 10,000-byte burst take to clear?
4. Explain why "replace, do not append" bounds the backlog by the number of entities.

<details>
<summary>Answers</summary>

1. `a = v² / R = 16 / 8 = 2` m/s². `T = √(2 × 0.2 / 2) = √0.2 = 0.447` s, about 2.24 Hz. A 5 Hz tier sends 2.2 times as often for a patrol whose path is perfectly regular. Better still, send the patrol route once and let the client run it.
2. The far band was 3,522 of 6,758 B/s, 52% of the stream. The new total keeps the near and mid bands and adds the summaries, `1,078 + 2,157 + 96 = 3,331` B/s, about 26.6 kbit/s.
3. `ρ = 64,000 / 8 = 8,000` B/s and `σ = 4,000` B. Drain time `≈ (10,000 − 4,000) / (8,000 − 5,000) = 2` s.
4. Each entity has at most one waiting update, because a newer one overwrites it. So the queue can never hold more items than there are relevant entities, however long the burst lasts.

</details>

## Lab / assignment hook

[Lab 05, dead reckoning and shaping](../labs/lab05.md). You implement an error-driven sender and check its interval against `√(2ε / a)`, then a token bucket with a priority queue that replaces stale updates, and run both on a seeded hub where a boss spawns halfway through. Deliverable: your `lod.py`, a CSV of bandwidth and error over time for tiers and error-driven updates, and a one-page shaping policy.

## Sources

- Aronson, J. "Dead Reckoning: Latency Hiding for Networked Games" (Gamasutra, 19 September 1997; now at gamedeveloper.com). DIS grew out of DARPA's SIMNET project. The threshold rule for sending an Entity State PDU when dead-reckoned and true state differ by more than an agreed threshold; Entity State PDUs sent at least once every five seconds under DIS; the scheme's origin in military simulation.
- Wikipedia, "Distributed Interactive Simulation" (accessed September 2026). IEEE 1278 standard family (1278-1993 to 1278.1-2012); dead reckoning introduced by BBN during SIMNET.
- Frohnmayer, M. and Gift, T. "The TRIBES Engine Networking Model" (Dynamix, undated paper written while Tribes II was in development; Starsiege: Tribes shipped December 1998. Copy at https://www.gamedevs.org/uploads/tribes-networking-model.pdf). Stream manager rate and size set by the receiving host, 28.8 modem example of 10 packets per second of 200 bytes, server-imposed per-client maximum; state mask with upwards of 20 flags per object and partial updates.
- Epic Games, "Actor Network Dormancy" (Unreal Engine 5.8 documentation). `ENetDormancy` states; dormant actors skipped by the net driver; savings of multiple milliseconds of server CPU per frame.
- Fiedler, G. "State Synchronization" (Gaffer on Games, 5 January 2015). Priorities of 100 for interacting cubes and 1 for cubes at rest; 256 kbit/s target.

## Interactive spec: examples/w05-network-lod.html

**Insight the visual must make obvious:** distance tiers cost the same whatever the crowd does and overspend on idle and predictable entities, while error-driven updates cost bytes only when entities are unpredictable, which makes them cheap on a quiet evening and more expensive than tiers in a panic. The shaper's budget line shows why error-driven sending needs one.

**Layout.** Two linked views and a number panel. Desktop: path view on top, bandwidth bars below, panel at the side. Under 700 px: stacked in that order.

**Top view (one walker, two policies).** Two small panels side by side, "Tiers" and "Error-driven". Each shows the same walker's true path over the last 3 seconds (solid line) and the client's dead-reckoned guess (dashed line), with update moments marked as dots and the current error as a short red segment. The walker follows a seeded path: straight for 1 s, a smooth turn with `a = 2 m/s²`, then a stop, repeating. The band selector (near 10 m, mid 40 m, far 100 m) sets the distance, which sets the tier rate and the threshold `ε = θd`. Print below each panel the updates per second and the maximum angle error over the last 3 s.

**Bottom view (the hub).** Three horizontal bars (flat, tiers, error-driven) in kbit/s on one axis from 0 to 1,000 kbit/s with a break or log option, stacked by band (near, mid, far). A vertical line for the client budget (default 96 kbit/s). Put the flat bar behind a toggle, off by default, so the scale fits tiers and error-driven.

**Model (must match section 2).**
- Bands: near 30 at 10 m, mid 90 at 40 m, far 180 at 100 m.
- Tiers: near 20 Hz × 20 B, mid 5 Hz × 12 B, far 1 Hz × 6 B.
- Error-driven moving rate `min(20, max(0.2, √(a / (2 θ d)) + c))`, idle rate 0.2, 20 bytes per update.
- Bytes/s `= Σ n × rate × bytes`; kbit/s `= bytes × 8 / 1000`.

**Controls (keyboard accessible).**
- Crowd behaviour slider with five stops matching the table in section 2: idle (moving share 0), quiet hub (0.5, `c = 1`), everyone walking (1.0, `c = 1`), half dodging (0.5, `c = 3`), panic (1.0, `c = 3`). Default "quiet hub".
- θ slider 0.25° to 4°, default 1°.
- `a` slider 0.5 to 6 m/s², default 2.
- Client budget slider 32 to 256 kbit/s, default 96.
- Custom mode: editable counts and distances for the three bands.
- Crowd summary toggle: replaces the far band with 12 cells × 8 B/s.

**Number panel.** Per band and policy: rate per entity, bytes/s, kbit/s. Totals row.

**Test values (defaults).** Flat 960.0, tiers 147.8, error-driven 54.1 kbit/s. Error-driven rates 3.39, 2.20, 1.76 Hz for moving near, mid, far. Crowd behaviour stops give error-driven totals 9.6, 54.1, 98.5, 102.1, 194.5 kbit/s. θ = 2° with quiet hub gives 46.7 kbit/s. Crowd summary toggle with quiet hub gives 3,331 B/s, 26.6 kbit/s (26.65 before rounding).

**First screen.** Quiet hub, near band, both path panels animating, and the caption "Tiers pay every tick. Error-driven pays when the guess is wrong."
