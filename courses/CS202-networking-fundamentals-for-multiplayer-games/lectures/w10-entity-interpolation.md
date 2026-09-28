# CS202 · Week 10 — Entity interpolation

**Why this matters:** Prediction and reconciliation made your own character feel instant. Everyone else on your screen is still built from snapshots that arrive 20 times a second, late, unevenly, and sometimes not at all. Draw them naively and they teleport. Entity interpolation makes them glide, and the price is that you always see other players in the past. This week you learn to choose how far in the past, and to say what that choice costs in meters.

**You will be able to:**
- Compute where a client draws another player at any frame, from the snapshot times, the one-way latency and the interpolation delay `D`.
- Derive how many lost snapshots in a row a given `D` survives, and size `D` from a send rate, a loss pattern and a jitter margin.
- Compute how far behind the server, and behind the other player's own screen, an interpolated player is drawn, in milliseconds and meters.
- Implement an interpolation buffer with extrapolation limits, angle wrapping and teleport handling, and critique when a game should extrapolate instead.

**Before class:** Gabriel Gambetta, *Fast-Paced Multiplayer*, part III, "Entity Interpolation" (15 minutes). Valve Developer Community, "Source Multiplayer Networking", the section "Entity interpolation" (half a page). Glenn Fiedler, "Snapshot Interpolation" (Gaffer on Games, November 2014), from "Interpolation buffer" to the end.

**Prerequisites from earlier courses:** [MA101 week 8, lerp, inverse lerp and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (the whole technique is one inverse lerp on time and one lerp on position). [MA101 week 10, angles](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (why 350° to 10° is a 20° turn). [CS202 week 2](w02-latency-jitter-loss-measure-your-own.md) (the jitter buffer, which this week generalizes). [CS202 week 7](w07-snapshots-and-delta-compression.md) (what a snapshot holds). [CS202 week 8](w08-client-side-prediction.md) (the 150 ms setup, 6 m/s walking speed and 60 Hz ticks this week reuses). [CS202 week 9, server reconciliation](w09-server-reconciliation.md).

**Interactive:** [examples/w10-lag-lab.html](../examples/w10-lag-lab.html). Keep it open during section 2.

---

## 1. Twenty pictures a second, sixty frames to fill

Your client has a local player it predicts (week 8) and corrects (week 9). Every other moving thing, the other players, their projectiles, the enemy that is chasing them, comes only from **snapshots**, the server's periodic reports of world state (week 7). This week's setup is the same as week 8's. The server simulates at 60 Hz, sends a snapshot every third tick (20 per second, one every 50 ms), and the display draws 60 frames per second. So for every snapshot the client must draw three frames, and for every snapshot that gets lost it must draw six.

A client has three options for where to draw a remote entity on a frame between snapshots.

- **Snap to the newest.** Draw the entity at the position in the newest snapshot received. It is simple and it is as fresh as the data allows. At 6 m/s the entity jumps 0.3 m every 50 ms and stands still in between, so it stutters. When a snapshot is lost, it freezes for 100 ms and then jumps 0.6 m.
- **Extrapolate.** Take the newest known position and velocity and project them forward to "now". This is also called **dead reckoning**, after ship navigation. It is smooth while the entity keeps going in a straight line and wrong every time it turns, stops or is pushed.
- **Interpolate.** Draw the entity a little in the past, at a time for which you already hold a snapshot on each side, and blend between the two. It is smooth and it only ever shows positions the server really sent. The cost is delay.

Gambetta's series makes the point that the right choice depends on how predictable the entity is. A racing car at 100 m/s can't turn around in 100 ms, so dead reckoning works. A shooter character can reverse direction in one tick, so dead reckoning fails, and almost every shooter since Half-Life interpolates.

### The two lerps

Interpolation is two operations from MA101 week 8. Give each snapshot the server time it describes, `t_a` and `t_b`. Pick a **render time** `t_r` between them.

```
alpha = (t_r − t_a) / (t_b − t_a)          inverse lerp on time, 0 at t_a, 1 at t_b
x     = x_a + alpha × (x_b − x_a)          lerp on position
```

The only design decision is `t_r`, and it has one knob.

```
t_r = (client's estimate of the server's time now) − D
```

`D` is the **interpolation delay**. Valve's documentation calls it the lerp, or interpolation period. The client's estimate of the server's time is the server time of the newest snapshot, plus the time since it arrived, which is roughly the server's clock minus one one-way latency. Section 3 shows how a client keeps that estimate honest.

## 2. Worked example: the lag lab at 150 ms

### The hook

Valve's Source engine, the engine behind Counter-Strike: Source and Team Fortress 2, draws every other player 100 ms in the past by default. Week 2 sized that delay as a jitter buffer. This week asks what it costs in meters. Valve's documentation adds that this happens even on a listen server, where the server and the client are the same machine and the network delay is zero. At a 150 ms round trip, that means the player you are looking at is really about a meter and a half further along than your screen shows. Yet these games are known for tight, responsive combat. How can a game add 100 ms on purpose and feel faster for it?

The answer takes all three techniques of weeks 8 to 10 together. Each one hides a different delay, and each one moves the error somewhere you notice less. This worked example follows one match at 150 ms and adds the techniques one by one.

### The model

The setup is fixed for the whole example. Round trip `RTT = 150` ms, so one-way latency `L = 75` ms each way. Server tick 60 Hz. Snapshot interval `Δ = 50` ms. Walking speed `v = 6` m/s. Interpolation delay `D = 100` ms, Source's default.

**Your own character.** From week 8, a client that waits for the server shows your first step one round trip plus a few periodic waits after the key press. With prediction, you move the same frame. Week 8 showed that prediction without reconciliation snaps you back each time an old snapshot arrives. Reconciliation (week 9) replays your unacknowledged inputs on top of each snapshot, so the snaps disappear.

**Another player.** The server knows player B's position `L_B` late, because B's inputs take one uplink to arrive. You receive that position one downlink `L` later, then hold it for `D` before drawing it. So what you see is old by

```
age behind the server          = L + D
age behind B's own screen      ≈ L_B + L + D
distance behind                = v × age
```

**Coverage.** Snapshots arrive every `Δ`. With `D = kΔ`, the renderer always has a snapshot at or after `t_r` unless the `k − 1` snapshots after the one before `t_r` are all missing. So

```
D = kΔ + J   survives k − 1 lost snapshots in a row, with J ms of jitter margin
```

When the renderer runs out, it must either **hold** (freeze) or **extrapolate** past the newest snapshot. Source extrapolates for at most 0.25 s of loss and then stops.

### Numbers you can check

**Table 1. One match, three techniques.** All values at `RTT = 150` ms, 6 m/s, `D = 100` ms. The own-player rows reproduce week 8's simulator. The remote rows come from the same simulator with player B strafing, holding right for 700 ms, then left for 700 ms.

| What is switched on | Your character | Player B on your screen |
|---|---|---|
| Nothing (dumb client, snap to newest) | First step 183 ms after the key press. Keeps sliding 1.0 m (183 ms) after release. | Jumps 0.3 m every 50 ms. Freezes 100 ms when a snapshot is lost. |
| Prediction only | Moves the same frame. Snaps back 0.5, 0.3 and 0.1 m in the first 183 ms, then trails. | Unchanged. |
| Prediction and reconciliation | Moves the same frame. No snaps. | Unchanged. |
| All three (add interpolation) | Moves the same frame. No snaps. | Glides. Drawn 175 ms behind the server (1.05 m) and about 242 ms behind B's own screen (1.45 m). |

Check the last cell by hand. `L + D = 75 + 100 = 175` ms, and `6 × 0.175 = 1.05` m. B's inputs reach the server one uplink late and run on the next 60 Hz tick, which in the simulator puts the server 4 ticks (0.4 m, about 67 ms) behind B's own screen. `1.05 + 0.4 = 1.45` m.

That is the trade in one row. Your own character is correct and instant. Everyone else is smooth and a meter and a half in the past. Week 11 deals with the consequence for shooting.

**Table 2. Inside the buffer.** Now zoom in on four snapshots of player B. B walks right at 6 m/s and reverses at server time 1100 ms, so B's true positions are 4.00 m at 1000, 4.30 m at 1050, 4.60 m at 1100, 4.30 m at 1150 and 4.00 m at 1200. The snapshot for 1100, the one that holds the peak, is **lost**. Every snapshot arrives exactly 75 ms after it was sent. The table shows what three clients draw at the same client moments. Client time is written on the server's clock for easy comparison, so a snapshot sent at 1050 arrives at 1125.

| Client time | Snap to newest (`D = 0`) | `D = 50`: `t_r`, drawn, how | `D = 100`: `t_r`, drawn, how |
|---|---|---|---|
| 1175 | 4.30 | 1050, 4.30, extrapolate | 1000, 4.00, lerp 1000 to 1050, α = 0 |
| 1200 | 4.30 | 1075, 4.45, extrapolate | 1025, 4.15, lerp, α = 0.5 |
| 1220 | 4.30 | 1095, **4.57**, extrapolate | 1045, 4.27, lerp, α = 0.9 |
| 1225 | 4.30 | 1100, **4.30**, lerp 1050 to 1150, α = 0.5 | 1050, 4.30, lerp 1050 to 1150, α = 0 |
| 1250 | 4.30 | 1125, 4.30, lerp, α = 0.75 | 1075, 4.30, lerp, α = 0.25 |
| 1275 | 4.00 (jump) | 1150, 4.30, lerp 1150 to 1200, α = 0 | 1100, 4.30, lerp, α = 0.5 |
| 1300 | 4.00 | 1175, 4.15 | 1125, 4.30, lerp, α = 0.75 |
| 1325 | 3.70 | 1200, 4.00 | 1150, 4.30, lerp 1150 to 1200, α = 0 |

Verify two cells. At client time 1220 with `D = 50`, `t_r = 1220 − 75 − 50 = 1095`. The newest snapshot the client holds is 1050, because 1100 was lost and 1150 does not arrive until 1225. So it extrapolates with the last known velocity, `4.30 + 6 × 0.045 = 4.57` m. Five milliseconds later the 1150 snapshot lands, `t_r = 1100` now sits between 1050 and 1150, and the lerp gives `4.30 + 0.5 × 0 = 4.30` m. B jumps 0.27 m backwards in one frame.

At client time 1250 with `D = 100`, `t_r = 1075`, `alpha = (1075 − 1050) / 100 = 0.25`, and `x = 4.30 + 0.25 × (4.30 − 4.30) = 4.30` m. The true position was 4.45 m.

Three behaviors, one lost packet.

- **Snap to newest** freezes B at 4.30 m from client time 1125 to 1275, 150 ms, then jumps 0.3 m.
- **`D = 50`** is one interval, `k = 1`. It survives zero losses. It extrapolates through the gap, overshoots toward the peak, then pops back 0.27 m.
- **`D = 100`** is two intervals, `k = 2`. It survives one loss. B never jumps. The price is a flattened corner. B turns around at 4.30 m instead of 4.60 m, and the 0.30 m of peak never appears on your screen. Bernier described the same effect in 2001 as a bouncing ball whose bounce gets "flattened" because the samples miss the extremes.

**Table 3. Sizing `D`.** At 20 snapshots per second (`Δ = 50` ms), using `D = kΔ + J`.

| Goal | k | J | D | Drawn behind the server (`L + D`, L = 75) | At 6 m/s |
|---|---|---|---|---|---|
| Smooth on a perfect network | 1 | 0 | 50 ms | 125 ms | 0.75 m |
| Survive 1 lost snapshot (Source default) | 2 | 0 | 100 ms | 175 ms | 1.05 m |
| Survive 2 lost in a row | 3 | 0 | 150 ms | 225 ms | 1.35 m |
| Survive 2 lost, plus 20 ms jitter | 3 | 20 | 170 ms | 245 ms | 1.47 m |

Every row of safety costs 50 ms, which at walking speed is 0.3 m of "where you see them versus where they are". The only way to get safety cheaper is to shrink `Δ`, by sending snapshots more often. That is week 13's bandwidth question.

### Move it yourself

Open `examples/w10-lag-lab.html`. The top view is a corridor with your character on one lane and player B on the other. Ghost outlines show where the server has each of you right now and, for B, where B's own screen has B. The bottom view plots position against time for the same run, one line per view, so you can see the gaps between them as distances. Start with all three switches off at 150 ms. Walk with the arrow keys and watch your character lag behind your key presses while B stutters. Turn on prediction, then reconciliation, then interpolation. Your character becomes instant and B becomes smooth, and the ghost of the real B pulls 1.45 m ahead of the B you see. Then turn on 5% loss and drag `D` from 100 down to 50. The pops of Table 2 appear.

### Same idea elsewhere

Each system below is the same formula, `D = kΔ + J`, with a different choice of `k` and `J`.

**Source engine (Valve documentation, current).** Default 20 snapshots per second and `cl_interp 0.1`, so `Δ = 50` and `D = 100`, which is `k = 2`, `J = 0`. Valve's reason is our Table 2. With 100 ms, even if one snapshot is lost there are still two valid snapshots to draw between. Newer Source games compute the period as `max(cl_interp, cl_interp_ratio / cl_updaterate)`, which states `k` directly as a ratio of intervals. If more than one snapshot in a row is lost, Source extrapolates linearly, and only for up to 0.25 s of loss.

**Half-Life (Bernier, 2001).** Yahn Bernier's paper on Half-Life's netcode describes the same buffer at 10 updates per second, `Δ = 100`, with `D = 100` ms, and notes that `D = 200` would let the client miss one whole update. That is `k = 1` and `k = 2` at a slower rate. Half-Life itself sent 20 updates per second by default and interpolated over 100 ms, the same values Source kept.

**Glenn Fiedler's physics demos (Gaffer on Games, 2014).** Fiedler networked a pile of physics cubes with snapshots. His rule of thumb is to survive two lost packets in a row, `k = 3`, plus one or two frames of jitter margin. At 10 snapshots per second that is `3 × 100 + 50 = 350` ms. At 30 per second it drops to 150 ms, and at 60 per second to 85 ms. His numbers make Table 3's point. Doubling the send rate halves the delay for the same safety.

**VALORANT (Riot Games technology blog, July 2020).** Riot runs servers at 128 ticks per second and targets one buffered frame of movement data on the client, one 60 FPS frame or about 16.7 ms in Riot's example, `k = 1` at a much smaller `Δ`. Players can raise the client buffering in the settings to trade latency for smoothness on a bad connection. A competitive shooter at 128 Hz chooses `k = 1` because every millisecond of `D` becomes peeker's advantage (week 11).

Four systems, one decision. Choose how many missing snapshots you can survive, then pay `Δ` milliseconds for each one.

### Design judgment

- **Interpolate what the player cannot control, predict what they can.** The local player is predicted, everyone else interpolated. Mixing them, such as predicting a remote player, needs their future keypresses and fails in the way extrapolation fails.
- **Choose `k` from your loss data, not from a default.** Week 2's burst model says what fraction of losses come in pairs. On a network with `q = 0.5`, half of all losses are bursts, and `k = 2` fails on each of them.
- **Buy safety with send rate when you can.** `D = kΔ`, so safety costs latency in proportion to `Δ`. VALORANT and Fiedler's 60 Hz demo pay in bandwidth to keep `D` small. An MMO with 200 players in view can't, so it accepts a larger `D` (week 13).
- **Extrapolate briefly, then stop.** Extrapolation hides a short gap for an entity moving in a straight line and invents motion for everything else. Cap it, as Source does at 0.25 s, and hold after that. A frozen player on a lagging connection is honest. A player running through a wall is not.
- **Know who pays.** Interpolation delay makes you see others late, so it slows *your* reactions. Valve notes that it gives a moving player a small advantage over a stationary one, because the mover sees the stationary target at its real place while the target sees the mover in the past. The fix for shooting is next week. The fix for reacting is a smaller `D`.

### Check this example

1. A game sends 30 snapshots per second and wants to survive one lost snapshot with 10 ms of jitter margin. What `D` does the formula give? At 75 ms one-way latency and 6 m/s, how far behind the server is a remote player drawn?
2. In Table 2, suppose the snapshot for 1150 is lost instead of the one for 1100. What does the `D = 100` client draw at client time 1275, and is B's peak visible?
3. A designer halves `D` from 100 to 50 ms at 20 Hz to reduce peeker's advantage. Using week 2's numbers, if 1% of snapshots are lost independently, how often per minute will players see a pop?

<details>
<summary>Answers</summary>

1. `Δ = 33.3` ms, `k = 2`, so `D = 66.7 + 10 = 76.7` ms. Behind the server by `75 + 76.7 = 151.7` ms, which at 6 m/s is 0.91 m.
2. At client time 1275, `t_r = 1100`. Snapshots 1050 and 1100 arrived (1100 at client time 1175), 1150 was lost, and 1200 arrived at 1275. So `t_r = 1100` sits exactly on the 1100 snapshot and the client draws 4.60 m. The peak is visible. After it, the client lerps from 1100 to 1200, which is a straight line from 4.60 to 4.00 and matches the truth, because B moved in a straight line over that span.
3. With `D = Δ` the client extrapolates every time a snapshot is lost. At 20 per second there are 1,200 snapshots a minute, so about 12 losses and roughly 12 extrapolations a minute. Each one pops if B changed direction or speed during the gap. For a strafing player that is often.

</details>

## 3. Building the buffer

The lab asks you to write the buffer. Its core is short.

```python
class InterpolationBuffer:
    def __init__(self, max_extrap_ms=250):
        self.snaps = []                          # (server_time, x), sorted by time
        self.max_extrap_ms = max_extrap_ms

    def sample(self, t_r):
        s = self.snaps
        if t_r > s[-1][0]:                       # ran out: extrapolate, capped
            (ta, xa), (tb, xb) = s[-2], s[-1]
            v = (xb - xa) / (tb - ta)
            return xb + v * min(t_r - tb, self.max_extrap_ms), "extrap"
        for (ta, xa), (tb, xb) in zip(s, s[1:]):
            if ta <= t_r <= tb:                  # the normal case
                alpha = (t_r - ta) / (tb - ta)
                return xa + alpha * (xb - xa), "interp"
        return s[0][1], "hold"                   # older than anything we have
```

Three details make the difference between this sketch and a buffer you can ship.

**Timestamps come from the server.** Each snapshot carries the server tick it describes. Never stamp snapshots with the client's arrival time. Arrival time includes jitter, and interpolating on it would put the jitter straight back into the motion you were trying to smooth. Gambetta's article uses arrival times to keep the explanation short. Real engines use tick numbers.

**The render clock runs smoothly.** The client needs "the server's time now" to compute `t_r`. The first estimate is the newest snapshot's tick time, advanced by the client's own clock since it arrived. But the network delay changes, so the estimate drifts. If you correct it by jumping, every remote entity jumps too. Instead, compare the estimate with each new snapshot and nudge the clock's rate. Run render time 1% fast when the buffer is filling up and 1% slow when it is running dry. At 1%, a 10 ms correction takes a second and nobody sees it. This is the adaptive version of week 2's jitter buffer. VALORANT's server does the same with each client's queue of incoming moves, keeping it as short as possible while still absorbing jitter.

**Old snapshots are thrown away.** Keep the newest snapshot at or before `t_r` and everything after it. Anything older can never be used again.

## 4. What to interpolate, and what not to

Position is the easy case. Real snapshots hold more than position.

**Angles wrap.** A player's facing goes from 350° to 10°. The plain lerp gives `350 + 0.5 × (10 − 350) = 180` at the halfway point, so the model spins most of the way around, the wrong way, in 50 ms. Take the shortest signed difference first:

```python
def lerp_angle(a, b, alpha):
    diff = (b - a + 180) % 360 - 180     # shortest signed difference, in [-180, 180)
    return (a + alpha * diff) % 360

print(lerp_angle(350, 10, 0.5))          # 0.0
```

Rotations in 3D have the same problem in a harder form, and engines use spherical interpolation of quaternions for them. Fiedler's article found that slerp alone was good enough for tumbling cubes.

**Discrete state does not blend.** "Crouching", "reloading", "dead" and the current animation clip have no halfway value. Switch them at `t_b`, when the render time reaches the snapshot that introduced them. Some games switch at `alpha ≥ 0.5` instead. Either way, pick one rule and apply it to every discrete field, or a player's gun will fire while their body is still standing up.

**Teleports must not be interpolated.** A player who respawns 80 m away would otherwise slide across the map in 50 ms. Bernier's paper gives the two standard fixes. The server sets a "do not interpolate" flag in the update, or the client treats any jump longer than a threshold as a teleport, clears the history and snaps. The Source SDK's lag compensation uses the same kind of distance threshold (next week).

**Linear is not always enough.** A lerp moves at constant speed between samples, so a curved path becomes a polygon with a corner at every snapshot. Fiedler switched position to Hermite interpolation, which also matches the velocity at each snapshot, at the cost of sending velocity too. He reported that the artifacts disappeared at 10 snapshots per second. If your entities move in curves and your send rate is low, it is worth the bytes.

**Extrapolation needs its own rules.** When you must extrapolate, cap the time (Source, 0.25 s) and when real data arrives, do not snap to it. Blend toward it over a few frames. Racing games, where extrapolation is the main technique, spend most of their netcode effort on this blend.

## 5. What this costs, in one sentence

Interpolation makes other players look right by showing them late, and "late" at 150 ms round trip and 6 m/s is about 1.5 m. Anything that needs other players' *current* positions, most of all hit detection, now has to account for that gap. If the server checked your shot against where the target is now, you would have to aim 1.5 m ahead of what you see. Week 11 shows how the server rewinds the world to what you saw instead.

## In-class activity (25 minutes)

Pairs. Each pair gets a printed strip of 12 snapshots for one remote player at 20 Hz, with server times, positions, arrival times and two missing rows. The strips differ. Some have a single loss, some a burst of two, and some include a direction change.

1. For `D = 50`, `D = 100` and `D = 150`, compute `t_r` and the drawn position at six marked client times. Mark each as interpolated, extrapolated or held.
2. Mark every frame where the drawn position jumps by more than 0.2 m. Count them for each `D`.
3. Choose `D` for a third-person action game where the remote player's exact position matters for melee range. Justify it in two sentences using your counts and the distance-behind column of Table 3.
4. Swap strips with the next pair and check two of their cells.

Expected output: a filled table, a pop count per `D`, and the chosen `D` with its justification.

## Common misconceptions

- **"Interpolation predicts where the other player will be."** It does the opposite. It only draws positions the server already sent, at a time in the past. Predicting forward is extrapolation.
- **"Interpolation delay is network lag."** It is added by the client on purpose, and it exists even on a LAN. Valve's documentation notes the 100 ms applies on a listen server where server and client share a machine.
- **"Lower `cl_interp` always makes me better."** It shows others more recently only while no snapshots are lost. Below two intervals, each lost snapshot turns into an extrapolation, and with it a pop.
- **"If the local player is predicted, the whole world is current."** Your own character is current. Every other entity is at least `L + D` old, so your screen shows two different moments at once.

## Check yourself

1. A client receives snapshots at 20 Hz. It holds snapshots for server times 2000 (x = 10.0) and 2050 (x = 10.4). One-way latency is 60 ms and `D = 100`. At client time 2210 (on the server's clock), what is `t_r`, and what does the client draw?
2. Interpolate a heading from 20° to 340° at `alpha = 0.25`. What does a plain lerp give, and what does the shortest-arc version give?
3. A strategy game sends unit snapshots at 5 Hz. The designers want to survive one lost snapshot. What `D` is that, and why is it much less of a problem in an RTS than in a shooter?
4. Player B strafes at 6 m/s. You have 40 ms one-way latency, B has 40 ms one-way latency, and `D = 100`. Roughly how far behind B's own screen do you see B?
5. Your buffer receives snapshots stamped 3000, 3050 and 3150, with 3100 missing, and then one stamped 3120 arrives late. What should `add` do with it, and does anything break if the buffer ignores it?

<details>
<summary>Answers</summary>

1. `t_r = 2210 − 60 − 100 = 2050`, which is exactly the 2050 snapshot. The client draws 10.4. At `t_r = 2050` it needs no later snapshot, so it doesn't matter whether 2100 has arrived.
2. Plain lerp: `20 + 0.25 × (340 − 20) = 100°`, turning the long way through 90°. Shortest arc: `diff = (340 − 20 + 180) % 360 − 180 = −40`, so `20 + 0.25 × (−40) = 10°`.
3. `Δ = 200` ms, `k = 2`, `D = 400` ms. Players in an RTS rarely need to react to another unit's exact position within half a second, and Age of Empires' own testing (week 12) found 250 to 500 ms of command latency very playable in that genre. In a shooter, 400 ms would be about 2.4 m of error at walking speed.
4. `L_B + L + D ≈ 40 + 40 + 100 = 180` ms, about `6 × 0.18 = 1.08` m, plus up to one server tick of waiting.
5. Insert it in time order. The buffer can now lerp through 3120, which describes the path between 3050 and 3150 more closely. Ignoring it breaks nothing, but it loses information. A buffer must not append it at the end as if it were newest, or `t_r` will run backwards across it.

</details>

## Lab / assignment hook

[Lab 10, the interpolation buffer](../labs/lab10.md). You implement `lerp`, `lerp_angle`, `InterpolationBuffer.sample` and `render_time`, reproduce Table 2 with the `--check` tests, then sweep `D` from 0 to 200 ms on a clean network and on a network with 5% loss and 20 ms of jitter. The deliverable is a recommended `D` for a given game, backed by your measured pop counts and the distance-behind cost.

## Sources

- Valve Developer Community, "Source Multiplayer Networking" (archived copy of 14 August 2026, web.archive.org). About 20 snapshots per second by default, `cl_interp 0.1` (100 ms) so that one lost snapshot still leaves two to interpolate between, the view lag applying even on a listen server, linear extrapolation (`cl_extrapolate`) for up to 0.25 s of loss (`cl_extrapolate_amount`), the formula `max(cl_interp, cl_interp_ratio / cl_updaterate)`, and the note that interpolation delay gives a moving player a small advantage over a stationary one.
- Bernier, Y. W. (2001). "Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization." Game Developers Conference 2001; republished on the Valve Developer Community (archived copy of 18 June 2026). 100 ms interpolation at 10 updates per second, 200 ms to survive one missed update, Half-Life's default of 20 updates per second and 100 ms, the "flattened" bouncing ball, the position-history method, and teleport handling.
- Gambetta, G. *Fast-Paced Multiplayer*, part III, "Entity Interpolation" (gabrielgambetta.com, accessed September 2026). Dead reckoning for predictable entities such as cars, interpolation for shooter characters, and each player seeing themselves in the present and others in the past.
- Fiedler, G. (2014). "Snapshot Interpolation." Gaffer on Games, 30 November 2014. Interpolation buffer sized to survive two lost packets, about three send intervals, plus one or two frames of jitter margin; 350 ms at 10 packets per second, 150 ms at 30 and 85 ms at 60; Hermite interpolation for position and slerp for orientation; extrapolation is poor for colliding rigid bodies.
- deWet, M. & Straily, D. (2020). "Peeking into VALORANT's Netcode." Riot Games technology blog, 28 July 2020. 128 tick servers, client target of one buffered frame of movement data and servers half a frame on average, the server's per-client move queue kept as short as possible, and a player setting for client network buffering.

## Interactive spec: examples/w10-lag-lab.html

This is the course's signature interactive from `curriculum.yaml`: "toggle prediction/reconciliation/interpolation at 150 ms and watch the ghosts".

**Insight the visual must make obvious:** each technique hides one delay by moving the error somewhere else. With all three on, your own character is exact and instant, and every other player is smooth but drawn about 1.5 m (250 ms) behind where they really are.

**Layout.** Two linked views and a readout strip. Stack vertically at all widths. No horizontal page scroll at 390 px.

1. **Corridor view.** Two horizontal lanes, 0 to 12 m, tick marks every meter. Lane 1 "You": a filled circle for what your screen shows, a hollow square for your authoritative server position. Lane 2 "Player B": a filled circle for what your screen shows of B, a hollow square for B's server position, and a dashed outline circle for "B's own screen" (B's predicted position). Draw a thin bracket between B's drawn circle and B's own-screen ghost, labelled with the distance in meters to two decimals.
2. **Time plot.** Position (y) against time (x), last 2 seconds, scrolling. Lines: your server position, your drawn position, B's own-screen position, B's server position, B as drawn. Dots on the time axis mark snapshot arrivals; lost snapshots are drawn as red crosses at their send time. Backward jumps of your drawn position larger than 1 cm get a small red marker.

**Controls.**
- Three switches: "Prediction", "Reconciliation" (disabled unless prediction is on), "Interpolation". Default all off.
- Round trip slider 0 to 300 ms, step 10, default 150. One-way latency is half the round trip in each direction, for both you and B.
- Interpolation delay `D` slider 0 to 200 ms, step 5, default 100 (active only when interpolation is on).
- Loss slider 0 to 20%, step 1, default 0, independent per snapshot, seeded (seed field, default 10).
- Jitter slider 0 to 40 ms, step 5, default 0, extra one-way delay drawn from `U(0, J)` per snapshot.
- Arrow keys and on-screen Left and Right buttons (hold to walk) move you. A "Demo" button plays a scripted walk: hold right for 2 s, release.
- "Reset" button.

**Simulation.** Your own character must match `labs/lab09-starter/netsim.py` without the snare (`--no-snare`), the same model and constants as the week 8 spec and the week 9 spec (`examples/w09-reconcile-replay.html`): `TICK = 1/60` s, `SPEED = 6.0` m/s (0.1 m per tick), `SNAPSHOT_EVERY = 3` (20 Hz), inputs sent every tick with one-way delay `RTT/2`, `step` rounding `x` to 9 decimals. Per tick, with `now = tick × TICK + 1e-9`, the server runs every input that has arrived (arrival ≤ now) in sequence order, then sends a snapshot on ticks divisible by 3. The client then handles every snapshot that has arrived, then samples, sends and predicts input `seq = tick + 1`. The demo walk is `netsim.py`'s script: +1 for ticks 0 to 119, then 0. Without prediction, you are drawn at the newest snapshot's position. Prediction without reconciliation sets the predicted state to each snapshot. Reconciliation sets it to the snapshot and replays unacknowledged inputs.

Player B is scripted: B's input is +1 for 42 ticks (700 ms), then −1 for 42 ticks, repeating, starting at x = 0. B's own screen is B's predicted position, the sum of B's inputs so far. B's inputs reach the server `RTT/2` later under the same rule as yours. Without interpolation, B is drawn at the newest received snapshot. With interpolation, B is drawn at `t_r = t − RTT/2 − D` (the client knows the offset exactly; jitter is not added to the offset) by lerping the two received snapshots that bracket `t_r`. If no later snapshot has arrived, extrapolate from the newest two for at most 250 ms, then hold. Snapshots are stamped with the server time they describe, never with arrival time.

**Readouts.** Your first visible move after the last key press (ms), your backward-jump count, B's distance behind the server and behind B's own screen (m and ms), B's render mode this frame (interp, extrap, hold), and the fraction of frames extrapolated in the last 10 seconds.

**Test values** (assert on load, no loss, no jitter, RTT 150, D 100). Own character, demo walk: without prediction, first visible move at 183.3 ms and the character stops 183.3 ms after release; prediction only, backward jumps of 0.5, 0.3 and 0.1 m at 83.3, 133.3 and 183.3 ms; prediction and reconciliation, zero backward jumps. Player B, interpolation on: at t = 500 ms, B's own screen 3.000 m, server 2.600 m, drawn 1.550 m; at t = 1000 ms (moving left), own screen 2.400, server 2.800, drawn 3.850. So B is drawn 1.05 m behind the server and 1.45 m behind B's own screen while moving. Interpolation off: B's drawn position steps 2.000, 2.300, 2.600 m at t = 500, 533.3, 583.3 ms (0.3 m per snapshot).

**Buffer test** (a static panel under a "Show the buffer" disclosure, reproducing Table 2): snapshots at server times 1000, 1050, 1150, 1200, 1250 with x = 4.00, 4.30, 4.30, 4.00, 3.70 (1100 lost), each arriving 75 ms after its time. At client times 1175, 1200, 1220, 1225, 1250, 1275, 1300, 1325 the `D = 50` column draws 4.30, 4.45, 4.57, 4.30, 4.30, 4.30, 4.15, 4.00 and the `D = 100` column draws 4.00, 4.15, 4.27, 4.30, 4.30, 4.30, 4.30, 4.30.

**First screen:** all three switches on, RTT 150, the demo walk already played, B strafing, with the bracket reading "1.45 m" and a caption: "You are instant. B is smooth. B is also 1.45 m from where B really is. Turn the switches off one at a time."
