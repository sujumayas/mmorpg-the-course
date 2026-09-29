# MMO406 · Exercises brief

**Weight:** 40% of the course grade, marked out of 100.
**Work mode:** individual, except lab 09, which is done in pairs. Labs 07 and 08 end with a pair review, but the code and report are your own.
**Assigned:** week 1. **Last lab due:** start of week 15. **Revision piece due:** end of week 13.
**Lectures:** every week from 1 to 14. Each exercise is the lab of its week.

## What this component is for

The course has two outcomes. You create a setting bible that scales across expansions, and you tie lore to systems: factions, economy, geography. The exercises train the second outcome one model at a time. Each lab turns a lecture model into a small tool, checks it against the lecture's numbers, and then runs it on your own world.

The exercises are also the parts list for the [world bible](world-bible-brief.md). Every lab produces a chapter or appendix of it. The ledger from lab 01, the region checker from lab 02, the faction analyser from lab 03 and the continuity checker from lab 11 all run on your final bible. Keep them working, and keep your world the same world from week 1 to week 14.

## The fourteen exercises

| Lab | Week | Exercise | The model you apply | The bible chapter it builds |
|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | The tension ledger | Stock `P`, consumption `c`, refill `R = g × S`, expansions `N` | Tensions and expansion supply |
| [02](../labs/lab02.md) | 2 | A map that needs its neighbours | Local share `C(r, k) / C(M, k)`, coverage, the ten percent check | Regions, resources and ecology |
| [03](../labs/lab03.md) | 3 | The faction web | Balanced triads, tension index `T`, flips | Factions |
| [04](../labs/lab04.md) | 4 | The lore clock and timeline checker | `w(t)`, span, density, time gap | History and calendars |
| [05](../labs/lab05.md) | 5 | Naming languages players can tell apart | Weighted overlap `o`, `P_amb(L)`, markers | Cultures and naming |
| [06](../labs/lab06.md) | 6 | A pantheon, a ledger and four accounts | Settled, answerable and unrecoverable facts | Religions and myths |
| [07](../labs/lab07.md) | 7 | Lore memory | Knowledge share `K(m)`, catch-up reach `r` | Lore delivery and assumed knowledge |
| [08](../labs/lab08.md) | 8 | Canon fit | Fit `F`, contradictions `E`, honor budget | Canon policy |
| [09](../labs/lab09.md) | 9 | The realm clock | Finish day, fatigue ceiling, narrative window | Living events |
| [10](../labs/lab10.md) | 10 | The foreshadowing plan | `E(d)`, `d*`, plan-change rate `ρ` | Expansion briefs and hooks |
| [11](../labs/lab11.md) | 11 | The continuity checker | Blast radius, cost `W`, frozen nodes, tiers | Canon graph and tiers |
| [12](../labs/lab12.md) | 12 | The transmedia plan | Context share `C`, extra share `X`, retell lines | Beyond the game |
| [13](../labs/lab13.md) | 13 | Roleplay hubs and the community chapter | Live hubs `V`, scene share `S`, `λ*` | Community |
| [14](../labs/lab14.md) | 14 | The question test | Answer rate `a`, `a_min`, wait `W`, margin | Front, reserved list and change log |

## What every exercise contains

Each lab file sets the tasks, the deliverable and the length limit. Every submission also meets these standards.

- **Tests pass.** Code you write passes the lab's tests. Paste the test output into the report. Lab 12 has no code; its calculator output takes the place of the tests.
- **Numbers show their inputs.** Every number in a report names the model it came from and its inputs, so a marker can recompute it. "`N = 9` (`P(0) = 21`, `c = 4`, `R = 2`)" is right. "About nine expansions" is not.
- **Same world, growing.** Every lab after lab 01 works on the world you started in lab 01. If you change something an earlier lab fixed (a faction's name, a date, a resource), say so in one line and update the earlier chapter's data file.
- **Numbers first.** Open each report with its results table, then explain. Pages past the lab's word limit are not read.

### Originality rule

Every setting, faction, place, character, god, language and line of lore in your exercises is your own invention. You may not base your world on the setting of any existing game, book, film, television series, tabletop game or fan work, and you may not use *Thornmere*, the course's sample world, as your own. Do not copy lore text from a shipped game or a wiki, not even as a placeholder. When a report discusses a shipped game, describe it in your own words and cite the course lecture that covers it. Borrowing structure from real cultures and religions follows the rules in [week 5](../lectures/w05-cultures-languages-names.md) and [week 6](../lectures/w06-religion-and-myth-in-fiction.md): borrow on purpose, from more than one source, and never make a living faith's sacred figures into villains or jokes.

## How exercises are marked

Each lab is marked out of 100 with the rubric in its own file. Two formats are in use.

- **Band rubrics** (labs 01 to 06 and 10 to 14) score each criterion Excellent 4, Adequate 2 or 3, Weak 0 or 1. A criterion is worth `weight × band / 4`. A criterion weighted 25% that earns Adequate at 3 is worth 18.75 points.
- **Point rubrics** (labs 07 to 09) give full, half or zero marks per criterion, and the points add to 100.

Your twelve best lab scores count. Each is worth 7 points of this component (`lab score / 100 × 7`), for 84 points. The two lowest are dropped. A lab you did not submit scores 0 and can be one of the two you drop. The drop exists to cover illness and a bad week, so it is not extended for either.

Dropping a lab's score does not drop its chapter. Every lab builds a chapter the world bible requires, so you still have to do the work before week 15. The bible brief marks the chapter, not the lab.

The other 16 points come from the revision piece.

## The revision piece

Pick one of labs 01 to 12 that came back with feedback. Revise it, and show with numbers what changed. This is the one place in the component where you are marked on responding to a reader, which is most of a lore lead's working life.

Submit the following.

1. **The revised artifact.** The data file and the chapter text, in the lab's format.
2. **A change note of at most 400 words.** For each piece of feedback you acted on, say what you changed and why. For feedback you chose not to act on, say why.
3. **Before and after numbers** from the lab's own model, in one table, with the tool's output pasted underneath.
4. **The ripple.** Name every other chapter the change touched, and show that its checker still passes. A new faction edge may change the ledger. A moved date may move a character's age in an expansion brief.

### A sample change note

This sample is invented to show the format and length. Your note will be about your own world.

> **Exercise:** lab 03, the faction web. World: the salt marshes of Vey, five factions.
>
> **Feedback 1:** "`T = 0.7` leaves writers no direction; every triad is under pressure." I made the Reed Clans and the Lamplighters allies, which the history chapter already supported (they share the flood shrines). `T` fell from 7/10 to 3/10, inside my target of 20% to 40%.
>
> **Feedback 2:** "The first flip is not backed by a system." I kept the flip (the Saltwardens break with the Crown) and tied it to the salt-tax reputation pair from lab 02's region sheet. The ledger gains one structural tension with `g = 0.5`.
>
> | | Before | After |
> |---|---|---|
> | `T` | 70% | 30% |
> | Unbalanced triads | 7 of 10 | 3 of 10 |
> | `T` after first flip | 60% | 20% |
> | Ledger `N` at `c = 3` | 8 | 11 |
>
> **Ripple:** ledger (lab 01) rerun, `N` rose from 8 to 11. History checker (lab 04) clean.

## Milestones and deadlines

| When | What is due | Feedback back by |
|---|---|---|
| Start of week 2 | Lab 01 | End of week 2 |
| Start of week 3 | Lab 02 | End of week 3 |
| Start of week 4 | Lab 03 | End of week 4 |
| Start of week 5 | Lab 04 | End of week 5 |
| Start of week 6 | Lab 05 | End of week 6 |
| Start of week 7 | Lab 06 | End of week 7 |
| Start of week 8 | Lab 07 | End of week 8 |
| Start of week 9 | Lab 08 | End of week 9 |
| Start of week 10 | Lab 09 (pairs) | End of week 10 |
| Start of week 11 | Lab 10 | End of week 11 |
| Start of week 12 | Lab 11 | End of week 12 |
| Start of week 13 | Lab 12 | Middle of week 13 |
| End of week 13 | Revision piece | Week 15, with the final grade |
| Start of week 14 | Lab 13 | End of week 14 |
| Start of week 15 | Lab 14 | Week 15, with the final grade |

Short ungraded quizzes from the [exam bank](exam-bank.md) open most lab sessions. They do not count toward this component. They tell you whether you can use the week's model with the lecture closed, which is what the lab assumes.

## Rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Lab exercises, best twelve of fourteen | 84 | Computed: the sum of your twelve best lab scores, each multiplied by 7/100. Each lab is marked with the rubric in its own file. | — | — | — |
| Revision: use of feedback | 4 | 4: every piece of feedback answered, with a reason for each one declined | 3: all answered, one reason thin | 2: some feedback ignored without comment | 0-1: no change note, or changes unrelated to the feedback |
| Revision: measured change | 5 | 5: before and after numbers from the lab's model, tool output pasted, every change traced to a number that moved | 4: numbers complete, one change not traced | 2-3: numbers for one version only, or a calculation error | 0-1: no numbers |
| Revision: ripple | 4 | 4: every touched chapter named and its checker rerun clean | 3: chapters named, one checker not rerun | 2: ripple claimed without evidence | 0-1: no ripple check |
| Revision: writing and originality | 3 | 3: revised lore reads better, in the world's voice, fully original | 2: better, with one weak or generic passage | 1: little change to the writing | 0: worse, or content taken from existing work |

## Late work

Each lab loses 10 of its 100 points per 48 hours late, and nothing is accepted after its feedback has been returned to the class. You have two free 48-hour extensions for the semester. Tell your tutor before the deadline that you are using one. The revision piece and lab 14 cannot use an extension, because they are graded with the world bible.

## Academic integrity

Code is individual, except in lab 09, where the pair submits one solution with both names. You may start from the starter files and from code in the lectures, and you may discuss approaches. You may not share solutions. All lore must follow the originality rule above. Every fact about a shipped game must come from a course lecture and cite it. Invented or altered test output, playtest results or listening-test data score 0 for the exercise and are treated as misconduct.
