---
id: C-02
title: Reconcile the Session Log Against Repo Reality at Resume
type: spec
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-effort: _local/skill-roadmaps/2026-08-16/continue-session.md
linked-plan: implementation-plan.md
ac-count: 9
source-count: 9
requires-human-review: true
target-release: v0.6.0
linked-release: docs/internal/release-plans/plan_05_reconcile-at-resume/plan.md
priority: P1
---

# Spec: Reconcile the Session Log Against Repo Reality at Resume

## Task Summary

**Status:** draft
**Last updated:** 2026-08-23
**Linked plan:** `implementation-plan.md`
**Open questions:** 3 (see Open Questions / Decisions)
**Revisions:** 1 (initial draft; see Revisions)

### Acceptance Criteria Fulfillment

- [ ] AC-1: Leading delta section exists and is positioned before "Waiting on you"
- [ ] AC-2: Remote and tag state is collected by reusing hygiene-sweep Check 1's commands
- [ ] AC-3: Commit count uses `commit-sha` when present, a date-based fallback otherwise
- [ ] AC-4: Release-cut detection compares tag creation dates against the log's date
- [ ] AC-5: Branch existence is checked locally and on the remote
- [ ] AC-6: Continuation-prompt file paths are existence-checked with a rename hint on failure
- [ ] AC-7: A next-action-already-done signal is surfaced as an advisory flag
- [ ] AC-8: A check that cannot complete reports itself broken, never silently clean
- [ ] AC-9: The reconciliation step never mutates repository state

### Currently In Progress

None.

## Purpose

This effort is the roadmap's C-2 (zero-padded here to C-02 per this document set's ID convention). `plab-continue-session` 1.4.0 (the version it will carry into this release after v0.4.0 ships) replays a session log's claims without checking them against the repository. C-02 closes that gap: at resume, the skill derives current repository state (commits, tags, branch existence, file existence) and diffs it against what the log claimed, then leads the resumption display with that delta rather than burying it below the fold. This corrects a named asymmetry: `plab-wrap-session` 1.5.0 already runs a pre-wrap hygiene sweep that checks remote divergence and release state before writing a log, and the read side has never run the equivalent check before acting on one. This effort adds no capability to `plab-wrap-session`, which ships unchanged in v0.6.0 per the release ladder.

## Scope

### In Scope

- A new reconciliation step in `plab-continue-session`'s workflow, run after the log is read and parsed and before the resumption context is displayed.
- A new reference file documenting the git commands, the fallback logic for logs missing optional fields, and the explicit broken-state reporting rule.
- An update to the resumption display's required structure so the delta leads it.
- The version 1.4.0 to 1.5.0 bump for `plab-continue-session` (shared with C-03 in the same v0.6.0 release; see the implementation plan's coordination note).
- Updates to `HISTORY.md`, `CHANGELOG.md`, the skill's usage README, and `AGENTS.md` reflecting the new behavior.

### Non-Goals

- Does not modify `plab-wrap-session`. The release ladder fixes it unchanged at 1.6.0 (the version it reaches in v0.4.0) for v0.6.0.
- Does not reimplement `claude --resume`. Native resume remains the cheap path when no boundary was crossed; this skill's territory stays the cross-machine, cross-agent, cross-time gap, per the roadmap's "What not to do" section.
- Does not merge `plab-continue-session` into `plab-wrap-session`. The write/read pair separation stands.
- Does not implement C-04 (consumption disposition: fulfilled, superseded, or ignored), the roadmap's C-4, which ships in v0.9.0. This effort's delta output is a natural future input to that disposition tracking, but no wiring between them is built now.
- Does not implement C-05 (resume the arc: reading multiple logs), the roadmap's C-5, which ships in v0.8.0.
- Does not take remediating action on any finding. No auto-pull, no auto-checkout, no edit to the log being resumed from. The delta is diagnostic display only (AC-9).
- Does not add a CI-enforced, canary-tested detector. See the implementation plan's CI and Documentation Coverage section for why this is a documented convention, not a script.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer (JP) | The person resuming work in a repository | Reads the delta block, decides whether to proceed with the log's named next action, redirect, or investigate a flagged discrepancy further |
| Agent (the LLM or harness invoking `/plab-continue-session`) | Executes the reconciliation and presents it | Runs the git checks, computes the delta, reports a broken check honestly instead of silently omitting it, never acts on a finding without the maintainer's confirmation |

## Requirements

1. At resume, before any log content is presented as though it were current, the skill must derive live repository state and compare it against what the log claims, per the roadmap's central instruction to "derive the current state and diff it against the log's claims, then lead with the delta." [S1]
2. The comparison must cover, at minimum, the five categories of drift the roadmap names explicitly: commits landed, a release cut elsewhere, the named next action already done, the branch moved or no longer existing, and a file the continuation prompt points at having been renamed. [S1]
3. Remote and tag state collection must reuse the git command sequence already defined and shipped in `hygiene-sweep.md` Check 1, rather than defining a parallel implementation, per the explicit instruction to reuse rather than reinvent. [S3]
4. The mechanism must work uniformly across logs written with and without the optional `commit-sha` field, since that field is Tier 3 ("nice to have") today and `plab-wrap-session` is unchanged in this release, so a log lacking it is a normal case this effort must handle, not an edge case it can ignore. [S7]
5. Any check that cannot complete (network unavailable, git command errors, a fetch that times out) must report its own failure explicitly. The absence of a finding must never be presented in a way indistinguishable from a verified clean result. [S2]
6. The effort must not add any capability for the skill to modify repository state. The existing "never modify the session log being resumed from" and related constraints continue to apply to the new step. [S4]
7. The effort must not grow the skill's always-on YAML `description`. All new instruction content belongs in the SKILL.md body and a new reference file, both of which are loaded only on invocation, consistent with this repository's standing token-economy principle. [S8]

## Acceptance Criteria

**AC-1:** A new leading section, titled "What changed since this log," appears in the resumption display between the `## Resuming from` header and the `**Last session:**` facts line, ahead of `### Waiting on you`. [S1]

**AC-2:** The delta's remote-and-tag content (branch ahead/behind counts versus its remote, and any tags visible on the remote) is produced using the same command sequence as `hygiene-sweep.md` Check 1: `git fetch origin --tags`, `git status -sb`, `git log --oneline HEAD..@{u}`, `git log --oneline @{u}..HEAD`, `git ls-remote --heads origin`, and `git tag -l | tail -5`. [S1][S3]

**AC-3:** Commits landed since the log was written are counted correctly whether or not the log's `commit-sha` field is present: via `git rev-list --count <sha>..HEAD` when present, or via `git log --since=<log date> --oneline` on the log's branch when absent. [model-inference]

**AC-4:** A release cut after the log was written is detected by comparing each tag's creation date (`git for-each-ref refs/tags --sort=-creatordate --format='%(refname:short) %(creatordate:short)'`) against the log's `date` frontmatter field, independent of any tag information recorded in the log itself. [model-inference]

**AC-5:** The delta reports whether the log's `branch` field still exists, both locally (`git branch --list <branch>`) and on the remote (`git ls-remote --heads origin <branch>`). This check is additive to, and distinct from, the existing current-branch-mismatch warning already defined in `references/handoff-display.md`, which only fires when the current branch differs from the log's branch and says nothing about whether the log's branch still exists at all. [model-inference]

**AC-6:** A file path named in the continuation prompt is scoped for checking using the same three-way rule D-12 (path-citation precision) already adopted: a citation containing a path separator is checked for existence and, if missing, gets a rename-hint attempt via `git log --follow --diff-filter=R -- <path>` before being reported as missing; a backtick-wrapped citation with no separator is resolved against the repository root and produces no finding whether it resolves or not, matching D-12's own adopted behavior for that branch exactly rather than a looser reading of it; a bare prose word carrying a file extension, with neither signal, is excluded from checking entirely. [S2][S9]

**AC-7:** Given/When/Then. Given a continuation prompt naming a next action tied to specific files, when commits have landed since the log that touch those same files, then the delta states that the named next action may already be complete and asks the maintainer to verify before proceeding, rather than asserting completion as fact. [model-inference]

**AC-8:** Given/When/Then. Given any step of the delta computation cannot complete (git unavailable, the fetch fails, the fetch times out, the repository is offline), when the resumption display is produced, then the delta section names which specific check failed and states that reconciliation is incomplete, rather than omitting the section or presenting an unqualified "no changes found" result. [S2]

**AC-9:** The reconciliation step executes no git command that mutates repository state: no `pull`, `merge`, `checkout`, `reset`, `push`, or equivalent appears anywhere in the delta's command set. [S4]

## Behavior / Examples

### Example 1: Drift found, log resumed with informed context

```
## Resuming from: 2026-08-10_09-15_claude_v1.9.0-prep.md

### What changed since this log

Log written 2026-08-10 at `fa13177`. Since then: 4 commits on `main`
(3 local, 1 pulled from origin), tag `v1.9.0` cut from another checkout,
and `skills/plab-guide/SKILL.md`, named in the continuation prompt's next
action, was modified in commit `9c2a441`. The stated next action ("bump
plab-guide's version line") may already be complete; verify before
repeating it.

**Last session:** 2026-08-10T09:15:00-07:00, claude opus 4.6, status `completed`
**Summary:** Prepped the v1.9.0 release notes
**Branch:** `main`

### Waiting on you
...
```

This mirrors the worked example already in the source roadmap and adds the file-overlap advisory from AC-7. [S1]

### Example 2: Reconciliation cannot complete

```
## Resuming from: 2026-08-15_14-02_claude_docs-cleanup.md

### What changed since this log

Reconciliation incomplete: `git fetch origin --tags` did not return
(offline or origin unreachable). Local-only facts: no new commits on
`main` since this log's date. Remote state, tags, and branch existence
on the remote could not be verified this run.

**Last session:** 2026-08-15T14:02:00-07:00, claude opus 4.6, status `completed`
...
```

The section still appears, still names what it could and could not verify, and never implies a clean result it did not earn (AC-8).

### Example 3: Branch no longer exists

```
### What changed since this log

Log written 2026-08-01 on branch `feature/spec-gates`. That branch no
longer exists locally or on origin; it was likely merged and deleted.
Currently on `main`. Confirm before resuming whether this work already
landed.
```

This is distinct from the existing branch-mismatch warning (which fires when the current branch merely differs from the log's) because here the log's branch is gone entirely (AC-5).

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token cost | No growth to the always-on `description`; new instruction content lives only in the SKILL.md body and a new reference file, loaded on invocation | [S8] |
| Latency | `git fetch origin --tags` adds a network round trip at the start of a session, when the maintainer wants to get moving; the check must be time-boxed and degrade to the AC-8 broken-state report rather than hang indefinitely | [S3] |
| Reliability | The delta must not fail open: a git command that errors must produce an explicit "could not verify" state, never a silently-empty "no changes" result | [S2] |
| Compatibility | The mechanism must produce correct output for logs written by `plab-wrap-session` 1.2.0 through the current version, including logs that predate `commit-sha` ever being populated | [S7] |

## Revisions

| Date | Revision | Author |
|---|---|---|
| 2026-08-23 | Initial draft created | Claude (agent) |

## Sources & Evidence

[S1] `_local/skill-roadmaps/2026-08-16/continue-session.md` (maintainer-local, gitignored), section "C-2. Reconcile the log against reality, do not just replay it." Credibility A: first-party, maintainer-authored design intent, read in full. This document's C-02 is the roadmap's unpadded C-2.

[S2] `_local/skill-roadmaps/2026-08-18/pair-defects.md` (maintainer-local, gitignored), entries D-11 ("The Log Self-Check gates are two-state and can fail open") and D-12 ("The path-existence gate treats bare filenames as repo-relative paths"). Credibility A: first-party, verified-against-file-and-line defect record, read in full. D-11 and D-12 are already two-digit in the source and need no repadding; this spec follows the same precision rule D-12 established for its own gate rather than restating a looser one.

[S3] `skills/plab-wrap-session/references/hygiene-sweep.md`, Check 1 ("Remote reconciliation"), the exact command block this effort reuses. Credibility A: shipped, in-repo, read in full.

[S4] `skills/plab-continue-session/SKILL.md`, the current Phase 1 through Phase 5 workflow and the Constraints section (including "Never modify the session log being resumed from"). Credibility A: shipped, in-repo, read in full.

[S5] `skills/plab-continue-session/references/log-discovery.md`, the existing age-warning (7-day threshold) and repo/branch-mismatch mechanisms this effort extends without replacing. Credibility A: shipped, in-repo, read in full.

[S6] `skills/plab-continue-session/references/handoff-display.md`, the current required display structure this effort adds a leading section to. Credibility A: shipped, in-repo, read in full.

[S7] `skills/plab-wrap-session/references/frontmatter-schema.md`, Tier 2 (`resumed-from`) and Tier 3 (`commit-sha`) field definitions. Credibility A: shipped, in-repo, read in full.

[S8] `AGENTS.md`, line 17: "Always-on context cost is paid by one person in every session, forever." Credibility A: shipped, in-repo, read in full.

[S9] `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-12_path-citation-precision/spec.md`, AC-1 through AC-3, the committed three-way scoping rule (path separator checked and flagged; backtick-wrapped-no-separator resolved with no finding either way; bare word excluded entirely). Credibility A: a sibling effort's own spec in this document set, read in full; cited directly rather than re-deriving the rule from the underlying roadmap entry, since D-12 already resolved the ambiguity in the source prose that its own Open Questions section flags.

### Unverified Claims

- AC-3, AC-4, AC-5, AC-7, and the rename-hint half of AC-6 (the git-level mechanisms for the commit-sha/date fallback, the tag-creation-date comparison, the branch-existence check, the file-overlap heuristic, and the rename-hint attempt on a missing path) are not themselves named at this level of detail in any source. They are this document's own design synthesis and should be reviewed before an agent implements them without discussion. AC-6's scoping rule itself (which citations get checked at all) is no longer inferential: it now cites D-12's committed spec [S9] directly rather than this document's own reading of the underlying roadmap prose.

## Open Questions / Decisions

| ID | Question | Status |
|---|---|---|
| OQ1 | Should the next-action-already-done signal (AC-7) ever hard-block proceeding, rather than only flagging? | Open |
| OQ2 | Should `plab-wrap-session` eventually promote `commit-sha` from Tier 3 to Tier 1, removing the need for AC-3's date-based fallback? | Open, deferred |
| OQ3 | What is the exact timeout budget for the `git fetch origin --tags` call before the delta must report itself broken due to a hang? | Open |

**OQ1: Hard-block or advisory-only for the next-action-already-done signal.**
The roadmap's own worked example treats this as informational ("The stated next action may already be complete"), which is what AC-7 implements. A stricter design could refuse to proceed with the named next action until the maintainer explicitly overrides. Held at advisory-only for this release because the underlying signal (file overlap between recent commits and the continuation prompt's text) is a heuristic, not a certainty, and a false hard-block would cost more than a false advisory note. Revisit after dogfooding shows the heuristic's actual false-positive rate.

**OQ2: Promoting `commit-sha` to Tier 1.**
AC-3's fallback exists specifically because `commit-sha` is Tier 3 today and `plab-wrap-session` ships unchanged in v0.6.0 per the release ladder. A Tier 1 promotion would collapse AC-3 to a single code path, but that is a `plab-wrap-session` change, out of scope here, and would need its own effort in a release where wrap is allowed to move. Noted for whoever plans a future wrap-side release.

**OQ3: Fetch timeout budget.**
`hygiene-sweep.md`'s own resolution protocol says to time-box the sweep without naming a number [S3]. This spec inherits that same non-numeric guidance rather than inventing a constant, because resume-time latency tolerance (a session just starting) may differ from wrap-time tolerance (a session already ending) in ways this spec has not measured. Left to implementation-time judgment, with the explicit requirement (AC-8) that a timeout must still produce a broken-state report, never a silent hang or a silently empty delta.
