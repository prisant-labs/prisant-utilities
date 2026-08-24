---
id: D-03
title: "Implementation plan: Make the documentation-drift check bidirectional"
type: implementation-plan
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.3.0/plan_v0.3.0.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: Make the documentation-drift check bidirectional

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Make Check 4 of the pre-wrap hygiene sweep catch content changed with no version bump, not only a version bumped with a stale doc, so the confirmed real defect (`plab-continue-session` changed behavior at commit `38a75f0` while `metadata.version` stayed `"1.2.0"`) is a class the sweep can name going forward.

**Architecture:** One documented git recipe added to `hygiene-sweep.md` Check 4 (no new script, matching Check 4's existing pattern), plus a matching one-line summary update in `SKILL.md`. Both edits are text-only; the recipe itself was dry-run against this repository during planning (see Phase 1 verification) and produces zero false positives against the current tree.

**Spec:** `spec.md`
**Target versions:** `plab-wrap-session` 1.6.0, shipping in plugin v0.3.0 alongside CI-01 (CI bootstrap), D-04 (capture-lite consumers), D-05 (superseding logs), D-06 (resumed-from semantics), D-07 (Waiting-on blocker contract), D-11 (three-state gate canaries), and D-12 (path-citation precision). `plab-continue-session` is not touched by this effort (see spec Non-Goals).

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) in any file this touches. Use " - " or restructure.
- State the check's logic once, in `hygiene-sweep.md`'s Check 4 recipe. `SKILL.md`'s one-line summary references what the recipe does at a higher altitude; it must not restate the recipe's mechanics in different words that could drift from them.
- Archive, never delete: not applicable directly; this effort edits reference text and adds no new files.
- Token economy: this effort adds no characters to any skill's `description:` frontmatter field. The new recipe lives in a `references/*.md` file, loaded only when the sweep runs, and the `SKILL.md` change is one clause inside body content already loaded on invocation.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Write the bidirectional recipe in `hygiene-sweep.md` Check 4 | AC-1, AC-2, AC-4, AC-5 | agent | Not started |
| P2 | Extend `SKILL.md`'s one-line Check 4 summary | AC-3 | agent | Not started |
| P3 | Version bump and documentation coverage | (packaging for AC-1 through AC-5) | agent | Not started |

---

## Phase 1: Write the bidirectional recipe in `hygiene-sweep.md` Check 4

**Goal:** Check 4 detects content-changed-but-unbumped and missing-HISTORY-entry, scoped to skill directories with diffs since the last tag, degrading gracefully with no tags or a skill new since the last tag.
**Files:** Modify `skills/plab-wrap-session/references/hygiene-sweep.md`.
**Fulfills:** AC-1, AC-2, AC-4, AC-5

**Steps:**
- [ ] Step 1: Replace `## Check 4: Documentation drift` (currently lines 40-46) with:

  ```markdown
  ## Check 4: Documentation drift

  Compare what the session changed against what documents it, in both directions.

  Stale docs, caught by reading:

  - Skill or component version bumped but its usage doc still shows the old version
  - Feature behavior changed but README or reference docs describe the old behavior
  - Work completed with no CHANGELOG entry where the repo maintains one

  Unbumped versions, caught by this recipe. For each skill directory with content
  changed since the last tag, its `metadata.version` should have moved; if it did
  not, or if `HISTORY.md` has no entry for the version currently shipping, that is
  a finding:

  ```bash
  LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
  if [ -z "$LAST_TAG" ]; then
    echo "No tags yet; version-drift comparison has nothing to compare against, skipped."
  else
    for dir in skills/*/; do
      skill=$(basename "$dir")
      skill_file="${dir}SKILL.md"
      history_file="${dir}HISTORY.md"
      git cat-file -e "$LAST_TAG:$skill_file" 2>/dev/null || continue    # new since last tag, skip
      git diff --quiet "$LAST_TAG" HEAD -- "$dir" && continue            # unchanged, skip
      head_version=$(grep -m1 'version:' "$skill_file" | sed -E 's/.*"([^"]+)".*/\1/')
      tag_version=$(git show "$LAST_TAG:$skill_file" | grep -m1 'version:' | sed -E 's/.*"([^"]+)".*/\1/')
      [ "$head_version" = "$tag_version" ] && echo "FINDING: $skill changed since $LAST_TAG but metadata.version is still $head_version"
      grep -qE "^\| $head_version \|" "$history_file" 2>/dev/null || echo "FINDING: $skill/HISTORY.md has no entry for version $head_version"
    done
  fi
  ```

  Flag: content changed with the version identical to the last tag; a skill's
  `HISTORY.md` missing an entry for the version currently in its `metadata.version`.
  Skip silently, not as a finding: a skill with no diff since the last tag, and a
  skill that did not exist at the last tag.
  ```

**Verification:**

Two checks, both already run once during the authoring of this plan with the results shown.

1. **Live dry run against this repository today**, confirming no false positives:

   ```
   $ LAST_TAG=$(git describe --tags --abbrev=0); echo "Last tag: $LAST_TAG"
   Last tag: v0.2.0
   ```

   Running the Step 1 recipe against the current tree reports exactly one line: `OK (version bumped): plab-guide 2.2.1 -> 2.2.2` (adapt the recipe's echo statements to show non-findings during manual testing; the shipped version only echoes findings). This matches the CHANGELOG `[Unreleased]` entry recording `plab-guide` 2.2.2 as the one skill that changed since `v0.2.0`, and confirms the recipe does not flag a version that was, in fact, bumped correctly.

2. **Known-positive fixture, the confirmed real defect**, proving the comparison logic:

   ```
   $ git show 9c7f5ce:skills/plab-continue-session/SKILL.md | grep -m1 'version:'
     version: "1.2.0"
   $ git show 38a75f0:skills/plab-continue-session/SKILL.md | grep -m1 'version:'
     version: "1.2.0"
   $ git diff --stat 9c7f5ce 38a75f0 -- skills/plab-continue-session/SKILL.md
    skills/plab-continue-session/SKILL.md | 13 ++++++-------
    1 file changed, 6 insertions(+), 7 deletions(-)
   ```

   Content changed, version identical: the recipe's finding condition is met. See spec.md Behavior Example 2 and Open Question D1 for why this is run as a direct commit-pair replay rather than a live "last tag" run: the defect predates this repository's first tag, so no live tag-relative run can reproduce it today.

3. **Edge case (AC-5), a skill absent at the comparison ref:**

   ```
   $ git cat-file -e d44564b^:skills/plab-continue-session/SKILL.md; echo "exit=$?"
   fatal: path 'skills/plab-continue-session/SKILL.md' exists on disk, but not in 'd44564b^'
   exit=128
   ```

   Confirms the `git cat-file -e ... || continue` guard correctly skips a skill directory that did not exist at the comparison point, rather than erroring the whole recipe.

---

## Phase 2: Extend `SKILL.md`'s one-line Check 4 summary

**Goal:** The one-line summary `SKILL.md` shows in the Pre-Wrap Hygiene Sweep list names both directions, matching what `hygiene-sweep.md` now checks.
**Files:** Modify `skills/plab-wrap-session/SKILL.md`.
**Fulfills:** AC-3

**Steps:**
- [ ] Step 1: In the Pre-Wrap Hygiene Sweep numbered list (currently line 56), replace:

  ```
  4. **Documentation drift.** User or technical docs this session made stale: version tables, skill or feature READMEs vs source of truth, missing CHANGELOG entries.
  ```

  with:

  ```
  4. **Documentation drift, both directions.** User or technical docs this session made stale: version tables, skill or feature READMEs vs source of truth, missing CHANGELOG entries. Also: a skill's content changed with no version bump, or no HISTORY.md entry for the version currently shipping.
  ```

**Verification:** `grep -n "both directions" skills/plab-wrap-session/SKILL.md` returns the updated line. Read the surrounding paragraph and `references/hygiene-sweep.md` Check 4 side by side and confirm neither describes the check in terms the other contradicts.

---

## Phase 3: Version bump and documentation coverage

**Goal:** `plab-wrap-session` ships at 1.6.0 with accurate HISTORY, manifest, and human-facing version references.
**Files:** Modify `skills/plab-wrap-session/SKILL.md`, `skills/plab-wrap-session/HISTORY.md`, `library.json`, `README.md`, `CHANGELOG.md`.
**Fulfills:** Packaging for AC-1 through AC-5 (no single AC maps to this phase).

**Steps:**
- [ ] Step 1: `skills/plab-wrap-session/SKILL.md` frontmatter: `version: "1.5.0"` to `version: "1.6.0"` (skip if D-07 (Waiting-on blocker contract) or another v0.3.0 effort has already made this edit); bump `updated:` to the ship date.
- [ ] Step 2: `skills/plab-wrap-session/HISTORY.md`: add this effort's paragraph describing the bidirectional Check 4 to the `1.6.0` entry. If D-07 or another v0.3.0 effort already opened the `1.6.0` table row and section, add to it rather than duplicating the row.
- [ ] Step 3: `library.json`: confirm or bump the `plab-wrap-session` component version (currently line 32) to `1.6.0`.
- [ ] Step 4: Root `README.md`: confirm or bump the `plab-wrap-session` version-table entry (currently line 11) to `1.6.0`.
- [ ] Step 5: `CHANGELOG.md`: add or extend an entry under `[Unreleased]` (or a new `v0.3.0` heading if already cut) in plain English: the hygiene sweep now catches a skill whose behavior changed without its version number moving, which is the same class of defect the `[Unreleased]` section's existing "documentation correctness" theme already covers.

**Verification:** `grep -n "1.6.0" skills/plab-wrap-session/SKILL.md library.json README.md` shows a consistent version string across all three files. `grep -c "^| 1\.6\.0" skills/plab-wrap-session/HISTORY.md` returns `1`, not more, confirming no duplicate row from coordinating with the other v0.3.0 efforts that also land in `plab-wrap-session` 1.6.0.

---

## CI and Documentation Coverage

### CI

No CI change; the repository has no `.github/` directory (greenfield, per conventions section 10). This effort is verified by the recipe itself, run live during the sweep, and by the two dry runs recorded in Phase 1's verification.

Mechanization ladder rung: **rung 3** (documented convention: a git-command recipe the wrapping agent runs during the sweep, read directly by the agent, not automated in CI and not a committed script). This matches Check 4's existing rung; Check 5 is the sweep's only script-backed check, and only because it shares a code path with `--organize`'s own dry run [spec.md S3]. This effort does not promote Check 4 to rung 2; the source explicitly names a plugin-root script as the fallback "if it ever feels slow" and explicitly defers building it now, a deferral this plan keeps. It also does not need D-11's three-state canary discipline (clean / findings / broken): that discipline is scoped to the two Log Self-Check gates backed by a text-matching detector that can silently fail to match its pattern. This recipe is a direct git-command comparison whose output the agent reads and reports; there is no pattern-match step that can fail open the way an unescaped regex can.

### Agent-facing documentation

- `skills/plab-wrap-session/references/hygiene-sweep.md`: Check 4 gains the bidirectional recipe (AC-1, AC-2), with graceful skips for no-tags and new-since-tag skills (AC-4, AC-5).
- `skills/plab-wrap-session/SKILL.md`: Check 4's one-line summary extended to name both directions (AC-3); `metadata.version` bumped to 1.6.0.
- `skills/plab-wrap-session/HISTORY.md`: new `1.6.0` entry (or addition to one opened by a co-landing v0.3.0 effort) recording this change.

These are runtime configuration read at invocation. A stale line here poisons every future wrap's sweep, so both edits above must match what Phase 1 and Phase 2 actually shipped.

### Human-facing documentation

- Root `README.md`: version-table entry for `plab-wrap-session` updated to 1.6.0 (shared step with any other v0.3.0 effort landing in the same version; see Phase 3).
- `CHANGELOG.md`: `[Unreleased]` entry in plain English, extending the existing "documentation correctness" theme already present there: a reader away for three months should understand that the hygiene sweep now catches a skill that changed behavior without its version number moving, not only the reverse.
- `docs/skills/plab-wrap-session/README.md`: no change strictly required; its hygiene-sweep description (around the Deep mode section) already describes "doc drift" at a summary level that remains accurate under the extended check. Confirm during Phase 3 that no line there asserts only the single direction this effort now supersedes; if one does, correct it in the same per-action-confirmation manner the skill itself uses for its own doc updates.

## Rollback

Both substantive edits (Phase 1's recipe, Phase 2's one-liner) are same-file text changes to `hygiene-sweep.md` and `SKILL.md`; reverting the commit that ships this effort restores the prior, one-directional Check 4 exactly, with no data migration to undo. The recipe is read-only (it only echoes findings; it changes nothing in the repository), so there is no cleanup step beyond the text revert itself. If the recipe produces false positives in practice that Phase 1's dry run did not anticipate, the fallback is to revert Phase 1 only, keeping Phase 2's one-line summary reverted alongside it so the two do not drift back out of sync with each other.
