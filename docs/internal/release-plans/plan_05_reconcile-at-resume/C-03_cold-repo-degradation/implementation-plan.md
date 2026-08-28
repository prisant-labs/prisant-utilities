---
id: C-03
title: "Implementation plan: Build Orientation From Repo Reality When No Recent Log Exists"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_05_reconcile-at-resume/plan.md
ac-coverage: complete
phase-count: 4
---

# Implementation Plan: Build Orientation From Repo Reality When No Recent Log Exists

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Turn "no recent log" from a dead end into a supported path that builds real orientation from the repository itself.

**Architecture:** A new reference file assembles orientation from five sources (commits since the maintainer's last authored commit, `gh` issues and pull requests, README/AGENTS.md, working-tree state, and capture-lite records where D-04, the capture-lite consumers effort shipped in v0.4.0, has made them consumable), wired into Phase 1's no-log and 30-day-stale-log branches. The orientation path is reached only through the skill's existing explicit-resume triggers; per the v0.6.0 release plan's D2 decision (Option A), neither the always-on description nor the body's status-question carve-out changes in this release, so "where were we" alone does not route here yet. No change touches `plab-wrap-session`.

**Spec:** `spec.md`
**Target versions:** `plab-continue-session` 1.4.0 to 1.5.0. `plab-wrap-session` remains at 1.6.0 (the version it reaches when v0.4.0 ships) and is not touched by this effort.

**Global constraints:**

- No em-dash (U+2014) or en-dash (U+2013) in any file this plan touches. Use " - " or restructure. Numeric ranges use plain hyphens.
- State a contract once, in one named file, and have everything else cite it. The orientation mechanism belongs entirely in `references/cold-repo-orientation.md`; SKILL.md points at it rather than restating it.
- Never grow the always-on `description`, and do not touch the "When NOT to Use" section either. These are not just the general rule; they are AC-8 and AC-9, hard acceptance criteria for this specific effort, and the Phase 3 verification step below diffs both explicitly to prove it.
- Archive, never delete. This effort adds no deletion capability; the orientation is read-only by design.
- This effort ships together with C-02 (reconcile at resume) as a single `plab-continue-session` 1.5.0 release. Coordinate the version bump and the shared `HISTORY.md` entry so neither effort's execution overwrites the other's half; see Phase 4, Step 1.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Build the cold-repo orientation mechanism | AC-2, AC-3, AC-4, AC-5, AC-6 | agent | Not started |
| P2 | Wire orientation into discovery and the staleness path | AC-1, AC-7 | agent | Not started |
| P3 | Confirm the trigger surface is unchanged, per release-plan decision D2 | AC-8, AC-9 | agent | Not started |
| P4 | Version, HISTORY, and surrounding documentation | N/A | agent | Not started |

---

## Phase 1: Build the cold-repo orientation mechanism

**Goal:** Produce a single reference file that fully specifies how to assemble orientation from all five sources, with an explicit degrade rule for each.

**Files:** Create `skills/plab-continue-session/references/cold-repo-orientation.md`

**Fulfills:** AC-2, AC-3, AC-4, AC-5, AC-6

**Steps:**
- [ ] Step 1: Write the "maintainer's last authored commit" mechanism: `git log --author="$(git config user.email)" -1 --format=%H`, with a fallback to matching `git config user.name` when the email-based query returns nothing (AC-2).
- [ ] Step 2: Write the commits-since-that-commit listing: `git log <that-sha>..HEAD --oneline`, summarized by author when more than one contributor appears in the range.
- [ ] Step 3: Write the `gh` CLI issue and pull-request mechanism (`gh issue list`, `gh pr list`) with its degrade rule stated explicitly: omit the subsection entirely, not with an error message, when `gh` is not installed, not authenticated, or the remote is not GitHub (AC-3).
- [ ] Step 4: Write the README.md / AGENTS.md inclusion rule: read both if present, produce a one-line summary rather than reproducing either in full, and state "not found" plainly for whichever is absent rather than omitting the line (AC-4).
- [ ] Step 5: Write the working-tree-state inclusion, citing `hygiene-sweep.md` Check 2 by name and reusing its exact commands (`git status --short`, `git stash list`, `git worktree list`) rather than a rewritten equivalent (AC-5).
- [ ] Step 6: Write the capture-lite inclusion: read `_local/_session-logs/_capture/YYYY-MM.jsonl` for the current and prior month, report a session count and head-range since the last log's date (or a fixed lookback window when no log exists at all), and name the exact JSONL fields this reads (`ts`, `head`, `dirty`, `untracked`, `stashes`, `last_tag`, `commits_today`, `session_id`) so a future implementer does not have to reverse the schema from the hook. State the silent-degradation rule explicitly: when the capture directory does not exist, this subsection is omitted with no visible "not found" line (AC-6).
- [ ] Step 7: Assemble the full orientation display template, matching the format shown in the spec's Behavior / Examples section (the "No recent session log for this repository" block).

**Verification:** Read the finished file top to bottom. Confirm every one of AC-2 through AC-6 has a findable subsection naming its exact command or file path. Confirm the capture-lite subsection's silent-degradation rule is stated in its own text, not only implied by omission from the rest of the file.

---

## Phase 2: Wire orientation into discovery and the staleness path

**Goal:** Make the orientation mechanism actually run in place of the current dead end, and extend it to the stale-log case.

**Files:** Modify `skills/plab-continue-session/SKILL.md`, `skills/plab-continue-session/references/log-discovery.md`

**Fulfills:** AC-1, AC-7

**Steps:**
- [ ] Step 1: In `log-discovery.md`'s "Empty or missing directory" section, replace the closing two-bullet dead-end block ("Start fresh" / "Manually point me at a log") with a pointer to `references/cold-repo-orientation.md`, keeping the preceding version-skew symptom check unchanged (AC-1).
- [ ] Step 2: In `log-discovery.md`'s "Age warning" section, add the 30-day staleness branch: when the log's `date` is more than 30 days old, present both the existing age-warning-then-resume option and the cold-repo-orientation option, and require an explicit choice between them (AC-7). State the 30-day number explicitly as this effort's own threshold, distinct from the existing 7-day soft-warning threshold, with both numbers named side by side so a future reader does not conflate them.
- [ ] Step 3: In `SKILL.md` Phase 1, add a step directing the agent to `references/cold-repo-orientation.md` when discovery yields no log, or when the AC-7 staleness branch is chosen.
- [ ] Step 4: Update `SKILL.md`'s References table to add `references/cold-repo-orientation.md`, loaded at Phase 1's no-log and stale-log branches.

**Verification:** Read `log-discovery.md`'s "Empty or missing directory" and "Age warning" sections; confirm the old two-bullet dead-end text no longer appears verbatim anywhere in the file, and that both the 7-day and 30-day thresholds are stated explicitly and distinctly, not merged into one number.

---

## Phase 3: Confirm the trigger surface is unchanged, and cross-reference the deferred decision

**Goal:** Verify this effort has not touched how the skill is triggered, matching the v0.6.0 release plan's D2 decision (Option A: leave the entire trigger surface alone this release), and leave a pointer so a future reader does not wonder why C-03 shipped without also reopening D-01's (the roadmap's D-1) removed trigger phrases.

**Files:** Verify only, no edits to `skills/plab-continue-session/SKILL.md`'s `description` field or its "When NOT to Use" section. One documentation-only addition to `skills/plab-continue-session/references/cold-repo-orientation.md`.

**Fulfills:** AC-8, AC-9

**Steps:**
- [ ] Step 1: Diff the current `description` field and the current "When NOT to Use" section against a pre-effort git baseline (`git show <pre-effort ref>:skills/plab-continue-session/SKILL.md`, where `<pre-effort ref>` is the commit or tag before this effort's Phase 1 started) and confirm zero difference in each (AC-8, AC-9). If either differs, undo the unintended change before proceeding to Phase 4; this phase's job is to confirm, not to introduce, a difference. A git-based diff is used rather than a scratch-note snapshot taken before Phase 1, since phases execute in order and Phase 3 runs after Phase 1 and Phase 2 are already done.
- [ ] Step 2: In `references/cold-repo-orientation.md` (built in Phase 1), add one sentence near the top noting that whether a bare status question like "where were we" should also reach this orientation path was considered and deliberately deferred, citing `docs/internal/release-plans/plan_05_reconcile-at-resume/plan.md` decision D2 by name. This is a documentation-only addition; it changes no behavior and adds no trigger.
- [ ] Step 3: Confirm no step in Phase 1 or Phase 2 touched `docs/skills/plab-continue-session/README.md`'s or `AGENTS.md`'s existing "When NOT to Use" / status-question language. Both stay exactly as `plab-continue-session` 1.4.0 left them.

**Verification:** Diff `skills/plab-continue-session/SKILL.md`'s frontmatter block, and its "When NOT to Use" section, against the pre-effort git baseline from Step 1; confirm zero byte difference in both (AC-8, AC-9). Grep `docs/skills/plab-continue-session/references/cold-repo-orientation.md` for "D2" to confirm the cross-reference from Step 2 landed. Grep `docs/skills/plab-continue-session/README.md` and `AGENTS.md` for any change to their status-question language and confirm there is none.

---

## Phase 4: Version, HISTORY, and surrounding documentation

**Goal:** Ship the version bump and bring every document that describes this skill's behavior into agreement with it.

**Files:** Modify `skills/plab-continue-session/SKILL.md` frontmatter (`metadata.version`), `skills/plab-continue-session/HISTORY.md`, `CHANGELOG.md`, `docs/skills/plab-continue-session/README.md`, `AGENTS.md`, `library.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `manifest.generated.json`, root `README.md` (skill version table)

**Fulfills:** N/A (documentation and release housekeeping; no new capability introduced in this phase)

**Steps:**
- [ ] Step 1: Confirm whether the `1.4.0` to `1.5.0` version bump already landed via C-02's implementation. If it did, do not bump again; if it did not (this effort's implementation is running first), bump `skills/plab-continue-session/SKILL.md` `metadata.version` to `1.5.0` and `updated` to the ship date here, and leave a note for whoever executes C-02 that the bump is already done.
- [ ] Step 2: Add this effort's half to the shared `1.5.0` entry in `skills/plab-continue-session/HISTORY.md`: the cold-repo orientation path, the 30-day staleness branch, and an explicit line stating that neither the `description` field nor the "When NOT to Use" section changed (AC-8, AC-9; per the v0.6.0 release plan's D2 decision). If C-02 already started this entry, extend it; do not create a second `1.5.0` heading.
- [ ] Step 3: Extend the same `CHANGELOG.md` release entry (started by C-02, or start it here if this effort executes first) with this effort's user-facing framing: no more dead-end menu; a missing or stale log now produces a real answer built from git history, issues and PRs, and, when present, capture-lite records.
- [ ] Step 4: Update `docs/skills/plab-continue-session/README.md`: replace "Example 3: No Log Found," which currently shows the old two-bullet menu, with the new cold-repo orientation example; bump the Version line to `1.5.0` if C-02 has not already done so. Do not touch the "When NOT to Use" list; it is unchanged (AC-9).
- [ ] Step 5: Add one clause to `AGENTS.md`'s `plab-continue-session` blurb describing the cold-repo orientation capability (what happens when no log exists or the newest is stale). Do not touch the blurb's existing status-question sentence ("Does not fire on status questions; those get answered directly"); it is unchanged (AC-9). Coordinate with C-02 if both effort implementations touch this blurb in the same session.
- [ ] Step 6: Bump the `plab-continue-session` component version to `1.5.0` in `library.json`, and the top-level version in `library.json`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json` to `0.5.0` (shared with C-02; do not duplicate if already done). Regenerate `manifest.generated.json` from `library.json` using the command named in `AGENTS.md` ("Build and validate"); never hand-edit it directly, per `release-checklist.yaml`'s stated reason for that row. Bump the Version column for `plab-continue-session` in the root `README.md` skill table if C-02 has not already done so.

**Verification:** `git diff --stat` shows every file listed above touched, including `manifest.generated.json` and the root `README.md` skill table. Grep `docs/skills/plab-continue-session/README.md` for the old "No prior session log found" dead-end text to confirm "Example 3" no longer shows it verbatim. Grep `AGENTS.md` and `docs/skills/plab-continue-session/README.md` for their existing status-question language and confirm it is byte-for-byte unchanged. Grep the same files C-02 checked for `1.5.0` and `0.5.0` to confirm no duplicate or conflicting bump was written.

---

## CI and Documentation Coverage

### CI

No CI change. This repository has no `.github/` directory yet; CI-01 bootstraps it in v0.4.0, which ships before this release. This effort adds no rung-1 (CI or hook) check and no new detector; it adds new agent-followed instructions (the orientation mechanism) and a verification step confirming the trigger surface did not move, neither of which is code a canary could exercise. The one place a future CI check could plausibly help, catching a description-field or "When NOT to Use" diff automatically so AC-8 and AC-9 do not rely on a human or agent remembering to diff them by hand, is noted as a candidate for CI-01 or a later hygiene-sweep check, not built here.

### Agent-facing documentation

- `skills/plab-continue-session/SKILL.md`: Phase 1 gains a no-log and stale-log routing step, the References table gains an entry, `metadata.version` bumps. The `description` field and the "When NOT to Use" section are both explicitly unchanged (AC-8, AC-9), matching the v0.6.0 release plan's D2 decision.
- `skills/plab-continue-session/references/cold-repo-orientation.md`: new file, the complete mechanism (AC-2 through AC-6), plus the one-sentence cross-reference to D2 added in Phase 3.
- `skills/plab-continue-session/references/log-discovery.md`: the dead-end menu is replaced, and the 30-day staleness branch is added alongside the existing 7-day warning.
- `AGENTS.md`: the `plab-continue-session` blurb gains one clause describing the cold-repo orientation capability; its existing status-question sentence is unchanged.

These are runtime configuration read by an agent every time the skill fires; the AC-8 and AC-9 diff checks exist specifically because a stale or accidentally-widened trigger surface here would poison every future session's routing, not just this one.

### Human-facing documentation

- `docs/skills/plab-continue-session/README.md`: version line, replaced "Example 3." The "When NOT to Use" list is unchanged.
- `CHANGELOG.md`: the shared v0.6.0 entry's C-03 half, in the established "what changes for you / what does not change" style.
- `skills/plab-continue-session/HISTORY.md`: the shared `1.5.0` entry, co-written with C-02's half.
- Root `README.md`: the skill version table's `plab-continue-session` row (shared with C-02; do not duplicate).
- `manifest.generated.json`: regenerated, never hand-edited, per `release-checklist.yaml`'s explicit row for this file.

A reader returning after three months should be able to read the README's replaced example alone and understand that a missing or stale log is no longer a dead end, without needing to read this plan, the source roadmap, or the release plan's D2 decision that explains why the trigger phrases themselves were left alone.

---

## Rollback

Revert `SKILL.md` (the Phase 1 routing step only; the `description` field and "When NOT to Use" section were never touched, so there is nothing to revert there), `log-discovery.md`, `cold-repo-orientation.md` (including its one-sentence D2 cross-reference), and the version and documentation changes, in a single commit revert. Because AC-8 and AC-9 guarantee the entire trigger surface is untouched throughout this effort, rollback carries zero routing risk: the skill's trigger surface is identical before, during, and after, so reverting cannot reintroduce or remove any over-triggering behavior. No data migration is needed; the orientation is computed live at invocation time and never written anywhere.
