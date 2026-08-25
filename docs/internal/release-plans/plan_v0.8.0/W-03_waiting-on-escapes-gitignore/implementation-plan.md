---
id: W-03
title: "Implementation plan: Waiting-on items escape the gitignored log via offered GitHub issues"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.8.0/plan_v0.8.0.md
ac-coverage: complete
phase-count: 4
---

# Implementation Plan: Waiting-on items escape the gitignored log via offered GitHub issues

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Let a wrap offer, under per-item confirmation, to promote a carried-forward Waiting-on item
into a GitHub issue, so a blocker that was only ever a diary entry gains a URL, a state, and a history.

**Architecture:** The mechanism adds one offer step to the existing hygiene sweep flow in
`plab-wrap-session`'s `SKILL.md` and reuses `hygiene-sweep.md`'s Resolution protocol verbatim rather
than defining a new one. Promotion touches four surfaces: the offer/confirm step itself, the
`gh issue create` content template and its current-repository default, the post-promotion bullet
rewrite that lets D-07's carry-forward step recognize and skip already-promoted items, and the
version/documentation bookkeeping this release requires. Because this effort ships in v0.8.0, after
three intervening releases (v0.5.0 through v0.7.0) will already have changed the files it touches,
step-by-step detail below is deliberately light: phases name the goal, the files, and the verification
each phase owes, and the exact edit is decided against the code as it exists when this plan executes.

**Spec:** `spec.md`

**Target versions:** `plab-wrap-session` 1.9.0 (functional changes). `plab-continue-session` 1.8.0
(version bump only, required by the pairing contract whenever the log format changes; this effort
requires no functional change to continue's own `SKILL.md` or references, confirmed in Phase 3).
Plugin 0.8.0.

**Global constraints:** No em-dash or en-dash characters anywhere, in code, comments, or docs; use
" - " or restructure. State a contract once in one named file and have everything else cite it, never
restate a rule in different words in two places; this effort cites `hygiene-sweep.md`'s Resolution
protocol rather than duplicating it. Archive, never delete; dry-run by default; per-action confirmation
for anything that touches the world, which for this effort means no `gh issue create` runs without an
explicit per-item "y". No skill-description growth.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Add the promotion-offer step to the wrap flow | AC-1, AC-2, AC-6 | agent | Not started |
| P2 | Define issue content and the current-repo default | AC-3 | agent | Not started |
| P3 | Post-promotion bullet rewrite and carry-forward exclusion | AC-4, AC-5 | agent | Not started |
| P4 | Version bump and documentation | N/A | agent | Not started |

---

## Phase 1: Add the promotion-offer step to the wrap flow

**Goal:** Give the wrap a step, gated to deep/final mode, that walks the carried-forward Waiting-on
list and proposes promotion per item using the existing Resolution protocol, degrading silently when
`gh` is unavailable.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md` (add the step under or adjacent to the Pre-Wrap Hygiene
  Sweep section, after D-07's carry-forward step has produced the list to offer against)
- Modify: `skills/plab-wrap-session/references/hygiene-sweep.md` (name the new proposal's shape and
  the degradation rule alongside the existing check catalog, matching how Check 5 was added in 1.5.0)

**Fulfills:** AC-1, AC-2, AC-6

**Steps:**
- [ ] Step 1: Read the shipped v0.4.0 state of D-07's carry-forward step in `SKILL.md` and decide
      where the promotion offer attaches in the actual flow at execution time.
- [ ] Step 2: Add the offer step, citing `hygiene-sweep.md`'s Resolution protocol by reference rather
      than restating it, gated to deep/final mode only.
- [ ] Step 3: Add the `gh`-unavailable degradation path and its Hygiene Sweep note.
- [ ] Step 4: Update `hygiene-sweep.md` with the new proposal's shape and the degradation rule.

**Verification:** `grep -n "gh issue create\|promot" skills/plab-wrap-session/SKILL.md
skills/plab-wrap-session/references/hygiene-sweep.md` returns matches in both files. Manually author a
fixture log carrying one D-07-style Waiting-on item and walk the new step's text against it; confirm
the resulting proposal matches AC-1's shape (one item, y/n, nothing adjacent executed).

---

## Phase 2: Define issue content and the current-repo default

**Goal:** Specify exactly what `gh issue create` sends: title, body (blocked-since date, linked files,
raising log's filename), and the current-repository default per `plan_v0.8.0.md`'s open D2.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md` (issue content template; current-repository default
  statement; a one-line pointer to `plan_v0.8.0.md`'s D2 for future revision)

**Fulfills:** AC-3

**Steps:**
- [ ] Step 1: Draft the issue title and body template: item text, blocked-since date, linked files,
      and the raising log's filename.
- [ ] Step 2: State the current-repository default explicitly, with the pointer to D2.
- [ ] Step 3: Confirm the template cites the session log by filename only, never a directory-qualified
      path, per the existing rule.

**Verification:** Walk `spec.md`'s Walkthrough 1 example against the drafted template and confirm
every named field has a slot. `grep -n "filename" skills/plab-wrap-session/SKILL.md` shows the
template citing the log by filename, matching `frontmatter-schema.md:100`'s existing rule (verified
this session).

---

## Phase 3: Post-promotion bullet rewrite and carry-forward exclusion

**Goal:** Make a promoted item's bullet collapse to a short issue reference in the log being written,
and make D-07's carry-forward step recognize and skip already-promoted items on the next wrap.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md` (D-07's carry-forward step: add the recognize-and-skip
  rule)
- Modify: `skills/plab-wrap-session/references/session-log-template.md` (Waiting on You section
  comment: note the short-reference shape for promoted items)
- Read only, no edit expected: `skills/plab-continue-session/references/handoff-display.md` (confirm
  its existing verbatim bullet mirror already covers a promoted item's shortened bullet; state that
  confirmation in the file's own terms if a maintainer reading it later would otherwise wonder)

**Fulfills:** AC-4, AC-5

**Steps:**
- [ ] Step 1: Define the exact short-reference string shape (spec.md's OQ-2 leaves this open;
      resolve it here against the codebase as it exists at execution time).
- [ ] Step 2: Add the bullet-rewrite instruction to the promotion-offer step from Phase 1.
- [ ] Step 3: Add the recognize-and-skip rule to D-07's carry-forward step.
- [ ] Step 4: Add the template comment noting the short-reference shape.
- [ ] Step 5: Confirm `handoff-display.md` needs no functional edit; if it does turn out to need one
      once read against the then-current file, make it here rather than opening a second phase.

**Verification:** Author two fixture logs, log A containing a promoted item's short-reference bullet
and log B wrapped as if resuming from A. Read the updated `SKILL.md` carry-forward text against that
pair and confirm it does not reproduce log A's original full item text in log B's Waiting on You
section.

---

## Phase 4: Version bump and documentation

**Goal:** Ship the version and documentation bookkeeping this release requires, per `plan_v0.8.0.md`'s
Doc-Update Checklist.

**Files:** `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `library.json`,
`manifest.generated.json`, `skills/plab-wrap-session/SKILL.md` frontmatter,
`skills/plab-wrap-session/HISTORY.md`, `skills/plab-continue-session/HISTORY.md`,
`docs/skills/plab-wrap-session/README.md`, root `README.md`, `CHANGELOG.md`.

**Fulfills:** N/A (release bookkeeping; no acceptance criterion names a version number)

**Steps:**
- [ ] Step 1: Bump `plab-wrap-session` to 1.9.0 everywhere its version is declared.
- [ ] Step 2: Bump `plab-continue-session` to 1.8.0 everywhere its version is declared; its
      `HISTORY.md` entry states the bump is contractual, with no functional change from this effort.
- [ ] Step 3: Bump both `plugin.json` manifests and `library.json` to 0.8.0, then regenerate
      `manifest.generated.json` from `library.json`.
- [ ] Step 4: Write the `HISTORY.md` entries and the `CHANGELOG.md` `[0.8.0]` section describing the
      promotion offer.
- [ ] Step 5: Update `docs/skills/plab-wrap-session/README.md` and the root `README.md` skill table
      version columns.

**Verification:** `grep -rn "\"version\"" .claude-plugin/plugin.json .codex-plugin/plugin.json
library.json` shows `0.8.0` for the plugin and `1.9.0` / `1.8.0` for the two components.
`grep -n "1.9.0" skills/plab-wrap-session/HISTORY.md docs/skills/plab-wrap-session/README.md
README.md` returns a match in each.

---

## CI and Documentation Coverage

### CI

No CI change from this effort. The repository's CI, established by CI-01 in v0.4.0, verifies
conformance and structure, not this effort's prose behavior; this effort is verified by the manual
walkthroughs named per phase above, mechanization-ladder rung 3 (documented convention), the same rung
the hygiene sweep's existing checks occupy. This effort adds no detector, so no canary obligation
applies.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: new promotion-offer step, issue content template, carry-forward
  recognize-and-skip rule, `version` frontmatter bump.
- `skills/plab-wrap-session/references/hygiene-sweep.md`: new proposal shape and degradation rule
  alongside the existing check catalog.
- `skills/plab-wrap-session/references/session-log-template.md`: Waiting on You section comment
  updated for the short-reference shape.
- `skills/plab-continue-session/references/handoff-display.md`: no functional edit expected; Phase 3
  records the confirmation explicitly so a future reader does not wonder whether this was overlooked.
- `AGENTS.md`: no change expected; this effort adds no new trigger phrase or skill.

### Human-facing documentation

- `skills/plab-wrap-session/HISTORY.md` and `skills/plab-continue-session/HISTORY.md`: version-table
  rows plus narrative entries for 1.9.0 and 1.8.0 (continue's entry states its bump is contractual).
- `docs/skills/plab-wrap-session/README.md`: describe the promotion offer for a human reader; version
  line bump.
- Root `README.md`: skill table version column bump for both skills.
- `CHANGELOG.md`: `[0.8.0]` entry.
- The mechanical version-bump rows across `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
  `library.json`, and `manifest.generated.json` are `plan_v0.8.0.md`'s Doc-Update Checklist rows; this
  plan does not restate that table, only the effort-specific content changes listed above it.

---

## Rollback

Revert the `SKILL.md` and reference-file edits in `plab-wrap-session` and roll both version numbers
back. Nothing this effort creates is destructive to existing data: declined and skipped promotions
leave the log format exactly as D-07 already produces it, and any GitHub issue already created by an
approved promotion is left in place, not auto-deleted by the rollback; closing it is the maintainer's
own out-of-band call, matching the Reversibility NFR in `spec.md`.
