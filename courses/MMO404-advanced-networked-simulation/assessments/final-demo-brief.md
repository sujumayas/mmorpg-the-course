# MMO404 · Final demo brief: a seamless two-server handoff

**Weight:** 60% of the course grade.
**Assigned:** week 2, with [Lab 02](../labs/lab02.md). **Milestone 1:** end of week 5. **Milestone 2:** end of week 10. **Final submission:** start of week 15, followed by a 15-minute live demo and a 10-minute viva in week 15.
**Work mode:** individual, or a pair with a contribution statement. In a pair, each partner answers the viva questions alone.
**Lectures:** all fourteen, most directly [week 2, seamless worlds and boundary handoff](../lectures/w02-seamless-worlds-and-boundary-handoff.md), [week 4, replication prioritization](../lectures/w04-replication-prioritization-and-relevancy.md), [week 7, time dilation revisited](../lectures/w07-time-dilation-revisited.md), [week 8, distributed simulation research](../lectures/w08-distributed-simulation-research.md), [week 9, server meshing concepts](../lectures/w09-server-meshing-concepts.md), [week 10, consistency models](../lectures/w10-consistency-models.md) and [week 13, cost engineering](../lectures/w13-cost-engineering.md).

## What this component is for

A seamless world hides its server borders from players, and the engineering that makes that possible is invisible when it works and catastrophic when it fails. One handoff bug in ten thousand becomes an item duplication on a busy evening. This assessment asks you to build the smallest system that has all the hard parts: two servers that share a border, players who walk and fight across it, and a network between the servers that delays, drops, duplicates and reorders messages. Then you prove, with logs and a checker, that it never has two owners, never loses or doubles an input, and never duplicates an item, including when a server pauses in the middle of a handoff.

It assesses the course outcome "design distributed simulation across many servers" directly, and the outcome "optimize replication for massive battles" through the ghost stream and the bandwidth report.

## What you build

A top-down 2D world 400 m wide and 500 m tall, with a border at `x = 0`. Server A owns the west, server B the east. Players are circles. They walk, and they have one attack with a range of a few metres that can hit a player on the other side of the border. The world also holds one treasure chest that sits 2 m inside B's side and respawns every 30 seconds, and one boss standing on the border with 500,000 health. No art is marked, and you must not use copyrighted characters, sprites or logos.

### Processes

- **Two zone servers**, A and B, each its own process, ticking at 10 Hz.
- **A gateway** that routes each client's inputs to the server it believes owns that player.
- **A directory** that grants ownership and issues epochs (week 9). It may run inside the gateway process, but it must be a separate object with its own log.
- **Bot clients**, each its own process or many per process, that send numbered inputs every tick and receive snapshots. At least two behaviours from the week 2 lecture: travellers who cross the border and dwellers who mill around a spot near it. A human-controlled client is welcome but not required.
- **A persistence stub**, a file or SQLite database where servers write player state and inventories. Every write carries the writer's epoch, and the stub rejects writes whose epoch is not current.

### Technical rules

- **Language and libraries.** Python 3.10 or later, standard library for everything that moves messages or decides ownership. You may use pygame, matplotlib or any drawing library for display and plots only. Another language is allowed with the instructor's written approval, under the same rule.
- **Real processes and sockets.** Servers, gateway and bots talk over UDP or TCP on `127.0.0.1`. The server-to-server link must go through a fault injector you control.
- **Seeds.** Every source of randomness takes a seed from the command line, and a run with the same seeds and settings produces the same ownership log.
- **Switches for the demo.** Command-line flags that the examiner will use: `--band W` (hysteresis width in metres, 0 allowed), `--no-fence` (the directory stops checking epochs), `--chest guess|forward`, `--link delay=D,loss=P,dup=Q,reorder=R` and `--seed S`.

### Required features

Each item names the lab that gives you a starting point.

1. **Handoff protocol (Lab 02).** The four roles (`authoritative`, `transferring`, `ghost`, `absent`), the hysteresis band, buffering of inputs that reach the old owner, forwarding after the `ack`, and strict in-order application on the new owner. The server-to-server link loses and duplicates messages in the demo, so `transfer`, `ack` and forwarded inputs need sequence numbers, retransmission until acknowledged, and receivers that ignore duplicates.
2. **Ghosts and visibility (week 2, Lab 04).** Each server holds ghosts of the other's players in a strip of width `R + w` with `R = 60 m`, and includes them in its clients' snapshots. Snapshots to each client respect a byte budget of your choice, filled in priority order by the fair-share rule or an accumulator. You log bytes sent per client per second.
3. **Cross-seam combat (week 2, section 4).** The attacker's owner checks the attack against its ghost of the target, and the target's owner applies the damage. Nobody changes the state of an entity it does not own.
4. **The chest (Lab 10).** Two policies behind `--chest`. Forward sends every claim to B and waits. Guess grants locally and reconciles, and your logs must count every reversal. Only one player may ever hold the chest's item.
5. **The boss (Lab 10).** Boss damage is a per-server grow-only counter merged by `max`. The boss's owner alone decides its death and rolls one loot drop.
6. **One clock (Labs 07 and 08).** Both servers tick on one shared schedule, with tick numbers in every message. State the border's lookahead from your attack's rules and show from logs how often a server stalled waiting for the other.
7. **Epoch fencing (Lab 09).** The directory bumps a player's epoch on every ownership grant. Servers attach their epoch to every write to the persistence stub and to every `transfer`. A server that learns its epoch is stale drops the player to a ghost.
8. **Fault injector.** Seeded delay (0 to 3 ticks), loss, duplication and reordering on the server-to-server link, set per direction. A pause command that freezes one server for a given time (for example 500 ms), during which the directory may reassign its players.
9. **Invariant checker.** A separate script that reads the logs of a run and checks, per player and per tick: at most one authoritative owner; every input applied exactly once and in sequence order; the chest's item held by at most one player; the boss dead at most once with at most one loot drop; and every persistence write from a stale epoch rejected. It prints `all invariants hold` or the first violation with its tick, player and seed.

## Milestones

| Milestone | Due | What you show | Marked as |
|---|---|---|---|
| 1 | End of week 5 | Servers A and B, the gateway and one bot as separate processes on real sockets. The bot walks across the border 100 times with `--band 5` over a link with 2 ticks of delay and no loss. The checker verifies the first two invariants from the logs. | 2 points, all or nothing |
| 2 | End of week 10 | Ghosts, cross-seam combat, the directory with epochs, the fault injector with loss and duplication, and 50 bots. The checker passes on 10 seeds with `delay=2,loss=0.05,dup=0.01`. One paragraph on what broke on the way. | 3 points: 3 if the checker passes on all 10 seeds, 2 on 8 or 9, 1 on fewer |

Milestones are short submissions on the course site: a commit hash, the checker output and a two-minute screen recording. They exist so that the week 15 demo is a demonstration, not a debugging session. Feedback on each milestone arrives within a week.

## The report

Put one `REPORT.md` in your repository, with every number carrying its unit, its settings and, where randomness is involved, its seed.

### 1. Correctness under faults

A test matrix of at least five link profiles (a clean link, delay only, loss and duplication, reordering, and the demo profile with all four), each run for 10 seeds with at least 200 bots for 5 minutes of simulated time, plus a pause test in which one server freezes for 500 ms during a handoff. For each cell, the number of handoffs performed and the checker's result. Then two runs with deliberate faults: once with `--no-fence` during the pause test, and once with one bug of your choice from Lab 02 step 4. Show the checker catching each, with the first violation it reports.

### 2. The seam

A sweep of handoffs per second and ghost count against band width, from 0 to 40 m, with your bots. Compare it with the week 2 lecture's table and model `S(w) = H(w) × E_h + G(w) × T × c_g`, using your own measured `E_h` (CPU time per handoff, both servers together) and `c_g`. State the band width you chose and why, and the handoffs per hour at that width.

### 3. Bandwidth and interaction

Bytes per second per client near the seam and far from it, with the budget you chose and the priority rule. The chest under both policies: measured claim rate, reversals per 100 claims under guess, the week 10 formula's prediction for the same `λ` and `W`, and the added latency under forward. The boss: the largest gap you observed between the two servers' health bars, compared with `D_B × W`.

### 4. Clock, lookahead and cost

The border's lookahead from your attack's rules, the share of ticks on which a server stalled, and what would happen to that share if you added an instant attack across the border. Then the cost of 1,000 player-hours of your demo from the week 13 model, using your measured bytes per client and one zone's capacity from week 1, with each term's share. Name the lever you would pull first.

### 5. What breaks first

Using the week 1 and week 9 models, the number of players your two servers could hold if everyone crowded onto the border. Name what fails first in your own system when you push past it (tick overrun, shaper backlog, checker violation), with the run that shows it.

## The demo and viva (week 15)

The demo is 15 minutes, run from a clean checkout on the lab machine with `.venv/bin/python`.

1. **Two minutes.** Start everything with one command. Show 200 bots crossing and fighting on the border, with a live counter of handoffs and ghost count on each server.
2. **Three minutes.** Set `--band 0` and then your chosen band, and show the handoff rate change.
3. **Four minutes.** The examiner chooses a seed and a link profile from your matrix. Run it for two minutes of simulated time and run the checker on its logs.
4. **Three minutes.** The pause test. Freeze a server during a handoff, show the directory reassigning players, and show the stale writes being rejected. Then repeat with `--no-fence` and show the checker finding the violation.
5. **Three minutes.** The chest under guess and forward with a crowd of bots clicking it, and the reversal counts.

The viva is 10 minutes of questions in the style of the [exam bank](exam-bank.md), rewritten with your numbers, for example "Your stall share was 4% at lookahead 2. What happens with a 30 ms link?" or "Show me the line that rejects a stale epoch, and the log entry it produced in the pause test."

## Rubric

Each row is scored in the same five bands as the labs (4, 3, 2, 1 or 0), and earns `points × band ÷ 4`. The milestones are scored as their table says.

| Criterion | Excellent (band 4) | Adequate (bands 2 to 3) | Missing or wrong (bands 0 to 1) | Points |
|---|---|---|---|---|
| Handoff correctness under faults | The checker passes on every cell of the matrix with 200 bots; retransmission and duplicate handling are in the protocol, not special cases; both deliberate faults are caught and explained | Passes on the clean and delay profiles, fails on some seeds under loss or duplication, with the cause diagnosed | Two owners or lost inputs on clean links, or no checker | 25 |
| Ghosts and seam cost | Ghost strip correct at every band width; sweep reproduces the shape of the week 2 table; `E_h` and `c_g` measured; band chosen from the data | Ghosts work, sweep present, constants assumed rather than measured | No ghosts across the border, or no sweep | 15 |
| Cross-seam interaction and consistency | Owner-applies rule holds in the logs; chest never duplicated under either policy; guess reversals compared with the week 10 formula; boss dies once with one drop and the health gap compared with `D_B × W` | Rules hold, measurements or comparisons partly missing | Chest or loot duplicated, or damage applied by a non-owner | 15 |
| Failure handling and fencing | Pause test passes with fencing and fails visibly without it; epochs on every write and transfer; stale owner drops to ghost | Fencing works, pause test partial or the `--no-fence` failure not shown | No epochs, or a stale write accepted with fencing on | 15 |
| Budgets report | Bandwidth, lookahead and stall share, and the cost of 1,000 player-hours computed from measured numbers, with shares and a named lever; "what breaks first" shown with a run | Numbers present, some assumed or unexplained | Report sections missing or copied from the lectures | 10 |
| Milestones | Both on time and passing | See the milestone table | Missed | 5 |
| Live demo and viva | Clean start from one command; every step within time; the examiner's seed passes; answers trace a number to the code and the log that produced it | Demo needs a restart or runs over; answers correct but vague about where numbers came from | Demo does not run, or the student cannot explain their own protocol | 15 |
| **Total** | | | | **100** |

## Rules that apply to everything

- **Your own work.** You may reuse any code from the lectures, labs and starter files, including your own Lab 02 and Lab 09 solutions. You may use documentation, forums and AI assistants to understand an error or an API, and you must list each use in one line at the end of the report. You may not submit code you cannot explain in the viva.
- **Reproducibility.** Every result in the report names the command, the seeds and the settings that produced it. The examiner may rerun any of them.
- **Honest failures.** A known bug that your checker catches and your report explains costs far less than a bug the examiner finds. If a cell of your matrix fails, say so and say why.
- **Late work.** The report and code are due at the start of week 15. Up to 48 hours late, the report sections are marked out of 80% of their points. The demo slot cannot be moved without a documented reason under university policy.
