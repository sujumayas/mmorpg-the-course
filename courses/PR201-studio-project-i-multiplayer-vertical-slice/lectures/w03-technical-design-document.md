# PR201 · Week 03 — Technical Design Document

**Why this matters:** Your scope sheet says what the slice contains. It doesn't say how six people will build it without breaking each other's work, or which part might not be buildable at all. The technical design document (TDD) answers both before sprint 1 starts. The most useful page in it is the risk register, because that page decides what you try first.

**You will be able to:**
- Write a TDD for a networked slice that fixes the engine version, topology, authority rules, tick and send rates, replication list and asset pipeline.
- Compute a per-client bandwidth budget for your slice from entity count, bytes per entity and send rate.
- Compute risk exposure, spike value and spike return for each technical risk, and choose which spikes fit in sprint 1.
- Explain how the time of discovery changes a risk's loss, and redo the ranking when it does.

**Before class:** [CS202 week 3](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) section 4 (choosing a topology) and [CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) section 2 (bandwidth budgets). Godot Engine documentation (stable, 4.x), "High-level multiplayer" (about 30 minutes). Bring your locked scope sheet.

**Prerequisites from earlier courses:** [CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) for intent-only messages and validation. [CS202 week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md) for the network test matrix. [PR101 week 2](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w02-git-fundamentals-and-branching.md) and [PR101 week 3](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w03-asset-workflows-and-large-files-lfs.md) for branching and large files. [AR101 week 14](../../AR101-visual-foundations-for-games/lectures/w14-pipeline-export-atlases-import-settings.md) and [AU101 week 5](../../AU101-audio-for-games/lectures/w05-implementation-in-engine.md) for the art and audio pipelines. [CS201 week 12](../../CS201-game-engine-architecture/lectures/w12-serialization-and-save-files.md) (section 4) and [DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) (section 3.1) for the save format and the atomic write in TDD section 11.

---

## 1. What a TDD is for

A **technical design document** records the technical decisions the whole team must follow, and the reasons behind them. It is not a manual for the engine and not a full class diagram. Think of it as the page a new team member reads to avoid breaking the build on day one, plus the page the team rereads when two people disagree about how something should work.

A good TDD for this course fits in six to ten pages and has these twelve sections. The last two feed alpha criteria A2 and A6 in week 10. DB201 runs alongside this course and has only reached its week 1 by now, so version 1 of those two sections asks for what you can already build. Version 2, with the database and the full tracking plan, is marked at alpha:

| Section | Decides | Taught in |
|---|---|---|
| Engine and versions | Engine version, plugins, export targets. Nobody upgrades mid-semester without a team decision | PR101 week 13 |
| Topology and hosting | Dedicated server, listen server or relay, and where the server runs during tests | CS202 week 3 |
| Authority | What the server owns, what the client may predict, what the client may never send | CS202 week 4 |
| Rates and budgets | Server tick rate, snapshot send rate, bytes per entity, per-client bandwidth | CS202 week 13 |
| Replication list | Every replicated object, its properties, who owns it, and how it is sent | CS202 weeks 5 and 7 |
| Message list | Every client-to-server request, with its validation checks | CS202 week 4 |
| Repository and builds | Branching rules, LFS patterns, the build command, versioning | PR101 weeks 2, 3 and 13 |
| Asset pipeline | Source formats, export settings, scale, naming, import presets for art and audio | AR101 week 14, AU101 week 5 |
| Test plan | Network profiles you test under and what each build must pass | CS202 week 14 |
| Risk register | What might stop you, how likely, how costly, and what you will try first | Section 2 below |
| Persistence | Version 1: the saved character record and its format version, when the server saves, and a file save with an atomic write (temporary file, flush, rename). Version 2 at alpha: schema, transactions and grant ids | CS201 week 12, DB201 week 1; version 2 from DB201 weeks 2, 5 and 6 |
| Tracking plan | Version 1: at least six server-side events and the playtest question each answers. Version 2 at alpha adds properties and storage | Week 7 of this course; version 2 from DB201 week 10 |

Each row is a decision, and each decision has one owner. If a section says "TBD", the risk register needs a matching line.

## 2. Worked example: which spikes go into sprint 1?

### The hook

Respawn runs *Apex Legends* servers at 20 Hz. In an April 2021 developer post, Respawn explained the choice with numbers. A match starts at about 60 kB/s per player at 20 Hz, and 60 Hz would be about 180 kB/s, with CPU cost rising the same way. The rate was a decision made on paper with its costs written down. Players argue about it, but the team knew what the other options cost.

Riot did the same in the other direction. Its 2020 post on *Valorant*'s 128-tick servers starts from a budget of 7.8125 ms per tick and a target of 2.34 ms of server time per game, then describes the engineering needed to reach it. The number came first, and the work was organized around proving it could be met.

Your TDD makes the same kind of commitment at a smaller scale. Some of its decisions rest on things nobody on your team has done before. The question for this week is which of those uncertain decisions you test first, and how much of sprint 1 you spend testing them.

### The model

A **risk** is something that may happen and would cost you hours if it did. For each risk `k`:

```
RE_k    = p_k × L_k                  risk exposure, in expected hours lost
ΔRE_k   = (p_k − p'_k) × L_k         exposure removed by a spike
net_k   = ΔRE_k − s_k                value of the spike after paying for it
ret_k   = net_k / s_k                return per spike hour
```

- `p_k` is the probability, between 0 and 1, that the risk happens if you do nothing. Estimate it as a team, in steps of 0.1.
- `L_k` is the loss in hours if it happens: rework, workarounds, cut features.
- A **spike** is a short, timeboxed experiment that answers one yes-or-no question. `s_k` is its cost in hours.
- `p'_k` is the probability left after the spike. A spike rarely drives it to zero.

Barry Boehm defined risk exposure as probability times loss in his 1991 *IEEE Software* paper on software risk management. It also drives his spiral model (1986, published more widely in 1988), where the risks decide how much effort each part of the project gets. The ranking rule adds one step. **Order spikes by return, not by exposure**, and fund them from the top until the spike budget runs out. A spike with `net ≤ 0` costs more than it saves, so accept that risk and watch it.

Alistair Cockburn separates a spike from a **walking skeleton**. A spike is thrown away after it answers its question. A walking skeleton is the thinnest end-to-end version of the real system, built to production habits and kept. Sprint 1 in this course builds the walking skeleton and runs the spikes next to it.

### Numbers you can check

The *Hollowmarch* team listed six technical risks. Their spike budget for sprint 1 is 20 hours.

| Risk | `p` | `L` (h) | `RE` | Spike question | `s` | `p'` | `ΔRE` | net | return |
|---|---|---|---|---|---|---|---|---|---|
| R1 30 server-owned enemies won't stay in sync at 20 Hz | 0.3 | 60 | 18.0 | Can 30 synced enemies stay under 12 kB/s per client? | 6 | 0.1 | 12.0 | 6.00 | 1.00 |
| R2 Movement feels bad at 100 ms round trip | 0.5 | 40 | 20.0 | Does predicted movement pass a blind feel test at 100 ms? | 8 | 0.2 | 12.0 | 4.00 | 0.50 |
| R3 Character export arrives at wrong scale or loses clips | 0.4 | 30 | 12.0 | Does one rigged character with two clips import at 1 unit = 1 m? | 4 | 0.1 | 9.0 | 5.00 | 1.25 |
| R4 Home players can't reach a host behind NAT | 0.6 | 20 | 12.0 | Can a home client join a lab server through the relay? | 3 | 0.1 | 10.0 | 7.00 | 2.33 |
| R5 Remote footstep sounds double-trigger | 0.3 | 10 | 3.0 | Do replicated animation events fire once per step? | 3 | 0.1 | 2.0 | −1.00 | −0.33 |
| R6 Headless server export fails on lab machines | 0.2 | 15 | 3.0 | Does a command-line export run headless on a clean machine? | 2 | 0.05 | 2.25 | 0.25 | 0.13 |

Total exposure is 68 expected hours, about a fifth of the team's 312 plannable hours. That number alone justifies the week.

Rank by return and fund from the top:

| Order | Risk | Spike hours | Running total | Decision |
|---|---|---|---|---|
| 1 | R4 | 3 | 3 | Spike in sprint 1 |
| 2 | R3 | 4 | 7 | Spike in sprint 1 |
| 3 | R1 | 6 | 13 | Spike in sprint 1 |
| 4 | R2 | 8 | 21 | Over budget. Spike in sprint 2 |
| 5 | R6 | 2 | 15 | Spike in sprint 1 |
| 6 | R5 | 3 | | Accept, since net is negative |

Look at R2. It has the **largest exposure** on the sheet, and it doesn't make the sprint. Its spike is expensive and leaves a lot of doubt behind (from 0.5 to 0.2), so each spike hour buys less than the others. R4, with half R2's exposure, comes first, because three hours nearly remove it.

Lab 03's `check_risks.py` reproduces both tables and prints the decisions.

### When the loss depends on the date

The model treats `L` as fixed. It isn't. If the team finds out in week 4 that predicted movement feels bad, the fix is a change to one system that nothing else depends on yet, and 40 hours is fair. If they find out at alpha in week 10, the combat, the boss and the hit feedback have all been tuned against the bad movement, and the loss might be 80.

Rerun R2 with `L = 80`. Exposure becomes 40, `ΔRE` becomes 24, net 16, return 2.00. R2 jumps to second place. Funding from the top gives R4 (3), R2 (8) and R3 (4) for 15 hours. R1 (6) would make 21 and no longer fits, and R6 (2) takes the total to 17. The spike that was deferred is now in, and R1 is deferred instead.

The lesson is to **estimate `L` as the cost of finding out when you would find out**. For a risk you defer, that date is the day the deferred spike runs. The *Hollowmarch* team asked when combat tuning starts. The answer was sprint 2. If the R2 spike is the first task of sprint 2, in week 6, nothing has been tuned against the movement yet and `L = 40` still holds. So they kept the first ranking, put the R2 spike at the top of the sprint 2 backlog, and wrote a rule in the register: "if the R2 spike slips past the first day of sprint 2, rerun with `L = 80`." Deferring a risk is fine. Deferring it without a date is how it reaches alpha.

### The same idea elsewhere

**Insurance.** An insurer prices a policy from probability times loss, the same product as `RE`. A spike is like fitting a smoke alarm. You pay a small fixed cost to lower the probability, and it is only worth it when the drop in expected loss is bigger than the price.

**Security threat models.** Security teams rank threats by likelihood and impact and fix the cheapest large reductions first. A patch that closes a likely hole in one hour comes before a redesign that closes a worse one in a month. The CS202 week 4 validation checklist is a threat model in this form.

**The Riot and Respawn posts.** Both published a number first and spent engineering time proving it. A spike question is the same kind of statement. "12 kB/s per client with 30 enemies" can be tested, while "networking might be slow" cannot.

### Eyes-open judgment

Probabilities from a student team are guesses. That is fine. The point is to make the guesses visible so someone can challenge them, not to be precise. Two traps are worth naming. The first is the risk nobody lists because nobody on the team knows enough to fear it. Ask the instructor and one other team to read your register for missing lines. The second is a spike with no question. "Look into networking" has no end and no answer. Each spike needs a yes-or-no question and a timebox, and it stops when either runs out.

Accepting a risk is a real decision, not a shrug. R5 is accepted, so the register says who notices if footsteps double-trigger (the audio primary, in every sprint review) and what the fallback is (disable remote footsteps).

### Check yourself

1. The R3 spike comes back "no". The export arrives at 100 times scale. The team estimates that fixing the pipeline costs 6 hours now. What was the spike worth, and what would you write in the register?
2. A new risk appears. The boss's second phase needs synchronized physics debris. `p = 0.5`, `L = 30`, spike cost 6 hours, `p' = 0.3`. Is the spike worth running, and would you rather cut the debris?

<details><summary>Answers</summary>

1. It turned a 0.4 chance of losing 30 hours later into a known 6-hour fix now. The register changes R3 to "happened, fixed in sprint 1, 6 h", and the art pipeline section of the TDD gets the corrected export settings. The spike is worth its 4 hours even though the answer was bad. A spike that finds a problem is doing its job.
2. `RE = 15`, `ΔRE = 0.2 × 30 = 6`, net = 6 − 6 = 0, return 0. The spike saves exactly what it costs, so the rule says accept the risk. But accepting leaves 15 expected hours on the sheet, and a cut costs almost nothing. Non-synchronized, client-side debris removes the risk (and the synchronization cost) completely. When a risk comes from a feature, removing the feature is often the cheapest spike.

</details>

## 3. A bandwidth budget for your slice

The rates section of the TDD needs a number, and CS202 week 13 gives you the model. For a first estimate, compute what one client downloads per second:

```
bytes per snapshot = header + E × b
download per client = send_rate × bytes per snapshot
server upload       = players × download per client
```

For *Hollowmarch* with 3 players, 30 enemies and up to 6 projectiles, `E = 40`. At `b = 12` bytes per entity (position, facing, state and health, packed as in CS202 week 5), with a 28-byte IPv4 and UDP header plus 8 bytes of game header, one snapshot is `36 + 480 = 516` bytes. That fits in one packet under a typical 1,200-byte safe payload. At 20 snapshots per second, each client downloads 10,320 bytes per second, about 10.3 kB/s. The server uploads three times that, about 31.0 kB/s.

That gives the R1 spike its question. If the engine's default replication sends 30 enemies at more than 12 kB/s per client, the team either packs the data by hand or sends enemies less often than players.

If your team uses Godot 4, as PR101 did, the documented building blocks are an `ENetMultiplayerPeer` for the connection, `@rpc` functions for requests, and `MultiplayerSpawner` and `MultiplayerSynchronizer` nodes for replication. The server always has peer ID 1. A `MultiplayerSynchronizer` sends on every network frame unless you set `replication_interval`, so write your send rate in the TDD and set it in the project. Don't let the default decide it.

## 4. Keeping the TDD true

A TDD that is written once and never updated is worse than none, because people trust it. Three habits keep it honest:

- **One owner per section**, named at the top of the section. The owner updates it when the decision changes.
- **A change log** at the top of the document. Each entry has a date, a section and one line. Sprint reviews end with "what in the TDD changed?"
- **Answers flow back.** Every spike result goes into the register and into the section it affects, on the day it comes in.

## Studio session plan

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Scope sheet feedback: each team hears one challenge from the instructor | Challenges logged |
| 0:15 to 0:55 | TDD sections in parallel. Programmers take topology, authority, rates and replication. Artist and audio take the pipeline section. Producer takes repository, builds and test plan. Designer drafts the message list with a programmer | Draft of every section |
| 0:55 to 1:20 | Bandwidth budget. Compute the slice's per-client download and set the send rate | Rates section with numbers |
| 1:20 to 1:30 | Break | |
| 1:30 to 2:15 | Risk register. Each person writes risks alone for 10 minutes, then the team merges them, estimates `p`, `L`, `s` and `p'`, and runs `check_risks.py` | Ranked register |
| 2:15 to 2:40 | Swap registers with another team. Each team adds at least one risk the other missed and challenges one `L` | Two new lines per register |
| 2:40 to 3:00 | Rerun the ranking, set the sprint 1 spike list, lock scope and TDD version 1.0 | Tagged commit `tdd-1.0` |

## Deliverables

Due before next week's studio session.

- **TDD version 1.0** in `docs/tdd.md`, from the lab 03 template, with an owner on every section and no "TBD" without a matching risk.
- **Risk register** (`risks.csv` in the lab 03 format) and the `check_risks.py` output, with the sprint 1 spike list.
- **Locked scope sheet** from week 2, updated if the TDD changed any estimate.
- A **git tag** `tdd-1.0` on the commit that contains all three.

See [lab 03](../labs/lab03.md) for the template and rubric.

## Common failure modes

- **Engine tutorial as TDD.** Pages on how the engine's networking works in general. Fix: write only decisions about *your* slice and their reasons.
- **"TBD" everywhere.** Fix: each TBD becomes a risk with a spike question, or the owner decides now.
- **Risks that are fears, not events.** "Networking is hard." Fix: write what would happen and what it would cost, such as "30 enemies exceed 12 kB/s per client".
- **Spikes that become features.** The spike code is good enough, so it ships. Fix: spike code lives on a branch named `spike/…` and is deleted after the answer is recorded. The walking skeleton is rebuilt properly.
- **One programmer writes it all.** Fix: art and audio write their own pipeline sections. The pipeline is where cross-discipline slices break.

## Review checklist

- [ ] Engine and version fixed, with an upgrade rule.
- [ ] Topology, hosting for tests and authority written, with every client message in intent form and a validation line.
- [ ] Tick rate, send rate and per-client bandwidth computed and written.
- [ ] Replication list covers every object in the must tier.
- [ ] Art and audio pipeline sections written by their primaries, with scale, naming and import settings.
- [ ] Risk register has at least six risks, each with an owner and a yes-or-no spike question, and `check_risks.py` passes.
- [ ] Sprint 1 spike list fits the budget, and every accepted risk has a watcher and a fallback.
- [ ] Tag `tdd-1.0` exists.

## Sources

- Respawn Entertainment, "What Makes Apex Tick: A Developer Deep Dive into Servers and Netcode" (Apex Legends news, ea.com, 28 April 2021). 20 Hz servers, about 60 kB/s at match start, about 180 kB/s at 60 Hz. As cited in CS202 week 13.
- Randall, B. "VALORANT's 128-Tick Servers" (Riot Games technology blog, 31 August 2020). 7.8125 ms per tick and a 2.34 ms target per game. As cited in CS202 week 13.
- Boehm, B. W. (1991). "Software Risk Management: Principles and Practices." *IEEE Software*, 8(1), 32-41. doi:10.1109/52.62930. Risk exposure as probability times loss.
- Wikipedia, "Spiral model" (accessed September 2026). Boehm's 1986 paper and 1988 publication; the model as risk-driven, with risk deciding the level of effort.
- Cockburn, A. "Walking skeleton" (alistair.cockburn.us, archived copy read September 2026). A walking skeleton as a tiny end-to-end implementation kept and grown, distinguished from a spike, which is thrown away after answering whether the team is heading the wrong way.
- Godot Engine documentation, "High-level multiplayer" and class reference "MultiplayerSynchronizer" (stable branch, version 4.7, read September 2026). `ENetMultiplayerPeer`, `@rpc`, server peer ID 1, `replication_interval` defaulting to every network process frame, and the link between `MultiplayerSpawner` and synchronizer visibility.
- The *Hollowmarch* risks, probabilities and costs are invented for teaching.
