# PR201 · Milestone 2 brief: technical design document

**Weight:** 10% of the course grade, inside the milestones component (50%).
**Assigned:** week 2. **Due:** end of week 3, tagged `tdd-1.0`, before sprint 1 planning in week 4. **Reviewed:** week 4, first 30 minutes of the studio session. The spike results are reviewed at the [sprint 1 review](../lectures/w05-sprint-1-review.md).
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md). Every section names its owner.
**Session guide and lab:** [week 3, technical design document](../lectures/w03-technical-design-document.md) and [lab 03](../labs/lab03.md). The TDD is updated in [week 6](../lectures/w06-sprint-2-core-combat.md) (feedback table) and [week 8](../lectures/w08-sprint-3-content-and-progression.md) (progression stories). Those updates, and version 2 of sections 11 and 12 (database schema, transactions, grant ids and the full tracking plan), are marked at alpha.

## What this milestone proves

That the team has decided how the slice works before building it, and has written down the numbers that will tell it when a decision was wrong. A TDD in this course is short and specific. It says what runs where, what goes over the wire, how often, what is stored, what is logged, and what you are least sure of. It is not an engine tutorial.

The networking and persistence content is taught elsewhere. Link to it instead of explaining it again.

- [CS202 week 3, topologies](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md) and [week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md)
- [CS202 week 6, reliability over UDP](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w06-reliability-over-udp.md) and [week 7, snapshots and delta compression](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w07-snapshots-and-delta-compression.md)
- [CS202 week 8, client-side prediction](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) and [week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md)
- [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) and [week 14, testing under bad networks](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md)
- [CS201 week 12, serialization and save files](../../CS201-game-engine-architecture/lectures/w12-serialization-and-save-files.md) (versioned save formats and the atomic write, from last semester) and [DB201 week 1, why persistence is hard](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md) (the crash in the middle of a write)
- [PR101 week 3, asset workflows and LFS](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w03-asset-workflows-and-large-files-lfs.md) and [week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md)

## Deliverables

`docs/tdd.md`, from the lab 03 template, plus `docs/risks.csv` and `docs/risks.md`, all on the commit tagged `tdd-1.0`. That commit also holds the locked scope sheet from week 2, updated if the TDD changed any estimate.

The twelve template sections:

1. **Engine and versions.**
2. **Topology and hosting.** The choice, one reason and what it rules out.
3. **Authority.** A table of game state and its owner: position, health, damage, cooldowns, loot, XP, inventory.
4. **Rates and budgets.** Tick rate, send rate, bytes per snapshot, per-client download and server upload at the maximum player count, with the arithmetic shown and the margin against a stated limit.
5. **Replication list.** What is replicated, to whom and how often; which actions the client predicts, which it interpolates and which wait for the server.
6. **Message list.** Every message with its fields, size in bytes, rate and channel (reliable or unreliable).
7. **Repository and builds.** Branching, the build script and version numbering.
8. **Asset pipeline.** Written by the art and audio primaries: scale, naming, import settings, route into the build.
9. **Test plan.** The network profiles you will test under and the smoke test a build must pass.
10. **Risk register.** At least six risks, `check_risks.py` passing at your spike budget, the swap additions from another team, and a watcher and fallback for every accepted risk.

Sections 11 and 12 exist because alpha criteria A2 and A6 depend on them. DB201 runs in the same semester, and by week 3 it has covered only its week 1. So version 1 asks for what you can build now. The database version of section 11 and the full tracking plan are marked at alpha ([milestone 3](m3-alpha-brief.md)), after DB201 weeks 2, 5, 6 and 10:

11. **Persistence, version 1: a documented save format and a file-based save.** The character record the server saves (id, class, level, XP, inventory, and a format version number), one example file, when the server writes it (at least at level-up and logout), and a save routine that writes a temporary file, flushes it and renames it over the old one, so a crash leaves the old save or the new one and never half of each ([CS201 week 12](../../CS201-game-engine-architecture/lectures/w12-serialization-and-save-files.md), section 4; [DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md), section 3.1). The client never sends a value that goes into the save.
12. **Tracking plan, version 1.** At least six server-side events named, each with the playtest question it answers. Properties, storage and queries come after DB201 week 10.

A "TBD" is allowed only where a matching risk sits in the register.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Bandwidth arithmetic | Section 4, reproducible from section 6 | Recomputes one row from the message sizes |
| Risk register | `risks.csv`, checker output in `risks.md` | Reruns `check_risks.py` with your stated budget |
| Spike list | Sprint 1 spikes ranked by return, each with a yes-or-no question | Compares with the sprint 1 plan in week 4 and the results at the week 5 review |
| Section owners | Name under each heading | Compares with the RACI in the charter |

## How it is marked

The instructor and a second reader from the CS202 teaching team each read the TDD and mark it alone, then agree a mark. In the week 4 review each section owner answers one question on their section. A TDD in which one person wrote everything is marked the same, but the "team ownership" row drops, and the peer assessment will show it.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Decisions, not description | 10 | Every section is a decision about this slice with a reason; no bare TBD | Engine tutorial, or mostly TBD |
| Topology and authority | 15 | Topology justified; combat results, loot and XP decided on the server; every state item has one owner | Client decides damage or rewards, or owners are missing |
| Rates and budgets | 15 | Arithmetic reproducible, at maximum players, headers included, margin against a named limit | Numbers without derivation, or budget at one player |
| Replication and messages | 10 | Sizes, rates and channels for every message; predict, interpolate or wait decided per action | Messages without sizes; "we will use prediction" with no list |
| Persistence, version 1 | 10 | Save format documented with a version field and an example file; the server writes it at named moments; the save routine writes a temporary file, flushes and renames, and a crash test (kill the server mid-save) leaves a loadable file | Progression kept only in memory, the file is overwritten in place, or the client sends saved values |
| Tracking plan, version 1 | 5 | Six or more server events named, each tied to a playtest question | Events with no question, or client-only events |
| Builds and asset pipeline | 10 | Build script and versioning decided; art and audio sections written by their primaries | Generic, or written by a programmer for the artists |
| Test plan | 5 | Named network profiles and a smoke test with pass criteria | No bad-network testing planned |
| Risk register and spikes | 15 | Checker passes; spikes ranked by return with testable questions; accepted risks have watchers and fallbacks | Risks without owners; spikes chosen by exposure alone |
| Team ownership | 5 | Section owners answer their questions | One author, or owners cannot explain their sections |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. Sprint 1 may not start without a TDD. A team that has none by week 4 writes sections 2, 3, 6 and 10 in the first days of sprint 1, at the cost of sprint capacity.
