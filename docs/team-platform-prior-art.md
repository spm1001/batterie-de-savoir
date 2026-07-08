# Team Platform — Prior Art Survey

Surveyed live: 2026-07-08 (bds-halonu). Method: WebSearch/WebFetch against current docs
(training knowledge treated as stale by construction), claude-code-guide agent for the
Anthropic surface, parallel research agents for the analogue ecosystems, estate sweep
for internal prior art. Companion to `team-platform-requirements.md`,
`team-platform-design-lessons.md`, `team-platform-distribution-spike.md`.
Feeds bds-ronuho (the blueprint).

## 1. Anthropic current state

Surveyed via claude-code-guide agent against live docs, 2026-07-08. Empirical facts we
held going in, checked against current documentation:

- **Private SAML org repo + ambient git auth: CONFIRMED by docs** (bds-nupepe spike
  verified it live first). [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- **Version-gated updates: TRUE when `version` is set — but docs document an escape
  hatch: leave `version` UNSET and update detection keys on the git commit SHA.**
  ("If you're iterating quickly, leave version unset so the git commit SHA is used
  instead.") If real, merge=shipped needs NO CI auto-stamp at all — the class-deletion
  goes one level deeper than bds-pozubo concluded. **Spike result below (§1a).**
- **Org Directory private/internal-only: CONFIRMED unchanged.** Also: a public
  marketplace repo referencing private plugin repos is NOT supported
  ([#61271](https://github.com/anthropics/claude-code/issues/61271)) — external
  sources must be public, or plugins vendored in-repo with `./` sources. (Family
  estate concern only; MIT has no Anthropic org.)

### 1a. SPIKE (2026-07-08, live on ITV/mit-commons): the escape hatch is REAL

Two probes, run the moment the docs claim surfaced (spike-before-design):

- **Probe A** — removed the `version` field from plugin.json entirely + a sentinel
  content change; `claude plugin update` reported *"updated from 0.0.2 to
  29d1effea291"* — the installed cache dir is now **SHA-named**, installed_plugins.json
  records the short SHA as the version, sentinel content arrived.
- **Probe B (decisive)** — a second content-only commit, no version anywhere in the
  repo: *"updated from 29d1effea291 to 6ded718f3b71"*, new sentinel verified in the
  new cache dir. **SHA→SHA propagation on pure content change.**

**Consequence: merge = shipped needs NO CI auto-stamp.** The bds-pozubo conclusion
("a bump is necessary and sufficient") was true *of a versioned plugin*; the deeper
class-deletion is to not have a version at all. Version ceremony doesn't move to
machinery — it ceases to exist. Trade-offs, honestly: every commit (docs-only
included) becomes an update; the human-legible version number is gone — but "what am
I on?" gets a *better* answer (the SHA names the exact content, directly comparable
to repo HEAD — the "us or them?" diagnostic from design-lessons Family 5 improves).
mit-commons now runs unversioned; its README warns against re-adding the field.

### Plugin spec (July 2026)

- `plugin.json`: `name`, `description`, `version`, `author`; `defaultEnabled: false`
  (May 2026) ships a plugin disabled pending user opt-in. Unrecognized top-level
  fields are ignored; no breaking schema changes in 2026.
  [Reference](https://code.claude.com/docs/en/plugins-reference)
- Directories: `skills/` (preferred; `commands/` legacy still works), `agents/`,
  `hooks/hooks.json`, `.mcp.json` for bundled MCP servers.
- `claude plugin init <name>` scaffolds the structure (May 2026). The browse pane now
  shows projected **context cost** and full contents (commands/agents/skills/hooks/
  MCP) before install ([w21](https://code.claude.com/docs/en/whats-new/2026-w21),
  [w22](https://code.claude.com/docs/en/whats-new/2026-w22)).
- Marketplace rename maps sync to user settings automatically (June 2026).

### Marketplace mechanics

- Install cache: `~/.claude/plugins/cache/<owner>/<name>/<version>/` — version-keyed;
  orphaned versions auto-removed after 7 days. Update detection compares installed
  version vs the marketplace's declared version.
- Known wrinkle: directory-source (local-path) marketplaces can serve a stale
  marketplace.json indefinitely ([#72616](https://github.com/anthropics/claude-code/issues/72616)).
- No announced move to content-based detection as the default; the unset-version SHA
  path is documented as an iteration convenience, not a strategy.

### Team distribution WITHOUT an org — the surface matrix (the key question)

| Surface | Private-repo marketplace? | Notes |
|---|---|---|
| Claude Code CLI | **YES** | Ambient git credential helper; proven on ITV/mit-commons (bds-nupepe) |
| Claude Desktop (personal tab) | **NO** | "Add marketplace by URL" not shipped — open request [#66184](https://github.com/anthropics/claude-code/issues/66184). Workaround: clone locally + hand-register in `known_marketplaces.json`. Can browse Anthropic's official/add-on marketplaces; can **upload a plugin file directly** |
| Cowork | **NO** | Server-side sync uses an internal git library that ignores credential helpers — private repos fail ([#17201](https://github.com/anthropics/claude-code/issues/17201)); Cowork Directory is org-only |
| claude.ai web | docs silent | No documented plugin upload or marketplace-add on the web surface |

Pro vs Max: identical plugin capabilities, different usage headroom.

**Design consequence for mit-commons:** the requirements' "genuine parity" between the
terminal half and the GUI half cannot come from marketplace machinery today. The
marketplace serves the CLI half; the GUI half needs a different vehicle (plugin-file
handout, local-path registration, or waiting on #66184) — or the parity requirement is
met at the *content* level (skills as portable prose) rather than the *pipe* level.
This needs its own spike before the blueprint promises any GUI surface (design-lessons
Family 5: verify each promised surface empirically).

### Roadmap signals

- `anthropics/claude-plugins-official` launched May 2026 — curated (~45 plugins),
  no public application process.
- Cowork managed plugins (Feb 2026) are **Enterprise-only**; expanded Cowork rolling
  to Max users July 2026.
- **No small-group/team distribution pathway announced.** The gap between "individual
  with CLI" and "Enterprise org" is real and unfilled — mit-commons lives exactly in
  that gap.

## 2. Gemini Spark (watch item)

**Status 2026-07-08: launched but immature; no plugin format to target — the
extensibility story is MCP.** Spark was unveiled at Google I/O 2026 (2026-05-19) as a
24/7 agentic assistant on dedicated Google Cloud VMs (Gemini 3.5 Flash + Antigravity
2.0), with full MCP support; custom MCP connections are rolling out, alongside
first-party connected apps (Canva, Dropbox, Instacart, OpenTable, Zillow). Access is
still trusted-testers / AI Ultra (US) / select business users; macOS app landed June
2026.

**Verdict: remains a watch item, and the requirements record's call stands** — the
convergence seam is MCP, which the estate already speaks (an MCP server built for
Claude Code reportedly works with Spark unmodified). No Spark adapter until it ships
generally AND a teammate asks. Content-first skills (portable prose) keep the door
open for free.

Sources:
- [TechCrunch: Google introduces Gemini Spark at I/O 2026](https://techcrunch.com/2026/05/19/google-introduces-gemini-spark-a-24-7-agentic-assistant-with-gmail-integration/)
- [Google blog: Gemini Spark updates — macOS launch, connected apps (June 2026)](https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-june-2026/)
- [Gemini Spark overview](https://gemini.google/overview/agent/spark/)

## 3. Analogue survey

Six ecosystems, each mapped to: ownership unit / versioning grain / contribution gate
/ drift guard / update propagation / failure stories. All claims verified against
live 2026 documentation by research agents (2026-07-08); full agent reports carry
per-claim citations — the most load-bearing are kept inline here.

### Homebrew taps (third-party)

- **Ownership:** the tap = a whole git repo, owned by its repo owner; formula files
  are the sub-unit. Anyone can create one (`brew tap-new` scaffolds CI).
- **Versioning:** per-formula, derived from the download URL + pinned `sha256`.
  **The `revision` field exists precisely for content-changed-but-version-didn't**
  (forced reinstall without an upstream bump) — Homebrew's answer to our pozubo
  problem, needed only because formulae carry versions at all.
- **Gate:** third-party taps have NONE (push = shipped); homebrew-core has
  BrewTestBot CI + human review + notability thresholds ("maintain your own tap"
  is the documented escape valve).
- **Drift guards:** install-time checksums; formal `deprecate!` → `disable!` →
  auto-remove-after-1-year lifecycle; **analytics-driven abandonment** (zero installs
  in 90 days per formulae.brew.sh/analytics); **NEW June 2026: `brew trust`** — 6.0.0
  requires explicit trust of non-official taps before their Ruby loads
  ([Tap Trust](https://docs.brew.sh/Tap-Trust)), the systemic answer to tap
  hijack/ownership-transfer.
- **Updates:** transport is commit-based (git pull of every tap, auto-piggybacked
  ~daily), detection is version-gated (`brew outdated` compares versions), upgrade is
  always user-initiated; `brew pin` opts out per-package.
- **Failures:** 2018 Jenkins token leak (response: branch protection, org 2FA — GPG
  signing proposed and *rejected*); **2021 review-cask-pr RCE — the automated
  version-bump-only merge gate was fooled by a diff-parser flaw; response: bots
  stripped of commit rights, ALL cask PRs now human-reviewed**
  ([disclosure](https://brew.sh/2021/04/21/security-incident-disclosure/)).

### Oh My Zsh (in-tree, the nearest mit-commons relative)

- **Ownership:** in-tree plugin directory in the single repo; the maintainer team
  owns everything; authors informally CC'd. 357 plugins live. The `custom/` dir is
  the local override/escape hatch (same-name custom plugin shadows the in-tree one).
- **Versioning:** **NONE — zero tags, zero releases (verified live via API).** Merge
  to master IS the release. "Forgot to bump" is impossible by construction. **The
  documented cost: security-fix communication degrades to dates** — the 2026 dotenv
  advisory could only say "update to a version released after 2026-05-28"
  ([GHSA-3rgh-p3mg-rjqg](https://github.com/ohmyzsh/ohmyzsh/security/advisories/GHSA-3rgh-p3mg-rjqg)).
- **Gate:** PR review by a small volunteer team; extensive changes must find their
  own +1 testers; **new themes refused outright** (moratorium as surface-area cap);
  alias criteria published; AI-disclosure policy (~2025). Live backlog: 423 open PRs.
- **Drift guards:** whole-tree `zsh -n` syntax CI on every PR (a plugin can't become
  unparseable); deprecation-by-shim ad hoc; otherwise thin — an abandoned in-tree
  plugin still "updates" with the framework, invisibly.
- **Updates:** whole-framework git pull, **user-prompted every 2 weeks by default**
  (auto/reminder/disabled modes); commit-based detection; all-or-nothing granularity.
  **The project REMOVED `omz update --unattended` — "it has side effects"** — even
  the versionless ecosystem found fully-silent self-update too sharp.
- **Failures:** CVE-2026-50187 (dotenv ACE on `cd`, fixed 2026-05-28) — in-tree
  distribution shipped the fix to everyone's next update with zero coordination, but
  versionlessness muddied the advisory; chronic review starvation answered by
  *governance* (moratoria, criteria), not tooling.

### VS Code extensions (the registry counter-model)

- **Ownership:** extension = `publisher.name`, publisher account is the identity;
  IDs immutable; registry enforces namespace protection against typosquatting
  official publishers. (Open VSX: namespaces claimable via public GitHub issue;
  unowned → "unverified" badge.)
- **Versioning:** per-extension SemVer in package.json; registry rejects re-publish
  of an existing version — the registry, not git, is the source of truth.
- **Gate:** no human pre-review; registry-side automation on every publish: malware
  scan (multiple engines), sandboxed dynamic analysis, secret scanning,
  **registry signing verified at install**. Human review only for the
  verified-publisher badge (domain proof + 6 months standing).
- **Drift guards:** **kill switch** (verified-malicious extensions auto-uninstalled
  from clients — strongest post-hoc guard of the six); usage-anomaly monitoring;
  publisher-trust dialog on first third-party install; `@deprecated` filter.
- **Updates:** auto-update by default, version-gated against the registry, **with a
  default 2-hour `autoUpdateDelay` between publish and fleet rollout** (added after
  the 2025 malware waves — a damper window for monitoring to catch a bad release).
  Sideloaded VSIX = auto-update disabled (frozen).
- **Failures:** Open VSX publish-extensions token exposure 2025 (registry-wide
  takeover primitive — the auto-publish workflow ran untrusted `npm install` with a
  super-token in env); GlassWorm (self-propagating extension worm, invisible-Unicode
  payloads, ~35.8k installs, recurred into 2026); Material Theme false-positive
  (9M-install extension removed then reinstated with apology) — the mechanism trail
  (signing, secret scan, trust dialog, update delay) is legible incident-by-incident.

### Obsidian community plugins (+ BRAT)

- **Ownership:** one GitHub repo = one plugin + one entry in the central registry;
  ids unique; **forks banned** unless the author approves or is unreachable 6+ months
  (anti-hijack doubling as an abandonment escape hatch).
- **Versioning:** per-plugin semver in manifest.json; release tag must match exactly.
  **"Forgot to bump" = the update silently never propagates** (the manifest version
  IS the entire update signal) — the pozubo shape as a whole ecosystem's daily lived
  cost. Bump-without-release = uninstallable.
- **Gate — the instructive transition (2026-05-12):** the original model (human
  review of initial submission, then unreviewed self-service releases) **drowned** —
  2.5–3-month waits, a 2,300-submission queue, coding agents accelerating authorship.
  Replaced by **automated review of every version** (policy adherence, vuln/malware
  scan, minutes not months), with human review retargeted at popular/featured/flagged
  ([blog](https://obsidian.md/blog/future-of-plugins/)). BRAT sideloading bypasses
  the gate entirely (de-facto beta channel via GitHub pre-releases).
- **Drift guards:** policy-based removal of unmaintained plugins; per-plugin safety
  scorecards (2026); the 6-month fork rule.
- **Updates:** pull-on-demand, user-initiated, manifest-version-gated. "For security
  purposes, community plugins don't update automatically." Plugins forbidden from
  self-updating.
- **Failures:** the review-queue collapse (above); PHANTOMPULSE (April 2026) — a RAT
  delivered not via registry compromise but via **legitimate powerful plugins +
  vault-sync** as the attack surface ([Elastic](https://www.elastic.co/security-labs/phantom-in-the-vault)).

### Debian vs nixpkgs (two maintainer models)

- **Ownership:** Debian — the source package with a named exclusive Maintainer
  (taking one without assent "would be package hijacking"); whole orphan/RFA/salvage/
  MIA apparatus exists to transfer it safely (1,059 orphaned packages today).
  nixpkgs — a derivation file in the monorepo with deliberately **non-exclusive**
  maintainership: "the maintainer doesn't have exclusive control over the packages
  they maintain… one reason why we scale." (Also: nixpkgs no longer uses GitHub
  CODEOWNERS — a custom `ci/OWNERS` routes review for *infrastructure paths*, while
  `meta.maintainers` covers packages: two parallel ownership systems by kind.)
- **Versioning:** Debian — per-package, and **the archive refuses an upload whose
  version already exists**: a versionless change structurally cannot ship. nixpkgs —
  the consumable unit is a *monorepo commit*; the **r-ryantm bot bumps versions FOR
  maintainers** (Repology + release APIs → auto-PRs), and a merge-bot lets
  non-committer maintainers self-merge bot bumps.
- **Gate:** Debian vests trust in **people up front** (DD/DM status, sponsorship as
  mentoring, ftpmaster NEW review); nixpkgs vests trust in **the change at merge
  time** (ofborg CI + ~200 committers + one-week maintainer-feedback etiquette).
- **Drift guards:** Debian — heavyweight social machinery (orphan → QA uploads →
  21-day salvage window). nixpkgs — bots and campaigns (r-ryantm; zh.fail groups
  build failures *by maintainer*; Zero Hydra Failures drives ~8k failing builds down
  before each release; inactive maintainers removed after ~3 months, one-week
  objection window).
- **Updates:** Debian — pull-based apt against release trains. nixpkgs — **channel
  advance is CI-gated: "Hydra… updating the official channels when their jobs
  succeed" — propagation simply does not move past a broken commit.**
- **Failures:** **xz backdoor (CVE-2024-3094)** — 2.5 years of sock-puppet-assisted
  trust-building on a burned-out solo maintainer; the unit of compromise was a
  trusted *person*, not an unreviewed change; hit both ecosystems via release
  tarballs ≠ git. Debian NEW-queue delays (11-month stalls → the ftpmaster team was
  dissolved/split in Oct 2025; queue now healthy). nixpkgs review-capacity rot
  (11,838 open PRs live today; the 2022 "not sustainable" thread's problem statement
  still broadly true — merge-bot, OWNERS routing, and ZHF are mitigations, not a fix).

### Backstage golden paths (the social model)

- **Ownership:** a Template entity (`template.yaml` + skeleton) with a `spec.owner`
  team, ingested from an ordinary repo the platform team curates — no tool-level
  gate; ordinary git review is the gate.
- **Versioning:** **templates have no version at all** — the catalog serves HEAD
  with refresh lag ("forgot to bump" inverts into *stale serving until refresh*).
  Instantiated projects carry no link to the template version that produced them.
- **Drift — the famous gap:** the scaffolder is **one-shot by design**; instantiated
  projects are static copies; OSS Backstage has no re-sync (issue trail 2021→2025,
  still open). What fills it at Spotify: **Soundcheck** (standards as continuously-
  scored checks — drift becomes a visible failing check, not silent divergence) +
  **Fleetshift** (mass automated PRs across thousands of repos; a ~200-day framework
  upgrade cut to <7 days). Create / detect / repair are **three separate tools** —
  and the two that keep things aligned are commercial add-ons; OSS ships only the
  create verb.
- **Failures:** adoption death by under-resourcing — "most teams that thrive on
  Backstage dedicate 3–5 engineers"; a lone engineer serving 130 users spent all
  bandwidth keeping catalog data accurate. The discriminating success factor, per
  Backstage's own blog: **"approach it like you're building a product."** Spotify
  also documented a governance failure: dropping dedicated tech-writers for
  distributed tutorial ownership created a coordination gap.

### The comparison table

| | Ownership unit | Version grain | Contribution gate | Drift guard | Update propagation |
|---|---|---|---|---|---|
| **Homebrew taps** | tap = whole repo | per-formula + sha256 (+`revision` for content-w/o-bump) | none (3rd-party) / CI+human (core) | checksums; deprecate→disable→remove; analytics; `brew trust` (2026) | git-pull transport, version-gated detection, user-initiated |
| **Oh My Zsh** | in-tree dir, team owns all | **none — merge IS release** | PR + small team; moratoria; find-your-own-testers | whole-tree syntax CI; governance caps | whole-framework pull, prompted fortnightly |
| **VS Code** | publisher.name, registry identity | per-ext semver, registry rejects re-publish | no human; malware/secret scan + signing per publish | kill switch; anomaly monitoring; trust dialog | auto-update + **2h damper**; sideload=frozen |
| **Obsidian** | repo + registry entry | manifest semver = sole update signal | automated per-version review (since 2026-05); was human, drowned | policy removal; scorecards; 6-mo fork rule | pull-on-demand, version-gated, never auto |
| **Debian / nixpkgs** | package+named owner / derivation+non-exclusive | forced increment / monorepo commit, bot-bumped | trust-in-person up front / trust-in-change at merge | orphan-salvage machinery / bots+campaigns+visibility | apt release trains / **CI-gated channel advance** |
| **Backstage** | template.yaml + owner team | **none — HEAD-served** | ordinary repo review | Soundcheck scorecards + Fleetshift mass-repair (commercial) | one-shot scaffold; no push channel |

### Cross-cutting observations (all six)

1. **Every human pre-publication gate documented here eventually drowned** — Obsidian
   (2,300-queue collapse → automated review, May 2026), Debian NEW (11-month stalls →
   team dissolved/split, Oct 2025), OMZ (423 open PRs → moratoria + AI-disclosure
   policy). The 2025–26 convergent answer: **automate the check, retarget humans at
   exceptions** (popular/flagged/core).
2. **And yet: every ecosystem that gave automation *authority* got burned at exactly
   that point** — Homebrew's auto-approving review-cask-pr (2021 RCE → all cask PRs
   human-reviewed again), Open VSX's auto-publish super-token (2025 registry-wide
   takeover). The synthesis is precise: **automation may check; it must not hold
   publish authority or bypass credentials.**
3. **Where the version signal lives differs in kind, and each location has a
   documented cost:** author-remembered (Obsidian's silent no-ship; Homebrew needed
   `revision` to patch content-w/o-bump) · forced-by-registry (Debian, VS Code) ·
   bot-carried (nixpkgs) · absent (OMZ — advisories degrade to dates; Backstage —
   stale HEAD-serving). Nobody has author-remembered versioning *without*
   compensating machinery.
4. **Update-propagation dampers appeared independently twice** (VS Code's 2-hour
   delay, OMZ removing `--unattended`) — instant silent fleet-wide propagation
   proved too sharp under opposite threat models. Pull-on-demand ecosystems
   (Obsidian, Homebrew, CC plugins) get the damper structurally.
5. **Drift guards divide into four mechanism families:** social-transfer machinery
   (Debian), bot-pressure + visibility (nixpkgs), policy + scorecards (Obsidian,
   VS Code), measure-then-mass-repair (Backstage). Pick per failure mode, not per
   ecosystem.
6. **The xz caution applies to every maintainer model:** the unit of compromise was
   a trusted *person* (and solo-maintainer burnout was the vulnerability). Gates
   protect against bad changes, not compromised or exhausted maintainers.
7. **The platform-as-product law** (Backstage): internal platforms die of
   under-resourcing, not bad design — and distributed content ownership without a
   coordinating owner creates gaps even at Spotify scale.

## 4. Internal prior art

**Found.** The remembered research is a May–June 2026 cluster centred on **`mit-tools`
— a repo that was researched but never created** (that's the "didn't fruit"), plus its
built-but-stalled walking skeleton **`piano`**. Ranked by relevance:

1. **`~/notes/raw/mit-tools-research-brief.md`** (~2026-06-04) — "Research brief —
   multi-agent tool packaging & distribution": one source of truth serving Claude,
   OpenAI Codex, AND Google Gemini. Names batterie's "Claude-only" pain point. The
   repo it was for was never created.
2. **`~/repos/spm1001/piano/`** (2026-05-31; `.bon/understanding.md`,
   `docs/build-plan.md`) — the implementation attempt: "one tool that installs once
   and appears in Claude, Codex, and Antigravity." Carries the full **surface
   capability matrix** (skills dirs per vendor; MCP everywhere; remote-HTTP as the
   only path to claude.ai chat), the named "VENDOR DRIFT" enemy, and
   flatten-vs-symlink-vs-submodule analysis. Built to Stage 0/1, stalled. (The
   `piano` *service* now running on tube is the ping MCP — same repo, the part that
   survived.)
3. **`~/notes/raw/2026-05-31-cross-agent-skeleton-build-plan.md`** — the canonical
   standalone write-up: cross-agent install matrix, per-vendor update mechanics,
   org-marketplace rules as of May 2026.
4. **`~/notes/raw/2026-06-01-piano-marketplace-reframe.md`** — the reframe to "emit a
   marketplace dialect per agent"; verified June-2026 vendor landscape (Codex's
   `.codex-plugin/plugin.json` near-isomorphic to Claude's; Gemini deferred — Spark
   has no paste-a-repo-URL marketplace, consistent with §2's July finding).
5. **`~/repos/spm1001/cornichon/docs/sharing.md`** (2026-05-16) — the earliest
   team-distribution pipeline design (Google Doc → Drive Approvals → GitHub → Cowork
   sync → Desktop marketplace), single-vendor precursor.

Partial: `~/notes/raw/atelier-loose/coordination-research-brief.md` (key line: "skills
don't sync across Claude surfaces — claude.ai, API, and Claude Code each have separate
skill stores"); `~/notes/raw/2026-05-31-mise-update-bug-vendor-drift.md` (the origin
trigger, closing "Parked for the mit-tools / cross-agent repo design"). The
half-remembered "bestiary" teardown is real but off-tube (hezza/Mac) and is a
*substrate* teardown (SDK/agent internals), not distribution.

**What the cluster teaches the blueprint (vs re-deriving):** the cross-agent ambition
is why mit-tools never shipped — it front-loaded a three-vendor abstraction before one
vendor's path was proven. mit-commons inverts that: one vendor proven live first
(§1), portability held as a *constraint* (content-first skills, MCP seams — exactly
the requirements record's Gemini demotion), not as day-one machinery. The piano
surface matrix remains the best map of WHERE content must land per vendor if/when the
door reopens.

## 5. Steal-list, ranked by fit

Ranking = size of failure class prevented × cheapness at our scale (8 people, one
private repo, merge=shipped, SHA-keyed updates). Each entry names the scar or
requirement it serves — scars from `team-platform-design-lessons.md` (Families 1–6),
requirements from `team-platform-requirements.md`.

1. **Propagation gated on green** (nixpkgs: channels advance only when CI succeeds).
   Branch-protect `main`; the whole-tree lint must pass before merge. In
   marketplace-is-the-repo, HEAD *is* the fleet — this is the only thing standing
   between a broken merge and every installed Claude. **Prevents:** the husk class
   (Family 1) re-emerging at the new topology; OMZ's
   unparseable-plugin-ships-anyway class. Note this diverges from batterie's own
   no-branch-protection choice — right for a single operator, wrong for eight; the
   requirements' "approve button" owner experience implies PR flow anyway.
2. **Whole-tree lint on every PR** (OMZ's `zsh -n` across 357 plugins — proven at
   scale far past ours). Ours checks: SKILL.md frontmatter validity, dirname = name,
   description length vs platform caps, generated tables fresh. **Prevents:** Family
   4 (doc drift — this IS "generate from the substrate", enforced), the bds-kusodu
   silent-truncation class, and it's the check that #1 gates on.
3. **Automate the review, humanize the exception** (Obsidian's May-2026 pivot;
   negatively proven three times — Obsidian queue, Debian NEW, OMZ backlog: **every
   human pre-publication gate drowned**). The hybrid gate is validated as designed:
   automated checks on everything, CODEOWNERS humans on the protected core only,
   the Fable sweep as the continuous reviewer of the rest. **Prevents:** Family 3's
   17-day-unmerged-PR class (a human gate on a recurring path WILL rot) — without
   giving up review where it counts.
4. **Automation checks; it never holds publish authority** (Homebrew 2021 +
   Open VSX 2025: both burned exactly at the automated gate that could approve or
   publish). For us: no auto-approve bot, no CI credential with rights beyond the
   repo itself, deadman pings as the only outbound. Marketplace-is-the-repo already
   deletes the publish credential — **keep it deleted.** **Prevents:** Family 3
   (release tooling as its own hazard) recurring in CI clothing; the xz-shaped
   super-credential.
5. **The commons takes graduates, not experiments** (OMZ's moratorium + `custom/`
   escape-hatch pair; Obsidian's registry-vs-BRAT split). Personal `~/.claude/skills`
   is the sandbox/beta channel; the commons curates what proved out. Caps the
   surface eight people must keep alive — the governance answer to contribution
   pressure, which every ecosystem eventually reached for. **Serves:** "seeded,
   never empty" with exemplars (requirements); prevents the backlog-hygiene-debt
   class at social scale.
6. **Drift as a visible failing check, not silent divergence** (Soundcheck). The
   Fable sweep emits a scorecard — a generated table in the repo: per skill, lint
   status, last-touched, owner, last sweep verdict. Homebrew's analytics-driven
   deprecation is the same move (visibility → lifecycle decisions). **Serves:**
   Family 5 (platform-owned failures need a glanceable "us or them?" surface);
   platform-as-product without platform-team headcount.
7. **Ownership transfer as a one-liner, not machinery** (Debian's 21-day salvage
   window / Obsidian's 6-month fork rule / nixpkgs' 3-month inactive removal —
   three scales of the same policy). One sentence in the repo docs: "core-skill
   owner unresponsive ~a month → the sweep may propose reassignment."
   **Prevents:** the abandoned-core-skill wedge without importing Debian's
   apparatus. (xz corollary: solo-owner burnout is itself the vulnerability —
   non-exclusive nixpkgs-style ownership for everything outside the core.)
8. **Exemplar copies drift — budget for it** (Backstage's one-shot scaffolder, the
   2021→2025 open wound; create/detect/repair are three different verbs). When a
   teammate copies the exemplar skill and the pattern later improves, their copy is
   a static snapshot. At our scale the Fable sweep can do Fleetshift-lite (propose
   PRs applying pattern updates across skills) — **don't build it until it hurts,
   but don't be surprised** (spike-before-design applies to remedies too).
9. **Keep pull-on-demand; never add auto-update** (VS Code's 2-hour damper and
   OMZ's removal of `--unattended` both re-invented the damper we get free; Obsidian
   forbids self-updating plugins outright, "for security purposes"). CC plugin
   updates are user/session-initiated — that structural damper plus SHA-instant
   *availability* is the right pair. **Prevents:** fleet-wide blast of a bad merge
   (bounds Family 1's successor risk at the propagation layer).
10. **Unversioned SHA-keying is the right side of the taxonomy** (observation 3:
    author-remembered versioning always grew compensating machinery — Homebrew's
    `revision`, Obsidian's silent no-ship; versionless's one real cost, date-based
    advisories, is answered by SHAs naming exact content). Confirms §1a's choice
    with six ecosystems of evidence. **Deletes:** Family 2 whole.

**Not stolen, deliberately:** central-registry machinery (VS Code/Obsidian — wrong
scale, and the repo already is the registry); Debian's trust-in-person
onboarding (ITV employment + repo access is our identity layer); malware
scanning (private repo, known eight); BRAT-style beta channels (personal repos
serve this); Backstage's catalog (a flat `skills/` dir needs no catalog).
