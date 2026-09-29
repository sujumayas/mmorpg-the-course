# Launch T01 case file (invented)

Everything in this file is invented for the lab. The game, studio and people do not exist. T01 is row `T01` in `launches.csv`.

## The game

A fantasy MMO with 12 worlds at launch (NA 6, EU 6), each admitting 3,000 players. Launch at 16:00 UTC on a Thursday, global unlock. A paid head start ran for the three days before. Account system and store built new for this launch.

## The launch plan's forecasts

| Forecast | Plan | Source in the plan |
|---|---|---|
| Arrivals in the first hour (all worlds) | 900 per minute | marketing pre-orders × 0.6 |
| Bottleneck stage | world entry | load test at 60% of target CCU |
| Mean session length, day 1 | 150 minutes | closed beta telemetry (2,400 testers) |
| Peak world queue, hour 3 (one full world) | 4,000 | week 2 queue model |
| Severity-1 incidents, week 1 | at most 2 | beta exposure estimate |
| Day-30 monthly active players | 120,000 | 50% of launch-week players |

## What happened (from dashboards and incident postmortems)

| Measure | Actual |
|---|---|
| Arrivals in the first hour | 1,450 per minute |
| First stage to saturate | account service (entitlement check), at about 700 per minute |
| Mean session length, day 1 | 230 minutes |
| Peak world queue, hour 3 (busiest world) | 9,800 |
| Severity-1 incidents, week 1 | 4 |
| Day-30 monthly active players | 84,000 |

## Timeline (UTC)

| Time | Event |
|---|---|
| Mon 16:00 | Head start opens. Arrivals 300 per minute, no queues. |
| Thu 15:45 | Final go/no-go. Entitlement error rate in rehearsal 0.4%, below the 1% criterion. Go. |
| Thu 16:00 | Unlock. |
| Thu 16:04 | Entitlement check latency above 5 s. Launcher retries automatically every 10 s. |
| Thu 16:11 | Login success rate 38%. War room convened. |
| Thu 16:25 | Store purchases fail for 20% of attempts; store kill switch exists but its owner is not in the channel. |
| Thu 16:52 | Store turned off. Entitlement latency falls to 2 s. |
| Thu 17:30 | Two more account-service nodes added. Login success 91%. Queues form at world entry on 4 worlds. |
| Thu 19:00 | Peak queue 9,800 on the busiest world. |
| Thu 21:10 | 4 extra worlds opened (2 NA, 2 EU); free transfers announced. |
| Fri 03:15 | Severity-1: duplicated items from a store refund path. Trading disabled for 5 h. |
| Sat 18:40 | Severity-1: world server crash loop on one EU world, 2 h down. |
| Tue 10:05 | Severity-1: guild bank rollback of 3 h. |
| Day 30 | 84,000 monthly active players. Steam: 11,000 reviews, 48% positive. |

## Team notes (raw, from the retrospective board)

- "Launch queues were brutal."
- "The account service was never load-tested at launch scale, only the world servers."
- "Store and account system both new, both shipped in the last six weeks."
- "Head start went great, so we relaxed."
- "Nobody knew who owned the store switch at 16:25."
- "The beta had only 2,400 testers; session lengths were from people who knew it would wipe."
- "Marketing forecast was too low."
- "Should have been more careful with the refund path."
