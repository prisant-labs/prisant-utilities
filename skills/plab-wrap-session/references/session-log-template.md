# Session Log Template

Adapt section depth to the selected mode. Remove instructional comments before delivery.

---

## Final Mode

```markdown
---
date:
type: session-log
machine: # hostname
repo:
branch:
summary: # ≤ 120 chars
files-changed: []
session-type:
model: # full model name, e.g. "claude opus 4.6"
model-settings: # e.g. "extended-thinking max"
agent:
status:
decisions-count:
skills-used: []
resumed-from: # log filename if this session resumed from one
---

# Session: [Brief Title]

## Summary

<!-- 2-4 sentences. What happened and why it matters. -->

## Work Completed

<!-- Bulleted list of accomplishments. Be specific. -->

## Decisions Made

<!-- Scale verbosity to significance:
  Minor: one-liner
  Significant: 2-3 sentences with reasoning
  Architectural: full alternatives analysis + ADR reference (e.g., "See ADR-0008")
  If an ADR was created, reference it: "Created docs/decisions/0008-title.md" -->

## Files Changed

<!-- From git. Group by purpose if many. -->

## Gitignored Outputs

<!-- Work products git cannot see: path + one-liner each
  (e.g. _local/audit/..., _local/reference/...). Omit only if none. -->

## Verification

<!-- Checklist format:
  - [x] Tests passing for X
  - [x] Manual check: Y works as expected
  - [ ] Not verified: Z (reason)
-->

## Outstanding Issues

<!-- Blockers, risks, unfinished work. If none, omit section. -->

## Hygiene Sweep

<!-- Findings from the pre-wrap sweep (see references/hygiene-sweep.md):
  state found, actions proposed, actions taken vs declined.
  Include the skip note if checks were skipped. -->

## Waiting on You

<!-- REQUIRED in every mode. One bullet per item blocked on the maintainer:
  what is awaited, why it blocks, links to relevant files.
  Write "Nothing pending." explicitly when empty; never omit this section.
  Mirror the list inside the continuation prompt. -->

## What's Next

<!-- Ordered list. Most important action first.
  When one decision unlocks the rest, name it as the single unlocking decision. -->

1.
2.
3.

## Continuation Prompt

```text
[Copy-paste-ready prompt for the next session.
Must include: task context, current state, immediate next action,
key constraints, relevant file paths, branch name.]
```
```

---

## Quick Mode

```markdown
---
date:
type: session-log
machine: # hostname
repo:
branch:
summary:
files-changed: []
session-type:
model:
model-settings:
status: completed
---

# Session: [Brief Title]

[1-3 sentence summary of what happened.]

## Waiting on You

[One bullet per item awaited from the maintainer with file links, or "Nothing pending."]

## Continuation Prompt

```text
[Copy-paste-ready prompt, or "No continuation needed."]
```
```

---

## Blocked Mode

```markdown
---
date:
type: session-log
machine: # hostname
repo:
branch:
summary:
files-changed: []
session-type:
model:
model-settings:
status: blocked
---

# Session: [Brief Title]

## Summary

[What was attempted and why it's blocked.]

## Blocker

**What:** [Description of the blocker]
**Who can unblock:** [Person or action needed]
**Impact:** [What can't proceed until this is resolved]

## Waiting on You

[One bullet per item awaited from the maintainer with file links; the blocker itself belongs here when the maintainer is the unblocker.]

## Continuation Prompt

```text
[What to do when the blocker is resolved.
Include: how to verify the blocker is cleared,
then the next action to take.]
```
```

---

## Deep Mode (Default)

The default mode for every wrap since v1.3.0. Use the full Final Mode template, plus:

```markdown
## Evidence Index

<!-- Link to specific evidence for key claims:
  - "Tests pass" → link to test output or commit
  - "Performance improved" → link to benchmark
  - "Design reviewed" → link to review document
  Workflow runs, one row each when the session used multi-agent workflows:
  - run ID, agent count, token total, journal/transcript path -->

## Verification Detail

<!-- Expanded verification with method and result:
  | Check | Method | Result | Notes |
  |-------|--------|--------|-------|
  | Unit tests | `npm test` | 47/47 pass | - |
  | Manual smoke test | Opened app, tested flow | Works | Edge case X not tested |
-->
```
