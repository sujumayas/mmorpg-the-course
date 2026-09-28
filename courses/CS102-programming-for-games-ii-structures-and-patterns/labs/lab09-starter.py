"""CS102 Lab 09 starter: components, a World with a component index, and systems.

Run it with:
    .venv/bin/python courses/CS102-programming-for-games-ii-structures-and-patterns/labs/lab09-starter.py
Add --time to also run the polling-vs-index timing table (Part 5) once your queries work.

Work top to bottom. Each TODO raises NotImplementedError; the tests at the bottom report
TODO, PASS or FAIL. Do not edit the tests. Standard library only.
"""
import math
import random
import sys
import time

# ---------------------------------------------------------------------------
# Part 1. Components: plain data, plus the one behaviour that belongs to the data.
# ---------------------------------------------------------------------------


class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = x, y


class Render:
    def __init__(self, glyph="?"):
        self.glyph = glyph


class Mover:
    def __init__(self, speed=0.0):
        self.speed, self.vx, self.vy = speed, 0.0, 0.0


class Health:
    def __init__(self, hp=1.0):
        self.hp = hp

    def damage(self, amount):
        """TODO 1a: lower hp by amount, never below 0. Return True if still alive."""
        raise NotImplementedError("1a: Health.damage")


class AI:
    def __init__(self, target="player"):
        self.target = target        # name of the entity to chase or face
        self.facing = 0.0           # degrees


class Burning:
    def __init__(self, dps=5.0):
        self.dps = dps


# ---------------------------------------------------------------------------
# Part 2. Entities and the World.
#
# An Entity is a name plus a dict {component class: component}.
# The World owns every entity and keeps an INDEX: {component class: ordered set of entities}.
# Use a dict with None values as the ordered set (dicts keep insertion order since Python 3.7),
# so queries return entities in spawn order and replays stay deterministic.
# ---------------------------------------------------------------------------


class Entity:
    def __init__(self, name):
        self.name = name
        self.components = {}

    def get(self, cls):
        return self.components.get(cls)

    def has(self, *classes):
        return all(c in self.components for c in classes)


class World:
    def __init__(self):
        self.entities = {}          # name -> Entity, in spawn order
        self.index = {}             # component class -> {Entity: None}
        self.doomed = []            # entities waiting for flush()

    def spawn(self, name):
        e = Entity(name)
        self.entities[name] = e
        return e

    def add(self, e, component):
        """TODO 2a: store component on e under its class AND record e in self.index."""
        raise NotImplementedError("2a: World.add")

    def remove(self, e, cls):
        """TODO 2b: remove the component of class cls from e AND from self.index."""
        raise NotImplementedError("2b: World.remove")

    def query_poll(self, *classes):
        """TODO 2c: the slow way. Scan every entity; return those that have all classes."""
        raise NotImplementedError("2c: World.query_poll")

    def query(self, *classes):
        """TODO 2d: the indexed way. Start from the SMALLEST index set among classes,
        keep the entities that have all classes. Return a list (a copy), in spawn order."""
        raise NotImplementedError("2d: World.query")

    def destroy(self, e):
        """Mark e for removal at the end of the frame. Safe to call while iterating a query."""
        self.doomed.append(e)

    def flush(self):
        """TODO 2e: really remove every doomed entity: from self.entities and from every
        index set it is in. Then clear self.doomed."""
        raise NotImplementedError("2e: World.flush")


# ---------------------------------------------------------------------------
# Part 3. Entity types are data.
# ---------------------------------------------------------------------------

BLUEPRINTS = {
    "player": {Render: {"glyph": "@"}, Mover: {"speed": 120}, Health: {"hp": 100}},
    "goblin": {Render: {"glyph": "g"}, Mover: {"speed": 90}, Health: {"hp": 30}, AI: {}},
    "chest":  {Render: {"glyph": "="}, Health: {"hp": 10}},
    "tree":   {Render: {"glyph": "T"}},
    # TODO 3b: add "turret": renders as "Y", 40 hp, has AI, cannot move
    # TODO 3c: add "mimic":  renders as "=", moves at 60, 25 hp, has AI
}


def make(world, kind, name, x, y):
    """TODO 3a: spawn an entity, add Position(x, y), then every component in BLUEPRINTS[kind]
    constructed with its keyword arguments. Return the entity."""
    raise NotImplementedError("3a: make")


# ---------------------------------------------------------------------------
# Part 4. Systems. Each one asks the world for the entities it needs.
# ---------------------------------------------------------------------------


def ai_system(world):
    """TODO 4a: for each entity with AI and Position, look up its target by name in
    world.entities. Set ai.facing to the angle toward the target in degrees (math.atan2).
    If the entity also has a Mover, set vx, vy to speed along that direction."""
    raise NotImplementedError("4a: ai_system")


def move_system(world, dt):
    """TODO 4b: for each entity with Mover and Position, add velocity * dt to its position."""
    raise NotImplementedError("4b: move_system")


def burn_system(world, dt):
    """TODO 4c: for each entity with Burning and Health, apply dps * dt damage.
    If it dies, world.destroy(it). Do NOT flush here."""
    raise NotImplementedError("4c: burn_system")


# ---------------------------------------------------------------------------
# Part 5. Timing (run with --time once Part 2 works). Nothing to write here.
# ---------------------------------------------------------------------------


def build_crowd(n, seed=1):
    rng = random.Random(seed)
    w = World()
    for i in range(n):
        e = w.spawn(f"e{i}")
        w.add(e, Health(100.0))
        if rng.random() < 0.9:
            w.add(e, Render())
        if rng.random() < 0.3:
            w.add(e, Mover())
        if rng.random() < 0.05:
            w.add(e, AI())
        if rng.random() < 0.005:
            w.add(e, Burning())
    return w


def best_ms(fn, reps=30):
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t)
    return best * 1000


def timing_table():
    print(f"{'N':>8} {'burning':>8} {'poll ms':>9} {'index ms':>9} {'ratio':>7}")
    for n in (1_000, 10_000, 100_000):
        w = build_crowd(n)
        k = len(w.query(Burning, Health))
        tp = best_ms(lambda: w.query_poll(Burning, Health))
        ti = best_ms(lambda: w.query(Burning, Health))
        print(f"{n:>8} {k:>8} {tp:>9.3f} {ti:>9.4f} {tp / ti:>7.0f}")


# ---------------------------------------------------------------------------
# Tests. Do not edit below this line.
# ---------------------------------------------------------------------------


def close(a, b, tol=0.01):
    return abs(a - b) <= tol


def test_components_and_index():
    w = World()
    p = make(w, "player", "player", 0, 0)
    g = make(w, "goblin", "g1", 30, 40)
    make(w, "chest", "c1", 5, 5)
    make(w, "tree", "t1", 9, 9)
    assert [e.name for e in w.query(Render)] == ["player", "g1", "c1", "t1"]
    assert [e.name for e in w.query(Health, Mover)] == ["player", "g1"]
    assert [e.name for e in w.query(AI)] == ["g1"]
    for q in [(Render,), (Health, Mover), (AI,), (Burning,)]:
        assert w.query(*q) == w.query_poll(*q), q
    w.remove(g, AI)
    assert w.query(AI) == [] and not g.has(AI)
    h = p.get(Health)
    assert h.damage(60) is True and h.damage(60) is False and h.hp == 0


def test_systems():
    w = World()
    make(w, "player", "player", 0, 0)
    g = make(w, "goblin", "g1", 30, 40)
    ai_system(w)
    move_system(w, 0.5)
    assert close(g.get(Position).x, 3.0) and close(g.get(Position).y, 4.0)


def test_deferred_destroy():
    w = World()
    for i in range(5):
        e = make(w, "chest", f"c{i}", i, 0)
        w.add(e, Burning(dps=12.0 if i % 2 == 0 else 1.0))
    burn_system(w, 1.0)                     # 10 hp chests: even ones die this frame
    assert len(w.entities) == 5             # nothing removed until flush
    w.flush()
    assert list(w.entities) == ["c1", "c3"]
    assert [e.name for e in w.query(Burning)] == ["c1", "c3"]
    assert [e.name for e in w.query(Render)] == ["c1", "c3"]


def test_new_types():
    w = World()
    make(w, "player", "player", 100, 0)
    t = make(w, "turret", "t1", 0, 0)
    m = make(w, "mimic", "m1", 0, 100)
    ai_system(w)
    move_system(w, 1.0)
    assert t.get(Mover) is None and t.get(Health).hp == 40 and t.get(Render).glyph == "Y"
    assert close(t.get(AI).facing, 0.0) and close(t.get(Position).x, 0.0)
    assert close(m.get(AI).facing, -45.0), m.get(AI).facing
    assert close(m.get(Position).x, 42.43) and close(m.get(Position).y, 57.57)


if __name__ == "__main__":
    for test in (test_components_and_index, test_systems, test_deferred_destroy, test_new_types):
        try:
            test()
            print(f"PASS  {test.__name__}")
        except NotImplementedError as e:
            print(f"TODO  {test.__name__}: part {e}")
        except (AssertionError, KeyError, AttributeError, TypeError) as e:
            print(f"FAIL  {test.__name__}: {type(e).__name__} {e}")
    if "--time" in sys.argv:
        print()
        try:
            timing_table()
        except NotImplementedError as e:
            print(f"(timing needs part {e})")
