# MMO308 · Week 08 — Event Design and Calendars

**Why this matters:** Live events make the tallest spikes on any engagement chart, and they are the easiest numbers in live ops to overclaim. Players who know an event is coming move their play into it, so part of every spike is borrowed from the days around it. This week you learn to measure what an event added rather than what it moved, and to lay out a calendar where events do not eat each other.

**You will be able to:**
- Compute an event's gross lift, borrowed play and net lift against a baseline, and its incrementality ratio.
- Explain how a baseline taken from the days just before an announced event overstates its lift, and compute by how much.
- Use a recovery model to compare event spacings by lift per event and total lift per year.
- Design a 12-week event calendar with stated goals, target segments and non-overlap rules, and critique one for fatigue and fairness.

**Before class:** Seif El-Nasr, Drachen & Canossa (eds.), *Game Analytics* (2013), the introductory chapters on metrics for live games (review the definitions of engagement metrics). RuneScape Wiki, "Double XP" and its guide page (about 15 minutes; look at the announcement and start dates in the events table). Reread your DB201 week 12 notes on DAU and player-hours.

**Prerequisites from earlier courses:** [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (engagement KPIs and their definitions). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (choosing a median over a mean). [MMO304 week 3, faucets and sinks](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (event rewards are faucets). [UX201 week 5, reinforcement schedules and ethics](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md) (time pressure and fear of missing out). From this course, [week 7, segmentation](w07-segmentation.md) and [week 13, incident response](w13-incident-response.md), whose baseline-and-rebound measurement is the mirror image of this week's.

**Interactive:** [w08-event-pull-forward.html](../examples/w08-event-pull-forward.html). Keep it open during section 2.

---

## 1. What a live event is

A **live event** is a time-limited change to a game's rules or content, announced to players, that ends on a date. Events come in a few families:

- **Modifier events** change a rate: double experience, extra drops, reduced costs. They need almost no new content, so they are cheap to run.
- **Content events** add something to do for a while: a seasonal quest line, a festival zone, a limited cosmetic.
- **Competitive events** add a ranking: a tournament, a race to a milestone, a temporary league with fresh characters.
- **Social events** give many players a shared moment: a world boss, a server-wide goal.

Every event has four parts you design on purpose: the **announcement** (when players learn about it), the **window** (when it runs), the **reward** (what players get, which is often a faucet in the economy, as MMO304 week 3 showed) and the **recurrence** (whether and when it comes back).

To judge an event you need three more terms.

- The **baseline** `B_t` is what a metric would have been on day `t` without the event. You never observe it. You estimate it.
- The **lift** on day `t` is the observed value minus the baseline, `A_t − B_t`. It can be negative.
- The **counterfactual** is the whole imagined world without the event. The baseline is your model of it, and every lift figure is only as good as that model.

The metric in this lecture is **player-hours per day**, the total time all players spent in the game. It suits events better than DAU does, because an event can make people play longer without changing whether they log in. Everything below works the same for DAU, XP gained or purchases.

## 2. Worked example: the Double XP spike that was mostly borrowed

### The hook

RuneScape has run double-experience events since the first Bonus XP Weekend on 12 March 2010. In 2024 and 2025 they ran four times a year, ten days each, and Jagex announced each one ahead of time. The November 2025 event was announced on 7 November and started on 14 November. The May 2025 event was announced on 25 April and started on 16 May.

Now read the RuneScape Wiki's Double XP guide as a player would. It says that after an event is announced, players often prepare their accounts. The list includes making money to buy supplies, stocking up on skilling resources from the Grand Exchange, pre-planting farming patches and saving Slayer points. It points out that for skills trained by buying materials, double XP halves both the time and the cost of a level.

Put yourself in that player's shoes. If a level costs half as much next week, you stop buying it this week. After the event you have just gained a pile of levels, so you have less left to do for a while. The event's spike on the engagement chart is real. But some of it is play that would have happened anyway, on other days, and was moved into the window. How much of the spike did the event add?

The numbers below are invented. Jagex has not published daily player-hours around its events, and nothing here depends on the real values.

### The model

Take a window that starts when the event is announced and ends when play has returned to normal after it. Split it into three phases: pre (announcement to start), event, and post. Then:

```
net lift  = Σ over the whole window of (A_t − B_t)
gross lift = Σ over event days of (A_t − B_t)
borrowed   = Σ over pre and post days of (B_t − A_t)
net lift   = gross lift − borrowed
incrementality ratio = net lift / gross lift
```

- `A_t` is the observed metric on day `t`.
- `B_t` is the baseline for day `t`, estimated from days the event could not have touched.
- **Gross lift** is what the dashboard shows during the event.
- **Borrowed** play is the dip before the event (players waiting) and after it (players who already did what they came for).
- The **incrementality ratio** says what fraction of the spike was new play. A ratio of 1 means nothing was borrowed. A ratio of 0 means the event only moved play around.

For hand calculation, use flat phases: baseline `B` per day, a pre-dip of `d_pre` for `a` days, a lift of `L` for `E` days, and a post-dip of `d_post` for `h` days. Then:

```
gross    = B × L × E
borrowed = B × (d_pre × a + d_post × h)
net      = B × (L × E − d_pre × a − d_post × h)
```

### Numbers you can check

A game averages `B = 10,000` player-hours per day. It announces a ten-day double-XP event 14 days ahead.

| Phase | Days | Change vs baseline | Player-hours per day | Total vs baseline |
|---|---|---|---|---|
| Pre (announced, waiting) | 14 | −10% | 9,000 | −14,000 |
| Event | 10 | +60% | 16,000 | +60,000 |
| Post (hangover) | 14 | −15% | 8,500 | −21,000 |
| **Window** | 38 | | | **+25,000** |

The event dashboard reports a 60% lift and 60,000 extra player-hours. Borrowed play is `14,000 + 21,000 = 35,000`. Net lift is 25,000 player-hours. The incrementality ratio is `25,000 / 60,000 = 0.42`. Fewer than half of the hours on the spike were new.

Now make the mistake almost every first event report makes. The analyst needs a baseline and takes "the week before the event", a natural choice. That week is inside the pre-dip, so it averages 9,000, not 10,000. Against that baseline, each event day looks like `16,000 − 9,000 = 7,000` extra, and the event looks like it added 70,000 hours. The report now says the event added nearly three times what it really did, and the next event gets budgeted on that number.

The same calculation in code, which runs as shown:

```python
B = 10_000                      # baseline player-hours per day
pre, event, post = 14, 10, 14   # days in each window
dip_pre, lift, dip_post = 0.10, 0.60, 0.15

actual = ([B * (1 - dip_pre)] * pre
          + [B * (1 + lift)] * event
          + [B * (1 - dip_post)] * post)
phase = ["pre"] * pre + ["event"] * event + ["post"] * post

gross = sum(a - B for a, p in zip(actual, phase) if p == "event")
borrowed = sum(B - a for a, p in zip(actual, phase) if p != "event")
net = sum(a - B for a in actual)
print(f"gross {gross:,.0f}  borrowed {borrowed:,.0f}  net {net:,.0f}  ratio {net / gross:.2f}")

naive_base = sum(actual[pre - 7:pre]) / 7   # the week just before the event
naive_gross = sum(a - naive_base for a, p in zip(actual, phase) if p == "event")
print(f"baseline from the week before: {naive_base:,.0f} per day, gross {naive_gross:,.0f}")
```

Output:

```
gross 60,000  borrowed 35,000  net 25,000  ratio 0.42
baseline from the week before: 9,000 per day, gross 70,000
```

### The visual

Open `examples/w08-event-pull-forward.html`. The top chart is the daily metric with the baseline as a dashed line: a shallow trough, a tall spike, another trough. Areas above the baseline are shaded in one color and areas below in another. The bottom chart is the **cumulative lift**, the running total of `A_t − B_t` from the announcement day.

Watch the bottom chart. It slopes down through the pre-dip, climbs steeply during the event, then slopes down again through the hangover and settles at the net lift. The height of the climb, from the bottom of the pre-dip trough to the peak, is the gross lift, 60,000. The peak itself reads 46,000, because the running total already lost 14,000 to the pre-dip. Where it settles is what the event really added. Drag the post-dip slider up to about 33% and the cumulative line ends at zero: a spike of +60% that added nothing. Push it to 43% and the event ends 14,200 hours in the red. Then switch the baseline to "week before event" and watch the dashed line drop and the reported lift grow.

### Cross-game recognition

**Steam discounts (Steamworks rules, current since 1 January 2023).** Valve's rules say a product cannot be discounted within 30 days of another discount (the gap was 28 days before 2023), with exceptions for the big seasonal sales. A sale is a modifier event on price, and buyers who know sales come round can wait for them. That waiting is the pre-dip, and the quiet weeks after a sale are the hangover, in sales instead of hours. Valve states the purpose of its rules as pricing transparency. Read through this lecture's model, a 30-day gap also caps how often a waiting buyer gets rewarded, which limits the pre-dip. Write it in our form: gross is sale-week revenue above baseline, borrowed is the lost full-price sales around it.

**World of Warcraft's Darkmoon Faire (retail, 2026).** The Faire opens on the Sunday of the first full week of each month and lasts one week. Its profession quests give profession skill points and can be done only once per monthly Faire. That is an event with no net lift on its own quest content by design. The skill points are rationed to one batch a month, so their timing moves entirely into Faire week. Players who want them plan around the calendar, and the Faire's value to the game is a predictable monthly reason to log in, not extra hours. When you measure a recurring event like this, the baseline must come from a month's cycle, not from the week before.

**Outages, the negative event (MMO308 week 13).** An outage is an unannounced event with a negative lift. In week 13 you measured its cost against a same-hour-last-week baseline and subtracted the **rebound**, the players who came back afterwards and played the hours they had missed. That is the same accounting with the signs flipped: gross loss minus the rebound gives the net loss. An announced event borrows play from the days around it. An outage pushes play into the days after it. In both cases the net is the area under the whole window, not the peak.

Three contexts, one model. The spike is not the effect. Sum the difference from baseline over a window wide enough to catch the play that moved.

### Eyes-open design judgment

- **Borrowing is not always bad.** An event with a ratio of 0.4 may still be worth running. Concentrated play makes a world feel full, fills groups faster and gives lapsed players a date to come back. Decide which of those you want, and measure that (for example, reactivations in the lapsed segment from week 7) instead of claiming hours you did not add.
- **Announcement lead time is a lever.** A long lead gives players time to plan and deepens the pre-dip. A short lead limits the pre-dip but helps only players who happen to be around. RuneScape's recent leads ranged from about one to four weeks.
- **Rationing per player limits borrowing.** RuneScape's first Bonus XP Weekend in 2010 gave 2.7× experience that decayed with time logged in, down to 1.1× after 7 hours. In 2020, double XP became a personal allowance of 48 hours spread over a 10-day event, with a pause button. A cap per player limits how much of a player's future play can be moved into the window, and it keeps players with more free time from taking all the benefit.
- **Every event reward is a faucet.** Extra XP, drops or currency during an event enter the economy all at once. Check the event against the economy dashboard from MMO304 before you ship it, not after.

## 3. Building a baseline you can defend

The whole analysis rests on `B_t`, and you cannot observe it. Four ways to estimate it, from weakest to strongest:

1. **The days just before the event.** Contaminated by the pre-dip when the event was announced, as section 2 showed. Only acceptable for a surprise event.
2. **The same weekdays in clean weeks before the announcement.** Take the median of the last three or four Mondays, Tuesdays and so on, skipping weeks with other events, patches or outages. Use the median rather than the mean for the reason MA102 week 12 gave: one odd day should not move the baseline. This is the same idea as week 13's same-hour-last-week baseline, stretched to a longer window.
3. **Clean weeks plus trend.** If the game is growing or shrinking, a flat baseline will credit the event with the trend. Fit a straight line through the clean weeks and extend it.
4. **A holdout.** Run the event on some servers or regions and not others, and use the others as the baseline. This is the only method that gives a true counterfactual. In a shared world it is often impossible or unfair, for the reasons MA102 week 14 listed for A/B tests in MMOs: players compare notes and trade across the boundary.

Two rules apply whatever you choose. **Fix the baseline method before the event,** in the event brief, so nobody tunes it afterwards to flatter the result. And **extend the measurement window until the cumulative lift stops moving,** because a hangover that you stop measuring on day 3 is a hangover you did not subtract.

## 4. Calendars: spacing, overlap and segments

A **live-ops calendar** is the schedule of every event, patch and sale for the next quarter or year. Planning it is where most of the design work happens, because events interact.

### Layers of cadence

Most MMOs stack rhythms of different lengths.

| Cadence | Example | What it gives players |
|---|---|---|
| Daily | daily quests, login rewards | a reason to log in today |
| Weekly | weekly resets, rotating bonus events | a short-term plan |
| Monthly | WoW's Darkmoon Faire | a fixed date to return |
| Seasonal | holiday festivals, RuneScape's double XP | a peak to look forward to |
| Rotating | WoW Timewalking (added in patch 6.2.0, 2015), old expansion content on a cycle | variety without new content |

The layers should not all peak at once. Put the seasonal peak on a week without a monthly event, so each has room to be measured and so players are not asked to do everything in the same seven days.

### Spacing and fatigue

An event feels special partly because it is rare. Model that with a **recovery curve**: the lift an event can achieve depends on the gap `g` in days since the last event of its kind.

```
L(g) = L_max × (1 − e^(−g / τ))
```

- `L_max` is the lift a fully fresh event achieves.
- `τ` (tau) is the recovery time in days. After `τ` days, players have recovered 63% of their appetite. After `3τ`, 95%.

These two parameters are not constants of nature. You estimate them from your own past events by plotting each event's lift against the gap before it. Take `L_max = 60%` and `τ = 30` days, with ten-day events, a baseline of 10,000 player-hours per day, and no other events.

| Gap `g` (days) | Events per year | Lift per event `L(g)` | Gross lift-days per year | Relative cost per lift-day |
|---|---|---|---|---|
| 30 | 12.2 | 37.9% | 46.1 | 1.55 |
| 45 | 8.1 | 46.6% | 37.8 | 1.26 |
| 60 | 6.1 | 51.9% | 31.6 | 1.14 |
| 90 | 4.1 | 57.0% | 23.1 | 1.03 |
| 120 | 3.0 | 58.9% | 17.9 | 1.00 |

"Gross lift-days per year" is events per year × lift per event × 10 days. Multiply by 10,000 to get gross player-hours. The last column is the production cost per unit of lift if every event costs the same to make, relative to the 120-day spacing: `L(120) / L(g)`.

Read the table both ways. Monthly events buy the most total lift, about twice the quarterly total (46.1 against 23.1 lift-days). Each one buys less, so every unit of lift costs 1.55 times as much to make, against 1.03 for quarterly events. And this table only shows gross lift. More frequent events are easier to predict, which gives players more reason to wait, so the pre-dip grows too. Your choice of spacing is a choice about budget and about what the event should feel like, and the model lets you put numbers on both.

### Overlap and segments

Use week 7's segments to decide which events may overlap.

- **Events aimed at the same segment compete.** Two events for veterans in the same week split their time, and each one's measured lift shrinks. Worse, you cannot tell which event earned what.
- **Events aimed at different segments can stack.** A new-player welcome event and an endgame raid race in the same week draw on different people.
- **Write each event's goal as a metric and a segment.** "Raise D7 retention of players created during the event by 3 points" can be measured. "Boost engagement" cannot.

### Fairness and pressure

Events create time pressure on purpose. UX201 week 5 covered where that becomes manipulation. On a calendar, two checks help. Can a player with five hours a week get the core reward? And does missing an event lock a player out of something permanent? RuneScape's move to a personal 48-hour double-XP allowance with a pause button is one studio's answer to the first question. For the second, many studios bring limited rewards back on a later rotation.

## In-class activity (25 minutes)

In groups of three, plan a 12-week calendar for a mid-size MMO with three segments from week 7: new (under 7 days), established, and lapsed (absent 30 days or more).

1. Place exactly four events: one modifier event, one content event, one competitive event and one reactivation event. For each, write a goal as "metric, segment, target".
2. Use the recovery model with `L_max = 60%` and `τ = 30` to compute each event's expected gross lift, assuming the previous event of the same kind ended 90 days before week 1.
3. Pick a pre-dip and post-dip for the modifier event from section 2's example, and compute its expected net lift and incrementality ratio.
4. Swap calendars with another group. Find one overlap that makes an event impossible to measure, and one player who would be unfairly shut out.

Expected output: a one-page calendar table (week, event, segment, goal, expected gross and net lift), and the other group's two critiques.

## Common misconceptions

- **"The event's lift is the height of the spike."** The spike is gross lift. Net lift subtracts the play that moved into the window from the days around it.
- **"Use the week before as the baseline."** For an announced event that week is already depressed by players waiting, so the event looks bigger than it was.
- **"More events means more engagement."** More events means more gross lift at a higher cost per unit, and a deeper pre-dip as players learn the pattern.
- **"An event with a low incrementality ratio failed."** It failed only if its goal was extra hours. Many events exist to concentrate play, reactivate a segment or give the community a shared date.

## Check yourself

1. A game with `B = 20,000` player-hours per day runs a 7-day event at +50%. It announced it 7 days ahead, and players dipped 5% while waiting. After the event, players dip 10% for 10 days. Compute gross lift, borrowed play, net lift and the incrementality ratio.
2. For the event in question 1, an analyst uses the 7 days before the event as the baseline. What gross lift does the report show, and by what percent does it overstate the true gross?
3. With the recovery model `L_max = 50%`, `τ = 20` days and 5-day events, compare an event every 20 days with an event every 40 days: lift per event, gross lift-days per year, and the relative cost per lift-day.
4. A reactivation event has an incrementality ratio near zero for total player-hours. Name one metric and segment under which it might still be a clear success.

<details>
<summary>Answers</summary>

1. Gross `20,000 × 0.5 × 7 = 70,000`. Borrowed `20,000 × (0.05 × 7 + 0.10 × 10) = 7,000 + 20,000 = 27,000`. Net `43,000`. Ratio `43,000 / 70,000 ≈ 0.61`.
2. Baseline `19,000`, so each event day shows `30,000 − 19,000 = 11,000` and gross shows `77,000`. That overstates the true 70,000 by 10%.
3. Every 20 days: `L = 0.5 × (1 − e^−1) ≈ 31.6%`, `365/20 × 0.316 × 5 ≈ 28.8` lift-days per year. Every 40 days: `L = 0.5 × (1 − e^−2) ≈ 43.2%`, `≈ 19.7` lift-days per year. Relative cost per lift-day at 20 days is `0.432 / 0.316 ≈ 1.37` times the 40-day cost.
4. For example, the number of lapsed-segment players who returned during the event and were still active 14 days later. Hours may simply move from established players, while the lapsed segment grows.

</details>

## Lab / assignment hook

[Lab 08, measure an event and plan a calendar](../labs/lab08.md). You get 120 days of synthetic player-hours with weekly rhythm, a trend and one announced event. You build a clean-week baseline, measure gross, borrowed and net lift, show how a contaminated baseline changes the report, and then plan a 12-week calendar with the recovery model. Deliverable: passing tests, a chart, and a one-page event report.

## Sources

- RuneScape Wiki, "Double XP" (accessed September 2026). First Bonus XP Weekend 12 March 2010; decaying multiplier from 2.7× down to 1.1× after 7 hours in 2010; constant double XP from October 2012; 48 hours of double XP time within 10-day events and a pause button with a one-hour cooldown (2020); event table with announcement and start dates for 2024 to 2026 (for example, announced 25 April 2025 for 16 May 2025, and 7 November 2025 for 14 November 2025).
- RuneScape Wiki, "Double XP/Guide" (accessed September 2026). Players prepare after an announcement by making money, stocking resources, pre-planting farming patches and saving Slayer points; buyable skills cost half the time and money during the event.
- Valve, Steamworks documentation, "Discounting" (accessed September 2026). A product cannot be discounted within 30 days of another discount; the period was 28 days before 1 January 2023; seasonal sales are exempt; the stated motivation is pricing transparency.
- Warcraft Wiki, "Darkmoon Faire" (accessed September 2026, retail). Opens on the Sunday of the first full week of each month for one week; profession quests completable once per monthly Faire.
- Warcraft Wiki, "Timewalking" (accessed September 2026). Added in patch 6.2.0 (23 June 2015); rotating bonus events for past expansions.
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer.

## Interactive spec: examples/w08-event-pull-forward.html

**The one insight.** A tall event spike can add much less than it shows. The cumulative lift climbs during the event and then falls back through the hangover, and where it settles (the net lift) is what the event added.

**Layout.** Two linked charts stacked on all widths, sharing one x-axis of days from −21 (three weeks before the event starts) to +30. Top: daily player-hours `A_t` as bars or a step line, the baseline as a dashed line, area above baseline shaded "gain" and below shaded "borrowed", with the pre, event and post phases labelled along the top. Bottom: cumulative lift `C_t = Σ_{s ≤ t} (A_s − B_s)` from the announcement day, with horizontal markers for the peak (gross lift minus the pre-dip, 46,000 at defaults) and net lift (the final value), and a bracket over the event days labelled with the gross lift. Controls sit between the charts.

**Model (flat phases, integer days).**
- Baseline `B` per day, default 10,000, editable.
- Announcement lead `a` days, 0 to 21, default 14. Pre-dip `d_pre`, 0% to 30%, default 10%.
- Event length `E`, 1 to 14, default 10. Lift `L`, 0% to 150%, default 60%.
- Post length `h`, 0 to 30, default 14. Post-dip `d_post`, 0% to 60%, default 15%.
- Days before the announcement and after the post phase sit at `B`.
- `A_t = B(1 − d_pre)` in pre, `B(1 + L)` in event, `B(1 − d_post)` in post.
- `gross = B·L·E`, `borrowed = B(d_pre·a + d_post·h)`, `net = gross − borrowed`, `ratio = net / gross` (show "n/a" when gross is 0).

**Baseline toggle.** "True baseline" (default) or "week before event": the dashed line moves to the mean of `A_t` over the 7 days before the event start (if `a < 7`, those days include baseline days), and a readout shows "reported gross" computed against it, next to the true gross.

**Readouts.** Gross, borrowed, net (player-hours, thousands separators), incrementality ratio (two decimals), and reported gross under the chosen baseline with its percent error.

**Test values.**
- Defaults: gross 60,000, borrowed 35,000, net 25,000, ratio 0.42. Week-before baseline 9,000 per day, reported gross 70,000 (+16.7%).
- `d_post = 43%`, other defaults: borrowed 74,200, net −14,200. `d_post = 32.86%` makes net about 0. Label the 43% case "the event cost hours".
- Check-yourself question 1 (`B = 20,000`, `a = 7`, `d_pre = 5%`, `E = 7`, `L = 50%`, `h = 10`, `d_post = 10%`): gross 70,000, borrowed 27,000, net 43,000, ratio 0.61; week-before baseline 19,000, reported gross 77,000 (+10%).
- `a = 0`, `d_pre` any: pre phase empty, borrowed `= B·d_post·h`.

**Secondary panel, spacing.** A small table driven by `L_max` (default 60%) and `τ` (default 30) showing `L(g) = L_max(1 − e^(−g/τ))`, events per year `365/g`, gross lift-days `365/g × L(g) × E`, and relative cost `L(120)/L(g)` for g = 30, 45, 60, 90, 120. Defaults must reproduce the lecture table: 37.9%, 46.6%, 51.9%, 57.0%, 58.9%; lift-days 46.1, 37.8, 31.6, 23.1, 17.9; cost 1.55, 1.26, 1.14, 1.03, 1.00.

**Accessibility and style.** Native range inputs with labels and live numeric outputs; charts have text summaries for screen readers. Respect `prefers-reduced-motion`. Palette from `templates/interactive-tokens.css`; gain and borrowed areas differ by hatch as well as color. No game art or logos.
