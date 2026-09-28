# CS202 · Week 02 — Latency, jitter, loss: measure your own

**Why this matters:** "My ping is 40" is the most quoted number in online games and one of the least useful. What a player feels depends on the spread of delays, the losses, and the buffers the game adds on purpose to hide them. If you cannot measure those, you cannot tune a netcode, and you will argue about feel instead of numbers.

**You will be able to:**
- Break an action's end-to-end latency into propagation, serialization, queuing and game-side waits, and compute each from distance, packet size, bandwidth and tick rates.
- Compute RTT, mean, median, percentiles, standard deviation and RFC 3550 jitter from a log of your own pings.
- Size a jitter buffer from measured delays for a target late-packet rate, and state the latency it costs.
- Estimate how often loss bursts break a buffer, for independent and bursty loss.

**Before class:** Valve Developer Community, "Source Multiplayer Networking", the sections on basic networking and entity interpolation (about 10 minutes). Riot Games Technology blog, "Fixing the Internet for Real Time Applications: Part I" (2015). Reread your notes on percentiles from MA102 week 12.

**Prerequisites from earlier courses:** [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (mean, median, sample SD and the inclusive percentile rule, all used here on ping data). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one lost packet in `n`). [CS202 week 1](w01-networks-for-game-devs-tcp-vs-udp.md) (UDP sockets, send interval `Δ`, the UDP gap `2Δ`).

**Interactive:** [examples/w02-jitter-buffer.html](../examples/w02-jitter-buffer.html). Keep it open during section 3.

---

## 1. Four numbers that describe a connection

A connection between a player and a server is described by four numbers. Each one hurts a game in a different way.

- **Latency** is how long a packet takes to get from one end to the other. **One-way latency** is one direction. **Round-trip time (RTT)** is there and back, which is what "ping" reports. One-way latency is hard to measure because the two machines' clocks disagree (section 5). RTT needs only one clock.
- **Jitter** is how much latency varies from packet to packet. A connection that is always 40 ms is easy to play on. One that swings between 40 and 95 ms is not, even if its average is lower than a steady 60.
- **Packet loss** is the fraction of packets that never arrive. Over UDP a lost packet is simply a gap. Over TCP it is a stall, as week 1 showed.
- **Bandwidth** is how many bits per second the link can carry. It limits how *much* you can send, not how *fast* one packet arrives. A motorway with more lanes carries more cars. It does not make any single car's trip shorter.

Games need little bandwidth and are sensitive to the other three. Riot's network team made the contrast plain in 2015. A video service can buffer five seconds of video, so its packets could take a long detour and nobody would notice. A game cannot buffer the future, because it has not been played yet. This week is about what a game *can* buffer, and what that costs.

## 2. Where latency comes from

A packet's one-way latency is the sum of four delays.

```
latency = propagation + serialization + queuing + processing
```

- **Propagation** is distance divided by signal speed. Light in optical fiber travels at about 200,000 km per second, two thirds of its speed in vacuum. That is **1 ms per 200 km**, one way. Sydney and New York are about 16,000 km apart on the globe, so a fiber path between them can never be faster than 80 ms one way, whatever you pay. That is our own arithmetic from the 200 km per ms rule.
- **Serialization** is the time to push the bits onto the wire, `bits / link rate`. An 83-byte game packet on a 10 Mbit/s uplink takes `83 × 8 / 10,000,000 s = 0.066 ms`. A 1,500-byte packet on a 1 Mbit/s uplink takes 12 ms. It matters on slow links and for big packets.
- **Queuing** is time spent waiting in router buffers behind other traffic. It is near zero on an idle network and can reach tens or hundreds of milliseconds when someone in the house starts a large upload. Queuing is where most **jitter** comes from, because it changes packet by packet.
- **Processing** is time inside routers and network stacks, usually well under a millisecond per hop.

Real routes are not straight lines. Riot published a trace from a *League of Legends* player whose traffic between San Francisco and Portland went through Los Angeles, Denver and Seattle. They estimated a direct trip at 14 ms and measured the detour at 70 ms. Internet providers route traffic along the cheapest path, not the fastest. That is a propagation problem no amount of game code can fix. Week 3 looks at what companies do about it.

### The latency you feel is bigger than your ping

Ping measures the network. A player feels the network plus every wait the game adds. Take a Source-engine shooter on its documented defaults. The client sends commands about 30 times per second. The server simulates a tick every 15 ms and sends snapshots 20 times per second. The client draws other players 100 ms in the past. Assume 30 ms one way each direction (a 60 ms ping) and a 60 frames-per-second display. On average, how long after you press a key does *another* player see you move?

| Step | Average wait | Why |
|---|---|---|
| Your input waits for the next command packet | 16.7 ms | Half of the 33.3 ms send interval |
| Travels to the server | 30 ms | One way |
| Waits for the next server tick | 7.5 ms | Half of 15 ms |
| Waits for the next snapshot to the other player | 25 ms | Half of 50 ms |
| Travels to the other player | 30 ms | One way |
| Other player's interpolation delay | 100 ms | Default, on purpose |
| Waits for the next frame on screen | 8.3 ms | Half of 16.7 ms |
| **Total** | **217.5 ms** | With a 60 ms ping |

Only 60 of those 217.5 ms are the network. The biggest single item is a delay the game adds by choice. The rest of this course is about shrinking the other items (prediction, week 8), hiding them (interpolation, week 10) and being fair about them (lag compensation, week 11). This week is about the choice of the 100 ms, and it starts from measurements.

## 3. Worked example: sizing a jitter buffer from your own ping

### The hook

By default the Source engine shows you every other player 100 ms in the past. On a nearby server that is more than most players' entire ping. Valve's documentation gives the reason in one line. With 20 snapshots per second and a 100 ms delay, even if one snapshot is lost there are always two valid snapshots to draw between. A game that competes on responsiveness adds latency deliberately, and players rarely notice. Why is adding a delay better than drawing the newest data the moment it arrives, and how would you pick the number?

### The model

Packets are sent at a steady rate. Each one's travel time differs a little. Call the smallest travel time you observed the **base** delay, and each packet's extra delay above it `e_i`.

A **jitter buffer** holds every packet until a fixed time after it was sent, `base + B`, and only then hands it to the game. `B` is the **buffer depth**, in milliseconds above the base.

- A packet with `e_i ≤ B` arrives in time. The game sees it at exactly `base + B` after it was sent, so every packet appears evenly spaced, as if jitter did not exist.
- A packet with `e_i > B` arrives **late**. The game has already moved on, so for a real-time game a late packet is as good as lost.

```
late fraction   L(B) = (number of packets with e_i > B) / n
felt latency         = base + B              (for every packet, not just the slow ones)
choose          B    = the (1 − L_target) percentile of e
```

So the buffer converts jitter into a fixed extra delay. Deeper buffer, fewer late packets, and more delay on *every* packet. There is no setting that gives both. The percentile is the inclusive rule from MA102 week 12.

For a round-trip log, `e_i = RTT_i − min RTT`. For one-way logs you need `send_i` and `arrive_i` from two different clocks. Their offset is unknown, but it is the same for every packet, so it cancels when you subtract the minimum. If the sender's clock runs 960 ms ahead, raw values of `arrive − send` come out as `−920, −918, −919, ...`. Subtract the smallest and you get the same `e_i` as with perfect clocks. You never need the true one-way latency to size a buffer. You need only the spread.

### Numbers you can check

Twenty pings at 20 Hz on a home connection. The smallest RTT was 40 ms. Here are the extra delays `e_i` in send order, in milliseconds:

```
0  2  1  3  0  5  1  18  2  0  1  4  2  55  1  0  3  16  2  1
```

Sorted:

```
0 0 0 0 1 1 1 1 1 2 2 2 2 3 3 4 5 16 18 55
```

The usual summaries, using MA102's formulas:

| Statistic | Value | How |
|---|---|---|
| Mean of `e` | 5.85 ms | 117 / 20 |
| Median | 2 ms | Average of the 10th and 11th values, (2 + 2) / 2 |
| Sample SD | 12.57 ms | `sqrt(Σ(e − 5.85)² / 19)` |
| 90th percentile | 16.2 ms | `h = 19 × 0.9 + 1 = 18.1`, between 16 and 18 |
| 95th percentile | 19.85 ms | `h = 19.05`, between 18 and 55 |
| RFC 3550 jitter | 8.18 ms | Smoothed average of changes, below |
| Mean RTT | 45.85 ms | 40 + 5.85. This is "your ping" |

Now try buffer depths. The felt one-way latency assumes a base of 20 ms (half of the 40 ms minimum RTT, a good enough estimate when both directions are similar).

| Buffer `B` | Late packets | Late fraction | Felt one-way latency |
|---|---|---|---|
| 0 ms | 16 of 20 | 80% | 20 ms |
| 3 ms | 5 | 25% | 23 ms |
| 5 ms | 3 | 15% | 25 ms |
| 16 ms | 2 | 10% | 36 ms |
| 18 ms | 1 | 5% | 38 ms |
| 55 ms | 0 | 0% | 75 ms |

Three things stand out.

- **Drawing packets the moment they arrive (`B = 0`) is not an option.** Four out of five packets would be "late" relative to the fastest one. Without a buffer, motion stutters every time the delay changes.
- **The mean and SD describe the spike, not the connection.** A tempting rule is "buffer = mean + 2 SD" = 31 ms. It happens to land between 18 and 55 here, but for the wrong reason. Most of the SD comes from one 55 ms packet. Drop that packet and the SD falls to 5.04 ms. A buffer rule should come from the percentile of lateness you accept, and nothing else.
- **The last few percent are expensive.** Going from 10% late to 5% late costs 2 ms. Going from 5% to 0% costs 37 ms, for one packet in twenty. Buffers that try to catch every spike make the whole game feel slow.

### The RFC 3550 jitter number

Voice and video over the internet use a standard running estimate of jitter, defined in RFC 3550, the RTP specification. For each new packet, take `D`, the change in delay from the previous packet, and nudge the estimate one sixteenth of the way toward `|D|`:

```
J = J + (|D| − J) / 16          starting from J = 0
```

Over our 20 packets, `J` ends at 8.18 ms. It is a smoothed "how much does delay change between neighbours" number. It reacts to spikes gradually, which makes it a good live readout for a network graph. It is not a buffer size. Use percentiles for that.

### Move it yourself

Open `examples/w02-jitter-buffer.html`. The top view is a timeline. Packets leave the sender evenly spaced, and each lands on the receiver's line at its own delay. The horizontal line is the playout deadline `base + B`. Packets that land after it turn red. The bottom view shows the same packets as a sorted bar chart of `e_i` with the buffer line across it, and the late fraction written next to it. Drag `B` from 0 up to 55. In the timeline the red packets vanish one by one. In the bar chart you can see why the last one is so expensive. Then switch the dataset to "Bursty evening" and watch the percentile you need move.

### Same idea elsewhere

**Source engine (Valve documentation, archived 2024).** The interpolation delay is set by `interpolation period = max(cl_interp, cl_interp_ratio / cl_updaterate)`. With the default snapshot rate of 20 per second and a ratio of 2, that is `2 / 20 s = 100 ms`. In our model, the buffer is sized in *snapshot intervals*, not in percentiles. A depth of two intervals means one whole snapshot can be late or lost and the client still has data. It is the same trade. Valve pays 100 ms on every player's view to buy robustness against one missing packet.

**Voice chat (RTP, RFC 3550).** Every voice-over-IP system holds incoming audio in a jitter buffer, because audio played the moment it arrives crackles whenever delay changes. RFC 3550's `J` exists so each side can report jitter to the other and tune that buffer. Late audio is dropped, exactly like our late packets.

**Age of Empires (1997 onward, Bettner and Terrano, 2001).** Ensemble Studios scheduled each player's commands to run two "communications turns" in the future, so the messages had time to reach every machine before they were needed. That is a jitter buffer for commands. They also measured how much buffer players tolerate. In their tests, 250 ms of command delay was not noticed in an RTS, 250 to 500 ms was very playable, and beyond 500 ms players began to notice. A slower genre can afford a deeper buffer.

**Video streaming.** Riot's example of a five-second video buffer is the same model with `B` set very large. With `B = 5,000 ms`, practically nothing is ever late. The price, five seconds of delay, is fine for a film and impossible for a game.

Four systems, one decision. Pick `B`. Everything later than `B` is lost to the player, and everything else is delayed by exactly `B`.

### Design judgment

- **Choose the late target first, then read `B` off the data.** "At most 1% of snapshots late" is a design decision. The buffer depth follows from it and from the player's connection, and it will differ from player to player.
- **Adapt, carefully.** A fixed `B` is wrong for someone on fiber and for someone on a crowded café network. Most modern netcode grows the buffer quickly when lateness rises and shrinks it slowly when things calm down. Changing `B` makes time run slightly fast or slow on screen, so do it gradually.
- **Sample over the right window.** A percentile from 20 packets is a sketch. From 30 seconds at 20 Hz you have 600 packets, and a 1% target means about 6 late ones. Percentiles need enough data to be meaningful, and the network at 9 p.m. is not the network at 9 a.m.
- **Do not buffer your own actions.** A buffer is for other players' state, which is always somewhat in the past anyway. Your own inputs should feel instant, which is the job of client-side prediction (week 8).
- **Late equals lost, so count them together.** A connection with 1% true loss and 4% late packets behaves like 5% loss to the game.

### Check this example

1. With the same 20 samples, a designer sets a target of "no more than 10% late". What `B` does the table give, and what is the felt one-way latency?
2. Suppose the 55 ms spike had been 200 ms. Which rows of the buffer table change, and how much do the mean and median change?
3. A game sends snapshots at 30 per second and uses Source's rule with `cl_interp_ratio = 2`. What interpolation delay results, and how many lost snapshots in a row can it survive?

<details>
<summary>Answers</summary>

1. `B = 16 ms` gives 2 of 20 late, 10%. Felt one-way latency `20 + 16 = 36 ms`.
2. Only the last row changes, from `B = 55` to `B = 200` for zero late packets, with felt latency 220 ms. Rows up to `B = 18` are unchanged. The mean rises from 5.85 to `(117 − 55 + 200) / 20 = 13.1` ms. The median stays at 2 ms.
3. `2 / 30 s = 66.7 ms`. It holds two intervals, so it can survive one lost snapshot, the same as Source at 20 per second, with 33 ms less delay.

</details>

## 4. Packet loss: independent and bursty

### Independent loss

The simplest model says each packet is lost with probability `p`, independently of the others. At `p = 1%` and 20 packets per second:

- Expected losses per minute: `1,200 × 0.01 = 12`.
- Chance of at least one loss among 20 packets (one second): `1 − 0.99^20 = 18.2%`. Among 100 packets: `1 − 0.99^100 = 63.4%`. That is MA102 week 3's complement rule, and the same "one expected run gives about 63%" pattern.
- Chance that a given loss is followed by a second loss: `p = 1%`. So a 100 ms buffer at 20 Hz, which survives one lost snapshot, fails only about once in 100 losses.

A ping measures loss in both directions. If each direction loses 5%, an echo survives only if both trips do, so the round-trip loss is `1 − 0.95² = 9.75%`. When you run Lab 02's proxy at 5% loss per direction, expect about 10% of pings missing. That is the model, not a bug.

### Bursty loss

Real loss is rarely independent. A queue overflows for 80 ms, a Wi-Fi radio retrains, a microwave oven switches on, and several packets in a row disappear. A standard way to model this is the **Gilbert-Elliott model**, a two-state Markov chain. The link is either in a good state, where packets get through, or a bad state, where they are lost with high probability. The simplest version needs one number beyond the average loss rate.

```
q = P(packet i+1 is lost | packet i was lost)
mean burst length = 1 / (1 − q)
```

With independent loss, `q = p`, and bursts average barely more than 1 packet. With `q = 0.5`, bursts average 2 packets. The average loss rate can be the same 1% in both cases, but they are very different to a game.

| Loss pattern | Average loss | `q` | Mean burst | Chance a loss breaks a 2-interval buffer |
|---|---|---|---|---|
| Independent | 1% | 0.01 | 1.01 packets | 1% |
| Mildly bursty | 1% | 0.3 | 1.43 packets | 30% |
| Bursty | 1% | 0.5 | 2 packets | 50% |

A two-interval buffer breaks when two or more packets in a row are lost, which happens with probability `q` after the first loss. The same "1% loss" connection breaks Source-style interpolation once per hundred losses or once per two losses, depending only on burstiness. So report loss as a rate *and* a burst length. Lab 02 asks you to measure both.

## 5. Measure your own

`ping` in a terminal sends ICMP echo packets about once a second. Your game sends UDP packets 20 to 60 times a second, and routers do not always treat the two alike. To measure what your game will experience, send packets that look like your game's. Riot's 2015 post notes that when routers are overloaded, many start dropping UDP before TCP, so a TCP or ICMP test can look healthier than your game traffic will.

A game-style ping needs three things in every packet.

- A **sequence number**, so the receiver can detect loss (a missing number), reordering (a number lower than one already seen) and duplicates (a number seen twice).
- A **send timestamp**, so the reply's arrival time gives the RTT without keeping a table.
- A **size and rate** matching your game. Lab 02 uses 12 bytes of payload at 20 Hz.

The core of Lab 02's `udp_ping.py`, with a local socket standing in for the echo server so the block runs on its own:

```python
import socket, struct, time

FMT = "!Id"                                   # uint32 sequence, float64 send time (ms)
now_ms = lambda: time.perf_counter() * 1000
echo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
echo.bind(("127.0.0.1", 0))                   # stands in for Lab 02's echo server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server, rtt, seq = echo.getsockname(), {}, 0

sock.sendto(struct.pack(FMT, seq, now_ms()), server)
data, addr = echo.recvfrom(64)
echo.sendto(data, addr)                       # the echo server's whole job

data, _ = sock.recvfrom(64)
s, sent_ms = struct.unpack(FMT, data)
rtt[s] = now_ms() - sent_ms                   # one clock, so no offset problem
print(len(data), "bytes of payload, sequence", s)   # 12 bytes of payload, sequence 0
```

Then analyze the log as in section 3. Report the minimum, median and 95th percentile RTT, the RFC 3550 jitter, the loss rate, the longest loss burst and the count of reordered packets. Those numbers tell a netcode programmer more than any single "ping".

## In-class activity (25 minutes)

Groups of three. Each group gets one of three printed ping logs (60 pings each): "fiber, idle", "Wi-Fi, flatmate streaming" and "mobile hotspot".

1. Compute the minimum, median, 95th percentile and mean RTT. Mark the lost pings and find the longest burst.
2. Choose a late target for a third-person action game and size `B`. Compute the felt one-way latency.
3. Using the latency table from section 2 with your log's median as the network part, compute how long another player takes to see your move.
4. Report to the room. The instructor writes the three `B` values side by side.

Expected output: one card per group with the five statistics, the chosen target, `B`, the felt latency, and a one-line answer to this question. Should the game use one fixed buffer for all players?

## Common misconceptions

- **"Ping is latency."** Ping is round-trip network time. One-way latency is roughly half of it, if both directions are similar. The latency a player feels adds tick waits, send intervals, buffers and frames, often three or four times the ping.
- **"More bandwidth means lower ping."** Bandwidth shortens serialization for big packets. For small game packets it changes almost nothing. Distance, routing and queuing set the ping.
- **"Jitter is the standard deviation of ping."** SD is one way to describe spread, and a poor one when a few spikes dominate. Games care about the percentile of delay they must cover. RFC 3550's `J` is another, smoothed measure. Always say which you mean.
- **"1% loss is 1% loss."** The same average can hide single losses or long bursts, and bursts break buffers.

## Check yourself

1. A player is 3,000 km of fiber from the server. What is the minimum possible RTT? Their measured minimum RTT is 48 ms. How much of that is not propagation?
2. A game packet is 120 bytes on the wire. How long does it take to serialize on a 2 Mbit/s uplink? On a 100 Mbit/s one?
3. Using the 20 samples from section 3, what late fraction does `B = 4` give? What `B` would you need for at most 20% late?
4. Each direction of a connection loses 2% of packets independently. What fraction of pings get no reply? At 20 Hz, how many snapshots per minute should the client expect to lose?
5. A link has 2% average loss and `q = 0.6`. What is the mean burst length? How often does a loss break a two-interval interpolation buffer?

<details>
<summary>Answers</summary>

1. One way, `3,000 / 200 = 15 ms`, so the minimum RTT is 30 ms. That leaves `48 − 30 = 18 ms` for routing detours, queuing, serialization and processing.
2. `120 × 8 = 960` bits. At 2 Mbit/s, `960 / 2,000,000 s = 0.48 ms`. At 100 Mbit/s, `0.0096 ms`.
3. Values greater than 4 are 5, 16, 18 and 55, so 4 of 20 are late, 20%. `B = 4` meets a 20% target exactly. The inclusive 80th percentile is also 4 (`h = 16.2`, between 4 and 5, giving 4.2), so `B = 4` is the smallest observed value that works.
4. `1 − 0.98² = 3.96%` of pings. Snapshots only travel one way, so the client loses about `1,200 × 0.02 = 24` per minute.
5. `1 / (1 − 0.6) = 2.5` packets. After a loss, the next packet is also lost with probability 0.6, so 60% of losses break the buffer.

</details>

## Lab / assignment hook

[Lab 02, measure your own connection](../labs/lab02.md). You run a UDP echo server, a proxy that injects delay, jitter and loss, and a game-style ping. You then write the analysis that turns the log into the statistics of section 3 and sizes a buffer for three late targets. The last part runs against a classmate's machine or a real remote host.

## Sources

- Valve Developer Community, "Source Multiplayer Networking" (archived copy, 2024). Tick of 15 ms, command packets usually 30 per second, `cl_updaterate` default 20, interpolation period rule `max(cl_interp, cl_interp_ratio / cl_updaterate)` and the default of 100 ms that survives one lost snapshot.
- Valve Software, Source SDK 2013, `src/game/client/cdll_bounded_cvars.cpp` (GitHub, ValveSoftware/source-sdk-2013, accessed September 2026). `cl_interp_ratio` default 2.0.
- Riot Games Technology blog, "Fixing the Internet for Real Time Applications: Part I" (6 November 2015). San Francisco to Portland route through Los Angeles, Denver and Seattle, about 14 ms direct and 70 ms measured. Providers route by cost, not latency. Video can buffer seconds and games cannot. Routers under load may drop UDP before TCP.
- Wikipedia, "Optical fiber" (accessed September 2026). Refractive index around 1.44 to 1.45 and the rule of thumb of about 200,000 km/s in fiber.
- Schulzrinne, H., Casner, S., Frederick, R. & Jacobson, V. (2003). RFC 3550, *RTP: A Transport Protocol for Real-Time Applications*. Interarrival jitter estimator `J = J + (|D| − J) / 16`.
- Bettner, P. & Terrano, M. (2001). "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond." Gamasutra, 22 March 2001 (now Game Developer). Commands scheduled two communications turns ahead. 250 ms of command latency not noticed, 250 to 500 ms very playable, beyond 500 ms noticeable.
- Gilbert, E. N. (1960). "Capacity of a burst-noise channel." *Bell System Technical Journal* 39(5). Elliott, E. O. (1963). "Estimates of error rates for codes on burst-noise channels." *Bell System Technical Journal* 42(5). The two-state burst-loss model.
- Diez, D., Çetinkaya-Rundel, M. & Barr, C. (2019). *OpenIntro Statistics*, 4th ed., section 2.1, for the summary statistics (as used in MA102 week 12).

## Interactive spec: examples/w02-jitter-buffer.html

**Insight the visual must make obvious:** a jitter buffer turns uneven arrivals into evenly spaced ones by delaying every packet by the same `B`. Each increase in `B` rescues fewer late packets than the one before, and covering the last spike costs more latency than everything else together.

**Layout.** Two linked views and a number panel. On desktop, the views stack on the left and the panel sits on the right. Under 700 px wide, everything stacks, panel last.

1. **Timeline view.** Horizontal time axis. Top line "sent": packets as dots every `Δ = 50 ms`. Bottom line "arrived": each packet at `send_i + base + e_i`, with a thin line from its send dot. A dashed line for each packet's playout deadline `send_i + base + B` is drawn as a short tick on the arrived line. Packets arriving after their deadline are red and labelled "late". Packets on time are drawn a second time on a third line "played" at exactly `send_i + base + B`, evenly spaced, to show that the buffer removes the jitter. Base defaults to 20 ms (one way).
2. **Sorted bar view.** One bar per packet, heights `e_i`, sorted ascending. A horizontal line at `B`. Bars above it are red. Label on the line: "B = 18 ms, 1 of 20 late (5%)". Mark the median, the 95th percentile and the mean with small labelled ticks on the vertical axis.
3. **Number panel.** n, base, mean, median, sample SD, P90, P95, P99, RFC 3550 jitter (in send order), B, late count, late fraction, felt one-way latency (`base + B`), and "cost of the last packet": the difference between `B` for 0% late and `B` for the next lower late count.

**Controls.**
- Slider `B`, 0 to 120 ms, step 1, default 18. Keyboard arrows move 1 ms, Page Up and Page Down move 10.
- Buttons "Snap to target": 20%, 10%, 5%, 1%, 0%. Each sets `B` to the smallest observed `e_i` whose late fraction is at or below the target.
- Dataset selector: "Home connection" (default, the 20 values in the lecture), "Bursty evening" (below) and "Random" (generates 200 values with `e = U(0, 5)` plus, with probability 0.06, an extra `U(20, 80)`, from a seed field defaulting to 202).
- Toggle "Show mean + 2 SD" draws that line on the bar view, in a different color, so students see where it falls.

**Formulas.** Inclusive percentile: sort, `h = (n − 1)p`, interpolate between the values at `floor(h)` and `ceil(h)` (0-indexed). Sample SD with `n − 1`. RFC 3550: `J = 0`, then for `i ≥ 1`, `J += (|e_i − e_{i−1}| − J) / 16`. Late if `e_i > B`.

**Datasets.**
- Home connection: `0 2 1 3 0 5 1 18 2 0 1 4 2 55 1 0 3 16 2 1`.
- Bursty evening (20 values): `3 4 2 30 34 28 3 2 4 3 2 41 38 3 2 3 4 2 3 2`.

**Test values** (assert on load, Home connection): mean 5.85, median 2.00, SD 12.57, P90 16.20, P95 19.85, RFC 3550 J 8.18. Late counts: `B = 0` gives 16, `B = 3` gives 5, `B = 5` gives 3, `B = 16` gives 2, `B = 18` gives 1, `B = 55` gives 0. Mean + 2 SD = 30.98. Bursty evening: median 3.00, P90 34.40, P95 38.15, `B = 4` gives 5 late (25%).

**First screen:** Home connection with `B = 18`, one red packet (the 55 ms spike) in both views, and a caption: "One packet in twenty needs 37 ms more buffer. Is it worth it?"
