#!/usr/bin/env python3
"""
what-it-is: A extractor that turns one CHANGELOG.md version section into release-note text.
what-it-does: Reads CHANGELOG.md, finds the section for a given version, strips fixed-width
  formatting (fenced blocks and inline code spans), and writes the result to stdout.
why: A hand-cut git tag is only a ref. GitHub shows a Release only when something creates one,
  and for thirteen tags nothing did. This is the piece that was missing. It deliberately does
  not decide a version, bump a file, or create a tag: the CHANGELOG entry and the tag are both
  authored by a human, and this only publishes what they already wrote.
used-by: .github/workflows/publish-release.yml, and runnable by hand for a dry run.

FIXED-WIDTH TEXT IS REMOVED ON PURPOSE. Release notes are read on a web page, in email
digests, and in the GitHub mobile app, where a monospace run wraps badly and a fenced block
scrolls sideways. The maintainer's instruction is that tags and release notes carry no
fixed-width content. Inline code spans become plain text; fenced blocks are dropped whole,
because a code block in a changelog entry is illustration rather than substance, and half a
code block is worse than none.

THREE-STATE, MATCHING EVERY OTHER SCRIPT IN THIS DIRECTORY.
  exit 0  the section was found and printed
  exit 1  no section for that version, so the caller must not publish an empty release
  exit 2  BROKEN: CHANGELOG.md missing, unreadable, not valid UTF-8, or the self-test failed

NEVER INTERPRET 2 AS CLEAN. An empty stdout with a zero exit would publish a release with no
notes, which reads as a release that had nothing to say rather than one whose extraction
broke. That is the fail-open-by-omission the other gates in this directory exist to close.

ENCODING IS PINNED. Every read passes encoding="utf-8". `scripts/check-dashes.py`'s docstring
records why: Python's text mode defaults to the locale encoding, which is cp1252 on this
maintainer's machine, and cp1252 cannot represent the same bytes UTF-8 can, so an unpinned
read can silently see the wrong thing and report a clean result that is really a broken one.
"""

import argparse
import io
import os
import re
import sys

CHANGELOG = "CHANGELOG.md"


class Broken(Exception):
    """A failure of this script or its inputs, never a property of one version section."""


def strip_fixed_width(text):
    """Remove fenced blocks entirely, then turn inline code spans into plain text."""
    text = re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def extract(changelog_text, version):
    """Return the body of the section for `version`, or None when there is no such section.

    A section runs from its own `## [x.y.z]` heading to the next `## [` heading or end of file.
    The version is matched literally rather than as a pattern, so a version containing regex
    metacharacters cannot widen the match.
    """
    pattern = r"^## \[%s\].*?$(.*?)(?=^## \[|\Z)" % re.escape(version)
    match = re.search(pattern, changelog_text, flags=re.M | re.S)
    if match is None:
        return None
    return strip_fixed_width(match.group(1))


def read_changelog(root):
    path = os.path.join(root, CHANGELOG)
    try:
        return io.open(path, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as exc:
        raise Broken("could not read %s: %s" % (path, exc))


def self_test():
    """Prove the extractor against a fixture before any real result is trusted.

    A script that cannot show it still works is not a script anyone should believe, which is
    the rule the detector gates in this directory were built on. Five properties are proven:
    a section is found and bounded by the next heading, a missing version returns None rather
    than the whole file, inline code becomes plain text, a fenced block is removed whole, and
    a version's regex metacharacters cannot widen the match.
    """
    fixture = "\n".join([
        "# Changelog",
        "",
        "## [Unreleased]",
        "",
        "- pending work",
        "",
        "## [1.2.0] - 2026-01-02",
        "",
        "Real prose with `inline code` in it.",
        "",
        "```",
        "a fenced block that must not survive",
        "```",
        "",
        "Trailing sentence.",
        "",
        "## [1.1.0] - 2026-01-01",
        "",
        "Older entry that must not leak upward.",
        "",
    ])

    got = extract(fixture, "1.2.0")
    if got is None:
        raise Broken("self-test: the 1.2.0 section was not found")
    if "Older entry" in got:
        raise Broken("self-test: the section ran past the next heading")
    if "`" in got:
        raise Broken("self-test: an inline code span survived")
    if "fenced block" in got:
        raise Broken("self-test: a fenced block survived")
    if "inline code" not in got or "Trailing sentence." not in got:
        raise Broken("self-test: real prose was lost while stripping formatting")
    if extract(fixture, "9.9.9") is not None:
        raise Broken("self-test: a missing version did not return None")
    if extract(fixture, "1.2.0") != extract(fixture, "1.2.0"):
        raise Broken("self-test: extraction is not deterministic")
    # A version carrying regex metacharacters must be matched literally, never as a pattern.
    if extract(fixture, "1.2..") is not None:
        raise Broken("self-test: the version was treated as a regex and widened the match")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Print one CHANGELOG version section as release-note text, with no fixed-width content."
    )
    parser.add_argument("version", nargs="?", help="version without a leading v, for example 0.5.3")
    parser.add_argument("--root", default=".", help="repository root holding CHANGELOG.md")
    parser.add_argument("--self-test", action="store_true", help="run the self-test and exit")
    args = parser.parse_args()

    try:
        self_test()
        if args.self_test:
            sys.stdout.write("self-test: PASS (bounded section, missing version, inline code, fenced block, literal version match)\n")
            return 0
        if not args.version:
            raise Broken("a version argument is required unless --self-test is given")

        version = args.version.lstrip("v")
        body = extract(read_changelog(args.root), version)
        if body is None:
            sys.stderr.write(
                "FINDING: CHANGELOG.md has no section for %s. Refusing to publish an empty release.\n"
                "Add the section, or publish by hand if this tag is deliberately undocumented.\n" % version
            )
            return 1
        if not body:
            sys.stderr.write("FINDING: the section for %s is empty after stripping formatting.\n" % version)
            return 1

        sys.stdout.write(body + "\n")
        return 0
    except Broken as exc:
        sys.stderr.write("BROKEN: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
