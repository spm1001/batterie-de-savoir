# Team Platform — Requirements Record

Interview: 2026-07-08, Sameer × Claude (session 86d7aadc, bds-cagapa).
Status: draft pending Sameer's confirmation. Feeds bds-ronuho (blueprint synthesis).

## Who

- **MIT core, 8 people day one**; friends/adjacent ITV folk later.
- Skill spread: **half and half** terminal-capable vs GUI/web-only → Claude Code and the
  GUI surfaces are both first-class; the kit needs genuine parity, not a power-user tier.

## What ships day one (content inventory)

- **Not a batterie migration.** Batterie keeps serving the generic tools (mise, consommé
  etc.) as today. The team repo is for **team-authored content**.
- **Seeded, never empty** ("the wind will whistle through it"): one or two Skills, one CLI,
  one MCP server — chosen as *pattern exemplars* that role-model the shapes for others.
- **Recruit Alex's Region Lift skill as founding content** — a first skill authored by a
  teammate makes the repo "ours" on day one structurally, not rhetorically.
- **Structure: flat `skills/`, zero hierarchy** until the list outgrows it (~15+ entries),
  then at most one layer, derived from what accumulated (`~/notes/work` shape as reference).

## Surfaces

- **Day one, tested not theorised:** Claude Code (CLI) · Claude Desktop/Cowork · claude.ai
  web + mobile.
- **Gemini: demoted from day-one surface to portability constraint** (agreed in interview —
  team is Gemini-allergic day-to-day; Google models are used heavily wrapped inside apps
  like Plongeur; occasional Gems are for other audiences). Content-first design keeps
  skills as portable prose and MCP as the standard seam, so the door stays open free.
  **Watch item: Gemini Spark** (Google's web-first Desktop-equivalent) — build that adapter
  when it ships and a teammate asks, not before. Prior-art action (bds-halonu) tracks it.

## Ownership & contribution

- **Hybrid gate:** CODEOWNERS on load-bearing core skills; open edges anyone can edit;
  a scheduled Fable review sweeps everything.
- The owner experience is a **GitHub notification + approve button** — no local git, no
  ceremony. (Judi approves changes to her skill from her phone.)
- Team picks the repo's name and identity — deliberately not the founder's aesthetic.

## Support model ("the 4pm question")

- Teammates **ask their own Claude** — nobody debugs alone, and the support surface is
  the Claude they already have open.
- Therefore the kit ships a **maintenance skill authored for Claude-as-audience**:
  self-diagnosis steps, plain-English explanation for the human, and surface-awareness —
  "to fix this I need hands; let's open Claude Code" when the current surface can't act.
- **Load-bearing design principle (Sameer's words): equal access for Claudes and humans —
  "this is as much for you as for us."** Every part of the platform (docs, board, checks,
  contribution flow) must be legible and operable by both kinds of reader.

## Defaults assumed unless corrected

- **Cadence: continuous** — merge = shipped (marketplace-is-the-repo topology makes
  releases an anti-concept; the Fable sweep is the periodic quality pass).
- Each person authenticates with their **own ITV Google identity** for Workspace-touching
  tools (the mise pattern), no shared credentials.

## Open forks (not yet decided)

1. **Repo home:** ITV GitHub org (governance-right, but SAML/SSO friction for every
   machine and possibly for marketplace/Directory plumbing) vs `spm1001` private
   (frictionless, wrong-shaped governance for a team asset). Verify the Teams Directory
   private-repo rule's current form (bds-halonu) before deciding.
2. **Naming process:** team chooses — mechanism TBD (a poll? a christening over tea?).
