---
id: D-11
title: Three-state, canary-verified detector gates in the Log Self-Check
type: spec
status: fulfilled
created: 2026-08-23
updated: 2026-08-24
linked-effort: the maintainer's private defect record for the wrap/continue pair, 2026-08-18
linked-plan: implementation-plan.md
ac-count: 7
source-count: 5
requires-human-review: true
target-release: v0.4.0
linked-release: docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md
priority: P1
---

# Spec: Three-state, canary-verified detector gates in the Log Self-Check

## Task Summary

**Status:** Fulfilled
**Last updated:** 2026-08-24
**Linked plan:** implementation-plan.md
**Open questions:** 2 open, see Open Questions / Decisions
**Revisions:** Initial draft

### Acceptance Criteria Fulfillment

- [x] AC-1: The dash-sweep gate runs a canary self-test before scanning the log
- [x] AC-2: A failed canary self-test reports broken and blocks exactly like findings
- [x] AC-3: A passed self-test yields correct clean or findings results for the dash-sweep gate
- [x] AC-4: The path-existence gate runs an equivalent canary self-test before scanning citations
- [x] AC-5: The SKILL.md gate bullets name each backing script explicitly
- [x] AC-6: The four non-detector gates are unchanged, with no canary mechanism added to them
- [x] AC-7: Both detectors are committed scripts requiring no new runtime dependency

### Currently In Progress

None.

## Purpose

Two of the wrap skill's six Log Self-Check gates (`skills/plab-wrap-session/SKILL.md:186`) run an
actual detector rather than stating a structural assertion, and both have failed open, silently
reporting a clean log while structurally incapable of detecting anything, three times in one week. This
effort replaces the two-state (pass/fail) shape of those two gates with three states, clean, findings,
and broken, gated by a canary self-test that must fire before either state is trusted, following the
pattern already proven in this maintainer's own `pii-gate.py`. D-11 is the roadmap's own numbering
already; both digits are needed regardless of padding, so no zero-padding transformation applies here
(unlike D-1 through D-9 elsewhere in this release).

This effort depends on D-12 (path citation precision) landing first: D-11 wraps the path-existence gate
in canary verification, and that gate's subject-matching rule is D-12's own fix. See Requirement 7 and
Open Questions. CI-01 (CI bootstrap) applies the same discipline in a different place: the release
plan's own D2 decision states that CI-01's repo-wide dash checker "must prove it still detects against a
known-positive canary before a clean result is trusted" [S3], the same discipline this effort applies at
wrap time. Neither effort is a prerequisite of the other. They are two independent applications of one
principle, which originates in the maintainer's own `pii-gate.py` and is recorded in this effort's
defect-ledger entry. The two are separate, differently-scoped scripts (this effort's dash checker scans
one drafted session log at wrap time; CI-01's checker scans the whole tracked tree in a GitHub Actions
run); this spec does not assume CI-01's file names or reuse its script, per the scope boundary set for
this task, and either may land first.

## Scope

### In Scope

- The two detector-backed Log Self-Check gates: path-existence (`SKILL.md`, currently line 194, as
  narrowed by D-12) and dash-sweep (`SKILL.md`, currently line 195).
- Two new committed scripts implementing canary-verified, three-state detection for those two gates.
- The SKILL.md gate-line wording naming those scripts.

### Non-Goals

- Does not touch the other four Log Self-Check gates (continuation-prompt self-containment, Waiting on
  You presence, summary length, frontmatter Tier 1 completeness). Those are structural assertions a
  reader verifies by looking; adding canary ceremony to them would be theater, per the source mechanism.
- Does not redefine the path-existence gate's subject-matching rule. That rule is D-12's, already
  settled; this effort consumes it.
- Does not build or modify CI-01's repo-wide dash checker. That is a separate script with a separate
  scope, tracked in its own effort.
- Does not change `plab-continue-session`. The Log Self-Check gate is wrap-only.
- Does not attempt to make the Pre-Wrap Hygiene Sweep's five checks (a different mechanism, defined in
  `references/hygiene-sweep.md`) three-state. Those are out of scope for this effort; nothing in the
  source material asks for it.

## Users / Actors

| Actor | Role | Interaction |
|---|---|---|
| Maintainer | Sole user of the wrap skill; trusts a clean Log Self-Check result to mean the log is sound | Currently cannot distinguish a truly clean log from a silently broken checker; this effort restores that distinction |
| Wrapping agent | Runs the Log Self-Check gate before writing a session log | Invokes the two named scripts instead of improvising detection logic fresh each time |

## Requirements

1. The two detector-backed gates report one of three states: `clean` (ran successfully, zero findings),
   `findings` (ran successfully, one or more hits), or `broken` (the canary self-test failed, or the
   detector could not run). [S1]
2. A gate reporting `broken` blocks the log exactly as `findings` does; the wrapping agent must never
   read a `broken` result as `clean`. [S1]
3. Before a detector's scan result is allowed to count as `clean` or `findings`, it must first prove
   itself against at least one known-positive canary, a deliberately-constructed example the detector
   must catch. [S1]
4. The canary self-test runs automatically every time the gate is invoked, as part of the same script
   execution, not as a separate step the agent could skip. This mirrors `pii-gate.py`'s structure, where
   `self_test()` runs before any scan and a failure exits before scanning begins. [S2]
5. The detector logic for both gates is a named, committed script that the SKILL.md gate line invokes
   explicitly, replacing prose the agent previously had to improvise into a shell command at check time.
   Agent-improvised detection produced all three recorded failures: a broken shell escape, a Perl regex
   reading undecoded bytes, and a prior `ripgrep -E` mistake recorded in the skill-candidates memo. [S1]
6. The four non-detector Log Self-Check gates are unchanged: they remain plain assertions a reader
   verifies by looking, with no canary mechanism added. [S1]
7. This effort lands after D-12 (path citation precision). The path-existence gate's canary corpus this
   effort authors needs a known-not-flagged example shaped like a bare, separator-free citation, which
   only has a stable, correct answer once D-12's narrowed subject rule already governs the gate.
   [model-inference: neither roadmap entry states this ordering; it is derived by combining this
   effort's own canary-plus-anti-canary precedent with D-12's mechanism. See Open Questions.]

## Acceptance Criteria

**AC-1:** Given the dash-sweep gate is invoked, when it runs, then it executes a canary self-test before
scanning any log content, checking at least one string that must be caught (containing a genuine
em-dash or en-dash character) and at least one string that must not be flagged (containing only plain
hyphens or the words "em-dash" or "en-dash" spelled out with no actual character). [S1][S2]

**AC-2:** Given the dash-sweep gate's canary self-test fails (a must-catch example is not caught, or a
must-not-flag example is incorrectly flagged), when the gate runs, then it reports `broken`, exits with
a distinct non-zero, non-one exit code, and this blocks the log exactly as a `findings` result would.
[S1][S2]

**AC-3:** Given the dash-sweep gate's canary self-test passes, when the drafted log contains zero
em-dash or en-dash characters, then the gate reports `clean`; when the log contains one or more, then
the gate reports `findings` and names the offending line number(s). [S1]

**AC-4:** Given the path-existence gate (as scoped by D-12) is invoked, when it runs, then it executes a
canary self-test before scanning any citations, checking at least one known-missing, in-scope citation
that must be caught and at least one known bare, separator-free citation that must not be flagged, and
reports `broken` when that self-test fails. [S1][S2]

**AC-5:** Given the SKILL.md Log Self-Check section, when a reader looks at the path-existence and
dash-sweep bullets, then each names its backing script by path (for example, `scripts/dash-check.py`),
and the other four bullets remain unmodified prose with no script reference. [S1]

**AC-6:** Given a diff of this effort against `SKILL.md`'s Log Self-Check section, when the diff is
reviewed, then only the path-existence and dash-sweep bullets (and the short explanatory sentence
introducing the three-state contract) changed; the continuation-prompt, Waiting-on-You, summary-length,
and frontmatter-Tier-1 bullets are byte-for-byte unchanged. [S1]

**AC-7:** Given the two new scripts, when their location is checked, then both are committed files
under `skills/plab-wrap-session/scripts/`, alongside the existing `organize-logs.py`, written in Python
with no dependency beyond the Python 3 standard library, consistent with the runtime already available
to this skill (organize-logs.py's own precedent) and with `pii-gate.py`'s "no new dependency" claim.
[S1][S2][S3]

## Behavior / Examples

**Example 1: broken detector caught before it ships a false clean.**
Given: a hypothetical regression where `dash-check.py`'s regex is rewritten to a form that, like the
Perl bug in the evidence, reads bytes without decoding them.
When: the gate runs (any invocation, on any log).
Then: the canary self-test's must-catch example (a string containing a real em-dash character) is not
detected, so `self_test()` fails, the script prints a message to that effect and exits 2, and the
wrapping agent sees `broken`, not a passing check. This is the exact class of failure recorded in the
evidence [S1], made structurally impossible to ship past silently.

**Example 2: genuine finding still fires.**
Given: a drafted log that (contrary to the rules elsewhere in this skill) contains a literal em-dash
character in its Summary section.
When: the gate runs.
Then: the canary self-test passes first (proving the detector works), the scan then finds the real hit,
and the gate reports `findings` naming the line.

**Example 3: path-existence gate inherits D-12's scope, then adds canary proof on top.**
Given: the log citation `scripts/em-dash-sweep.sh` (path separator present, does not exist in the
repo, per D-12's Example 1) and the log citation `` `test-organize-logs.py` `` (backtick-wrapped, no
separator, per D-12's Example 2).
When: the path-existence gate runs (after both D-12 and this effort have landed).
Then: the canary self-test runs first, proving the script both catches a deliberately-missing,
in-scope canary and correctly ignores a deliberately-bare, separator-free anti-canary; only after that
proof does the real scan run, flagging `scripts/em-dash-sweep.sh` and staying silent on
`` `test-organize-logs.py` ``, matching D-12's own worked examples.

**Example 4: constructing a real dash codepoint in the canary corpus without ever writing the literal
character.** The canary strings inside `dash-check.py` must contain a genuine em-dash or en-dash
codepoint to be valid must-catch examples, but this repository's own PreToolUse hook blocks writing a
literal em-dash or en-dash character to any file, including this script's own source. Python's `chr()`
builtin resolves this cleanly: calling it with the hex value 2014, or with 2013, constructs the real
codepoint at run time from plain ASCII source text, so the script file never contains the literal
character or anything that looks like one. This was verified directly this session rather than assumed,
using the digits 2014 as the argument to `chr()` and comparing the result against the string built with
it:

```
python3 -c "
s = 'x' + chr(0x2014) + 'y'
print('length:', len(s))
print('contains the target codepoint:', chr(0x2014) in s)
print('codepoint of middle character:', hex(ord(s[1])))
"
```

which printed `length: 3`, `contains the target codepoint: True`, and `codepoint of middle character:
0x2014`. A Python backslash-u string escape would also decode correctly here, unlike the broken shell
and Perl escapes described in the evidence, but composing this very document surfaced a concrete,
repeatable authoring risk with that form: an escape sequence sitting next to prose that discusses the
character it represents is easy for a human or a model to mistranscribe back into the literal glyph by
hand, which is exactly the kind of silent, self-inflicted failure this effort exists to guard against.
`chr()` built from a hex integer has no such risk, there is no escape-looking token for an editor or an
author to helpfully expand. The canary source should build its target characters this way, not with
string escapes. [S4]

## Non-Functional Requirements

| Category | Requirement | Source |
|---|---|---|
| Reliability | A detector that cannot detect must report `broken`, never `clean`, in 100% of cases where its own canary self-test fails | [S1] |
| Token cost | The change lives in SKILL.md body text and two new script files; zero always-on session cost, since neither the frontmatter description nor any always-loaded text grows | design frame, conventions section 3 |
| Runtime dependency | No new dependency beyond the Python 3 standard library already required by `organize-logs.py` | [S1][S2][S3] |
| Scope discipline | Canary ceremony applies to exactly the two detector-backed gates; the other four remain simple assertions | [S1] |

## Revisions

| Date | Change |
|---|---|
| 2026-08-23 | Initial draft created |

## Sources & Evidence

- **[S1]** the maintainer's private defect record for the wrap/continue pair, 2026-08-18, "D-11. The Log Self-Check gates are
  two-state and can fail open" (lines 187-209). Maintainer-local, gitignored. Credibility A: primary
  planning artifact; the three recorded failures are each independently dated and one (the dash-hook
  blocking this very entry's prose) was observed live during the document's own authoring.
- **[S2]** the maintainer's canary-verified PII gate script. Maintainer-local, gitignored (not shipped in this
  plugin; it is a different repo's migration tool the maintainer wrote). Credibility A: verified by
  direct read. Specific anchors checked: exit-code contract in the module docstring (lines 30-35: 0
  clean, 1 dirty, 2 broken, "NEVER interpret [2] as clean"); `self_test()` function (lines 206-227),
  which checks a `MUST_MATCH` list and a `MUST_NOT_MATCH` list and exits 2 with an explicit
  "GATE SELF-TEST FAILED" message before any scan runs; `read_text(encoding="utf-8")` calls at lines
  238 and 299, confirmed as the mechanism that avoids a platform-default (non-UTF-8) text decoding on
  Windows. Note: the source document [S1] describes this script as running "14 canaries and 14
  anti-canaries"; a direct count of this file's `MUST_MATCH` and `MUST_NOT_MATCH` lists found 16 and 14
  respectively. This spec cites the mechanism (self-test-before-scan, MUST_MATCH/MUST_NOT_MATCH,
  three-way exit code) rather than the specific counts, which are not load-bearing for this effort's
  AC.
- **[S3]** `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md`, decision D2 (lines 153-186).
  Credibility A: verified by direct read; cited for the CI-01 cross-reference in Purpose, specifically
  the sentence naming this effort's canary discipline as a precondition for CI-01's dash checker.
- **[S4]** Verified empirically this session (see Behavior/Examples, Example 4, for the exact command
  and output). Credibility A: directly reproduced, not inferred, confirming that constructing the
  target codepoint via Python's `chr()` builtin from a hex integer behaves correctly and safely,
  distinct from the shell and Perl failures recorded in [S1].
- **[S5]** `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/CI-01_ci-bootstrap/spec.md`, Purpose section and
  Open Question OQ-2 (lines 45, 61, 140-141, 165-167 as written when this citation was checked).
  Credibility A: verified by direct read. Cited in Open Questions below for the precedence-direction
  inconsistency between this spec and CI-01's.

### Unverified Claims

- **Requirement 7** ([model-inference]): the "D-11 after D-12" sequencing is this author's inference,
  not a statement in either roadmap entry. See Open Questions for the full reasoning and the
  alternative considered.

## Open Questions / Decisions

| ID | Title | Resolution | Status | Updated |
|---|---|---|---|---|
| D1 | Sequence this effort after D-12 | D-12 executed first; resolved by execution | Resolved | 2026-08-25 |
| D2 | Precedence direction versus CI-01, reconcile the two Purpose sections | Applied: Option B, no direction claimed | Applied | 2026-08-23 |

### D1: Sequence this effort after D-12 (Open)

**Summary.** Whether this effort must land strictly after D-12 (path citation precision), or whether
the two can land in either order, or concurrently.

**Context.** This effort's mechanism [S1] says the pattern generalizes to both detector-backed gates
using `MUST_MATCH`/`MUST_NOT_MATCH` canaries and anti-canaries, following `pii-gate.py` [S2]. For the
path-existence gate specifically, a faithful anti-canary needs a known example that must NOT be
flagged, and the most natural such example is a bare, separator-free citation, exactly the shape D-12
exists to exclude. If this effort's canary corpus is authored before D-12 lands, that anti-canary would
be asserting behavior the pre-D-12 gate does not actually have (the current gate DOES flag such
citations, per D-12's own evidence of 6 false positives in one wrap), meaning the anti-canary would fail
against the real gate until D-12 also lands, or would have to be written to match the current, buggy
behavior and then rewritten once D-12 ships. Landing D-12 first avoids authoring a canary against
soon-to-be-obsolete behavior.

**Desired outcome.** Whoever executes these two efforts produces one coherent SKILL.md edit history for
the shared gate bullets, without a canary corpus that needs revision the moment the sibling effort
lands.

**Options / approaches.**

- **Option A:** D-12 lands first, this effort second (as stated in Requirement 7). This effort's
  path-existence canary corpus is authored once, against final behavior.
- **Option B:** This effort lands first, with its path-existence anti-canary either omitted initially
  (partial canary coverage until D-12 lands) or authored against current, soon-to-change behavior (then
  requiring a follow-up edit when D-12 lands).
- **Option C:** Land both in a single combined change. Rejected as a live option here because each
  effort has its own spec, AC set, and version-trail entry per this task's conventions; combining them
  would blur which AC belongs to which defect.

**Recommendation.** Option A. It is the only option that produces a canary corpus authored once, against
final behavior, with no follow-up rework implied.

---

> **Maintainer decision:** _(pending)_
>
> - **Status:** Open
> - **Choice:** (none)
> - **Reasoning:** (none)
> - **Decided by / date:** (none)

### D2: Precedence direction versus CI-01, reconcile the two Purpose sections (Applied, Option B)

> **Applied 2026-08-23, same session.** Option B was taken and both Purpose sections have been
> rewritten: neither effort is a prerequisite of the other, and both are described as independent
> applications of the `pii-gate.py` pattern that predates them. The quoted contradiction below is the
> historical state and no longer appears in either file; it is kept here as the record of why the
> wording reads as it does. Both implementation plans carry a matching note. This was applied by
> Claude during the planning session, not ratified by the maintainer, so it remains open to reversal.

**Summary (historical).** This spec's Purpose section stated that this effort "sets a precedent CI-01
(CI bootstrap) draws on directly." `CI-01_ci-bootstrap/spec.md`, written in parallel, stated the
opposite: "CI-01 is the substrate D-11 builds on, not the other way around" [S5]. The two Purpose
sections contradicted each other on a narrative point neither spec's Acceptance Criteria depend on.

**Context.** Neither effort's scripts import from or otherwise depend on the other's (confirmed by both
specs' own Non-Goals: this spec excludes building or modifying CI-01's checker, and CI-01's spec [S5]
excludes retrofitting the pattern onto this skill's gates), so the contradiction has no code-level
consequence. It is, however, exactly the "text contradicting text" defect class this release exists to
close, so it should not ship unreconciled. The controlling document both specs cite,
`docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md` decision D2 [S3], reads: "the checker must be a
committed script that CI invokes, and per D-11 it must prove it still detects against a known-positive
canary before a clean result is trusted" (verified directly, lines 175-176). That phrasing attributes the
canary requirement to this effort, not to CI-01, which is what this spec's Purpose section already
reflects.

**Desired outcome.** Both specs' Purpose sections agree on which effort originated the three-state,
canary-before-trust framing for this repository, or both are reworded to avoid claiming a direction at
all (both patterns ultimately trace to the same pre-existing `pii-gate.py` [S2], which predates the
2026-08-23 planning session that produced both specs).

**Options / approaches.**

- **Option A:** Keep this spec's reading (grounded in the "per D-11" phrase in the controlling release
  plan) and ask CI-01's author or the maintainer to correct CI-01's Purpose section to match.
- **Option B:** Reword this spec's Purpose section to drop the directional claim entirely, describing
  both efforts as independently applying `pii-gate.py`'s pre-existing pattern rather than one setting a
  precedent for the other.
- **Option C:** Leave both as written and let a human reader reconcile them at promotion time. Weakest
  option: ships two committed specs that contradict each other on a point both cite the same source
  document for.

**Recommendation (superseded by what was applied).** The original recommendation was Option A, on the
grounds that the "per D-11" phrase in the controlling release plan names this effort. Option B was
applied instead: on inspection, neither spec's own Non-Goals allow a real dependency in either
direction, so any directional claim was narrative rather than technical, and the honest description is
that both efforts apply a principle that predates them both. Option B also removes the contradiction
without requiring either effort to be sequenced behind the other.

---

> **Maintainer decision:** _(pending ratification)_
>
> - **Status:** Applied as this session's working default; NOT yet ratified
> - **Choice (applied):** Option B. Both Purpose sections reworded to drop the directional claim.
> - **Reasoning:** Neither script consumes the other's artifacts, so the direction was narrative only;
>   describing both as independent applications of the `pii-gate.py` pattern is what the evidence
>   supports and leaves either free to land first.
> - **Applied by / date:** Claude, planning session 2026-08-23. No maintainer input has been received
>   on this item.
