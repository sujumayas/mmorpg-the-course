"""Hot-reload demo for Lab 07. Works once Parts B and C pass.

Run:  python watch_demo.py
Then edit a file in assets/ in a text editor and save. The demo polls the
modification times once a second (as in CS102 week 13) and calls
ResourceManager.reload at the start of the next "frame". Ctrl+C to stop.
"""
import os
import time

import resources as r

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def read_file(path):
    with open(os.path.join(ASSETS, path)) as f:
        return f.read()


def main():
    manager = r.ResourceManager(read_file)
    names = sorted(n for n in os.listdir(ASSETS) if n.endswith(".tex"))
    handles = {n: manager.acquire(n) for n in names}
    mtimes = {n: os.path.getmtime(os.path.join(ASSETS, n)) for n in names}
    frame = 0
    while True:
        changed = []
        for n in names:
            m = os.path.getmtime(os.path.join(ASSETS, n))
            if m != mtimes[n]:
                mtimes[n] = m
                changed.append(n)
        for n in changed:                       # swap point: start of the frame
            ok = manager.reload(n)
            print(f"frame {frame}: {n} {'reloaded' if ok else 'kept previous (invalid file)'}")
        if frame % 5 == 0 or changed:
            print(f"frame {frame}: " + ", ".join(f"{n}={manager.get(h)}" for n, h in handles.items()))
        frame += 1
        time.sleep(1.0)


if __name__ == "__main__":
    main()
