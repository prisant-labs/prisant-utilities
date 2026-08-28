---
id: D-06
title: "Fix resumed-from semantics: written only by an in-session resume, never back-filled"
type: spec
status: fulfilled
created: 2026-08-23
updated: 2026-08-24
linked-effort: the maintainer's private defect record for the wrap/continue pair, 2026-08-18
linked-plan: implementation-plan.md
ac-count: 4
source-count: 4
requires-human-review: false
target-release: v0.4.0
linked-release: docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md
priority: P3
---

# Spec: Fix resumed-from semantics: written only by an in-session resume, never back-filled

## Task Summary

Status: Fulfilled
Last updated: 2026-08-24
Linked plan: implementation-plan.md
Open questions: 1 (see Open Questions / Decisions)
Revisions: 1 (see Revisions)

### Acceptance Criteria Fulfillment

- [x] AC-1: `frontmatter-schema.md` states the four-part semantics
- [x] AC-2: `SKILL.md`'s frontmatter comment matches or cross-references the semantics
- [x] AC-3: Neither file describes `resumed-from` as suitable for cross-repo pointers
- [x] AC-4: No shipped file justifies writing the field from memory rather than an in-session resume

### Currently In Progress

None.

## Purpose

D-06 (resumed-from semantics) fixes what the `resumed-from:` frontmatter field means: written only
when `/plab-continue-session` performed the resume in the current session, never back-filled from
narrative memory, omitted otherwise, with cross-repo lineage left to Summary prose. Both real session
logs in this repository currently carry a `resumed-from:` value pointing at a filename that lives in a
different repo (jp-library) and cannot be resolved, because the field was back-filled from memory
rather than written by an actual resume. D-06 is the roadmap's D-6.

## Scope

### In Scope

- A four-part semantics statement added to `references/frontmatter-schema.md` for the `resumed-from`
  field.
- A matching update to the inline YAML comment for `resumed-from:` in
  `skills/plab-wrap-session/SKILL.md`'s frontmatter block.
- Version bump and a `HISTORY.md` entry for `plab-wrap-session` only.

### Non-Goals

- No repo qualifier added to the field. Rescoped in the source: continue-session already refuses
  cross-repo resumption (`skills/plab-continue-session/SKILL.md:108`), so a skill-mediated resume is
  same-repo by construction and a bare filename is always resolvable.
- No global index of resumed-from relationships across repos.
- No change to any file under `skills/plab-continue-session/`. Its Phase 5 language already states
  same-session semantics ("Note the consumed log's filename: when this session is eventually
  wrapped...") and needs no edit (see Requirement 3). Continue's own 1.4.0 version bump this release is
  carried by D-04 (capture-lite consumers) and D-05 (superseding logs), which do touch its files; D-06
  contributes nothing to it and does not bump it.
- No hand-fix of the two existing local logs' unresolvable `resumed-from:` values. The source names
  this optional; it is not required by this effort's acceptance criteria (see Open Questions, OQ1).
- No further investment beyond this fix. The source explicitly assesses this metric as cheap to keep
  and not worth more effort than the two sentences this effort spends.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Wrapping agent | Writes `resumed-from:` only when it has direct knowledge a resume happened this session | Reads the updated schema and comment before drafting frontmatter |
| Maintainer (JP) | Reads the field when reviewing a log, or when counting log consumption | Trusts the field means "consumed via the skill this session," not "the arc's ultimate origin" |

## Requirements

1. `references/frontmatter-schema.md`'s Tier 2 entry for `resumed-from` states four things: it is
   written only when `/plab-continue-session` performed the resume in the current session; it is
   never back-filled from narrative memory; it is omitted when no resume occurred this session; and
   cross-repo lineage, when relevant, belongs in the Summary section's prose, not in this field.
   [S1, S3]
2. `skills/plab-wrap-session/SKILL.md`'s frontmatter block inline comment for `resumed-from:` is
   updated to match, or to explicitly cross-reference, the same semantics, so the two files do not
   restate the rule in different words. [S1, S4]
3. No file under `skills/plab-continue-session/` needs to change. Its Phase 5 text already reads "Note
   the consumed log's filename: when this session is eventually wrapped, `/plab-wrap-session` (1.4.0+)
   records it in the new log's `resumed-from:` frontmatter," which is already same-session language,
   not a promise of cross-session back-filling. [S2, model-inference: this is this spec's own
   verification finding against the source file, not a claim stated in pair-defects.md itself]
4. The two existing local session logs' `resumed-from:` values are left unedited by this effort's
   required scope; the source names hand-fixing them as optional, and doing so has no effect on either
   skill's behavior since both files are gitignored working notes. [S1]

## Acceptance Criteria

**AC-1:** `references/frontmatter-schema.md`'s Tier 2 table, or an adjoining note immediately below
it, states all four of: written only via an in-session `/plab-continue-session` resume, never
back-filled, omitted when no resume occurred, and that cross-repo lineage belongs in Summary prose.
[S1, S3]

**AC-2:** `skills/plab-wrap-session/SKILL.md`'s frontmatter block inline comment for `resumed-from:`
states that the field is populated only by an in-session resume via `/plab-continue-session`, or
explicitly cross-references `references/frontmatter-schema.md` for the full rule, in place of the
current unqualified "filename of the session log this session resumed from, if any - measures log
consumption". [S1, S4]

**AC-3:** Neither `references/frontmatter-schema.md` nor `skills/plab-wrap-session/SKILL.md` describes
`resumed-from` as suitable for pointing at a log in a different repository; both remain consistent
with continue's existing same-repo-only resumption behavior. [S1, S2]

**AC-4:** After this change, no shipped skill file, SKILL.md or references, in either skill, contains
language that would justify writing `resumed-from` from memory of a resume that happened in a prior
session, rather than from an in-session `/plab-continue-session` invocation. [S1]

## Behavior / Examples

Given a session in which the agent invoked `/plab-continue-session` and it performed a resume from
`2026-08-20_09-00_claude_prior-work.md`, when that same session is later wrapped, then the new log's
frontmatter carries `resumed-from: 2026-08-20_09-00_claude_prior-work.md`.

Given a session in which no resume occurred (the agent started fresh, or the user chose "pick
something else" at continue's Phase 4 rather than the named continuation), when that session is
wrapped, then `resumed-from:` is omitted from the frontmatter entirely, never written with an empty or
guessed value.

Given a session in which the agent recalls, from conversation context or narrative memory, that some
earlier session resumed from a particular file, but `/plab-continue-session` did not run this session,
when that session is wrapped, then `resumed-from:` is still omitted; that recollection, if worth
recording at all, belongs in Summary prose, not in this field. This is precisely the failure mode both
real logs in this repository exhibit today: a value pointing at a jp-library filename that this repo's
`_local/_session-logs/` never contained. [S1]

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token cost | No description growth on either skill; the fix is a reference-file paragraph and a comment edit | [S1] |
| Investment ceiling | This effort is intentionally minimal; the source explicitly recommends no further investment in this metric beyond this fix | [S1] |

## Revisions

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial draft created | agent |

## Sources & Evidence

- [S1] the maintainer's private defect record for the wrap/continue pair, 2026-08-18, D-6 section and the "Rejected and
  rescoped" table. Maintainer-local, class A (primary design source).
- [S2] `skills/plab-continue-session/SKILL.md`, Phase 5 (lines 95-99) and the Constraints list
  (cross-repo refusal at line 108, corrected from the source's approximate "around line 105", which
  predates several lines of accumulated edits). In-repo, class A, verified by direct read.
- [S3] `skills/plab-wrap-session/references/frontmatter-schema.md`, the Tier 2 table row for
  `resumed-from` (line 33). In-repo, class A, verified by direct read.
- [S4] `skills/plab-wrap-session/SKILL.md`, the frontmatter block's `resumed-from:` inline comment
  (line 128). In-repo, class A, verified by direct read.

### Unverified Claims

None. All four acceptance criteria cite verified in-repo anchors or the primary source document; none
depends on this spec's own inference beyond Requirement 3's verification finding, which is a factual
read of an existing file, not a design choice.

## Open Questions / Decisions

| ID | Title | Status |
|---|---|---|
| OQ1 | Hand-fix the two existing local logs' unresolvable value | Open |

### OQ1: Hand-fix the two existing local logs' unresolvable value

Both real session logs on disk today carry `resumed-from:` values pointing at a jp-library filename
this repo cannot resolve. The source marks correcting them as optional, and this effort's acceptance
criteria do not require it, since the two files are gitignored working notes with no effect on either
skill's shipped behavior. Recommend leaving this as a manual maintainer action, taken or not at the
maintainer's discretion, rather than a step in the implementation plan.
