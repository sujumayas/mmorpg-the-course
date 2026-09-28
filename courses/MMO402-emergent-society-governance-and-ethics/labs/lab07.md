# MMO402 · Lab 07: Tune a review panel

**Week:** 7 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the case analyses (30%)

## Objective

Design the review, sanction and appeal stages of a justice pipeline for a mid-sized MMO, test your design on a simulated caseload, and defend the balance of errors you chose. You will see in practice what [week 7](../lectures/w07-justice-systems-reports-reviews-appeals.md) showed on paper: panel size, threshold, correlation between reviewers, strike ladders and appeals each move wrongful convictions and missed offences in different directions, and they all cost reviewer time.

## Starter materials

- [`lab07-starter.py`](lab07-starter.py), a standard-library Python script (3.8 or later, no packages). It simulates 20,000 players for 12 weeks. By default 3% are persistent offenders (a reported offence in 30% of weeks), everyone else offends in 0.4% of weeks, and any player is reported without having offended in 0.2% of weeks. Every reported case goes to a review panel; convictions climb a strike ladder whose last rung is a permanent ban; appeals are optional. Run `python lab07-starter.py --help` to see every option.
- Key options: `--n` and `--t` (panel size and threshold), `--s` and `--f` (reviewer sensitivity and false-guilty rate), `--rho` (share of cases where the panel shares one impression), `--ladder` (for example `warn,1d,7d,perm` or `perm`), `--appeal` with `--a-i`, `--a-g`, `--s-a`, `--f-a`, and `--seed`.
- The week 7 interactive, `examples/w07-review-panel.html`, for quick checks of single-panel probabilities. If it is not yet built, use the formulas in section 2 of the lecture.
- A spreadsheet for recording runs.

All numbers in the script are synthetic. They describe no real game.

## Steps

1. **Baseline (15 minutes).** Run the script with defaults. Record conviction rate, correct and wrongful convictions, missed offences, permanent bans and how many of them had a wrongful strike, and reviewer workload per week. Then run it with `--ladder perm` (every conviction is a permanent ban) and record the same numbers. Write two sentences on what the ladder does.
2. **Careful and harsh crowds (15 minutes).** Keep the default ladder. Run `--n 5 --t 3` with `--f 0.3`, then with `--f 0.6`. Compare the conviction rates and the wrongful convictions. Check that the pattern matches the lecture's Crowd A and Crowd B tables.
3. **Correlation (10 minutes).** Run `--n 5 --t 3 --f 0.3` with `--rho 0`, `0.3` and `0.6`. Plot wrongful convictions against `rho`.
4. **Set your error targets (10 minutes).** Before tuning, write down your targets for a 12-week run:
   - the maximum number of permanently banned players with at least one wrongful strike you will accept;
   - the maximum share of real offences you will let go unpunished;
   - your reviewer budget: 2,000 reviews a week.
5. **Tune (40 minutes).** Search over `n`, `t`, ladder and appeal settings to meet your targets within the budget, with `f = 0.35`, `s = 0.9`, `rho = 0.2` (your estimates for your volunteer reviewers). Record every run in your spreadsheet. Try at least eight configurations.
6. **Robustness (15 minutes).** Take your chosen configuration and change `--seed` to five different values. Report the range of each output. Then change `--f` to 0.55 to represent a crowd that has drifted harsh. Which of your targets fails first?
7. **Two sanctions (15 minutes).** Your game also needs a 24-hour chat restriction for minor offences, reviewed by the same team. Propose a separate, cheaper panel for it (for example `--n 1`), and argue in one paragraph why its error ratio can differ from the permanent-ban pipeline's.

## Deliverable

A policy memo of about 500 words plus your spreadsheet. The memo must:

- state your chosen `n`, `t`, ladder and appeal settings, and your error targets;
- report your results with the seed range from step 6;
- give your ratio of missed offences to wrongful convictions and defend it, referring to Blackstone's ratio or another principle from the lecture;
- name the first target that fails when reviewers drift harsh, and one monitoring measure (an audit sample, a reviewer score) that would warn you before it happens;
- check your design against the Notice and Appeal sections of the Santa Clara Principles 2.0 and Article 20 of the Digital Services Act, listing what you meet and what you do not.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Baseline and experiments (steps 1-3) | All runs recorded; ladder, crowd and correlation effects explained correctly with numbers | Runs recorded, one effect misread | Runs missing or unexplained | 20% |
| Targets and tuning (steps 4-5) | Targets set before tuning; at least eight configurations; chosen design meets targets within budget | Targets set but tuning thin, or budget exceeded | No targets, or no search | 25% |
| Robustness (step 6) | Seed range reported; harsh-drift failure identified with a monitoring measure that would catch it | Seed range or drift test missing | Neither | 15% |
| Error ratio argument | Ratio computed and defended with a stated principle, different for the two sanctions | Ratio stated, weak defence | No ratio | 20% |
| Compliance check | Every Santa Clara Notice and Appeal item and DSA Article 20 requirement addressed | Partial | Missing | 10% |
| Writing | Clear, about 500 words, numbers in every paragraph | Some paragraphs without evidence | Unclear or far off length | 10% |

<details>
<summary>Instructor check values (seed 402)</summary>

- Defaults (`n = 3`, `t = 2`, `f = 0.3`, ladder `warn,1d,7d,perm`, no appeal): 3,328 cases, conviction rate 85.8%, 2,759 correct and 96 wrongful convictions, 89 missed, 294 permanent bans of which 1 had a wrongful strike, 832 reviews a week.
- `--ladder perm`: 91 wrongful convictions, all 91 of them permanent bans of players with no rightful strike; 1,561 permanent bans in total.
- `--n 5 --t 3 --f 0.6`: conviction rate 94.7%, 334 wrongful convictions, 33 missed.
- `--n 5 --t 3 --rho 0.5`: 115 wrongful convictions, 172 missed.
- `--n 9 --t 7 --appeal`: 5 wrongful convictions, 140 missed, 1,078 appeals of which 1,074 from guilty players, 95 guilty released on appeal, about 2,628 reviews a week (over the budget).

Exact values can differ slightly across Python versions; the patterns will not.

</details>
