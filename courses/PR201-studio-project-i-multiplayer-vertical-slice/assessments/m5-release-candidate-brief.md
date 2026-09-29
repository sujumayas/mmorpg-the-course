# PR201 · Milestone 5 brief: release candidate

**Weight:** 6% of the course grade, inside the milestones component (50%).
**Assigned:** week 13. **Due:** the fix log and player-facing known issues list at the end of the week 14 meeting. The final RC, go/no-go record, submission package and post-mortem data before the week 15 showcase.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 14, release candidate](../lectures/w14-release-candidate.md) and [lab 14](../labs/lab14.md).
**Builds on:** [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md), [PR101 week 10, bug tracking](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md), [DB201 week 13, privacy and retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) and [DB201 week 14, backups and disaster recovery](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md).

## What this milestone proves

That the build you show in week 15 is the build you tested. The week 14 rules apply. From `v1.0.0-rc.1` the code is frozen except for fixes approved at triage. Every change makes a new RC, built from a clean checkout and checked again. The showcase build is the last RC that passed go/no-go, not a newer one from the night before.

This milestone is small in weight because it mostly checks that the process works. It is also the milestone where a team that skipped the process loses the most time.

## Deliverables

Due at the end of the week 14 meeting, in `production/week14/`:

1. **RC fix log** (lab 14 format). Every open bug with priority, change type, regression rate `r_i`, decision (fix, remove, known issue) and, for each fix, author and reviewer. `check_rc.py` prints `PASS`.
2. **Known issues list** written for players.

Due before the week 15 showcase:

3. **Final RC**, tagged `v1.0.0-rc.N`, and the **go/no-go record** naming it. The rule was written before the meeting.
4. **Submission package** as in week 14 section 4: versioned builds and the server build with its start command, README, CHANGELOG with a heading per RC, `KNOWN_ISSUES.md`, credits with every asset's source and licence, and the telemetry note.
5. **Data safety.** A backup of the persistent database taken from the RC server and a restore onto a fresh instance, with row counts before and after.
6. **Post-mortem data** committed under `production/postmortem-data/`, as listed in week 14 section 5.
7. **Showcase plan.** Machines, network, who runs the server, and the fallback if the server fails.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Reproducible RC | Tag, build script, artifact hash | A team member who is not the build owner rebuilds from the tag; the file lists match |
| Clean start | README in the package | Starts the RC from a clean download using only the README |
| Fix log | `check_rc.py` output | Reruns it; checks each high-risk fix is alone in its RC with a reviewer who is not the author |
| Regression rates | `r_i` values with tracker references | Checks they cite the tracker or are marked as defaults with a reason |
| Go/no-go | Rule with a date before the meeting, and the record | Compares dates and the named RC with the tag |
| Restore test | Command log and row counts | Asks a team member to repeat the restore |
| Telemetry note | Section in the package | Checks identifiers are removed or anonymised and the endpoint is off or team-controlled |

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| RC discipline | 20 | Every change produced a new tagged RC built from a clean checkout; rebuilt by a non-build owner | RC patched by hand, or only the build owner can build |
| Fix log | 20 | `check_rc.py` passes; every P1 fixed or its feature removed; high-risk fixes isolated and reviewed | Checker fails, or high-risk fixes bundled |
| Go/no-go | 15 | Rule written before the meeting; record names the RC that passed; showcase uses it | Rule written afterwards, or a newer untested build shown |
| Known issues | 10 | Written for players; matches the tracker | Markers find unlisted issues |
| Submission package | 15 | Every item present, including licences and the telemetry note | Missing licences, README or telemetry note |
| Data safety | 10 | Backup and restore tested; counts match | No restore test |
| Post-mortem data and showcase plan | 10 | Exports committed; showcase plan has a tested fallback | Data not frozen; no fallback |
| **Total** | **100** | | |

## Late and missing work

The RC cannot be late in practice. The showcase uses the last RC that passed go/no-go. If there is none, it uses the beta build and this milestone scores at most 30.
