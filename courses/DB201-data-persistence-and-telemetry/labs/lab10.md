# DB201 · Lab 10: Tracking plan and event validator

**Week:** 10 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the SQL labs (SQL labs are 40% of the course)

**Lecture:** [Week 10, telemetry design: events and properties](../lectures/w10-telemetry-design-events-and-properties.md)

## Objective

Turn seven design questions into a tracking plan that can answer all of them, prove it with a validator, and price it. You will fix a starter plan that has the naming, cardinality and privacy mistakes from the lecture, find the errors in a sample event stream, and estimate storage per day and per year for your finished plan.

## Starter materials

All in [`lab10-starter/`](lab10-starter/):

- `tracking_plan.json`: a plan with seven questions and three events. It has deliberate problems: an event that answers nothing, a badly named event carrying a player's name, and four questions no event can answer.
- `sample_events.ndjson`: 27 events, one JSON object per line, as a collector would receive them. Seven lines are wrong in different ways.
- `validate_events.py`: checks the plan (names, types, question coverage), prints a storage estimate using the week 10 size model (28-byte row overhead, 54-byte envelope), and validates the event stream against the plan.

You need Python 3.10 or later. No packages to install. From the `lab10-starter` folder run:

```
python validate_events.py
python validate_events.py --dau 120000
```

On the starter files the validator reports 5 plan problems and 7 event problems, and prints `player_died` at 98 bytes per row, 98.0 MB per day and 35.77 GB per year at 40,000 DAU. That matches Design B in the lecture. Check it before you change anything.

## Steps

1. **Read the stream (15 min).** Open `sample_events.ndjson`. Before running the validator, find as many problems as you can by eye and list them in `RESULTS.md`. Then run the validator and compare. Which did you miss?
2. **Explain each event error (15 min).** For each of the 7 event problems, write one line in `RESULTS.md` naming the cause in the lecture's terms (missing envelope field, value baked into a name, retry duplicate, undeclared property, wrong type, and so on) and whether the fix belongs in the game code, the plan or the pipeline.
3. **Fix the plan (30 min).** Edit `tracking_plan.json` until `python validate_events.py` reports "plan OK". You must:
   - rename `PlayerLevelUp` and remove `player_name` (identify players only through the envelope);
   - make every one of Q1 to Q7 answerable, adding events and properties as needed;
   - give every event a `per_player_per_day` estimate and a one-line justification in `RESULTS.md`.
   Q2 asks for deaths **per hour played** in each zone. Deaths alone cannot answer it. Design the denominator.
4. **Price it (15 min).** Paste the storage table for 40,000 DAU and for 120,000 DAU into `RESULTS.md`. Which event dominates? What single change would cut total storage the most without losing a question?
5. **Cardinality (15 min).** Your zones are 800 m square and there are 40 of them. Choose a grid size for a death heat map that stays under 15,000 cells in total, and show the arithmetic. State where the bucketing happens (in the event or in the query) and why.
6. **Break it on purpose (at home).** Write 5 more event lines into a copy of the sample file, each violating your plan in a different way, and confirm the validator catches each. If one is not caught, extend `validate_events.py` to catch it and explain the check in two sentences.

## Deliverable

A zip or repository link with:

- your `tracking_plan.json`, passing the validator with "plan OK";
- `RESULTS.md` with steps 1 to 5, including both storage tables and the heat-map arithmetic;
- if you did step 6, your extra events file and any change to the validator;
- a memo of at most 300 words to the live producer: the three questions your plan answers that the starter plan could not, the storage cost per year at 120,000 DAU, and one question you chose **not** to support, with the reason.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Plan correctness | Validator reports "plan OK"; every question maps to the fields it needs; Q2 has a real exposure denominator; no personal data beyond the envelope id | Plan OK but one question answered only loosely, or the denominator is vague | Validator errors remain, or questions are marked answered without the needed fields | 30% |
| Error diagnosis | All 7 event errors explained with the right cause and the right place to fix | Most explained, some causes or fix locations wrong | Fewer than half explained | 20% |
| Cost model | Both storage tables, the dominant event named, and a cut that loses no question, with numbers | Tables present, reasoning thin | Missing, or numbers inconsistent with the validator | 20% |
| Cardinality | Grid size under the limit with arithmetic, bucketing placed in the query with a reason | Right grid, weak reasoning | Missing or over the limit | 15% |
| Memo | Specific, uses the student's own numbers, names a deliberate omission | Generic but correct | Missing or contradicts the plan | 15% |
