---
id: C-04
title: Record whether a resumed log's next action survived contact with reality
type: spec
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-effort: _local/skill-roadmaps/2026-08-16/continue-session.md
linked-plan: implementation-plan.md
ac-count: 6
source-count: 6
requires-human-review: false
target-release: v0.9.0
linked-release: docs/internal/release-plans/plan_08_escape-and-measure/plan.md
priority: P2
---

# Spec: Record whether a resumed log's next action survived contact with reality

## Task Summary

- **Status:** draft
- **Last updated:** 2026-08-23
- **Linked plan:** `implementation-plan.md`
- **Open questions:** 2 (see Open Questions / Decisions)
- **Revisions:** 1 (see Revisions)

### Acceptance Criteria Fulfillment

- [ ] AC-1: A genuine skill-mediated resume gets a `resumed-from-disposition:` value in the new log
- [ ] AC-2: No resume this session means the field is omitted, never a placeholder
- [ ] AC-3: The three values are defined exactly as fulfilled, superseded, and ignored
- [ ] AC-4: The field modifies only the new log, never the log named by `resumed-from:`
- [ ] AC-5: Only the wrap skill writes the field; continue-session writes no files
- [ ] AC-6: No aggregation, digest, or report reads the field as part of this effort

### Currently In Progress

None.

## Purpose

Consumption of a session log is already recorded: `resumed-from:` notes which log a resume consumed.
What it cannot say is whether that log's named next action survived contact with reality. C-04 (the
roadmap's C-4) closes that loop with one frontmatter field, written back by the next wrap, classifying
the prior log's next action as fulfilled, superseded, or ignored; the third value is the falsifier the
roadmap named, the only signal that would tell the maintainer to stop wrapping. It depends on D-06
(resumed-from semantics, the roadmap's D-6, shipping in v0.4.0), which fixes `resumed-from` itself to
be written only from an actual skill-mediated resume and never back-filled from narrative memory;
C-04's field inherits that exact discipline, and D-06's own honest assessment, that this metric class
is worth one line and no further investment, applies to it too.

## Scope

### In Scope

- One new Tier 2 frontmatter field, `resumed-from-disposition`, written into the log currently being
  written.
- Exactly three permitted values: `fulfilled`, `superseded`, `ignored`.
- Writing the field only when this session's `resumed-from:` was itself set via an actual
  `/plab-continue-session` resume performed this session.
- Omitting the field entirely when no such resume occurred.

### Non-Goals

- No aggregation, digest, or cross-log reporting of disposition values; the field is read by opening a
  log's frontmatter, nothing more.
- No new evidence-gathering step, script, or session-log section beyond the one field.
- Does not change `resumed-from`'s own semantics beyond what D-06 already fixes; C-04 only adds a
  sibling field.
- Does not measure the "log written but never consumed" case. A session that never invoked
  `/plab-continue-session` carries neither `resumed-from:` nor this field, and that silence is not
  something this field resolves (see Behavior / Examples, Walkthrough 3).
- Does not build W-06 (the log as a checkable contract, the roadmap's speculative item).
  `docs/internal/release-plans/plan_08_escape-and-measure/plan.md`'s D1 decision records W-06 as deliberately
  deferred and unscheduled. Neither this effort nor W-03 is W-06.
- Does not retroactively backfill disposition values for historical logs.
- Does not add a fourth "unclear" or "partial" value; see Open Questions OQ-2.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Wrapping agent | Judges and writes the disposition value, using evidence already gathered for the log | Writes `resumed-from-disposition:` into the new log's frontmatter, only when `resumed-from:` is itself present |
| Maintainer | Eventual reader of accumulated disposition values, deciding whether wrapping still pays for itself | Reads individual log frontmatter directly; no tooling is built for this in this effort |

## Requirements

1. The disposition field is written only by `/plab-wrap-session`, never by `/plab-continue-session`,
   which produces no files of its own. [S3]
2. The field is written into the frontmatter of the log currently being written, never back into the
   log named by `resumed-from:`, matching continue's existing constraint never to modify the log it
   resumed from. [S3]
3. The field is written only when this session's `resumed-from:` value was itself set via an actual
   `/plab-continue-session` resume in this session, mirroring D-06's (the roadmap's D-6, shipping in
   v0.4.0) fix to `resumed-from` itself: never inferred from narrative memory, and omitted when no
   resume occurred. [S2, S6]
4. The three permitted values are exactly `fulfilled`, `superseded`, and `ignored`, matching the
   roadmap's own definitions. [S1]
5. The disposition judgment draws only on evidence the wrap already gathers (git state, conversation
   context); no new evidence-gathering step, script, or report is added. [S2]
6. This field measures only the "consumed but ignored" half of the falsifier the roadmap named. A
   session that never invoked `/plab-continue-session` carries neither `resumed-from:` nor this field,
   and that non-consumption case remains invisible to this field by construction. [S1, S5]

## Acceptance Criteria

**AC-1:** Given this session's `resumed-from:` value was set via an actual `/plab-continue-session`
resume performed in this session, when the wrap writes the new log, then it writes
`resumed-from-disposition:` valued exactly one of `fulfilled`, `superseded`, or `ignored`. [S1, S2]

**AC-2:** Given this session did not perform a skill-mediated resume, when the wrap writes the new
log, then `resumed-from-disposition:` is omitted entirely, never written with a placeholder or empty
value. [S2]

**AC-3:** Given the wrap is classifying the outcome, when it assigns a value, then `fulfilled` means
the prior log's named next action was completed, `superseded` means circumstances changed and the plan
was correctly abandoned, and `ignored` means the session re-derived context and proceeded without
engaging the prior log's next action. [S1]

**AC-4:** Given a wrap writes `resumed-from-disposition:`, when the write happens, then it modifies
only the new log being written and never the log named by `resumed-from:`. [S3]

**AC-5:** Given a session invoked `/plab-continue-session` and later ends, when that session is
wrapped, then `resumed-from-disposition:` is written by the wrap skill; `/plab-continue-session` itself
writes no file at any point in the exchange. [S3]

**AC-6:** Given this field exists, when the repository is inspected for tooling that reads it, then
none is found: no digest, aggregation script, or report consumes `resumed-from-disposition` as part of
this effort. [S2]

## Behavior / Examples

**Walkthrough 1: fulfilled.** The prior log's Continuation Prompt named a specific immediate next
action. This session invoked `/plab-continue-session`, resumed from that log, and did exactly that.
This session's wrap writes `resumed-from: <prior log filename>` and
`resumed-from-disposition: fulfilled`.

**Walkthrough 2: ignored.** Same prior log, same resume. This session's conversation shows the
maintainer redirected to unrelated work without engaging the named action, whether by choosing "pick
something else" at Phase 4 or by drifting after starting. `resumed-from:` is still set, since a
skill-mediated resume did occur; `resumed-from-disposition: ignored`.

**Walkthrough 3: no resume, field silent.** This session never invoked `/plab-continue-session`.
Neither `resumed-from:` nor `resumed-from-disposition:` appears in this log's frontmatter. This case
is, by this field alone, indistinguishable from a log that nobody ever consumed; the roadmap's "logs
written but never consumed" half of the falsifier is visible only as the absence of `resumed-from:`
across a corpus of logs, a cross-log reading concern and not something this single field resolves by
itself.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token cost | One frontmatter field; no new section, script, or report | pair-defects.md:125 |
| Investment ceiling | No further investment beyond this field, explicitly inherited from D-06's own honest assessment of the sibling field | pair-defects.md:125 |
| Data integrity | Written only from actual skill-mediated resume state this session; never inferred or back-filled from narrative memory | pair-defects.md:119-121 |

## Revisions

| Date | Change | Author |
|---|---|---|
| 2026-08-23 | Initial draft created | agent |

## Sources & Evidence

[S1] `_local/skill-roadmaps/2026-08-16/continue-session.md` (maintainer-local, gitignored). Class A.
Section "C-4. Close the consumption loop," lines 82-95. Primary roadmap source; C-04 is the padded
form of this document's C-4.

[S2] `_local/skill-roadmaps/2026-08-18/pair-defects.md` (maintainer-local, gitignored). Class A.
Section "D-6. The `resumed-from` field is an unresolvable pointer," lines 115-126. D-06 is the padded
form of this document's D-6; its semantics fix and its cost-and-risk assessment are both inherited
whole by this effort's field.

[S3] `skills/plab-continue-session/SKILL.md`. Class A. Line 99 (Phase 5 hand-off: wrap records the
consumed log's filename), line 103 (Constraints: never modify the session log being resumed from),
line 113 (Output: this skill produces no files).

[S4] `skills/plab-wrap-session/references/frontmatter-schema.md`. Class A. Line 33, the existing Tier
2 definition of `resumed-from`, the sibling field this effort's field sits beside.

[S5] `docs/internal/release-plans/plan_08_escape-and-measure/plan.md`. Class A. Context section (C-04
paragraph), lines 35-46; Open Question D1 (W-06 deferred, resolved), lines 107 and 110-144.

[S6] `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md`. Class A. Confirms D-06 ships in v0.4.0
and names the skill versions for that release (wrap 1.6.0, continue 1.4.0), lines 27-28.

### Unverified Claims

None. Every acceptance criterion above cites a verified anchor; none carries `[model-inference]`.

## Open Questions / Decisions

| ID | Title | Status |
|---|---|---|
| OQ-1 | Field name is this spec's proposal | Open |
| OQ-2 | No escape hatch for genuinely ambiguous disposition | Open |

### OQ-1: Field name is this spec's proposal

No source document names the new field; both [S1] and [S2] describe it only as "one frontmatter
field." This spec proposes `resumed-from-disposition` to sit beside `resumed-from` in the Tier 2
table. The maintainer may prefer different naming at implementation time; changing it affects no
acceptance criterion's substance.

### OQ-2: No escape hatch for genuinely ambiguous disposition

AC-1 requires exactly one of three values whenever a genuine resume occurred this session. The
roadmap does not anticipate a session whose outcome is genuinely mixed, for example partially
fulfilled and then superseded partway through. This spec does not add a fourth value, consistent with
the "invest nothing further" constraint inherited from D-06; the wrap agent is expected to use
judgment and commit to the closest of the three.
