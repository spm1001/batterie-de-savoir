#!/usr/bin/env bash
# plugin-smoke.sh — Lightweight plugin install + discovery test
#
# Creates an isolated ~/.claude with only credentials and marketplace config,
# installs specified plugins, and verifies skills/hooks/commands are discovered.
#
# Uses the same env-scrub pattern as neutral-claude.sh but seeds plugin config
# instead of stripping it.
#
# Usage:
#   ./plugin-smoke.sh                  # Test all batterie plugins
#   ./plugin-smoke.sh bon trousse      # Test specific plugins
#   ./plugin-smoke.sh --keep           # Don't clean up (inspect the temp dir)
#   ./plugin-smoke.sh --verbose        # Show full claude output
#
# Requirements:
#   - claude binary in PATH
#   - ~/.claude/.credentials.json (OAuth token)
#   - git (for plugin clone)

set -euo pipefail

# ── Config ─────────────────────────────────────────────────────────────

ALL_PLUGINS=(bon trousse mise todoist-gtd garde-manger passe consomme gueridon)

# Expected skills per plugin (subset — smoke test, not exhaustive)
declare -A EXPECTED_SKILLS=(
    [bon]="bon open close audit"
    [trousse]="titans diagram screenshot skill-forge toise"
    [mise]="mise"
    [todoist-gtd]="todoist-gtd"
    [garde-manger]="garde"
    [passe]="passe"
    [consomme]="consomme"
    [gueridon]="setup"
)

# Expected commands per plugin
declare -A EXPECTED_COMMANDS=(
    [consomme]="consomme consomme-explore consomme-profile"
)

# ── Parse args ─────────────────────────────────────────────────────────

KEEP=false
VERBOSE=false
PLUGINS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --keep) KEEP=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --help|-h)
            echo "Usage: $0 [--keep] [--verbose] [plugin ...]"
            exit 0
            ;;
        *) PLUGINS+=("$1"); shift ;;
    esac
done

[[ ${#PLUGINS[@]} -eq 0 ]] && PLUGINS=("${ALL_PLUGINS[@]}")

# ── Find claude ────────────────────────────────────────────────────────

CLAUDE_BIN=$(command -v claude 2>/dev/null) || {
    echo "FAIL: claude not found in PATH" >&2
    exit 1
}
CLAUDE_DIR=$(dirname "$CLAUDE_BIN")

# ── Find credentials ──────────────────────────────────────────────────

REAL_CREDS="$HOME/.claude/.credentials.json"
[[ -f "$REAL_CREDS" ]] || {
    echo "FAIL: No credentials at $REAL_CREDS" >&2
    exit 1
}

# ── Build isolated HOME ───────────────────────────────────────────────

SANDBOX_HOME=$(mktemp -d)
if [[ "$KEEP" == false ]]; then
    cleanup() { rm -rf "$SANDBOX_HOME"; }
    trap cleanup EXIT
fi

echo "Sandbox: $SANDBOX_HOME"

# Seed credentials
mkdir -p "$SANDBOX_HOME/.claude"
cp "$REAL_CREDS" "$SANDBOX_HOME/.claude/.credentials.json"

# Build enabledPlugins map
ENABLED_JSON="{"
for i in "${!PLUGINS[@]}"; do
    [[ $i -gt 0 ]] && ENABLED_JSON+=","
    ENABLED_JSON+="\"${PLUGINS[$i]}@batterie-de-savoir\":true"
done
ENABLED_JSON+="}"

# Seed settings.json with marketplace + enabled plugins
cat > "$SANDBOX_HOME/.claude/settings.json" << SETTINGS
{
  "permissions": {
    "allow": ["Bash", "Read", "Glob", "Grep", "Skill(*)"]
  },
  "extraKnownMarketplaces": {
    "batterie-de-savoir": {
      "source": {
        "source": "github",
        "repo": "spm1001/batterie-de-savoir"
      },
      "autoUpdate": true
    }
  },
  "enabledPlugins": $ENABLED_JSON
}
SETTINGS

# ── Minimal PATH ──────────────────────────────────────────────────────

CLEAN_PATH="${CLAUDE_DIR}:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

# ── Helper: run claude in sandbox ─────────────────────────────────────

run_sandboxed() {
    local prompt="$1"
    env -i \
        HOME="$SANDBOX_HOME" \
        PATH="$CLEAN_PATH" \
        TERM="${TERM:-dumb}" \
        CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1 \
        bash -c 'cd /tmp && exec "$@"' _ \
        claude -p --max-turns 1 --output-format json "$prompt" 2>/dev/null
}

# ── Test 1: Plugin install + skill discovery ──────────────────────────

echo ""
echo "=== Test 1: Skill Discovery ==="
echo "Installing plugins: ${PLUGINS[*]}"
echo ""

# Ask Claude to list its skills
RESULT=$(run_sandboxed "List all your available skills. Output ONLY the skill names, one per line, no descriptions or formatting. Just the names.")

if [[ "$VERBOSE" == true ]]; then
    echo "Raw output:"
    echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('result',''))" 2>/dev/null || echo "$RESULT"
    echo ""
fi

# Extract the text result
SKILL_OUTPUT=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('result',''))" 2>/dev/null || echo "$RESULT")

PASS=0
FAIL=0
SKIP=0

for plugin in "${PLUGINS[@]}"; do
    expected="${EXPECTED_SKILLS[$plugin]:-}"
    [[ -z "$expected" ]] && { echo "  SKIP $plugin (no expected skills defined)"; ((SKIP++)); continue; }

    for skill in $expected; do
        # Match both "skill" and "plugin:skill" formats
        if echo "$SKILL_OUTPUT" | grep -qiE "(^|:)$skill($|\s)"; then
            echo "  PASS $plugin/$skill"
            ((PASS++))
        else
            echo "  FAIL $plugin/$skill — not found in output"
            ((FAIL++))
        fi
    done
done

echo ""

# ── Test 2: Hook files exist ─────────────────────────────────────────

echo "=== Test 2: Hook File Existence ==="

CACHE_DIR="$SANDBOX_HOME/.claude/plugins/cache/batterie-de-savoir"

if [[ -d "$CACHE_DIR" ]]; then
    for plugin in "${PLUGINS[@]}"; do
        plugin_dir=$(find "$CACHE_DIR/$plugin" -maxdepth 1 -type d 2>/dev/null | head -1)
        [[ -z "$plugin_dir" ]] && { echo "  SKIP $plugin (not in cache)"; ((SKIP++)); continue; }

        # Check plugin.json
        pj="$plugin_dir/.claude-plugin/plugin.json"
        if [[ -f "$pj" ]]; then
            echo "  PASS $plugin/plugin.json exists"
            ((PASS++))

            # Check if hooks reference existing files
            hook_cmds=$(python3 -c "
import json, sys
d = json.load(open('$pj'))
for event, groups in d.get('hooks', {}).items():
    for group in groups:
        for hook in group.get('hooks', []):
            cmd = hook.get('command', '')
            # Replace variable with actual path
            cmd = cmd.replace('\${CLAUDE_PLUGIN_ROOT}', '$plugin_dir')
            print(f'{event}:{cmd}')
" 2>/dev/null)

            while IFS= read -r line; do
                [[ -z "$line" ]] && continue
                event="${line%%:*}"
                cmd="${line#*:}"
                script=$(echo "$cmd" | awk '{print $NF}')
                if [[ -f "$script" ]]; then
                    echo "  PASS $plugin/$event hook script exists"
                    ((PASS++))
                else
                    echo "  FAIL $plugin/$event hook references missing: $script"
                    ((FAIL++))
                fi
            done <<< "$hook_cmds"
        else
            echo "  FAIL $plugin/plugin.json missing"
            ((FAIL++))
        fi

        # Check SKILL.md files
        if [[ -d "$plugin_dir/skills" ]]; then
            for skill_dir in "$plugin_dir"/skills/*/; do
                skill_name=$(basename "$skill_dir")
                if [[ -f "$skill_dir/SKILL.md" ]]; then
                    # Check for allowed-tools in frontmatter
                    if head -20 "$skill_dir/SKILL.md" | grep -q "allowed-tools"; then
                        echo "  PASS $plugin/skills/$skill_name has allowed-tools"
                        ((PASS++))
                    else
                        echo "  WARN $plugin/skills/$skill_name missing allowed-tools"
                    fi
                else
                    echo "  FAIL $plugin/skills/$skill_name missing SKILL.md"
                    ((FAIL++))
                fi
            done
        fi

        # Check commands
        if [[ -d "$plugin_dir/commands" ]]; then
            md_count=$(find "$plugin_dir/commands" -name "*.md" | wc -l)
            toml_count=$(find "$plugin_dir/commands" -name "*.toml" | wc -l)
            echo "  PASS $plugin/commands: $md_count .md files"
            ((PASS++))
            if [[ $toml_count -gt 0 ]]; then
                echo "  WARN $plugin/commands: $toml_count .toml files (CC ignores these)"
            fi
        fi

        # Check LICENSE
        if [[ -f "$plugin_dir/LICENSE" ]]; then
            echo "  PASS $plugin/LICENSE exists"
            ((PASS++))
        else
            echo "  FAIL $plugin/LICENSE missing"
            ((FAIL++))
        fi
    done
else
    echo "  FAIL Plugin cache not created at $CACHE_DIR"
    ((FAIL++))
fi

# ── Summary ───────────────────────────────────────────────────────────

echo ""
echo "=== Summary ==="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  SKIP: $SKIP"

[[ "$KEEP" == true ]] && echo "" && echo "Sandbox preserved at: $SANDBOX_HOME"

exit $FAIL
