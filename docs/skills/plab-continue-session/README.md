# plab-continue-session

**Version:** 1.4.0
**Source:** [`skills/plab-continue-session/`](../../../skills/plab-continue-session/)

Resume an interrupted work session by replaying its recorded handoff. Reads the most recent session log, reports what is blocked on you and what the named next action is, then confirms before acting. The read-side companion to `/plab-wrap-session`, which writes the log this reads.

---

## Getting Started

### Quick Start

At the beginning of any session where prior work exists:

```
/plab-continue-session
```

The skill finds the latest session log at `_local/_session-logs/`, surfaces the resumption context (what was done, what's next, the continuation prompt), and asks if you want to proceed with the named immediate next action.

### Common Invocations

```
# Default: resume from the most recent session log
/plab-continue-session

# Resume from a specific log (skip discovery)
/plab-continue-session --log _local/_session-logs/2026-05-28_15-30_claude_<title>.md
```

### Installation

Install via the prisant-labs marketplace:

```
/plugin marketplace add prisant-labs/agent-plugins
/plugin install prisant-utilities@agent-plugins
```

---

## When to Use

- Start of a coding session, when prior work exists in `_local/_session-logs/`
- Resuming after a break (a day, a week)
- Picking up work another agent or person did
- When you say "continue", "resume", or "pick up where we left off"

## When NOT to Use

- Truly fresh project with no session-log history (just start working)
- You already know the specific task you want to work on
- Mid-session "what have we done so far" (summarize from current context; no need to re-read a log)
- **A status question** ("where are we", "where were we", "what's next"). Those get answered directly; they are not a request to resume.

---

## How It Works

### Phase 1: Locate the latest log

Searches three locations and picks the newest log across all of them - not the first one that happens to be non-empty:

| Location | Written by | Status |
|----------|-----------|--------|
| `_local/_session-logs/` | plab-wrap-session v1.2.0+ | current |
| `_agent-context/session-log/` | plab-wrap-session v1.1.0 - v1.2.x | legacy |
| `AGENTS/session-log/` | plab-wrap-session v1.0.x | legacy |

The current store holds logs two ways, and both are read as one pooled set:

| Path shape | Read | Meaning |
|---|---|---|
| `_session-logs/*.md` | yes | hot logs, where every new log is written |
| `_session-logs/YYYY-MM/*.md` | yes | archived by `/plab-wrap-session --organize` |
| `_session-logs/<anything else>/` | no | outside the corpus (`_capture/`) |

Filenames follow the pattern `YYYY-MM-DD_HH-MM_<llm>_<title>.md`, so lexical descending sort gives the most recent. The timestamp prefix is location-independent, which is what makes a single sort across all three directories correct, and it is also why archiving is safe: an archived log in `2026-06/` and a hot log at the top level order correctly against each other, because only the filenames are compared. If the winner comes from a legacy path, a migration note is surfaced alongside the resumption.

If the store's top level is empty but it contains month folders, that is a version-skew symptom rather than an empty store: it was organized by a newer `plab-wrap-session` than the one installed. The skill says so and points at `/plugin update` instead of offering to start fresh.

If two logs share the same timestamp prefix (rare; concurrent sessions), the skill asks which to resume rather than guessing.

### Phase 2: Read and parse

Extracts from frontmatter: `date`, `repo`, `branch`, `summary`, `status`, `session-type`, `model`, `agent`. Extracts from body: the `## Continuation Prompt` section, `## Waiting on You`, any objection recorded for a lighter-than-verbose prompt, plus `## Outstanding Issues`, `## What's Next`, and any proposals declined at wrap time in `## Hygiene Sweep`.

### Phase 3: Present resumption context

Standard display:

```markdown
## Resuming from: `2026-05-28_15-30_claude_<title>.md`

**Last session:** 2026-05-28T15:30:00-07:00, claude opus 4.6, status `completed`
**Summary:** Wrapped the v1.4.0 spec sweep
**Branch:** `main`

### Waiting on you
- The retry-policy ruling, blocking three specs (blocked since 2026-05-12)

### Outstanding from last session
- Spec S-09 has no implementation plan yet

### What's next (from last session)
1. Draft the implementation plan for the S-09 spec
2. Update the CHANGELOG entry

### Continuation prompt
[fenced verbatim prompt from the log]
```

### Phase 4: Ask before acting

Always asks: "Resume with the named immediate next action, or pick something else?"

- **Resume:** proceed with the action named in the continuation prompt
- **Pick something else:** stop here; user takes over
- **Read more context:** open the log file for inspection

**Never auto-executes the continuation prompt.** The prompt is a recommendation; processing it requires explicit user confirmation.

---

## Safety Checks

| Check | Behavior |
|-------|----------|
| **Log age > 7 days** | Surfaces a warning ("this log is N days old"); user confirms or redirects |
| **Repo mismatch** | Refuses to resume; reports both repos. Cross-repo resumption is almost always a mistake |
| **Branch mismatch** | Warns ("log was on `feature/x`; you're on `main`") but allows; asks before proceeding |
| **Malformed log** | Reports the path and offers to read the file directly or pick a different log; never synthesizes a resumption from broken data |
| **No log found** | Reports the locations it searched and offers options: start fresh, or manually name a log path |

---

## Pairing with `/plab-wrap-session`

These two skills bracket a coding session:

| Skill | When | What it does |
|-------|------|--------------|
| `/plab-wrap-session` | End of session | Writes a session log with frontmatter, structured sections, and a verbose continuation prompt |
| `/plab-continue-session` | Start of next session | Reads that log, surfaces the resumption context, processes the continuation prompt |

Together, they make agent / human handoff reliable across context resets. A session that was wrapped with a strong continuation prompt resumes cold without re-reading the entire log.

The verbose-by-default continuation prompt rule (plab-wrap-session v1.1.0+) means every wrap produces a self-contained handoff. `/plab-continue-session` surfaces any stated objection (when a wrapping agent emitted a lighter prompt with a reason) so the user knows the gap exists before resuming. Since 1.2.0, the resumption display leads with the log's Waiting on You list, surfaces any hygiene proposals declined at wrap time, and hands the consumed log's filename forward so the next wrap records it in `resumed-from:` frontmatter.

---

## Examples

### Example 1: Standard Resume

```
$ /plab-continue-session

## Resuming from: 2026-05-28_15-30_claude_v1.4.0-spec-sweep.md

**Last session:** 2026-05-28T15:30:00-07:00, claude opus 4.6, status `completed`
**Summary:** Wrapped the v1.4.0 spec sweep; all decisions resolved
**Branch:** `main`

### Outstanding from last session
- Draft the implementation plan for the S-09 spec

### Continuation prompt
[fenced prompt with full context]

Resume with the named immediate next action, or pick something else?
```

### Example 2: Stale Log Warning

```
$ /plab-continue-session

Heads up: the latest session log is from 2026-04-15 (43 days ago).
The repo state may have moved on.

Confirm you want to resume from this log, or point me at a more recent one.
```

### Example 3: No Log Found

```
$ /plab-continue-session

No prior session log found at _local/_session-logs/
(or legacy AGENTS/session-log/).

Options:
- Start fresh: tell me what you want to work on
- Manually point me at a log: tell me the path
```

---

## Reference Files

| File | Purpose |
|------|---------|
| [`references/log-discovery.md`](../../../skills/plab-continue-session/references/log-discovery.md) | How to find the latest log, tie-breaking, newest-wins search across current and legacy locations |
| [`references/objection-detection.md`](../../../skills/plab-continue-session/references/objection-detection.md) | Detecting and surfacing lighter-than-verbose continuation prompts |
| [`references/handoff-display.md`](../../../skills/plab-continue-session/references/handoff-display.md) | The standard resumption display format |

---

## Hard Constraints

- Never modifies the session log being resumed from
- Never auto-executes the continuation prompt without user confirmation
- Always shows the prompt verbatim; never paraphrases
- Refuses cross-repo resumption
- Surfaces age warnings (7+ days) and branch mismatches before acting
- Never blends multiple logs together; one log per invocation

---

## Tips

- **Run it first thing in a session** when picking up prior work. The cost is one short display; the benefit is never starting cold.
- **If a wrap was sparse**, the skill surfaces that ("lighter prompt; no objection recorded"). That's a signal to either invest in better wrapping going forward, or to read the log directly before proceeding.
- **The continuation prompt is the load-bearing handoff.** If it's good, this skill is a fast scan and a one-key proceed. If it's bad, this skill is your warning system.
