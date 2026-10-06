#!/usr/bin/env python3
"""
plab-audit output-bundle self-check. Invoked by the skill after writing a bundle,
and by CI against the committed sample bundle.

EXIT-CODE CONTRACT
------------------
  0  CLEAN    self-test passed AND the bundle satisfies every structural rule
  1  FINDINGS self-test passed AND at least one rule is violated
  2  BROKEN   the bundle directory is unreadable or absent, a file could not be
              decoded, or the self-test could not prove this checker works

NEVER INTERPRET 2 AS CLEAN. Two states cannot distinguish a well-formed bundle
from a checker that has stopped working, which is the failure this repository's
gate discipline exists to prevent. A missing directory is BROKEN, not FINDINGS:
"I could not look" is not "I looked and it was fine".

WHAT THIS CHECKS, AND WHICH ACCEPTANCE CRITERION EACH RULE CARRIES
-----------------------------------------------------------------
  R1  evidence.md exists, in every mode                           AC-5
  R2  evidence.md carries a coverage statement                    AC-5, AC-14
  R3  evidence.md names the decision records consulted            AC-15
  R4  every finding in findings.md carries a file path            AC-4
  R5  roadmap.md carries exactly one horizontal break             AC-10
  R6  every roadmap item above the break cites a real finding     AC-9
  R7  no roadmap item below the break cites a finding             AC-10

WHY THE FILE SET IS INFERRED RATHER THAN REQUIRED
-------------------------------------------------
The plan for this script said "all five files exist". That is wrong for a
mode-composable skill: `--appraise` writes two files by AC-2, and a checker
demanding five would fail every legitimate partial bundle.

So the mode is inferred from what is present, and each present file is checked
against its own rules. Two implications are load-bearing:

  * evidence.md is required unconditionally. A bundle with no coverage
    statement is not an audit output regardless of mode (AC-5).
  * roadmap.md present without findings.md is a FINDING, not a tolerated
    partial. Roadmap items must cite findings (AC-9), so a roadmap with no
    findings file cannot satisfy its own contract.

WHY A FINDING ID IS RESOLVED RATHER THAN PATTERN-MATCHED
--------------------------------------------------------
R6 does not check that a roadmap item contains something shaped like `F-NN`.
It checks that the id resolves to a real `## F-NN` heading in findings.md. A
roadmap citing F-12 in a bundle whose findings stop at F-08 is exactly the
defect this rule exists to catch, and a shape check passes it.
"""

import io
import os
import re
import shutil
import sys
import tempfile

FINDING_HEADING_RE = re.compile(r"^##\s+(F-\d+)\b", re.M)
FINDING_CITATION_RE = re.compile(r"\bF-\d+\b")
HRULE_RE = re.compile(r"^---\s*$", re.M)
# A ranked roadmap item: "## 3. Attach an expiry alarm". Items are numbered by
# rank per output-bundle.md, which is what separates an item from a prose
# heading such as "## The shape of this list".
ROADMAP_ITEM_RE = re.compile(r"^##\s+(\d+\..*)$", re.M)

# A path is a backticked token containing a dot and a plausible extension, or a
# `file.ext:line` citation. Deliberately structural: matching prose that "looks
# like it mentions a file" is the mechanize-the-prose mistake this corpus has
# already made once, at a measured cost of 11 false positives in 13 flags.
PATH_RE = re.compile(r"`[^`\s]*[\w)-]\.[A-Za-z0-9]{1,6}(?::\d+(?:-\d+)?)?[^`]*`")

COVERAGE_MARKERS = ("what was read", "what was sampled", "what was skipped")
DECISION_MARKERS = ("decision record", "decision records consulted")


class Broken(Exception):
    """Raised for every condition that must exit 2 rather than 1."""


def read(path):
    try:
        with io.open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except UnicodeDecodeError as exc:
        raise Broken("%s is not valid UTF-8: %s" % (path, exc))
    except OSError as exc:
        raise Broken("cannot read %s: %s" % (path, exc))


def split_on_break(text):
    """Return (above, below, count). `below` is None when there is no break."""
    breaks = list(HRULE_RE.finditer(text))
    if not breaks:
        return text, None, 0
    first = breaks[0]
    return text[: first.start()], text[first.end():], len(breaks)


def check_evidence(bundle, findings):
    path = os.path.join(bundle, "evidence.md")
    if not os.path.isfile(path):
        findings.append("evidence.md is missing; it is required in every mode (R1, AC-5)")
        return
    low = read(path).lower()
    missing = [m for m in COVERAGE_MARKERS if m not in low]
    if missing:
        findings.append(
            "evidence.md has no coverage statement; missing section(s): %s (R2, AC-5/AC-14)"
            % ", ".join(repr(m) for m in missing))
    if not any(m in low for m in DECISION_MARKERS):
        findings.append(
            "evidence.md does not name the decision records consulted (R3, AC-15). "
            "Add a 'Decision records consulted' section, naming 'absent' where a record does not exist")


def check_findings(bundle, findings):
    """R4, and return the set of ids findings.md defines (empty when absent)."""
    path = os.path.join(bundle, "findings.md")
    if not os.path.isfile(path):
        return set()
    text = read(path)
    ids = FINDING_HEADING_RE.findall(text)
    if not ids:
        findings.append("findings.md defines no '## F-NN' finding headings (R4)")
        return set()

    # Slice each finding's body: from its heading to the next heading or EOF.
    starts = [(m.group(1), m.start()) for m in FINDING_HEADING_RE.finditer(text)]
    for i, (fid, start) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        if not PATH_RE.search(text[start:end]):
            findings.append(
                "finding %s carries no file path; every finding must cite one (R4, AC-4)" % fid)
    return set(ids)


def check_roadmap(bundle, defined_ids, findings):
    path = os.path.join(bundle, "roadmap.md")
    if not os.path.isfile(path):
        return
    if not defined_ids:
        findings.append(
            "roadmap.md is present but findings.md defines no findings; "
            "roadmap items must cite findings (AC-9), so this roadmap cannot satisfy its contract")
    text = read(path)
    above, below, count = split_on_break(text)

    if count != 1:
        findings.append(
            "roadmap.md has %d horizontal break(s); exactly one is required, introducing the "
            "speculation section (R5, AC-10)" % count)
    if below is None:
        return  # Nothing further is checkable without a break.

    cited_above = set(FINDING_CITATION_RE.findall(above))
    for fid in sorted(cited_above):
        if fid not in defined_ids:
            findings.append(
                "roadmap.md cites %s above the break, which resolves to no '## %s' entry in "
                "findings.md (R6, AC-9)" % (fid, fid))

    # Per-ITEM, not per-file. Checking only that the citations present resolve
    # lets an item lose its citation silently while its siblings keep the file
    # passing. Found by canary 4 on 2026-09-20: deleting one item's `Traces to`
    # line left seven valid citations and the checker reported CLEAN, so the
    # gate could not fail on the AC-9 violation it exists to catch.
    items = list(ROADMAP_ITEM_RE.finditer(above))
    if not items:
        findings.append(
            "roadmap.md has no numbered items above the break; an evidenced roadmap needs at "
            "least one (R6, AC-9)")
    for i, m in enumerate(items):
        end = items[i + 1].start() if i + 1 < len(items) else len(above)
        body = above[m.start():end]
        resolvable = [f for f in FINDING_CITATION_RE.findall(body) if f in defined_ids]
        if not resolvable:
            findings.append(
                "roadmap item %r cites no finding that resolves to an entry in findings.md; every "
                "item above the break must trace to one (R6, AC-9)" % m.group(1).strip())

    cited_below = sorted(set(FINDING_CITATION_RE.findall(below)))
    if cited_below:
        findings.append(
            "roadmap.md cites %s below the break; nothing below the speculation break may trace to "
            "a finding (R7, AC-10)" % ", ".join(cited_below))


def run_all_checks(bundle):
    if not os.path.isdir(bundle):
        raise Broken("%s is not a directory; cannot check a bundle that is not there" % bundle)
    findings = []
    check_evidence(bundle, findings)
    defined = check_findings(bundle, findings)
    check_roadmap(bundle, defined, findings)
    return findings


# ---------------------------------------------------------------------------
# Self-test. Every rule is proved against a canary that must fail and an
# anti-canary that must pass. A checker with no proof that it can fail is not a
# check, and this block is what makes exit 0 mean something.
# ---------------------------------------------------------------------------

GOOD_EVIDENCE = (
    "# Evidence\n\n## Decision records consulted\n\nADR: absent.\n\n"
    "## What was read in full\n\nlibrary.json\n\n"
    "## What was sampled\n\nthe findings\n\n"
    "## What was skipped, and why\n\nnode_modules, by convention\n")
GOOD_FINDINGS = (
    "# Findings\n\n## F-01 - High: a thing\n\n**Observed evidence.** `library.json:5` says so.\n\n"
    "## F-02 - Low: another\n\n**Observed evidence.** `docs/README.md` says so.\n")
GOOD_ROADMAP = (
    "# Roadmap\n\n## 1. Do the thing\n\n**Traces to:** F-01\n**Rung:** CI check\n\n"
    "## 2. Do the other\n\n**Traces to:** F-02\n**Rung:** documented convention\n\n"
    "---\n\n# Questions this audit cannot answer\n\nNothing below traces to a finding.\n\n"
    "Is the compliance layer the product?\n")


def _write(d, name, text):
    with io.open(os.path.join(d, name), "w", encoding="utf-8") as fh:
        fh.write(text)


def _fixture(root, evidence=GOOD_EVIDENCE, findings=GOOD_FINDINGS, roadmap=GOOD_ROADMAP):
    d = tempfile.mkdtemp(dir=root)
    if evidence is not None:
        _write(d, "evidence.md", evidence)
    if findings is not None:
        _write(d, "findings.md", findings)
    if roadmap is not None:
        _write(d, "roadmap.md", roadmap)
    return d


def self_test():
    """Return a list of self-test failures. Empty means the checker is proved."""
    bad = []
    root = tempfile.mkdtemp()
    try:
        def expect(label, d, should_fail, needle=None):
            got = run_all_checks(d)
            if should_fail and not got:
                bad.append("  %s: expected a finding, got none" % label)
            elif not should_fail and got:
                bad.append("  %s: expected clean, got %r" % (label, got))
            elif should_fail and needle and not any(needle in g for g in got):
                bad.append("  %s: findings %r contain no %r" % (label, got, needle))

        # Anti-canary: a well-formed bundle must pass, or every canary below is
        # meaningless (a checker that fails everything proves nothing).
        expect("anti-canary, well-formed bundle", _fixture(root), False)

        # Anti-canary: a legitimate --appraise partial (evidence only) passes.
        expect("anti-canary, appraise-only partial",
               _fixture(root, findings=None, roadmap=None), False)

        # R1
        expect("R1 missing evidence.md", _fixture(root, evidence=None), True, "evidence.md is missing")
        # R2
        expect("R2 no coverage statement",
               _fixture(root, evidence="# Evidence\n\n## Decision records consulted\n\nnone\n"),
               True, "no coverage statement")
        # R3
        expect("R3 no decision records",
               _fixture(root, evidence=GOOD_EVIDENCE.replace(
                   "## Decision records consulted\n\nADR: absent.\n\n", "")),
               True, "decision records")
        # R4
        expect("R4 finding with no path",
               _fixture(root, findings="# F\n\n## F-01 - High: a thing\n\nNo citation here at all.\n"),
               True, "carries no file path")
        # R5
        expect("R5 two breaks",
               _fixture(root, roadmap=GOOD_ROADMAP.replace(
                   "# Questions this audit cannot answer", "---\n\n# Questions this audit cannot answer")),
               True, "horizontal break")
        # R6, both halves. The second was added after canary 4 on 2026-09-20
        # caught the first half passing a real AC-9 violation.
        expect("R6 unresolvable citation",
               _fixture(root, roadmap=GOOD_ROADMAP.replace("F-01", "F-99")),
               True, "resolves to no")
        expect("R6 item loses its citation while siblings stay valid",
               _fixture(root, roadmap=GOOD_ROADMAP.replace(
                   "## 2. Do the other\n\n**Traces to:** F-02\n", "## 2. Do the other\n\n")),
               True, "cites no finding that resolves")
        # R7
        expect("R7 citation below the break",
               _fixture(root, roadmap=GOOD_ROADMAP.replace(
                   "Is the compliance layer the product?", "Follow up on F-02 somehow.")),
               True, "below the break")

        # BROKEN, not FINDINGS: a directory that is not there.
        try:
            run_all_checks(os.path.join(root, "definitely-absent"))
            bad.append("  absent directory: expected Broken, got a normal return")
        except Broken:
            pass
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return bad


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        sys.stderr.write("usage: bundle-check.py <bundle-dir>\n")
        sys.exit(2)

    failures = self_test()
    if failures:
        sys.stderr.write("BROKEN: self-test failed; this checker cannot be trusted:\n")
        sys.stderr.write("\n".join(failures) + "\n")
        sys.exit(2)
    sys.stdout.write(
        "gate self-test: PASS (7 rules proved against 8 canaries, including both halves of R6, "
        "plus a well-formed anti-canary, a legitimate appraise-only partial, and an "
        "absent-directory BROKEN case)\n")

    try:
        findings = run_all_checks(argv[0])
    except Broken as exc:
        sys.stderr.write("BROKEN: %s\n" % exc)
        sys.exit(2)

    if findings:
        sys.stdout.write("FINDINGS: %d structural rule(s) violated in %s\n" % (len(findings), argv[0]))
        for f in findings:
            sys.stdout.write("  - %s\n" % f)
        sys.exit(1)

    sys.stdout.write("CLEAN: canary proved, %s satisfies every structural rule.\n" % argv[0])
    sys.exit(0)


if __name__ == "__main__":
    main()
