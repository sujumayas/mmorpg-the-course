# MMO404 lab 09 starter

Standard library only. Run from this folder with the course Python (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `mesh.py`: the week 9 meshing model and an authority table. You write `tick_ms`, `capacity`, `servers_for`, `ghost_updates`, `spread_tick_ms`, `spread_capacity` and the `AuthorityTable` methods. The paused-server scenario, the table printer and the CSV writer are provided.
- `test_mesh.py`: checks your functions against the lecture's numbers and the fencing rules. Run `python test_mesh.py` until it prints `all lab 09 tests passed`.

Commands once the tests pass:

```
python mesh.py --table
python mesh.py --curves curves.csv
python mesh.py --pause
```
