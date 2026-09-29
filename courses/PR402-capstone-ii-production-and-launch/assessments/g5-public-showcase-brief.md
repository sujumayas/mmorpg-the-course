# PR402 · Launched game brief 5: the game at the public showcase

**Weight:** 8% of the course grade, inside the launched game component (40%).
**Assigned:** week 12. **Due:** the week 15 public showcase. The operations record for weeks 12 to 15 is due at the start of the showcase, in `production/showcase/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 9, launch](../lectures/w09-launch.md) (what "launched" means here), [week 11](../lectures/w11-live-ops-week-2-operating-rhythm.md) (the rhythm you keep until the showcase) and [week 14](../lectures/w14-post-mortem.md) (the evidence you present).

## What this milestone proves

That the game the team launched in week 9 is still live, still operated by the rhythm it set, and good enough that strangers at the showcase want to keep playing. This is the only brief in the course that marks the game as played. The other launched game briefs mark how it was run.

The showcase is a public event. Visitors play on stations connected to your production servers, alongside your real players, and a panel of two staff and one guest from outside the program visits each team. The panel plays for 15 minutes before it hears any presentation, so it meets the game the way a player does.

## Gates

- **G1. Still live.** The production server is up and reachable from outside the venue at the start of the showcase. Stations connect to production, not to a local build.
- **G2. On call during the event.** One team member holds the pager for the whole event, following the week 11 rota rules, and is not the person presenting.
- **G3. No private data on screen.** Dashboards shown to visitors show aggregates only.

A team that fails G1 presents a recorded session and its operations record, and rows 1 and 2 are capped at 40%.

## Deliverables

1. **The live game** on production, with the latest patch and a public page (store, itch.io or your site) with the code of conduct, known issues and patch note history.
2. **Showcase stations**: two or more machines, a one-page start guide, and a new-player path that reaches the game's first social moment within 15 minutes.
3. **A live dashboard** on a screen: CCU now, CCU today, crash rate per 100 player-hours this week, and the cohort table.
4. **A 10-minute presentation** for the panel: the game in two minutes, then launch and operations in numbers (forecast against actual for launch, the week 11 interrupt fraction before and after the buy-back, the patch forecast against actual, the economy decision), then one decision the team would make differently, with its evidence.
5. **Operations record, weeks 12 to 15**: daily review log, incident log and postmortems, rota as run, uptime per week, and the week 12 patch's expected numbers checked against actual.

## Evidence required

| Evidence | Format | How the panel checks it |
|---|---|---|
| Build | Tag of the running build, deploy log | Checks the station build matches the latest tag |
| Uptime | Monitoring history, weeks 12 to 15 | Reads uptime per week and matches outages to incident log entries |
| Incident log | Timestamped entries and postmortems | Picks one incident since week 12 and asks the on-call person how it was mitigated |
| Telemetry | Dashboard queries | Asks the team to rerun the crash-rate query live |
| Playtest data | New-player funnel for accounts created at the showcase | Checks how many showcase visitors reached the first social moment |
| Player-facing record | Public page, patch note history, known-issues post | Checks the page is current |
| Patch follow-up | Expected-number list with actual values | Compares one expected number with its query |

## How it is marked

The panel plays first, then hears the presentation, then asks questions for five minutes. Each panellist scores alone and the panel agrees a mark. The guest's scores count for rows 1 and 2 only. The operations record is marked by the instructor from the folder.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| The game as played | 25 | Pillars from PR401 visible in 15 minutes of play; the new-player path reaches a social moment; systems hold together with strangers in the world | Pillars only visible in the slides; visitors stuck in the tutorial |
| Stability during the event | 15 | No SEV1 during the showcase, or one handled by the on-call person by the rota with a player message, while the team keeps presenting | Server down with nobody assigned; restarts by whoever is nearest |
| Operations since week 12 | 20 | Daily reviews continued; every incident logged with a postmortem where required; rota followed; uptime reported honestly | Rhythm dropped after the patch; gaps in the log |
| Numbers in the presentation | 20 | Each claim is a number with its source and `n`; forecasts shown beside actuals, errors included | Claims of success with no numbers; only the good results shown |
| Handling questions | 10 | Answers with a number and a pointer to the record; says "we do not know" when the data cannot say | Reassurance; a teammate answers every question |
| Public page and players | 10 | Page current; code of conduct linked; patch history complete; real players treated fairly during the event (no showcase-only items or wipes) | Stale page; visitors given advantages over real players |
| **Total** | **100** | | |

## Builds on

- [PR401 week 3, pillars and vision](../../PR401-capstone-i-pre-production/lectures/w03-pillars-and-vision.md) (the pillars the panel looks for) and [PR401 week 14, pre-production review](../../PR401-capstone-i-pre-production/lectures/w14-pre-production-review.md).
- [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md).
- [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (the dashboard).
- [MMO308 week 3, cohorts](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) and [week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md).
- [MMO407 week 14, presentations](../../MMO407-launch-scaling-and-post-mortems/lectures/w14-presentations.md) (presenting a launch with numbers and answering the panel).
