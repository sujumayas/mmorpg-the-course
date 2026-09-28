<!-- generated-stub: safe to overwrite -->
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
| 1 | Scale targets: CCU, messages per second, the n-squared problem | _todo_ | _todo_ |
| 2 | Shards, realms, zones, instances, layers | _todo_ | _todo_ |
| 3 | Area of interest: grids, radius, hysteresis | _todo_ | _todo_ |
| 4 | Zone servers and handoff | _todo_ | _todo_ |
| 5 | Tick rate for MMOs vs shooters | _todo_ | _todo_ |
| 6 | Simulation authority and anti-cheat by design | _todo_ | _todo_ |
| 7 | Persistence strategies: write-through, periodic save, event sourcing | _todo_ | _todo_ |
| 8 | Item ownership and transactional integrity | _todo_ | _todo_ |
| 9 | Login, character select, gateway services | _todo_ | _todo_ |
| 10 | Chat, guild and social services | _todo_ | _todo_ |
| 11 | Load testing with bots | _todo_ | _todo_ |
| 12 | Single-shard architectures (EVE) and time dilation | _todo_ | _todo_ |
| 13 | Cloud deployment and autoscaling | _todo_ | _todo_ |
| 14 | Observability: logs, metrics, traces | _todo_ | _todo_ |
| 15 | Final: 500-bot load test of a world server | [assessments](#assessment-materials) | — |

## Signature worked examples

- Interest management: broadcast-to-all vs grid AOI, messages per tick as players cluster (interactive)
- EVE Online time dilation: slowing the clock to keep a 3,000-player battle consistent (verify figures)

## Readings

- Alexander (ed.) — Massively Multiplayer Game Development (selected)
- CCP Games dev blogs on Time Dilation (2011)

## Assessment

Labs (40%), load test (20%), final server (40%)
