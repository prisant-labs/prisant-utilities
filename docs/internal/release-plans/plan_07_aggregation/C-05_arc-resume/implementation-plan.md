---
id: C-05
title: "Implementation plan: Arc resume: read the last N logs, not just the newest"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_07_aggregation/plan.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: Arc resume: read the last N logs, not just the newest

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Add an explicit `--arc [N]` flag to `plab-continue-session` that resumes from a narrative collapse of the last N logs instead of the single newest one, without touching the unflagged default flow.

**Architecture:** A new `--arc [N]` branch in `plab-continue-session`'s Phase 1 calls `skills/plab-wrap-session/scripts/aggregate-logs.py`, the shared script W-04 ships inside wrap's own directory per `plan.md`'s D1 resolution ("Where the shared aggregation layer lives"; not a plugin-root location), instead of the skill's own single-log discovery. From `plab-continue-session`'s own directory this is a cross-skill relative path, `../plab-wrap-session/scripts/aggregate-logs.py`, one directory hop shorter than the plugin's existing `../../lib/render-mermaid.py` cross-reference pattern but resting on the same guarantee: every skill under `skills/` ships and installs as one plugin unit, so the relative path between two sibling skill directories is as stable as the path from a skill into plugin-root `lib/`. The result feeds an extended Phase 3 display: a narrative section and an open-threads section are added around the existing display, and the newest log's Continuation Prompt still appears verbatim exactly as it does today. This effort has a hard, one-directional dependency: `skills/plab-wrap-session/scripts/aggregate-logs.py` and `skills/plab-wrap-session/references/log-aggregation.md` must already exist, which means W-04's implementation plan must be executed, and ideally shipped, before this one starts. Do not begin Phase 1 below against a repository where that script does not yet exist. As with W-04, this is a v0.8.0 effort under the conventions' depth-scaling rule: the phases and verification commands are real and complete, but the exact narrative-generation prompt wording and the precise Markdown layout of the new display sections are deliberately left to be settled at execution time against whatever shape W-04 actually shipped.

**Spec:** `spec.md`
**Target versions:** `plab-continue-session` 1.7.0 (plugin v0.8.0), shipping alongside `plab-wrap-session` 1.8.0 (W-04) in the same v0.8.0 release.

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) anywhere in any file this plan touches. Use " - " or restructure.
- State every contract once. This effort adds no new window-selection, extraction, or coverage-statement rules; all of that is defined once in `skills/plab-wrap-session/references/log-aggregation.md` (W-04) and cited here, never restated.
- `--arc` is opt-in only. No step in this plan may make it fire without the explicit flag.
- The existing hard constraints in `plab-continue-session`'s Constraints section, never paraphrase the Continuation Prompt, refuse cross-repo resumption, surface branch and age mismatches, apply unchanged to arc mode. No step here may relax them.
- No new skill description growth. `--arc` is documented in the SKILL.md body and argument-hint, not in the always-on description.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Wire `--arc [N]` into Phase 1 discovery, delegating to the shared script | AC-1, AC-2, AC-5, AC-6, AC-7 | agent | Not started |
| P2 | Extend the Phase 3 display with the narrative and open-threads sections | AC-3, AC-4 | agent | Not started |
| P3 | Version bump and documentation sync | - | agent | Not started |

---

## Phase 1: Wire `--arc [N]` into Phase 1 discovery

**Goal:** `/plab-continue-session --arc [N]` reads the last N logs via the shared script and states the read cost before spending it; `/plab-continue-session` without the flag is untouched.

**Files:**
- Modify: `skills/plab-continue-session/SKILL.md` (Phase 1 gains an `--arc [N]` branch; update `argument-hint` to `"[--log <path>] [--arc [N]]"`)
- Create: `skills/plab-continue-session/references/arc-mode.md` (arc-specific behavior only: the pre-read cost statement, the call into `skills/plab-wrap-session/scripts/aggregate-logs.py`, and a pointer to `skills/plab-wrap-session/references/log-aggregation.md` for the window and rollup rules rather than restating them)

**Fulfills:** AC-1, AC-2, AC-5, AC-6, AC-7

**Steps:**
- [ ] Step 1: Confirm `skills/plab-wrap-session/scripts/aggregate-logs.py` and `skills/plab-wrap-session/references/log-aggregation.md` exist in the target repository state (W-04 shipped) before starting. If not, stop; this phase cannot proceed against its own dependency.
- [ ] Step 2: Add the `--arc [N]` branch to Phase 1 in `SKILL.md`: when present, skip the existing single-log discovery entirely and call `skills/plab-wrap-session/scripts/aggregate-logs.py` with the requested or default N.
- [ ] Step 3: Implement the pre-read cost statement (AC-5) as the first output of arc mode, before the script's result is narrated: log count and date span, with a yes/no confirmation gate before proceeding, consistent with this skill's existing confirm-before-acting posture.
- [ ] Step 4: Write `references/arc-mode.md` documenting the branch added in Step 2 and Step 3. State explicitly that it defines no discovery or extraction logic of its own and instead points at `skills/plab-wrap-session/references/log-aggregation.md`.
- [ ] Step 5: Update `argument-hint` in `SKILL.md`'s frontmatter.

**Verification:** Manually run `/plab-continue-session` (no flag) against this repository and confirm the output and flow are byte-for-byte the same as before this phase (AC-1). Manually run `/plab-continue-session --arc 5` and confirm: the pre-read cost statement naming the log count and date span appears first, before any window content is read or shown (AC-5); a confirmation is required before the window is read; and the underlying call is to `skills/plab-wrap-session/scripts/aggregate-logs.py` (AC-2) rather than any new discovery code written in this skill, grep `skills/plab-continue-session/` for anything resembling independent multi-log pooling, filtering, or same-arc comparison logic and confirm it finds none (satisfying both AC-6, no dedup logic, and AC-7, no independent discovery logic; D-05's own spec, `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-05_superseding-logs/spec.md`, is the reason AC-6 expects nothing to find: its AC-3 already removes same-arc duplicates from the corpus before arc mode ever runs).

---

## Phase 2: Extend the Phase 3 display

**Goal:** The resumption display arc mode produces adds a narrative section and an open-threads section around the existing single-log display shape, states its harness and store coverage the same way W-04's digest does, and never touches the verbatim Continuation Prompt.

**Files:**
- Modify: `skills/plab-continue-session/references/handoff-display.md` (add one short note pointing to `references/arc-mode.md` for the arc-extended shape; do not restate the extension inline)
- Modify: `skills/plab-continue-session/references/arc-mode.md` (add the extended display shape: narrative section, open-threads section, coverage line, and the explicit rule that the newest log's Continuation Prompt block is unchanged from the single-log flow)

**Fulfills:** AC-3, AC-4

**Steps:**
- [ ] Step 1: Add the narrative section and open-threads section shapes to `references/arc-mode.md`, positioned around the existing Phase 3 structure from `handoff-display.md` rather than replacing any of it.
- [ ] Step 2: State the coverage-line requirement using the exact wording contract `skills/plab-wrap-session/references/log-aggregation.md` defines, so the same rollup reads identically whether it surfaces from `--digest` or `--arc`.
- [ ] Step 3: State explicitly, next to the Continuation Prompt section of the extended display, that it is copied verbatim from the newest log exactly as `handoff-display.md`'s existing rule already requires; this phase adds no new prompt-handling logic.
- [ ] Step 4: Add the one-line cross-reference in `handoff-display.md` pointing to `references/arc-mode.md`.

**Verification:** Manually run `/plab-continue-session --arc` against this repository's real log store (once it has more than one log) and confirm by inspection: the display has a narrative section, an open-threads section, a coverage line matching W-04's digest wording, and a Continuation Prompt block that is identical to what the plain (non-arc) flow would show for the same newest log.

---

## Phase 3: Version bump and documentation sync

**Goal:** Shipped version numbers, manifests, and human-facing docs agree with what actually shipped, per this repo's own release-checklist rows.

**Files:**
- Modify: `skills/plab-continue-session/SKILL.md` (`metadata.version: "1.7.0"`, `updated:`)
- Modify: `skills/plab-continue-session/HISTORY.md` (new 1.7.0 entry: `--arc [N]` flag, its dependency on `skills/plab-wrap-session/scripts/aggregate-logs.py` from the `plab-wrap-session` 1.8.0 release, and the pairing-contract note that this is a read-side change consuming write-side-adjacent shared infrastructure rather than a session-log format change)
- Modify: `library.json` (bump the `plab-continue-session` component version to 1.7.0; confirm the top-level plugin version is 0.7.0, already bumped by W-04's implementation plan if it ran first)
- Modify: `manifest.generated.json` (regenerate; do not hand-edit, per `AGENTS.md`)
- Modify: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (confirm `version` reads `0.7.0` in both; only bump here if W-04's plan has not already done so)
- Modify: `docs/skills/plab-continue-session/README.md` (version line, new subsection documenting `--arc`)
- Modify: `README.md` (skill table Version column, line 9 per `release-checklist.yaml`)
- Modify: `CHANGELOG.md` (add to the same `[Unreleased]` or `[0.7.0]` entry W-04 added to, Added: `--arc [N]` flag)

**Fulfills:** (housekeeping; every AC is already covered by P1 and P2)

**Steps:**
- [ ] Step 1: Bump `plab-continue-session`'s version in `SKILL.md` frontmatter and add the HISTORY.md entry.
- [ ] Step 2: Bump `library.json`'s `plab-continue-session` entry; confirm rather than re-bump the top-level plugin version and both native manifests if W-04's plan already set them to 0.7.0 in this same release.
- [ ] Step 3: Regenerate `manifest.generated.json` with the toolkit generator (`--write --target=all`).
- [ ] Step 4: Update `docs/skills/plab-continue-session/README.md` and the root `README.md` table, and add this effort's line to the shared CHANGELOG entry.

**Verification:** `grep -n '"version"' library.json .claude-plugin/plugin.json .codex-plugin/plugin.json` shows matching values across both this effort's and W-04's bumps; `git diff --stat` shows every file listed above touched; the conformance gate (`node <agent-skills-toolkit>/scripts/check.mjs .`) exits 0.

---

## CI and Documentation Coverage

### CI

No CI change. The repo has no `.github/` directory yet (CI is greenfield as of this writing); this effort ships no workflow file and adds no deterministic gate. Verification is manual per-phase (above) plus the existing conformance gate. This effort adds no rung-1 check of its own; it is rung 2 infrastructure (a flag on an existing skill, calling an already-committed script), so D-11's canary discipline does not apply, there is no detector here that could silently fail open.

### Agent-facing documentation

- `skills/plab-continue-session/SKILL.md`: new `--arc [N]` branch in Phase 1, updated `argument-hint`, updated `metadata.version`.
- `skills/plab-continue-session/references/arc-mode.md` (new): the arc-specific behavior, pointing at `skills/plab-wrap-session/references/log-aggregation.md` (W-04) rather than restating its rules.
- `skills/plab-continue-session/references/handoff-display.md`: one added cross-reference line to `arc-mode.md`; the base single-log display contract is otherwise untouched.
- `skills/plab-continue-session/SKILL.md`'s References table: add a row for `references/arc-mode.md`.
- `AGENTS.md`: add one clause to the `plab-continue-session` entry mentioning `--arc`, mirroring how the `plab-wrap-session` entry already mentions `--organize` inline (and how W-04's implementation plan handles the equivalent row for `--digest`). State the intended change and confirm with the maintainer before editing, per this skill's own `doc-update-rules.md`; this is not optional to consider, it is a real row on the release plan's Doc-Update Checklist ("Reflect new or renamed skills"), even though the resolution here is a one-clause addition rather than a new or renamed skill.

### Human-facing documentation

- `docs/skills/plab-continue-session/README.md`: new subsection documenting `--arc [N]` alongside the existing Phase descriptions, written for a reader who has been away for three months: what problem it solves (a three-month gap making the newest log alone insufficient), the pre-read cost statement, and one worked example matching the spec's Behavior / Examples section.
- `README.md`: version bump only (line 9's table), no new prose needed there.
- `CHANGELOG.md`: added to the same release entry W-04 uses, one paragraph, following the file's own established "What changes for you" framing.
- `skills/plab-continue-session/HISTORY.md`: the 1.7.0 entry, written in this file's own established style, explicitly naming the dependency on `plab-wrap-session` 1.8.0's shared script.

---

## Rollback

`--arc` is opt-in and additive: the unflagged default flow is untouched by this effort (AC-1), so rolling back is a version revert with no data migration for existing users who never pass the flag. If `references/arc-mode.md` and the Phase 1 branch need to be pulled, revert the commits that introduced them, drop the `--arc` argument-hint change, remove the cross-reference line from `handoff-display.md`, and revert the version bump in every manifest listed in Phase 3. This effort has no downstream dependents to consider, since nothing in this plugin depends on `plab-continue-session`'s arc mode existing.
