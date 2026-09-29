"""Regenerates level.csv, the lab 01 test level. You do not need to run this."""
import csv

tris = []

def quad(name, p0, p1, p2, p3):
    # p0 -> p1 -> p2 -> p3 counter-clockwise seen from the front (right-handed, Y up)
    tris.append((name + "_a", p0, p1, p2))
    tris.append((name + "_b", p0, p2, p3))

# Flat floor 10 x 10, normal up.
quad("floor", (0, 0, 0), (0, 0, 10), (10, 0, 10), (10, 0, 0))
# Ramps rising along +x from the floor's edge at x=10, 2 m wide in z, each with a given rise:run.
def ramp(name, z0, run, rise):
    quad(name, (10, 0, z0), (10, 0, z0 + 2), (10 + run, rise, z0 + 2), (10 + run, rise, z0))
ramp("ramp_1_4", 0, 4, 1)
ramp("ramp_3_4", 2, 4, 3)
ramp("ramp_1_1", 4, 2, 2)
ramp("ramp_101_100", 6, 2, 2.02)
ramp("ramp_6_5", 8, 5, 6)
# A vertical wall facing +z at z=0.
quad("wall", (0, 0, 0), (10, 0, 0), (10, 3, 0), (0, 3, 0))
# A ceiling 3 m up, facing down.
quad("ceiling", (0, 3, 0), (10, 3, 0), (10, 3, 10), (0, 3, 10))
# The same 1:1 ramp authored with the wrong winding (b and c swapped).
tris.append(("ramp_1_1_flipped", (10, 0, 12), (12, 2, 12), (10, 0, 14)))
# A degenerate sliver: three points on a line.
tris.append(("sliver", (1, 0, 1), (2, 0, 2), (3, 0, 3)))

with open("level.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "ax", "ay", "az", "bx", "by", "bz", "cx", "cy", "cz"])
    for name, a, b, c in tris:
        w.writerow([name, *a, *b, *c])
print(len(tris), "triangles written")
