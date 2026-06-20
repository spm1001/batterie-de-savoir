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

# ---- dry-run integration: touches nothing ----
with tempfile.TemporaryDirectory() as td:
    repo = Path(td)
    (repo / ".claude-plugin").mkdir()
    pj = repo / ".claude-plugin" / "plugin.json"
    original = '{\n  "name": "bon",\n  "version": "0.26.5"\n}'
    pj.write_text(original)
    # a git repo with one commit, so `git status` and a would-be commit are real
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin"}
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "commit", "-qm", "init"]):
        subprocess.run(cmd, cwd=repo, env=env, check=True)

    cp = subprocess.run(
        [sys.executable, str(PUBLISH), "--patch", "--dry-run",
         "--no-pull", "--no-wait", "--repo", str(repo)],
        capture_output=True, text=True,
    )
    check("dry-run exits 0", cp.returncode, 0)
    check("dry-run plans the bump", "0.26.5 -> 0.26.6" in cp.stdout, True)
    check("dry-run did NOT write version", pj.read_text(), original)
    log = subprocess.run(["git", "log", "--oneline"], cwd=repo, env=env,
                         capture_output=True, text=True)
    check("dry-run made NO commit", log.stdout.count("\n"), 1)  # only "init"

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
