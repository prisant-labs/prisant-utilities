# Log Discovery

How `/plab-continue-session` finds the right session log to resume from.

## Search locations

Search all three stores, in this order for reporting purposes only. Skip any that do not exist.

| Location | Written by | Status |
|----------|-----------|--------|
| `_local/_session-logs/` | plab-wrap-session v1.2.0+ | current |
| `_agent-context/session-log/` | plab-wrap-session v1.1.0 - v1.2.x | legacy |
| `AGENTS/session-log/` | plab-wrap-session v1.0.x | legacy |

## Store layout: flat or month folders

The current store holds logs two ways, and discovery reads both as one pooled corpus.

| Path shape | Discovered | Meaning |
|---|---|---|
| `_session-logs/*.md` | yes | hot logs; this is where every new log is written |
| `_session-logs/YYYY-MM/*.md` | yes | archived logs, filed by `/plab-wrap-session --organize` |
| `_session-logs/<anything else>/` | **no** | deliberately outside the corpus (`_capture/`) |

**Discovery is a date-shaped allowlist exactly one level deep, never a recursive walk.** A
subdirectory is visible only if its name is `YYYY-MM`. This is what lets `_capture/` sit inside the
store without polluting the corpus, and it is the mechanism any future deliberately-hidden
subdirectory relies on.

Do not "simplify" this into a recursive find with an underscore exclusion. The obvious form of that
is broken: `find "$d" -name '*.md' -not -path '*/_*/*'` matches against the entire path, and both
`_local` and `_session-logs` are themselves underscore-prefixed components, so every file is
excluded via its ancestors and discovery silently returns zero results. An allowlist can only match
what it literally describes; its failure mode is "too few results", which is visible, rather than
"silently zero", which is not.

**Legacy stores are searched flat.** They are frozen, nothing writes to them, and the organizer
never touches them.

## Selection rule: newest across the union

Pool the `.md` files from every location that exists, then pick the single newest by filename. **Do not stop at the first non-empty directory.**

This matters during migration. A project that has just moved to `_local/_session-logs/` still has its history in a legacy path, and a first-non-empty rule gets it wrong in both directions: before the first new log is written it resumes from the legacy path indefinitely, and immediately after it permanently hides everything older. Newest-wins across the union is correct at every point in the migration.

## Sort rule

Filenames follow the pattern `YYYY-MM-DD_HH-MM_<llm>_<brief-kebab-title>.md`. Because the date+time prefix is ISO-style and zero-padded, **lexical descending sort = most recent first**. The prefix is location-independent, so pooled filenames from different directories sort correctly against each other.

```bash
current=_local/_session-logs
log='[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_*.md'
for f in "$current"/$log "$current"/[0-9][0-9][0-9][0-9]-[0-9][0-9]/$log \
         _agent-context/session-log/$log AGENTS/session-log/$log; do
  [ -f "$f" ] && printf '%s\n' "$f"
done | awk -F/ '{print $NF"\t"$0}' | sort -r | head -1 | cut -f2
```

PowerShell equivalent:

```powershell
$current = '_local/_session-logs'
$stores  = @($current) + (Get-ChildItem $current -Directory -ErrorAction Ignore |
                          Where-Object Name -match '^\d{4}-\d{2}$' | ForEach-Object FullName)
$stores += '_agent-context/session-log', 'AGENTS/session-log'
Get-ChildItem ($stores | Where-Object { Test-Path $_ }) -Filter *.md -File |
  Where-Object Name -match '^\d{4}-\d{2}-\d{2}_' |
  Sort-Object Name -Descending | Select-Object -First 1 -ExpandProperty FullName
```

**Both match the date prefix, not bare `*.md`.** A store can legitimately contain other Markdown
(a `README.md` explaining the folder, scratch `notes.md`). Selecting on `*.md` would pick those:
lexical descending sort puts any lowercase name above every `2026-...` log, so a stray `notes.md`
would be resumed from as though it were the latest session. `--organize` reports such files as
"left in place", so the store is expected to hold them and discovery has to skip them.

Both sort on the **basename** so the directory prefix never affects ordering, and both return the **full path** so the winner can be read directly. Three details worth preserving if these are rewritten:

- Sorting on the full path instead of the basename would order by directory name first, which silently breaks newest-wins across locations. It is also what makes month folders safe: an archived log and a hot log order correctly against each other because only their filenames are compared.
- Both filter to entries that exist rather than suppressing errors from missing ones. In PowerShell, `-ErrorAction SilentlyContinue` hides the message but still leaves a failure exit status, so a caller checking `$?` would read a successful lookup as a failure.
- Both enumerate month directories explicitly rather than recursing. A bare `-Recurse`, or a `find` over the whole store, would pull `_capture/` and any future deliberately-hidden subdirectory into the corpus.

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

**First, check for a version-skew symptom.** Before reporting that nothing was found, look for
`YYYY-MM` subdirectories in the current store. If the top level has no `.md` files but month folders
are present, the store was organized by a newer `plab-wrap-session` than the one installed here, and
this discovery is too old to read it:

> No `.md` logs at the top level of `_local/_session-logs/`, but it contains month folders
> (`2026-06/`, `2026-07/`). This store was organized by a newer `plab-wrap-session` than the one
> installed here. Run `/plugin update`, then resume.

Reporting "no prior session log" in that state would be wrong and would invite starting fresh on top
of work that is sitting one directory down.

Otherwise, if none of the search locations exist, or all of them contain no `.md` files:

```
No prior session log found in _local/_session-logs/ (or the legacy
_agent-context/session-log/ and AGENTS/session-log/ paths).

Options:
- Start fresh: tell me what you want to work on.
- Manually point me at a log: tell me the path.
```

If `_local/_session-logs/_capture/` holds any qualifying record, surface it first; see
"Capture-lite orientation" below.

## Age warning

If the latest log's date prefix is more than 7 days old, surface an age warning before proceeding:

> **Heads up:** the latest session log is from 2026-04-15 (43 days ago). The repo state may have moved on. Confirm you want to resume from this log, or point me at a more recent one.

The 7-day threshold is a heuristic; it does not block. The user can confirm and proceed.

Also check `_local/_session-logs/_capture/` for records since this log; see "Capture-lite
orientation" below.

## Capture-lite orientation (when present)

On the no-log-found branch above, and on the age-warning path, check whether
`_local/_session-logs/_capture/` exists and its `.jsonl` files hold any record with a non-null
`session_id` newer than the relevant boundary: no existing log at all for the no-log-found case, or
the stale log's date for the age-warning case. If so, surface one line before the existing message:
the most recent qualifying record's `branch`, `head`, `commits_today`, and `ts` for the no-log case,
or the count of such records since the stale log for the age-warning case. Say nothing when the
directory is absent or nothing qualifies; the hook is optional machine-local infrastructure and this
store may not exist at all.

## Repo / branch mismatch

After reading the log's frontmatter, compare:

- `repo` field vs `git remote -v` (or current directory name as fallback)
- `branch` field vs `git branch --show-current`

If either mismatches, surface clearly before resuming:

- **Repo mismatch:** refuse to resume. Cross-repo resumption is almost always a mistake. Report both repos and ask the user to confirm they're in the right place.
- **Branch mismatch:** warn but allow. Different branch may be intentional (resuming work that was wrapped on `feature/x` but now you're on `main` reviewing). Ask before proceeding.
