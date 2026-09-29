# MMO404 lab 08 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `lookahead.py`: the week 8 two-server model. You write `finish_times`, `effective_tick`, `stalls`, `smallest_lookahead` and `border_lookahead`. The seeded generator, the random tick lists, the lecture's ability table and the printers are provided.
- `test_lookahead.py`: checks your functions against every number in the lecture's section 2. Run `python test_lookahead.py` until it prints `all lab 08 tests passed`.

Commands once the tests pass:

```
python lookahead.py --pattern
python lookahead.py --random
python lookahead.py --smallest
python lookahead.py --abilities
```
