---
id: D-10
title: "Implementation plan: Make derive-log-facts.py's output the single log-format contract"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.6.0/plan_v0.6.0.md
ac-coverage: complete
phase-count: 5
---

# Implementation Plan: Make derive-log-facts.py's output the single log-format contract

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Make every document that restates the wrap/continue session-log format defer to `derive-log-facts.py`'s actual output for the fields it derives, and delete the prose that used to restate them independently.

**Architecture:** This plan is pure documentation and reference-file consolidation: no new code, no new script, no CI change. Every phase either deletes duplicated prose and replaces it with a pointer, or moves an assertion from several files down to one. Step-level detail is deliberately lighter than a v0.4.0 or v0.5.0 plan would carry, per the conventions' own depth-scaling rule for this release band, for two reasons: the exact line numbers in every touched file will have moved by execution time (W-02 changes `SKILL.md`, and, upstream of that, v0.4.0's D-11, D-12, and D-7 and v0.5.0's C-02 and C-03 will already have changed continue's files before this effort's turn), and the corrective text itself, what each pointer actually says, is better drafted against the real file content at execution time than pre-written now against a state that will already be stale.

**Spec:** `spec.md`

**Target versions:** `plab-continue-session` 1.6.0; plugin v0.6.0. `plab-wrap-session` is unaffected by this plan; it is already at 1.7.0 from W-02 by the time this effort runs.

**Global constraints:**
- No em-dashes (U+2014) or en-dashes (U+2013) anywhere in any file this plan touches. Use " - " or restructure.
- State a contract once, in one named file. This is the entire point of this effort, not an incidental rule to remember.
- This plugin is built for its one maintainer. No configurability for hypothetical third-party users.
- This effort stays at mechanization-ladder rung 3 (documented convention) deliberately; it does not add a new rung-1 or rung-2 check. See spec Non-Goal 3 and Open Questions item D3 for why.
- Archive, never delete; dry-run by default; per-action confirmation for anything that touches the world. Not directly triggered here (this plan edits tracked, reviewable documentation files, not destructive operations), but no step in this plan should introduce a write path that skips review.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Confirm W-02 has shipped, then consolidate `frontmatter-schema.md` and `session-log-template.md` | AC-7, AC-1, AC-2 | agent | Not started |
| P2 | Consolidate continue's Phase 2 and `handoff-display.md` | AC-4 | agent | Not started |
| P3 | Consolidate both skills' human-facing docs READMEs | AC-3, AC-6 | agent | Not started |
| P4 | Consolidate the versioned-together pairing claim | AC-5 | agent | Not started |
| P5 | Version bump and release bookkeeping for continue 1.6.0 | N/A - release hygiene | agent | Not started |

---

## Phase 1: Gate check, then frontmatter-schema.md and session-log-template.md

**Goal:** Confirm W-02 has shipped, then make `frontmatter-schema.md` and `session-log-template.md` defer to `derive-log-facts.py` for every field it produces.

**Files:** Modify `skills/plab-wrap-session/references/frontmatter-schema.md`, `skills/plab-wrap-session/references/session-log-template.md`.

**Fulfills:** AC-7, AC-1, AC-2

**Steps:**
- [ ] Step 1: Confirm `skills/plab-wrap-session/scripts/derive-log-facts.py` exists and `SKILL.md`'s Evidence Gathering section references it. Stop and report if either is missing; this is AC-7's gate, not a step to skip.
- [ ] Step 2: In `frontmatter-schema.md`, for each field the script produces, replace the "How to Derive" cell's hand-written method with a pointer to the script; leave the tiering rationale and the rows for agent-authored fields unchanged.
- [ ] Step 3: Fix or remove the Example Frontmatter block so it no longer omits `type` and `machine` relative to its own Tier 1 table.
- [ ] Step 4: In `session-log-template.md`, replace the "# hostname"-style inline comments (three per-mode occurrences, one each in Final, Quick, and Blocked mode) with a comment pointing at the script, for every field the script produces.

**Verification:** `grep -rn hostname skills/plab-wrap-session/references/` returns no matches. The Example Frontmatter block, read directly, includes `type:` and `machine:`, or no longer exists as independent prose.

---

## Phase 2: Continue's Phase 2 and handoff-display.md

**Goal:** Make continue's Phase 2 and `handoff-display.md` defer to the same contract instead of hand-enumerating fields.

**Files:** Modify `skills/plab-continue-session/SKILL.md`, `skills/plab-continue-session/references/handoff-display.md`.

**Fulfills:** AC-4

**Steps:**
- [ ] Step 1: Rewrite Phase 2's "Extract from frontmatter:" line to name the reference it defers to instead of hand-listing fields, following the deferral pattern already shipped at `skills/plab-wrap-session/SKILL.md:104`.
- [ ] Step 2: Check `handoff-display.md` for the same pattern and apply the same fix if found.
- [ ] Step 3: Confirm the corrected field set actually includes every Tier 1 field; `type`, `machine`, and `files-changed` were the three missing before this effort.

**Verification:** Read Phase 2 after the edit and confirm no independently maintained field list remains that could drift from `frontmatter-schema.md` a second time.

---

## Phase 3: Human-facing docs READMEs

**Goal:** Make both skills' `docs/skills/*/README.md` defer instead of re-describing the contract.

**Files:** Modify `docs/skills/plab-wrap-session/README.md`, `docs/skills/plab-continue-session/README.md`.

**Fulfills:** AC-3, AC-6

**Steps:**
- [ ] Step 1: Remove every "18-field" instance in `docs/skills/plab-wrap-session/README.md` (three at the time this spec was written); replace with a pointer to the canonical reference rather than a new hardcoded count.
- [ ] Step 2: Rewrite the Tier table and the "Output Shape" table so they reference `SKILL.md`'s Body Sections prose and `frontmatter-schema.md` instead of independently re-describing every field and section a second time.
- [ ] Step 3: Check `docs/skills/plab-continue-session/README.md` for the same pattern (field lists, pairing-relationship prose) and apply the same fix where found.

**Verification:** `grep -rn "18-field" skills/ docs/skills/ README.md CHANGELOG.md` returns zero matches. This scope deliberately excludes `docs/internal/release-plans/`, where D-10's own spec and plan name the stale string as the thing being removed; a repo-wide grep would never pass once those documents exist. Confirm the same command currently returns the three known matches in `docs/skills/plab-wrap-session/README.md` before this phase, and zero after.

---

## Phase 4: The versioned-together pairing claim

**Goal:** Consolidate the pairing claim to one file.

**Files:** Modify `skills/plab-continue-session/HISTORY.md`, `README.md` (repository root).

**Fulfills:** AC-5

**Steps:**
- [ ] Step 1: Decide which of the two locations keeps the assertion (root README's install-facing framing, "versioned and released together," or continue's HISTORY.md provenance framing, "move and version together") and remove it from the other, replacing the removed copy with a cross-reference. Keep the surviving location's wording exactly as it already reads; do not invent a third phrasing, since the verification below checks for the two existing wordings by name.
- [ ] Step 2: Re-check `skills/plab-wrap-session/HISTORY.md` to confirm it still does not carry a third copy. The task briefing's "both HISTORY files" framing did not match what direct verification found (spec Open Questions item D2); confirm that has not changed.

**Verification:** `grep -rlnE "version together|versioned and released together" skills/ docs/skills/ README.md CHANGELOG.md` returns exactly one file. This scope deliberately excludes `docs/internal/release-plans/`, where D-10's own spec and plan name both wordings. Confirm the same command currently returns two files (`skills/plab-continue-session/HISTORY.md` and root `README.md`) before this phase, and one after.

---

## Phase 5: Version bump and release bookkeeping

**Goal:** Bump `plab-continue-session` to 1.6.0 and update the surrounding bookkeeping.

**Files:** Modify `skills/plab-continue-session/SKILL.md`, `skills/plab-continue-session/HISTORY.md`, `CHANGELOG.md`, `README.md`, `library.json`; regenerate `manifest.generated.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`.

**Fulfills:** N/A - release hygiene, not a functional AC.

**Steps:**
- [ ] Step 1: Bump `skills/plab-continue-session/SKILL.md`'s `metadata.version` to `1.6.0` and `updated` to the ship date.
- [ ] Step 2: Add a `skills/plab-continue-session/HISTORY.md` entry for 1.6.0 describing the consolidation, following the existing entry style (see the 1.3.0 entry).
- [ ] Step 3: Add a `CHANGELOG.md` `[Unreleased]` bullet for continue 1.6.0.
- [ ] Step 4: Update continue's version cell in root `README.md`'s skill table and continue's `version` field in `library.json`.
- [ ] Step 5: Run `node <agent-skills-toolkit>/scripts/generators/gen-manifest.mjs . --write --target=all` per `AGENTS.md:73` to regenerate the derived manifests; do not hand-edit them.

**Verification:** `git diff library.json manifest.generated.json .claude-plugin/plugin.json .codex-plugin/plugin.json` shows only continue's version and description fields changed.

---

## CI and Documentation Coverage

### CI

No CI change. This effort is entirely documentation and reference-file consolidation, verified by the grep and read checks named in each phase's Verification line and in the spec's AC. This plan explicitly declines to add a new automated detector for future contract drift (spec Non-Goal 3); D-3 (extending the hygiene sweep's documentation-drift check to catch content changed without a version bump) and D-11 (three-state gate canaries) are the closer-fitting places for that, and both are sequenced into v0.4.0, ahead of this release.

### Agent-facing documentation

`skills/plab-wrap-session/references/frontmatter-schema.md`, `skills/plab-wrap-session/references/session-log-template.md`, `skills/plab-continue-session/SKILL.md` (Phase 2 and `metadata.version` only), `skills/plab-continue-session/references/handoff-display.md`. No change to `skills/plab-wrap-session/SKILL.md` itself (W-02's territory) and no change to `AGENTS.md`.

### Human-facing documentation

`docs/skills/plab-wrap-session/README.md`, `docs/skills/plab-continue-session/README.md`, `skills/plab-continue-session/HISTORY.md`, `CHANGELOG.md`, root `README.md`.

---

## Rollback

Because this effort only deletes duplicated prose and replaces it with pointers, without changing any field name or log shape, rollback is a straightforward revert of the touched files' text. There is no data migration, no re-tagging, and no impact on logs already written, since parsing behavior for existing frontmatter is unchanged throughout. If a specific consolidation turns out to have deleted context a reader actually needed (for example, if collapsing the Output Shape table lost information its replacement pointer does not adequately cover), the fix is to restore that one paragraph's content, not to revert the whole effort.
