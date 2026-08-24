---
id: D-04
title: "Implementation plan: Consume capture-lite records in wrap and continue"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.3.0/plan_v0.3.0.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: Consume capture-lite records in wrap and continue

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Give `plab-wrap-session` an unwrapped-session count from capture-lite records, and give
`plab-continue-session` a capture-lite orientation line on its no-log-found and stale-log paths, both
degrading silently when the capture store is absent.

**Architecture:** Two independent read-only consumers of an existing, unmodified producer. (1) Wrap's
Evidence Gathering reads the capture store's `.jsonl` files, filters by timestamp and a non-null
`session_id`, and reports into the existing Outstanding Issues section, never Hygiene Sweep. (2)
Continue's `log-discovery.md` reads the same store on its no-log-found and age-warning paths and
surfaces one orientation line. Neither consumer adds a script, grows a description, or documents more
than five field names from the hook's schema.

**Spec:** `spec.md`

**Target versions:** `plab-wrap-session` 1.6.0, `plab-continue-session` 1.4.0. Plugin-level version
(`library.json` top field, both `plugin.json` files) stays at 0.2.0 through this effort; that bump is
a release-level action gated by all eight v0.3.0 efforts completing (`plan_v0.3.0.md` Hygiene Gate
(f)), not something any single effort's plan performs.

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) anywhere. Use " - " or restructure. A PreToolUse hook
  blocks the write.
- State a contract once. The capture-lite trigger logic for continue's two paths lives once, in the
  new `log-discovery.md` subsection; the existing "no log found" and "age warning" sections gain only
  a one-line forward pointer, never a restatement.
- The unwrapped-session report belongs in Outstanding Issues, never Hygiene Sweep. Hygiene Sweep is
  defined as findings from the pre-wrap sweep specifically; putting a non-sweep fact there would make
  that definition false.
- Reference only these five capture-lite field names, anywhere in either skill's public text: `ts`,
  `head`, `session_id`, `branch`, `commits_today`. Do not add `harness`, `reason`, `last_tag`,
  `transcript`, `dirty`, `untracked`, or `stashes`.
- No new script. No `description:` frontmatter growth on either skill.
- If another v0.3.0 effort (most likely D-05) has already added a numbered item to wrap's Evidence
  Gathering list by the time this plan executes, add this effort's item as the next available number,
  not a hard-coded "7". Same create-or-append rule for the shared `## 1.6.0` / `## 1.4.0` HISTORY.md
  headings as the sibling D-05 and D-06 plans use.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Wrap-side capture consumption | AC-1, AC-2, AC-3 | agent | Not started |
| P2 | Continue-side capture consumption | AC-4, AC-5, AC-6 | agent | Not started |
| P3 | Repo bookkeeping and AC-7 field-minimality verification | AC-7 | agent | Not started |

---

## Phase 1: Wrap-side capture consumption

**Goal:** Wrap reports the count of unwrapped sessions since the last log, and their head range, in
Outstanding Issues, only when qualifying capture records exist.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md`
- Modify: `skills/plab-wrap-session/HISTORY.md`

**Fulfills:** AC-1, AC-2, AC-3

**Steps:**

- [ ] Step 1: Add a new numbered item to `## Evidence Gathering` (after the existing item 6 and before
  the closing "If git is unavailable..." sentence). Renumber to the next available integer if a
  sibling effort already added an item 7 this release (see Global constraints):

  ```markdown
  7. In deep and final modes, when `_local/_session-logs/_capture/` exists, read its `.jsonl` files
     (there may be more than one) and filter to records with a non-null `session_id` and a `ts` after
     the newest existing log's filename timestamp (see `references/log-discovery.md` for the
     newest-wins sort; if no existing log exists, every qualifying record counts). If any remain, note
     the count and the earliest-to-latest `head` for Outstanding Issues below. Say nothing if the
     directory is absent or nothing qualifies.
  ```

- [ ] Step 2: Append one clause to the **Outstanding Issues** bullet under
  `### Body Sections (Final Mode)` (the line reading "**Outstanding Issues** - Blockers, risks,
  unfinished work."):

  ```markdown
  **Outstanding Issues** - Blockers, risks, unfinished work, including any sessions since the last log
  that were never wrapped (from capture-lite records, when present; see Evidence Gathering above).
  ```

- [ ] Step 3: Bump wrap's frontmatter, if not already at this value from a sibling effort:

  ```yaml
  metadata:
    version: "1.6.0"
    updated: 2026-08-23
  ```

- [ ] Step 4: Add (or append to, if present) the `## 1.6.0` section in
  `skills/plab-wrap-session/HISTORY.md`, same create-or-append rule as the sibling D-05 and D-06 plans.

  Paragraph to add under `## 1.6.0 - 2026-08-23`:

  ```markdown
  **Added: capture-lite consumption, wrap side (D-04).** In deep and final modes, when
  `_local/_session-logs/_capture/` holds `.jsonl` records newer than the last existing log, Outstanding
  Issues now states how many sessions since then were never wrapped, with the earliest-to-latest head.
  Records with a null `session_id` are skipped. Silent when the directory is absent or nothing
  qualifies. No new script; the hook itself lives outside this repository, under the user's home
  directory.
  ```

**Verification:**

```bash
grep -n "capture" skills/plab-wrap-session/SKILL.md
```
Expected: the new Evidence Gathering item and the Outstanding Issues clause both appear.

```bash
grep -n "1.6.0" skills/plab-wrap-session/SKILL.md skills/plab-wrap-session/HISTORY.md
```
Expected: version in both files.

---

## Phase 2: Continue-side capture consumption

**Goal:** Continue surfaces one capture-lite orientation line on the no-log-found path and the
stale-log path, only when qualifying records exist.

**Files:**
- Modify: `skills/plab-continue-session/references/log-discovery.md`
- Modify: `skills/plab-continue-session/SKILL.md` (frontmatter version only)
- Modify: `skills/plab-continue-session/HISTORY.md`

**Fulfills:** AC-4, AC-5, AC-6

**Steps:**

- [ ] Step 1: Add a new subsection to `log-discovery.md`, after "## Age warning" and before
  "## Repo / branch mismatch":

  ```markdown
  ## Capture-lite orientation (when present)

  On the no-log-found branch above, and on the age-warning path, check whether
  `_local/_session-logs/_capture/` exists and its `.jsonl` files hold any record with a non-null
  `session_id` newer than the relevant boundary: no existing log at all for the no-log-found case, or
  the stale log's date for the age-warning case. If so, surface one line before the existing message:
  the most recent qualifying record's `branch`, `head`, `commits_today`, and `ts` for the no-log case,
  or the count of such records since the stale log for the age-warning case. Say nothing when the
  directory is absent or nothing qualifies; the hook is optional machine-local infrastructure and this
  store may not exist at all.
  ```

- [ ] Step 2: At the end of "## Empty or missing directory" (before "## Age warning" begins), add one
  forward-pointer sentence:

  ```markdown
  If `_local/_session-logs/_capture/` holds any qualifying record, surface it first; see
  "Capture-lite orientation" below.
  ```

- [ ] Step 3: At the end of "## Age warning" (before "## Repo / branch mismatch" begins), add one
  forward-pointer sentence:

  ```markdown
  Also check `_local/_session-logs/_capture/` for records since this log; see "Capture-lite
  orientation" below.
  ```

- [ ] Step 4: Bump continue's frontmatter, only if no sibling v0.3.0 effort (most likely D-05) has
  already bumped it this release:

  ```yaml
  metadata:
    version: "1.4.0"
    updated: 2026-08-23
  ```

- [ ] Step 5: Add (or append to, if present) the `## 1.4.0` section in
  `skills/plab-continue-session/HISTORY.md`, same create-or-append rule as Phase 1 Step 4.

  Paragraph to add under `## 1.4.0 - 2026-08-23`:

  ```markdown
  **Added: capture-lite orientation, continue side (D-04).** On the no-log-found path and the
  stale-log (7+ day) path, when `_local/_session-logs/_capture/` holds qualifying records, continue
  now surfaces one orientation line, branch, head, commits today, and timestamp for the no-log case, or
  a count for the stale-log case, before its existing message. Silent when the directory is absent or
  nothing qualifies.
  ```

**Verification:**

```bash
grep -n "Capture-lite orientation\|capture" skills/plab-continue-session/references/log-discovery.md
```
Expected: the new subsection heading and both forward-pointer sentences appear.

```bash
grep -n "1.4.0" skills/plab-continue-session/SKILL.md skills/plab-continue-session/HISTORY.md
```
Expected: version in both files.

---

## Phase 3: Repo bookkeeping and AC-7 field-minimality verification

**Goal:** Record the change in the places a reader looks, and confirm no forbidden capture-lite field
name was introduced.

**Files:**
- Modify: `library.json` (component versions only)
- Modify: `docs/skills/plab-wrap-session/README.md`
- Modify: `docs/skills/plab-continue-session/README.md`
- Modify: `README.md` (skill table)
- Modify: `CHANGELOG.md` ([Unreleased])

**Fulfills:** AC-7

**Steps:**

- [ ] Step 1: In `library.json`, set `components.skills[plab-wrap-session].version` to `"1.6.0"` and
  `components.skills[plab-continue-session].version` to `"1.4.0"`, if not already at those values from
  a sibling effort. Do not change the top-level `version` field.

- [ ] Step 2: In `docs/skills/plab-wrap-session/README.md`, update the `**Version:**` line to `1.6.0`
  and add one sentence near the Evidence Gathering or Outstanding Issues description noting the
  capture-lite count, cross-referencing the skill body rather than restating its logic.

- [ ] Step 3: In `docs/skills/plab-continue-session/README.md`, update the `**Version:**` line to
  `1.4.0` and add one sentence to the "How It Works" or Safety Checks section noting the capture-lite
  orientation line, cross-referencing `references/log-discovery.md`.

- [ ] Step 4: In root `README.md`'s skill table, bump the Version column for `plab-wrap-session` to
  `1.6.0` and `plab-continue-session` to `1.4.0`, if not already bumped by a sibling effort.

- [ ] Step 5: Add a bullet under `CHANGELOG.md`'s `[Unreleased]` heading (`### Added`):

  ```markdown
  - `plab-wrap-session` 1.6.0 and `plab-continue-session` 1.4.0: capture-lite records are now read,
    not just written. Wrap reports unwrapped sessions since the last log in Outstanding Issues;
    continue surfaces a one-line orientation on its no-log-found and stale-log paths. Both are silent
    when the capture store is absent.
  ```

- [ ] Step 6: Verify AC-7 directly:

  ```bash
  grep -n '`harness`\|`reason`\|`last_tag`\|`transcript`\|`dirty`\|`untracked`\|`stashes`' skills/plab-wrap-session/SKILL.md skills/plab-continue-session/references/log-discovery.md
  ```
  Expected: no output. If this produces a match, a forbidden field name was introduced somewhere in
  this plan's execution and must be removed; re-read spec.md's Requirement 7 and Non-Goals.

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
or move any `.github/workflows/` file. CI-01 (a separate v0.3.0 effort) gives this repository
continuous integration for the first time; once it lands, this effort's changes are graded like
everything else by the toolkit's `check.mjs` gate at Universal tier. The consumption logic itself is
mechanization-ladder rung 3, a documented convention the agent follows each session, not a rung-1
deterministic check. The field-minimality mitigation (spec Requirement 7, AC-7) is explicitly **not**
a standing gate: the source states the mitigation is field discipline, not built validation, because
both the hook and the skills share one owner. Phase 3 Step 6's grep is a one-time verification run
during implementation, not a check this plan wires into CI or into either skill's Log Self-Check.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: new Evidence Gathering item, Outstanding Issues clause, version
  bump (Phase 1).
- `skills/plab-wrap-session/HISTORY.md`: 1.6.0 entry (Phase 1).
- `skills/plab-continue-session/references/log-discovery.md`: new "Capture-lite orientation"
  subsection and two forward-pointer sentences (Phase 2).
- `skills/plab-continue-session/SKILL.md`: version bump only, no behavioral text changes (Phase 2).
- `skills/plab-continue-session/HISTORY.md`: 1.4.0 entry (Phase 2).

### Human-facing documentation

- `docs/skills/plab-wrap-session/README.md`: version line, one new sentence (Phase 3).
- `docs/skills/plab-continue-session/README.md`: version line, one new sentence (Phase 3).
- `README.md`: skill table version bump for both skills (Phase 3).
- `CHANGELOG.md`: `[Unreleased]` bullet (Phase 3).
- `library.json`: component versions only (Phase 3). The top-level plugin version and both
  `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` files are deliberately **not** touched by
  this plan; that bump, and the `manifest.generated.json` regeneration it triggers, is a release-level
  action gated by all eight v0.3.0 efforts completing (`plan_v0.3.0.md` Hygiene Gate (f)), performed
  once at tag time rather than once per effort.

---

## Rollback

Both consumers are read-only: neither writes, moves, or deletes any file, including inside the
capture store itself. Reverting this effort is a pure text revert of the SKILL.md and reference-file
diffs from Phases 1 and 2, plus the version and HISTORY bumps. No data migration is needed in either
direction: the capture store is untouched by this effort regardless of whether it ships or is rolled
back, since both consumers only ever read it.
