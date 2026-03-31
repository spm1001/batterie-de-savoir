---
layout: default
title: Consommé
---

# Consommé — Clarification

> **Now part of [Trousse](trousse).** The consomme skill was absorbed into trousse in v0.5.0. Install trousse and the analysis skill comes with it. The standalone `spm1001/consomme` repo is archived.

BigQuery data analysis for AI coding agents. Messy data goes in, crystal-clear insights come out — like the classical technique it's named for, where a raft of egg whites draws impurities from a murky stock and leaves behind a perfectly transparent broth. The technique does the work, not the person.

Consommé is a skill that pairs Google's BigQuery Data Analytics MCP extension with a structured methodology adapted from Anthropic's data plugin approach. It gives Claude Code a repeatable workflow from "what tables do we have?" to an interactive HTML dashboard with KPI cards and filters.

## How to get it

Install trousse — consomme comes with it:

```
claude plugin install batterie-de-savoir/trousse
```

The skill is invoked as `/consomme` (or `trousse:consomme`). Seven commands provide shortcuts: `/consomme-profile`, `/consomme-explore`, `/consomme-dashboard`, `/consomme-validate`, `/consomme-sheets`, `/consomme-ingest`.

## When to use / When NOT to use

**Use Consommé when:**
- You need to explore, query, or analyse structured data in BigQuery
- You want interactive visualisations — HTML dashboards with Chart.js, filters, KPI cards
- You're building funnels, cohort analyses, or forecasts from warehouse data
- You need the agent to profile a dataset before jumping to conclusions

**Do NOT use Consommé when:**
- You need content from Google Workspace (Docs, Sheets, Gmail, Drive) — **use [Mise](mise)**
- You need to prepare raw data for BigQuery (SPSS, codebooks, schema design) — **use `/mandoline`** (also in trousse)
- You're working with local CSV/Excel files that aren't in BigQuery
- You need real-time streaming data rather than analytical queries

## Key concepts

### 5-stage methodology

1. **Discovery** — Catalogue search. What datasets and tables exist? What's the schema?
2. **Exploration** — 3-phase data profiling: structural (row counts, partitioning), column-level (types, nulls, cardinality), and relationships (keys, joins, referential patterns).
3. **SQL craft** — BigQuery-specific SQL reference: window functions, CTEs, funnels, cohort analysis, approximate aggregation.
4. **Analysis** — Execute queries via MCP tools (`execute_sql`, `forecast`, `analyze_contribution`). Interpret results in context.
5. **Validation** — Pre-delivery QA framework. Sense-check results before presenting.

### Companion skill: Mandoline

Mandoline (`/mandoline`, also in trousse) is the upstream counterpart — it transforms raw data (SPSS files, messy spreadsheets) into self-documenting BigQuery tables. Consommé analyses what mandoline produces. Together they cover the full pipeline from raw survey data to interactive dashboards.

## How it relates to other tools

| Tool | Relationship |
|------|-------------|
| [**Mise**](mise) | Mise handles Google Workspace content. Consommé handles structured data in BigQuery. The boundary is explicit — consommé's skill routes Workspace requests to Mise. |
| **Mandoline** | Data prep (in trousse). Transforms raw data INTO BigQuery. Consommé analyses data already IN BigQuery. |
| [**Bon**](bon) | An analysis task tracked as a bon outcome; consommé does the analytical work within that outcome. |
| [**Garde-manger**](garde-manger) | Past analyses are searchable in garde-manger. |

## Source

The skill lives in [trousse](https://github.com/spm1001/trousse) at `skills/consomme/`. The archived standalone repo is at [spm1001/consomme](https://github.com/spm1001/consomme).
