# PR301 · Final world brief: stabilization and showcase

**Weight:** 30% of the course grade (the "final world" component).
**Assigned:** week 13. **Stabilization:** week 14, with the feature freeze from the start of the week 14 session. **Due:** the release candidate pack at the start of the week 15 session; the showcase in week 15.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 14, stabilization](../lectures/w14-stabilization.md), with [week 8](../lectures/w08-sprint-3-review.md) (severity scale and kill switches) and [week 13](../lectures/w13-beta-open-class-playtest.md) (the beta evidence). **Lab:** [lab 14](../labs/lab14.md).
**Builds on:** [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) and [week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) (persistence and transactional integrity), [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md), [week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) and [week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (transactions, races, backups), [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) and [week 14](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w14-designing-an-economy-from-scratch.md) (the economy as designed), [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (hotfix decisions), [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (why switching a system off does not fix its dupe) and [PR201 week 14](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w14-release-candidate.md) (the release candidate).

## What this component proves

That the team shipped the world the course asked for, in a build it can install, back up, restore and show. The course brief from [week 1](../lectures/w01-pitch-and-world-pillars.md), section 1, is the checklist.

| Requirement | Shown by |
|---|---|
| Persistent | A live restart at the showcase, and the week 14 restore on the candidate |
| 50+ concurrent players | The beta peak export, or a showcase peak on the server metric, humans only |
| An economy | Named faucets and sinks in the build; the ledger reconciles to zero over the showcase session |
| Grouping | A party that shares credit, loot and a channel |
| One group encounter | A party kills the boss live; a solo player at party level loses |
| Server-authoritative | The client sends intent and the server decides; the reviewer asks to see the damage and loot code paths |

A system switched off with a tested week 8 kill switch and a showcase note is a production decision and costs nothing here, as long as the world still meets the brief without it. The encounter cannot be switched off.

## Deliverables

At the start of the week 15 session:

1. **Triage table and fix budget** (lab 14) passing `check_stabilization.py`, with fix hours and reopen rate from tracker history and expected arrivals from sprint 5 testing.
2. **Release branch** with a bug ID on every merge since the freeze.
3. **Release candidate** tagged with version and changelog, with the [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) checklist completed against it.
4. **Backup and restore record** on the candidate: restored into a clean environment, server started against it, three named characters logged in and checked.
5. **Clean install record**: a teammate who did not build the candidate installs the client from the release artifact on a machine that has never run the game.
6. **Soak test**: two hours at 50 bots on the candidate, with memory and p99 tick exports.
7. **Daily must-fix count** from the freeze to the candidate.
8. **Showcase notes**: every switched-off system and every reclassification, with its reason and evidence.
9. **Showcase build**: the last candidate that passed the checklist.

At the showcase (20 minutes per team):

10. **Live world** on the team's host, started from the showcase build, with the dashboard on screen.
11. **Live persistence**: the reviewer names a change (a craft, a trade, a guild invite); the team makes it, restarts the server, and shows it survived.
12. **Live encounter**: a party of team members and guests runs the boss.
13. **Ledger at close**: the residual over the showcase session, recomputed on screen.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Tracker history | Closed bugs from sprints 1 to 5 with hours and reopen flag | Recomputes `q` and the mean fix hours for one severity |
| Beta telemetry | Week 13 export | Traces two S2 or S3 frequencies to it |
| Release branch log | `git log` of the release branch | Every merge references a bug ID |
| Soak data | Two-hour memory and per-tick exports | Looks for slow growth in memory and p99 |
| Restore | Backup file and restore log | Repeats the restore on a clean machine in the session if time allows |
| Server logs | Showcase session logs | Matches the live restart to the log and checks for errors after it |
| Ledger | Showcase session ledger and money supply | Residual must be zero, or its cause named on the spot |
| Concurrency | Beta or showcase player-count export, humans only | Reads the peak from the export |

## How it is marked

The instructor and a second reviewer mark the pack and the showcase separately and agree a mark. Stabilization is judged on decisions as much as on fixes. The *Saltmarsh* team in the week 14 guide faced 67.1 hours of effective demand against 45.5 hours of capacity. It flipped the market kill switch (one S1 and four S2 bugs), reclassified three visual bugs with telemetry, kept the dupe open at S1 on main, and did not work the weekend. That is full marks on the budget and switch rows, whatever the final bug count.

Two things cap this component at 40 however good the rest is. One is a showcase build that loses or duplicates value in the live restart. The other is any S1 downgraded to make the list fit.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Course brief met | 20 | Every requirement in the table above shown live or from exports | A requirement missing, or shown only in the editor |
| 50+ humans | 10 | Server metric shows 50 or more humans at the beta or the showcase | Neither export reaches 50 (partial credit follows the M6 shortfall report) |
| Live persistence | 12 | Reviewer's change survives the live restart; no loss or gain of value | Change lost, or value duplicated (component capped at 40) |
| Economy integrity | 8 | Showcase ledger residual is zero; money supply covers every place currency lives | Residual non-zero and unexplained |
| Triage and fix budget | 12 | Week 8 scale applied; no S1 downgraded; frequency from telemetry on every S2 and S3; demand with reopen rate and arrivals at or below capacity, margin stated | Estimates from the meeting; data bug reclassified |
| Kill switches and reclassification | 8 | Only tested week 8 switches used, re-checked on the candidate, noted, bugs kept open on main; reclassifications backed by telemetry | New switch built during the freeze; bug closed as "won't fix, disabled" |
| Release discipline | 10 | Release branch with bug IDs on every merge; tagged candidate with changelog; checklist complete | Features merged after the freeze |
| Backup, restore, install, soak | 12 | All four done on the candidate and recorded; soak shows no slow growth, or growth is filed | Any of the four missing |
| Showcase | 8 | Runs from the showcase build; dashboard on screen; the encounter kill and the restart go as planned or are handled from the runbook | Crash handled by improvising |
| **Total** | **100** | | |

## Late and missing work

The showcase cannot move. A pack that arrives up to 48 hours late is capped at 70 for its rows. A team whose showcase host fails runs from its restored backup on a lab machine. That is what the restore record is for.
