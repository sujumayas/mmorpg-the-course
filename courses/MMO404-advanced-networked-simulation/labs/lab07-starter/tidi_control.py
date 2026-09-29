"""MMO404 lab 07 starter: a time dilation controller.

    python test_tidi_control.py          # checks your functions against the week 7 lecture
    python tidi_control.py --table       # section 2: one fleet, four controllers
    python tidi_control.py --battle      # section 3: the noisy 180-second battle
    python tidi_control.py --grid out.csv   # sweep aim and alpha_up on the noisy battle

Implement every function marked TODO. The model is in the week 7 lecture, sections 2 to 4.
Standard library only.
"""
import csv
import sys

A = 0.0003       # CPU-s per pilot per game-second
B = 0.000001     # CPU-s per pilot pair per game-second
C = 1.0          # CPU-s the node can spend per real second
FLOOR = 0.1      # slowest game speed allowed


def mulberry32(seed):
    """Seeded generator shared with the week 7 interactive. Given."""
    s = seed & 0xFFFFFFFF

    def rnd():
        nonlocal s
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((s ^ (s >> 15)) * (s | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def work(n):
    """CPU-seconds to simulate one game-second with n pilots: A*n + B*n*n. TODO."""
    raise NotImplementedError("work")


def target_speed(q, m, aim=0.9, tau=None, floor=FLOOR):
    """The controller's target: clamp((aim*C - q/tau) / m, floor, 1).
    q is the backlog (CPU-seconds owed) after this second, m the measured cost per game-second.
    tau=None means no payback term. TODO."""
    raise NotImplementedError("target_speed")


def next_speed(f, target, a_down=1.0, a_up=1.0):
    """Move f toward target by gain a_down if target < f, else a_up. TODO."""
    raise NotImplementedError("next_speed")


def run(pilots, aim=0.9, tau=None, a_down=1.0, a_up=1.0, noise=0.0, seed=7, floor=FLOOR):
    """Step the node one real second at a time, starting at f = 1 and q = 0.

    Each second, in this order (the lecture's code):
      r = rnd() from mulberry32(seed), drawn every second even when noise is 0
      m = work(n) * (1 + noise * (2r - 1))
      q = max(0, q + f*m - C)
      record (f, q)
      f = next_speed(f, target_speed(q, m, aim, tau, floor), a_down, a_up)

    Return a dict:
      "rows"      list of (f, q) as recorded
      "max_lag"   largest backlog q
      "mean_lag"  mean backlog q
      "jitter"    mean over seconds of |f_new - f| / f
      "game_s"    sum of recorded f
    TODO."""
    raise NotImplementedError("run")


def domain_speeds(needs, links):
    """Clock domains. needs[i] is the speed server i can afford alone. links is a list of
    (i, j) pairs that interact every tick. Every server runs at the minimum need in its
    connected component. Return the list of speeds. TODO."""
    raise NotImplementedError("domain_speeds")


def node_speed(loads, capacity=C, floor=FLOOR):
    """Speed of one node (section 4). loads lists W for each system the node hosts, in
    CPU-seconds per game-second; they add. Every system on the node runs at
    clamp(capacity / total, floor, 1). TODO."""
    raise NotImplementedError("node_speed")


def battle():
    """The lecture's 180-second battle. Given."""
    return [500] * 10 + [2000] * 50 + [2800] * 60 + [800] * 60


def clear_time(rows, eps=0.05):
    """First second t >= 1 with backlog below eps, or None. Given."""
    return next((t for t in range(1, len(rows)) if rows[t][1] < eps), None)


def table():
    fleet = [2000] * 60
    for name, kw in [("aim 100%", dict(aim=1.0)), ("aim 90%", dict(aim=0.9)),
                     ("aim 90%, tau 5", dict(aim=0.9, tau=5))]:
        r = run(fleet, **kw)
        rows = r["rows"]
        lags = " ".join(f"{rows[t][1]:5.2f}" for t in (1, 5, 10))
        print(f"{name:14s} f(1)={rows[1][0]:.3f} backlog@1,5,10s {lags}  "
              f"clear {str(clear_time(rows)):>4}  game-s {r['game_s']:5.1f}")


def show_battle():
    for name, kw in [("fast both ways", {}), ("slow both ways", dict(a_down=0.3, a_up=0.3)),
                     ("fast down, slow up", dict(a_up=0.2)), ("no payback term", dict(tau=None))]:
        args = dict(tau=5, noise=0.3, seed=7)
        args.update(kw)
        r = run(battle(), **args)
        print(f"{name:19s} max backlog {r['max_lag']:.2f}  mean backlog {r['mean_lag']:.2f}  "
              f"jitter {r['jitter']:.3f}  game-s {r['game_s']:.1f}")


def grid(path):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["aim", "a_up", "max_lag", "mean_lag", "jitter", "game_s"])
        for aim in (0.7, 0.8, 0.9, 1.0):
            for a_up in (0.05, 0.1, 0.2, 0.5, 1.0):
                r = run(battle(), aim=aim, tau=5, a_up=a_up, noise=0.3, seed=7)
                w.writerow([aim, a_up, round(r["max_lag"], 3), round(r["mean_lag"], 3),
                            round(r["jitter"], 4), round(r["game_s"], 2)])
    print("wrote", path)


if __name__ == "__main__":
    if "--table" in sys.argv:
        table()
    elif "--battle" in sys.argv:
        show_battle()
    elif "--grid" in sys.argv:
        grid(sys.argv[sys.argv.index("--grid") + 1])
    else:
        print(__doc__)
