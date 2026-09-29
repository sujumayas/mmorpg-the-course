"""Run: python test_tidi_control.py   (prints 'all lab 07 tests passed')"""
from tidi_control import (work, target_speed, next_speed, run, domain_speeds, node_speed,
                          battle, clear_time)


def near(got, want, tol, label):
    assert abs(got - want) <= tol, f"{label}: got {got}, want {want}"


near(work(500), 0.4, 1e-12, "work(500)")
near(work(2000), 4.6, 1e-12, "work(2000)")
near(target_speed(0.0, 4.6, aim=1.0), 1 / 4.6, 1e-12, "target aim=1")
near(target_speed(3.6, 4.6, aim=0.9), 0.9 / 4.6, 1e-12, "no payback ignores lag")
near(target_speed(3.6, 4.6, aim=0.9, tau=5), 0.1, 1e-12, "payback clamps to the floor")
near(target_speed(0.0, 0.4, aim=0.9), 1.0, 1e-12, "clamps to 1")
near(next_speed(1.0, 0.2, a_down=0.5, a_up=0.1), 0.6, 1e-12, "a_down used going down")
near(next_speed(0.2, 1.0, a_down=0.5, a_up=0.1), 0.28, 1e-12, "a_up used going up")

fleet = [2000] * 60
r = run(fleet, aim=1.0)
near(r["rows"][1][1], 3.6, 1e-9, "aim=1 backlog stays 3.6")
near(r["rows"][10][1], 3.6, 1e-9, "aim=1 backlog at 10 s")
near(r["game_s"], 13.8, 0.05, "aim=1 game seconds")
r = run(fleet, aim=0.9)
assert clear_time(r["rows"]) == 36, clear_time(r["rows"])
near(r["game_s"], 12.5, 0.05, "aim=0.9 game seconds")
r = run(fleet, aim=0.9, tau=5)
near(r["rows"][1][0], 0.1, 1e-12, "payback f(1)")
near(r["rows"][5][1], 1.09, 0.005, "payback lag at 5 s")
assert clear_time(r["rows"]) == 10, clear_time(r["rows"])
near(r["game_s"], 12.0, 0.05, "payback game seconds")

for kw, want in [({}, (2.93, 0.32, 0.159, 83.2)),
                 (dict(a_down=0.3, a_up=0.3), (7.63, 1.32, 0.053, 81.4)),
                 (dict(a_up=0.2), (2.93, 0.16, 0.062, 75.8)),
                 (dict(tau=None), (3.08, 0.82, 0.159, 84.1))]:
    args = dict(tau=5, noise=0.3, seed=7)
    args.update(kw)
    r = run(battle(), **args)
    got = (r["max_lag"], r["mean_lag"], r["jitter"], r["game_s"])
    for g, w, tol, lab in zip(got, want, (0.005, 0.005, 0.0005, 0.05), ("max", "mean", "jitter", "game")):
        near(g, w, tol, f"battle {kw} {lab}")

assert domain_speeds([1.0, 1.0, 0.4, 0.25], [(0, 1), (1, 2), (2, 3)]) == [0.25] * 4
assert domain_speeds([1.0, 1.0, 0.4, 0.25], [(0, 1), (2, 3)]) == [1.0, 1.0, 0.25, 0.25]
assert domain_speeds([1.0, 0.5, 1.0, 1.0, 0.2], [(0, 1), (1, 2), (2, 3)]) == [0.5, 0.5, 0.5, 0.5, 0.2]
assert domain_speeds([0.7], []) == [0.7]
near(node_speed([work(1600), work(800), 0.2], 1.0), 1 / 4.12, 1e-9, "shared node")
near(node_speed([work(1600)], 2.0), 2 / 3.04, 1e-9, "dedicated node")
near(node_speed([work(800), 0.2], 1.0), 1 / 1.08, 1e-9, "neighbour after the move")
near(node_speed([work(2000), 0.2], 1.0), 1 / 4.8, 1e-9, "the crowd moved to Y")
near(node_speed([0.2], 1.0), 1.0, 1e-12, "quiet node at full speed")
near(node_speed([work(4000)], 1.0), 0.1, 1e-12, "floor")
print("all lab 07 tests passed")
