# MMO402 · Week 08 — Rights of Avatars (Koster 2000)

**Why this matters:** Your players will ask what they are entitled to: a warning before a rule changes, an explanation before a ban, protection from a developer who plays favourites. Raph Koster's 2000 declaration is the best-known attempt to answer that question in writing. Reading it closely shows you which promises a studio can keep, which ones collide with each other, and why the most curious players pay when a studio skips the rule of law.

**You will be able to:**
- Sort the articles of Koster's declaration into rule-of-law, liberty, accountability and equality clauses, and state which party each one constrains.
- Compute a player's chance of being punished over a career under retroactive, warn-first and notice-first exploit policies.
- Explain, with numbers, why retroactive enforcement concentrates punishment on explorers who acted in good faith.
- Rewrite an abstract right as a studio commitment that can be checked, and name the right it conflicts with.

**Before class:** Koster, "Declaring the Rights of Players" (raphkoster.com, 27 August 2000). You skimmed it for week 1. This week read all 19 articles and the commentary that follows them, about 30 minutes. Balkin, "Virtual Liberty: Freedom to Design and Freedom to Play in Virtual Worlds," *Virginia Law Review* 90(8), 2004, introduction and part I. Optional: Lastowka and Hunter, "The Laws of the Virtual Worlds," *California Law Review* 92(1), 2004, the section on avatar rights.

**Prerequisites from earlier courses:** [MMO301 week 11, Koster's Laws](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w11-kosters-laws-of-online-world-design.md) (the same author's earlier design observations). [MMO301 week 8, player types](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w08-player-types-bartle-1996-and-the-heros-journey.md) (who explorers are). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the career-risk formula is a "chance of at least one" calculation). [MMO401 week 12, exploits and rollbacks](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w12-economic-shocks-exploits-and-rollbacks.md). From this course: [week 1](w01-worlds-as-polities.md) (the developer as sovereign, LambdaMOO), [week 3](w03-eves-council-of-stellar-management.md) (EVE's player council), [week 5, rules and terms of service](w05-rules-eulas-and-terms-of-service.md) and [week 7, justice systems](w07-justice-systems-reports-reviews-appeals.md) (strike ladders and appeals).

**Interactive:** [w08-retroactive-risk.html](../examples/w08-retroactive-risk.html)

---

## 1. The declaration and where it came from

In August 2000 Raph Koster, who had worked on Ultima Online and whose design notes you read in MMO301 week 11, posted an essay called "Declaring the Rights of Players." Its centre is a short document in 19 articles. Koster modelled its language on two famous texts: the French Declaration of the Rights of Man and of the Citizen (1789) and the United States Bill of Rights. He swapped "citizens" for "avatars" and "the state" for "the admins" (the administrators who run the servers), and asked what such a document would look like for an online world.

The essay was written as a provocation. Koster called the declaration hypothetical and said it was full of traps. He also noted the plain fact that admins control the hardware, the software and the data. They can switch the world off. Any rights players hold exist because the operator grants them or because players organize to keep them. His practical argument was that operators should adopt most of these principles anyway, because a world whose rules are clear and fairly enforced is a better business.

### The 19 articles, sorted

Reading 19 articles in a row blurs them. Sort them by what they do and whom they bind. The paraphrases below are short summaries; read the original for the wording.

| Cluster | Articles (paraphrased) | Constrains whom |
|---|---|---|
| Equality and personhood | 1: avatars are equal in rights, privileges exist only for the common good. 2: the community exists for its members' good and avatars are persons. 13: required contributions are shared fairly, and payment never buys rights. | Mainly admins |
| Rule of law | 3: admins must publish the standards they enforce. 4: liberty ends only where others' rights begin, set out in a clear code. 5: the code forbids only what harms the community or the world. 7: punishment only under the published code. 8: only necessary penalties, and no punishing acts that were allowed when done. 9: presumption of innocence, humane treatment of the accused. 15: everyone, admins included, follows the code. | Admins and players |
| Liberty | 10: freedom of opinion. 11: freedom of speech, with responsibility defined by the code. 17: freedom of assembly. 18: privacy, no investigation without cause. | Admins, and players against each other |
| Accountability of power | 6: the community shapes the code, and admins must listen. 12: admin powers exist for the common good, not personal advantage. 14: admins answer for their decisions. 16: player data is protected, except to save the world itself. | Admins |
| Reserve | 19: rights not listed are kept by the avatars. | Admins |

Two things stand out. First, most articles bind the admins, not the players. The declaration is about limiting the operator's power, exactly as its 1789 model was about limiting a king's. Second, the rule-of-law cluster is the largest. Koster's concern was less "what may players do" and more "how may players be punished."

### Why nobody adopted it, and why it still matters

No major MMO adopted the declaration. The reasons are the ones Koster anticipated. Terms of service (week 5) give the operator the right to change rules, close accounts and alter data at any time, and a company's lawyers will not accept a binding promise to the contrary. Some articles conflict with obligations the operator owes outside the game: article 18's privacy clause runs into the need to read chat logs to stop harassment, and article 16's data integrity runs into rollbacks after an exploit.

Yet many of its ideas now appear in practice, piecemeal. Published codes of conduct are article 3. Appeals are articles 9 and 14. Public exploit notices are article 8. The EU's Digital Services Act, which you met in week 7, requires stated reasons and a complaint route, which is articles 3, 7 and 14 written into law for platforms. The declaration is best read as a checklist of the promises players will eventually demand, twenty years early.

## 2. Rights that collide

A right for one player can be a restriction on another. Koster's own article 4 admits this: liberty ends where others' rights begin. In a world, that boundary is a design decision.

- **Speech against harassment.** Article 11 protects speech. Other players want freedom from abuse. Every chat filter, mute and ban draws the line between them. There is no neutral setting: an unfiltered chat protects the speaker, a heavy filter protects the listener.
- **Privacy against safety.** Article 18 forbids investigation without cause. Week 7's review pipeline reads chat logs of reported players. Is a report "cause"? If yes, anyone can trigger an investigation of anyone. If no, the reviewers have no evidence.
- **Data integrity against fairness.** Article 16 protects a player's data. After a duplication exploit, a rollback deletes innocent players' progress to remove the exploiters' gains. MMO401 week 12 showed the trade-off in economic terms. In rights terms, one player's right to their data collides with every other player's right to a fair economy.
- **Assembly against the world.** Article 17 protects assembly. Week 2's coalitions of tens of thousands are assemblies too, and they can make whole regions unplayable for everyone else.

Balkin's 2004 paper names the deepest collision. On one side is the **freedom to design**: the right of the people who build a world to shape it, including its rules and its limits. On the other is the **freedom to play**: the interest of players in the world they have invested in, including the social life they built there. Every article of Koster's declaration that binds the admins protects freedom to play by limiting freedom to design. Your job as a designer is to choose, knowingly, how much design freedom to give up and in return for what.

## 3. Worked example: the exploit nobody declared

### The hook

During development of Street Fighter II, producer Noritaka Funamizu noticed during a bug check that a player could land extra hits in a sequence on one of the bonus stages. He judged the timing too hard to be a useful feature and left it in as a hidden one. Players found it. Combos became the backbone of a whole genre. Had Capcom punished the first players who found them, there would have been nothing to build on.

Now read a modern exploit policy. Blizzard's, as summarized by the Warcraft Wiki, defines an exploit as playing in a way clearly not intended by the developer to gain an advantage, and warns of temporary or permanent suspensions. EVE Online keeps a public page of declared exploits, but the page itself warns that it is not an exhaustive list of every disallowed action. In both cases the test is the developer's intent. Players cannot read intent. They can only read the game.

So here is the puzzle. A policy that says "we may punish anything we later decide was unintended" sounds reasonable case by case: surely the player knew. How dangerous is it across a career, and to whom?

### The model

Take a single player who acts in good faith: they use techniques they believe are part of the game.

- `n` is the number of **novel techniques** the player tries in a year: unusual routes, item combinations, positioning tricks, market plays.
- `q` is the chance that any one of those techniques is later ruled an exploit by the developer.
- `d` is the chance that, once a technique is ruled an exploit, the developer detects this player's past use of it.
- `Y` is the number of years the player plays.

Per technique, the chance of being caught out is `r = q × d`. Over a career of `N = n × Y` techniques, under three policies:

```
Retroactive ban     (any detected past use is banned):
    P(ban) = 1 − (1 − r)^N

Warn first          (first detected use gets a warning, second a ban):
    P(ban) = 1 − (1 − r)^N − N × r × (1 − r)^(N − 1)

Notice first        (only uses after a public exploit notice are punished):
    P(ban) = 0 for a good-faith player who stops using a technique once it is declared
```

The first line is the complement rule from MA102 week 3: the player avoids a ban only if every one of `N` techniques comes out clean. The second subtracts the chance of exactly one detection, the binomial term from MA102 week 6, because one detection only earns a warning. The third is article 8 of Koster's declaration, no punishment for acts that were allowed when done, turned into a policy.

### Numbers you can check

Take `q = 0.02` (one novel technique in fifty is later ruled an exploit) and `d = 0.5`. Then `r = 0.01`: a 1% risk per technique. Compare a casual player who tries 2 novel techniques a year with an explorer, in Bartle's sense from MMO301 week 8, who tries 50.

| Player | Techniques `N` | Retroactive ban | Warn first | Notice first |
|---|---|---|---|---|
| Casual, 1 year | 2 | 1.99% | 0.01% | 0 |
| Casual, 3 years | 6 | 5.85% | 0.15% | 0 |
| Explorer, 1 year | 50 | 39.5% | 8.9% | 0 |
| Explorer, 3 years | 150 | 77.9% | 44.3% | 0 |

Check the explorer's first year by hand:

```
retroactive: 1 − 0.99^50 = 1 − 0.605 = 0.395
warn first:  0.395 − 50 × 0.01 × 0.99^49 = 0.395 − 50 × 0.01 × 0.611 = 0.395 − 0.306 = 0.089
```

A 1% risk per technique sounds negligible, and for the casual player it is. For the explorer, a retroactive policy means a better-than-even chance of a ban within three years, for play they believed was legitimate.

Now look at a whole server. Suppose 100,000 players, of whom 2% are explorers with `n = 50` and the rest casual with `n = 2`, over one year:

```
Retroactive:  explorers banned = 2,000 × 0.395  ≈ 790
              casuals banned   = 98,000 × 0.0199 ≈ 1,950
              explorers' share of bans = 790 / 2,740 = 29%

Warn first:   explorers banned = 2,000 × 0.0894 ≈ 179
              casuals banned   = 98,000 × 0.0001 ≈ 10
              explorers' share of bans = 179 / 189 = 95%
```

Under the retroactive policy, 2% of the population takes 29% of the bans. The warn-first ladder from week 7 protects casual players almost completely, which is why it feels fair to most of the community, but it makes the concentration worse: 95% of the remaining bans land on explorers. Only notice-first removes the good-faith explorer's risk altogether.

### The insight

The risk per act is small. The risk per career is large, and it falls on your most curious players. They are the ones who find the bugs, write the guides, discover the strategies that become the meta, and report the exploits they stumble on. A retroactive policy teaches them one lesson: do not experiment, or if you do, keep it to yourself. That is the opposite of what a live world needs.

### A visual you can move

Open `examples/w08-retroactive-risk.html`. The left view shows the per-technique risk `r` as a single small bar: it looks harmless. The right view plots career ban risk against the number of techniques `N`, one curve per policy, with markers for the casual player and the explorer. Drag the years slider and watch the explorer marker climb the retroactive curve while the casual marker barely moves. Switch on the server panel to see the share of all bans that fall on explorers.

### Cross-game recognition

**RuneScape, the Falador Massacre (6 June 2006).** During a party in a player-owned house with player-versus-player combat enabled, a bug let a group of players keep their ability to attack after leaving the house. They killed players across the city of Falador, where combat should have been impossible. Jagex moderators first messaged the exploiters asking them to stop, then disabled player combat across the game until morning. Players who killed large numbers of others were permanently banned. There was no rollback, and victims got no compensation for lost items. In the model, this was a technique with `q` close to 1: nobody could believe attacking in a safe city was intended. Retroactive punishment of an obvious exploit does not threaten good-faith explorers, because they would not have used it. The model's warning is about ambiguous techniques, not obvious ones.

**EVE Online, declared exploits (current).** CCP maintains a public list of declared exploits, each linked to the notice that announced it. Examples include delaying the NPC police's response to a crime by feeding it decoy targets, and farming loyalty points by repeatedly destroying one's own characters. This is notice-first, turned into a document. The list is backed by a catch-all: CCP says it is not exhaustive, asks players to report suspected exploits through a support ticket, and treats publishing steps to abuse an error as publishing an exploit. So EVE runs a hybrid: notice first for declared exploits, discretion for the rest, and a reporting channel that lets an explorer turn a discovery into safety.

**Law outside games.** The ban on retroactive punishment is one of the oldest ideas in legal systems. Article 7 of the European Convention on Human Rights says no one may be held guilty of an offence for an act that was not an offence when it was committed. The United States Constitution bars ex post facto laws. Koster's article 8 imports this principle, and the model shows why it exists: without it, the risk of punishment accumulates on whoever acts most.

**Street Fighter II, the other way round.** Capcom's decision to keep the combo was the opposite of a retroactive ban: a developer finding an unintended technique and declaring it legal. That choice is always available, and it is the cheapest one when the technique makes the game better.

### Eyes-open design judgment

- **Split your exploits into obvious and ambiguous.** For obvious ones, such as duplication, attacking where combat is disabled or bypassing a paywall, retroactive punishment is defensible, because a reasonable player would have known. For ambiguous ones, punish only after notice. Write down the test you use, since "obvious" will be argued in every appeal.
- **Give explorers a safe harbour.** A reporting channel that grants immunity for exploits reported before use at scale turns your riskiest players into your QA team. EVE's exploit ticket category is one example.
- **Notice-first has a cost.** Between discovery and notice, bad-faith players can profit freely. A short window, a public notice the same day, and the option to reverse gains made in bad faith (week 7's asset removal) keep that cost small.
- **Sometimes the right move is to make it legal.** Before you declare an exploit, ask whether the technique hurts anyone, or only surprises you.
- **Measure who you ban.** If a disproportionate share of exploit bans hit long-tenure, high-activity players, the model says your policy is probably retroactive in practice, whatever it says on paper.

## 4. Who watches the admins?

Articles 12, 14 and 15 say admins are bound by the code and must not use their power for personal advantage. The best-documented breach in a major MMO shows why these articles need machinery behind them.

In February 2007 a player named Kugutsumen published evidence that a CCP developer, known in game as t20, had given six valuable blueprints to his own player corporation, a clear advantage over rival groups. CCP set up an internal affairs division to monitor in-game activity by staff accounts, both privileged accounts and staff members' personal player accounts. The developer apologized in a developer blog and stayed at CCP until late 2008. Kugutsumen was permanently banned for breaking the terms of service by revealing the developer's real name. As week 3 discussed, the Council of Stellar Management followed about a year later.

Read this against the declaration:

- **Article 12 (power for the common good)** was broken by the developer.
- **Article 14 (admins account for their decisions)** was enforced only because a player went public. There was no internal route that worked first.
- **Article 15 (everyone follows the code)** was applied unevenly: the whistleblower got a permanent ban, the developer an apology and continued employment.
- **The remedy** was institutional: an internal monitor and, later, a player council. Rights against the admin need a body that is not the admin to watch for breaches.

The general lesson is that rights against the operator need two things the operator does not naturally supply: someone independent who can see what staff do, and a safe route for players to report it. Without the second, the only route is public exposure, and the terms of service may punish it.

## 5. Turning articles into commitments

A right written as "avatars have the right to X" cannot be tested. A commitment written as "we will do Y within Z days, and publish how often we did" can. Here is one translation for five articles, with what each costs and what it collides with.

| Article | Commitment a studio can check | Cost | Collides with |
|---|---|---|---|
| 3, publish standards | A code of conduct with examples, and a changelog of every rule change | Writing and legal review | Flexibility to handle new misconduct |
| 7 and 9, punish only under the code, presume innocence | Every sanction names the rule broken and the evidence; appeals reviewed by someone not in the first decision (week 7) | Reviewer time | Speed of response |
| 8, no retroactive punishment | Ambiguous exploits punished only after public notice; obvious ones listed by category in advance | Exploit window before notice | Economy integrity |
| 13, payment never buys rights | Support queues, appeals and moderation are the same for paying and free players | Lost premium-support revenue | Business model (MMO403) |
| 16, data integrity | Rollbacks only for listed causes, with notice and compensation for innocent players | Engineering and compensation | Fair economy after exploits |

Notice that every commitment has a cost and a collision. That is why Koster's document stayed a declaration. A studio that adopts the commitments one at a time, choosing which collisions it accepts, ends up with most of the declaration in practice while keeping the ability to run the world.

## In-class activity (25 minutes)

In groups of four, each group takes one cluster from the table in section 1 (rule of law, liberty, accountability, equality).

1. For your cluster, pick two articles and rewrite each as a checkable commitment in the form "we will do Y within Z, and publish W" (8 minutes).
2. For each commitment, name one realistic situation in which keeping it would hurt another player or the world (5 minutes).
3. Rule-of-law groups only: use the interactive to choose a policy for ambiguous exploits. Report the explorer's three-year ban risk under your policy with `q = 0.02` and `d = 0.5`. Other groups: estimate the staff hours a week your commitments need for a 100,000-player game (5 minutes).
4. Groups swap commitments and try to break them with a case (7 minutes).

Expected output: four commitments, four collisions, one number from the interactive or a staffing estimate, and one case that broke another group's commitment.

## Common misconceptions

- **"Koster's declaration was a proposal for binding player rights."** Koster presented it as a hypothetical, noted that admins can always switch the world off, and argued mainly that adopting its principles was good practice.
- **"A 1% risk per action is negligible."** Per action, yes. Over 150 actions it is a 78% chance of at least one hit. Risk accumulates on whoever acts most.
- **"A warning-first ladder solves retroactive punishment."** It protects casual players almost completely but still bans many explorers, and it makes explorers an even larger share of those banned.
- **"Rights protect players from the developer, so more rights are always better for players."** Many rights protect one player at another's expense: speech against harassment, privacy against investigation, data integrity against a fair economy.

## Check yourself

1. With `r = 0.02` per technique, what is an explorer's chance of a retroactive ban after 30 techniques? After 100?
2. Under warn first with `r = 0.01`, what is the ban risk for `N = 10`? Compare with the retroactive risk for the same `N`.
3. A studio's data shows that players in the top 5% by hours played receive 40% of exploit bans. Using this lecture's model, give two explanations: one that means the policy is fine and one that means it is not. What would you check to tell them apart?
4. Pick article 18 (privacy). Write it as a checkable commitment that still lets a week 7 review pipeline read chat logs. State the collision you accepted.

<details>
<summary>Answers</summary>

1. `1 − 0.98^30 = 1 − 0.545 = 45.5%`. `1 − 0.98^100 = 1 − 0.133 = 86.7%`.
2. Warn first: `1 − 0.99^10 − 10 × 0.01 × 0.99^9 = 1 − 0.9044 − 0.0914 = 0.0043`, about 0.43%. Retroactive: `1 − 0.904 = 9.6%`. The ladder cuts the risk by a factor of about 22 at this `N`.
3. Fine: high-hour players try more techniques and, as a group, include more bad-faith exploiters, who knowingly use obvious exploits. Not fine: the bans are for ambiguous techniques used before any notice, which the model predicts would land on the most active good-faith players. Check the ban records: what share were for techniques on the declared list at the time of use, or in an "obvious" category, versus techniques declared only afterwards.
4. One possible answer: "We read a player's chat logs only for the matches named in a report from another player, only the reviewer assigned to the case sees them, and we publish every quarter how many logs were read." The collision: a report is enough cause, so a malicious reporter can trigger a reading. Week 7's reporter weighting limits this but does not remove it.

</details>

## Lab / assignment hook

[Lab 08, a player charter](../labs/lab08.md). You write a one-page charter of commitments for a fictional MMO, derived from Koster's articles, with a measurable target for each, a named collision, and an exploit policy tested in the week's interactive. It feeds the final governance design paper.

## Sources

- Koster, R. (2000, 27 August). "Declaring the Rights of Players." raphkoster.com. The 19 articles; modelled on the 1789 French Declaration and the US Bill of Rights; Koster's description of the document as hypothetical and full of traps; admins' ultimate control of the world; the business case for adopting its principles. Articles paraphrased.
- Balkin, J. M. (2004). "Virtual Liberty: Freedom to Design and Freedom to Play in Virtual Worlds." *Virginia Law Review* 90(8), 2043. Citation confirmed via Crossref.
- Lastowka, F. G. & Hunter, D. (2004). "The Laws of the Virtual Worlds." *California Law Review* 92(1), 1. Citation confirmed via Crossref.
- Wikipedia, "Combo (video games)" (accessed September 2026). Noritaka Funamizu noticing extra hits during a bug check on a Street Fighter II bonus stage, and keeping them as a hidden feature.
- Warcraft Wiki, "Exploit" (accessed September 2026). Blizzard's definition of an exploit as play clearly not intended by the developer to gain an advantage, and the warning of temporary or permanent suspension.
- CCP Games, EVE Online Support, "Known & Declared Exploits" (policy page, updated 9 September 2026). Public exploit notifications still in effect, including delaying CONCORD's response and farming loyalty points by destroying one's own characters; the statement that the list is not exhaustive; the exploit ticket category; publishing abuse steps treated as publishing an exploit.
- RuneScape Wiki, "Falador Massacre" (accessed September 2026). 6 June 2006, World 111; the player-owned house bug; moderators' messages; player combat disabled until morning; permanent bans for players who killed many; no rollback and no compensation.
- Wikipedia, "Eve Online" (accessed September 2026). The t20 incident exposed on 9 February 2007 (six blueprints to his corporation); CCP's internal affairs division; t20 remaining a developer until late 2008; Kugutsumen's permanent ban for revealing the developer's real name; the Council of Stellar Management from March 2008.
- Council of Europe, European Convention on Human Rights, Article 7 ("No punishment without law"). United States Constitution, Article I, Sections 9 and 10 (ex post facto clauses).
- The values of `q`, `d`, `n` and the 2% explorer share in section 3 are invented for teaching.

## Interactive spec: examples/w08-retroactive-risk.html

**Purpose.** Show that a tiny per-action risk of retroactive punishment becomes a large career risk for players who try many novel techniques, and that policy choice decides who carries it.

**The one insight the visual must make obvious.** The same 1% per-technique risk that looks harmless in the left view becomes a 78% three-year ban risk for the explorer in the right view under a retroactive policy, and drops to zero under notice-first.

**Layout.** Two linked views side by side on desktop, stacked on mobile, plus a server panel below.

- **Left view: "One technique."** A single vertical bar showing `r = q × d` on a 0 to 100% scale, labelled with its value. Deliberately small. Caption: "Risk that one technique gets you banned later."
- **Right view: "A career."** x axis: techniques tried `N` from 0 to 300. y axis: ban probability 0 to 100%. Three curves: Retroactive, Warn first, Notice first (flat at 0). The selected policy's curve is bold, the others faint. Two markers on the selected curve: the casual player at `N = n_casual × Y` and the explorer at `N = n_explorer × Y`, each labelled with its exact percentage.
- **Server panel: "Who gets banned."** For a population `M`, show a two-segment bar of expected bans (explorers vs casuals) under the selected policy, with counts and the explorers' share of bans printed, plus the explorers' share of the population for comparison.

**Controls.**
- `q`, slider 0.005 to 0.10, step 0.005, default 0.02.
- `d`, slider 0.1 to 1.0, step 0.05, default 0.5.
- `n_casual`, slider 0 to 20, default 2.
- `n_explorer`, slider 10 to 100, default 50.
- `Y` years, slider 1 to 10, default 1.
- Explorer share `e` of the population, slider 0.5% to 20%, step 0.5%, default 2%.
- Population `M`, fixed at 100,000 (display only).
- Policy, segmented control: Retroactive (default), Warn first, Notice first.

**Formulas.**
```
r = q × d
N = n × Y
retro(N) = 1 − (1 − r)^N
warn(N)  = 1 − (1 − r)^N − N × r × (1 − r)^(N − 1)
notice(N) = 0
explorerBans = M × e × P(N_explorer)
casualBans   = M × (1 − e) × P(N_casual)
explorerShare = explorerBans / (explorerBans + casualBans)   (show "n/a" if both are 0)
```

**Test values (defaults unless stated; page must reproduce, rounded).**
- `r = 0.01`.
- `Y = 1`: casual retro 1.99%, explorer retro 39.5%, explorer warn 8.9%.
- `Y = 3`: casual retro 5.85%, casual warn 0.15%, explorer retro 77.9%, explorer warn 44.3%.
- Server, `Y = 1`, Retroactive: explorers ≈ 790, casuals ≈ 1,950, explorers' share 29%.
- Server, `Y = 1`, Warn first: explorers ≈ 179, casuals ≈ 10, explorers' share 95%.
- `q = 0.04`, `d = 0.5`, `N = 30` (set `n_explorer = 30`, `Y = 1`): retro 45.5%.

**Accessibility and style.** Use `templates/interactive-tokens.css` inline. Keyboard-operable controls with visible labels and live readouts. Curves distinguishable by line style (solid, dashed, dotted) as well as colour. Respect `prefers-reduced-motion`. No game art or logos; players are drawn as generic dots.
