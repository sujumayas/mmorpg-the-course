# MMO407 · Case analyses brief

**Weight:** 50% of the course grade.
**Assigned:** week 4, with one case analysis most weeks from week 4 to week 12. **Final post-mortem analysis:** chosen by the end of week 12, due at the start of week 15 and presented at the week 15 panel.
**Work mode:** the case analyses in Labs 04, 05 and 06 are individual (the code parts are in pairs). Labs 11 and 12 are individual. The final post-mortem analysis is written by your launch plan group, with a contribution statement.
**Lectures:** [week 4, FFXIV 1.0 to A Realm Reborn](../lectures/w04-case-ffxiv-1-0-to-a-realm-reborn.md), [week 5, Star Wars Galaxies and the NGE](../lectures/w05-case-star-wars-galaxies-and-the-nge.md), [week 6, New World's duplication exploits](../lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md), [week 7, classic and legacy servers](../lectures/w07-classic-and-legacy-servers.md), [week 8, EVE's large-scale events](../lectures/w08-eve-large-scale-events.md), [week 10, recovery strategies](../lectures/w10-recovery-strategies.md), [week 11, shutdowns and emulation](../lectures/w11-shutdowns-and-emulation-communities.md), [week 12, writing a post-mortem](../lectures/w12-writing-a-post-mortem.md) and [week 14, presentations](../lectures/w14-presentations.md).

## What this component is for

This component assesses the course outcome "extract transferable lessons from post-mortems". Reading a failed launch is easy. Reading it so that a different team, on a different game, would change a number in its plan is hard. Every case analysis in this course follows the same discipline: fix the dates, rewrite the case in one model's terms, name the parameter that moved, judge the decision by what was known at the time, and end with a lesson a launch plan can use.

A case analysis that retells the story earns little. One that says "the structural share was high and the measured penalty was above the crossover, so the rebuild was right, and here is what the public record cannot tell us" earns a lot.

## The parts

| Part | Case | Length | Work mode | When due | Weight within this component | Share of the course grade |
|---|---|---|---|---|---|---|
| [Lab 04](../labs/lab04.md) | A relaunch (The Elder Scrolls Online or No Man's Sky) through the patch-or-rebuild model | 600 words plus code | pairs for code, individual analysis | start of week 5 | 12 | 6% |
| [Lab 05](../labs/lab05.md) | The NGE through the redesign break-even model | 600 words plus code | pairs for code, individual analysis | start of week 6 | 12 | 6% |
| [Lab 06](../labs/lab06.md) | New World's first two months against the response kit | 600 words plus code | pairs for code, individual analysis | start of week 7 | 12 | 6% |
| [Lab 11](../labs/lab11.md) | A preservation plan with the rebuild clock | 800 to 1,100 words plus code | individual | start of week 12 | 10 | 5% |
| [Lab 12](../labs/lab12.md) | A launch post-mortem with contrast ratios | 400 to 600 words plus a 1,200 to 1,800 word post-mortem | individual | start of week 13 | 14 | 7% |
| Final post-mortem analysis | A published launch, relaunch or shutdown of your choice | 2,000 to 3,000 words | launch plan group | start of week 15 | 40 | 20% |
| **Total** | | | | | **100** | **50%** |

Each lab is marked out of 100 with its own rubric, including its code rows, and enters the table at its weight. The final post-mortem analysis is marked with the rubric below.

## The final post-mortem analysis

### Choosing a case

Pick one published launch, relaunch or shutdown. It may come from weeks 4 to 11 or from the course reading list of Game Developer post-mortems. Two rules apply.

- **New ground.** Choose a case, or a model, that no member of your group used for a graded lab case analysis. Analysing New World again through week 6's discovery curve is not allowed. Analysing New World's launch queue through week 2's cumulative curves is.
- **Enough evidence.** You need at least four dated sources, at least two of them contemporary with the events (official posts, news reports, published post-mortems or talks). If the public record is too thin to fix a timeline, choose another case.

Tell the instructor your case and your model by the end of week 12. The instructor may refuse a case if two groups in the same panel session choose it.

### What to write

Follow the four parts from [week 14, section 4](../lectures/w14-presentations.md), with the evidence habits from [week 12](../lectures/w12-writing-a-post-mortem.md).

1. **What happened, with dates.** A timeline from sources, each row cited with a date or version. Keep what the sources report apart from what you conclude.
2. **The model that explains it.** Rewrite the case in one model from this program: week 1's narrowest stage, week 2's cumulative curves, week 3's beta exposure, week 4's crossover penalty, week 5's break-even, week 6's discovery curve, week 7's tipping realm, week 8's escalation loop, week 9's critical ratio, week 10's review mixture, week 11's rebuild clock, week 13's register, or a model from MMO301 or MMO308 for a shutdown. Show which parameter moved and by roughly how much. Where the record cannot give a number, say so, and bracket it with a range instead of inventing one.
3. **What the team could have seen, and when.** The evidence that existed before the failure, and the gate or trigger that would have acted on it. Judge each decision by what was known then. Include one place where hindsight could mislead a reader and how you guarded against it.
4. **The transferable lesson.** At least one lesson written as a row a different game's plan could hold: a gate, a weight, a risk with `p` and `I`, or a trigger. Grade it A, B or C with week 12's scale. If you have a contrast across launches, report the counts. The lesson you choose to present also appears in annex G of your [launch plan](launch-plan-brief.md).

Add a source list with a date or version for every source, and a short appendix with any calculation, runnable with the course Python.

### Gates

Two of the panel's gates from week 14 apply to the written analysis. An analysis that fails one is returned for resubmission within one week and capped at 50.

1. Every real-game fact has a source with a date or version, and no invented number is presented as fact.
2. The analysis uses a model and names a parameter that moved.

### Rubric: final post-mortem analysis (100 points)

A criterion earns full points for Excellent, half for Adequate and zero for Missing or wrong. Markers may award a point or two between bands where the work sits between them.

| Criterion | Excellent | Adequate | Missing or wrong | Points |
|---|---|---|---|---|
| Timeline and sources | Dated timeline from four or more sources, two contemporary; facts kept apart from interpretation; conflicting sources noted and weighed | Timeline correct but thinly sourced, or facts and interpretation mixed | Undated or unsourced | 20 |
| Model and parameter | The case rewritten in one model's terms; the parameter that moved named with a size or an honest range; the model's limits stated | Model named and applied loosely; parameter vague | Story with no model | 30 |
| What was knowable, and when | Pre-failure evidence identified with dates; the gate or trigger that would have acted named; blameless; a hindsight note | Evidence named without dates or triggers | Blame with hindsight | 20 |
| Transferable lesson | Written as a gate, weight, risk or trigger with numbers; graded A, B or C honestly; counts reported where a contrast is claimed | Lesson sound but not in a plan-ready form, or graded generously | "Test more", "communicate better" | 20 |
| Writing and reproducibility | Plain, within length; every calculation reproducible from the appendix | Minor gaps | Calculations cannot be checked | 10 |
| **Total** | | | | **100** |

The analysis is presented in the post-mortem part of the week 15 panel. The panel mark counts toward the launch plan component, and the [launch plan brief](launch-plan-brief.md) has its rubric. The written analysis is marked here, on its own.

## Evidence rules for every case analysis

These rules come from the case lectures. They apply to Labs 04, 05, 06, 11 and 12 and to the final analysis.

- **Separate what was said from what was measured.** Boxes sold are not subscribers. A reported Friday-night count that the studio denied is not a number (week 5, section 5).
- **Do not fit what the record cannot support.** New World's public record does not list every exploit found, so a fitted `a` would be invented precision (week 6). State the shape the record supports.
- **Give every source a date or version.** Formulas, prices and caps change across patches.
- **Invented values are allowed only if labelled.** A symbolic `S₀` or a bracketed range is honest. An invented subscriber count presented as fact fails the evidence row of the lab rubric.
- **No invented quotes.** Paraphrase and cite, with at most one short quoted phrase per source.

## Individual marks

Lab case analyses are individual even where the code was done in pairs. For the final analysis, the instructor may adjust an individual's mark by up to 10 points either way, using the contribution statement and that member's answers to the post-mortem questions at the panel.

## Late work and integrity

- **Late submission.** A lab case analysis up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and scores 0. The final analysis, up to 48 hours late, is marked out of 80. Extensions for illness or other documented reasons follow the university policy.
- **Integrity.** The analysis must be your own words. You may discuss cases with anyone, but you may not share drafts of an individual case analysis. Cite every source you used, including the lecture.
