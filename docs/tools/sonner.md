---
layout: default
title: Sonner
---

# Sonner

*The bell.*

`sonner` is French for *to ring*. In a kitchen the bell at the pass cuts across the noise — service, please, now. Sonner does that between Claude Code sessions, with one change of aim that turns out to matter: **it rings a repo, not a session.**

That sounds like a detail and isn't. The harness's own `SendMessage` addresses a *session id* — which means before you can say anything you have to know who exists, and if nobody is home in the place you care about, you can't say it at all. Sonner takes the address you actually have in your head:

```bash
sonner infra "the deploy is red — can you look at the workflow file?"
```

A live session in that repo gets it on its inbox socket. An **empty** repo gets a session spawned under tmux first, and *then* the message is delivered — so it still arrives framed as a peer message rather than as the user speaking.

It supersedes [Sonnette](https://github.com/spm1001/aboyeur), which was delisted from the suite in August 2026.

## The one thing to understand: delivery is not the same as being heard

Sonnette's trap was that sending and receiving were asymmetric — you could hold the tools and still be structurally deaf unless the session was launched with a special flag. Sonner removes that: there is no launch flag, and any session that binds a socket can hear.

But a quieter version of the problem survives, and it is worth knowing before you build anything that waits for a reply:

- **Deaf sessions are real.** A session billed through a third-party provider writes a full registry record with no `messagingSocketPath`. It is live, busy, and reachable by nothing. Its repo does not look empty — it looks occupied and silent.
- **Claude Code silently drops a byte-identical repeat message while reporting success to the sender.** Sonner timestamps every message by default precisely so your second attempt isn't swallowed. `--no-stamp` exists for genuine one-offs; don't make it your habit.
- **A cold spawn needs a trusted directory.** A session spawned into a folder Claude Code doesn't trust stalls at the trust dialog and never binds its socket, so the ring times out looking like a slow start rather than a blocked one.

The habit that covers all three is an explicit acknowledgement round-trip before you rely on anything you sent. The companion **peer-messaging** skill carries that and the rest of the house rules; it ships with the plugin and is worth loading before your first ring.

## Seeing who's out there

```bash
sonner --list                    # every reachable session and the repo it sits in
sonner --wake <repo>             # ensure a session exists, say nothing yet
sonner --name <name> "message"   # ring one specific session from the registry
```

Discovery deliberately unions two sources — the sockets on disk and every config directory's session records — because each catches sessions the other misses. If you are tempted to simplify that to one source, it has been tried.

## When to use / When NOT to use

**Use Sonner when:**
- You want an opinion from the Claude that actually knows another codebase, and you'd rather not care whether one is currently running there
- You need to nudge or query a long-running session without touching its files
- Two sessions are genuinely co-working and a handoff file is too slow a channel

**Do NOT use Sonner when:**
- The content needs to survive the session — ring the bell to point at a file, don't paste the wall of text. A pointer survives the peer dying mid-read; a pasted essay doesn't
- You want orchestration rather than conversation — alternating workers and reflectors over a body of work is [Aboyeur](aboyeur)'s job
- You want the message to read as an instruction from the human. It won't, by design: sonner delivers over the socket *after* the session starts, specifically so peer framing and the harness's peer guardrails stay intact

## Prerequisites

Needs [uv](https://docs.astral.sh/uv/) on the host, and `tmux` if you want it to spawn sessions. The CLI is stdlib-only, so there is nothing else to install. The plugin's session hook puts `sonner` on PATH the first time it finds it missing:

```
claude plugin install sonner@batterie
```

One caveat worth carrying: that hook installs a *missing* CLI and does not replace a present one, so a machine that already had `sonner` installed from source keeps its old copy. If the documented verbs above don't exist in your `sonner --help`, reinstall with `uv tool install git+https://github.com/spm1001/sonner --force --reinstall --no-cache`.
