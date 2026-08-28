---
id: W-04
title: "Digest mode: aggregate the last N session logs"
type: spec
status: draft
created: 2026-08-23
updated: 2026-08-23
linked-effort: the maintainer's private plab-wrap-session evolution roadmap, 2026-08-16
linked-plan: implementation-plan.md
ac-count: 8
source-count: 9
requires-human-review: true
target-release: v0.8.0
linked-release: docs/internal/release-plans/plan_07_aggregation/plan.md
priority: P2
---

# Spec: Digest mode: aggregate the last N session logs

## Task Summary

Status: Draft
Last updated: 2026-08-23
Linked plan: implementation-plan.md
Open questions: 3 items (1 open, 1 deferred, 1 resolved), see Open Questions / Decisions
Revisions: 1, see Revisions

### Acceptance Criteria Fulfillment

- [ ] AC-1: `--digest` runs instead of a wrap
- [ ] AC-2: window selection reuses log-discovery.md's rules, extended to N
- [ ] AC-3: output is exactly three labeled sections
- [ ] AC-4: outstanding items distinguish persistent from fresh
- [ ] AC-5: every count states its harness and store coverage
- [ ] AC-6: no same-arc dedup logic
- [ ] AC-7: the aggregation logic is a shared, independently invocable script
- [ ] AC-8: N defaults to 10 when omitted

### Currently In Progress

None.

## Purpose

`plab-wrap-session` writes session logs but nothing reads more than one of them at a time; the corpus is write-only. W-04 is the roadmap's W-4. It adds a `--digest` mode that reads the last N logs and answers three fixed questions: what shipped, what decisions were made, and what is still outstanding across the window. The pull is concrete, not speculative: reconstructing a recent multi-week arc required hand-reading three documents across two repositories, and a per-skill usage analysis had to mine raw transcripts because no aggregate view of the logs existed [S1]. This spec also owns the shared aggregation layer that C-05 (the roadmap's C-5, arc resume) consumes rather than reimplementing, per the roadmaps' own instruction that the two "should share whatever aggregation is built rather than each growing their own" [S1].

## Scope

### In Scope

- A `--digest [N]` mode on `plab-wrap-session` that reads the last N session logs and prints three sections: shipped, decisions, outstanding.
- A shared, deterministic aggregation script at `skills/plab-wrap-session/scripts/aggregate-logs.py` that performs window selection and per-log section extraction, callable by any skill in the plugin.
- A shared contract document describing that script's rules, so `plab-continue-session` can consume the identical logic for C-05.
- An explicit statement, on every count the digest prints, of which harnesses and which log stores were read to produce it.

### Non-Goals

- **Not a dashboard.** No charts, no persisted index file, no cross-session metrics beyond the three named questions. The roadmap states this explicitly and it is load-bearing: "Not a dashboard" [S1].
- **Not a fifth session-log-writing mode.** The four writing modes (deep, quick, blocked, final) are unchanged. `--digest`, like `--organize` before it, runs instead of a wrap rather than adding a way to write one; the roadmap's "do not add modes" caution is about the four writing modes, not about a separate read-only operation [S1]/[S6].
- **Not full cross-harness capture.** W-05 is the roadmap's W-5, cross-harness capture; unlike D-04, D-05, and D-07, it has no assigned release in the version ladder as of this writing, so nothing here schedules it. It proposes either running capture-lite in both harnesses or having the digest read `~/.codex/sessions` directly; neither is built here. This spec implements only W-05's narrower, load-bearing lesson: state which harnesses a number covers [S1].
- **Not a consumer of capture-lite's unwrapped-session data.** D-04 (capture-lite consumers) is wrap-time, this-session-window tooling; folding its unwrapped-session counts into a multi-log digest is a plausible future extension, not built here (see Open Questions).
- **Not a same-arc deduplication mechanism.** D-05 (superseding logs) already removes same-arc duplicate logs from the discovery corpus at write time, which is why this spec builds none (see AC-6).
- **Not a change to the session-log format.** No new frontmatter field is added to individual logs by this effort.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer (JP) | Invokes digest mode and reads the report | Runs `/plab-wrap-session --digest [N]`; reads the three sections; no confirmation step, since digest mode is read-only and writes nothing |
| Agent (Claude Code or Codex session running the skill) | Executes digest mode | Calls `skills/plab-wrap-session/scripts/aggregate-logs.py` for the deterministic window and rollup, then narrates that output into the three-question report |

## Requirements

1. `plab-wrap-session` gains a `--digest [N]` invocation that runs instead of a wrap: no session log is written and no hygiene sweep runs, mirroring the contract `--organize` already established for a non-wrap operation [S6].
2. Window selection (which logs count as "the last N") reuses the pooling, allowlist, and sort rules already defined once in `log-discovery.md`: the flat store plus its `YYYY-MM` folders across all three stores (current and both legacy locations), non-date subdirectories invisible, lexical-descending filename sort. This effort extends that rule from "return the newest one" to "return the newest N"; it does not redefine the rule [S2].
3. The extraction and rollup logic is deterministic and script-computed, not model-recalled: the script reads each log's frontmatter and its Work Completed, Decisions Made, Waiting on You, and Outstanding Issues sections, and emits structured output. The agent's job is to narrate that output into prose, not to re-derive it from N full log bodies. This mirrors the derived-versus-authored split already established for single-log facts [S1]/[S7].
4. Output is exactly three labeled sections, in this order: what shipped, what decisions were made, what is still outstanding. Nothing else is added; this is the roadmap's explicit minimalism constraint, not an oversight [S1].
5. The outstanding section must make a long-lived item visibly different from a fresh one. Waiting-on items already carry a `(blocked since YYYY-MM-DD)` marker and are carried forward log-to-log once D-07 (the Waiting-on blocker contract, shipping v0.4.0, before this effort) lands, so the digest can read that marker directly rather than computing recurrence itself. Outstanding Issues items are not carried forward, so the digest scans the full window for those and reports each item's first-seen log [S1]/[S3]/[S9].
6. Every count the digest prints, logs read, shipped items, decisions, outstanding items, is paired with an explicit statement of which harnesses (the `agent` frontmatter value recorded on each log) and which store(s) were read. This is W-05's lesson, not its full mechanism: a number presented without its scope was the actual failure, not merely missing data [S1]/[S8].
7. The digest performs no logic to detect that two logs describe the same arc. D-05 (superseding logs, shipping v0.4.0, before this effort) already moves same-arc duplicates out of the discovery corpus at write time by archiving the older log to a subdirectory that discovery's allowlist does not read; the digest inherits a corpus that is already deduplicated by the time it runs [S3]/[S9].
8. The window-selection-and-extraction logic ships as `skills/plab-wrap-session/scripts/aggregate-logs.py`, inside `plab-wrap-session`'s own directory rather than a third shared plugin-root location, even though `plab-continue-session` also consumes it. This is the release plan's own resolved placement decision: wrap already owns in-skill scripts and, after v0.7.0, the executable log-format contract this layer must agree with, so the aggregation belongs next to that contract rather than in a new component with its own always-on cost [S4]. `plab-continue-session` already crosses into this skill's sibling directory to read `log-discovery.md`, just in the other direction, so a cross-skill script invocation is not a new kind of coupling [S6]. The script follows the CLI shape already established by `organize-logs.py`: a positional store path, a count flag, and a `--json` output mode [S7].

## Acceptance Criteria

AC-1: Invoking `/plab-wrap-session --digest [N]` runs digest mode instead of writing a session log: no log file is created and no hygiene sweep runs. [S6]

AC-2: Digest mode selects its window of up to N logs using the pooling, allowlist, and sort rules defined once in `log-discovery.md` (flat store plus `YYYY-MM` folders across all three stores, non-date subdirectories invisible, lexical-descending filename sort), extended from "return the single newest" to "return the newest N"; digest mode defines no separate discovery logic of its own. [S2]

AC-3: Digest output contains exactly three labeled sections, no more: what shipped, what decisions were made, and what is still outstanding, computed across the read window. [S1]

AC-4: The outstanding section distinguishes an item that persists across more than one log in the window from an item appearing only in the newest log, for example by carrying forward a Waiting-on item's `(blocked since YYYY-MM-DD)` marker or by naming the log an Outstanding Issues item was first seen in. [S1]/[S3]/[S9]

AC-5: Every count the digest prints, logs read, shipped items, decisions, and outstanding items, is paired with an explicit statement of which harnesses (the `agent` frontmatter value of each log read) and which store or stores were read to produce it. [S1]/[S8]

AC-6: Digest mode contains no logic to detect or collapse same-arc duplicate logs; it relies on D-05 having already moved same-arc duplicates out of the discovery corpus at write time. [S3]/[S9]

AC-7: The window-discovery-and-extraction logic ships as a script at `skills/plab-wrap-session/scripts/aggregate-logs.py`, invocable independently of `plab-wrap-session`'s own instructions, so that `plab-continue-session`'s arc-resume mode (C-05, the roadmap's C-5) can call the identical logic instead of reimplementing it. [S4]/[S6]

AC-8: When N is omitted, digest mode defaults to reading the last 10 logs; N may be overridden explicitly, for example `/plab-wrap-session --digest 20`. [model-inference]

## Behavior / Examples

**Example 1: ordinary digest run.**

```
/plab-wrap-session --digest
```

reads the newest 10 logs (the default from AC-8) across `_local/_session-logs/` (flat and month folders) and the two legacy stores, and prints something in the shape of:

```
## Digest: last 10 session logs (2026-07-02 through 2026-08-23)

Coverage: 10 logs read from _local/_session-logs/ (8 claude-code, 2 codex-cli).
Legacy stores empty. No capture-lite unwrapped-session data included.

### What shipped
- --organize mode and month-folder archiving (2026-08-18)
- ...

### Decisions made
- Superseding logs archive rather than delete (2026-08-17)
- ...

### Still outstanding
- The source-of-truth ruling (blocked since 2026-07-xx, first seen 2026-07-14, present in 6 of 10 logs)
- ...
```

The "Coverage" line is mandatory per AC-5 regardless of how the counts above it read; a digest that happens to read only Claude Code logs still states that explicitly rather than omitting a Codex line because it would read zero.

**Example 2: fewer logs exist than requested.**

`/plab-wrap-session --digest 20` in a project with only 6 logs total reads all 6 and states "6 logs read (fewer than the 20 requested; that is the entire corpus)" rather than silently reporting on 6 logs as though 20 had been asked for and honored.

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Token economy | `--digest` is invocation-only cost with zero always-on description growth; the model narrates the script's pre-extracted rollup rather than re-reading N full log bodies | [S1]/[S5]/[S7] |
| Determinism | Window selection, section extraction, and the harness tally are entirely script-computed; only the three sections' prose is model-authored | [S7]/[S8] |
| Reuse | The aggregation logic exists in exactly one place consumable by two skills, not duplicated per skill | [S4] |
| Mechanization rung | Rung 2: a committed script the maintainer or agent runs on demand. No CI gate applies; this is a reporting feature, not a correctness check | [S7] |

## Revisions

| Date | Change | Author |
|---|---|---|
| 2026-08-23 | Initial draft created | Claude (agent) |

## Sources & Evidence

- [S1] the maintainer's private plab-wrap-session evolution roadmap, 2026-08-16 (maintainer-local, gitignored; exists on disk). Sections W-04 (the roadmap's own heading reads "W-4", lines 76-85), W-05 (the roadmap's own heading reads "W-5", lines 89-95), "Current state" harness-scope precedent (line 15), "What not to do" (lines 113-117). Credibility: A, first-party maintainer-authored roadmap.
- [S2] `skills/plab-continue-session/references/log-discovery.md` (lines 15-44). The corpus pooling, allowlist, and sort rules this effort extends from N=1 to N=many. Credibility: A, verified current shipped file.
- [S3] the maintainer's private defect record for the wrap/continue pair, 2026-08-18 (maintainer-local, gitignored; exists on disk). D-05, same-arc superseding logs (lines 101-111, the "removed at write time instead of demanding dedup logic at read time forever" line is 109); D-07, the Waiting-on blocker contract's blocked-since marker and carry-forward (lines 129-144); D-04, capture-lite consumers and the ordering constraint (lines 83-97). Credibility: A, first-party maintainer-authored addendum, verified.
- [S4] `docs/internal/release-plans/plan_07_aggregation/plan.md`, Open Questions / Decisions, D1 "Where the shared aggregation layer lives" (lines 109-140). The resolved, maintainer-accepted decision that the aggregation layer lives inside `plab-wrap-session` rather than a third shared plugin-root location, with its reasoning. Credibility: A, first-party, this release's own planning artifact, verified current file.
- [S5] `AGENTS.md` (design frame lines 15-18). The token-economy and single-user design frame this effort is judged against. Credibility: A, verified current file.
- [S6] `skills/plab-wrap-session/SKILL.md`. Organize Mode section (lines 82-106, "runs instead of a wrap" is line 84) as the direct precedent for a non-wrap operation. Credibility: A, verified current file.
- [S7] `skills/plab-wrap-session/scripts/organize-logs.py` (lines 113-141). The CLI shape (positional store, a flag, `--json` output) this effort's script follows. Credibility: A, verified current file.
- [S8] `skills/plab-wrap-session/references/frontmatter-schema.md` (line 29). The `agent` Tier 2 field, the per-log harness signal the coverage statement in AC-5 is built from. Credibility: A, verified current file.
- [S9] `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-05_superseding-logs/spec.md` and `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-07_waiting-on-blocker-contract/spec.md`. These sibling efforts' own specs now exist in this repository (written independently of this document, targeting the earlier v0.4.0 release) and confirm, with their own AC, the two mechanisms [S3] describes from the proposal-stage `pair-defects.md`: D-05's AC-3 and AC-6 confirm the `_superseded/` archive path and its exclusion from `log-discovery.md`'s allowlist; D-07's AC-1 and AC-4 confirm the `(blocked since YYYY-MM-DD)` marker and the carry-forward mechanism. Credibility: A, first-party, this release's own sibling planning artifacts, verified by direct reading.

### Unverified Claims

- AC-8's default of 10 logs is a proposed default, not sourced from either roadmap document; the roadmap only says "the last N logs" without naming a number. Confirm or adjust before implementation, hence `requires-human-review: true`.

## Open Questions / Decisions

| ID | Question | Status |
|---|---|---|
| D1 | Is 10 the right default window for `--digest`? | Open |
| D2 | Should the digest eventually fold in D-04's capture-lite unwrapped-session counts? | Deferred |
| D3 | Should `skills/plab-wrap-session/scripts/aggregate-logs.py` call a per-log parsing utility from W-02 (derived log facts, shipping v0.7.0, before this effort) instead of parsing Markdown sections itself? | Resolved: no, see below |

**D1.** AC-8 proposes 10 as the default log count for a digest run with no explicit N. This is a guess calibrated to "recent enough to be a real arc, small enough to stay cheap," not a number either roadmap states. The maintainer should confirm or replace it during implementation.

**D2.** W-04's own roadmap section does not ask for capture-lite integration; W-05 (cross-harness capture, the roadmap's W-5) gestures at Codex-side data more broadly. Folding D-04's unwrapped-session counts into the digest's "outstanding" or a fourth implicit signal is plausible but was not requested, and adding it now would grow the three-question contract past what the roadmap asked for. Held for a future effort if the unwrapped-session gap turns out to matter across a multi-log window, not just at single-session wrap time.

**D3.** Resolved by directly reading W-02's own spec (`docs/internal/release-plans/plan_06_derived-facts/W-02_derived-log-facts/spec.md`), which already exists in this repository as of this writing, drafted alongside this one, even though W-02 has not actually shipped: it targets v0.7.0, which sequences before this effort's v0.8.0 in the release ladder, but its own `status:` is still `draft`, the same as this spec's. `derive-log-facts.py` derives facts about the session currently being wrapped (`machine`, `repo`, `branch`, `date`, `files-changed`, commit-range, latest-tag, a post-hoc `decisions-count`, and verification content when a live tool-call record exists) from git and the environment, before or while that session's own log is being written. It explicitly does not touch Summary, Decisions Made, Waiting on You, or the Continuation Prompt, which stay fully agent-authored (that spec's own Requirement 6 and AC-6). `aggregate-logs.py` needs the opposite operation: reading and parsing the Work Completed, Decisions Made, Waiting on You, and Outstanding Issues sections of many already-written historical logs. The two scripts solve different problems with no shared implementation surface, so there is nothing in `derive-log-facts.py` for `aggregate-logs.py` to call. What does carry forward from W-02 and D-10 (log-format-contract, `docs/internal/release-plans/plan_06_derived-facts/D-10_log-format-contract/spec.md`) is that by v0.8.0 the frontmatter fields `aggregate-logs.py` reads (`date`, `agent`, `status`, `summary`) are derived rather than recalled, so the values themselves are more trustworthy; no code-level dependency between the two scripts is needed or appropriate.
