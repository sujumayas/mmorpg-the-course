# MMO402 · Week 01 — Worlds as Polities

**Why this matters:** The moment thousands of people share a persistent world, you are running a small state. You write its laws in code and in a terms-of-service document, you enforce them with game masters, and you change them every patch. Your players will respond to those changes the way citizens respond to governments, and if you do not plan for that, you find out from a churn graph that drops off a cliff.

**You will be able to:**
- Classify the rules of an online world by Lessig's four modalities (code, law, norms, market) and name who controls each.
- Compute a dissatisfied player's choice between staying silent, speaking up and leaving, using a simple exit-voice model.
- Explain, with the model's numbers, why high switching costs hide discontent until it collapses into a mass exit.
- Critique a studio's voice channels (forums, councils, surveys) by estimating how responsive they are and what that does to exit.

**Before class:** Koster, "Declaring the Rights of Players" (2000, raphkoster.com), the whole essay, about 30 minutes. Hirschman, *Exit, Voice, and Loyalty* (1970), chapters 1-3. Lessig, *Code: Version 2.0* (2006), chapter 7, "What Things Regulate." Mnookin, "Virtual(ly) Law: The Emergence of Law in LambdaMOO" (1996), sections on the "New Direction" and the petition system.

**Prerequisites from earlier courses:** [MMO301 week 1, what is a virtual world](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w01-what-is-a-virtual-world-bartles-definition.md) (persistence and the shared world). [MMO301 week 11, Koster's Laws](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w11-kosters-laws-of-online-world-design.md) (why "someone will" misuse every system). [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) (where LambdaMOO comes from). [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) (the cascade in section 3 is one). [MMO305 week 1, MMOs as societies](../../MMO305-social-systems-and-online-behaviour/lectures/w01-mmos-as-societies-social-capital.md) and [MMO305 week 4, guilds](../../MMO305-social-systems-and-online-behaviour/lectures/w04-guilds-formation-lifecycle-leadership.md) (social capital and guild life, which make up most of a player's switching cost).

**Interactive:** [w01-exit-or-voice.html](../examples/w01-exit-or-voice.html)

---

## 1. Why call a game world a polity?

A **polity** is any organized community with a government: a set of people, a territory, rules, and someone with the power to make and enforce those rules. The word covers nation states, city councils and medieval guilds. This course argues that it also covers an MMO shard, and that treating it as one gives you better design decisions.

Check the four parts against a live MMO.

- **People.** A shard has a population that persists from day to day and knows itself. Players recognize names, keep grudges and remember history.
- **Territory.** The world is a bounded space that exists whether or not any one player is logged in. MMO301 week 1 called this persistence.
- **Rules.** Some rules are in the code (you cannot attack in a safe zone), some are in the terms of service (you may not sell gold for money), and some are unwritten (you do not ninja-loot in a pickup group).
- **A sovereign.** Someone can change the rules and punish the people who break them. In every commercial MMO that someone is the developer.

That last point is the one players forget and designers must not. Raph Koster, a designer of early graphical MMOs, put it bluntly in his 2000 essay "Declaring the Rights of Players." The people who run a world control its hardware, software and data, and can shut the whole community down at will. Players live in the world at the operator's discretion, even though their investment in it is real. Koster did not argue that players have legal rights. He argued that operators should write down the principles they follow anyway, so that both sides can judge whether the world is being run fairly. You will read the full essay again in week 8.

So you are a sovereign. The rest of this course asks what kind.

### Four things that regulate a world

Lawrence Lessig's *Code and Other Laws of Cyberspace* (1999, revised as *Code: Version 2.0* in 2006) gives the most useful map. Lessig says four forces constrain what anyone does, online or off:

- **Law.** Written rules backed by punishment. In a game, these are the terms of service, the end-user license agreement (EULA) and the published code of conduct, enforced by bans and suspensions.
- **Norms.** Unwritten expectations enforced by other people: reputation, shaming, guild membership, being blacklisted from raids.
- **Market.** Prices and scarcity. An expensive action happens less. In a game, the developer sets many of these prices directly (repair costs, travel fees, market taxes).
- **Architecture.** What the environment physically allows. Lessig's famous slogan is "code is law": software can make an action impossible instead of forbidden.

The four modalities differ in who controls them and how they fail. Here is one behavior, killing other players in a starting zone, regulated each way.

| Modality | How it stops starting-zone player killing | Who controls it | How it fails |
|---|---|---|---|
| Architecture | The server refuses the attack in newbie areas | Developer, fully | Players find the edge of the zone, or lure targets out of it |
| Law | The code of conduct bans "harassment of new players" | Developer writes, game masters enforce | Enforcement is slow, costly and needs reports |
| Norms | Guilds shame and expel members who gank newbies | Players | Only works where the killer cares about a group |
| Market | Killing a newbie costs you reputation that raises your prices in town | Developer sets the price, players choose | Rich players pay the price and keep doing it |

The developer controls architecture and market completely, writes the law, and can only influence norms. That asymmetry is why this course separates the developer's government (weeks 5 to 7) from the players' own government (weeks 2 to 4).

### A short history of handing power to players

Worlds have tried more than one kind of sovereign. The best documented experiment is LambdaMOO, a text-based world run from Xerox PARC by Pavel Curtis from 1990.

In December 1992 (Mnookin, writing in 1996, places Curtis's memo in early 1993), Curtis announced that the "wizards" (the administrators) would stop making social decisions and act only as technicians. Discipline and dispute resolution would pass to the community. In March 1993 the community faced its first crisis under the new policy, when a player called Mr. Bungle used a programming trick to force other players' characters into sexual acts in a public room. Julian Dibbell's account, "A Rape in Cyberspace," appeared in *The Village Voice* on 21 December 1993. One wizard then removed Mr. Bungle's account on his own judgment. Curtis then introduced a formal petition and ballot system, in place by the summer of 1993, so that the next decision would not depend on one person.

Jennifer Mnookin's 1996 study of LambdaMOO records the rules. A petition needed 10 signatures to go to the wizards for a technical check, then about 60 signatures (roughly 5% of the average number of votes cast on a ballot) to become a ballot. A ballot passed with a two-to-one margin after two weeks of voting. By 1996 the wizards had taken back the power to make social decisions, while keeping the ballot system as a channel for player input.

Notice what that history contains. A sovereign gave away power, discovered that decisions still had to be made, built a formal channel for players to speak, and then reclaimed some of the power it had given away. Every MMO governance debate since has replayed some part of that cycle. You will meet the ballot thresholds again in week 3, because they share a hidden weakness with elections for EVE Online's player council.

## 2. Worked example: exit or voice?

### The hook

In April 2016, Blizzard sent a cease-and-desist letter to Nostalrius, a fan-run private server that recreated World of Warcraft as it was before its first expansion. The server shut down on 10 April 2016. It had more than 800,000 registered accounts. A Change.org petition asking Blizzard to offer official "legacy" servers passed 280,000 signatures. Blizzard invited the Nostalrius team to its headquarters, and on 3 November 2017 it announced World of Warcraft Classic, which launched on 26 August 2019 (Americas time; 27 August in Europe).

Hundreds of thousands of players had left the official game for an unlicensed copy of its older self, then, when that copy closed, organized to change the developer's mind. They had tried two strategies, and the second one worked. Why did they not simply quit, or simply complain?

Now compare Star Wars Galaxies. In November 2005, Sony Online Entertainment released the "New Game Enhancements" (NGE), which rebuilt the game's professions and combat. The backlash was large. SOE offered refunds on the Trials of Obi-Wan expansion, which had gone on sale only days before the redesign was announced, and kept the NGE. The game closed on 15 December 2011.

Same situation: a developer changes the world, and a large group of players hate the change. Very different outcomes. You need a model that tells you which one you are heading for.

### The model

The economist Albert Hirschman, in *Exit, Voice, and Loyalty* (1970), described two responses to an organization in decline. **Exit** means leaving: a customer switches brands, a citizen emigrates, a player quits. **Voice** means staying and trying to change the organization from inside: complaining, petitioning, voting. Hirschman's central claim is that the two trade off. The easier exit is, the less anyone bothers with voice. **Loyalty**, attachment to the organization, raises the cost of leaving and so pushes people toward voice.

Turn that into numbers. A player has just seen a change they dislike. Measure everything in one unit, "value over the next year," with 0 meaning the world as it was before the change.

- `g` is the **grievance**: how much value the change takes away if it stays.
- `p` is **responsiveness**: the chance that speaking up gets the change reversed. It describes the developer, not the player.
- `c` is the **cost of voice**: time spent writing posts, signing petitions, attending a town hall.
- `A` is the value of the best **alternative**, relative to the old world. It is usually negative: another game, or a private server, is worse than the world you had.
- `S` is the player's **switching cost**: characters, gear and, above all, friends left behind. Hirschman's loyalty lives here.

The player has three options:

```
stay silent:  −g
voice:        −(1 − p) × g − c
exit:         A − S
```

Voice is better than silence when `p × g > c`, meaning the expected gain from speaking up beats its cost. The player exits when `A − S` beats the better of the two ways of staying. Call the gain from exiting before switching costs `R`:

```
R = A + min(g, (1 − p) × g + c)
exit if S < R
```

`R` combines everything except the individual's switching cost. It rises when the grievance grows, when the developer stops listening, and when alternatives improve.

### From one player to a server

A server holds many players with different switching costs. A new player has almost none. A guild officer with six years of history has a lot. Model the population with switching costs spread evenly from 0 up to some maximum `S_max`. Then the share of players who leave is

```
x = R / S_max        (clamped between 0 and 1)
```

Write `r = R / S_max` for short. Without anything else, the exit share is just `r`.

But switching cost is mostly social, and social ties depend on who else stays. If a share `x` of the server has left, your friends have left in roughly that share, and the social part of your switching cost shrinks with them. Make the simplest assumption, that everyone's switching cost scales by the share who remain, `S × (1 − x)`. Now a player exits when `S × (1 − x) < R`, and the exit share must satisfy

```
x = r / (1 − x)
```

Each departure lowers the cost of the next one. That is a positive feedback loop of the kind you met in GD102 week 3. Rearranged, `x(1 − x) = r`, a quadratic. The smaller root is the share that leaves:

```
x = (1 − √(1 − 4r)) / 2      if r ≤ 0.25
x = 1                        if r > 0.25   (everyone goes)
```

The quadratic has no real root when `r > 0.25`, which means there is no stable server population. Every departure triggers enough others that the process runs to the end.

### Numbers you can check

Fix the cost of voice at `c = 5`, the alternative at `A = −60` and the spread of switching costs at `S_max = 200`. Vary the grievance and the developer's responsiveness.

| Case | g | p | Best way to stay | R | r | Exit, no social ties | Exit, with social ties |
|---|---|---|---|---|---|---|---|
| Developer listens | 100 | 0.5 | voice, −55 | −5 | < 0 | 0% | 0% |
| Developer sometimes listens | 100 | 0.3 | voice, −75 | 15 | 0.075 | 7.5% | 8.2% |
| Developer rarely listens | 100 | 0.2 | voice, −85 | 25 | 0.125 | 12.5% | 14.6% |
| Developer ignores voice | 100 | 0 | silence, −100 | 40 | 0.20 | 20% | 27.6% |
| Grievance grows | 110 | 0 | silence, −110 | 50 | 0.25 | 25% | 50% |
| Grievance grows a little more | 112 | 0 | silence, −112 | 52 | 0.26 | 26% | 100% |

Check two rows by hand. With `p = 0.2`, voice is worth `−(0.8 × 100) − 5 = −85`, better than silence at −100. So `R = −60 + 85 = 25`, `r = 25/200 = 0.125`, and the coupled exit share is `(1 − √0.5)/2 = (1 − 0.7071)/2 = 0.146`. With `g = 110` and `p = 0`, voice is worth `−110 − 5 = −115`, worse than silence, so `R = −60 + 110 = 50` and `r = 0.25`. The formula gives `(1 − √0)/2 = 0.5`.

### The insight

Read down the last two columns. Without social ties, exit rises in a straight line with the grievance: 20%, 25%, 26%. With social ties, it creeps up (27.6%, then 50%) and then jumps from half the server to all of it when the grievance grows by 2 more points. The last few players who leave are the ones whose friends have already gone.

Two lessons follow for anyone running a world.

First, **responsiveness is the developer's biggest lever.** Moving `p` from 0 to 0.5 turned a 27.6% exodus into none at all, with the grievance unchanged. Players who believe they can change things stay and argue instead of leaving. That is the whole case for voice channels.

Second, **high switching costs hide discontent.** An MMO with years of character investment and dense friendships has a large `S_max`, so the first bad patch loses few players. Your churn dashboard looks fine. But the same social ties that keep people in are the ones that pull them out together once a threshold is crossed. When whole guilds leave at once, it is the model's `r > 0.25` region, not bad luck.

### The visual

Open the interactive. The left panel shows a single player's choice as a map: switching cost on the horizontal axis, grievance on the vertical, with regions shaded silence, voice and exit. The right panel shows the whole server: exit share against grievance, with one curve for no social ties and one with them. Drag the responsiveness slider from 0.5 down to 0 and watch the voice region on the left shrink while the cliff on the right slides toward smaller grievances. The single-player map changes smoothly. The server curve does not.

### Cross-game recognition

**World of Warcraft and Nostalrius (2016-2019).** The Nostalrius community had an unusually good alternative: `A` close to 0, because the private server was the old game itself. Its switching cost was low, because whole guilds moved together, which is the social-tie effect working in the developer's disfavor. When the server closed, `A` fell sharply and exit stopped being attractive. Players turned to voice, with 280,000 signatures and a meeting at Blizzard. Blizzard's announcement 19 months after the shutdown raised `p` in hindsight. The case also shows that exit and voice are not one-time choices. The same players used both, in sequence.

**Star Wars Galaxies and the NGE (2005).** SOE kept the redesign, so from the players' point of view `p` was near 0. The refund on a newly released expansion lowered the cost of leaving at the exact moment the grievance peaked. In the model's terms, the developer lowered `S` and `p` together, which moves a server toward the exit region from two sides.

**EVE Online and Incarna (2011).** In 2011, EVE Online players protested the Incarna expansion and the introduction of microtransactions. In October 2011 CCP announced it would lay off 20% of its staff worldwide, and said it had been a mistake to release Incarna in its state at the time. CCP shifted focus back to EVE. Week 3 looks at the institution EVE players already had for voice, the Council of Stellar Management, and asks how much `p` it actually buys.

**LambdaMOO petitions (1993 onward).** The petition system turned voice from forum complaints into a procedure with known thresholds. In model terms, it lowered `c`, because signing a petition was cheap, and made `p` visible, because a ballot with a two-to-one majority would be implemented. You cannot measure `p` directly for most games, but you can build institutions that make it predictable.

Outside games, Hirschman's own example is a public school that slowly declines. The parents who care most about quality leave for private schools. The school loses its most demanding critics, so it has less pressure to improve. That is the Nostalrius story told from the other side. When your most committed players leave for a private server, you lose your most informed voices along with their subscriptions.

### Eyes-open design judgment

The model is a sketch. Real grievances differ across players, voice is collective (one post changes nothing, 280,000 signatures might), and switching costs are not spread evenly. Use it for direction, not forecasts. Within those limits it supports several decisions you should make deliberately.

- **Build voice before you need it.** A forum where developers never reply has `p ≈ 0`. Players learn that fast, and the forum becomes a place to organize exit. Regular developer responses, public roadmaps, player councils and surveys all raise the perceived `p`. They cost staff time, and they create expectations you must meet.
- **Voice can be captured.** Formal voice channels favor the organized. A council elected by the most engaged 5% of players may represent them well and everyone else badly. Week 3 puts numbers on this.
- **Do not read low churn as consent.** In a world with high switching costs, a quiet server may be a trapped server. Look for signs of silent grievance: falling session length, fewer new characters, guilds merging.
- **Watch clusters, not individuals.** Because exit cascades through social ties, the early warning is a guild or friend group leaving together, not the overall percentage.
- **Lowering switching costs is not always wrong.** Character transfers, account-wide progress and cross-realm play make exit easier, which reduces voice. They also make players less trapped, which is fairer. That is a values choice, and you should make it on purpose.

## 3. The developer as sovereign

If the developer is the sovereign, what kind of government is a live MMO? Most are what political scientists would call an autocracy with consultation. One party makes every rule. It consults when it chooses, through forums, surveys, test servers and, occasionally, elected councils. There is no separation of powers. The team that writes the rules also enforces them and hears the appeals.

That sounds alarming, but it has reasons. A developer is responsible for the world's code, its servers and its legal obligations, and cannot hand those to players. The question is which constraints the developer accepts on itself. You can sort the options by how binding they are:

| Constraint | Example | How binding |
|---|---|---|
| Published principles | Koster's proposed "rights of players" (2000) | Voluntary. Breaking them costs reputation only |
| Terms of service | The EULA every player accepts | Binding on players, rarely on the developer (week 5) |
| Procedural rules | Published ban appeals process, response times | Binding in practice, because breaking them is visible (week 7) |
| Advisory institutions | EVE's Council of Stellar Management | Can speak, cannot decide (week 3) |
| Player-run institutions | Guilds, alliances, player courts | Decide inside the space the developer leaves open (week 2) |
| Outside law | Consumer protection, data protection, age rules | Binding on the developer (weeks 9 and 11) |

The design question is not "democracy or dictatorship." A world where players vote on balance changes would be unplayable. It is where to leave room for players to govern themselves, and what commitments to make about how you govern the rest.

### Legitimacy

A government is **legitimate** when the people it governs accept its right to rule, not only its power. Players accept a lot from developers: nerfs, wipes, bans, even shutdowns. They accept it more readily when three conditions hold, and you can use them as a checklist.

- **Predictable rules.** Players knew the rule before they were punished for breaking it.
- **Fair process.** Decisions follow a known procedure and can be appealed.
- **Voice that sometimes works.** Players can point to a case where they changed the developer's mind.

The Nostalrius case scores on the third point, eventually. The LambdaMOO petition system was an attempt to score on all three. Weeks 5 to 7 return to the first two.

### Nested government

Real MMO government has layers. The developer sets the outer rules. Inside them, players run guilds with ranks, dues and loot rules. Guilds form alliances with councils and treaties. In EVE Online, alliances form coalitions with tens of thousands of members. Each layer governs the one below within the room the layer above allows. Elinor Ostrom, who studied how communities manage shared resources such as fisheries and irrigation, called this pattern "nested enterprises" and found it in most long-lived self-governing systems. Week 2 uses her full list of design principles to ask why some player governments last and others collapse.

## In-class activity (25 minutes)

In groups of three, pick an MMO at least one of you has played for more than 50 hours.

1. List five rules that shape how players treat each other. Put each in one of Lessig's four modalities and name who controls it (8 minutes).
2. List every channel through which players can influence the developer. For each, estimate `p` for a moderately popular request on a scale of 0 to 1, and write one sentence of evidence (8 minutes).
3. Estimate the switching cost structure. What makes a veteran player's `S` high? Is it mostly items, mostly progress or mostly people? (4 minutes)
4. Put your estimates into the interactive. Report the grievance level at which your game's server would tip into a cascade, and name the one change the developer could make that would move that point furthest (5 minutes).

Expected output: a filled four-modality table, a list of voice channels with `p` estimates, and one recommendation with the interactive's numbers.

## Common misconceptions

- **"Players who don't complain are happy."** In a high-switching-cost world, silence is often the best of three bad options. The model's silent players have the same grievance as the ones who post.
- **"Voice and exit are opposites, so a game with lots of complaints is in trouble."** A lot of voice usually means players still believe `p > 0` and intend to stay. The dangerous server is the quiet one where `p` has fallen to zero.
- **"Code is law means the developer can prevent any behavior."** Architecture regulates only what the developer anticipated. Players route around it, and norms and law cover the rest. MMO301 week 11's "someone will" applies.
- **"Handing governance to players is more ethical."** LambdaMOO's wizards handed social decisions over and later took them back. Giving players a vote without the tools to enforce the result, or on questions they cannot judge, produces frustration instead of legitimacy.

## Check yourself

1. With `A = −60`, `c = 5` and `S_max = 200`, the developer raises responsiveness to `p = 0.4` while the grievance stays at `g = 100`. What share of the server leaves with social ties? Without them?
2. A player has `g = 60`, `p = 0.05` and `c = 5`. Should they speak up or stay silent? Explain with the payoffs.
3. A studio adds free character transfers to a rival server it also owns, which roughly halves every player's switching cost. Using `r = R / S_max`, what happens to `r`? If `R = 30` and `S_max` was 200, does the server now tip into a cascade?
4. Classify each rule by Lessig's modality: (a) a 5% tax on auction house sales; (b) a guild rule that members must attend two raids a week; (c) a ban for using third-party automation software; (d) a wall that makes a city unreachable except by its gate.

<details>
<summary>Answers</summary>

1. Voice is worth `−(0.6 × 100) − 5 = −65`, better than silence. `R = −60 + 65 = 5`, `r = 0.025`. Without ties, 2.5% leave. With ties, `x = (1 − √0.9)/2 = (1 − 0.9487)/2 ≈ 2.6%`.
2. Voice gains `p × g = 0.05 × 60 = 3` in expectation and costs 5, so silence is better (−60 against −62). A rational player with those numbers says nothing, which is why a low-`p` developer hears less than it should.
3. Halving every switching cost doubles `r`, since `S_max` becomes 100. `r = 30/100 = 0.3`, which is above 0.25, so the model predicts a full cascade. Before the change, `r = 0.15` and about 18.4% would have left with social ties.
4. (a) Market. (b) Norms, enforced by the guild, though the guild's rank system may encode it in code. (c) Law, the terms of service, enforced by the developer. (d) Architecture.

</details>

## Lab / assignment hook

[Lab 01, governance audit](../labs/lab01.md). You audit one live MMO as a polity: map its rules by modality, list its voice channels with evidence for `p`, and estimate switching costs from observable features. The audit is the first of the course's case analyses.

## Sources

- Koster, R. (2000, 27 August). "Declaring the Rights of Players." raphkoster.com. Operators' control of hardware, software and data; the case for voluntary written principles.
- Lessig, L. (1999). *Code and Other Laws of Cyberspace*. Basic Books. Revised as *Code: Version 2.0* (2006). The four modalities of regulation and "code is law."
- Hirschman, A. O. (1970). *Exit, Voice, and Loyalty: Responses to Decline in Firms, Organizations, and States*. Harvard University Press. Exit, voice, loyalty; the declining-school example.
- Mnookin, J. L. (1996). "Virtual(ly) Law: The Emergence of Law in LambdaMOO." *Journal of Computer-Mediated Communication* 2(1). The "New Direction," petition thresholds (10 signatures, about 60 for a ballot), the two-to-one margin and two-week vote.
- Wikipedia, "LambdaMOO" and "A Rape in Cyberspace" (accessed September 2026). Curtis and Xerox PARC, the December 1992 "New Direction," the Mr. Bungle incident (March 1993), petitions and ballots from summer 1993, the 1993-1996 democratic period, Dibbell's article in *The Village Voice* of 21 December 1993, the wizards later reclaiming power while keeping ballots.
- Wikipedia, "Nostalrius" (accessed September 2026). Shutdown on 10 April 2016 after a cease-and-desist letter; over 800,000 registered accounts; petition over 280,000 signatures; Blizzard meeting; WoW Classic announced 3 November 2017. Wikipedia, "World of Warcraft Classic" (accessed September 2026): global release 26 August 2019.
- Wikipedia, "Star Wars Galaxies" (accessed September 2026). NGE in November 2005, refunds on *Trials of Obi-Wan*, closure on 15 December 2011.
- Wikipedia, "CCP Games" (accessed September 2026). October 2011 layoffs of 20% of staff after the Incarna and microtransactions controversy; CCP's statement that releasing Incarna at that stage was a mistake.
- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press. "Nested enterprises" as a design principle.

## Interactive spec: examples/w01-exit-or-voice.html

**The one insight.** A player's choice between silence, voice and exit changes smoothly as conditions change, but a server's exit share does not: once social ties are counted, exit creeps up and then jumps to 100% at `r = R / S_max = 0.25`. Responsiveness `p` moves that cliff more than anything else.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px (left panel first). A control strip above both. A numbers readout under the right panel.

**Controls (all sliders, keyboard operable, with numeric readouts).**
- Grievance `g`: 0 to 200, step 1, default 100.
- Responsiveness `p`: 0 to 1, step 0.01, default 0.2.
- Cost of voice `c`: 0 to 30, step 1, default 5.
- Alternative `A`: −150 to 50, step 1, default −60.
- Max switching cost `S_max`: 20 to 400, step 10, default 200.
- Toggle "social ties" (on by default) that shows or hides the coupled curve.
- Preset buttons for the six rows of the lecture's table (set `g` and `p`, reset `c = 5`, `A = −60`, `S_max = 200`).

**Formulas.**
- `silence = −g`; `voice = −(1 − p) × g − c`; `stay = max(silence, voice)`.
- `R = A − stay`; `r = R / S_max`.
- Uncoupled exit share: `clamp(r, 0, 1)`.
- Coupled exit share: `0` if `r ≤ 0`; `(1 − sqrt(1 − 4r)) / 2` if `0 < r ≤ 0.25`; `1` if `r > 0.25`. Also compute it by iterating `x ← min(1, r / (1 − x))` from `x = 0` for 200 steps (stop when `x ≥ 0.999`) and assert the two agree within 0.001 when `r ≤ 0.249`.

**Left panel, one player's choice.** Horizontal axis switching cost `S` from 0 to `S_max`; vertical axis grievance from 0 to 200. Shade each cell by the best option: exit if `A − S > stay(g)`, else voice if `voice > silence`, else silence. Three colors from the shared palette with a legend. Draw a horizontal line at the current `g`. The share of that line lying in the exit region equals the uncoupled exit share; label it.

**Right panel, the server.** Horizontal axis grievance 0 to 200; vertical axis exit share 0% to 100%. Plot the uncoupled curve (dashed) and the coupled curve (solid). Mark the current `g` with a vertical line and dots on both curves. Draw the cliff as a vertical jump in the coupled curve and label the grievance where `r = 0.25`, computed as the smallest `g` where `R ≥ 0.25 × S_max`.

**Readout.** Show `stay` option chosen (silence or voice) and its value, `R`, `r`, uncoupled share, coupled share, and "cliff at g = …".

**Test values (the builder must check these).**
- `g = 100, p = 0.2, c = 5, A = −60, S_max = 200`: stay = voice at −85, `R = 25`, `r = 0.125`, uncoupled 12.5%, coupled 14.6%.
- `g = 100, p = 0`: stay = silence at −100, `R = 40`, `r = 0.2`, coupled 27.6%.
- `g = 110, p = 0`: `r = 0.25`, coupled 50%. `g = 112, p = 0`: `r = 0.26`, coupled 100%.
- `g = 100, p = 0.5`: `R = −5`, both shares 0%.
- With `p = 0`, `A = −60`, `S_max = 200`, the cliff is at `g = 110`.

**Accessibility and style.** Follow `templates/interactive-tokens.css`. Region colors must also differ in pattern or have text labels so the map reads without color. Respect reduced motion (no animated transitions when set). No game logos or art.
