# PR402 · Week 13 — Economy Review: Reading Four Weeks of Live Currency Data

**Why this matters:** Your economy has now run for four weeks with real players, and the design numbers from PR401 week 8 have met reality. Most student economies inflate after launch, and the usual chart hides it. The total net inflow falls week after week, the sink ratio climbs, and the team concludes the economy is settling. Meanwhile each remaining player gets richer every week at almost the same rate. This week you read your own ledger per active player, size an intervention to a target you choose, and decide whether to ship it before the showcase.

**You will be able to:**
- Compute net flow, sink-to-faucet ratio and wealth per active player week by week from your currency ledger and active-account counts.
- Explain, with the per-player update rule, why a falling total net inflow can hide a steady rise in wealth per player.
- Size an intervention (a faucet cut, a fee, or both) to a stated growth target, including a behavioural-response scenario.
- Write an economy review that states what you measured, what you will change, who pays for it, and how you will know it worked.

**Before class:** Export your currency ledger since launch, grouped by week and by source (every faucet and every sink), your weekly active accounts, and the median price of three commonly traded items. Reread MMO304 week 12, sections 1 and 3, on the ledger and the choice of denominator (20 minutes), and MMO401 week 14, sections 3 and 4, on who pays for an intervention and how to announce it (20 minutes). Bring your PR401 economy design document.

**Prerequisites from earlier courses:** [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (why prices follow money per player). [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (the ledger, active supply, and the choice of denominator, used here without re-teaching). [MMO308 week 12, economy monitoring](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md) (alarms and baselines). [MMO401 week 13, reading an economic report](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w13-reading-an-economic-report.md) and [MMO401 week 14, intervention design](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w14-intervention-design.md) (incidence, pilots and the intervention spec). From this course, [week 11](w11-live-ops-week-2-operating-rhythm.md) (the cohort table) and [week 12](w12-patch.md) (where an intervention would ship).

**Interactive:** [Wealth per player](../examples/w13-wealth-per-player.html)

---

## 1. What an economy review is

An **economy review** is a short, regular document in which the team reads its currency data and decides whether to change anything. MMO401 week 13 showed how to read a large studio's report. Yours is smaller and has one job: turn four weeks of ledger into one decision, with a number attached.

It answers four questions in order.

1. **How much currency entered and left, and from where?** The ledger by faucet and by sink.
2. **How rich is the typical active player, and how fast is that changing?** Wealth per active player, week by week.
3. **Are prices moving?** A small basket of items traded every week.
4. **What, if anything, do we change?** An intervention sized to a target, or a recorded decision to leave it.

The review is not a redesign. You have two weeks left, one of them for the post-mortem. Anything you change must be a parameter you can set in configuration, such as a reward amount or a fee rate, not a new system.

## 2. The ledger and the denominator

MMO304 week 12 asked you to measure flows and derive stocks. Every currency event in your game should already write a ledger row with a source (quest reward, vendor sale, repair, market stall fee, and so on) and an amount. Summed by week, that gives the **faucet** total `F` and the **sink** total `S`. Their difference, `F − S`, is the **net flow**. Their ratio, `S / F`, is the **sink-to-faucet ratio**. A ratio of 1 means as much currency leaves as enters.

The same lecture warned that the denominator decides what you see. A small persistent game loses many of its launch players in the first month. MMO308 week 3 called them tourists. When they leave, they take their currency out of active circulation, and the players who remain keep earning. Total figures fall because there are fewer players. Figures per active player do not. The worked example shows how far apart the two stories can drift.

Choose **weekly active accounts** as the denominator: accounts with at least one session in the week, counting accounts rather than characters, with any accounts flagged as bots removed. Say so on the review.

## 3. Worked example: the economy that looked like it was settling

### The hook

On 9 December 2021, Jagex added a tax to the Grand Exchange in Old School RuneScape. Sellers paid 1% of the sale price, capped at 5 million coins per item, with a list of low-value items exempt. Jagex framed it as a sink. Most of the coins collected are removed from the game, and a small part is used to buy selected high-value items from players and delete them, to hold up their prices. On 29 May 2025 the rate went up to 2%.

Here is the puzzle. Old School RuneScape had been live since 2013 when the tax arrived. Why add a sink to a game that had run for more than eight years, and then double it? Because in a live economy the question is never "is money entering?" It is "how fast is each player getting richer, and is that faster than we want?" That rate can stay high long after the headline numbers look calm. Your economy is four weeks old, and you are about to meet the same question on a small scale.

### The model

Let `m_t` be the average wealth held by an active player at the end of week `t`, and `N_t` the weekly active accounts. Two simplifying assumptions make the arithmetic clean.

- Players who leave during the week take average wealth with them, so they neither raise nor lower `m`.
- The week's net flow goes to the players still active at the end of it. New accounts after launch week are few and are ignored here. Week 9's active accounts are the launch cohort from [week 10](w10-live-ops-week-1.md), 260 accounts created on launch day, plus the players who joined later that week.

Then:

```
m_t = m_(t−1) + (F_t − S_t) / N_t
```

Wealth per player rises each week by the net flow per remaining player. When faucets and sinks scale with the number of players, write them per player, `φ = F / N` and `σ = S / N`. The weekly rise becomes `φ − σ`, which does not depend on `N` at all. Losing players shrinks every total on your dashboard but leaves each remaining player's weekly gain where it was.

To size an intervention, choose an allowed growth rate `g` for `m` per week. Some growth is healthy, because players move into content where things cost more. The cut needed per player per week is:

```
cut = (φ − σ) − g × m
```

and the two levers in most student games contribute:

```
faucet cut c on rewards:           c × φ
stall fee rise f on sales v:      f × v × (1 − e)
```

where `v` is market stall sales per active player per week and `e` is the share of trade that disappears because of the higher fee (the behavioural response). Emberfall already charges the 5% stall fee from PR401 week 8, and it is in `S`, so `f` here is the rise on top of it.

### Numbers you can check

The Emberfall team's economy uses a currency called marks (PR401 week 8). Their ledger, weekly active accounts, and the median stall price of an iron ingot:

| Week | Faucet `F` | Sink `S` | Net | `S / F` | Active `N` | Net per player | `m` | Total stock | Iron ingot |
|---|---|---|---|---|---|---|---|---|---|
| 9 (launch) | 1,800k | 1,080k | 720k | 0.600 | 400 | 1,800 | 1,800 | 720k | 40 |
| 10 | 1,650k | 1,160k | 490k | 0.703 | 310 | 1,581 | 3,381 | 1,210k | 46 |
| 11 | 1,420k | 1,050k | 370k | 0.739 | 260 | 1,423 | 4,804 | 1,580k | 57 |
| 12 | 1,300k | 990k | 310k | 0.762 | 240 | 1,292 | 6,095 | 1,890k | 71 |

Check week 11. Net is `1,420k − 1,050k = 370k`. Per player, `370,000 / 260 = 1,423.1`. So `m_11 = 3,380.6 + 1,423.1 = 4,803.7`.

Now read it the way the team first did. Net inflow fell from 720k to 310k, less than half. The sink ratio rose from 0.60 to 0.76. Total stock is growing more slowly each week. "The economy is settling."

Read it per player. Net flow per player fell only from 1,800 to 1,292. Wealth per active player more than tripled, from 1,800 to 6,095, and rose by 27% in week 12 alone (`6,095 / 4,804 = 1.27`). The iron ingot price is up 78% since launch. Prices lag wealth, as MMO304 week 4 explained, so more increases are on the way. With no change, four more weeks at the week-12 rate add `4 × 1,291.7 = 5,167` marks, for `m ≈ 11,262` at the showcase.

Most of the fall in total net inflow came from players leaving, not from sinks getting stronger. From week 9 to week 12, active accounts fell 40% and total net inflow fell 57%. Net per player fell 28%.

**Sizing the fix.** In week 12, `φ = 1,300,000 / 240 = 5,416.7` and `σ = 990,000 / 240 = 4,125.0`, a gap of 1,291.7 marks per player per week. The team sets `g = 3%` a week, so allowed growth is `0.03 × 6,095.4 = 182.9`. The cut needed is `1,291.7 − 182.9 = 1,108.8` marks per player per week. Market stall sales were 2,100k marks in week 12, so `v = 8,750` per player.

| Option | Removes per player | Net per player | Growth of `m` |
|---|---|---|---|
| A. Quest rewards cut 12.5% and the stall fee raised 5 points, to 10% | `677.1 + 437.5 = 1,114.6` | 177.1 | 2.9% |
| B. As A, but the higher fee drives away 20% of stall trade | `677.1 + 350.0 = 1,027.1` | 264.6 | 4.3% |
| C. Quest rewards cut 20.5%, stall fee unchanged | 1,110.4 | 181.3 | 3.0% |

Option A hits the target on paper. Option B shows how much of that depends on players not changing behaviour. Option C hits the target without relying on behaviour, but it takes a fifth of the rewards from players who are still here, which they will notice.

This script reproduces both tables. Run it with `.venv/bin/python`.

```python
F = [1_800_000, 1_650_000, 1_420_000, 1_300_000]
S = [1_080_000, 1_160_000, 1_050_000, 990_000]
N = [400, 310, 260, 240]
m = 0.0
for week, f, s, n in zip((9, 10, 11, 12), F, S, N):
    m += (f - s) / n
    print(f"week {week}: S/F {s / f:.3f}  net/player {(f - s) / n:7.1f}  m {m:7.1f}")
phi, sig = F[-1] / N[-1], S[-1] / N[-1]
need = (phi - sig) - 0.03 * m
v = 2_100_000 / N[-1]
for name, c, fee, e in (("A", 0.125, 0.05, 0.0), ("B", 0.125, 0.05, 0.2), ("C", 0.205, 0.0, 0.0)):
    removed = c * phi + fee * v * (1 - e)
    net = phi - sig - removed
    print(f"{name}: removes {removed:7.1f}  net {net:6.1f}  growth {net / m:.1%}  (need {need:.1f})")
```

It prints:

```
week 9: S/F 0.600  net/player  1800.0  m  1800.0
week 10: S/F 0.703  net/player  1580.6  m  3380.6
week 11: S/F 0.739  net/player  1423.1  m  4803.7
week 12: S/F 0.762  net/player  1291.7  m  6095.4
A: removes  1114.6  net  177.1  growth 2.9%  (need 1108.8)
B: removes  1027.1  net  264.6  growth 4.3%  (need 1108.8)
C: removes  1110.4  net  181.3  growth 3.0%  (need 1108.8)
```

### Cross-game recognition

**Old School RuneScape (Grand Exchange tax, 2021 and 2025).** A fee on trade volume, the `f × v` lever in the model. Raising the rate from 1% to 2% in 2025 is a rise of `f = 1%`. What it removes depends on how much trading continues at the higher rate, which is `e`. The cap per item and the exempt list both limit `v`, which is part of who pays.

**EVE Online (Monthly Economic Report).** CCP publishes a monthly report for EVE. The August 2025 edition, published on 11 September 2025, includes the money supply and a history of the top sinks and faucets. That is the review you are writing, at the scale of a game that has run for over two decades. Its faucet and sink charts are the `F` and `S` columns of your table, split by source.

**The MMO304 denominator case.** MMO304 week 12 showed an economy where total gold rose 8.3% while gold per monthly active player rose 30%, because players who left kept their gold on their characters. Your table is the same effect over four weeks, with the model written out so that you can size a fix.

### Eyes-open design judgment

- **Choose `g` deliberately.** Zero growth means players never feel richer, which undercuts progression. Too much growth means prices race away from new players. Write the number and the reason in the review.
- **Faucet cuts are felt; fees are dodged.** Cutting quest rewards is predictable but visible, and players read it as a nerf. A fee depends on behaviour you cannot predict well. Mixing them spreads both risks. MMO401 week 14 has the incidence argument.
- **The assumptions matter.** If the players who leave are poorer than average, as tourists often are, `m` rises faster than this model says. If many new accounts join, `m` rises more slowly. Check the model against your ledger's actual active-held stock before trusting the projection.
- **Two weeks is short.** Anything you change now will barely show before the showcase. A pilot on one server or a parameter change with a clear rollback is safer than a large move, and "we measured it and chose not to change it" is a legitimate outcome if the argument is written down.

### Check this example

1. Another team has `F = 900k`, `S = 810k` and `N = 150` in its latest week. Its sink ratio is 0.90. How fast is `m` rising per week?
2. For Emberfall, how far must the stall fee rise, with no faucet cut and no behavioural response, to meet `g = 3%`? Is that realistic?
3. Emberfall's active accounts fall to 200 next week while `φ` and `σ` stay the same. What happens to total net inflow, and to the weekly rise in `m`?

<details>
<summary>Answers</summary>

1. `(900,000 − 810,000) / 150 = 600` marks per player per week. A high sink ratio does not mean slow growth per player.
2. `f × 8,750 = 1,108.8`, so `f = 12.7%`, a stall fee of 17.7%. That is high enough that players will trade face to face instead of at the stalls, or stop trading, so `e` would be large, and the real removal much smaller. A fee alone cannot do it.
3. Total net inflow falls to `1,291.7 × 200 = 258.3k`, which looks like progress. The weekly rise in `m` stays at 1,291.7, because it does not depend on `N`.

</details>

## 4. From numbers to a decision

The review ends with a decision in the intervention-spec form from MMO401 week 14: the change, the parameter values, who pays, how you will announce it, the metric you expect to move and by how much, and how you would reverse it. For a student team two points carry the most weight.

**Who pays.** A faucet cut on quests hits players who are levelling. A fee on trades hits traders and crafters. Look at your own cohort table from week 11. If the players still levelling are the newest ones, a quest cut lands on the players you most need to keep.

**Announce before you change.** Players who wake up to smaller rewards without an explanation assume a mistake or bad faith. Post the reason and the numbers in the patch notes. A short version of your table is usually enough.

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: the per-player update rule, sizing a cut, behavioural response | Notes |
| 0:15-0:55 | Build the weekly ledger table: `F`, `S`, net, `S / F`, `N`, net per player, `m`, total stock, three prices (lab 13, part A) | Ledger table |
| 0:55-1:20 | Check the model: compare `m × N` with the active-held stock from a direct query. Explain any gap (part B) | Model check |
| 1:20-1:30 | Break | |
| 1:30-2:10 | Choose `g`, compute the cut needed, cost three options including one behavioural scenario (part C) | Option table |
| 2:10-2:40 | Write the decision in intervention-spec form, including who pays and rollback (part D) | Decision |
| 2:40-3:00 | Two-minute stand-up per team: the headline number, the decision, the reason. Instructor sign-off | Sign-off |

## Deliverables

Due before the week 14 studio meeting, in `production/week13/` in the team repository.

1. **Lab 13 worksheet**, parts A to D. Checked by recomputing two rows of the ledger table and one option.
2. **The economy review**, at most two pages, with the table, the model check, the options and the decision. Checked against the worksheet.
3. **If you ship a change:** the configuration diff, the patch note, and the metric with its expected value and check date. **If you do not:** the written reason and the level at which you would act.

## Common failure modes

- **Reading totals only.** Total net inflow and the sink ratio can improve while each player gets richer at almost the same rate. Always compute per active player.
- **Counting characters as players.** Alts inflate `N` and shrink `m`. Use accounts.
- **Trusting the model without checking it.** Compare `m × N` with a direct query of currency held by active accounts. If they differ by more than about 10%, find out why before sizing anything.
- **Sizing a fee as if nobody reacts.** Always cost one scenario in which trade volume drops.
- **Nerfing without telling players.** Announce the change and the reason with the patch.
- **Redesigning in week 13.** You have time for a parameter change, not a new system.

## Review checklist

The instructor checks, at the week 14 meeting:

- [ ] The ledger table covers every week since launch, with `F`, `S` and `N` sourced from queries the team can show.
- [ ] Two recomputed rows match the table, including `m`.
- [ ] The model is checked against a direct measure of active-held currency, and any gap is explained.
- [ ] `g` is stated with a reason, and the needed cut is computed from it.
- [ ] At least three options are costed, including one with a behavioural response.
- [ ] The decision names who pays, how it is announced, the metric and expected value, and how it would be reversed.
- [ ] A shipped change matches its configuration diff and patch note, or a no-change decision states the level at which the team would act.

## Sources

- Old School RuneScape Wiki, "Grand Exchange" (oldschool.runescape.wiki, read September 2026). The tax introduced on 9 December 2021 in the "Grand Exchange Tax & Item Sink" update at 1%; the cap of 5 million coins per item; the exempt item list; the increase to 2% on 29 May 2025; Jagex's explanation, via Mod Ash, that most of the collected coins are removed from the game and a small amount buys selected items from players to delete them.
- CCP Games, "Monthly Economic Report, August 2025" (eveonline.com news, published 11 September 2025, read September 2026). The report's money supply charts and its history of top sinks and faucets.
- The Emberfall ledger, player counts, prices and trade volumes are a constructed example for teaching. They are not data from any real game.

## Interactive spec: examples/w13-wealth-per-player.html

**The one insight.** A total net inflow that falls week after week can sit on top of a wealth-per-player line that keeps rising almost as fast as before. The two views must look like two different economies until the student sees they are the same data.

**Layout.** Two linked views side by side on desktop, stacked on mobile, with the left view first.

1. **Left view, "the dashboard".** Weekly bars of total net inflow (`F − S`) for weeks 9 to 16, with the sink-to-faucet ratio as a line on a right-hand axis. Weeks 9 to 12 are data; weeks 13 to 16 are projection, drawn hatched. Large text above: "Net inflow down 57% since launch".
2. **Right view, "per player".** A line of `m`, wealth per active player, for the same weeks, with a dashed line showing the path at the allowed growth `g`. Large text above: "Wealth per player ×3.4 since launch; +1,292 per week".
3. **Readout table** under both: week, `F`, `S`, `N`, net, `S / F`, net per player, `m`.

**Controls.**
- Weekly churn `d` for weeks 13 to 16 (0% to 20%, default 5%).
- Quest reward cut `c` (0% to 40%, step 0.5%, default 0%).
- Stall fee rise `f` on top of the existing 5% (0% to 15%, step 0.5%, default 0%).
- Trade lost to the fee `e` (0% to 60%, default 0%).
- Allowed growth `g` (0% to 10%, default 3%).
- Buttons for options A, B and C that set `c`, `f` and `e`.
All controls keyboard operable with visible focus.

**Formulas.**

```
data weeks 9-12: F = [1800000, 1650000, 1420000, 1300000], S = [1080000, 1160000, 1050000, 990000], N = [400, 310, 260, 240]
m_t = m_(t−1) + (F_t − S_t) / N_t,  m_8 = 0
projection weeks 13-16:
  N_t = N_(t−1) × (1 − d)
  φ = 5416.67, σ = 4125.0, v = 8750  (week-12 values per player)
  removed = c × φ + f × v × (1 − e)
  net per player = φ − σ − removed
  F_t = (1 − c) × φ × N_t;  S_t = σ × N_t + f × v × (1 − e) × N_t
  m_t = m_(t−1) + net per player
cut needed = (φ − σ) − g × m_12
```

**Test values** (must match the guide).
- Data weeks: `S/F` 0.600, 0.703, 0.739, 0.762; `m` 1,800.0, 3,380.6, 4,803.7, 6,095.4.
- Defaults (no change, `d` 5%): `m_16` = 11,262; `N_16` = 195.5 (display 195); net inflow week 13 = 294.5k.
- Cut needed at `g` 3%: 1,108.8.
- Option A: removes 1,114.6, net 177.1, growth 2.9%. Option B: 1,027.1, 264.6, 4.3%. Option C: 1,110.4, 181.3, 3.0%.

**Behaviour.** Changing any control redraws both views and the table within one frame; transitions 200 ms, none under `prefers-reduced-motion`. Colors from `templates/interactive-tokens.css`; projection weeks carry a text label "projected" as well as hatching. No game art or logos.
