# History - plab-release-plan

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.4.0 | 2026-08-27 | unreleased | changed | Removed `disable-model-invocation`. The skill is auto-discoverable; a do-NOT-fire clause in the description replaces the binary gate. |
| 1.3.0 | 2026-08-24 | v0.3.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.3.0; prior history remains there. |


## 1.4.0 - 2026-08-27

**`disable-model-invocation` removed. This is a behavior change.**

The flag was set because "plan the release" is a common phrase. That remains true, and it is now
handled in the description rather than by a gate: explicit triggers ("create the release plan",
"promote these efforts into v0.5.0", "can we tag yet", "check release readiness") paired with an
explicit do-NOT-fire clause for general planning talk, release-notes or changelog requests, and
questions about what already shipped. Those three are the realistic false positives, and naming them
is something a boolean cannot do.

**Why now.** The flag was refusing approved invocations. It also meant the skill had never run in
this repository, so its own hygiene gates and doc-update checklist have never been exercised against
a real release, which is a worse state than an occasional misfire.

**What did not change.** `/plab-release-plan` with a subcommand still works. The five subcommands,
the six hygiene gates, the generated aggregation table, and the refusal to invent or modify
acceptance criteria are untouched.

**Note on `--gate`.** It is read-only and reports readiness. A misfire on `--gate` costs a report
nobody asked for. A misfire on `--create` or `--promote` would move folders, so those remain the ones
worth watching if the description turns out to be too broad.

## 1.3.0 - 2026-08-24

First public release. All five subcommands behave as they did privately: `--create`, `--promote`,
`--demote`, `--update`, `--gate`. The aggregation table is still generated rather than hand-edited,
and the skill still refuses to add or modify acceptance criteria. This entry records the move, not a
feature change.

**Why it moved.** `docs/internal/release-plans/` in this repository is the folder structure this
skill owns, and that folder's own README said so while naming a skill no reader could install. The
five release plans and sixteen effort folders committed there were produced against this skill's
contract. Tool and output now live together.

**Invocation is manual only, and this is a behavior change.** The skill ships with
`disable-model-invocation: true`. Privately it auto-triggered on "create release plan", "promote to
release" and "check release readiness". It no longer does. It runs when invoked as
`/plab-release-plan` with a subcommand. The always-on description budget in this plugin is paid by
one person in every session, and a release-management skill is reached for deliberately, on the
handful of days a release is actually being cut, rather than discovered mid-sentence.

**References repointed.** `/jp-spec` becomes `/plab-spec`. `/jp-implementation-plan` was retired
upstream with no successor here; the two places that named it as the producer of
`implementation-plan.md` now name `/superpowers:writing-plans`.

**Default checklist rows are unchanged.** The eight built-in doc-update rows were derived from the
private library's release contract, but they describe a conventional plugin layout and apply here
unmodified. This repository's `docs/internal/release-plans/release-checklist.yaml` already extends
them with five project-specific rows and marks one built-in (`docs/skills/README.md`, which does not
exist here) as not applicable. That is the extension mechanism working as designed, so the hardcoded
defaults were left alone; editing them would duplicate the YAML and collide with the documented
"built-in wins" merge rule. Only the prose attributing the defaults to a specific private repository
was neutralised.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo
layouts and planning folders that do not ship in this plugin.

**Example content genericised.** The worked examples in the reference files and usage docs used
effort folder names drawn from the private library's own backlog, including skills that have since
been retired. They now use neutral placeholder names, since what the examples teach is the folder
shape and the promotion ceremony, not the specific efforts.
