# Folder Spine

Complete directory and file specification per profile. The creation sequence is ordered: directories before files, parent before child.

## Naming Standards (Important Context)

Three names sometimes get confused. This skill creates the following and keeps them distinct:

| Name | Type | What it is | Reads/writes |
|------|------|-----------|--------------|
| `AGENTS.md` | file at root | [Open standard](https://agents.md/) from Agentic AI Foundation. "README for AI agents." | Read by Claude, Codex, Cursor, Windsurf, etc. (standard+ profile) |
| `CLAUDE.md` | file at root | Claude Code's project-specific overlay. Supplements AGENTS.md with Claude-specific rules. | Read by Claude Code (all profiles) |
| `_local/` | folder at root | Gitignored scratch directory for per-machine local files (notes, drafts, session logs, init-project reports). Never committed. | Skills and humans write here; git ignores it |
| `.claude/agents/` | folder | Claude Code subagent definitions (per project or per plugin). **This skill does NOT create or touch this folder** - subagents are added later if you need them. | Claude Code's subagent system |

Session logs are written to `_local/_session-logs/` (gitignored). They are local-only working notes and are never scaffolded as a tracked folder. The `_agent-context/` folder that v1.2.x scaffolded is no longer created.

## Creation Sequence

| Step | Path | Type | Profile | Notes |
|------|------|------|---------|-------|
| 1 | `CLAUDE.md` | file | All | Claude Code project instructions (Claude-specific overlay) |
| 2 | `README.md` | file | All | Project overview |
| 3 | `CHANGELOG.md` | file | All | Keep a Changelog format |
| 4 | `LICENSE` | file | All (unless `--no-license`) | MIT default; `--license apache` for Apache-2.0 |
| 5 | `.gitignore` | file | All | Standard + type-specific exclusions + `_local/` entry |
| 6 | `_local/` | dir | All | Gitignored scratch directory for untracked local files |
| 7 | `_local/README.md` | file | All | Explainer: gitignored, per-machine scratch, not for shared work |
| 8 | `AGENTS.md` | file | standard+ | Open-standard agent instructions (read by any AI agent) |
| 9 | `DESIGN.md` | file | standard+ | Design system spec for AI agents (Stitch format) |
| 10 | `docs/internal/decisions/` | dir | standard+ | Architecture Decision Records (MADR v4) |
| 11 | `docs/internal/decisions/README.md` | file | standard+ | Explainer: what ADRs are, when to write, how agents use |
| 12 | `docs/internal/decisions/0001-initial-setup.md` | file | standard+ | Seed ADR documenting initialization |
| 13 | `docs/internal/backlog.md` | file | standard+ | Work tracking with header row, no entries |
| 14 | `docs/internal/release-plans/` | dir | standard+ | Release plans (per planning-artifact-model.md) |
| 15 | `docs/internal/release-plans/_unassigned/` | dir | standard+ | Pre-release home for specs and implementation plans without an assigned release |
| 16 | `docs/releases/` | dir | standard+ | Public release notes per version |
| 17 | `CONTRIBUTING.md` | file | public | Contribution guidelines |
| 18 | `CODE_OF_CONDUCT.md` | file | public | Contributor Covenant 2.1 |
| 19 | `SECURITY.md` | file | public | Vulnerability reporting |
| 20 | `.github/PULL_REQUEST_TEMPLATE.md` | file | public | PR template |
| 21 | `.github/ISSUE_TEMPLATE/*.yml` | files | public | bug_report.yml, feature_request.yml, config.yml |

## Profile Trees

### Minimal Profile

```
project-root/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── _local/
    └── README.md
```

### Standard Profile

```
project-root/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── AGENTS.md
├── DESIGN.md
├── LICENSE
├── .gitignore
├── _local/
│   └── README.md
└── docs/
    ├── internal/
    │   ├── backlog.md
    │   ├── decisions/
    │   │   ├── README.md
    │   │   └── 0001-initial-setup.md
    │   └── release-plans/
    │       └── _unassigned/
    └── releases/
```

### Public Profile

```
project-root/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── AGENTS.md
├── DESIGN.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── .gitignore
├── _local/
│   └── README.md
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.yml
│       ├── feature_request.yml
│       └── config.yml
└── docs/
    ├── internal/
    │   ├── backlog.md
    │   ├── decisions/
    │   │   ├── README.md
    │   │   └── 0001-initial-setup.md
    │   └── release-plans/
    │       └── _unassigned/
    └── releases/
```

## Notes

- Session logs go to `_local/_session-logs/` (gitignored). All agents write here; the LLM short name appears in each filename (e.g., `2026-05-28_15-30_claude_<title>.md`). This folder is not scaffolded at init time - it is created on first use by whichever skill writes a session log.
- `AGENTS.md` (standard+) serves the open standard at https://agents.md/ - it is what Codex, Cursor, Windsurf and other AI agents read. `CLAUDE.md` is the Claude-specific overlay.
- `DESIGN.md` follows the Google Stitch format. Optional - delete if project has no UI surface.
- Project type additions (src/, tests/, etc.) layer on top - see `project-types.md`.
- **Decisions location:** `docs/internal/decisions/` - NOT `docs/decisions/` and NOT per-agent `DECISIONS.md`. The seeded `README.md` there explains the contract to any agent.
- **Release plans:** `docs/internal/release-plans/` follows the planning-artifact-model. Specs and implementation plans live inside per-effort folders at `release-plans/{plan_vX.Y.Z,_unassigned}/<id>_<slug>/`. The `_unassigned/` subdir is created at init time as the default home for pre-release work.
- **`_local/`:** Always created, always gitignored. Use for per-machine scratch (notes, drafts, experimental outputs, init-project's own dry-run and onboarding reports, session logs at `_local/_session-logs/`).
- **No per-agent subfolders** (v1.1.x had `AGENTS/<agent>/CONTEXT.md` and `AGENTS/<agent>/TODO.md` per agent). v1.2.0 dropped these because per-agent context duplicates what `AGENTS.md` + `CLAUDE.md` already cover.
