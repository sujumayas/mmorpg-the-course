# MMO302 — MMO Server Architecture

Year 3, semester 5 · 4 credits · Prerequisites: CS202, DB201

How thousands of players share one world: zoning, sharding, interest management, persistence and scaling.

## Learning outcomes

- Design a server topology for a target concurrency
- Implement area-of-interest management
- Build a persistent, authoritative world server with safe item transactions

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Scale targets: CCU, messages per second, the n-squared problem | [lecture](lectures/w01-scale-targets-ccu-messages-and-n-squared.md) | [crowd-cost](examples/w01-crowd-cost.html) |
| 2 | Shards, realms, zones, instances, layers | [lecture](lectures/w02-shards-realms-zones-instances-layers.md) | [layer-split](examples/w02-layer-split.html) |
| 3 | Area of interest: grids, radius, hysteresis | [lecture](lectures/w03-area-of-interest-grids-radius-hysteresis.md) | [aoi-grid-vs-broadcast](examples/w03-aoi-grid-vs-broadcast.html) |
| 4 | Zone servers and handoff | [lecture](lectures/w04-zone-servers-and-handoff.md) | [zone-handoff](examples/w04-zone-handoff.html) |
| 5 | Tick rate for MMOs vs shooters | [lecture](lectures/w05-tick-rate-for-mmos-vs-shooters.md) | [tick-budget](examples/w05-tick-budget.html) |
| 6 | Simulation authority and anti-cheat by design | [lecture](lectures/w06-simulation-authority-and-anti-cheat-by-design.md) | [authority-dial](examples/w06-authority-dial.html) |
| 7 | Persistence strategies: write-through, periodic save, event sourcing | [lecture](lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) | [persistence-strategies](examples/w07-persistence-strategies.html) |
| 8 | Item ownership and transactional integrity | [lecture](lectures/w08-item-ownership-and-transactional-integrity.md) | [ledger-drift](examples/w08-ledger-drift.html) |
| 9 | Login, character select, gateway services | [lecture](lectures/w09-login-character-select-gateway-services.md) | [login-queue](examples/w09-login-queue.html) |
| 10 | Chat, guild and social services | [lecture](lectures/w10-chat-guild-and-social-services.md) | [chat-fanout](examples/w10-chat-fanout.html) |
| 11 | Load testing with bots | [lecture](lectures/w11-load-testing-with-bots.md) | [latency-knee](examples/w11-latency-knee.html) |
| 12 | Single-shard architectures (EVE) and time dilation | [lecture](lectures/w12-single-shard-architectures-and-time-dilation.md) | [time-dilation](examples/w12-time-dilation.html) |
| 13 | Cloud deployment and autoscaling | [lecture](lectures/w13-cloud-deployment-and-autoscaling.md) | [autoscaling-headroom](examples/w13-autoscaling-headroom.html) |
| 14 | Observability: logs, metrics, traces | [lecture](lectures/w14-observability-logs-metrics-traces.md) | [tick-tail](examples/w14-tick-tail.html) |
| 15 | Final: 500-bot load test of a world server | [assessments](#assessment-materials) | — |

## Signature worked examples

- Interest management: broadcast-to-all vs grid AOI, messages per tick as players cluster (interactive)
- EVE Online time dilation: slowing the clock to keep a 3,000-player battle consistent (verified: CCP dev blog 22 Apr 2011, 10% floor, Crucible 29 Nov 2011)

## Labs

- [MMO302 · Lab 01: The crowd cost model](labs/lab01.md)
- [MMO302 · Lab 02: Layer assignment](labs/lab02.md)
- [MMO302 · Lab 03: Build interest management](labs/lab03.md)
- [MMO302 · Lab 04: Zone handoff simulator](labs/lab04.md)
- [MMO302 · Lab 05: Tick budget profiler](labs/lab05.md)
- [MMO302 · Lab 06: Movement validators](labs/lab06.md)
- [MMO302 · Lab 07: Persistence strategies under crash](labs/lab07.md)
- [MMO302 · Lab 08: A dupe-proof item service](labs/lab08.md)
- [MMO302 · Lab 09: Login queue and session tickets](labs/lab09.md)
- [MMO302 · Lab 10: Chat router under load](labs/lab10.md)
- [MMO302 · Lab 11: Ramp test with an open-loop bot fleet](labs/lab11.md)
- [MMO302 · Lab 12: A time-dilation governor](labs/lab12.md)
- [MMO302 · Lab 13: An autoscaler for a zone-server fleet](labs/lab13.md)
- [MMO302 · Lab 14: Tick telemetry and a stall alert](labs/lab14.md)

## Assessment materials

- [MMO302 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [MMO302 · Final server brief: a persistent, authoritative world server](assessments/final-server-brief.md)
- [MMO302 · Labs brief](assessments/labs-brief.md)
- [MMO302 · Load test brief: 500 bots against your world server](assessments/load-test-brief.md)

## Readings

- Alexander (ed.) — Massively Multiplayer Game Development (selected)
- CCP Games dev blogs on Time Dilation (2011)

## Assessment

Labs (40%), load test (20%), final server (40%)
