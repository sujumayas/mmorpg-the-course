"""PR101 Lab 02 checker. Run it on your practice repository.

Usage:
    python check_lab02.py lab02-repo

Prints PASS or FAIL for each check and exits 0 only when all pass.
"""
import re
import subprocess
import sys
from pathlib import Path

BAD_FIRST_WORDS = {"wip", "stuff", "misc", "update", "updates", "fix", "fixes"}
BOT_EMAIL = "setup@lab02.invalid"


def git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def is_ancestor(repo, a, b):
    return git(repo, "merge-base", "--is-ancestor", a, b)[0] == 0


def show(repo, path):
    code, out = git(repo, "show", f"HEAD:{path}")
    return out if code == 0 else ""


def checks(repo):
    results = []

    def add(name, ok, hint=""):
        results.append((name, bool(ok), hint))

    _, branch = git(repo, "branch", "--show-current")
    add("on branch main", branch == "main", f"currently on '{branch}'")
    _, status = git(repo, "status", "--porcelain")
    add("working tree clean", status == "", "commit or discard your changes")

    for b in ("feature/hud", "balance-pass"):
        code, _ = git(repo, "rev-parse", "--verify", "-q", b)
        add(f"{b} merged into main", code == 0 and is_ancestor(repo, b, "main"),
            f"git merge {b}")

    _, tip = git(repo, "rev-parse", "-q", "balance-pass")
    _, merges = git(repo, "log", "--merges", "--format=%P", "main")
    add("merge commit joins balance-pass", any(tip in line.split() for line in merges.splitlines()),
        "balance-pass must be merged with a merge commit, not rebased")

    _, files = git(repo, "ls-files")
    marked = [f for f in files.splitlines()
              if re.search(r"^(<{7}|={7}|>{7})", show(repo, f), re.M)]
    add("no conflict markers in tracked files", not marked, f"markers in {marked}")

    enemy = show(repo, "game/enemy.cfg")
    add("slime hp follows DECISIONS.md", re.search(r"^hp = 65$", enemy, re.M),
        "read DECISIONS.md")
    add("slime damage kept from balance-pass", re.search(r"^damage = 12$", enemy, re.M))
    add("HUD scale kept from feature/hud",
        re.search(r"^scale = 1\.5$", show(repo, "game/hud.cfg"), re.M))

    _, branches = git(repo, "branch", "--format=%(refname:short)")
    mine = [b for b in branches.splitlines() if re.fullmatch(r"feature/[a-z0-9-]+-doublejump", b)]
    add("your feature/<name>-doublejump branch exists", mine, "see step 4")
    add("your branch merged into main", mine and is_ancestor(repo, mine[0], "main"))
    add("double jump enabled in player.cfg",
        re.search(r"^double_jump = true$", show(repo, "game/player.cfg"), re.M))

    code, tag = git(repo, "rev-parse", "-q", "--verify", "v0.1^{commit}")
    _, head = git(repo, "rev-parse", "main")
    add("tag v0.1 on the tip of main", code == 0 and tag == head, "git tag v0.1")

    ignore = show(repo, ".gitignore")
    add(".gitignore ignores .godot/", re.search(r"^/?\.godot/?$", ignore, re.M))
    add("no .godot/ files tracked", not any(f.startswith(".godot/") for f in files.splitlines()),
        "git rm -r --cached .godot")

    _, log = git(repo, "log", "--no-merges", "--format=%ae%x09%s", "main")
    bad = []
    for line in log.splitlines():
        email, subject = line.split("\t", 1)
        if email == BOT_EMAIL:
            continue
        first = subject.split()[0].lower() if subject.split() else ""
        if (len(subject) > 72 or subject.endswith(".") or not subject[:1].isupper()
                or first in BAD_FIRST_WORDS or first.endswith("ed") or first.endswith("ing")):
            bad.append(subject)
    student = [l for l in log.splitlines() if not l.startswith(BOT_EMAIL)]
    add("you made at least 2 non-merge commits", len(student) >= 2)
    add("your commit messages follow the rules", not bad, f"fix: {bad}")
    return results


def main(argv):
    if len(argv) != 2 or not (Path(argv[1]) / ".git").exists():
        print(__doc__)
        return 2
    results = checks(argv[1])
    for name, ok, hint in results:
        print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not hint else f"  ({hint})"))
    passed = sum(ok for _, ok, _ in results)
    print(f"{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
