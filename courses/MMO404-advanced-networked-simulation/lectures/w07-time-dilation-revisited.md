# MMO404 · Week 07 — Time dilation revisited

**Why this matters:** MMO302 gave you time dilation as a steady-state formula and a smoothing controller for one node. A live cluster adds three things that formula does not see. The node learns about a fleet only after the fleet has cost it a second. The load is noisy and changes every second. And a fight spreads over several systems and several machines, some of which the operator prepared and some of which it did not. This week you build the controller and the node plan that cope with all three.

**You will be able to:**
- Compute the backlog a node builds when a fleet arrives, for a controller that only measures the past, with a given aim and payback time.
- Explain why a controller should drop game speed fast and raise it slowly, and measure the effect on backlog and speed jitter in a seeded run.
- Compute the game speed of every server when servers that interact must share one clock, and find where a gate or boundary breaks the coupling.
- Plan a node reinforcement for a fight across several systems, and compute what it buys the fight and its neighbours.

**Before class:** Reread [MMO302 week 12](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md), sections 2 and 3, and your MMO302 lab 12 solution. CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), the part on how the server picks the speed. CCP Falcon, "Fleet Fight Notifications & You!" (EVE Online news, 31 March 2016) and "Changes To The Fleet Fight Notification System!" (EVE Online news, 22 January 2018), both short. Glenn Fiedler, "Fix Your Timestep!" (Gaffer on Games, June 2004), from "Free the physics" to the end.

**Prerequisites from earlier courses:** [MMO302 week 12, single-shard architectures and time dilation](../../MMO302-mmo-server-architecture/lectures/w12-single-shard-architectures-and-time-dilation.md) (the model `f = clamp(C / W(n), f_min, 1)`, the backlog, the smoothing controller with its aim, and which clocks dilate; this lecture starts from all four). [MMO302 week 5, tick rate for MMOs vs shooters](../../MMO302-mmo-server-architecture/lectures/w05-tick-rate-for-mmos-vs-shooters.md) (what happens when a tick does not fit). [MMO302 week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (why you cannot add a machine in the middle of a fight). [CS202 week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) (the client clock that must follow the server's). [MMO404 week 2](w02-seamless-worlds-and-boundary-handoff.md) (servers that share a border) and [week 6](w06-massive-battles.md) (the levers left in a massive battle).

**Interactive:** [w07-tidi-controller.html](../examples/w07-tidi-controller.html). Keep it open during sections 2 and 3.

---

## 1. Where MMO302 stopped

MMO302 week 12 built the model this lecture uses, so here it is only restated in the same notation. One node runs one crowded solar system.

```
W(n) = a × n + b × n²        CPU-seconds to simulate one game-second with n pilots
a = 0.3 ms,  b = 1 µs,  C = 1 CPU-second per real second,  f_min = 0.1
f = clamp(C / W(n), f_min, 1)
```

`f` is the time-dilation factor, the game-seconds that pass per real second. The **backlog** is work the node owes from earlier seconds. With these constants MMO302 found that dilation starts at 861 pilots and reaches EVE's 10% floor at about 3,016. It then built a controller that moves `f` a share `α` of the way to a target each second, aimed at a fraction `aim` of `C`, and showed that a controller aimed at 100% never repays a backlog it builds while it lags behind a warp-in. Its section 4 sorted the game's clocks into those that dilate and those that keep real time. You need all of that. None of it is repeated here.

Three things were left out.

1. **The node only sees the past.** MMO302's controller computes this second's target from this second's `W(n)`, before the second runs. That is why its `α = 1` rows show no backlog at all. A real node knows how long the last second took. When a fleet jumps in, the first second after the jump runs at the old speed and overruns, whatever the controller does.
2. **The load is noisy and keeps changing.** A second in which 400 pilots activate modules costs more than one in which they sit still. A controller that follows every measurement changes the game speed every second, and players feel it.
3. **A fight lives on more than one node.** Fights spill across neighbouring systems. Some of those systems sit on hardware prepared for the fight, and some share a node with quiet systems. Where servers share a border, their clocks interact.

This lecture takes the three in order. Two words are new. We write the backlog as `q`, in CPU-seconds. With `C = 1`, a backlog of 3 means a command issued now waits about 3 extra real seconds, which is what players call **lag**. The **payback time** `τ` is how fast the controller tries to repay `q`.

## 2. Worked example: a controller that learns only from the past

### The hook

EVE Online lets fleet commanders warn CCP about a fight ahead of time through its fleet fight notification tool. CCP then places the named solar systems on a dedicated high-performance node. In January 2018 CCP explained a detail that confused many commanders. Nodes are mapped at the daily downtime, so a request has to arrive before the downtime that precedes the fight. Two years earlier, after a fight in the Tribute region, CCP had reminded players that the tool reinforces only the systems named in the request. Only part of that constellation had been reinforced, and performance varied from system to system.

So the node a fight lands on is fixed for the whole day. If the fight arrives unannounced, or spreads to a system nobody named, the only thing left to react is the node's dilation controller. It has to handle a fleet of 1,500 pilots jumping in during a single second, on hardware it cannot change, using nothing but measurements of seconds that have already happened. How well can it do?

### The model

Start from MMO302's controller and change two things. The controller now acts after it measures. And its target sets aside capacity to repay the backlog. Each real second `t`, the node does three things in this order.

```
1. simulate:  demand   = f_t × m_t                    m_t = W(n_t), measured as the second runs
2. account:   q_{t+1}  = max(0, q_t + demand − C)
3. control:   target   = clamp((aim × C − q_{t+1} / τ) / m_t, f_min, 1)
              f_{t+1}  = f_t + α × (target − f_t)       α = α_down if target < f_t, else α_up
```

- `m_t` is the measured cost of one game-second during second `t`. The speed `f_t` was chosen before `m_t` was known.
- `aim` is MMO302's aim, the share of `C` the controller plans to use. `aim = 0.9` leaves 10% headroom.
- `τ` is the payback time in seconds. The term `q / τ` sets aside enough capacity to clear the current backlog in `τ` seconds. Without it (`τ` off), only the headroom repays the backlog, as in MMO302.
- `α` is the gain. This week it can differ by direction: `α_down` when the controller slows the game, `α_up` when it speeds it up. Section 3 is about why.

### Numbers you can check

A node holds 500 pilots at full speed, because `W(500) = 0.15 + 0.25 = 0.4 < 1`. At time 0 a fleet jumps in and the count becomes 2,000. Now `W(2,000) = 0.6 + 4.0 = 4.6`.

Second 0 runs at the old speed `f = 1`. The node is asked for 4.6 CPU-seconds and has 1, so it ends the second 3.6 CPU-seconds behind. No controller that acts after measuring can prevent this. What the controller decides is how the next minute goes. Take `α = 1` in both directions for now.

- **Aim 100%, no payback.** The target is `1 / 4.6 = 0.217`. Demand is then exactly `C`, so the backlog stops growing and stays at 3.6. Every command waits 3.6 extra seconds for the rest of the fight.
- **Aim 90%, no payback.** The target is `0.9 / 4.6 = 0.196`. Demand is 0.9, so 0.1 CPU-seconds per second go to the backlog. Clearing 3.6 takes 36 seconds.
- **Aim 90%, `τ = 5`.** After second 0 the target is `(0.9 − 3.6 / 5) / 4.6 = 0.039`, below the floor, so second 1 runs at `f = 0.1`. Demand is 0.46, and the backlog falls by 0.54 per second, to 3.06. As the backlog shrinks, the payback term shrinks too, and `f` climbs back toward 0.196.

The code runs all three for 60 seconds.

```python
A, B, C, FLOOR = 0.0003, 0.000001, 1.0, 0.1   # MMO302 week 12's node

def work(n):
    """CPU-seconds to simulate one game-second with n pilots."""
    return A * n + B * n * n

def run(pilots, aim=1.0, tau=None, a_down=1.0, a_up=1.0):
    f, q, rows = 1.0, 0.0, []
    for n in pilots:                      # one real second per step
        m = work(n)                       # measured cost of a game-second, after the fact
        q = max(0.0, q + f * m - C)       # backlog: CPU-seconds still owed
        rows.append((f, q))
        want = aim * C - (q / tau if tau else 0.0)
        target = min(1.0, max(FLOOR, want / m))
        f += (a_down if target < f else a_up) * (target - f)
    return rows

fleet = [2000] * 60
for name, kw in [("aim 100%", dict(aim=1.0)), ("aim 90%", dict(aim=0.9)),
                 ("aim 90%, tau 5", dict(aim=0.9, tau=5))]:
    rows = run(fleet, **kw)
    clear = next((t for t in range(1, 60) if rows[t][1] < 0.05), None)
    backlog = " ".join(f"{rows[t][1]:5.2f}" for t in (1, 5, 10))
    game = sum(f for f, q in rows)
    print(f"{name:14s} f(1)={rows[1][0]:.3f} backlog@1,5,10s {backlog}  clear {str(clear):>4}  game-s {game:5.1f}")
```

```
aim 100%       f(1)=0.217 backlog@1,5,10s  3.60  3.60  3.60  clear None  game-s  13.8
aim 90%        f(1)=0.196 backlog@1,5,10s  3.50  3.10  2.60  clear   36  game-s  12.5
aim 90%, tau 5 f(1)=0.100 backlog@1,5,10s  3.06  1.09  0.02  clear   10  game-s  12.0
```

Each row stores the backlog at the end of that second, so `rows[1]` is the state one second after the jump. Read the backlog columns as "extra seconds a new command waits."

The first row is the trap MMO302 showed for a slow controller. Aimed at 100%, a backlog, once built, never clears. The difference here is that even the fastest possible controller builds one, because the overrun happens before any measurement exists. Headroom is no longer optional for a controller that only sees the past.

Now read the last column, the game-seconds that passed in the first real minute. The payback controller clears a 3.6-second backlog in 10 seconds instead of 36. It pays for that with 0.5 game-seconds, about 4% of the minute's game time. That trade is the lesson. **A lag spike you cannot avoid should be paid back fast, by slowing time even further for a few seconds.** Slow time is fair to everyone on the node. Lag is not, because it hits whoever pressed a button during it.

### Move it yourself

Open `examples/w07-tidi-controller.html`. The top chart shows the pilot count and the game speed `f` over three minutes of real time. The bottom chart shows the backlog in seconds, with a dashed line at 1 second, where players start to notice that commands are late. Start with the default battle, aim 0.9 and payback off. A block of backlog appears at the fleet's arrival and drains slowly. Turn payback on with `τ = 5` and watch the block shrink to a sliver while the speed line dips to the 10% floor for a few seconds. Then raise the second wave to 3,100 pilots. Even at the floor, demand is `0.1 × W(3,100) = 1.05`, above `C`, and a red banner reports that the backlog grows without limit while that wave lasts. Dilation has a ceiling, and the floor sets it.

### Same idea elsewhere

Every simulation that must run in real time has to decide what to do with work it could not finish. There are three answers. It can pay the debt back later, forgive it, or refuse to dilate and let it grow.

**EVE Online (CCP, TiDi since 2011, current rules).** EVE pays back. The 2011 post describes the server as aiming to keep a very small queue of waiting work and adjusting the speed in fine steps to hold it there, even running at 98% when a node is only a little overloaded. In our form the small queue is `q` held near zero and the fine steps are the gain. The EVE University wiki gives today's floor, 10% speed, and says dilation applies to the whole node.

**Unity (current scripting reference, `Time.maximumDeltaTime`).** Unity forgives. Its engine loop runs fixed physics steps to catch up with real time, and `maximumDeltaTime` caps how much time can pass between two frames. The documentation says this bounds how many catch-up physics steps run in one frame, and it warns that a long physics step can otherwise cause a chain of long frames. In our form, any debt above the cap is written off, and while the cap bites, the game runs slower than real time. That is involuntary dilation with no controller and no payback.

**Fiedler's fixed timestep (Gaffer on Games, June 2004).** The same pattern in its classic form. A physics loop that steps a fixed `dt` can fall into what Fiedler calls the spiral of death. Being behind makes it simulate more steps to catch up, which puts it further behind. His final loop clamps each frame's time to 0.25 seconds. In our form, a frame's debt beyond 0.25 s is forgiven.

Three systems, one quantity. Each decides what happens to `q`, and the choice shapes what players feel. Paying back keeps game time consistent and costs a short, deep slowdown. Forgiving keeps delays bounded and silently drops simulated time. Refusing to dilate, the pre-2011 EVE answer, lets `q` grow until clients time out.

### Design judgment

- **Keep headroom and a payback term.** A controller that only sees the past always starts a fight in debt. Headroom alone clears the debt slowly. The payback term clears it fast for almost no game time.
- **Mind the floor.** The floor is a promise to players that time will never run slower than this. It also sets the largest fight the node can hold. At aim 90% and a 10% floor, this node holds `0.1 × W(n) = 0.9`, about 2,854 pilots, a little below MMO302's 3,016 because of the headroom. Above that, the backlog grows whatever the controller does, and your levers are the ones in section 4 and week 6.
- **Measure what players feel.** CPU load is the input, but players feel lag and speed changes. Log both, per second, for every large fight.
- **Know when to forgive.** For a single-player game, dropping a quarter second during a hitch is harmless. For a battle where a fleet's destruction hangs on who fired first, it is not. Decide by asking what a lost second destroys.

### Check this example

1. A node at `f = 1` jumps from 500 to 1,500 pilots. What is the backlog after the first second? What speed does an aim-90% controller without payback choose, and how long does the backlog take to clear?
2. With aim 90% and `τ = 5`, what is the controller's target in the second after question 1's jump, and is it clamped?
3. MMO302's controller with `α = 1` built no backlog in the same kind of warp-in. Using the three-step model above, say in one sentence which step it effectively swaps, and why a real server cannot.

<details>
<summary>Answers</summary>

1. `W(1,500) = 0.45 + 2.25 = 2.7`. The first second demands 2.7 and gets 1, so the backlog is 1.7. The target is `0.9 / 2.7 = 0.333`. At that speed demand is 0.9, so 0.1 per second goes to the backlog, and 1.7 takes 17 seconds.
2. `(0.9 − 1.7 / 5) / 2.7 = (0.9 − 0.34) / 2.7 = 0.207`. That is above the 0.1 floor, so it is not clamped.
3. It runs step 3 before step 1: it picks `f` from this second's `W(n)` and then simulates, so demand never exceeds `C`. A real server learns `W(n)` only by running the second, so its first overloaded second always runs at the old speed.

</details>

## 3. Noise, and why you drop fast and recover slow

The fleet in section 2 had a constant cost. Real fights do not. The cost of a second swings with how many modules fire, how many ships warp and how many drones are launched. Model this as noise on the measured cost, `m_t = W(n_t) × (1 + ε_t)`, with `ε_t` uniform between −0.3 and +0.3. A seeded generator keeps the run reproducible. This is the same `mulberry32` generator the interactive uses.

A controller with `α = 1` follows every swing, so `f` jumps around every second. Players feel that as modules that cycle at uneven rates and ships that speed up and slow down. MMO302's answer was a smaller `α`. Slowing the gain in both directions does smooth `f`, but it reacts late to each new wave, and backlog piles up. The fix most control systems use is asymmetry. Respond to overload at once (`α_down = 1`), because overload makes backlog and backlog is the worst outcome. Recover slowly (`α_up = 0.2`), because running a little too slow for a few seconds only costs game time.

The run below is a 180-second battle: 500 pilots for 10 s, 2,000 for 50 s, 2,800 for 60 s, then 800 for 60 s. **Jitter** is the average relative change in `f` from one second to the next.

```python
A, B, C, FLOOR = 0.0003, 0.000001, 1.0, 0.1

def mulberry32(seed):
    s = seed & 0xFFFFFFFF
    def rnd():
        nonlocal s
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((s ^ (s >> 15)) * (s | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd

def run(pilots, aim=0.9, tau=5, a_down=1.0, a_up=1.0, noise=0.3, seed=7):
    rnd = mulberry32(seed)
    f, q, backlogs, jitter, game = 1.0, 0.0, [], 0.0, 0.0
    for n in pilots:
        m = (A * n + B * n * n) * (1 + noise * (2 * rnd() - 1))
        q = max(0.0, q + f * m - C)
        backlogs.append(q)
        game += f
        target = min(1.0, max(FLOOR, (aim * C - (q / tau if tau else 0)) / m))
        new = f + (a_down if target < f else a_up) * (target - f)
        jitter += abs(new - f) / f
        f = new
    return max(backlogs), sum(backlogs) / len(backlogs), jitter / len(pilots), game

battle = [500] * 10 + [2000] * 50 + [2800] * 60 + [800] * 60   # 180 real seconds
for name, kw in [("fast both ways", {}), ("slow both ways", dict(a_down=0.3, a_up=0.3)),
                 ("fast down, slow up", dict(a_up=0.2)), ("no payback term", dict(tau=None))]:
    print("%-19s max %.2f  mean %.2f  jitter %.3f  game-s %.1f" % ((name,) + run(battle, **kw)))
```

```
fast both ways      max 2.93  mean 0.32  jitter 0.159  game-s 83.2
slow both ways      max 7.63  mean 1.32  jitter 0.053  game-s 81.4
fast down, slow up  max 2.93  mean 0.16  jitter 0.062  game-s 75.8
no payback term     max 3.08  mean 0.82  jitter 0.159  game-s 84.1
```

`max` and `mean` are the largest and the average backlog in seconds. Compare the rows.

- **Slow both ways** has the smoothest speed and the worst backlog, 7.6 seconds at peak. It took too long to react to each wave.
- **Fast down, slow up** has the same peak backlog as the fast controller, half its average backlog, and 61% less jitter. The price is 7.4 game-seconds out of 83, about 9% less game time over three minutes. When a lucky quiet second tempts the fast controller to speed up, the next noisy second pushes it back over, and it owes backlog again. The slow-up controller does not take the bait.
- **No payback term** repays the unavoidable spikes through headroom alone, so its average backlog is five times that of the asymmetric controller.

The same asymmetry appears wherever a system must share capacity it cannot measure directly. TCP congestion control ([CS202 week 1](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w01-networks-for-game-devs-tcp-vs-udp.md)) halves its congestion window on loss and grows it back by about one segment per round trip, for the same reason. Overshooting is expensive and undershooting is cheap.

## 4. One fight, many nodes

Everything so far happened on one node. A real fight spreads, and this section asks two questions. How do the speeds of neighbouring servers interact? And what does moving a system to a better node buy?

### Clock domains

Put a fight on the border between two servers of a seamless world, the setting of week 2. Suppose server 1 needs `f = 1` and server 2, holding most of the fleet, needs `f = 0.25`. If each runs its own clock, a ship on server 1's side of the line moves four times as fast as a ship 10 metres away on server 2's side. A missile fired across the border slows down in mid-flight. Worse, events cross the border every tick, and a server running four times faster sends events stamped with game times its neighbour has not reached yet. Week 8 treats that ordering problem in full. For now the rule is simple.

> **Servers that exchange events every tick must share one game clock, so they run at the speed of the slowest.**

Group servers into **clock domains**, sets of servers joined by tick-level interaction. Every server in a domain runs at the lowest speed any of its members needs. Two domains can run at different speeds only if nothing crosses between them faster than a deliberate, slow transition.

Take four servers in a row, needing speeds 1.0, 1.0, 0.4 and 0.25 on their own. Count the game-seconds of simulation delivered per real second, summed over the four, a rough measure of how much game the servers provide.

| Layout | Domains | Speed of each server | Game-seconds per real second |
|---|---|---|---|
| Separate clocks (no coupling) | four | 1.0, 1.0, 0.4, 0.25 | 2.65 |
| Seamless, one domain | one | 0.25, 0.25, 0.25, 0.25 | 1.00 |
| A gate between servers 2 and 3 | two | 1.0, 1.0, 0.25, 0.25 | 2.50 |

The seamless world gives up 62% of its delivered game time for continuity. Two servers with no fight on them are held at a quarter speed because a fight happens next door. The gate recovers almost all of it.

This is why EVE can dilate one node and not the rest. Solar systems connect only through stargates, and a jump is a slow, discrete transition, not a tick-level interaction. The gate is the edge of the clock domain. It is also why seamless worlds work hard to keep large fights inside one server's territory, or to split the domain where the design allows a transition, such as a zone line, a loading tunnel or a portal. Week 9's server meshing moves territory between servers at run time, and it has to reckon with this coupling every time it splits a crowd.

### Moving load before the fight

EVE's clock domain is the node, not the system. MMO302 noted that a quiet system sharing hardware with a battle slows down with it. The fleet fight notification from section 2 is the operator's answer: move the named systems to their own, faster nodes at downtime, before the fight. Here is what that buys, with MMO302's cost model.

A fight fills two neighbouring systems joined by a gate: 1,600 pilots in X and 800 in Y. On an ordinary node they share hardware with some quiet systems whose load totals 0.2 CPU-seconds per game-second. Loads on one node add, because pairs form only inside a system: `W(1,600) = 0.48 + 2.56 = 3.04` and `W(800) = 0.24 + 0.64 = 0.88`. A dedicated node has `C = 2`.

```python
A, B, FLOOR = 0.0003, 0.000001, 0.1     # MMO302 week 12's cost model

def work(n):
    return A * n + B * n * n

def speed(load, capacity):
    """MMO302's f for a node: every system on it shares one speed."""
    return max(FLOOR, min(1.0, capacity / load))

quiet = 0.2                              # CPU-s per game-second of the node's other systems
x, y = work(1600), work(800)             # the two battle systems
plans = {
    "no request: X, Y and the quiet systems share one node": [("X, Y, quiet", x + y + quiet, 1.0)],
    "X moved to a dedicated node, C = 2":  [("X", x, 2.0), ("Y, quiet", y + quiet, 1.0)],
    "X and Y each on a dedicated node":    [("X", x, 2.0), ("Y", y, 2.0), ("quiet", quiet, 1.0)],
}
for plan, nodes in plans.items():
    print(plan)
    for name, load, cap in nodes:
        print(f"   {name:12s} load {load:4.2f}  C {cap:.0f}  speed {speed(load, cap):6.1%}")
```

```
no request: X, Y and the quiet systems share one node
   X, Y, quiet  load 4.12  C 1  speed  24.3%
X moved to a dedicated node, C = 2
   X            load 3.04  C 2  speed  65.8%
   Y, quiet     load 1.08  C 1  speed  92.6%
X and Y each on a dedicated node
   X            load 3.04  C 2  speed  65.8%
   Y            load 0.88  C 2  speed 100.0%
   quiet        load 0.20  C 1  speed 100.0%
```

Three readings. Without a request, everyone, including players in the quiet systems who are not fighting, runs at 24%. Moving X alone lifts the main fight to 66% and nearly frees the rest. Moving both frees everyone except the main fight, which is limited by its own `W(n)`.

Now let the fight move after downtime, which fights do. Suppose X was reinforced but 1,200 pilots follow a target through the gate, leaving 400 in X and 2,000 in Y. Y still shares the ordinary node: `W(2,000) + 0.2 = 4.8`, so Y and the quiet systems run at `1 / 4.8 = 20.8%`, while X's dedicated node idles at full speed. That is the Tribute pattern from the hook. The reinforcement was real, but it sat on the wrong system. Because nodes are mapped once a day, the plan cannot follow the fleet. During the fight, the controller of sections 2 and 3 is all that reacts.

## 5. Clocks at the edges

MMO302 week 12, section 4, gave the rule for which game clocks dilate: if you would check your watch to know when something finishes, it keeps real time. Two edges of that rule appear only once dilation spans many nodes and many clients.

**The client's clock.** The client from CS202 week 10 interpolates between snapshots using its own clock. Under dilation the server must send `f` with each update, and the client must advance its render clock at `f` times real time. If it does not, ships animate at full speed, reach the end of the snapshot buffer, and stop dead until the next update arrives. Players read that as lag. When `f` changes quickly, as it does under the fast-down controller, the client must follow the change too, or its buffer drains or overfills. Send `f` in every snapshot, not only when it changes.

**Crossing between domains.** A pilot who jumps from a system at full speed into one at 20% changes clocks at the gate. Timers the pilot carries in game time, such as a module cooldown or a warp in progress, convert at the moment of crossing: 6 game-seconds of cooldown left stay 6 game-seconds, which now take 30 real seconds. Timers in real time do not convert. A design that stores a timer as a real-time deadline on one side and a game-time duration on the other gives players a gate trick, crossing back and forth to shorten a cooldown. Store every combat timer in game time and convert only at display.

## In-class activity (25 minutes)

Groups of three. Each group gets the node model from section 2 and one scene card: a 1,200-player castle siege on one server, a fight of 2,400 pilots across three gate-linked systems (1,200, 800 and 400 pilots), or a fleet fight on the border between two seamless-world servers.

1. Compute the pilot count at which your busiest node needs dilation, and the count at which it reaches the 10% floor with aim 90%.
2. Choose aim, `τ`, `α_down` and `α_up`. Justify each in one sentence with a number from sections 2 or 3. Use the interactive to check your peak backlog for the default battle.
3. Plan your nodes. You have one dedicated node with `C = 2`, booked at downtime. Say what it hosts and compute the speed of every system with and without it. Then move a third of the largest crowd to a neighbouring system and recompute.
4. Border card only: draw the clock domains and compute delivered game-seconds with and without a transition you add.

Expected output: one page with the two pilot counts, the controller settings and their reasons, the node plan with its speeds before and after the crowd moves, and (border card) the domain drawing. Groups present the plan that broke worst when the crowd moved.

## Common misconceptions

- **"Time dilation removes lag."** It removes lag growth. The first overloaded second always creates a backlog, and a controller without headroom or a payback term keeps it forever, as the aim-100% row shows.
- **"A lower floor lets the node hold any fight."** The floor sets a maximum crowd. At 10% this node reaches its limit near 2,854 pilots with 10% headroom, and past that the backlog grows without bound.
- **"Smoother is always better."** Slowing the controller in both directions smooths the speed and more than doubles the peak backlog. Smooth only the direction that is cheap to get wrong, which is speeding up.
- **"Reinforcing the fight's system protects the fight."** It protects that system for the day. If the crowd moves to a neighbour on an ordinary node, the neighbour and everything sharing its node slow down, and the reinforced node idles.

## Check yourself

1. A node holds 1,000 pilots at `f = 1`. Is it dilated? What speed does an aim-90% controller pick, and how much backlog does the first second at 1,000 create if the node was previously at 500 pilots and `f = 1`?
2. A designer proposes aim 50% so that backlog always clears quickly. What does this cost in game speed for the 2,000-pilot fleet, compared with aim 90%? Suggest a better way to clear backlog quickly.
3. Five servers in a seamless row need speeds 1.0, 0.5, 1.0, 1.0, 0.2 on their own. Compute delivered game-seconds per real second as one domain. Where would a single gate recover the most?
4. A node with `C = 1` hosts a system with 1,800 pilots and quiet systems with a total load of 0.3. What speed do the quiet systems run at? What if the 1,800-pilot system moves to a dedicated node with `C = 2`?

<details>
<summary>Answers</summary>

1. `W(1,000) = 0.3 + 1.0 = 1.3 > 1`, so yes. The target is `0.9 / 1.3 = 0.692`. The first second runs at `f = 1` and demands 1.3, so it leaves a backlog of 0.3 seconds.
2. At aim 50% the target is `0.5 / 4.6 = 0.109`, against 0.196 at aim 90%, so the fight runs 45% slower for its whole length. A payback term (`τ = 5`) clears the backlog in about 10 seconds while keeping aim 90%, costing about 4% of a minute's game time.
3. One domain runs everything at 0.2, delivering `5 × 0.2 = 1.0`. A gate between servers 4 and 5 gives `4 × 0.5 + 0.2 = 2.2`. A gate between 2 and 3 gives `2 × 0.5 + 3 × 0.2 = 1.6`. The best single gate isolates the slowest server.
4. `W(1,800) = 0.54 + 3.24 = 3.78`, plus 0.3 is 4.08, so everything on the node runs at `1 / 4.08 = 24.5%`. After the move, the quiet systems carry 0.3 on `C = 1` and run at 100%. The fight runs at `2 / 3.78 = 52.9%`.

</details>

## Lab / assignment hook

[Lab 07, a dilation controller](../labs/lab07.md). You implement the controller from section 2, reproduce the tables of sections 2 and 3, tune it on a seeded battle with noise to meet a backlog and jitter target, compute clock domains for a small seamless map, and plan node reinforcements for a fight across several systems. Deliverable: your `tidi_control.py`, a table of controller settings with their backlog, jitter and game-time scores, and a one-page dilation and node plan for one of the in-class scene cards.

## Sources

- CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011). Goal of holding a small queue of waiting work; fine-grained speed adjustment, including running at 98%.
- CCP Falcon, "Fleet Fight Notifications & You!" (EVE Online news, 31 March 2016). The notification tool reinforces only the solar system requested; the fight in Tribute where only part of the constellation was reinforced and performance varied by system; one request per system.
- CCP Falcon, "Changes To The Fleet Fight Notification System!" (EVE Online news, 22 January 2018). The tool lets players notify CCP of a large fight so the systems go on a dedicated high-performance node; nodes are mapped at downtime; requests must arrive at least one hour before the downtime preceding the fight.
- EVE University Wiki, "Time dilation" (accessed September 2026, current mechanics). Slowest speed 10%, one game-second per ten real seconds; dilation applies to every system on an overloaded node.
- MMO302 week 12 (this program). The cost model `W(n) = a n + b n²` with `a = 0.3` ms, `b = 1` µs, `C = 1`, floor 0.1; thresholds 861 and 3,016 pilots; the smoothing controller with its aim; the rule for which clocks dilate.
- Unity Technologies, "Time.maximumDeltaTime" (Unity Scripting API, current documentation, accessed September 2026). Caps the time that passes between frames and so the number of fixed physics steps run in one frame; warns that long physics steps can otherwise cause a series of long frames.
- Fiedler, G. "Fix Your Timestep!" (Gaffer on Games, 10 June 2004). The spiral of death; the 0.25 s clamp on frame time in the final loop.
- Allman, M., Paxson, V. and Blanton, E. RFC 5681, *TCP Congestion Control* (IETF, 2009). Window reduced to half the flight size on loss; additive increase of about one segment per round trip in congestion avoidance.

## Interactive spec: examples/w07-tidi-controller.html

**Insight the visual must make obvious:** the first overloaded second always creates a backlog, and the controller's settings decide how long it lives. A payback term clears it in seconds for almost no game time, and a controller that drops fast and recovers slowly keeps both backlog and speed jitter low.

**Layout.** Two stacked charts sharing a real-time x axis (0 to 180 s), a control panel and a number panel. Desktop: charts left (two thirds), controls and numbers right. Under 700 px: charts first, then controls, then numbers.

**Model (must match section 2 and 3 code exactly).**
- `W(n) = 0.0003 n + 0.000001 n²`, `C = 1`, one step per real second.
- Each step: `m = W(n) × (1 + noise × (2r − 1))` with `r` from `mulberry32(seed)` (the lecture's function; one draw per step, drawn even when noise is 0 so sequences stay aligned), `q = max(0, q + f m − C)`, then `target = clamp((aim × C − q/τ) / m, floor, 1)` (drop the `q/τ` term when payback is off), then `f += (target < f ? α_down : α_up) × (target − f)`.
- Record `f` and `q` before the control update, as the code does.
- Metrics: max backlog, mean backlog, jitter (mean of `|f_new − f| / f`), game-seconds (sum of recorded `f`).

**Default battle timeline.** Pilots 500 for 10 s, wave 1 of 2,000 for 50 s, wave 2 of 2,800 for 60 s, then 800 for 60 s. Wave sizes editable. A second timeline, "wave 1 only, 60 s", runs wave 1 from t = 0 for the section 2 test.

**Top chart.** Pilot count as a stepped grey area on a right-hand axis (0 to 3,500). Game speed `f` as a line on the left axis (0 to 1), with a dotted line at the floor. Shade the time the controller sits at the floor.

**Bottom chart.** Backlog `q` in seconds as a filled area, y axis 0 to 10 (extend automatically to the max if it exceeds 10). Dashed line at 1 s labelled "players notice." Show a red "growing without limit" banner when the largest pilot count in the timeline cannot fit even at the slowest allowed speed, that is when `floor × W(n_max) > C` with dilation on, or `W(n_max) > C` with dilation off. Also show it when the backlog at 180 s exceeds the backlog at 120 s by more than 5.

**Controls (all keyboard accessible, each with a live value label).**
- Aim (share of `C`): slider 0.5 to 1.0, step 0.01, default 0.9.
- Payback: toggle, default off on first screen; `τ` slider 1 to 30 s, default 5.
- `α_down` and `α_up`: sliders 0.05 to 1, step 0.05, defaults 1 and 1.
- Noise: slider 0 to 0.5, step 0.05, default 0. Seed: number input, default 7.
- Floor: slider 0.05 to 0.5, default 0.1.
- Wave 1 and wave 2 sizes: number inputs 0 to 5,000.
- Timeline: battle (180 s) or wave 1 only (60 s).
- Preset buttons: "No dilation" (sets f fixed at 1), "Lecture: fast both ways", "Slow both ways", "Fast down, slow up".

**Number panel.** Max backlog, mean backlog, jitter, game-seconds, seconds at the floor, and the largest pilot count the floor can hold at the current aim (solve `floor × W(n) = aim × C`).

**Test values.**
- Wave 1 only (2,000 pilots from t = 0 for 60 s), noise 0, `α` 1/1: aim 1.0: backlog 3.60 at t = 1, 5, 10, game-seconds 13.8. Aim 0.9: backlog 3.50, 3.10, 2.60, clears at t = 36, game-seconds 12.5. Aim 0.9, payback `τ = 5`: `f(1) = 0.100`, backlog 3.06, 1.09, 0.02, clears at t = 10, game-seconds 12.0.
- Default battle, noise 0.3, seed 7, aim 0.9, payback `τ = 5`: fast both ways max 2.93, mean 0.32, jitter 0.159, game-seconds 83.2. `α` 0.3/0.3: 7.63, 1.32, 0.053, 81.4. `α_down = 1`, `α_up = 0.2`: 2.93, 0.16, 0.062, 75.8. Payback off with `α` 1/1: 3.08, 0.82, 0.159, 84.1.
- Floor capacity at aim 0.9, floor 0.1: 2,854 pilots. Wave 2 at 3,100 with noise 0 triggers the banner (`0.1 × W(3,100) = 1.05 > 1`).

**First screen.** Default battle, noise 0, payback off, aim 0.9, so the backlog block after wave 1 is large and slow to drain. Caption: "The first second always overruns. How long the lag lives is your choice." A single highlighted button "Turn on payback" next to the caption.
