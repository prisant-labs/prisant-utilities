# Attribution & Finding Format Guide

All LLM contributions in the review document are attributed with role, name, and date. This prevents ambiguity about who wrote what across the multi-phase workflow.

---

## Attribution Format

Two roles appear in the document:

```markdown
**Reviewer - Codex (2026-04-07):**

[Reviewer's content]

**Requestor - Claude Opus 4.6 (2026-04-07):**

[Requestor's content]
```

- **Role** comes first (Reviewer / Requestor)
- **LLM name** follows the dash - use the common name, not a model ID
- **Date** in parentheses - YYYY-MM-DD
- Bold the entire attribution line
- Reviewer always speaks first per section; requestor responds below

---

## Finding Format

Reviewers use this compact format for every finding:

```markdown
- [Severity | Confidence] Description with evidence woven in. Source says "X"
  (Section N) but also says "Y" (Section M). → Recommendation.
```

- **Severity**: Blocker, Major, Minor, Note
- **Confidence**: High, Medium, Low
- Evidence is inline, not in footnotes - cite sections, quotes, file paths
- End with an actionable recommendation after the arrow (→)

### Severity Definitions

| Severity | Meaning | Proceed? |
|----------|---------|----------|
| **Blocker** | Must resolve before proceeding. Will cause incorrect results or structural failure. | No |
| **Major** | Should resolve before proceeding. Significant gap causing confusion or rework. | Risky |
| **Minor** | Can defer. Real issue but won't prevent the work from succeeding. | Yes |
| **Note** | Observation or suggestion. No action required but worth considering. | Yes |

---

## Anti-Sycophancy Instructions

Every review document includes these instructions for the reviewer:

- "Your role is to find problems, not to validate"
- "If you find nothing wrong, that's suspicious - look harder"
- "Disagreement is more valuable than agreement"
- "Rate your confidence - low-confidence concerns are still worth noting"
- "If you find nothing wrong in a section, say so explicitly and explain WHY - don't skip it"

These are embedded in the "Instructions for Reviewer" section of the review document.

---

## Response Depth (Requestor)

When writing inline responses in `--respond` mode, scale depth to severity:

| Severity | Response depth |
|----------|---------------|
| **Blocker** | Full paragraph. State agree/disagree with evidence. Describe the specific change proposed. |
| **Major** | Full paragraph. Same structure as Blocker. |
| **Minor** | One-liner. "Agree. [brief action]." or "Disagree - [reason]." |
| **Note** | One-liner. "Noted. Deferring to backlog." or "Good point. No action needed." |

---

## Structured Decisions Format

Canonical layout for the 5-column summary table and per-decision Parts 1/2/3 block lives in `references/review-template.md`. This section names the attribution rules specific to decisions.

- **Part 1 (Context & options)** - authored by the requestor LLM during `--respond` P4. Attribution follows the standard `**Requestor - [LLM] ([date]):**` format (no separate attribution line - the whole P4 pass is requestor content).
- **Part 2 (Maintainer Response)** - authored by JP manually during P5. No LLM attribution required; label the block `**Maintainer Response** - [P5: JP fills]`.
- **Part 3 (Clarification)** - the question is written by JP (P5); the response is written by the requestor LLM on `--respond` re-run (P6). The requestor's response uses the standard attribution line: `**Requestor Response - [LLM] ([date]):**`.

### When to Create a Decision Section

- **Every Blocker and every Major finding MUST generate a per-decision section.** Non-negotiable; enforced as a skill constraint.
- Minor / Note findings may generate sections at the requestor's judgment - typically when they require priority tradeoffs the human must make.
- Multiple valid approaches with different trade-offs are a natural trigger for a section regardless of severity.
