# MMO405 · Lab 14: Results figure audit and research presentation

**Week:** 14 ([lecture](../lectures/w14-research-presentations.md))
**Time:** 2 hours in the lab (Parts A and B), plus a presentation slot in the week 14 session (Part C) and preparation time.
**Work mode:** individual code and figure; presentations are individual, or by paper team if your instructor approved a team paper.
**Counts toward:** methods labs (30% of the course grade). The redrawn figure and slides go straight into your final paper (50%).

## Objective

Compute what a results slide implies from its error bars, find the six invented slides whose claims do and don't match their evidence, redraw your own main figure so it can't be misread, and give a 12-minute talk built around one claim, with the people-related content cleared against your ethics approval.

## Starter materials

- [`lab14-starter/error_bars.py`](lab14-starter/error_bars.py), Python 3, standard library only. It loads the slides and has three stubs:
  - `se_from_bar` (TODO 1), recovering a mean's standard error from an SE, 95% CI or SD bar.
  - `diff_test` (TODO 2), the independent and paired tests of a difference from lecture section 2.
  - `audit_slide` (TODO 3), which returns what a slide looks like, the p-value of the comparison its claim is about, and whether the claim holds.
- [`lab14-starter/slides.json`](lab14-starter/slides.json), six invented results slides from fictional online-game studies. Each has a title, the bar type and arms as drawn, group sizes, and the speaker's claim.
- [`lab14-starter/test_error_bars.py`](lab14-starter/test_error_bars.py) has twelve tests. All fail on the starter and pass on a correct solution. Run them from inside `lab14-starter/` with `python -m unittest test_error_bars.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w14-error-bar-reading.html`](../examples/w14-error-bar-reading.html), once it is built.
- Your final-paper draft, its main result, and your ethics approval (week 10).

## Steps

### Part A: audit six slides (50 min)

1. Implement `se_from_bar` and `diff_test` (TODOs 1 and 2) and run their tests. Use `diff_test` to reproduce every row of the lecture's table.
2. Implement `audit_slide` (TODO 3), run all twelve tests, then run `python error_bars.py`.
3. For each of the six slides, write two lines in a results sheet: what a typical audience would conclude from the picture, and what the test says. Use week 2's four verdicts where you can: for slides 1, 2 and 6, propose a SESOI in the slide's natural units and classify the result.
4. Rewrite the title of every slide whose claim is not supported so that it states what the evidence shows, with the number. For slide 5, rewrite it about the difference between the two groups.
5. Slide 3 is paired. Find the correlation between weeks below which its claim ("did not change") would become the weak two-verdict reading's "not significant." Explain in two sentences why even then the title would still overstate the evidence.

### Part B: redraw your own figure (40 min)

6. Take the main quantitative result of your final paper. Draw it as you currently have it, then redraw it following the lecture's section 3 checklist (title as claim with the number, natural units, labelled interval, the comparison drawn, n and unit of analysis, SESOI or reference line, readable and color-safe). If your main result is qualitative, build the evidence slide from section 3 instead: a theme with three pseudonymized excerpts, one of which complicates it.
7. Run your figure's numbers through `diff_test` (or explain why your analysis needs a different test, such as a regression or a multilevel model, and report its interval instead).
8. Fill in the people check: list every screenshot, quote, character, guild or server name and network figure in your slides, and for each say what your approval allows and what you did (cropped, redrawn, paraphrased, consent obtained, suppressed).

### Part C: present (in the week 14 session)

9. Give a 12-minute talk with the structure from lecture section 1, followed by 5 minutes of questions. Your slide titles must read as your argument on their own. Bring the claim sentence on a card; you will be asked to read it before you start.
10. Peer-review two classmates' talks with the form below. Hand your forms in at the end of the session. Your instructor passes them on anonymously.

**Peer review form (one per talk).**

| Question | Your answer |
|---|---|
| The claim in one sentence, as you understood it | |
| Its claim type (descriptive, associational, causal, interpretive) | |
| The main figure: what quantity, what interval, what n | |
| One thing the figure did not let you tell | |
| The strongest alternative explanation the speaker addressed, or should have | |
| One change that would most improve the talk | |

## Deliverable

- `error_bars.py` passing all twelve tests.
- A results sheet (two pages at most) with your answers to steps 3 to 5.
- Before and after versions of your main figure, with the output from step 7 and the people check from step 8.
- Your slides (PDF) and the two peer review forms you wrote.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (TODOs 1-3) | All tests pass; lecture table reproduced | Tests pass, table incomplete | Tests fail | 15 |
| Slide audit (steps 3-5) | Every slide's picture and test contrasted; SESOIs sensible; rewritten titles state the evidence; slide 3 threshold computed and interpreted | Most slides right, titles vague | Missing | 20 |
| Own figure (steps 6-7) | Meets all seven checklist items; the comparison and its interval are the evidence | Meets most items; comparison left to the viewer | Unlabelled bars or no interval | 20 |
| People check (step 8) | Every item listed and matched to the approval; no identifying content left | Items listed, some decisions unexplained | Missing, or identifying content remains | 10 |
| Talk (step 9) | One claim, stated at start and end; titles carry the argument; on time; design and limitations explained; questions answered with the design | Clear but over time, or claim drifts | No clear claim | 25 |
| Peer reviews (step 10) | Both forms specific and constructive | Forms complete but generic | Missing | 10 |
| **Total** | | | | **100** |
