#!/usr/bin/env python3
"""Turn a course's generated syllabus stub into its finished syllabus.

Usage:  .venv/bin/python tools/finish_syllabus.py MA101 [GD203 ...]

Regenerates the stub (so schedule links reflect every lecture and example on disk),
adds Labs and Assessments sections that link each file with its title, and removes
the stub marker so build_plan.py leaves the syllabus alone from then on.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_plan  # noqa: E402

ROOT = build_plan.ROOT


def title_of(path):
    for line in path.read_text().splitlines():
        if line.startswith("# "):
            return re.sub(r"^#\s*", "", line).strip()
    return path.stem


def finish(code):
    d = next((ROOT / "courses").glob(f"{code}-*"))
    syl = d / "syllabus.md"
    if build_plan.STUB_MARK not in syl.read_text():
        print(f"{code}: already finished, skipped")
        return
    build_plan.main()  # rewrites stubs with current links
    text = syl.read_text().replace(build_plan.STUB_MARK + "\n", "")
    labs = sorted(p for p in (d / "labs").glob("*.md"))
    asm = sorted((d / "assessments").glob("*.md"), key=lambda p: (p.name != "exam-bank.md", p.name))
    extra = ["## Labs", ""]
    extra += [f"- [{title_of(p)}](labs/{p.name})" for p in labs]
    extra += ["", "## Assessment materials", ""]
    extra += [f"- [{title_of(p)}](assessments/{p.name})" for p in asm]
    extra.append("")
    # Insert before the Readings section so the course-level material stays together.
    marker = "\n## Readings"
    block = "\n".join(extra)
    text = text.replace(marker, "\n" + block + marker, 1) if marker in text else text + "\n" + block
    syl.write_text(text)
    print(f"{code}: syllabus finished ({len(labs)} labs, {len(asm)} assessment files)")


if __name__ == "__main__":
    for c in sys.argv[1:]:
        finish(c)
