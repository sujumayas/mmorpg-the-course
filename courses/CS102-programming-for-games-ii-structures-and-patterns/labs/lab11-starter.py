"""CS102 Lab 11 starter: table-driven state machines.

Usage:  python lab11-starter.py            print the flag heroine's reachable states and a jump-chain log
        python lab11-starter.py --test     run the self-checks (several FAIL until you finish the lab)

Pure standard library. Python 3.10+.

What is here
  FSM                  A small table-driven machine: (state, input) -> next state, with
                       optional per-transition hooks. Works; you will extend it.
  FlagHeroine          The boolean version from the week 11 lecture. Buggy on purpose.
  reachable(make, step, key, inputs, depth)
                       Breadth-first search over every input sequence up to `depth`,
                       returning the set of distinct states reached. Use it on any design.
  JumpChain            The lecture's jump-chain model (Super Mario 64's single, double and
                       triple jump, reduced) built on FSM. Guards turn an A press into an
                       input symbol; the table stays data. Two rules are missing (TODO step 5).
"""
import sys
from collections import deque

# ---------------------------------------------------------------- generic FSM


class FSM:
    def __init__(self, start, table, hooks=None):
        """table: {(state, input): next_state}. Missing keys mean 'ignore'.
        hooks: {(from, to): callable(from, to)} run on that transition."""
        self.state = start
        self.table = table
        self.hooks = hooks or {}

    def send(self, inp):
        nxt = self.table.get((self.state, inp))
        if nxt is None:
            return False
        old, self.state = self.state, nxt
        hook = self.hooks.get((old, nxt))
        if hook:
            hook(old, nxt)
        return True


# ---------------------------------------------------------------- heroine, flag version

INPUTS = ["B", "DOWN_PRESS", "DOWN_RELEASE", "LANDED"]


class FlagHeroine:
    def __init__(self):
        self.on_ground, self.is_jumping, self.is_ducking, self.is_diving = True, False, False, False

    def handle(self, button):
        if button == "B" and self.on_ground and not self.is_jumping:
            self.is_jumping, self.on_ground = True, False
        elif button == "DOWN_PRESS":
            if self.on_ground:
                self.is_ducking = True
            else:
                self.is_diving = True
        elif button == "DOWN_RELEASE":
            self.is_ducking = False
        elif button == "LANDED" and not self.on_ground:
            self.on_ground, self.is_jumping = True, False

    def key(self):
        return (self.on_ground, self.is_jumping, self.is_ducking, self.is_diving)


def reachable(make, step, key, inputs, depth):
    """Every distinct key() reachable by any input sequence of length <= depth."""
    import copy
    start = make()
    seen = {key(start)}
    frontier = deque([(start, 0)])
    while frontier:
        obj, d = frontier.popleft()
        if d == depth:
            continue
        for inp in inputs:
            nxt = copy.deepcopy(obj)
            step(nxt, inp)
            k = key(nxt)
            if k not in seen:
                seen.add(k)
                frontier.append((nxt, d + 1))
    return seen


VALID_FLAG_KEYS = {
    (True, False, False, False),    # standing
    (False, True, False, False),    # jumping
    (True, False, True, False),     # ducking
    (False, False, False, True),    # diving
}

# TODO step 3: write StateHeroine using FSM with states standing, jumping, ducking, diving,
# and the lecture's transition table. Give it key() returning the state name.

# ---------------------------------------------------------------- jump chain

LAND_FRAMES = 4                    # frames in each landing action
CHAIN_FRAMES = {"jump_land": 5, "double_jump_land": 5, "triple_jump_land": 0}
TRIPLE_SPEED = 20.0                # forward speed must be strictly greater
AIR_FRAMES = {"jump": 20, "double_jump": 24, "triple_jump": 30}   # invented
LANDS_AS = {"jump": "jump_land", "double_jump": "double_jump_land",
            "triple_jump": "triple_jump_land"}

JUMP_TABLE = {
    ("grounded", "A"): "jump",
    ("grounded", "A_AFTER_SINGLE"): "double_jump",
    ("grounded", "A_AFTER_DOUBLE_FAST"): "triple_jump",
    ("jump_land", "A"): "double_jump",
    ("double_jump_land", "A_FAST"): "triple_jump",
    ("double_jump_land", "A_SLOW"): "jump",
}
for _air, _land in LANDS_AS.items():
    JUMP_TABLE[(_air, "TOUCHDOWN")] = _land
    JUMP_TABLE[(_land, "SETTLE")] = "grounded"
# triple_jump_land has no A row, so an A press there is ignored.


class JumpChain:
    """Frame-stepped jump chain. INCOMPLETE: the speed guard on the double-jump landing
    is missing, and a handler that switches action does not rerun in the same frame."""

    def __init__(self, speed):
        self.speed = speed
        self.fsm = FSM("grounded", JUMP_TABLE)
        self.prev_land = None      # the landing Mario settled from
        self.timer = 0             # frames left to continue the chain
        self.count = 0             # frames in the current action
        self.frame = 0
        self.log = []              # (frame, from, to)

    def _send(self, inp):
        old = self.fsm.state
        if not self.fsm.send(inp):
            return False
        self.log.append((self.frame, old, self.fsm.state))
        self.count = 0
        return True                # the action changed

    def _a_symbol(self):
        """Guards decide which input symbol an A press becomes."""
        s = self.fsm.state
        if s == "grounded" and self.timer > 0:
            if self.prev_land == "jump_land":
                return "A_AFTER_SINGLE"
            if self.prev_land == "double_jump_land" and self.speed > TRIPLE_SPEED:
                return "A_AFTER_DOUBLE_FAST"
        if s == "double_jump_land":
            return "A_FAST"        # TODO step 5: apply the speed guard here
        return "A"

    def handle(self, a):
        """One handler pass. Returns True if the action changed."""
        s = self.fsm.state
        if s in AIR_FRAMES:
            if self.count == AIR_FRAMES[s]:
                self._send("TOUCHDOWN")
                return False       # touchdown ends the frame
            self.count += 1
            return False
        if s == "grounded":
            if not a:
                return False
            sym = self._a_symbol()
            self.timer = 0
            return self._send(sym)
        self.timer = CHAIN_FRAMES[s]   # a landing frame
        self.count += 1
        if self.count >= LAND_FRAMES:
            self.prev_land = s
            return self._send("SETTLE")
        return a and self._send(self._a_symbol())

    def step(self, a):
        if self.timer > 0:
            self.timer -= 1        # counts down before any handler runs
        self.handle(a)
        # TODO step 5: while handle() reports a change, run it again this frame (cap at 4 passes).
        self.frame += 1


def run_chain(delays, speed, frames=240):
    """Press A on frame 0, then delays[i] frames after the (i+1)-th touchdown."""
    m, pressed, next_press = JumpChain(speed), 0, 0
    for f in range(frames):
        m.step(f == next_press)
        touched_down = m.log and m.log[-1][0] == f and m.log[-1][2].endswith("_land")
        if touched_down and pressed < len(delays):
            next_press = f + delays[pressed]
            pressed += 1
    return m.log


def jumps(log):
    return [(f, to) for f, _, to in log if to in AIR_FRAMES]


def tests():
    ok = True

    def check(label, cond):
        nonlocal ok
        ok &= bool(cond)
        print(("PASS " if cond else "FAIL ") + label)

    flags = reachable(FlagHeroine, FlagHeroine.handle, FlagHeroine.key, INPUTS, 6)
    check("flag heroine reaches illegal states (the bug this lab removes)", flags - VALID_FLAG_KEYS)
    sh = globals().get("StateHeroine")
    check("StateHeroine exists", sh is not None)
    if sh:
        st = reachable(sh, sh.handle, sh.key, INPUTS, 6)
        check("StateHeroine reaches exactly 4 states", st == {"standing", "jumping", "ducking", "diving"})
    check("clean triple at speed 25: jumps on frames 0, 23, 50",
          jumps(run_chain([3, 3], 25)) == [(0, "jump"), (23, "double_jump"), (50, "triple_jump")])
    window = [jumps(run_chain([d], 25))[1:2] for d in range(1, 10)]
    check("window: second press 1 to 8 frames after touchdown doubles, 9 hops",
          [w[0][1] if w else None for w in window] == ["double_jump"] * 8 + ["jump"])
    check("speed guard: 20 gives a hop at frame 50, 20.5 a triple",
          jumps(run_chain([3, 3], 20))[-1] == (50, "jump")
          and jumps(run_chain([3, 3], 20.5))[-1] == (50, "triple_jump"))
    check("triple_jump_land ignores A",
          len(jumps(run_chain([3, 3, 2], 25))) == 3)
    return ok


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.exit(0 if tests() else 1)
    flags = reachable(FlagHeroine, FlagHeroine.handle, FlagHeroine.key, INPUTS, 6)
    print(f"flag heroine: {len(flags)} reachable flag combinations (of 16), "
          f"{len(flags - VALID_FLAG_KEYS)} illegal:")
    for k in sorted(flags - VALID_FLAG_KEYS):
        print("   on_ground=%s jumping=%s ducking=%s diving=%s" % k)
    print("jump chain, presses 3 frames after each touchdown, speed 25 (starter version):")
    for row in run_chain([3, 3], 25):
        print("  ", row)
