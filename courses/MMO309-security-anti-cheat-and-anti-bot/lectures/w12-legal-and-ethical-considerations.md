# MMO309 · Week 12 — Legal and Ethical Considerations

**Why this matters:** Anti-cheat work gives a studio unusual power over its players. You read what runs on their computers, you decide alone whether they are guilty, and you take away accounts they may have paid for over a decade. The law limits some of that power, and ethics has to limit the rest. A defender who ignores either one ends up banning innocent people, shipping software that attackers reuse, or losing in court.

**You will be able to:**
- Compute the probability that a flagged player is cheating from a base rate and a set of detection signals, using likelihood ratios.
- Derive the confidence a sanction requires from the relative cost of wrongly punishing an innocent player, and apply it to a sanction ladder.
- Evaluate a client-side anti-cheat design against data minimization and against the risk that attackers reuse it.
- Explain what recent lawsuits against cheat makers achieved and what they did not.

**Before class:** GDPR (Regulation (EU) 2016/679), Articles 5 and 22, about two pages together. Trend Micro Research, "Ransomware Actor Abuses Genshin Impact Anti-Cheat Driver to Kill Antivirus" (24 August 2022), about 15 minutes. Hoglund & McGraw, *Exploiting Online Games* (2007), the chapter on the legal and ethical questions around cheating. This lecture is about design choices, not legal advice. Laws differ by country, and your studio's lawyers decide what applies.

**Prerequisites from earlier courses:** [MMO402 week 5, rules, EULAs and terms of service](../../MMO402-emergent-society-governance-and-ethics/lectures/w05-rules-eulas-and-terms-of-service.md) (the contract layer, and *MDY v. Blizzard*). [MMO402 week 7, justice systems](../../MMO402-emergent-society-governance-and-ethics/lectures/w07-justice-systems-reports-reviews-appeals.md) (review panels, appeals and correlated reviewers). [MMO402 week 12, research ethics in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md). [MMO305 week 9, toxicity research and interventions](../../MMO305-social-systems-and-online-behaviour/lectures/w09-toxicity-research-and-interventions.md) (precision and the base rate). From this course, [week 2, never trust the client](w02-never-trust-the-client.md), [week 5, client integrity](w05-memory-editing-and-client-integrity.md), and [week 11, exploit response](w11-exploit-response-rollback-vs-ban.md).

**Interactive:** [examples/w12-how-sure-to-ban.html](../examples/w12-how-sure-to-ban.html).

---

## 1. Four sets of rules that reach anti-cheat

Four different bodies of rules touch the work you have done in this course. Each one asks a different question.

**Contract.** Your terms of service say what players may not do and what you may do in response. MMO402 week 5 showed how little of that contract players read. For anti-cheat, the contract is where you reserve the right to scan, to suspend and to terminate. A clause is not the same as fairness. It gives you the legal right to act, and it tells players very little about how you will use it.

**Intellectual property and anti-circumvention.** Studios sue the people who make and sell cheats, usually for copyright infringement and for breaking anti-circumvention law such as the US Digital Millennium Copyright Act (DMCA). MMO402 week 5 covered *MDY Industries v. Blizzard* (9th Cir., 2010), in which the appeals court held that selling Glider, a tool built to get past Warden, violated the DMCA's anti-circumvention rules. Section 4 below looks at later cases, and [week 14](w14-case-studies.md) scores the lawsuit route as a lever.

**Privacy and data protection.** Anti-cheat collects data about players: their inputs, their hardware, sometimes the processes on their machines. In the European Union the General Data Protection Regulation (GDPR) sets principles for any processing of personal data. Two are central here. Data minimization says you may keep only data that is adequate, relevant and limited to what the purpose needs. Storage limitation says you may not keep identifiable data longer than that purpose needs. Article 22 gives people a right not to be subject to a decision based solely on automated processing that has legal effects on them or similarly significant effects. Where an exception applies, the controller must still offer human intervention, a chance to express a view, and a way to contest the decision. Whether a game ban counts as "similarly significant" is not settled, and lawyers disagree. A designer does not need to settle it. Build systems that could meet the standard, and you are safe either way.

**Security ethics.** Some duties come from no statute. If your anti-cheat runs with the highest privileges on a player's computer, you have made it part of their security. A flaw in your driver is a flaw in their machine. Section 3 shows what happened when that went wrong.

Two of these sets of rules, contract and anti-circumvention, mostly empower the studio. The other two, data protection and security ethics, mostly constrain it. This lecture spends most of its time on the constraints, because that is where designers make choices.

## 2. Worked example: how sure do you need to be?

### The hook

In November 2006, Blizzard banned a large number of World of Warcraft accounts in an action against cheating. Some of the banned players had done nothing wrong. They played on Linux through Cedega, a compatibility layer, and the detection mistook it for a cheat. Blizzard investigated with the Cedega developers, reinstated the accounts, apologized, and credited each one with twenty days of free play.

Look at what Blizzard did afterward. It put a price on the error: twenty days of play plus an apology. That price tells you how the studio weighed wrongly banning an innocent player against missing a cheater, at least after the fact. This worked example makes that weighing explicit and does it before the ban, not after.

### The model

Two ideas, both from probability you already know.

**Evidence updates odds.** Let `π` be the base rate, the share of players who cheat. Express belief as odds, `odds = P / (1 − P)`. Each detection signal has a true positive rate `TPR` (the share of cheaters it flags) and a false positive rate `FPR` (the share of honest players it flags). Its **likelihood ratio** is `LR = TPR / FPR`. When a signal fires:

```
posterior odds = prior odds × LR
P(cheat)       = odds / (1 + odds)
```

If signals are independent given the truth, each one multiplies the odds in turn. That condition matters, and we return to it below.

**The sanction sets the bar.** Suppose wrongly sanctioning an innocent player costs `C` times as much as letting one cheater go unpunished. Sanctioning a player with probability `P` of cheating has expected cost `(1 − P) × C`. Not sanctioning has expected cost `P × 1`. Sanction when the first is smaller:

```
sanction if   P(cheat) ≥ C / (C + 1)
```

This is [week 8](w08-machine-learning-for-detection-overview.md)'s threshold rule seen from one player. Flagging where the likelihood ratio exceeds `C × (1 − π) / π` is the same test as `P(cheat) ≥ C / (C + 1)`. Week 8 used one `C` to set one threshold. Here each sanction gets its own `C`.

`C` is not a measured number. It is a value judgment, and it should grow with the severity and irreversibility of the sanction. A 24-hour trade lock that auto-expires costs an innocent player little, so `C` might be 1. A permanent ban of a paid account with years of play is severe and slow to undo even on appeal, so `C` might be 20.

- `π` base rate of cheating in the population you scan
- `TPR`, `FPR` a signal's true and false positive rates; `LR = TPR / FPR`
- `C` cost of wrongly sanctioning an innocent, in units of one missed cheater
- `C / (C + 1)` the confidence the sanction requires

### Numbers you can check

The rates below are invented for teaching. The base rate is 1%. Three signals are available: an aim-snap detector on server-side telemetry (flags 90% of cheaters and 1% of honest players), three or more independent player reports (50% and 5%), and a match between a file on the player's machine and a known cheat program (60% and 0.1%). The sanction ladder has three rungs with `C` of 1, 5 and 20, so the thresholds are 0.5, 0.833 and 0.952.

```python
prior = 0.01                                   # share of accounts that cheat
signals = [("aim-snap detector", 0.90, 0.010),   # (name, true positive rate, false positive rate)
           ("3+ player reports", 0.50, 0.050),
           ("known cheat file hash", 0.60, 0.001)]
sanctions = {"24 h trade lock": 1, "7-day suspension": 5, "permanent ban": 20}
# cost of sanctioning one innocent player, in units of one cheater left unpunished

odds = prior / (1 - prior)
print(f"{'evidence':26}{'LR':>6}{'P(cheat)':>10}  sanctions allowed")
for name, tpr, fpr in [("prior only", 1, 1)] + signals:
    odds *= tpr / fpr
    p = odds / (1 + odds)
    allowed = [s for s, c in sanctions.items() if p >= c / (c + 1)]
    print(f"{name:26}{tpr / fpr:>6.0f}{p:>10.4f}  {', '.join(allowed) or 'none'}")
```

It prints:

```
evidence                      LR  P(cheat)  sanctions allowed
prior only                     1    0.0100  none
aim-snap detector             90    0.4762  none
3+ player reports             10    0.9009  24 h trade lock, 7-day suspension
known cheat file hash        600    0.9998  24 h trade lock, 7-day suspension, permanent ban
```

Check the second row by hand. Prior odds are `0.01 / 0.99 = 0.0101`. Times 90 gives `0.909`. `P = 0.909 / 1.909 = 0.476`. A detector that is right about 99% of honest players, taken alone, leaves you less than 50% sure. It does not justify even the 24-hour lock.

Check the third row. `0.909 × 10 = 9.09`, so `P = 9.09 / 10.09 = 0.901`. That clears 0.5 and 0.833 but not 0.952. You may suspend but not permanently ban.

Now apply the same rules to a population of a million players, 10,000 of them cheating. Each rule sanctions only players on whom every listed signal fired.

```python
players, prior = 1_000_000, 0.01
cheaters = players * prior
honest = players - cheaters
rules = {"aim-snap alone": [(0.90, 0.010)],
         "aim-snap + reports": [(0.90, 0.010), (0.50, 0.050)],
         "all three signals": [(0.90, 0.010), (0.50, 0.050), (0.60, 0.001)]}
print(f"{'rule':20}{'cheaters caught':>16}{'innocents hit':>15}{'precision':>11}")
for name, sig in rules.items():
    tp, fp = cheaters, honest
    for tpr, fpr in sig:
        tp, fp = tp * tpr, fp * fpr
    print(f"{name:20}{tp:>16,.0f}{fp:>15,.1f}{tp / (tp + fp):>11.2%}")
```

It prints:

```
rule                 cheaters caught  innocents hit  precision
aim-snap alone                 9,000        9,900.0     47.62%
aim-snap + reports             4,500          495.0     90.09%
all three signals              2,700            0.5     99.98%
```

Precision here is the same number as `P(cheat)` above, seen across a population instead of for one player. The rows show the price of confidence. Requiring all three signals cuts innocent sanctions from 9,900 to about one every two waves, and it also lets 7,300 of the 10,000 cheaters through. The sanction ladder resolves this. Use the weak evidence for cheap, reversible actions on many players. Keep the permanent ban for the few cases with overwhelming evidence.

### A visual you can move

Open the interactive. The left view is an evidence ladder: a vertical probability axis from 0 to 1 on a logit scale, with a marker that climbs as you switch signals on. The right view shows the sanction ladder as three horizontal threshold lines at `C / (C + 1)`, each lit when the marker is above it. Under both, a population strip of 1,000 icons, one per thousand players, shows cheaters caught and innocents hit for the current combination. Slide the base rate from 1% down to 0.1% and watch the marker fall below every threshold even with two signals on. Slide `C` for the permanent ban from 20 to 100 and watch its line rise out of reach. The picture makes one point: whether an action is justified depends on three things you choose (the base rate of the population you scan, the evidence you require and the sanction you apply), and a single accuracy number decides nothing.

### Cross-context recognition

**Criminal and civil law.** Blackstone's formulation in the 1760s, that it is better for ten guilty people to escape than for one innocent to suffer, is `C = 10` in this model, a threshold of `10 / 11 ≈ 0.91`. Civil courts in common-law countries decide most disputes on the balance of probabilities, which is `C = 1` and a threshold of 0.5. The law already runs a sanction ladder: the harsher the penalty, the higher the standard of proof.

**Medical screening.** A cheap, sensitive screening test is followed by a more specific confirmatory test before anyone is treated for a serious condition. The screen is the aim-snap detector. The confirmatory test is the file hash. Doctors do not act on the screen alone for the same reason you should not ban on the detector alone: at a low base rate, most positives of a good screen are false.

**World of Warcraft, 2006.** The Cedega incident is what happens when a signal is treated as if its `LR` were enormous but it has a hidden failure mode shared by a whole group of honest players. Every Cedega user produced the same false match, so for that group the false positive rate was close to 1, not close to 0. That is why the model's independence assumption must be checked, not assumed. [Week 11](w11-exploit-response-rollback-vs-ban.md) turns the same incident into a checklist to run before any mass sanction.

**MMO402 week 7, correlated reviewers.** When review panel members see the same misleading evidence, their votes are not independent, and a unanimous panel is weaker than it looks. Signals behave the same way. Player reports are often triggered by the same high kill count that fired the aim-snap detector, so multiplying their likelihood ratios counts one piece of evidence twice.

### Eyes-open design judgment

- **Choose `C` for each sanction in writing, before you need it.** It is a value judgment about your players. Written down, it can be debated and audited. Left implicit, it drifts toward whatever keeps the ban queue short.
- **Match reversibility to evidence.** Weak evidence justifies actions that expire on their own (trade locks, queue restrictions, extra verification). The permanent ban should require independent strong evidence and, for anything that looks like Article 22 territory, a human review with a route to contest.
- **Test independence on labelled data.** For each pair of signals, compare how often they fire together on known honest players with the product of their separate rates. If they fire together far more often, combine them into one signal with one likelihood ratio.
- **Watch the base rate.** Run the same detector on a population with a lower cheating rate (new accounts in a region with few cheaters, or a casual queue) and precision falls. Rules tuned on a competitive ladder can misfire elsewhere.
- **Notice where the strongest evidence came from.** In the example, the signal that made a permanent ban justified was a scan of the player's own files. The next section asks what that scan costs.

### Check yourself (worked example)

1. With the lecture's signals, what base rate would make the aim-snap detector alone clear the 24-hour trade lock threshold?
2. A studio sets `C = 50` for permanent bans. Which combination of the three signals, if any, still clears the bar at a 1% base rate?

<details>
<summary>Answers</summary>

1. The lock needs `P ≥ 0.5`, which means posterior odds of at least 1. With `LR = 90`, prior odds must be at least `1/90`, so `π ≥ 1/91 ≈ 1.1%`. At a 1% base rate the detector alone falls just short.
2. The threshold is `50 / 51 ≈ 0.980`. All three signals give `0.9998` and clear it. Aim-snap plus file hash gives odds `0.0101 × 90 × 600 = 545`, so `P ≈ 0.998`, which also clears it. Aim-snap plus reports (0.901) does not.

</details>

## 3. The privacy bargain of client-side anti-cheat

Week 2 of this course taught you never to trust the client, and week 5 looked at how cheats edit a client's memory. The server can validate movement, damage and trades. It cannot see a program that reads the game's memory to draw enemies through walls. To see that, anti-cheat has to look at the player's machine. How deeply it looks is a design choice with ethical weight.

Three points on the spectrum, each from a shipped game:

**User-mode scanning (World of Warcraft's Warden, from about 2005).** Warden scanned parts of the memory of processes running on the player's computer and compared hashes of what it found with hashes of known cheat programs. Blizzard's terms asked players to consent to this. Privacy advocates objected when it became public, because the scan touched processes unrelated to the game and could in principle meet personal information.

**Kernel-mode, loaded at boot (Riot Vanguard).** Riot describes Vanguard as its game security software, with a client and a kernel-mode driver. Riot says it usually loads at boot, and League of Legends and VALORANT require it to be running. A kernel driver runs with the highest privilege on the machine, which lets it see cheats that hide from ordinary programs. It also means any flaw in it is a flaw in the operating system's most trusted layer.

**The failure case (Genshin Impact's driver, 2022).** Trend Micro reported in August 2022 that a ransomware group had used `mhyprot2.sys`, the kernel driver of Genshin Impact's anti-cheat, to kill antivirus processes before deploying ransomware. The driver carried a valid code signature, so Windows loaded it without warnings. The researchers stressed that the game did not need to be installed on the victim's machine. The attackers brought the driver with them. A tool built to protect a game became a tool for attacking computers that had never run the game.

Put the three into the terms of section 2. Deeper client access raises the likelihood ratio of your strongest signals. A file-hash or memory-integrity match can have a false positive rate far below any behavioral detector. It also raises the cost of your own mistakes and of attacks on your software, and those costs fall on people who are not cheating.

Design principles that follow from GDPR Article 5 and from security practice:

- **Collect the conclusion, not the evidence.** Report "known cheat signature 4127 present" instead of uploading a list of every process running. That is data minimization in practice.
- **Scan for a purpose and only while it applies.** A scanner that runs only while the game runs has a narrower footprint than one that runs from boot. If you need boot-time loading, say why in plain language.
- **Keep what you collect for as long as the appeal window, then delete it.** That is storage limitation, and it also limits what a breach can expose.
- **Treat your driver as security-critical software.** Minimize what it exposes to user mode, get it reviewed, run a bug bounty for it (week 13), and plan how you would revoke a vulnerable version. The Genshin case shows that the old signed version stays useful to attackers after you patch it.
- **Prefer server-side signals where they suffice.** Speed hacks, teleports, duplication and impossible trades (weeks 3 and 4) are all visible from the server. Reach into the client only for cheats the server cannot see.

## 4. Suing cheat makers

Bans act on players. Lawsuits act on the businesses that sell cheats. Two cases show what that route can and cannot achieve.

**Blizzard v. Bossland (US, 2017).** Blizzard sued Bossland, a company that sold cheat and bot software for several Blizzard games, for copyright infringement and DMCA violations. Bossland did not respond to the suit, and in April 2017 the court granted Blizzard a default judgment of about $8.5 million, based on roughly 42,818 counts of infringement, and barred Bossland from selling its hacks in the United States.

**Bungie v. Phoenix Digital Group (AimJunkies) (US, 2024).** Bungie sued the operators of the AimJunkies cheat site over Destiny 2 cheats in 2021. In May 2024 a jury found that the defendants had infringed Bungie's copyrights and awarded Bungie $63,210. Reporting at the time described it as possibly the first time a jury had found that a cheat maker infringed a game company's copyright.

Read the two numbers side by side. The large award came from a defendant who never showed up. The contested jury trial produced a small one. A judgment is worth only what you can collect, and a company in another country that ignores the case may never pay. What the cases did produce was a public legal record that selling cheats carries risk, and that is aimed at the business model, the same place week 10 aimed its graph.

Two ethical points for designers:

- **Aim legal pressure at sellers, not at players.** Suing a teenager who bought a cheat for twenty dollars is legal in some places and a public-relations disaster everywhere. Bans are the proportionate tool for players.
- **Do not let the lawsuit shape the detection.** If lawyers ask for evidence, your logs may be read in court. Log what the purpose needs and nothing more, and assume that anything you keep will be seen by a judge.

## 5. The defender's own conduct

Security teams sometimes use deception: honeypot items that only a cheat client would pick up, fake data sent to suspected cheat clients, delayed bans that let a cheater keep playing while you watch. These tools can be legitimate. Each one has a cost to someone other than the cheater.

- **Delayed bans** keep a known cheater in matches with honest players. [Week 5](w05-memory-editing-and-client-integrity.md) showed the benefit. The cost is paid by the players they meet. Make the delay no longer than the model says it needs to be, and prioritize removing cheaters from ranked play.
- **Honeypots** must be invisible to honest players, or you have built a trap for your customers. If an honest player could plausibly trigger it (an accessibility tool, a macro your own rules allow), it is not a honeypot, it is a false positive.
- **Studying cheaters** is research on people. The questions from MMO402 week 12 apply: what data you use, who approves it, and whether you publish anything that identifies individuals.
- **Minors** play your game and some of them cheat. A permanent ban on a child's account, with a family's purchases on it, deserves a higher `C` and a route for a parent to be heard. MMO402 week 11 covers minors in online worlds.

## In-class activity (25 minutes)

Pairs. Each pair receives a one-page design brief for a new anti-cheat feature (four different briefs rotate around the room): a boot-time kernel driver, a screenshot uploader that sends a capture when a detector fires, a mouse-movement recorder for aim analysis, or a friend-graph analysis that flags accounts linked to banned ones.

1. Write down what data the feature collects, where it is stored and for how long. (5 minutes)
2. Estimate its likelihood ratio in words (weak, moderate, strong) and say which sanction rung it could justify alone and with one other signal. (8 minutes)
3. Name the worst plausible harm to an innocent player, including if the feature were compromised by an attacker. (7 minutes)
4. Propose one change that keeps most of the detection value and reduces that harm. (5 minutes)

Expected output: a four-line data inventory, a sanction mapping, one harm and one mitigation.

## Common misconceptions

- **"Our detector is 99% accurate, so a flagged player is 99% likely to be cheating."** At a 1% base rate a detector with a 1% false positive rate and 90% recall gives 47.6%. Accuracy on honest players is not the chance that a flagged player cheats.
- **"If the terms of service allow it, it is fine."** The contract gives you a right. It does not make a scan proportionate, an automated ban fair, or a vulnerable driver safe.
- **"More signals always help."** Only independent ones. Correlated signals inflate your confidence without adding evidence, and the Cedega case shows a signal can fail for a whole group at once.
- **"Winning a lawsuit ends a cheat business."** The biggest award in section 4 came from a default judgment against a company that did not appear. Legal action raises the cost of selling cheats. It does not collect itself.

## Check yourself

1. A new behavioral detector has `TPR = 0.8` and `FPR = 0.002`. At a 0.5% base rate, what is `P(cheat)` for a flagged player? Which rungs of the lecture's ladder does it justify alone?
2. Your team wants to add "was on a friends list with a banned player" as a signal with `LR = 5`. Give one reason it may not be independent of your other signals and one ethical objection to it.
3. A proposed anti-cheat uploads the full list of running processes every time a match starts. Rewrite the design so it meets data minimization while keeping its detection value.
4. Using the population table, how many of 10,000 cheaters does an "all three signals" permanent-ban rule let through? How would you still act against them without permanent bans?

<details>
<summary>Answers</summary>

1. `LR = 400`. Prior odds `0.005 / 0.995 = 0.005025`. Posterior odds `2.01`, `P = 2.01 / 3.01 ≈ 0.668`. That clears the trade lock (0.5) but not the 7-day suspension (0.833) or the permanent ban (0.952).
2. Friends of cheaters are more likely to be reported by the same opponents and to play in the same matches, so the signal is correlated with reports and with match-based detectors. Ethically, it punishes people for their associations rather than their actions, and it hits siblings, school friends and new players who accepted a random friend request.
3. Check on the client against a list of known cheat signatures and upload only the IDs of signatures that matched, not the process list. Run the check only while the game runs, sign and version the signature list, and delete match results after the appeal window.
4. `10,000 − 2,700 = 7,300` get through. Use the lower rungs: suspensions for those with two signals, trade locks and ranked restrictions for those with one, and a queue that matches repeatedly flagged players with each other while evidence accumulates, which protects honest players without a permanent sanction.

</details>

## Lab / assignment hook

[Lab 12, a sanction policy with an error budget](../labs/lab12.md). You receive a generator for 200,000 labelled simulated accounts with the three signals from this lecture. You measure each signal's rates, test whether pairs are independent (one pair is not), set `C` for a four-rung sanction ladder in writing, and report the expected innocent sanctions per million players at each rung. Deliverable: your script, the policy table and a 400-word policy memo that a lawyer and a community manager could both read. The policy also feeds the threat model assessment.

## Sources

- Linuxlookup, "Blizzard Unbans Linux World of Warcraft Players", 22 November 2006, reproducing Blizzard's letter to players (archived by the Internet Archive, August 2008). Cedega users banned in error, reinstated with a two-week credit plus locked time, twenty days in total.
- Regulation (EU) 2016/679 (GDPR), Article 5(1)(c) and (e) (data minimization, storage limitation) and Article 22 (automated individual decision-making, exceptions, and the safeguards of human intervention, expressing a view and contesting the decision). Text via gdpr-info.eu, retrieved September 2026.
- Riot Games Support, "What is Vanguard?" (retrieved September 2026). Custom game security software with a kernel-mode driver, usually loaded at boot, required by League of Legends and VALORANT.
- Trend Micro Research, "Ransomware Actor Abuses Genshin Impact Anti-Cheat Driver to Kill Antivirus", 24 August 2022. Abuse of the signed `mhyprot2.sys` driver in late July 2022; the game did not need to be installed.
- Wikipedia, "Blizzard Entertainment", section "Warden client" (retrieved September 2026), citing Play.tm, "WoW's Warden stirs controversy", 8 November 2005. Warden's hashing of scanned process memory, consent in the terms of service, and privacy objections.
- McAloon, A., "Blizzard awarded $8.5M in damages following copyright infringement lawsuit", Gamasutra (now Game Developer), 4 April 2017. Default judgment against Bossland, about 42,818 counts of infringement, sales barred in the US.
- Wikipedia, "Cheating in online games" (retrieved September 2026), and The Verge, "A jury hands Bungie a victory in a landmark anti-cheating decision", 25 May 2024. Jury verdict for Bungie against Phoenix Digital Group (AimJunkies), $63,210, suit filed 2021.
- Wikipedia, "Blackstone's ratio" (retrieved September 2026). The ten-to-one formulation from Blackstone's *Commentaries on the Laws of England* (1760s) and its role in legal thinking.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley.

## Interactive spec: examples/w12-how-sure-to-ban.html

**The one insight:** whether a sanction is justified depends on the base rate, the combination of evidence and the severity of the sanction together. A single "accuracy" number decides nothing, and the same evidence can justify a trade lock but not a ban.

**Layout.** Left panel (evidence ladder), right panel (sanction ladder), population strip below both, controls under that. Stacked on mobile in the order evidence, sanction, strip, controls.

**Model (exact).**
```
priorOdds = π / (1 − π)
odds      = priorOdds × Π over enabled signals of (TPR_i / FPR_i)
P         = odds / (1 + odds)
threshold_k = C_k / (C_k + 1)
population (per 1,000,000): TP = 1e6 π Π TPR_i;  FP = 1e6 (1 − π) Π FPR_i
```

**Left panel.** Vertical axis `P(cheat)` on a logit scale with ticks at 0.001, 0.01, 0.1, 0.5, 0.9, 0.99, 0.999, 0.9999. A marker at the current `P`, with a thin trail showing each step as signals are enabled in order (prior, then each enabled signal), labelled with the step's likelihood ratio.

**Right panel.** The same logit axis, aligned with the left, with one horizontal line per sanction at `C_k / (C_k + 1)`. Lines above the marker are dim with the label "not justified". Lines at or below it are solid with the label "justified".

**Population strip.** 1,000 small icons (each 1,000 players) in a 50 × 20 grid. Color counts: cheaters caught, cheaters missed, innocents sanctioned (round up to at least one icon if FP ≥ 1, and show the exact count in text beside the strip), others. Text readout of TP, FP and precision to two decimals.

**Controls (defaults in brackets).** Base rate `π`, log slider from 0.01% to 20% [1%]. Three signal toggles [all off], each with editable TPR and FPR: aim-snap [0.90, 0.010], reports [0.50, 0.050], file hash [0.60, 0.001]. Three `C` sliders, 0.5 to 200 on a log scale: trade lock [1], suspension [5], permanent ban [20]. A checkbox "reports correlated with aim-snap" that, when both are on, replaces the reports LR with 3 (to show double counting).

**Test values (defaults).** Prior only: `P = 0.0100`, nothing justified. Aim-snap on: `P = 0.4762`, nothing justified, TP 9,000, FP 9,900, precision 47.62%. Aim-snap and reports: `P = 0.9009`, lock and suspension justified, TP 4,500, FP 495, precision 90.09%. All three: `P = 0.9998`, all justified, TP 2,700, FP 0.5, precision 99.98%. With `π = 0.1%` and aim-snap plus reports: `P ≈ 0.4739`, nothing justified. With the correlation checkbox on and aim-snap plus reports: odds `0.0101 × 90 × 3 = 2.727`, `P ≈ 0.7317`, lock only.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. All toggles and sliders keyboard operable with visible labels and values. Status is shown by text as well as color. Respect `prefers-reduced-motion` and `prefers-color-scheme`. No game art or logos.
