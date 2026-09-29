"""PR101 Lab 03, part B: build a repository with the classic mistake.

Usage:
    python setup_lab03.py            # creates ./lab03-repo
    python setup_lab03.py --force    # deletes and recreates it

Three weeks of work on a small game were committed WITHOUT Git LFS:
8 PNG sprites (500,000 bytes), 2 WAV effects (1,000,000 bytes) and one
PSD source painting (2,000,000 bytes), each saved 3 times. Every binary
version is fully re-randomized, like a re-exported compressed file.
Needs Git 2.28+ and git-lfs 3.x on PATH. Standard-library Python 3.10+.
"""
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("lab03-repo")
ASSETS = ([(f"art/sprites/enemy_{i}.png", 500_000) for i in range(8)]
          + [("audio/sfx/jump.wav", 1_000_000), ("audio/sfx/hit.wav", 1_000_000),
             ("art/source/key_art.psd", 2_000_000)])
BOT = {"GIT_AUTHOR_NAME": "Setup Bot", "GIT_AUTHOR_EMAIL": "setup@lab03.invalid",
       "GIT_COMMITTER_NAME": "Setup Bot", "GIT_COMMITTER_EMAIL": "setup@lab03.invalid"}


def git(*args, date="2026-01-19T10:00:00"):
    env = dict(os.environ, **BOT, GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    subprocess.run(["git", *args], cwd=REPO, env=env, check=True, stdout=subprocess.DEVNULL)


def main():
    if REPO.exists():
        if "--force" not in sys.argv:
            sys.exit(f"{REPO} already exists. Use --force to recreate it.")
        shutil.rmtree(REPO)
    REPO.mkdir()
    git("init", "-q", "-b", "main")
    rng = random.Random(3)
    (REPO / "src").mkdir()
    (REPO / ".gitignore").write_text(".godot/\n")
    for week in range(1, 4):
        (REPO / "src/enemy.gd").write_text(
            "extends Node2D\n" + "".join(f"var tuning_{i} = {week * i}\n" for i in range(40)))
        for path, size in ASSETS:
            p = REPO / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(rng.randbytes(size))
        git("add", "-A", date=f"2026-01-{5 + 7 * week:02d}T10:00:00")
        git("commit", "-q", "-m", f"Week {week} art and audio pass",
            date=f"2026-01-{5 + 7 * week:02d}T10:00:00")
    print(f"Created {REPO}/ with 3 commits of binaries stored without LFS.")


if __name__ == "__main__":
    main()
