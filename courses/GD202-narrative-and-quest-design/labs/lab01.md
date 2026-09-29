# GD202 · Lab 01: Plot order audit

**Week:** 1, story vs narrative vs plot ([lecture](../lectures/w01-story-vs-narrative-vs-plot.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** dialogue exercises (40% of the course, shared across the exercise labs).

## Objective

Measure how a shipped game orders its backstory for you, then design two plot orders for a backstory of your own and defend each by the effect it produces. By the end you should be able to look at any quest or level and say which layer (story, plot, narration, play story) a problem lives in.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python, run with the program's `.venv/bin/python`.

- [`plot_order.py`](lab01-starter/plot_order.py), a skeleton with a CSV loader and four empty functions: `validate`, `inversions`, `scramble` and `open_questions`.
- [`sample_log.csv`](lab01-starter/sample_log.csv), the lecture's "mystery" telling of the lighthouse story as a discovery log. Use it as a format example.
- [`test_plot_order.py`](lab01-starter/test_plot_order.py), tests built from the lecture's values: the four tellings give `I = 0, 5, 15, 28`; `[3, 1, 2, 6, 4, 5]` gives `S = 4/15`; two different orders both give `I = 7`; the open-questions profile of the in medias res telling is `[1, 1, 1, 1, 1, 0, 0, 0]`. The tests fail on the starter and pass once your functions are correct.
- The [interactive](../examples/w01-plot-order.html), for checking hand counts.

Run the tests from inside the starter folder:

```
cd courses/GD202-narrative-and-quest-design/labs/lab01-starter
../../../../.venv/bin/python test_plot_order.py
```

## Steps

1. **Code (40 min).** Implement the four functions. Run the tests until all six pass. Then run `plot_order.py` with no arguments and confirm it prints `inversions: 15` and `scramble: 0.54` for the sample log.
2. **Pick a game (10 min).** Choose a game with a backstory you learn in pieces: notes, logs, flashbacks, item text, environmental clues. Short is better. A one-hour section of a longer game is fine. Name the game and the version or platform you played.
3. **Play and log (40 min).** Play the section. Each time you learn a backstory event, write it down in a CSV with columns `plot_position,story_number,label`. Leave `story_number` blank while you play.
4. **Reconstruct the story (15 min).** After playing, sort your events into the order they happened in the fiction and fill in `story_number`. Where the game leaves the order ambiguous, pick one and note it. Keep between 8 and 15 events.
5. **Measure (10 min).** Run `plot_order.py your_log.csv`. Record `I`, `S` and the open-questions profile. Mark the plot position where the most questions are open at once.
6. **Diagnose the channels (20 min).** For each event, record the narration channel (cutscene, dialogue, text in the world, environment, systemic) and whether a player could miss it. For any missable event, state which inversion would stay unresolved if a player missed it.
7. **Design (at home).** Write an original 8 to 10 event backstory for a small quest location. No existing characters or settings. Produce two plot orders: one built for suspense and one built for surprise. Compute `I`, `S` and the open-questions profile for each.
8. **Justify (at home).** For each of your two orders, write one paragraph explaining how the position of its inversions produces the intended effect. Refer to specific event numbers.

## Deliverable

A single PDF or Markdown file, at most 1,000 words plus tables, containing:

- Your completed `plot_order.py` (or a link to it) with all tests passing.
- The game log CSV with `I`, `S`, the open-questions profile and the channel table from step 6.
- A 200-word diagnosis of the game's plot order: where it creates curiosity, and where (if anywhere) it risks losing the player.
- Your original backstory, both plot orders with their numbers, and the two justification paragraphs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All six tests pass; functions readable | Tests pass with hard-coded or unclear logic | Tests fail | 20% |
| Game log and measurement | 8-15 events, story order justified, numbers correct, peak of open questions identified | Log complete, minor counting errors or ambiguities unexplained | Too few events or numbers wrong | 20% |
| Channel diagnosis | Every missable event tied to a specific unresolved inversion | Channels listed, links to inversions partial | Channels missing | 20% |
| Original plot orders | Two orders that clearly produce suspense and surprise, with correct numbers | Orders differ but the intended effects are weak or confused | One order, or effects not distinguishable | 25% |
| Writing | Specific, refers to event numbers, uses the four-layer terms correctly | Mostly clear, some terms mixed up | Vague or uses "story" for every layer | 15% |
