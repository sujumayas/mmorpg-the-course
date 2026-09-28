"""Checker for CS101 Lab 03. Run from this folder:  python check_lab03.py [cave_file] [invaders_file]"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAVE = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "loop_cave.py"
INV = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "invaders.py"


def run(path, stdin):
    try:
        out = subprocess.run([sys.executable, str(path)], input=stdin, capture_output=True,
                             text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return ["ERROR timed out (infinite loop?)"]
    lines = []
    for l in out.stdout.splitlines():
        l = l.split("> ")[-1].split(": ")[-1].strip()
        if l:
            lines.append(l)
    if out.returncode != 0:
        err = out.stderr.strip().splitlines()[-1] if out.stderr else "crashed"
        lines.append("ERROR " + err)
    return lines


CAVE_CASES = {
    "Part A loop": [
        ("north\nsouth\nnorth\nquit\n", ["ROOM hall", "ROOM entrance", "ROOM hall", "QUIT"]),
        ("dance\nnorth\nwest\neast\nquit\n", ["BLOCKED", "ROOM hall", "ROOM well", "ROOM hall", "QUIT"]),
    ],
    "Part B key and vault": [
        ("north\nnorth\nquit\n", ["ROOM hall", "LOCKED", "QUIT"]),
        ("north\neast\ntake key\nwest\nnorth\nquit\n",
         ["ROOM hall", "ROOM armory", "KEY", "ROOM hall", "ROOM vault", "WIN in 5 moves"]),
        ("take key\nquit\n", ["BLOCKED", "QUIT"]),
    ],
    "Part C win and lose": [
        ("north\neast\ntake key\nwest\nnorth\n", ["ROOM hall", "ROOM armory", "KEY", "ROOM hall",
                                                "ROOM vault", "WIN in 5 moves"]),
        ("dance\n" * 15 + "quit\n", ["BLOCKED"] * 15 + ["LOSE lamp out"]),
        ("dance\n" * 10 + "north\neast\ntake key\nwest\nnorth\nquit\n",
         ["BLOCKED"] * 10 + ["ROOM hall", "ROOM armory", "KEY", "ROOM hall", "ROOM vault", "WIN in 15 moves"]),
    ],
}

INV_CASES = [  # alive, fps, per_frame, frames
    (55, 60, 1, 165), (28, 60, 1, 84), (11, 60, 1, 33), (1, 60, 1, 3),
    (20, 30, 1, 60), (55, 60, 2, 84), (11, 60, 2, 18), (1, 60, 2, 3),
]


def main():
    passed = 0
    for name, cases in CAVE_CASES.items():
        ok = True
        for stdin, want in cases:
            got = run(CAVE, stdin)
            if got != want:
                ok = False
                print(f"  {name}: commands {stdin.strip().splitlines()[:6]}...\n    got  {got}\n    want {want}")
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        passed += ok
    ok = True
    for alive, fps, per, frames in INV_CASES:
        seconds = frames / fps
        want = f"FRAMES {frames} SECONDS {seconds:.3f} SPEED {3 * 2 / seconds:.2f}"
        got = run(INV, f"{alive}\n{fps}\n{per}\n")
        if not got or got[-1] != want:
            ok = False
            print(f"  Part D: alive={alive} fps={fps} per_frame={per} got '{got[-1] if got else ''}' want '{want}'")
    print(f"{'PASS' if ok else 'FAIL'}  Part D frame loop")
    passed += ok
    print(f"{passed}/4 parts pass")
    sys.exit(0 if passed == 4 else 1)


if __name__ == "__main__":
    main()
