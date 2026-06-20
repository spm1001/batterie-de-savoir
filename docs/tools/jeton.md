---
layout: default
title: Jeton
---

# Jeton — The token

Google OAuth token management for the Batterie de Savoir. Every Google-facing tool in the suite — mise for Workspace content, consommé for BigQuery — needs OAuth credentials. Jeton handles the full OAuth 2.0 flow so the tools themselves don't have to reinvent authentication. It acquires tokens, refreshes them when they expire, and manages scope negotiation across three auth modes.

## When to use / When NOT to use

**Use jeton when:**

- You need Google API access from a Python tool in the suite
- You're setting up mise or consommé for the first time and need credentials
- A token has expired or scopes have changed and you need to re-authenticate
- You want to check token status or available scopes

**Do NOT use jeton when:**

- You're accessing non-Google APIs — jeton is Google OAuth only
- You need macOS Keychain secrets — use `security find-generic-password`
- You're working with a tool that manages its own auth (e.g., `gh` for GitHub)

## Key concepts

### Three auth modes

Jeton supports three ways to complete the OAuth flow, chosen based on the environment:

| Mode | Flag | When to use |
|------|------|-------------|
| **Auto** | *(default)* | Local development — starts localhost:3000, opens browser, handles callback |
| **Manual** | `--manual` | SSH, remote, headless — prints URL, you paste the redirect back |
| **Non-interactive** | `--manual --code URL` | Scripting, CI, Claude Code — provide the auth code directly |

### Scope shortcuts

Instead of typing full Google OAuth URLs, jeton uses readable shortcuts: `drive.readonly`, `gmail.readonly`, `sheets`, `calendar`. The CLI and Python API both accept these shortcuts and resolve them to the full scope URIs.

### Explicit paths over defaults

Each project provides its own `credentials.json`, `token.json`, and scopes. There's no shared `~/.config/jeton/` directory. This keeps projects independent — one project's tokens can't leak into another's scope. The consuming tool (mise, consommé) passes paths explicitly when calling jeton's Python API.

### Token refresh

Tokens expire. Jeton handles refresh transparently — if a valid refresh token exists, `load_credentials()` returns fresh credentials without user interaction. The `jeton status` command shows whether a token is valid, expired-but-refreshable, or needs full re-auth.

### Scope mismatch handling

Google sometimes grants different scopes than requested (incremental auth). Jeton catches the `Scope has changed` error during token exchange and extracts credentials manually rather than failing. This is a known Google OAuth quirk that jeton absorbs so downstream tools don't have to.

## How it relates to other tools

Jeton is **infrastructure** — it sits beneath the Google-facing tools and provides them with credentials. It has no skill of its own (no behavioural document to load) because agents don't interact with it directly during normal work. It's plumbing.

| Tool | Relationship to jeton |
|------|----------------------|
| **Mise** | Primary Python consumer — calls `authenticate()` and `load_credentials()` for Workspace access |
| **Consommé** | Uses jeton credentials when connecting to BigQuery via Google APIs |
| **Bon, Trousse, Passe** | No dependency — these don't touch Google APIs |

When you set up mise for the first time, jeton is the prerequisite. Run `jeton` to complete the OAuth flow, and mise picks up the resulting `token.json`.

## CLI

```
jeton                    # Authenticate (auto mode)
jeton --manual           # Authenticate (manual mode — prints URL)
jeton status             # Show token validity and scopes
jeton refresh            # Force token refresh
jeton list-scopes        # Show available scope shortcuts
```

## Python API

```python
from jeton import authenticate, load_credentials, TokenStatus

# Full OAuth flow (interactive)
creds = authenticate(credentials_path, token_path, scopes)

# Load existing token (refreshes if needed)
creds = load_credentials(token_path, scopes)

# Check token status without modifying it
status = TokenStatus.check(token_path)
```

## Prerequisites

- A Google Cloud project with OAuth 2.0 credentials (`credentials.json`)
- The relevant Google APIs enabled in your GCP project
- Python 3.11+ with uv

## Repo

Install, usage, and full reference: [github.com/spm1001/jeton](https://github.com/spm1001/jeton)
