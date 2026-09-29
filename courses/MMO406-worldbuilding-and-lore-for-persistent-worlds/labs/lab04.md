# MMO406 · Lab 04: The lore clock and the timeline checker

**Week:** 4, history and timelines ([lecture](../lectures/w04-history-and-timelines.md)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the exercises (40%). The history you write here becomes the history chapter of your world bible.

## Objective

Implement the week 4 lore clock and a checker that catches impossible timeline rows. Then write a three-era history for your own world, pick a ten-year clock policy for its live years, and prove with the checker and the clock that both hold together.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`lore_clock.py`](lab04-starter/lore_clock.py) has the model in its docstring and three empty functions: `world_year`, `clock_summary` and `check_timeline`.
- [`thornmere.py`](lab04-starter/thornmere.py) holds a sample timeline for the lecture's invented world: three eras, five people, ten events, and exactly four planted problems.
- [`test_lore_clock.py`](lab04-starter/test_lore_clock.py) holds the test values. The four clock policies of the lecture table at `t = 10` (span 0, 2.5, 10, 12; density 60, 24, 6, 5; Ysolde's age 16, 18.5, 26, 28). A jump counts only once its expansion has shipped (`t = 4.9` gives one jump at `T = 2.5`, `t = 5.0` gives two). Check-yourself question 1 (span 10.5, age 40.5). The four planted problems in the sample timeline. Birth and death years are allowed; era ranges are inclusive.
- The [interactive](../examples/w04-lore-clock.html), for checking your clock by eye.

Run the tests from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab04-starter/test_lore_clock.py
```

On the starter all six tests report `TODO` and the script exits with status 1.

## Steps

1. **Clock.** Implement `world_year` and `clock_summary`. Watch the jump term. `floor(t / T)` counts expansions already shipped, and there is no jump term when `T` is `None`.
2. **Checker.** Implement `check_timeline`. It returns a sorted list of `(event_id, code)` pairs with the four codes described in the docstring. Run `lore_clock.py` and confirm it prints the four planted problems in `thornmere.py`.
3. **Your eras.** For your own world (the one you started in weeks 1 to 3), write three to five eras before the present. For each, write its date range at the precision the lecture's gradient allows, one sentence on its defining condition, and one item each "in the ground", "in the living" and "in the dark".
4. **Your timeline.** Write at least 25 events across the eras as a Python file in the same format as `thornmere.py`, with at least eight named people. Include the "public or secret" and "referenced by" columns from lecture section 4 as extra keys; the checker ignores keys it does not use. Run the checker until it reports nothing.
5. **Break it on purpose.** Hand your file to a classmate. They plant three errors without telling you where. Find them with the checker, and write down any error the checker could not catch (for example, a secret that an NPC knows too early). Propose one new check that would catch it.
6. **Your clock.** Choose `r`, `J` and `T` for your game's first ten live years and a realistic beat rate `E`. Report the span, time gap, density and the age of your youngest important character at years 2, 5 and 10.
7. **Defend it.** In at most 300 words, argue for your clock policy using the numbers from step 6. Say what your launch zones will claim about their date for a player who starts at year 5, and which characters you will allow to age.

## Deliverable

`lore_clock.py` with all tests passing; your timeline file; a report of at most 900 words containing the era table (step 3), the checker output before and after step 5 with your proposed extra check, the clock table (step 6), and the defence (step 7).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Clock and checker correctness | All six tests pass; checker handles multiple problems per event | Four or five pass | Three or fewer | 25% |
| Era design | Every era has all three items; "in the dark" questions could each carry an expansion; precision falls with distance | One or two eras thin or overly precise | Eras are lists of dates with no content hooks | 25% |
| Timeline quality | 25+ events, 8+ people, clean checker run, reference column filled | Meets counts but thin references | Below counts or fails checker | 15% |
| Break-it analysis | Found all planted errors; a sensible new check proposed for what the tool missed | Found errors, no new check | Did not find errors | 15% |
| Clock policy defence | Numbers used to argue; time gap addressed for a year-5 starter; ageing rule stated | Numbers reported but argument generic | No numbers or no policy | 20% |

<details>
<summary>Instructor check values</summary>

- `world_year(10, 1200, 0, 3, 2.5)` is 1212; `world_year(4.9, 0, 0, 3, 2.5)` is 3.
- `clock_summary(9, 400, 0.5, 2, 3, E=8, a0=30)` gives span 10.5, gap 10.5, density `72 / 10.5 ≈ 6.857`, age 40.5.
- Planted problems in `thornmere.py`: E04 dated 985 but filed under Twin Crowns (640 to 911); E06 has Brother Caddoc acting in 1181, two years after his death; E09 has Queen Adelmar acting in 1140, two years before her birth; E10 names Lord Fenwick, who is not in the people list.
- Common student bug: counting a jump at `t = 0` or using `round` instead of `floor`. The `t = 4.9` test catches `round`.
- Typical missed error in step 5: an event marked secret whose participants include a character who later "reveals" it in dialogue dated earlier. A good proposed check compares "who knows" against the dates of dialogue references.

</details>
