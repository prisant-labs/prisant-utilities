#!/usr/bin/env python3
"""
Dash gate for a drafted plab-wrap-session log.

EXIT-CODE CONTRACT
------------------
  0  CLEAN    self-test passed AND no banned characters found in the log
  1  FINDINGS self-test passed AND at least one banned character found
  2  BROKEN   the detector could not prove itself, or the log could not be read

NEVER INTERPRET 2 AS CLEAN. A two-state gate cannot tell "found nothing" from
"never ran", and this repository has shipped that exact failure three times in
one week: a sweep written as a shell escape that expanded to a literal string,
a replacement sweep in Perl that read undecoded bytes and could never match,
and a path-existence gate that produced six false positives out of seven flags.
All three reported success while being structurally incapable of detecting
anything. See `docs/internal/release-plans/plan_04_gates-that-cannot-fail-open/D-11_three-state-gate-canaries/spec.md`.

WHY THE CANARY CORPUS IS BUILT WITH chr()
-----------------------------------------
The banned characters are constructed by calling chr() on a hex integer, never
written as a string escape and never as the literal glyph. This is a hard
requirement, not a style preference.

A string escape sitting next to prose that discusses the characters is the
exact authoring shape that kept regenerating the literal glyph by transcription
while this script's own spec was being drafted; it tripped the repository's
dash-blocking PreToolUse hook three separate times. The literal glyph is worse
still: it would make this file the one thing it exists to detect.

chr(0x2014) has no equivalent failure mode. Do not "simplify" it back.
"""

import argparse
import re
import sys

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)

PATTERN = re.compile("[" + EM_DASH + EN_DASH + "]")

# Canaries: strings the detector MUST flag. If it stops flagging these, it is
# broken, and a clean scan result from it means nothing.
MUST_MATCH = [
    "a sentence with a dash right" + EM_DASH + "here",
    "a range written badly, 2" + EN_DASH + "5, in running prose",
]

# Anti-canaries: strings the detector MUST NOT flag. These guard the other
# direction, a matcher so greedy it flags ordinary punctuation.
MUST_NOT_MATCH = [
    "a sentence with a plain hyphen - right here",
    "prose that spells out the words em dash and en dash without using either",
    "a range like 2-5 written with a plain hyphen",
]


def first_hit(text):
    """Return the matched character and its column, or None."""
    m = PATTERN.search(text)
    if m is None:
        return None
    return m.group(0), m.start()


def self_test():
    """Prove the matcher works before trusting a clean result."""
    failures = []
    for s in MUST_MATCH:
        if first_hit(s) is None:
            failures.append("  should have matched but did not: %r" % s)
    for s in MUST_NOT_MATCH:
        hit = first_hit(s)
        if hit is not None:
            failures.append(
                "  should NOT have matched but did: %r -> %r at column %d"
                % (s, hit[0], hit[1]))
    if failures:
        print("GATE SELF-TEST FAILED - the matcher is not trustworthy.",
              file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print("\nExiting 2 (broken). Do NOT read this as a clean log.",
              file=sys.stderr)
        return False
    print("gate self-test: PASS (%d canaries matched, "
          "%d anti-canaries correctly ignored)"
          % (len(MUST_MATCH), len(MUST_NOT_MATCH)))
    return True


def scan(log_path):
    """Return [(line_number, line_text), ...] for every line carrying a hit."""
    hits = []
    with open(log_path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if PATTERN.search(line):
                hits.append((n, line.rstrip("\n")))
    return hits


def main():
    ap = argparse.ArgumentParser(
        description="Canary-verified em-dash and en-dash gate for a drafted session log.")
    ap.add_argument("log_path", nargs="?",
                    help="the drafted log file to scan (omit with --self-test-only)")
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
        hits = scan(args.log_path)
    except OSError as exc:
        print("BROKEN: could not read %s: %s" % (args.log_path, exc),
              file=sys.stderr)
        sys.exit(2)

    if hits:
        for n, line in hits:
            print("%s:%d: %s" % (args.log_path, n, line))
        print("FINDINGS: %d line(s) carry a banned character." % len(hits),
              file=sys.stderr)
        sys.exit(1)

    print("CLEAN: canary proved, no banned characters in %s" % args.log_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
