# CS202 · Week 11 — Lag compensation (rewind hit detection)

**Why this matters:** Last week you chose to show other players in the past. That makes them smooth, and it means your crosshair is on a position the target left a quarter of a second ago. Either every player learns to aim ahead by an amount that depends on their ping, or the server rewinds time to check each shot against what the shooter saw. Almost every competitive shooter rewinds. This week you learn how, and you learn to name the cost, which is paid by the player being shot.

**You will be able to:**
- Compute the rewind time the server must apply to a shot, from the shooter's round trip and interpolation delay, and the lead a player would need without it.
- Implement a per-player history buffer and a rewound ray-versus-hitbox test.
- Compute how long a victim can be behind cover, on their own screen, and still be hit, and how a rewind cap changes it.
- Critique a game's lag compensation policy (cap, what is rewound, projectiles, trust in client timestamps) and state who gains and who pays.

**Before class:** Gabriel Gambetta, *Fast-Paced Multiplayer*, part IV, "Lag Compensation" (10 minutes). Yahn Bernier (2001), "Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization", the sections "Lag Compensation" and "Game Design Implications of Lag Compensation". Riot Games technology blog, "Peeking into VALORANT's Netcode" (July 2020), the sections on peeker's advantage.

**Prerequisites from earlier courses:** [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (projecting a target onto a ray). [MA101 week 14, distances and squared distance](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (comparing squared distances with a squared radius). [CS101 week 10, collision basics](../../CS101-programming-for-games-i/lectures/w10-collision-basics-aabb-and-circles.md) (circle hitboxes). [CS202 week 4](w04-server-authority-never-trust-the-client.md) (why the client may not declare its own hits). [CS202 week 10](w10-entity-interpolation.md) (the interpolation delay `D` and the 1.45 m gap this week closes).

**Interactive:** [examples/w11-rewind-hit.html](../examples/w11-rewind-hit.html). Keep it open during section 2.

---

## 1. You are aiming at a ghost

Put last week's numbers together. You play at a 150 ms round trip. Player B runs across your view at 6 m/s. Your client draws B at render time `t_r = now − L − D`, with one-way latency `L = 75` ms and interpolation delay `D = 100` ms. When you click, the click travels to the server, another 75 ms. By the time the server reads your shot, B has moved on for

```
L (snapshot's trip to you) + D (your interpolation delay) + L (your shot's trip back) = RTT + D = 250 ms
```

At 6 m/s that is 1.5 m. A human torso is roughly 0.6 m wide, so treat B's hitbox as a circle of radius 0.3 m, seen from above. If the server tests your shot against B's *current* position, a perfect shot at B's center misses by five hitbox radii.

Before lag compensation, games had two answers. One is to make players **lead** their targets, aiming ahead by `v × (RTT + D)`. That is a skill, but a strange one, because the right amount changes with your ping, the target's speed and the server you joined. The other is to let the client decide hits, which week 4 ruled out. Valve's documentation puts it bluntly. A client that sends "I hit player B" could be a cheat, or a clean client whose packets are modified on the way.

There is a third answer. The server keeps a short history of where every player was, and when your shot arrives, it looks up where B was at the moment you saw B. That is **lag compensation**, also called **rewind** or **backward reconciliation**.

## 2. Worked example: rewinding the target at 150 ms

### The hook

Valve's own networking documentation contains a warning that sounds like a bug report. With lag compensation, it says, you can be hit by an attacker you can't even see anymore, because you already took cover. The server moved your hitboxes back in time, to where you were still exposed. Valve adds that this inconsistency can't be solved in general. Bernier's 2001 paper gives the extreme case. A player with around 500 ms of lag lines up a shot, the target darts around a corner and crouches behind a crate, and the shot still lands. The target says they were "shot around a corner". The shooter says they hit a player standing in the open. Both are right. How can one shot be both fair and unfair, and how far behind cover can you be before the server should say no?

### The model

The shooter's client draws other players at `t_r = t_now − L_down − D` on the server's clock. The shot reaches the server one uplink later. So when the server processes the shot at `t_arrival`, the shooter was looking at

```
t_view  = t_arrival − (L_up + L_down + D) = t_arrival − (RTT + D)
R       = RTT + D                              the rewind, in ms
R_used  = min(R, R_max)                        the server's cap
```

The server keeps each player's position for every tick of the last `R_max` milliseconds. To test a shot it:

1. Computes `t_view` from `R_used`.
2. Moves every *other player* to their recorded position at `t_view`, lerping between the two ticks that bracket it (the same lerp as week 10).
3. Traces the shot against those rewound hitboxes and the world, which does not move.
4. Puts every player back.

Two quantities fall out of the model.

```
lead needed without rewind           = v × R
lead still needed with a cap         = v × max(0, R − R_max)
victim's time behind cover when hit  = W = RTT_shooter + D + RTT_victim     (up to R_max + RTT_victim)
```

The last line needs a word. The victim's own screen runs ahead of the server by their uplink, because their movement is predicted. The server learns they reached cover `L_up,victim` after their screen showed it. A shot aimed at their last exposed position can arrive up to `R` later and still be valid. The death message takes another `L_down,victim` to reach them. Add the three and you get `W`.

### Numbers you can check

Throughout, `D = 100` ms, `v = 6` m/s, hitbox radius 0.3 m, and the victim's round trip is 40 ms.

**Table 1. The lead a player needs without rewind.** A shot aimed at the center of what the screen shows misses whenever the lead exceeds the hitbox radius.

| Shooter RTT | Rewind `R = RTT + D` | Lead `v × R` | Center shot without rewind | With rewind |
|---|---|---|---|---|
| 0 ms (LAN) | 100 ms | 0.60 m | miss | hit |
| 50 ms | 150 ms | 0.90 m | miss | hit |
| 100 ms | 200 ms | 1.20 m | miss | hit |
| 150 ms | 250 ms | 1.50 m | miss | hit |
| 250 ms | 350 ms | 2.10 m | miss | hit |
| 400 ms | 500 ms | 3.00 m | miss | hit |

The first row surprises people. Even on a LAN, with no network delay at all, the 100 ms interpolation delay alone puts a running target 0.6 m, two radii, from where you see it. This is why Valve's documentation says you do *not* have to lead your aim, because lag compensation knows about interpolation and corrects for it. The interpolation term is in the rewind because the client added it.

Lab 11's simulator, `rewind.py`, has a target strafing left and right at 6 m/s and a shooter who fires every 70 ms at exactly what their screen shows. With rewind it hits 100% of shots at every RTT. Without rewind it hits 10%, all of them near the moments the target reverses direction and briefly stands still.

**Table 2. The victim's side.** The victim runs behind a wall at 6 m/s. The shooter fires on the last frame their screen shows a sliver of the victim. How long has the victim's own screen shown them fully hidden when the death message arrives?

| Shooter RTT | `W = RTT_s + D + RTT_v` | Victim's distance behind the wall edge at 6 m/s |
|---|---|---|
| 0 ms | 140 ms | 0.84 m |
| 50 ms | 190 ms | 1.14 m |
| 100 ms | 240 ms | 1.44 m |
| 150 ms | 290 ms | 1.74 m |
| 250 ms | 390 ms | 2.34 m |
| 400 ms | 540 ms | 3.24 m |

Verify the 150 ms row. `150 + 100 + 40 = 290` ms, and `6 × 0.29 = 1.74` m. The lab's simulator prints 289 ms, because its shooter fires 1 ms before the victim is fully hidden. At 150 ms the victim is nearly two meters around the corner when they die. From their side it looks like the shot bent.

**Table 3. What a cap does.** Now add `R_max = 200` ms, a design choice made for this example.

| Shooter RTT | `R` | `R_used` | Residual lead `v × (R − R_used)` | Center shot | Longest cover window |
|---|---|---|---|---|---|
| 50 ms | 150 ms | 150 ms | 0 m | hit | 190 ms |
| 100 ms | 200 ms | 200 ms | 0 m | hit | 240 ms |
| 150 ms | 250 ms | 200 ms | 0.30 m | grazes the edge | 240 ms |
| 250 ms | 350 ms | 200 ms | 0.90 m | miss | 240 ms |
| 400 ms | 500 ms | 200 ms | 1.80 m | miss | 240 ms |

The cap does two things at once. It limits the victim's worst case to `R_max + RTT_v = 240` ms, whoever is shooting. And it hands the latency back to the high-ping shooter, who must now lead by `v × (R − R_max)`. The cap decides who pays for a bad connection. Below it, the victim pays. Above it, the shooter does.

### Move it yourself

Open `examples/w11-rewind-hit.html`. The left view is the shooter's screen, the right view is the server at the moment the shot arrives. Both show the same top-down corridor with a wall. On the shooter's screen, the target is where interpolation put it. On the server, the target is further along, and a dashed outline marks where the rewind puts it. Click to fire at the target on the shooter's screen. The shot's ray is drawn in both views. Toggle rewind off and watch the ray pass 1.5 m behind the real target. Toggle it on and the dashed outline lands under the ray. Then switch to the cover scenario and drag the shooter's RTT from 0 to 400. A timeline under the views shows the victim's screen, the moment they reached cover, and the moment the death message arrived. Set a cap and watch the timeline stop growing while the shooter's view starts showing a lead marker.

### Same idea elsewhere

Every system below computes some version of `t_view = t_arrival − R`, with a limit on `R`.

**Source engine (Valve documentation, current, and the Source SDK 2013 code).** The documentation gives the rule as command execution time equals current server time minus packet latency minus client view interpolation, which is our `R = RTT + D`. The server keeps a history of all players' positions for one second and moves only players back, not the world. In the Source SDK 2013 code, the history is pruned after `sv_maxunlag`, default 1.0 s, so `R_max = 1000` ms. The client sends the tick it was rendering with each command, and the server rewinds to that tick minus the interpolation ticks. But if that disagrees with the server's own latency-based estimate by more than 200 ms, the server ignores the client's tick and uses its estimate. That clamp exists because the tick comes from the client, and week 4 taught you what to do with client claims. The code also refuses to rewind a player who moved more than 64 units between records, treating it as a teleport, the same rule as week 10's interpolation.

**Half-Life (Bernier, 2001).** The paper describes the same algorithm. Compute the player's latency, find the stored updates around the target time, move the other players back to where they were when the command was created, including both latency and interpolation, then restore them. It notes that more than position may need to go back, such as whether a player was crouching or dead. Half-Life did not lag compensate projectiles at all, only instant-hit weapons. A rocket lives on the server for many ticks, and there is no single "time the shooter saw" to rewind to.

**VALORANT (Riot Games technology blog, July 2020).** The server rewinds the world to what the shooter was looking at when they pulled the trigger, so players do not have to lead by an amount that depends on their latency. Riot also caps the rewind, with the reason from our Table 2. Without a limit, a player with 500 ms of latency could kill you half a second after you moved behind cover. Riot does not publish its limit. It says the limits are tuned to stop abuse while giving most players in each region near-perfect hit registration. In our terms, `R_max` is set just above the `R` of the typical player in a region.

**Gambetta's series (part IV).** Gambetta tells the same story in its simplest form. The client sends the shot with its exact timestamp and aim, and the server, which keeps timestamped state, reconstructs the world as that client saw it and judges the shot there. In our terms the client reports `t_view` directly and `R` is implied. His summary of the trade matches Bernier's. The shooter gets the hit they aimed for, and a target who just reached cover can still be shot a moment later. He calls it somewhat unfair and still the most agreeable option, because missing a shot that could not miss would be worse.

Four systems, one rule. Rewind by what the shooter could not help, `RTT + D`, and stop at a cap that decides where the unfairness moves.

### Design judgment

- **Favor the shooter, knowingly.** Rewinding means the shooter's screen is the truth for their shot. That makes aiming a pure skill and makes dying behind cover possible. Bernier argues that in normal combat the victim rarely notices, because a target running across your view can't see where you are aiming anyway. The case they do notice is the corner, and the cap is how you limit it.
- **Pick `R_max` from your latency data.** Set it just above the `R` of most of your players in a region, as Riot describes. Players above it must lead, which is the honest cost of their connection. A generous cap, like Source's full second, makes high-ping players deadly and low-ping players frustrated.
- **Never trust the client's clock without a bound.** The client's reported render tick is more precise than any server estimate, so use it, but clamp it to the server's own estimate, as the Source SDK does with its 200 ms check. A cheat that claims to have seen the world 800 ms ago gets a free "backtrack" through every corner.
- **Rewind only what the shooter aimed at.** Players, and whatever determines their hitboxes (pose, crouch, alive). Not the world, not projectiles already in flight. Anything you rewind must also be put back exactly.
- **Decide projectiles separately.** Slow projectiles are usually simulated in server time and not compensated, as in Half-Life. Another option for fast projectiles is to spawn them further along their path, by the distance they would have covered during the shooter's latency. Either choice changes how a weapon feels at high ping. Write it down.
- **Lag compensation doesn't remove peeker's advantage.** It fixes aiming. It does not change the fact that the victim sees the peeker late. Section 4 measures that.

### Check this example

1. A shooter has a 60 ms round trip and uses a 30 Hz snapshot rate with `cl_interp_ratio 2`. What is `R`? How far must they lead a target running at 6 m/s if the server does not rewind?
2. With `R_max = 200` ms and `D = 100`, what is the largest RTT at which a shooter needs no lead? What lead does a 180 ms shooter need?
3. A victim with a 20 ms round trip is shot by a player with a 100 ms round trip and `D = 50`. How long could the victim have been behind cover, on their own screen, when the death message arrives?

<details>
<summary>Answers</summary>

1. `D = 2 / 30 s = 66.7` ms, so `R = 60 + 66.7 = 126.7` ms. The lead is `6 × 0.1267 = 0.76` m.
2. `R ≤ R_max` means `RTT + 100 ≤ 200`, so RTT up to 100 ms. At 180 ms, `R = 280`, residual `80` ms, lead `6 × 0.08 = 0.48` m.
3. `W = 100 + 50 + 20 = 170` ms.

</details>

## 3. The rewind in code

Lab 11 builds the server side. Three pieces.

```python
from collections import deque

class History:
    """Positions of one player, one record per server tick, oldest first."""
    def __init__(self, max_unlag_ms=1000, tick_ms=1000 / 60):
        self.records = deque(maxlen=round(max_unlag_ms / tick_ms) + 1)

    def record(self, t_ms, pos):
        self.records.append((t_ms, pos))          # called once per tick, after simulation

    def position_at(self, t_ms):
        r = self.records
        if t_ms <= r[0][0]:  return r[0][1]       # older than we keep: clamp
        if t_ms >= r[-1][0]: return r[-1][1]
        for (ta, pa), (tb, pb) in zip(r, list(r)[1:]):
            if ta <= t_ms <= tb:
                a = (t_ms - ta) / (tb - ta)
                return (pa[0] + (pb[0] - pa[0]) * a, pa[1] + (pb[1] - pa[1]) * a)

def ray_hits_circle(origin, direction, center, radius):
    dx, dy = direction
    n = (dx * dx + dy * dy) ** 0.5
    dx, dy = dx / n, dy / n
    cx, cy = center[0] - origin[0], center[1] - origin[1]
    along = cx * dx + cy * dy                     # dot product: distance along the ray
    if along < 0:
        return False                              # behind the shooter
    perp_sq = cx * cx + cy * cy - along * along   # Pythagoras, no square root needed
    return perp_sq <= radius * radius

def server_hit(history, arrival_ms, aim, rtt_ms, interp_ms, max_unlag_ms=1000):
    t_view = arrival_ms - min(rtt_ms + interp_ms, max_unlag_ms)
    return ray_hits_circle((0, 0), aim, history.position_at(t_view), 0.3)
```

The ray test is MA101's dot product and squared-distance comparison. Project the target's center onto the ray to get `along`, then compare the squared perpendicular distance with the squared radius. Real games test capsules or boxes per body part and trace against world geometry too, but the rewind is the same.

**What it costs.** Memory is small. A server at 60 ticks per second with 32 players, keeping one second at an illustrative 48 bytes per record (position, angles, a hitbox pose index), stores `32 × 61 × 48 = 93,696` bytes, under 100 KB. CPU is the real cost. Every shot moves up to 31 players back and forward. A busy 32-player server can process hundreds of shots per second. Engines first test the ray against a bounding box around each player's whole recorded path, and rewind only the players the ray could possibly touch.

**Where the timestamp comes from.** The code above uses the server's measured RTT. That is the fallback. The precise method is the one in the Source SDK. Each command carries the tick number the client was rendering and its interpolation amount, so the server knows exactly which frame the shooter saw, down to the tick. The server then checks that claim against its own estimate and falls back when they disagree by too much.

## 4. The other half: peeker's advantage

Lag compensation makes the shooter's view authoritative for the shooter's shots. It says nothing about when the *defender* sees the shooter.

Picture a defender holding a corner, and an attacker who walks out from behind it. The attacker sees the defender as soon as the attacker's own predicted movement clears the corner, which is instant. The defender sees the attacker only after the attacker's movement has gone up to the server, been processed, come down to the defender, and waited in the defender's interpolation buffer. Riot's July 2020 article writes the head start as the holder's reaction time needing to beat the peeker's by the round-trip latency plus the buffering on both sides.

```
peeker's advantage = RTT + server buffering + client buffering
```

Riot's example assumes two frames of server buffering (half a frame waiting to be queued, half a frame of network buffering, one frame to apply and send the move) and three frames on the client (the same, except a full frame of network buffering, plus half a frame of render delay). With 128 tick servers, a 35 ms round trip and a 60 FPS client:

```
35 + 2 × (1000 / 128) + 3 × (1000 / 60) = 35 + 15.6 + 50.0 = 100.6 ms       (Riot: about 101 ms)
```

At 144 FPS the client term drops to `3 × 6.9 = 20.8` ms and the total to about 71 ms, which is the 49% reduction Riot reports against its unoptimized baseline.

Now plug in this course's setup. Our interpolation delay alone is `D = 100` ms, twice Riot's entire client buffering, and our round trip is 150 ms. The peeker's head start is over a quarter of a second, before counting ticks and frames. That is why a tactical shooter, where one shot kills, spends money on 128 Hz servers and data centers near players, and why it runs `D` at one frame instead of two intervals. Lag compensation cannot buy any of this back. Only lower latency and less buffering can.

## 5. Lag compensation beyond shooters

The technique applies whenever a player targets something by aiming at a moving on-screen position.

- **Action MMOs and hack-and-slash games** with free aim or skill shots face the same problem, and many rewind for area checks too. It is one topic of MMO404, advanced networked simulation (see the [MMO404 syllabus](../../MMO404-advanced-networked-simulation/syllabus.md)).
- **Tab-target MMOs** mostly avoid it. The player selects a target, and the server checks range and line of sight against current positions when the cast finishes. Nothing is aimed at a screen position, so nothing needs rewinding. A small range tolerance, a meter or two, often absorbs the difference instead.
- **Melee** is a special case. The attacker sees the target in the past, but the target also sees the attacker in the past, so both are rewound or neither is, and designers often widen melee hitboxes instead.
- **Anti-cheat.** A "backtrack" cheat claims an old render tick to shoot where enemies used to be. The server-side clamp is the defense. MMO309 covers the wider topic (see the [MMO309 syllabus](../../MMO309-security-anti-cheat-and-anti-bot/syllabus.md)).

## In-class activity (25 minutes)

Groups of three. One student is the shooter, one the target, one the server. Use a printed strip of the target's positions every 16.7 ms (60 Hz ticks) over one second, running at 6 m/s past a wall edge at 0.5 s.

1. The shooter has a 120 ms round trip and `D = 100`. The shooter picks a frame to fire at, on the last moment the target is visible. The server computes `t_view`, looks up the rewound position (lerping between ticks), and decides the hit.
2. The target, with a 50 ms round trip, computes how long they had been behind cover on their own screen when the death message arrived.
3. Repeat with `R_max = 150` ms. Does the shot still count? If not, how far should the shooter have led?
4. As a group, choose an `R_max` for a game whose players' round trips are 30 to 90 ms in one region and 150 to 200 ms in another. Write one sentence for each region on who pays.

Expected output: the three numbers from steps 1 to 3 and a one-paragraph cap policy.

## Common misconceptions

- **"Lag compensation means the client decides hits."** The server decides every hit. It only changes the moment it tests against, and it limits how far back that moment may be.
- **"Low ping players are penalized by lag compensation."** As shooters they are unaffected. As targets they absorb the high-ping shooter's `R`, which is what the cap limits. The penalty belongs to the connection that was slow.
- **"With lag compensation I never need to lead."** Only up to the cap, and only for weapons that are compensated. Slow projectiles and anything above `R_max` still need a lead.
- **"Rewinding fixes peeker's advantage."** It fixes the shooter's aim. The defender still sees the peeker late by `RTT + buffering`, and nothing on the server can change what the defender's screen showed.

## Check yourself

1. The server runs at 64 ticks per second and keeps history for 400 ms. How many records per player does the ring buffer need? For 10 players at 40 bytes per record, how much memory?
2. Records exist at 1000.0 ms (x = 3.0) and 1015.625 ms (x = 3.1). A shot needs the position at 1010 ms. What does the server use?
3. A ray starts at (0, 0) with direction (0, 1). A target's rewound center is at (0.25, 12). Radius 0.3. Hit or miss? Show the dot product and the squared distance.
4. A game sets `R_max = 150` ms and `D = 50` ms. A player at 180 ms round trip complains that they "have to aim ahead". By how much, for a target at 5 m/s? What would you tell them?
5. Why does a well-designed server rewind to the client's reported render tick instead of using only its own RTT estimate, and why must it still check that tick?

<details>
<summary>Answers</summary>

1. One tick is `1000 / 64 = 15.625` ms, and `400 / 15.625 = 25.6` intervals. Round up to 26 intervals, which need 27 records and cover 406 ms. `10 × 27 × 40 = 10,800` bytes.
2. `alpha = (1010 − 1000) / 15.625 = 0.64`, so `x = 3.0 + 0.64 × 0.1 = 3.064`.
3. `along = 0.25 × 0 + 12 × 1 = 12`. Squared distance to the center `0.25² + 12² = 144.0625`. Perpendicular squared `144.0625 − 144 = 0.0625`, which is `0.25²`, less than `0.3² = 0.09`. Hit.
4. `R = 180 + 50 = 230` ms, residual `80` ms, lead `5 × 0.08 = 0.4` m. Tell them the cap protects the players they shoot, and that their connection, not the game, puts the target 0.4 m ahead. A closer server would fix it.
5. The client knows exactly which frame it drew, while the server's RTT estimate is smoothed and lags behind jitter, so the reported tick is more accurate. But it is a client claim. A cheat could report an older tick to shoot where players used to be. The server accepts the claim only within a tolerance of its own estimate and never beyond `R_max`.

</details>

## Lab / assignment hook

[Lab 11, rewind hit detection](../labs/lab11.md). You implement `History.position_at`, `ray_hits_circle` and `rewind_time`, pass the `--check` tests built from Tables 1 to 3, then measure hit rates with and without rewind and the victim's cover window across round trips. The deliverable is a one-page cap policy for a given player population, with numbers for who pays at each ping.

## Sources

- Valve Developer Community, "Source Multiplayer Networking" (archived copy of 14 August 2026, web.archive.org). Command execution time as server time minus packet latency minus client view interpolation; history of all player positions for one second; only players are moved back; no need to lead because lag compensation knows about interpolation; being hit after taking cover; client-side hit detection rejected because of cheats and man-in-the-middle proxies.
- Valve Software, Source SDK 2013, `src/game/server/player_lagcompensation.cpp` (GitHub, ValveSoftware/source-sdk-2013, master branch, accessed September 2026). `sv_maxunlag` default 1.0 s and history pruned beyond it; target tick is the command's tick count minus the interpolation ticks; fallback to a latency-based target when the two differ by more than 0.2 s; `sv_lagcompensation_teleport_dist` default 64 units.
- Bernier, Y. W. (2001). "Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization." Game Developers Conference 2001; Valve Developer Community (archived copy of 18 June 2026). The lag compensation algorithm, extra state such as crouching or dead moved back too, the "shot around a corner" case at around 500 ms, the argument from field of view, and projectiles not lag compensated in Half-Life.
- Gambetta, G. *Fast-Paced Multiplayer*, part IV, "Lag Compensation" (gabrielgambetta.com, accessed September 2026). The client sends the shot's timestamp and aim; the server reconstructs the world as that client saw it; a target can be shot shortly after taking cover, a trade the author judges worth making.
- deWet, M. & Straily, D. (2020). "Peeking into VALORANT's Netcode." Riot Games technology blog, 28 July 2020. Peeker's advantage as round-trip latency plus buffering on both sides; two frames of server buffering and three of client buffering; 128 tick, 35 ms, 60 FPS gives about 101 ms; 144 FPS gives about 71 ms, a 49% reduction; rewind for hit registration with unpublished limits, and the 500 ms example.

## Interactive spec: examples/w11-rewind-hit.html

**Insight the visual must make obvious:** the server tests your shot against where the target was when you saw it, `RTT + D` ago. Without that, a perfect shot misses by `v × (RTT + D)`. With it, the victim can die up to `RTT_shooter + D + RTT_victim` after reaching cover, and a cap trades one unfairness for the other.

**Layout.** Two side-by-side views (stacked under 700 px) plus a timeline strip and a readout panel.

1. **Shooter's screen** (left). Top-down corridor 10 m deep (shooter at the bottom center, (0, 0), facing +y) and 8 m wide (x from −4 to +4). Target lane at y = 10. A wall occupies x > 0 near the lane, drawn as a block from (0, 9) to (4, 11) in the cover scenario only. The target is a circle of radius 0.3 m drawn where the shooter's client shows it, the true position at `t − RTT/2 − D`.
2. **Server at arrival** (right). Same geometry. Solid circle: the target's position at the arrival time. Dashed circle: the rewound position at `t_view = t_arrival − min(RTT + D, R_max)`. Faint circle: the shooter's-screen position, for comparison. The shot's ray is drawn in both views from (0, 0) toward the aim point. Label HIT or MISS in large text, with the perpendicular distance in meters.
3. **Timeline strip.** A horizontal ms axis from −100 to 700 with markers: "victim hidden on own screen", "victim hidden on server", "shooter's screen shows last sliver", "shot arrives at server", "death reaches victim". A shaded span between the first and last markers is labelled `W = … ms`.

**Controls.**
- Scenario: "Strafe" (target moves at `v`, reversing every 700 ms between x = −2.1 and +2.1) or "Cover" (target runs right from x = −2 at `v`; the wall hides it once its center passes x = 0.3).
- Shooter RTT slider 0 to 400 ms, step 10, default 150. Victim RTT slider 0 to 200, step 10, default 40.
- `D` slider 0 to 200 ms, step 5, default 100.
- Speed `v` slider 2 to 10 m/s, step 0.5, default 6.
- Rewind switch (default on). Cap `R_max` slider 50 to 1000 ms, step 10, default 1000.
- Strafe scenario: click or tap on the shooter's view (or press Space to fire at the target's displayed center) to fire; the aim point is the click position. A "Fire at center" button is the keyboard-accessible equivalent. Cover scenario: a "Fire at last sliver" button fires at the moment the shooter's screen shows 6 mm of the victim past the wall edge (1 ms before the victim is fully hidden at the default 6 m/s), aiming 5 mm left of the wall edge at (−0.005, 10).
- Pause/step buttons that freeze the simulation and step one 60 Hz tick.

**Model.** Server ticks at 60 Hz and records the target position each tick; history interpolates linearly between ticks. Hit test: ray from (0, 0) through the aim point against a circle of radius 0.3 using `along = c · d̂`, reject if `along < 0`, hit if `|c|² − along² ≤ r²`. Without rewind, test against the position at arrival. With rewind, test at `t_view`. Residual lead `v × max(0, RTT + D − R_max)`. Cover window `W = arrival + RTT_v/2 − (t_hidden − RTT_v/2)`.

**Readouts.** `R = RTT + D`, `R_used`, lead needed without rewind (`v × R`), residual lead, perpendicular miss distance of the last shot, HIT/MISS, and in the cover scenario `W` in ms and the victim's distance behind the wall edge (`v × W`).

**Test values** (assert on load). `v = 6`, `D = 100`, radius 0.3, victim RTT 40. Lead without rewind for shooter RTT 0, 50, 100, 150, 250, 400: 0.60, 0.90, 1.20, 1.50, 2.10, 3.00 m, all MISS for a center shot, all HIT with rewind. Cover window for the same RTTs with no cap: 139, 189, 239, 289, 389, 539 ms (firing with 6 mm of the victim showing, 1 ms before it is fully hidden). With `R_max = 200`: RTT 0, 50, 100 give 139, 189, 239 ms; RTT 150 and above give MISS. Residual lead with `R_max = 200` at RTT 150, 250, 400: 0.30, 0.90, 1.80 m. Ray test: aim (0, 1) against center (0.25, 12) is a HIT with perpendicular distance 0.25 m.

**First screen:** Strafe scenario, shooter RTT 150, rewind off, one center shot already fired and shown as MISS by 1.50 m, with a caption: "You hit what you saw. The server disagreed by 1.5 m. Turn on rewind."
