# MMO305 · Lab 13: Field observation with a bias correction

**Week:** 13, [Ethnography of online worlds](../lectures/w13-ethnography-of-online-worlds.md)
**Time:** one 2-hour lab session plus about 4 hours of observation during the week
**Feeds:** the field observation assessment (30%)

## Objective

Plan, run and write up a short piece of participant observation in a public space of an online game. Correct your counts for length bias using the week 13 model. By the end you should be able to say what you saw, who you probably did not see, and how far your raw numbers differ from the corrected ones.

## Starter materials

1. **The synthetic dataset.** Before you go into the field, you practise the correction on data where you know the right answer. Save the script below as `make_sightings.py` and run it with any Python 3 (no packages needed). It builds a 1,000-player server with the week 13 groups (600 casual players at 4 hours a week, 300 regular at 12, 100 hardcore at 40). It then simulates an observer who logs in at 10 random hours and meets a random 15% of whoever is online. It writes `sightings.csv` with the columns `session_hour`, `player` and `reported_hours`. Player IDs start with C, R or H for the group.

```python
"""Lab 13 starter: synthetic sightings log for a 1,000-player server."""
import csv, random

random.seed(305)
GROUPS = [("casual", 600, 4), ("regular", 300, 12), ("hardcore", 100, 40)]
HOURS_IN_WEEK = 168

players = []
for group, count, hours in GROUPS:
    for i in range(count):
        # each player has a fixed set of online hours in the week
        online = set(random.sample(range(HOURS_IN_WEEK), hours))
        players.append((f"{group[0].upper()}{i:03d}", group, hours, online))

# the observer logs in at 10 random hours of the week
sessions = sorted(random.sample(range(HOURS_IN_WEEK), 10))
# in each session the observer meets a random 15% of the players online
with open("sightings.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["session_hour", "player", "reported_hours"])
    for hour in sessions:
        for pid, group, hours, online in players:
            if hour in online and random.random() < 0.15:
                w.writerow([hour, pid, hours])
```

With seed 305 on a current Python 3 the file has about 90 rows. Exact counts can differ slightly between Python versions, and that does not matter for the lab.

2. **Field-note template.** Use one page per session with four headed blocks: *Setting* (game, server or shard, place, date, start and end time, your character's role), *Jottings* (timestamped, pseudonyms only), *Expanded notes* (written the same day), *Memos* (your interpretations, kept separate).

3. **Sighting sheet.** A spreadsheet with the columns `session`, `minute`, `pseudonym`, `activity` and `grouped (y/n)`. Once per minute, record every player character inside a fixed area you define in advance (for example, the bank steps of a capital city).

4. **The week 13 interactive**, `examples/w13-who-you-meet.html`, once it is built. Until then, the formulas in section 2 of the lecture.

## Steps

### Part A, practice on known data (in the lab session, 45 minutes)

1. Run the script. Count the rows (sightings) and the unique player IDs.
2. Compute the group shares three ways: (a) share of sightings, (b) share of unique players, (c) share of unique players weighted by `1 / reported_hours`, then renormalised.
3. Compute the mean reported hours over sightings and over unique players, and compare both with the true mean of 10.
4. Compare your three sets of shares with the true 60/30/10. Write two sentences on which method came closest and why.

You should find that raw sightings put the hardcore group near 40% and the mean hours near 21. The weighted estimate should land within a few points of 60/30/10.

### Part B, plan the fieldwork (in the lab session, 30 minutes)

5. Choose a public space in a game you can access: a city hub, a starting zone, a public event, or a queue lobby. Only public, open-to-anyone spaces. No guild chat, voice channels or private Discords. That keeps the lab within observation of public behaviour, which needs no consent under the course's ethics guidance.
6. Choose at least four one-hour sessions spread across different days and times, including at least one weekday daytime slot. Use `P(seen) = 1 − (1 − h/168)^k` to estimate the chance of seeing a 4-hour-a-week player at least once with your plan. Write that number in your plan.
7. Define your fixed observation area and your pseudonym scheme (for example P01, P02 in order of first sighting). Write a one-paragraph statement of your role. Will you only watch, or also take part? How might your presence change what happens?

### Part C, observe (during the week, about 4 hours)

8. In each session, take jottings throughout and fill the sighting sheet once per minute.
9. Write expanded notes the same day. For at least three events, write both a thin and a thick description.
10. Do not quote chat verbatim in anything you hand in. Paraphrase and use pseudonyms. Replace server and guild names if the community is small.

### Part D, analyse (after fieldwork)

11. From the sighting sheet, compute sightings per pseudonym ("minutes seen"). Treat total minutes seen across your sessions as a stand-in for each player's time in the space.
12. Split players into light (seen in 1 session), medium (2) and heavy (3 or more sessions). Report their shares by sighting, by unique pseudonym, and by unique pseudonym weighted by `1 / minutes seen`.
13. State one claim your raw data would support and one it would not, given the bias.

## Deliverable

A single PDF or Markdown file with:

- The Part A table (three sets of shares, two means) and your two-sentence comparison.
- Your observation plan, including the `P(seen)` estimate and your role statement.
- Field notes from all sessions, with pseudonyms, including three thin/thick pairs.
- The Part D table and the two claims.
- An 800-word analytic memo. Say what social norm or pattern you observed, what you think it means for the people involved, and which players your method probably missed.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or weak (0) | Weight |
|---|---|---|---|---|
| Part A correction | All three share estimates and both means correct; comparison explains length bias in terms of `h` | Numbers mostly correct; explanation vague | Numbers wrong or missing | 20% |
| Observation plan | Sessions spread across the week; `P(seen)` computed and used to justify the plan; clear role statement | Plan present but timing not justified, or role statement thin | No plan or single-slot plan | 15% |
| Field notes | Jottings, expanded notes and memos kept separate; three convincing thin/thick pairs | Notes present but description and interpretation mixed | Notes missing or retrospective only | 25% |
| Part D analysis | Correct shares by sighting, unique and weighted; one supported and one unsupported claim, both well argued | Tables present with minor errors, or claims weakly linked to the bias | Missing or incorrect | 15% |
| Analytic memo | Names a specific norm with evidence; interprets it with care; states who was missed and why | Describes behaviour without interpreting it, or ignores who was missed | Missing or generic | 20% |
| Ethics | Public spaces only; pseudonyms throughout; no verbatim chat | One lapse (for example a real character name) | Repeated lapses or private spaces observed | 5% |
