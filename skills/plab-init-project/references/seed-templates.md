# Seed Templates

All file templates created by init-project. Variables are replaced at creation time.

## Template Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{{PROJECT_NAME}}` | User input or directory name | `my-project` |
| `{{DESCRIPTION}}` | User input | `A tool for analyzing survey data` |
| `{{DATE}}` | System clock | `2026-05-28` |
| `{{YEAR}}` | System clock | `2026` |
| `{{PROFILE}}` | User selection | `standard` |
| `{{LICENSE}}` | User selection | `MIT` |

> **v1.2.0 note:** `{{AGENT}}` and `{{AGENT_LIST}}` variables removed. v1.1.x scaffolded per-agent CONTEXT.md and TODO.md files inside `AGENTS/<agent>/`. v1.2.0 drops these because per-agent context overlaps with `AGENTS.md` (open standard, agent-neutral) and `CLAUDE.md` (Claude-specific overlay). See `folder-spine.md` for the naming clarification.

---

## Root Files

### CLAUDE.md (All profiles)

```markdown
# Claude Code Instructions

## Project Context

- **{{PROJECT_NAME}}** - {{DESCRIPTION}}
- Created: {{DATE}}

## Repository Structure

*Update this section as the project evolves.*

## Rules

- Use conventional commits for commit messages (`feat:`, `fix:`, `docs:`, `chore:`)
- Never commit secrets, credentials, or `.env` files
- Prefer editing existing files over creating new ones

## Conventions

*Add project-specific coding conventions here.*

## Testing

*Add test commands and testing conventions here.*

## Development

*Add build, run, and development workflow commands here.*
```

### README.md (All profiles)

```markdown
# {{PROJECT_NAME}}

{{DESCRIPTION}}

## Overview

*Brief description of what this project does.*

## Getting Started

*Instructions for getting started.*

## License

This project is licensed under the {{LICENSE}} License - see [LICENSE](LICENSE) for details.
```

### CHANGELOG.md (All profiles)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
```

### AGENTS.md (standard+ only)

This file follows the [agents.md open standard](https://agents.md/) from the Agentic AI Foundation. It is read by any AI agent that recognises the standard (Claude, Codex, Cursor, Windsurf, and others). Keep it agent-neutral; Claude-specific overlays go in `CLAUDE.md`.

```markdown
# {{PROJECT_NAME}}

> {{DESCRIPTION}}

## Project Overview

*Brief description of the project, its purpose, and key technologies.*

## Build and Test Commands

*Commands an agent should know to build, run, and test this project.*

```bash
# Build
# Test
# Run
```

## Code Style

*Coding conventions, formatters, linters.*

## Conventions

- Use conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- See `CLAUDE.md` for Claude Code-specific rules
- Record architectural decisions as MADR v4 ADRs in `docs/internal/decisions/` (see that directory's `README.md`)

## Working Folders

- `_local/_session-logs/` - chronological session logs from all agents (gitignored)
- `_local/` - per-machine scratch (gitignored)

## Key Files

- `CLAUDE.md` - Claude Code overlay (Claude-specific rules)
- `CHANGELOG.md` - Version history
- `docs/internal/decisions/` - Architecture Decision Records (MADR v4)
- `docs/internal/release-plans/` - In-progress release plans with per-effort spec/plan folders
```

### DESIGN.md (standard+ only)

```markdown
# Design System

> Design system for {{PROJECT_NAME}}. AI agents should reference this file when generating UI components, styles, or layouts.

## Visual Theme & Atmosphere

*Describe the overall mood, visual density, and design philosophy.*

## Color Palette

| Role | Value | Usage |
|------|-------|-------|
| Primary | #1A73E8 | Buttons, links, key actions |
| Secondary | #34A853 | Success states, confirmations |
| Background | #FFFFFF | Page background |
| Surface | #F8F9FA | Cards, panels |
| Error | #EA4335 | Error states, destructive actions |
| Text Primary | #202124 | Body text |
| Text Secondary | #5F6368 | Captions, labels |

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Heading 1 | Inter, sans-serif | 32px | 700 |
| Heading 2 | Inter, sans-serif | 24px | 600 |
| Body | Inter, sans-serif | 16px | 400 |
| Caption | Inter, sans-serif | 12px | 400 |

## Spacing

- Base unit: 8px
- Scale: 4, 8, 16, 24, 32, 48px

## Component Styles

| Component | Border Radius | Shadow | Border |
|-----------|---------------|--------|--------|
| Button | 8px | none | none |
| Card | 12px | 0 1px 3px rgba(0,0,0,0.12) | none |
| Input | 6px | none | 1px solid #DADCE0 |

## Layout Principles

*Grid system, max-width, responsive breakpoints.*

## Do's and Don'ts

**Do:**
- *List design principles to follow*

**Don't:**
- *List anti-patterns to avoid*
```

---

## Documentation Files

### docs/internal/decisions/README.md (standard+ only)

```markdown
# Architecture Decision Records

This directory tracks architectural decisions for {{PROJECT_NAME}} using the [MADR v4](https://github.com/adr/madr) (Markdown Architectural Decision Records) format.

## What Goes Here

One numbered markdown file per decision: `nnnn-title-in-kebab-case.md` (e.g., `0001-initial-setup.md`, `0002-use-postgres-over-mysql.md`).

**Create an ADR when:**

- A decision affects project architecture, structure, or conventions
- Multiple alternatives were considered
- A future reader (human or AI agent) would ask "why was this done this way?"
- The decision is hard to reverse

**Don't create an ADR for:**

- Implementation details (variable names, minor refactors)
- Trivially reversible choices
- Personal preferences with no structural impact

## Expected Behavior

### For human contributors

Before making a significant architectural change, write a `proposed` ADR describing the options and preferred outcome. Move it to `accepted` once the decision lands.

### For AI agents (claude, codex, and others)

You are expected to read this directory before making architectural changes and to create ADRs when you make architectural decisions yourselves. Use `decision-makers: [claude]` or `decision-makers: [codex]` in the frontmatter.

**Important:** If you see a pattern in the code that looks wrong or non-standard, check this directory first. The most valuable ADRs are the ones that document intentional choices that look incorrect to an outsider - without them, you may "correct" a deliberate decision and undo work.

## Format

Use the MADR v4 template. Required sections:

1. **Title** - short, captures problem + solution
2. **Context and Problem Statement**
3. **Considered Options**
4. **Decision Outcome** - chosen option + justification

Optional sections: Decision Drivers, Consequences, Confirmation, Pros and Cons of the Options, More Information.

### Optional YAML frontmatter

```yaml
---
status: "proposed | accepted | rejected | deprecated | superseded by ADR-0123"
date: YYYY-MM-DD
decision-makers: [jp, claude]
consulted: []
informed: []
---
```

## Lifecycle

```
proposed -> accepted -> [deprecated | superseded by ADR-NNNN]
proposed -> rejected
```

Once an ADR is `accepted`, treat it as immutable history. New circumstances get a new ADR that supersedes the old one - don't rewrite the original.

## Outcomes This Directory Enables

- **Traceability:** every non-trivial architectural choice has a "why" that survives turnover
- **Coherence across agents:** Claude and Codex read the same directory and respect the same decisions
- **Safe refactoring:** future work can check this directory before "correcting" intentional patterns
- **Audit trail:** the decision history is git-tracked, reviewable, and cross-referenceable

## References

- MADR v4 standard: https://github.com/adr/madr
- ADR hub: https://adr.github.io/
```

### docs/internal/decisions/0001-initial-setup.md (standard+ only)

```markdown
---
status: accepted
date: {{DATE}}
decision-makers: [jp]
---

# 1. Project Initialization

## Context and Problem Statement

New project {{PROJECT_NAME}} is being initialized. We need to establish base structure, conventions, and tracking infrastructure before any meaningful work begins.

## Considered Options

- Ad-hoc scaffolding (create folders as needed)
- prisant-utilities `plab-init-project` skill with `{{PROFILE}}` profile
- Copy structure from an existing project

## Decision Outcome

Chosen: **prisant-utilities `plab-init-project` skill with `{{PROFILE}}` profile.**

Configuration:

- Profile: `{{PROFILE}}`
- License: {{LICENSE}}
- Changelog: Keep a Changelog format
- Decisions: MADR v4 in `docs/internal/decisions/`
- Gitignored scratch: `_local/`
- Session logs: `_local/_session-logs/` (gitignored, written on first use)
- Agent instructions: `AGENTS.md` (open standard) + `CLAUDE.md` (Claude Code overlay)

### Consequences

- Standardized agentic infrastructure from day one
- Decision history tracked in MADR v4 format
- `_local/` available for per-machine scratch without polluting git
- AGENTS.md and CLAUDE.md split keeps agent-neutral instructions separate from Claude-specific rules
- Future scaling: profile can be upgraded (minimal -> standard -> public) by re-running init-project non-destructively
```

### docs/internal/backlog.md (standard+ only)

```markdown
# Backlog

| ID | Title | Type | Status | GH | Release |
|----|-------|------|--------|----|---------|
```

---

## Community Files

### CONTRIBUTING.md (public only)

```markdown
# Contributing to {{PROJECT_NAME}}

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run any tests
5. Commit with a descriptive message
6. Push to your fork
7. Open a Pull Request

## Reporting Bugs

Please open a [GitHub Issue](../../issues/new?template=bug_report.yml) with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
```

### CODE_OF_CONDUCT.md (public only)

```markdown
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone.

## Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the project maintainers. All complaints will be reviewed and
investigated.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org/), version 2.1.
```

### SECURITY.md (public only)

```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue**
2. Email the maintainers or use GitHub's [private vulnerability reporting](../../security/advisories/new)
3. Include steps to reproduce, impact assessment, and any suggested fixes

We will acknowledge receipt within 48 hours and provide a detailed response
within 5 business days.

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |
```

---

## GitHub Templates

### .github/PULL_REQUEST_TEMPLATE.md (public only)

```markdown
## Summary

<!-- Brief description of changes -->

## Changes

- 

## Testing

- [ ] Tests pass
- [ ] Manual verification completed

## Related Issues

<!-- Closes #XX, Fixes #YY -->
```

### .github/ISSUE_TEMPLATE/bug_report.yml (public only)

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: What happened? What did you expect to happen?
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this?
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, version, relevant tools
```

### .github/ISSUE_TEMPLATE/feature_request.yml (public only)

```yaml
name: Feature Request
description: Suggest a new feature or improvement
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this solve?
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this work?
    validations:
      required: true
```

### .github/ISSUE_TEMPLATE/config.yml (public only)

```yaml
blank_issues_enabled: true
```

---

## License Files

### LICENSE - MIT (All profiles, default)

```
MIT License

Copyright (c) {{YEAR}} {{PROJECT_NAME}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### LICENSE - Apache-2.0 (All profiles, when `--license apache`)

Use the standard Apache License, Version 2.0 text from https://www.apache.org/licenses/LICENSE-2.0.txt with `{{YEAR}}` and `{{PROJECT_NAME}}` substituted in the copyright notice.

### _local/README.md (All profiles)

```markdown
# _local/

This directory is **gitignored**. Use it for untracked local files - personal notes, drafts, experimental outputs, init-project's own reports (dry-run, onboarding), and session logs.

## Rules

- **Nothing here is backed up via git.** If you care about it, move it elsewhere before committing.
- **Not for shared work.** Files here never reach other contributors or other machines.
- **Safe to delete wholesale.** If `_local/` ever feels crowded, archive what matters and clear the rest.

## Typical Contents

- `_session-logs/` - chronological session logs from all agents (created on first use)
- `plab-init-project/` - init-project's own dry-run and onboarding reports
- `backup/` - archived legacy files from migrations (kept outside git)
- Local scratch notes, draft outputs, in-progress experiments
- Temporary data files, downloaded fixtures
- Per-machine configuration that shouldn't be shared

## Why This Exists

Every project accumulates ephemeral artifacts that shouldn't be committed but shouldn't live in a temp directory either. `_local/` gives them one predictable home. This pattern supersedes the older `_NOTES/` convention.
```

### .gitignore (All profiles)

```
# OS
.DS_Store
Thumbs.db
Desktop.ini

# Editors
.vscode/
.idea/
*.swp
*.swo
*~

# Project
_local/
.env
.env.local
.env.*.local

# Build
dist/
build/
```

Notes:
- `_local/` entry is always ensured in `.gitignore` (appended if `.gitignore` already exists but doesn't include it).
- Project-type-specific entries are appended by project type - see `project-types.md`.

---

## Report Templates

Both reports are written to `_local/plab-init-project/` in the target project. `_local/` is gitignored - reports stay local.

### Dry-Run Report Template

Output path: `_local/plab-init-project/plab-init-project_dry-run_YYYY-MM-DD.md`

```markdown
# Init-Project Dry Run

**Date:** {{DATE}}
**Project:** {{PROJECT_NAME}}
**Profile:** {{PROFILE}}
**Type:** {{TYPE}}

## Preview

| Action | Path | Notes |
|--------|------|-------|
| would create | ... | ... |

## Summary

- Would create: N files/directories
- Would skip: N existing
- Would merge: N

## Next Step

Run `/plab-init-project` (without `--dry-run`) to apply.
```

### Onboarding Report Template

Output path: `_local/plab-init-project/plab-init-project_onboard_YYYY-MM-DD.md`

```markdown
# Init-Project Onboarding Report

**Date:** {{DATE}}
**Project:** {{PROJECT_NAME}}
**Profile:** {{PROFILE}}

## Summary Checklist

- [ ] Project purpose defined
- [ ] Conventions established
- [ ] Tech stack documented
- [ ] Design system configured (standard+ only)
- [ ] First tasks captured

## Session Record

### Q1: [Topic]

**Question:** [What was asked]

**Response:** [User's answer]

**Actions taken:**
- [File updated and what changed]

## Incomplete Items

| Item | Reason | Recommendation |
|------|--------|----------------|
| ... | ... | ... |

## Recommendations

- [LLM suggestions based on answers]
```
