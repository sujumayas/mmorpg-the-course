# MMO304 · Week 14 — Designing an Economy from Scratch

**Why this matters:** Every economy in this course was patched after launch, often in a hurry. This week you design one before launch, in the order that avoids most of those patches. You start from the wealth you want players to hold and size the sinks to hit it, instead of adding faucets and hoping.

**You will be able to:**
- Derive the steady-state wealth of a player from a faucet rate, flat sinks and proportional sinks, and compute how fast wealth approaches it.
- Size a set of sinks to hit a target wealth and a target half-life, and check the result with a table you can verify by hand.
- Predict how the mix of new and veteran players pulls a server's average wealth below the steady state, and say which telemetry segment to watch.
- Write the economy section of a game design spec (currencies, flow tables, market design, telemetry and levers) that another designer can implement and tune.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the chapters on money supply and on economic design goals. Reread your week 3 and week 4 notes on faucets, sinks and money supply per capita. Reread [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) on doubling intervals; today you use the same idea for halving.

**Prerequisites from earlier courses:** [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (growth and decay by a constant factor). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (solving for time). GD102 [week 2 on stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md), [week 7 on sources and drains](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md) and [week 14 on tuning with spreadsheets](../../GD102-systems-design-and-game-mechanics/lectures/w14-tuning-with-spreadsheets.md). From this course, [week 3](w03-faucets-sinks-and-transformations.md), [week 4](w04-money-supply-per-capita-and-inflation.md), [week 8](w08-item-decay-durability-and-destruction-as-sinks.md), [week 12](w12-economic-telemetry-and-dashboards.md) and [week 13](w13-case-studies-eve-diablo-runescape-grand-exchange.md).

**Interactive:** [examples/w14-steady-state-sinks.html](../examples/w14-steady-state-sinks.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. Design in the right order

Most failed economies were designed faucet first. Someone writes quest rewards, someone else writes loot tables, and a third person adds repair costs because it "feels right". Months later telemetry shows prices doubling, and the team bolts on a sink.

Reverse the order. Decide what you want and work backwards.

1. **What is money for?** Name the two or three things players should want to buy. If nothing worth buying exists at the top level, rich players stop earning, and your faucets turn into pure inflation for everyone else.
2. **Targets.** Pick a target for how much currency a typical active player should hold once settled, and how quickly they should get there. This lecture calls them `W*` (steady-state wealth) and the half-life.
3. **Faucets.** List every source per active player per day.
4. **Flat sinks.** List costs that do not depend on wealth, such as repairs, travel and consumables.
5. **Proportional sinks.** Add sinks that grow with wealth or trade, such as market taxes and luxury goods, and size them to hit the targets. Section 2 shows how.
6. **Markets and reach.** Decide what can be traded and how far (week 13).
7. **Telemetry and levers.** Choose the numbers you will watch, the thresholds that trigger action, and the knob you will turn.

Steps 2 and 5 are the ones teams skip. They are the reason this lecture exists.

## 2. Worked example: the sink that sets its own ceiling

### The hook

In 2025 two long-running MMOs raised the same kind of fee. In March, EVE Online raised its market sales tax from 4% to a 7.5% base rate. In May, Old School RuneScape doubled its Grand Exchange tax from 1% to 2%. Neither studio added a new flat cost, like a bigger repair bill. Both raised a *percentage*.

Why a percentage? Because a percentage sink grows as players get richer, and a sink that grows with wealth stops wealth from growing without limit. A flat sink cannot do that. This worked example shows exactly how far wealth rises under each kind of sink, and how to choose the rate.

### The model

Follow one typical active player's currency `W`, measured in gold, day by day.

- `F` is faucet income per day (quest rewards, loot sold to vendors, daily bonuses).
- `S` is flat sinks per day (repairs, travel, consumables).
- `s` is the proportional sink rate per day, the share of held wealth removed each day.
- `N = F − S` is net income before proportional sinks.

Wealth changes each day by income minus outflow:

```
dW/dt = N − s × W
```

When `W` is small, the proportional sink is small and wealth grows at almost `N` per day. As `W` grows, the sink grows with it. Wealth stops growing when outflow equals income, at the **steady state**:

```
W* = N / s
```

Starting from `W = 0`, the solution is

```
W(t) = W* × (1 − e^(−s·t))
```

This is exponential decay of the gap between `W` and `W*`. The gap halves every `ln 2 / s` days. Call that the **half-life** of the economy for one player. After two half-lives the player is at 75% of `W*`. It takes `ln 10 / s` days to reach 90%.

A proportional sink usually comes from a tax on trade. If a player sells a share `v` of their holdings through the market each day (their personal velocity) and the market tax is `τ`, the sink removes `τ × v × W` per day, so

```
s = τ × v
```

Several proportional sinks add. A 3% market tax at `v = 0.3` gives `s = 0.009`. Add luxury spending of 1.1% of holdings per day and `s = 0.02`.

If `s = 0`, there is no steady state. Wealth rises by `N` every day, forever. That straight line is the inflation you met in week 4, where more money per capita chasing the same goods pushed prices up.

### Numbers you can check

Take a fictional MMO, Tidewater, and a player who plays two hours a day. All the numbers are invented and chosen to be easy to check.

| Faucet or sink | Gold per day |
|---|---|
| Quest rewards | +3,000 |
| Loot sold to vendors | +5,000 |
| Daily contract | +2,000 |
| **Faucets `F`** | **+10,000** |
| Repairs | −2,500 |
| Travel | −1,000 |
| Consumables from vendors | −500 |
| **Flat sinks `S`** | **−4,000** |
| **Net `N`** | **+6,000** |

Now compare three designs. Design A has no proportional sink. Design B has only a 3% market tax, `s = 0.009`. Design C adds luxury spending on top, `s = 0.02`.

| Day | A: `s = 0` | B: `s = 0.009` | C: `s = 0.02` |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 30 | 180,000 | 157,747 | 135,357 |
| 60 | 360,000 | 278,168 | 209,642 |
| 90 | 540,000 | 370,095 | 250,410 |
| 180 | 1,080,000 | 534,734 | 291,803 |
| 365 | 2,190,000 | 641,706 | 299,797 |
| Steady state `W*` | none | 666,667 | 300,000 |
| Half-life `ln 2 / s` | none | 77.0 days | 34.7 days |

Check one cell by hand. Design C at day 30 is `300,000 × (1 − e^(−0.6))`. Since `e^(−0.6) ≈ 0.5488`, that gives `300,000 × 0.4512 ≈ 135,357`.

Three things to notice.

1. Design A's player holds 2.19 million gold after a year, and will hold 4.38 million after two. Nothing stops it.
2. Design B has a ceiling, but it takes 77 days to close half the gap. A player who quits after three months never sees the ceiling.
3. Design C settles near 300,000 within about four months, and its sinks then remove almost exactly `N` per day. At day 365 the proportional sink takes `0.02 × 299,797 ≈ 5,996` gold per day against 6,000 of net income. At steady state, sinks equal faucets.

That third point is the whole game. You cannot make sinks equal faucets with flat costs unless you guess every player's income correctly. A proportional sink finds the balance by itself, at the wealth level `N / s`.

### The visual

Open the interactive. The left panel shows wealth over a year for the current settings, with a dashed line at `W*` and a marker at one half-life. The right panel shows two flows per day against the same time axis: net income `N` as a flat line, and proportional sink outflow `s × W(t)` rising to meet it. The shaded gap between them is the daily growth of `W`.

Set the luxury slider to zero and the market tax to zero. The right panel's outflow line lies on the floor, the gap never closes, and the left panel's wealth is a straight line upward. Now raise the market tax. The outflow line rises until it touches `N`, and the wealth curve bends flat at exactly that moment. The left panel shows a ceiling appearing. The right panel shows why. Wealth stops rising when the sink reaches the faucet.

Then try the "double the faucet" button. `F` goes from 10,000 to 20,000, and since flat sinks stay at 4,000, `N` goes from 6,000 to 16,000. `W*` rises in the same proportion, from 300,000 to 800,000, and the half-life does not move. Faucet size sets *where* wealth settles. The proportional rate sets *how fast* it gets there. Those are separate knobs, and you should tune them separately.

### Cross-game recognition

The same form, `s = τ × v`, sits under every market fee.

**Old School RuneScape (Grand Exchange tax, since May 29, 2025).** A 2% tax on most sales, so `τ = 0.02`. For a player who sells a third of their holdings each day, `s ≈ 0.0067` and the half-life is about 104 days. The tax is capped at 5 million coins per item, which makes it flat for any item priced above 250 million. A cap turns a proportional sink back into a flat one exactly at the top of the wealth distribution, where the ceiling matters most. Part of the revenue funds a system that buys selected items and deletes them, so the same fee also works as an item sink.

**EVE Online (sales tax and broker fee, from release 22.02, March 2025).** Sales tax has a 7.5% base and broker fees at NPC stations a 3% base, both reduced by skills and standings. A seller who lists at an NPC station at the base rates pays about 10.5% of each sale, which is a large `τ`. EVE's players trade heavily, so `v` is high too. CCP publishes the resulting ISK faucets, sinks and money supply every month in its economic report.

**World of Warcraft (faction auction house, all eras).** The house keeps 5% of each winning bid, so `τ = 0.05`, plus a deposit based on the item's vendor price that is lost if the item does not sell.

**Diablo III gold auction house (2012 to March 2014).** A 15% cut, `τ = 0.15`. Even with that high rate, the case study last week showed that the market's bigger problem was reach, not money supply.

Four games, one equation. When you meet a new fee, find `τ`, estimate `v`, and you can predict the ceiling it sets and how long players take to reach it.

### Design judgment, eyes open

- **Strength.** A proportional sink balances itself. You do not have to predict every player's income. Players who earn more settle higher, and every player settles somewhere.
- **Strength.** The two knobs split cleanly. Faucets set `W*`, and `s` sets the half-life. You can raise rewards for a new zone without changing how fast wealth settles.
- **Cost.** A market tax only hits players who trade. A hoarder with `v = 0` pays nothing and has no ceiling. Always ask whose `v` is low, and add a second proportional sink that reaches them, such as luxury goods, upkeep on property they choose to own, or cosmetic crafting that consumes currency.
- **Cost.** High `τ` pushes trade off the market. Players arrange direct trades, or trade items instead of gold, to dodge the fee, which lowers `v` and weakens the sink. RuneScape's 2007-2011 limits on unbalanced direct trades (week 13) show how much effort it takes to close that route.
- **Cost.** Caps and flat fees are regressive. A flat 2,500 gold repair bill is 25% of a new player's daily income and a rounding error to a veteran. Decide deliberately who pays.

## 3. The server is not one player

Your telemetry will show the server's *average* wealth per active player, not one player's curve. The two differ, because players are at different ages.

Suppose players arrive at a steady rate and each stays active for `L` days, so account ages are spread evenly from 0 to `L`. Each player follows `W(a) = W* × (1 − e^(−s·a))` at age `a`. Averaging over ages gives

```
server average = W* × (1 − (1 − e^(−s·L)) / (s·L))
```

For Tidewater's design C (`s = 0.02`):

| Typical stay `L` | `s·L` | Server average as a share of `W*` | Server average |
|---|---|---|---|
| 30 days | 0.6 | 24.8% | 74,406 |
| 90 days | 1.8 | 53.6% | 160,883 |
| 365 days | 7.3 | 86.3% | 258,932 |

This has two design consequences.

**Retention changes money supply.** If a content update keeps players longer, `L` rises and the server average climbs, with no change to any faucet or sink. A dashboard that shows only the server average will report "inflation" that is really a shift in who is playing. Segment every wealth metric by account age (week 12).

**A launch is not a steady state.** On day 1 every account has age 0. For a month or more the server average rises steeply whatever your sinks are, and prices of scarce goods rise with it. Do not tune sinks against launch-month data. Tune against the cohort of players who have been active for several half-lives.

## 4. The rest of the spec

The steady-state model sets the size of the money flows. The rest of the spec decides what those flows are made of. Write each part below as a short section of your final economy spec (see [Lab 14](../labs/lab14.md) and the final assessment brief).

### Currencies

List every currency, what earns it, what spends it, and whether it can be traded. For each tradeable one, give its steady-state target and half-life. A premium currency bought with real money needs its own section on exchange rates and real-money trade (week 11), and MMO401 goes further on exchange rates.

### Transformations and items

Draw the crafting graph from week 7. Mark every node where an item leaves the game (week 8), such as consumption, decay or destruction. An item economy has its own steady state. If items enter at `I` per day and a share `δ` of the stock is destroyed per day, the item stock settles at `I / δ`, the same equation as gold. Items with `δ = 0` pile up forever, and their prices fall until they reach the vendor price.

### Market design

Decide per item category what `m`, the market reach from week 13, should be. Bind the core reward, open the market for inputs and cosmetics, and choose a tax `τ` from the steady-state calculation. Say whether you run one global market or several regional ones.

### Telemetry and levers

For each target, write one row:

| Metric | Segment | Target band | Lever if above | Lever if below |
|---|---|---|---|---|
| Median gold held | Active 60+ days | 250,000 to 350,000 | Raise luxury sink rate | Lower market tax |
| Price index of basic goods (week 4) | All trades | ±10% month on month | Add or raise sinks | Review faucets for the affected goods |
| Market tax revenue ÷ net faucet | Server | 0.3 to 0.6 | Check for tax evasion through direct trade | Check that `v` has not collapsed |

The levers column is the part most specs leave out. Every threshold without a lever is just a warning light with nobody to act on it.

### Failure modes to write down in advance

- **Exploit faucet.** A duplication bug or an unintended farm spot raises `F` for a few players by a factor of 100. Your proportional sink still caps their wealth at `N / s`, but with 100 times the faucet that cap is over 100 times the normal `W*` (about 166 times for Tidewater's design C, since flat sinks do not scale up), which is far too much. Plan for rollback and for detection (MMO309 covers anti-cheat).
- **Real-money pressure.** A steady-state wealth that takes 100 days to reach is a 100-day grind someone will sell a shortcut to (week 11).
- **Dead top end.** If `W*` is far above the price of the best purchasable item, rich players have nothing to spend on and stop engaging with money. Keep something desirable priced near `W*`.

## In-class activity (30 minutes)

Pairs. Each pair designs the currency flows for one of three fictional games: a fishing-village life sim, a space-trading MMO with ship loss, or a dungeon crawler with bound loot.

1. (8 min) Fill a faucet and flat-sink table like Tidewater's for a player who plays one hour a day. Make `N` positive.
2. (7 min) Choose `W*` and a half-life. Compute `s`. Split it into at least two proportional sinks, one of which must reach players with low `v`.
3. (5 min) Use the section 3 formula to predict the server average for a typical stay of 60 days.
4. (10 min) Swap with another pair. Find one player type your partners' sinks miss, and one lever in their telemetry table that would not work.

Expected output: a one-page table with `F`, `S`, `N`, `s`, `W*`, half-life and server average, and one written weakness from the other pair.

## Common misconceptions

- **"Sinks should equal faucets from day one."** Early on, sinks are small because players are poor. Proportional sinks equal net faucets only at steady state. If your flat sinks equalled faucets at launch, new players could never save.
- **"A bigger tax fixes inflation faster."** A bigger `s` shortens the half-life and lowers `W*`, but it also pushes trade off the market, which lowers `v` and can cancel the gain. Model `v` as something the tax changes.
- **"If the server average is rising, faucets are too high."** It may be rising because players stay longer. Check wealth by account-age cohort first.
- **"Doubling rewards doubles the time to reach the ceiling."** It raises `W*` in proportion to net income `N` (more than double when flat sinks stay fixed) and leaves the half-life unchanged. Time to reach a *fixed* amount of gold goes down, not up.

## Check yourself

1. A player earns `F = 12,000` gold per day and pays `S = 3,000` in flat sinks. You want them to settle near 450,000 gold. What proportional rate `s` do you need, and what is the half-life?
2. With `τ = 0.04` and `v = 0.25`, what is `s`? If `N = 5,000`, what is `W*`, and how many days until the player holds 90% of it?
3. A designer doubles every faucet in design C (`s = 0.02`, `N = 6,000`). What are the new `W*` and half-life? On what day does the player first pass 250,000 gold, before and after the change?
4. Players' typical stay rises from 30 to 90 days in design C. By what factor does the server average rise? Did any faucet or sink change?
5. Your market tax is capped at 1 million gold per sale with `τ = 0.02`. Above what sale price does the tax stop being proportional, and why is that a problem for the richest players' wealth?

<details>
<summary>Answers</summary>

1. `N = 9,000`, so `s = 9,000 / 450,000 = 0.02` per day. Half-life `ln 2 / 0.02 ≈ 34.7` days.
2. `s = 0.04 × 0.25 = 0.01`. `W* = 5,000 / 0.01 = 500,000`. 90% takes `ln 10 / 0.01 ≈ 230` days.
3. Only the faucets double, so `F = 20,000`, `S = 4,000`, `N = 16,000`, `W* = 800,000`, half-life still 34.7 days. Before: solve `300,000 (1 − e^(−0.02t)) = 250,000`, so `e^(−0.02t) = 1/6` and `t = ln 6 / 0.02 ≈ 89.6` days. After: `800,000 (1 − e^(−0.02t)) = 250,000`, so `e^(−0.02t) = 0.6875` and `t = ln(1/0.6875) / 0.02 ≈ 18.7` days.
4. From 24.8% to 53.6% of `W*`, a factor of about 2.16. No faucet or sink changed. The rise comes only from the age mix.
5. The tax hits 1 million at a sale price of `1,000,000 / 0.02 = 50 million`. Above that, each sale pays a flat fee, so `τ` falls as prices rise. The richest players trade the most expensive items, so their effective `s` is lowest and their `W*` highest, which is the opposite of what a ceiling should do.

</details>

## Lab / assignment hook

[Lab 14, economy spec and steady-state simulation](../labs/lab14.md). You build a day-by-day spreadsheet for your own game's economy with faucets, flat sinks, two proportional sinks and a population of arriving and leaving players, then tune it to hit your targets. The lab's output is the core of the final economy spec, and it uses the market-reach analysis from [Lab 13](../labs/lab13.md).

## Sources

- EVE University Wiki, "Sales tax" and "Market" (accessed September 2026). Sales tax raised from 4% to a 7.5% base in release 22.02 (March 12, 2025); broker fee base 3% at NPC stations; reductions from skills and standings.
- Old School RuneScape Wiki, "Grand Exchange" (accessed September 2026). Tax of 1% from December 9, 2021, raised to 2% on May 29, 2025, capped at 5 million coins per item; revenue funds an item sink.
- Warcraft Wiki, "Auction House" (accessed September 2026). 5% cut of the winning bid on the faction auction house; deposit based on vendor sell price and duration.
- Wikipedia, "Diablo III" (accessed September 2026). 15% cut on gold auction house sales; auction houses closed March 18, 2014.
- CCP Games, *Monthly Economic Report, January 2024*, eveonline.com. ISK faucets and sinks and money supply sections.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w14-steady-state-sinks.html

**Purpose.** Show that a proportional sink creates a wealth ceiling at `W* = N / s`, that wealth stops rising exactly when the sink outflow reaches net income, and that faucet size and sink rate are separate knobs (level versus speed).

**Layout.** Two linked panels, side by side at desktop width and stacked on mobile (left first). Controls above. A numbers strip below.

**Controls.**
- Faucets `F`: slider 0 to 30,000 gold per day, step 500, default 10,000.
- Flat sinks `S`: slider 0 to 20,000, step 500, default 4,000. If `S ≥ F`, show "net income is zero or negative, wealth never grows" and clamp `N` at 0 for plotting.
- Market tax `τ`: slider 0% to 20%, step 0.5%, default 3%.
- Velocity `v`: slider 0 to 1 per day, step 0.05, default 0.3. Label "share of holdings sold through the market each day".
- Luxury sink `ℓ`: slider 0% to 5% of holdings per day, step 0.1%, default 1.1%.
- Button "Double the faucet": sets `F` to twice its value (capped at the slider max) so students see `W*` rise with `N` (300,000 to 800,000 for design C) and the half-life stay put.
- Preset buttons: "Design A" (τ = 0, ℓ = 0), "Design B" (τ = 3%, ℓ = 0), "Design C" (τ = 3%, ℓ = 1.1%), all with F = 10,000, S = 4,000, v = 0.3.
- Day marker slider 0 to 365, default 90.

**Derived values.** `N = max(0, F − S)`. `s = τ × v + ℓ`. If `s > 0`, `W* = N / s`, half-life `h = ln 2 / s`, 90% time `ln 10 / s`. Wealth `W(t) = W* × (1 − e^(−s·t))` for `s > 0`, and `W(t) = N × t` for `s = 0`.

**Left panel, wealth over time.** x axis days 0 to 365. y axis gold, auto-scaled to the larger of `W(365)` and `W*`, rounded up to a nice number. Solid curve `W(t)`. Dashed horizontal line at `W*` labelled with its value (hidden when `s = 0`, replaced by the text "no ceiling"). A dot on the curve at `t = h` labelled "half-life".

**Right panel, flows per day.** Same x axis. y axis gold per day, 0 to `1.1 × N`. Flat line at `N` ("net income"). Rising curve `s × W(t)` ("proportional sinks"), which equals `N × (1 − e^(−s·t))`. Shade the gap between them ("daily growth of wealth"). When the gap at the marker falls below 1% of `N`, show the caption "sinks ≈ faucets: steady state".

**Numbers strip, at the day marker.** `N`, `s` (4 decimal places), `W*`, half-life (1 decimal place), days to 90%, `W(t)`, sink outflow `s × W(t)`, gap `N − s × W(t)`.

**The one insight.** Wealth stops rising when the proportional sink reaches net income. Faucets set where wealth settles, and the sink rate sets how fast.

**Test values (F = 10,000, S = 4,000, v = 0.3).**
- Design A (s = 0): W(30) = 180,000; W(365) = 2,190,000.
- Design B (s = 0.009): W* = 666,667; half-life 77.0 days; W(30) = 157,747; W(90) = 370,095; W(365) = 641,706.
- Design C (s = 0.02): W* = 300,000; half-life 34.7 days; days to 90% 115.1; W(30) = 135,357; W(90) = 250,410; W(180) = 291,803; W(365) = 299,797; sink outflow at day 365 = 5,996.
- Design C with F doubled to 20,000: N = 16,000, W* = 800,000, half-life still 34.7 days.

**Optional third tab, server average.** Slider for typical stay `L` (7 to 365 days, default 90). Show `W* × (1 − (1 − e^(−s·L)) / (s·L))` next to `W*`. Test values for design C: L = 30 gives 24.8% of W* (74,406); L = 90 gives 53.6% (160,883); L = 365 gives 86.3% (258,932).

**Accessibility.** Keyboard-operable sliders and buttons with visible values. Distinct line styles (solid wealth, dashed ceiling, solid flat income, dotted sink). Colours from `templates/interactive-tokens.css`. No animation under `prefers-reduced-motion`.
