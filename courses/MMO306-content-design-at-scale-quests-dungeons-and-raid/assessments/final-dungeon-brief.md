# MMO306 · Final dungeon brief: a dungeon with three boss encounters

**Weight:** 60% of the course grade.
**Assigned:** week 8. **Milestone 1:** end of week 10. **Milestone 2:** end of week 13. **Final submission:** start of week 15, followed by a 20-minute review and viva in week 15.
**Work mode:** individual, or a pair with a contribution statement. A pair also delivers a second fully tuned difficulty tier (see "Pairs"). In the viva each partner answers alone.
**Lectures:** all fourteen. The ones you will open most are [week 3, dungeon design](../lectures/w03-dungeon-design-trash-bosses-loot.md), [week 4, encounter mechanics](../lectures/w04-encounter-mechanics-tank-and-spank-to-dance-fights.md), [week 5, telegraphing](../lectures/w05-telegraphing-and-readability.md), [week 8, repeatable content](../lectures/w08-repeatable-content-dailies-dungeons-rotations.md), [week 12, tooling and pipelines](../lectures/w12-content-tooling-and-pipelines.md), [week 13, budgets and cadence](../lectures/w13-content-budgets-and-cadence-planning.md) and [week 14, accessibility](../lectures/w14-accessibility-in-group-content.md).

## What this component is for

A dungeon is where every idea in this course meets the others. The approach zone decides who arrives and at what level. The trash decides how long the run takes and how the group moves. The bosses decide what the dungeon tests. The loot and the repeat structure decide how many times players come back, and the production plan decides whether the team can ship it before players run out of the last drop.

This assessment asks you to design one dungeon completely, in prose, in numbers and in content data, and to defend each decision with the model it came from. It assesses all three course outcomes. The bosses, telegraphs and cue tables assess "design group encounters with clear mechanics and telegraphs." The budget, roadmap and locust numbers assess "plan content cadence against consumption rate." The loot, repeat structure and any generated elements assess "use procedural and repeatable content responsibly."

## What you design

A dungeon for a fictional MMO of your own. Name it, sketch it and write its premise in three sentences. No copyrighted characters, settings, art or logos.

- **Group.** A fixed group of 5 to 20 players, or a flexible range inside 10 to 30. State the size and the roster (tanks, healers, damage dealers). Every model in the document uses that size.
- **Length.** A target run time between 20 and 45 minutes for the reference group on the base tier, split into trash, bosses and travel (week 3, section 3).
- **Three bosses.** They must test different things. One is a low-tax fight that checks gear and rotation. One is an execution check whose tax separates a crisp group from a sloppy one (week 4). The final boss has at least two phases, combines mechanics the group has already met in the dungeon, and has a stated deaths budget.
- **Trash.** At least two wings of packs between the bosses, with a forces requirement or a kill-everything rule, and at least one pack per wing that teaches the next boss's mechanic.
- **Tiers.** At least two difficulty tiers. The second may be a harder tier (week 6) or an alternative way to play such as a story version with NPC allies (week 14, section 3). Pairs deliver three.

### What you may reuse

Most of the work already exists in your labs. [Lab 01](../labs/lab01.md) gives the locust functions and the player population. [Lab 02](../labs/lab02.md) gives the approach zone. [Lab 03](../labs/lab03.md) gives the first wing. [Lab 04](../labs/lab04.md), [Lab 05](../labs/lab05.md) and [Lab 06](../labs/lab06.md) give the encounter calculator, telegraph tools and ladder, and your [encounter dossier](encounter-designs-brief.md) boss can be one of the three. [Lab 07](../labs/lab07.md) gives the tuning method, [Lab 08](../labs/lab08.md) the rotation and cap tools, [Lab 09](../labs/lab09.md) the generator measures, [Lab 12](../labs/lab12.md) the validator, [Lab 13](../labs/lab13.md) the roadmap simulator and [Lab 14](../labs/lab14.md) the cue audit. The new work is joining them into one dungeon and checking that the parts agree with each other.

## Deliverables

### 1. `DESIGN.md`, the dungeon document (4,000 to 7,000 words plus tables)

Twelve sections, in this order.

1. **Premise and group.** The three-sentence premise, the group size and roster, the target run time, and the percentile of players (week 1) the dungeon is built for.
2. **Approach zone.** The zone in front of the entrance from Lab 02: `X`, hub split, `n`, `c` and hub coverage for at least three player types, and the breadcrumb quest into the dungeon, which every supported type must reach.
3. **Layout and time budget.** A map sketch with bosses, wings, valleys and checkpoints. The run-time budget. An intensity graph for the whole run with one peak per boss and one bump per pull (GD201 week 3).
4. **Trash.** The pack table for every wing (enemy count, health, damage, forces value, walking time). The pull model's largest safe pull and clear time at base scaling and at a harder tier's scaling. The forces slack. The fastest route from Lab 03's planner, showing it passes through every must-see pack.
5. **The three bosses.** For each: what it tests, in one sentence. The mechanic table with cycle, cost per role, currency spent and tax per role. Paper DPS and `x` of the target group. Kill time from the average model and the simulation. The deaths budget and the health it implies. For the final boss, the tax per phase and the time the target group has left when it enters the last phase.
6. **Telegraphs and failure outcomes.** For every mechanic of every boss: telegraph length, `N × k`, per-player success from measured data, clean-pull chance or expected misses, and the failure outcome with its reason. A latency check at the round trip of your worst-served region.
7. **Accessibility.** The cue table for each boss with the essential mechanics marked, `E` and `G` before and after your fixes, and `E = 0` on every essential mechanic with channels in two senses (Lab 14). The list of barriers the cue table can't see (held or rapid inputs, exact-moment checks, voice-only calls, peak simultaneous rules per phase), each with a fix classified as a per-player setting, a shared encounter change or an alternative way to play.
8. **Tiers.** The ladder table for your tiers with the new test each adds. If the group flexes, the neutral health rule and the exposure choice for each mechanic, with clean-pull numbers at the smallest and largest size.
9. **Loot and repeat structure.** Loot table sizes, items per run and expected runs for one specific item (week 3, section 4). The deterministic path, if any, and its worst case in runs. The repeat structure with numbers from Lab 08: lockout, rotation (with `p`, repeats from yesterday and days or weeks to 90% exposure), cap (hard or accumulating, with `h*`) or first-run bonus (reward per hour curve). One sentence naming the chore it creates.
10. **Generated elements (only if you use any).** The signature, `M`, `M_eff` and `n_50`, measured on accepted outputs, the validation rule and pass rate, and the fallback (Lab 09). If you use none, say why the dungeon is better hand-built.
11. **Tuning plan.** For the hardest tier's final boss: a dated kill-rate target, assumed median and spread of group DPS, `H*`, a growth projection, the events you log and your decision rule for health versus mechanic changes (Lab 07).
12. **Budget and cadence.** A three-point estimate for building this dungeon with one sentence of reasoning for each number. The team count and cadence chosen with Lab 13's simulator, the on-time share of drops over a 12-drop roadmap, and where this dungeon sits on it. `C` and `r` for the dungeon, and `T` and `L` for p50, p90 and p99 of the Lab 01 population. The minor drop you would place in each cycle and the percentile it serves. A slip-or-cut decision for one simulated late drop, with the extra drought for p50, p90 and p99.

### 2. Content data

- `content/dungeon.json` in Lab 12's format, extended for encounters: quests (at least the breadcrumb and one dungeon quest), NPCs, items, loot tables, and one record per boss with its health, enrage, phases, mechanics and cue channels.
- Your Lab 12 validator with your three Part B rules and at least one new rule for encounter records (for example "every boss has an enrage shorter than the instance reset" or "every essential mechanic has channels in two senses"). `validate_content.py content/dungeon.json` must print no errors.

### 3. `numbers.py`

A script that imports your lab code, reads `content/dungeon.json` where it can, and prints every number and table in `DESIGN.md`. The examiners run it from a clean copy with `.venv/bin/python`. A number in the document that `numbers.py` does not print is treated as unsupported.

### 4. Playtest report (at most 2 pages)

Playtest one boss with at least four people outside your team, as a paper prototype (a grid, tokens, cards for mechanics and a timer) or as a graybox in any engine. Record every mechanic failure with its cause (didn't see it, saw it late, misread it, couldn't move in time), the time players took to resolve each mechanic, and one change you made in response, with the model number that changed. A graybox earns no extra marks for looks.

### 5. Roadmap page

One page for two years: major drops with their on-time chance, this dungeon's drop, minor drops, and the p50 and p90 drought lines.

### Pairs

A pair also delivers a third difficulty tier with its own tuned numbers for all three bosses, and `CONTRIBUTIONS.md` with one paragraph each naming the sections and files each partner wrote.

## Milestone 1: pitch and budget (end of week 10, 10 points)

At most three pages. The premise, group size and target run time. The map sketch and time budget. One paragraph per boss saying what it tests, with a first mechanic list and a tax estimate. The approach zone numbers from Lab 02 and the first wing from Lab 03, adjusted to this dungeon. A first three-point estimate for building the dungeon. Feedback comes back within a week. Anything may change later, but `DESIGN.md` must say what changed and why.

## Milestone 2: three tuned bosses and valid data (end of week 13, 15 points)

A 5-minute check in the lab session. Show `content/dungeon.json` passing your validator on your machine. Run `numbers.py` (or a first version of it) and show, for each boss, the tax, both kill times and the deaths budget, and for the hardest mechanic of each boss the telegraph length and clean-pull chance from measured data. Bring a one-page note listing the cue channels of every essential mechanic.

## Review and viva (week 15, 20 minutes)

You run `numbers.py` and the validator from a clean copy on a lab machine while two examiners watch.

1. **Walkthrough (6 min).** Take the examiners through the run with the intensity graph, then through one boss's enrage line and its telegraph table.
2. **Change an input (6 min).** The examiner changes one assumption, for example: the response-time spread rises by 30 ms, outside XP in the approach zone rises to 0.3, enemies scale by `1.08⁵`, the population falls to 40%, or a drop comes in 30 days late. You rerun the numbers and say what breaks, what you would change and which model tells you so.
3. **Questions (8 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your dungeon's numbers. At least one is a compute question you answer by hand, and one asks you to critique a decision in your own document.

## Rubric

Bands for each row: Excellent earns the full points, Adequate earns half to three quarters of them, and Weak or missing earns a quarter or less.

| Stage | Criterion | Excellent | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Milestone 1 | Pitch and budget | Three bosses that test different things, each with a first tax; time budget adds up; zone and wing numbers recomputed for this dungeon; lopsided three-point estimate with reasons | One boss purpose vague, or the budget doesn't add up | Concept only, no numbers | 10 |
| Milestone 2 | Valid data | Content file passes the validator with the new encounter rule; no warnings left unexplained | Passes, but the encounter rule is missing | Fails the validator | 5 |
| Milestone 2 | Three tuned bosses | Tax, average and simulated kill times and a deaths budget for all three; hardest mechanic of each sized from measured data | Two bosses complete, or telegraphs from the normal model only | Kill times not computed | 10 |
| Final | Zone, layout and trash | Every supported player type reaches the breadcrumb; run-time budget matches the pull model within 10%; must-see packs on the fastest route at both scalings; slack between 1.1 and 1.5 or justified | One element off target without a reason | Trash placed by feel | 10 |
| Final | Three bosses | Each boss tests a named, different thing; per-role tax; `H` set from a deaths budget; final boss's phase budget computed; average and simulation gaps explained | Bosses tuned but overlap in what they test, or the phase budget missing | Bosses unpriced or untested against the enrage | 15 |
| Final | Telegraphs and accessibility | Every telegraph sized for `N × k` from measured data with a latency check and a justified failure outcome; `E = 0` on essential mechanics with two senses; non-perception barriers listed and classified | Telegraphs sized but failure outcomes unjustified, or two-senses rule not met on one mechanic | Telegraph lengths guessed, or a colour-only or sound-only essential mechanic | 12 |
| Final | Tiers, loot and repeat structure | Each tier adds a named test; flex rule neutral if used; expected runs per item and worst case stated; repeat structure with Lab 08 numbers and its chore named; generated elements measured on accepted outputs or hand-building argued | Structure described with some numbers missing | Loot or repeats chosen with no numbers | 10 |
| Final | Tuning and production plan | Dated kill-rate target with `H*` and a decision rule; team count and cadence found by simulation; `T` and `L` for three percentiles; minor drops aimed at a named percentile; slip-or-cut decided with numbers | Plan present, one part unsupported by a simulation or a number | Cadence or budget asserted | 10 |
| Final | Content data and reproducibility | `numbers.py` prints every number in `DESIGN.md` from a clean copy; content file passes the validator; validator rules each small and tested | Most numbers reproduce | Numbers cannot be reproduced | 8 |
| Final | Playtest | Four or more outside players; failures recorded by cause with resolve times; one change made and traced to a model number | Playtest run, causes or the change thin | No playtest | 5 |
| Final | Review and viva | Clean run; the changed input handled with the right model and a concrete fix; answers use your own numbers | One step needs help, or answers generic | Cannot run or explain the work | 5 |
| | **Total** | | | | **100** |

The final dungeon mark is this total multiplied by 0.60.

## Rules and advice

- **The labs are the parts.** Start `numbers.py` in week 8 by importing Labs 01 to 06 and printing what you already have. Add each later lab as you finish it. A script written the night before will not agree with the document.
- **Check that the parts agree.** The zone's player types, the trash's group, the bosses' roster and the roadmap's population must be the same people. The most common lost marks are a boss tuned for 20 players in a 5-player dungeon, or a loot table that assumes more runs than the repeat structure allows.
- **Design the failure before the warning.** For each mechanic, decide what a miss costs (week 5, section 5) before you size its telegraph. A wipe mechanic needs a far longer telegraph than a debuff with the same target.
- **Keep the scope small.** Three bosses, two wings, two tiers. Extra bosses earn nothing, and each one is another row every model must cover.
- **Real games.** Cite any shipped game's number with its version or era. If you can't verify a figure, design around it.
- **Late submission.** Up to 48 hours late, the final stage is marked out of 60 instead of 75, and the viva is rescheduled if the timetable allows. Milestones cannot be late, but a missed milestone can be shown at the next lab session for half marks.
- **Integrity.** The rules in the [encounter designs brief](encounter-designs-brief.md#rules-and-advice) apply. Playtest records and simulation seeds must come from your own runs. In the viva you must be able to explain every number and every file you submit.
