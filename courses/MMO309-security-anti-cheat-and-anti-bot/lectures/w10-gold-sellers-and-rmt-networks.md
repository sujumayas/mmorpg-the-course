# MMO309 · Week 10 — Gold Sellers and RMT Networks

**Why this matters:** A gold seller is a supply chain, with farm accounts at one end and paying customers at the other. If you ban only the accounts you can see, the chain replaces them for a few dollars each and keeps shipping. The accounts that hold the chain together are few and valuable, and they are visible only when you look at who gives gold to whom. This week you learn to look.

**You will be able to:**
- Map a real-money trading (RMT) operation onto a trade graph and name the role each account plays in it.
- Compute precision, recall and gold seized for per-account and graph-based detection rules on a labelled server.
- Design a guilt-by-association rule that expands from a confirmed hub without sweeping in guildmates and theft victims.
- Critique an anti-RMT plan by where in the chain it strikes and what it costs honest players.

**Before class:** Keegan, B., Ahmed, M. A., Williams, D., Srivastava, J. & Contractor, N. (2010), "Dark Gold: Statistical Properties of Clandestine Networks in Massively Multiplayer Online Games", *IEEE SocialCom 2010*, the abstract and the results on connectivity and brokers. CCP's dev blog "Unholy Rage" (17 August 2009), about 10 minutes. Hoglund & McGraw, *Exploiting Online Games* (2007), the chapter on money and why people cheat.

**Prerequisites from earlier courses:** [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (why RMT exists, the farmer's cost per gold, and the black-market price band under a token). [MMO305 week 9, toxicity research and interventions](../../MMO305-social-systems-and-online-behaviour/lectures/w09-toxicity-research-and-interventions.md) (precision of punishment and the base rate). [DB201 week 3, SQL I](../../DB201-data-persistence-and-telemetry/lectures/w03-sql-i-select-join-aggregate.md) (the joins and group-bys you will use to build the graph). From this course, [week 6 on botting economics](w06-botting-economics.md) and [week 7 on behavioral features](w07-bot-detection-behavioral-features.md).

**Interactive:** [examples/w10-follow-the-gold.html](../examples/w10-follow-the-gold.html).

---

## 1. An RMT operation is a supply chain

In MMO304 week 11 you met real-money trade from the economist's side: why players buy gold, what a sanctioned token does to its price, and what a farm account costs to run. This week you sit on the other side of the table, as the person who has to find and dismantle the operation.

Start with what the operation has to do. Every gold-selling business, whatever game it works in, must solve five problems.

1. **Produce.** Gold has to come from somewhere. Most of it comes from farm accounts, usually bots, running the most profitable activity in the game around the clock. Some comes from stolen accounts, whose owners' gold and items are stripped and sold.
2. **Consolidate.** Hundreds of farm accounts each hold a little gold. The operation moves it into a small number of storage accounts before selling. Security teams call these **mules** or **banks**. A mule is an account whose job is to hold and move value, not to play.
3. **Sell.** A website or a marketplace listing takes the order. Advertising reaches players through in-game spam, whispers and forum posts.
4. **Deliver.** A mule, or a delivery account fed by a mule, hands the gold to the buyer. The handover has to look like something the game allows: a direct trade, a mailed parcel, or a rigged auction where the buyer lists a worthless item and the seller buys it for a fortune.
5. **Get paid and survive.** The payment happens outside the game, sometimes with stolen cards that later turn into chargebacks. The operation replaces banned accounts, rotates IP addresses and changes its patterns when bans arrive.

Research on real data agrees with this picture. Keegan and colleagues (2010) built trade networks from anonymized data of a large commercial MMO and found that gold farmers had distinctive behavior, but that the farmers' signatures were masked by brokering affiliates, the accounts in the middle. They compared the structure to a real-world drug trafficking network and found the same pressures at work: secrecy, resilience and efficiency. Kwon and colleagues (2016) studied a large-scale MMORPG with its operator's cooperation. They reported that earlier detection work could find individual gold farmers but not whole gold farming groups with their internal hierarchies. They also reported that these groups hid by forming front organizations, concealing their money and changing trade patterns after bans. They built a graph of economic transactions and used features of that graph to identify groups in their entirety.

Two words from those papers organize this lecture. **Hierarchy** means the chain has a shape, with many producers feeding few consolidators. **Adaptation** means the chain changes when you push on it, which is why [week 5](w05-memory-editing-and-client-integrity.md) models ban timing and week 6 prices the operator's response.

### The trade graph

A **trade graph** is a directed graph built from your server logs. Each account is a node. Each transfer of value is an edge from giver to receiver, weighted by the value moved. You already log trades, mail, auction purchases and guild bank deposits. The graph is a join over those tables.

One refinement makes the graph far more useful. Most trades are **reciprocal**: gold for an item of similar market value. RMT flows are **one-way**: the farm gives gold to the mule and gets nothing back inside the game. The payment happens off-platform. So compute, for each transfer, the value given minus the market value received, and keep only the edges where that net value is large. Call these **gift edges**. An auction that sells a grey item for 50,000 gold becomes a gift edge from buyer to seller once you price the grey item at its vendor value.

On gift edges, two numbers describe an account's position in the chain.

- **Fan-in** is the number of distinct accounts that sent it gifts.
- **Fan-out** is the number of distinct accounts it sent gifts to.

A farm account has fan-out of one or two (its mule) and fan-in of zero. A mule has high fan-in (its farms) and high fan-out (its buyers). A buyer has fan-in of one per purchase. Most honest players have small numbers on both.

## 2. Worked example: follow the gold

### The hook

On 22 June 2009, during scheduled downtime, CCP banned a little over 6,200 paying EVE Online accounts in one action, which it code-named Unholy Rage. CCP wrote that the banned accounts were about 2% of the active registered accounts, yet average server CPU use per user fell by about 30%. Solar systems that had been clogged by mission-running haulers emptied overnight, and asteroid belts that bots had stripped filled up again.

How did CCP find them? Its blog says the team spent months watching ISK sellers and in particular their supporting groups of macro-miners, ratters and mission farmers, then used that research to identify further accounts. It started from the sellers and worked outward through the accounts that supplied them.

That is the idea of this worked example. Farm accounts are many and cheap, and each one looks like a player who plays too much. The accounts that consolidate the gold are few, and they look like nothing an honest player does. Find those first.

### The model

Label every account on a server as RMT (part of the operation) or honest. Any detection rule flags some set of accounts. Compare the flags with the labels:

```
TP = flagged RMT accounts         (true positives)
FP = flagged honest accounts      (false positives)
FN = RMT accounts not flagged     (false negatives)

precision = TP / (TP + FP)        of the accounts you ban, the share that deserved it
recall    = TP / (TP + FN)        of the operation, the share you caught
seized    = gold held by the flagged RMT accounts
```

You met precision in MMO305 week 9 as "precision of punishment". Recall is its partner. The third number, gold seized, is the one security teams often forget. Banning an account that holds 5,000 gold costs the operation that account. Banning one that holds 2 million costs it a day of production for a whole farm.

The rules we compare are:

- **R1, per-account.** Flag every account that plays 16 or more hours a day.
- **R2, fan-in.** Flag every account with gift fan-in of 10 or more.
- **R3, hub.** R2, plus at least half of the account's gift fan-out goes to strangers, meaning accounts outside its guild.
- **R4, expand.** R3, plus every account that sent gifts to an R3 hub.
- **R5, careful expand.** R3, plus the hub's senders who have no guild and an account younger than 30 days.

R4 and R5 are **guilt by association**: once you trust that a hub is part of the operation, its suppliers become suspects. R5 adds a second condition to each expansion.

### Numbers you can check

Here is a toy server, small enough to reason about and big enough to show the effect. The numbers are invented for teaching.

- 9,600 honest players in 200 guilds of 48. One in 64 plays 17 hours a day (150 players).
- 50 guilds keep a guild-bank alt. Each receives gifts from 20 members and pays out to 10. One of these guilds runs public giveaways, so its bank pays out to 10 strangers.
- The operation has 200 farm accounts (180 run 16 or more hours a day, 20 run shifts of 10 hours) and 4 mules. Each mule collects from 50 farms and pays out to 250 buyers, 1,000 buyers in all. The buyers are ordinary players and are not labelled RMT.
- Six honest accounts were stolen, and the operation stripped their gold into mule 0.
- Farms ship their gold every hour, so each holds about 5,000 gold. Each mule holds 2 million, about two days of its farms' output.

The code below builds this server and scores the five rules. It uses only the standard library.

```python
# A deterministic toy server: 10,000 honest accounts, one gold-selling operation.
accounts = {}   # id -> dict(kind, guild, hours, age, gold)
gifts = []      # one-way transfers: (sender, receiver, amount)

def add(aid, kind, guild, hours, age, gold):
    accounts[aid] = dict(kind=kind, guild=guild, hours=hours, age=age, gold=gold)

# 200 guilds x 48 members; every 64th member plays 16+ hours a day
for i in range(9600):
    add(f"p{i}", "honest", i // 48, 17 if i % 64 == 0 else 4, 400, 30_000)
# 50 guild-bank alts; bank 0 belongs to a "giveaway" guild that pays strangers
for g in range(50):
    add(f"bank{g}", "honest", g, 1, 900, 500_000)
    for m in range(20):                          # 20 members donate to the bank
        gifts.append((f"p{g*48+m}", f"bank{g}", 10_000))
    for m in range(20, 30):                      # bank pays out 10 times
        target = f"p{(g*48+m+2400) % 9600}" if g == 0 else f"p{g*48+m}"
        gifts.append((f"bank{g}", target, 5_000))
# The operation: 4 mules, 200 farmers (180 run 16+ hours), 1,000 buyers
for k in range(4):
    add(f"mule{k}", "rmt", None, 8, 20, 2_000_000)
for f in range(200):
    add(f"farm{f}", "rmt", None, 20 if f < 180 else 10, 10, 5_000)
    gifts.append((f"farm{f}", f"mule{f % 4}", 20_000))
for b in range(1000):
    gifts.append((f"mule{b % 4}", f"p{(b*7) % 9600}", 50_000))
# 6 stolen honest accounts stripped of their gold into mule 0
for v in range(6):
    gifts.append((f"p{9000+v}", "mule0", 30_000))

senders, receivers = {}, {}
for s, r, _ in gifts:
    senders.setdefault(r, set()).add(s)
    receivers.setdefault(s, set()).add(r)

def stranger_share(a):
    out = receivers.get(a, set())
    g = accounts[a]["guild"]
    return sum(accounts[r]["guild"] != g or g is None for r in out) / len(out) if out else 0

hubs = {a for a in accounts if len(senders.get(a, ())) >= 10 and stranger_share(a) >= 0.5}
rules = {
    "R1 hours >= 16": {a for a, d in accounts.items() if d["hours"] >= 16},
    "R2 fan-in >= 10": {a for a in accounts if len(senders.get(a, ())) >= 10},
    "R3 R2 + strangers >= 50%": hubs,
    "R4 R3 + all senders": hubs | {s for h in hubs for s in senders[h]},
    "R5 R3 + new unguilded senders": hubs | {s for h in hubs for s in senders[h]
                                          if accounts[s]["guild"] is None and accounts[s]["age"] < 30},
}
positives = {a for a, d in accounts.items() if d["kind"] == "rmt"}
print(f"{'rule':32}{'TP':>5}{'FP':>5}{'FN':>5}{'precision':>11}{'recall':>8}{'gold seized':>13}")
for name, flagged in rules.items():
    tp, fp = len(flagged & positives), len(flagged - positives)
    fn = len(positives - flagged)
    seized = sum(accounts[a]["gold"] for a in flagged & positives)
    print(f"{name:32}{tp:>5}{fp:>5}{fn:>5}{tp/(tp+fp):>11.1%}{tp/(tp+fn):>8.1%}{seized:>13,}")
```

It prints:

```
rule                               TP   FP   FN  precision  recall  gold seized
R1 hours >= 16                    180  150   24      54.5%   88.2%      900,000
R2 fan-in >= 10                     4   50  200       7.4%    2.0%    8,000,000
R3 R2 + strangers >= 50%            4    1  200      80.0%    2.0%    8,000,000
R4 R3 + all senders               204   27    0      88.3%  100.0%    9,000,000
R5 R3 + new unguilded senders     204    1    0      99.5%  100.0%    9,000,000
```

Check each row by hand from the story. There are 204 RMT accounts (200 farms, 4 mules).

- **R1.** It catches the 180 farms that run 16 hours or more and misses 20 farms and all 4 mules, so `FN = 24`. It also flags the 150 honest heavy players. Precision `180 / 330 = 54.5%`. Nearly one ban in two hits a real person, and the operation loses 180 accounts holding `180 × 5,000 = 900,000` gold.
- **R2.** Fan-in of 10 or more picks out the 4 mules and all 50 guild banks. Precision `4 / 54 = 7.4%`. It catches 2% of the operation, yet seizes `4 × 2,000,000 = 8,000,000` gold, almost nine times what R1 seized.
- **R3.** Asking where the hub's money goes removes 49 guild banks, which pay their own members. Only the giveaway bank stays. Precision `4 / 5 = 80%`.
- **R4.** Expanding to every sender of every hub adds the 200 farms, which is what you wanted. It also adds the giveaway bank's 20 donors and the 6 theft victims. `FP = 1 + 20 + 6 = 27`, precision `204 / 231 = 88.3%`.
- **R5.** Requiring expanded accounts to be new and unguilded keeps the farms and drops the donors and victims, who are old accounts in guilds. The giveaway bank remains the only false positive. Precision `204 / 205 = 99.5%`.

Three lessons are in that table.

1. **The per-account view is noisy.** A farm account, taken alone, looks like a player who plays a lot. Your honest heavy players look the same. In this toy server a threshold of 18 hours would happen to split them, because we drew every heavy player at 17 hours and every long-shift farm at 20. Real heavy players spread across that gap, and an operator who learns the rule runs farms at 17. Even the lucky threshold misses the 4 mules that hold most of the stock. Week 7's behavioral features sharpen the per-account view, but they cannot remove the overlap.
2. **The hub is rare and valuable.** The mules are 4 accounts out of 10,054, yet they hold 89% of the operation's gold on hand (8 million of 9 million). Banning a mule costs the operation stock, not only an account.
3. **Guilt by association inherits the hub's errors and adds its own.** One false hub (the giveaway bank) brought 20 innocent donors with it in R4. The six theft victims were the operation's victims, not its members, and a careless expansion would have punished them twice. Every expansion step needs its own evidence.

### A visual you can move

Open the interactive. The left view is the per-account view: a scatter of hours played per day against gold held, one dot per account, with RMT accounts drawn in a second color that you can toggle off to see what the detector sees. The farms sit inside the cloud of heavy players. The right view is the graph view of the same accounts: guild banks as small stars inside their guilds, the four mules as large hubs, farms as a ring around each mule and buyers fanning out. Drag the fan-in threshold and the stranger-share threshold and watch which nodes light up. The readout shows TP, FP, FN, precision, recall and gold seized for the current rule, with the same numbers as the table above at the default settings. Switch expansion on and watch the donors of the giveaway bank light up, then tick "new and unguilded only" and watch them go dark again. The picture makes one point: the operation is invisible as a cloud of dots and obvious as a shape.

### Cross-game recognition

**EVE Online, Unholy Rage (June 2009).** The hook. CCP studied ISK sellers and their supporting farms before acting, banned about 6,200 accounts at once, and reported the server load and market effects afterward. CCP also reported that some RMT accounts it had banned only temporarily for research came back and flooded the market with implants they had stockpiled, and it then banned those accounts permanently. That is a stockpile held by the network, released the moment the pressure lifted. In this lecture's terms, CCP seized the accounts but not the stock.

**EverQuest II and the Dark Gold networks (Ahmad et al., 2009; Keegan et al., 2010).** The same research group first used EverQuest II data to classify individual gold farmers from per-account statistics, and noted that investigating each suspect costs money, so detection methods must be judged by that cost. Their follow-up built trade networks from anonymized data of a popular online game (the abstract does not name it) and found that farmers were distinctive but that brokers masked them. Rewrite it in this lecture's form: R1-style per-account rules find farmers with limited precision, while the brokering layer is where the network's structure shows. The authors' comparison with drug trafficking is the same point in another field. Police investigations look for the distributors, not the street sellers, because the distributors are fewer and harder to replace.

**Kwon et al. (2016).** Graph features found whole gold farming groups, including their hierarchy, where earlier behavioral detection found individual farmers. The same paper reports the adaptation you should expect: front organizations, concealed money and new trade patterns after bans. A front organization is a hub disguised as something honest, like our giveaway bank in reverse.

**Outside games: payment fraud and money laundering.** Banks' anti-money-laundering teams look for "mule accounts" that receive many small incoming transfers and quickly pass the money on. The vocabulary of this lecture comes from there. The fan-in and fan-out rules above are the textbook starting point, and so is the warning that legitimate collectors, such as a charity or a small business, share the same shape. Our guild banks are the game's version of the charity.

Four contexts, one idea. When value has to flow from many hands to few and back out to many, the few in the middle are both the most valuable target and the easiest to see, provided you look at edges instead of nodes.

### Eyes-open design judgment

- **Use the graph to find hubs, and use per-account features to confirm members.** R5 works because it combines both. Graph position says "this account supplies a hub". Account age and guild membership say "this account is not a player who happens to know the hub".
- **Treat victims as victims.** Stolen accounts appear one hop from a mule, because the operation strips them. Your expansion rule should route them to account recovery ([week 9](w09-account-security-and-takeovers.md)), not to the ban queue. The ledger of a theft victim and the ledger of a farm look the same on one edge. They differ in account history.
- **Expect the shape to change.** Once hubs get banned, operations add layers: farms feed intermediate accounts that feed the mule, or they spread the stock across many small mules. Every extra layer costs the operation time and accounts and leaves more edges in your logs. Chasing the operation into a more expensive shape is a win even if you never catch the last layer.
- **Decide what to do about buyers.** In our server, 1,000 honest-looking players received gold from mules. Banning buyers raises the risk of buying, which pushes up the risk term `r` from MMO304 week 11 and lowers the black-market price ceiling. It also bans players who often spent real money on your game. One middle path is to remove the purchased gold and warn first-time buyers. Whatever you choose, write it down before the first wave.

### Check yourself (worked example)

1. Change the toy server so each mule pays its buyers only from inside one purchased guild (the operation buys a guild and routes deliveries through it). Which rule stops working, and what feature would you add?
2. A second operation uses 40 mules of 5 farms each instead of 4 mules of 50. Using the R3 thresholds, how many of its mules does R3 flag? What does that tell you about fixed thresholds?

<details>
<summary>Answers</summary>

1. R3 depends on the hub paying strangers. If the mule's payouts go to members of its own guild, the stranger share drops to zero and R3 flags nothing, so R4 and R5 find nothing either. Add a feature that does not depend on guild membership, for example how long the receiving accounts have been in that guild, or whether they ever played together (shared groups, shared zones) before the transfer.
2. Each mule now has fan-in of 5, below the threshold of 10, so R3 flags none of them. Fixed thresholds invite the operation to stay just below them. Better rules compare an account with its peers (fan-in far above what accounts of its age and activity normally show) or add up flow across connected accounts, which you will do in the lab.

</details>

## 3. Where to strike in the chain

The table above tells you which accounts you can identify. It does not tell you which bans hurt most. For that, use the farmer's cost model from MMO304 week 11. The cost of producing gold is `(h + A / t) / g`, where `h` is the hourly running cost of an account, `A` the price of a replacement account, `t` the expected hours before a ban and `g` the gold farmed per hour. Bans raise the cost by shortening `t`.

Seizing stock adds a second term. If a mule holds `S` gold when you ban it, and the operation would have sold that gold at price `p` per unit, each mule ban costs the operation `A + S × p`, not only `A`. Put the toy server into those terms, with invented prices of $15 per account and $5 per million gold.

| Ban | Accounts replaced | Stock lost | Cost to the operation |
|---|---|---|---|
| One farm | 1 × $15 | 5,000 gold = $0.03 | $15.03 |
| All 180 farms from R1 | 180 × $15 | 900,000 gold = $4.50 | $2,704.50 |
| One mule | 1 × $15 | 2,000,000 gold = $10.00 | $25.00 |
| All 4 mules and 200 farms (R5) | 204 × $15 | 9,000,000 gold = $45.00 | $3,105.00 |

The table has a surprise in it. In dollars, the stock is small next to the account costs, because gold is cheap per unit. So why did Unholy Rage matter? There are two reasons the table does not show.

First, the mule's real value to the operation is not its gold but its **relationships**. A mule carries the trust of buyers, the delivery routines and the in-game identity the storefront uses. A new farm account is productive within hours. A new mule has to be built, aged and trusted.

Second, **downtime** costs more than stock. When every mule goes at once, orders cannot be delivered until new mules exist. A storefront that misses deliveries loses customers to competitors, and that loss lasts longer than any ban. It is the same lesson [week 5](w05-memory-editing-and-client-integrity.md) draws about ban timing. What matters is not the count of accounts banned, but whether the operation can keep serving customers while you ban them.

## 4. Design levers against RMT networks

Detection is one lever. Designers have others, and each one costs honest players something.

**Make fresh accounts expensive to move gold out of.** RuneScape today limits how much value an account that has never paid for membership can give away in trades: no more than 25,000 coins' worth of items a day, measured against Grand Exchange prices. It was introduced on 22 November 2011 to fight gold farming, and it lifts permanently once the account subscribes. There is no limit on how much a new player can receive, so gifts to newcomers still work. In the chain, this attacks the consolidation step. A farm account on a free account can no longer ship its gold to a mule quickly.

**Make fresh accounts expensive to get.** In November 2021, Amazon Games disabled Steam Family Sharing for New World, citing an increase in bots, gold sellers and ban evaders. Family sharing had let accounts play without buying the game. Removing it raised the replacement cost `A` in the farmer's formula. It also inconvenienced players who shared the game for honest reasons, and Amazon promised them a path to keep playing. [Week 14](w14-case-studies.md) scores the same change as a lever on the operator's downtime.

**Restrict unbalanced trades for everyone.** RuneScape tried this from 2008 to 2011, blocking trades whose values differed too much from market prices. MMO304 week 11 tells that story. In this lecture's terms, the rule removed gift edges from the whole graph. It worked against farms and against every honest gift, and players rejected it.

**Offer a sanctioned channel.** EVE's PLEX, the WoW Token and Old School RuneScape's bonds give buyers a legal way to turn money into currency, which caps the black-market price. MMO304 covers the economics. From the security side, the point is that a sanctioned channel shrinks the customer base the network serves, so each ban wave has a larger effect on a smaller business.

**Break the delivery methods.** Rigged auctions and trade windows are the handover step. Logging the market value of what changes hands, and flagging auctions where a common item sells for far above its price, turns hidden gift edges into visible ones. Few players will notice this lever, which is its main virtue.

A practical rule for choosing levers: prefer the ones that land on edges only an RMT network uses heavily (fresh account to hub, hub to strangers, grey item for a fortune) over the ones that land on every player (all trades, all new accounts).

## In-class activity (25 minutes)

Work in groups of three. Each group gets a printed trade graph of 40 accounts (the instructor's sheet has the labels): nodes with account age and guild, arrows with gold amounts.

1. Circle every account with fan-in of 4 or more. Mark those that send more than half of their gifts outside their guild. (8 minutes)
2. Expand one hop from your marked hubs, but only to senders younger than 30 days with no guild. List the accounts you would ban. (7 minutes)
3. The instructor reveals the labels. Compute your precision and recall. (5 minutes)
4. Name one account you flagged wrongly and the single extra piece of data that would have cleared it. (5 minutes)

Expected output: a list of flagged accounts, your precision and recall, and one sentence naming the missing feature.

## Common misconceptions

- **"Banning more accounts means a better anti-RMT team."** R1 banned 180 accounts and seized 900,000 gold. R3 banned 4 and seized 8 million. Count gold seized and operation downtime, not bans.
- **"If an account sent gold to a gold seller, it is part of the operation."** The six stolen accounts in our server did exactly that. So did the donors to a mistaken hub. Expansion needs its own evidence at every hop.
- **"Gold farmers are bots, so bot detection solves RMT."** Bots produce much of the gold, but the network also runs on stolen accounts, human farmers and delivery accounts that behave like traders. Week 7's features find bots. The graph finds the business.
- **"A sanctioned token ends gold selling."** It caps the price. Operations that can produce gold below the cap keep selling. MMO304 week 11 computes the band.

## Check yourself

1. A rule flags 120 accounts. 90 of them belong to an operation of 150 accounts. Compute precision and recall.
2. In the toy server, suppose the 150 heavy honest players each also received gifts from 12 friends. Which rules change, and how?
3. An operation spreads its stock so that no mule holds more than 200,000 gold, and uses 40 mules. Using the section 3 prices, what does banning all 40 mules cost it in stock? What else changed for the operation, and is that change good for you?
4. Your team proposes banning every account that received gold from a mule. In the toy server that is 1,000 accounts. Give one argument for and one against, each using a number or a model from this course.

<details>
<summary>Answers</summary>

1. Precision `90 / 120 = 75%`. Recall `90 / 150 = 60%`.
2. Their fan-in becomes 12, so R2 flags all 150 as well: FP rises from 50 to 200 and precision falls to `4 / 204 ≈ 2%`. R3 filters them only if they pay out to strangers. They pay out to no one, so their stranger share is 0 and R3 drops them. R4 and R5 are unchanged. The second feature earns its place.
3. Stock is `40 × 200,000 = 8` million gold, $40 at $5 per million, about the same as before. But the operation now has to build, age and run 40 mules instead of 4, which costs time and accounts, and gives you 40 hubs to find instead of 4. Each hub is smaller and closer to the fan-in threshold, so detection is harder per hub. You pushed it into a more expensive shape, which is good, as long as your rules adapt.
4. For: buyers are the demand. Raising their risk raises `r` in the MMO304 ceiling `p_s / (1 + r)` and shrinks the market. Against: at 1,000 accounts, even a small share of mistaken deliveries (gifts, scams, a mule paying a random player to confuse you) creates innocent bans, and buyers are often paying customers. A removal-plus-warning policy keeps most of the deterrent at lower cost.

</details>

## Lab / assignment hook

[Lab 10, follow the gold](../labs/lab10.md). You get a seeded simulated server of about 12,000 accounts with two operations, one of which uses a two-layer mule chain. You build the gift-edge graph, implement fan-in, fan-out and stranger-share features, write an expansion rule, and report precision, recall and gold seized. Deliverable: your script, a results table and a 300-word note to a live-ops lead recommending one rule.

## Sources

- Keegan, B., Ahmed, M. A., Williams, D., Srivastava, J. & Contractor, N. (2010). "Dark Gold: Statistical Properties of Clandestine Networks in Massively Multiplayer Online Games." *2010 IEEE Second International Conference on Social Computing*. doi:10.1109/SocialCom.2010.36. Abstract: farmers show distinctive signatures masked by brokering affiliates, and the networks resemble a drug trafficking network.
- Ahmad, M. A., Keegan, B., Srivastava, J., Williams, D. & Contractor, N. (2009). "Mining for Gold Farmers: Automatic Detection of Deviant Players in MMOGs." *2009 International Conference on Computational Science and Engineering*. doi:10.1109/CSE.2009.307. Abstract: EverQuest II data, logistic regression and classification of gold farmers, and criteria that account for the cost of investigating suspects.
- Kwon, H., Mohaisen, A., Woo, J., Kim, Y., Lee, E. & Kim, H. K. (2016). "Crime Scene Reconstruction: Online Gold Farming Network Analysis." *IEEE Transactions on Information Forensics and Security* (published online 2016). doi:10.1109/TIFS.2016.2623586. Abstract: earlier work detected farmers but not whole groups; groups use front organizations, conceal money and change trade patterns after bans; detection from a trading graph.
- CCP Games, GM Grimmi, "Unholy Rage", EVE Online dev blog, 17 August 2009 (eveonline.com/news/view/unholy-rage). The ban of a little over 6,200 paying accounts on 22 June 2009, about 2% of active registered accounts, the roughly 30% fall in CPU per user, the research on ISK sellers and their supporting macro-miners, ratters and mission farmers, and the implant stockpiles released by temporarily banned accounts.
- RuneScape Wiki, "Trade limit" (retrieved September 2026). The 25,000-coin daily giving limit for accounts that have never had membership, introduced 22 November 2011 to combat gold farming, with no limit on receiving.
- Wikipedia, "New World (video game)" (retrieved September 2026), citing the New World forum post "[Notice] Family Sharing Update", 4 November 2021. Family sharing disabled because of an increase in bots, gold sellers and ban evaders.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley.

## Interactive spec: examples/w10-follow-the-gold.html

**The one insight:** a gold-selling operation is almost invisible as a cloud of individual accounts and obvious as a shape in the trade graph. Rules that find the hubs first and then expand carefully get high precision, high recall and most of the stock.

**Data.** Reproduce the toy server from section 2 exactly in JavaScript, deterministic, no randomness: 9,600 players (`p0`...`p9599`, guild `floor(i/48)`, hours 17 if `i % 64 == 0` else 4, age 400, gold 30,000), 50 banks (`bank0`...`bank49`, guild = index, hours 1, age 900, gold 500,000; 20 donors each, members `g*48 + 0..19`; 10 payouts, to `p((g*48+m+2400) % 9600)` for bank 0 and to `p(g*48+m)` otherwise, `m = 20..29`), 4 mules (no guild, hours 8, age 20, gold 2,000,000), 200 farms (no guild, hours 20 for `f < 180` else 10, age 10, gold 5,000, each sends to `mule(f % 4)`), 1,000 buyer edges from `mule(b % 4)` to `p((b*7) % 9600)`, and 6 victim edges from `p9000`...`p9005` to `mule0`. Put a small seeded jitter on dot positions only, never on the data.

**Layout.** Two panels side by side on desktop (left 45%, right 55%), stacked on mobile with the graph view first. Readout table below both.

**Left panel, per-account view.** Scatter, x = hours per day (0 to 24), y = gold held on a log scale (1,000 to 5,000,000). Jitter x by ±0.8 hours so the 17-hour and 20-hour groups spread. A toggle "show true labels" (default off) colors RMT accounts with the accent color. Flagged accounts get a ring. With labels off, the 180 farms must sit visibly beside the 150 heavy players, not separable by eye on gold alone (farms at 5,000, heavy players at 30,000, same order of magnitude on the log axis).

**Right panel, graph view.** Do not draw 10,000 nodes. Draw the operation, the 50 banks with their donors collapsed into one small cluster glyph each (label "20 donors"), the 6 victims, and buyers collapsed into 4 fans (one per mule, label "250 buyers"). Honest players who are not in any gift edge appear only as a count in a corner label ("9,xxx accounts with no gift edges"). Mules as large circles, farms as a ring of small circles around each mule, banks as small stars. Flagged nodes fill with the flag color. Edges are thin lines with arrowheads; highlight edges into flagged hubs.

**Controls.**
- Rule preset buttons R1 to R5 (keyboard reachable, `aria-pressed`).
- Slider "fan-in threshold", 2 to 60, step 1, default 10.
- Slider "stranger share", 0% to 100%, step 5%, default 50%.
- Slider "hours threshold" for R1, 8 to 24, default 16.
- Checkbox "expand to senders of hubs" and nested checkbox "only new (under 30 days) and unguilded senders".
Presets set the sliders and checkboxes. Moving any control switches the preset label to "custom".

**Readout.** TP, FP, FN, precision, recall, RMT gold seized, and number of accounts flagged. Test values, which must match exactly: R1 180/150/24, 54.5%, 88.2%, 900,000. R2 4/50/200, 7.4%, 2.0%, 8,000,000. R3 4/1/200, 80.0%, 2.0%, 8,000,000. R4 204/27/0, 88.3%, 100.0%, 9,000,000. R5 204/1/0, 99.5%, 100.0%, 9,000,000. With R3 and fan-in threshold 51, only mule 0 (fan-in 56) is flagged: TP 1, FP 0, gold seized 2,000,000.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. Colors are not the only signal: flagged nodes also get a thicker outline, RMT labels a different marker shape. Respect `prefers-reduced-motion` (no animated layout) and `prefers-color-scheme`. No game art or logos.
