# MMO307 · Progression analysis brief

**Weight:** 30% of the course grade.
**What counts:** Part A, a lab portfolio of seven labs ([01](../labs/lab01.md), [02](../labs/lab02.md), [03](../labs/lab03.md), [04](../labs/lab04.md), [05](../labs/lab05.md), [06](../labs/lab06.md) and [12](../labs/lab12.md)), and Part B, a written progression analysis of one MMO endgame with a 10-minute interview.
**Assigned:** week 1. **Milestone:** end of week 6. **Report due:** end of week 13. **Interview:** in the week 14 lab session.
**Work mode:** individual. Part B may use a shared game choice with classmates, but the numbers, the analysis and the recommendations are your own.
**Lectures:** [week 1, the endgame problem](../lectures/w01-the-endgame-problem.md), [week 2, power creep](../lectures/w02-vertical-progression-and-power-creep.md), [week 3, horizontal progression](../lectures/w03-horizontal-progression.md), [week 4, gear treadmills](../lectures/w04-gear-treadmills-and-item-level.md), [week 5, stat squish](../lectures/w05-stat-squish-when-numbers-get-too-big.md), [week 6, catch-up](../lectures/w06-catch-up-mechanics.md) and [week 12, alternative advancement](../lectures/w12-alternative-advancement-and-account-progression.md).

## What this component is for

The course outcome "design endgame progression that resists power creep" is assessed here. The labs give you one tool per week: the chase model, the ratchet, the frequency model, the season ladder, the squish planner, the allowance function and the AA schedules. The analysis asks you to point all of them at one game and answer the question a live team asks every expansion. How long will this endgame last, who does it leave behind, and what will it cost us in two years?

A good analysis reads like a memo to a design director. It states each number, the model that produced it and what the number means for a named kind of player. It ends with recommendations that change a specific parameter by a specific amount, and it says what each change costs.

## Part A: the lab portfolio (50 points)

| Lab | Week | Title | Checker | Points |
|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Gear chase simulator | `test_gear_chase.py` | 7 |
| [02](../labs/lab02.md) | 2 | Power creep audit | `test_creep.py` | 7 |
| [03](../labs/lab03.md) | 3 | Horizontal reward track | `test_horizontal.py` | 7 |
| [04](../labs/lab04.md) | 4 | The season ladder | `test_ladder.py` | 7 |
| [05](../labs/lab05.md) | 5 | The squish planner | `test_squish.py` | 7 |
| [06](../labs/lab06.md) | 6 | Catch-up simulator | `test_catchup.py` | 7 |
| [12](../labs/lab12.md) | 12 | Designing an AA track | `test_aa_schedules.py` | 8 |
| **Total** | | | | **50** |

Each lab is marked out of 100 with its own rubric and scaled to the points above. Labs 01 to 06 score criteria in bands, Excellent (4), Adequate (2 to 3) and Weak (0 to 1), and a criterion earns `weight × band ÷ 4`. Lab 12 scores each criterion at full marks, half marks or zero. The first criterion in every lab is capped at its lowest band if the checker fails on a clean copy run with `.venv/bin/python`. Each lab is due at the start of the following week's class.

Lab 07 (split register) and lab 13 (patch cadence) are formative here. They feed the [final season design](final-season-design-brief.md).

## Part B: the progression analysis (50 points)

### Choose a game

Pick one of the two options below and say which in your first line.

- **Option 1, Tidereach (invented).** The dossier below describes a fictional MMO. Every number you need is in it. Choose this if you want to spend your time on analysis rather than on sources.
- **Option 2, a shipped MMO.** Analyse the current endgame of a game you know, for example World of Warcraft, Final Fantasy XIV, Guild Wars 2 or The Elder Scrolls Online. Every game fact must be cited with its version or era, from an official source or a maintained wiki, as the lectures do. Where a number is not published (a drop rate, a budget exponent), say so, state the value you assume, and show how your conclusion changes if it is off by half or double. A fact you cannot verify cannot carry a conclusion.

### The Tidereach dossier

Tidereach is an invented MMO in its sixth year. All numbers are invented for this brief.

| System | Current design |
|---|---|
| Gear chase | 14 slots per tier. The raid pays random single drops. A weekly vault shows 3 random items and the player keeps one. The median raider runs the raid 4 times a week. Tiers last 16 weeks. |
| Raid ladder | 4 difficulty rungs 13 item levels apart. A visible upgrade needs 6 item levels. The rule is "the new tier's entry beats the old tier's top". 3 tiers per expansion. |
| Power per item level | Exponential budget, `g = 1%` per item level. Encounters serve a band `F = 2`. |
| Season ladder | Season 1 runs from item level 300 to 372. Season 2 starts at 348. |
| Numbers | Creature health by expansion: 1,200; 9,000; 70,000; 540,000; 4,200,000. A current player hits for 700,000. The UI team wants creature health between 800 and 25,000. |
| Upgrade currency | Weekly cap of 90, not rolling. A full set of upgrades costs 1,620. A season lasts 24 weeks. |
| Horizontal rewards | Six mounts, each `+30%` travel speed in one kind of zone. Raiders spend 45%, 20%, 15%, 10%, 6% and 4% of their time in those zones. PvP players spend 10%, 10%, 5%, 5%, 0% and 70%. |
| Alternative advancement | Uncapped. Flat cost of 8 hours per point, `+1%` power per point. Light players play 5 post-cap hours a week, heavy players 25. |
| Alts | 40 hours from cap to endgame-ready. About 20% of that progress is account-wide. |

### What the report must contain

Write `ANALYSIS.md`, 2,000 to 3,000 words plus tables. Use these sections.

1. **The chase (weeks 1 and 4).** Expected runs and weeks to finish a tier, the upgrade rate at which the median player drops below a floor you choose, and what the weekly vault does to both. Where old gear lands on the next season's ladder, how long it survives, and the patch-day gap, season growth and in-season spread.
2. **Creep and its bill (weeks 2 and 5).** Creep per tier and per expansion, shelf life, and the power multiplier over the next three expansions. Whether a uniform squish can still fit the game's numbers, and if not, a per-era divisor table with its compensation multipliers. How many years your squish buys at the game's growth rate.
3. **Who gets left behind (weeks 6 and 12).** The gap a player who joins 6 weeks late carries under the current cap, and when they finish. The free lateness window your proposed rule would create for a heavy player. The AA power gap between light and heavy players after one and three years, and when it crosses `F`.
4. **Breadth (week 3).** The value of each horizontal reward for each segment, `N_eff`, `G_max`, and how many rewards each segment will chase at an upgrade margin you choose.
5. **Recommendations.** At most five changes. Each one names the parameter, its old and new value, the number it improves, and the number it makes worse. At least one recommendation must be about the game's next two years, not the next patch.
6. **Sources and assumptions.** For option 2, every game fact with a source and its version or era. For both options, a list of every assumption the models make that you think is weakest for this game.

Every number must come from your own lab code, run on the game's numbers. Put the commands in an appendix, with the seed for any simulated value.

### Milestone (end of week 6)

A one-page note, not marked separately but required before the report is accepted. It gives your option, and for option 2 your game and version with three cited sources. It also gives three numbers from labs 01, 02 and 04 run on your game (for example expected runs to finish, creep per tier and landing position) and one question you expect the analysis to answer. Feedback comes back within a week.

### The interview (week 14, 10 minutes)

An examiner asks three questions in the style of the [exam bank](exam-bank.md), rewritten with the numbers from your report. At least one is a compute question you answer on paper. At least one asks what happens to one of your recommendations if a parameter changes, for example "What if the median raider runs 2 times a week, not 4?" You may bring your report.

## Rubric for Part B

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| The chase | 11 to 12: expected runs, the floor crossing and the vault effect correct; ladder landing, survival and the three gaps correct and read for a named player | 7 to 10: one calculation wrong or unexplained | 3 to 6: numbers without interpretation, or two errors | 0 to 2 | 12 |
| Creep and squish | 9 to 10: creep, shelf life and multiplier correct; dynamic-range test shown; divisor and compensation tables consistent; headroom computed | 6 to 8: one table incomplete | 3 to 5: squish treated as uniform without a test | 0 to 2 | 10 |
| Late players and AA | 9 to 10: shelf gap and finish week correct; free window for the proposed rule; AA gap at one and three years with the crossing week | 6 to 8: one of the three missing | 3 to 5: qualitative only | 0 to 2 | 10 |
| Breadth | 5 to 6: values, `N_eff` and `G_max` for both segments; chase lists at a stated margin | 3 to 4: one segment only | 1 to 2: tooltip values treated as worth | 0 | 6 |
| Recommendations | 6 to 7: each change has a parameter, old and new value, a gain and a cost in numbers; one two-year recommendation | 4 to 5: one change missing its cost | 1 to 3: advice without numbers | 0 | 7 |
| Accuracy and writing | 5: every fact sourced with version or era (option 2) or every assumption named (option 1); commands reproduce; plain, within length | 3 to 4: one unsourced fact or unreproducible number | 1 to 2: several | 0 | 5 |
| **Part B total** | | | | | **50** |

The interview does not add points. It confirms the report. If you cannot explain a number in your report, the criterion that uses it is marked as if the number were missing. If the interview shows you understand a number better than the report does, the examiner may raise that criterion by one band.

## Totals

Part A (50) plus Part B (50) gives the component mark out of 100. Your progression analysis component is that mark multiplied by 0.30.

## Advice

- **Run the labs on your game as you go.** Every lab's design task is a rehearsal for one section of the report. If you choose Tidereach, run lab 01 on its chase in week 1 and lab 02 on its ladder in week 2, and the report is mostly written by week 7.
- **Name the player.** "The chase is too long" earns little. "The median raider crosses a 20% upgrade floor in week 5 of a 16-week tier" earns a lot.
- **Price every recommendation.** Each lecture ends with the trade-off its lever creates. A recommendation without a cost is incomplete.
