---
id: W-04
title: "Implementation plan: Digest mode: aggregate the last N session logs"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.7.0/plan_v0.7.0.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: Digest mode: aggregate the last N session logs

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Give `plab-wrap-session` a `--digest [N]` mode that reads the last N session logs and reports what shipped, what decisions were made, and what is still outstanding, built on a shared aggregation script `plab-continue-session` can also consume.

**Architecture:** A new script inside `plab-wrap-session`'s own directory, `skills/plab-wrap-session/scripts/aggregate-logs.py`, extends the existing single-newest-log discovery rule in `log-discovery.md` to return the last N logs and extracts each one's frontmatter plus its Work Completed, Decisions Made, Waiting on You, and Outstanding Issues sections, emitting structured JSON. It lives inside wrap rather than at a shared plugin-root location, per `plan_v0.7.0.md`'s own resolved D1 decision ("Where the shared aggregation layer lives"): wrap already owns in-skill scripts and the log-format contract this layer depends on, so the aggregation stays adjacent to it. A companion contract document, `skills/plab-wrap-session/references/log-aggregation.md`, states the rollup and harness-coverage rules once so `plab-continue-session` points at it rather than restating it, exactly as `plab-wrap-session` already points at `plab-continue-session`'s `log-discovery.md` in the other direction. `plab-wrap-session` gains a thin `--digest` section in its `SKILL.md` that calls the script and narrates its output into the three fixed sections. This is a v0.7.0 effort per the conventions' depth-scaling rule: the phases and their verification commands below are real and complete, but exact function signatures and JSON field names are deliberately left to be settled at execution time. W-02 (derived log facts, shipping v0.6.0) lands before this effort but does not provide a reusable per-log parsing utility for this purpose: its script derives facts about the session currently being wrapped from git and the environment, not parsed content from already-written historical logs, so this script's Markdown section-boundary parsing is independent, new work (spec Open Question D3, resolved).

**Spec:** `spec.md`
**Target versions:** `plab-wrap-session` 1.8.0 (plugin v0.7.0). `plab-continue-session` is not modified by this effort; C-05 in the same release depends on the script this effort ships but bumps continue-session's own version independently.

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) anywhere in any file this plan touches. Use " - " or restructure.
- State every contract once, in the file that owns it. `skills/plab-wrap-session/references/log-aggregation.md` is the single source of truth for the window-selection, extraction, and coverage-statement rules; `SKILL.md` points at it rather than restating it, exactly as `SKILL.md` already does for `log-discovery.md`.
- Digest mode is read-only: it writes nothing, moves nothing, and therefore needs no per-action confirmation step.
- No new skill description growth. `--digest` is documented in the SKILL.md body and argument-hint, not in the always-on description.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Build the shared aggregation script and its contract doc | AC-2, AC-6, AC-7, AC-8 | agent | Not started |
| P2 | Wire `--digest` mode into `plab-wrap-session` | AC-1, AC-3, AC-4, AC-5 | agent | Not started |
| P3 | Version bump and documentation sync | - | agent | Not started |

---

## Phase 1: Build the shared aggregation script and its contract doc

**Goal:** A deterministic, independently invocable script that selects the last N logs and extracts their shipped, decision, and outstanding content, plus the contract document describing its rules once for both consuming skills.

**Files:**
- Create: `skills/plab-wrap-session/scripts/aggregate-logs.py` (per the release plan's D1 resolution: inside `plab-wrap-session`'s own directory, not a shared plugin-root location)
- Create: `skills/plab-wrap-session/scripts/test-aggregate-logs.py` (fixture-based, following the pattern already established by the sibling `skills/plab-wrap-session/scripts/test-organize-logs.py`: pinned dates, small synthetic log fixtures, no network or real-clock dependency)
- Create: `skills/plab-wrap-session/references/log-aggregation.md` (the shared contract: window-selection rule referencing `log-discovery.md` rather than restating it, the four sections extracted per log, the rollup shape, the harness-coverage statement requirement, and an explicit note that no same-arc dedup is implemented because D-05 already handles it at write time)

**Fulfills:** AC-2, AC-6, AC-7, AC-8

**Steps:**
- [ ] Step 1: Do not call W-02's `derive-log-facts.py` from this script (spec Open Question D3, resolved). That script derives facts about the session currently being wrapped, from git and the environment; this script parses the authored sections of many already-written historical logs. The two do not share an implementation surface. Confirm this is still true at execution time only if W-02's actual shipped shape has diverged materially from its spec.
- [ ] Step 2: Implement window selection in `skills/plab-wrap-session/scripts/aggregate-logs.py` by extending, not reimplementing, the pooling and sort logic `log-discovery.md` already defines: pool the flat store, its `YYYY-MM` folders, and the two legacy stores, sort descending on filename, take the newest N (default 10 per AC-8, overridable).
- [ ] Step 3: Implement per-log extraction: frontmatter fields (`date`, `agent`, `status`, `summary`) plus the four body sections named in the spec. Malformed or missing sections degrade to an empty result for that log rather than raising, consistent with the rest of this skill pair's error handling.
- [ ] Step 4: Implement the cross-log rollup: `shipped` and `decisions` as ordered lists tagged with their source log; `outstanding` as the union of the newest log's Waiting-on items (already carrying forward `(blocked since YYYY-MM-DD)` markers once D-07 has shipped) plus any Outstanding Issues item seen anywhere in the window, each tagged with its first-seen log.
- [ ] Step 5: Implement the coverage tally: count of logs read, grouped by `agent` value, and the list of stores actually scanned (a store that does not exist is omitted, not reported as zero).
- [ ] Step 6: CLI surface mirrors `organize-logs.py`: positional store path, a count flag, `--json` for machine output, plain-text summary otherwise. No `--apply` equivalent exists; this script never writes.
- [ ] Step 7: Write `skills/plab-wrap-session/references/log-aggregation.md` stating the rules from steps 2, 4, and 5 once. This skill's `references/` folder has no separate index file to update (unlike the plugin-root `lib/` and `references/` folders); the only place this new file needs listing is `SKILL.md`'s own References table, handled in Phase 2.
- [ ] Step 8: Write `skills/plab-wrap-session/scripts/test-aggregate-logs.py` covering: fewer logs than N exist, a window spanning a `YYYY-MM` folder and the flat store, a log missing one of the four sections, a log from each legacy store, and the coverage tally against a fixture set with mixed `agent` values.

**Verification:** `python skills/plab-wrap-session/scripts/test-aggregate-logs.py` exits 0 with every fixture check passing (report the pass count, mirroring `test-organize-logs.py`'s 34-check precedent). Manually run `python skills/plab-wrap-session/scripts/aggregate-logs.py _local/_session-logs --count 3 --json` against this repo's real log store and confirm the JSON's `logs-read` list matches the 3 newest filenames by inspection.

---

## Phase 2: Wire `--digest` mode into `plab-wrap-session`

**Goal:** `/plab-wrap-session --digest [N]` runs the script from Phase 1 and narrates its output into the three-question report, without writing a log or running the hygiene sweep.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md` (add a `## Digest Mode (--digest)` section immediately after Organize Mode, following that section's own shape: what it does, that it runs instead of a wrap, a pointer to `references/log-aggregation.md` (this skill's own, at `skills/plab-wrap-session/references/log-aggregation.md`) for the extraction and coverage rules rather than restating them; update `argument-hint` to `"[mode: quick|final|deep|blocked] [--organize] [--digest [N]]"`)
- Modify: `docs/skills/plab-wrap-session/README.md` (document the new mode alongside the existing Organize Mode section, human-facing)

**Fulfills:** AC-1, AC-3, AC-4, AC-5

**Steps:**
- [ ] Step 1: Add the `## Digest Mode` section to `SKILL.md`: invocation shape, "runs instead of a wrap, no log written, no hygiene sweep" contract stated explicitly (mirroring Organize Mode's own wording), and the three fixed section names.
- [ ] Step 2: State the coverage-line requirement inline in `SKILL.md` (not only in `skills/plab-wrap-session/references/log-aggregation.md`), since it is a gate on every digest run rather than incidental detail: the digest must not print a count without the harnesses-and-stores line from the script's output.
- [ ] Step 3: Add one worked example to `docs/skills/plab-wrap-session/README.md`, not `SKILL.md`, matching the precedent Organize Mode already set: `SKILL.md` stays mechanism-focused, the human-facing README carries the worked example (the spec's Behavior / Examples section has the reference shape). Showing the three sections plus the coverage line against realistic content does not need a dedicated `examples/` file the way `--organize`'s captured-output walkthrough does; inline in the README is sufficient at this scale.
- [ ] Step 4: Update the argument-hint in `SKILL.md`'s frontmatter.
- [ ] Step 5: Update `docs/skills/plab-wrap-session/README.md`'s mode documentation and its Reference Files table to add rows for `references/log-aggregation.md` and `scripts/aggregate-logs.py`, matching that table's existing skill-relative naming style.

**Verification:** Manually invoke `/plab-wrap-session --digest` in this repository once real logs exist in `_local/_session-logs/` and confirm by inspection: no file is created under `_local/_session-logs/`, the output has exactly three labeled sections plus the coverage line, and an outstanding item present in more than one log in the window is visibly marked as such (age or first-seen log) rather than looking identical to a fresh one.

---

## Phase 3: Version bump and documentation sync

**Goal:** The shipped version numbers, manifests, and human-facing docs agree with what actually shipped, per this repo's own release-checklist rows.

**Files:**
- Modify: `skills/plab-wrap-session/SKILL.md` (`metadata.version: "1.8.0"`, `updated:`)
- Modify: `skills/plab-wrap-session/HISTORY.md` (new 1.8.0 entry: `--digest` mode, the introduction of `skills/plab-wrap-session/scripts/aggregate-logs.py` as shared plugin infrastructure, and a forward pointer noting C-05 consumes the same script)
- Modify: `library.json` (bump the `plab-wrap-session` component version to 1.8.0 and the top-level plugin version to 0.7.0; C-05's implementation plan bumps `plab-continue-session` in the same release)
- Modify: `manifest.generated.json` (regenerate; do not hand-edit, per `AGENTS.md`)
- Modify: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (bump `version` to `0.7.0` in both, per `docs/internal/release-plans/release-checklist.yaml`)
- Modify: `docs/skills/plab-wrap-session/README.md` (version line)
- Modify: `README.md` (skill table Version column, line 9 per `release-checklist.yaml`)
- Modify: `CHANGELOG.md` (new `[Unreleased]` or `[0.7.0]` entry, Added: `--digest` mode and `skills/plab-wrap-session/scripts/aggregate-logs.py`)

**Fulfills:** (housekeeping; every AC is already covered by P1 and P2)

**Steps:**
- [ ] Step 1: Bump `plab-wrap-session`'s version in `SKILL.md` frontmatter and add the HISTORY.md entry.
- [ ] Step 2: Bump `library.json` per `release-checklist.yaml`'s rows, then regenerate `manifest.generated.json` with the toolkit generator (`--write --target=all`) rather than hand-editing.
- [ ] Step 3: Bump both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` to the same version; release hygiene gate (f) fails the tag when they disagree.
- [ ] Step 4: Update the two README surfaces and the CHANGELOG per `doc-update-rules.md` and `release-checklist.yaml`.

**Verification:** `grep -n '"version"' library.json .claude-plugin/plugin.json .codex-plugin/plugin.json` shows matching values; `git diff --stat` shows every file listed above touched; the conformance gate (`node <agent-skills-toolkit>/scripts/check.mjs .`) exits 0.

---

## CI and Documentation Coverage

### CI

No CI change. The repo has no `.github/` directory yet (CI is greenfield as of this writing); this effort ships no workflow file and adds no deterministic gate. Verification is manual per-phase (above) plus the existing conformance gate, which already runs against any repo state. This effort does not add a rung-1 check; `skills/plab-wrap-session/scripts/aggregate-logs.py` itself is rung 2 (a committed script the maintainer or agent runs on demand), not a check with a pass/fail verdict, so the three-state clean/findings/broken canary discipline from D-11 does not apply here, there is nothing for this script to report as "broken" in that sense.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: new `## Digest Mode (--digest)` section, updated `argument-hint`, updated `metadata.version`.
- `skills/plab-wrap-session/references/log-aggregation.md` (new): the shared contract both consuming skills point at. This is the file that must stay accurate above all others in this plan; a stale line here poisons both skills' next invocation. It has no separate index file to update, since individual skills' `references/` folders in this plugin are not indexed the way the plugin-root `lib/` and `references/` folders are.
- `skills/plab-wrap-session/SKILL.md`'s own References table: add a row for `references/log-aggregation.md`, alongside the existing rows for `frontmatter-schema.md`, `session-log-template.md`, `hygiene-sweep.md`, and `doc-update-rules.md`.
- `AGENTS.md`: add one clause to the `plab-wrap-session` entry mentioning `--digest` and its script path, mirroring how the existing entry already names `--organize` and `scripts/organize-logs.py` inline. State the intended change and confirm with the maintainer before editing, per this skill's own `doc-update-rules.md`; this is not optional to consider, it is a real row on the release plan's Doc-Update Checklist ("Reflect new or renamed skills"), even though the resolution here is a one-clause addition rather than a new or renamed skill.

### Human-facing documentation

- `docs/skills/plab-wrap-session/README.md`: new subsection documenting `--digest` alongside the existing `--organize` subsection, written for a reader who has been away for three months: what it does, why it exists (the arc-reconstruction and skill-usage pain points from the spec's Purpose), and one worked example.
- `README.md`: version bump only (line 9's table), no new prose needed there.
- `CHANGELOG.md`: an `[Unreleased]` or `[0.7.0]` entry in the Added section, one paragraph, following this file's own established "What changes for you" framing.
- `skills/plab-wrap-session/HISTORY.md`: the 1.8.0 entry, written in this file's own established style (what shipped, why, what does not change).

---

## Rollback

`--digest` is read-only and additive: it writes no files and changes no existing behavior when not invoked, so rolling back is a version revert with no data migration. If `skills/plab-wrap-session/scripts/aggregate-logs.py` or `skills/plab-wrap-session/references/log-aggregation.md` need to be pulled, revert the commits that introduced them, drop the `--digest` section and argument-hint change from `SKILL.md`, and revert the version bump in every manifest listed in Phase 3; C-05 must be reverted or re-pointed first if it has already shipped against this script, since it has a hard dependency on `skills/plab-wrap-session/scripts/aggregate-logs.py` existing.
