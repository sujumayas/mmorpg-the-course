# MMO404 lab 07 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `tidi_control.py`: the week 7 dilation controller. You write `work`, `target_speed`, `next_speed`, `run`, `domain_speeds` and `node_speed`. The seeded generator, the battle timeline, the table printers and the CSV sweep are provided.
- `test_tidi_control.py`: checks your functions against every number in the lecture's sections 2 to 4. Run `python test_tidi_control.py` until it prints `all lab 07 tests passed`.

Commands once the tests pass:

```
python tidi_control.py --table
python tidi_control.py --battle
python tidi_control.py --grid grid.csv
```
