#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""test_publish.py — unit + dry-run integration tests for scripts/publish.py.

No pytest in this repo (PEP723 scripts + shell smoke), so this is a self-
contained runner: assert, count, exit non-zero on any failure.

    uv run --script tests/test_publish.py

Covers the genuinely failure-prone surface: the semver bump arithmetic, the
targeted version-write (must NOT reformat sibling JSON), and the dry-run
contract (touches nothing — no version write, no commit).
"""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PUBLISH = SCRIPTS / "publish.py"

# Import publish.py as a module (the `# /// script` block is a comment to Python).
spec = importlib.util.spec_from_file_location("publish", PUBLISH)
publish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publish)

passed = 0
failed = 0


def check(name: str, got, want):
    global passed, failed
    if got == want:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {name}\n  got:  {got!r}\n  want: {want!r}")


def check_raises(name: str, fn):
    global passed, failed
    try:
        fn()
    except ValueError:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {name}: expected ValueError, none raised")


# ---- plugin_update_disposition (bds-dicalu) ----
# The skip fixture is the REAL error from the 2026-07-22 incident (publishing
# passe from tube), not a hand-made string.
check("pull ok", publish.plugin_update_disposition(0, ""), "ok")
check("pull skip on real not-found",
      publish.plugin_update_disposition(1, "Plugin passe not found"), "skip")
check("pull skip case-insensitive",
      publish.plugin_update_disposition(1, "Error: plugin Not Found"), "skip")
check("pull fail on other error",
      publish.plugin_update_disposition(1, "network unreachable"), "fail")
check("pull fail on empty output", publish.plugin_update_disposition(1, ""), "fail")

# ---- bump_version ----
check("patch", publish.bump_version("0.26.5", "patch"), "0.26.6")
check("minor", publish.bump_version("0.26.5", "minor"), "0.27.0")
check("major", publish.bump_version("0.26.5", "major"), "1.0.0")
check("patch rollover digit", publish.bump_version("1.9.9", "patch"), "1.9.10")
check("minor zeroes patch", publish.bump_version("2.4.7", "minor"), "2.5.0")
check("major zeroes both", publish.bump_version("9.9.9", "major"), "10.0.0")
check_raises("non-semver text", lambda: publish.bump_version("1.0", "patch"))
check_raises("non-numeric", lambda: publish.bump_version("1.0.x", "patch"))
check_raises("bad level", lambda: publish.bump_version("1.0.0", "nope"))

# ---- replace_version: surgical, preserves sibling formatting ----
SRC = '''{
  "name": "bon",
  "version": "0.26.5",
  "keywords": [
    "gtd",
    "tracking"
  ]
}'''
out = publish.replace_version(SRC, "0.26.6")
check("version replaced", '"version": "0.26.6"' in out, True)
check("old version gone", "0.26.5" not in out, True)
check("keywords array untouched", '"keywords": [\n    "gtd",\n    "tracking"\n  ]' in out, True)
check("only the version line changed", out, SRC.replace("0.26.5", "0.26.6"))
check_raises("no version field", lambda: publish.replace_version('{"name":"x"}', "1.0.0"))

# ---- prepend_changelog: entry goes above newest, header preserved ----
CL = """# Changelog

> A header blockquote that must survive.

## [1.8.1] - 2026-07-12

Old top entry.
"""
out = publish.prepend_changelog(CL, "1.8.2", "2026-07-13", "The new thing.")
check("new entry present", "## [1.8.2] - 2026-07-13" in out, True)
check("new message present", "The new thing." in out, True)
check("header survives", out.startswith("# Changelog\n\n> A header blockquote"), True)
check("new entry is above the old", out.index("[1.8.2]") < out.index("[1.8.1]"), True)
check("old entry preserved", "## [1.8.1] - 2026-07-12" in out and "Old top entry." in out, True)
check("header sits above new entry", out.index("blockquote") < out.index("[1.8.2]"), True)
check_raises("duplicate version refused",
             lambda: publish.prepend_changelog(CL, "1.8.1", "2026-07-13", "dup"))
# Degenerate: no `## ` heading yet — append rather than lose the entry.
out2 = publish.prepend_changelog("# Changelog\n", "1.0.0", "2026-01-01", "First.")
check("degenerate appends entry", "## [1.0.0] - 2026-01-01" in out2 and "First." in out2, True)

# ---- pick_dispatched_run / find_run_id (bds-gebaza) ----
# Fixture = the REAL 2026-08-03 incident: our dispatch at 21:52:02 registered
# run 30856400891, while a stranger's run 30856370894 (created 21:51:36, 26s
# earlier) already existed. The old 30s-grace timestamp fence watched the
# stranger to a green it never earned; the baseline fence must pick ours.
INCIDENT_OURS = {"databaseId": 30856400891,
                 "createdAt": "2026-08-03T21:52:02Z", "status": "in_progress"}
INCIDENT_STRANGER = {"databaseId": 30856370894,
                     "createdAt": "2026-08-03T21:51:36Z", "status": "completed"}
BASELINE = {"30856370894"}

check("gebaza incident: picks ours, not the baseline stranger",
      publish.pick_dispatched_run([INCIDENT_OURS, INCIDENT_STRANGER], BASELINE),
      "30856400891")
check("gebaza pre-existing completed run does NOT satisfy",
      publish.pick_dispatched_run([INCIDENT_STRANGER], BASELINE), None)
check("gebaza empty listing", publish.pick_dispatched_run([], set()), None)
check("gebaza two fresh runs -> earliest (ours registered first)",
      publish.pick_dispatched_run(
          [{"databaseId": 2, "createdAt": "2026-08-03T21:52:30Z", "status": "queued"},
           {"databaseId": 1, "createdAt": "2026-08-03T21:52:02Z", "status": "in_progress"}],
          set()),
      "1")

# find_run_id polls: a baseline-only listing must never satisfy the wait, and
# the wait resolves the moment our run registers.
listings = iter([[INCIDENT_STRANGER], [INCIDENT_STRANGER, INCIDENT_OURS]])
check("gebaza find_run_id waits past a baseline-only listing",
      publish.find_run_id(BASELINE, attempts=3, delay=0,
                          list_runs=lambda: next(listings)),
      "30856400891")
check("gebaza find_run_id gives up if only baseline runs ever appear",
      publish.find_run_id(BASELINE, attempts=3, delay=0,
                          list_runs=lambda: [INCIDENT_STRANGER]),
      None)

# ---- dry-run integration: touches nothing, bumps the SUITE version ----
ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin"}


def make_repo(path: Path, name: str, version: str) -> Path:
    """A git repo with a plugin.json and one commit, so status/commit are real."""
    (path / ".claude-plugin").mkdir(parents=True)
    pj = path / ".claude-plugin" / "plugin.json"
    pj.write_text(f'{{\n  "name": "{name}",\n  "version": "{version}"\n}}')
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "commit", "-qm", "init"]):
        subprocess.run(cmd, cwd=path, env=ENV, check=True)
    return pj


def commits(path: Path) -> int:
    log = subprocess.run(["git", "log", "--oneline"], cwd=path, env=ENV,
                         capture_output=True, text=True)
    return log.stdout.count("\n")


CL_FIXTURE = "# Changelog\n\n## [1.2.1] - 2026-06-27\n\nOld entry.\n"

# Case A: cwd IS the suite repo — one commit carries content + the suite bump.
with tempfile.TemporaryDirectory() as td:
    suite = Path(td)
    spj = make_repo(suite, "batterie", "1.2.1")
    scl = suite / "CHANGELOG.md"
    scl.write_text(CL_FIXTURE)
    # Track the changelog (as it is in reality) so the fifuko untracked-guard
    # doesn't refuse; fold it into the single init commit to keep counts at 1.
    subprocess.run(["git", "add", "-A"], cwd=suite, env=ENV, check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit", "-q"], cwd=suite, env=ENV, check=True)
    suite_orig, cl_orig = spj.read_text(), scl.read_text()
    cp = subprocess.run(
        [sys.executable, str(PUBLISH), "--patch", "--dry-run", "--no-pull",
         "--no-wait", "--repo", str(suite), "--suite-repo", str(suite)],
        capture_output=True, text=True,
    )
    check("caseA exits 0", cp.returncode, 0)
    check("caseA plans the suite bump", "suite 1.2.1 -> 1.2.2" in cp.stdout, True)
    check("caseA is single-repo", "== suite repo" in cp.stdout, True)
    check("caseA plans the changelog", "changelog: [1.2.2]" in cp.stdout, True)
    check("caseA did NOT write version", spj.read_text(), suite_orig)
    check("caseA did NOT write changelog", scl.read_text(), cl_orig)
    check("caseA made NO commit", commits(suite), 1)

# Case B: content repo != suite repo — the bump target is the SUITE version
# (1.2.1), NOT the content repo's own version (0.28.0). Neither is touched.
with tempfile.TemporaryDirectory() as td:
    base = Path(td)
    content, suite = base / "bon", base / "bds"
    cpj = make_repo(content, "bon", "0.28.0")
    spj = make_repo(suite, "batterie", "1.2.1")
    scl = suite / "CHANGELOG.md"
    scl.write_text(CL_FIXTURE)
    # Track the changelog (see Case A) — the content repo (bon) has none.
    subprocess.run(["git", "add", "-A"], cwd=suite, env=ENV, check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit", "-q"], cwd=suite, env=ENV, check=True)
    content_orig, suite_orig, cl_orig = cpj.read_text(), spj.read_text(), scl.read_text()
    cp = subprocess.run(
        [sys.executable, str(PUBLISH), "--patch", "--dry-run", "--no-pull",
         "--no-wait", "--repo", str(content), "--suite-repo", str(suite)],
        capture_output=True, text=True,
    )
    check("caseB exits 0", cp.returncode, 0)
    check("caseB bumps the SUITE, not content", "suite 1.2.1 -> 1.2.2" in cp.stdout, True)
    check("caseB ignores content version", "0.28.0 ->" not in cp.stdout, True)
    check("caseB is 2-repo push", "2-repo push" in cp.stdout, True)
    check("caseB did NOT write content version", cpj.read_text(), content_orig)
    check("caseB did NOT write suite version", spj.read_text(), suite_orig)
    check("caseB did NOT write changelog", scl.read_text(), cl_orig)
    check("caseB made NO content commit", commits(content), 1)
    check("caseB made NO suite commit", commits(suite), 1)

# ---- fifuko: untracked WIP cannot be silently swept into a release ----
# The guard is a precondition (before the assemble trigger), so a DRY-RUN
# exercises it fully — no CI is fired, nothing is committed.
def dry_publish(repo, suite, *extra):
    return subprocess.run(
        [sys.executable, str(PUBLISH), "--patch", "--dry-run", "--no-pull",
         "--no-wait", "--repo", str(repo), "--suite-repo", str(suite), *extra],
        capture_output=True, text=True,
    )


with tempfile.TemporaryDirectory() as td:
    suite = Path(td)
    make_repo(suite, "batterie", "1.2.1")
    (suite / "CHANGELOG.md").write_text(CL_FIXTURE)
    # Commit the changelog so the tree is clean apart from what each case adds.
    subprocess.run(["git", "add", "-A"], cwd=suite, env=ENV, check=True)
    subprocess.run(["git", "commit", "-qm", "cl"], cwd=suite, env=ENV, check=True)

    # (1) clean tree → default proceeds, and stages with -u (not -A).
    cp = dry_publish(suite, suite)
    check("fifuko clean tree ok", cp.returncode, 0)
    check("fifuko default stages -u", "git add -u in content repo" in cp.stdout, True)

    # (2) untracked WIP present → default REFUSES (loud), names the file, no --all.
    (suite / "scratch-wip.txt").write_text("stray")
    cp = dry_publish(suite, suite)
    check("fifuko refuses untracked", cp.returncode, 1)
    check("fifuko names the stray file", "scratch-wip.txt" in cp.stderr, True)

    # (3) same untracked file + --all → allowed, and plans -A.
    cp = dry_publish(suite, suite, "--all")
    check("fifuko --all allows untracked", cp.returncode, 0)
    check("fifuko --all stages -A", "git add -A in content repo" in cp.stdout, True)

    # (4) a tracked modification is still staged by default (no regression):
    #     the skill relies on this — staged-only would ship a bump with no content.
    (suite / "scratch-wip.txt").unlink()  # clear the untracked file from (2)/(3)
    (suite / "CHANGELOG.md").write_text(CL_FIXTURE + "\ntracked edit\n")
    cp = dry_publish(suite, suite)
    check("fifuko tracked mod ok by default", cp.returncode, 0)


print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
