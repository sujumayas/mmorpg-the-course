# MMO308 · Live-ops plan brief: a live-ops plan and the analysis report behind it

**Weight:** 40% of the course grade.
**Assigned:** week 8, after Lab 08. **Milestone 1:** end of week 10. **Milestone 2:** end of week 13. **Final submission:** start of week 15, followed by a 15-minute presentation and viva in week 15.
**Work mode:** individual, or a pair with a signed contribution statement. In a pair, each partner answers the viva questions alone.
**Lectures:** all fourteen. Most directly [week 1](../lectures/w01-what-live-ops-is.md) (the plateau and its levers), [week 2](../lectures/w02-kpis-dau-mau-stickiness-arpdau.md) (the KPI tree), [week 3](../lectures/w03-cohorts-and-retention-curves.md) (the retention triangle), [week 7](../lectures/w07-segmentation.md) (segments), [week 8](../lectures/w08-event-design-and-calendars.md) (events and calendars), [week 9](../lectures/w09-patch-management-and-hotfixes.md) (rollouts), [week 12](../lectures/w12-economy-monitoring.md) (alarms), [week 13](../lectures/w13-incident-response.md) (incidents) and [week 14](../lectures/w14-sunsetting-content-and-servers.md) (end of life).

## What this component is for

It assesses the course outcome "plan a live-ops calendar", and it uses the other two outcomes as evidence. A live-ops plan is the document a team runs from for the next quarter: what it will measure, what it will ship and when, what it will test, what wakes someone at night, and how the world ends. Every choice in it should trace back to a number in the analysis report.

A plan that lists twelve fun events earns little here. A plan whose calendar names the lever each event pulls, predicts gross and net lift with a baseline method fixed in advance, keeps events for the same segment apart, stages its patches with a stated expected harm, and budgets its false alarms earns a lot.

## Choose your game

Pick one of two options by Milestone 1 and keep it.

- **Option A, your studio project.** Use the persistent world you are building in [PR301](../../PR301-mmo-studio-project-i-persistent-world-prototype/syllabus.md), with its playtest telemetry. Small playtest numbers are fine. Scale them to a stated launch scenario and say which numbers are measured and which are assumed.
- **Option B, the course reference game.** Treat the lab datasets as one invented MMO in its first six months: `activity.csv` from [Lab 02](../labs/lab02.md) for KPIs, `installs.csv` and `activity.csv` from [Lab 03](../labs/lab03.md) for cohorts, the log from [Lab 04](../labs/lab04.md) for funnels and churn, `daily_hours.csv` from [Lab 08](../labs/lab08.md) for events, `economy.csv` from [Lab 12](../labs/lab12.md) for the economy and `make_history()` from [Lab 14](../labs/lab14.md) for the long-run decline. Generate each with its lab's seed. The datasets were not built to agree with each other, so state the scale you use (for example, 5,000 DAU) and rescale where needed.

Either way, the game is yours to describe in one page: genre, platforms, business model, server structure (one shard, realms or a single shared world) and team size. The server structure decides your experiment units and rollout stages, so choose it on purpose.

## What you hand in

### The analysis report

At most 2,500 words plus tables and figures, as `analysis.pdf`. It establishes the facts the plan relies on. Each section leads with numbers and names the lecture model it uses.

1. **Health baseline.** The KPI tree with current values, MAU next to an engagement-weighted KPI, and one rolling-window echo annotated if your data has an event (week 2). The layer cake with the plateau `I × L` and the launch share at the latest week (week 1).
2. **Cohorts.** The retention triangle and the D1, D7 and D30 series by install day, with every seam and diagonal labelled as a cohort, one-day period or lasting period effect, and the standard error of the largest step (week 3).
3. **Funnel and churn.** A closed, time-boxed cohort funnel with the box justified by `1 / (q + h)`, and a churn window per segment with its measured or modelled false-churn share (week 4).
4. **Segments.** One mix and rate decomposition of a real change in your data, with the ordering named and margins on every cell (week 7).
5. **Economy.** The alarm layer run on your economy series, with each alarm labelled as incident, planned change or noise (week 12).

### The live-ops plan

At most 3,500 words plus tables, as `plan.pdf`. Seven sections.

1. **Goals and KPIs.** Three KPI targets for the next 12 weeks, each with a definition footnote, a guardrail it is paired with, and the plateau lever it pulls (`I`, `w`, `qs` or `qt`). Say what each target is worth at the plateau.
2. **The 12-week calendar.** A week-by-week table of every event, patch and sale. Each event states its family, target segment, goal as "metric, segment, target", announcement lead, baseline method (fixed now), expected gross lift, expected net lift and incrementality ratio. Use a recovery model with parameters you fitted or justified (Lab 08). No two events for the same segment may overlap. Mark the weeks in which each measurement window closes.
3. **Experiments.** Two experiments that run inside the calendar, each as a one-page plan with unit, trigger, primary metric, guardrails, MDE with `deff`, duration in whole weeks and stopping rule. At least one must test something the calendar depends on. Show that they do not share players in a way that tangles their results (salts, segments or timing).
4. **Patches and rollouts.** For each patch in the calendar, what can be staged by player, by realm or not at all, the stage plan with its expected harm for a stated bug rate and detection rate, the canary size from the rule of three, the way back for each part, and your team's hotfix break-even harm rate.
5. **Feedback and voting.** The channel for each kind of question, the survey trigger with its `π` logged, the unit of each question, the loop measures you will publish (time to acknowledge, time to decision, coverage), and whether players vote on anything. If they do, the threshold with its blocking group `τ × (1 − T)` and the categories you will not poll.
6. **Monitoring and incidents.** The alarm specification (series, rule, `k`, `h`, direction, baseline, owner, page or ticket) with a false-alarm budget met by simulation, the severity table, incident roles for your team size, the communication cadence, and three kill switches the calendar's riskiest features ship behind, with their `R`.
7. **End of life.** Your Lab 14 memo, revised for this game: which content you would retire first by hours share over cost share, the six-month ratios you will watch, the cost step to maintenance mode, the notice period, the sales cut-off, what happens to player data, and what the last event is.

### Code and data folder

Every table and figure in both documents comes from code in the folder, with a `README.md` that gives the exact command for each and the seeds. Standard-library Python with `.venv/bin/python`. Spreadsheets are accepted for charts if the numbers they plot come from the code.

## Milestone 1: game and health baseline (end of week 10, 10 points)

Submit the one-page game description, your option (A or B), and draft sections 1 and 2 of the analysis report: the KPI tree with values, the layer cake with its plateau, and the retention triangle with at least one labelled effect. Feedback within a week tells you whether your data can carry the plan.

## Milestone 2: calendar and experiments (end of week 13, 10 points)

Submit draft plan sections 2 and 3: the 12-week calendar table with gross and net lift for each event, and the two experiment plans. Feedback within a week focuses on overlaps, baselines and sizing, because those are the parts hardest to fix late.

## Final presentation and viva (week 15)

Fifteen minutes per student or pair. Five minutes presenting the calendar and the one number you are least sure of. Ten minutes of questions in the style of the [exam bank](exam-bank.md), rewritten with your plan's own numbers. For example, "Your double-XP event has a ratio of 0.4. What pre-dip did you assume, and what does the net lift become if players learn the pattern and the pre-dip doubles?" or "Your canary is 2% of 60,000 players. What bug rate does it catch with 95% probability at your detection rate?"

## Rubric

| Criterion | Excellent (full marks) | Adequate (about half) | Weak (little or none) | Points |
|---|---|---|---|---|
| Milestone 1 | Game described with a deliberate server structure; KPI tree, plateau and a labelled triangle on real or reference data | Parts present, one missing or unlabelled | Not submitted | 10 |
| Milestone 2 | Calendar with gross and net per event and two sized experiment plans | Calendar without net lift, or experiments unsized | Not submitted | 10 |
| Analysis report | All five sections lead with numbers from the named lecture models; every effect in the triangle typed and dated; decomposition and alarms labelled; uncertainty stated | Most sections present, some claims without numbers or margins | Descriptive only, or models misapplied | 20 |
| Goals, KPIs and calendar | Targets tied to plateau levers with guardrails; calendar events each with segment, goal, fixed baseline method, gross, net and ratio from a fitted recovery model; no same-segment overlaps; measurement windows marked | Calendar sound but lift estimates not tied to the model, or one rule broken | A list of events without goals or numbers | 20 |
| Experiments and patches | Two plans sized with `deff` and a tested stopping rule; patches classified by what can be staged, with expected harm, canary size, ways back and a hotfix break-even | One of the two parts thin | Missing or unsized | 15 |
| Feedback, monitoring and incidents | Survey trigger and unit per question; loop measures; alarm spec meeting a simulated budget; severity table, roles and kill switches with `R` | Present but budget chosen by feel or kill switches unnamed | Missing | 10 |
| End of life | Revised Lab 14 memo with retirement candidate, ratio watch, cost step, notice, sales cut-off, data handling and last event | Present, some parts generic | Missing | 5 |
| Presentation and viva | Calendar explained clearly; weakest number named honestly; questions answered with the plan's own numbers | Presentation clear, some questions answered from memory rather than the model | Cannot explain the plan | 10 |
| **Total** | | | | **100** |

In a pair, the viva mark is individual. If a partner cannot explain a section of the plan they claim in the contribution statement, that section is re-marked for them alone, using the Full, Partial, Weak and None scale from the [analytics labs brief](analytics-labs-brief.md).

## Late work

Milestones are accepted up to 3 days late at half marks, because their value is the feedback. The final submission is accepted up to 48 hours late, marked out of 70, and the presentation slot does not move. Extensions follow university policy.

## Ethics and integrity

- Plans must pass the week 5 and week 8 fairness checks. No test on prices or power that players can compare in the same world without a stated reason. No event whose core reward a player with five hours a week cannot reach, unless you say why. No experiment designed to push vulnerable players to spend.
- Real-game facts in your plan (a cadence, a policy, a threshold) must be cited with their era, as the lectures do. Invented numbers must be labelled as assumptions.
- You may reuse all of your own lab code and text. Code or text from other students is not allowed. Acknowledge documentation, forum and AI help in one line.
