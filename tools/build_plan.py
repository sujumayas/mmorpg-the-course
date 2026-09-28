#!/usr/bin/env python3
"""Generate PLAN.md and courses/<CODE>-<slug>/syllabus.md from curriculum.yaml.

Run from repo root:  python tools/build_plan.py
Syllabi are only (re)written when they are still the generated stub, so hand-edited
syllabi are never overwritten.
"""
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
STUB_MARK = "<!-- generated-stub: safe to overwrite -->"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def course_dir(c):
    return ROOT / "courses" / f"{c['code']}-{slug(c['title'])}"


def main():
    data = yaml.safe_load((ROOT / "curriculum.yaml").read_text())
    prog, courses = data["program"], data["courses"]
    by_sem = {}
    for c in courses:
        by_sem.setdefault(c["semester"], []).append(c)

    out = [f"# {prog['name']} — Program Plan", "",
           "_Generated from `curriculum.yaml` by `tools/build_plan.py`. Edit the YAML, not this file._", "",
           "## Structure", ""]
    out += [f"- {s}" for s in prog["structure"]]
    out += ["", f"{prog['years']} years · {prog['semesters']} semesters · {prog['weeks_per_semester']} weeks each · "
            f"{len(courses)} courses · {sum(c['credits'] for c in courses)} credits", "",
            "### Reference stack", ""]
    out += [f"- **{k.replace('_', ' ')}**: {v}" for k, v in prog["reference_stack"].items()]

    out += ["", "## Curriculum map", "", "| Sem | Year | Courses |", "|---|---|---|"]
    for s in sorted(by_sem):
        cs = by_sem[s]
        out.append(f"| {s} | {cs[0]['year']} | " + "<br>".join(f"{c['code']} {c['title']}" for c in cs) + " |")

    out += ["", "## Prerequisite graph", "", "```mermaid", "flowchart LR"]
    for c in courses:
        for p in c["prereqs"]:
            out.append(f"  {p} --> {c['code']}")
    out += ["```", "", "## Build status", "",
            "| Course | Syllabus | Lectures written | Worked examples built |", "|---|---|---|---|"]
    for c in courses:
        d = course_dir(c)
        lec = len(list((d / "lectures").glob("*.md"))) if (d / "lectures").exists() else 0
        ex = len(list((d / "examples").glob("*.html"))) if (d / "examples").exists() else 0
        out.append(f"| {c['code']} | generated | {lec}/14 | {ex}/{max(len(c['worked_examples']), 0)} |")

    out += ["", "## Course details", ""]
    for s in sorted(by_sem):
        out += [f"### Semester {s} (Year {by_sem[s][0]['year']})", ""]
        for c in by_sem[s]:
            out += [f"#### {c['code']} — {c['title']}",
                    f"Track: {c['track']} · Credits: {c['credits']} · Prerequisites: {', '.join(c['prereqs']) or 'none'}", "",
                    c["description"], "", "**Outcomes**", ""]
            out += [f"- {o}" for o in c["outcomes"]]
            out += ["", "**Weekly topics**", ""]
            out += [f"{i}. {w}" for i, w in enumerate(c["weeks"], 1)]
            if c["worked_examples"]:
                out += ["", "**Signature worked examples**", ""]
                out += [f"- {w}" for w in c["worked_examples"]]
            if c["readings"]:
                out += ["", "**Core readings**", ""]
                out += [f"- {r}" for r in c["readings"]]
            out += ["", f"**Assessment:** {c['assessment']}", ""]
    (ROOT / "PLAN.md").write_text("\n".join(out))

    for c in courses:
        d = course_dir(c)
        for sub in ("lectures", "examples", "labs", "assessments"):
            (d / sub).mkdir(parents=True, exist_ok=True)
        syl = d / "syllabus.md"
        if syl.exists() and STUB_MARK not in syl.read_text():
            continue
        lines = [STUB_MARK, f"# {c['code']} — {c['title']}", "",
                 f"Year {c['year']}, semester {c['semester']} · {c['credits']} credits · "
                 f"Prerequisites: {', '.join(c['prereqs']) or 'none'}", "", c["description"], "",
                 "## Learning outcomes", ""]
        lines += [f"- {o}" for o in c["outcomes"]]
        lines += ["", "## Schedule", "", "| Week | Topic | Lecture | Example |", "|---|---|---|---|"]
        for i, w in enumerate(c["weeks"], 1):
            lec = sorted((d / "lectures").glob(f"w{i:02d}-*.md"))
            exs = sorted((d / "examples").glob(f"w{i:02d}-*.html"))
            lcell = f"[lecture](lectures/{lec[0].name})" if lec else "_todo_"
            ecell = " · ".join(f"[{e.stem[4:]}](examples/{e.name})" for e in exs) or "_todo_"
            lines.append(f"| {i} | {w} | {lcell} | {ecell} |")
        if c["worked_examples"]:
            lines += ["", "## Signature worked examples", ""] + [f"- {w}" for w in c["worked_examples"]]
        if c["readings"]:
            lines += ["", "## Readings", ""] + [f"- {r}" for r in c["readings"]]
        lines += ["", "## Assessment", "", c["assessment"], ""]
        syl.write_text("\n".join(lines))
    print(f"PLAN.md + {len(courses)} syllabi written")


if __name__ == "__main__":
    main()
