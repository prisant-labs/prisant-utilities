# Log Discovery

How `/plab-continue-session` finds the right session log to resume from.

## Search locations

Search all three, in this order for reporting purposes only. Skip any that do not exist.

| Location | Written by | Status |
|----------|-----------|--------|
| `_local/_session-logs/` | plab-wrap-session v1.2.0+ | current |
| `_agent-context/session-log/` | plab-wrap-session v1.1.0 - v1.2.x | legacy |
| `AGENTS/session-log/` | plab-wrap-session v1.0.x | legacy |

## Selection rule: newest across the union

Pool the `.md` files from every location that exists, then pick the single newest by filename. **Do not stop at the first non-empty directory.**

This matters during migration. A project that has just moved to `_local/_session-logs/` still has its history in a legacy path, and a first-non-empty rule gets it wrong in both directions: before the first new log is written it resumes from the legacy path indefinitely, and immediately after it permanently hides everything older. Newest-wins across the union is correct at every point in the migration.

## Sort rule

Filenames follow the pattern `YYYY-MM-DD_HH-MM_<llm>_<brief-kebab-title>.md`. Because the date+time prefix is ISO-style and zero-padded, **lexical descending sort = most recent first**. The prefix is location-independent, so pooled filenames from different directories sort correctly against each other.

```bash
for d in _local/_session-logs _agent-context/session-log AGENTS/session-log; do
  [ -d "$d" ] && ls "$d"/*.md 2>/dev/null
done | awk -F/ '{print $NF"\t"$0}' | sort -r | head -1 | cut -f2
```

PowerShell equivalent:

```powershell
$dirs = '_local/_session-logs', '_agent-context/session-log', 'AGENTS/session-log' |
  Where-Object { Test-Path $_ }
Get-ChildItem $dirs -Filter *.md | Sort-Object Name -Descending |
  Select-Object -First 1 -ExpandProperty FullName
```

Both sort on the **basename** so the directory prefix never affects ordering, and both return the **full path** so the winner can be read directly. Two details worth preserving if these are rewritten:

- Sorting on the full path instead of the basename would order by directory name first, which silently breaks newest-wins across locations.
- Both filter to directories that exist rather than suppressing errors from missing ones. In PowerShell, `-ErrorAction SilentlyContinue` hides the message but still leaves a failure exit status, so a caller checking `$?` would read a successful lookup as a failure.

## Migration note

If the winning log came from a legacy path, surface this alongside the resumption context:

> **Migration note:** The most recent session log is at `<legacy path>`. Current logs are written to `_local/_session-logs/`. To consolidate, move the old files there - they leave version control (`_local/` is gitignored), and git history retains every committed version.

Do not move anything automatically. The choice is the user's.

## Tie-breaking

If two logs share the same `YYYY-MM-DD_HH-MM_` prefix (different LLMs ran a session at the exact same minute, rare but possible), surface both to the user and ask which to resume:

```
Two logs share the most-recent timestamp:
  1. 2026-05-28_14-30_claude_<title>.md
  2. 2026-05-28_14-30_codex_<title>.md
Which session should I resume?
```

Do not silently pick one. The choice is the user's.

## Empty or missing directory

If none of the search locations exist, or all of them contain no `.md` files:

```
No prior session log found in _local/_session-logs/ (or the legacy
_agent-context/session-log/ and AGENTS/session-log/ paths).

Options:
- Start fresh: tell me what you want to work on.
- Manually point me at a log: tell me the path.
```

## Age warning

If the latest log's date prefix is more than 7 days old, surface an age warning before proceeding:

> **Heads up:** the latest session log is from 2026-04-15 (43 days ago). The repo state may have moved on. Confirm you want to resume from this log, or point me at a more recent one.

The 7-day threshold is a heuristic; it does not block. The user can confirm and proceed.

## Repo / branch mismatch

After reading the log's frontmatter, compare:

- `repo` field vs `git remote -v` (or current directory name as fallback)
- `branch` field vs `git branch --show-current`

If either mismatches, surface clearly before resuming:

- **Repo mismatch:** refuse to resume. Cross-repo resumption is almost always a mistake. Report both repos and ask the user to confirm they're in the right place.
- **Branch mismatch:** warn but allow. Different branch may be intentional (resuming work that was wrapped on `feature/x` but now you're on `main` reviewing). Ask before proceeding.
