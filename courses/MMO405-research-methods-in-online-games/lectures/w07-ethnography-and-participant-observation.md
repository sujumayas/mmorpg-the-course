# MMO405 · Week 07 — Ethnography and Participant Observation

**Why this matters:** Your thesis question may be about what players mean, owe each other or take for granted, and no log file holds those things. Ethnography is how you get them, and it produces numbers too. Every time you write "players were chatting most of the evening" you have measured something, and the rule you used to write it down decides whether the number is true.

**You will be able to:**
- Choose an observer role and a field site that fit a research question, and justify both in a methods section.
- Compute what continuous recording, instantaneous (scan) sampling and one-zero sampling each report for the same behaviour, and predict the one-zero bias factor `1 + T/b`.
- Design a recording plan that combines open field notes with a structured sampling rule, and say which claims each record can support.
- Critique a published ethnography of an online world for its role, its site, its recording rules and its ethics.

**Before class:** Boellstorff, Nardi, Pearce and Taylor, *Ethnography and Virtual Worlds: A Handbook of Method* (2012), chapter 3, "Ten Myths about Ethnography" (pp. 29-51), and chapter 5, "Participant Observation in Virtual Worlds" (pp. 65-91). Altmann, "Observational Study of Behavior: Sampling Methods" (1974), the sections on one-zero sampling and instantaneous and scan sampling. Skim Pearce, *Communities of Play* (2009), the chapters "Methodology" and "Being Artemesia".

**Prerequisites from earlier courses:** [MMO305 week 13, ethnography of online worlds](../../MMO305-social-systems-and-online-behaviour/lectures/w13-ethnography-of-online-worlds.md) (field notes, thick description, emic and etic, length-biased sampling, AoIR guidelines). [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) (the World of Warcraft `/who` census). [MMO308 week 2, DAU, MAU and stickiness](../../MMO308-live-operations-analytics-and-experimentation/lectures/w02-kpis-dau-mau-stickiness-arpdau.md) (touches versus play). [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (thematic analysis). [MMO405 week 6, interviews](w06-qualitative-methods-interviews.md) (recruiting, consent and coding).

**Interactive:** [examples/w07-recording-rules.html](../examples/w07-recording-rules.html). Keep it open during section 2.

---

## 1. What this week adds

In MMO305 you learned what ethnography is. You wrote jottings, expanded them into field notes and turned thin descriptions into thick ones. You also learned the trap of presence. The people you meet in-world are weighted by how long they play. This week you use ethnography as a research design, the way you would in a thesis. That raises four questions a methods section has to answer.

1. **Why ethnography?** Which part of your question needs you to be there?
2. **Who are you in the field?** What role do you take, and what does it change?
3. **What do you write down, and by what rule?** Open notes, structured samples, or both.
4. **Why should a reader believe you?** How your claims are warranted, and what you did about ethics.

Ethnography fits "how" and "what does it mean" questions. How does a raiding guild decide who sits out? What does "casual" mean on this server? These need a researcher who spends long periods among the people involved and learns their categories before imposing any.

Four studies give you a sense of the range. T. L. Taylor's *Play Between Worlds* (2006) studied EverQuest players, and her *Watch Me Play* (2018) followed game culture onto Twitch. Tom Boellstorff's *Coming of Age in Second Life* (2008) was built from more than two years inside one world. Bonnie Nardi's *My Life as a Night Elf Priest* (2010) came from her play in World of Warcraft guilds. Celia Pearce's *Communities of Play* (2009) followed a group of players whose game, Uru, closed. They called themselves refugees, moved into There.com and rebuilt a hybrid culture there. Pearce followed the group across worlds, and this is the model for a multi-sited study.

The four authors of the 2012 handbook are Boellstorff, Nardi, Pearce and Taylor, and they give a whole chapter to "Ten Myths about Ethnography". Read it with two opposite mistakes in mind. One treats ethnography as anecdote because it does not report a p-value. The other treats it as unstructured hanging out that needs no method. Neither is right. Ethnography has its own standards of evidence, and one of them is that you record systematically. That is where this week's worked example lives.

## 2. Worked example: the census that changed its clock

### The hook

From June 2005, a team at the Palo Alto Research Center ran software that typed World of Warcraft's `/who` command over and over. It recorded every character online on five servers, with each character's level, zone, guild and whether it was in a group. You met this census in MMO305 week 2. Here is a detail that is easy to skip. The census ran every 5 to 15 minutes, **depending on server load**. Busy servers were sampled less often than quiet ones.

That should worry you. The team compared servers and reported figures like the share of time characters spent grouped. If a busy server was checked every 15 minutes and a quiet one every 5, are the two numbers comparable? Would a slower clock make players look more social, or less?

The answer is that the clock did not matter for the averages, because of how each snapshot was recorded. A field observer using a different, very common recording rule would have got numbers that shift with the clock and with how players chop up their play. This section shows you why.

### The model

Watch one behaviour (call it B) for a session of length `L` minutes. B might be "in a group", "talking in guild chat" or "standing at the auction house". B happens in **bouts**, stretches of time with a start and an end. Three recording rules turn the session into a number.

```
Continuous recording:     p       = (total minutes in bouts) / L
Instantaneous (scan):     p_scan  = (sample points where B is on) / (number of sample points)
One-zero:                 p_10    = (blocks in which B happened at all) / (number of blocks)
```

- `L` is the session length.
- `T` is the sampling interval. Scan sampling checks at the instants `0, T, 2T, ...`. One-zero sampling cuts the session into blocks of length `T` and scores each block 1 if B happened at any moment inside it, 0 if not.
- `b` is the length of a bout and `n` the number of bouts.
- `p` is the true share of time in B. It is what a continuous record measures.

Jeanne Altmann's 1974 review of observational sampling set out these rules and several others. Her verdict on the first two is the heart of this example. Taken over many possible start times, a scan sample's expected value is exactly `p`, whatever `T` is. A larger `T` gives fewer points and a noisier estimate, but not a biased one. The census sampled instants, so a slower clock made each server's figure noisier. It did not push the figure up or down.

One-zero sampling is different. A bout of length `b` placed at a random point on a grid of blocks of width `T` touches, on average, `1 + b/T` blocks. If the bouts are separated by gaps of at least `T`, so that no two bouts share a block, the expected one-zero score is

```
E[p_10] = n × (1 + b/T) × T / L = n × (T + b) / L
E[p_10] / p = (T + b) / b = 1 + T/b
```

**The one-zero score overstates the time share by a factor of `1 + T/b`.** Short bouts and long blocks make it worse. Altmann's advice was blunt. One-zero scores estimate neither how long nor how often a behaviour happens, so do not use them for either.

### Numbers you can check

Take one character on one 120-minute evening. The character is grouped four times, each time for 6 minutes, at minutes 3-9, 31-37, 58-64 and 95-101. That is 24 minutes, so the true share is `p = 24/120 = 20%`.

This code applies each rule to that evening. It runs as shown with `.venv/bin/python`.

```python
# One focal character, one 120-minute evening. Each bout is (start, end) in minutes.
BOUTS = [(3, 9), (31, 37), (58, 64), (95, 101)]
L = 120

def continuous(bouts, L):
    return sum(end - start for start, end in bouts) / L

def scan(bouts, L, T, offset=0):
    points = range(offset, L, T)
    hits = sum(any(s <= t < e for s, e in bouts) for t in points)
    return hits / len(points)

def one_zero(bouts, L, T):
    blocks = [(b, b + T) for b in range(0, L, T)]
    hits = sum(any(s < b1 and e > b0 for s, e in bouts) for b0, b1 in blocks)
    return hits / len(blocks)

print(f"continuous       {continuous(BOUTS, L):.1%}")
for T in (5, 15):
    avg = sum(scan(BOUTS, L, T, o) for o in range(T)) / T
    print(f"T={T:2}  scan {scan(BOUTS, L, T):.1%}  scan averaged over start times {avg:.1%}"
          f"  one-zero {one_zero(BOUTS, L, T):.1%}")
```

```
continuous       20.0%
T= 5  scan 20.8%  scan averaged over start times 20.0%  one-zero 33.3%
T=15  scan 12.5%  scan averaged over start times 20.0%  one-zero 62.5%
```

Check the `T = 15` row by hand. The scan points are minutes 0, 15, 30, ..., 105. Only minute 60 falls inside a bout (58-64), so the scan reads 1 of 8, or 12.5%. That single evening's scan is low, but shift the start time through every minute from 0 to 14 and the average comes back to exactly 20%. The one-zero blocks are 0-15, 15-30, and so on. The bouts touch blocks 0-15, 30-45, 45-60, 60-75 and 90-105. The bout at 58-64 straddles a boundary and counts twice. Five blocks of 8 gives 62.5%, more than three times the truth.

Now use the formula to see how the bias depends on how the same 24 minutes are chopped. Every row has `p = 20%` and every scan estimate has expected value 20%.

| Bouts | Bout length `b` | One-zero, `T = 5` | One-zero, `T = 10` | One-zero, `T = 15` | Bias factor at `T = 15` |
|---|---|---|---|---|---|
| 1 | 24 min | 24.2% | 28.3% | 32.5% | 1.63 |
| 2 | 12 min | 28.3% | 36.7% | 45.0% | 2.25 |
| 4 | 6 min | 36.7% | 53.3% | 70.0% | 3.50 |

Check one cell. With four 6-minute bouts and `T = 10`, `E[p_10] = 4 × (10 + 6) / 120 = 64/120 = 53.3%`. The bias factor is `1 + 10/6 = 2.67`, and `20% × 2.67 = 53.3%`. The formula gives 70% for the 4-bout row at `T = 15`, and the actual evening above gave 62.5%. That is one draw, and the formula is the average over where the bouts fall on the grid.

Two lessons follow. A one-zero score climbs as the interval grows, so observers with different block lengths cannot compare numbers. Worse, the score depends on bout structure. A player who groups in four short bursts looks more than twice as "grouped" as a player who groups once for the same total time. If you compare casual players (short sessions, short groups) with raiders (long groups), a one-zero checklist will manufacture a difference that is not there, or hide one that is.

### A visual you can move

Open the interactive. The top panel is the evening as a timeline, with bouts drawn as bars. Scan points appear as ticks and one-zero blocks as shaded bands, and a hit is filled in. The page opens with the four bouts evenly spaced at minutes 3, 33, 63 and 93. At `T = 15` each of those bouts sits inside a single block, so this evening scores 4 of 8 blocks, 50%, below the formula's 70%. The formula is the average over where bouts fall against the block edges, and a bout that crosses an edge counts twice, as the 58-64 bout did above. Press "Lecture evening" to load the hand-placed bouts and see 62.5%. The lower panel plots the estimate against the interval `T` from 1 to 30 minutes. The flat line is the true `p`. The scan estimate wobbles around it, and the one-zero estimate climbs away from it. Drag the number-of-bouts slider from 1 to 6 while keeping total minutes fixed. The true line does not move and the scan average does not move, but the one-zero curve rises steeply. Then press "shuffle bouts" a few times and watch the single-evening scan jump while its long-run average stays on the line.

### Cross-game recognition

Rewrite each case as a recording rule with an interval `T`, and ask whether it measures time or touches.

**World of Warcraft census (2005-2006).** Each `/who` sweep is an instantaneous sample of every character online, with `T` between 5 and 15 minutes. The share of snapshots in which a character is grouped estimates its share of online time spent grouped, without bias at any `T`. The Tree House study of WoW guilds (Williams and colleagues, 2006) used the same kind of census over January 2006 and reported that 2.5% of the characters in its sampling frame were online at any one time. "At any one time" is the signature of an instantaneous measure.

**DAU and MAU (live operations, any era).** In MMO308 week 2 you saw that MAU counts touches and DAU measures play. In this lecture's terms, MAU is a one-zero score with a 30-day block, since a player counts once if they logged in at any moment in the window. DAU is a one-zero score with a 1-day block. Average concurrent players, as SteamCharts reports it for Steam games, is an instantaneous scan. So stickiness, `DAU/MAU`, is the ratio of two one-zero scores taken at different `T`. Its sensitivity to "tourists" who play in short bursts is the same `1 + T/b` effect you just computed. A player with one short session a month adds a full touch to MAU.

**Field primatology (Altmann's own context).** Altmann wrote for researchers watching animal groups, where "time spent grooming" is the classic target. Observers there had often used one-zero checklists because they are easy to fill in. Her paper showed they cannot estimate time or frequency, and it recommended combining methods. For example, a researcher can take instantaneous samples of nearest neighbours every 5 or 10 minutes during a longer focal watch and, alongside, record all occurrences of conspicuous events. That combined plan transfers directly to a raid night.

Three settings, one question. When someone reports "how much" of anything from observation, ask what the recording rule was and what `T` was. If it was one-zero, the number is a count of touched blocks. It is not a share of time.

### Eyes-open design judgment

One-zero sampling is not useless. It answers a different question, and you should choose each rule on purpose.

- **Use scans for time budgets.** "What share of a raid night is spent fighting, waiting or wiping?" needs instantaneous samples. Set `T` shorter than the typical bout if you also want to see bouts, and use a fixed schedule decided before you start.
- **Use all-occurrence recording for conspicuous, rare events.** Loot disputes, rage-quits, a guild leader's announcement. You cannot scan for these, because they will fall between your points. Record every one, with a timestamp.
- **Use one-zero only for "did it ever happen?"** It is a fine answer to "in how many raid nights did anyone mention the loot rules?" Report it that way and never convert it to time.
- **Keep open field notes running alongside.** Structured records tell you how much. Only thick description tells you what the behaviour meant. Altmann's own advice was to run several methods at once where the conditions allow, and an MMO session with a chat log often does.
- **Decide before you look.** If you choose the recording rule after seeing the evening, you will choose the one that tells your story.

### Check yourself (worked example)

1. A character talks in guild chat in 10 bouts of 1 minute each during a 100-minute session. What is the true share? What does one-zero sampling with 5-minute blocks report on average, assuming the bouts are far apart?
2. You scan every 20 minutes and a colleague scans every 2 minutes. Whose estimate of time-in-group is biased? Whose is more precise?
3. A study reports "raiders spent 80% of observed blocks in voice chat, casual players 55%." What do you need to know before you believe that raiders spend more time in voice chat?

<details>
<summary>Answers</summary>

1. `p = 10/100 = 10%`. `E[p_10] = 10 × (5 + 1) / 100 = 60%`, six times the truth, since `1 + 5/1 = 6`.
2. Neither is biased, since scan samples estimate `p` without bias at any interval. The 2-minute scan has ten times as many points, so it is more precise.
3. The recording rule and the block length. If it was one-zero, you also need the bout structure. Casual players with short, frequent chats could spend more time talking and still score lower, or the reverse. Ask for instantaneous samples or a continuous record.

</details>

## 3. Who you are in the field

In 1958 the sociologist Raymond Gold described four roles a field researcher can take. They are still the standard vocabulary.

- **Complete participant.** You are a full member and your research role is hidden.
- **Participant-as-observer.** You are a full member and people know you are also researching.
- **Observer-as-participant.** You are mainly observing, with limited and known participation, such as a short visit or an interview.
- **Complete observer.** You watch without taking part and without people being aware of you.

Online worlds change the costs of each role. An avatar makes full participation cheap. You can join a guild tonight, where joining a village would take months. It also makes hidden roles easy, because nobody sees your face or knows your job. That ease is a temptation, and section 5 explains why a hidden role needs a strong justification.

Most published ethnographies of virtual worlds sit in the participant-as-observer role. Boellstorff did his Second Life fieldwork as the avatar Tom Bukowski. Pearce's chapter "Being Artemesia" is about her own avatar and how being known as a researcher shaped her relationships with the Uru group. Ducheneaut and colleagues, before their census, spent hundreds of hours playing World of Warcraft and joined guilds of different sizes. They said this experience framed how they read their numbers.

Your role changes the data in three ways.

- **Reactivity.** People act differently when they know they are watched. Long fieldwork reduces this, because people get used to you.
- **Access.** Full members see officer channels and the argument after the wipe. Access comes through gatekeepers, like the guild leader or a moderator. Record what you told them.
- **Position.** If you are the main healer, you shape the raid you are studying. If you are an officer, members tell you different things than they tell each other. This is not contamination to be removed. It is part of the data, and you report it.

Reporting it is called **reflexivity**, an explicit account of how your position and choices shaped what you saw. Say how long you were in the field, which role you held, what you told whom, and where your own play might have changed events. Your **positionality**, where you stand in relation to the community, belongs in the same paragraph. A former member, a rival-faction player and a newcomer will each see different things.

## 4. From field site to claim

### Choosing and bounding the site

A field site is where your question happens, not where the game's servers are. For a raiding guild, that includes the raid instance, the guild's voice server, its Discord and its loot spreadsheet. Pearce's site was a group, not a world. When Uru closed she followed the players into There.com and other spaces, because the culture moved with them. This is a **multi-sited** design. You bound the site by the people and practices you study, and follow them across platforms.

Bounding matters because every claim you make is about the site. A year in one raiding guild supports claims about how that guild, and guilds like it, handle loot. It does not support claims about "WoW players". MMO305 week 13 showed you why the people you meet in-world are a length-biased sample. Say who you studied and let the reader decide how far it reaches.

### Sampling inside ethnography

Ethnographers do not draw random samples of people, but they do sample, deliberately. You choose which **events** to attend (raid nights, recruitment trials, the day after a patch), which **times** (weekday afternoons as well as prime time), and which **people** to follow closely. A **focal** observation follows one person for a set period, which is how the character in section 2 was recorded. Choosing people and events because they will test or extend an emerging idea is called **theoretical sampling**. If your notes suggest that loot disputes cluster after wipes, you go looking for nights with many wipes and nights with none.

### A recording plan

Put the lessons of section 2 into a plan you write before you enter the field.

| Record | Rule | Use it for | Example in a raid night |
|---|---|---|---|
| Jottings and expanded notes | Ad libitum, written up the same day | Meaning, sequence, context | What happened after the third wipe, and how people talked about it |
| Scan samples | Instantaneous, fixed `T` | Time budgets | Every 5 minutes, is the raid fighting, waiting, or wiping? |
| All-occurrence log | Every instance, timestamped | Rare, conspicuous events | Every loot roll dispute and every departure |
| Chat and combat logs | Continuous, automatic | Checking your notes | Who spoke, when, and whether your memory of the order is right |
| Analytic memos | Your interpretations, kept separate | Building the argument | "Disputes follow wipes, not boss kills. Check next week." |

Automatic logs are continuous but record only text and game events. Movement, silence and the tone of an in-joke are not in them. Your notes supply those.

### Analysis and warrant

Analysis runs alongside fieldwork, not after it. You code field notes the way UX201 week 12 and week 6 taught you to code interview transcripts, going back and forth between notes and emerging ideas.

A reader should believe an ethnographic claim when you can show the following.

- **Time and depth.** How long you were there and how many events of each kind you saw.
- **Triangulation.** The same pattern appears in your notes, in logs and in what people told you. Week 8 turns this into a formal design.
- **Negative cases.** You looked for events that contradict your claim and report what you found. A claim that "loot disputes always follow wipes" needs you to report the nights where they didn't.
- **Member checking.** You showed your interpretation to people in the community and recorded whether they recognised it. They can be wrong about themselves, so this is evidence, not a veto.
- **Transparency about structure.** Where you give a "how much" number, you name the recording rule, as section 2 requires.

## 5. Ethics in the field

MMO405 week 10 covers ethics review in detail. You need four points now, because they shape your role and your site before you start.

**Hidden roles need strong justification.** Deception, including a complete-participant role where people do not know you are researching, is generally permitted only when the research could not be done otherwise, the risks are minimal, and an ethics committee has approved it in advance. For a student project, assume an open role. Put a short note in your character profile or guild application saying you are a student researcher and how to contact you.

**Visibility is not consent.** The Association of Internet Researchers (AoIR) guidelines, version 3.0 (2019), treat privacy as a matter of what people expect in a context, not of whether text is technically visible. A city hub is public. A guild's voice channel is not, even if anyone who joins the guild can hear it. Consent scales with intimacy. Interviews always need consent.

**Names are identifiers.** Character names, guild names and server names can be searched. Use pseudonyms for all three in anything you publish, and paraphrase chat rather than quoting it word for word, because an exact quote can be found.

**Terms of service and automation.** Bots and add-ons that log other players can breach a game's terms of service, and some games ban them. The Tree House team noted that Blizzard declined to assist their project. Your ethics application should say what software you will run and whether the game permits it.

## In-class activity (25 minutes)

Work in groups of three. The instructor provides a 20-minute screen recording of a public city hub in a free-to-play MMO, made on a course account. Character names in it are blurred, and the chat log is included with names replaced by codes.

1. (3 min) Before watching, choose one behaviour to measure (for example "standing still near the bank", "emoting" or "in a visible group"). Agree on a written definition of when a bout starts and ends.
2. (10 min) Each person applies a different rule to the same focal character, chosen by the instructor. One records continuously with start and end times. One scans every 60 seconds. One does one-zero scoring with 2-minute blocks.
3. (5 min) Compute each person's estimate. Compute the bias factor `1 + T/b` from the continuous record's average bout length and check whether it predicts the gap between the one-zero and continuous estimates.
4. (7 min) Together, write one thick description of the most interesting event in the clip. State which of your three records it came from, and what none of them captured.

Expected output: a three-row table of estimates, the predicted and observed bias factor, and one paragraph of thick description with a sentence on what was missing.

## Common misconceptions

- **"Ethnography is anecdote, so it needs no method."** It has explicit methods for role, site, recording and analysis, and the handbook gives chapters to each of them. When an ethnography reports how much, the recording rule decides whether the number means anything.
- **"A bigger sampling interval biases scan samples."** It makes them noisier. Their expected value stays at the true share. It is one-zero scores that drift with `T`.
- **"Checking a box every 15 minutes is the same as a scan."** Only if the box asks "is it happening right now?" If it asks "did it happen in the last 15 minutes?", it is one-zero, and it overstates time by `1 + T/b`.
- **"Being hidden gives more natural data, so it is better."** It may reduce reactivity, but it costs consent and needs strong justification and approval. Long, open fieldwork also reduces reactivity, because people get used to you.

## Check yourself

1. A focal player is in voice chat in 3 bouts of 20 minutes in a 180-minute raid night. Compute `p`, the expected one-zero score with 30-minute blocks (assume no two bouts share a block), and the bias factor.
2. A classmate proposes to study "how new players learn guild norms" by joining three guilds under a hidden role for a month. Name Gold's role for this plan. Give two changes that would make it acceptable for a student project.
3. You want to know what share of a raid night is spent waiting. You also want to understand why a raid leader's call to "take five" sometimes starts a dispute. Write the two lines of a recording plan that cover these, naming the rule for each.
4. Pearce's study followed the Uru group into There.com. Why would a study bounded by one world have missed her main finding?
5. A published study says its authors played the game for hundreds of hours before collecting data. Give one way this helps the analysis and one way it could bias it.

<details>
<summary>Answers</summary>

1. `p = 60/180 = 33.3%`. `E[p_10] = 3 × (30 + 20) / 180 = 150/180 = 83.3%`. Bias factor `1 + 30/20 = 2.5`, and `33.3% × 2.5 = 83.3%`.
2. Complete participant. Make the role open (participant-as-observer), with a profile note and a message to each guild leader, and get ethics approval before starting. Use pseudonyms for players and guilds, and paraphrase chat.
3. Waiting share, instantaneous scan every 2 to 5 minutes with a fixed definition of "waiting". Disputes after "take five", all-occurrence log of every dispute with a timestamp, plus same-day expanded notes on what preceded and followed each one.
4. Her finding was about a culture that moved and was rebuilt, as refugees, inside a new world. A single-world study would see either the old community disappearing or a new group arriving, but not the continuity between them.
5. It helps the authors know what the numbers mean in play, such as why characters in cities are often AFK, and which questions to ask. It can bias them toward the kinds of play and guilds they experienced, and toward reading data through their own habits.

</details>

## Lab / assignment hook

[Lab 07, recording rules and a field observation](../labs/lab07.md). You implement the three recording rules, run them on a supplied focal-observation log, and check the `1 + T/b` prediction. Then you conduct a 60-minute open-role observation of a public space in an MMO with a written recording plan, and submit field notes, a scan-sample table and a reflexive methods paragraph. This feeds the methods section of your research proposal.

## Sources

- Boellstorff, T., Nardi, B., Pearce, C. & Taylor, T. L. (2012). *Ethnography and Virtual Worlds: A Handbook of Method*. Princeton University Press. Chapter 3, "Ten Myths about Ethnography" (pp. 29-51); chapter 5, "Participant Observation in Virtual Worlds" (pp. 65-91); chapter 8, "Ethics" (pp. 129-150); chapter 9, "Human Subjects Clearance and Institutional Review Boards" (pp. 151-158); chapter 10, "Data Analysis" (pp. 159-181). Chapter titles and pages from the De Gruyter listing (DOI prefix 10.1515/9781400845286). A second edition appeared in 2024.
- Altmann, J. (1974). "Observational Study of Behavior: Sampling Methods." *Behaviour* 49(3-4), 227-266. https://doi.org/10.1163/156853974X00534. The catalogue of sampling methods, the bias of one-zero sampling, and the recommendation to combine instantaneous samples during focal watches with all-occurrence records of conspicuous behaviour.
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2007). "The Life and Death of Online Gaming Communities: A Look at Guilds in World of Warcraft." *Proceedings of CHI 2007*, 839-848. https://doi.org/10.1145/1240624.1240750. World of Warcraft, data from June 2005: `/who` census of five servers every 5 to 15 minutes depending on server load; the authors' prior play and guild membership since the November 2004 launch.
- Williams, D., Ducheneaut, N., Xiong, L., Zhang, Y., Yee, N. & Nickell, E. (2006). "From Tree House to Barracks: The Social Life of Guilds in World of Warcraft." *Games and Culture* 1(4), 338-361. https://doi.org/10.1177/1555412006292616. Census in January 2006; 2.5% of sampled characters online at any one time; Blizzard declined to assist.
- Gold, R. L. (1958). "Roles in Sociological Field Observations." *Social Forces* 36(3), 217-223. https://doi.org/10.2307/2573808. The four field roles.
- Pearce, C. (2009). *Communities of Play: Emergent Cultures in Multiplayer Games and Virtual Worlds*. MIT Press. https://doi.org/10.7551/mitpress/8039.001.0001. The Uru Diaspora, its move to There.com, and the chapters "Methodology" and "Being Artemesia".
- Taylor, T. L. (2006). *Play Between Worlds*. MIT Press. Taylor, T. L. (2018). *Watch Me Play: Twitch and the Rise of Game Live Streaming*. Princeton University Press.
- Boellstorff, T. (2008). *Coming of Age in Second Life*. Princeton University Press. Fieldwork as the avatar Tom Bukowski (publisher's description).
- Nardi, B. (2010). *My Life as a Night Elf Priest: An Anthropological Account of World of Warcraft*. University of Michigan Press. https://doi.org/10.3998/toi.8008655.0001.001.
- franzke, a. s., Bechmann, A., Zimmer, M., Ess, C. & the Association of Internet Researchers (2020). *Internet Research: Ethical Guidelines 3.0*. Approved by the AoIR membership on 6 October 2019. https://aoir.org/reports/ethics3.pdf

## Interactive spec: examples/w07-recording-rules.html

**The one insight:** for the same evening, a scan sample's long-run average sits on the true time share at every interval, while a one-zero score climbs above it by `1 + T/b`, and climbs faster when the same minutes are chopped into more, shorter bouts.

**Layout.** Two linked panels, stacked (timeline on top) at all widths. At 1280px a readout column sits to the right of both.

- **Top panel, the evening.** x-axis minutes 0 to `L`. Bouts drawn as solid bars on a single track. Below the track, scan points as short ticks at `offset, offset + T, ...`; a tick is filled when it falls inside a bout (`s ≤ t < e`) and hollow otherwise. Behind the track, one-zero blocks `[kT, (k+1)T)` as alternating light bands; a band is tinted when any bout overlaps it (`s < b1` and `e > b0`). A mode toggle shows scan ticks, one-zero bands, or both.
- **Bottom panel, estimate versus interval.** x-axis `T` from 1 to 30 minutes (integer steps). y-axis 0% to 100%. Three series: true `p` (flat line), scan averaged over all integer offsets `0..T−1` (line with small markers), one-zero for the current evening (line), and a dashed curve for the formula `min(1, n(T + b)/L)`. A vertical marker at the current `T`.

**Controls** (keyboard accessible, each with a visible numeric readout):

- Session length `L`: 60 to 240 minutes, step 30, default 120.
- Number of bouts `n`: 1 to 8, default 4.
- Total minutes in bouts: 5 to 60, step 1, default 24. Bout length `b = total / n` (shown to one decimal; bouts may have fractional length).
- Interval `T`: 1 to 30, step 1, default 15.
- Scan offset: 0 to `T − 1`, step 1, default 0.
- "Even spacing" (default) places bout `i` (0-based) starting at `round(i × L / n + 3)` minutes, capped so the bout ends by `L`. With defaults this gives starts 3, 33, 63, 93 (not the lecture's hand-placed evening). At `T = 15` no bout crosses a block edge, so the default evening scores `p_10` = 4/8 = 50.0% against the formula's 70.0%. Show a note whenever `p_10` differs from the formula, saying that the formula averages over bout positions relative to the block edges.
- "Lecture evening" preset sets `L = 120`, bouts at exactly 3-9, 31-37, 58-64, 95-101.
- "Shuffle bouts" places `n` bouts at random non-overlapping positions (seeded PRNG; display the seed).

**Formulas.**

```
p          = Σ (e_i − s_i) / L
p_scan(o)  = #{t in {o, o+T, ..., < L} : ∃i s_i ≤ t < e_i} / #points
scan_avg   = mean over o = 0..T−1 of p_scan(o)
p_10       = #{k : ∃i s_i < (k+1)T and e_i > kT, kT < L} / ceil(L / T)
formula    = min(1, n × (T + b) / L)      (valid when gaps between bouts ≥ T)
bias       = p_10 / p ; formula bias = 1 + T/b
```

The last block may be shorter than `T` when `L` is not a multiple of `T`; count it as a block.

**Readouts:** `p`, `p_scan` at the current offset, `scan_avg`, `p_10`, formula value, observed bias `p_10/p` and formula bias `1 + T/b`, each to one decimal place (percent) or two decimals (factors). One sentence: "One-zero overstates time by ×N.NN at this interval."

**Test values** (lecture evening, `L = 120`):

| `T` | offset | `p_scan` | `scan_avg` | `p_10` |
|---|---|---|---|---|
| 5 | 0 | 20.8% | 20.0% | 33.3% |
| 15 | 0 | 12.5% | 20.0% | 62.5% |

Formula (4 bouts of 6, `L = 120`): `T = 5` 36.7%, `T = 10` 53.3%, `T = 15` 70.0%. One bout of 24: `T = 15` 32.5%. Two bouts of 12: `T = 15` 45.0%.

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. Scan hits and one-zero hits must differ by shape as well as colour (filled tick versus tinted band with a hatch). Respect `prefers-reduced-motion` (shuffle redraws without animation). Provide a text summary for screen readers giving `p`, `scan_avg`, `p_10` and the bias factor. No game art or logos; the timeline is abstract.
