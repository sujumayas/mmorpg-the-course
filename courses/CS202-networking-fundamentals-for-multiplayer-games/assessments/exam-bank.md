# CS202 · Exam bank: quiz, practice and viva questions

CS202 has no written exam. The grade comes from the labs (40%, see [labs-brief.md](labs-brief.md)) and the final networked prototype (60%, see [final-prototype-brief.md](final-prototype-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers or traces code, and one asks you to explain or critique.
- **Viva.** The lab spot checks and the week 15 prototype viva ask questions in this style, rewritten with the numbers from your own measurements and your own code.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model (latency, bandwidth, tick rate, bit budgets, loss) to values you have not seen before.
- **code**: trace what a piece of Python prints or does.
- **explain**: say why something behaves as it does, with a number or a trace as evidence.
- **design**: choose a technique or setting for a stated situation and justify it.
- **critique**: find what is wrong with a piece of code or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`), using the lecture's definitions where the question says so, and every number was recomputed in Python. Write your own answer before you open the solution.

---

## Week 1: Networks for game devs, TCP vs UDP

1. *Week 1 · compute.* A game sends a 40-byte payload 64 times per second. How many bytes per second of headers does that cost over UDP/IPv4 and over TCP/IPv4 with minimum headers? What fraction of each packet is header?

<details>
<summary>Answer and worked solution</summary>

**Answer:** UDP 1,792 B/s (14.3 kbit/s), 41.2% header. TCP 2,560 B/s (20.5 kbit/s), 50.0% header.

UDP over IPv4 pays `20 + 8 = 28` bytes per packet, so `28 × 64 = 1,792` B/s. Each packet is `40 + 28 = 68` bytes, and `28 / 68 = 41.2%`. TCP pays at least `20 + 20 = 40` bytes, so `40 × 64 = 2,560` B/s, and each packet is 80 bytes, half of it header.

The lesson from the lecture's table holds. Small, frequent game messages spend a large share of their bytes on headers, so batching or packing matters more than it would for bulk traffic.
</details>

2. *Week 1 · compute.* Use the lecture's head-of-line model with one lost packet and `RTO = RTT + 200 ms` unless told otherwise.
   (a) 25 Hz, RTT 120 ms. Give the UDP gap, the TCP gap and which TCP path fires.
   (b) 4 Hz, RTT 60 ms. Same three answers.
   (c) Repeat (b) with the RFC 6298 minimum, `RTO = 1,000 ms`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) UDP 80 ms, TCP 280 ms, fast retransmit. (b) UDP 500 ms, TCP 510 ms, timeout. (c) UDP 500 ms, TCP 1,060 ms, fast retransmit.

(a) `Δ = 1000 / 25 = 40` ms. UDP gap `2Δ = 80`. Fast retransmit needs `3Δ + RTT = 240 ms`, less than `RTO = 320`, so it fires first and the gap is `4Δ + RTT = 160 + 120 = 280` ms.

(b) `Δ = 250` ms. Fast retransmit would need `3Δ + RTT = 810` ms, more than `RTO = 260`, so the timeout fires. Gap `Δ + RTO = 250 + 260 = 510` ms against UDP's 500. At a low send rate the transports cost nearly the same, because the send interval dominates both.

(c) Now `RTO = 1,000` and `810 < 1,000`, so fast retransmit wins after all. Gap `4Δ + RTT = 1,000 + 60 = 1,060` ms. Always compute both paths and take the earlier one.
</details>

3. *Week 1 · code.* This function parses a buffer that uses the lecture's 2-byte length prefix. What does the last line print, and what should the caller do with the second value it returns?

```python
import struct

def parse_frames(buf):
    msgs, pos = [], 0
    while pos + 2 <= len(buf):
        (n,) = struct.unpack_from("!H", buf, pos)
        if pos + 2 + n > len(buf):
            break
        msgs.append(bytes(buf[pos + 2: pos + 2 + n]))
        pos += 2 + n
    return msgs, bytes(buf[pos:])

print(parse_frames(b"\x00\x04MOVE\x00\x00\x00\x03GG!\x00\x05FI"))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `([b'MOVE', b'', b'GG!'], b'\x00\x05FI')`

`\x00\x04` is length 4, giving `MOVE`. `\x00\x00` is length 0, an empty message, which the loop handles correctly. `\x00\x03` gives `GG!`. Then `\x00\x05` says 5 bytes follow, but only 2 (`FI`) are present, so the loop stops.

The leftover bytes are the start of a message whose remaining 3 bytes have not arrived yet. TCP is a byte stream, so a message can be split across `recv()` calls. The caller must keep the leftover and prepend it to the next chunk it reads. Throwing it away would desynchronize every later message, because the next read would start in the middle of `FI...` and treat payload bytes as a length.
</details>

4. *Week 1 · critique.* A teammate writes in the design doc: "Our shooter uses TCP. We set `TCP_NODELAY`, so we have no head-of-line stalls, and if players complain we will raise the send rate from 20 to 60 Hz." Find the two mistakes and put a number on each at RTT 150 ms.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `TCP_NODELAY` turns off Nagle's batching, not in-order delivery, so a loss still stalls everything behind it. And a higher send rate shrinks only the `4Δ` part of the stall. At RTT 150 the stall goes from 350 ms to 216.7 ms, while UDP's gap goes from 100 ms to 33.3 ms.

At 20 Hz, `4 × 50 + 150 = 350` ms. At 60 Hz, `4 × 16.7 + 150 = 216.7` ms. Three times the packets buy a 38% shorter stall, and the 150 ms round-trip term never shrinks. Over UDP the same change takes the gap from `2 × 50 = 100` to `2 × 16.7 = 33.3` ms. The fix is to move state traffic to UDP and keep TCP (or a reliable channel) for messages that must arrive and can wait, as the lecture's section 5 table suggests.
</details>

## Week 2: Latency, jitter, loss

5. *Week 2 · compute.* Ten pings give these extra delays above the minimum RTT, in ms: `4 0 1 7 2 0 30 3 1 12`. Using the lecture's definitions, compute the mean, the median and the inclusive 90th percentile. Then choose the jitter buffer depth `B` for a target of at most 10% late packets, and for at most 20%, and give the felt one-way latency for each if the base one-way delay is 25 ms.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Mean 6.0 ms, median 2.5 ms, P90 13.8 ms. `B = 12` ms for 10% (felt latency 37 ms). `B = 7` ms for 20% (felt latency 32 ms).

Sorted: `0 0 1 1 2 3 4 7 12 30`. The sum is 60, so the mean is 6.0. The median is the average of the 5th and 6th values, `(2 + 3) / 2 = 2.5`. For P90, `h = (10 − 1) × 0.9 = 8.1` (0-indexed), between 12 and 30, so `12 + 0.1 × 18 = 13.8`.

A packet is late if `e > B`. With `B = 12`, only the 30 is late, 1 of 10, which meets 10%. With `B = 7`, the 12 and the 30 are late, 2 of 10, which meets 20%. Felt one-way latency is `base + B`, so 37 and 32 ms. Notice the P90 of 13.8 is not an observed value. The smallest observed `B` that meets the target is 12, and a buffer sized from observed values is what the lab's `buffer_for` returns.
</details>

6. *Week 2 · code.* This is the RFC 3550 jitter estimator from the lecture, applied to the extra delays from question 5. What does it print? Show the running value after each packet.

```python
def rfc3550(vals):
    J = 0.0
    for a, b in zip(vals, vals[1:]):
        J += (abs(b - a) - J) / 16
    return J

print(round(rfc3550([4, 0, 1, 7, 2]), 4))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `0.925`

The changes `|D|` are 4, 1, 6 and 5.

| After packet | `|D|` | `J` |
|---|---|---|
| 2 | 4 | `0 + (4 − 0) / 16 = 0.25` |
| 3 | 1 | `0.25 + (1 − 0.25) / 16 = 0.2969` |
| 4 | 6 | `0.2969 + (6 − 0.2969) / 16 = 0.6533` |
| 5 | 5 | `0.6533 + (5 − 0.6533) / 16 = 0.925` |

The estimate moves one sixteenth of the way toward each new change, so after four packets it is still far below the typical change of about 4 ms. That slowness is why the lecture says `J` is a live readout for a network graph, not a buffer size.
</details>

7. *Week 2 · compute.* (a) A player is 5,000 km of fiber from the server. What is the smallest possible RTT? How long does a 200-byte packet take to serialize on a 1 Mbit/s uplink? (b) A game samples commands at 60 Hz, ticks at 64 Hz, sends snapshots at 32 Hz, interpolates other players over two snapshot intervals, and renders at 144 fps. One-way latency is 40 ms each way. Using the lecture's key-to-screen table, how long on average until another player sees you move, and what share of it is the network?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 50 ms RTT, 1.6 ms serialization. (b) 177.7 ms, of which 80 ms (45%) is the network.

(a) One way, `5,000 / 200 = 25` ms, so the RTT is at least 50 ms. Serialization is `200 × 8 / 1,000,000 s = 1.6` ms.

(b) Each periodic wait averages half its interval.

| Step | Average |
|---|---|
| Wait for the command packet | `16.7 / 2 = 8.33` ms |
| Travel to the server | 40 ms |
| Wait for the server tick | `15.625 / 2 = 7.81` ms |
| Wait for the snapshot | `31.25 / 2 = 15.63` ms |
| Travel to the other player | 40 ms |
| Interpolation, two intervals | `2 × 31.25 = 62.5` ms |
| Wait for the frame | `6.94 / 2 = 3.47` ms |
| **Total** | **177.7 ms** |

Even at higher rates than Source's defaults, the interpolation delay is the single largest item.
</details>

8. *Week 2 · compute.* Each direction of a connection loses 3% of packets independently. (a) What fraction of pings get no reply? (b) At 30 snapshots per second, how many snapshots does the client lose per minute? (c) The same link is re-measured and turns out to be bursty, with `q = 0.4`. What is the mean burst length, and what fraction of losses break a two-interval interpolation buffer?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5.91%. (b) 54 per minute. (c) Mean burst 1.67 packets, and 40% of losses break the buffer.

(a) A ping survives only if both trips survive: `1 − 0.97² = 0.0591`.

(b) Snapshots cross once. `1,800 × 0.03 = 54`.

(c) Mean burst `1 / (1 − 0.4) = 1.67`. A two-interval buffer survives one lost snapshot and breaks when the next is lost too, which happens with probability `q = 0.4` after any loss. Under independent loss that chance would be only 3%. Report loss as a rate and a burst length.
</details>

## Week 3: Topologies

9. *Week 3 · compute.* Ten players, `r = 30` Hz, `s = 24` bytes of state per player, `i = 8` bytes per input, `h = 28`. Compute in kbit/s (a) a mesh peer's upload, (b) a server client's download and upload, (c) the dedicated server's upload and (d) a listen host's upload. (e) What is the largest `n` for which a listen host with a 4 Mbit/s uplink still fits?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 112.3 kbit/s. (b) Download 64.3 kbit/s, upload 8.6 kbit/s. (c) 643.2 kbit/s. (d) 578.9 kbit/s. (e) 26 players.

(a) `(n − 1) × r × (s + h) = 9 × 30 × 52 = 14,040` B/s.

(b) One snapshot is `n × s + h = 240 + 28 = 268` bytes, so download is `30 × 268 = 8,040` B/s. Upload `30 × (8 + 28) = 1,080` B/s.

(c) `n × 8,040 = 80,400` B/s.

(d) `(n − 1) × 8,040 = 72,360` B/s.

(e) The host needs `(n − 1) × 30 × (24n + 28) × 8 ≤ 4,000,000`. At `n = 26`, `25 × 30 × 652 × 8 = 3.91` Mbit/s, which fits. At `n = 27`, `26 × 30 × 676 × 8 = 4.22` Mbit/s, which does not. Solve it with a loop rather than by guessing, because the formula is quadratic in `n`.
</details>

10. *Week 3 · compute.* Three players P, Q and R have one-way direct latencies P-Q 20 ms, P-R 70 ms and Q-R 45 ms. A server S is 15 ms from P, 12 from Q and 30 from R. A relay network is 18 ms from P, 14 from Q and 16 from R. Find the worst pair for the mesh, the server, a listen host at each player, and the relayed mesh.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Mesh 70 ms, server 45 ms, host P 90 ms, host Q 65 ms, host R 115 ms, relay 34 ms.

| Pair | Mesh | Server | Host P | Host Q | Host R | Relay |
|---|---|---|---|---|---|---|
| P-Q | 20 | 27 | 20 | 20 | 115 | 32 |
| P-R | 70 | 45 | 70 | 65 | 70 | 34 |
| Q-R | 45 | 42 | 90 | 45 | 45 | 30 |
| **Worst** | **70** | **45** | **90** | **65** | **115** | **34** |

Two cells by hand. Q to R through host P is `20 + 70 = 90`. P to Q through host R is `70 + 45 = 115`. The P-R direct route is slow enough that every design that forces traffic along it loses. The relay avoids it entirely, which is the triangle inequality failing in the relay's favor, as in the lecture's section 3.
</details>

11. *Week 3 · design.* A studio is making a 6-player co-op roguelike with drop-in play, cosmetic-only purchases and no ranked mode. It has no budget for servers. Choose a topology, name the two risks the lecture says your choice carries, and give one mitigation for each.

<details>
<summary>Answer and worked solution</summary>

**A strong answer:** A listen server, ideally reached through a relay. At `n = 6` the host's upload is small (with `r = 20`, `s = 40`, `h = 28`, it is `5 × 20 × 268 = 26,800` B/s, about 214 kbit/s), and servers cost nothing.

Risks and mitigations from the lecture's design judgment:
- **The host leaves and the match ends.** Mitigate with host migration, or at least by saving the run state often so players can resume.
- **The host's machine is authoritative and can be modified.** In co-op with no ranked mode, cheating hurts only the cheater's own group, so this is acceptable. Keep purchases and account data on a separate trusted service.
- **Addresses leak and NAT blocks connections.** A relay hides IPs and removes the need for hole punching, because both players connect out.
- **Host advantage.** The host's actions reach the server in 0 ms. In co-op this matters little.

A weak answer picks dedicated servers "because they are better" without the cost, or picks a full mesh without computing that each peer now uploads `5 × r × (s + h)` and must reach every other peer through NAT.
</details>

## Week 4: Server authority

12. *Week 4 · compute.* Packets arrive every `Δ = 40` ms. Honest jitter is `J = 12` ms. Run speed is 7 m/s. (a) What tolerance does policy A need? (b) How fast can a cheater run, and how far ahead are they after 30 seconds? (c) Redo (b) for `J = 30` ms and say whether policy A is usable.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 42.9%. (b) 10.0 m/s and 90 m. (c) 300% tolerance, 28 m/s. Not usable.

(a) `tol_min = J / (Δ − J) = 12 / 28 = 0.429`.

(b) The cheater claims `(1 + tol)` times real speed on every packet: `7 × 1.429 = 10.0` m/s. Lead `v × tol × t = 7 × 0.429 × 30 = 90` m.

(c) `30 / 10 = 3.0`, so 300%, and `7 × 4 = 28` m/s. The tolerance explodes as `J` approaches `Δ`, and each point of it is a permanent speed gift. Switch to policy B.
</details>

13. *Week 4 · compute.* A server ticks at 30 Hz. Each packet carries 2 commands, and each command moves at most 0.2 m. Honest jitter is 45 ms. (a) What is `B_min` for policy B? (b) A lag-switcher holds 5 packets and releases them with the next one. How many commands run in one tick at `B = B_min`, how far does the cheater jump, and how many commands are dropped? (c) Same with `B = 30`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 4. (b) 4 commands run, a 0.8 m jump, 8 dropped. (c) All 12 run, a 2.4 m jump, none dropped.

(a) The tick is `1000 / 30 = 33.3` ms. A 45 ms delay misses `⌈45 / 33.3⌉ = 2` ticks, so `B_min = 2 + 2 = 4`.

(b) The burst is `5 × 2 + 2 = 12` commands. The credit caps it at 4, so the cheater moves `4 × 0.2 = 0.8` m and loses `12 − 4 = 8` commands of movement.

(c) With 30 credits saved up, all 12 commands run in one tick: `12 × 0.2 = 2.4` m. The larger budget forgives honest lag spikes and lets the lag switch teleport. That is the trade the lecture's Source example makes with `B = 24`.
</details>

14. *Week 4 · critique.* A prototype server handles two client messages like this. The client sends `fwd` and `side` as signed bytes and `count` and `price` as signed 16-bit integers. What does the last line print? List every check from the lecture's section 3 that is missing, and rewrite the sell message as intent.

```python
SPEED, TICK = 6.0, 1 / 60

def on_move(player, fwd, side):
    player["x"] += side * SPEED * TICK
    player["y"] += fwd * SPEED * TICK

def on_sell(player, item_id, count, price):
    player["gold"] += price * count
    player["items"][item_id] -= count

p = {"x": 0.0, "y": 0.0, "gold": 100, "items": {17: 2}}
on_move(p, 127, 127)
on_sell(p, 17, -5, 30)
print(p)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `{'x': 12.7, 'y': 12.7, 'gold': -50, 'items': {17: 7}}`

One move message carried the player 17.96 m in one tick, which is 1,078 m/s. One sell message turned 2 items into 7 and paid for it with negative gold.

Missing checks:
- **Range.** `fwd` and `side` must be −1, 0 or 1. `count` must be positive and at most what the player holds.
- **Normalization.** Even with legal values, `fwd = side = 1` moves `√2 × 0.1 = 0.141` m per tick, 41% faster than straight. Normalize the input vector on the server.
- **Rate.** Nothing stops 50 move messages per tick. Policy B's tick budget bounds that.
- **Trust.** The price comes from the client. The server must look it up.
- **Ownership.** The item id is never checked against the sender's inventory. A missing id raises `KeyError`, which should never crash a handler.
- **State and reach.** Is the player alive, and within reach of a vendor?

Rewrite as intent: `SELL vendor_id item_id count`. The server checks that the vendor exists and is within reach, that the item belongs to the sender, that `1 ≤ count ≤ held`, looks up the price itself, and only then changes gold and inventory.
</details>

15. *Week 4 · explain.* Two proposals to stop speed hacks come up in a meeting. "Encrypt the packets" and "check distance against the time the client says it sent each packet." Explain in two sentences each why neither works.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

Encryption protects traffic from third parties on the network. The player owns the client that encrypts, so a modified client encrypts whatever lie it wants to tell.

A speed hack works by running the client's clock fast. Its timestamps then say exactly enough time passed to cover the distance it claims, so the check passes. Only a clock the server keeps, its own tick count, cannot be sped up by the client.
</details>

## Week 5: Serialization and bit packing

16. *Week 5 · compute.* A world is 1,000 m × 1,000 m horizontally and 100 m tall. (a) At 2 cm precision, how many bits does a position take, and how many whole bytes if nothing else is in the packet? (b) Yaw is sent in 9 bits. What is the step, the largest error, and the sideways error at 40 m? (c) Compare with an 8-bit yaw at 40 m, against a 0.3 m hitbox radius.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 45 bits, 6 bytes. (b) Step 0.703°, largest error 0.352°, 0.245 m at 40 m. (c) 8 bits gives 0.49 m, wider than the hitbox radius.

(a) x and y: `1,000 / 0.02 + 1 = 50,001` values. `2^15 = 32,768` is too few and `2^16 = 65,536` is enough, so 16 bits each. z: `100 / 0.02 + 1 = 5,001` values, 13 bits (`2^13 = 8,192`). Total `16 + 16 + 13 = 45` bits, which rounds up to 6 bytes.

(b) Yaw wraps, so `count = 512` and the step is `360 / 512 = 0.703°`. The largest error is half a step, 0.352°. Sideways at 40 m: `40 × 0.352 × π / 180 = 0.245` m.

(c) 8 bits: step 1.406°, largest error 0.703°, `0.49` m at 40 m. That is bigger than a 0.3 m hitbox radius, so a shot along the received aim could miss a head it was pointed at. Fine for drawing another player's facing, never for hit detection.
</details>

17. *Week 5 · code.* Using the lecture's `BitWriter` (least significant bit first), what does this print? Then say what `w.write(8, 3)` would do.

```python
w = BitWriter()
w.write(3, 2)
w.write(0, 1)
w.write(45, 7)
w.write(1, 1)
print(w.buf.hex(), w.nbits)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `6b05 11`. `w.write(8, 3)` raises `ValueError: 8 does not fit in 3 bits`.

Write the bits in order, lowest bit of each value first.

| Value | Width | Bits written (low first) | Bit positions |
|---|---|---|---|
| 3 | 2 | `1 1` | 0, 1 |
| 0 | 1 | `0` | 2 |
| 45 = `0101101` | 7 | `1 0 1 1 0 1 0` | 3 to 9 |
| 1 | 1 | `1` | 10 |

Byte 0 holds positions 0 to 7: `1 1 0 1 0 1 1 0`. Reading from bit 7 down, that is `0110 1011 = 0x6b`. Byte 1 holds positions 8, 9 and 10: `1 0 1`, which is `0x05`. Eleven bits in two bytes.

The range check at the top of `write` is what stops a 3-bit field from silently corrupting its neighbour.
</details>

18. *Week 5 · compute.* (a) A 32-player server sends 30 snapshots per second with a 28-byte header. Compute its upload with the naive 44-byte state and with the packed 14-byte state, and the saving. (b) A team sends health (0 to 250) as a 32-bit integer on a 64-player server at 20 Hz. How many bits per second of waste is that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 11,028.5 kbit/s and 3,655.7 kbit/s, a 66.9% saving. (b) 1,966,080 bit/s, about 1.97 Mbit/s.

(a) `n × r × (n × s + h)`. At `s = 44`: `32 × 30 × (1,408 + 28) = 1,378,560` B/s, 11,028.5 kbit/s. At `s = 14`: `32 × 30 × (448 + 28) = 456,960` B/s, 3,655.7 kbit/s. Saving `1 − 476 / 1,436 = 66.9%`, a little under the 68% limit because the header is a bigger share at 32 players.

(b) 251 values need `⌈log2 251⌉ = 8` bits, so 24 bits are wasted per player per snapshot. Each snapshot carries 64 players to 64 clients 20 times a second: `24 × 64 × 64 × 20 = 1,966,080` bit/s.
</details>

19. *Week 5 · critique.* A server reads client packets like this. Name three problems and the fix for each.

```python
import pickle

def on_packet(data):
    msg = pickle.loads(data)
    count = msg["count"]
    players = [msg["players"][i] for i in range(count)]
    return players
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

- **`pickle` on untrusted bytes.** A crafted packet can make `pickle.loads` run code of the attacker's choosing. Use a fixed binary layout read with `struct` or a bit reader that can only produce the values you expect.
- **The count is trusted.** A packet that claims 40 players but holds 21 either raises an `IndexError` that can kill the handler, or, in a language without bounds checks, reads past the buffer. Check `count` against the bytes that remain before reading anything, and reject the packet if it does not fit.
- **No clean failure.** Any error escapes as whatever exception Python raises. Wrap parsing so every malformed packet raises your own `ReadError`, is dropped and counted, and never crashes the server. Then fuzz it with thousands of random byte strings, as Lab 05 does.
</details>

## Week 6: Reliability over UDP

20. *Week 6 · code.* Using the lecture's `seq_greater_than`, what does this print?

```python
def seq_greater_than(a, b):
    return (a > b and a - b <= 32768) or (a < b and b - a > 32768)

pairs = [(3, 65530), (65530, 3), (32768, 0), (0, 32768), (20000, 60000)]
print([seq_greater_than(a, b) for a, b in pairs])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `[True, False, True, False, True]`

- `(3, 65530)`: `a < b` and `b − a = 65,527 > 32,768`, so 3 has wrapped and is newer.
- `(65530, 3)`: `a > b` but `a − b = 65,527` is more than half the circle, so 65,530 is older.
- `(32768, 0)`: `a − b = 32,768`, which passes `<= 32768`. Exactly half a lap counts as newer.
- `(0, 32768)`: `b − a = 32,768` is not `> 32768`, so False. The two halves of the test agree that 32,768 is newer than 0 and not the reverse.
- `(20000, 60000)`: `b − a = 40,000 > 32,768`, so 20,000 is newer, from the next lap.
</details>

21. *Week 6 · compute.* A receiver has received packets 100, 102, 103, 105 and 106. Write `ack` and `ack_bits` (bits 0 to 5, in binary and decimal). Which packets between 100 and 106 does the sender learn were not received?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ack = 106`, `ack_bits = 0b101101 = 45`. Packets 101 and 104 were not received.

Bit `n` stands for packet `106 − 1 − n`.

| Bit | Packet | Received |
|---|---|---|
| 0 | 105 | 1 |
| 1 | 104 | 0 |
| 2 | 103 | 1 |
| 3 | 102 | 1 |
| 4 | 101 | 0 |
| 5 | 100 | 1 |

Reading from bit 5 down gives `101101`, which is `32 + 8 + 4 + 1 = 45`. The sender does not resend packets 101 and 104. It puts any reliable messages they carried into its next packet, with a new sequence number.
</details>

22. *Week 6 · compute.* A client sends 60 inputs per second in 60 packets per second. Loss is 2%. (a) For `k = 1, 2, 3` copies per input, how many inputs are lost per hour under independent loss, and what is the upload? (b) The link is actually bursty with `q = 0.5`. Redo the loss column and say what `k = 4` buys.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `k` | Independent, lost per hour | Bursty `q = 0.5`, lost per hour | Packet | Upload |
|---|---|---|---|---|
| 1 | 4,320 | 4,320 | 40 B | 19.2 kbit/s |
| 2 | 86.4 | 2,160 | 44 B | 21.1 kbit/s |
| 3 | 1.7 | 1,080 | 48 B | 23.0 kbit/s |

An hour is `60 × 3,600 = 216,000` inputs. Independent: `216,000 × 0.02^k`. Bursty: `216,000 × 0.02 × 0.5^(k − 1)`. Packet size `28 + 8 + 4k`, times 60 packets and 8 bits.

On the bursty link `k = 4` still loses 540 inputs an hour. Each copy only halves the losses, because consecutive copies share the same burst. Spacing the copies out (packets `i`, `i + 2`, `i + 4`) or adding ack-and-resend does more than a fourth copy.
</details>

23. *Week 6 · design.* A designer puts chat, inventory changes and quest updates on one reliable ordered channel "to keep it simple." Loss hits one chat message at RTT 140 ms and a 30 Hz packet rate. How long, at least, are inventory updates held up? Propose a channel layout for these three streams plus movement input and other players' positions.

<details>
<summary>Answer and worked solution</summary>

**Answer:** At least `Δ + RTT = 33.3 + 140 = 173.3` ms. That is week 1's head-of-line stall rebuilt inside your own protocol.

Layout:

| Message | Class | Channel |
|---|---|---|
| Movement input | Redundant, fixed `k` (2 to 4) | none, in every packet |
| Other players' positions | Unreliable, sequenced | per entity |
| Chat | Reliable, ordered | chat |
| Inventory changes | Reliable, ordered | inventory |
| Quest updates | Reliable, ordered | quest |

Each ordered stream waits only for its own losses. Ask also whether a stream needs order at all. Two quest updates for different quests can arrive in any order, so only updates to the same quest need ordering.
</details>

## Week 7: Snapshots and delta compression

24. *Week 7 · compute.* Use the lecture's entity format (12 bytes of state, 2-byte id, 10-byte header, 13 bytes per moving player in a delta, 5 bytes per changed prop). An arena has 24 players and 100 props at 20 snapshots per second. (a) What is a full snapshot on the wire and per second? (b) What is a delta when all 24 players move and 3 props change, and how much smaller is it? (c) With `p = 0.01` per prop per tick, what is the expected delta against a baseline 6 ticks old? (d) At 150 ms RTT, what is the smallest baseline age the server can use?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,774 bytes on the wire, 283.8 kbit/s. (b) 337 bytes (365 on the wire, 58.4 kbit/s), 5.2 times smaller. (c) 351.3 bytes. (d) 3 ticks.

(a) `10 + 124 × 14 = 1,746` bytes, plus 28 is 1,774. Times 20 times 8 is 283.8 kbit/s.

(b) `10 + 24 × 13 + 3 × 5 = 337` bytes. `1,746 / 337 = 5.18`.

(c) `10 + 13 × 24 + 5 × 100 × (1 − 0.99^6) = 10 + 312 + 500 × 0.0585 = 351.3` bytes. Against the previous tick it would be `10 + 312 + 5 = 327` bytes, so waiting for acks costs about 7%.

(d) The ack for snapshot `t` takes a round trip to come back. `150 / 50 = 3` snapshot intervals, so `k ≥ 3`.
</details>

25. *Week 7 · code.* Using the lecture's `FIELDS`, `HEADER` and `encode_delta`, what does this print? Give the mask of each entity that is written.

```python
base = {1: dict(x=1.0, y=2.0, yaw=90, hp=100, anim=0),
        2: dict(x=5.0, y=5.0, yaw=0, hp=100, anim=1),
        7: dict(x=9.0, y=0.5, yaw=180, hp=40, anim=2)}
world = {1: dict(x=1.25, y=2.0, yaw=95, hp=100, anim=0),
         2: dict(x=5.0, y=5.0, yaw=0, hp=100, anim=1),
         7: dict(x=9.0, y=0.5, yaw=180, hp=35, anim=3)}
data = encode_delta(812, 809, base, world)
print(len(data), apply_delta(data, base) == world)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `24 True`

- Header: 10 bytes (tick 812, baseline 809, count 2).
- Entity 1: `x` (bit 0) and `yaw` (bit 2) changed, mask `0b00101 = 5`. It costs `2 + 1 + 4 + 2 = 9` bytes.
- Entity 2: nothing changed, so it is not written.
- Entity 7: `hp` (bit 3) and `anim` (bit 4) changed, mask `0b11000 = 24`. It costs `2 + 1 + 1 + 1 = 5` bytes.

`10 + 9 + 5 = 24`. `apply_delta` rebuilds `world` exactly, because every changed field carries its absolute new value and the client holds baseline 809.
</details>

26. *Week 7 · explain.* A team encodes each delta against the last snapshot *sent*, to save a few percent. In testing at 2% loss, players look correct but a door sometimes shows closed for several seconds after it opened. Explain the mechanism in three steps, and say why the players are not affected.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

1. Snapshot `t` carries "door open" and is lost.
2. Snapshot `t + 1` is a delta against `t`, which the client never saw. The door did not change between `t` and `t + 1`, so the delta does not mention it. The client applies the delta to its older copy, where the door is closed.
3. No later delta mentions the door until it changes again. The client shows it closed until then.

Players are not affected because they move every tick, so every delta carries their full absolute `x`, `y` and `yaw`, which overwrite any stale value. The errors land on rarely changing entities, the ones testers look at least. Encoding against the last *acknowledged* snapshot fixes it, because that delta mentions everything that changed since a state the client is known to hold.
</details>

## Week 8: Client-side prediction

27. *Week 8 · compute.* Input is sampled at 60 Hz, the server ticks at 60 Hz, snapshots go out at 30 Hz, and the display runs at 144 Hz. RTT is 80 ms. Compute the dumb client's average and worst-case key-to-screen delay, the predicted client's average delay, and the dumb client's average overshoot at 5 m/s.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Dumb average 116.8 ms, worst 153.6 ms. Predicted about 11.8 ms. Overshoot 0.58 m.

Average: `RTT + T_input/2 + T_tick/2 + T_snap/2 + T_frame/2 = 80 + 8.33 + 8.33 + 16.67 + 3.47 = 116.8` ms. Worst: `80 + 16.67 + 16.67 + 33.33 + 6.94 = 153.6` ms. Predicted: only the input and frame waits remain, `8.33 + 3.47 = 11.8` ms. Overshoot `5 × 0.1168 = 0.58` m.

The fast display barely helps the dumb client, because the round trip and the 30 Hz snapshot wait dominate.
</details>

28. *Week 8 · compute.* On the server, a slow drops a player from 5 m/s to 3 m/s. RTT is 200 ms, the tick and input rate are 60 Hz and snapshots are 20 Hz. (a) Using the lecture's error model, how large is the prediction error when the news arrives, and about how many inputs were predicted wrong? (b) A knockback of 10 m/s lasts only 80 ms at the same latency. What is the error?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.47 m, about 14 inputs. (b) 0.8 m.

(a) The horizon is `RTT + w_tick + w_snap = 200 + 8.3 + 25 = 233.3` ms. `Δv = 2` m/s, so the error is `2 × 0.2333 = 0.47` m. Inputs predicted wrong `233.3 / 16.7 ≈ 14`.

(b) The knockback ends before the horizon does, so the error is bounded by its duration: `10 × 0.08 = 0.8` m. The rule is `Δv × min(duration, horizon)`.
</details>

29. *Week 8 · design.* For a third-person action game, decide for each action whether to predict it fully, predict the effect only, or wait for the server: sprint, dodge roll, fire a hitscan rifle, loot a chest two players are racing for, drink a health potion. Give one reason per action naming what the client does or does not know.

<details>
<summary>Answer and worked solution</summary>

**A strong answer:**

| Action | Choice | Reason |
|---|---|---|
| Sprint | Predict fully | Only your input decides it. The client runs the shared `step` |
| Dodge roll | Predict fully | Same, as long as the roll's movement and cooldown are in `step` |
| Fire a hitscan rifle | Predict the effect | Show the muzzle flash, sound and a hit puff at once. The server decides the damage, after lag compensation (week 11) |
| Loot a contested chest | Effect only, or wait | Another player may have got there first. Play the lid animation and show the item only when the server grants it |
| Health potion | Predict the effect | Play the drink animation at once. The health bar waits, because the server knows about damage in flight that the client does not |

The pattern is the lecture's rule. Predict what only you control. Do not predict outcomes other players decide.
</details>

## Week 9: Server reconciliation

30. *Week 9 · code.* Using the lecture's `step` and `on_snapshot` (the version without smoothing), trace this. The client was at `x = 20.0` before input 300. It pressed right for inputs 300 to 305, nothing for 306 to 308, and left for 309 to 311, so it predicted `x = 20.3`. Then a snapshot arrives. What does the client end at, what is the correction, and which inputs are still pending?

```python
pending = ([(s, 1) for s in range(300, 306)] + [(s, 0) for s in range(306, 309)]
           + [(s, -1) for s in range(309, 312)])
c = Client()
c.state = dict(x=20.3, snare_from=10**9, snare_to=10**9)
c.pending = pending
corr = c.on_snapshot(dict(x=20.2, ack=302, snare_from=301, snare_to=400))
print(c.state["x"], round(corr, 6), [s for s, _ in c.pending])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `20.2 -0.1 [303, 304, 305, 306, 307, 308, 309, 310, 311]`

1. **Drop.** Inputs 300 to 302 are acknowledged and removed.
2. **Accept.** State becomes the server's: `x = 20.2`, snare on inputs 301 to 399. The server ran 300 at full speed (20.1) and 301 and 302 at half speed (20.15, 20.2).
3. **Replay** 303 to 311, all snared, so each step is 0.05 m. Three rights give 20.35, three idles leave it, three lefts give 20.2.
4. **Correction** `20.2 − 20.3 = −0.1` m.

Where does the 0.1 m come from? The client predicted inputs 301 and 302 at full speed, and the server ran them at half speed, which accounts for `2 × 0.05 = 0.1` m. Inputs 303 to 305 were also over-predicted by 0.15 m to the right, but 309 to 311 were over-predicted by 0.15 m to the left, so those two errors cancel. The lecture's `Δv × n × T_tick` counts snared inputs that moved in one direction. When the player turns around inside the horizon, count each direction separately.
</details>

31. *Week 9 · compute.* A vehicle game's `step` costs 0.25 ms. Inputs and ticks run at 60 Hz, snapshots at 20 Hz, and RTT is 180 ms. (a) About how many inputs are pending per snapshot, and how many milliseconds per second go to replay? (b) What share of a 60 fps frame is that on average? (c) The team raises input and tick rate to 120 Hz with the same `step` cost. What happens to replay time?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 12.8 inputs, 64 ms per second. (b) 1.07 ms per frame, 6.4% of a 16.7 ms frame. (c) About 25.1 inputs and 125.5 ms per second, nearly double.

(a) `n ≈ (180 + 8.3 + 25) / 16.7 = 12.8`. Replay `20 × 12.8 × 0.25 = 64` ms per second.

(b) `64 / 60 = 1.07` ms per frame.

(c) At 120 Hz, `n ≈ (180 + 4.2 + 25) / 8.33 = 25.1`, and `20 × 25.1 × 0.25 = 125.5` ms per second. Replay cost scales with the input rate times the round trip. For heavy physics, cap the replay or replay only the local player's body.
</details>

32. *Week 9 · compute.* A reconciliation produces a −0.6 m correction. The player is now snared and walks at 3 m/s. The display runs at 60 fps. (a) With smoothing over 0.15 s, how far does the drawn character move per frame while the offset decays? (b) With 0.3 s? (c) Which would you pick for slows, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About −1.7 cm per frame, a slow backward drift. (b) About +1.7 cm per frame, a slow forward walk. (c) 0.3 s, for this kind of error.

(a) 0.15 s is 9 frames. The offset shrinks by `0.6 / 9 = 0.0667` m per frame, and walking adds `3 / 60 = 0.05` m. Net `−0.0167` m per frame.

(b) 0.3 s is 18 frames. `−0.6 / 18 + 0.05 = +0.0167` m per frame. The character never moves backward. It just walks slowly for 0.3 s.

(c) For a slow, a longer smoothing time makes the correction look like the slow itself, which is what happened. Keep a snap threshold above which you do not smooth, because smoothing a large error lies about where the player is.
</details>

33. *Week 9 · critique.* A student's reconciling client shows a correction of about 2 cm on every snapshot while walking on flat ground with no other players. They propose raising the snap threshold to 5 cm "so nobody sees it." A second student matches snapshots to inputs by timestamp instead of by sequence number. Critique both.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

Constant small corrections mean `step` is not shared. The client and server use different `dt` values, a constant (speed, friction) differs between builds, or floating-point results differ between machines. Raising the threshold hides the symptom and leaves the cause. Every real surprise then arrives on top of a drift. Fix the code so the correction on flat ground is exactly zero, as in the lecture's no-snare run.

Matching by timestamp breaks the moment the client's frame rate stutters or the server holds an input for a tick. The snapshot's `ack` names exactly which input the server state follows. Sequence numbers make the comparison exact. Clocks make it approximate.
</details>

## Week 10: Entity interpolation

34. *Week 10 · code.* Using the lecture's `InterpolationBuffer`, what does this print for each render time? Snapshot 3150 was lost.

```python
buf = InterpolationBuffer(max_extrap_ms=100)
buf.snaps = [(3000, 12.0), (3050, 12.25), (3100, 12.5), (3200, 12.0)]
for t_r in (2990, 3030, 3150, 3230, 3400):
    x, mode = buf.sample(t_r)
    print(t_r, round(x, 4), mode)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
2990 12.0 hold
3030 12.15 interp
3150 12.25 interp
3230 11.85 extrap
3400 11.5 extrap
```

- 2990 is older than every snapshot, so the buffer holds the oldest, 12.0.
- 3030: `alpha = 30 / 50 = 0.6`, `12.0 + 0.6 × 0.25 = 12.15`.
- 3150 falls in the gap left by the lost snapshot. It lerps 3100 to 3200 with `alpha = 0.5`: `12.5 − 0.25 = 12.25`. If the entity really turned at 3150, that peak never appears.
- 3230: past the newest snapshot, so it extrapolates with the last velocity, `(12.0 − 12.5) / 100 = −0.005` m/ms, for 30 ms: `12.0 − 0.15 = 11.85`.
- 3400: 200 ms past the newest, but the cap is 100 ms, so `12.0 − 0.5 = 11.5`. The cap stops the entity sliding forever.
</details>

35. *Week 10 · compute.* Snapshots arrive at 30 Hz. The game wants to survive two lost snapshots in a row with 15 ms of jitter margin. (a) What `D` does `D = kΔ + J` give? (b) At 40 ms one-way latency, how far behind the server is a remote player drawn, in ms and in meters at 5 m/s? (c) What would doubling the snapshot rate to 60 Hz give for the same safety?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 115 ms. (b) 155 ms, 0.78 m. (c) `D = 65` ms, drawn 105 ms behind, 0.53 m.

(a) Surviving 2 losses needs `k = 3`. `Δ = 33.3`, so `D = 100 + 15 = 115` ms.

(b) Age behind the server is `L + D = 40 + 115 = 155` ms. `5 × 0.155 = 0.775` m.

(c) `Δ = 16.7`, `D = 50 + 15 = 65` ms, `40 + 65 = 105` ms, `0.525` m. Doubling the send rate halves the `kΔ` part. The price is week 13's bandwidth.
</details>

36. *Week 10 · code.* What does this print, and which line is correct for a heading?

```python
def lerp_angle(a, b, alpha):
    diff = (b - a + 180) % 360 - 180
    return (a + alpha * diff) % 360

print(300 + 0.75 * (20 - 300), lerp_angle(300, 20, 0.75), lerp_angle(10, 190, 0.5))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `90.0 0.0 280.0`

The plain lerp goes from 300° down through 180° to 20°, the long way round, 280° of turning. At `alpha = 0.75` it reaches 90°, pointing almost the opposite way. The shortest arc is `diff = (20 − 300 + 180) % 360 − 180 = 80`, so `300 + 60 = 360 → 0°`. That is the correct heading.

The last call is the tie case. From 10° to 190° is exactly 180° either way. The formula gives `diff = −180` (its range is `[−180, 180)`), so it turns the negative way and passes through 280°. Any consistent choice is fine, but a buffer must make the same choice on every frame, or a model turning exactly half a circle will flicker between two directions.
</details>

37. *Week 10 · critique.* A student's interpolation buffer stamps each snapshot with the client's arrival time, because "the server clock is on another machine." Motion is smooth on the lab LAN and jerky on Wi-Fi. Explain why, and fix it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Arrival time includes jitter. On Wi-Fi, a snapshot that arrives 20 ms late gets a timestamp 20 ms late, so the buffer lerps between samples placed at the wrong times and plays the jitter straight back into the motion. On a LAN jitter is near zero, which hides the bug.

Fix: stamp each snapshot with the server tick it describes, and compute `t_r` from a smoothed estimate of the server's clock. Nudge the render clock's rate by about 1% when the buffer fills or runs dry, rather than jumping it. The server's clock being on another machine does not matter, because only differences between server ticks are used, and they are exact.
</details>

## Week 11: Lag compensation

38. *Week 11 · compute.* A shooter has a 90 ms RTT, 30 snapshots per second and `cl_interp_ratio 2`. The target runs at 7 m/s with a 0.3 m hitbox radius. The victim's RTT is 30 ms. (a) What is the rewind `R`, and how far would the shooter have to lead without rewind? (b) What is the victim's worst time behind cover `W`? (c) The server sets `R_max = 150` ms. What residual lead does this shooter need, does a center shot still hit, and what is the new worst `W`? (d) Up to what RTT does a shooter need no lead at all?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `R = 156.7` ms, lead 1.10 m. (b) 186.7 ms. (c) Residual 6.7 ms, 0.047 m, the center shot hits, `W = 180` ms. (d) 83.3 ms.

(a) `D = 2 / 30 s = 66.7` ms. `R = RTT + D = 156.7` ms. Lead `7 × 0.1567 = 1.10` m, more than three radii.

(b) `W = RTT_s + D + RTT_v = 90 + 66.7 + 30 = 186.7` ms.

(c) `R_used = 150`, so the shooter is short by 6.7 ms, `7 × 0.0067 = 0.047` m. That is inside the 0.3 m radius, so a center shot hits. The victim's worst case is now `R_max + RTT_v = 180` ms whoever shoots.

(d) `RTT + 66.7 ≤ 150`, so up to 83.3 ms.
</details>

39. *Week 11 · code.* Using the lecture's `ray_hits_circle`, what does this print? Show `along` and the squared perpendicular distance for each.

```python
for center in ((6.2, 7.9), (6.5, 7.6), (-6.0, -8.0)):
    print(center, ray_hits_circle((0, 0), (3, 4), center, 0.3))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
(6.2, 7.9) True
(6.5, 7.6) False
(-6.0, -8.0) False
```

The direction normalizes to `(0.6, 0.8)`.

| Center | `along` | `|c|²` | Perpendicular² | Against `0.3² = 0.09` |
|---|---|---|---|---|
| (6.2, 7.9) | `3.72 + 6.32 = 10.04` | 100.85 | `100.85 − 100.8016 = 0.0484` | hit |
| (6.5, 7.6) | `3.90 + 6.08 = 9.98` | 100.01 | `100.01 − 99.6004 = 0.4096` | miss, 0.64 m off |
| (−6, −8) | −10 | 100 | 0 | behind the shooter |

The third target sits exactly on the line, but behind the muzzle. Without the `along < 0` test it would count as a hit.
</details>

40. *Week 11 · code.* Using the lecture's `History`, what does this print? Then say what is wrong with the answer for `t = 100` and what a server should do about shots that need it.

```python
h = History(max_unlag_ms=200, tick_ms=50)
print(h.records.maxlen)
for t in range(0, 400, 50):
    h.record(t, (t / 100, 0.0))
for t in (100, 180, 330, 500):
    print(t, h.position_at(t))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
5
100 (1.5, 0.0)
180 (1.8, 0.0)
330 (3.3, 0.0)
500 (3.5, 0.0)
```

`maxlen = round(200 / 50) + 1 = 5`, so after eight records only 150 to 350 remain. 180 lerps between 150 and 200. 330 lerps between 300 and 350. 500 is newer than anything stored, so it clamps to 3.5.

At 100 ms the true position was 1.0, but the record is gone, so `position_at` clamps to the oldest record, 1.5. That is a position the target reached 50 ms later. A shot needing a rewind older than the buffer is, by design, older than `R_max`. The server should rewind only to `arrival − R_max` (which `server_hit` does with its `min`), so the shooter must lead by the rest. The history must cover at least `R_max` plus one tick, or clamping will silently return wrong positions.
</details>

41. *Week 11 · compute.* Use the peeker's-advantage formula from the lecture (RTT plus two server frames plus three client frames, Riot's accounting). A game runs 64 tick servers, and the round-trip latency term is 50 ms. (a) What is the peeker's advantage for a 144 fps client and for a 60 fps client? (b) This course's arena instead interpolates with `D = 100` ms on top of the 60 fps figure. What is the head start then, and can lag compensation reduce it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 102.1 ms at 144 fps, 131.2 ms at 60 fps. (b) About 231 ms. No.

(a) Server frames `2 × 1000 / 64 = 31.25` ms. At 144 fps, `3 × 6.94 = 20.8`, total `50 + 31.25 + 20.8 = 102.1`. At 60 fps, `3 × 16.7 = 50`, total 131.25.

(b) `131.2 + 100 = 231.2` ms. Lag compensation makes the shooter's view authoritative for the shooter's own shots. It cannot change when the defender's screen showed the peeker. Only lower latency and less buffering (higher tick and snapshot rates, a smaller `D`) reduce it.
</details>

## Week 12: Deterministic lockstep

42. *Week 12 · compute.* Six players in a full mesh. Lockstep uses `T = 250` ms turns, 1.5 commands per player per second at 10 bytes, and 32 bytes of header and turn field per packet. State sync would send 6 bytes per unit, 2 times per second, with the same 32-byte overhead. (a) What is each peer's upload under lockstep? (b) Under state sync with 600 units in total? (c) At what unit count do the two cost the same?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 715 B/s. (b) 6,320 B/s. (c) About 40 units (39.5).

(a) `(P − 1) × [(1000 / T) × 32 + b × c] = 5 × (4 × 32 + 15) = 5 × 143 = 715` B/s.

(b) Each player owns `600 / 6 = 100` units. `(P − 1) × r × (32 + s × N / P) = 5 × 2 × (32 + 600) = 6,320` B/s.

(c) With `s = 6` and `P = 6`, `s × N / P = N`, so `10 × (32 + N) = 715` gives `N = 39.5`. Below about 40 units state sync is cheaper. Above it, lockstep's flat cost wins, and at 600 units by a factor of 8.8.
</details>

43. *Week 12 · compute.* A lockstep game uses `T = 160` ms. The worst one-way latency between any two peers is 220 ms. (a) With `k = 2`, what is `T_eff`, the average command delay, and how much slower does the game run? (b) With `k = 3`? (c) Which would Ensemble's finding about consistent delay tell you to pick?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `T_eff = 190` ms, average delay 285 ms, 18.75% slower. (b) `T_eff = 160` ms, average delay 400 ms, no slowdown. (c) `k = 3`.

(a) `max(160, (160 + 220) / 2) = 190`. Delay `(k − ½) × T_eff = 1.5 × 190 = 285` ms. `190 / 160 = 1.1875`.

(b) `(160 + 220) / 3 = 126.7`, so `T_eff = 160`. Delay `2.5 × 160 = 400` ms. `k = 3` tolerates `L_max` up to `2 × 160 = 320` ms.

(c) `k = 3`. Both delays are under Ensemble's 500 ms "noticeable" line, and a steady 400 ms beats a game whose turns stretch and shrink with the slowest link. In practice the 220 ms link will also have jitter, which under `k = 2` means stalls on every spike.
</details>

44. *Week 12 · critique.* This fragment runs on every peer of a lockstep RTS. Find four determinism bugs and fix each. (It uses helper functions not shown.)

```python
import random

def resolve_turn(units, commands):
    for cmd in commands:                        # in the order this peer received them
        apply(cmd, units)
    for u in {u for u in units if u.hp > 0}:
        target = nearest_enemy(u, units)
        if target and random.random() < 0.75:
            target.hp -= u.damage * 1.1
        if on_my_screen(u) and random.random() < 0.2:
            play_sound("battle_cry", u)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

1. **Command order.** Each peer receives its own commands first, so the order differs between peers. Sort each turn's commands by a canonical key, such as (player id, sequence number), before applying them.
2. **Set iteration.** A set has no promised order, so peers can resolve the same fight in different orders, and the order decides who dies first. Iterate a list sorted by unit id.
3. **Local-only state drawing from the shared generator.** `on_my_screen` differs per peer, so peers make different numbers of `random.random()` calls, and every later hit roll diverges. That is Ensemble's terrain-sound bug. Give cosmetic effects their own local generator. Also use one explicitly seeded `random.Random(seed)` for the simulation, not the module-level generator.
4. **Floating-point damage.** `damage * 1.1` makes health a float, and sums of floats depend on order and, across builds and platforms, on the compiler. Keep health in integer fixed point (for example tenths of a point) and use integer damage.

Then checksum each turn (week 12's CRC-32 over units in id order) so any remaining leak is caught on the turn it shows up.
</details>

45. *Week 12 · code.* What does this print, and what does the result mean for a lockstep game?

```python
import struct, zlib

def checksum(turn, units):
    data = struct.pack("<i", turn)
    for u in units:
        data += struct.pack("<iiii", *u)
    return zlib.crc32(data)

a = [(1, 10, 20, 100), (2, 30, 40, 90)]
b = list(reversed(a))
print(checksum(5, a) == checksum(5, b), checksum(5, a) == checksum(5, sorted(b)))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `False True`

The two peers hold identical units, but CRC-32 hashes bytes in order, so listing the same units in a different order gives a different checksum. Sorting by id restores the match.

For lockstep this cuts both ways. A checksum over an unordered collection reports a desync that is not there. And if the simulation itself iterates in that unordered way, the states really will diverge. The lecture's rule covers both. Keep units in a list in id order, and pack with an explicit byte order (`<`) so the bytes are identical on every machine.
</details>

## Week 13: Tick rate and bandwidth budgets

46. *Week 13 · code.* Using the lecture's `budget` function, what are the client download (kbit/s) and server upload (Mbit/s) for each call? What happens to each when the player count doubles?

```python
for args in ((80, 30, 20), (160, 30, 20)):
    print(budget(*args), budget(*args, K=24))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `n` | Cap | Packets | Snapshot | Client download | Server upload |
|---|---|---|---|---|---|
| 80 | none | 2 | 1,656 B | 397.4 kbit/s | 31.8 Mbit/s |
| 80 | 24 | 1 | 508 B | 121.9 kbit/s | 9.75 Mbit/s |
| 160 | none | 3 | 3,284 B | 788.2 kbit/s | 126.1 Mbit/s |
| 160 | 24 | 1 | 508 B | 121.9 kbit/s | 19.5 Mbit/s |

At `n = 80` with no cap, `80 × 20 = 1,600` bytes need `⌈1,600 / 1,252⌉ = 2` packets, so `S = 1,600 + 56 = 1,656`. Client `30 × 1,656 = 49,680` B/s. Server `80 × 49,680 = 3,974,400` B/s. With the cap, `24 × 20 + 28 = 508` bytes.

Doubling `n` without a cap multiplies the server's upload by 3.97 (the `n²` wall, slightly off 4 because of headers) and doubles each client's download. With the cap the client's download does not change, and the server's upload exactly doubles.
</details>

47. *Week 13 · compute.* Use the lecture's illustrative tick cost `c(n) = 0.2 + 0.1n + 0.002n²` ms. (a) At 64 ticks per second, what is the largest match that fits one game per core? (b) The studio wants 3 games per core at 64 Hz. What is the largest match now? (c) At 20 Hz with one game per core?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 66 players. (b) 30 players. (c) 134 players.

(a) The tick is `1000 / 64 = 15.625` ms. `c(66) = 0.2 + 6.6 + 8.712 = 15.51` ms fits. `c(67) = 15.88` does not.

(b) Each game gets `15.625 / 3 = 5.21` ms. `c(30) = 0.2 + 3 + 1.8 = 5.0` fits. `c(31) = 5.22` does not.

(c) The tick is 50 ms. `c(134) = 0.2 + 13.4 + 35.9 = 49.5` fits, and `c(135) = 50.2` does not.

The `n²` term is why a large match is pushed to a low tick rate even when the per-player cost is the same, the lecture's Valorant against Apex comparison in numbers.
</details>

48. *Week 13 · code.* Using the lecture's `fill_packet`, trace five ticks. Four entities have priorities A 1.0, B 0.5, C 0.25 and D 0.25. There is room for 2 per packet (`fill_packet(ents, 40, 20)`). Python's sort is stable, so ties keep their previous order. Which entities are sent each tick, and how many times is each sent over the five ticks?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Tick | Accumulators before sending | Sent | Left over |
|---|---|---|---|
| 1 | A 1.0, B 0.5, C 0.25, D 0.25 | A, B | C 0.25, D 0.25 |
| 2 | A 1.0, B 0.5, C 0.5, D 0.5 | A, B | C 0.5, D 0.5 |
| 3 | A 1.0, C 0.75, D 0.75, B 0.5 | A, C | D 0.75, B 0.5 |
| 4 | A 1.0, D 1.0, B 1.0, C 0.25 | A, D | B 1.0, C 0.25 |
| 5 | B 1.5, A 1.0, C 0.5, D 0.25 | B, A | C 0.5, D 0.25 |

Totals: A 5, B 3, C 1, D 1. At tick 3, B ties with nobody but is overtaken by C and D, whose accumulators grew while B's was reset twice. At tick 4, A, D and B tie at 1.0 and the stable sort keeps A and D ahead because of their order after tick 3.

The priorities sum to 2.0 per tick and there are 2 slots, so in the long run every entity is sent in proportion to its priority. A 12,000-tick run gives A every tick, B every 2 ticks, and C and D every 4. Nobody starves.
</details>

49. *Week 13 · design.* An MMO city hub must hold 300 players in view at `r = 10` Hz with `b = 24` bytes per entity. (a) Compute server upload without a cap. (b) With an interest cap `K = 40`. (c) Compare with two other levers applied alone, halving `b` to 12 and halving `r` to 5. Rank the levers and say which one changes the shape of the curve.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 176.8 Mbit/s. (b) 23.7 Mbit/s. (c) Halving `b` or halving `r` gives 88.4 Mbit/s each. The cap wins by a factor of 7.5 over no cap, and it is the only lever that bends the curve.

(a) `300 × 24 = 7,200` bytes need 6 packets, so `S = 7,368` bytes, client `73,680` B/s (589.4 kbit/s), server `22,104,000` B/s.

(b) `40 × 24 + 28 = 988` bytes, client `9,880` B/s (79.0 kbit/s), server `2,964,000` B/s.

(c) `b = 12`: `3,600 + 3 × 28 = 3,684` bytes, server `11,052,000` B/s. `r = 5`: half of (a).

Halving `b` or `r` divides everything by 2 at every `n`. The cap changes `n²` into `K × n`, so its advantage grows with every player added. Halving `r` also costs 100 ms more interpolation delay at two intervals, which a city hub can afford.
</details>

## Week 14: Testing under bad networks

50. *Week 14 · compute.* A bug needs a burst of at least 4 lost packets. The game sends at 60 Hz. (a) Under bursty loss `p = 2%`, `q = 0.5`, how many such bursts happen per minute, and how long until a 95% chance of seeing one? (b) Under independent 2% loss? (c) What is the chance that a 10-minute playtest on the independent profile finds it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 4.5 per minute, `t95 = 0.67` minutes (40 s). (b) 0.00056 per minute, `t95 ≈ 5,300` minutes (88 hours). (c) 0.56%.

(a) `β = p(1 − q)q^(k − 1) = 0.02 × 0.5 × 0.125 = 0.00125`. `λ = 3,600 × 0.00125 = 4.5` per minute. `t95 = ln 20 / 4.5 = 0.67`.

(b) `β = 0.02 × 0.98 × 0.02³ = 1.568 × 10⁻⁷`. `λ = 3,600 × 1.568 × 10⁻⁷ = 0.000564`. Mean wait `1 / λ ≈ 1,772` minutes, `t95 = ln 20 / 0.000564 ≈ 5,307` minutes.

(c) `1 − e^(−0.000564 × 10) = 0.56%`. Same average loss, eight thousand times longer to find. Always include bursty loss.
</details>

51. *Week 14 · compute.* A test uses netem with `delay 60ms 25ms` (uniform jitter). What fraction of consecutive packet pairs arrive out of order at 20 Hz, 30 Hz and 60 Hz sending?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0% at 20 Hz, 5.6% at 30 Hz, 22.2% at 60 Hz.

`W = 2 × 25 = 50` ms. `P = (W − Δ)² / (2W²)` when `Δ < W`.

- 20 Hz: `Δ = 50 = W`, so 0.
- 30 Hz: `(50 − 33.3)² / 5,000 = 277.8 / 5,000 = 5.56%`.
- 60 Hz: `(50 − 16.7)² / 5,000 = 1,111 / 5,000 = 22.2%`.

The same netem line is a reordering stress test for a 60 Hz game and tests no reordering at all for a 20 Hz one. Real connections reorder far less than 22%, so label this profile a stress test.
</details>

52. *Week 14 · compute.* Write the netem `gemodel` settings for an average loss of 3% with a mean burst of 2.5 packets (100% loss in the bad state, 0% in the good). Show that the settings give back 3%. What round-trip loss would a ping measure on `lo`, where both legs pass through netem, if loss were independent?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `loss gemodel 1.24% 40% 100% 0%`. About 5.9% round-trip loss.

Mean burst `1 / (1 − q) = 2.5` gives `q = 0.6`, so the chance of leaving the bad state is `1 − q = 40%`. The chance of entering is `a = p(1 − q) / (1 − p) = 0.03 × 0.4 / 0.97 = 1.237%`.

Check the long-run balance: `a(1 − p) + qp = 0.01237 × 0.97 + 0.6 × 0.03 = 0.012 + 0.018 = 0.03`.

Round trip with independent loss: `1 − 0.97² = 5.91%`. With the bursty settings, the request and its reply pass through the same netem queue a moment apart, so their fates are linked and a measured round-trip loss can differ from 5.91%. Measure it with Lab 02's ping before you trust the setting, as the lecture's section 3 advises.
</details>

53. *Week 14 · critique.* A lead writes: "We ran the netcode at 5% independent loss for a full hour at 30 Hz and saw no problems, so our redundant reliable messages (fail only on 5 lost in a row) are safe." Is the test evidence for that claim? Compute the chance that the test would have exposed the failure, and suggest a better test.

<details>
<summary>Answer and worked solution</summary>

**Answer:** No. The hour had about a 3.2% chance of producing even one burst of 5.

`β = 0.05 × 0.95 × 0.05⁴ = 2.97 × 10⁻⁷`. At 30 Hz, `λ = 108,000 × 2.97 × 10⁻⁷ = 0.032` per hour, so `1 − e^(−0.032) = 3.2%`. The same hour would have shown a burst of 3 almost surely (`λ = 0.21` per minute), which is why "no problems" felt convincing.

A better test targets the event. With bursty loss `q = 0.6` at 5% average, `β = 0.05 × 0.4 × 0.6⁴ = 0.0026`, about 280 bursts of 5 per hour. Or set `p` and `q` so `t95` is a few minutes, run several seeds, and log the profile and seed for every failure so it replays.
</details>

54. *Week 14 · design.* Your prototype has an interpolation buffer of 2 intervals at 60 Hz snapshots. Design a test for it. Give (a) the network event that triggers the rare branch, (b) how often the lecture's "Evening Wi-Fi" profile (1% loss, `q = 0.5`, ±15 ms jitter) produces it and the `t95`, (c) how much reordering that profile causes at 60 Hz, and (d) one invariant a program can check.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) A burst of 2 lost snapshots empties the buffer and forces extrapolation. (b) 9 per minute, `t95 ≈ 20` seconds. (c) About 9.9% of pairs. (d) For example, "the drawn position never moves more than the maximum speed times the frame time, plus a tolerance," or "the server tick used for rendering never goes backwards."

(b) `β = 0.01 × 0.5 × 0.5 = 0.0025` per packet. `λ = 3,600 × 0.0025 = 9` per minute. `t95 = 3.0 / 9 = 0.33` minutes.

(c) `W = 30` ms, `Δ = 16.7` ms. `(30 − 16.7)² / (2 × 900) = 9.9%`. At 30 Hz this profile cannot reorder at all (`Δ = 33.3 > W`), which is why the lecture's toy client only met its reordering bug on the mobile profile.

(d) Invariants must be checks a program can apply without a human, and each run needs a seed so a failure replays exactly.
</details>

## Across the course: viva questions

55. *Weeks 2, 8, 10, 11, 13 · design.* You are building a 4-player co-op arena. Server tick and snapshots 30 Hz, input sampled at 60 Hz, 60 fps display, RTT 120 ms, `D` = two snapshot intervals, `b = 16` bytes per entity, walking speed 5 m/s. Give (a) the dumb client's average key-to-screen delay and what prediction reduces it to, (b) how far behind the server a teammate is drawn, (c) the rewind a hitscan shot needs, and (d) one client's download and the server's upload. Then say which of these numbers you would measure rather than trust in your final prototype, and with which lab's tool.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 170 ms, about 16.7 ms with prediction. (b) 126.7 ms, 0.63 m. (c) `R = 186.7` ms. (d) 22.1 kbit/s per client, 88.3 kbit/s at the server.

(a) `120 + 8.33 + 16.67 + 16.67 + 8.33 = 170` ms (input 60 Hz, tick 30 Hz, snapshots 30 Hz, frame 60 Hz). Predicted: `8.33 + 8.33 = 16.7` ms.

(b) `D = 2 / 30 s = 66.7` ms, `L = 60` ms, so `L + D = 126.7` ms, `5 × 0.1267 = 0.63` m.

(c) `R = RTT + D = 120 + 66.7 = 186.7` ms.

(d) `budget(4, 30, 16)`: `S = 64 + 28 = 92` bytes, client `2,760` B/s, server `11,040` B/s.

Measure rather than trust: the RTT distribution and loss burstiness (Lab 02's ping and `analyze.py`), the real bytes per snapshot on the wire (Lab 13's encoder and a byte counter on the socket), and whether the interpolation and reconciliation branches survive bursts (Lab 14's matrix). The final prototype brief asks for exactly these.
</details>

56. *Weeks 2, 10, 11, 13 · critique.* In a 60-player shooter at 20 Hz snapshots with `b = 40` bytes and no interest cap, a producer says: "Players complain about peeker's advantage. Triple the snapshot rate to 60 Hz. It's just a config change." Quantify what the change buys and what it costs, and propose a cheaper way to get part of the benefit.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It buys about 83 ms (tick wait plus two-interval interpolation falls from 125 to 41.7 ms). It costs three times the bandwidth: each client's download goes from 393 to 1,179 kbit/s and the server's upload from 23.6 to 70.7 Mbit/s, plus three times the snapshot-writing CPU if the tick rate rises too.

From the week 13 table, the rate's latency is `1000 / (2r) + 2 × 1000 / r`: 125 ms at 20 Hz, 41.7 ms at 60 Hz. `budget(60, 20, 40)`: 2 packets, 2,456 bytes, 49,120 B/s per client, 2.95 MB/s at the server. At 60 Hz, triple each.

Cheaper options: quantize to cut `b` (week 5), add an interest cap so each client hears only nearby players (the only lever that bends `n²`), or keep 20 Hz but shrink `D` if loss data allows, which week 10 says costs pops. Lag compensation will not help, because it fixes the shooter's aim, not when the defender sees the peeker (week 11).
</details>
