# PR402 · Week 06 — Telemetry and Balance Review

**Why this matters:** Your closed beta ended last week. For the first time, people outside the program played your persistent world for days, and your server logged what they did. In three weeks the game goes public. This week decides which balance numbers you change before open beta and which you leave alone. A team that changes everything that "felt off" ships four new problems. A team that changes nothing ships the one class that deletes a mob in half the design time. The review turns a week of tester data into a short list of changes the data can defend.

**You will be able to:**
- Check a beta telemetry export for the three contaminations that break balance numbers (internal accounts, stale builds, broken counts) before computing anything.
- Compare a per-class balance metric against the design target from your PR401 balance document, using a 95% interval at the player level.
- Size a balance change from telemetry so that the predicted value lands inside the target band.
- Decide, per question, whether the closed beta answered it or whether open beta needs a targeted test, and say how many players that test needs.

**Before class:** Export your closed-beta telemetry tables (sessions, kills, deaths, quest completions, encounter results). Bring your PR401 economy and balance design document with its numeric targets. Re-read [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md), sections 2 and 4, on units of analysis and count checks (20 minutes). Skim [MMO303 week 13](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w13-combat-simulators.md), section 4, on validating a simulator against live data (10 minutes).

**Prerequisites from earlier courses:** [PR201 week 11, playtest and telemetry review](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (units, count checks, the evidence table this week extends). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (intervals and why small samples mislead). [MMO303 week 13, combat simulators](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w13-combat-simulators.md) and [MMO303 week 14, communicating balance changes](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md). [MMO307 week 14, measuring balance with win rates and pick rates](../../MMO307-game-balance-ii-pvp-progression-and-endgame/lectures/w14-measuring-balance-with-win-rates-and-pick-rates.md) (if your game has PvP). [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md). PR401 week 8, economy and balance design, is where your targets come from (see the [PR401 week 8 lecture](../../PR401-capstone-i-pre-production/lectures/w08-economy-and-balance-design.md)). PR301 week 10 ran a telemetry review on your prototype (see the [PR301 week 10 lecture](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w10-telemetry-review.md)).

---

## 1. What the closed beta can and cannot tell you

A closed beta of a student MMO usually has one or two hundred active testers, most of whom play two or three sessions, and only a few dozen of them reach any one piece of content. That is enough to answer some balance questions and hopeless for others. Sort your questions before you open a spreadsheet.

- **Rates of things every player does often.** Kill time, deaths per hour, gold earned per hour, time to reach level 5. Every tester produces dozens of events, so the closed beta can answer these at the class level.
- **Outcomes of group content.** Dungeon clears, boss wipes. Your unit is the party, and you may have had eight parties. Expect wide intervals (PR201 week 11, section 2).
- **Anything rare or late.** Endgame gear, crafting chains that take ten hours, PvP between rated players. The closed beta probably did not reach these. Say so, and move them to open beta or to live-ops.
- **Economy flows.** Faucet and sink totals per player-hour are frequent events, so they are answerable. Price levels in a market with 40 players are not; a market that thin has no stable price (MMO304 week 6).

Balance questions have a second filter. They only mean something against a target. "The Hexer kills fast" is an opinion. "The Hexer's median kill time on a level-5 mob is 8.9 seconds and the design target is 12 plus or minus 15%" is a finding. If your PR401 balance document has no numeric target for a question, write one today, date it, and mark it as set after the beta. Honesty about when a threshold was set is marked. Pretending is not.

## 2. Clean the export before you trust it

Three contaminations break balance numbers more often than bad statistics do. Check each one and log what you found.

1. **Internal accounts.** Your own team played during the beta, with admin tools, debug gear and full knowledge of every mechanic. Filter them out by account ID, not by name. One developer who killed 600 mobs with a debug weapon can move a class average by seconds.
2. **Stale builds.** If you patched mid-beta, every balance number from before the patch describes a different game. Tag each event with the build number (PR101 week 13, section 3) and split the table. A number computed across two builds is an average of two games.
3. **Broken counts.** Run PR201 week 11's count checks. Sessions that start must end. Kills must have a matching damage event. Quest completions cannot exceed quest starts. If the counts do not balance, the rate built on them is wrong, and no interval fixes it.

Write the cleaning as a script, not as manual edits in a spreadsheet. You will run the same cleaning on open-beta data in week 8 and on live data in week 10. If the cleaning lives in someone's head, week 10 will not match week 6.

## 3. Pick the unit, then the metric

PR201 taught you to ask "one observation of what?" for party outcomes. Balance data raises the same question in a sneakier form. A tester who plays a Warden for three hours produces 200 kill events. Those 200 kills are not 200 independent observations of the Warden. They share one player's skill, gear choices and habits. A slow player gives you 200 slow kills.

So compute the metric **per player first**, then summarise across players. For kill time, that means each player's median kill time on the standard mob, then the mean and standard deviation of those per-player values. Your `n` is the number of players, not the number of kills. Using kills as `n` shrinks the interval by a factor of about the square root of kills per player, and makes you confident about a number you know little about. The worked example shows how large that error gets.

Choose metrics that isolate the thing you tuned.

| Question | Good metric | Why not the obvious one |
|---|---|---|
| Is class damage in line? | Median time to kill the standard mob, per player | Total damage per session mixes damage with play time |
| Is the healer's solo play viable? | Solo quest completion time, per player | Deaths per hour punishes cautious players less than bad design |
| Is the first dungeon tuned? | Clear rate per party, first attempt | Clear rate per player counts one wipe three to five times |
| Is gold income on plan? | Gold from faucets per player-hour, per player | Gold held rewards hoarders and punishes spenders |

Use medians inside a player where one bad pull (a mob that ran away, a disconnect) can produce a 90-second outlier. Use means across players, because you need the interval.

## 4. Sizing a change from the data

When a class misses its band, the change should be computed, not guessed. Split the metric into the part your change affects and the part it does not. Kill time has two parts:

```
kill time = approach time + mob HP / class DPS
```

Approach time is the gap between aggro and first hit, which your telemetry records and which barely depends on class. The second part scales with damage. To move kill time from its current value to a target, scale damage by:

```
damage multiplier = (current − approach) / (target − approach)
```

This assumes the class spends the fight dealing damage at a steady rate. A class with long cooldowns or a burst opener breaks that assumption, which is why you run the change through your combat simulator (MMO303 week 13) before shipping it. The simulator is your prediction. Next week's data is the test of the prediction.

Change one lever per class per patch where you can. If you cut the Hexer's damage and raise mob HP in the same patch, the next review cannot tell you which change did what.

## 5. Worked example: which classes move before open beta?

### The hook

When Microsoft's user research team tested Halo 3 before its 2007 release, they logged more than 3,000 hours of play from about 600 players and recorded where every player died. Your closed beta's balance sample is a few dozen testers. The method is the same, a metric per player compared with a target. What changes is how often the honest answer is "we cannot tell yet". The skill this example practises is saying that out loud and planning the test that would settle it.

### The model

For each class, take the per-player median kill times, and compute:

```
mean  m = average of the per-player medians
SD    s = standard deviation of the per-player medians
95% interval = m ± t × s / √n
```

`n` is players and `t` is the two-sided 95% value from a t table with `n − 1` degrees of freedom. The t value is larger than 1.96 for small `n`, which widens the interval to account for estimating `s` from few players (MA102 week 13).

Compare the interval with the target band and give one of three verdicts.

- **Act**: the whole interval is outside the band.
- **Leave**: the whole interval is inside the band.
- **Can't decide**: the interval crosses a band edge. This becomes a targeted test in open beta.

### Numbers you can check

Emberfall, the seven-person team used as the running example in this course, had 150 active testers in its closed beta (week 5). After cleaning, 40 of them logged at least ten kills on the standard level-5 mob on the final beta build, and those 40 are the balance sample. Emberfall has two classes with two builds each, and its PR401 balance document gives each build its own target, so this guide treats the four builds as four classes. Its PR401 balance document set the standard level-5 mob at 12 seconds to kill for damage classes, with a band of plus or minus 15% (10.2 to 13.8 s). The healer class, the Mender, has a solo target of 16 s plus or minus 20% (12.8 to 19.2 s), because the team chose to make healers slower alone and faster in groups. All values below are invented teaching values.

| Class | Players `n` | Mean `m` (s) | SD `s` | `t` | 95% interval (s) | Band (s) | Verdict |
|---|---|---|---|---|---|---|---|
| Warden | 9 | 13.1 | 2.4 | 2.306 | 11.26 to 14.94 | 10.2 to 13.8 | can't decide |
| Hexer | 11 | 8.9 | 1.6 | 2.228 | 7.83 to 9.97 | 10.2 to 13.8 | act (too fast) |
| Ranger | 14 | 11.8 | 2.0 | 2.160 | 10.65 to 12.95 | 10.2 to 13.8 | leave |
| Mender | 6 | 17.5 | 3.9 | 2.571 | 13.41 to 21.59 | 12.8 to 19.2 | can't decide |

Check the Hexer row by hand. `s / √n = 1.6 / 3.317 = 0.482`. Times 2.228 gives 1.075. The interval is 8.9 ± 1.075, from 7.83 to 9.97. Its top end is below 10.2, so even the most generous reading of the data says the Hexer kills too fast.

Now the trap from section 3. The nine Warden testers logged 400 kills between them, with a per-kill SD of 4.0 s. Treat kills as `n` and the interval becomes 13.1 ± 1.96 × 4.0 / √400 = 13.1 ± 0.39, from 12.71 to 13.49 s. That sits inside the band, and the verdict flips to "leave" with apparent confidence. Nothing about the Warden changed. Only the unit did.

How many Warden players would settle it? The mean is 0.7 s below the band's top edge. For the interval's half-width to shrink below 0.7 s you need roughly `n = (1.96 × 2.4 / 0.7)² ≈ 46` players. Open beta can deliver that; the closed beta could not. So the Warden gets a targeted test, with instrumentation already in place, rather than a change.

Now size the Hexer change. Telemetry puts approach time at 2.0 s for every class. Aiming at the band's centre:

```
multiplier = (8.9 − 2.0) / (12.0 − 2.0) = 0.690    a 31% damage cut
```

Aiming at 11.0 s instead:

```
multiplier = (8.9 − 2.0) / (11.0 − 2.0) = 0.767    a 23% damage cut
```

The team takes the 23% cut. The interval's top end, 9.97 s, says the Hexer could be closer to the band than the mean suggests, and a 31% cut aimed at the centre could overshoot into the slow side. A 23% cut also reads better in patch notes than a 31% one (MMO303 week 14). If open-beta data puts the Hexer at 11 s with a tight interval, the job is done; if it lands at 10.3, a second smaller step follows.

This script reproduces every number above. It uses only the standard library, with t values copied from a t table.

```python
import math

T95 = {5: 2.571, 8: 2.306, 10: 2.228, 13: 2.160}   # two-sided 95%, df = players - 1
classes = [  # name, players, mean of per-player medians, SD across players, target band
    ("Warden", 9, 13.1, 2.4, (10.2, 13.8)),
    ("Hexer", 11, 8.9, 1.6, (10.2, 13.8)),
    ("Ranger", 14, 11.8, 2.0, (10.2, 13.8)),
    ("Mender", 6, 17.5, 3.9, (12.8, 19.2)),
]
for name, n, mean, sd, (lo_t, hi_t) in classes:
    half = T95[n - 1] * sd / math.sqrt(n)
    lo, hi = mean - half, mean + half
    if hi < lo_t:
        verdict = "too fast: act"
    elif lo > hi_t:
        verdict = "too slow: act"
    elif lo >= lo_t and hi <= hi_t:
        verdict = "inside band: leave"
    else:
        verdict = "can't decide"
    print(f"{name:7} n={n:2}  {lo:5.2f} to {hi:5.2f} s  band {lo_t}-{hi_t}  {verdict}")

half = 1.96 * 4.0 / math.sqrt(400)          # the trap: kills used as n
print(f"Warden, kills as n=400: {13.1 - half:.2f} to {13.1 + half:.2f} s")
print(f"Warden players needed: {math.ceil((1.96 * 2.4 / (13.8 - 13.1)) ** 2)}")

approach = 2.0
for target in (12.0, 11.0):
    scale = (8.9 - approach) / (target - approach)
    print(f"Hexer to {target} s: multiply damage by {scale:.3f} ({1 - scale:.1%} cut)")
```

It prints:

```
Warden  n= 9  11.26 to 14.94 s  band 10.2-13.8  can't decide
Hexer   n=11   7.83 to  9.97 s  band 10.2-13.8  too fast: act
Ranger  n=14  10.65 to 12.95 s  band 10.2-13.8  inside band: leave
Mender  n= 6  13.41 to 21.59 s  band 12.8-19.2  can't decide
Warden, kills as n=400: 12.71 to 13.49 s
Warden players needed: 46
Hexer to 12.0 s: multiply damage by 0.690 (31.0% cut)
Hexer to 11.0 s: multiply damage by 0.767 (23.3% cut)
```

### Move it yourself

Open the [MA102 week 13 sampling interactive](../../MA102-mathematics-for-games-ii-probability-and-statist/examples/w13-sampling-intervals.html) and set the sample size to 6, then 46. Watch how often an interval from six players misses the true value by more than a band's width. Then put your own class table into lab 6; the sheet recomputes every interval and verdict when you change `n`.

### Cross-game recognition

The same three-verdict comparison runs through every balance question in this program. MMO307 week 14 compares a spec's win rate against 50% with an interval and warns that rating systems absorb some of the gap. MMO304 week 12 compares gold income per player-hour against a planned faucet rate. PR201 week 11 compared tutorial completion against a threshold. In each case the steps are a per-unit metric, an interval, a band set in advance, and a verdict that is allowed to be "can't decide".

### Eyes-open design judgment

Intervals do not decide for you. A Mender band that is plus or minus 20% was a design choice; so was 15% for damage classes. Narrow bands produce more "act" verdicts and more churn. Wide bands let real problems through. Set the band from what players can feel. A two-second kill-time difference on a 12-second fight is noticeable in a group, a half-second one is not. Also watch the classes that no one picked. If only six testers played the Mender, that is itself a finding about the class's appeal or its onboarding, and no damage change fixes it.

### Check yourself

1. The Ranger's 14 players give an interval of 10.65 to 12.95 s. If the team tightens the band to plus or minus 10% (10.8 to 13.2 s), what is the new verdict, and what would you do about it?
2. After the 23% cut, open beta shows the Hexer at 11.4 s with `n = 40` and `s = 1.7`. Compute the interval with `t ≈ 2.02` and give the verdict.
3. A teammate reports "the Warden averages 13.1 s across 400 kills, interval 12.7 to 13.5, so leave it". Explain in two sentences what is wrong and what the correct interval is.

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: units, the three verdicts, sizing a change | — |
| 0:15-0:45 | Cleaning pass: run the filter script for internal accounts and builds; run the count checks | Cleaning log with before and after counts |
| 0:45-1:25 | Fill the balance review sheet (lab 6), one row per target in the PR401 balance document | Balance sheet with intervals and verdicts |
| 1:25-1:35 | Break | — |
| 1:35-2:05 | Size every "act" change with the formula, then run it through the combat simulator | Change log with predicted values |
| 2:05-2:35 | Pair review with another team: challenge one unit, one band, one change size | Challenge notes |
| 2:35-3:00 | Write the targeted-test list for open beta; instructor walk-round | Test list, sign-off |

## Deliverables

Due before the week 7 studio meeting, in `production/week06/` in the team repository.

1. **Cleaning log**: accounts removed, builds split, count checks with numbers. Checked by repeating one count from the raw export.
2. **Balance review sheet** (lab 6): every row has a unit, `n`, interval, band, the date the band was set, and a verdict. Checked by recomputing two rows.
3. **Balance change log**: for every "act" row, the lever, the old and new value, the formula or simulator run that predicts the new metric, and the predicted value. Checked by recomputing one prediction.
4. **Targeted-test list for open beta**: every "can't decide" row with the players needed, the instrumentation it requires and the owner. These become sprint 4 backlog items next week.

## Common failure modes

- **Counting events as observations.** Kills, hits and quest steps cluster inside players. Compute per player first.
- **Balancing against feel.** A change with no target and no predicted value cannot be checked, so it can never be wrong, and it can never be right.
- **Mixing builds.** A class average computed across a mid-beta patch describes neither build.
- **Leaving developers in the data.** One admin account with debug gear can move a class mean by several seconds.
- **Changing three levers at once.** Next review, nobody can say which change did what.
- **Treating "can't decide" as "leave".** It means the data is silent. Plan the test or say explicitly that you accept the risk.
- **Tuning the class nobody played.** Six Mender players is a pick-rate finding first. Ask why before you retune numbers.

## Review checklist

The instructor checks, at the week 7 meeting:

- [ ] The cleaning log shows internal accounts removed by ID and events split by build.
- [ ] Every balance row uses players (or parties, for group content) as `n`, and states it.
- [ ] Two recomputed intervals match the sheet to one decimal place.
- [ ] Every band is dated; bands set after the beta are marked as such.
- [ ] Every "act" row has a sized change with a predicted value, and at most one lever per class.
- [ ] Every "can't decide" row has a players-needed estimate and an owner in the open-beta test list.
- [ ] The cleaning is a script in the repository that will run on week 8 data unchanged.

## Sources

- Thompson, C. "Halo 3: How Microsoft Labs Invented a New Science of Play." *Wired*, issue 15.09 (September 2007), posted online 21 August 2007 (read via the Internet Archive copy of 17 March 2014). More than 3,000 hours of Halo 3 play from about 600 players analysed by Microsoft's user research team, with tracking of where players died.
- Seif El-Nasr, M., Drachen, A. and Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Background on game telemetry pipelines and metric design.
- Student [W. S. Gosset] (1908). "The probable error of a mean." *Biometrika* 6(1), 1-25. The t distribution used for small-sample intervals; t values in section 5 are standard table values.
- All class names, targets, bands and beta values in sections 4 and 5 are invented teaching values, not data from any real team.
