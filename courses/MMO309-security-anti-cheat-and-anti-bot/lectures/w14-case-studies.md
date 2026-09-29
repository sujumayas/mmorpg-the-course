# MMO309 · Week 14 — Case Studies: Ban Waves, Bot Nukes and the Courts

**Why this matters:** Every studio that has run an MMO for long enough has fought the same few fights, and most of them are on record. Reading those records well is a skill. You pick the right model, put numbers on the parts that can be measured, and separate what worked from what only looked decisive. This week you practice that on four real cases and one scorecard that puts them side by side.

**You will be able to:**
- Analyze a published security incident with the course's case template, naming the asset, the attacker's economics, the control and the response.
- Compute an attack's uptime from its detection lag, response lag and attacker downtime, and score a response by the harm it leaves, what it costs the studio and what it costs honest players.
- Derive when a day of attacker downtime is worth more than a day of faster detection, and use it to rank levers.
- Critique a studio's response (a ban wave, a structural fix, a price change or a lawsuit) by rewriting it as one row of the scorecard.

**Before class:** Hoglund, G. & McGraw, G. (2007), *Exploiting Online Games*, chapter 3 ("Money") and chapter 4 ("Enter the Lawyers"). Read the RuneScape Wiki page "ClusterFlutterer" and the Wikipedia article "MDY Industries, LLC v. Blizzard Entertainment, Inc." (15 minutes each). Bring the threat model you drafted in week 1.

**Prerequisites from earlier courses:** [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (why gold has a dollar price, and RuneScape's trade limit). [MMO401 week 12, economic shocks, exploits and rollbacks](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w12-economic-shocks-exploits-and-rollbacks.md) (harm per hour of an exploit). [MMO402 week 5, rules, EULAs and terms of service](../../MMO402-emergent-society-governance-and-ethics/lectures/w05-rules-eulas-and-terms-of-service.md) (the Glider case from the contract side). [MMO402 week 7, justice systems, reports, reviews and appeals](../../MMO402-emergent-society-governance-and-ethics/lectures/w07-justice-systems-reports-reviews-appeals.md) (what a false ban costs a player). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). In this course, [week 1, threat modeling](w01-threat-modeling-for-games.md) (the loss ledger, where harm per day comes from), [week 5, memory editing and client integrity](w05-memory-editing-and-client-integrity.md) (the ban-wave timing model, which this lecture links to and does not repeat), [week 6, botting economics](w06-botting-economics.md) (the break-even lifetime), [week 7, behavioral bot detection](w07-bot-detection-behavioral-features.md), [week 11, exploit response](w11-exploit-response-rollback-vs-ban.md), [week 12, legal and ethical considerations](w12-legal-and-ethical-considerations.md) and [week 13, bug bounties and disclosure](w13-bug-bounty-and-disclosure.md).

**Interactive:** [examples/w14-response-scorecard.html](../examples/w14-response-scorecard.html). Keep it open during section 2.

---

## 1. How to read a security case

A case study is not a story with a moral. It is evidence about how a system behaved under attack. To get evidence out of it, read every case with the same questions, so that cases from different games and decades line up side by side.

The course's case template has seven rows:

| Row | Question | Where you learned the tool |
|---|---|---|
| Asset | What was the attacker after? Gold, items, rank, accounts, the anti-cheat itself? | Week 1 threat modeling |
| Attacker economics | What did one attack or one bot earn, and what did it cost? | Week 6 botting economics |
| Control | What design or technical measure stood in the way? | Weeks 2 to 5 |
| Detection | How was the attack noticed, and how fast? | Weeks 7 and 8 |
| Response | Ban, rollback, patch, lawsuit, rule change? When? | Weeks 5 and 11 |
| Outcome | What changed, measured if possible? | This week |
| Transferable rule | What would you do the same way in a new game? | This week |

Two habits make the template work.

First, **separate what the studio said from what was measured.** "We believe this targets 98% of bots" is a studio estimate, not a count. It is still useful, but label it.

Second, **find the number that decided the outcome.** In most cases one quantity did most of the work, such as the time an attacker needed to come back, the price of a new account or the cost of a court case. The worked example below gives you a scorecard for finding that number.

## 2. Worked example: scoring four responses on one card

### The hook

Two studios, two opposite habits.

Valve Anti-Cheat (VAC) flags an account the moment it detects cheat software, tells the player nothing, and bans "days or even weeks" later, often in large batches players call VAC waves. Valve never says which cheat it detected or how.

Jagex did the reverse in October 2011. It announced a "bot-nuking day" for RuneScape four days ahead, with a countdown, then shipped ClusterFlutterer, an update it said would permanently stop "reflection" bots, which it believed were 98% of the bots in the game.

One studio hides everything and waits. The other announces the date. Players argued about which one was right. Both were, and one small formula shows why. It also puts Glider's lawsuit and New World's family-sharing change on the same card.

### The model

Every attack in this course runs in cycles. It works for a while, you notice, you act, the attacker loses some days rebuilding, and then it works again. Three durations describe one cycle:

- `detect`, the detection lag. Days from the attack going live until you have a signal you trust (weeks 7 and 8).
- `act`, the response lag. Days from that signal until you act. A ban wave chooses a long `act` on purpose ([week 5](w05-memory-editing-and-client-integrity.md) derives how long). A structural fix has a long `act` because it takes time to build.
- `down`, the attacker's downtime. Days from your action until the attack is live again. It covers patching the bot, buying new accounts or finding a new supplier.

The share of the year the attack is live, its **uptime**, is

```
live   = detect + act
uptime = live / (live + down)
```

Now attach money. Let `h` be the harm per live day in dollars (your week 1 loss ledger gives it), `K` the studio's yearly cost of running the response (engineering, support, lawyers), and `C` the yearly collateral cost to honest players (false bans, lost features, friction). Then

```
harm left = 365 × h × uptime
saving    = 365 × h − harm left − K − C
```

`saving` is measured against doing nothing, where uptime is 1. A response is worth running when its saving is positive, and the best response has the largest saving.

One rule falls out of the uptime formula. Cut one day from `live` and uptime drops by about `down / (live + down)²`. Add one day to `down` and uptime drops by about `live / (live + down)²`. So:

**A day of attacker downtime is worth `live / down` days of faster detection.**

When the attacker comes back faster than you catch them (`down` smaller than `live`), stretching their downtime beats speeding up your detection. Most real bot fights sit in that regime.

### Numbers you can check

All numbers below are invented for teaching. Each row is styled after one case, and every row uses the same attack, with `h = $1,000` per live day, so that only the lever differs. With no response, the attack is live all year and costs $365,000.

```python
def scorecard(detect, act, down, K, C, h=1000):
    """One response lever on a one-year scorecard. Returns (uptime, harm left, saving)."""
    live = detect + act                       # days the attack runs in each cycle
    u = live / (live + down)                  # share of the year the attack is live
    harm = 365 * h * u                        # harm your players still take
    return u, harm, 365 * h - harm - K - C    # saving against doing nothing

levers = {
    "no response":        (1, 0, 0, 0, 0),
    "instant bans":       (6, 0, 2, 40_000, 10_000),
    "faster detection":   (3, 0, 2, 80_000, 10_000),
    "delayed wave":       (6, 14, 30, 40_000, 10_000),
    "structural fix":     (6, 90, 365, 120_000, 30_000),
    "close free account": (6, 0, 60, 5_000, 25_000),
}
print(f"{'lever':<19}{'live':>5}{'down':>6}{'uptime':>8}{'harm left':>11}{'K + C':>9}{'saving':>10}")
for name, (dt, a, dn, K, C) in levers.items():
    u, harm, s = scorecard(dt, a, dn, K, C)
    print(f"{name:<19}{dt + a:>5}{dn:>6}{u:>8.3f}{harm:>11,.0f}{K + C:>9,}{s:>10,.0f}")

u_before, u_after, legal = 0.75, 0.10, 500_000
print("lawsuit pays when h >=", round(legal / (365 * (u_before - u_after))), "dollars per live day")
```

It prints (runs as shown with `.venv/bin/python`):

```
lever               live  down  uptime  harm left    K + C    saving
no response            1     0   1.000    365,000        0         0
instant bans           6     2   0.750    273,750   50,000    41,250
faster detection       3     2   0.600    219,000   90,000    56,000
delayed wave          20    30   0.400    146,000   50,000   169,000
structural fix        96   365   0.208     76,009  150,000   138,991
close free account     6    60   0.091     33,182   30,000   301,818
lawsuit pays when h >= 2107 dollars per live day
```

What each row assumes:

- **Instant bans.** A signature finds bots in 6 days and you ban at once. The bot maker sees the bans and patches in 2 days.
- **Faster detection.** Twice the detection spend halves `detect` to 3 days. Everything else is the same.
- **Delayed wave (VAC style).** You wait 14 days, then ban in one batch. We assume the bot maker, who learns nothing until the wave and then cannot tell what was detected, needs 30 days to recover. Week 5 shows how to check that assumption.
- **Structural fix (ClusterFlutterer style).** Building the fix takes 90 days. Afterward the attacker needs a new kind of bot, which we set at a year. Build cost and some disruption to honest players are high.
- **Close the free account (New World style).** Bans stay instant, but banned operators can no longer return on a free account. Week 6's break-even lifetime says most of them stop returning at all, so `down` jumps from 2 to 60 days. It costs almost nothing to build and something to the honest players who lose the free path.

Check two rows by hand. Instant bans: `uptime = 6 / 8 = 0.75`, harm left `= 365,000 × 0.75 = 273,750`, saving `= 365,000 − 273,750 − 50,000 = 41,250`. Delayed wave: `live = 20`, `uptime = 20 / 50 = 0.4`, harm left `= 146,000`, saving `= 169,000`.

Three things to see.

1. **Doubling detection spend barely helps.** Going from 6 days to 3 moves uptime from 0.75 to 0.60 and saving by $14,750, because `down` is only 2. The rule predicts it. At `live = 6` and `down = 2`, a day of downtime is worth 3 days of detection. Check it directly. Cutting `detect` to 5 gives `5 / 7 = 0.714`. Adding a day to `down` gives `6 / 9 = 0.667`.
2. **The wave waits longer and still wins.** It more than triples `live`, and it wins anyway because `down` grows fifteenfold. That is VAC's bargain. You accept more live days in exchange for a much longer, blinder recovery.
3. **The cheapest lever tops the card.** Closing the free account keeps instant bans and fast detection and adds $260,000 of saving over instant bans, for $5,000 of build cost.

The last line is the lawsuit (Glider style). Suing the bot's maker does not fit a cycle, so score it as a break-even. It pays when the harm it removes beats its legal cost `L`:

```
365 × h × (uptime before − uptime after) ≥ L
```

With $500,000 a year in legal cost, cutting uptime from 0.75 to 0.10 pays only if the supplier's bots do at least $2,107 of harm per live day. That is twice this card's attack, so the lawsuit does not pay here.

### A visual you can move

Open the interactive. The left panel is a one-year strip for the lever you select, shaded live and down, cycle by cycle. The right panel is the scorecard as stacked bars, one per lever: harm left, then `K`, then `C`, with a line at $365,000 for doing nothing. The shortest bar wins.

Select "instant bans" and drag `detect` from 6 down to 1. The strip barely changes, because it is mostly live already, and the bar shrinks slowly while the `K` segment grows. Now reset and drag `down` from 2 to 10. The strip turns mostly grey after a few clicks. Then select "delayed wave" and drag `act` from 14 to 0 while leaving `down` at 30. Uptime falls further, which is the case for keeping silent and banning early *if* a quick ban still left the attacker blind. Whether it does is week 5's question, not this card's. The panel shows the answer to "which term moves uptime most" before you do any algebra. It is whichever of `live` and `down` is smaller relative to the other.

### Cross-game recognition

**VAC waves and ClusterFlutterer (the hook).** Both studios pushed `down` up, by different routes. Valve lengthens `down` with silence. Every detail a ban notice leaks helps the cheat maker patch faster, so Valve pays for a longer `act` to get a longer `down`. Jagex's fix made `down` long by changing how the client exposes game state, so secrecy no longer protected it. Announcing the date cost nothing in `down`, and Jagex kept the project secret only while it was being built. Same card, opposite habits, one lever.

**Steam phone numbers (May 2016).** Valve began banning accounts registered with the same phone number as a banned account, and a number used on a banned account cannot be registered again for three months. That is a `down` lever aimed at ban evaders. Coming back now needs a fresh phone number, not just a fresh account. [Week 6](w06-botting-economics.md) reads the same rule as a rise in setup cost `A`. Both readings describe the same effect.

**RuneScape's trade limit (2008 to 2011).** Section 3 covers it in detail. On the card it is the row where `C` ate the saving. It hit every honest player who wanted to give a gift, and 91% voted in 2011 to bring free trade back.

**Bug bounties ([week 13](w13-bug-bounty-and-disclosure.md)).** A bounty buys a shorter `detect` for exploits, because an outside finder reports before abusing. The rule tells you when that is the right purchase. For a dupe, `down` after a fix is effectively forever, so `live` is the only term left and every day off `detect` counts in full.

### Eyes-open design judgment

- **Measure `down`, do not assume it.** Every row above depends on how fast the attacker comes back. Watch bot forums and release notes after each action. If a new build ships within a day of every wave, the wave row collapses to the instant row with more live days.
- **`K` is often one-off.** The structural fix loses to the wave in year one because it carries its whole build cost. If next year's `K` falls to $20,000, the same row saves $238,991 and passes the wave. Score multi-year levers over the years they run.
- **`C` is the term studios forget.** Honest players pay it in false bans, lost features and friction, and they pay it whether or not the lever works. Put a number on it before you ship, and track it after, as MMO402 week 7 does for appeals.
- **`h` is not constant.** A PvP cheater ruins other people's matches today, so `h` is high and long `act` is expensive. A farming bot spreads harm through the economy more slowly. Score each threat with its own `h`.
- **The card ranks levers. It does not choose the timing.** How long a wave should wait is week 5's model. The card tells you whether waves are the right family of lever at all.

### Check yourself (worked example)

1. A bot program has `detect = 4`, `act = 0`, `down = 1`. Should you spend on detection or on attacker downtime? By how much does uptime fall for one day of each?
2. Rescore the delayed wave with `down = 10`. Does it still beat instant bans?

<details>
<summary>Answers</summary>

1. `live / down = 4`, so a day of downtime is worth four days of detection. Now `uptime = 4 / 5 = 0.8`. One day less `detect` gives `3 / 4 = 0.75`. One day more `down` gives `4 / 6 = 0.667`. Spend on downtime.
2. `uptime = 20 / 30 = 0.667`, harm left `= 243,333`, saving `= 365,000 − 243,333 − 50,000 = 71,667`. It still beats instant bans ($41,250), by much less. With `down` below about 6.7 days the wave's uptime is above 0.75 and it loses.

</details>

## 3. Case: RuneScape, 2007 to 2011, from trade limits to a bot nuke

Put this case through the template. It shows a studio trying three levers in four years.

**Asset.** RuneScape gold, sold for real money (MMO304 week 11 covers the market side).

**Attacker economics.** Gold farming required moving gold from farming accounts to buyers. The trade was the choke point.

**Control, attempt 1: restrict trade (2007 to 2011).** Jagex announced a trade limit on 10 December 2007 and applied it to all players on 2 January 2008. Unbalanced trades were blocked, and during the period without free trade, free players could hand over at most 10,000 coins of excess value every 15 minutes. On the card this lowers `h` per bot, since gold that cannot be delivered is worth little to a buyer. It also put a large `C` on every honest player who wanted to give a friend a gift. Players protested, and the limit was lifted on 1 February 2011 after a referendum in which 91% voted for the return of free trade.

**Control, attempt 2: structural fix (October 2011).** Nine months later came ClusterFlutterer. Jagex's claim that it targeted "98% of the bots seen in game" is a studio estimate, and the RuneScape Wiki records that afterward free worlds were heavily depopulated. Label that as observation, not a measurement of bot share. On the card it is the structural row, with a long `act` (a secret build) and a very long `down`.

**Control, attempt 3: a narrow trade limit (November 2011).** On 22 November 2011 Jagex added a limit of 25,000 coins a day on what new accounts that had never paid for membership could give away. It lifts permanently once the account pays. This cuts `h` for the attacker's cheapest accounts while keeping `C` small, because honest new players rarely need to give away large sums.

**Transferable rule.** Blanket restrictions on trade hit the whole population to reach a small attacking one, so `C` swamps the saving and players vote them out. Narrow restrictions that bite on the attacker's cheapest input (new, never-paid accounts) last longer.

## 4. Case: Glider, Warden and the courts

**Asset.** Leveling time in World of Warcraft. Glider, built by Michael Donnelly's company MDY Industries, played the game unattended for its users.

**Control.** Blizzard's terms of use banned bots, and Warden scanned for them.

**Response.** MDY sought a court ruling that Glider was legal, and Blizzard counterclaimed. On 14 July 2008 the U.S. District Court for Arizona found MDY liable for contributory and vicarious copyright infringement and tortious interference. The same court later found MDY liable under the DMCA for trafficking in a tool that gets past Warden. On 14 December 2010 the Ninth Circuit reversed the copyright infringement finding. It held that breaking a term in the license is copyright infringement only if the term is tied to the copyright holder's exclusive rights, and a no-bots rule is not. But it upheld the finding that MDY had violated the DMCA's ban on trafficking in circumvention technology, at least for the content WoW's servers supply, and it did so without requiring any link to actual copyright infringement.

**Outcome.** The legal route worked against a commercial bot maker, but on narrower grounds than the first ruling. Other studios followed with suits against cheat sellers. Nexon was awarded $1.4 million against the operator of a Combat Arms cheat service in 2013. Riot Games won $10 million against the LeagueSharp service in 2017. Blizzard was awarded $8.5 million against Bossland. Bungie won about $4 million in arbitration against AimJunkies on its DMCA claims, then a jury verdict of $63,210 on copyright claims in May 2024, reported as possibly the first jury finding that a cheat maker infringed a game's copyright ([week 12](w12-legal-and-ethical-considerations.md) reads the two awards side by side).

**Model reading.** The break-even line from section 2 explains who gets sued. A lawsuit's legal cost is large and fixed, so it pays only when `h` is large. That happens when the defendant is a supplier whose one product runs thousands of accounts, so the harm of all its customers counts together. Suing one botter would never clear the line. The appeal adds a second lesson. The legal result is uncertain, so "uptime after" is an expected value (MA102 week 4), and a narrower ruling means a smaller drop than you planned for.

**Transferable rule.** Write your terms of service knowing which clauses you may need to enforce in court (MMO402 week 5), and keep technical controls such as Warden in place, because the claim that survived on appeal was about getting past one.

## 5. Case: New World and the price of coming back

**Asset.** New World's gold, and the ability to keep playing after a ban.

**Attacker economics.** New World is buy-to-play. Normally a banned bot account costs the operator a copy of the game. Family sharing on Steam let other accounts play without buying it.

**Response.** In November 2021, about a month after reports that family sharing gave free access, Amazon disabled family sharing for New World, naming bots, gold sellers and ban evaders, while offering help to players who shared for legitimate reasons.

**Model reading.** This is the "close free account" row. Detection and bans did not change. What changed was `down`, because returning after a ban now meant buying a copy, and week 6 shows that a higher account cost can push a bot below its break-even lifetime so that it never returns at all. The collateral `C` is real (families who shared for ordinary reasons), and Amazon's offer of help is an attempt to keep it small. It is the cheapest lever in the case set and the first one to check in any threat model.

**Transferable rule.** Audit every path that creates a playable account for less than your intended price (free trials, family sharing, gifting, promotional keys) as part of threat modeling, before launch.

## 6. What the cases say together

Line the cases up on the card and one pattern stands out. The studios that got lasting results moved `down`, not `detect`. They changed the client's data exposure (ClusterFlutterer), the price of coming back (New World, the 2011 trade limit on never-paid accounts), or the survival of the party supplying patches (the lawsuits). Signatures and waves were necessary, and VAC shows how far careful silence can stretch `down`, but they buy days rather than end the fight.

A second pattern is about `C`. The lever players voted out, the 2008 trade limit, was the one that charged every honest player to reach a few attackers. The levers that lasted were narrow.

A third pattern is about communication. The studios said very little while a countermeasure was being built and quite a lot afterward. That matches the card. Silence protects `down` only while `down` depends on what the attacker knows. Once it does not, publishing numbers costs nothing and restores the trust that silence cost.

## In-class activity (30 minutes)

Groups of three. Each group gets one brief: VAC, ClusterFlutterer, Glider or New World.

1. Fill the seven-row case template for your case using the sources in this lecture. Mark every number as "measured," "studio estimate" or "our assumption."
2. Write your case as one scorecard row. Choose `detect`, `act`, `down`, `K` and `C` (or the legal cost and uptime before and after, for Glider), write one sentence justifying each, and compute uptime and saving with `h = $1,000`.
3. Use `live / down` to name the one term that would move your row most, and change it by 50%. Report the new saving.
4. Present in two minutes. The class votes on which lever would transfer best to the MMO you threat-modeled in week 1.

Expected output: a filled template, a scorecard row with justifications, and the sensitivity result from step 3.

## Common misconceptions

- **"Faster detection is always the best investment."** Only when `live` is short relative to `down`. With `live = 6` and `down = 2`, each day of attacker downtime is worth three days of detection.
- **"A delayed ban means the studio is slow."** The delay is a trade. It adds to `live` to buy a much larger `down`. If it does not buy that, it is just slow, and the card shows it.
- **"A structural fix that costs more than a ban wave is worse."** Its build cost falls in one year and its `down` keeps paying. Score it over the years it runs.
- **"Suing cheat makers is about the damages."** Awards are often hard to collect. The value is shutting down the supplier whose patches keep `down` short for every customer at once.

## Check yourself

1. A lever has `detect = 10`, `act = 5`, `down = 45`, `K = $60,000`, `C = $15,000` and `h = $800`. Compute uptime, harm left and saving.
2. A lawsuit would cost $300,000 a year and cut uptime from 0.6 to 0.2. What is the smallest `h` at which it pays?
3. A blanket trade limit cuts uptime from 0.75 to 0.2 but costs honest players $250,000 a year. A limit on never-paid accounts cuts it only to 0.3 and costs $20,000. With `h = $1,000` and no `K`, which saves more?
4. Jagex announced ClusterFlutterer four days ahead. Explain with the card why the same announcement for a VAC signature would be costly.

<details>
<summary>Answers</summary>

1. `live = 15`, `uptime = 15 / 60 = 0.25`. Harm left `= 365 × 800 × 0.25 = 73,000`. Saving `= 292,000 − 73,000 − 60,000 − 15,000 = 144,000`.
2. `h ≥ 300,000 / (365 × 0.4) = 2,054.8`, so about $2,055 per live day.
3. Blanket: harm left `73,000`, saving `= 365,000 − 73,000 − 250,000 = 42,000`. Narrow: harm left `109,500`, saving `= 365,000 − 109,500 − 20,000 = 235,500`. The narrow limit wins by a wide margin, which is RuneScape's story.
4. A signature's `down` comes from the cheat maker not knowing what you detect. Announcing it lets them patch before the ban, so `down` falls toward zero and uptime toward 1. ClusterFlutterer's `down` came from a change in how the client works, which the bot makers could not patch around in four days whether or not they knew.

</details>

## Lab hook

[Lab 14, response scorecard](../labs/lab14.md). You implement the scorecard, add multi-year costs and the lawsuit break-even, score six levers for three invented games, and write a one-page recommendation naming the lever each game should fund first.

## Sources

- Wikipedia, "Valve Anti-Cheat" (accessed September 2026). Immediate flagging, bans "days or even weeks" later, waves, no disclosure of the cheat or detection method; permanent bans since VAC2 in 2005; from May 2016, bans for accounts registered with the same phone number as a banned account and a three-month bar on re-registering that number.
- RuneScape Wiki, "ClusterFlutterer" (accessed September 2026). Update of 25 October 2011 aimed at reflection and injection bots; Jagex's 98% estimate; over 1.5 million accounts recently banned; depopulated free worlds afterward.
- RuneScape Wiki, "Update:Bot-Busting and Bonuses For All" (Jagex news post of 21 October 2011, as archived on the wiki). Announcement four days ahead, "permanently preventing" reflection bots, secrecy during development.
- RuneScape Wiki, "Trade limit" (accessed September 2026). Announcement 10 December 2007, applied 2 January 2008, 10,000 coins per 15 minutes for free players, referendum closing 14 January 2011 with 91% in favor of free trade, and the 25,000-coins-per-day limit for never-paid accounts from 22 November 2011. The return date of 1 February 2011 as cited in MMO304 week 11.
- Wikipedia, "MDY Industries, LLC v. Blizzard Entertainment, Inc." (accessed September 2026). Glider; district court ruling of 14 July 2008; Warden and the DMCA; Ninth Circuit ruling of 14 December 2010 and its requirement of a link between the license term and the copyright holder's exclusive rights. The case citation 629 F.3d 928 (9th Cir. 2010) as given in MMO402 week 5.
- Wikipedia, "Cheating in online games" (accessed September 2026). Nexon's $1.4 million award (April 2013), Riot's $10 million against LeagueSharp (January 2017), Blizzard's $8.5 million against Bossland. The Verge, "A jury hands Bungie a victory in a landmark anti-cheating decision", 25 May 2024. The $63,210 jury award and an arbitration award of about $4 million on the DMCA claims, then under appeal (Wikipedia gives $4.3 million).
- Wikipedia, "New World (video game)" (accessed September 2026). Family sharing access reported in October 2021 and disabled about a month later, citing bots, gold sellers and ban evaders.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley. Chapter titles as listed by Open Library.
- All scorecard parameters (`detect`, `act`, `down`, `K`, `C`, `h`, legal cost) are teaching assumptions, not figures from any studio.

## Interactive spec: examples/w14-response-scorecard.html

**Purpose.** Show that an attack's uptime is `live / (live + down)`, so when `down` is short, shortening detection barely helps and stretching the attacker's downtime helps a lot. Put six response levers on one card so students see that the cheapest lever can top it.

**Model** (exact):

```
live      = detect + act
uptime    = live / (live + down)          (uptime = 1 when down = 0)
harm left = 365 × h × uptime
saving    = 365 × h − harm left − K − C
lawsuit break-even h = L / (365 × (u_before − u_after))
```

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.

- Left panel, "One year of this attack." A horizontal strip 365 days long for the selected lever. Repeat cycles from day 0: `live` days shaded "live" (accent color), then `down` days shaded "down" (grey), until day 365. Label the strip with the uptime to three decimals and the live-day count, `365 × uptime`, to one decimal. Below the strip, a small readout "a day of downtime is worth `live / down` days of detection" with the ratio to two decimals (show "infinite" when `down = 0`).
- Right panel, "Yearly cost by lever." One horizontal stacked bar per lever in this order: no response, instant bans, faster detection, delayed wave, structural fix, close free account. Segments: harm left, `K`, `C`, each labelled with its dollar value on hover and in a data table below the chart. A vertical line at `365 × h` labelled "do nothing". Sort toggle "sort by saving". Highlight the selected lever. Show saving to the nearest dollar at the end of each bar.
- Below both panels, a "Lawsuit break-even" box with inputs `L` (default 500,000), `u_before` (default 0.75), `u_after` (default 0.10) and the output "pays when h ≥ $N", plus a green or red badge comparing it with the current `h`.

**Controls** (sliders with numeric readouts, keyboard accessible):
- Lever selector (radio buttons, the six levers). Selecting one shows that lever's current values in the sliders. Each lever keeps its own edits while you switch between levers; only "Reset all" restores the defaults below.
- `detect`: 0 to 60 days, step 1.
- `act`: 0 to 120 days, step 1.
- `down`: 0 to 400 days, step 1.
- `K`: $0 to $300,000, step 5,000.
- `C`: $0 to $300,000, step 5,000.
- `h` (global, applies to all bars): $100 to $5,000, step 100, default 1,000.
- "Reset all" button.

Defaults per lever (`detect`, `act`, `down`, `K`, `C`): no response (1, 0, 0, 0, 0), instant bans (6, 0, 2, 40,000, 10,000), faster detection (3, 0, 2, 80,000, 10,000), delayed wave (6, 14, 30, 40,000, 10,000), structural fix (6, 90, 365, 120,000, 30,000), close free account (6, 0, 60, 5,000, 25,000).

**The one insight.** With "instant bans" selected, dragging `detect` from 6 to 1 barely changes the strip or the bar, while dragging `down` from 2 to 10 turns the strip mostly grey. Downtime is the lever when `down` is small.

**Test values** (`h = 1,000`, must match exactly):

| Lever | live | down | uptime | harm left | K + C | saving |
|---|---|---|---|---|---|---|
| no response | 1 | 0 | 1.000 | 365,000 | 0 | 0 |
| instant bans | 6 | 2 | 0.750 | 273,750 | 50,000 | 41,250 |
| faster detection | 3 | 2 | 0.600 | 219,000 | 90,000 | 56,000 |
| delayed wave | 20 | 30 | 0.400 | 146,000 | 50,000 | 169,000 |
| structural fix | 96 | 365 | 0.208 | 76,009 | 150,000 | 138,991 |
| close free account | 6 | 60 | 0.091 | 33,182 | 30,000 | 301,818 |

Further checks: instant bans with `detect = 5` gives uptime 0.714; with `down = 3` gives 0.667; ratio readout at defaults is 3.00. Delayed wave with `down = 10` gives saving 71,667. Lawsuit defaults give break-even $2,107 (red badge at `h = 1,000`, green at `h = 2,200`). With `L = 300,000`, 0.6 and 0.2, break-even is $2,055.

**Accessibility and style.** Use the shared tokens from `templates/interactive-tokens.css`. The data table under the bars is the text alternative; the strip also has a text summary (uptime, live days, cycles). Respect reduced motion. No game logos or art; name games only in lever captions.
