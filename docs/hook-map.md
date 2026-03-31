# Hook Map

How the batterie uses Claude Code hooks. Updated 2026-03-30.

## Active Hooks by Repo

| Repo | SessionStart | UserPromptSubmit | SessionEnd | What it does |
|------|-------------|-----------------|------------|--------------|
| **bon** | `ensure-bon.sh` | `bon-tactical.sh` | `session-end.sh` | Health-checks `bon` CLI. Emits bon state + handoff summary for Claude on startup. Injects active tactical step into every prompt. Auto-writes handoff on exit if `/close` didn't run. |
| **bon** | `session-start.sh` | | | Runs `open-context.sh` (bon hierarchy, ready work, last handoff). Kicks off `update-all.sh` in background. Warns about incomplete `/close`. |
| **garde-manger** | `ensure-garde.sh` | | `session-end.sh` | Health-checks `garde` CLI + version alignment. Indexes session into garde-manger on exit, consumes staged extraction from `/close`. |
| **mise** | `ensure-mise.sh` | | | Health-checks uv, .venv, OAuth token. Auto-syncs deps if missing. |
| **todoist-gtd** | `ensure-todoist.sh` | | | Health-checks `todoist` CLI and API token (env var, Keychain, or file). |
| **global** | | `context-budget-hook.sh` | | Tiered context window usage warnings at 30/75/90%. Lives in `~/.claude/`, registered in `~/.claude/settings.json`. |

**Repos with no hooks:** trousse (empty `hooks.json` placeholder), aboyeur,
consomme, ecoute, gueridon, jeton, passe, plongeur, tafelmusik (has dormant
ensure hook, not installed).

### Ownership

Hook scripts are owned by their source repo — each `plugin.json` registers
scripts from its own `hooks/` directory. No cross-repo ownership mismatches.

### Machine Parity

| Plugin | Hezza | Mac | Issue |
|--------|-------|-----|-------|
| bon | 0.8.2 | 0.8.2 | |
| garde-manger | 0.3.1 | **not installed** | Enabled in settings but missing from `installed_plugins.json`. SessionStart + SessionEnd hooks don't fire — sessions on Mac aren't indexed. |
| mise | 0.5.2 | 0.5.2 | |
| todoist-gtd | 0.4.5 | 0.4.5 | |
| trousse | 0.4.0 | 0.4.0 | |
| compound-engineering | 2.56.1 | **not installed** | Not in Mac's `enabledPlugins` either — intentional per-machine difference. |

---

## Available But Unused

Claude Code provides 28 hook event types. We use 3. Notable unused events
relevant to the session lifecycle:

| Hook Event | Since | Can Block? | Potential Use |
|-----------|-------|-----------|---------------|
| **Stop** | v1.0.38 | Yes | Inject "/close reminder" when Claude is about to stop without having run /close. Could replace the SessionEnd safety-net approach with an interactive one. |
| **SubagentStop** | v1.0.41 | Yes | Inject context or tactical awareness into subagents before they finish. |
| **PreCompact** | v1.0.48 | No | Preserve critical context (bon state, active tactical) before compaction. |
| **PostCompact** | v2.1.74 | No | Re-inject context after compaction so Claude doesn't lose orientation. |
| **CwdChanged** | v2.1.80 | No | Reload bon context when Claude `cd`s to a different project. |
| **FileChanged** | v2.1.80 | No | React to `.bon/items.jsonl` changes from external processes. |
| **Notification** | v2.0.37 | No | Matchers: permission_prompt, idle_prompt, auth_success. |
| **StopFailure** | v2.1.78 | No | Observability when sessions crash (rate limits, auth errors). |
| **InstructionsLoaded** | v2.1.69 | No | Observability: which CLAUDE.md files loaded and why. |
| **SubagentStart** | v2.0.43 | No | Inject context into subagents at launch. |

### Hook Types

| Type | Since | Where Supported |
|------|-------|----------------|
| `command` | v1.0.38 | All 28 events |
| `http` | v2.0.55 | All except SessionStart |
| `prompt` | v2.0.30 | 9 events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, Stop, SubagentStop, TaskCreated, TaskCompleted, UserPromptSubmit) |
| `agent` | v2.0.65 | Same 9 events as prompt |

### Key Infrastructure

- **Conditional `if` field** (v2.1.86): Permission-rule syntax to skip hooks
  when they don't apply. Reduces process spawning.
- **`CLAUDE_ENV_FILE`**: SessionStart, CwdChanged, FileChanged hooks can
  persist env vars across the session.
- **`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`**: Configurable timeout for
  SessionEnd hooks (default was killing after 1.5s until v2.1.75).
- **Matchers**: SessionStart matches on `source` (startup/resume/clear/compact).
  SessionEnd matches on `reason` (clear/resume/logout/prompt_input_exit).

---

## Design Notes

### The SessionStart Bottleneck

Five hooks fire on SessionStart. Each is a separate process spawn. The bon
`session-start.sh` is the heaviest — it runs `open-context.sh` which reads
bon state and handoffs. The four `ensure-*` hooks are lightweight PATH/token
checks.

As of v2.1.72, Claude Code defers SessionStart hook execution (~500ms faster
startup). Hooks run in parallel per-plugin but sequentially across plugins.

### The Stop Hook Opportunity

The **Stop** hook is the most interesting unused event for session lifecycle.
It fires when Claude decides to stop responding, before the turn ends. It can
**block** (tell Claude to continue) and provide a reason. This means:

- It could check whether `/close` ran and, if not, tell Claude to run it
- Unlike SessionEnd (fire-and-forget), Stop is interactive — Claude can still
  act on the feedback
- `last_assistant_message` is available (v2.1.73+), so the hook can read what
  Claude was about to say

Risk: Stop hooks that always block create infinite loops. The `stop_hook_active`
field prevents re-entry, but the hook must have clear "don't block" conditions.

### CwdChanged for Multi-Project Sessions

When Claude `cd`s between projects, bon context becomes stale. A CwdChanged
hook could re-run `open-context.sh` for the new directory, keeping bon state
fresh without manual `/open`. This pairs with the `watchPaths` return value
to also monitor `.bon/items.jsonl` via FileChanged.
