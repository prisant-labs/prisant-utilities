# Lens: docs

**Invoked by:** `--lens=docs`. Off by default.

A lens narrows an audit rather than adding a mode. With this lens the findings file is about documentation and the appraisal says so.

## What this lens audits

### 1. Absence

What is not written that should be.

- **A root instruction file for agents.** `AGENTS.md`, and the `CLAUDE.md` that bridges to it. This is the highest-value absence in this corpus and the one most often missing: a repository can carry thirteen decision records and still have no front door pointing at them.
- **An onboarding path.** Can someone go from clone to running without asking a person. Follow it literally and note the first step that is not true.
- **A reference page per public surface.** Every skill, agent, command, CLI or exported API that a user can invoke. Count the surfaces, count the pages, name the difference.
- **A recorded decision for anything surprising.** Where the audit had to recover a convention by reading source, ask whether it is written anywhere. The trace from a non-obvious behaviour back to its written justification is the measurement, and the number of hops is the finding.

### 2. Staleness of substance

Not whether a document is old. Whether what it says is still true.

- **Standards claimed against standards in force.** A document naming an authority, a threshold or a schema that has since moved.
- **Promises a file makes about itself.** A file saying "modifications will be recorded here" with no modifications recorded, or "this list is generated" for a list maintained by hand. These are the highest-yield staleness findings because the file states its own contract and the violation is checkable without external knowledge.
- **Tense contradictions.** The same change described as scheduled in one entry and shipped in another. Look hardest inside a single unreleased section, where no release boundary has forced a reconciliation.
- **Examples that no longer run.** Commands, paths and outputs in documentation, tested against the current tree.
- **Citations that do not resolve.** Identifiers, row numbers and file references pointing at something the reader cannot reach. A tracked file citing a gitignored one is the specific case worth calling out, because it is unresolvable by construction rather than by accident.

### 3. Readability, judged differently by audience

**Human-facing documents** are judged on structure and wording: does it open with what the reader needs, is the ordering usable, can a paragraph be found by scanning.

**Agent-facing documents** are judged on token economy and load-bearing accuracy: is every line carrying weight, is anything stated twice, and is anything ambiguous in a way that would let an agent do the wrong thing confidently. Length is a cost here in a way it is not for human documents.

**Do not apply the wrong standard.** A 35,000-byte README written for end users is not a defect. The same length in a file loaded into every session is.

### 4. Release discipline, as documented

Whether the repository says how it releases, and whether that description matches what the tags and workflows do. An untagged repository that states its pre-release posture is in good order; one that does not is a finding, and it is a documentation finding rather than a release finding.

## What this lens explicitly excludes

**Version parity and drift.** Whether a version number in a document matches the manifest is owned by `plab-wrap-session`'s hygiene sweep and by the repository's deterministic gates. It is not audited here.

This boundary is a standing decision and it has a rule attached: **if this lens keeps finding drift the gates missed, fix the gates rather than widening the lens.** A lens that grows to cover what a deterministic check should have caught converts a mechanical guarantee into a model's attention, which is the wrong direction on the mechanization ladder.

Also excluded, and owned elsewhere:

- **Conformance grading.** `check.mjs` does this model-free, which is strictly better.
- **Prose style and voice.** Not an audit concern unless a stated house rule is being violated, in which case it is a staleness finding about the rule.
- **Spelling and grammar.** Not worth a model's attention at audit cost.

## Judgment questions

1. **What did this audit have to learn the hard way?** Every convention recovered by reading source is a candidate documentation finding, and the audit's own difficulty is the evidence.
2. **If the maintainer vanished, what would be unrecoverable?** Not lost, but unrecoverable: reasoning that exists only in their head or in a gitignored file.
3. **Does any document promise something about itself that it does not deliver?** These are the cheapest findings to verify and the most embarrassing to leave.
4. **Is the reasoning written down near where the question gets asked?** Excellent reasoning in a file nobody opens is a recording failure, not a thinking failure, and the remedy is a pointer rather than a rewrite.

## Reporting under this lens

Findings carry the same shape as any other. Two additions:

- **Name the audience** each finding concerns: human, agent, or both. The remedy differs.
- **Where the audit itself is the evidence, say so.** "This audit spent four detours recovering conventions that a root instruction file would have carried" is a stronger argument for writing that file than any general claim about documentation quality.
