# MMO305 · Final social system design and research proposal brief

**Weight:** 50% of the course grade.
**Covers:** labs 05, 06 and 14, a social system design document, a research proposal to test it, and a presentation with viva in week 15.
**Related briefs:** [reading-responses-brief.md](reading-responses-brief.md) and [field-observation-brief.md](field-observation-brief.md). Viva questions follow the style of the [exam bank](exam-bank.md), rewritten with your own numbers.

## What this component is for

The course outcomes behind this component are "design grouping, guild and communication systems" and "diagnose and mitigate griefing and toxicity." Every week of the course gave you one model that turns a social design choice into a number: reach, density, acquaintances per month, a guild's tipping point, `ρ`, a reputation half-life, precision, `I*`, the punishment ceiling, `L*`, the connection clock, the voice ratio, length bias and `Δr`. The final project asks you to use several of them at once on a game of your own, to say where they pull against each other, and then to plan the study that would tell you whether you were right.

A design here is judged by whether each claim traces to a model and a number, whether the trade-offs are named, and whether the research proposal could actually catch you being wrong.

## Part A: design labs (30% of this component)

| Lab | Topic | Assigned | Due | Feeds |
|---|---|---|---|---|
| [05](../labs/lab05.md) | DKP simulator | Week 5 | Start of week 6 | Reward-allocation section (D2) |
| [06](../labs/lab06.md) | Reputation replay | Week 6 | Start of week 7 | Trust and harm section (D3) |
| [14](../labs/lab14.md) | Positive-sum audit | Week 14 | Start of week 15 | Reward-allocation section (D2) and the `Δr` column of the system map |

Each lab is worth 10% of this component (5% of the course). No lab is dropped. Labs 05 and 06 print points that sum to 100. Lab 14 uses full, half or zero marks on each weighted criterion.

Other labs feed this project without being graded here. Lab 03 (requeue and pool size) feeds D1, labs 08 and 09 feed D3, lab 04 feeds module D4, lab 10 feeds D6, lab 11 feeds D7 and the research proposal, and lab 12 feeds D8. Reuse your own lab work freely and cite it.

## Part B: social system design document (40% of this component)

### The game

Invent the game. You are designing its social systems, so keep the rest brief. State in a one-page frame: genre and setting in one line, population per server or shard, typical session length, content types and their group sizes (for example 5-player dungeons and a 20-player raid), business model (subscription, box price or free to play, since it changes your identity costs in week 6), and the audience you are designing for.

You may base the frame on a shipped game you know well, if you say so. Any fact about a real game must be cited with its version or era. Facts already cited in the course lectures may be reused with the lecture's source.

### Required sections

The document is 4,000 to 5,000 words, not counting tables, figures, appendices and sources.

**A. Frame.** One page, as above.

**B. Social goals.** Which ties the design should produce and for whom, in the week 1 terms of bonding and bridging. Give each goal a measurable target, such as "a newcomer attached by day 14 in 40% of cases" or "no broker on a typical server."

**C. System map.** A table with one row per social system in the game (grouping, guild, loot or credit, reputation, status items, channels, newcomer path, moderation and any other). Columns:

| System | Ties it creates (internal or external) | Layer (co-presence, co-location, co-activity) | Intended sign of `Δr` | Main harm route | Section |
|---|---|---|---|---|---|

**D. Subsystems in depth.** D1, D2 and D3 are required. Choose two of D4 to D8. Each subsystem section needs its lecture model with your parameter values, at least one table of numbers you computed, one precedent from the lectures rewritten in the model's terms, and the trade-off you chose deliberately.

| Section | Lecture | What it must decide, with numbers |
|---|---|---|
| D1 Grouping and matchmaking (required) | [Week 3](../lectures/w03-forced-vs-voluntary-grouping.md) | Pool size `N` and group size `m` per content tier; expected acquaintances per month; the re-meet tool and its target share (lab 03); the grouping rule `R_g(1 − w) > R_s` for your main content |
| D2 Reward allocation (required) | [Weeks 5](../lectures/w05-raiding-as-organization-dkp.md) and [14](../lectures/w14-designing-for-positive-social-play.md) | The loot or credit rule for group content with its `ρ` and a recruit's first-item wait (lab 05); the open-world credit rule with `Δr` for `n = 1` to 6, faucet multiplier and free-rider limit (lab 14) |
| D3 Trust and harm (required) | [Weeks 6](../lectures/w06-trust-and-reputation-systems.md), [8](../lectures/w08-griefing-typology-and-design-responses.md) and [9](../lectures/w09-toxicity-research-and-interventions.md) | Reputation parameters `λ`, `a`, `b` with half-life, newcomer score and whitewashing gain (lab 06); the griefing type each system invites and the response family you chose; a toxicity package with its punishment ceiling and expected wrong punishments per month |
| D4 Guilds | [Week 4](../lectures/w04-guilds-formation-lifecycle-leadership.md) | Formation rule, cap, exit costs, succession rule; critical mass `M` for your content and the steady states for a typical guild |
| D5 Status items | [Week 7](../lectures/w07-status-prestige-and-conspicuous-display.md) | Three display items with the signal each carries, precision estimates for the credential one, display venue, and how you damp the gatekeeping loop |
| D6 Channels | [Week 10](../lectures/w10-communication-design-chat-emotes-pings.md) | Every public channel with audience, vocabulary, persistence and rate limit; `L*` and coverage for the busiest; one restricted-vocabulary or ping channel |
| D7 Newcomers | [Week 11](../lectures/w11-newcomers-and-mentoring-systems.md) | The newcomer channel or mentor program with eligibility, capacity and exit rules; predicted `a`, `b`, `p` and day-7 and day-30 retention against a baseline |
| D8 Community feedback | [Week 12](../lectures/w12-community-management.md) | The feedback pipeline, which channels are self-selected and which representative, and how you will estimate and record `ρ` |

**E. Interactions.** At least two places where your subsystems act on each other, each with a number. For example, a loot rule's recruit wait lowers a guild's `R` (weeks 4 and 5), a reputation gate on chat changes a newcomer's `a` (weeks 6 and 11), or shared credit raises the faucet the economy team must sink (week 14). Name the interaction you worry about most and what you would watch for at launch.

**F. What you chose not to do.** One design you considered and rejected, with the model's reason.

**G. Sources.** Every reading, lecture and game fact you relied on.

**Appendix.** The spreadsheets or scripts behind every number, runnable from a clean start, with inputs in labelled cells or named constants.

## Part C: research proposal (20% of this component)

A design is a set of predictions. The proposal plans the study that would test the most important ones after launch, or in a closed test before it. It is 1,500 to 2,000 words.

1. **Question and hypotheses.** One research question and two or three hypotheses, each stated as a prediction about a model quantity. "The requeue button raises the share of runs with a repeat partner from 2% to at least 15%" is testable. "Players will feel more social" is not.
2. **Method.** At least two methods that check each other, such as a randomised A/B test on telemetry (MA102 week 14) plus a field observation or a survey. Say what each one can and cannot show. Week 13 section 4 describes how the qualitative and quantitative sides feed each other.
3. **Sampling and bias.** How you will reach players, and how you will handle length bias (week 13), the voice ratio (week 12) and self-selection into treatment (week 11, the Teahouse design). If you assign treatments, say how you randomise.
4. **Measures and horizon.** The metrics, drawn where possible from the week 14 dashboard list, with the time horizon for each and why (week 11 shows a day-7 metric can miss a connection effect). Include the counterweight measure, such as reports or blocks per stranger encounter.
5. **Sample size.** A calculation of how many players or sessions you need so the effect you predict is large compared with its standard error. Exam bank question 65 shows the method.
6. **Ethics.** Consent, data handling and what you will not collect, following the field observation rules and AoIR's guidelines. Treatments that could harm players (for example, withholding a safety tool from a control group) need a justification or a redesign.
7. **Decision rule.** What result would make you change the design, and what you would change.

## Part D: presentation and viva (10% of this component)

In week 15 you present for 8 minutes, then take a 12-minute viva with two examiners.

| Minutes | What happens |
|---|---|
| 0 to 8 | You present the frame, the system map, one subsystem in depth with its numbers, and the research proposal's main hypothesis. |
| 8 to 12 | An examiner changes one input in your design (a pool size, a price, `λ`, a threshold) and asks you to predict the direction and rough size of the change in a named output, then check it in your appendix model. |
| 12 to 17 | One exam-bank-style question from a week your design uses, rewritten with your numbers. |
| 17 to 20 | "What would you cut if you had half the team?" |

### Presentation and viva rubric (20 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Presentation | 5 | 5: on time, map and numbers clear, one trade-off made explicit | 4: clear, trade-off implied | 3: over time or numbers hard to follow | 0-2: no numbers or no structure |
| Change prediction | 5 | 5: direction and rough size right, reasoned from the model before running it | 4: direction right, size off, reason sound | 3: direction right, reasoned only after running | 0-2: wrong direction or no reason |
| Exam-bank question | 5 | 5: correct answer with the model named | 4: right method, arithmetic slip | 3: partial method | 0-2: no method |
| Scope judgment | 5 | 5: cuts argued from the social goals and the model | 4: sensible cuts, thin reasons | 3: cuts without reasons | 0-2: no answer |

## Rubrics for Parts B and C

### Design document rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Goals and system map | 15 | 14-15: measurable goals; every system in the map with ties, layer, `Δr` sign and harm route | 11-13: map complete, one goal not measurable | 8-10: map missing columns or systems | 0-7: no map, or goals are slogans |
| D1 Grouping | 15 | 14-15: `N`, `m`, acquaintances and re-meet target computed per tier; trade-off between queue speed and ties argued | 11-13: correct numbers, one tier thin | 8-10: model named, numbers partial | 0-7: no model |
| D2 Reward allocation | 15 | 14-15: `ρ`, recruit wait, `Δr` table, faucet multiplier and free-rider limit all correct and linked to the goals | 11-13: one number missing or off | 8-10: rule described, few numbers | 0-7: no rule or no model |
| D3 Trust and harm | 15 | 14-15: reputation parameters with half-life, newcomer score and whitewashing gain; harm routes typed; toxicity package with ceiling and wrong-punishment count | 11-13: one of the three parts thin | 8-10: two parts thin | 0-7: harm treated as "we will moderate" |
| Two chosen modules | 15 | 14-15: both modules apply the model with correct numbers, rewrite a precedent in model terms and choose a trade-off | 11-13: both correct, trade-offs implied | 8-10: one module strong and one weak, or both described with weak numbers | 0-7: a module missing |
| Interactions and rejected option | 15 | 14-15: two interactions quantified, the main risk named with a launch signal, a rejected design with the model's reason | 11-13: interactions named, one quantified | 8-10: interactions asserted without numbers | 0-7: missing |
| Evidence, appendix and writing | 10 | 9-10: every number reproducible from the appendix; real-game facts cited with era; plain, within length | 7-8: one number not traceable | 5-6: appendix incomplete | 0-4: numbers cannot be checked |

### Research proposal rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Question and hypotheses | 20 | 18-20: hypotheses are predictions about model quantities with values | 14-17: testable, values missing on one | 10-13: partly testable | 0-9: untestable |
| Method | 25 | 22-25: two methods that check each other, limits of each stated, randomisation where needed | 17-21: two methods, limits thin | 12-16: one method only | 0-11: no workable method |
| Sampling and bias | 20 | 18-20: length bias, voice ratio and self-selection each addressed where relevant | 14-17: two of three addressed | 10-13: bias mentioned, not handled | 0-9: ignored |
| Measures, horizon and sample size | 15 | 14-15: metrics with horizons justified, counterweight included, sample size computed correctly | 11-13: sample size rough or horizon unjustified | 8-10: metrics listed only | 0-7: missing |
| Ethics and decision rule | 20 | 18-20: consent and data handling specific; harmful treatments avoided or justified; a clear rule for what result changes the design | 14-17: one part thin | 10-13: generic ethics statement | 0-9: missing |

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Start of week 6 | Lab 05 | Yes, Part A |
| Start of week 7 | Lab 06 | Yes, Part A |
| End of week 8 | One-page pitch: frame, social goals, the two chosen modules, one sentence on the research question. Feedback within a week. | Required, ungraded |
| Week 12 lab session | Design review, 10 minutes with a tutor: the system map and one subsystem model running from a clean start | Required, ungraded |
| Start of week 15 | Lab 14 | Yes, Part A |
| Start of week 15 | Design document and research proposal | Yes, Parts B and C |
| Week 15 sessions | Presentation and viva | Yes, Part D |

## How the component grade is computed

`component = 0.1 × (lab 05 + lab 06 + lab 14) + 0.4 × design + 0.2 × proposal + 0.1 × (viva points × 5)`, with every score out of 100 and the viva out of 20. It is worth 50% of the course.

## Late work and extensions

- Labs 05 and 06 submitted up to 48 hours late lose 10 points out of 100, after which they score 0. The free extensions from the reading responses brief apply to them. They do not apply to lab 14, the design document or the proposal, because the viva schedule depends on them.
- The design document and proposal lose 5 points out of 100 per day late, up to three days, after which they score 0.
- The viva can be moved only for documented illness or emergency.

## Academic integrity

The design, numbers and words must be your own. You may discuss ideas and models with classmates and reuse your own lab work. If you adapt a classmate's or a public script, name it and say what you changed. Paraphrase every source and quote at most one short phrase from each.
