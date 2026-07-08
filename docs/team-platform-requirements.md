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

## Account & billing reality (constrains distribution)

- **There is no Anthropic Team/org for MIT.** Everyone pays for their own Claude
  (Sameer's Anthropic Team is his family's). Consequence: the org **Directory route does
  not exist for the team case** — claude.ai/Desktop distribution is a per-individual-
  account question, and the family-Directory precedent (bds-niluga) does not transfer.
- **Vertex billing opened to the team 2026-07-07** — team members can run Claude Code on
  ITV's Vertex billing (gcloud setup exists). Strengthens CC as a first-class surface;
  note Vertex sessions have no WebSearch.
- Everyone on the team is on **ITV GitHub**.

## Defaults assumed unless corrected

- **Cadence: continuous** — merge = shipped (marketplace-is-the-repo topology makes
  releases an anti-concept; the Fable sweep is the periodic quality pass).
- Each person authenticates with their **own ITV Google identity** for Workspace-touching
  tools (the mise pattern), no shared credentials.

## Decisions from the interview's final round

1. **Repo home: ITV GitHub org, working assumption** (everyone's already there; there is
   a GitHub Team). Pending: bds-halonu verifies the mechanics — can `claude plugin
   marketplace add` consume a SAML-SSO private org repo (per-person, per-machine token
   authorization — the mit-plongeur dance × 8 people), and what individual claude.ai
   accounts can consume without an org Directory. gh-owners Slack channel is the venue
   for org-side asks (friendly but busy).
2. **Name: choose now, boring-durable over clever** (names bite; old names are hard to
   expunge; avoid the French-kitchen register — that's batterie's, i.e. Sameer's).
   **DECIDED 2026-07-08: `mit-commons`** (Sameer's pick from the shortlist — "ours" is
   in the name, and a commons *is* the governance model: protected core, open edges).
   Runners-up for the record: mit-toolkit, mit-kit, mit-workbench.
