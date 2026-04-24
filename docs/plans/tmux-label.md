# Plan: tmux-label — Auto-label tmux windows from CC session theme

## Context

Sameer runs multiple CC sessions in tmux panes on hezza. He currently hand-labels windows ("reviewing easter tasks", "ways of working in 'work'", etc). The label describes *what we're trying to achieve* — a semantic, goal-level description, not tool-level activity.

The theme doesn't emerge until 3-5 turns in, then stabilises. It may evolve if the session pivots.

## Approach

A single bash hook script in trousse, registered as `UserPromptSubmit`. It accumulates user prompts in per-pane state files, and after a threshold of turns, fires a background Haiku call to generate a 2-4 word window label.

### How it works

1. Every `UserPromptSubmit`, the hook:
   - Reads the `prompt` field from stdin JSON
   - Appends it (truncated to 200 chars) to a rolling 5-prompt buffer
   - Increments a turn counter
2. At **turn 3** (first evaluation), **turn 8**, then **every 10 turns**: spawns a background LLM call
3. The LLM receives the recent prompts + current label + project name, returns a 2-4 word label
4. Background process runs `tmux rename-window` and writes the label to state

### Evaluation schedule

| Turn | Action |
|------|--------|
| 1-2 | Accumulate only |
| 3 | First LLM call — enough signal to form a label |
| 4-7 | Skip |
| 8 | Re-evaluate (catch early pivots) |
| 18, 28, ... | Re-evaluate every 10 turns |

Typical 15-turn session: exactly 2 LLM calls. Cost: negligible (~300 input tokens each).

### LLM call

```
claude -p --model haiku
```

Runs in background (`& disown`). The synchronous hook path takes <50ms and exits immediately. A lock file prevents stacking concurrent calls for the same pane.

### Prompt for the summariser

```
You label tmux windows. Given these user prompts from a coding session,
produce a 2-4 word label describing the session's goal.

Rules:
- 2-4 words, lowercase, no punctuation
- Describe the goal or task, not the tools or files
- Good: "fix auth redirect bug", "add csv export", "tmux auto labelling"
- Bad: "editing auth.ts", "working on code", "using grep"
- If the current label still describes the work, return it unchanged
- Reply with ONLY the label, nothing else

Working directory: {project}
Current label: {current_label or "none"}

Recent prompts:
{last 5 prompts}

Label:
```

### State files

Per-pane, in `/tmp/.tmux-label/`:

```
/tmp/.tmux-label/
  {pane_id}.prompts   # rolling buffer (last 5 lines)
  {pane_id}.count     # turn counter
  {pane_id}.label     # current label text
  {pane_id}.lock      # prevents concurrent LLM calls (30s staleness)
```

Keyed by `$TMUX_PANE` (stripped `%` prefix). Ephemeral — clears on reboot, which is correct.

### Guards (fail open, never block)

- No `$TMUX_PANE` → exit 0
- No `claude` CLI → exit 0
- `$CLAUDE_SUBAGENT` set → exit 0
- Lock file < 30s old → exit 0
- LLM returns garbage (empty, >40 chars, <3 chars) → silently ignored
- All errors trapped to exit 0

### tmux interaction

- `tmux rename-window -t $TMUX_PANE "label"` — works regardless of `allow-rename` setting (that controls escape sequences, not tmux commands)
- `tmux set-option -t $TMUX_PANE automatic-rename off` — prevents tmux overwriting the label with the running process name
- Current `~/.tmux.conf` has `allow-rename off` — no change needed

## Files to create/modify

| File | Action |
|------|--------|
| `~/Repos/batterie/trousse/hooks/tmux-label.sh` | **Create** — the hook script |
| `~/Repos/batterie/trousse/.claude-plugin/plugin.json` | **Edit** — add `UserPromptSubmit` hook entry |

### plugin.json addition

```json
"UserPromptSubmit": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/tmux-label.sh",
        "timeout": 2
      }
    ]
  }
]
```

## Not in scope

- Updating `batterie-de-savoir/docs/hook-map.md` or brigade.toml — this isn't a new tool, it's an environmental hook
- Cleanup of `/tmp/.tmux-label/` — reboot handles it
- Integration with the statusline — separate concern

## Verification

1. `cd ~/Repos/batterie/trousse && chmod +x hooks/tmux-label.sh`
2. Restart CC session in a tmux pane
3. Issue 3 prompts about a clear topic
4. Observe: window title should update within ~5 seconds of the 3rd prompt
5. Verify state files exist: `ls /tmp/.tmux-label/`
6. Issue prompts about a different topic, wait until turn 8 — label should update
7. Test outside tmux: hook should silently exit (no errors)
