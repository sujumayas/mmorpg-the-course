# CS202 — Networking Fundamentals for Multiplayer Games

Year 2, semester 4 · 4 credits · Prerequisites: CS102

How multiplayer works under latency: sockets, authority, prediction, reconciliation and lag compensation.

## Learning outcomes

- Explain latency, jitter, packet loss and bandwidth effects on gameplay
- Implement an authoritative server with client-side prediction and reconciliation
- Implement entity interpolation and lag compensation

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Networks for game devs: TCP vs UDP | [lecture](lectures/w01-networks-for-game-devs-tcp-vs-udp.md) | [head-of-line](examples/w01-head-of-line.html) |
| 2 | Latency, jitter, loss — measure your own | [lecture](lectures/w02-latency-jitter-loss-measure-your-own.md) | [jitter-buffer](examples/w02-jitter-buffer.html) |
| 3 | Topologies: peer-to-peer, client-server, relay | [lecture](lectures/w03-topologies-peer-to-peer-client-server-relay.md) | [topology-explorer](examples/w03-topology-explorer.html) |
| 4 | Server authority: never trust the client | [lecture](lectures/w04-server-authority-never-trust-the-client.md) | [movement-validator](examples/w04-movement-validator.html) |
| 5 | Serialization and bit packing | [lecture](lectures/w05-serialization-and-bit-packing.md) | [quantization-bits](examples/w05-quantization-bits.html) |
| 6 | Reliability over UDP | [lecture](lectures/w06-reliability-over-udp.md) | [redundant-inputs](examples/w06-redundant-inputs.html) |
| 7 | Snapshots and delta compression | [lecture](lectures/w07-snapshots-and-delta-compression.md) | [delta-baseline](examples/w07-delta-baseline.html) |
| 8 | Client-side prediction | [lecture](lectures/w08-client-side-prediction.md) | [prediction-timeline](examples/w08-prediction-timeline.html) |
| 9 | Server reconciliation | [lecture](lectures/w09-server-reconciliation.md) | [reconcile-replay](examples/w09-reconcile-replay.html) |
| 10 | Entity interpolation | [lecture](lectures/w10-entity-interpolation.md) | [lag-lab](examples/w10-lag-lab.html) |
| 11 | Lag compensation (rewind hit detection) | [lecture](lectures/w11-lag-compensation-rewind-hit-detection.md) | [rewind-hit](examples/w11-rewind-hit.html) |
| 12 | Deterministic lockstep (RTS) | [lecture](lectures/w12-deterministic-lockstep-rts.md) | [lockstep-timeline](examples/w12-lockstep-timeline.html) |
| 13 | Tick rate and bandwidth budgets | [lecture](lectures/w13-tick-rate-and-bandwidth-budgets.md) | [bandwidth-budget](examples/w13-bandwidth-budget.html) |
| 14 | Testing under bad networks (netem, clumsy) | [lecture](lectures/w14-testing-under-bad-networks-netem-clumsy.md) | [burst-hunt](examples/w14-burst-hunt.html) |
| 15 | Final: networked arena prototype | [assessments](#assessment-materials) | — |

## Signature worked examples

- Interactive lag lab: toggle prediction/reconciliation/interpolation at 150 ms and watch the ghosts
- Bandwidth budget: 100 players x 20 Hz x bytes per entity — the n-squared wall

## Labs

- [CS202 · Lab 01: Sockets and the cost of order](labs/lab01.md)
- [CS202 · Lab 02: Measure your own connection](labs/lab02.md)
- [CS202 · Lab 03: The topology calculator](labs/lab03.md)
- [CS202 · Lab 04: Policing movement](labs/lab04.md)
- [CS202 · Lab 05: 108 bits](labs/lab05.md)
- [CS202 · Lab 06: Acks and copies](labs/lab06.md)
- [CS202 · Lab 07: A snapshot codec](labs/lab07.md)
- [CS202 · Lab 09: Prediction and reconciliation](labs/lab09.md)
- [CS202 · Lab 10: The interpolation buffer](labs/lab10.md)
- [CS202 · Lab 11: Rewind hit detection](labs/lab11.md)
- [CS202 · Lab 12: Lockstep timing and the desync hunt](labs/lab12.md)
- [CS202 · Lab 13: Bandwidth budget](labs/lab13.md)
- [CS202 · Lab 14: Break it on purpose](labs/lab14.md)

## Assessment materials

- [CS202 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [CS202 · Final prototype brief: a networked arena prototype](assessments/final-prototype-brief.md)
- [CS202 · Labs brief](assessments/labs-brief.md)

## Readings

- Gambetta — Fast-Paced Multiplayer (series)
- Bernier (2001) — Latency Compensating Methods in Client/Server In-game Protocol Design (Valve)
- Fiedler — Networking for Game Programmers

## Assessment

Labs (40%), final prototype (60%)
