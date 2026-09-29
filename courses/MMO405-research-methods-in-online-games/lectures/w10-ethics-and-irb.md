# MMO405 · Week 10 — Ethics and IRB

**Why this matters:** No ethics board, no study. Before your thesis collects a single answer, someone outside your project will read your plan and decide whether players are safe in it. Students who treat that review as paperwork get sent back for revisions and lose weeks. Students who design the protections into the method get approved, and they often end up with better data. This week shows how, including one case where adding deliberate noise to a survey gives you a more accurate answer.

**You will be able to:**
- Classify a proposed game study by review level (not human-subjects research, exempt, expedited, full board) using the Common Rule's definitions, and name the fact that decides each call.
- Compute the estimate, standard error, sample-size cost and privacy guarantee of a randomized response survey, and compare it with a direct question that players answer dishonestly.
- Draft the sections of an ethics application for an online-game study: consent, waiver requests, data handling, distress and incidental-findings protocols.
- Critique a study plan for the ethical problems that are also validity problems, and propose a design change that fixes both.

**Before class:** U.S. Code of Federal Regulations, 45 CFR 46 (Common Rule, 2018 requirements), read §46.102 (definitions), §46.104(d)(2) to (d)(4) (exemptions) and §46.116(f) (waivers), about 25 minutes on the Cornell Legal Information Institute site. Boellstorff, Nardi, Pearce and Taylor, *Ethnography and Virtual Worlds* (2012), chapter 8, "Ethics" (pp. 129-150), and chapter 9, "Human Subjects Clearance and Institutional Review Boards" (pp. 151-158). Tourangeau and Yan, "Sensitive Questions in Surveys" (2007), pp. 859-866.

**Prerequisites from earlier courses:** [MMO402 week 12, research ethics in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md) (the Belmont principles, when product testing becomes research, terms of service are not consent, and k-anonymity for data releases; this week does not repeat them). [MMO402 week 11, minors in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w11-minors-in-online-worlds.md). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the standard error of a proportion). Earlier in this course, [week 3](w03-telemetry-as-research-data.md) (consent for linkage and the GDPR research rules), [week 6](w06-qualitative-methods-interviews.md) (interview consent) and [week 7](w07-ethnography-and-participant-observation.md) (observer roles).

**Interactive:** [Randomized response explorer](../examples/w10-randomized-response.html). Keep it open during section 2.

---

## 1. What an ethics board decides

MMO402 week 12 gave you the principles. This week is about the institution that applies them, and how to design a study that passes.

In the United States the institution is an **Institutional Review Board (IRB)**, working under the Common Rule (45 CFR 46). In the UK, the EU and most other places it is a **research ethics committee (REC)** at your university, working under national rules and the university's own policy. The questions are close enough that one application template serves both. This lecture uses the Common Rule's wording because it is public and precise.

### Is it human-subjects research at all?

Two definitions decide whether review applies. **Research** is a systematic investigation designed to contribute to generalizable knowledge (§46.102(l); MMO402 week 12 covered this). A **human subject** is a living person about whom a researcher either obtains information through interaction or intervention, or obtains identifiable private information (§46.102(e)(1)).

The second half of that definition matters most for game studies. **Private information** means behavior in a context where the person can reasonably expect no one is observing or recording, and information given for a specific purpose that the person can reasonably expect will not be made public (§46.102(e)(4)). A guild's private voice channel meets that test. A leaderboard does not. Most of what you will study sits between those poles: trade chat in a capital city, a guild forum that requires an account, a Discord server with 40,000 members. The regulation gives you the question. The AoIR guidelines you met in [week 7](w07-ethnography-and-participant-observation.md) give you the context-based way to answer it. Your board gives you the answer for your study.

### Four levels of review

| Level | What qualifies | Who reviews | Typical game study |
|---|---|---|---|
| Not human-subjects research | No interaction and no identifiable private information | Often a short determination form | Content analysis of patch notes; public aggregate player counts |
| Exempt | Fits one of the categories in §46.104(d) | IRB office confirms; no full board | Anonymous survey of adult players; observation of public spaces without participating |
| Expedited | No more than minimal risk and on the federal expedited list (§46.110) | The chair or one or more experienced reviewers the chair designates | Recorded interviews with adult players; identified survey linked to logs |
| Full board | More than minimal risk, or not eligible for the other routes | The convened board | Sensitive questions put to minors, studies of players in crisis, or deception about harmful content |

**Minimal risk** means the probability and size of harm are not greater than those met in daily life or in routine examinations (§46.102(j)). Playing a game, answering questions about it and being observed in a public city usually meet that test. Being asked to admit a bannable offense, with your account name attached, may not.

Three exemptions cover most student game research.

- **(d)(2): surveys, interviews, observation of public behavior.** Exempt if at least one holds: the data are recorded so that people cannot be readily identified, or disclosure of the answers would not reasonably put people at risk of criminal or civil liability or damage their financial standing, employability, educational advancement or reputation, or the board does a limited review of the privacy protections. Read the second condition with a game study in mind. Answers that could cost someone their account or their standing in a competitive community are the kind the board will ask about.
- **(d)(3): benign behavioral interventions** with adults who agree in advance. The regulation's own examples include "having the subjects play an online game" (§46.104(d)(3)(ii)). Deception is allowed under this exemption only if participants agree in advance that they may be deceived.
- **(d)(4): secondary research on identifiable private information**, exempt if the information is publicly available, or if you record it so that people cannot be identified, never contact them and never re-identify them. This is the category [week 9](w09-social-network-analysis-of-guilds.md) pointed to for network data collected from logs without players' knowledge. It removes the full review. It does not remove the duties in week 9's list: third parties, structural re-identification and what you hand back to the community.

Two cautions. Exempt does not mean "no review". The federal Office for Human Research Protections (OHRP) recommends that researchers not declare their own studies exempt, so the IRB office usually confirms it. Check your institution's policy before you start. And children change the rules. Under Subpart D, the survey and interview exemption does not apply to minors, (d)(3) covers adults only, and observation of public behavior qualifies only when you do not take part (§46.104(b)(3)). A game with a young player base pushes your study toward expedited or full review unless you screen for adults.

### What the board must find

To approve a study, the board must find the criteria in §46.111(a)(1) to (7). Risks are minimized, and procedures are "consistent with sound research design". Risks are reasonable relative to benefits and to the knowledge gained. Selection of participants is fair. Consent is sought, and it is documented, unless either step is properly waived. Data are monitored for safety when appropriate. Privacy and confidentiality are protected.

Look at the first item again. **A study that cannot answer its question has no benefit to weigh against any risk.** An underpowered experiment, a survey whose answers will be dishonest, a sample that cannot speak for the population named in the title: these are validity problems, and a board can treat them as ethics problems. The worked example is a case where the ethical fix and the validity fix are the same design.

## 2. Worked example: the survey that tells players to lie

### The hook

Old School RuneScape's rules forbid real-world trading, meaning buying or selling gold, items or accounts for money or anything else of value. Jagex clarified the definition in its Rules of RuneScape on 9 April 2025, and players caught at it risk temporary or permanent bans. Suppose your thesis asks what share of active players have ever bought gold.

Ask the question directly and every honest "yes" is a written confession to a bannable offense. If you link the survey to accounts, as [week 4](w04-survey-design-and-validated-scales.md) recommended for validity, the confession is attached to a name. Your board will ask what happens if the data leak or the studio asks for them. Your players will do the obvious thing, and many buyers will say "no". Tourangeau and Yan's review of survey research found that misreporting on sensitive topics is common and that respondents edit their answers to avoid embarrassment or "repercussions from third parties". A ban is exactly that.

In 1965 Stanley Warner proposed a fix that sounds absurd: have each respondent flip a coin in private, and on some flips give a random answer instead of the true one. No single answer then means anything. The aggregate still does. In 2014 Google used the same idea in Chrome (RAPPOR, below). The same trick protects your gold buyers.

### The model

This version of **randomized response** works as follows. Each respondent privately rolls a die or uses a random-number widget you provide. With probability `t` they answer truthfully. Otherwise a fair coin decides their answer, "yes" or "no", regardless of the truth.

- `π` is the true share of players who have bought gold. It is what you want.
- `t` is the truth probability, set by you, between 0 and 1.
- `q` is the share of "yes" answers you will observe.
- `n` is the number of respondents.

The chance of a "yes" is

```
q = t × π + (1 − t) / 2
```

Solve for `π` and put the observed share of "yes" answers, `q̂`, in place of `q`:

```
π̂ = (q̂ − (1 − t) / 2) / t
SE(π̂) = sqrt(q × (1 − q) / n) / t
```

The standard error is the MA102 week 13 standard error of a proportion, `sqrt(q(1 − q)/n)`, divided by `t`. That division is the price. With `t = 0.5`, you are measuring a signal half as strong, so every bit of sampling noise is doubled.

Now the protection. A player who has bought gold says "yes" with probability `t + (1 − t)/2`. A player who has not says "yes" with probability `(1 − t)/2`. The ratio of the two is

```
(1 + t) / (1 − t)        (the same ratio holds for "no")
```

That ratio caps how much any single answer can shift anyone's belief about that player. Whatever you, the studio or a data thief believed before, a "yes" multiplies the odds that the player bought gold by exactly this factor, and no more. In the language of **differential privacy**, which MMO402 week 12 introduced, this is `ε`-differential privacy for each respondent (local differential privacy) with

```
ε = ln((1 + t) / (1 − t))
```

With `t = 0.5`, the ratio is 3 and `ε = ln 3 ≈ 1.10`. This is the standard textbook example in Dwork and Roth's monograph on differential privacy.

### Numbers you can check

Take `π = 0.10` (one player in ten has bought gold; an invented value) and `n = 2,000` respondents.

```python
from math import sqrt, log

def rr_row(pi, t, n):
    q = t * pi + (1 - t) / 2                  # chance of a "yes"
    se = sqrt(q * (1 - q) / n) / t            # standard error of the estimate
    post_yes = pi * (t + (1 - t) / 2) / q     # P(bought | said yes)
    eps = log((1 + t) / (1 - t)) if t < 1 else float("inf")
    return q, se, post_yes, eps

pi, n = 0.10, 2000
se_direct = sqrt(pi * (1 - pi) / n)
print(" t     q     SE     +-95%   P(bought|yes)  eps   n for direct SE")
for t in (1.0, 0.75, 0.5, 0.25):
    q, se, post, eps = rr_row(pi, t, n)
    n_match = round(n * (se / se_direct) ** 2)
    print(f"{t:4.2f}  {q:.2f}  {se:.4f}  {1.96*se:.3f}  {post:13.3f}  {eps:4.2f}  {n_match:>6}")
```

Output:

```
 t     q     SE     +-95%   P(bought|yes)  eps   n for direct SE
1.00  0.10  0.0067  0.013          1.000   inf    2000
0.75  0.20  0.0119  0.023          0.438  1.95    6321
0.50  0.30  0.0205  0.040          0.250  1.10   18667
0.25  0.40  0.0438  0.086          0.156  0.51   85333
```

| Truth probability `t` | "Yes" share `q` | Standard error | 95% margin | P(bought given "yes") | `ε` | `n` for the direct question's precision |
|---|---|---|---|---|---|---|
| 1.00 (direct question) | 0.10 | 0.0067 | ±1.3 points | 100% | no protection | 2,000 |
| 0.75 | 0.20 | 0.0119 | ±2.3 points | 43.8% | 1.95 | 6,321 |
| 0.50 | 0.30 | 0.0205 | ±4.0 points | 25.0% | 1.10 | 18,667 |
| 0.25 | 0.40 | 0.0438 | ±8.6 points | 15.6% | 0.51 | 85,333 |

Check the `t = 0.5` row by hand. `q = 0.5 × 0.10 + 0.25 = 0.30`. `SE = sqrt(0.30 × 0.70 / 2000) / 0.5 = 0.01025 / 0.5 = 0.0205`. A "yes" comes from a buyer with probability `0.10 × 0.75 = 0.075` and from a non-buyer with probability `0.90 × 0.25 = 0.225`, so P(bought given "yes") `= 0.075 / 0.30 = 0.25`. Prior odds were 1 to 9. Posterior odds are 1 to 3. The factor is 3, as promised.

Read it as a trade. At `t = 0.5` a "yes" is 25% evidence instead of 100%, and you pay a factor of 9.3 in sample size.

### Why the noisy survey can still win

The table assumes everyone answers honestly. The whole point is that they don't. Suppose half of the buyers deny it when asked directly (an invented but modest figure given Tourangeau and Yan's review). The direct question then estimates `0.5 × 0.10 = 0.05` with a standard error of about 0.005. It is precise and wrong by 5 points, and **no sample size fixes it**. Twenty thousand respondents give you a tighter interval around the wrong number.

Randomized response with `t = 0.5`, if players follow the instructions, is centered on 0.10 with a standard error of 0.02. Its root-mean-square error, the typical distance from the truth, is about 0.020 against the direct question's 0.050. The noisy method is about 2.45 times closer to the truth at `n = 2,000` (0.0502 / 0.0205). Bias is a fixed cost. Variance is a cost you pay down with sample size.

That "if" matters. Lensvelt-Mulders and colleagues' meta-analysis of validation studies, where researchers knew the true answers, found that randomized response reduced wrong answers but did not remove them. The mean share of incorrect answers was 0.38 with randomized response and 0.49 with other methods, and the advantage grew with how sensitive the topic was. Treat randomized response as a large improvement, not a cure.

### A visual you can move

Open the interactive. The left view, **"What one answer reveals"**, shows the prior share of buyers as a bar, then the share among players who said "yes" and among those who said "no". At `t = 1` the "yes" bar jumps to 100%. Slide `t` down and watch it sink toward the prior. The right view, **"What the study learns"**, plots each method's estimate with its 95% interval against sample size. The direct question's interval is narrow and sits below the true value. The randomized-response interval is wide and centered on the truth, and it narrows as you drag `n` up. Set the honesty slider to 100% and the direct question wins everywhere. Set it to 50% and find the sample size where the randomized interval first excludes the direct estimate.

### Cross-context recognition

**Google RAPPOR (Chrome, 2014).** Google's announcement describes the forced-"yes" cousin of our design: flip a coin, answer truthfully on heads, and always say "yes" on tails. In our notation the "yes" share is `q = t × π + (1 − t)`. The algebra and the square-root cost are the same. RAPPOR adds hashing and repeated noise so a browser's reports cannot be linked over time, which is the trajectory problem from MMO402 week 12 solved at collection time.

**Sensitive surveys in health and education.** Randomized response has been used for decades to estimate drug use, academic cheating and tax evasion, the three kinds of question where a truthful individual answer can hurt the person. The Lensvelt-Mulders meta-analysis pooled 32 comparative studies of this kind.

**Your own game's anti-cheat survey.** A studio that asks its players "have you used a bot?" in an in-client survey has the same problem in a stronger form, because the studio can ban. Here the protection must be real to the player, not only to the researcher. A die roll the studio controls on its own server is no protection at all. The randomization must happen where the player can see it, and the studio must be unable to recover it.

### Eyes-open design judgment

- **Use it only for questions that need it.** Randomized response costs a factor of 3 to 40 in sample size. For a question like "how many hours did you play last week?" there is no confession to protect, and the cost buys nothing.
- **Players must understand and trust the randomizer.** If they think you can see the die, they answer as if asked directly. Show the randomizer on screen and pilot the instructions.
- **Choose `t` deliberately and report it.** `t = 0.5` to 0.75 is common. Lower `t` protects more and costs quadratically more. Put `t`, the implied `ε` and the sample size calculation in your ethics application and your methods section.
- **You lose individual-level analysis.** You cannot correlate one player's gold buying with their satisfaction score, because you do not know who bought. You can still compare groups (buyers' share among satisfied versus dissatisfied players) with a regression built for randomized responses, at a further cost in precision. If your question needs individual linkage, randomized response is the wrong tool. Consider instead whether you need the account link at all.
- **It is one of several indirect methods.** The **item count technique** (a list of items, respondents report only how many apply) and simply not collecting identifiers are alternatives. The board wants to see that you considered the least identifying design that still answers the question, in the spirit of GDPR Article 89(1)'s data minimization.

### Check yourself (worked example)

1. With `t = 0.6` and 900 "yes" answers from 3,000 respondents, what is `π̂` and its standard error?
2. What value of `t` gives `ε = ln 2`? What share of "yes" answers would you expect from a population with `π = 0.2`?
3. A classmate says, "randomized response is less accurate, so it's the ethical choice but the worse method." Using this section's numbers, when is that true and when is it false?

<details>
<summary>Answers</summary>

1. `q̂ = 0.30`. `π̂ = (0.30 − 0.20) / 0.6 = 0.167`. `SE = sqrt(0.3 × 0.7 / 3000) / 0.6 = 0.00837 / 0.6 = 0.0139`.
2. `(1 + t)/(1 − t) = 2` gives `t = 1/3`. Then `q = (1/3)(0.2) + (1/3) = 0.40`.
3. It is true when respondents would answer a direct question honestly, because then randomized response only adds variance. It is false when direct answers are biased: the direct method's bias does not shrink with `n`, so with enough respondents randomized response has the smaller total error (about 2.45 times smaller at `n = 2,000` in the lecture's example with half the buyers lying, and smaller at every `n` from 318 up).

</details>

## 3. Writing the application

[Week 3](w03-telemetry-as-research-data.md) listed what an application must contain. Here is how to write each part for a game study, and what boards push back on.

### Summary and question

One plain paragraph a board member outside games can follow: game, population (adults who played in the last 30 days), question, method. Define every game term on first use.

### Recruitment

Say where and how you will reach players, and show the exact text. Guild leaders and Discord moderators are gatekeepers. A post by a moderator can feel like pressure from someone with power over the reader, so ask them to share a neutral message and not to endorse it. Say how you will exclude minors: an age question at the start that ends the survey for anyone under 18, plus recruitment in adult spaces. Admit the screen is imperfect.

Incentives need care. An in-game item may breach the game's rules if you give it yourself, and it ties the study to the studio in players' minds. Keep payments small, and pay people who withdraw halfway.

### Consent

The Common Rule requires that consent start with a **concise and focused presentation of the key information** that helps a person decide whether to take part (§46.116(a)(5)(i)). For a game study that is usually five sentences: who you are, what you are asking, how long it takes, the main risk, and that they can stop at any time without losing anything. The full elements follow: purpose, procedures, foreseeable risks, benefits, confidentiality, contacts, that participation is voluntary, and whether the data may be used in future research (§46.116(b)).

For online studies, the board can waive the **signed** form, for example when the study is minimal risk and involves nothing for which written consent is normally required, or when the signature would be the only record linking the player to the study and a breach is the main risk (§46.117(c)). A consent page with an "I agree" button is the usual result. That is a waiver of documentation, not of consent.

### Waivers and deception

Sometimes asking for consent would ruin the study. Observing trade chat to measure scam rates is one example. Telling a field experiment's players what is being tested is another. The board may **waive or alter consent** only if it finds all five of the following (§46.116(f)(3)):

1. The research involves no more than minimal risk.
2. It could not practicably be carried out without the waiver.
3. If it uses identifiable information, it could not practicably be done without the identifiers.
4. The waiver will not adversely affect participants' rights and welfare.
5. Where appropriate, participants will receive pertinent information afterward.

Item 3 is the one students forget. If you can do the study without character names, the board will ask why you are keeping them. Item 5 is the **debrief**: after a study that withheld information, you tell participants what you did and why, and in most designs you let them withdraw their data. For a field experiment in a live game, the debrief may be an in-game message or a post the community will see. Plan its wording before the study, not after.

Covert roles in ethnography ([week 7](w07-ethnography-and-participant-observation.md)) fall under the same test. Your application must show that the role is necessary, the risk minimal, and the protection of everyone you observe complete.

### Data management

Say what you will collect, where it lives, who can see it, when it is pseudonymized, when the key linking pseudonyms to accounts is destroyed, and when the data are deleted. Include the calculation from MMO402 week 12 if you plan to release any rows. If a studio partner holds the logs, say who holds the linkage key and who controls publication (week 3). If EU or UK players are involved, attach your data protection notice as a separate document, because research consent and the GDPR legal basis are different things (week 3).

### Distress and incidental findings

Game research meets people in trouble more often than students expect: a player who mentions self-harm in an interview about quitting, a chat log with a threat against a named person. Your application needs a written protocol: what you will say, which resources you will give (a crisis line for the players' country, the game's own reporting tools), when you will stop the session, and whom you will tell. Do not promise confidentiality you cannot keep if someone is at risk.

**Incidental findings** are things you learn that you were not looking for: evidence of cheating in logs, an account you recognize as a minor, a guild's plan to harass another. Decide in advance which you will report and to whom, and tell participants in the consent form. "We will not report rule-breaking to the developer" is a promise you must be able to keep, including against a studio partner.

### Studies inside a studio

If you publish from a studio's data, you are doing research even if no university is involved (MMO402 week 12). Without a board, write these sections for yourself before the study runs. Venues increasingly ask for an ethics statement (week 11).

## In-class activity (25 minutes)

Groups of three. Each group receives a one-page study plan (invented): "We will survey 1,500 players of a free-to-play MMO recruited through the game's official Discord, ask whether they have ever used a third-party bot, link answers to account IDs supplied by the studio, and correlate botting with 90-day spending."

1. **Classify (5 min).** Human-subjects research? Which review level? Name the fact that decides it and cite the section of the regulation.
2. **Find the double problems (8 min).** List at least three features that are both an ethical problem and a validity problem. For each, write one sentence on each side.
3. **Redesign (8 min).** Rewrite the plan so it could be exempt or expedited. Decide whether to use randomized response, drop the account link, or both. If you use randomized response, pick `t` and compute the sample size that keeps the 95% margin at ±4 points when `π` is about 0.10.
4. **Key information (4 min).** Write the five-sentence opening of the consent page.

Expected output: a classification with a citation, a table of three double problems, a redesigned plan with a sample-size number, and five sentences.

## Common misconceptions

- **"Exempt means I don't need to apply."** Exempt means exempt from most of the Common Rule's requirements. OHRP advises that researchers not decide this alone, so expect the IRB office to confirm the exemption. You still owe participants honest information and confidentiality.
- **"Public data needs no ethics review."** Publicly available information can make secondary research exempt under (d)(4)(i). Whether a Discord server or a guild forum is "public" in the sense that matters is a context question, and the board decides. The ethical duties to third parties and against re-identification remain.
- **"Adding noise to answers makes the data worse."** It makes each answer worse. It can make the estimate better, when the alternative is an answer players will lie to.

## Check yourself

1. You plan to interview 12 adult raid leaders about how they handle loot disputes, record the calls and quote them under pseudonyms. Which review level is most likely, and what single change could make it exempt under (d)(2)?
2. Your randomized response survey uses `t = 0.5` and gets 1,200 "yes" answers out of 4,000. Estimate `π`, its standard error and a 95% interval.
3. A board rejects your field experiment's consent waiver on criterion 3 of §46.116(f)(3). What did your design probably include, and how do you fix it?
4. For `π = 0.05` and `t = 0.75`, how many respondents give a 95% margin of ±2 points? Compare with a direct question answered honestly.
5. Why does §46.111(a)(1)'s phrase "consistent with sound research design" make an underpowered study an ethics problem?

<details>
<summary>Answers</summary>

1. Expedited, because the recordings are identifiable (voices) and (d)(2)(i) fails. Whether (d)(2)(ii) applies depends on whether the content could damage reputations, which loot disputes might. The simplest route to exempt under (d)(2)(i) is not recording audio, and writing notes in which people cannot be identified. You lose verbatim quotes, which may be a fair trade.
2. `q̂ = 0.30`, `π̂ = (0.30 − 0.25)/0.5 = 0.10`. `SE = sqrt(0.3 × 0.7/4000)/0.5 = 0.00725/0.5 = 0.0145`. Interval `0.10 ± 0.028`, about 7.2% to 12.8%.
3. You kept identifiable information, such as character names or account IDs, that the study did not need. Record at a level that cannot identify players, or show why identifiers are necessary (for example, you must link two datasets, and you destroy the key right after).
4. `q = 0.75 × 0.05 + 0.125 = 0.1625`. Need `1.96 × sqrt(q(1 − q)/n)/t ≤ 0.02`, so `n ≥ (1.96/0.02)² × 0.1625 × 0.8375 / 0.5625 = 9,604 × 0.2419 ≈ 2,324`. The direct question needs `9,604 × 0.05 × 0.95 ≈ 457`. About 5 times more.
5. A study that cannot detect the effect it asks about produces no knowledge to set against the risks and time it imposes. The board must find risks reasonable relative to the knowledge expected, and zero expected knowledge makes any risk unreasonable.

</details>

## Lab / assignment hook

[Lab 10, a randomized response study and its ethics application](../labs/lab10.md). You implement the estimator, its standard error, the privacy level and a sample-size planner, run them on a simulated survey where some players lie to a direct question, and then write the ethics application for your own course project using the section template from section 3. The application is also the ethics section of your course proposal.

## Sources

- Office for Human Research Protections, "Exempt Research Determination" FAQs (hhs.gov, read via the Internet Archive, September 2026): the regulations do not say who determines exemption, and OHRP recommends that investigators not make that determination independently.
- U.S. Code of Federal Regulations, 45 CFR 46 (Common Rule, 2018 requirements), text via Cornell Legal Information Institute, law.cornell.edu/cfr/text/45/part-46 (accessed September 2026). §46.102(e)(1), (e)(4), (j) and (l) definitions; §46.104(b)(3) and (d)(2) to (d)(4) exemptions, including the online-game example in (d)(3)(ii); §46.110 expedited review; §46.111(a) approval criteria; §46.116(a)(5)(i), (b) and (f)(3) consent and waiver; §46.117(c) waiver of signed consent.
- Old School RuneScape Wiki, "Real world trading" and "Code of Conduct" (accessed September 2026). Real-world trading forbidden under the Rules of RuneScape, with bans as the penalty; definition clarified by Jagex on 9 April 2025.
- Warner, S. L. (1965). "Randomized Response: A Survey Technique for Eliminating Evasive Answer Bias." *Journal of the American Statistical Association* 60(309), 63-69. https://doi.org/10.1080/01621459.1965.10480775
- Tourangeau, R. & Yan, T. (2007). "Sensitive Questions in Surveys." *Psychological Bulletin* 133(5), 859-883. https://doi.org/10.1037/0033-2909.133.5.859
- Lensvelt-Mulders, G. J. L. M., Hox, J. J., van der Heijden, P. G. M. & Maas, C. J. M. (2005). "Meta-Analysis of Randomized Response Research." *Sociological Methods & Research* 33(3), 319-348. https://doi.org/10.1177/0049124104268664. Six validation studies (incorrect answers 0.38 with randomized response, 0.49 otherwise) and 32 comparative studies.
- Erlingsson, Ú., Pihur, V. & Korolova, A. (2014). "RAPPOR: Randomized Aggregatable Privacy-Preserving Ordinal Response." *Proceedings of ACM CCS 2014*, 1054-1067. https://doi.org/10.1145/2660267.2660348
- Google Online Security Blog, "Learning statistics with privacy, aided by the flip of a coin" (30 October 2014). The forced-"yes" coin description and the Chrome test on settings hijacking.
- Dwork, C. & Roth, A. (2014). "The Algorithmic Foundations of Differential Privacy." *Foundations and Trends in Theoretical Computer Science* 9(3-4), 211-487. https://doi.org/10.1561/0400000042. Randomized response as `ln 3`-differential privacy.
- Regulation (EU) 2016/679 (GDPR), Article 89(1), via gdpr-info.eu (accessed September 2026). Safeguards for research processing, including data minimization and pseudonymization.
- Boellstorff, T., Nardi, B., Pearce, C. & Taylor, T. L. (2012). *Ethnography and Virtual Worlds: A Handbook of Method*. Princeton University Press. Chapter 8, "Ethics" (pp. 129-150) and chapter 9, "Human Subjects Clearance and Institutional Review Boards" (pp. 151-158); pages from the Crossref chapter records (doi:10.1515/9781400845286).
- The gold-buying share, sample sizes, the share of buyers who lie, and the in-class study plan are invented for teaching.

## Interactive spec: examples/w10-randomized-response.html

**The one insight.** Randomized response trades a bias you cannot fix for variance you can buy down with sample size. The left view shows how little one answer reveals as `t` drops. The right view shows the direct question's narrow interval sitting in the wrong place while the randomized interval is wide and centered on the truth.

**Layout.** Controls on top at 390px, on the left at 1280px. Two panels side by side at 1280px, stacked at 390px: "What one answer reveals" and "What the study learns". A readout table under both.

**Controls (keyboard operable, with visible numeric values).**
- True share `π`: 0.01 to 0.50, step 0.01, default 0.10.
- Truth probability `t`: 0.05 to 1.00, step 0.05, default 0.50.
- Honesty under direct questioning `h` (share of buyers who admit it when asked directly): 0 to 1, step 0.05, default 0.50. Non-buyers always answer "no".
- Sample size `n`: log slider 100 to 100,000, default 2,000.
- "Simulate one survey" button: draws `n` respondents with a seeded PRNG (seed displayed), applies both methods, and marks the simulated estimates as hollow dots next to the expected ones.

**Left panel, "What one answer reveals".** Three vertical bars on a 0-100% axis: prior `π`; P(bought given "yes") `= π(t + (1 − t)/2) / q`; P(bought given "no") `= π(1 − t)/2 / (1 − q)`. Label each with its value to one decimal place. Under the bars, the odds factor `(1 + t)/(1 − t)` and `ε = ln((1 + t)/(1 − t))` (show "none" at `t = 1`).

**Right panel, "What the study learns".** Horizontal axis: `n` on a log scale, 100 to 100,000. Vertical axis: estimated share, 0 to `max(0.6, π + 0.2)`. A horizontal dashed line at the true `π`. Two bands: direct question, center `h × π`, half-width `1.96 × sqrt(hπ(1 − hπ)/n)`; randomized response, center `π`, half-width `1.96 × sqrt(q(1 − q)/n)/t`. Distinguish bands by fill pattern as well as color. A vertical cursor line at the current `n`.

**Readout.** `q`, randomized SE, direct SE, direct bias `(h − 1)π`, root-mean-square error of each method `sqrt(bias² + SE²)`, the `n` at which the randomized RMSE first drops below the direct RMSE (or "never" when `h = 1`), and the sample-size multiplier `(SE_rr / SE_direct_honest)²`.

**Test values (the builder must check these).**
- `π = 0.10, t = 0.5, n = 2000`: `q = 0.30`, randomized SE 0.0205, P(bought given "yes") 25.0%, P(bought given "no") 3.6%, `ε = 1.10`, multiplier 9.33.
- `t = 0.75`, same `π` and `n`: `q = 0.20`, SE 0.0119, P(bought given "yes") 43.8%, `ε = 1.95`.
- `t = 0.25`: `q = 0.40`, SE 0.0438, P(bought given "yes") 15.6%, `ε = 0.51`.
- `h = 0.5, t = 0.5, n = 2000`: direct center 0.05, direct SE 0.0049, direct RMSE 0.0502, randomized RMSE 0.0205.
- `h = 0.5, t = 0.5, π = 0.10`: the two RMSEs are exactly equal at `n = 317`, so the crossover readout (the smallest `n` at which the randomized RMSE is strictly lower) says 318. Formula: `n > (q(1 − q)/t² − hπ(1 − hπ)) / ((1 − h)π)² = 317`.
- `h = 1`: the "RMSE crossover" readout says "never".

**Accessibility and style.** Use `templates/interactive-tokens.css`. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Numbers selectable for copying. No game logos, art or characters; the game is named in text only.
