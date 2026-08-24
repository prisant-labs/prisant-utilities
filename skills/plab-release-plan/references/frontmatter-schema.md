# Frontmatter Schema

The release plan's YAML frontmatter is the machine-readable contract that downstream tooling (and humans scanning) reads.

## Required fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `version` | string | Semver release version with `v` prefix | `v1.4.0` |
| `title` | string | Convention: `"Release plan: vX.Y.Z"`. Quote it (colon). | `"Release plan: v1.4.0"` |
| `type` | const | Always `release-plan` | `release-plan` |
| `status` | enum | `draft`, `in-progress`, `released` | `draft` |
| `created` | ISO date | When the plan file was first written | `2026-05-28` |
| `updated` | ISO date | Last substantive edit | `2026-05-28` |
| `spec-count` | integer | Count of effort folders with `spec.md` (computed by `--update`) | `2` |
| `plan-count` | integer | Count of effort folders with `implementation-plan.md` (computed by `--update`) | `2` |
| `checklist-complete` | boolean | Whether every doc-update checklist item is checked (computed by `--update`) | `false` |

## Optional fields

| Field | Type | When to use | Example |
|-------|------|-------------|---------|
| `target-date` | ISO date | Optional target ship date | `2026-06-15` |
| `includes` | list of strings | Effort ids in scope; grows on `--promote`, shrinks on `--demote` | `[S-07, S-05]` |
| `gate-waivers` | list of `{id, gate, reason}` | Explicit waivers for hygiene gates (e.g., an effort that ships without an implementation plan because the change is one-line) | See below |
| `theme` | string | Short release theme | `"Workflows release"` |

### `gate-waivers` example

```yaml
gate-waivers:
  - id: S-12
    gate: b                       # which hygiene gate is waived
    reason: "One-line README fix; no implementation plan needed."
```

## Status lifecycle

```
draft -> in-progress -> released
```

| Status | Meaning | Who sets it |
|--------|---------|-------------|
| `draft` | `--create` just ran; aggregation is empty or sparse | Skill on creation |
| `in-progress` | At least one effort promoted into the release; work underway | Auto on first `--promote` |
| `released` | Tag cut, doc-update checklist complete, hygiene gates pass | Manual (maintainer after tag; skill never auto-sets this) |

## Validation rules

- `version` matches `^v\d+\.\d+\.\d+$` (semver with `v` prefix)
- `type` is always `release-plan`
- `status` must be one of the enum values
- `spec-count` must equal the actual number of effort folders containing `spec.md`
- `plan-count` must equal the actual number of effort folders containing `implementation-plan.md`
- `checklist-complete` must reflect the actual state of the doc-update checklist checkboxes
- `includes` must equal the sorted list of effort ids found in the release folder
- Every entry in `gate-waivers` references a real effort id and a real gate (a-e)

## Full example

```yaml
---
version: v1.4.0
title: "Release plan: v1.4.0"
type: release-plan
status: in-progress
created: 2026-05-12
updated: 2026-05-28
target-date: 2026-06-15
includes:
  - S-07
  - S-05
spec-count: 2
plan-count: 1
checklist-complete: false
gate-waivers:
  - id: S-05
    gate: b
    reason: "v1.2.0 zone removal; implementation plan deferred until decomposition stabilizes."
---
```

## Why this schema

- **Counts are dynamic.** `spec-count`, `plan-count`, `checklist-complete` are computed; never hand-edit. Hand-edits drift; computed values stay honest.
- **`includes` is the canonical list of in-scope work.** Whatever's listed here MUST exist on disk (`--update` regenerates from disk; if you remove an entry by hand, the next `--update` will add it back).
- **`gate-waivers` is the only explicit-override surface.** A waiver requires a reason. The release plan's hygiene gate report shows waived items so they remain visible.
- **`status: released` is manual.** The skill reports readiness; only a human sets the flag after tagging. This prevents "skill says released, tag never happened" drift.

Do not invent fields. If a need arises that this schema doesn't cover, propose an extension in the plab-release-plan backlog rather than ad-hoc adding it.
