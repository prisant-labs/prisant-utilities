---
id: C-02
title: "Implementation plan: Reconcile the Session Log Against Repo Reality at Resume"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_05_reconcile-at-resume/plan.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: Reconcile the Session Log Against Repo Reality at Resume

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Make `plab-continue-session` check the session log's claims against the repository's current state before replaying them, and lead the resumption display with what changed.

**Architecture:** A new reconciliation step sits between reading the log (current Phase 2) and displaying it (current Phase 3), backed by a new reference file that reuses `plab-wrap-session`'s hygiene-sweep Check 1 commands for remote and tag state and adds four checks of its own (commit count, tag-date release detection, branch existence, file existence) plus an explicit broken-state path for when any check cannot complete. No change touches `plab-wrap-session` or the session-log write format; this is a pure read-side addition.

**Spec:** `spec.md`
**Target versions:** `plab-continue-session` 1.4.0 to 1.5.0. `plab-wrap-session` remains at 1.6.0 (the version it reaches when v0.4.0 ships) and is not touched by this effort.

**Global constraints:**

- No em-dash (U+2014) or en-dash (U+2013) in any file this plan touches. Use " - " or restructure. Numeric ranges use plain hyphens.
- State a contract once, in one named file, and have everything else cite it. The reconciliation mechanism belongs entirely in `references/reconciliation.md`; SKILL.md points at it rather than restating it.
- Never grow the always-on `description`. All new instruction content goes in the SKILL.md body and the new reference file.
- Archive, never delete. This effort adds no deletion capability; the reconciliation step is read-only by design (AC-9).
- This effort ships together with C-03 (cold-repo degradation) as a single `plab-continue-session` 1.5.0 release. Coordinate the version bump and the shared `HISTORY.md` entry so neither effort's execution overwrites the other's half; see Phase 3, Step 1.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Design and document the reconciliation mechanism | AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9 | agent | Not started |
| P2 | Wire the reconciliation step into the workflow and display | AC-1, AC-5 | agent | Not started |
| P3 | Version, HISTORY, and surrounding documentation | N/A | agent | Not started |

---

## Phase 1: Design and document the reconciliation mechanism

**Goal:** Produce a single reference file that fully specifies the reconciliation delta: what it checks, the exact commands for each check, the fallback logic, and the broken-state contract.

**Files:** Create `skills/plab-continue-session/references/reconciliation.md`

**Fulfills:** AC-2, AC-3, AC-4, AC-5, AC-6, AC-7, AC-8, AC-9

**Steps:**
- [ ] Step 1: Write the remote-and-tag command catalog, citing `hygiene-sweep.md` Check 1 by name and reproducing its exact commands (`git fetch origin --tags`, `git status -sb`, `git log --oneline HEAD..@{u}`, `git log --oneline @{u}..HEAD`, `git ls-remote --heads origin`, `git tag -l | tail -5`). State explicitly that this is the same command set, not a rewritten equivalent (AC-2).
- [ ] Step 2: Write the commit-counting logic: `git rev-list --count <sha>..HEAD` when the log's `commit-sha` frontmatter field is present, `git log --since=<log date> --oneline` on the log's branch when it is absent (AC-3).
- [ ] Step 3: Write the tag-date release-detection logic: `git for-each-ref refs/tags --sort=-creatordate --format='%(refname:short) %(creatordate:short)'`, comparing each tag's creation date against the log's `date` field (AC-4).
- [ ] Step 4: Write the branch-existence check: `git branch --list <branch>` locally, `git ls-remote --heads origin <branch>` remotely. State explicitly that this is additive to the existing branch-mismatch warning in `references/handoff-display.md`, not a replacement for it (AC-5).
- [ ] Step 5: Write the continuation-prompt file-existence check, restating D-12's (path-citation precision) exact three-way scoping rule inline so this file is self-contained: a path-separator citation is checked and, if missing, gets the rename-hint fallback `git log --follow --diff-filter=R -- <path>`; a backtick-wrapped citation with no separator is resolved against the repo root and produces no finding either way (never reported as missing, never rename-hinted); a bare prose word with a file extension is excluded from checking entirely. Cite `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-12_path-citation-precision/spec.md` directly rather than re-deriving the rule from the underlying roadmap entry (AC-6).
- [ ] Step 6: Write the next-action-already-done heuristic: when files touched by commits since the log overlap with files or names mentioned in the continuation prompt's immediate next action, state the possibility and ask for verification. Frame this explicitly as advisory, never a hard assertion (AC-7).
- [ ] Step 7: Write the three-state (clean, findings, broken) reporting contract: name each check that can fail, and the exact wording pattern for reporting it broken (which check, why, what could still be verified). State explicitly that this is a documented convention the invoking agent follows each run, not a canary-tested script, because `plab-continue-session` has no independent execution runtime beyond an agent reading and following its SKILL.md (AC-8).
- [ ] Step 8: Add an explicit statement that no command in this file mutates repository state, and list the mutating verbs that must never appear here (`pull`, `merge`, `checkout`, `reset`, `push`) as a self-check for whoever edits this file later (AC-9).

**Verification:** Read the finished file top to bottom. Confirm every one of AC-2 through AC-9 has a corresponding, findable subsection. Grep the file for `pull`, `merge`, `checkout -`, `reset`, and `push`; each hit must be inside a sentence explaining that the verb is forbidden, never inside a command to run.

---

## Phase 2: Wire the reconciliation step into the workflow and display

**Goal:** Make the reconciliation step actually run during a resume, and make its output the leading section of the resumption display.

**Files:** Modify `skills/plab-continue-session/SKILL.md`, `skills/plab-continue-session/references/handoff-display.md`

**Fulfills:** AC-1, AC-5

**Steps:**
- [ ] Step 1: In `SKILL.md`, insert a new phase between the current Phase 2 (Read and parse) and Phase 3 (Present the resumption context), titled "Phase 3: Reconcile against reality," directing the agent to `references/reconciliation.md`. Renumber the current Phase 3, 4, and 5 to Phase 4, 5, and 6.
- [ ] Step 2: Update the References table at the bottom of `SKILL.md` to add `references/reconciliation.md`, loaded at the new Phase 3.
- [ ] Step 3: In `handoff-display.md`, add a `### What changed since this log` section to the Required structure block, positioned immediately after the `## Resuming from` header and before the `**Last session:**` line (AC-1).
- [ ] Step 4: Update `handoff-display.md`'s "What to include" list with a bullet for the delta section, in the same style as the existing "Waiting on you" bullet, and add a one-line note in "What to elide" clarifying that the delta reports drift, not a full re-derivation of every fact in the log (so the section stays a header, not a re-read).
- [ ] Step 5: Add a sentence to the new delta section's description in `handoff-display.md` cross-referencing the existing branch-mismatch warning ("Mismatch warnings" section) and stating that the AC-5 branch-existence check is additive to it, not a replacement, so a future reader does not treat the two as duplicates and delete one.

**Verification:** Read `SKILL.md`'s Workflow section top to bottom; confirm phases are numbered consecutively 1 through 6 with no gap or duplicate, and that Phase 3 is the only new one. Read `handoff-display.md`'s Required structure block; confirm `### What changed since this log` appears in exactly the position AC-1 specifies, between the header and the facts line.

---

## Phase 3: Version, HISTORY, and surrounding documentation

**Goal:** Ship the version bump and bring every document that describes this skill's behavior into agreement with it.

**Files:** Modify `skills/plab-continue-session/SKILL.md` frontmatter (`metadata.version`), `skills/plab-continue-session/HISTORY.md`, `CHANGELOG.md`, `docs/skills/plab-continue-session/README.md`, `AGENTS.md`, `library.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `manifest.generated.json`, root `README.md` (skill version table)

**Fulfills:** N/A (documentation and release housekeeping; no new capability introduced in this phase)

**Steps:**
- [ ] Step 1: Bump `skills/plab-continue-session/SKILL.md` `metadata.version` to `1.5.0` and `updated` to the ship date. This version is shared with C-03 (cold-repo degradation). If C-03's implementation runs first and has already made this bump, skip it here and proceed; do not bump twice.
- [ ] Step 2: Add a single `1.5.0` entry to `skills/plab-continue-session/HISTORY.md`, in the same format as the existing `1.3.0` entry, covering this effort's half (the reconciliation delta). If C-03 has already started this entry, extend it rather than creating a second `1.5.0` heading.
- [ ] Step 3: Add this effort's change to `CHANGELOG.md`, in the current `[Unreleased]` section or a new `[0.5.0]` section depending on repository convention at execution time, in the same plain-English "what changes for you / what does not change" style already used for the `[0.2.0]` entry.
- [ ] Step 4: Update `docs/skills/plab-continue-session/README.md`: bump the Version line to `1.5.0`, add a subsection under "How It Works" for the new Phase 3 in the same per-phase style already used there, and add a worked example under "Examples" showing the delta block from a real drift scenario.
- [ ] Step 5: Add one clause to `AGENTS.md`'s `plab-continue-session` blurb noting that resumption now reconciles the log against current repository state before presenting it. Coordinate with C-03 if both efforts touch this blurb in the same session; land as one combined edit rather than two conflicting ones.
- [ ] Step 6: Bump the `plab-continue-session` component version to `1.5.0` in `library.json`, and the top-level version in `library.json`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json` to `0.5.0`. Regenerate `manifest.generated.json` and the two plugin manifests from `library.json` using the command named in `AGENTS.md` ("Build and validate") where the generator is available in this environment; never hand-edit `manifest.generated.json` directly, since it embeds skill descriptions verbatim and a hand-edit that skips regeneration ships a manifest contradicting the skill, per `release-checklist.yaml`'s own stated reason for this row. If the generator cannot be run in this environment, hand-edit `library.json` only and say so explicitly.
- [ ] Step 7: Bump the Version column for `plab-continue-session` in the root `README.md` skill table (the table starting near line 9, per `release-checklist.yaml`), distinct from any prose version mention the built-in doc-update checklist already covers.

**Verification:** `git diff --stat` shows every file listed above touched, including `manifest.generated.json` and the root `README.md` skill table. Grep `skills/plab-continue-session/` and `docs/skills/plab-continue-session/` for `1.5.0` to confirm the bump landed everywhere the version string appears; grep `library.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `manifest.generated.json` for `0.5.0`. If the toolkit is available locally, run `node <agent-skills-toolkit>/scripts/check.mjs .` and confirm it reports `0 error(s)`.

---

## CI and Documentation Coverage

### CI

No CI change. This repository has no `.github/` directory yet; CI-01 bootstraps it in v0.4.0, which ships before this release. This effort adds no rung-1 (CI or hook) check. The clean, findings, broken discipline in AC-8 is a rung-3 documented convention, written into `references/reconciliation.md` and followed by whichever agent invokes the skill each time it runs, not a rung-1 canary-tested script: `plab-continue-session` has no independent execution runtime beyond an agent reading and following its SKILL.md, so there is no standalone script for a canary to test against. Once CI-01's toolkit action is live, the existing conformance gate (`check.mjs`) validates SKILL.md structure and frontmatter automatically; this effort introduces no new frontmatter field or schema element, so the gate needs no change to cover it.

### Agent-facing documentation

- `skills/plab-continue-session/SKILL.md`: new Phase 3 (Reconcile against reality), Phases 4 through 6 renumbered, References table entry, version bump.
- `skills/plab-continue-session/references/reconciliation.md`: new file, the complete mechanism (AC-2 through AC-9).
- `skills/plab-continue-session/references/handoff-display.md`: new leading section in the required structure and the "What to include" / "What to elide" lists.
- `AGENTS.md`: the `plab-continue-session` blurb gains one clause describing the reconciliation behavior.

These are runtime configuration read by an agent every time the skill fires; a stale line here poisons every future resumption, so precision matters more than prose polish.

### Human-facing documentation

- `docs/skills/plab-continue-session/README.md`: version line, a new "Reconcile against reality" subsection under How It Works, and a worked delta example under Examples.
- `CHANGELOG.md`: an entry in the established "what changes for you / what does not change" style, written for a reader who has not seen this plan.
- `skills/plab-continue-session/HISTORY.md`: the shared `1.5.0` entry, co-written with C-03's half.
- Root `README.md`: the skill version table's `plab-continue-session` row.
- `manifest.generated.json`: regenerated, never hand-edited, per `release-checklist.yaml`'s explicit row for this file. Listed here rather than under Agent-facing documentation because it is a build artifact, not an authored source; the authored source is `library.json`.

A reader returning after three months should be able to read the README's new subsection alone and understand that resuming now tells them what changed since the log was written, without needing to read this plan or the source roadmap.

---

## Rollback

Revert `SKILL.md`, `references/reconciliation.md`, `references/handoff-display.md`, and the version and documentation changes in a single commit revert. The effort touches no schema, no other skill, and (at this release) no CI, so reverting is a pure file-content rollback with no data migration. The delta is computed at resume time from live git state and is never written into the log itself, so no log produced during this version needs any change if the effort is rolled back.
