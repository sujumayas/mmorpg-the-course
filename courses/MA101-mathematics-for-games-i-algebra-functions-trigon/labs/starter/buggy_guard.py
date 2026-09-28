"""A teammate's guard vision. Players report: "it sees me from the side when I'm far away."
Do not read this file until step 5 of the lab. Run it to get its seen/not-seen answers."""
import math
from lab13_starter import Vec2, load_guards, load_path


def guard_sees(guard_pos, guard_fwd, half_angle_deg, sight_range, player_pos):
    c = math.cos(math.radians(half_angle_deg))
    d = player_pos - guard_pos
    if d.length() > sight_range:
        return False
    return guard_fwd.x * d.x + guard_fwd.y * d.y >= c


if __name__ == "__main__":
    g = [g for g in load_guards() if g["name"] == "sentry_a"][0]
    seen = sum(guard_sees(g["pos"], g["fwd"], g["half_angle_deg"], g["range"], Vec2(x, y))
               for x in range(-30, 31) for y in range(-30, 31))
    print("grid points seen by the buggy guard:", seen)
    first = next((t for t, p in load_path()
                  if guard_sees(g["pos"], g["fwd"], g["half_angle_deg"], g["range"], p)), None)
    print("buggy guard first sees the player at t =", first)
