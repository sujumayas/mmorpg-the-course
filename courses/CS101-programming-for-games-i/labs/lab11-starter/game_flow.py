"""CS101 Lab 11 starter, part 2: the game-flow machine (menu, play, pause, game over).

Fill in the TODOs. The table in lecture 11, section 3 is the specification.
"""

TRANSITIONS = {
    ("MENU", "start"): "PLAY",
    ("PLAY", "pause"): "PAUSE",
    # TODO: add the other five rows from the lecture's table
}

GAME_OVER_LOCK = 1.0   # seconds of ignored input after entering GAME_OVER


def new_game():
    """Given, do not change."""
    return {"state": "MENU", "score": 0, "lives": 3, "high_score": 0,
            "clock_running": False, "play_time": 0.0, "input_lock": 0.0}


def handle(game, event):
    """Apply one event. Return True if a transition happened, False if ignored.

    - Unknown (state, event) pairs are ignored.
    - "retry" is ignored while input_lock > 0.
    - "start" and "retry" reset score to 0 and lives to 3 (a TRANSITION action).
    - "out_of_lives" saves score into high_score if it is higher.
    - Call on_exit(old) before changing state and on_enter(new) after."""
    raise NotImplementedError("TODO")


def on_enter(game, state):
    """State actions: PLAY starts the clock, PAUSE stops it,
    GAME_OVER stops it and sets input_lock to GAME_OVER_LOCK.
    Do NOT reset score or lives here (see the unpause bug)."""
    raise NotImplementedError("TODO")


def on_exit(game, state):
    """Nothing required. Keep it for your own extensions."""
    pass


def update(game, dt):
    """Per-state update. Given, but read it."""
    if game["state"] == "PLAY":
        game["play_time"] += dt
    elif game["state"] == "GAME_OVER":
        game["input_lock"] = max(0.0, game["input_lock"] - dt)


def score_points(game, points):
    """Given. Points only count while playing."""
    if game["state"] == "PLAY":
        game["score"] += points
