"""PR101 lab 13: an automated release checker.

Run:  python release_check.py sample_build
Exit code 0 means every check passed, 1 means at least one failed.

A build folder holds:
  version.txt       one line, the version being released (Semantic Versioning 2.0.0)
  last_release.txt  one line, the last version you released
  CHANGELOG.md      one "## <version>" heading per release
  settings.cfg      key=value lines; keys in DEBUG_KEYS must not be true
  manifest.txt      one relative file path per line; every file must exist

The five check functions below are stubs. Each one returns a value that
makes the checker PASS everything, which is exactly what a checklist that
checks nothing does. Replace each stub with a real check (lecture sections 3 and 4).
"""
import sys
from pathlib import Path

DEBUG_KEYS = {"show_fps", "god_mode", "level_skip", "verbose_log"}


def parse_version(text):
    """Parse a SemVer 2.0.0 string into (major, minor, patch, prerelease).

    - Strip surrounding whitespace first.
    - Drop build metadata (everything from the first "+").
    - The core must be exactly three dot-separated non-negative integers,
      with no leading zeros ("01" is invalid, "0" is fine).
    - An optional pre-release follows a "-": return it as a tuple of
      identifiers split on ".", with numeric identifiers converted to int
      ("rc.2" -> ("rc", 2)). No pre-release -> empty tuple ().
    - Raise ValueError for anything else ("1.0", "v1.0.0", "1.0.0-", "a.b.c").

    Examples:
        parse_version("1.2.3")            -> (1, 2, 3, ())
        parse_version("1.0.0-rc.10+abc")  -> (1, 0, 0, ("rc", 10))
    """
    return (0, 0, 0, ())  # TODO: replace this stub


def is_newer(new, old):
    """True if version string `new` has higher SemVer precedence than `old`.

    Compare major, minor, patch as numbers. If they are equal:
    a version WITHOUT a pre-release is newer than one WITH a pre-release,
    and two pre-releases compare identifier by identifier (numbers as numbers,
    numbers lower than text, a shorter list lower if all earlier ones are equal).
    Equal versions are not newer. Use parse_version.

    Examples: is_newer("1.0.0", "1.0.0-rc.2") -> True
              is_newer("1.0.0-rc.10", "1.0.0-rc.2") -> True
              is_newer("0.9.2", "0.9.2") -> False
    """
    return True  # TODO: replace this stub


def debug_flags_on(config_text):
    """Return a sorted list of DEBUG_KEYS that are switched on in config_text.

    Lines look like "key=value" or "key = value". Ignore blank lines,
    [section] headers and comment lines starting with ";" or "#".
    A value counts as on if, lowercased and stripped, it is "true", "1" or "yes".
    """
    return []  # TODO: replace this stub


def missing_files(build_dir, manifest_text):
    """Return a sorted list of manifest paths that do not exist under build_dir.

    One relative path per line. Ignore blank lines and lines starting with "#".
    """
    return []  # TODO: replace this stub


def changelog_has(changelog_text, version):
    """True if some line of the changelog is exactly "## <version>" (after stripping)."""
    return True  # TODO: replace this stub


def release_risk(risks, catches):
    """Chance a release is clean: product over items of 1 - p * (1 - c).

    risks[i] is item i's chance of being wrong, catches[i] the catch rate of its
    check (0 if the item has no check). Lecture section 2.
    """
    return 1.0  # TODO: replace this stub


# ---------------------------------------------------------------------------
# The runner below is complete. It calls your functions; you do not need to edit it.

def read(build_dir, name):
    path = Path(build_dir) / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run_checks(build_dir):
    """Return a list of (check name, passed, detail)."""
    results = []
    version = read(build_dir, "version.txt").strip()
    last = read(build_dir, "last_release.txt").strip()

    try:
        parse_version(version)
        valid = True
        results.append(("version is SemVer", True, version))
    except ValueError as err:
        valid = False
        results.append(("version is SemVer", False, f"{version!r}: {err}"))

    if valid:
        newer = is_newer(version, last)
        results.append(("version is newer", newer, f"{version} vs last {last}"))
    else:
        results.append(("version is newer", False, "cannot compare an invalid version"))

    has_entry = changelog_has(read(build_dir, "CHANGELOG.md"), version)
    results.append(("changelog entry", has_entry, f"## {version}"))

    flags = debug_flags_on(read(build_dir, "settings.cfg"))
    results.append(("no debug flags", not flags, ", ".join(flags) or "none on"))

    missing = missing_files(build_dir, read(build_dir, "manifest.txt"))
    results.append(("all manifest files present", not missing, ", ".join(missing) or "all found"))
    return results


def main(argv):
    build_dir = argv[1] if len(argv) > 1 else "sample_build"
    results = run_checks(build_dir)
    for name, ok, detail in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name:28} {detail}")
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
