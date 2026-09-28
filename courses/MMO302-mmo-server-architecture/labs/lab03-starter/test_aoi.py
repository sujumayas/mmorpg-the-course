"""Run: python test_aoi.py   (prints 'all lab 03 tests passed')"""
from aoi import (mulberry32, make_world, brute_sets, build_grid, candidates,
                 grid_count, grid_radius_sets, boundary_run)

r = mulberry32(302)
assert [round(r(), 6) for _ in range(3)] == [0.835469, 0.983486, 0.200036], "generator"

tiny = [(10, 10), (60, 10), (140, 10), (10, 95)]
g = build_grid(tiny, 50)
assert sorted(g[(0, 0)]) == [0] and sorted(g[(1, 0)]) == [1] and sorted(g[(2, 0)]) == [2], "cells"
assert sorted(candidates(g, tiny[0], 50)) == [0, 1, 3], "3x3 block around (0,0)"
assert grid_count(tiny, 50) == 8, f"tiny grid count {grid_count(tiny, 50)}"

want = {0.0: (21000, 7474), 0.10: (29826, 17138), 0.25: (80152, 69026),
        0.50: (258670, 252512), 0.75: (564926, 562266), 1.0: (999000, 999000)}
for f, (gc, rc) in want.items():
    pts = make_world(1000, f)
    assert grid_count(pts, 50) == gc, f"grid f={f}: {grid_count(pts, 50)}"
    sets = grid_radius_sets(pts, 50, 50)
    assert sum(len(s) for s in sets) == rc, f"radius f={f}"
pts = make_world(1000, 0.1)
assert grid_radius_sets(pts, 50, 50) == brute_sets(pts, 50), "narrow phase equals brute force"
assert grid_radius_sets(pts, 50, 25, k=2) == brute_sets(pts, 50), "5x5 with c = r/2 also exact"
assert grid_count(make_world(1000, 0.0), 25, k=2) == 14690, "5x5 grid count"

assert boundary_run(50, 50) == (16, 15, 303), f"no hysteresis {boundary_run(50, 50)}"
assert boundary_run(50, 52) == (16, 15, 349), "small margin"
assert boundary_run(50, 60) == (1, 0, 600), "hysteresis"
print("all lab 03 tests passed")
