# MMO302 · Week 12 — Single-Shard Architectures (EVE) and Time Dilation

**Why this matters:** Most MMOs escape a crowd by copying the world. A single-shard game has promised its players one world, so it cannot. When 3,000 players decide to fight in the same place, the server has to do something, and every option costs the players something. EVE Online's answer, slowing time itself, is the clearest worked case in the field of choosing *which* cost players pay.

**You will be able to:**
- Compute the time-dilation factor, the real length of a dilated fight, and the backlog of unfinished work for a node from a load model.
- Explain why slowing the clock keeps a battle consistent and fair while letting the server fall behind does not.
- Design a dilation controller (target, floor, smoothing) and predict when it builds or repays a backlog.
- Decide which game timers should dilate and which must not, and critique time dilation against caps, copies and bigger hardware.

**Before class:** CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011), the whole post. CCP Logibro, "Battle for 6VDT-H: summary and numbers" (EVE Online news, 30 July 2013). CCP Gun Show, "Tranquility Tech III" (EVE Online news, 14 October 2015), the section on Everest nodes. Alexander (ed.), *Massively Multiplayer Game Development* (2003), selected chapters as assigned on the course page.

**Prerequisites from earlier courses:** From this course, [week 1, the n-squared problem](w01-scale-targets-ccu-messages-and-n-squared.md) (the model `u × Σ g(g − 1)` and why time dilation cuts `u`), [week 2, shards and layers](w02-shards-realms-zones-instances-layers.md) (where a single shard sits among the alternatives), [week 4, zone servers and handoff](w04-zone-servers-and-handoff.md) (EVE's solar systems as zones and nodes as hosts), [week 5, tick rate](w05-tick-rate-for-mmos-vs-shooters.md) (the four policies for a tick that does not fit) and [week 11, load testing](w11-load-testing-with-bots.md) (queues with `ρ > 1`). [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (clamping `dt` makes the game run in slow motion for a frame). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md).

**Interactive:** [Time dilation](../examples/w12-time-dilation.html). Keep it open during section 2.

---

## 1. One universe, many nodes

Week 2 laid out the ways to fit many players into one game. Copy the world into realms or layers, and each copy holds a manageable crowd. Or keep one world and cut it into pieces run by different processes. EVE Online took the second path completely. Its main cluster, Tranquility, runs one universe for every player outside China. There are no realms and no layers. Its record, set in May 2013, was 65,303 players logged in to that one universe at once.

Inside, the universe is partitioned. The map is made of solar systems joined by stargates, and each system is simulated by one server process on a **node**. Week 4 showed why solar systems make good zones. Stargates are discrete jumps, not borders you can drift across, so there are no ghosts and no continuous handoff. The EVE University wiki notes that a typical node hosts hundreds of systems, most of them nearly empty at any moment.

A single shard buys things copies cannot. There is one market, so prices mean something everywhere. There is one map to conquer, so territory is scarce and wars have stakes. There is one history, so a battle is an event the whole playerbase shares. Week 2 called this "the hardest engineering in the field," and here is the reason.

### Players choose where the crowd forms

In a sharded game the operator chooses the crowd size. A realm has a cap, a layer splits when it fills, an instance holds 25. In a single shard the players choose it, and in a war they choose the same place on purpose. The most important system in a war is the one both sides are fighting over. Both sides bring everyone they have.

You can see the scale in EVE's records. In July 2013 the battle for the system 6VDT-H peaked at 4,070 pilots in one system, beating the previous record of 3,615 set in 2010. In January 2014 the battle of B-R5RB lasted 21 hours, with more than 7,500 characters involved and up to 2,670 in the system at once.

Think about what that does to capacity planning. Take a universe with 30,000 pilots online spread over 150 nodes. The average node carries 200 pilots. In our week 1 model the load of a crowd grows with its square, so one node carrying a 3,000-pilot fight carries 15 times the average pilot count and, in its n-squared term, 225 times the average load. You cannot buy 150 nodes each big enough for the worst fight. You can buy a few. CCP's 2015 hardware blog described exactly that. It ran one special high-end "Everest" node reserved for the biggest fleet battles and planned to go to six. Big hardware raises the ceiling. Week 1 showed it buys only a square root in crowd size, so something else has to handle the fight that is bigger still.

That something is the subject of this lecture.

## 2. Worked example: slowing the clock to keep a 3,000-pilot battle consistent

### The hook

During the battle for 6VDT-H, CCP reported that time in the system ran at one tenth of its normal speed for most of the fight. Every module cycle, every missile flight and every warp took ten times as long in real time as its tooltip said. Players watched their ships move in slow motion for hours. The node stayed up, and CCP noted that the battle did not come to an abrupt halt.

Here is the puzzle. The server could not keep up with 4,070 pilots at normal speed, so CCP made the game ten times slower on purpose. Why is that better than letting the server run behind and do its best? A small model answers it.

### The model

Take one node running one crowded system. Measure everything in CPU-seconds.

```
work per game-second    W(n) = a × n + b × n²      CPU-seconds to simulate 1 s of game time
node capacity           C                           CPU-seconds the node can spend per real second
game speed              f = clamp(C / W(n), f_min, 1)
real seconds per game second = 1 / f
backlog growth          max(0, f × W(n) − C)        CPU-seconds added to the queue per real second
command delay           backlog / C + 1 / f         real seconds before a command takes effect
```

- `n` is the number of pilots in the system.
- `a` is the cost of each pilot alone (their modules, their movement, their messages).
- `b` is the cost of each pair of pilots, the n-squared part from week 1 (who sees whom, who can target whom, what each event must be sent to).
- `f` is the **time dilation factor**. At `f = 1` the game runs at normal speed. At `f = 0.1` one game-second takes ten real seconds.
- `f_min` is the **floor**, the slowest the operator allows. EVE's floor is 10%.
- The **backlog** is work the node has been asked to do but has not done yet. While it is zero, every command takes effect at the next tick. When it grows, commands wait behind it.
- EVE's server aims for one tick per game-second (week 5). At speed `f` that tick comes every `1 / f` real seconds, which is the second term of the command delay.

The key idea is in the definition of `f`. Slowing game time by `f` cuts the work per real second by the same factor, because almost everything the server simulates is tied to the game clock. CCP's 2011 blog made exactly this argument. It observed that the large majority of load in big fights is tied to the clock, while physics alone was only 5 to 10% of it. So the controller picks `f` so that `f × W(n) = C`. The node does as much work per real second as it can, and no more.

The model's constants are invented for teaching, chosen so the numbers are easy to check. We use `a = 0.3` ms, `b = 1` µs and `C = 1` CPU-second per real second, one core's worth. They are not CCP's measured costs, which CCP has not published in this form.

### Numbers you can check

```python
A = 0.0003     # CPU-seconds per pilot per game-second (0.3 ms)
B = 0.000001   # CPU-seconds per pilot pair per game-second (1 us)
C = 1.0        # CPU-seconds the node has per real second
FLOOR = 0.1    # slowest allowed game speed

def work(n):
    return A * n + B * n * n          # CPU-seconds to simulate one game-second

print(f"{'pilots':>6} {'work':>6} {'speed':>6} {'real s per game s':>18} {'backlog growth':>15}")
for n in [500, 1000, 1500, 2000, 2670, 3000, 3500]:
    w = work(n)
    f = max(FLOOR, min(1.0, C / w))
    growth = max(0.0, f * w - C)      # CPU-seconds of unfinished work added per real second
    print(f"{n:>6} {w:>6.2f} {f:>6.1%} {1 / f:>18.2f} {growth:>13.2f} s")
```

It prints:

```
pilots   work  speed  real s per game s  backlog growth
   500   0.40 100.0%               1.00          0.00 s
  1000   1.30  76.9%               1.30          0.00 s
  1500   2.70  37.0%               2.70          0.00 s
  2000   4.60  21.7%               4.60          0.00 s
  2670   7.93  12.6%               7.93          0.00 s
  3000   9.90  10.1%               9.90          0.00 s
  3500  13.30  10.0%              10.00          0.33 s
```

Check the 3,000 row by hand. `0.0003 × 3,000 = 0.9` and `0.000001 × 3,000² = 9`, so one game-second costs 9.9 CPU-seconds. The node has 1 per real second, so it runs at `1 / 9.9 = 10.1%` speed. One game-second takes 9.9 real seconds. A fight that would last 10 minutes of game time lasts 99 minutes of real time. The backlog stays at zero, so every pilot's command takes effect at the next tick, 9.9 real seconds away at worst.

Notice a neat property of this range. Between the start of dilation and the floor, real seconds per game second equal `W(n)` exactly, because `C = 1`. The table's "real s per game s" is the work column.

Two thresholds come straight out of the model. Dilation starts where `W(n) = C`, and the floor is reached where `W(n) = C / f_min = 10`.

```python
import math

A, B = 0.0003, 0.000001

def pilots_at(w):
    """Solve A*n + B*n^2 = w for n."""
    return (-A + math.sqrt(A * A + 4 * B * w)) / (2 * B)

print(f"dilation starts at {pilots_at(1.0):.0f} pilots")
print(f"floor reached at   {pilots_at(10.0):.0f} pilots")
```

It prints:

```
dilation starts at 861 pilots
floor reached at   3016 pilots
```

So with these costs, one core carries a normal-speed fight up to 861 pilots, and time dilation stretches that to about 3,016. That is 3.5 times the pilots, not 10 times, for the reason week 1 gave. Dilation divides the work by 10, and the work grows with the square of the crowd. The small linear term gives a little extra, which is why the ratio here is 3.5 rather than √10 ≈ 3.16.

Past the floor, the node is out of options. At 3,500 pilots it can slow the game only to 10%, which still asks for `0.1 × 13.3 = 1.33` CPU-seconds per real second. The backlog grows by 0.33 CPU-seconds every second, commands start waiting, and the fight degrades the way it would have without dilation, only later and more slowly.

### What happens without dilation

Now turn dilation off at 3,000 pilots. The node tries to run at full speed, so it is asked for 9.9 CPU-seconds of work every real second and can do 1. In week 11's terms the utilization is `ρ = 9.9`, and no stable queue exists. The backlog grows by 8.9 CPU-seconds every real second.

| Real time into the fight | Backlog without dilation | Command delay without dilation | Command delay with dilation |
|---|---|---|---|
| 1 s | 8.9 CPU-s | 9.9 s | 9.9 s |
| 10 s | 89 CPU-s | 90 s | 9.9 s |
| 60 s | 534 CPU-s | 535 s | 9.9 s |
| 10 min | 5,340 CPU-s | about 89 min | 9.9 s |

After one second the two look the same. After a minute, a pilot who presses a button without dilation waits almost nine minutes for it to happen. With dilation the wait is one dilated tick, 9.9 seconds, forever.

The model is kind to the no-dilation case, because it assumes the server serves commands in order. Real servers under this load do not. CCP's blog described EVE's server as a cooperative scheduler in which each task runs until it yields. Under heavy load, a task could wait five seconds or more to get another turn. Whose task waits is close to arbitrary. One pilot's guns cycle, another's never fire, a third is shot while their client still shows them warping away. The backlog is not only long. It is unevenly shared. Dilation replaces that with one rule for everyone. The game runs slowly, in order, and nothing is dropped.

That is the answer to the hook. Dilation does not make the server faster. It changes what players lose. Without it they lose **consistency**. Actions happen late, out of order, or not at all, and the outcome depends on whose task got the CPU. With it they lose **speed**. Everything happens, in the right order, but slowly. For a fight with thousands of players and real stakes, EVE decided consistency matters more.

### A visual the student can move

Open `examples/w12-time-dilation.html`. The top panel shows two clocks running side by side, real time and game time, with the speed `f` between them. The bottom panel plots command delay against real time, one line with dilation and one without. Drag the pilot slider from 500 to 3,000. The top panel slows its game clock smoothly. The bottom panel's "with dilation" line stays flat at `1 / f` while the "without" line climbs into minutes. Push past 3,016 pilots and the "with dilation" line starts to climb too. That is the floor, and the edge of what one node can do.

Two more controls matter. The capacity slider stands in for the Everest node. Doubling `C` moves both thresholds right but, because of the square, not twice as far. The smoothing slider shows section 3's controller problem.

### Cross-game recognition

The same idea appears wherever a simulation cannot keep up with its clock. Rewrite each into `f = clamp(C / W, f_min, 1)`.

**EVE Online, 2011 onward.** The mechanic itself, shipped with the Crucible expansion in November 2011. The EVE University wiki describes the slowest speed as 10%, where one game-second takes ten real seconds, and notes that reaching it usually takes thousands of pilots in one system. The client shows an icon with the current speed. The 6VDT-H figures (4,070 pilots, one tenth speed for most of the battle) put that fight at the floor. With our invented constants it would be past the floor, with a growing backlog, but the constants are ours, so treat that as an illustration and not a measurement of CCP's servers.

**Second Life (Linden Lab, current scripting documentation).** Every Second Life region runs on one simulator process, and the scripting function `llGetRegionTimeDilation` returns a number from 0 to 1. The documentation defines it as the ratio between the change in script time and the change in real time, and says physics and script load can cause it. That is our `f`, reported by the engine to the scripts, with no floor above zero. At zero, script execution halts.

**Minecraft (Java Edition, current wiki).** Minecraft's game loop aims for 20 ticks per second. The Minecraft Wiki says that when the computer cannot keep up, the ticks per second drop, and the game runs slower. That is dilation without a controller. The engine simply takes as long as it takes, the "stretch" policy of week 5. The same wiki lists a safety valve in the loop. If the server falls 2 seconds behind its expected tick time, it resets its schedule instead of trying to catch up. In our model that is throwing the backlog away so it cannot grow forever, the "skip" policy.

**Your own game loop (CS101 week 9).** When a frame takes too long, you clamp `dt` to, say, 0.1 s, and the game runs in slow motion for that frame instead of teleporting objects through walls. That is `f = 0.1 / frame_time`, a one-frame time dilation on a single machine.

Four systems, one rule. When the work per unit of game time exceeds the capacity per unit of real time, something gives. You choose whether it is game speed (EVE, Second Life, your clamp), history (Minecraft's reset drops simulated time), or fairness (a server that runs behind and serves whoever gets the CPU).

### Eyes-open design judgment

- **Dilation fits slow, tactical combat.** EVE ticks once per second (week 5), and its fights are about positioning, target calling and module timing over minutes. Slowing that by 10 is painful but playable. A shooter or an action MMO at 10% speed would be a slideshow, and would be better served by week 5's "shed load" policy or by caps.
- **Dilation buys a square root, not a multiple.** Week 1 and this example agree. A 10% floor carries about 3.2 to 3.5 times the crowd. It is a last line, behind interest management, fast code and big nodes.
- **Dilation is node-wide.** The EVE University wiki notes that the icon appears in all systems on an overloaded node. A quiet system that shares hardware with a battle slows too. Keeping big fights on dedicated hardware, like the Everest nodes, protects the neighbors as much as the fight.
- **The floor is a promise, and past it the model fails.** Above 3,016 pilots in our model, the backlog comes back. The operator must decide in advance what happens then. Options are a population cap on the system, a gate queue, or accepting degraded service.
- **Not every timer should dilate.** Section 4 is about this, and it matters as much as the formula.

### Check this example

1. With the lecture's constants, what speed does a 2,500-pilot fight run at? How long in real time does a 5-minute game-time engagement take?
2. CCP moves the fight to a node twice as fast (`C = 2`). At what pilot count does the floor now bite? Compare it with 3,016.
3. Without dilation, a 2,000-pilot fight starts at real time 0. How long before a new command waits more than one minute?

<details>
<summary>Answers</summary>

1. `W = 0.75 + 6.25 = 7.0`, so `f = 1 / 7 ≈ 14.3%`. Five game-minutes take `5 × 7 = 35` real minutes.
2. The floor bites where `W(n) = C / f_min = 20`. Solve `0.000001 n² + 0.0003 n = 20`: `n = (−0.0003 + √(0.00000009 + 0.00008)) / 0.000002 ≈ 4,325`. Doubling the node gives about 43% more pilots, not twice as many.
3. `W(2,000) = 4.6`, so the backlog grows at 3.6 CPU-seconds per second and the delay is `3.6 t + 1` seconds. It passes 60 s when `t > 59 / 3.6 ≈ 16.4` real seconds.

</details>

## 3. Building the controller

The model sets `f = C / W(n)` as if the server knew `W(n)` in advance. It does not. It measures how long the last ticks took and adjusts. CCP's 2011 blog walked through an illustrative 1,600-pilot fight in which the factor dropped to about 5% as the fleets warped in, rose to about 30% as the fight settled, climbed toward 60% as ships died, dipped again to 10% during the retreat, and returned to 100%. The factor follows the load, and the load changes fast.

A real controller has to choose two things.

**How fast to follow.** A common approach is to move `f` part of the way to its target each second: `f ← f + α × (target − f)`. With `α = 1` the factor jumps instantly, which is ideal on paper but makes the game's speed lurch whenever a measurement is noisy. With small `α` the speed changes smoothly, but it lags behind a sudden warp-in, and while it lags the node is overloaded and builds a backlog.

**What to aim at.** If the target is exactly `C / W(n)`, the node runs at 100% of its capacity once it settles. Any backlog built during the lag then stays forever, because there is no spare capacity to pay it off. Week 11 already warned that a queue at 100% utilization has no stable length. Aim a little lower, say 90% of `C`, and the node repays its debt.

```python
A, B, C, FLOOR = 0.0003, 0.000001, 1.0, 0.1

def work(n):
    return A * n + B * n * n

def run(alpha, aim, seconds=600):
    """2,000 pilots warp onto 500 at t = 10 s. Each second the speed f moves a share
    alpha of the way to its target, aim * C / work(n). Returns (worst, final) backlog."""
    f, backlog, worst = 1.0, 0.0, 0.0
    for t in range(seconds):
        n = 500 if t < 10 else 2500
        target = max(FLOOR, min(1.0, aim * C / work(n)))
        f = f + alpha * (target - f)
        backlog = max(0.0, backlog + f * work(n) - C)
        worst = max(worst, backlog)
    return worst, backlog

for alpha in [1.0, 0.5, 0.2]:
    for aim in [1.0, 0.9]:
        worst, end = run(alpha, aim)
        print(f"alpha {alpha:3.1f}, aim {aim:.0%}: worst backlog {worst:5.1f} CPU-s, "
              f"after 10 min {end:5.1f} CPU-s")
```

It prints:

```
alpha 1.0, aim 100%: worst backlog   0.0 CPU-s, after 10 min   0.0 CPU-s
alpha 1.0, aim 90%: worst backlog   0.0 CPU-s, after 10 min   0.0 CPU-s
alpha 0.5, aim 100%: worst backlog   6.0 CPU-s, after 10 min   6.0 CPU-s
alpha 0.5, aim 90%: worst backlog   5.4 CPU-s, after 10 min   0.0 CPU-s
alpha 0.2, aim 100%: worst backlog  24.0 CPU-s, after 10 min  24.0 CPU-s
alpha 0.2, aim 90%: worst backlog  22.2 CPU-s, after 10 min   0.0 CPU-s
```

Read it in pairs. A smooth controller (`α = 0.2`) builds 24 CPU-seconds of debt during the warp-in, which at 2,500 pilots means commands wait about 24 extra seconds. Aimed at 100%, that debt is still there ten minutes later. Aimed at 90%, it is gone. The price of the 90% aim is that the fight runs 10% slower than it strictly had to. That is the same trade week 11 made when it planned for 60 to 70% utilization instead of 100%.

## 4. Which clocks dilate?

A game has many clocks. Dilation slows the one inside the simulation. Everything that touches the outside world keeps real time. Deciding which is which is design work, and players will find every mistake.

CCP's 2011 blog gave a rule of thumb. If you would look at your watch to know when something finishes, it probably should not dilate. Its examples were a structure's reinforcement timer, which does not dilate, and shield recharge, which must, because it is part of the flow of combat. The EVE University wiki lists what stays on real time today: the server clock, skill training, industry jobs and the repair timers of player structures.

Walk through why each choice holds.

- **Combat timers dilate.** Module cycles, missile flight, warp, shield and capacitor recharge. If shields recharged in real time during a 10% fight, a ship would regain ten times as much shield per game-second of combat as normal, and fights on a dilated node would play by different rules.
- **Scheduled events do not.** A structure's reinforcement timer tells both sides when to come back for the next fight, often days later. Players plan real lives around it. If it dilated, a fight on the same node could push the next battle hours later for everyone, and a side could slow a timer on purpose by bringing more ships.
- **Progress timers do not.** Skill training and industry are measured against the real calendar. A player who happens to be docked in a dilated system should not lose training time.

The dangerous cases are the ones in between, where a real-time timer meets a dilated fight. In our model, a 3,000-pilot fight runs at 10.1%. A real-time timer with 15 minutes left gives the defenders only about 91 game-seconds of fighting before it expires. Whoever benefits from that timer expiring now wants the fight to be as large and as slow as possible. Any real-time timer that can resolve during a dilated fight is a lever players will pull. You should list them before launch, not after.

## 5. The alternatives, and when they win

Time dilation is one answer to "the crowd does not fit." Week 5 listed four policies for an overlong tick, and week 2 listed the ways to divide a world. Here is how they compare for a 3,000-player fight in one place.

| Approach | What players lose | Works when | Fails when |
|---|---|---|---|
| Time dilation | Speed. Everything happens, slowly. | Combat is slow and tactical; the world must stay one piece | Twitch combat; the crowd is past the floor |
| Hard population cap on the zone | Access. Late arrivals cannot join. | Crowds are rare and the cap is well above normal play | The fight is over the right to be there, which is what wars are |
| Copies (layers, shards) | Shared history. Two sides may never meet. | The crowd is incidental (a launch, a town) | The crowd is the point (a battle, a siege) |
| Shed load (smaller AOI, lower update rate) | Detail. Distant players update rarely or vanish. | The simulation is dominated by what each player sees | The rules themselves need every pair (who can target whom) |
| Bigger hardware | Money | Always helps, up to a point | Buys a square root in crowd size per doubling of power |
| Split one place over many processes | Engineering time and consistency guarantees | You can afford a research-grade effort | The cost of coordination between processes eats the gain |

EVE combines several of these. It has fast code and big nodes, keeps fights on dedicated hardware, and uses dilation as the last line. The design lesson is to decide in advance which loss your game can afford. A fantasy MMO's capital-city crowd is incidental. Layer it and nobody minds. A war game's decisive battle is the product. Copying it would break the promise the single shard made.

## In-class activity (25 minutes)

Groups of three. You run a single-shard space MMO with the lecture's cost model. Your biggest node has `C = 4`, and the floor is 10%.

1. Compute the pilot counts where dilation starts and where the floor bites on that node.
2. Your design team wants a new capital ship whose weapons affect every pilot in range, which raises `b` to 1.5 µs in fights where it appears. Recompute the floor threshold.
3. List three timers in your game (invent them) and decide for each whether it dilates. Justify each in one sentence, using the "look at your watch" rule.
4. Write one sentence to your producer on what you will do when a fight exceeds the floor.

Expected output: three pilot counts, a three-row table, one sentence.

## Common misconceptions

- **"Time dilation makes the server faster."** It makes the server do less per real second. Total work for the fight is the same, spread over more real time.
- **"At 10% speed the node carries 10 times the players."** Work grows with the square of the crowd, so it carries about √10 ≈ 3.2 times as many (a little more if the per-pilot term is large).
- **"Lag and time dilation are the same thing."** Lag is uncontrolled. Commands wait unpredictably and some are lost. Dilation is controlled. Commands wait one dilated tick, in order, for everyone.
- **"Everything in the game should slow down together."** Timers tied to the real calendar must keep real time, or players lose training, production or the schedule of their next fight.

## Check yourself

1. With the lecture's constants, a node at `C = 1` holds 2,000 pilots. 400 more warp in. What is the new speed, and how much longer in real time does each game-second take?
2. A controller aims at 100% and has built 30 CPU-seconds of backlog during a warp-in. The fight then holds steady for an hour. How big is the backlog at the end of the hour? What if the controller aims at 80% instead (and the floor does not bind)?
3. A structure timer with 20 real minutes left expires during a fight running at 12.5% speed. How many game-seconds of combat happen before it expires? Name one behavior this could encourage.
4. Second Life reports a time dilation of 0.6 in a region. Using the model with `C = 1`, what is the ratio of work demanded at full speed to capacity?

<details>
<summary>Answers</summary>

1. `W(2,400) = 0.72 + 5.76 = 6.48`, so `f = 1 / 6.48 ≈ 15.4%`. At 2,000 each game-second took 4.6 real seconds. Now it takes 6.48, about 1.9 seconds longer.
2. Aimed at 100%, the node does exactly `C` of work per second, so nothing repays the debt. It is still 30 CPU-seconds, and commands still wait about 30 extra seconds. Aimed at 80%, the node spends `0.8 C` on new work and has `0.2` CPU-seconds per second to repay, so the debt is gone after 150 seconds.
3. `20 × 60 × 0.125 = 150` game-seconds. The side that wants the timer to expire has a reason to bring more ships, or to start fights on the same node, to slow the game further.
4. `f = C / W`, so `W / C = 1 / 0.6 ≈ 1.67`. The region is asked for about 67% more work than it can do at full speed.

</details>

## Lab / assignment hook

[Lab 12, a time-dilation governor](../labs/lab12.md). You implement the model, replay a 66-minute battle timeline through a node with and without dilation, measure game time, backlog and worst command delay, then design your own controller and floor policy and defend it with the numbers.

## Sources

- CCP Veritas, "Introducing Time Dilation (TiDi)" (EVE Online dev blog, 22 April 2011). The cooperative round-robin scheduler and tasks waiting five seconds or more under load; most load in large engagements tied to the game clock; physics about 5 to 10% of the load; the illustrative 1,600-pilot fight with factors of about 5%, 30%, 60% and 10%; the "look at your watch" rule; reinforcement timers not dilated, shield recharge dilated; no floor fixed at the time of writing.
- CCP Logibro, "Battle for 6VDT-H: summary and numbers" (EVE Online news, 30 July 2013). Peak of 4,070 pilots in one system; previous record 3,615 in P-2TTL (2010); time at one tenth of normal speed for most of the battle; the node stayed up.
- CCP Gun Show, "Tranquility Tech III" (EVE Online news, 14 October 2015). One Everest node for the biggest fleet battles before the upgrade, six planned after.
- EVE University Wiki, "Time dilation" (accessed September 2026, current mechanics). Slowest speed 10%, one game-second as ten real seconds; applies to all systems on an overloaded node; the client icon; server time, skill training, industry and Upwell structure repair timers not affected; server load `O(n²)` in players on grid.
- EVE University Wiki, "Server tick" and "Tranquility" (accessed September 2026). One tick per second; a typical node hosts hundreds of systems; Tranquility as one universe split over nodes.
- Wikipedia, "Eve Online" (accessed September 2026). Tranquility as a single universe for players outside China; 65,303 concurrent players on 5 May 2013; server and client written in Stackless Python.
- Wikipedia, "Expansions of Eve Online" (accessed September 2026). Crucible, released 29 November 2011, included time dilation.
- Wikipedia, "Battle of B-R5RB" (accessed September 2026). January 2014; 21 hours; over 7,548 characters involved; peak of 2,670 in the system; time dilation at ten percent.
- Second Life Wiki, "Region" (accessed September 2026). Each region is hosted by a single simulator process.
- Second Life Wiki, "llGetRegionTimeDilation" (accessed September 2026). Returns 0.0 to 1.0, the ratio of script time to real time; caused by physics and script load; script execution halts at zero.
- Minecraft Wiki, "Tick" (accessed September 2026, Java Edition). 20 ticks per second; ticks per second fall when the computer cannot keep up; the loop resets its next tick time when it lags 2 seconds behind.
- Alexander, T. (ed.) (2003). *Massively Multiplayer Game Development*. Charles River Media.

## Interactive spec: examples/w12-time-dilation.html

**Insight the visual must make obvious:** with dilation, command delay stays flat at one dilated tick for everyone; without it, delay grows every second the fight lasts. Dilation trades speed for consistency, and it works only up to the floor.

**Layout.** Top: two clocks side by side ("Real time", "Game time") as horizontal progress bars that fill over a 60-second animation loop, with `f` shown between them. Bottom: a chart of command delay (y, seconds, log scale 1 to 10,000) against real time into the fight (x, 0 to 600 s). Number panel beside the chart on desktop, beneath it under 700 px.

**Chart lines.**
- "With dilation": `delay(t) = backlog_d(t) / C + 1 / f`, where `backlog_d(t) = max(0, f × W − C) × t`.
- "Without dilation": `delay(t) = (W − C) × t / C + 1`, floored at 1.
- A horizontal reference line at 60 s labelled "one minute".

**Controls.**
- Pilots `n`: slider 100 to 5,000, step 10, default 3,000.
- Node capacity `C`: slider 0.5 to 8, step 0.5, default 1 (label "1 core", "Everest ×2" etc. as plain numbers).
- Floor `f_min`: slider 0.02 to 1, step 0.01, default 0.10.
- Per-pilot cost `a` (ms): 0.1 to 2, default 0.3. Per-pair cost `b` (µs): 0.2 to 5, default 1.
- Toggle "show controller": replaces the steady-state lines with a 600-second run of section 3's controller, 500 pilots rising to `n` at t = 10 s, with sliders `α` 0.05 to 1 (default 0.2) and aim 70% to 100% (default 100%). Plot backlog (CPU-s) instead of delay in this mode.
- Preset buttons: "6VDT-H scale (4,070)", "B-R5RB peak (2,670)", "Everest node (C = 2)".

**Number panel.** `W(n)`, `f`, real seconds per game second, a 10-minute game-time fight in real minutes, backlog growth per second, dilation start `n₁ = pilots_at(C)` and floor `n₂ = pilots_at(C / f_min)` where `pilots_at(w) = (−a + √(a² + 4 b w)) / (2 b)`.

**Formulas.** `W = a n + b n²` (a, b in seconds). `f = clamp(C / W, f_min, 1)`. Growth `= max(0, f W − C)`. Controller: `f ← f + α (clamp(aim × C / W, f_min, 1) − f)`, then `backlog ← max(0, backlog + f W − C)`, one step per real second.

**Test values** (defaults `a = 0.3` ms, `b = 1` µs, `C = 1`, floor 0.1): `n = 1,000` gives `W = 1.30`, `f = 76.9%`. `n = 3,000` gives `W = 9.90`, `f = 10.1%`, 99 real minutes for 10 game-minutes, growth 0. `n = 3,500` gives `f = 10.0%`, growth 0.33. Thresholds 861 and 3,016. With `C = 2`, floor threshold 4,325. Without dilation at 3,000 pilots, delay at `t = 60` is 535 s. Controller mode with `n = 2,500`, `α = 0.2`: worst backlog 24.0 at aim 100% and 22.2 at aim 90%; at 600 s, 24.0 and 0.0.

**First screen:** `n = 3,000`, both lines drawn, caption "3,000 pilots at 10% speed: every command waits 9.9 s. Without time dilation, after one minute it waits 9 minutes."

**Accessibility.** Clock animation pauses under `prefers-reduced-motion` and shows static bars with the ratio in text; all controls keyboard reachable; number panel is `aria-live="polite"`.
