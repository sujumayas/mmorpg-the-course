# PR301 · Week 02 — Technical Architecture Review

**Why this matters:** Your architecture is the one decision that sprints cannot easily undo. A review this week costs an afternoon. Discovering in week 9 that the server falls over at 40 players costs the alpha weekend. Most student architectures fail the review in the opposite direction, though. They carry machinery that a 50-player world does not need, and that machinery eats the hours the economy needed.

**You will be able to:**
- Compute the worst-case deliveries per second, CPU share, bandwidth and database commit rate for your world at twice its concurrency target.
- Find the largest crowd your server can hold within a CPU budget, and compare it with the load test you plan to run.
- Map each line of your persistence promise to a persistence strategy and a transaction boundary.
- Run an architecture review that ends with a signed decision record, including the machinery you chose not to build.

**Before class:** Reread [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) sections 2 and 3 (deliveries and machine counts), [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) section 4 (picking a persistence policy), and [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) section 2 (the latency knee). Bring your week 1 persistence promise and a one-page architecture diagram. Before class, run a spike that measures how many microseconds your server spends building and queuing one state update for one client.

**Prerequisites from earlier courses:** [PR201 week 3](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w03-technical-design-document.md) for the technical design document, spikes and the walking skeleton. [MMO302 week 2](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) for shards, zones and layers. [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) for what zone handoff costs to build. [MMO302 week 5](../../MMO302-mmo-server-architecture/lectures/w05-tick-rate-for-mmos-vs-shooters.md) for tick budgets. [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) for transactions. [CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) for bandwidth budgets.

---

## 1. What an architecture review is for

A review is a meeting where people outside the team try to break the design on paper. Each team presents for twenty minutes. Two reviewers from another team and one instructor ask questions. The meeting ends with a **decision record**: a short list of decisions, each with its reason and what would make the team revisit it.

The review answers four questions, in this order.

1. **Does it carry the load?** At twice the concurrency target, in the worst crowd the design allows, with numbers.
2. **Does it keep the promise?** Every line of the week 1 persistence promise maps to a strategy that delivers it.
3. **Is anything unnecessary?** Every component must be justified by question 1 or 2. Anything else is cut or deferred.
4. **What will sprint 1 prove?** The walking skeleton from PR201 week 3, stated as a test that passes or fails.

Question 3 surprises students. They expect a review to add work, and at 50 players it usually removes it. [MMO302](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) taught you the architecture of worlds with tens of thousands of players, with zone servers, handoff, gateways and layers. Those are answers to problems you do not have yet. The review's job is to find out which ones you do have.

## 2. Worked example: does one process carry the test?

### The hook

In the summer of 2019 Blizzard ran three public stress tests before World of Warcraft Classic launched on 26 August. On the stress test realms, the level cap was five. Players could not leave the starting areas even if they wanted to, so they piled into the same few zones. Blizzard wanted the worst crowd, on purpose, before real players made it by accident.

Your week 9 alpha has 50 players and you control where they start. The same logic applies. Plan the test around the worst crowd your world allows, not the average one. Players spread across a map are cheap. Players packed around one group encounter are not.

### The model

This is [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md)'s delivery count, with mobs added and a budget attached.

```
N           = headroom × target CCU
deliveries  = u × N × (N − 1) + m × u_m × N
cpu         = deliveries × e
bandwidth   = deliveries × s + N × f × h
commits     = N × c
```

- `N` is the number of players in the load test. The course target is 50, and the load test runs at `headroom = 2`.
- `u` is state updates each player produces per second, and `u_m` is the same for each of the `m` mobs near the crowd.
- A **delivery** is one update written for one recipient. In the worst case all `N` players stand in one group, so each player update goes to `N − 1` others and each mob update goes to all `N`.
- `e` is the CPU time for one delivery, measured by your spike. `cpu` is then the share of one core spent on deliveries.
- `s` is bytes per delivery, `f` is packets per client per second (one per tick) and `h` is the header bytes per packet.
- `c` is persistent changes per player per second that go to the database as commits.

The budgets come from earlier courses. Keep `cpu ≤ 0.6`, because [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) showed that response time explodes as a single worker approaches full use. Keep bandwidth under your host's uplink, and commits under what you measured on your database.

One extra number is worth having. Solve `cpu = 0.6` for `N` to get `N_max`, the largest crowd one process can hold within budget.

### Numbers you can check

The *Saltmarsh* team from week 1 plans one server process for the whole world, a 10 Hz tick and a PostgreSQL database. Their spike measured `e = 8` microseconds per delivery. The market square, where the group encounter also starts, can hold 60 mobs and critters.

| Parameter | Value |
|---|---|
| Target CCU, headroom, `N` | 50, 2, 100 |
| `u`, `u_m`, `m` | 5, 2, 60 |
| `e` | 8 µs |
| `s`, `h`, `f` | 20 B, 28 B (IPv4 and UDP headers), 10 per second |
| `c` | 0.1 changes per player per second |

At the target, 50 players:

```
deliveries = 5 × 50 × 49 + 60 × 2 × 50 = 12,250 + 6,000 = 18,250 per second
cpu        = 18,250 × 8 µs = 0.146, about 15% of one core
```

At the load test, 100 players:

```
deliveries = 5 × 100 × 99 + 60 × 2 × 100 = 49,500 + 12,000 = 61,500 per second
cpu        = 61,500 × 8 µs = 0.492, about 49% of one core
bandwidth  = 61,500 × 20 + 100 × 10 × 28 = 1,230,000 + 28,000 = 1,258,000 B/s
           ≈ 10.1 Mbit/s in total, 12.6 kB/s per client
commits    = 100 × 0.1 = 10 per second
```

Doubling the players multiplied the deliveries by `61,500 / 18,250 = 3.37`. The player-to-player part grew by `49,500 / 12,250 = 4.04`, close to four, because it grows with `N²`. The mob part grew by exactly two.

Now the ceiling. Set `8 µs × (5N² − 5N + 120N) = 0.6`:

```
5N² + 115N = 75,000
N = (−115 + √(115² + 4 × 5 × 75,000)) / 10 = (−115 + 1,230.1) / 10 ≈ 111.5
```

So one process holds a crowd of 111 players within budget. The load test at 100 is inside it, with about 10% to spare.

| Crowd | Deliveries/s | CPU share | Outbound | Commits/s |
|---|---|---|---|---|
| 50 | 18,250 | 15% | 3.0 Mbit/s | 5 |
| 100 | 61,500 | 49% | 10.1 Mbit/s | 10 |
| 111 | 74,370 | 59% | 12.2 Mbit/s | 11 |
| 120 | 85,800 | 69% | 14.0 Mbit/s | 12 |

Check the first row's bandwidth by hand: `18,250 × 20 + 50 × 10 × 28 = 365,000 + 14,000 = 379,000` bytes per second. Times 8 bits, divided by 1,000,000, that is 3.03 Mbit/s. This course uses 1 Mbit = 1,000,000 bits, as network providers do.

### What the numbers decide

The team's first diagram had three zone servers with handoff between them, a separate login gateway and Redis in front of the database. Read against the table:

- **Zone servers and handoff: cut.** One process holds 111 in the worst crowd. [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) showed that handoff is where items get duplicated and players get lost between servers. The team estimated it at 60 hours. That is half again the 40 hours the team saved by cutting a crafting tier in week 1.
- **Separate login service: keep, in the same process for now.** Login is a different job from simulation, so it keeps its own module and its own tests. It does not need its own machine at 100 players.
- **Redis cache: cut.** Ten commits a second is nothing for PostgreSQL. A cache adds a second copy of the truth and a new way to lose items.
- **Area of interest: defer, with a trigger.** At 100 players everyone can hear everyone within budget. The decision record says the team adds a grid ([MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md)) if the week 6 load test shows tick time above budget.

Run `check_capacity.py` from [lab 02](../labs/lab02.md) on the starter file to reproduce the 100-player row. Change `headroom` to 2.4 and it prints `NOT READY`, because 120 players pass the ceiling.

### The same idea elsewhere

**EVE Online.** CCP's battle for 6VDT-H in July 2013 put 4,070 pilots in one star system, and the system ran at one tenth of normal speed for most of the fight. Less than three months earlier, the whole cluster had held 65,303 players at once without trouble. Total population did not decide the load. The biggest crowd did. MMO302 week 1 opened with the same case.

**WoW Classic layering.** At the 2019 launch, Blizzard ran several copies of the outdoor world per realm, called layers, to spread crowds. Each layer had its own NPCs and resources. On 13 November 2019, before content phase 2, realms went down to a single layer. Blizzard built machinery for the launch crowd and then removed it once the crowd thinned. In the model, a layer caps the group size `N` that enters the square term.

**Your PR201 bandwidth budget.** CS202 week 13 and PR201 week 3 costed bytes per client. That budget is the `s` and `h` terms here. The new part in this course is the square.

### Eyes-open judgment

The model is a worst case in one direction and optimistic in another. It is pessimistic because it assumes every player hears every other player, and nobody sends an update when they stand still. It is optimistic because `e` came from a spike, and a spike measures the cheap path. Real delivery code also does interest checks, compression and logging. Treat `e` as a floor, and rerun the numbers with the week 6 load-test measurement.

The model also leaves out the simulation itself: AI, combat resolution and physics. At 60 mobs this is small. Week 6 measures it directly when the mobs think.

Most of all, the 0.6 budget is a choice, not a law. A team that runs the test at 100 and sees p99 tick time well inside the tick may go higher. A team that sees spikes lowers it. The review should record the number and why.

### Check yourself

1. The team adds a world boss that brings 40 extra mobs into the square. Recompute CPU at 100 players. Does the design still pass?
2. A team measured `e = 20` µs in their spike, in an interpreted language. Find their `N_max` with the same `u`, `u_m` and `m`. What would you change first?
3. Why does halving `u` from 5 to 2.5 raise `N_max` by more than halving `m` from 60 to 30?

<details><summary>Answers</summary>

1. Mob deliveries become `100 × 2 × 100 = 20,000`. Total is `49,500 + 20,000 = 69,500`, and CPU is `69,500 × 8 µs = 0.556`. It passes, with little room left.
2. Solve `20 µs × (5N² + 115N) = 0.6`, so `5N² + 115N = 30,000`. `N = (−115 + √(13,225 + 600,000)) / 10 = (−115 + 783.1) / 10 ≈ 66.8`. The 100-player test fails. First cut `u`: most players send far fewer than 5 updates a second when they are not moving. Then measure again before adding zones.
3. The player term `u × N × (N − 1)` grows with `N²`, so it dominates at large `N`. The mob term grows only with `N`. Cutting the square term moves the ceiling more.

</details>

## 3. Mapping the persistence promise

Bring the week 1 table and add two columns: the **strategy** and the **transaction boundary**. The strategies are the ones in [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md).

| State | Acceptable loss | Strategy | Transaction boundary |
|---|---|---|---|
| Gold, items, level | None | Write-through | One transaction per trade, loot or craft |
| Position | Up to a minute | Periodic save, 60 s, and on logout | One row per player |
| Market listings | None | Write-through | Listing plus item escrow in one transaction |
| Mob state | All | Not saved | None |

The transaction boundary is where student worlds lose items. A craft that removes three reeds and adds one net must do both in one transaction, or a crash between them destroys the reeds. A trade must move both sides together. [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) showed the split save, and [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) showed how two concurrent trades duplicate an item. In the review, reviewers pick two actions from your design and ask you to name every row each one changes.

Check the commit rate against the capacity sheet. Write-through at 10 commits a second is fine. Write-through of position at 10 updates a second per player would be 1,000 commits a second at 100 players. That is why position uses a periodic save.

## 4. The decision record

End the review with a record of five to ten decisions, one line each, in this form:

> **D3.** One server process for the whole world. *Because* one process holds 111 players at 60% CPU in the worst crowd. *Revisit if* the week 6 load test shows p99 tick time above 80 ms at 100 bots.

Every decision needs a revisit trigger that someone could measure. "Revisit if it gets slow" is not a trigger. The record also lists **deferred** machinery (zone servers, a cache, area of interest), so nobody starts building it in sprint 3 because it seemed like a good idea.

Finish with the **sprint 1 proof**, one sentence that sprint 1 must make true. For *Saltmarsh*: "50 bots log in, walk, log out and log back in at the position they left, and the server survives a restart in the middle." Week 3 plans the sprint around it.

## Studio session plan

The studio meets for 3 hours. Teams are paired, and each team reviews the other.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Briefing: the four review questions and the decision record format | |
| 0:15 to 0:50 | Capacity sheet. Each team fills `capacity.csv` with its spike's `e`, its worst crowd and its host budgets, then runs `check_capacity.py` | Capacity output and `N_max` |
| 0:50 to 1:30 | Review A. Team A presents for 20 minutes. Team B and an instructor question it for 20 | Draft decision record for A |
| 1:30 to 1:40 | Break | |
| 1:40 to 2:20 | Review B, the other way round | Draft decision record for B |
| 2:20 to 2:45 | Each team revises its record: cuts, deferrals, revisit triggers, the sprint 1 proof | Final decision record |
| 2:45 to 3:00 | Instructor sign-off: each team reads its sprint 1 proof and its largest cut | Sign-off or a named concern |

## Deliverables

Due before the week 3 session, in `docs/architecture/` in the team repository.

- **Architecture diagram** (one page) showing processes, the database and what talks to what.
- **Capacity sheet** (`capacity.csv`) with the spike's measured `e`, and the saved output of `check_capacity.py` showing `PASS`.
- **Spike note**: how `e` was measured (code, machine, number of runs), in a few lines.
- **Persistence map**: the week 1 table with strategy and transaction boundary added.
- **Decision record** with revisit triggers, the deferred list and the sprint 1 proof.

The instructor reruns the checker and checks each decision for a measurable trigger. See [lab 02](../labs/lab02.md).

## Common failure modes

- **Architecture from the textbook.** The diagram copies MMO302's largest system. Fix: justify every box with a number from the capacity sheet or a line of the persistence promise.
- **Average crowd.** The sheet assumes players spread over five areas. Fix: use the worst crowd your design allows, usually the town or the encounter.
- **Guessed `e`.** No spike was run, so `e` is a number from the internet. Fix: measure it, even crudely, on the machine that will host the alpha.
- **Items in two places.** Gold lives in the server's memory and the database, and nobody knows which wins after a crash. Fix: the persistence map names the source of truth for every row.
- **No revisit triggers.** Decisions are final until they fail in public. Fix: every decision names a measurement that would reopen it.

## Review checklist

The instructor signs off the architecture milestone when:

- [ ] `check_capacity.py` prints `PASS` at `headroom = 2` with a measured `e`.
- [ ] The worst crowd is identified and used in the sheet.
- [ ] Every "None" loss in the persistence promise maps to write-through with a named transaction boundary.
- [ ] Every component on the diagram is justified by the capacity sheet or the persistence map.
- [ ] The decision record lists deferred machinery and a measurable revisit trigger for each decision.
- [ ] The sprint 1 proof is one testable sentence that includes a restart.

## Sources

- Warcraft Wiki, "Stress test" (read September 2026). WoW Classic stress tests on 22 to 23 May, 19 to 20 June and 25 to 26 July 2019; level cap of five on stress test realms.
- Wikipedia, "World of Warcraft Classic" (read September 2026). Released 26 August 2019; layering used at launch.
- Warcraft Wiki, "Layering" (read September 2026). Added in patch 1.13.2 at the Classic launch; each layer a copy of the outdoor world with its own NPCs and objects; realms reduced to a single layer on 13 November 2019, before phase 2.
- CCP Logibro, "Battle for 6VDT-H: summary and numbers" (EVE Online news, 30 July 2013), as cited in MMO302 week 1. Peak of 4,070 pilots in one system; one tenth of normal speed for most of the battle.
- Wikipedia, "Eve Online" (read September 2026). Concurrency record of 65,303 on 5 May 2013.
- The *Saltmarsh* team, its spike result and all parameter values in section 2 are invented for teaching. The 0.6 CPU budget and the headroom of 2 are course conventions.
