"""Checks for CS201 Lab 14. Run from this folder: python test_reflect.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys

import reflect as r

results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"TODO: {exc} not written yet"
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


@r.component
class Lamp:  # declared here so a tool that names fields cannot pass
    color: str = r.prop("#ffcc88")
    lumens: int = r.prop(800, lo=0, hi=20_000)
    flicker: float = r.prop(0.0, lo=0.0, hi=1.0, edit=False)


def step1_inspector():
    got = r.inspector_rows(r.Spawner(waves=5))
    want = [("enemy", "goblin", None, None), ("waves", 5, 1, 20),
            ("interval_s", 8.0, 0.5, 120.0), ("radius", 4.0, 0.0, 50.0)]
    lamp = r.inspector_rows(Lamp())
    return (got, lamp) == (want, [("color", "#ffcc88", None, None), ("lumens", 800, 0, 20_000)]), \
        f"got {got} and {lamp}"


def step2_save():
    a = r.save(r.Health(current=80, last_hit_by=7))
    b = r.save(Lamp(lumens=1200))
    wa = {"type": "Health", "fields": {"current": 80, "maximum": 100, "regen_rate": 1.5}}
    wb = {"type": "Lamp", "fields": {"color": "#ffcc88", "lumens": 1200, "flicker": 0.0}}
    return (a, b) == (wa, wb), f"got {a} and {b}"


def step3_roundtrip():
    for obj in [r.Health(current=5, maximum=50, regen_rate=0.0), r.Spawner("orc", 2, 1.5, 0.0),
                r.Door(True, 42, 2.0), Lamp("#fff", 3, 0.5)]:
        back, warnings = r.load(r.save(obj))
        if warnings:
            return False, f"clean round trip of {obj} gave warnings {warnings}"
        if r.save(back) != r.save(obj):
            return False, f"{obj} came back as {back}"
    return True, ""


def step3_warnings():
    data = {"type": "Spawner", "fields": {"enemy": "orc", "waves": 40, "interval": 3.0,
                                          "colour": "red", "radius": -2.0}}
    obj, warnings = r.load(data, {"Spawner.interval": "interval_s"})
    want_obj = r.Spawner(enemy="orc", waves=20, interval_s=3.0, radius=0.0)
    want_w = ["Spawner.waves: 40 clamped to 20", "Spawner.colour: not declared",
              "Spawner.radius: -2.0 clamped to 0.0"]
    if r.save(obj) != r.save(want_obj):
        return False, f"object {obj}, want {want_obj}"
    return warnings == want_w, f"warnings {warnings}, want {want_w}"


def step3_runtime_field_not_loaded():
    obj, warnings = r.load({"type": "Health", "fields": {"current": 3, "last_hit_by": 9}})
    ok = obj.last_hit_by == 0 and warnings == ["Health.last_hit_by: not declared"]
    return ok, f"last_hit_by {obj.last_hit_by}, warnings {warnings}"


def step4_diff():
    got = r.diff(r.Door(), r.Door(locked=True, key_id=7))
    same = r.diff(r.Health(last_hit_by=1), r.Health(last_hit_by=2))
    try:
        r.diff(r.Door(), r.Health())
        raised = False
    except TypeError:
        raised = True
    ok = got == [("locked", False, True), ("key_id", 0, 7)] and same == [] and raised
    return ok, f"got {got}, runtime-only diff {same}, TypeError raised: {raised}"


def step5_transactions():
    h = r.History()
    sp = r.Spawner()
    if h.undo() is not None:
        return False, "undo on an empty history should return None"
    h.begin("drag waves")
    for v in range(3, 30):
        h.set(sp, "waves", v)
    h.end()
    if sp.waves != 20:
        return False, f"set should clamp to the field's range: waves {sp.waves}, want 20"
    h.begin("empty")
    h.end()
    h.begin("multi")
    doors = [r.Door() for _ in range(3)]
    for d in doors:
        h.set(d, "key_id", 5)
    h.set(sp, "radius", 9.0)
    h.end()
    steps = [h.undo(), (sp.radius, [d.key_id for d in doors]),
             h.undo(), sp.waves, h.undo(),
             h.redo(), sp.waves, h.redo(), sp.radius, h.redo()]
    want = ["multi", (4.0, [0, 0, 0]), "drag waves", 3, None,
            "drag waves", 20, "multi", 9.0, None]
    return steps == want, f"got {steps}, want {want}"


def step5_redo_cleared():
    h = r.History()
    d = r.Door()
    h.begin("a"); h.set(d, "key_id", 1); h.end()
    h.undo()
    h.begin("b"); h.set(d, "key_id", 2); h.end()
    try:
        h.set(d, "key_id", 3)
        outside = False
    except RuntimeError:
        outside = True
    ok = h.redo() is None and d.key_id == 2 and outside
    return ok, f"redo after a new edit should be None; key_id {d.key_id}; RuntimeError outside: {outside}"


check("step 1: inspector rows from descriptors", step1_inspector)
check("step 2: save only save=True fields", step2_save)
check("step 3: load round-trips every component", step3_roundtrip)
check("step 3: redirects, clamping and unknown keys", step3_warnings)
check("step 3: runtime-only fields are not loaded", step3_runtime_field_not_loaded)
check("step 4: field-by-field diff", step4_diff)
check("step 5: transactions, undo and redo", step5_transactions)
check("step 5: a new edit clears redo", step5_redo_cleared)
print(f"{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
