# MMO402 · Week 04 — Wars, Betrayals and Meta-Gaming

**Why this matters:** Some of the most famous stories in online games are thefts, betrayals and ambushes that the developer refused to undo. Other acts that look almost identical get the player banned. If you run a world, you have to say where that line sits before the first heist, because your players will test it in week one and your support team will need an answer that holds up.

**You will be able to:**
- Apply the four-part allowed-play test (means, stakes, target, notice) to a betrayal or scam and predict how an operator with a given policy will rule.
- Compute the real-money shadow of an in-game loss from a currency price, and explain why that shadow changes with era and conversion rules.
- Rewrite the scam policies of EVE Online, Old School RuneScape, League of Legends and the board game Diplomacy as settings of the same four tests.
- Critique a proposed betrayal policy by naming who it protects (the victim, the game's frame or the operator) and what stories it rules out.

**Before class:** Salen & Zimmerman, *Rules of Play* (2003), chapter 9, "The Magic Circle" (reread; you met it in GD101). EVE University Wiki, "Scams" (about 15 minutes, read the section on what CCP forbids). Graham, F., "The struggle among the stars", BBC News, 23 February 2009 (5 minutes). Groen, *Empires of Eve* (2016), the chapter on the fall of Band of Brothers, if you did not finish it for week 2.

**Prerequisites from earlier courses:** [GD101 week 3, resources, conflict, boundaries and outcome](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md) (the magic circle as a boundary). [MMO301 week 6, EVE Online: the single-shard sandbox](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md) (how EVE prices crime instead of banning it). [MMO401 week 8, player banks, loans and scams](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w08-player-banks-loans-and-scams.md) (why unenforced banks end in theft; this week asks whether the theft is allowed, not why it happens). [MMO303 week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (betrayal as a payoff). [MMO305 week 8, griefing](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md) (Foo and Koivisto's griefing types). [MMO304 week 11, real-money trade](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md). This course: [week 1, worlds as polities](w01-worlds-as-polities.md) (the operator as sovereign) and [week 2, alliances and councils](w02-emergent-player-government-alliances-and-councils.md) (the Band of Brothers collapse as a permissions problem).

**Interactive:** [w04-allowed-play.html](../examples/w04-allowed-play.html)

---

## 1. Two thefts, one ban

In June 2009 the chief executive of EBank, a player-run bank in EVE Online, took about 200 billion ISK (EVE's currency) out of the bank's vault. That was roughly 8% of the 2.6 trillion ISK the bank held. News of the theft started a run, and depositors rushed to pull their money out. The player, known in the game as Ricdic, then sold the stolen ISK for about £3,115 of real money and used it toward a house deposit and medical bills.

CCP, EVE's developer, banned him. But read the BBC's account closely. He was thrown out because trading in-game currency for real money breaks EVE's terms. The BBC adds that EVE's rules would not have punished him if he had simply stolen the money and kept it in the game.

So the depositors lost exactly the same ISK either way. The theft was allowed. What got him banned was what he did with the loot afterwards, a step the victims never saw and that did not change their loss by one ISK.

That is this week's puzzle. When a world allows fraud, what exactly is it allowing? And where does "part of the game" end?

## 2. Worked example: when is in-world fraud allowed play?

### The hook, continued

EBank is one case in a long run. In April 2005 a player corporation called the Guiding Hand Social Club spent ten months placing agents inside a rival corporation, Ubiqua Seraph. On the night of the job they killed its CEO's ship, took her frozen corpse as a trophy for the client who had paid them, and emptied the corporation's hangars in every office across the galaxy. PC Gamer put the damage at more than 30 billion ISK. In 2006 another player ran off with about 700 billion ISK from an in-game bank. In early 2009 a director of Band of Brothers, then one of the largest alliances in the game, defected to Goonswarm and used his access to strip and disband his own alliance. Players asked CCP to roll the game back. The BBC reported that because no rules had been broken, the changes stood.

All four stories are betrayals. Three of them stood untouched and one ended in a ban. You need a model that sorts them.

### The model

Call an act **allowed play** if the operator treats it as a legitimate move inside the world, with no penalty for the actor and no restoration for the victim. The model is a test with four parts. Each part is a yes/no question, and an act is allowed play only if it passes all four:

```
allowed = M × S × T × N        (each is 1 for "passes", 0 for "fails")
```

- `M`, **means**. Did the actor use only mechanics the game offers every player? Bug exploits, bots, hacked clients and stolen accounts fail.
- `S`, **stakes**. Did everything taken and everything gained stay inside the game's asset layer? Selling the loot for real money fails. So does scamming someone out of real-world property.
- `T`, **target**. Was the act aimed at a character in the world, rather than at the person behind it or at the operator's authority? Impersonating staff or another player fails. So do out-of-game threats and harassment.
- `N`, **notice**. Could the victim fairly have known this was possible? The rules must say so, and the victim must have had a reasonable chance to learn them.

Because the four terms multiply, one failure is enough. The test has no weights and no partial credit. That is a design choice, and section 4 comes back to it.

EVE's published scam policy maps onto the test almost clause by clause. The EVE University Wiki summarizes it as follows. CCP treats most scams as part of the game and will not act on petitions about them, with a short list of exceptions:

- Impersonating another character or corporation is bannable (fails `T`).
- Scamming someone out of real-world assets is not allowed (fails `S`). The ban on selling ISK for money belongs here too.
- Abusing new players' lack of knowledge in the starter systems is prohibited (fails `N`).
- Fraud in a character sale through the official character bazaar can be reversed (a sale that runs through the operator's own service, so it fails `T`).

Bots and exploits are covered by separate rules (fails `M`).

### Numbers you can check: the verdict table

Apply the test to the four real cases and three constructed ones that probe each exception. "EVE's ruling" is what the sources report, not what the model says.

| Case | M | S | T | N | Model verdict | EVE's ruling |
|---|---|---|---|---|---|---|
| Guiding Hand heist on Ubiqua Seraph (2005) | 1 | 1 | 1 | 1 | Allowed | Stood; CCP's stance was to let players do what they may |
| 700 billion ISK bank theft (2006) | 1 | 1 | 1 | 1 | Allowed | Reported as one of EVE's permitted swindles |
| Band of Brothers disbanded by its own director (2009) | 1 | 1 | 1 | 1 | Allowed | Rollback refused; no rules broken |
| EBank theft, kept in the game (2009) | 1 | 1 | 1 | 1 | Allowed | Would not have been punished |
| EBank theft, sold for £3,115 (2009) | 1 | 0 | 1 | 1 | Violation | Player banned |
| A scammer poses as a well-known corporation to take a hauler's cargo (constructed) | 1 | 1 | 0 | 1 | Violation | Bannable impersonation |
| A contract scam on a two-day-old player in a starter system (constructed) | 1 | 1 | 1 | 0 | Violation | Prohibited |

Check the EBank rows. Change only `S` from 1 to 0 and the verdict flips. Nothing about the victims changed.

### Numbers you can check: the real-money shadow

The `S` question keeps coming back because in-game money has a price outside the game. Define the **real-money shadow** of a loss as

```
shadow = L × P
```

where `L` is the loss in game currency and `P` is the real-world price of one unit of that currency at the time. The shadow is a way of measuring, not a statement that anyone paid that much. Most of the ships lost in EVE's big battles were bought with ISK earned in play.

The sources give three data points. Work out `P` for each (prices per billion ISK, rounded).

| Event (year) | Loss `L` | Reported real value | `P` per billion ISK | Where the price came from |
|---|---|---|---|---|
| Guiding Hand heist (2005) | 30 billion ISK | US$16,500 | US$550 | A third-party gold seller's prices at the time |
| EBank cash-out (2009) | 200 billion ISK | £3,115 | £15.6 | What the thief was paid |
| Battle of B-R5RB (2014) | about 11,000 billion ISK | US$300,000 to 330,000 | US$27 to 30 | PLEX, CCP's own game-time item, at its market price |

Two things stand out. First, the price of ISK fell roughly twentyfold between 2005 and 2014 (550 / 28.5 ≈ 19). The same "30 billion ISK heist" had a very different real shadow depending on the year. Second, the source of `P` changed. In 2005 it came from a gray market that CCP prohibited. By 2014 it came from PLEX, an item CCP sells for real money that players can trade for ISK on the in-game market. PLEX made the shadow official. The flow runs one way only, since selling ISK or items for money is still banned. But anyone can now read a real price for any loss.

Try one more by hand. Put the 2006 bank theft of 700 billion ISK through both prices. At the 2005 price it shadows about US$385,000. At the 2014 price it shadows about US$20,000. Neither figure was reported at the time. The point is that the shadow depends on when and how you price it, while the verdict does not depend on the shadow at all.

### The visual

Open the interactive. The left panel lists the case cards with their four test chips. The right panel shows two bars for the selected case. One is the victim's loss in game currency. The other is its real-money shadow at a price you set with a slider, with presets for the 2005 and 2014 dollar prices. The 2009 EBank price was reported in pounds, so it has no dollar preset; set the slider by hand if you want to compare it.

Above both panels is a policy bar where you choose which tests your world enforces. Turn off `S` and the EBank cash-out becomes allowed play. Turn on "no deception for gain", the Old School RuneScape setting described below, and every card turns red. Watch the right panel while you do this. The victim's bars never move. Only the verdict changes.

### The insight

The test protects the game's frame, not the victim. Every question asks about the actor's methods, where the proceeds went, whom the act was aimed at, or what the rules announced. None of them asks how much the victim lost. That is why the Ubiqua Seraph heist, with a shadow of US$16,500, stood, while a £3,115 cash-out ended in a ban.

This is a coherent position. The magic circle you met in GD101 week 3 is the boundary that makes "taking your friend's queen" a good move rather than theft. EVE draws that circle around the game's asset layer and defends the edges. Inside the circle, loss is part of play. Crossing the edge in either direction breaks the frame, whether that means real money leaving, a real identity being borrowed, or a newcomer who never saw the rules.

It is also a position with costs, and you should see them before you copy it.

### Cross-game recognition

Rewrite each game's rule as settings of `M`, `S`, `T` and `N`.

**Old School RuneScape (current rules).** Rule 2 of the Code of Conduct prohibits scamming, and a reported scammer can be muted or banned. The game adds a fifth test that EVE lacks, "was the act deceptive and aimed at gain?" Any deceptive act for gain fails it. The Old School RuneScape Wiki also states that victims will not get their items back under any circumstances, even when Jagex punishes the scammer. So Jagex draws the circle much tighter than CCP does, yet the victim's outcome is the same in both games. The loss stands. What differs is the risk to the scammer. MMO401 week 8 calls this the penalty `K`.

**League of Legends (Riot Games Terms of Service, version of 1 December 2024).** The user rules forbid acts that defraud or may defraud another player, "including by scamming or social engineering". League has little tradable property, so the rule mostly protects accounts and in-game purchases. It is the same tighter circle as Old School RuneScape. Deception about items or accounts fails, however clean the means.

**Diplomacy (board game, 1959).** In the negotiation phase players may promise anything, and no promise is binding. A well-timed betrayal is a standard way to win. That is `S`, `T` and `N` all set to pass by the rulebook. Diplomacy still has an `M` line, though. Betraying an ally is play, but peeking at another player's written orders is cheating. Even the purest betrayal game keeps the means test.

**Your own group chat.** When friends play a social-deduction game over voice and one of them lies about their role, nobody calls it fraud. If the same friend lies to borrow real money "for the game", everyone does. The line sits at `S`.

Four contexts give one structure. Every world that allows betrayal still has a boundary, and the boundary is always drawn with some mix of these four questions.

### Eyes-open design judgment

- **Decide whose interests the line protects, and say so.** EVE's line protects the frame. A line that protected victims would need a loss threshold ("thefts over X are reversed"), which would make large heists impossible and small ones safe. Neither is neutral.
- **A permissive line needs a strong `N`.** "Scams are allowed" is fair only if players know it before they have anything to lose. EVE protects starter systems for this reason. A world that allows betrayal but hides the fact in page 30 of its terms fails `N` for most of its players (week 5 measures exactly this).
- **Currency conversion keeps pushing on `S`.** Every official route from money to game currency, such as PLEX, gives every in-game loss a public price. The more real the shadow, the harder it is to tell a crying victim that it was "only a game". The operator who sells the conversion has also profited from the shadow.
- **Restoration is a separate decision from punishment.** Old School RuneScape punishes but does not restore. EVE does neither for allowed scams. A game could restore without punishing, for example by reversing trades flagged within an hour. Choose each on purpose.
- **Allowed betrayal is a product, and a filter.** The PC Gamer account of the 2005 heist reports that the Guiding Hand's operations drove some players out of the game for good. The same stories drew others in. A permissive line selects the players who stay, and that choice is made on the first day, not in the patch notes.

## 3. Wars and meta-gaming

**Meta-gaming** here means play that draws on resources outside the game's fiction: second accounts, voice servers, spreadsheets, forums, and the players' real time zones and jobs. In a world like EVE, most of the war happens in the meta-game.

### Spies are a mechanic

Every betrayal in section 2 depended on access. The Guiding Hand had agents on Ubiqua Seraph's board of directors. The Band of Brothers director held roles that let him disband the alliance. Two things make spying cheap in EVE. Players can run extra characters on extra accounts, so an agent costs a subscription rather than a friendship. And corporations hand out roles that grant access to hangars and wallets. Week 2 showed how the number of keys to a vault sets the chance that one traitor can empty it. The betrayal is emergent. The access that makes it possible was designed.

Spying passes all four tests in EVE. The alt account is a standard feature (`M`). The loot stays in the game (`S`). The agent deceives characters, not people about their real lives (`T`). And the rules announce that corporate theft is possible (`N`). The EVE University Wiki's advice is that a player seriously planning to rob a corporation will hide their intentions until it is too late. That is the sound of `N` being met.

### Wars run on real clocks

The Battle of B-R5RB in January 2014 started with an unpaid bill. EVE's sovereignty system let alliances claim star systems by paying a regular fee to CONCORD, the game's non-player police. Sovereignty came with reinforcement timers, waiting periods of several days that gave defenders time to rally. A single player in the N3 and Pandemic Legion coalition missed the payment on their staging system. The system became open to immediate capture with no timer, and both sides poured in. The fight lasted 21 hours and involved more than 7,548 characters, with at most 2,670 in the system at once. It ended when the server went down for daily maintenance.

Notice what decided it. Wikipedia's account, drawing on Wired, reports that two of the attacking fleet commanders were at their real-world jobs when the fight began. The defenders hoped their United States players would turn the tide once they logged on, and the reinforcements they expected did not come. Reinforcement timers exist to move battles onto a schedule that real people can attend. That means the designer is choosing which time zones, jobs and sleep patterns can defend territory. The timer is a rule about the meta-game.

### Where meta-gaming meets the target test

The meta-game is where `T` is tested most often. Forum propaganda about an enemy alliance's leaders is aimed at characters and organizations. Publishing a player's real name, or organizing people to message them outside the game, is aimed at the person. The step from one to the other is short, and it usually happens in spaces the operator does not run, such as voice servers, social media and fan sites.

An operator has two options here. One is to extend enforcement to conduct outside the game when it targets players, at least for threats and for publishing personal details. The other is to declare it out of scope. The second leaves players with no remedy for the harms most likely to follow them home. Week 6 looks at how moderation copes with that volume, and week 7 at how its judgments are reviewed.

## 4. Why a yes/no test, and what it costs

The allowed-play test is a set of bright lines. **Bright-line rules** decide by checking facts ("was the loot sold for money?"). **Standards** decide by weighing ("was this unreasonably harmful?"). Bright lines are cheap to apply, predictable for players, and hard to argue about in a support ticket. Standards fit messy cases better but need judgment, and judgment at scale is expensive and inconsistent.

EVE's test is almost pure bright line, and that fits a single-shard world where scams are a daily event and every ruling is watched by the whole player base. Its cost is the cases it gets "wrong" by anyone's intuition. A months-long heist that destroys a corporation passes. A newcomer who gets scammed on day ten, one day after leaving the starter systems, has no remedy. A clumsy player who sells 1 billion ISK for pocket money is banned.

Two design moves soften bright lines without giving up predictability:

1. **Graduated notice.** Instead of one line between starter systems and everything else, raise `N` protection gradually with a player's age or with explicit opt-in. The rules stay factual ("account younger than 30 days"), yet the edge moves.
2. **Friction instead of verdicts.** Many scams in the verdict table exploit presentation, not rules. Clearer trade windows, contract summaries and warnings when a price is far from market prevent them without anyone ruling on them. MMO401 week 8 sorts scams by trust gap. Use its table when you choose which gaps to close in the interface and which to leave as play.

### Betrayal as a payoff

It is worth seeing betrayal through MMO303 week 10. Two allies each choose to cooperate or to defect. If promises cannot be enforced, the one-shot game is a prisoner's dilemma and defection is the dominant move. What keeps alliances together is repetition, reputation and the chance of revenge, the same forces that keep MMO401's honest banker honest until the vault gets too big. The operator's policy is one of the payoffs. Allowing betrayal, as EVE does, keeps the dilemma sharp. Banning it, as Old School RuneScape does, adds a penalty to defection and softens the dilemma. So your allowed-play line is also a statement about how much trust players must build by themselves.

## In-class activity (25 minutes)

Groups of three. You run *Harbor*, a fictional survival sandbox with player-owned towns, a player market, and a premium item bought for real money that can be sold in-game for gold (like PLEX).

1. Write your allowed-play policy in five lines or fewer, using `M`, `S`, `T`, `N` and any extra test you add (8 minutes).
2. Rule on each case below with your policy (10 minutes):
   - a. A mayor collects taxes for a town wall for three months, then leaves with the treasury.
   - b. A player uses a second account to join a rival town, gains builder rights, and demolishes its walls the night before a raid.
   - c. A player sells 40 premium items' worth of stolen gold on a third-party site.
   - d. A player tells a new arrival, in their first hour, that the market tax is 50% and "helps" them sell at a loss.
   - e. A raid leader posts a rival mayor's real first name and city in a public voice channel during a war.
3. Swap policies with another group and find one case where their policy gives a verdict you think is wrong. Write one sentence on which test caused it (7 minutes).

Expected output: a policy, five verdicts with the failing test named, and one disagreement traced to a test.

## Common misconceptions

- **"EVE allows everything."** It allows most deception inside the asset layer. It bans impersonation, real-money trading, starter-system abuse and exploits, and it enforces those rules with bans.
- **"The bigger the loss, the more likely the operator steps in."** In EVE the verdict does not depend on the size of the loss. The EBank depositors' 200 billion ISK loss was never restored. The thief was banned for what he did afterwards.
- **"Banning scams protects victims."** Old School RuneScape bans scams and still does not restore stolen items. Punishment changes the scammer's risk, not the victim's loss. Restoration is a separate decision.
- **"Meta-gaming is cheating."** Most meta-gaming (alt-account spies, voice comms, planning around time zones) is allowed and designed for. It becomes a violation when it fails a specific test, most often `T`.

## Check yourself

1. A player in EVE runs a fake "ISK doubling" service in a major trade hub, keeps the ISK, and never sells it. Apply the four tests. What does the model predict CCP does?
2. The same player advertises the service by using a character name that differs from a famous alliance leader's by one letter. Which test fails, and does the verdict change?
3. Suppose a later heist takes 90 billion ISK, at a time when the PLEX price makes 1 billion ISK worth US$25. What is the real-money shadow? What would it have been at the 2005 price used in section 2?
4. A designer proposes "thefts larger than 500 billion ISK are reversed". Using the verdict table, name one historical case this rule would have changed. Name one behavior the rule would create.
5. Old School RuneScape and EVE handle a small scam differently. Compare the victim's outcome and the scammer's expected penalty in each game, using the sources in this lecture.

<details>
<summary>Answers</summary>

1. `M = 1` (trade and chat are standard mechanics), `S = 1` (the ISK stays in the game), `T = 1` (it targets characters), `N = 1` (the hub is not a starter system, and the rules announce that scams are allowed). Allowed play. CCP takes no action, and victims have no petition.
2. `T = 0`. Posing as another character or corporation is bannable impersonation, so the verdict flips to violation even though the scam itself is unchanged.
3. `90 × 25 = US$2,250`. At the 2005 price of US$550 per billion it would shadow `90 × 550 = US$49,500`. Same ISK, a 22-fold difference.
4. The 2006 theft of about 700 billion ISK would have been reversed. The rule would push thieves to steal just under the threshold, perhaps in several separate thefts of 499 billion. It would also create disputes over how a loss is valued, and it adds a loss-based standard to a bright-line test.
5. In both games the victim does not get the items back. In EVE the scammer's expected penalty is zero for an allowed scam. In Old School RuneScape it is the chance of being reported and caught, times the cost of a mute or ban.

</details>

## Lab / assignment hook

[Lab 04, the allowed-play brief](../labs/lab04.md). You write a two-page case analysis of one documented betrayal or scam from any online game. You apply the four tests, compute its real-money shadow with a sourced price, compare the operator's actual ruling with your model's prediction, and propose one policy change with its cost. It counts toward the case analyses (30%).

## Sources

- Graham, F. (2009). "The struggle among the stars." BBC News, 23 February 2009. http://news.bbc.co.uk/1/hi/technology/7905924.stm. The Band of Brothers collapse (a disgruntled director contacted Goonswarm, stripped assets, disbanded the alliance), player calls for a rollback, and the report that the changes stood because no rules were broken. Also the 2006 theft of 700 billion ISK from an EVE bank and the January 2009 Dynasty Banking theft of over 80 billion ISK.
- BBC News (2009). "Billions stolen in online robbery." 3 July 2009. http://news.bbc.co.uk/1/hi/8132547.stm. EBank: about 200 billion ISK taken in early June 2009, 8% of 2.6 trillion ISK in deposits; sold for £3,115; a run on the bank; the player was removed from the game because trading in-game cash for real money breaks EVE's terms, and would not have been sanctioned for the theft alone.
- Wikipedia, "Eve Online" (accessed September 2026). The corporate infiltration and assassination worth about US$16,500; the 700 billion ISK scam (citing Softpedia, 2007); EBank; the one-way PLEX rule (PLEX bought for money and sold in-game for ISK; selling ISK for money prohibited); 500 PLEX for 30 days of Omega time since May 2017.
- Francis, T. (2005, republished 2015). "Murder Incorporated: ten months of deception for one kill in Eve Online." PC Gamer, originally in PC Gamer UK, September 2005. The Guiding Hand Social Club's hit on Ubiqua Seraph on 18 April 2005; damage above 30 billion ISK, US$16,500 at a gold seller's prices at the time; a contract fee of 1 billion ISK; CCP's stated intention to let players do what they may; some victims leaving the game for good.
- Wikipedia, "Battle of B-R5RB" (accessed September 2026), drawing on CCP's report (CCP Dolan, 1 February 2014), Wired (Moore, 8 February 2014) and Polygon (Pitcher, 28 and 30 January 2014). A missed sovereignty payment, reinforcement timers, 21 hours, 7,548 characters with a peak of 2,670 in system, about 11 trillion ISK destroyed, US$300,000 to 330,000 at PLEX prices, commanders at their jobs, and the end at daily downtime.
- EVE University Wiki, "Scams" (accessed September 2026). CCP treats most scams as part of the game and does not accept petitions for them. Exceptions: fraud in official character bazaar sales (reversible), impersonation (bannable), abuse of new players in starter systems, scams for real-world assets, and scams using PLEX for GOOD campaigns (permanent ban). Also the advice that corporate thieves hide their intentions until it is too late.
- Old School RuneScape Wiki, "Scams" (accessed September 2026). Rule 2 of the Code of Conduct prohibits scamming (mute or ban if reported); victims do not have items returned under any circumstances.
- Riot Games, Terms of Service, last modified 1 December 2024 (accessed September 2026). User rules forbid acts that defraud or may defraud any other player, including by scamming or social engineering.
- Wikipedia, "Diplomacy (game)" (accessed September 2026). Created by Allan B. Calhamer in 1954, published in 1959; players are not bound by anything they say or promise in negotiation.
- Salen, K. & Zimmerman, E. (2003). *Rules of Play*. MIT Press. Chapter 9, the magic circle.
- Groen, A. (2016). *Empires of Eve: A History of the Great Wars of EVE Online*. Lightburn Industries.

## Interactive spec: examples/w04-allowed-play.html

**The one insight:** the allowed-play verdict depends on the actor's means, where the loot went, whom the act targeted and what the rules announced. It never depends on the victim's loss. Toggling a policy test flips verdicts while the loss bars stay still.

**Layout.** A policy bar across the top. Below it two linked panels, side by side on desktop and stacked on mobile (case list first).

- **Policy bar.** Five toggles: "Means (M)", "Stakes (S)", "Target (T)", "Notice (N)", all on by default, and "No deception for gain (D)", off by default. Three preset buttons: "EVE Online" (M, S, T, N on; D off), "Old School RuneScape" (all five on), "Diplomacy" (only M on).
- **Left panel, "Cases".** Seven case cards in the order of the verdict table in section 2. Each card shows its name, four small chips `M S T N` coloured pass or fail (with the letters and a pass/fail icon, not colour alone), a verdict badge ("Allowed play" or "Violation") computed from the current policy, and a smaller line "EVE's ruling: ..." with the text from the table. When the policy equals the EVE preset, a counter above the list reads "Your policy matches EVE's ruling on N of 7 cases" (it must read 7 of 7 for the EVE preset).
- **Right panel, "What the victim lost".** For the selected case (click or Enter on a card), two horizontal bars. Bar 1 is the loss in billions of ISK on a log scale from 1 to 20,000. Bar 2 is the real-money shadow `L × P` in US dollars, log scale from $10 to $1,000,000. Below the bars sits a slider `P` (US$ per billion ISK), 5 to 1,000, log steps, default 550, with presets "2005 gold seller (550)", "2014 PLEX (28.5)". Each bar carries its exact value in text. The bars must not change when policy toggles change; only the verdict badge on the card changes, and a short line under the bars repeats the verdict.

**Case data.**

| id | name | M | S | T | N | deceptive gain (D test fails) | loss L (bn ISK) |
|---|---|---|---|---|---|---|---|
| ghsc | Guiding Hand heist (2005) | 1 | 1 | 1 | 1 | yes | 30 |
| bank06 | 700 bn bank theft (2006) | 1 | 1 | 1 | 1 | yes | 700 |
| bob | Band of Brothers disbanded (2009) | 1 | 1 | 1 | 1 | yes | 0 (show "not reported"; hide bars) |
| ebank-keep | EBank theft kept in game (2009) | 1 | 1 | 1 | 1 | yes | 200 |
| ebank-cash | EBank theft sold for money (2009) | 1 | 0 | 1 | 1 | yes | 200 |
| impostor | Impersonating a corporation (constructed) | 1 | 1 | 0 | 1 | yes | 5 |
| rookie | Starter-system contract scam (constructed) | 1 | 1 | 1 | 0 | yes | 0.05 |

**Formula.**

```
for each case c:
  fails = (policy.M and c.M == 0) or (policy.S and c.S == 0)
       or (policy.T and c.T == 0) or (policy.N and c.N == 0)
       or (policy.D and c.deceptiveGain)
  verdict = fails ? "Violation" : "Allowed play"
shadow = L × P
```

**Test values.**

- EVE preset: ghsc, bank06, bob, ebank-keep allowed; ebank-cash, impostor, rookie violations. Counter reads 7 of 7.
- Old School RuneScape preset: all seven violations.
- Diplomacy preset: all seven allowed.
- EVE preset with S turned off: ebank-cash becomes allowed; counter reads 6 of 7.
- ghsc at P = 550: shadow $16,500. At P = 28.5: $855.
- bank06 at P = 550: $385,000. At P = 28.5: $19,950.
- ebank-keep and ebank-cash show identical bars at any P.

**Accessibility.** All toggles and cards reachable by keyboard with visible focus; the verdict change is announced in an `aria-live` region; pass/fail chips use letters and icons as well as colour. `prefers-reduced-motion` turns off bar transitions. No game logos or art; ships and players are not drawn at all.
