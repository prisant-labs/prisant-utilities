---
id: D-07
title: "Implementation plan: Restore Waiting on You as an enforced blocker contract"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.4.0/plan_v0.4.0.md
ac-coverage: complete
phase-count: 5
---

# Implementation Plan: Restore Waiting on You as an enforced blocker contract

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Make it mechanically impossible for a session log's Waiting on You section to pass the Log Self-Check while diluted with optional items or missing an age signal, and stop blocked-since dates from resetting every wrap.

**Architecture:** Four small edits to two skills, all documented convention (no new scripts): tighten the definition and add two syntactic gates in `plab-wrap-session/SKILL.md`; add a carry-forward step to the same file's Evidence Gathering; add a Parked list and updated comments to `session-log-template.md`; sort the read-side display oldest-first in `plab-continue-session/references/handoff-display.md`. Both skills version-bump together because this changes the session-log format and its gates on both the write and read side, per the pairing contract both HISTORY.md files assert.

**Spec:** `spec.md`
**Target versions:** `plab-wrap-session` 1.6.0, `plab-continue-session` 1.4.0, shipping in plugin v0.4.0 alongside CI-01 (CI bootstrap), D-03 (bidirectional drift check), D-04 (capture-lite consumers), D-05 (superseding logs), D-06 (resumed-from semantics), D-11 (three-state gate canaries), and D-12 (path-citation precision).

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) in any file this touches. Use " - " or restructure.
- State the Waiting-on contract once, in `SKILL.md`'s definition (AC-1). The template comments and `handoff-display.md`'s description must reference or restate that same contract consistently, not invent their own wording, so the section is never defined two different ways in two files.
- Archive, never delete: not applicable to this effort directly, since it edits reference text rather than moving or removing session logs.
- Token economy: this effort adds no characters to any skill's `description:` frontmatter field. All new text lives in `SKILL.md` body content or `references/*.md`, paid only when the skill is invoked, never as always-on cost.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Tighten the Waiting-on definition and add two Log Self-Check gates | AC-1, AC-2, AC-3 | agent | Not started |
| P2 | Add the carry-forward Evidence Gathering step | AC-4, AC-8 | agent | Not started |
| P3 | Add the Parked list and update template comments | AC-6, AC-7 | agent | Not started |
| P4 | Sort the read-side display oldest-first | AC-5 | agent | Not started |
| P5 | Version bump and documentation coverage | (packaging for AC-1 through AC-8) | agent | Not started |

---

## Phase 1: Tighten the Waiting-on definition and add two Log Self-Check gates

**Goal:** `SKILL.md` states the tightened contract once, and the Log Self-Check can reject a log that violates it.
**Files:** Modify `skills/plab-wrap-session/SKILL.md`.
**Fulfills:** AC-1, AC-2, AC-3

**Steps:**
- [ ] Step 1: In `skills/plab-wrap-session/SKILL.md`, replace the Waiting on You bullet in Body Sections (Final Mode) (currently line 153) from:

  ```
  **Waiting on You** - Required in every mode. Every item blocked on the maintainer's decision or action, one bullet each: what is awaited, why it blocks, and links to the relevant files. Write "Nothing pending" explicitly when the list is empty; never omit the section. Mirror the list inside the continuation prompt so the next session re-presents it.
  ```

  to:

  ```
  **Waiting on You** - Required in every mode. Only items blocked on the maintainer's decision or action belong here, one bullet each: what is awaited, why it blocks, a `(blocked since YYYY-MM-DD)` marker, and links to the relevant files. Optional or nice-to-have items are not blockers; route them to What's Next or the Parked list instead. Write "Nothing pending" explicitly when the list is empty; never omit the section. Mirror the list inside the continuation prompt so the next session re-presents it.
  ```

- [ ] Step 2: In the same file's Log Self-Check list (currently lines 190-195, six bullets ending with "No em-dash or en-dash characters anywhere in the log"), add two bullets:

  ```
  - No Waiting on You item begins with "Optional"
  - Every Waiting on You item carries a `(blocked since YYYY-MM-DD)` marker
  ```

**Verification:** `grep -n "blocked since\|begins with \"Optional\"" skills/plab-wrap-session/SKILL.md` returns the new definition line and both new gate bullets. Manually confirm the Log Self-Check list now has eight bullets, not six.

---

## Phase 2: Add the carry-forward Evidence Gathering step

**Goal:** Wrap reads the previous log's Waiting on You section and carries unresolved items forward with their original dates, degrading sensibly when the previous log predates the marker.
**Files:** Modify `skills/plab-wrap-session/SKILL.md`.
**Fulfills:** AC-4, AC-8

**Steps:**
- [ ] Step 1: In `skills/plab-wrap-session/SKILL.md`'s Evidence Gathering list (currently 6 numbered items, lines 40-45), add a 7th item:

  ```
  7. Locate the previous session log using `plab-continue-session`'s newest-log selection rule (`references/log-discovery.md` in that skill), read its Waiting on You section, and carry forward items still applicable, preserving each item's original `(blocked since YYYY-MM-DD)` date. If the previous log predates this marker (no date to preserve), record the carried item as newly observed with today's date instead of fabricating one. If no previous log exists, skip this step; there is nothing to carry.
  ```

**Verification:** `grep -n "log-discovery.md\|Locate the previous session log" skills/plab-wrap-session/SKILL.md` returns the new step. Confirm it cites `plab-continue-session/references/log-discovery.md` rather than restating that file's selection algorithm, consistent with the existing cross-reference pattern at `SKILL.md:104`.

---

## Phase 3: Add the Parked list and update template comments

**Goal:** The template states the tightened contract in its own instructional comments and offers Parked as the named destination for demoted items.
**Files:** Modify `skills/plab-wrap-session/references/session-log-template.md`.
**Fulfills:** AC-6, AC-7

**Steps:**
- [ ] Step 1: In Final Mode, replace the Waiting on You comment (currently lines 75-78):

  ```
  <!-- REQUIRED in every mode. One bullet per item blocked on the maintainer:
    what is awaited, why it blocks, links to relevant files.
    Write "Nothing pending." explicitly when empty; never omit this section.
    Mirror the list inside the continuation prompt. -->
  ```

  with:

  ```
  <!-- REQUIRED in every mode. Only items blocked on the maintainer's decision or
    action belong here: what is awaited, why it blocks, a (blocked since YYYY-MM-DD)
    marker, and links to relevant files. Optional or nice-to-have items go in the
    Parked list below, never here.
    Write "Nothing pending." explicitly when empty; never omit this section.
    Mirror the list inside the continuation prompt. -->
  ```

- [ ] Step 2: Immediately after the Waiting on You block and before `## What's Next` in Final Mode, add:

  ```
  ## Parked

  <!-- Optional or nice-to-have context that does not meet the Waiting on You bar:
    smoke tests never run, cosmetic cleanups, ideas worth remembering but nobody
    is blocked on. One bullet each. Omit the section entirely when there is
    nothing to park. -->
  ```

- [ ] Step 3: In Quick Mode, replace the Waiting on You comment (currently line 123):

  ```
  [One bullet per item awaited from the maintainer with file links, or "Nothing pending."]
  ```

  with:

  ```
  [One bullet per item blocked on the maintainer, each with a (blocked since YYYY-MM-DD) marker and file links, or "Nothing pending." Optional items do not belong here.]
  ```

- [ ] Step 4: In Blocked Mode, replace the Waiting on You comment (currently line 165):

  ```
  [One bullet per item awaited from the maintainer with file links; the blocker itself belongs here when the maintainer is the unblocker.]
  ```

  with:

  ```
  [One bullet per item blocked on the maintainer, each with a (blocked since YYYY-MM-DD) marker and file links; the blocker itself belongs here when the maintainer is the unblocker. Optional items do not belong here.]
  ```

  Per spec Open Question D1, Quick and Blocked mode do not gain their own Parked section; only their Waiting-on comment tightens to match the same contract.

**Verification:** `grep -n "Parked\|blocked since" skills/plab-wrap-session/references/session-log-template.md` shows the new Parked heading once (Final Mode only) and the tightened comment language in all three mode blocks.

---

## Phase 4: Sort the read-side display oldest-first

**Goal:** `plab-continue-session` presents Waiting-on items oldest first, and its display contract explicitly accounts for the new Parked section rather than leaving it undocumented.
**Files:** Modify `skills/plab-continue-session/references/handoff-display.md`.
**Fulfills:** AC-5

**Steps:**
- [ ] Step 1: Replace the "Waiting on you" bullet under "### Waiting on you" section description (currently line 15):

  ```
  <bullets from `## Waiting on You`, links intact, or "Nothing pending." Lead with these: they are the maintainer's open obligations. If the log predates the section (pre-1.3.0 wrap), say so instead of fabricating a list.>
  ```

  with:

  ```
  <bullets from `## Waiting on You`, sorted oldest-blocked-first by each item's `(blocked since YYYY-MM-DD)` marker, links intact, or "Nothing pending." Lead with these: they are the maintainer's open obligations. If an item predates this marker (pre-1.6.0 wrap), display it last, unordered, rather than guessing its age. If the log predates the section entirely (pre-1.3.0 wrap), say so instead of fabricating a list.>
  ```

- [ ] Step 2: In the "What to elide" list (currently lines 41-46), add a bullet so the new Parked section is accounted for rather than left silently undocumented:

  ```
  - The `## Parked` list (optional context; read the log directly if wanted)
  ```

**Verification:** `grep -n "oldest-blocked-first\|Parked" skills/plab-continue-session/references/handoff-display.md` returns both edits. Manually confirm the "What to elide" list now has five bullets, not four.

---

## Phase 5: Version bump and documentation coverage

**Goal:** Both skills ship at their v0.4.0 versions with accurate HISTORY, manifest, and human-facing version references.
**Files:** Modify `skills/plab-wrap-session/SKILL.md`, `skills/plab-continue-session/SKILL.md`, `skills/plab-wrap-session/HISTORY.md`, `skills/plab-continue-session/HISTORY.md`, `library.json`, `README.md`, `CHANGELOG.md`.
**Fulfills:** Packaging for AC-1 through AC-8 (no single AC maps to this phase; it ships the release artifacts for all of them).

**Steps:**
- [ ] Step 1: `skills/plab-wrap-session/SKILL.md` frontmatter: `version: "1.5.0"` to `version: "1.6.0"`; bump `updated:` to the ship date.
- [ ] Step 2: `skills/plab-continue-session/SKILL.md` frontmatter: `version: "1.3.0"` to `version: "1.4.0"`; bump `updated:` to the ship date.
- [ ] Step 3: `skills/plab-wrap-session/HISTORY.md`: add a `1.6.0` row to the table and a matching section describing the tightened Waiting-on contract, the two new gates, and the carry-forward step. If another effort in this same v0.4.0 release has already opened a `1.6.0` entry, add this effort's paragraph to it rather than creating a duplicate entry.
- [ ] Step 4: `skills/plab-continue-session/HISTORY.md`: add a `1.4.0` row and section describing the oldest-first sort and the Parked-list elision. Same duplicate-entry check as Step 3.
- [ ] Step 5: `library.json`: bump the `plab-wrap-session` component version (currently line 32) to `1.6.0` and the `plab-continue-session` component version (currently line 39) to `1.4.0`.
- [ ] Step 6: Root `README.md`: bump the version-table entries (currently lines 11-12) to `1.6.0` and `1.4.0`.
- [ ] Step 7: `CHANGELOG.md`: add an entry under `[Unreleased]` (or a new `v0.4.0` heading if the release has been cut by the time this lands) describing the tightened Waiting-on contract in plain-English, user-facing terms: what a diluted list looked like before, what it looks like now, and that Parked is the new home for optional context.

**Verification:** `grep -rn "1.6.0\|1.4.0" skills/plab-wrap-session/SKILL.md skills/plab-continue-session/SKILL.md library.json README.md` shows consistent version strings across all four files. `grep -c "^| 1\." skills/plab-wrap-session/HISTORY.md skills/plab-continue-session/HISTORY.md` confirms exactly one new table row was added per file, not a duplicate.

---

## CI and Documentation Coverage

### CI

No CI change; the repository has no `.github/` directory (greenfield, per conventions section 10). This effort is verified by the two new Log Self-Check gates it adds (AC-2, AC-3), which run inside the wrapping agent's own self-check pass before writing a log, exactly like the six gates already there.

Mechanization ladder rung: **rung 3** (documented convention, enforced by the agent's own self-check each session), the same rung as the four existing structural gates it joins. This is not a rung-1 CI check, and it does not need D-11's three-state canary discipline: D-11 scopes canary/broken-state verification specifically to the two gates in this list that are backed by a text-matching detector (the em-dash sweep and the path-existence check). The two gates this effort adds are structural assertions a reader (or the agent re-reading its own draft) can verify by looking, the same shape as "Waiting on You section present in every mode" or "Summary is 120 characters or fewer" - adding canary ceremony to them would be theater, per D-11's own scoping note.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: Waiting on You definition tightened (AC-1); two new Log Self-Check gates (AC-2, AC-3); new Evidence Gathering step 7 (AC-4, AC-8); `metadata.version` bumped to 1.6.0.
- `skills/plab-wrap-session/references/session-log-template.md`: Waiting on You comment updated in all three mode blocks (AC-6); new Parked section in Final Mode (AC-7).
- `skills/plab-continue-session/references/handoff-display.md`: oldest-first sort and pre-schema fallback (AC-5); Parked added to "What to elide".
- `skills/plab-wrap-session/HISTORY.md`, `skills/plab-continue-session/HISTORY.md`: new version entries recording all of the above.

These are runtime configuration the agent reads at invocation. A stale line here poisons every future wrap or resume, so every edit above must match what Phases 1-4 actually shipped, not what was planned.

### Human-facing documentation

- `docs/skills/plab-wrap-session/README.md`: the Waiting on You table row (currently line 83, "Everything blocked on the maintainer, with reasons and file links; 'Nothing pending.' when empty") gains the blocked-since requirement; the Output Shape table row (currently line 166) gets the same addition; a new row or note documents the Parked section using the same pattern.
- `docs/skills/plab-continue-session/README.md`: no change required to the Phase 3 worked example (currently lines 100-101), which already shows a Waiting-on item in the `(blocked since YYYY-MM-DD)` shape this effort formalizes [S7 in spec.md]. The Phase 2 field-extraction description (currently line 87) may note that `## Parked` is read but not surfaced in the resumption display, matching `handoff-display.md`'s elision list.
- Root `README.md`: version-table entries updated to 1.6.0 and 1.4.0.
- `CHANGELOG.md`: `[Unreleased]` entry in plain English: a reader away for three months should understand that Waiting on You now enforces a real contract instead of accepting anything, and that optional context has a new home (Parked) instead of being silently dropped or smuggled into the blockers list.

## Rollback

Every edit in this effort is a same-file text change to `SKILL.md`, `session-log-template.md`, and `handoff-display.md`, plus routine version/HISTORY bookkeeping; reverting the commit that ships this effort restores prior behavior exactly, with no data migration to undo. If the two new gates and tightened definition (Phase 1) prove correct but carry-forward (Phase 2) misbehaves in practice (see spec Open Question D2, "how does the agent judge 'still applicable'"), Phase 2 can be reverted independently: an agent can still hand-write correctly dated, correctly scoped Waiting-on items without automated carry-forward, it simply loses cross-session date persistence, which is the one deliberate ceremony cost this spec already names. Nothing in this effort deletes or archives a session log, so the archive-never-delete constraint is not implicated.
