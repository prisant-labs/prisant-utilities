# The output bundle

Five files. Each answers exactly one question, and they are separate so that one can be read without the others.

| File | The question it answers |
|---|---|
| `README.md` | Should I care? |
| `appraise.md` | What is this and is it healthy? |
| `findings.md` | What is wrong? |
| `roadmap.md` | What do I do about it? |
| `evidence.md` | Can I trust this? |

`evidence.md` has its own reference, `coverage-statement.md`. The other four are defined here.

## `README.md`

Index and verdict. The only file that assumes the reader has read nothing else.

**Required:**

1. **Header block.** Repository path, audit date, branch and HEAD, detected type and what detected it, mode, auditor.
2. **The bundle table.** The five files and what each holds, so a reader can jump.
3. **Executive verdict.** Prose, not bullets. Lead with the single most important thing, state it as a claim, and support it. If the headline is that the repository is healthier than its tooling suggests, say that first and give the numbers.
4. **Recommended sequencing.** Which roadmap items to take first and roughly what they cost. Name anything that should explicitly not be displaced.
5. **What this audit did not do.** Named, not left to inference. A short version of the coverage statement's skips, plus any operator error.

**The verdict is a judgment and must read like one.** A verdict that hedges every clause is a summary, and the reader already has four other files if they want a summary.

## `appraise.md`

What the repository is and is worth. Six required sections.

1. **What this is.** Written for someone who has not seen it. Name the architecture's organising idea, not just its parts.
2. **Current status.** A table: version, last release, last commit, open pull requests, branches in flight, worktree state, and the conformance position. Where something was not checked, say `not queried` rather than leaving it out.
3. **Recent history.** The last few releases, or, where there are none, whatever unit the repository actually organises work into. Say which unit you used and why.
4. **What it is good at.** Specific and cited. "Good test coverage" is not a finding of strength; "the gate and the CLI call the identical engine functions, so they cannot compute different answers" is.
5. **What the repository declares as next.** From its own planning artifacts, each citation named. If the declaration is only in a gitignored file, say so.
6. **Declared plans against observed state.** The comparison, item by item. **Agreements are reported as plainly as disagreements**, because "the declared state and the actual state match" is a real result and its absence from a report is not evidence of anything.

A stalled branch named in a current release plan is the canonical disagreement this section exists to catch. So is a changelog describing the same change as both scheduled and shipped.

## `findings.md`

Two parts: what was published, and what was withdrawn.

### Published findings

Ordered by impact on the maintainer, not by ease of fix. Each finding uses a stable identifier `F-NN` so roadmap items can cite it.

```markdown
## F-01 - <Severity>: <one-line claim>

**Observed evidence.** File paths, line numbers where line-scoped, quoted output where it matters.

**Why it matters.** The consequence, to this maintainer, of leaving it alone.

**Likely cause.** Optional. Include it when it changes the remedy.

**Recommended remedy.** What to do, and the mechanization rung it should end at.
```

Severity is `Critical`, `High`, `Medium`, `Low` or `Informational`, and it describes consequence rather than effort.

**Every finding carries a file path.** A finding scoped to a line carries the line. A finding about a tool rather than the audited repository cites the tool's file and says explicitly that its citation points outside the repository under audit.

**Where a tool's stated consequence was tested and turned out to be wrong, that goes inside the finding**, not in a footnote and not silently dropped. The difference between "the tool said so" and "I checked" is most of what an audit is for.

**Where a finding was checked against a prior audit or a decision record and survived, say so.** A finding that survived reconciliation is stronger than one that was never tested, and the reader cannot tell them apart unless you say.

### Candidate findings withdrawn on evidence

A table, always present, with a line explaining why it is there.

| Column | Contents |
|---|---|
| Candidate | The finding as it would have been published |
| Why it was withdrawn | The specific thing that refuted or pre-empted it |
| Where the answer was | The file, with a path |

Close the section with where those answers lived and what that implies. If none of them was reachable from the repository root, that is itself a finding and belongs above.

**If nothing was withdrawn, write "Nothing was withdrawn" and say what was reconciled against.** An absent section and a skipped step look identical.

## `roadmap.md`

Ranked actions above a labelled break, speculation below it.

### Above the break

Each item:

- Is numbered by rank, not by finding order
- Carries a **Traces to:** line naming the finding identifier, which must resolve to a real entry in `findings.md`
- Carries a **Rung:** line naming one of: CI check, committed script, documented convention, remembered practice
- Explains in prose why it sits where it does in the ranking

Rank by `calibration.md`. Say early, in one or two sentences, what shape the list has: whether the items are one problem at several boundaries, whether the whole list is cheap, whether one item unblocks the rest. A ranked list with no stated shape makes the reader derive it.

**An item whose honest recommendation is "do nothing" is still an item.** Write it, trace it, and say why nothing is the right answer. Deleting it loses the measurement.

### The break

Exactly one horizontal rule in the entire file, immediately before the speculation heading. Use `---` on its own line and nowhere else in the document.

The heading names the section as questions the audit cannot answer. The paragraph under it states, in plain words, that **nothing below traces to a finding** and that these are the auditor's own generative questions rather than recommendations.

### Below the break

Open questions, each a short prose block. **No item below the break carries a finding citation**, and no item above it lacks one; those two rules are what the break means and `bundle-check.py` enforces both.

Point onward rather than down: where a question deserves pursuit, the next step is a strategy brief, not an implementation plan.

## Cross-file rules

- **Nothing is asserted in two files.** `README.md` summarises and cites; it does not restate a finding's evidence.
- **Identifiers are stable within a bundle.** `F-03` means the same thing in all five files.
- **Every file states its audit date and the commit audited**, because a bundle outlives the state it describes.
- **No em-dashes and no en-dashes.** Use " - " or restructure.
- **Do not hard-wrap prose.** One paragraph is one line. Tables, code blocks and frontmatter keep their natural structure.
