"""CS201 Lab 10: the engine side of a scripting layer.

You write the parts marked TODO. Everything else is finished.
Run `python script_host.py` for a small demo and `python test_script_host.py` for the checks.
Standard library only.
"""
import math
import time


class BoundaryError(Exception):
    """Raised when a value is not allowed to cross the script boundary."""


# ---------------------------------------------------------------- part 1: handles (table finished, from week 5)

class HandleTable:
    """Week 5's generational handle table, finished. Scripts only ever see (index, generation) pairs."""

    def __init__(self):
        self.slots = []
        self.free = []

    def create(self, obj):
        if self.free:
            i = self.free.pop()
            self.slots[i][1] = obj
        else:
            i = len(self.slots)
            self.slots.append([0, obj])
        return (i, self.slots[i][0])

    def get(self, handle):
        """Return the object for a live handle, or None (week 5's alive check)."""
        if not (isinstance(handle, tuple) and len(handle) == 2):
            return None
        i, gen = handle
        if isinstance(i, int) and 0 <= i < len(self.slots) and self.slots[i][0] == gen:
            return self.slots[i][1]
        return None

    def destroy(self, handle):
        if self.get(handle) is None:
            return
        i = handle[0]
        self.slots[i][0] += 1
        self.slots[i][1] = None
        self.free.append(i)


def bound(table, fn):
    """Return a function that scripts call as f(handle, *args).

    It must look the handle up in `table`. If the handle is stale or malformed,
    return None without calling fn. Otherwise return fn(obj, *args).
    Any exception fn raises must propagate unchanged (run_frame deals with those).
    """
    # TODO step 1
    raise NotImplementedError


# ---------------------------------------------------------------- part 2: marshalling

def marshal(value):
    """Return a copy of value that is safe to hand to a script.

    Allowed: None, bool, int, float, str, a handle (tuple of exactly two ints),
    and lists of allowed values (copied recursively, so the script cannot
    mutate an engine list). Anything else raises BoundaryError, including
    dicts, sets, tuples that are not handles, and arbitrary objects.
    """
    # TODO step 2
    raise NotImplementedError


# ---------------------------------------------------------------- the host (finished)

class Engine:
    """Engine-owned state: positions and velocities stored per handle index."""

    def __init__(self):
        self.handles = HandleTable()
        self.pos = {}
        self.vel = {}

    def spawn(self, x, y, vx, vy):
        h = self.handles.create("mover")
        self.pos[h[0]] = [x, y]
        self.vel[h[0]] = [vx, vy]
        return h


class Host:
    """Every call from script into the engine goes through call(), which counts crossings
    and marshals arguments and results."""

    def __init__(self, engine):
        self.engine = engine
        self.crossings = 0
        self.api = {
            "get_velocity": self._get_velocity,
            "set_position": self._set_position,
            "get_velocities": self._get_velocities,
            "add_to_positions": self._add_to_positions,
        }

    def call(self, name, *args):
        self.crossings += 1
        args = [marshal(a) for a in args]
        return marshal(self.api[name](*args))

    def _alive(self, h):
        return self.engine.handles.get(tuple(h)) is not None

    def _get_velocity(self, h):
        return list(self.engine.vel[h[0]]) if self._alive(h) else None

    def _set_position(self, h, x, y):
        if self._alive(h):
            self.engine.pos[h[0]] = [x, y]

    def _get_velocities(self, hs):
        return [list(self.engine.vel[h[0]]) if self._alive(h) else None for h in hs]

    def _add_to_positions(self, hs, deltas):
        for h, d in zip(hs, deltas):
            if self._alive(h) and d is not None:
                p = self.engine.pos[h[0]]
                p[0] += d[0]
                p[1] += d[1]


def move_one(host, h, dt, known_pos):
    """The per-object script: two crossings per entity."""
    v = host.call("get_velocity", h)
    if v is None:
        return
    x, y = known_pos
    host.call("set_position", h, x + v[0] * dt, y + v[1] * dt)


# ---------------------------------------------------------------- part 3: batching

def move_batched(host, handles, dt, batch):
    """Move every entity by velocity * dt using the batched API.

    Process handles in chunks of `batch`. For each chunk, make exactly one
    `get_velocities` call and one `add_to_positions` call, so the total number
    of crossings is 2 * ceil(len(handles) / batch). Skip stale handles
    (their velocity comes back as None; pass None as their delta).
    """
    # TODO step 3
    raise NotImplementedError


def predict_frame_us(n, batch, c_cross, c_work):
    """The lecture's crossing model: T = ceil(n / batch) * c_cross + n * c_work."""
    # TODO step 4
    raise NotImplementedError


# ---------------------------------------------------------------- part 4: budgets

def run_frame(scripts, budget, errors):
    """Resume generator scripts round-robin until `budget` yields have happened
    or no scripts remain.

    - A script that yields goes to the back of the list and counts 1 toward the budget.
    - A script that finishes (StopIteration) is removed and costs nothing.
    - A script that raises any other exception is removed, costs nothing, and
      `errors` gets one string that starts with the exception's class name,
      e.g. "ZeroDivisionError: division by zero". The engine keeps running.
    Return the list of yielded values in order.
    """
    # TODO step 5
    raise NotImplementedError


# ---------------------------------------------------------------- measurement (finished)

def measure(n=20000, repeats=5):
    """Time per-object and fully batched movement on this machine. Returns (us_per_object,
    us_batched) as the best of `repeats` runs. Needs steps 1-3 done."""
    best_one, best_batch = float("inf"), float("inf")
    for _ in range(repeats):
        eng = Engine()
        hs = [eng.spawn(0.0, 0.0, 1.0, 2.0) for _ in range(n)]
        host = Host(eng)
        t0 = time.perf_counter()
        for h in hs:
            move_one(host, h, 1 / 60, eng.pos[h[0]])
        best_one = min(best_one, time.perf_counter() - t0)
        t0 = time.perf_counter()
        move_batched(host, hs, 1 / 60, n)
        best_batch = min(best_batch, time.perf_counter() - t0)
    return best_one * 1e6, best_batch * 1e6


if __name__ == "__main__":
    try:
        one, batched = measure(n=20000, repeats=3)
        print(f"20,000 movers: per-object {one / 1000:.2f} ms, one batch {batched / 1000:.2f} ms")
    except NotImplementedError:
        print("Finish steps 1-3 first, then run this file again to measure your machine.")
