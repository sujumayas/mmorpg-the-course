# PR401 · Week 07 — Technical Design

**Why this matters:** In PR402 your server will meet strangers, and strangers crowd into one spot to see what happens. A technical design written this week decides whether twice the expected crowd costs you a quarter of each server tick, or three quarters of it and a world that stutters. The difference is a few lines in the design that nobody will add in week 9 of PR402.

**You will be able to:**
- Write a technical design document for an MMO-scope capstone that names every process, what state it owns and how that state is saved.
- Compute a per-client bandwidth, a server egress and a replication CPU budget from CCU, visible entities, update rate and bytes per update.
- Compare the spread, hub and 2× load cases and decide which design change (an interest cap, a lower rate, a smaller update) brings the worst case inside budget.
- Plan time-boxed technical spikes that turn the riskiest numbers in the budget into measurements before vertical slice sprint 1.

**Before class:** Reread [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md), section 2, on why a crowd costs the square of its size (20 minutes), and open its interactive, [`w01-crowd-cost.html`](../../MMO302-mmo-server-architecture/examples/w01-crowd-cost.html). Skim [CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) for the per-packet overhead you will use. Bring the week 6 decision record, your risk register, and the server code from PR301.

**Prerequisites from earlier courses:** [MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (area of interest). [MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) (who is authoritative for what). [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (persistence strategies). [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (load testing and the knee). [MMO302 week 13](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (cloud deployment). [MMO404 week 4](../../MMO404-advanced-networked-simulation/lectures/w04-replication-prioritization-and-relevancy.md) (relevancy and priority). [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (builds and release checklists). The PR301 architecture review ([PR301 week 2](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w02-technical-architecture-review.md)).

---

## 1. What the technical design document is for

A **technical design document** (TDD) is the team's written answer to "how will this run, and how will we know it is working?" It is not a code tour. It exists for three readers.

- **The team in week 9 of PR402**, at 2 a.m., trying to find which process owns the inventory that just duplicated.
- **The new contributor**, who needs to add a quest type without reading the whole server.
- **The panel at the week 14 pre-production review**, who will check that the numbers in this document match the load test.

For a capstone the TDD is eight to twelve pages. Anything longer will not be kept current, and a TDD that is wrong is worse than none. Keep it in the repository beside the code, in Markdown, and change it in the same pull request as the code it describes.

You already have most of the parts. PR301 built a persistent world for 50 or more concurrent players. This week you decide what changes for the PR402 launch and write down why.

## 2. The sections

The lab 07 template has these sections. Each one answers one question.

1. **Targets.** Peak concurrent users (CCU) at launch, the load-test target (twice the launch CCU, for headroom), session length, and the world's size in zones and entities. Everything else is sized from this.
2. **Process map.** A diagram of every running process: gateway or login, world or zone servers, database, chat and social services, telemetry collector. For each, what state it owns and what it may never do. MMO302 week 10 explains why chat and guilds usually live outside the world server.
3. **Authority table.** For each gameplay action (move, attack, loot, trade, craft), who decides the outcome and what the client is trusted with. MMO302 week 6 and MMO309 week 2 give the rules. An empty cell here is next semester's exploit.
4. **Data model and persistence.** The tables or documents, which writes are transactional (trades, crafting that consumes items), which are periodic (position, health), and the save interval. MMO302 weeks 7 and 8 and DB201 week 5 cover the choices.
5. **Message catalog.** Every message type, its direction, its size in bytes, its rate and whether it must arrive reliably. This is the input to section 4's budget.
6. **Budgets.** Bandwidth per client, server egress, replication CPU per tick, database writes per second. Computed for three load cases. Section 4 shows how.
7. **Build, deploy and observe.** How a commit becomes a running server, how you roll back, and which three metrics tell you the server is healthy. MMO302 weeks 13 and 14 and PR101 week 13.
8. **Decisions and spikes.** A short log of each architecture decision with the alternatives you rejected, and the spikes planned to test the risky numbers (section 5).

## 3. Choose the smallest architecture that meets the target

Students reach for zone servers, sharding and microservices because the lectures described them. Your launch target is probably between 50 and 200 CCU (week 2 showed how to set it). MMO302 week 1 showed that a single process can hold a crowd of that size if you control who sees whom. The extra processes buy you scale you will not need and failure modes you will certainly get: handoff bugs, split-brain inventories, a message bus that drops events.

So the default for a capstone is one world process, one database, one gateway, and chat inside the world process unless you have a reason. Every process you add needs a line in the decisions log that says which target it serves and what the load test showed without it.

The same logic applies to technology. A new engine or a new database in pre-production is a risk, not a feature. If the team wants one, it goes into the risk register from week 6 with a spike attached.

## 4. Worked example: will one server hold the launch weekend?

### The hook

In April 2011 CCP described a mechanism for EVE Online called time dilation. EVE runs one shared universe, and when thousands of pilots jump into one star system, the server for that system has to tell every pilot about every other pilot. Most of that work is tied to the game clock: weapons cycle, ships move, modules activate. CCP's answer was to slow the clock. Under time dilation the game in that one system runs slower, down to 10% of normal speed, so a second of game time takes ten seconds of real time. Players still fight, just in slow motion, instead of the node falling over.

That is a technical design decision made in response to one fact: the cost of a crowd grows with the square of its size. MMO302 week 1 derived it. Your capstone will not see thousands of players in one place. It will see sixty, or a hundred and twenty on a good night, and strangers will gather at the spawn point, the market and the raid. Does your design survive the square?

### The model

For one client and one server:

```
update size       u = e × s + o                        bytes per update to one client
client downstream B = u × r                            bytes per second
                  B × 8 / 1000                         kbit/s
server egress     G = N × B                            bytes per second
entity updates    U = N × e × r                        per second
replication CPU   U × t                                core-seconds per second
per tick          (U / r) × t                          time spent replicating each tick
```

- `N` is the concurrent players in the load case.
- `e` is how many entities one client receives updates about. Without an interest cap, in a crowd, `e = N − 1`. With an area-of-interest cap (MMO302 week 3, MMO404 week 4), `e = min(N − 1, k)` for a cap `k`, filled nearest first.
- `s` is the bytes per entity update after quantization and delta compression (CS202 weeks 5 and 7). Measure it.
- `o` is the per-packet overhead. IPv4 and UDP headers are 28 bytes. Add your own protocol header if you have one.
- `r` is the update rate to clients in hertz, often the server tick rate.
- `t` is the server time to prepare and serialize one entity update for one client. Measure it in a spike.

The course's budget lines for a launch are these. A client downstream at or under 128 kbit/s, so players on weak connections can join. Replication at or under half of each tick at the 2× load-test case, so simulation and persistence keep the other half. Egress is not capped, but you must write its total for the weekend in gigabytes and check it against your host's current price and any free tier.

### Numbers you can check

*Emberfall*'s draft design: launch target `N = 60`, the figure the week 4 storage risk (R2) was written against, and a load test at 120. Update rate `r = 10` Hz. The PR301 build measured `s = 20` bytes per entity update and `t = 5` microseconds per entity update per client. The PR301 server runs in a managed language with a general-purpose serializer, which is why `t` is not smaller. These are the sample team's measurements, not general values. Overhead `o = 28` bytes.

Three load cases:

- **Spread.** Players spread across the valley, about 15 in view each.
- **Hub, no cap.** Everyone in the town market on the first evening, which is where *Emberfall*'s pillars send them. `e = N − 1`.
- **Hub, capped.** The same crowd with an interest cap of `k = 40` nearest entities.

| Case | `N` | `e` | `u` (bytes) | Client kbit/s | Egress Mbit/s | Updates/s `U` | CPU (cores) | Replication ms per 100 ms tick |
|---|---|---|---|---|---|---|---|---|
| Spread | 60 | 15 | 328 | 26.2 | 1.6 | 9,000 | 0.05 | 4.5 |
| Hub, no cap | 60 | 59 | 1,208 | 96.6 | 5.8 | 35,400 | 0.18 | 17.7 |
| Hub, capped | 60 | 40 | 828 | 66.2 | 4.0 | 24,000 | 0.12 | 12.0 |
| Load test, no cap | 120 | 119 | 2,408 | 192.6 | 23.1 | 142,800 | 0.71 | 71.4 |
| Load test, capped | 120 | 40 | 828 | 66.2 | 7.9 | 48,000 | 0.24 | 24.0 |

Check the uncapped load-test row by hand. `u = 119 × 20 + 28 = 2,408` bytes. At 10 Hz that is 24,080 bytes a second, times 8 is 192,640 bits, which is 192.6 kbit/s. For 120 clients, egress is `120 × 24,080 = 2,889,600` bytes a second, or 23.1 Mbit/s. Updates: `120 × 119 × 10 = 142,800` a second. At 5 microseconds each that is 0.714 core-seconds per second, or 71.4 ms of every 100 ms tick.

Read the table against the budget lines.

- **The spread case tells you nothing.** It is the case teams test by accident, because testers spread out. It passes every line with room to spare.
- **The uncapped hub passes at launch, barely.** 96.6 kbit/s is under the client line and 17.7 ms is well under half a tick. A team that only tests its launch target signs off here. But a 1,208-byte update is right at the size of a safe UDP payload, about 1,200 bytes, so any extra message in the same tick splits the update into two packets.
- **Doubling the crowd quadruples the cost.** From 60 to 120 players, replication goes from 17.7 ms to 71.4 ms per tick, four times as much, and the client stream doubles to 192.6 kbit/s. The load test fails both lines. The server cannot finish replication and simulation inside one tick, the tick stretches, and every player sees the market stutter. This is the failure EVE's time dilation manages on purpose. Yours would happen by accident, on the evening your game gets a mention somewhere and twice the expected crowd turns up.
- **The cap fixes it with one number.** With `k = 40`, the 120-player load test needs 24 ms per tick and 66 kbit/s per client. The cost grows with `N`, not `N²`, because each client's `e` stops growing at 40.

And the weekend bill. At the uncapped launch hub rate, 0.725 MB/s for 48 hours is `0.725 × 172,800 = 125,245` MB, about 125 GB of egress. Capped, it is about 86 GB. Look up your host's current egress price per GB before you commit to a host. Prices change and free tiers differ, so the TDD records the date you checked.

### Cross-game recognition

- **EVE Online** keeps every player in the one system and slows the clock, so the square still costs the same per game-second but the game-seconds come more slowly. It trades game speed for server load.
- **World of Warcraft Classic** launched on 26 August 2019 with **layering**: several copies of the outdoor world on one realm, each with its own players, mobs and resource nodes. Players see only their own layer. In this week's terms, layering lowers `N` for each copy so that `N × e` stays manageable. It trades a shared world for load, and Blizzard turned it off in November 2019 once launch crowds thinned.
- **Your interest cap** keeps everyone in one world and one clock but lets each client see only the nearest 40. It trades completeness of view. MMO302 week 2 and MMO404 week 6 show more variations. Each is a different answer to the same `N × e × r` product, and each costs players something different.

### Eyes-open judgment

An interest cap is a design decision with player-facing costs, which is why it belongs in a document the designers read. With `k = 40`, sixty players at market day will not all see each other, and a stall-holder may not see the buyer standing at the back. A town raid with 25 attackers and 25 defenders will show some players a fight with a few of the enemy missing. Decide which entities always make the cut (your group, your town's defenders, the player you are trading with, your target) and put that priority rule in the TDD.

The model also leaves things out. Chat, combat events and inventory messages add traffic. Resends on loss add more. Measure `s` and `t` in the real build, not in a unit test, and treat the table as a lower bound until the load test says otherwise. The 2× load-test target exists because the table is optimistic.

## 5. Spikes: turn assumptions into measurements

A **spike** is a time-boxed piece of throwaway work whose only output is a number or a yes or no. Every budget input you have not measured is a spike candidate. For *Emberfall* they were:

- Measure `s` for the player entity with the real component set. One day. Output: bytes per update, median and p95.
- Measure `t` with 120 headless bots in the market. Two days. Output: replication ms per tick at 60 and 120, and the knee from MMO302 week 11.
- Measure town storage write time under 60 and 120 bots against R2's trigger (p95 above 50 ms). One day. This retires the last of R2's exposure from week 6.

Each spike has an owner, a time box and a result written into the TDD. A spike that runs over its time box stops, and the result is "unknown, rated as a risk". Spikes are not features. They do not appear in the demo. They are the cheapest insurance you will buy all year.

## Studio session plan

Week 7 meeting, 3 hours. Two teams pair up and review each other's drafts.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:20 | Targets agreed: launch CCU, load-test CCU, zones, session length | Section 1 of the TDD filled in |
| 0:20-0:55 | Process map and authority table on the whiteboard, photographed | Sections 2 and 3 drafted |
| 0:55-1:30 | Message catalog and the budget sheet for three load cases (lab 07) | `budget.csv` with measured or flagged inputs |
| 1:30-1:40 | Break | |
| 1:40-2:20 | Paired review: the other team tries to break your design with a crowd, a trade and a crash mid-save | List of holes, each with an owner |
| 2:20-2:45 | Spike plan: owners, time boxes, what counts as a result | Section 8 drafted |
| 2:45-3:00 | Producer check-in with the instructor: which week 6 risk each spike retires | Risk register updated |

## Deliverables

Due at the start of week 8, in `docs/tdd.md` and `preproduction/week07/`:

1. **Technical design document**, eight to twelve pages, with all eight sections.
2. **Budget sheet** in the [lab 07](../labs/lab07.md) format with at least the spread, hub and 2× load-test cases. The checker `net_budget.py` must print `PASS`.
3. **Spike plan**: at least three spikes with owner, time box and expected output. Results are due at the end of week 9.
4. **Updated risk register** from week 6, with each technical risk linked to a spike or a design change.

## Common failure modes

- **Architecture by lecture.** Zone servers and a message bus for 60 players. Each process needs a target it serves and a measurement that justifies it.
- **Testing the spread case.** The team runs a load test with bots that wander, sees green graphs, and meets the hub on launch night. Script at least one hub case.
- **Budgets with no measured inputs.** `s` and `t` copied from a lecture. The table then describes someone else's game. Measure them, or flag them and plan the spike.
- **An empty authority cell.** "The client sends the loot it picked up." Every action that changes items or currency is decided by the server.
- **A TDD that drifts.** Written in week 7, never touched again. Change it in the same pull request as the code.
- **Egress forgotten.** The server runs fine and the bill arrives. Write the weekend gigabytes down and the date you checked the price.

## Review checklist

The instructor checks in the submission and at the week 8 stand-up:

- [ ] Targets state launch CCU and a load-test CCU at least twice as high.
- [ ] Every process in the map owns named state, and no state is owned twice.
- [ ] The authority table has no empty cells for actions that change items, currency or health.
- [ ] Persistence names the save interval and which writes are transactional.
- [ ] The budget sheet covers spread, hub and 2× load test, and `net_budget.py` prints `PASS`.
- [ ] Every case over a budget line has a design change or an accepted risk with a reason.
- [ ] `s` and `t` are measured or have a spike planned with an owner and a time box.
- [ ] The decisions log records at least three decisions with rejected alternatives.

## Sources

- CCP Veritas, "Introducing Time Dilation (TiDi)", EVE Online dev blog, 22 April 2011. Most of the load in large engagements tied to the game clock; slowing the clock reduces load in proportion. https://www.eveonline.com/news/view/introducing-time-dilation-tidi
- EVE University Wiki, "Time dilation" (accessed September 2026). Maximum slowdown to 10% speed, one game second taking ten real seconds; server load growing with the square of players on grid. https://wiki.eveuniversity.org/Time_dilation
- Warcraft Wiki, "Layering" (accessed September 2026). Introduced with World of Warcraft Classic in patch 1.13.2 on 26 August 2019 to relieve overcrowding; each layer a separate copy of the outdoor world with its own NPCs and nodes; disabled before Phase 2 on 13 November 2019. https://warcraft.wiki.gg/wiki/Layering
- MMO302 weeks 1, 3 and 11, and CS202 weeks 5, 7 and 13 of this program, for the square law, interest management, load testing and packet overhead.
- The *Emberfall* targets and measurements (`s = 20` bytes, `t = 5` µs) are invented for teaching and continue weeks 1 to 6. The 128 kbit/s client line and the half-tick replication line are this course's teaching values, not industry standards.
