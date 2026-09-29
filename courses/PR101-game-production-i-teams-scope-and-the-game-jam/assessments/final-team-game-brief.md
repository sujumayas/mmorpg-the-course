# PR101 · Final team game brief: plan it, track it, release it

**Weight:** 40% of the course grade.
**Assigned:** week 9, after the jam post-mortem. **Milestone 1 (plan):** end of week 9. **Milestone 2 (first playable):** end of week 11. **Milestone 3 (release candidate dry run):** end of week 13, through lab 13. **Feature freeze:** release minus 5 days. **Release:** the first day of week 15. **Release demo:** week 15.
**Work mode:** your team of four. A team may re-form after the jam only with the instructor's agreement, requested by the end of week 9. The team receives one mark, except the release demo, where each member answers alone.
**Lectures:** all fourteen, most directly [week 4, scope](../lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [week 6, estimation](../lectures/w06-estimation-and-why-it-fails.md), [week 9, jam post-mortem](../lectures/w09-jam-post-mortem.md), [week 10, bug tracking](../lectures/w10-bug-tracking-and-qa-basics.md), [week 12, crunch](../lectures/w12-crunch-causes-costs-alternatives.md) and [week 13, builds and release checklists](../lectures/w13-builds-and-release-checklists.md).

## What this component is for

The jam asked whether your team could finish something in 48 hours. This component asks whether it can finish something over six weeks while other courses compete for the same hours, and do it without crunch. That is closer to how studios work, and it is where the semester's tools earn their place: a plan sized from your own jam data, a board and a bug tracker that tell the truth, a release checklist, and a version number that tells a grader exactly which build they played.

It assesses all four course outcomes. Git in a team workflow shows in your repository and tags. Scoping to a timebox shows in your plan and cut list. Sprints, standups and retrospectives show in your sprint records. Shipping with a team shows in the build the marker downloads.

## What you build

A small, finished game. You may extend your jam game or start a new concept, but you must decide at milestone 1 and say why.

- **Size.** Plan it from your capacity, not your ambition. Capacity comes from the hours each member actually logged in weeks 5 to 8, over the weeks left, reduced by the week 1 channel cost. Hold back a buffer set from your jam plan ratio (`b = 1 − 1/R`, week 6), not from a guess.
- **Engine.** Godot 4.x, one pinned version written in the README. Another engine needs the instructor's agreement at milestone 1.
- **Platform.** A Windows build that runs on a lab machine without the editor, or a web build that runs in two current browsers. Both is fine. Pick at milestone 1.
- **Content rules.** No copyrighted characters, logos or unlicensed assets. Every third-party asset is credited in the game with its licence.

### Process rules

These are the habits the lectures taught, required so the post-mortem has data.

1. **Repository.** `main` protected, one reviewed pull request per change, LFS tracking and lockable source formats (weeks 2 and 3). Tags for every milestone and release candidate.
2. **Sprints.** One-week or two-week sprints, the length chosen from your measured `h` and `λ` (week 5). Each sprint has a written goal, a review where at least one person outside the team plays the build, and a retrospective with one owned change. Keep a short record for each in `sprints/`, in the lab 05 format.
3. **Board and log.** One board with the week 7 definition of done and a WIP limit. At each sprint review, add a row per open card to `task_log.csv` in the [lab 08](../labs/lab08.md) format, with `hour` replaced by the review date. This is what your final post-mortem analyses.
4. **Bug tracker.** From milestone 2, every bug goes into one tracker with severity, frequency and priority from the week 10 matrix. Triage at least twice a week, daily in the last week.
5. **Overtime.** Your working agreement's overtime policy from lab 12 applies, and every overtime hour goes into the contribution record.

## Deliverables

### Milestone 1: the plan (end of week 9)

A `PLAN.md` of at most three pages in the repository, tagged `m1-plan`, with:

- The game in three sentences, with the MVP sentence in the week 4 template.
- Capacity: each member's measured hours per week, the weeks left, `C`, the buffer `b` from your jam plan ratio, and `P`.
- The ordered task list in lab 04's format, with tiers, the cut line, `S_MVP` and `m_max`.
- The cut list with dependencies, and cut triggers written as dates (for example, "at the end of sprint 2, if the MVP loop is not playable, all slice work stops").
- The feature freeze date (release minus 5 days) and the first release-candidate date (release minus 3 days).
- The three changes from your jam post-mortem, each with its owner and the check you will apply in week 13.

### Milestone 2: first playable (end of week 11)

- Tag `v0.2.0`: the MVP loop, graybox allowed, played start to end by someone outside the team. Record a video under 60 seconds.
- The bug tracker running with priorities computed as in [lab 10](../labs/lab10.md).
- The signed working agreement from [lab 11](../labs/lab11.md).
- A one-paragraph note comparing hours spent so far with the plan, and any cut-trigger decisions.

### Milestone 3: release candidate dry run (end of week 13)

This is [lab 13](../labs/lab13.md): `RELEASE_CHECKLIST.md`, your game-specific checker in `tools/`, and `rc.2` on a restricted itch.io page, downloaded and run on a second machine. It is marked through lab 13's rubric.

### Release (first day of week 15)

- `v1.0.0` on your itch.io page (restricted is fine; share the link with the markers), uploaded with butler and `--userversion 1.0.0`, with the version and commit hash visible on the title screen.
- The repository at tag `v1.0.0`, containing:
  - `README.md` with setup (`git lfs install`), the pinned engine version and the one-line export command.
  - `CHANGELOG.md` with a heading for every tagged version from `0.2.0`.
  - `RELEASE_CHECKLIST.md` with the final run filled in: pass or fail, who checked, when.
  - `KNOWN_ISSUES.md` listing every open P3 bug, in words a player understands.
  - `task_log.csv`, `sprints/`, the tracker export and the working agreement with its overtime policy.
- `RELEASE_RECORD.md`, one page: the go/no-go meeting's date, the release candidate tag that shipped, each checklist owner's pass, the count of open P1 and P2 bugs (it must be zero, or the page says why you shipped anyway), and every problem found after upload.

## The release demo (week 15, 12 minutes per team)

1. **Download (4 minutes).** A marker downloads the build from your itch.io page onto a lab machine and plays with no help. The team watches silently, as in GD101 week 7.
2. **Release record (3 minutes).** The team shows the checklist run and the go/no-go record, and names the one item most likely to have escaped.
3. **Questions (5 minutes).** Each member answers one question alone, in the style of the [exam bank](exam-bank.md), rewritten with your team's own data. For example: "Your plan ratio was 1.4. What buffer did that imply, and did your cut line use it?" or "Your tracker shows 9 reopened bugs out of 45 fixes. What does that do to your net drain?"

A member who is absent without an approved reason scores 0 for step 3. The rest of the demo mark is shared.

## Peer assessment

The second round of peer assessment happens at release. It is described in the [peer review brief](peer-review-brief.md), which counts separately (10%). It does not change this component's team mark.

## Rubric

The final team game mark is the total below, out of 100, multiplied by 0.40.

### Milestones and labs (40 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: the plan | 5: capacity from measured hours; buffer from the jam `R`; cut line placed without skipping; `m_max` stated; dated triggers; three jam changes with checks | 3 to 4: one element estimated rather than measured, or triggers vague | 1 to 2: a feature list without capacity or a cut line | 0 | 5 |
| M2: first playable | 5: `v0.2.0` loop played start to end by an outsider on video; tracker live with computed priorities; agreement signed | 3 to 4: playable with help, or tracker incomplete | 1 to 2: not playable start to end | 0 | 5 |
| [Lab 10](../labs/lab10.md), bug triage and forecast | Lab rubric percentage × 10 | | | | 10 |
| [Lab 12](../labs/lab12.md), recovery plan | Lab rubric percentage × 10 | | | | 10 |
| [Lab 13](../labs/lab13.md), release checker and dry run | Lab rubric percentage × 10 | | | | 10 |
| **Subtotal** | | | | | **40** |

### Release (60 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Release process | 18 to 20: built from a clean clone of the tag by script; checklist run with owners and pass evidence on every line; go/no-go recorded; zero open P1 and P2, or a reasoned exception; version, changelog, title screen and itch.io user version agree; known issues listed | 13 to 17: one element thin (a checklist line without evidence, or a version mismatch) | 7 to 12: checklist written but not run, or built from a laptop | 0 to 6: no checklist or no tags | 20 |
| Runs and completes | 9 to 10: the downloaded build runs first time; a stranger reaches a win or loss and restarts | 6 to 8: runs after a small fix noted in the README | 3 to 5: needs the team's help to start or finish | 0 to 2: does not run | 10 |
| Scope delivered | 9 to 10: every MVP and slice task from the M1 plan shipped, or its cut is logged with the date and the trigger that fired | 6 to 8: most shipped; one cut undocumented | 3 to 5: the shipped game differs from the plan with no record of why | 0 to 2: no plan to compare with | 10 |
| Quality in play | 9 to 10: in a 10-minute session the marker meets no S1 or S2 bug; feedback makes every action readable; one look and sound throughout | 6 to 8: one S2, or uneven feedback | 3 to 5: several S2 bugs, or a section in graybox | 0 to 2: an S1 ends the session | 10 |
| Release demo | 9 to 10: the download works; the team names its riskiest item; each member answers with the team's own numbers | 6 to 8: answers correct but general | 3 to 5: answers vague, or the release record is missing | 0 to 2: cannot run or explain | 10 |
| **Subtotal** | | | | | **60** |

**Total: 40 + 60 = 100.**

"Scope delivered" rewards a plan that met reality honestly. A team that cut a third of its slice at a trigger, logged the cut and shipped a stable game can score full marks there. A team that shipped everything in a build the marker cannot finish cannot.

## Rules

- **Late release.** Up to 48 hours late, the release section is marked out of 45 instead of 60, and the demo is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab for half marks.
- **No crunch as a grading strategy.** The overtime policy you wrote in lab 12 applies to the team. If the contribution record shows members working past it without a logged team decision, the release process criterion loses up to 4 points. The course does not reward a finished game bought with a week of all-nighters.
- **Integrity.** Code and assets must be your team's work or licensed and credited. Every member must be able to explain any file in the repository at the demo. Measurements and logs must be real. An invented log is misconduct, while an honest log that shows the plan failing earns full marks.
- **Shared mark.** All members receive the same mark except demo step 3. Contribution problems go through the week 11 escalation ladder and the [peer review](peer-review-brief.md) component.

## Advice

- **Your jam data is the plan's best input.** Use lab 09's `--lab06` export to get your jam plan ratio, and size the buffer from it.
- **Cut early, by trigger.** Week 12's ledger shows a cut in week 10 saves work, and a cut in week 14 only saves what was unfinished. Your M1 triggers exist so that nobody has to argue for a cut when tired.
- **Coverage first.** Week 13 showed a short check on every failure item beats a careful check on half. Write the checklist system by system before you polish any line.
- **Keep the log going.** The post-mortem, worth 20%, is built from `task_log.csv`, the tracker and the contribution record. Two minutes per person at each review is cheap. Reconstructing it in week 15 is not possible.
