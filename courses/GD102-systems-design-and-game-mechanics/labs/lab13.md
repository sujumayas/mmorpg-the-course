# GD102 · Lab 13: Write a system specification

**Assigned:** week 13 ([lecture](../lectures/w13-systems-documentation.md)). **Due:** start of week 14 class. **Feeds:** the final system design document (40%) and [Lab 14](lab14.md), which tunes the numbers you specify here.

## Objective

Turn a vague one-paragraph brief into a system specification that someone else can implement and test without asking you a question. You will compute the system's derived numbers, write numbered testable rules, build a parameter table and write given/when/then test cases. Then a classmate tries to "implement" your system on paper, and every question they have to ask you counts as a hole.

## Starter materials

Everything you need is on this page. Copy the brief and the template into your own document (Markdown, Google Docs or Word).

### The brief (deliberately vague)

> **Workshop energy.** In our small crafting game, players craft items at a workshop. Crafting uses energy. Energy refills over time, a bit faster if the player is in their home town. There is a maximum. Players can drink a tonic to get some energy back. Rare recipes cost more energy. We want players to come back a couple of times a day, but we don't want to punish people who can only play in the evening.

Design constraints from the lead designer (these are fixed):

| Constraint | Value |
|---|---|
| Common recipe cost | 10 energy |
| Rare recipe cost | 40 energy |
| Target crafts per day for a player who checks in twice a day (every 12 h), all common recipes | 12 |
| Target crafts per day for a player who checks in once a day (evening only), all common recipes | at least 8 |
| Tonic | restores 50 energy; sold in the in-game shop for gold |

### Specification template

Use these headings in this order (they match the week 13 lecture, section 3):

1. Purpose
2. Vocabulary
3. Model (a stock-flow sketch or Machinations diagram, plus one sentence per feedback loop)
4. Rules (numbered, testable)
5. Parameters (table with Name, Value, Unit, Safe range, Why this value, Owner)
6. Derived numbers (table with Name, Formula, Value)
7. Edge cases and states (include a state diagram for the refill timer)
8. Interfaces (what the system reads and writes)
9. Telemetry and success criteria
10. Open questions and change log

### Implementer's question log

Your partner uses this table in step 6. Copy it into the end of your document.

| # | Section read | Question asked | Could the document answer it? (yes / no) | Fix made |
|---|---|---|---|---|

## Steps

1. **Derive the numbers first (30 min).** The brief's targets pin down two things. A 12-hour player must get 120 energy per 12 hours of play (12 common crafts a day), and a 24-hour player must get at least 80 per day. Choose a regeneration rate `R` (energy per hour, in town) and a cap `C`. Compute the knee `C / (energy per hour)` and the energy per day for check-in intervals of 4, 8, 12 and 24 hours using `min(C, rate × T)` per visit. Put these in section 6. Show that both targets are met. Hint: one choice that works has a rate of 5 energy per hour and a cap of 80 or more; you may choose differently.
2. **Decide the out-of-town rate (10 min).** The brief says energy refills "a bit faster" in town. Choose the out-of-town rate as a fraction of the in-town rate, and recompute the 12-hour and 24-hour rows for a player who is out of town the whole time. State in one sentence which player the difference affects.
3. **Close the holes (40 min).** Write rules for at least these questions, plus any others you find: Does the refill timer keep progress when energy is spent? Does it run at the cap? Can a tonic take energy above the cap? If so, does regeneration continue above the cap? What happens if a rare recipe costs 40 and the player has 35? Is energy spent when crafting starts or when it finishes? What happens if the player disconnects mid-craft? Which clock is authoritative? What happens to stored energy if a patch lowers the cap?
4. **Parameter table (15 min).** Every number in your rules must appear here by name. Give each one a unit, a safe range and a one-line reason. Mark placeholders as placeholders.
5. **Test cases (20 min).** Write at least eight given/when/then cases. At least one must distinguish "pause at full" from "wall clock", at least one must cover the tonic above the cap, and at least one must cover offline time crossing the knee.
6. **Paper implementation (30 min, in class or by arrangement).** Swap documents with a partner. Your partner writes pseudocode (15 to 30 lines) for `on_tick`, `on_craft_start` and `on_tonic` using only your document. Every time they need to ask you something, they log it in the question log. You may answer, and then you must fix the document. Keep the log in your submission.
7. **Revise (20 min).** Close every "no" in the question log. Add a change log entry for each fix.

## Deliverable

One document (PDF or Markdown) containing:

- The completed specification with all ten sections.
- The derived-numbers table with the four check-in intervals, in town and out of town.
- At least eight test cases.
- Your partner's pseudocode (a photo or pasted text) and the completed question log.
- A 150-word reflection: which hole surprised you most, and what it would have done to which players if it had shipped.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Derived numbers | Knee, daily maximum and all four intervals correct in and out of town; both brief targets shown to be met | Numbers mostly correct, one target not checked | Numbers missing or targets not met | 20% |
| Rules | Numbered, testable, parameter names instead of numbers; every question in step 3 answered | Most questions answered; some rules vague ("should", "usually") | Rules are prose descriptions | 25% |
| Parameter table | Every parameter present with unit, safe range, reason and owner; placeholders marked | Table present, missing ranges or reasons | No table, or numbers only in prose | 15% |
| Test cases | Eight or more, including the three required types; each would fail under a wrong implementation | Eight cases, one required type missing | Fewer than five cases | 20% |
| Paper implementation and revision | Question log complete; every "no" fixed and logged in the change log | Log present, some fixes missing | No partner implementation | 10% |
| Reflection | Names a specific hole, the affected players and the size of the effect in numbers | Names a hole without consequences | Missing | 10% |
