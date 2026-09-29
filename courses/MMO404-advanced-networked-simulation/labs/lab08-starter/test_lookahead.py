"""Run: python test_lookahead.py   (prints 'all lab 08 tests passed')"""
from lookahead import (finish_times, effective_tick, stalls, smallest_lookahead,
                       border_lookahead, random_ticks, ABILITIES)


def near(got, want, tol, label):
    assert abs(got - want) <= tol, f"{label}: got {got}, want {want}"


xa, xb = [40, 60] * 50, [60, 40] * 50
fa, fb = finish_times(xa, xb, 1, 0)
assert fa[:4] == [40, 120, 160, 240] and fb[:4] == [60, 100, 180, 220], (fa[:4], fb[:4])
fa, fb = finish_times(xa, xb, 2, 0)
assert fa[:4] == [40, 100, 140, 200] and fb[:4] == [60, 100, 160, 200], (fa[:4], fb[:4])
fa, fb = finish_times(xa, xb, 2, 60)
assert fa[:4] == [40, 100, 160, 220], fa[:4]
for L, d, want in [(1, 0, 60.0), (2, 0, 50.0), (1, 20, 79.8), (2, 20, 50.0), (2, 60, 55.0)]:
    near(effective_tick(xa, xb, L, d), want, 1e-9, f"pattern L={L} d={d}")
near(effective_tick([30, 70] * 50, [70, 30] * 50, 1, 0), 70.0, 1e-9, "check-this-example 1")
sa, sb = stalls(xa, xb, 1, 0)
assert (sa, sb) == (1000, 980), (sa, sb)   # A stalls on ticks 2, 4, ..., 100; B on 3, 5, ..., 99
assert stalls(xa, xb, 2, 0) == (0, 0)

rx, ry = random_ticks()
for L, w20, w60 in [(1, 72.4, 111.0), (2, 51.7, 58.8), (3, 50.8, 51.4), (4, 50.5, 50.7)]:
    near(effective_tick(rx, ry, L, 20), w20, 0.05, f"random L={L} d=20")
    near(effective_tick(rx, ry, L, 60), w60, 0.05, f"random L={L} d=60")
assert smallest_lookahead(rx, ry, 20) == 2
assert smallest_lookahead(rx, ry, 60) == 3
assert smallest_lookahead([50] * 10, [50] * 10, 0) == 1

assert border_lookahead([ABILITIES["melee, next tick"]]) == 1
assert border_lookahead([ABILITIES["arrow, 5 m minimum at 50 m/s"]]) == 2
assert border_lookahead([1.0]) == 20
assert border_lookahead([1.5]) == 30
assert border_lookahead([0.4, 1.5]) == 8
assert border_lookahead([0.01]) == 1
assert border_lookahead(list(ABILITIES.values())) == 1
print("all lab 08 tests passed")
