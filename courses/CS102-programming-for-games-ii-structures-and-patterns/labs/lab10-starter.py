"""CS102 Lab 10 starter: quests and achievements, polled and event-driven.

Usage:  python lab10-starter.py            run the scripted session and print a report
        python lab10-starter.py --test     run the self-checks (some FAIL until you fix the bugs)

Pure standard library. Python 3.10+.

What is here
  make_session(seed)   A scripted 10-minute session at 60 fps. Each frame is a list
                       of (event_name, payload_dict) tuples. Deterministic per seed.
  PollingTracker       The "before" design. Every frame it checks every objective.
  EventBus             The "after" design. It has TWO planted bugs (see TODOs).
  EventTracker         Quests and achievements as event listeners.
  Enemy                Subscribes to player_moved for aggro checks. Planted lapsed-listener bug.
"""
import random
import sys
from collections import defaultdict

FPS = 60
SECONDS = 600
KINDS = ["wolf", "boar", "bandit", "spider"]

# Objectives: (name, event kind to count, target). 150 objectives in total.
OBJECTIVES = [(f"kill_{k}_{n}", k, n) for k in KINDS for n in range(5, 5 + 37 * 5, 5)][:148]
OBJECTIVES += [("loot_50", "loot", 50), ("level_5", "level", 5)]


def make_session(seed=2026):
    """Return a list of frames; each frame is a list of (event, payload) tuples."""
    rng = random.Random(seed)
    frames = []
    level_xp = 0
    for f in range(FPS * SECONDS):
        events = []
        if rng.random() < 0.4 / FPS:                 # ~0.4 kills per second
            events.append(("enemy_killed", {"kind": rng.choice(KINDS), "killer": "p1"}))
            level_xp += 1
            if level_xp % 40 == 0:
                events.append(("level_up", {"level": level_xp // 40 + 1}))
        if rng.random() < 0.25 / FPS:                # ~0.25 loot pickups per second
            events.append(("item_looted", {"item": "coin"}))
        if rng.random() < 1 / 30:                    # an enemy spawns ~2 times per second
            events.append(("enemy_spawned", {"id": f}))
        if rng.random() < 1 / 30:
            events.append(("enemy_despawned", {}))
        events.append(("player_moved", {"x": f % 100, "y": 0}))
        frames.append(events)
    return frames


class Counters:
    """Game-side numbers that the polling design reads."""
    def __init__(self):
        self.kills = defaultdict(int)
        self.loot = 0
        self.level = 1


class PollingTracker:
    def __init__(self):
        self.done = set()
        self.checks = 0

    def poll(self, counters):
        for name, kind, target in OBJECTIVES:
            self.checks += 1
            if name in self.done:
                continue
            value = counters.loot if kind == "loot" else counters.level if kind == "level" else counters.kills[kind]
            if value >= target:
                self.done.add(name)


def run_polling(frames):
    c, t = Counters(), PollingTracker()
    for events in frames:
        for name, p in events:
            if name == "enemy_killed":
                c.kills[p["kind"]] += 1
            elif name == "item_looted":
                c.loot += 1
            elif name == "level_up":
                c.level = p["level"]
        t.poll(c)
    return t.done, t.checks


class EventBus:
    def __init__(self):
        self._listeners = defaultdict(list)
        self.calls = 0

    def subscribe(self, event, callback):
        self._listeners[event].append(callback)
        # TODO bug 1: return an unsubscribe function so listeners can leave.

    def emit(self, event, **payload):
        # TODO bug 2: iterating the live list skips a listener when one unsubscribes mid-loop.
        for callback in self._listeners[event]:
            self.calls += 1
            callback(**payload)

    def listener_count(self, event):
        return len(self._listeners[event])


class Objective:
    """One quest or achievement. Unsubscribes itself when complete."""
    def __init__(self, bus, name, kind, target, done):
        self.name, self.kind, self.target, self.count, self.done = name, kind, target, 0, done
        event = {"loot": "item_looted", "level": "level_up"}.get(kind, "enemy_killed")
        self._unsub = bus.subscribe(event, self.on_event)

    def on_event(self, **p):
        if self.kind == "level":
            self.count = p["level"]
        elif self.kind == "loot" or p.get("kind") == self.kind:
            self.count += 1
        if self.count >= self.target:
            self.done.add(self.name)
            if self._unsub:
                self._unsub()
                self._unsub = None


class Enemy:
    def __init__(self, bus):
        self.alive = True
        bus.subscribe("player_moved", self.on_player_moved)
        # TODO bug 3: keep the unsubscribe handle and call it in destroy().

    def on_player_moved(self, x, y):
        pass                                          # aggro range check would go here

    def destroy(self):
        self.alive = False


def run_events(frames):
    bus, done = EventBus(), set()
    objectives = [Objective(bus, n, k, t, done) for n, k, t in OBJECTIVES]
    enemies = []
    moved_calls_last_minute = 0
    for i, events in enumerate(frames):
        for name, p in events:
            if name == "enemy_spawned":
                enemies.append(Enemy(bus))
            elif name == "enemy_despawned" and enemies:
                enemies.pop(0).destroy()
            else:
                before = bus.calls
                bus.emit(name, **p)
                if name == "player_moved" and i >= len(frames) - FPS * 60:
                    moved_calls_last_minute += bus.calls - before
    return done, bus.calls, len(enemies), bus.listener_count("player_moved"), moved_calls_last_minute, objectives


def report():
    frames = make_session()
    kills = sum(1 for f in frames for e, _ in f if e == "enemy_killed")
    done_p, checks = run_polling(frames)
    done_e, calls, alive, moved_listeners, moved_last_min, _ = run_events(frames)
    print(f"session: {len(frames)} frames, {kills} kills")
    print(f"polling: {len(done_p)} objectives complete, {checks:,} checks")
    print(f"events:  {len(done_e)} objectives complete, {calls:,} callback calls")
    print(f"enemies alive at end: {alive}, player_moved listeners: {moved_listeners}")
    print(f"player_moved calls in the last minute: {moved_last_min:,}")
    if done_p != done_e:
        print("MISMATCH: objectives differ:", sorted(done_p ^ done_e)[:5])


def tests():
    ok = True

    def check(label, cond):
        nonlocal ok
        ok &= cond
        print(("PASS " if cond else "FAIL ") + label)

    bus = EventBus()
    seen = []
    unsub = bus.subscribe("x", lambda: seen.append("a"))
    check("subscribe returns an unsubscribe function", callable(unsub))
    bus2 = EventBus()
    hits = []
    handles = {}
    handles["q"] = bus2.subscribe("k", lambda: (hits.append("q"), handles["q"] and handles["q"]()))
    bus2.subscribe("k", lambda: hits.append("a"))
    bus2.emit("k")
    check("a listener after a self-removing listener still runs", hits == ["q", "a"])
    frames = make_session()
    done_p, _ = run_polling(frames)
    done_e, _, alive, moved_listeners, _, _ = run_events(frames)
    check("polling and events complete the same objectives", done_p == done_e)
    check("player_moved listeners equal live enemies", moved_listeners == alive)
    return ok


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.exit(0 if tests() else 1)
    report()
