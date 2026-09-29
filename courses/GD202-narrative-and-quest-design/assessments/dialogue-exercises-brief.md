# GD202 · Dialogue exercises brief

**Weight:** 40% of the course grade, marked out of 100.
**Work mode:** individual. You may discuss methods with classmates, but your code, numbers and writing are your own.
**Assigned:** week 1. **Last exercise due:** start of week 13. **Revision piece due:** end of week 13.
**Lectures:** every week from 1 to 12. Each exercise is the lab of its week.

## What this component is for

The course's first outcome is to write branching dialogue with manageable scope. That takes two skills at once. You have to write lines a player wants to read, and you have to know what those lines cost before you write them. Each exercise pairs one of the lecture models with a short piece of original writing, so that by week 12 you measure a scene as a habit, the way you would spell-check it.

The exercises are also the parts list for the [quest chain](quest-chain-brief.md). The branch analyzer from lab 03, the rule checker from lab 04, the variation engine from lab 12 and the linter from lab 11 all run on your final chain. Keep them working.

## The ten exercises

| Lab | Week | Exercise | The model you apply | The writing you produce |
|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Plot order audit | Inversions `I` and scramble `S` | An original backstory in two plot orders |
| [02](../labs/lab02.md) | 2 | The remembered choice | `W`, `V/W`, `R` and cost per acknowledgement | A 6 to 8 scene sequence honoring one binary choice |
| [03](../labs/lab03.md) | 3 | Branch explosion analyzer | Nodes, endings, paths, share seen | A branching quest plan under a 5,000-word budget |
| [04](../labs/lab04.md) | 4 | Rule-based dialogue checker | Rule matching, ties, silent states, dead rules | An 8 to 12 rule set for a returning-location NPC |
| [05](../labs/lab05.md) | 5 | Approval tuning | Approval walk, clamped meter, personas | A companion values sheet and event table |
| [07](../labs/lab07.md) | 7 | The drop-rate tax | Negative binomial mean, P90, P99 | A quest redesigned by numbers and by verb |
| [09](../labs/lab09.md) | 9 | Stranger to rival | Rematch chance and memory weight | Four rival memory lines |
| [10](../labs/lab10.md) | 10 | Lore budget | Reading decay, split plans, break-even find chance | A lore delivery plan and its pieces |
| [11](../labs/lab11.md) | 11 | Localization linter | CLDR plural categories, width budgets | A fixed string file with context notes |
| [12](../labs/lab12.md) | 12 | Variation engine | Repeat chances under dice, bag and cycle | A gate-guard scene in ink or Yarn Spinner |

Labs 06, 08, 13 and 14 are milestones of the quest chain and are marked there.

## What every exercise contains

The lab file sets the tasks, the deliverable and the length limit. Every submission also meets these standards.

- **Tests pass.** Any code you write passes the lab's tests. Paste the test output into the report.
- **Numbers show their inputs.** Every number in the report names the model it came from and its inputs, so a marker can recompute it. "`W = 11,240` (acknowledge + payoff, `N = 10`, `w = 1,000`, `k = 6`, `a = 40`)" is right. "About 11k words" is not.
- **Original story content.** Every character, place and line is yours. Do not use characters or settings from existing games, books or films. Never paste script text from a shipped game, not even as an example. When you discuss a shipped game, describe it in your own words and cite the course lecture that covers it.
- **Numbers first.** Open each report with the results table, then explain. Pages past the lab's word limit are not read.

## How exercises are marked

Each lab is marked out of 100 with its own rubric. Lab rubrics score each criterion in bands: Excellent is 4, Adequate is 2 or 3, Weak is 0 or 1. A criterion is worth `weight × band / 4`, so a criterion weighted 20% that earns Adequate at 3 is worth 15 points.

Your eight best lab scores count. Each is worth 10 points of this component (`lab score / 10`), for 80 points. The two lowest are dropped. A lab you did not submit scores 0 and can be one of the two you drop. The drop exists to cover illness and a bad week, so it is not extended for either.

The other 20 points come from the revision piece.

## The revision piece

Pick one exercise that came back with feedback. Revise it, and show with numbers what changed. This is the one place in the component where you are marked on responding to a reader, which is most of a writer's working life.

Submit the following.

1. **The revised artifact.** The scene, rule set, plan or script, in the lab's format.
2. **A change note of at most 400 words.** For each piece of feedback you acted on, say what you changed and why. For feedback you chose not to act on, say why.
3. **Before and after numbers** from the lab's own model, in one table.
4. **One reader check after the revision.** A two-reader playtest, a cold read by a classmate, or a lab 04 audit, whichever fits the exercise. Report what the reader noticed without prompting.

### A sample change note

This sample is invented to show the format and length. Your own note will be about your own work.

> **Exercise:** lab 02, the remembered choice. Scene: a salt merchant, Bettany Crane, asks the player to hide a crate from the harbour watch in Brinmoor.
>
> **Feedback 1:** "Neither reader mentioned the choice until the payoff scene." Both of my early callbacks were in optional dialogue with the dock boy. I moved one onto the critical path. The harbour captain now asks about the missing crate in scene 4, a line every player hears.
>
> **Feedback 2:** "The heavy acknowledgement comes too late." I kept it in scene 8. It is the scene where Bettany leaves town or stays, and moving it would break the ending. I added a medium acknowledgement in scene 6 instead.
>
> | | Before | After |
> |---|---|---|
> | `W` | 3,410 | 3,520 |
> | `V/W` | 94.1% | 91.2% |
> | `R` (heavy) | 4 (1) | 5 (1) |
> | On the critical path | 1 | 2 |
>
> **Reader check:** two new readers, one per option. Both named the harbour captain's question when asked where the choice mattered. One named the scene 6 line.

## Milestones and deadlines

| When | What is due | Feedback back by |
|---|---|---|
| Start of week 2 | Lab 01 | End of week 2 |
| Start of week 3 | Lab 02 | End of week 3 |
| Start of week 4 | Lab 03 | End of week 4 |
| Start of week 5 | Lab 04 | End of week 5 |
| Start of week 6 | Lab 05 | End of week 6 |
| Start of week 8 | Lab 07 | End of week 8 |
| Start of week 10 | Lab 09 | End of week 10 |
| Start of week 11 | Lab 10 | End of week 11 |
| Start of week 12 | Lab 11 | End of week 12 |
| Start of week 13 | Lab 12 | Middle of week 13 |
| End of week 13 | Revision piece | Week 15, with the final grade |

Short ungraded quizzes from the [exam bank](exam-bank.md) open most lab sessions. They do not count toward this component. They tell you whether you can use the week's model with the lecture closed, which is what the lab assumes.

## Rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Lab exercises, best eight of ten | 80 | Computed: the sum of your eight best lab scores, each divided by 10. Each lab is marked with the rubric in its own file. | — | — | — |
| Revision: use of feedback | 6 | 6: every piece of feedback answered, with a reason for each one declined | 5: all answered, one reason thin | 3-4: some feedback ignored without comment | 0-2: no change note, or changes unrelated to the feedback |
| Revision: measured change | 6 | 6: before and after numbers from the lab's model, every change traced to a number that moved | 5: numbers complete, one change not traced | 3-4: numbers for one version only, or a calculation error | 0-2: no numbers |
| Revision: reader check | 4 | 4: a reader check suited to the exercise, run after the revision, with what the reader noticed unprompted | 3: reader check run, prompts leaked the answer | 2: a check reported without detail | 0-1: no reader check |
| Revision: writing | 4 | 4: the revised lines are clearly better, in one voice, and within the lab's limits | 3: better, with one weak or over-long line | 2: little change to the writing itself | 0-1: worse, or over the limit |

## Late work

Each lab loses 10 of its 100 points per 48 hours late, and nothing is accepted after its feedback has been returned to the class. You have two free 48-hour extensions for the semester. Tell your tutor before the deadline that you are using one. The revision piece cannot use an extension, because it is graded with the final quest chain.

## Academic integrity

Code is individual. You may start from the starter files and from code in the lectures, and you may discuss approaches. You may not share solutions. All story content must be your own invention, and no text from a shipped game may appear in any submission. Every fact about a shipped game must come from a course lecture and cite it. Invented or altered test results or playtest data score 0 for the exercise and are treated as misconduct.
