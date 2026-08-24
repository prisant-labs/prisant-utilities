# History - plab-init-project

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.3.0 | 2026-08-24 | unreleased | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.3.0; prior history remains there. |

## 1.3.0 - 2026-08-24

First public release. The three profiles (`minimal`, `standard`, `public`), the seeded files, and
the non-destructive reconciliation behavior are unchanged from the last private version. The skill
is still idempotent and still safe to run against an existing repository. This entry records the
move, not a feature change.

**Why it moved.** The skill scaffolds `_local/_session-logs/` and writes AGENTS.md guidance that
names the session-wrap pair. Both of those already ship in this plugin as `plab-wrap-session` and
`plab-continue-session`. Initialising a project and then closing sessions in it is one workflow, and
it was split across a public plugin and a private one.

**Invocation is manual only, and this is a behavior change.** The skill ships with
`disable-model-invocation: true`. Privately it auto-triggered on "init", "initialize", "set up
project" and "scaffold". It no longer does. It runs when invoked as `/plab-init-project`. Those
trigger words are among the most common in ordinary conversation about a repository, and a skill
that writes files into a project root should not fire on an ambiguous match. Project initialisation
happens once per repository; it does not need to be discoverable mid-sentence.

**References repointed.** The AGENTS.md and CLAUDE.md seed templates named `jp-wrap-session` and
`jp-continue-session`. They now name `plab-wrap-session` and `plab-continue-session`, which are the
skills a reader of a newly initialised project can actually install. Those references were dangling
for anyone outside the maintainer's machine; the move fixes them.

**Decision-record provenance line.** Generated MADR records recorded that they were created by the
`jp-library init-project` skill. They now name `prisant-utilities plab-init-project`, so the
provenance line in someone's committed decision record points at an installable plugin.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo
layouts, an `_LOCAL/` scratch convention this plugin does not use, and a retired `_jp-library/`
output namespace.
