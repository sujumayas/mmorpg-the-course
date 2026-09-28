# MMO305 · Week 05 — Raiding as Organization: Roles, Attendance, Loot Rules (DKP)

**Why this matters:** A raid is the closest thing an MMO has to a workplace. It has a roster, a schedule, job roles and a pay system, and the pay is loot. When 20 or 40 people split a handful of items, the rule for who gets what decides who stays, who recruits and who quits. Players invented those rules because the games didn't, and the rules behave like small economies with inflation, hoarding and newcomer penalties you can compute.

**You will be able to:**
- Compute the roster size a raid needs to field a full group on a given night from members' attendance rates.
- Simulate earned-spent and zero-sum DKP and predict who gets geared first under each.
- Derive the inflation ratio of a points-based loot system and use it to compute how long a new recruit waits for a first item.
- Critique a loot system (DKP, EPGP, gold auctions, game-assigned personal loot) by the behaviour it rewards and the members it drives away.

**Before class:** Malone, K.-L. (2009), "Dragon Kill Points: The Economics of Power Gamers", *Games and Culture* 4(3), 296-316 (the whole paper). Castronova, E. & Fairfield, J. (2006), "Dragon Kill Points: A Summary Whitepaper", SSRN 958945 (10 pages). Reread MMO303 week 5 section 4 on raid composition.

**Prerequisites from earlier courses:** [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md) (how raid size sets tank, healer and DPS slots). [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (how many of `n` show up). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (DKP inflation is the same arithmetic). [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md). This course: [week 4, guilds](w04-guilds-formation-lifecycle-leadership.md) (critical mass and churn).

**Interactive:** [DKP simulator](../examples/w05-dkp-simulator.html) (spec at the end of this lecture). Keep it open during section 3.

---

## 1. A raid is an organization

Last week you modelled a guild as a stock of members. A raid team is a tighter unit inside a guild, and it has every feature of a small firm.

- **Fixed headcount.** Raid size is set by the game. World of Warcraft's original raids, such as Molten Core, took 40 players. From Wrath of the Lich King (2008) new raids came in 10- and 25-player versions. Since Warlords of Draenor (2014), Normal and Heroic scale from 10 to 30 and Mythic is fixed at 20.
- **Job roles.** MMO303 week 5 showed how a boss's damage profile sets the number of tanks and healers. A 20-player raid might need 2 tanks, 4 to 5 healers and 13 to 14 damage dealers. Roles are not interchangeable, so the raid needs enough of each, not just enough people.
- **A schedule.** Raids run on fixed nights for a few hours. Everyone must be online at once.
- **Pay.** Bosses drop a few items. The raid decides who gets them. That decision is the raid's wage system.

The first two problems are logistics. The last one is where raids fall apart.

### Attendance and the roster you actually need

Suppose your raid needs 20 players and each member of the roster shows up on a given night with probability `p`, independently. The number who show up is binomial (MA102 week 6). The chance of fielding 20 from a roster of `R` is

```
P(at least 20) = sum over x = 20..R of C(R, x) × p^x × (1 − p)^(R − x)
```

| Roster size `R` | P(field 20), `p = 0.85` | P(field 20), `p = 0.90` |
|---|---|---|
| 20 | 3.9% | 12.2% |
| 22 | 33.8% | 62.0% |
| 24 | 71.3% | 91.5% |
| 26 | 91.7% | 98.8% |
| 28 | 98.2% | 99.9% |

A roster of exactly 20 players who each attend 85% of the time fields a full raid less than one night in 25. To raid reliably (about 9 nights in 10) at that attendance, you need about 26 players. The six extras are the **bench**: players who sign up, may not play, and still expect some reward for being available.

Now you can see the tension. The raid needs extras who often sit out. The extras need a reason to keep showing up. And at the end of each boss there are two or three items for twenty people. The loot rule has to pay the core, pay the bench, and not drive away new recruits, all at once.

## 2. Loot as an allocation problem

Early MMOs left loot allocation to players. EverQuest's raid bosses dropped a handful of items for dozens of players. World of Warcraft offered group loot options (free-for-all, round-robin, need-before-greed rolls, and a **master looter** who hands out items by hand), but none of them could encode "this person has attended every raid for two months". Guilds wrote their own rules and ran them through the master looter.

The main families are:

- **Random rolls.** Everyone who wants the item rolls; highest roll wins. Fair in expectation, ignores attendance, and a newcomer on their first night has the same chance as a founder.
- **Loot council.** Officers decide. Can weigh everything (attendance, role, who the item helps most) and is only as fair as the officers.
- **Points systems.** Members earn points for attending and spend them on items. The first and most copied is **DKP**, for dragon kill points. Thott created it for the EverQuest guild Afterlife in 1999, and it is named after the game's two original dragon bosses, Lady Vox and Lord Nagafen.

Malone's 2009 study of raiding guilds argues that DKP works less as money than as a **social stabilizer**. It rewards steady participation and loyalty to the guild. Castronova and Fairfield's 2006 white paper points to the hard part. Setting a fair price for each item requires judgment, which is why many guilds switched to auctions where members bid their points. This lecture uses fixed prices so the arithmetic stays visible. Auctions are one of the variants in section 4.

## 3. Worked example: zero-sum versus earned-spent DKP

### The hook

Picture two raiding guilds on the same server. Same boss, same two drops a night, same 10-player raid. Both say they use DKP. In the first, a recruit who attends every night gets their first item on their fifth night. In the second, the same recruit, with the same perfect attendance, waits twenty-three nights while the veterans keep winning.

Both guilds run "DKP." They differ in one number that nobody in either guild wrote down. This worked example finds it.

### The model

Each raider `i` has a balance `B_i`. Each raid night, `n` raiders are present, `k` items drop, and each item has a fixed price `P`. Every present raider earns some points, then the `k` present raiders with the highest balances each take one item and pay `P`. Ties go to roster order. For the whole example, assume every item is an upgrade for everyone (a simplification we remove in section 4).

```
B_i(next night) = B_i + earn_i − P × won_i
```

The two systems differ only in `earn`:

- **Earned-spent DKP** (sometimes called standard or simple DKP): each present raider earns a fixed `e` per night.
- **Zero-sum DKP**: the price of every item is shared out among the raiders present. Each present raider earns `k × P / n` per night, and winners pay `P`.

Now count points. Each night the raid creates `n × e` points (earned-spent) and destroys `k × P` points (spent on items). Their ratio is the **inflation ratio**:

```
ρ = (n × e) / (k × P)
```

- `ρ > 1`: more points are created than spent. Balances climb over time. This is inflation, exactly as in MMO304 week 4.
- `ρ < 1`: more are spent than created. Balances drift negative.
- `ρ = 1`: the total never changes.

Put zero-sum's earning into the ratio: `ρ = n × (k × P / n) / (k × P) = 1`. **Zero-sum DKP is earned-spent DKP with the earning rate locked so that ρ = 1.** That is the whole difference, and it explains everything that follows.

### Numbers you can check: four raiders

Take a tiny raid: 4 raiders A, B, C, D, one item per night, price `P = 40`. Earned-spent pays `e = 20` a night, so `ρ = 4 × 20 / 40 = 2`. Zero-sum pays `40 / 4 = 10` to each present raider. Balances are shown after that night's item is paid for.

| Night | Earned-spent winner | A | B | C | D | Zero-sum winner | A | B | C | D |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | −20 | 20 | 20 | 20 | A | −30 | 10 | 10 | 10 |
| 2 | B | 0 | 0 | 40 | 40 | B | −20 | −20 | 20 | 20 |
| 3 | C | 20 | 20 | 20 | 60 | C | −10 | −10 | −10 | 30 |
| 4 | D | 40 | 40 | 40 | 40 | D | 0 | 0 | 0 | 0 |
| 8 | D | 80 | 80 | 80 | 80 | D | 0 | 0 | 0 | 0 |

Check night 1 of earned-spent. Everyone earns 20, all tie, A wins by roster order and pays 40, so A has `20 − 40 = −20`. Check night 1 of zero-sum. Everyone earns 10, A wins and pays 40, so A has `−30`, and the four balances sum to 0.

Among veterans, both systems do the same thing. Items rotate A, B, C, D. The only visible difference is that earned-spent balances climb by 40 every four nights while zero-sum balances return to 0.

That difference is harmless until someone new arrives. After night 8, D leaves and newcomer E takes D's place with a balance of 0.

| | Veterans' balance when E joins | E's first item | Nights E attended before it |
|---|---|---|---|
| Earned-spent (`ρ = 2`) | 80 each | night 18 | 10 |
| Zero-sum (`ρ = 1`) | 0 each | night 12 | 4 |

Under zero-sum, E joins at the average and gets an item after one full turn of the rotation, just like anyone else. Under earned-spent, E joins 80 points behind a group that keeps inflating. You can run this table by hand in ten minutes; do it once.

### The newcomer's wait, in one formula

Scale up. A 10-player raid (`n = 10`), 2 items a night (`k = 2`), price `P = 50`. A newcomer replaces a veteran after `T = 20` nights. Vary the earning rate `e`:

| Earning per night `e` | Inflation ratio `ρ` | Veterans' average balance at night 80 | Newcomer's first item (nights after joining) | Newcomer's items by night 80 | Each veteran's items by night 80 |
|---|---|---|---|---|---|
| 5 | 0.5 | −394 | 1 | 13 | 15-16 |
| 10 (= zero-sum) | 1 | 0 | 5 | 12 | 16 |
| 20 | 2 | +778 | 23 | 8 | 16-17 |
| 30 | 3 | +1,556 | 41 | 4 | 16-17 |

Where do 23 and 41 come from? When the newcomer joins, the veterans are ahead by about `T × e × (1 − 1/ρ)`, the points inflation has piled on each of them. The newcomer closes that gap at `k × P / (n − 1)` a night, because the veterans keep paying for every item while the newcomer only earns. Add the ordinary wait for a turn in the rotation, `n / k` nights:

```
first-item wait ≈ n/k + T × (ρ − 1) × (n − 1)/n        for ρ ≥ 1
```

With `ρ = 2`: `10/2 + 20 × 1 × 9/10 = 5 + 18 = 23`. With `ρ = 3`: `5 + 36 = 41`. With `ρ = 1`, the second term vanishes and every newcomer waits one rotation, whatever the guild's age. Check the four-raider case too: `4/1 + 8 × 1 × 3/4 = 4 + 6 = 10` nights.

Two things in this formula matter for design. The wait grows with `T`, the **age of the guild**. An inflating DKP system gets harder on recruits every week it runs, which is the opposite of what a guild that needs recruits wants (week 4). And when `ρ < 1`, newcomers are favoured, because the veterans are in debt and a fresh 0 is the richest balance in the raid.

### Who gets geared first when attendance varies

Now let raiders miss nights. Take a roster of 12: six attend every night, three attend 75% of nights, three attend 50%. Two items drop a night at `P = 50`, and the raid runs 40 nights. On average 9.75 raiders are present. This needs a Monte Carlo run (MA102 week 11); the table shows the mean of 2,000 simulated seasons.

| System | `ρ` (at 9.75 present) | Items per 100% raider | Items per 75% raider | Items per 50% raider | 50% raider's first item (mean night) | 50% raiders with no item in 40 nights |
|---|---|---|---|---|---|---|
| Earned-spent, `e = 10` | about 0.98 | 8.1 | 6.3 | 4.2 | 6.6 | 0% |
| Zero-sum | 1 | 8.2 | 6.2 | 4.0 | 6.5 | 0% |
| Earned-spent, `e = 20` | about 1.95 | 9.6 | 5.6 | 1.9 | 11.9 | about 7% |

The first-item column averages only the raiders who got an item during the 40 nights. The last column counts the ones who did not. Read the two together. Under `e = 20` the typical half-time raider waits about twice as long, and one in fourteen goes the whole season with nothing.

With `ρ` near 1, items are shared roughly in proportion to attendance. A 50% raider gets about half of what a 100% raider gets, which is what most guilds say they want. With `ρ` near 2, the half-time raider gets a fifth. Inflation turns a proportional reward into a winner-take-most one. The full-time raiders earn faster than the item prices drain them, their balances pull away, and the part-timers fall behind for good. This is the positive feedback loop of GD102 week 3 hiding inside a spreadsheet.

So, who gets geared first? Under every version, the players who attend most. Under inflating earned-spent, they also get geared *most*, far beyond their share of attendance, and recruits and part-timers wait.

### A visual you can move

Open the interactive. The top panel shows every raider's balance over 60 nights, with the newcomer highlighted. The bottom panel shows the cumulative items each raider has received. Start with zero-sum. The balance lines braid around 0 and the item staircases climb together. Now switch to earned-spent and drag `e` from 10 up to 30. The balance lines lift off and fan out, the newcomer's line starts far below the pack, and the newcomer's item staircase goes flat for weeks. The readout shows `ρ` and the predicted wait beside the simulated one. Then set `e` to 5 and watch the newcomer jump the queue.

### Cross-game recognition

The same inflation ratio shows up wherever players or designers split scarce loot.

**EPGP (a World of Warcraft guild addon by Alkis Evlogimenos, maintained through Battle for Azeroth).** Members earn **effort points** (EP) for attending and are charged **gear points** (GP) for items. Priority is the ratio `PR = EP / GP`, and the addon adds a base GP to every member so no one divides by zero. Periodically, both EP and GP are cut by the same **decay** percentage. In our model, decay is a sink on points, so it pulls `ρ` back toward balance over time. A veteran's hoard shrinks by the decay rate every period, so the gap a newcomer faces stops growing with `T`. EPGP is earned-spent DKP with a built-in fix for the inflation problem this lecture found.

**GDKP (Classic World of Warcraft).** Raiders bid in-game gold for items, and the winning bids are split among all raid members. That is exactly the zero-sum structure: the winner pays, and the payment is shared out to the raid. The difference is the currency. Gold comes from outside the raid, so a newcomer with gold can buy on night one, and a veteran's attendance earns a share of the pot rather than priority. It removes the newcomer penalty and replaces it with a wealth advantage.

**World of Warcraft personal loot (Battle for Azeroth, patch 8.0.1, 2018).** Patch 8.0.1 removed the ability to change loot modes and made personal loot the only option. The game picks which players receive an item, and nobody can trade or assign drops the way a master looter could. In model terms, the game set everyone's earning to "be present" and took the allocation out of players' hands. DKP had nothing left to allocate. Current retail raids default to group loot rolls, and master loot has not returned.

**EverQuest (1999).** DKP itself. Afterlife's rule turned attendance into priority because the game had no memory of who had shown up. The recurring lesson across all four cases is that when the game provides no allocation rule, players build one, and its inflation ratio decides who it favours.

### Eyes-open design judgment

- **Zero-sum is not automatically better.** It pays only when items drop. A night of wipes on a new boss earns nothing, so the raid's hardest nights are unpaid. A zero-sum guild that adds an attendance bonus to fix this breaks `ρ = 1` and brings inflation back.
- **Zero-sum leaks when people leave.** A departing member takes their balance with them. If they leave in debt, the rest of the raid's total goes up; if they leave rich, it goes down. Over a year of churn (week 4), the sum drifts.
- **Inflation can be a choice.** A guild that wants to reward seniority can run `ρ > 1` on purpose. It should know that the price is recruits' patience, and that the price grows each week.
- **Every points system rewards attendance, which is its point.** It also punishes real life. A player who misses two weeks for exams falls behind under inflation and never catches up. Decay (EPGP) or caps soften that.
- **As a game designer, you can take the problem away.** Personal loot removes allocation fights and also removes the guild's tool for rewarding loyalty. Malone's reading of DKP as a social stabilizer suggests that is a real loss. Decide what you want the loot rule to do for the guild before you pick one.

### Check yourself (worked example)

1. A 20-player raid uses earned-spent DKP with `e = 15` per night, 3 items per night, fixed price `P = 80`. What is `ρ`? Is the system inflating?
2. In that raid, a recruit replaces a veteran after 30 nights. Estimate the recruit's wait for a first item.
3. The officers want the wait from question 2 to be no more than 10 nights for a recruit who joins after 30 nights. What price `P` should they set, keeping `e = 15`?

<details>
<summary>Answers</summary>

1. `ρ = 20 × 15 / (3 × 80) = 300 / 240 = 1.25`. Yes, it inflates by 60 points a night across the raid.
2. `n/k + T(ρ − 1)(n − 1)/n = 20/3 + 30 × 0.25 × 19/20 ≈ 6.7 + 7.1 ≈ 14` nights.
3. The rotation alone takes about 6.7 nights, so the inflation term must be at most 3.3: `30 × (ρ − 1) × 0.95 ≤ 3.3` gives `ρ ≤ 1.116`. Then `300 / (3P) ≤ 1.116` gives `P ≥ 89.6`. A price of 90 works (ρ ≈ 1.11, wait ≈ 6.7 + 3.2 = 9.8 nights); 85 does not (ρ ≈ 1.18, wait ≈ 11.7).

</details>

## 4. Beyond fixed prices: what real raids add

The model left out three things real raids care about. Each one changes who gets geared first.

**Not every item is wanted by everyone.** A plate chest only goes to plate wearers. Split the raid into gear groups and each group runs its own queue on its own items. A class with few members competes against few people and gears fast; a crowded class waits. That is a composition problem (MMO303 week 5) turning into a loot problem, and it is a common cause of officers "recruiting for gear" instead of for skill.

**Auctions instead of prices.** Many DKP guilds let members bid their points. Castronova and Fairfield's white paper favours this because it avoids officers guessing prices. Auctions let players reveal how much they want an item, and they let rich veterans outbid everyone for the best item of the tier. In an inflating system, bids inflate too, so newcomers are priced out even of items the veterans don't need.

**Minimum bids, caps and decay.** A cap on balances stops hoarding and bounds the newcomer gap at the cap. Decay (as in EPGP) shrinks old balances by a fixed percentage. Both are sinks, the same tools you met for gold in MMO304.

## 5. Raid leadership and the bench

The raid leader runs the encounter. The loot officer runs the pay system. In a healthy raid, these are different people, because the person calling mechanics during a fight should not also be the person everyone is angry at afterward.

The bench raises a pay question points systems handle explicitly. A benched player gave up their evening to be available. EPGP lets officers award EP to **standby** players at a set percentage of what raiders earn; the addon's default is 100%. Paying the bench fully keeps them coming back, and it adds points without adding items, which raises `ρ`. Paying them nothing drives them away and shrinks the roster below what the binomial table in section 1 says you need.

This is where the week 4 model reconnects. A loot system that punishes newcomers lowers `R`, the guild's recruitment. A loot system that drives off part-timers raises `c`. Either can push a guild toward its critical mass, and the officers who chose the rule may never connect the two.

## In-class activity (25 minutes)

Pairs. You are the officers of a 20-player raid with a roster of 26 and two items per boss, four bosses per night.

1. Pick earned-spent or zero-sum. Choose `e` (if earned-spent) and `P`, and compute `ρ` for a night with 20 present.
2. Estimate how long a recruit who joins after 12 weeks (two raid nights a week) waits for a first item.
3. Decide what the six bench players earn on a night they sit out, and recompute `ρ` with them included.
4. Swap with another pair. Find the member of their raid who is most likely to quit under their rules, and say why in one sentence.

Expected output: a one-paragraph loot policy with your numbers, the recruit's wait, the bench rule and the quitting member your partners found.

## Common misconceptions

- **"DKP is one system."** It is a family. Earned-spent and zero-sum behave the same among veterans and very differently for newcomers, part-timers and old guilds.
- **"Zero-sum means nobody gains."** The total is fixed, not each balance. Individual balances move every night; zero-sum only guarantees that the average stays where it started.
- **"Inflation doesn't matter because everyone's points inflate equally."** Only for people who were there from the start and attend equally. Anyone who joins later or attends less falls behind, and the gap grows with the guild's age.
- **"Personal loot solved raid drama."** It solved allocation fights. It also removed the guild's way to reward attendance and loyalty, which DKP existed to do.

## Check yourself

1. A roster of 24 players each attends 90% of nights, independently. What is the chance of fielding a 20-player raid? What if attendance drops to 85%?
2. A 25-player raid runs zero-sum DKP with 3 items a night at `P = 50`. How many points does each present raider earn per night? A night ends in wipes and no items. What does each raider earn?
3. Under earned-spent DKP with `ρ = 1.5`, a guild has run for 40 nights with `n = 10` and `k = 2`. A recruit joins. Estimate their wait for a first item. The guild then starts applying a 10% weekly decay to all balances. Say in one sentence why the wait for the next recruit is shorter.
4. A guild switches from earned-spent (`ρ = 2`) to zero-sum by resetting everyone to 0. Which members gain from the switch, and which lose?

<details>
<summary>Answers</summary>

1. From the table in section 1: 91.5% at `p = 0.90`, 71.3% at `p = 0.85`.
2. `k × P / n = 3 × 50 / 25 = 6` points per night. A night with no items earns 0 under pure zero-sum.
3. `10/2 + 40 × 0.5 × 9/10 = 5 + 18 = 23` nights. Decay removes a fixed share of every balance each week, so the veterans' lead stops growing with the guild's age and is bounded, and the recruit faces a smaller gap.
4. Recent recruits and part-timers gain, because the gap they faced disappears. Long-serving full-time raiders with large balances lose their banked priority. Expect those veterans to object, and expect the officers to face the storming stage of week 4.

</details>

## Lab / assignment hook

[Lab 05, DKP simulator](../labs/lab05.md). You build the model in this lecture in a spreadsheet or a short Python script, reproduce the tables in section 3, then design a loot rule for a fictional guild's roster and defend it with simulated numbers. It feeds the final design project, where your social system must include a reward-allocation rule.

## Sources

- Warcraft Wiki, "Dragon kill points". DKP created by Thott of the EverQuest guild Afterlife (1999), named for Lady Vox and Lord Nagafen; earned-and-spent points; GDKP in Classic World of Warcraft, with the winning gold bid split among all raid members.
- Wikipedia, "Dragon kill points" (accessed 2026). Zero-sum DKP redistributes the price among raid members so the raid's total is constant; simple DKP pays a fixed amount per raid; auction variants.
- Malone, K.-L. (2009). "Dragon Kill Points: The Economics of Power Gamers." *Games and Culture* 4(3), 296-316. DKP as a social stabilizer rewarding participation and loyalty.
- Castronova, E. & Fairfield, J. (2006). "Dragon Kill Points: A Summary Whitepaper." Rational Models Seminar, University of Chicago. SSRN 958945. Difficulty of pricing items; auctions as an alternative.
- EPGP addon for World of Warcraft, by Alkis Evlogimenos, source code (fork iceflame5/epgp on GitHub, version v7.0.0 alpha, interface 80000, last updated January 2021). `epgp.lua`: priority sorted by `EP / GP`, base GP added to stored GP, `DecayEPGP` reduces all EP and GP by a configured percentage. `guild_info.lua`: defaults decay 0%, base GP 1, standby ("extras") EP 100%. https://github.com/iceflame5/epgp
- Warcraft Wiki, "Loot" (patch history and current). Patch 8.0.1: loot mode changes removed and personal loot made the sole option; current retail: group loot is the default for all raid difficulties and personal loot the default in dungeons.
- Warcraft Wiki, "Raid" and "Flexible Raid". 40-player original raids (Molten Core); 10- and 25-player versions from Wrath of the Lich King; 10 to 30 flexible sizes and 20-player Mythic from patch 6.0.2.
- Simulated values in section 3 were computed by the author with the rules stated in the model (ties to roster order, 2,000 seasons for the attendance table). The interactive reproduces them.

## Interactive spec: examples/w05-dkp-simulator.html

**The one insight:** zero-sum DKP is earned-spent DKP with the inflation ratio `ρ = n × e / (k × P)` locked at 1. When `ρ > 1`, veterans' balances lift away from zero, a newcomer starts far behind, and the wait for a first item grows with the guild's age. The linked balance and item plots make the newcomer's flat staircase impossible to miss.

**Layout.** Two stacked panels sharing an x-axis (night 1 to 60, extended to `T + predicted wait + 10` nights when that is larger, rounded up to a multiple of 10), then a readout strip and a controls block. At 1280px, controls sit to the right of the panels; at 390px, controls go below.

- **Top panel, balances.** One line per raider (up to 12), newcomer drawn thicker in the accent token colour, departing veteran's line ends where they leave. A horizontal line at 0. A dashed vertical line at the newcomer's join night.
- **Bottom panel, items received.** Cumulative items per raider as step lines, same colours. A marker on the newcomer's first item, labelled with the night.

**Controls.**

- System: segmented control "Earned-spent" / "Zero-sum".
- Raiders present `n`: 4 to 12, default 10.
- Items per night `k`: 1 to 4, default 2.
- Price `P`: 10 to 100, step 5, default 50.
- Earning per night `e` (earned-spent only; disabled with a note under zero-sum): 0 to 40, step 1, default 20.
- Newcomer joins at night `T + 1`: `T` from 0 to 40, default 20. The newcomer replaces the last roster member.
- Attendance mode: "Everyone attends" (deterministic) or "Mixed attendance" (roster of `n + 2`, first half attend 100%, next quarter 75%, rest 50%, rounded; uses a seeded random generator with a "Reroll" button and a "Run 500 seasons" button that shows mean items per attendance group in a small table).
- Preset buttons: "Hand table (4 raiders)" sets `n = 4, k = 1, P = 40, e = 20, T = 8`; "Lecture default" sets `n = 10, k = 2, P = 50, e = 20, T = 20`.

**Rules (exactly).** Each night:

```
present = everyone active (deterministic mode) or each active raider with probability a_i (mixed mode)
earned-spent: B_i += e for each present i
zero-sum:     B_i += k × P / |present| for each present i
repeat min(k, |present|) times:
    w = present raider (not yet a winner tonight) with highest B; ties to lowest roster index; newcomer has the highest index
    B_w −= P; items_w += 1
```

**Readouts.** `ρ = n × e / (k × P)` (shows 1.00 under zero-sum), total points in the system, veterans' mean balance, the newcomer's simulated first-item night, and the predicted wait `n/k + max(0, T × (ρ − 1) × (n − 1)/n)` beside it.

**Test values (deterministic mode).**

| Preset / settings | Check |
|---|---|
| Hand table, earned-spent | Night 1 balances −20, 20, 20, 20; night 4 all 40; newcomer E (joins night 9) first item night 18 |
| Hand table, zero-sum | Night 1 balances −30, 10, 10, 10; night 4 all 0; newcomer first item night 12 |
| Lecture default, `e = 5` | `ρ = 0.5`; newcomer first item night 21 (wait 1) |
| Lecture default, `e = 10` or zero-sum | `ρ = 1`; newcomer first item night 25 (wait 5); both runs identical |
| Lecture default, `e = 20` | `ρ = 2`; newcomer first item night 43 (wait 23); predicted 23 |
| Lecture default, `e = 30` | `ρ = 3`; newcomer first item night 61 (wait 41); x-axis extended to 80 |

**Mixed attendance check** (roster 12: 6 at 100%, 3 at 75%, 3 at 50%, `k = 2`, `P = 50`, 40 nights, 500 or more seasons): mean items per raider about 8.1 / 6.3 / 4.2 for earned-spent `e = 10`, about 9.6 / 5.6 / 1.9 for `e = 20`, about 8.2 / 6.2 / 4.0 for zero-sum, each within ±0.3. The 50% group's mean first-item night counts only raiders who got an item, and the table shows the share who got none: about 6.5 (0%) for `e = 10` and zero-sum, about 11.9 (about 7%) for `e = 20`, each within ±0.5.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline; raider colours from the categorical tokens, newcomer always the accent colour. Keyboard operable controls with visible focus. A text summary under each chart for screen readers (newcomer's first-item night, `ρ`). Respect `prefers-reduced-motion` (no animated replay; a "Play" button steps nights only when motion is allowed). No game art or logos.
