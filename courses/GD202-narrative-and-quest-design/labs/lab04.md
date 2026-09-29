# GD202 · Lab 04: Rule-based dialogue checker

**Week:** 4, dialogue systems and state flags ([lecture](../lectures/w04-dialogue-systems-and-state-flags.md)).
**Time:** 2 hours in lab, plus about 2 hours at home.
**Weight:** part of the dialogue exercises (40%). Keep the checker; it is a useful tool for week 14, narrative testing.

## Objective

Build the rule matcher from the week 4 lecture, then turn it into a checker that enumerates every state of a set of facts and reports silent states, ties and dead rules. Use the checker to write a clean rule set for an NPC of your own.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`dialogue_rules.py`](lab04-starter/dialogue_rules.py) has a `Rule` dataclass (name, list of `(fact, op, value)` conditions, line), the six barkeep rules from lecture section 2, and four empty functions: `matches`, `winners`, `all_states` and `audit`.
- [`test_rules.py`](lab04-starter/test_rules.py) holds the lecture's test values. The barkeep has 8 states, 0 silent, ties `[R1, R3]` and `[R4, R5]`, and each rule wins exactly one state alone. Adding R6 (`met` and `thief`) leaves one three-way tie. Removing R0 leaves the all-false state silent. An unused fourth flag doubles the states to 16 and the ties to 4. A rule whose conditions contradict each other is reported as dead. A New Vegas style threshold rule beats the weak fallback at 25 and loses at 24.
- The [interactive](../examples/w04-rule-matcher.html) for spot checks.

Run the tests from the repository root:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab04-starter/test_rules.py
```

On the starter every test reports `TODO` and the script exits with status 1. When all ten pass it prints `All tests pass.`

## Steps

1. **Match.** Implement `matches(rule, state)`. A rule with no conditions always matches. Numeric conditions use the `OPS` table.
2. **Pick.** Implement `winners(rules, state)`. Keep the order of `rules` in the result so ties read the same every run.
3. **Enumerate.** Implement `all_states(domains)` with `itertools.product`. Check by hand that `{"met": [F, T], "wolves": [0, 10, 20, 30]}` gives 8 states.
4. **Audit.** Implement `audit(rules, domains)`. Run `dialogue_rules.py` directly and confirm it prints 8 states, 0 silent and the two ties.
5. **Your NPC.** Choose an NPC who speaks in a place the player returns to often (a ferryman, a gate guard, a quartermaster). Define four or five facts. At least one must be a stage with gaps (0, 10, 20, 30) and at least one must be numeric (a skill, a counter or an approval value, with three to five test values). Write the fact table from lecture section 3.
6. **Write the rules.** Write 8 to 12 rules, one of them a fallback, each line one sentence of your own. Put them in a new file `my_npc.py` that imports from `dialogue_rules.py`.
7. **Clean it.** Run `audit`. Fix every silent state and every dead rule. For each tie, decide whether it is acceptable (a bark where either line fits) or must be resolved, and resolve it with a more specific rule or a changed condition. Record the audit before and after.
8. **Break the order.** Add one fact change that a designer might make late in production (a new branch that skips a stage, or a fifth flag). Rerun the audit and report what broke.

## Deliverable

`dialogue_rules.py` with all tests passing, `my_npc.py`, and a report of at most 500 words with: the fact table, the rule table, the audit output before and after step 7 (states, silent, ties, dead), your reasoning for every tie you left in, and the step 8 result.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Checker correctness | All ten tests pass; `audit` output matches the lecture | Eight or nine tests pass | Fewer than eight pass | 30% |
| Fact design | Stage with gaps and a numeric fact used well; one writer per fact stated; legal values listed | Facts work but the table is incomplete | Only booleans, or no table | 20% |
| Rule set | 8-12 rules, no silent states, no dead rules, every remaining tie justified | One silent state or dead rule left | Several problems left, or no audit | 25% |
| Writing | Lines are short, in one consistent voice, and the fallback fits every state | Voice drifts or the fallback contradicts some states | Lines copied or placeholder text | 15% |
| Late change (step 8) | Change and breakage reported with numbers and a fix proposed | Breakage reported without a fix | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- Barkeep: 8 states, `wins` = 1 for each of R0 to R5, ties `[R1, R3]` at (met, not wolves, thief) and `[R4, R5]` at the all-true state.
- With R6: ties reduce to one, `[R4, R5, R6]`; R6 wins one state alone.
- Without R0: exactly one silent state, all flags false.
- With an unused fourth flag: 16 states, 4 ties.
- A student NPC with a 4-value stage, two booleans and a numeric fact tested at 3 values has `4 × 2 × 2 × 3 = 48` states.

</details>
