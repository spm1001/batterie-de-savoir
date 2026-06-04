# Changelog

## 2026-06-04 — Vendor-drift deploy + Desktop re-sync probe

The 2026-05-31 diagnosis (Desktop stuck on mise 0.7.2) deployed today:
spm1001/batterie's vendored shims re-synced (bon 0.23.0, trousse 0.5.9,
mise 0.7.3) and the phantom gueridon entry dropped. This commit also
probes the Desktop update mechanism: hypothesis is that Desktop
re-resolves this marketplace's URL sources only when THIS repo gets a
new commit — source-repo version bumps alone are invisible to it.
If Desktop offers mise 0.7.3 after this lands, hypothesis confirmed
(relevant to bds-sucega convergence and the mit-tools design).

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
