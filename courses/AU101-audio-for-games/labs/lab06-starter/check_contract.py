"""AU101 Lab 06: validate an engine event contract.

Usage:  python check_contract.py [engine_contract.json]
Prints PASS or FAIL for each check and exits with status 0 only if all pass.

Curves are lists of [rpm, gain] points with gain as a linear amplitude from 0 to 1,
interpolated linearly between points and held flat beyond the first and last point
(as a curve editor does). Outside a loop's curve points the loop is silent only if
the end point's gain is 0.

Checks
1. complete     required fields present, no "TODO" left anywhere
2. structure    event path, type, parameter range, curve points sorted and in 0..1
3. level        total level 10*log10(sum of gain^2) within +/-1.5 dB of 0 dB
                at every RPM from min to max in steps of 10
4. stretch      every loop with gain >= 0.1 (-20 dB) is within +/-6.0 semitones
                of its recorded RPM, at every RPM step
5. seek         both seek speeds are numbers > 0; a full rise takes at most 1.0 s;
                falling is no faster than rising
"""
import json
import math
import sys

LEVEL_TOLERANCE_DB = 1.5
MAX_STRETCH_ST = 6.0
AUDIBLE_GAIN = 0.1
STEP = 10


def gain_at(curve, rpm):
    if rpm <= curve[0][0]:
        return curve[0][1]
    if rpm >= curve[-1][0]:
        return curve[-1][1]
    for (x0, y0), (x1, y1) in zip(curve, curve[1:]):
        if x0 <= rpm <= x1:
            if x1 == x0:
                return y1
            return y0 + (y1 - y0) * (rpm - x0) / (x1 - x0)
    raise ValueError("curve not sorted")


def has_todo(obj):
    if isinstance(obj, str):
        return "TODO" in obj
    if isinstance(obj, dict):
        return any(has_todo(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_todo(v) for v in obj)
    return False


def check_complete(c):
    need = ["event", "type", "bank", "owner", "parameters", "loops"]
    missing = [k for k in need if k not in c]
    if missing:
        return f"missing fields {missing}"
    if c.get("type") == "persistent" and not c.get("stop_when"):
        return "a persistent event needs 'stop_when'"
    if has_todo(c):
        return "some fields still contain TODO"
    return None


def rpm_param(c):
    return next((p for p in c["parameters"] if p.get("name") == "RPM"), None)


def check_structure(c):
    if not str(c["event"]).startswith("event:/"):
        return "event path must start with 'event:/'"
    if c["type"] not in ("one-shot", "persistent"):
        return "type must be 'one-shot' or 'persistent'"
    p = rpm_param(c)
    if p is None or p.get("kind") != "continuous":
        return "needs a continuous parameter named RPM"
    if not p["min"] < p["max"]:
        return "RPM min must be below max"
    if len(c["loops"]) < 2:
        return "needs at least two loops"
    for loop in c["loops"]:
        pts = loop["gain_curve"]
        if not p["min"] <= loop["recorded_rpm"] <= p["max"]:
            return f"{loop['file']}: recorded_rpm outside the parameter range"
        if len(pts) < 2 or any(a[0] > b[0] for a, b in zip(pts, pts[1:])):
            return f"{loop['file']}: curve needs 2+ points sorted by rpm"
        if any(not 0 <= g <= 1 for _, g in pts):
            return f"{loop['file']}: gains must be between 0 and 1"
    return None


def sweep(c):
    p = rpm_param(c)
    rpm = p["min"]
    while rpm <= p["max"]:
        yield rpm, [(loop, gain_at(loop["gain_curve"], rpm)) for loop in c["loops"]]
        rpm += STEP


def check_level(c):
    worst = None
    for rpm, gains in sweep(c):
        power = sum(g * g for _, g in gains)
        db = -math.inf if power == 0 else 10 * math.log10(power)
        if worst is None or abs(db) > abs(worst[1]):
            worst = (rpm, db)
    if abs(worst[1]) > LEVEL_TOLERANCE_DB:
        return f"level {worst[1]:+.2f} dB at {worst[0]} rpm (allowed +/-{LEVEL_TOLERANCE_DB})"
    return None


def check_stretch(c):
    worst = (0, 0.0, "")
    for rpm, gains in sweep(c):
        for loop, g in gains:
            if g >= AUDIBLE_GAIN:
                st = 12 * math.log2(rpm / loop["recorded_rpm"])
                if abs(st) > abs(worst[1]):
                    worst = (rpm, st, loop["file"])
    if abs(worst[1]) > MAX_STRETCH_ST:
        return f"{worst[2]} stretched {worst[1]:+.2f} st at {worst[0]} rpm (allowed +/-{MAX_STRETCH_ST})"
    return None


def check_seek(c):
    p = rpm_param(c)
    up, down = p.get("seek_up_range_per_s"), p.get("seek_down_range_per_s")
    if not all(isinstance(v, (int, float)) and v > 0 for v in (up, down)):
        return "seek speeds must be positive numbers (range per second)"
    if 1 / up > 1.0:
        return f"a full rise takes {1 / up:.2f} s (at most 1.0 s)"
    if down > up:
        return "falling faster than rising: the player's own input should be the fastest change"
    return None


CHECKS = [("complete", check_complete), ("structure", check_structure),
          ("level", check_level), ("stretch", check_stretch), ("seek", check_seek)]


def main(path):
    with open(path) as f:
        contract = json.load(f)
    ok = True
    for name, fn in CHECKS:
        try:
            problem = fn(contract)
        except (KeyError, TypeError, ValueError) as e:
            problem = f"could not check ({type(e).__name__}: {e})"
        print(("PASS " if problem is None else "FAIL ") + name + ("" if problem is None else " - " + problem))
        ok = ok and problem is None
    print("contract OK" if ok else "contract has problems")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "engine_contract.json"))
