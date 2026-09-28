# MMO402 · Week 14 — Debates

**Why this matters:** Most arguments about running a world go in circles because the two sides disagree about different things. One side is arguing about facts, the other about priorities, and neither notices. A designer who can find the exact point where a decision flips, and say whether that point is a fact or a value, ends the circle. This week gives you a tool for finding that point, a structure for arguments, and the format for this week's graded debates.

**You will be able to:**
- Compute the crux weight at which two design options tie in a weighted-criteria model, and the crux score that would flip the decision.
- Classify a disagreement as a dispute of fact or a dispute of value by locating both sides on a decision map.
- Build an argument in Toulmin's six parts and state the strongest version of the opposing case before rebutting it.
- Critique a player poll as evidence by naming who could vote, who could not, and what the result measures.

**Before class:** Toulmin, *The Uses of Argument* (1958, updated edition 2003), chapter 3, "The Layout of Arguments." Reread MMO304 week 11, section 4, on RuneScape's trade limit. Bring your lab 13 memo, which is evidence for one of this week's motions.

**Prerequisites from earlier courses:** [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (the RuneScape trade limit and the Diablo III auction house, which this week treats as debates). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (a weighted sum is the same arithmetic as an expected value). [MMO303 week 10, payoff matrices](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (scoring options against each other). In this course, [week 1, worlds as polities](w01-worlds-as-polities.md) (legitimacy and voice) and [week 13, shutdown ethics](w13-shutdown-ethics.md) (the player-loss weight `k`). The debate motions draw on weeks 3, 4, 6, 7, 11 and 12.

**Interactive:** [Crux map: fact gap or value gap](../examples/w14-crux-map.html). Keep it open during section 2.

---

## 1. What a design debate is for

In a debate club the goal is to win. In a studio the goal is to make the right call and to make it in a way the losing side can accept. Those goals overlap more than you might expect. The debater who wins a studio argument is usually the one who found what the disagreement was actually about and moved it there.

Every argument you have had this semester has had the same shape. Two options are on the table: restrict trade or keep it free, punish the scammer or let the scam stand, close the world with three months' notice or six. Each option is better on some criteria and worse on others. People disagree for two different reasons.

- **A dispute of fact.** They agree on what matters but disagree about what an option would do. "Trade limits cut gold farming by half" against "trade limits barely touched it."
- **A dispute of value.** They agree on what an option would do but weigh the outcomes differently. "Stopping fraud matters more than free trade" against "free trade is the point of the game."

The two kinds of dispute need different moves. A dispute of fact is settled by evidence: telemetry, a test, a comparable case. A dispute of value is settled by argument about priorities, by appeal to principles the other side already holds, or by a procedure that everyone accepts, such as a vote. Bringing a chart to a value dispute wastes it. Bringing a principle to a fact dispute sounds like stubbornness.

The worked example gives you a way to tell which kind you are in, using numbers.

## 2. Worked example: finding the crux

### The hook

On 10 December 2007, Jagex changed RuneScape to fight real-world trading. It limited how unbalanced a trade between players could be, and removed free player-versus-player combat from the Wilderness, the lawless zone where one player could take another's items by killing them. MMO304 week 11 covered the economics. Wikipedia's RuneScape article reports that subscriptions fell by 60,000 during the changes, and notes that nobody published how many of those were gold farmers' accounts rather than players'. Players complained for three years.

From 24 December 2010 to 14 January 2011, Jagex ran a referendum on bringing both back. 1,234,658 votes were cast, and 91% said yes. Free trade and the old Wilderness returned on 1 February 2011.

Now the puzzle. Does the 91% prove that the 2007 decision was wrong? The people who defended it had a real argument. Gold farming funds account theft and bots, and bots make a world worse for everyone. The people who attacked it also had a real argument. Trade and risk were what made RuneScape feel like a world. Both sides were right about something. If you had been in the room in 2007, what exactly would you have needed to know to decide?

### The model

Put the choice into a **weighted-criteria model**, the simplest tool decision analysts use. List the options. List the criteria that matter. Score each option on each criterion from 0 to 10, where higher is always better. Give each criterion a weight, with the weights adding to 1. An option's value is its weighted score.

For the first pass, use two options and two criteria.

- Option **R**, restrict trade. Option **F**, keep trade free.
- Criterion **h**, harm prevented: less fraud, fewer bots, less account theft.
- Criterion **f**, freedom and fun: trade, risk, the feeling of a world.
- `w` is the weight on harm prevented. The weight on freedom is then `1 − w`.

```
U(option) = w × h(option) + (1 − w) × f(option)
D(w) = U(R) − U(F) = w × Δh + (1 − w) × Δf
```

Here `Δh = h(R) − h(F)` is how much better restriction is at preventing harm, a positive number. `Δf = f(R) − f(F)` is how much worse it is for freedom, a negative number. `D` is the gap. When `D > 0`, restriction wins. Setting `D = 0` gives the **crux weight**, the weight at which the options tie:

```
w* = −Δf / (Δh − Δf)
```

Anyone who puts more weight than `w*` on harm prevention should choose restriction. Anyone below it should choose free trade. That single number is where the debate actually lives.

### Numbers you can check

Suppose a debater scores the options like this. These are one person's judgments for teaching, not measurements. Restriction gets `h(R) = 8` and `f(R) = 3`. Free trade gets `h(F) = 4` and `f(F) = 9`. So `Δh = 4`, `Δf = −6`, and

```
w* = 6 / (4 + 6) = 0.6
U(R) = 3 + 5w        U(F) = 9 − 5w
```

| Weight on harm, w | U(R), restrict | U(F), free | Winner |
|---|---|---|---|
| 0.3 | 4.5 | 7.5 | Free |
| 0.5 | 5.5 | 6.5 | Free |
| 0.6 | 6.0 | 6.0 | Tie (the crux) |
| 0.7 | 6.5 | 5.5 | Restrict |
| 0.9 | 7.5 | 4.5 | Restrict |

Check the 0.7 row. `U(R) = 0.7 × 8 + 0.3 × 3 = 5.6 + 0.9 = 6.5`. `U(F) = 0.7 × 4 + 0.3 × 9 = 2.8 + 2.7 = 5.5`.

Now add the fact question. Nobody knew in 2007 how much harm the restriction would actually prevent. Treat `h(R)` as uncertain and keep the other scores fixed. The crux weight becomes a function of that fact:

```
w*(h_R) = 6 / (h_R + 2)
```

| Harm score for restriction, h(R) | Crux weight w* | Reading |
|---|---|---|
| 5 | 0.857 | Only someone who cares almost only about harm restricts |
| 6 | 0.75 | |
| 8 | 0.6 | The first table |
| 9 | 0.545 | |
| 10 | 0.5 | Restriction wins for anyone who weighs harm at least equally |

### The decision map

Put the two unknowns on two axes. The horizontal axis is the value question, the weight `w`. The vertical axis is the fact question, the score `h(R)`. The curve `w = 6 / (h_R + 2)` divides the plane. Above and to the right, restriction wins. Below and to the left, free trade wins.

Now place three debaters on the map.

| Debater | Weight w | Believes h(R) | U(R) | U(F) | Chooses |
|---|---|---|---|---|---|
| Ana | 0.7 | 8 | 6.5 | 5.5 | Restrict |
| Ben | 0.7 | 5 | 4.4 | 5.5 | Free |
| Cara | 0.4 | 8 | 5.0 | 7.0 | Free |

Ana and Ben share values. They weigh harm the same. They disagree about a fact, how well trade limits work. Ana and Cara share the facts and disagree about values. The map tells Ana what to do in each argument. Against Ben she should bring evidence: bot reports, gold prices, account-theft tickets before and after December 2007. Against Cara, evidence is useless, because Cara already accepts Ana's facts. Ana has to argue that harm matters more than Cara thinks, or find a principle Cara holds that implies it.

That is the insight of the model. **Before you argue, find out which axis separates you from your opponent. The direction of the gap tells you whether to bring evidence or argue about priorities.**

### The visual

Open the interactive. The left panel is the decision map, shaded by winner, with the crux curve drawn and three draggable debaters. The right panel shows the two value bars for the selected debater and the line `D(w)` crossing zero at `w*`. Drag Ben straight up. His bars swap when he crosses the curve, though his weight never changed. Drag Cara straight right and the same thing happens along the other axis. Then change the fixed scores with the sliders and watch the whole curve move. The panels show the same thing two ways. The bars show who wins. The map shows why.

### Cross-game recognition

Every debate this semester has the same shape: two options, criteria that pull in opposite directions, a crux weight and a fact that moves it. Rewriting a case into this form is the skill.

**RuneScape's referendum (2010-2011) as a measurement of weights.** The 91% vote did not measure `h(R)`. Voters could not observe how many bots the trade limit had stopped. It measured players' weights, and only for the players who were still there to vote. Players who had quit over the restriction could not vote, and neither could players who would later lose accounts to thieves. The referendum gave the free-trade side a strong answer on the value axis for the voting population. It said little about the fact axis. Jagex presented the return alongside its work against bots and account theft. In map terms, that is an attempt to raise `h(F)` so that free trade would win on both axes.

**Diablo III's real-money auction house (2012-2014).** Blizzard opened a real-money auction house in June 2012. The criteria were a safe, sanctioned route for real-money trade against the pleasure of finding your own loot. MMO304 week 11 modelled the second criterion. In March 2013 the game's director, Jay Wilson, said the feature had "really hurt" the game. Blizzard announced its closure on 17 September 2013 and shut it on 18 March 2014. In map terms, a fact moved. Once the studio believed the loot-hunt harm was large, the crux weight fell below almost anyone's weight on the fun of loot, and the decision flipped. Wilson later said the long delay came from legal work, because the feature had been advertised on retail packaging. That is a third criterion, keeping promises to buyers, which the week 13 lecture would recognise.

**Shutdown notice (week 13).** The best notice period `N* = L × (1 − C / (k × s))` is a crux in continuous form. The weight `k` on player losses is the value axis. The useful life `L` that buyers expected is the fact axis, or, if the store copy was vague, a second value question about what buyers were entitled to expect. Two studio executives who disagree about notice periods can locate each other on exactly this kind of map.

**Old School RuneScape polls (current).** Old School RuneScape still lets players vote on content. The wiki lists the pass mark as a 70% supermajority, with votes limited to members who have at least 300 total level and 25 hours of play. A supermajority is a rule that tilts the map toward the status quo. A change must win clearly, not narrowly. The eligibility rules decide whose weights are counted. Both are design decisions about the value axis, made once so they do not have to be argued each time.

**EVE Online and the Bank of EVE case.** The course's signature case study ([week 4](w04-wars-betrayals-and-meta-gaming.md) and [week 9](w09-virtual-property-and-law.md)) asks whether in-world fraud is allowed play. The criteria are freedom to betray against protection from loss. The fact axis is whether scams drive away the new players a world needs. Map both sides before you argue.

Outside games, cost-benefit analysis in public policy uses the same structure, and its best practice is the same. Report the answer together with the threshold values at which it would change, so decision makers can see which assumptions carry the result.

### Eyes-open design judgment

The weighted-criteria model is a diagnostic, not a verdict. Use it to find the crux, then argue about the crux in plain words.

- **The criteria list decides a lot.** Add a criterion on which your option scores well and your option gains. In a debate, check which criteria the other side left out, and say so.
- **Weights hide who bears the cost.** A single weight on "harm" treats a scam victim's loss and a bot's effect on prices as one thing. Distribution matters. A policy that is good on average and ruinous for a few players may still be wrong. Week 13's player-loss weight `k` is one way to put this back in.
- **Some options are off the table whatever they score.** Protecting minors (week 11) and obeying the law are constraints, not criteria. Do not let a high score on fun outweigh them. Name constraints before you score.
- **Scores feel more precise than they are.** An 8 against a 5 is one person's judgment. That is why the map is more useful than the table. It shows how far a score must move before the answer changes, and whether that distance is plausible.
- **A tie is information.** When debaters sit close to the curve, the options are genuinely close. The right move may be a hybrid (RuneScape later kept a smaller limit for new free accounts), a test on one server, or a decision that is easy to reverse.

## 3. Building an argument

The crux tells you where to argue. Stephen Toulmin's model tells you how to build each argument so that it can be checked. Toulmin, a philosopher, noticed in 1958 that real arguments rarely look like textbook syllogisms. They have six parts.

- **Claim.** What you want the audience to accept.
- **Grounds.** The evidence you offer for it.
- **Warrant.** The general rule that connects the grounds to the claim. It is often left unsaid, and it is often where arguments fail.
- **Backing.** The support for the warrant.
- **Qualifier.** How strongly you make the claim ("in most cases," "for this game").
- **Rebuttal.** The conditions under which the claim would not hold.

Here is one side of the 2007 decision laid out this way.

| Part | Restrict-trade side |
|---|---|
| Claim | Jagex was right to limit unbalanced trades in December 2007 |
| Grounds | Real-world trading moved gold through unbalanced trades and the Wilderness, and it funded account theft and botting |
| Warrant | If a mechanic is the main channel for a harmful activity, closing the channel reduces the activity |
| Backing | Gold sellers need a way to deliver gold. With no delivery channel, they have nothing to sell |
| Qualifier | At least until better detection tools existed |
| Rebuttal | Unless sellers found other channels, or the restriction drove away more honest players than it protected |

Laid out like this, you can see where the other side should attack. The warrant is a claim of fact, how well closing a channel works. The rebuttal already names the two routes: substitution and cost to honest players. A good opponent does not attack the grounds, which are largely true. They attack the warrant, which is where the fact axis of the map lives.

### Steelman before you rebut

A **steelman** is the strongest version of your opponent's case, the opposite of a straw man. Before rebutting, state the other side's position so well that they would accept your statement of it. Then name what you agree with. Only then rebut.

This is not politeness. It has three practical effects. It forces you to find the crux, because you cannot state the strongest version without knowing what it rests on. It stops you wasting time on points nobody holds. And it makes the audience trust you, which matters in the graded debate, where the audience votes.

### Burden and status quo

In most debates, the side proposing a change carries the **burden of proof**. It must show the change is better, not merely that the status quo has problems. Old School RuneScape's 70% pass mark writes that burden into a rule. In the decision model, the burden is a margin. The proposing side must show `D` above some positive threshold, not just above zero. Say at the start of a debate what the burden is. Arguments about who has to prove what are otherwise easy to lose track of.

## 4. Weighing evidence

Four kinds of evidence will appear in your debates. Each answers a different axis of the map, and each has a typical flaw.

| Evidence | Answers | Typical flaw | Question to ask |
|---|---|---|---|
| Telemetry (logs, economic reports, ticket counts) | Facts | Measures what was logged, not what mattered | What would this number look like if the other side were right? |
| Polls and referendums | Values, of those who voted | Self-selection; excludes those who left and those not yet harmed | Who could vote, and who could not? |
| Developer statements | Facts about intent and internal data | Written for an audience; data rarely shown | What would the studio gain by saying this? |
| Comparable cases from other games | Facts, by analogy | The other game differs in ways that matter | Which terms of the model are the same, and which differ? |

A poll result is the evidence debaters misuse most. "91% of players voted for free trade" is strong evidence about what the voters valued. It is weak evidence about the effect of trade limits on bots. It says nothing about the players who left in 2008. Week 3 made the same point about council elections, where turnout decides whose weights are counted. When an opponent cites a poll, ask which axis they think it answers.

## 5. The debates

This week's second session is the course debate, worth 20% of your final mark (see the Assessment section of the [syllabus](../syllabus.md)).

### Format

Each debate is Oxford-style: one motion, a proposition team and an opposition team of three students each, and an audience vote before and after.

| Stage | Time | Who |
|---|---|---|
| Audience vote on the motion | 2 min | Audience |
| Opening speeches | 5 min each | Proposition 1, then Opposition 1 |
| Cross-examination | 3 min each | Opposition questions Proposition 1, then the reverse |
| Second speeches | 5 min each | Proposition 2, then Opposition 2 |
| Floor questions | 8 min | Audience to either team |
| Closing speeches | 3 min each | Opposition 3, then Proposition 3 |
| Audience vote again | 2 min | Audience |

Sides are assigned by coin toss 48 hours before the debate. You will prepare both sides, which is the point. The first opening speech must state the crux as the speaker's team sees it. The first opposition speech must say whether it accepts that crux or relocates it.

### Motions

Each motion draws on earlier weeks. Your tutor assigns one per team.

1. This house believes that in-world fraud that breaks no rule of the game should never be punished by the operator (week 4 and the Bank of EVE case).
2. This house would require every online game to publish a sunset charter at launch (week 13).
3. This house believes an elected player council should have a binding veto over major design changes (week 3).
4. This house would stop all premium-currency sales to accounts registered as under 18 (week 11).
5. This house believes researchers may study public in-game chat without asking the players (week 12).
6. This house believes no ban should be issued by an automated system without human review (weeks 6 and 7).

### How you are marked

The audience vote decides the "winner" for the day. It does not decide your grade. You are marked on four things, each with equal weight: identifying and stating the crux; quality of evidence and its fit to the axis it answers; a fair steelman of the other side; and rebuttal that engages the other side's strongest point rather than its weakest. A team that loses the vote with a clear crux and a fair steelman can earn full marks.

## In-class activity (25 minutes)

Pairs, then groups of four. Use motion 2 (sunset charters) or motion 6 (automated bans).

1. (8 min) In pairs, list the two options, pick two or three criteria, and score both options. Compute the crux weight for your most important criterion. Use the interactive or the lab 14 script.
2. (5 min) Write one Toulmin argument for your side and circle its warrant.
3. (7 min) Join another pair that chose the other side of the same motion. Place all four of you on one decision map. For each pair of opponents, say whether you are separated by a fact or a value.
4. (5 min) Each person writes a two-sentence steelman of the other side. The other side marks it "accepted" or "not yet."

Expected output: a criteria table with scores and crux weight, one Toulmin argument, a map with four dots and each gap labelled "fact" or "value," and four steelmen with their marks.

## Common misconceptions

- **"A 91% vote settles the question."** It settles what the voters wanted. It does not tell you what the policy did, and it does not count people who could not vote. It answers the value axis for one population.
- **"If we just had more data, we'd agree."** Only if you disagree about facts. Ana and Cara share every fact and still disagree. More data will not move either of them.
- **"The weighted model is objective because it has numbers."** The criteria and scores are judgments. The model makes them visible and checkable, which is its value. It does not make them true.
- **"Steelmanning concedes the argument."** It concedes only what is true in the other side's case. That usually shrinks the debate to its crux, where your real argument is.

## Check yourself

1. Two options score `h(R) = 7, f(R) = 2` and `h(F) = 3, f(F) = 8`. Compute `w*`. Which option does someone with `w = 0.55` choose?
2. With the lecture's scores (`h(F) = 4`, `f(R) = 3`, `f(F) = 9`), a debater weighs harm at `w = 0.75`. What is the lowest `h(R)` at which they choose restriction?
3. Dev says, "Our logs show gold-seller spam fell 40% after the trade limit." Lee replies, "Freedom to trade is the whole point of an MMO." Which axis is each of them arguing on? Are they arguing with each other?
4. In the three-criterion example from lab 14 (weights 0.5, 0.4, 0.1; restrict scores 8, 3, 6; free scores 4, 9, 4), which option wins, and by how much? By how much would restriction's harm score have to rise to make a tie?
5. Write a Toulmin warrant for the claim "Blizzard was right to close the Diablo III real-money auction house," and name one rebuttal condition.

<details>
<summary>Answers</summary>

1. `Δh = 4`, `Δf = −6`, so `w* = 6/10 = 0.6`. At `w = 0.55`, `U(R) = 0.55 × 7 + 0.45 × 2 = 3.85 + 0.9 = 4.75` and `U(F) = 0.55 × 3 + 0.45 × 8 = 1.65 + 3.6 = 5.25`. Free trade wins. The crux matches the lecture's, because only the differences matter.
2. Set `w*(h_R) = 6 / (h_R + 2) = 0.75`, so `h_R + 2 = 8` and `h_R = 6`. At any score above 6 they restrict. At exactly 6 they are indifferent.
3. Dev argues on the fact axis, about what the limit did. Lee argues on the value axis, about what matters. They are not yet arguing with each other. Lee could accept Dev's 40% and still prefer free trade. The productive next step is for each to say whether they accept the other's point.
4. `U(R) = 0.5 × 8 + 0.4 × 3 + 0.1 × 6 = 5.8`. `U(F) = 0.5 × 4 + 0.4 × 9 + 0.1 × 4 = 6.0`. Free trade wins by 0.2. Restriction's harm score must rise by `0.2 / 0.5 = 0.4`, to 8.4.
5. One answer. Warrant: "A feature that makes the core reward loop pointless harms the game more than the revenue and safety it provides." Rebuttal condition: "unless removing it pushes real-money trade back to unsafe black markets and the resulting fraud outweighs the loss of fun." Both are claims a debater could test.

</details>

## Lab / assignment hook

[Lab 14, debate case file](../labs/lab14.md). Your team builds the case file for its assigned motion: a criteria table with a computed crux, a decision map placing both sides, three Toulmin arguments, a steelman of the other side, and an evidence log labelled by axis. You bring the case file to the debate and submit it with your team's mark.

## Sources

- Wikipedia, "RuneScape" (accessed September 2026). Updates of 10 December 2007 removing free player-versus-player combat in the Wilderness and restricting unbalanced trades to fight real-world trading; a reported fall of 60,000 subscriptions, with no split between players and gold farmers; restoration on 1 February 2011 after a referendum.
- RuneScape Wiki, "Referendum Vote" (accessed September 2026). Vote from 24 December 2010 to 14 January 2011; 1,234,658 votes; 91% yes; return on 1 February 2011; Jagex's stated link to measures against bots and account stealing.
- RuneScape Wiki, "Trade limit", as cited in MMO304 week 11. Announcement 10 December 2007, applied 2 January 2008, removed 1 February 2011, smaller limit kept for new accounts that have never paid for membership.
- Wikipedia, "Diablo III" (accessed September 2026). Real-money auction house opened June 2012; Jay Wilson's March 2013 remark that it had "really hurt" the game; closure announced 17 September 2013; closed 18 March 2014; Wilson's 2022 account that legal issues from retail packaging caused the delay.
- Old School RuneScape Wiki, "Polls" (accessed September 2026). 70% supermajority to pass, excluding skipped votes; voters must be members with at least 300 total level and 25 hours of play.
- Toulmin, S. (1958). *The Uses of Argument*. Cambridge University Press (updated edition 2003). The six-part layout of arguments.
- The criteria scores, weights and the debaters Ana, Ben and Cara are invented for teaching.

## Interactive spec: examples/w14-crux-map.html

**The one insight.** Two debaters who reach opposite conclusions are separated either along the value axis (weights) or along the fact axis (scores). The decision map shows which, so a student can see whether an argument needs evidence or needs a case about priorities.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px (map first). Score sliders above. Readout below.

**Controls.**
- Four score sliders, 0 to 10, step 0.5: `h(F)` default 4, `f(R)` default 3, `f(F)` default 9, and `h(R)` shown as the vertical axis of the map (not a slider).
- Option names as two short text fields, defaults "Restrict" and "Free".
- Three draggable debater dots on the map, named Ana, Ben, Cara, defaults (w, h_R) = (0.7, 8), (0.7, 5), (0.4, 8). Each dot is also keyboard movable: Tab to select, arrow keys move by 0.01 in `w` and 0.1 in `h_R`.
- Buttons: "Reset," and "Diablo III preset" which renames options to "Keep auction house" and "Close it" and relabels the criteria "safe real-money trade" (h) and "fun of finding loot" (f). It sets `h(F)` (safety if closed) to 3, `f(R)` (loot fun if kept) to 2, `f(F)` to 8, and places one dot at (0.5, 7), which gives `w* = 0.6` and "Close it" as the winner.

**Formulas.**
- `U(R) = w × h_R + (1 − w) × f_R`; `U(F) = w × h_F + (1 − w) × f_F`; `D = U(R) − U(F)`.
- `Δh = h_R − h_F`, `Δf = f_R − f_F`. Crux weight `w* = −Δf / (Δh − Δf)` when `Δh − Δf ≠ 0` and the result lies in [0, 1]. Otherwise display "one option wins at every weight."
- Map boundary: for each `h_R` in [0, 10], `w*(h_R) = (f_F − f_R) / ((h_R − h_F) + (f_F − f_R))`, drawn only where it lies in [0, 1].

**Left panel, the decision map.** Horizontal axis `w` from 0 to 1 ("weight on harm prevented"), vertical axis `h(R)` from 0 to 10, labelled with the first option's name ("h score for Restrict" by default). Shade each region by winner with a text label in each region. Draw the boundary curve. Draw the three dots with names. When two dots are selected (shift-click or a "compare" dropdown), draw a line between them and label it "value gap" if their `h_R` values match within 0.1, "fact gap" if their `w` values match within 0.01, and "both" otherwise.

**Right panel, the selected debater.** Two horizontal bars `U(R)` and `U(F)` with values to two decimals, and below them a small chart of `D(w)` from 0 to 1 at the debater's `h_R`, crossing zero at `w*`, with the debater's `w` marked.

**Readout.** Selected debater's `w`, `h_R`, `U(R)`, `U(F)`, winner, `w*` at their `h_R`, and the smallest change in `w` alone, or in `h_R` alone, that would flip their choice.

**Test values (the builder must check these).**
- Defaults, `h_R = 8`: `w* = 0.6`. At `w = 0.7`, `U(R) = 6.5`, `U(F) = 5.5`.
- Boundary: `h_R = 5 → w* = 0.857`; `6 → 0.75`; `9 → 0.545`; `10 → 0.5`.
- Ana (0.7, 8): Restrict, 6.5 against 5.5. Ben (0.7, 5): Free, 4.4 against 5.5. Cara (0.4, 8): Free, 5.0 against 7.0.
- Ana against Ben is a "fact gap." Ana against Cara is a "value gap."
- Ben's smallest flip: raise `h_R` to above 6 (at `w = 0.7`, `w*(h_R) = 0.7` gives `h_R = 6/0.7 − 2 = 6.571`), so "raise h_R by 1.57" or "raise w to 0.857".
- Check-yourself 1 (set `h_R = 7`, `h_F = 3`, `f_R = 2`, `f_F = 8`): `w* = 0.6`; at `w = 0.55`, `U(R) = 4.75`, `U(F) = 5.25`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Region colours paired with text labels and a hatch pattern on one region. Dots have visible focus rings and names. Respect reduced motion. No game logos or art; game names appear only in the preset label.
