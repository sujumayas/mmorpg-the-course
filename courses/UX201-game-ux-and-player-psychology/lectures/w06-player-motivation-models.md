# UX201 · Week 06 — Player Motivation Models: Bartle, Yee, Quantic Foundry

**Why this matters:** "Our players are achievers" is one of the most common sentences in a game pitch and one of the least tested. Whether it is true depends on how you asked. A questionnaire that forces players to choose between motivations will always find trade-offs, even among people who have none. This week you learn the three models designers use most, what each one measured, and how to tell a finding about players from a finding about the questionnaire.

**You will be able to:**
- Describe Bartle's four player types and their two axes, Yee's three motivation components, and Quantic Foundry's twelve motivations, and say how each was built.
- Compute forced-choice and rating-scale scores for the same player, and show why forced-choice scores always sum to a constant.
- Apply a primary-motivation rule to a profile and explain why many players have no single type.
- Critique a motivation claim in a pitch or report by asking what instrument produced it, and design a short survey that avoids the forced-choice trap.

**Before class:** Richard Bartle, "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs," *Journal of MUD Research* 1(1), 1996 (free at mud.co.uk). Read up to the end of the section on the interest graph. Nick Yee, "Motivations for Play in Online Games," *CyberPsychology & Behavior* 9(6), 772-775 (2006), or the longer online version "Motivations of Play in MMORPGs: Results from a Factor Analytic Approach" (nickyee.com). Browse Quantic Foundry's Gamer Motivation Model page and take the profile survey yourself (about five minutes).

**Prerequisites from earlier courses:** [GD101 week 5, player experience goals and the eight kinds of fun](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md), which introduced Bartle's four types in one paragraph. This week goes further. [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md), for correlation and standard scores. [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), for the sample-size cautions in the lab. [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md), for the MUDs Bartle was describing. From this course, [week 4](w04-self-determination-theory.md). SDT's needs are the "why" underneath every motivation model here.

**Interactive:** [Forced choice vs rating scales](../examples/w06-forced-choice.html). Use it during section 2.

---

## 1. Bartle's four types

Richard Bartle co-wrote MUD1, the first multi-user dungeon (GS101 week 5). His 1996 paper grew out of a long argument among the most experienced players of a commercial MUD in the UK, from November 1989 to May 1990. About 15 people took a major part and perhaps 15 more joined in, debating what people want out of a MUD. When Bartle summarised the debate, he found four clusters of things players enjoyed.

- **Achievers** set themselves goals inside the game, such as treasure, levels and points, and pursue them.
- **Explorers** want to find out as much as they can about the world, first its geography and later how its rules work.
- **Socialisers** use the game as a setting for talking to and getting to know other players.
- **Killers** want to act on other players, usually by beating or distressing them.

He arranged them on two axes. One runs from **acting** (doing things to something) to **interacting** (doing things with something). The other runs from **players** to **world**. Achievers act on the world, explorers interact with it, socialisers interact with players, and killers act on them. The paper even suggests the axes could be scaled, so a player could sit anywhere in the square, not only in a corner.

Two parts of the paper are often forgotten. First, Bartle wrote that most players leaned at least a little to all four, but each tended to have an overall preference. The types were tendencies, not boxes. Second, most of the paper is about **population dynamics**, how the numbers of each type affect the others. More killers drive achievers away, and socialisers even more strongly. More explorers keep killers in check. He described four stable configurations. Killers and achievers can reach an equilibrium. Socialisers can dominate a MUD once killing is prevented. All four types can balance, which is the hardest state to reach. Or the game can end up with no players at all. [MMO301 week 8](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w08-player-types-bartle-1996-and-the-heros-journey.md) studies these dynamics in depth.

Bartle was clear about the paper's limits. In an endnote he says he isn't a trained psychologist and that readers shouldn't expect a conventionally rigorous approach. The four types came from one community's debate, not from measurement. What happened next is a lesson in what goes wrong when someone builds a measurement on top of a model like that.

## 2. Worked example: why every Bartle Test adds up to 200%

### The hook

In 1999 and 2000, Erwin Andreasen and Brandon Downey built an online questionnaire based on Bartle's paper. It became known as the Bartle Test of Gamer Psychology, and for years it was the way many players and designers "found out their type." Its result, the Bartle Quotient, comes from 30 questions. The four percentages always total 200%, and no single one can go above 100%.

That is odd if you think about it for a moment. Two players could get an identical result, say 100% Achiever, 67% Explorer, 33% Socialiser and 0% Killer, and one of them could love games while the other barely likes them. No player can score high on everything, and every point gained in one type must be lost from another. Nick Yee put the objection bluntly in his online report on MMO motivations. He argued that the test's forced-choice design merely perpetuates the assumptions of Bartle's types instead of testing them. This example shows exactly how.

### The model

There are two ways to ask a player about motivation.

A **rating-scale** (or **normative**) item asks about one thing at a time. "How much do you enjoy exploring the world for its own sake?" from 1 to 5. Every motivation gets its own answer, and a player can rate everything high or everything low.

A **forced-choice** (or **ipsative**) item asks the player to pick one of two. "Would you rather explore a new zone or finish a set of achievements?" Every answer is a win for one motivation and a loss for another.

We don't have the Bartle Test's scoring code, and we haven't checked how its questions were actually paired. So what follows is a **teaching model**, not a description of the published test. It is the simplest design that reproduces the published facts (30 questions, a 200% total, a 100% maximum).

- There are four types. Each question pits two of them against each other.
- There are 6 possible pairs. Each pair is asked 5 times, which makes 30 questions. Each type appears in `3 × 5 = 15` questions.
- A type's score is the share of its 15 questions in which the player chose it:

```
score_T = (times T was chosen) / 15 × 100%
```

Every question gives exactly one win, so the wins total 30, and the scores total `30 / 15 × 100% = 200%`. A type chosen every time scores `15 / 15 = 100%`, the maximum. The constant sum comes from the arithmetic of the questionnaire, not from anything about the people answering it.

To see what the player's real interests do to the score, give each player an underlying interest `u_T` from 0 to 10 in each type, which is what a rating scale would measure. On a forced-choice question between `T` and `U`, the player picks whichever they like more. On a tie they pick either with equal chance.

### Numbers you can check

Five invented players. Rating scores on the left, the forced-choice result on the right. Types are in the order Achiever, Explorer, Socialiser, Killer.

| Player | Interests `u` (A, E, S, K) | Mean interest | Forced-choice (A, E, S, K) | Sum |
|---|---|---|---|---|
| Rhea | 9, 8, 7, 2 | 6.5 | 100, 67, 33, 0 | 200 |
| Sol | 3, 2, 1, 0.5 | 1.6 | 100, 67, 33, 0 | 200 |
| Tam | 6, 6, 6, 6 | 6.0 | 50, 50, 50, 50 | 200 |
| Uma | 9, 1, 8.9, 1 | 5.0 | 100, 17, 67, 17 | 200 |
| Vik | 2, 9, 2.5, 3 | 4.1 | 0, 100, 33, 67 | 200 |

Check Rhea by hand. Achiever beats all three others, so it wins 3 pairs × 5 questions = 15 out of 15, which is 100%. Explorer beats Socialiser and Killer, 10 out of 15, which is 67%. Socialiser beats only Killer, 5 out of 15, which is 33%. Killer wins nothing, so 0%. For Uma, Explorer and Killer tie, so each takes half of their 5 shared questions. Explorer's score is `2.5 / 15 = 17%`.

Four things stand out.

1. **Rhea and Sol are indistinguishable.** Rhea is enthusiastic about three kinds of play. Sol is lukewarm about everything. A forced-choice instrument sees only the order of a player's interests, never their level.
2. **Uma is a strong socialiser labelled a weak one.** Her socialising interest (8.9) is almost equal to her achieving interest (9). The forced-choice score reports 100 against 67, a large gap made from a 0.1 difference.
3. **Vik's killer score of 67% comes from an interest of 3 out of 10.** He likes killing more than achieving or socialising, and that is all the score can say.
4. **The instrument invents a trade-off.** In any group of players whose interests are unrelated, forced-choice scores for any two types come out negatively correlated. With four types and a fixed total, the average correlation between two types is exactly `−1/3`. In one simulated population of 2,000 players with independent random interests, the rating-scale correlation between Achiever and Socialiser was 0.01 and the forced-choice correlation was −0.35. Those two values are specific to that sample. Rerun it with other random players and the rating-scale value stays near 0 while the forced-choice value lands between about −0.31 and −0.36, around the theoretical −1/3. "Achievers aren't socialisers" is built into the questionnaire.

### A second trap: one type per person

Suppose you avoid forced choice and measure interests on rating scales. You still have to decide whether to give each player a type. Yee's rule, from his own data, assigns a primary motivation only when the top score is clearly ahead. Formally, when `top × 0.75 > second`.

- Rhea: `9 × 0.75 = 6.75`, which is less than 8. **No primary motivation.** The forced-choice test called her 100% Achiever.
- Sol: `3 × 0.75 = 2.25`, which is more than 2. **Primary: Achiever.** The lukewarm player gets the clean label.
- Uma: `9 × 0.75 = 6.75 < 8.9`. **No primary.**
- Vik: `9 × 0.75 = 6.75 > 3`. **Primary: Explorer.**

In Yee's real data, applied to three components, 43% of respondents had no primary motivation. Of those who did, 20% were primarily Achievement, 20% Immersion and 17% Social. Nearly half the players didn't fit a single box, even with a rule Yee himself called lax.

### A visual you can move

Open `examples/w06-forced-choice.html`. On the left are one player's four interest sliders and their rating-scale bars. On the right are the same player's forced-choice bars, with the sum printed underneath. Start with Rhea. Now drag all four sliders down together, towards Sol. The left bars fall and the right bars don't move at all. Then drag Uma's socialising slider from 8.9 past 9. The right chart swaps her Achiever and Socialiser bars from 100 and 67 to 67 and 100, a jump of 33 points each, while the left chart barely changes.

The second tab simulates a population with independent interests and draws two scatter plots of Achiever against Socialiser. The rating-scale plot is a round cloud. The forced-choice plot is a set of diagonal stripes sloping down. Same players, two instruments, opposite conclusions.

### Cross-game recognition

**Ultima IV: Quest of the Avatar (1985).** Before play begins, a fortune-teller poses a series of ethical dilemmas built around the game's eight virtues. The player must, in effect, rank the virtues, and whichever comes out on top sets the character's class. Choose Compassion and you are a bard, Honor and you are a paladin. That is a forced-choice instrument used on purpose. The designer wants one class out, so a ranking is exactly the right tool. The same method is wrong when you want to know how much a player cares about each thing.

**Quantic Foundry's Gamer Motivation Profile (2015 onward).** Yee's company built a rating-scale survey covering twelve motivations. They report each player's scores as standardised scores against the whole sample of respondents, not as shares of a fixed total. A player can be high on many motivations or low on all of them. When they list games popular with a motivation, they take the players in the top 20% on that motivation and don't require them to be low on anything else. That is the normative method, and it removes both traps.

**Yee's MMO survey (2005-2006).** About 3,200 players rated 39 items one at a time. When the answers were analysed, the Achievement and Social components were mildly *positively* correlated, `r = .10`, which is the opposite of the trade-off Bartle's axes imply. Achievement and Competition, which Bartle placed in different quadrants, correlated at `r = .41`. Bartle's Explorer split into two unrelated interests, Discovery (finding things in the world) and Mechanics (understanding the rules). The data didn't support the corners of the square.

Three instruments, one principle. What you can learn about players depends on whether each answer is allowed to vary on its own.

### Eyes-open design judgment

- **Use forced choice when you need a ranking.** If a team must decide which of two features to cut, asking players to choose between them is honest. The result is a ranking. Don't report it as a level of interest.
- **Report profiles, not types.** A profile of four numbers per player loses nothing. A type throws away everything except the largest number. For audience decisions, report the share of players high on each motivation, for example "top 20% on Discovery." Those shares can overlap and needn't sum to 100%.
- **Bartle's model is still useful.** Its population dynamics are a good way to think about how one group's play affects another's, for example what open player-killing does to a social population. Use it as a design lens for interactions. Don't use it as a measurement.
- **Every instrument has a shape.** Rating scales have their own biases. Some people use the top of any scale and some the middle, and older respondents in Quantic Foundry's data rate every motivation lower (section 4). Standardising scores within the sample handles some of that. None of it goes away by avoiding surveys.

### Check yourself (worked example)

1. A player's interests are A 7, E 7, S 2, K 5. Compute the forced-choice scores and check that they sum to 200%. Does the player have a primary motivation under Yee's rule?
2. A student designs a 24-question forced-choice test with four types, where every pair is asked 4 times. What is each type's maximum number of wins, what do all the scores sum to, and what is the maximum score?
3. A studio's survey of its community finds "only 8% of our players are Socialisers." The survey was forced-choice with four types. Give two reasons the true share of players who care a lot about socialising could be much higher.

<details>
<summary>Answers</summary>

1. A and E tie. Each beats S and K (10 wins) and takes half of their 5 shared questions (2.5), so each has 12.5 out of 15, 83.3%. K beats S, 5 out of 15, 33.3%. S has 0. The sum is `83.3 + 83.3 + 33.3 + 0 = 200%`. Primary rule: `7 × 0.75 = 5.25`, less than 7, so no primary.
2. Each type appears in `3 × 4 = 12` questions, so it has at most 12 wins. The 24 questions give 24 wins, so the scores sum to `24 / 12 = 200%`, and the maximum is 100%. Any balanced pairwise design with four types sums to 200%.
3. A player who loves socialising but loves something else slightly more scores low on Socialiser, because forced choice only counts ranks. And if the survey gave each player a single type, every player with no clear primary was forced into one box, and a close second place counts for nothing. A rating-scale item on socialising would show the level directly.

</details>

## 3. Yee's components

Yee's aim was to test Bartle's model with measurement. He wrote survey items from Bartle's types and from players' open-ended answers, collected ratings, and used **factor analysis**. That is a statistical method that groups items whose answers go up and down together. Items in one group measure one underlying motivation. Items in different groups measure different ones. The result, from about 3,200 respondents to 39 items, was 10 subcomponents that fell into 3 main components.

| Component | Subcomponents | Example of what a high scorer enjoys |
|---|---|---|
| Achievement | Advancement, Mechanics, Competition | Levelling fast, optimising a build, beating other players |
| Social | Socializing, Relationship, Teamwork | Chatting, forming close friendships, group goals |
| Immersion | Discovery, Role-Playing, Customization, Escapism | Exploring, inventing a character's story, styling a character, getting away from real life |

Yee stressed that these are components, not types. Each player has a score on all ten, and the three main components are largely unrelated to each other (correlations around `.10`).

Two further findings matter for designers.

- **Gender differences were real but modest.** Men scored higher on Achievement and women on the Relationship and Customization subcomponents. The effect sizes were small to moderate, and age correlated with several subcomponents about as strongly as gender did. Achievement and Competition declined with age.
- **Escapism was the best predictor of problematic use.** In a model that included gender, age, hours played and all ten subcomponents, Escapism predicted problematic usage more strongly than anything else (standardised coefficient `.31`). Hours played alone didn't capture it. Players using the game to avoid real-life problems are a different risk group from players who simply play a lot. That links directly to last week's ethics checklist.

Ryan, Rigby and Przybylski (2006, study 4) compared Yee's components with the SDT needs from week 4 in the same MMO sample. The two models are answers to different questions. Yee's components describe what players seek in a game. SDT's needs describe why those activities satisfy them. A player high on Teamwork seeks group play, and group play satisfies relatedness and competence.

## 4. Quantic Foundry's twelve motivations

Yee later co-founded Quantic Foundry, a market research company, which built a new model for all genres, not only MMOs. Their five-minute Gamer Motivation Profile had been taken by over 140,000 gamers by 2016, and its factor analysis produced twelve motivations in six pairs.

| Group | Motivations |
|---|---|
| Action | Destruction (blowing things up), Excitement (fast-paced, intense) |
| Social | Competition (duels, matches, leaderboards), Community (teaming up, social interaction) |
| Mastery | Challenge (practice, hard content), Strategy (thinking and planning) |
| Achievement | Completion (collect and finish everything), Power (progress, becoming powerful) |
| Immersion | Fantasy (being someone or somewhere else), Story (plot and characters) |
| Creativity | Design (expression, customisation), Discovery (experiment, explore, tinker) |

Their analysis also found that the motivations fall into three larger clusters, and that the same high-level structure appeared across the geographic regions they had data for.

Two published findings show why the normative method pays off.

**Age matters more than gender.** Competition has the largest gender difference among the twelve motivations, an effect size of `d = .33`. That means about 87% of the men's and women's distributions overlap. Competition's correlation with age is `r = −.28`, and Quantic Foundry reports that age explains about three times as much of the variation in Competition as gender does. Excitement falls just as fast with age (`r = −.28`). Strategy barely changes (`r = −.05`), which makes it the most stable motivation across ages. A forced-choice test couldn't show any of this. If every motivation falls with age, every rank can stay the same.

**Scores are relative to the respondents.** A 90th-percentile Discovery score means higher than 90% of the people who took the survey. People who take an online motivation survey are not a random sample of players, so a studio should compare its own players against the benchmark and read differences, not absolute levels.

### Using a motivation model in a real project

- **Audience fit.** Survey your beta players with a short rating-scale instrument. Compare their profile with the benchmark for games in your genre. A strategy game whose testers are high on Excitement and low on Strategy has a marketing problem or a design problem.
- **Feature mapping.** List the major features and mark which motivations each serves. A feature that serves no motivation your audience holds is a candidate to cut.
- **Segments, not types.** Build segments from people who are high on a motivation, and let them overlap. "38% are top-quartile on Completion" is actionable. "Our players are Completionists" is not.
- **Pair with behaviour.** Self-report tells you what players say they enjoy. Telemetry and playtests (week 3) tell you what they do. When the two disagree, investigate.

## In-class activity (25 minutes)

Groups of four.

1. **Write items (10 min).** Write four rating-scale items (1 to 5) and six forced-choice items, one for each pair of Bartle's types. Write your own wording, don't copy any published test.
2. **Answer (5 min).** Everyone in the group answers both sets.
3. **Score (10 min).** For each person, compute the mean rating per type and the forced-choice percentage per type (each type appears in 3 questions, so a score is wins ÷ 3). Check that each person's forced-choice scores sum to 200%. Find the group member whose two profiles disagree most, and explain why.

Expected output: the item lists, a score table for all four members in both formats, and one paragraph on the biggest disagreement.

## Common misconceptions

- **"Bartle's paper says every player is one type."** It says most players lean a little towards all four, with an overall preference. The single-type reading came later, from the test and from casual use.
- **"If the test says 0% Killer, the player dislikes competition."** It says only that the player ranked it last. Their interest could still be high.
- **"Achievers and socialisers are opposites."** In Yee's rating data they were mildly positively related. The opposition comes from the forced-choice design.
- **"Male players are competitive, female players are social."** The differences exist but are modest. Competition shows 87% overlap between genders, and age explains more of it.

## Check yourself

1. Place each on Bartle's axes and name the type: (a) a player who maps every cave in a zone; (b) a player who ambushes others at a quest giver; (c) a player who runs a weekly role-play tavern night; (d) a player who completes every achievement in the log.
2. Which of Yee's subcomponents does Bartle's Explorer split into, and why does it matter for a designer adding a "hidden lore" system?
3. A pitch deck says, "80% of our survey respondents are Achievers, so we will prioritise progression." List three questions you would ask about the survey before accepting that.
4. Using Quantic Foundry's age correlations, predict how the Competition and Strategy scores of a game's audience would change if its average player age rose by ten years. Which prediction is safer, and why?

<details>
<summary>Answers</summary>

1. (a) Interacting with the world, Explorer. (b) Acting on players, Killer. (c) Interacting with players, Socialiser. (d) Acting on the world, Achiever.
2. Discovery (finding things in the world) and Mechanics (understanding the rules). They are unrelated, so a hidden lore system serves Discovery players and does little for Mechanics players, who want systems to analyse. Don't assume one "Explorer" audience will want both.
3. Was it forced-choice? If so, the 80% is a ranking, not a level. Was each respondent given one type, and how many had no clear primary? Who responded (existing fans, a social media sample), and how does that compare with the audience you want?
4. Competition should fall noticeably (`r = −.28`). Strategy should barely change (`r = −.05`). The Strategy prediction is safer, because a near-zero correlation predicts little change and the age data are cross-sectional. The Competition drop could partly be a generational difference rather than an effect of ageing, and Quantic Foundry notes that risk.

</details>

## Lab hook

[Lab 06, two instruments, one audience](../labs/lab06.md). You run a short motivation survey on 12 or more classmates or players in two formats, a forced-choice set and a rating-scale set, using the item bank in the starter materials. The starter script scores both formats, applies the primary-motivation rule and prints the correlations between types in each format. You compare the two pictures of the same people and write a recommendation for a fictional studio. Deliverable: the data, the script output and a two-page report.

## Sources

- Bartle, R. (1996). "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs." *Journal of MUD Research* 1(1). mud.co.uk/richard/hcds.htm (accessed September 2026). The November 1989 to May 1990 debate among about 15 major and 15 occasional contributors; the four types and two axes; the remark that most players lean a little to all four; the population dynamics and the four stable configurations; the endnote that the author is not a trained psychologist.
- Wikipedia, "Bartle taxonomy of player types" (accessed September 2026). The Bartle Test by Erwin Andreasen and Brandon Downey (1999-2000); 30 questions; the Bartle Quotient totals 200% with no category above 100% (citing Mulligan & Patrovsky, *Developing Online Games*, 2003, appendix C). Williams, Yee & Caplan (2008) on the missing Explorer factor.
- Yee, N. "Motivations of Play in MMORPGs: Results from a Factor Analytic Approach" (online report, nickyee.com/daedalus/motivations.pdf, about 2005). 3,200 respondents, 39 items, 10 subcomponents, 3 components with correlations around .10; Achievement and Socializing r = .10; Advancement and Competition r = .41; Discovery and Mechanics separate; the forced-choice critique of the Bartle Test; the primary-motivation rule (primary × .75 > secondary), 43% without a primary, 20% Achievement, 20% Immersion, 17% Social; gender and age table; Escapism as the best predictor of problematic usage (β = .31). Published in short form as Yee, N. (2006), *CyberPsychology & Behavior* 9(6), 772-775.
- Quantic Foundry, "Gamer Motivation Model" (archived 2024 copy, accessed September 2026). Factor analysis on over 140,000 gamers; three clusters, consistent across regions.
- Quantic Foundry blog, "Most Popular Games by Gaming Motivations" (Yee, August 2015, archived copy). The twelve motivations in six groups with their short descriptions; top 20th percentile method.
- Quantic Foundry blog, "Gender Differences in Gaming Motivations Align with Stereotypes, But Small Compared to Age Differences" (Yee, August 2015, archived copy). Competition gender d = .33, 87% overlap; age correlations for all twelve motivations (Competition −.28, Excitement −.28, Strategy −.05); z-scores.
- Quantic Foundry blog post on gamer age, quanticfoundry.com/2016/02/10/gamer-generation/ (Yee, February 2016, archived copy). Competition changes most with age; Strategy is the most age-stable; caution about cross-sectional age data.
- Wikipedia, "Ultima IV: Quest of the Avatar" (accessed September 2026). Character creation by ethical dilemmas posed by a fortune-teller; the player's top virtue sets the class (Compassion to bard, Honor to paladin).
- Ryan, R. M., Rigby, C. S. & Przybylski, A. (2006). *Motivation and Emotion*, 30, 347-363. Study 4 compares SDT measures with Yee's components.
- The pairwise reconstruction of the Bartle Test's scoring, the five players, the tie rule and the simulated population are this course's own teaching models. The published test's exact question design was not checked.

## Interactive spec: examples/w06-forced-choice.html

**Purpose.** Show that forced-choice scores depend only on the order of a player's interests, always sum to 200%, and create negative correlations between types that rating scales don't show.

**The one insight the visual must make obvious.** Moving all four interest sliders up or down together changes the rating-scale bars and leaves the forced-choice bars exactly where they are, with "Sum = 200%" printed under them the whole time.

**Layout.** Two tabs. "One player" (default) and "A population."

- One player: at 1280px, sliders on the left, two bar charts side by side on the right ("Rating scale, 0 to 10" and "Forced choice, % of questions won"). At 390px, sliders first, then the two charts stacked. Under the forced-choice chart, the sum in large type. Under both, a line with Yee's rule result ("Primary: Achiever" or "No primary motivation").
- A population: two scatter plots side by side (stacked on mobile), Achiever score (x) against Socialiser score (y), rating scale on the left and forced choice on the right, each with its Pearson `r` printed in the corner. A dropdown chooses which pair of types to plot.

**Controls (One player).**

- Four sliders for `u_A`, `u_E`, `u_S`, `u_K`, 0 to 10, step 0.1.
- A "move all" slider that adds the same amount (−10 to +10) to all four, clamped to 0 to 10, so students can shift the level without changing the order.
- Response noise `s`: 0 to 3, step 0.1, default 0. At 0, the higher interest always wins and ties split evenly. Above 0, `P(T over U) = 1 / (1 + exp(−(u_T − u_U) / s))`.
- Questions per pair: 1 to 10, default 5 (shows total questions = 6 × value).
- Primary rule factor: 0.5 to 1.0, default 0.75.
- Presets: Rhea, Sol, Tam, Uma, Vik (values from the lecture table), and "Check yourself 1" (7, 7, 2, 5).

**Controls (A population).** Population size 100 to 5,000 (default 2,000). Interest distribution: independent uniform 0 to 10 (default), or "correlated A and S" with a correlation slider from −0.8 to +0.8 (generate with a shared normal component, then clamp). Seed (default 1) and reroll. Noise `s` shared with the first tab.

**Formulas.**

- Expected wins for type `T` = `q × Σ_{U ≠ T} P(T over U)`, where `q` is questions per pair. Score = wins / (3q) × 100%.
- Sum of scores = 200% always (display computed value to one decimal to prove it).
- Primary: sort interests; primary is the top type if `top × factor > second`, else "none".
- Pearson `r` computed on the displayed points.

**Test values** (`q = 5`, `s = 0`, factor 0.75).

- Rhea (9, 8, 7, 2): FC 100.0, 66.7, 33.3, 0.0; primary none.
- Sol (3, 2, 1, 0.5): FC 100.0, 66.7, 33.3, 0.0; primary Achiever.
- Tam (6, 6, 6, 6): FC 50, 50, 50, 50; primary none.
- Uma (9, 1, 8.9, 1): FC 100.0, 16.7, 66.7, 16.7; primary none. Raising S to 9.1 gives 66.7, 16.7, 100.0, 16.7.
- Vik (2, 9, 2.5, 3): FC 0.0, 100.0, 33.3, 66.7; primary Explorer.
- Check yourself 1 (7, 7, 2, 5): FC 83.3, 83.3, 0.0, 33.3; primary none.
- With `s = 1`: Rhea 87.0, 66.6, 46.0, 0.3; Sol 84.5, 60.6, 33.7, 21.2; Uma 84.1, 16.7, 82.5, 16.7.
- `q = 4`: every sum still 200%; each type appears in 12 questions.
- Population, independent uniform, 2,000 players, `s = 0`: rating-scale `r` near 0 (within ±0.05); forced-choice `r` near −0.33 (within about ±0.04 depending on seed; theory −1/3).

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Bars carry numeric labels. The two formats differ by fill pattern as well as colour. Sliders keyboard operable with visible values. Scatter points use shape and partial transparency so overlapping stripes stay readable. No game art, logos or the published test's questions; types are labelled with Bartle's names in text only.
