# MMO301 · Week 09 — Motivation research beyond Bartle (Yee)

**Why this matters:** Studios still write design documents that say "this feature is for achievers". Last week you saw that Bartle's types were a thoughtful summary, never a measurement. This week you meet the research that measured them. It found that most players do not have one dominant motivation at all. If you design for four kinds of people, you design for a population that does not exist.

**You will be able to:**
- Explain in plain terms how a factor analysis turns survey answers into motivation components, and state Yee's three components and ten subcomponents.
- Compute the share of players that a "primary motivation" rule can label, as a function of the number of components and the strictness of the rule.
- Compare type models and component models, and name what each hides.
- Critique a motivation study by its sample, its measures and its era, and turn its findings into design questions rather than personas.

**Before class:** Yee, "Motivations of Play in MMORPGs: Results from a Factor Analytic Approach" (the Daedalus Project white paper, free at nickyee.com, all ten pages). Yee (2006), "Motivations for Play in Online Games", *CyberPsychology & Behavior* 9(6), 772-775 (the short peer-reviewed version). Reread the "Player interactions" section of Bartle (1996) from last week.

**Prerequisites from earlier courses:** From this course, [week 8, Bartle's player types](w08-player-types-bartle-1996-and-the-heros-journey.md). [GD101 week 5, the 8 kinds of fun](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md) (a game offers several kinds of fun at once). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), [week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md), [week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) and [week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md).

**Interactive:** [examples/w09-primary-motivation.html](../examples/w09-primary-motivation.html). Keep it open during section 2.

---

## 1. From types to components

### The problem with brainstormed types

Bartle's four types came from a discussion among experienced players. That is a good way to generate ideas and a poor way to test them. Nick Yee, then a researcher running an online survey project on MMO players called the Daedalus Project, named three problems with using the types as a model.

1. **The pieces of a type may not belong together.** Bartle's socialiser both chats and role-plays. Nobody checked whether players who like chatting also like role-playing.
2. **The types may overlap.** A member of a serious raiding guild works toward loot (achiever) and depends on a tight group (socialiser). Bartle's graph puts those two types in opposite corners.
3. **There was no way to measure the types.** And the popular online "Bartle Test", written by other people years later, forces respondents to choose between types in each question. A test built that way will always produce types, whether or not they exist.

His fix was to stop assuming the groups and let the data form them.

### What a factor analysis does

Yee's method has three steps. You do not need the matrix algebra to follow it.

1. **Collect many specific reasons to play.** Yee drew candidate motivations from the literature, including Bartle, and from open-ended answers in earlier surveys. He turned each into a survey item, such as how important it is to level up fast, rated on a five-point importance scale.
2. **Ask many players.** In the white paper's data set, 3,200 respondents answered 39 items.
3. **Find the items that move together.** If players who rate item 4 high also tend to rate items 9 and 17 high, and players who rate it low rate those low too, the three items are probably measuring one underlying thing. A factor analysis finds these groups mathematically. It makes items within a group as correlated as possible and the groups as uncorrelated as possible. The researcher then names each group.

The output is a set of **components**. A component is a dimension, not a box. Every respondent gets a score on every component.

### What Yee found

The 39 items formed 10 **subcomponents**, which together explained 60% of the variation in answers. A second analysis on the 10 subcomponent scores grouped them into 3 **main components**, explaining 54% of the variation.

| Main component | Subcomponents |
|---|---|
| Achievement | Advancement (progress, power, status), Mechanics (numbers, optimization, analysis), Competition (challenging, provoking and dominating others) |
| Social | Socializing (chat, helping, making friends), Relationship (personal, supportive, lasting), Teamwork (grouping, group achievement) |
| Immersion | Discovery (exploring, lore, hidden things), Role-playing (story, character history), Customization (appearance, style), Escapism (relaxing, escaping real-life problems) |

Two results matter more than the table.

**The three main components are nearly independent.** Yee reports correlations among them of about 0.10. A correlation of 0 means knowing one score tells you nothing about the other. A correlation of 0.10 means it tells you almost nothing.

**Achievement and social are slightly positively related.** Bartle's graph puts achievers and socialisers on opposite sides, which predicts that the more of one you are, the less of the other. Yee found the opposite sign. Achievement and the socializing subcomponent correlated at about +0.10. Yee's image is that liking ice cream does not mean you hate pasta.

## 2. Worked example: how many players have a type?

### The hook

Yee tried to give his model a familiar face. He assigned each respondent a **primary motivation** only when their top component score clearly beat their second. His rule was that the top score multiplied by 0.75 had to exceed the second score. He called the rule "somewhat lax". In other words, the second score only had to be less than 75% of the top one.

Even with that lax rule, 43% of players had no primary motivation. Of the rest, about 20% of all players were achievement-primary, 20% immersion-primary and 17% social-primary.

Stop and compare that with how types are used in practice. A designer who writes a persona for "the achiever" is writing for about one player in five. The largest single group, 43%, is the players with no dominant motivation. They appear in no persona at all.

Is 43% a strange property of MMO players, or would any rule like this leave a big share unlabelled? You can answer that with a model.

### One model, stated once

Give each player a score on each of `k` components, expressed as a percentile from 0 to 1. A score of 0.8 means the player is higher than 80% of players on that component. Assume, for now, that the components are independent, so each score is an independent uniform number between 0 and 1.

Apply Yee's rule with a strictness `c` between 0 and 1. A player has a primary motivation when

```
second-highest score < c × highest score
```

Yee's rule is `c = 0.75`. A stricter rule has a smaller `c`.

Then the share of players who get a primary motivation is

```
P(typed) = c^(k − 1)
```

Why this works. Pick any player and call their highest score `m`. The other `k − 1` scores are below `m`, and, because each score is uniform and independent, each of them is equally likely to be anywhere between 0 and `m`. The player is typed only if every one of them is below `c × m`. For each score the chance is `c`. For all `k − 1` independent scores it is `c` multiplied `k − 1` times. The value of `m` drops out, so the answer is the same for every player.

- `k` is the number of components (or types).
- `c` is the strictness of the rule, the largest allowed ratio of second score to top score.
- `P(typed)` is the fraction of players who receive a single label.

### Numbers you can check

Compute `c^(k − 1)` by hand.

| Components `k` | `c = 0.75` (Yee's rule) | `c = 0.9` (very lax) |
|---|---|---|
| 2 | 75.0% | 90.0% |
| 3 | 56.3% | 81.0% |
| 4 (Bartle's types) | 42.2% | 72.9% |
| 8 (Bartle's eight types) | 13.3% | 47.8% |
| 10 (Yee's subcomponents) | 7.5% | 38.7% |

With three independent components and Yee's rule, the model predicts that 0.75² = 56.25% of players get a primary motivation and 43.75% do not (the table rounds to 56.3%). Yee observed 57% and 43%. That match is partly luck. Yee's scores were not percentiles, and his components were slightly correlated. But the order of magnitude is not luck. **Any single-label rule leaves a large share of players unlabelled once there is more than one independent dimension.** With Bartle's four types it labels fewer than half. With Bartle's eight types, about one player in seven. The more carefully you describe motivations, the fewer players fit one box.

Now look at six individual players, with component percentiles in the order achievement, social, immersion.

| Player | Achievement | Social | Immersion | Top | Second ÷ top | Primary (c = 0.75) | Forced label (highest score) |
|---|---|---|---|---|---|---|---|
| P1 | 0.90 | 0.40 | 0.30 | Ach | 0.44 | Achievement | Achievement |
| P2 | 0.85 | 0.80 | 0.20 | Ach | 0.94 | none | Achievement |
| P3 | 0.30 | 0.35 | 0.33 | Soc | 0.94 | none | Social |
| P4 | 0.20 | 0.90 | 0.60 | Soc | 0.67 | Social | Social |
| P5 | 0.70 | 0.10 | 0.95 | Imm | 0.74 | Immersion | Immersion |
| P6 | 0.72 | 0.10 | 0.95 | Imm | 0.76 | none | Immersion |

Three things show up in six rows.

- **P2 is the raider.** High on both achievement and social. A forced label calls them an achiever and throws away the fact that they are the second most social person in the table.
- **P3 is low on everything.** A forced label calls them a socialiser because 0.35 beats 0.33. They are below average on all three. Many real players look like this, and a type model has no place for them.
- **P5 and P6 differ by 0.02 in achievement.** One gets a label and one does not. Labels near the boundary are fragile, and small changes in a survey answer move players across it.

### A visual you can move

Open the interactive. The left panel is a triangle (a ternary plot) showing 2,000 simulated players by their three component scores, coloured by label (achievement, social, immersion or none). The unlabelled players fill a broad band through the middle and along every edge between two corners. The labelled players sit only in the three corners. The right panel shows the same population as a single bar, split by label, beside the formula value.

Drag `c` from 0.75 toward 0.5. The corners shrink and the grey band grows. Switch `k` from 3 to 4 to 8 and watch the labelled share fall along the table above. Then raise the correlation between components. The simulated share moves a little, but much less than it moves with `k`. Finally, switch the right panel to "forced label". Every player now has a type, and the bar looks tidy. Toggle back and forth. That is the difference between measuring types and manufacturing them.

### Cross-context recognition

**The Bartle Test.** The online test that most people know was written in 1999 and 2000 by Erwin Andreasen and Brandon Downey. It asks about 30 questions, each a forced choice between two options tied to different types, and reports a "Bartle Quotient" whose four percentages add to 200%. Forced choice means a gain on one type is always a loss on another. In model terms it sets the correlation between types to be negative by construction, and it always hands out a top type. It cannot discover that 43% of players have none.

**Bartle's own eight types.** Adding the implicit/explicit axis (week 8) doubles `k` from 4 to 8. With Yee's rule, the share of players who fit one type falls from 42.2% to 13.3%. Bartle's extra axis makes the model describe people better and makes it much worse at labelling them. That is the trade every type model faces.

**Personality testing outside games.** The Myers-Briggs Type Indicator sorts people into 16 types by placing them on one side of four scales. That only makes sense if most people score near the ends of each scale. Studies of its scores, including item-response analyses by Bess and Harvey (2002), found that scores cluster in the middle, like a bell curve. Most people are near the boundary, so a small change in answers flips the type. Dimension-based personality models avoid the problem by reporting a score on each scale instead of a type. It is the same argument Yee made, in a different field.

### Eyes-open design judgment

- **Design for profiles, not people-types.** A feature has a profile too. A guild raid serves achievement and teamwork at once. A housing system serves customization and socializing. Score features on components and ask whether each component has enough features serving it. Do not ask "which type is this for?"
- **Remember the unlabelled majority.** If "high" means the top 30% on a component and the three components are independent, the complement rule gives `1 − 0.7³ = 65.7%` of players high on at least one, and `0.7³ = 34.3%` high on none. A third of your players are moderate on everything. They still pay and still play. They need a game that is pleasant at moderate intensity on all three.
- **Types still have a use.** A four-type label is quick to say in a meeting and easy to remember. Use it as shorthand for a direction on the graph, never as a headcount.
- **Watch the boundary.** If you segment players by a primary label (for a live event, a marketing email, a tutorial path), players near the boundary will be mis-sorted. Prefer rules that use the scores directly, such as "social score above 0.7", which can put one player in several segments.

### Check yourself (worked example)

1. A game's research team uses four components and a rule with `c = 0.6`. What share of players does the model predict will get a primary motivation?
2. A player scores achievement 0.64, social 0.50, immersion 0.20. Under Yee's rule, do they have a primary motivation? Under `c = 0.8`?
3. With three independent components, "high" defined as the top 20%, what share of players is high on exactly one component? On two or more?

<details>
<summary>Answers</summary>

1. `0.6³ = 0.216`, about 21.6%.
2. Second ÷ top `= 0.50 / 0.64 = 0.78`. Under `c = 0.75`, 0.78 is not below 0.75, so no primary motivation. Under `c = 0.8`, 0.78 is below 0.8, so yes, achievement.
3. Exactly one: `3 × 0.2 × 0.8² = 0.384`, 38.4%. None: `0.8³ = 0.512`. Two or more: `1 − 0.512 − 0.384 = 0.104`, 10.4%.

</details>

## 3. Where the data disagreed with Bartle

Beyond the overall finding, Yee's white paper lists four specific places where the measured structure differed from Bartle's model.

**Socializing and role-playing are separate.** Bartle placed both in the socialiser. In the data, chatting and making friends formed one subcomponent under Social, while role-playing landed under Immersion with story and character history.

**Achievement and killing go together.** Bartle's achievers and killers are separate types in different quadrants. Yee's Competition subcomponent (challenging, provoking and dominating other players) grouped with Advancement under Achievement, and the two subcomponents correlated at about 0.41, a moderate relationship. Players who want power in the game's terms also tend to want power over other players.

**The explorer splits in two.** Bartle's explorer maps the world and also tinkers with its mechanics. Yee reports that his early attempts to find a single explorer factor failed until he looked for the two separately. Discovery (places, lore, hidden things) sits under Immersion. Mechanics (numbers, optimization, theorycrafting) sits under Achievement. The player who reads MMO303's armor formulas for fun need not be the player who climbs a mountain to see the view.

**Immersion is new.** Story, customization and escapism did not appear in Bartle's four types at all. They formed their own component, independent of socializing.

A caution on words. Yee's "Immersion" component means discovery, role-play, customization and escapism. Bartle's "immersion", which [week 10](w10-immersion-identity-and-the-avatar.md) covers, is a ladder describing how a player relates to their character. Same word, two different ideas.

### Who plays for what

Yee also compared groups. Treat these results as descriptions of his respondents, not of all players.

- **Gender.** Male respondents scored higher on Achievement, with an effect size of r ≈ 0.26 (squared, about 7% of the variation in the score). Female respondents scored higher on Relationship (about 0.25) and Customization (about 0.18). The primary-motivation shares differed sharply. About 22.6% of male respondents were achievement-primary against 4.2% of female respondents. About 30.9% of female respondents were immersion-primary against 18.3% of male respondents.
- **Age.** Younger players scored higher on Achievement. Among male respondents the correlation between age and Achievement was about −0.35.
- **Time played.** Achievement had the strongest link to hours played per week, about 0.22 for male respondents and 0.12 for female respondents.

The gender differences sit on top of large overlap. An effect size of 0.26 means most of the variation in achievement scores has nothing to do with gender. A studio that designs "for women" or "for men" from these numbers will be wrong about most individual players of both.

## 4. Reading motivation research critically

Yee's work replaced a brainstorm with evidence. It is still evidence of a particular kind, and you should read it the way MA102 taught you to read any study.

**Who answered.** The respondents were players who found Yee's online survey and chose to answer it, in the mid-2000s. That is a self-selected sample. 2,769 of the roughly 3,200 were male. Players who read research surveys about their hobby are not a random draw from all players. The quotes in the white paper come from players of EverQuest, Dark Age of Camelot, Star Wars Galaxies and EVE Online. A 2026 mobile MMO audience may differ.

**What was measured.** The items are self-reports. They measure what players say motivates them, not what they do. A player may rate "helping other players" as very important and never do it. Combine survey data with behavioural data (week 12 and MMO308 cover telemetry) before you make decisions.

**What the method can and cannot do.** Factor analysis finds structure in the items you wrote. If no item asked about, say, collecting for its own sake, no collecting factor can appear. Yee answered Bartle's version of this objection by saying the method tests groupings rather than assuming them, which is true. It is still limited to the questions asked.

**The labels are chosen.** The analysis produces groups of items. People name them. "Immersion" is Yee's name for a group that includes escapism. Another researcher could have named it differently and changed how designers talk about it.

**Where the work went next.** Yee later co-founded Quantic Foundry (2015) with Nicolas Ducheneaut, which runs a much larger gamer motivation survey across many genres. It keeps the component approach. This course does not rely on its specific numbers, but you should know it exists when a studio cites "motivation data".

## In-class activity (25 minutes)

The whole class takes a nine-item survey written for this course, not taken from Yee. Rate each from 1 (strongly disagree) to 5 (strongly agree), thinking about the online game you play most.

- **Achievement.** (a1) I compare my character's numbers with other players'. (a2) I plan my progress several sessions ahead. (a3) Beating other players matters to me.
- **Social.** (s1) I log in partly to see particular people. (s2) I would rather do a hard task in a group than alone. (s3) I have talked with people from a game about life outside it.
- **Immersion.** (i1) I go somewhere in a game world just because I have not seen it. (i2) I spend real time on how my character looks. (i3) A session helps me stop thinking about the rest of my day.

Steps:

1. **Score yourself (3 min).** Each component score is `(mean of its three items − 1) / 4`, which gives 0 to 1.
2. **Pool anonymously (5 min).** Everyone enters three scores into the shared sheet. No names.
3. **Label (7 min).** In pairs, apply Yee's rule with `c = 0.75` to every row. Count the unlabelled share. Compare it with 43.75% from the model.
4. **Check the assumption (10 min).** Compute the correlation between the achievement and social columns (MA102 week 12 has the formula, or use the spreadsheet function). Is it negative, as Bartle's graph predicts, or near zero, as Yee found?

Expected output: the class's unlabelled share, its correlation between achievement and social, and a one-paragraph note on why a class of game students is a poor sample for either number.

## Common misconceptions

- **"Yee disproved Bartle."** Yee tested Bartle's model and kept much of it. Achievement, socializing and discovery all appear in the data. What failed was the idea that the four are exclusive types sitting on two axes.
- **"Components are just more types."** A component is a score every player has. Yee stresses that his subcomponents are not ten boxes.
- **"43% of players have no motivation."** They have motivations. They lack a single dominant one. Many of them are high on two components at once.
- **"Survey data tells you what to build."** It tells you what respondents said they value. Behaviour, retention and spending data tell you what they do. Neither alone is enough.

## Check yourself

1. Explain in two or three sentences, without formulas, why a forced-choice test like the Bartle Test cannot discover that players have no dominant type.
2. A designer says "our players are 40% achievers, so 60% of the budget should not go to progression systems." Using Yee's findings, name two things wrong with this reasoning.
3. A studio's survey uses Yee's ten subcomponents and a primary rule with `c = 0.75`. Assuming independent subcomponents, what share of players get a single label? Why might the real share be higher?
4. Which of Yee's findings would you cite to argue that a PvP arena and a gear-progression ladder can share an audience? Give the number.
5. Two players score (achievement, social, immersion) = (0.8, 0.2, 0.1) and (0.6, 0.55, 0.5). A type-based design document calls both "achievers". Describe one feature that would serve the second player and not the first.

<details>
<summary>Answers</summary>

1. Every answer forces a gain for one type and a loss for another, so the results always rank the types and one always comes out on top. A player who likes everything equally, or nothing much, still gets a type. The test's format assumes the conclusion.
2. First, a primary label does not mean the player ignores other components. Achievement and social correlate slightly positively, and many "achievers" are also high on social or immersion. Second, the unlabelled players (43% in Yee's data) are missing from the 40%/60% split, and they are moderate on progression too, so the budget logic is built on a partition that does not describe them.
3. `0.75⁹ ≈ 0.075`, about 7.5%. Real subcomponents are not independent. Those within a main component are correlated, so a player high on Advancement is often high on Mechanics too. Correlated scores change the share (in the interactive, for large `k`, positive correlation raises it a little).
4. The correlation between Advancement and Competition, about 0.41. Players who want progression also tend to want to compete.
5. The second player is nearly as social and immersive as they are achievement-driven. A group progression activity with a story, such as a guild questline that unlocks a shared hall the guild can decorate, serves all three of their scores. The first player would likely do it only for the reward.

</details>

## Lab / assignment hook

[Lab 09, a motivation survey study](../labs/lab09.md). You write your own twelve-item survey, collect at least 20 responses, score components, apply and vary the primary rule, test the independence assumption, and write a critique of type-based personas. This lab is the evidence base for your player-type critique (20% of the course grade).

## Sources

- Yee, N. "Motivations of Play in MMORPGs: Results from a Factor Analytic Approach." Daedalus Project white paper, nickyee.com/daedalus/motivations.pdf (undated; the PDF's file metadata gives 14 March 2005, and the paper cites Bartle's *Designing Virtual Worlds* as 2004; checked September 2026). Three limitations of Bartle's types; 3,200 respondents and 39 items; 10 subcomponents explaining 60% of variance; 3 main components explaining 54%; components correlated around 0.10; Achievement and socializing correlated about +0.10; Advancement and Competition about 0.41; the four differences from Bartle's model; gender and age differences and correlations with hours played (2,769 male and 431 female respondents); the primary motivation rule (top × 0.75 > second), described as "somewhat lax"; 57% assigned a primary motivation; 20% Achievement, 20% Immersion, 17% Social; primary motivations by gender (male 22.6%, 15.4%, 18.3%; female 4.2%, 25.1%, 30.9% for Achievement, Social, Immersion).
- Yee, N. (2006). "Motivations for Play in Online Games." *CyberPsychology & Behavior* 9(6), 772-775. doi:10.1089/cpb.2006.9.772. PubMed record 17201605. The peer-reviewed version; three components, achievement, social and immersion.
- Bartle, R. A. (1996). "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs." mud.co.uk/richard/hcds.htm.
- Wikipedia, "Bartle taxonomy of player types" (accessed September 2026). The Bartle Test by Erwin Andreasen and Brandon Downey (1999 to 2000); about 30 questions; Bartle Quotient totals 200% across the categories, citing Mulligan and Patrovsky (2003), *Developing Online Games*.
- Wikipedia, "Myers-Briggs Type Indicator" (accessed September 2026). Four dichotomies and 16 types; studies finding centrally peaked rather than bimodal score distributions, including Bess and Harvey (2002).
- Wikipedia, "Nick Yee" (accessed September 2026). The Daedalus Project; co-founding of Quantic Foundry with Nicolas Ducheneaut in 2015. No Quantic Foundry figures are used in this lecture.
- The `c^(k − 1)` model, the six example players, the correlated simulations and the nine class survey items are teaching constructions written for this course.

## Interactive spec: examples/w09-primary-motivation.html

**The one insight.** A single-label rule leaves a large share of players unlabelled, and that share falls fast as the number of motivation dimensions grows. Forced labels hide this by giving everyone a type. The student must see the unlabelled band fill the middle of the triangle, and see the tidy "forced label" bar next to the true labelled share.

**Layout.** Controls on top. Two panels, side by side at 1024 px and wider, stacked on mobile. A small six-player table below.

**Controls.**
- Slider `c`, 0.30 to 1.00, step 0.01, default 0.75.
- Segmented control `k`: 2, 3, 4, 8, 10. Default 3.
- Slider `r`, correlation between every pair of components, 0 to 0.5, step 0.1, default 0.
- Toggle "Forced label" (off by default).
- Button "New sample" reseeds the simulation.
- All keyboard operable.

**Simulation.** `n = 2,000` players (use 20,000 internally for the readout and draw only the first 2,000). For each player draw a shared normal `z0` and `k` independent normals `z_i`. Score `u_i = Φ(√r · z0 + √(1 − r) · z_i)`, where `Φ` is the standard normal cumulative distribution function (use a standard numeric approximation). Sort scores. Typed if `second < c × top`; label is the index of the top score. Forced label: always the index of the top score. Use a seeded PRNG (for example mulberry32) so a given seed gives repeatable numbers.

**Left panel.** If `k = 3`, a ternary plot. Position each player by `(u1, u2, u3) / (u1 + u2 + u3)`, corners labelled Achievement, Social, Immersion. Colour by label, grey for unlabelled. If `k ≠ 3`, replace with a strip chart of "second ÷ top" ratios (x from 0 to 1) with a vertical line at `c`; points left of the line are labelled.

**Right panel.** A horizontal bar split by label share, with a grey segment for unlabelled. Beside it, the formula value `c^(k − 1)` and the simulated share. With "Forced label" on, the grey segment disappears and a caption reads "every player labelled; the grey share is hidden, not gone".

**Six-player table.** The six players from the lecture (P1 to P6, `k = 3`), with second ÷ top and the label recomputed live from `c`.

**Test values (formula exact; simulated share with 20,000 players within ±0.01).**

| k | c | r | Formula | Simulated share typed |
|---|---|---|---|---|
| 2 | 0.75 | 0 | 0.750 | 0.750 |
| 3 | 0.75 | 0 | 0.5625 | 0.562 |
| 3 | 0.75 | 0.1 | 0.5625 | 0.544 |
| 3 | 0.75 | 0.3 | 0.5625 | 0.507 |
| 3 | 0.75 | 0.5 | 0.5625 | 0.465 |
| 4 | 0.75 | 0 | 0.4219 | 0.422 |
| 4 | 0.75 | 0.5 | 0.4219 | 0.360 |
| 8 | 0.75 | 0 | 0.1335 | 0.133 |
| 8 | 0.75 | 0.5 | 0.1335 | 0.185 |
| 10 | 0.75 | 0 | 0.0751 | 0.075 |
| 3 | 0.90 | 0 | 0.810 | 0.810 |
| 3 | 0.60 | 0 | 0.360 | 0.360 |

Six-player table at `c = 0.75`: P1 Achievement, P2 none, P3 none, P4 Social, P5 Immersion, P6 none (ratios 0.44, 0.94, 0.94, 0.67, 0.74, 0.76). At `c = 0.8`: P5 and P6 both Immersion.

**Style.** Shared palette from `templates/interactive-tokens.css`. Three label colours plus a neutral grey, each also marked by shape so the chart reads in grayscale. The formula value is shown in text next to the simulated value so students can copy both. No game art or logos.
