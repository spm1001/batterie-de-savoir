---
layout: default
title: Plugin Capabilities Reference
---

# Plugin Capabilities Reference

*What the plugin system can do, what each batterie tool uses, and where the gaps are.*

Last updated: 2026-03-19

## How the Plugin System Works

### Installation and Cache

When a plugin is installed from a marketplace, Claude Code clones the repo into:

```
~/.claude/plugins/<plugin-name>/
```

The variable `${CLAUDE_PLUGIN_ROOT}` resolves to this path at runtime. All file references in plugin.json must use this variable — relative paths resolve to the user's cwd, not the plugin directory.

Plugins are refreshed on install or update. `/reload-plugins` refreshes the cache within a session. Full exit + restart (`/exit` then `claude -c`) is needed for SessionStart hooks to fire.

### What a Plugin Can Provide

A plugin is a git repo with a `.claude-plugin/plugin.json` manifest and optional auto-discovered directories.

#### Skills (`skills/<name>/SKILL.md`)

Auto-discovered. Each subdirectory of `skills/` with a `SKILL.md` file becomes an invocable skill. The SKILL.md content is loaded into Claude's context when the skill is invoked.

**Triggering:** Model-guided. Claude reads skill descriptions (from YAML frontmatter) and decides when to invoke based on context. Users can also invoke explicitly via `Skill(name)` or `/name`.

**No file placement.** Skills are read directly from the plugin cache. Nothing is copied to `~/.claude/skills/`. This replaces the old symlink model entirely.

#### Hooks (declared in `plugin.json` or `hooks/hooks.json`)

Deterministic shell commands that fire on specific events. Two declaration methods:

1. **In plugin.json** under a `"hooks"` key — explicit, visible in the manifest
2. **In `hooks/hooks.json`** — auto-discovered by convention

Do not use both — Claude Code raises a "Duplicate hooks" error.

Each hook is a shell command. It receives event-specific JSON on stdin and can return JSON on stdout. The key output mechanism:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Message injected into Claude's context"
  }
}
```

This is how hooks communicate: they tell Claude things via `additionalContext`, and Claude decides whether and how to surface them to the user. There is no mechanism to display a message directly to the user from a hook.

For PreToolUse hooks, returning `{"decision": "block"}` prevents the tool call.

#### Hook Events

| Event | When | Stdin contains | Can block? | Typical use |
|---|---|---|---|---|
| **SessionStart** | Session begins | Session metadata | No | Check prerequisites, inject context |
| **SessionEnd** | Session ends | Session metadata | No | Capture state, write handoffs |
| **UserPromptSubmit** | Every user message | `{cwd, ...}` | No | Inject reminders, tactical state |
| **PreToolUse** | Before tool executes | Tool name + arguments | **Yes** | Guard dangerous operations |
| **PostToolUse** | After tool executes | Tool name + result | No | Validate output, flag issues |
| **Stop** | Claude wants to stop | Conversation state | **Yes** (force continue) | Ensure checklist completion |
| **SubagentStop** | Subagent wants to stop | Subagent state | **Yes** | Same as Stop for delegated work |
| **PreCompact** | Before context compression | Context state | No | Preserve critical information |
| **Notification** | CC sends a notification | Notification content | No | Customise or suppress |

**Matcher field:** PreToolUse and PostToolUse hooks support a `"matcher"` string to filter by tool name (e.g. `"Bash"`, `"Edit"`). Other events use `""` (match all).

**Caveat:** SessionStart hooks fire on full session start, not on `/reload-plugins`. This means plugin installation cannot trigger setup guidance until the user exits and restarts.

#### MCP Servers (`"mcpServers"` in plugin.json)

Declared inline in plugin.json. Claude Code launches the server process automatically. MCP tools appear in Claude's tool list.

```json
"mcpServers": {
  "mise": {
    "command": "uv",
    "args": ["run", "--project", "${CLAUDE_PLUGIN_ROOT}", "python3", "${CLAUDE_PLUGIN_ROOT}/server.py"]
  }
}
```

**Startup is deterministic** (server launches on session start). **Use is model-guided** (Claude decides when to call MCP tools).

`${CLAUDE_PLUGIN_ROOT}` is only expanded inside plugin.json. External `.mcp.json` files referenced by path do not get variable expansion — inline the config instead.

#### Commands (`commands/<name>.md`)

Auto-discovered. Markdown files with YAML frontmatter, invoked by the user typing `/<name>`.

Key features that skills don't have:

| Feature | How it works |
|---|---|
| **`$ARGUMENTS`** | User input after the slash is interpolated into the markdown |
| **`` !`shell command` ``** | Shell commands in the markdown execute at load time, output spliced in before Claude thinks |
| **`allowed-tools`** | Pre-approves tools — no permission prompts for listed tools |
| **`argument-hint`** | Shown in `/help` list |
| **`model`** | Can override the model (e.g. use haiku for simple commands) |

Commands are user-initiated only. They do not trigger from model-guided context matching.

Commands can use `.md` format (with YAML frontmatter) or `.toml` format (with `description` and `prompt` fields).

#### Agents (`agents/<name>.md`)

Auto-discovered. Markdown files that define subagents Claude can delegate to.

| Field | Purpose |
|---|---|
| `description` | With trigger examples — Claude reads these to decide when to delegate |
| `tools` | Restricted tool set for the agent |
| `model` | Can use a different/cheaper model |
| `color` | TUI label colour |

Agents are model-delegated — Claude spawns them as subagents when it judges the task matches.

### What the Plugin System Does NOT Do

- **Install CLI tools.** Python packages providing executables (bon, garde, passe, todoist) need `uv tool install` separately. The plugin handles skills/hooks/MCP but not PATH binaries.
- **Show messages to users at install time.** No toast, no banner, no post-install script output.
- **Hot-reload hooks.** SessionStart hooks require full exit + restart.
- **Share state between plugins.** Each plugin is isolated. Cross-plugin coordination happens via the filesystem (e.g. `.bon/` directory) or via skills that reference each other by name.
- **Declare dependencies on other plugins.** No `"requires"` field. Soft dependencies are documented in descriptions ("Best with: bon, garde-manger").

### File Layout Summary

```
my-plugin/
  .claude-plugin/
    plugin.json          # Manifest (required)
  skills/
    my-skill/
      SKILL.md           # Skill content (auto-discovered)
      references/        # Supporting files loaded by @reference
  hooks/
    hooks.json           # Hook declarations (auto-discovered, OR use plugin.json)
    my-hook.sh           # Hook scripts
  commands/
    my-command.md        # Slash commands (auto-discovered)
  agents/
    my-agent.md          # Subagent definitions (auto-discovered)
  scripts/
    helper.sh            # Internal scripts (NOT auto-discovered — called by hooks/skills)
  LICENSE                # Required for marketplace
  README.md              # Required for marketplace
```

---

## Current Usage Matrix

Which plugin capabilities each batterie tool currently uses.

### Skills

| Plugin | Skills | Notes |
|---|---|---|
| **bon** | tracker, open, close, audit | Session lifecycle + work tracking |
| **trousse** | 18 skills (titans, diagram, picture, skill-forge, screenshot, ...) | Utility/behavioural skills |
| **mise** | workspace | Google Workspace orchestration |
| **todoist-gtd** | coaching | GTD coaching for Todoist |
| **garde-manger** | memory | Persistent memory search |
| **passe** | browser | Chrome automation |
| **consomme** | analysis | BigQuery methodology |
| **gueridon** | setup | Mobile UI setup |

### Hooks

| Event | bon | trousse | mise | todoist-gtd | garde-manger | passe | consomme | gueridon |
|---|---|---|---|---|---|---|---|---|
| **SessionStart** | ensure-bon + session-start | — | ensure-mise | ensure-todoist | ensure-garde | — | — | — |
| **SessionEnd** | session-end | — | — | — | session-end | — | — | — |
| **UserPromptSubmit** | bon-tactical | — | — | — | — | — | — | — |
| **PreToolUse** | — | — | — | — | — | — | — | — |
| **PostToolUse** | — | — | — | — | — | — | — | — |
| **Stop** | — | — | — | — | — | — | — | — |
| **SubagentStop** | — | — | — | — | — | — | — | — |
| **PreCompact** | — | — | — | — | — | — | — | — |
| **Notification** | — | — | — | — | — | — | — | — |

### MCP Servers

| Plugin | MCP Server | Tools provided |
|---|---|---|
| **mise** | mise | Google Drive search, Gmail search, document fetch, file operations |
| All others | — | — |

### Commands

| Plugin | Commands | Notes |
|---|---|---|
| **batterie** | 1 command (.md format) | batterie-update — cross-plugin updater with marketplace refresh, CLI drift detection, and auto-install |
| **consomme** | 7 commands (.toml format) | consomme, consomme-explore, consomme-ingest, consomme-profile, consomme-dashboard, consomme-sheets, consomme-validate |
| All others | — | — |

### Agents

| Plugin | Agents | Notes |
|---|---|---|
| All | — | None of our plugins define agents yet |

### CLI Tools (outside plugin system)

| Plugin | CLI binary | Install method |
|---|---|---|
| **bon** | `bon` | `uv tool install "${CLAUDE_PLUGIN_ROOT}"` |
| **garde-manger** | `garde` | `uv tool install garde-manger` |
| **passe** | `passe` | `uv tool install passe` |
| **todoist-gtd** | `todoist` | `uv tool install todoist-gtd` |
| **mise** | — | No CLI; MCP server only |
| **trousse** | — | No CLI; skills only |
| **consomme** | — | No CLI; skills + commands only |
| **gueridon** | — | Node.js app, separate setup |

---

## Friction Points and Opportunities

### Overview

| Area | Issue | Severity | Plugins affected | Section |
|---|---|---|---|---|
| **Hooks: Stop** | No completion enforcement | High | bon, trousse | [H1](#h1-stop-hooks-for-session-discipline) |
| **Hooks: PreCompact** | Context loss on compaction | High | bon, garde-manger | [H2](#h2-precompact-to-preserve-state) |
| **Hooks: PreToolUse** | No convention guardrails | Medium | trousse, bon | [H3](#h3-pretooluse-for-convention-enforcement) |
| **Hooks: SessionStart** | No fire on reload | Medium | all with hooks | [H4](#h4-sessionstart-doesnt-fire-on-reload-plugins) |
| **Commands** | Skills used where commands fit better | Medium | bon, trousse | [C1](#c1-skills-that-should-be-commands) |
| **Agents** | No custom agents defined | Low | trousse, bon | [A1](#a1-subagents-for-parallel-review) |
| **CLI install** | No version drift detection | Medium | bon, passe, todoist-gtd, garde-manger | [T1](#t1-cli-version-drift) |
| **CLI install** | uv tool install not editable | Low | all with CLIs | [T2](#t2-uv-editable-installs) |
| **Prerequisites** | Silent failure without setup hooks | Medium | garde-manger, passe, consomme, gueridon | [P1](#p1-plugins-missing-prerequisite-checks) |
| **Cross-plugin** | No dependency declaration | Low | all | [X1](#x1-cross-plugin-dependencies) |

---

### <a id="h1-stop-hooks-for-session-discipline"></a>H1: Stop hooks for session discipline

**What:** The Stop event fires when Claude wants to finish responding. A hook can force continuation by returning `{"decision": "block"}` with a message explaining what's missing.

**Opportunity:** Enforce the GODAR pattern mechanically. Before Claude stops after substantial work, a Stop hook could check:
- Did bon items get updated? (`bon show --json` → check for stale tactical)
- Is there a handoff written for long sessions?
- Were tests run if code was changed?

This is currently handled by skill instructions (the close skill says "follow GODAR") but nothing enforces it. A Stop hook makes it structural.

**Complication:** Stop hooks fire on *every* response, not just session-ending ones. The hook needs to distinguish "Claude finished answering a question" from "Claude finished a multi-step task." May need heuristics (session duration, number of tool calls, file changes detected).

**Belongs in:** bon (owns session lifecycle).

---

### <a id="h2-stop-hooks-for-session-discipline"></a>H2: PreCompact to preserve state

**What:** PreCompact fires before Claude Code compresses the conversation to fit the context window. This is where we lose track of what we were doing in long sessions.

**Opportunity:** Inject a structured summary before compaction:
- Current bon tactical state and recent steps completed
- Key decisions made this session
- Files modified
- Any waiting-fors or blockers identified

This would act as a "you are here" marker that survives compaction. Currently we rely on Claude remembering, and it often doesn't after compaction.

**Belongs in:** bon (owns tactical state) and potentially garde-manger (could persist the summary).

---

### <a id="h3-pretooluse-for-convention-enforcement"></a>H3: PreToolUse for convention enforcement

**What:** PreToolUse fires before any tool call. It can inspect the tool name and arguments, then block or inject warnings.

**Opportunities:**
- **WebFetch guard:** Block WebFetch and inject "use passe fetch instead" (currently only in trousse's old install.sh, not active as a plugin hook)
- **Commit convention:** On `Bash(git commit:*)`, check commit message format
- **Dangerous command guard:** Warn on `rm -rf`, `git push --force`, `git reset --hard`
- **TodoWrite suppression:** Remind Claude to use bon instead (currently in deny list, but a hook could explain *why*)

**Belongs in:** trousse (behavioural guardrails are its domain). This would give trousse hooks again — purposeful ones, not the ghost hooks it had before.

---

### <a id="h4-sessionstart-doesnt-fire-on-reload-plugins"></a>H4: SessionStart doesn't fire on /reload-plugins

**What:** After installing a plugin, the TUI tells users to run `/reload-plugins`. But SessionStart hooks — which provide setup guidance — only fire on full exit + restart.

**Impact:** Users install a plugin, reload, and get no guidance. The ensure-* hooks (ensure-bon, ensure-mise, ensure-todoist) that check prerequisites never fire until the next full session.

**Workaround options:**
1. **Report as CC bug/feature request.** SessionStart should fire on reload — the TUI already tells users to reload.
2. **Duplicate guidance in skill descriptions.** The skill itself can check prerequisites when invoked, not just at session start.
3. **Use UserPromptSubmit as fallback.** A one-shot check on the first prompt after install. Set a flag file to avoid repeating.

**Affects:** All plugins with SessionStart hooks.

---

### <a id="c1-skills-that-should-be-commands"></a>C1: Skills that should be commands

**What:** Several of our skills are always user-invoked via `/name` and would benefit from command-specific features.

| Skill | Why it's a better command |
|---|---|
| `/open` | Could `!`backtick`` git status, bon show, last handoff at load time instead of tool calls |
| `/close` | Could pre-approve Write, Bash for handoff writing |
| `/commit` (if we made one) | Could `!`backtick`` git diff + git log, pre-approve `Bash(git:*)` |
| `/audit` | Could `!`backtick`` bon list at load time |

The `!`backtick`` feature is particularly valuable — it gathers context *before* Claude starts thinking, saving tool call round-trips and giving Claude a complete picture from the start.

**Not all skills should become commands.** Skills that are model-triggered (titans, diagram, skill-forge) should stay as skills. The distinguishing question: "Does the user always invoke this explicitly?" If yes, it's a command.

**Consideration:** Can a skill and a command coexist with the same name? If so, the skill handles model-triggered invocation while the command handles `/name` invocation. If not, we'd need to choose.

**Belongs in:** bon (open, close, audit) and potentially a new shared commands set.

---

### <a id="a1-subagents-for-parallel-review"></a>A1: Subagents for parallel review

**What:** The agents/ directory lets plugins define specialist subagents that Claude can delegate to.

**Opportunity:** Trousse's titans skill (Epimetheus/Metis/Prometheus three-lens review) currently instructs Claude to spawn three parallel subagents via the Agent tool. If these were declared as plugin agents with their own system prompts and tool sets, they'd be:
- Reusable outside the titans skill
- Discoverable by Claude without loading the full skill
- Configurable with restricted tool sets and model overrides

Similarly, bon's audit skill dispatches subagents to verify brief items against code. These could be declared agents.

**Belongs in:** trousse (review agents), bon (verification agents).

---

### <a id="t1-cli-version-drift"></a>T1: CLI version drift

**What:** When a plugin updates (new version pulled into cache), the CLI binary installed via `uv tool install` remains at the old version. The plugin's skills and hooks update, but the CLI doesn't.

**Opportunity:** A SessionStart hook that compares the installed CLI version against the plugin version:

```bash
INSTALLED=$(bon --version 2>/dev/null)
EXPECTED=$(python3 -c "import json; print(json.load(open('${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json'))['version'])")
if [ "$INSTALLED" != "$EXPECTED" ]; then
  # inject: "bon CLI is v$INSTALLED but plugin is v$EXPECTED — run: uv tool install ${CLAUDE_PLUGIN_ROOT} --force"
fi
```

**Belongs in:** Each plugin that has a CLI (bon, garde-manger, passe, todoist-gtd). Could be a shared pattern in ensure-*.sh hooks.

---

### <a id="t2-uv-editable-installs"></a>T2: uv editable installs

**What:** `uv tool install` copies the package at a point in time. There is no `uv tool install -e` for editable/live installs. Every source change requires `uv cache clean <pkg> && uv tool install <path> --force --reinstall`.

**Impact:** Reduced now that the plugin cache handles skills/hooks/MCP. The CLI binary is the only thing that needs reinstalling. But during active CLI development it's still friction.

**Mitigation:** This is a uv roadmap item, not something we can fix. Version drift detection (T1) is the practical workaround.

---

### <a id="p1-plugins-missing-prerequisite-checks"></a>P1: Plugins missing prerequisite checks

**What:** Three plugins require external tools or services but have no SessionStart hook to verify:

| Plugin | Prerequisites | What fails silently |
|---|---|---|
| **passe** | `passe` CLI + Chrome with CDP on port 9222 | Browser skill tells Claude to run passe commands |
| **consomme** | Google BQ MCP extension | Analysis skill references MCP tools that aren't available |
| **gueridon** | Node.js + Tailscale | Setup skill assumes both are present |

**Resolved:** garde-manger added `ensure-garde.sh` in v0.3.0 (Mar 2026), including CLI version alignment check.

**Pattern to follow:** bon, mise, todoist-gtd, and now garde-manger all have `ensure-*.sh` hooks that check prerequisites and inject guidance via `additionalContext`. The pattern is established — it just needs replicating for the remaining three.

**Belongs in:** Each plugin, as `hooks/ensure-<name>.sh`.

---

### <a id="x1-cross-plugin-dependencies"></a>X1: Cross-plugin dependencies

**What:** The plugin system has no `"requires"` or `"recommends"` field. Soft dependencies are noted in description text ("Best with: bon, garde-manger") but nothing enforces or checks them.

**Practical impact:** Low. Our plugins fail gracefully when companions are missing — skills check for CLI availability, hooks exit silently. But a new user wouldn't know that trousse works better with bon until they read the description carefully.

**Workaround:** SessionStart hooks can check for companion plugins:

```bash
[ -d ~/.claude/plugins/bon ] || echo "Note: trousse works best with bon installed"
```

This is informational, not blocking. The description field remains the primary signal.

---

## Consomme: A Different Pattern

Consomme was the first batterie plugin to use the **commands** feature (7 `.toml` commands). The batterie plugin itself now also has a command (`/batterie-update`). Consomme's approach gives it a clean sub-command UX:

```
/consomme          → orient
/consomme-explore  → discover datasets
/consomme-ingest   → load data
/consomme-profile  → inspect a table
/consomme-dashboard → build visualisation
/consomme-sheets   → analyse a spreadsheet directly
/consomme-validate → QA checklist
```

Each command uses `{{args}}` for argument interpolation and a focused `prompt` field. This is a good model for other plugins that have distinct operational modes — bon could have `/bon-show`, `/bon-work`, `/bon-step` as commands rather than routing everything through the skill.

---

## Summary: What We Have vs What's Available

```
                    USING          NOT USING
Skills              ████████████
Commands            ██             ██████████   (batterie + consomme)
Agents              ░              ████████████ (none)
MCP Servers         █              ███████████  (only mise)

SessionStart        █████          ███          (5/8 plugins)
SessionEnd          ██             ██████████   (bon + garde-manger)
UserPromptSubmit    █              ███████████  (only bon)
PreToolUse          ░              ████████████ (none)
PostToolUse         ░              ████████████ (none)
Stop                ░              ████████████ (none)
SubagentStop        ░              ████████████ (none)
PreCompact          ░              ████████████ (none)
Notification        ░              ████████████ (none)
```

We are skill-heavy and hook-light. Commands are gaining traction (batterie + consomme), but the plugin system's most powerful features — Stop hooks for discipline, PreCompact for memory, PreToolUse for guardrails, declared agents — remain unused. The infrastructure is there; the wiring isn't.
