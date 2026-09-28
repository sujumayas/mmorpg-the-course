"""Checker for CS101 Lab 01. Run from this folder:  python check_lab01.py [file]"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "state.py"

# (keyboard input, expected STATUS fields)
CASES = [
    ("5\n2.5\n3\n", {"room": "hall", "gold": "995", "oil": "97.5", "level": "253", "lit": "True"}),
    ("20\n10\n10\n", {"room": "hall", "gold": "999", "oil": "90.0", "level": "4", "lit": "True"}),
    ("0\n0\n6\n", {"room": "hall", "gold": "990", "oil": "100.0", "level": "0", "lit": "True"}),
    ("9\n0.25\n262\n", {"room": "hall", "gold": "999", "oil": "99.8", "level": "0", "lit": "True"}),
]



def run(stdin):
    out = subprocess.run([sys.executable, str(TARGET)], input=stdin, capture_output=True,
                         text=True, timeout=10)
    if out.returncode != 0:
        return None, out.stderr.strip().splitlines()[-1] if out.stderr else "crashed"
    line = [l for l in out.stdout.splitlines() if "STATUS" in l]
    if not line:
        return None, "no STATUS line printed"
    fields = dict(p.split("=", 1) for p in line[-1].split("STATUS", 1)[1].split())
    return fields, None


def main():
    results = {"A types": [], "C lamp/room/oil": [], "D gold clamp": [], "E level wrap": []}
    for stdin, want in CASES:
        got, err = run(stdin)
        label = stdin.strip().replace("\n", ", ")
        if err:
            print(f"input [{label}]: ERROR {err}")
            for k in results:
                results[k].append(False)
            continue
        results["A types"].append(got.get("types") == "float,bool")
        results["C lamp/room/oil"].append(all(got.get(k) == want[k] for k in ("room", "oil", "lit")))
        results["D gold clamp"].append(got.get("gold") == want["gold"])
        results["E level wrap"].append(got.get("level") == want["level"])
        bad = {k: (got.get(k), v) for k, v in want.items() if got.get(k) != v}
        if bad:
            print(f"input [{label}]: " + "; ".join(f"{k} got {g} want {w}" for k, (g, w) in bad.items()))
    score = 0
    for part, oks in results.items():
        ok = all(oks)
        score += ok
        print(f"{'PASS' if ok else 'FAIL'}  Part {part}")
    print(f"{score}/{len(results)} parts pass")
    sys.exit(0 if score == len(results) else 1)


if __name__ == "__main__":
    main()
