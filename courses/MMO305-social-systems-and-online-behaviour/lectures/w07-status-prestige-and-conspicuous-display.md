# MMO305 · Week 07 — Status, Prestige and Conspicuous Display

**Why this matters:** Players chase mounts, titles and capes they could never use in a fight, and they judge each other by them. When a status item stops meaning what players think it means, groups make bad decisions about who to invite, and the players who earned it feel robbed. You design what those items say, whether you mean to or not.

**You will be able to:**
- Compute the precision of a status signal (the chance that an owner has the quality the item is supposed to show) from base rates, earning rates and purchase rates.
- Separate an item's rarity from its meaning, and show with numbers that a rare item can say nothing about skill.
- Critique a display item by naming what it signals (skill, time, wealth, luck or tenure) and who can fake it.
- Design a display venue and an earning rule that keep a status signal honest, and predict the gatekeeping loop it may start.

**Before class:** Veblen, T. (1899), *The Theory of the Leisure Class*, chapters 3 and 4 (conspicuous leisure and conspicuous consumption; public domain, on Project Gutenberg). Spence, M. (1973), "Job Market Signaling", *Quarterly Journal of Economics* 87(3), pp. 355-374, sections I and II. Skim Taylor, *Play Between Worlds* (2006), chapter 3, "Beyond Fun: Instrumental Play and Power Gamers" (pp. 67-92).

**Prerequisites from earlier courses:** [MMO304 week 2, functional, hedonic and social value](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w02-functional-hedonic-and-social-value.md) (the `log2(1/f)` rarity model; this week builds on it and does not repeat it). [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) (conditional probability `P(A | B)`). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md). [UX201 week 4, Self-Determination Theory](../../UX201-game-ux-and-player-psychology/lectures/w04-self-determination-theory.md) (competence and relatedness as needs that status items feed). [MMO305 week 6, trust and reputation systems](w06-trust-and-reputation-systems.md), for the idea that a score is only as good as what it predicts.

**Interactive:** [Signal precision](../examples/w07-signal-precision.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. What status is, and why games make so much of it

**Status** is a person's standing in the eyes of others. **Prestige** is status earned by doing something others admire. A **status signal** is anything visible that lets others infer that standing without watching you earn it: a title under your name, a mount parked outside the bank, a cape, a rank border, an achievement badge.

Online worlds are full of status signals for a simple reason. In a crowd of strangers you cannot watch someone play for three hours before deciding whether to invite them. You glance at what they carry. Gear, titles and mounts become a public record of where a player has been and what they have beaten. Taylor's ethnography of EverQuest (2006) shows how much of that world's social life ran through such records.

### Veblen's two kinds of display

The economist Thorstein Veblen wrote about the rich of the 1890s, not about gamers, but his two ideas map onto MMOs almost too well.

- **Conspicuous leisure** is proof that you have time to spare. In Veblen's world that meant skills with no practical use, such as dead languages or fine manners, which could only be learned by someone who did not need to work. In an MMO it is the 3,000-hour reputation grind, the mount collection, the maxed skill in a profession nobody needs.
- **Conspicuous consumption** is proof that you can afford to waste. In Veblen's world, expensive goods bought to be seen. In an MMO, the gold-sink cosmetic, the store mount, the item bought on a black market for millions.

Both work the same way. The display is valuable because it is costly, and it is costly in a way that only the kind of person being advertised can afford.

### Signals, and why cost makes them honest

Michael Spence's 1973 paper on job markets gave the idea a precise form. An employer cannot see a worker's ability. A degree is a signal. It works only if earning the degree costs a low-ability worker more than a high-ability one. If everyone can get the degree at the same cost, it tells the employer nothing. Biologists found the same logic in animals (Zahavi's "handicap principle"). A peacock's tail is believable because a sick bird cannot grow one.

The game version: **a status signal is honest when the players who lack the quality find it much harder to obtain than the players who have it.** A cape that requires beating a hard boss solo is honest about skill, because unskilled players cannot get it. A title that anyone can buy with gold is honest about gold and nothing else.

### Five things an item can say

Before you do any math, name what the item signals. Most display items say one of five things:

| Signal | What it shows | Example shape |
|---|---|---|
| Skill | The owner can do something hard | A reward for beating the hardest difficulty before a deadline |
| Time | The owner invested many hours | A long reputation grind, a collection count |
| Wealth | The owner has in-game or real money | A store mount, a gold-sink cosmetic |
| Luck | The owner was lucky, or persistent at a low drop rate | A 1-in-100 mount drop |
| Tenure | The owner was there early | A reward from a retired event or an anniversary |

The trouble starts when players read an item as one kind of signal and it is really another. That confusion is what the worked example measures.

## 2. Worked example: when a rare badge stops meaning anything

### The hook

In World of Warcraft, the Cutting Edge achievements are earned by defeating the final boss of a raid tier on Mythic, the hardest difficulty, before the next tier or expansion releases. The Mythic requirement dates from Warlords of Draenor (2014), when Mythic difficulty arrived; the Mists of Pandaria versions asked for Heroic. Many player groups ask for the achievement before they invite someone to a hard raid, because it looks like proof of skill.

But WoW also has a busy market in carries. A carry is a service where a strong group takes a paying player through the fight. Blizzard has historically tolerated individual players selling carries for in-game gold while prohibiting commercial operations that sell them for real money. So some owners of any Cutting Edge badge earned it by being good, and some by paying gold.

Here is the puzzle. If carry sales doubled next month, the badge would still look rare. The number of owners would barely move. Would the badge still mean the same thing? The model says no, and says by how much.

### The model

Split the active population into two groups. **Skilled** players could clear the fight themselves. **Unskilled** players could not. Then ask how each group ends up owning the badge.

```
f = s × e + (1 − s) × (u + b)

P(skilled | owns) = s × e / f

lift = P(skilled | owns) / s

rarity (bits) = log2(1 / f)
```

- `s` is the share of active players who are skilled, between 0 and 1. This is the **base rate**.
- `e` is the chance that a skilled player earns the badge (some skilled players never try).
- `u` is the chance that an unskilled player earns it legitimately anyway, through luck, a strong guild or a generous group.
- `b` is the chance that an unskilled player buys it through a carry.
- `f` is the share of all active players who own the badge.
- `P(skilled | owns)` is the badge's **precision**: of all the players showing the badge, what fraction are actually skilled. This is conditional probability from MA102 week 2, worked out with Bayes' rule. It is the number a group leader is guessing at when they read the badge.
- `lift` compares precision to the base rate. A lift of 10 means an owner is ten times more likely to be skilled than a random player. A lift of 1 means the badge tells you nothing about skill.
- `rarity` is the same `log2(1/f)` you met in MMO304 week 2. It measures how rare the badge is, not what it means.

The whole lecture rests on one observation. **Rarity depends on `f`. Meaning depends on who makes up `f`.** A designer who watches only ownership numbers will miss the change that matters.

### Numbers you can check

Take `s = 5%` skilled, `e = 60%`, `u = 0.5%`, and vary the carry rate `b`. These are invented numbers for a teaching model, not WoW data.

| Carry rate `b` | Owners `f` | Rarity (bits) | Precision | Lift |
|---|---|---|---|---|
| 0% | 3.47% | 4.85 | 86.3% | 17.3× |
| 1% | 4.42% | 4.50 | 67.8% | 13.6× |
| 3% | 6.33% | 3.98 | 47.4% | 9.5× |
| 6% | 9.18% | 3.45 | 32.7% | 6.5× |
| 10% | 12.97% | 2.95 | 23.1% | 4.6× |

Check the first row by hand. Skilled owners are `0.05 × 0.6 = 0.03` of the population. Unskilled owners are `0.95 × 0.005 = 0.00475`. So `f = 0.03475`, precision `= 0.03 / 0.03475 = 0.863`, and rarity `= log2(1 / 0.03475) = log2(28.8) = 4.85` bits.

Now check the `b = 6%` row. Unskilled owners are `0.95 × (0.005 + 0.06) = 0.06175`. So `f = 0.09175` and precision `= 0.03 / 0.09175 = 0.327`.

Read the table from top to bottom. At a 6% carry rate the badge lost about 1.4 bits of rarity. It went from "about 1 in 29 players" to "about 1 in 11". A player glancing at it still thinks "rare". But precision collapsed from 86% to 33%. Two out of three owners now cannot do the fight. Nothing about the skilled players changed. They are still 3% of the population and all still own the badge. They are simply outnumbered.

### The lottery mount: rare and meaningless

Run the same model on a mount that drops at 1% for everyone who kills a boss. Set `e = u = 0.01` and `b = 0`. Then:

```
f = s × 0.01 + (1 − s) × 0.01 = 0.01
P(skilled | owns) = s × 0.01 / 0.01 = s
lift = 1
rarity = log2(100) = 6.64 bits
```

The lottery mount is rarer than the Cutting Edge badge in every row of the table, and it says nothing at all about skill. Its precision equals the base rate. It is still a real status signal, but of luck, persistence (players who farmed the boss for months) or wealth, not skill. When a game adds a way to buy it, it becomes a wealth signal too.

World of Warcraft has a well-known case. Ashes of Al'ar, the phoenix mount that Kael'thas Sunstrider drops in Tempest Keep, was added in the Burning Crusade era (patch 2.0.3) and has always dropped very rarely. It is bind-on-pickup, so it cannot be traded, but the game's Black Market Auction House has at times offered it for gold. Players prize it, and they are right to. They are just not prizing skill.

### A visual you can move

Open `examples/w07-signal-precision.html`. The left view plots the badge's rarity in bits as you drag the carry-rate slider. The right view plots precision on the same slider. On the left, the line sags gently. On the right, it falls off a cliff in the first few percent. Below both, a row of 100 owner icons recolours live. Skilled owners are one colour and carried owners another, so you see the crowd behind the badge change while the count at the top barely moves. A preset button switches to the lottery mount and shows precision pinned to the base rate.

### Cross-game recognition

The same three questions apply everywhere. What is the base rate? Who can get the item without the quality? Can it be bought?

**Old School RuneScape, the Infernal cape (1 June 2017).** Players receive the cape for defeating TzKal-Zuk at the end of the Inferno, a long solo challenge. The cape cannot be traded. In the model this pushes `b` toward zero from the design side. You cannot buy the cape on the Grand Exchange, so the only unskilled owners are those whose accounts someone else played, which breaks the rules. With `b ≈ 0` and a small `u`, precision stays high, which is why players read the cape as one of the game's clearest skill signals. It is also rare, but notice that its value comes from low `b`, not from low `f`.

**Steam global achievement percentages (Valve, current).** Steam shows every player the percentage of a game's owners who have unlocked each achievement, sorted from most to least common. This is `f` published by the platform, so every player can compute rarity in bits. It does not publish precision. An achievement for finishing a game on the hardest setting and an achievement for a random event may show the same 2%. The Steam display invites players to read rarity as prestige, which is exactly the confusion the model separates.

**World of Warcraft, transmogrification (patch 4.3, Cataclysm era, 2011).** Transmogrification lets a player make their armour look like other gear they own. Before it, what you wore was what you used, so a raider's appearance was a live skill-and-progress signal. After it, players could wear the look of old gear from any era, and appearance became a signal of collection (time), taste and tenure. The same display venue changed from saying "skill now" to saying "history and style". The model's lesson is that `e`, `u` and `b` are properties of the rule for getting the look, not of the look itself.

Three games, one idea. A display item's meaning is the precision of the inference players draw from it, and that precision depends on who else can get it.

### Eyes-open design judgment

- **Decide what each item is for.** If an item is meant to signal skill, protect `b` and `u`. Make it untradeable, tie it to the character that did the deed, and keep luck out of the path. If it is meant to signal wealth or time, sell or grant it freely, and do not dress it up as a skill badge.
- **Rarity is not your target, precision is.** Lowering `f` by making something harder to get only helps if the barrier is harder for players without the quality. A 1% drop rate lowers `f` for everyone equally and buys no meaning.
- **Carries are not always bad.** A carry market lets strong players earn gold and lets weaker players see content. The cost falls on the badge's meaning and on the players who earned it. You can keep carries and keep meaning by separating them. Award the badge only to players who meet a performance bar, or show on inspection how a run was completed.
- **Tolerating carries is a policy.** Blizzard's line between gold carries (tolerated) and real-money carries (banned) is a choice about which kind of `b` is acceptable. Whatever line you pick, it sets the precision of every badge in your game.
- **Players will compute precision for you.** When official badges lose meaning, players invent their own signals, such as third-party score sites and log rankings. Those are often harsher and less fair than yours. Keeping your own signals honest is cheaper than fighting the replacements.

## 3. Display venues: where status is seen

A status item needs an audience. The **display venue** is the place and moment where others can see it. The same item can be a strong or weak signal depending on the surface.

- **Ambient display.** Visible without any action: a mount in a crowded city, a glowing weapon, a title on a nameplate. Everyone sees it, including strangers. This is Veblen's conspicuousness in its pure form.
- **On-inspection display.** Visible when someone chooses to look: an achievement list, a gear window, a profile page. Seen mostly by people deciding whether to group with you. This is where gatekeeping happens.
- **Recorded display.** A permanent public record: a server-first announcement, a leaderboard, a hall of fame. Seen by the whole community, including people who were not online.

Each surface changes who pays attention and how much. Ambient display tends to reward items that look impressive, since strangers judge by eye. On-inspection display tends to reward precise signals, since the viewer is making a decision. Recorded display rewards being first, which is a status race with one winner.

A quick design test. For every status item, answer two questions. Who sees it? And what do they do differently after seeing it? If nobody sees it, it is a hedonic item only (MMO304 week 2). If people see it and change nothing, it is decoration. If people see it and decide whether to invite you, it is a credential, and its precision matters a lot.

### Hiding versus showing

Players do not always want to be seen. Some hide titles to avoid being targeted in PvP, and some hide achievements to avoid being gatekept. Some games let players choose what to show. That choice has an effect you can predict with the model. If only proud owners show a badge, the owners who show it are a selected group. When hiding is allowed, showers skew toward players who earned the item in the most impressive way, and the displayed version gets a higher precision than the item itself. Honest players benefit. The cost is that an empty slot now carries a faint negative signal.

## 4. The gatekeeping loop

Status signals do not just reflect social structure. They reshape it. Here is a loop that shows up in almost every MMO with visible credentials.

1. Group leaders start requiring a badge for entry, because it predicts success.
2. Players without the badge cannot get into groups, so the badge's practical value rises.
3. Demand for carries rises, because a carry is now the fastest way in.
4. Carry sales raise `b`, which lowers the badge's precision.
5. Leaders notice that badge holders fail more often, and demand a stricter badge, or a badge plus a score.
6. Return to step 2 with a higher bar.

This is a positive feedback loop in the sense of GD102 week 3: each turn makes the next turn stronger. Its outcome is credential inflation. Newer and weaker players are pushed further out every cycle, even though the content has not become harder.

Designers have a few ways to damp the loop:

- **Supply entry without credentials.** Automated group finders that do not show achievements, or that match by measured performance, remove step 1 for some of the population.
- **Make the credential expire.** A badge that only counts for the current tier cannot inflate across tiers. Cutting Edge achievements have a deadline in exactly this sense. They must be earned before the next tier releases.
- **Keep `b` low for credential items.** The loop runs through step 4. Cut it and precision stays high, so leaders have no reason to raise the bar.
- **Offer a separate status track for the pushed-out.** Collection and time signals give players standing that does not depend on being invited.

## 5. Status as a social system, not a loot table

Two more patterns matter when you design status into a world.

**Status is positional.** MMO304 week 2 showed that an item's social value falls as ownership spreads. The same is true of standing. One player's rise is others' relative fall. That makes status systems zero-sum in a way that most progression is not. If every player gets the same title, nobody gains standing. Your choice is who gets less, not whether anyone does.

**Status spreads through groups.** In guild-based MMOs, a lot of status belongs to groups, not individuals. A guild's rank on a progress leaderboard lends standing to all its members, including members who rarely raid. This is one reason guild hopping happens. Players move to a guild with more standing because some of it rubs off (MMO305 week 4 covers guild lifecycles). When you design recorded display, decide whether it credits the individual, the group or both.

Finally, a warning. Status systems are some of the strongest motivators you have, and they touch real social needs (UX201 week 4 calls them competence and relatedness). A player who loses standing overnight because a status item was re-released or a badge lost meaning feels something closer to a social loss than an economic one. Treat changes to status rules with the same care as changes to items people paid for.

## In-class activity (25 minutes)

In groups of three, audit the status items of a game one of you plays.

1. List six display items: titles, mounts, cosmetics, achievements or ranks. For each, name what it signals from the five-row table in section 1.
2. Pick the one your group thinks players treat as a skill signal. Estimate `s`, `e`, `u` and `b` with a one-line reason for each. Guesses are fine if you say where they came from.
3. Compute `f`, precision and lift. Then enter your numbers in the interactive's custom mode and find the carry rate at which precision falls below 50%.
4. Name one rule change that would raise precision by at least 20 points, and one group of players it would upset.

Expected output: a six-row table, a computed precision with its inputs, the 50% carry rate, and a two-sentence proposal.

## Common misconceptions

- **"Rare means prestigious."** Rarity is `log2(1/f)`. Prestige depends on precision, which depends on who owns the item. The 1% lottery mount is rarer than most skill badges and says nothing about skill.
- **"If ownership barely moves, the item is fine."** In the worked example, ownership rose from 3.5% to 9.2% and precision fell from 86% to 33%. Small changes in `f` can hide large changes in meaning, because the new owners are a different kind of player.
- **"Making the item harder to get fixes it."** Only if the new barrier is harder for players without the quality. A lower drop rate cuts `e` and `u` together and leaves precision where it was.
- **"Cosmetics are harmless because they have no stats."** A cosmetic that players read as a credential affects who gets invited. It can have more social effect than a weapon.

## Check yourself

1. A title requires clearing a dungeon in under 20 minutes. The base rate of skilled players is 10%, skilled players earn it at `e = 50%`, and unskilled players never do (`u = 0`). A boosting market appears with `b = 2%`. Compute `f`, precision and lift before and after the market appears.
2. In the lecture's example (`s = 5%`, `e = 60%`, `u = 0.5%`), what carry rate `b` makes precision exactly 50%?
3. A designer halves the drop rate of a lottery mount from 1% to 0.5% to make it "more prestigious". What happens to its rarity in bits and to its precision as a skill signal?
4. A game lets players hide their achievements. Explain, using the model, why the achievements that remain visible may be more trustworthy than the achievement system as a whole.

<details>
<summary>Answers</summary>

1. Before: `f = 0.1 × 0.5 = 0.05`, precision `= 0.05 / 0.05 = 100%`, lift `= 1.0 / 0.1 = 10×`. After: `f = 0.05 + 0.9 × 0.02 = 0.068`, precision `= 0.05 / 0.068 = 73.5%`, lift `= 7.35×`. Ownership rose by a third and one owner in four is now carried.
2. Precision is 50% when unskilled owners equal skilled owners: `0.95 × (0.005 + b) = 0.03`, so `0.005 + b = 0.03158` and `b ≈ 2.66%`.
3. `f` falls from 1% to 0.5%, so rarity rises by exactly one bit, from 6.64 to 7.64. Precision stays equal to the base rate `s`, because the drop rate is the same for skilled and unskilled players. The mount becomes rarer, not more meaningful about skill.
4. If players who earned an achievement impressively are more likely to show it, the displayed set has a higher share of skilled owners than the full set of owners. In model terms, showing acts like an extra filter that removes more unskilled owners than skilled ones, which raises precision among the badges people can see.

</details>

## Lab / assignment hook

[Lab 07, status signal audit](../labs/lab07.md). You pull achievement percentages for one game from a public source, classify each achievement by what it signals, estimate precision for the three that players treat as credentials, and write a 400-word memo recommending one rule change. This lab also feeds your field observation assignment, since you will watch how players ask for and read credentials in a real group finder.

## Sources

- Veblen, T. (1899). *The Theory of the Leisure Class*. Macmillan. Conspicuous leisure and conspicuous consumption, chapters 3 and 4. Public domain.
- Spence, M. (1973). "Job Market Signaling." *Quarterly Journal of Economics* 87(3), pp. 355-374. Signals are informative when their cost differs by type.
- Zahavi, A. (1975). "Mate selection: a selection for a handicap." *Journal of Theoretical Biology* 53(1), pp. 205-214. The handicap principle.
- Taylor, T. L. (2006). *Play Between Worlds: Exploring Online Game Culture*. MIT Press. Ethnography of EverQuest players, including power gamers and raiding.
- Warcraft Wiki, "Cutting Edge" (accessed September 2026). Earned by defeating the final raid boss on Mythic before the next season or expansion; introduced in Warlords of Draenor; Heroic requirement in Mists of Pandaria before Mythic existed.
- Warcraft Wiki, "Boosting" (accessed September 2026). Blizzard's historical tolerance of individual boosting for gold, prohibition of commercial real-money boosting, and the June 2022 blue post on boosting spam.
- Warcraft Wiki, "Ashes of Al'ar" (accessed September 2026). Very rare, bind-on-pickup drop from Kael'thas Sunstrider in Tempest Keep, added in patch 2.0.3; availability on the Black Market Auction House.
- Warcraft Wiki, "Transmogrification" (accessed September 2026). Patch 4.3 preview, August 2011; appearances collection.
- Old School RuneScape Wiki, "Infernal cape" (accessed September 2026). Released 1 June 2017 with the Inferno; awarded for defeating TzKal-Zuk; not tradeable.
- Valve, Steamworks documentation, "Achievements" (current). Global achievement statistics showing the percentage of players who unlocked each achievement, ordered from most common to rarest.

## Interactive spec: examples/w07-signal-precision.html

**Purpose.** Make visible that rarity and meaning are different quantities. As the carry rate rises, the badge stays rare-looking while its precision collapses.

**The one insight.** A few percent of bought ownership barely changes how rare a badge looks but can halve what it means.

**Model (exact).**

```
f     = s*e + (1 - s)*(u + b)
prec  = s*e / f
lift  = prec / s
bits  = log2(1 / f)
```

**Layout.** Two linked charts side by side (stacked on phones), sharing the same x-axis: carry rate `b` from 0% to 20%.

- Left chart, "How rare it looks": `bits` on the y-axis (0 to 8). Secondary label shows "1 in N" where `N = round(1/f)`.
- Right chart, "What it means": `prec` on the y-axis (0% to 100%). Draw a dashed horizontal line at `prec = s` labelled "base rate: badge tells you nothing".
- A vertical marker at the current `b` on both charts, with the exact values printed next to each marker.
- Below the charts, a 10 × 10 grid of 100 owner icons. The number of skilled icons is `round(100 × prec)`; the rest are drawn in a second colour and split into "lucky" (`(1−s)u/f`) and "carried" (`(1−s)b/f`) with a third shade. Use shape as well as colour (filled circle for skilled, ring for lucky, square for carried) for colour-blind users.

**Controls.**
- Slider `b` (carry rate), 0 to 20%, step 0.1%. Default 0%.
- Slider `s` (base rate), 1% to 30%, step 1%. Default 5%.
- Slider `e`, 10% to 100%, step 5%. Default 60%.
- Slider `u`, 0% to 5%, step 0.1%. Default 0.5%.
- Preset buttons: "Skill badge" (s=5%, e=60%, u=0.5%, b=0%), "Carry market" (same, b=6%), "Lottery mount" (s=5%, e=1%, u=1%, b=0%), "Untradeable cape" (s=3%, e=40%, u=0.1%, b=0%).
- A readout table under the controls: `f`, bits, "1 in N", precision, lift, and the carry rate at which precision crosses 50% (solve `(1−s)(u+b) = s*e`, so `b50 = s*e/(1−s) − u`; show "never" if `b50 > 20%` and "already below" if `b50 < 0`).

**Test values (must match to the shown precision).**

| s | e | u | b | f | bits | precision | lift |
|---|---|---|---|---|---|---|---|
| 5% | 60% | 0.5% | 0% | 3.475% | 4.85 | 86.3% | 17.3 |
| 5% | 60% | 0.5% | 3% | 6.325% | 3.98 | 47.4% | 9.5 |
| 5% | 60% | 0.5% | 6% | 9.175% | 3.45 | 32.7% | 6.5 |
| 5% | 1% | 1% | 0% | 1.000% | 6.64 | 5.0% | 1.0 |
| 10% | 50% | 0% | 2% | 6.800% | 3.88 | 73.5% | 7.35 |

`b50` for the default skill badge is `0.03/0.95 − 0.005 = 2.66%`.

**First screen.** Load with the "Carry market" preset so the gap between a mildly lower rarity and a much lower precision is visible before any interaction.

**Accessibility.** All sliders keyboard operable with visible focus; values announced via `aria-valuetext` (for example "carry rate 6 percent"). Respect `prefers-reduced-motion` by disabling icon transitions. No game logos or art; the badge is drawn as a generic shield shape.
