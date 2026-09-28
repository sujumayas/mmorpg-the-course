"""MMO302 lab 12 starter: time dilation on one overloaded node.

Standard library only.
  python tidi.py               prints the battle summary for both modes
  python -m unittest test_tidi.py

The model is the lecture's (section 2):
  work(n)   = A*n + B*n*n      CPU-seconds needed to simulate one game-second
  speed f   = clamp(C / work(n), FLOOR, 1)
The simulation steps one real second at a time.
"""
import csv

A = 0.0003       # CPU-s per pilot per game-second
B = 0.000001     # CPU-s per pilot pair per game-second
C = 1.0          # CPU-s the node can spend per real second
FLOOR = 0.1      # slowest game speed allowed


def work(n):
    """CPU-seconds to simulate one game-second with n pilots on the node."""
    # TODO
    raise NotImplementedError("work")


def dilation(n):
    """Game speed f for n pilots: C / work(n), clamped to [FLOOR, 1]."""
    # TODO
    raise NotImplementedError("dilation")


def load_timeline(path="battle.csv"):
    """Return pilots on the node for each real second, from a CSV of (minute, pilots).
    Each row's count holds until the next row; the last row lasts one minute."""
    rows = [(int(r["minute"]), int(r["pilots"])) for r in csv.DictReader(open(path))]
    out = []
    for (m, n), nxt in zip(rows, rows[1:] + [(rows[-1][0] + 1, None)]):
        out += [n] * ((nxt[0] - m) * 60)
    return out


def simulate(pilots_per_second, mode):
    """Step the node through the timeline one real second at a time.

    mode "none": the node tries to run at full speed (f = 1).
    mode "tidi": the node runs at f = dilation(n).

    Each real second:
      demand   = f * work(n)                 CPU-seconds of simulation requested
      backlog  = max(0, backlog + demand - C) CPU-seconds of work not yet done
      game    += f                           game-seconds that pass
      delay    = backlog / C + 1 / f         real seconds before a command issued now
                                             takes effect (clear the backlog, then one tick)

    Return a dict with keys:
      "real_s"       number of real seconds simulated
      "game_s"       game-seconds that passed
      "max_backlog"  largest backlog seen (CPU-seconds)
      "max_delay"    largest delay seen (real seconds)
      "end_backlog"  backlog after the last second
    """
    # TODO
    raise NotImplementedError("simulate")


if __name__ == "__main__":
    timeline = load_timeline()
    for mode in ["none", "tidi"]:
        try:
            r = simulate(timeline, mode)
        except NotImplementedError as e:
            print(f"{mode}: not run yet ({e})")
            continue
        print(f"{mode:>4}: {r['real_s']} real s, {r['game_s']:.0f} game s, "
              f"max backlog {r['max_backlog']:.0f} CPU-s, max delay {r['max_delay']:.1f} s, "
              f"backlog at end {r['end_backlog']:.0f} CPU-s")
