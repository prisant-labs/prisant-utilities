---
id: W-02
title: Derive session-log facts from git instead of model recall
type: spec
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-effort: the maintainer's private plab-wrap-session evolution roadmap, 2026-08-16
linked-plan: implementation-plan.md
ac-count: 9
source-count: 7
requires-human-review: false
target-release: v0.7.0
linked-release: docs/internal/release-plans/plan_06_derived-facts/plan.md
priority: P1
---

# Spec: Derive session-log facts from git instead of model recall

## Task Summary

**Status:** Draft
**Last updated:** 2026-08-23
**Linked plan:** `implementation-plan.md`
**Open questions:** 1 open, 2 decided and recorded below (see Open Questions / Decisions)
**Revisions:** Initial draft created 2026-08-23

### Acceptance Criteria Fulfillment

- [ ] AC-1: Environment fields (machine, repo, branch, date) come from the script, not manual commands
- [ ] AC-2: files-changed comes from `git diff --name-only`, grouped
- [ ] AC-3: Commit-range and latest-tag data derived without colliding with existing fields
- [ ] AC-4: decisions-count is a mechanical count, never a model estimate
- [ ] AC-5: Verification content is derived only when a real record exists; otherwise stays model-authored
- [ ] AC-6: The four judgment sections receive no script-generated content
- [ ] AC-7: Script path resolution follows the `organize-logs.py` precedent
- [ ] AC-8: Script is read-only, supports `--json`, and ships with a stdlib-only test script
- [ ] AC-9: `SKILL.md` is rewired to actually call the script

### Currently In Progress

None.

## Purpose

W-02 (the roadmap's W-2, zero-padded per this effort's ID scheme) adds `scripts/derive-log-facts.py` to `plab-wrap-session` and rewires the skill's own Evidence Gathering and Frontmatter instructions to run it, replacing model-recalled transcription of `files-changed`, `machine`/`repo`/`branch`/`date`, `decisions-count`, commit range, tags, and the verification table with values derived directly from git and the environment. Summary, Decisions Made, Waiting on You, and the Continuation Prompt stay entirely agent-authored, since judgment over those four is the actual point of the skill. [S1]

The case for this is not only token cost. A long session's early hours are the haziest part of the model's own context, and they are exactly where today's factual sections draw from, so derivation is the version that stays correct as sessions lengthen, not merely the version that is cheaper to produce. [S1]

## Scope

### In Scope

1. New file `skills/plab-wrap-session/scripts/derive-log-facts.py`: a stdlib-only Python script that derives the fields named in Requirements below.
2. New file `skills/plab-wrap-session/scripts/test-derive-log-facts.py`: fixture tests with no external test framework, matching the existing `test-organize-logs.py` precedent.
3. Edits to `skills/plab-wrap-session/SKILL.md`: the Evidence Gathering section and the "### Frontmatter" block, wiring the skill's own procedure to run the script and use its output; `metadata.version` bump to 1.7.0.
4. A new entry in `skills/plab-wrap-session/HISTORY.md` for 1.7.0.
5. Version bookkeeping owned by wrap alone: a `CHANGELOG.md` `[Unreleased]` bullet for wrap 1.7.0, wrap's row in root `README.md`'s skill table, wrap's `version` field in `library.json`, and a regeneration of `manifest.generated.json` and both `plugin.json` files via the existing generator (`AGENTS.md:73`).

### Non-Goals

1. Does not change what Summary, Decisions Made, Waiting on You, or the Continuation Prompt contain, or how they are authored. These stay fully model-written; that is the explicit point the source roadmap makes about this split. [S1]
2. Does not implement or repair W-1's capture-lite `SessionEnd` hook. The script may consume an existing capture-lite record where one is relevant, but building, fixing, or wiring that hook is a separate, already-tracked item (D-4) and is out of scope here. [S6]
3. Does not edit any file under `skills/plab-continue-session/`, any file under `skills/plab-wrap-session/references/`, or `docs/skills/plab-wrap-session/README.md`. Those restate the same log-format contract from the read side or the human-facing side, and consolidating them is D-10's territory, not this effort's. Touching them here would let two specs claim the same edit.
4. Does not commit to a specific frontmatter key name for commit-range or git-tag data without first checking it does not collide with the existing Tier 3 `tags:` field (topic keywords, `frontmatter-schema.md:50`) or `commit-sha` field (single SHA, `frontmatter-schema.md:49`). The exact name is left to implementation; colliding silently with an existing field is explicitly out of bounds (see AC-3).
5. Does not change the plugin-level version in `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json` beyond what the existing generator produces from `library.json`. The release-level `0.6.0` plugin version is the release plan's own gate to set, not a step in this effort's plan.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer (JP) | Runs and reads the output of wrap sessions | Reads the written log and continuation prompt; does not normally invoke the script directly |
| Wrapping agent (Claude Code or Codex running `plab-wrap-session`) | Executes the skill | Runs `derive-log-facts.py`, folds its output into the frontmatter and Files Changed section, then authors the four judgment sections |

## Requirements

1. The script must derive `machine`, `repo`, `branch`, and `date` from the environment (hostname, git remote or directory name, `git branch --show-current`, system clock) without the wrapping agent running its own equivalent commands and transcribing the result by hand. [S1, S3]
2. The script must derive `files-changed` from `git diff --name-only` against a caller-supplied base ref, grouped consistently with the "grouped by purpose if many" guidance already in `SKILL.md`'s Files Changed section. [S1, S2]
3. The script must derive commit-range and latest-tag information via `git log` and `git describe`, under a name or names that do not collide with the existing Tier 3 `commit-sha` (single SHA) or `tags` (topic keywords) fields already defined in `frontmatter-schema.md`. [S1, S3]
4. `decisions-count` in the written frontmatter must be a deterministic count of the drafted Decisions Made section's entries, computed after that section exists, never a number the model supplies from estimation or memory. [S1]
5. When a tool-call record or transcript is available for the current session, the script should surface verification-relevant facts into the Verification table's content. When none is available, including when only a capture-lite record exists (capture-lite fires at `SessionEnd` and therefore cannot describe a still-open session, per D-4's finding), the Verification section stays fully model-authored, with nothing presented as derived that was not actually derived. [S1, S6]
6. Summary, Decisions Made, Waiting on You, and the Continuation Prompt must receive no script-generated content; all four remain entirely agent-authored text. [S1]
7. The script must resolve its own path relative to the skill's own installed directory, and must treat any git-repository argument as relative to the project being wrapped, matching the resolution rule already shipped for `organize-logs.py`. [S2, S4]
8. The script must be read-only (it inspects git and the environment; it writes nothing to disk) and must support a `--json` output mode, matching `organize-logs.py`'s existing contract. A stdlib-only sibling test script must exercise it against fixture git repositories with no external test framework. [S4, S5]
9. `SKILL.md`'s Evidence Gathering section and its "### Frontmatter" block must be rewritten to call the script and use its output, rather than leaving the script and the skill's own manual-derivation prose as two disconnected paths. A committed script nothing calls is exactly the "producer with zero consumers" failure D-4 already found once in this pair; this requirement exists so W-02 does not repeat it. [S2, S6]

## Acceptance Criteria

**AC-1:** Running `derive-log-facts.py` inside a git checkout emits `machine`, `repo`, `branch`, and `date` values equal to `hostname`, the git remote (or directory name absent a configured remote), `git branch --show-current`, and the system clock, respectively, with none of the four requiring the wrapping agent to separately run git or shell commands to obtain them. [S1, S3]

**AC-2:** The script's output includes a `files-changed` list equal to `git diff --name-only` against a caller-supplied base ref, grouped per the existing "grouped by purpose if many" guidance at `SKILL.md:143`. [S1, S2]

**AC-3:** The script's output includes commit-range and latest-tag values derived from `git log` and `git describe`, under field or key names distinct from the existing `commit-sha` field (`frontmatter-schema.md:49`) and `tags` field (`frontmatter-schema.md:50`). [S1, S3]

**AC-4:** The `decisions-count` value in a written log's frontmatter equals a manual count of that same log's own Decisions Made section entries; it is never a value the model supplies from estimation or recall. [S1]

**AC-5 (Given/When/Then):** Given a session with an available tool-call or transcript record, when the script runs, then it surfaces verification-relevant facts into the Verification content. Given no such record is available, including when only a `SessionEnd`-triggered capture-lite record exists for a prior, already-closed session, when the script runs, then the Verification section is left for the agent to author, and nothing in the log is presented as derived that was not actually derived. [S1, S6]

**AC-6:** No content in the Summary, Decisions Made, Waiting on You, or Continuation Prompt sections of a written log originates from the script; all four remain fully agent-authored text. [S1]

**AC-7:** The script resolves its own file location relative to the skill's own installed directory rather than the project being wrapped, matching the resolution rule already shipped for `organize-logs.py` at `SKILL.md:91`. Any argument identifying the git repository to inspect is relative to the project being wrapped, not the plugin install location. [S2, S4]

**AC-8:** The script performs no filesystem writes, supports a `--json` output mode, and ships with a stdlib-only sibling `test-derive-log-facts.py` that exercises it against fixture git repositories with no external test framework, matching the `organize-logs.py` / `test-organize-logs.py` pair. [S4, S5]

**AC-9:** `SKILL.md`'s Evidence Gathering section and its "### Frontmatter" block instruct the agent to run `derive-log-facts.py` and use its output, rather than leaving the script unreferenced by the skill's own procedure. [S2, S6]

## Behavior / Examples

### Example 1: Pre-prose invocation

Before drafting any prose, the wrapping agent runs the script against the project being wrapped:

```
python <skill-dir>/scripts/derive-log-facts.py --base origin/main --json
```

```json
{
  "machine": "dev-laptop",
  "repo": "prisant-labs/prisant-utilities",
  "branch": "main",
  "date": "2026-08-23T14:12:00-07:00",
  "files-changed": [
    "skills/plab-wrap-session/SKILL.md",
    "skills/plab-wrap-session/scripts/derive-log-facts.py"
  ],
  "commit-range": "a1b2c3d..e4f5g6h",
  "latest-tag": "v0.6.0"
}
```

The agent pastes these values into the frontmatter and the Files Changed section rather than reconstructing them from memory or re-running the underlying git commands one at a time.

### Example 2: decisions-count, computed after the prose exists

The script's frontmatter-and-files-changed output happens before the model drafts prose (see Open Questions / Decisions, item D2, for why). Once the agent has drafted the Decisions Made section, `decisions-count` is filled by a mechanical count of that section's entries rather than by the model's own running tally. A log with three bulleted decisions gets `decisions-count: 3` because three bullets exist under `## Decisions Made`, not because the agent remembers making three decisions.

### Example 3: Verification section with no available record

A session run in a harness that exposes no transcript or tool-call record, and with no capture-lite record relevant to it (capture-lite describes prior closed sessions only, never the current one), produces a Verification section identical in authorship to today's: the agent writes it from context, and the log does not claim any part of it was derived.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token cost | One script invocation whose output is pasted into context replaces several manual git tool-calls plus the model's own transcription of their results, on every wrap. | [S1] |
| Correctness under session length | Derived-field accuracy must not degrade as a session gets longer, unlike model-recalled facts drawn from early-session context. | [S1] |
| Portability | stdlib-only Python, no third-party dependencies, matching the existing script in this skill. | [S4] |
| Consistency | Git commands the script needs that the hygiene sweep already documents (for example, tag lookups) are reused from `hygiene-sweep.md` rather than re-invented a second way. | [S7] |
| Safety | Read-only: no filesystem writes, so every invocation is safe to re-run and never needs a dry-run flag. | [S4] |

## Revisions

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial draft created | agent |

## Sources & Evidence

- [S1] the maintainer's private plab-wrap-session evolution roadmap, 2026-08-16, section "W-2. Split the log into a derived layer and an authored layer." Maintainer-local, gitignored, exists on disk. Credibility A (primary design source for this effort; the full section, including the fact/judgment table, was read before writing this spec).
- [S2] `skills/plab-wrap-session/SKILL.md` (current, v1.5.0). Repo file, credibility A, read in full.
- [S3] `skills/plab-wrap-session/references/frontmatter-schema.md`. Repo file, credibility A, read in full.
- [S4] `skills/plab-wrap-session/scripts/organize-logs.py`. Repo file, credibility A, read in full.
- [S5] `skills/plab-wrap-session/scripts/test-organize-logs.py`. Repo file, credibility A, read in full.
- [S6] the maintainer's private defect record for the wrap/continue pair, 2026-08-18, section "D-4. Capture-lite is a producer with zero consumers." Maintainer-local, gitignored, exists on disk. Credibility A.
- [S7] `skills/plab-wrap-session/references/hygiene-sweep.md`. Repo file, credibility A, read in full.

### Unverified Claims

None.

## Open Questions / Decisions

| ID | Item | Status |
|---|---|---|
| D1 | Exact field/key names for commit-range and git-describe-tag data | Open, left to implementation |
| D2 | Whether `decisions-count` needs a second script invocation after the Decisions Made section is drafted | Decided, see below |
| D3 | Whether capture-lite (W-1 / D-4) grounds the current session's Verification table | Decided, see below |

**D1.** The roadmap names "commit range and tags" as one derivable row but does not name field keys. `frontmatter-schema.md` already has Tier 3 fields `commit-sha` (single SHA) and `tags` (topic keywords) that a careless implementation could collide with. Left open for implementation time; AC-3 constrains the answer (must not collide) without dictating the exact name.

**D2.** The roadmap's implementation shape describes the script as emitting "a frontmatter block and a files-changed section... which the skill then wraps prose around," which reads as the script running before the model drafts prose. But `decisions-count` depends on the Decisions Made section's content, which does not exist yet at that point. This spec resolves the ordering by treating `decisions-count` as computed after that section is drafted (AC-4), which may mean a second, smaller invocation of the script, or a single generation pass in which the model still authors the whole document but defers the exact count to a mechanical recount rather than free recall. The precise mechanism is left to the implementation plan; the fixed outcome is a mechanical count, never an estimate.

**D3.** D-4 already established that a `SessionEnd`-triggered capture-lite record for the *current* session does not exist at wrap time, so it cannot ground this session's Verification table. AC-5 reflects this directly: verification derivation depends on a tool-call or transcript record if the harness exposes one, not on capture-lite, which is the record W-1 defines for prior sessions. Where no such record exists, the section stays model-authored, same as today. This spec treats the source roadmap's table row ("Verification table... tool-call record, or capture-lite from W-1") as needing this caveat rather than taking it literally, since a literal reading would contradict D-4's own, already-settled finding.
