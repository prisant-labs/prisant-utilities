# The coverage statement

`evidence.md` is the file that makes the other four trustworthy. It exists so a reader can tell the difference between "the audit looked and found nothing" and "the audit did not look". Without it those two are indistinguishable, and an audit whose silence cannot be interpreted is not evidence of anything.

Write it from a running record kept during the audit. Do not reconstruct it afterwards. Exit codes, in particular, are gone the moment the terminal scrolls, and an exit code recalled rather than recorded is a guess.

## Required sections, in this order

### 1. Header

Repository path and name, audit date, auditor (model and mode), and one line on what this bundle is for.

### 2. Repository snapshot

A two-column table of observed values. Minimum rows: branch, HEAD and its subject, worktree cleanliness, declared version and whether the manifests agree, git tags, commit count with span and author count, branches in flight, tracked file count, and the component counts the type pack specifies.

Mark an absence as an absence rather than omitting the row. `Root AGENTS.md | absent` is a finding waiting to happen; a missing row is nothing.

### 3. Validation commands and outcomes

Every command run during the audit, with its **exit code**. Not "PASS" or "FAIL": the number.

The distinction matters because the three-state convention this repository uses everywhere reads 0 as clean, 1 as findings, and 2 as broken, and a prose "FAIL" collapses the last two. A reader cannot tell a detector that found a problem from a detector that could not run.

For each command record: the command as invoked, the exit code, and what it reported in one or two lines. Where output was surprising, quote it.

**Three things that must appear here if they happened:**

- **A tool that could not run.** Command, exit code or failure mode, and what is therefore unassessed. This is the AC-12 obligation: a missing toolchain degrades to a reported gap, never to silence and never to generic advice.
- **Your own operator errors.** A command you invoked wrongly, its exit code, the correction, and a sentence saying the first was yours. The corrected run is what licenses whatever conclusion you drew.
- **Any place a tool's human output and machine output disagreed.** A gate that prints a clean summary while holding suppressed findings is a fact about the audit's reliability, and the number withheld belongs here.

### 4. Decision records consulted

**This section is required and it is the one most likely to be skipped.** It satisfies AC-15.

A table naming each decision record read and what it settled. At minimum, say whether each of these was found, read, or absent:

| Source | Typical location |
|---|---|
| Architecture decision records | `docs/adr/`, `docs/decisions/` |
| Suppression or gate configuration | `askit.config.json`, linter overrides, reasoned exception files |
| Release notes and changelog | `RELEASE-NOTES.md`, `CHANGELOG.md` |
| Prior audits | anywhere in the tree, including gitignored `_local/` |
| Root instruction files | `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` |

"Absent" is a real and useful entry. A repository with no decision records is telling you something, and it is usually the same thing as a repository with no root instruction file.

Where a record caused a candidate to be withdrawn or narrowed, say so here as well as in `findings.md`. The two files serve different readers: this one serves someone deciding whether to trust the audit.

### 5. What was read in full

List them. Be specific enough that someone could repeat it.

### 6. What was sampled

Name the population and what was drawn from it. "The 152 findings, aggregated by check, with individual messages read for seven of eleven checks" is a sample description. "Reviewed the findings" is not.

### 7. What was skipped, and why

Every skip carries a reason. Acceptable reasons include scope, cost, risk, and irrelevance to the type. "Ran out of time" is acceptable and honest; leaving the skip out is not.

**Include tools considered and deliberately not run.** A gate belonging to a different repository, a suite that costs money, a check whose preconditions the target does not meet: each is a decision, and a decision recorded is worth more than a tool quietly not mentioned.

### 8. Limits and confidence

Group findings by confidence and say what each rests on. Separate:

- **High confidence, directly observed**, with the mechanism traced to source
- **High confidence, single measurement**, where the number is exact but its interpretation carries a caveat
- **Lower confidence, judgment rather than observation**

Then state **what would change these conclusions**: the specific further reading or execution that would add, remove or overturn findings. Name the most probable remaining source of error explicitly. An audit that cannot say how it might be wrong has not finished thinking.

Close with any bias worth declaring, including the auditor's own position relative to the repository.

### 9. Cost record

Wall clock start and end, elapsed, commands executed, context consumed, and the candidate-to-finding accounting: candidates produced, findings published, candidates withdrawn on recorded decisions.

That last triple is the number worth watching across runs. A run with zero withdrawals either audited a repository with no recorded decisions or skipped step 4.

## What this file is not

It is not a log of everything that happened. It is the answer to one question, asked by a reader who is deciding whether to act on `findings.md`: **what did this audit actually look at, and what did it not?**

Anything that does not help answer that belongs somewhere else or nowhere.
