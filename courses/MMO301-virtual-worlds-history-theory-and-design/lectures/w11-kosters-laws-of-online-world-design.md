# MMO301 · Week 11 — Koster's Laws of Online World Design

**Why this matters:** Every MMO team relearns the same painful lessons: players find every loophole, a few people ruin things for many, and nobody reads the patch notes the way you meant them. In the late 1990s the designers of text MUDs and the first graphical worlds wrote those lessons down as short "laws." This week you learn to read them as testable claims, and to put numbers on the most important family of them: the laws that say "with enough players, someone will."

**You will be able to:**
- Explain where Koster's Laws came from, how they are organized, and why they read as aphorisms rather than theorems.
- Compute the probability that a loophole is found, or a troublemaker is present, using `1 − (1 − q)^H ≈ 1 − e^(−qH)`, and compare a test team's exposure to a launch population's.
- Estimate how the number of possible system interactions grows with the number of systems, and use it to argue for or against adding a feature.
- Critique a feature design against at least five named laws and state which law each risk comes from.

**Before class:** Koster, "The Laws of Online World Design" (raphkoster.com), the whole page; it is short, about 20 minutes. Bartle, *Designing Virtual Worlds* (2003, free CC edition), chapter 4, "Reset Strategy" (the opening paragraphs on content consumption).

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) is the whole model of section 2, applied to players instead of drops. [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) gives the "expected wait is `1/p`" result. [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) covers `e^x`. [GD102 week 12, emergent behavior from simple rules](../../GD102-systems-design-and-game-mechanics/lectures/w12-emergent-behavior-from-simple-rules.md) explains why interactions between systems surprise their designers. [GS101 week 9](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) tells the Ultima Online story this lecture opens with. Within this course, [week 3 (Ultima Online)](w03-ultima-online-the-simulation-dream-and-its-limits.md) and [week 8 (Bartle's player types)](w08-player-types-bartle-1996-and-the-heros-journey.md) come first.

**Interactive:** [examples/w11-someone-will.html](../examples/w11-someone-will.html). Keep it open during section 2.

---

## 1. Where the Laws came from

In the late 1990s the people building online worlds talked to each other on a mailing list called MUD-Dev. Raph Koster, then a designer on Ultima Online, collected the list's hard-won rules of thumb in an email exchange with J.C. Lawrence, then asked the list for more. The collection was presented at Game Developers Conference roundtables starting in 1999 and has lived on Koster's website since. Many laws carry the name of the person who first said them, partly as a joke. Koster notes that the attribution of many has been lost.

The page is organized in three parts: design rules, modes of expression, and social laws. The laws are short. Most are one or two sentences. That is their strength and their weakness. They are memorable, and they are vague enough that anyone can agree with them after the fact.

The collection even includes a law about the laws. Ola's Law, from Ola Frosheim Grostad, says in effect that general laws are there to challenge a designer's thinking, not to hand them answers. Take that seriously. This lecture treats each law as a claim you can test, and asks what it would take for it to be false.

### A map of the collection

Here is a selection, paraphrased and grouped by what they are about. Read the originals on Koster's page; they are more pointed than any paraphrase.

| Family | Law | Paraphrase |
|---|---|---|
| Population | Hyrup's Loophole Law | Anything that can be exploited will be. |
| Population | John Hanke's Law | Any online population contains a fixed share of troublemakers that you cannot get rid of. |
| Population | Koster's Law | The quality of role-play falls as the number of players rises. |
| Population | Lambert's Laws | The more actions a world allows, the more ways it can be exploited; bored players become willing subverters; players take the most efficient path to rewards. |
| Expectations | Schubert's Law of Player Expectations | New players expect a single-player story in which other players will not interfere. |
| Expectations | Darklock's Laws | Cheating is an advantageous violation of what other players assumed; once one assumption is broken, players feel entitled to break others. |
| Communication | Dundee's Law | Players' names for things win over the designers' names. |
| Communication | Staerfeldt's Law and Hal Black's Elaboration | The more you pamper players, the more they complain; whatever feedback you respond to, you get more of. |
| Community | Baron's Theorem | Shared conflict builds community. |
| Persistence | Design rule on persistence | Once a world opens, players expect it never to close. |
| Identity | Design rule on identity | Players carry the same identity across games for years, so a character system alone does not keep them. |

Weeks 8 and 9 of this course studied why players play. The Laws are the other half: what happens when those players arrive in numbers. The first family, the population laws, is the most useful because it has a precise mathematical core. That core is this week's worked example.

## 2. Worked example: "someone will"

### The hook

On 9 August 1997, during a server stress test in Ultima Online's beta, a player called Rainz killed Lord British, the in-game character of the game's creator, Richard Garriott. Lord British was supposed to be invulnerable. After a server crash, that protection did not come back, and Rainz cast a fire field spell on him. Rainz's account was banned from the beta soon after. The published accounts say it was for repeatedly exploiting bugs instead of reporting them, and Origin said the ban was not for the assassination itself.

The story gave players a rule they still quote, sometimes called the Lord British Postulate: if something in the world can be killed, someone will try to kill it. Koster's page has the design version in Hyrup's Loophole Law: if it can be exploited, it will be.

Here is the puzzle. Origin's own staff had been playing that world for months. The invulnerability flag had failed only briefly. How did a single beta player find a gap that the whole team missed? You do not need to assume Rainz was a genius. You need arithmetic.

### The model

Suppose a loophole exists, and each hour one player spends in the world gives a tiny chance `q` that they find it (and try it). Players are independent. Over a total of `H` player-hours of play:

```
P(found at least once) = 1 − (1 − q)^H  ≈  1 − e^(−qH)
expected number of discoveries  E = qH
```

- `q` is the chance per player-hour. It can be very small: one in a hundred thousand is `q = 0.00001`.
- `H = N × h` is total player-hours: `N` players each playing `h` hours.
- The approximation `(1 − q)^H ≈ e^(−qH)` holds whenever `q` is small, which it always is for loopholes worth worrying about.

If `C` players are online at the same moment, the expected wall-clock wait until the first discovery is:

```
expected wait (hours) = 1 / (C × q)
```

That is the geometric-distribution result from MA102 week 7, with "one player-hour" as the trial.

The whole model says one thing: **what matters is `qH`, not `q`.** A tiny per-player chance multiplied by a huge number of player-hours is a near-certainty.

### Numbers you can check

Take one loophole with `q = 0.00001` (one discovery per 100,000 player-hours). All the populations below are invented, but they are realistic in scale for a mid-sized MMO.

| Who is playing | Players `N` | Hours each `h` | Player-hours `H` | `E = qH` | P(found) |
|---|---|---|---|---|---|
| Internal QA team | 20 | 200 | 4,000 | 0.04 | 3.9% |
| Closed beta | 2,000 | 20 | 40,000 | 0.4 | 33.0% |
| Launch day | 100,000 | 3 | 300,000 | 3 | 95.0% |
| Launch week | 100,000 | 20 | 2,000,000 | 20 | more than 99.99% |

Check the launch-day row: `1 − e^(−3) = 1 − 0.0498 = 0.950`.

Now look from one player's side. A single player in their first three hours has a chance of `3 × 0.00001 = 0.003%`. From their seat, the loophole is invisible. From the world's seat, it is almost certain to be found on day one. The QA team's four thousand careful hours are 1.3% of the launch day's player-hours.

With 30,000 players online at peak on launch day, the expected wait for the first discovery is `1 / (30,000 × 0.00001) = 3.3` hours.

How sensitive is this to `q`? You rarely know `q`, so look at a range:

| `q` per player-hour | QA (4,000 h) | Beta (40,000 h) | Launch day (300,000 h) | Launch week (2,000,000 h) |
|---|---|---|---|---|
| 1 in 1,000,000 | 0.4% | 3.9% | 25.9% | 86.5% |
| 1 in 100,000 | 3.9% | 33.0% | 95.0% | ~100% |
| 1 in 10,000 | 33.0% | 98.2% | ~100% | ~100% |

Even a loophole so obscure that it takes a million player-hours per discovery is more likely than not to be found in the first week. That is Hyrup's Loophole Law with numbers on it. It is also why "we tested it" means very little for a rare edge case. QA teams find the common bugs. Players find the rare ones.

### The same model, applied to people

John Hanke's Law says that every online population has a share of troublemakers you cannot remove. Call that share `f`. In a group of `n` players, the chance that at least one is a troublemaker is:

```
P(at least one) = 1 − (1 − f)^n
```

Same shape, different question. With `f = 1%`:

| Group | Size `n` | Expected troublemakers `f × n` | P(at least one) |
|---|---|---|---|
| Small party | 5 | 0.05 | 4.9% |
| Two parties | 10 | 0.1 | 9.6% |
| Raid | 40 | 0.4 | 33.1% |
| Busy town square | 100 | 1 | 63.4% |
| Full server | 2,000 | 20 | ~100% |

Koster's own law, that role-play quality falls as population rises, is the same arithmetic. One player who breaks character in a scene breaks it for everyone in the scene. If a share `f` of players will not role-play, a scene with `n` people survives intact with chance `(1 − f)^n`, and that falls as scenes grow. Small groups can keep a fiction alive. Crowds cannot.

This gives you a rule of design: **do not design systems whose worst case needs zero bad actors.** If a system only works when nobody in a group of 40 misbehaves, a 1% troublemaker rate breaks one raid in three.

### A visual you can move

Open `examples/w11-someone-will.html`. The left view, "One player's chance," shows a single bar for `q × h`, which is almost empty. The right view, "The world's chance," plots P(found) against total player-hours on a logarithmic axis, with markers for QA, beta, launch day and launch week. Drag `q` down to one in a million. The left bar becomes invisible. The right curve slides to the right but the launch-week marker stays above 85%. Then switch to the "People" tab and drag the group size from 5 to 40 with `f = 1%`. The same S-shaped curve appears, now with raids on it instead of launches.

### Cross-game recognition

**World of Warcraft, the Corrupted Blood incident (13 September to 8 October 2005).** When the Zul'Gurub raid opened, its final boss, Hakkar the Soulflayer, cast a debuff called Corrupted Blood that spread to nearby characters. It was meant to stay in the raid. But players' pets could carry it: a player could dismiss an infected pet and summon it again in a city, where it spread to crowds. The designers had not built a way to clear the debuff when the pet left the raid. Some players then spread it deliberately, travelling to crowded cities to infect others. Blizzard tried fixes for about a week and resolved it with a hard reset and a patch that made pets immune. In our model, the combination of pet dismissal and this debuff was one loophole with small `q`. Millions of player-hours in the days after the patch made its discovery certain. And the deliberate spreaders are Hanke's troublemakers: once the loophole existed, `f` did the rest. The incident was later studied by epidemiologists (Lofgren and Fefferman, 2007) because players' reactions to a spreading plague looked like real human behaviour.

**RuneScape, the Falador Massacre (5 to 6 June 2006, World 111).** A bug in player-owned houses let some players keep their player-versus-player attack option after leaving a house's combat area. They could attack players anywhere, in places the game treated as safe. They went through towns killing players, and one, Durial321, targeted wealthy players to take their items. As news spread, World 111 filled to its 2,000-player limit with people coming to watch. The exact mechanism was never identified. That is the model's prediction exactly. Nobody on the team could find it by looking. A large population found it by playing.

**Ultima Online's Lord British, again.** In the model's terms, the gap was a short window (invulnerability missing after a crash) and a very common action (casting an offensive spell at a character). `q` per player-hour near the right place was not small at all. The world just needed one player there at the right time who chose to act. The reported reason for Rainz's ban, exploiting rather than reporting, shows the other half of the story: `q` has two parts, finding the loophole and choosing to use it.

Three games, three decades apart in engine technology, one idea: `qH` large means certain.

### Eyes-open design judgment

What should a designer do with this, knowing that "test harder" will never close the gap?

- **Design the failure, not only the feature.** Ask what the worst version of this feature looks like if one player in a thousand uses it maliciously. If that worst case is a disaster (players killable in safe zones, a plague in the capital), add a hard limit. Corrupted Blood needed only a rule that the debuff cannot exist outside the raid instance.
- **Make discovery report-shaped.** You cannot stop players from finding loopholes. You can make reporting better than exploiting: bug bounties, public credit, and clear, enforced penalties for exploiting. Ultima Online's ban of Rainz was that message.
- **Put detection where `qH` is largest.** Telemetry that flags impossible states (a debuff outside its zone, a combat flag outside a combat area) finds the loophole in hours instead of days. [MMO309](../../MMO309-security-anti-cheat-and-anti-bot/syllabus.md) covers detection in depth.
- **Plan the rollback before you need it.** Some loopholes will be found in ways that damage the economy or other players. Decide in advance what you will roll back and what you will let stand. [MMO401 week 12](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w12-economic-shocks-exploits-and-rollbacks.md) treats this for economic exploits.
- **Do not over-read the law.** "Anything that can be exploited will be" does not mean every exploit is a crisis. Most loopholes are minor. Spend effort where the damage from `qH` discoveries is large, not on every conceivable edge.

### Check yourself (worked example)

1. A loophole has `q = 0.000002` per player-hour. Your closed beta has 5,000 players playing 10 hours each. What is the chance the beta finds it?
2. At launch you expect 50,000 players online at peak. With the same `q`, how long until the first expected discovery at that concurrency?
3. A dungeon mechanic fails if any one of 25 players intentionally stands in the wrong place. With `f = 2%`, what share of 25-player groups will have at least one player who might do it?

<details>
<summary>Answers</summary>

1. `H = 50,000`, `qH = 0.1`, `P = 1 − e^(−0.1) = 9.5%`.
2. `1 / (50,000 × 0.000002) = 10` hours.
3. `1 − 0.98^25 = 1 − 0.603 = 39.7%`, about two groups in five.

</details>

## 3. Lambert's Laws: why every feature adds more than one risk

Jon Lambert's first two laws say that the more actions a world allows, the more ways it can be exploited. The reason is that features combine.

Corrupted Blood was not a bug in pets and not a bug in the debuff. Each worked as designed. The loophole was in the pair. If a world has `A` systems (combat flags, pets, housing, debuffs, trading, travel), the number of pairs is:

```
pairs = A (A − 1) / 2
```

Suppose each pair has a small chance `r = 0.1%` of hiding an exploitable interaction. The chance that at least one pair does is `1 − (1 − r)^pairs`.

| Systems `A` | Pairs | Expected exploitable pairs | P(at least one) |
|---|---|---|---|
| 5 | 10 | 0.01 | 1.0% |
| 10 | 45 | 0.045 | 4.4% |
| 20 | 190 | 0.19 | 17.3% |
| 50 | 1,225 | 1.2 | 70.6% |
| 100 | 4,950 | 5.0 | 99.3% |

Going from 50 systems to 100 doubles the features and multiplies the pairs by four. And this counts only pairs. Three-way interactions grow faster still. The Falador Massacre involved at least three: the house, the combat option, and the world outside.

Two practical consequences follow:

- **Isolation is a design tool.** Every rule that stops two systems from touching removes pairs. "Pets are reset when they leave an instance" and "combat flags are cleared at the door" are boring rules that delete whole rows of this table.
- **Late features are the riskiest.** A system added in year three interacts with every system that already exists. It is also the one least tested against all of them.

GD102 week 12 showed how simple rules produce emergent behaviour you did not design. Lambert's Laws are the same observation from the operator's side: emergent behaviour includes emergent exploits.

## 4. The laws about expectations and communication

Not every law is about numbers. The others are about the gap between what the designer meant and what players believe.

**Schubert's Law of Player Expectations** says that new players arrive expecting a single-player story in which other players will not get in their way. This is why the first player killing, the first stolen kill and the first camped spawn feel like betrayal to a new player, even when the world was designed for it. The design response is to teach the shared-world rules early and gently, or to build starting areas where the single-player expectation is true for a while.

**Darklock's Laws** define cheating as an advantageous violation of other players' assumptions, and warn that once one assumption is broken, players feel free to break the rest. The practical reading: the rules players believe in are part of your game, whether you wrote them or not. If players assume the capital city is safe and it is not, the Falador Massacre feels like cheating even though the game allowed it.

**Dundee's Law** says the players' names for things will win. If players call your "Instanced Cooperative Challenge Zones" dungeons, they are dungeons, and your user interface should say so. This matters for tutorials, patch notes and support: you communicate in your players' language or you do not communicate.

**Staerfeldt's Law and Hal Black's Elaboration** say that pampering produces complaining, and whatever feedback you respond to, you get more of. If you change a class every time its forum thread gets loud, you are training players that loud threads work. [MMO303 week 14](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md) treats communicating balance changes.

**The persistence rule** says once a world opens, players expect it never to close. That shapes everything from how you store data to how you plan a shutdown. [Week 12](w12-persistence-and-time-what-should-last.md) takes up what should last, and [week 13](w13-worlds-that-died-shutdowns-and-their-lessons.md) looks at worlds that did close.

## 5. Using the Laws in a design review

The Laws are most useful as a checklist in review. For any new feature, go through the families and ask one question each.

| Family | Question to ask of the feature |
|---|---|
| Loophole | If one player in 100,000 finds the worst use of this in an hour, what happens by the end of launch week? |
| Troublemakers | What happens if one member of the group is hostile? Does the feature still work? |
| Interactions | Which existing systems can touch this one? Can you isolate it from the ones you do not need? |
| Expectations | What will a new player assume this does? What happens when that assumption breaks? |
| Communication | What will players call it? Does your UI use that name? |
| Persistence | Once this exists, can you ever take it away? |

Remember Ola's Law. The table does not produce answers. It produces questions that someone must answer in writing before the feature ships. And remember the era. The Laws were written by designers of text MUDs and the first graphical worlds, with populations in the hundreds to hundreds of thousands. The population laws have only become stronger as worlds grew to millions of players. Some others, such as those about role-play, describe a community that most modern MMOs no longer design for.

## In-class activity (25 minutes)

Groups of four. Each group receives one invented feature brief from the instructor, such as "players can place a campfire anywhere that heals everyone nearby," "guilds can declare war on each other in any zone," or "players can adopt any creature as a pet, including bosses after they are defeated."

1. **(10 min)** Run the design-review table from section 5 on your feature. For the loophole row, write the worst plausible exploit and guess `q` as a range (for example, one in 10,000 to one in a million player-hours).
2. **(5 min)** Using the interactive, find the probability your exploit is found by launch day and by launch week at both ends of your range, for a launch of 50,000 players playing 4 hours on day one and 25 hours in the week.
3. **(10 min)** Propose one isolation rule that removes the exploit's worst case without removing the feature. Swap with another group and try to break their rule.

Expected output: the filled review table, two probabilities per end of the range, and one isolation rule with the other group's attempt to break it.

## Common misconceptions

- **"We tested it thoroughly, so the rare bug won't show up."** Testing multiplies `q` by the test team's hours. Launch multiplies it by the players' hours, which are 100 to 1,000 times larger. Rare bugs are found by players.
- **"If only a tiny share of players are troublemakers, groups will be fine."** The chance of at least one grows fast with group size. At `f = 1%`, a third of 40-player raids have one.
- **"The Laws are rules to follow."** They are compressed experience from a specific era, meant to provoke. Treat each as a claim, test it against your world, and write down when you choose to break it.
- **"Adding one feature adds one risk."** It adds as many new pairs as there are existing systems. The hundredth feature adds 99.

## Check yourself

1. A studio has 50 testers who each play 300 hours before launch. The loophole has `q = 0.000005` per player-hour. What is the chance QA finds it? What is the chance 80,000 players find it on launch day if each plays 2.5 hours?
2. A raid mechanic needs all 20 players to cooperate. If `f = 1.5%` of players will deliberately fail it, what share of raid groups is at risk? What if the raid is cut to 10 players?
3. Your world has 30 systems. The team proposes adding 6 more. How many new pairs of systems does that create?
4. Pick one law from section 4 and describe a situation in a game you know where it held. Then describe one design that would make it false.
5. The Lord British story is often told as "players are malicious." Using the model, give a better explanation for why it happened in a stress test rather than in months of internal play.

<details>
<summary>Answers</summary>

1. QA: `H = 15,000`, `qH = 0.075`, `P = 1 − e^(−0.075) = 7.2%`. Launch day: `H = 200,000`, `qH = 1`, `P = 1 − e^(−1) = 63.2%`.
2. 20 players: `1 − 0.985^20 = 1 − 0.739 = 26.1%`. 10 players: `1 − 0.985^10 = 1 − 0.860 = 14.0%`. Halving the group nearly halves the risk.
3. Before: `30 × 29 / 2 = 435`. After: `36 × 35 / 2 = 630`. New pairs: 195. Six features added 195 new pairs.
4. Answers vary. A good answer names the law, the game and era, the observed behaviour, and a design change with a mechanism (for example, Dundee's Law held when players gave a zone their own nickname and ignored the official one; a UI that adopts the players' term ends the contest instead of losing it).
5. A stress test puts many players in the world at once, raising `H` sharply, and crashes are more likely under stress, which briefly created the gap (invulnerability not restored). A large `qH` during a short window made discovery likely. It needed only one player in the window willing to act, which is Hanke's share of troublemakers, not a malicious population.

</details>

## Lab / assignment hook

[Lab 11, the laws review](../labs/lab11.md). You receive a one-page feature brief for an invented MMO feature, run a full laws review, compute exposure numbers for three populations, and write an isolation plan. It also prepares the "risks" section of your world design bible.

## Sources

- Koster, R., "The Laws of Online World Design" (raphkoster.com, page updated 2023) and its introduction page (updated 2014). Collected from the MUD-Dev mailing list with J.C. Lawrence; presented at GDC roundtables from the 1999 Austin Roadtrip onward; lost attributions. Laws paraphrased in section 1 and 4: Ola's Law, Hyrup's Loophole Law, John Hanke's Law, Koster's Law, Lambert's Laws, Schubert's Law, Darklock's Laws, Dundee's Law, Staerfeldt's Law, Hal Black's Elaboration, Baron's Theorem, and the design rules on persistence and identity.
- Wikipedia, "Ultima Online" (accessed September 2026). Lord British killed by the player Rainz with a fire field during a beta stress test on 9 August 1997 after his invulnerability did not persist through a server crash; Rainz banned from the beta for exploiting rather than reporting bugs, with Origin saying the ban was not for the killing itself; launch on 24 September 1997. Wikipedia's source for the beta account is Computer Gaming World no. 220 (November 2002), "Five Biggest Moments in UO History," p. 104; the archived scan could not be read for this review, so treat the details as the commonly reported account.
- Wikipedia, "Lord British" (accessed September 2026). The "Lord British Postulate" as a players' principle that any killable creature will be attacked.
- Wikipedia, "Corrupted Blood incident" (accessed September 2026). 13 September to 8 October 2005 in World of Warcraft; Hakkar the Soulflayer in Zul'Gurub; spread by pets; deliberate spreading; resolved by resets and a patch making pets immune.
- Lofgren, E. T. & Fefferman, N. H. (2007). "The untapped potential of virtual game worlds to shed light on real world epidemics." *The Lancet Infectious Diseases* 7(9), 625-629.
- RuneScape Wiki, "Falador Massacre" (accessed September 2026). 5 to 6 June 2006 on World 111; attack option carried out of player-owned houses; Durial321; world filled to its 2,000-player limit; mechanism never identified.
- Bartle, R. A. (2003). *Designing Virtual Worlds*. New Riders, free CC edition. Chapter 4, "Reset Strategy": players consume content faster than it can be produced.

## Interactive spec: examples/w11-someone-will.html

**The one insight:** a per-player chance that looks like zero becomes a near-certainty across a launch population. What matters is `qH`, and the curve `1 − e^(−qH)` is the same whether the event is a loophole found or a troublemaker present.

**Layout.** Two tabs, "Loopholes" (default) and "People." Each tab has two linked views, side by side on desktop, stacked on mobile.

**Loopholes tab.**

- **Left view, "One player's chance":** one vertical bar from 0 to 100% showing `1 − e^(−q × h_launch_day)` for a single player, with its exact value printed beside it to 4 significant figures in percent. It should look empty at default settings; add a 100× zoom inset (a second bar on the scale 0 to 1%) so the student can see it is not zero.
- **Right view, "The world's chance":** line chart of P(found) (0 to 100%) against total player-hours `H` on a log axis from 100 to 10,000,000. Plot `1 − e^(−qH)`. Draw four vertical markers, labelled, for QA, Beta, Launch day and Launch week, at their `H` values, each with its P value printed next to it. Draw a horizontal dashed line at 50%, with its crossing `H = ln 2 / q` labelled.
- **Readouts (copyable):** for each of the four populations, `H`, `E = qH` (3 decimals), P (1 decimal percent, "more than 99.99%" above that). Plus "Expected wait at peak concurrency: X.X hours" `= 1 / (C × q)`.

**Loopholes controls:**

1. `q` per player-hour: log slider from 1e-7 to 1e-3, default 1e-5, displayed as "1 in N" with N = 1/q formatted with separators.
2. QA testers `N_qa` (1 to 200, default 20) and hours each (10 to 1,000, default 200).
3. Beta players (100 to 50,000, default 2,000) and hours each (1 to 100, default 20).
4. Launch players (1,000 to 1,000,000, log slider, default 100,000), hours on day one (0.5 to 12, default 3), hours in first week (1 to 60, default 20).
5. Peak concurrency `C` (100 to 500,000, log slider, default 30,000).

**People tab.**

- **Left view, "One player":** a single dot, coloured as a troublemaker with probability `f`, with the text "f = X%".
- **Right view, "The group":** line chart of P(at least one) `= 1 − (1 − f)^n` against group size `n` from 1 to 200 (linear). Markers at 5, 10, 25, 40, 100 labelled "party", "two parties", "25-player raid", "40-player raid", "town square". A dot grid of `n` players (cap drawing at 200) under the chart, with the expected number of troublemakers `f × n` highlighted (round to nearest whole dot; draw at least one outlined dot if `f × n` is between 0.5 and 1).
- **Controls:** `f` slider 0.1% to 10%, step 0.1%, default 1%; group size `n` slider 1 to 200, default 40; toggle "role-play scene" that relabels the chart to "P(scene broken)" and the title to "Koster's Law."

**Formulas.**

```
H          = N × h
E          = q × H
P_found    = 1 − exp(−E)
wait_peak  = 1 / (C × q)
H_50       = ln(2) / q
P_group    = 1 − (1 − f)^n
```

**Test values.**

Loopholes, `q = 1e-5`, defaults: QA `H = 4,000`, `E = 0.040`, 3.9%. Beta `H = 40,000`, `E = 0.400`, 33.0%. Launch day `H = 300,000`, `E = 3.000`, 95.0%. Launch week `H = 2,000,000`, `E = 20.000`, more than 99.99%. Wait at peak 3.3 hours. `H_50 = 69,315`. Single player, 3 hours: 0.003%.

`q = 1e-6`: QA 0.4%, beta 3.9%, launch day 25.9%, launch week 86.5%.

`q = 1e-4`: QA 33.0%, beta 98.2%, launch day and week more than 99.99%.

People, `f = 1%`: `n = 5` 4.9%; `n = 10` 9.6%; `n = 25` 22.2%; `n = 40` 33.1%; `n = 100` 63.4%. `f = 2%`, `n = 25`: 39.7%. `f = 1.5%`, `n = 20`: 26.1%.

**First screen:** Loopholes tab, defaults. Caption above both views: "One player's chance in 3 hours: 0.003%. The chance someone finds it on launch day: 95%."

**Content rules.** No game art, logos or characters. Players are plain dots; the loophole is an abstract marker. Small text under the views: "All populations are invented. The model assumes players search independently; in practice, a discovered loophole spreads by word of mouth, which makes use after discovery faster still."
