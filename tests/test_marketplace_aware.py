#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""test_marketplace_aware.py — tests the marketplace-aware discovery in the
/batterie:update and /batterie:version skills (bds-lodita).

No pytest in this repo (PEP723 scripts + shell smoke), so this is a self-
contained runner: assert, count, exit non-zero on any failure.

    uv run --script tests/test_marketplace_aware.py

It runs the ACTUAL inline-python block extracted from each SKILL.md against
fixture plugins dirs (via the BATTERIE_PLUGINS_DIR test seam the skills read) —
no copy of the logic, so the test can't drift from what ships. If the heredoc
format ever changes, extraction fails loudly rather than skipping silently.

Covers the failure-prone surface: source-repo (not plugin-membership) matching,
the cherry-pick case (a private-flavour plugin with no `batterie` plugin from
that marketplace), single-marketplace output staying byte-identical, the
registry-unreadable fallback, and exclusion of a look-alike imposter marketplace.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

passed = 0
failed = 0


def check(name: str, cond: bool, detail: str = ""):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"FAIL {name}" + (f"\n  {detail}" if detail else ""))


def extract_block(skill_md: Path) -> str:
    """Pull the python out of the skill's `!`python3 << 'PYEOF' ... PYEOF`` block."""
    m = re.search(r"<< 'PYEOF'\n(.*?)\nPYEOF`", skill_md.read_text(), re.DOTALL)
    if not m:
        raise SystemExit(f"could not find PYEOF block in {skill_md} — heredoc format changed?")
    return m.group(1)


def make_fixture(tmp: Path, known_marketplaces, installed_plugins) -> Path:
    d = tmp / f"plugins_{abs(hash((str(known_marketplaces), str(installed_plugins))))}"
    d.mkdir(parents=True, exist_ok=True)
    if known_marketplaces is not None:
        (d / "known_marketplaces.json").write_text(json.dumps(known_marketplaces))
    (d / "installed_plugins.json").write_text(
        json.dumps({"version": 2, "plugins": installed_plugins}))
    return d


def run_block(block: str, plugins_dir: Path) -> str:
    env = dict(os.environ, BATTERIE_PLUGINS_DIR=str(plugins_dir))
    r = subprocess.run([sys.executable, "-c", block], env=env, text=True,
                       capture_output=True, timeout=30)
    if r.returncode != 0:
        raise AssertionError(f"skill block crashed (exit {r.returncode}):\n{r.stderr}")
    return r.stdout


def entry(version, sha="0123456789abcdef"):
    return [{"scope": "user", "installPath": "/x", "version": version,
             "gitCommitSha": sha, "lastUpdated": "2026-06-28T00:00:00Z"}]


def gh(repo):
    return {"source": {"source": "github", "repo": repo}}


# ---- marketplace registries ----
MKT_PUBLIC_ONLY = {"claude-plugins-official": gh("anthropics/claude-plugins-official"),
                   "batterie": gh("spm1001/batterie")}
MKT_TWO = {"claude-plugins-official": gh("anthropics/claude-plugins-official"),
           "batterie": gh("spm1001/batterie"),
           "batterie-pm": gh("spm1001/batterie-pm")}
MKT_IMPOSTER = {"batterie": gh("spm1001/batterie"),
                "imposter": gh("someoneelse/batterie-fork")}  # name looks family, repo isn't

# ---- installed sets ----
SIX_PUBLIC = {f"{n}@batterie": entry(v) for n, v in {
    "batterie": "1.1.2", "bon": "0.28.0", "trousse": "0.5.12",
    "mise": "0.7.12", "passe": "0.6.5", "todoist-gtd": "0.4.8"}.items()}
CHERRY_PICK = {  # the brief's case: a private-flavour plugin with NO batterie@batterie-pm
    "mise@batterie": entry("0.7.12"), "trousse@batterie": entry("0.5.12"),
    "batterie@batterie": entry("1.1.2"), "mise-pm@batterie-pm": entry("0.7.12")}
WITH_IMPOSTER = {"batterie@batterie": entry("1.1.2"), "mise@batterie": entry("0.7.12"),
                 "evilthing@imposter": entry("9.9.9")}

update_block = extract_block(REPO / "skills/update/SKILL.md")
version_block = extract_block(REPO / "skills/version/SKILL.md")

with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)

    # === update skill ===
    out = run_block(update_block, make_fixture(tmp, MKT_PUBLIC_ONLY, SIX_PUBLIC))
    check("update/single: suite version shown", "📦 Batterie suite v1.1.2" in out)
    check("update/single: no 'Marketplaces to refresh' line", "Marketplaces to refresh" not in out)
    check("update/single: found 6", "Found 6 batterie plugin(s)" in out)
    check("update/single: bare name, no @suffix (byte-identical view)",
          "- bon: v0.28.0" in out and "- bon@batterie:" not in out)

    out = run_block(update_block, make_fixture(tmp, MKT_TWO, CHERRY_PICK))
    check("update/two: found 4 incl cherry-picked mise-pm", "Found 4 batterie plugin(s)" in out)
    check("update/two: both marketplaces listed", "Marketplaces to refresh: batterie, batterie-pm" in out)
    check("update/two: mise-pm shown by FULL key", "- mise-pm@batterie-pm: v0.7.12" in out)
    check("update/two: public plugins shown by FULL key", "- mise@batterie: v0.7.12" in out)
    check("update/two: suite version still found", "📦 Batterie suite v1.1.2" in out)

    out = run_block(update_block, make_fixture(tmp, None, {
        "mise@batterie": entry("0.7.12"), "mise-pm@batterie-pm": entry("0.7.12")}))
    check("update/fallback: registry unreadable → only @batterie (1)", "Found 1 batterie plugin(s)" in out)
    check("update/fallback: private flavour excluded in degraded mode", "mise-pm" not in out)

    out = run_block(update_block, make_fixture(tmp, MKT_IMPOSTER, WITH_IMPOSTER))
    check("update/imposter: found 2 (batterie + mise)", "Found 2 batterie plugin(s)" in out)
    check("update/imposter: someoneelse/batterie-fork excluded", "evilthing" not in out)

    out = run_block(update_block, make_fixture(tmp, MKT_PUBLIC_ONLY, {
        "claude-md@claude-plugins-official": entry("1.0.0")}))
    check("update/none: reports none installed", "No batterie plugins installed." in out)

    # === version skill ===
    out = run_block(version_block, make_fixture(tmp, MKT_PUBLIC_ONLY, SIX_PUBLIC))
    check("version/single: suite line", "📦  Batterie suite  v1.1.2" in out)
    check("version/single: bare name + (suite) marker", "- batterie: v1.1.2  (suite)" in out)
    check("version/single: no @suffix", "- bon@batterie:" not in out and "- bon: v0.28.0" in out)

    out = run_block(version_block, make_fixture(tmp, MKT_TWO, CHERRY_PICK))
    check("version/two: mise-pm by full key", "- mise-pm@batterie-pm: v0.7.12" in out)
    check("version/two: batterie by full key + (suite)", "- batterie@batterie: v1.1.2  (suite)" in out)
    check("version/two: suite version", "📦  Batterie suite  v1.1.2" in out)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
