---
id: D-03
title: Make the documentation-drift check bidirectional
type: spec
status: fulfilled
created: 2026-08-23
updated: 2026-08-24
linked-effort: the maintainer's private defect record for the wrap/continue pair, 2026-08-18
linked-plan: implementation-plan.md
ac-count: 5
source-count: 6
requires-human-review: true
target-release: v0.4.0
linked-release: docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md
priority: P1
---

# Spec: Make the documentation-drift check bidirectional

## Task Summary

**Status:** Fulfilled
**Last updated:** 2026-08-24
**Linked plan:** implementation-plan.md
**Open questions:** 1 (see Open Questions / Decisions)
**Revisions:** Initial draft created 2026-08-23.

### Acceptance Criteria Fulfillment

- [x] AC-1: Check 4 gains a recipe that flags content-changed-but-version-identical
- [x] AC-2: The same recipe flags a missing HISTORY.md entry for the current version
- [x] AC-3: SKILL.md's one-line Check 4 summary names both directions of drift
- [x] AC-4: The check degrades gracefully when the repository has no tags at all
- [x] AC-5: The check degrades gracefully when a skill directory did not exist at the last tag

### Currently In Progress

None.

## Purpose

The pre-wrap hygiene sweep's Check 4 (Documentation drift) catches a version bumped with a stale usage doc, but not the inverse: content changed with no version bump. That inverse is precisely the drift that shipped in this repository, confirmed independently by the roadmap's evidence, by this repository's own `plab-continue-session` HISTORY.md erratum entry, and by this spec's own verification against the actual commit that caused it [S1][S4][S5]. This spec extends Check 4 with a second, symmetric comparison so both directions of drift are caught by the same check, at the same mechanization rung it already occupies (a documented git recipe the wrapping agent runs live, not a new script), and updates `SKILL.md`'s one-line summary so it stops describing only half of what the detailed reference file checks.

## Scope

### In Scope

- Extending `skills/plab-wrap-session/references/hygiene-sweep.md` Check 4 with a runnable git-command recipe covering the new direction.
- Extending `skills/plab-wrap-session/SKILL.md`'s one-line Check 4 summary to match.
- Graceful degradation for a repository with no tags, and for a skill directory that did not exist at the last tag.
- The version bump and documentation coverage this effort contributes to the shared v0.4.0 release.

### Non-Goals

- Does not become a committed script or CI check. It stays a documented convention the wrapping agent executes live during the sweep, matching Check 4's existing pattern; Check 5 is the only check in this sweep backed by a script (`organize-logs.py`), and only because it shares a code path with `--organize`'s own dry run [S3].
- Does not retroactively re-scan every historical release for this drift pattern. The check only ever compares "since the last tag" going forward from whenever it ships; see Open Question D1 for what that means for the specific historical case used as this spec's verification fixture.
- Does not change Check 1, 2, 3, or 5, or the sweep's propose-then-per-action-confirmation resolution protocol.
- Does not add three-state canary discipline (clean / findings / broken). D-11 (three-state gate canaries, a separate v0.4.0 effort) scopes that discipline to the two Log Self-Check gates backed by a text-matching detector that can silently fail to match. This check is a direct git-command comparison the agent reads and reports, not a pattern-match with a false-clean failure mode of that shape.
- Does not touch `plab-continue-session`. This effort's change is entirely inside `plab-wrap-session`'s own hygiene sweep; only `plab-wrap-session` version-bumps for this specific effort (see Non-Functional Requirements).

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| The maintainer (JP) | Decides what to do with a finding | Reviews the proposed finding under the sweep's existing per-action confirmation protocol; bumps the version or adds the HISTORY entry, or declines |
| The wrapping agent | Runs the sweep every deep or final wrap | Executes the Check 4 recipe, including its new direction, and reports findings exactly as it already does for the sweep's other checks |

## Requirements

1. Check 4 must detect drift in both directions: version bumped with a stale usage doc (existing behavior), and content changed with no version bump (the actual defect that shipped). [S1][S4]
2. The new direction must be a runnable git recipe, not a script, matching Check 4's existing no-script pattern. [S1][S3]
3. A skill directory with no diff since the last tag is not checked at all; an unchanged skill is not a finding. [S1]
4. A missing `HISTORY.md` entry for the version currently at HEAD is a distinct finding from the version-unchanged finding, both scoped to skill directories with diffs since the last tag. [S1]
5. `SKILL.md`'s one-line Check 4 summary must not contradict the detailed recipe in `hygiene-sweep.md`; the two state the same check at different altitudes, per this repository's own rule that a contract lives in one place and everything else cites it. [S1][S2]
6. The check must degrade gracefully, skipping rather than crashing or false-flagging, when there is no last tag to compare against or when a skill directory did not exist at the last tag. [model-inference], corroborated by [S5]

## Acceptance Criteria

**AC-1:** `skills/plab-wrap-session/references/hygiene-sweep.md` Check 4 gains a git-command recipe that, for each `skills/*/` directory with a diff since the last tag, compares that directory's `SKILL.md` `metadata.version` value at HEAD against its value at the last tag, and reports a finding when the directory's content changed but the version string is identical. [S1][S3]

**AC-2:** The same Check 4 recipe reports a second, distinct finding when a skill directory (scoped the same way: diffs since the last tag) has no `HISTORY.md` entry for the version currently in `metadata.version` at HEAD. [S1][S3]

**AC-3:** `skills/plab-wrap-session/SKILL.md`'s one-line Check 4 summary in the Pre-Wrap Hygiene Sweep list is extended to name both directions of drift, so it no longer describes only the direction `hygiene-sweep.md` already checked before this effort. [S1][S2]

**AC-4:** When the repository has no git tags at all, the Check 4 drift comparison is skipped for every skill directory without error, and the sweep reports the skip rather than crashing on an absent tag reference or false-flagging every directory as drifted. [model-inference]

**AC-5:** When a skill directory did not exist at the last tag (added since), the comparison for that directory is skipped without error, rather than treating `git show`'s failure to find the file at that ref as a false "version identical" or crashing the sweep. [model-inference]

## Behavior / Examples

**Example 1: the mechanism, replayed against the confirmed real defect.** Commit `38a75f0` (2026-08-17) changed `skills/plab-continue-session/SKILL.md`'s description text while `metadata.version` stayed `"1.2.0"`, identical to its parent commit `9c7f5ce` [S5]. Running AC-1's comparison directly against that pair confirms the logic:

```
$ git show 9c7f5ce:skills/plab-continue-session/SKILL.md | grep -m1 'version:'
  version: "1.2.0"
$ git show 38a75f0:skills/plab-continue-session/SKILL.md | grep -m1 'version:'
  version: "1.2.0"
$ git diff --stat 9c7f5ce 38a75f0 -- skills/plab-continue-session/SKILL.md
 skills/plab-continue-session/SKILL.md | 13 ++++++-------
 1 file changed, 6 insertions(+), 7 deletions(-)
```

Content changed, version identical: exactly AC-1's finding condition. This is independently corroborated in prose by `skills/plab-continue-session/HISTORY.md`'s own 1.2.1 erratum entry, which names commit `38a75f0` directly and states plainly: "the gap that allowed it sits on the writing side: `plab-wrap-session`'s pre-wrap hygiene sweep checks documentation drift in one direction only" [S4].

**Example 2: the timing caveat, found while verifying this spec.** Commit `38a75f0` predates this repository's first tag: it is an ancestor of both `v0.1.0` and `v0.1.1` [S5]. By the time the 2026-08-17 22:15 wrap ran and reported "Documentation drift: none" [S6], HEAD equaled `v0.1.1` exactly, so a literal "diffs since the last tag" comparison run at that exact moment finds zero diff for `plab-continue-session`, because nothing had changed since the last tag: the defect was already baked into the tag itself before the tag existed to compare against. AC-1's comparison, run going forward from any tag, catches drift that accumulates after that tag; it cannot retroactively catch a defect that predates a repository's first-ever tag, because there is no earlier tag to diff against. See Open Question D1 for what this means for how the implementation plan frames its verification step.

**Example 3: missing HISTORY entry (AC-2), a related but distinct case.** At commit `38a75f0`, `HISTORY.md` for `plab-continue-session` already had a `1.2.0` entry (it was not missing); that entry's claim of "unchanged in behaviour from its last private version" simply became false the moment the commit landed [S4][S5]. AC-2's check would not have fired here; it catches an entry that is absent, not one that is present but inaccurate. The two findings are complementary, not the same finding under two names.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Performance / sweep cost | The recipe short-circuits per skill directory (skip when no diff since the last tag), so added cost scales with skills actually touched since the last tag, not the total skill count. Acceptable at today's five skills per the source's own estimate; the source names a plugin-root script as the fallback if this ever feels slow, and explicitly defers building that now. | [S1] |
| Mechanization ladder | Stays at rung 3 (documented convention, agent-run git commands), the same rung Check 4 already occupies. Not promoted to rung 2 (committed script) by this effort. | [S1], design frame (conventions section 3) |
| Correctness under edge cases | Must not crash or false-flag when there is no last tag, or when a skill directory did not exist at the last tag. Neither case is addressed in the source text; both are real conditions this repository will hit (a future skill added mid-cycle; any repository before its first tag). | [model-inference], corroborated by [S5] |

## Revisions

| Date | Change |
|---|---|
| 2026-08-23 | Initial draft created. |

## Sources & Evidence

- [S1] the maintainer's private defect record for the wrap/continue pair, 2026-08-18, section "D-3. The hygiene sweep checks documentation drift in one direction only" (lines 71-79). Class A: maintainer-authored roadmap with evidence verified against the shipped artifacts. Maintainer-local, gitignored, exists on disk.
- [S2] `skills/plab-wrap-session/SKILL.md`, line 56, the Check 4 one-line summary inside the Pre-Wrap Hygiene Sweep list ("**Documentation drift.** User or technical docs this session made stale: version tables, skill or feature READMEs vs source of truth, missing CHANGELOG entries."). Class A: the file this effort edits.
- [S3] `skills/plab-wrap-session/references/hygiene-sweep.md`, lines 40-46 (Check 4) and lines 48-56 (Check 5, cited for contrast: the sweep's only script-backed check, and why). Class A: the file this effort edits.
- [S4] `skills/plab-continue-session/HISTORY.md`, lines 44-54, the `1.2.1` "Erratum" entry. Class A: primary evidence, independently corroborates [S1]'s account and names the root cause on the writing side in the maintainer's own words.
- [S5] This repository's git history: commits `9c7f5ce` and `38a75f0`, and tags `v0.1.0` / `v0.1.1`. Class A: primary evidence, verified directly during this spec's authoring via `git show`, `git diff --stat`, `git log`, `git merge-base --is-ancestor`, and `git tag -l`.
- [S6] the session log of 2026-08-17 22:15, line 102 ("**Documentation drift:** none. `skills/` directories, AGENTS.md sections, README rows and `library.json` components all read 5."). Class A: primary evidence artifact, the real log that passed while sitting on the confirmed defect.

### Unverified Claims

- AC-4, AC-5, and Requirement 6 are [model-inference]: the source roadmap specifies the comparison ("for each skill directory with diffs since the last tag, compare `metadata.version` at HEAD against the same file at the tag") but does not address what happens when there is no last tag, or when a skill directory postdates the last tag. Both are this spec's addition, motivated directly by [S5]: this repository's own history shows the confirmed defect occurred in exactly that second condition (a skill new since the most recent prior state), one level up (repository-wide rather than per-skill).
- The Open Questions section below records that this spec's framing of the "regression test" (Behavior Example 2) departs from a literal reading of the source's claim that the 22:15 wrap "flags it" after this change ships. The mechanism itself (AC-1) is unchanged from the source's design; only the verification framing is adjusted, and only with the evidence shown.

## Open Questions / Decisions

| ID | Question | Status |
|---|---|---|
| D1 | How should the implementation plan frame the regression test against the confirmed real defect, given the timing caveat in Behavior Example 2? | Decided for this spec: direct commit-pair replay |

**D1: Regression test framing.** The source roadmap states that, after this change ships, "that same wrap flags it" [S1], referring to the 2026-08-17 22:15 wrap. Verified against this repository's actual git history (Behavior Example 2), that is true in the sense that matters: the comparison logic (content changed, version identical) correctly classifies the `9c7f5ce` to `38a75f0` pair as a finding when the two are compared directly. It is not true in the most literal sense of re-running "HEAD vs the last tag" at the exact historical moment of that wrap, because HEAD equaled the last tag (`v0.1.1`) at that point; the defect-introducing commit predates this repository's first tag entirely, so there was no earlier tag for that wrap to have diffed against. This is a boundary condition of any repository's first-ever release, not a flaw in the mechanism as specified, and this spec has not changed the mechanism: AC-1 still compares HEAD against the last tag, which is what correctly catches drift going forward from any release after the first. The implementation plan's verification step (see implementation-plan.md Phase 1) replays the recipe's comparison logic directly against the `9c7f5ce` / `38a75f0` commit pair rather than attempting a live run against current tags, which would find nothing, since the defect was fixed at `1.2.1` several tags ago. Flagging the choice here in case the maintainer wants the regression test framed differently.
