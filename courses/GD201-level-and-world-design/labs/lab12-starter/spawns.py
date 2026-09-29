"""GD201 Lab 12: sightline heatmaps, spawn camping and contested camps.

Maps are lists of strings: '#' is wall, anything else is floor. Cells are (x, y) with x to
the right and y down, counted from 0 at the top-left. See lecture week 12, section 2.

    python spawns.py            report for the teaching map
    python spawns.py --design   check your redesigned lab map against the targets
"""
import math
import sys

TEACHING_MAP = """
#################
#...............#
#...............#
#.......A.......#
#...............#
#...##.....##...#
#...#.......#...#
#...#.......#...#
##.##..###..#####
#B..#.......#..C#
#...........#.###
#...#...........#
#################
""".split()

ARENA = ["#" * 11] + ["#" + "." * 9 + "#" for _ in range(9)] + ["#" * 11]

# The lab map: a small capture zone. The team spawn S sits in the open by the west wall.
LAB_MAP = """
#####################
#...................#
#...................#
#.....###.....###...#
#.....#.........#...#
#S....#....X....#...#
#.....#.........#...#
#.....###.....###...#
#...................#
#...................#
#####################
""".split()
LAB_SPAWN = (1, 5)
LAB_EXITS = [(1, 5)]      # in the open, the spawn cell is its own exit
LAB_ROOM = set()          # cells that belong to the spawn area (excluded from K)

# Part D: copy LAB_MAP here and redesign it. Update the spawn, exits and room to match.
MY_MAP = list(LAB_MAP)
MY_SPAWN = LAB_SPAWN
MY_EXITS = list(LAB_EXITS)
MY_ROOM = set(LAB_ROOM)
DESIGN_TARGETS = {"R": 8, "max_E_spawn": 20, "min_exits": 2, "max_E_exit": 45, "max_K": 5}


def walls(m):
    """Set of wall cells. Given."""
    return {(x, y) for y, row in enumerate(m) for x, ch in enumerate(row) if ch == "#"}


def open_cells(m):
    """List of floor cells in reading order. Given."""
    return [(x, y) for y, row in enumerate(m) for x, ch in enumerate(row) if ch != "#"]


def los(m, a, b):
    """True if no wall cell lies on the segment between the centres of a and b.
    Rule: n = max(1, 4 * max(|dx|, |dy|)); for i in 0..n, t = i / n, the sample lands in cell
    (floor(x0 + dx*t + 0.5), floor(y0 + dy*t + 0.5)). Any wall sample blocks the line."""
    # TODO Part A
    raise NotImplementedError("los")


def exposure(m, p, R):
    """E(p): number of floor cells c != p with dx^2 + dy^2 <= R^2 and los(m, c, p)."""
    # TODO Part A
    raise NotImplementedError("exposure")


def heatmap(m, R):
    """Dict {cell: E(cell)} for every floor cell."""
    # TODO Part A
    raise NotImplementedError("heatmap")


def camp_positions(m, exits, room, R):
    """Sorted list of floor cells outside `room` that see every exit (in range and in sight).
    A cell standing on an exit does not see that exit (c != p)."""
    # TODO Part B
    raise NotImplementedError("camp_positions")


def p_star(M, t_k, T):
    """Players at which a camp becomes supply-limited: M * t_k / T."""
    # TODO Part C
    raise NotImplementedError("p_star")


def quest_time(k, t_k, M, T, P):
    """Seconds for k kills with P players sharing M spawns that respawn every T seconds:
    k * max(t_k, T * P / M)."""
    # TODO Part C
    raise NotImplementedError("quest_time")


def print_heatmap(m, R):
    """Print the map with E in every floor cell. Given (needs heatmap)."""
    h = heatmap(m, R)
    for y, row in enumerate(m):
        print(" ".join("##" if ch == "#" else f"{h[(x, y)]:2d}" for x, ch in enumerate(row)))


def spawn_report(m, spawn, exits, room, R):
    return {
        "E_spawn": exposure(m, spawn, R),
        "E_exits": [exposure(m, e, R) for e in exits],
        "K": len(camp_positions(m, exits, room, R)),
    }


def check_design():
    t = DESIGN_TARGETS
    r = spawn_report(MY_MAP, MY_SPAWN, MY_EXITS, MY_ROOM, t["R"])
    tests = [
        (f"E at spawn <= {t['max_E_spawn']}", r["E_spawn"] <= t["max_E_spawn"]),
        (f"at least {t['min_exits']} exits", len(MY_EXITS) >= t["min_exits"]),
        (f"every exit E <= {t['max_E_exit']}", all(e <= t["max_E_exit"] for e in r["E_exits"])),
        (f"K <= {t['max_K']}", r["K"] <= t["max_K"]),
    ]
    print(r)
    for label, ok in tests:
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")


def main():
    try:
        if "--design" in sys.argv:
            check_design()
            return
        print_heatmap(TEACHING_MAP, 8)
        room_b = {(x, y) for x in (1, 2, 3) for y in (9, 10, 11)}
        print("B", spawn_report(TEACHING_MAP, (1, 9), [(4, 10), (2, 8)], room_b, 8))
        print("lab spawn", spawn_report(LAB_MAP, LAB_SPAWN, LAB_EXITS, LAB_ROOM, 8))
    except NotImplementedError as e:
        print(f"not implemented yet ({e})")


if __name__ == "__main__":
    main()
