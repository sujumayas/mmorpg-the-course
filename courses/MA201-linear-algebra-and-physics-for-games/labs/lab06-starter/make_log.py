"""Regenerates platform_log.csv (already provided). Do not read before step 5.

A platform slides back and forth, x_p(t) = 260 sin(pi t / 4) px, half-width 40 px.
The player stands at its center and jumps at t = 0.5 s and t = 2.0 s with Godot's
template jump (400 px/s, gravity 980 px/s^2) and platform_on_leave = ADD_VELOCITY.
Positions are logged at 60 Hz, rounded to the nearest pixel (error up to 0.5 px).
"""
import csv, math

A, W, HALF, G, JUMP, HZ = 260.0, math.pi / 4, 40.0, 980.0, 400.0, 60
JUMPS = (0.5, 2.0)

def xp(t):
    return A * math.sin(W * t)

def vp(t):
    return A * W * math.cos(W * t)

rows, rel, state = [], 0.0, None       # state: None on platform, else (t0, x0, vx) in air
for i in range(int(3.5 * HZ) + 1):
    t = i / HZ
    if state is None and any(abs(t - j) < 1e-9 for j in JUMPS):
        state = (t, xp(t) + rel, vp(t))
    if state is None:
        px, py = xp(t) + rel, 0.0
    else:
        t0, x0, vx = state
        tau = t - t0
        px, py = x0 + vx * tau, JUMP * tau - 0.5 * G * tau * tau
        if py <= 0 and tau > 0.1 and abs(px - xp(t)) <= HALF:
            rel, state, py = px - xp(t), None, 0.0
    rows.append((f"{t:.4f}", round(xp(t)), round(px), round(py)))

with open("platform_log.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["t", "platform_x", "player_x", "player_y"])
    w.writerows(rows)
