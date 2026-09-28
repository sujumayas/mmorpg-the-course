# MMO402 · Exam bank: quiz, practice and viva questions

MMO402 has no written exam. The grade comes from the debate (20%, [debate-brief.md](debate-brief.md)), the case analyses (30%, [case-analyses-brief.md](case-analyses-brief.md)) and the final governance design paper (50%, [final-paper-brief.md](final-paper-brief.md)). This bank does three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Viva and spot checks.** The 10-minute viva on the final paper and the floor questions in the debate draw on questions in this style. Examiners rewrite them with the numbers from your own paper or case file.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model or a case behaves the way it does, with a number or a named mechanism as evidence.
- **design**: choose rules or values that meet a stated goal and show that they meet it.
- **critique**: find what is wrong with a proposal or a claim and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and its version or date. No question relies on a game fact the lectures do not state. Every numeric answer was recomputed in Python. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: Worlds as polities

1. *Week 1 · compute.* A server has `A = −40`, `c = 10` and `S_max = 250`. A patch causes a grievance of `g = 120`, and the developer's responsiveness is `p = 0.25`. (a) Which way of staying is better for a dissatisfied player, and what is it worth? (b) Compute `R`, `r`, and the exit share with and without social ties. (c) By how much can the grievance grow before the server tips into a full cascade?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Voice, worth −100. (b) `R = 60`, `r = 0.24`, 24% leave without ties and 40% with them. (c) About 3.3 points. The cliff is at `g ≈ 123.3`.

(a) Silence is worth `−120`. Voice is worth `−(1 − 0.25) × 120 − 10 = −90 − 10 = −100`. Voice is better.

(b) `R = A − stay = −40 − (−100) = 60`. `r = 60 / 250 = 0.24`. Without ties, exit is `r = 24%`. With ties, `x = (1 − √(1 − 0.96)) / 2 = (1 − 0.2) / 2 = 0.40`.

(c) The cascade starts when `r > 0.25`, so `R > 62.5`. While voice is the better way to stay, `R = −40 + 0.75g + 10 = 0.75g − 30`. Setting `0.75g − 30 = 62.5` gives `g = 123.3`. A grievance 3.3 points larger turns a 40% exodus into 100%. This is the week 1 point that high switching costs hide how close a server is to the edge.
</details>

2. *Week 1 · design.* Use the lecture's default world (`A = −60`, `c = 5`, `S_max = 200`) and a grievance of `g = 100`. The studio wants no more than 10% of the server to leave once social ties are counted. What is the lowest responsiveness `p` that achieves this? Name two concrete voice channels that could plausibly raise perceived `p` that far, and one cost of each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = 0.27`.

Work backwards from the coupled formula. The exit share `x` satisfies `x(1 − x) = r`. For `x = 0.10`, `r = 0.1 × 0.9 = 0.09`, so `R = 0.09 × 200 = 18`.

With voice as the way to stay, `R = A + (1 − p)g + c = −60 + 100(1 − p) + 5`. Set it to 18: `100(1 − p) = 73`, so `p = 0.27`. Check that voice beats silence: `p × g = 27 > c = 5`, so it does.

Check forward: at `p = 0.27`, voice is worth `−73 − 5 = −78`, `R = 18`, `r = 0.09`, and `x = (1 − √0.64)/2 = 0.10`. At `p = 0.26` the share rises to 10.6%.

Channels, with costs: a public roadmap with dated developer replies to top requests (staff time, and a commitment that is visible when broken); an advisory council like the CSM (travel and NDA overheads, and the week 3 risk that organized blocs capture it); randomly sampled surveys with published results (survey design and the expectation that results are acted on). Any two with a real cost are acceptable.
</details>

3. *Week 1 · critique.* A producer says: "Monthly churn has been 2% for a year and our forums are quiet. Players are happy with the direction of the game." Using the exit-voice model, give two readings of these numbers that are not "players are happy", and name the data you would look at to tell them apart.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Quiet forums and low churn fit a trapped server as well as a happy one.

Reading 1, high switching costs. A large `S_max` keeps `r = R / S_max` small even when the grievance `R` is large, so few leave. The model's silent players have the same grievance as the vocal ones. Low churn here measures how much players have to lose, not how satisfied they are.

Reading 2, `p` has fallen to zero. If players have learned that the developer never changes course, voice is worth less than silence (`p × g < c`), so they stop posting. A quiet forum can mean players no longer believe voice works. That is the dangerous state in the lecture's misconceptions, because the next increase in grievance can cross `r > 0.25` with no warning.

Data to separate them: session length and days played per week (falling while churn stays flat suggests silent grievance), new-character creation, guild merges and whole guilds leaving together (the cluster signal from the eyes-open list), and a survey question on whether players believe feedback changes decisions (a direct estimate of perceived `p`).
</details>

4. *Week 1 · explain.* In an invented survival MMO, classify each rule by Lessig's four modalities and say who controls it. (a) Houses cannot be built within 50 metres of a spawn point. (b) The code of conduct bans posting another player's real name. (c) Guilds refuse to trade with members who have stolen from a partner guild. (d) Teleporting between cities costs 200 gold, and the fee doubles during sieges. Then say which of the four the developer can change in a patch and which it can only influence.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Architecture, developer. (b) Law, developer writes it and moderators enforce it. (c) Norms, players. (d) Market, developer sets the price and players choose.

The developer can patch (a) and (d) directly and can rewrite (b). It can only influence (c), for example by giving guilds tools to publish a blacklist or trade logs that make theft visible. That asymmetry is why the course separates the developer's government from the players' own government.
</details>

## Week 2: Emergent player government

5. *Week 2 · compute.* A guild has `N = 4` officers. Each is a traitor with probability `q = 0.05` and available when needed with probability `a = 0.7`. A hijack costs `H = 200`. (a) Compute `P(hijack)` and `P(timely)` for `K = 1` to `4`. (b) Find the cheapest `K` when lateness costs `L = 5` and when it costs `L = 40`. (c) Where is `N × a`, and how does it relate to your answers?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| K | P(hijack) | P(timely) | cost, L = 5 | cost, L = 40 |
|---|---|---|---|---|
| 1 | 18.549% | 99.19% | 37.14 | 37.42 |
| 2 | 1.402% | 91.63% | 3.22 | **6.15** |
| 3 | 0.048% | 65.17% | **1.84** | 14.03 |
| 4 | 0.0006% | 24.01% | 3.80 | 30.40 |

(a) `K = 1`: `P(hijack) = 1 − 0.95^4 = 0.18549`. `K = 2`, timely: `1 − 0.3^4 − 4 × 0.7 × 0.3^3 = 1 − 0.0081 − 0.0756 = 0.9163`. The others follow from the binomial tail.

(b) With `L = 5`, `K = 3` wins: `200 × 0.000481 + 5 × 0.3483 = 0.096 + 1.742 = 1.84`. With `L = 40`, `K = 2` wins: `200 × 0.014019 + 40 × 0.0837 = 2.80 + 3.35 = 6.15`.

(c) `N × a = 2.8`. Timeliness holds up for `K ≤ 2` and falls steeply at `K = 3`, just past it. When lateness is cheap the rule can afford to go one step past `N × a`. When it is expensive the best `K` stays below it.
</details>

6. *Week 2 · compute.* The guild hall's rent must be paid within a 3-day window. Each of 6 officers is online on a given day with probability 0.4, independently. (a) What is the chance the rent is missed if one designated treasurer must pay it? (b) If any officer can pay it on any of the 3 days? (c) Which of the lecture's principles does this illustrate, and which real battle does the lecture tie it to?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 21.6%. (b) About 0.01%. (c) Duties should be "any of N".

(a) The treasurer misses all three days with probability `0.6^3 = 0.216`.

(b) All six officers miss all three days with probability `0.6^(6 × 3) = 0.6^18 ≈ 0.000102`, about 0.01%.

(c) A duty does no harm if done twice, so the rule should let any one of `N` people do it. The Battle of B-R5RB (January 2014) began when one corporation missed a scheduled sovereignty payment. The independence assumption flatters (b). Officers in one time zone are unavailable together, so a warning before the lapse is still worth building.
</details>

7. *Week 2 · design.* Use the lecture's guild (`N = 5`, `q = 0.1`, `a = 0.6`) and the upkeep-duty costs `H = 100`, `L = 50`. The lecture found `K = 2` best, with cost 12.50. A designer proposes a visible 24-hour delay on the action, during which any member can cancel it. Model the delay as dividing `P(hijack)` by 5 and assume it does not change `P(timely)`. Recompute the cost for `K = 1` to `3`. What is the new best rule, and what does this say about rate limits and delays compared with co-signing?

<details>
<summary>Answer and worked solution</summary>

**Answer:** With the delay, `K = 2` costs 5.98 and is still best, and even `K = 1` (8.70) now beats the old best of 12.50.

| K | cost without delay | cost with delay |
|---|---|---|
| 1 | 41.46 | `100 × 0.40951 / 5 + 50 × 0.01024 = 8.19 + 0.51 = 8.70` |
| 2 | 12.50 | `100 × 0.08146 / 5 + 50 × 0.08704 = 1.63 + 4.35 = 5.98` |
| 3 | 16.73 | `100 × 0.00856 / 5 + 50 × 0.31744 = 0.17 + 15.87 = 16.04` |

The delay attacks the hijack term without touching timeliness, so it lowers the cost of every rule. It helps most where hijack risk dominates, at small `K`. This is the lecture's point that delays, rate limits and co-signing are substitutes. A delay lets you require fewer keys for the same safety, and fewer keys means actions still happen on time. The model's assumption is that the delay does not hurt timeliness. That is plausible for a weekly upkeep and false for an action that must happen within the hour.
</details>

8. *Week 2 · critique.* A new MMO ships guilds with one rank, "officer", that can do everything: withdraw any amount, kick members, disband the guild. Critique this against Ostrom's principles 1, 4 and 5 and against the K-of-N model, and propose three concrete changes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One all-powerful rank forces `K = 1` for every power and gives the guild no tools for accountable monitoring or graduated sanctions.

- **Principle 1, clear boundaries.** Officers see and touch everything, so nothing distinguishes who may use which resource. Fix: per-tab and per-rank bank permissions (the World of Warcraft guild bank model since patch 2.3).
- **Principle 4, accountable monitors.** With no audit log, members cannot check what officers did. Fix: a bank and roster log visible to all members.
- **Principle 5, graduated sanctions.** The only sanction a guild can apply to a bad officer is expulsion, often after the damage. Fix: demotion steps and a withdrawal cap per day.
- **K-of-N.** With `K = 1`, hijack risk is `1 − (1 − q)^N`, 41% for five officers at `q = 0.1`. Fix: 2-of-N or a visible delay for disbanding and large withdrawals, while keeping upkeep payment as "any of N".

A defensible answer may also say the designer could keep `K = 1` on purpose in a sandbox about betrayal, as EVE does, but must say so.
</details>

## Week 3: EVE's Council of Stellar Management

9. *Week 3 · compute.* A 7-seat council is elected by STV with the Droop quota from 24,000 valid ballots. (a) What is the quota? (b) How many seats does a disciplined bloc of 7,000 voters guarantee itself? (c) How many more bloc voters would it need to guarantee a third seat, with the other ballots unchanged?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3,001. (b) 2 seats. (c) 3,203 more voters. The quick answer, 2,003, forgets that the new ballots also raise the quota.

(a) `Q = floor(24,000 / 8) + 1 = 3,000 + 1 = 3,001`.

(b) `floor(7,000 / 3,001) = 2`.

(c) A first estimate is `3 × 3,001 − 7,000 = 2,003`. But those 2,003 new ballots also raise `V` to 26,003, so the quota becomes `floor(26,003 / 8) + 1 = 3,251`, and three quotas need 9,753. Solving properly, the bloc needs `B ≥ 3 × (floor((17,000 + B) / 8) + 1)`, since the other 17,000 ballots stay fixed. At `B = 10,200`, `V = 27,200`, `Q = 3,401`, and three quotas are 10,203, so it is not enough. At `B = 10,203`, `V = 27,203`, `Q = 3,401`, and three quotas are exactly 10,203, so it is enough. The bloc needs 3,203 more voters. Accept 2,003 only if the student says the quota is held fixed. The point of the question is that a bloc's own growth raises the bar it must clear.
</details>

10. *Week 3 · compute.* An electorate has `E = 200,000` accounts, a disciplined bloc `B = 5,000` that always votes, and 10 seats under STV with the Droop quota. (a) How many seats does the bloc guarantee at casual turnout `t = 5%` and `t = 10%`? (b) Find the turnout at which the bloc's guarantee falls from 2 seats to 1, and from 1 to 0.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 3 seats at 5%, 2 seats at 10%. (b) From 2 to 1 above about 11.5%, from 1 to 0 above about 25.6%.

(a) At 5%: `V = 5,000 + 0.05 × 195,000 = 14,750`, `Q = floor(14,750 / 11) + 1 = 1,341`, and `floor(5,000 / 1,341) = 3`. At 10%: `V = 24,500`, `Q = 2,228`, guarantee 2.

(b) Two seats need `2Q ≤ 5,000`, so `Q ≤ 2,500`, so `floor(V / 11) ≤ 2,499`, so `V ≤ 27,499`. That means `t × 195,000 ≤ 22,499`, or `t ≤ 11.54%`. One seat needs `Q ≤ 5,000`, so `V ≤ 54,999`, so `t ≤ 49,999 / 195,000 = 25.64%`.

The bloc is 2.5% of the electorate at every turnout. Its guaranteed share of the council moves from 30% to 0% with other people's turnout alone.
</details>

11. *Week 3 · compute.* A studio considers filling its 10-seat council by lottery from all eligible accounts. A bloc makes up 5% of those accounts. (a) What is the chance the bloc gets at least one seat? (b) At least two? (c) What is its expected number of seats? Compare with question 10(a).

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40.1%. (b) 8.6%. (c) 0.5 seats.

(a) `1 − 0.95^10 = 1 − 0.5987 = 0.401`.

(b) `1 − 0.95^10 − 10 × 0.05 × 0.95^9 = 1 − 0.5987 − 0.3151 = 0.086`.

(c) `10 × 0.05 = 0.5`.

Under STV at 5% casual turnout, the same kind of bloc guaranteed itself 3 seats. Under sortition it expects half a seat, which matches its share of the population. The cost is the one the lecture names: volunteers self-select, members may lack expertise, and a drawn member has no mandate. Sortition fixes the turnout problem and creates a legitimacy problem.
</details>

12. *Week 3 · critique.* A community manager proposes raising the council from 10 to 15 seats "so that no single bloc can dominate". Use the lecture's 5% turnout row (20,700 ballots, a bloc of 6,000) to test the claim. Then say what the change does achieve.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The bloc's share barely moves. It goes from 3 of 10 (30%) to 4 of 15 (26.7%).

With 15 seats, `Q = floor(20,700 / 16) + 1 = 1,293 + 1 = 1,294`, and `floor(6,000 / 1,294) = 4`. The bloc still holds about its share of ballots cast, which is 29%. More seats lower the quota, so smaller organized groups (7% to 10% of ballots) gain seats more easily. Unorganized players gain little, because their problem is turnout, not the quota. The lever that moves seats for them is raising casual turnout, for example voting inside the client and login reminders.
</details>

13. *Week 3 · explain.* Using Scharpf's input and output legitimacy, explain the loop in which an advisory council loses influence. Where would a studio intervene, and what would it publish?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Low output lowers turnout, low turnout hands seats to blocs, a bloc-dominated council has weaker input legitimacy, and the developer gives its advice less weight, which lowers output again.

Intervene on both rows at once. On output, publish agreed summit summaries and credit changes the council won, so players can see results. On input, make voting cheap (in-client ballots, reminders at login) so turnout rises and the council's claim to speak for everyone gets stronger. The NDA makes the output side harder, because voters cannot see most of what members did. That is why the published summary matters.
</details>

## Week 4: Wars, betrayals and meta-gaming

14. *Week 4 · compute.* A heist takes 45 billion ISK. Using the three prices in the lecture's shadow table, give its real-money shadow at the 2005 gold-seller price, at the 2009 EBank cash-out price, and at the 2014 PLEX price range. What does the spread tell you, and does it change the allowed-play verdict?

<details>
<summary>Answer and worked solution</summary>

**Answer:** US$24,750 at 2005 prices. About £702 at the 2009 price. US$1,215 to 1,350 at 2014 prices.

`45 × 550 = 24,750`. `45 × 15.6 = 702`. `45 × 27 = 1,215` and `45 × 30 = 1,350`.

The same ISK shadows amounts that differ by a factor of about 20, depending on the year and on where the price came from (a prohibited gray market in 2005, an official route through PLEX by 2014). The verdict does not change. The four tests ask about means, stakes, target and notice, never about the size of the loss. That is the lecture's point that the test protects the game's frame, not the victim.
</details>

15. *Week 4 · explain.* Apply the four tests (`M`, `S`, `T`, `N`) to each case in an EVE-style world whose rules match CCP's published scam policy. Give the verdict and the failing test. (a) A player joins a corporation on an alt account, earns hangar roles over six weeks, empties the hangar and keeps the loot in the game. (b) The same player then sells the loot for money on a third-party site. (c) A player posts in a trade hub claiming to be a recruiter for a famous alliance, using that alliance's name, to collect "deposits". (d) A player sells a ship through the contract system at ten times the market price to a player created three days ago, in a starter system.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Allowed play. (b) Violation, fails `S`. (c) Violation, fails `T`. (d) Violation, fails `N`.

(a) The alt account and the roles are standard mechanics (`M = 1`), the loot stays in the game (`S = 1`), the target is a corporation of characters (`T = 1`), and the rules announce that corporate theft is possible (`N = 1`). This is the Guiding Hand pattern from 2005.

(b) Selling in-game assets for real money fails `S`. This is the EBank pattern: the theft stood, and the cash-out got the player banned. The depositors' loss is the same in (a) and (b).

(c) Impersonating another character or corporation fails `T` and is bannable, even though the deposit scam itself would otherwise pass.

(d) Abusing a new player's lack of knowledge in the starter systems fails `N`. The same contract offered to a veteran in a trade hub would pass all four tests.
</details>

16. *Week 4 · design.* You run *Harbor*, the lecture's fictional survival sandbox with a premium item bought for real money and sellable in-game for gold. Write an allowed-play policy of at most five lines using the four tests plus at most one extra test. Then rule on these two cases: a mayor who collects wall taxes for three months and leaves with the treasury, and a raid leader who posts a rival mayor's real first name and city in a voice channel during a war.

<details>
<summary>Answer and worked solution</summary>

**Answer (one model policy):**

1. Betrayal, theft and deception using ordinary game mechanics are part of play. We do not reverse them. (`M`, `S`)
2. Buying or selling gold, items or accounts outside the premium-item route is banned. (`S`)
3. Anything aimed at a real person, including their real name, location or accounts elsewhere, is banned, wherever it is posted. (`T`)
4. Impersonating staff or another guild is banned. (`T`)
5. Accounts under 14 days old are protected from trades priced more than 3 times the market average. (`N`, graduated)

Rulings: the mayor passes all four tests, so the theft is allowed play. A strong answer adds interface friction, such as a visible treasury log, so townsfolk accept the risk knowingly. The raid leader fails `T`. The act targets a person, so it is a violation. The policy extends enforcement to off-platform spaces when a player is targeted, because the alternative leaves the victim with no remedy for the harm most likely to follow them home.

Mark on whether each line maps to a named test, whether rulings follow from the policy as written, and whether the student names who the policy protects.
</details>

17. *Week 4 · critique.* A designer proposes: "Any scam in which the victim loses more than 100 billion ISK will be reversed and the scammer banned." Name two historical cases from the lecture whose outcome this rule would change and one it would not. Then name two behaviours the rule would create.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It would change the 2006 bank theft of about 700 billion ISK and the 2009 EBank theft of about 200 billion ISK. It would not change the 2005 Guiding Hand heist (above 30 billion ISK).

Behaviours it creates: thieves split thefts into amounts just under the threshold, and players and support staff argue over how to value a loss (market price, build cost or PLEX shadow). The rule also turns a bright-line test into a loss-based standard, which makes rulings slower and less predictable. It protects large victims and leaves small ones unprotected, which is a choice about whom the line protects and should be stated as one.
</details>

## Week 5: Rules, EULAs and terms of service

18. *Week 5 · compute.* A new player meets three documents in this order: a EULA of 9,000 words, terms of service of 14,000 words and a privacy notice of 7,500 words. (a) How long does each take to read at 250 words per minute, and the whole stack? (b) What share of the stack does a 51-second reader cover, and where does their reading stop? (c) The arbitration opt-out sits at word 2,500 of the terms of service. How many minutes must a reader who starts at the top of the stack spend to reach it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 36, 56 and 30 minutes, 122 in total. (b) 0.70%, inside the EULA. (c) 46 minutes.

(a) `9,000 / 250 = 36`. `14,000 / 250 = 56`. `7,500 / 250 = 30`. Total `30,500 / 250 = 122` minutes.

(b) `0.85 × 250 = 212.5` words, which is `212.5 / 30,500 = 0.70%` of the stack. All 212 words are in the EULA (2.4% of it). The reader never opens the terms of service.

(c) The clause sits at stack position `9,000 + 2,500 = 11,500`, which needs `11,500 / 250 = 46` minutes. Coverage is set by the reader. Reach is set by the writer. Moving a one-line pointer to the top of the first document would reach every reader.
</details>

19. *Week 5 · design.* A studio writes a "key points" summary of 250 words and puts it at the top of its terms. The last point, at word 240, says selling items for money gets your account closed. (a) Does a 51-second reader meet that point? (b) Redesign the summary so that every point is met, and place the real-money rule in at least one other layer. Say which layer and where.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) No. The reader covers 212.5 words, so points past word 212 are missed. (b) Cut the summary to at most 200 words and put the most surprising rules first. Add a just-in-time notice.

The summary is 85% covered (`212.5 / 250`), so the tail is lost, and summaries often put the most consequential rule last. A 200-word summary sits inside the budget.

Layering: the real-money rule also belongs at layer 2, as a just-in-time notice of at most 25 words. One example: "Selling gold or items outside the game breaks our terms and can close your account." It appears in the trade window the first time a player trades above a set value, and on any screen that links out of the game. A code-layer option also exists: trade limits or detection on unbalanced trades. Week 14 shows what that costs.
</details>

20. *Week 5 · explain.* A studio's lawyer proposes suing the maker of a bot for copyright infringement, "because using the bot breaks our EULA, so every copy in memory is infringing". Using *MDY v. Blizzard* (9th Cir. 2010), explain the likely problem with that theory, what did work against the bot maker in that case, and what this says about which of Lessig's modalities carried the enforcement.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The court held that breaking a licence term is infringement only when the term is connected to rights copyright protects, such as copying and distribution. A ban on bots is a promise about how you play, so breaking it is breach of contract. MDY still lost, because Glider was built to get around Warden, Blizzard's anti-cheat program, and trafficking in such a tool violated the DMCA.

The contract alone was a weak weapon. The strong enforcement came from code (Warden), and the law protected the code. For a designer, the lesson is to put anti-cheat rules in architecture where possible and treat the contract as the backstop.
</details>

## Week 6: Moderation at scale

21. *Week 6 · compute.* This is the lecture's in-class scenario. An MMO expects 30,000 reports a day at launch and 12,000 after a month. There are 12 moderators on 7-hour days, and a report takes 2 minutes. The vendor's bands: High (5% of reports, 85% violating), Middle (15%, 35% violating), Low (80%, 2% violating). (a) Compute `C`. (b) For launch week, compare "auto-act High, review Middle, dismiss Low" with "auto-act High and Middle". (c) Repeat the first policy for month two.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `C = 2,520`. (b) The first policy overflows by 1,980 reports a day. The second is stable but wrongly acts on 3,150 players a day. (c) Stable, with 1,140 correct actions, 90 wrong and 192 missed per day.

(a) `C = 12 × 7 × 60 / 2 = 2,520`.

(b) Launch: High is 1,500 reports (1,275 violations, 225 not). Middle is 4,500 (1,575 violations, 2,925 not). Low is 24,000 (480 violations).

- Auto High, review Middle: the load is 4,500 against 2,520, so the backlog grows by 1,980 a day. While the team keeps up with a random 2,520 of the middle band, it catches `2,520 × 0.35 = 882`. Correct actions `1,275 + 882 = 2,157`. Wrong 225. Missed `480 + (1,575 − 882) = 1,173`, plus whatever ages out of the backlog.
- Auto High and Middle: correct `1,275 + 1,575 = 2,850`, wrong `225 + 2,925 = 3,150`, missed 480. Precision `2,850 / 6,000 = 47.5%`.

A better launch plan is an explicit surge policy: review only the top of the middle band up to 2,520 a day and dismiss the rest, so the queue stays stable. The automatic penalty must be light and reversible.

(c) Month two: High 600 (510 violations, 90 not), Middle 1,800 (630 violations, 1,170 not), Low 9,600 (192 violations). The review load is 1,800 against 2,520, which is stable with 720 spare. Correct `510 + 630 = 1,140`, wrong 90, missed 192.
</details>

22. *Week 6 · compute.* A review tier receives 12,600 reports a day. The team is 40 moderators at 7 hours and 1.5 minutes per report. (a) What is `C`, and what is the backlog after 10 days? (b) How long does a new report wait on day 10? (c) How many moderators would clear that backlog within 7 days while keeping up with new reports?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `C = 11,200`, backlog 14,000. (b) 1.25 days. (c) 53 moderators.

(a) `C = 40 × 7 × 60 / 1.5 = 11,200`. The backlog grows by `12,600 − 11,200 = 1,400` a day, so it holds 14,000 after 10 days.

(b) `14,000 / 11,200 = 1.25` days, and still growing.

(c) The team must handle `12,600 + 14,000 / 7 = 14,600` a day. Each moderator handles `7 × 60 / 1.5 = 280`, so `14,600 / 280 = 52.1`. Round up to 53. Afterwards 45 moderators (12,600 capacity) keep pace. A cheaper alternative is to raise `l` for a week, which the lecture calls a surge policy, and audit what it dismisses.
</details>

23. *Week 6 · compute.* A proactive chat scanner reads 5 million messages a day. 0.5% break the rules. The scanner has 85% recall and a 0.2% false-positive rate. How many acceptable messages does it flag each day, and what is its precision? What kind of action should it take, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 9,950 acceptable messages flagged a day. Precision about 68%.

True positives `= 0.85 × 0.005 × 5,000,000 = 21,250`. False positives `= 0.002 × 4,975,000 = 9,950`. Precision `= 21,250 / 31,200 = 68.1%`.

Nearly one flag in three hits an acceptable message. That is the base-rate effect from MMO305 week 9. So the scanner should hide or block the message, which is cheap to reverse, and not penalize the account. The penalty ladder carries the ethical weight the classifier cannot.
</details>

24. *Week 6 · critique.* A quarterly safety report says: "Reports are up 40%, so toxicity is rising. Our appeal reinstatement rate is 26%, so our system is wrong a quarter of the time." Correct both claims and say what the report should track instead.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Neither conclusion follows.

Report volume also rises with player count, with how easy reporting is, and with report abuse such as mass reporting. Track the actioned share and the share of matches with a confirmed violation instead.

A 26% reinstatement rate measures errors among players who appealed. Rightly punished players appeal less often, and some wrongly punished players never appeal. So the rate is neither the overall error rate nor a bound on it. Measure accuracy with a random audit sample reviewed independently, split into cases the system actioned and cases it dismissed. The Xbox 2025 report's 26% (about 85,000 of more than 332,000 appeals) has the same limit.
</details>

## Week 7: Justice systems

25. *Week 7 · compute.* Reviewers have sensitivity `s = 0.85` and false-guilty rate `f = 0.25`. The base rate of guilt among reviewed cases is `b = 0.8`. Compare a 5-reviewer majority (`t = 3`) with a 5-reviewer supermajority (`t = 4`). For each give `P_g`, `P_i`, the conviction rate, and wrongful convictions and wrongful acquittals per 10,000 cases.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Panel | `P_g` | `P_i` | Conviction rate | Wrongful convictions | Wrongful acquittals |
|---|---|---|---|---|---|
| Single reviewer | 0.850 | 0.250 | 73.0% | 500 | 1,200 |
| 5, `t = 3` | 0.973 | 0.104 | 79.9% | 207 | 213 |
| 5, `t = 4` | 0.835 | 0.016 | 67.1% | 31 | 1,318 |

For `t = 4` with innocents: `P_i = 5 × 0.25^4 × 0.75 + 0.25^5 = 0.01465 + 0.00098 = 0.01563`. Wrongful convictions `= 10,000 × 0.2 × 0.01563 = 31`.

For `t = 4` with the guilty: `P_g = 5 × 0.85^4 × 0.15 + 0.85^5 = 0.3915 + 0.4437 = 0.8352`. Wrongful acquittals `= 10,000 × 0.8 × 0.1648 = 1,318`.

The supermajority cuts wrongful convictions by a factor of about 7 and multiplies wrongful acquittals by about 6. The acquittal-to-conviction error ratio moves from about 1:1 to about 42:1.
</details>

26. *Week 7 · design.* Use Crowd A from the lecture (`b = 0.85`, `s = 0.9`, `f = 0.3`). For a permanent ban you want at least Blackstone's ratio (10 wrongful acquittals per wrongful conviction). (a) If you will also accept at most 1,000 wrongful acquittals per 10,000 cases, what is the smallest panel that meets both targets? (b) If the acquittal limit is 500? Use majority or higher thresholds only.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5 reviewers, `t = 4`. (b) 9 reviewers, `t = 7`.

Candidate panels per 10,000 cases:

| Panel | Wrongful convictions | Wrongful acquittals | Ratio |
|---|---|---|---|
| 3, `t = 3` | 40.5 | 2,304 | 57 |
| 5, `t = 4` | 46.2 | 692 | 15.0 |
| 5, `t = 5` | 3.6 | 3,481 | 955 |
| 7, `t = 5` | 43.2 | 218 | 5.1 |
| 7, `t = 6` | 5.7 | 1,272 | 224 |
| 9, `t = 6` | 37.9 | 71 | 1.9 |
| 9, `t = 7` | 6.4 | 450 | 70 |

(a) 3-of-3 meets the ratio but lets 2,304 guilty players go. 4-of-5 meets both targets with 5 reviews per case.

(b) 4-of-5 fails the 500 limit. 6-of-7 fails it too (1,272). 5-of-7 has a ratio of only 5.1. The first panel that meets both is 7-of-9, at 9 reviews per case. Tightening the acquittal limit from 1,000 to 500 nearly doubles the review cost, which is exactly the trade the lecture's eyes-open list asks you to write down.
</details>

27. *Week 7 · compute.* A 7-reviewer panel convicts at `t = 5`, with `f = 0.3` and 15% of cases innocent. (a) What is `P_i` if reviewers are independent? (b) What is it if, with probability `ρ = 0.3`, the whole panel follows a single shared impression? (c) What happens to wrongful convictions per 10,000 cases, and name two design changes that lower `ρ`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.0288. (b) 0.110. (c) From 43 to 165 per 10,000.

(a) `P_i = Σ_{k=5}^{7} C(7, k) 0.3^k 0.7^(7−k) = 0.02500 + 0.00357 + 0.00022 = 0.0288`.

(b) `P_i = ρ × f + (1 − ρ) × P_i(panel) = 0.3 × 0.3 + 0.7 × 0.0288 = 0.090 + 0.020 = 0.110`.

(c) `10,000 × 0.15 × 0.0288 = 43` rises to `10,000 × 0.15 × 0.110 = 165`, almost four times as many. To lower `ρ`, show every reviewer the full context (both sides of the chat, the whole match) and hide other reviewers' votes until each has voted. Avoid a reviewer score that rewards agreement with the crowd.
</details>

28. *Week 7 · compute.* A panel produces 300 wrongful and 7,000 correct convictions per 10,000 cases. Wrongly convicted players appeal with `a_i = 0.7`, rightly convicted ones with `a_g = 0.3`. The appeal reviewer has `s_a = 0.95` and `f_a = 0.25`. Compute wrongful convictions reversed, guilty players wrongly released, total appeals, and the share of appeals from guilty players. What would you tell an appeal team that says "nearly everyone who appeals is guilty"?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 157.5 reversed, 105 guilty released, 2,310 appeals, 90.9% from guilty players.

Reversed `= 300 × 0.7 × (1 − 0.25) = 157.5`, about half of all wrongful convictions. Released `= 7,000 × 0.3 × (1 − 0.95) = 105`. Appeals `= 300 × 0.7 + 7,000 × 0.3 = 210 + 2,100 = 2,310`. Guilty share `= 2,100 / 2,310 = 90.9%`.

The team is right about the share and wrong about what it means. Most appeals come from guilty players because most convicted players are guilty. The appeal still saves about 158 innocent players per 10,000 cases, and those are the errors that damage trust most. Ask instead for an audit of rejected appeals and for the number of wrongful convictions reversed.
</details>

29. *Week 7 · critique.* A studio launches a player-jury system and advertises: "Our juries convict 94% of reported players, proof that reports are accurate." Reviewers get a "justice rating" measured by how often they vote with the majority. Critique both choices using the lecture's model, and say what to measure and report instead.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A conviction rate measures output, not accuracy, and a rating tied to agreeing with the majority raises correlation between reviewers.

The lecture shows that a 94% conviction rate fits two opposite worlds. Careful reviewers (`f = 0.3`) with a guilty-heavy caseload give about 87%. Harsh reviewers (`f = 0.6`) with a 5-reviewer majority give 94.5% while wrongly punishing 1,024 players per 10,000. The number cannot tell them apart.

The justice rating rewards agreeing with the crowd, so reviewers learn to predict the majority, which raises `ρ` and can push a harsh crowd harsher. By Condorcet's theorem, if single reviewers have `f > 0.5`, larger panels make wrongful convictions more likely.

Report audited accuracy instead: a random sample of cases re-reviewed by trained staff, with agreement split into guilty and innocent cases. Score reviewers against that ground truth, not against each other.
</details>

## Week 8: Rights of avatars

30. *Week 8 · compute.* In a game, 3% of novel techniques are later declared exploits, and once declared, the studio detects 40% of past uses. An explorer tries 30 novel techniques a year. A casual player tries 4. Compute each player's chance of a ban after one year and after two years, under retroactive and warn-first policies.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `r = 0.03 × 0.4 = 0.012`.

| Player | `N` | Retroactive | Warn first |
|---|---|---|---|
| Explorer, 1 year | 30 | 30.4% | 5.0% |
| Explorer, 2 years | 60 | 51.5% | 16.2% |
| Casual, 1 year | 4 | 4.7% | 0.085% |
| Casual, 2 years | 8 | 9.2% | 0.38% |

Explorer, one year, retroactive: `1 − 0.988^30 = 1 − 0.696 = 0.304`. Warn first: `0.304 − 30 × 0.012 × 0.988^29 = 0.304 − 0.254 = 0.050`.

Under a retroactive policy the explorer is more likely than not to be banned within two years, for play believed legitimate. Notice-first gives 0 for both players, provided they stop once a technique is declared.
</details>

31. *Week 8 · compute.* A server has 50,000 players. 4% are explorers who try 25 novel techniques a year. The rest try 2. The per-technique risk is `r = 0.01`. For one year, compute bans among explorers and among everyone else, and the explorers' share of bans, under retroactive and warn-first policies. What does the warn-first result tell you?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Retroactive: about 444 explorers and 955 others, so explorers take 31.7% of bans. Warn first: about 52 explorers and 5 others, so 91.5%.

There are 2,000 explorers and 48,000 others. Retroactive: `2,000 × (1 − 0.99^25) = 2,000 × 0.2222 = 444` and `48,000 × (1 − 0.99^2) = 48,000 × 0.0199 = 955`. Share `444 / 1,399 = 31.7%`.

Warn first: `1 − 0.99^25 − 25 × 0.01 × 0.99^24 = 0.2222 − 0.1964 = 0.0258`, so about 52 explorers. Others: `0.99^2` leaves `1 − 0.9801 − 0.0198 = 0.0001`, so about 5.

Warn-first protects casual players almost completely, which is why it feels fair to most of the community. It also concentrates the remaining bans on the 4% who explore. If a studio finds most exploit bans hit its most active players, the model says its policy is retroactive in practice for ambiguous techniques.
</details>

32. *Week 8 · design.* Rewrite Koster's article 13 (payment never buys rights) and article 18 (privacy, no investigation without cause) as commitments a studio can check. For each, state the cost and the right or interest it collides with.

<details>
<summary>Answer and worked solution</summary>

**Answer (model):**

- Article 13: "Support queues, appeals and moderation decisions follow the same process and targets for paying and free players. We publish median appeal times for both groups every quarter." Cost: lost revenue from priority support. Collides with the business model, and with the fairness claim of subscribers who fund the service.
- Article 18: "We read a player's chat logs only for the matches named in a report, only the assigned reviewer sees them, and we publish the number of logs read each quarter." Cost: reviewer tooling and reporting. Collides with safety. A report counts as cause, so a malicious reporter can trigger a reading. Reporter weighting from week 7 limits this but does not remove it.

Mark on the three parts the lecture requires: an action, a time limit or scope, and something published. "Players have a right to privacy" scores zero.
</details>

33. *Week 8 · explain.* The Falador Massacre (RuneScape, June 2006) ended in permanent bans for players who killed many others after a bug. Why does the lecture say this retroactive punishment does not threaten good-faith explorers, and what test would you write to separate such cases from ambiguous ones?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Attacking players in a city where combat should be impossible has `q` close to 1. No reasonable player could believe it was intended, so good-faith explorers would not have used it, and punishing it afterwards does not add risk to their careers.

One test: "A technique is an obvious exploit if it gives an advantage that a rule, tooltip or zone property says is impossible, such as combat in a safe zone, duplicated items or bypassing a purchase." Obvious exploits can be punished on first use. Everything else is punished only after public notice. The test must be written down, because "obvious" will be argued in every appeal.
</details>

## Week 9: Virtual property and law

34. *Week 9 · explain.* Run each case through the four-question layer test and give the layer and the question where it stops. (a) In a game whose rules allow in-game scams, a player swaps the item in a trade window at the last second and the victim clicks accept. (b) Malware logs a player's password, and the thief moves their items to his own account. (c) The operator bans a player by mistake and deletes her inventory. (d) A duplication bug moves items out of a shared guild vault without anyone's action.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Play, at Q4. (b) Law, at Q2. (c) Contract, at Q1. (d) Operator, at Q4 (exploit).

(a) Q1 another player. Q2 no outside means. Q3 the rules allow it. Q4 the mechanics moved the item through the victim's own click. Play layer, no remedy. Good design shows the risk with a trade window that highlights last-second changes.

(b) Q2 yes. Hacking the account is an outside means. Law layer, as in the Dutch RuneScape case, where the court protected the victim's control through his login whatever the EULA said about ownership. The operator will also act on the hacked account.

(c) Q1 the operator is the taker. The dispute is under the contract and consumer law, as in *Bragg*.

(d) Q4 no. A bug carried out the transfer. Operator layer: reversal and possible punishment of anyone who used it.
</details>

35. *Week 9 · compute.* Your game forbids scams and processes 5 million trades a day. 0.004% of trades lead to a scam report, and each takes 20 minutes to investigate. (a) How many staff hours a day does the rule cost, and how many 8-hour investigators? (b) At the EBank-implied price of about £15.6 per billion ISK, what real-money value would a 120 billion ISK vault theft have, and does the value move the case between layers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 66.7 hours, a little over 8 investigators. (b) About £1,872. No.

(a) `5,000,000 × 0.00004 = 200` reports. `200 × 20 / 60 = 66.7` hours. `66.7 / 8 = 8.3` investigators before appeals.

(b) `120 × 15.6 = £1,872`. The layer test turns on who took the item and by what means. Value matters inside the law layer, for whether an item counts as goods and for sentencing, but it does not move a case between layers.
</details>

36. *Weeks 4 and 9 · explain.* This is the course's signature case. Explain why EVE Online treated the 2009 EBank withdrawal as allowed play while banning the same player for the cash-out. Use both the week 4 allowed-play test and the week 9 layer test, and say what each test adds that the other does not.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both tests split the event into two acts. The withdrawal passes, and the cash-out fails at the stakes question.

Week 4: the withdrawal uses standard mechanics (`M`), keeps the ISK in the game (`S`), targets a bank of characters (`T`), and CCP's policy announces that scams are allowed (`N`), so it is allowed play. The cash-out fails `S`, because the proceeds left the asset layer, and the BBC reported that this, not the theft, was the reason for the ban.

Week 9: the withdrawal stops at Q4 (depositors handed over ISK voluntarily, and ordinary mechanics moved it), so it is in the play layer. The cash-out stops at Q3 (the EULA forbids selling ISK for money), so it is in the operator layer.

What each adds: the allowed-play test names who the line protects (the game's frame, not the victim) and makes the policy comparable across games. The layer test adds routes outside the operator's control. It shows when the law or the contract takes over, for example if the depositors' accounts had been hacked. The depositors' loss is identical in both halves of the story. Only the verdict changes.
</details>

37. *Week 9 · critique.* A studio's support lead says: "Our EULA says we own every item, so an account theft is not a real theft, and it is not our problem beyond resetting the password." Critique this with the week 9 cases and give two design consequences.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The EULA governs disputes between the operator and the player. It does not decide whether a third party committed theft.

The Dutch Supreme Court (2012) held that RuneScape items taken through threats were goods under the theft article, because they had real value to the victim and he had exclusive control through his login. The contract between the victim and Jagex could not make the taking legal. So account theft can be in the law layer whatever the EULA says.

Design consequences: account security (two-factor login) and item recovery after hacks are part of the studio's legal exposure, not only its support costs. The support policy should state which layer handles each way an item can leave a player, so hacked-account cases are not left between layers the way the Dragon Sabre case was.
</details>

## Week 10: Addiction, wellbeing and responsible design

38. *Week 10 · compute.* Use the lecture's constants (`b = 10`, `a = 0.625`, rested cap 150, daily bonus `d = 10`, fatigue as in the lecture). A player plays three 2-hour sessions a week on Monday, Wednesday and Saturday. Compute the weekly experience under flat, rested, fatigue and daily-reward rules, and each as a ratio to flat.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Flat 60, rested 120, fatigue 60, daily reward 90. Ratios 1.0, 2.0, 1.0 and 1.5.

Flat: `6 × 10 = 60`.

Rested: `min(0.625 × (168 − 6), 10 × 6) = min(101.25, 60) = 60` of bonus. The gaps between sessions are at least 46 hours, which bank at least 28.75, more than the 20 each session can spend. So every hour is doubled, for 120. The bank is limited by what the player can spend, not what they earn. The surplus builds up to the cap of 150 and is then wasted.

Fatigue: each day's play is under 3 hours, so it earns the full rate, 60.

Daily reward: `60 + 3 × 10 = 90`.

Like the lecture's light player, this player gets the largest relative boost from rested experience. Rested is a catch-up mechanism.
</details>

39. *Week 10 · compute.* A designer builds a rested rule with the shape the lecture describes for Final Fantasy XIV: a 50% bonus instead of 100%, and a bank that fills in 7 days. The invented numbers are a bank cap of 50 (percent of a level), filling at `50 / 168` per hour offline, a bonus of `b / 2 = 5` per hour played while the bank lasts, and `b = 10`. (a) Write the weekly bonus in the lecture's closed form. (b) At what `H` does the limit switch from spending to banking? (c) Compute the total for 4 and 14 hours a week, as ratios to flat. Compare with the lecture's World of Warcraft figures.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `bonus = min(0.2976 × (168 − H), 5H)`. (b) About 9.4 hours. (c) 4 hours: 60, ratio 1.50. 14 hours: 185.8, ratio 1.33.

(b) `0.2976 (168 − H) = 5H` gives `50 = 5.2976 H`, so `H ≈ 9.44`.

(c) At 4 hours, `min(48.8, 20) = 20`, so the total is `40 + 20 = 60`. At 14 hours, `min(0.2976 × 154, 70) = min(45.8, 70) = 45.8`, so the total is `140 + 45.8 = 185.8`.

The World of Warcraft model gave ratios of 2.0 for the light player and 1.69 at 14 hours. The gentler rule compresses the gap between light and heavy players less. It reads the same clock (time offline), so it still does not care how the 14 hours are arranged, and it does nothing about session length.
</details>

40. *Week 10 · compute.* A login calendar pays `5 × min(k, 7)` percent of a level on the `k`-th consecutive login day, and resets to `k = 1` after a missed day. A player on a 30-day streak misses one day, then logs in every day. Over the 8 days starting with the missed day, how much do they earn compared with a player who never missed? Compare the loss with the lecture's flat daily reward, and apply the obligation test.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 140 against 280, a loss of 140. The flat daily reward loses 10.

Uninterrupted, the player earns 35 a day, so 280 over 8 days. After the miss they earn 0, then `5 + 10 + 15 + 20 + 25 + 30 + 35 = 140`. The loss is 140, fourteen times the flat daily reward's 10.

Obligation test: the loss cannot be avoided by rearranging the same hours. Only logging in on the missed day avoids it. And unlike the flat reward, the cost of missing a day grows with the length of the streak. That is the lecture's case against streaks that reset to zero. A fix is to let the streak fall back one step instead of resetting, or to use a weekly cap on claims.
</details>

41. *Week 10 · critique.* A journalist writes: "Players of this MMO average 30 hours a week, so the game is clinically addictive." Correct the claim using ICD-11, DSM-5 and the 2022 telemetry study, and say what a studio should measure instead.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Neither clinical definition uses hours. ICD-11 gaming disorder (in effect from 1 January 2022) needs impaired control, gaming taking priority over other interests, and continuing despite negative consequences, with significant impairment, normally over 12 months. DSM-5 lists Internet Gaming Disorder in Section III as a condition for further study, with nine proposed criteria. Vuorre and colleagues (2022) linked six weeks of play data from 38,935 players to wellbeing surveys and found little evidence that time played affected wellbeing, while motivations did matter.

A studio should measure obligation: the share of logins under 10 minutes that only claim a daily reward, and survey items on why people play. It should run the obligation test on each pacing rule.
</details>

## Week 11: Minors in online worlds

42. *Week 11 · compute.* A game has 200,000 sign-ups, 12% of them under 13. Compare a self-declared gate where 40% of children lie with an age-estimation check with `se = 0.92` and `sp = 0.97`. For each, compute children missed, 13+ players wrongly restricted, precision of the child flag, and children exposed to stranger chat with a default-on keep rate of 0.85 and a default-off opt-in rate of 0.25.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Gate | Missed | Wrongly restricted | Precision | Exposed, default on | Exposed, default off |
|---|---|---|---|---|---|
| Self-declared | 9,600 | 0 | 100% | 8,160 | 2,400 |
| Estimation | 1,920 | 5,280 | 80.7% | 1,632 | 480 |

There are 24,000 children and 176,000 older players. Self-declared: `24,000 × 0.4 = 9,600` missed. Estimation: `24,000 × 0.08 = 1,920` missed and `176,000 × 0.03 = 5,280` restricted. Flagged children `22,080`, total flags `27,360`, precision `22,080 / 27,360 = 80.7%`.

Exposure is missed children times the keep rate. The cheapest large cut is the default. Switching it off with the self-declared gate cuts exposure from 8,160 to 2,400, a 71% drop, and costs no older player a wrong restriction. The estimator with the default left on reaches 1,632, lower, but restricts 5,280 older players to get there. Both levers together reach 480.
</details>

43. *Week 11 · compute.* An age-estimation check has `se = 0.9` and `sp = 0.95`. (a) At what share of child sign-ups `π` does it restrict exactly as many older players as it correctly catches children? (b) Repeat for `se = 0.92`, `sp = 0.97`. (c) What does this mean for a studio choosing a check?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About 5.3%. (b) About 3.2%. (c) Measure `π` before you buy a check.

Set caught children equal to wrongly restricted older players: `π × se = (1 − π)(1 − sp)`. So `π = (1 − sp) / (se + 1 − sp)`.

(a) `0.05 / 0.95 = 5.26%`. The lecture's 5% case sits just below this, which is why it restricted 4,750 older players while catching 4,500 children.

(b) `0.03 / 0.95 = 3.16%`.

(c) Below that `π`, most "child" flags are wrong. A game with few children will generate more support tickets from misclassified adults than protected children, so it needs an appeal route (week 7) and should change the default first.
</details>

44. *Week 11 · critique.* A studio's new fantasy MMO asks for a birth year at sign-up, puts every player on open text and voice chat by default, and lets parents "opt in" to controls through a web page. Critique the design using the gate, default and fallback model, the Epic case and the UK Children's Code, and propose a redesign using the communication ladder.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The gate is a weak self-declaration, the default puts every missed child on the top rung, and the fallback depends on parents finding a web page.

- Default: open chat on by default is what the FTC alleged against Epic, whose 2022 order required voice and text off by default for children and teens. Standard 7 of the UK Children's Code asks for high-privacy defaults for services likely to be accessed by under-18s.
- Knowledge: asking for a birth year gives the studio actual knowledge under COPPA for every user who answers under 13, so it must then get verifiable parental consent.
- Redesign: start everyone at menu chat or filtered chat, open friend chat through a code exchanged outside the game (Toontown's True Friends pattern), and require an explicit choice to reach open chat. For under-13 accounts, open chat needs parental consent. Give wrongly restricted older players an appeal path. Store an age band, not a birth date.

Exposure is `N × π × (1 − se) × k`. Moving `k` from about 0.9 to about 0.3 cuts exposure by two thirds whatever gate is used.
</details>

## Week 12: Research ethics in online worlds

45. *Week 12 · compute.* A studio plans to release 40,000 character rows with class (12 values), race (8), exact level (80) and faction (2). (a) Estimate `C`, `λ`, the unique share and the share in equivalence classes smaller than 5. (b) Repeat with level reported in 8 brackets of 10.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `C = 15,360`, `λ = 2.60`, 7.4% unique, 73.5% in classes smaller than 5. (b) `C = 1,536`, `λ = 26.0`, effectively 0% on both.

(a) `C = 12 × 8 × 80 × 2 = 15,360`. `λ = 39,999 / 15,360 = 2.604`. Unique share `e^(−2.604) = 0.074`. Share below 5 is the Poisson sum for 0 to 3 others: `e^(−λ)(1 + λ + λ²/2 + λ³/6) = 0.0740 × 9.94 = 0.735`.

(b) `C = 12 × 8 × 8 × 2 = 1,536`. `λ = 26.04`. `e^(−26)` is about 5 × 10⁻¹², and the share below 5 is about 2 × 10⁻⁸.

Only 7% are unique in (a), yet almost three quarters fail 5-anonymity. The level brackets fix both. As the lecture warns, real data are skewed, so audit actual counts: rare class and race combinations stay small even when `λ` is large.
</details>

46. *Week 12 · design.* A server has 25,000 characters. You want to release class (12 values), race (8), guild size band (3) and level in `B` equal brackets. What is the largest `B` that keeps the estimated unique share below 0.5%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `B = 16`.

The unique share is `e^(−λ) < 0.005`, so `λ > ln 200 = 5.298`. That needs `C < 24,999 / 5.298 = 4,718`. With `C = 12 × 8 × 3 × B = 288B`, `B < 16.4`.

Check: `B = 16` gives `C = 4,608`, `λ = 5.43`, unique share 0.44%. `B = 17` gives `λ = 5.11` and 0.61%, which fails. Then audit the real counts, because rare combinations will still form small classes.
</details>

47. *Week 12 · explain.* For each scenario, say whether it is product testing or research under the Common Rule definition, name the Belmont principle most at risk, and say what should happen first. (a) A studio tests two tutorial texts to choose one for launch. (b) The same studio raises drop rates on one server for a month to measure whether generous loot increases spending, and plans to present the result at an academic conference. (c) A university team asks for per-character zone histories for 90 days.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

(a) Product testing. Its purpose is a decision about this game. Low risk. No ethics review is needed in most places, though a debrief is good practice.

(b) Research, because it aims at generalizable knowledge. Beneficence and justice are at risk: players in one group bear a cost (spending pressure), and the ToS is not informed consent to a manipulation. Before running it, get ethics review (a partner university's board or an internal one), use a specific opt-in or justify a waiver (a waiver is hard to justify here, because the harm lands on one group), and plan a debrief.

(c) Research, and the release plan is the main risk. Zone histories are trajectories, and trajectories are identifying even with coarse fields. Offer aggregates, or enclave access under a signed agreement with only aggregates leaving the enclave. Respect for persons asks for a consent plan too.
</details>

48. *Week 12 · critique.* A data team says: "We replaced every character name with a hash, so the dataset of daily level, guild and zone per character is anonymous and can go on a public site." Give three reasons this is wrong, with examples from the lecture.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

1. Quasi-identifiers remain. Level, guild and zone are visible on public profiles. On the lecture's 10,000-character server, class, race, level and guild left 99.2% of rows unique, and a unique row is a named row.
2. Daily snapshots form a trajectory. A sequence of zones and levels over time is far more distinctive than one row. The Netflix Prize ratings with dates were re-identified by matching them to public reviews.
3. A hash is a stable pseudonym. It links every row for a character across days, which builds the trajectory. The AOL release replaced names with numbers, and *The New York Times* still identified a user from her searches.

Fix: release aggregates, generalize and check k-anonymity for any rows, and put trajectories behind enclave access.
</details>

## Week 13: Shutdown ethics

49. *Week 13 · compute.* Players spent `s = $120,000` a month on durable items with an expected life of `L = 18` months. Running the world costs `C = $40,000` a month. (a) Find `N*`, `V(N*)` and the total cost at `N*`. (b) Compare with closing at once and refunding exact unused value. (c) How much stranded value does the first month of notice remove?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `N* = 12` months, `V = $120,000`, total $600,000. (b) Closing at once costs $1,080,000 in refunds, $480,000 more. (c) $116,667.

(a) `N* = 18 × (1 − 40,000 / 120,000) = 12`. `V(12) = 120,000 × 6² / 36 = 120,000`. Total `= 40,000 × 12 + 120,000 = 600,000`.

(b) `V(0) = 120,000 × 18² / 36 = 1,080,000`.

(c) `V(1) = 120,000 × 17² / 36 = 963,333`, so the first month removes `116,667` for $40,000 of running cost. Notice is a refund paid in time, and early months are the cheapest.
</details>

50. *Week 13 · compute.* Use the lecture's numbers (`s = $200,000`, `L = 12`, `C = $100,000`). Plan A: 6 months' notice. Plan B: 3 months' notice plus a community server release that preserves `ρ = 0.4` of the value of every purchase. Compare stranded value and running cost. Up to what cost is the server release the cheaper plan?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Plan A leaves $300,000 stranded and costs $600,000 to run. Plan B leaves $405,000 stranded and costs $300,000 to run, plus the release. Plan B is cheaper overall if the release costs less than $195,000.

Plan A: `V(6) = 300,000`, running `600,000`, total $900,000.

Plan B: `(1 − 0.4) × V(3) = 0.6 × 675,000 = 405,000`, running `300,000`, total $705,000 before the cost of the release.

The totals differ by $195,000. Plan B also reaches purchases older than `L`, which notice never can, and it keeps some of the value of time and community (Knockout City's route in 2023). Middleware licences can make a release impossible without months of legal work, which is why the lecture says to decide at launch.
</details>

51. *Week 13 · compute.* A live-service game closes after `T = 4` months with `L = 12`, with no notice. What share of everything ever spent is stranded? How much more than exact unused value does a full refund of every purchase cost? Compare with the Concord case in the lecture.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 83.3% stranded. A full refund costs 20% more than exact unused value.

Stranded share `= 1 − T / (2L) = 1 − 4 / 24 = 0.833`. A full refund pays 100%, which is `1 / 0.833 − 1 = 0.20` more.

Concord ran 14 days (`T ≈ 0.5`), where the share is 97.9% and a full refund costs only about 2% more. The longer a game runs, the further the two policies come apart, which is why operators of old games rarely refund everything.
</details>

52. *Week 13 · critique.* A publisher announces 6 months' notice but keeps selling cosmetics at the usual rate (`s = $200,000` a month, `L = 12`) until the final month. Treat each notice month's sales as bought 6, 5, 4, 3 and 2 months before closure. Compare stranded value with a 3-month notice that stops sales on day 0.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The 6-month plan with sales strands about $966,667. The 3-month plan with sales stopped strands $675,000.

Pre-announcement purchases: `V(6) = 300,000`.

Sales during notice: `200,000 × [(1 − 6/12) + (1 − 5/12) + (1 − 4/12) + (1 − 3/12) + (1 − 2/12)] = 200,000 × 3.333 = 666,667`.

Total `966,667`, against `V(3) = 675,000` with sales stopped. The longer notice leaves players worse off, and the publisher collected $1,000,000 in notice-period sales that are mostly stranded. The model assumes sales stop on day 0. The sunset charter makes that a commitment.
</details>

53. *Weeks 13 and 14 · compute.* With the lecture's numbers (`s = $200,000`, `L = 12`, `C = $100,000`), a studio weights each player dollar lost as `k = 1.25` operator dollars. What is the new `N*`? Where does this weight sit on a week 14 decision map, fact axis or value axis?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `N* = 7.2` months. `k` is on the value axis.

`N* = L × (1 − C / (k × s)) = 12 × (1 − 100,000 / 250,000) = 12 × 0.6 = 7.2`.

`k` says how much the studio cares about player losses relative to its own costs. No measurement settles it, so it is a value. `L`, the life buyers were led to expect, is closer to a fact about what the store page and terms said. Two executives who disagree about notice can check which of the two separates them before arguing.
</details>

## Week 14: Debates

54. *Week 14 · compute.* A debater scores two options on harm prevented (`h`) and freedom (`f`). Restrict: `h = 6`, `f = 4`. Free: `h = 3`, `f = 8`. (a) Compute the crux weight `w*`. (b) Which option does a debater with `w = 0.45` choose, and by how much? (c) How high must they believe restriction's harm score is before they switch, keeping their weight?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `w* = 0.571`. (b) Free, by 0.85. (c) Above about 7.89.

(a) `Δh = 3`, `Δf = −4`, so `w* = 4 / (3 + 4) = 0.571`.

(b) `U(R) = 0.45 × 6 + 0.55 × 4 = 4.9`. `U(F) = 0.45 × 3 + 0.55 × 8 = 5.75`. `D = −0.85`.

(c) The crux score is `x = −D / w = 0.85 / 0.45 = 1.89`, so `h(R)` must rise from 6 to 7.89. Check with the map curve: `w*(h_R) = 4 / (h_R + 1)`, and setting it to 0.45 gives `h_R = 7.89`. Against this debater, bring evidence about the fact (how much harm restriction prevents), not arguments about priorities.
</details>

55. *Week 14 · compute.* A three-criterion table has weights 0.3, 0.5 and 0.2. Option A scores 7, 4 and 5. Option B scores 4, 6 and 8. (a) Which option wins, and by how much? (b) Using lab 14's rule that the other weights keep their proportions, compute the crux weight of each criterion. (c) Compute each criterion's crux score for option A. Which criterion is the debate most likely to turn on, and why can a crux weight fall outside 0 to 1?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) B wins, 5.8 to 5.1, so `D = −0.7`. (b) 0.432, 0.231 and no tie in range (−0.043). (c) +2.33, +1.40 and +3.50. Criterion 2 is closest in score terms.

(a) `U(A) = 2.1 + 2.0 + 1.0 = 5.1`. `U(B) = 1.2 + 3.0 + 1.6 = 5.8`.

(b) With the other weights rescaled by `(1 − w) / (1 − w_j)`, the rest of the gap is `R_j = (D − w_j Δ_j) / (1 − w_j)` and the crux weight is `w* = −R_j / (Δ_j − R_j)`.

- Criterion 1 (`Δ = 3`): `R = (−0.7 − 0.9) / 0.7 = −2.286`, so `w* = 2.286 / 5.286 = 0.432`. Check: at 0.432 the other weights are 0.405 and 0.162, and both options score 5.459.
- Criterion 2 (`Δ = −2`): `R = (−0.7 + 1.0) / 0.5 = 0.6`, so `w* = −0.6 / −2.6 = 0.231`. A would win if the weight on criterion 2 fell below 0.231.
- Criterion 3 (`Δ = −3`): `R = (−0.7 + 0.6) / 0.8 = −0.125`, so `w* = −0.043`. Even at weight 0, A loses (5.125 against 5.25). Changing this weight alone cannot flip the decision.

(c) `x = −D / w_j`: `0.7 / 0.3 = 2.33`, `0.7 / 0.5 = 1.40`, `0.7 / 0.2 = 3.50`. Criterion 2 needs the smallest score change, and its crux weight (0.231 against 0.5) is also the one a reasonable opponent might argue toward.
</details>

56. *Week 14 · explain.* Classify each statement as a claim on the fact axis or the value axis, and say whether the two speakers are arguing with each other. Dev: "After we required human review of automated bans, wrongful bans fell from 600 a day to 40." Lee: "A ban decided by a machine is illegitimate even if it is accurate." Then name the evidence that would move each of them.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Dev is on the fact axis. Lee is on the value axis. They are not yet arguing with each other.

Lee could accept Dev's numbers and still hold the position, because Lee's claim is about process (week 1's fair-process condition, and the DSA's rule that complaint handling is not solely automated). Dev's claim is about outcomes.

What moves Dev: an audit showing the fall came from something else, or that missed violations rose. What moves Lee: not data, but an argument from a principle Lee already holds. For example, if Lee cares about players who are harmed while a queue waits, the week 6 backlog numbers show the human-only alternative has victims too. The productive next step is for each to say whether they accept the other's point.
</details>

57. *Week 14 · critique.* A debater cites RuneScape's 2010 to 2011 referendum (1,234,658 votes, 91% for restoring free trade and the Wilderness) as proof that the December 2007 trade limit "did nothing against gold farming". Critique the use of this evidence, and say what evidence would answer the claim.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The vote measures voters' weights, not the effect of the limit.

Voters could not observe how many bots the limit had stopped, so the 91% says nothing about `h(R)`, the fact axis. It is strong evidence on the value axis, but only for those who voted. Players who had quit after 2007 (subscriptions fell by 60,000, and nobody published how many of those were gold farmers) could not vote, and neither could players who would later lose accounts to thieves. Jagex also presented the return alongside its work against bots and account theft, which is an attempt to raise `h(F)`.

Evidence that answers the claim is telemetry: bot reports, gold-seller spam, account-theft tickets and gold prices before and after December 2007. A comparable case from another game would also help, with the ways it differs stated.
</details>

58. *Week 14 · design.* For debate motion 6 ("no ban should be issued by an automated system without human review"), write one Toulmin argument for the opposition with all six parts, and say which part a good proposition team should attack.

<details>
<summary>Answer and worked solution</summary>

**Answer (model):**

| Part | Opposition |
|---|---|
| Claim | Some bans may be issued automatically without prior human review |
| Grounds | Client-side cheat detection can be near-certain, and at the week 6 volumes (about 107,000 reports a day on Xbox in 2025) human review of every case builds a backlog that delays justice for victims |
| Warrant | When evidence is near-certain and delay harms others, a fast automatic sanction with a human appeal protects more people than a slow human-first process |
| Backing | Week 6's queue model: a review load above `C` grows without limit; week 7's rule to match sanction to confidence |
| Qualifier | Only for detected cheating programs, not for chat or behavior |
| Rebuttal | Unless the detector's false-positive rate is not measured, or appeals are not heard by a person, as DSA Article 20 requires |

The proposition should attack the warrant, specifically the claim that detection is "near-certain". That is a fact claim that audited false-positive rates can test. Attacking the grounds wastes time, because the queue arithmetic is true.
</details>
