# MMO309 · Week 06 — Botting economics

**Why this matters:** A bot farm is a small business with a spreadsheet. It buys accounts, runs them until they are banned, and sells what they farmed. You will never ban every bot. You can make the spreadsheet come out negative, and then the farm shuts itself down. This week you build that spreadsheet, find the one inequality that decides whether farming pays, and compare the levers you have to break it, including a few that have nothing to do with detection.

**You will be able to:**
- Compute a bot account's expected profit from its margin per day, its setup cost, the detection rate and the ban-wave interval.
- Derive the break-even lifetime `A / m` and use it to judge whether a detection or policy change will stop farming.
- Compare defender levers (detection, wave timing, account cost, gold price, gold per hour) by how much each moves the farm's profit.
- Predict how an operator adapts to detection pressure, and how prices respond when bots disappear.

**Before class:** Hoglund, G. & McGraw, G. (2007), *Exploiting Online Games*, chapter 7 ("Building a Bot"), pp. 185-200 only, read for how a bot is structured, not how to write one. Read the RuneScape Wiki page "ClusterFlutterer" (10 minutes). Reread section 3 of [MMO304 week 11](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md), the farmer's cost per gold.

**Prerequisites from earlier courses:** [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (the token price ceiling and the farmer's cost per gold). [MMO304 week 3, faucets and sinks](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) (a bot is a faucet). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (a daily detection chance `d` means an expected wait of `1/d` days). From this course, [week 1](w01-threat-modeling-for-games.md) (attackers run a business; the Glider figures) and [week 5](w05-memory-editing-and-client-integrity.md) (why a ban wave waits).

**Interactive:** [Bot farm profit](../examples/w06-bot-farm-pnl.html). Keep it open during section 2.

---

## 1. The farm as a business

A **bot** is software that plays the game in place of a person. A **bot farm** runs many bot accounts at once, usually on rented servers, to collect gold or items for sale. The people who run farms are **operators**. They are not the same people as the **bot vendors** who sell botting software to ordinary players, though both show up in your logs. Week 1 told the vendor's story through Glider. This week is about the operator.

An operator's costs and income fit on one card:

| Item | Symbol | Teaching value | What it covers |
|---|---|---|---|
| Gold farmed per bot-hour | `g` | 20,000 gold | depends on your content and drop rates |
| Hours botted per day | `H` | 20 | a bot does not sleep |
| Black-market price of gold | `p` | $1.50 per 100,000 gold | set by buyers, capped by any token |
| Running cost per day | `c` | $1.00 | server share, residential proxy, subscription if any |
| Setup cost per account | `A` | $35 | account or box price, verification, the bot time or labor to reach a farming spot |
| Daily chance detection finds the bot | `d` | varies | your detection |
| Days between ban waves | `W` | varies | your policy |

These numbers are invented for teaching, chosen to be in a plausible range and easy to compute with. Real ones vary by game and year. What makes them useful is that every one of them is something a designer or a security team can move.

From the card:

```
revenue per day   = g × H × p / 100,000  = 20,000 × 20 × 1.50 / 100,000 = $6.00
margin per day  m = revenue − c           = $5.00
```

So a bot earns $5 a day for as long as it lives. It cost $35 to start. The whole question of botting economics is whether it lives long enough.

## 2. Worked example: the break-even lifetime

### The hook

On 25 October 2011 Jagex shipped ClusterFlutterer, an update that stopped injection and reflection bots from working in RuneScape. Jagex believed those were 98% of the bots in the game. At RuneFest that weekend, Jagex's Mark Gerhard said 7.7 million accounts had been banned for gold farming in four days. The RuneScape Wiki records a second number that tells you more about the business than the first. New account creation from the regions where most farms had operated fell by 99.9%, from hundreds of thousands a month to under a thousand.

Operators lost accounts, and they also stopped buying new ones. Meanwhile the prices of goods used for skill training rose. Trout, a cheap fish players use to train skills, had sold for 27 coins. By February 2012 it sold for 155.

Why did the new accounts stop, when the bans alone were a cost operators had always paid? Because the update broke the spreadsheet itself. The model shows which cell.

### The model

A bot account is detected on a random day. If the chance of detection is `d` each day, the expected wait is `1/d` days (MA102 week 7). If you ban in waves every `W` days, a detected bot survives until the next wave, on average another `W/2` days. So:

```
expected lifetime  L = 1/d + W/2
expected profit      = m × L − A
the farm pays when   L > A / m
```

- `m` is the margin per day, revenue minus running cost.
- `A` is the setup cost of one account.
- `d` is the daily detection chance, so `1/d` is mean days to detection.
- `W` is the ban-wave interval, 0 for bans on detection.
- `A / m` is the **break-even lifetime**, the number of days a bot must survive to pay back its setup cost.

With the card's numbers, `A / m = 35 / 5 = 7` days. Every bot has to live a week. That single number is what the rest of this lecture is about. Detection attacks the left side of `L > A/m`. Everything else you can do attacks the right side.

### Numbers you can check

```python
def farm(d, W, gold_per_hour=20_000, hours=20, price=1.50, run_cost=1.00, setup=35.0):
    """Expected profit of one bot account, in dollars.
    d: chance per day that detection finds the bot; W: days between ban waves."""
    revenue = gold_per_hour * hours / 100_000 * price   # dollars per day
    margin = revenue - run_cost
    lifetime = 1 / d + W / 2                             # expected days until the ban
    return margin * lifetime - setup

print("detection d   lifetime   W=0     W=7    W=14")
for d in (0.02, 0.05, 0.1, 0.2, 0.5, 1.0):
    row = "  ".join(f"{farm(d, W):6.1f}" for W in (0, 7, 14))
    print(f"   {d:4.2f}       {1/d:5.1f}   {row}")
```

It prints:

```
detection d   lifetime   W=0     W=7    W=14
   0.02        50.0    215.0   232.5   250.0
   0.05        20.0     65.0    82.5   100.0
   0.10        10.0     15.0    32.5    50.0
   0.20         5.0    -10.0     7.5    25.0
   0.50         2.0    -25.0    -7.5    10.0
   1.00         1.0    -30.0   -12.5     5.0
```

The "lifetime" column is `1/d`, before any wave delay. Check two cells. At `d = 0.1` and `W = 0`, `L = 10`, profit `5 × 10 − 35 = $15`. At `d = 1` and `W = 14`, `L = 1 + 7 = 8`, profit `5 × 8 − 35 = $5`.

Read the table in three passes.

1. **Detection has a threshold.** Going from `d = 0.02` to `d = 0.05` cuts profit from $215 to $65 and the farm still thrives. Crossing `1/d = 7` is what matters. Below that line, and only there, farming loses money.
2. **Ban waves add days.** A 14-day wave adds seven days to every bot's life. With these numbers that is exactly the break-even lifetime. The bottom-right cell says that with fortnightly waves, a farm is profitable even if you detect every bot on its first day.
3. **The same `d` looks different to each side.** "We catch 20% of bots every day" sounds like a strong detection team. With weekly waves the operator still clears $7.50 per account, and a farm of 500 accounts clears $3,750 per account generation.

Week 5 found that for cheats, a short wave delay can leave less cheating in the game. For bots the same delay pays the operator. The two results do not conflict. A cheater gains nothing you can count per day, and your signature is the scarce thing. A bot's whole purpose is to earn per day, and every day it lives is money. The design answer is in section 4.

### A visual you can move

Open the interactive. The left panel is a dashboard tile of the kind a detection team reports: "bots detected per day", `d` as a percentage, big and green. The right panel plots expected profit per account against mean days to detection `1/d` (log scale, half a day to 100 days), with one curve for each wave interval and a horizontal zero line. The break-even lifetime `A/m` is a vertical marker.

Drag `d` up until the tile reads 50% a day. The tile looks like victory. Then look right. With `W = 14` the curve is still above zero. Now leave `d` alone and drag the setup cost `A` from $35 to $70, or the gold price down by half. The break-even marker jumps right, and the dot on every curve, at the same 50% a day, sinks below zero. The two views show the same farm. Only one of them tells you whether it closes.

### Cross-game recognition

**RuneScape, ClusterFlutterer (October 2011).** The hook. [Week 5](w05-memory-editing-and-client-integrity.md) read the same update as ban timing; here it is a cost sheet. The update set `g` to zero for the bot types Jagex believed were 98% of all bots, since a bot that cannot read the game state farms nothing. With `m < 0`, `L` no longer matters. Every account's `A` was lost at once, and no new `A` was worth paying. That is why account creation from farm regions fell by 99.9%: operators ran the model and stopped entering. The rise in trout prices is the market side of the same event, which section 3 picks up.

**MMO304's farmer's cost per gold.** MMO304 week 11 wrote the farm's condition in different units. The farmer's cost per gold is `(h + A/t) / g`, and the black market survives when that cost is below the price. Multiply both sides by `g × t` and rearrange: `(p × g − h) × t > A`. Here `p × g − h` is the hourly margin and `t` the lifetime in hours. It is `m × L > A` again, in hours instead of days. MMO304 used it to price gold against a token. This week uses it to choose defenses.

**New World (November 2021).** About a month after reports that Steam family sharing let players run New World without buying it, Amazon disabled family sharing for the game, citing an increase in bots, gold sellers and ban evaders. Before the change, a banned bot could return on a shared library at nearly zero `A`. After it, every new bot needed its own copy of the game. [Week 14](w14-case-studies.md) examines this case as a whole.

**Steam accounts and VAC (May 2016).** Valve began banning accounts registered with the same phone number as a banned account, and a phone number used on a banned account could not be registered again for three months. For a ban evader that adds a fresh phone number to `A`. Phone verification is a common `A` lever because it is cheap for a real player, who already has one number, and costly for an operator who needs hundreds.

**Glider (2005 to 2008).** Week 1 showed the vendor side. Glider Elite sold "additional protection from game detection software" for five dollars a month. In this model, the vendor was selling `L`. A customer paid to push `1/d` up, which only makes sense because a longer life is worth more than five dollars a month to them.

Five cases, one inequality. When you read about any anti-bot change, ask which term it moved: `g`, `H`, `p`, `c`, `A`, `d` or `W`.

### Eyes-open design judgment

- **Aim for the threshold, not the maximum.** Detection effort that moves `1/d` from 50 days to 20 feels like progress and changes nothing for the operator. Effort that moves it from 10 to 5 closes farms. Track `A/m` next to your detection metrics.
- **Every `A` lever also taxes honest newcomers.** A box price, phone verification or a trade lock on new accounts raises `A` for bots and friction for real players, some of whom leave. RuneScape's trade limit (MMO304 week 11) is the cautionary tale. Measure new-player conversion before and after.
- **Cutting `g` hits your grinders too.** Diminishing returns on repeating the same farm spot hurt bots most, since bots repeat. They also hurt a human who likes one spot. Aim cuts at patterns only a bot sustains, like 20 hours a day in one place.
- **Do not let the wave carry the margin.** If you delay bans for the reasons in week 5, cut the margin during the delay. A flagged account whose trades are held or whose drops stop earns nothing, and still learns nothing. That is a silent penalty, which [week 12](w12-legal-and-ethical-considerations.md) treats as an ethics question, not only a design one.
- **Watch the price.** A successful purge raises the price of whatever bots supplied, which raises `m` for any bot that survives. Section 3 shows by how much.

### Check yourself (worked example)

1. With the card's numbers, what daily detection chance `d` makes a bot exactly break even when `W = 0`? When `W = 7`?
2. An operator switches to a cheaper proxy, cutting `c` from $1.00 to $0.50 a day. What is the new break-even lifetime? Does a `d = 0.2`, `W = 0` defense still close the farm?
3. A studio bans on detection (`W = 0`) and detects at `d = 0.25`. It then raises the account price so that `A` goes from $35 to $50. By how much does profit per account change, and is the farm open or closed before and after?

<details>
<summary>Answers</summary>

1. With `W = 0` you need `1/d = 7`, so `d = 1/7 ≈ 0.143` a day. With `W = 7`, `1/d + 3.5 = 7`, so `1/d = 3.5` and `d ≈ 0.286` a day. A weekly wave doubles the detection rate you need.
2. `m = 6 − 0.5 = 5.5`, so `A/m = 35 / 5.5 ≈ 6.4` days. At `d = 0.2`, `L = 5` days, below 6.4. Profit `5.5 × 5 − 35 = −$7.50`. Still closed, by a smaller margin.
3. Before: `L = 4`, profit `5 × 4 − 35 = −$15`, closed. After: `5 × 4 − 50 = −$30`, closed. Profit falls by exactly the $15 added to `A`. The farm was already closed, so the price rise only hurt honest newcomers. Check which side of `A/m` you are on before pulling a lever that has a cost.

</details>

## 3. The operator and the market fight back

The model so far holds the operator and the market still. Neither holds still.

### The operator adapts: bots that keep human hours

Detection systems look for inhuman behavior, and 20 hours a day in one spot is the least human thing a bot does. Suppose your detection chance grows with the square of the hours botted, `d = 0.01 × (H/8)²`, so a bot that plays 8 hours a day is found about once in 100 days and one that plays 16 is found four times as often. Each bot-hour earns `0.2 × $1.50 = $0.30`. The operator now chooses `H`:

```python
def profit_at_hours(H, d8=0.01, dollars_per_hour=0.30, run_cost=1.00, setup=35.0):
    d = d8 * (H / 8) ** 2            # detection per day grows with hours botted
    lifetime = 1 / d
    return (dollars_per_hour * H - run_cost) * lifetime - setup, lifetime

for H in (4, 6, 8, 12, 16, 20):
    profit, life = profit_at_hours(H)
    print(f"{H:2} h/day  lifetime {life:6.1f} days  profit {profit:7.2f}  gold/day {H * 20_000:7,}")
best = max(range(1, 25), key=lambda H: profit_at_hours(H)[0])
print("operator's best:", best, "hours a day")
```

It prints:

```
 4 h/day  lifetime  400.0 days  profit   45.00  gold/day  80,000
 6 h/day  lifetime  177.8 days  profit  107.22  gold/day 120,000
 8 h/day  lifetime  100.0 days  profit  105.00  gold/day 160,000
12 h/day  lifetime   44.4 days  profit   80.56  gold/day 240,000
16 h/day  lifetime   25.0 days  profit   60.00  gold/day 320,000
20 h/day  lifetime   16.0 days  profit   45.00  gold/day 400,000
operator's best: 7 hours a day
```

A rational operator throttles to about 7 hours a day. The farm still makes money. But each bot now adds 140,000 gold a day instead of 400,000, a 65% cut in the faucet, and the operator needs almost three times as many accounts, each paying `A`, to ship the same volume. Detection that never bans a single extra bot still shrinks the bot economy, by forcing bots to look human. That is also why bots get harder to tell from people over time. [Week 7](w07-bot-detection-behavioral-features.md)'s behavioral features are measuring a population that has already adapted to last year's detectors.

The model ignores that money in 178 days is worth less to an operator than money this week, which pushes the real optimum a little higher. The direction holds.

### The market adapts: prices rise when bots leave

Bots are a faucet (MMO304 week 3). Remove most of them and the goods they supplied become scarce, so prices rise. The trout that went from 27 to 155 coins after ClusterFlutterer is the textbook case. For the operators who survived, a higher price means a higher `m`. Suppose a purge halves bot supply and the black-market gold price rises by 50%, from $1.50 to $2.25 per 100,000. Revenue per day goes from $6.00 to $9.00, `m` from $5 to $8, and the break-even lifetime falls from 7 days to `35 / 8 ≈ 4.4` days.

So a purge that works makes the remaining bots more profitable, and invites new ones. Two practical consequences:

- **Anti-bot work is a level you hold, not a victory you win.** Plan staffing for the steady state after the purge, not the purge.
- **Pair a purge with a price cap.** A sanctioned token, MMO304 week 11's ceiling, stops the black-market price from rising as far after a purge, which keeps `m` low when supply is short.

## 4. Choosing a lever

Take one situation and compare every lever on it. Detection finds bots at `d = 0.2` a day and waves run weekly, so `L = 5 + 3.5 = 8.5` days and the farm makes $7.50 an account. Change one thing at a time:

```python
def farm(d, W, gold_per_hour=20_000, hours=20, price=1.50, run_cost=1.00, setup=35.0):
    margin = gold_per_hour * hours / 100_000 * price - run_cost
    return margin * (1 / d + W / 2) - setup, setup / margin

levers = {
    "baseline":                     {},
    "gold price halved":            {"price": 0.75},
    "setup cost doubled":           {"setup": 70.0},
    "gold per hour cut by 25%":     {"gold_per_hour": 15_000},
    "detection doubled (d = 0.4)":  {"d": 0.4},
    "ban waves off (W = 0)":        {"W": 0},
}
for name, change in levers.items():
    args = {"d": 0.2, "W": 7, **change}
    profit, breakeven = farm(**args)
    print(f"{name:30} profit {profit:6.2f}   break-even life {breakeven:4.1f} days")
```

It prints:

```
baseline                       profit   7.50   break-even life  7.0 days
gold price halved              profit -18.00   break-even life 17.5 days
setup cost doubled             profit -27.50   break-even life 14.0 days
gold per hour cut by 25%       profit  -5.25   break-even life 10.0 days
detection doubled (d = 0.4)    profit  -5.00   break-even life  7.0 days
ban waves off (W = 0)          profit -10.00   break-even life  7.0 days
```

Every lever closes this farm. They differ in what they cost you and who else pays:

| Lever | Moves | Who else pays | Typical cost to the studio |
|---|---|---|---|
| Better detection | `d` | honest players hit by false positives | engineers, forever; an arms race |
| Faster ban waves | `W` | nobody directly, but you lose week 5's signature protection | a policy change |
| Account cost | `A` | new honest players | lost conversions |
| Gold price | `p` | players who sell gold for tokens | a token system and its economics |
| Gold per hour | `g`, `H` | grinders who repeat content | design time, player complaints |

Two things stand out. The cheapest lever on this list is often `W`, a policy decision, and the most expensive is `d`, which never stops costing. And three of the levers work without identifying a single bot. A game designer who makes repetitive farming pay less, or a producer who adds phone verification to trading, is doing anti-bot work with no detector at all.

The best plans use several levers at once, because the operator's profit is a product and a sum. Halving `m` and halving `L` together cuts the revenue term to a quarter.

## In-class activity (25 minutes)

Groups of four. Each group gets a game card with its own numbers: gold per hour, price, running cost, setup cost, detection rate, wave interval, and one line about the game's players.

- **A:** Free-to-play MMO, no box price, `A = $3` (a fresh email and 40 minutes of bot leveling).
- **B:** Subscription MMO, `A = $40`, `c` includes a $15 monthly fee.
- **C:** Buy-to-play MMO with a token, gold price capped at $1.00 per 100k.
- **D:** Mobile MMO where most players grind the same spot for hours, so `g` cuts hit everyone.

1. Compute `m`, `A/m` and current profit per account (8 minutes).
2. Pick the two levers from section 4 that close the farm at the lowest cost to your game's honest players. Show the new profit (10 minutes).
3. Predict how the operator adapts, using section 3, and name the metric that would show it happening (7 minutes).

Expected output: three numbers, two levers with their new profit, and one adaptation with its metric, presented in two minutes.

## Common misconceptions

- **"More detection always means fewer bots."** Only when it crosses the break-even lifetime. Detection that keeps bots alive longer than `A/m` days leaves every farm open.
- **"Ban waves are always good because they catch more."** They catch more per signature and hand every bot extra days of income. For bots the delay can decide whether the farm pays.
- **"If we purge the bots, the problem is solved."** Prices rise, margins rise, and the break-even lifetime falls. The next generation of bots needs to live less time to profit.
- **"Anti-bot is the security team's job."** Economy designers set `g` and `p`, producers set `A`, and ops sets `W`. Most levers sit outside security.

## Check yourself

1. A bot farms 30,000 gold an hour for 18 hours a day. Gold sells for $1.00 per 100,000, running cost is $0.90 a day and setup is $24. Compute `m` and the break-even lifetime.
2. For that bot, detection is `d = 0.25` and waves run every 10 days. Is the farm profitable? What wave interval makes it break even?
3. After a purge, the gold price in question 1 rises to $1.60 per 100,000. Recompute the break-even lifetime and say whether the same defense still closes the farm.
4. In the hours model of section 3, the studio doubles `d8` to 0.02. Without computing every row, predict what happens to the operator's best `H` and to profit per account. Then check one row.
5. A colleague argues that a trade lock on accounts younger than 14 days "raises `A` for free". Using the model, say what it really changes, and name one honest group that pays for it.

<details>
<summary>Answers</summary>

1. Revenue `30,000 × 18 × 1.00 / 100,000 = $5.40`, `m = 5.40 − 0.90 = $4.50`, `A/m = 24 / 4.5 ≈ 5.3` days.
2. `L = 1/0.25 + 10/2 = 4 + 5 = 9` days, profit `4.5 × 9 − 24 = $16.50`. Profitable. Break-even needs `4 + W/2 = 5.33`, so `W ≈ 2.7` days. Weekly waves are already too slow.
3. Revenue `30,000 × 18 × 1.60 / 100,000 = $8.64`, `m = $7.74`, `A/m = 24 / 7.74 ≈ 3.1` days. With `W = 10`, `L = 9`, even more profitable. With `W = 0`, `L = 4 > 3.1`, still profitable. The defense that would have closed the old farm at `W ≤ 2.7` no longer does.
4. Best `H` stays at 7. Doubling `d8` halves every lifetime, so the revenue term `(0.30 × H − 1) × L` is halved at every `H` and its peak does not move. Profit falls by more than half, because `A` is subtracted after. Check `H = 8`: `L = 50` days, profit `(2.4 − 1) × 50 − 35 = $35`, down from $105. At `H = 7`, `d = 0.02 × (7/8)² ≈ 0.0153`, `L ≈ 65.3`, profit `1.1 × 65.3 − 35 ≈ $36.80`. The farm stays open. To shrink the faucet you need either a bigger push that turns profit negative, or a detector that punishes long hours more steeply.
5. It does not change the price of an account. It delays when an account can sell its gold, so the first 14 days produce no income. In the model that is like adding `14 × m` to `A` for accounts that would have lived longer than 14 days, and it kills accounts with `L < 14` outright. New honest players who want to trade with friends in their first two weeks pay for it.

</details>

## Lab / assignment hook

[Lab 06, the bot farm ledger](../labs/lab06.md). You get a synthetic ban log for 2,000 bot accounts with creation, detection and ban days. You estimate the detection rate from censored data, compute the farm's profit under the current wave policy, and recommend the cheapest combination of levers that closes it, with a 300-word memo. Your recommendation joins the course threat model (30%).

## Sources

- RuneScape Wiki, "ClusterFlutterer" (retrieved September 2026). 25 October 2011; injection and reflection bots stopped; Jagex's belief that they made up 98% of bots; 7.7 million accounts banned for gold farming between 25 and 29 October, as stated in a RuneFest session with Mark Gerhard; account creation from certain regions down 99.9% to as few as 953 a month; trout rising from 27 coins to 155 by February 2012. https://runescape.wiki/w/ClusterFlutterer
- Wikipedia, "New World: Aeternum" (the article on New World, retrieved September 2026). Family sharing disabled in November 2021, one month after reports of free access, citing an increase of bots, gold sellers and ban evaders.
- Wikipedia, "Valve Anti-Cheat" (retrieved September 2026). From May 2016, bans for accounts registered with the same phone number as a banned account, and a three-month bar on reusing that number.
- *MDY Industries, LLC v. Blizzard Entertainment, Inc.*, 629 F.3d 928 (9th Cir. 2010), statement of facts. Glider Elite at five dollars a month offering "additional protection from game detection software".
- MMO304 week 11 of this program, for the farmer's cost per gold and the token ceiling, with its own sources.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley. Page numbers from the publisher's table of contents (InformIT).

## Interactive spec: examples/w06-bot-farm-pnl.html

**The one insight:** a detection rate that looks strong on a dashboard can leave every farm profitable, because what decides farming is whether bots live longer than the break-even lifetime `A/m`. Levers that move `A/m` (price, setup cost, gold per hour) can close a farm without detecting a single extra bot.

**Layout.** Left: a dashboard tile. Right: the profit chart. Below: lever buttons and a copyable readout. On mobile, the chart comes first, then the tile, then controls.

**Dashboard tile.** Large number: "Bots detected per day: `d` as a percentage". Under it, smaller: "Mean days to detection: `1/d`". Color it green when `d ≥ 0.1` regardless of profit, on purpose, with a caption "what the detection team reports".

**Profit chart.** x-axis mean days to detection `1/d`, log scale from 0.5 to 100. y-axis expected profit per account in dollars. Three curves for `W = 0`, `W = 7`, `W = 14`, plus a fourth for the user's custom `W` if it differs. Horizontal zero line. Vertical marker at `A/m` labelled "break-even lifetime (W = 0)". A dot on each curve at the current `1/d`. Shade the region below zero.

**Controls.**
- `d` daily detection: 0.01 to 1.0, log slider, default 0.2.
- `W` wave interval: 0 to 30 days, step 1, default 7.
- `g` gold per bot-hour: 5,000 to 50,000, step 1,000, default 20,000.
- `H` hours per day: 1 to 24, default 20.
- `p` price per 100,000 gold: $0.25 to $5.00, step $0.05, default $1.50.
- `c` running cost per day: $0 to $5, step $0.10, default $1.00.
- `A` setup cost: $1 to $150, step $1, default $35.
- Lever buttons that apply section 4's one-at-a-time changes from the baseline and show the result: "halve price", "double setup", "cut gold/hour 25%", "double detection", "waves off". A "reset" button.

**Model.** `m = g × H × p / 100,000 − c`; `L = 1/d + W/2`; `profit = m × L − A`; break-even `A/m` (show "never" when `m ≤ 0`).

**Readout table** (copyable): `m`, `A/m`, `L`, profit per account, profit for a 500-account farm, and the `d` needed to break even at the current `W` (`1 / (A/m − W/2)`, or "no detection rate is enough" when `A/m ≤ W/2`).

**Test values.**
- Defaults: `m = 5.00`, `A/m = 7.0`, `L = 8.5`, profit $7.50, farm $3,750, break-even `d = 0.2857`.
- `d = 0.1, W = 0`: $15.00. `d = 1, W = 14`: $5.00. `d = 0.02, W = 14`: $250.00.
- `W = 14`, defaults otherwise: break-even `d` shows "no detection rate is enough" (`A/m = 7 = W/2`).
- Levers from baseline, each applied alone at `d = 0.2`, `W = 7`. The values are the resulting profit per account, not changes from $7.50: halve price −$18.00 (`A/m = 17.5`); double setup −$27.50 (14.0); cut gold/hour 25% −$5.25 (10.0); double detection −$5.00; waves off −$10.00.

**Accessibility.** All sliders keyboard operable with visible values. Curves distinguished by dash pattern and direct labels. A live region announces "farm profitable" or "farm closed" when the sign of profit changes. No animation under `prefers-reduced-motion`.
