<!-- generated-stub: safe to overwrite -->
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
| 1 | Networks for game devs: TCP vs UDP | _todo_ | _todo_ |
| 2 | Latency, jitter, loss — measure your own | _todo_ | _todo_ |
| 3 | Topologies: peer-to-peer, client-server, relay | _todo_ | _todo_ |
| 4 | Server authority: never trust the client | _todo_ | _todo_ |
| 5 | Serialization and bit packing | _todo_ | _todo_ |
| 6 | Reliability over UDP | _todo_ | _todo_ |
| 7 | Snapshots and delta compression | _todo_ | _todo_ |
| 8 | Client-side prediction | _todo_ | _todo_ |
| 9 | Server reconciliation | _todo_ | _todo_ |
| 10 | Entity interpolation | _todo_ | _todo_ |
| 11 | Lag compensation (rewind hit detection) | _todo_ | _todo_ |
| 12 | Deterministic lockstep (RTS) | _todo_ | _todo_ |
| 13 | Tick rate and bandwidth budgets | _todo_ | _todo_ |
| 14 | Testing under bad networks (netem, clumsy) | _todo_ | _todo_ |
| 15 | Final: networked arena prototype | [assessments](#assessment-materials) | — |

## Signature worked examples

- Interactive lag lab: toggle prediction/reconciliation/interpolation at 150 ms and watch the ghosts
- Bandwidth budget: 100 players x 20 Hz x bytes per entity — the n-squared wall

## Readings

- Gambetta — Fast-Paced Multiplayer (series)
- Bernier (2001) — Latency Compensating Methods in Client/Server In-game Protocol Design (Valve)
- Fiedler — Networking for Game Programmers

## Assessment

Labs (40%), final prototype (60%)
