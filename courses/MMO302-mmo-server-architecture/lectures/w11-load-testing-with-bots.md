# MMO302 · Week 11 — Load Testing with Bots

**Why this matters:** Your server will meet its real load on launch night, with thousands of players and the whole internet watching. A load test is the only rehearsal you get. Run it badly and it tells you the server is fine right up to the moment it is not, because the bots were too polite, too spread out, or measured the wrong thing.

**You will be able to:**
- Compute mean and 99th-percentile response time for a service from its capacity and offered load, and locate the "knee" where latency takes off.
- Use Little's law to move between queue length, arrival rate and waiting time.
- Explain coordinated omission and design open-loop bots that measure latency honestly.
- Design a bot fleet whose traffic shape (clustering, message mix, ramp) matches the players you expect, and run a ramp test against a real server.

**Before class:** Gil Tene, "How NOT to Measure Latency" (QCon San Francisco 2015, video on InfoQ), the first 25 minutes. The `wrk2` README on GitHub, the closing section on coordinated omission. Blizzard, "Mark Your Calendars: WoW Classic Launch and Testing Schedule" (May 2019).

**Prerequisites from earlier courses:** [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (percentiles and why the mean hides the tail). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (memoryless waiting, the discrete cousin of the exponential used here). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). [CS102 week 6, queues](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w06-queues-and-stacks-undo-and-command-buffers.md). [CS102 week 11, state machines](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w11-state-and-state-machines.md) (bot behavior). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) (tick time as a CPU budget). From this course, [week 1, the n-squared problem](w01-scale-targets-ccu-messages-and-n-squared.md), [week 3, area of interest](w03-area-of-interest-grids-radius-hysteresis.md), [week 5, tick rate](w05-tick-rate-for-mmos-vs-shooters.md), [week 9, the login queue](w09-login-character-select-gateway-services.md) and [week 10, fan-out](w10-chat-guild-and-social-services.md).

**Interactive:** [examples/w11-latency-knee.html](../examples/w11-latency-knee.html). Keep it open during section 2.

---

## 1. What a load test is for

A **load test** drives a server with synthetic clients, called **bots**, and measures how it behaves as load grows. For an MMO the bots are headless clients. They speak the real network protocol, log in with test accounts, move, chat, fight and trade, but they draw nothing.

A load test answers four different questions, and each wants a different test shape.

- **Ramp test.** Increase the bot count in steps and hold each step long enough to settle. Answers "how many players before we miss our target?"
- **Soak test.** Hold a realistic load for hours. Answers "does anything grow without limit?" Memory leaks, unbounded queues, a table that never gets vacuumed.
- **Spike test.** Go from quiet to peak in seconds. Answers "what happens after a server restart, when everyone logs in at once?" Week 10's presence storm is a spike.
- **Stress test.** Push past the limit on purpose. Answers "how does it fail?" A server that slows down and recovers is fine. One that crashes, corrupts saves or loses items is not.

Every test needs a pass line written down before it starts. That line is a **service level objective (SLO)**, a target on a measured quantity, for example "99% of player actions answered within 100 ms" or "99% of ticks finish within the 100 ms tick budget." Without an SLO, a test produces a graph and an argument.

The SLO is written as a **percentile**, not a mean. MA102 week 12 showed that the mean of a skewed sample hides its tail. Response times are always skewed, since they cannot go below the service time but can grow without limit. The player who rage-quits is in the tail.

## 2. Worked example: finding the knee

### The hook

In the summer of 2019 Blizzard ran three public stress tests before World of Warcraft Classic launched. The announcement said the tests would "push our tech to the limit," and Blizzard capped character levels during them so that players would crowd into the same starting areas. Blizzard wanted the load concentrated on purpose.

Here is the question that makes load testing necessary. Suppose a server is 80% busy at 800 players. How many players can it take? Most people answer "about 1,000." At 1,000 it is 100% busy, and the players see something much worse than 25% slower responses. The rest of this example shows why.

### The model

Treat one service, say the process that handles player actions for a zone, as a single worker with a queue in front of it. Requests arrive at random and are served one at a time in arrival order. This is the **M/M/1 queue**, the simplest model in queueing theory. The two Ms say that arrivals are random (Poisson) and that service times are random (exponential). The 1 is the single worker.

```
capacity          μ = requests per second the worker can finish (1 / mean service time)
offered load      λ = n × r      (n bots, each sending r requests per second)
utilization       ρ = λ / μ      (share of time the worker is busy; must stay below 1)
mean response     W = 1 / (μ − λ)
p99 response      W99 = ln(100) / (μ − λ) ≈ 4.6 / (μ − λ)
Little's law      N = λ × W      (average number of requests in the system)
```

- A **response time** here includes both waiting in the queue and being served.
- In an M/M/1 queue the response time is itself exponential with rate `μ − λ`, which is where the p99 formula comes from. The `ln(100)` factor is the same one that gives the 99th percentile of any exponential.
- **Little's law** holds for almost any stable queue, not only M/M/1. If 450 requests arrive per second and each spends 20 ms in the system, then on average `450 × 0.02 = 9` are inside it.

Look at the denominator `μ − λ`. It is the server's **spare capacity**. Response time is inversely proportional to spare capacity, not to load. When spare capacity halves, response time doubles. When it approaches zero, response time approaches infinity.

### Numbers you can check

A service takes 2 ms per request on average, so `μ = 500` per second. Each bot sends one action every two seconds, `r = 0.5`.

```python
import math

MU = 500          # requests per second one service can finish (2 ms each)
RATE = 0.5        # requests per second per bot (one action every 2 s)

print(f"{'bots':>5} {'load':>5} {'mean ms':>8} {'p99 ms':>8} {'in system':>10}")
for bots in [200, 500, 800, 900, 950, 980]:
    lam = bots * RATE
    rho = lam / MU
    mean = 1 / (MU - lam)                  # M/M/1 time in system, seconds
    p99 = math.log(100) / (MU - lam)       # 99th percentile of that time
    in_system = lam * mean                 # Little's law, L = lambda * W
    print(f"{bots:>5} {rho:>5.0%} {mean*1000:>8.1f} {p99*1000:>8.1f} {in_system:>10.1f}")
```

It prints:

```
 bots  load  mean ms   p99 ms  in system
  200   20%      2.5     11.5        0.2
  500   50%      4.0     18.4        1.0
  800   80%     10.0     46.1        4.0
  900   90%     20.0     92.1        9.0
  950   95%     40.0    184.2       19.0
  980   98%    100.0    460.5       49.0
```

Check the 900 row by hand. `λ = 900 × 0.5 = 450`, so spare capacity is `500 − 450 = 50` per second. Mean response `1 / 50 = 20` ms. p99 `4.605 / 50 = 92.1` ms. Requests in the system `450 × 0.02 = 9`. One printing detail. The 200 row's exact value is `100 × 0.0025 = 0.25` requests, and Python rounds an exact half to the even digit, so it prints 0.2.

Now read the table the way a launch team should. Going from 200 to 800 bots, four times the players, costs 34.6 ms at p99. Going from 800 to 900, one eighth more players, costs another 46 ms. Going from 900 to 980 costs 368 ms more. With an SLO of "p99 under 100 ms," this service passes at 900 and fails at 950. The **knee** is the region where each added player costs more latency than all the players before it, and here it sits between 80% and 95% utilization.

Back to the hook. At 800 players the server is 80% busy. At 1,000 it is 100% busy, the queue has no stable length, and response time grows for as long as the load lasts. The answer to "how many players can it take?" is about 900, and the reason is the tail, not the average.

### A visual the student can move

Open `examples/w11-latency-knee.html`. The left panel plots utilization against bot count. It is a straight line, and it looks harmless. The right panel plots mean and p99 response time on the same horizontal axis, with your SLO as a horizontal line. Drag the bot count from 200 to 980 and watch the left panel creep while the right panel turns a corner and goes vertical. Then halve the service time. The whole right curve slides to the right and keeps its shape. Buying a faster server moves the knee. It does not remove it.

The third control switches the bots from open loop to closed loop, the subject of section 3. Watch the right panel flatten into a comfortable lie.

### Cross-game recognition

**World of Warcraft Classic stress tests (May to July 2019).** Blizzard capped levels so that players would pile into a few zones, which drives `λ` for those zone servers far above what an even spread would give. In the model, the test raised `λ` on the servers that matter most at launch, the starting zones, which is where the queue knee would appear first. A stress test that spreads players out evenly measures a server that will never exist on launch night.

**EVE Online mass tests (Singularity, ongoing).** CCP runs "mass tests" on its public test server, Singularity, and rewards players who join with skill points to spend on that server. Large fights in EVE are the worst case for the server (week 12), and no bot script reproduces how several hundred real pilots actually behave in a fight. CCP's answer is to recruit real players as the load. In the model, these tests measure `μ` for fight-shaped load, which synthetic bots could only guess at.

**Discord's guild process, from week 10.** A 30,000-member guild received about 25 posts a second, and each post took about 1.5 s of sending. Rewrite that as a queue. `λ = 25` per second, `μ = 1 / 1.5 ≈ 0.67` per second, so `ρ ≈ 37.5`. The model says no stable queue exists, and Discord saw the process fall behind at peak. Any service with `ρ > 1` over a sustained period is not "slow." It is broken.

**Your own login queue (week 9).** Little's law also runs backwards. If your login service admits 20 players a second and 3,000 players are in the queue, each waits about `3,000 / 20 = 150` seconds. You can print that estimate on the queue screen without measuring anyone's wait.

### Eyes-open design judgment

- **Plan for 60 to 70% utilization at expected peak, not 100%.** At 70% the p99 in our table is about `4.6 / (500 − 350)` ≈ 31 ms, and a 20% surprise in players only takes you to 84%. At 90%, a 10% surprise takes you over the edge.
- **Real game traffic is burstier than Poisson.** Players act in bursts, a boss pull, a gate opening, a world event, and a tick-based server receives its inputs in batches. Burstier arrivals move the knee to the left. Treat the M/M/1 table as the best case and let the test find the real knee.
- **Report p99 and max, per step.** A mean that rises from 2.5 to 20 ms looks acceptable. A p99 of 92 ms is where the players are.
- **A tick is a queue too.** For a tick-based zone server, the "request" is the tick and the "service time" is the tick's CPU cost. CS202 week 13 treated tick time as a budget. Under load, tick cost grows with players, and the p99 tick time shows the knee the same way.

### Check this example

1. A chat service handles 2,000 requests per second at capacity. Bots offer 1,600 per second. What are the mean and p99 response times? How many requests are in the system on average?
2. For the lecture's service (`μ = 500`, `r = 0.5`), what is the largest bot count that keeps p99 at or under 50 ms?
3. A team doubles `μ` to 1,000. The designers double the players too. Is the p99 the same as before, better or worse? Show it with the 900-bot row.

<details>
<summary>Answers</summary>

1. Spare capacity `2,000 − 1,600 = 400`. Mean `1 / 400 = 2.5` ms. p99 `4.605 / 400 ≈ 11.5` ms. In system `1,600 × 0.0025 = 4`.
2. `4.605 / (500 − 0.5 n) ≤ 0.05` gives `500 − 0.5 n ≥ 92.1`, so `n ≤ 815`.
3. Better. With 1,800 bots, `λ = 900`, spare capacity `1,000 − 900 = 100`, p99 `4.605 / 100 = 46` ms, half the old 92 ms. Utilization is the same 90%, but response time depends on spare capacity in absolute terms, and that doubled.

</details>

## 3. Bots that lie: coordinated omission

The obvious way to write a bot is a loop. Send an action, wait for the reply, record how long it took, think for a moment, repeat. This is a **closed-loop** bot. It is also the most common way to get a load test wrong.

Here is the problem. When the server slows down, a closed-loop bot waits longer for each reply, so it sends fewer requests. The server gets less load exactly when it is struggling, and the bot records only the requests it managed to send. The slow period is under-sampled by the very bots measuring it. Gil Tene named this **coordinated omission**. The load generator coordinates with the server so that it avoids measuring during the bad moments. The `wrk2` benchmarking tool was written to avoid it.

Real players do not behave like closed-loop bots. A client sends movement updates on a timer whether or not the last reply came back, and thousands of players on different machines do not slow down together because one server is behind. The honest bot is **open loop**. It decides in advance when each request should be sent, sends it on schedule, and measures latency from the *intended* send time, not the actual one.

You can see the size of the lie with a small simulation of the section 2 server.

```python
import heapq, random

MU, RATE, SECONDS = 500, 0.5, 600      # capacity (req/s), per-bot rate, test length

def p99(xs):
    xs = sorted(xs)
    return xs[int(0.99 * (len(xs) - 1))]

def open_loop(bots, seed=1):
    """Each bot sends on its own timer, whether or not old replies came back."""
    rng = random.Random(seed)
    t, free_at, lat = 0.0, 0.0, []
    while True:
        t += rng.expovariate(bots * RATE)          # next request from any bot
        if t > SECONDS:
            return lat
        start = max(t, free_at)                    # wait while the server is busy
        free_at = start + rng.expovariate(MU)      # random service time, mean 2 ms
        lat.append(free_at - t)

def closed_loop(bots, seed=1):
    """Each bot waits for its reply, thinks, then sends again."""
    rng = random.Random(seed)
    events = [(rng.expovariate(RATE), b) for b in range(bots)]
    heapq.heapify(events)
    free_at, lat = 0.0, []
    while events:
        t, b = heapq.heappop(events)
        if t > SECONDS:
            break
        start = max(t, free_at)
        free_at = start + rng.expovariate(MU)
        lat.append(free_at - t)
        heapq.heappush(events, (free_at + rng.expovariate(RATE), b))
    return lat

for bots in [900, 1200]:
    for name, run in [("open", open_loop), ("closed", closed_loop)]:
        lat = run(bots)
        print(f"{bots} bots, {name:>6} loop: {len(lat) / SECONDS:3.0f} req/s sent, "
              f"p99 {p99(lat) * 1000:7,.0f} ms")
```

It prints:

```
900 bots,   open loop: 450 req/s sent, p99      97 ms
900 bots, closed loop: 446 req/s sent, p99      77 ms
1200 bots,   open loop: 600 req/s sent, p99 119,372 ms
1200 bots, closed loop: 500 req/s sent, p99     562 ms
```

At 900 bots the open-loop p99 of 97 ms is close to the model's 92.1 ms, as it should be for a ten-minute sample. The closed-loop bots already report 20 ms less, because they send a little less while the server is busy.

At 1,200 bots the two stories split completely. The open-loop bots offer 600 requests a second to a server that can finish 500. The queue grows by 100 requests every second for ten minutes, and the p99 player waits about two minutes. The closed-loop bots report a p99 of about half a second and a throughput of exactly 500 per second. A team reading only the closed-loop numbers would say "slow but working." In reality the server is past its limit and getting worse every second. The tell is in the throughput column. The closed-loop fleet sent 500 requests a second, not the 600 the test plan asked for, and nobody planned that.

Two rules follow.

1. **Schedule sends in advance, measure from the schedule.** Lab 11's bot fleet does exactly this.
2. **Always report offered load next to achieved load.** If the bots sent less than you asked, your test measured a different load than the one you meant to measure.

## 4. Bots that behave like players

An honest clock is not enough. The bots also have to put load where players put it.

### Clustering

Use a simpler version of week 3's grid AOI, where each player hears only about the others in their own cell (a 1 × 1 block instead of 3 × 3). The 3 × 3 block raises both counts, and the clustered one far more. Take 1,000 bots on a map of 100 cells. If the bots spread evenly, each cell holds 10, and each bot hears from 9 others:

```
uniform:     1,000 × 9 = 9,000 updates per tick
```

Now put half of them in one town cell, the way players gather at a bank, a quest hub or a world boss, and spread the rest over the other 99 cells (five cells get 6 bots, 94 cells get 5):

```
clustered:   500 × 499  +  5 × (6 × 5)  +  94 × (5 × 4)
           = 249,500    +  150          +  1,880
           = 251,530 updates per tick
```

Same bot count, 28 times the traffic. At 10 ticks a second that is 90,000 against 2.5 million updates a second. A bot fleet that wanders at random tests the uniform case. Launch night is the clustered case. This is why Blizzard capped levels during the Classic stress tests.

### Message mix

Players do not send one kind of message. A bot script should produce the mix you expect, with rates you can defend:

| Behavior | Rate per bot | What it loads |
|---|---|---|
| Movement input | 10 per second while moving | Zone simulation, AOI, outbound snapshots |
| Combat action | 0.5 to 1 per second in combat | Zone simulation, combat rules |
| Chat post | about 0.001 per second | Chat fan-out (week 10) |
| Loot, trade, vendor | a few per minute | Database transactions (week 8) |
| Zone change | a few per hour | Handoff (week 4), persistence |
| Login and logout | once per session | Gateway, auth, presence (weeks 9 and 10) |

These rates are planning assumptions for this course's reference game, not measurements from a shipped title. Replace them with telemetry from your own playtests as soon as you have any (DB201 covers telemetry). The point is that a load test with only movement will never find the bug in the trade path.

### Scripting a bot

Write each bot as a state machine (CS102 week 11). States such as `LoggingIn`, `Traveling`, `Questing`, `Fighting`, `Trading` and `Idle`, with transition probabilities per second, give you a controllable mix. Give each bot its own seeded random generator so a failing run can be replayed exactly. Reuse the real client's network code, not a copy, or the bots will test a protocol your players never speak.

One machine can usually run hundreds of bots, because a headless bot does little more than build packets. Many bots share a few network connections in some load tools, which saves ports and threads. That is fine for services where connections are cheap. For a gateway, whose job includes managing one connection per player, use one connection per bot, or you are not testing the gateway.

## 5. Running the test

A ramp test for this course's final project (500 bots against your world server) looks like this.

1. **Write the SLO and the plan.** For example "p99 action response ≤ 100 ms and p99 tick time ≤ 100 ms at every step up to 500 bots." Steps of 100 bots, 3 minutes each, after a 1-minute warm-up.
2. **Measure the server, not only the bots.** Record per step: tick time percentiles, queue lengths, CPU per core, memory, garbage-collection pause times (the .NET runtime reports them), database connections in use and query time, and bytes sent. Week 14 turns these into proper metrics.
3. **Record offered and achieved load** for every step, as section 3 demands.
4. **Stop when the SLO breaks, then go one step further** to see how it fails. Does the server recover when load drops back?
5. **Soak at 70% of the knee** for at least an hour. Watch memory and queue lengths for slopes.
6. **Keep the bots off the server's machine.** A bot fleet on the same host competes for CPU and makes the server look worse than it is.

The output is a short report with one table (step, offered, achieved, p50, p99, max, CPU) and one sentence: "the knee for this build is between N and M bots, limited by X."

## In-class activity (25 minutes)

Pairs. Your zone server's action service has a mean service time of 1.25 ms. Your SLO is p99 ≤ 50 ms. Each player sends 0.8 actions per second on average.

1. Compute `μ` and the largest player count that meets the SLO under the M/M/1 model.
2. Your designers plan a world event that doubles action rates for players in one zone. How many players can that zone hold during the event?
3. Your QA lead proposes a closed-loop bot that waits for each reply and then sleeps 1.25 s. Predict what its report will show at 1.2 times the player count from step 1, and write one sentence to the lead explaining why the report cannot be trusted.

Expected output: two numbers, a prediction, one sentence.

## Common misconceptions

- **"80% busy means 20% headroom."** Headroom in players is not headroom in latency. Response time depends on `1 / (μ − λ)`, which has already quadrupled between 20% and 80% busy, and doubles again by 90%.
- **"The average response time is what players feel."** Players remember the worst moments. Report p99 and max.
- **"If the bots say it is fine, it is fine."** Closed-loop bots under-report exactly when the server struggles. Check that achieved load matches offered load.
- **"More bots is a harder test."** A thousand bots spread evenly can load the server less than two hundred standing in one town. Match the shape of real play, not only the count.

## Check yourself

1. A login service admits 25 players per second. A queue screen shows 4,000 players waiting. Estimate the wait for someone joining the back of the queue.
2. A service has `μ = 1,200` per second. Bots offer 1,080 per second. Compute utilization, mean and p99 response time. Then compute the same after an optimization cuts the service time by 20%.
3. A test report shows, at 1,500 bots, "offered 750 req/s, achieved 610 req/s, p99 95 ms." Is the server meeting a 100 ms p99 SLO at 1,500 bots? Explain.
4. 600 bots on a 60-cell map. Compare updates per tick for an even spread and for 300 bots in one cell with the rest spread evenly over the other 59 cells (rounded to whole bots, 5 cells with 6 and 54 with 5).

<details>
<summary>Answers</summary>

1. Little's law, `W = N / λ = 4,000 / 25 = 160` seconds, a little under three minutes.
2. `ρ = 1,080 / 1,200 = 90%`. Spare capacity 120, mean `8.3` ms, p99 `4.605 / 120 ≈ 38.4` ms. After the 20% cut in service time, `μ = 1 / (0.8 / 1,200) = 1,500`. `ρ = 72%`, spare 420, mean 2.4 ms, p99 about 11 ms. A 20% faster service cut the p99 by more than two thirds, because it more than tripled the spare capacity.
3. No. The bots could not send what the plan asked, which is the signature of closed-loop bots or a saturated fleet. The 95 ms p99 was measured on 610 requests a second, not on the 750 real players would send. Re-run with open-loop bots before drawing a conclusion.
4. Even: 10 per cell, `600 × 9 = 5,400` updates. Clustered: `300 × 299 + 5 × 30 + 54 × 20 = 89,700 + 150 + 1,080 = 90,930`, about 17 times more.

</details>

## Lab / assignment hook

[Lab 11, ramp test with an open-loop bot fleet](../labs/lab11.md). You finish a Python bot fleet that drives a small TCP service, ramp it from 200 to 1,200 bots, find the knee against a 100 ms SLO, and compare open-loop and closed-loop results. The same method, with your own C# world server in place of the toy service, is the course's final 500-bot load test.

## Sources

- Blizzard Entertainment, "Mark Your Calendars: WoW Classic Launch and Testing Schedule" (World of Warcraft news, 14 May 2019, archived copy of 3 July 2019 on web.archive.org). Stress tests on 22 to 23 May, 19 to 20 June and 25 to 26 July 2019 (the third first planned for 18 to 19 July); the aim to "push our tech to the limit"; level caps to put many players close together; launch on 26 to 27 August 2019 depending on region. Warcraft Wiki, "Stress test" (accessed September 2026): level cap of five on stress-test realms.
- EVE University Wiki, "Singularity" (accessed September 2026). CCP runs mass tests on the Singularity test server and rewards participants, often with skill points for use on that server.
- Discord Engineering, "How Discord Scaled Elixir to 5,000,000 Concurrent Users" (6 July 2017). Figures as used in week 10.
- Tene, G. "How NOT to Measure Latency" (QCon San Francisco 2015, published on InfoQ March 2016).
- Tene, G. `wrk2` README (GitHub, giltene/wrk2). Definition of coordinated omission in closed-loop load generators and the constant-rate fix.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula L = λW." *Operations Research* 9(3), 383-387.
- Kleinrock, L. (1975). *Queueing Systems, Volume 1: Theory*. Wiley. The M/M/1 queue and its exponential response-time distribution.

## Interactive spec: examples/w11-latency-knee.html

**Insight the visual must make obvious:** utilization grows in a straight line with players, but response time grows with `1 / (μ − λ)`, so the p99 turns a corner and goes vertical near 100%. A faster server slides the corner right without changing its shape. Closed-loop bots flatten the curve and hide the corner.

**Layout.** Two linked charts side by side on desktop, stacked under 700 px (utilization first), number panel beneath. Shared x axis: bots `n`, linear, 0 to `1.2 × μ / r`.

**Left chart, "How busy the server is".** y axis utilization 0 to 120%. Line `ρ = n r / μ`. Shade above 100% and label it "no stable queue". Marker at the current `n`.

**Right chart, "What players wait".** y axis milliseconds, linear 0 to 500, clipped with an arrow when off-chart. Lines: mean `W = 1000 / (μ − n r)` and p99 `W99 = 1000 × ln(100) / (μ − n r)` for `n r < μ`. Stop the lines at `ρ = 0.995`. Horizontal dashed line at the SLO. Vertical dashed line at the knee `n* = (μ − ln(100) × 1000 / SLO) / r`, labelled "SLO limit". In closed-loop mode, draw a third line (see below) and fade the open-loop lines.

**Controls.**
- Bots `n`: slider, 0 to `1.2 × μ / r`, default 900.
- Mean service time: slider 0.5 to 10 ms, default 2 ms (`μ = 1000 / service_ms`).
- Rate per bot `r`: slider 0.1 to 2 per second, default 0.5.
- SLO p99: slider 20 to 500 ms, default 100.
- Toggle "closed-loop bots" with think time `Z` slider 0.5 to 5 s, default `1 / r`.

**Closed-loop line.** Use the exact mean-value analysis (MVA) for a closed network of one M/M/1 station plus a think-time delay: for `k = 1..n`, `R_k = S × (1 + Q_{k−1})`, `X_k = k / (R_k + Z)`, `Q_k = X_k × R_k`, with `S = 1/μ`, `Q_0 = 0`. Plot `R_n` in ms (mean response as the closed-loop bot reports it). Show achieved throughput `X_n` in the panel next to offered `n / Z`.

**Number panel.** Offered load `n r`, utilization, spare capacity `μ − n r`, mean and p99 in ms (or "unbounded" when `ρ ≥ 1`), Little's-law requests in system, knee `n*`. In closed-loop mode also: achieved throughput and "the bots sent X% less than planned".

**Test values** (assert on load, `μ = 500`, `r = 0.5`, SLO 100 ms): `n = 200` gives 20%, mean 2.5 ms, p99 11.5 ms. `n = 900` gives 90%, mean 20.0 ms, p99 92.1 ms, in system 9.0. `n = 980` gives 98%, mean 100.0 ms, p99 460.5 ms. Knee `n* = (500 − 46.05) / 0.5 = 907.9`, shown as 907. With service time 1 ms and `n = 1,800`: 90%, p99 46.1 ms.

**First screen:** `n = 900`, open loop, caption "90% busy: p99 is 92 ms. Add 80 bots and it is 460 ms."

**Accessibility.** Keyboard reachable controls, `aria-live="polite"` number panel, text labels on all reference lines, reduced motion disables transitions.
