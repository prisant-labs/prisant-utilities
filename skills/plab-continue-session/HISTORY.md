# History - plab-continue-session

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.2.1 | 2026-08-18 | v0.1.2 | fixed | Body trigger list aligned with the narrowed description. Records the 2026-08-17 description change that shipped un-versioned. |
| 1.2.0 | 2026-08-14 | v0.1.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.2.0; prior history remains there. |

## 1.2.1 - 2026-08-18

**Fixed: the body contradicted the description.** The When to Use list still named "where were we" and
"what were we doing" as triggers, eighteen lines below a description that explicitly refuses to fire on
status questions. The description is the router and the body is the program. Narrowing only the router
reduced the frequency of a mis-fire without removing it, because once the skill loaded, its own
instructions authorised the resumption ritual anyway. The list now names explicit resume intent only, and
When NOT to Use carries the status-question case as a named entry rather than leaving it implied.

**Erratum: 1.2.0 shipped a behaviour change undocumented.** Commit `38a75f0` (2026-08-17) rewrote this
skill's description, narrowing it to explicit resume intent and adding the do-not-fire clause. Transcript
evidence had shown every sampled invocation following a status question rather than a request to resume.
That change shipped inside plugin v0.1.1 with no version bump and no history entry, which means the 1.2.0
entry below, stating the skill was unchanged in behaviour from its last private version, was true when
written and false by the time v0.1.1 was tagged. This entry records the change retroactively rather than
amending the record.

The gap that allowed it sits on the writing side: `plab-wrap-session`'s pre-wrap hygiene sweep checks
documentation drift in one direction only, catching a version bump with a stale doc but not content
changed with no version bump. Closing that is scheduled, not shipped.

**Also corrected.** `docs/skills/plab-continue-session/README.md` still opened with the pre-narrowing
description, two rewrites stale, and pointed readers three times at `/jp-init-project`, which does not
ship in this plugin. Its Phase 2 field list had also not been updated for the Waiting on You and Hygiene
Sweep extraction that 1.2.0 added.

## 1.2.0 - 2026-08-14

First public release. The skill is unchanged in behaviour from its last private version; this entry records the move, not a feature change.

**Migration provenance.** 85 recorded invocations via the Skill tool and 8 typed slash invocations in Claude Code on the origin machine, as of 2026-08-14. Counts come from local transcripts on one machine and are bounded by local retention.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo layouts and skills that do not ship in this plugin.

**Pairing contract.** This skill reads what `/plab-wrap-session` writes. The two move and version together; a change to the session-log format in one requires a matching change in the other. Legacy locations (`_agent-context/session-log/`, `AGENTS/session-log/`) are still searched so projects on an older layout keep working.
