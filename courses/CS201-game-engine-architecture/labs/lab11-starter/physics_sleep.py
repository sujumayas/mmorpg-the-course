"""CS201 Lab 11: islands, sleep and a safe event queue.

You write the parts marked TODO. Everything else is finished.
Run `python physics_sleep.py` to print the lecture's stack table once your code works,
and `python test_physics_sleep.py` for the checks. Standard library only.
"""
import math

HZ = 60


# ---------------------------------------------------------------- part 1: islands

def build_islands(n, contacts, static=frozenset()):
    """Group bodies 0..n-1 into islands.

    contacts: iterable of (a, b) pairs of touching bodies.
    static:   set of static body ids. Static bodies never join an island and
              never connect two islands (two crates on one floor stay separate).
    Return a list of islands, each a sorted list of body ids, sorted by first id.
    Static bodies appear in no island. Every dynamic body appears in exactly one.
    Use union-find (disjoint sets) so the cost is close to linear in contacts.
    """
    # TODO step 1
    raise NotImplementedError


# ---------------------------------------------------------------- part 2: the sleep rule

def sleep_time_alone(v0, k, v_sleep, t_sleep):
    """Seconds until a body with speed v0 * exp(-k t) can sleep on its own:
    ln(v0 / v_sleep) / k + t_sleep, or just t_sleep if v0 is already below v_sleep."""
    # TODO step 2
    raise NotImplementedError


class SleepSystem:
    """Still-timers per body, island sleep, and wake-on-touch."""

    def __init__(self, n, v_sleep=0.05, t_sleep=0.5, hz=HZ):
        self.n = n
        self.v_sleep = v_sleep
        self.need = round(t_sleep * hz)     # ticks of stillness needed
        self.timers = [0] * n
        self.asleep = [False] * n

    def tick(self, speeds, contacts, static=frozenset()):
        """Advance one physics tick.

        speeds:   list of n speeds this tick (a sleeping body's entry is ignored).
        contacts: touching pairs this tick.
        Rules, in this order:
        1. Build islands from contacts (static bodies excluded).
        2. Wake: if an island contains at least one sleeping body and at least one
           awake body, every body in it wakes up with its timer reset to 0.
        3. For each awake body: timer += 1 if speed < v_sleep, else timer = 0.
        4. For each island whose bodies are all awake and all have timer >= need,
           put every body in it to sleep.
        Return the number of awake dynamic bodies after the tick.
        """
        # TODO step 3
        raise NotImplementedError


# ---------------------------------------------------------------- part 3: events

class World:
    """A toy physics world that refuses changes while it is stepping."""

    def __init__(self, health):
        self.health = dict(health)          # body id -> hit points
        self.locked = False
        self.events = []

    def destroy(self, body):
        if self.locked:
            raise RuntimeError("world is locked during step")
        del self.health[body]

    def step(self, pairs, on_contact=None):
        """Record contact events. If on_contact is given, call it for each pair
        during the step (the unsafe callback style)."""
        self.locked = True
        self.events = []
        try:
            for a, b in pairs:
                self.events.append((a, b))
                if on_contact:
                    on_contact(self, a, b)
        finally:
            self.locked = False


def process_contacts(world, damage):
    """After world.step(): every body in every event loses `damage` hit points per
    event it appears in. Bodies at or below 0 are destroyed after all damage is
    applied, each exactly once, in ascending id order. Return the sorted list of
    destroyed ids. Must not raise, even if a body appears in several events."""
    # TODO step 4
    raise NotImplementedError


# ---------------------------------------------------------------- driver (finished)

def settle(v0s, floors, k=2.0, v_sleep=0.05, t_sleep=0.5, max_s=10, stacks=1):
    """Simulate `stacks` identical stacks (each a chain of touching bodies) settling.
    Returns the list of awake-body counts, one per tick."""
    per = len(v0s)
    n = per * stacks
    contacts = [(s * per + i, s * per + i + 1) for s in range(stacks) for i in range(per - 1)]
    sys_ = SleepSystem(n, v_sleep, t_sleep)
    counts = []
    for tick in range(1, max_s * HZ + 1):
        t = tick / HZ
        speeds = [max(v0s[i % per] * math.exp(-k * t), floors[i % per]) for i in range(n)]
        counts.append(sys_.tick(speeds, contacts))
    return counts


if __name__ == "__main__":
    try:
        counts = settle([4.0, 2.0, 1.0, 0.5, 0.25], [0, 0, 0, 0, 0])
        first = next(i for i, c in enumerate(counts, 1) if c == 0)
        print(f"stack of 5 sleeps at tick {first} = {first / HZ:.3f} s")
        for v0 in (4.0, 2.0, 1.0, 0.5, 0.25):
            print(f"v0 {v0:4}: alone {sleep_time_alone(v0, 2.0, 0.05, 0.5):.3f} s")
    except NotImplementedError:
        print("Finish steps 1-3 first.")
