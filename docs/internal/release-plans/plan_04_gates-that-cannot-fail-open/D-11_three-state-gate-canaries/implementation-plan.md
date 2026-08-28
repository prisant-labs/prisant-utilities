---
id: D-11
title: "Implementation plan: Three-state, canary-verified detector gates in the Log Self-Check"
type: implementation-plan
status: complete
created: 2026-08-23
updated: 2026-08-24
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md
ac-coverage: complete
phase-count: 4
---

# Implementation Plan: Three-state, canary-verified detector gates in the Log Self-Check

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Replace the wrap skill's two improvised, two-state detector gates (path-existence, dash-sweep)
with committed scripts that prove themselves against a canary before any scan result is trusted, and
report clean, findings, or broken instead of a plain pass or fail.

**Architecture:** Two new, independent Python scripts under `skills/plab-wrap-session/scripts/`,
`dash-check.py` and `path-citation-check.py`, each self-contained (canary corpus embedded as literals,
no external data file), each following `pii-gate.py`'s shape: a `self_test()` that runs before any
scan and exits 2 on failure, and a three-way exit code (0 clean, 1 findings, 2 broken). SKILL.md's Log
Self-Check section gains one short explanatory sentence about the three-state contract plus two rewritten
bullets naming the scripts explicitly. The other four gates, and every other file in the skill, are
untouched.

**Spec:** `spec.md`

**Target versions:** `plab-wrap-session` 1.6.0. This effort contributes content only; the
`metadata.version` frontmatter bump and the plugin/manifest version bumps are release-level actions
tracked in `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md`'s Doc-Update Checklist, shared across
every v0.4.0 effort that touches wrap. Do not bump `metadata.version` in this plan's phases.

**Global constraints:**

- No em-dash (U+2014) or en-dash (U+2013) characters anywhere, including inside canary strings, code
  comments, and docstrings. Build the actual codepoints in the scripts' canary corpus using `chr()`
  called on the hex integer (`chr(0x2014)`, `chr(0x2013)`), never a string escape and never the literal
  glyph. This is not stylistic: this exact plan's sibling spec document (`spec.md`, Example 4) hit the
  repository's own dash-blocking hook three times while drafting the equivalent example with a string
  escape, and the escape form is what kept regenerating the literal character by transcription. `chr()`
  built from a hex integer has no equivalent failure mode and is the required technique here.
- State the three-state contract once, in SKILL.md's Log Self-Check section. Do not restate the canary
  mechanism's rationale inside the scripts beyond a short docstring pointer back to `spec.md`.
- This plugin is built for one user, its maintainer. No configuration surface, no third-party
  onboarding, no flags beyond what each script's own operation requires (`--self-test-only`, and for
  `path-citation-check.py`, `--repo-root`).
- **Sequencing precondition:** D-12 (path citation precision)
  (`docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-12_path-citation-precision/`) must already be merged to
  `main` before Phase 2 of this plan begins. Phase 2 authors `path-citation-check.py`'s canary corpus
  against D-12's narrowed subject rule; if D-12 has not landed, stop and land it first rather than
  guessing at the rule's final wording.
- Do not modify the four non-detector Log Self-Check bullets (continuation-prompt, Waiting on You,
  summary length, frontmatter Tier 1). Touching them is out of scope for every effort in this release
  except the ones that specifically name them.

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Build the canary-verified dash-sweep script | AC-1, AC-2, AC-3, AC-7 | agent | Done |
| P2 | Build the canary-verified path-citation script | AC-4, AC-7 | agent | Done |
| P3 | Rewrite the SKILL.md gate bullets to invoke both scripts | AC-5, AC-6 | agent | Done |
| P4 | Documentation and version-trail content | N/A (documentation) | agent | Done |

---

## Phase 1: Build the canary-verified dash-sweep script

**Goal:** A committed script that proves it can detect a real em-dash or en-dash character before
trusting any scan of a drafted log, and reports one of three states.

**Files:** Create `skills/plab-wrap-session/scripts/dash-check.py`

**Fulfills:** AC-1, AC-2, AC-3, AC-7

**Steps:**

- [x] Step 1: Create the file with a module docstring modeled on `_local/migration/2026-08-14/pii-gate.py`'s
  own docstring shape: state the exit-code contract up front (0 clean, 1 findings, 2 broken, "never
  interpret 2 as clean"), and state explicitly why the canary strings are built with `chr()` rather than
  a string escape (see Global constraints above), so a future editor does not "helpfully" rewrite them
  back into an escape or a literal character.
- [x] Step 2: Add argparse with a positional `log_path` (the drafted log file to scan) and a
  `--self-test-only` flag, mirroring `pii-gate.py`'s own `--self-test-only` flag.
- [x] Step 3: Define the canary corpus as module-level lists, built with `chr()`:
  - `MUST_MATCH`: at least two entries, one containing `chr(0x2014)` (em-dash) mid-string and one
    containing `chr(0x2013)` (en-dash) mid-string, each embedded in an otherwise-ordinary sentence
    fragment (for example: the concatenation of `"a sentence with a dash right"`, `chr(0x2014)`, and
    `"here"`).
  - `MUST_NOT_MATCH`: at least three entries: a sentence using a plain ASCII hyphen
    (`"a sentence with a plain hyphen - right here"`), a sentence spelling out the words "em dash" with
    no actual character, and a numeric range written with a plain hyphen (`"a range like 2-5"`).
- [x] Step 4: Implement `self_test()`: for every `MUST_MATCH` string, confirm the detection regex finds
  a hit; for every `MUST_NOT_MATCH` string, confirm it finds none. On any failure, print a
  "GATE SELF-TEST FAILED" message to stderr naming which canary or anti-canary failed and return
  `False`; on success print a one-line pass summary with the corpus sizes and return `True`. Mirror
  `pii-gate.py:206-227`'s structure exactly.
- [x] Step 5: Implement the scan: read `log_path` with `open(log_path, encoding="utf-8")` (never rely on
  a platform-default encoding; this matters specifically on Windows, per `pii-gate.py:238` and `:299`),
  iterate lines, and on each line search for either target codepoint using a character class built from
  the same `chr()` calls used in the canary corpus (not a re-typed escape). Collect `(line_number,
  line_text)` for every hit.
- [x] Step 6: Wire `main()`: run `self_test()` first, always, even when scanning is also requested. On
  failure, print to stderr and `sys.exit(2)`. If `--self-test-only`, exit 0 after a passing self-test
  without scanning anything. Otherwise scan `log_path`; if any hits, print them with line numbers and
  `sys.exit(1)`; if none, print a clean confirmation and `sys.exit(0)`.

**Verification:**

- `python scripts/dash-check.py --self-test-only` (run with cwd at
  `skills/plab-wrap-session/`) exits 0 and prints a pass summary naming the canary and anti-canary
  counts.
- Construct a scratch file containing a line built with `chr(0x2014)` (a small one-line Python script
  writing it, not a hand-typed character) and confirm `dash-check.py <scratch-file>` exits 1 and prints
  the correct line number.
- Confirm a scratch file with zero target codepoints exits 0.
- Temporarily break the detection regex (for example, comment out the em-dash branch of the character
  class), confirm `--self-test-only` now exits 2 with a message naming the specific canary that failed,
  then revert the deliberate breakage before moving on. This step is the one that matters most: it is
  the exact failure class recorded in the evidence, reproduced on purpose to confirm this script does
  not repeat it.

---

## Phase 2: Build the canary-verified path-citation script

**Goal:** A committed script implementing D-12's narrowed subject-matching rule, that proves it can
both catch a genuine missing path citation and correctly ignore a bare, separator-free one before
trusting any scan.

**Files:** Create `skills/plab-wrap-session/scripts/path-citation-check.py`

**Fulfills:** AC-4, AC-7

**Precondition:** D-12 (path citation precision) merged to `main`. Re-read the current wording of the
path-existence gate bullet in `skills/plab-wrap-session/SKILL.md` before starting this phase and confirm
it already reflects the narrowed rule; if it does not, stop this phase and land D-12 first.

**Steps:**

- [x] Step 1: Create the file with a module docstring stating the exit-code contract (same 0/1/2 shape
  as Phase 1) and a one-line summary of D-12's subject-matching rule, with a pointer to
  `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-12_path-citation-precision/spec.md` rather than restating
  the full rule's reasoning.
- [x] Step 2: Add argparse with a positional `log_path`, an optional `--repo-root` (default: current
  working directory), and `--self-test-only`. Document in the docstring, following the precedent
  already set by `organize-logs.py` (`SKILL.md:91`, "the store argument is relative to the project being
  wrapped. Do not assume the two share a root"), that `--repo-root` must be the project being wrapped,
  not this skill's own installed location.
- [x] Step 3: Implement citation extraction from the log text: find every backtick-wrapped span
  (`` `...` ``), and separately find every whitespace-delimited bare token containing a path separator
  (`/` or `\`) that is not already inside a backtick span (to avoid double-counting). For each
  candidate, classify per D-12's rule:
  - Contains a path separator (backtick-wrapped or not): in scope. Check existence at
    `<repo-root>/<citation>` (stripped of backticks). Report a finding if it does not exist.
  - Backtick-wrapped, no separator: attempt to resolve `<repo-root>/<citation>`. If it exists, treat as
    in-scope-and-passing (no output). If it does not exist, exclude it silently, no finding (per D-12
    spec Requirement 2 and its Open Question D1: this branch can never produce a finding by design).
  - Neither backtick-wrapped nor separator-bearing: excluded entirely, never entered into the candidate
    set.
- [x] Step 4: Define the canary corpus so the self-test never depends on the tree of whatever project is
  being wrapped. This script ships in a published plugin invoked against arbitrary repos, so a
  MUST_NOT_MATCH entry that asserts "this real, existing repo file is not flagged" is only valid in the
  one repo that happens to contain that file; in every other installation it would not exist, the
  self-test would then fail its own true-positive check, and every wrap everywhere else would report
  `broken`. Avoid this by having `self_test()` build its own throwaway fixture directory
  (`tempfile.TemporaryDirectory()`), write exactly one real file into it (for example
  `real/canary-target.md`, arbitrary content), and run the classification-plus-existence logic for
  every corpus entry against that fixture's path as the resolution root, never against `--repo-root` or
  this script's own installed location. Corpus, expressed relative to the fixture:
  - `MUST_MATCH`: one citation with a path separator pointing at a path that is never created inside
    the fixture, for example `` `missing/canary-target.md` ``. Must be flagged.
  - `MUST_NOT_MATCH`: at least three entries:
    - a bare word with a file extension, no backticks, no separator, appearing in an ordinary sentence
      (for example, mentioning `results.json` unformatted in running prose); the fixture is irrelevant
      to this one, since it must never be evaluated as a filesystem candidate at all;
    - a backtick-wrapped bare name with no separator that does not resolve inside the fixture, for
      example `` `bare-nonexistent-canary.py` `` (must NOT be flagged, per the branch-3 rule above);
    - a citation with a path separator pointing at the one file the fixture actually created, for
      example `` `real/canary-target.md` `` (must NOT be flagged, since inside the fixture it is a true
      positive for existence).
- [x] Step 5: Implement `self_test()` mirroring Phase 1's shape, using the fixture from Step 4 as the
  resolution root for every corpus entry: every `MUST_MATCH` entry must produce a finding; every
  `MUST_NOT_MATCH` entry must produce none. Exit 2 with a named failure on any mismatch, and tear down
  the fixture directory afterward regardless of outcome (use the context manager form so cleanup is not
  skippable). The production scan path (not self-test) still resolves against the real `--repo-root`
  argument as described in Step 3; only the self-test is fixture-isolated.
- [x] Step 6: Wire `main()` with the same 0 clean / 1 findings / 2 broken contract as Phase 1.

**Verification:**

- `python scripts/path-citation-check.py --self-test-only` exits 0 and prints a pass summary, run from
  at least two different working directories (for example, this repo's root and an unrelated scratch
  directory with no `skills/` tree at all) to directly confirm the self-test no longer depends on which
  project is being wrapped. This is the check that matters most here: it is the exact failure this
  design was rewritten to avoid, reproduced on purpose to confirm it does not occur.
- Run the script against a scratch log file containing the two lines `` `scripts/em-dash-sweep.sh` `` and
  `` `test-organize-logs.py` `` with `--repo-root` pointed at this repository, and confirm it flags only
  the first (matching D-12 spec Behavior/Examples 1 and 2). This exercises the production scan path, not
  the fixture-isolated self-test.
- As a manual smoke test specific to this repository (not part of the portable self-test corpus),
  confirm `` `skills/plab-wrap-session/SKILL.md` `` in a scratch log, scanned with `--repo-root` pointed
  at this repository, produces no finding (true positive
  for existence, not a false flag).

---

## Phase 3: Rewrite the SKILL.md gate bullets to invoke both scripts

**Goal:** SKILL.md's Log Self-Check section states the three-state contract once and names each
detector-backed gate's backing script explicitly.

**Files:** Modify `skills/plab-wrap-session/SKILL.md`

**Fulfills:** AC-5, AC-6

**Steps:**

- [x] Step 1: Re-open `skills/plab-wrap-session/SKILL.md` and re-verify current line numbers for the Log
  Self-Check section before editing (D-12's phase may have already shifted the path-existence bullet's
  wording, and other v0.4.0 efforts landing before this one may have shifted line numbers elsewhere in
  the file).
- [x] Step 2: Immediately below the section's existing intro sentence ("Verify the drafted log passes
  every gate; fix failures before writing, never after:"), add one to two sentences stating: the two
  detector-backed gates below report one of three states, clean, findings, or broken; each runs a
  canary self-test before scanning; a gate reporting broken blocks the log exactly as findings does.
- [x] Step 3: Replace the path-existence bullet (as D-12 left it) with a version that keeps D-12's
  subject-matching rule in full and adds the script invocation and exit-code contract, for example:
  "Path citations exist, detector-backed, three-state: run
  `python scripts/path-citation-check.py <log-path> --repo-root <project-root>`. Checks only citations
  with a path separator, or backtick-wrapped and resolving against the repo root; see the script's own
  docstring for the canary corpus. Exit 0 clean, 1 findings, 2 broken; broken blocks exactly like
  findings." Do not drop any part of D-12's subject-matching wording while adding this.
- [x] Step 4: Replace the em-dash/en-dash bullet with a version naming `dash-check.py`, for example:
  "No em-dash or en-dash characters, detector-backed, three-state: run
  `python scripts/dash-check.py <log-path>`. Exit 0 clean, 1 findings, 2 broken; broken blocks exactly
  like findings."
- [x] Step 5: Leave the continuation-prompt, Waiting-on-You, summary-length, and frontmatter-Tier-1
  bullets exactly as they are. Do not reformat or reorder the list.

**Verification:** `git diff skills/plab-wrap-session/SKILL.md` shows changes confined to the section
intro (one to two added sentences) and the two detector-backed bullets; a line-by-line diff confirms
the other four bullets are byte-for-byte unchanged, satisfying AC-6 directly.

---

## Phase 4: Documentation and version-trail content

**Goal:** Record the fix in the human-facing history so a reader three months from now knows what
changed, why, and where the new scripts live.

**Files:** Modify `CHANGELOG.md`, `skills/plab-wrap-session/HISTORY.md`

**Fulfills:** N/A (documentation; all behavioral AC are fulfilled by Phases 1-3)

**Steps:**

- [x] Step 1: Add a bullet under `CHANGELOG.md`'s `## [Unreleased]` section, in a `### Added` subsection
  (this introduces new committed scripts, which is an addition, distinct from D-12's `### Fixed` entry).
  Content: state that the two detector-backed Log Self-Check gates now run committed, canary-verified
  scripts reporting clean, findings, or broken, replacing improvised checks that had silently failed
  open three times.
- [x] Step 2: Check `skills/plab-wrap-session/HISTORY.md` for an existing `## 1.6.0` heading (D-12, or
  another co-landing v0.4.0 effort, may have already created it). Append this effort's bullet(s) under
  the existing heading without disturbing any other effort's content, following the file's established
  style (bold lead sentence, then supporting detail, as in the 1.5.0 and 1.4.1 entries). If no heading
  exists yet, create both the version-table row and the section heading.

**Verification:** Both files remain valid Markdown; `HISTORY.md` still has exactly one `## 1.6.0`
heading and one matching version-table row regardless of how many v0.4.0 efforts have appended bullets
beneath it.

---

## CI and Documentation Coverage

### CI

No CI workflow change. This effort moves the two detector-backed gates from mechanization-ladder rung 4
(agent-improvised detection logic, re-invented at each wrap) to rung 2 (a committed script the agent
runs), with canary-before-trust discipline layered on top per the design frame's rule that a
deterministic check is only cheaper than a remembered practice if it actually works. It does not reach
rung 1 (a CI check or hook) because the Log Self-Check is inherently a wrap-time, pre-write gate the
agent runs as part of its own workflow over one drafted log, not a repo-wide, every-commit check.
CI-01 (CI bootstrap) separately establishes a rung-1, repo-wide dash check over the whole tracked tree,
using the same canary-before-trust pattern (`docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md`,
decision D2); that is a distinctly-scoped script and out of this effort's scope per its Non-Goals.

**Note for whoever executes this plan (resolved 2026-08-23).** `CI-01_ci-bootstrap/spec.md` and this
effort's `spec.md` briefly disagreed on which effort originated the three-state, canary-before-trust
pattern: each claimed the other built on it. Both Purpose sections were corrected the same day to the
accurate statement, which is that neither is a prerequisite of the other. They are two independent
applications of one principle that originates in the maintainer's own `pii-gate.py` and is recorded in
the D-11 defect-ledger entry; the two scripts share no code, and either effort may land first. No step
in this plan changes as a result. The one real ordering constraint for this effort is unchanged and
unrelated: D-12 (path citation precision) must land before this effort, because the path-existence
gate's canary suite needs D-12's narrowed subject rule to have a stable answer.

The reconciliation is recorded in this effort's `spec.md`, Open Questions D2, which is marked Applied
(Option B) and retains the original contradictory wording as history so the reason for the current
phrasing stays legible. Like every other decision in this planning set, it was applied by Claude and
has not been ratified by the maintainer, so treat it as reversible until they say otherwise.

### Agent-facing documentation

- `skills/plab-wrap-session/SKILL.md`: the Log Self-Check section rewrite (Phase 3).
- `skills/plab-wrap-session/scripts/dash-check.py` (new, Phase 1) and
  `skills/plab-wrap-session/scripts/path-citation-check.py` (new, Phase 2): these are themselves
  agent-facing runtime artifacts, invoked at wrap time; their docstrings are their primary internal
  documentation and are covered by Phase 1 Step 1 and Phase 2 Step 1.
- No `references/*.md` file changes. Neither the six-gate list nor the canary mechanism is duplicated
  into any reference file, consistent with stating the contract once in SKILL.md.

### Human-facing documentation

- `CHANGELOG.md`: new `[Unreleased] > Added` bullet (Phase 4, Step 1).
- `skills/plab-wrap-session/HISTORY.md`: new bullet(s) under the shared `## 1.6.0` heading (Phase 4,
  Step 2), co-owned with D-12 and the other v0.4.0 efforts that touch wrap.
- `docs/skills/plab-wrap-session/README.md`: no change. As confirmed in D-12's plan, this file does not
  currently describe the Log Self-Check gates; that remains true after this effort, so nothing here
  needs to stay in sync.
- Root `README.md`, both plugin manifests, `library.json`, `manifest.generated.json`, and the
  `SKILL.md` `metadata.version` field: **not touched by this effort's phases**, for the same reason
  given in D-12's plan: these are release-level actions tracked once in
  `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md`'s Doc-Update Checklist, shared across every
  v0.4.0 effort that bumps wrap to 1.6.0.

---

## Rollback

Delete `skills/plab-wrap-session/scripts/dash-check.py` and
`skills/plab-wrap-session/scripts/path-citation-check.py`, and revert the SKILL.md Log Self-Check
section to its post-D-12, pre-D-11 wording (the two detector bullets as D-12 left them, without the
three-state intro sentence or the script references). Revert the HISTORY.md and CHANGELOG.md bullets
this effort added. No schema and no data migration exist to unwind; the scripts are pure additions with
no other file depending on their existence except the two SKILL.md bullets this same rollback also
reverts, so there is no partial-rollback hazard. If CI-01 has, by the time of rollback, started reusing
either script or its canary pattern, confirm with that effort's own plan before deleting anything it
depends on.
