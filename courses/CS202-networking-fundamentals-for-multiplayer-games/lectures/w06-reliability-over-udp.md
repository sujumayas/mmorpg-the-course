# CS202 · Week 06 — Reliability over UDP

**Why this matters:** Week 1 chose UDP so that one lost packet would not freeze the game. The price was that nothing arrives for certain. Some messages must arrive (the fire button, the item pickup, the chat line), and you now have to build that guarantee yourself, only where it is needed, and without the stalls TCP would have added. This week you build the pieces and learn to choose between them with numbers.

**You will be able to:**
- Compare 16-bit sequence numbers across wraparound, and write and read an ack header that confirms 33 packets at once.
- Compute the chance that an input is lost when it is sent in `k` consecutive packets, under independent and bursty loss, and what the extra copies cost in bandwidth.
- Compare redundancy with ack-and-resend on delivery delay, and choose the right one for each message type.
- Explain why a reliable ordered channel brings head-of-line blocking back, and design channels to contain it.

**Before class:** Glenn Fiedler, "Reliability and Congestion Avoidance over UDP" (Gaffer on Games, 20 October 2008). Frohnmayer, M. & Gift, T. (undated), "The TRIBES Engine Networking Model", the opening list of data classes and the "Move Stream Manager" section. Reread MA102 week 3 on the complement rule.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance that every copy is lost). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (copies until the first one gets through). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (the lab checks a formula against an hour of simulated packets). [CS202 week 1](w01-networks-for-game-devs-tcp-vs-udp.md) (head-of-line blocking and the message table), [week 2](w02-latency-jitter-loss-measure-your-own.md) (bursty loss and `q`), [week 5](w05-serialization-and-bit-packing.md) (packing a header).

**Interactive:** [examples/w06-redundant-inputs.html](../examples/w06-redundant-inputs.html). Keep it open during section 2.

---

## 1. What UDP leaves you to build

UDP hands you datagrams that may be lost, duplicated or reordered, and says nothing about which happened. To build anything reliable on top, you need three pieces.

- A **sequence number** on every packet, so the receiver can tell which packets arrived, which are missing, and which came out of order.
- **Acknowledgements (acks)** going back, so the sender learns which packets arrived.
- A policy for what to do about the missing ones. Resend what was in them, send it again in advance just in case, or do nothing because newer data replaces it.

The third piece is where games differ from TCP. TCP treats every byte alike. A game has several kinds of data with different needs, and it should treat each kind differently.

### Delivery classes

The Tribes networking paper, written while *Tribes 2* was in development, sorted all of a game's data into four classes. The list is still the clearest way to think about it.

| Class (Tribes name) | Meaning | Examples |
|---|---|---|
| Non-guaranteed | Never resent if lost | Sound cues, cosmetic effects |
| Guaranteed | Resent until it arrives, delivered in order | Chat, inventory changes, "player joined" |
| Most recent state | Only the newest version matters | Positions, health bars, scores |
| Guaranteed quickest | Must arrive, as fast as possible | Player inputs |

Libraries give the same menu under other names. RakNet, the library under *Minecraft: Bedrock Edition* that week 1 mentioned, offers `UNRELIABLE`, `UNRELIABLE_SEQUENCED`, `RELIABLE`, `RELIABLE_ORDERED` and `RELIABLE_SEQUENCED`. "Sequenced" means old messages that arrive after newer ones are thrown away, which is Tribes' "most recent state." "Ordered" means messages wait for earlier ones, which is Tribes' "guaranteed."

### Sequence numbers that wrap

A sequence number costs bytes, so games use 16 bits. At 60 packets per second, 16 bits run out after `65,536 / 60 = 1,092` seconds, about 18 minutes. After 65,535 comes 0 again. So "is packet `a` newer than packet `b`?" cannot be `a > b`. Fiedler's answer treats the numbers as points on a circle, and calls `a` newer if it is less than half the circle ahead of `b`.

```python
def seq_greater_than(a, b):
    return (a > b and a - b <= 32768) or (a < b and b - a > 32768)
```

So 2 is newer than 65,534 (it is 4 steps ahead, around the wrap), and 40,000 is *older* than 5,000 (it is more than half the circle ahead, so it must be from the previous lap). This works as long as no packet arrives more than half a lap late, about 9 minutes at 60 Hz, which never happens.

### Acks, 33 at a time

The receiver could ack each packet with its own message. Fiedler's scheme is cheaper and survives lost acks. Every packet going the other way carries two fields.

- `ack`, the newest sequence number received.
- `ack_bits`, 32 bits. Bit `n` is set if packet `ack − 1 − n` was received.

Together with its own sequence number, that is an 8-byte header (`struct.Struct("!HHI")`, two 16-bit numbers and one 32-bit number), and each header confirms up to 33 packets.

Trace one. The receiver got 65,533, 65,534, 0, 1 and 3. Packets 65,535 and 2 were lost. The newest is 3, so `ack = 3`. Counting back from 2, bit 0 is packet 2 (missing, 0), bit 1 is packet 1 (1), bit 2 is packet 0 (1), bit 3 is 65,535 (0), bit 4 is 65,534 (1), bit 5 is 65,533 (1). Reading from bit 5 down, `ack_bits = 0b110110`, which is 54.

Why 33? Because every ack is repeated in the next 32 headers. An ack is lost for good only if all 33 packets carrying it are lost. At 5% independent loss that is `0.05^33`, about `10^-43`. Even with bursty loss where `q = 0.5`, it is `0.05 × 0.5^32`, about `10^-11`. The sender will know.

### Resend messages, never packets

When the sender learns a packet was lost, it does not resend that packet. The packet's old sequence number has already been reported missing, and the data in it may be out of date. Instead the sender puts the *messages* that must arrive into a new packet with a new sequence number. Fiedler states it as a rule. A packet with a given sequence number is never sent twice. Reliability belongs to messages. Packets are just the trucks that carry them.

## 2. Worked example: send it three times, or wait for the ack?

### The hook

*Starsiege: Tribes* (1998) sent its players' input moves over UDP. Moves were the only thing that controlled a player's movement, so every one mattered, and they had to arrive quickly. The first version sent every move the server had not yet acknowledged in every packet. That guaranteed delivery. It also set off what the developers called a negative feedback loop. A dropped packet meant more unacknowledged moves, so the next packet was bigger. On a low-bandwidth internet connection, the bigger packet could exceed the connection's bandwidth, which dropped more packets, which made the next one bigger still.

For *Tribes 2*, the design changed, as the paper describes it. The paper is undated and was written while *Tribes 2* was still in development, so this is the planned design, not a check of the shipped game. Each move was sent exactly three times, in three consecutive packets. If three packets in a row were lost, the moves unique to them were gone, and the player saw a brief warp. The developers wrote that this handled heavy loss better than the guaranteed version did.

*Quake III Arena* (1999) made the same kind of choice with a setting players could change. Its client includes every command since a packet from `cl_packetdup` packets ago, so with the default of 1 each command rides in two consecutive packets. The setting is clamped between 0 and 5.

So three shipped games decided that for inputs, sending extra copies up front beat waiting to hear what was lost. How much does each copy buy, and when does it stop working?

### The model

The client sends one packet per tick, every `Δ` ms. Each packet is lost with probability `p`. Each input is sent in `k` consecutive packets.

**Redundancy.** The input is lost only if all `k` copies are lost.

```
P(input lost), independent loss   = p^k
P(input lost), bursty loss        = p × q^(k − 1)
extra delay if copy j is the first to arrive = j × Δ
```

- `q` is week 2's burstiness, the chance that a packet is lost given that the one before it was. Independent loss is `q = p`.
- Every copy after the first is one packet later, so a rescued input arrives `Δ`, `2Δ`, ... late.

**Ack and resend.** Send each input once. When an ack shows the packet was lost, send the input again in the next packet. The input is never lost for good, but the sender cannot know about the loss until an ack for a *later* packet comes back.

```
extra delay after one loss ≥ Δ + RTT
```

**Bandwidth.** Each packet carries a 28-byte UDP/IPv4 header (week 1), an 8-byte sequence and ack header, and `k` inputs of 4 bytes each (week 5 packs an input that small).

```
packet bytes = 28 + 8 + 4k
```

### Numbers you can check

An hour of play at 60 inputs per second is 216,000 inputs. At 60 packets per second:

| Loss `p` | Copies `k` | `P(input lost)` | Inputs lost per hour | Packet | Upload |
|---|---|---|---|---|---|
| 1% | 1 | 1 in 100 | 2,160 | 40 B | 19.2 kbit/s |
| 1% | 2 | 1 in 10,000 | 21.6 | 44 B | 21.1 kbit/s |
| 1% | 3 | 1 in 1,000,000 | 0.2 | 48 B | 23.0 kbit/s |
| 5% | 1 | 1 in 20 | 10,800 | 40 B | 19.2 kbit/s |
| 5% | 2 | 1 in 400 | 540 | 44 B | 21.1 kbit/s |
| 5% | 3 | 1 in 8,000 | 27 | 48 B | 23.0 kbit/s |
| 20% | 3 | 1 in 125 | 1,728 | 48 B | 23.0 kbit/s |

Check the 5%, `k = 3` row. `0.05^3 = 0.000125`, and `216,000 × 0.000125 = 27`. Each extra copy divides the losses by 20 and costs 4 bytes per packet, 1.9 kbit/s. The headers already cost 36 bytes, so three copies make a 48-byte packet, only 20% bigger than the 40 bytes of a single copy. That is why redundancy is the usual answer for inputs. Inputs are tiny, and the header is paid for anyway.

Now make the loss bursty. Same average loss of 5%, but `q = 0.5`, so bursts average two packets.

| Loss pattern | `k = 1` | `k = 2` | `k = 3` | `k = 4` |
|---|---|---|---|---|
| Independent, `p = 5%` | 10,800 | 540 | 27 | 1.4 |
| Bursty, `p = 5%`, `q = 0.5` | 10,800 | 5,400 | 2,700 | 1,350 |

Under independent loss, each copy divides losses by 20. Under bursty loss, each copy only halves them. The third copy that saved 513 inputs an hour on the independent link saves 2,700 on the bursty one but leaves 2,700 behind, a hundred times more than the formula for independent loss promised. Week 2 said to report loss as a rate *and* a burst length. This is why.

Lab 06 checks the formulas by simulating the hour. With its default seed, independent 5% loss and three copies lose 23 inputs against the formula's 27, and bursty loss loses 2,702 against 2,700. The small gap in the first case is chance. At 27 expected losses, a spread of 5 either way is normal.

### Delay: where redundancy wins

Losses are only half the story. The other half is *when* the rescued input arrives. Take `Δ = 16.7 ms` and `RTT = 100 ms`, and suppose one packet is lost.

| Method | Extra delay for the input in the lost packet |
|---|---|
| Redundancy, `k ≥ 2` | `Δ` = 16.7 ms (the next packet has a copy) |
| Ack and resend | at least `Δ + RTT` = 116.7 ms |

The server simulates inputs tick by tick. An input 16.7 ms late usually still makes its tick, because servers keep a small buffer of incoming inputs. An input 117 ms late has missed seven ticks. The server has already simulated those ticks without it, and the client's prediction will be corrected (week 9). For inputs, redundancy's speed matters more than resend's certainty.

For a chat line, the reverse holds. A chat line 117 ms late is fine. A chat line sent three times in advance, every time, wastes bytes on a message that almost always arrived the first time.

### Move it yourself

Open `examples/w06-redundant-inputs.html`. The top row shows packets over three seconds, with lost ones crossed out. Below it, one small row per input shows its `k` copies, and colors the first copy that got through. Inputs with no surviving copy turn red. The number panel counts lost inputs, the average extra delay and the upload. Start at 5% loss, `k = 3`, independent, and count the red inputs (usually none on screen). Then slide `q` from 0.05 to 0.5 with the same 5% loss. The crosses bunch into pairs and triples, and red inputs appear. Switch to "ack and resend" and watch every input arrive, with the rescued ones about 117 ms late.

### Same idea elsewhere

**Starsiege: Tribes and Tribes 2 (1998, 2001).** Moves sent until acknowledged, then three times each. In our model, the first design was `k` growing with loss, which had no upper bound on bytes. The second fixed `k = 3` and accepted `p^3`. The negative feedback loop is the bandwidth column of our table running away. When loss makes packets bigger, bigger packets cause more loss.

**Quake III Arena (1999; ioquake3 source, current).** `cl_packetdup` default 1, so `k = 2`, adjustable from 1 to 6 copies. Up to 32 commands fit in one packet. Handing players the knob is a design choice in itself. A player on bad Wi-Fi can trade a little upload for fewer lost inputs.

**Fiedler's reliable messages (2016).** Fiedler's later scheme blends the two methods. A reliable message goes into outgoing packets until an ack confirms it, but is only included again if it has not been sent in the last 0.1 seconds and there is room. That is redundancy with a rate limit, so it cannot run away the way the first Tribes design did.

**RakNet (Minecraft: Bedrock Edition and many others).** `RELIABLE` resends until acknowledged. `UNRELIABLE_SEQUENCED` is Tribes' "most recent state." A game using RakNet picks a class per message, which is exactly the per-message decision week 1 asked you to make.

Four systems, one model. For any message type, ask what losing it costs, what a delay of `Δ` costs, and what a delay of `RTT` costs. Then pick redundancy, resend, both or neither.

### Design judgment

- **Inputs: redundancy, with a fixed `k`.** Two to four copies is common. Fix `k` or cap the bytes. Never let packet size grow with loss, or you rebuild the first Tribes loop.
- **Must-arrive events: ack and resend.** Item pickups, chat, purchases, "you died". They are rare, and a delay of one round trip is acceptable.
- **State: neither.** Positions and health bars are replaced every snapshot. Resending an old position is worse than useless. Throw away anything older than what you already have (sequenced).
- **Measure burstiness before you trust `p^k`.** If `q` is high, consecutive copies share the same fate. Space the copies out (packets `i`, `i + 2`, `i + 4`), or fall back to resend for anything that must arrive.
- **Budget the header.** Our 8 bytes of sequence and acks ride on every packet. At 60 Hz that is 3.8 kbit/s before any game data. Week 13 adds it to the full budget.

### Check this example

1. A mobile game sees 3% independent loss. How many copies of each input keep losses below 1 per hour at 30 inputs per second?
2. Measured loss is 3% with `q = 0.4`. With the `k` from question 1, how many inputs are lost per hour?
3. At `Δ = 33.3 ms` and `RTT = 180 ms`, how late is an input rescued by redundancy, and how late by resend? How many server ticks at 30 Hz does the resent input miss?

<details>
<summary>Answers</summary>

1. 108,000 inputs per hour. `k = 3`: `0.03^3 × 108,000 = 2.9`. `k = 4`: `0.03^4 × 108,000 = 0.087`. So 4 copies.
2. `0.03 × 0.4^3 × 108,000 = 207` per hour. Bursty loss undoes most of the benefit. Spacing the copies or adding resend is needed.
3. Redundancy: `Δ` = 33.3 ms. Resend: at least `33.3 + 180 = 213.3` ms, which is 6.4 ticks, so the input misses at least 6 ticks.

</details>

## 3. Ordered channels bring the stall back

Suppose you put chat and inventory updates on one `RELIABLE_ORDERED` channel. A chat message is lost. Every inventory update sent after it arrives and then waits, because ordering says it cannot be delivered before the chat message. You have rebuilt week 1's head-of-line blocking inside your own protocol. The stall is the same `Δ + RTT` or longer.

The fix is the same one QUIC uses. Give each independent stream of ordered messages its own **channel**, with its own ordering. Chat waits only for chat. Inventory waits only for inventory. Better still, ask whether a stream needs ordering at all. Two "item picked up" events for different items can arrive in any order. Only events that change the same thing need an order.

A rule of thumb from the week 1 table:

| Message | Class | Channel |
|---|---|---|
| Movement input | Redundant, `k = 3` | none (in every packet) |
| Positions and health | Unreliable, sequenced | per entity |
| Chat | Reliable, ordered | chat |
| Inventory changes | Reliable, ordered | inventory |
| Fire and ability use | Reliable, sent redundantly as well | none |
| Sound cues | Unreliable | none |

## 4. Do not flood the link

Reliability has a failure mode that TCP handles for you and UDP does not. If the link is overloaded, every message you add makes loss worse, and resends add more messages. TCP's congestion control slows the sender down. On UDP you do it yourself.

Two shipped approaches:

- **Let the receiver set the rate.** In Tribes, each side told the other what packet rate and size it could take. A client on a 28.8 kbit/s modem might ask for 10 packets per second of 200 bytes, about 2 KB per second. The server also capped its own sending per client.
- **Back off when round trips grow.** Fiedler's 2008 article smooths the RTT (each new sample moves the estimate 10% of the way) and switches from 30 to 10 packets per second when it passes a threshold such as 250 ms. It returns to 30 after conditions stay good for a set time, and doubles that time (up to 60 seconds) whenever it has to drop back within 10 seconds, so a flaky link does not flip back and forth.

Both come down to one idea. Rising latency is a sign of queues filling (week 2), and the kind response is to send less before packets start to drop.

## In-class activity (25 minutes)

Groups of three. Each group gets a game brief and a measured connection. Examples: "fighting game, 60 Hz, 2% loss, `q = 0.3`, RTT 70 ms"; "MMO, 10 Hz, 1% loss, `q = 0.6`, RTT 150 ms"; "battle royale, 30 Hz, 4% loss, `q = 0.2`, RTT 90 ms".

1. List the game's message types (at least six). Put each in a delivery class and a channel.
2. For inputs, choose `k`. Compute lost inputs per hour under independent loss and under the measured `q`, and the upload.
3. For one reliable message type, compute its delay after one loss.
4. Present your table in two minutes. The other groups challenge one choice with a number.

Expected output: a message table with class and channel, the two lost-per-hour figures, the upload, the resend delay, and one challenged choice with the result.

## Common misconceptions

- **"Reliable UDP means rebuilding TCP."** It means rebuilding only what each message needs. Most game traffic is unreliable and sequenced, a small part is redundant, and a smaller part is resent.
- **"Three copies means three times the bandwidth."** Only the input bytes triple. The 36 bytes of headers are paid once. In section 2 the third copy added 4 bytes to a 44-byte packet.
- **"At 5% loss, three copies lose 1 in 8,000."** Only if losses are independent. With bursts of two on average, they lose 1 in 80.
- **"Sequence numbers must be 32 bits to be safe."** Sixteen bits are enough if you compare them with wraparound, as long as nothing arrives more than half a lap late (about 9 minutes at 60 Hz).

## Check yourself

1. Is 100 newer than 65,000 under `seq_greater_than`? Is 30,000 newer than 100?
2. The receiver got packets 10, 11, 13 and 14. Write `ack` and `ack_bits` in binary for bits 0 to 3.
3. At 10% independent loss, how many copies make an input's loss rate below 1 in 100,000?
4. A designer puts every reliable message on one ordered channel "to keep it simple." A loss hits a chat message at RTT 120 ms and `Δ` 50 ms. How long are inventory updates held up, at least?
5. Explain the Tribes negative feedback loop with the bandwidth formula from section 2.

<details>
<summary>Answers</summary>

1. 100 against 65,000: `100 < 65,000` and `65,000 − 100 = 64,900 > 32,768`, so yes, 100 is newer (it has wrapped). 30,000 against 100: `30,000 > 100` and the difference 29,900 is at most 32,768, so yes.
2. `ack = 14`. Bit 0 is packet 13 (1), bit 1 is 12 (0), bit 2 is 11 (1), bit 3 is 10 (1). Reading bit 3 down to bit 0, `ack_bits` ends in `1101`.
3. `0.1^k < 10^-5` needs `k = 6`, since `0.1^5` is exactly `10^-5`, not below it.
4. At least `Δ + RTT = 170 ms`, the time for the sender to learn of the loss and get a resend across. Every inventory update sent in that window waits.
5. Packet size was `28 + 8 + 4k` with `k` equal to the number of unacknowledged moves. Loss meant fewer acks, so `k` grew, so packets grew. On a link near its limit, bigger packets raised the loss rate, which made `k` grow again. Fixing `k = 3` breaks the loop, because packet size no longer depends on loss.

</details>

## Lab / assignment hook

[Lab 06, acks and copies](../labs/lab06.md). You write `seq_greater_than`, an ack tracker with a 32-bit ack field and a redundant-input simulator, reproduce the tables in section 2 by formula and by simulating an hour of packets, then find the `k` your own measured connection from Lab 02 needs. Deliverable: your code, the outputs, and a one-page delivery-class table for the game you designed in Lab 04 or 05.

## Sources

- Frohnmayer, M. & Gift, T. (undated). "The TRIBES Engine Networking Model." Dynamix. The paper carries no date or venue; its abstract says the model "is being developed for TRIBES II", so it was written after December 1998 and before *Tribes 2* shipped. Copy at https://www.gamedevs.org/uploads/tribes-networking-model.pdf. The four data classes (non-guaranteed, guaranteed, most recent state, guaranteed quickest). Moves collected every 32 ms and sent three times in consecutive packets in the Tribes 2 design. The earlier *Starsiege: Tribes* scheme of sending every move in the window, and the negative feedback loop on low-bandwidth links. Per-connection packet rate and size, with the example of 10 packets per second of 200 bytes on a 28.8 modem.
- id Software, *Quake III Arena* client code as maintained in ioquake3, `code/client/cl_input.c`, `code/client/cl_main.c` and `code/qcommon/qcommon.h` (GitHub ioquake/ioq3, main branch, accessed September 2026). `cl_packetdup` default 1, clamped to 0 to 5. Commands resent from `cl_packetdup` packets back. `MAX_PACKET_USERCMDS` 32.
- Fiedler, G. (2008). "Reliability and Congestion Avoidance over UDP." *Gaffer on Games*, 20 October 2008. 16-bit `sequence_greater_than` with wraparound. `ack` plus a 32-bit ack bitfield confirming 33 packets. Never resending a packet with the same sequence number. Congestion avoidance at 30 and 10 packets per second, a 250 ms RTT threshold, 10% RTT smoothing, and the doubling recovery timer up to 60 seconds.
- Fiedler, G. (2016). "Reliable Ordered Messages." *Gaffer on Games*, 15 September 2016. Messages included in packets until acked, and only if not sent in the last 0.1 seconds.
- RakNet, `Source/PacketPriority.h` (GitHub facebookarchive/RakNet, archived repository, accessed September 2026). Reliability types `UNRELIABLE`, `UNRELIABLE_SEQUENCED`, `RELIABLE`, `RELIABLE_ORDERED`, `RELIABLE_SEQUENCED`, with their ordering and dropping rules.
- Minecraft Wiki, "RakNet" (accessed September 2026). *Bedrock Edition* uses RakNet over UDP.
- Iyengar, J. & Thomson, M. (2021). RFC 9000, *QUIC*. Independent streams to avoid head-of-line blocking across streams.

## Interactive spec: examples/w06-redundant-inputs.html

**Insight the visual must make obvious:** each extra copy of an input divides losses by `1/p` when loss is independent, but only by `1/q` when loss is bursty, so the same average loss rate can mean 27 lost inputs an hour or 2,700. Redundancy rescues an input one packet later, while ack-and-resend always delivers but a full round trip later.

**Layout.** A packet lane, an input grid and a number panel, plus a small chart. Under 700 px wide, stack lane, grid, chart, numbers. The lane and grid scroll horizontally inside their own container. No page-level horizontal scroll.

1. **Packet lane.** 180 packets (3 s at 60 Hz) as small squares on a time axis. Lost packets drawn hollow with an X.
2. **Input grid.** For each input `i`, a column of `k` cells at packets `i` to `i + k − 1`. The first surviving copy is filled in the "delivered" color. Copies after it are faded. If no copy survives, the whole column is red. In resend mode, each input has one cell at packet `i`, plus, if lost, a second cell at the packet sent at `iΔ + Δ + RTT` (and again if that is lost), linked by a thin line and labelled with the extra delay.
3. **Chart, "Lost inputs per hour vs copies".** Log y axis from 0.01 to 100,000, x axis `k` from 1 to 6. Two lines, independent `p^k × 216,000` and bursty `p q^(k−1) × 216,000`, with the current `k` marked.
4. **Number panel.** `p`, `q`, mean burst length `1/(1 − q)`, `k`, inputs lost on screen, formula losses per hour for both loss models, mean extra delay of rescued inputs (ms), packet bytes `28 + 8 + 4k`, upload in kbit/s at 60 Hz.

**Controls.**
- Loss `p` slider, 0 to 30%, default 5%.
- Burstiness `q` slider, from `p` (independent) to 0.9, default equal to `p`. A button "Independent" snaps `q` to `p`.
- Copies `k` stepper, 1 to 6, default 3.
- Mode radio: "Redundancy" (default), "Ack and resend", "Both" (redundant copies, and resend if all copies are lost).
- RTT slider, 20 to 300 ms, default 100 (used by resend).
- Seed field with a "New pattern" button, so students can see that the same `p` and `q` give different screens.
- All controls reachable by Tab, with visible focus.

**Formulas (match `labs/lab06-starter/reliability.py`).** Loss pattern: `r = p` if `q = p`, else `r = p(1 − q)/(1 − p)`. Packet lost with probability `q` if the previous one was lost, else `r`. Use a small seeded PRNG (mulberry32 or similar; exact sequence need not match Python). Input `i` is lost under redundancy if packets `i..i+k−1` are all lost. Formula losses per hour `216,000 × p^k` or `216,000 × p × q^(k−1)`. Extra delay of copy `j` is `j × 16.7 ms`. Resend delay `Δ + RTT` per failed attempt. Packet bytes `28 + 8 + 4k`, upload `bytes × 60 × 8 / 1000` kbit/s.

**Test values** (assert on load, formula only):
- `p = 0.05`, independent: `k = 1` 10,800 per hour, `k = 2` 540, `k = 3` 27, `k = 4` 1.35.
- `p = 0.05`, `q = 0.5`: `k = 1` 10,800, `k = 2` 5,400, `k = 3` 2,700, `k = 4` 1,350.
- `p = 0.01`, `k = 3`: 0.216 per hour.
- Packet bytes: `k = 1` 40 (19.2 kbit/s), `k = 3` 48 (23.04 kbit/s).
- Resend delay at `Δ = 16.7`, RTT 100: 116.7 ms.

**First screen:** redundancy, `p = 5%`, `q = 0.5`, `k = 3`, with red columns visible in the grid and the chart showing both lines with the gap at `k = 3` labelled "27 vs 2,700 per hour". Caption: "Same 5% loss. Independent: 27 inputs lost an hour. In bursts: 2,700."
