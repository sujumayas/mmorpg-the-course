# CS202 · Week 03 — Topologies: peer-to-peer, client-server, relay

**Why this matters:** Before you write a line of netcode you decide who sends packets to whom. That one decision sets whose internet connection pays the bandwidth, how many milliseconds an action takes to reach every other player, who can cheat, and what happens when someone's router hangs up. Studios have shipped with one topology and then paid to switch. This week gives you the arithmetic to choose on paper first.

**You will be able to:**
- Compute per-machine upload and download for full-mesh peer-to-peer, dedicated server and listen server, from player count, send rate, state size and header size.
- Compute the one-way latency for every pair of players under each topology from a latency matrix, and find the worst pair.
- Explain why a relay can be faster than a direct connection, using a latency matrix that breaks the triangle inequality.
- Recommend a topology for a given game and defend it on bandwidth, latency, cost, cheating and failure.

**Before class:** Bettner, P. & Terrano, M. (2001), "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond" (Gamasutra, now Game Developer), the sections on the design goals, simultaneous simulations and peer topology. Steamworks documentation, "Steam Datagram Relay", the first two paragraphs.

**Prerequisites from earlier courses:** [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (the server's upload grows as `O(n²)`, and you will see the wall). [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (the lab reads its scenario from JSON). [CS202 week 1](w01-networks-for-game-devs-tcp-vs-udp.md) (28-byte UDP/IPv4 header) and [week 2](w02-latency-jitter-loss-measure-your-own.md) (one-way latency, routing detours).

**Interactive:** [examples/w03-topology-explorer.html](../examples/w03-topology-explorer.html). Keep it open during section 2.

---

## 1. Who talks to whom

A **topology** is the pattern of connections between the machines in a match. Four patterns cover almost every shipped game.

- **Peer-to-peer (full mesh).** Every player's machine, a **peer**, sends directly to every other peer. There is no machine in the middle. With `n` players there are `n(n − 1)/2` connections.
- **Dedicated server (client-server).** Every player's machine, a **client**, talks only to one **server**, a machine the developer runs in a data center. Clients never talk to each other. With `n` players there are `n` connections.
- **Listen server (player-hosted).** Client-server, but the server runs inside one player's game, the **host**. The host is a client and the server at once. Everyone else connects to the host.
- **Relay.** A machine in the middle that only forwards packets. It does not run the game. A relay can carry peer-to-peer traffic (every peer sends to the relay, the relay forwards) or client-server traffic (clients reach the server through it).

Keep one distinction clear from the start. Topology says where packets go. **Authority** says which machine decides what is true, for example whether a shot hit. They are separate decisions. A dedicated server is usually authoritative, but a peer-to-peer game can make one peer the authority, or have every peer run the same simulation and agree. Week 4 is about authority. This week is about packets.

### A practical obstacle: NAT

Most home players sit behind a router that performs **network address translation (NAT)**. Many devices share one public IP address, and the router lets packets in only as replies to something a device inside sent first. A server in a data center has a public address that anyone can reach, so clients can always connect out to it. Two players behind NAT cannot simply send to each other, because neither router expects the other's packets. Peer-to-peer games need a technique called **hole punching**, where both peers send to each other at the same moment through a matchmaking service, and it does not work with every router. Ensemble Studios listed exactly this as a weakness of their peer-to-peer design in 2001. Some NAT setups could not be supported at all. Relays solve it, because both peers connect *out* to the relay.

## 2. Worked example: counting bytes and milliseconds

### The hook

In 1997 *Age of Empires* ran eight-player matches with hundreds of units per player over 28.8 kbit/s dial-up modems. Its network ran peer-to-peer, with every machine connected to every other. The designers wrote that if they had sent the position, status, facing and damage of each unit, the modems would have limited them to about 250 moving units in the whole game. Today an eight-player shooter usually runs on a dedicated server in a data center. So why could a 1997 strategy game run on eight home modems with no server, and why would a modern action game not copy it? The answer is two tables of arithmetic.

### The model

**Bandwidth.** There are `n` players. Each sends updates `r` times per second. One player's state is `s` bytes, one client input packet carries `i` bytes, and every packet pays `h` bytes of header (28 for UDP over IPv4, from week 1).

```
Full mesh, each peer:           upload = (n − 1) × r × (s + h)       (download the same)
Dedicated server:               one snapshot to one client = n × s + h
                                client download = r × (n × s + h)
                                client upload   = r × (i + h)
                                server upload   = n × r × (n × s + h)
Listen server, host's uplink:   host upload     = (n − 1) × r × (n × s + h)
```

The server's upload has `n` twice, once for the number of clients and once for the players in each snapshot. That is the `O(n²)` from CS102 week 4, in bytes per second. In a full mesh, *each* peer's cost grows as `O(n)`, but the total over all peers is `O(n²)` as well, spread across everyone's home connections.

**Latency.** Let `d(X, Y)` be the one-way latency between two machines. Player A acts. How long until player B receives it?

```
Full mesh:              d(A, B)
Dedicated server S:     d(A, S) + d(S, B)
Listen server, host H:  d(A, H) + d(H, B)          (0 for the host's own leg)
Relay R:                d(A, R) + d(R, B)
```

The quantity to watch is the **worst pair**, the largest of these over all pairs of players. That pair decides whether the match feels fair.

### Numbers you can check: bandwidth

Take `n = 8`, `r = 20` Hz, `s = 40` bytes, `i = 12` bytes and `h = 28` bytes. To convert bytes per second to kilobits per second, multiply by 8 and divide by 1,000.

| Role | Formula | Bytes/s | kbit/s |
|---|---|---|---|
| Mesh peer, upload | 7 × 20 × 68 | 9,520 | 76.2 |
| Server client, upload | 20 × 40 | 800 | 6.4 |
| Server client, download | 20 × (8 × 40 + 28) = 20 × 348 | 6,960 | 55.7 |
| Dedicated server, upload | 8 × 6,960 | 55,680 | 445.4 |
| Listen host, upload | 7 × 6,960 | 48,720 | 389.8 |

Now grow the match with the same `r`, `s`, `i` and `h`:

| Players `n` | Mesh peer upload | Client download | Dedicated server upload | Listen host upload |
|---|---|---|---|---|
| 2 | 10.9 kbit/s | 17.3 kbit/s | 34.6 kbit/s | 17.3 kbit/s |
| 4 | 32.6 | 30.1 | 120.3 | 90.2 |
| 8 | 76.2 | 55.7 | 445.4 | 389.8 |
| 16 | 163.2 | 106.9 | 1,710 | 1,603 |
| 32 | 337.3 | 209.3 | 6,697 | 6,488 |
| 64 | 685.4 | 414.1 | 26,501 | 26,087 |

Read down the last two columns. Doubling the players roughly quadruples the server's upload. For a data-center machine, 26 Mbit/s is fine. For a player hosting from home, it is not. Home connections usually upload far less than they download, so the listen-server host is the first machine to choke. Meanwhile each client's upload stays at 6.4 kbit/s whatever `n` is, which is why client-server scales to large matches and full mesh does not. Week 13 follows the same growth to 100 players and beyond, and shows how games break the `n²`.

Back to 1997. A 28.8 kbit/s modem carries at most 3,600 bytes per second. The eight-player mesh row needs 9,520 bytes per second of upload, 2.6 times the modem. Even a client of a dedicated server needs 6,960 bytes per second of download. Sending state was never going to work. So *Age of Empires* sent something much smaller than state. Every machine ran the same simulation, and peers exchanged only the **commands** players gave ("these 20 archers attack that building"). Suppose, for illustration, that each peer sends one 12-byte command packet every 200 ms turn, with today's 28-byte header. Its upload is `7 × 5 × 40 = 1,400` bytes per second, 39% of the modem, however many archers are on the map. Week 12 covers this technique, **deterministic lockstep**, and what it costs.

### Numbers you can check: latency

Four players and two candidate server sites. These numbers are invented for the exercise, and they are one-way latencies in milliseconds. A and B live in the same city. C is a few hundred kilometers away. D is farthest. Note one odd value. A and D are 60 ms apart directly, because their providers route traffic between them through a detour, just like the San Francisco to Portland trace in week 2.

| Direct | A | B | C | D |
|---|---|---|---|---|
| A | — | 10 | 35 | 60 |
| B | 10 | — | 30 | 55 |
| C | 35 | 30 | — | 30 |
| D | 60 | 55 | 30 | — |

| To server | A | B | C | D |
|---|---|---|---|---|
| S1 (in A's city) | 5 | 12 | 33 | 58 |
| S2 (central) | 25 | 22 | 12 | 25 |

Apply the formulas to every pair:

| Pair | Mesh | Server S1 | Server S2 | Host A | Host C | Host D |
|---|---|---|---|---|---|---|
| A-B | 10 | 17 | 47 | 10 | 65 | 115 |
| A-C | 35 | 38 | 37 | 35 | 35 | 90 |
| A-D | 60 | 63 | 50 | 60 | 65 | 60 |
| B-C | 30 | 45 | 34 | 45 | 30 | 85 |
| B-D | 55 | 70 | 47 | 70 | 60 | 55 |
| C-D | 30 | 91 | 37 | 95 | 30 | 30 |
| **Worst pair** | **60** | **91** | **50** | **95** | **65** | **115** |

Check two cells by hand. C to D through S1 is `33 + 58 = 91`. B to D through host A is `10 + 60 = 70`.

Four results are worth a sentence each.

- **The mesh is not the fastest.** Its worst pair is 60 ms, because it must use the bad A to D route. The central server S2 does better at 50 ms, even though every packet makes two trips.
- **Server placement matters more than the topology label.** S1 and S2 are both dedicated servers. S1, convenient for A and B, makes the worst pair 91 ms. S2 makes it 50.
- **The host's choice matters most of all.** Hosting at C gives a 65 ms worst pair. Hosting at D gives 115 ms. A matchmaker that picks the host at random picks D one time in four.
- **Round trips are unequal.** Under S1, A's round trip to the server is 10 ms and D's is 116 ms. Under a listen server, the host's own actions reach the server in 0 ms. Week 11 comes back to this **host advantage** when it deals with fairness in hit detection.

### Move it yourself

Open `examples/w03-topology-explorer.html`. Four players sit on a map, and you can drag them and the server. Pick a topology. Lines show which machines send to which, with thickness proportional to bytes per second. Bars under each machine show its upload against a chosen home uplink. A matrix shows every pair's one-way latency, with the worst pair highlighted. Start on "Listen server" with the host at D and watch the worst pair jump to 115 ms. Then raise the player count slider from 4 to 32 and watch the host's upload bar pass the home uplink line while every client's bar stays flat.

### Same idea elsewhere

**Age of Empires (1997, 1999), peer-to-peer mesh.** Ensemble connected every client to every other client. Their paper lists the strengths as lower latency from direct paths and no central point of failure, since the game continues if any player, even the host, disconnects. The weaknesses were more connections to fail and some NAT setups that could not work. In our model, they took the mesh row and shrank `s` from unit state to commands, so the `(n − 1)` cost stayed small.

**Source engine (Valve documentation, archived 2024), dedicated and listen servers.** Valve describes Source multiplayer as client-server and says that usually the server is a dedicated host. The same documentation illustrates lag compensation with a screenshot taken on a listen server, the other mode the engine supports. Same code, two rows of our table. The dedicated row costs Valve or the community a machine. The listen row costs the host's uplink and hands the host a 0 ms leg.

**Minecraft (Java and Bedrock, 2026), every row at once.** Minecraft runs an internal server even in single-player, so single-player and multiplayer share one code path. A player can open that world to others, which makes their game a listen server. Anyone can run the standalone server software as a dedicated server. Mojang also sells Realms, a subscription where Mojang hosts an always-online server. One game lets its players pick a topology by how much they want to pay and whether the host must stay online.

**Steam Datagram Relay (Valve, current Steamworks documentation).** Valve's relay network carries game traffic over its own backbone. Valve lists three effects. Players' and servers' IP addresses stay hidden, which blocks denial-of-service attacks. Traffic is authenticated and rate-limited. And for many players the relayed route is faster than the direct one. It works for peer-to-peer and dedicated-server games alike. In our model, a relay is a server site like S2 that forwards instead of simulating, and S2's 50 ms beat the direct 60 ms for exactly the reason Valve gives.

Four systems, one model. For any network design, write down who sends to whom, compute each machine's upload, and compute the worst pair.

### Design judgment

- **Dedicated servers cost money every hour a match runs.** Peer-to-peer and listen servers cost the developer almost nothing, because players supply the machines and the bandwidth. That is why many console and indie games start there. Budget the server bill before you promise dedicated servers.
- **A player's machine cannot be trusted.** In a mesh or on a listen server, some player's computer is doing the authoritative work, and its owner can modify it. Gambetta's first rule of multiplayer, don't trust the player, is far easier to follow when the authority runs in your data center. Competitive games pay for servers largely for this reason.
- **Somebody leaves.** When a mesh peer drops, the others carry on. When a listen-server host drops, the match ends unless you build **host migration**, moving the server to another player mid-match, which is hard to get right. A dedicated server survives any player leaving.
- **Hosts leak addresses.** In a mesh or listen server, every player learns other players' IP addresses, and some will use them to flood a rival's connection. Relays and dedicated servers hide them.
- **Scale decides for you.** An MMO with thousands of players per world has no choice. Look at the `n = 64` row and imagine `n = 2,000`. Persistent worlds are always client-server, and MMO302 builds the server side.
- **Latency is an empirical question.** Direct is often fastest, and sometimes it is not. Measure your players' real latency matrix (week 2's tools, run from matchmaking) before you assume.

### Check this example

1. With `r = 30`, `s = 24`, `h = 28` and `n = 12`, compute a mesh peer's upload and a listen host's upload in kbit/s.
2. In the latency scenario, add a relay R with one-way latencies A 20, B 18, C 15, D 20, used for peer-to-peer traffic. What is the worst pair? Is it better than S2?
3. The host in a 16-player listen-server game has a 5 Mbit/s uplink. With `r = 20`, `s = 40` and `h = 28`, does it fit? What is the largest `r` that fits?

<details>
<summary>Answers</summary>

1. Mesh: `11 × 30 × 52 = 17,160` B/s, 137.3 kbit/s. Listen host: one snapshot is `12 × 24 + 28 = 316` bytes, so `11 × 30 × 316 = 104,280` B/s, 834.2 kbit/s.
2. Pairs: A-B 38, A-C 35, A-D 40, B-C 33, B-D 38, C-D 35. The worst pair is A-D at 40 ms, better than S2's 50 ms and the mesh's 60 ms.
3. Host upload is `15 × 20 × (16 × 40 + 28) = 15 × 20 × 668 = 200,400` B/s, 1,603 kbit/s, which fits in 5,000 kbit/s. The largest rate is `5,000,000 / 8 / (15 × 668) = 62.4`, so 62 Hz.

</details>

## 3. Relays and the triangle that is not there

In geometry, going from A to D through a third point is never shorter than going straight, the **triangle inequality**. Internet latency does not obey it. Paths are chosen by cost and business agreements between networks, not by distance, so the direct route between two homes can take a long detour while a route through a well-connected data center stays short.

That is the whole business case for a relay network. A relay adds a hop, and the hop costs a little processing time. But if the relay operator owns fast links between its sites, a packet that goes player, nearest relay, relay backbone, other relay, other player can beat the public route. Riot's 2015 series on this problem opens with exactly the gap you saw in week 2, 14 ms expected against 70 ms measured, and the post describes the team Riot set up in response, Riot Direct, whose job is to give players the fastest possible route to Riot's servers. Valve's Steam Datagram Relay does the same for any game that uses it.

Relays also solve two problems from section 1 almost by accident. Both players connect *out* to a relay, so NAT is no obstacle. And players only ever see the relay's address, never each other's.

A relay is still not a server. It does not run the simulation and cannot settle arguments about who hit whom. A relayed peer-to-peer game has the latency and privacy of a good server and the trust problems of peer-to-peer.

## 4. Choosing a topology

Use the model to fill a table like this for your own game. The rows below are typical starting points, not rules.

| Game | Players | Typical choice | Main reason from the model |
|---|---|---|---|
| 1v1 fighting game | 2 | Peer-to-peer, often relayed | Mesh is one connection, and the direct path is the lowest-latency pair |
| Co-op campaign | 2-4 | Listen server | Host upload is small at `n = 4` and servers cost money |
| RTS | 2-8 | Peer-to-peer lockstep | Command traffic is tiny, whatever the unit count |
| Competitive shooter | 10-12 | Dedicated servers | Trust, fairness between pairs, host leaving |
| Battle royale | 60-150 | Dedicated servers | `n²` upload rules out any player host |
| MMO | Thousands per world | Dedicated server clusters | Persistence and scale. See MMO302 |

## In-class activity (25 minutes)

Groups of three. Each group gets a game brief card: "4-player co-op roguelike", "6-player party racing game" or "2v2 arena brawler with ranked play". Each card lists a send rate, a state size and a latency matrix for four players in two regions.

1. Compute upload for a mesh peer, a listen host and a dedicated server, and compare each to a 10 Mbit/s home uplink.
2. Compute the worst pair for mesh, both server sites and the best and worst host.
3. Choose a topology. List one risk the numbers do not show (cheating, cost, host leaving, NAT).
4. Present in 90 seconds. The room votes on whether the risk you named is serious enough to change the choice.

Expected output: the two computed tables, the choice, and the named risk with one mitigation.

## Common misconceptions

- **"Peer-to-peer is always lower latency."** Only if the direct routes are good. A well-placed server or relay can beat a detoured direct path, as S2 did.
- **"A listen server is a free dedicated server."** It carries the same `O(n²)` upload on a home uplink, gives the host a 0 ms advantage, and ends the match when the host leaves.
- **"Relays are servers."** A relay forwards bytes. It does not decide what happened in the game.
- **"Mesh bandwidth is fine because each peer only sends its own state."** It sends that state `n − 1` times. The per-peer cost grows with `n`, and the total grows with `n²`.

## Check yourself

1. How many connections does a 10-player full mesh have? A 10-player dedicated-server game?
2. A mesh game at 20 Hz with 40-byte state and 28-byte headers must keep each peer's upload under 256 kbit/s. What is the largest `n`?
3. In the latency scenario, which player would you choose as host to minimize the worst pair, and why is B not the answer?
4. Explain in two sentences how *Age of Empires* avoided the mesh bandwidth wall, naming which variable in the model it changed.
5. A studio moves a 4v4 game from listen servers to dedicated servers. List two numbers from this lecture that get better and one cost that gets worse.

<details>
<summary>Answers</summary>

1. Mesh: `10 × 9 / 2 = 45`. Dedicated: 10.
2. `(n − 1) × 20 × 68 × 8 / 1000 ≤ 256`, so `n − 1 ≤ 23.5` and `n = 24`.
3. C gives the smallest worst pair, 65 ms. B's worst pair is C-D at `30 + 55 = 85` ms, because routing C and D through B sends both of them the long way when they are only 30 ms apart.
4. It made `s`, the bytes per update, tiny by sending commands instead of unit state, and every machine ran the same simulation from those commands. Upload then depended on how often players gave orders, not on how many units existed.
5. Better: the host's upload (389.8 kbit/s at `n = 8` on the listen host drops to 6.4 kbit/s per client), and the worst-pair latency can fall with a central server site (95 ms under host A against 50 ms under S2 in our scenario). The host's 0 ms advantage also disappears. Worse: the studio now pays for server hours.

</details>

## Lab / assignment hook

[Lab 03, the topology calculator](../labs/lab03.md). You implement this lecture's bandwidth and latency formulas in `topology.py`, check them against the tables above, then build a scenario for a game of your own with a measured or researched latency matrix and write a one-page topology recommendation.

## Sources

- Bettner, P. & Terrano, M. (2001). "1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond." Gamasutra, 22 March 2001 (now Game Developer). Design goals of 8 players and a 28.8 modem. The estimate of 250 moving units if unit state were sent. Commands executed two communications turns ahead. Peer topology with all clients connected to all others. Its listed strengths (latency, no single point of failure) and weaknesses (more connections, some NAT configurations unsupported).
- Valve Developer Community, "Source Multiplayer Networking" (archived copy, 2024). Source uses client-server networking, usually with a dedicated host. Lag compensation illustrated on a listen server.
- Minecraft Wiki, "Multiplayer", "Server" and "Bedrock Dedicated Server" (accessed September 2026). Single-player runs an internal server. Players can host, run the server software, or use Realms, a paid Mojang-hosted server.
- Valve, Steamworks documentation, "Steam Datagram Relay" (accessed September 2026). Relay network over Valve's backbone. IP addresses hidden against denial-of-service attacks. Authenticated, encrypted, rate-limited traffic. Faster routes for many players. Usable for peer-to-peer and dedicated servers.
- Riot Games Technology blog, "Fixing the Internet for Real Time Applications: Part I" (6 November 2015). Routing by cost rather than latency, the San Francisco to Portland example, and the Riot Direct team's goal of the fastest connection to Riot's servers.
- Gambetta, G. *Fast-Paced Multiplayer*, part I, "Client-Server Game Architecture" (gabrielgambetta.com). Don't trust the player. Authoritative servers and clients as privileged spectators.
- Postel, J. (1980). RFC 768 and Postel, J. (1981). RFC 791. The 8-byte UDP and 20-byte IPv4 headers used for `h = 28`.

## Interactive spec: examples/w03-topology-explorer.html

**Insight the visual must make obvious:** the topology decides whose uplink pays and which path each action takes. The listen host's upload bar grows with `n²` while client bars stay flat, and a well-placed server or relay can beat a direct path when the direct route is bad.

**Layout.** A map panel, a bar panel and a latency matrix, plus a number panel. On desktop, the map is on the left and the bars and matrix on the right. Under 700 px wide, everything stacks in the order map, matrix, bars, numbers. No page-level horizontal scroll.

1. **Map.** Four player circles labelled A to D, plus a server square S and a relay diamond R (R only shown in relay mode). All are draggable with pointer and keyboard (focus with Tab, arrows move 10 px, Shift+arrow 50 px). Lines show packet flows for the chosen topology, with thickness proportional to bytes per second on that link. In listen mode, the host has a crown-shaped outline drawn with plain shapes, no icons or art.
2. **Upload bars.** One bar per machine (players, plus S or R when present) showing upload in kbit/s, with a horizontal line at the chosen home uplink. Bars over the line turn red. Data-center machines (S, R) are drawn in a different color and are not compared with the home line.
3. **Latency matrix.** One-way latency for every pair of players under the current topology. The worst pair is highlighted, and its value is shown large above the matrix.
4. **Number panel.** For the current settings: mesh peer upload, client upload, client download, server upload, listen host upload (B/s and kbit/s), worst pair and which pair, each player's round trip to whatever they send to.

**Latency source.** Two modes, selected by a toggle.
- "Scenario" (default). Uses the lecture's matrices exactly. Dragging is disabled for players and enabled only to pick a host or server site. S snaps between "S1" and "S2". The relay uses A 20, B 18, C 15, D 20.
- "Map". One-way latency between two points is `distance_px × 0.1 ms + 2 ms`, plus a "detour" control that adds a chosen number of ms (default 25) to the direct A-D path only, to show a broken triangle.

**Controls.**
- Topology radio: Mesh, Dedicated server, Listen server, Relay (P2P through R).
- Host picker (listen mode): A, B, C, D.
- Player count slider `n`, 2 to 64, default 4. Bandwidth values use `n`. The map and matrix keep showing four players, with a note "bandwidth for n players".
- Send rate `r` (5 to 60 Hz, default 20), state bytes `s` (8 to 200, default 40), input bytes `i` (default 12), header `h` (fixed 28, shown).
- Home uplink selector: 1, 5, 10, 20 Mbit/s, default 10.

**Formulas.** Mesh peer upload `(n − 1) r (s + h)`. Snapshot `n s + h`. Client download `r (n s + h)`. Client upload `r (i + h)`. Server upload `n r (n s + h)`. Listen host upload `(n − 1) r (n s + h)`. Relay P2P, each peer upload `r (s + h)` (one packet to R, which fans out), relay upload `n (n − 1) r (s + h)`. Latency: mesh `d(a, b)`, server `d(a, S) + d(S, b)`, listen `d(a, H) + d(H, b)` with `d(H, H) = 0`, relay `d(a, R) + d(R, b)`. kbit/s = B/s × 8 / 1000. This matches `labs/lab03-starter/topology.py`.

**Test values** (assert on load, Scenario mode, `r = 20`, `s = 40`, `i = 12`, `h = 28`):
- `n = 8`: mesh 9,520 B/s (76.2 kbit/s), client upload 800, client download 6,960 (55.7), server 55,680 (445.4), listen host 48,720 (389.8).
- `n = 64`: server 3,312,640 B/s (26,501.1 kbit/s).
- Worst pair: mesh 60 (A-D). S1 91 (C-D). S2 50 (A-D). Host A 95 (C-D). Host B 85 (C-D). Host C 65. Host D 115 (A-B). Relay 40 (A-D).

**First screen:** Scenario mode, listen server, host D, `n = 4`, with the worst pair "A-B 115 ms" shown large and a caption: "Same four players. Host at C: 65 ms. Host at D: 115 ms."
