---
name: plab-wrap-session
description: "Document and close agentic coding sessions with structured session logs.
  Use at the end of any coding session, when wrapping up work, when switching tasks,
  or when blocked. Defaults to a deep log with a verbose copy-paste-ready continuation
  prompt, runs a pre-wrap hygiene sweep (remote divergence, release state, doc drift,
  working-tree reconciliation with per-action confirmation), and always lists what it
  is waiting on from the maintainer with links. Triggers on 'wrap up', 'wrap session',
  'end of session', 'session log', 'close out', or 'document this
  session'. Also use when the session is blocked and needs to capture blocker details
  for the next session."
argument-hint: "[mode: quick|final|deep|blocked]"
license: MIT
metadata:
  version: "1.4.1"
  updated: 2026-08-18
---

# Wrap Session

Leave the project in a legible, resumable, evidence-backed state.

## Mode Selection

**Deep is the default.** Every wrap produces the deep template unless the agent records a specific objection in the log justifying a lighter mode (comply-or-explain, the same contract as the continuation prompt's verbosity rule). The user can always override in either direction.

| Mode | When | What to Include |
|------|------|-----------------|
| **deep** | Default for every session | Full template + evidence index + verification detail + hygiene sweep |
| **final** | Downgrade with stated objection: mid-length, low-risk, nothing autonomous | Full template below |
| **quick** | Downgrade with stated objection: < 30 min, < 3 files, trivial fix | Frontmatter + summary + files + waiting-on + continuation prompt |
| **blocked** | Session ended by unresolved blocker | Frontmatter + summary + blocker detail + waiting-on + continuation prompt |

Valid downgrade objections mirror the verbosity rule: "trivial typo fix, clean tree, nothing pending from the maintainer" or "user asked for a quick wrap". Without a recorded objection, wrap deep.

## Evidence Gathering

Before writing the log, gather facts:

1. Run `git status` and `git diff --stat` to ground file changes in reality
2. Count decisions made during the session
3. Identify what was verified vs. assumed - never conflate "completed" with "tested"
4. Check for blockers, outstanding issues, and risks introduced
5. Inventory work products in gitignored locations (`_local/` and kin) - git-derived file lists cannot see them
6. List skills invoked this session and any multi-agent workflow runs (run IDs, agent counts, token totals) for the frontmatter and Evidence Index

If git is unavailable, note that and proceed with session context only.

## Pre-Wrap Hygiene Sweep (deep and final modes)

Run before writing the log; record findings in the log's Hygiene Sweep section. Check catalog, commands, and the confirmation protocol live in `references/hygiene-sweep.md`.

1. **Remote reconciliation.** `git fetch origin`, then compare: local branch vs its remote (ahead/behind), remote tags vs local, other remote branches. Parallel work from another checkout must surface at wrap time, not at the next release.
2. **Working-tree and worktree state.** Uncommitted changes, untracked files, stashes, `git worktree list`, unpushed commits.
3. **Release and repo hygiene.** Un-released CHANGELOG content, version fields vs the latest tag, and the repo's own CI validation scripts run locally when it has them (report results; never fix silently).
4. **Documentation drift.** User or technical docs this session made stale: version tables, skill or feature READMEs vs source of truth, missing CHANGELOG entries.

**Resolution protocol: propose, then per-action confirmation.** For each finding, propose one concrete action (commit these files with this message, push, prune this worktree, apply this doc update) and execute only what the user approves, action by action. Declined or unanswered proposals are recorded in the log and carried into the continuation prompt. The sweep itself changes nothing; only confirmed actions do.

In quick and blocked modes, run only check 2 and note the skips.

## Session Log Output

Write to: `_local/_session-logs/YYYY-MM-DD_HH-MM_<llm>_<brief-kebab-title>.md`

- `<llm>` is the short LLM name: `claude`, `codex`, `gpt`, `gemini`, `grok`, `mistral`
- Example: `_local/_session-logs/2026-05-28_15-30_claude_deploy-ai-review.md`
- All agents write to the same directory - chronological project timeline
- Create the directory if it doesn't exist
- Session logs are machine-local by design. `_local/` is gitignored, so logs stay out of version control and out of the repo's public surface

**Always write to the current path**, even when a legacy directory exists. Do not write to a legacy path and do not move existing logs automatically. If either legacy directory contains logs, add one migration note after writing:

| Legacy path | Written by |
|-------------|-----------|
| `_agent-context/session-log/` | plab-wrap-session v1.1.0 - v1.2.x |
| `AGENTS/session-log/` | plab-wrap-session v1.0.x |

> **Migration note:** This project has session logs at `<legacy path>`. New logs are written to `_local/_session-logs/`. `/plab-continue-session` reads both, so nothing is lost. To consolidate, move the old files into `_local/_session-logs/` (they leave version control; git history retains them).

### Frontmatter

Include all Tier 1 fields. Add Tier 2 and Tier 3 when available. See `references/frontmatter-schema.md` for the complete field reference.

```yaml
---
date: # ISO 8601 datetime
type: # always session-log
machine: # hostname - which checkout wrote this log; logs are machine-local and cannot cross checkouts
repo: # from git remote
branch: # from git branch
summary: # max 120 chars, human-scannable
files-changed: # list from git diff --name-only
session-type: # bugfix|feature|refactor|research|planning|review|docs|autonomous|exploration
model: # full model name, e.g. "claude opus 4.6"
model-settings: # key settings, e.g. "extended-thinking max"
agent: # claude-code|codex-cli|other
status: # completed|interrupted|blocked
decisions-count: # integer
skills-used: # skills invoked this session, e.g. [plab-guide, plab-ai-review] - feeds usage telemetry
resumed-from: # filename of the session log this session resumed from, if any - measures log consumption
---
```

### Body Sections (Final Mode)

**Summary** - 2-4 sentences. What happened and why it matters.

**Work Completed** - Bulleted list of what was accomplished.

**Decisions Made** - Each decision with rationale. Scale verbosity to significance:
- Minor: one-liner ("Chose MIT license - standard for personal repos")
- Significant: 2-3 sentences with reasoning
- Architectural: full alternatives-considered analysis

**Files Changed** - List from git, grouped by purpose if many.

**Gitignored Outputs** - Work products in gitignored locations, path plus a one-liner each. Without this section, `_local/` work is undiscoverable later. Omit only when there are none.

**Verification** - Checklist format. What was tested, what was assumed, what was skipped.

**Outstanding Issues** - Blockers, risks, unfinished work.

**Hygiene Sweep** - Findings from the pre-wrap sweep: state found, actions proposed, actions taken vs declined.

**Waiting on You** - Required in every mode. Every item blocked on the maintainer's decision or action, one bullet each: what is awaited, why it blocks, and links to the relevant files. Write "Nothing pending" explicitly when the list is empty; never omit the section. Mirror the list inside the continuation prompt so the next session re-presents it.

**What's Next** - Ordered list. Most important action first. When one decision unlocks the rest, name it as the single unlocking decision.

**Continuation Prompt** - In a fenced code block. See requirements below.

### Body Sections (Quick Mode)

Summary + files changed + waiting-on + continuation prompt. That's it.

### Body Sections (Blocked Mode)

Summary + blocker detail (what, who can unblock, impact) + waiting-on + continuation prompt.

## Continuation Prompt

The single most important output. Must be:

- **Copy-paste ready** - wrapped in a fenced code block, no editing needed
- **Specific** - names exact files, branches, and next actions
- **Bounded** - one clear immediate action, then ordered secondary steps
- **Self-contained** - readable without the original session

A continuation prompt that says "continue where we left off" has failed. It must include enough context that a cold-start session can resume without re-reading anything.

### Default verbosity (v1.1.0)

**The continuation prompt defaults to the deep / verbose form in every mode** (quick, final, blocked, deep). "Verbose" means: includes the task context paragraph, the current state summary, the immediate next action, the ordered secondary actions, the relevant file paths, and the branch name. Even quick-mode sessions get the full prompt - the cost is a dozen extra lines; the benefit is a cold-start session that never has to ask "what's the context?"

The only path to a lighter continuation prompt is for the agent to state a **specific objection** (one short sentence) in the session log explaining why a lighter prompt is appropriate for this particular session. Examples of valid objections: "Session was a trivial typo fix; no context to carry forward" or "User explicitly requested a one-line prompt." Without such an objection, the verbose form is mandatory.

This default is a comply-or-explain rule: produce the verbose form, or produce a lighter form *with the explicit reason recorded*.

## Log Self-Check (before writing)

Verify the drafted log passes every gate; fix failures before writing, never after:

- Continuation prompt is self-contained (readable by a cold-start session with zero other context)
- Waiting on You section present in every mode ("Nothing pending." counts; absence does not)
- Summary is 120 characters or fewer
- Frontmatter Tier 1 complete, including `machine:`
- Every file path and link named in the log exists
- No em-dash or en-dash characters anywhere in the log

## Surrounding Document Updates

After writing the session log, check if changes warrant updates to:

- **README.md** - only if user-facing capabilities changed
- **CHANGELOG.md** - only if release-worthy (new feature, visible bugfix, breaking change)
- **Active plans** - only if sequence, scope, or assumptions changed
- **Decision records** - if an architectural decision was made this session, propose capturing it as an ADR (MADR, `docs/internal/decisions/` where the repo uses them)
- **Agent memory** - if durable facts or decisions emerged that outlive this session, confirm they are recorded in persistent memory rather than only in the log

**Before making any edit, state the intended change and ask for confirmation.** Never update surrounding docs silently.

If nothing warrants an update, move on without commenting.

## Constraints

- Never embed full transcripts - reference the transcript path only
- Never conflate "completed" with "verified" - state verification status explicitly
- Never commit, push, or modify anything beyond the session log without explicit per-action confirmation; the hygiene sweep proposes, the user disposes
- Never update surrounding docs without confirmation
- The Waiting on You section is mandatory in every mode; an empty list is stated, never omitted
- Summary must be ≤ 120 characters (for index display)
- The session log must be self-contained - readable without the original session
- Never produce an empty or generic continuation prompt
- Never produce a lighter-than-verbose continuation prompt without a stated objection (see "Default verbosity" above)
