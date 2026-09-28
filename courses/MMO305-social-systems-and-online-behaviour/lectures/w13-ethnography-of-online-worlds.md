# MMO305 · Week 13 — Ethnography of Online Worlds (Taylor, Boellstorff)

**Why this matters:** Telemetry tells you what players did. It rarely tells you what they meant, what they owe each other, or which unwritten rules keep a server civil. Ethnography is the method that finds those things, and it has one built-in trap. The people you meet while you are in the world are not a fair sample of the people who play it.

**You will be able to:**
- Describe participant observation, field notes and thick description, and name what each gives a designer that a dashboard cannot.
- Compute how strongly time-in-world weights the players an observer meets, and correct an observed sample back to the population with inverse-hours weights.
- Compute the chance that a player with a given weekly schedule shows up in a set of observation sessions, and use it to plan fieldwork.
- Critique a published study of an online world for who it saw, who it missed, and what it did about it.

**Before class:** Taylor, *Play Between Worlds* (2006), chapter 1, "Finding New Worlds" (pp. 1-20), and chapter 3, "Beyond Fun: Instrumental Play and Power Gamers" (pp. 67-92). Boellstorff, *Coming of Age in Second Life* (2008), chapter 3, "Method" (pp. 60-86 in the 2015 paperback). Ducheneaut, Yee, Nickell and Moore (2006), "Alone Together?", read the section on data collection and the one on playing time. Skim Boellstorff, Nardi, Pearce and Taylor, *Ethnography and Virtual Worlds: A Handbook of Method* (2012), the chapters on participant observation and on ethics.

**Prerequisites from earlier courses:** [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (sampling bias versus sampling error). [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (interview technique). [GS101 week 10, World of Warcraft and the mass-market MMO](../../GS101-history-and-critical-study-of-games/lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md) (the game most of this week's studies examine). [MMO301 week 4, EverQuest: the treadmill and the raid](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w04-everquest-the-treadmill-and-the-raid.md) (the game Taylor studied). Earlier this term, [MMO305 week 2, playing alone together](w02-playing-alone-together.md) introduced the Ducheneaut et al. findings; this week looks at how they were produced.

**Interactive:** [Who plays is not who you meet](../examples/w13-who-you-meet.html). Use it during section 2.

---

## 1. What ethnography is, and why a designer should care

Ethnography is the study of a group's way of life by spending long periods inside it. The core method is **participant observation**: you take part in the group's activities while watching and recording them. You play the game, join the guild, turn up for the raid, and write down what happened afterwards. Anthropologists developed the method for villages and neighbourhoods. Since the 1990s it has been applied to MUDs, MMOs and social worlds, on the argument that a place made of software is still a place where people build norms, status and obligations.

Three terms carry most of the weight.

- **Field notes** are the ethnographer's raw data. They are written during or soon after observation and record what happened, who was there, what was said, and what the observer thought at the time. Short "jottings" taken in the moment are expanded into full notes the same day.
- **Thick description** is a description that includes the meaning an action has for the people doing it, and not only its surface. The philosopher Gilbert Ryle introduced the term, and the anthropologist Clifford Geertz made it the standard for ethnography in *The Interpretation of Cultures* (1973). "A player typed /bow at the healer" is thin. "At the end of a wipe-heavy night, the raid leader bowed to the healer in raid chat, which in this guild is the accepted way to apologise for blaming someone publicly" is thick.
- **Emic and etic** views. The emic view is the insiders' own categories ("a ninja looter", "a carry"). The etic view is the outside analyst's categories ("a norm violation in resource allocation"). Good fieldwork records the first before translating into the second.

Why should a designer care? Because most of the social rules of an MMO are not in the code. The Warcraft Wiki's page on mob tapping records one example. In classic World of Warcraft only the first player (and that player's party) to hit a monster gets credit for it, and players built an etiquette on top of that rule. You invite a stranger to your party if you are both after the same monster. Snatching a monster that another player was about to engage counts as rude, and doing it on purpose to block someone's quest counts as griefing. None of that etiquette is in the game's code. It emerged from the code, it shaped how the game felt, and a designer who changes the tapping rule changes it. You find rules like this by being there.

### The canonical studies

You will meet four works again and again. Each one is a model of a different kind of fieldwork.

**T. L. Taylor, *Play Between Worlds* (MIT Press, 2006).** A study of EverQuest built on the author's own play and on conversations with players. Taylor gives sustained attention to power gamers (players who pursue efficiency and top-end achievement with great intensity), to women who play, and to the ways players build and own the culture around a game. Its main argument is that the line between "the game" and "real life" is blurry in practice. Money, friendship and reputation cross it all the time. Taylor now teaches Comparative Media Studies at MIT and has since written on esports (*Raising the Stakes*, 2012) and live streaming (*Watch Me Play*, 2018).

**Tom Boellstorff, *Coming of Age in Second Life* (Princeton University Press, 2008; second edition 2015).** More than two years of fieldwork inside Second Life, conducted as the avatar "Tom Bukowski". Boellstorff's stance is that a virtual world can be studied the same way anthropologists have always studied cultures, by living among its residents and watching what they do. His topics include gender, money, conflict and griefing, and how residents experience place and time.

**Bonnie Nardi, *My Life as a Night Elf Priest* (University of Michigan Press, 2010).** An anthropological account of World of Warcraft, based on Nardi's own play as a member of the game's guilds. It is one of the best-known ethnographies of the game.

**Ducheneaut, Yee, Nickell and Moore, "Alone Together?" (CHI 2006).** This one is not a book-length ethnography, and it is the reason it belongs on the list. The authors began with what they call a virtual ethnography. All four created characters and alts on different servers, joined guilds, and took part in quests, raids and player-versus-player combat. Then they moved to a quantitative method. They wrote a program that used the game's `/who` command to take a census of the entire server every 5 to 15 minutes, starting in June 2005, on five servers. Over the study they observed 129,372 unique characters. It is a mixed-methods study. The qualitative phase told them which questions were worth counting.

In 2012 Boellstorff, Nardi, Celia Pearce and Taylor co-wrote *Ethnography and Virtual Worlds: A Handbook of Method* (Princeton University Press). It is the standard how-to for this kind of fieldwork, and you will use it again in [MMO405 week 7, ethnography and participant observation](../../MMO405-research-methods-in-online-games/syllabus.md).

## 2. Worked example: who you meet is not who plays

### The hook

Ducheneaut and colleagues measured the average play time of a World of Warcraft character in 2005 at 10.2 hours per week. They were careful to add that players often run several characters, so the time per *player* is higher. Now imagine a different study. An ethnographer logs in every evening for a month, chats with everyone they meet, and asks each one how many hours a week they play. What average will that ethnographer get?

The answer is not 10. On a server like the one modelled below, it comes out above 20, even if every single person answers honestly. Nobody lied and the arithmetic is right. The sample is the problem, and the bias has a precise size you can compute.

### The model

Split the population into groups. Group `i` makes up a share `p_i` of the players and each of its members plays `h_i` hours per week. There are 168 hours in a week.

At any random moment you are in the world, a group's share of the players online is proportional to its share of the population times its hours:

```
q_i = p_i × h_i / Σ_j (p_j × h_j)
```

- `p_i` is the group's share of all players (the population).
- `h_i` is the group's weekly hours.
- `q_i` is the group's share of the people you meet (the encounters).

This is called **length-biased sampling**. You sample moments, and every moment is filled by whoever happens to be online. A player who is online four times as long is four times as likely to be the one in front of you.

Two consequences follow directly.

The average hours of the people you meet is

```
mean hours met = Σ (p_i × h_i²) / Σ (p_i × h_i)
               = true mean + variance / true mean
```

So the bias grows with the spread of play time. If everyone played the same hours, the variance would be zero and there would be no bias. MMO populations are the opposite of that.

The correction runs the other way. If you only have the encounter shares `q_i`, weight each observed person by `1 / h_i` and renormalise:

```
p_i = (q_i / h_i) / Σ_j (q_j / h_j)
```

This is an inverse-probability weight. Everyone you met had a chance of being met proportional to their hours, so you divide that chance back out.

### Numbers you can check

Take an invented server with three groups. The hours are chosen so that the population mean is 10 hours, close to the 2005 WoW figure, which keeps the scale familiar.

| Group | Share of players `p` | Hours per week `h` | `p × h` | Share of encounters `q` |
|---|---|---|---|---|
| Casual | 60% | 4 | 2.4 | 24% |
| Regular | 30% | 12 | 3.6 | 36% |
| Hardcore | 10% | 40 | 4.0 | 40% |
| Total | 100% | mean 10.0 | 10.0 | 100% |

Hardcore players are one tenth of the server and four tenths of the people you meet. Casual players are the majority of the server and under a quarter of your encounters.

The mean hours of the people you meet is

```
(0.6 × 16 + 0.3 × 144 + 0.1 × 1,600) / 10 = (9.6 + 43.2 + 160) / 10 = 21.28 hours
```

That is more than double the true 10. Check it with the second form. The variance is `Σ p h² − mean² = 212.8 − 100 = 112.8`, and `10 + 112.8 / 10 = 21.28`. Both forms agree.

Now run the correction. Suppose all you know is the encounter column (24%, 36%, 40%) and the hours. Divide each by its hours: `0.24/4 = 0.06`, `0.36/12 = 0.03`, `0.40/40 = 0.01`. The sum is 0.10. Divide again by the sum: 60%, 30%, 10%. The population comes back exactly.

### Will this player ever appear in my notes?

Length bias also decides who is missing altogether. Suppose you observe at `k` random one-hour moments spread across the week. A player online `h` hours has a chance `h/168` of being online at each moment, so the chance they appear at least once is

```
P(seen) = 1 − (1 − h/168)^k
```

This is the complement rule from MA102 week 3.

| Hours per week | `k = 10` sessions | `k = 96` sessions | `k = 672` (every 15 minutes for a week) |
|---|---|---|---|
| 4 | 21.4% | 90.1% | above 99.9% |
| 12 | 52.3% | above 99.9% | above 99.9% |
| 40 | 93.4% | above 99.9% | above 99.9% |

Ten sessions, a realistic number for a student doing field observation, will find almost every hardcore player and miss nearly four in five casual ones. An automated census at 5 to 15 minute intervals, like Ducheneaut's, runs hundreds of samples a week, so almost every character appears at least once. That is why the census could report per-character figures such as the 10.2-hour mean. It counted each character once and then measured that character's time, instead of counting sightings. Counting unique people, not sightings, is the other standard fix for length bias.

Open the interactive. The left panel shows the server by head count and the right panel shows it by encounter, with the same three groups and colours. Drag the hardcore hours from 12 up to 60 and watch the right panel fill with one colour while the left panel does not move at all. Then switch on the correction and watch the right panel snap back to match the left.

### Cross-game recognition

Length bias turns up wherever you sample by presence instead of by person. It goes by several names.

**The friendship paradox (Feld, 1991).** The sociologist Scott Feld showed that, in most networks, your friends have more friends than you do on average. The reason is the same weighting. Pick a random friend of a random person and you are picking an end of a random friendship. A person with 40 friendships is 40 times as likely to be picked as a person with one. Replace hours `h` with friend count `d` and the formula is identical: mean friends of a friend `= Σ d² / Σ d`. In a guild this is the reason the players you know best seem to know everyone. You met them through their many ties. It is also why the players in guild chat every night give you a skewed view of the guild. The guild network analysis in [MMO405 week 9](../../MMO405-research-methods-in-online-games/syllabus.md) runs into the same effect.

**Participation inequality on forums and Discord (Nielsen, 2006).** Jakob Nielsen's "90-9-1" rule of thumb says that in large online communities about 90% of users only read, 9% contribute occasionally, and 1% contribute most of the content. Reading a forum samples by *post*, so it is length-biased in posting rate exactly as an evening in-game is length-biased in hours. A design team that reads its official forums is interviewing the 1% and hearing them 90 times over. Week 12's community management work has to correct for this, or it will be steered by the loudest few.

**Ethnographers' field sites.** Taylor's EverQuest work gives long attention to power gamers. Nardi's World of Warcraft account is written from inside the guilds she played in. Neither is a mistake, because both authors say clearly who they studied and why. The lesson is about claims. A study embedded in a raiding guild can say a great deal about raiding culture. It cannot say what "WoW players" do without the correction above or a second, differently sampled source. Ducheneaut and colleagues paired their in-game ethnography with a whole-server census for exactly this reason.

Three settings, one formula. When someone reports what "players" think, ask how the players were reached. If it was through presence, posting or connection, their answer is weighted by `h`, and you know how to weight it back.

### Design and research judgment

The bias is not a reason to stop doing fieldwork. It is a reason to be exact about what fieldwork can support.

- **Name your sample.** An ethnography of the 40-hour players is a legitimate study of the 40-hour players, and those players often set the norms everyone else lives under. Say who you saw.
- **Correct counts, not meaning.** Inverse-hours weighting fixes shares and averages. It cannot recover a casual player's reasons if you never talked to one. For those you need targeted recruitment, such as interviewing players who log in once a week (UX201 week 12 covers recruiting).
- **Don't over-correct.** A weight of `1/h` assumes you know each person's hours. Self-reported hours are noisy, and the error need not be the same for every group. With bad hours, the corrected numbers can be worse than the raw ones. Report both.
- **Designers carry the same bias.** Your team plays its own game in the evenings and meets the evening crowd. Your QA and community staff live in the forums. Every internal intuition about "what players want" is length-biased unless someone deliberately goes looking for the players who are rarely there.

## 3. Doing fieldwork in an online world

### Choosing a field site

A field site in an MMO is rarely "the server". It is a guild, a city hub, a PvP battleground queue, a roleplay community, a Discord. Choose it by your question. If you want to know how newcomers learn norms, the site is the starting zone and its chat channel, at several times of day. If you want to know how loot disputes end, the site is a raiding guild that will let you in.

Timing is part of the site. Run the `P(seen)` numbers from section 2 before you plan sessions. If the players you care about log in for four hours a week, ten sessions will find about one in five of them. Spread your sessions across the week, including mornings and weekday afternoons, or recruit those players directly.

### Access and the observer's role

Participant observation runs along a spectrum. At one end you only watch. At the other you are a full member who also happens to be taking notes. Boellstorff lived in Second Life for more than two years, and Nardi played World of Warcraft as a guild member. Full participation gives you insider knowledge and trust. It also makes you part of what you are observing. If you are the guild's main healer, your research changes the guild. Write down your role and how it may have shaped what you saw.

Access usually comes through a gatekeeper, such as a guild leader or a community moderator. Ask them explicitly and record what you told them.

### Field notes in practice

Keep three kinds of record, clearly separated.

1. **Jottings** during play: timestamps, names (to be replaced by pseudonyms), a few words of what happened. In an MMO the chat log does much of this for you, but only for text. Movement, silence and emotes need your own notes.
2. **Expanded notes** written the same day: a full account of each event with who, what, where and when, and what happened before and after.
3. **Analytic memos**: your interpretations, kept apart from the description so a reader can see which is which.

A useful habit is to write each event twice, once thin and once thick. The thin version is what a screenshot would show. The thick version adds what it meant to the people involved, and how you know that (they told you, or you saw the same thing happen three times).

### Ethics

Online fieldwork raises ethical questions that the offline kind handles more easily. The Association of Internet Researchers (AoIR) publishes guidelines for them. The current version is *Internet Research: Ethical Guidelines 3.0* (2019), which replaced the 2002 and 2012 versions. Its approach is case-based judgment rather than a fixed checklist. For a class project the working rules are these:

- **Public is not the same as fair game.** A zone chat channel is visible to anyone, but its users did not expect to be quoted in a report. Paraphrase and use pseudonyms.
- **Pseudonyms need pseudonyms.** A character name is already an identity, and it is searchable. Replace it, and replace the guild and server names too if the community is small.
- **Consent scales with intimacy.** Watching a city hub needs no consent. Joining a guild's voice chat to study it does. Interviews always do.
- **Your institution may require review.** In most universities any study involving interviews with identifiable people needs ethics approval. MMO405 week 10 covers the review process. For this course's field observation, your lab brief (lab 13) is written so that it stays within observation of public spaces.

## 4. What ethnography gives a designer

It is fair to ask what a designer does with a thick description. Three things.

**It finds the unwritten rules your systems create.** The classic-WoW tapping etiquette in section 1 is one example. The social contract around loot councils, the "no ninja" norms of pickup groups, and the informal queue for a rare spawn are others. These norms are part of your design even though you did not write them. If you remove the system that produced them, they disappear with it.

**It tells you what a number means.** Ducheneaut and colleagues found that WoW characters spent much of their time outside groups. The ethnographic phase is what let them interpret that. Players were not antisocial. They liked being surrounded by others, as an audience and a presence, while playing on their own. A dashboard shows the grouping ratio. It takes fieldwork to see that "alone" was not the right word for it.

**It generates hypotheses worth instrumenting.** Fieldwork is slow and small, and telemetry is fast and broad. The productive loop runs between them. You observe a norm, form a hypothesis, instrument it, and then go back into the field when the numbers surprise you. MMO308 and MMO405 build on this loop.

## In-class activity (25 minutes)

Work in pairs. You need one laptop with a free-to-play MMO installed, or the 10-minute recording of a city hub that the instructor provides on the course page (chat log included).

1. (10 min) One partner observes the hub and takes jottings. The other counts every *sighting* of a player character in a fixed area once per minute, writing down the name each time (sightings, not unique players).
2. (5 min) Count unique names. Compute sightings per unique name. Which players appear in almost every minute, and which appear once?
3. (5 min) Treat "minutes seen" as a stand-in for `h`. Compute the share of sightings belonging to the top 20% of names, and the corrected share using `1 / minutes seen`.
4. (5 min) Rewrite one jotting as a thick description. State in one sentence what you would need to know to make it thicker.

Expected output: a small table (names, minutes seen, raw share, corrected share), one thin and one thick description, and one sentence on what you could not see.

## Common misconceptions

- **"If everyone answers honestly, the average is right."** Honesty controls measurement error. Length bias is a sampling problem. The 21.28-hour average in section 2 comes from perfectly honest answers.
- **"More observation removes the bias."** More sessions shrink the random error around a biased estimate. They do not move it toward the truth. At `k = 672` you still meet hardcore players 40% of the time. Counting unique people or weighting by `1/h` is what removes the bias.
- **"Ethnography is just playing the game and writing a diary."** Playing is the access. The method is the systematic record (jottings, expanded notes, memos), the explicit account of your role, and the discipline of separating description from interpretation.
- **"Chat in a public channel can be quoted freely."** Visibility is not consent. Paraphrase, use pseudonyms, and treat character names as identifying.

## Check yourself

1. A server has 80% of players at 5 hours a week and 20% at 30 hours. What share of the people you meet in-game come from the 30-hour group? What is the mean weekly hours of the people you meet, compared with the true mean?
2. You interviewed 50 players you met in-game. Thirty said they play about 40 hours a week and twenty said about 5. Estimate the share of 40-hour players in the population.
3. A small guild's friendship network is a star. The leader is friends with four members, and those four know only the leader. What is the mean number of friends per member? What is the mean number of friends of a randomly chosen friend?
4. How many random one-hour observation moments do you need for a 90% chance of seeing a particular 4-hour-a-week player at least once?
5. A colleague reports "players in our Discord want harder raids, 70% agree." Name the sampling mechanism at work and one way to check the claim.

<details>
<summary>Answers</summary>

1. `p × h`: `0.8 × 5 = 4` and `0.2 × 30 = 6`, total 10. The 30-hour group is `6/10 = 60%` of encounters. Mean hours met `= (0.8 × 25 + 0.2 × 900) / 10 = (20 + 180) / 10 = 20` hours, against a true mean of 10.
2. Weight by `1/h`: `30/40 = 0.75` and `20/5 = 4`. The 40-hour share is `0.75 / 4.75 ≈ 15.8%`. Your sample said 60%.
3. Degrees are 4, 1, 1, 1, 1. Mean friends `= 8/5 = 1.6`. Mean friends of a friend `= Σ d² / Σ d = (16 + 4) / 8 = 2.5`. Four of the eight friendship ends point at the leader.
4. Solve `1 − (1 − 4/168)^k ≥ 0.9`. `k ≥ ln(0.1) / ln(0.97619) ≈ −2.3026 / −0.0241 ≈ 95.6`, so 96 moments.
5. Participation inequality. Discord messages are length-biased toward the most active posters, and the people who read raid discussion are raiders. Check with a sample reached per person, for example an in-game survey shown once to every account that logs in during a week, and compare the answers by play time.

</details>

## Lab / assignment hook

[Lab 13, field observation with a bias correction](../labs/lab13.md). You plan and run four hours of observation in a public space of an MMO, keep jottings and expanded notes, and correct your sighting counts with the week's model. The lab is the practice run for the course's field observation assessment (30%).

## Sources

- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "Alone Together? Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*. ACM. World of Warcraft, data from June 2005: virtual ethnography followed by a `/who` census every 5 to 15 minutes on five servers; 129,372 unique characters; mean play time 10.2 hours per character per week, with the authors' note that per-player time is higher because of alts.
- Taylor, T. L. (2006). *Play Between Worlds: Exploring Online Game Culture*. MIT Press. EverQuest; power gaming, gender, player-created culture. Biographical details (MIT Comparative Media Studies; *Raising the Stakes*, 2012; *Watch Me Play*, 2018) from Wikipedia, "T. L. Taylor" (accessed September 2026).
- Boellstorff, T. (2008; 2nd ed. 2015). *Coming of Age in Second Life: An Anthropologist Explores the Virtually Human*. Princeton University Press. Publisher's description: more than two years of fieldwork as the avatar Tom Bukowski. https://press.princeton.edu/books/paperback/9780691168340/coming-of-age-in-second-life
- Nardi, B. (2010). *My Life as a Night Elf Priest: An Anthropological Account of World of Warcraft*. University of Michigan Press.
- Boellstorff, T., Nardi, B., Pearce, C. & Taylor, T. L. (2012). *Ethnography and Virtual Worlds: A Handbook of Method*. Princeton University Press.
- Geertz, C. (1973). *The Interpretation of Cultures*. Basic Books. Thick description, a term Geertz took from Gilbert Ryle (Wikipedia, "Thick description", accessed September 2026).
- Warcraft Wiki, "Tap" (accessed September 2026). Classic tapping (first player and party only), the etiquette of inviting players who want the same monster, and tap-denial as griefing; patch history. https://warcraft.wiki.gg/wiki/Tap
- Feld, S. L. (1991). "Why Your Friends Have More Friends Than You Do." *American Journal of Sociology* 96(6), 1464-1477.
- Nielsen, J. (2006, October 9; updated 2022). "Participation Inequality: The 90-9-1 Rule for Social Features" (first published as "Participation Inequality: Encouraging More Users to Contribute"). Nielsen Norman Group. https://www.nngroup.com/articles/participation-inequality/
- Association of Internet Researchers, "Ethics" (accessed September 2026). *Internet Research: Ethical Guidelines 3.0* (2019), replacing the 2002 and 2012 guidance. https://aoir.org/ethics/
- The three-group server in section 2 is invented for teaching. Its 10-hour mean was chosen to match the scale of the 2005 WoW figure, not its distribution.

## Interactive spec: examples/w13-who-you-meet.html

**The one insight:** the population by head count and the population by encounter are different pictures, and the gap is set by the spread of play time. The student should see a group that is small on the left become dominant on the right as its hours rise, and then see the correction restore the left picture from the right.

**Layout.** Two linked panels side by side (stacked on narrow screens), each a single 100% horizontal stacked bar or a waffle of 100 squares.
- Left panel, "Who plays": shares `p_i`.
- Right panel, "Who you meet": shares `q_i = p_i h_i / Σ p_j h_j`.
- Three groups with fixed colours from the shared palette: Casual, Regular, Hardcore. Label each segment with its percentage to one decimal.
- Below the panels, a readout row: "True mean hours: X", "Mean hours of people you meet: Y", "Ratio: Y/X". Use `Y = Σ p h² / Σ p h`.

**Controls.**
- Three share sliders `p_casual`, `p_regular`, `p_hardcore` (0-100, step 1). Moving one rescales the other two proportionally so the sum stays 100. Keyboard: arrow keys step by 1.
- Three hours sliders `h_i` (1-80, step 1).
- Toggle "Correct with 1/h weights". When on, a third bar appears under the right panel showing `(q_i / h_i) / Σ (q_j / h_j)`, which must equal the left panel exactly (display both to one decimal).
- Second tab, "Will I see them?": slider `k` for observation sessions (1-700, step 1, log-scaled track). Plot `P(seen) = 1 − (1 − h/168)^k` for each group as three horizontal bars with percentages. Also plot the curve of `P(seen)` against `k` for the three groups, with a vertical line at the current `k`.
- Reset button restores the defaults.

**Defaults.** `p = (60, 30, 10)`, `h = (4, 12, 40)`, `k = 10`.

**Test values (must match to the shown precision).**
- Defaults: `q = (24.0%, 36.0%, 40.0%)`; true mean 10.00; mean met 21.28; ratio 2.13.
- `p = (80, 0, 20)`, `h = (5, any, 30)`: `q = (40.0%, 0.0%, 60.0%)`; true mean 10.00; mean met 20.00.
- All three `h` equal (e.g. 10): `q` equals `p` and the ratio is 1.00.
- `P(seen)` at `k = 10`: 4 h → 21.4%, 12 h → 52.3%, 40 h → 93.4%. At `k = 96`, 4 h → 90.1%.

**Numbers visible.** Every percentage and mean is printed next to its visual so students can copy them into the section 2 tables. No game art or logos. Groups are drawn as plain coloured shapes.
