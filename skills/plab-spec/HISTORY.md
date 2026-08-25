# History - plab-spec

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.2.1 | 2026-08-24 | v0.3.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.2.1; prior history remains there. |

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
