# History - plab-wrap-session

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.6.0 | 2026-08-24 | v0.4.0 | fixed | Detector gates that could not fail open, plus the log-format and hygiene fixes batched with them. |
| 1.5.0 | 2026-08-18 | v0.2.0 | added | `--organize` files old logs into `YYYY-MM/` folders. Hygiene sweep gained Check 5. |
| 1.4.1 | 2026-08-18 | v0.1.2 | fixed | Dropped the "what did we do" trigger. Added `type:` to the frontmatter block and `machine:` to the Quick and Blocked templates. |
| 1.4.0 | 2026-08-14 | v0.1.0 | migrated | First release in prisant-utilities. Migrated from a private upstream at version 1.4.0; prior history remains there. |

## 1.6.0 - 2026-08-24

**Fixed: the path-existence gate stopped flagging prose.** The Log Self-Check gate "Every file path
and link named in the log exists" resolved any citation as if it were a repo-relative path. In the
2026-08-23 10:27 wrap it flagged 7 of 21 citations and 6 of the 7 were false positives: bare
filenames and document titles mentioned in running prose, not claims about where a file lives.

The gate now tests what a citation actually asserts. A citation containing a path separator is a
location claim and must exist as written. A backtick-wrapped citation with no separator is resolved
against the repo root and passes silently when it does not resolve, because naming a file is not the
same as saying where it is. A bare word with a file extension and neither signal is prose and is not
evaluated at all.

A gate that cries wolf six times out of seven trains its reader to skim the output, which is how the
one real finding in that wrap nearly went unread.

**Added: both detector gates became canary-verified scripts.** The dash gate and the path-citation
gate now run `scripts/dash-check.py` and `scripts/path-citation-check.py`. Each proves its detector
against a canary corpus before scanning anything and reports clean, findings, or broken. Broken
blocks the log exactly as findings does, because a check that cannot prove it still works is not a
passing check.

This exists because the same failure happened three times in one week: a dash sweep written as a
shell escape that expanded to a literal string, a replacement sweep in Perl that read undecoded bytes
and could never match, and a path gate that produced six false positives out of seven. All three
reported success. A two-state gate cannot tell "found nothing" from "never ran".

Mechanizing the path rule also revealed that it was under-specified. Applied literally to a real log
it produced 13 flags, 11 of them false, against the pre-D-12 gate's 7 and 6: separators appear in
slash commands, repository slugs, git refs, globs, template placeholders and URLs, none of which
claim where a file lives. The script excludes all six mechanically and lands at 4 flags. See the
D-12 spec's Revisions entry for the superseded criterion.

## 1.5.0 - 2026-08-18

**Added: `--organize`.** A flat session-log store grows without bound. `--organize` files logs older
than the current and previous month into `YYYY-MM/` subdirectories, driven by
`scripts/organize-logs.py`: dry run by default, idempotent, move-only, never deleting. The month
comes from the filename prefix rather than mtime, because mtime is wrong after any copy or restore
and the filename is the log's identity. Collisions skip the file and exit non-zero rather than
overwriting. It runs instead of a wrap, so no log is written and no sweep fires.

**Added: hygiene sweep Check 5.** Deep and final wraps now report how many logs could be filed and
offer to file them under the existing per-action confirmation protocol. The sweep's read-only
detection phase is exactly the script's dry run, so one code path serves both and the check cannot
drift from the operation it proposes.

**Added: cite session logs by filename, never by path.** A directory-qualified reference to another
log breaks the moment that log is archived. The filename is stable identity, so a move needs no
rewrite step and therefore has no rewrite bugs. `resumed-from:` already worked this way; the rule now
covers prose references too.

**The write path is unchanged.** New logs are still written flat to
`_local/_session-logs/YYYY-MM-DD_HH-MM_<llm>_<title>.md`. Archiving is a separate, confirmed
operation, and nothing that documents the write path needed to change.

**Requires `plab-continue-session` 1.3.0.** The reader must understand month folders before anything
is filed into one, or the first archival makes the store read as empty. Both ship in plugin v0.2.0.

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
