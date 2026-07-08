# Distribution Spike Result — ITV/mit-commons (bds-nupepe)

Run: 2026-07-08, on tube. Companion to `team-platform-requirements.md`; feeds
bds-halonu (question a) and bds-ronuho (blueprint distribution section).

## The question

Does Claude Code's marketplace machinery work against a **private, SAML-SSO,
ITV-org** GitHub repo — and what does onboarding cost per teammate?

## The answer: yes, end-to-end, with zero Claude-specific auth

Proven live, all four links:

1. **Created** `ITV/mit-commons` private via `gh repo create` from a CC session.
2. **`claude plugin marketplace add ITV/mit-commons`** — resolved the shorthand to
   GitHub, cloned via HTTPS through the ambient git credential helper
   (`!gh auth git-credential`). No Claude-side token, no GitHub App, no PAT setup.
   The SAML/private wall is invisible to Claude because git itself carries the
   credentials.
3. **`claude plugin install mit-commons@mit-commons`** — instant, from the local
   marketplace clone (user scope).
4. **Skill invoked** in a fresh CC session (`claude -p "/mit-commons:hello"`) —
   responded correctly, reporting its version from the delivered plugin.json.

## Topology validated

The repo IS the marketplace — `.claude-plugin/` holds both `marketplace.json` and
`plugin.json`, the single plugin's `source` is `"./"` (repo root), `skills/` sits
flat at top level. No assembler, no vendoring, no version stamping. Merge = shipped.
This is the shape the blueprint favours, now tested rather than assumed.

## Per-teammate onboarding cost (the mit-plongeur dance × 8 question)

**The marketplace adds nothing beyond standard private-ITV-repo access.** The full
prerequisite is exactly "can you clone a private ITV repo over HTTPS?":

- Install `gh` CLI, `gh auth login` (browser device-flow), authorize the token for
  the ITV org when the SSO prompt appears. One-time per person per machine, ~5 min.
- Anyone already working with ITV GitHub from a terminal has already paid this —
  their incremental cost is the two `claude plugin` commands.
- Updates ride the same credentials (marketplace refresh = git pull via the same
  helper); SSO authorization persists on the OAuth app, no re-dance.

Caveat for honesty: this run's machine was already SSO-authorized, so the dance's
steps come from the mit-plongeur/sf-latici precedent, not a fresh stopwatch. The
new datum is the *zero increment* — Claude never asked for auth of its own.

## What this does NOT answer (still bds-halonu's remit)

- What **individual claude.ai / Desktop accounts** can consume without an Anthropic
  org (MIT has none — the Directory route doesn't exist for the team case).
- GUI-only teammates: the CC path proven here serves the terminal half of the team;
  the other half needs the claude.ai-side answer.
- Windows/Mac specifics of the gh dance (same steps, different installers).

## Repo status

CREATED ≠ LAUNCHED: `ITV/mit-commons` stays private and unannounced until seeded
(Alex's Region Lift skill, exemplar CLI + MCP, the Claude-audience maintenance
skill). Structure stays provisional while it's one skill deep. Local clone on tube:
`~/repos/itv/mit-commons`.
