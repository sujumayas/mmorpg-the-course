# MMO308 · Week 12 — Economy Monitoring

**Why this matters:** Most economy problems in a live game don't arrive as a spike. They arrive as a leak: a duplication bug that a few players use quietly, a faucet that pays 3% too much after a patch, a bot farm that grows a little every day. A dashboard shows all of these, but only to someone who looks, and a threshold alarm set by eye either fires every weekend or never fires at all. This week you learn to build alarms that catch a slow leak in days, with a false-alarm rate you chose on purpose.

**You will be able to:**
- Build a same-weekday baseline for a daily economy series and turn each day into a standardized residual.
- Compute a CUSUM statistic by hand and in code, and predict its detection delay and false-alarm rate from its two parameters.
- Compare a spike rule, a CUSUM rule and a percentage-change rule on the same series, with numbers for false alarms per year and days to detection.
- Design the alarm layer for an economy dashboard: which series to watch, which rule suits each, and a false-alarm budget across all of them.

**Before class:** Raph Koster, "Economy Stats" (Star Wars Galaxies live server report, 30 April 2004, available from the Internet Archive). NIST/SEMATECH *e-Handbook of Statistical Methods*, section 6.3.2.3, "CUSUM Control Charts". Seif El-Nasr, Drachen & Canossa (eds.), *Game Analytics* (2013), chapter 29, "Data Collection in Massively Multiplayer Online Games" (Ducheneaut & Yee, pp. 641-664).

**Prerequisites from earlier courses:** [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (the ledger, reconciliation, price indices and the panel list this week puts alarms on). [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md). [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (compare a day with the same weekday). [MA102 week 8, the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) and [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positives, multiple comparisons). From this course, [week 6 on peeking](w06-ab-testing-statistics-and-pitfalls.md) (what repeated looks do to error rates) and [week 8 on event baselines](w08-event-design-and-calendars.md).

**Interactive:** [`examples/w12-faucet-alarm.html`](../examples/w12-faucet-alarm.html). Keep it open during section 2.

---

## 1. From dashboard to alarm

MMO304 week 12 gave you an economy dashboard: a ledger of every faucet and sink, a daily reconciliation, price indices, wealth distribution. A dashboard answers questions when someone asks them. **Monitoring** asks the questions for you, every day, and interrupts a person only when the answer is "something changed".

Every alarm has three parts.

1. **An expected value**, the baseline. What would today's number be if nothing unusual were happening?
2. **A scale**, the noise. How far does the number normally wander from the baseline?
3. **A rule**, the trigger. How far from the baseline, for how long, before a person gets paged?

And every alarm fails in two ways.

- A **false alarm** pages someone when nothing is wrong. One false alarm costs an hour. Many false alarms cost more, because people learn to ignore the alarm, and then they ignore the real one. This is **alert fatigue**.
- A **late detection** lets a real problem run. In an economy, each day of delay is another day of gold entering or leaving that shouldn't have, and MMO401 shows how the cost of cleaning it up grows with that delay.

The two failures trade against each other. A more sensitive rule catches leaks sooner and pages people more often for nothing. You can't escape the trade, but you can measure it and choose where to sit on it. The standard measure is the **average run length (ARL)**, the average number of days until the rule fires. You want a long ARL when nothing is wrong and a short ARL when something is.

## 2. Worked example: the leak no alarm caught

### The hook

In April 2004, Raph Koster published a live server report for Star Wars Galaxies players about the game's economy. He showed the daily flow of credits into the game and noted that it rose and fell with how many people were playing, which varied by day of the week. He also explained how the team had found a duplication bug. By his account, for a while the game had run at a deficit, with more credits leaving through sinks than entering through faucets. Yet players weren't running short of money. Nobody went broke. The team concluded that counterfeit credits were entering by a path they weren't logging, went looking, found the dupe, banned many of the players involved, and removed trillions of credits.

No alarm caught it. People did, by noticing over weeks that two numbers disagreed.

Compare Old School RuneScape on 12 July 2018. An update introduced a bug that turned stacks of items into 2,147,483,647 coins, the largest amount a stack can hold. Jagex took the game offline, fixed it, and rolled back to about the time of the update, so players lost what they had done since it went live (the OSRS Wiki puts the gap at about 20 minutes). That anomaly was enormous from the first minute. Any rule would have caught it.

Spikes are easy. Leaks are hard, because each day's excess is smaller than the ordinary Saturday bump. So how do you build an alarm that ignores Saturdays and still catches a leak worth a few percent a day?

### The model

Let `x_t` be a daily economy series, for example gold entering from mob loot, in millions.

**Baseline.** Players play more on weekends, so compare each day with the same weekday in recent clean weeks, as DB201 week 12 and week 8 of this course recommended:

```
b_t = average of x on the same weekday over the last 4 clean weeks
```

**Standardized residual.** Divide the gap by the normal day-to-day noise `σ`, measured on quiet weeks:

```
z_t = (x_t − b_t) / σ
```

When nothing is wrong, `z_t` behaves roughly like a draw from a standard normal curve (MA102 week 8): mean 0, and beyond 3 only about 0.13% of the time.

**Rule 1, the spike rule.** Alarm when `z_t > 3`. This is a Shewhart rule, the oldest kind of control chart. It looks at one day at a time.

**Rule 2, CUSUM.** Keep a running score `S_t` that adds up evidence of an upward shift and forgets it slowly:

```
S_0 = 0
S_t = max(0, S_(t−1) + z_t − k)
alarm when S_t > h
```

- `k` is the **allowance**. Each day, the score drops by `k` before today's evidence is added, so ordinary noise drains away. Set `k` to half the shift you want to catch, in units of `σ`. To catch a 1σ leak, `k = 0.5`.
- `h` is the **decision interval**, how much accumulated evidence you demand before paging. `h = 4` or `5` is a common starting point.
- The `max(0, …)` means good days can't bank credit against future bad days.

CUSUM stands for cumulative sum. E. S. Page proposed it in 1954 for factory inspection, and it is still the standard tool for catching small, sustained shifts.

### Numbers you can check

A server's mob-loot faucet has this weekly pattern, in millions of gold per day, with day-to-day noise `σ = 1.0` million:

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|
| 40 | 39 | 40 | 41 | 44 | 52 | 50 |

On day 4, a Thursday, a duplication bug starts adding 1.0 million gold a day. That is 1σ, about 2.3% of an average day, and smaller than any Friday-to-Saturday jump. Here are two weeks. The column "10% rule" is a common first attempt, "alarm when today is more than 10% above the average of the last 7 days", and it uses a clean previous week equal to the baseline.

| Day | Weekday | Baseline `b` | Observed `x` | 10% rule | `z` | Spike (`z > 3`) | CUSUM `S` (`k = 0.5`) | CUSUM alarm (`S > 5`) |
|---|---|---|---|---|---|---|---|---|
| 1 | Mon | 40 | 40.3 | — | 0.3 | — | 0.0 | — |
| 2 | Tue | 39 | 38.5 | — | −0.5 | — | 0.0 | — |
| 3 | Wed | 40 | 40.8 | — | 0.8 | — | 0.3 | — |
| 4 | Thu | 41 | 41.8 | — | 0.8 | — | 0.6 | — |
| 5 | Fri | 44 | 45.4 | — | 1.4 | — | 1.5 | — |
| 6 | Sat | 52 | 51.9 | fires | −0.1 | — | 0.9 | — |
| 7 | Sun | 50 | 51.6 | fires | 1.6 | — | 2.0 | — |
| 8 | Mon | 40 | 41.2 | — | 1.2 | — | 2.7 | — |
| 9 | Tue | 39 | 39.6 | — | 0.6 | — | 2.8 | — |
| 10 | Wed | 40 | 41.9 | — | 1.9 | — | 4.2 | — |
| 11 | Thu | 41 | 42.1 | — | 1.1 | — | 4.8 | — |
| 12 | Fri | 44 | 44.6 | — | 0.6 | — | 4.9 | — |
| 13 | Sat | 52 | 53.7 | fires | 1.7 | — | 6.1 | **fires** |
| 14 | Sun | 50 | 51.5 | fires | 1.5 | — | 7.1 | fires |

Check a few rows by hand. On day 5, `z = 45.4 − 44 = 1.4`, and `S = max(0, 0.6 + 1.4 − 0.5) = 1.5`. On day 6, `z = 51.9 − 52 = −0.1`, and `S = max(0, 1.5 − 0.1 − 0.5) = 0.9`. On day 13, `S = 4.9 + 1.7 − 0.5 = 6.1`, above 5.

Read the three alarm columns.

- **The 10% rule** fires on every Saturday and Sunday. It would have fired on those days with no leak at all, because weekends are always more than 10% above the weekly average. Within a month, the team mutes it. It never distinguishes the leak.
- **The spike rule** never fires. The largest `z` in two weeks is 1.9. A 1σ leak almost never produces a single day above 3σ.
- **CUSUM** fires on day 13, ten days after the leak began, when about 10 million gold has leaked. No single day looked unusual. The run of slightly-high days did.

That is Koster's story, turned into arithmetic. His team noticed the deficit that didn't bite. CUSUM notices the surplus that keeps coming.

### How often each rule is wrong

Two weeks is one example. Simulate thousands of them to get the average run lengths. The code below reproduces the table's alarm day and then simulates both rules.

```python
import random

BASE = [40, 39, 40, 41, 44, 52, 50]  # expected gold per weekday, Mon..Sun, millions
NOISE = [0.3, -0.5, 0.8, -0.2, 0.4, -1.1, 0.6, 0.2, -0.4, 0.9, 0.1, -0.4, 0.7, 0.5]
SIGMA, K, H = 1.0, 0.5, 5.0


def cusum_step(s, z, k=K):
    return max(0.0, s + z - k)


s = 0.0
for day, e in enumerate(NOISE, start=1):
    leak = 1.0 if day >= 4 else 0.0  # the dupe starts on day 4, a Thursday
    x = BASE[(day - 1) % 7] + e + leak
    z = (x - BASE[(day - 1) % 7]) / SIGMA
    s = cusum_step(s, z)
    if s > H:
        print(f"CUSUM alarm on day {day}: S = {s:.1f}")
        break


def run_length(rule, shift, rng, cap=20_000):
    """Days until the first alarm when z ~ Normal(shift, 1)."""
    s = 0.0
    for day in range(1, cap + 1):
        z = rng.gauss(shift, 1.0)
        if rule == "spike" and z > 3:
            return day
        if rule == "cusum":
            s = cusum_step(s, z)
            if s > H:
                return day
    return cap


rng = random.Random(12)
for rule in ("spike", "cusum"):
    quiet = sum(run_length(rule, 0.0, rng) for _ in range(4000)) / 4000
    leak = sum(run_length(rule, 1.0, rng) for _ in range(4000)) / 4000
    print(f"{rule:5s}: a false alarm every {quiet:.0f} days, a 1-sigma leak caught in {leak:.1f} days")
```

It prints:

```
CUSUM alarm on day 13: S = 6.1
spike: a false alarm every 740 days, a 1-sigma leak caught in 44.3 days
cusum: a false alarm every 931 days, a 1-sigma leak caught in 10.4 days
```

Put the results in one table. The spike figure for a quiet series is exact, `1 / 0.00135 ≈ 741` days. The others are simulated, and a different seed moves them by a few percent.

| Rule | Days between false alarms | Days to catch a sustained 1σ leak | Days to catch a sustained 3σ jump |
|---|---|---|---|
| Spike, `z > 3` | about 740 | about 44 | about 2 |
| CUSUM, `k = 0.5`, `h = 5` | about 930 | about 10 | about 3 |
| 10% above the 7-day average | fires every weekend | never distinguishes it | depends on the weekday |

CUSUM wins on both of the first two columns. It raises fewer false alarms *and* catches the leak four times sooner. It gives up about half a day on big jumps, which the spike rule catches a little faster. The NIST handbook states the general result. CUSUM charts detect shifts of about 2σ or less more efficiently than Shewhart charts. The practical answer is to run both, a spike rule for coin-pouch days and CUSUM for Star Wars Galaxies weeks.

### A visual you can move

Open `examples/w12-faucet-alarm.html`. The top chart is the faucet over 84 days, with the weekly bumps, a shaded band where the 10% rule would fire, and a marker where the leak begins. The bottom chart shows `z` as bars and the CUSUM score as a line, with the decision interval `h` as a horizontal rule. At the default settings the top chart looks the same before and after the leak. The bottom line climbs steadily. With the default noise (seed 12) it crosses `h` on day 35, seven days into the leak, faster than the lecture's table because these draws happen to run high. The spike rule fires once too, on day 47, where one ordinary high day sits on top of the leak. Drag the leak size down to 0.5σ and the crossing moves to day 54, 26 days in. Drag `k` up to 1.0 and the small leak vanishes from the score entirely. Turn on "spike on day 60" and both rules react to that day. Press "New noise" a few times to see how much the detection day varies from draw to draw. The readouts show the days to detection and the gold leaked by then.

### Cross-game and cross-context recognition

**Factory inspection (Page, 1954).** CUSUM was designed for production lines, where a machine drifts slightly out of adjustment and each part is only a little off. Checking one part at a time against a wide tolerance misses the drift, and accumulating the small deviations catches it. A duplication bug used by a few players is a machine drifting out of adjustment.

**Public health surveillance (CDC's EARS, 2003 onward).** The US Centers for Disease Control and Prevention built the Early Aberration Reporting System to spot unusual rises in counts such as emergency-room visits with particular symptoms, including for short events like large public gatherings where little history exists. EARS compares each day with a short recent baseline and offers three detectors, C1 to C3, of increasing sensitivity. The most sensitive adds up evidence over several days, as CUSUM does. A health department faces your exact trade. It has to page investigators early enough to matter without training them to ignore the pager.

**Old School RuneScape, 12 July 2018.** The coin-pouch bug is the spike case. Stacks worth billions appeared at once, many thousands of `σ` above any baseline, and the game was taken offline the same day. A spike rule is enough for this class of incident, and it is the cheapest rule to run.

**Star Wars Galaxies, early 2000s.** The drift case, found by people noticing that a deficit had no consequences. With a daily reconciliation residual (MMO304 week 12) as the series and CUSUM as the rule, the same discovery becomes a page within about two weeks of the leak starting, instead of whenever someone happens to compare two charts.

Four settings, one question. *Is today's evidence, added to recent days' evidence, more than normal noise can explain?*

### Eyes-open design judgment

- **Choose `k` from the smallest leak worth catching.** Decide what a leak costs per day and what size you can afford to miss. If a 0.5σ leak matters, `k = 0.25`, and you will get more false alarms at the same `h`. If only 2σ leaks matter, `k = 1.0`, and small leaks become invisible by design. Write the choice down.
- **Choose `h` from your false-alarm budget,** not by feel. Section 5 does this across many series.
- **Freeze the baseline when you investigate.** A same-weekday baseline over four weeks will slowly learn the leak. After four weeks of a 1 million gold leak, the leak *is* the baseline, and `z` returns to zero. CUSUM has to win that race, which is one reason to catch leaks in days rather than weeks.
- **Reset after an explained alarm.** When an alarm fires and the cause is known and fixed, reset `S` to zero. If the cause was a planned change you forgot to annotate, fix the baseline instead (section 4).
- **Watch the direction.** The formula above catches rises. A sink that silently stops charging is a fall in the sink series, so run the mirror score, `max(0, S − z − k)`, on it.

### Check yourself (worked example)

1. With `k = 0.5` and `h = 5`, a series shows `z = 2.0, 2.0, 2.0, 2.0` from a starting score of 0. On which day does CUSUM fire?
2. In the table, suppose day 12's noise had been −1.4 instead of −0.4. Recompute `S` for days 12 and 13. Does the alarm still fire on day 13?
3. A leak adds 0.5σ a day. Roughly how many days would CUSUM with `k = 0.5` need, and why is `k = 0.5` a poor choice for this leak?

<details>
<summary>Answers</summary>

1. `S` goes 1.5, 3.0, 4.5, 6.0. It fires on day 4.
2. Day 12: `x = 44 − 1.4 + 1 = 43.6`, `z = −0.4`, `S = max(0, 4.8 − 0.4 − 0.5) = 3.9`. Day 13: `S = 3.9 + 1.7 − 0.5 = 5.1`, still above 5. It fires on day 13 again, just barely.
3. With `k = 0.5`, a 0.5σ leak adds `0.5 − 0.5 = 0` to the score on average, so only noise pushes `S` upward. Detection takes weeks (about 38 days in simulation). Setting `k = 0.25` restores a positive drift of 0.25σ per day.

</details>

## 3. What to watch

MMO304 week 12 listed the panels of an economy dashboard. Monitoring puts a rule on each, and the right rule depends on how that series usually goes wrong.

| Series | Typical failure | Rule | Direction |
|---|---|---|---|
| Reconciliation residual (snapshot supply minus ledger-predicted supply) | Untagged faucet or dupe, often small and steady | CUSUM plus spike | Both |
| Gold per faucet source, per day | Bot farm growth, a patch that pays too much | CUSUM on the per-source series | Up |
| Gold per sink source, per day | A sink that stopped charging after a patch | Mirror CUSUM | Down |
| Active supply per active player (MMO304) | Inflation drifting past the target band | CUSUM on the weekly change | Up |
| Price index for a basket (MMO304) | A shortage, a corner, a dupe of a traded item | Spike on the weekly change | Both |
| Top 1% share of a faucet source | Bots concentrating a faucet | Spike plus CUSUM | Up |
| Count of a high-value item in existence | Item dupe (doesn't move gold at all) | Spike | Up |

Two notes on this table. First, the reconciliation residual is the best single series to watch. It should be zero every day, so its baseline is known exactly, and anything steady and positive is gold nobody logged. Second, **item dupes need their own series**. A duplicated rare item leaves the gold ledger untouched until someone sells it. Count copies of every item above a value threshold, daily, and alarm on the count.

## 4. Baselines that know the calendar

A baseline that ignores the calendar raises false alarms on every planned change. Four fixes cover most of them.

- **Planned events.** A double-gold weekend (week 8) raises the faucet on purpose. Before the event, write down the expected change, for example "mob-loot faucet × 1.8 on event days", and multiply the baseline by it. Now the alarm watches the *difference from plan*. If the event pays 2.4 times instead of 1.8, that is worth a page.
- **Patches.** A patch that changes a reward table is a planned step. Note the expected step in the patch spec (week 9), move the baseline by that amount on release day, and drop the old weeks from the baseline window once four clean weeks exist at the new level.
- **Player counts.** When a new expansion doubles daily players, every faucet doubles and every CUSUM fires. Watch gold per active player instead of total gold for faucets that scale with play. DB201 week 12 and MMO304 week 12 both warned that the denominator is a choice. Here the choice decides whether your alarm pages the whole team on launch day.
- **Robust noise.** If a past incident sits inside the weeks you use to measure `σ`, it inflates `σ` and deafens the alarm. Estimate `σ` from the median absolute deviation instead of the standard deviation. For normal data, `σ ≈ 1.4826 × MAD`, and one bad day barely moves it.

## 5. From alarm to action

### A false-alarm budget

An economy team doesn't watch one series. Suppose it runs CUSUM on 40 series: faucets and sinks by source, per currency, plus the reconciliation residual. Each series has an in-control ARL of about 930 days at `h = 5`. Together they produce about `40 × 365 / 930 ≈ 16` false alarms a year, more than one a month. That is MA102 week 14's multiple-comparisons problem again, and this course's week 6 peeking problem in another form. Every daily check is a look.

Raise `h` to 6 and the in-control ARL rises to about 2,500 days in simulation, which is about 6 false alarms a year across 40 series. The price is detection speed. A 1σ leak now takes about 12 days instead of 10. Choose the budget first ("no more than six false pages a year"), then set `h` to meet it, then tell the team what detection delay they bought.

Use tiers. The reconciliation residual and item-count spikes page someone immediately, because a dupe is a SEV1 incident even when the servers are healthy (week 13). Per-source faucet drifts open a ticket for the economy designer to review next working day. Price and distribution alarms go into a weekly review. Not every alarm deserves to wake someone up.

### Every alarm is a labelled example

When an alarm fires, record what it turned out to be: a real leak, a planned change nobody annotated, a data pipeline fault, or noise. After three months you have the **precision** of each rule, the share of its alarms that were real. A rule with low precision needs a higher `h` or a better baseline. A rule that never fired may be tuned too loosely to catch anything. Either way, you are now tuning with evidence, which is the point of the whole exercise.

### The first ten minutes

An economy alarm needs a runbook, a short list of first steps that anyone on call can follow. Week 13 covers incident response in general. For economy alarms, the first steps are usually these.

1. Confirm the data. Is the pipeline healthy, and does the raw ledger show the same thing as the dashboard?
2. Locate it. Which server, currency, source and accounts carry the excess?
3. Decide whether to stop the spread. If the residual is growing and concentrated in a few accounts, restricting trade for those accounts, or for everyone, limits how far the gold moves. MMO401 week 12 models the choice between rollback, clawback and freezing.
4. Page the owner named on the alarm.

## In-class activity (25 minutes)

Pairs. You get a printed 28-day series for a crafting-sink source (gold removed per day, in millions), its weekday baseline, and `σ = 0.8` million. The sink stops charging a fee on some items after a patch on day 15, so the series drops a little.

1. Compute `z` for days 15 to 28.
2. Run the mirror CUSUM, `S_t = max(0, S_(t−1) − z_t − k)`, with `k = 0.5` and `h = 4`. On which day does it fire?
3. Would a spike rule at `z < −3` have fired? Would "alarm if today is 10% below the 7-day average"?
4. Your team watches 25 series with the same rule. Estimate the false alarms per year, taking the in-control ARL at `h = 4` as about 340 days. Propose a change to meet a budget of 12 false pages a year, and say what it costs.

Expected output: the `z` column, the CUSUM column with the alarm day circled, answers to step 3, and a one-line recommendation for step 4.

## Common misconceptions

- **"If no single day looks unusual, nothing is wrong."** A 1σ leak almost never produces a 3σ day. It produces a run of slightly high days, which only an accumulating rule sees.
- **"A percentage-change alarm is simple and safe."** On a series with a weekly cycle, it fires on the cycle. Compare with the same weekday, or it will be muted within a month.
- **"More sensitive alarms are safer."** Across many series, they produce enough false pages that people stop answering them. Set a false-alarm budget and tune to it.
- **"The baseline should always use the most recent weeks."** A baseline that includes a leak learns the leak. Freeze it during investigations and drop weeks known to contain incidents.

## Check yourself

1. A faucet's Saturday baseline is 52 million and `σ = 1.2` million. Saturday's value is 55.0 million. What is `z`? Does the spike rule fire?
2. A CUSUM with `k = 0.5`, `h = 5` has `S = 3.2`. The next three days have `z = 0.4, 1.9, 1.3`. On which day, if any, does it fire?
3. An economy team runs spike rules at `z > 3` on 60 daily series. How many false alarms should it expect per year? What would you change first?
4. A double-gold event is planned for a weekend. The faucet usually runs at 52 on Saturdays. During the event, Saturday reads 98 with `σ = 1.0`. The plan said "× 1.8". Should the alarm fire? Show the baseline you would use.
5. Explain why a one-person dupe of a rare item might never show up in any gold series for weeks, and name the series that would catch it.

<details>
<summary>Answers</summary>

1. `z = (55.0 − 52) / 1.2 = 2.5`. The spike rule doesn't fire.
2. `S` goes `3.2 + 0.4 − 0.5 = 3.1`, then `3.1 + 1.9 − 0.5 = 4.5`, then `4.5 + 1.3 − 0.5 = 5.3`. It fires on the third day.
3. Each series raises a false alarm every 741 days on average, so 60 series raise about `60 × 365 / 741 ≈ 30` a year. First, sort the series into tiers so most of them open tickets rather than page someone, and move the drift-prone ones to CUSUM with a higher `h`.
4. The planned baseline is `52 × 1.8 = 93.6`. `z = (98 − 93.6) / 1.0 = 4.4`, so yes. The event is paying more than planned, which is worth a page even though everyone knew the faucet would be high.
5. Duplicated items don't create gold until someone sells them to an NPC or another player, and a trade between players moves gold without creating any. The count of copies of that item in existence is the series that catches it.

</details>

## Lab / assignment hook

[Lab 12, faucet alarms](../labs/lab12.md). You get 168 days of faucet and sink data for a fictional server, with a planned event, a patch and some incidents hidden in it. You build weekday baselines and robust `σ`, implement the spike and CUSUM rules, tune them to a false-alarm budget, find the incidents, and write the alarm specification for the team. This lab counts toward the analytics labs (40%).

## Sources

- Koster, R. (2004, 30 April). "Economy Stats." Star Wars Galaxies live server report, read by the author from the Internet Archive copy of simbaspaws.org, September 2026; a re-check in the September 2026 fact sweep failed because the Internet Archive was offline, so the lecture reports it as Koster's account. Faucet inflow varying by day of the week; a period of deficit with no shortage of money; the dupe found, many players banned and trillions of credits removed; monitoring of large individual wealth changes.
- Jagex, "Old School RuneScape Status Update" (Old School RuneScape news, 12 July 2018, read September 2026). Game offline after the weekly update; stacks of other items converted to 2.1b coins by faulty coin-pouch death logic; rollback to the approximate time of the update (11.30am BST); back online at the 18:11 update. https://secure.runescape.com/m=news/old-school-runescape-status-update?oldschool=1
- Old School RuneScape Wiki, "Coin pouch glitch" (accessed September 2026). Stacks became 2,147,483,647 coins; servers taken offline about 20 minutes after the update went live.
- Page, E. S. (1954). "Continuous Inspection Schemes." *Biometrika* 41(1-2), 100-115. doi:10.1093/biomet/41.1-2.100.
- NIST/SEMATECH *e-Handbook of Statistical Methods*, section 6.3.2.3, "CUSUM Control Charts" (accessed September 2026). CUSUM more efficient than Shewhart charts for shifts of about 2σ or less.
- Hutwagner, L., Thompson, W., Seeman, G. M. & Treadwell, T. (2003). "The bioterrorism preparedness and response Early Aberration Reporting System (EARS)." *Journal of Urban Health* 80(Suppl. 1), i89-i96. doi:10.1007/PL00022319. Method summary (C1, C2, C3 of increasing sensitivity, for short baselines) from a 2025 comparison study on PubMed Central (PMC12641150).
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Chapter 29, Ducheneaut, N. & Yee, N., "Data Collection in Massively Multiplayer Online Games: Methods, Analytic Obstacles, and Case Studies", pp. 641-664.
- Run lengths in section 2 and section 5 are this course's simulations with the code shown (Python 3.13, seed 12 for the table). The spike-rule false-alarm interval of 741 days follows from the normal tail probability of 0.00135 above 3σ.

## Interactive spec: examples/w12-faucet-alarm.html

**Insight the visual must make obvious:** a slow leak is invisible in the raw series and to a one-day threshold, because the weekly cycle is bigger than the leak. Accumulating the standardized residuals (CUSUM) makes it climb out of the noise within one to two weeks (seven days at seed 12, ten in the lecture's fixed table).

**Data.** Generate 84 days (12 weeks) in the page with a seeded mulberry32 generator (seed 12), the same generator the MA102 interactives use. `x_t = BASE[(t−1) mod 7] + σ × n_t + leak_t + spike_t`, where `BASE = [40, 39, 40, 41, 44, 52, 50]` (Mon to Sun, millions), `n_t` is a standard normal draw (Box-Muller from the generator), `leak_t = L × σ` for `t ≥ t_leak` and 0 before, and `spike_t = 8 × σ` on day 60 only when the spike toggle is on. The baseline is the true `BASE` value for the weekday (explain this in a note: "baseline assumed known; the lab estimates it").

**Layout.** Two stacked charts sharing a day axis, full width on all screens.

- **Top, "Gold from mob loot".** Line of `x_t`. Dashed line of the baseline. Shade the days where the 10% rule fires (`x_t > 1.10 × mean of x over the previous 7 days`, using `BASE` for days before day 1). Vertical marker at `t_leak` labelled "leak starts". Vertical marker at the first CUSUM alarm.
- **Bottom, "Evidence".** Bars of `z_t = (x_t − b_t) / σ`, with a horizontal line at 3 (spike threshold). Line of `S_t = max(0, S_(t−1) + z_t − k)` on the same axis, with a horizontal line at `h`. Mark the first day `S_t > h` and the first day `z_t > 3`.
- **Readouts.** First alarm day for each rule (CUSUM, spike, 10% rule after `t_leak`), days from leak start to CUSUM alarm, gold leaked by then (`L × σ × days`), and the count of 10% rule firings before the leak began.

**Controls.**
- Leak size `L` in units of `σ`: slider 0 to 3, step 0.25, default 1.0.
- Leak start `t_leak`: slider 8 to 70, step 1, default 29 (a Monday in week 5).
- `k`: slider 0 to 1.5, step 0.05, default 0.5.
- `h`: slider 1 to 10, step 0.5, default 5.
- Toggle "spike on day 60", default off.
- Button "New noise" re-seeds (seed + 1). Button "Reset" restores seed 12 and all defaults.

**Test values (use to check the build).** With the seeded noise, the exact alarm day depends on the draws, so the spec's hand check uses the lecture's fixed table instead. Provide a hidden "lecture table" mode (a checkbox "Use the lecture's 14 days") that replaces days 1 to 14 with the lecture's `NOISE = [0.3, −0.5, 0.8, −0.2, 0.4, −1.1, 0.6, 0.2, −0.4, 0.9, 0.1, −0.4, 0.7, 0.5]`, `t_leak = 4`, `L = 1`, `k = 0.5`, `h = 5`, and shows 14 days only. In that mode:
- `S` for days 1 to 14: 0.0, 0.0, 0.3, 0.6, 1.5, 0.9, 2.0, 2.7, 2.8, 4.2, 4.8, 4.9, 6.1, 7.1.
- CUSUM alarm on day 13. Spike rule never fires. The 10% rule fires on days 6, 7, 13 and 14.
- With `k = 1.0`, `S` never exceeds 5 in the 14 days.

**Behaviour.** Every control redraws both charts immediately. Hovering or focusing a day shows `x`, `b`, `z` and `S` for that day. No animation beyond a short transition, disabled under `prefers-reduced-motion`.

**Accessibility.** Controls keyboard operable with visible focus. Readouts in an `aria-live` region. Alarm markers use shape and label as well as colour.
