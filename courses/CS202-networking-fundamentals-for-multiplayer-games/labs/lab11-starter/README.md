# Lab 11 starter

Standard library only. One file, `rewind.py`.

1. Finish the three functions marked TODO: `History.position_at`, `ray_hits_circle` and `rewind_time`.
2. `python rewind.py --check` must print `all checks passed`. The tests use the numbers from the week 11 lecture: 150 ms RTT, 100 ms interpolation, a 0.3 m hitbox and a 6 m/s target.
3. `python rewind.py --accuracy` prints the hit rate of a shooter who aims exactly at what their screen shows, with and without rewind, for RTTs from 0 to 400 ms.
4. `python rewind.py --cover` prints how long a victim with 40 ms RTT has been behind cover, on their own screen, when the kill arrives. Add `--cap 200` to limit rewind to 200 ms and watch high-ping shots get rejected.

Geometry: the shooter stands at (0, 0) facing +y. Targets move along y = 10 m. A wall hides every x > 0 for the cover test.
