# MMO305 · Field observation brief

**Weight:** 30% of the course grade.
**Covers:** a field observation of one live online community, run over weeks 6 to 13 and written up in week 14, plus labs 04, 10, 12 and 13.
**Related briefs:** [reading-responses-brief.md](reading-responses-brief.md) and [final-design-proposal-brief.md](final-design-proposal-brief.md). The methods come from [week 2](../lectures/w02-playing-alone-together.md) (census and the three layers) and [week 13](../lectures/w13-ethnography-of-online-worlds.md) (participant observation, field notes, length bias). Read week 13 section 3 before your first session, even though it is taught later. The lab 13 materials show the notes format.

## What this component is for

Telemetry tells you what players did. Fieldwork tells you what it meant to them and which unwritten rules keep a space working. The course outcome behind this component is "explain how game systems create or erode social ties," and here you do it with evidence you collected yourself, from a real community, without harming anyone in it.

The component also trains a habit the lectures keep returning to. Every sample has a shape. The players you meet in a city hub are length-biased toward heavy players (week 13), and the posters in a forum are biased by the voice ratio (week 12). Your report has to say who you saw, who you probably missed, and how far the correction moves your numbers.

## Part A: field labs (40% of this component)

These labs are marked here with the rubric printed in each lab file.

| Lab | Topic | Assigned | Due | Role in the field observation |
|---|---|---|---|---|
| [04](../labs/lab04.md) | Guild health model | Week 4 | Start of week 5 | Model for module M6 (guild rules) |
| [10](../labs/lab10.md) | Chat channel load and design | Week 10 | Start of week 11 | Step 1 is a real channel count; seeds module M3 |
| [12](../labs/lab12.md) | Reading a loud forum | Week 12 | Start of week 13 | Tagging method for module M5 |
| [13](../labs/lab13.md) | Field observation with a bias correction | Week 13 | Start of week 14 | Length-bias correction for the core analysis; its sessions may count toward your fieldwork |

Each lab is worth 10% of this component (3% of the course). No lab is dropped, because each one supplies a method the report uses.

**Converting lab rubrics.** Lab 04 prints points that sum to 100. Labs 10 and 12 use four bands with percentage weights, scored `weight × band / 4` with Excellent as 4. Lab 13 uses full, half or zero marks on each weighted criterion.

## Part B: field observation report (60% of this component)

### Choose a site

A field site is a specific place and community, not a whole game. Good sites for this assignment include a capital city's bank or auction area, a starting zone and its chat channel, a public world event or world boss, a queue lobby or group-finder channel, or a public forum board or subreddit about one game. Pick a game you can play or read regularly. The site must fit the ethics rules below.

You may study the same game as a classmate, but not the same site. Tell the course team your site in the week 5 milestone.

### Fieldwork minimum

- At least **six** observation sessions totalling at least **eight** hours, between week 6 and the end of week 13.
- Spread over at least three different days, including at least one weekday daytime session. Compute `P(seen) = 1 − (1 − h/168)^k` for a 4-hour-a-week player with your plan and put the number in your plan (week 13 section 2).
- One sighting sheet row per player per sampled minute inside a fixed observation area you define in advance, as in lab 13. Sample every minute, or every five minutes in busy areas, and say which.
- Sessions you run for lab 13 count toward the six if they are in the same site.

### What the report contains

The report is 3,000 to 4,000 words, not counting tables, figures and appendices. Use these sections.

1. **Site and question.** The game, the version or season, the place, and the one question your fieldwork tries to answer, in one sentence ("How do strangers at the world boss decide whether to group?").
2. **Plan and role.** Session times, the observation area, your sampling interval and `P(seen)`. A role statement: did you only watch, or also take part, and how your presence may have changed what happened.
3. **Core analysis.** Required for everyone.
   - Counts by sighting and by unique pseudonym, split into light, medium and heavy players by sessions seen, with shares by sighting, by unique pseudonym, and weighted by `1 / minutes seen` (the lab 13 Part D method).
   - The grouped share of sightings and the "alone together" share, meaning sightings of ungrouped players doing the same activity in the area as others (week 2).
   - One claim your raw data supports and one it does not, given the bias.
4. **Two modules.** Choose two from the list below. Each module has at least one table and one number computed with its lecture's model.
5. **Analytic memo.** One norm or recurring pattern you observed, told through at least two thick descriptions (week 13 section 1). What it means for the people involved, how you know, which system in the game produces it, and what a designer who changed that system would lose or gain.
6. **Who you missed.** The players your method probably did not see or hear, and what that does to your claims.
7. **Design implication.** One change to the game that your evidence supports, with the model term it moves.
8. **Appendices.** Field notes from every session (jottings, expanded notes and memos kept separate, with at least three thin and thick pairs), the sighting sheet, the approved ethics checklist, and your pseudonym scheme without the key.

### Modules (choose two)

| Module | Lecture | What you collect | What you compute |
|---|---|---|---|
| M1 Credential watch | [Week 7](../lectures/w07-status-prestige-and-conspicuous-display.md), lab 07 | Every request for or citation of an achievement, rank, score or item as proof of ability, in a group finder or LFG channel | Requests per hour; the signal each credential carries (skill, time, wealth, luck, tenure); precision and `b50` for the most requested one, with estimated inputs |
| M2 Harm log | [Weeks 8](../lectures/w08-griefing-typology-and-design-responses.md) and [9](../lectures/w09-toxicity-research-and-interventions.md), lab 09 | Every griefing or toxic incident you witness, with time and context | Incidents per observed player-hour; counts by Foo and Koivisto type and by Kou type; reaction-driven or gain-driven; the system that carried each one |
| M3 Channel load | [Week 10](../lectures/w10-communication-design-chat-emotes-pings.md), lab 10 | Message counts, distinct posters and repeats in a public channel, in at least three 10-minute windows | `M`, `s × r`, `T` for your window size, coverage for a stated `R`, the share of repeats, and whether the channel is past `L*` |
| M4 Newcomer space | [Week 11](../lectures/w11-newcomers-and-mentoring-systems.md), lab 11 | Questions asked in a starting zone or newcomer channel, whether and how fast they were answered, and any rejection events | Answer rate, median time to first answer, rejections per hour, and which model term (`a` or `p`) each pattern would move |
| M5 Community voice | [Week 12](../lectures/w12-community-management.md), lab 12 | At least 150 public posts on one topic, tagged by poster and sentiment | Negative share by post and by poster; a range for `d` from a stated range of `ρ`; any behavioural evidence that narrows it |
| M6 Guild rules | [Weeks 4](../lectures/w04-guilds-formation-lifecycle-leadership.md) and [5](../lectures/w05-raiding-as-organization-dkp.md), lab 04 | A guild's written and unwritten rules, gathered **only with the guild leader's written consent** (see the ethics rules) | Each rule mapped to `R`, `c` or `M`; the guild's critical mass; if it has a loot rule, its `ρ` |

### Research-ethics rules for observing live communities

These rules follow the week 13 lecture and the Association of Internet Researchers' *Internet Research: Ethical Guidelines 3.0* (2019), which the lecture cites. They are not optional. A breach can cap the report grade at the Ethics criterion's "Weak" band and, if serious, will be referred under the university's research-conduct procedures.

**Before you start**

1. **Approval first.** Submit the one-page site proposal and ethics checklist (milestone, week 5) and wait for written approval before your first session. Sessions run before approval do not count.
2. **Public spaces by default.** You may observe spaces that any player can enter without an invitation or an application: city hubs, zones, open world events, public queues, public chat channels, and public forums or subreddits. Guild chat, private or application-only Discord servers, voice channels, party chat you were not invited into as an ordinary player, and direct messages are off limits.
3. **The one exception is module M6.** To study a guild you must have the guild leader's written consent, sent after you have told them, in writing, what you are studying, what you will record, how you will anonymise it, and that any member can opt out. Keep the message and put a redacted copy in the appendix. Announce your role in the guild channel. If a member opts out, record nothing about them and delete what you have.
4. **No interviews.** This assessment uses observation only. Formal interviews and surveys with identifiable people need institutional ethics approval, which MMO405 covers. Casual in-game conversation that happens while you play is not data unless it took place in a public channel.

**While you observe**

5. **Observe, do not experiment.** Play as an ordinary player would. Do not provoke, bait, grief, deceive or test players to see how they react. Do not pose as a newcomer, a seller or anyone else you are not.
6. **Follow the game's rules.** No cheats, exploits or tools the terms of service forbid. Automated logging is allowed only through features the game provides to every player (for example a built-in chat log) and only if the terms allow it. Ask the course team if unsure.
7. **Record behaviour, not people.** Never record real names, ages, locations, voices, faces, or anything a player discloses about their offline life. If someone shares such details in public chat, leave them out of your notes.
8. **Minors.** Avoid spaces aimed at children. If you learn that a player is a minor, stop recording that player and remove what you have.
9. **If you witness harm.** Do not intervene as a researcher in a way that escalates it. You may use the game's own report and block tools, as any player would. You may end a session whenever a space becomes hostile to you. If you see a threat to someone's safety, use the platform's reporting route and tell the course team.

**When you write**

10. **Pseudonyms for everything identifying.** Replace every character name with a code (P01, P02 in order of first sighting). Replace guild names, and server names too if the community is small enough to identify. Remember that character names are searchable, so a real name in a footnote is a breach.
11. **No verbatim chat.** Paraphrase every message. Do not quote chat lines or forum posts word for word, because a quoted line can be searched back to its author. The same rule covers screenshots. Include none that show names or chat text.
12. **Store data safely.** Keep raw notes and logs on university storage, not in a shared or public folder. Keep the pseudonym key in a separate file, never submit it, and delete it and any raw logs with real names within 30 days of receiving your grade.

### Report rubric (100 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Site, question and plan | 10 | 9-10: focused question, sessions spread with `P(seen)` computed and used, honest role statement | 7-8: plan sound, one of `P(seen)` or role statement thin | 5-6: plan present, timing not justified | 0-4: single time slot, or no plan |
| Field notes | 20 | 18-20: jottings, expanded notes and memos kept separate for every session; three convincing thin and thick pairs | 14-17: notes complete, one pair weak | 10-13: description and interpretation mixed, or sessions missing | 0-9: retrospective notes only, or fewer than six sessions |
| Core analysis | 20 | 18-20: shares by sighting, unique and weighted all correct; grouped and alone-together shares; supported and unsupported claims argued from the bias | 14-17: one computation off, reasoning sound | 10-13: correction missing or misapplied | 0-9: raw counts only |
| Two modules | 20 | 9-10 each: data collected as specified, model applied correctly, a finding a designer could use | 7-8 each: correct, finding thin | 5-6 each: data present, model loosely applied | 0-4 each: missing or no model |
| Analytic memo and design implication | 20 | 18-20: a specific norm, told with thick description, tied to the system that produces it; who was missed and why; implication names the model term | 14-17: norm and system clear, missed players thin | 10-13: describes behaviour without interpreting it | 0-9: generic or unsupported |
| Ethics | 10 | 10: approved plan followed; public spaces only (or documented consent for M6); pseudonyms throughout; no verbatim chat or identifying screenshots | 7-9: one minor slip corrected before submission | 4-6: one lapse in the submission, such as a real character name | 0-3: repeated lapses, private spaces without consent, or experimenting on players |

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Start of week 5 | Lab 04 | Yes, Part A |
| End of week 5 | One-page site proposal and ethics checklist: game, site, question, planned session times, modules, and a signed statement that you have read the ethics rules. Approval or requested changes come back within a week. | Required before fieldwork |
| Week 7 lab session | Pilot session report: one hour of notes and sighting sheet from your site, checked by a tutor for format and ethics | Required, ungraded |
| Week 10 lab session | Progress check: notes from at least three sessions and a first look at your two modules | Required, ungraded |
| Start of week 11 | Lab 10 | Yes, Part A |
| Start of week 13 | Lab 12 | Yes, Part A |
| End of week 13 | Fieldwork closes | |
| Start of week 14 | Lab 13 | Yes, Part A |
| End of week 14 | Field observation report | Yes, Part B |

## How the component grade is computed

`component = 0.1 × (lab 04 + lab 10 + lab 12 + lab 13) + 0.6 × report`, with every score out of 100. It is worth 30% of the course.

## Late work and extensions

- A lab or report submitted up to 48 hours late loses 10 points out of 100. After that it scores 0.
- The free 48-hour extensions from the reading responses brief also apply to labs 04, 10 and 12. They do not apply to lab 13 or the report, because the report deadline sits close to the final design deadline.
- If your site closes, changes beyond use, or becomes unsafe for you to observe, tell the course team at once. You may switch sites with approval, and the fieldwork minimum is reduced in proportion to the time left.

## Academic integrity

Your notes and sighting sheets must record sessions you actually ran. Invented or copied field data is misconduct. You may discuss methods with classmates and share general observations about a game, but your data, analysis and words must be your own.
