# PR401 · Milestone 4 brief: prototype 1

**Weight:** 15% of the course grade, half of the prototypes component (30%).
**Assigned:** week 4. **Due:** before the week 5 studio session, in `preproduction/week04/` and `prototypes/p1/`. **Reviewed:** at the start of week 5.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 4, prototype 1](../lectures/w04-prototype-1.md) with [lab 04](../labs/lab04.md).
**Builds on:** [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), section 2 (why a gate that can say stop is worth money), [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 4 (a prototype is not a vertical slice), [MMO405 week 2, quantitative methods](../../MMO405-research-methods-in-online-games/lectures/w02-quantitative-methods-overview.md), section 5 (deciding in advance what result would change your mind), and [MMO405 week 10, ethics](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md) (consent from playtesters).

## What this milestone proves

That the team spent its first 45 hours of prototyping where they remove the most risk, and came back with a result it wrote the pass mark for in advance. The *Emberfall* team chose R1 and R6 because their exposure removed per hour was 2.5 and 2.4. It skipped the siege, the most fun thing to build, because its ratio was 0.56. This milestone marks the choice and the honesty of the report. A prototype that refutes its claim scores as well as one that supports it.

## Deliverables

1. **Risk sheet** (`risks.csv`) with every load-bearing claim, `p` and `L` estimated by someone other than the risk's owner, and the checker output before (`check-output.txt`) and after (`check-output-after.txt`) the build.
2. **Prototype briefs** (`brief-Rn.md`), one per item, each committed before its first build commit: one question, the observable, the kill criterion, the fidelity and a "will not build" list.
3. **Prototype build or paper materials** in `prototypes/p1/`, runnable or usable by the instructor, with a README saying how to run it and what was faked.
4. **Result reports** (`result-Rn.md`), one page each, stating supported, refuted or unclear against the criterion, with raw observation notes attached.
5. **Claims sheet update** with evidence levels changed by the results.
6. **Time log** (`timelog.csv`) of actual hours per prototype by discipline against the planned cost `c`.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Prototype choice | `check_risks.py` output | Reruns it with the team's budget; built items match its choice, or the deviation is argued in writing |
| Blind estimates | `estimated_by` column and commit history | The estimator differs from the owner; numbers predate choices |
| Kill criteria in advance | Commit dates | Each brief predates the first build commit for its item |
| Raw notes | Attached to each result report | Reads the notes and checks the verdict follows from them |
| Tester consent | Consent line in each result report | Testers were told what was recorded and could stop at any time |
| Time log | `timelog.csv` | Compares actual hours with `c` and reads the gap note |

## How it is marked

The instructor reruns the checker, runs or reads the prototype and meets the team for 15 minutes. One member who did not build the prototype explains its result.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes and choice follows it | 10 | `PASS` on rerun; built items match the choice or the deviation is justified | Fails, or the team built what it liked and explained nothing |
| Risk coverage | 10 | Every load-bearing claim and pillar test line is in `risks.csv`; costs include running the test | Claims missing, or costs cover the build only |
| Blind estimates | 10 | Estimator is never the owner; numbers committed before choices | Owners rated their own risks |
| Briefs | 20 | One question each, an observable, a kill criterion, fidelity justified, "will not build" list, all committed before the build | Brief written after the build, or several questions per prototype |
| Result reports | 25 | Verdict stated against the criterion; raw notes attached; surprises recorded; "unclear" when it is | Verdict not tied to the criterion, or "promising" |
| Build or materials | 10 | The instructor can run or use it from the README; fakes are listed | Does not run, or no README |
| Update and time log | 10 | Claims and risks changed; actual hours by discipline against `c`, gap noted | Sheets unchanged, or no time log |
| Team ownership | 5 | A non-builder explains the result | Only the builder can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. A brief committed after its build started scores 0 on the briefs row for that item. Prototype 2 and the greenlight depend on this milestone, so it must be handed in even if it scores 0.
