#!/usr/bin/env python3
"""Headless check of interactive examples at 390px and 1280px, light and dark.

Usage:  .venv/bin/python tools/check_examples.py courses/MA101-*/examples/*.html

Reports console errors, page errors, horizontal overflow, and keyboard-reachable
controls. Saves screenshots to /tmp/example-shots/ for a visual look.
Exit code 1 if any file fails.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SHOTS = Path("/tmp/example-shots")


def check(browser, path):
    fails = []
    for width, scheme in ((390, "light"), (1280, "light"), (390, "dark"), (1280, "dark")):
        ctx = browser.new_context(viewport={"width": width, "height": 844}, color_scheme=scheme)
        page = ctx.new_page()
        errs = []
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errs.append(str(e)))
        # Block font requests: the page must work offline, and waiting on them can hang.
        page.route("**/fonts.{googleapis,gstatic}.com/**", lambda r: r.abort())
        page.goto(path.resolve().as_uri(), wait_until="domcontentloaded")
        page.wait_for_timeout(600)
        # Font requests may fail offline; ignore those.
        errs = [e for e in errs if "fonts.g" not in e and "net::ERR" not in e]
        if errs:
            fails.append(f"{width}px {scheme}: console errors {errs[:3]}")
        overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        if overflow > 1:
            fails.append(f"{width}px {scheme}: horizontal overflow {overflow}px")
        if width == 1280 and scheme == "light":
            n = page.evaluate("""document.querySelectorAll(
                'input,button,select,textarea,a[href],[tabindex]:not([tabindex="-1"])').length""")
            if n == 0:
                fails.append("no keyboard-focusable controls")
        SHOTS.mkdir(exist_ok=True)
        page.screenshot(path=str(SHOTS / f"{path.stem}-{width}-{scheme}.png"), full_page=True)
        ctx.close()
    return fails


def main():
    files = [Path(a) for a in sys.argv[1:]]
    bad = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for f in files:
            fails = check(browser, f)
            print(f"{'FAIL' if fails else 'ok  '} {f}")
            for x in fails:
                print("   -", x)
            bad += bool(fails)
        browser.close()
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
