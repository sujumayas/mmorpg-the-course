# PR101 · Lab 11: Working agreement and contribution record

**Week:** 11, communication and conflict in teams ([lecture](../lectures/w11-communication-and-conflict-in-teams.md)).
**Time:** 2 hours in lab, plus about 1 hour at home and 5 minutes a day for two weeks to keep the record.
**Work mode:** your final-project team.
**Weight:** part of the peer review component (10%). The contribution record you start here is the evidence your peer reviews must refer to.

## Objective

Turn your week 1 team charter into a signed working agreement that handles the problems the jam exposed. It needs a channel table, a decision log, a contribution record strong enough to beat the free-rider threshold `k*`, and a conflict escalation ladder. Then test the agreement against a scripted conflict before a real one tests it.

This is a production exercise with no code. Every part has a checkable output.

## Starter materials

- Your team charter and RACI from [lab 01](lab01.md), and your jam post-mortem notes from week 9.
- Your contribution table from the week 11 in-class activity.
- Three role-play scenario cards, handed out in the lab. Each has a situation, a secret goal for each of two roles, and a fact only one role knows.
- The [interactive](../examples/w11-free-rider.html), for step 3.
- A shared document or wiki page for the agreement, plus a sheet with these columns for the contribution record: `date, member, task id, what was done, evidence link, hours`.

## Steps

### Part A: write the agreement (60 min)

1. **Channel table (10 min).** Copy the channel table from lecture section 1 and adapt it to your team's tools. Every row needs a channel, an expected response time in working hours, and what counts as "working hours" for your team (for example, 9:00-21:00 on weekdays).
2. **Decision log (10 min).** Create the log page with columns `date, decision, decided by, reason, replaces`. Enter at least five decisions your team has already made for the final game, recovered from chat history or memory. Mark any where two members remember it differently. Settle those now.
3. **Contribution record and `k` (20 min).**
   - List what counts as a contribution. It must include at least one shared, unglamorous kind of work (merges, build fixes, bug triage, playtest organization).
   - Say how each contribution is evidenced (a task id, a commit, a merge request, a tracker entry).
   - Agree your team's `m`, compute `k* = 1 − m / n`, and describe your individual-credit mechanisms (the peer review rubric, named ownership, demo slots, visible cards). Argue in three to five sentences that together they are at least `k*`. Use the interactive to show the effect of your chosen `k`.
   - Name one way someone could game each measure and the rule that prevents it.
4. **Escalation ladder (10 min).** Adapt the four rungs from lecture section 3. Give each rung a trigger, a time limit and a named person or role. State the exception that skips the ladder (harassment or safety) and the university route for it.
5. **Overtime placeholder (5 min).** Leave a heading "Overtime policy" with the text "to be completed in lab 12".
6. **Sign (5 min).** Every member adds their name and the date. Unsigned agreements are not accepted.

### Part B: role-play (40 min)

7. Two members take the roles on scenario card 1. The other two observe with a checklist: Did the speaker use observation, impact and request? Which Thomas-Kilmann mode did each person use? Was the conflict about the task or the relationship, and did it shift? Did it end in a decision that could go in the log? Play for 6 minutes.
8. Debrief for 5 minutes using the checklist. Then swap roles and play card 2, then card 3, so everyone plays at least once.
9. For each card, write which rung of your ladder the situation would reach if the role-play had failed, and whether your agreement as written covers it. Change the agreement if it does not.

### Part C: keep the record (two weeks, 5 min a day)

10. Every member logs their contributions in the record, with evidence, for the next two weeks. The team triage owner from week 10 checks once a week that every entry has an evidence link.

## Deliverable

Submitted as one PDF or a link to the team's shared page, plus the record sheet:

- The signed working agreement with all five sections (channels, decision log location, contribution record rules with the `k*` argument, ladder, overtime placeholder).
- The decision log with at least five entries.
- The contribution record covering the two weeks after the lab.
- A **role-play debrief** of about 300 words: what the three scenarios revealed, the changes you made to the agreement, and the mode each role used in each scenario.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Channel table | Every message type has a channel, a response time and a defined working-hours window | Table present, some times vague ("quickly") | Missing | 10 |
| Decision log | Five or more entries with reasons; conflicting memories found and settled | Five entries, reasons thin | Fewer than five | 15 |
| `k*` and contribution rules | `k*` computed correctly; mechanisms argued to meet it; shared work counts; gaming risk and rule for each measure | `k*` correct, argument or gaming rules weak | Missing or `k*` wrong | 25 |
| Escalation ladder | Four rungs with triggers, time limits and names; safety exception and route stated | Rungs present, triggers or names missing | Missing | 15 |
| Role-play debrief | Modes and conflict types identified with evidence; agreement changed where it failed | Debrief present, no changes or vague | Missing | 20 |
| Contribution record | Two weeks, every member, evidence links on at least 90% of entries | Gaps of a few days or missing links | Missing or one member only | 15 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

- Scenario cards to prepare (one per team per card, secret goals folded): (1) an artist has redrawn a key sprite three times and the programmer refuses another change; the artist knows the lead asked for it. (2) A member has logged two hours in a week against a plan of ten; they have a family emergency they have not mentioned. (3) Two members disagree about cutting the second level; one has playtest data nobody else has seen.
- Card 2 checks whether teams separate `H` (available hours) from free riding. Strong debriefs say so explicitly.
- A `k*` argument that relies only on "we trust each other" earns no marks for that row. Visibility (named cards, evidence links) is enough to count as a mechanism if the team says how it enters peer review.

</details>
