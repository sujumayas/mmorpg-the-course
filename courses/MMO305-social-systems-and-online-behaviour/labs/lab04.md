# MMO305 · Lab 04: Guild health model

**Assigned:** week 4. **Due:** start of week 5. **Weight:** part of the field observation component (30% of the course).
**Lecture:** [Week 4, guilds: formation, lifecycle, leadership](../lectures/w04-guilds-formation-lifecycle-leadership.md). **Interactive:** `examples/w04-guild-tipping-point.html`, for checking your model once it is built.

## Objective

Fit the week 4 guild model (`N(next) = N + R − c(N) × N`, with churn switching at a critical mass `M`) to 16 weeks of roster data from a fictional raiding guild. Estimate its recruitment and churn rates, find its steady states, explain what happened to it, and write a rescue plan its officers could act on. By the end you should be able to look at any guild's roster history and say which side of its tipping point it is on.

## Starter materials

**Tool.** Any spreadsheet (Google Sheets, Excel, LibreOffice Calc) or Python with a plotting library. Say which you used.

**The guild.** "Lanternwatch" is a fictional guild in a fictional MMO whose hardest raid needs exactly 20 players. Lanternwatch raids two nights a week. "Active" means the member attended at least one guild event that week. The "walkout" column counts members who left together after an argument between officers in week 9, separately from ordinary departures.

Copy this table into your sheet as it stands.

| Week | Active at start | Joined | Left (ordinary) | Walkout | Active at end | Raid nights held (of 2) |
|---|---|---|---|---|---|---|
| 1 | 26 | 2 | 1 | 0 | 27 | 2 |
| 2 | 27 | 3 | 1 | 0 | 29 | 2 |
| 3 | 29 | 2 | 2 | 0 | 29 | 2 |
| 4 | 29 | 2 | 1 | 0 | 30 | 2 |
| 5 | 30 | 1 | 2 | 0 | 29 | 2 |
| 6 | 29 | 3 | 1 | 0 | 31 | 2 |
| 7 | 31 | 2 | 2 | 0 | 31 | 2 |
| 8 | 31 | 2 | 1 | 0 | 32 | 2 |
| 9 | 32 | 2 | 2 | 13 | 19 | 1 |
| 10 | 19 | 2 | 4 | 0 | 17 | 0 |
| 11 | 17 | 3 | 3 | 0 | 17 | 0 |
| 12 | 17 | 2 | 4 | 0 | 15 | 0 |
| 13 | 15 | 2 | 3 | 0 | 14 | 0 |
| 14 | 14 | 1 | 3 | 0 | 12 | 0 |
| 15 | 12 | 2 | 2 | 0 | 12 | 0 |
| 16 | 12 | 1 | 3 | 0 | 10 | 0 |

**Attendance note from the officers.** On a typical night, about 85% of active members sign up.

## Steps

1. **Check the data.** Add a column that verifies `start + joined − left − walkout = end` for every week. Fix nothing; report any row that fails (none should).
2. **Plot it.** Chart active members at end of week against week, with a horizontal line at 20.
3. **Estimate `R`.** Compute mean weekly joins for weeks 1 to 8 and for weeks 10 to 16. Is recruitment different in the two periods? Use one value of `R` for the model and justify it.
4. **Estimate `c_low` and `c_high`.** For weeks 1 to 8, divide total ordinary departures by the sum of "active at start". Do the same for weeks 10 to 16. Leave week 9 out of both and explain why in one sentence.
5. **Choose `M`.** The raid needs 20, but members don't all show up. Use the binomial method from week 5 section 1 (or the table there) to estimate how many active members Lanternwatch needs to field 20 on about 70% of nights at 85% sign-up. Compare that with 20. Which value explains the "raid nights held" column better? Use it as `M`.
6. **Compute the steady states** `N_high = R / c_low` and `N_low = R / c_high`, and say which are valid.
7. **Run the model.** Starting from 26 in week 1, simulate 16 weeks with your parameters and the week 9 walkout of 13. Plot the model next to the data. Report the largest gap between them and one reason for it.
8. **Rescue plan.** Compute the rescue condition `R > c_high × M`. Then design a plan for the officers starting in week 17 at 10 active members. The plan must name which model term each action moves and by how much you assume it moves it. Simulate the plan for 12 weeks and show whether Lanternwatch crosses `M`. Consider at least one action that is not recruiting (for example, running a smaller flexible-size raid, which lowers `M`, or merging with another guild).
9. **Reflect.** In 150 words, say what the officers could have done in weeks 8 and 9 that the model suggests would have mattered most.

## Deliverable

A short report (PDF or document, at most 4 pages plus the sheet or script) containing: the data check, the plot with the threshold line, a parameter table (`R`, `c_low`, `c_high`, `M`, each with how you got it), the steady states, the model-versus-data plot with the gap discussion, the rescue plan with its simulation, and the reflection. Attach the spreadsheet or script.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Data check and plot | 10 | Every row checked; plot labelled with threshold line | Plot without check, or unlabelled | Missing |
| Parameter estimates | 25 | `R`, `c_low`, `c_high` computed correctly from the right weeks; week 9 exclusion explained | One estimate wrong or unexplained | Two or more wrong |
| Critical mass | 15 | Binomial reasoning applied, `M` chosen and compared with the raid-nights column | `M = 20` used without discussion | Missing |
| Model run and comparison | 20 | Steady states correct and model plotted against data with a reasoned gap explanation | Model run without comparison | Missing |
| Rescue plan | 20 | Each action tied to a model term with an assumed size; simulation shows the outcome; includes a non-recruiting action | Plan without simulation or without model terms | Missing |
| Reflection | 10 | Specific to weeks 8 and 9, grounded in the model | Generic advice | Missing |
