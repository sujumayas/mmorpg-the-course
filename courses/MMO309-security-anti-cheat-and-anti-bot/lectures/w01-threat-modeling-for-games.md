# MMO309 · Week 01 — Threat modeling for games

**Why this matters:** Every security team runs out of engineers before it runs out of threats. A threat model is how you decide which attacks to stop first, which to live with, and which defenses cost your players more than the attack does. Teams without one defend against whatever is loudest in the support queue, and that is rarely what costs the most.

**You will be able to:**
- Draw the assets, attackers, entry points and trust boundaries of an MMO on one page.
- Classify a list of game threats with STRIDE and name the game threats STRIDE misses.
- Compute expected annual loss for each threat and the first-year net value of a control, including the cost it puts on honest players.
- Critique a proposed defense by asking what it costs the attacker, what it costs the studio, and what it costs everyone else.

**Before class:** Hoglund, G. & McGraw, G. (2007), *Exploiting Online Games*, chapter 1 ("Why Games?") and chapter 3 ("Money"). Shostack, A. (2014), *Threat Modeling: Designing for Security*, chapter 1. Skim the Ninth Circuit's statement of facts in *MDY Industries v. Blizzard Entertainment* (2010, amended 2011), sections C and D, about four pages.

**Prerequisites from earlier courses:** [CS202 week 4, server authority](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) (the trust boundary between client and server, and the rule that clients send intent). [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (why gold has a dollar price, which is why people attack it). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (the arithmetic behind expected loss). MMO302 is this course's prerequisite, and its architecture weeks give you the server diagram you will draw on: [MMO302 week 1, scale targets](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md), [week 2, shards, realms, zones and instances](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) and [week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md).

**Interactive:** [the threat ledger](../examples/w01-threat-ledger.html). Keep it open during section 2.

---

## 1. What a threat model is

A **threat model** is a written answer to four questions about a system. What are we protecting? Who wants to take it or break it? How could they do it? What will we do about it? Shostack's book reduces the method to roughly those questions, and you will use them all term. The final assessment of this course is a threat model for a game of your choice, so treat this week as the first draft of that document.

Four terms carry the method.

- An **asset** is anything of value that an attacker could take, change, see or deny. In an MMO that is more than data. It includes a character's items and currency, the account itself, the fairness of a PvP match, the stability of market prices, and hidden information such as where an enemy is standing.
- An **attacker** (or threat actor) is a person or group with a motive and some means. Motive matters more than skill, because motive predicts where effort goes.
- An **entry point** is any place where input from outside your control reaches your system. The game client's network messages are the obvious one. The website's password reset form, the support chat, the in-game mail system and a staff member's admin tool are also entry points.
- A **trust boundary** is a line where data moves from something you control to something you do not, or the reverse. CS202 week 4 drew one boundary, between client and server. A real MMO has several.

### Assets in a persistent world

MMOs have assets that single-player and match-based games lack, because their state outlives any session. A useful first list for any MMO:

| Asset | What an attacker wants with it | Who notices when it goes wrong |
|---|---|---|
| Account credentials | Take the account, sell it or strip it | The owner, then support |
| Items and currency | Create them from nothing, or move them to themselves | The market, weeks later |
| Economy-wide prices | Profit from inflation, cornering or dumped gold | Every player, slowly |
| Competitive fairness | Win matches, climb ladders, farm kills | Opponents, at once |
| Hidden information | See enemies, loot rolls or map secrets early | Nobody, often |
| Service availability | Take servers down, extort, disrupt a rival | Everyone, at once |
| Staff tools | Give themselves anything the game can give | Maybe an auditor, much later |
| Player personal data | Sell it, use it for phishing | Regulators, press |

Look at the last column. Assets that fail loudly get defended because people complain. Assets that fail silently, like the economy and staff tools, can bleed for months.

### Attackers and their motives

Here are the attacker profiles you will meet in this course. Each has a different motive, so each spends effort differently.

| Attacker | Motive | Budget and patience | Weeks that cover them |
|---|---|---|---|
| Curious or griefing player | Fun, status, annoying others | Low; stops when bored | 2, 3, 5 |
| Competitive cheater | Winning | Medium; pays for tools | 3, 5 |
| Cheat or bot seller | Revenue from other attackers | High; a business with staff | 5, 6, 7 |
| Gold farmer | Revenue from selling currency | High; runs many accounts | 6, 7, 10 |
| Account thief | Revenue from stolen accounts and items | Medium; works at volume | 9 |
| Insider (staff, contractor) | Money, grudges | Low effort, high access | 1, 12 |

Watch the third row. Most cheaters never write code. They buy a tool from a seller whose business is maintaining it, and that seller, who reasons about money, is your real opponent.

### Drawing the system

Before you list threats, draw the system as boxes and arrows. A **data flow diagram** shows the processes (the game server, the login service), the data stores (the character database), the external entities (players, payment provider) and the flows between them. Then draw a dashed line wherever a flow crosses a trust boundary. For a small MMO the diagram has at least these boxes:

- Game client (untrusted, on the player's machine)
- Login and account service, with a website for password resets
- World servers (trusted), each simulating a zone
- Character and item database
- Trade or auction service
- Payment and shop service, talking to an outside payment provider
- Support tools and GM (game master) tools used by staff
- Telemetry and logs

Every dashed-line crossing is a place to ask what happens if the far side lies. A model that draws only the client-to-server line misses the support agent who can be talked into an account reset.

## 2. Worked example: the ticket queue and the loss ledger

### The hook

In March 2005 a *World of Warcraft* player named Michael Donnelly wrote a bot called Glider that played his character for him. By summer he was selling it through his company, MDY Industries, for fifteen to twenty-five dollars a license. In September 2005 Blizzard launched Warden, anti-cheat software that looked for known bots, and banned most Glider users at once. MDY changed Glider to avoid Warden and started selling an extra subscription, Glider Elite, for five dollars a month, which promised more protection from detection. After those changes, the court record says, Warden caught Glider only occasionally. By September 2008 MDY had sold 120,000 licenses for about $3.5 million in gross revenue.

The defender's side is in the same court record. From December 2004 to March 2008 Blizzard received 465,000 complaints about WoW bots and spent $940,000 a year responding to them. And in a November 2005 email quoted by the court, Donnelly described his strategy in economic terms. Blizzard had limited engineering time, so MDY wanted each change to Blizzard's detection code to be bad business. Each change should be costly to build and carry a risk of banning innocent customers.

The attacker had a threat model of the defender, priced in engineering time and fear of false bans. You need one at least that good of the attacker, and of your own losses.

### The model

A threat model turns into decisions when you attach numbers to it. The simplest useful number is **expected annual loss** (security texts call it annualized loss expectancy, ALE):

```
ALE = f × I
```

- `f` is the expected number of incidents per year.
- `I` is the cost of one incident in dollars. Count support time, refunds, rollback work, lost subscriptions and damage to the economy.

A **control** is anything that lowers `f` or `I`, such as a code change, a policy or a detection system. Its first-year net value is

```
net = r × ALE − B − P
```

- `r` is the share of the loss the control removes (0.9 means 90%).
- `B` is the build and run cost for the first year.
- `P` is the **player cost**, what the control costs honest players, turned into dollars (usually lost subscriptions from friction).

Every symbol is a guess. Written down, a guess can be challenged. A priority based on "this feels bad" cannot.

### Numbers you can check

Take an invented subscription MMO with 200,000 monthly players. The security lead has eight threats in the backlog. Incidents per year come from support tickets and logs. The cost per incident is the team's estimate.

| ID | Threat | STRIDE | Incidents per year `f` | Cost per incident `I` | ALE `f × I` |
|---|---|---|---|---|---|
| T1 | Account takeover from reused passwords | S | 1,200 | $60 | $72,000 |
| T2 | Item duplication through a crash during trade | T | 2 | $150,000 | $300,000 |
| T3 | Speed hacks | T | 5,000 | $4 | $20,000 |
| T4 | Wallhacks in open-world PvP | I | 8,000 | $5 | $40,000 |
| T5 | Gathering bots | — | 20,000 | $8 | $160,000 |
| T6 | DDoS on the login servers | D | 3 | $30,000 | $90,000 |
| T7 | Stolen GM tool session | E | 0.1 | $800,000 | $80,000 |
| T8 | "I never agreed to that trade" disputes | R | 3,000 | $10 | $30,000 |

The STRIDE column is explained in section 3. The dash for bots is deliberate, and section 3 explains that too.

Now sort the same list two ways. The support queue sorts by how often things happen. The ledger sorts by what they cost.

| Rank | By incidents (the ticket queue) | By ALE (the loss ledger) |
|---|---|---|
| 1 | T5 bots, 20,000 | T2 duplication, $300,000 |
| 2 | T4 wallhacks, 8,000 | T5 bots, $160,000 |
| 3 | T3 speed hacks, 5,000 | T6 DDoS, $90,000 |
| 4 | T8 disputes, 3,000 | T7 GM session, $80,000 |
| 5 | T1 takeover, 1,200 | T1 takeover, $72,000 |
| 6 | T6 DDoS, 3 | T4 wallhacks, $40,000 |
| 7 | T2 duplication, 2 | T8 disputes, $30,000 |
| 8 | T7 GM session, 0.1 | T3 speed hacks, $20,000 |

The two rarest threats, a duplication bug that happens twice a year and a GM session stolen once a decade, rank first and fourth by money. Speed hacks, third in the ticket queue, are last in the ledger. Check two rows by hand. T7 is `0.1 × 800,000 = 80,000`. T3 is `5,000 × 4 = 20,000`. The total is $792,000 a year.

Why is a dupe so expensive? A duplicated item is money printed by an attacker. Once dupes spread, prices move, honest players' savings lose value, and the fix is often a rollback that erases everyone's progress for hours ([week 4](w04-duplication-exploits-and-transactional-design.md) and [MMO401 week 12](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w12-economic-shocks-exploits-and-rollbacks.md)). Two incidents a year at $150,000 each is a conservative guess.

Next, the controls. The team has five proposals.

| ID | Control | Threat | Share removed `r` | Build `B` | Player cost `P` | Saved `r × ALE` | Net, year 1 |
|---|---|---|---|---|---|---|---|
| C1 | Atomic trades (both sides commit or neither does) | T2 | 90% | $60,000 | $0 | $270,000 | +$210,000 |
| C2 | Optional authenticator app | T1 | 36% | $50,000 | $0 | $25,920 | −$24,080 |
| C3 | Trade limits on unbalanced trades | T5 | 60% | $10,000 | $480,000 | $96,000 | −$394,000 |
| C4 | Server-side movement credit check | T3 | 95% | $15,000 | $0 | $19,000 | +$4,000 |
| C5 | Two-factor login and audit log for GM tools | T7 | 75% | $20,000 | $0 | $60,000 | +$40,000 |

Two rows need explaining. C2's `r = 0.36` is an adoption rate times an effectiveness: 40% of players turn it on and it stops 90% of takeovers on accounts that have it. C3's player cost assumes 2% of players (4,000) quit over the friction at $10 a month for a year, `4,000 × 120 = 480,000`.

This short script reproduces both tables. Run it, then change a number and watch the ranking move.

```python
ale = {"T1": 72_000, "T2": 300_000, "T3": 20_000, "T5": 160_000, "T7": 80_000}
controls = [  # (id, control, threat, share of loss removed, build cost, yearly player cost)
    ("C1", "Atomic trades", "T2", 0.90, 60_000, 0),
    ("C2", "Optional authenticator", "T1", 0.40 * 0.90, 50_000, 0),
    ("C3", "Trade limits", "T5", 0.60, 10_000, 480_000),
    ("C4", "Movement credit check", "T3", 0.95, 15_000, 0),
    ("C5", "GM 2FA and audit log", "T7", 0.75, 20_000, 0),
]
for cid, name, t, cut, build, friction in controls:
    saved = ale[t] * cut
    net = saved - build - friction
    print(f"{cid} {name:24} saves {saved:>9,.0f}  net year 1 {net:>+10,.0f}")
```

Output:

```
C1 Atomic trades            saves   270,000  net year 1   +210,000
C2 Optional authenticator   saves    25,920  net year 1    -24,080
C3 Trade limits             saves    96,000  net year 1   -394,000
C4 Movement credit check    saves    19,000  net year 1     +4,000
C5 GM 2FA and audit log     saves    60,000  net year 1    +40,000
```

C1 is the clear first job. A boring transactional fix beats any anti-cheat work on the list. C5 is cheap insurance against the scariest single event. C2 loses money in year one but its build cost is paid once, so from year two it saves $25,920 a year, and raising adoption (a reward for turning it on) raises `r`. C4 barely pays for itself, which says speed hacks are a fairness problem more than a money problem, and fairness belongs in your cost estimate if players quit over it. C3 is a disaster on paper, and the RuneScape case below shows a real game that learned this.

### Move it yourself

Open `examples/w01-threat-ledger.html`. The left panel is the ticket queue, bars sorted by incidents. The right panel is the loss ledger, the same threats sorted by ALE. A line connects each threat's two bars so you see it jump. Drag T2's cost per incident down from $150,000. Below $80,000 it drops under bots, below $36,000 it falls under the account takeovers, and only below $20,000 does it leave the top five. Then open the controls tab and slide C3's player cost to zero. Trade limits become the second-best control on the list. Almost every argument about a restrictive anti-cheat measure is an argument about that one number.

### Cross-game recognition

**World of Warcraft and Glider (2005 to 2008).** Put the court's numbers into the model. Blizzard's complaint handling alone was $940,000 a year. Over the 40 months from December 2004 to March 2008, 465,000 complaints is about 139,500 a year, so each complaint cost roughly $6.74 to handle. On the attacker's side, $3.5 million over 120,000 licenses is about $29 per sale. MDY's strategy was to push up the defender's `B` for each detection update and to make false bans a live risk, which is a player cost `P`. The attacker attacked the defender's net-value calculation directly. Glider returns in [week 5](w05-memory-editing-and-client-integrity.md) as ban timing, [week 6](w06-botting-economics.md) as a vendor selling bot lifetime and [week 14](w14-case-studies.md) as a court case.

**RuneScape's trade limit (December 2007 to February 2011).** Jagex announced limits on unbalanced trades on 10 December 2007 and applied them to all accounts from 2 January 2008, as part of measures against real-world trading. It is control C3 in real life. The RuneScape Wiki notes a side benefit. Stealing accounts became far less profitable, because a thief could no longer move the account's wealth out. That is one control lowering the ALE of two threats (bots and takeovers), which your ledger should record. The player cost was also real. Players disliked the limits for three years, and in a referendum that closed in January 2011, 91% voted to bring free trade back, which Jagex did on 1 February 2011 ([MMO304 week 11](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) has the full story and its sources). In model terms, `P` was large enough that the players themselves voted the control out. [Week 14](w14-case-studies.md) follows Jagex's next two attempts.

**Diablo and Diablo II (1996 and 2000).** CS202 week 4 told this story as authority. Here it is as a control. *Diablo* stored characters on players' own machines, so character editing was an entry point with a very high `f`. For *Diablo II*, Blizzard added closed realms whose characters lived on Blizzard's servers. That control moved an asset across the trust boundary. Its `B` was server storage and operations for every character. Its `P` was that closed-realm players could not play offline with the same character. Blizzard kept open realms for players who preferred that trade.

Three cases, one ledger. Each defender decision is a bet on `f`, `I`, `r`, `B` and `P`, written down or not.

### Design judgment

- **Rank by loss, then argue.** The ledger's first use is to stop the team from sorting by volume or by whichever threat embarrassed you on social media last week. A rare catastrophic event (dupes, staff tool abuse) usually outranks a common annoying one.
- **Player cost is part of every control.** Friction, false bans, and privacy concerns about invasive anti-cheat software all cost players something. If you leave `P` out, every restrictive control looks free, and you will ship RuneScape's trade limit.
- **Controls interact.** One control can lower several threats (trade limits hurt thieves and farmers). One attacker can move to a neighboring threat when you block the first. Record both in the model.
- **Uncertain numbers are still useful.** When you cannot agree on `I`, compute the ranking at the low and the high estimate. If the top three stay the same, stop arguing and build. If they swap, that estimate is worth a day of research.

### Check this example

1. A bug lets players reset a dungeon's loot lockout. It happens about 40 times a year, and each case costs about $2,500 in cleanup and economy damage. Where does it rank in the loss ledger?
2. The authenticator in C2 gets a mount reward that raises adoption to 80%. The reward costs nothing to run. What is C2's first-year net now?
3. Suppose only 0.5% of players quit over C3 instead of 2%. Does C3 pay for itself in year one?

<details>
<summary>Answers</summary>

1. ALE is `40 × 2,500 = $100,000`. It ranks third, between bots ($160,000) and DDoS ($90,000).
2. `r = 0.8 × 0.9 = 0.72`, saved `0.72 × 72,000 = $51,840`, net `51,840 − 50,000 = +$1,840`. It pays for itself in year one.
3. Player cost becomes `1,000 × 120 = $120,000`. Net is `96,000 − 10,000 − 120,000 = −$34,000`. Still negative in year one. It would need a lower quit rate or a higher bot loss to pay.

</details>

## 3. STRIDE for an MMO, and what it misses

Once you have the diagram, you need a way to generate threats so you do not rely on memory. **STRIDE** is a checklist developed at Microsoft by Loren Kohnfelder and Praerit Garg in 1999. Each letter is a kind of threat, and each is the opposite of a security property.

| Letter | Threat | Property it breaks | MMO example |
|---|---|---|---|
| S | Spoofing | Authenticity | Logging in as someone else; a client pretending to be another player's client |
| T | Tampering | Integrity | Changing a message so the server duplicates an item; editing a saved character |
| R | Repudiation | Non-repudiation | "I never agreed to that trade"; a GM denying they spawned an item |
| I | Information disclosure | Confidentiality | Seeing enemies through walls; reading another player's mail |
| D | Denial of service | Availability | Flooding the login server; crashing a zone with a malformed packet |
| E | Elevation of privilege | Authorization | A player reaching a GM command; a support agent reaching the payment database |

The method is mechanical. For each trust-boundary crossing in your diagram, ask all six questions. You will delete duplicates and silly rows. The point is that no category gets skipped because nobody thought of it.

Repudiation is the letter game teams skip most often, and T8 in the ledger shows why it matters. If your trade log does not record both players' confirmations with a server timestamp, every scam report becomes one person's word against another's, and support pays for each one. The control is a log, which is cheap.

### What STRIDE misses in games

STRIDE was built for software where the rules are the security policy. In a game, a player can follow every rule of the software and still attack the game. Three threat families fall between STRIDE's letters.

- **Automation of legitimate play.** A bot sends exactly the inputs a human could send. Nothing is spoofed or tampered with. What it breaks is a design assumption, that the time spent belongs to a human. That is why T5 has a dash. Weeks 6 to 8 treat bots as an economic and statistical problem.
- **Exploits of design.** An unintended combination of legitimate mechanics (an infinite crafting loop, a vendor that buys for more than another vendor sells) needs no hacking at all. The threat is in the design document. MMO304's faucet and sink analysis is your tool here.
- **Social attacks.** Scams, phishing for account details, and talking a support agent into an account reset. These use people as the entry point. Week 9 covers the account side.

Add a fourth question to STRIDE for games: **"What can a player do, with no hacking, that the design did not intend and that pays?"** The words "that pays" matter. Players find unintended actions every day. The ones that become threats are the ones someone can profit from, repeat and sell.

## 4. Attackers are running a business

The attacker's side of the model explains why some threats grow and others fade. A rational attacker keeps attacking while

```
expected value to the attacker > attacker's cost + expected penalty
```

- **Value** is what the attack yields: gold sold for money, a win, a stolen account's contents.
- **Cost** is the time and money to build, buy or maintain the attack: a cheat license, new accounts, servers.
- **Expected penalty** is the chance of being caught times what is lost: a banned account, a lost stockpile, in rare cases legal action.

A defender has three levers, and each maps to a different kind of control.

1. **Lower the value.** Make the loot worthless to steal or sell. Bind-on-pickup items and trade limits do this. So does fixing the economy so that farmed gold is worth less.
2. **Raise the cost.** Make the attack harder to build or run. Server authority (week 2), client integrity checks (week 5) and CAPTCHA-style gates raise cost.
3. **Raise the expected penalty.** Detect more, and make each detection take away more. Bans, confiscation and delayed ban waves ([week 5](w05-memory-editing-and-client-integrity.md)) do this.

Glider's history shows the arms race in these terms. Warden's first version made detection nearly certain, so the expected penalty was high and most users were banned. MDY responded by lowering the chance of detection and charging for that as a separate product, Glider Elite. The seller turned the defender's detection rate into its own revenue line. When an attacker profits from your detection rate, a cat-and-mouse fight on detection alone will cost you engineering time forever, so look for controls on the other two levers.

You do not need to make an attack impossible, only unprofitable for most attackers. If a bot account earns $30 of gold before its ban and costs $40 to set up, farming stops without a perfect detector. Week 6 builds that model in full.

### Asymmetry

The defender must be right every time and the attacker only once, goes the saying. In games the asymmetry also runs your way. A cheat seller with 120,000 customers must keep every copy working, so a protocol change that breaks all copies at once costs the seller more than it costs you. The server sees every player, while the attacker sees only their own account, which is what statistical detection uses (weeks 7 and 8). And you choose when to ban. [Week 5](w05-memory-editing-and-client-integrity.md) shows why banning in waves slows the seller down.

## 5. Writing the threat model document

The course's first assessment is a threat model. Keep it short enough that your team will read it, in this order:

1. System summary and the data flow diagram with trust boundaries marked.
2. Assets, each with an owner on the team.
3. Attackers that apply, with motive and budget.
4. Threats from STRIDE per boundary crossing plus the three game families, each with `f` and `I` and the source of each guess.
5. The ledger, with low and high estimates for uncertain rows.
6. Controls for the top threats, with `r`, `B`, `P` and net value.
7. Accepted risks, and why. Writing these down turns "we forgot" into "we decided".
8. A review date. A patch that adds a trade feature adds rows.

Update the model when a feature is designed, when a control costs least.

## In-class activity (25 minutes)

Groups of three. You receive a one-page design for a small survival MMO: 5,000 concurrent players, a player-run market, guild housing, a cash shop that sells cosmetics, and a support team of four.

1. (8 min) Draw the data flow diagram. Mark every trust boundary with a dashed line. There are at least five.
2. (8 min) Run STRIDE on two boundary crossings of your choice, then add one threat from each of the three game families. Aim for ten threats.
3. (5 min) Estimate `f` and `I` for your ten threats and rank them by ALE. Write the source of each guess ("support tickets from a similar game", "pure guess").
4. (4 min) Pick your top threat and propose one control. Give `r`, `B` and `P`. Swap with another group, who must find one number in your control they think is wrong, and say which way it is wrong.

Expected output: a diagram, a ten-row ledger with a ranking, and one control with the other group's critique written beside it.

## Common misconceptions

- **"The most common attack is the most important one."** Frequency is one factor of two. Two dupes a year outrank 5,000 speed hackers in the section 2 ledger.
- **"A good defense costs players nothing."** Every restrictive control has a player cost. RuneScape's trade limit cost enough that 91% of voting players asked for it to go.
- **"Threat modeling means listing hacks."** Many of the costliest game threats involve no hacking: bots using normal inputs, design exploits, and social attacks on support staff.
- **"If we can't make an attack impossible, we can't stop it."** Attackers stop when the attack stops paying. Lowering value or raising cost can end an attack that detection alone never ends.

## Check yourself

1. A trade exploit lets a player receive an item without the other side's gold leaving their bag. It is found 6 times a year, and each case costs $20,000. Compute its ALE and place it in the section 2 ledger.
2. Which STRIDE letter fits each of these? (a) A player edits a packet so that their character's name contains a GM tag. (b) A modified client shows the contents of other players' bank vaults. (c) A player claims support restored the wrong items and there is no record of what was restored.
3. A cheat seller charges $10 a month. Your new detection system bans 30% of its users each month and each banned user loses an account worth $25 to them. What is a user's expected monthly penalty? What happens to the seller's customer count over time if nothing else changes?
4. Your team proposes a mandatory authenticator for all accounts. Name one value you would expect to rise and one you would expect to fall, in the model's terms, compared with C2.

<details>
<summary>Answers</summary>

1. `6 × 20,000 = $120,000`. It ranks third, after duplication ($300,000) and bots ($160,000), and just above DDoS ($90,000).
2. (a) Spoofing (pretending to be staff), with a tampered name as the method; you could argue elevation if the tag grants powers. (b) Information disclosure. (c) Repudiation.
3. Expected penalty is `0.3 × 25 = $7.50` a month, on top of the $10 fee, so a month of cheating costs a user $17.50 in expectation. Customers who are banned must buy a new account to continue, and 30% leave the base each month, so the customer count falls unless the seller recruits faster, or lowers its detection rate, which is what MDY sold as Glider Elite.
4. `r` rises (100% adoption instead of 40%). `P` rises too, because some players will not bother to set it up and leave or stop logging in. `B` may rise for support load from locked-out players.

</details>

## Lab / assignment hook

[Lab 01, the threat ledger](../labs/lab01.md). You complete a small Python ledger tool, reproduce this lecture's tables, then build a threat model for the lab's sample game with at least twelve threats and four costed controls. It is the first draft of the course's threat model assessment (30%).

## Sources

- *MDY Industries, LLC v. Blizzard Entertainment, Inc.*, 629 F.3d 928 (9th Cir. 2010, amended opinion filed 17 February 2011), statement of facts, sections C and D. Glider developed in March 2005 and sold from summer 2005 at $15 to $25 per license; Warden launched September 2005 and used to ban most Glider users; Glider Elite at $5 a month; Warden only occasionally detecting Glider afterwards; $3.5 million gross revenue from 120,000 licenses by September 2008; 465,000 bot complaints from December 2004 to March 2008; $940,000 a year spent responding; Donnelly's November 2005 email describing the aim of making detection "bad business" (paraphrased). Opinion PDF via CourtListener.
- Wikipedia, "MDY Industries, LLC v. Blizzard Entertainment, Inc." (accessed September 2026). District court ruling of 14 July 2008 and appeal decided 14 December 2010.
- Wikipedia, "STRIDE model" (accessed September 2026), citing Kohnfelder, L. & Garg, P. (1999), "The threats to our products", Microsoft. The six categories and the properties they correspond to.
- RuneScape Wiki, "Trade limit" (historical article, accessed September 2026). Announced 10 December 2007 as a measure against real-world trading; applied to all players 2 January 2008; the side benefit of discouraging account theft; limits of 10,000 coins per 15 minutes for free players during the period.
- RuneScape Wiki, "Trade limit" and "Update:The Wilderness and Free Trade Return!" (accessed September 2026). The referendum that closed on 14 January 2011 with 91% voting yes, and the return of free trade on 1 February 2011.
- Wikipedia, "Battle.net" and "Diablo II" (accessed September 2026), as cited in CS202 week 4. Locally stored *Diablo* characters and the closed realms of *Diablo II*.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley. Chapter titles checked against the publisher's table of contents (InformIT, published 9 July 2007).
- Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley.
- The invented MMO, its threat list and every dollar figure in the ledger and control tables are teaching values, not data from any real game.

## Interactive spec: examples/w01-threat-ledger.html

**Insight the visual must make obvious:** sorting threats by how often they happen and sorting them by what they cost give very different orders. Rare, expensive threats (duplication, staff tool abuse) jump to the top of the loss ledger. A second tab makes a second point. A control that looks strong on loss removed can be a net loss once its cost to honest players is counted.

**Layout.** Two tabs, "Threats" (default) and "Controls". On screens under 700 px wide, panels stack vertically. No page-level horizontal scroll.

**Threats tab.** Two horizontal bar charts side by side with the eight threats T1 to T8.
1. Left, "Ticket queue: incidents per year". Bars sorted descending by `f`, on a log scale from 0.05 to 50,000, each bar labelled with ID, short name and `f`.
2. Right, "Loss ledger: expected loss per year". Bars sorted descending by `ALE = f × I`, linear scale from $0 to the current maximum rounded up to the next $50,000, labelled with ID and ALE in dollars.
3. A thin connector line joins each threat's bar on the left with its bar on the right, so a rank change reads as a slanted line. Lines for threats that moved three or more ranks are drawn in the accent colour.
4. Below the charts, a table of the eight threats with editable number inputs for `f` and `I`, and computed ALE. Editing re-sorts both charts immediately, with a 200 ms transition that is disabled under `prefers-reduced-motion`.
5. A total line: "Total expected loss: $792,000 per year" at defaults.

**Controls tab.** A table of C1 to C5 with sliders for `r` (0 to 100%), `B` ($0 to $200,000, step 1,000) and `P` ($0 to $600,000, step 1,000), and computed saved and net. Next to it, a diverging horizontal bar chart of net value per control, positive bars right, negative left, sorted descending. C2 has two sliders instead of one for `r`, adoption (0 to 100%) and effectiveness (0 to 100%), with `r` = their product. The saved value uses the ALE of the linked threat from the Threats tab, so editing T2's cost there changes C1 here.

**Controls.** Every input keyboard reachable, with visible focus. A "Reset to lecture values" button.

**Default data.**
- Threats (`f`, `I`): T1 (1,200, 60), T2 (2, 150,000), T3 (5,000, 4), T4 (8,000, 5), T5 (20,000, 8), T6 (3, 30,000), T7 (0.1, 800,000), T8 (3,000, 10).
- Controls (threat, `r`, `B`, `P`): C1 (T2, 0.90, 60,000, 0), C2 (T1, 0.40 × 0.90, 50,000, 0), C3 (T5, 0.60, 10,000, 480,000), C4 (T3, 0.95, 15,000, 0), C5 (T7, 0.75, 20,000, 0).

**Formulas.** `ALE = f × I`. `saved = r × ALE(threat)`. `net = saved − B − P`.

**Test values** (assert on load, log failures to the console):
- Total ALE = 792,000. Ledger order T2, T5, T6, T7, T1, T4, T8, T3. Queue order T5, T4, T3, T8, T1, T6, T2, T7.
- Nets: C1 +210,000, C2 −24,080, C3 −394,000, C4 +4,000, C5 +40,000.
- T2 `I` = 40,000 gives ALE 80,000, which ties T7; ties sort by ID, so T2 is placed above T7 and below T6.
- C3 with `P = 0` gives net +86,000, second after C1.
- C2 with adoption 80% gives net +1,840.

**First screen:** the Threats tab at defaults, with the T2 and T7 connector lines highlighted as they climb from ranks 7 and 8 to ranks 1 and 4. Caption: "Two dupes a year cost more than 20,000 bot reports."
