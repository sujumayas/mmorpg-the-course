# MMO306 · Week 07 — Tuning Encounters with Logs

**Why this matters:** After a raid boss ships, you stop guessing how hard it is. Thousands of groups pull it, and their combat logs tell you exactly where they fail. The hard part is reading those logs without fooling yourself, and knowing how far one tuning change will move the number of guilds who get the kill. A 5% health cut sounds small. Near the middle of the field it can add half again as many guilds able to win.

**You will be able to:**
- Compute a boss's kill rate from a sample of groups' best-pull DPS, and predict how a health change moves it.
- Derive the slope of the kill-rate curve and explain why the same nerf helps many groups near the median and few in the tails.
- Build a death table from a combat log and decide whether a boss needs a health change or a mechanic change.
- Correct a logged statistic for upload bias before you tune to it.

**Before class:** Warcraft Logs, "Getting Started" help page (what a combat log is and how uploads work). Reread MA102 week 12 (percentiles) and week 13, section 5 (bias). Skim the hotfix list for Queen Ansurek in the Warcraft Wiki tactics page (Nerub-ar Palace, autumn 2024).

**Prerequisites from earlier courses:** [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md) (the damage check `H / T`). [MMO303 week 1, what balanced means](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w01-what-balanced-means.md) (tuning margin). [MA102 week 8, the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md). [MA102 week 13, sampling and bias](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md). [DB201 week 10, telemetry events](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md). From this course, [week 4, the enrage line](w04-encounter-mechanics-tank-and-spank-to-dance-fights.md) (required paper DPS and the mechanic tax `u`), and [week 6, raid difficulty tiers](w06-raid-design-and-difficulty-tiers.md).

**Interactive:** [`examples/w07-kill-rate-curve.html`](../examples/w07-kill-rate-curve.html). Keep it open during section 2.

---

## 1. What a combat log is, and what it is not

A **combat log** is a time-stamped list of everything that happened in a fight. Each line is one event. In World of Warcraft, each event carries a timestamp, a sub-event name such as `SPELL_DAMAGE`, and the source and destination units, followed by details like the spell and the amount. Players turn on file logging with the `/combatlog` chat command, which writes to `WoWCombatLog.txt`, and third-party sites such as Warcraft Logs parse that file into charts.

Three facts about logs shape everything in this lecture.

1. **A log records events, not intentions.** It tells you a player died to a fire wave at 131.0 seconds. It does not tell you whether they saw the wave, misread it, or were stuck behind a pillar. For that you still need the telegraph work from earlier in this course and a person watching a recording.
2. **Players choose to upload.** Warcraft Logs needs an account and a client application. A guild that never uploads is invisible. Your own server-side telemetry (DB201 week 10) sees every group, but many studios still read the public sites, because that is where the community argues.
3. **The designer's question is about groups, not players.** A boss is killed by a group on a pull. So the unit of analysis is the pull, and the population you care about is the set of groups trying the boss this week.

### The three numbers you pull from every pull

For every pull of a boss, you want three things:

- **Length**, in seconds, from encounter start to end.
- **Raid DPS**, the total damage the group dealt to the boss divided by the length.
- **First death**, the ability that killed the first player. In most raids the first death starts the collapse, so it is the best single clue to why a pull ended.

Here is a toy log with three pulls on an invented boss, the Warden, who has 440,000,000 health and a 400-second enrage. The damage lines are already summed into chunks so the log stays short. The code reads the log and prints the three numbers per pull, plus a count of deaths by ability.

```python
import csv, io
from collections import Counter

LOG = """t,event,source,target,ability,amount
0.0,ENCOUNTER_START,,Warden,,1
40.0,DAMAGE,raid,Warden,all,36000000
52.5,DEATH,Warden,Ines,Cinder Wave,0
90.0,DAMAGE,raid,Warden,all,44000000
96.0,ENCOUNTER_END,,Warden,,0
0.0,ENCOUNTER_START,,Warden,,2
120.0,DAMAGE,raid,Warden,all,118000000
131.0,DEATH,Warden,Tomas,Cinder Wave,0
133.5,DEATH,Warden,Ruth,Falling Glass,0
240.0,DAMAGE,raid,Warden,all,112000000
251.0,ENCOUNTER_END,,Warden,,0
0.0,ENCOUNTER_START,,Warden,,3
200.0,DAMAGE,raid,Warden,all,205000000
388.0,DAMAGE,raid,Warden,all,195000000
400.0,DEATH,Warden,Ines,Enrage,0
400.0,ENCOUNTER_END,,Warden,,0
"""

pulls, deaths = [], Counter()
for row in csv.DictReader(io.StringIO(LOG)):
    if row["event"] == "ENCOUNTER_START":
        cur = {"id": row["amount"], "damage": 0, "first_death": None}
    elif row["event"] == "DAMAGE":
        cur["damage"] += int(row["amount"])
    elif row["event"] == "DEATH":
        deaths[row["ability"]] += 1
        if cur["first_death"] is None:
            cur["first_death"] = row["ability"]
    elif row["event"] == "ENCOUNTER_END":
        cur["length"] = float(row["t"])
        cur["dps"] = cur["damage"] / cur["length"]
        pulls.append(cur)

for p in pulls:
    print(f"pull {p['id']}: {p['length']:.0f} s, raid DPS {p['dps']:,.0f}, "
          f"first death: {p['first_death']}")
print("deaths by ability:", dict(deaths))
```

Output:

```
pull 1: 96 s, raid DPS 833,333, first death: Cinder Wave
pull 2: 251 s, raid DPS 916,335, first death: Cinder Wave
pull 3: 400 s, raid DPS 1,000,000, first death: Enrage
deaths by ability: {'Cinder Wave': 2, 'Falling Glass': 1, 'Enrage': 1}
```

Read the three pulls as a story. The first two ended early, and Cinder Wave caused the first death in both. The third pull survived every mechanic and still lost, because it dealt 400,000,000 damage in 400 seconds against a 440,000,000 pool. That group is about 9% short of the damage check. Those are two different problems, and they need two different fixes. Section 3 comes back to the first kind. Section 2 is about the second.

## 2. Worked example: the kill-rate curve

### The hook

Mythic difficulty of Nerub-ar Palace, the first raid of World of Warcraft: The War Within, opened on 17 September 2024. On 14 October, Blizzard hotfixed the final boss, Queen Ansurek, on Mythic. The list was long. Her health went down by 5%, and about a dozen mechanics were softened, including a 26.7% cut to one poison's damage and a 50% cut to the duration of a debuff.

Why 5%? A player who reads "5% less health" thinks "5% easier." A designer holding the logs knows something else. The effect of 5% depends entirely on where the struggling guilds sit relative to the damage check. If most of them are just short, 5% is a large change. If they are far short, it barely registers. The kill-rate curve is how you see which case you are in.

### The model

From MMO303 week 5, a boss with health `H` and enrage time `T` demands a raid DPS of at least

```
R = H / T
```

Call `R` the **required DPS**. In [week 4](w04-encounter-mechanics-tank-and-spank-to-dance-fights.md) you drew this as a damage line crossing the boss's health pool, and you saw that mechanics tax a group's paper DPS by its uptime `u`. Now add the population. Every group `g` has a best sustained raid DPS `D_g`, which you read off its logs. A group can kill the boss (as far as damage goes) if `D_g ≥ R`. So the **kill rate**, the fraction of groups able to meet the check, is

```
K(H) = fraction of groups with D_g ≥ H / T
```

That is the whole model. `K` is one minus the cumulative distribution of group DPS, read at `H / T`. Every symbol:

- `H`, boss health. The lever you pull in a hotfix.
- `T`, enrage time in seconds. A second lever.
- `R = H / T`, required DPS.
- `D_g`, the best raid DPS group `g` has shown on this boss, taken from its logs. This is damage that landed, so it already includes each group's own mechanic tax from week 4.
- `K`, the share of groups whose `D_g` clears `R`.

### Numbers you can check

Here are twenty groups' best raid DPS on the Warden, in thousands, sorted:

```
1380 1290 1210 1160 1120 1080 1060 1050 1020  990
 970  940  910  890  860  830  800  760  720  650
```

With `T = 400` seconds, count the groups at or above `R` for several health values:

| Boss health `H` | Change from 440M | Required DPS `R = H/T` | Groups with `D ≥ R` | Kill rate `K` |
|---|---|---|---|---|
| 480,000,000 | +9.1% | 1,200,000 | 3 | 15% |
| 440,000,000 | — | 1,100,000 | 5 | 25% |
| 418,000,000 | −5% | 1,045,000 | 8 | 40% |
| 400,000,000 | −9.1% | 1,000,000 | 9 | 45% |
| 396,000,000 | −10% | 990,000 | 10 | 50% |

Check one row by hand. At 418M, `R = 418,000,000 / 400 = 1,045,000`. The groups at 1,080, 1,060 and 1,050 now clear it, joining the five that already did, so 8 of 20 groups, or 40%.

A 5% health cut took the kill rate from 25% to 40%. That is 60% more guilds able to meet the check. The next 22M (to 396M) adds only two more groups, because the gap between 1,045 and 990 happens to hold only the groups at 1,020 and 990. A sample of twenty is lumpy. A smooth model shows the shape underneath.

### The smooth version: log-normal groups

Group DPS is the product of many factors: gear level, player skill, class mix, how well the group handles movement. Products of many factors tend to give a **log-normal** distribution, one where `ln D` is normally distributed. That shape has a long right tail, which is exactly what logs show: a few groups far above the rest. Write the median group DPS as `m` and the spread of `ln D` as `σ` (sigma). Then

```
z = ln(R / m) / σ
K = 1 − Φ(z)
```

`Φ` is the standard normal cumulative distribution from MA102 week 8. With `m = 1,000,000` and `σ = 0.15` (a spread that fits the twenty groups above), the model gives:

| Boss health `H` | `R` | `z` | Kill rate `K` | Points gained per 1% of health removed |
|---|---|---|---|---|
| 480M | 1,200,000 | 1.215 | 11.2% | 1.3 |
| 440M | 1,100,000 | 0.635 | 26.3% | 2.2 |
| 418M | 1,045,000 | 0.293 | 38.5% | 2.5 |
| 400M | 1,000,000 | 0.000 | 50.0% | 2.7 |
| 360M | 900,000 | −0.702 | 75.9% | 2.1 |

The model agrees with the sample to within 2 points at 440M and 418M. The last column is the important one. Differentiate `K` with respect to `ln H`:

```
dK / d(ln H) = −φ(z) / σ
```

`φ` is the normal density, 0.399 at `z = 0`. Removing 1% of health changes `ln H` by about 0.01, so near the median one percent of health is worth about `0.399 × 0.01 / 0.15 ≈ 2.7` percentage points of kill rate. At `z = 1.2`, where only one group in nine can win, it is worth only about 1.3 points.

That is the one idea to take from this example. **The kill-rate curve is steepest where the median group meets the check, and flat in the tails.** A small health change near the median moves many guilds. The same change on a boss tuned for the top 5% moves almost none, and players will say the nerf "did nothing."

The spread `σ` matters as much as the position. Halve `σ` (a field of very similar groups, like a tightly gear-gated tier) and the slope at the median doubles, to 5.3 points per 1%. A narrow field turns small tuning changes into cliffs.

### A visual you can move

Open the interactive. The left panel shows the distribution of group DPS as a curve, with a vertical line at `R`. The shaded area to the right of the line is the kill rate. The right panel plots `K` against boss health as an S-shaped curve with a dot at the current health.

Drag the health slider from 440M down to 418M. On the left, the line slides a short way into the thick part of the distribution and the shaded area grows fast. On the right, the dot climbs the steep part of the S. Now set health to 480M and drag down by the same 22M. The line moves through the thin tail and the dot barely rises. The same change, two very different results, and the picture shows why. Then drag `σ` down and watch the S sharpen into a step.

### Cross-game recognition

**World of Warcraft, Nerub-ar Palace (patch 11.0, autumn 2024).** Blizzard's Mythic hotfix for Queen Ansurek cut her health by 5% and softened many mechanics in the same patch note. The health cut moves `R`. The mechanic cuts target a different check, the one section 3 covers. Shipping both at once is a sensible way to reach the groups who are close on both counts, though it makes it harder to tell afterwards which change did the work.

**Final Fantasy XIV, the Echo (current era).** Square Enix rarely touches a high-end fight's numbers after release. Instead, once a duty is no longer new, it can add the Echo, a percentage buff to the players' maximum HP, damage dealt and healing. The wiki notes that the Echo changes only the players, never the enemy's health or mechanics. For the damage check, a buff of `e` to every group's damage is the same as dividing boss health by `1 + e`:

```
D_g × (1 + e) ≥ H / T   ⟺   D_g ≥ (H / (1 + e)) / T
```

So a 5% damage buff equals a boss health cut of `1 − 1/1.05 ≈ 4.8%`. Same curve, same slope, delivered as a buff so the enemy's numbers stay intact for the record books.

**World of Warcraft, Mythic+ keystones (The War Within).** Each keystone level raises enemy health and damage by 8%. That is a ladder of damage checks, each one 8% higher than the last. On the kill-rate curve, every level is a fixed step of `ln 1.08 ≈ 0.077` to the right. With `σ = 0.15` around the median, one keystone level costs about `0.399 × 0.077 / 0.15 ≈ 20` points of completion rate. The ladder is built so the population spreads out across levels, and the log shows you where each group tops out.

Three presentations: a health nerf, a player buff, a scaling ladder. One curve underneath. When you meet a new tuning lever, ask how it moves `R` relative to the DPS distribution.

### Eyes-open design judgment

- **Choose the target kill rate on purpose.** The kill-rate curve lets you write a sentence such as "by week 6, 40% of groups attempting Mythic should meet the damage check." Without a target, every nerf is a reaction to forum noise.
- **Tune early changes near the median, and small.** Where the curve is steep, a 3% change can move 8 points. Large early nerfs overshoot and remove the challenge for the groups that were about to earn it.
- **Expect the curve to move on its own.** Every week, groups gain gear and practice, so `m` rises. A boss that sits at `K = 25%` in week 1 may reach 50% by week 5 with no hotfix. Before you nerf, project where natural growth takes the curve.
- **Pick the lever that matches the failure.** A health change helps groups who survive the mechanics and hit the enrage. It does nothing for groups dying to a wave at 90 seconds. The next section shows how to tell them apart.
- **Say what you changed and why.** Players who see a small nerf and a large jump in kills assume favoritism or a bug. A patch note that says "the boss's health was reduced by 5%, which we expect to help groups within a few percent of the enrage" teaches them the curve.

## 3. Which check is failing: the death table

A raid boss sets at least two checks. The **damage check** asks whether the group can deal `H` before `T`. The **execution check** asks whether the group survives the mechanics long enough to try. Logs tell you which one each pull failed.

Take the first death of each wipe, over every wipe on the boss this week. Group them by ability. Divide by the number of pulls. That gives a **death table**:

| First death (share of wiped pulls) | Pulls ended before 200 s | Pulls ended 200 to 399 s | Pulls reaching enrage |
|---|---|---|---|
| Cinder Wave | 41% | 9% | — |
| Falling Glass | 12% | 14% | — |
| Enrage | — | — | 24% |

These shares are invented for the Warden, and they sum to 100% of wipes. Read them as a designer. Half the wipes (50%) start with Cinder Wave, and most of those happen early. Groups that die early never reach the damage check, so a health nerf would not help them at all. The 24% who reach the enrage are the groups the kill-rate curve describes.

Two rules follow.

- **If most wipes reach the enrage, tune `H` or `T`.** Use the kill-rate curve to size the change.
- **If most wipes start with one mechanic early in the fight, tune that mechanic.** Its damage, its telegraph, its timing, or how many players it targets. Look at the patterns in the Ansurek note: a longer cast time, fewer players targeted, less damage. Those are execution-check changes.

A death table has a trap. A mechanic can be the first death because it comes first. If Cinder Wave is the first ability the boss casts, it will lead the table even when it is no harder than anything else. Normalize by exposure: divide deaths to an ability by the number of times players faced it. "Deaths per 100 casts" is fairer than "share of first deaths." This is the same correction GD201 week 14 made for death heat maps, where raw death counts mostly showed where players spent time; see [GD201 week 14](../../GD201-level-and-world-design/lectures/w14-playtesting-levels-with-heatmaps.md).

### Pull survival: where do pulls end?

A second view is the **pull survival curve**: the share of pulls still alive at each second of the fight. You build it from the pull lengths alone. If 100 pulls start and 60 are alive at 100 seconds, the curve reads 0.6 at 100 s. Steep drops mark killers. A drop at the phase change at 180 s says the transition is the wall. A long flat stretch followed by a cliff at `T` says the fight is a pure damage check. Read this curve first. It takes seconds to compute and points you to the right part of the death table.

## 4. Reading logs without fooling yourself

### Upload bias

The kill-rate curve is only as good as the DPS distribution under it. If you build it from public logs, you build it from the groups who chose to upload. Stronger, more organized guilds upload more.

Here is how much that matters. Suppose 1,000 guilds attempt a boss. Of the top half by DPS, 80% upload. Of the bottom half, 20% upload. The logs hold 400 top-half guilds and 100 bottom-half guilds, 500 in all. The median logged guild is the 250th from the top of the logs. All 400 top-half uploaders come first, so it is the 250th of them. Those uploaders are spread evenly through the top 500, so the 250th uploader sits at about rank `250 / 0.8 ≈ 312` of the whole population. That guild is at about the **69th percentile**, not the 50th.

If you tune "for the median guild in the logs," you are tuning for a guild better than two thirds of the real field. The kill rate you predicted for the logged population will be too high for the real one.

Two fixes:

1. **Use your own telemetry** where you have it. Server-side encounter records see every pull by every group. This is the main reason DB201 week 10 asked you to design an encounter event.
2. **Reweight.** If you know the upload rate for each band (from your telemetry, or from a survey), weight each logged guild by `1 / upload rate`. A bottom-half guild then counts four times as much as a top-half guild, which restores the real mix.

### Best pull, not average pull

Use each group's best sustained DPS on the boss, not its average across pulls. Early pulls are practice and die before the group reaches full output. Averages mix execution failures into the damage number. MA102 week 12 made the same point about summaries: choose the one that answers your question.

### Small samples and early weeks

In week 1, perhaps 200 groups have reached the last boss, and they are the strongest 200. The sample is small and biased toward the top. MA102 week 13 gave you confidence intervals for a rate. A kill rate of 25% from 200 groups carries a 95% interval of about ±6 points. Two weeks later, with 2,000 groups, the same interval is about ±2 points. Make large changes on large samples.

### Survivorship

Groups who gave up on the boss vanish from next week's logs. Their absence raises the next week's median DPS and makes the boss look easier than it was. If you track "groups attempting" week by week, keep the ones who stopped in the denominator, or at least count them.

## 5. Tuning with a target, step by step

Pull the pieces together into a method you can run each week after a raid opens.

1. **State the target.** "By the end of week 4, 35% of groups who reached this boss should kill it on Mythic."
2. **Split the wipes.** Build the death table and the pull survival curve. Decide whether the damage check, the execution check, or both is holding groups back.
3. **For the damage check,** fit `m` and `σ` from best-pull DPS, corrected for upload bias. Compute the health `H*` that gives the target kill rate:

   ```
   H* = T × m × exp(σ × z*)     where z* = Φ⁻¹(1 − K_target)
   ```

   With `m = 1,000,000`, `σ = 0.15`, `T = 400` and a 35% target, `z* = Φ⁻¹(0.65) ≈ 0.385`, so `H* ≈ 400 × 1,000,000 × e^0.0578 ≈ 423,800,000`. That is a 3.7% cut from 440M.
4. **Project growth.** If median DPS rises 2% a week from gear, the same 35% arrives two weeks later with no hotfix at all. Decide whether to wait.
5. **Change one lever at a time when you can.** If you must change both checks together, predict each effect separately and record the prediction, so next week's logs can test it.
6. **Write the patch note** with the reasoning in one sentence.

## In-class activity (25 minutes)

In groups of three. Materials: the interactive, a printout of the twenty-group sample from section 2, and this invented week-3 death table for a second boss:

| First death | Share of wipes | Median time of death |
|---|---|---|
| Shard Rain | 18% | 250 s |
| Glass Tether | 47% | 95 s |
| Enrage | 35% | 360 s |

1. For the Warden, find the smallest health change (to the nearest 1%) that reaches a 40% kill rate in the smooth model with `m = 1,000,000` and `σ = 0.15`. Check it on the twenty-group sample.
2. Repeat with `σ = 0.30`. Explain in one sentence why the answer changed.
3. For the second boss, decide which lever to pull first. Write the one-line patch note you would ship.
4. Name one reason your answer to step 3 could be wrong, and what data would tell you.

Expected output: two health values, a lever choice with its patch note, and one named risk.

## Common misconceptions

- **"A 5% nerf makes the boss 5% easier."** A 5% health cut lowers `R` by 5%. The change in kill rate depends on how many groups sit in that 5% band. Near the median it can be 13 points; in the tails, under 2.
- **"The public logs show the player base."** They show the players who upload, and those skew strong. Correct for upload rate or use server-side data.
- **"The ability at the top of the death table is the hardest one."** It may just come first. Normalize deaths by how many times players faced the ability.
- **"If the boss is too hard, cut its health."** Only if groups reach the enrage. A group dying at 90 seconds gains nothing from less health.

## Check yourself

1. Using the twenty-group sample with `T = 400`, what is the largest boss health at which the kill rate is still 25%? What happens to the kill rate if the enrage timer is extended to 420 seconds at 440M health?
2. In the smooth model with `m = 1,000,000` and `σ = 0.15`, estimate the kill-rate gain from cutting health by 2% at `H = 400M`. Now do the same at `H = 480M`.
3. Final Fantasy XIV adds an Echo buff of 10% damage to a fight. What boss health cut is that equivalent to for the damage check?
4. In the upload-bias example, suppose the top half uploads 60% and the bottom half 40%. At what population percentile is the median logged guild?
5. A boss's death table shows 70% of wipes reaching the enrage, and the kill rate is 20%. Your target is 30%. With `σ = 0.15`, roughly how much health would you remove? Show the slope estimate.

<details>
<summary>Answers</summary>

1. The fifth-best group has 1,120,000 DPS, so five groups clear any `R` up to 1,120,000. The largest health is `1,120,000 × 400 = 448,000,000`. Above that the kill rate drops to 20%. With `T = 420`, `R = 440,000,000 / 420 ≈ 1,047,619`, so the groups at 1,080, 1,060 and 1,050 join: 8 of 20, or 40%. Extending the enrage by 5% acts like a 4.8% health cut.
2. At `H = 400M`, `z = 0`, slope about 2.7 points per 1%, so about 5.3 points (the exact model gives 50.0% to 55.4%). At `H = 480M`, `z = 1.215`, `φ(1.215) ≈ 0.19`, slope about 1.3 points per 1%, so about 2.5 points.
3. `1 − 1/1.10 ≈ 9.1%` of boss health.
4. Uploads are 300 top-half and 200 bottom-half guilds, 500 in all. The median logged guild is the 250th from the top, within the top-half uploaders, at population rank about `250 / 0.6 ≈ 417`. That is about the 58th percentile.
5. `K = 20%` means `z = Φ⁻¹(0.8) ≈ 0.842`, `φ(0.842) ≈ 0.28`, slope `0.28 / 0.15 ≈ 1.9` points per 1% of health. Ten points needs about 5% (the exact answer: `K = 30%` needs `z = 0.524`, a change in `ln H` of `0.15 × (0.842 − 0.524) ≈ 0.048`, a cut of about 4.7%). Because 70% of wipes reach the enrage, the health lever is the right one.

</details>

## Lab / assignment hook

[Lab 07, tuning from logs](../labs/lab07.md). You parse an invented encounter log, build the death table and pull survival curve, fit the kill-rate model to 300 groups' best pulls, correct it for upload bias, and write a tuning memo. The encounter-design assignment (40%) asks for a tuning target and death-table plan for each of your bosses.

## Sources

- Warcraft Wiki, "COMBAT_LOG_EVENT" (current, notes the change in Midnight patch 12.0.0 that removed addon access to this event). Base event fields: timestamp, sub-event, source and destination units. https://warcraft.wiki.gg/wiki/COMBAT_LOG_EVENT
- Warcraft Logs, "Getting Started With Warcraft Logs" (help page, archived June 2026). The `/combatlog` command, the `WoWCombatLog.txt` file, Advanced Combat Logging, account-based and voluntary uploads, live logging. https://www.warcraftlogs.com/help/start
- Blizzard Entertainment, "The War Within Season 1 and Raid Schedule Overview" (22 July 2024). Mythic Nerub-ar Palace opened on 17 September 2024. https://worldofwarcraft.blizzard.com/en-us/news/24117143/the-war-within-season-1-and-raid-schedule-overview
- Warcraft Wiki, "Queen Ansurek (tactics)", patch changes. Hotfix of 14 October 2024: on Mythic, health reduced by 5%, Frothy Toxin damage reduced by 26.7%, Essence Scarred duration reduced by 50%, and other mechanic changes. https://warcraft.wiki.gg/wiki/Queen_Ansurek_(tactics)
- Warcraft Wiki, "Mythic+" (The War Within era). Enemies gain 8% health and damage per keystone level. https://warcraft.wiki.gg/wiki/Mythic%2B
- Final Fantasy XIV Online wiki (consolegameswiki), "The Echo", game mechanic section (current). A percentage buff to player HP, damage and healing, added to group duties once they are no longer new; does not change enemy health or mechanics. https://ffxiv.consolegameswiki.com/wiki/The_Echo
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Background on analytics-driven balance.

## Interactive spec: examples/w07-kill-rate-curve.html

**The one insight.** The same health change moves the kill rate a lot when the required-DPS line sits in the thick middle of the group-DPS distribution, and almost not at all in the tails. The student must see the shaded area jump near the median and crawl at the edges.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (left panel first).

- **Left panel, "Groups by best raid DPS."** x-axis: raid DPS from 500,000 to 1,800,000. y-axis: density (unlabeled ticks are fine). Draw the log-normal density `f(D) = φ((ln D − ln m)/σ) / (σ D)` as a filled curve in `--ink-soft` at low opacity. Draw a vertical line at `R = H / T` in `--blood`, labeled "required DPS". Shade the area to the right of `R` in `--moss`, labeled "can kill: K%". When the "sample" toggle is on, overlay the twenty sample groups from the lecture as dots along the x-axis (values in thousands: 1380, 1290, 1210, 1160, 1120, 1080, 1060, 1050, 1020, 990, 970, 940, 910, 890, 860, 830, 800, 760, 720, 650), filled `--moss` if `D ≥ R`, hollow otherwise, with the count "k of 20" shown.
- **Right panel, "Kill rate vs boss health."** x-axis: boss health from 300M to 600M. y-axis: kill rate 0% to 100%. Plot `K(H) = 1 − Φ(ln(H/(T·m))/σ)` as a line in `--ochre`. A dot at the current `H`. A short tangent segment at the dot showing the slope, with a label "≈ X points per 1% health" where `X = 100 × φ(z) × ln(1.01) / σ` rounded to 1 decimal.
- **Readout row** beneath both panels: `H`, `R`, `z`, `K` (1 decimal), slope label, and when the sample is shown, "sample: k/20".

**Controls.**

- Boss health `H`: slider 300M to 600M, step 1M, default 440M. Also two buttons "−5%" and "+5%" that multiply `H` by 0.95 or 1/0.95 and animate the line (instant if `prefers-reduced-motion`).
- Enrage `T`: slider 300 to 600 s, step 10, default 400.
- Median group DPS `m`: slider 700,000 to 1,400,000, step 10,000, default 1,000,000.
- Spread `σ`: slider 0.05 to 0.40, step 0.005, default 0.15 (the half-step is needed to reach the `σ = 0.075` test value).
- Toggle "Show the 20-group sample" (default on).
- Toggle "Logged guilds only (upload bias)": when on, the displayed density is the population density reweighted by upload rate `u(D) = 0.8` if `D ≥ m`, `0.2` if `D < m`, renormalized; `K` is recomputed on the reweighted density and a note shows "logged K" next to "true K". Default off.
- Echo mode (optional stretch): a slider "player damage buff e" 0% to 20%; the effective required DPS becomes `R / (1 + e)`.

**Formulas.** `R = H/T`. `z = ln(R/m)/σ`. `K = 1 − Φ(z)`. Use an accurate `Φ` (for example the Abramowitz and Stegun 7.1.26 erf approximation, error below 1.5e-7). Slope per 1% = `100 × φ(z) × 0.01 / σ` percentage points (the lecture's approximation that 1% of health moves `ln H` by 0.01; using `ln(1.01)` instead would print 2.6 at 400M).

**Test values** (defaults `T = 400`, `m = 1,000,000`, `σ = 0.15`):

| `H` | `R` | `z` | `K` | sample k/20 |
|---|---|---|---|---|
| 480M | 1,200,000 | 1.215 | 11.2% | 3 |
| 440M | 1,100,000 | 0.635 | 26.3% | 5 |
| 418M | 1,045,000 | 0.293 | 38.5% | 8 |
| 400M | 1,000,000 | 0.000 | 50.0% | 9 |
| 360M | 900,000 | −0.702 | 75.9% | 13 |

Slope label at 400M: 2.7 points per 1% health. At 480M: 1.3. With `σ = 0.075` at 400M: 5.3. Upload-bias toggle at 400M: true K 50.0%, logged K 80.0% (because the logged population is 80% above the median).

**First screen.** Defaults, sample on. The shaded area and "K = 26.3%" are visible without scrolling. No instructions paragraph above the panels; one line of caption under the title: "Drag health. Watch how much the kill rate moves."

**Accessibility.** All sliders keyboard operable with visible focus; readouts in an `aria-live="polite"` region. Colors from the shared tokens; the sample dots use shape (filled vs hollow) as well as color.
