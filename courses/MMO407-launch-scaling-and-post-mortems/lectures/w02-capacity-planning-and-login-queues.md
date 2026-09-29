# MMO407 · Week 02 — Capacity planning and login queues

**Why this matters:** Every launch team has to answer one question weeks in advance: how many worlds do we open? Open too few and players spend launch night in a queue. Open too many and, a month later, half your worlds feel empty and you are planning merges. This week you learn to predict the queue at any hour of a launch from two curves, why it peaks hours after the rush, and how to pick a world count that survives both launch night and day 30.

**You will be able to:**
- Compute the queue length and the wait at the back of the queue at any hour of a fresh launch, from cumulative arrival and admission curves.
- Explain, with the model, why a launch queue peaks when arrivals fall below the admission rate, not at the unlock spike.
- Choose a world count (or a layering plan) that meets a launch-night wait target and a day-30 population target, and defend it with numbers.
- State how the assumption about session lengths changes the answer, and give the range.

**Before class:** Reread MMO302 week 9, section 2 (the `C / L` model and Little's law); you need it and it is not re-taught here. Read Newell, G. F., *Applications of Queueing Theory* (2nd ed., 1982), chapter 2 on cumulative-count diagrams for queues, the first 10 pages. Skim MMO302 week 2 section 2 on layers.

**Prerequisites from earlier courses:** [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) (a full world admits `μ = C / L`; wait for position `p` is `p × L / C`). [MMO302 week 2, shards, realms and layers](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) (layers as temporary capacity). [MMO302 week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (headroom, provisioning lag). [MMO404 week 13, cost engineering](../../MMO404-advanced-networked-simulation/lectures/w13-cost-engineering.md) (what an under-filled server costs per player-hour). [Week 1 of this course](w01-launch-day-anatomy.md) (the bottleneck stage, and why the queue should sit at world entry).

**Interactive:** [examples/w02-launch-queue-hour-three.html](../examples/w02-launch-queue-hour-three.html). Keep it open during section 2.

---

## 1. What changes at a launch

MMO302 week 9 modelled an evening on a world that was already full. Players left at `C / L` per minute, each departure admitted one queued player, and the queue grew at `λ − C / L`. That model is right for a normal busy evening. A launch breaks three of its assumptions.

- **The worlds start empty.** At the unlock, nobody is online. For the first part of the night, admissions are set by how fast a world can load characters, not by logouts.
- **Arrivals change by the hour.** A launch has a spike at the unlock, a long shoulder through the first evening, and a quieter night. A single constant `λ` hides the shape that decides when the queue is worst.
- **The capacity decision is hard to undo.** Worlds you open for launch night are still there on day 30, holding communities, guilds and player-owned property. You cannot scale a world in or out the way MMO302 week 13 scales a fleet of stateless servers.

Week 1 argued that world entry should be the planned bottleneck, with one visible queue in front of it. This week you size that queue.

## 2. Worked example: how long is the queue at hour 3?

### The hook

New World launched on 28 September 2021 with over 700,000 players online on Steam that day. Each world server admitted 2,000 players at a time. On the most popular worlds, the queue reached its own limit of 25,000 players. Amazon added servers in every region within two days and offered free character transfers.

Put those two numbers into MMO302's formula. The back of a 25,000-player queue behind a 2,000-player world waits `25,000 × L / 2,000 = 12.5 × L`. If players stay for three hours, that is 37.5 hours. No one waits that long, so most of that queue was people who would give up, come back and try again. The part players find strangest is that the worst queues were not at the unlock. They came later, when the launch rush had calmed down. This section shows why.

### The model

Count players, not rates. Draw two running totals against time.

- `A(t)`, **cumulative arrivals**: everyone who has tried to get in by time `t`.
- `D(t)`, **cumulative admissions**: everyone the world has let in by time `t`.

The queue at time `t` is the vertical gap between them, and the wait for the player at the back is the horizontal gap:

```
Q(t) = A(t) − D(t)
wait at the back ≈ Q(t) / μ(t)
```

The slopes of the two curves are the rates you already know. The slope of `A` is the arrival rate `λ(t)` per world. The slope of `D` is the admission rate `μ(t)`, which at a fresh launch has two phases:

```
while filling:  μ = min(λ, a)          a = how fast one world loads characters
once full:      μ = C / L              (MMO302 week 9)
```

Here `C` is the world's cap, `L` the average launch-night session in minutes, and `a` the world's entry rate, the most characters per minute it can load and place. The queue grows whenever the `A` curve is steeper than the `D` curve, and shrinks when it is shallower. So:

**The queue peaks at the moment `λ(t)` falls below `μ(t)`, not when `λ` is largest.** Until that moment, the gap keeps widening, however calm the arrival rate looks.

This way of drawing a queue, as two cumulative curves, comes from traffic engineering. Newell's textbook uses it for cars at a signal and at a lane closure. It has one advantage over rate charts. You can read queue length and wait straight off the picture, for any arrival shape, with no formula for the shape.

### Numbers you can check

Take one launch with these invented teaching values. The game opens 10 worlds, each with `C = 4,000`, entry rate `a = 100` per minute, and a launch-night session of `L = 160` minutes, so a full world admits `μ = 4,000 / 160 = 25` per minute. Across the whole game, 1,200 players per minute try to log in during the first hour, 400 per minute in hours 2 and 3, and 150 per minute after that. Spread over 10 worlds, each world sees `λ = 120`, then 40, then 15.

Walk the curves forward.

- **Minutes 0 to 40.** The world is filling. `λ = 120` but `μ = a = 100`, so the queue grows by 20 per minute. The world holds 4,000 after 40 minutes.
- **Minutes 40 to 60.** The world is full, `μ = 25`. The queue grows by `120 − 25 = 95` per minute.
- **Minutes 60 to 180.** Arrivals fall to 40, which feels like the rush is over. But `40 > 25`, so the queue still grows by 15 per minute.
- **From minute 180.** Arrivals fall to 15, below 25. The queue finally shrinks, by 10 per minute.

| Minute | `A(t)` arrivals so far | `D(t)` admitted so far | Queue `Q = A − D` | `λ` | `μ` |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 120 | 100 |
| 40 | 4,800 | 4,000 | 800 | 120 | 25 |
| 60 | 7,200 | 4,500 | 2,700 | 40 | 25 |
| 120 | 9,600 | 6,000 | 3,600 | 40 | 25 |
| 180 | 12,000 | 7,500 | **4,500** | 15 | 25 |
| 240 | 12,900 | 9,000 | 3,900 | 15 | 25 |
| 630 | 18,750 | 18,750 | 0 | 15 | 25 |

Check hour 3 by hand. `A(180) = 120 × 60 + 40 × 120 = 12,000`. `D(180) = 4,000 + 25 × 140 = 7,500`. The queue at hour 3 is 4,500 players per world, and the player at the back waits about `4,500 / 25 = 180` minutes. The queue empties when `D` catches `A`. The gap shrinks by 10 a minute, `4,500 / 10 = 450` minutes after hour 3, at minute 630, more than ten hours after the unlock.

This minute-by-minute simulation follows the same rules for 10, 15 and 20 worlds.

```python
C, L, A = 4000, 160, 100          # world cap, launch-night session (min), world entry rate/min

def demand(t):
    """Players per minute trying to log in, across the whole game."""
    return 1200 if t < 60 else 400 if t < 180 else 150

def launch(worlds, cap=C, entry=A, minutes=720):
    """One world at a fresh launch: it fills at the entry rate, then admits cap/L."""
    online = queue = 0.0
    log = []
    for t in range(minutes):
        queue += demand(t) / worlds
        if online >= cap - 1e-9:
            online -= cap / L                       # logouts start once the world is full
        admit = min(queue, entry, cap - online)
        queue -= admit
        online += admit
        log.append(queue)
    return log

for w in (10, 15, 20):
    log = launch(w)
    peak = max(range(len(log)), key=lambda t: log[t])
    empty = next(t + 1 for t in range(peak, len(log)) if log[t] < 0.5)
    print(f"{w} worlds: at 1 h {log[59]:5.0f}, at 3 h {log[179]:5.0f}, "
          f"peak {log[peak]:5.0f} at minute {peak + 1}, empty at minute {empty}")
```

It prints:

```
10 worlds: at 1 h  2700, at 3 h  4500, peak  4500 at minute 180, empty at minute 630
15 worlds: at 1 h   550, at 3 h   750, peak   750 at minute 180, empty at minute 230
20 worlds: at 1 h     0, at 3 h     0, peak    15 at minute 82, empty at minute 85
```

Each line's `log[t]` is the queue after minute `t` ends, so `log[179]` is the queue at hour 3. With 15 worlds, each world sees 80, then 26.7, then 10 per minute. It fills in 50 minutes with no queue, builds 550 in the last ten minutes of the rush, and then gains only 1.7 per minute until hour 3. With 20 worlds, arrivals of 20 per minute in the shoulder are below `μ = 25`, and only a brief queue of 15 appears in the minute the world fills.

### Move it yourself

Open the interactive. The left view is the rate view that most dashboards show: arrivals per minute as a step line, and admissions per minute below it. At hour 1 the arrival line drops from 120 to 40, and the chart looks like the crisis is over. The right view draws `A(t)` and `D(t)`. The gap between them keeps widening for two more hours, and the vertical bar at the cursor reads "queue 4,500, wait 180 min" at hour 3. Drag the world count from 10 to 15 and watch the two curves meet almost everywhere. Then drag the entry rate `a` from 100 to 400. The world fills a few minutes sooner and the hour-3 queue barely moves, from 4,500 to about 4,350, because the world was going to be full anyway. The only settings that move hour 3 a lot are the ones that change the slopes after the world is full, which are `C`, `L` and the arrivals themselves.

### Cross-game recognition

Every launch-queue story rewrites into `A(t)`, `D(t)` and the moment `λ` falls below `μ`.

**New World (launch, September 2021).** With `C = 2,000`, a world's `D` curve was shallow, `2,000 / L` per minute. Amazon's two fixes map onto the two curves. New servers split `A(t)` across more worlds, which lowers each world's arrival slope. Testing a higher cap would raise `C` and steepen `D`. The 25,000 queue limit is a third element, a ceiling on `A − D`. When the gap hit it, new arrivals were turned away, which hides demand instead of serving it.

**World of Warcraft Classic (launch, August 2019).** Blizzard launched with larger realms than the original game and used layering, which raises `C` for a realm by running extra copies of the world. Some realms still had extreme queues, and Blizzard opened extra realms in every region, which splits `A(t)`. The Warcraft Wiki records, citing Jason Schreier's *Play Nice* (2024), that the Classic team had expected most players to log in, log off and never return, and the opposite happened. In the model, the team expected `λ` to fall below `μ` within days. It did not, so the gap kept widening and extra realms were the only fast lever.

**Lost Ark (western release, February 2022).** The game passed 1.3 million concurrent players on Steam and had long queues, and a new European server region was added. Founder's pack buyers had played since 8 February, three days before the 11 February release. A head start takes the steepest part of `A(t)` and moves some of it days earlier, which is the cheapest way to flatten the curve without refusing anyone.

**FFXIV: A Realm Reborn (August 2013).** MMO302 week 9 covered Square Enix's decision to suspend digital sales. In this week's picture, that decision lowered the slope of `A(t)` for every world at once, the only lever that did not require new hardware.

**Outside games: a traffic signal.** Newell's cumulative-count diagram was built for roads. Cars arrive along `A(t)`, the green light releases them along `D(t)`, and the queue at the signal is the vertical gap. A traffic engineer reads the worst queue off the point where arrivals drop below the green-light discharge rate, exactly as you read hour 3 here.

### Eyes-open design judgment

- **Plan against the shoulder, not the spike.** The unlock spike fills the world in minutes whatever you do. The hours of `λ` just above `μ` that follow are what build the long queue. A forecast that gives only a peak rate is missing the number you need.
- **Entry speed is not queue speed.** A faster login and entry path shortens the first minutes and changes almost nothing at hour 3 once worlds are full. Spend that budget only after `C` and the world count are right.
- **Queue limits hide demand.** A cap on queue length turns away players you cannot count. Log every refused attempt so your post-launch analysis sees the real `A(t)`.
- **The model is only as good as `L`.** Launch-night sessions run long, and `μ` is inversely proportional to `L`. If your playtests measured 90 minutes but launch night runs 160, the model's hour-3 queue will be low by more than half. Section 3 shows the second way `L` misleads.

### Check this example

1. Using the section 2 numbers with 12 worlds, find each world's arrival rates, the minute the world fills, and the queue at hour 3.
2. With 10 worlds, the team raises the cap to 5,000 for launch night (same `a` and `L`). What is the new `μ`, and the queue at hour 3?
3. The rush lasts 90 minutes instead of 60, then drops to 40 per world as before. What is the queue at hour 3 with 10 worlds?

<details>
<summary>Answers</summary>

1. `λ = 100`, then 33.3, then 12.5. The world fills at the entry rate of 100 with no queue, full at minute 40. Minutes 40 to 60 add `(100 − 25) × 20 = 1,500`. Minutes 60 to 180 add `(33.3 − 25) × 120 = 1,000`. Queue at hour 3 about 2,500, back-of-queue wait 100 minutes.
2. `μ = 5,000 / 160 = 31.25`. Fill takes 50 minutes (queue grows 20 per minute, 1,000). Minutes 50 to 60 add `(120 − 31.25) × 10 = 887.5`. Minutes 60 to 180 add `(40 − 31.25) × 120 = 1,050`. Queue at hour 3 about 2,938, wait about 94 minutes.
3. `A(180) = 120 × 90 + 40 × 90 = 14,400`. `D(180) = 7,500` as before. Queue 6,900, wait 276 minutes.

</details>

## 3. Why the first hours are worse than the formula

The model above lets logouts start at the full-world rate `C / L` the moment a world fills. That is the MMO302 assumption that sessions end at random, so a fixed share of online players leaves every minute. On a normal evening it is a good approximation, because the players online started their sessions at many different times.

At a launch, every player online started within the same hour. Their sessions are all young. If sessions tend to last a similar length, few of them end until that length has passed, and the logout rate starts well below `C / L`. Compare three assumptions for the 10-world launch at hour 3, all with the same average session `L = 160`:

| How sessions end | Queue at hour 3 | Why |
|---|---|---|
| At random from the first minute, including while the world fills | about 4,060 | early leavers free slots during the fill, so `D` gets a head start |
| At random, starting once the world is full (section 2) | 4,500 | the teaching model |
| Every session lasts exactly 160 minutes | 6,000 | nobody leaves until minute 160; the queue peaks at 7,200 at minute 160 |

Real launch sessions sit between the last two rows. The practical lesson is that the steady-state formula is a floor for a launch, not a forecast. The honest way to present a launch-night queue estimate is as a range, and the width of the range comes from how session lengths are distributed, not from the average. You can measure that distribution in a stress test or a head start (week 3), and you should.

## 4. Capacity planning: launch night against day 30

Now the decision. More worlds shorten the launch queue, and every world you open must still feel alive a month later. Put numbers on both ends.

Suppose the forecast for day 30 is 30,000 players online at the evening peak across the whole game, and the design team says a world feels alive with at least 2,500 players at peak. Both are invented teaching values, but every studio has versions of both. The second one comes from design, not engineering. It is the population at which the auction house has sellers, groups form in minutes and towns look inhabited (MMO305 covers why).

| Plan | Queue at hour 3 | Wait at the back | Day-30 peak per world | Alive on day 30? |
|---|---|---|---|---|
| 10 worlds | 4,500 | 180 min | 3,000 | yes |
| 15 worlds | 750 | 30 min | 2,000 | no |
| 20 worlds | 0 | 0 | 1,500 | no |
| 10 worlds, layered to 6,000 for launch week | 1,125 | 30 min | 3,000 | yes |

The first three rows are the trade-off in its plain form. No fixed world count meets both targets. The last row is how most modern launches escape it. Each of the 10 worlds runs extra layers during launch week, which raises its cap to 6,000 and its entry rate to 150, since the extra layer is extra servers. Check it. The world fills at `λ = 120` (below the entry rate) and is full at minute 50. Then `μ = 6,000 / 160 = 37.5`. Minutes 50 to 60 add `(120 − 37.5) × 10 = 825`, and minutes 60 to 180 add `(40 − 37.5) × 120 = 300`, for 1,125 at hour 3. The wait at the back is `1,125 / 37.5 = 30` minutes, the same as 15 worlds, on about the same hardware. When the layers close, the population collapses to 10 communities of 3,000.

The layers are not free. MMO302 week 2 lists what they cost players. Friends on different layers cannot see each other, and players can hop layers to farm fresh copies of rare resources. They also cost money only while they run, which is the point. MMO404 week 13 showed that a server's cost per player-hour rises steeply as its fill drops. A layer closed on day 7 stops costing on day 7. A world opened on launch night and merged on day 60 has cost two months of low fill, and the merge is its own painful project (week 10 of this course).

Three other levers change the same curves:

- **Head start or staggered access** moves part of `A(t)` to earlier days (Lost Ark's founders, Guild Wars 2's pre-purchase head start), which lowers the shoulder on launch night itself.
- **Free transfers from full worlds** move players from a steep `A(t)` to a shallow one after the fact, as New World offered. They work only if players believe the new world will stay alive.
- **Selling fewer copies**, the FFXIV lever, flattens `A(t)` everywhere and costs revenue and goodwill.

A launch capacity plan is a document with one row per lever, the number it moves, and the day it is switched off.

## In-class activity (25 minutes)

In groups of three. Your MMO launches with 8 worlds, `C = 5,000`, entry rate `a = 125` per minute per world, and launch-night `L = 200` minutes. Across the game, 1,600 players per minute arrive in the first hour, 320 per minute in hours 2 to 4, and 120 per minute afterwards. Day-30 peak is forecast at 28,000, and a world needs 3,000 at peak to feel alive.

1. Compute each world's `λ` by phase, its `μ` once full, and the minute it fills.
2. Find the queue and the back-of-queue wait at hour 3 and at hour 4. When does the queue peak?
3. Is 8 worlds alive on day 30? Would 10 be?
4. Design a plan that keeps the wait at hour 4 under 60 minutes and passes the day-30 test. Use layers, a head start or both, and state each number you assume.

Expected output: per world `λ = 200`, 40 and 15; `μ = 25`. The world fills at the entry rate 125, full at minute 40 with a queue of 3,000, then the rush adds `(200 − 25) × 20 = 3,500`, so 6,500 at hour 1. Hours 2 to 4 add 15 per minute, 8,300 at hour 3 and 9,200 at hour 4, where it peaks (arrivals fall to 15, below 25). The wait at hour 4 is 368 minutes. On day 30, 8 worlds hold 3,500 each (alive), 10 worlds hold 2,800 (not alive). A layering plan that doubles each world to 10,000 and entry to 250 for launch week fills at minute 50 and has `μ = 50`, so the queue is `(200 − 50) × 10 = 1,500` at hour 1 and drains at 10 per minute in hours 2 to 4 (0 by about minute 210). Groups that add a head start should show which part of `A(t)` it moves.

## Common misconceptions

- **"The queue is worst right after the unlock."** The queue keeps growing as long as arrivals exceed admissions. It peaks when arrivals fall below `μ`, often hours later.
- **"Faster logins shorten the launch queue."** Entry speed matters only while worlds fill. At hour 3 the world is full and admits `C / L` regardless.
- **"`p × L / C` tells you the launch-night wait."** It assumes sessions end at random. At a launch, sessions are all young, and the real wait is longer.
- **"Open enough worlds and there is no problem."** The day-30 population does not grow with the world count. Extra worlds on launch night are thin worlds a month later.

## Check yourself

1. A world has `C = 3,000`, `a = 150`, `L = 120`. Its arrivals are 180 per minute for 30 minutes, then 35 per minute. Find when it fills, the queue at hour 2, and whether the queue is growing or shrinking then.
2. On a cumulative diagram, the `A` curve has slope 60 and the `D` curve slope 40 between minutes 90 and 150. The gap at minute 90 is 1,000. What is the queue at minute 150 and the wait at the back?
3. A producer says, "The arrival rate has fallen by two thirds since the unlock, so the queue must be shrinking." What must be true for that to be right?
4. Explain why a fixed session length of `L` gives a longer launch queue than random session ends with the same average `L`.
5. For the section 4 numbers, the day-30 forecast rises to 45,000. Which plans now pass the day-30 test? What would you do differently?

<details>
<summary>Answers</summary>

1. The world fills at 150 per minute while `λ = 180`, so the queue grows by 30 per minute and the world is full at minute 20 (queue 600). `μ = 3,000 / 120 = 25`. Minutes 20 to 30 add `(180 − 25) × 10 = 1,550`, so 2,150 at minute 30. Minutes 30 to 120 add `(35 − 25) × 90 = 900`, so 3,050 at hour 2. It is still growing, by 10 per minute.
2. The gap grows by `(60 − 40) × 60 = 1,200`, so the queue is 2,200. The wait at the back is about `2,200 / 40 = 55` minutes.
3. The new arrival rate must be below the admission rate `μ`. A fall of two thirds from 120 to 40 still leaves the queue growing if `μ = 25`.
4. At a launch, all sessions start within a short window. With fixed lengths, none of them end until `L` minutes have passed, so admissions stop almost entirely between filling and minute `L`. With random ends, a steady share leaves every minute from the start.
5. With 45,000 at peak, 10 worlds hold 4,500, 15 hold 3,000 and 20 hold 2,250. The 10-world, 15-world and layered plans all pass; 20 does not. Now 15 permanent worlds meet both targets (30-minute wait, 3,000 on day 30), so the layers are no longer needed for the launch-night target. You might still layer for safety, because a forecast that rose once can rise again.

</details>

## Lab / assignment hook

[Lab 02, launch queue planner](../labs/lab02.md). You build a launch-queue simulator with cumulative curves, three session-ending models, layers and a head start, reproduce this lecture's hour-3 table, then choose a capacity plan for a given forecast and write a one-page capacity memo. The memo is the first section of the launch plan assessed at the end of the course.

## Sources

- Wikipedia, "New World: Aeternum" (read September 2026). Release on 28 September 2021; over 700,000 concurrent players on Steam on release day; 2,000 players per server; queues on popular servers reaching the 25,000-person limit; additional servers in all regions within two days; tests to raise the 2,000 cap; free character transfers.
- Warcraft Wiki, "World of Warcraft: Classic" (read September 2026). Launch on 27 August 2019 at midnight CEST (26 August, 3 p.m. PDT, in the Americas); larger servers than the original and temporary layering; extreme login queues and additional servers in all regions; the team's expectation that most players would log in, log off and not return, citing Schreier, J. (2024), *Play Nice: The Rise, Fall, and Future of Blizzard Entertainment*, p. 277.
- Wikipedia, "Lost Ark (video game)" (read September 2026). Western release on 11 February 2022 by Amazon Games; founder's packs playable from 8 February; over 1.3 million concurrent players on Steam; long queues and a new European server region.
- Wikipedia, "Final Fantasy XIV" (read September 2026), section on A Realm Reborn. Early access from 24 August 2013, launch on 27 August; temporary suspension of digital sales.
- Wikipedia, "Guild Wars 2" (read September 2026). Pre-purchasers playing from 25 August 2012, launch on 28 August 2012.
- Newell, G. F. (1982). *Applications of Queueing Theory* (2nd ed.). Chapman and Hall. Cumulative arrival and departure curves for queues.
- MMO302 weeks 2, 9 and 13 and MMO404 week 13 (this program) for the full-world admission model, layers, autoscaling and cost per player-hour, with their sources.
- World caps, entry rates, session lengths, arrival schedules and day-30 forecasts in sections 2 to 4 and the activity are invented teaching values.

## Interactive spec: examples/w02-launch-queue-hour-three.html

**The one insight:** at a fresh launch, the queue keeps growing for as long as arrivals exceed admissions, so it peaks when the arrival rate falls below `C / L`, hours after the unlock spike. The rate chart looks calm while the cumulative chart shows the gap still widening.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "rates": x is time from 0 to 12 hours (labelled "unlock", "+1 h", …). A step line for arrivals per world `λ(t)` in `--blood`, and a line for admissions per minute `μ(t)` in `--steel` (entry-limited while filling, then `C / L`). Shade the region where `λ > μ` in a light `--blood` wash and label it "queue growing"; shade `λ < μ` in `--moss` as "queue shrinking".
- View B, "running totals": the same x axis. `A(t)` in `--blood` and `D(t)` in `--steel`. A vertical cursor (draggable, default at hour 3) shows a bracket between the curves labelled "queue Q" and a horizontal bracket from `A` across to `D` labelled "wait". The peak of `Q` is marked with a dot.
- Below both, a planning strip: a row of world tiles for the chosen world count, each tile showing launch-night queue at the cursor and day-30 peak population, coloured `--moss` if the day-30 population meets the "alive" threshold and `--ochre` otherwise.

**Controls:**

- World count `W`, 4 to 30, step 1 (default 10).
- Cap `C`, 1,000 to 10,000, step 250 (default 4,000).
- Entry rate `a`, 25 to 500 per minute, step 25 (default 100).
- Session length `L`, 30 to 300 minutes, step 10 (default 160).
- Arrivals across the game: rush rate (default 1,200/min), rush length (default 60 min), shoulder rate (default 400/min), shoulder end (default 180 min), night rate (default 150/min).
- Session model selector: "random, from full" (default), "random, from first minute", "fixed length".
- Layer toggle: multiplies `C` and `a` by a layer factor slider (1.0 to 3.0, default 1.5) for the whole simulated night.
- Day-30 forecast (default 30,000) and "alive" threshold (default 2,500).
- Cursor time (draggable in View B, and a slider for keyboard users).

**Readout (always visible, `aria-live="polite"`):** per-world `λ` by phase, `μ` once full, minute the world fills, queue and wait at the cursor, peak queue and its minute, minute the queue empties, day-30 per-world peak and pass/fail.

**Formulas (per world, one-minute steps, `t = 0, 1, …, 719`):**

```
λ(t) = demand(t) / W
queue += λ(t)
session model "random, from full":  if online ≥ C: online −= C / L
session model "random, from first": online −= online / L
session model "fixed length":       online −= admitted[t − L]  (if t ≥ L)
admit = min(queue, a, C − online);  queue −= admit;  online += admit;  admitted[t] = admit
Q at hour h = queue after minute 60h − 1 (log index 60h − 1)
wait at the back = Q / (C / L)
day-30 per world = forecast / W
```

**Test values (must match, defaults unless stated):**

- `W = 10`: queue 2,700 at 1 h, 4,500 at 3 h (peak, minute 180), empty at minute 630; wait at 3 h 180 min; day-30 3,000, alive.
- `W = 15`: 550 at 1 h, 750 at 3 h, empty at minute 230; day-30 2,000, not alive.
- `W = 20`: 0 at 1 h and 3 h; peak 15 at minute 82; day-30 1,500.
- `W = 10`, layer factor 1.5 (`C = 6,000`, `a = 150`): 825 at 1 h, 1,125 at 3 h, empty at minute 230; wait 30 min.
- `W = 10`, entry rate 400: queue at 3 h 4,350.
- `W = 10`, "random, from first minute": about 4,059 at 3 h.
- `W = 10`, "fixed length": 3,200 at 1 h, 7,200 at minute 160 (peak), 6,000 at 3 h.

**First screen:** defaults with the cursor at hour 3. Caption: "Arrivals dropped by two thirds two hours ago. The queue is still growing: 4,500 people, 180 minutes. Drag the world count."

**Accessibility:** all controls keyboard operable with visible focus; the cursor moves with arrow keys (1 minute) and Shift plus arrows (10 minutes); readout in `aria-live="polite"`; respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.
