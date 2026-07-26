---
layout: default
title: Plugin Capabilities Reference
---

# Plugin Capabilities Reference

*What the plugin system can do, what each batterie tool uses, and where the gaps are.*

> **Scope note (trimmed 2026-07-26).** This page is evergreen Claude Code plugin-system reference — how the machinery works, not what the suite currently uses it for. The usage-matrix and friction snapshots that used to live below rotted and were removed (see the pointer at the end for where current state lives). For canonical install steps see [getting-started](getting-started.html) and [for-agents](for-agents.html); for current versions run `/batterie:version`.

## How the Plugin System Works

### Installation and Cache

When a plugin is installed via the CLI from a marketplace, Claude Code clones the marketplace and stores plugin content under:

```
~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/
```

(Claude **Desktop** is a separate codepath — it loads from Anthropic's server-side marketplace, not this local cache. See "Desktop vs CLI" in the repo's understanding.md.)

The variable `${CLAUDE_PLUGIN_ROOT}` resolves to the plugin's cache path at runtime. All file references in plugin.json must use this variable — relative paths resolve to the user's cwd, not the plugin directory.

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

- **Install CLI tools.** Python packages providing executables (bon, todoist) need `uv tool install` separately — the suite's session hooks do this install-if-missing. The plugin handles skills/hooks/MCP but not PATH binaries.
- **Show messages to users at install time.** No toast, no banner, no post-install script output.
- **Hot-reload hooks.** SessionStart hooks require full exit + restart.
- **Share state between plugins.** Each plugin is isolated. Cross-plugin coordination happens via the filesystem (e.g. `.bon/` directory) or via skills that reference each other by name.
- **Declare dependencies on other plugins.** No `"requires"` field. Soft dependencies are documented in descriptions ("Best with: bon").

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

## Where the rest of this page went

Until July 2026 this page also carried a **Current Usage Matrix** (which capabilities each
batterie tool uses) and a **Friction Points** section — both a March 2026 snapshot that drifted
as tools changed (passe rows survived its delisting by three weeks; one friction point shipped
as resolved). Hand-maintained inventory tables rot; that lesson is why they're gone rather than
refreshed (bds-naceje).

For current state, ask the systems that can't drift:

- **What's in the suite:** the [generated brigade table](index) (from `brigade.toml`)
- **What each plugin ships:** its repo README skill table (generated from `skills/`, checked in CI)
- **What's installed and at what version:** `/batterie:version`
- **Agent-facing routing and vocabulary:** [for-agents](for-agents) (generated)

The history is in git if you want the snapshot back.
