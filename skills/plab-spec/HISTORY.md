# History - plab-spec

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.3.1 | 2026-08-28 | v0.5.1 | changed | `linked-effort` documented as a string, not a path. A tracked artifact must not cite an untracked one. |
| 1.3.0 | 2026-08-27 | unreleased | changed | Removed `disable-model-invocation`. The skill is auto-discoverable; a do-NOT-fire clause in the description replaces the binary gate. |
| 1.2.1 | 2026-08-24 | v0.3.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.2.1; prior history remains there. |



## 1.3.1 - 2026-08-28

**Documentation only. No behavior change.**

`references/frontmatter-schema.md` previously typed `linked-effort` as a path and gave a tracked path as its only example. In practice every spec in this repository set it to a file under gitignored `_local/`, which meant 16 tracked artifacts each carried a link that resolved for nobody who cloned the repository, and for the author only on one machine.

The field is now typed as a string, and the schema states the rule that was previously only implicit: **a tracked artifact must not cite an untracked one.** When the source is private, name it descriptively and summarize its substance into the spec's own Sources and Evidence section, which is the convention Kubernetes KEPs, Rust RFCs and Python PEPs all share.

This is a patch rather than a minor because no skill behavior changes: `plab-spec` never validated the field's contents, and specs written before this entry remain valid.

## 1.3.0 - 2026-08-27

**`disable-model-invocation` removed. This is a behavior change and it reverses a decision made at
1.2.1.**

The 1.2.1 entry below justified the flag on the grounds that "superpowers owns the default
spec-writing triggers on the maintainer's machine, and a second skill competing for the same phrases
would fire unpredictably." **That justification does not survive inspection.** The installed
superpowers plugin ships seventeen skills and none of them is a spec skill; "Spec" is a phase inside
`brainstorming`, not a separate trigger surface. The real overlap is with `brainstorming` alone, and
it is narrower than the original reasoning assumed.

**What replaces the flag.** The description now carries explicit trigger phrases ("write the spec",
"spec this effort", "turn this into acceptance criteria") and an explicit do-NOT-fire clause naming
the three ways the word "spec" appears without being a request: a passing mention, a question about
an existing spec, and a request to implement one. This is the instrument that took
`plab-continue-session` from over-triggering to firing correctly, and it is strictly more
expressive than a boolean, because it can distinguish a request from a mention where a flag cannot.

**Why the change was made.** The flag has a measured cost. On 2026-08-27 an agent was asked to run
this skill, the action was approved by the maintainer, and the invocation was still refused, twice
in one session. A guard that blocks an approved action is paying a real price to prevent a
hypothetical one. The skill had also never run in this repository, so the misfire risk the flag
guarded against was never observed.

**What did not change.** Typing `/plab-spec` still works and is still the precise way to invoke it.
The skill body, the eleven mandatory sections, the frontmatter contract, and the refusal to invent
acceptance criteria are all untouched. `plab-init-project` keeps its flag: it writes into a
repository root and its triggers ("init", "set up") are genuinely ambiguous.

**The honest risk.** This is a bet that a narrowed description fires correctly, and it is not yet
tested. If `plab-spec` starts firing on conversation about specs rather than requests to write one,
narrow the description further; do not restore the flag without first trying that.

## 1.2.1 - 2026-08-24

First public release. The skill's behavior is unchanged from its last private version: the same
eleven mandatory sections, the same frontmatter contract, the same refusal to invent acceptance
criteria. This entry records the move and the reference repointing it required, not a feature
change.

**Why it moved.** This repository already contains the artifact this skill produces. The sixteen
effort folders under `docs/internal/release-plans/` were authored to this skill's spec format while
the skill itself lived in a private plugin, so a reader of the public repo could see the output and
not the tool. The move closes that gap.

**Invocation is manual only.** The skill ships with `disable-model-invocation: true`. It does not
auto-trigger on "write a spec" or "create spec"; it runs when invoked as `/plab-spec`. This is
deliberate. `superpowers` owns the default spec-writing triggers on the maintainer's machine, and a
second skill competing for the same phrases would fire unpredictably. The private version already
carried this flag and it is preserved here rather than introduced.

**References repointed.** The skill previously positioned itself against siblings in the private
library. Those references now name what actually exists:

- `/jp-implementation-plan` was retired upstream with no successor in this plugin. Every reference
  now names `/superpowers:writing-plans`, which produces the `implementation-plan.md` this skill's
  specs sit beside.
- `/jp-skill-builder` was retired upstream. The one routing reference now names `/skill-creator`.
- `/jp-strategy-brief`, `/jp-ai-review` and `/jp-release-plan` now name their `plab-` twins in this
  plugin.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo
layouts and planning folders that do not ship in this plugin. `CREATION_NOTES.md` is also dropped:
it was a build diary from the private library recording friction points from skills that no longer
exist, and no skill in this plugin ships one.

**Example content genericised.** The bundled examples cited a private repository's GitHub issues as
sample source citations. The citation *form* is what the examples teach, so the URLs were replaced
with neutral placeholders rather than repointed at another real repository.
