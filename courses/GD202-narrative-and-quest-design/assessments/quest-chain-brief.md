# GD202 · Quest chain brief

**Weight:** 60% of the course grade, marked out of 100.
**Work mode:** individual. Playtesters and cold readers can be anyone. The design, writing and numbers are your own.
**Assigned:** week 6. **Final submission:** week 15, day 2. **Showcase and viva:** week 15, days 3 to 5.
**Milestones that count toward it:** [lab 06](../labs/lab06.md) (quest spec), [lab 08](../labs/lab08.md) (zone graph), the week 11 playable draft and [lab 13](../labs/lab13.md) (phase budget). [Lab 14](../labs/lab14.md) (test harness) is a required appendix of the final submission.
**Lectures:** the whole course. The table in "What the chain must contain" names the week behind each requirement.

## What this component is for

This is the course's final project: a quest chain with branching dialogue for one zone of an online RPG. It tests all three course outcomes together. You write branching dialogue whose scope you have measured. You design quest structures whose rewards hold up against the player's other options. You use environmental and emergent narrative where they carry the story better than dialogue does.

A chain is done when three things are true. A player can play it through in ink or Yarn Spinner. A reader can check every number in the design document by running your files. And testers who played it can tell you what happened in it.

## What you make

A zone of 12 to 16 quests, told as one story with a spine of 3 to 5 bottleneck quests and ribs between them (week 8). You choose the setting, level range and tone. Everything is your own invention.

Hand in four things.

1. **The design document**, 3,000 to 5,000 words plus tables. Use the section order in the next table.
2. **The scripts.** Every dialogue scene of the chain in ink (`.ink`) or Yarn Spinner (`.yarn`), compiling with no errors or loose ends, playable in Inky or Try Yarn Spinner.
3. **The data files and tools.** The zone CSV (lab 08 format), quest board CSV (lab 06), zone file (lab 13), story file (lab 14), string file (lab 11), and the lab tools, with a README saying which command produces each number in the document.
4. **Appendices.** The lab 14 harness report on your chain, the comprehension test sheets, and your cold-read log from the week 11 draft.

## What the chain must contain

Each row is a section of the design document. The target column is the number a marker checks.

| Section | What it holds | Target | Week |
|---|---|---|---|
| 1. Premise and backstory | The zone's problem in two sentences. An 8 to 12 event backstory, its plot order, `I`, `S` and the open-questions profile. | Every inversion resolves on the spine, or is marked as a deliberate open question | 1 |
| 2. Zone structure | The quest graph, drawn and as a CSV, with `T`, `W`, `C` and zone time at `t_task = 3`, `t_travel = 4`. A paragraph for each spine quest on why it must be a bottleneck. | `C ≥ 0.6`, `T ≤ 6`, `W ≤ 5` | 8 |
| 3. Quest specs | Every quest in four lines (hook, objective with all four slots, complication, reward) with a promise ledger of at least three rows. | No broken promises left. At least three complication types used | 6 |
| 4. Reward logic | The detour table at the arrival level: XP paid, minutes, rate, pass or fail. The complication tax for every complication. For any collect objective, `n`, `p`, mean and P90. | Every quest passes for its intended player, or names the non-XP currency that carries it. Every collect objective has P90 at most 1.5 × mean, or is priced from the P90 | 6, 7 |
| 5. Branching and scope | The dialogue graph report from the lab 03 analyzer: nodes, endings, paths, mean playthrough. Words written and words read on the spine path. | At most 9,000 words written. At least 35% of them read on one playthrough | 2, 3 |
| 6. State | The fact table (name, type, legal values, who writes, who reads, can it go back). The flag ledger. | At least 3 content choices whose flags are read after their bottleneck. At least 1 heavy acknowledgement. No flag written and never read | 2, 4 |
| 7. A reactive NPC | One NPC the player returns to, with 8 to 12 rules and the lab 04 audit. | No silent states, no dead rules, every remaining tie justified | 4 |
| 8. A recurring character | One companion or rival with a values sheet. If their attitude runs on a number, the lab 05 persona table or the lab 09 rematch numbers. | Devotee, wanderer and rival outcomes stated and met, or `R` and `w` meeting the rematch targets you set | 5, 9 |
| 9. Lore delivery | The zone's lore in three tiers. The delivery plan with channels, find chances and expected sentences read. | Every need-to-know fact is forced and in the first sentence of its piece. The plan beats the wall by at least 1.5 times at `s = 0.8` or a fitted `s` | 10 |
| 10. Localization | The string file for every UI and system string of the chain, with context notes and plural forms. Linter output. | The lab 11 linter reports 0 problems | 11 |
| 11. Barks | One bark group the player hears at least 20 times per play-through, with its selection rule and expected back-to-back repeats. | At most 2 expected back-to-back repeats per play-through | 12 |
| 12. Shared and personal story | The consequence table (scope and duration for every world-changing step). The lab 13 report for the chain at 41 players. | Expected visible at least 20 of 40, smallest phase at least 3, or the step moved into an instance with the reason stated | 13 |
| 13. Testing | The lab 14 harness report. The comprehension test: 3 to 5 beats, at least 5 testers, the beat table and what you changed. A test plan naming automatic checks and human checks. | No unreachable nodes, dead ends or dead speakers. Every beat that 3 or more of 5 testers missed is rewritten and retested | 14 |

Sections 5 to 11 can sit on the same few scenes. One well-built spine scene can carry a content choice, a heavy acknowledgement, the reactive NPC and a bark group at once.

### A sample quest entry

This sample is invented to show the level of detail for section 3. Do not reuse its setting.

> **Q7, "The miller's ledger" (rib, level 18).**
> **Hook.** Odran the miller says his ledger vanished the night the sluice failed, and without it he cannot prove who owes him grain.
> **Objective.** Search the flooded counting house (1 ledger) on the east bank of the Reedwater.
> **Complication.** Reversal. The ledger shows Odran sold the lock-keeper faulty timber.
> **Reward.** Access and story. The player chooses to return the ledger or hand it to the lock-keeper (flag `ledger_to_keeper`, read by Q10 and by the reeve's rules R4 and R7). 1,600 XP.
>
> | The hook implies | The reward delivers | Kept? |
> |---|---|---|
> | Odran is the wronged party | Odran is shown to be partly at fault | Kept as a reversal, set up in the hook's "who owes him" |
> | The ledger matters to the zone's story | It decides who takes the blame for the sluice | Yes |
> | Odran is short of grain, not money | No gold from Odran. XP from the game, access to the lock from the keeper if he gets the ledger | Yes |

## Milestones

| When | Milestone | Points |
|---|---|---|
| Start of week 7 | **Lab 06** submitted: three quests in four-line form with ledgers and the detour audit. Marked with its own rubric. | 5 |
| Start of week 9 | **Lab 08** submitted: the zone graph with `T`, `W` and `C`. Marked with its own rubric. | 5 |
| Week 11 lab session | **Playable draft.** The spine scenes in ink or Yarn Spinner, running end to end, with the flag ledger and the lab 03 budget table. A classmate cold-reads one path aloud and logs every place they stumble. Bring the log to the final submission. | 5 |
| Start of week 14 | **Lab 13** submitted: the phase budget, including your own zone file. Marked with its own rubric. | 5 |
| Week 15, day 2 | **Final submission**, with lab 14 as an appendix. | 65 |
| Week 15, days 3 to 5 | **Showcase and viva**, 15 minutes each. | 15 |

Labs 06, 08 and 13 convert as `lab score / 100 × 5`. Lab scores follow each lab's rubric (bands of 4, 2 or 3, and 0 or 1 for labs 06 and 08; full, half or zero marks for lab 13).

## Showcase and viva

You have 15 minutes: 5 to present, 10 for questions. Play one spine scene live in Inky or Try Yarn Spinner on both sides of one content choice, and show where the choice is acknowledged later. The examiners then ask three questions.

- **Change prediction.** The examiner changes one input in your files, such as a drop chance, the funnel, a rival weight or a quest's travel time. You predict which numbers in your document move and in which direction, then run the tool.
- **Exam-bank question.** One question from the [exam bank](exam-bank.md), rewritten with your chain's numbers.
- **Weakest part.** You name the weakest part of your chain, what it costs in numbers, and how you would fix it with one more week.

## Rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Lab 06, quest spec | 5 | Computed from the lab rubric: `lab score / 100 × 5` | — | — | — |
| Lab 08, zone graph | 5 | Computed from the lab rubric: `lab score / 100 × 5` | — | — | — |
| Playable draft (week 11) | 5 | 5: spine runs end to end, ledger and budget table match the script, cold-read log complete | 4: runs, one table out of date | 2-3: runs with a loose end, or no cold read | 0-1: does not run, or not presented |
| Lab 13, phase budget | 5 | Computed from the lab rubric: `lab score / 100 × 5` | — | — | — |
| Premise, structure and arc (sections 1, 2) | 10 | 9-10: all structure targets met; spine beats are real turns of the story; every rib works in any order within its group; backstory inversions resolve on the spine | 7-8: targets met, one bottleneck weakly argued or one rib depends on a sibling | 5-6: one target missed, or spine chosen for numbers rather than story | 0-4: two or more targets missed, or no graph |
| Quest design and reward logic (sections 3, 4) | 12 | 11-12: every quest answers the four player questions; ledgers clean; every quest passes for its intended player; every complication priced and paid back; collect objectives meet the P90 rule | 9-10: one quest fails without a named currency, or one tax unexplained | 6-8: several quests unpriced, or broken promises left | 0-5: specs incomplete or no detour table |
| Branching dialogue and state (sections 5 to 8) | 16 | 15-16: scripts compile clean; word and share targets met; every content choice acknowledged after its bottleneck, with one heavy; fact table and ledger complete; NPC audit clean; recurring character meets its targets; lines are distinct and in voice | 12-14: one target missed with a stated reason, or one flag with no read | 8-11: scope over budget, or choices fold back with no memory | 0-7: scripts do not run, or no state |
| Lore and localization (sections 9, 10) | 7 | 7: need tier forced and first; plan beats the wall by 1.5 times; linter clean with useful notes | 5-6: one need fact left to chance, or notes vague | 3-4: plan under target, or linter problems left | 0-2: missing |
| Barks, shared and personal story (sections 11, 12) | 6 | 6: bark target met with the rule named; consequence table complete; phase targets met, or each exception moved to an instance with a reason | 5: one target missed with a reason | 3-4: numbers without a consequence table, or targets missed without comment | 0-2: missing |
| Testing (section 13, lab 14) | 8 | 8: harness clean on the chain and on the fixed Lantern; each Lantern bug given its `q` and runs needed; comprehension test run with open questions; missed beats rewritten and retested; test plan splits automatic from human checks | 6-7: one of those thin | 4-5: harness run but findings not acted on, or no retest | 0-3: no harness report or no human test |
| Writing and originality | 6 | 6: lines are short, speakable and in character; hooks name a person, a problem and a stake; all content original; document leads with numbers | 5: one weak scene | 3-4: voice drifts, or hooks generic | 0-2: hard to follow, or content taken from existing work |
| Viva: live walkthrough | 5 | 5: both sides of the choice played, later acknowledgement shown, cost stated in words | 4: played, cost missing | 2-3: described rather than played | 0-1: not prepared |
| Viva: change prediction | 5 | 5: correct direction for two outputs with a reason from the model, confirmed by running the tool | 4: one right with sound reasoning | 2-3: guesses, reasons after the run | 0-1: cannot find the input |
| Viva: exam-bank question and weakest part | 5 | 5: correct answer with the model named; weakest part named with its cost and a fix | 4: one slip in either | 2-3: partial method, or a weakness without a fix | 0-1: no method |

The points add to 100: milestones 20, final submission 65, viva 15.

## How the numbers are checked

The marker runs your tools from the README and applies two tests.

- **Trace test.** The marker picks three numbers from the document (for example `C`, a quest's rate and `V`) and finds each in a tool's output from your data files. A number typed into the document that no file produces loses the marks for its section.
- **Script test.** The marker plays your chain in Inky or Try Yarn Spinner along one path you did not demo, and checks that the flags it sets are read where the fact table says.

## Late work

The final submission cannot be late without documented illness or emergency, because the vivas start the next day. Work submitted up to 24 hours late with permission is marked normally. Labs 06, 08 and 13 lose 10 of their 100 points per 48 hours late and can use the free extensions from the [dialogue exercises brief](dialogue-exercises-brief.md).

## Academic integrity

The chain's world, characters, quests and every line of dialogue are your own invention. Do not use characters, places or lore from existing games, books, films or shows, and never paste script text from a shipped game. You may reuse your own lab work and the course's starter code. Name any template you started from. Every fact about a shipped game in the document must come from a course lecture and cite it. Invented playtest or comprehension data scores 0 for the final submission and is treated as misconduct.
