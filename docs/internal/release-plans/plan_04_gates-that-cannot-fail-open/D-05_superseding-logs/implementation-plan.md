---
id: D-05
title: "Implementation plan: Declare and archive same-arc superseding session logs"
type: implementation-plan
status: complete
created: 2026-08-23
updated: 2026-08-24
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: Declare and archive same-arc superseding session logs

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Give `plab-wrap-session` a same-arc supersession check that declares superseding logs in
prose and archives the older file to `_local/_session-logs/_superseded/` under per-action
confirmation, with no new frontmatter field.

**Architecture:** Three layers. (1) Wrap's Evidence Gathering gains a same-arc judgment against the
newest existing log, and the Summary section carries the resulting declaration and disposition; the
archive proposal reuses the hygiene sweep's existing confirmation protocol rather than a new one. (2)
`plab-continue-session`'s `log-discovery.md` documents `_local/_session-logs/_superseded/` as a
directory its existing one-level-deep allowlist already excludes, with no pipeline change. (3) Both
skills bump together and the repo-level bookkeeping records the change, per the pairing contract.

**Spec:** `spec.md`

**Target versions:** `plab-wrap-session` 1.6.0, `plab-continue-session` 1.4.0. Plugin-level version
(`library.json` top field, both `plugin.json` files) stays at 0.2.0 through this effort; that bump is
a release-level action gated by all eight v0.4.0 efforts completing (see `plan.md`'s Hygiene
Gate (f)), not something any single effort's plan performs. See Human-facing documentation below.

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) anywhere. Use " - " or restructure. A PreToolUse hook
  blocks the write.
- State a contract once, in one named file; everything else cites it. The archive proposal cites the
  hygiene sweep's resolution protocol rather than restating it; the same-arc declaration lives only in
  Summary, not duplicated into a new heading.
- Archive, never delete. Every filesystem-changing action is per-action confirmed before it executes.
- No `supersedes:` (or equivalent) frontmatter field, at any point in this plan. If a step seems to
  need one, stop and re-read spec.md's Non-Goals; it does not.
- If another v0.4.0 effort (most likely D-04 or D-07) has already added a numbered item to wrap's
  Evidence Gathering list by the time this plan executes, add this effort's item as the next available
  number, not a hard-coded "7". Same for the shared `## 1.6.0` / `## 1.4.0` HISTORY.md headings:
  create the heading if absent, append this effort's own paragraph if present. Never overwrite another
  effort's paragraph.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Wrap-side same-arc check, declaration, and archive mechanics | AC-1, AC-2, AC-3, AC-4, AC-5 | agent | Done |
| P2 | Continue-side `_superseded/` documentation | AC-6 | agent | Done |
| P3 | Repo bookkeeping and AC-7 verification | AC-7 | agent | Done |

---

## Phase 1: Wrap-side same-arc check, declaration, and archive mechanics

**Goal:** Wrap judges same-arc coverage against the newest existing log, declares supersession and its
disposition in Summary, and executes the archive move only on explicit confirmation.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md`
- Modify: `skills/plab-wrap-session/HISTORY.md`

**Fulfills:** AC-1, AC-2, AC-3, AC-4, AC-5

**Steps:**

- [x] Step 1: Add a new numbered item to `## Evidence Gathering` (after the existing item 6, "List
  skills invoked this session...", and before the closing "If git is unavailable..." sentence).
  Renumber to the next available integer if a sibling effort already added an item 7 this release
  (see Global constraints):

  ```markdown
  7. In deep and final modes, determine the newest existing log in `_local/_session-logs/` (see
     `references/log-discovery.md` for the newest-wins sort across the flat store and any `YYYY-MM/`
     folders) and judge whether it covers the same arc as this session. If it does, prepare one
     archive proposal under the same per-action confirmation protocol the hygiene sweep uses (see
     `references/hygiene-sweep.md`): propose moving the older file to
     `_local/_session-logs/_superseded/`, execute only on explicit approval, and record the
     disposition, declared plus archived-or-not, in the new log's Summary.
  ```

- [x] Step 2: Append one sentence to the **Summary** bullet under `### Body Sections (Final Mode)`
  (the line reading "**Summary** - 2-4 sentences. What happened and why it matters."):

  ```markdown
  When the Evidence Gathering same-arc check above judges the newest existing log to cover the same
  arc as this session, end Summary with one additional sentence naming that log by filename only (no
  path) and stating whether it was archived to `_superseded/` or not archived.
  ```

- [x] Step 3: Bump wrap's frontmatter:

  ```yaml
  metadata:
    version: "1.6.0"
    updated: 2026-08-23
  ```

- [x] Step 4: Add (or append to, if present) the `## 1.6.0` row and section in
  `skills/plab-wrap-session/HISTORY.md`. If the row and heading already exist (a sibling v0.4.0 effort
  landed first), add this paragraph under the existing heading rather than duplicating the row.

  Row (only if the 1.6.0 row does not yet exist):
  `| 1.6.0 | 2026-08-23 | v0.4.0 | added | Gates that cannot fail open: see the 1.6.0 section for the full list. |`

  Paragraph to add under `## 1.6.0 - 2026-08-23`:

  ```markdown
  **Added: same-arc log supersession (D-05).** When the newest existing log covers the same arc as
  the session being wrapped, the new log declares the supersession in Summary and proposes archiving
  the older file to `_local/_session-logs/_superseded/` under per-action confirmation. No
  `supersedes:` frontmatter field was added; it would have had zero consumers today, the same shape
  as D-04 (capture-lite consumers). `references/log-discovery.md` documents `_superseded/` as excluded
  from discovery, using the allowlist mechanism unchanged.
  ```

**Verification:**

```bash
grep -n "same arc\|_superseded" skills/plab-wrap-session/SKILL.md
```
Expected: the new Evidence Gathering item and the Summary bullet addition both appear.

```bash
grep -n "1.6.0" skills/plab-wrap-session/SKILL.md skills/plab-wrap-session/HISTORY.md
```
Expected: version in both files.

Manual check (no fixture harness exists for this behavior; it is agent-judgment-driven, not
script-driven): re-read Requirement 2 and confirm the new SKILL.md text does not attempt to specify a
deterministic same-arc algorithm.

---

## Phase 2: Continue-side `_superseded/` documentation

**Goal:** Document `_local/_session-logs/_superseded/` as a directory the existing discovery allowlist
already excludes, with no change to either search pipeline.

**Files:**
- Modify: `skills/plab-continue-session/references/log-discovery.md`
- Modify: `skills/plab-continue-session/SKILL.md` (frontmatter version only)
- Modify: `skills/plab-continue-session/HISTORY.md`

**Fulfills:** AC-6

**Steps:**

- [x] Step 1: In the "Store layout: flat or month folders" table, change the last row from:

  ```markdown
  | `_session-logs/<anything else>/` | **no** | deliberately outside the corpus (`_capture/`) |
  ```

  to:

  ```markdown
  | `_session-logs/<anything else>/` | **no** | deliberately outside the corpus (`_capture/`, `_superseded/`) |
  ```

- [x] Step 2: Add one sentence after the existing allowlist paragraph (the one ending "...the
  mechanism any future deliberately-hidden subdirectory relies on."):

  ```markdown
  As of `plab-wrap-session` 1.6.0, `_local/_session-logs/_superseded/` holds logs archived because a
  newer log superseded them (D-05 in `_local/skill-roadmaps/2026-08-18/pair-defects.md`). The
  allowlist above already excludes it; neither pipeline below needed to change.
  ```

- [x] Step 3: Bump continue's frontmatter, only if no sibling v0.4.0 effort (most likely D-04) has
  already bumped it this release:

  ```yaml
  metadata:
    version: "1.4.0"
    updated: 2026-08-23
  ```

- [x] Step 4: Add (or append to, if present) the `## 1.4.0` row and section in
  `skills/plab-continue-session/HISTORY.md`, same create-or-append rule as Phase 1 Step 4.

  Paragraph to add under `## 1.4.0 - 2026-08-23`:

  ```markdown
  **Added: `_superseded/` named in the discovery allowlist (D-05).** `plab-wrap-session` 1.6.0 can
  archive a same-arc superseded log to `_local/_session-logs/_superseded/`. The existing one-level-deep
  allowlist already excluded it; this only documents the name. No pipeline change.
  ```

**Verification:**

```bash
grep -n "_superseded" skills/plab-continue-session/references/log-discovery.md
```
Expected: two hits (the table row and the new sentence).

```bash
grep -n "1.4.0" skills/plab-continue-session/SKILL.md skills/plab-continue-session/HISTORY.md
```
Expected: version in both files.

---

## Phase 3: Repo bookkeeping and AC-7 verification

**Goal:** Record the change in the places a reader or a future tool looks, and confirm no
`supersedes:` field was introduced anywhere.

**Files:**
- Modify: `library.json` (component versions only)
- Modify: `docs/skills/plab-wrap-session/README.md`
- Modify: `docs/skills/plab-continue-session/README.md`
- Modify: `README.md` (skill table)
- Modify: `CHANGELOG.md` ([Unreleased])

**Fulfills:** AC-7

**Steps:**

- [x] Step 1: In `library.json`, set `components.skills[plab-wrap-session].version` to `"1.6.0"` and
  `components.skills[plab-continue-session].version` to `"1.4.0"`, if not already at those values from
  a sibling effort. Do not change the top-level `version` field (stays `"0.2.0"`; see Target versions
  above).

- [x] Step 2: In `docs/skills/plab-wrap-session/README.md`, update the `**Version:**` line to `1.6.0`
  and add one sentence to the Reference Files or Output Shape section describing the same-arc check
  and `_superseded/`, cross-referencing `references/log-discovery.md` rather than restating it.

- [x] Step 3: In `docs/skills/plab-continue-session/README.md`, update the `**Version:**` line to
  `1.4.0` and add `_superseded/` to the "Store layout" table shown in that README (mirrors Phase 2
  Step 1).

- [x] Step 4: In root `README.md`'s skill table, bump the Version column for `plab-wrap-session` to
  `1.6.0` and `plab-continue-session` to `1.4.0`, if not already bumped by a sibling effort.

- [x] Step 5: Add a bullet under `CHANGELOG.md`'s `[Unreleased]` heading (in the existing
  "What changes for you" voice, `### Added`):

  ```markdown
  - `plab-wrap-session` 1.6.0: same-arc log supersession. When the newest existing log covers the
    same arc as the session being wrapped, the new log declares it in Summary and proposes archiving
    the older file to `_local/_session-logs/_superseded/` under per-action confirmation. No new
    frontmatter field.
  ```

- [x] Step 6: Verify AC-7 directly:

  ```bash
  grep -rn "supersedes:" skills/plab-wrap-session/references/frontmatter-schema.md
  ```
  Expected: no output. If this ever produces a match, a `supersedes:` field was introduced somewhere
  in this plan's execution and must be removed; re-read spec.md's Non-Goals.

**Verification:**

```bash
grep -n "1.6.0" library.json docs/skills/plab-wrap-session/README.md README.md
grep -n "1.4.0" library.json docs/skills/plab-continue-session/README.md README.md
```
Expected: the new version string present in each named file.

---

## CI and Documentation Coverage

### CI

No CI change. This effort modifies skill behavior and reference documentation only; it does not add
or move any `.github/workflows/` file. CI-01 (CI bootstrap, a separate v0.4.0 effort) gives this
repository continuous integration for the first time; once it lands, this effort's changes are graded
like everything else by the toolkit's `check.mjs` gate at Universal tier. This effort's own mechanism,
the same-arc judgment, the Summary declaration, the archive proposal, is mechanization-ladder rung 3,
a documented convention the wrapping agent follows each session, not a rung-1 deterministic check. No
canary-backed detector is added, and none is warranted: the judgment is agent discretion by design
(spec Requirement 2), so there is nothing for a canary to prove still detects.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: new Evidence Gathering item, Summary bullet addition, version
  bump (Phase 1).
- `skills/plab-wrap-session/HISTORY.md`: 1.6.0 entry (Phase 1).
- `skills/plab-continue-session/references/log-discovery.md`: `_superseded/` named in the store-layout
  table and one explanatory sentence (Phase 2).
- `skills/plab-continue-session/SKILL.md`: version bump only, no behavioral text changes (Phase 2).
- `skills/plab-continue-session/HISTORY.md`: 1.4.0 entry (Phase 2).

### Human-facing documentation

- `docs/skills/plab-wrap-session/README.md`: version line, one new sentence on the same-arc check
  (Phase 3).
- `docs/skills/plab-continue-session/README.md`: version line, `_superseded/` row (Phase 3).
- `README.md`: skill table version bump for both skills (Phase 3).
- `CHANGELOG.md`: `[Unreleased]` bullet (Phase 3).
- `library.json`: component versions only (Phase 3). The top-level plugin version and both
  `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` files are deliberately **not** touched by
  this plan; that bump, and the `manifest.generated.json` regeneration it triggers, is a release-level
  action gated by all eight v0.4.0 efforts completing (`plan.md` Hygiene Gate (f)), performed
  once at tag time rather than once per effort.

---

## Rollback

Every filesystem-changing action this feature performs is per-action confirmed and move-only, so an
individual archived file is trivially reversible: move it back from `_local/_session-logs/_superseded/`
to `_local/_session-logs/`. To revert the feature itself, revert the SKILL.md and reference-file diffs
from Phases 1 and 2 and the version and HISTORY bumps; no data migration is needed, because the
`_superseded/` directory was already invisible to discovery before this effort (the allowlist
mechanism predates it), so removing the feature does not orphan any file or reference.
