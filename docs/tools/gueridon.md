---
layout: default
title: Guéridon
---

# Guéridon

*Tableside trolley — mobile web UI for Claude Code.*

In fine dining, the guéridon is the small table wheeled to your table for tableside service — flambé, carving, preparation done right in front of you. This tool does the same thing for Claude Code: it brings the full session experience to wherever you are — phone, tablet, or a browser on a different machine — via a lightweight bridge that speaks Claude's streaming protocol over WebSocket.

## When to use

- You want to interact with Claude Code from a mobile device or remote browser.
- You're away from your terminal but want to continue (or monitor) a session.
- You need to run Claude Code on one machine (e.g., a Kube server) and access it from another.

## When NOT to use

- You're already at your terminal — just use Claude Code directly.
- You need to run CLI tools or scripts interactively — guéridon is a conversational interface, not a terminal emulator.
- You want to automate Claude across multiple sessions — that's [aboyeur](aboyeur).

## Key Concepts

**Process-per-session.** Each connected session gets its own `claude -p` process running in `stream-json` mode against a MAX subscription. There's no shared daemon or connection pool — one bridge, one process, one conversation.

**Lazy spawn.** The Claude Code process doesn't start when the WebSocket connects — it starts on the first prompt. This keeps idle connections cheap and avoids wasting cold-start time on sessions that never send a message.

**Resume.** Sessions carry a session-id. If the bridge process is killed or the connection drops, the client reconnects and the bridge resumes the session via `--resume`. The ~8-second cold start only happens once; reconnects pick up where you left off. Idle sessions time out after 5 minutes.

**Single-port bridge.** The Node.js bridge serves both HTTP and WebSocket on a single port (`:3001`). Mobile browser connects over the network — no tunnelling or proxy config required.

**CLI client.** In addition to the mobile web UI, there's a terminal client for accessing the bridge from a different machine — useful for SSH-ing to a remote box and talking to the bridge without a browser.

## How it Relates to Other Tools

Guéridon extends Claude Code's reach without changing its protocol. The session you start from your phone is the same kind of session you'd run in a terminal — same skills from [trousse](trousse), same handoffs, same [garde-manger](garde-manger) memory. The bridge is transparent; it's a delivery mechanism, not a new runtime.

The bridge can run on a different machine from where you're browsing, which means guéridon also serves as remote access infrastructure — run the bridge on a server, connect from anywhere.

Where [aboyeur](aboyeur) orchestrates *multiple* Claude sessions, guéridon gives you *one* session, untethered from the terminal.

## Links

- [Repository](https://github.com/spm1001/gueridon) — install, usage, and development
