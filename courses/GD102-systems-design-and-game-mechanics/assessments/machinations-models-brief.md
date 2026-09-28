# GD102 · Machinations models and exercises brief

**Weight:** 30% of the course grade.
**Covers:** the weekly modelling labs in weeks 1 to 6, 8 and 10 to 12, plus a model review in week 12.
**Related briefs:** [economy-design-brief.md](economy-design-brief.md) (labs 07 and 09 count there) and [final-sdd-brief.md](final-sdd-brief.md) (labs 13 and 14 count there).

## What this component is for

The course outcome behind this component is "diagram systems in Machinations" and, with it, "identify positive and negative feedback and predict dynamics". A diagram you cannot run is a guess. So every lab in this component asks the same three things. Did you build the model so that each number traces to one input? Does it reproduce the check values the lecture printed? And did you predict what it would do before you ran it, then explain the difference?

The labs build the habits one week at a time. The model review at the end checks that you can do it without a worksheet in front of you.

## Part A: weekly labs (80% of this component)

| Lab | Topic | Assigned | Due | Can be dropped? |
|---|---|---|---|---|
| [01](../labs/lab01.md) | Interaction audit | Week 1 | Start of week 2 | Yes |
| [02](../labs/lab02.md) | Stock-and-flow spreadsheet | Week 2 | Start of week 3 | Yes |
| [03](../labs/lab03.md) | Snowball simulator | Week 3 | Start of week 4 | Yes |
| [04](../labs/lab04.md) | Rubber-band tuning | Week 4 | Start of week 5 | Yes |
| [05](../labs/lab05.md) | Three spending machines | Week 5 | Start of week 6 | **No** |
| [06](../labs/lab06.md) | Pricing a converter | Week 6 | Start of week 7 | **No** |
| [08](../labs/lab08.md) | Loop anatomy and the bend | Week 8 | Start of week 9 | Yes |
| [10](../labs/lab10.md) | Emergence audit | Week 10 | Start of week 11 | Yes |
| [11](../labs/lab11.md) | Payoff matrix lab | Week 11 | Start of week 12 | Yes |
| [12](../labs/lab12.md) | Cave generator | Week 12 | Start of week 13 | Yes |

"Start of week N" means before the first class session of that week.

Labs 05 and 06 are the two labs built entirely in Machinations. They always count, because the model review and the economy design both assume you can build those diagrams.

### How Part A is computed

1. Each lab is marked out of 100 with the rubric printed in that lab.
2. Labs 04, 05, 06 and 08 print points that already sum to 100. Labs 01 to 03 and 10 to 12 print four bands with percentage weights. Convert each criterion as `weight × band points / 4`, where the top band is 4. Labs 01 to 03 have a Good band worth 3. Labs 10 to 12 have an Adequate band, which the marker scores as 2 or 3 and records which. For example, an Adequate (3) on a 20% criterion is `20 × 3/4 = 15`.
3. Your two lowest lab scores are dropped, except labs 05 and 06.
4. The eight remaining labs are averaged with equal weight. The average is worth 80% of this component, 24% of the course. Each counted lab is worth 3% of the course.

A missing lab scores 0 and is a candidate for dropping like any other score.

### What to submit each week

- The spreadsheet, script or Machinations file, or a view link that stays live until grades are released. Links that need a login to open are not marked.
- A screenshot of any Machinations diagram the lab asks for, with the pool chart after a run if the lab asks you to run it.
- The memo the lab asks for, as a PDF or on a tab named `Memo`. Word counts are targets. Anything within 20% either way is fine.

### Rules that apply to every lab

These are the habits the lectures teach. Markers apply them in every lab, whatever that lab's rubric calls the criterion.

- **Inputs are separate.** Every constant lives in one labelled cell or one named parameter, with its unit. No number other than 0 and 1 is typed into a formula.
- **Check values first.** Each lab prints check values. Reproduce them before you run any experiment. If yours differ, say so in the memo and say which you trust and why. An honest mismatch loses fewer points than a silent one.
- **Conservation holds.** Any model with pools carries the week 5 check, `start + arrived = end + left + lost`, as a column or a readout. If it fails, the model has a bug.
- **Signs are named.** Every feedback loop you draw is labelled reinforcing or balancing, with the count of minus links that decided it.
- **Predict, then run.** Where a lab asks for a prediction, write it before the result. Markers look for the prediction in the file history or above the result on the page.

## Part B: model review (20% of this component)

### What it is

In the week 12 lab session you bring one model you built this semester, improved, and defend it for 10 minutes with a marker. The marker changes one number in front of you and asks what will happen before running it.

### What to bring

1. **One running model.** Choose one of: the capped pool, turn-reset pool or carry-over pool from lab 05; the Catan converter diagram from lab 06; or the farm core and meta loop from lab 08, drawn in Machinations. It must run in machinations.io or, if the tool is down, in a spreadsheet with one row per step. Fix anything the lab feedback flagged.
2. **A one-page model card**, with these headings in this order.
   - *Question.* The one design question the model answers, in one sentence.
   - *Boundary.* What is inside and what is treated as fixed input (week 1, section 4).
   - *Elements.* Every pool, source, drain, converter, trader and gate, with its activation mode and pull or push rule.
   - *Loops.* Every closed path through a state connection, with its sign and the count of minus links.
   - *Prediction and result.* One numbered prediction you made before running it, the result, and one sentence on the gap.
   - *Conservation.* One line showing the check for one pool over the whole run.
   - *Known limits.* What the model leaves out and which way that biases the answer.

### How the review runs

| Minutes | What happens |
|---|---|
| 0 to 3 | You run the model and read the card's question and result aloud. |
| 3 to 6 | The marker changes one input (a rate, a cap, a ratio, an activator threshold). You predict the direction and rough size of the change in one named output, then run it. |
| 6 to 9 | One question from the [exam bank](exam-bank.md) for the week your model comes from, rewritten with your model's numbers. |
| 9 to 10 | The marker asks what you would change next and why. |

### Model review rubric (20 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Model runs and matches its lab | 5 | 5: runs from a clean start, reproduces the lab's check values, lab feedback fixed | 4: runs, one check value off with the cause named | 3: runs, check values not shown | 0-2: does not run, or not the lab's model |
| Model card | 5 | 5: all seven headings, loop signs counted, conservation line holds, limits say which way they bias the result | 4: one heading thin | 3: two or more headings thin, or no bias direction | 0-2: card missing or restates the lab |
| Change prediction | 5 | 5: direction and rough size right, reason given from the model's structure | 4: direction right, size off, reason sound | 3: direction right, reason given after the run | 0-2: wrong direction or no reason |
| Exam-bank question | 5 | 5: correct answer with the model named | 4: right method, arithmetic slip | 3: partial method | 0-2: no method |

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Weekly, start of weeks 2 to 13 | Lab submitted (see the Part A table) | Yes, Part A |
| Week 7 | Feedback on labs 05 and 06 returned. Tell the marker by the end of week 8 which model you will bring to the review. | No |
| Week 11 lab session | Five-minute check that your chosen model runs. The marker signs it off or names what is broken. | No, but required before the review |
| Week 12 lab session | Model review | Yes, Part B |

## Late work and extensions

- A lab submitted up to 48 hours late loses 10 points out of 100. After that it scores 0 and becomes a candidate for dropping.
- You have two free 48-hour extensions over the semester, for any of labs 01 to 12, including labs 07 and 09 from the [economy design brief](economy-design-brief.md). Tell the course team before the deadline. You cannot use them on labs 05 and 06, because the week after each builds on it, or on labs 13 and 14, which are SDD milestones.
- The model review can be moved only for documented illness or emergency. A missed review without one scores 0.

## Academic integrity

Discuss methods with classmates, and you should. The cells, diagrams and words you submit are yours. Machinations community templates are fine as a starting point if you name the template on the model card and say what you changed.
