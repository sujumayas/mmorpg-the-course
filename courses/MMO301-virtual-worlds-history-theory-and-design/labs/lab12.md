# MMO301 · Lab 12: The persistence budget

Assigned in week 12 ([lecture](../lectures/w12-persistence-and-time-what-should-last.md)). Due at the start of week 14. Marked with the rubric below; the finished budget becomes the persistence chapter of your world design bible.

## Objective

Write a persistence budget for your own world concept (or the supplied one): every class of object the world creates, with a creation rate, a lifetime, a clock-reset rule, the steady-state stock `S = λW`, per-zone density, time to reach the ceiling, and a warning plan for anything players will miss. The skill you are practising is deciding what should last, and showing the cost of each decision.

## Starter materials

Everything below is included in this file.

**1. Default world concept, "Saltmarsh Commons"** (use it if you do not yet have your own concept). A settlement-building MMO for 25,000 active players on one shard with 30 zones. Players farm, build homes and workshops, place signs and decorations, leave corpses when they die, drop items, plant crops, raise shared town monuments and name their settlements. Players play 2 hours a day on average. About 1.5% of players quit each week.

**2. Starter object list** (extend it to at least ten classes).

| Object class | Rough creation rate per player | Notes |
|---|---|---|
| Dropped items | 20 per play-hour | Mostly junk |
| Corpses | 0.5 per play-hour | Hold the player's gear |
| Crops | 10 per day | Grow and are harvested |
| Signs and decorations | 1 per day | Player expression |
| Homes | 1 per player (created once) | Abandoned when players quit |
| Workshops | 0.3 per player (created once) | Shared by neighbours |
| Town monuments | 1 per 500 players per month | Built by groups |
| Settlement names | 1 per 50 players (created once) | Identity |

**3. Spreadsheet layout.** Columns: object class, creation rate per player per day, `λ` (whole world, per day), lifetime `W` (days), lifetime type (fixed, random, conditional), clock resets when, who depends on it, `S = λW`, per zone `S / Z`, bytes per object, storage, time to 95% of ceiling (`3W` random, `W` fixed), warning schedule, reason.

For objects created once per player and abandoned when players quit (homes, workshops), use the abandoned stock only: `λ = players quitting per day × objects per player`, and `W` is the grace period before an abandoned object is removed.

**4. Reference lifetimes from shipped games** (all cited in the week 12 lecture): Minecraft Java dropped items, 5 minutes of loaded time; EVE Online wrecks, 2 hours; Final Fantasy XIV housing, demolished after 45 days without a visit, with notices at 30, 35 and 42 days.

## Steps

1. Choose your concept (yours or Saltmarsh Commons) and state player count, zone count and play hours per day.
2. List at least ten object classes. Include at least one that should be permanent and at least one that should last less than an hour.
3. Estimate `λ` for each. Show the arithmetic from per-player rates.
4. Assign each a lifetime, a lifetime type and a clock-reset rule. Write the "who depends on it" column before choosing `W`, not after.
5. Compute `S`, per-zone density, storage and time to 95% of the ceiling. Flag any class with more than 5,000 objects per zone, and any class whose 95% time is longer than your planned beta.
6. For every flagged class, either change the lifetime or write one paragraph defending it.
7. Write warning schedules for every class a player built or owns.
8. Plot `S(t)` over three years for your four largest classes on one log-scale chart.

## Deliverable

- The spreadsheet and the chart.
- A 600-word persistence chapter for your world bible: your budget's principles (which of the four rules from lecture section 4 you rely on and where you break them), your three hardest calls with numbers, and what you would promise players about what lasts. End with one sentence on what you would do if you had to roll the world back.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Coverage | Ten or more classes spanning seconds to permanent; dependency column filled before lifetimes | Eight to nine classes, or narrow range | Fewer than eight | 15% |
| Arithmetic | `λ`, `S`, density, storage and 95% times correct, with abandoned-stock method used for owned objects | Minor errors | Model misapplied | 25% |
| Judgment | Lifetimes justified by who depends on each object; flagged classes resolved; conditional lifetimes used where people care | Justifications present but generic | Lifetimes chosen without reasons | 30% |
| Warnings and promise | Specific warning schedules; a clear, honest statement of what lasts; rollback sentence | Warnings present, promise vague | Missing | 15% |
| Chart and writing | Readable log chart with ceilings; chapter concise and specific | Chart or chapter weak | Missing | 15% |

Instructor check values for Saltmarsh Commons: dropped items `λ = 25,000 × 20 × 2 = 1,000,000` per day, so a 10-minute lifetime gives about 6,944 on the ground (231 per zone). Players quitting per day `= 25,000 × 0.015 / 7 ≈ 53.6`; with a 45-day grace period about 2,411 abandoned homes stand at any time (80 per zone).
