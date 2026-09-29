"""Regenerates turret_keys.csv (already provided). Kept so you can see how the
'exporter' wrote the file: it forces w >= 0 on every key, a common convention."""
import csv, math, random
random.seed(5)
yaw, rows = 150.0, []
for i in range(41):
    h = math.radians(yaw) / 2
    q = (math.cos(h), 0.0, math.sin(h), 0.0)
    if q[0] < 0:
        q = tuple(-c for c in q)
    rows.append((round(i * 0.5, 2), round(yaw, 3), *[round(c, 6) for c in q]))
    yaw += random.uniform(-35, 45)
with open("turret_keys.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["time", "yaw_deg_unwrapped", "qw", "qx", "qy", "qz"])
    w.writerows(rows)
