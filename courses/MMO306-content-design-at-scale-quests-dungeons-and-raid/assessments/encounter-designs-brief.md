# MMO306 · Encounter designs brief: the encounter portfolio

**Weight:** 40% of the course grade.
**Assigned:** week 2. **Lab pieces:** due with each lab, before the next lecture. **Checkpoint:** week 7 lab session. **Encounter dossier:** due before the week 12 lecture.
**Work mode:** each lab follows its own work mode (Labs 02 to 06 individual, Labs 07, 10 and 11 in pairs). The encounter dossier is individual.
**Lectures:** weeks 2 to 7, 10 and 11, most directly [week 4, encounter mechanics](../lectures/w04-encounter-mechanics-tank-and-spank-to-dance-fights.md), [week 5, telegraphing and readability](../lectures/w05-telegraphing-and-readability.md), [week 6, raid design and difficulty tiers](../lectures/w06-raid-design-and-difficulty-tiers.md) and [week 7, tuning encounters with logs](../lectures/w07-tuning-encounters-with-logs.md).

## What this component is for

The course's first outcome is "design group encounters with clear mechanics and telegraphs." You can't show that with a pitch. You show it by stating what a boss tests, pricing every mechanic in uptime, healing, attention or lives, sizing each telegraph for the group that will face it, and saying in advance how you will tune the fight once logs arrive. This portfolio collects that work as you do it, week by week, and then asks you to pull it together for one boss you know well.

It also assesses part of the third outcome, "use procedural and repeatable content responsibly," through the player-content rules of Lab 10 and the event schedule of Lab 11. The [final dungeon](final-dungeon-brief.md) (60%) reuses almost everything here, so work you do well now is work you do once.

## Part A: the lab pieces (50 points)

Eight labs count. Each is marked out of 100 with the rubric in the lab itself, then scaled to the points in the table. Lab 01 is formative and does not count here. Labs 08, 09, 12, 13 and 14 feed the final dungeon instead.

| Lab | Week | What it adds to the portfolio | Points |
|---|---|---|---|
| [02](../labs/lab02.md) | 2 | The approach zone's hub layout, with every supported player type reaching the climax | 5 |
| [03](../labs/lab03.md) | 3 | A trash wing whose fastest route passes through the packs you meant players to fight | 5 |
| [04](../labs/lab04.md) | 4 | The encounter calculator and three bosses: a gear check, an execution check and a one-death boss | 8 |
| [05](../labs/lab05.md) | 5 | Three mechanics tuned from measured response times, with failure outcomes | 8 |
| [06](../labs/lab06.md) | 6 | A neutral flex rule and a four- or five-tier ladder for your execution-check boss | 8 |
| [07](../labs/lab07.md) | 7 | A tuning memo from logs: death table, kill-rate fit, upload bias and one hotfix | 8 |
| [10](../labs/lab10.md) | 10 | Reward levers and a publication funnel for player-made content | 4 |
| [11](../labs/lab11.md) | 11 | Reach, crowd and scaling for two world bosses and an hourly event | 4 |

A lab marked 72 out of 100 earns `72 × 8 / 100 = 5.76` points in an 8-point row. Nothing is dropped, because each lab adds a piece the dossier needs.

### Automatic checks

Every lab ships with a test file. Markers run it on a clean copy of your folder with `.venv/bin/python`. If the tests fail there, the lab's code criterion cannot score above its lowest band. Code that runs only on your machine, because of an absolute path or a missing file, counts as failing.

### Spot checks

From week 3 on, a marker picks a few students in each lab session and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own numbers. For example: "Your execution-check boss has a tax of 0.22. What paper DPS does group A need, and at what tax would it start clearing?" or "Your telegraph for mechanic (a) is 1,240 ms. Which measured percentile set it, and what happens to the clean pull if you add one player on a 250 ms connection?"

A spot check never lowers a mark for a slip. It confirms the work is yours. If you cannot explain your own numbers at all, the lab is re-marked after a 10-minute conversation with the instructor.

## Part B: the encounter dossier (50 points)

### The boss

Choose one **signature boss**, normally your Lab 04 execution-check boss as developed in Labs 05 and 06. You may pick a different boss if you redo its numbers with the same tools. The boss is for a group of 10 to 30 players, and the dossier states the group size, the roster (tanks, healers, damage dealers) and whether the size flexes.

Add one **world boss** from Lab 11.

### What the dossier contains

Write it as one document, 3,000 to 5,000 words plus tables, in seven sections.

1. **Boss sheet.** One paragraph on what the fight tests and where it sits in a raid. The mechanic table from the week 4 menu: family, cycle `c`, cost `d` per role, the currency it spends and what it tests. The tax per role and for the raid. The target group's paper DPS and `x`. Kill time from the average model and from Lab 04's simulation, the gap between them and its cause. The deaths budget and the health it implies.
2. **Telegraphs and failure design.** For every mechanic: shape, colour, timer, target marker and sound (week 5, section 3). Its telegraph length, `N × k`, per-player success from Lab 05's measured data, and clean-pull chance or expected misses. The failure outcome (wipe, death, damage or shared damage), with one sentence on why. A latency check for your worst-served region's round trip.
3. **Intensity graph.** The tax over time, phase by phase, drawn from the mechanic schedule. Mark where each mechanic is taught alone and where mechanics combine.
4. **Tier ladder.** The ladder from Lab 06 with the new test each tier adds, the neutral health rule for your roster, the exposure choice for each mechanic (raid-wide, `N / 5` or fixed) with clean-pull numbers at the smallest and largest group, and a catch-up tool priced for groups at 60%, 70%, 80% and 90% of the requirement.
5. **Tuning plan.** A target kill rate with a week ("35% of groups that reach the boss kill it on the top tier by the end of week 4"). An assumed median and spread of group DPS, stated as assumptions. The health `H*` that meets the target, and the growth projection that says whether you would wait. The events your server would log for this boss (DB201 week 10 is the reference). Your rule for choosing between a health change and a mechanic change, based on a death table and a pull survival curve. The patch note you would publish if the rule fires, in one sentence.
6. **World boss.** Interval, join window, `n_min`, `N_crit`, and the health rule `H(n) = H_0 + h n` with kill times at `n_min`, the knee crowd and three times the knee crowd. The check at launch and at 40% population, with the lever you pulled when something failed.
7. **What the numbers changed.** At most 300 words. Name two design decisions you made differently because of a model result, with the result.

### Supporting files

- `dossier.py`, which imports your lab code and prints every number and table in the dossier. A marker must be able to run it from a clean copy and see the same values.
- The Lab 05 data file and any other input you used, unchanged or with your changes explained.
- Figures as PNG or SVG. No copyrighted art, logos or screenshots.

### Checkpoint (week 7 lab session, 5 of the 50 points)

Bring a two-page draft of sections 1 and 2 for your signature boss: the mechanic table, the tax, the kill times and the deaths budget, and a telegraph table with at least three mechanics. A marker gives feedback in the session. Full marks go to a draft where every number is computed and every mechanic has a failure outcome. Numbers may change later, but the dossier must say what changed and why.

## Rubric

Part A rows are scaled from each lab's own rubric. Part B rows are marked in three bands. Excellent earns the full points, Adequate earns half to three quarters of them, and Weak or missing earns a quarter or less.

| Part | Criterion | Excellent | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| A | Lab 02, zone XP budget | Marked by the lab's rubric | | | 5 |
| A | Lab 03, pull planner and routes | Marked by the lab's rubric | | | 5 |
| A | Lab 04, the enrage line | Marked by the lab's rubric | | | 8 |
| A | Lab 05, telegraph tuning | Marked by the lab's rubric | | | 8 |
| A | Lab 06, flexible tier ladder | Marked by the lab's rubric | | | 8 |
| A | Lab 07, tuning from logs | Marked by the lab's rubric | | | 8 |
| A | Lab 10, best-farm simulator | Marked by the lab's rubric | | | 4 |
| A | Lab 11, the event clock | Marked by the lab's rubric | | | 4 |
| B | Checkpoint | Mechanic table, tax, both kill times and a deaths budget, plus a telegraph table with failure outcomes, all computed | Draft present with gaps in the numbers | Missing, or no numbers | 5 |
| B | Boss sheet | States what the fight tests; per-role tax; average and simulated kill times with the gap explained; `H` set from a stated deaths budget | Numbers correct but the purpose or the deaths budget is vague | Mechanics listed without costs, or kill time not checked | 10 |
| B | Telegraphs and failure design | Every mechanic has all channels specified, a telegraph sized from measured data for `N × k`, a latency check and a justified failure outcome | Telegraphs sized from the normal model only, or failure outcomes unjustified | Telegraph lengths guessed | 9 |
| B | Intensity graph and tier ladder | Tax over time drawn from the schedule; each tier adds a named test; neutral rule derived for your roster; exposure choices give clean pulls within 10 points across sizes; catch-up priced at four levels | Ladder complete but one element unpriced or untested | Tiers differ only in health | 9 |
| B | Tuning plan | Dated target, `H*` from the model, growth projection, logged events listed, a decision rule tied to the death table and a one-sentence patch note | Target and `H*` present, decision rule vague | No target, or "we will look at the logs" | 7 |
| B | World boss | Knee, `N_crit` and health rule computed; launch and 40% checks pass after named levers | Works at launch only, or kill times out of band | Schedule chosen by feel | 5 |
| B | Reproducibility and writing | `dossier.py` reprints every number from a clean copy; plain, numeric prose; reflection names two decisions the models changed | Most numbers reproduce; some vague claims | Numbers cannot be reproduced | 5 |
| | **Total** | | | | **100** |

The component mark is this total multiplied by 0.40.

## Rules and advice

- **Keep one boss.** The dossier rewards depth on one fight over breadth across five. Your final dungeon needs three bosses, and the one you develop here can be one of them.
- **Predict, then compute.** Where a lab asks for a prediction before a run, write it first and date it. A wrong prediction with honest working loses nothing. A prediction changed after the run earns the lowest band for that criterion.
- **Name your assumptions.** Median group DPS, response-time spread, session length and population are assumptions until you have telemetry. Label each one and say what data would replace it.
- **Real games.** If you cite a shipped game's number, cite it with its version or era, as the lectures do. If you can't verify a figure, design around it rather than guess.
- **Late work.** A lab piece up to 48 hours late is marked out of 80. After 48 hours it earns feedback and no points. The dossier up to 48 hours late is marked out of 36 of its 45 section points. The checkpoint cannot be late, but a missed checkpoint can be shown at the next lab session for half marks. Extensions for illness or documented reasons follow university policy.
- **Integrity.** You may use lecture and starter code freely. You may use documentation, forums and AI assistants to understand an error or a concept, and you must say so in one line in the relevant report. In pair labs, each partner must be able to explain every number. Measurements and simulation seeds must be your own and recorded.
