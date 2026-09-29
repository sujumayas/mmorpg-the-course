# PR101 · Jam game brief: a game in 48 hours, and the plan behind it

**Weight:** 30% of the course grade.
**Assigned:** week 1, when teams form. **Preparation labs:** weeks 2 to 7. **Jam:** week 8, 48 hours from 17:00 on the first day of jam week. **Submission:** aim for hour 46; the hard close is hour 48. **Play-marking:** week 9.
**Work mode:** your team of four from lab 01. The team receives one mark. Individual contribution counts through the [peer review](peer-review-brief.md) component.
**Lectures:** weeks 1 to 8, most directly [week 4, scope and cut lists](../lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [week 7, task tracking and definitions of done](../lectures/w07-task-tracking-and-definitions-of-done.md) and [week 8, the 48-hour jam](../lectures/w08-48-hour-game-jam.md).

## What this component is for

It assesses the course outcome "ship a jam game with a team", and it tests the others under a clock that doesn't move. You will use Git as a team (weeks 2 and 3), scope to a fixed timebox (weeks 4 and 6), and run short build-and-play cycles with a board that tells the truth (weeks 5 and 7).

Most jam teams that fail don't fail on skill. They fail because nothing was playable at hour 40, or the upload was missing a folder. So this component marks two things. One is the game a stranger plays. The other is the production work that made a finished game likely: the plan, the board, the log and the freeze. A small game that runs start to end from the zip beats an ambitious one that only runs in the editor, and the rubric says so in points.

## What you make

A complete game, made from scratch in 48 hours around a theme announced at hour 0. The jam rules are the ones in [week 8, section 1](../lectures/w08-48-hour-game-jam.md). The short version:

- Teams are fixed at the theme announcement.
- The game connects to the theme in a way a stranger can see in the first minute.
- Engines, frameworks and code libraries are allowed. Code and art made before the jam are not, other than libraries.
- Third-party assets are allowed only if their licence permits it, and every one is credited in the game and on the submission page.
- The build runs on a lab machine, or in a web browser, without the engine installed.
- No copyrighted characters, logos or music you don't have a licence for.

There is no required genre, size or engine. Godot 4 is the supported engine. Any other needs the instructor's agreement before week 6, because the markers must be able to run your build.

## Deliverables

### Before the jam: preparation labs

Each lab is submitted and marked on its own rubric in the week it is due. Their scores count here.

| Lab | What it gives the jam | Due |
|---|---|---|
| [Lab 02, branching drill and team repository](../labs/lab02.md) | The shared repository, protected `main`, pull-request habit and merge-interval rule | End of week 2 |
| [Lab 03, asset pipeline and LFS](../labs/lab03.md) | LFS tracking and lockable patterns before any art is committed | End of week 3 |
| [Lab 04, the jam scope sheet](../labs/lab04.md) | MVP sentence, ordered task list, cut line, cut list and four cut triggers | End of week 4 |
| [Lab 06, your estimate log](../labs/lab06.md) | A buffer set from data, and task ranges | End of week 6 |
| [Lab 07, a board that tells the truth](../labs/lab07.md) | Card list, definition of done, WIP limit and the seeded jam log | End of week 7 |

Labs 01 and 05 also feed the jam (your charter's capacity, and the build-and-play cycle length you measured). They are scored under the [peer review](peer-review-brief.md) component, so they are not counted twice.

### At the jam: the submission

Everything in [lab 08](../labs/lab08.md), submitted through the course page by hour 48:

1. The zipped build, `<team>-v0.1.0.zip`, which runs on a lab machine or in a browser without the engine, with a credits screen.
2. The repository link with the tags `jam-start`, any `jam-good-*`, `v0.1.0-rc.*` and `v0.1.0`.
3. `jam_log.csv`, passing lab 08's `check_log.py`.
4. Board images at hours 12, 24, 36 and 42.
5. The one-pager written in the first two hours, with the MVP sentence at the top.
6. The freeze record: when you froze, each cut-trigger decision, every post-freeze change, and whether you would move the freeze next time, argued with the week 8 model.
7. A `PLAY.md` of at most 150 words: controls, how to win and lose, and anything the marker must know to start the build. Nothing in it may explain the game's design. If a stranger needs the design explained, that is feedback for your post-mortem.

## Timeline

| When | What happens | Marked where |
|---|---|---|
| Week 1 | Teams of four formed, charter signed | Peer review (lab 01) |
| Weeks 2 to 7 | Preparation labs | Part A below |
| Week 8 lecture slot, before hour 0 | Your `q` values, freeze hour and tested tag commands, from the week 8 in-class activity | Used in your freeze record |
| Week 8, hours 0 to 48 | The jam | Parts B and C |
| Week 9 lab | Play-marking and the peer play session | Part C |

## How the game is marked

Two markers play each game in week 9. Each downloads the zip onto a clean lab machine (or opens the web build), reads `PLAY.md` and plays for 10 minutes without help from the team. Each marker scores Part C alone. The two scores are averaged, and if they differ by more than 10 of Part C's 50 points a third marker plays and the median counts.

The markers compare the game with your one-pager's MVP sentence. They mark whether the promised loop works, not whether the game is large.

### The peer play session (not graded)

In the week 9 lab, every team plays three other teams' games for 10 minutes each and fills a short form: did you understand what to do within a minute, did you reach a win or a loss, what did you remember, and one bug with steps to reproduce. The forms go to the team that made the game. They are input to your [jam post-mortem](post-mortem-brief.md) and the first bug reports for the [week 10](../lectures/w10-bug-tracking-and-qa-basics.md) in-class activity. They carry no marks, so be honest.

## Rubric

The jam game mark is the total below, out of 100, multiplied by 0.30.

### Part A: preparation labs (30 points)

Each lab's own rubric gives a percentage. Multiply it by 6.

| Lab | What its rubric rewards most | Points |
|---|---|---|
| Lab 02 | Checker passes; four reviewed pull requests; merge interval set from the model | 6 |
| Lab 03 | Model tests pass; repository repaired; `.gitattributes` committed before any binary | 6 |
| Lab 04 | Cut line placed without skipping; `m_max` for both build orders; checkable triggers | 6 |
| Lab 06 | Tests pass; own plan ratio and buffer; plan redrawn with ranges | 6 |
| Lab 07 | Cards split and checkable; DoD traced to a real incident; WIP limit justified | 6 |
| **Subtotal** | | **30** |

### Part B: jam production evidence (20 points)

[Lab 08](../labs/lab08.md)'s rubric gives a percentage for the build, the jam log, the checkpoint evidence and the freeze record. Multiply it by 20. The log is marked on completeness, never on estimate accuracy.

### Part C: the game as played (50 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Runs from the submission | 9 to 10: the zip runs first time on a clean machine or browser; the version in the file name matches the `v0.1.0` tag | 6 to 8: runs after one small fix the team noted in `PLAY.md` | 3 to 5: runs only with the team's help, or from a different build than the tag | 0 to 2: not submitted or does not run | 10 |
| Complete loop | 11 to 12: a stranger can start, understand the goal, reach a win or a loss, and restart without leaving the game; the loop matches the MVP sentence | 8 to 10: complete, but restart or the return to the title is missing or awkward | 4 to 7: a win or a lose state is missing, or the loop needs `PLAY.md` to make sense | 0 to 3: no way to finish | 12 |
| Core mechanic | 9 to 10: the one idea the MVP sentence names works and is the center of play; the player can read what happened after every action | 6 to 8: works, but feedback is thin, so some deaths or successes are unclear | 3 to 5: present but buried, or replaced by a generic mechanic | 0 to 2: not playable | 10 |
| Theme | 5: a stranger sees the connection in the first minute | 3 to 4: visible only after a few minutes or after reading the page | 1 to 2: named but not played | 0: none | 5 |
| Vertical slice | 7 to 8: at least one section is finished through every layer (art, sound, UI, feedback) and looks and sounds like one game | 5 to 6: one layer is missing or clashes | 2 to 4: graybox with scattered finished pieces | 0 to 1: nothing past graybox | 8 |
| Credits and licences | 5: a credits screen names every team member and every third-party asset with its licence and source | 3 to 4: one asset or licence missing | 1 to 2: credits only on the web page | 0: none | 5 |
| **Subtotal** | | | | | **50** |

**Total: 30 + 20 + 50 = 100.**

A crash that ends a marker's session counts against "runs from the submission" once, not against every criterion. If the game crashes before a marker reaches the end state, the marker restarts once. The loop is marked on the best of the two runs.

## Rules

- **Hard close.** A build uploaded after hour 48 is not marked in Part C. Parts A and B still count. If illness or an emergency stops the team from submitting, the university's extension process applies, and the instructor sets a new close.
- **The tag is the submission.** Markers may rebuild from the `v0.1.0` tag. If the zip and the tag disagree, the tag's content is what the team claims to have made, and Part C's first row is marked down.
- **Integrity.** The jam rules above are the integrity rules. Code or art made before hour 0, other than libraries and engines, is not allowed, and neither is an asset whose licence you can't show. Both are academic misconduct under the university's policy.
- **Shared mark.** All four members receive the same mark. A member who stopped contributing is handled through the week 11 escalation ladder and the peer review component, not by changing this mark.

## Advice

- **Build the loop first.** Your lab 04 `m_max` is the best predictor of whether Part C's second row is safe. A vertical build order protects it.
- **Tag every build that works.** Week 8's model shows a tagged last-good build turns a late mistake from "lose the game" into "lose one feature".
- **Test the zip, not the project.** Part C's first row is worth 10 points, and the fix is to download your own submission on a machine that isn't the build owner's, at hour 44.
- **Log honestly.** Part B rewards a complete log. A task that took four times its estimate, honestly logged, earns full marks and gives week 9 something to analyse.
