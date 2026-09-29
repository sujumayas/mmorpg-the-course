# MMO402 · Week 09 — Virtual Property and Law

**Why this matters:** Your players will lose items they care about: to a scammer, to a hacker, to a friend who sold what he borrowed, or to you, when you ban them. Each time someone will ask whether it was theft. The answer depends on which of several rulebooks you consult, and you write two of them. If you do not decide in advance which losses are part of the game, a court, the police or an angry player will decide for you.

**You will be able to:**
- Apply a four-question layer test to decide whether a lost virtual item is a matter for play, for the operator or for the law.
- Explain why EVE Online treats an in-game bank theft as allowed play while banning the sale of the stolen currency for real money.
- Distinguish what a EULA says about ownership from what a criminal court may say about theft, using the Dutch RuneScape case and Bragg v. Linden.
- Design a loss policy for a fictional world that states, for each way an item can leave a player's hands, which layer handles it.

**Before class:** Fairfield, "Virtual Property," *Boston University Law Review* 85 (2005), parts I and II. Lastowka and Hunter, "The Laws of the Virtual Worlds," *California Law Review* 92(1), 2004, the section on virtual property. Read EVE Online's two short support pages "Scams" and "Corp Theft" (support.eveonline.com), about 5 minutes together.

**Prerequisites from earlier courses:** [MMO401 week 8, player banks, loans and scams](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w08-player-banks-loans-and-scams.md) (why player banks fail, and the EBank case in economic terms). [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (sanctioned and unsanctioned exchanges). [MMO304 week 1, artificial scarcity](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w01-why-virtual-economies-exist-artificial-scarcity.md) (why a copyable file can be scarce). [MMO301 week 6, EVE Online](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md). From this course: [week 4, wars, betrayals and meta-gaming](w04-wars-betrayals-and-meta-gaming.md), [week 5, rules, EULAs and terms of service](w05-rules-eulas-and-terms-of-service.md), [week 7, justice systems](w07-justice-systems-reports-reviews-appeals.md) and [week 8, rights of avatars](w08-rights-of-avatars-koster-2000.md).

**Interactive:** [Whose sword is it? The layer test](../examples/w09-whose-sword.html)

---

## 1. Can a database row be property?

A sword in an MMO is a row in a database: an item ID, an owner ID, some stats. Nobody can hold it. The operator can copy it, delete it or change it with one query. Why would anyone call that property?

Because of how it behaves for the people who use it. The legal scholar Joshua Fairfield argued in 2005 that some code behaves like land and chattels (movable things) rather than like ideas, and named the features that make it so:

- **Rivalry.** If I have it, you do not. A song file can be copied endlessly; a sword in a game is designed so that only one character holds it at a time. MMO304 week 1 showed that this scarcity is a design choice, made so that items can have value.
- **Persistence.** It lasts when you log off. An item that vanished between sessions could not be owned in any useful sense.
- **Interconnection.** Other people can see it, trade for it and be affected by it. A sword that exists only in a single-player save file interacts with nobody.

Later summaries of Fairfield's work add secondary markets (people buy and sell the thing for money) and value added by users (players customize or build it). Items that tick all these boxes look like property to the people who hold them. They trade them, lend them, fight over them and grieve when they vanish.

### What the contract says

Operators answer differently. Nearly every MMO's end-user licence agreement (EULA) says that the operator owns everything in the game and that the player holds only a licence to use it. Two current examples:

- Blizzard's EULA (last revised 21 March 2024) lists virtual goods, including currency, weapons, armor, mounts and pets, and characters' names, likenesses and inventories among the content Blizzard owns. It forbids gathering in-game currency, items or resources for sale outside Blizzard's platform or games.
- EVE Online's EULA grants a limited, revocable licence to use game content, forbids selling or buying characters, items or currency for real money except through CCP's permitted character transfer system, and calls such trading a violation of CCP's proprietary rights.

The game designer Richard Bartle put the operator's argument plainly: because the developer can change the world at any time, ban a player, delete items or shut the world down, players cannot truly own anything in it. Week 13 shows what happens to every item in a world when the servers close.

So there are two stories. Players experience items as property. Contracts define them as licensed content. The law has had to decide which story to believe, and it turns out the answer depends on who took the item and how.

## 2. Worked example: whose sword is it? When in-world fraud is allowed play

This is the course's signature case study. The Bank of EVE scam case, told here through the best-documented EVE bank collapse, EBank in 2009, asks when fraud inside a world is part of the game.

### The hook

Four stories, one event: a valuable item or currency leaves a player's control and ends up with someone else.

1. **EVE Online, 2009.** Ricdic, the chief executive of EBank, a player-run bank in EVE, withdrew 200 billion ISK (EVE's currency) of depositors' money and sold it for £3,115 of real money, which he used toward a house deposit and medical bills (BBC News, July 2009). CCP's published scam policy says scams carried out through legal in-game means do not break game mechanics, cannot be compensated by game masters, and generally cannot be punished.
2. **Leeuwarden, the Netherlands, 6 September 2007.** Two teenagers used threats and violence, including a knife, to force a 13-year-old to log in to his RuneScape account and transfer a virtual amulet and mask to one of theirs. On 31 January 2012 the Dutch Supreme Court (Hoge Raad) upheld their conviction for theft.
3. **Shanghai, 2005.** Qiu Chengwei won a rare sword, the Dragon Sabre, in The Legend of Mir 3 and lent it to a friend, Zhu Caoyuan, who sold it for 7,200 yuan (about £470, or US$870). Qiu went to the police, who told him the sword was not real property. He then stabbed Zhu to death. The BBC reported the killing in March 2005, and in June 2005 reported that a Shanghai court had given Qiu a suspended death sentence, which in China usually becomes life imprisonment.
4. **Second Life, decided 2007.** Linden Lab, the operator, closed Marc Bragg's account and took the virtual land he had bought, which he valued at US$4,000-6,000, after deciding he had used an exploit in Linden's land auctions. Bragg sued. A US federal court refused to force the case into Linden's arbitration clause, finding it unconscionable. The parties settled in October 2007.

The first case was allowed play. The second was a crime. The third had no remedy at any level and ended in a killing. The fourth was a contract dispute with the operator. Why did the same kind of loss get four different answers?

### The model: the layer test

A virtual item sits inside four rulebooks at once, like nested boxes. Each layer asks one question. Ask them in order, and the first "yes" decides which layer handles the loss.

```
Q1  Who took it?
      The operator            → CONTRACT layer: consumer and contract law (Bragg)
      Another player          → go to Q2

Q2  Did the taker gain control by means outside the game?
    (force, threats, or hacking or phishing the account)
      Yes                     → LAW layer: theft or fraud, if the item has real value
                                and the victim had exclusive control
      No                      → go to Q3

Q3  Do the operator's rules forbid this in-game method?
      Yes                     → OPERATOR layer: ban, reversal, asset removal
      No                      → go to Q4

Q4  Did the game's mechanics carry out the transfer through the victim's
    own action or permissions the victim granted?
      Yes                     → PLAY layer: allowed play, no remedy
      No (a bug did it)       → OPERATOR layer: exploit (weeks 7 and 8)
```

Deception that happens in the game's own channels stays out of Q2, even when it involves real money or someone pretending to be the operator. The taker did not seize control of the account; the victim handed the item over. Operators usually forbid those scams at Q3, and the interactive flags them as possible fraud on its "outside the game" card.

Each outcome names who has the power to fix the loss, and who does not:

- **Play layer.** Nobody reverses it. The loss is part of the game, like losing a battle.
- **Operator layer.** The operator can reverse it, compensate, or punish. Players complain to support.
- **Law layer.** Police and courts can act, whatever the EULA says about ownership.
- **Contract layer.** The player's claim is against the operator itself, under the terms they agreed to and whatever consumer law limits those terms.

Two pieces of this model need defending.

**Why means come before rules (Q2 before Q3).** The Dutch Supreme Court's reasoning shows it. The court held that the amulet and mask counted as goods under the theft article of the Dutch criminal code because they had real value to the victim, who had put time and effort into getting them, and because he had exclusive actual control over them through his login, which the defendants took from him. The court also noted that the game's rules did not permit taking items this way. Force applied to a person in the real world does not become play because its target is a database row.

**Why the EULA does not settle Q2.** A EULA is a contract between the operator and the player. It can say the operator owns the amulet, and that governs disputes between those two parties. Criminal law asks a different question: did a third party take something of value from someone who controlled it? The Dutch court protected the victim's control, not an ownership title. A contract between the victim and Jagex could not make the robbery legal.

### Numbers you can check

Run the four hook cases, and four more, through the test. For each, apply Q1 to Q4 yourself and check the verdict.

| Case | Q1 taker | Q2 outside means? | Q3 rules forbid? | Q4 mechanics, own action? | Layer |
|---|---|---|---|---|---|
| EBank withdrawal, EVE 2009 | Player | No: deposits made voluntarily in game | No: scams by legal in-game means are allowed | Yes | Play |
| EBank cash-out for real money | Player (seller) | No | Yes: selling ISK for real money breaks the EULA | n/a | Operator |
| Leeuwarden, RuneScape 2007 | Player | Yes: threats and violence | n/a | n/a | Law |
| Dragon Sabre sale, Mir 3 2005 | Player | Arguably: a real-money sale of a lent item | Unclear | Yes: the borrower held the item | No layer took it up in time |
| Bragg, Second Life 2007 | Operator | n/a | n/a | n/a | Contract |
| EVE corporation theft by a director with roles | Player | No | No: CCP says removing corp assets with access gained through normal mechanics is not an exploit | Yes: the corp granted the roles | Play |
| EVE Character Bazaar scam | Player | No | Yes: scamming in character transfers is explicitly forbidden | n/a | Operator |
| Old School RuneScape "doubling money" scam | Player | No | Yes: the Code of Conduct prohibits scamming | n/a | Operator |

Count the verdicts. Of the eight rows, two land in play, three with the operator, one in law, one in contract, and one fell between layers. The same kind of act, deceiving another player to get their goods, lands in the play layer in EVE space and in the operator layer at the Character Bazaar and in Old School RuneScape. The deception is identical. What changed is the operator's rule at Q3.

Now check the money. The EBank figures imply a grey-market price for ISK in 2009:

```
£3,115 / 200 billion ISK ≈ £15.6 per billion ISK
```

This is the same price week 4 used for the EBank row of its real-money shadow table.

And the Dragon Sabre:

```
7,200 yuan ≈ US$870, so about 8.3 yuan per US dollar (China's pegged rate in early 2005)
```

Neither number is large by the standards of real crime. Both are large enough that the owners cared, and that is what the Dutch court's "real value" test picks up. Value in the eyes of the holder, backed by a market, is what pulls a virtual item into the law layer when the means are real-world.

### Why the EBank case is allowed play

Go back to the signature question. CCP's position on EBank rests on Q3 and Q4. The depositors handed ISK to a player they chose to trust. The withdrawal used ordinary game mechanics and permissions they granted. EVE's rules deliberately allow in-game deception, because betrayal, espionage and risk are part of what EVE sells (week 4). So the theft is play. CCP's scam page says so in plain words, and EVE's reputation for heists is part of the world's identity (MMO301 week 6).

But the case does not stay in one layer. The moment Ricdic sold ISK for real money, he left the play layer. CCP's current real-money-trading policy treats ISK selling as grounds for a permanent ban without appeal. The theft was allowed. The cash-out was not. One sequence of actions, two layers, two answers.

### A visual you can move

Open `examples/w09-whose-sword.html`. Build a case with the controls: who took the item, by what means, what the operator's rules say, and whether the item has a real-money market. The left view walks your case through the four questions as a flowchart and lights the path. The right view shows two verdict cards side by side, "Inside the game" and "Outside the game," so you can see a case that is allowed play inside and a crime outside, or the reverse. Try the EBank preset, then change only the means from "in-game trust" to "hacked account" and watch the verdict jump from Play to Law without any change in the item or its value.

### Cross-game recognition

**EVE Online, corporation theft (current policy).** CCP's policy says that taking corporation assets is not an exploit if the access was gained through normal game mechanics, that losses caused by granting roles are not reimbursed, and that support will not reveal the thief's identity if the game does not show it. That is Q4 written as policy: permissions you granted are your risk.

**EVE Online, the Character Bazaar (current policy).** The same scam policy that leaves in-game scams alone forbids scams involving character transfers, scams that imitate CCP's services, scams using exploits, and scams that push the victim to buy PLEX (CCP's real-money-backed item) to pay the scammer. Every exception touches something outside the pure game: real money, CCP's identity, or bugs. EVE draws its Q3 line exactly where the play layer meets the others.

**Old School RuneScape (current rules).** Jagex's Code of Conduct prohibits scamming, punishable by a mute or ban if reported. The same "doubling money" trick that would be allowed play in EVE space is an operator-layer offence here. Neither choice is wrong. They are different answers to Q3, and each shapes a different world: EVE's players learn to verify, Old School RuneScape's learn to report.

**Second Life and Bragg v. Linden (2007).** When the operator is the taker, the EULA is the whole dispute. The court's refusal to enforce the arbitration clause turned partly on the facts that the terms were offered on a take-it-or-leave-it basis and that Second Life, unusually, had told users they could hold property rights in virtual land. The lesson for designers: what you say in marketing about ownership can be read against what your contract says.

### Eyes-open design judgment

- **Decide, for every way an item can leave a player, which layer handles it, and publish the answer.** EVE's scam and corp theft pages are short and blunt. That is their strength: nobody deposits ISK in a player bank believing CCP will refund them.
- **Allowed play needs visible risk.** If deception is part of your game, show it: trade windows that display exactly what is exchanged, contract systems with escrow (MMO401 week 8), and warnings the first time a player grants permissions over shared assets.
- **Forbidding scams has a cost too.** An operator-layer rule creates support tickets, evidence disputes and a justice pipeline (week 7). A game with millions of trades a day that forbids scams must be able to investigate them.
- **You do not control the law layer.** Your EULA can say you own every item. A court may still treat a robbery of those items as theft, because it protects the player's control and the item's real value. Design for account security accordingly: two-factor login and item recovery for hacked accounts are part of your legal exposure, not only your support costs.
- **Watch for cases that fall between layers.** The Dragon Sabre case is what happens when a valuable item has no rulebook that will hear a dispute about it. A lending feature with a built-in return, or a clear support policy on disputes between friends, is cheaper than the alternative.

## 3. When the operator is the taker

Bragg is worth a closer look, because it is the case where the operator's own power over items met the law.

Marc Bragg had bought land in Second Life. Linden Lab concluded that he had acquired some of it through an exploit in its land auctions, closed his account and took the land and other assets, which he valued at US$4,000-6,000. Linden's terms of service required disputes to go to private arbitration. In 2007 Judge Robreno of the US District Court for the Eastern District of Pennsylvania refused to enforce that clause. He found it unconscionable, a legal term for contract terms so one-sided that a court will not enforce them. Among his reasons: the terms were presented on a take-it-or-leave-it basis, and Second Life had set itself apart by letting users hold property rights in virtual land. The parties settled out of court in October 2007, and Bragg's account was restored.

Later courts mostly enforced online terms of service, so Bragg did not become the landmark some expected. Its lasting value for designers is narrower and practical:

- The operator's power to take items is real, and the EULA usually backs it.
- That power is weakest where the operator itself encouraged players to see items as property, especially when players paid real money for them.
- Procedure matters. Taking a player's goods without notice, reasons or a route to challenge the decision is the kind of act week 7's due-process checklist and week 8's articles 7, 9 and 14 warn against. Here it put the whole contract in front of a judge.

Connect this to week 7. When EVE removes assets bought for real money, it follows a published strike ladder and states that it returns stolen items to their original owners where possible. That is an operator taking items, with published rules, graduated sanctions and a stated reason. It is much harder to call unconscionable.

## 4. Four legal routes, and what each needs

When a virtual-item dispute leaves the game, it usually travels one of four routes. You do not need to be a lawyer, but you should know which route your design choices open.

| Route | Who brings it | What the item must be | Example |
|---|---|---|---|
| Criminal law (theft, fraud, extortion) | The state | Something of value the victim controlled | Leeuwarden, RuneScape (Netherlands, 2012) |
| Contract and consumer law | The player, against the operator | Something the contract and marketing promised | Bragg v. Linden (US, 2007) |
| Operator rules (EULA, policies) | The operator | Anything the rules cover | EVE's RMT and Character Bazaar rules |
| Nothing | Nobody | A loss inside allowed play | EBank's withdrawal |

Two cautions. First, legal treatment varies by country and changes over time. The Dutch ruling binds Dutch courts, and other systems have taken other paths. Always name the jurisdiction and the year. Second, the empty route is a choice. EVE chose it for in-game scams and told everyone. The Dragon Sabre case shows what happens when a world leaves a route empty by accident.

## In-class activity (25 minutes)

In groups of three, you design the loss policy for a new sandbox MMO with a player-driven economy, player corporations with shared vaults, and a sanctioned real-money token (like PLEX or the WoW Token, MMO304 week 11).

1. List every way an item can leave a player's control in your game. Aim for at least eight: trade, contract, corp vault withdrawal, death in PvP, theft by a hacker, a scam in chat, a bug, a ban (8 minutes).
2. For each, run the layer test and write the layer you choose. Where you have a real choice (usually Q3), write one sentence on why (8 minutes).
3. Write the two-sentence policy text a player would read for your most controversial choice, in the blunt style of EVE's scam page (4 minutes).
4. Swap with another group and find one case their policy leaves between layers (5 minutes).

Expected output: a table of at least eight loss routes with layers, one published policy text, and one gap found in another group's design.

## Common misconceptions

- **"The EULA says the company owns everything, so stealing virtual items can't be theft."** The EULA governs operator and player. The Dutch Supreme Court held that virtual items taken by force from a player who controlled them were goods under theft law, whatever the contract said about ownership.
- **"EVE allows everything."** EVE allows in-game deception through legal mechanics. It forbids real-money trading, scams at the Character Bazaar, scams imitating CCP, scams using exploits and scams that push victims to buy PLEX.
- **"If something is allowed play, the victim did something wrong."** Allowed play means no one will reverse the loss. It says nothing about blame. A good design makes the risk visible so that players accept it knowingly.
- **"Bragg established that players own their virtual property."** The court refused to force arbitration, and the case settled. Later courts mostly enforced online terms. Its lesson is about how marketing and procedure can weaken an operator's contract.

## Check yourself

1. Run this case through the layer test: in EVE, a player gets another player's password through a fake website that imitates CCP's login page, logs in, and moves the victim's ships to his own corporation. Which layer handles it, and at which question does it stop?
2. A World of Warcraft player lets a friend log in to her account to finish a raid, and the friend sells her gold for real money on a third-party site. Which layers does this case touch? Use the Blizzard EULA terms from section 1.
3. The EBank figures imply about £15.6 per billion ISK. At that rate, what real-money value would a 50 billion ISK corporation vault theft have? Would the layer test's verdict change if the value were ten times larger? Why or why not?
4. Your game forbids scams (Q3 = yes) and has 2 million trades a day. If 0.01% of trades lead to a scam report and each takes 15 minutes to investigate, how many staff hours a day does your rule cost?

<details>
<summary>Answers</summary>

1. Q1: another player. Q2: yes, hacking the account through a phishing site is an outside means. It stops at Q2, in the law layer (and the operator will also act: the scam imitates CCP, which CCP forbids, and hacked accounts are a support case). The item and the in-game transfer are the same as a corp theft; the means changed the layer.
2. At least two. Selling in-game currency outside Blizzard's platform breaks section 1.C.iii of the EULA, so the operator layer applies to the friend, and Blizzard may also act on the account the gold came from. Whether the sale is a matter for the law layer depends on the jurisdiction and on whether handing over the login gave the friend legitimate control. The case is close to the Dragon Sabre case, and a real court's answer is uncertain. Notice that Q2 is hard here: the friend did not hack anything, but he used access for a purpose the owner never agreed to.
3. `50 × 15.6 = £780`. No. The layer test turns on who took it and by what means, not on how much it was worth. Value matters inside the law layer, for whether an item counts as goods at all and for sentencing, but it does not move a case between layers.
4. `2,000,000 × 0.0001 = 200` reports a day, `200 × 0.25 h = 50` staff hours a day, about six full-time investigators before appeals.

</details>

## Lab / assignment hook

[Lab 09, case briefs with the layer test](../labs/lab09.md). You brief three virtual-property cases from fact sheets, run each through the layer test, and write a loss policy for a fictional MMO. The briefs count toward the course's case analyses.

## Sources

- Fairfield, J. A. T. (2005). "Virtual Property." *Boston University Law Review* 85, 1047. Rivalry, persistence and interconnection. The later list of five characteristics (adding secondary markets and user value-added) as summarized in Wikipedia, "Virtual economy" (accessed September 2026), which also records Bartle's argument that developer control negates ownership.
- Lastowka, F. G. & Hunter, D. (2004). "The Laws of the Virtual Worlds." *California Law Review* 92(1), 1.
- Blizzard Entertainment, "Blizzard End User License Agreement" (last revised 21 March 2024). Section 2.A on Blizzard's ownership of virtual items, currency and characters' names, likenesses and inventories; section 1.C.iii forbidding gathering in-game currency, items or resources for sale outside the platform.
- CCP Games, "EVE Online - End User License Agreement" (support.eveonline.com, updated 11 August 2026). Limited revocable licence; ban on selling or buying characters, items or currency except via permitted character transfer.
- CCP Games, EVE Online Support, "Scams" and "Corp Theft" (updated 15 July 2024) and "Real Money Trading (RMT)" (read September 2026, shown as updated 9 September 2026; not reloadable for a re-check on 29 September 2026). In-game scams not compensated or generally punished; listed forbidden scam types; corp theft through granted roles not an exploit; permanent ban for ISK sellers.
- BBC News (2009). "Billions stolen in online robbery." 3 July 2009. http://news.bbc.co.uk/1/hi/8132547.stm. EBank: about 200 billion ISK taken in early June 2009 by its chief executive, Ricdic; sold for £3,115; used toward a house deposit and medical bills; banned for trading in-game cash for real money, and would not have been sanctioned for the theft alone.
- Hoge Raad (Supreme Court of the Netherlands), judgment of 31 January 2012, ECLI:NL:HR:2012:BQ9251 (via data.rechtspraak.nl). Events of 6 September 2007 in Leeuwarden; RuneScape amulet and mask; virtual items as goods under article 310 of the criminal code; real value and exclusive control; game rules did not permit the taking.
- BBC News (2005). "'Game theft' led to fatal attack," 31 March 2005, http://news.bbc.co.uk/1/hi/world/asia-pacific/4397159.stm, and "Chinese gamer sentenced to life," 8 June 2005, http://news.bbc.co.uk/1/hi/technology/4072704.stm. Qiu Chengwei, the Dragon Sabre lent to Zhu Caoyuan and sold for 7,200 yuan (£473); police told Qiu the weapon was not real property; suspended death sentence from a Shanghai court. Wikipedia, "The Legend of Mir 3" (accessed September 2026), gives the sale price as US$870.
- Wikipedia, "Bragg v. Linden Research, Inc." (accessed September 2026). E.D. Pa. 2007; account closure and assets valued at US$4,000-6,000; arbitration clause held unconscionable; settlement in October 2007 restoring Bragg's account.
- Old School RuneScape Wiki, "Scams" (as cited in MMO401 week 8). Rule 2 of the Code of Conduct prohibits scamming, punishable by mute or ban; the doubling-money scheme.

## Interactive spec: examples/w09-whose-sword.html

**Purpose.** Let students build a virtual-item loss case and see which layer (play, operator, law, contract) handles it, with the same case judged "inside the game" and "outside the game."

**The one insight the visual must make obvious.** Changing only the means of taking (from in-game trust to a hacked account or physical threat), while the item and its value stay fixed, moves the verdict from Play to Law. The item does not decide the layer; the means do.

**Layout.** Left: a vertical flowchart of the four questions (Q1 to Q4) with four terminal boxes (Contract, Law, Operator, Play). The path for the current case is highlighted; unvisited nodes are dimmed. Right: two verdict cards, "Inside the game" (what the operator will do: nothing, reverse, ban, or "not the operator's call") and "Outside the game" (what law may do: nothing, possible theft or fraud, contract claim). Under the cards, a one-line explanation generated from the path, for example "Stopped at Q2: control was taken by an outside means."

**Controls.**
- Taker: Operator / Another player.
- Means (shown if taker is a player): In-game trust (victim handed it over) / Permissions the victim granted (corp roles) / Deception in game chat / Deception involving real money or impersonating the operator / Account hacking or phishing / Physical threats or force / A bug.
- Operator's rule on in-game scams: Allowed (EVE-style) / Forbidden (OSRS-style).
- Real-money market exists for this item: Yes / No.
- Item value in US$: number input, default 870, shown in the verdict text only.
- Preset buttons: "EBank withdrawal," "EBank cash-out," "Leeuwarden," "Corp theft," "Character Bazaar scam," "OSRS doubling," "Bragg."

**Decision logic (implement exactly).**
```
if taker == Operator: layer = Contract
else if means in {Account hacking, Physical threats}: layer = Law
else if means == Deception involving real money or impersonating the operator: layer = Operator   (and Outside card shows "possible fraud")
else if means == A bug: layer = Operator (exploit)
else if means == Deception in game chat and scamRule == Forbidden: layer = Operator
else: layer = Play
Outside card:
  Law → "Possible theft or fraud if the item has real value and the victim controlled it" (add "value: US$X" when market == Yes; if market == No, add "a court may doubt the item has real value")
  Contract → "Claim against the operator under its terms and consumer law"
  otherwise → "No outside remedy expected"
```
The "EBank cash-out" preset is special: taker Player, means In-game trust, plus a toggle "Sold for real money" = on, which forces the Inside card to "Ban: real-money trading" while the Play verdict for the withdrawal is shown struck through. Implement the toggle generally: when "Sold for real money" is on, the Inside card always adds "Ban for real-money trading" regardless of layer.

**Test cases (page must reproduce).**
- EBank withdrawal: Player, In-game trust, scams Allowed → Play; Inside "No action"; Outside "No outside remedy expected."
- EBank withdrawal, change means to Account hacking → Law.
- Leeuwarden: Player, Physical threats, market Yes → Law; Outside card mentions the value.
- Corp theft: Player, Permissions granted, scams Allowed → Play.
- OSRS doubling: Player, Deception in game chat, scams Forbidden → Operator.
- Bragg: Operator → Contract.

**Accessibility and style.** Use `templates/interactive-tokens.css` inline. All controls are native radio groups and buttons, keyboard operable, with labels. The highlighted path must be shown by weight and an "on path" text marker, not colour alone. Respect `prefers-reduced-motion`. No game art or logos.
