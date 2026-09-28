# GS101 · Week 14 — Games and representation

**Why this matters:** Every game you ship puts people on screen, and players notice who is there, who is in charge and who is missing. Arguments about this get loud fast and often go nowhere, because people compare numbers against different baselines without saying so. This week you learn to measure representation the way researchers do, and to say exactly what your numbers mean.

**You will be able to:**
- Compute a representation index for any group and convert it into the "percent over- or under-represented" form used in published studies.
- Explain how the choice of reference population (country, players, developers) changes the verdict, and justify a choice for a given question.
- Critique a representation claim by checking its sample, its weighting and its coding reliability.
- Design a character roster or creator default and state what a content census of your own game would find.

**Before class:** Williams, Martins, Consalvo & Ivory, "The virtual census: representations of gender, race and age in video games," *New Media & Society* 11(5), 2009, pp. 815-834 (read the introduction, method and results; about 12 pages). Skim the abstract and figures 1 to 3 of Jones et al., "The virtual census 2.0" (2025). Lynch et al., "Sexy, strong, and secondary" (2016), abstract and discussion only.

**Prerequisites from earlier courses:** None required. This lecture uses the rules-fiction ledger from [GS101 week 13](w13-ludology-vs-narratology.md) and the close-reading method from [GS101 week 1](w01-play-before-computers.md), section 5. If you are taking MA102 alongside, [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) covers proportions and weighted averages, and [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) explains why a sample of 150 games can support general claims while a sample of five cannot. Online identity and harassment come back in depth in [MMO305](../../MMO305-social-systems-and-online-behaviour/syllabus.md) and [MMO402](../../MMO402-emergent-society-governance-and-ethics/syllabus.md).

**Interactive:** [Representation index explorer](../examples/w14-representation-index.html). Keep it open during section 2.

---

## 1. What "representation" means here

**Representation** has two meanings that get mixed up. The first is counting, meaning who appears on screen, in what numbers and in which roles. The second is portrayal: how they are shown, what they do and what the work implies about them. A game can have many women in it and still show all of them as background decoration. A game can have one person from a group and show them with more depth than anyone else in the cast.

This lecture starts with counting because counting can be checked. Two careful people counting the same thirty minutes of play should get nearly the same numbers. That makes counting a good place to start an argument, though not a good place to finish one. Section 3 turns to portrayal.

A few terms first.

- A **content analysis** is a study that samples media (here, games), plays or watches a fixed slice of each, and records features of what appears using a written codebook.
- A **codebook** is the list of categories and rules for assigning them. "Primary character: controlled by the player at any point in the sample" is a codebook rule.
- **Coders** are the people who apply the codebook. Studies use two or more and measure how often they agree.
- **Inter-rater reliability** is that agreement, usually reported as **Cohen's kappa** (κ). κ = 1 is perfect agreement; κ = 0 is no better than chance. Values above about 0.8 are usually treated as strong.
- A **reference population** (or baseline) is the group you compare the on-screen numbers against.

The studies you will read this week followed exactly this design, so you can check their claims with arithmetic.

## 2. Worked example: the virtual census, and "compared to what?"

### The hook

In 2009 Dmitri Williams and three colleagues published a study they called "the virtual census." They took the top-selling games of one year (March 2005 to February 2006) across nine platforms, played 30 minutes of each, and coded every character. After removing non-human characters, they had 4,966 people. Weighted by how many copies each game sold, 85.23% of those characters were male.

In 2025 a team including two of the original authors repeated the study with the 100 best-selling boxed games of 2017. Here is one result that sounds like good news. **The share of white characters fell**, from 80.05% to 77.16%.

Here is the catch. **Measured against the US population, white characters became more over-represented, not less.** Both statements are true. By the end of this example you will be able to show why in two lines of arithmetic, and you will never again read a representation statistic without asking "compared to what?"

### The model

```
Representation index   RI = s_game / s_ref

Percent over/under     P  = (RI − 1) × 100%
```

- `s_game` is the group's share of characters in the sample (as a percentage or fraction).
- `s_ref` is the group's share of the reference population you choose.
- `RI = 1` means the group appears on screen in proportion to the reference. `RI = 0.5` means half as often as proportional. `RI = 2` means twice as often.
- `P` is the same fact in the wording studies use. `RI = 0.87` is "13% under-represented."

That is the whole model. Every number in this section is one division. The difficulty is never the arithmetic. It is choosing `s_ref` and being honest about the choice.

### Numbers you can check

First, confirm that the model reproduces the published claims. The 2009 study compared its race figures with the 2000 US census (the census counts Hispanic origin separately from race, so these columns do not sum to exactly 100%).

| Group | Share of characters, 2005-06 games | Share of US population, 2000 | RI | Published wording |
|---|---|---|---|---|
| White | 80.05% | 75.1% | 1.066 | 6.59% over-represented |
| Asian / Pacific Islander | 5.03% | 4.0% | 1.258 | 25.75% over |
| Black | 10.74% | 12.3% | 0.873 | 12.68% under |
| Biracial | 1.39% | 2.4% | 0.579 | 42.08% under |
| Hispanic | 2.71% | 12.5% | 0.217 | 78.32% under |
| Native American | 0.09% | 0.9% | 0.100 | 90% under |

Take the Black row by hand: `10.74 / 12.3 = 0.873`, and `(0.873 − 1) × 100 = −12.7%`. The paper's "12.68 percent under-represented" is this index. You now know the formula behind the prose.

Now the 2017 replication, compared with 2017 US Census estimates. One detail changes the baseline. The replication coded ethnicity as mutually exclusive categories (a character is Hispanic or another group, not both), so it compares against census figures that separate Hispanic origin out, such as "white, non-Hispanic." The 2009 study used the 2000 census race categories, where a Hispanic person is also counted in a race. For the white row, the replication supplies the matching 2000 figure, 69.10% white non-Hispanic, so you can compare like with like.

| Group | Share of characters, 2017 games | Share of US population, 2017 est. | RI 2017 | RI 2005-06 | Share changed | Index changed |
|---|---|---|---|---|---|---|
| White (non-Hispanic baseline both years) | 77.16% | 60.85% | 1.268 | 1.158 (80.05 / 69.10) | down 2.89 pts | **up** |
| Hispanic | 1.75% | 18.02% | 0.097 | 0.217 | down about 1 pt | **halved** |
| Black | 15.49% | 12.48% | 1.241 | 0.873* | up 4.75 pts | up, now over |
| Biracial | 3.15% | 2.13% | 1.479 | 0.579* | up 1.76 pts | up, now over |
| Asian / Pacific Islander | 2.40% | 5.77% | 0.416 | 1.258* | down 2.63 pts | down, now under |
| Native American | 0.04% | 0.74% | 0.054 | 0.100* | down 0.05 pts | halved |

*These 2005-06 indexes use the original study's 2000 baselines, which were defined slightly differently. Treat their direction as reliable and their exact size as approximate.

Here is the hook explained. The white share of characters fell by about three points. But on a consistent definition, the white non-Hispanic share of the US population fell by more than eight points, from 69.10% to 60.85%. The on-screen share moved much less than the population did, so the index rose from 1.16 to 1.27. The replication's authors make the same point in their discussion. White representation in games fell more slowly than the white share of the population.

Notice also that the two papers word "over-represented" differently. The 2009 paper uses the ratio. Whites were "6.59 percent" over-represented, meaning `RI = 1.066`. The 2025 paper uses the difference in percentage points. White characters were over-represented "by 10.95%" in 2005-06 (80.05 − 69.10) and by 16.31 points in 2017 (77.16 − 60.85). Both are legitimate. They are not the same measure, and the same finding can sound very different in each. When you read "X% over-represented," check which one the author means.

The Hispanic row is the starkest. The on-screen share dropped by only one point, but the population share rose from 12.5% to 18.0%, so the index fell from about 1 in 5 of proportional to about 1 in 10.

Gender tells a steadier story. Women were 14.77% of characters in 2005-06 and 18.98% in 2017, against population shares of 50.9% and 50.75%. The index rose from 0.29 to 0.37. That is progress, and it is also still barely a third of proportional.

### A second choice: which reference?

So far the reference has been the national population. That is one defensible baseline. It is not the only one. The 2009 paper itself offers two others, and each answers a different question.

| Reference population | Share female | RI for female characters (14.77%) | RI for female primary characters (10.45%) | The question it answers |
|---|---|---|---|---|
| US population, 2000 | 50.9% | 0.29 | 0.21 | Do games look like the society they are sold in? |
| Game players, ESA 2009 figure cited by the paper | 40% | 0.37 | 0.26 | Do games show the people who buy and play them? |
| Game developers, 2005 survey cited by the paper | 11.5% | 1.28 | 0.91 | Do games look like the people who make them? |

Against society or players, women are heavily under-represented. Against developers, female characters appear **more** often than female developers do, and female primary characters (the ones you control) appear at almost exactly the developer rate. The paper's authors use this third comparison as evidence for an explanation. People tend to make characters who look like themselves, and the industry's workforce was about 88.5% male.

None of these rows is "the" answer. The honest move is to state your question first, pick the reference that matches it, and name it in the same sentence as the number.

### A third choice: what you count

The 2009 study weighted every game by its sales. A game that sold 4 million copies counted twice as much as one that sold 2 million. The authors report both versions.

| Sample | Female share, 2005-06 | Female share, 2017 |
|---|---|---|
| Games as made (each title counts once) | 18.76% | 22.41% |
| Games as bought (weighted by sales) | 14.77% | 18.98% |

In both years the games people bought had a smaller share of women than the games studios made. The 2009 paper traces part of this to the best-selling sports games of the time, which were all adaptations of men's professional leagues. Weighting is a choice about what you want to measure. Unweighted counts describe what developers produced. Weighted counts describe what players actually saw.

### A visual you can move

Open the interactive. The left panel shows the raw shares as paired bars, game against reference, for each group. The right panel shows the index as a single bar per group on a log scale centred on 1, so "half as often" and "twice as often" sit the same distance from the centre. Switch the year from 2005-06 to 2017 and watch the white bars on the left shrink while the white index on the right grows. Then switch the reference from "US population" to "developers" on the gender tab and watch the female index cross the line at 1. The raw shares never change when you switch reference. Only the verdict does.

### Cross-game recognition

The index is one idea you can carry to any "who is on screen" claim. Rewrite each claim into `s_game / s_ref` and ask what `s_ref` is.

**Age in the same study.** Adults (20 to 64) were 86.88% of characters against 58.97% of the 2000 population, so `RI = 1.47`. The paper's wording is that adults appear "47.33 percent" more often than their prevalence, which is this index. Children (3.58% against 21.41%, `RI = 0.17`) and people over 65 (1.75% against 12.43%, `RI = 0.14`) were both far under. Teens came out close to proportional (`7.81 / 7.18 = 1.09`). Same formula, a different axis, and it immediately tells you who is missing.

**Sports games and the league baseline.** The 2009 paper found that E-rated games had far more Black and biracial characters than other ratings. The reason was the popular sports titles, whose rosters were real athletes from real leagues. For those games the natural reference is the league, not the country. Against the country, a basketball game might look very over-representative of one group. Against the league it adapts, it is close to `RI = 1` by construction, because it copies the roster. The index is the same. The right `s_ref` changed because the question changed ("does this game reflect its source?").

**Primary vs secondary roles.** Split the characters by role and compute the index twice. In 2005-06, female primary characters were 10.45% (RI 0.21 against population) and female secondary characters 14.65% (RI 0.29). By 2017 the replication reports 21.57% for primary and 20.64% for secondary. The gap by role closed, and in 2017 women were slightly more common as the character you play than as the ones around you. Role is where counting starts to touch portrayal, because the primary character is the one whose goals the game adopts.

### Eyes-open design judgment

- **Always name the baseline.** "Only 19% of characters are women" is a share. It becomes a claim about fairness only when you add "against a population that is 51% women" or "against a player base that is about 40% women." Critics and defenders often talk past each other because each picked a different `s_ref` without saying so.
- **Proportional is not automatically the goal.** A game set in a Viking village or a 1940s submarine may have a historically narrow cast. The index then measures the setting choice, and the critical question moves to why that setting was chosen and how the cast is shown. A fantasy world has no historical reason for any particular cast, so its index reflects designer choices directly.
- **Counting is necessary and not sufficient.** An index of 1 with every member of a group cast as a villain or as scenery is not good representation. Section 3 covers portrayal.
- **Defaults are representation decisions.** The 2017 replication found that 9 of its 100 games let players customize the main character, and the coders recorded the default appearance. Any census of your game will do the same. If you ship a character creator, the default body, face and name are what most screenshots, trailers and first sessions show. That default is the character your game puts forward, whether or not you think of it that way.
- **Check the method before the conclusion.** Ask how the sample was chosen, whether it was weighted, what counted as a character, and how well the coders agreed. The 2009 study reports κ of 0.93 for gender, 0.92 for age and 0.89 for race. The 2017 replication reports 0.95 for gender but 0.73 for race and age. Coding race from appearance is harder, and the authors discuss why. A κ of 0.73 is acceptable, but it means the race figures carry more error than the gender figures.

### Check the model

1. In the 2017 sample, female characters were 18.98% against a population that was 50.75% female. Compute RI and state it in the "percent under-represented" form.
2. A game's roster has 24 playable characters, 6 of them women. Compute RI against a population that is 50% women and against a player base that is 45% women.
3. The Asian / Pacific Islander share of characters fell from 5.03% to 2.40% between the two samples, and the population share rose from 4.0% to 5.77%. Which of the two changes did more to move the index? (Hint: compute the 2017 index with the 2000 population share, then with the 2017 population share.)

<details>
<summary>Answers</summary>

1. `RI = 18.98 / 50.75 = 0.374`. `P = (0.374 − 1) × 100 ≈ −62.6%`, so about 63% under-represented.
2. Share = `6 / 24 = 25%`. Against 50%: `RI = 0.50`, 50% under. Against 45%: `RI = 0.56`, about 44% under.
3. With the old population share: `2.40 / 4.0 = 0.60`. With the new one: `2.40 / 5.77 = 0.416`. The on-screen drop alone took the index from 1.26 to 0.60. The population change took it from 0.60 to 0.42. The on-screen drop did more.

</details>

## 3. From counting to portrayal

Counting tells you who is present. Portrayal asks what the game does with them. Three questions organize most portrayal research, and each has a rough measurable form.

### Role and agency

Who acts, and who is acted upon? The primary/secondary split is the simplest version. A richer one records whether a character makes choices that change the plot, has goals of their own, or exists only to be rescued, to die, or to give the protagonist a reason to act. Critics sometimes call the last pattern a character used as a device. You can count it. For each named character, record whether they make at least one decision the story treats as consequential.

### Sexualization and the body

Teresa Lynch and colleagues analysed 571 games released between 1983 and 2014 that featured playable female characters. They found that sexualization of female characters peaked in the 1990s and has declined since. It was higher in traditionally male-oriented genres such as fighting games than in role-playing games. Teen- and Mature-rated games were more sexualized than Everyone-rated games. Female characters in secondary roles were more sexualized than primary ones. And a game's critical success was unrelated to how sexualized its characters were. That last finding matters for designers, because it weakens the claim that critics reward sexualized designs. Note also that this study measures *how* characters are drawn, not *how many* there are. It needs its own codebook, with categories such as body proportions and clothing, and its own reliability checks.

### Stereotype and context

Are members of a group shown in a narrow set of roles? The 2009 paper observed that outside sports games, many of the remaining Black characters in its sample appeared as gangsters or street figures. That is a portrayal finding sitting inside a counting study, and it changes the meaning of the index. A Black RI close to 1 across all games hid a very different picture once sports were separated out. This is why good studies break the index down by genre and role before drawing conclusions.

### Reading representation with the ledger

The rules-fiction ledger from week 13 applies here too. Representation is not only in the art and the script. It is also in the rules.

- In the rules layer, ask which characters have stats, abilities and verbs, and which exist only as scenery or targets. If the playable women in a fighting game have lower health than the men, the rules make an argument about women, whatever the fiction says.
- In the fiction layer, ask how the characters are framed: named or unnamed, with or without backstory, shown from whose point of view.
- Then check whether the layers agree. A game whose story celebrates a character while its rules make her the weakest option in the roster is tense in exactly the week 13 sense.

### Where representation comes from

Why do the numbers look the way they do? The 2009 paper tests three explanations and leans toward a combination of developer demographics and marketing assumptions about who plays. Its evidence is the index against developers. Female characters (15%) sat much closer to the share of female developers (11.5%) than to the share of female players (about 38 to 40%). That points to a production-side cause, not a demand-side one. If sales alone drove the cast, the paper argues, there would be far more women on screen, because women were already a large share of buyers.

This is a historical argument as much as a statistical one. The previous weeks traced who made games in each era: university labs, arcade companies, bedroom coders, publisher-backed studios. Each era's workforce left fingerprints on who appears in its games. When you read a game critically, "who made this, and who did they imagine was playing?" is part of step 4 of your close-reading method (place it in context).

## 4. Doing this responsibly

A few practical rules for when you run a census yourself, which you will in the lab.

- **Code what is shown, not what you assume.** Coders judge from on-screen appearance and in-game text. That is an imperfect measure of a fictional character's identity, and every study says so. Record "cannot determine" rather than guessing, and report how many characters fell there.
- **Separate the categories you inherit from the ones you choose.** Using the national census categories makes comparison possible, but those categories are themselves historical and political choices. The 2017 replication discusses coding gender beyond a binary and reports that its sample contained five nonbinary characters, four of them non-human, and no transgender characters.
- **Report the denominator.** "Three women" means little until you say "out of 40 human characters in 30 minutes."
- **Separate description from judgment.** Your census is description. Your close reading is judgment. Keep them in different paragraphs, so a reader who disagrees with your judgment can still use your numbers.
- **Remember the players.** Representation research exists because on-screen patterns are thought to shape how players see groups and themselves. The 2009 paper grounds this in social identity theory: people look for representations of their own group, and absence can signal that a group does not matter. You do not need to settle how strong those effects are to see why studios, players and critics care.

## In-class activity (25 min)

In groups of three, run a mini census on a character-select screen.

Materials: screenshots or a live view of three character-select screens from different genres (the instructor supplies a fighting game, a hero shooter and a party-based RPG, all current versions), the codebook from [Lab 14](../labs/lab14.md), which the class shares so data can be pooled (gender as presented: woman, man, cannot determine; role: all playable here; age band: child, teen, adult, older adult, cannot determine; human or non-human), and the interactive's Custom tab.

1. (8 min) Two members code each roster independently. The third keeps time and does not code.
2. (5 min) Compare codes. Count agreements and compute simple percent agreement for gender and for age band.
3. (5 min) Enter the counts for human characters into the interactive. Compute the female RI against a 50% baseline, then against a baseline you choose and justify (the game's reported player base, its genre's player base, or its source material).
4. (7 min) Write three sentences: one description (the numbers), one comparison across the three games, one judgment that names a rule or portrayal choice, not only the count.

Expected output: two code sheets, a percent-agreement figure, two indexes per game, and the three-sentence reading.

## Common misconceptions

- **"If the share went down, representation got worse."** Only if the baseline stayed put. The white share of characters fell between the two censuses while white over-representation rose, because the population changed more than the games did.
- **"Representation means matching the population exactly."** Proportion is one reference. Players, developers or the source material are sometimes better ones, and some settings have a reason for a narrow cast. What matters is stating the reference and defending it.
- **"More characters from a group solves it."** Counting is only the first question. Role, agency and portrayal can make a proportional cast still narrow, as the 2009 paper's note on non-sports Black characters shows.
- **"Coding is objective, so the numbers are facts."** Coding is a disciplined judgment. That is why studies report κ. A figure with κ = 0.73 carries more uncertainty than one with κ = 0.95.

## Check yourself

1. The 2009 study reports adults as "47.33 percent" over-represented. Rebuild that figure from the shares in section 2.
2. A critic says: "Women were 15% of characters in 2005-06, almost exactly the share of women making games, so games were representative." What reference has the critic chosen, what question does it answer, and what question does it not answer?
3. Unweighted, the 2017 sample was 22.41% female. Weighted by sales, it was 18.98%. Explain in one sentence what this tells you about which games sold best.
4. You are designing a 16-character roster for a hero shooter. You want the female RI against a 50% baseline to be at least 0.75. What is the minimum number of women? Name one portrayal check you would add on top of the count.

<details>
<summary>Answers</summary>

1. `RI = 86.88 / 58.97 = 1.473`. `P = (1.473 − 1) × 100 = 47.3%`.
2. The critic chose developers as the reference. That answers "do games look like the people who make them?" (roughly yes, `RI ≈ 1.3` overall, 0.91 for primary characters). It does not answer whether games look like the society or the players they are sold to, where RI is about 0.29 to 0.37.
3. The best-selling games had a smaller share of female characters than the average game made that year, so the titles that sold most copies were more male-dominated than the typical release.
4. `RI = s / 50 ≥ 0.75` means `s ≥ 37.5%`. `0.375 × 16 = 6`, so at least 6 women. A portrayal check: compare average health, damage and ability counts by gender to make sure the rules do not make women systematically weaker picks, or count which characters get story roles in the trailer and the tutorial.

</details>

## Lab / assignment hook

[Lab 14, a virtual census of one game](../labs/lab14.md). You will code 30 minutes of a game with a partner using the course codebook, compute Cohen's kappa for your coding, compute representation indexes against two references you justify, and write a 700-word reading that combines the count with one portrayal finding and one rules-layer finding. It feeds directly into the final essay.

## Sources

- Williams, D., Martins, N., Consalvo, M. & Ivory, J. D. (2009). "The virtual census: representations of gender, race and age in video games." *New Media & Society* 11(5), 815-834. doi:10.1177/1461444809105354. Author copy at dmitriwilliams.com. Sample of top-selling games from March 2005 to February 2006 on nine platforms; 8,572 characters coded, 4,966 human; 30 minutes per game; sales weighting; κ values; figures 1 to 3 (gender by role, race, age); unweighted 81.24% male; the 2000 census baselines; the 40% female player figure (ESA 2009, as cited) and 38% (discussion); developer demographics (Gourdin 2005, as cited); the note on sports titles and on non-sports Black characters.
- Jones, S. S. Y., Harrisson, A., Pedraça, S., Marchessault-Brown, J., Williams, D. & Consalvo, M. (2025). "The virtual census 2.0: A continued investigation on the representations of gender, race, and age in videogames." *New Media & Society*. doi:10.1177/14614448251336427. Author copy at dmitriwilliams.com. Top 100 best-selling boxed games of 2017; 13,144 characters coded, 8,178 human; 15 minutes plus opening cutscenes per game; 2017 census estimates; female share 18.98% weighted and 22.41% unweighted; race figures in figure 2; primary and secondary female shares; 9 of 100 games with customizable characters; κ of 0.95, 0.73 and 0.73; nonbinary and transgender counts.
- Lynch, T., Tompkins, J. E., van Driel, I. I. & Fritz, N. (2016). "Sexy, strong, and secondary: A content analysis of female characters in video games across 31 years." *Journal of Communication* 66(4), 564-584. doi:10.1111/jcom.12237. Findings as summarized in the abstract.

## Interactive spec: examples/w14-representation-index.html

**The one insight:** a group's share of characters and its representation index can move in opposite directions, because the index also depends on the reference. The raw-share view and the index view must be linked so that switching year or reference visibly changes one and not the other.

**Layout.** Two linked panels, side by side at 1280px, stacked at 390px. Tabs above them: "Race", "Gender", "Age", "Custom".

**Left panel, "Shares".** For each group, a pair of horizontal bars: share of characters (solid) and share of the reference population (outline). Exact percentages printed at the end of each bar.

**Right panel, "Index".** For each group, one horizontal bar from a centre line at `RI = 1`, drawn on a log2 scale from 0.05 to 4, so 0.5 and 2 are equidistant from centre. Bars left of centre are "under", right of centre "over". Print `RI` to 3 decimals and `P = (RI − 1) × 100%` to 1 decimal next to each bar.

**Controls.**
- Year toggle on Race and Gender tabs: "2005-06 games vs 2000 census" and "2017 games vs 2017 estimates".
- Reference selector on the Gender tab: "US population", "Players (ESA 2009 as cited)", "Developers (2005 as cited)". Players and developers apply to 2005-06 only; for 2017 the selector shows population only, with a note that the replication does not report comparable player and developer baselines.
- Role selector on the Gender tab: "All characters", "Primary", "Secondary".
- "Show change" checkbox: when on, draw a ghost marker at the other year's value in both panels, with an arrow, so the student sees share and index arrows point opposite ways for the white row.
- Custom tab: editable table of up to 8 rows (group name, count on screen, reference share %). Computes shares from counts and draws both panels. Used in the in-class activity and lab.

**Data (exact).**
- Race 2005-06 (games / 2000 census): White 80.05 / 75.1 (original study baseline), with an alternative White baseline of 69.10 (non-Hispanic, used for the year comparison and whenever "Show change" is on); Black 10.74 / 12.3; Hispanic 2.71 / 12.5; Biracial 1.39 / 2.4; Native American 0.09 / 0.9; Asian/PI 5.03 / 4.0.
- Race 2017 (games / 2017 est.): White 77.16 / 60.85; Black 15.49 / 12.48; Hispanic 1.75 / 18.02; Biracial 3.15 / 2.13; Native American 0.04 / 0.74; Asian/PI 2.40 / 5.77.
- Gender 2005-06 female share: all 14.77, primary 10.45, secondary 14.65. References: population 50.9, players 40, developers 11.5.
- Gender 2017 female share: all 18.98, primary 21.57, secondary 20.64. Reference: population 50.75.
- Age 2005-06 (games / 2000 census): Children 3.58 / 21.41; Teens 7.81 / 7.18; Adults 86.88 / 58.97; Elderly 1.75 / 12.43.

**Test values.** White 2005-06 RI 1.066 against the original 2000 baseline (P +6.6%), 1.158 against the 2000 non-Hispanic baseline, 2017 RI 1.268 (+26.8%). Hispanic 0.217 then 0.097. Asian/PI 1.258 then 0.416. Female all-characters vs population 0.290 (2005-06) and 0.374 (2017); vs players 0.369; vs developers 1.284. Female primary vs developers 0.909. Adults 1.473. Custom: 6 of 24 with reference 50 gives 0.500.

**Text on first screen.** Default view is the Race tab with "Show change" on. Caption: "The white share of characters fell. White over-representation rose." No instructions above the fold.

**Notes.** Generic bars only; no game art or character images. A footer names both studies with DOIs and notes that census Hispanic origin overlaps race categories, so race columns need not sum to 100.
