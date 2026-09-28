"""CS202 Lab 04: two ways to police a client's movement, and what each lets a cheater keep.

    python movement_check.py --check             # tests your functions against the lecture
    python movement_check.py --table             # prints the lecture's section 2 table
    python movement_check.py --jitter 20 --budget 4 --cheat 2.0
                                                 # one scenario, both policies

The model is the week 4 lecture, section 2. Times in milliseconds, distances in metres.
Standard library only.

The client runs at 60 ticks per second. Each tick it produces one movement command worth
at most STEP = 0.1 m (6 m/s). It sends a packet every 3 ticks (20 packets per second).
"""
import argparse
import math

TICK_HZ = 60
TICK_MS = 1000 / TICK_HZ          # 16.67 ms
SPEED = 6.0                       # metres per second
STEP = SPEED / TICK_HZ            # 0.1 m per command
CMDS_PER_PACKET = 3
PACKET_MS = CMDS_PER_PACKET * TICK_MS   # 50 ms between packets
LATENCY_MS = 50.0                 # constant one-way delay
N_PACKETS = 200                   # 10 seconds of play
HORIZON_MS = N_PACKETS * PACKET_MS + LATENCY_MS + 60


def arrivals(n_packets, jitter_ms):
    """Arrival time of each packet at the server.

    Packet k is sent at (k + 1) * PACKET_MS, once its three commands exist, and takes
    LATENCY_MS to arrive. Every fourth packet (k % 4 == 1) is delayed by an extra
    jitter_ms. This fixed pattern stands in for jitter so you can check it by hand.
    """
    return [(k + 1) * PACKET_MS + LATENCY_MS + (jitter_ms if k % 4 == 1 else 0.0)
            for k in range(n_packets)]


# ---------------------------------------------------------------- policy A: speed check

def min_tolerance(jitter_ms):
    """Smallest tolerance (0.25 means 25%) at which an honest client never fails the
    speed check, given the arrival pattern above. Derive it from the lecture:
    the shortest gap between arrivals is PACKET_MS - jitter_ms, and in that gap the
    client claims a full PACKET_MS worth of movement. TODO."""
    raise NotImplementedError


def speed_check(arr, moves, tol):
    """Policy A. The client reports how far it moved since its last packet (moves[k],
    metres). The server accepts packet k if

        moves[k] <= SPEED * gap_k / 1000 * (1 + tol)

    where gap_k is arr[k] - arr[k - 1] (use PACKET_MS for the first packet). Accepted
    moves add to the position; rejected ones are ignored and counted as flags.
    Return (position, flags). Add 1e-9 to the right-hand side to absorb float error. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- policy B: tick budget

def tick_budget(arr, cmds, budget, horizon_ms=HORIZON_MS):
    """Policy B. The client sends commands, not positions. Packet k arrives at arr[k]
    carrying cmds[k] commands. The server ticks every TICK_MS, at TICK_MS, 2*TICK_MS, ...
    At each tick, in this order:

      1. add every packet that has arrived (arrival time <= tick time) to a queue
      2. credit = min(budget, credit + 1)
      3. run min(credit, queued) commands, subtract them from credit
      4. drop whatever is left in the queue

    Credit starts at 0. Return (commands run, commands dropped, trace), where trace is a
    list of (tick time, commands run so far). TODO."""
    raise NotImplementedError


def min_budget(jitter_ms):
    """Smallest budget at which the honest client (3 commands per packet, the arrival
    pattern above) loses no commands. Search upward from 1 with tick_budget. TODO."""
    raise NotImplementedError


# ---------------------------------------------------------------- report

def scenario(jitter_ms, tol, budget, cheat):
    arr = arrivals(N_PACKETS, jitter_ms)
    clean = arrivals(N_PACKETS, 0)      # the cheater's packets happen to arrive on time
    honest_a = speed_check(arr, [STEP * CMDS_PER_PACKET] * N_PACKETS, tol)
    smart = min(cheat, 1 + tol)         # under policy A a cheater runs exactly at the limit
    cheat_a = speed_check(clean, [STEP * CMDS_PER_PACKET * smart] * N_PACKETS, tol)
    honest_b = tick_budget(arr, [CMDS_PER_PACKET] * N_PACKETS, budget)
    cheat_b = tick_budget(clean, [round(CMDS_PER_PACKET * cheat)] * N_PACKETS, budget)
    return {
        "A honest position": honest_a[0], "A honest flags": honest_a[1],
        "A cheater position": cheat_a[0], "A cheater flags": cheat_a[1],
        "B honest position": honest_b[0] * STEP, "B honest dropped": honest_b[1],
        "B cheater position": cheat_b[0] * STEP, "B cheater dropped": cheat_b[1],
    }


def table():
    print(f"{'jitter':>6} {'min tol':>8} {'cheat m/s':>9} {'lead 10 s':>9} | "
          f"{'min B':>5} {'window':>7} {'2x cheat lead':>13}")
    for j in (0, 10, 20, 30, 40):
        tol = min_tolerance(j)
        b = min_budget(j)
        s = scenario(j, tol, b, 2.0)
        lead_a = speed_check(arrivals(N_PACKETS, 0),
                             [STEP * CMDS_PER_PACKET * (1 + tol)] * N_PACKETS, tol)[0] \
            - s["A honest position"]
        lead_b = s["B cheater position"] - s["B honest position"]
        print(f"{j:>4}ms {tol:>8.1%} {SPEED * (1 + tol):>9.1f} {lead_a:>8.1f}m | "
              f"{b:>5} {b * TICK_MS:>5.1f}ms {lead_b:>12.1f}m")


def check():
    tests = []

    def t(name, got, want, tol=1e-6):
        ok = got is not None and abs(got - want) <= tol
        tests.append((name, ok, got, want))

    try:
        t("min_tolerance(20)", min_tolerance(20), 2 / 3)
        t("min_tolerance(40)", min_tolerance(40), 4.0)
        arr = arrivals(8, 20)
        t("speed_check flags, honest, tol 0.5", speed_check(arr, [0.3] * 8, 0.5)[1], 2)
        t("speed_check flags, honest, tol 2/3", speed_check(arr, [0.3] * 8, 2 / 3)[1], 0)
        t("speed_check position, 1.6x cheater", speed_check(arrivals(8, 0), [0.48] * 8, 2 / 3)[0], 3.84)
        full = arrivals(N_PACKETS, 20)
        t("tick_budget dropped, J=20, B=3", tick_budget(full, [3] * N_PACKETS, 3)[1], 100)
        t("tick_budget dropped, J=20, B=5", tick_budget(full, [3] * N_PACKETS, 5)[1], 0)
        t("tick_budget ran, J=20, B=5", tick_budget(full, [3] * N_PACKETS, 5)[0], 600)
        t("min_budget(10)", min_budget(10), 4)
        t("min_budget(40)", min_budget(40), 6)
        s = scenario(20, 2 / 3, 5, 2.0)
        t("2x cheater lead under budget 5 (m)", s["B cheater position"] - s["B honest position"], 0.2)
    except NotImplementedError:
        print("some functions still raise NotImplementedError; finish the TODOs")
        return
    bad = [x for x in tests if not x[1]]
    for name, ok, got, want in bad:
        print(f"FAIL {name}: got {got}, want {want}")
    print("all checks passed" if not bad else f"{len(bad)} of {len(tests)} checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--jitter", type=float, default=20)
    ap.add_argument("--tol", type=float, default=None, help="default: min_tolerance(jitter)")
    ap.add_argument("--budget", type=int, default=None, help="default: min_budget(jitter)")
    ap.add_argument("--cheat", type=float, default=2.0, help="cheater speed multiplier")
    a = ap.parse_args()
    if a.check:
        check()
    elif a.table:
        table()
    else:
        tol = min_tolerance(a.jitter) if a.tol is None else a.tol
        budget = min_budget(a.jitter) if a.budget is None else a.budget
        print(f"jitter {a.jitter} ms, tolerance {tol:.1%}, budget {budget}, cheat x{a.cheat}")
        for k, v in scenario(a.jitter, tol, budget, a.cheat).items():
            print(f"  {k:<22} {v:>8.2f}")
