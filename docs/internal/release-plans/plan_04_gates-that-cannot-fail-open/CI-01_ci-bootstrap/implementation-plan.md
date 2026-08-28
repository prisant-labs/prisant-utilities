---
id: CI-01
title: "Implementation plan: CI bootstrap - toolkit standard gate and repo-wide dash check"
type: implementation-plan
status: complete
created: 2026-08-23
updated: 2026-08-24
linked-spec: spec.md
linked-release: docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/plan.md
ac-coverage: complete
phase-count: 3
---

# Implementation Plan: CI Bootstrap - Toolkit Standard Gate and Repo-Wide Dash Check

> **For agentic workers:** steps use checkbox syntax for tracking. Execute phases in order.

**Goal:** Give `prisant-utilities` its first CI: an automatic toolkit-standard gate and a repo-wide, canary-proven check for banned dash characters, both report-only.

**Architecture:** Two independent GitHub Actions jobs in one new workflow file, `.github/workflows/gate.yml`: `standard-gate` (the toolkit's pinned reusable Action, SARIF-enabled) and `dash-check` (a new committed Python script that invokes ripgrep as a subprocess). The script proves a canary before trusting any scan result, giving three exit states instead of a pass/fail binary. Neither job fixes, tags, or releases anything; both only report, and the toolkit gate additionally leaves a persistent Security-tab record via SARIF.

**Spec:** `spec.md`

**Target versions:** Plugin `v0.4.0` at release time, across every effort landing in that release together (this plan does not itself edit `library.json`, `.claude-plugin/plugin.json`, or `.codex-plugin/plugin.json`; see Non-Goals in `spec.md`). CI-01 does not bump either skill: `plab-wrap-session` stays `1.5.0` and `plab-continue-session` stays `1.3.0` as a direct result of this effort. The release's own version ladder separately targets wrap `1.6.0` / continue `1.4.0` across the other v0.4.0 efforts (D-03 through D-12), not this one.

**Global constraints:**
- No em-dash (U+2014) or en-dash (U+2013) anywhere this plan produces, or in any file an executing agent writes as a result of it. Use " - " or restructure. This applies with extra force here: `scripts/check-dashes.py` must build its comparison pattern from the two characters' Unicode code points in source rather than by typing either character directly, for the same reason `~/.claude/hooks/no-em-dashes.py` already does for its own source (see `spec.md` R4, S11).
- State a contract once, in one named file, and have everything else cite it. This plan is that file for CI-01; workflow YAML comments cite `spec.md` and the toolkit's own Standard sec 4.1/4.4 rather than re-deriving either.
- CI configuration MUST contain no validation logic of its own; it MUST only invoke a pinned Action or a committed, portable script (Standard sec 4.1/4.4, quoted in `spec.md` R7 and AC-7).
- Fixed values beat options for a single maintainer: the dash check's exclusion list is one named entry, not a configurable ignore-file mechanism.
- Archive, never delete; dry-run by default; per-action confirmation for anything that touches the world beyond this effort's own files. Phase 3's `CHANGELOG.md` line is proposed and confirmed, not written silently (spec.md OQ-4).

---

## Completion Status

| Phase | Goal | Fulfills AC | Owner | Status |
|---|---|---|---|---|
| P1 | Build the canary-proven dash detector | AC-5, AC-6 | agent | Done |
| P2 | Wire both gate jobs into `gate.yml` | AC-1, AC-2, AC-3, AC-4, AC-8 | agent | Done |
| P3 | Verify no inline gate logic; update agent- and human-facing docs | AC-7 | agent | Done |

---

## Phase 1: The canary-proven dash detector

**Goal:** A standalone, portable script that scans git-tracked files for em-dash and en-dash characters using ripgrep, proves its own detector against an in-memory canary before trusting any result, and exits with one of three distinguishable states.

**Files:** Create `scripts/check-dashes.py` (new file; new top-level `scripts/` directory).

**Fulfills:** AC-5, AC-6

**Steps:**
- [x] Step 1: Create `scripts/check-dashes.py` with a `#!/usr/bin/env python3` shebang and a module docstring that names the three exit states, cites `spec.md`, and states why ripgrep rather than perl or a shell-escaped pattern is the detection engine (spec.md R5: both have independently failed open on this codebase's own tooling).
- [x] Step 2: Define the two banned characters by Unicode code point, U+2014 and U+2013 (for example via Python's `chr()` builtin, called on each code point separately), and combine the two resulting single-character strings into one character-class pattern for ripgrep. Do not type either character directly into the source file: doing so would both defeat the point of this script and risk tripping the PreToolUse hook this effort promotes to CI. This mirrors the reason `~/.claude/hooks/no-em-dashes.py` also builds its own comparison values from code points rather than literal characters.
- [x] Step 3: Define an exclusion set naming exactly one file, `skills/plab-guide/references/voice-and-style.md`, with a comment stating why: that file displays the literal banned characters as pedagogical "what this looks like" examples (spec.md R6), and this is a fixed, single-entry list, not a general suppression mechanism.
- [x] Step 4: Implement `rg_path() -> str`: `shutil.which("rg")`; if `None`, print `BROKEN: ripgrep (rg) not found on PATH.` to stderr and `sys.exit(2)` before doing anything else.
- [x] Step 5: Implement `run_rg(rg: str, text: str) -> int`: run ripgrep as a subprocess (`-n`, `--color=never`, the pattern from Step 2) with `text` piped via stdin (`input=text, capture_output=True, text=True`); return its exit code. Ripgrep's own convention: 0 means matched, 1 means no match, 2 means an rg-internal error.
- [x] Step 6: Implement `self_test(rg: str) -> None`: build a known-positive string (containing both banned characters, from the same code points as Step 2) and a known-negative string (containing only plain hyphens and a numeric range such as "2-5"). Assert `run_rg(rg, known_positive) == 0` and `run_rg(rg, known_negative) == 1`. On either failure, print a `BROKEN:` message naming which side failed (known-positive not detected, or known-negative wrongly flagged) and `sys.exit(2)`. No real scan runs past this point unless both hold.
- [x] Step 7: Implement `tracked_files() -> list[str]`: run `["git", "ls-files"]`, split stdout on newlines, drop anything in the exclusion set from Step 3.
- [x] Step 8: Implement `main()`: call `rg_path()`, then `self_test(rg)`, then `tracked_files()`, then run ripgrep against the tracked-file list with the same pattern and flags as Step 5. Map its exit code: `2` prints ripgrep's own stderr under a `BROKEN:` prefix and exits 2; `0` (matched) prints the matching lines, prints a `FINDINGS: N line(s)...` summary to stderr, and exits 1; `1` (no match) prints `CLEAN: canary proved, no banned characters found in tracked files.` and exits 0.
- [x] Step 9: Guard with `if __name__ == "__main__": main()`.

**Verification:**
```
python3 scripts/check-dashes.py; echo "exit: $?"
```
Expected: prints `CLEAN: canary proved, no banned characters found in tracked files.` and reports `exit: 0` (the repo's one real dash-bearing file is excluded by name).

Prove the findings path without fabricating a violation (spec.md Walkthrough 4): temporarily comment out the one exclusion entry from Step 3, rerun the same command, confirm the output lists lines from `skills/plab-guide/references/voice-and-style.md` and reports `exit: 1`, then restore the exclusion and rerun to confirm it returns to `exit: 0`.

Prove the broken path:
```
PATH= python3 scripts/check-dashes.py; echo "exit: $?"
```
Expected: prints `BROKEN: ripgrep (rg) not found on PATH.` and reports `exit: 2`.

---

## Phase 2: Wire both gate jobs into `gate.yml`

**Goal:** A single workflow file that runs the toolkit's pinned standard gate (with SARIF upload) and the dash check from Phase 1, on pull requests and pushes to `main`, with the two toolkit-internal scripts deliberately absent and explained.

**Files:** Create `.github/workflows/gate.yml` (new file; new `.github/workflows/` directory tree).

**Fulfills:** AC-1, AC-2, AC-3, AC-4, AC-8

**Steps:**
- [x] Step 1: Create `.github/workflows/gate.yml` with `name: Gate` and a header comment block stating: (a) this file makes no pass/fail decision of its own, per Standard sec 4.1/4.4; (b) `check-parity.mjs` is not invoked because it is the toolkit's own validator-parity harness, run by the toolkit's own CI, not by consumer repos (spec.md R2, S2); (c) `verify-tag-matches-manifests.mjs` is not invoked because it requires a `package.json` this repo has never had, and `AGENTS.md` names only `check.mjs` as this repo's gate (spec.md R2, R3, S3, S4); (d) CI reports, it does not release, auto-fix, or tag (spec.md AC-8).
- [x] Step 2: Add the trigger block:
  ```yaml
  on:
    pull_request:
    push:
      branches: [main]
  ```
- [x] Step 3: Add a top-level `permissions: contents: read`.
- [x] Step 4: Add the `standard-gate` job:
  ```yaml
  jobs:
    standard-gate:
      name: Advanced Skill Library Standard
      runs-on: ubuntu-latest
      permissions:
        contents: read
        security-events: write   # required to upload SARIF to the Security tab
      steps:
        - uses: actions/checkout@v7

        - name: Grade against the Advanced Skill Library Standard
          id: gate
          uses: product-on-purpose/agent-skills-toolkit@v1.16.1   # pin a released tag, never a branch
          with:
            path: .
            fail-on-error: true
            annotations: true
            sarif: true

        - name: Upload SARIF to the Security tab
          if: always() && steps.gate.outputs.sarif-path != ''
          uses: github/codeql-action/upload-sarif@v3   # matches the toolkit's own documented example; spec.md OQ-3
          with:
            sarif_file: ${{ steps.gate.outputs.sarif-path }}

        - name: Report tier
          run: |
            echo "Earned tier: ${{ steps.gate.outputs.tier }}"
            echo "${{ steps.gate.outputs.errors }} error(s), ${{ steps.gate.outputs.warnings }} warning(s)"
  ```
- [x] Step 5: Add the `dash-check` job in the same `jobs:` block:
  ```yaml
    dash-check:
      name: "No em-dash / en-dash (repo-wide)"
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v7

        - uses: actions/setup-python@v6
          with:
            python-version: "3.12"

        - name: Install ripgrep
          run: sudo apt-get update -qq && sudo apt-get install -y ripgrep

        - name: Run the dash check
          run: python3 scripts/check-dashes.py
  ```

**Verification:**
Static: open `.github/workflows/gate.yml` and confirm both jobs match the blocks above exactly; run `grep -n "check-parity.mjs\|verify-tag-matches-manifests.mjs" .github/workflows/gate.yml` and confirm every match is inside the header comment (explaining the exclusion), never inside a `uses:` or `run:` line; run `grep -n "git tag\|git push\|npm publish\|version" .github/workflows/gate.yml` and confirm no match (AC-8).

End-to-end: push the branch and open a PR. Confirm two checks appear, named "Advanced Skill Library Standard" and "No em-dash / en-dash (repo-wide)", and both go green on a clean PR. Confirm the repository's Security > Code scanning tab shows a run attributed to `agent-skills-toolkit` after `standard-gate` completes.

---

## Phase 3: Verify no inline gate logic; update agent- and human-facing docs

**Goal:** Confirm the finished workflow contains no validation logic of its own, and bring the two documentation surfaces this effort touches into agreement with the new CI.

**Files:** Modify `AGENTS.md`. Propose (confirm before writing) a `CHANGELOG.md` entry. Read-only check of `.github/workflows/gate.yml`.

**Fulfills:** AC-7

**Steps:**
- [x] Step 1: Re-read the finished `.github/workflows/gate.yml` end to end. Confirm every conditional (`if:`) references a step output (`steps.<id>.outputs.*`) or a prior step's success/failure, never file content matched inline; confirm no `run:` block contains a regex or string comparison evaluated against tracked-file contents (the only content-inspecting logic in the whole workflow is the call to `python3 scripts/check-dashes.py`, which is a committed script, not inline YAML logic).
- [x] Step 2: In `AGENTS.md`'s `## Build and validate` section, immediately after the existing "Conformance gate" bullet (`AGENTS.md:71`), add one bullet stating that `.github/workflows/gate.yml` now runs this gate automatically on every pull request and push to `main`, alongside the dash check.
- [x] Step 3: Propose a short `CHANGELOG.md [Unreleased]` entry (an `### Added` line) stating that the repo's first CI gate now exists, covering the toolkit standard grade and the dash check. State the exact proposed line to the maintainer and confirm before writing it (spec.md OQ-4; this repo's own `doc-update-rules.md` excludes routine "CI tweaks" from this file, but this is the first CI, not a tweak, so the judgment call is surfaced rather than made silently in either direction).
- [x] Step 4: Do not modify `README.md` (excluded by this repo's own `doc-update-rules.md` for CI/infrastructure changes, and by this effort's Non-Goals). Do not modify `library.json`, `.claude-plugin/plugin.json`, or `.codex-plugin/plugin.json` (version bumps are release-level, not per-effort).

**Verification:**
```
grep -n "gate.yml" AGENTS.md
```
Expected: one new line, immediately after the existing conformance-gate bullet.

```
git diff --stat
```
Expected (once Phase 3 is complete): `AGENTS.md` changed, `CHANGELOG.md` changed only if the maintainer confirmed the proposed line, and no diff at all to `README.md`, `library.json`, `.claude-plugin/plugin.json`, or `.codex-plugin/plugin.json`.

---

**Note on the relationship to D-11 (resolved 2026-08-23).** This spec and `D-11_three-state-gate-canaries/spec.md` briefly disagreed on which effort originated the three-state, canary-before-trust pattern: each claimed the other built on it. Both Purpose sections were corrected the same day. Neither effort is a prerequisite of the other; they are independent applications of one principle that originates in the maintainer's own `pii-gate.py` and is recorded in the D-11 defect-ledger entry. The two dash checkers are deliberately separate scripts with different scopes: this effort's scans the whole tracked tree in a GitHub Actions run, while D-11's scans one drafted session log at wrap time. They share no code, and either effort may land first. No step in this plan changes as a result.

## CI and Documentation Coverage

### CI

`.github/workflows/gate.yml` is entirely new; there is no prior CI to compare against (this effort is the greenfield bootstrap). It adds two jobs. `standard-gate` promotes the toolkit's `check.mjs` grading from rung 3 (a documented, manually-run command, `AGENTS.md:71`) to rung 1 (an automatic CI check that runs on every PR and push, zero model tokens forever). `dash-check` is new rung 1: the underlying rule (no em-dash or en-dash) previously existed only as a machine-local rung-1 hook (`~/.claude/hooks/no-em-dashes.py`), not as anything repo-wide or portable. Its detector is `scripts/check-dashes.py`, a new committed rung-2 script invoked by the rung-1 CI job. Canary: an in-memory known-positive string (both banned characters) piped to ripgrep via stdin, proven to match before any real scan result is trusted, plus a known-negative anti-canary (plain hyphens, a numeric range) proven not to match, so the detector cannot silently pass a tree it should fail. Three exit states, not two: 0 clean, 1 findings, 2 broken.

### Agent-facing documentation

`AGENTS.md`'s `## Build and validate` section gains one line (Phase 3, Step 2), so an agent reading it before working in this repo learns the gate now runs automatically rather than only on manual invocation. No `skills/*/SKILL.md` or `skills/*/references/*.md` changes: this effort does not touch either skill's runtime behavior, and `skills/plab-guide/references/voice-and-style.md`'s own G-11 convention is explicitly out of scope (spec.md OQ-1, Non-Goals).

### Human-facing documentation

`CHANGELOG.md` gains a proposed, confirm-before-writing `[Unreleased]` entry (Phase 3, Step 3; spec.md OQ-4). `README.md` is deliberately not touched, per this repo's own `doc-update-rules.md` exclusion of CI/infrastructure changes from README updates and per this plan's Non-Goals. No skill `HISTORY.md` gains an entry: this effort touches neither `plab-wrap-session` nor `plab-continue-session`'s own version or documented behavior.

---

## Rollback

Delete `.github/workflows/gate.yml`, or set `if: false` on one or both of its jobs, to immediately stop the gate from running; delete `scripts/check-dashes.py` if the dash check specifically is the problem while leaving `standard-gate` running alone. Both are net-new, self-contained files that nothing else in the repo depends on; the one added `AGENTS.md` line and any `CHANGELOG.md` line are prose-only and safe to leave in place or revert independently of the workflow itself. No session-log format, schema, or other skill's runtime behavior is touched anywhere in this effort, so rollback's blast radius is exactly CI reverting to its pre-CI-01 state: conformance checked only when the maintainer remembers to run `check.mjs` by hand, and dash characters caught only on the one machine that has the hook installed.
