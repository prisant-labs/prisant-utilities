# History - plab-wrap-session

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.4.1 | 2026-08-18 | v0.1.2 | fixed | Dropped the "what did we do" trigger. Added `type:` to the frontmatter block and `machine:` to the Quick and Blocked templates. |
| 1.4.0 | 2026-08-14 | v0.1.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.4.0; prior history remains there. |

## 1.4.1 - 2026-08-18

**Fixed: a status question was listed as a trigger.** The description fired on "what did we do", which is
a request for an answer, not a request to write a session log. This is the same over-trigger class that
`/plab-continue-session` narrowed out of its own description on 2026-08-17, so the lesson had been applied
to one half of the pair and not the other. The phrase is removed and nothing replaces it: "wrap up",
"wrap session", "end of session", "session log", "close out", and "document this session" carry the load.
The description gets shorter, so always-on context cost falls rather than rising.

Usage documentation carried the same contradiction more starkly, listing "what did we do" as a trigger at
line 46 and "what have we done so far?" as an anti-trigger at line 50. Both now agree.

**Fixed: the skill failed its own gate.** The Log Self-Check requires Tier 1 frontmatter complete in every
mode, and `references/frontmatter-schema.md` places both `type` and `machine` in Tier 1. The Quick and
Blocked templates in `references/session-log-template.md` omitted `machine:`, so an agent following either
one produced a log this skill rejects. The frontmatter block in SKILL.md omitted `type:`, which the schema
and the Final Mode template both carry. Four lines added. The schema was correct throughout; the other two
surfaces had drifted from it.

**Not changed.** The description still fires on the bare phrase "session log", which is arguably the same
over-trigger class: a mention of a session log is not a request to write one. There is no misfire evidence
for it in transcripts, so it stays and gets watched rather than guessed at.

## 1.4.0 - 2026-08-14

First public release. The skill is unchanged in behaviour from its last private version; this entry records the move, not a feature change.

**Migration provenance.** 158 recorded invocations via the Skill tool and 20 typed slash invocations in Claude Code, plus 86 Codex sessions referencing the skill, on the origin machine as of 2026-08-14. Counts come from local transcripts on one machine and are bounded by local retention. Claude Code stores no per-skill counter, so this snapshot is the only surviving record of pre-migration usage.

**Not carried over.** The prior HISTORY file is not reproduced here. It documented an internal path migration across three private-repo layouts and referenced skills that do not ship in this plugin.

**Renamed references.** `/plab-continue-session` is the read-side companion. Legacy session-log locations (`_agent-context/session-log/`, `AGENTS/session-log/`) are still recognised for backward compatibility; only the writing skill's name changed.
