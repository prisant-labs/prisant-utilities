# History - plab-ai-review

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.2.1 | 2026-08-14 | v0.1.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.2.1; prior history remains there. |

## 1.2.1 - 2026-08-14

First public release. The skill is unchanged in behaviour from its last private version; this entry records the move, not a feature change.

**Migration provenance.** Zero recorded invocations in Claude Code, and 153 Codex sessions referencing this skill with 102 containing a review artifact in its own naming convention, on the origin machine as of 2026-08-14. For scale, only 86 Codex sessions reference the session-wrap skill.

Both halves of that number matter. This skill exists to get a **second** model to review your work, so it runs in whichever harness is not the one that produced the document. A count scoped to a single harness reads as dormancy when the skill is in fact the most widely used of the five. Anyone using these figures to judge whether a skill earns its keep should measure every harness it can run in.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo layouts and planning folders that do not ship in this plugin.

**Bundled example.** `examples/v1.1.0-sample_reviewed-by-codex.md` is a complete worked review of a fictional API rate-limiting plan. It was read in full before publication and contains no real product, company, or person.
