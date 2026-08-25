---
id: D-12
title: "Implementation plan: Narrow the path-existence gate to real path citations"
type: implementation-plan
status: complete
created: 2026-08-23
updated: 2026-08-24
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_v0.4.0/plan_v0.4.0.md
ac-coverage: complete
phase-count: 2
---

# Implementation Plan: Narrow the path-existence gate to real path citations

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Rewrite the wrap skill's path-existence Log Self-Check gate so it only evaluates citations
that actually assert a location, eliminating the six-false-positive-per-wrap pattern while still
catching genuine missing-file references.

**Architecture:** A single prose edit to one bullet in `skills/plab-wrap-session/SKILL.md`'s Log
Self-Check section, plus the matching documentation trail (HISTORY.md, CHANGELOG.md). No new script.
This effort stays at mechanization-ladder rung 3 (documented convention); turning the detector into a
committed, canary-verified script belongs to D-11 (three-state gate canaries), done on top of this
effort's narrowed rule.

**Spec:** `spec.md`

**Target versions:** `plab-wrap-session` 1.6.0. This effort contributes content only; the
`metadata.version` frontmatter bump and the plugin/manifest version bumps are release-level actions
tracked in `docs/internal/release-plans/plan_v0.4.0/plan_v0.4.0.md`'s Doc-Update Checklist, shared
across every v0.4.0 effort that touches wrap. Do not bump `metadata.version` in this plan's phases.

**Global constraints:**

- No em-dash (U+2014) or en-dash (U+2013) characters anywhere, including inside example citation text
  or code comments. Use " - " or restructure. Applies to every file this plan touches.
- State the scoping rule once, in the SKILL.md gate line. Do not restate it in a reference file.
- This plugin is built for one user, its maintainer. No configuration surface, no third-party
  onboarding.
- **Sequencing:** this plan must land, and be merged to `main`, before D-11 (three-state gate canaries)
  (`docs/internal/release-plans/plan_v0.4.0/D-11_three-state-gate-canaries/`) begins its own Phase 1. D-11
  wraps this effort's rule in canary verification and needs the rule already narrowed before authoring
  its canary corpus. See spec Requirement 5.
- Do not edit the em-dash/en-dash gate bullet (currently `SKILL.md:195`) or any of the other four Log
  Self-Check bullets. That is out of scope here and belongs to D-11.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Rewrite the path-existence gate bullet | AC-1, AC-2, AC-3, AC-4, AC-5 | agent | Done |
| P2 | Documentation and version-trail content | N/A (documentation) | agent | Done |

---

## Phase 1: Rewrite the path-existence gate bullet

**Goal:** Replace the current gate bullet with one that states the narrowed scoping rule as an explicit
test.

**Files:** Modify `skills/plab-wrap-session/SKILL.md`

**Fulfills:** AC-1, AC-2, AC-3, AC-4, AC-5

**Steps:**

- [x] Step 1: Open `skills/plab-wrap-session/SKILL.md` and confirm the current text at the Log
  Self-Check section (`## Log Self-Check (before writing)`, currently starting at line 186). The
  target bullet currently reads "Every file path and link named in the log exists" (currently line
  194, the fifth of six bullets, immediately above the em-dash/en-dash bullet). Re-verify the line
  number before editing, since a prior phase in this same release may have already shifted lines above
  it.
- [x] Step 2: Replace that one bullet with:
  `Every citation with a path separator, or backtick-wrapped and resolving against the repo root,
  exists as a file (a bare word with a file extension and neither signal is not a path claim and is
  not checked)`
  Minor rewording is acceptable if the executing agent finds a clearer phrasing, provided all three
  branches of the rule survive: (a) separator present -> checked, flagged if missing; (b)
  backtick-wrapped, no separator -> resolved against repo root, non-resolution is not a finding; (c)
  neither signal -> not evaluated.
- [x] Step 3: Leave every other line in the Log Self-Check section, and the rest of the file, untouched.
  Do not touch the em-dash/en-dash bullet immediately below.
- [x] Step 4: Re-read the six-bullet list top to bottom and confirm it still reads as six single-line
  bullets (the new one may wrap in the editor but should remain one logical bullet, consistent with the
  style of its neighbors).

**Verification:**

- `git diff skills/plab-wrap-session/SKILL.md` shows exactly one bullet line changed, no other lines
  touched.
- Manually apply the new rule to three real citations from
  `_local/_session-logs/2026-08-23_10-27_claude_doc-version-parity-and-guide-222.md` (maintainer-local;
  read it directly to check) and confirm the outcome matches the spec's Behavior/Examples:
  - Line 52, `scripts/em-dash-sweep.sh` (path separator present): in scope, and does not exist at
    `skills/plab-guide/scripts/em-dash-sweep.sh` (confirm with a filesystem check), so it is flagged.
  - Line 119, `` `test-organize-logs.py` `` (backtick-wrapped, no separator): resolving
    `test-organize-logs.py` against the repo root finds nothing, so per branch (b) this produces no
    finding.
  - Line 97, `` `README.md` `` (backtick-wrapped, no separator): resolving `README.md` against the
    repo root succeeds, so it is in scope and passes silently.

---

## Phase 2: Documentation and version-trail content

**Goal:** Record the fix in the human-facing history so a reader three months from now knows what
changed and why.

**Files:** Modify `CHANGELOG.md`, `skills/plab-wrap-session/HISTORY.md`

**Fulfills:** N/A (documentation; all behavioral AC are fulfilled by Phase 1)

**Steps:**

- [x] Step 1: Add a bullet under `CHANGELOG.md`'s `## [Unreleased]` section, in a `### Fixed`
  subsection (create the subsection if the current `[Unreleased]` block does not already have one).
  Content: state that the path-existence Log Self-Check gate previously flagged bare filenames
  mentioned in prose as missing paths (6 of 7 flags were false positives in one observed wrap), and
  that it now only checks citations carrying a path separator or a backtick-wrapped, repo-root
  resolving reference.
- [x] Step 2: Check `skills/plab-wrap-session/HISTORY.md` for an existing `## 1.6.0` heading and
  version-table row. If a co-landing v0.4.0 effort has already added one, append this effort's content
  as an additional bulleted paragraph under the existing heading, without editing or removing any
  other effort's bullets. If no `1.6.0` heading exists yet, add both the version-table row (`| 1.6.0 |
  <date> | v0.4.0 | fixed | <short summary, to be extended by later v0.4.0 efforts> |`) and the
  section heading with this effort's bullet.
- [x] Step 3: Follow the existing HISTORY.md style (bold lead sentence, then supporting detail), as
  seen in the 1.5.0 and 1.4.1 entries already in the file.

**Verification:** Both files remain valid Markdown (visual check); `skills/plab-wrap-session/HISTORY.md`
has exactly one `## 1.6.0` heading and exactly one matching version-table row regardless of how many
v0.4.0 efforts have appended bullets beneath it.

---

## CI and Documentation Coverage

### CI

No CI change. This effort stays at mechanization-ladder rung 3 (documented convention): the scoping
rule lives as explicit prose in the SKILL.md gate line, applied by the wrapping agent at check time.
It deliberately does not become a committed script here; that lift, and its accompanying canary corpus,
is D-11 (three-state gate canaries), which generalizes both detector-backed gates in one pass.
Scripting this rule one effort early would duplicate work D-11 already plans and risks the two efforts
producing conflicting SKILL.md gate-bullet edits.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: the one gate-bullet rewrite (Phase 1). This is the only
  agent-facing file this effort touches.
- `skills/plab-wrap-session/references/frontmatter-schema.md`: no change. Its existing "cite session
  logs by filename only" convention (lines 98-107) was checked against the new rule and is already
  compatible: filename-only citations carry no path separator, so they were already out of scope.

### Human-facing documentation

- `CHANGELOG.md`: new `[Unreleased] > Fixed` bullet (Phase 2, Step 1).
- `skills/plab-wrap-session/HISTORY.md`: new bullet under the shared `## 1.6.0` heading (Phase 2, Steps
  2-3), co-owned with the other v0.4.0 efforts that touch wrap.
- `docs/skills/plab-wrap-session/README.md`: no change. Confirmed by direct read that this file does
  not currently describe the Log Self-Check gates at all (no mention of "self-check," "gate," "em-dash,"
  or "path exist" anywhere in it), so nothing here goes stale and there is nothing to keep accurate.
- Root `README.md`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `library.json`,
  `manifest.generated.json`, `docs/skills/plab-wrap-session/README.md`'s version line, and the
  `SKILL.md` `metadata.version` field: **not touched by this effort's phases.** These are release-level
  actions, already tracked as unchecked rows in
  `docs/internal/release-plans/plan_v0.4.0/plan_v0.4.0.md`'s Doc-Update Checklist, shared across every
  v0.4.0 effort that bumps wrap to 1.6.0. Bumping them once per effort would produce competing edits to
  the same lines across up to six efforts; the release plan's checklist bumps them once, at tag time.

---

## Rollback

Revert the SKILL.md bullet to its pre-D-12 wording (a one-line change) and remove the HISTORY.md and
CHANGELOG.md bullets this effort added. No script, no schema, and no data migration exist to unwind, so
this is a plain text revert. The one dependency to check first: if D-11 (three-state gate canaries) has
already landed on top of this effort, its path-citation canary corpus assumes this narrowed rule (see
D-11's spec Requirements). Reverting D-12 without also reverting or updating D-11's canaries would leave
D-11's self-test asserting behavior the gate no longer has, which is exactly the broken-canary failure
mode D-11 exists to prevent. Roll back D-11 first, or update its canary corpus in the same revert.
