"""Checks for CS201 Lab 13. Run from this folder: python test_frameprof.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys

import frameprof as fp

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


def step1_self_times():
    st = fp.self_times(fp.simulated_frame())
    want = {"frame": 0, "input": 400, "gameplay": 0, "scripts": 2_700, "triggers": 900,
            "ai": 2_000, "physics": 600, "broadphase": 900, "solver": 1_500,
            "animation": 2_200, "audio": 500, "ui": 1_000, "render_submit": 0,
            "cull": 1_300, "draw_calls": 2_800}
    return st == want, f"got {st}"


def step1_repeated_names():
    ev = []
    clock = fp.FakeClock()
    prof = fp.Profiler(clock, fp.MAIN, ev)
    with prof.scope("frame"):
        for _ in range(3):
            with prof.scope("spawn"):
                clock.work(100)
                with prof.scope("alloc"):
                    clock.work(50)
    st = fp.self_times(ev)
    want = {"frame": 0, "spawn": 300, "alloc": 150}
    return st == want, f"got {st}, want {want}"


def step2_overhead():
    measured = {"script_update": 3_630_000, "solver": 3_000_400, "vec_normalize": 2_400_000,
                "update_transform": 2_200_000, "tiny": 100}
    calls = {"script_update": 600, "solver": 8, "vec_normalize": 40_000,
             "update_transform": 20_000, "tiny": 10}
    got = fp.correct_overhead(measured, calls, 50)
    want = {"script_update": 3_600_000, "solver": 3_000_000, "vec_normalize": 400_000,
            "update_transform": 1_200_000, "tiny": 0}
    return got == want, f"got {got}, want {want}"


def step3_frames_needed():
    cases = [((400_000, 8_000, 10), 32), ((800_000, 10_000, 5), 50), ((750_000, 1_000, 10), 134),
             ((3_600_000, 8_000, 2), 87), ((400_000, 8_000, 2), 782), ((10_000_000, 10_000, 100), 1)]
    bad = [(args, fp.frames_needed(*args), want) for args, want in cases
           if fp.frames_needed(*args) != want]
    if bad:
        return False, f"(args, got, want): {bad}"
    return isinstance(fp.frames_needed(400_000, 8_000, 10), int), "return an int"


def step3_bottleneck():
    a = fp.bottleneck({"game": 12_700, "render": 4_100, "gpu": 11_000})
    b = fp.bottleneck({"game": 8_700, "render": 4_100, "gpu": 11_000})
    return (a, b) == (("game", 12_700), ("gpu", 11_000)), f"got {a}, {b}"


def step4_percentile():
    frames = [14_000] * 118 + [48_000, 52_000]
    got = (fp.percentile(frames, 50), fp.percentile(frames, 99), fp.percentile(frames, 100),
           fp.percentile([5, 1, 3], 1), fp.percentile(frames, 98))
    want = (14_000, 48_000, 52_000, 1, 14_000)
    return got == want, f"got {got}, want {want}"


def step5_trace():
    ev = fp.simulated_frame()
    tr = fp.to_trace(ev)
    if len(tr) != 2 * len(ev):
        return False, f"{len(tr)} trace events for {len(ev)} scopes, want {2 * len(ev)}"
    keys = {"name", "ph", "ts", "pid", "tid"}
    if any(set(e) != keys for e in tr):
        return False, "every event needs exactly name, ph, ts, pid, tid"
    stacks = {}
    last_ts = {}
    for e in tr:  # replay: every E must close the innermost open B on its thread
        st = stacks.setdefault(e["tid"], [])
        if e["ts"] < last_ts.get(e["tid"], 0):
            return False, "events are not ordered by ts"
        last_ts[e["tid"]] = e["ts"]
        if e["ph"] == "B":
            st.append(e["name"])
        elif not st or st.pop() != e["name"]:
            return False, f"E for {e['name']} at ts {e['ts']} does not close the innermost scope"
    if any(stacks.values()):
        return False, "some scopes are never closed"
    first = [e["name"] for e in tr if e["tid"] == fp.MAIN][:3]
    return first == ["frame", "input", "input"], f"main thread starts {first}, want frame, input, input"


check("step 1: self times of the lecture frame", step1_self_times)
check("step 1: repeated scope names are summed", step1_repeated_names)
check("step 2: overhead correction", step2_overhead)
check("step 3: frames of capture for a target error", step3_frames_needed)
check("step 4: the slowest thread sets the pace", step3_bottleneck)
check("step 5: nearest-rank percentiles", step4_percentile)
check("step 6: Chrome trace B/E events nest", step5_trace)
print(f"{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
