# GD202 · Week 07 — Quest Types: Kill, Fetch, Escort, Puzzle, and Redeeming Them

**Why this matters:** Most quests in most RPGs are built from a handful of verbs, and players can name them in their sleep. "Kill ten wolves" is not a bad quest because it involves killing. It goes stale because of how the count, the chance and the walk are set up, and those are numbers you choose. This week you learn to price a quest in player time, see where the frustration hides, and rebuild the four classic types so they earn their place.

**You will be able to:**
- Decompose any quest into a sequence of atomic actions and name its type from that sequence.
- Compute the mean, spread and 90th-percentile kill count of a collect quest from its item count `n` and drop chance `p`.
- Compare quest designs with the same average cost and predict which one players will call a grind.
- Redesign a kill, fetch, escort or puzzle quest by changing one named lever, and state what the change costs.

**Before class:** Doran, J. and Parberry, I. (2011), "A Prototype Quest Generator Based on a Structural Analysis of Quests from Four MMORPGs", sections 1 to 3 (eight pages in total, free on Ian Parberry's site). Bateman (ed.), *Game Writing: Narrative Skills for Videogames*, 2nd ed. (2021), the chapter on quest and mission structure (the course reader lists the pages). Reread your notes from MA102 week 7.

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) covered the wait for a single drop, its mean `1/p` and its long tail. This week counts the wait for several drops and does not re-derive the single case. [MA102 week 10, pity timers](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md) is the toolbox for controlling streaks. Next semester, [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) explains why quest rewards are tied to time. [Last week's quest anatomy](w06-quest-anatomy-hook-objective-complication-reward.md) gave you the hook, objective, complication and reward. This week is about the objective.

**Interactive:** [`examples/w07-drop-rate-tax.html`](../examples/w07-drop-rate-tax.html). Keep it open during section 2.

---

## 1. Four verbs, over and over

### What 750 quests have in common

In 2011 Jonathon Doran and Ian Parberry read more than 750 quests from four online RPGs: EverQuest, World of Warcraft, EVE Online and Vanguard: Saga of Heroes. They were looking for structure, and they found far less variety than you would expect from four teams of writers working for years.

Every quest they read could be explained by one of nine NPC motivations. Four of those nine covered three quarters of the sample. Conquest (the NPC wants an enemy hurt) was the most common at 20.2%. Equipment, Knowledge and Protection followed at about 18% each. Each motivation was carried out through a small set of strategies such as "kill pests" or "rescue NPC", and each strategy was a short sequence of **atomic actions**, the verbs a player can actually perform. Their table lists about twenty: goto, kill, gather, give, take, escort, use, listen, report and a few others.

An atomic action is a single thing the game can check. "You are standing in the cave" is a goto. "The wolf is dead" is a kill. Quests are sentences built from these words.

### The four classic types as action sequences

Write the four types this course names in that grammar, and you can see why they feel the way they do.

| Type | Typical sequence | What the player spends |
|---|---|---|
| Kill | goto, kill × n, goto, report | Combat time, which scales with `n` |
| Fetch (collect) | goto, kill or gather until n items, goto, give | Combat time plus a luck tax set by the drop chance `p` |
| Escort | goto, escort, (defend), goto, report | Travel at someone else's speed, with a failure state you partly don't control |
| Puzzle | goto, use or experiment until solved, report | Thinking time, with a hard stop if the player never finds the solution |

The word **fetch** covers two shapes. A pure delivery ("take this letter to the smith") is goto, give. A collect quest ("bring me eight boar tusks") hides a random process inside the gathering step. That hidden process is the subject of this week's worked example.

### Why designers keep using them

These verbs survive for good reasons. They reuse systems the game already has. A kill quest needs no new code if the game has combat. They are easy to track with a counter, easy to show on a map, and easy to localize (week 11). A zone designer who needs twenty quests by Friday can write twenty kill-and-collect quests.

The cost is that players recognize the sentence before they read it. After the fortieth "bring me n of something", the quest text stops mattering and only the counter is read. Designers call these quests **filler** when they fill time without adding story or decisions. The rest of this lecture is about turning filler into something players choose to do, and the first step is to measure what it costs them.

## 2. Worked example: the drop-rate tax

### The hook

Players who level through quest zones notice something odd. "Kill 20 wolves" and "bring 10 wolf pelts" both average about 20 wolves if half the wolves carry a pelt. On paper they cost the same. Now add a third quest, "bring me the fang of the pack leader", where one wolf in twenty carries the fang. That also averages 20 wolves. Ask a room of players which of the three they would rather not get, and most pick the fang. Is that only a dislike of randomness, or is something measurable going on?

Something measurable is going on. Designs with the same average can have very different worst cases, and players remember the worst cases.

### The model

A collect quest asks for `n` items. Each kill drops one item with probability `p`, independently of every other kill. Let `K` be the number of kills a player needs to finish.

```
mean of K                 E[K]  = n / p
standard deviation of K   SD[K] = sqrt(n × (1 − p)) / p
chance to be done by k    P(K ≤ k) = P(at least n drops in k kills)
```

- `n` is the number of items the quest asks for.
- `p` is the drop chance per kill, between 0 and 1. A plain kill quest is the case `p = 1`.
- `K` counts kills, not items. Multiply by the seconds per kill to get time.
- `P(K ≤ k)` is a binomial tail, the sum over `j = n … k` of `C(k, j) × p^j × (1 − p)^(k − j)`.

`K` has the **negative binomial distribution**. You met its `n = 1` case in MA102 week 7 as the geometric distribution. For `n` items you wait for `n` geometric waits in a row, so the means add up to `n/p` and the variances add up to `n(1 − p)/p²`.

One more quantity matters for design. Divide the standard deviation by the mean and you get the relative spread:

```
SD[K] / E[K] = sqrt((1 − p) / n)
```

Hold the mean fixed and the relative spread shrinks as `n` grows. Many common drops average out. One rare drop does not.

### Numbers you can check

Five quests, all tuned to the same mean of 20 kills. The **P90** column is the kill count by which 90% of players are done, so one player in ten needs more.

| Design | `n` | `p` | Mean | SD | Median | P90 | P99 | Chance of needing more than 40 kills |
|---|---|---|---|---|---|---|---|---|
| The one true fang | 1 | 0.05 | 20 | 19.5 | 14 | 45 | 90 | 12.9% |
| Two rare trophies | 2 | 0.10 | 20 | 13.4 | 17 | 38 | 64 | 8.1% |
| Five tusks | 5 | 0.25 | 20 | 7.7 | 19 | 30 | 43 | 1.6% |
| Ten pelts | 10 | 0.50 | 20 | 4.5 | 19 | 26 | 33 | 0.03% |
| Kill 20 wolves | 20 | 1.00 | 20 | 0 | 20 | 20 | 20 | 0% |

Check two rows by hand. The fang is a single drop at 5%, so `P(K > k) = 0.95^k`. The chance of still waiting after 40 kills is `0.95^40 = 0.129`. The P90 is the smallest `k` with `0.95^k ≤ 0.1`, which is `k = ln 0.1 / ln 0.95 = 44.9`, so 45 kills. For the pelts, `SD = sqrt(10 × 0.5) / 0.5 = 4.47`.

Now read the table as a player. At 20 seconds per kill, every design averages under seven minutes. The pelt quest keeps 90% of players under nine minutes. The fang quest leaves one player in ten past 15 minutes and one in a hundred past half an hour. Put five fang-style quests in a zone and the chance that a given player hits at least one of those 90th-percentile runs is `1 − 0.9^5 = 41%`. Most players will have a bad story to tell.

You can reproduce the percentile columns with a few lines of Python:

```python
from math import comb

def done_by(k, n, p):
    return sum(comb(k, j) * p**j * (1 - p)**(k - j) for j in range(n, k + 1))

def percentile(n, p, q):
    k = n
    while done_by(k, n, p) < q - 1e-12:
        k += 1
    return k

for n, p in [(1, 0.05), (2, 0.10), (5, 0.25), (10, 0.50), (20, 1.0)]:
    print(n, p, [percentile(n, p, q) for q in (0.5, 0.9, 0.99)])
```

```
1 0.05 [14, 45, 90]
2 0.1 [17, 38, 64]
5 0.25 [19, 30, 43]
10 0.5 [19, 26, 33]
20 1.0 [20, 20, 20]
```

### A visual you can move

Open the interactive. The left view shows the mean kill count as a single bar for each of the five designs. All five bars are the same height, which is the designer's spreadsheet view. The right view shows the full distribution of `K` for the selected design as a histogram, with the median, P90 and P99 marked. Click through the designs and watch the histogram stretch to the right while the left bars stay level.

Then use the sliders. Set `n` and `p` yourself, or lock the mean and drag `n`. With the mean locked at 20, dragging `n` from 20 down to 1 lowers `p` to keep the mean fixed, and the P90 marker climbs from 20 to 45. That is the drop-rate tax. It is paid by the unlucky tenth of your players, and the average never shows it.

### Cross-game recognition

The same model, `K ~ negative binomial(n, p)`, describes many quest systems once you rewrite them.

**World of Warcraft, Warlords of Draenor onward (patch 6.0.2, October 2014).** Bonus objectives appear when you enter an area, need no quest giver, and fill a progress bar as you act there. Progress is kept if you leave. The bar replaces "collect `n` items at chance `p`" with many small, certain credits, so in our terms each action is `p = 1` with a large `n`. The relative spread `sqrt((1 − p)/n)` goes to zero. The frustration of the rare drop disappears, and so does the walk back to a quest giver.

**Guild Wars 2 (2012 onward).** Renown hearts are fixed areas on the map with a list of local tasks, and any task on the list fills the same meter. The wiki describes them as an alternative to a checklist done in sequence: you pick whichever listed activity is closest. In our model the heart has several `(n, p)` channels feeding one counter, and each channel has `p` near 1. Players can also leave and return at any time, so a bad run never locks them in.

**Drops for everyone in a group.** When a game gives each group member their own roll on a quest item, `K` is the same for each player as when solo, but kills come faster. When the item drops for only one member, a group of `g` players needs `g × n` items from the same pool, and every player waits for the slowest. Write it as one quest with `n_total = g × n`, and the mean kill count multiplies by `g`. This is a design pattern rather than one game's rule, and games have handled it differently across versions, so check the version of any game you cite for it.

**Pity timers.** MA102 week 10 showed games that guarantee a drop after a run of misses. A pity rule cuts off the right tail of `K` directly. Our table tells you where to put the cut. For the fang, a guarantee on the 30th kill without a drop removes every run past 30. A player reaches the 30th kill without the fang only if the first 29 kills all missed, so about 23% of players ever get that far (`0.95^29 = 0.226`). The mean falls from 20 to 15.7 kills, and the worst case falls from 90 kills at the P99 to 30.

### Eyes-open design judgment

Rare quest drops are not always wrong. They have uses, and each use has a cost.

- **A rare drop makes an item feel special.** The fang from the pack leader should feel harder won than a pelt. If you want that, accept the tail and cap it with pity, or tie the drop to a single named enemy that always drops it (`p = 1`, `n = 1`) and put the challenge in the fight.
- **Tune to the P90, not the mean.** Reward and XP tables are usually set from mean completion time (GD203 week 7). If you set rewards from the mean, your unlucky players are underpaid by exactly the gap between the mean and the P90. Price quests from the P90 time, or narrow the spread until the mean and the P90 are close. Week 6's detour test compares a quest's reward rate `v = R / t` with the player's baseline. Run it with the P90 `t_task` as well as the mean, and you see which quests fail the test for one player in ten.
- **Many small certain steps beat one uncertain one,** if the steps have something to do. A bar filled by 40 identical kills is not better writing. It is only fairer.
- **Randomness in collect quests is often a disguise.** Designers sometimes use a low drop rate to stretch a quest's play time without writing a longer quest. Players read that correctly as padding. If the quest is too short, add content, not variance.

### Check the model

Before you move on, predict and then verify in the interactive. A quest asks for 4 items at `p = 0.2`. What are the mean and SD of `K`? Is its P90 closer to the "five tusks" row or the "two rare trophies" row? (Mean 20, SD `sqrt(4 × 0.8) / 0.2 = 8.9`. Its P90 is 32, close to five tusks.)

## 3. Redeeming the four types

The model above deals with one lever, the randomness of the count. Each classic type has its own typical failure and its own set of levers. The rule for all of them is the same. **Change one lever at a time, and say what the change costs.**

### Kill quests: turn the count into a hunt

A kill quest fails when the killing has no information in it. The player learns nothing by killing the eighth wolf that they did not learn from the first.

The levers are about information and preparation.

- **Replace the count with a target.** One named enemy with a reason to exist beats twenty anonymous ones. The count drops to 1 and the fight has to carry the weight.
- **Add an investigation step before the fight.** The Witcher 3: Wild Hunt (CD Projekt Red, 2015) does this with its witcher contracts. Most contracts follow the same outline. The player reads a notice or talks to the person posting it, can haggle over the fee, then investigates the killings by questioning locals or following tracks with a special sense. Partway through, the bestiary gains an entry for the monster, and the player can read its weaknesses and prepare. In our grammar, the contract is goto, listen, goto, (investigate × several), kill, goto, report. The kill is still there. The steps before it give the player choices (what to ask, what to prepare) and a small mystery.
- **Make the count mean something in the world.** Twenty wolves killed should change the valley. If the quest giver's farm is visibly safer afterwards, the count had a reason.

The cost is production. A contract with an investigation needs scene dressing, dialogue and a unique enemy. You cannot build two hundred of them for one zone, which is why kill quests remain.

### Fetch quests: make the getting matter

A fetch quest fails when the object is only a counter. The player collects eight tusks and hands them over, and the tusks vanish from the story.

- **Give the object a source with a choice.** The herb grows in two places, one guarded, one far away. The player now makes a decision (GD101 week 9 called this a stakes decision).
- **Make the delivery the story.** The letter you carry could be read. Reading it could change what you do next. The quest is now about the letter, not the walk.
- **Cut the return leg when it adds nothing.** Warlords of Draenor's bonus objectives, and many later designs, grant the reward where the work happens. Keep the return only when the conversation at the end is worth the walk.
- **Shrink the tail** with the tools from section 2 if the item must be random.

### Escort quests: give back the pace

Escort quests have the worst reputation of the four, and the grammar shows why. The escort action hands two things to an NPC, the player's pace and the quest's failure state.

- **Speed mismatch.** If the NPC walks slower than the player and faster than the player can comfortably wait, the player spends the quest stopping and starting. Match the NPC's speed to the player's walking speed, or let the NPC wait at checkpoints for the player to catch up.
- **Fragility.** If the NPC can die to damage the player could not reasonably prevent, the player fails for reasons outside their control. Make the NPC tough enough that failure comes from the player's choices, or make the NPC help in the fight.
- **Silence.** An escort is the one quest type where an NPC is beside the player for minutes. Doran and Parberry's "rescue captured NPC" strategy ends with escort, goto, report. That walk is the best place in the whole quest for character dialogue (week 5's companions are escorts that worked).

The cost of these fixes is small in code and large in testing. An escort has more ways to break than any other type, because it runs a second agent through your level.

### Puzzle quests: guarantee a way forward

A puzzle quest fails in two ways. It is too easy and nothing was learned, or the player never sees the solution and quits.

- **Build a hint ladder.** Plan three hints of rising strength and decide what triggers each (time spent, failed attempts, a question the player asks an NPC). The player who solves it without hints has the full experience. The player who needs all three still finishes.
- **Test the solution, not the syntax.** If the player must type or place an exact answer, accept every form of the right answer.
- **Keep puzzles off the critical path in online games,** or let groups share the solution. A puzzle that stops one player in a party stops the party.

### A quick redesign checklist

When you meet a stale quest, run through these levers in order and change the first one that fixes the complaint.

1. **Count and chance.** Is the frustration in the tail? Use section 2.
2. **Verb.** Could a different atomic action carry the same motivation? "Protection" can be kill pests, or it can be repair the fence.
3. **Information.** Does the player learn anything while doing it? Add an investigation or a reveal.
4. **Choice.** Is there any decision? Add a second source, a second solution, or a cost.
5. **Pace and walk.** Who controls the speed, and is the return trip worth it?

## In-class activity (25 minutes)

Work in pairs. Your instructor hands out four filler quests from a fictional starter zone, one of each type, each written as a quest giver's line plus an objective line.

1. **(5 min)** Write each quest as an atomic-action sequence using Doran and Parberry's verbs.
2. **(5 min)** For the collect quest (`n = 6`, `p = 0.3`, 25 seconds per kill), compute the mean, SD and P90 time with the interactive or the lab starter. Mean 20 kills, SD `sqrt(6 × 0.7) / 0.3 = 6.8` kills, P90 29 kills, so about 12 minutes for the unlucky tenth.
3. **(10 min)** Redesign two of the four quests. For each, name the single lever you changed from the checklist, write the new objective line, and state one cost of the change (production time, testing, a new failure case).
4. **(5 min)** Swap with another pair. Each pair picks one of the other pair's redesigns and names a player who will still dislike it, and why.

Expected output: four action sequences, the numbers from step 2, two redesigns with lever and cost, and the other pair's critique.

## Common misconceptions

- **"Same average, same quest."** Designs with an equal mean can differ by a factor of two or more at the P90. Always report a percentile alongside the mean.
- **"Kill quests are bad design."** Doran and Parberry's sample shows how central they are, and a kill can carry a whole quest if the fight is good. The problem is a count with no information in it, not the verb.
- **"A higher drop rate fixes collect quests."** It shrinks the tail but also shortens the quest. If you want the same length, raise `n` and `p` together. The relative spread `sqrt((1 − p)/n)` falls on both counts.
- **"Escort quests fail because players hate NPCs."** Players like companions. They dislike losing control of the pace and the failure state. Fix those two and the escort works.

## Check yourself

1. A quest asks for 8 boar tusks at `p = 0.25`, with 15 seconds per kill. Compute the mean kill count, the SD, and the mean time in minutes.
2. You must keep a collect quest at a mean of 30 kills. Compare `n = 3, p = 0.1` with `n = 15, p = 0.5` by their relative spread. Which will draw fewer complaints, and why?
3. A single-item quest drops at `p = 0.04`. What share of players still lack the item after 50 kills? After how many kills would you put a pity guarantee so that at most 10% of players ever reach it?
4. Rewrite "Escort the wounded scout to the camp" as an action sequence, then name two levers you would change and one new failure case each change creates.

<details>
<summary>Answers</summary>

1. Mean `8 / 0.25 = 32` kills. SD `sqrt(8 × 0.75) / 0.25 = 9.8` kills. Mean time `32 × 15 = 480` s, which is 8 minutes. (The lab starter reports a P90 of 45 kills, about 11 minutes.)
2. Relative spread for `n = 3, p = 0.1` is `sqrt(0.9 / 3) = 0.55`. For `n = 15, p = 0.5` it is `sqrt(0.5 / 15) = 0.18`. The second design has a third of the relative spread, so its unlucky players wait much closer to the mean. Expect fewer complaints, though some players may still find fifteen items dull.
3. `0.96^50 = 0.130`, so 13%. A player reaches a guarantee on kill `m` only if the first `m − 1` kills all missed, which has chance `0.96^(m − 1)`. That must be at most 0.1, so `m − 1 ≥ ln 0.1 / ln 0.96 = 56.4`, which gives `m − 1 = 57` and `m = 58`. At kill 57 the share would be `0.96^56 = 10.2%`, just over the limit. The P90 (57) is where 90% are done, and the guarantee sits one kill later.
4. Goto, escort, (defend), goto, report. Example levers: match the scout's speed to the player's walk (new failure case: the scout reaches ambush points faster, so the player may arrive late to a fight), and let the scout fight back (new failure case: the scout can steal kills or pull extra enemies). Any two levers with a real cost are fine.

</details>

## Lab / assignment hook

[Lab 07, the drop-rate tax](../labs/lab07.md). You implement the negative binomial percentile calculator, audit a five-quest starter zone, and redesign its worst quest twice: once by changing `n` and `p`, once by changing its verb. The redesigned quest goes into your dialogue exercise portfolio (40% of the course grade).

## Sources

- Doran, J. and Parberry, I. (2011). "A Prototype Quest Generator Based on a Structural Analysis of Quests from Four MMORPGs." *Proceedings of the Second International Workshop on Procedural Content Generation in Games* (PCG 2011), Bordeaux. Sample of over 750 quests from EverQuest, World of Warcraft, EVE Online and Vanguard; nine motivations and their shares (Conquest 20.2%, Equipment 18.5%, Knowledge 18.3%, Protection 18.2%); strategies of 1 to 6 actions; the atomic action table. https://ianparberry.com/pubs/pcg2011.pdf
- Warcraft Wiki, "Bonus objective". Introduced in Warlords of Draenor, patch 6.0.2 (14 October 2014); no quest giver; progress kept after leaving the area. https://warcraft.wiki.gg/wiki/Bonus_objective
- Guild Wars 2 Wiki, "Renown Heart" (game version as of 2026). Fixed areas with a list of tasks that all feed one progress meter; no need to talk to the NPC first; progress can be started and stopped at any time. https://wiki.guildwars2.com/wiki/Renown_Heart
- Witcher Wiki, "The Witcher 3 contracts" (base game plus DLC). Typical contract sequence of notice, optional haggling, investigation with Witcher Senses or questioning, bestiary entry, fight. https://witcher.fandom.com/wiki/The_Witcher_3_contracts
- Wikipedia, "The Witcher 3: Wild Hunt". Developer CD Projekt Red; release 19 May 2015.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury. Course text.
- All kill counts, drop chances and times in the worked example are invented for teaching and computed from the negative binomial model in this lecture.

## Interactive spec: examples/w07-drop-rate-tax.html

**The one insight.** Quests with the same average kill count can have very different tails. Fewer, rarer items stretch the right tail of the distribution, so the unlucky tenth of players pays a "drop-rate tax" that the mean never shows.

**Layout.** Two linked views side by side on wide screens, stacked on phones.
- **Left view, "What the spreadsheet sees".** A bar chart with one bar per preset design (five bars), height = mean kills `n / p`. Overlay a thin tick on each bar at its P90 (a second color from the palette), so the gap between the mean and the P90 is visible for every design at once. The selected design's bar is highlighted.
- **Right view, "What players live through".** Histogram of the probability mass `P(K = k)` for the selected design, `k` from `n` to the P99.9 value (cap at 200). Vertical markers for the median, P90 and P99, labeled with their values. Shade the region right of the P90. Show a second, faint outline of the `p = 1` design (a single spike at the mean) for comparison.
- **Number panel** next to the right view: `n`, `p`, mean, SD, relative spread `SD/mean`, median, P90, P99, `P(K > 2 × mean)`, and the P90 time in minutes for the seconds-per-kill setting.

**Controls.**
- Preset buttons for the five designs in the lecture table: (1, 0.05), (2, 0.10), (5, 0.25), (10, 0.50), (20, 1.00). Keyboard: arrow keys move between presets.
- Slider `n` (1 to 40, step 1) and slider `p` (0.01 to 1.00, step 0.01).
- Toggle "Lock mean". When on, a "target mean" field (default 20) fixes the mean, and moving `n` sets `p = n / mean` (clamped to 1; if clamped, show a note that the mean is now `n`). Moving `p` sets `n = round(mean × p)` with `n ≥ 1`.
- Slider "seconds per kill" (5 to 60, default 20).
- Optional toggle "Pity at kill m" (off by default; slider m from `n` to 200). When on, apply only for `n = 1`: `P(K = m)` becomes `(1 − p)^(m − 1)`, and all mass beyond `m` is removed. For `n > 1` show the toggle disabled with the note "pity shown for single-item quests only".

**Formulas.**
- `P(K = k) = C(k − 1, n − 1) × p^n × (1 − p)^(k − n)` for `k ≥ n`.
- `P(K ≤ k) = Σ_{j=n}^{k} C(k, j) p^j (1 − p)^(k − j)`. Compute with log-gamma or iteratively to avoid overflow at `k = 200`.
- Percentile `q`: smallest `k` with `P(K ≤ k) ≥ q − 1e-12`.
- Mean `n/p`, SD `sqrt(n(1 − p))/p`, relative spread `sqrt((1 − p)/n)`.
- With pity at `m` for `n = 1`: mean `= (1 − (1 − p)^m) / p`.

**Test values.**
- (1, 0.05): mean 20, SD 19.49, median 14, P90 45, P99 90, `P(K > 40) = 0.1285`.
- (2, 0.10): median 17, P90 38, P99 64, `P(K > 40) = 0.0805`.
- (5, 0.25): SD 7.75, median 19, P90 30, P99 43, `P(K > 40) = 0.0160`.
- (10, 0.50): SD 4.47, median 19, P90 26, P99 33, `P(K > 40) = 0.0003`.
- (20, 1.00): every percentile 20, SD 0.
- (8, 0.25): mean 32, SD 9.80, P90 45 (check yourself Q1). At 15 s per kill, P90 time 11.25 min.
- (1, 0.05) with pity at 30: mean `(1 − 0.95^30) / 0.05 = 15.71`; P99 becomes 30.

**First screen.** Preset (1, 0.05) selected, lock mean on at 20, 20 s per kill. The left view shows five equal bars with P90 ticks falling from 45 to 20; the right view shows the long-tailed histogram with the shaded tail past 45.
