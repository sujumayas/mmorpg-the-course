#!/usr/bin/env python3
"""Build a static website of the curriculum into site/.

Renders every course's syllabus, lectures, labs and assessments from
Markdown to HTML, wraps each interactive example in a viewer page, turns
starter code and data files into readable pages, and adds a home page,
an examples gallery, a labs index, a bibliography and a search index.

All links are relative, so the output works on Netlify and from disk.

    python tools/build_site.py            # writes site/
    python tools/build_site.py --out dist
"""
import argparse
import csv
import html
import io
import json
import os
import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml
from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.util import ClassNotFound

ROOT = Path(__file__).resolve().parent.parent
SITE_NAME = "Game Dev · MMORPG curriculum"
STUDIO = {"PR201", "PR301", "PR401", "PR402"}

# Top-level documents published as pages. Everything under courses/ is published too.
ROOT_DOCS = ["README.md", "PLAN.md", "STYLE_GUIDE.md", "docs/00-course-architecture-research.md"]
ROOT_FILES = ["curriculum.yaml", "templates/interactive-tokens.css"]

# Files shown in a code viewer page (raw copy kept next to it).
TEXT_EXT = {".py", ".csv", ".json", ".txt", ".h", ".hpp", ".cpp", ".c", ".sql", ".yaml", ".yml",
            ".ndjson", ".cfg", ".tex", ".hex", ".gd", ".cs", ".js", ".css", ".sh", ".toml", ".ini", ".tsv"}
SKIP_NAMES = {".DS_Store", ".gitkeep", "REVIEW.md"}
SKIP_DIRS = {"__pycache__", ".pytest_cache"}

BROKEN = []


# ----------------------------------------------------------------------------- helpers

def esc(s):
    return html.escape(str(s), quote=True)


def rel(target, frm):
    """Relative URL from output page `frm` to output path `target` (both site-relative)."""
    base = posixpath.dirname(frm) or "."
    return posixpath.relpath(target, base)


def prefix(out_rel):
    depth = out_rel.count("/")
    return "../" * depth


def repo_rel(p):
    return p.resolve().relative_to(ROOT).as_posix()


def skipped(p):
    return p.name in SKIP_NAMES or p.suffix == ".pyc" or any(part in SKIP_DIRS for part in p.parts)


def published(p):
    """True if a repo file or directory is part of the site."""
    try:
        r = repo_rel(p)
    except ValueError:
        return False
    if r.startswith("courses/"):
        return not skipped(p)
    return r in ROOT_DOCS or r in ROOT_FILES


def out_path_for(p):
    """Site-relative output path for a repo file or directory, or None if not published."""
    if not p.exists() or not published(p):
        return None
    r = repo_rel(p)
    if p.is_dir():
        return r + "/index.html"
    if p.suffix == ".md":
        if p.name == "syllabus.md":
            return posixpath.dirname(r) + "/index.html"
        return r[:-3] + ".html"
    if p.suffix == ".html" and p.parent.name == "examples" and r.startswith("courses/"):
        return r[:-5] + "/index.html"  # the viewer page; the raw file stays at r
    if p.suffix in TEXT_EXT:
        return r + ".html"
    return r


def strip_md(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return re.sub(r"[`*_]", "", s).strip()


def first_h1(text):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def split_title(h1, code=None):
    """'MMO303 · Week 02 — Armor' -> ('MMO303 · Week 02', 'Armor')."""
    if " — " in h1:
        a, b = h1.split(" — ", 1)
        return a.strip(), b.strip()
    if " · " in h1:
        a, b = h1.split(" · ", 1)
        return a.strip(), b.strip()
    return (code or ""), h1


def drop_h1(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[i + 1:])
        if line.strip():
            break
    return text


def section(text, heading):
    """Body of the '## heading' section, up to the next '## ' heading."""
    m = re.search(r"^## " + re.escape(heading) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def header_value(text, label):
    m = re.search(r"^\*\*" + re.escape(label) + r":\*\*\s*(.+)$", text, re.M)
    return strip_md(m.group(1)) if m else ""


def write(out_dir, out_rel, content):
    dest = out_dir / out_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")


# ----------------------------------------------------------------------------- markdown

def pyg_highlight(code, lang, attrs):
    if not lang:
        return ""
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        return ""
    return highlight(code, lexer, HtmlFormatter(nowrap=True))


def rewrite_href(href, env):
    if not href or href.startswith(("#", "//")) or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
        return href
    path, _, frag = href.partition("#")
    if not path:
        return href
    target = (env["src"].parent / unquote(path))
    new = out_path_for(target)
    if new is None:
        BROKEN.append((repo_rel(env["src"]), href))
        return href
    url = rel(new, env["out"])
    return url + ("#" + frag if frag else "")


def make_md():
    md = MarkdownIt("commonmark", {"html": True, "typographer": False, "highlight": pyg_highlight})
    md.enable(["table", "strikethrough"])
    md.use(anchors_plugin, min_level=2, max_level=3, permalink=True, permalinkSymbol="#",
           permalinkBefore=False)
    md.use(footnote_plugin)
    md.use(tasklists_plugin)

    def link_open(self, tokens, idx, options, env):
        tok = tokens[idx]
        href = tok.attrGet("href")
        if href:
            new = rewrite_href(href, env)
            tok.attrSet("href", new)
            if re.match(r"^https?:", new):
                tok.attrSet("rel", "noopener")
        return self.renderToken(tokens, idx, options, env)

    def image(self, tokens, idx, options, env):
        tok = tokens[idx]
        src = tok.attrGet("src")
        if src:
            tok.attrSet("src", rewrite_href(src, env))
        tok.attrSet("loading", "lazy")
        return self.image(tokens, idx, options, env)

    md.add_render_rule("link_open", link_open)
    md.add_render_rule("image", image)
    return md


MD = make_md()


def render_md(text, src, out_rel):
    env = {"src": src, "out": out_rel}
    tokens = MD.parse(text, env)
    toc = []
    for i, tok in enumerate(tokens):
        if tok.type == "heading_open" and tok.tag == "h2":
            toc.append((tok.attrGet("id"), strip_md(tokens[i + 1].content)))
    body = MD.renderer.render(tokens, MD.options, env)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return body, toc


# ----------------------------------------------------------------------------- data model

class Page:
    def __init__(self, path, out, title, eyebrow="", kind=""):
        self.path, self.out, self.title, self.eyebrow, self.kind = path, out, title, eyebrow, kind


def load_courses():
    data = yaml.safe_load((ROOT / "curriculum.yaml").read_text(encoding="utf-8"))
    dirs = {d.name.split("-")[0]: d for d in (ROOT / "courses").iterdir() if d.is_dir() and "-" in d.name}
    courses = []
    for info in data["courses"]:
        code = info["code"]
        d = dirs.get(code)
        if d is None:
            continue
        c = {"code": code, "info": info, "dir": d, "rel": repo_rel(d), "studio": code in STUDIO}
        c["index"] = c["rel"] + "/index.html"
        c["lectures"] = []
        for p in sorted((d / "lectures").glob("w*.md")):
            text = p.read_text(encoding="utf-8")
            eyebrow, title = split_title(first_h1(text), code)
            pg = Page(p, out_path_for(p), title, eyebrow, "lecture")
            pg.week = int(p.name[1:3])
            pg.text = text
            pg.why = header_value(text, "Why this matters")
            pg.sources = section(text, "Sources")
            pg.headings = [strip_md(h) for h in re.findall(r"^## (.+)$", text, re.M)]
            c["lectures"].append(pg)
        c["examples"] = []
        for p in sorted((d / "examples").glob("*.html")):
            if p.name.startswith("__"):
                continue
            raw = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"<title>(.*?)</title>", raw, re.S)
            t = html.unescape(m.group(1).strip()) if m else p.stem
            t = re.sub(r"\s+[—·|:-]\s+[A-Z]{2,3}\d{3}\b.*$", "", t) or p.stem
            pg = Page(p, out_path_for(p), t, "", "example")
            pg.raw = repo_rel(p)
            pg.week = int(p.name[1:3]) if re.match(r"w\d\d", p.name) else 0
            c["examples"].append(pg)
        c["labs"] = []
        for p in sorted((d / "labs").glob("*.md")):
            text = p.read_text(encoding="utf-8")
            _, title = split_title(first_h1(text), code)
            pg = Page(p, out_path_for(p), title or p.stem, code, "lab")
            pg.headings = [strip_md(h) for h in re.findall(r"^## (.+)$", text, re.M)]
            c["labs"].append(pg)
        c["assessments"] = []
        items = sorted((d / "assessments").glob("*.md"), key=lambda p: (p.name == "exam-bank.md", p.name))
        for p in items:
            text = p.read_text(encoding="utf-8")
            _, title = split_title(first_h1(text), code)
            c["assessments"].append(Page(p, out_path_for(p), title or p.stem, code, "assessment"))
        c["n_sources"] = sum(len(re.findall(r"^\s*[-*] ", L.sources, re.M)) for L in c["lectures"])
        courses.append(c)
    by_code = {c["code"]: c for c in courses}
    for c in courses:
        c["required_by"] = [o["code"] for o in courses if c["code"] in (o["info"].get("prereqs") or [])]
    return data, courses, by_code


# ----------------------------------------------------------------------------- layout

ICON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>'
ICON_THEME = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/>'
              '<path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8'
              'M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/></svg>')
ICON_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7z"/></svg>'

NAV = [("Courses", "index.html#map"), ("Interactives", "examples.html"), ("Labs", "labs.html"),
       ("Bibliography", "bibliography.html"), ("Program plan", "PLAN.html")]


def site_nav(out_rel, root=None):
    p = prefix(out_rel) if root is None else root
    return "".join(f'<a href="{p}{href}">{label}</a>' for label, href in NAV)


def course_sidebar(c, out_rel):
    def link(target, label, extra=""):
        cur = ' aria-current="page"' if target == out_rel else ""
        return f'<a href="{esc(rel(target, out_rel))}"{cur}>{extra}{label}</a>'

    info = c["info"]
    ex_weeks = {e.week for e in c["examples"]}
    parts = [f'<div class="side-course"><a class="side-code" href="{esc(rel(c["index"], out_rel))}">{c["code"]}</a>'
             f'<span>{esc(info["title"])}</span></div>',
             '<nav class="side-nav">', link(c["index"], "Overview")]
    label = "Sessions" if c["studio"] else "Lectures"
    parts.append(f'<h4>{label}</h4><ol class="side-weeks">')
    for L in c["lectures"]:
        dot = f'<span class="dot" title="Has an interactive">{ICON_PLAY}</span>' if L.week in ex_weeks else ""
        parts.append("<li>" + link(L.out, f'<span class="wk">{L.week:02d}</span><span class="wt">{esc(L.title)}</span>{dot}') + "</li>")
    parts.append("</ol><h4>Materials</h4>")
    parts.append(link(c["rel"] + "/examples/index.html", f'Interactives <small>{len(c["examples"])}</small>'))
    parts.append(link(c["rel"] + "/labs/index.html", f'Labs <small>{len(c["labs"])}</small>'))
    parts.append(link(c["rel"] + "/assessments/index.html", f'Assessments <small>{len(c["assessments"])}</small>'))
    parts.append(link(c["rel"] + "/bibliography.html", f'Bibliography <small>{c["n_sources"]}</small>'))
    parts.append("</nav>")
    return "".join(parts)


def crumbs_html(crumbs, out_rel):
    if not crumbs:
        return ""
    items = []
    for label, target in crumbs:
        if target:
            items.append(f'<a href="{esc(rel(target, out_rel))}">{esc(label)}</a>')
        else:
            items.append(f'<span aria-current="page">{esc(label)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(items) + "</nav>"


def toc_html(toc, extra=""):
    if not toc and not extra:
        return ""
    out = ['<aside class="toc">', extra]
    if toc:
        out.append('<p class="toc-title">On this page</p><ul>')
        out += [f'<li><a href="#{esc(i)}">{esc(t)}</a></li>' for i, t in toc if i]
        out.append("</ul>")
    out.append("</aside>")
    return "".join(out)


def layout(out_rel, title, main, *, sidebar="", toc="", crumbs=None, body_class="", root=None,
           description=""):
    p = prefix(out_rel) if root is None else root
    has_side = bool(sidebar)
    cls = " ".join(x for x in [body_class, "has-side" if has_side else "no-side", "has-toc" if toc else ""] if x)
    desc = f'<meta name="description" content="{esc(description)}">' if description else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(SITE_NAME)}</title>
{desc}
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&family=Figtree:wght@400;600;700&display=swap">
<link rel="stylesheet" href="{p}assets/site.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body class="{cls}">
<a class="skip" href="#content">Skip to content</a>
<header class="topbar">
  <button class="icon-btn menu-btn" type="button" aria-label="Open navigation" aria-expanded="false" data-menu>{ICON_MENU}</button>
  <a class="brand" href="{p}index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-text">{esc(SITE_NAME)}</span></a>
  <nav class="topnav" aria-label="Site">{site_nav(out_rel, p)}</nav>
  <div class="search" role="search">
    <input id="q" type="search" placeholder="Search courses, lectures, labs" aria-label="Search" autocomplete="off" spellcheck="false">
    <kbd class="search-key" aria-hidden="true">/</kbd>
    <div id="q-results" class="search-results" role="listbox" hidden></div>
  </div>
  <button class="icon-btn" type="button" aria-label="Switch light or dark theme" data-theme-toggle>{ICON_THEME}</button>
</header>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <nav class="side-site" aria-label="Site">{site_nav(out_rel, p)}</nav>
    {sidebar}
  </aside>
  <div class="scrim" data-scrim hidden></div>
  <main id="content">
    {crumbs_html(crumbs, out_rel)}
    {main}
  </main>
  {toc}
</div>
<footer class="footer"><p>{esc(SITE_NAME)}. BSc Game Development with an MMORPG specialization. Built from <code>curriculum.yaml</code> and the course folders.</p></footer>
<script src="{p}assets/site.js" data-root="{p}"></script>
</body>
</html>
"""


def course_crumbs(c, extra=()):
    info = c["info"]
    return [("Home", "index.html"), (f'Year {info["year"]}', f'index.html#year-{info["year"]}'),
            (c["code"], c["index"]), *extra]


def page_head(eyebrow, title, sub=""):
    e = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    s = f'<p class="lede">{sub}</p>' if sub else ""
    return f'<header class="page-head">{e}<h1>{esc(title)}</h1>{s}</header>'


# ----------------------------------------------------------------------------- page builders

def build_lecture(out, c, i):
    L = c["lectures"][i]
    text = drop_h1(L.text)
    spec = ""
    m = re.search(r"^## Interactive spec", text, re.M)
    if m:
        text, spec = text[:m.start()], text[m.start():]
    body, toc = render_md(text, L.path, L.out)
    spec_html = ""
    if spec:
        spec_title = strip_md(spec.splitlines()[0][3:])
        spec_body, _ = render_md("\n".join(spec.splitlines()[1:]), L.path, L.out)
        spec_html = (f'<details class="spec"><summary>{esc(spec_title)} <small>notes for the example builder</small></summary>'
                     f'{spec_body}</details>')
    exs = [e for e in c["examples"] if e.week == L.week]
    cards = "".join(
        f'<a class="ex-card" href="{esc(rel(e.out, L.out))}"><span class="ex-icon">{ICON_PLAY}</span>'
        f'<span><small>Interactive</small><strong>{esc(e.title)}</strong></span></a>' for e in exs)
    pager = []
    if i > 0:
        P = c["lectures"][i - 1]
        pager.append(f'<a class="prev" href="{esc(rel(P.out, L.out))}"><small>Week {P.week:02d}</small>{esc(P.title)}</a>')
    else:
        pager.append("<span></span>")
    if i + 1 < len(c["lectures"]):
        N = c["lectures"][i + 1]
        pager.append(f'<a class="next" href="{esc(rel(N.out, L.out))}"><small>Week {N.week:02d}</small>{esc(N.title)}</a>')
    kind = "Session" if c["studio"] else "Week"
    main = (page_head(f'{c["code"]} · {kind} {L.week:02d}', L.title)
            + (f'<div class="ex-cards mobile-only">{cards}</div>' if cards else "")
            + f'<article class="prose">{body}{spec_html}</article>'
            + f'<nav class="pager" aria-label="Weeks">{"".join(pager)}</nav>')
    right = toc_html(toc, f'<div class="ex-cards">{cards}</div>' if cards else "")
    write(out, L.out, layout(L.out, f'{c["code"]} week {L.week}: {L.title}', main,
                             sidebar=course_sidebar(c, L.out), toc=right,
                             crumbs=course_crumbs(c, [(f"{kind} {L.week:02d}", None)]),
                             body_class="page-lecture", description=L.why))


def build_doc(out, c, pg, crumb_label):
    """Lab or assessment page."""
    text = drop_h1(pg.path.read_text(encoding="utf-8"))
    body, toc = render_md(text, pg.path, pg.out)
    main = page_head(pg.eyebrow, pg.title) + f'<article class="prose">{body}</article>'
    write(out, pg.out, layout(pg.out, f'{c["code"]} {pg.title}', main, sidebar=course_sidebar(c, pg.out),
                              toc=toc_html(toc), crumbs=course_crumbs(c, [(crumb_label, None)]),
                              body_class="page-doc"))


def build_course_index(out, c, by_code):
    info = c["info"]
    o = c["index"]
    syl = (c["dir"] / "syllabus.md").read_text(encoding="utf-8")
    m = re.search(r"^## ", syl, re.M)
    body, toc = render_md(syl[m.start():] if m else drop_h1(syl), c["dir"] / "syllabus.md", o)

    def clinks(codes):
        return ", ".join(f'<a href="{esc(rel(by_code[x]["index"], o))}">{x}</a>' if x in by_code else x
                         for x in codes) or "none"

    track = "MMO specialization" if info["track"] == "mmo" else "Core"
    chips = [f'Year {info["year"]}, semester {info["semester"]}', f'{info["credits"]} credits', track]
    if c["studio"]:
        chips.append("Studio course")
    meta = "".join(f'<span class="chip">{esc(x)}</span>' for x in chips)
    rels = (f'<dl class="course-rel"><div><dt>Prerequisites</dt><dd>{clinks(info.get("prereqs") or [])}</dd></div>'
            f'<div><dt>Leads to</dt><dd>{clinks(c["required_by"])}</dd></div></dl>')
    first = c["lectures"][0].out if c["lectures"] else o
    tiles = [
        ("Sessions" if c["studio"] else "Lectures", len(c["lectures"]), first),
        ("Interactives", len(c["examples"]), c["rel"] + "/examples/index.html"),
        ("Labs", len(c["labs"]), c["rel"] + "/labs/index.html"),
        ("Assessments", len(c["assessments"]), c["rel"] + "/assessments/index.html"),
        ("Sources", c["n_sources"], c["rel"] + "/bibliography.html"),
    ]
    tiles_html = '<div class="tiles">' + "".join(
        f'<a class="tile" href="{esc(rel(t, o))}"><strong>{n}</strong><span>{esc(lbl)}</span></a>' for lbl, n, t in tiles) + "</div>"
    main = (f'<header class="page-head course-head"><p class="eyebrow">{c["code"]}</p><h1>{esc(info["title"])}</h1>'
            f'<div class="chips">{meta}</div><p class="lede">{esc(info["description"])}</p>{rels}</header>'
            + tiles_html + f'<article class="prose">{body}</article>')
    write(out, o, layout(o, f'{c["code"]} {info["title"]}', main, sidebar=course_sidebar(c, o),
                         toc=toc_html(toc), crumbs=course_crumbs(c)[:-1] + [(c["code"], None)],
                         body_class="page-course", description=info["description"]))


def build_course_lists(out, c):
    # Interactives gallery
    o = c["rel"] + "/examples/index.html"
    lec_by_week = {L.week: L for L in c["lectures"]}
    cards = []
    for e in c["examples"]:
        L = lec_by_week.get(e.week)
        sub = f'<small>Week {e.week:02d}{" · " + esc(L.title) if L else ""}</small>'
        cards.append(f'<a class="card ex" href="{esc(rel(e.out, o))}"><span class="ex-icon">{ICON_PLAY}</span>'
                     f'<span>{sub}<strong>{esc(e.title)}</strong></span></a>')
    main = page_head(c["code"], "Interactives", f'{len(c["examples"])} interactive worked examples. Each runs in the browser.') \
        + f'<div class="card-grid">{"".join(cards) or "<p>No interactives in this course.</p>"}</div>'
    write(out, o, layout(o, f'{c["code"]} interactives', main, sidebar=course_sidebar(c, o),
                         crumbs=course_crumbs(c, [("Interactives", None)])))

    # Labs and assessments lists
    for key, label, blurb in (("lectures", "Sessions" if c["studio"] else "Lectures", "One per week, in order."),
                              ("labs", "Labs", "Hands-on exercises, with starter files and checkers where the lab has them."),
                              ("assessments", "Assessments", "Assignment briefs with rubrics, and the exam question bank.")):
        o = f'{c["rel"]}/{key}/index.html'
        rows = "".join(f'<li><a href="{esc(rel(pg.out, o))}">{"Week %02d: " % pg.week if key == "lectures" else ""}{esc(pg.title)}</a></li>' for pg in c[key])
        main = page_head(c["code"], label, blurb) + f'<ul class="link-list">{rows}</ul>'
        write(out, o, layout(o, f'{c["code"]} {label.lower()}', main, sidebar=course_sidebar(c, o),
                             crumbs=course_crumbs(c, [(label, None)])))

    # Bibliography
    o = c["rel"] + "/bibliography.html"
    parts = []
    readings = c["info"].get("readings") or []
    if readings:
        parts.append('<h2 id="course-readings">Course readings</h2><ul>'
                     + "".join(f"<li>{esc(r)}</li>" for r in readings) + "</ul>")
    toc = [("course-readings", "Course readings")] if readings else []
    for L in c["lectures"]:
        if not L.sources:
            continue
        sid = f"week-{L.week:02d}"
        src_html, _ = render_md(L.sources, L.path, o)
        parts.append(f'<h2 id="{sid}">Week {L.week:02d}: <a href="{esc(rel(L.out, o))}">{esc(L.title)}</a></h2>{src_html}')
    main = page_head(c["code"], "Bibliography", "Course readings, then every source cited in each week.") \
        + f'<article class="prose biblio">{"".join(parts)}</article>'
    write(out, o, layout(o, f'{c["code"]} bibliography', main, sidebar=course_sidebar(c, o),
                         crumbs=course_crumbs(c, [("Bibliography", None)])))


def build_example_viewer(out, c, e):
    L = next((L for L in c["lectures"] if L.week == e.week), None)
    raw = rel(e.raw, e.out)
    lec = f'<a class="btn" href="{esc(rel(L.out, e.out))}">Read the week {e.week:02d} lecture</a>' if L else ""
    main = (page_head(f'{c["code"]} · Week {e.week:02d} · Interactive', e.title)
            + f'<div class="ex-actions">{lec}<a class="btn" href="{esc(raw)}" target="_blank" rel="noopener">Open full screen</a></div>'
            + f'<div class="ex-frame"><iframe src="{esc(raw)}" title="{esc(e.title)}" data-sync-theme loading="lazy"></iframe></div>')
    write(out, e.out, layout(e.out, f'{c["code"]} interactive: {e.title}', main, sidebar=course_sidebar(c, e.out),
                             crumbs=course_crumbs(c, [(f"Week {e.week:02d}", L.out if L else None), ("Interactive", None)]),
                             body_class="page-example"))


def course_of(path, courses):
    for c in courses:
        if c["dir"] in path.parents or c["dir"] == path:
            return c
    return None


def build_file_viewer(out, p, courses):
    r = repo_rel(p)
    o = r + ".html"
    raw = p.name
    c = course_of(p, courses)
    text = p.read_text(encoding="utf-8", errors="replace")
    lines = text.count("\n") + 1
    body = ""
    if p.suffix == ".csv" and lines <= 400:
        try:
            rows = list(csv.reader(io.StringIO(text)))
            if rows:
                head = "".join(f"<th>{esc(x)}</th>" for x in rows[0])
                trs = "".join("<tr>" + "".join(f"<td>{esc(x)}</td>" for x in row) + "</tr>" for row in rows[1:])
                body = f'<div class="table-wrap"><table class="data"><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div>'
        except csv.Error:
            body = ""
    if not body:
        try:
            lexer = get_lexer_for_filename(p.name if p.suffix != ".ndjson" else "x.json", text)
            code = highlight(text, lexer, HtmlFormatter(nowrap=True))
        except ClassNotFound:
            code = esc(text)
        body = f'<pre class="code-file"><code>{code}</code></pre>'
    main = (page_head(posixpath.dirname(r).split("/", 2)[-1] if c else posixpath.dirname(r), p.name,
                      f"{lines} lines · {p.stat().st_size:,} bytes")
            + f'<div class="ex-actions"><a class="btn" href="{esc(raw)}" download>Download {esc(p.name)}</a>'
              f'<a class="btn" href="{esc(raw)}">View raw</a></div>' + body)
    crumbs = course_crumbs(c, [(p.name, None)]) if c else [("Home", "index.html"), (p.name, None)]
    write(out, o, layout(o, p.name, main, sidebar=course_sidebar(c, o) if c else "", crumbs=crumbs,
                         body_class="page-file"))


def build_dir_listing(out, d, courses):
    r = repo_rel(d)
    o = r + "/index.html"
    c = course_of(d, courses)
    entries = sorted((x for x in d.iterdir() if not skipped(x)), key=lambda x: (not x.is_dir(), x.name))
    rows = []
    for x in entries:
        target = out_path_for(x)
        if not target:
            continue
        label = x.name + ("/" if x.is_dir() else "")
        rows.append(f'<li><a href="{esc(rel(target, o))}">{esc(label)}</a></li>')
    readme = ""
    rd = d / "README.md"
    if rd.exists():
        readme, _ = render_md(drop_h1(rd.read_text(encoding="utf-8")), rd, o)
        readme = f'<article class="prose">{readme}</article>'
    main = page_head(c["code"] if c else "", d.name + "/", f"{len(rows)} files") + f'<ul class="link-list files">{"".join(rows)}</ul>' + readme
    crumbs = course_crumbs(c, [(d.name, None)]) if c else [("Home", "index.html"), (d.name, None)]
    write(out, o, layout(o, d.name, main, sidebar=course_sidebar(c, o) if c else "", crumbs=crumbs))


def build_root_doc(out, rel_path):
    p = ROOT / rel_path
    o = out_path_for(p)
    text = p.read_text(encoding="utf-8")
    title = first_h1(text).replace(" — ", ": ") or p.stem
    body, toc = render_md(drop_h1(text), p, o)
    main = page_head("Program", title) + f'<article class="prose">{body}</article>'
    write(out, o, layout(o, title, main, toc=toc_html(toc), crumbs=[("Home", "index.html"), (title, None)],
                         body_class="page-doc"))


# ----------------------------------------------------------------------------- global pages

def build_home(out, data, courses):
    o = "index.html"
    n_lec = sum(len(c["lectures"]) for c in courses)
    n_ex = sum(len(c["examples"]) for c in courses)
    n_lab = sum(len(c["labs"]) for c in courses)
    n_src = sum(c["n_sources"] for c in courses)
    credits = sum(c["info"]["credits"] for c in courses)
    stats = [(len(courses), "courses"), (n_lec, "lectures and sessions"), (n_ex, "interactives"),
             (n_lab, "labs"), (n_src, "cited sources"), (credits, "credits")]
    stats_html = '<div class="stats">' + "".join(f"<div><strong>{n:,}</strong><span>{l}</span></div>" for n, l in stats) + "</div>"

    exemplar = next((L for c in courses if c["code"] == "MMO303" for L in c["lectures"] if L.week == 2), None)
    start = [("Program plan", "PLAN.html", "Every course's outcomes, weekly topics, readings and assessment on one page.")]
    if exemplar:
        start.append(("Exemplar lecture", exemplar.out, "MMO303 week 2, armor and damage mitigation. The lecture that set the standard for the rest."))
    start += [("All interactives", "examples.html", f"{n_ex} browser models you can move, from armor curves to login queues."),
              ("Research behind the program", "docs/00-course-architecture-research.html", "The frameworks, benchmark programs and MMO literature the structure comes from.")]
    start_html = '<div class="card-grid start">' + "".join(
        f'<a class="card" href="{esc(h)}"><strong>{esc(t)}</strong><span>{esc(d)}</span></a>' for t, h, d in start) + "</div>"

    years = []
    for y in range(1, data["program"]["years"] + 1):
        sems = []
        for s in sorted({c["info"]["semester"] for c in courses if c["info"]["year"] == y}):
            cards = []
            for c in courses:
                info = c["info"]
                if info["year"] != y or info["semester"] != s:
                    continue
                kind = "studio" if c["studio"] else info["track"]
                cards.append(
                    f'<a class="course-card {kind}" href="{esc(c["index"])}">'
                    f'<span class="cc-code">{c["code"]}</span><strong>{esc(info["title"])}</strong>'
                    f'<span class="cc-meta">{len(c["lectures"])} weeks · {len(c["examples"])} interactives · {len(c["labs"])} labs</span></a>')
            sems.append(f'<section class="sem"><h3>Semester {s}</h3><div class="sem-cards">{"".join(cards)}</div></section>')
        label = "Core" if y <= 2 else "MMORPG specialization"
        years.append(f'<section class="year" id="year-{y}"><h2>Year {y} <small>{label}</small></h2><div class="sems">{"".join(sems)}</div></section>')

    legend = ('<p class="legend"><span class="lg core"></span>Core <span class="lg mmo"></span>MMO specialization '
              '<span class="lg studio"></span>Studio project</p>')
    main = (f'<section class="hero"><p class="eyebrow">Four-year BSc · 8 semesters · 15 weeks each</p>'
            f'<h1>Game development, with an MMORPG specialization</h1>'
            f'<p class="lede">Years 1 and 2 build the foundation in design, programming, math, art, audio and production. '
            f'Years 3 and 4 specialize in MMORPGs: virtual worlds, server architecture, balance, economies, '
            f'social systems, live operations and the ethics of running a persistent world. Each concept is taught '
            f'through a worked example from a shipped game, with real numbers and an interactive model.</p></section>'
            + stats_html + '<h2 class="section-title">Start here</h2>' + start_html
            + f'<section id="map"><h2 class="section-title">Curriculum map</h2>{legend}{"".join(years)}</section>')
    write(out, o, layout(o, "Home", main, body_class="page-home",
                         description="A four-year BSc curriculum in game development with an MMORPG specialization."))


def filter_box(placeholder):
    return (f'<div class="filter"><input type="search" data-filter placeholder="{esc(placeholder)}" '
            f'aria-label="{esc(placeholder)}"><span data-filter-count></span></div>')


def build_examples_page(out, courses):
    o = "examples.html"
    groups = []
    for c in courses:
        if not c["examples"]:
            continue
        lec = {L.week: L for L in c["lectures"]}
        cards = "".join(
            f'<a class="card ex" data-filter-item href="{esc(e.out)}"><span class="ex-icon">{ICON_PLAY}</span>'
            f'<span><small>{c["code"]} · Week {e.week:02d}{" · " + esc(lec[e.week].title) if e.week in lec else ""}</small>'
            f'<strong>{esc(e.title)}</strong></span></a>' for e in c["examples"])
        groups.append(f'<section class="group" data-filter-group><h2><a href="{esc(c["index"])}">{c["code"]}</a> {esc(c["info"]["title"])}</h2>'
                      f'<div class="card-grid">{cards}</div></section>')
    n = sum(len(c["examples"]) for c in courses)
    main = page_head("Program", "Interactives", f"{n} interactive worked examples across {len(groups)} courses.") \
        + filter_box("Filter interactives") + "".join(groups)
    write(out, o, layout(o, "Interactives", main, crumbs=[("Home", "index.html"), ("Interactives", None)]))


def build_labs_page(out, courses):
    o = "labs.html"
    groups = []
    for c in courses:
        rows = "".join(f'<li data-filter-item><a href="{esc(pg.out)}">{esc(pg.title)}</a></li>' for pg in c["labs"])
        ass = "".join(f'<li data-filter-item><a href="{esc(pg.out)}">{esc(pg.title)}</a></li>' for pg in c["assessments"])
        groups.append(f'<section class="group" data-filter-group><h2><a href="{esc(c["index"])}">{c["code"]}</a> {esc(c["info"]["title"])}</h2>'
                      f'<div class="two-col"><div><h3>Labs</h3><ul class="link-list">{rows}</ul></div>'
                      f'<div><h3>Assessments</h3><ul class="link-list">{ass}</ul></div></div></section>')
    n = sum(len(c["labs"]) for c in courses)
    main = page_head("Program", "Labs and assessments", f"{n} labs, plus every assignment brief and exam bank.") \
        + filter_box("Filter labs and briefs") + "".join(groups)
    write(out, o, layout(o, "Labs and assessments", main, crumbs=[("Home", "index.html"), ("Labs", None)]))


def build_biblio_page(out, courses):
    o = "bibliography.html"
    groups = []
    for c in courses:
        items = []
        for r in c["info"].get("readings") or []:
            items.append(f'<li data-filter-item><span class="tag">Reading</span> {esc(r)}</li>')
        for L in c["lectures"]:
            if not L.sources:
                continue
            html_src, _ = render_md(L.sources, L.path, o)
            lis = re.findall(r"<li>(.*?)</li>", html_src, re.S)
            for li in lis:
                items.append(f'<li data-filter-item><a class="tag" href="{esc(L.out)}">W{L.week:02d}</a> {li.strip()}</li>')
        groups.append(f'<details class="group biblio-group" data-filter-group><summary><strong>{c["code"]}</strong> '
                      f'{esc(c["info"]["title"])} <small>{len(items)}</small></summary>'
                      f'<p class="more"><a href="{esc(c["rel"] + "/bibliography.html")}">Course bibliography by week</a></p>'
                      f'<ul class="biblio-list">{"".join(items)}</ul></details>')
    n = sum(c["n_sources"] for c in courses)
    main = page_head("Program", "Bibliography",
                     f"{n:,} sources cited in lectures, plus each course's readings. Open a course, or filter across all of them.") \
        + filter_box("Filter sources, for example Castronova or EVE") + "".join(groups)
    write(out, o, layout(o, "Bibliography", main, crumbs=[("Home", "index.html"), ("Bibliography", None)],
                         body_class="page-biblio"))


def build_404(out):
    main = page_head("404", "Page not found", 'That page does not exist. Try the search box, or go back to the <a href="/index.html">home page</a>.')
    write(out, "404.html", layout("404.html", "Not found", main, root="/"))


def build_search_index(out, courses):
    idx = []

    def add(t, code, kind, url, ctx, extra=""):
        s = " ".join([t, code, ctx, extra]).lower()
        idx.append({"t": t, "c": code, "k": kind, "u": url, "x": ctx, "s": s})

    for c in courses:
        info = c["info"]
        add(info["title"], c["code"], "course", c["index"], f'Year {info["year"]}, semester {info["semester"]}',
            info["description"])
        for L in c["lectures"]:
            add(L.title, c["code"], "lecture", L.out, f'{c["code"]} · Week {L.week:02d}',
                L.why + " " + " ".join(L.headings))
        for e in c["examples"]:
            add(e.title, c["code"], "interactive", e.out, f'{c["code"]} · Week {e.week:02d}')
        for pg in c["labs"]:
            add(pg.title, c["code"], "lab", pg.out, c["code"], " ".join(pg.headings))
        for pg in c["assessments"]:
            add(pg.title, c["code"], "assessment", pg.out, c["code"])
    for t, u in (("Program plan", "PLAN.html"), ("Style guide", "STYLE_GUIDE.html"),
                 ("Research behind the program", "docs/00-course-architecture-research.html"),
                 ("All interactives", "examples.html"), ("Bibliography", "bibliography.html"),
                 ("Labs and assessments", "labs.html")):
        add(t, "", "page", u, "Program")
    write(out, "assets/search-index.js", "window.SEARCH_INDEX=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";")


def build_assets(out):
    src = ROOT / "tools" / "site"
    dest = out / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        shutil.copy2(f, dest / f.name)
    light = HtmlFormatter(style="default").get_style_defs(".prose pre code, pre.code-file code")
    dark = HtmlFormatter(style="github-dark").get_style_defs(".prose pre code, pre.code-file code")
    dark_scoped = re.sub(r"^(\S[^{]*)\{", lambda m: ", ".join(":root[data-theme=\"dark\"] " + s.strip()
                                                              for s in m.group(1).split(",")) + " {", dark, flags=re.M)
    dark_media = re.sub(r"^(\S[^{]*)\{", lambda m: ", ".join(":root:not([data-theme=\"light\"]) " + s.strip()
                                                             for s in m.group(1).split(",")) + " {", dark, flags=re.M)
    css = (light + "\n" + dark_scoped + "\n@media (prefers-color-scheme: dark) {\n" + dark_media + "\n}\n")
    # Keep token colors only; the page styles own backgrounds.
    css = re.sub(r"background(-color)?:\s*#[0-9a-fA-F]+;?", "", css)
    (dest / "pygments.css").write_text(css, encoding="utf-8")


# ----------------------------------------------------------------------------- main

def copy_raw(out, p):
    dest = out / repo_rel(p)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dest)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="site", help="output directory (default: site)")
    args = ap.parse_args()
    out = (ROOT / args.out).resolve()
    if out == ROOT or ROOT not in out.parents:
        sys.exit("--out must be a subdirectory of the repository")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    data, courses, by_code = load_courses()
    build_assets(out)

    handled = set()
    for c in courses:
        build_course_index(out, c, by_code)
        handled.add(c["dir"] / "syllabus.md")
        for i in range(len(c["lectures"])):
            build_lecture(out, c, i)
            handled.add(c["lectures"][i].path)
        for pg in c["labs"]:
            build_doc(out, c, pg, pg.title.split(":")[0])
            handled.add(pg.path)
        for pg in c["assessments"]:
            build_doc(out, c, pg, pg.title)
            handled.add(pg.path)
        for e in c["examples"]:
            build_example_viewer(out, c, e)
        build_course_lists(out, c)

    # Every other published file under courses/: raw copy, plus a viewer or rendered page.
    dirs_needed = set()
    for p in sorted((ROOT / "courses").rglob("*")):
        if skipped(p):
            continue
        if p.is_dir():
            if p.parent.name != "courses" and p.name not in ("lectures", "examples", "labs", "assessments"):
                dirs_needed.add(p)
            continue
        if p in handled:
            continue
        if p.suffix == ".md":
            c = course_of(p, courses)
            text = p.read_text(encoding="utf-8")
            o = out_path_for(p)
            body, toc = render_md(drop_h1(text), p, o)
            main = page_head(c["code"] if c else "", first_h1(text) or p.name) + f'<article class="prose">{body}</article>'
            write(out, o, layout(o, p.stem, main, sidebar=course_sidebar(c, o) if c else "", toc=toc_html(toc),
                                 crumbs=course_crumbs(c, [(p.stem, None)]) if c else None))
            continue
        copy_raw(out, p)
        if p.suffix in TEXT_EXT:
            build_file_viewer(out, p, courses)
    for d in sorted(dirs_needed):
        build_dir_listing(out, d, courses)

    for r in ROOT_DOCS:
        build_root_doc(out, r)
    for r in ROOT_FILES:
        p = ROOT / r
        copy_raw(out, p)
        if p.suffix in TEXT_EXT:
            build_file_viewer(out, p, courses)

    build_home(out, data, courses)
    build_examples_page(out, courses)
    build_labs_page(out, courses)
    build_biblio_page(out, courses)
    build_404(out)
    build_search_index(out, courses)

    n_pages = sum(1 for _ in out.rglob("*.html"))
    print(f"site: {len(courses)} courses, {n_pages} HTML files written to {out.relative_to(ROOT)}/")
    if BROKEN:
        uniq = sorted(set(BROKEN))
        print(f"warning: {len(uniq)} links point to files that are not published:")
        for src, href in uniq[:40]:
            print(f"  {src}: {href}")


if __name__ == "__main__":
    main()
