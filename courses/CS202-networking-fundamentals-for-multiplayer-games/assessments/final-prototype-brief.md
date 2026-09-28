# CS202 · Final prototype brief: a networked arena prototype

**Weight:** 60% of the course grade.
**Assigned:** week 9. **Milestone 1:** end of week 10. **Milestone 2:** end of week 12. **Final submission:** start of week 15, followed by a 20-minute demo and viva in week 15.
**Work mode:** individual, or a pair with a contribution statement. In a pair, each partner answers the viva questions alone.
**Lectures:** all fourteen, most directly [week 4, server authority](../lectures/w04-server-authority-never-trust-the-client.md), [week 8, client-side prediction](../lectures/w08-client-side-prediction.md), [week 9, server reconciliation](../lectures/w09-server-reconciliation.md), [week 10, entity interpolation](../lectures/w10-entity-interpolation.md), [week 11, lag compensation](../lectures/w11-lag-compensation-rewind-hit-detection.md), [week 13, tick rate and bandwidth budgets](../lectures/w13-tick-rate-and-bandwidth-budgets.md) and [week 14, testing under bad networks](../lectures/w14-testing-under-bad-networks-netem-clumsy.md).

## What this component is for

The labs test each technique alone, in a simulator. This assessment asks you to put them together in a small game that real packets carry between real processes, and then to prove how it behaves with measurements instead of adjectives. A prototype that "feels fine on my laptop" earns little here. A prototype that states its latency, its bytes per second and the network conditions under which it breaks, with seeds that reproduce each failure, earns a lot.

It assesses all three course outcomes. Your reports assess "explain latency, jitter, packet loss and bandwidth effects on gameplay". The server and client assess "implement an authoritative server with client-side prediction and reconciliation". The remote players and the hit rule assess "implement entity interpolation and lag compensation".

## What you build

A top-down 2D arena for 2 to 8 players. Players move, and they have one aimed action that can hit another player, such as a hitscan shot, a dash strike or a thrown hook. Keep the game small. Circles on a plain background are enough, and a score counter is the only rule beyond movement and the hit. No art is marked, and you must not use copyrighted characters, sprites or logos.

### Technical rules

- **Language and libraries.** Python 3.10 or later. All networking uses the standard library's `socket` module over UDP, written by you. You may use pygame (or any drawing library, or a text display) for input and drawing only. No networking libraries, engine replication systems or reliability layers you did not write. Another language is allowed with the instructor's written approval, under the same rule.
- **Processes.** One dedicated server process and one process per client. The server is authoritative (week 4). The client also has a headless bot mode that plays a scripted or random input pattern, so you can measure without a human.
- **Switches for the demo.** Command-line flags turn off prediction, reconciliation, interpolation and lag compensation one at a time (for example `--no-predict`), so the examiner can see what each technique does.

### Required features

Each item names the lab that gives you a starting point.

1. **Transport and framing (Lab 01).** UDP for game traffic. A connection handshake that carries a protocol version, and a refusal for a mismatched version.
2. **Authority and validation (Lab 04).** Clients send inputs with sequence numbers, never positions or hits. The server clamps and normalizes movement input, runs a per-client tick budget (policy B) and applies the five checks (range, rate, state, ownership, reach) to the aimed action.
3. **Packet format (Lab 05).** Snapshots and inputs are packed binary with quantized fields. A written bit budget for each message. A reader that rejects malformed packets with its own error type and survives a 10,000-packet fuzz run.
4. **Reliability (Lab 06).** 16-bit wraparound sequence numbers and an ack field. Inputs are sent redundantly with a fixed `k`. Any message that must arrive (a hit confirmation, a score change) is resent until acknowledged, on its own channel.
5. **Snapshots (Lab 07).** Snapshots at a fixed rate no higher than the tick rate. Either deltas against the last acknowledged snapshot with a full-snapshot fallback, or full snapshots with a paragraph in `DESIGN.md` explaining why deltas are not worth it at your entity count.
6. **Prediction and reconciliation (Lab 09).** The client predicts its own movement with the same `step` function and fixed timestep as the server, and reconciles on every snapshot by dropping acknowledged inputs and replaying the rest. Corrections below a threshold you choose are smoothed, and larger ones snap.
7. **Interpolation (Lab 10).** Remote players are drawn from a buffer at `t_r = server time estimate − D`, with `D` chosen from your measurements, capped extrapolation and a teleport rule for respawns.
8. **Lag compensation (Lab 11).** The server keeps a per-player history and tests the aimed action against rewound positions, with a cap `R_max` you choose. If the client reports the tick it was rendering, the server clamps that claim against its own estimate.
9. **Instrumentation.** The server and client count bytes sent and received per second at the socket, per client, and log to CSV. The client logs RTT samples in Lab 02's format, reconciliation corrections, and interpolation pops.
10. **A seeded conditioner (Lab 14).** Traffic between client and server can pass through a conditioner with a seed, separate settings for each direction, delay, jitter and Gilbert-Elliott loss. Lab 14's `udp_conditioner.py` or Lab 02's proxy is fine, extended as needed.

## The three reports

Put all three in `REPORT.md`, each in its own section, with every number carrying its unit, its settings and, where randomness is involved, its seed.

### 1. Latency report

- The RTT distribution from your client's own logs, analyzed with Lab 02's `analyze.py`, on at least two network paths. One is localhost through the conditioner. The other is a real path, such as two lab machines, Wi-Fi across the building, or a classmate's machine at home. Give minimum, median, P95, RFC 3550 jitter, loss rate and the longest loss burst, with at least five minutes of data per path.
- A key-to-screen table for your game in the form of the week 2 and week 8 lectures (input wait, network, tick wait, snapshot wait, interpolation, frame wait), predicted from your rates. Then measure the first visible move after a key press with prediction off and on, and compare.
- Your choice of `D` from the measured loss and jitter, using `D = kΔ + J`, and how far behind the server a remote player is drawn at your walking speed.
- Your choice of `R_max`, with the residual lead and the worst victim window for the 50th and 90th percentile RTT you measured.

### 2. Bandwidth report

- A prediction from the week 13 model (`budget(n, r, b, K)`) of each client's download and the server's upload at 2, 4 and your maximum player count. Predict before you measure, and date the prediction in the report.
- Measured bytes per second at the socket for the same player counts, with bots. Add 28 bytes per packet to your application byte counts, or say how you counted headers.
- The difference between predicted and measured, explained. Typical causes are acks, redundant inputs, reliable resends and delta savings.
- A projection with the model, checked against your measurement, to four times your maximum player count. Say which lever from the lecture you would pull first and what it saves.

### 3. Bad-network test report

- A test matrix of at least five profiles, each run with at least 10 seeds by a script. Include a LAN baseline, two realism profiles built from your latency report, and two stress profiles, one on the client-to-server direction and one on the server-to-client direction (week 14, section 4).
- At least three automatic checks a program applies, such as a speed invariant on drawn positions, convergence after the network recovers, a correction-size budget and "no crash or disconnect".
- For each stress profile, the rare event it targets (for example, a burst of `k` lost snapshots) and its `λ` and `t95` from the week 14 model, showing the run length is long enough.
- The matrix output before and after your fixes. For every failure, the profile, seed and time, a one-line replay command, the cause and the fix. If your matrix finds nothing, plant a bug of the week 14 kinds, show the matrix finding it, and say why your stress profiles would have caught a real one.
- One run through a real OS conditioner (netem on Linux or clumsy on Windows), measured with Lab 02's ping and compared with the settings. On macOS, use the lab's Linux machines or explain the substitute you used.

## Deliverables

- A repository or zip containing the server, the client, the bot mode, the conditioner and the matrix script.
- `README.md` with commands to start the server, start a client, run bots, run the matrix and replay one seed, all from a clean copy on the lab machines.
- `DESIGN.md`, 1,500 to 2,500 words, with these sections.
  1. **Topology and authority.** Your topology, what the client sends, and the validation table for every client message.
  2. **Messages.** Every message type with its delivery class, channel and bit budget.
  3. **Rates.** Tick rate, snapshot rate and input rate, with the latency each adds and the bandwidth and CPU each costs.
  4. **Client techniques.** Prediction, reconciliation (threshold and smoothing time with the reason), interpolation (`D` and extrapolation cap) and lag compensation (`R_max` and who pays).
  5. **What you would change at 64 players.** Using your bandwidth model, the first thing that breaks and your fix.
- `REPORT.md` with the three reports.
- The CSV logs behind every table in the reports.
- Pairs only: `CONTRIBUTIONS.md`, one paragraph each, naming the files each partner wrote.

## Milestone 1: paper design (end of week 10, 10 points)

A two-page design before most of the code exists. It covers the game in three sentences, the topology, the message table with delivery classes, the packed layout of your input and snapshot messages with bit counts, the tick and snapshot rates, and a bandwidth prediction from the week 13 model at your maximum player count. Feedback comes back within a week. Numbers may change later, but `DESIGN.md` must say what changed and why.

## Milestone 2: networked skeleton (end of week 12, 15 points)

A short demo in the lab session, 5 minutes per student or pair. The server and two clients run as separate processes on one machine. Inputs go up and snapshots come down over UDP, with sequence numbers and acks. Prediction and reconciliation work through the conditioner at 150 ms RTT with no loss. Remote players may still be drawn without interpolation. Bring a one-page note with the first measured bytes per second at 2 players next to your milestone 1 prediction.

## Demo and viva (week 15, 20 minutes)

You run your submission from a clean copy on a lab machine while two examiners watch. Every student follows the same steps.

1. **Start (2 min).** Server, two human clients and two bots from the README commands.
2. **Clean network (2 min).** Play briefly on localhost. The examiner reads the bytes-per-second counters and compares them with your bandwidth report.
3. **Bad network (5 min).** The examiner sets the conditioner to a profile of their choice, for example 150 ms RTT with 3% loss and `q = 0.5`. You play. The examiner then turns off prediction, reconciliation, interpolation and lag compensation one at a time with your flags, and you say what the screen shows and why, with a number from the lectures.
4. **Replay (3 min).** The examiner picks one failure from your test report. You replay it from its seed and show the fix.
5. **Questions (8 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your rates, your measured RTT and your code. At least one is a compute question and one is a trace through your own reconciliation or interpolation code.

## Rubric

### Milestones (25 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: design choices | 5: topology, delivery classes and rates each justified with a lecture number | 3 to 4: one choice unjustified | 1 to 2: choices listed with no reasons | 0 | 5 |
| M1: bit and bandwidth budget | 5: every field has range, precision and bits; the week 13 prediction is correct for the stated numbers | 3 to 4: one arithmetic slip or a missing field | 1 to 2: sizes guessed | 0 | 5 |
| M2: skeleton demo | 10: separate processes over UDP; inputs with sequence numbers; prediction and reconciliation hold at 150 ms with no visible false corrections | 6 to 9: works, but reconciliation shows corrections on flat ground | 2 to 5: runs only on one process or without reconciliation | 0 to 1 | 10 |
| M2: first measurement | 5: measured bytes per second next to the prediction, difference explained | 3 to 4: measured, not explained | 1 to 2: estimate only | 0 | 5 |

### Final submission, demo and viva (75 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Authority, protocol and packet format | 9 to 10: intent-only client messages; all five checks and a tick budget; packed quantized format with version; fuzz run clean; reliable channel for must-arrive messages | 7 to 8: one check or the fuzz run missing | 4 to 6: validation partial, or text or `pickle` on the wire | 0 to 3: client-authoritative | 10 |
| Prediction and reconciliation | 11 to 12: one shared `step`; exact drop, accept, replay; zero correction on flat ground; smoothing and snap threshold chosen from measured corrections | 8 to 10: works, threshold not justified | 4 to 7: visible false corrections or naive snapping | 0 to 3: missing | 12 |
| Interpolation and lag compensation | 11 to 12: server-time stamps; `D` from data; capped extrapolation and teleport rule; rewind with `R_max` and a clamped client claim | 8 to 10: one of the two complete, the other simplified | 4 to 7: interpolation on arrival time, or no rewind cap | 0 to 3: missing | 12 |
| Latency report | 8 to 9: two paths with all statistics; predicted and measured key-to-screen; `D` and `R_max` derived from the data | 6 to 7: one path, or choices not tied to data | 3 to 5: localhost only | 0 to 2: missing | 9 |
| Bandwidth report | 8 to 9: prediction made first; measured at three player counts; gap explained item by item; projection with a lever | 6 to 7: gap unexplained or one player count | 3 to 5: measurement or prediction only | 0 to 2: missing | 9 |
| Bad-network test report | 12 to 13: five or more profiles, 10 or more seeds, three or more automatic checks; `t95` for each stress target; every failure replayed and fixed; real OS conditioner measured against its settings | 9 to 11: one element thin | 5 to 8: few seeds, or checks by eye | 0 to 4: one manual "bad network" run | 13 |
| Demo and viva | 9 to 10: all five steps work from a clean copy; each switch explained with a number; answers use your own code and data | 7 to 8: one step needs help | 4 to 6: two steps fail, or answers vague | 0 to 3: cannot run or explain | 10 |
| **Total** | | | | | **75** |

The prototype mark is the milestones plus the final, out of 100, multiplied by 0.60.

## Rules and advice

- **Your labs are the parts.** Most of the prototype is Lab 01's framing, Lab 04's budget, Lab 05's bit packer, Lab 06's acks, Lab 07's codec, Lab 09's client, Lab 10's buffer, Lab 11's history and Lab 14's conditioner, moved from simulators onto sockets. The new work is joining them and measuring the result.
- **Measure early.** Add the byte counters and the RTT log in week 11, before the game is fun. A counter added the night before submission has no history to compare.
- **Predict, then measure.** Every report section rewards a prediction written before the run and an honest account of the gap.
- **Keep it small.** Two to eight players, one arena, one aimed action. Extra features earn nothing, and every one is another branch your test matrix must cover.
- **Late submission.** Up to 48 hours late, the final is marked out of 60 instead of 75, and the demo is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** The rules in the [labs brief](labs-brief.md#academic-integrity) apply. Measurements must come from your own runs, with seeds and settings recorded. In the viva you must be able to explain every file you submit.
