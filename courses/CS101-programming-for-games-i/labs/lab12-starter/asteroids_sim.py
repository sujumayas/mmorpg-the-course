"""CS101 Lab 12 starter: a headless arcade simulation with three planted bugs.

Python 3.10+, standard library only. Nothing is drawn. The "game" is a ship parked in the
middle of a 320 x 240 field while rocks drift past. It uses the collision test from week 10
and the state machine from week 11, and it has three bugs that players reported (see lab12.md).

Run a session:        python asteroids_sim.py            (seed 7, 600 frames)
Turn on debug logs:   python asteroids_sim.py --debug
Everything is deterministic for a given seed, so every bug can be reproduced exactly.
"""
import logging
import random
import sys

log = logging.getLogger("sim")

FIELD_W, FIELD_H = 320, 240
DT = 1 / 60


# ---------------------------------------------------------------- collision (week 10)

def edges(box):
    return box["x"], box["x"] + box["w"], box["y"], box["y"] + box["h"]


def overlap(a, b):
    """Strict AABB overlap: touching edges do not count."""
    a_left, a_right, a_top, a_bottom = edges(a)
    b_left, b_right, b_top, b_bottom = edges(b)
    return (a_left < b_right and
            a_right > b_left and
            a_top < b_bottom and
            a_bottom >= b_top)


# ---------------------------------------------------------------- waves

def enemies_for_wave(wave):
    """Rocks per wave. Designers want this to never go down as waves go up."""
    return 3 + 2 * wave


def next_wave(game):
    """Advance the wave counter. The save format stores the wave in one byte."""
    game["wave"] = (game["wave"] + 1) & 0xFF
    return game["wave"]


# ---------------------------------------------------------------- state machine (week 11)

TRANSITIONS = {
    ("MENU", "start"): "PLAY",
    ("PLAY", "pause"): "PAUSE",
    ("PLAY", "out_of_lives"): "GAME_OVER",
    ("PAUSE", "resume"): "PLAY",
    ("PAUSE", "quit"): "MENU",
    ("GAME_OVER", "retry"): "PLAY",
    ("GAME_OVER", "quit"): "MENU",
}


def new_game(seed=7):
    return {"state": "MENU", "lives": 3, "score": 0, "wave": 0, "frame": 0,
            "ship": {"x": 150, "y": 110, "w": 20, "h": 20},
            "rocks": [], "rng": random.Random(seed)}


def on_enter(game, state):
    if state == "PLAY":
        game["lives"] = 3
        log.debug("frame=%d enter PLAY lives=%d", game["frame"], game["lives"])


def handle_event(game, event):
    """Apply one event. Returns True if the state changed."""
    key = (game["state"], event)
    if key not in TRANSITIONS:
        return False
    if event in ("start", "retry"):
        game["score"] = 0
        game["wave"] = 0
    game["state"] = TRANSITIONS[key]
    on_enter(game, game["state"])
    return True


# ---------------------------------------------------------------- play

def spawn_wave(game):
    rng = game["rng"]
    for _ in range(enemies_for_wave(game["wave"])):
        side = rng.choice(["left", "right"])
        y = rng.randrange(0, FIELD_H - 16)
        x = -16 if side == "left" else FIELD_W
        vx = rng.choice([60, 90, 120]) * (1 if side == "left" else -1)
        game["rocks"].append({"x": x, "y": y, "w": 16, "h": 16, "vx": vx})


def update_play(game):
    """One frame of play: move rocks, resolve hits, advance waves."""
    game["frame"] += 1
    if not game["rocks"]:
        spawn_wave(game)
    for rock in game["rocks"]:
        rock["x"] += rock["vx"] * DT
    hits = [r for r in game["rocks"] if overlap(r, game["ship"])]
    for rock in hits:
        game["lives"] -= 1
        game["rocks"].remove(rock)
        log.debug("frame=%d hit rock=(%.1f,%.1f) lives=%d",
                  game["frame"], rock["x"], rock["y"], game["lives"])
    game["rocks"] = [r for r in game["rocks"] if -32 < r["x"] < FIELD_W + 32]
    if not game["rocks"]:
        game["score"] += 100
        next_wave(game)
    if game["lives"] <= 0:
        handle_event(game, "out_of_lives")


def run(seed=7, frames=600, events=None):
    """Play `frames` frames. `events` maps a frame number to an event name,
    for example {120: "pause", 180: "resume"}. Returns the final game dict."""
    events = events or {}
    game = new_game(seed)
    handle_event(game, "start")
    for f in range(1, frames + 1):
        if f in events:
            handle_event(game, events[f])
        if game["state"] == "PLAY":
            update_play(game)
        else:
            game["frame"] += 1
    return game


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG if "--debug" in sys.argv else logging.INFO,
                        format="%(message)s")
    g = run()
    print(f"state={g['state']} lives={g['lives']} score={g['score']} wave={g['wave']}")
