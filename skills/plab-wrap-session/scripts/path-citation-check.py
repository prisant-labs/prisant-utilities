#!/usr/bin/env python3
"""
Path-citation gate for a drafted plab-wrap-session log.

EXIT-CODE CONTRACT
------------------
  0  CLEAN    self-test passed AND every in-scope citation resolves
  1  FINDINGS self-test passed AND at least one in-scope citation is missing
  2  BROKEN   the detector could not prove itself, or the log could not be read

NEVER INTERPRET 2 AS CLEAN. See the sibling `dash-check.py` docstring and
`docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-11_three-state-gate-canaries/spec.md`.

THE SUBJECT-MATCHING RULE
-------------------------
Only citations that assert a location are evaluated. The base rule comes from
`docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-12_path-citation-precision/spec.md`:

  (a) contains a path separator      -> must exist, flagged when missing
  (b) backtick-wrapped, no separator -> resolved against the repo root;
                                        non-resolution is NOT a finding
  (c) neither signal                 -> prose, never evaluated at all

Branch (b) can never produce a finding by design. Naming a file is not the
same as claiming where it lives.

WHY BRANCH (a) NEEDED NARROWING AGAIN (spec Revision 2, 2026-08-25)
-------------------------------------------------------------------
"Contains a path separator" survives as prose because a reader applies
judgment. A script has none. Measured against a real session log while
implementing this gate:

  old gate, pre-D-12                    7 flags, 6 false
  D-12's rule mechanized as written    13 flags, 11 false
  this file's rule                      4 flags, 2 false

Separators appear in many things that make no claim about a file's location:
slash commands (`/plab-wrap-session`), repository slugs
(`prisant-labs/agent-plugins`), git refs (`origin/main`), globs
(`docs/skills/*/README.md`), template placeholders (`_inbox/<skill>.md`), and
URLs. Shipping the unnarrowed rule would have put a detector that fails loud
into a release themed on detectors that fail open, at a worse false-positive
rate than the gate it replaces.

`is_path_claim()` below is the resulting test. Every exclusion is mechanical,
with no per-citation judgment. See D-12 spec Revisions for the superseded
criterion and the maintainer decision authorising this.

--repo-root IS THE PROJECT BEING WRAPPED
----------------------------------------
Not this skill's installed location. Same contract as `organize-logs.py`'s
store argument (SKILL.md:91): "the store argument is relative to the project
being wrapped. Do not assume the two share a root."

The self-test never touches --repo-root. It builds a throwaway fixture and
resolves every canary against that instead, so the gate's trustworthiness does
not depend on which project happens to be under the cursor.
"""

import argparse
import os
import re
import sys
import tempfile

BACKTICK_SPAN = re.compile(r"`([^`\n]+)`")
URI_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.]*://")
WINDOWS_ABS = re.compile(r"^[A-Za-z]:[\\/]")
STRIP_CHARS = ".,;:!?()[]{}\"'<>"


def has_separator(cite):
    return "/" in cite or "\\" in cite


def is_path_claim(cite):
    """Does this citation assert where a file lives? Returns (bool, reason).

    Every branch is mechanical. Nothing here inspects meaning.
    """
    if URI_SCHEME.match(cite):
        return False, "uri scheme"
    if WINDOWS_ABS.match(cite):
        return False, "absolute path outside the repo root"
    if "*" in cite or "?" in cite:
        return False, "glob"
    if "<" in cite or ">" in cite:
        return False, "template placeholder"
    if cite.startswith("/") and cite.count("/") == 1:
        return False, "slash command"
    if not has_separator(cite):
        return False, "no separator"
    if cite.endswith("/") or cite.endswith("\\"):
        return True, "directory claim"
    base = os.path.basename(cite.rstrip("/\\").replace("\\", "/"))
    if "." not in base:
        return False, "no file extension"
    return True, "path claim"


def extract_citations(text):
    """Return [(citation, was_backtick_wrapped), ...] for one log's text.

    Bare tokens are only candidates when they carry a separator; a bare word
    with an extension and no separator is branch (c) and never enters the set.
    """
    cites = []
    for m in BACKTICK_SPAN.finditer(text):
        c = m.group(1).strip()
        if c:
            cites.append((c, True))
    # Blank out backtick spans so a wrapped citation is not counted twice.
    outside = BACKTICK_SPAN.sub(" ", text)
    for tok in outside.split():
        c = tok.strip(STRIP_CHARS)
        if c and has_separator(c):
            cites.append((c, False))
    return cites


def findings_for(text, root):
    """Return the citations that assert a location and do not resolve."""
    out = []
    for cite, backticked in extract_citations(text):
        claim, _reason = is_path_claim(cite)
        if not claim:
            continue
        if not os.path.exists(os.path.join(root, cite)):
            out.append(cite)
    return out


# Canaries are log-line fragments, evaluated against a throwaway fixture that
# self_test() builds, never against --repo-root.
MUST_MATCH = [
    "the file `missing/canary-target.md` was updated this session",
]

MUST_NOT_MATCH = [
    "the run wrote results.json into the output folder",
    "the helper `bare-nonexistent-canary.py` covers this case",
    "see `real/canary-target.md` for the worked example",
    "published at https://github.com/prisant-labs/prisant-utilities for reference",
    "type `/plab-wrap-session` to close the session",
    "the marketplace lives at prisant-labs/agent-plugins today",
    "rebased onto origin/main before pushing",
    "swept `docs/skills/*/README.md` for stale version lines",
    "the intake path is `_local/roadmaps/_inbox/<skill>.md` per convention",
    r"read C:\Users\someone\notes\scratch.md on the other machine",
]


def self_test():
    """Prove the matcher works before trusting a clean result."""
    failures = []
    with tempfile.TemporaryDirectory() as fixture:
        target = os.path.join(fixture, "real", "canary-target.md")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write("fixture canary target\n")

        for s in MUST_MATCH:
            if not findings_for(s, fixture):
                failures.append("  should have been flagged but was not: %r" % s)
        for s in MUST_NOT_MATCH:
            got = findings_for(s, fixture)
            if got:
                failures.append(
                    "  should NOT have been flagged but was: %r -> %r" % (s, got))

    if failures:
        print("GATE SELF-TEST FAILED - the matcher is not trustworthy.",
              file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print("\nExiting 2 (broken). Do NOT read this as a clean log.",
              file=sys.stderr)
        return False
    print("gate self-test: PASS (%d canaries flagged, "
          "%d anti-canaries correctly ignored)"
          % (len(MUST_MATCH), len(MUST_NOT_MATCH)))
    return True


def main():
    ap = argparse.ArgumentParser(
        description="Canary-verified path-citation gate for a drafted session log.")
    ap.add_argument("log_path", nargs="?",
                    help="the drafted log file to scan (omit with --self-test-only)")
    ap.add_argument("--repo-root", default=os.getcwd(),
                    help="the project being wrapped (default: cwd), not this skill's location")
    ap.add_argument("--self-test-only", action="store_true",
                    help="prove the detector and exit, scanning nothing")
    args = ap.parse_args()

    if not self_test():
        sys.exit(2)

    if args.self_test_only:
        sys.exit(0)

    if not args.log_path:
        print("BROKEN: no log_path given and --self-test-only not set.",
              file=sys.stderr)
        sys.exit(2)

    try:
        with open(args.log_path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print("BROKEN: could not read %s: %s" % (args.log_path, exc),
              file=sys.stderr)
        sys.exit(2)

    hits = []
    for n, line in enumerate(lines, 1):
        for cite in findings_for(line, args.repo_root):
            hits.append((n, cite))

    if hits:
        for n, cite in hits:
            print("%s:%d: does not resolve under %s: %s"
                  % (args.log_path, n, args.repo_root, cite))
        print("FINDINGS: %d citation(s) assert a location that does not exist."
              % len(hits), file=sys.stderr)
        sys.exit(1)

    print("CLEAN: canary proved, every in-scope citation in %s resolves"
          % args.log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
