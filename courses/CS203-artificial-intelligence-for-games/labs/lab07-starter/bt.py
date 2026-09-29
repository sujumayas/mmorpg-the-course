"""CS203 Lab 07 starter: a behavior tree you can trace. Standard library only.

Fill in the three TODO methods (Selector.tick, Sequence.tick, Inverter.tick),
then run the tests:

    python3 test_bt.py

Then run this file to print the guard's tick-by-tick trace in all three modes:

    python3 bt.py

Names and numbers follow the week 7 lecture. Every node's tick() returns one of
SUCCESS, FAILURE or RUNNING, and adds 1 to the global visit counter.

Modes (set per composite, the whole tree uses one mode):
    "reactive"  every composite starts from its first child on every tick
    "memory"    every composite resumes at the child that was RUNNING last tick
    "hybrid"    selectors are reactive; sequences resume at the RUNNING child
                but still re-check every Condition before it
"""

SUCCESS, FAILURE, RUNNING = "success", "failure", "running"
MODES = ("reactive", "memory", "hybrid")
visits = 0


def visit():
    global visits
    visits += 1


# ------------------------------------------------------------ provided leaves

class Condition:
    """Reads one boolean from the blackboard. Never RUNNING."""

    def __init__(self, key):
        self.key = key

    def tick(self, bb):
        visit()
        return SUCCESS if bb[self.key] else FAILURE

    def halt(self):
        pass


class Action:
    """Takes `ticks` ticks to finish (0 means it runs until interrupted).
    Writes its name to bb["acted"] so the trace shows what the NPC did."""

    def __init__(self, name, ticks=0):
        self.name, self.ticks, self.done = name, ticks, 0

    def tick(self, bb):
        visit()
        bb["acted"] = self.name
        self.done += 1
        if self.ticks and self.done >= self.ticks:
            self.done = 0
            return SUCCESS
        return RUNNING

    def halt(self):
        self.done = 0


class Composite:
    """Shared bookkeeping for Selector and Sequence.

    self.running is the index of the child that returned RUNNING on the last
    tick, or None. Call self.finish(i, status) as your LAST step: it aborts the
    previously running child if a different child is now in charge, updates
    self.running and returns status. Pass i=None when no child is running."""

    def __init__(self, children, mode):
        assert mode in MODES
        self.children, self.mode, self.running = children, mode, None

    def halt(self):
        for c in self.children:
            c.halt()
        self.running = None

    def finish(self, i, status):
        if self.running is not None and self.running != i:
            self.children[self.running].halt()
        self.running = i if status == RUNNING else None
        return status


# ------------------------------------------------------------ your code

class Selector(Composite):
    def tick(self, bb):
        """TODO step 1. Call visit() once. Tick children in order and return the
        first status that is not FAILURE (via self.finish). If every child
        fails, return self.finish(None, FAILURE).
        In "memory" mode only, start at self.running when it is not None.
        In "reactive" and "hybrid" mode always start at child 0."""
        raise NotImplementedError("Selector.tick() is yours to write")


class Sequence(Composite):
    def tick(self, bb):
        """TODO step 2. Call visit() once. Tick children in order and return the
        first status that is not SUCCESS (via self.finish). If every child
        succeeds, return self.finish(None, SUCCESS).
        "reactive": always start at child 0.
        "memory":   skip every child before self.running (when not None).
        "hybrid":   like memory, but still tick any Condition before
                    self.running; skip only the non-Condition children."""
        raise NotImplementedError("Sequence.tick() is yours to write")


class Inverter:
    """Decorator: swaps SUCCESS and FAILURE, passes RUNNING through."""

    def __init__(self, child):
        self.child = child

    def tick(self, bb):
        """TODO step 3. Call visit() once, tick the child, invert the result."""
        raise NotImplementedError("Inverter.tick() is yours to write")

    def halt(self):
        self.child.halt()


# ------------------------------------------------------------ the lecture's guard

def guard(mode):
    Seq = lambda *c: Sequence(list(c), mode)
    Sel = lambda *c: Selector(list(c), mode)
    return Sel(
        Seq(Condition("hurt"), Action("RunToSafety", 3)),
        Seq(Condition("sees"), Sel(Seq(Condition("in_range"), Action("Shoot")),
                                   Action("Chase"))),
        Seq(Condition("noise"), Action("GoToNoise", 2), Action("LookAround", 2)),
        Action("Patrol", 4),
    )


# World facts: the ticks (5 per second) on which each fact is true.
TIMELINE = {"noise": {2, 3, 4, 5, 6}, "sees": {5, 6, 7, 8},
            "in_range": {7, 8}, "hurt": {9, 10, 11}}


def run(tree, timeline=TIMELINE, ticks=12):
    """Tick `tree` once per tick. Returns a list of (acted, visits) pairs."""
    global visits
    out = []
    for t in range(ticks):
        bb = {k: t in ts for k, ts in timeline.items()}
        bb["acted"] = "-"
        visits = 0
        tree.tick(bb)
        out.append((bb["acted"], visits))
    return out


if __name__ == "__main__":
    for mode in MODES:
        rows = run(guard(mode))
        print(f"{mode:<9}", " ".join(a[:7].ljust(7) for a, _ in rows))
        print(f"{'':<9}", " ".join(str(v).ljust(7) for _, v in rows),
              f"total visits {sum(v for _, v in rows)}")
