# PR301 · Post-mortem and viva brief

**Weight:** 10% of the course grade (the post-mortem half of the "post-mortem and peer review" component). The peer review half is in the [peer assessment brief](peer-assessment-brief.md).
**Assigned:** week 13. **Due:** the team post-mortem and the individual reflection at the start of the week 15 session; vivas during week 15.
**Work mode:** mixed. The team document earns one shared score. The reflection and the viva are individual. This component is not adjusted by the peer factor.
**Guides:** [week 14](../lectures/w14-stabilization.md), section 5 (the evidence folder), [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md) and [MMO407 week 12, writing a post-mortem](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md). Question bank: [exam-bank.md](exam-bank.md).
**Builds on:** [PR201 week 14](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w14-release-candidate.md) and the PR201 post-mortem you already wrote. This one is about a world that ran for weeks, not a slice played once.

## What this component proves

That each student understands the world they helped ship well enough to explain its numbers, defend its decisions and say what they would do differently. The team document shows what the team learned. The reflection and the viva show what you learned, including about the parts you did not build.

## Deliverables

### Team post-mortem (one per team, 3,000 to 5,000 words)

1. **Timeline**: milestones, planned and actual, with every sprint's goal answered yes or no.
2. **Predictions against measurements**: each model the team used (pitch load, capacity, soak bound, camp utilization, tick fit, money budget, sign-ups, invitation target, fix budget) with the prediction, the measurement and the gap. At least six.
3. **Incidents**: every S1 found from the alpha on, its cause, how it was found, how long it was open and the class-of-bug fix.
4. **Decisions**: the three decisions that mattered most, including one the team now thinks was wrong, with the evidence.
5. **Cut and deferred list**: everything cut or deferred, with the reason at the time and a judgment now.
6. **What we would keep and change** for PR401, as specific practices with owners, not virtues.

### Individual reflection (one per student, 1,000 to 1,500 words)

1. Your role and what you owned, with ticket IDs.
2. One number you computed that changed a decision, and how.
3. One thing you got wrong and what the evidence showed.
4. One practice you will take into PR401 and how you will know it worked.

### Viva (one per student, 15 minutes)

The instructor and a second member of staff ask four questions from the [exam bank](exam-bank.md): two about systems you owned, one about a system a teammate owned, and one reflection question. You may bring the team's evidence folder and your reflection. You may not bring prepared answers.

## Evidence required

| Evidence | Format | How it is used |
|---|---|---|
| Evidence folder from week 14 | Beta exports, triage table, burn-downs, capacity and turnout numbers | Every claim in the post-mortem cites a file in it |
| Server logs and telemetry | Alpha and beta exports | Incidents and predictions are traced to them |
| Soak and load data | Lab 04, 06 and 13 files | The capacity story is checked against them |
| Playtest notes | Alpha and beta observer notes | Player-facing findings are traced to them |
| Tracker and hours log | Tracker export, personal hours log | The reflection's ownership claims are checked against them |

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| **Team document (shared)** | | | |
| Predictions against measurements | 12 | Six or more models, each with prediction, measurement, gap and a reason for the gap | Only successes listed |
| Incidents and causes | 8 | Every S1 with cause, discovery, time open and the class-of-bug fix | Symptoms only |
| Decisions and cuts | 10 | One wrong decision owned with evidence; every cut judged in hindsight | "Everything went well" |
| Practices for PR401 | 5 | Specific practices with owners and a check | Generic lessons |
| **Individual reflection** | | | |
| Ownership and evidence | 10 | Role and work traced to tickets and the hours log | Claims the records do not show |
| A number that changed a decision | 8 | The calculation, the decision and what happened | A number with no decision attached |
| An error and its evidence | 7 | Honest, specific, with what the data showed | Blame placed on others |
| **Viva** | | | |
| Own systems (two questions) | 20 | Explains the model, the numbers and the trade-offs in the team's own world | Recites the guide's example without the team's numbers |
| A teammate's system (one question) | 10 | Explains what it does, what it costs and how it failed or held | Does not know how it works |
| Reflection (one question) | 10 | Links a change in practice to evidence | Vague or defensive |
| **Total** | **100** | | |

## Late and missing work

A team document or reflection up to 48 hours late is capped at 70 for its rows. A student who misses the viva without an agreed reason scores 0 on the viva rows. Mitigating circumstances follow the university's policy and move the viva, not the standard.
