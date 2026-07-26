# MIT Commons — The Blueprint

Drafted: 2026-07-09 (bds-ronuho). Status: **ENDORSED — Sameer, 2026-07-26** (estate
review), with three implementation riders: (1) build the whole-tree lint **before**
flipping branch protection — a required check that doesn't exist blocks every merge;
(2) the end of direct push binds Sameer too, accepted knowingly — his estate-wide
"push freely to main" gets a carve-out for this repo; (3) §7's seed inventory is a
period piece (nine `mit-*` skills ship today) and the §10 proof-of-flow spike is
still owed — clean-room landed 2026-07-17 as a direct commit, outside the flow, so
CODEOWNERS paths must use the live `mit-*` directory names and one real PR must run
the gate end-to-end. Implementation tracked under `mc-zotoze`.
Synthesizes: `team-platform-requirements.md` (who/what/surfaces),
`team-platform-design-lessons.md` (batterie's scars → class-deletions),
`team-platform-prior-art.md` (Anthropic state + six-ecosystem survey + steal-list),
`team-platform-distribution-spike.md` (the proven CC path). On endorsement this
document lands in `ITV/mit-commons` as its founding design record; scaffolding
decisions trace back here.

This is a decision record, not a menu. Each section states the decision, the
alternatives costed, the evidence, and — where deferred — the revisit trigger.
Written for both kinds of reader: teammates and their Claudes ("this is as much
for you as for us").

---

## 1. Topology — the marketplace IS the repo

**DECIDED: one repo, `ITV/mit-commons`, which is simultaneously the marketplace,
the plugin, and the content.** `.claude-plugin/` carries both manifests, plugin
`source: "./"`, flat `skills/` at top level, zero hierarchy until ~15+ skills.

**Alternative costed — multi-repo + assembler (batterie's shape):** rejected.
Batterie needs its assembler because it federates five source repos and a
credential-flavour transform; the commons is team-authored content in one place.
The assembler's copy step is what bought batterie its four vendoring incident
classes (copy-list omissions, parity drift, working-tree leaks, husk publishes)
and the guards to catch them — **no copy step, no class** (design-lessons
Family 1). Proven live: install + skill invocation on tube, zero Claude-specific
auth (distribution spike).

Blast radius shrinks with it: one repo means no bus for a laggard to wedge, no
cross-repo consumer archaeology, one understanding surface (design-lessons #3).

## 2. Versioning — none. SHA-keyed, by construction

**DECIDED: no `version` field in plugin.json, ever.** Update detection keys on
the git commit SHA; merge = shipped; "what am I on?" is answered by a SHA
directly comparable to repo HEAD (the "us or them?" diagnostic in one glance).

**Alternatives costed:**
- *Author-remembered semver* (Obsidian's model): "forgot to bump" = update
  silently never propagates — a whole ecosystem's daily lived cost, and
  batterie's own repeat scar (three ratchet catches, one 4-day bus wedge).
- *CI auto-stamp* (the bds-pozubo remedy): superseded same day — version
  ceremony doesn't move to machinery, it ceases to exist (bds-halonu §1a,
  two live SHA→SHA probes).
- The six-ecosystem taxonomy confirms the grain: nobody has author-remembered
  versioning without compensating machinery (Homebrew grew `revision`; Debian's
  registry force-increments). Versionless's one real cost — security advisories
  degrade to dates (Oh My Zsh's documented wound) — is answered better than OMZ
  answers it: the SHA names exact content.

**Guard (standing):** the README warns against re-adding the field. A
well-meaning "let's version this properly" PR is the likeliest regression;
the whole-tree lint (§3) should reject a `version` key in plugin.json.

**Guard (standing):** `latest` remains the ONLY GitHub Release. `releases/latest`
means "newest release" — any future versioned release silently hijacks the
stable download URL teammates' frozen copies point at (bds-loludi).

## 3. Contribution flow — protected core, open edges, gate on green

This is the fork bds-loludi deliberately left open. **DECIDED as follows:**

- **Branch protection ON `main`**: all changes land by PR; a required whole-tree
  lint check must be green to merge. Direct push ends — including Sameer's.
  This diverges from batterie's own no-protection choice deliberately: right for
  a single operator, wrong for eight (steal-list #1). In marketplace-is-the-repo,
  HEAD is the fleet — the lint gate is the only thing between a broken merge and
  every installed Claude (nixpkgs: propagation never advances past a red commit).
  Live evidence from launch night: the README concurrent-edit race (Sameer's web
  edit vs a session's push) — PR flow makes that race structurally impossible.
- **The whole-tree lint** (to build, cheap): SKILL.md frontmatter valid, dirname
  = frontmatter name, description lengths vs platform caps, marketplace.json ↔
  plugin dir ↔ skills consistency (the manifest invariant, reborn at the new
  topology), no `version` field, generated tables fresh. OMZ proves the pattern
  at 357 plugins; ours is an afternoon.
- **CODEOWNERS on the protected core only**: `.claude-plugin/`, `.github/`,
  `docs/blueprint.md`, `skills/self-help/`, and any skill whose author claims
  ownership (Judi's skill → Judi). Branch protection is set to *require review
  from Code Owners* with required-approvals otherwise 0: a PR touching owned
  paths waits for the owner's phone-button approve; a PR touching only open
  edges merges on green lint alone. That is the requirements' hybrid gate,
  expressed in stock GitHub mechanics — no bots, no custom machinery.
- **Humans hold merge authority; automation and Claudes check and propose.**
  No auto-approve bot, no CI credential with rights beyond the repo, deadman
  pings as the only outbound (steal-list #4: every ecosystem that gave
  automation publish authority was burned at exactly that point — Homebrew
  2021, Open VSX 2025). Teammates' Claudes author PRs freely; a human presses
  merge.
- **Why no human review on the open edges:** every human pre-publication gate
  in the survey drowned (Obsidian's 2,300 queue, Debian NEW's 11-month stalls,
  OMZ's 423 open PRs). Automate the check, retarget humans at exceptions —
  the Fable sweep (§6) is the continuous reviewer of the unprotected surface.

**Owner experience (requirement, preserved):** a GitHub notification and an
approve button. No local git, no ceremony.

## 4. Distribution — per surface, tested not theorised

Mostly decided pre-blueprint; recorded here as the standing shape:

| Surface | Day-one path | Status |
|---|---|---|
| Claude Code CLI | `claude plugin marketplace add ITV/mit-commons` — live updates via ambient git creds | **PROVEN** (spike, zero Claude-side auth; cost = "can you clone a private ITV repo?") |
| Claude Desktop | **Upload plugin** (`mit-commons.zip` from the rolling `latest` Release) — frozen copy, re-upload to refresh | **PROVEN** (live test 2026-07-08) |
| Cowork | Runs the account's uploaded/installed skills; its sandbox `claude` CLI is blind to host plugins — skills must be surface-aware | **PROVEN** (both facts live-verified) |
| claude.ai web | Covered by the same upload — uploads are ACCOUNT-scoped (one upload serves Desktop + Cowork + web) | Visible: proven. *Invocation in a web chat: unverified — spike below* |
| Gemini/Spark | Not a surface. Portability held as constraint (content-first prose, MCP seams), not machinery | Watch item (prior-art §2; mit-tools died front-loading this) |

- **DECIDED (2026-07-08, stands): stay on `ITV/mit-commons`.** The spm1001
  bridge dodges the GitHub-App gate but makes the commons structurally Sameer's;
  revisit only if GUI-live proves a day-one dealbreaker.
- **GUI-live parity unlock:** the ITV Claude-GitHub-App approval (applied for,
  single repo, unlikely). If granted, Desktop marketplace-add switches on with
  zero repo move.
- **Frozen copies self-identify and self-point:** `build-info.txt` (export-subst)
  names the commit; manifest description/homepage carry the latest-download URL.
  The update path travels inside the artifact.
- **DEFERRED — public latest-marker** (a tiny public "current SHA" endpoint
  would let sandboxed Claudes auto-compare freshness; today it's a human-relayed
  two-glance). Exposure trade-off (leaks commit timing of an internal tool);
  team call once teammates exist to ask. Not urgent.

## 5. CI guards — batterie's inventory, kept or deleted by design

| Batterie guard | Commons verdict | Why |
|---|---|---|
| Version ratchet + quarantine | **Deleted by design** | No versions to ratchet, no bus to wedge (§2) |
| Parity guard (vendored vs source) | **Deleted by design** | No vendoring (§1) |
| Manifest invariant | **Reborn as lint** | marketplace ↔ plugin ↔ skills consistency, checked on every PR (§3) |
| publish.py machinery | **Deleted by design** | Merge is the release path; a PR stages exactly what was reviewed (Family 3) |
| Generate docs from substrate | **Adopted at birth** | Skill tables in README generated/linted from frontmatter — never author a fact twice (Family 4: manual tables had a 100% observed drift rate) |
| Deadman-on-success | **Kept** — on the release workflow now; on the Fable sweep when scheduled | Failure-notifications structurally can't catch dead schedules (Family 6) |
| Consumer-side verify | **Kept** (already shipped in release.yml) | The check exercises the real download path |
| Claude-audience maintenance skill | **Kept** (self-help, already shipped) | Family 5: platform-owned failures can't be deleted, only met with a first responder |

## 6. The Fable sweep — continuous review of the open edges

**DECIDED in shape, deferred in automation.** The sweep is the reviewer that
makes merge-on-green safe outside the core: a scheduled pass over every skill —
lint status, staleness, register (write for competence, not compliance), pattern
drift against the exemplars — emitting a **scorecard as a generated table** in
the repo (drift as a visible failing check, not silent divergence — Soundcheck's
move at our scale).

- **Day one: run on demand** from a Claude Code session (Sameer's, or any
  teammate's). **Automate on a schedule when content justifies it** (~5+ skills),
  with a deadman ping from day one of automation (Family 6).
- **Ownership transfer as one sentence, not machinery** (steal-list #7): a
  core-skill owner unresponsive for ~a month → the sweep may propose
  reassignment. (xz corollary: solo-owner burnout is itself the vulnerability.)
- Fleetshift-lite (sweep proposes PRs applying pattern improvements across
  copied skills) is anticipated but **not built until it hurts** (Backstage's
  one-shot-scaffolder wound; spike-before-design applies to remedies too).

## 7. Content policy — the commons takes graduates, not experiments

**DECIDED.** Personal `~/.claude/skills/` (and personal repos) are the sandbox
and beta channel; the commons curates what proved out in real use (steal-list
#5 — the moratorium/custom-dir pair, the registry/BRAT split: every ecosystem
converged on capping the curated surface).

**Day-one seeds, each earning a distinct slot:**

| Seed | Slot | Provenance |
|---|---|---|
| `hello` | install proof | shipped |
| `self-help` | the support model ("ask your own Claude"), pattern exemplar for skill anatomy + surface-awareness | shipped, lint 98/100 |
| **`clean-room`** | **first workhorse** — the 5-condition DCR audit + setup runbook; MIT institutional knowledge (Sophus3, BT, the `itv-mit-{partner}-exch` convention) currently invisible in Sameer's personal skills dir | **ported as this blueprint's proof-of-flow: it lands via the §3 contribution flow as the first governed PR** |
| Region Lift | first teammate-authored skill — makes the repo "ours" structurally | recruit from Alex (standing requirement) |

Port discipline (applies to clean-room and every future graduate): snip personal
tendrils (paths into the donor's estate), make script paths plugin-relative, add
surface-awareness (the audit runs where gcloud lives — Claude Code; GUI surfaces
get the knowledge and a "this needs hands" handoff), and **retire the personal
copy on merge** — one source of truth.

**DEFERRED — CLI and MCP exemplars** (the requirements' other two slots): wait
for a real candidate to graduate rather than forcing one. The wind no longer
whistles — four skills is a seeded commons.

## 8. Hooks — deferred, and not timidly

The creative question this blueprint got asked directly: should the commons do
silent session open/close hooking (bon-style orientation)?

**DECIDED: no hooks in the commons until both conditions clear.** Hooks are
arbitrary shell executing on every teammate's machine at session start. That
changes the repo's trust model from *prose you can read* to *code that runs on
you* — a materially higher bar than skills, which execute only when invoked.

1. **Governance first:** the §3 flow must be live and bedded in — hooks raise
   the stakes of exactly the push-access question it governs. (Seven
   push-holders + no branch protection + startup-executing content is a
   supply-chain amplifier batterie never had to price, because batterie has
   one operator.)
2. **Surface spike first:** whether hooks even fire on Desktop-uploaded frozen
   copies or in Cowork is **unverified** — and the internal prior art's one
   lesson is that mit-tools died front-loading machinery before one path was
   proven. No capability claims without a live probe.

Revisit trigger: contribution flow live + the hook-surface spike run + a
concrete need a skill can't serve (orientation currently lives happily in
skill-space: self-help IS the orientation surface, invoked not injected).

## 9. Migration note — batterie

**Nothing migrates.** Batterie keeps serving the generic tools (mise, consommé,
bon…) exactly as today — it keeps its assembler because it genuinely federates
five repos and a credential transform; the commons deletes those classes by
never having the shape that produced them (requirements: "not a batterie
migration"). The two share only lessons: this document is batterie's scar
tissue, exported.

One precedent flows back: clean-room's port defines what *graduation* looks
like (personal estate → commons, tendrils snipped, personal copy retired).
Future candidates (mandoline is the obvious next; consommé's MCP server if the
MCP-exemplar slot ever demands it) follow the same door.

## 10. Spike ledger — assumptions still outrunning evidence

Per the meta-lesson (batterie's costliest wrong turns were doc-derived
assumptions; its cheapest wins were spikes), every remaining unknown is named
with its verifying probe:

| Assumption | Spike | Owner/when |
|---|---|---|
| Skills *invoke* (not just appear) in claude.ai web chats | Two-minute test next time Sameer is in a browser | Sameer + any session |
| Hooks fire (or don't) on uploaded/Cowork copies | Add a trivial hook to a scratch upload, observe | Before any §8 revisit |
| Windows gh dance matches the Mac/Linux steps | First Windows teammate onboarding, timed | First real onboarding |
| The §3 GitHub mechanics behave as designed (owners gate owned paths; green-lint merges elsewhere) | The clean-room PR itself — proof-of-flow | This week |

## Vocabulary note

The glossary (bds-mawuvu) lands separately. This document uses Anthropic's
current terms (plugin, marketplace, skill) and the commons' own few (the sweep,
the core, the edges, graduation) — the glossary will map both onto the team's
tongue.
