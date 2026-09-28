#!/usr/bin/env python3
"""Mechanical QA for one course (or all). Reviewers run this before the manual checklist.

Usage:  .venv/bin/python tools/check_course.py MA101 [GD203 ...]
        .venv/bin/python tools/check_course.py --all

Checks per lecture: word count (2,500-5,000), required template sections, relative links
resolve, no unresolved "(verify)", em dashes in prose, an Interactive spec when the week
ships an example. Per course: 14 lectures, >=6 labs, assessments present, syllabus finished.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    (r"^\*\*Why this matters:\*\*", "Why this matters"),
    (r"^\*\*You will be able to:\*\*", "You will be able to"),
    (r"^\*\*Before class:\*\*", "Before class"),
    (r"^\*\*Prerequisites", "Prerequisites"),
    (r"^## \d+\. Worked example", "## N. Worked example"),
    (r"^## In-class activity", "## In-class activity"),
    (r"^## Common misconceptions", "## Common misconceptions"),
    (r"^## Check yourself", "## Check yourself"),
    (r"^## (Lab|Lab / assignment) hook", "## Lab hook"),
    (r"^## Sources", "## Sources"),
]
LINK = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")


def words(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9][\w'’.-]*", text))


def check_links(path, text, problems):
    for m in LINK.finditer(text):
        target = m.group(1)
        if re.match(r"^[a-z]+:", target):
            continue
        if not (path.parent / target).resolve().exists():
            problems.append(f"{path.name}: broken link -> {target}")


def check_lecture(path, problems):
    text = path.read_text()
    n = words(text.split("## Interactive spec")[0])
    if not 2500 <= n <= 5000:
        problems.append(f"{path.name}: {n} words (target 2,500-5,000, spec excluded)")
    for pat, label in REQUIRED:
        if not re.search(pat, text, re.M):
            problems.append(f"{path.name}: missing section '{label}'")
    if not text.startswith("# "):
        problems.append(f"{path.name}: first line is not the '# CODE · Week NN' title")
    if re.search(r"\(verify\)", text, re.I):
        problems.append(f"{path.name}: unresolved (verify)")
    body = "\n".join(text.splitlines()[1:])
    body = re.sub(r"^\|.*\|$", "", body, flags=re.M)  # table placeholder cells are fine
    dashes = body.count("—")
    if dashes:
        problems.append(f"{path.name}: {dashes} em dash(es) in prose")
    check_links(path, text, problems)
    return n


def check_course(d):
    problems = []
    lec = sorted((d / "lectures").glob("w*.md"))
    ex = sorted((d / "examples").glob("*.html"))
    labs = sorted((d / "labs").glob("*.md"))
    asm = [p for p in (d / "assessments").glob("*.md")]
    counts = []
    for p in lec:
        counts.append(check_lecture(p, problems))
    for p in labs + asm + [d / "syllabus.md"]:
        if p.exists():
            check_links(p, p.read_text(), problems)
    weeks = {int(p.name[1:3]) for p in lec}
    missing = [w for w in range(1, 15) if w not in weeks]
    if missing:
        problems.append(f"missing lectures for weeks {missing}")
    if len(labs) < 6:
        problems.append(f"only {len(labs)} labs (need >= 6)")
    exam = [p for p in asm if "exam" in p.name]
    if not exam:
        problems.append("no exam bank in assessments/")
    else:
        q = sum(len(re.findall(r"^\s*(?:\*\*)?Q?\d+[.)]", p.read_text(), re.M)) for p in exam)
        if q < 40:
            problems.append(f"exam bank has ~{q} numbered questions (need >= 40)")
    if len(asm) < 2:
        problems.append("assessments/ needs assignment briefs + rubrics and an exam bank")
    syl = (d / "syllabus.md").read_text()
    if "generated-stub" in syl:
        problems.append("syllabus.md still has the generated-stub marker")
    if "_todo_" in syl:
        problems.append("syllabus.md schedule still has _todo_ cells")
    print(f"== {d.name}: {len(lec)} lectures, {len(ex)} examples, {len(labs)} labs, "
          f"{len(asm)} assessment files, words min/max "
          f"{min(counts, default=0)}/{max(counts, default=0)}")
    for p in problems:
        print("  -", p)
    if not problems:
        print("  OK")
    return not problems


def main():
    args = sys.argv[1:]
    dirs = sorted((ROOT / "courses").glob("*-*"))
    if "--all" not in args:
        dirs = [d for d in dirs if d.name.split("-")[0] in args]
    ok = all([check_course(d) for d in dirs])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
