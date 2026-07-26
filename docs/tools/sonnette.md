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

One more binding constraint: channel binding is a first-party feature. Sessions billed through third-party providers can't bind channels at all — Claude Code ignores the flag at launch and says so in its banner ("Channels are not available on Bedrock, Vertex, or Foundry"). Whatever else a Vertex-billed session has, it is structurally deaf to the mesh.

## Designing the trap away: all-or-nothing launch

The halfway state — tools present, inbound dead — can be abolished at the estate level rather than merely documented (proven 2026-07-26, bds-micozi):

- **Standing state: installed but disabled.** `claude plugin disable sonnette@batterie`. The plugin stays installed, so `/batterie:update` keeps its cache current — but no session loads its MCP by default. Bare, cron, background and headless sessions get *neither* tools nor a mesh registration: nothing left to look mesh-capable while deaf.
- **Mesh launches re-enable it per-launch**, alongside the channels flag:

  ```
  claude --settings '{"enabledPlugins":{"sonnette@batterie":true}}' \
         --dangerously-load-development-channels plugin:sonnette@batterie
  ```

  Wrap that in a shell function (`claudem` on this estate) and every mesh session is born with tools *and* inbound, while every other session has neither.

Three measured facts hold the pattern together. The channels flag *rides* an enabled plugin — it cannot load a disabled or uninstalled one (the launch banner reads `plugin not installed` and no tools appear). Repeated `--settings` flags are last-wins, not merged — a wrapper that already passes `--settings` (billing env, say) must splice the enable into its existing JSON rather than add a second flag. And a wrapper whose billing is third-party should *refuse* its mesh flag outright — enabling the plugin there would mint a registered-but-deaf session on purpose, which is the exact state this pattern exists to kill. Daemon-spawned [Aboyeur](aboyeur) workers are untouched throughout: they bind `server:conductor-channel` directly and never ride the plugin.

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
