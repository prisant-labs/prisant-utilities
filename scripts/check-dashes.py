#!/usr/bin/env python3
"""
Repo-wide em-dash and en-dash gate. Invoked by CI, not by a skill.

EXIT-CODE CONTRACT
------------------
  0  CLEAN    canary proved AND no banned characters in any tracked file
  1  FINDINGS canary proved AND at least one banned character found
  2  BROKEN   ripgrep is missing, the canary failed, or ripgrep itself errored

NEVER INTERPRET 2 AS CLEAN. See
`docs/internal/release-plans/plan_v0.4.0/CI-01_ci-bootstrap/spec.md`.

WHY RIPGREP, NOT PERL AND NOT A SHELL-ESCAPED PATTERN
-----------------------------------------------------
Both alternatives have independently failed open on this codebase's own
tooling (spec.md R5):

  1. A sweep written as a shell escape expanded to a literal string and
     matched nothing, while reporting success.
  2. A replacement sweep in Perl read undecoded bytes and could never match
     the codepoints it was looking for, while reporting success.

Both produced the same observable output as a clean tree. Ripgrep is used
here because it decodes UTF-8 by default and because its exit codes
distinguish matched (0), no match (1), and internal error (2), which is what
makes the three-state contract above expressible at all.

WHY EVERY SUBPROCESS BOUNDARY PINS encoding="utf-8"
---------------------------------------------------
Python's subprocess text mode uses the locale encoding, which is cp1252 on
this maintainer's machine. cp1252 encodes U+2014 as the single byte 0x97,
which is not valid UTF-8, so ripgrep received bytes it could never match
and reported no hits. The canary caught it on the first run. That is the
same "read undecoded bytes, report success" failure listed above, so the
encoding is pinned explicitly at every boundary rather than inherited.

WHY THE PATTERN IS BUILT WITH chr()
-----------------------------------
The two banned characters are constructed by calling chr() on a hex integer.
Typing either character directly into this file would both defeat the point
of the script and trip the PreToolUse hook this gate promotes to CI. A string
escape is avoided for a different reason: it is the authoring shape that kept
regenerating the literal glyph by transcription elsewhere in this repository.
"""

import shutil
import subprocess
import sys

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
PATTERN = "[" + EM_DASH + EN_DASH + "]"

# Exactly one file is excluded, by name, and it is not a general suppression
# mechanism. This file displays the literal banned characters as pedagogical
# "what this looks like" examples, so it is the one place in the repository
# where their presence is correct (spec.md R6).
EXCLUSIONS = {
    "skills/plab-guide/references/voice-and-style.md",
}

RG_FLAGS = ["-n", "--color=never"]


def rg_path():
    rg = shutil.which("rg")
    if rg is None:
        print("BROKEN: ripgrep (rg) not found on PATH.", file=sys.stderr)
        sys.exit(2)
    return rg


def run_rg(rg, text):
    """Run rg against text on stdin. Returns rg's exit code: 0 hit, 1 miss, 2 error."""
    proc = subprocess.run([rg] + RG_FLAGS + [PATTERN, "-"],
                          input=text, capture_output=True, text=True,
                          encoding="utf-8")
    return proc.returncode


def self_test(rg):
    """Prove the detector before trusting any clean result."""
    known_positive = ("a sentence with a dash right" + EM_DASH + "here, and a range 2"
                      + EN_DASH + "5 as well")
    known_negative = "a sentence with a plain hyphen - right here, and a range like 2-5"

    pos = run_rg(rg, known_positive)
    neg = run_rg(rg, known_negative)

    failures = []
    if pos != 0:
        failures.append("  known-positive was NOT detected (rg exit %d)" % pos)
    if neg != 1:
        failures.append("  known-negative was wrongly flagged (rg exit %d)" % neg)

    if failures:
        print("BROKEN: gate self-test failed, the detector is not trustworthy.",
              file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print("\nExiting 2. Do NOT read this as a clean tree.", file=sys.stderr)
        sys.exit(2)


def tracked_files():
    proc = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                          encoding="utf-8")
    if proc.returncode != 0:
        print("BROKEN: git ls-files failed: %s" % proc.stderr.strip(), file=sys.stderr)
        sys.exit(2)
    files = [f for f in proc.stdout.split("\n") if f.strip()]
    return [f for f in files if f not in EXCLUSIONS]


def main():
    rg = rg_path()
    self_test(rg)
    files = tracked_files()

    proc = subprocess.run([rg] + RG_FLAGS + [PATTERN, "--"] + files,
                          capture_output=True, text=True, encoding="utf-8")

    if proc.returncode == 2:
        print("BROKEN: ripgrep errored during the real scan.", file=sys.stderr)
        print(proc.stderr.rstrip(), file=sys.stderr)
        sys.exit(2)

    if proc.returncode == 0:
        print(proc.stdout.rstrip())
        hits = len([ln for ln in proc.stdout.split("\n") if ln.strip()])
        print("FINDINGS: %d line(s) carry a banned character." % hits, file=sys.stderr)
        sys.exit(1)

    print("CLEAN: canary proved, no banned characters found in tracked files.")
    sys.exit(0)


if __name__ == "__main__":
    main()
