# MMO308 — Live Operations, Analytics and Experimentation

Year 3, semester 6 · 4 credits · Prerequisites: DB201, MA102

Running a world after launch: KPIs, cohorts, retention, A/B tests, patches and events.

## Learning outcomes

- Define and compute core live-game KPIs
- Run and analyze A/B tests correctly
- Plan a live-ops calendar

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | What live ops is | [lecture](lectures/w01-what-live-ops-is.md) | [layer-cake](examples/w01-layer-cake.html) |
| 2 | KPIs: DAU, MAU, stickiness, ARPDAU | [lecture](lectures/w02-kpis-dau-mau-stickiness-arpdau.md) | [mau-window](examples/w02-mau-window.html) |
| 3 | Cohorts and retention curves | [lecture](lectures/w03-cohorts-and-retention-curves.md) | [retention-triangle](examples/w03-retention-triangle.html) |
| 4 | Funnels and churn | [lecture](lectures/w04-funnels-and-churn.md) | [snapshot-funnel](examples/w04-snapshot-funnel.html) |
| 5 | A/B testing: design | [lecture](lectures/w05-ab-testing-design.md) | [cluster-design-effect](examples/w05-cluster-design-effect.html) |
| 6 | A/B testing: statistics and pitfalls | [lecture](lectures/w06-ab-testing-statistics-and-pitfalls.md) | [peeking-simulator](examples/w06-peeking-simulator.html) |
| 7 | Segmentation | [lecture](lectures/w07-segmentation.md) | [segment-mix](examples/w07-segment-mix.html) |
| 8 | Event design and calendars | [lecture](lectures/w08-event-design-and-calendars.md) | [event-pull-forward](examples/w08-event-pull-forward.html) |
| 9 | Patch management and hotfixes | [lecture](lectures/w09-patch-management-and-hotfixes.md) | [staged-rollout](examples/w09-staged-rollout.html) |
| 10 | Player feedback loops: forums, surveys, polls | [lecture](lectures/w10-player-feedback-loops-forums-surveys-polls.md) | [who-gets-asked](examples/w10-who-gets-asked.html) |
| 11 | Community-voted design (Old School RuneScape polls — verify thresholds) | [lecture](lectures/w11-community-voted-design-old-school-runescape-polls.md) | [poll-threshold](examples/w11-poll-threshold.html) |
| 12 | Economy monitoring | [lecture](lectures/w12-economy-monitoring.md) | [faucet-alarm](examples/w12-faucet-alarm.html) |
| 13 | Incident response | [lecture](lectures/w13-incident-response.md) | [revert-or-fix](examples/w13-revert-or-fix.html) |
| 14 | Sunsetting content and servers | [lecture](lectures/w14-sunsetting-content-and-servers.md) | [sunset-forecast](examples/w14-sunset-forecast.html) |
| 15 | Final: live-ops plan + analysis report | [assessments](#assessment-materials) | — |

## Signature worked examples

- Retention curves: D1/D7/D30 cohorts plotted — spot the patch that broke onboarding
- Peeking at an A/B test inflates false positives — simulation

## Labs

- [MMO308 · Lab 01: The layer cake](labs/lab01.md)
- [MMO308 · Lab 02: Touches and play](labs/lab02.md)
- [MMO308 · Lab 03: The retention triangle](labs/lab03.md)
- [MMO308 · Lab 04: Funnels and churn from an event log](labs/lab04.md)
- [MMO308 · Lab 05: Design an experiment for a shared world](labs/lab05.md)
- [MMO308 · Lab 06: Peeking, boundaries and a broken split](labs/lab06.md)
- [MMO308 · Lab 07: Segment the retention drop](labs/lab07.md)
- [MMO308 · Lab 08: Measure an event and plan a calendar](labs/lab08.md)
- [MMO308 · Lab 09: Rollout planner](labs/lab09.md)
- [MMO308 · Lab 10: Who answered the survey?](labs/lab10.md)
- [MMO308 · Lab 11: The poll archive](labs/lab11.md)
- [MMO308 · Lab 12: Faucet alarms](labs/lab12.md)
- [MMO308 · Lab 13: Incident analysis and a blameless postmortem](labs/lab13.md)
- [MMO308 · Lab 14: Sunset forecast and recommendation](labs/lab14.md)

## Assessment materials

- [MMO308 · Exam bank: quiz, practice and viva questions](assessments/exam-bank.md)
- [MMO308 · A/B report brief: one experiment, designed and then read honestly](assessments/ab-report-brief.md)
- [MMO308 · Analytics labs brief](assessments/analytics-labs-brief.md)
- [MMO308 · Live-ops plan brief: a live-ops plan and the analysis report behind it](assessments/live-ops-plan-brief.md)

## Readings

- Seif El-Nasr, Drachen, Canossa (eds.) — Game Analytics (2013)

## Assessment

Analytics labs (40%), A/B report (20%), live-ops plan (40%)
