# MMO405 · Week 06 — Qualitative Methods: Interviews

**Why this matters:** Telemetry shows that a player left their guild on a Tuesday. Only the player can tell you it was because the raid leader mocked their gear in voice chat. Interviews are how you get reasons, meanings and the vocabulary players use for them. But an interview study is only as trustworthy as the way you turn talk into codes, and the standard agreement statistic can call two coders who never agreed on a single case "90% in agreement."

**You will be able to:**
- Design a semi-structured interview study of an online game: a purposive sample, a recruitment route that names its bias, an interview guide built from the research question, and a mode (voice, text or video) chosen for the question.
- Compute percent agreement, Cohen's kappa, positive and negative specific agreement and PABAK from a two-coder table, and predict how kappa changes with a code's prevalence.
- Write codebook entries that two coders can apply, and decide whether a study should report inter-rater reliability at all.
- Plan consent, pseudonymization and distress procedures for interviews with players, including character names and minors.

**Before class:** McDonald, Schoenebeck and Forte (2019), "Reliability and Inter-rater Reliability in Qualitative Research: Norms and Guidelines for CSCW and HCI Practice", *Proceedings of the ACM on Human-Computer Interaction* 3(CSCW), read the introduction, the findings on local norms and the guidelines. Feinstein and Cicchetti (1990), "High Agreement but Low Kappa: I. The Problems of Two Paradoxes", *Journal of Clinical Epidemiology* 43(6), 543-549 (seven pages). Boellstorff, Nardi, Pearce and Taylor, *Ethnography and Virtual Worlds* (2012), chapter 6, "Interviews and Virtual Worlds Research" (pp. 92-112), and skim the chapter "Data Analysis" (pp. 159-181).

**Prerequisites from earlier courses:** [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (running a semi-structured interview, how many interviews, saturation, and Braun and Clarke's six phases; this week does not repeat them). [GS101 week 14, games and representation](../../GS101-history-and-critical-study-of-games/lectures/w14-games-and-representation.md) (Cohen's kappa defined and computed on a content-analysis codebook). [MMO305 week 9, toxicity research](../../MMO305-social-systems-and-online-behaviour/lectures/w09-toxicity-research-and-interventions.md) (Kou's player-centred taxonomy of toxic behavior in League of Legends). [MMO305 week 13, ethnography of online worlds](../../MMO305-social-systems-and-online-behaviour/lectures/w13-ethnography-of-online-worlds.md) (field ethics and pseudonyms). This course: [week 7, ethnography](w07-ethnography-and-participant-observation.md) and [week 8, mixed methods](w08-mixed-methods.md) (choosing interviewees from quantitative results).

**Interactive:** [examples/w06-kappa-prevalence.html](../examples/w06-kappa-prevalence.html). Keep it open during section 2.

---

## 1. The research interview

UX201 week 12 taught interviews as a UX tool. You ran them to find usability problems, stopped when new sessions stopped producing new problems, and reported themes to a design team. A research interview uses the same skills for a different goal. You want an account of how some group of players understands part of their world, one that other researchers can check and build on. Three things change.

**The question drives everything.** An interpretive research question (week 1) asks what something means to people or how they make sense of it: "How do raid leaders in a progression guild decide whom to bench?" The interview guide, the sample and the analysis all follow from that sentence. If the question is really about prevalence ("How many raid leaders bench by gear score?"), you need a survey or telemetry, not interviews.

**The sample is chosen on purpose.** Interview samples are small, and they aren't random. A **purposive sample** is chosen because each participant can speak to the question. Common strategies:

- **Maximum variation**: pick people who differ on the dimensions you think matter, such as guild size, role and tenure, so a theme that appears across all of them is not an artifact of one kind of player.
- **Criterion sampling**: everyone meets a condition, such as "has led at least ten raids in the current expansion".
- **Snowball sampling**: each participant introduces the next. It reaches closed groups, and it keeps you inside one friendship network.
- **Connecting from quantitative data**: choose interviewees from survey or log results, including contrast cases. Week 8 covers this in detail.

**Recruitment has a bias, and you must name it.** In online games the easy route is through gatekeepers, such as a guild leader or a Discord moderator who posts your call. That gets you people the gatekeeper likes and people who read announcements. MMO305 week 13 showed with numbers that the players you meet in the field are not the players who play. The same holds for the players who answer your recruitment post. Write down the route, estimate who it misses, and add a second route aimed at them, such as an in-game message to players who recently left guilds.

### Building an interview guide

Don't ask your research question. Ask for the experiences that will let you answer it. A useful guide has three layers:

1. **Topics**, taken from the research question and from what you already know (the literature, your fieldwork from week 7).
2. **Main questions**, one or two per topic, open and about specific episodes: "Tell me about the last time you had to bench someone."
3. **Probes**, prepared follow-ups: "What did you say to them?", "What did you weigh?", "Was that typical?"

Put easy, concrete questions first and sensitive ones in the middle, once you have rapport. End with "Is there anything I should have asked?", which often produces the best material of the session.

Players use dense jargon (DPS check, carry, parse, bench, loot council). Ask what the terms mean even when you know. The definitions players give are data. Two raid leaders who both say "we bench on performance" may mean logs, attendance or attitude.

Online games also add the **player and character split**. One person may have three characters in two guilds, with a different reputation on each. Decide in advance whether your unit is the person or the character, and ask accordingly.

### Choosing a mode

| Mode | Gains | Costs | Fits when |
|---|---|---|---|
| Voice call (Discord or similar) | Tone, pace, easy probing; players are used to it | Needs recording consent and transcription | Most research interviews |
| Text chat (in-game or messaging) | Instant transcript; comfortable for some players; supports anonymity | Short answers; hard to probe; attention split with play | Sensitive topics, participants who avoid voice, non-native speakers who prefer to read |
| Video call | Facial expression; can share screen and replay a session | Least anonymous; some players refuse | Walking through a replay or a UI |
| Inside the game world | Context, and the participant can show you places and objects | Interruptions; other players nearby; logs may be visible to the operator | Questions about space, place or a specific activity |

Choosing a mode is a method decision, so report it. Text interviews in particular produce shorter, more edited answers, and that changes what you can claim.

## 2. Worked example: 80% agreement, and what it hides

### The hook

In the early 2010s, League of Legends ran the **Tribunal**. Reported players were put "on trial": the system bundled up to five reported matches into a case, with chat logs and scoreboards, stripped names, and showed it to community volunteers who voted to punish or pardon. Majority vote decided. By Riot's figures, reviewers cast more than 47 million votes in the Tribunal's first year.

At the Game Developers Conference in 2013, Riot's Jeffrey Lin reported that the Tribunal's verdicts matched Riot's in-house team about 80% of the time, and that the in-house team was stricter. That sounds strong. Four out of five cases got the same verdict from volunteers and professionals.

Whether 80% is strong depends on a number the talk didn't give: how often cases deserved punishment. If most reported players really were guilty, two judges who punished almost everyone would agree most of the time without looking at the evidence. The same problem appears every time you and a colleague code interview transcripts for a code that is rare.

### The model

GS101 week 14 defined **Cohen's kappa**. Here is the version for one yes-or-no code applied by two coders, A and B, to the same `n` items (cases, excerpts, transcripts). Put the results in a 2 × 2 table:

| | B: yes | B: no |
|---|---|---|
| **A: yes** | `a` | `b` |
| **A: no** | `c` | `d` |

- **Observed agreement**: `p_o = (a + d) / n`.
- **Each coder's "yes" rate**: `p_A = (a + b) / n`, `p_B = (a + c) / n`.
- **Chance agreement**, the agreement expected if each coder said yes at their own rate without looking: `p_e = p_A × p_B + (1 − p_A) × (1 − p_B)`.
- **Kappa**: `κ = (p_o − p_e) / (1 − p_e)`. It is the share of the possible improvement over chance that the coders achieved. 1 is perfect, 0 is chance, and negative is worse than chance.

Two more numbers split agreement by category, following Cicchetti and Feinstein's companion paper:

- **Positive specific agreement**: `p_pos = 2a / (2a + b + c)`. Of the times either coder said yes, how often did both?
- **Negative specific agreement**: `p_neg = 2d / (2d + b + c)`. The same for no.

The key relation: `p_e` depends on the coders' yes rates. When a code is rare, both coders say no most of the time, `p_e` is close to 1, and even high observed agreement leaves little room above chance.

### Numbers you can check

First the Tribunal. Keep `p_o = 0.80` and try splits the talk might have hidden. Staff are the stricter judge, so their punish rate is at least the Tribunal's.

| Staff punish rate | Tribunal punish rate | `p_e` | κ |
|---|---|---|---|
| 50% | 50% | .50 | .60 |
| 70% | 60% | .54 | .57 |
| 80% | 80% | .68 | .38 |
| 90% | 80% | .74 | .23 |

The same 80% ranges from "moderate" to "barely above chance" depending on a figure nobody reported. Check the last row. With 100 cases, staff punish 90 and the Tribunal 80, and they agree on 80. The only table that fits is `a = 75, b = 15, c = 5, d = 5`. Then `p_e = .9 × .8 + .1 × .2 = .74` and `κ = (.80 − .74) / (1 − .74) = .23`.

Now an interview study. You and a partner code 100 excerpts from interviews with former guild members, each for one code at a time. You agree on 90 of the 100 every time, and your 10 disagreements always split 5 and 5. Only the code's prevalence changes, meaning the share of excerpts each of you marks "yes".

| Prevalence (each coder) | `p_o` | `p_e` | κ | `p_pos` | `p_neg` |
|---|---|---|---|---|---|
| 50% ("talks about raid schedule") | .90 | .500 | +.80 | .90 | .90 |
| 30% | .90 | .580 | +.76 | .83 | .93 |
| 20% | .90 | .680 | +.69 | .75 | .94 |
| 10% | .90 | .820 | +.44 | .50 | .94 |
| 5% ("describes harassment by an officer") | .90 | .905 | −.05 | .00 | .95 |

Look at the last row. You agree on 90% of excerpts. Kappa is negative. And `p_pos = 0`: of the 10 excerpts where either of you coded harassment, you never agreed on a single one. The 90% came entirely from agreeing that ordinary excerpts were not harassment. For a study whose findings depend on the harassment code, that is a total failure hiding behind a good-looking headline number.

The table comes from this code, which prints it exactly:

```python
def kappa_2x2(a, b, c, d):
    """a: both yes, b: A yes B no, c: A no B yes, d: both no (shares or counts)."""
    n = a + b + c + d
    po = (a + d) / n
    pa, pb = (a + b) / n, (a + c) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return po, pe, (po - pe) / (1 - pe)

def specific(a, b, c, d):
    return 2 * a / (2 * a + b + c), 2 * d / (2 * d + b + c)

print("prevalence  p_o   p_e    kappa  p_pos  p_neg")
for q in (50, 30, 20, 10, 5):          # % of excerpts each coder marks "present"
    a, b, c = q - 5, 5, 5              # 100 excerpts, 10 disagreements split evenly
    d = 100 - a - b - c
    po, pe, k = kappa_2x2(a, b, c, d)
    pp, pn = specific(a, b, c, d)
    print(f"{q:>9}%  {po:.2f}  {pe:.3f}  {k:+.2f}  {pp:.2f}   {pn:.2f}")
```

```
prevalence  p_o   p_e    kappa  p_pos  p_neg
       50%  0.90  0.500  +0.80  0.90   0.90
       30%  0.90  0.580  +0.76  0.83   0.93
       20%  0.90  0.680  +0.69  0.75   0.94
       10%  0.90  0.820  +0.44  0.50   0.94
        5%  0.90  0.905  -0.05  0.00   0.95
```

This is the first of Feinstein and Cicchetti's two paradoxes: high agreement, low kappa, when prevalence is far from 50%. Kappa is doing its job. It is telling you that agreement on the rare category is poor. What misleads is reporting `p_o` alone, or reporting kappa without the table.

### A visual you can move

Open the interactive. The left panel shows percent agreement as a bar. It stays at 90% the whole time. The right panel plots kappa against prevalence, with a marker at the current setting, and shows the 2 × 2 table as a grid of 100 squares colored by cell. Drag the prevalence slider from 50% down to 5%. The bar doesn't move. The kappa marker slides down the curve and crosses zero, and the "both yes" squares in the grid disappear one by one until none are left. Then turn on "show PABAK". The **prevalence-adjusted bias-adjusted kappa**, `PABAK = 2 × p_o − 1`, stays at .80 at every prevalence. It removes the paradox by ignoring prevalence, and with it the warning. Finally use the "coder bias" slider to give coder A a higher yes rate than B. Kappa drops further. That is the second paradox, which involves unequal marginals, and it is what the Tribunal rows with different punish rates show.

### Cross-game recognition

**The Tribunal and Riot's staff (League of Legends, era up to the 2013 GDC talk).** Two judges, one binary code (punish or pardon), a prevalence well above 50% (the in-house team punished more often than the community), and a headline agreement of 80%. In our form, `p_o = .80`, and κ between about .23 and .60 depending on the unreported split.

**A toxicity classifier (League of Legends, Tribunal data crawled in 2013).** Blackburn and Kwak trained a model on 1.46 million Tribunal cases to predict the crowd's verdict and reported that it separated guilty from innocent about 80% of the time. The classifier and the crowd are two coders. Their "accuracy" is `p_o`. Whether it is impressive depends on how often cases were punished, exactly as with the human judges. In automatic moderation this is often called the accuracy paradox: a filter that flags nothing is 95% accurate on chat where 5% of messages are toxic.

**Interview coding in a guild study (your project).** Two coders, one code, 100 excerpts. The rare, important codes (harassment, real-money trading, account sharing) are exactly the ones where `p_o` is least informative.

Three contexts, one formula. Whenever someone reports agreement or accuracy on a yes-or-no judgment, ask for the prevalence and the full 2 × 2 table.

### Eyes-open design judgment

- **Report the table, not only the coefficient.** Give `a`, `b`, `c`, `d` for each important code, or at least `p_pos` and `p_neg`. A reader can compute everything else.
- **Compute agreement per code.** A single kappa averaged over a codebook hides the rare codes that fail. McDonald and colleagues recommend being specific about what was compared and at what level.
- **Don't switch to PABAK to make the number look better.** PABAK answers a different question. Use it alongside kappa if you want, and explain why.
- **Fix rare-code disagreement with the codebook.** When `p_pos` is low, the definition is usually the problem. Sharpen the "when to use" and "when not to use" rules, add boundary examples, and recode (section 3).
- **Sample for the rare code on purpose.** If harassment appears in 5% of excerpts, a reliability check on 100 random excerpts contains about 5 positive cases, too few to estimate anything. Build the check set so that it contains enough candidate excerpts for each code you will report.

### Check yourself (worked example)

1. Two coders code 200 excerpts for "mentions leaving because of schedule." Table: `a = 30, b = 10, c = 6, d = 154`. Compute `p_o`, `p_e`, κ, `p_pos` and `p_neg`.
2. A paper reports that its moderators agreed on 94% of 500 chat reports and says nothing else. What is the least extra information you would ask for, and why?

<details>
<summary>Answers</summary>

1. `p_o = (30 + 154) / 200 = .92`. `p_A = 40/200 = .20`, `p_B = 36/200 = .18`. `p_e = .20 × .18 + .80 × .82 = .036 + .656 = .692`. `κ = (.92 − .692) / (1 − .692) = .228 / .308 = .74`. `p_pos = 60 / (60 + 16) = .79`. `p_neg = 308 / (308 + 16) = .95`.
2. The full 2 × 2 table, or at least each moderator's rate of calling a report actionable. With a prevalence far from 50%, 94% agreement is compatible with a kappa anywhere from high to near zero.

</details>

## 3. From transcript to codebook

UX201 week 12 walked through Braun and Clarke's six phases. For a research study with more than one analyst, the step that decides quality is the **codebook**, the written definition of every code. MacQueen and colleagues proposed a structure for team codebooks that is still the standard starting point. Each entry has a code name, a brief definition, a full definition, when to use the code, when not to use it, and an example. Here is one for a guild-leaving study:

| Field | Entry |
|---|---|
| Code | OFFICER_HARASSMENT |
| Brief definition | Participant describes being targeted by a guild officer's hostile behavior. |
| Full definition | Repeated or severe hostile acts (insults, public mockery, threats, exclusion from events) by someone with a guild rank above member, directed at the participant. |
| When to use | The participant attributes the acts to a ranked officer, even if they don't use the word harassment. |
| When not to use | Criticism of performance delivered privately and without insult ("your parses are low, can you fix your rotation?"). Hostility from non-officers (use MEMBER_CONFLICT). |
| Example | "Every raid he'd call out my gear in voice, in front of everyone, and then laugh." |

The "when not to use" line does most of the work. Rare-code disagreements are almost always boundary cases, and each disagreement you discuss should end with a new line in one of the two "when" fields.

A workable team process:

1. Two coders read the same three or four transcripts and draft codes separately.
2. Merge the drafts into a first codebook.
3. Both code a **reliability set** independently. Choose it so every code you plan to report has enough positive candidates.
4. Compute per-code tables, kappa, `p_pos` and `p_neg`.
5. Discuss every disagreement. Revise definitions. Recode the set.
6. When agreement is adequate for your purpose, split the remaining transcripts between coders, and double-code a sample throughout to catch drift.

What counts as adequate? You'll see thresholds quoted, such as κ above .60 or above .80. Treat them as conventions, not laws. A code whose counts appear in your findings needs better agreement than a code that only helped you find a theme.

### When not to compute inter-rater reliability

Some qualitative traditions reject the whole exercise. Braun and Clarke, whose 2006 paper defined thematic analysis for psychology, argued in 2019 that their **reflexive** version treats the researcher's interpretation as the analytic resource. On that view, coding is not a measurement that two people should reproduce, and agreement statistics answer a question the method doesn't ask. McDonald, Schoenebeck and Forte found that in a representative sample of CSCW and HCI papers from 2016 to 2018, inter-rater reliability appeared in only about 1 in 9 qualitative papers. They argue this is often appropriate, and give guidelines for when it is.

A practical rule that follows their guidelines:

- **Compute and report IRR** when a team applies a fixed codebook, when you report counts or compare groups by code frequency, or when coding feeds a quantitative analysis (as in week 8's joint displays).
- **Don't compute IRR** when one researcher does an interpretive analysis and the claims are about meaning. Show rigor differently: an audit trail of how codes became themes, the researcher's position (week 7), rich quotes, and negative cases that didn't fit.
- **Either way, say which approach you took and why.** Reviewers in game studies come from both traditions (week 12).

### Reporting interview findings

- Describe the sample in a table: pseudonym, role, guild size, tenure, mode of interview. No real character names.
- Count participants, not mentions, as UX201 taught, and don't turn counts from 15 interviews into population percentages (week 8).
- Use short quotes as evidence, each tagged with a pseudonym, and include at least one quote that complicates each theme.
- State what the sample cannot speak for, based on your recruitment route.

## 4. Ethics of interviewing players

Interviews are the method where you meet participants most directly. The duties below are the general ones for human-participants research. Your institution's ethics review sets the exact rules (week 10), and it must approve the study before you recruit anyone.

**Informed consent.** Before the interview, the participant receives and agrees to a plain-language statement of what the study is about, what you will ask, how long it takes, whether and how you will record, how you will store and use the data, and how they can withdraw. Say until when they can withdraw their data, since once transcripts are anonymized and analyzed, removal may no longer be possible. Recording needs explicit consent, separate from consent to the interview. For an online interview, record consent in a form the participant can keep, such as a signed form or a recorded spoken agreement at the start.

**Identifiability.** Character names, guild names and server names are identifying. Players search them, and many games have public armory or profile pages that link a character to its history. A quote with a distinctive phrase from a public forum can be found with a search engine. So:

- Pseudonymize people, characters and guilds. Give each participant one pseudonym for the person and don't report their character names at all.
- Change or remove details that identify a small community, such as the server name when a guild is famous on it.
- Paraphrase quotes that come from public sources rather than quoting them verbatim, unless the person has agreed to be named. MMO305 week 13 and MMO402 week 12 cover AoIR guidance on this.
- Store recordings encrypted, keep the key linking pseudonyms to real identities separate, and delete recordings on the schedule your approval states. Voice recordings are personal data under laws such as the EU's GDPR.

**Minors.** Many online game players are under 18. Expect your ethics board to require consent from a parent or guardian and the minor's own agreement (assent), and to scrutinize online recruitment that could reach minors. The simplest student design screens for age and interviews adults only, and says so in the limitations.

**Sensitive topics.** Interviews about harassment, toxicity or leaving a community can bring back distressing experiences. Plan a **distress protocol**: remind participants they can skip any question or stop at any time, watch for signs of distress, pause and offer to stop, and have support resources ready to share. Don't probe for detail the research question doesn't need.

**Your own safety.** Researchers who study toxic communities can become targets. Use a research account, not your personal one. Don't reveal your main character. Agree with your supervisor what to do if you receive threats.

## In-class activity (25 minutes)

Pairs. You receive a one-page sheet of 40 short excerpts from invented interviews with former guild members, and a two-code codebook: SCHEDULE_CONFLICT and OFFICER_HARASSMENT. The harassment code has a brief definition only.

1. (8 min) Code all 40 excerpts for both codes independently. Don't confer.
2. (5 min) Build your 2 × 2 table for each code. Compute `p_o`, κ and `p_pos`.
3. (7 min) Discuss every harassment disagreement. Write a "when to use" and a "when not to use" line that would have settled each one.
4. (5 min) Report to the room: both kappas, both `p_pos` values, and your best new boundary rule.

Expected output: two 2 × 2 tables with statistics, and two new codebook lines. Most pairs should find higher `p_o` on the rare code and lower κ and `p_pos`, which is the worked example happening to you.

## Common misconceptions

- **"90% agreement means reliable coding."** With a rare code, 90% agreement can come entirely from agreeing on the absences. Check `p_pos` and κ.
- **"Low kappa with high agreement means kappa is broken."** Kappa is reporting that agreement on the rare category is poor. The fix is in the codebook or the sampling, not a different coefficient.
- **"Every qualitative study must report inter-rater reliability."** It fits codebook-based, team-coded studies that report counts. Reflexive, interpretive analyses show rigor in other ways, and the major methods literature says so.
- **"Changing the player's name is enough anonymization."** Character, guild and server names, and distinctive public quotes, can identify a player. Pseudonymize all of them.

## Check yourself

1. Two coders code 50 excerpts for "real-money trading." Coder A marks 4 yes and coder B marks 2. They agree on both of B's yeses. Build the 2 × 2 table and compute `p_o`, κ and `p_pos`.
2. For a code with 50% prevalence in both coders' hands, what observed agreement gives κ = .60? What observed agreement gives the same κ at 10% prevalence?
3. Your research question is "How do players in a hardcore raiding guild justify benching a friend?" You plan to recruit through the guild leader. Name the recruitment bias and propose a second route.
4. A student's single-researcher reflexive thematic analysis of 12 interviews reports κ = .91 against a friend who coded three transcripts. What is wrong with this, and what should they report instead?
5. A participant in a toxicity study mentions their main character's name and the server twice. What do you do with the recording, the transcript and the published quote?

<details>
<summary>Answers</summary>

1. `a = 2, b = 2, c = 0, d = 46`. `p_o = 48/50 = .96`. `p_A = .08`, `p_B = .04`, `p_e = .08 × .04 + .92 × .96 = .0032 + .8832 = .8864`. `κ = (.96 − .8864) / (1 − .8864) = .0736 / .1136 = .65`. `p_pos = 4 / (4 + 2) = .67`. Note how few positive cases the estimate rests on.
2. At 50%, `p_e = .5`, so `.60 = (p_o − .5) / .5` gives `p_o = .80`. At 10%, `p_e = .1 × .1 + .9 × .9 = .82`, so `.60 = (p_o − .82) / .18` gives `p_o = .928`, about 93%.
3. The leader will pass the call to members they trust or who agree with them, and benched players, the people most affected, may be the least likely to hear of it or to answer. A second route: contact former members, or players who recently left the guild, through public recruitment channels or a server-wide post, with a separate consent route that the leader doesn't see.
4. Reflexive thematic analysis doesn't aim at reproducible coding, and three transcripts coded by an untrained friend don't test the analysis anyway. Report an audit trail, the researcher's position, how themes were developed and reviewed, and negative cases. If they want a check, use a peer debrief, not a kappa.
5. Keep the recording under the stored-data rules in the consent, and don't share it. In the transcript, replace the character and server names with pseudonyms or tags such as [CHARACTER] and [SERVER]. In publication, use the participant's pseudonym, omit character and server details, and paraphrase any phrasing distinctive enough to be searched.

</details>

## Lab / assignment hook

[Lab 06, from interview guide to reliable codes](../labs/lab06.md). You write an interview guide for your own project question and pilot it with one classmate in a role-play. Then you code a supplied set of invented interview excerpts with a partner, write functions for the 2 × 2 table, kappa, specific agreement and PABAK, and revise the codebook until the rare code reaches the agreement you set in advance. Deliverable: passing code, your guide, the revised codebook and a short reliability report. The guide and consent text go into your proposal.

## Sources

- Blackburn, J. & Kwak, H. (2014). "STFU NOOB! Predicting Crowdsourced Decisions on Toxic Behavior in Online Games." *Proceedings of WWW 2014*. Checked in the arXiv version (arXiv:1404.5905, September 2026): Tribunal case structure (up to five matches, chat logs, scoreboards, names removed, majority vote, agreement levels), 1.46 million cases crawled in April 2013, the classifier's roughly 80% performance, and their report of Jeffrey Lin's GDC 2013 talk: about 80% agreement between the Tribunal and Riot's in-house team, the in-house team being less lenient, and 47 million votes in the first year.
- Cohen, J. (1960). "A Coefficient of Agreement for Nominal Scales." *Educational and Psychological Measurement*, 20(1), 37-46. https://doi.org/10.1177/001316446002000104.
- Feinstein, A. R. & Cicchetti, D. V. (1990). "High Agreement but Low Kappa: I. The Problems of Two Paradoxes." *Journal of Clinical Epidemiology*, 43(6), 543-549. https://doi.org/10.1016/0895-4356(90)90158-L. Cicchetti, D. V. & Feinstein, A. R. (1990). "High Agreement but Low Kappa: II. Resolving the Paradoxes." *Journal of Clinical Epidemiology*, 43(6), 551-558. https://doi.org/10.1016/0895-4356(90)90159-M. Positive and negative specific agreement.
- Byrt, T., Bishop, J. & Carlin, J. B. (1993). "Bias, Prevalence and Kappa." *Journal of Clinical Epidemiology*, 46(5), 423-429. https://doi.org/10.1016/0895-4356(93)90018-V. PABAK.
- McDonald, N., Schoenebeck, S. & Forte, A. (2019). "Reliability and Inter-rater Reliability in Qualitative Research: Norms and Guidelines for CSCW and HCI Practice." *Proceedings of the ACM on Human-Computer Interaction*, 3(CSCW), 1-23. https://doi.org/10.1145/3359174. Abstract checked via OpenAlex: CSCW and HCI papers 2016-2018; IRR in around 1 in 9 qualitative papers.
- Braun, V. & Clarke, V. (2006). "Using Thematic Analysis in Psychology." *Qualitative Research in Psychology*, 3(2), 77-101. https://doi.org/10.1191/1478088706qp063oa. Braun, V. & Clarke, V. (2019). "Reflecting on Reflexive Thematic Analysis." *Qualitative Research in Sport, Exercise and Health*, 11(4), 589-597. https://doi.org/10.1080/2159676X.2019.1628806.
- MacQueen, K. M., McLellan, E., Kay, K. & Milstein, B. (1998). "Codebook Development for Team-Based Qualitative Analysis." *CAM Journal*, 10(2), 31-36. https://doi.org/10.1177/1525822X980100020301.
- O'Connor, C. & Joffe, H. (2020). "Intercoder Reliability in Qualitative Research: Debates and Practical Guidelines." *International Journal of Qualitative Methods*, 19. https://doi.org/10.1177/1609406919899220. Further reading on when intercoder reliability fits.
- Boellstorff, T., Nardi, B., Pearce, C. & Taylor, T. L. (2012). *Ethnography and Virtual Worlds: A Handbook of Method*. Princeton University Press. Chapter titles and pages checked via Crossref chapter records (JSTOR, doi:10.2307/j.cttq9s20.10 and .14).

## Interactive spec: examples/w06-kappa-prevalence.html

**Purpose.** Make it obvious that percent agreement can stay fixed while kappa and positive agreement collapse as a code becomes rare, and that PABAK hides the problem.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (agreement bar first).

- **Left panel, "What the headline says".** A single horizontal bar for `p_o` from 0 to 100%, labeled with the exact value. Below it, when toggled on, a second bar for PABAK.
- **Right panel, "What the table says".**
  - A line chart of κ (y from −0.2 to 1.0) against prevalence (x from 2% to 50%) for the current `p_o` and bias, computed at every whole percent, with a marker at the current prevalence and a horizontal line at κ = 0.
  - Below it, a 10 × 10 grid of 100 squares, one per excerpt, colored by cell: both yes (accent), both no (neutral light), A yes B no and A no B yes (two distinct warning shades, also distinguished by pattern). Counts shown in a small 2 × 2 table next to the grid.

**Controls.**
- Prevalence `q`, the average yes rate of the two coders: slider 2% to 50%, step 1, default 50%.
- Observed agreement `p_o`: slider 70% to 99%, step 1, default 90%.
- Coder bias `Δ`, coder A's yes rate minus coder B's: slider 0 to 20 points, step 1, default 0.
- Toggle "show PABAK".
- Presets: "Balanced code" (`q = 50, p_o = 90, Δ = 0`), "Rare code" (`q = 5, p_o = 90, Δ = 0`), "Tribunal-like" (`q = 85, p_o = 80, Δ = 10`; allow `q` up to 95 when this preset is active, or extend the slider to 95 for all).

**Model (counts out of n = 100).**
- `p_A = q + Δ/2`, `p_B = q − Δ/2` (as proportions).
- Disagreement total `D = 1 − p_o`. From `b − c = p_A − p_B = Δ` and `b + c = D`: `b = (D + Δ) / 2`, `c = (D − Δ) / 2`, `a = p_A − b`, `d = 1 − a − b − c`.
- If any cell is negative, the combination is impossible: show "not possible with these settings" and grey out the readouts. (Constraint examples: `Δ ≤ D`, `a ≥ 0`.)
- `p_e = p_A p_B + (1 − p_A)(1 − p_B)`, `κ = (p_o − p_e) / (1 − p_e)`, `p_pos = 2a / (2a + b + c)`, `p_neg = 2d / (2d + b + c)`, `PABAK = 2 p_o − 1`.
- For the grid, round cells to whole excerpts so that they sum to 100.

**Readouts.** `p_e` to three decimals, because the rare-code case (.905) needs the third digit. `p_o`, κ, `p_pos`, `p_neg` and PABAK to two decimals. The four cell counts as whole excerpts.

**Test values.**
- `q = 50, p_o = 90, Δ = 0`: cells 45, 5, 5, 45; `p_e = .50`, κ = .80, `p_pos = .90`, `p_neg = .90`, PABAK .80.
- `q = 10, p_o = 90, Δ = 0`: cells 5, 5, 5, 85; `p_e = .82`, κ = .44, `p_pos = .50`.
- `q = 5, p_o = 90, Δ = 0`: cells 0, 5, 5, 90; `p_e = .905`, κ = −.05, `p_pos = .00`, `p_neg = .95`, PABAK .80.
- `q = 85, p_o = 80, Δ = 10` (staff 90%, Tribunal 80%): cells 75, 15, 5, 5; `p_e = .74`, κ = .23.

**The one insight.** Drag prevalence from 50% to 5% at 90% agreement. The left bar never moves. The kappa marker falls below zero, and the "both yes" squares vanish from the grid.

**Accessibility and style.** Grid colors paired with patterns so the four cells are distinguishable without color. A live text summary states the table and κ after each change. Sliders keyboard operable with visible focus. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Use `templates/interactive-tokens.css` inline. No game logos or art; the Tribunal preset is named in text only.
