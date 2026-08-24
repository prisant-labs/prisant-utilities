---
id: C-05
title: "Arc resume: read the last N logs, not just the newest"
type: spec
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-effort: _local/skill-roadmaps/2026-08-16/continue-session.md
linked-plan: implementation-plan.md
ac-count: 7
source-count: 7
requires-human-review: false
target-release: v0.6.0
linked-release: docs/internal/release-plans/plan_v0.6.0/plan_v0.6.0.md
priority: P2
---

# Spec: Arc resume: read the last N logs, not just the newest

## Task Summary

Status: Draft
Last updated: 2026-08-23
Linked plan: implementation-plan.md
Open questions: 3, see Open Questions / Decisions
Revisions: 1, see Revisions

### Acceptance Criteria Fulfillment

- [ ] AC-1: default behavior unchanged without `--arc`
- [ ] AC-2: `--arc` delegates window reading to the shared script
- [ ] AC-3: narrative collapse extends, and does not paraphrase, the existing display
- [ ] AC-4: coverage statement matches the shared contract
- [ ] AC-5: pre-read cost statement before spending tokens
- [ ] AC-6: no same-arc dedup logic
- [ ] AC-7: no independent multi-log logic anywhere in this skill

### Currently In Progress

None.

## Purpose

C-05 is the roadmap's C-5, promoted out of speculative status on 2026-08-17 because transcripts asked for it in the maintainer's own words, not as a hypothetical [S1]. `plab-continue-session` today reads exactly one log, the newest; after a long gap that log is the end of a story the reader no longer remembers the middle of. This effort adds an explicit `--arc [N]` flag that reads the last N logs and resumes from a narrative of the whole window instead of a single entry. This spec is the read-side twin of W-04 (the roadmap's W-4, digest mode) and depends on it directly: it declares no aggregation logic of its own and instead consumes the shared script and contract W-04 ships, `skills/plab-wrap-session/scripts/aggregate-logs.py` and `skills/plab-wrap-session/references/log-aggregation.md`, per the roadmaps' own instruction that the two "should share whatever aggregation is built rather than each growing their own" [S1]. Do not implement this spec ahead of W-04; the script it calls does not exist until W-04 ships.

## Scope

### In Scope

- An explicit `--arc [N]` flag on `plab-continue-session` that reads the last N logs (default per the shared script) instead of the single newest log.
- A narrative collapse of the window plus the open threads that survived across all of it, added to the existing resumption display.
- A pre-read statement of how many logs are about to be read, so the user can decline the cost before it is spent.

### Non-Goals

- **Not a default.** Arc mode runs only when `--arc` is passed explicitly. The roadmap's own promotion note names the token-cost tradeoff as the reason to prototype this as a flag before ever considering a default [S1].
- **Not a second aggregation implementation.** This is the central design constraint stated in both source roadmaps: no independent multi-log discovery or section-extraction logic is written inside `plab-continue-session`. Everything of that kind is `skills/plab-wrap-session/scripts/aggregate-logs.py`'s job (see AC-2 and AC-7).
- **Not a replacement for the single-log flow.** Phases 1 through 5 of `plab-continue-session` are unchanged when `--arc` is absent (AC-1). Existing hard constraints, never paraphrase the Continuation Prompt, refuse cross-repo resumption, surface branch mismatches, are unchanged and unrelaxed by this effort.
- **Not cold-repo re-orientation.** C-03 (the roadmap's C-3, cold-repo degradation, a separate effort scheduled at v0.4.0, before this one) handles the case of no recent log or no log at all. C-05 assumes multiple logs exist; it does not build a fallback for when they do not.
- **Not an automatic age-based trigger.** Whether `--arc` should someday suggest itself when the newest log is old is explicitly deferred (see Open Questions), not built here.
- **Not a same-arc deduplication mechanism.** Exactly as W-04, this effort relies on D-05 (superseding logs) having already removed same-arc duplicate logs from the corpus at write time [S6].

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer (JP) | Invokes arc mode after a gap, reads the narrative and open threads, decides whether to resume | Runs `/plab-continue-session --arc [N]`; sees the pre-read cost statement first; reads the narrative, the open threads, and the verbatim newest Continuation Prompt; answers the existing Phase 4 confirmation question |
| Agent (Claude Code or Codex session running the skill) | Executes arc mode | Calls `skills/plab-wrap-session/scripts/aggregate-logs.py` for the window and rollup, narrates the shipped and outstanding content into the display, never synthesizes or paraphrases the newest log's Continuation Prompt |

## Requirements

1. `--arc [N]` is an explicit flag, never a default. Without it, `/plab-continue-session` behaves exactly as it does today: single newest log, unchanged Phases 1 through 5 [S1].
2. Window reading is entirely delegated to `skills/plab-wrap-session/scripts/aggregate-logs.py`, the script W-04 ships. `plab-continue-session` writes no independent logic to pool stores, sort by filename, or extract per-log sections; those rules live once in `skills/plab-wrap-session/references/log-aggregation.md`, which this skill points at rather than restates [S1]/[S2].
3. The resumption display gains a narrative section (what happened across the window) and an open-threads section (what survived across all of it, reusing the shared aggregation's outstanding rollup), inserted into the existing Phase 3 display shape defined in `handoff-display.md` rather than replacing it [S5].
4. The newest log's Continuation Prompt still appears verbatim, unedited, in its own fenced block exactly as it does in the single-log flow today. The narrative and open-threads sections are additional context placed around it, not a substitute for it or a paraphrase of it [S3]/[S5].
5. Arc mode's coverage statement, which harnesses and which stores were read, uses the identical contract W-04's digest uses, so the same rollup read by both modes is described the same way in both places [S1].
6. Before spending the tokens to read and narrate the window, arc mode states how many logs it is about to read (for example, "reading the last 8 logs, spanning 2026-06-02 to 2026-08-23") so the maintainer can decline. This is the roadmap's own stated caution: the cost lands exactly when the user is least willing to spend it [S1].
7. Arc mode performs no logic to detect or collapse same-arc duplicate logs. Like W-04, it relies on D-05 having already removed same-arc duplicates from the corpus at write time [S6]/[S7].
8. Arc mode uses `skills/plab-wrap-session/scripts/aggregate-logs.py`'s own default log count when N is omitted; this spec does not declare a second, separate default. The number itself is W-04's to own and is not restated here (see W-04 spec, AC-8).

## Acceptance Criteria

AC-1: `/plab-continue-session` invoked without `--arc` behaves identically to the current single-newest-log flow; arc mode never runs implicitly. [S1]

AC-2: `/plab-continue-session --arc [N]` reads the last N logs by calling `skills/plab-wrap-session/scripts/aggregate-logs.py`, the script W-04 (the roadmap's W-4) ships, rather than `plab-continue-session` running its own multi-log discovery. [S1]/[S2]

AC-3: Arc mode's resumption display adds a narrative collapse of what happened across the window, plus the open threads that survived across all of it, as an extension of the existing Phase 3 handoff-display format; it does not replace or paraphrase the newest log's verbatim Continuation Prompt, which still appears exactly as it does today. [S1]/[S5]

AC-4: Arc mode's display states which harnesses and stores its narrative and open-thread list were read from, using the same coverage-statement contract W-04's digest uses. [S1]

AC-5: Before reading the window, arc mode states how many logs it is about to read, so the user can decline before the token cost is spent. [S1]

AC-6: Arc mode contains no logic to detect or collapse same-arc duplicate logs; like digest mode, it relies on D-05 having already removed same-arc duplicates from the corpus at write time. [S6]/[S7]

AC-7: Arc mode contains no independently implemented multi-log discovery or per-log section-extraction logic anywhere in `plab-continue-session`; that logic is entirely delegated to `skills/plab-wrap-session/scripts/aggregate-logs.py`. [S1]/[S2]

## Behavior / Examples

**Example 1: default flow, unchanged.**

```
/plab-continue-session
```

behaves exactly as documented today: single newest log, standard Phase 1 through 5 flow, no window reading, no narrative section. AC-1 exists precisely so this example needs no further elaboration.

**Example 2: arc resume after a gap.**

```
/plab-continue-session --arc
```

first prints the pre-read cost statement (AC-5), for example:

```
About to read the last 10 logs, spanning 2026-06-02 to 2026-08-23. Proceed? (y/n)
```

On confirmation, it calls `skills/plab-wrap-session/scripts/aggregate-logs.py` and presents a resumption display that extends the existing shape:

```
## Resuming from the last 10 logs (2026-06-02 through 2026-08-23)

Coverage: 10 logs read from _local/_session-logs/ (9 claude-code, 1 codex-cli).

### What happened across this arc
The migration to prisant-utilities completed, --organize and month-folder
archiving shipped, and the wrap/continue pairing gained a hygiene sweep.
...

### Waiting on you
- The source-of-truth ruling (blocked since 2026-07-xx, present in 6 of 10 logs)

### Continuation prompt (from 2026-08-23_10-27, the newest log)
[fenced, verbatim, unedited]
```

The final section is the same verbatim-prompt guarantee the single-log flow already makes; arc mode adds context above it, it does not touch it.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token economy | `--arc` is opt-in, per-invocation cost, gated by AC-5's pre-read statement; it adds zero always-on cost since it is never a default | [S1] |
| Reuse | No independent multi-log logic exists in this skill; window reading and extraction are entirely delegated | [S1]/[S2] |
| Determinism | Window selection and section extraction are script work; only the narrative prose is model-authored | [S2] |
| Consistency | The coverage statement's wording matches W-04's digest exactly, since both read the same underlying rollup shape | [S1] |

## Revisions

| Date | Change | Author |
|---|---|---|
| 2026-08-23 | Initial draft created | Claude (agent) |

## Sources & Evidence

- [S1] `_local/skill-roadmaps/2026-08-16/continue-session.md` (maintainer-local, gitignored; exists on disk). Section C-05 (the roadmap's own heading reads "C-5", lines 98-106, including the promotion note and the "share whatever aggregation is built" instruction on line 104), "What not to do" (lines 110-114). Credibility: A, first-party maintainer-authored roadmap.
- [S2] `docs/internal/release-plans/plan_v0.6.0/W-04_digest-mode/spec.md`, this session's sibling artifact and the owner of the shared aggregation layer this spec depends on. Cited by section (Requirements item 8, AC-2, AC-7, AC-8) rather than by line number, since both documents were drafted in the same session. Credibility: A, first-party.
- [S3] `skills/plab-continue-session/SKILL.md`. The current single-log Phase 1 through 5 flow (lines 34-99) and the never-paraphrase constraint (line 105) this effort must not relax. Credibility: A, verified current shipped file.
- [S4] `skills/plab-continue-session/references/log-discovery.md` (lines 15-44). The corpus contract reused, not redefined, by the shared script. Credibility: A, verified current shipped file.
- [S5] `skills/plab-continue-session/references/handoff-display.md` (lines 7-28 for the required structure, line 39 for "Never paraphrase"). The Phase 3 display format this effort extends. Credibility: A, verified current shipped file.
- [S6] `_local/skill-roadmaps/2026-08-18/pair-defects.md` (maintainer-local, gitignored; exists on disk). D-05, same-arc superseding logs (the roadmap's own heading reads "D-5"), specifically the line stating the dedup hazard "for W-4 and C-5 is removed at write time instead of demanding dedup logic at read time forever" (lines 101-111, quoted line is 109; "W-4" and "C-5" in that quoted line are the source's own unpadded form for W-04 and C-05). Credibility: A, first-party maintainer-authored addendum, verified.
- [S7] `docs/internal/release-plans/plan_v0.3.0/D-05_superseding-logs/spec.md`. D-05's own spec now exists in this repository (written independently of this document, targeting the earlier v0.3.0 release) and confirms, with its own AC-3 and AC-6, the mechanism [S6] describes from the proposal-stage `pair-defects.md`: the `_superseded/` archive path and its exclusion from `log-discovery.md`'s allowlist. Credibility: A, first-party, this release's own sibling planning artifact, verified by direct reading.

### Unverified Claims

None. Every AC in this spec cites a verified source; no AC in this spec carries `[model-inference]`.

## Open Questions / Decisions

| ID | Question | Status |
|---|---|---|
| D1 | The task brief that produced this spec asked for `spec-dependencies: [W-04]` in frontmatter; the conventions' spec.md schema is closed and does not define that field. How is the dependency declared? | Resolved for this draft |
| D2 | Should `--arc` ever auto-suggest itself based on the newest log's age? | Deferred |
| D3 | Does arc mode need its own default N, distinct from the shared script's default? | Resolved for this draft |

**D1.** The conventions governing this document set state plainly that its frontmatter schema is closed and that inventing a field is a named hard constraint, already responsible for prior defects in this repository. Rather than add an undefined `spec-dependencies` field, this spec declares the W-04 dependency in the body: in Purpose (first paragraph), in Scope's Non-Goals ("not a second aggregation implementation"), in Requirements (item 2 and item 8), in three of the seven AC (AC-2, AC-7, and by extension AC-4), and as [S2] in Sources & Evidence, which points directly at `W-04_digest-mode/spec.md`. A reader or a future gate script gets the same dependency information from the body that a `spec-dependencies` field would have given from frontmatter, without violating the closed-schema rule. If a future revision of the conventions adds `spec-dependencies` to the closed schema, this frontmatter block should be updated to add it explicitly rather than inferring it should already be there.

**D2.** C-03 (cold-repo degradation) already handles the no-recent-log case at a different point on the same spectrum. Whether the boundary between "C-03 should fire" and "arc mode should suggest itself" is worth automating is a real question, but building it now would couple two efforts that the version ladder deliberately sequences a full release apart (C-03 at v0.4.0, this effort at v0.6.0). Held until both have shipped and real usage shows whether the gap between them is actually felt.

**D3.** No. Requirement 8 states this explicitly: a second default here would restate a number W-04 already owns, which is exactly the "text contradicting text" failure mode this repo's own conventions name as its dominant defect class. If the shared default ever needs to differ by caller, that is a parameter the shared script should expose, not a value either skill hard-codes.
