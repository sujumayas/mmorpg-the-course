# MMO403 · Business plan brief

**Weight:** 40% of the course grade.
**Work mode:** individual. You may base the plan on your team's capstone concept (PR401), but the plan, the numbers and the pitch are your own.
**Due:** written plan, financial model and deck at the start of week 15; pitch and viva in the week 15 session.

## What the business plan is

Week 15 is the final. You present a business plan for an MMO or persistent online game of your own design, of the kind a publisher or investor would read before funding its first stage. Every section is a model from this course run on your game, with the ethics built into the design rather than added at the end.

A funder reading your plan should be able to answer four questions from section 1 of the [week 14 lecture](../lectures/w14-pitching-to-publishers-and-investors.md): what it costs and when, what it is worth if it works, how likely that is, and what happens after bad news.

## Deliverables

1. **The written plan,** at most 12 pages plus appendices, with these sections in this order.
   1. *Summary* (one page): the game, the business model, the ask for stage 1, the gate, and the three biggest risks.
   2. *Business model* ([week 1](../lectures/w01-business-models-box-subscription-f2p-hybrid.md)): door, upfront price and monthly meter as ranges, the contribution model over 36 months at three retention levels, and the retention at which your model beats the nearest alternative.
   3. *Unit economics* ([week 2](../lectures/w02-unit-economics-ltv-cac-arppu.md)): an LTV curve with horizon, fee basis and cohort stated, CAC by channel, and payback days.
   4. *Monetization design* ([weeks 3 to 6](../lectures/w03-premium-currencies.md), [week 10](../lectures/w10-pricing-experiments.md), [week 11](../lectures/w11-subscription-tokens.md)): what the store sells, in which currency, with the pack grid audited for forced leftovers; the store policy in rating points for any ranked mode; the pass finish line and rebate if you have a pass; the full cost disclosure if you sell random items; the first price test you would run, with its sample size; a token only if its net premium survives your channel fees.
   5. *Ethics and compliance* ([weeks 7 to 9](../lectures/w07-regulation-belgium-netherlands-china-others.md)): the eight-market rule table for your design as of a stated date, a dark-pattern review of your two riskiest features, the expected concentration of revenue (payer rate, `G_pay`, top 1% and top 10% of payers) and the spending protection you will ship with its modelled cost.
   6. *Channels and publishing* ([week 12](../lectures/w12-publishing-platforms-and-fees.md)): the channels you launch on, each fee schedule dated, the average and marginal rate at forecast revenue, and the waterfall from consumer spend to studio receipts for your chosen deal.
   7. *Team, budget and runway* ([week 13](../lectures/w13-team-and-budget-planning.md)): the phase plan from lab 13 Part C, sourced loaded cost and fixed costs, contingency, three slip scenarios and the cut list.
   8. *Funding plan* ([week 14](../lectures/w14-pitching-to-publishers-and-investors.md)): the stage-1 ask, the gate (metric, threshold, date, decider), `EV_all` and `EV_gate` at three values of `p`, the break-even false-go rate, the funder or dilution table, and the stop plan.
2. **The financial model**: one script or notebook (Python run with `.venv/bin/python`) or one spreadsheet in which every result cell is a formula. It reproduces every number in the plan from the plan's stated inputs. Your lab code from labs 01, 02, 09, 12, 13 and 14 may be reused.
3. **The pitch deck**: at most 12 slides following section 4 of the week 14 lecture, including the ask for stage 1 only and a gate slide. Your own art or plain shapes only. No copyrighted game art, characters or logos.
4. **The pitch and viva** in week 15: a 5-minute pitch, then a 10-minute viva in which the panel asks questions in the style of the [exam bank](exam-bank.md), rewritten with your plan's numbers.

## Milestones

Milestones are checkpoints with written feedback. They are not graded on quality, but submitting each on time and acting on its feedback is worth 5 points in the rubric.

| Week | Milestone | What you hand in | Built in |
|---|---|---|---|
| 4 | M1: concept and model | One page: the game in one sentence, its audience, the business model with `d`, `U`, `m` and `r` as ranges, and the 36-month contribution at three retention levels | [Lab 01](../labs/lab01.md), [lab 02](../labs/lab02.md) |
| 9 | M2: monetization and ethics draft | Two pages: store contents and pack grid audit, any random items with their cost disclosure, the eight-market table, and a first dark-pattern review | [Lab 03](../labs/lab03.md), [lab 06](../labs/lab06.md), [lab 07](../labs/lab07.md), [lab 08](../labs/lab08.md) |
| 13 | M3: budget | Lab 13 Part C: phase plan, sourced costs, slip scenarios, cut list and raise memo | [Lab 13](../labs/lab13.md) |
| 14 | M4: funding plan and deck | Lab 14 Parts C and D: stage definitions, gate, EV table, funder or dilution table, stop plan, draft deck | [Lab 14](../labs/lab14.md) |
| 15 | Final | Written plan, financial model, deck; pitch and viva | All |

## Rubric (100 points)

| Criterion | Full marks | About half | Little or none | Points |
|---|---|---|---|---|
| Business model and unit economics | Contribution, LTV and payback computed from stated, sourced or labelled inputs; horizon, fee basis and cohort on every LTV; the model chosen holds across the low and high cases or the plan says where it fails | Correct numbers, single case only, or LTV unlabelled | Revenue asserted without a model | 15 |
| Monetization design | Store, currency, pass, random items and tests each designed with the week's model; pack grid audited; any ranked-mode sale limited in rating points; price test sized for revenue | Design described, one or two models missing | A list of features with no numbers | 15 |
| Ethics and compliance | Rule table correct as of a stated date; dark-pattern review applies the disclosure test honestly; concentration reported with `G_pay` and two top shares; a spending protection chosen with its modelled cost | Present but one element missing or undated | Missing, or the law misstated | 15 |
| Channels and waterfall | Fee schedules dated; average and marginal rates at forecast revenue; waterfall to studio receipts including recoupment | Channel fees right, waterfall incomplete | Headline rates only | 10 |
| Budget and runway | Sourced loaded cost and fixed costs; contingency tied to named risks; slip scenarios with decisions; no reliance on unplanned overtime | Budget complete, sources or scenarios thin | Salaries only, or no runway | 15 |
| Funding plan and gate | Stage-1 ask; one metric, threshold, date and decider fixed in advance; EV at three `p` values and `f*`; humane stop plan | Gate named, numbers or stop plan missing | Asks for the whole budget with no gate | 10 |
| Pitch and viva | Deck supports the four funder numbers; answers use the models on the spot with correct arithmetic | Clear pitch, viva answers partly from memory | Cannot explain own numbers | 10 |
| Honesty, sources and reproducibility | Low-end case shown; comps' survivorship bias acknowledged; the financial model reproduces every number; all real facts sourced and dated | A few numbers not reproducible or undated | Wishful numbers presented as forecasts | 5 |
| Milestones | All four submitted on time and the final plan shows the feedback was acted on | Some milestones late or feedback ignored | None submitted | 5 |
| **Total** | | | | **100** |

## How the viva works

The panel (two staff) reads your plan before the session. After your 5-minute pitch it asks three or four questions, at least two of them compute questions on your own numbers, for example:

- "Your retention forecast drops two points. What happens to your 36-month contribution, and does your model still beat a box price?" (week 1)
- "What share of revenue would a $100 monthly cap remove under your fitted `α`?" (week 9)
- "At your forecast revenue, what is Steam's marginal rate, and why did you budget with the average?" (week 12)
- "Your beta slips two months. When does the cash run out?" (week 13)
- "What false-go rate would make your gated plan worthless?" (week 14)

You may use your financial model during the viva. Answers that use the model correctly and state what the number means score full marks on that row even if you need a minute to run it.

## Rules

- **Your own game.** The plan must be for an original concept. You may compare with real games (comps), with sources and dates, and you must say that comps only include games that shipped.
- **Invented numbers are labelled.** Retention, conversion and spending figures for an unreleased game are assumptions. Give them as ranges and say where each range comes from (a comparable title's published figure, a lecture's teaching value, a playtest).
- **Ethics is part of the design.** A plan whose revenue depends on a pattern the course calls dark, or on selling paid random items where the plan's own rule table says they must be removed, loses marks in the ethics row even if the numbers work.
- **No copyrighted art** in the deck or the plan. Plain shapes and your own sketches are fine.
- **Late work.** The written plan loses 5 points per day late for up to five days. The pitch and viva cannot be moved except for documented illness or emergency.
