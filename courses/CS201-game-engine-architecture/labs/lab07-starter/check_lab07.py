"""Checks for CS201 Lab 07. Run from this folder:  python check_lab07.py
Each check prints PASS, FAIL (with the reason) or TODO. Exit code 0 only if all pass."""
import sys

import resources as r

results = []


def check(name):
    def wrap(fn):
        try:
            fn()
            results.append(("PASS", name, ""))
        except NotImplementedError as e:
            results.append(("TODO", name, str(e)))
        except AssertionError as e:
            results.append(("FAIL", name, str(e)))
        except Exception as e:  # a crash is a failure too
            results.append(("FAIL", name, f"{type(e).__name__}: {e}"))
        return fn
    return wrap


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def fake_disk(files):
    def read(path):
        return files[path]
    return read


@check("A1 load_time")
def _():
    assert close(r.load_time(400, 200, 15, 100), 8.0), "400 reads of 200 MB on the laptop HDD should take 8.0 s"
    assert close(r.load_time(1, 200, 0.1, 5500), 0.0001 + 200 / 5500), "one SSD read of 200 MB"
    assert close(r.load_time(0, 0, 15, 100), 0.0), "no reads, no time"


@check("A2 knee_mb")
def _():
    assert close(r.knee_mb(15, 100), 1.5), "laptop HDD knee is 1.5 MB"
    assert close(r.knee_mb(0.1, 5500), 0.55), "SSD knee is 0.55 MB"


@check("A3 pack_or_loose")
def _():
    loose, packed, speedup = r.pack_or_loose([0.04] * 120, 15, 100)
    assert close(loose, 1.848), f"loose should be 1.848 s, got {loose}"
    assert close(packed, 0.063), f"packed should be 0.063 s, got {packed}"
    assert close(speedup, 1.848 / 0.063), "speedup is loose / packed"


@check("B1 acquire loads once and returns equal handles")
def _():
    m = r.ResourceManager(fake_disk({"goblin.tex": "64x64 green", "ogre.tex": "128x128 grey"}))
    hs = [m.acquire("goblin.tex") for _ in range(500)]
    assert len(set(hs)) == 1, "500 acquires of one path must return equal handles"
    ogre = m.acquire("ogre.tex")
    assert m.disk_reads == 2, f"expected 2 disk reads, got {m.disk_reads}"
    assert ogre != hs[0], "different paths need different handles"
    assert m.get(ogre) == {"w": 128, "h": 128, "color": "grey"}


@check("B2 release frees at zero and old handles go stale")
def _():
    m = r.ResourceManager(fake_disk({"a.tex": "8x8 red", "b.tex": "16x16 blue"}))
    a1 = m.acquire("a.tex")
    a2 = m.acquire("a.tex")
    m.release(a1)
    assert m.refs("a.tex") == 1 and m.get(a2) is not None, "one reference left, still resident"
    m.release(a2)
    assert m.refs("a.tex") == 0, "count should reach zero"
    assert m.get(a1) is None, "handle to a freed resource must be stale"
    b = m.acquire("b.tex")
    assert b.index == a1.index, "the freed slot should be reused"
    assert b.generation == a1.generation + 1, "reused slot must have a new generation"
    assert m.get(a1) is None, "stale handle must not see the new occupant"
    try:
        m.release(a1)
    except ValueError:
        pass
    else:
        raise AssertionError("releasing a stale handle must raise ValueError")


@check("B3 re-acquire after free reads the disk again")
def _():
    m = r.ResourceManager(fake_disk({"a.tex": "8x8 red"}))
    m.release(m.acquire("a.tex"))
    h = m.acquire("a.tex")
    assert m.disk_reads == 2, "freed at zero, so the second acquire must read again"
    assert m.get(h)["color"] == "red"


@check("B4 a bad file at acquire changes nothing")
def _():
    m = r.ResourceManager(fake_disk({"bad.tex": "63x64 red", "ok.tex": "4x4 red"}))
    try:
        m.acquire("bad.tex")
    except ValueError:
        pass
    else:
        raise AssertionError("63 is not a power of two, acquire must raise ValueError")
    assert m.refs("bad.tex") == 0, "a failed load must not become resident"
    h = m.acquire("ok.tex")
    assert h.index == 0, "a failed load must not use up a slot"


@check("C1 reload swaps in place and keeps the last good data")
def _():
    files = {"rock.tex": "64x64 grey"}
    m = r.ResourceManager(fake_disk(files))
    hs = [m.acquire("rock.tex") for _ in range(300)]
    files["rock.tex"] = "128x128 mossy"
    assert m.reload("rock.tex") is True, "valid file must reload"
    assert all(m.get(h) == {"w": 128, "h": 128, "color": "mossy"} for h in hs), "all 300 handles must see new data"
    files["rock.tex"] = "128x12 mossy"          # half-typed save
    assert m.reload("rock.tex") is False, "invalid file must not reload"
    assert m.get(hs[0])["h"] == 128, "keep the last good data"
    assert m.refs("rock.tex") == 300, "reload must not change reference counts"
    reads = m.disk_reads
    assert m.reload("never_loaded.tex") is False and m.disk_reads == reads, "non-resident reload reads nothing"


@check("C2 rebuild_order is a topological order")
def _():
    uses = {
        "mat/rock": ["shader/lit", "tex/rock"],
        "mat/moss": ["shader/lit", "tex/moss"],
        "mat/ui": ["shader/unlit", "tex/ui_atlas"],
        "model/cliff": ["mat/rock", "mat/moss"],
    }
    assert r.rebuild_order("shader/lit", uses) == ["mat/moss", "mat/rock", "model/cliff"]
    assert r.rebuild_order("tex/ui_atlas", uses) == ["mat/ui"]
    assert r.rebuild_order("model/cliff", uses) == [], "nothing uses the cliff"
    diamond = {"a/model": ["shader", "z/mat"], "z/mat": ["shader"]}
    got = r.rebuild_order("shader", diamond)
    assert got == ["z/mat", "a/model"], f"a/model uses z/mat, so z/mat must come first; got {got}"


@check("C3 rebuild_order reports a cycle")
def _():
    uses = {"mat/a": ["shader", "mat/b"], "mat/b": ["mat/a"]}
    try:
        r.rebuild_order("shader", uses)
    except ValueError as e:
        assert "cycle" in str(e), "message must say 'cycle'"
    else:
        raise AssertionError("a cycle must raise ValueError")


if __name__ == "__main__":
    width = max(len(n) for _, n, _ in results)
    for status, name, why in results:
        print(f"{status:4}  {name:<{width}}  {why}")
    passed = sum(s == "PASS" for s, _, _ in results)
    print(f"\n{passed}/{len(results)} checks pass")
    sys.exit(0 if passed == len(results) else 1)
