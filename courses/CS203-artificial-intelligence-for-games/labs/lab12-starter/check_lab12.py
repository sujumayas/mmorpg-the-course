"""Checks for CS203 Lab 12. Run: python check_lab12.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys

import mob as m

results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def radius():
    got = [m.aggro_radius(mob, 30) for mob in (10, 25, 30, 38, 55, 70)] + [m.aggro_radius(38, 42)]
    want = [5, 15, 20, 28, 45, 45, 16]
    return got == want, f"got {got}, want {want}"


def adding():
    t = m.ThreatTable()
    t.add_damage("tank", 200, 1.3)
    t.add_damage("tank", 100, 1.15)
    t.add_heal("healer", 600, 3)
    t.add_heal("healer", 600)
    got = (t.threat.get("tank"), t.threat.get("healer"))
    return got == (375, 400), f"got {got}, want (375, 400)"


def switching():
    t = m.ThreatTable()
    for who, amt in (("tank", 1000), ("rogue", 1100), ("healer", 1250)):
        t.add_damage(who, amt)
    first = t.choose({"tank", "rogue"})          # healer is highest, no target yet
    t2 = m.ThreatTable()
    for who, amt in (("tank", 1000), ("rogue", 1000), ("healer", 1000)):
        t2.add_damage(who, amt)
    t2.target = "tank"
    t2.add_damage("rogue", 100)                  # 1100: exactly 110%, no switch
    t2.add_damage("healer", 290)                 # 1290: under 130%, no switch
    a = t2.choose({"tank", "rogue"})
    t2.add_damage("rogue", 1)                    # 1101 > 110%
    t2.add_damage("healer", 20)                  # 1310 > 130%, and highest
    b = t2.choose({"tank", "rogue"})
    empty = m.ThreatTable().choose(set())
    got = (first, a, b, empty)
    return got == ("healer", "tank", "healer", None), f"got {got}, want ('healer', 'tank', 'healer', None)"


def taunting():
    t = m.ThreatTable()
    t.add_damage("tank", 1600)
    t.add_damage("healer", 2100)
    t.target = "healer"
    t.taunt("tank", now=8, duration=3)
    locked = [t.choose({"tank"}, now=s) for s in (8, 9, 10)]
    t.add_damage("healer", 5000)
    after = t.choose({"tank"}, now=11)
    ok = t.threat["tank"] == 2100 and locked == ["tank"] * 3 and after == "healer"
    return ok, f"tank {t.threat.get('tank')} (want 2100), locked {locked}, after {after}"


def removing():
    t = m.ThreatTable()
    for who, amt in (("tank", 3000), ("rogue", 1500), ("healer", 1400)):
        t.add_damage(who, amt)
    t.choose({"tank", "rogue"})
    t.remove("tank")
    t.remove("nobody")
    got = t.choose({"rogue"})
    return got == "rogue" and "tank" not in t.threat, f"after tank dies target {got}, want rogue"


def flicker():
    got = (m.flicker(False), m.flicker(True))
    return got == (60, 3), f"got {got}, want (60, 3)"


def healer():
    got = tuple(m.healer_pull(x, 600, 200) for x in (1.0, 1.1, 1.15, 1.2)) + (m.healer_pull(1.0, 600, 200, mobs=2),)
    want = (8, 22, 301, None, None)
    if got != want:
        return False, f"healer_pull got {got}, want {want}"
    ms = m.min_safe_multiplier(600, 200)
    return ms == 1.16, f"min_safe_multiplier(600, 200) = {ms}, want 1.16"


def fsm():
    mob = m.Mob(level=30, spawn=(0, 0), leash=40)
    s1 = mob.update({"far": ((25, 0), 30)})              # outside 20 yd
    s2 = mob.update({"near": ((19, 0), 30)})             # inside
    ok_combat = s1 == "IDLE" and s2 == "COMBAT" and mob.table.threat.get("near") == 0
    mob.take_damage("near", 300)
    mob.pos = (41, 0)                                    # chased too far
    s3 = mob.update({"near": ((45, 0), 30)})
    evading = s3 == "EVADE" and mob.hp == 1000 and mob.table.threat == {}
    mob.take_damage("near", 500)                         # ignored while evading
    s4 = mob.update({"near": ((45, 0), 30)})
    home = s4 == "IDLE" and mob.pos == (0, 0) and mob.hp == 1000
    return ok_combat and evading and home, \
        f"states {s1, s2, s3, s4}, hp {mob.hp}, pos {mob.pos}"


check("step 1: aggro_radius follows the rule of thumb", radius)
check("step 2: damage x multiplier and split healing threat", adding)
check("step 2: 110% melee / 130% ranged switch rule, highest challenger wins", switching)
check("step 3: taunt sets threat to the maximum and locks the target", taunting)
check("step 3: removing the target falls back to the highest remaining", removing)
check("step 3: flicker counts match the lecture (60 without margin, 3 with)", flicker)
check("step 4: healer_pull and min_safe_multiplier match the lecture", healer)
check("step 5: IDLE -> COMBAT -> EVADE -> IDLE with reset and immunity", fsm)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
