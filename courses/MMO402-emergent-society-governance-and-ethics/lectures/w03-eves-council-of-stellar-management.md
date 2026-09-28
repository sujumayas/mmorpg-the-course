# MMO402 · Week 03 — EVE's Council of Stellar Management

**Why this matters:** Sooner or later someone on your team will propose a player council. It sounds like pure goodwill. But an elected body has a voting rule, and the voting rule decides who gets elected. If you do not work out whose voice your council amplifies before you launch it, your players will work it out for you.

**You will be able to:**
- Describe how EVE Online's Council of Stellar Management (CSM) is elected, what it may do and what it may not, with dates.
- Compute the Droop quota for a single transferable vote election and the number of seats a disciplined voting bloc can guarantee itself.
- Show, with numbers, how turnout among unorganized players changes an organized bloc's seats under STV and under block voting.
- Critique a proposed player council by its electorate, voting rule, powers and information rules, and propose an alternative such as reserved seats or random selection.

**Before class:** EVE University Wiki, "Council of Stellar Management" (15 minutes). Hirschman, *Exit, Voice, and Loyalty* (1970), chapter 3 again, on voice. Scharpf, *Governing in Europe: Effective and Democratic?* (1999), the introduction, on input and output legitimacy. Bring a laptop with Python 3 for the in-class activity.

**Prerequisites from earlier courses:** [MMO301 week 6, EVE Online: the single-shard sandbox](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md) (why EVE's one-server world makes politics matter). [MMO304 week 13, case studies](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md) (EVE's economy and CCP's in-house economist). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (used for random selection in section 4). [MMO305 week 13, ethnography of online worlds](../../MMO305-social-systems-and-online-behaviour/lectures/w13-ethnography-of-online-worlds.md) (the players you meet are not the players who play; the same bias applies to the players who vote). This course: [week 1, exit and voice](w01-worlds-as-polities.md) and [week 2, alliances and councils](w02-emergent-player-government-alliances-and-councils.md).

**Interactive:** [w03-quota-and-turnout.html](../examples/w03-quota-and-turnout.html)

---

## 1. A council for a single-shard world

EVE Online runs almost all its players on one server cluster, so a decision by the developer, CCP Games, lands on everyone at once. That makes voice unusually valuable in EVE, in the sense of week 1. There is no other realm to move to.

In March 2008, CCP invited players to stand for a new elected body, the Council of Stellar Management. The first election ran in May 2008. Sixty-six candidates competed for nine seats. Wikipedia's summary of the first council notes seven men and two women, from the Netherlands, the United Kingdom, the United States and Denmark, aged from 17 to 52. The council arrived about a year after a scandal in which a CCP developer, known as t20, gave valuable blueprints to his own player corporation in February 2007. Wikipedia's account says CCP set up the council partly because of that incident, so read it as, in part, CCP's answer to a trust problem.

### What the CSM is today

The EVE University Wiki describes the current rules, which have changed several times since 2008.

- **Size and term.** Ten representatives, each council lasting twelve months.
- **Voting rule.** Single transferable vote (STV), explained in section 2. CCP does not publish the exact variant, but its published counts from past elections use the Droop quota. Wikipedia records STV arriving with the eighth council (2013), when voters could rank up to 14 candidates. Today a voter ranks up to as many candidates as there are seats.
- **Electorate.** One ballot per paid (Omega) account that has been active for at least 30 consecutive days. Free accounts do not vote.
- **Eligibility.** Candidates need an account older than 60 days, must be 18 or older, and must hold a passport and be able to travel to Iceland. CCP staff, their families and players with serious warnings or bans are excluded. Candidates once had to run under their real names. That rule is gone.
- **Term limits.** From the fifteenth council, three years in a row and then one year off.
- **Summit.** Members travel to Iceland once per term to meet developers in person. CCP pays travel, lodging and most meals. Since the seventeenth council (2022), candidates who cannot travel may still stand.
- **Secrecy.** Members sign a non-disclosure agreement (NDA) before their term starts, so they can see plans that are not public.
- **Powers.** The council has a voice inside CCP and no formal powers. It cannot veto a feature, set a budget or overrule a designer.

Read those rules as a designer. The CSM is an **advisory body**. In week 1's terms it is a channel that raises `p`, the chance that player voice changes the developer's decision, without taking the decision away from the developer. Its members see more than ordinary players, which makes them better advisors and harder to hold accountable, because they cannot tell voters what they saw.

### Did it matter?

The hardest test came in 2011. Players protested the Incarna expansion and the arrival of microtransactions. In October 2011 CCP laid off 20% of its staff worldwide, said releasing Incarna at that stage had been a mistake, and moved its focus back to EVE. How much of that the CSM caused is hard to separate from the wider protest, and you should be suspicious of anyone who claims to know. What the case shows is that an advisory council does not replace exit. It gives exit a place to be heard before it happens.

## 2. Worked example: what share of the vote buys a seat?

### The hook

Here is a fact about the CSM that follows from its rules alone. With ten seats and a Droop quota, **any group that controls just over one eleventh of the ballots cast, about 9.1%, is guaranteed a seat, whatever everyone else does.** Twice that guarantees two seats.

Notice the words "ballots cast." Not players, not accounts. Every EVE player who does not vote makes the organized groups' share bigger. And EVE, as week 2 showed, is full of organized groups: corporations, alliances and coalitions with chains of command, voice servers and the habit of following instructions. So the designer's question is "fair to whom, at what turnout?"

### The model

In a **single transferable vote** election, each voter ranks candidates in order of preference. The count works like this.

1. Compute the **quota**, the number of votes that guarantees election. EVE's past counts use the Droop quota:

   ```
   Q = floor(V / (S + 1)) + 1
   ```

   where `V` is the number of valid ballots and `S` the number of seats.
2. Count every ballot for its highest-ranked candidate still in the race.
3. Anyone at or above `Q` is elected. Their **surplus**, the votes above `Q`, moves to the next preference on their ballots, at reduced weight so that the total moved equals the surplus.
4. If nobody reaches `Q`, the lowest candidate is eliminated and their ballots move to the next preference.
5. Repeat until all seats are filled.

Why `S + 1`? If `S` candidates each hold more than `V/(S + 1)` votes, the votes left over are less than `V/(S + 1)`, so no one else can match them. The Droop quota is the smallest quota that can never elect more than `S` people.

Now the bloc. Suppose a group of `B` voters all rank the group's own candidates first, in an agreed order. No matter how the other ballots are cast, the bloc's votes can be passed along its own list through the surplus transfers, so as long as it ranks enough of its own candidates it is guaranteed

```
guaranteed seats = min(S, floor(B / Q))
```

It may win more through other people's transfers. It cannot win fewer.

To see turnout, split the electorate. `E` accounts can vote. The bloc's `B` members all vote. Everyone else votes with probability `t`, the **casual turnout**:

```
V = B + t × (E − B)
bloc share = B / V
```

### Numbers you can check

Use invented round numbers so nobody mistakes them for EVE's real figures: `E = 300,000` eligible accounts, a bloc of `B = 6,000` (2% of the electorate), and `S = 10` seats.

| Casual turnout t | Ballots V | Bloc share of ballots | Quota Q | Seats guaranteed to the bloc |
|---|---|---|---|---|
| 2% | 11,880 | 50.5% | 1,081 | 5 |
| 5% | 20,700 | 29.0% | 1,882 | 3 |
| 10% | 35,400 | 16.9% | 3,219 | 1 |
| 20% | 64,800 | 9.3% | 5,891 | 1 |
| 30% | 94,200 | 6.4% | 8,564 | 0 |

Check the 5% row. Casual voters cast `0.05 × 294,000 = 14,700` ballots, so `V = 20,700`. `Q = floor(20,700 / 11) + 1 = 1,881 + 1 = 1,882`. The bloc's 6,000 votes contain `floor(6,000 / 1,882) = 3` quotas.

Now compare the two ways to read the same table. The bloc is 2% of the electorate in every row. It holds anywhere from none to half of the seats, depending only on whether everyone else turned up.

### STV against block voting

STV is often praised as proportional, and the table shows why: the bloc's seats track its share of ballots cast. Compare the simplest alternative, **block voting** (also called plurality-at-large), in which each ballot gives one vote to each of up to `S` names and the `S` highest totals win.

Lab 03 includes a ballot file for a made-up ten-seat election with 20,700 ballots, the 5% row above. A disciplined bloc (candidates N1 to N5) casts 6,000 ballots. Two smaller organized groups, one from low-security space and one from wormhole space (L and W), cast 2,000 and 1,500. The remaining 11,200 ballots come from unorganized players. They spread across eight candidates (H1 to H8) and two solo candidates (S1 and S2), and most name only two to four candidates. Counting the same ballots two ways gives:

| Rule | Bloc N seats | Group L | Group W | Unorganized H |
|---|---|---|---|---|
| STV, Droop quota 1,882 | 3 | 1 | 1 | 5 |
| Block voting | 5 | 0 | 0 | 5 |

Under block voting, every one of the bloc's 6,000 ballots gives a full vote to each of its five candidates, so all five collect 6,000 and top the count. Under STV, the bloc's votes are counted once, and after three quotas only a small remainder is left to pass down its list. The two smaller organized groups, shut out under block voting, each win a seat under STV.

### The insight

Put the two findings together.

- **STV protects minorities from majorities.** Under block voting a cohesive 29% can take every seat it contests. Under STV it gets roughly its share, and a group with 7% to 10% of ballots can win a seat.
- **STV does not protect the unorganized from the organized.** A bloc's seats depend on its share of *ballots*, and that share is set by everyone else's turnout. Low turnout among casual players turns a 2% bloc into a council majority.

In other words, the voting rule decides how fairly ballots become seats. Turnout decides whose ballots exist.

### The visual

Open the interactive. The top panel plots the bloc's guaranteed seats against casual turnout, from 0% to 50%. Under STV it is a descending staircase. Switch the rule to block voting and it becomes a cliff: the bloc takes every seat it runs for below a certain turnout and nothing above it. The bottom panel shows the ballots as one bar divided into the bloc and everyone else, with tick marks every quota, so you can count the bloc's quotas directly. Drag the turnout slider and watch the ticks spread apart as the quota grows.

### Cross-game recognition

**LambdaMOO's ballots (1993 onward).** From week 1: a LambdaMOO petition needed about 60 signatures, which Mnookin describes as roughly 5% of the average number of votes cast, and a ballot passed with a two-to-one margin of votes cast. Every threshold was measured against turnout, not against the population. The same property as the CSM follows: a small, motivated group could put measures on the ballot and pass them when most residents did not vote.

**EVE's executor rule (week 2).** An alliance's executor needs the support of CEOs from half the member corporations. That threshold is measured against members, not against those who show up, so a quiet corporation counts as a "no." Two rules in the same game make opposite choices about absent voters, and each choice makes sense for its purpose. Choosing a leader should need real majority support. Electing an advisory council should include as many voices as possible, even if few use them.

**National STV elections.** The Droop quota has been used for about a century in STV elections in Ireland, Northern Ireland, Malta and Australia. The arithmetic in the table above applies to them unchanged: seats follow shares of ballots cast, whoever casts them.

### Eyes-open design judgment

- **Choosing STV was a reasonable call.** It stops a single coalition from taking every seat, which block voting would allow. Under STV the organized groups share the council.
- **The unorganized are the hardest group to represent.** Players who play alone or in small groups, often in the game's safer regions, have no chain of command telling them to vote. Their low turnout is the bloc's advantage. Raising their turnout (voting inside the game client, reminders at login, explaining candidates in plain language) moves more seats than any change to the counting rule.
- **Consider reserved seats or appointed members.** A council could reserve seats for play styles (for example, one seat for players who spend most of their time in high-security space) or add a few appointed members chosen by the developer to fill gaps. Both improve coverage and both cost legitimacy, because some members were not elected in an open race.
- **Weak powers limit the damage.** Because the CSM advises and does not decide, a captured council can argue for its bloc but cannot impose its bloc's wishes. That is a real safeguard, and it is also why some players see the council as having little effect.
- **The NDA cuts both ways.** Secrecy lets members see early plans and give better advice. It also means voters cannot check what their representatives did, which weakens accountability in the next election.

## 3. Legitimacy: input and output

Week 1 gave a three-point checklist for legitimacy: predictable rules, fair process, and voice that sometimes works. Political scientist Fritz Scharpf offers a sharper split. **Input legitimacy** comes from how decisions are made: were the governed involved, and were they represented fairly? **Output legitimacy** comes from what decisions achieve: did they solve the problems people cared about?

An advisory council can supply both, and it can fail at both.

| | Council strong | Council weak |
|---|---|---|
| **Input** | Many players vote, elected members span play styles, meetings are summarized publicly | Low turnout, one bloc dominates, members bound by NDA say little |
| **Output** | Players can point to changes the council won | The developer's decisions look the same with or without the council |

The failure most councils fall into is a loop between the two rows. If players see no output, they stop voting. Lower turnout hands the council to organized blocs. A council that represents blocs has less claim to speak for everyone, so the developer gives its advice less weight, which produces even less output. Breaking the loop takes work on both rows at once: published minutes and credited changes on the output side, easier voting on the input side.

### What the council knows that voters don't

The NDA creates an **information asymmetry**, a situation where one side of a relationship knows more than the other. Members know what CCP is planning. Voters do not. When the next election comes, voters must judge a representative's record without seeing most of it. They fall back on what they can see: the candidate's in-game group, public statements and reputation. That again favors organized blocs, whose members hear about their representative's work through internal channels.

A developer can soften this by publishing summaries of each summit, agreed with the council, and by giving members a way to report publicly which of their proposals were adopted. Neither removes the asymmetry. Both give voters something to judge.

## 4. Alternatives to election

If elections favor the organized, what else could you do? Two options deserve a designer's attention.

### Random selection

**Sortition** means choosing representatives by lottery from the eligible population, the way many countries choose juries. Some governments use it for citizens' assemblies on specific questions. A lottery gives every player the same chance of a seat, so the council reflects the population instead of the voters.

The complement rule from MA102 week 3 shows what that means for a bloc. If a bloc makes up 2% of eligible accounts and the council draws 10 members at random, the chance the bloc gets at least one seat is

```
1 − (1 − 0.02)^10 = 1 − 0.98^10 ≈ 18.3%
```

Its expected number of seats is `10 × 0.02 = 0.2`. Compare that with the table in section 2, where the same bloc guaranteed itself between one and five seats under STV at low turnout.

Random selection has costs of its own. Most randomly chosen players will not want the job, so you need a pool of volunteers, which brings back self-selection. Randomly chosen members may know little about the game's deeper systems. And they have no mandate: nobody voted for them, so players may not accept what they say. A mixed design, with a few elected members and a few drawn by lot, is worth testing.

### Many narrow channels instead of one council

A council is one voice channel. Week 1's model says what matters to players is `p`, the chance their voice changes things, not the form of the channel. Surveys sent to random samples of players, public test servers with feedback tools, and developer forum replies all raise `p` for different groups. A council works best as one channel among several, especially for questions that need long discussion under NDA.

## In-class activity (25 minutes)

Work in groups of three with the Lab 03 starter files (`labs/lab03-starter.py` and `labs/lab03-ballots.csv`).

1. Run the starter on the ballot file. Record the STV and block-voting winners and check them against the table in section 2 (5 minutes).
2. Halve the unorganized turnout by scaling every ballot whose first choice starts with `H` by 0.5 (the starter has a helper, `scale_group`). Recount both ways. How many seats does bloc N win now under each rule? (8 minutes)
3. Design a rule change for the council that would give unorganized players at least four seats even at half turnout. Test it in the code if you can, or argue it from the quota arithmetic if you cannot (12 minutes).

Expected output: a small table of seats by group under the two rules at full and half casual turnout, and a one-paragraph proposal with the numbers that support it. (At half turnout, 15,450 ballots, the starter gives bloc N four seats under STV and five under block voting.)

## Common misconceptions

- **"STV is proportional, so the council represents the players."** STV makes seats proportional to ballots cast. If turnout differs by group, the council is proportional to the voters, not to the players.
- **"A bloc needs a majority to control an election."** Under STV, each 1/(S + 1) of the ballots guarantees a seat. With ten seats, a bloc with 46% of ballots guarantees five seats, half the council.
- **"The CSM governs EVE."** It advises. It has no formal power to veto or require anything. Its influence works through CCP's willingness to listen.
- **"More seats would dilute blocs."** More seats lower the quota, which lets smaller groups in, but a bloc keeps the same share of seats. Adding seats helps small organized groups more than it helps unorganized ones.

## Check yourself

1. An election for 10 seats has 42,000 valid ballots. What is the Droop quota? How many seats does a disciplined bloc of 9,000 voters guarantee itself?
2. With `E = 300,000`, `B = 6,000` and `S = 10`, find the lowest casual turnout at which the bloc no longer has a guaranteed seat. (Hint: the bloc loses its guarantee when `Q > B`.)
3. A developer changes the council from 10 seats to 7 while keeping STV. With 20,700 ballots, how many seats does the 6,000-voter bloc now guarantee? What share of the council is that, compared with before?
4. Under sortition with 10 seats, what is the chance that a group making up 10% of eligible players gets no seat at all?

<details>
<summary>Answers</summary>

1. `Q = floor(42,000 / 11) + 1 = 3,818 + 1 = 3,819`. The bloc guarantees `floor(9,000 / 3,819) = 2` seats.
2. The bloc keeps one guaranteed seat while `floor(V/11) + 1 ≤ 6,000`, that is while `V ≤ 65,999`. `V = 6,000 + t × 294,000`, so the guarantee ends when `t × 294,000 > 59,999`, at `t ≈ 20.4%`. The table's 20% row still shows one seat, and the 30% row shows none.
3. `Q = floor(20,700 / 8) + 1 = 2,587 + 1 = 2,588`, so the bloc guarantees `floor(6,000 / 2,588) = 2` seats. That is 2 of 7, or 28.6%, against 3 of 10, or 30%, before. Shrinking the council barely changes the bloc's share.
4. `0.9^10 ≈ 34.9%`. Random selection can leave a sizeable group out entirely, which is one reason to combine it with election or reserved seats.

</details>

## Lab / assignment hook

[Lab 03, count the council](../labs/lab03.md). You count a council election under STV and block voting with the provided Python starter, measure how each group's seats move with turnout, and write a 500-word council design recommendation. It counts as one of the course's case analyses.

## Sources

- Wikipedia, "Eve Online" (accessed September 2026). CSM invitation in March 2008, partly in response to the t20 incident; first election in May 2008, 66 candidates for nine seats, composition of the first council; STV introduced with the eighth CSM with up to 14 ranked candidates; the t20 blueprint incident of 9 February 2007.
- EVE University Wiki, "Council of Stellar Management" (accessed September 2026). Ten representatives; twelve-month councils; STV, variant unspecified, Droop quota in past counts; voters rank up to as many candidates as seats, one ballot per Omega account active 30 consecutive days; eligibility (60-day account, 18+, passport, travel to Iceland, relaxed from CSM 17 in 2022); real-name rule dropped; three-year term limits from CSM 15 (2021); summit in Iceland with CCP paying travel, lodging, lunch and dinner; NDA.
- Wikipedia, "CCP Games" (accessed September 2026). October 2011 layoffs of 20% of staff after the Incarna and microtransactions controversy.
- Wikipedia, "Droop quota" (accessed September 2026). Formula, the proof that it cannot elect more than S candidates, and its use in Ireland, Northern Ireland, Malta and Australia for about a century.
- Mnookin, J. L. (1996). "Virtual(ly) Law: The Emergence of Law in LambdaMOO." *Journal of Computer-Mediated Communication* 2(1). Signature thresholds as about 5% of average votes cast; two-to-one margin.
- EVE University Wiki, "Alliance" (accessed September 2026). Executor support threshold of 50% of member corporation CEOs.
- Scharpf, F. W. (1999). *Governing in Europe: Effective and Democratic?* Oxford University Press. Input and output legitimacy.
- Hirschman, A. O. (1970). *Exit, Voice, and Loyalty*. Harvard University Press.

## Interactive spec: examples/w03-quota-and-turnout.html

**The one insight.** A bloc's seats depend on its share of ballots cast, so casual turnout, not the bloc's size, sets how many seats it wins. Under STV that dependence is a staircase. Under block voting it is a cliff.

**Layout.** Control strip on top, then two panels: seats against casual turnout (top) and a single ballot bar with quota ticks (bottom). A readout row under the bar. Stacks at 390px without horizontal page scroll.

**Controls.**
- Electorate `E`: 50,000 to 1,000,000, step 10,000, default 300,000.
- Bloc size `B`: 500 to 50,000, step 500, default 6,000.
- Casual turnout `t`: 0% to 50%, step 0.5%, default 5%.
- Seats `S`: 3 to 15, default 10.
- Rule toggle: STV (Droop) or block voting.
- Block-voting assumptions (shown only for block voting): bloc candidates `n_b` 1 to 15, default 5; opposition candidates `C_o` 5 to 60, default 20; names per casual ballot `m` 1 to `S`, default 3.
- Preset buttons for each row of the lecture's turnout table.

**Formulas.**
- `V = B + round(t × (E − B))`.
- `Q = floor(V / (S + 1)) + 1`.
- STV guaranteed seats: `min(S, floor(B / Q))`.
- Block voting (stated simplification: casual ballots spread evenly over opposition candidates): each bloc candidate gets `B`; each opposition candidate gets `t × (E − B) × m / C_o`. Bloc seats = `min(n_b, S)` if `B > t × (E − B) × m / C_o`, else 0. Show the stated assumption as a note under the chart.
- Proportional reference line: `S × B / V` (fractional), drawn dashed.

**Top panel.** Horizontal axis casual turnout 0% to 50%. Vertical axis seats 0 to `S`. Plot the chosen rule's bloc seats as a step line computed at every 0.1% of turnout, plus the dashed proportional line. Mark the current `t` with a vertical line and label the seats there. Label the turnout at which the bloc loses its last guaranteed STV seat (smallest `t` with `Q > B`).

**Bottom panel.** One horizontal bar of length `V` split into the bloc (left) and casual ballots (right). Tick marks at every multiple of `Q` along the bar, labelled 1Q, 2Q and so on. The number of ticks inside the bloc segment equals the STV guarantee.

**Readout.** `V`, bloc share of ballots (one decimal percent), `Q`, seats under the chosen rule, and seats under the other rule for comparison.

**Test values.**
- Defaults (E 300,000, B 6,000, S 10): t = 2% gives V 11,880, share 50.5%, Q 1,081, STV 5 seats. t = 5% gives 20,700, 29.0%, 1,882, 3 seats. t = 10% gives 35,400, 16.9%, 3,219, 1 seat. t = 20% gives 64,800, 9.3%, 5,891, 1 seat. t = 30% gives 94,200, 6.4%, 8,564, 0 seats.
- The last STV seat is lost at t ≈ 20.4%.
- Block voting with defaults: at t = 5%, opposition per-candidate votes 2,205, bloc wins 5 seats; at t = 20%, 8,820, bloc wins 0. The switch happens at `t = 40,000 / 294,000 ≈ 13.6%`.
- S = 7, t = 5%: Q = 2,588, STV 2 seats.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The step line and the proportional line differ by dash as well as color. Controls keyboard operable, focus visible. No animation under reduced motion. No game logos, ship art or screenshots.
