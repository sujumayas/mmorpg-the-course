# CS202 · Week 01 — Networks for game devs: TCP vs UDP

**Why this matters:** The first decision in any multiplayer game is which transport carries your packets, and it is hard to undo later. Pick TCP for a fast action game and one lost packet freezes every update behind it. Pick UDP for everything and you must rebuild the guarantees TCP gave you for free. This week gives you a model that predicts, in milliseconds, what each choice costs.

**You will be able to:**
- Compute the header overhead of a game packet over UDP and TCP, and the bandwidth it costs at a given send rate.
- Derive the delivery gap that one lost packet causes over TCP and over UDP, from send rate and round-trip time.
- Write a UDP sender and receiver, and a length-prefixed message protocol over TCP, in Python.
- Decide, message type by message type, which transport a game should use, and defend the choice with numbers.

**Before class:** Glenn Fiedler, "UDP vs. TCP" (Gaffer on Games, October 2008, the first article of *Networking for Game Programmers*). Gabriel Gambetta, *Fast-Paced Multiplayer*, part I, "Client-Server Game Architecture" (short, and it frames the whole course).

**Prerequisites from earlier courses:** [CS101 week 3, the game loop](../../CS101-programming-for-games-i/lectures/w03-loops-and-the-game-loop.md) (a loop that runs at a fixed rate is where a "send rate" comes from). [CS102 week 5, arrays, linked lists and hash maps](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w05-arrays-linked-lists-and-hash-maps.md) (you will buffer packets in a queue and look them up by sequence number). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (every delay formula this week is a straight line in send interval and round-trip time).

**Interactive:** [examples/w01-head-of-line.html](../examples/w01-head-of-line.html). Keep it open during section 3.

---

## 1. What actually travels between two machines

When your game "sends a message," the operating system wraps your bytes in several layers of addressing and hands them to the network card. The unit that crosses the network is a **packet**: a block of bytes with a header that says where it is going.

Three ideas carry the whole course.

- An **IP address** names a machine on the internet (for example `203.0.113.7`). The **Internet Protocol (IP)** moves packets from one address to another, hop by hop through routers. IP makes no promises. A packet can be lost, duplicated, delayed or delivered out of order.
- A **port** is a 16-bit number that names one program on that machine. A server can run a game on one port and a chat service on another.
- A **socket** is the handle your program opens to send and receive through one port. In Python it is `socket.socket(...)`. Everything you write this term goes through sockets.

On top of IP sit the two **transport protocols** you will choose between. **UDP** (User Datagram Protocol) adds ports and a checksum to IP and nothing else. **TCP** (Transmission Control Protocol) adds ports, a connection, sequence numbers, acknowledgements, retransmission and congestion control. Everything this lecture says about their behavior follows from that difference.

### Headers cost bytes

Every packet pays for its headers. An IPv4 header is at least 20 bytes. A UDP header is exactly 8 bytes. A TCP header is at least 20 bytes, and usually more once options such as timestamps are on. So the minimum overhead is:

```
UDP over IPv4: 20 + 8  = 28 bytes per packet
TCP over IPv4: 20 + 20 = 40 bytes per packet (minimum)
```

Game messages are small. Riot Games' network team wrote in 2015 that *League of Legends* sends a steady stream of packets of about 55 bytes, against the 1,500-byte packets that carry most web and video traffic. At game sizes, headers are a large share of what you send. The payloads below are illustrative:

| Payload | UDP packet | UDP overhead | TCP packet (min) | TCP overhead |
|---|---|---|---|---|
| 55 bytes | 83 bytes | 33.7% | 95 bytes | 42.1% |
| 100 bytes | 128 bytes | 21.9% | 140 bytes | 28.6% |
| 300 bytes | 328 bytes | 8.5% | 340 bytes | 11.8% |
| 1,200 bytes | 1,228 bytes | 2.3% | 1,240 bytes | 3.2% |

At 20 packets per second, 28 bytes of UDP header is `28 × 20 = 560` bytes per second, or 4.5 kilobits per second, before you send a single byte of game. That seems small until a server multiplies it by a thousand players. Week 13 turns this into a full bandwidth budget.

Mojang cared enough about this to change *Minecraft: Java Edition*'s protocol in snapshot 23w32a (August 2023, part of the 1.20.2 cycle). Gameplay packets were batched into bigger TCP packets to cut TCP header overhead and total network usage. Batching trades a little delay for fewer headers. Keep that trade in mind, because section 4 shows TCP doing the same thing on its own.

### How big can one packet be?

The largest packet a link carries in one piece is its **MTU** (maximum transmission unit). Ethernet's is 1,500 bytes, which is why that number keeps appearing. A path's MTU is the smallest MTU of any link on it, and you usually do not know it. IPv6 guarantees every link carries at least 1,280 bytes. A simple rule that never fails is to keep every game packet, headers included, at or below 1,280 bytes. Bigger packets may be split into fragments, and if any fragment is lost, the whole packet is lost.

## 2. Two contracts

Think of each transport as a contract between your game and the operating system.

| | TCP | UDP |
|---|---|---|
| Setup | A handshake before any data (one round trip) | None. Send whenever you like |
| Unit you read | A **byte stream**. Message boundaries are not kept | A **datagram**. One send is one receive, or nothing |
| Loss | Lost data is resent until it arrives | Lost data is gone |
| Order | Bytes arrive in the order sent | Datagrams may arrive in any order |
| Duplicates | Removed | Possible |
| Pacing | Congestion control slows you when the network is busy | None. You pace yourself |
| Small writes | May be held and merged (Nagle's algorithm, section 4) | Sent immediately |

Neither is "fast" or "slow" on a clean network. On a network with no loss, a TCP segment and a UDP datagram of the same size take the same time to cross it. The difference shows up only when something goes wrong, and on the internet something is always going wrong for someone.

### UDP in twelve lines

Here is the smallest useful UDP program. [Lab 01's starter](../labs/lab01.md) has it as `udp_hello.py`, with the server and client in separate processes. Here both ends share one script so you can run it as shown.

```python
import socket

srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # SOCK_DGRAM means UDP
srv.bind(("127.0.0.1", 40001))
cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cli.sendto(b"seq=0", ("127.0.0.1", 40001))   # client: one datagram, no connection
data, addr = srv.recvfrom(2048)       # server: one call returns exactly one datagram
srv.sendto(data, addr)                # server: echo it to whoever sent it
reply, _ = cli.recvfrom(2048)         # client: the echo
print(reply)                          # b'seq=0'
```

There is no `connect`, no `listen`, no `accept`. The server does not know a client exists until a datagram arrives. That is simple, and it also means everything a game needs beyond "maybe deliver this" is your job.

### The TCP trap: a stream has no messages

TCP hands you a stream of bytes, not a list of messages. If a client writes `MOVE 10 4`, then `CAST fireball`, then `CHAT gg`, the server's next `recv()` may return all three glued together, or half of the first one. On a test machine it usually looks fine. Under load it breaks. The Lab 01 demo shows it on your own laptop:

```
one recv() returned 29 bytes: b'MOVE 10 4CAST fireballCHAT gg'
```

The standard fix is **framing**: put the length of each message in front of it, and read exactly that many bytes. A 2-byte length prefix allows messages up to 65,535 bytes.

```python
import struct

def send_msg(sock, payload):
    sock.sendall(struct.pack("!H", len(payload)) + payload)   # !H = 2-byte big-endian length

def recv_msg(sock):
    (n,) = struct.unpack("!H", recv_exact(sock, 2))
    return recv_exact(sock, n)                                # loop on recv() until n bytes
```

You will write `recv_exact` in the lab. UDP does not need framing, because every datagram is already one message.

## 3. Worked example: one lost packet, two protocols

### The hook

On 8 January 2008, *World of Warcraft* patch 2.3.2 listed one line under its general changes. Network latency was reduced by disabling the Nagle algorithm. Nagle's algorithm only exists in TCP, so the note tells you something most players never think about. WoW's game traffic runs over TCP. Community server emulators built to talk to the WoW client, such as TrinityCore for the 3.3.5a client, accept it on a TCP port and expose the same Nagle switch in their config.

Now compare *Counter-Strike*-style shooters on Valve's Source engine. Valve's own documentation sets the client's default snapshot rate at 20 per second and its default interpolation delay at 100 milliseconds. Its stated reason is that even if one snapshot is lost, the client still has two valid snapshots to draw between. That design only makes sense on a transport where snapshots can be lost and the game keeps going without them.

Both games work. One accepts TCP and tunes it. The other designs around loss. The model below tells you why a tab-target MMO can live with TCP and a shooter cannot.

### The model

A game sends a state update every `Δ` milliseconds. Packets take `d` milliseconds one way, so the round-trip time is `RTT = 2d`. Packet `k` is lost. Every other packet arrives.

- `Δ` is the send interval. At a send rate of `f` updates per second, `Δ = 1000 / f`.
- `RTT` is the round-trip time, the time for a packet to go and a reply to come back.
- `RTO` is TCP's retransmission timeout, how long TCP waits for an acknowledgement before it resends.

**Over UDP**, packet `k` never arrives. Packet `k − 1` arrives at time `(k − 1)Δ + d` and packet `k + 1` at `(k + 1)Δ + d`. The game waits

```
UDP gap = 2Δ
```

between updates, instead of the usual `Δ`. Because each update carries the full current state, the next one replaces the lost one. Nothing is waiting for it.

**Over TCP**, the receiver must deliver bytes in order, so packets `k + 1, k + 2, ...` sit in a buffer until `k` is resent and arrives. TCP learns that `k` is missing in one of two ways.

1. **Fast retransmit.** Each packet that arrives after the gap makes the receiver repeat its last acknowledgement. After three such **duplicate ACKs**, the sender resends `k` right away. The third duplicate is triggered by packet `k + 3`, which arrives at `(k + 3)Δ + d`. Its ACK reaches the sender `d` later, and the resent packet arrives `d` after that, at `(k + 3)Δ + 3d`.
2. **Timeout.** If the sender does not send three more packets soon enough, it waits for the RTO instead. RFC 6298 recommends an RTO of at least 1 second. Linux uses a lower floor. It sets the RTO to the smoothed RTT plus a variance term that is never below 200 ms, so on a steady link `RTO ≈ RTT + 200 ms`.

Take the earlier of the two. Everything delivered after the gap comes out in one burst when `k` arrives. The gap the game sees, from the delivery of `k − 1` to the burst, is:

```
TCP gap (fast retransmit) = 4Δ + RTT          when 3Δ + RTT < RTO
TCP gap (timeout)         = Δ + RTO
```

That is the whole idea of **head-of-line blocking**: one missing packet at the head of the line holds up every packet behind it, even though they already arrived.

This is a teaching model. It assumes a fixed delay, that the receiver acknowledges every packet at once, and that the resent packet gets through. Real stacks add delayed ACKs, selective acknowledgements and newer loss detection (RACK). Those change the constants. They do not remove the stall, because an in-order stream cannot deliver byte `n + 1` before byte `n`.

### Numbers you can check

Take one loss at packet 10, and use `RTO = RTT + 200`.

| Send rate | RTT | Normal gap `Δ` | UDP gap `2Δ` | TCP gap | TCP ÷ UDP |
|---|---|---|---|---|---|
| 20 Hz | 100 ms | 50 ms | 100 ms | 4(50) + 100 = **300 ms** | 3.0× |
| 60 Hz | 100 ms | 16.7 ms | 33.3 ms | 4(16.7) + 100 = **166.7 ms** | 5.0× |
| 20 Hz | 200 ms | 50 ms | 100 ms | 4(50) + 200 = **400 ms** | 4.0× |
| 60 Hz | 200 ms | 16.7 ms | 33.3 ms | 4(16.7) + 200 = **266.7 ms** | 8.0× |
| 30 Hz | 50 ms | 33.3 ms | 66.7 ms | 4(33.3) + 50 = **183.3 ms** | 2.75× |
| 5 Hz | 100 ms | 200 ms | 400 ms | timeout: 200 + 300 = **500 ms** | 1.25× |

Check the first row packet by packet. At 20 Hz with RTT 100 ms, packet `i` is sent at `50i` and arrives at `50i + 50`.

| Packet | Sent (ms) | Arrives (ms) | UDP delivers | TCP delivers |
|---|---|---|---|---|
| 9 | 450 | 500 | 500 | 500 |
| 10 (lost) | 500 | resent, 800 | never | 800 |
| 11 | 550 | 600 | 600 | 800 (waited 200) |
| 12 | 600 | 650 | 650 | 800 (waited 150) |
| 13 | 650 | 700 | 700 | 800 (waited 100) |
| 14 | 700 | 750 | 750 | 800 (waited 50) |
| 15 | 750 | 800 | 800 | 800 |

Packet 13 arrives at 700 ms. Its duplicate ACK is the third, and it reaches the sender at 750. The resend arrives at 800. The UDP game went 100 ms without news. The TCP game went 300 ms, then received the lost packet and the four it had held back, all in the same instant. On screen that is a freeze followed by a jump.

Two patterns in the table matter more than any single number.

- **A faster send rate helps UDP much more than TCP.** Going from 20 Hz to 60 Hz shrinks the UDP gap from 100 to 33 ms. The TCP gap only drops from 300 to 167 ms, because the `RTT` term does not shrink.
- **Distance hurts TCP and not UDP.** Doubling RTT adds 100 ms to every TCP stall. The UDP gap ignores RTT entirely.

### Move it yourself

Open `examples/w01-head-of-line.html`. The top lane shows packets leaving the sender. The two lanes below show when each packet reaches the game, over UDP and over TCP. Click any packet to lose it. With the defaults (20 Hz, 100 ms), the UDP lane shows one missing tick. The TCP lane shows a 300 ms hole and a stack of packets delivered at once. Drag the send rate to 60 Hz and watch the UDP hole close while the TCP hole barely moves. Then drag RTT to 200 ms. Only the TCP lane changes.

### Same idea elsewhere

**World of Warcraft (patch 2.3.2, January 2008, and later).** Tab-target combat sends events such as "cast this spell" and "this unit took damage," and every one must arrive. Losing a damage event is worse than delivering it late. TCP's guarantee is worth its stalls here. What WoW could not accept was extra delay on every packet, which is what Nagle adds (section 4). So it kept TCP and switched Nagle off. In the model, WoW sends event traffic that is not at a fixed `Δ`, so after a loss there are often fewer than three packets in flight. The timeout row of the table applies, and `Δ + RTO` is the cost it accepts.

**Source engine (Valve Developer Community documentation, archived 2024).** Default snapshot rate 20 per second, so `Δ = 50 ms`. Default interpolation delay 100 ms, which is exactly `2Δ`, the UDP gap from our model. Valve sized the client's delay to survive precisely one lost snapshot. Over TCP the same client would need a buffer of `4Δ + RTT`, about 300 ms at RTT 100, and every shot would feel that much later.

**Minecraft (Java and Bedrock, 2026).** *Java Edition* servers listen on TCP port 25565. *Bedrock Edition* servers use UDP on port 19132, through the RakNet library, which adds its own acknowledgements and resends on top of UDP only where the game asks for them. Same game, two transports. Java pays head-of-line stalls on every loss. Bedrock pays for its own reliability layer and gets to choose which messages wait.

**QUIC (RFC 9000, May 2021).** The protocol under HTTP/3 runs over UDP and splits data into independent streams. Its specification names head-of-line blocking as the problem it avoids, since a lost packet blocks only the streams whose data was in it. In our model, that is a separate line per stream. A loss on stream A does not add `4Δ + RTT` to stream B.

Four systems, one model. Whenever you see a network design, ask two questions. Does a lost packet block anything behind it? If so, how many `Δ` and how many `RTT` does the stall cost?

### Design judgment

- **Use TCP** when every message must arrive, order matters, and a stall of a few hundred milliseconds on a loss is acceptable. Logins, purchases, chat, turn-based moves, lobby traffic, patch downloads and much of a tab-target MMO fit. You get years of tested reliability and congestion control for free. Turn Nagle off.
- **Use UDP** when newer data replaces older data (positions, aim, snapshots) or when a stall is worse than a gap. You must then write, or adopt, the pieces you need: sequence numbers, acks for the few messages that must arrive, and pacing. Weeks 5 to 7 build these.
- **Do not reach for "both" by reflex.** Running TCP and UDP side by side sounds like the best of each. Fiedler warns it costs you control, and that TCP's congestion behavior can raise loss for the UDP traffic sharing the link. Most shipped action games put everything on UDP with a small reliability layer.
- **Decide deliberately what "lost" means for each message.** A position update that arrives late is useless. A "you received a legendary item" message that arrives late is fine and one that never arrives is a support ticket. The transport choice follows from that, not from genre habit.

### Check this example

1. A game sends at 30 Hz to a server 160 ms RTT away. One packet is lost. What gap does the game see over UDP and over TCP (use `RTO = RTT + 200`)?
2. A designer proposes raising the send rate from 20 Hz to 60 Hz "to fix TCP stalls" at RTT 150 ms. Compute the stall before and after. Was it worth tripling the packets?
3. An MMO sends a combat event only when something happens, about 2 per second, at RTT 80 ms. Which formula applies after a loss, and what is the gap?

<details>
<summary>Answers</summary>

1. `Δ = 33.3 ms`. UDP gap `2Δ = 66.7 ms`. TCP: `3Δ + RTT = 260 ms` is less than `RTO = 360 ms`, so fast retransmit applies, and the gap is `4Δ + RTT = 133.3 + 160 = 293.3 ms`.
2. At 20 Hz, `4(50) + 150 = 350 ms`. At 60 Hz, `4(16.7) + 150 = 216.7 ms`. Three times the packets bought a 38% shorter stall. The same change over UDP would cut the gap from 100 ms to 33 ms, 67% shorter.
3. `Δ = 500 ms`, so fast retransmit needs `3Δ + RTT = 1,580 ms`, longer than `RTO = 280 ms`. The timeout applies. The gap is `Δ + RTO = 500 + 280 = 780 ms`. On sparse traffic, loss costs a full timeout.

</details>

## 4. Nagle's algorithm: TCP's own batching

In 1984 John Nagle described a problem he saw on early networks (RFC 896). Programs such as remote terminals sent one keystroke per packet, 1 byte of data behind 40 bytes of header. His fix, now on by default in almost every TCP stack, is simple. If you have sent data that has not yet been acknowledged, hold any new small writes and merge them until the acknowledgement comes back or a full packet's worth has built up.

For a keystroke terminal on a slow link, that is a large bandwidth saving. For a game, it adds up to one round trip of delay to any small write that follows another. It gets worse when combined with **delayed ACKs**, a separate TCP feature where the receiver waits briefly before acknowledging in the hope of piggybacking the ACK on a reply. The two features can wait on each other, and the stall can reach the delayed-ACK limit, which can be as long as 500 ms.

Games turn it off with one socket option:

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # a TCP socket
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)        # Nagle off
print(sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY) != 0)   # True
```

That is what WoW did in patch 2.3.2. In patch 4.1.0 (April 2011) Blizzard moved the switch into the options screen as "Optimize network for speed," on by default. The patch notes explain the trade honestly. The setting sends packets more often, uses more bandwidth, and players with limited bandwidth who kept disconnecting should try turning it off. That one checkbox is the whole of section 1 and section 4 in a sentence. Fewer, bigger packets save header bytes. More, smaller packets save milliseconds. Mojang made the opposite choice for *Minecraft: Java Edition* in 2023, batching to save bandwidth. Both are correct for their players. What matters is that each team chose on purpose.

## 5. Choose per message, not per game

A real game sends many kinds of messages, and they want different contracts. Sort them by two questions. Must it arrive? Does newer data replace it?

| Message | Must arrive? | Replaced by newer? | Fits |
|---|---|---|---|
| Login, account, purchase | Yes | No | TCP, or a separate HTTPS service |
| Player position, aim, velocity | No | Yes | Unreliable UDP, sent every tick |
| "Fire weapon" input | Yes, quickly | No | Reliable on UDP, or resent in the next few packets |
| Chat line | Yes | No | Reliable, order matters per channel |
| Voice | No | Yes (late audio is useless) | Unreliable UDP with a jitter buffer (week 2) |
| Door opened, item picked up | Yes | Sometimes (state can be resent) | Reliable, or included in snapshots |

Notice the "fire weapon" row. It must arrive, and it must arrive fast. TCP gives you the first and not the second. A common UDP trick is to send each input in several consecutive packets, so one loss costs nothing. Week 6 builds this "redundant input" scheme with numbers.

## In-class activity (25 minutes)

Pairs. Your team is building a four-player co-op dungeon crawler with real-time melee combat, loot drops, a trade window and text chat.

1. List every message type your game sends (aim for eight to ten). For each, answer the two questions from section 5.
2. For player movement, choose a send rate. Using the model, compute the UDP gap and the TCP gap after one loss at RTT 60 ms and at RTT 180 ms.
3. Decide the transport for each message type. If you choose UDP for anything that must arrive, say how you will make sure it does.
4. Swap with another pair. Find the one message whose choice you most disagree with, and settle it with a number from the model.

Expected output: a table of message types with the two answers and the chosen transport, the four gap values from step 2, and one sentence recording the disagreement and how the number settled it.

## Common misconceptions

- **"UDP is faster than TCP."** On a clean network they take the same time. UDP avoids the stall after a loss and the one-round-trip handshake. That is where the "speed" comes from.
- **"TCP is reliable, so my messages arrive as I sent them."** Your bytes arrive in order. Your message boundaries do not. Frame every message.
- **"Turning on TCP_NODELAY removes head-of-line blocking."** It removes Nagle's batching delay only. A lost packet still blocks everything behind it.
- **"A higher tick rate fixes TCP stalls."** It shrinks the `4Δ` part. The `RTT` part stays, and on long routes it dominates.

## Check yourself

1. A 70-byte payload is sent 30 times per second. How many bytes per second of headers does that cost over UDP/IPv4 and over TCP/IPv4 (minimum headers)? What fraction of the traffic is header in each case?
2. Over UDP at 20 Hz, two consecutive packets are lost. What gap does the game see? Over TCP at 20 Hz and RTT 100 ms, the same two packets are lost. Use the Lab 01 model to find the gap.
3. A player in São Paulo connects to a server with RTT 190 ms. The game sends at 64 Hz. Compute both gaps for one loss, then decide whether a 100 ms interpolation buffer (like Source's default) would hide the loss under each transport.
4. Explain, using the model, why QUIC does not suffer head-of-line blocking between two streams but does within one stream.
5. You receive `b'\x00\x05HELLO\x00\x02GG'` on a TCP socket that uses the 2-byte length prefix from section 2. List the messages.

<details>
<summary>Answers</summary>

1. UDP: `28 × 30 = 840` bytes/s of header. Each packet is 98 bytes, so 28.6% is header. TCP: `40 × 30 = 1,200` bytes/s. Each packet is 110 bytes, so 36.4% is header.
2. UDP: packets `k` and `k + 1` are missing, so the gap is `3Δ = 150 ms`. TCP in the model: packet `k` is resent after `k + 3` arrives and delivered at `(k + 3)50 + 150`. The previous delivery was at `(k − 1)50 + 50`. The gap is 300 ms. Packet `k + 1` is resent after `k + 4` arrives and delivered 50 ms later. The largest gap is 300 ms, and the stall ends 350 ms after `k − 1` was delivered.
3. `Δ = 15.6 ms`. UDP gap `2Δ = 31.3 ms`, well inside 100 ms. TCP: `4Δ + RTT = 62.5 + 190 = 252.5 ms`, far beyond 100 ms. The buffer hides the loss over UDP and not over TCP.
4. Each QUIC stream has its own ordering. A loss holds back only the stream whose data was in the lost packet. Other streams keep delivering, so they see no `4Δ + RTT` stall. Within the stream, bytes are still in order, so its own data waits for the resend, exactly as in TCP.
5. `\x00\x05` is length 5, giving `HELLO`. `\x00\x02` is length 2, giving `GG`. Two messages, `HELLO` and `GG`.

</details>

## Lab / assignment hook

[Lab 01, sockets and the cost of order](../labs/lab01.md). You run a UDP echo on your own machine, see TCP glue three messages together, write length-prefix framing, and finish a head-of-line model whose output must reproduce the table in section 3. Deliverable: your code, the model's output for three scenarios of your choice, and a half-page transport recommendation for the in-class dungeon crawler.

## Sources

- Blizzard Entertainment, *World of Warcraft* patch 2.3.2 notes (released 8 January 2008), as recorded on Warcraft Wiki, "Patch 2.3.2". General change reducing network latency by disabling the Nagle algorithm.
- Blizzard Entertainment, *World of Warcraft* patch 4.1.0 notes (26 April 2011), as recorded on Warcraft Wiki, "Patch 4.1.0". New Network options category with "Optimize network for speed," on by default, sending packets more often at the cost of bandwidth, and advice to players who disconnect.
- TrinityCore, branch 3.3.5, `src/server/worldserver/worldserver.conf.dist` and `src/server/shared/Networking/Socket.h` (GitHub, accessed September 2026). Open-source server emulator for the WoW 3.3.5a client. World server on a TCP port (default 8085) and a `Network.TcpNodelay` setting for Nagle. Evidence of the client's transport, not Blizzard's own code.
- Valve Developer Community, "Source Multiplayer Networking" (archived copy, 2024). Default tick of 15 ms (about 66.7 ticks per second), `cl_updaterate` default 20, default interpolation period 100 ms so that one lost snapshot still leaves two to interpolate between.
- Minecraft Wiki, "Java Edition 23w32a" (snapshot released 9 August 2023). Gameplay packets batched into bigger TCP packets to reduce header overhead. "Bedrock Dedicated Server" and "Server" pages (accessed September 2026). Java uses TCP port 25565, Bedrock uses UDP port 19132. "RakNet" page. Bedrock's RakNet runs over UDP with its own reliability.
- Riot Games Technology blog, "Fixing the Internet for Real Time Applications: Part I" (6 November 2015). *League of Legends* sends a steady stream of packets of about 55 bytes, compared with 1,500-byte bulk packets. Statement that most games send traffic over UDP.
- Fiedler, G. (2008). "UDP vs. TCP." *Gaffer on Games*, 1 October 2008. Why TCP's in-order delivery stalls time-critical data, and the argument against mixing TCP and UDP.
- Gambetta, G. *Fast-Paced Multiplayer*, part I, "Client-Server Game Architecture" (gabrielgambetta.com).
- Postel, J. (1980). RFC 768, *User Datagram Protocol*. 8-byte header. Postel, J. (1981). RFC 791, *Internet Protocol*. Minimum header of 5 words, 20 bytes. Eddy, W. (2022). RFC 9293, *Transmission Control Protocol*. Header format, 20 bytes without options.
- Deering, S. & Hinden, R. (2017). RFC 8200, *IPv6 Specification*. Every link must carry 1,280-byte packets.
- Allman, M., Paxson, V. & Blanton, E. (2009). RFC 5681, *TCP Congestion Control*. Fast retransmit after 3 duplicate ACKs. Paxson, V. et al. (2011). RFC 6298, *Computing TCP's Retransmission Timer*. RTO rounded up to at least 1 second.
- Linux kernel source, `include/net/tcp.h` (`TCP_RTO_MIN` = HZ/5, 200 ms) and `net/ipv4/tcp_input.c` (RTO = smoothed RTT + rttvar, rttvar floored at the minimum), mainline as of September 2026.
- Nagle, J. (1984). RFC 896, *Congestion Control in IP/TCP Internetworks*, 6 January 1984. Wikipedia, "Nagle's algorithm" (accessed September 2026), for the interaction with delayed ACKs and the 500 ms upper bound.
- Iyengar, J. & Thomson, M. (2021). RFC 9000, *QUIC: A UDP-Based Multiplexed and Secure Transport*, May 2021. Section on stream multiplexing and head-of-line blocking.

## Interactive spec: examples/w01-head-of-line.html

**Insight the visual must make obvious:** one lost packet costs UDP one missing tick, while TCP freezes every later packet until the resend arrives and then delivers them in a burst. Raising the send rate shrinks the UDP hole almost to nothing but leaves most of the TCP hole, because the TCP hole contains a full round trip.

**Layout.** Three horizontal lanes on a shared time axis (0 to 1,200 ms, auto-extended if needed), plus a number panel. On screens under 700 px wide, the panel sits below the lanes and the time axis scrolls inside its own container (no page overflow).

1. **Sender lane.** One small square per packet at its send time `iΔ`, labelled with `i`. The lost packet is drawn hollow with a red X. For TCP, draw the resend as a second marker at its resend time (`(k + 3)Δ + 2d` or `kΔ + RTO`), with a thin arrow to its arrival.
2. **UDP delivery lane.** Each delivered packet at `iΔ + d`. The lost packet leaves an empty slot. Shade the gap between the delivery before and after the loss, labelled with its length in ms.
3. **TCP delivery lane.** Each packet at its delivery time, `max(arrival_i, delivery_{i−1})`. Packets that waited are stacked vertically at the burst time and drawn with a line back to their original arrival time, labelled "waited N ms". Shade the gap and label it.
4. **Number panel.** `Δ`, `d`, `RTO`, which TCP path fired (fast retransmit or timeout), UDP gap, TCP gap, TCP ÷ UDP, and the count of packets delivered in the TCP burst.

**Controls.**
- Send rate slider, 5 to 128 Hz, default 20. Show `Δ` beside it.
- RTT slider, 10 to 400 ms, default 100.
- RTO mode radio: "Linux-like (RTT + 200 ms)" (default), "RFC 6298 minimum (1,000 ms)", "Custom" with a numeric field.
- Click or press Enter/Space on any packet in the sender lane to toggle it lost. Default: packet 10 lost, 20 packets shown. Allow up to 3 lost packets.
- Button "Reset".
- All controls reachable by Tab, with visible focus.

**Formulas.** `Δ = 1000 / f`, `d = RTT / 2`. Not lost: `arrival_i = iΔ + d`. Lost (one resend, which always arrives): `fast = (i + 3)Δ + 3d` if `i + 3 < n`, else infinity. `timeout = iΔ + RTO + d`. `arrival_i = min(fast, timeout)`. TCP `delivery_0 = arrival_0`, `delivery_i = max(arrival_i, delivery_{i−1})`. UDP delivery is `arrival_i` for packets not lost. Gap = largest difference between consecutive delivery times. This is exactly `labs/lab01-starter/hol_sim.py`.

**Test values** (assert on load, with packet 10 lost, n = 20, RTO = RTT + 200):
- 20 Hz, RTT 100: UDP gap 100.0, TCP gap 300.0, fast retransmit, burst of 5 packets (10 to 14).
- 60 Hz, RTT 100: UDP 33.3, TCP 166.7.
- 20 Hz, RTT 200: UDP 100.0, TCP 400.0.
- 5 Hz, RTT 100: UDP 400.0, TCP 500.0, timeout path.
- 20 Hz, RTT 100, RTO fixed at 1,000 ms: fast retransmit still fires first, TCP 300.0.

**First screen:** 20 Hz, RTT 100 ms, packet 10 lost, with both gaps shaded and labelled "UDP 100 ms" and "TCP 300 ms". One caption line: "Same loss. UDP skips one update. TCP freezes for 300 ms, then delivers five at once."
