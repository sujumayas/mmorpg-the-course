# MMO304 · Week 02 — Value: Functional, Hedonic, Social

**Why this matters:** Players pay for items for different reasons. The reason decides how long the item keeps its value, whether selling it in a store will anger your players, and whether a patch will wipe it out overnight. If you cannot say which kind of value an item carries, you cannot predict what your next patch does to its price.

**You will be able to:**
- Decompose an item's value into functional, hedonic and social parts and estimate each in gold.
- Compute an item's social value from the share of players who own it, and predict how it changes as ownership spreads or the item is retired.
- Predict the shape of an item's value over a content cycle from the mix of its three parts.
- Critique a store or reward plan by naming which kind of value it sells and who loses when it does.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), chapters 2 and 3, "Theories of Human Behavior" and "Goods: Material, Digital, Virtual". Lehdonvirta, V. (2009), "Virtual item sales as a revenue model: identifying attributes that drive purchase decisions", *Electronic Commerce Research* 9(1-2), pp. 97-113.

**Prerequisites from earlier courses:** [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (reading `log2` as "how many halvings"). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication by a fixed factor). [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (tier shelf life). [Week 1 of this course](w01-why-virtual-economies-exist-artificial-scarcity.md) (artificial scarcity and fixed supply).

**Interactive:** [Value over time: three items, three reasons their value moves](../examples/w02-value-over-time.html)

---

## 1. Three reasons to want a thing

A RuneScape partyhat is a paper hat. It adds nothing to combat. It first appeared in Christmas crackers on a single day in December 2001, and partyhats now trade for billions of coins. Meanwhile, the best weapon from a raid tier in almost any MMO loses most of its price the week the next tier opens, even though it still hits exactly as hard.

The hat that does nothing holds its value. The weapon that does a lot loses it. To explain that, you need to split "value" into parts. This course uses three.

- **Functional value** is what the item lets you do: more damage, more speed, more bag space, a shortcut. It is the value a spreadsheet can measure.
- **Hedonic value** is the pleasure of the item itself: how it looks, sounds and feels to use. It is personal. Your enjoying a mount's animation does not reduce mine.
- **Social value** is what the item says about you to other players: that you were there, that you are rich, that you beat something hard. It exists only because others can see the item and most of them do not have it.

**Value** here means the most a player would give up to get the item, measured in gold. Economists call this **willingness to pay**. It differs from **price**, which is what the item actually trades for, and from **cost**, which is what it took to make (week 1's `w × T`). Price is set where buyers' willingness to pay meets sellers' costs, which is week 6's topic. This week is about the buyer's side.

The split matters because each part responds to different events. A patch changes functional value. Nothing much changes hedonic value. Other players' behaviour changes social value. Lehdonvirta's 2009 paper on why players buy virtual items is a good place to see the range of item attributes that feed each part. Read it for that list, and then use the model below to put numbers on it.

### Functional value runs on the developer's clock

Functional value is always relative. A sword's damage matters compared to the best sword you could otherwise have. When the developer adds a better tier, every older item's functional value drops, whether or not a single player chose to sell it. GD203 week 14 measured a tier's **shelf life**, the time until a new tier makes it obsolete. From the economy's side, shelf life is the half-life of functional value. The developer sets it, usually on a patch schedule.

In PvE, functional value is not rival: my sword does not make yours weaker. In PvP it partly is. If everyone gets the same power boost, nobody's win rate moves. Keep that in mind when we reach stores in section 4.

### Hedonic value is steady and personal

Hedonic value is the part that survives patches. A mount that looks great still looks great after the next expansion. It can fade as a player tires of it, and it differs a lot between players. One player loves a glowing cloak and another finds it garish. As a first model we treat it as a constant for a typical buyer.

### Social value is a share of the crowd

Social value depends on who else owns the item. A mount every player has says nothing about you. A mount one player in a thousand has says a lot. Economists call a good like this **positional**: its value comes from your position relative to others. Positional value is zero-sum. When one more player gets the item, every existing owner's item says slightly less.

## 2. Worked example: the hat, the sword and the mount

### The hook

Why does a tradeable paper hat gain value for twenty years while a raid weapon collapses in a week? Let's write one model that puts all three parts into gold, and then watch three items move through two years of a live game.

### The model

An item's value to a typical buyer at week `t` is the sum of its three parts:

```
V(t) = F(t) + H + S(t)

F(t) = F0          before the next tier releases (week t_R)
       F0 × r      after it

S(t) = s × log2(1 / f(t))

f(t+1) = f(t) + q × (1 − f(t)) − c × f(t)
```

- `V(t)` is the item's value in gold at week `t`.
- `F0` is its functional value while it is the best available. `r` is the share left after the next tier arrives (0.1 means it keeps 10%). `t_R` is the week the next tier releases.
- `H` is hedonic value in gold, held constant.
- `f(t)` is the share of active players who own the item, between 0 and 1.
- `s` is the gold value of one "halving" of ownership. `log2(1/f)` counts how many times you would halve the whole population to get down to the owners. At `f = 1` (everyone owns it) social value is zero. At `f = 1/2` it is `s`. At `f = 1/1024` it is `10 × s`.
- `q` is the weekly chance that a non-owner acquires the item (0 for an item that can no longer be obtained).
- `c` is the weekly share of active players who quit and are replaced by new players, who start as non-owners.

The `log2` form is a modelling choice, not a law. It says that each halving of the ownership share adds the same amount of prestige. Going from "half the server has one" to "a quarter has one" adds as much as going from "one in 500" to "one in 1,000". That matches how players talk about rarity ("one in a thousand", "one per server"), and it keeps social value finite for any real item. You will test a different form in the lab.

The ownership update says two things happen each week. Some non-owners get the item (`q × (1 − f)`). Some owners quit and are replaced by newcomers who do not have it (`c × f`). If `q` is zero, the share can only shrink, by a factor `(1 − c)` each week.

### Numbers you can check

Use `s = 1,000` gold per halving and churn `c = 2%` per week. Three items:

- **Tier sword:** `F0 = 20,000`, `r = 0.1`, next tier at week 26, `H = 500`. It starts owned by 1% and non-owners get it at `q = 2%` a week.
- **Store mount (still obtainable):** `F = 0`, `H = 3,000`. It starts at 1% ownership, `q = 3%`.
- **Retired event mount:** `F = 0`, `H = 3,000`. Owned by 0.1% (10 players out of 10,000) when the event ended at week 0. `q = 0`.

Values rounded to the nearest gold:

| Week | Sword `f` | Sword `S` | Sword `V` | Store mount `f` | Store mount `V` | Retired mount `f` | Retired mount `V` |
|---|---|---|---|---|---|---|---|
| 0 | 1.0% | 6,644 | 27,144 | 1.0% | 9,644 | 0.100% | 12,966 |
| 13 | 21.2% | 2,239 | 22,739 | 29.7% | 4,751 | 0.077% | 13,345 |
| 26 | 33.0% | 1,597 | 4,097 | 44.5% | 4,170 | 0.059% | 13,724 |
| 52 | 44.1% | 1,180 | 3,680 | 55.9% | 3,839 | 0.035% | 14,481 |
| 104 | 49.3% | 1,020 | 3,520 | 59.7% | 3,744 | 0.012% | 15,997 |

Check a few by hand. At week 0 the sword has `f = 0.01`, so `S = 1,000 × log2(100) = 6,644`, and `V = 20,000 + 500 + 6,644 = 27,144`. After one week the store mount's share is `0.01 + 0.03 × 0.99 − 0.02 × 0.01 = 0.0395`. The retired mount's share at week 52 is `0.001 × 0.98^52 = 0.00035`, and `log2(1 / 0.00035) = 11.48`.

Read the three stories off the table.

- The sword loses most of its social value in the first quarter as players catch up, then loses 18,000 of functional value in a single week when the next tier arrives. Its value drops by 82% between weeks 13 and 26. Nothing about the sword changed. The developer's calendar did.
- The store mount starts high on novelty, then settles toward a floor. Its share cannot pass `q / (q + c) = 0.03 / 0.05 = 60%`, because quitting owners balance new buyers there. At 60% ownership its social value is `1,000 × log2(1/0.6) = 737`, so it settles near `3,000 + 737 = 3,737`.
- The retired mount gains value every week without anyone touching it. Owners quit and newcomers can never get one, so the share halves every `ln 2 / −ln(0.98) ≈ 34.3` weeks, and each halving adds 1,000 gold of social value. Over two years that is three halvings and about 3,000 gold.

### The visual

Open the interactive. The top view plots ownership share `f(t)` for the three items on a log scale. The bottom view plots `V(t)` as stacked areas of `F`, `H` and `S` for whichever item you select. Watch the retired mount's `f` line slope steadily down on the log scale while its value line climbs. Then move the "next tier" slider and watch the sword's cliff move with it. Try setting the retired mount's `q` above zero ("re-release the mount"): the share climbs toward `q / (q + c)` and the value built over years drains away within weeks.

### Cross-game recognition

**World of Warcraft, the gates of Ahn'Qiraj (patch 1.9.0, January 2006).** Each server ran a war effort, and the player who rang the Scarab Gong received the Black Qiraji Resonating Crystal, a mount summoned from it. Once the event ended the mount could not be obtained by any means, and new realms opened with the gates already unlocked. This is the retired mount in our model with `q = 0` and a tiny starting `f`, about one owner per server. Every new player who has joined since then has lowered `f` and raised the item's social value. Note that the crystal cannot be traded, so there is no market price to observe. The value is real to its owner even though the model's number is never paid by anyone.

**RuneScape partyhats (Christmas crackers, 25 December 2001).** These are tradeable, so the model's value shows up as a price. `F = 0` because the hat has no combat use. Supply was fixed on a single day, which makes `q = 0`. Over two decades the RuneScape population turned over many times, so the owner share fell and partyhats now trade for billions of coins. The model also explains why RuneScape players still talk about the 2003 duplication glitch. Duplication raises `f`. Every extra hat subtracted social value from every existing hat.

**Path of Exile (2013 onward).** Grinding Gear Games has said its goal is a free game funded by what it calls "ethical micro-transactions", and its store mainly sells cosmetic item skins. In our model, the store sells `H` and `S` and leaves `F` to be earned in play. The game's functional value lives in its currency items, which have their own uses (upgrading or rerolling items) and are traded by barter rather than for gold. It is the same three-part split, with the developer choosing which parts it will sell for money.

Three games, one model. When you look at any item, ask which of `F`, `H` and `S` carries its value, and which event will move each one.

### Eyes-open design judgment

- **Decide which value your store sells.** Selling `F` for money ("pay to win") lowers the functional value of everything players earned in play, and in PvP it is zero-sum, since your gain is my loss. Selling `H` harms nobody's items. Selling `S` is delicate: every sale lowers existing owners' prestige.
- **Retiring an item is a promise.** A limited-time item gains value only while `q` stays at 0. Re-releasing it drains the value its owners built, often years of it, in a few weeks. If you might re-release, say so up front.
- **Limited-time items create pressure.** Low `f` at launch makes an item look valuable, and a closing window pushes players to act now. That can be a fun event or a manipulative one. The model shows the pressure is real, which is exactly why you should use it sparingly.
- **Functional value is your sink for obsolescence.** Tier releases wipe out `F` on schedule. That keeps players chasing new items and removes old value from the economy. Week 8 treats obsolescence alongside item decay as one of your strongest sinks. The cost is that players feel their work was erased.

## 3. Using the split: reading prices and planning patches

### Separating the parts from market data

You rarely know `F`, `H` and `S` directly, but you can separate them with prices. Three tricks:

- **Compare near-identical items.** Two items with identical stats and different looks differ only in `H` and `S`. Two recolours of the same model with different drop rates differ mostly in `S`. The price gap is the part that differs.
- **Watch a patch.** When a new tier releases, the drop in an old item's price is roughly its lost functional value, `F0 × (1 − r)`.
- **Watch a re-release.** When an old cosmetic returns to a shop, the drop in its price is mostly the social value lost as `f` rises.

In the sword example, the week-26 drop from 22,739 (week 13) to 4,097 mixes two effects: 18,000 of lost `F` and 642 of lost `S`. If you only had prices at weeks 25 and 26, the social part would be tiny and the step would be almost all functional. The closer the two observations are to the patch, the cleaner the split.

### Planning what a patch will do

Before a patch ships, list its major items and the kind of value each carries. Then predict:

1. Items whose value is mostly `F` will drop by about `(1 − r)` of that part when the patch lands. Their owners may sell early, so expect prices to start sliding before the patch.
2. Items whose value is mostly `S` will move with ownership. Anything the patch makes easier to get will lose social value.
3. Items whose value is mostly `H` will barely move.

That list is also a list of who will complain. Players holding functional items expect the drop, because they know the tier cycle. Players holding social items often do not, and a re-release can feel like confiscation.

## 4. Stores, status and the rival parts

Many MMOs now sell items for money as well as dropping them in play. The three-part split tells you what each sale does to everyone else.

- A cosmetic that nobody else can obtain in play adds `H` for the buyer and gives social value from the start, since `f` begins near zero. Other players lose nothing except the chance to own it.
- A cosmetic that is also available in play, made cheaper by the store, raises `f` and lowers the social value of copies earned in play. Players who earned it notice.
- A functional item for sale lowers `F` for earned items (they are no longer the best available) and, in PvP, directly lowers the relative power of players who did not buy.

This is why players and regulators react so differently to stores that look similar on the surface. Week 11 (real-money trade) and MMO403 (monetization and ethics) come back to these questions. For now, the design habit is simple. For every item you put in a store, write down which of `F`, `H` and `S` you are selling, and who loses each part.

## In-class activity (25 minutes)

Work in groups of three. Each group gets a list of eight items from an imaginary MMO (your instructor will hand it out, or invent your own): a raid weapon, a crafted bag, a battle pet, a recoloured armour set, a title for beating a hard boss, a limited holiday hat, a store mount, and a teleport scroll.

1. For each item, estimate `F`, `H` and `S` in gold, using `s = 1,000` and a guessed ownership share `f`. Write the total `V`.
2. Pick the item whose value you expect to change most over the next year. Write the event that changes it and your predicted new `V`.
3. The studio wants to add two items to a real-money store. Choose two from the list, and name who loses value and how much, using the model.

Expected output: an eight-row table with `F`, `H`, `f`, `S` and `V`, one prediction with numbers, and a short store recommendation.

## Common misconceptions

- **"Cosmetics have no value because they do nothing."** They have no functional value. Their hedonic and social value can exceed any weapon's, as partyhats show.
- **"Rarer always means more valuable."** Rarity feeds only the social part, and only for items other players can see and care about. A rare item nobody notices has little `S`.
- **"An item keeps its value if nobody sells it."** Functional value falls when a better tier arrives, even if every copy stays in its owner's bag. Value is relative to what else exists.
- **"Re-releasing an old item is harmless because new players get something fun."** It raises `f` and lowers the social value of every existing copy. The loss falls on players who acquired it the hard way.

## Check yourself

1. An item is owned by 1 in 256 active players and `s = 800`. What is its social value? What is it if ownership rises to 1 in 16?
2. A retired title is owned by 2% of active players. Churn is 3% a week and `q = 0`. How many weeks until its social value has risen by `s`?
3. A store mount has `q = 4%` and `c = 1%` a week. What ownership share does it approach? With `s = 1,000` and `H = 2,500`, what value does it settle at?
4. A weapon's price falls from 15,000 to 4,000 gold in the week a new tier releases. Its ownership share barely changed. Estimate `F0` and `r` if its `H + S` is about 1,500.
5. Your producer wants to sell a copy of a retired event mount in the store for one week. Using the model, describe what happens to the value of the mount for existing owners during and after that week.

<details>
<summary>Answers</summary>

1. `log2(256) = 8`, so `S = 8 × 800 = 6,400`. At 1 in 16, `log2(16) = 4`, so `S = 3,200`. Ownership rose 16-fold and social value halved.
2. Social value rises by `s` each time `f` halves. With `q = 0`, `f` shrinks by 0.97 a week, so a halving takes `ln 2 / −ln(0.97) = 0.6931 / 0.03046 ≈ 22.8` weeks.
3. `f* = q / (q + c) = 0.04 / 0.05 = 80%`. `S = 1,000 × log2(1 / 0.8) = 1,000 × 0.322 = 322`. `V ≈ 2,500 + 322 = 2,822`.
4. Before the patch `F0 + 1,500 = 15,000`, so `F0 = 13,500`. After it, `F0 × r + 1,500 = 4,000`, so `F0 × r = 2,500` and `r ≈ 0.185`. The weapon kept about 19% of its functional value.
5. During the week `q` becomes positive, so `f` rises every day the store is open. How far depends on sales: if 1% of players buy it, `f` goes from, say, 0.05% to about 1.05%, a factor of 21, and social value drops by `log2(21) ≈ 4.4` halvings, `4.4 × s`. After the week `q` returns to 0 and `f` starts to shrink again, but at 34 weeks per halving (at 2% churn) it takes years to recover the loss.

</details>

## Lab / assignment hook

[Lab 02, pricing the three kinds of value](../labs/lab02.md). You will fit `F`, `H` and `S` to a price history for a set of items, test the `log2` social-value model against an alternative, and write a patch forecast. It feeds the Models assignment (30%).

## Sources

- Lehdonvirta, V. (2009). "Virtual item sales as a revenue model: identifying attributes that drive purchase decisions." *Electronic Commerce Research* 9(1-2), 97-113. Assigned for its catalogue of item attributes that drive purchases. The gold-valued sum `V = F + H + S` and the `log2` social-value function in this lecture are this course's own.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.
- RuneScape Wiki, "Christmas cracker". Released 25 December 2001, available that day only, contained partyhats, the 2003 duplication glitch, partyhat prices in the billions of coins.
- Warcraft Wiki, "Gates of Ahn'Qiraj" and "Scarab Lord". Patch 1.9.0 (3 January 2006); the Black Qiraji Resonating Crystal given to the player who rang the Scarab Gong on each server; unobtainable once the event ended; new realms opened with the gates unlocked.
- Wikipedia, "Path of Exile" (article as of 2026). The developers' stated goal of a free game financed by "ethical micro-transactions", a store mainly of cosmetic item skins, and a barter economy of currency items with their own uses.

## Interactive spec: examples/w02-value-over-time.html

**The one insight:** an item's value moves for three different reasons. Functional value drops on the developer's patch calendar, social value moves with the ownership share, and a retired item gains value every week while nothing about it changes.

**Model** (weekly steps, `t` = 0 to 104):

```
F(t) = F0 if t < t_R, else F0 × r
S(t) = s × log2(1 / f(t))
f(t+1) = f(t) + q × (1 − f(t)) − c × f(t)
V(t) = F(t) + H + S(t)
```

**Layout.** Two stacked views sharing one x-axis (weeks 0-104).

- Top view, "Who owns it": `f(t)` for all three items on a log-scale y-axis from 0.01% to 100%, one line each, labelled at the right end of each line.
- Bottom view, "What it is worth": stacked areas of `F`, `H` and `S` for the selected item, with the total `V` printed at the cursor week. Item selector as three buttons (Tier sword, Store mount, Retired mount).
- A week scrubber (slider 0-104) draws a vertical line in both views and fills a readout table with `f`, `F`, `H`, `S` and `V` for all three items at that week.

**Controls** (apply to the selected item, except the shared ones).

- Shared: `s` (0-3,000, default 1,000), churn `c` (0-10% a week, default 2%).
- Per item: `F0` (0-40,000), `r` (0-1), `t_R` (0-104 weeks), `H` (0-10,000), starting `f` (0.01%-50%, log slider), `q` (0-10% a week).
- Button "Re-release retired mount at week 52": sets the retired mount's `q` to 3% from week 52 onward, so students see the share climb and the value drain.

**Defaults and test values** (must match the lecture's table, rounded to whole gold and to the shown precision for `f`):

- Tier sword: `F0` 20,000, `r` 0.1, `t_R` 26, `H` 500, `f0` 1%, `q` 2%. Week 0: `S` 6,644, `V` 27,144. Week 13: `f` 21.2%, `S` 2,239, `V` 22,739. Week 26: `f` 33.0%, `V` 4,097. Week 104: `f` 49.3%, `V` 3,520.
- Store mount: `F0` 0, `H` 3,000, `f0` 1%, `q` 3%. Week 1: `f` 3.95%. Week 52: `f` 55.9%, `V` 3,839. Week 104: `f` 59.7%, `V` 3,744. Long-run share `q / (q + c)` = 60% shown as a dashed line.
- Retired mount: `F0` 0, `H` 3,000, `f0` 0.1%, `q` 0. Week 52: `f` 0.035%, `V` 14,481. Week 104: `f` 0.012%, `V` 15,997. Halving time readout `ln 2 / −ln(1 − c)` = 34.3 weeks.

**Edge cases.** Clamp `f` to at least 1e-6 so `log2` stays finite. When `q = 0` and `c = 0`, show "share never changes".

**Accessibility.** Distinguish the three lines and three stacked areas by pattern or label as well as colour. Keyboard operable sliders and buttons with visible focus. Respect `prefers-reduced-motion`.
