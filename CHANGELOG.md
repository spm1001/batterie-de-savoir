# Changelog

> **This is the canonical CHANGELOG for the whole Batterie de Savoir suite.**
> Since the single-version cutover (suite 1.2.2, 2026-06-28) every published
> plugin ships at the same **suite** version, so there is one changelog, not
> one per plugin. Each entry is a suite release; the note names which
> plugin(s) the release carried. Per-repo `CHANGELOG.md` files still exist in
> each source repo for git browsing, but they are no longer vendored into the
> shipped plugins — every plugin ships a generated stub pointing back here.
>
> Maintained by `/batterie:publish` (engine: `scripts/publish.py`), which
> prepends an entry at each release. Entries below **1.8.2** were reconstructed
> from git history when the automation landed (bds-mawitu, 2026-07-12) — they
> are honest headlines, not exhaustive; the per-repo changelogs hold the detail.

## [1.8.8] - 2026-07-14

Carrying mise: catastrophic signature strips revert instead of eating the email body (mise-rejula)

## [1.8.7] - 2026-07-13

Carrying mise-home: the personal-flavour skill now names its Workspace in the picker and calls its own mcp__mise-home__ tools (was mis-wired to the work server).

## [1.8.6] - 2026-07-12

publish.py hardening: refuse untracked files unless --all (bds-fifuko); reinstall CLIs from git+https not the working tree (bds-zelobu)

## [1.8.5] - 2026-07-12

Carrying mise: the work and personal flavours now name which Workspace they act on — an unauthed personal mise no longer reads as the work one being broken (SessionStart + setup_oauth honesty).

## [1.8.4] - 2026-07-12

Hardening: stale-ref sweep (retired Taildrive paths, passe-orphan note, stale footer) + registry-drop guard in /batterie:update

## [1.8.3] - 2026-07-12

Docs: document the suite-changelog mechanism in the versioning guide (bds-defeci); ships pending mise CLAUDE.md doc updates

## [1.8.2] - 2026-07-12

Suite changelog automation (bds-mawitu): one canonical CHANGELOG maintained by publish.py at release time; per-plugin shipped changelogs are now generated stubs pointing here, so no plugin can ship a stale changelog.

## [1.8.1] - 2026-07-12

Carrying **mise**. Rules shard is now copied into `~/.claude/rules/` rather
than symlinked (the plugin root can be an ephemeral Desktop temp dir that
macOS purges, dangling the old symlink so the shard silently vanished);
`displayName: "Mise Home"` on the private flavour (Desktop was title-casing the
id); mise's own CHANGELOG caught up 1.6.0/1.7.0.

## [1.8.0] - 2026-07-12

Family distribution. The `batterie-home` private Directory marketplace and its
`mise-home` flavour, validated end-to-end on a real non-admin family member
across both the GUI auto-push and the standalone-CLI paths.

## [1.7.0] - 2026-07-11

Carrying **mise**. `do(comment)` — open a new comment thread on a Drive file.

## [1.6.0] - 2026-07-11

Carrying **mise**. Google Docs checkbox tick-state via the markdown-export oracle.

## [1.5.3] - 2026-07-08

Suite maintenance (batterie).

## [1.5.2] - 2026-07-08

Carrying **bon**.

## [1.5.1] - 2026-07-08

Carrying **bon**.

## [1.5.0] - 2026-07-08

Carrying **bon**.

## [1.4.0] - 2026-07-07

Carrying **bon**.

## [1.3.2] - 2026-07-07

Carrying **mise**. `do(setup_oauth, force=true)` actually forces now — `force`
was documented and dispatched but never declared in `do()`'s signature, so
FastMCP's schema dropped it and pydantic silently discarded the argument. Found
by a live smoke test minutes after 1.3.1; two seam tests now pin the full
server→dispatch→handler path.

## [1.3.1] - 2026-07-07

Carrying **mise**. `setup_oauth` no longer races itself — the tool mints the
consent URL once (persisting the PKCE verifier) and the detached subprocess
consumes it, so the returned URL is always exchangeable; stale/revoked creds
now fall through to a fresh flow instead of bouncing between "authed!" and
errors; port pre-check hardened (SO_REUSEADDR, pre-browser).

## [1.3.0] - 2026-07-07

Carrying **mise**.

## [1.2.2] - 2026-06-28 — Single-version cutover

The Debian halfway-house (per-plugin versions under a headline suite number)
collapsed to **one version across all plugins**. `assemble.sh` stamps every
vendored `plugin.json` to the suite version; `publish.py` bumps the suite
centrally with a 2-repo push for non-batterie sources; the version ratchet
went suite-level. This is the release from which one-version-one-changelog
became the coherent model — everything above is a single suite release.

---

## History before the single-version cutover

The entries below predate suite 1.2.2, when each plugin carried its own
version. Kept for provenance.

## 2026-06-20 — batterie 1.1.2

Propagate the CLAUDE.md `/batterie-update` → `/batterie:update` staleness fix
(committed 9acd892 without a bump) — clears the version-ratchet quarantine.
CLAUDE.md is vendored into the batterie plugin, so a docs-sweep edit to it needs
a plugin bump.

## 2026-06-12 — batterie 0.2.2

Propagate the source/artifact-pair CLAUDE.md clarification (the "two jobs"
verdict committed 2026-06-11 at 210a878 without a bump) — clears the batterie
assemble version-ratchet that was failing every run.

## 2026-06-11 — batterie 0.2.1

Assembler vendors top-level `scripts/` for skill plugins (restores bon
close/open context scripts, trousse ardoise.sh); suite plugin ships its
`scripts/` for parity.

## 2026-06-10 — Marketplace cutover (batterie 0.2.0)

The bds-bajibo convergence moment. `marketplace.json` removed —
spm1001/batterie (the assembled, bot-maintained repo) is now the single
marketplace for CLI, Desktop, and org. This repo remains the docs umbrella and
the source of the suite-level `batterie` plugin. The `/batterie:update` skill
now targets `@batterie` keys and the `batterie` marketplace name; garde-manger
(decommissioned 2026-06-03) dropped from its CLI-tool table and from the
instruction shard. Tafelmusik unvendored from spm1001/batterie the same evening
— too experimental to distribute; the source repo lives on. Migration for old
installs: add new marketplace + reinstall as `<name>@batterie` + remove old —
keys change, repointing isn't enough.

## 2026-06-04 — Vendor-drift deploy + Desktop re-sync probe

The 2026-05-31 diagnosis (Desktop stuck on mise 0.7.2) deployed today:
spm1001/batterie's vendored shims re-synced (bon 0.23.0, trousse 0.5.9,
mise 0.7.3) and the phantom gueridon entry dropped. **CONFIRMED same evening:**
Desktop offered and installed mise 0.7.3 after this commit landed.
Marketplace-repo commits are the update bus; source-repo bumps alone are
invisible to Desktop/org clients.

## [0.2.0] - 2026-03-18

Batterie-wide consistency pass: docs consolidation, registry, versioning.

### Added
- Plongeur, todoist-gtd, aboyeur added to brigade and marketplace

### Fixed
- Broken path references in CLAUDE.md and README.md
- Marketplace schema issues (strict:false, source format)

### Changed
- Dropped sha pins in favour of pulling HEAD during active development

## 2026-02-27 — Plugin Marketplace

### Added
- `marketplace.json` cataloguing all 8 Batterie de Savoir plugins
- Local Jekyll preview instructions
- Plugin marketplace install path documentation

### Fixed
- Blank-line kramdown compatibility for generated tables

## 2026-02-22 — Registry Automation

### Added
- CLAUDE.md and GitHub Actions lint workflow
- Registry-driven doc generation from `brigade.toml`

## 2026-02-16 — Jeton Integration

### Added
- Jeton (Google OAuth) added to kitchen table and all docs

## 2026-02-15 — Docs Site Launch

### Added
- Full docs site: index page, 8 tool pages, getting-started, principles, for-agents
- README with brigade table and docs site link
- Brigade diagram with system font stack
- Maturity badges, robustness column, source types in brigade table

## 2026-02-15 — Initial Release

### Added
- Plan, bon tracker, initial repo structure
