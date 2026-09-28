"""CS202 Lab 09: client-side prediction and server reconciliation, in one file.

    python netsim.py --check                     # tests your client against the lectures
    python netsim.py --mode dumb                 # no prediction
    python netsim.py --mode naive                # predict, then snap to every snapshot
    python netsim.py --mode reconcile            # predict, snap, replay pending inputs
    python netsim.py --mode reconcile --smooth 0.1 --rtt 150 --loss 0.05 --csv out.csv
    python netsim.py --mode reconcile --no-snare --input-loss 0.05   # no input redundancy

The world is one axis. The player walks at 6 m/s (0.1 m per 60 Hz tick). A scripted
player holds "right" for 2 s and then lets go. At 1.0 s of server time an enemy snares
the player: the next 60 inputs the server processes move at half speed. The client does
not know about the snare until a snapshot tells it. Weeks 8 and 9 of the lecture.
Standard library only.
"""
import csv
import random
import sys

TICK = 1 / 60          # s, the shared fixed timestep (CS101 week 9)
SPEED = 6.0            # m/s
SNARE_FACTOR = 0.5
SNARE_INPUTS = 60
SNAPSHOT_EVERY = 3     # server ticks per snapshot: 20 Hz


# ---------- shared movement code: client and server run exactly this ----------

def step(state, seq, move):
    """Advance one tick. state: dict with x, snare_from, snare_to (input sequence numbers,
    snare applies when snare_from <= seq < snare_to). move is -1, 0 or +1. Returns new state."""
    speed = SPEED * (SNARE_FACTOR if state["snare_from"] <= seq < state["snare_to"] else 1.0)
    new = dict(state)
    new["x"] = round(state["x"] + move * speed * TICK, 9)
    return new


def new_state():
    return {"x": 0.0, "snare_from": 0, "snare_to": 0}


# ---------- the client (your work: three TODOs) ----------

class Client:
    def __init__(self, mode, smooth=0.0):
        self.mode = mode              # "dumb", "naive" or "reconcile"
        self.smooth = smooth          # seconds over which a correction fades (0 = snap)
        self.state = new_state()      # predicted state (or last server state in dumb mode)
        self.pending = []             # (seq, move) not yet acknowledged by the server
        self.error = 0.0              # display offset still being smoothed away
        self.error_t = 0.0            # seconds since the offset was set
        self.error0 = 0.0

    def on_input(self, seq, move):
        """Called every tick with this tick's input, after it has been sent."""
        # TODO (week 8): in "dumb" mode do nothing. Otherwise remember (seq, move) in
        # self.pending and advance self.state with the shared step().
        raise NotImplementedError("Client.on_input")

    def on_snapshot(self, snap):
        """snap: dict with x, snare_from, snare_to, ack (last input seq the server ran).
        Returns the size of the jump in the *predicted* position, in metres."""
        # TODO (week 9):
        # 1. drop pending inputs with seq <= snap["ack"] (every mode)
        # 2. "dumb" and "naive": state = the server's state
        #    "reconcile": state = the server's state, then replay the pending inputs
        # 3. jump = new predicted x - old predicted x
        # 4. if self.smooth > 0 and the jump is not zero: set self.error0 to
        #    self.displayed_offset() - jump and self.error_t to 0
        # return jump
        raise NotImplementedError("Client.on_snapshot")

    def displayed_offset(self):
        # TODO (week 9): the linear fade error0 * (1 - error_t / smooth), and 0 when
        # smoothing is off or the fade has finished.
        return 0.0

    def advance_display(self, dt):
        self.error_t += dt

    def displayed_x(self):
        return self.state["x"] + self.displayed_offset()


# ---------- the server and the network (given) ----------

class Server:
    def __init__(self, snare_at):
        self.state = new_state()
        self.ack = 0
        self.snare_at = snare_at      # server time in s when the snare lands (None = never)

    def run_input(self, now, seq, move):
        if self.snare_at is not None and now >= self.snare_at and self.state["snare_to"] == 0:
            self.state["snare_from"], self.state["snare_to"] = seq, seq + SNARE_INPUTS
        self.state = step(self.state, seq, move)
        self.ack = seq

    def snapshot(self):
        return dict(self.state, ack=self.ack)


def script(tick):
    """Hold right for 2 s (120 ticks), then release."""
    return 1 if tick < 120 else 0


def run(mode, rtt_ms=150, loss=0.0, smooth=0.0, seconds=3.0, snare_at=1.0, seed=1, input_loss=0.0):
    """Simulate. Inputs are sent every tick and snapshots every 3 ticks. Each direction
    takes rtt/2. A message arriving between ticks is handled on the next tick.
    Snapshots are lost with probability `loss`. Inputs are assumed to be sent redundantly
    (week 6), so none is lost, unless you set `input_loss` to model a client without
    redundancy. Returns a list of per-tick rows."""
    rng, rng_in = random.Random(seed), random.Random(seed + 7)
    one_way = rtt_ms / 2000
    client, server = Client(mode, smooth), Server(snare_at)
    to_server, to_client = [], []           # (arrival time, payload)
    rows = []
    for tick in range(int(seconds * 60) + 1):
        now = tick * TICK + 1e-9
        # server: run inputs that have arrived, in order
        for t, (seq, move) in sorted(m for m in to_server if m[0] <= now):
            server.run_input(now, seq, move)
        to_server = [m for m in to_server if m[0] > now]
        if tick % SNAPSHOT_EVERY == 0 and rng.random() >= loss:
            to_client.append((now + one_way, server.snapshot()))
        # client: snapshots that have arrived
        jump = 0.0
        client.advance_display(TICK)
        for t, snap in sorted((m for m in to_client if m[0] <= now), key=lambda m: m[0]):
            jump += client.on_snapshot(snap)
        to_client = [m for m in to_client if m[0] > now]
        # client: sample and send this tick's input (seq starts at 1), then predict
        seq, move = tick + 1, script(tick)
        if rng_in.random() >= input_loss:
            to_server.append((now + one_way, (seq, move)))
        client.on_input(seq, move)
        rows.append({"tick": tick, "ms": round(tick * TICK * 1000, 1),
                     "server_x": round(server.state["x"], 3),
                     "predicted_x": round(client.state["x"], 3),
                     "shown_x": round(client.displayed_x(), 3),
                     "jump": round(jump, 3), "pending": len(client.pending)})
    return rows


def first_move_ms(rows):
    return next(r["ms"] for r in rows if r["shown_x"] > 0)


def biggest_jump(rows):
    return max((abs(r["jump"]), r["ms"]) for r in rows)


def biggest_shown_step(rows):
    """Largest change in the displayed position between two frames, in metres."""
    return max(abs(b["shown_x"] - a["shown_x"]) for a, b in zip(rows, rows[1:]))


def biggest_backstep(rows):
    """Largest backward move of the displayed position between two frames (0 if none)."""
    return max(0.0, max(a["shown_x"] - b["shown_x"] for a, b in zip(rows, rows[1:])))


def report(rows, mode):
    j, at = biggest_jump(rows)
    moving = [r["pending"] for r in rows if 30 <= r["tick"] < 120]
    print(f"mode {mode}: first visible move {first_move_ms(rows):.1f} ms after the key press")
    print(f"  biggest correction {j:.3f} m at {at:.1f} ms; biggest on-screen step {biggest_shown_step(rows):.3f} m,"
          f" biggest backward step {biggest_backstep(rows):.3f} m")
    print(f"  jumps over 1 cm: {sum(1 for r in rows if abs(r['jump']) > 0.01)}")
    if moving and mode != "dumb":
        print(f"  pending inputs while walking: {min(moving)} to {max(moving)}")
    print(f"  final x: server {rows[-1]['server_x']}, shown {rows[-1]['shown_x']}")


def check():
    try:
        _check()
    except NotImplementedError as e:
        print(f"TODO: implement {e} first")


def _check():
    dumb = run("dumb")
    naive = run("naive", snare_at=None)
    rec0 = run("reconcile", snare_at=None)
    rec = run("reconcile")
    sm = run("reconcile", smooth=0.1)
    expect = {
        "dumb: first visible move (ms)": (first_move_ms(dumb), 183.3),
        "reconcile: first visible move (ms)": (first_move_ms(rec), 0.0),
        "naive, no snare: biggest jump (m)": (biggest_jump(naive)[0], 0.5),
        "reconcile, no snare: biggest jump (m)": (biggest_jump(rec0)[0], 0.0),
        "reconcile, snare: biggest jump (m)": (biggest_jump(rec)[0], 0.5),
        "reconcile, snare: backward step (m)": (biggest_backstep(rec), 0.45),
        "smoothed 0.1 s: backward step (m)": (round(biggest_backstep(sm), 3), 0.034),
        "final x agrees (m)": (rec[-1]["shown_x"], rec[-1]["server_x"]),
    }
    bad = []
    for k, (got, want) in expect.items():
        ok = abs(got - want) < 1e-3
        bad += [] if ok else [k]
        print(f"  {k:<40} got {got:<8} want {want}")
    print("all checks passed" if not bad else f"check these: {bad}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--check":
        check()
        sys.exit()
    opt = lambda k, d: type(d)(a[a.index(k) + 1]) if k in a else d
    mode = opt("--mode", "reconcile")
    try:
        rows = run(mode, rtt_ms=opt("--rtt", 150.0), loss=opt("--loss", 0.0),
               smooth=opt("--smooth", 0.0), snare_at=None if "--no-snare" in a else 1.0,
               seed=opt("--seed", 1), input_loss=opt("--input-loss", 0.0))
    except NotImplementedError as e:
        sys.exit(f"TODO: implement {e} first")
    report(rows, mode)
    if "--csv" in a:
        with open(opt("--csv", "out.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
