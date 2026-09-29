# PR301 · Milestone 4 brief: alpha, the first persistent weekend

**Weight:** 10% of the course grade, inside the milestones component (50%).
**Assigned:** week 8, when the go/no-go list is agreed. **Due:** the ops pack at the Thursday 18:00 freeze in week 9; the weekend evidence by the Monday after, untouched.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md). The on-call rota is also evidence for the operations criterion in the peer rating.
**Session guides:** [week 8, sprint 3 review and the alpha go/no-go](../lectures/w08-sprint-3-review.md) and [week 9, the first persistent weekend](../lectures/w09-alpha-first-persistent-weekend.md). **Labs:** [08](../labs/lab08.md) and [09](../labs/lab09.md).
**Builds on:** [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (hotfixes), [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (incident response and the incident log), [MMO308 week 12](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md) (economy alarms), [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (dashboards and alarms), [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (Little's law), [DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (restore drills), [DB201 week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) (consent and retention), [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) (rollback or ban) and [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (dupes).

## What this milestone proves

That the team can run a persistent world unattended from Friday 18:00 to Sunday 18:00, and learn from it. The alpha is an operation, not a playtest. It is marked on how the team prepared, how it ran the weekend and whether it kept the evidence. It is not marked on whether something broke. Something will. A crash handled from the runbook within the rota's 15 minutes scores better than a quiet weekend with no incident log.

## Deliverables

At the freeze, Thursday of week 9, 18:00:

1. **Go/no-go list** from week 8, every item answered yes or no with evidence, or with its planned response in place.
2. **Ops plan** `ops/alpha-weekend.md`: runbook of copyable commands, dashboard link, alarm list, on-call rota with backups, hotfix policy and incident log template.
3. **Lab 09**: sign-up sizing and rota passing `check_weekend.py`, with rates marked measured or guessed.
4. **Drill evidence**: timed restore on a second machine with a character logged in; `kill -9` crash drill with the loss window and the post-restart ledger residual.
5. **Consent notice** as shown to testers, with the data deletion date, and the exploit policy published before the weekend.
6. **Coordinated event time** agreed with the other teams at the board.

By the Monday after the weekend:

7. **Incident log** with an entry every shift, every deploy and every kill-switch flip.
8. **Exports, untouched**: telemetry events, the ledger, the tick log, the server logs and the final database backup.
9. **Turnout sheet**: sign-ups, logins, sessions, player-hours and event attendance, humans and bots separately.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Server logs | Raw logs for the weekend, with restarts | Finds every restart and matches it to an incident log entry |
| Tick log | Per-tick CSV for the weekend | Reads p99 by hour against the week 6 limits |
| Telemetry | Event export with `server_seq`, bots flagged | Counts humans and bots separately; checks sequence gaps |
| Ledger | Ledger export and hourly residual | Reruns the residual for two hours of the weekend |
| Backup and restore | Final backup file; restore drill timing | Restores the final backup on a clean machine and logs in one character |
| On-call | Rota file, incident log, alarm test record | Messages the on-call channel at a random hour; expects a reply within 15 minutes |
| Kill switch | Flip log from the freeze | Flips one switch of the instructor's choice at the freeze, with clients connected |
| Playtest notes | Report channel and observer notes from the Saturday event | Reads them for handled reports and exploit disclosures |

## How it is marked

The freeze pack is marked on Thursday, the weekend conduct from the logs and the spot-check, and the evidence rows on the Monday export. The instructor does not mark the size of the crowd. The course outcome of 50 humans is checked at the [beta](m6-beta-open-class-playtest-brief.md). Here the crowd is marked on whether the team sized it from stated rates and reported humans and bots apart.

The *Saltmarsh* weekend in the week 10 guide would lose marks on the alarm row, because the hourly residual alarm was muted on Friday night and missed the mail dupe at 04:00. It would score well on incident response. Fay, on call, flipped the crafting kill switch at 05:05, and the hotfix went out at 11:00 after review.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Go/no-go at the freeze | 12 | Every item yes with evidence, or a planned response in place; no open S1 without a tested kill switch | Items unanswered, or an S1 downgraded to pass |
| Runbook | 12 | Every action is a copyable command; restart, restore and a kill switch run by a non-author before the weekend | Descriptions instead of commands; only the author can restart |
| Drills | 12 | Restore and crash drills timed; loss window matches the persistence map; post-restart residual is zero | Drills skipped, or residual not checked |
| Dashboard and alarms | 12 | Humans and bots apart, p99 tick, hourly ledger residual; one alarm triggered on purpose and received; no alarm muted without a fix | Mixed counts; alarms muted or never tested |
| Rota and weekend conduct | 12 | Every hour covered with a backup; no shift over six hours; entry every shift; spot-check answered in 15 minutes | Gaps in the rota or the log |
| Incident handling | 10 | Each incident logged with time, reason and person; S1 only hotfixes, each read by a second person; rollback first when a fix makes things worse | Tired unreviewed hotfixes; unlogged flips |
| Sign-up sizing | 8 | Rates stated and marked measured or guessed; plan for the gap; event time coordinated | Sign-up target without a model |
| Testers and data | 10 | Consent notice with data, purpose, access and deletion date shown before login; exploit and conduct policies published; no personal data in shared files | Notice missing, or tester names in bug reports |
| Evidence kept | 12 | All exports and the final backup handed in untouched on Monday; nothing wiped | World wiped, or exports missing |
| **Total** | **100** | | |

## Late and missing work

The freeze cannot move. A team that misses it launches on Saturday only and loses the go/no-go row. Weekend evidence that is late by up to 48 hours is capped at 70 for its rows. A wiped world scores 0 on the evidence row, because week 10 has nothing to check.
