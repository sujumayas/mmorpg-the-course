# MMO402 · Week 07 — Justice Systems: Reports, Reviews, Appeals

**Why this matters:** Every online world that bans people runs a court, whether or not anyone designed it as one. The number of reviewers you ask, the vote you require and the appeal you offer decide how many innocent players you punish and how many offenders walk free. Players judge the whole world by whether that court feels fair.

**You will be able to:**
- Compute the chance that a review panel of `n` reviewers with threshold `t` convicts a guilty player and an innocent one, using the binomial distribution.
- Explain, with numbers, why a high conviction rate says nothing on its own about whether a review system is fair.
- Design an appeal stage and estimate how many wrongful sanctions it reverses and how much review work it costs.
- Critique a shipped justice system (League of Legends' Tribunal, CS:GO's Overwatch, EVE Online's strike ladder) against due-process principles.

**Before class:** Santa Clara Principles on Transparency and Accountability in Content Moderation, version 2.0 (santaclaraprinciples.org), the sections on Notice and Appeal, about 15 minutes. EU Digital Services Act (Regulation 2022/2065), Article 20, "Internal complaint-handling system" (one page). Reread MA102 week 6 on the binomial distribution.

**Prerequisites from earlier courses:** [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (the panel model is a binomial tail). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [MMO305 week 9, toxicity research and interventions](../../MMO305-social-systems-and-online-behaviour/lectures/w09-toxicity-research-and-interventions.md) (precision of punishment and the base-rate effect, which this lecture builds on). [MMO305 week 8, griefing](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md). From this course: [week 1, worlds as polities](w01-worlds-as-polities.md) (legitimacy needs fair process), [week 2, alliances and councils](w02-emergent-player-government-alliances-and-councils.md) (Ostrom's graduated sanctions), and [week 6, moderation at scale](w06-moderation-at-scale.md) (how reports are collected and triaged).

**Interactive:** [w07-review-panel.html](../examples/w07-review-panel.html)

---

## 1. A justice system is a pipeline

Week 6 was about volume: millions of chat lines, thousands of reports, a small team. This week is about a single case and what happens to it. When a player is reported, their case passes through a chain of stages. Each stage is a design decision, and each one can make mistakes.

| Stage | Question it answers | Who usually does it |
|---|---|---|
| Report | Did someone think a rule was broken? | Other players |
| Triage | Is this worth a reviewer's time? | Automation: report counts, classifiers, reporter history |
| Review | Did the player break the rule? | Staff, trained volunteers, crowds of players, or a model |
| Sanction | What happens to them? | A rule table, often a strike ladder |
| Notice | What are they told? | Automated message, sometimes with evidence |
| Appeal | Was the decision right? | Ideally someone who did not make the first decision |

Some words you will use all lecture:

- A **case** is one accused player plus the evidence gathered about them (chat logs, match data, replays).
- A **verdict** is the review's answer: guilty or not guilty. Some systems use softer labels, such as CS:GO's "insufficient evidence."
- A **sanction** is the consequence: a warning, a chat restriction, a matchmaking penalty, a suspension, a permanent ban, or confiscation of items.
- A **wrongful conviction** (a false positive) sanctions a player who did not break the rule. A **wrongful acquittal** (a false negative) lets a rule-breaker go.
- **Due process** is the set of procedural protections that make a verdict trustworthy even when it goes against you. Legal systems disagree on details, but most include notice of the charge, a chance to respond, a decision-maker who is not the accuser, reasons for the decision, and a route to appeal.

### Why games need due process at all

A studio is not a state, and a ban is not a prison sentence. Why borrow court language?

First, because players invest real time and money in accounts. A permanent ban on a ten-year account destroys something the player valued, and week 1 showed that switching costs are what make a player stay. A ban sets that player's switching cost to zero in the worst way.

Second, because legitimacy depends on it. Week 1 listed three conditions under which players accept rulings they dislike: predictable rules, fair process and voice that sometimes works. The justice pipeline is where "fair process" is either real or not.

Third, because it is increasingly the law. The EU's Digital Services Act (DSA) applied to all online platforms from 17 February 2024. Article 20 requires platforms to let users complain about moderation decisions for at least six months after the decision, electronically and free of charge. Complaints must be handled under the supervision of qualified staff and not solely by automated means, and decisions found to be unfounded must be reversed without undue delay. A game with chat, user-generated content or a player marketplace should assume its moderation falls under rules like these in the EU. MMO403 and week 11 return to the regulatory side.

Civil society groups have written similar standards. The Santa Clara Principles (version 1.0 in 2018, version 2.0 after a 2020-2021 consultation) ask platforms to tell users which specific rule they broke and how the violation was detected, and to offer appeals reviewed by a person or panel not involved in the first decision. You will use these as a checklist in the activity.

## 2. Worked example: how many reviewers does a ban need?

### The hook

From May 2011 until early 2014, League of Legends ran the **Tribunal**. Players with accounts of sufficient level could review reported cases, reading chat logs and game statistics, and vote to punish or pardon. The majority decided. According to the official League of Legends Wiki's summary of Riot's published figures, 94% of players who reached the Tribunal were punished by their peers, and 74% of players warned just once never came back to it.

Is 94% good news? One reading says the system works: only players with hundreds of reports over dozens of games reached review, so of course nearly all were guilty. Another reading says the crowd was a rubber stamp that convicted almost everyone put in front of it. The number alone cannot tell you which reading is right. By the end of this example you will be able to show that both readings can produce the same 94%, and what you would need to measure to tell them apart.

### The model

Model each reviewer as a noisy test. For a case that reaches review:

- `b` is the **base rate**: the share of reviewed cases where the player really is guilty.
- `s` is a reviewer's **sensitivity**: the chance a single reviewer votes guilty when the player is guilty.
- `f` is a reviewer's **false-guilty rate**: the chance a single reviewer votes guilty when the player is innocent.
- `n` reviewers vote independently. The panel convicts if at least `t` of them vote guilty. `t` is the **threshold**. A simple majority of 5 is `t = 3`; unanimity is `t = n`.

The number of guilty votes is binomial, as in MA102 week 6. So:

```
P_g = P(convict | guilty)   = sum over k = t..n of C(n, k) × s^k × (1 − s)^(n − k)
P_i = P(convict | innocent) = sum over k = t..n of C(n, k) × f^k × (1 − f)^(n − k)

conviction rate          = b × P_g + (1 − b) × P_i
share of convicted who are innocent = (1 − b) × P_i / conviction rate
```

Per 10,000 reviewed cases:

```
wrongful convictions = 10,000 × (1 − b) × P_i
wrongful acquittals  = 10,000 × b × (1 − P_g)
```

This is the **Condorcet jury theorem** in design form. The Marquis de Condorcet showed in 1785 that if each voter is right more often than not, and votes independently, a majority of many voters is almost always right. The version above splits "right" into two numbers, `s` and `f`, because reviewers can be good at spotting guilt and bad at clearing the innocent, and that asymmetry is where game juries go wrong.

### Numbers you can check

Take `b = 0.85`. Triage only sends cases with many reports, so most are guilty. Take `s = 0.9`: reviewers catch nine guilty players in ten. Now compare two crowds.

**Crowd A, careful reviewers, `f = 0.3`.** An innocent player's chat log still looks bad to three reviewers in ten, perhaps because the log shows arguing without the provocation that caused it.

| Panel | `P_g` | `P_i` | Conviction rate | Innocent share of convicted | Wrongful convictions per 10,000 | Wrongful acquittals per 10,000 |
|---|---|---|---|---|---|---|
| 1 reviewer | 0.900 | 0.300 | 81.0% | 5.6% | 450 | 850 |
| 3, majority (`t = 2`) | 0.972 | 0.216 | 85.9% | 3.8% | 324 | 238 |
| 5, majority (`t = 3`) | 0.991 | 0.163 | 86.7% | 2.8% | 245 | 73 |
| 9, majority (`t = 5`) | 0.999 | 0.099 | 86.4% | 1.7% | 148 | 8 |
| 9, supermajority (`t = 7`) | 0.947 | 0.004 | 80.6% | 0.1% | 6 | 450 |
| 5, unanimous (`t = 5`) | 0.590 | 0.002 | 50.2% | 0.1% | 4 | 3,481 |

Check the 5-reviewer majority row for innocents by hand. The panel convicts if 3, 4 or 5 of 5 vote guilty:

```
P(3) = 10 × 0.3^3 × 0.7^2 = 10 × 0.027 × 0.49 = 0.1323
P(4) =  5 × 0.3^4 × 0.7   =  5 × 0.0081 × 0.7 = 0.0284
P(5) =  0.3^5                                  = 0.0024
P_i  = 0.1631
wrongful convictions = 10,000 × 0.15 × 0.1631 = 245
```

With careful reviewers, adding reviewers helps on both sides. Going from one reviewer to five majority cuts wrongful convictions by almost half and wrongful acquittals by more than 90%. Raising the threshold trades one error for the other: the 9-reviewer supermajority nearly eliminates wrongful convictions but lets 450 guilty players go.

**Crowd B, harsh reviewers, `f = 0.6`.** Now an innocent player's case looks guilty to six reviewers in ten. Maybe reviewers see only the accused's chat lines, maybe the interface nudges them toward "punish," maybe the crowd has learned that most cases are guilty and votes that way by habit.

| Panel | `P_g` | `P_i` | Conviction rate | Innocent share of convicted | Wrongful convictions per 10,000 |
|---|---|---|---|---|---|
| 1 reviewer | 0.900 | 0.600 | 85.5% | 10.5% | 900 |
| 5, majority (`t = 3`) | 0.991 | 0.683 | 94.5% | 10.8% | 1,024 |
| 9, majority (`t = 5`) | 0.999 | 0.733 | 95.9% | 11.5% | 1,100 |
| 9, supermajority (`t = 7`) | 0.947 | 0.232 | 84.0% | 4.1% | 348 |

Look at the 5-reviewer majority row. Crowd B convicts 94.5% of cases, almost exactly the Tribunal's published 94%. And it wrongly punishes 1,024 players per 10,000 cases, four times as many as Crowd A. Adding reviewers to a harsh crowd makes things worse, not better: `P_i` rises from 0.60 to 0.68 to 0.73.

That is the reverse side of Condorcet's theorem. A majority of many voters amplifies whatever tendency single voters have. If each reviewer is more likely than not to clear an innocent player (`f < 0.5`), more reviewers push wrongful convictions toward zero. If each reviewer is more likely than not to convict an innocent player (`f > 0.5`), more reviewers push wrongful convictions toward certainty.

To be clear about what this does and does not show: these are teaching numbers, not estimates of the Tribunal's accuracy. The point is that a 94% conviction rate fits both a careful crowd with a guilty-heavy caseload and a harsh crowd convicting many innocents. To tell them apart you need a different measurement: a sample of cases reviewed independently by trained staff, compared with the crowd's verdicts. A conviction rate measures the system's output. It cannot measure the system's accuracy.

### When reviewers are not independent

The theorem assumes each reviewer judges alone. Real reviewers do not. They see the same evidence, framed by the same interface, and in some systems they see how others voted. If the evidence itself misleads (a chat log that omits the other side's provocation, a replay clipped to the worst eight rounds), every reviewer is misled together.

A simple way to model this: with probability `ρ` (rho), the whole panel reaches the verdict a single reviewer would reach, because they all respond to the same misleading impression. With probability `1 − ρ` they vote independently.

```
P_i(correlated) = ρ × f + (1 − ρ) × P_i(panel)
```

For Crowd A's 9-reviewer supermajority, `P_i(panel) = 0.004`. With `ρ = 0.5`:

```
P_i = 0.5 × 0.3 + 0.5 × 0.004 = 0.152
```

Wrongful convictions jump from 6 per 10,000 to about 228. Half the panel's protection disappears because the reviewers were never really nine separate opinions. Two design choices raise independence: show every reviewer the full context (both sides of the chat, the whole match), and hide other reviewers' votes until each has voted.

### A visual you can move

Open `examples/w07-review-panel.html`. The left view plots `P_g` and `P_i` against the number of reviewers, with the threshold set as a fraction of the panel. The right view shows 10,000 reviewed cases as a stacked bar: correct convictions, wrongful convictions, wrongful acquittals and correct acquittals, with the conviction rate printed on top. Start with Crowd A and a panel of 5. Now drag `f` slowly from 0.3 up past 0.5 and watch the innocent curve on the left flip from falling to rising while the conviction rate on the right barely moves. The number a studio would report stays near 90%. The number that matters to innocent players quadruples.

### Cross-game recognition

**League of Legends, the Tribunal (May 2011 to early 2014).** Player reviewers, simple majority, cases formed only after many reports over many games, so `b` was high by design. Reviewers had a "justice rating" based on their voting accuracy, with no reward attached. A rating like that matters for the model: if accuracy is measured against the crowd's own verdicts, it rewards agreeing with the crowd, which pushes reviewers toward each other and raises `ρ`. If it is measured against staff-reviewed ground truth, it rewards being right. When you design a reviewer score, decide which of the two you are measuring. MMO305 week 9 covers the research on the Tribunal's data and Riot's later shift toward rewarding good conduct.

**Counter-Strike: Global Offensive, Overwatch (CS:GO era).** Valve's Overwatch sends reported cases to experienced community "investigators," chosen on criteria such as competitive wins, account age, hours played, skill group and a low report count of their own. Investigators watch an eight-round replay with chat removed and other players' names hidden. Multiple investigators review each case independently, investigators with better accuracy records get more weight, and a conviction requires the collective judgment to converge on an overwhelming verdict. The two verdict options are "insufficient evidence" and "evident beyond a reasonable doubt." In model terms, Valve chose a high threshold `t`, weighted votes by past accuracy (raising the effective `s` and lowering `f`), and removed chat to cut one source of shared bias. The cost is visible in the supermajority rows of the tables: more guilty players acquitted.

**Criminal juries.** Many legal systems treat wrongful conviction as far worse than wrongful acquittal. The English jurist William Blackstone put a ratio on it in the 1760s: better that ten guilty persons escape than that one innocent suffers. A unanimous or near-unanimous jury is a choice of `t` that buys that ratio. In Crowd A's 9-reviewer supermajority row, the ratio of wrongful acquittals to wrongful convictions is `450 / 6 = 75`, well past Blackstone's 10. The 5-reviewer majority gives `73 / 245 ≈ 0.3`, the opposite way round: more than three innocents punished for each guilty player freed.

Three systems, one model. Each chose a panel size, a threshold and a way of presenting evidence, and those choices fixed its balance of errors whether or not anyone wrote the balance down.

### Eyes-open design judgment

- **Decide your error ratio before you pick your panel.** Write down how many wrongful acquittals you will accept to avoid one wrongful conviction, for each sanction. For a 10-minute chat mute, 1:1 may be fine. For a permanent ban on a paid account, you probably want something closer to Blackstone's 10:1 or beyond. Then choose `n` and `t` to hit it.
- **More reviewers are not automatically fairer.** They help only if each reviewer is more likely to clear an innocent than convict one. Measure `f` with audits before you scale a crowd.
- **Protect independence.** Hide votes until each reviewer has voted, show full context, and avoid reviewer scores that reward agreement with the crowd.
- **Do not report conviction rate as a quality metric.** Report audited accuracy: the share of a random sample where an independent expert agrees with the verdict, split into guilty and innocent cases.
- **Crowds cost less money but not less responsibility.** A studio that hands verdicts to players still owns the outcome, and under the DSA it still owes a complaint route with qualified human oversight.

## 3. Appeals: a second look, and who uses it

An appeal is a second review of a sanction, triggered by the sanctioned player. It is the stage that catches what the panel missed. Model it as one more reviewer, ideally a staff member who did not take part in the first decision.

- `a_i` is the chance a wrongly convicted (innocent) player appeals. Innocent players appeal often, but not always: some give up, some never read the notice.
- `a_g` is the chance a rightly convicted (guilty) player appeals. It is lower than `a_i`, but not zero. Appealing is cheap.
- The appeal reviewer overturns an innocent conviction with probability `1 − f_a`, and wrongly overturns a guilty one with probability `1 − s_a`.

```
wrongful convictions reversed = wrongful convictions × a_i × (1 − f_a)
guilty wrongly released        = correct convictions × a_g × (1 − s_a)
appeal workload                = wrongful convictions × a_i + correct convictions × a_g
```

Apply it to Crowd A's 5-reviewer majority: 245 wrongful convictions and `10,000 × 0.85 × 0.991 = 8,427` correct convictions per 10,000 cases. Take `a_i = 0.8`, `a_g = 0.4`, and an appeal reviewer with `s_a = 0.9` and `f_a = 0.2`.

```
wrongful convictions reversed = 245 × 0.8 × 0.8 = 157      (88 remain)
guilty wrongly released       = 8,427 × 0.4 × 0.1 = 337
appeal workload               = 245 × 0.8 + 8,427 × 0.4 = 196 + 3,371 = 3,567
```

Three lessons sit in those lines.

1. **The appeal reverses about two thirds of wrongful convictions.** That is a large gain in fairness for innocent players.
2. **Most of the appeal workload comes from guilty players.** Of 3,567 appeals, 3,371 are from people who were rightly convicted. That is 95%. If your appeal team feels that "everyone who appeals is guilty," this is why, and it is not evidence that the innocent do not exist.
3. **The appeal also frees guilty players.** Here 337 of them, more than twice the number of innocents saved. Whether that trade is acceptable is the same Blackstone question as before.

Design choices that shift these numbers:

- **Independence.** An appeal heard by the same reviewer, or by one who can see the first verdict and its confidence, has a much higher `f_a`, because people tend to confirm what they already decided or were told. The Santa Clara Principles ask for a reviewer not involved in the initial decision.
- **New information.** An appeal that only replays the same evidence adds a correlated reviewer (high `ρ`). Let the player say what the evidence leaves out, and look for it: the other side of the chat, the match before.
- **Reasons.** A notice that names the rule and the evidence lets innocent players appeal precisely, which raises `a_i`, and lets guilty players see there is little point, which can lower `a_g`. Both the DSA and the Santa Clara Principles require stated reasons for this reason among others.
- **Time.** An appeal that takes three weeks on a one-week suspension reverses nothing useful. Match turnaround to sanction length, or pause the sanction while the appeal is heard when the first verdict was close.
- **Costs to appeal.** Some studios limit appeals to one per sanction or charge nothing but require a written statement. A small friction lowers `a_g` more than `a_i` only if innocent players care more, which is plausible for long suspensions and doubtful for short ones.

## 4. Sanctions: proportion and reversibility

The verdict says whether. The sanction says how much. Two principles do most of the work.

**Graduated sanctions.** Week 2 met Ostrom's fifth principle: long-lived communities punish first offences lightly and escalate on repetition. Games implement this as a **strike ladder**. EVE Online's published policy on buying ISK for real money is a clear example: a first offence brings a warning and removal of the purchased goods, a second adds a 7-day ban, and a third makes the ban permanent. Selling ISK, which CCP treats as more serious because it feeds account theft and fraud, goes straight to a permanent ban without appeal. CS:GO's Overwatch splits the other way, by offence type: convicted cheaters are removed from the game, convicted griefers get a cooldown.

A ladder also reduces the damage of wrongful convictions. An innocent player on the first rung loses little, and a second wrongful conviction on the same player is much less likely than the first.

**Match sanction to confidence.** A permanent ban is irreversible in practice: even if you restore the account later, the player's friends and guild have moved on. When the verdict was close, prefer sanctions you can undo: chat restrictions, matchmaking penalties, temporary suspensions. Keep the irreversible ones for cases where evidence is strong, such as a cheating program detected on the client. A useful rule is to compute the expected harm of each sanction option under the probability of guilt, the same expected-value reasoning as MA102 week 4, and pick the sanction with the least expected harm across both kinds of error.

**Reversal of the loot.** Confiscation raises a question sanctions on the person do not: where do the goods go? EVE's RMT policy removes illicit assets even if this drives a wallet negative, and says that where possible CCP returns stolen items to their original owners. Week 9 looks at why this makes items look a lot like property.

## 5. Reports as evidence, and as weapons

The pipeline starts with reports, and reports are not neutral. MMO305 week 9 showed that most toxic incidents come from ordinary players having bad matches, and that precision of punishment falls when the guilty are rare. Two more problems belong here.

**Mass reporting.** If triage sends a case to review after `r` reports, a group of `r` friends can put anyone in front of a jury. With a harsh crowd (`f > 0.5`), that is close to a guaranteed conviction. Defences: count reports per distinct match rather than per reporter, weight each reporter by how often their past reports were upheld, and flag clusters of reports from players who always queue together.

**Reporter reputation.** Weighting reporters by past accuracy lowers the false-report rate at triage, which raises `b` for the cases that reach review. Note the loop: a harsh jury upholds bad reports, which raises those reporters' weight, which sends more bad cases to the same jury. Audits against staff ground truth break the loop, and nothing else does.

## In-class activity (25 minutes)

In groups of three, you run trust and safety for a mid-sized MMO. Your review team can handle 2,000 case reviews a week. You get about 400 cases a week that pass triage, and you estimate `b = 0.8`, `s = 0.9` and `f = 0.35` for your trained volunteer reviewers.

1. Use the interactive to choose `n` and `t` for two sanctions: a 24-hour chat restriction and a permanent ban. State your target error ratio for each first (5 minutes).
2. Check your workload: `400 × n` reviews per week, plus appeals. Use `a_i = 0.8`, `a_g = 0.4`. Does it fit in 2,000? If not, what do you cut (10 minutes)?
3. Audit your design against the Santa Clara Notice and Appeal sections. List every requirement you meet and every one you miss (5 minutes).
4. One group presents; another group plays the harsh crowd (`f = 0.6`) and shows what happens to the presented design (5 minutes).

Expected output: a one-page design with `n`, `t` and the error ratio for each sanction, a workload line, and a compliance list.

## Common misconceptions

- **"A 94% conviction rate proves the reviewers are good."** It is equally consistent with harsh reviewers and a guilty-heavy caseload. Only an audit against independent ground truth measures accuracy.
- **"More jurors always means fairer verdicts."** Only if each juror is more likely to clear an innocent than to convict one (`f < 0.5`). Otherwise more jurors make wrongful convictions more likely.
- **"Nine reviewers means nine opinions."** Reviewers who see the same misleading evidence, or each other's votes, behave like fewer reviewers. Correlation erases much of a panel's protection.
- **"Appeals are mostly from guilty players, so they are a waste."** Most appeals are from guilty players because most convicted players are guilty. The appeal still reverses a large share of the wrongful convictions, which are the errors that damage trust most.

## Check yourself

1. A panel of 3 reviewers convicts on a majority (`t = 2`). Each reviewer has `f = 0.2`. What is `P_i`? What is it for a single reviewer? Is the panel fairer to innocent players?
2. Two studios both use a 3-reviewer majority, and both have `b = 0.9` and `s = 0.95`. Studio X's reviewers have `f = 0.2`, studio Y's have `f = 0.6`. Compute each studio's conviction rate and its wrongful convictions per 10,000 cases. Which difference is bigger, in relative terms?
3. A 5-reviewer unanimous panel has `P_i = 0.3^5 = 0.0024` when reviewers are independent. With `ρ = 0.4` and `f = 0.3`, what is `P_i`?
4. Your appeal team reports that 97% of appeals are rejected, and proposes removing appeals for 3-day suspensions. What two numbers would you ask for before agreeing?

<details>
<summary>Answers</summary>

1. `P_i = 3 × 0.2^2 × 0.8 + 0.2^3 = 0.096 + 0.008 = 0.104`, against 0.2 for one reviewer. Yes: with `f < 0.5`, the majority halves the innocent conviction rate.
2. `P_g = 3 × 0.95^2 × 0.05 + 0.95^3 = 0.135 + 0.857 = 0.993`. For X, `P_i = 0.104` (from question 1), so the conviction rate is `0.9 × 0.993 + 0.1 × 0.104 = 0.894 + 0.010 = 90.4%` and wrongful convictions are `10,000 × 0.1 × 0.104 = 104`. For Y, `P_i = 3 × 0.6^2 × 0.4 + 0.6^3 = 0.432 + 0.216 = 0.648`, so the rate is `0.894 + 0.065 = 95.9%` and wrongful convictions are 648. The conviction rates differ by about 6%. The wrongful convictions differ by a factor of six.
3. `P_i = 0.4 × 0.3 + 0.6 × 0.0024 = 0.12 + 0.0014 = 0.121`. Correlation raises it fifty-fold.
4. The share of appeals that come from players who were wrongly convicted, estimated by auditing a sample of rejected appeals, and the number of wrongful convictions reversed per week. A 97% rejection rate is expected when most convicted players are guilty. What matters is how many innocent players the remaining 3% saves, and whether the appeal reviewer is independent enough that the 97% reflects a real second look rather than a rubber stamp on the first verdict.

</details>

## Lab / assignment hook

[Lab 07, tune a review panel](../labs/lab07.md). You run a simulated justice pipeline on a synthetic caseload, choose panel size, threshold, strike ladder and appeal policy for two sanctions, and defend the error ratios you chose in a 500-word policy memo. The memo counts toward the course's case analyses.

## Sources

- League of Legends Wiki (official), "Tribunal" (accessed September 2026). Launched May 2011, disabled early 2014; reviewers level 20 (formerly 30) and not banned; up to 20 cases a day; chat logs, game statistics and report details; punish or pardon by majority; "justice rating" with no reward; cases formed only after many reports over many games; 94% of players reaching the Tribunal punished; 74% of players warned once never returned.
- Valve, "Counter-Strike: Global Offensive, Overwatch FAQ" (blog.counter-strike.net, CS:GO era, accessed September 2026). Investigator selection criteria; eight-round replays with chat removed and names hidden; independent reviews weighted by investigator accuracy; overwhelming convergence required; verdicts "insufficient evidence" and "evident beyond a reasonable doubt"; cheaters removed, griefers given a cooldown.
- CCP Games, EVE Online Support, "Real Money Trading (RMT)" (policy page, updated 9 September 2026). Three-strike ladder for ISK buying (warning and removal; plus 7-day ban; permanent ban); permanent ban without appeal for ISK sellers; removal of illicit assets even into negative wallet balance; returning items to original owners.
- Regulation (EU) 2022/2065, Digital Services Act, Article 20 (text via eu-digital-services-act.com), and Wikipedia, "Digital Services Act" (accessed September 2026). Complaint window of at least six months, free and electronic, not solely automated, reversal without undue delay; application to all platforms from 17 February 2024.
- Santa Clara Principles on Transparency and Accountability in Content Moderation, version 2.0 (santaclaraprinciples.org, accessed September 2026). Version 1.0 in 2018; Notice (specific rule, detection method) and Appeal (human review by someone not involved in the initial decision, reasons) requirements.
- Condorcet, Marquis de (1785). *Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix*. The jury theorem.
- Blackstone, W. (1765-1769). *Commentaries on the Laws of England*, Book 4. The ten-to-one ratio, paraphrased.
- Ostrom, E. (1990). *Governing the Commons*. Cambridge University Press. Graduated sanctions.
- All values of `b`, `s`, `f`, `ρ`, `a_i`, `a_g`, `s_a` and `f_a` in sections 2 and 3 are invented for teaching. They do not estimate the accuracy of the Tribunal, Overwatch or any other real system.

## Interactive spec: examples/w07-review-panel.html

**Purpose.** Show that a review panel's conviction rate can stay almost flat while the number of innocent players it punishes changes several-fold, and that more reviewers help only when single reviewers lean toward clearing the innocent.

**The one insight the visual must make obvious.** Dragging `f` across 0.5 flips the innocent-conviction curve from falling to rising with panel size, while the headline conviction rate barely moves.

**Layout.** Two linked views side by side on desktop, stacked on mobile (left view first).

- **Left view: "What the panel does to one case."** x axis: panel size `n` from 1 to 15 (odd and even allowed). y axis: probability 0 to 1. Two lines: `P_g` (guilty convicted) and `P_i` (innocent convicted). Mark the currently selected `n` with a vertical line and print both values beside it. Draw a faint dashed horizontal reference at `f` (what one reviewer does).
- **Right view: "10,000 reviewed cases."** One horizontal stacked bar (or a 100 × 100 waffle grid of cells if it fits) with four segments: correct convictions, wrongful convictions, wrongful acquittals, correct acquittals. Above it, large text: "Conviction rate: X%". Below it, three numbers: "Innocent players punished: N", "Guilty players freed: M", "Freed guilty per punished innocent: R" (R = M / N, show "∞" if N rounds to 0).
- **Appeal panel (collapsible, closed by default).** Toggle "Add an appeal". When on, the right view gains a second bar "After appeal" and prints: wrongful convictions reversed, guilty wrongly released, appeal workload, and the share of the workload from guilty players.

**Controls.**
- `b` base rate, slider 0.50 to 0.99, step 0.01, default 0.85.
- `s` sensitivity, slider 0.50 to 0.99, step 0.01, default 0.90.
- `f` false-guilty rate, slider 0.05 to 0.80, step 0.01, default 0.30.
- `n` panel size, slider 1 to 15, default 5.
- Threshold rule, segmented control: "Majority" (`t = floor(n/2) + 1`), "Two thirds" (`t = ceil(2n/3)`), "Unanimous" (`t = n`), "Custom" (reveals a `t` slider from 1 to `n`), default Majority. Print the resulting `t`. In Custom mode the left view keeps the same fraction `t/n` as `n` changes, rounded up.
- `ρ` correlation, slider 0 to 0.9, step 0.05, default 0.
- Appeal (when on): `a_i` 0 to 1 default 0.8, `a_g` 0 to 1 default 0.4, `s_a` default 0.9, `f_a` default 0.2.
- Preset buttons: "Crowd A (careful)" sets `b = 0.85, s = 0.9, f = 0.3, ρ = 0`; "Crowd B (harsh)" sets `f = 0.6`, others the same; "Supermajority" sets Crowd A with `n = 9` and Custom `t = 7`.

**Formulas.**
```
binomTail(n, t, p) = sum_{k=t..n} C(n,k) p^k (1−p)^(n−k)
P_g = ρ × s + (1 − ρ) × binomTail(n, t, s)
P_i = ρ × f + (1 − ρ) × binomTail(n, t, f)
convictionRate = b × P_g + (1 − b) × P_i
wrongConv   = 10000 × (1 − b) × P_i
wrongAcq    = 10000 × b × (1 − P_g)
correctConv = 10000 × b × P_g
correctAcq  = 10000 × (1 − b) × (1 − P_i)
reversed    = wrongConv × a_i × (1 − f_a)
released    = correctConv × a_g × (1 − s_a)
workload    = wrongConv × a_i + correctConv × a_g
guiltyShare = correctConv × a_g / workload
```
In the left view, the lines use the same threshold rule at every `n`.

**Test values (the page must reproduce these, rounded).**
- Crowd A, `n = 5`, Majority: `P_g = 0.991`, `P_i = 0.163`, conviction 86.7%, wrongful convictions 245, wrongful acquittals 73.
- Crowd A, `n = 9`, Custom `t = 7`: `P_g = 0.947`, `P_i = 0.0043`, conviction 80.6%, wrongful convictions 6, wrongful acquittals 450.
- Crowd A, `n = 9`, Custom `t = 7`, `ρ = 0.5`: `P_i = 0.152`, wrongful convictions about 228.
- Crowd B, `n = 5`, Majority: `P_i = 0.683`, conviction 94.5%, wrongful convictions 1,024.
- Appeal on, Crowd A, `n = 5`, Majority: reversed 157, released 337, workload 3,567, guilty share 94.5%.

**Accessibility and style.** Use `templates/interactive-tokens.css` inline. All sliders keyboard operable with visible labels and live numeric readouts. Colour segments must also differ by pattern or label so the bar reads without colour. Respect `prefers-reduced-motion` (no animated transitions). No game logos or art; label the presets in text only.
