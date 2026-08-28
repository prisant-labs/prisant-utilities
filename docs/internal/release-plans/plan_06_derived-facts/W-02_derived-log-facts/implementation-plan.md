---
id: W-02
title: "Implementation plan: Derive session-log facts from git instead of model recall"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_06_derived-facts/plan.md
ac-coverage: complete
phase-count: 5
---

# Implementation Plan: Derive session-log facts from git instead of model recall

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Replace model-recalled session-log facts with values derived from git and the environment, via a new `derive-log-facts.py` script that `plab-wrap-session`'s `SKILL.md` is rewired to call.

**Architecture:** `derive-log-facts.py` is a single stdlib-only Python script at `skills/plab-wrap-session/scripts/derive-log-facts.py`, invoked twice per wrap: once early, for environment fields, files-changed, commit-range, and tags, before any prose is drafted; once late, for `decisions-count`, after the Decisions Made section exists (see spec Open Questions item D2). `SKILL.md`'s Evidence Gathering and Frontmatter sections are rewritten to call it in place of manual derivation. Step-level detail below is deliberately lighter than a v0.4.0 or v0.6.0 plan would carry: by the time this effort executes, v0.4.0 and v0.6.0 will already have changed `SKILL.md`'s exact line numbers and possibly its gate list (D-11, D-12, D-7 land first), so steps describe what changes, not exact line ranges to edit.

**Spec:** `spec.md`

**Target versions:** `plab-wrap-session` 1.7.0; plugin v0.7.0. `plab-continue-session`'s move to 1.6.0 is unaffected by this plan; it belongs to D-10.

**Global constraints:**
- No em-dashes (U+2014) or en-dashes (U+2013) anywhere in any file this plan touches. Use " - " or restructure.
- State a contract once, in one named file. This plan deliberately does not touch the reference docs that restate the frontmatter or template contract (`references/frontmatter-schema.md`, `references/session-log-template.md`, anything under `skills/plab-continue-session/`, `docs/skills/plab-wrap-session/README.md`); that consolidation is D-10's job, sequenced after this one.
- This plugin is built for its one maintainer. No configurability for hypothetical third-party users.
- Token economy is a first-class objective. Do not grow `SKILL.md`'s description.
- Archive, never delete; dry-run by default; per-action confirmation for anything that touches the world. The script itself is read-only and needs no dry-run flag, but nothing in this plan should introduce a write path that skips confirmation.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Build the core derivation script (environment fields, files-changed, commit-range/tags, path resolution) | AC-1, AC-2, AC-3, AC-7 | agent | Not started |
| P2 | Add decisions-count and verification-table derivation with graceful degradation | AC-4, AC-5 | agent | Not started |
| P3 | Lock the read-only / `--json` contract and add the stdlib-only test script | AC-8 | agent | Not started |
| P4 | Wire the script into `SKILL.md`; confirm the four judgment sections stay untouched | AC-6, AC-9 | agent | Not started |
| P5 | Version bump and release bookkeeping (HISTORY, CHANGELOG, README, manifests) | N/A - release hygiene | agent | Not started |

---

## Phase 1: Build the core derivation script

**Goal:** Emit `machine`, `repo`, `branch`, `date`, `files-changed`, commit-range, and latest-tag as JSON or Markdown, resolving paths per the `organize-logs.py` precedent.

**Files:** Create `skills/plab-wrap-session/scripts/derive-log-facts.py`.

**Fulfills:** AC-1, AC-2, AC-3, AC-7

**Steps:**
- [ ] Step 1: Scaffold the script on `organize-logs.py`'s shape: `argparse`, `from __future__ import annotations`, a `--json` flag, stdlib-only imports (`subprocess` for git, `socket` for hostname, `datetime` for the clock).
- [ ] Step 2: Implement environment-field derivation: `machine` via `socket.gethostname()`, `repo` via `git remote -v` falling back to the directory name, `branch` via `git branch --show-current`, `date` via the system clock.
- [ ] Step 3: Implement `files-changed` via `git diff --name-only <base>..HEAD`, with a `--base` argument (default a sensible upstream ref), grouped consistently with `SKILL.md:143`'s existing guidance.
- [ ] Step 4: Implement commit-range (`git log`) and latest-tag (`git describe`) derivation under names resolved per spec Open Questions item D1, confirmed not to collide with the existing `commit-sha` or `tags` fields.
- [ ] Step 5: Resolve the script's own path relative to `Path(__file__).resolve().parent`, matching `organize-logs.py`; accept the project root to inspect as a separate, explicit argument, never assumed to share a root with the script's own location.

**Verification:** `python skills/plab-wrap-session/scripts/derive-log-facts.py --json` run from inside this repo prints a JSON object whose `machine`, `repo`, and `branch` values match `hostname`, this repo's remote, and `git branch --show-current` run directly; `files-changed` matches `git diff --name-only` for the same base ref.

---

## Phase 2: decisions-count and verification-table derivation

**Goal:** Add the decisions-count mechanism (a mechanical count, computed after prose exists) and verification-content derivation with graceful degradation when no record is available.

**Files:** Modify `skills/plab-wrap-session/scripts/derive-log-facts.py`.

**Fulfills:** AC-4, AC-5

**Steps:**
- [ ] Step 1: Implement a mode that accepts a drafted log body (path or stdin) and returns a mechanical count of `## Decisions Made` entries, resolving spec item D2's chosen mechanism (second invocation vs. a single generation pass with a mechanical recount).
- [ ] Step 2: Implement verification-content derivation that reads a tool-call or transcript record when the harness exposes one; return an explicit "no record available" signal otherwise, never a fabricated entry.
- [ ] Step 3: Confirm the "no record available" path is what fires when capture-lite is the only thing present, since capture-lite cannot describe the current, still-open session (D-4).

**Verification:** Given a fixture log body with three `## Decisions Made` bullets, the script reports `3`. Given a fixture run with no transcript and no capture-lite record, the script's verification output is the explicit "no record" signal, not a silent empty success.

---

## Phase 3: Read-only / `--json` contract and the test script

**Goal:** Lock in that the script never writes to disk, and add a stdlib-only sibling test script.

**Files:** Create `skills/plab-wrap-session/scripts/test-derive-log-facts.py`. No behavior change to `derive-log-facts.py` beyond fixing any write path this phase's audit finds.

**Fulfills:** AC-8

**Steps:**
- [ ] Step 1: Audit `derive-log-facts.py` for any filesystem write; there should be none. Fix if one is found.
- [ ] Step 2: Scaffold `test-derive-log-facts.py` on `test-organize-logs.py`'s shape: a `check()` helper, throwaway fixtures in a temp directory, no external framework.
- [ ] Step 3: Build fixture git repositories (`git init` in a temp dir, a couple of commits, a tag) to exercise files-changed, commit-range, and tag derivation deterministically.
- [ ] Step 4: Add cases for the Phase 2 decisions-count and verification-degradation paths.

**Verification:** `python skills/plab-wrap-session/scripts/test-derive-log-facts.py` exits 0 and prints an all-pass summary, matching `test-organize-logs.py`'s own reporting style.

---

## Phase 4: Wire the script into SKILL.md

**Goal:** Rewire Evidence Gathering and the Frontmatter block to call the script; confirm the four judgment sections are untouched.

**Files:** Modify `skills/plab-wrap-session/SKILL.md`.

**Fulfills:** AC-6, AC-9

**Steps:**
- [ ] Step 1: Replace the Evidence Gathering steps that currently ask the agent to run `git status` / `git diff --stat` and recall facts with an instruction to run `derive-log-facts.py` and use its output.
- [ ] Step 2: Replace the "### Frontmatter" block's per-field manual guidance for derived fields with a short pointer to the script; leave the agent-authored fields (`session-type`, `model`, `model-settings`, `agent`, `status`, `skills-used`, `resumed-from`) as agent-filled, unchanged.
- [ ] Step 3: Re-read the Body Sections instructions for Summary, Decisions Made, Waiting on You, and Continuation Prompt and confirm none of them were touched by this phase.
- [ ] Step 4: Bump `metadata.version` to `1.7.0` and `updated` to the ship date.

**Verification:** Diff `SKILL.md` before and after this phase; the only sections that changed are Evidence Gathering, the Frontmatter block, and the version frontmatter. A manual read of Summary, Decisions Made, Waiting on You, and Continuation Prompt shows text unchanged from before this effort.

---

## Phase 5: Version bump and release bookkeeping

**Goal:** Update HISTORY, CHANGELOG, README, and manifests for wrap's move to 1.7.0.

**Files:** Modify `skills/plab-wrap-session/HISTORY.md`, `CHANGELOG.md`, `README.md`, `library.json`; regenerate `manifest.generated.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`.

**Fulfills:** N/A - release hygiene, not a functional AC.

**Steps:**
- [ ] Step 1: Add a `skills/plab-wrap-session/HISTORY.md` entry for 1.7.0 describing the derived-facts split, following the existing entry style (see the 1.5.0 entry).
- [ ] Step 2: Add a `CHANGELOG.md` `[Unreleased]` bullet for wrap 1.7.0.
- [ ] Step 3: Update wrap's version cell in root `README.md`'s skill table and wrap's `version` field in `library.json`.
- [ ] Step 4: Run `node <agent-skills-toolkit>/scripts/generators/gen-manifest.mjs . --write --target=all` per `AGENTS.md:73` to regenerate the derived manifests; do not hand-edit them.

**Verification:** `git diff library.json manifest.generated.json .claude-plugin/plugin.json .codex-plugin/plugin.json` shows only wrap's version and description fields changed, and the generated files match what the generator produces rather than hand-typed edits.

---

## CI and Documentation Coverage

### CI

No CI change. This repo has no `.github/` directory yet (CI is greenfield), and bootstrapping it is CI-01's job, a separate v0.4.0 effort not owned here. This effort is verified by the command named in each phase's Verification line and by `test-derive-log-facts.py`, a rung-2 committed script the maintainer runs, at the same mechanization-ladder rung as its sibling `test-organize-logs.py`.

### Agent-facing documentation

`skills/plab-wrap-session/SKILL.md`: Evidence Gathering and the Frontmatter block rewritten to call the script (Phase 4); `metadata.version` bumped to 1.7.0. No change to any file under `skills/plab-wrap-session/references/` (D-10's territory) and no change to `AGENTS.md` (no new trigger phrase, no skill renamed, no change to the plugin's skill list).

### Human-facing documentation

`skills/plab-wrap-session/HISTORY.md` (new 1.7.0 entry), `CHANGELOG.md` (`[Unreleased]` bullet), root `README.md` (wrap's version cell). `docs/skills/plab-wrap-session/README.md` is explicitly not touched here; its restatement of the frontmatter contract is D-10's territory, and editing it in both plans would create the exact double-ownership the conventions warn against.

---

## Rollback

If `derive-log-facts.py` ships with a defect that produces wrong facts (for example, a wrong branch value or a bad files-changed diff), revert `SKILL.md`'s Evidence Gathering and Frontmatter sections to their pre-1.7.0 text; this is a single-file revert, since Phase 4 is the only phase that changes agent-facing runtime behavior. The skill returns to manual derivation immediately, with no session-log format change to unwind, because the log's own shape does not change, only how its fields get filled in. Because the script never writes to disk (AC-8), rollback carries no data-migration risk; the script can stay in the tree, unused, until the defect is fixed.
