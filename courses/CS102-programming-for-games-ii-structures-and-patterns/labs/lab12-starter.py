"""CS102 Lab 12 starter: record 30 s of commands, replay them, find the desync.

Usage:  python lab12-starter.py record run.rep     play the scripted 30 s and save a recording
        python lab12-starter.py replay run.rep     replay a recording and compare checksums
        python lab12-starter.py check              record, then replay in a NEW Python process,
                                                   and report the first second that differs
        python lab12-starter.py --test             self-checks (several FAIL until you finish)

Pure standard library. Python 3.10+.

The simulation has THREE planted determinism bugs. `check` will show a desync until all
three are fixed. They are marked only with the comment `# suspicious?` among several
harmless lines that carry the same comment, so read carefully.

Recording format (little-endian):
  4 bytes  magic b"CS12"
  1 byte   format version
  4 bytes  world seed (uint32)
  2 bytes  tick count T (uint16)
  T bytes  one command byte per tick (bit flags below)
  4 bytes  per full second: first 4 bytes of the state checksum at the end of that second
"""
import hashlib
import math
import os
import random
import struct
import subprocess
import sys
import tempfile
import time

HZ = 60
DT = 1 / HZ
SECONDS = 30
TICKS = SECONDS * HZ
VERSION = 1
UP, DOWN, LEFT, RIGHT, FIRE = 1, 2, 4, 8, 16
NAMES = ["wolf", "boar", "bandit", "spider", "slime"]


class Enemy:
    def __init__(self, name, x, y):
        self.name, self.x, self.y = name, x, y
        self.hp = 20
        self.respawn_ticks = 0


class World:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.x, self.y = 0.0, 0.0
        self.enemies = {n: Enemy(n, 40.0 * i, -60.0) for i, n in enumerate(NAMES)}
        self.alive = set(NAMES)                                   # suspicious?
        self.kills = 0
        self.tick = 0

    def step(self, buttons, dt):
        speed = 90.0
        dx = ((buttons & RIGHT) > 0) - ((buttons & LEFT) > 0)     # suspicious?
        dy = ((buttons & DOWN) > 0) - ((buttons & UP) > 0)
        self.x += dx * speed * dt
        self.y += dy * speed * dt
        if buttons & FIRE and self.alive:
            target = next(iter(self.alive))                       # suspicious?
            if random.random() < 0.5:                             # suspicious?
                e = self.enemies[target]
                e.hp -= 3 + self.rng.randrange(4)                 # suspicious?
                if e.hp <= 0:
                    self.alive.discard(target)
                    e.respawn_ticks = 2 * HZ
                    self.kills += 1
        for e in self.enemies.values():
            if e.respawn_ticks > 0:
                e.respawn_ticks -= 1
                if e.respawn_ticks == 0:
                    e.hp = 20
                    self.alive.add(e.name)
        self.tick += 1

    def checksum(self):
        h = hashlib.sha1()
        h.update(struct.pack("<ddii", self.x, self.y, self.kills, self.tick))
        for n in NAMES:                                           # suspicious?
            e = self.enemies[n]
            h.update(struct.pack("<ii", e.hp, e.respawn_ticks))
        return h.digest()[:4]


def scripted_player(seed=7):
    """The recorded 'human'. Holds a direction for 20 ticks, taps fire ~30% of ticks."""
    rng = random.Random(seed)
    held, out = 0, []
    for tick in range(TICKS):
        if tick % 20 == 0:
            held = rng.choice([UP, DOWN, LEFT, RIGHT, UP | RIGHT, 0])
        out.append(held | (FIRE if rng.random() < 0.3 else 0))
    return out


def measured_dt():
    """How long the last frame took on this machine's clock. It wobbles by up to 20%."""
    return DT * (1 + 0.2 * math.sin(time.perf_counter() * 997))


def record(seed=1234):
    world = World(seed)
    commands = scripted_player()
    sums = []
    for tick, buttons in enumerate(commands):
        dt = measured_dt()                                         # suspicious?
        world.step(buttons, dt)
        if (tick + 1) % HZ == 0:
            sums.append(world.checksum())
    header = b"CS12" + struct.pack("<BIH", VERSION, seed, len(commands))
    return header + bytes(commands) + b"".join(sums), world


def parse(data):
    if data[:4] != b"CS12":
        raise ValueError("not a CS12 recording")
    version, seed, n = struct.unpack("<BIH", data[4:11])
    if version != VERSION:
        raise ValueError(f"recording is version {version}, this build is {VERSION}")
    commands = list(data[11:11 + n])
    raw = data[11 + n:]
    sums = [raw[i:i + 4] for i in range(0, len(raw), 4)]
    return seed, commands, sums


def replay(data):
    """Returns (first_bad_second or None, world)."""
    seed, commands, sums = parse(data)
    world = World(seed)
    for tick, buttons in enumerate(commands):
        dt = measured_dt()
        world.step(buttons, dt)
        if (tick + 1) % HZ == 0:
            second = (tick + 1) // HZ
            if world.checksum() != sums[second - 1]:
                return second, world
    return None, world


# ------------------------------------------------------------------ level editor (for undo)

class Level:
    def __init__(self, w=16, h=16):
        self.tiles = [[0] * w for _ in range(h)]

    def paint(self, x, y, tile):
        self.tiles[y][x] = tile

# TODO step 6: write PaintTile (execute/undo) and History (run/undo/redo) as in the lecture,
# and a FillRect command that paints a rectangle and can undo it.


# ------------------------------------------------------------------ driver

def check():
    data, world = record()
    path = os.path.join(tempfile.gettempdir(), "cs102_lab12_check.rep")
    with open(path, "wb") as f:
        f.write(data)
    out = subprocess.run([sys.executable, __file__, "replay", path], capture_output=True, text=True)
    print(f"recorded {len(data)} bytes, kills {world.kills}, pos ({world.x:.3f}, {world.y:.3f})")
    print(out.stdout.strip())
    return "MATCH" in out.stdout


def tests():
    ok = True

    def t(label, cond):
        nonlocal ok
        ok &= bool(cond)
        print(("PASS " if cond else "FAIL ") + label)

    data, _ = record()
    t("recording is 11 + 1800 + 30*4 bytes", len(data) == 11 + 1800 + 120)
    first, _ = replay(data)
    t("same-process replay matches", first is None)
    t("replay in a new process matches (run `check` to see where it breaks)", check())
    try:
        parse(data[:4] + bytes([VERSION + 1]) + data[5:])
        t("wrong version is rejected", False)
    except ValueError:
        t("wrong version is rejected", True)
    has_history = "History" in globals() and "PaintTile" in globals()
    t("History and PaintTile exist", has_history)
    if has_history:
        lv = Level()
        h = globals()["History"](lv)
        P = globals()["PaintTile"]
        h.run(P(1, 1, 5)); h.run(P(1, 1, 7)); h.undo()
        t("undo restores the previous tile", lv.tiles[1][1] == 5)
        h.run(P(2, 2, 9))
        h.redo()
        t("a new command clears redo", lv.tiles[1][1] == 5 and lv.tiles[2][2] == 9)
    return ok


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["record"]:
        data, w = record()
        open(args[1], "wb").write(data)
        print(f"wrote {len(data)} bytes to {args[1]}")
    elif args[:1] == ["replay"]:
        first, w = replay(open(args[1], "rb").read())
        if first is None:
            print(f"MATCH: all {SECONDS} checksums agree (kills {w.kills})")
        else:
            print(f"DESYNC: first bad checksum at second {first} "
                  f"(replay pos ({w.x:.3f}, {w.y:.3f}), kills {w.kills})")
    elif args[:1] == ["check"]:
        check()
    elif "--test" in args:
        sys.exit(0 if tests() else 1)
    else:
        print(__doc__)
