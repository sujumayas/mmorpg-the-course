"""DB201 Lab 01 starter: save intervals, crash loss, and a save that survives a crash.

Run:
    python save_sim.py --check     # correctness tests only
    python save_sim.py             # tests, then the save-interval table

Python 3.10+, standard library only. You edit the three functions marked TODO.
"""
import json
import os
import random
import sys
import tempfile

# ---------------------------------------------------------------------------
# Part A: the save-interval model
# ---------------------------------------------------------------------------


def model(n_players, interval_s, state_bytes):
    """Return the periodic-save model from lecture as a dict.

    saves_per_s   = N / T
    bytes_per_s   = N * S / T
    avg_loss_s    = T / 2         (crash lands uniformly inside an interval)
    worst_loss_s  = T
    player_hours  = N * T / 2 / 3600   (progress erased by one server crash)
    """
    return {
        "saves_per_s": n_players / interval_s,
        "bytes_per_s": n_players * state_bytes / interval_s,
        "avg_loss_s": interval_s / 2,
        "worst_loss_s": interval_s,
        "player_hours": n_players * interval_s / 2 / 3600,
    }


def simulate_loss(interval_s, n_crashes=20000, seed=1):
    """Monte Carlo: each player's last save happened at a random phase.

    TODO (Part A): for each simulated crash, draw the time since the player's
    last save and record the progress lost. Return the mean loss in seconds.
    Hint: the time since the last save is uniform on [0, interval_s).
    """
    rng = random.Random(seed)
    raise NotImplementedError("simulate_loss")


def hybrid_writes_per_s(n_players, interval_s, events_per_player_hour):
    """TODO (Part A): writes per second when the server saves every player every
    interval_s seconds AND also saves immediately on each valuable event
    (trade, rare drop, purchase). Return periodic + event writes per second.
    """
    raise NotImplementedError("hybrid_writes_per_s")


# ---------------------------------------------------------------------------
# Part B: crash-safe saving
# ---------------------------------------------------------------------------


class SimulatedCrash(Exception):
    """Raised by write_with_crash to imitate the process dying mid-write."""


def write_with_crash(f, text, crash_after=None, chunk=64):
    """Write text to an open file in small chunks.

    If crash_after is a number, raise SimulatedCrash once that many characters
    have been written. The file is flushed first, so the partial data is really
    on disk, as it would be if the server died at that moment.
    """
    written = 0
    for i in range(0, len(text), chunk):
        piece = text[i:i + chunk]
        if crash_after is not None and written + len(piece) > crash_after:
            f.write(piece[: crash_after - written])
            f.flush()
            raise SimulatedCrash()
        f.write(piece)
        written += len(piece)


def naive_save(path, state, crash_after=None):
    """Overwrite the save file in place. Complete, and unsafe."""
    text = json.dumps(state, indent=1)
    with open(path, "w") as f:
        write_with_crash(f, text, crash_after)


def atomic_save(path, state, crash_after=None):
    """TODO (Part B): save so that a crash at ANY point leaves either the old
    file or the new file on disk, never a mix.

    Steps: write the full text to a temporary file in the same directory
    (use write_with_crash so the test can inject a crash), flush, os.fsync the
    file, then os.replace(temp, path). Clean up the temp file if you crash
    before the replace is fine but not required.
    """
    raise NotImplementedError("atomic_save")


def load(path):
    with open(path) as f:
        return json.load(f)


def make_state(version):
    """A character save of about 17 kB (the lecture model uses 24 kB)."""
    items = [{"slot": i, "type_id": 1000 + i, "qty": (i * 7) % 50 + 1} for i in range(300)]
    return {"version": version, "name": "Test Character", "gold": 1000 * version,
            "xp": 5000 * version, "items": items}


# ---------------------------------------------------------------------------
# Checks and report
# ---------------------------------------------------------------------------


def crash_test(save_fn):
    """Save v1, then crash while saving v2 at many points. Count corrupt loads."""
    corrupt = 0
    trials = 0
    with tempfile.TemporaryDirectory(prefix="db201-lab01-") as d:
        path = os.path.join(d, "character.json")
        v1, v2 = make_state(1), make_state(2)
        size = len(json.dumps(v2, indent=1))
        for crash_at in range(0, size, max(1, size // 40)):
            save_fn(path, v1)
            try:
                save_fn(path, v2, crash_after=crash_at)
            except SimulatedCrash:
                pass
            trials += 1
            try:
                got = load(path)
                if got not in (v1, v2):
                    corrupt += 1
            except (json.JSONDecodeError, FileNotFoundError):
                corrupt += 1
    return corrupt, trials


def check():
    ok = True
    try:
        m = simulate_loss(300)
        good = abs(m - 150) < 3
        print(f"simulate_loss(300) = {m:.1f} s  (expect about 150)  {'OK' if good else 'FAIL'}")
        ok &= good
    except NotImplementedError as e:
        print(f"TODO: {e}")
        ok = False
    try:
        w = hybrid_writes_per_s(4000, 300, 12)
        good = abs(w - 26.667) < 0.01
        print(f"hybrid_writes_per_s(4000, 300, 12) = {w:.3f}  (expect 26.667)  {'OK' if good else 'FAIL'}")
        ok &= good
    except NotImplementedError as e:
        print(f"TODO: {e}")
        ok = False
    bad, n = crash_test(naive_save)
    print(f"naive_save:  {bad}/{n} crashes left a corrupt file  (expected: many)")
    try:
        bad, n = crash_test(atomic_save)
        print(f"atomic_save: {bad}/{n} crashes left a corrupt file  {'OK' if bad == 0 else 'FAIL'}")
        ok &= bad == 0
    except NotImplementedError as e:
        print(f"TODO: {e}")
        ok = False
    return ok


def report():
    n, s = 4000, 24000
    print()
    print(f"Periodic save model, N = {n} players, S = {s:,} bytes")
    print(f"{'T (s)':>7} {'saves/s':>9} {'kB/s':>9} {'avg loss s':>11} {'player-h lost':>14}")
    for t in (1, 10, 60, 300, 840):
        m = model(n, t, s)
        print(f"{t:>7} {m['saves_per_s']:>9.1f} {m['bytes_per_s'] / 1000:>9.1f} "
              f"{m['avg_loss_s']:>11.1f} {m['player_hours']:>14.2f}")


if __name__ == "__main__":
    passed = check()
    if "--check" not in sys.argv:
        report()
    sys.exit(0 if passed else 1)
