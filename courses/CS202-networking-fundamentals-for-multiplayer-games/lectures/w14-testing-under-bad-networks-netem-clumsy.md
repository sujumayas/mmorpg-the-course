# CS202 · Week 14 — Testing under bad networks (netem, clumsy)

**Why this matters:** Your netcode works on localhost, where the round trip is under a millisecond and nothing is ever lost. Players will run it on Wi-Fi next to a microwave. Every technique from this term (prediction, reconciliation, interpolation, reliability) has branches that only run when the network misbehaves, and a branch that never runs in testing is a branch that ships broken. This week is about making the network misbehave on purpose, in a way you can measure and repeat.

**You will be able to:**
- Compute how long a test must run to trigger a bug that needs a burst of `k` lost packets, for independent and bursty loss, and choose test settings from that number.
- Translate the settings of netem, clumsy and the Unreal and Unity simulators into one model (loss rate, burst length, direction, delay, jitter) and predict what each will do to a game's traffic.
- Predict how much reordering a jittered delay creates at a given send rate, and decide whether a test should include it.
- Design a test matrix of network profiles with seeds, invariants and pass/fail metrics, and run it automatically.

**Before class:** Linux `tc-netem(8)` manual page, the options and examples sections (man7.org, 20 minutes). Epic Games, "Using Network Emulation in Unreal Engine" (UE 5 documentation). Unity Transport 2.4 manual, "Using pipelines", the simulator section. Reread your notes from MA102 week 7 on waiting times.

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (waiting for a rare event, and the 95th-percentile wait). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (checking a formula with seeded runs). [CS102 week 14, unit testing gameplay rules](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w14-unit-testing-gameplay-rules.md) (seeded, repeatable tests). [CS202 week 2](w02-latency-jitter-loss-measure-your-own.md) (the Gilbert-Elliott burst model, `q`, round-trip loss) and [week 13](w13-tick-rate-and-bandwidth-budgets.md) (send rates). Prediction, reconciliation and interpolation come from [CS202 weeks 8](w08-client-side-prediction.md), [9](w09-server-reconciliation.md) and [10](w10-entity-interpolation.md), and reliability over UDP from [week 6](w06-reliability-over-udp.md).

**Interactive:** [examples/w14-burst-hunt.html](../examples/w14-burst-hunt.html). Keep it open during section 2.

---

## 1. Three places to break a network

A **network conditioner** (or network emulator) is anything that sits between your game's sockets and deliberately delays, drops, duplicates or reorders packets. You can put one in three places.

- **Inside the game.** The engine's own transport drops and delays packets before they reach the socket. Unreal has `PktLag`, `PktLoss`, `PktIncomingLoss`, `PktOrder`, `PktDup` and more. Unity Transport has a `SimulatorPipelineStage`. Source has `net_fakelag`, which Valve used for the 200 ms lag compensation screenshot in its own networking documentation.
- **In a proxy.** A small program forwards UDP between client and server and misbehaves on the way. Lab 02's `bad_net_proxy.py` is one. You point the client at the proxy's port instead of the server's.
- **In the operating system.** The OS impairs packets on a network interface, so every program using it is affected and neither the game nor its engine knows. On Linux the tool is **netem**, a queueing discipline you configure with `tc`. On Windows the common free tool is **clumsy**, which intercepts packets with the WinDivert driver.

Each place trades one thing for another.

| Where | Reproducible with a seed | Affects | Needs a special build | Good for |
|---|---|---|---|---|
| In the game | Yes, if you seed it | Only the game's traffic | No, but only on engines that include it | Every developer, every day, and automated tests |
| Proxy | Yes | Only traffic you route through it | No | Tests of a shipped build, cross-platform |
| OS (netem, clumsy) | Partly (netem has a `seed` option) | Every packet on the interface, unless filtered | No | Final checks on real builds, the whole stack including the OS |

Use all three. The in-game simulator runs in continuous integration. The OS tool catches what the in-game one cannot see, such as the engine's own timers behaving differently when real packets are late.

## 2. Worked example: the bug that needs three lost packets

### The hook

Two engine vendors give opposite advice. Epic's Unreal Engine documentation tells you to test locally with extremely harsh conditions, and gives as examples a 500 ms round trip and 10% packet loss or higher. Unity's Transport manual says the drop percentage should rarely go above 3%, even when simulating a poor connection. One says crank it up. The other says stay realistic. Both are right, and the model below shows which question each one answers.

### The model

Take a real kind of bug. Your client interpolates other players 120 ms in the past from 30 Hz snapshots. That is three snapshot intervals of buffer (week 2's model, one interval deeper than Source's default) plus 20 ms to absorb jitter. One or two lost snapshots in a row are covered. Three in a row empty the buffer, and the client takes the "extrapolate" branch, a piece of code that almost never runs. If that branch has a bug, you will see it only when the network delivers a **burst** of at least `k = 3` consecutive losses.

Use the two-state loss model from week 2.

- `p` is the average loss rate.
- `q` is the chance that a packet is lost given the one before it was lost. For independent loss, `q = p`. Mean burst length is `1 / (1 − q)`.
- `r` is the send rate, in packets per second.

A burst of length at least `k` starts at a given packet when that packet is lost, the packet before it was not, and the next `k − 1` are lost too. In the long run this happens a fraction

```
β = p × (1 − q) × q^(k − 1)          bursts of length ≥ k, per packet
λ = 60 × r × β                        such bursts per minute
```

Bursts arrive roughly at random, so the waiting time for the first one is (almost) exponential, the continuous version of MA102 week 7's geometric wait.

```
P(seen within t minutes) = 1 − e^(−λ t)
mean wait               = 1 / λ
95% chance by           t95 = ln(20) / λ ≈ 3.0 / λ
```

For independent loss, `β = (1 − p) × p^k`, which for small `p` is close to `p^k`. That power is the heart of the problem. Rare events at a low loss rate are rare to the power `k`.

### Numbers you can check

`r = 30` Hz, so 1,800 snapshots per minute, and `k = 3`.

| Profile | `p` | `q` | Mean burst | `β` (per packet) | Bursts ≥ 3 per minute | Mean wait | 95% found by | Found in a 10-minute playtest |
|---|---|---|---|---|---|---|---|---|
| Independent 1% | 0.01 | 0.01 | 1.01 | 9.9 × 10⁻⁷ | 0.0018 | 9.4 h | 28 h | 1.8% |
| Independent 3% (Unity's ceiling) | 0.03 | 0.03 | 1.03 | 2.62 × 10⁻⁵ | 0.047 | 21 min | 64 min | 38% |
| Independent 10% (Unreal's example) | 0.10 | 0.10 | 1.11 | 9.0 × 10⁻⁴ | 1.62 | 37 s | 1.9 min | ~100% |
| Bursty 1% | 0.01 | 0.5 | 2.0 | 1.25 × 10⁻³ | 2.25 | 27 s | 1.3 min | ~100% |
| Bursty 1%, milder | 0.01 | 0.3 | 1.43 | 6.3 × 10⁻⁴ | 1.13 | 53 s | 2.6 min | ~100% |

Check two cells by hand. Independent 3%: `β = 0.03 × 0.97 × 0.03² = 2.62 × 10⁻⁵`, and `1,800 × 2.62 × 10⁻⁵ = 0.047` per minute, so `t95 = 3.0 / 0.047 = 64` minutes. Bursty 1%: `β = 0.01 × 0.5 × 0.5² = 0.00125`, and `1,800 × 0.00125 = 2.25` per minute.

Four results are worth a sentence each.

- **A realistic independent-loss test will not find this bug.** At 1% independent loss, a whole team playtesting for 10 minutes has under a 2% chance of triggering it. Real players, in their millions of hours, will trigger it every day.
- **Unreal's harsh setting finds it in about two minutes.** 10% loss is not what players have. It is a way to make a `p³` event common. That is the question Epic's advice answers: does every branch work?
- **Burstiness beats rate.** Bursty 1% triggers the bug faster than independent 10%, while losing a tenth as many packets. If your conditioner only offers independent loss, you are testing a network that does not exist and missing the patterns that do.
- **Each extra packet of buffer multiplies the wait by about `1 / q`.** For independent loss that is a factor of 100 at 1%. With a four-deep buffer at 1% independent loss, the mean wait for one failure is about 39 days of nonstop testing. For bursty loss with `q = 0.5`, it is only a factor of 2.

To check the formula, simulate it. 400 seeded runs of the bursty 1% profile at 30 Hz found the first burst of three after a median of 0.31 minutes, with 95% of runs done by 1.36 minutes. The model predicts `ln(2) / 2.25 = 0.31` and `1.33`. Here is the dropper those runs used.

```python
import random

class GilbertLoss:
    """Two-state burst loss with average rate p and P(loss | previous lost) = q."""
    def __init__(self, p, q, seed):
        self.rng = random.Random(seed)
        self.q = q
        self.a = p * (1 - q) / (1 - p)     # P(loss | previous delivered)
        self.lost = False

    def drop(self):
        chance = self.q if self.lost else self.a
        self.lost = self.rng.random() < chance
        return self.lost
```

The line for `a` comes from the long-run balance. The loss rate must equal `a × (1 − p) + q × p`, and solving for `a` gives `p(1 − q) / (1 − p)`. For `p = 0.01` and `q = 0.5` it is 0.505%, a number you will meet again in netem's syntax.

### Move it yourself

Open `examples/w14-burst-hunt.html`. The top view is one minute of snapshots, 1,800 cells in a grid of 30 per row (one row per second). Lost packets are dark, and bursts of `k` or more are outlined in red. Press "New minute" a few times on "Independent 1%" and you will almost never see red. Switch to "Bursty 1%" and red appears in nearly every minute, while the count of dark cells stays about the same. The bottom view plots the chance of having found the bug against test minutes, on a log time axis, with one curve per profile and the 95% line drawn across. The independent 1% curve crawls off the right edge of the chart. Move the `k` slider from 3 to 2 and watch every curve jump left, and to 4 and watch the independent ones vanish.

### Same idea elsewhere

Every conditioner is a way of setting `p`, `q`, a direction and a delay. Rewrite each in that form and you know what it tests.

**Unreal Engine 5 network emulation (Epic documentation, UE 5.8).** `PktLoss` is a percentage chance of discarding an outbound packet, and `PktIncomingLoss` does the same for inbound packets. Each packet is judged on its own, so `q = p`. The recommended 10% sits in the third row of the table, a stress test. Because the directions are separate settings, you can starve the server of inputs (outbound on the client) without touching snapshots, which tests prediction and reconciliation (weeks 8 and 9) separately from interpolation (week 10).

**Unity Transport 2.4 simulator.** `packetDropPercentage` sets `p`, `packetDelayMs` and `packetJitterMs` set the delay, and a `mode` applies it to sending, receiving or both. The manual suggests 20 ms of delay for a good connection up to 200 ms for a poor mobile one, jitter at about half the delay, and drop rarely above 3%. That is the second row, a realism test. It answers whether the game feels right on a bad day, not whether every branch works.

**netem (Linux, tc-netem(8)).** `loss random 1%` is independent, `q = p`. `loss gemodel` is the Gilbert-Elliott model itself, with four numbers: the chance of entering the bad state, the chance of leaving it, and the loss rates in each state. With loss 100% in the bad state and 0% in the good one, entering is our `a` and leaving is `1 − q`. So the bursty 1% profile is

```
sudo tc qdisc add dev lo root netem delay 30ms loss gemodel 0.505% 50% 100% 0%
sudo tc qdisc del dev lo root          # always remove it afterwards
```

netem acts on packets going *out* of the interface. On the loopback interface `lo`, both the request and the reply go out through it, so each suffers the delay and loss once, and a ping sees `2 × 30 = 60` ms more round trip and a round-trip loss of about 2%.

**clumsy 0.3 (Windows, jagt/clumsy, October 2023).** clumsy's Drop module drops each matched packet independently with a set chance, default 10%, and both its Inbound and Outbound boxes are ticked by default. So the defaults are `p = 0.1` in each direction and `q = p`, and a ping through them loses `1 − 0.9² = 19%` of its round trips. Its Lag module holds every packet for the same fixed time, with no jitter, so lag alone never reorders. Reordering is a separate "Out of order" module. clumsy chooses packets with a WinDivert filter such as `udp and outbound`, so it can leave your browser alone.

**Source engine (Valve documentation, archived 2023).** Valve demonstrated its own lag compensation on a listen server with 200 ms of artificial lag from `net_fakelag`. In our form that is delay only, `p = 0`. It tests hit registration under latency, which is week 11's question, and says nothing about bursts.

Five tools, one form. Before you run any of them, write down `p`, `q`, the direction, the delay and the jitter, and use the table to say which bugs the run can find.

### Design judgment

- **Run two kinds of test and label them.** A stress profile (high loss, long bursts, big delay) exists to execute every branch within minutes. A realism profile (built from measurements like week 2's) exists to judge feel and tune buffers. Mixing them up gives you either false confidence or a game tuned for a network nobody has.
- **Size a test by its target event, not by the clock.** "We ran it for an hour" means nothing without `λ`. Decide which rare event you need to see (`k` losses, a reorder, a duplicate after a disconnect), compute `t95`, and run at least that long, or raise `p` and `q` until `t95` fits your time.
- **Always include bursty loss.** Real loss comes in bursts (week 2). A conditioner with only independent loss makes the most common real failure the rarest test event.
- **Test each direction on its own.** Lost inputs and lost snapshots break different systems. A symmetric setting hides which one failed.
- **Seed everything and log the settings.** A bug that appears once in 28 hours is useless unless you can replay it. In-game and proxy conditioners should take a seed, and every bug report should carry the profile and seed that produced it.

### Check this example

1. At 60 Hz with independent 2% loss, how many bursts of three or more should you expect per minute, and how long until you have a 95% chance of seeing one?
2. A reliability layer (week 6) resends an important message in each of the next four packets, so it fails only if five packets in a row are lost. With bursty loss `p = 0.02`, `q = 0.6`, at 20 Hz, how often does that happen per hour?
3. Your test budget is 5 minutes at 30 Hz, and you want a 95% chance of seeing a burst of three. With `q = 0.5`, what average loss rate `p` do you need?

<details>
<summary>Answers</summary>

1. `β = 0.02 × 0.98 × 0.02² = 7.84 × 10⁻⁶`. Per minute `3,600 × 7.84 × 10⁻⁶ = 0.0282`. `t95 = 3.0 / 0.0282 = 106` minutes.
2. `β = 0.02 × 0.4 × 0.6⁴ = 0.001037`. Per hour `72,000 × 0.001037 = 74.6`. About 75 failures an hour, so four resends are not enough for bursty links.
3. You need `λ ≥ 3.0 / 5 = 0.6` per minute, so `β ≥ 0.6 / 1,800 = 3.33 × 10⁻⁴`. With `q = 0.5`, `β = p × 0.5 × 0.25 = 0.125 p`, so `p ≥ 0.27%`.

</details>

## 3. What your conditioner does that you did not ask for

Conditioners have side effects. You need to know them, or you will chase bugs the tool created.

### Jitter reorders packets

netem's `delay 100ms 20ms` gives each packet its own delay, drawn uniformly from 80 to 120 ms unless you name another distribution (the kernel's default is uniform). Its internal queue releases packets in order of their release time, not their send time, so a packet with a short delay can overtake one sent earlier. The manual warns that packets get reordered if jitter is large enough.

How often? Let the jitter be `±j`, so delays spread over a width `W = 2j`, and let packets leave `Δ = 1000 / r` ms apart. Packet `i + 1` overtakes packet `i` when packet `i`'s delay exceeds packet `i + 1`'s by more than `Δ`. For two independent uniform delays, that probability is

```
P(pair reordered) = (W − Δ)² / (2 W²)     if Δ < W
                  = 0                      if Δ ≥ W
```

| Send rate | `Δ` (ms) | `±10` ms (`W = 20`) | `±20` ms (`W = 40`) | `±40` ms (`W = 80`) |
|---|---|---|---|---|
| 20 Hz | 50 | 0 | 0 | 7.0% |
| 30 Hz | 33.3 | 0 | 1.4% | 17.0% |
| 60 Hz | 16.7 | 1.4% | 17.0% | 31.3% |
| 128 Hz | 7.8 | 18.6% | 32.4% | 40.7% |

Check one cell. At 60 Hz with `±20` ms, `(40 − 16.7)² / (2 × 1,600) = 543 / 3,200 = 17.0%`. A 200,000-pair simulation gives 17.05%.

The same netem line tests reordering heavily for a 60 Hz game and not at all for a 20 Hz one. Real connections reorder far less than 17% of packets, so a jittered netem profile at high send rates is a reordering stress test whether you meant it or not. If you want delay variation without reordering, the manual shows how to replace netem's internal queue with a plain FIFO. If you want reordering on purpose, clumsy's Out of order module and netem's `reorder` option do it explicitly.

### Direction doubles things

A setting on "both directions" applies twice to a round trip. clumsy's default 10% drop becomes 19% round-trip loss. netem on `lo` delays both legs. Unreal separates outbound and incoming. When you compare a measured ping with the setting, write down which directions the setting touches, or the numbers will not match and you will blame the game.

### The conditioner is a program too

clumsy's lag module keeps delayed packets in a buffer, and its source code caps that buffer at 2,000 packets and flushes 800 at once when it fills. A game sends far fewer packets than that, but a large file download on the same machine during a test can hit the cap and release a burst the network never produced. Filter the conditioner to your game's traffic and close other network programs while you test.

## 4. A test matrix you can run every night

A single "bad network" test is a guess. A **test matrix** runs a fixed set of profiles, each with several seeds, against automated checks, and reports which combination failed.

### Profiles

Build profiles from measurements (week 2) for realism and from the model (section 2) for stress. A starting set for this course:

| Profile | Delay one way | Jitter | Loss `p` | Burst `q` | Direction | Purpose |
|---|---|---|---|---|---|---|
| LAN | 1 ms | 0 | 0 | — | Both | Baseline. Anything failing here is not a network bug |
| Good broadband | 20 ms | ±3 ms | 0.1% | 0.1 | Both | Realism |
| Evening Wi-Fi | 30 ms | ±15 ms | 1% | 0.5 | Both | Realism, bursty |
| Mobile | 60 ms | ±30 ms | 3% | 0.5 | Both | Realism, poor case |
| Stress, snapshots | 250 ms | ±50 ms | 10% | 0.5 | Server to client | Execute interpolation and extrapolation branches |
| Stress, inputs | 250 ms | ±50 ms | 10% | 0.5 | Client to server | Execute prediction, reconciliation and input redundancy |

### Checks

A test needs a pass/fail rule a program can apply. Four kinds work for netcode.

- **Invariants.** Things that must always hold. An entity never moves farther in one frame than its maximum speed allows (plus a tolerance). Nothing ever appears at the world origin. Sequence numbers delivered to game code never go backwards.
- **Convergence.** After the network recovers, client and server agree within a tolerance within a time limit, for example 500 ms after the last lost packet.
- **Budgets.** Correction distance per reconciliation stays under a threshold. Bandwidth stays under week 13's per-client ceiling.
- **Crashes and disconnects.** The trivial check that catches the most bugs.

### Seeds and replay

Each run gets a seed that controls every random choice the conditioner makes. When a run fails, the report names the profile, the seed and the time of the first violation, and one command replays exactly that run. This is CS102 week 14's advice about testing random systems, applied to packets. Here is Lab 14's `run_matrix.py` on its toy client, before any bugs are fixed:

```
profile            seeds fails  first failure (s)  replay
lan                   10     0                  -
good_broadband        10     1               47.0  python run_matrix.py --repro good_broadband 4
evening_wifi          10    10                1.9  python run_matrix.py --repro evening_wifi 7
mobile                10    10                0.1  python run_matrix.py --repro mobile 1
stress_snapshots      10    10                0.3  python run_matrix.py --repro stress_snapshots 6
```

The stress row fails in every seed within a second, which is its job. Evening Wi-Fi fails in every seed too, as section 2 predicts. Bursty 1% loss gives 2.25 bursts of three per minute, so a 60-second run catches one 89% of the time. The row to read carefully is good broadband. It failed in one seed of ten, at 47 seconds, when 0.1% loss happened to produce a burst of three. A team that ran one seed of that profile and saw it pass would have shipped the bug. Mobile fails at 0.1 seconds for a different reason. Its ±30 ms jitter reorders about 10% of pairs at 30 Hz, and the client has a second bug that only reordering exposes. Evening Wi-Fi's ±15 ms can never reorder 30 Hz packets, which you can check with section 3's formula.

## In-class activity (25 minutes)

Groups of three. Each group gets a card describing one netcode feature and the bug it might hide: an input-redundancy scheme that sends the last 3 inputs in each packet, a reliable-message layer that resends every 100 ms, an interpolation buffer of 2 intervals at 60 Hz, or a reconnect flow that expects the server's "welcome" message before any snapshot.

1. Name the network event that triggers the rare branch (a burst of `k`, a reorder, a duplicate, a delay above some value). Give `k` or the threshold.
2. For the Evening Wi-Fi profile, compute how often the event happens per minute and `t95`.
3. Design a stress profile that makes `t95` under 60 seconds. Write it as a netem command and as clumsy settings. Say which direction it applies to.
4. Write one invariant a program can check that fails if the branch is broken.

Expected output: a card with the event, the two `t95` values, the netem line, the clumsy settings and the invariant. Groups swap cards and check one computation.

## Common misconceptions

- **"We tested at 5% loss and it was fine."** Fine for what event, for how long? At 30 Hz, a 5% independent test finds a three-packet burst about every 5 minutes and a five-packet burst about once every 31 hours of test time. The setting alone says nothing.
- **"Harsher settings are more realistic."** They are less realistic and more useful for a different job. Stress tests find broken branches. Realism tests judge feel. Label which one you are running.
- **"Loss is loss."** 1% bursty and 1% independent loss produce similar packet counts and very different games. Always set `q`, or at least know what your tool assumes.
- **"The conditioner only adds what I set."** Jitter adds reordering, both-direction settings double round-trip loss, and buffers inside the tool can release bursts. Measure the tool before you trust it, with week 2's ping.

## Check yourself

1. A game sends at 20 Hz and uses netem with `delay 50ms 30ms`. What fraction of consecutive pairs arrive out of order? What if the game sends at 60 Hz?
2. clumsy is set to Drop 5% with both boxes ticked. What round-trip loss does Lab 02's ping measure? What loss rate does the server see on client inputs?
3. Write the netem `gemodel` settings for an average loss of 2% with a mean burst of 4 packets.
4. At 30 Hz, a bug needs a burst of 2. How long, for a 95% chance, under independent 1% loss? Under bursty 1% with `q = 0.5`?
5. A colleague says the nightly matrix is too slow and proposes dropping the seeds from 10 per profile to 1. Using the good broadband row of the example output, what is the chance a single seed would have caught that bug?

<details>
<summary>Answers</summary>

1. `W = 60` ms. At 20 Hz, `Δ = 50`, so `(60 − 50)² / (2 × 3,600) = 100 / 7,200 = 1.4%`. At 60 Hz, `Δ = 16.7`, so `43.3² / 7,200 = 1,878 / 7,200 = 26.1%`.
2. Round trip `1 − 0.95² = 9.75%`. Inputs cross the conditioner once, so the server sees 5%.
3. Mean burst 4 means `1 − q = 0.25`, so `q = 0.75` and the chance of leaving the bad state is 25%. Entering is `a = 0.02 × 0.25 / 0.98 = 0.51%`. So `loss gemodel 0.51% 25% 100% 0%`.
4. Independent: `β = 0.01 × 0.99 × 0.01 = 9.9 × 10⁻⁵`, `λ = 1,800 × 9.9 × 10⁻⁵ = 0.178` per minute, `t95 = 16.8` minutes. Bursty: `β = 0.01 × 0.5 × 0.5 = 0.0025`, `λ = 4.5`, `t95 = 0.67` minutes, about 40 seconds.
5. One of ten seeds failed, so one seed catches it about 10% of the time. The model agrees: `β = 0.001 × 0.9 × 0.1² = 9 × 10⁻⁶`, `λ = 1,800 × 9 × 10⁻⁶ = 0.0162` per minute, and `1 − e^(−0.0162) = 1.6%` per 60-second run, so the matrix was a little lucky. Either way, nine nights in ten or more, the bug would pass unnoticed.

</details>

## Lab / assignment hook

[Lab 14, break it on purpose](../labs/lab14.md). You implement the Gilbert-Elliott dropper and burst statistics, check the section 2 formula with seeded runs, then run a test matrix against a toy interpolation client with two planted bugs. You find both, replay each from its seed, fix them, and show the matrix passing. The last part measures a real conditioner (netem on Linux, clumsy on Windows, or the lab's own proxy on macOS) with Lab 02's ping and compares it with the model.

## Sources

- Epic Games, "Using Network Emulation in Unreal Engine" (Unreal Engine 5.8 documentation, accessed September 2026). Settings `PktLoss` (outbound), `PktIncomingLoss` (inbound), `PktLag`, `PktLagVariance`, `PktOrder`, `PktDup`. The advice to test locally with harsh conditions such as a 500 ms round trip and 10% loss or higher.
- Unity Technologies, Unity Transport 2.4 manual, "Using pipelines" (accessed September 2026). `SimulatorPipelineStage` with `packetDelayMs`, `packetJitterMs`, `packetDropPercentage` and `mode`. Suggested delays from 20 ms to 200 ms, jitter about half the delay, drop rarely above 3%. Meant for testing.
- Linux manual page `tc-netem(8)` (man7.org, accessed September 2026). Delay with jitter as `±`, distributions, `loss random`, `loss gemodel` parameters, `duplicate`, `reorder`, reordering from jitter through the internal tfifo queue and the pfifo workaround, impairment applied to outgoing packets.
- Linux kernel source, `net/sched/sch_netem.c`, function `tabledist` (torvalds/linux, master, September 2026). Uniform jitter when no distribution table is set.
- jagt, clumsy (GitHub, release 0.3, 21 October 2023, MIT licence). Modules Lag, Drop, Throttle, Duplicate, Out of order, Tamper, Reset and Bandwidth (`src/main.c`). Drop chance default 10% with inbound and outbound on by default (`src/drop.c`). Fixed lag with no jitter, a 2,000-packet buffer and an 800-packet flush (`src/lag.c`, `KEEP_AT_MOST` and `FLUSH_WHEN_FULL`, checked on the 0.3 tag). WinDivert filters and localhost support (README and manual).
- Valve Developer Community, "Source Multiplayer Networking" (archived copy, December 2023). The lag compensation screenshot taken on a listen server with 200 ms of lag from `net_fakelag`.
- Gilbert, E. N. (1960). "Capacity of a burst-noise channel." *Bell System Technical Journal* 39(5), 1253-1265, doi:10.1002/j.1538-7305.1960.tb03959.x. Elliott, E. O. (1963). "Estimates of error rates for codes on burst-noise channels." *Bell System Technical Journal* 42(5), 1977-1997, doi:10.1002/j.1538-7305.1963.tb00955.x. The two-state burst-loss model.

## Interactive spec: examples/w14-burst-hunt.html

**Insight the visual must make obvious:** the chance of hitting a bug that needs `k` consecutive losses depends on burstiness far more than on the loss rate. Bursty 1% loss finds a three-packet bug in about a minute, while independent 1% loss would need more than a day, even though both lose the same number of packets.

**Layout.** Two linked views and a number panel. Desktop: views stacked on the left, panel on the right. Under 700 px: stacked, panel last.

1. **One-minute strip (top).** `60 × r` cells (default 1,800), in rows of `r` cells, one row per second. Delivered cells light, lost cells dark. Any run of `k` or more consecutive losses gets a red outline and a small count label. Caption above, for example "This minute: 18 lost, 2 bursts of ≥ 3" (seed 14, first minute: bursts of 3 and 4). Button "New minute" advances the seeded generator. Cells must scale down to fit 390 px width without horizontal scroll (cell size `floor(width / r)`).
2. **Detection curves (bottom).** x axis: test minutes on a log scale from 0.1 to 10,000. y axis: probability the bug has been triggered, 0 to 1. One curve `1 − exp(−λ t)` per preset profile (the five rows of the lecture table), in muted colors, plus the current settings in the accent color. Horizontal dashed line at 0.95. Each curve's `t95` marked with a dot and label. A vertical marker at "10-minute playtest".
3. **Number panel.** `p`, `q`, mean burst `1 / (1 − q)`, `a = p(1 − q)/(1 − p)`, `β`, `λ` per minute, mean wait, `t95`, P(found in 10 min), and the equivalent netem line, `loss gemodel {a%} {(1 − q)%} 100% 0%`, or `loss random {p%}` when independent.

**Controls.**
- Preset buttons: Independent 1%, Independent 3%, Independent 10%, Bursty 1% (`q = 0.5`), Bursty 1% milder (`q = 0.3`).
- Slider `p`, 0.1% to 20%, log scale, default 1%.
- Toggle "Independent" (forces `q = p`) and slider `q`, 0 to 0.95, step 0.01, default 0.5.
- Slider `k`, 1 to 6, default 3.
- Slider `r`, 10 to 128 Hz, default 30.
- Seed field, default 14.
- All controls keyboard operable. With `prefers-reduced-motion`, "New minute" redraws without animation.

**Formulas.** `a = p(1 − q)/(1 − p)`; generator: state starts delivered; each packet lost with probability `q` if the previous was lost, else `a`; seeded PRNG (mulberry32 is fine). `β = p(1 − q) q^(k − 1)` (with `q = p` when independent). `λ = 60 r β`. Mean wait `1/λ`, `t95 = ln 20 / λ`, `P(t) = 1 − e^(−λ t)`. Display waits in s, min, h or days as appropriate.

**Test values** (assert on load, `r = 30`, `k = 3`).
- Independent 1%: `β = 9.9e-7`, `λ = 0.001782`/min, mean 561.2 min, `t95` 1,681 min (28.0 h), P(10 min) 0.0177.
- Independent 3%: `β = 2.619e-5`, `λ = 0.04714`, `t95` 63.55 min, P(10 min) 0.376.
- Independent 10%: `λ = 1.62`, `t95` 1.85 min.
- Bursty 1%, `q = 0.5`: `a = 0.005051`, `β = 0.00125`, `λ = 2.25`, mean 0.444 min, `t95` 1.33 min. netem line `loss gemodel 0.505% 50% 100% 0%`.
- Bursty 1%, `q = 0.3`: `β = 6.3e-4`, `λ = 1.134`, `t95` 2.64 min.
- `k = 2`, independent 1%: `λ = 0.178`, `t95` 16.8 min. `k = 2`, bursty 1% `q = 0.5`: `λ = 4.5`, `t95` 0.67 min.
- Generator check: over 1,000,000 packets with seed 14 and bursty 1%, the measured loss rate is within 0.01 ± 0.001 and the mean burst length within 2.0 ± 0.1.

**First screen:** the Bursty 1% preset, one minute drawn with its red bursts, the curves for all five presets, and a caption: "Same 1% loss. Bursty finds the bug in about a minute. Independent needs more than a day."
