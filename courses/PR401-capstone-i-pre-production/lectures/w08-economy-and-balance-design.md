# PR401 · Week 08 — Economy and Balance Design

**Why this matters:** Your live period in PR402 is four weeks long. An economy tuned for a game that runs for years will do nothing in four weeks: the big purchase nobody reaches, the sink that never fires, the price nobody pays. This week you write the economy and balance tables as numbers you can check against the live window, before a single price is typed into the game.

**You will be able to:**
- Write an economy one-pager that lists every currency, faucet, sink and transformation with a rate per hour of play.
- Compute the hours of play to afford each key purchase, and the week of the live period in which each player type reaches it.
- Compute how the money created in the live period splits across player types, and design a sink that reaches the players who hold most of it.
- Set balance targets as numbers (time to kill, death penalty, currency per hour) in one data table the game reads, so that a balance change is a data change.

**Before class:** Reread [MMO304 week 14, designing an economy from scratch](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w14-designing-an-economy-from-scratch.md), sections 1 and 2 (25 minutes). Reread [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) for the vocabulary. Look up the Diablo III auction house on Wikipedia and note when it opened and when it closed (10 minutes). Bring your week 1 player-type table (weekly hours for light, median, keen and heavy players) and your week 3 pillars and anti-pillars.

**Prerequisites from earlier courses:** [MMO304 week 4](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (money supply per capita and inflation). [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (economic telemetry). [MMO401 week 4](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w04-monetary-policy-tools-in-games.md) (policy levers). [MMO303 week 3](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) (effective HP and DPS). [MMO403 week 3](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w03-premium-currencies.md) (premium currencies, if your game sells anything). [Week 1 of this course](w01-pitch-development.md) (player types and the four-week live period).

---

## 1. The economy one-pager

Before you tune a number, write the economy on one page. MMO304 week 14 gives the full design order. For a capstone the page has five parts.

1. **Currencies.** Every currency and what it is for. Most capstones need one. A second currency needs a sentence saying what the first could not do.
2. **Faucets.** Every way currency enters the game: quest rewards, mob drops, vendor sales of loot. Each with a rate in currency per hour of the activity.
3. **Sinks.** Every way currency leaves: repairs, vendor purchases, fees, taxes. Each with a rate per hour, or a one-off price.
4. **Transformations.** Where items become other items (crafting) or currency becomes items (vendors). MMO304 week 3 explains why these matter as much as faucets and sinks.
5. **Trade.** How players exchange with each other: a trade window, mail, a market. Each channel you open is a channel for bots and scams, as MMO309 week 10 showed. Open only the ones a pillar needs.

The rates are guesses this week. Label each one with its source: "prototype 2, 9 testers" or "assumed". Week 12's vertical slice replaces the guesses with telemetry, so every faucet and sink needs an event in the telemetry plan (DB201 week 10).

## 2. Price in hours of play

A live MMO can price a house at a month of play because it has years. Yours has four weeks. So write every important price twice, in currency and in **hours of play to afford**:

```
net rate     n = Σ faucets − Σ recurring sinks          currency per hour of play
hours        T = price / n
week reached w = T / h                                  for a player who plays h hours a week
```

A purchase is only in the game for the players who reach it inside the live period. If `w` is above 4 for the median player, the median player never sees it, and the sink attached to it never fires for them.

## 3. Balance targets are numbers

Balance design in pre-production is not tuning. It is choosing targets that the tuning will aim at, so that the team can argue about targets instead of about feel. Write them as a table:

| Target | Value | Why |
|---|---|---|
| Time to kill a valley creature, solo, player-made tier 1 gear | 8 to 12 s | Long enough to use three abilities, short enough that gathering trips keep moving |
| Time to kill a player in the same gear tier | 12 to 18 s | Long enough to run for the town gate or call for help (P3: danger has a price, not instant death) |
| Share of carried goods dropped on death | 30% | Enough to hurt, little enough that players still carry goods to market |
| Hours of use before a tier 1 tool breaks | 3 | Keeps crafters' orders flowing (P1) without making tools feel disposable |
| Town raid length | 10 to 15 min | Fits one evening session with time to trade afterward |
| Currency per hour of play | 150 | Section 4 sizes this |

These values are *Emberfall*'s choices, not rules. MMO303 week 3 shows how to turn a time-to-kill target into health and damage numbers with effective HP and effective DPS. The point this week is that every row has a number and a reason, and the reason names a pillar where it can.

Put the targets and the derived values in one data table the game reads at start, such as a CSV or JSON file in the repository. A balance change then becomes a one-line data change with a review, not a code change. PR402's patch week depends on this.

## 4. Worked example: who reaches the house plot?

### The hook

Diablo III launched in 2012 with two global auction houses: one for gold and one for real money, which opened in June 2012. On 17 September 2013 Blizzard announced that both would close, and they shut on 18 March 2014. The game's former director, Jay Wilson, had said in 2013 that the auction house "really hurt" the game. Players could buy upgrades faster than they could find them, so the loot the game was built around stopped mattering.

*Emberfall*'s week 3 anti-pillar "no global market" is the same lesson learned in advance. The deeper lesson is that the economy decides what the rest of the game is for. If currency buys everything, currency is the game. If the key purchase takes longer than the live period, the purchase is decoration. You can check both before launch with one number per purchase: the hours of play to afford it.

### The model

Use the section 2 model with the four player types from week 1:

| Player | `h` (hours per week) | Hours in 4 weeks | Share of launch players |
|---|---|---|---|
| Light | 3 | 12 | 40% |
| Median | 5 | 20 | 35% |
| Keen | 12 | 48 | 20% |
| Heavy | 25 | 100 | 5% |

The shares are *Emberfall*'s guess for 100 players at launch.

```
money created in the live period  M = Σ (players of type i × hours of type i × n)
share of M held by type i         = players_i × hours_i / Σ players × hours
```

The second line assumes everyone earns at the same rate per hour, so money follows hours.

### Numbers you can check

*Emberfall*'s currency is the mark. Pillar P1 means no vendor sells gear, so marks come in from two faucets: waystation contracts (bounties on valley creatures and deliveries) at 90 marks per hour, and salvage and raw goods sold to the waystation at 60. In the draft economy (design A), recurring sinks are the town upkeep share and death insurance premiums, 30 marks per hour together. The one big purchase is a house plot inside a held town, at 5,000 marks. Players trade gear with each other at town market stalls.

Design B keeps the faucets, raises the upkeep share, adds tool repair fees at the town forge and prices insurance per trip, so recurring sinks take 70 marks per hour. It prices the house plot at 1,200.

| | Design A | Design B |
|---|---|---|
| Net rate `n` (marks per hour) | 150 − 30 = 120 | 150 − 70 = 80 |
| House plot price | 5,000 | 1,200 |
| Hours to afford `T` | 41.7 | 15.0 |
| Light (12 h): reaches it in week | never | never (week 5) |
| Median (20 h) | never | 3.0 |
| Keen (48 h) | 3.5 | 1.25 |
| Heavy (100 h) | 1.7 | 0.6 |
| Marks left at the end, median | 2,400 | 400 |
| Marks left at the end, heavy | 7,000 | 6,800 |
| Money created, 100 players | 316,800 | 211,200 |

Check two cells by hand. Design A, keen: `T = 5,000 / 120 = 41.7` hours, and `41.7 / 12 = 3.47` weeks. Design B, median: `T = 1,200 / 80 = 15` hours, and `15 / 5 = 3.0` weeks. Money created in B: hours played are `40 × 12 + 35 × 20 + 20 × 48 + 5 × 100 = 2,640`, times 80 is 211,200.

Read it.

- **Design A's house plot is decoration.** Three players in four never see it. The median player ends the live period with 2,400 marks and nothing to spend them on. The sink the team designed around fires for a quarter of the players, and P2 (towns are held together) loses its main reason to join a town.
- **Design B puts the purchase in week 3 for the median player.** That gives the median player a goal in weeks 1 and 2 and a reason to be in a town before the end. The light player still misses it. The team decides to accept that and give light players a town banner at 400 marks (5 hours).
- **Neither design touches the heavy player's pile.** In both, the heavy player ends with about 7,000 marks. Keen and heavy players are 25% of launch players but play 55% of the hours (`(960 + 500) / 2,640`), so they hold about 55% of the money. Every market stall price will be set by them.

So design B needs one more line: a **repeatable sink that scales with play**, so that the players with the most money spend the most. *Emberfall* adds a market stall fee of 5% of each sale, paid by the seller and removed from the game, and a dye vendor with unlimited colors at 300 marks each. Both cost almost nothing to a light player who rarely sells and never dyes. MMO304 week 14 shows how a sink like this sets its own ceiling on hoarding.

### Cross-game recognition

- **World of Warcraft Token.** When it launched in the Americas in April 2015 at 30,000 gold, the token put a gold price on 30 days of game time. In this week's terms, the studio chose `T` for a purchase by setting its price in gold and let the market adjust it. MMO304 week 4 follows its price over time.
- **Old School RuneScape Grand Exchange tax.** The trading post charges a fee on sales, 1% from December 2021 and 2% since May 2025, capped at 5 million coins per item, and most of it is removed from the game. It is a sink that scales with trade volume, so it lands on the players who trade most. *Emberfall*'s stall fee is the same sink at capstone scale.
- **Diablo III after March 2014.** Removing the auction house raised the hours to get an upgrade back to the hours to find one. The design moved `T` for power back to where the loot game needed it.

### Eyes-open judgment

The model assumes everyone earns at the same rate. They do not. Heavy players learn the best contract route and earn more per hour, so the real split of money is more skewed than 55%. Your vertical slice telemetry should record marks earned per hour by player so you can see the real spread.

Pricing the big purchase for the median player has a cost. The heavy player buys it on day 4 and has nothing to chase. Decide which player you are designing the live period for, as week 1 asked, and say what the heavy player does after the plot. A second, larger purchase for the top 5% is cheap to add if it gives no power, which *Emberfall*'s anti-pillars already require.

Finally, four weeks is too short for inflation to matter much, and too short to fix it if it does. Prefer sinks that work from day 1 over ones that need a price history to tune.

## 5. From one-pager to data

By the end of the week the economy and balance live in the repository as data:

- `data/economy.csv`: every faucet and sink with its rate, source and telemetry event name.
- `data/prices.csv`: every priced item with the player type it targets and the week it should be reached.
- `data/balance.csv`: the targets from section 3 and the derived stats.

The lab 07 checker checked your server. The lab 08 checker checks these tables against the live window. Teams that keep the tables in data will change a price in PR402 with a one-line pull request and a rerun of the checker. Teams that hard-code prices will change them with a rebuild.

## Studio session plan

Week 8 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:25 | Economy one-pager: each team lists currencies, faucets, sinks, transformations and trade channels | One page, rates labelled with sources |
| 0:25-1:00 | Hours-to-afford table for every priced item, four player types (lab 08 steps 2 to 4) | `prices.csv` and checker run |
| 1:00-1:10 | Break | |
| 1:10-1:40 | Money split: who holds the money at the end, and which sink reaches them | A repeatable sink added or a reason why not |
| 1:40-2:20 | Balance targets: time to kill, time to die, boss length, with MMO303 effective HP | `balance.csv` with targets and reasons |
| 2:20-2:45 | Cross-team audit: another team tries to find the purchase nobody reaches and the exploit in your trade channel | List of findings |
| 2:45-3:00 | Telemetry: every faucet and sink gets an event name for the vertical slice | Events added to the telemetry plan |

## Deliverables

Due at the start of week 9, in `docs/economy.md`, `data/` and `preproduction/week08/`:

1. **Economy one-pager** with all five parts and a source label on every rate.
2. **Price and flow tables** in the [lab 08](../labs/lab08.md) format. The checker `economy_check.py` must print `PASS`.
3. **Balance targets table** with at least six rows, each with a value and a reason.
4. **Telemetry list**: one event per faucet and sink, with the properties that let you compute currency per hour per player.

## Common failure modes

- **Prices copied from a game that runs for years.** A 5,000-mark house plot in a four-week world. Price in hours of play first.
- **Sinks that only reach the median.** Repairs and fees scaled to average play do nothing about the heavy player's pile. Add one sink that grows with activity.
- **A market because MMOs have markets.** Each trade channel is a place for bots, scams and duplication bugs. Open the ones a pillar needs.
- **Balance by feel.** "Combat should feel punchy" gives the tuner nothing. Write a time to kill.
- **Hard-coded numbers.** Prices in code mean a rebuild for every change in PR402. Put them in data.
- **No events for flows.** In week 12 you will want currency per hour by player. If the events are not in the plan, the data will not exist.

## Review checklist

The instructor checks in the submission and at the week 9 stand-up:

- [ ] Every faucet and sink has a rate per hour and a source label.
- [ ] Every priced item has a target player type and target week, and `economy_check.py` prints `PASS`.
- [ ] The key purchase is reached by the median player inside the live period, or the team explains why not.
- [ ] The money split by player type is computed, and at least one sink scales with activity.
- [ ] The balance table has at least six targets, each with a value and a reason.
- [ ] Economy and balance values live in data files the game reads.
- [ ] Each faucet and sink has a telemetry event.

## Sources

- Wikipedia, "Diablo III" (accessed September 2026). Real-money auction house opened in June 2012; closure of both auction houses announced 17 September 2013 and carried out on 18 March 2014; Jay Wilson's 2013 remark that the auction house hurt the game. https://en.wikipedia.org/wiki/Diablo_III
- Old School RuneScape Wiki, "Grand Exchange" (accessed September 2026). Tax of 1% from 9 December 2021 and 2% from 29 May 2025, capped at 5 million coins per item; most of it removed from the game. https://oldschool.runescape.wiki/w/Grand_Exchange
- MMO304 week 4 of this program, for the WoW Token's Americas launch on 7 April 2015 (patch 6.1.2) at 30,000 gold, sourced there to Warcraft Wiki.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press. Background on faucets, sinks and money supply.
- The *Emberfall* rates, prices, player shares and balance targets are invented for teaching and continue weeks 1 to 7. The four player types and the four-week live period come from week 1 of this course.
