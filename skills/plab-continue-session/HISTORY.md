# History - plab-continue-session

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.2.0 | 2026-08-14 | v0.1.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.2.0; prior history remains there. |

## 1.2.0 - 2026-08-14

First public release. The skill is unchanged in behaviour from its last private version; this entry records the move, not a feature change.

**Migration provenance.** 85 recorded invocations via the Skill tool and 8 typed slash invocations in Claude Code on the origin machine, as of 2026-08-14. Counts come from local transcripts on one machine and are bounded by local retention.

**Not carried over.** The prior HISTORY file is not reproduced here; it referenced private-repo layouts and skills that do not ship in this plugin.

**Pairing contract.** This skill reads what `/plab-wrap-session` writes. The two move and version together; a change to the session-log format in one requires a matching change in the other. Legacy locations (`_agent-context/session-log/`, `AGENTS/session-log/`) are still searched so projects on an older layout keep working.
