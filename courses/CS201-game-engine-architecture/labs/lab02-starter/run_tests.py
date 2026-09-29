"""Build and run the Lab 02 tests.

Usage:
    python run_tests.py          # UndefinedBehaviorSanitizer if available
    python run_tests.py --asan   # also AddressSanitizer (catches double frees and leaks)

Falls back to a plain debug build when the compiler does not support the
sanitizers (for example MinGW on Windows). Exit code 0 means every test passed.
Set the CXX environment variable to choose a compiler (default: c++).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "test_lab02"
EXE = HERE / (NAME + (".exe" if os.name == "nt" else ""))
TIMEOUT_S = 60


def build(asan):
    cxx = os.environ.get("CXX") or shutil.which("c++") or shutil.which("g++") or shutil.which("clang++")
    if not cxx:
        sys.exit("No C++ compiler found. Install clang or g++, or set CXX.")
    base = [cxx, "-std=c++20", "-Wall", "-Wextra", "-g", str(HERE / f"{NAME}.cpp"), "-o", str(EXE)]
    san = "address,undefined" if asan else "undefined"
    last = ""
    for extra in ([f"-fsanitize={san}", "-fno-omit-frame-pointer"], []):
        result = subprocess.run(base + extra, capture_output=True, text=True)
        if result.returncode == 0:
            print("built with", " ".join(extra) or "no sanitizers", flush=True)
            if result.stderr.strip():
                print(result.stderr)
            return
        last = result.stderr
    print(last)
    sys.exit("Build failed.")


if __name__ == "__main__":
    build("--asan" in sys.argv[1:])
    try:
        code = subprocess.run([str(EXE)], timeout=TIMEOUT_S).returncode
    except subprocess.TimeoutExpired:
        sys.exit(f"Tests did not finish in {TIMEOUT_S} s. Look for an infinite loop, "
                 "or run without --asan if AddressSanitizer is broken on your machine.")
    sys.exit(code)
