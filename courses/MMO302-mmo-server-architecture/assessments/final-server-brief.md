# MMO302 · Final server brief: a persistent, authoritative world server

**Weight:** 40% of the course grade.
**Assigned:** week 3. **Milestone 1:** end of week 6. **Milestone 2:** end of week 10. **Final submission:** start of week 15, followed by a 20-minute viva in week 15.
**Work mode:** individual, or a pair with a contribution statement. In a pair, each partner answers the viva questions alone.
**Lectures:** all fourteen, most directly [week 3, area of interest](../lectures/w03-area-of-interest-grids-radius-hysteresis.md), [week 4, zone servers and handoff](../lectures/w04-zone-servers-and-handoff.md), [week 6, authority](../lectures/w06-simulation-authority-and-anti-cheat-by-design.md), [week 7, persistence](../lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md), [week 8, item ownership](../lectures/w08-item-ownership-and-transactional-integrity.md), [week 9, login and gateway](../lectures/w09-login-character-select-gateway-services.md) and [week 14, observability](../lectures/w14-observability-logs-metrics-traces.md).
**Related assessment:** the [week 15 load test](load-test-brief.md) (20%) drives this server with 500 bots. Build the two together.

## What this component is for

The labs test each technique alone, in Python simulators. This assessment asks you to put them into one running server that real clients connect to, that survives being killed, and that cannot duplicate an item however the clients misbehave. A server that "seems to work with three bots" earns little here. A server that states its tick cost, its handoff protocol, its persistence loss window and its audit result, and shows each one working in the viva, earns a lot.

It assesses all three course outcomes. The design document assesses "design a server topology for a target concurrency". The zones and the interest manager assess "implement area-of-interest management". The authority checks, persistence and item service assess "build a persistent, authoritative world server with safe item transactions".

## What you build

A small persistent world with at least two zones on a flat 2D map, for example two 1 km squares joined by a border. Players log in, walk, see each other, fight simple monsters that drop gold and items, pick up loot, trade items and gold with each other, mail items, and chat. Everything a player earns survives a server restart. No art is marked. A headless bot is the main client. A minimal debug viewer (Godot, a web page, or a text map) helps in the viva but earns no marks on its own. Do not use copyrighted characters, sprites or logos.

### Technical rules

- **Language and data.** C# (.NET 8) is the program's reference server stack, and Go is accepted. PostgreSQL is the system of record and Redis holds sessions and short-lived state. Another language needs the instructor's written approval before Milestone 1. The lab logic you wrote in Python (grid, validator, event log, transfer, tickets, bucket, histogram) is your specification. Port it, and port its tests.
- **Processes.** At least three process types: a gateway (week 9), two or more zone servers (week 4), and PostgreSQL plus Redis. Chat may live in the gateway or in its own process. One command (`docker compose up`, or a documented script) starts everything on one machine.
- **Authority.** Clients send intents and at most one bounded claim, position. Every other outcome (damage, loot, item moves, gold) is computed by the server (week 6).
- **Switches for the viva.** Command-line flags or config keys that turn off the AOI grid (broadcast to the zone), the movement check, the stale-sequence check in handoff, and the operation-ID check in transfers, one at a time, so the examiner can see what each one prevents.

### Required features

Each item names the lab that gives you a starting point.

1. **Fixed-rate tick (week 5, lab 05).** Each zone server runs a fixed timestep at a rate you choose and justify from your fitted `a`, `d`, `e` and the densest moment your design allows. Overruns follow a written policy (stretch, shed load or dilate), not whatever happens by default.
2. **Interest management (week 3, lab 03).** A uniform grid as broad phase, an exact radius test as narrow phase, and enter and leave radii with hysteresis. A test shows the grid gives exactly the same interest sets as brute force on a seeded world.
3. **Zones and handoff (week 4, lab 04).** A static partition with a hysteresis band. Handoff follows the numbered protocol: one owner at every instant, `seq` increasing on every ownership change, stale messages rejected, inputs buffered during transfer. Ghosts let players near the border see across it.
4. **Movement validation (week 6, lab 06).** A token bucket with a stated tolerance plus a wall check. Failures correct the player, log the event, and never kick on a single failure.
5. **Persistence (week 7, lab 07).** A written per-state policy. At minimum, character position and stats on a periodic or write-behind save, and valuable events (rare loot, quest completion) in an event log with group commit and snapshots. Recovery loads the snapshot and replays the tail.
6. **Items and gold (week 8, lab 08).** One row per unique item with one owner column. Stackable gold in wallets with `CHECK (gold >= 0)`. Trades, mail and loot pickups are single transactions with operation IDs supplied by the client once per intent. A conservation audit that sums every container (wallets, bags, mail, trade escrow, the ground) against the mint and destroy ledger and reports drift, which must be exactly zero.
7. **Login and gateway (week 9, lab 09).** A login service that issues signed, short-lived, single-use session tickets with an audience. A world cap with a queue that admits one player per departure, and a reconnect grace period. The gateway holds the client connection across zone changes.
8. **Chat (week 10, lab 10).** At least a zone channel and whispers, with a per-sender token bucket. State the delivery guarantee of each channel in `DESIGN.md`.
9. **Telemetry (week 14, lab 14).** Tick time per zone as a histogram with a bucket edge exactly at the budget, stalls per minute per zone, players per zone, handoffs per second, commits per second and audit drift, exported where the load-test report can read them. Structured logs for every item creation, transfer and destruction, with a correlation ID.

### The design document

`DESIGN.md`, at most 2,500 words plus tables. It sizes your architecture for a target you did not build: a shard of 20,000 PCU in an 8 km by 8 km world, with a capital holding 30% of players and a world boss that can draw 400 players into one place.

- **Topology.** Zone layout, handoff rate `H`, ghost fraction `G` and busiest zone from the week 4 model. Zone servers, gateways and chat processes needed, with the headroom from week 1 and the failure spare.
- **The crowd.** What happens when the world boss spawns: which levers from weeks 1, 2, 3, 5 and 12 you use, and the tick cost with and without them.
- **Persistence and integrity.** The per-state policy table with commits per second at 20,000 players, the average loss, and the recovery time at your snapshot interval.
- **Deployment.** From lab 13: the provisioning lag you would expect, the target utilization for launch night and for a normal evening, and the scale-in rule.
- **Measured against predicted.** For your built server, the tick cost your lab 05 fit predicts at 500 bots, set against what you measured in the load test.

## Milestones

Milestones are demos in the lab session, about 10 minutes each. They are marked in the rubric below, and their main job is to catch a server that is going wrong early.

| Milestone | Due | What you show |
|---|---|---|
| 1 | End of week 6 | One zone server with a fixed tick; bots connect, move and see each other through grid AOI with hysteresis; the grid-equals-brute-force test passes; the movement check rejects a scripted speed cheat and a walk through a wall; a one-page tick-rate choice with numbers |
| 2 | End of week 10 | Two zones with handoff and ghosts; login with tickets and a capped queue; loot, trade and mail through the item service; the audit reads zero after a scripted mix of trades with injected crashes; the server is killed and restarts with every committed item in place |
| Final | Start of week 15 | Everything above plus chat, telemetry and the design document; the server passes its own test suite from a clean checkout |

A missed milestone can be shown at the next lab session for half its marks.

## What to submit

A repository link or zip, tagged `final`, containing:

- The source, with a `README.md` that starts everything with one command and runs the tests with another.
- Tests ported from the labs, plus these integration tests: grid equals brute force; a handoff with a lost ACK and a late duplicate never leaves two owners; a trade replayed with the same operation ID moves gold once; a crash between the two writes of a transfer leaves zero drift; a forged, expired, misdirected or replayed ticket is refused.
- `DESIGN.md` as described above.
- `RUNBOOK.md`, one page: how to start, stop, back up and restore the world, and what to do when the audit reads nonzero.

## The viva

Twenty minutes in week 15, with your server running. The examiner will:

1. Ask you to start the world from a clean checkout and log in two bots.
2. Walk a bot across the border while the other watches, and ask you to show the handoff in the logs.
3. Turn off one safety switch (for example the operation-ID check), run a scripted retry storm, and ask you to predict the audit result before it prints. Then turn it back on and run it again.
4. Kill a zone server with `kill -9` in the middle of a trade and ask you to say, before restart, exactly what state each player will be in afterwards.
5. Ask two questions from the [exam bank](exam-bank.md), rewritten with your own numbers ("your tick costs 38 ms at 500 bots; what happens at 700 if 200 of them stand at the boss?").

## Rubric

Each criterion is scored Excellent (full points), Adequate (half), or Missing or wrong (0). A marker may give a quarter or three quarters of the points where the work falls clearly between two cells.

| Criterion | Excellent | Adequate | Missing or wrong | Points |
|---|---|---|---|---|
| Milestone 1 | All five items shown on time | Shown late, or one item missing | Not shown | 10 |
| Milestone 2 | All five items shown on time | Shown late, or one item missing | Not shown | 10 |
| Interest management and tick | Grid equals brute force in a test; hysteresis stops flicker; tick rate and overrun policy justified with fitted constants | Works, but tick rate or policy chosen without numbers | Broadcast only, or grid misses players | 10 |
| Zones and handoff | Numbered protocol with stale rejection and input buffering; hysteresis band; ghosts across the border; the lost-ACK and duplicate tests pass | Handoff works but one failure case is untested | Players duplicated or lost at the border | 10 |
| Authority and validation | Only intents plus bounded position; token bucket and wall check; correct, log, no kick on first failure | A check exists but uses a weaker shape or kicks on failure | Client claims accepted for damage, loot or items | 10 |
| Persistence and recovery | Per-state policy implemented; event log with snapshots; `kill -9` loses nothing committed and recovery time matches the model | Saves work but recovery replays the whole log, or loss window unmeasured | Progress lost on restart | 15 |
| Items and transactional integrity | Owner column, single transactions, operation IDs, overdraft refused and recorded; audit counts every container and reads exactly zero after the crash and retry tests | Correct under normal play, one crash or retry case unguarded | Items or gold can be duplicated | 15 |
| Login, gateway and chat | Signed single-use tickets with audience and expiry; queue admits per departure with a grace period; chat rate-limited with stated guarantees | Login works but tickets are reusable or the queue is unbounded | Clients connect straight to zone servers without a ticket | 10 |
| Design document and viva | Every number in `DESIGN.md` traced to a lecture model or a measurement; predicted against measured explained; viva predictions correct and explained | Document complete but some numbers unbacked, or viva answers partial | Opinion without numbers, or cannot explain own server | 10 |
| **Total** | | | | **100** |

## Academic integrity

You may reuse your own lab code and any code from the lectures and starters. Libraries for networking, serialization, database access and testing are fine. Libraries that provide replication, interest management, persistence or transactions for game servers are not, because those are what this course assesses. You may use AI assistants and documentation, and you must list them in one line per use in `README.md`. In a pair, the contribution statement names who wrote each component, and the viva checks it.
