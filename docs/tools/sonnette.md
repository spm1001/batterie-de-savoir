---
layout: default
title: Sonnette
---

# Sonnette

*The bell.*

In a professional kitchen, the sonnette is the bell at the pass — a sharp ring that cuts across the noise: service, please, now. Sonnette does the same between Claude sessions. It connects a session to the **conductor mesh**, a peer-to-peer channel where live sessions can discover each other (`mesh_peers`) and message each other (`send_message`) — across repos, across machines, in real time.

It lives in the [Aboyeur](https://github.com/spm1001/aboyeur) repo, and the two are siblings with different tempos: Aboyeur coordinates sessions *across time* (worker → handoff → reflector), Sonnette connects them *in the moment* (a live session rings another live session).

## The one thing to understand: sending and receiving are not symmetric

**Having Sonnette's tools in your context does not mean you can receive.** This is the trap the page exists to flag.

- **Sending always works.** Any session with the plugin installed can call `send_message` and `mesh_peers` — outbound is just an MCP tool call.
- **Receiving only works if the session was *launched* for it.** Inbound mesh messages arrive as `<channel source="conductor-channel">` tags, and a session only gets those if it was started with the channels flag:

  ```
  claude --dangerously-load-development-channels plugin:sonnette@batterie
  ```

  One trust dialog per launch, then inbound messages surface live. A session launched *without* the flag never sees them — it is **send-only**, however connected it looks.

So before building anything conversational on the mesh — a request that expects a reply, a ping-and-wait — check which kind of session you are. If you're not channel-bound, you can ring the bell but you can't hear it ring back; ask the human to relay, or fall back to files (handoffs are the durable protocol).

One more binding constraint: channel binding is a first-party feature. Sessions billed through third-party providers (e.g. Vertex) can't bind channels at all — the outbound tools still work there, but those sessions are structurally send-only.

## When to use / When NOT to use

**Use Sonnette when:**
- You want a live opinion from a session sitting in another repo — a peer review from the Claude that actually knows that codebase (the `consult` pattern rides on this)
- You need to nudge or query a long-running session without touching its files
- Two sessions are genuinely co-working and need a channel faster than handoff files

**Do NOT use Sonnette when:**
- The message needs to survive the session — mesh messages are ephemeral; durable context goes in handoffs, [Bon](bon) items, or files (files are the protocol)
- You want orchestration rather than conversation — alternating workers and reflectors over a body of work is [Aboyeur](aboyeur)'s job
- The receiving session isn't channel-bound — see above; a message into a send-only session's mesh is a bell nobody hears

## Prerequisites

Requires [bun](https://bun.sh) on the host. Installs from the marketplace like any suite plugin: `claude plugin install sonnette@batterie`.
