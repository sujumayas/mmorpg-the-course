# MMO305 · Week 06 — Trust and Reputation Systems

**Why this matters:** Every pickup group, trade and guild bank asks players to trust strangers. When a game can't make an exchange safe by itself, it can show players who has behaved well before. How that record adds up, and how fast it forgets, decides whether it helps good players, protects bad ones, or pushes them to make a new account.

**You will be able to:**
- Compute a reputation score from positive and negative ratings with a prior and a forgetting factor, and state its half-life.
- Predict how a score reacts to a veteran who turns bad, a good player on a bad streak, and a reformed player.
- Critique shipped reputation systems (League of Legends Honor, Final Fantasy XIV commendations, World of Warcraft's Dungeon Finder) by the memory they keep.
- Design newcomer defaults and identity costs that stop bad actors from escaping their record with a fresh account.

**Before class:** Resnick, Zeckhauser, Friedman & Kuwabara (2000), "Reputation Systems", *Communications of the ACM* 43(12), 45-48 (4 pages). Friedman & Resnick (2001), "The Social Cost of Cheap Pseudonyms", *Journal of Economics & Management Strategy* 10(2), sections 1 and 2 and the conclusion. Steinkuehler & Williams (2006), "Where Everybody Knows Your (Screen) Name", the sections on social capital.

**Prerequisites from earlier courses:** [MMO303 week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication and half-lives). [MA102 week 13, sampling and why n = 5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md). Looking ahead, [MMO401 week 8, player banks, loans and scams](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w08-player-banks-loans-and-scams.md) (year 4) covers atomic versus trust exchanges and the honesty ceiling. This course: [week 1, social capital](w01-mmos-as-societies-social-capital.md), [week 4, guilds](w04-guilds-formation-lifecycle-leadership.md), [week 5, loot rules](w05-raiding-as-organization-dkp.md).

**Interactive:** [Reputation memory](../examples/w06-reputation-memory.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. Trust, and where games need it

**Trust** is a willingness to take an action whose outcome depends on another person's later choice. You hand over the item before they pay. You pull the boss expecting the healer to heal. You deposit gold in a guild bank the leader can empty.

MMO401 week 8 gave you the first question to ask about any exchange: does the server guarantee both halves? An **atomic exchange** (a two-sided trade window, an auction house purchase) needs no trust. A **trust exchange** completes one half now and relies on a person for the other. Games are full of trust exchanges that no trade window can make atomic:

- A pickup group where a player could leave mid-dungeon, or stay and play badly on purpose.
- A loot roll where a player can claim an item they don't need (the "ninja looter").
- A crafting order where materials go to the crafter before the product comes back.
- A guild bank, where every permission is a trust decision (week 4).
- A raid spot, where the raid leader trusts you to know the fight.

### Three sources of trust

Players find reasons to trust each other in three places.

1. **The future.** If you will meet this person again, cheating them now costs you later. In game theory this is the **shadow of the future**. In a repeated game (MMO303 week 10), cooperation can be stable when the chance of meeting again is high enough. On a small server where everyone knows the regular tanks, a ninja looter is remembered.
2. **The group.** A guild tag is a promise backed by the guild. If you cheat a stranger, they can complain to your guild leader, and your guild has a reason to police you. This is the bonding social capital of week 1 turned outward.
3. **The record.** The game or the community keeps a history of how someone has behaved, and shows it to people who have never met them. This is a **reputation system**.

Resnick and colleagues (2000) named the conditions a reputation system needs to work. Identities must be long-lived, so behaviour today affects the future. Feedback about past interactions must be captured and shared. And people must actually use that feedback when deciding whom to trust. Break any one and the system turns into noise.

### When the game removes the future

World of Warcraft's Dungeon Finder, added in patch 3.3.0 (December 2009), formed 5-player groups from all realms in a battlegroup. Before it, most pickup groups came from your own realm's players. After it, you could run a dungeon with four people you would likely never see again.

In the terms above, the Dungeon Finder shrank the shadow of the future. The game added rules to replace what it removed. A group can vote to kick a player, with a higher vote count needed when three or more friends want to kick a stranger. A player who leaves before the dungeon is done receives a Deserter debuff that bars them from the queue for 30 minutes. Those are enforcement tools, not reputation. They keep no record of who you are beyond the next half hour. That design choice is the subject of this lecture's worked example: how much should the past count?

## 2. Worked example: how much should last month count?

### The hook

Two current games have reputation systems for strangers matched together, and they answer that question in opposite ways.

In **League of Legends**, players give Honor votes to up to four other players in their game who behaved well. An account's Honor level runs from 1 to 5, and level 3 is neutral. An account that receives a penalty for bad behaviour drops to level 1, however many years of good games came before, and must rebuild with fresh good behaviour.

In **Final Fantasy XIV**, after a matched duty each player may give one commendation to another member of the party who was matched with them. Commendations only add up. To become a Battle Mentor, one requirement is 1,500 commendations received. A player with 1,500 commendations who turns abusive tomorrow still has 1,500 commendations.

One system forgets everything at the first offence. The other forgets nothing and hears only good news. Which is right? Neither. Each is an extreme setting of one number, and you can compute what each setting does.

### The model

Count a player's good and bad interactions. After every match, rated good or bad:

```
r = λ × r + (1 if this match was good, else 0)
s = λ × s + (1 if this match was bad,  else 0)

score = (r + 1) / (r + s + 2)
```

- `r` is the (decayed) count of positive ratings, and `s` the count of negative ones. Both start at 0.
- `λ` (lambda) is the **forgetting factor**, between 0 and 1. Before each new match, old counts are multiplied by `λ`. With `λ = 1`, nothing is forgotten. With `λ = 0.9`, each match's weight shrinks by 10% per later match.
- The `+1` and `+2` are a **prior**: they act as one imaginary good match and one imaginary bad one. A brand-new player scores `1/2`. This is Laplace's rule of succession, and it is the expected value of a beta distribution, which is why this family is called a **beta reputation system** (Jøsang & Ismail 2002). The paper describes combining feedback through beta distributions. The forgetting factor and the particular `λ` values in this lecture are design choices for teaching, not settings taken from the paper. The prior matters for small samples, exactly the "n = 5 lies" problem of MA102 week 13. One good match gives `2/3`, not 100%.

Two numbers follow from `λ`. If a player has always behaved the same way, their counts stop growing at a total of

```
memory = 1 / (1 − λ)       matches
```

because each match adds 1 and each step shrinks the pile by the fraction `1 − λ`, the stock-and-flow balance of week 4. And a single match's weight halves after

```
half-life = ln(0.5) / ln(λ)     matches
```

With `λ = 0.9`, the memory is 10 matches and the half-life is 6.6. The score is now a statement about roughly the last ten matches.

### Numbers you can check: three matches

Take `λ = 0.9` and a player whose first three matches are good, good, bad.

| After match | `r` | `s` | Score with `λ = 0.9` | Score with `λ = 1` |
|---|---|---|---|---|
| 0 (new) | 0 | 0 | 1/2 = 0.500 | 0.500 |
| 1: good | 1 | 0 | 2/3 = 0.667 | 0.667 |
| 2: good | 0.9 × 1 + 1 = 1.9 | 0 | 2.9 / 3.9 = 0.744 | 3/4 = 0.750 |
| 3: bad | 0.9 × 1.9 = 1.71 | 1 | 2.71 / 4.71 = 0.575 | 3/5 = 0.600 |

Over three matches the two settings barely differ. The difference appears over long histories.

### Numbers you can check: four players

Run four players through each forgetting factor. "Veteran" has 100 good matches. "Turncoat" has the same 100 good matches followed by 10 bad ones. "Bad week" has 100 good then 3 bad. "Reformed" has 20 bad then 20 good.

| `λ` | Memory (matches) | Half-life | Veteran | Turncoat | Bad week | Reformed | Good matches to reach 0.70 after 20 bad |
|---|---|---|---|---|---|---|---|
| 1.00 | unlimited | unlimited | 0.990 | 0.902 | 0.962 | 0.500 | 48 |
| 0.98 | 50 | 34.3 | 0.978 | 0.782 | 0.914 | 0.593 | 30 |
| 0.95 | 20 | 13.5 | 0.954 | 0.588 | 0.824 | 0.712 | 20 |
| 0.90 | 10 | 6.6 | 0.917 | 0.374 | 0.691 | 0.826 | 12 |
| 0.80 | 5 | 3.1 | 0.857 | 0.220 | 0.509 | 0.849 | 7 |

Read the rows as a trade-off, one column at a time.

- **Turncoat.** With no forgetting, ten straight bad matches leave the score at 0.902. The long history is a shield. The player has banked enough goodwill to misbehave for weeks and still look trustworthy. With `λ = 0.9`, the same ten matches drop the score to 0.374.
- **Reformed.** With no forgetting, a player who behaved badly for 20 matches and then well for 20 is stuck at 0.500. They need 48 good matches to reach 0.70. With `λ = 0.9`, they reach 0.826, and 12 good matches would have got them to 0.70.
- **Bad week.** Forgetting has a cost. A good player who has three bad matches in a row (bad luck, a disconnect, a tilted evening) drops to 0.691 with `λ = 0.9`. With no forgetting they barely move.
- **Veteran.** Forgetting also caps the best possible score. With `λ = 0.9`, a perfect player can't exceed `(10 + 1) / (10 + 2) = 0.917`, because only about ten matches count.

There is no setting that is good at everything. **Short memory punishes turncoats and forgives the reformed, and it also punishes honest bad luck. Long memory protects honest players from noise, and it also shields turncoats and traps the reformed.** The designer is choosing which error to make.

### A visual you can move

Open the interactive. The top panel is a strip of match results you can edit: click a match to flip it between good and bad, or pick a preset (veteran, turncoat, bad week, reformed). The bottom panel plots the score after every match for two forgetting factors at once, `λ = 1` in a grey line and your chosen `λ` in colour. Pick "turncoat" and drag `λ` from 1 down to 0.8. The grey line barely dips at the end; the coloured line falls off a cliff. Then pick "bad week" and watch the same slider hurt an honest player. The readout shows memory, half-life and the current score for both lines.

### Cross-game recognition

Rewrite each shipped system in terms of `r`, `s`, the prior and `λ`.

**Final Fantasy XIV commendations (current).** Only positive ratings exist, so `s` is always 0. Nothing decays, so `λ = 1`. Each player may give one per duty, and only to players matched from outside a premade party. That last rule stops friends from boosting each other, which is a defence against **collusion**. With `s = 0`, the system can't detect a turncoat at all; it can only rank how often someone was liked. The community wiki notes that tanks and healers receive more commendations than damage dealers, so the count also measures role, not only behaviour. As a Mentor requirement, a lifetime count of 1,500 is a measure of long, well-liked service, which is what it is for.

**League of Legends Honor (current, Honor framework reworked in patch V7.13 and again in V25.04).** Honor progression depends on behaving well and receiving votes over time, and the system says it is not tied to a fixed number of votes. A penalty drops the account to level 1 and, for suspensions, locks progression for a time. In model terms, a penalty sets `r` back to 0 and restarts the climb: an **asymmetric reset**, where one bad event erases all good history. That removes the turncoat's shield completely. It also means one penalty in five years costs as much as one in five days.

**World of Warcraft Dungeon Finder (since patch 3.3.0, 2009).** The group's vote-kick is a judgment made by four strangers about the last few minutes, and the game carries no rating forward to the next group. The Deserter debuff remembers only one fact (you left) for 30 minutes. In our terms that is `λ` close to 0: memory of about one match. Short memory makes it cheap to misbehave in the next group, which is why the system leans on in-the-moment enforcement instead of reputation.

**Player banks in EVE Online (MMO401 week 8).** A banker's reputation is the asset that lets the bank grow, and the honesty ceiling showed that the reputation's value can be smaller than the vault. A long-memory reputation is exactly what a turncoat exploits. In `λ` terms, depositors trusted a record with `λ = 1` and no `s`, the same shape as FFXIV's commendations.

Four systems, one model. For any reputation system you meet, find the prior (what does a newcomer look like?), whether negative ratings exist (is there an `s`?), and how fast the past fades (what is `λ`?).

### Eyes-open design judgment

- **Pick λ from the behaviour you want to catch.** If the harm is a sudden switch (a trusted player scamming), you want short memory. If the harm is steady low-level toxicity that ratings measure noisily, longer memory averages out the noise. Write down the half-life in matches and ask whether a player would find it fair.
- **Positive-only systems are safe and blind.** They can't be used to grief someone with false reports, and they can't warn anyone about bad behaviour. Pair them with a separate reporting system (weeks 8 and 9), and don't present a positive count as a trust score.
- **Resets are clear and harsh.** Players understand "one penalty and you start over". They also learn that after a penalty, there is nothing left to protect.
- **Ratings are given by players, and players are biased.** Role bias (tanks get thanked), friendship bias, and retaliation all enter `r` and `s`. Restrict who may rate (FFXIV's matched-only rule), limit how many ratings each player gives, and weight ratings from raters who themselves rate sensibly.
- **Every visible score is a target.** Once a score gates rewards (Mentor status, Honor rewards), players optimize for the score. Hide the exact number or show only coarse levels if you want behaviour rather than score-farming.

### Check yourself (worked example)

1. With `λ = 0.95`, what is the highest score a player who is always good can approach? What is the half-life in matches?
2. A player with `λ = 0.9` has `r = 8`, `s = 1`. They play one bad match. What is their new score?
3. A designer wants a single bad match to cost a perfect player (at the steady state) no more than 0.10 of score. Is `λ = 0.9` acceptable?

<details>
<summary>Answers</summary>

1. Memory is `1 / 0.05 = 20`, so the ceiling is `21 / 22 ≈ 0.955`. Half-life `ln 0.5 / ln 0.95 ≈ 13.5` matches.
2. `r = 0.9 × 8 = 7.2`, `s = 0.9 × 1 + 1 = 1.9`. Score `8.2 / 11.1 ≈ 0.739`.
3. At the steady state `r = 10`, `s = 0`, score `11/12 ≈ 0.917`. After one bad match `r = 9`, `s = 1`, score `10 / 12 ≈ 0.833`. The drop is 0.083, which is under 0.10, so yes.

</details>

## 3. The newcomer problem and cheap identities

The model has a flaw that has nothing to do with `λ`. Look at a player who behaves badly every match with `λ = 0.9`. Their score settles at `(0 + 1) / (10 + 2) = 0.083`. A brand-new account scores 0.500. **A bad player can raise their reputation six-fold by abandoning their account.** This is **whitewashing**, and in a free-to-play game where accounts cost nothing, it is the rational move.

Friedman and Resnick (2001) studied this exact situation with a game-theory model: many players, random matching, and the ability to change identity freely. Their result is uncomfortable. When identities are cheap, the best society can do is a convention where **newcomers pay their dues**: established players treat unknown players with suspicion until they prove themselves. No equilibrium does much better. Being kind to newcomers invites every bad actor to become a newcomer.

They describe two ways out, both with costs:

- **Entry fees.** Make a new identity cost something. Then newcomers can be trusted up to the value of the fee. A subscription, a box price or a phone number are all entry fees. Overwatch 2 launched in October 2022 requiring SMS phone verification, partly to make throwaway accounts harder to create; Blizzard relaxed the requirement within days for players with older accounts. The fee also keeps out honest players who can't or won't pay it.
- **Unreplaceable identities.** Tie reputation to something a player can't easily get more of. Account-level rather than character-level reputation is the game version.

In the model, you have a third lever: **the prior**. Replace `(r + 1) / (r + s + 2)` with

```
score = (r + a) / (r + s + a + b)
```

A newcomer scores `a / (a + b)`. With `a = 1`, `b = 3`, a newcomer starts at 0.25, below where most honest players sit but still above the worst. Now whitewashing gains less, and every newcomer, honest or not, starts out paying dues. That is Friedman and Resnick's dues-paying convention built into the formula. You have decided who pays for the bad actors, and it is the new players. Week 11 on newcomers is largely about how to make that cost bearable.

## 4. What a reputation system should show

Computing a score is half the job. Deciding what players see is the other half.

- **Number or level?** Showing 0.742 invites comparison and farming. Showing a level (League's 1 to 5) or a badge hides noise and makes thresholds visible. Levels need hysteresis, a gap between the score that earns a level and the score that loses it, or players near a boundary flicker between levels.
- **Public or private?** A public score helps strangers decide whom to trust, which is its purpose. It also stigmatizes, and a low public score can become a reason for others to treat a player worse, which lowers the score further. A private score used only by matchmaking can steer bad actors toward each other without labelling them.
- **Who does it gate?** Tie a score to chat privileges (League's low levels restrict chat) and it becomes enforcement. Tie it to cosmetics (League's Honor rewards) and it becomes motivation. Tie it to responsibility (FFXIV's Mentors guide new players) and it becomes a selection process for community roles.

The guild of week 4 is also a reputation carrier. A guild tag tells strangers "my guild vouches for me". Guilds that care about their name police members, which is trust from the group, the second source in section 1. A good reputation system can build on that instead of replacing it: for example, by letting guilds see their members' standing, or by showing a guild's collective record.

## In-class activity (25 minutes)

Groups of three. Your MMO has cross-server 4-player dungeons with matchmaking, free-to-play accounts and no current reputation system.

1. Choose `λ`, `a` and `b`. Write the newcomer score, the ceiling for a perfect player, and the half-life.
2. Use the interactive to find how many bad matches drop a perfect player below 0.5 under your settings. Is that fair?
3. Decide what the score gates (matchmaking, chat, rewards, nothing visible) and whether it is shown as a number, a level or not at all.
4. Name the cheapest attack on your system (whitewashing, collusion, retaliation, role bias) and one rule that makes it more expensive.

Expected output: a one-page spec with your three parameters, the numbers from steps 1 and 2, the gating decision and the attack with its counter.

## Common misconceptions

- **"More history makes a reputation more accurate."** More history makes it more stable. If behaviour changes, a long memory is accurate about the past and wrong about the present.
- **"A new player should start at neutral."** A neutral start is generous to newcomers and to whitewashers alike. Where the prior sits is a decision about who pays for bad actors.
- **"Commendation counts measure trustworthiness."** Positive-only counts measure how often someone was thanked, which mixes behaviour, role and time played. They can't show bad behaviour at all.
- **"Resets are the fairest system because the rule is simple."** Simple rules are clear. A reset treats one penalty in five years like one in five days, and it leaves a penalized player nothing to protect.

## Check yourself

1. A player's history with `λ = 0.9` gives `r = 6`, `s = 3`. Compute their score. If they now play four good matches in a row, what is the new score?
2. Your game uses `(r + 1)/(r + s + 2)` with `λ = 0.95`. A player who always behaves badly makes a new account. By how much does their score rise?
3. You change the prior to `a = 1`, `b = 4`. What does a newcomer score now, and what is the ceiling for a perfect player with `λ = 0.95`?
4. A game's reputation shows only positive "kudos" with no decay. Players complain that a known scammer has a high kudos count. Explain in model terms why the system can't catch them, and propose the smallest change that would.

<details>
<summary>Answers</summary>

1. Score `7 / 11 ≈ 0.636`. After four good matches: `r = 6 × 0.9⁴ + (0.9³ + 0.9² + 0.9 + 1) = 6 × 0.6561 + 3.439 = 7.376`, `s = 3 × 0.6561 = 1.968`. Score `8.376 / 11.344 ≈ 0.738`.
2. The steady state for always-bad is `r = 0`, `s = 20`, score `1/22 ≈ 0.045`. A new account scores 0.5. The rise is about 0.455, an elevenfold gain.
3. Newcomer `1/5 = 0.20`. Ceiling `(20 + 1)/(20 + 5) = 0.84`.
4. The system has no `s` and `λ = 1`, so kudos only accumulate and nothing the scammer does lowers the count. The smallest change is to add negative ratings (an `s` term) with at least a moderate forgetting factor, so the score reflects recent behaviour and not only lifetime thanks.

</details>

## Lab / assignment hook

[Lab 06, reputation replay](../labs/lab06.md). You replay a log of 60 matched games for eight fictional players through three reputation designs, find which design misjudges which player, and write a recommendation. It also prepares the griefing and toxicity work of weeks 8 and 9.

## Sources

- Resnick, P., Zeckhauser, R., Friedman, E. & Kuwabara, K. (2000). "Reputation Systems." *Communications of the ACM* 43(12), 45-48. doi:10.1145/355112.355122. Conditions for reputation systems: long-lived identities, captured and shared feedback, feedback that guides decisions.
- Friedman, E. J. & Resnick, P. (2001). "The Social Cost of Cheap Pseudonyms." *Journal of Economics & Management Strategy* 10(2), 173-199. doi:10.1111/j.1430-9134.2001.00173.x. Dues-paying equilibrium, entry fees, unreplaceable pseudonyms.
- Jøsang, A. & Ismail, R. (2002). "The Beta Reputation System." *Proceedings of the 15th Bled Electronic Commerce Conference* (BLED 2002). Beta-distribution reputation from positive and negative ratings (verified against the abstract; some indexes list the authors in the reverse order). The forgetting factor as used here, and all `λ` values, are this lecture's design choices. See also Jøsang, A., Ismail, R. & Boyd, C. (2007), "A Survey of Trust and Reputation Systems for Online Service Provision," *Decision Support Systems* 43(2), 618-644.
- Steinkuehler, C. A. & Williams, D. (2006). "Where Everybody Knows Your (Screen) Name: Online Games as 'Third Places'." *Journal of Computer-Mediated Communication* 11(4), 885-909. doi:10.1111/j.1083-6101.2006.00300.x.
- Final Fantasy XIV Wiki (consolegameswiki), "Player Commendation" and "Mentor System and Novice Network" (current, Dawntrail era). One commendation per duty to a matched party member; not to members of a fully premade party; tanks and healers receive more; Battle Mentor requires 1,500 commendations and 1,000 completed duties among other achievements.
- League of Legends Wiki, "Honor" (current). Levels 1 to 5 with level 3 neutral; votes for well-behaved players; progression not tied to a fixed vote count; penalties drop the account to level 1 and suspensions lock progression; system launched 2012, reworked in patch V7.13 and consolidated in V25.04.
- Warcraft Wiki, "Dungeon Finder". Added in patch 3.3.0; groups formed from all realms in a battlegroup; vote-kick with 4 votes needed when 3 or more friends kick a stranger; 30-minute Deserter debuff.
- Wikipedia, "Overwatch 2" (accessed 2026). SMS phone verification required at launch in October 2022 as an anti-smurfing measure, relaxed within days for accounts active since June 2021.
- Worked-example values computed by the author from the model as stated.

## Interactive spec: examples/w06-reputation-memory.html

**The one insight:** the forgetting factor `λ` trades one error for another. Short memory drops a turncoat fast and forgives a reformed player, and it also punishes a good player's bad streak. Long memory does the reverse. Seeing the same history scored by `λ = 1` and by a chosen `λ` side by side makes the trade-off visible.

**Layout.** Top: a match strip. Middle: the score chart. Right (1280px) or below (390px): controls and readouts.

- **Match strip.** Up to 150 cells in a row (wrapping on mobile), each good (filled, "good" token colour) or bad (outlined, "bad" token colour with a cross so it isn't colour-only). Clicking or pressing Enter/Space on a focused cell flips it. Arrow keys move focus.
- **Score chart.** x-axis match number 0 to history length, y-axis score 0 to 1. Grey line: score with `λ = 1`. Coloured line: score with the chosen `λ`. Dashed horizontal line at the newcomer score `a/(a + b)`. Optional dotted line at the ceiling `(1/(1 − λ) + a)/(1/(1 − λ) + a + b)` for `λ < 1`.

**Controls.**

- `λ` slider 0.50 to 1.00, step 0.01, default 0.90.
- Prior `a` 0.5 to 5, step 0.5, default 1; prior `b` 0.5 to 5, step 0.5, default 1.
- Presets: "Veteran" (100 good), "Turncoat" (100 good, 10 bad), "Bad week" (100 good, 3 bad), "Reformed" (20 bad, 20 good), "Always bad" (100 bad), "Random 90%" (100 matches each good with probability 0.9, seeded, with Reroll).
- "Add good" and "Add bad" buttons append one match; "Clear".
- "Whitewash" button: shows a second coloured marker at the newcomer score next to the current score, with the gain printed.

**Formulas.**

```
r0 = s0 = 0
for each match m:  r = λ r + [m good];  s = λ s + [m bad]
score = (r + a) / (r + s + a + b)
memory = 1 / (1 − λ)     (show "unlimited" at λ = 1)
half-life = ln 0.5 / ln λ    (show "unlimited" at λ = 1)
```

**Readouts.** Current score for `λ = 1` and for the chosen `λ`, memory, half-life, newcomer score, ceiling, and the whitewash gain `a/(a + b) − current score` when negative scores make it positive.

**Test values** (`a = b = 1`), all to three decimals:

| Preset | `λ = 1` | `λ = 0.95` | `λ = 0.90` | `λ = 0.80` |
|---|---|---|---|---|
| Veteran | 0.990 | 0.954 | 0.917 | 0.857 |
| Turncoat | 0.902 | 0.588 | 0.374 | 0.220 |
| Bad week | 0.962 | 0.824 | 0.691 | 0.509 |
| Reformed | 0.500 | 0.712 | 0.826 | 0.849 |
| Always bad | 0.010 | 0.046 | 0.083 | 0.143 |

Three-match check at `λ = 0.9`: good, good, bad gives 0.667, 0.744, 0.575. Half-life at `λ = 0.9` shows 6.6; memory 10.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. Match cells are real buttons with `aria-pressed`. Chart has a text summary of both final scores. Respect `prefers-reduced-motion` and `prefers-color-scheme`. No game logos or art; presets are behaviour patterns, not named games.
