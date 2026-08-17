# History - plab-ai-review

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.2.1 | 2026-08-14 | v0.1.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.2.1; prior history remains there. |

## 1.2.1 - 2026-08-14

First public release. The skill is unchanged in behaviour from its last private version; this entry records the move, not a feature change.

**Migration provenance.** Zero recorded invocations in Claude Code, and 102 Codex sessions containing a review artifact in this skill's own naming convention, on the origin machine as of 2026-08-16.

Read those two numbers together. This skill exists to get a **second** model to review your work, so it runs in whichever harness is not the one that produced the document. A count scoped to a single harness reads as dormancy when the skill is in fact the most widely used of the five.

**On measuring this skill.** Codex transcripts carry no per-skill invocation record. Every occurrence of a skill's path sits inside the startup index Codex emits listing all installed skills, so counting mentions measures installation rather than use. An earlier draft of this entry cited such a count and overstated the figure. The artifact count above is the only Codex signal that proves work was done.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo layouts and planning folders that do not ship in this plugin.

**Bundled example.** `examples/v1.1.0-sample_reviewed-by-codex.md` is a complete worked review of a fictional API rate-limiting plan. It was read in full before publication and contains no real product, company, or person.
